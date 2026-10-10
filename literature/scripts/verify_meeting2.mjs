// 第二次组会 19 篇候选：Crossref 题录核验
// 用法: node verify_meeting2.mjs
import fs from "node:fs";

const MAILTO = "research@example.org";
const OUT = "D:/Deepseek Harness/auto-driving/literature/meeting2/crossref_verify.jsonl";

const TITLES = [
  "Deep Multi-Modal Object Detection and Semantic Segmentation for Autonomous Driving: Datasets, Methods, and Challenges",
  "Deep Learning for Image and Point Cloud Fusion in Autonomous Driving: A Review",
  "Deep Learning-Based Vehicle Behavior Prediction for Autonomous Driving Applications: A Review",
  "Methodology and Benchmark for Automated Driving Theory Test of Large Language Models",
  "A Review of Motion Planning for Highway Autonomous Driving",
  "Survey of Deep Reinforcement Learning for Motion Planning of Autonomous Vehicles",
  "Deep Reinforcement Learning for Autonomous Driving: A Survey",
  "A Deep Reinforcement Learning Method for Autonomous Driving Integrating Multi-Modal Fusion",
  "Interactive Decision-Making Integrating Graph Neural Networks and Model Predictive Control for Autonomous Driving",
  "LEAD: Learning-Enhanced Adaptive Decision-Making for Autonomous Driving in Dynamic Environments",
  "Safety Implications of Explainable Artificial Intelligence in End-to-End Autonomous Driving",
  "Q-Advantage Integrated Human-Guided Reinforcement Learning for Safe End-to-End Autonomous Driving",
  "Safety-Enhanced Deep Reinforcement Learning for Autonomous Driving: Dare to Make Mistakes to Learn Better and Faster",
  "Addressing Function Approximation Error in Actor-Critic Methods",
  "Accurate online training of dynamical spiking neural networks through Forward Propagation Through Time",
  "Deep networks for system identification: a survey",
  "Interpretable Autonomous Flight Via Compact Visualizable Neural Circuit Policies",
  "Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators",
  "Using online verification to prevent autonomous vehicles from causing accidents",
];

const jac = (a, b) => {
  const tok = (s) => new Set(s.toLowerCase().replace(/[^a-z0-9 ]/g, " ").split(/\s+/).filter((x) => x.length > 2));
  const A = tok(a), B = tok(b);
  const inter = [...A].filter((x) => B.has(x)).length;
  const uni = new Set([...A, ...B]).size;
  return uni ? inter / uni : 0;
};

const rows = [];
for (const t of TITLES) {
  const url = `https://api.crossref.org/works?query.bibliographic=${encodeURIComponent(t)}&rows=4&select=DOI,title,author,issued,container-title,volume,issue,page,type,is-referenced-by-count,publisher&mailto=${MAILTO}`;
  let rec = { query: t, ok: false, best: null, candidates: [] };
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const r = await fetch(url, { headers: { "User-Agent": `dsh-meeting2-verify/1.0 (mailto:${MAILTO})` } });
      if (!r.ok) throw new Error("HTTP " + r.status);
      const j = await r.json();
      const items = j.message.items || [];
      rec.candidates = items.map((it) => ({
        j: +jac(t, (it.title && it.title[0]) || "").toFixed(3),
        doi: it.DOI,
        title: (it.title && it.title[0]) || "",
        container: (it["container-title"] && it["container-title"][0]) || "",
        year: it.issued && it.issued["date-parts"] && it.issued["date-parts"][0] ? it.issued["date-parts"][0][0] : null,
        vol: it.volume || null, issue: it.issue || null, page: it.page || null,
        type: it.type, cited: it["is-referenced-by-count"],
        firstAuthor: it.author && it.author[0] ? [it.author[0].given, it.author[0].family].filter(Boolean).join(" ") : null,
        nAuthors: it.author ? it.author.length : null,
      }));
      rec.candidates.sort((a, b) => b.j - a.j);
      rec.best = rec.candidates[0] || null;
      rec.ok = !!(rec.best && rec.best.j >= 0.85);
      break;
    } catch (e) {
      rec.error = String(e.message || e);
      await new Promise((s) => setTimeout(s, 2500));
    }
  }
  rows.push(rec);
  console.log(`${rec.ok ? "OK  " : "CHK "} J=${rec.best ? rec.best.j : "-"}  ${rec.best ? rec.best.doi + " | " + rec.best.container + " " + (rec.best.vol || "") + "(" + (rec.best.issue || "") + ") " + (rec.best.year || "") + ":" + (rec.best.page || "") : rec.error || "no hit"}`);
  console.log(`      Q: ${t}`);
  if (rec.best) console.log(`      A: ${rec.best.title} [${rec.best.firstAuthor} et al., n=${rec.best.nAuthors}] cited=${rec.best.cited}`);
  await new Promise((s) => setTimeout(s, 1200));
}
fs.writeFileSync(OUT, rows.map((r) => JSON.stringify(r)).join("\n"), "utf-8");
console.log("\nWROTE " + OUT + "  n=" + rows.length + "  matched=" + rows.filter((r) => r.ok).length);
