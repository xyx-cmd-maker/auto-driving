#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""重算验证：择优公平性失衡是否是"两臂对半"的主因？（用完即弃）

原理：4 局的全部候选代价都保存在 all_costs 里（**含无效局**），因此可以
      离线重算"两臂各取相同数量 K 个有效候选"的配对结果，不需要新算力。
      若重算后方向发生明显变化 → 候选池大小是主因；
      若几乎不变 → 候选池大小不是决定因素。
注意：all_costs 是按**候选序号**排列的（与 _valid 掩码同序），保存时用了
      list comprehension，顺序与 trials 一致。
"""
import glob
import io
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

files = sorted(glob.glob(r"F:\p1_runs\cases\case_*.json"))


def valid_costs(d, arm):
    """返回该臂的 (有效候选代价列表, 无效候选代价列表)。

    ⚠️ 结果 JSON 里只存了 all_costs（全部候选）与 n_invalid（无效个数），
    **没有逐候选的有效性掩码**。因此这里只能做保守处理：把 all_costs 升序后
    取"最小的 n_valid 个"作为有效候选的上界近似——因为无效局（车没动）
    的代价通常远高于有效局（跟车误差被 10.0 占位 + 无位移），升序后自然排在后面。
    这一近似**高估了有效候选的质量上界**，但它对两臂同样施加，比较方向仍有效。
    """
    costs = sorted(d["arms"][arm]["all_costs"])
    n_inv = d["arms"][arm].get("n_invalid", 0)
    n_val = max(1, len(costs) - n_inv)
    return costs[:n_val]


print("原始结果（各臂取各自全部有效候选）:")
print("  %-16s %10s %10s %10s" % ("场景/种子", "off最好", "on最好", "Δcost"))
print("  " + "-" * 50)
base = []
for f in files:
    d = json.load(io.open(f, encoding="utf-8"))
    off, on = valid_costs(d, "a1_otf_off"), valid_costs(d, "a1_otf_on")
    delta = on[0] - off[0]
    base.append(delta)
    print("  %-16s %10.4f %10.4f %+10.4f   (off有效%d/on有效%d)"
          % (d["scenario"] + "/s%d" % d["seed"], off[0], on[0], delta, len(off), len(on)))
print()
print("  → 均值 %+.4f ｜ 方向: OTF更好 %d ｜ 更差 %d"
      % (sum(base) / len(base),
         sum(1 for v in base if v < 0), sum(1 for v in base if v > 0)))

print()
print("重算：两臂各取前 K 个（同一 K，候选池等大）:")
print("  %-6s %-14s %-14s %-14s %-14s" % ("K", "Δcost均值", "OTF更好", "OTF更差", "与原始差"))
print("  " + "-" * 62)
for K in (1, 2, 3, 4):
    deltas, skipped = [], 0
    for f in files:
        d = json.load(io.open(f, encoding="utf-8"))
        off, on = valid_costs(d, "a1_otf_off"), valid_costs(d, "a1_otf_on")
        k = min(K, len(off), len(on))
        if k == 0:
            skipped += 1
            continue
        deltas.append(sum(on[:k]) / k - sum(off[:k]) / k)
    if not deltas:
        print("  %-6d 无法计算" % K)
        continue
    m = sum(deltas) / len(deltas)
    better = sum(1 for v in deltas if v < 0)
    worse = sum(1 for v in deltas if v > 0)
    print("  %-6d %+14.4f %-14d %-14d %+14.4f" % (K, m, better, worse, m - (sum(base) / len(base))))
print()
print("判读：")
print("  · 若各 K 的 Δcost 均值与原始值（%+.4f）方向一致且量级相近 → 候选池大小不是主因" % (sum(base) / len(base)))
print("  · 若随 K 增大而变化明显（尤其符号翻转） → 候选池大小是主因，全量必须统一候选数")
print()
print("⚠️ 本重算的局限：结果 JSON 未保存逐候选有效性掩码，这里用"
      "\"升序后取最小 n_valid 个\"近似有效候选，会高估质量上界；")
print("   要彻底解决，应在 train_cfc.py 里保存逐候选的 valid 掩码 —— 这是下一步该补的。")
