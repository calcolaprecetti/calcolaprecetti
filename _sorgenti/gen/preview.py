#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Costruisce l'anteprima delle pagine di calcolaprecetti.it: ogni pagina in un file autosufficiente (stile, caratteri,
script, logo e immagini dentro il file), tutte nella stessa cartella, con i collegamenti riscritti da un file all'altro.
Serve per vedere le pagine prima di pubblicarle, anche fuori dal sito.

Uso: python3 _sorgenti/gen/preview.py [cartella] [--frammento] [--titolo=...]
- cartella: dove scrivere l'anteprima (di norma una cartella temporanea, fuori dal repository);
- --frammento: la pagina principale senza <html>, <head> e <body>, per chi la pubblica aggiungendoli."""
import base64
import io
import os
import re
import sys
import tempfile

GEN = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(GEN))  # radice del repository, cioè il sito pubblicato
OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else os.path.join(tempfile.gettempdir(), 'anteprima-calcolaprecetti')
FRAGMENT = '--frammento' in sys.argv
MAIN_TITLE = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--titolo=')), 'Anteprima di calcolaprecetti.it')
BASE = 'https://calcolaprecetti.it'

PAGES = {  # indirizzo del sito -> (file sorgente, file dell'anteprima)
    '/': ('index.html', 'index.html'),
    '/termini-precetto/': ('termini-precetto/index.html', 'termini-precetto.html'),
    '/interessi-moratori/': ('interessi-moratori/index.html', 'interessi-moratori.html'),
    '/guide/': ('guide/index.html', 'guide.html'),
    '/guide/fattura-non-pagata/': ('guide/fattura-non-pagata/index.html', 'fattura-non-pagata.html'),
    '/guide/decreto-ingiuntivo-tempi-costi/': ('guide/decreto-ingiuntivo-tempi-costi/index.html', 'decreto-ingiuntivo.html'),
    '/guide/precetto-notificato/': ('guide/precetto-notificato/index.html', 'precetto-notificato.html'),
    '/tassi/': ('tassi/index.html', 'tassi.html'),
    '/privacy/': ('privacy/index.html', 'privacy.html'),
    '/note-legali/': ('note-legali/index.html', 'note-legali.html'),
    '/chi-sono/': ('chi-sono/index.html', 'chi-sono.html'),
    '/newsletter/': ('newsletter/index.html', 'newsletter.html'),
    '/valutazione-credito/': ('valutazione-credito/index.html', 'valutazione-credito.html'),
    '/condizioni-parere/': ('condizioni-parere/index.html', 'condizioni-parere.html'),
    '/valutazione-credito/grazie/': ('valutazione-credito/grazie/index.html', 'valutazione-grazie.html'),
    '/recupero-crediti/': ('recupero-crediti/index.html', 'recupero-crediti.html'),
    '/404.html': ('404.html', '404.html'),
}
KNOWN = set(PAGES)  # tutte le pagine previste, anche quelle spente
PAGES = {u: v for u, v in PAGES.items() if os.path.exists(os.path.join(SITE, v[0]))}  # solo quelle che esistono


def rd(p, mode='r'):
    full = os.path.join(SITE, p)
    return open(full, 'rb').read() if 'b' in mode else io.open(full, encoding='utf-8').read()


def b64(p, mime):
    return 'data:%s;base64,%s' % (mime, base64.b64encode(rd(p, 'rb')).decode('ascii'))


def target(path, frag, here):
    """Da indirizzo del sito a file dell'anteprima."""
    if path not in PAGES and path in KNOWN:  # pagina di una funzione spenta (es. testo condizionale negli script)
        return '#'
    assert path in PAGES, 'collegamento senza pagina: %s (in %s)' % (path, here)
    return PAGES[path][1] + (frag or '')


