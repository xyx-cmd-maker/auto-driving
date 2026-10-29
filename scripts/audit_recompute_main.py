#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P0-2 独立复算：从 20 个预注册逐局 JSON 重建论文 Table I / Table II 与三态判定。

与 `scripts/verify_from_published_cases.py` 的区别
--------------------------------------------------
后者只算均值与 SD。本脚本按**冻结协议**（`audit/第一次组会/10-a1-protocol-freeze.md`）独立实现：
  - 精确双侧符号翻转检验（n=5，穷举 2^5）
  - 95% / 90% 配对 t 区间
  - TOST，margin = off 臂均值的 10%
  - 族内 Holm-Bonferroni（α=0.05），三个 endpoint 各自一族
  - 三态判定（有意义差异 / 实际等价 / 未定）
并逐项与论文记录值比对，任一超出容差即以退出码 1 报错（**不静默通过**）。

依赖：仅标准库（自带 t 分布 CDF，用正则化不完全 Beta 实现；含自检）。
用法：py -3.12 scripts/audit_recompute_main.py [--tol 1e-3]
"""
import argparse
import glob
import io
import json
import math
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CASES = os.path.join(ROOT, "results", "p1", "cases", "main")

SCENARIOS = ["none", "cutin", "lead-brake", "lead-exit"]
SEEDS = [0, 1, 2, 3, 4]

# 论文记录值（`audit/第一次组会/15-a1-full-results.md` 与 `_results-fragment.md` Table I/II）
PAPER = {
    "cost": {
        "mean": {"none": 0.256, "cutin": 0.326, "lead-brake": 0.858, "lead-exit": -0.051},
        "ci95": {"none": (-2.321, 2.832), "cutin": (-2.467, 3.119),
                 "lead-brake": (-2.092, 3.808), "lead-exit": (-1.968, 1.867)},
        "ci90": {"none": (-1.723, 2.234), "cutin": (-1.818, 2.471),
                 "lead-brake": (-1.407, 3.123), "lead-exit": (-1.523, 1.422)},
        "exact_p": {"none": 0.8125, "cutin": 0.8750, "lead-brake": 0.4375, "lead-exit": 1.0000},
        "tost_p": {"none": 0.0198, "cutin": 0.0273, "lead-brake": 0.0515, "lead-exit": 0.0060},
        "state": {"none": "equivalent", "cutin": "inconclusive",
                  "lead-brake": "inconclusive", "lead-exit": "equivalent"},
    },
    "rmse": {
        "mean": {"none": -4.361, "cutin": -4.767, "lead-brake": -0.761, "lead-exit": -2.317},
        "tost_p": {"none": 0.3184, "cutin": 0.3432, "lead-brake": 0.1484, "lead-exit": 0.1161},
    },
    "accel": {
        "mean": {"none": 34.47, "cutin": 40.13, "lead-brake": 46.89, "lead-exit": 8.98},
        "tost_p": {"none": 0.5786, "cutin": 0.6637, "lead-brake": 0.6435, "lead-exit": 0.2630},
    },
}


# ───────────────────────── t 分布（无 scipy） ─────────────────────────
def _betacf(a, b, x):
    """不完全 Beta 的连分式（Lentz 法）。"""
    MAXIT, EPS, FPMIN = 200, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < EPS:
            break
    return h


def betainc(a, b, x):
    """正则化不完全 Beta I_x(a,b)。"""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    ln_beta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(ln_beta + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_cdf(t, df):
    x = df / (df + t * t)
    p = 0.5 * betainc(df / 2.0, 0.5, x)
    return 1.0 - p if t > 0 else p


def t_ppf(q, df):
    lo, hi = -100.0, 100.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_cdf(mid, df) < q:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


T975_4 = t_ppf(0.975, 4)      # 期望 2.7764
T95_4 = t_ppf(0.95, 4)        # 期望 2.1318


# ───────────────────────── 统计 ─────────────────────────
def exact_signflip_p(d):
    """精确双侧符号翻转检验：p = #{|mean(s_i d_i)| >= |mean(d)|} / 2^n。"""
    n = len(d)
    obs = abs(sum(d) / n)
    cnt = 0
    for bits in range(1 << n):
        s = 1.0 if (bits & 1) else -1.0
        tot, k = 0.0, bits >> 1
        tot = s * d[0]
        for i in range(1, n):
            tot += (1.0 if (k & 1) else -1.0) * d[i]
            k >>= 1
        if abs(tot / n) >= obs - 1e-12:
            cnt += 1
    return cnt / float(1 << n)


