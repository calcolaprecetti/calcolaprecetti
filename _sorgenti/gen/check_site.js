// Controllo del sito vero (percorsi assoluti), servito in locale come farà GitHub Pages
const { chromium } = require('playwright');
const BASE = 'http://localhost:8765';
const pages = ['/', '/termini-precetto/', '/interessi-moratori/', '/tassi/', '/privacy/', '/note-legali/', '/chi-sono/', '/valutazione-credito/'];
(async () => {
  const b = await chromium.launch();
  let bad = 0; const seen = new Set();
  for (const [name, w, h] of [['desktop', 1280, 900], ['telefono', 360, 760]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h } });
    for (const u of pages) {
      const p = await ctx.newPage(); const errs = [];
      p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
      p.on('pageerror', e => errs.push('pageerror ' + e.message));
      p.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
      await p.goto(BASE + u); await p.waitForTimeout(200);
      const r = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
        links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')), title: document.title,
        nav: [...document.querySelectorAll('.tools a')].map(a => a.innerText.trim() + (a.getAttribute('aria-current') ? '*' : '')).join(' | '),
        navFits: (() => { const n = document.querySelector('.tools .wrap'); return n.scrollWidth <= n.clientWidth + 1; })(),
        foot: document.querySelector('.foot-bottom').innerText.slice(0, 60) }));
      for (const l of r.links) if (l.startsWith('/')) seen.add(l.split('#')[0] + (l.includes('#') ? '#' + l.split('#')[1] : ''));
      const ok = !errs.length && r.sw <= r.cw + 1 && r.navFits; if (!ok) bad++;
      console.log(`${ok ? 'ok ' : 'NO '} ${name.padEnd(8)} ${u.padEnd(42)} ${r.sw}/${r.cw}  barra: ${r.nav}${r.navFits ? '' : ' (non entra)'}${errs.length ? '\n   ' + errs.join(' | ') : ''}`);
      await p.close();
    }
    await ctx.close();
  }
  // tutti i collegamenti interni rispondono e le ancore esistono
  const ctx = await b.newContext(); const p = await ctx.newPage();
  for (const l of [...seen].sort()) {
    const [path, frag] = l.split('#');
    const resp = await p.goto(BASE + (/^caso-\d$/.test(frag || '') ? l : path));
    let ok = !resp || resp.status() === 200; // senza risposta: stessa pagina, cambia solo l'ancora
    if (ok && frag && !/^caso-\d$/.test(frag)) ok = await p.evaluate(id => !!document.getElementById(id), frag);
    if (ok && /^caso-\d$/.test(frag)) { await p.waitForTimeout(150); ok = await p.evaluate(() => !document.querySelector('.case-msg').hidden); }
    if (!ok) { bad++; console.log('NO  collegamento', l); }
  }
  console.log('collegamenti interni controllati:', seen.size);
  for (const old of ['tassi', 'verifica', 'registro', 'privacy', 'note-legali', 'termini']) {
    await p.goto(BASE + '/#' + old); await p.waitForTimeout(200);
    console.log('vecchio indirizzo /#' + old.padEnd(12), '->', p.url().replace(BASE, ''));
  }
  const resp = await p.goto(BASE + '/sitemap.xml'); const sm = await resp.text();
  for (const m of sm.matchAll(/<loc>https:\/\/calcolaprecetti\.it([^<]*)<\/loc>/g)) {
    const r2 = await p.goto(BASE + m[1]); if (r2.status() !== 200) { bad++; console.log('NO  sitemap', m[1]); }
  }
  console.log('sitemap:', [...sm.matchAll(/<loc>/g)].length, 'indirizzi, tutti raggiungibili');
  await b.close(); console.log(bad ? bad + ' problemi' : 'nessun problema');
})();
