#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A1 消融（合成版）：OTF 对短时事件的**预测信息增量**。

为什么是"信息量版"而不是"闭环控制版"
------------------------------------
闭环 A1 需要 CfC 控制器 + 闭环被控对象；本机无 GPU、CARLA 未建（AGENTS.md §2/§3）。
但红队 R1 的核心质疑是"**OTF 是事后统计量，拿它当控制输入是滞后量**"——这个质疑
**不需要控制器就能先验检验**：若 OTF 对近未来事件（前车急减速/驶离）没有增量预测力，
那么把它接进控制器也不可能凭空产生前瞻性。因此本轮先做信息量版，作为 A1 的第一道闸。

设计
----
- 同一批轨迹上做同一预测任务，两臂只差特征集：
    A1-off: ttc_min, gap_min, rel_speed_min, ego_speed, density_adj
    A1-on : 上式 + OTF（静态窗 5/10/20 s 或自有近似的动态窗）
- 敏感性（红队要求，一次只改一个因素）：
    因素① 跟驰模型 Krauss vs IDM
    因素② 窗函数 静态 vs 动态（动态窗为本项目**自有近似**，非论文式(3.13)复现）
- 统计：5 折 GroupKFold（按 run 分组，防同轨迹泄漏）× 5 个随机种子；报 mean±std 与 ΔAUC 95% CI。

