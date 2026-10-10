// build.mjs — merge curated mapping + verified metadata -> final list (md/jsonl/bibtex).
import fs from 'node:fs';
const main = JSON.parse(fs.readFileSync('dois_checked.json', 'utf8'));
const appx = JSON.parse(fs.readFileSync('dois_appendix_checked.json', 'utf8'));
const byN = new Map([...main, ...appx].map((r) => [r.n, r]));

// Curation: display grouping + why it matters for P1 (OTF-CfC) + corrections found during verification.
// Overrides for entries whose Crossref DOI is not registered (arXiv-only / PMLR-only).
// All values verified by the reader against the publisher's own record (see search-log §6, item 7).
const OVERRIDE = {
  12: {
    crossref_title: 'Addressing Function Approximation Error in Actor-Critic Methods',
    year_crossref: 2018, venue: 'Proc. 35th International Conference on Machine Learning (ICML), PMLR 80',
    short_venue: 'ICML (PMLR 80)', volume: null, issue: null, page: '1587-1596',
    authors: ['Scott Fujimoto', 'Herke van Hoof', 'David Meger'], publisher: 'PMLR',
    verdict: 'ARXIV-ONLY(Crossref DOI not registered)', jaccard: null, is_journal: false,
  },
  13: {
    crossref_title: 'Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor',
    year_crossref: 2018, venue: 'Proc. 35th International Conference on Machine Learning (ICML), PMLR 80',
    short_venue: 'ICML (PMLR 80)', volume: null, issue: null, page: '1861-1870',
    authors: ['Tuomas Haarnoja', 'Aurick Zhou', 'Pieter Abbeel', 'Sergey Levine'], publisher: 'PMLR',
    verdict: 'ARXIV-ONLY(Crossref DOI not registered)', jaccard: null, is_journal: false,
  },
};

