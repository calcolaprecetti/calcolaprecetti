// Controllo dell'anteprima nel browser: errori, larghezza, collegamenti, calcoli, casi di verifica, vecchi indirizzi.
// Uso: node check.js [cartella] [--shots]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const DIR = process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : path.join(require('os').tmpdir(), 'anteprima-calcolaprecetti');
const SHOTS = process.argv.includes('--shots');
const OUT = path.join(require('os').tmpdir(), 'schermate-calcolaprecetti');
const pages = fs.readdirSync(DIR).filter(f => f.endsWith('.html')).sort();
const views = [['desktop', 1280, 900], ['telefono', 390, 844], ['piccolo', 360, 740]];
const url = (f, h) => 'file://' + path.join(DIR, f) + (h || '');

(async () => {
  if (SHOTS) fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  let bad = 0;
  for (const [vname, w, h] of (process.argv.includes('--solo-calcoli') ? [] : views)) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, locale: 'it-IT' });
    for (const f of pages) {
      const page = await ctx.newPage();
      const errs = [];
      page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
      page.on('pageerror', e => errs.push('pageerror: ' + e.message));
      page.on('requestfailed', r => errs.push('richiesta fallita: ' + r.url().slice(0, 80)));
      await page.goto(url(f));
      await page.waitForTimeout(250);
      const info = await page.evaluate(() => {
        const de = document.documentElement;
        const wide = [];
        if (de.scrollWidth > de.clientWidth + 1) {
          document.querySelectorAll('body *').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.right > de.clientWidth + 1 && r.width > 0 && !el.closest('.scroll')) wide.push(el.tagName + '.' + el.className + ' ' + Math.round(r.right));
          });
        }
        const n = document.querySelector('.tools .wrap');
        return { sw: de.scrollWidth, cw: de.clientWidth, wide: wide.slice(0, 6),
                 links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')),
                 nav: [...document.querySelectorAll('.tools a')].map(a => a.innerText.trim() + (a.getAttribute('aria-current') ? '*' : '')).join(' | '),
                 navFits: n.scrollWidth <= n.clientWidth + 1,
                 ids: (() => { const seen = {}, dup = []; document.querySelectorAll('[id]').forEach(e => { if (seen[e.id]) dup.push(e.id); seen[e.id] = 1; }); return dup; })() };
      });
      const broken = [];
      for (const href of info.links) {
        if (/^(https?:|mailto:)/.test(href)) continue;
        const [file, frag] = href.split('#');
        const target = file || f;
        if (!fs.existsSync(path.join(DIR, target))) { broken.push(href); continue; }
        if (frag && !/^caso-\d$/.test(frag)) {
          const html = fs.readFileSync(path.join(DIR, target), 'utf8');
          if (!new RegExp('id="' + frag + '"').test(html)) broken.push(href + ' (ancora mancante)');
        }
      }
      const overflow = info.sw > info.cw + 1;
      const ok = !errs.length && !overflow && !broken.length && !info.ids.length && info.navFits;
      if (!ok) bad++;
      console.log(`${ok ? 'ok ' : 'NO '} ${vname.padEnd(8)} ${f.padEnd(26)} ${info.sw}/${info.cw}  ${vname === 'desktop' || vname === 'piccolo' ? info.nav : ''}` +
        (errs.length ? '\n     errori: ' + errs.join(' | ') : '') + (overflow ? '\n     troppo largo: ' + info.wide.join(' ; ') : '') +
        (info.navFits ? '' : '\n     la barra non entra') +
        (broken.length ? '\n     collegamenti: ' + broken.join(', ') : '') + (info.ids.length ? '\n     id doppi: ' + info.ids.join(', ') : ''));
      if (SHOTS && vname !== 'piccolo') await page.screenshot({ path: path.join(OUT, vname + '-' + f.replace('.html', '.png')), fullPage: true });
      await page.close();
    }
    await ctx.close();
  }

  // ---------------- calcoli e casi di verifica
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'it-IT' });
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  const txt = async sel => (await p.locator(sel).innerText()).replace(/\s+/g, ' ').trim();

  await p.goto(url('index.html'));
  await p.click('#btnExample');
  await p.waitForTimeout(150);
  console.log('\nHome, esempio:', await txt('#table tr.total'), '(atteso € 2.256,33)');
  console.log('  rimandi:', (await p.locator('.after').allInnerTexts()).join(' | '), '| riquadro termini presente:', await p.locator('#tNotifica').count());

  await p.goto(url('tassi.html'));
  const cases = await p.$$eval('#casiBody a', as => as.map(a => [a.getAttribute('href'), a.innerText]));
  console.log('\nTassi: casi', cases.length, '| righe legali', await p.locator('#tabLegali tbody tr').count(), '| moratori', await p.locator('#tabMora tbody tr').count(),
    '| compenso', await p.locator('#tabPrecetto tbody tr').count(), '| registro', await p.locator('#registroBody li').count());
  console.log('  in vigore:', await txt('.answer'));
  console.log('  prima riga moratori:', await txt('#tabMora tbody tr:first-child'));
  console.log('  ultima riga moratori:', await txt('#tabMora tbody tr:last-child'));
  console.log('  compenso:', await txt('#tabPrecetto tbody tr:first-child'), '|', await txt('.js-accessori'));
  for (const [href, label] of cases) {
    await p.goto(url(href.split('#')[0], '#' + href.split('#')[1]));
    await p.waitForTimeout(200);
    if (href.startsWith('index')) {
      console.log(`  ${href.padEnd(28)} ${label} -> ${await txt('#table tr.total')} | ${await txt('#caseMsg')} | indirizzo: ${p.url().split('/').pop()}`);
      await p.fill('#endDate', '2026-07-01');
      console.log('     dopo una modifica il caso sparisce:', await p.locator('#caseMsg').isHidden());
    } else {
      console.log(`  ${href.padEnd(28)} ${label} -> ${await txt('#tOut')} | ${await txt('#tCase')}`);
    }
  }

  for (const old of ['tassi', 'verifica', 'registro', 'privacy', 'note-legali', 'termini']) {
    await p.goto(url('index.html', '#' + old));
    await p.waitForTimeout(250);
    console.log('vecchio indirizzo #' + old.padEnd(12), '->', p.url().split('/').pop());
  }

  await p.goto(url('termini-precetto.html'));
  for (const d of ['2026-10-02', '2026-10-01']) {
    await p.fill('#tNotifica', d);
    console.log('\nTermini ' + d + ':', await txt('#tOut'));
  }
  await p.check('#tBis');
  await p.fill('#tBisFrom', '2026-10-20');
  console.log('  con istanza senza esito:', await txt('#tOut'));

  await p.goto(url('privacy.html'));
  console.log('\nPrivacy:', (await p.locator('#privacyBody h2').allInnerTexts()).join(' / '));
  await p.goto(url('note-legali.html'));
  console.log('Note legali:', (await txt('#legalBody')).slice(0, 160) + '…');

  if (fs.existsSync(path.join(DIR, 'guide.html'))) {
  await p.goto(url('guide.html'));
  console.log('\nGuide:', await txt('#atto'), '|', (await p.locator('.g-atto strong').allInnerTexts()).join(', '), '|', await txt('#clienti'), '|',
    (await p.locator('.g-card h3').allInnerTexts()).join(', '));
  await p.goto(url('fattura-non-pagata.html'));
  await p.click('#copyLink');
  await p.waitForTimeout(200);
  console.log('Guida 1, copia il collegamento:', await txt('#copyMsg'), '| condividi visibile:', await p.locator('#shareLink').isVisible());
  console.log('  strumento:', await txt('#qOutMora'));
  await p.goto(url('decreto-ingiuntivo.html'));
  await p.fill('#qValore', '8000');
  console.log('Guida 2, 8.000:', await txt('#qOutCosti'));
  await p.goto(url('precetto-notificato.html'));
  await p.fill('#qNotifica', '2026-10-02');
  console.log('Guida 3, 02.10.2026:', await txt('#qOutTermini'));
  }
  await p.goto(url('interessi-moratori.html'));
  await p.fill('[data-s=cap]', '1394,25'); await p.fill('[data-s=from]', '2025-09-25'); await p.fill('[data-s=to]', '2026-09-21');
  console.log('Moratori, caso 2:', await txt('#miniTotals'), '| riquadro guide:', (await p.locator('.send h2').count()) ? await txt('.send h2') : 'nessuno');
  if (errs.length) { bad++; console.log('errori:', errs.join(' | ')); }
  await browser.close();
  console.log(bad ? '\n' + bad + ' problemi' : '\nnessun problema nelle pagine');
})();
