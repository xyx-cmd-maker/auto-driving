#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补充实验启动器：高密度组 + 长窗口组（各 5 局，顺序执行）。

设计依据（来自 SUMO 相图，audit/第一次组会/13 §11）
----------------------------------------------------
主实验（16 辆 / 窗口 5 s）的 Φ_OTF>0 只有 0.084–0.167，处在**低信息区**。
相图显示：把密度从 ~1600 提到 ~3200 veh/h 等效，或把窗口从 5 s 提到 20 s，
非零比例可升到 0.5–0.9。因此跑两组补充：

  A 高密度：traffic=32, otf_window=5      （密度×2，窗口不变）
  B 长窗口：traffic=16, otf_window=20     （窗口×4，密度不变）

两组都只跑 `lead-brake`（主实验里 Δcost 最正、最可能掩盖真实效应的场景）× seeds 0–4。

**为什么必须每次杀 CARLA**：`--ensure-carla` 只在 CARLA 未运行时启动它；
若第二个子进程启动时 CARLA 已在跑，torch 会在 CARLA 占满 7 GB 后导入，
再次触发 `OSError: [WinError 1455] 页面文件太小`（2026-10-18 实测）。
所以每个配置开始前 `taskkill` 掉 CARLA，让"torch 先加载、CARLA 后启动"的顺序成立。

产物：分别写 `runs/p1_supp_A_highdensity/` 与 `runs/p1_supp_B_longwindow/`
（用 `P1_RUNS_DIR` 隔离，**绝不覆盖主实验的 20 局结果**）。

用法：
  py -3.12 scripts/run_supplementary.py
"""
import os
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
TRAIN = os.path.join(ROOT, "src", "ctrl", "train_cfc.py")

CONFIGS = [
    {
        "name": "A_highdensity",
        "runs_dir": os.path.join(ROOT, "runs", "p1_supp_A_highdensity"),
        "args": ["--traffic", "32", "--otf-window", "5"],
        "why": "密度×2（≈3200 veh/h 等效），验证相图预测的 Φ 上升",
    },
    {
        "name": "B_longwindow",
        "runs_dir": os.path.join(ROOT, "runs", "p1_supp_B_longwindow"),
        "args": ["--traffic", "16", "--otf-window", "20"],
        "why": "窗口×4，低密度下靠加长窗口进入高信息区",
    },
]

COMMON = ["--scenarios", "lead-brake", "--seeds", "0,1,2,3,4",
          "--episode-s", "60", "--resume", "--ensure-carla"]


def kill_carla() -> None:
    for exe in ("CarlaUE4-Win64-Shipping.exe", "CarlaUE4.exe"):
        subprocess.run(["taskkill", "/F", "/IM", exe],
                       capture_output=True, text=True)
    time.sleep(6)


def main() -> int:
    if not os.path.exists(TRAIN):
        print("  ✗ 找不到训练脚本: %s" % TRAIN)
        return 2
    t_all = time.time()
    results = []
    for cfg in CONFIGS:
        print("\n=== %s：%s" % (cfg["name"], cfg["why"]))
        print("    参数: %s" % " ".join(cfg["args"]))
        os.makedirs(cfg["runs_dir"], exist_ok=True)
        kill_carla()
        env = os.environ.copy()
        env["P1_RUNS_DIR"] = cfg["runs_dir"]
        env["OPENBLAS_NUM_THREADS"] = "1"
        env["OMP_NUM_THREADS"] = "1"
        t0 = time.time()
        r = subprocess.run([sys.executable, TRAIN] + COMMON + cfg["args"],
                           cwd=ROOT, env=env, capture_output=True, text=True)
        dt = time.time() - t0
        tail = [ln for ln in (r.stdout or "").splitlines() if ln.strip()][-8:]
        print("    exit=%d ｜ %.0f s" % (r.returncode, dt))
        for ln in tail:
            print("    " + ln[:150])
        if r.returncode != 0 and r.stderr:
            print("    stderr 末 5 行:")
            for ln in (r.stderr or "").splitlines()[-5:]:
                print("      " + ln[:150])
        results.append((cfg["name"], r.returncode, dt, cfg["runs_dir"]))

    print("\n=== 汇总（总耗时 %.0f min）" % ((time.time() - t_all) / 60.0))
    for name, rc, dt, d in results:
        import glob
        n = len(glob.glob(os.path.join(d, "cases", "case_*.json")))
        print("  %-16s exit=%-3d %5.0f s ｜ 完成 %d/5 局 ｜ %s" % (name, rc, dt, n, d))
    print("\n  下一步：对每个目录分别跑 --analyze（把 P1_RUNS_DIR 指向该目录）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