def mean_sd(d):
    n = len(d)
    m = sum(d) / n
    var = sum((x - m) ** 2 for x in d) / (n - 1)
    return m, math.sqrt(var)


def ci(d, tcrit):
    m, s = mean_sd(d)
    se = s / math.sqrt(len(d))
    return m - tcrit * se, m + tcrit * se, se


def tost_p(d, margin):
    """TOST：p = max( P(T >= (m+margin)/se), P(T <= (m-margin)/se) )。"""
    m, s = mean_sd(d)
    se = s / math.sqrt(len(d))
    if se == 0:
        return 0.0 if abs(m) < margin else 1.0
    p1 = 1.0 - t_cdf((m + margin) / se, len(d) - 1)   # H0: μ ≤ −margin
    p2 = t_cdf((m - margin) / se, len(d) - 1)         # H0: μ ≥ +margin
    return max(p1, p2)


def holm(ps):
    """返回 (按原顺序的调整后 p, 按原顺序是否拒绝 α=0.05)。"""
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i])
    adj = [0.0] * m
    rejected = [False] * m
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * ps[i])
        adj[i] = min(1.0, running)
        rejected[i] = adj[i] < 0.05
    return adj, rejected


def three_state(ci_lo, ci_hi, mean, margin, p_tost):
    if (ci_lo > 0 or ci_hi < 0) and abs(mean) > margin:
        return "meaningful"
    if ci_lo >= -margin and ci_hi <= margin and p_tost < 0.05:
        return "equivalent"
    return "inconclusive"


# ───────────────────────── 主流程 ─────────────────────────
def load():
    out = {}
    for sc in SCENARIOS:
        rows = []
        for sd in SEEDS:
            f = os.path.join(CASES, "case_%s_s%d.json" % (sc, sd))
            if not os.path.exists(f):
                raise SystemExit("  ✗ 缺文件：%s（不静默跳过）" % f)
            rows.append(json.load(io.open(f, encoding="utf-8")))
        out[sc] = rows
    extra = sorted(glob.glob(os.path.join(CASES, "case_*.json")))
    n_files = len(extra)
    return out, n_files


def audit_exec(rows_by_sc):
    """检查 20 局的执行指纹是否一致（除场景/种子外）。"""
    keys = ("episode_s", "traffic", "sim_hz", "control_hz", "hidden", "candidates_per_arm", "elite")
    bad = []
    ref = None
    for sc, rows in rows_by_sc.items():
        for r in rows:
            e = r.get("exec", {})
            cur = tuple(e.get(k) for k in keys)
            if ref is None:
                ref = cur
            elif cur != ref:
                bad.append((sc, r.get("seed"), cur))
    return keys, ref, bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tol", type=float, default=1e-3)
    ap.add_argument("--tol-p", type=float, default=1e-3)
    args = ap.parse_args()

    rows_by_sc, n_files = load()
    print("  案例文件总数 = %d（预注册 20 + 扩展 lead-brake 5）" % n_files)
    print("  t 临界值自检：t(0.975,4)=%.4f（期望 2.7764）｜t(0.95,4)=%.4f（期望 2.1318）"
          % (T975_4, T95_4))
    print()

    keys, ref, bad = audit_exec(rows_by_sc)
    print("  执行指纹一致性：%s" % ("✓ 20 局完全一致" if not bad else "✗ 不一致 %d 处" % len(bad)))
    print("    %s = %s" % (", ".join(keys), ref))
    print()

    # 三族统计
    fam = {}
    for name, dkey in (("cost", "delta_cost"),
                       ("rmse", "delta_following_rmse"),
                       ("accel", "delta_accel_sq_integral")):
        fam[name] = {}
        for sc in SCENARIOS:
            d = [r["paired"][dkey] for r in rows_by_sc[sc]]
