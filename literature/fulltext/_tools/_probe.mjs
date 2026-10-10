const urls = process.argv.slice(2);
for (const u of urls) {
  try {
    const r = await fetch(u, {
      redirect: 'follow',
      headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36' },
    });
    const t = await r.text();
    console.log(String(r.status).padEnd(4), String(t.length).padStart(9), r.headers.get('content-type'), u);
  } catch (e) {
    console.log('ERR ', '-'.padStart(9), '-', u, '::', e.message);
  }
}