const CUR = [
  [1, 'A', 'P1 控制器的直接方法学祖先（CfC 即本文控制器选型）；含 NMI 原文与 Publisher Correction 的引用注意'],
  [2, 'A', 'LNN 在真实机器人闭环控制上的最强实机证据（含 out-of-distribution 飞行）；P1 用它支撑“LNN 可上车/上机”'],
  [3, 'A', 'NCP 结构在自动驾驶飞行任务中的可解释控制；P1 的“小参数 + 可审计”论据'],
  [4, 'A', '在线验证（online verification）防止自动驾驶致害：P4 隔离层与 P1 安全对比的直接前置'],
  [5, 'A', '连续时间动力系统（脉冲网络）的在线训练：与“伴随法/直接 BP”消融 A5 同类问题'],
  [6, 'A', '算子学习：把“函数到函数”映射用于动力学；P2 势场算子的理论参照'],
  [7, 'A', 'PINN 用于动力学控制：与“把 OTF 势场作为 ODE 边界条件”最接近的范式'],
  [8, 'A', '连续时间动力学系统辨识综述：P1“用真实轨迹拟合控制曲线”的方法论边界'],
  [9, 'B', 'RL 用于自动驾驶的权威综述；P1 解释为什么选用 RL/连续控制的语境（学位论文 TD3 属此谱系）'],
  [10, 'B', '专门针对运动规划的 DRL 综述：P1 基线与评价协议的来源'],
  [11, 'B', '高速公路自动驾驶运动规划综述：P1 的 ODD 与基线（PID/MPC）分类框架'],
  [12, 'B', '学位论文 TD3 直控基线的原始算法（ICML 2018, PMLR 80:1587–1596）；引 PMLR 正式版，不引 arXiv'],
  [13, 'B', '连续控制 RL 基线；P1 若以 RL 作对照需引其正式出处'],
  [14, 'B', '深度学习自动驾驶的安全挑战综述：P1 安全论证与失效分类'],
  [15, 'B', '类人跟驰的 DRL 模型：与 OTF 势场最接近的“社会压力→跟驰”替代路线，必须显式对比'],
  [16, 'B', 'RL 速度控制同时优化安全/效率/舒适：P1 指标（加速度平方积分、Jerk）的可比对象'],
  [17, 'B', '换道决策的 DRL + 风险意识：超车/换道工况（OTF 定义域）的直接相关基线'],
  [18, 'B', '最优控制 vs 强化学习在极限竞速的对照：P1“MPC 基线 vs CfC”的同类公平性讨论'],
  [19, 'B', '带 GP 回归的谨慎 MPC：MPC 基线在不确定性下的处理方式，用于公平对比'],
  [20, 'C', '高阶 CBF：P4 安全过滤器的理论工具（相对阶问题）'],
  [21, 'C', '自适应 CBF：模型不确定下的安全保证；对抗“CfC 拟合误差导致安全性无保证”的质疑'],
  [22, 'C', '鲁棒 CBF：约束镇定下的安全性；P1/P4 的鲁棒性论证素材'],
  [23, 'C', 'CBF-QP 奠基性期刊论文（TAC 2017）：安全层形式化的标准出处'],
  [24, 'C', '预测式安全过滤器：可直接套在 LNN 控制器输出后的安全层设计'],
  [25, 'C', '安全学习综述：从基于学习的控制到安全 RL 的完整地图（P4 的定位依据）'],
  [26, 'C', '学习型控制的安全框架（不确定机器人）：把学习模块包进安全集的形式化模板'],
  [27, 'C', '可达性分析集合传播：长尾场景（前车急刹、cut-in）安全性证明的工具'],
  [28, 'C', '自动驾驶规划与决策综述：P1 决策层的边界与术语规范'],
  [29, 'D', '真实交通中的 CACC 实测：编队/跟驰实验协议的现实参照'],
  [30, 'D', 'CACC 网络感知的弦稳定性分析：通信/采样对稳定性的影响，支撑 P1 非均匀采样论证'],
  [31, 'D', 'CACC 通信-驾驶人-控制三方面综述：混行与人工驾驶异质性的入口'],
  [32, 'D', '信息流拓扑对编队稳定性与可扩展性的影响：P1 编队拓扑选择依据'],
  [33, 'D', 'Lp 弦稳定性：弦稳定性的可操作定义与判据（P1 必须报告的指标）'],
  [34, 'D', '编队弦稳定性的控制器综合方法：与 CfC 控制器对比的理论基线'],
  [35, 'D', '含扰动的时延间距策略与弦稳定性：前车加减速扰动下的稳定性条件（P1 动态扰动设计）'],
  [36, 'D', '重型车编队的协同前瞻控制（节油+安全）：多目标（效率/舒适）控制的工程模板'],
  [37, 'D', '时变异质时延下编队分布式协议的实验验证：P1 端到端延迟指标的现实基准'],
  [38, 'D', '纵横向联合的编队控制（扩展前瞻）：P1 纵向+横向双指标（车道居中、转角方差）的对照'],
  [39, 'D', '极限操纵下的 MPC 车辆镇定：MPC 基线的强度上限（避免“稻草人基线”批评）'],
  [40, 'D', '用实验数据建模 CACC/ACC 动态响应：仿真-实测差距的量化范式（P1 sim-to-real 章节）'],
  [41, 'D', '跟驰模型中的人因综述：OTF 作为“社会压力”的人因合法性来源'],
  [42, 'D', '网联自动驾驶对交通流稳定性与通行能力的影响：混行比例作为自变量的标准做法'],
  [43, 'D', '用自动驾驶车辆消散 stop-and-go 波的实地实验：混行控制有效性的最强实证（P1 场景动机）'],
  [44, 'D', '混行高速公路上编队运行的定量分析与设计：P1 ODD 的解析化处理'],
  [45, 'D', 'DeeP-LCC：混流行驶中数据驱动的领航巡航控制，与 CfC 路线最接近的竞争方法'],
  [46, 'E', '轨迹预测综述：P1 用 IDM 作扰动、P2 换 WLA 输出的接口定义'],
  [47, 'E', '运动规划现状与展望：P1 在“规划-控制”链条中的定位'],
  [48, 'E', '自动驾驶里程碑综述（Survey of Surveys）：选题定位与引用地图'],
  [49, 'E', '世界模型综述（IEEE T-IV 正式版）：P2 的定位与术语来源'],
  [50, 'E', '多模态端到端驾驶：P1 对比“端到端黑箱”与“可解释势场+连续控制”的差异'],
  [51, 'F', 'Koopman 算子：把非线性动力学线性化的另一条“可解释结构”路线，与 CfC 路线对照'],
  [52, 'F', '自主磁控结肠镜：NMI 上“学习+安全+实机”的跨域范例（写作层面的结构参照）'],
  [53, 'F', '大规模网络控制的 RL：NMI 上“可扩展性 + 效率”论证范式（P1 参数/延迟论证参照）'],
  [101, 'X', 'arXiv 预印本，无 Crossref DOI：NeurIPS 2018 最佳论文，NODE/伴随法理论根基'],
  [102, 'X', 'LNN 原始论文（CfC 的前身），AAAI 2021 正式版；P1 控制器谱系的必引起点'],
  [103, 'X', 'NCP 可审计自主性；P1 的“小参数 + 可审计”论据。⚠ 项目原清单所附 arXiv:2003.08554 指向另一篇论文，不得附 arXiv 链接'],
  [104, 'X', 'arXiv 预印本（正式题名 "Latent ODEs for Irregularly-Sampled Time Series"，NeurIPS 2019）：非均匀采样建模的基石'],
  [105, 'X', '弦稳定性的奠基期刊论文（Darbha & Hedrick, IEEE TAC 1996）。⚠ 核验更正：常被误引为 Swaroop & Hedrick；该 DOI 实为 Morse 的 supervisory control 一文，故不附 DOI，仅给题录'],
  [106, 'X', 'IDM 的原始出处（PRE 2000）；P1 用 IDM 模拟前车加减速扰动的参数与方程来源'],
  [107, 'X', 'Gipps 跟驰模型（TR-B 1981）；安全距离型跟驰基线的经典参照'],
  [108, 'X', 'FVD 全速度差模型（PRE 2001）；跟驰模型谱系补全，用于说明 OTF 之外的既有“压力式”建模传统'],
  [109, 'X', 'MOBIL 换道模型的正式期刊出处。⚠ 核验更正：正式题名为 "General Lane-Changing Model MOBIL for Car-Following Models"（TRR 1999: 86–94），不是 "MOBIL: General lane-changing model for traffic simulators"'],
  [110, 'X', '增强 IDM（驾驶策略对通行能力的影响）：P1 用 IDM 模拟前车扰动时的参数来源'],
  [111, 'X', 'CBF 理论与应用教程（ECC 2019）：安全层教学的规范引用'],
  [113, 'X', 'highD 高速公路自然驾驶轨迹数据集：与学位论文高速主线数据最可比的公开数据'],
  [114, 'X', 'nuScenes：P2 数据集（CVF 页码 11621–11631 与 IEEE 11618–11628 不可混用）'],
  [115, 'X', 'CARLA 开源城市驾驶仿真器（CoRL 2017, PMLR 78:1–16）；P1/P2 仿真平台。arXiv comments 已注明发表于 CoRL'],
  [116, 'X', 'CVPR 2023 最佳论文（规划导向端到端）：P5 全栈联合训练对标'],
  [117, 'X', '端到端自动驾驶挑战与前沿（TPAMI 2024）：P1/P5 定位与动机综述'],
  [118, 'X', 'MTR++（TPAMI 2024）：MTR 的期刊扩展版，IEEE 格式优先引用'],
  [119, 'X', 'DriveDreamer 正式版（ECCV 2024, LNCS pp. 55–72）：P2 直接对标。⚠ 不得再写“arXiv 预印本”'],
  [120, 'X', 'TransFuser（TPAMI 2023）：端到端传感器融合模仿学习对照。⚠ 本次核验 Crossref 未注册该 DOI（10.1109/TPAMI.2022.3200242 返回未注册）→ 引用前必须复核，暂标 [待核实]'],
  [121, 'X', 'DriveGPT4（RA-L 2024）：P3 的可解释端到端对照'],
  [123, 'X', '域随机化（IROS 2017）：sim-to-real 标准手段之一'],
  [125, 'X', '社会力模型（PRE 1995）：把“社会压力”写成势场的最经典先例，OTF 势场化的类比基础'],
];