产出：results/p1/ablation_a1_otf-info_highway-mixed_s1.json（mode: real，证据等级 C）
边界：SUMO 合成交通流，**不是 CARLA、不是实车**。
"""
import argparse
import hashlib
import json
import os
import sys
from collections import defaultdict

import numpy as np
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

SUMOHOME = os.environ.get("SUMO_HOME", r"D:\SUMO\sumo-1.27.1")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(ROOT, "configs", "p1", "params.frozen.yaml")
NET = os.path.join(ROOT, "configs", "p1", "sumo_highway.net.xml")
META = os.path.join(ROOT, "configs", "p1", "sumo_highway.meta.json")
OUT = os.path.join(ROOT, "results", "p1", "ablation_a1_otf-info_highway-mixed_s1.json")

SAMPLE_DT_S = 2.0        # 决策时刻采样间隔
HIST_S = 20.0            # 保留多长的历史用于 OTF 计数
PROX_M = 100.0           # 相邻车道"附近"的纵向距离阈值
DT_FWD = 3.0             # 预测时域
BRAKE_MPS = 2.0          # 前车减速判定阈值
NO_LEAD_TTC = 15.0
NO_LEAD_GAP = 150.0
LANES = {"slow": 0, "probe": 1, "fast": 2}


def load_cfg():
    with open(CFG, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def cfg_hash(cfg, model, window_mode):
    payload = json.dumps({"cfg": cfg, "model": model, "window": window_mode},
                         sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def dyn_window(vdiff, cfg):
    """自有近似的动态时间窗（NOT the thesis Eq.3.13）——只用于敏感性检查。"""
    d = cfg["otf"]["dynamic_window"]
    x = min(abs(vdiff) / d["speed_diff_ref_mps"], 1.0)
    w = d["base_s"] * (1.0 - d["speed_diff_gain"] * x / 2.0)
    return float(min(max(w, d["min_s"]), d["max_s"]))


def run_sim(seed, model, scenario, cfg, ego_speed, total_charge_cb=None):
    """跑一次 SUMO，收集逐样本记录（决策时刻快照 + 目标 + 历史）。"""
    sys.path.append(os.path.join(SUMOHOME, "tools"))
    import traci

    meta = json.load(open(META, encoding="utf-8"))
    east, west = meta["east_edge"]["id"], meta["west_edge"]["id"]
    step = cfg["simulation"]["step_length_s"]
    end = cfg["simulation"]["sim_end_s"]

    traci.start([os.path.join(SUMOHOME, "bin", "sumo.exe"), "-n", NET, "--seed", str(seed),
                 "--step-length", str(step), "--end", str(end), "--no-step-log", "true",
                 "--no-warnings", "true", "--time-to-teleport", "-1",
                 "--collision.action", "warn", "--default.carfollowmodel", model])

    speeds = dict(cfg["traffic"]["speed_limits_mps"])
    speeds["probe"] = ego_speed
    for tid, spd in speeds.items():
        traci.vehicletype.copy("DEFAULT_VEHTYPE", tid)
        traci.vehicletype.setMaxSpeed(tid, spd)
        traci.vehicletype.setAccel(tid, 2.6)
        traci.vehicletype.setDecel(tid, 4.5)
    traci.route.add("route_east", [east])
    traci.route.add("route_west", [west])

    prob = {k: v * step / 3600.0 for k, v in cfg["traffic"]["flows_vph"].items()}
    acc, seq, fail = defaultdict(float), defaultdict(int), defaultdict(int)

    # 历史缓冲：veh -> [(t, pos, lane, speed)]
    hist = defaultdict(list)
    # 待定目标：veh -> [(t_decision, rec_index)]，用于 dt 后回填
    pending = defaultdict(list)
    records = []
    t = 0.0
    while t <= end:
        traci.simulationStep()
        t = round(traci.simulation.getTime(), 3)
        if t > end:
            break

        # 注入（与 run_p1_scenarios.py 同口径）
        for kind, lane in LANES.items():
            acc[kind] += prob[kind]
            while acc[kind] >= 1.0:
                acc[kind] -= 1.0
                vid = "%s.%d.%d" % (kind, seed, seq[kind]); seq[kind] += 1
                try:
                    traci.vehicle.add(vid, "route_east", typeID=kind, departLane=str(lane),
                                      departSpeed="max", departPos="base")
                except Exception:
                    fail[kind] += 1
        acc["opposite"] += prob["opposite"]
        while acc["opposite"] >= 1.0:
            acc["opposite"] -= 1.0
            vid = "opp.%d.%d" % (seed, seq["opposite"]); seq["opposite"] += 1
            try:
                traci.vehicle.add(vid, "route_west", typeID="opposite",
                                  departSpeed="max", departPos="base")
            except Exception:
                fail["opposite"] += 1

        ids = traci.vehicle.getIDList()
        # 采样本帧状态
        if t >= cfg["simulation"]["warmup_s"]:
            for v in ids:
                hist[v].append((t, traci.vehicle.getLanePosition(v),
                                traci.vehicle.getLaneIndex(v), traci.vehicle.getSpeed(v)))

        # 决策时刻
        if t >= cfg["simulation"]["warmup_s"] and abs(t / SAMPLE_DT_S - round(t / SAMPLE_DT_S)) < 1e-6:
            for ego in ids:
                if traci.vehicle.getTypeID(ego) != cfg["traffic"]["ego_type"]:
                    continue
                if traci.vehicle.getRoadID(ego) != east:
                    continue
                ego_pos = traci.vehicle.getLanePosition(ego)
                ego_lane = traci.vehicle.getLaneIndex(ego)
                ego_spd = traci.vehicle.getSpeed(ego)

                lead = None; lead_gap = None; lead_rel = None
                for v in ids:
                    if v == ego or traci.vehicle.getRoadID(v) != east:
                        continue
                    if traci.vehicle.getLaneIndex(v) != ego_lane:
                        continue
                    gap = traci.vehicle.getLanePosition(v) - ego_pos
                    if gap > 0 and (lead_gap is None or gap < lead_gap):
                        lead_gap, lead, lead_rel = gap, v, traci.vehicle.getSpeed(v) - ego_spd
                if lead is None:
                    ttc, gap_f, rel_f = NO_LEAD_TTC, NO_LEAD_GAP, 0.0
                else:
                    ttc = min(lead_gap / max(-lead_rel, 1e-6), NO_LEAD_TTC) if lead_rel < 0 else NO_LEAD_TTC
                    gap_f, rel_f = lead_gap, lead_rel

                # 相邻车道近域车辆（两向）
                adj = 0
                for v in ids:
                    if v == ego or traci.vehicle.getRoadID(v) != east:
                        continue
                    if abs(traci.vehicle.getLaneIndex(v) - ego_lane) != 1:
                        continue
                    if abs(traci.vehicle.getLanePosition(v) - ego_pos) <= PROX_M:
                        adj += 1

                records.append({
                    "run": "%s|%s|%d" % (model, "dyn" if cfg["_window_mode"] == "dynamic" else "stat", seed),
                    "t": t, "ego": ego, "road": east,
                    "ego_pos": ego_pos, "ego_lane": ego_lane, "ego_speed": ego_spd,
                    "ttc_min": round(ttc, 3), "gap_min": round(gap_f, 3), "rel_speed_min": round(rel_f, 3),
                    "density_adj": adj, "lead": lead,
                    "_idx": len(records), "y": None,
                })
                pending[(ego, round(t + DT_FWD, 3))].append(len(records) - 1)

        # 回填目标：dt 后判定前车是否减速/消失
        for (ego, due), idxs in list(pending.items()):
            if t + 1e-6 >= due:
                for i in idxs:
                    r = records[i]
                    if r["lead"] is None:
                        r["y"] = 1          # 触发时无前车 → 标记为 1（驶离/无前车）
                    else:
                        try:
                            if r["lead"] not in traci.vehicle.getIDList():
                                raise KeyError("left network")
                            spd_now = traci.vehicle.getSpeed(r["lead"])
                            lane_now = traci.vehicle.getLaneIndex(r["lead"])
                            r["y"] = int(spd_now <= r["ego_speed"] + r["rel_speed_min"] - BRAKE_MPS
                                         or lane_now != r["ego_lane"])
                        except Exception:
                            r["y"] = 1      # 前车消失（驶离/离开路网）
                del pending[(ego, due)]

    # ── OTF 计数：按 run 建一次结构，逐秒推进枚举（避免 O(样本×窗×车辆)）──
    windows = list(cfg["otf"]["windows_s"])
    w_max = max(windows)
    if cfg["_window_mode"] == "dynamic":
        w_max = max(w_max, cfg["otf"]["dynamic_window"]["max_s"])
    per_run = defaultdict(list)
    for rec in records:
        per_run[rec["run"]].append(rec)

    for rk, recs in per_run.items():
        recs.sort(key=lambda x: x["t"])
        velist = [v for v in hist.keys()]
        # by_v[v][t] = (pos, lane, speed)
        by_v = {}
        for v in velist:
            tv = {}
            for (tt, pp, ll, ss) in hist[v]:
                tv[round(tt, 3)] = (pp, ll, ss)
            by_v[v] = tv
        for r in recs:
            t0, ego, elane = r["t"], r["ego"], r["ego_lane"]
            # 1 秒网格：t0-w .. t0
            secs = [round(t0 - k, 3) for k in range(0, int(w_max) + 1)]
            ot_by_w = {w: 0 for w in windows + (["dyn"] if cfg["_window_mode"] == "dynamic" else [])}
            wd = dyn_window(r["rel_speed_min"], cfg) if cfg["_window_mode"] == "dynamic" else None
            for v, tv in by_v.items():
                if v == ego:
                    continue
                prev = None
                for ts in sorted([x for x in tv.keys() if t0 - w_max <= x <= t0]):
                    cur = tv[ts]
                    if prev is not None:
                        p, c = prev[1], cur
                        age = t0 - ts
                        d = c[0] - p[0]
                        if abs(d) > 1e-9:
                            pass_lane = c[1] if d > 0 else p[1]
                            other_lane = p[1] if d > 0 else c[1]
                            if pass_lane == elane and abs(other_lane - elane) == 1:
                                for w in windows:
                                    if age <= w:
                                        ot_by_w[w] += (1 if d > 0 else -1)
                                if wd is not None and age <= wd:
                                    ot_by_w["dyn"] += (1 if d > 0 else -1)
                    prev = (ts, cur)
            for w in windows:
                r["otf_w%d" % w] = ot_by_w[w]
            if wd is not None:
                r["otf_dyn"] = ot_by_w["dyn"]
                r["win_dyn_s"] = round(wd, 2)

    traci.close()
    return records, dict(fail)


def featurize(records, window_mode, with_otf):
    base = ["ttc_min", "gap_min", "rel_speed_min", "ego_speed", "density_adj"]
    extra = ["otf_dyn"] if window_mode == "dynamic" else ["otf_w5", "otf_w10", "otf_w20"]
    cols = base + (extra if with_otf else [])
    rows = [r for r in records if r["y"] is not None]
    X = np.array([[r.get(c, 0.0) for c in cols] for r in rows], dtype=float)
    y = np.array([r["y"] for r in rows], dtype=int)
    g = np.array([r["run"] for r in rows])
    return X, y, g, cols


def arm_metrics(X, y, g, seed):
    """5 折 GroupKFold（按 run 分组）× 指定随机种子，返回折内 AUC/Brier。"""
    n_groups = len(set(g))
    k = min(5, n_groups)
    if k < 2:
        return None
    gkf = GroupKFold(n_splits=k)
    aucs, briers = [], []
    for tr, te in gkf.split(X, y, groups=g):
        if len(set(y[tr])) < 2 or len(set(y[te])) < 2:
            continue
        sc = StandardScaler().fit(X[tr])
        clf = LogisticRegression(max_iter=2000, random_state=seed)
        clf.fit(sc.transform(X[tr]), y[tr])
        p = clf.predict_proba(sc.transform(X[te]))[:, 1]
        aucs.append(roc_auc_score(y[te], p))
        briers.append(brier_score_loss(y[te], p))
    if not aucs:
        return None
    return {"auc": float(np.mean(aucs)), "auc_fold_std": float(np.std(aucs)),
            "auc_per_fold": [float(a) for a in aucs],
            "brier": float(np.mean(briers)), "brier_fold_std": float(np.std(briers)),
            "folds": len(aucs)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="Krauss,IDM")
    ap.add_argument("--window-modes", default="static,dynamic")
    ap.add_argument("--seeds", default="0,1,2,3,4")
    ap.add_argument("--ego-speed", type=float, default=23.0)
    ap.add_argument("--stat-seeds", default="0,1,2,3,4")
    ap.add_argument("--quick", action="store_true", help="只跑 1 模型 1 窗型 2 种子（冒烟）")
    args = ap.parse_args()

    cfg = load_cfg()
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    wmodes = [w.strip() for w in args.window_modes.split(",") if w.strip()]
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    if args.quick:
        models, wmodes, seeds = models[:1], wmodes[:1], seeds[:2]

    all_records, per_run = [], {}
    run_meta = {}
    for model in models:
        for wm in wmodes:
            cfg["_window_mode"] = wm
            for sd in seeds:
                rec, fail = run_sim(sd, model, "none", cfg, args.ego_speed)
                all_records.extend(rec)
                key = "%s|%s|%d" % (model, "dyn" if wm == "dynamic" else "stat", sd)
                per_run[key] = len([r for r in rec if r["y"] is not None])
                run_meta[key] = {"model": model, "window_mode": wm, "seed": sd,
                                 "n_records": len(rec), "insert_fail": fail}
                print("  run %-22s records=%d labeled=%d" % (key, len(rec), per_run[key]))

    stat_seeds = [int(s) for s in args.stat_seeds.split(",") if s.strip()]
    results = {}
    for model in models:
        for wm in wmodes:
            sel = [r for r in all_records if r["run"].startswith("%s|%s|" % (model, "dyn" if wm == "dynamic" else "stat"))
                   and r["y"] is not None]
            if not sel:
                continue
            X_off, y, g, cols_off = featurize(sel, wm, with_otf=False)
            X_on, _, _, cols_on = featurize(sel, wm, with_otf=True)
            off = [arm_metrics(X_off, y, g, s) for s in stat_seeds]
            on = [arm_metrics(X_on, y, g, s) for s in stat_seeds]
            off = [o for o in off if o]; on = [o for o in on if o]
            if not off or not on:
                continue
            d_auc = np.array([o["auc"] for o in on]) - np.array([o["auc"] for o in off])
            d_bri = np.array([o["brier"] for o in on]) - np.array([o["brier"] for o in off])
            # 折级配对差（比跨种子 CI 更诚实：跨种子在此设计下是确定性的，CI 会退化成点）
            fold_pairs = list(zip([o["auc_per_fold"] for o in off], [o["auc_per_fold"] for o in on]))
            fold_d = [np.mean(np.array(b) - np.array(a)) for a, b in fold_pairs
                      if len(a) == len(b) and len(a) > 0]
            fold_d = np.array(fold_d) if fold_d else np.array([float(np.mean(d_auc))])
            key = "%s|%s" % (model, wm)
            results[key] = {
                "n_samples": int(len(y)), "n_runs": len(set(g)), "positive_rate": float(np.mean(y)),
                "features_off": cols_off, "features_on": cols_on,
                "a1_off": {"auc_mean": float(np.mean([o["auc"] for o in off])),
                           "auc_fold_std": float(np.mean([o["auc_fold_std"] for o in off])),
                           "brier_mean": float(np.mean([o["brier"] for o in off]))},
                "a1_on": {"auc_mean": float(np.mean([o["auc"] for o in on])),
                          "auc_fold_std": float(np.mean([o["auc_fold_std"] for o in on])),
                          "brier_mean": float(np.mean([o["brier"] for o in on]))},
                "delta_auc_mean": float(np.mean(d_auc)),
                # 折级离散：用范围(max-min)而非 std —— 5 个折差若落在同一浮点网格上，std 会因
                # "同数相减"退化，而范围仍能反映"估得准不准"。另附逐折值供复核。
                "delta_auc_fold_spread": float(np.max(fold_d) - np.min(fold_d)),
                "delta_auc_per_fold": [float(x) for x in fold_d],
                # 跨种子 CI：仅当种子间确有差异时才有意义，否则显式置 null，避免"假 CI"
                "delta_auc_ci95": (None if float(np.std(d_auc)) < 1e-12 else
                                   [float(np.mean(d_auc) - 1.96 * np.std(d_auc) / np.sqrt(len(d_auc))),
                                    float(np.mean(d_auc) + 1.96 * np.std(d_auc) / np.sqrt(len(d_auc)))]),
                "delta_auc_ci95_note": ("跨 CV 随机种子的 ΔAUC 完全一致 → CI 退化为点，不予报告；"
                                        "不确定性以 delta_auc_fold_spread（折级配对差的范围）表达"),
                "delta_brier_mean": float(np.mean(d_bri)),
            }

    # 敏感性判定：模型间与窗型间 ΔAUC 符号是否一致
    signs = {k: (1 if v["delta_auc_mean"] > 0 else -1) for k, v in results.items()}
    consistent = len(set(signs.values())) == 1 if signs else False
    # "与 0 不可区分" 判据：折级配对差的**范围**跨过 0（CI 在此设计下退化，故不用 CI 判定）
    indistinguishable = {k: bool(np.min(v["delta_auc_per_fold"]) <= 0 <= np.max(v["delta_auc_per_fold"]))
                         for k, v in results.items()}

    payload = {
        "paper": "p1", "experiment": "ablation_a1_otf-info", "scenario": "highway-mixed",
        "seedset": "s1", "seeds": seeds,
        "seed_semantics": "SUMO --seed（交通流随机性）；统计侧另有 5 个 CV 随机种子",
        "config_path": "configs/p1/params.frozen.yaml + configs/p1/ablation_a1.yaml",
        "config_hash": cfg_hash(cfg["otf"], models, wmodes),
        "mode": "real",
        "platform": {"kind": "simulator", "detail": "Eclipse SUMO %s；合成高速三车道混行" % cfg["simulation"]["step_length_s"]},
        "provenance": "ours-reproduced",
        "metrics": {"per_scenario": results},
        "aggregates": {"method": "mean-std", "values": {"sensitivity": {"sign_consistent": consistent,
                                                                       "signs": signs,
                                                                       "indistinguishable_from_zero": indistinguishable}},
                       "n_seeds": len(stat_seeds)},
        "fairness": {"no_privileged_inputs": False,
                     "equal_tuning_budget": True, "same_map_and_seeds": True},
        "failure_modes": [],
        "notes": {
            "abandoned_settings": [
                "闭环控制版 A1：需 CfC 控制器与闭环被控对象，本机无 GPU、CARLA 未建 → 推迟",
                "更多决策采样密度（0.5 s）：样本量翻倍但组内相关增强，本轮取 2 s",
            ],
            "known_biases": [
                "SUMO 合成交通流；Krauss/IDM 跟驰模型本身决定 OTF 与跟车行为的耦合 → 结论不可外推到真实混行",
                "动态窗为本项目自有近似，非论文式(3.13)复现 → 仅用于判断'窗函数形式是否改变结论'",
                "无前车样本按 ttc=15 s / gap=150 m 编码（右删失），可能弱化 TTC 的判别力",
                "正类定义含'前车消失=驶离'，与'前车急刹'混合为一个标签 → 后续应拆分",
            ],
            "evidence_grade": "C（仿真）",
            "wording_limit": "在 SUMO 合成交通流中",
        },
        "snapshot_date": "2026-10-11",
        "run_meta": run_meta,
    }

    OUT_DIR = os.path.dirname(OUT)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print("\nSAVED: %s" % OUT)
    for k, v in results.items():
        print("  %-14s AUC off=%.4f on=%.4f  d=%+.5f (fold_spread=%.5f)  n=%d pos=%.3f"
              % (k, v["a1_off"]["auc_mean"], v["a1_on"]["auc_mean"], v["delta_auc_mean"],
                 v["delta_auc_fold_spread"], v["n_samples"], v["positive_rate"]))
    print("  sign consistent: %s | signs: %s" % (consistent, signs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
