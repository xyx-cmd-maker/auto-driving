// rank2024.mjs — 对 2024+ 候选池做主题归类 + 相关性打分（层 1：仅标题）
import fs from "node:fs";
const DIR = "D:/Deepseek Harness/auto-driving/literature/fresh2024";
const rows = fs.readFileSync(`${DIR}/candidates_2024.jsonl`, "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l));

const T = (r) => (r.title || "").toLowerCase();
// 主题桶：命中即归入（可多归）
const BUCKETS = {
  LNN: [/liquid neural/, /liquid time-constant/, /liquid time constant/, /closed-form continuous/, /neural circuit polic/, /\bncp\b/, /liquid network/, /liquid graph/, /\bltc\b/, /liquid comput/],
  CT: [/continuous-time/, /continuous time/, /neural ordinary differential/, /neural ode/, /\bode\b.*(network|neural)/, /continuous-depth/, /spiking neural/, /state-space model/],
  CF: [/car-follow/, /car follow/, /platoon/, /string stability/, /mixed traffic/, /mixed autonomy/, /adaptive cruise/, /\bcacc\b/, /\bacc\b.*control/],
  OV: [/overtak/, /lane-chang/, /lane chang/, /cut-in/, /cutin/, /merg/],
  CTRL: [/control/, /controller/, /policy/, /decision-making/, /decision making/, /planning/],
  INT: [/interpretab/, /explainab/, /mechanistic/, /auditab/, /transparen/],
  EMB: [/microcontroller/, /\bmcu\b/, /embedded/, /\btinyml\b/, /edge deploy/, /on-device/, /real-time inference/, /quantiz/],
  SAFE: [/safety/, /safe /, /barrier function/, /verification/, /robust/],
  RL: [/reinforcement learning/, /\brl\b/, /actor-critic/, /\btd3\b/, /\bsac\b/, /\bppo\b/, /\bdqn\b/, /imitation learning/],
  SOCIAL: [/social/, /pressure field/, /potential field/, /interaction-aware/, /game theor/, /human-like/, /humanlike/],
};
// 强相关词（命中直接加权）
const STRONG = [
  [/liquid neural/, 12], [/liquid time-constant/, 12], [/closed-form continuous/, 12], [/neural circuit polic/, 10],
  [/string stability/, 9], [/car-follow/, 8], [/platoon/, 8], [/mixed traffic/, 7], [/overtak/, 7],
  [/neural ode/, 7], [/continuous-time/, 6], [/interpretab/, 5], [/microcontroller/, 6], [/tinyml/, 6],
  [/explanab/, 4], [/potential field/, 5], [/social force/, 5], [/mixed autonomy/, 6], [/cacc/, 5],
];
// 排除（命中即扣分）：与 P1 无关的邻域
const NEG = [
  [/medical|clinical|patient|eeg|ecg|cancer|covid|drug/, -14],
  [/recommendation|sentiment|speech|audio|image classification|segmentation|detection|point cloud|lidar/, -12],
  [/wireless|antenna|network traffic prediction|energy|battery|power grid|wind|solar/, -12],
  [/quadruped|manipulat|drone|uav|aerial|underwater|marine|surgical/, -8],
  [/financial|stock|economic|supply chain|agricultur/, -14],
  [/robot arm|grasp|locomotion|humanoid/, -8],
];
const score = (r) => {
  const t = T(r);
  let s = 0;
  for (const [re, w] of STRONG) if (re.test(t)) s += w;
  for (const [re, w] of NEG) if (re.test(t)) s += w;
  // 轻微时效与影响加权
  s += Math.min(4, Math.log10((r.cited || 0) + 1) * 2);
  if (r.year >= 2025) s += 1.5;
  return s;
};
const bucketOf = (r) => Object.entries(BUCKETS).filter(([, res]) => res.some((re) => re.test(T(r)))).map(([k]) => k);

for (const r of rows) { r.bucket = bucketOf(r); r.score = +score(r).toFixed(2); }
const rel = rows.filter((r) => r.score > 0).sort((a, b) => b.score - a.score);

console.log(`TOTAL=${rows.length}  with_score>0=${rel.length}`);
const byY = {};
for (const r of rows) byY[r.year] = (byY[r.year] || 0) + 1;
console.log("年份分布:", JSON.stringify(byY));

const KEY = ["LNN", "CT", "CF", "OV", "INT", "EMB", "SOCIAL"];
console.log("\n===== 主题 × 强相关 交叉（score 降序，每桶最多 22 条）=====");
for (const k of KEY) {
  const sub = rel.filter((r) => r.bucket.includes(k)).slice(0, 22);
  console.log(`\n### ${k}  (n=${rel.filter((r) => r.bucket.includes(k)).length})`);
  for (const r of sub) {
    console.log(`  ${String(r.score).padStart(6)} [${r.year}] c=${String(r.cited ?? "-").padStart(5)} ${(r.venue || r.source).slice(0, 34).padEnd(34)} | ${r.title.slice(0, 108)} | ${r.doi || r.arxiv || ""}`);
  }
}
fs.writeFileSync(`${DIR}/ranked_2024.jsonl`, rel.map((r) => JSON.stringify(r)).join("\n") + "\n", "utf8");
console.log(`\nWROTE ${DIR}/ranked_2024.jsonl  (n=${rel.length})`);
