#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parti comuni a tutte le pagine di calcolaprecetti.it (barra, piè di pagina, intestazione, interruttori delle
sezioni) e modello delle pagine della sezione «Guide» (indice + tre guide).

I testi delle guide stanno in guide_testi.py: sono bozze da rivedere e restano fuori dal repository finché non
si pubblicano (istruzioni in _sorgenti/LEGGIMI.md). Le domande frequenti sono scritte una volta sola e
finiscono sia nella pagina sia nei dati strutturati, così restano identiche.
"""
import html
import json
import math
import os
import re

# percorsi relativi: questo file sta in _sorgenti/gen; il sito pubblicato è la radice del repository
GEN = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(GEN))
BASE = 'https://calcolaprecetti.it'
GUIDE_PUBBLICATE = '2026-11-10'  # prima pubblicazione delle guide (datePublished); la data di modifica la scrive finalize.py
COPY = ('<!-- calcolaprecetti.it - (c) 2026 il titolare indicato nelle Note legali '
        '(https://calcolaprecetti.it/note-legali/). Tutti i diritti riservati. Vietata la riproduzione, '
        'anche parziale, senza autorizzazione scritta. Licenza: file LICENSE. -->')

G1 = '/guide/fattura-non-pagata/'
G2 = '/guide/decreto-ingiuntivo-tempi-costi/'
G3 = '/guide/precetto-notificato/'


# --------------------------------------------------------------------------- parti comuni
GUIDE = True  # sezione «Guide» (False per toglierla: schede, piè di pagina, rimandi e pagine delle guide)
TABS = [  # parte «Per gli avvocati»: gli strumenti
    ('/', '<span><span class="tl">Somme del </span><span class="tm">precetto</span></span>', 'home'),
    ('/termini-precetto/', '<span><span class="tm">Termini</span><span class="tl"> del precetto</span></span>', 'termini'),
    ('/interessi-moratori/', '<span><span class="tl">Calcolo interessi </span><span class="tm">moratori</span></span>', 'mora'),
    ('/tassi/', '<span><span class="tm">Tassi</span><span class="tl"> e fonti</span></span>', 'tassi'),
] + ([('/guide/', 'Guide', 'guide')] if GUIDE else [])
TABS_CREDITORI = [  # parte «Per i creditori»: lo studio (valutazione e «Chi sono» si aggiungono più sotto)
    ('/recupero-crediti/', '<span><span class="tm">Recupero</span><span class="tl"> crediti</span></span>', 'recupero'),
]
CREDITORI = {'recupero', 'valutazione', 'chi', 'newsletter'}  # pagine della parte «Per i creditori»
AUD_A = ('<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false"><rect x="3" y="1.5" width="10" height="13" '
         'rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M5.5 4.5h5M5.5 8h1M9.5 8h1M5.5 11h1M9.5 11h1" '
         'stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>')  # calcolatrice
AUD_C = ('<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false"><circle cx="8" cy="8" r="6.3" fill="none" '
         'stroke="currentColor" stroke-width="1.4"/><path d="M10.3 5.5a2.9 2.9 0 1 0 0 5M4.9 7.2h4.2M4.9 8.8h4.2" fill="none" '
         'stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>')  # moneta con l'euro


def nav(current, actions=''):
    """Barra «Per gli avvocati | Per i creditori», intestazione e schede della parte in cui sta la pagina.
    current: home, termini, mora, tassi, guide (indice), guida (una guida) per gli avvocati; recupero, valutazione, chi
    per i creditori; altro (privacy, note legali, 404): nessuna delle due, con le schede degli strumenti."""
    lato = 'c' if current in CREDITORI else ('' if current == 'altro' else 'a')

    def parte(key, href, icon, label, conta):
        cur = ' aria-current="true"' if lato == key else ''
        return '    <a href="%s"%s data-conta="%s">%s<span>%s</span></a>' % (href, cur, conta, icon, label)

    def a(href, label, key):
        cur = ''
        if current == key:
            cur = ' aria-current="page"'
        elif key == 'guide' and current == 'guida':
            cur = ' aria-current="true"'
        return '    <a href="%s"%s>%s</a>' % (href, cur, label)
    return '\n'.join([
        '<nav class="aud" aria-label="Parti del sito">',
        '  <div class="wrap">',
        parte('a', '/', AUD_A, 'Per gli avvocati', 'vai-avvocati'),
        parte('c', '/recupero-crediti/', AUD_C, 'Per i creditori', 'vai-creditori'),
        '  </div>',
        '</nav>',
        '<header class="top">',
        '  <div class="wrap">',
        '    <a class="brand" href="/"><img src="/logo.svg" alt="" width="28" height="28" '
        'style="vertical-align:-7px;margin-right:8px">calcolaprecetti.it</a>',
    ] + (['    <div class="top-actions">', '      ' + actions, '    </div>'] if actions else []) + [
        '  </div>',
        '</header>',
        '<nav class="tools" aria-label="Sezioni del sito">',
        '  <div class="wrap">',
    ] + [a(h, l, k) for h, l, k in (TABS_CREDITORI if lato == 'c' else TABS)] + [
        '  </div>',
        '</nav>',
    ])


CONTACT_SITO = 'Hai trovato un errore o ti servirebbe una funzione in più? Scrivimi: ogni segnalazione aiuta a migliorare il sito.'
CONTACT_GUIDE = "Hai trovato un errore, o c'è un argomento che vorresti vedere spiegato? Scrivimi: ogni segnalazione aiuta a migliorare le guide."


def contact(text=CONTACT_SITO):
    return '''<section class="wrap contact" id="suggerimenti" aria-labelledby="contactTitle">
  <div class="contact-box">
    <div class="contact-text">
      <h2 id="contactTitle">Suggerimenti</h2>
      <p>%s</p>
      <p class="hint">Non inserire nei messaggi dati personali di clienti o di terzi.</p>
    </div>
    <div class="contact-actions">
      <a class="btn btn-secondary" id="mailBtn" href="#suggerimenti">Scrivimi un suggerimento</a>
      <span class="contact-mail" id="mailText"></span>
    </div>
  </div>
</section>''' % text


CONTACT = contact(CONTACT_GUIDE)

CHI_SONO = True  # variante «sito unico»: pagina «Chi sono» con i contatti dentro calcolaprecetti.it (False per toglierla)
if CHI_SONO:
    TABS_CREDITORI.append(('/chi-sono/', 'Chi sono', 'chi'))
BY = '<a href="/chi-sono/"><span class="js-titolare"></span></a>' if CHI_SONO else '<span class="js-titolare"></span>'
LINKEDIN = 'https://www.linkedin.com/company/calcolaprecetto-it/'
ICON_OUT = ('<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false"><path d="M9.5 2.5h4v4M13.5 2.5 7.5 8.5'
            'M11.5 9.5v3a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1v-7a1 1 0 0 1 1-1h3" fill="none" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')  # icona generica: «apre un altro sito»

# Newsletter (un consiglio sul recupero crediti ogni due settimane e gli avvisi sui tassi): pagina /newsletter/ e rimandi
# da home, tassi, interessi moratori, «Chi sono» e piè di pagina.
NEWSLETTER = False  # spenta: l'idea è stata accantonata (True per rimetterla)
# Collegamento al modulo di iscrizione creato in Brevo (Moduli > il modulo > Condividi > collegamento).
# Vuoto: al posto del collegamento compare un segnaposto, va bene solo per l'anteprima.
NEWSLETTER_URL = ''
if NEWSLETTER:  # scheda nella barra in alto, prima di «Chi sono»
    TABS_CREDITORI.insert(len(TABS_CREDITORI) - (1 if CHI_SONO else 0), ('/newsletter/', 'Newsletter', 'newsletter'))

# Valutazione del credito: parere scritto a pagamento, prestazione professionale dell'avvocato.
VALUTAZIONE = True
# Collegamento al questionario su Tally (con le caselle delle condizioni e il pagamento). Vuoto: segnaposto, solo anteprima.
VALUTAZIONE_URL = 'https://tally.so/r/gbjNRO'  # funziona quando il modulo è pubblicato su Tally
VALUTAZIONE_PREZZO = 22.00  # compenso fisso in euro, senza C.P.A. e IVA; None: segnaposto
VALUTAZIONE_REGIME = 'forfettario'  # 'forfettario' (niente IVA; bollo da 2 € sopra 77,47 €) o 'ordinario' (IVA 22%)
VALUTAZIONE_CONSEGNA = 'un giorno lavorativo'  # termine di consegna del parere, dal pagamento
PIVA = '04591770245'  # partita IVA del titolare: va in home page quando il sito offre prestazioni a pagamento
if VALUTAZIONE:
    TABS_CREDITORI.insert(len(TABS_CREDITORI) - (1 if CHI_SONO else 0),
                          ('/valutazione-credito/', '<span><span class="tm">Valutazione</span><span class="tl"> del credito</span></span>', 'valutazione'))

FOOTER = '''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-about">
        <a class="foot-brand" href="/"><img src="/logo.svg" alt="" width="24" height="24">calcolaprecetti.it</a>
        <p>Calcoli gratuiti per il precetto''' + (' e guide sul recupero crediti' if GUIDE else '') + '''. Nessun cookie: i dati che inserisci restano sul tuo dispositivo.</p>
        <a class="foot-social" href="''' + LINKEDIN + '''" target="_blank" rel="noopener noreferrer">''' + ICON_OUT + '''LinkedIn</a>
      </div>
      <nav class="foot-col" aria-label="Calcoli">
        <h2>Calcoli</h2>
        <a href="/">Somme del precetto</a>
        <a href="/termini-precetto/">Termini del precetto</a>
        <a href="/interessi-moratori/">Calcolo interessi moratori</a>
      </nav>
      <nav class="foot-col" aria-label="Servizi">
        <h2>Servizi</h2>
        <a href="/recupero-crediti/">Recupero crediti</a>
''' + ('        <a href="/valutazione-credito/">Valutazione del credito</a>\n        <a href="/condizioni-parere/">Condizioni del parere</a>\n'
       if VALUTAZIONE else '') + '''      </nav>
''' + ('''      <nav class="foot-col" aria-label="Guide">
        <h2>Guide</h2>
        <a href="/guide/#atto">Approfondimenti per l'atto</a>
        <a href="/guide/#clienti">Da mandare ai clienti</a>
      </nav>
''' if GUIDE else '') + '''      <nav class="foot-col" aria-label="Verifiche">
        <h2>Verifiche</h2>
        <a href="/tassi/">Tassi e fonti</a>
        <a href="/tassi/#verifica">Casi di verifica</a>
        <a href="/tassi/#registro">Registro aggiornamenti</a>
      </nav>
      <nav class="foot-col" aria-label="Informazioni">
        <h2>Informazioni</h2>
''' + ('        <a href="/chi-sono/">Chi sono</a>\n' if CHI_SONO else '') + ('        <a href="/newsletter/">Newsletter</a>\n' if NEWSLETTER else '') + '''        <a href="/privacy/">Privacy</a>
        <a href="/note-legali/">Note legali</a>
        <a href="#suggerimenti">Suggerimenti</a>
      </nav>
    </div>
    <p class="foot-bottom">© 2026 calcolaprecetti.it · A cura di ''' + BY + (' · P.IVA ' + PIVA if VALUTAZIONE else '') + ''' · Tutti i diritti riservati · Tassi aggiornati a <span class="js-updated"></span> · Strumento di supporto: verifica sempre gli importi prima di inserirli in un atto.</p>
  </div>
</footer>'''


def head(title, desc, path, og_desc, jsonld, og_type='article', base=BASE, site_name='calcolaprecetti.it', image=True, copy=COPY):
    url = base + path
    e = lambda s: html.escape(s, quote=True)
    lines = [
        '<!doctype html>', copy, '<html lang="it">', '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>%s</title>' % e(title),
        '<link rel="canonical" href="%s">' % url,
        '<meta name="description" content="%s">' % e(desc),
        '<meta property="og:title" content="%s">' % e(title),
        '<meta property="og:url" content="%s">' % url,
    ] + ([
        '<meta property="og:image" content="%s/og-image.png">' % BASE,
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="calcolaprecetti.it – Il conteggio del precetto, pronto per Word">',
    ] if image else []) + [
        '<meta property="og:site_name" content="%s">' % e(site_name),
        '<meta property="og:locale" content="it_IT">',
        '<meta name="twitter:card" content="%s">' % ('summary_large_image' if image else 'summary'),
        '<meta property="og:description" content="%s">' % e(og_desc),
        '<meta property="og:type" content="%s">' % og_type,
    ]
    if og_type == 'article':
        lines.append('<meta property="article:modified_time" content="__AGGIORNATA__">')  # la data la scrive finalize.py
    lines += [
        '<meta name="theme-color" content="#1E3F8C">',
    ] + ([
        '<link rel="icon" href="/favicon-192.png" sizes="192x192" type="image/png">',
        '<link rel="icon" href="/favicon.ico" sizes="32x32">',
        '<link rel="icon" href="/icon.svg" type="image/svg+xml">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
    ] if image else []) + [
        '<link rel="stylesheet" href="/assets/style.css">',
        '<script type="application/ld+json">%s</script>' % json.dumps(jsonld, ensure_ascii=False),
        '</head>',
    ]
    return '\n'.join(lines)


def tail(*scripts, noscript='Per usare i calcoli di questa pagina attiva JavaScript nel browser.'):
    """Script in fondo alla pagina; noscript vuoto se la pagina ha già il suo avviso."""
    return '\n'.join([''] + (['<noscript><p style="padding:16px">%s</p></noscript>' % noscript] if noscript else []) +
                     ['<script src="/assets/core.js" defer></script>'] +
                     ['<script src="/assets/%s" defer></script>' % x for x in scripts] + ['</body>', '</html>', ''])


TAIL = tail('guide.js')

ORG = {"@type": "Organization", "name": "calcolaprecetti.it", "url": BASE + "/"}


def plain(s):
    """Testo senza marcatori, per i dati strutturati."""
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(re.sub(r'\s+', ' ', s)).strip()


def faq_html(faqs):
    out = ['<section class="g-faq" id="domande">', '<h2>Domande frequenti</h2>']
    for q, a in faqs:
        out.append('<h3>%s</h3>' % q)
        out.append('<p>%s</p>' % a)
    out.append('</section>')
    return '\n'.join(out)


def gloss_html(items):
    out = ['<section id="parole">', '<h2>Parole «difficili», tradotte</h2>', '<dl class="g-gloss">']
    for t, d in items:
        out.append('<div><dt>%s</dt><dd>%s</dd></div>' % (t, d))
    out += ['</dl>', '</section>']
    return '\n'.join(out)


def minutes(body):
    words = len(plain(body).split())
    return max(3, int(math.ceil(words / 200.0))), words


def comuni():
    """Dati e parti condivisi con le altre pagine (sito, persona, riquadro dell'autore): stanno in build_pages.py, che a sua
    volta importa questo file, quindi si caricano solo quando servono."""
    import build_pages
    return build_pages


def guide_page(g, site=None):
    """Una guida. site: le parti che cambiano da un sito all'altro (vedi TOOL qui sotto e PRO in build_pro.py)."""
    site = site or TOOL
    base, fix = site['base'], site['content']
    path = g['path']
    mins, words = minutes(g['body'] + faq_html(g['faqs']) + gloss_html(g['gloss']))
    crumbs_ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": base + "/"},
        {"@type": "ListItem", "position": 2, "name": site['crumbs'][0], "item": base + site['crumbs'][1].split('#')[0]},
        {"@type": "ListItem", "position": 3, "name": g['crumb'], "item": base + path}]}
    bp = comuni()
    article_ld = {"@type": "Article", "headline": g['title'], "description": g['desc'], "inLanguage": "it-IT",
                  "datePublished": GUIDE_PUBBLICATE, "dateModified": bp.AGG, "mainEntityOfPage": base + path,
                  "author": {"@id": bp.PERSONA_ID}, "publisher": {"@id": bp.PERSONA_ID}, "isPartOf": {"@id": bp.SITO_ID}}
    if site.get('image', True):
        article_ld["image"] = BASE + "/og-image.png"
    faq_ld = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
        for q, a in g['faqs']]}
    ld = bp.con_nodi({"@context": "https://schema.org", "@graph": [article_ld, crumbs_ld, faq_ld]})

    toc = '\n'.join('      <li><a href="#%s">%s</a></li>' % (i, t) for i, t in g['toc'])
    brief = '\n'.join('      <li>%s</li>' % b for b in g['brief'])
    parts = [
        head(g['title'], g['desc'], path, g['og'], ld, base=base, site_name=site['site_name'], image=site.get('image', True), copy=site['copy']),
        '<body class="guide">',
        site['nav'](),
        site['top'],
        '',
        '<div class="wrap g-hero">',
        '  <div>',
        '    <nav class="crumbs" aria-label="Percorso"><a href="/">Home</a> <span>›</span> <a href="%s">%s</a> <span>›</span> %s</nav>' % (site['crumbs'][1], site['crumbs'][0], g['crumb']),
        '    <h1 class="g-title">%s</h1>' % g['h1'],
        '    <p class="g-lead">%s</p>' % g['lead'],
        '    <p class="g-meta"><span>Aggiornata il <time datetime="__AGGIORNATA__">__AGGIORNATA_IT__</time></span><span>%d minuti di lettura</span><span>%s</span></p>' % (mins, g['per']),
        '  </div>',
        '  <aside class="g-brief" aria-labelledby="briefTitle">',
        '    <h2 id="briefTitle">In breve</h2>',
        '    <ul>', brief, '    </ul>',
        '  </aside>',
        '</div>',
        '',
        '<div class="wrap g-layout">',
        '  <nav class="g-toc" aria-labelledby="tocTitle">',
        '    <h2 id="tocTitle">In questa guida</h2>',
        '    <ol>', toc, '    </ol>',
        '  </nav>',
        '  <main class="g-main">',
        fix(g['body'].strip()),
        '',
        fix(gloss_html(g['gloss'])),
        '',
        fix(faq_html(g['faqs'])),
        '',
        fix(g['mossa'].strip()),
        site['end'],
        '',
        '<div class="g-end">',
        '<p>Questa guida spiega le regole generali e non sostituisce un parere sul tuo caso specifico.</p>',
        '<details><summary>Norme citate</summary><p>%s</p></details>' % g['norme'],
        '</div>',
        bp.autore(data=False).rstrip('\n'),  # chi cura la guida, come nelle altre pagine (la data è già sotto il titolo)
        '  </main>',
        '</div>',
        '',
        site['contact'],
        '',
        site['footer'],
        site['tail'],
    ]
    return '\n'.join(parts).replace('\n\n\n', '\n\n'), mins, words


