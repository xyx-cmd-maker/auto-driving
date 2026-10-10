#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P1 合成 OTF 与论文表 3.3–3.7 的对拍

**只比两件可迁移的事**（绝对值不可比，协议不同；AGENTS.md §1）：
  P1 符号：OTF 的符号 = sign(自车车速 − 邻车道平均车速)
  P2 过渡：符号在"自车车速 ≈ 邻车平均车速"附近由负转正

**明确不可比的地方（量纲差异，必须写明，不要糊过去）**
  论文报的 OTF 占比来自**实车**试验：单车道高速场景，随车速分组（60/80/100/120 km/h），
  其加权均值跨窗口几乎不变（约 −0.15 / −0.05 / +0.04 / +0.18），说明该量已被**归一化**
  （量级 ~0.1，与"每窗口净超车数"这种 ~1–10 的计数型随机量不同量纲）。
  本项目报的是**每窗口净超车数**（未归一化的计数），因此**绝对值与论文相差 1–2 个数量级，
  不得并列比较**；可比的只有符号与过渡位置。

用法：python src/otf/compare_with_paper.py
"""
import glob
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PAPER = os.path.join(ROOT, "configs", "p1", "paper_tables_3_3_to_3_7.json")
RESDIR = os.path.join(ROOT, "results", "p1")

AMBIENT_SLOW, AMBIENT_FAST = 13.0, 32.0
AMBIENT_MEAN = (AMBIENT_SLOW + AMBIENT_FAST) / 2.0     # 22.5 m/s 邻车道平均速度
DEADBAND = 0.5                                          # |相对差| < 此值算"接近零"


def weighted_mean(fracs):
    return sum(float(k) * v for k, v in fracs.items())


def paper_wmean(tables, window, speed):
    t = tables.get(str(window))
    if not t:
        return None
    acc = tot = 0.0
    for otf, row in t.items():
        pct = row.get(str(speed), 0.0)
        acc += float(otf) * pct
        tot += pct
    return acc / tot if tot else None


def main():
    tables = None
    if os.path.exists(PAPER):
        tables = json.load(io.open(PAPER, encoding="utf-8"))["tables"]

    if tables:
        print("=" * 84)
        print("基准：论文表 3.3–3.7（实车报告值，协议不同，绝对值不可比）")
        print("=" * 84)
        print("  %-8s %-11s %-11s %-11s %-11s" % ("窗口", "60km/h", "80km/h", "100km/h", "120km/h"))
        for w in [5, 10, 20, 30, 60]:
            row = [paper_wmean(tables, w, s) for s in (60, 80, 100, 120)]
            print("  %-8s %-11s %-11s %-11s %-11s"
                  % ("%ds" % w, *["%+.3f" % v for v in row]))
        print("  → 符号：60/80 km/h 为负，100/120 km/h 为正；且均值跨窗口基本不变（≈±0.15/±0.19）")
        print("  → 该量已归一化（量级 ~0.1），与本项目的'每窗口净超车数'（~1–10）**不同量纲**")

    files = sorted(glob.glob(os.path.join(RESDIR, "*.json")))
    if not files:
        print("\n尚未找到结果文件：%s" % RESDIR)
        return 3

    # ── 车速扫描：符号与过渡 ──
    # ★ 只取 5 s 窗口（论文表 3.3 口径）。结果文件按窗口逐个覆盖同一文件名，
    #   故磁盘上留下的是最后一个窗口（60 s）；这里显式跳过非目标窗口，避免读到 60 s。
    TARGET_W = 5
    rows = []
    for f in files:
        doc = json.load(io.open(f, encoding="utf-8"))
        o = doc["metrics"]["otf"]
        if o.get("window_s") != TARGET_W:
            continue
        spd = o.get("probe_speed_mps")
        if spd is None:
            continue
        rows.append({"file": os.path.basename(f), "speed": spd,
                     "wm": weighted_mean(o["distribution_fractions"]),
                     "sign": o.get("sign"), "n_ot": sum(v["N_ot"] for v in
                                                         o["per_seed_run_meta"].values()),
                     "n_otn": sum(v["N_otn"] for v in o["per_seed_run_meta"].values())})
    by_speed = {}
    for r in rows:
        key = round(r["speed"], 3)
        if key not in by_speed or "_speed" in r["file"]:
            by_speed[key] = r
    rows = sorted(by_speed.values(), key=lambda r: r["speed"])

    print()
    print("=" * 84)
    print("本项目：探测车速扫描（SUMO 合成，窗口 %d s）" % TARGET_W)
    print("=" * 84)
    print("  邻车道设定：lane0 = %.0f m/s（与探测车左侧相邻），lane2 = %.0f m/s（右侧相邻）"
          % (AMBIENT_SLOW, AMBIENT_FAST))
    print("  ★ 探测车在 lane1，两侧邻车速度不同 ⇒ **不存在单一'邻车平均速度'**；")
    print("    只要探测车速低于两侧中的较快者，就会同时产生超车与被超车。")
    print()
    print("  %-10s %-11s %-9s %-9s %-10s %-9s %s"
          % ("探测车速", "OTF均值", "N_ot", "N_otn", "otn占比", "观测符号", "预期方向"))
    ok = True
    for r in rows:
        rel_slow = r["speed"] - AMBIENT_SLOW      # 相对慢流（lane0）
        rel_fast = r["speed"] - AMBIENT_FAST      # 相对快流（lane2）
        # 预期：比慢流快 ⇒ 有超车；比快流慢 ⇒ 有被超车
        expect = ("超车为主" if rel_slow > 0 and rel_fast >= 0 else
                  "被超为主" if rel_slow <= 0 and rel_fast < 0 else
                  "两者并存")
        mix = r["n_otn"] / float(r["n_ot"] + r["n_otn"]) if (r["n_ot"] + r["n_otn"]) else 0
        got = "+" if r["wm"] > 0.005 else ("-" if r["wm"] < -0.005 else "0")
        # 只有"纯被超"与"纯超车"两端可以硬判；中间态由 otn 占比描述
        if expect == "被超为主":
            hit = (got == "-")
        elif expect == "超车为主":
            hit = (got == "+")
        else:
            hit = None
        ok = ok and (hit is not False)
        print("  %-10s %-11.4f %-9d %-9d %-10.3f %-9s %s"
              % ("%.0f m/s" % r["speed"], r["wm"], r["n_ot"], r["n_otn"], mix, got,
                 expect + ("" if hit is None else (" OK" if hit else " MISS"))))

    print()
    print("  读法：随着探测车速升高，N_otn 单调下降（被超车变少）、N_ot 上升（超车变多），")
    print("        OTF 由负转正 —— 这就是与论文同向的趋势（论文：60→120 km/h 由 −0.15 转 +0.19）。")
    if len(rows) >= 2:
        print("  P1 符号翻转：存在 = %s（%.0f m/s 侧为 %s，%.0f m/s 侧为 %s）"
              % ((rows[0]["wm"] > 0) != (rows[-1]["wm"] > 0),
                 rows[0]["speed"], rows[0]["sign"], rows[-1]["speed"], rows[-1]["sign"]))

    # ── 四类工况对比（同一探测车速）──
    print()
    print("=" * 84)
    print("四类工况对比（探测车速 23 m/s，各工况的每窗口净超车数）")
    print("=" * 84)
    print("  %-14s %-10s %-9s %-9s %-11s %s" % ("工况", "窗口", "N_ot", "N_otn", "OTF均值", "文件"))
    for f in files:
        doc = json.load(io.open(f, encoding="utf-8"))
        o = doc["metrics"]["otf"]
        if o.get("probe_speed_mps") != 23.0:
            continue
        if "_speed" in os.path.basename(f):
            continue
        pm = o["per_seed_run_meta"]
        print("  %-14s %-10s %-9d %-9d %-11.4f %s"
              % (doc["experiment"].replace("main_otf_cfc_", ""), "%ds" % o["window_s"],
                 sum(v["N_ot"] for v in pm.values()), sum(v["N_otn"] for v in pm.values()),
                 weighted_mean(o["distribution_fractions"]), os.path.basename(f)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
