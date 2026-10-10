# 系统辨识的深度网络综述 [材料为讲稿，非全文]｜Deep networks for system identification: a survey

> ## ⚠️ 材料性质声明（置于卡片顶部，务必先读）
>
> **本卡不是基于论文全文写的。** `literature/fulltext/meeting2/` 内这一份 .txt 经核实是 **ERNSI Workshop 2023（斯德哥尔摩，2023-09-26）的讲稿幻灯片**：`PAGES=27`（幻灯片页码，页脚编号 1/22 至 22/22）、`CHARS=9,915`，首页逐字为 "*Deep networks for system identication: a survey … ERNSI Workshop 2023 / Stockholm, September 26, 2023 / arXiv link:*"。
>
> **本卡内容 = (a) 该讲稿幻灯片的目录与要点 + (b) 在线核验取得的正式发表信息与 arXiv 摘要。**
> **本组未读该综述的论文全文**（正文、图表、参考文献、定理与实验全部未见）。
>
> **因此：D5（材料完整度）只能给 0–1 分，本卡给 D5 = 1。** 本卡**不包含、也不得推演**该综述的任何图号、表号、定理编号、数据集规模或实验数字——凡幻灯片未印出的内容，一律标 `未见于讲稿` 或 `[待核实]`。
>
> **核验时间**：2026-10-03（web_search + web_fetch，通道与结果见 §2、§8）。

- **出处**：讲稿首页未印 venue 卷期页；**正式发表的对应论文**为 *Automatica*, vol. 171, 2025, article 111907（见 §2 在线核验）｜ **类型**：**讲稿（slides）** —— 对应论文为综述（survey）
- **作者**：Gianluigi Pillonetto et al.（讲稿首页逐字：Pillonetto G [University of Padova, Italy]、Aravkin A [University of Washington, USA]、Gedon D [Uppsala University, Sweden]、Ljung L、Ribeiro AH [Linköping University, Sweden]、Schön TB；联系页逐字 "*Daniel Gedon, Uppsala University, E-mail: daniel.gedon@it.uu.se, Web: dgedon.github.io, Twitter: @danigedon*"）
- **DOI**：**讲稿内未见**。对应论文 DOI = **10.1016/j.automatica.2024.111907**（Crossref `works?query.bibliographic=…` 核验 2026-10-03 命中，`container-title: Automatica`, `volume: 171`, `page: 111907`, `issued: 2025-01`）；arXiv 版 DOI = 10.48550/arXiv.2301.12832（`export.arxiv.org/abs/2301.12832` 核验，v1 提交于 2023-01-30）
- **全文来源**：`literature/fulltext/meeting2/deep-networks-for-system-identification-a-survey__ae332610.txt`（PAGES=27, CHARS=9,915）
- **分组**：连续时间 / 流体神经网络
- **证据等级初判**：**D 级（就本卡材料而言）** — 材料是讲稿幻灯片，**无摘要、无方法细节、无实验协议、无参考文献表**，幻灯片中的数字（29.71% / 99.31% / 参数量 184,200 等）**只出现在截图图注式文本中，缺少数据集划分、训练协议与不确定度**。**【确定】**
- **档位建议**：**B 略读（且限定为"背景与术语来源"）** — 其价值限于：① 提供系统辨识 vs 深度学习的**术语框架**（NARX / FIR / NFIR / stable spline / manifold GP / NTK / double descent / implicit regularization），② 提供**参数量 vs 训练样本量**的量级参照（AlexNet 62.3 M 参数 vs 1.2 M 数据点等）。**不建议按 A 档精读，也不得据本卡做任何定量引用。**【确定】
- **五维打分**：D1=1 D2=1 D3=2 D4=1 **D5=1** → 加权 = 3·1+2·1+2·2+1·1+2·1 = 3+2+4+1+2 = **12**

> 打分口径（本组统一）：D1 与 P1 工程命题的直接相关度；D2 实验设计与报告质量；D3 可迁移性；D4 与 P1 七项指标的可对齐度；**D5 材料完整度（讲稿类材料上限 1）**。权重 3/2/2/1/2。

## 1. 标题
Deep networks for system identi铿乧ation: a survey｜系统辨识中的深度网络：一篇综述
（讲稿首页标题逐字为小写 "a survey"；在线核验的正式版标题为 "Deep networks for system identification: **A** survey"，大小写不同，引用须以正式版为准。）

## 2. 摘要（≤400 字中文）
> **说明**：讲稿**没有摘要**。以下摘要为**在线核验取得的 arXiv:2301.12832 摘要**（`export.arxiv.org/abs/2301.12832`，2026-10-03 取用）的**中文转述**，**不是** Automatica 正式版的摘要（Elsevier 的 Crossref 记录**不含摘要**，正文需订阅）。**不得把本段当作"已读综述"的证据。**

作者从**系统辨识的视角**综述深度学习：**系统辨识**研究如何从输入-输出数据学习动力系统的数学描述，因此可受益于深度神经网络以**扩大可选模型的范围**。综述覆盖：① 文献中常用的**前馈、卷积、递归网络**架构，以及**其参数必须由过去数据估计以优化预测性能**；② 一组在实践中被证明高效的**一阶优化工具**；③ 与**核方法**这一成熟领域的联系——核方法通过正则项惩罚不符合先验假设的模型来控制数据拟合，作者展示如何把核方法嵌入深度架构得到**深度核方法**；④ 深度学习带来的**反直觉经验现象**：**过参数化模型**的作用、其与核的联系、影响泛化的**隐式正则化**机制，特别包括 **benign overfitting（良性过拟合）** 等有趣现象。作者称综述"提供严格的实践与理论洞见，以理解这些方法的收益与挑战"。**（本卡未读全文，无法给出该综述的结论、图表或实验清单。）**