const rows = CUR.map(([n, grp, why]) => {
  const r = byN.get(n);
  if (!r) return { n, grp, why, missing: true };
  const c = r.check || {};
  // When the DOI is not registered in Crossref (or resolves to a DIFFERENT paper), the bibliographic
  // truth must come from the independently verified record, not from Crossref. Fall back to the claim
  // only in those two cases; otherwise Crossref wins.
  const crOk = c.exists === true && (c.verdict === 'OK' || c.verdict === 'WEAK');
  const title = crOk ? c.title : (r.claim && r.claim.title) || c.title || null;
  const year = crOk ? c.year : (r.claim && r.claim.year) || c.year || null;
  const venue = crOk ? c.venue : (r.claim && r.claim.venue) || c.venue || null;
  const isJournal = !!(c.venue && !/Conference|Symposium|Proceedings|Lecture Notes|arXiv/i.test(c.venue));
  const base = {
    n, group: grp, why,
    key: r.key,
    crossref_title: title,
    year_crossref: year,
    year_note: crOk
      ? (r.claim && r.claim.year && c.year && r.claim.year !== c.year ? `清单年份 ${r.claim.year} → Crossref 记录 ${c.year}` : null)
      : 'Crossref 未注册该 DOI（或该 DOI 指向另一篇论文）→ 字段取自独立核验记录，引用前须复核',
    venue: venue,
    short_venue: c.short_venue || null,
    volume: c.volume || null, issue: c.issue || null, page: c.page || null,
    authors: c.authors || [],
    publisher: c.publisher || null,
    doi: r.doi,
    // Only emit a resolvable link when the DOI is actually registered (or when an arXiv id is known).
    url: (crOk && r.doi && !r.doi.startsWith('10.48550/'))
      ? `https://doi.org/${r.doi}`
      : (r.claim && r.claim.arxiv ? `https://arxiv.org/abs/${r.claim.arxiv}`
        : (r.doi && r.doi.startsWith('10.48550/') ? `https://arxiv.org/abs/${r.doi.replace('10.48550/arXiv.', '')}` : null)),
    crossref_cited_by: c.crossref_cited_by ?? null,
    verdict: c.verdict || (c.exists === false ? 'NOT-REGISTERED' : 'ARXIV-ONLY'),
    jaccard: c.jaccard_vs_claim ?? null,
    is_journal: isJournal,
  };
  return OVERRIDE[n] ? { ...base, ...OVERRIDE[n], doi: r.doi } : base;
});

