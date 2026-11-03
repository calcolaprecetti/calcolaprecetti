// Prova del contatore senza cookie: il sito vero è servito come se fosse su https://calcolaprecetti.it,
// le richieste ai servizi di statistica vengono intercettate e controllate (niente dati dei calcoli, niente cookie).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const SITE = path.resolve(__dirname, '..', '..'); // radice del repository, cioè il sito pubblicato
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.ico': 'image/x-icon', '.xml': 'application/xml' };

async function run(name, { servizio = 'plausible', codice = '', init = '' } = {}) {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ acceptDownloads: true });
  await ctx.addInitScript('Object.defineProperty(navigator, "webdriver", { get: () => false });' + init);
  const hits = [];
  await ctx.route('https://calcolaprecetti.it/**', route => {
    let p = new URL(route.request().url()).pathname;
    if (p.endsWith('/')) p += 'index.html';
    const f = path.join(SITE, p);
    if (!fs.existsSync(f)) return route.fulfill({ status: 404, body: 'non trovato' });
    let body = fs.readFileSync(f);
    if (p === '/assets/core.js') body = body.toString().replace(/statistiche: \{ servizio: '[a-z]*', codice: '[^']*' \}/,
      `statistiche: { servizio: '${servizio}', codice: '${codice}' }`);
    route.fulfill({ status: 200, contentType: TYPES[path.extname(f)] || 'application/octet-stream', body });
  });
  await ctx.route('https://plausible.io/api/event', route => {
    const r = route.request();
    hits.push({ to: 'plausible', ct: r.headers()['content-type'], cookie: r.headers()['cookie'] || '', data: JSON.parse(r.postData()) });
    route.fulfill({ status: 202, headers: { 'access-control-allow-origin': '*' }, body: '{}' });
  });
  await ctx.route('https://gateway.umami.is/api/send', route => {
    const r = route.request();
    if (r.method() === 'OPTIONS') return route.fulfill({ status: 204, headers: { 'access-control-allow-origin': '*', 'access-control-allow-headers': 'content-type' } });
    hits.push({ to: 'umami', ct: r.headers()['content-type'], cookie: r.headers()['cookie'] || '', data: JSON.parse(r.postData()) });
    route.fulfill({ status: 200, headers: { 'access-control-allow-origin': '*' }, contentType: 'application/json', body: '{}' });
  });
  await ctx.route(/goatcounter\.com/, route => {
    const u = new URL(route.request().url());
    hits.push({ to: u.hostname, cookie: route.request().headers()['cookie'] || '', data: Object.fromEntries(u.searchParams) });
    route.fulfill({ status: 200, contentType: 'image/gif', body: Buffer.from('R0lGODlhAQABAAAAACw=', 'base64') });
  });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));

  // home arrivando da un motore di ricerca: esempio, copia, file Word, stampa (finta)
  await page.goto('https://calcolaprecetti.it/', { referer: 'https://www.google.com/search?q=calcolo+precetto' });
  await page.evaluate(() => { window.print = () => {}; });
  await page.click('#btnExample');
  await page.waitForTimeout(500);
  await page.click('#btnCopy');
  const dl = page.waitForEvent('download');
  await page.click('#btnDocx');
  await dl;
  await page.click('#btnPrint');
  await page.fill('#endDate', '2026-07-01'); // altro calcolo nella stessa pagina: non si conta di nuovo
  await page.waitForTimeout(300);
  // pagina interna: nessuna provenienza
  await page.click('.foot a[href="/tassi/"]');
  await page.waitForLoadState('load');
  // termini: due date di seguito, un solo calcolo; calendario
  await page.goto('https://calcolaprecetti.it/termini-precetto/');
  await page.fill('#tNotifica', '2026-10-01');
  await page.fill('#tNotifica', '2026-10-02');
  await page.click('#tIcs');
  // moratori
  await page.goto('https://calcolaprecetti.it/interessi-moratori/');
  await page.fill('[data-s=cap]', '1394,25'); await page.fill('[data-s=from]', '2025-09-25'); await page.fill('[data-s=to]', '2026-09-21');
  // valutazione del credito: clic sul pulsante del questionario (in anteprima porta a #richiedi)
  await page.goto('https://calcolaprecetti.it/valutazione-credito/');
  await page.click('#richiedi .btn');
  await page.waitForTimeout(400);
  const cookies = await ctx.cookies();
  const storage = await page.evaluate(() => localStorage.length + sessionStorage.length);
  await browser.close();

  const label = h => h.to === 'plausible' ? (h.data.name === 'pageview' ? 'pagina ' + new URL(h.data.url).pathname : 'azione ' + h.data.name)
    : h.to === 'umami' ? (h.data.payload.name ? 'azione ' + h.data.payload.name : 'pagina ' + new URL(h.data.payload.url).pathname)
    : (h.data.e ? 'azione ' + h.data.p : 'pagina ' + h.data.p);
  console.log(`\n== ${name}: ${hits.length} richieste`);
  hits.forEach(h => console.log('  ' + label(h).padEnd(34) + JSON.stringify(h.data)));
  const all = JSON.stringify(hits);
  const leaks = ['2.256', '2256', '1394', '1.394', '2026-10-0', '2026-07-01', 'q=calcolo', 'Rossi'].filter(x => all.includes(x));
  console.log('  dati dei calcoli nelle richieste:', leaks.length ? 'SÌ ' + leaks.join(', ') : 'nessuno',
    '| cookie inviati:', hits.some(h => h.cookie) ? 'SÌ' : 'nessuno', '| cookie nel browser:', cookies.length, '| memoria del browser:', storage,
    '| errori:', errs.length ? errs.join(' | ') : 'nessuno');
  return hits;
}

(async () => {
  const a = await run('Plausible');
  const b = await run('GoatCounter', { servizio: 'goatcounter', codice: 'calcolaprecetti' });
  const u = await run('Umami', { servizio: 'umami', codice: 'bb2d5a3e-273f-4655-af5b-b3fdc692f6df' });
  const c = await run('Browser con «Global Privacy Control»', { init: 'Object.defineProperty(navigator, "globalPrivacyControl", { get: () => true });' });
  const d = await run('Statistiche spente', { servizio: '' });
  const exp = ['pagina /', 'azione esempio', 'azione calcolo-somme', 'azione copia-word', 'azione scarica-docx', 'azione stampa', 'pagina /tassi/',
    'pagina /termini-precetto/', 'azione calcolo-termini', 'azione calendario', 'pagina /interessi-moratori/', 'azione calcolo-moratori',
    'pagina /valutazione-credito/', 'azione inizia-valutazione'];
  const got = hits => hits.map(h => h.to === 'plausible' ? (h.data.name === 'pageview' ? 'pagina ' + new URL(h.data.url).pathname : 'azione ' + h.data.name)
    : h.to === 'umami' ? (h.data.payload.name ? 'azione ' + h.data.payload.name : 'pagina ' + new URL(h.data.payload.url).pathname)
    : (h.data.e ? 'azione ' + h.data.p : 'pagina ' + h.data.p)).sort().join(',');
  const ok = got(a) === exp.slice().sort().join(',') && got(b) === exp.slice().sort().join(',') && got(u) === exp.slice().sort().join(',') &&
    u.every(h => h.data.type === 'event' && h.data.payload.website === 'bb2d5a3e-273f-4655-af5b-b3fdc692f6df' && !/[?#]/.test(h.data.payload.url)) && !c.length && !d.length;
  console.log('\n' + (ok ? 'tutto come previsto' : 'ATTENZIONE: conteggi diversi dal previsto'));
})();