SHARE = '''<section class="g-share" aria-label="Per gli avvocati">
  <div class="wrap">
    <p><strong>Sei un avvocato?</strong> Questa guida è scritta per i tuoi clienti: copia il collegamento e mandagliela per mail o in un messaggio.</p>
    <div class="g-share-btns">
      <button type="button" class="btn btn-secondary" id="copyLink">Copia il collegamento</button>
      <button type="button" class="btn btn-secondary" id="shareLink" hidden>Condividi</button>
    </div>
    <span class="g-share-msg" id="copyMsg" role="status"></span>
  </div>
</section>'''

TOOL = {  # calcolaprecetti.it: le guide sono «da mandare ai clienti», con la barra per gli avvocati
    'base': BASE, 'site_name': 'calcolaprecetti.it', 'copy': COPY, 'image': True,
    'nav': lambda: nav('guida'), 'top': SHARE,
    'crumbs': ('Guide per i clienti', '/guide/#clienti'),
    'content': lambda s: s, 'end': '',
    'contact': CONTACT, 'footer': FOOTER, 'tail': TAIL,
}


def step(n, title, body, when=None, sid=None):
    return '\n'.join([
        '<li class="g-step"%s>' % (' id="%s"' % sid if sid else ''),
        '<div class="g-num" aria-hidden="true">%d</div>' % n,
        '<div>',
        ('<p class="g-when">%s</p>' % when) if when else '',
        '<h3>%s</h3>' % title,
        body.strip(),
        '</div>',
        '</li>',
    ]).replace('\n\n', '\n')


