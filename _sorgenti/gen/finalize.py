#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ultimo passaggio della generazione del sito (lo lancia patch_site.py alla fine).

1. Accessibilità: collegamento «Salta al contenuto», titolo della pagina dentro <main>, tabelle che scorrono
   raggiungibili da tastiera (tabindex, role=region, nome), barra del totale su telefono come regione con nome.
2. Copia statica dei contenuti scritti da JavaScript (prerender.js), per i crawler che non lo eseguono.
3. Sitemap con la data di ultima modifica di ogni pagina: cambia solo quando cambia il contenuto (gen/lastmod.json).
4. robots.txt: motori di ricerca e assistenti AI che cercano e citano le fonti ammessi; crawler che raccolgono
   testi per addestrare modelli di intelligenza artificiale esclusi.
"""
import datetime
import hashlib
import io
import json
import os
import re
import subprocess

# percorsi relativi: questo file sta in _sorgenti/gen; il sito pubblicato è la radice del repository
GEN = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(GEN))
BASE = 'https://calcolaprecetti.it'


def rd(p):
    return io.open(p, encoding='utf-8').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)


def html_files():
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if not d.startswith(('.', '_'))]  # né .git né _sorgenti
        for f in sorted(files):
            if f.endswith('.html') and not re.match(r'^google[0-9a-f]+\.html$', f):
                yield os.path.join(root, f)


# ---------------------------------------------------------------- 1. accessibilità
SCROLL = {  # tabelle che scorrono di lato: nome letto dai lettori di schermo
    'tabLegali': 'Tabella degli interessi legali',
    'tabMora': 'Tabella dei tassi moratori',
    'tabPrecetto': 'Tabella del compenso del precetto',
    'miniTable': 'Dettaglio del calcolo degli interessi moratori',
    'ratesTable': 'Tabella dei tassi moratori dal 2002',
}
print('accessibilità')
for f in html_files():
    rel = os.path.relpath(f, SITE)
    s = rd(f)
    if 'class="skip"' not in s:
        s, n = re.subn(r'(<body[^>]*>)', r'\1\n<a class="skip" href="#main">Salta al contenuto</a>', s, count=1)
        assert n == 1, rel + ': manca <body>'
    if '<main id="main"' not in s:  # il titolo (g-hero) entra nell'area principale
        hero = '<div class="wrap g-hero solo">'
        assert s.count(hero) == 1, rel + ': titolo della pagina non trovato'
        m = re.findall(r'<main class="(wrap [a-z]+)">', s)
        assert len(m) == 1 and s.count('</main>') == 1, rel + ': <main> non trovato'
        assert s.index(hero) < s.index('<main class='), rel + ': titolo dopo <main>'
        s = s.replace(hero, '<main id="main" tabindex="-1">\n' + hero, 1)
        s = s.replace('<main class="%s">' % m[0], '<div class="%s">' % m[0], 1)
        s = s.replace('</main>', '</div>\n</main>', 1)

    def scroll(mm):
        tid = mm.group(1)
        assert tid in SCROLL, rel + ': tabella scorrevole senza nome: ' + tid
        return '<div class="scroll" tabindex="0" role="region" aria-label="%s"><table%s' % (SCROLL[tid], mm.group(0)[len('<div class="scroll"><table'):])
    s = re.sub(r'<div class="scroll"><table class="[^"]*" id="([A-Za-z]+)"', scroll, s)
    assert '<div class="scroll">' not in s, rel + ': resta una tabella scorrevole senza nome'
    s = s.replace('<div class="mobilebar" id="mobilebar">', '<div class="mobilebar" id="mobilebar" role="region" aria-label="Totale del prospetto">')
    wr(f, s)
print('  salta al contenuto, titolo in <main>, tabelle scorrevoli e barra del totale')

# ---------------------------------------------------------------- 2. copia statica dei contenuti scritti da JavaScript
print('copia statica (prerender.js)')
subprocess.run(['node', os.path.join(GEN, 'prerender.js')], check=True)

# ---------------------------------------------------------------- 3. sitemap con la data di ultima modifica
oggi = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1))).date().isoformat()  # ora italiana (inverno)
try:
    from zoneinfo import ZoneInfo
    oggi = datetime.datetime.now(ZoneInfo('Europe/Rome')).date().isoformat()
except Exception:
    pass
STATE = os.path.join(GEN, 'lastmod.json')
stato = json.load(io.open(STATE, encoding='utf-8')) if os.path.exists(STATE) else {}
urls = re.findall(r'<loc>%s([^<]*)</loc>' % re.escape(BASE), rd(os.path.join(SITE, 'sitemap.xml')))
assert urls, 'sitemap vuota'
righe = []
for u in urls:
    s = rd(os.path.join(SITE, u.strip('/'), 'index.html') if u != '/' else os.path.join(SITE, 'index.html'))
    h = hashlib.sha256(re.sub(r'\?v=[0-9a-f]+', '', s).encode('utf-8')).hexdigest()[:16]  # senza i numeri di versione
    if stato.get(u, {}).get('impronta') != h:
        stato[u] = {'impronta': h, 'data': oggi}
    righe.append('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (BASE, u, stato[u]['data']))
wr(STATE, json.dumps(stato, indent=1, ensure_ascii=False) + '\n')
wr(os.path.join(SITE, 'sitemap.xml'), '<?xml version="1.0" encoding="UTF-8"?>\n'
   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(righe) + '</urlset>\n')
print('sitemap.xml: %d indirizzi con la data di ultima modifica' % len(righe))

# ---------------------------------------------------------------- 4. robots.txt
# Google-Extended resta ammesso per scelta: Google lo usa anche per le risposte dell'app Gemini, che così possono citare il sito.
ADDESTRAMENTO = [  # raccolgono testi per addestrare modelli di intelligenza artificiale
    'GPTBot',              # OpenAI
    'ClaudeBot',           # Anthropic
    'anthropic-ai',        # Anthropic, nome usato in passato
    'Applebot-Extended',   # Apple
    'CCBot',               # Common Crawl, archivio usato per addestrare molti modelli
    'meta-externalagent',  # Meta
    'Bytespider',          # ByteDance
    'cohere-training-data-crawler',  # Cohere
]
wr(os.path.join(SITE, 'robots.txt'),
   '# calcolaprecetti.it\n'
   '# Motori di ricerca e assistenti AI che cercano e citano le fonti (per esempio Googlebot, Bingbot,\n'
   '# OAI-SearchBot e ChatGPT-User, Claude-SearchBot e Claude-User, PerplexityBot): ammessi.\n'
   'User-agent: *\n'
   'Allow: /\n'
   '\n'
   '# Raccolta di testi per addestrare modelli di intelligenza artificiale: esclusa.\n'
   + ''.join('User-agent: %s\n' % b for b in ADDESTRAMENTO) +
   'Disallow: /\n'
   '\n'
   'Sitemap: %s/sitemap.xml\n' % BASE)
print('robots.txt: %d crawler di addestramento esclusi' % len(ADDESTRAMENTO))