fs.writeFileSync('final_list.json', JSON.stringify(rows, null, 2), 'utf8');

// JSONL (machine readable candidate pool, paper-discovery schema-ish)
const jsonl = rows.filter((r) => !r.missing).map((r) => JSON.stringify({
  id: r.doi ? `doi:${r.doi}` : `title:${r.key}`, n: r.n, doi: r.doi, title: r.crossref_title, year: r.year_crossref,
  venue: r.venue, authors: r.authors, volume: r.volume, issue: r.issue, page: r.page,
  url: r.url, crossref_cited_by: r.crossref_cited_by, group: r.group, why: r.why,
  verification: { source: r.doi && r.doi.startsWith('10.48550/') ? 'arxiv' : 'crossref', title_jaccard: r.jaccard, verdict: r.verdict },
  added: '2026-10-02', project: 'auto-driving/P1-OTF-CfC',
}));
fs.writeFileSync('final_list.jsonl', jsonl.join('\n') + '\n', 'utf8');

// markdown table
const esc = (s) => (s || '').replace(/\|/g, '\\|');
let md = '';
let curGrp = null;
const GNAME = { A: 'A. 连续时间/流体神经网络（P1 控制器方法学）', B: 'B. 决策基线：强化学习与安全强化学习', C: 'C. 安全层：控制障碍函数与形式化验证', D: 'D. 跟驰、编队与混行交通（P1 场景与控制理论）', E: 'E. 预测/规划/世界模型（接口与定位）', F: 'F. 结构保持学习与跨域范式', X: 'X. 附录：奠基性会议论文与经典文献（不计入 50 篇期刊）' };
for (const r of rows) {
  if (r.group !== curGrp) { curGrp = r.group; md += `\n### ${GNAME[r.group]}\n\n| # | 论文（Crossref 权威题名） | 作者（首作者等） | 期刊 | 年 | 卷(期):页 | DOI / 链接 | Crossref 被引 | 与 P1 的关系 |\n|---|---|---|---|---|---|---|---|---|\n`; }
  md += `| ${r.n} | ${esc(r.crossref_title)} | ${esc((r.authors[0] || '?') + (r.authors.length > 1 ? ' et al.' : ''))} | ${esc(r.venue)} | ${r.year_crossref} | ${r.volume ? r.volume : '—'}${r.issue ? `(${r.issue})` : ''}:${r.page || '—'} | ${r.url ? `[${r.doi}](${r.url})` : `⚠ 未取得可解析标识（${r.doi || 'no DOI'}）`} | ${r.crossref_cited_by ?? '—'} | ${esc(r.why)} |\n`;
}
fs.writeFileSync('final_list_table.md', md, 'utf8');
console.error(`rows=${rows.length} journals=${rows.filter((r) => r.is_journal).length} md=${md.length} bytes`);
