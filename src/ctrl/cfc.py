#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CfC 单元（Closed-form Continuous-time）——P1 控制器的最小可用实现。

为什么是这个形状
----------------
蓝图 4.3 要求 P1 用 CfC 做 100 Hz 连续控制。CfC 的卖点是"**不用 ODE 求解器**也能得到
连续时间动力学的闭式解"（Hasani et al., Nature Machine Intelligence 4(11):992-1003, 2022，
DOI 10.1038/s42256-022-00556-7）。本实现只做那一件事，不做别的：

    h(t+dt) = (f(x,h) ⊙ g) · dt + h · (1 - f(x,h) ⊙ g)

其中 f 是有界非线性（sigmoid/tanh），g 是时间常数门（sigmoid 输出 [0,1]）——这个式子就是
原论文的闭式表达，**不含任何 ODE 求解器**。

本文件**刻意不做**的事（等有需要再加，不预先搭架子）：
  - 不做完整 NCP 接线（那需要把感知—中间—命令神经元分开），做多神经元架构时再加
  - 不做多头输出、不做归一化层（不属于 CfC 单元本身）
  - 不做 OTF 势场输入（Φ_OTF）——它属于控制器的输入特征，不属于单元

术语纪律（AGENTS.md §1）：本实现是**结构先验 / 边界条件注入**，**不称 physics-informed**。

用法：
    from cfc import CfCCell, count_params
    cell = CfCCell(input_dim=4, hidden_dim=32)
    h = cell(rnn_input, hx, dt)       # rnn_input: (B, D)
"""
from __future__ import annotations

import torch
import torch.nn as nn


class CfCCell(nn.Module):
    """单个 CfC 单元：把连续时间动力学写成闭式，一步更新隐状态。

    参数
    ----
    input_dim  : 输入特征维度 D（P1 里含 lead_gap / rel_speed / ego_speed /（可选）Φ_OTF）
    hidden_dim : 隐状态维度 H
    mode       : 'default' 用 sigmoid 作 f（原论文主用配置）；
                 'pure' 用 tanh（原论文的 "pure" 变体，无门控混合）
    backbone   : 'linear'（最小实现）或 'mlp'（两层，增强表达力；P1 需要时可切）
    """

    def __init__(self, input_dim: int, hidden_dim: int, mode: str = "default",
                 backbone: str = "linear"):
        super().__init__()
        if mode not in ("default", "pure"):
            raise ValueError("mode 必须是 'default' 或 'pure'，收到 %r" % mode)
        if backbone not in ("linear", "mlp"):
            raise ValueError("backbone 必须是 'linear' 或 'mlp'，收到 %r" % backbone)
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.mode = mode

        # 融合输入与隐状态 → 隐层（这一步是"f"与"g"共用的特征提取）
        if backbone == "linear":
            self.fc = nn.Linear(input_dim + hidden_dim, hidden_dim)
        else:
            self.fc = nn.Sequential(
                nn.Linear(input_dim + hidden_dim, 2 * hidden_dim),
                nn.ReLU(),
                nn.Linear(2 * hidden_dim, hidden_dim),
            )
        self.f = nn.Sigmoid() if mode == "default" else nn.Tanh()
        self.g = nn.Sigmoid()          # 时间常数门，值域 [0,1]
        # 注意：这里**不**预先创建 'pure' 专用层。早期版本建了一个 ff1 却只在 pure 模式用，
        # 结果 default 模式下它是**死参数**（永远拿不到梯度）——自检抓到了这一点。
        # 现在按模式条件创建：default 模式不引入任何未使用的参数。

        # 初始化：与原论文一致的保守初始化（小权重 + 零偏置，避免开局饱和）
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.uniform_(m.weight, -0.1, 0.1)
                nn.init.zeros_(m.bias)

    def forward(self, input: torch.Tensor, hx: torch.Tensor, dt: float | torch.Tensor) -> torch.Tensor:
        """一步更新。

        input : (B, D) 当前输入
        hx    : (B, H) 上一时刻隐状态
        dt    : 步长（标量或 (B,1)/(B,) 张量），单位与训练时一致

        返回 : (B, H) 新隐状态
        """
        if input.dim() != 2 or hx.dim() != 2:
            raise ValueError("input/hx 必须是二维 (B,·)，收到 %s / %s"
                             % (tuple(input.shape), tuple(hx.shape)))
        if input.shape[1] != self.input_dim:
            raise ValueError("input 维度应为 %d，收到 %d" % (self.input_dim, input.shape[1]))
        if hx.shape[1] != self.hidden_dim:
            raise ValueError("hx 维度应为 %d，收到 %d" % (self.hidden_dim, hx.shape[1]))

        z = torch.cat([input, hx], dim=1)
        feat = self.fc(z)

        if self.mode == "pure":
            # 无门控：h' = tanh(feat)·dt + h·(1−dt)  —— 原论文的 pure 变体
            return self.f(feat) * dt + hx * (1.0 - dt)

        f_val = self.f(feat)          # 有界非线性 ∈ [0,1]（sigmoid）
        g_val = self.g(feat)          # 时间常数门 ∈ [0,1]
        # 闭式一步：h(t+dt) = f·g·dt + h·(1 − f·g)
        return f_val * g_val * dt + hx * (1.0 - f_val * g_val)


def count_params(module: nn.Module) -> int:
    """可训练参数量（与量化精度无关的"参数个数"）。"""
    return sum(p.numel() for p in module.parameters() if p.requires_grad)


def param_report(input_dim: int, hidden_dim: int, backbone: str = "linear") -> dict:
    """把一个 CfC 单元的参数量拆开报——防止把"递归分量"当成"全模型"来宣传。

    背景（AGENTS.md §1 参数量口径）：CfC 原论文只给了一组参数量，且**递归分量 4,184 /
    含感知头全模型 230,828** 是两个数。本项目必须同样区分，不得混用。
    """
    cell = CfCCell(input_dim, hidden_dim, backbone=backbone)
    total = count_params(cell)
    return {
        "input_dim": input_dim,
        "hidden_dim": hidden_dim,
        "backbone": backbone,
        "rnn_params": total,                       # 递归（控制）分量
        "fp32_kib": total * 4 / 1024,
        "fp16_kib": total * 2 / 1024,
        "int8_kib": total * 1 / 1024,
    }
