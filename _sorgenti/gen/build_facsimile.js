// Disegna il facsimile del parere (gen/facsimile.html) e lo salva come immagine per la pagina della valutazione:
// assets/facsimile-parere.webp, a doppia risoluzione per gli schermi nitidi. Uso: node gen/build_facsimile.js
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const OUT = path.resolve(__dirname, '..', '..', 'assets', 'facsimile-parere.webp');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 700, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'facsimile.html'));
  await p.evaluate(() => document.fonts.ready);
  const fonts = await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').length);
  if (fonts < 3) throw new Error('caratteri non caricati: ' + fonts);
  const png = path.join(__dirname, '_facsimile.png');
  await (await p.$('#sheet')).screenshot({ path: png });
  await b.close();
  execFileSync('python3', ['-c', [
    'import sys', 'from PIL import Image',
    'im = Image.open(sys.argv[1]).convert("RGB")',
    'im.save(sys.argv[2], "WEBP", quality=80, method=6)',
    'print("facsimile-parere.webp", im.size[0], "x", im.size[1])'].join('\n'), png, OUT], { stdio: 'inherit' });
  fs.unlinkSync(png);
  console.log(Math.round(fs.statSync(OUT).size / 1024) + ' KB');
})();