## 3. 结论（≤350 字中文）
> **说明**：**本卡没有该综述的结论节**（未读全文）。以下仅为**讲稿末页"Conclusion"幻灯片的逐字内容**（PAGE 26，页脚 21/22），不代表论文结论。

讲稿结论页逐字要点：**使用神经网络的两件要事** —— ① "many parameters → **overparameterization**"；② "many layers → **deep architectures**"。**Open problems（开放问题）**：*Successful architectures: Attention models and transformers; Flow-based models; Generative adversarial models (GANs) and diffusion models; Graph neural networks;* 以及 *Robustness issues; Theoretical development; . . .*。
末页（PAGE 27，页脚 22/22）为**联系方式页**，无内容。

**作者自承的局限（就讲稿而言）**：讲稿把理论部分（PAGE 17–22）建立在两个支柱上——① 过参数化与泛化的相互作用（"double descent"：interpolate and generalize）；② 非凸优化问题的简化（宽网络 + 小步更新 → 在 θ₀ 附近线性化 → **神经正切核 NTK** → 凸优化问题）——但**未在讲稿中给出任何定理编号、证明或适用条件**。属 **D 级（假设/概述）**，不可引用为"该综述证明了…"。

## 4. 方法一句话
讲稿无方法章；其**叙述链**为：系统辨识/深度学习流程对照 → DNN 架构族 → 一阶优化与学习率调度 → 深度核方法（manifold GP）→ 理论（过参数化/NTK）→ 两个工程基准。

## 5. 图表清单（占位符）
> **重要**：讲稿的图**全部是幻灯片插图，没有图号、没有图注**（PDF 文本层只提取到图中的坐标轴标签与图例文字）。**下表按"幻灯片页"给占位符，并逐页记录屏幕上可见的图元与文字**；"原文图注"一律为 **未见图注**（幻灯片无图注体例）。**本表覆盖讲稿全部 27 页**（其中 6 页为纯文字/目录/联系页，同样列出）。

