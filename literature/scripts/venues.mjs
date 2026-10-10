// Verify ISSN / venue identity via OpenAlex sources endpoint (existence check, not memory).
const names = [
  'IEEE Transactions on Intelligent Transportation Systems',
  'IEEE Transactions on Intelligent Vehicles',
  'IEEE Transactions on Pattern Analysis and Machine Intelligence',
  'Transportation Research Part C: Emerging Technologies',
  'Transportation Research Part B: Methodological',
  'IEEE Transactions on Control Systems Technology',
  'IEEE Transactions on Vehicular Technology',
  'IEEE Robotics and Automation Letters',
  'Nature Machine Intelligence',
  'Journal of Field Robotics',
  'IEEE Transactions on Neural Networks and Learning Systems',
  'IEEE Robotics and Automation Magazine',
  'Annual Review of Control, Robotics, and Autonomous Systems',
  'IEEE Transactions on Automatic Control',
  'Automatica',
  'IEEE Internet of Things Journal',
  'IEEE Transactions on Mobile Computing',
  'Transportation Research Part A: Policy and Practice',
  'Transportation Science',
  'IEEE Transactions on Intelligent Transportation Systems Magazine',
  'Nature Communications',
  'Science Robotics',
  'Journal of Machine Learning Research',
  'IEEE Transactions on Emerging Topics in Computational Intelligence',
  'Neurocomputing',
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (const n of names) {
  const url = `https://api.openalex.org/sources?search=${encodeURIComponent(n)}&per-page=3&select=id,display_name,issn_l,issn,type,works_count,host_organization_name&mailto=research@example.org`;
  try {
    const j = await (await fetch(url)).json();
    console.log(`\n### ${n}`);
    for (const s of j.results || []) {
      console.log(`  - ${s.display_name} | issn_l=${s.issn_l} | issn=${(s.issn || []).join(',')} | type=${s.type} | works=${s.works_count} | host=${s.host_organization_name}`);
    }
  } catch (e) {
    console.log(`\n### ${n}\n  ERR ${e.message}`);
  }
  await sleep(400);
}