def row(label, value, tot=False):
    return ('<div class="g-row%s"><span class="l">%s</span><span class="d"></span><span class="v">%s</span></div>'
            % (' tot' if tot else '', label, value))


def note(label, text, cls=''):
    return '<div class="g-note%s"><span class="g-note-l">%s</span><p>%s</p></div>' % (' ' + cls if cls else '', label, text)


def law(*pairs):
    return '<dl class="g-law">\n' + '\n'.join('<div><dt>%s</dt><dd>%s</dd></div>' % p for p in pairs) + '\n</dl>'


def tidy(text):
    """Nel corpo della pagina «€ 40» non va a capo tra il simbolo e la cifra."""
    cut = text.index('<body')
    return text[:cut] + re.sub(r'€ (?=\d)', '€&nbsp;', text[cut:])


def write(path, text):
    text = tidy(text)
    full = os.path.join(SITE, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(text)
    return full


if __name__ == '__main__':
    import shutil
    GUIDE_JS = os.path.join(SITE, 'assets', 'guide.js')  # script delle guide: si modifica in _sorgenti/gen/guide.js
    if not GUIDE:  # sezione spenta: nel sito non resta nessuna pagina delle guide
        shutil.rmtree(os.path.join(SITE, 'guide'), ignore_errors=True)
        if os.path.exists(GUIDE_JS):
            os.remove(GUIDE_JS)
        print('guide spente: cartella «guide» e assets/guide.js tolti dal sito')
        raise SystemExit
    try:  # testi delle guide: bozze fuori dal repository finché non si pubblicano
        from guide_testi import GUIDA1, GUIDA2, GUIDA3, CARDS, index_page
    except ImportError:
        raise SystemExit('GUIDE = True, ma manca _sorgenti/gen/guide_testi.py con i testi delle guide '
                         '(bozze consegnate a parte): vedi _sorgenti/LEGGIMI.md')
    shutil.copyfile(os.path.join(GEN, 'guide.js'), GUIDE_JS)
    info = []
    for g in (GUIDA1, GUIDA2, GUIDA3):
        page, mins, words = guide_page(g)
        f = write(g['path'], page)
        info.append((g, mins, CARDS[g['path']][1]))
        print('%-44s %5d parole, %d min, %6d byte | titolo %d, descrizione %d caratteri'
              % (g['path'], words, mins, len(page.encode('utf-8')), len(g['title']), len(g['desc'])))
    f = write('/guide/', index_page(info))
    print('%-52s %d byte' % ('/guide/', os.path.getsize(f)))
