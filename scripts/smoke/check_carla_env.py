#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CARLA 环境冒烟（可复跑）。

用法：
    python scripts/smoke/check_carla_env.py                       # 只检查客户端可用性
    python scripts/smoke/check_carla_env.py --exe "F:\\CARLA\\CarlaUE4.exe"   # 顺带启动服务端并连通

退出码：0 = 通过；1 = 有未过项；2 = 环境未就绪（缺依赖/缺可执行文件）

为什么需要它
------------
CARLA 的坑集中在"装了但连不上"：显卡驱动、端口占用、客户端与服务端版本不匹配、
Python 版本不兼容。本脚本把这些逐条变成可复跑的检查，避免"看起来装好了"。
"""
import argparse
import os
import socket
import subprocess
import sys
import time

DEFAULT_EXE_CANDIDATES = [
    r"F:\CARLA\CarlaUE4.exe",
    r"F:\CARLA\WindowsNoEditor\CarlaUE4.exe",
    r"D:\CARLA\CarlaUE4.exe",
    r"C:\CARLA\CarlaUE4.exe",
]
PORT = 2000


def check(results, name, ok, detail):
    results.append((name, ok, detail))


def port_open(host, port, timeout=2.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        return s.connect_ex((host, port)) == 0
    finally:
        s.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=None, help="CarlaUE4.exe 路径；给了就启动并连通")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=PORT)
    ap.add_argument("--wait", type=int, default=60, help="等待服务端就绪的秒数")
    ap.add_argument("--kill-after", action="store_true", help="测完关掉服务端")
    args = ap.parse_args()

    results = []

    # ---- 1. Python 客户端 ----
    carla = None
    try:
        import carla as _carla
        carla = _carla
        check(results, "import-carla", True, "carla %s（%s）" % (getattr(carla, "__version__", "?"),
                                                              os.path.dirname(carla.__file__)))
    except Exception as exc:
        check(results, "import-carla", False,
              "导入失败：%s —— 需按 CARLA 版本安装对应 Python API（0.9.16 通常要 Python ≤3.12；"
              "本机为 %s）" % (type(exc).__name__, sys.version.split()[0]))

    # ---- 2. 服务端可执行文件 ----
    exe = args.exe
    if not exe:
        for c in DEFAULT_EXE_CANDIDATES:
            if os.path.exists(c):
                exe = c
                break
    if exe:
        ok = os.path.exists(exe)
        check(results, "server-exe", ok, ("找到 %s（%.2f GB 目录）" % (exe, dir_size(os.path.dirname(exe)) / 1024 ** 3))
              if ok else "未找到 %s" % exe)
    else:
        check(results, "server-exe", False, "未找到 CarlaUE4.exe；请用 --exe 指定，或确认解压路径")

    # ---- 3. 端口是否已被占用（老进程残留）----
    occupied = port_open(args.host, args.port)
    check(results, "port-free-before", not occupied,
          "端口 %d %s" % (args.port, "已在监听（可能已有服务端在跑）" if occupied else "空闲"))

    proc = None
    if exe and os.path.exists(exe) and not occupied:
        try:
            # -quality-level=Low 降低渲染负担；-windowed 便于观察；-carla-port 指定端口
            proc = subprocess.Popen([exe, "-quality-level=Low", "-windowed",
                                     "-carla-port=%d" % args.port],
                                    cwd=os.path.dirname(exe),
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            check(results, "server-start", True, "已启动 PID=%d，等待端口就绪…" % proc.pid)
        except Exception as exc:
            check(results, "server-start", False, "启动失败：%s" % exc)

    if proc is not None:
        ready = False
        t0 = time.time()
        while time.time() - t0 < args.wait:
            if port_open(args.host, args.port, 1.0):
                ready = True
                break
            if proc.poll() is not None:
                break
            time.sleep(2)
        check(results, "port-ready", ready,
              "端口 %d 在 %.0f s 内%s就绪" % (args.port, time.time() - t0, "" if ready else "**未**"))

        if ready and carla is not None:
            try:
                client = carla.Client(args.host, args.port)
                client.set_timeout(20.0)
                world = client.get_world()
                m = world.get_map()
                check(results, "client-connect", True,
                      "已连接；地图=%s；仿真时间=%.1f s" % (m.name, world.get_snapshot().timestamp.elapsed_seconds))
                # 列出可用地图（Town04 是 P1 的目标地图）
                try:
                    maps = [x.split("/")[-1] for x in client.get_available_maps()]
                    has04 = any("Town04" in x for x in maps)
                    check(results, "town04-present", has04,
                          "可用地图 %d 张；Town04 %s" % (len(maps), "在" if has04 else "**不在**（P1 需要 Town04）"))
                except Exception as exc:
                    check(results, "town04-present", False, "枚举地图失败：%s" % exc)
                # GPU 侧：CARLA 服务端会用 GPU 渲染，这里只确认能取到世界（渲染成功）
            except Exception as exc:
                check(results, "client-connect", False, "连接后操作失败：%s" % exc)
        elif ready:
            check(results, "client-connect", False, "端口就绪但 Python 客户端不可用（见 import-carla）")

        if args.kill_after and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=15)
            except Exception:
                proc.kill()
            check(results, "server-stop", True, "已关闭服务端")

    failed = [n for n, ok, _ in results if not ok]
    print("CARLA 环境冒烟")
    print("")
    for name, ok, detail in results:
        print("  %s %-18s %s" % ("OK  " if ok else "FAIL", name, detail))
    print("")
    print("[carla-env] %s：%d/%d" % ("全部通过" if not failed else "有未过项 " + ", ".join(failed),
                                    len(results) - len(failed), len(results)))
    if failed:
        return 2 if any(x in failed for x in ("import-carla", "server-exe")) else 1
    return 0


def dir_size(path):
    total = 0
    try:
        for r, _, fs in os.walk(path):
            for x in fs:
                try:
                    total += os.path.getsize(os.path.join(r, x))
                except Exception:
                    pass
            if total > 200 * 1024 ** 3:
                break
    except Exception:
        pass
    return total


if __name__ == "__main__":
    sys.exit(main())
