#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""自审：把 audit/15 与摘要里引用的关键数字，逐项与机器输出/结果 JSON 对账。

不依赖 analyz_ 的打印格式，直接从 runs/p1/cases/*.json 重算，避免"抄错一行"。
"""
import glob
import io
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CASES = os.path.join(ROOT, "runs", "p1", "cases")

SC = ["none", "cutin", "lead-brake", "lead-exit"]

# 文档（audit/15 §2.1）里写的值，人工抄录，用于对账
DOC_COST = {
    "none": (0.256, -2.321, 2.832, 0.8125, 0.0198, 3.048),
    "cutin": (0.326, -2.467, 3.119, 0.8750, 0.0273, 3.031),
    "lead-brake": (0.858, -2.092, 3.808, 0.4375, 0.0515, 3.095),
    "lead-exit": (-0.051, -1.968, 1.867, 1.0000, 0.0060, 3.062),
}
# 文档里写的 90% CI（自审新增）
DOC_90 = {
    "none": (-1.723, 2.234),
    "cutin": (-1.818, 2.471),
    "lead-brake": (-1.407, 3.123),
    "lead-exit": (-1.523, 1.422),
}

files = sorted(glob.glob(os.path.join(CASES, "case_*.json")))
data = {}
for f in files:
    d = json.load(io.open(f, encoding="utf-8"))
    data.setdefault(d["scenario"], []).append(d)

sys.path.insert(0, os.path.join(ROOT, "src", "ctrl"))
import train_cfc as T  # noqa: E402

print("  场景           n   Δ均值(重算)  Δ均值(文档)  差   95%CI 对齐  90%CI 对齐  等价95  等价90")
bad = 0
for sc in SC:
    cs = data.get(sc, [])
    vals = [c["paired"]["delta_cost"] for c in cs]
    offs = [c["arms"]["a1_otf_off"]["best_cost"] for c in cs]
    n = len(vals)
    m = sum(vals) / n
    off_mean = sum(offs) / n
    var = sum((v - m) ** 2 for v in vals) / (n - 1)
    se = (var / n) ** 0.5
    lo, hi = m - T._t_quantile(0.975, n - 1) * se, m + T._t_quantile(0.975, n - 1) * se
    lo90, hi90 = m - T._t_quantile(0.95, n - 1) * se, m + T._t_quantile(0.95, n - 1) * se
    margin = 0.10 * abs(off_mean)
    p = T._sign_flip_p(vals)
    pt = T._tost_p(vals, margin)

    dm, dlo, dhi, dp, dpt, dmarg = DOC_COST[sc]
    ok_m = abs(m - dm) <= 0.0006
    ok_ci = abs(lo - dlo) <= 0.0015 and abs(hi - dhi) <= 0.0015
    ok_p = abs(p - dp) <= 1e-9
    ok_pt = abs(pt - dpt) <= 0.0002
    ok_marg = abs(margin - dmarg) <= 0.0015
    d90 = DOC_90[sc]
    ok_c90 = abs(lo90 - d90[0]) <= 0.0015 and abs(hi90 - d90[1]) <= 0.0015

    eq95 = lo >= -margin and hi <= margin
    eq90 = lo90 >= -margin and hi90 <= margin

    def mark(x):
        return "OK" if x else "✗"
    print("  %-12s %2d  %+10.4f  %+10.4f  %s   %s        %s        %-5s  %-5s"
          % (sc, n, m, dm, mark(ok_m), mark(ok_ci and ok_marg), mark(ok_c90),
             str(eq95), str(eq90)))
    if not (ok_m and ok_ci and ok_p and ok_pt and ok_marg and ok_c90):
        bad += 1
        print("      ✗ 不一致：p=%s(文档 %s) pt=%s(文档 %s) margin=%.3f(文档 %.3f)"
              % (round(p, 4), dp, round(pt, 4), dpt, margin, dmarg))

print()
if bad == 0:
    print("  ✓ audit/15 §2.1 与 §10 的 24 个数字（4 场景 × 均值/95%CI/p/TOST/margin + 90%CI）全部与重算一致")
else:
    print("  ✗ 有 %d 个场景存在不一致，需修正文档" % bad)

# 摘要里的两个数
print()
print("  摘要引用核对：")
print("    '+0.26' ← none 均值 %.4f  %s" % (data["none"][0]["paired"]["delta_cost"] if False else
      sum(c["paired"]["delta_cost"] for c in data["none"]) / len(data["none"]),
      "OK" if abs(sum(c["paired"]["delta_cost"] for c in data["none"]) / len(data["none"]) - 0.26) < 0.005 else "✗"))
le = sum(c["paired"]["delta_cost"] for c in data["lead-exit"]) / len(data["lead-exit"])
print("    '−0.05' ← lead-exit 均值 %.4f  %s" % (le, "OK" if abs(le + 0.05) < 0.005 else "✗"))
print("    'TOST p = 0.020 and 0.006' ← %.4f / %.4f" % (
    T._tost_p([c["paired"]["delta_cost"] for c in data["none"]],
              0.10 * abs(sum(c["arms"]["a1_otf_off"]["best_cost"] for c in data["none"]) / len(data["none"]))),
    T._tost_p([c["paired"]["delta_cost"] for c in data["lead-exit"]],
              0.10 * abs(sum(c["arms"]["a1_otf_off"]["best_cost"] for c in data["lead-exit"]) / len(data["lead-exit"])))))
sys.exit(0 if bad == 0 else 1)