| 占位符 | 位置 | 页面逐字标题 / 可见图元 | 读图要点 |
|---|---|---|---|
| {SLD-SYSID-01} | PAGE 1（页脚 1/22） | 标题页：*Deep networks for system identi铿乧ation: a survey*；作者与四国单位；*ERNSI Workshop 2023 / Stockholm, September 26, 2023*；*arXiv link:*（**链接文字后为空，未印 URL**） | **材料性质的决定性证据**：这是 workshop 讲稿，不是论文。 |
| {SLD-SYSID-02} | PAGE 2 | *Introduction — System identi铿乧ation with long history*；页脚 1/22 | 仅一句引言。 |
| {SLD-SYSID-03} | PAGE 3 | *Introduction — Deep neural networks with recent success*；箭头句 *Innovate system identi铿乧ation with power of deep neural networks*；页脚 2/22 | 讲稿的动机句。 |
| {SLD-SYSID-04} | PAGE 4 | **目录（Contents）**：*1. Modeling of dynamical systems｜2. Deep neural network architectures｜3. Optimization｜4. Deep kernel-based learning｜5. Theoretical development｜6. Applications｜7. Conclusion*；页脚 2/22 | **这就是本卡能提供的"综述骨架"**：七章结构。⚠ 只此一处给出章节名；论文各章的实际内容本卡一概未见。 |
| {SLD-SYSID-05} | PAGE 5 | *Modeling of dynamical systems — Three main players*：① 参数化模型族 Z={x(t),y(t)}^#train，g_θ: Z(t) ↦ ŷ(t+1), θ∈Θ；② 参数估计 θ̂ = argmin_θ L_N(θ, Z^e)；③ 验证（残差分析、交叉验证）。页脚 3/22；含 *#features = dim θ* 与 *L_emp = L(θ̂, Z^e)*、*over铿乼ting L_emp = 0 typically for #features = #train* | **可直接引用的术语骨架**：辨识 = 模型族 + 估计 + 验证三要素；并给出 **#features = #train 时 L_emp 通常为 0**（过拟合的经典判据）。 |
| {SLD-SYSID-06} | PAGE 6 | *Modeling of dynamical systems — Modeling procedure: System identication vs deep learning*；双流程对照图，可变更节点为 **Data / Parameter Estimation(Training) / Validation(ok?) / Model Structure(Hyperparameter) / Model Family(Architecture) / Experiment Design**（yes/no + change 分支）。页脚 4/22 | **本讲稿对 P1 最有价值的一页之一**：把经典辨识与深度学习流程**逐节点对齐**（模型族↔架构、模型结构↔超参、实验设计↔数据采集）。P1 的"同等调参预算/同等可用信息"公平性条款可用此框架陈述。 |
| {SLD-SYSID-07} | PAGE 7 | 目录页（同 PAGE 4），页脚 4/22 | 重复页。 |
| {SLD-SYSID-08} | PAGE 8 | *DNN architectures*：*Fully-connected networks｜Skip and direct connections｜Convolutional networks｜Recurrent neural networks｜Latent variable models (Autoencoder, Variational autoencoder, Deep state-space models)｜Energy-based models*。页脚 5/22 | **架构族清单（逐字可引）**。⚠ **本清单中没有 ODE-based / continuous-time / liquid 网络** —— 该综述的架构覆盖面与 P1 的 LNN 路线**不重合**（本卡基于讲稿，未见全文，`[待核实]`）。 |
| {SLD-SYSID-09} | PAGE 9 | *Convolutional networks*：卷积层 w(t)∗x(t) = Σ w(j)x(t−j)；多个滤波器 W={w₁…w_b}，第 i 个输出 xᵢ(t)=wᵢ(t)∗x(t)。页脚 6/22 | 卷积定义；与 P1 无关。 |
| {SLD-SYSID-10} | PAGE 10 | *Formulating regression problems*：求预测分布 p(y(t)|x(t))；例：**NARX** 模型 y(t)=f_θ(x(t))+e(t), e(t)~N(0,σ²)；隐含假设 p 为高斯 ⇒ NN 建模均值；**Energy-based models** p_θ(y(t)|x(t)) = e^{g_θ(y(t),x(t))}/Z_θ(x(t))，Z_θ(x(t))=∫e^{g_θ(z,x(t))}dz；把 NN 映射 g_θ:(y(t),x(t))↦R；泛化高斯假设 ⇒ 可表达**非对称、厚尾、多峰**分布。页脚 7/22 | **NARX 是 P1 基线 MPC 与参数量口径的可引术语**；EBM 部分与 P1 无关。 |
| {SLD-SYSID-11} | PAGE 11 | *Optimization*：辨识 min_θ ΣL(y(t), f_θ(z(t)))；深度学习 min_{θ₁…θ_L} ΣL(y(t), f^L_{θ_L}∘…∘f¹_{θ₁}(z(t)))；牛顿法复杂度 **O(#train·#param² + #param³)** ⇒ 一阶方法；大 dim(θ) + 嵌套结构 ⇒ 逐层梯度 + 链式法则 ⇒ **反向传播**；大数据集 ⇒ 随机方法。页脚 8/22 | **牛顿法复杂度式逐字可引**（P1 若要论证"为什么基线不用二阶法"可引此式）。 |
| {SLD-SYSID-12} | PAGE 12 | *Optimization — Gradient decent optimization*：θ_{i+1}=θ_i−α∇V(θ_i)；**固定 α 的 SGD 不收敛** ⇒ 学习率调度器 ⇒ 把 α 降到 0；插图三种调度：**Step / Cosine annealing / Cyclic**（横轴 steps 0–30，纵轴 learning rate α 0–1）。页脚 9/22 | 学习率调度三型的对照图；**P1 若做"同等调参预算"，调度器选择须写入协议**（本文未给具体参数）。 |
| {SLD-SYSID-13} | PAGE 13 | 目录页，页脚 9/22 | 重复页。 |
| {SLD-SYSID-14} | PAGE 14 | *Deep kernel-based learning — Kernels for modeling dynamical systems*：线性核 K(xᵢ,xⱼ)=xᵢᵀPxⱼ（P 半正定）⇒ 线性函数 f(x)=θᵀx ⇒ **FIR 模型**；线性核 P_ij=λ^{max(i,j)}, 0≤λ<1 ⇒ **stable spline/TC 核**；高斯核 K(xᵢ,xⱼ)=exp(−‖xᵢ−xⱼ‖²/ρ) ⇒ **NFIR 模型**；*Choice of kernel → encode high level assumptions*。页脚 10/22 | **"核 = 高层先验假设的编码"这一句话对 P1 的"OTF 作为 inductive bias"表述有直接支撑价值**（与本项目 `AGENTS.md` §1 术语口径一致）。 |
| {SLD-SYSID-15} | PAGE 15 | *Deep kernel-based learning — Example: f = sin(e^{x/2}) → complicated frequency content*：高斯核导致 **RKHS 范数大 ⇒ 有偏估计**；思路：变换数据 f = f̃∘G，G=e^{x/2} ⇒ 选 G=e^{x/2} 后 f̃=sin(x) 为单一频率；插图：函数 f（左）与 **RKHS 平方范数 vs 输入空间（原空间 / 被 G(x)=exp(x) 变换后的空间）**（右，横轴 10²–10⁵）。页脚 11/22 | **"输入空间变换可显著降低 RKHS 范数"的图示**是 P1 把 OTF 势场当作**输入空间变换/条件化**（而非损失项）的类比锚点。⚠ **图中无任何数值标注**。 |
| {SLD-SYSID-16} | PAGE 16 | *Deep kernel-based learning*：考虑 f = f̃∘G，插入 **Neural Network** 学 G ⇒ **manifold Gaussian process**，K(xᵢ,xⱼ) := K̃(x̃ᵢ,x̃ⱼ) = K̃(G(xᵢ),G(xⱼ))；此前高斯核只有 1 个尺度参数 ρ，现在 manifold 高斯核有**多参数 η=[ρ,θ]** ⇒ 用联合密度 p(Y,f|η) 的**边际似然**优化。页脚 12/22 | **manifold GP = "用神经网络学输入空间变换 + 核方法"的组合**，与 DeepONet 的 branch/trunk 分解同属"架构注入先验"家族；P1 的 OTF 条件化可归入这一族。 |
| {SLD-SYSID-17} | PAGE 17 | *Theoretical development — Why are deep models so successful?* 三条量级：① **2-layer ConvNet on MNIST: 1.2m parameters vs 60k data points**；② **AlexNet on ImageNet: 62.3m parameters vs 1.2m data points**；③ *…*；配 **Model complexity vs Error 的 Train/Test 曲线图**；文字 *Theoretical development: 1. interplay of overparameterization and generalization; 2. simpli铿乧ation of non-convex optimization problem*；旁注 **"Double descent" → interpolate and generalize**。页脚 13/22 | **★ P1 可直接引用的两个量级数字**（见 §8）。**"double descent / interpolate and generalize"** 是 P1 论证"小模型 vs 大模型"时的必要背景术语。 |
| {SLD-SYSID-18} | PAGE 18 | *Theoretical development — System identication example*：**NARX 模型** ŷ(t)=Σ_{i=1}^{#features} θᵢφᵢ(x(t))；数据来自 y(t)=f(x(t))+v(t)；**#train = 100 samples**；**1-step ahead prediction**；三张插图：MSE（train/test）vs **参数范数**（10⁻¹–10²，纵轴 10⁰–10⁵）、**log₁₀(参数范数)** 分布（−2.0…2.0）。页脚 14/22 | **在系统辨识自己的例子上重演 double descent**（仅 100 个训练样本）。→ P1 若观察到"模型越大测试误差先降后升"，此页是**同类现象在辨识领域的先例**。⚠ 无任何数值标注。 |
| {SLD-SYSID-19} | PAGE 19 | *Theoretical development*：非线性变换 φ(x) 把输入映到特征空间 φ: R^{#inputs} ↦ R^{#features}；线性模型 ŷ=θ̂ᵀφ(x)；估计 min_θ Σ(yᵢ−θᵀφ(xᵢ))²；优化：从 **0** 出发的梯度下降 θ_{i+1}=θ_i−α∇V(θ_i)。页脚 15/22 | 特征空间与"从零初始化"的设定（是下一页隐式正则结论的前提）。 |
| {SLD-SYSID-20} | PAGE 20 | *Theoretical development — Solutions of a linear system Xθ = y*，三种情形：**#features < #train ⇒ 无解**；**#features = #train ⇒ 唯一解**；**#features > #train ⇒ 多解**；梯度下降 min‖θ‖₂ s.t. Xθ=y **收敛到最小范数解 ⇒ 梯度下降的隐式正则化**。页脚 16/22 | **"过参数化 + 梯度下降 = 隐式正则化到最小范数解"** —— P1 若做参数量消融，这是解释"参数多不一定差"的标准论据。 |
| {SLD-SYSID-21} | PAGE 21 | *Theoretical development — Implicit Regularization*：梯度下降步 θ_{i+1}=θ_i−α∇V(θ_i) **不遵循连续梯度流**；更接近 θ̇=−∇Ṽ(θ)，修正代价 **Ṽ(θ)=V(θ)+λR(θ)**，其中 **λ = α·#features/4**，**R(θ) = (1/#features)·Σ_{j=1}^{#features}(∂_j V(θ))²** ⇒ 梯度下降**惩罚代价 V(θ) 大的方向 j**。页脚 17/22 | **★ 定量关系 λ = α·#features/4 逐字可引**：把学习率、参数量与隐式正则强度联系起来——P1 做"参数量 vs 性能"消融时，**必须承认学习率与参数量会通过隐式正则耦合**，否则"A2 消融一次只改一个因素"在这一维度上并不干净。 |
| {SLD-SYSID-22} | PAGE 22 | *Theoretical development — 2. Simplication of non-convex optimization problem*：设定 = **宽网络、dim(θ) 大**；每次更新只小幅改变 θ ⇒ 在 θ₀ 附近线性化 f_θ(x) ≈ f_{θ₀}(x) + ∇_θ f_{θ₀}(x)ᵀ(θ−θ₀) ⇒ **神经正切核 NTK** K(x,z;θ₀)=∇_θ f_{θ₀}(x)ᵀ∇_θ f_{θ₀}(z) ⇒ **凸优化问题**；插图：true / observed / NN / NTK samples / NTK intervals。页脚 18/22 | NTK 把宽网络训练**化为凸问题**；P1 若引用"LNN 训练可解性"背景，可引此页的定性链，但**讲稿未给定理**。 |
| {SLD-SYSID-23} | PAGE 23 | 目录页，页脚 18/22 | 重复页。 |
| {SLD-SYSID-24} | PAGE 24 | *Applications — Matlab example: forced duffling oscillator (**silverbox benchmark**)*：**Linear Box-Jenkins type model ⇒ Fit is 29.7%**；另一曲线 **mN2: 99.31%**；**Cascaded feedforward network ⇒ Fit is 99.2%**；两张 *Simulated Response Comparison*（横轴 Time 200–1200 s，纵轴 Amplitude −0.3…0.3），标注 *y1 / vdata (y1) / Simulation error*。页脚 19/22 | **★ 讲稿中仅有的两个工程数字来源之一**（29.71% / 99.31%）。⚠ **"Fit" 的定义、训练/验证划分、重复次数、不确定度均未给出**；且幻灯片上同时出现 "Fit is 99.2%" 与截图内的 "mN2: 99.31%" 两个数值。 |
| {SLD-SYSID-25} | PAGE 25 | *Applications — Pytorch example: **Coupled electronic drives benchmark***：Baseline = **linear ARX model**；Feedforward model；LSTM；**Deep state-space model**；*Good 铿乼 of deep models despite **#train = 300***；**dim(θ_FF) = 184, 200**；**dim(θ_LSTM) = 169, 801**；**dim(θ_DSSM) = 111, 902**；插图：True / FC / Deep SSM 的预测（t 0–4）与 **Fit** 条形图（Linear / FC / LSTM / Deep SSM，纵轴 82.5–92.5）。页脚 20/22 | **★ 讲稿中另一处工程数字来源，且是唯一的参数量数据**（三个模型的 dim(θ)）。注意数字中的空格疑为 OCR/排版产物（"184, 200" 应为 184,200）。⚠ **无数据集规模、无划分、无重复次数**（只有 #train = 300）。 |
| {SLD-SYSID-26} | PAGE 26 | *Conclusion*：见本卡 §3 逐字转录。页脚 21/22 | 讲稿结论。 |
| {SLD-SYSID-27} | PAGE 27 | *Contact — Thank you! / Daniel Gedon, Uppsala University / E-mail / Web dgedon.github.io / Twitter @danigedon / arXiv link:*。页脚 22/22 | 联系方式页。 |

**（无 >27 项的情形；讲稿全部 27 页已逐页覆盖。所有页均为"未见图注"——幻灯片无图注体例。）**

## 6. 对 P1 的用处

- **与 P1 的关系**：**不同问题（背景/术语来源）**。本材料是**系统辨识视角的深度学习综述讲稿**，其七章骨架（建模→架构→优化→深度核→理论→应用→结论）中，**没有一章是"连续时间/ODE 网络"**（PAGE 8 的架构族清单逐字为 FNN / skip connections / CNN / RNN / latent variable models（AE、VAE、deep SSM）/ energy-based models，**不含 ODE-RNN、Neural ODE、LTC 或 CfC**）。对 P1 的控制器选型、100 Hz 回路、MCU 部署**都不构成证据**。

- **可迁移**：
  1. **术语框架（可整段借用的叙述结构）**：PAGE 5 的"辨识三要素"（**模型族 + 参数估计 + 验证**）与 PAGE 6 的"经典辨识 ↔ 深度学习流程逐节点对照"（模型族↔架构、模型结构/超参↔架构超参、实验设计↔数据采集、参数估计↔训练、验证↔验证）。→ P1 的 Related Work 若要把"OTF-CfC 属于系统辨识还是控制"讲清楚，这套对照能一句话定位：**P1 学的是控制器而非辨识模型，其"验证"是闭环指标而非残差分析**。
  2. **"核 = 先验假设的编码"（PAGE 14）与"输入空间变换降低 RKHS 范数"（PAGE 15）**：前者可直接支撑 P1 把 OTF 写成 **inductive bias / structure prior**（与 `AGENTS.md` §1 术语口径一致）；后者给出"**变换输入空间**而非改损失函数"的类比（OTF 势场作为输入/条件变换）。**两条都只能作"框架类比"引用，不能作证据。**
  3. **★ 两个可引用的量级数字（PAGE 17，逐字）**：*2-layer ConvNet on MNIST: **1.2m parameters vs 60k data points***；*AlexNet on ImageNet: **62.3m parameters vs 1.2m data points***。→ 当 P1 需要说明"现代深度模型在参数量远超数据量时仍能泛化"这一背景时可用；**须注明是讲稿幻灯片给出的量级示例，未给引用出处**。
  4. **★ 隐式正则化的定量关系（PAGE 21，逐字）**：修正代价 **Ṽ(θ)=V(θ)+λR(θ)**，**λ = α·#features/4**，**R(θ)=(1/#features)Σ_j(∂_jV(θ))²**。→ **对 P1 的 A2 消融设计有直接后果**：学习率 α、参数量 #features 与隐式正则强度三者耦合，因此"LNN vs CfC vs ODE-RNN"的对比**不能只对齐参数量**，还须对齐优化器与学习率调度，否则差异可能来自隐式正则而非架构。**这条应写进 P1 的消融协议。**
  5. **"参数量远超数据量仍泛化"的辨识领域先例（PAGE 18）**：在 **NARX + 100 个训练样本 + 1 步预测**的纯辨识设定下重演 double descent（"interpolate and generalize"）。→ P1 若在少量实车数据上训练 LNN，可引此说明"小数据 + 过参数化"在辨识领域已有先例。⚠ **无任何数值标注**。
  6. **两个应用基准的量级（PAGE 24/25）**：silverbox（forced Duffing oscillator）上 **线性 Box-Jenkins 型模型 Fit 29.7% vs 级联前馈网络 Fit 99.2%**；coupled electronic drives 上 **#train = 300 时深度模型仍拟合良好**，参数量 **dim(θ_FF)=184,200 / dim(θ_LSTM)=169,801 / dim(θ_DSSM)=111,902**。→ **只可用于说明"在经典辨识基准上深度模型可大幅超过线性模型"的量级**；**不得作为 P1 的性能对标**（基准、指标、协议全不同）。

- **不可迁移 / 陷阱**：
  1. **★ 材料是讲稿，不是论文**：本卡不含该综述的任何正文、图表编号、定理、参考文献与实验细节。**任何"该综述指出/证明/报告……"的写法都不成立**；只能写"Pillonetto 等在 ERNSI Workshop 2023 讲稿中列出……"。
  2. **架构清单不含连续时间网络**（PAGE 8）：该清单是幻灯片级别的列举，**不能据此断言"该综述未覆盖 Neural ODE / LTC / CfC"**（全文未见，`[待核实]`）；同样**不能反推**该综述支持 LNN 路线。
  3. **幻灯片数字全部缺少协议**：29.71% / 99.2% / 99.31% / 184,200 / 169,801 / 111,902 都是**屏幕截图内的文字**，无数据集划分、无重复次数、无 CI、无硬件。→ **不可进入 P1 的任何对比表**。
  4. **数字排版歧义**："dim(θ_FF) = 184, 200" 中的空格在 PDF 文本层被拆开，**应为 184,200**（依据同页 169,801 / 111,902 的写法）——属**推断**，标 `[待核实]`。
  5. **"Fit" 指标未定义**：PAGE 24/25 的 "Fit"（29.7% / 99.2% / 82.5–92.5）**未给定义**（常见为 `100·(1−‖y−ŷ‖/‖y−ȳ‖)`，但讲稿未写）。→ 引用必须写"Fit（定义未在讲稿给出）"。
  6. **理论部分无定理**：PAGE 17–22 的 double descent / 隐式正则 / NTK 全部为**叙述与公式片段**，**无定理编号、无假设条件、无证明**，属 D 级（假设/概述）。→ P1 引用这些结论时**必须改引原始文献**（如 NTK 的原始论文），不得引本讲稿。
  7. **讲稿日期与正式版不同步**：讲稿为 2023-09-26，arXiv v1 为 2023-01-30，**正式版 Automatica 2025 年 1 月**。→ 讲稿**必然落后于正式版**至少 16 个月；**不得用讲稿的章节结构代表正式版的结构**。
  8. **本卡未做外部复现与取代检查**：该综述的"最新性"与"是否已被更新的综述取代"本卡**未检索**，标 `[待核实]`。

- **与 CfC（NMI 2022）的关系**：**无同源关系；本材料对 CfC 不提供任何证据。**
  - 讲稿的架构清单（PAGE 8）**不含** LTC / CfC / Neural ODE；讲稿的核方法与理论部分（deep kernel、NTK、double descent）与 CfC 的"闭式解替代 ODE 求解器"路线**正交**。
  - **对本卡的判断**：从**讲稿**看，系统辨识社区（Pillonetto/Ljung/Schön 一系）的综述框架**未把连续时间/液态网络列为独立架构族**。这是一个**观察**，**不是结论**——正式版全文未见，可能在某章某节讨论。
  - **对 P1 的直接含义**：若 P1 要在 Related Work 里声称"连续时间网络在系统辨识综述中已被覆盖/未被覆盖"，**必须先读 Automatica 正式版全文**；在此之前**不得作任何此类断言**（否则违反 `[待核实]` 纪律与"不编造"条款）。

- **引用时必须带的限定语**：
  "本组所核验的材料为 Pillonetto 等在 **ERNSI Workshop 2023（斯德哥尔摩，2023-09-26）的讲稿幻灯片**（27 页 / 9,915 字符），**不是论文全文**；其对应的正式综述为 Pillonetto G, Aravkin A, Gedon D, Ljung L, Ribeiro AH, Schön TB. *Deep networks for system identification: A survey*. **Automatica 2025;171:111907（DOI 10.1016/j.automatica.2024.111907，Crossref 核验 2026-10-03）**，arXiv 版为 2301.12832（v1, 2023-01-30）。**本组未读该综述全文**，因此：① 讲稿中的一切（七章目录、架构族清单、29.7%/99.2%/99.31% 的 Fit、dim(θ)=184,200/169,801/111,902、λ=α·#features/4）**均为幻灯片级陈述，缺失数据集划分、重复次数、不确定度与硬件**；② 正式版的结构、图表、定理与结论**不由此讲稿代表**；③ 讲稿的架构族清单**不含连续时间/ODE/液态网络**，但**不得据此断言正式综述未覆盖该方向**。"

- **P1 落地三问**：
  1. **是否有硬件实测？** **讲稿中未见（本卡未见全文）。** 幻灯片只出现两个软件基准：**Matlab 的 forced Duffing oscillator（silverbox benchmark）** 与 **Pytorch 的 coupled electronic drives benchmark**；**无任何 MCU/嵌入式/实时性/内存/时延内容**。→ 就本卡材料而言，**"无"**；正式版是否有，`[待核实]`。
  2. **是否报告参数量？** **讲稿中有一处，且只有一处**（PAGE 25）：**dim(θ_FF) = 184,200（前馈）；dim(θ_LSTM) = 169,801（LSTM）；dim(θ_DSSM) = 111,902（深度状态空间模型）**，条件是 **#train = 300**。⚠ 数字中含 OCR/排版空格，**是否为 184,200 属推断**（标 `[待核实]`）。**口径（是否含感知/特征提取部分）未说明**——该基准为**电子驱动系统辨识**，无感知头。→ **P1 不得用这三个数字做任何参数量预算参照**（任务、输入维、时间尺度全不同）。
  3. **训练是在线还是离线？** **讲稿中未见说明（本卡未见全文）。** 幻灯片只描述"参数估计/训练"流程与优化器（一阶方法、学习率调度），**未出现 online / incremental / streaming training 的字样**。两个应用基准均为**离线拟合 + 仿真响应对比**（*Simulated Response Comparison*）。→ 就本卡材料而言，**倾向离线，但 `[待核实]`**；**无任何内存或时间开销可报告**。

## 7. 缺失信息（≥3 条，写成可执行动作）
1. **★ 必须取得 Automatica 正式版全文（DOI 10.1016/j.automatica.2024.111907）并重做本卡**。→ 动作：通过机构订阅或作者主页/arXiv v-latest 获取全文（arXiv 2301.12832 全文 HTML 可用），核验：七章结构、架构族清单是否含连续时间/ODE 网络、图表编号与图注、参考文献条数、以及 §6 Applications 两个基准的完整协议。**在这之前，本卡的一切内容不得进入 P1 稿件。**
2. **需取回正式版摘要原文并替换本卡 §2**：本卡 §2 是 **arXiv v1 摘要的中文转述**（Crossref 的 Elsevier 记录**不含摘要**）。→ 动作：从 ScienceDirect 或 arXiv 最新版取英文摘要**逐字**，与本卡 §2 比对并记录差异。
3. **需补齐两个应用基准的完整协议**：silverbox（数据集来源、采样率、训练/验证/测试划分、Fit 的定义与公式、重复次数）与 coupled electronic drives（#train=300 之外的信息、模型超参、训练轮次、硬件）。（后果：讲稿里的 29.7%/99.2%/99.31% 目前**不可复核、不可比较**。）
4. **需核验幻灯片数字的准确性**：`dim(θ_FF) = 184, 200` 的空格是排版产物还是原意；`Fit is 99.2%` 与截图内 `mN2: 99.31%` 是同一指标的两次测量还是两个模型。（后果：避免把 OCR 噪声当成论文数字引用。）
5. **需核验"讲稿是否落后于正式版"**：讲稿 2023-09-26 vs 正式版 2025-01（Crossref `issued: 2025-01`）。→ 动作：比对 arXiv 最新版与讲稿的章节结构差异，记录"讲稿→正式版"的增删。
6. **需做 T5 撤稿/更正检查**：按 DOI 注册机构分流——`10.1016/j.automatica.2024.111907` 为 Elsevier/Crossref，应查 `api.crossref.org/works/10.1016/j.automatica.2024.111907` 的 `update-to` 字段。**本卡未做此检查**，标 `[待核实]`（Crossref 记录中 `relation: {}` 为空，但 `update-to` 未单独核）。
7. **需做 T2 取代检查**：检索 2025 年后是否有更新的"深度学习用于系统辨识"综述。→ 动作：OpenAlex/Crossref 检索并记录检索式与日期（本卡未做，标 `[待核实]`）。
8. **需明确该综述对 P1 的实际用途边界**：本卡结论是"对 P1 的证据贡献 ≈ 0，术语与背景贡献有限"。→ 动作：若 P1 的 Related Work 仍需引用系统辨识视角，**优先引具体方法原文**（如 NARX 的原始文献、stable spline 核的原始文献），而不是引这篇综述讲稿。

## 8. 关键数字（只抄**讲稿明确印出的**文字；正式版数字本卡一概未见）

> ⚠ 纪律：下表**全部来自讲稿幻灯片的文本层**，均为**幻灯片级陈述**，**无数据集划分、无重复次数、无不确定度、无硬件**。**不得进入 P1 的任何对比表**；引用时须写"讲稿幻灯片给出，协议未说明"。

| 指标 | 值 | 不确定度 | 出处（讲稿页） |
|---|---|---|---|
| 2 层 ConvNet 在 MNIST 上的参数量 vs 数据量 | **1.2m parameters vs 60k data points** | 未给（且**未给引用出处**） | PAGE 17（页脚 13/22） |
| AlexNet 在 ImageNet 上的参数量 vs 数据量 | **62.3m parameters vs 1.2m data points** | 未给（且**未给引用出处**） | PAGE 17 |
| 牛顿法复杂度 | **O(#train·#param² + #param³)** | 无 | PAGE 11（页脚 8/22） |
| 隐式正则化的修正代价 | **Ṽ(θ)=V(θ)+λR(θ)**，**λ = α·#features/4**，**R(θ)=(1/#features)Σ_{j=1}^{#features}(∂_jV(θ))²** | 无（**无定理、无假设条件、无证明**） | PAGE 21（页脚 17/22） |
| double descent 的表述 | *"Double descent" → **interpolate and generalize*** | 无 | PAGE 17 |
| 线性方程组解的三种情形 | **#features < #train ⇒ 无解**；**= ⇒ 唯一解**；**> ⇒ 多解**；梯度下降收敛到**最小范数解** | 无 | PAGE 20（页脚 16/22） |
| silverbox 基准：线性 Box-Jenkins 型模型 | **Fit is 29.7%**（截图内另印 **mbj: 29.71%**） | 无（**"Fit" 定义未给**） | PAGE 24（页脚 19/22） |
| silverbox 基准：级联前馈网络 | **Fit is 99.2%**（截图内另印 **mN2: 99.31%**） | 无 | PAGE 24 |
| coupled electronic drives：训练样本数 | **#train = 300** | 无 | PAGE 25（页脚 20/22） |
| coupled electronic drives：前馈模型参数量 | **dim(θ_FF) = 184, 200**（⚠ 空格疑为排版产物，**应为 184,200**，`[待核实]`） | 无（口径未说明） | PAGE 25 |
| coupled electronic drives：LSTM 参数量 | **dim(θ_LSTM) = 169, 801**（同上，**应为 169,801**） | 无 | PAGE 25 |
| coupled electronic drives：深度状态空间模型参数量 | **dim(θ_DSSM) = 111, 902**（同上，**应为 111,902**） | 无 | PAGE 25 |
| coupled electronic drives：Fit 条形图纵轴范围 | **82.5 – 92.5**（Linear / FC / LSTM / Deep SSM 四条） | 无（**各条形具体值未印出**） | PAGE 25 |
| 深度学习最成功架构清单（开放问题页） | Attention models and transformers；Flow-based models；GANs 与 diffusion models；Graph neural networks | — | PAGE 26（页脚 21/22） |
| 讲稿章节数 | **7**（Modeling of dynamical systems / DNN architectures / Optimization / Deep kernel-based learning / Theoretical development / Applications / Conclusion） | — | PAGE 4（页脚 2/22） |
| 讲稿列出的 DNN 架构族数 | **6 类**（Fully-connected / Skip and direct connections / Convolutional / Recurrent / Latent variable models（AE, VAE, Deep SSM）/ Energy-based models） | — | PAGE 8（页脚 5/22） |
| 核类型（讲稿列举） | 线性核 ⇒ **FIR**；线性核 P_ij=λ^{max(i,j)} ⇒ **stable spline/TC 核**；高斯核 ⇒ **NFIR** | — | PAGE 14（页脚 10/22） |
| NARX 示例的训练样本数（理论部分） | **#train = 100** | 无 | PAGE 18（页脚 14/22） |
| 讲稿规模 | **27 页**（页脚编号至 22/22，含 3 张重复目录页）；**9,915 字符** | — | 本地 .txt 头部 + 逐页核验 |
| 讲稿时间与地点 | **ERNSI Workshop 2023，斯德哥尔摩，2023-09-26** | — | PAGE 1 |
| 联系人与单位 | Daniel Gedon, **Uppsala University**，daniel.gedon@it.uu.se，dgedon.github.io，@danigedon | — | PAGE 27（页脚 22/22） |

**在线核验结果（2026-10-03，本卡唯一的外部证据来源）**

| 项目 | 核验值 | 来源（通道 + 查询式） |
|---|---|---|
| 正式发表信息 | **Automatica, vol. 171, 2025, article 111907**；`issued: 2025-01`；`published-print: 2025-01`；`created: 2024-09-21`；`reference-count: 364`；`is-referenced-by-count: 96`；ISSN 0005-1098；publisher: Elsevier BV | Crossref REST：`api.crossref.org/works?query.bibliographic=Deep+networks+for+system+identification+a+survey+Pillonetto&rows=3`（HTTP 200） |
| 正式版 DOI | **10.1016/j.automatica.2024.111907** | 同上 |
| 正式版标题 | *Deep networks for system identification: **A** survey*（大写 A，与讲稿首页小写 "a survey" 不同） | 同上 |
| 正式版作者（6 人，顺序） | Gianluigi Pillonetto（first）；Aleksandr Aravkin；Daniel Gedon；Lennart Ljung；Antônio H. Ribeiro；Thomas B. Schön | 同上 |
| 正式版摘要 | **Crossref 记录不含摘要**（Elsevier 未存 abstract 字段）→ 本卡 §2 改用 **arXiv 摘要** | 同上（缺失） |
| arXiv 版 | **arXiv:2301.12832（cs.LG; eess.SY）**，标题 *Deep networks for system identification: a Survey*，**v1 提交 2023-01-30**，仅一个版本；DOI 10.48550/arXiv.2301.12832；license: arXiv non-exclusive | `export.arxiv.org/abs/2301.12832`（HTTP 200） |
| arXiv 摘要取得 | 已取（见 §2 中文转述；关键短语：*survey of deep learning from a system identification perspective*、*feedforward, convolutional, and recurrent networks*、*first-order optimization tools*、*connections to the well-studied area of kernel-based methods*、*deep kernel-based methods*、*overparameterized models … implicit regularization … benign overfitting*） | 同上 |
| 许可 | 正式版含 CC-BY（Crossref `license` 中 `content-version: vor`，`URL: creativecommons.org/licenses/by/4.0/`，起始 2024-09-04） | Crossref `works/10.1016/j.automatica.2024.111907`（HTTP 200） |
| 讲稿的本地路径与字符数 | `literature/fulltext/meeting2/deep-networks-for-system-identification-a-survey__ae332610.txt`，**PAGES=27 / CHARS=9,915** | 本地核验 |

⚠内部不一致：讲稿首页标题为小写 "**a survey**" 且 **arXiv link 文字后为空（未印 URL）**；在线核验得到的正式版标题为大写 "**A survey**"。→ **标题大小写与链接缺失两处不一致**，引用须以正式版为准并把讲稿标注为 slides。

【确定】/【待核实】标注：讲稿内容与页码为本地逐页核验【确定】；正式发表信息与 arXiv 摘要为 2026-10-03 在线取用【确定】；`dim(θ)` 的空格歧义、Fit 定义、"讲稿是否代表正式版结构"均为 **`[待核实]`**；**该综述的全文内容一律未读**。
