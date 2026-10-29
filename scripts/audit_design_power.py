#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""设计功效的**硬下界**：n 个配对该取多少，才"有可能"得到显著结果？

为什么用"最小可达 p"而不是常规功效分析：
    精确符号翻转检验（两侧）在 n 对配对差下的最小值是 **2 / 2^n**（全部同号时取到）。
    这与数据无关，是**组合学硬下界**。若该下界 > 校正后的 α，则无论效应多大都不可能显著。

本脚本给出：
  - n = 4..12 的最小可达 p；
  - 与 Holm 校正（k = 1、2、4 个检验）比较；
  - 因此每个设计所需的最小 n；
  - 对 Route A（2 格 × n 种子）与完整四场景设计的结论。

用法：py -3.12 scripts/audit_design_power.py
"""
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ALPHA = 0.05


def min_p(n):
    return 2.0 / (2 ** n)


def min_n_for(k_tests, alpha=ALPHA):
    """Holm 家族里最小的阈值是 α/k；返回满足 min_p(n) <= α/k 的最小 n。"""
    thr = alpha / k_tests
    for n in range(2, 40):
        if min_p(n) <= thr:
            return n, thr
    return None, thr


def main() -> int:
    print("  精确符号翻转检验的最小可达双侧 p（组合学下界，与数据无关）")
    print("  %3s %12s %12s %12s %12s" % ("n", "min p", "vs α=0.05", "vs α/2=0.025", "vs α/4=0.0125"))
    for n in range(4, 13):
        p = min_p(n)
        print("  %3d %12.2e %12s %12s %12s" % (
            n, p,
            "OK" if p <= 0.05 else "不可能",
            "OK" if p <= 0.025 else "不可能",
            "OK" if p <= 0.0125 else "不可能"))

    print()
    for k, label in ((1, "单个比较"), (2, "2 个比较（Route A 省钱版）"), (4, "4 场景（主实验族）")):
        n, thr = min_n_for(k)
        print("  %-26s 最小可用 n = %s（Holm 阈值 α/%d = %.4f）" % (label, n, k, thr))

    print()
    nA, thrA = min_n_for(2)
    print("  ⇒ Route A（2 格）至少要 每格 n = %d，即 %d 局；" % (nA, 2 * nA))
    print("     若只做 5 种子/格（Round 09 的省钱版 10 局），最小可达 p = %.4f > %.4f，"
          % (min_p(5), thrA))
    print("     **在数学上不可能显著**，只能得到置信区间，不能得到正面结论。")
    print()
    n4, thr4 = min_n_for(4)
    print("  ⇒ 完整四场景若要能主张『有意义差异』，每场景至少 n = %d，共 %d 局。" % (n4, 4 * n4))
    return 0


if __name__ == "__main__":
    sys.exit(main())