os.makedirs(OUT, exist_ok=True)
css = rd('assets/style.css')
css = re.sub(r'url\("/fonts/([^"]+\.woff2)"\)', lambda m: 'url("%s")' % b64('fonts/' + m.group(1), 'font/woff2'), css)
assert '/fonts/' not in css
logo = b64('logo.svg', 'image/svg+xml')
for url, (src, dst) in PAGES.items():
    h = rd(src)
    CSS_LINK = r'<link rel="stylesheet" href="/assets/style\.css(?:\?v=[0-9a-f]+)?">'  # con o senza numero di versione
    assert len(re.findall(CSS_LINK, h)) == 1
    h = re.sub(CSS_LINK, lambda m: '<style>\n' + css + '\n</style>', h)

    def script(m):
        code = rd('assets/' + m.group(1))
        assert '</script' not in code.lower(), m.group(1)
        return '<script>\n' + code + '\n</script>'
    h = re.sub(r'<script src="/assets/([a-z]+\.js)(?:\?v=[0-9a-f]+)?" defer></script>', script, h)
    h = h.replace('src="/logo.svg"', 'src="%s"' % logo)
    h = re.sub(r'src="/assets/([a-z0-9-]+\.(jpe?g|png|webp))"', lambda m: 'src="%s"' % b64('assets/' + m.group(1),
               'image/' + ('jpeg' if m.group(2).startswith('jp') else m.group(2))), h)
    h = re.sub(r'<link rel="(?:icon|apple-touch-icon)"[^>]*>\n', '', h)
    h = re.sub(r'<link rel="preload" href="/fonts/[^"]+" as="font"[^>]*>\n', '', h)  # i caratteri sono già dentro lo stile
    h = h.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">')

    # collegamenti, solo nel corpo della pagina (non l'indirizzo canonico nell'intestazione)
    cut = h.index('<body')
    head_part, body = h[:cut], h[cut:]

    def link(m):
        path, frag = m.group(1), m.group(2) or ''
        if path == url:  # stessa pagina
            return 'href="%s"' % (frag or dst)
        return 'href="%s"' % target(path, frag, src)
    body = re.sub(r'href="(/[^"#]*)(#[^"]*)?"', link, body)
    body = re.sub(r'href="%s(/[^"#]*)(#[^"]*)?"' % re.escape(BASE), lambda m: 'href="%s"' % target(m.group(1), m.group(2), src), body)
    body = re.sub(r'(data-url-[a-z]+=)"(/[^"#]*)"', lambda m: '%s"%s"' % (m.group(1), target(m.group(2), '', src)), body)

    def moved(m):
        return re.sub(r"'(/[^'#]*)(#[^']*)?'", lambda n: "'%s'" % target(n.group(1), n.group(2), src), m.group(0))
    body = re.sub(r'var MOVED = \{[^}]*\};', moved, body)
    h = head_part + body

    # titolo
    t = re.search(r'<title>(.*?)</title>', h).group(1)
    h = h.replace('<title>%s</title>' % t, '<title>%s</title>' % (MAIN_TITLE if dst == 'index.html' else 'Anteprima – ' + t), 1)

    left = re.findall(r'(?:href|src)="/[^"]*"', h)
    assert not left, left[:5]

    if dst == 'index.html' and FRAGMENT:
        # pagina principale dell'anteprima: solo titolo, stile e contenuto, senza l'involucro del documento
        style = re.search(r'<style>.*?</style>', h, re.S).group(0)
        title = re.search(r'<title>.*?</title>', h).group(0)
        bm = re.search(r'<body([^>]*)>(.*)</body>', h, re.S)
        content = bm.group(2).strip()
        cls = re.search(r'class="([^"]+)"', bm.group(1))
        if cls:  # la classe del body (es. «home») passa a un contenitore, perché lo stile la usa
            content = '<div class="%s">\n%s\n</div>' % (cls.group(1), content)
        h = title + '\n' + style + '\n' + content + '\n'
        assert not re.search(r'<(?:html|head|body)[\s>]|<!doctype', h, re.I)
    io.open(os.path.join(OUT, dst), 'w', encoding='utf-8', newline='\n').write(h)
    print('%-34s %7d byte' % (dst, len(h.encode('utf-8'))))
print('anteprima in ' + OUT)
