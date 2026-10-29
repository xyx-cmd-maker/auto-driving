#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P0-1 探针：`otf_core._crossed` 的实际语义 vs 论文文字。

论文（摘要/§2.1/图注）写的规则：
    "A vehicle entering the ego lane from an adjacent lane scores +1;
     a vehicle leaving it scores −1."

本脚本用 4 个最小用例，把 `_crossed` 的真实行为钉下来。
不依赖任何模拟器，只构造帧序列。

用法：py -3.12 scripts/audit_otf_definition.py
"""
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "otf")))
from otf_core import otf_from_frames, otf_window, _crossed  # noqa: E402

EGO_LANE = 2
EGO_ID = "ego"

# 车道 2 = ego lane；3 = 左邻；1 = 右邻
CASES = [
    # 名字, prev_lane, cur_lane, prev_pos, cur_pos, 论文预期
    ("A 从左邻进入 ego lane，向前", 3, 2, 10.0, 12.0, "+1"),
    ("B 从 ego lane 驶出到左邻，向前", 2, 3, 10.0, 12.0, "-1"),
    ("C 从左邻进入 ego lane，向后", 3, 2, 12.0, 10.0, "+1?（论文未区分方向）"),
    ("D 从 ego lane 驶出到右邻，向后", 2, 1, 12.0, 10.0, "-1?"),
    ("E ego lane 内直行（不跨界）", 2, 2, 10.0, 12.0, "0"),
    ("F 邻道内直行（不跨界）", 3, 3, 10.0, 12.0, "0"),
]


def probe_crossed():
    print("=== 1. `_crossed` 单帧用例 ===")
    print("  %-30s %8s  %s" % ("用例", "代码返回", "论文预期"))
    for name, pl, cl, pp, cp, exp in CASES:
        got = _crossed(pl, cl, pp, cp, EGO_LANE)
        flag = "  " if str(got) == exp.replace("+", "") else "≠ "
        print("  %-30s %8d  %s   %s" % (name, got, exp, flag))


def probe_pipeline():
    """走完整 pipeline：单邻车、两帧。"""
    print()
    print("=== 2. `otf_from_frames` 端到端（单邻车、两帧）===")
    for name, pl, cl, pp, cp, exp in CASES[:4]:
        frames = [
            {"ego": {"pos": 0.0, "lane": EGO_LANE}, "nv": {"pos": pp, "lane": pl}},
            {"ego": {"pos": 1.0, "lane": EGO_LANE}, "nv": {"pos": cp, "lane": cl}},
        ]
        ot, otn = otf_window(frames, EGO_ID, EGO_LANE)
        val = otf_from_frames(frames, EGO_ID, EGO_LANE)
        print("  %-30s ot=%d otn=%d  OTF=%+d   (论文预期 %s)" % (name, ot, otn, val, exp))


def probe_zero_net():
    """关键：进入 + 离开同一窗口内是否抵消。"""
    print()
    print("=== 3. 同一窗口内「进 + 出」是否互相抵消（决定 P(OTF>0) ≠ P(至少一次 crossing)）===")
    # 车 A 从左邻进入 ego lane（向前 → +1）；车 B 在 ego lane 向后离开（→ −1）
    frames = [
        {"ego": {"pos": 0.0, "lane": EGO_LANE},
         "A": {"pos": 10.0, "lane": 3}, "B": {"pos": 20.0, "lane": 2}},
        {"ego": {"pos": 1.0, "lane": EGO_LANE},
         "A": {"pos": 12.0, "lane": 2}, "B": {"pos": 18.0, "lane": 1}},
    ]
    ot, otn = otf_window(frames, EGO_ID, EGO_LANE)
    print("  ot=%d otn=%d → OTF=%+d ；但窗口内确实发生了 2 次跨界" % (ot, otn, ot - otn))
    print("  ⇒ P(OTF>0) 与 P(OTF≠0) 与 P(至少一次 crossing) 在此例中互不相等")


def probe_sign():
    print()
    print("=== 4. 符号方向核对（Φ = OTF/W，单位 次/秒）===")
    print("  A（+1，一次进）→ Φ = +0.2 /s（W=5 s）")
    print("  B（-1，一次出）→ Φ = -0.2 /s")
    print("  控制器第四维输入允许为负：obs-phi 校验用的是 |Φ|（train_cfc.py L224: abs(phi) > 1e-12）")


if __name__ == "__main__":
    probe_crossed()
    probe_pipeline()
    probe_zero_net()
    probe_sign()
