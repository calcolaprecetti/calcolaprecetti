// Copia statica dei contenuti che le pagine scrivono con JavaScript (tabelle dei tassi, casi di verifica, registro,
// privacy, note legali, date nel piè di pagina): i crawler che non eseguono JavaScript, come quasi tutti quelli AI,
// li leggono così come li vede chi visita il sito. Al caricamento lo script li riscrive uguali (innerHTML).
// Uso: node gen/prerender.js  (lo lancia finalize.py, dopo patch_site.py)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const SITE = path.resolve(__dirname, '..', '..'); // radice del repository, cioè il sito pubblicato
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2', '.ico': 'image/x-icon', '.xml': 'application/xml' };
// elementi riempiti dagli script; l'indirizzo email del riquadro dei contatti resta fuori di proposito
// items: la prima voce di capitale della home, così la pagina non si sposta quando lo script la crea
const IDS = ['items', 'privacyBody', 'legalBody', 'tabLegali', 'tabMora', 'tabPrecetto', 'casiBody', 'registroBody', 'ratesTable',
  'nowLegal', 'nowLegalSrc', 'nowLegalYear', 'nowMora', 'nowMoraSem', 'nowMoraSrc', 'nowRate', 'nowSem', 'nowSrc', 'nowAgri'];
const CLASSES = ['js-updated', 'js-titolare', 'js-accessori'];

function pages(dir, out = []) {
  for (const f of fs.readdirSync(dir)) {
    if (f.startsWith('.') || f.startsWith('_')) continue; // né .git né _sorgenti
    const p = path.join(dir, f);
    if (fs.statSync(p).isDirectory()) pages(p, out);
    else if (f.endsWith('.html') && !/^google[0-9a-f]+\.html$/.test(f)) out.push(p);
  }
  return out;
}

// sostituisce il contenuto dell'elemento che inizia in «start», contando i tag uguali annidati
function replaceInner(html, start, inner) {
  const open = /^<([a-z0-9]+)\b[^>]*>/i.exec(html.slice(start));
  if (!open) throw new Error('tag non riconosciuto');
  const tag = open[1].toLowerCase(), from = start + open[0].length;
  const re = new RegExp('<(/?)' + tag + '\\b[^>]*>', 'gi');
  re.lastIndex = from;
  let depth = 1, m;
  while ((m = re.exec(html))) {
    depth += m[1] ? -1 : 1;
    if (!depth) return html.slice(0, from) + inner + html.slice(m.index);
  }
  throw new Error('chiusura di <' + tag + '> non trovata');
}

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  await ctx.route('**/*', route => {
    const u = new URL(route.request().url());
    if (u.hostname !== 'calcolaprecetti.it') return route.abort(); // statistiche e siti esterni: niente
    let p = decodeURIComponent(u.pathname);
    if (p.endsWith('/')) p += 'index.html';
    const f = path.join(SITE, p);
    if (!fs.existsSync(f)) return route.fulfill({ status: 404, body: '' });
    route.fulfill({ status: 200, contentType: TYPES[path.extname(f)] || 'application/octet-stream', body: fs.readFileSync(f) });
  });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  let total = 0;
  for (const file of pages(SITE)) {
    const rel = path.relative(SITE, file);
    const url = 'https://calcolaprecetti.it/' + rel.replace(/(^|\/)index\.html$/, '$1');
    await page.goto(url, { waitUntil: 'load' });
    await page.waitForTimeout(150);
    const got = await page.evaluate(([ids, classes]) => ({
      ids: ids.filter(id => document.getElementById(id)).map(id => [id, document.getElementById(id).innerHTML]),
      classes: classes.map(c => [c, [...document.getElementsByClassName(c)].map(e => e.innerHTML)])
    }), [IDS, CLASSES]);
    let html = fs.readFileSync(file, 'utf8'), n = 0;
    for (const [id, inner] of got.ids) {
      const re = new RegExp('<[a-z0-9]+\\b[^>]*\\bid="' + id + '"[^>]*>', 'gi');
      const hits = [...html.matchAll(re)];
      if (hits.length !== 1) throw new Error(rel + ': #' + id + ' trovato ' + hits.length + ' volte');
      if (!inner.trim()) continue;
      html = replaceInner(html, hits[0].index, inner); n++;
    }
    for (const [cls, inners] of got.classes) {
      const re = new RegExp('<[a-z0-9]+\\b[^>]*\\bclass="' + cls + '"[^>]*>', 'gi');
      const hits = [...html.matchAll(re)];
      if (hits.length !== inners.length) throw new Error(rel + ': .' + cls + ' ' + hits.length + ' nel file, ' + inners.length + ' nella pagina');
      for (let i = hits.length - 1; i >= 0; i--) { html = replaceInner(html, hits[i].index, inners[i]); n++; } // dal fondo: gli indici restano validi
    }
    fs.writeFileSync(file, html);
    total += n;
    console.log('  ' + rel.padEnd(32) + n + ' parti');
  }
  await browser.close();
  if (errors.length) throw new Error('errori negli script: ' + errors.join(' | '));
  console.log('  copia statica: ' + total + ' parti');
})().catch(e => { console.error('ERRORE: ' + e.message); process.exit(1); });
