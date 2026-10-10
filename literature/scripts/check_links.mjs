// 链接实测：node check_links.mjs
const LINKS = [
  ["CfC VoR PDF (NMI)", "https://www.nature.com/articles/s42256-022-00556-7.pdf"],
  ["CfC VoR 落地页", "https://www.nature.com/articles/s42256-022-00556-7"],
  ["CfC 更正", "https://doi.org/10.1038/s42256-022-00597-y"],
  ["CfC arXiv", "https://arxiv.org/abs/2106.13898"],
  ["LTC VoR PDF (AAAI OJS)", "https://ojs.aaai.org/index.php/AAAI/article/download/16936/16743"],
  ["LTC VoR 落地页", "https://ojs.aaai.org/index.php/AAAI/article/view/16936"],
  ["LTC arXiv", "https://arxiv.org/abs/2006.04439"],
  ["Chahine PDF (MIT CSAIL)", "https://cap.csail.mit.edu/sites/default/files/research-pdfs/Robust%20flight%20navigation%20out%20of%20distribution%20with%20liquid%20neural%20networks.pdf"],
  ["Chahine science.org", "https://www.science.org/doi/10.1126/scirobotics.adc8892"],
  ["DeepONet VoR 落地页", "https://www.nature.com/articles/s42256-021-00302-5"],
  ["DeepONet VoR PDF 端点", "https://www.nature.com/articles/s42256-021-00302-5.pdf"],
  ["DeepONet arXiv v3", "https://arxiv.org/abs/1910.03193"],
  ["DeepONet OSTI(镜像)", "https://www.osti.gov/servlets/purl/2281727"],
  ["sysid 综述 arXiv", "https://arxiv.org/abs/2301.12832"],
  ["sysid VoR DOI", "https://doi.org/10.1016/j.automatica.2024.111907"],
  ["sysid OA 副本(UU DiVA)", "https://uu.diva-portal.org/smash/get/diva2:1905714/FULLTEXT01"],
  ["sysid OA 副本(Unipd)", "https://www.research.unipd.it/bitstream/11577/3559960/1/1-s2.0-S0005109824004011-main.pdf"],
  ["PINC arXiv", "https://arxiv.org/abs/2104.02556"],
  ["PINC VoR DOI", "https://doi.org/10.1016/j.neucom.2024.127419"],
  ["TD3 PMLR v80 (猜测)", "https://proceedings.mlr.press/v80/fujimoto18a.html"],
  ["TD3 PMLR v80 索引", "https://proceedings.mlr.press/v80/"],
];
for (const [name, url] of LINKS) {
  let out = "";
  try {
    const r = await fetch(url, {
      redirect: "follow",
      headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" },
    });
    const ct = (r.headers.get("content-type") || "").split(";")[0];
    const len = r.headers.get("content-length") || "?";
    out = `${r.status} ${ct} len=${len} final=${r.url.slice(0, 90)}`;
    if (r.status === 200 && ct.includes("text/html")) { const t = await r.text(); out += ` | title="${(t.match(/<title[^>]*>([^<]{0,90})/i) || [, ""])[1].trim()}"`; }
  } catch (e) { out = "ERR " + e.message; }
  console.log(`${name.padEnd(30)} ${out}`);
  await new Promise((s) => setTimeout(s, 500));
}