# margin 必须按**该端点自身**的 off 臂均值算（成本/ RMSE / 加速度三个量纲不同）
            if name == "cost":
                off_vals = [r["arms"]["a1_otf_off"]["best_cost"] for r in rows_by_sc[sc]]
            elif name == "rmse":
                off_vals = [r["arms"]["a1_otf_off"]["best_metrics"]["following_rmse_m"] for r in rows_by_sc[sc]]
            else:
                off_vals = [r["arms"]["a1_otf_off"]["best_metrics"]["accel_sq_integral_mps3"] for r in rows_by_sc[sc]]
            off_mean = sum(off_vals) / len(off_vals)
            margin = 0.10 * off_mean
            lo95, hi95, se = ci(d, T975_4)
            lo90, hi90, _ = ci(d, T95_4)
            fam[name][sc] = dict(d=d, mean=sum(d) / len(d), off_mean=off_mean, margin=margin,
                                 lo95=lo95, hi95=hi95, lo90=lo90, hi90=hi90, se=se,
                                 p_exact=exact_signflip_p(d), p_tost=tost_p(d, margin))

    for name in fam:
        ps = [fam[name][sc]["p_exact"] for sc in SCENARIOS]
        adj, rej = holm(ps)
        for i, sc in enumerate(SCENARIOS):
            fam[name][sc]["p_holm"] = adj[i]
            fam[name][sc]["holm_reject"] = rej[i]

    fails = []
    print("  === cost（主终点）===")
    print("  %-11s %7s %8s %23s %23s %8s %8s %6s %9s" % (
        "场景", "mean", "SD", "95% CI", "90% CI", "exact_p", "holm_p", "margin", "TOST p"))
    for sc in SCENARIOS:
        s = fam["cost"][sc]
        st = three_state(s["lo95"], s["hi95"], s["mean"], s["margin"], s["p_tost"])
        s["state"] = st
        print("  %-11s %+7.3f %8.3f  [%+7.3f,%+7.3f]  [%+7.3f,%+7.3f] %8.4f %8.4f %6.3f %9.4f  %s" % (
            sc, s["mean"], mean_sd(s["d"])[1], s["lo95"], s["hi95"], s["lo90"], s["hi90"],
            s["p_exact"], s["p_holm"], s["margin"], s["p_tost"], st))

        p = PAPER["cost"]
        for label, got, want, tol in (
            ("mean", s["mean"], p["mean"][sc], args.tol),
            ("pi95_lo", s["lo95"], p["ci95"][sc][0], args.tol),
            ("pi95_hi", s["hi95"], p["ci95"][sc][1], args.tol),
            ("pi90_lo", s["lo90"], p["ci90"][sc][0], args.tol),
            ("pi90_hi", s["hi90"], p["ci90"][sc][1], args.tol),
            ("exact_p", s["p_exact"], p["exact_p"][sc], args.tol_p),
            ("tost_p", s["p_tost"], p["tost_p"][sc], 1e-4),
        ):
            if abs(got - want) > tol:
                fails.append((sc, label, got, want))
        if st != p["state"][sc]:
            fails.append((sc, "state", st, p["state"][sc]))

    for name, dkey, label in (("rmse", "delta_following_rmse", "Δ following RMSE (m)"),
                              ("accel", "delta_accel_sq_integral", "Δ accel. integral")):
        print()
        print("  === %s ===" % label)
        print("  %-11s %9s %8s %23s %9s" % ("场景", "mean", "SD", "95% CI", "TOST p"))
        for sc in SCENARIOS:
            s = fam[name][sc]
            print("  %-11s %+9.3f %8.3f  [%+8.3f,%+8.3f] %9.4f" % (
                sc, s["mean"], mean_sd(s["d"])[1], s["lo95"], s["hi95"], s["p_tost"]))
            p = PAPER[name]
            if abs(s["mean"] - p["mean"][sc]) > max(args.tol, 0.01):
                fails.append((sc, name + "_mean", s["mean"], p["mean"][sc]))
            if abs(s["p_tost"] - p["tost_p"][sc]) > args.tol_p:
                fails.append((sc, name + "_tost_p", s["p_tost"], p["tost_p"][sc]))

    print()
    print("  === 无效候选率（冻结协议要求逐局报告）===")
    print("  逐局明细：")
    for sc in SCENARIOS:
        off = [round(r["arms"]["a1_otf_off"]["invalid_ratio"], 3) for r in rows_by_sc[sc]]
        on = [round(r["arms"]["a1_otf_on"]["invalid_ratio"], 3) for r in rows_by_sc[sc]]
        print("    %-11s off=%s  on=%s" % (sc, off, on))
    for sc in SCENARIOS:
        off = [r["arms"]["a1_otf_off"]["invalid_ratio"] for r in rows_by_sc[sc]]
        on = [r["arms"]["a1_otf_on"]["invalid_ratio"] for r in rows_by_sc[sc]]
        print("  %-11s off %.3f ｜ on %.3f" % (sc, sum(off) / len(off), sum(on) / len(on)))

    print()
    if fails:
        print("  ✗ 与论文记录不一致 %d 处：" % len(fails))
        for sc, lab, got, want in fails[:20]:
            print("     %-11s %-12s got %.4f  want %.4f" % (sc, lab, got, want))
        return 1
    print("  ✓ 全部与论文记录一致（tol=%.0e / p-tol=%.0e）" % (args.tol, args.tol_p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
