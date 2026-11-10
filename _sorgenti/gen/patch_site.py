#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Porta il sito v5 alla nuova struttura.

Riparte ogni volta dai file puliti della v5 (cartella v5) e scrive il risultato nella cartella site,
quindi si può rilanciare quante volte serve. Le pagine nuove (termini, tassi, privacy, note legali,
guide) le scrivono build_pages.py e build_guides.py; i file nuovi in assets (termini.js, info.js,
guide.js) sono scritti a mano.

Cosa fa:
- barra in alto a quattro schede e piè di pagina nuovo, uguali in tutte le pagine;
- home più leggera: via il riquadro dei termini e le sezioni nascoste, un rimando alla pagina dei termini;
- app.js: tolti termini, testi legali, tabelle e casi (ora nelle loro pagine); i vecchi indirizzi
  (/#tassi, /#privacy...) portano alle pagine nuove; i casi di verifica si aprono con /#caso-1...;
- core.js: casi di verifica condivisi (CASI), riga del registro, istruzioni per le guide;
- stile, sitemap, licenza e intestazioni dei file.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_guides import nav, FOOTER, CHI_SONO, GUIDE, NEWSLETTER, VALUTAZIONE, faq_html, plain  # noqa: E402  stesse barre e stesso piè di pagina delle pagine generate

# percorsi relativi: questo file sta in _sorgenti/gen; il sito pubblicato è la radice del repository
GEN = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(GEN))
V5 = os.path.join(os.path.dirname(GEN), 'v5')  # pagine e script di partenza
OLD_URL = 'https://calcolaprecetti.it/#note-legali'
NEW_URL = 'https://calcolaprecetti.it/note-legali/'


def rd(p):
    return io.open(os.path.join(V5, p), encoding='utf-8').read()


def wr(p, s):
    full = os.path.join(SITE, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    io.open(full, 'w', encoding='utf-8', newline='\n').write(s)


def swap(s, old, new, name):
    assert s.count(old) == 1, 'atteso una volta sola: %s (trovato %d)' % (name, s.count(old))
    print('  ' + name)
    return s.replace(old, new)


def block(s, start, end, new, name, keep_end=True):
    """Sostituisce il testo da start (compreso) a end (escluso, o compreso se keep_end è falso)."""
    assert s.count(start) == 1, 'inizio non univoco: %s' % name
    a = s.index(start)
    b = s.index(end, a)
    if not keep_end:
        b += len(end)
    print('  ' + name)
    return s[:a] + new + s[b:]


def url(s, name):
    return swap(s, OLD_URL, NEW_URL, name + ': indirizzo delle note legali')


# ---------------------------------------------------------------- stile
print('assets/style.css')
css = url(rd('assets/style.css'), 'intestazione')
css = swap(css, '--mark:#FFF1A6; --radius:8px; --wrap:1120px;', '--mark:#FFF1A6; --hl:#FFD84D; --radius:8px; --wrap:1120px;', 'colore evidenziatore')
css = swap(css,
           '@media(min-width:720px){.foot-about{grid-column:auto}}\n'
           '@media(min-width:720px){.foot-grid{grid-template-columns:minmax(0,1.6fr) repeat(3,minmax(0,1fr));gap:32px}}',
           '@media(min-width:720px){.foot-grid{grid-template-columns:repeat(%d,minmax(0,1fr));gap:28px 24px}.foot-about p{max-width:60ch}}\n'
           '@media(min-width:1000px){.foot-grid{grid-template-columns:minmax(0,1.5fr) repeat(%d,minmax(0,1fr));gap:32px}.foot-about{grid-column:auto}.foot-about p{max-width:38ch}}'
           % ((5, 5) if GUIDE else (4, 4)),
           'piè di pagina a cinque colonne')
css = swap(css, '@media print{.termini-wrap,.check.fonti{display:none!important}}', '@media print{.termini-wrap,.check.fonti,.after,.home .g-hero,.aud,.home-info{display:none!important}}', 'stampa del prospetto')
SOLO_GUIDE = '/* ===== solo guide:'  # in guide.css, inizio della parte che serve solo alle pagine delle guide
for f in ('pages.css', 'guide.css'):
    parte = io.open(os.path.join(GEN, f), encoding='utf-8').read()
    if f == 'guide.css' and not GUIDE:  # guide spente: solo la parte comune (evidenziatore, barra delle schede, apertura delle pagine)
        assert parte.count(SOLO_GUIDE) == 1, 'guide.css: inizio della parte delle guide non trovato'
        parte = parte[:parte.index(SOLO_GUIDE)]
    css = css.rstrip('\n') + '\n' + parte.rstrip('\n') + '\n'
    print('  aggiunto ' + f + ('' if GUIDE or f != 'guide.css' else ', parte comune'))
wr('assets/style.css', css)

# ---------------------------------------------------------------- home
# spiegazione, compenso del precetto e domande frequenti sotto il calcolo (le ricerche su compenso e spese del precetto)
HOME_FAQ = [
    ('Come si calcola il precetto su una sentenza?',
     'Si inseriscono il capitale e gli interessi come li indica la sentenza, con la decorrenza del dispositivo, e le spese '
     'di lite liquidate; il calcolo aggiunge gli accessori sui compensi e il compenso del precetto. Gli acconti già ricevuti '
     'si scalano nell\'ordine dell\'art. 1194 c.c.'),
    ('E su un decreto ingiuntivo?',
     'Allo stesso modo: si inseriscono capitale, interessi e spese come li liquida il decreto, e il calcolo aggiunge il '
     'compenso del precetto sullo scaglione del credito.'),
    ("Quanto è il compenso per l'atto di precetto?",
     'Dipende dal valore del credito per cui si procede: la <a href="#compenso">tabella del compenso</a> riporta, per ogni scaglione, il minimo, il '
     'medio e il massimo secondo i parametri del D.M. 55/2014, con i valori del D.M. 147/2022. Al compenso si aggiungono '
     'rimborso forfettario, C.P.A. e, se dovuta, I.V.A.'),
    ('Quali spese si possono chiedere nel precetto?',
     'Le spese liquidate nel titolo, il compenso del precetto con i suoi accessori e le spese vive documentate, come la '
     'notifica. I € 40 di risarcimento forfettario dell\'art. 6 del D.Lgs. 231/2002 si chiedono solo se il titolo li riconosce.'),
    ('Come si imputano gli acconti?',
     'Nell\'ordine dell\'art. 1194 c.c.: prima alle spese liquidate nel titolo, poi agli interessi maturati fino al pagamento, '
     'infine al capitale. Il calcolo lo fa da solo e, dopo ogni acconto, calcola gli interessi sul capitale che resta.'),
    ('Entro quando va eseguito il precetto?',
     'Il debitore ha almeno 10 giorni dalla notifica per pagare (art. 480 c.p.c.); se l\'esecuzione non inizia entro 90 giorni '
     'dalla notifica, il precetto perde efficacia (art. 481 c.p.c.). Le date esatte, con festivi e sospensioni, le calcoli '
     'nella pagina dei <a href="/termini-precetto/">termini del precetto</a>.'),
]
from build_pages import autore as _autore  # noqa: E402
AUTORE_HOME = _autore()
HOME_INFO = """<section class="home-info" aria-label="Come si calcola e domande frequenti">
  <div class="prose">
    <h2 id="come-si-calcola">Come si calcolano le somme del precetto</h2>
    <p>Il prospetto mette in fila le somme che il precetto intima di pagare, nell'ordine dell'atto:</p>
    <ol class="terms">
      <li><strong>capitale</strong> riconosciuto dal titolo, anche in più voci;</li>
      <li><strong>interessi</strong> dalla decorrenza alla data del conteggio: legali (art. 1284, comma 1, c.c.), moratori commerciali (D.Lgs. 231/2002), legali maggiorati dalla domanda giudiziale (art. 1284, comma 4, c.c.) o al tasso convenzionale;</li>
      <li><strong>spese liquidate nel titolo</strong>, con rimborso forfettario, C.P.A. e, se dovuta, I.V.A. sui compensi;</li>
      <li><strong>acconti</strong> già ricevuti, imputati prima alle spese, poi agli interessi e infine al capitale (art. 1194 c.c.);</li>
      <li><strong>compenso del precetto</strong> con i suoi accessori, e le altre spese, come la notifica.</li>
    </ol>
    <p>Per ogni periodo il dettaglio indica il tasso applicato e la sua fonte; le tabelle complete sono nella pagina <a href="/tassi/">Tassi e fonti</a>.</p>

    <h2 id="compenso">Compenso e spese del precetto</h2>
    <p>Il compenso dell'atto di precetto segue i parametri del D.M. 55/2014, con i valori del D.M. 147/2022, e si calcola sullo scaglione del credito per cui si procede: capitale, interessi e spese, al netto degli acconti. Il calcolo usa il valore medio; in «Opzioni avanzate» puoi scegliere il minimo, il massimo o un importo libero.</p>
    <div class="scroll"><table class="det rates" id="tabPrecetto"></table></div>
    <p>Al compenso si aggiungono <span class="js-accessori"></span>. L'I.V.A. si chiede solo se il creditore non la detrae e l'avvocato non è in regime forfettario. Le spese vive documentate, come la notifica o l'imposta di registro del titolo, si aggiungono tra le «Altre spese».</p>
  </div>
  <div class="prose">
""" + faq_html(HOME_FAQ) + """
  </div>
""" + AUTORE_HOME + """</section>"""
print('index.html')
h = url(rd('index.html'), 'intestazione')
h = swap(h, "<title>calcolaprecetti.it – Calcolo delle somme dell'atto di precetto</title>",
         "<title>Calcolo dell'atto di precetto: somme, interessi, compenso e spese</title>", 'titolo con compenso e spese')
h = swap(h, '<main class="wrap layout">', '<main class="wrap calcolo">\n<div class="layout">', 'calcolo e spiegazione nella stessa area')
h = swap(h, '  </section>\n</main>', '  </section>\n</div>\n' + HOME_INFO + '\n</main>', 'spiegazione, compenso e domande frequenti')
h = swap(h,
         "spese del titolo, compenso secondo il D.M. 55/2014 e termini del precetto. Tabella pronta per Word.",
         "spese del titolo e compenso secondo il D.M. 55/2014. Tabella pronta per Word.",
         'descrizione senza i termini')
h = block(h, '<header class="top">', '</nav>\n',
          nav('home', '<button type="button" class="tbtn" id="btnNew">Nuovo calcolo</button>') + '\n',
          'barra a quattro schede', keep_end=False)
h = swap(h, '''<div class="wrap intro">
  <h1>Calcolo delle somme del precetto</h1>
  <p>Inserisci i dati del titolo: il prospetto si aggiorna mentre scrivi e lo porti in Word con un clic. <button type="button" class="linkbtn" id="btnExample">Prova con un esempio</button></p>
</div>''', '''<div class="wrap g-hero solo">
  <div>
    <h1 class="g-title">Calcolo delle <mark>somme del precetto</mark></h1>
    <p class="g-lead">Inserisci i dati del titolo: il prospetto si aggiorna mentre scrivi e lo porti in Word con un clic. <button type="button" class="linkbtn" id="btnExample" data-conta="esempio">Prova con un esempio</button></p>
  </div>
</div>''', 'apertura come nelle guide')
h = swap(h, '<button type="button" class="linkbtn" id="emptyExample">', '<button type="button" class="linkbtn" id="emptyExample" data-conta="esempio">', 'esempio contato')
h = swap(h, '<button type="button" class="btn btn-primary" id="btnCopy">', '<button type="button" class="btn btn-primary" id="btnCopy" data-conta="copia-word">', 'copia contata')
h = swap(h, '<button type="button" class="btn btn-secondary" id="btnDocx">', '<button type="button" class="btn btn-secondary" id="btnDocx" data-conta="scarica-docx">', 'file Word contato')
h = swap(h, '<button type="button" class="linkbtn" id="btnPrint">', '<button type="button" class="linkbtn" id="btnPrint" data-conta="stampa">', 'stampa contata')
h = swap(h, '      <div class="warnings" id="warnings" aria-live="polite"></div>\n',
         '      <p class="case-msg" id="caseMsg" hidden></p>\n'
         '      <div class="warnings" id="warnings" aria-live="polite"></div>\n', 'spazio per il caso di verifica')
h = swap(h, '    </div>\n    <p class="sr-only" aria-live="polite" id="srTotal"></p>\n',
         '    </div>\n'
         '    <p class="after"><a href="/termini-precetto/">Precetto notificato? Calcola i termini di 10 e 90 giorni</a></p>\n' +
         '    <p class="after"><a href="/recupero-crediti/" data-conta="recupero-da-home">Devi recuperare un credito? Avvocato per il recupero crediti a Vicenza e Bassano del Grappa</a></p>\n' +
         ('    <p class="after"><a href="/newsletter/">Un consiglio sul recupero crediti ogni due settimane: iscriviti alla newsletter</a></p>\n' if NEWSLETTER else '') +
         '    <p class="sr-only" aria-live="polite" id="srTotal"></p>\n', 'rimando alla pagina dei termini')
h = block(h, '<section class="wrap termini-wrap" id="termini"', '<section class="wrap contact"', '', 'via il riquadro dei termini')
h = block(h, '<section class="wrap legal" id="info" hidden>', '<footer class="foot">', '', 'via le sezioni nascoste')
h = block(h, '<footer class="foot">', '</footer>', FOOTER, 'piè di pagina nuovo', keep_end=False)
# i € 40 dell'art. 6 D.Lgs. n. 231/2002 anche nel calcolo del precetto, solo se riconosciuti nel titolo
h = swap(h, "      <button type=\"button\" class=\"addbtn\" id=\"addItem\">+ Aggiungi un'altra voce di capitale</button>\n    </section>",
         "      <button type=\"button\" class=\"addbtn\" id=\"addItem\">+ Aggiungi un'altra voce di capitale</button>\n"
         "      <label class=\"check\" style=\"margin-top:16px\">\n"
         "        <input type=\"checkbox\" id=\"optForfait\">\n"
         "        <span><span class=\"t\">Aggiungi €&nbsp;40,00 di risarcimento forfettario delle spese di recupero (art. 6 D.Lgs. n. 231/2002)</span>\n"
         "        <span class=\"hint\" style=\"margin-top:2px\">Solo se il titolo lo riconosce: nel precetto si chiedono soltanto le somme che risultano dal titolo.</span></span>\n"
         "      </label>\n"
         "    </section>",
         'casella dei 40 euro (art. 6)')
h = swap(h, '<meta name="description" content="Calcolo gratuito delle somme da intimare con l\'atto di precetto: capitale, interessi legali e moratori, '
         'acconti ex art. 1194 c.c., spese del titolo e compenso secondo il D.M. 55/2014. Tabella pronta per Word. Nessun cookie.">',
         '<meta name="description" content="Calcolo gratuito delle somme del precetto: capitale, interessi, acconti, spese '
         'e compenso (D.M. 55/2014), con la tabella dei compensi. Prospetto per Word.">', 'descrizione con il compenso')
# dati strutturati della home: il sito (nome mostrato da Google) e il calcolatore, con l'autore
import json  # noqa: E402
from build_pages import NOME, SITO_ID, PERSONA_ID, AGG, con_nodi, autore  # noqa: E402  stessi dati della pagina «Chi sono»
HOME_LD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebApplication", "name": "Calcolo delle somme del precetto", "url": "https://calcolaprecetti.it/",
     "isPartOf": {"@id": SITO_ID}, "dateModified": AGG,
     "description": "Calcolo delle somme da intimare con l'atto di precetto: capitale, interessi legali e moratori, acconti, "
                    "spese del titolo e compenso secondo il D.M. 55/2014, con il prospetto pronto per Word.",
     "applicationCategory": "BusinessApplication", "operatingSystem": "Tutti", "inLanguage": "it-IT", "isAccessibleForFree": True,
     "browserRequirements": "Richiede JavaScript", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
     "author": {"@id": PERSONA_ID}},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
                                         for q, a in HOME_FAQ]}]}
h = swap(h, '<link rel="stylesheet" href="/assets/style.css">\n',
         '<link rel="stylesheet" href="/assets/style.css">\n<script type="application/ld+json">%s</script>\n'
         % json.dumps(con_nodi(HOME_LD), ensure_ascii=False), 'dati strutturati della home')
wr('index.html', h)

# ---------------------------------------------------------------- interessi moratori
print('interessi-moratori/index.html')
h = url(rd('interessi-moratori/index.html'), 'intestazione')
h = block(h, '<header class="top">', '</nav>\n', nav('mora') + '\n', 'barra a quattro schede', keep_end=False)
h = swap(h, '''<div class="wrap intro">
  <nav class="crumbs" aria-label="Percorso"><a href="/">Home</a> <span>›</span> Calcolo interessi moratori</nav>
  <h1>Calcolo degli interessi moratori 2026</h1>
  <p>Interessi moratori, o interessi di mora, nelle transazioni commerciali: calcolo gratuito, semestre per semestre, con la fonte di ogni tasso.</p>
</div>''', '''<div class="wrap g-hero solo">
  <div>
    <nav class="crumbs" aria-label="Percorso"><a href="/">Home</a> <span>›</span> Calcolo interessi moratori</nav>
    <h1 class="g-title">Calcolo degli <mark>interessi moratori 2026</mark></h1>
    <p class="g-lead">Interessi moratori, o interessi di mora, nelle transazioni commerciali: calcolo gratuito, semestre per semestre, con la fonte di ogni tasso.</p>
  </div>
</div>''', 'apertura come nelle guide')
h = block(h, '<footer class="foot">', '</footer>', FOOTER, 'piè di pagina nuovo', keep_end=False)
if GUIDE:
    h = swap(h, '    <h2>Poi serve il precetto?</h2>',
             '''    <aside class="send" aria-labelledby="sendTitle">
          <p class="send-l">Da mandare al cliente</p>
          <h2 id="sendTitle">La fattura non è stata pagata: e adesso?</h2>
          <p>Due guide brevi e senza gergo per chi deve farsi pagare. Aprile e copia il collegamento: si mandano per mail o in un messaggio.</p>
          <ul>
            <li><a href="/guide/fattura-non-pagata/">Fattura non pagata: cosa fare, passo per passo</a><span>I sei passi dal sollecito al pignoramento, con il calcolo di quanto spetta.</span></li>
            <li><a href="/guide/decreto-ingiuntivo-tempi-costi/">Decreto ingiuntivo: tempi e costi</a><span>Quanto ci vuole, quanto si anticipa e chi paga alla fine.</span></li>
          </ul>
        </aside>
    
        <h2>Poi serve il precetto?</h2>''', 'riquadro «Da mandare al cliente»')
h = swap(h, "acconti già ricevuti e compenso per l'atto, con la tabella pronta da incollare in Word.</p>",
         "acconti già ricevuti e compenso per l'atto, con la tabella pronta da incollare in Word. Dopo la notifica, i 10 e i 90 giorni "
         "li calcoli nella pagina dei <a href=\"/termini-precetto/\">termini del precetto</a>.</p>", 'rimando alla pagina dei termini')
if VALUTAZIONE:
    h = swap(h, 'i 10 e i 90 giorni li calcoli nella pagina dei <a href="/termini-precetto/">termini del precetto</a>.</p>',
             'i 10 e i 90 giorni li calcoli nella pagina dei <a href="/termini-precetto/">termini del precetto</a>.</p>\n\n'
             '    <h2>Il credito non è ancora stato pagato?</h2>\n'
             '    <p>Se vuoi sapere se e come conviene recuperarlo, puoi chiedere una <a href="/valutazione-credito/" data-conta="valutazione-da-interessi">valutazione del credito</a>: '
             'un parere scritto e firmato da un avvocato, con costi e tempi stimati, a prezzo fisso. Per affidare il recupero, dalla diffida al '
             'pignoramento, vedi <a href="/recupero-crediti/" data-conta="recupero-da-interessi">Recupero crediti a Vicenza e Bassano del Grappa</a>.</p>',
             'rimando alla valutazione del credito')
# dati strutturati collegati: l'applicazione fa parte del sito, ha un autore e una data; riquadro dell'autore
_m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
_ld = json.loads(_m.group(1))
_app = [g for g in _ld['@graph'] if g['@type'] == 'WebApplication']
assert len(_app) == 1
_app[0].update({'isPartOf': {'@id': SITO_ID}, 'author': {'@id': PERSONA_ID}, 'dateModified': AGG})
h = h[:_m.start(1)] + json.dumps(con_nodi(_ld), ensure_ascii=False) + h[_m.end(1):]
h = swap(h, '  </article>\n</main>', '  </article>\n' + autore() + '</main>', 'riquadro dell\'autore')
h = swap(h, '<button type="button" class="btn btn-primary" id="miniCopy">', '<button type="button" class="btn btn-primary" id="miniCopy" data-conta="copia-moratori">', 'copia contata')
if NEWSLETTER:
    h = swap(h, 'La tabella completa dal 2002 è più sotto.</p>',
             'La tabella completa dal 2002 è più sotto. Per sapere quando cambia, iscriviti alla <a href="/newsletter/">newsletter</a>.</p>',
             'rimando alla newsletter')
h = swap(h, "senza doverli provare e salvo il maggior danno (art. 6). Nel precetto si indica come voce separata.</p>",
         "senza doverli provare e salvo il maggior danno (art. 6). Si chiede già nella diffida e nel ricorso per decreto ingiuntivo. "
         "Nel precetto va indicato come voce separata, ma solo se il titolo lo riconosce: nel "
         "<a href=\"/\">calcolo delle somme del precetto</a> si aggiunge con una casella.</p>",
         'i 40 euro nel precetto solo se riconosciuti nel titolo')
for t in ('<title>%s</title>', '<meta property="og:title" content="%s">'):
    h = swap(h, t % 'Interessi moratori 2026: calcolo online e tasso (D.Lgs. 231/2002)',
             t % 'Interessi moratori 2026: calcolo e tasso (D.Lgs. 231/2002)', 'titolo più corto')
h = re.sub(r'<meta name="description" content="Calcolo gratuito degli interessi moratori \(interessi di mora\)[^"]*">',
           '<meta name="description" content="Calcolo gratuito degli interessi di mora sulle fatture non pagate: tasso BCE più 8 punti, '
           'semestre per semestre, con le fonti. Tabella dal 2002.">', h, count=1)
assert 'Tabella dal 2002.">' in h, 'descrizione degli interessi moratori'
wr('interessi-moratori/index.html', h)

# ---------------------------------------------------------------- sitemap, licenza, altri file
print('sitemap.xml')
wr('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    '  <url><loc>https://calcolaprecetti.it%s</loc></url>\n' % p for p in (
        '/', '/termini-precetto/', '/interessi-moratori/', '/tassi/', '/recupero-crediti/')
    + (('/guide/', '/guide/fattura-non-pagata/', '/guide/decreto-ingiuntivo-tempi-costi/', '/guide/precetto-notificato/') if GUIDE else ())
    + (('/chi-sono/',) if CHI_SONO else ()) + (('/valutazione-credito/',) if VALUTAZIONE else ())
    + (('/newsletter/',) if NEWSLETTER else ())) + '</urlset>\n')
print('  %d indirizzi' % (5 + (4 if GUIDE else 0) + (1 if CHI_SONO else 0) + (1 if NEWSLETTER else 0) + (1 if VALUTAZIONE else 0)))
for f in ('LICENSE', 'assets/docx.js'):
    print(f)
    wr(f, url(rd(f), 'intestazione'))
print('assets/mini.js')
js = url(rd('assets/mini.js'), 'intestazione')
js = swap(js, "    out.hidden = false;\n    $('#miniActions').hidden = false;\n",
          "    out.hidden = false;\n    $('#miniActions').hidden = false;\n"
          "    if (window.Conta) Conta.evento('calcolo-moratori', true); // statistiche: un calcolo per pagina aperta, senza i dati\n",
          'calcolo contato')
wr('assets/mini.js', js)

# ---------------------------------------------------------------- core.js: casi di verifica, registro, istruzioni
print('assets/core.js')
js = url(rd('assets/core.js'), 'intestazione')
js = swap(js, "  titolare: 'a.m.',", "  titolare: 'avv. Alessandro Moro',", 'titolare del sito')
js = swap(js, "  informativaAggiornata: '22.09.2026'",
          "  informativaAggiornata: '29.10.2026',\n"
          "  piva: '04591770245',\n"
          "  // Statistiche delle visite senza cookie (in fondo a questo file e nella pagina «Privacy»):\n"
          "  // servizio 'umami' (codice: l'ID del sito, data-website-id nel codice dato da Umami), 'plausible'\n"
          "  // oppure 'goatcounter' (codice: quello scelto all'iscrizione, es. 'calcolaprecetti').\n"
          "  // servizio: '' le spegne. Cambiando servizio, l'informativa privacy si adegua da sola.\n"
          "  statistiche: { servizio: 'umami', codice: 'bb2d5a3e-273f-4655-af5b-b3fdc692f6df' }", 'data dell\'informativa e statistiche')
if GUIDE:
    js = swap(js,
              "      (_sorgenti/v5/interessi-moratori/index.html).\n\n   Regole:",
              "      (_sorgenti/v5/interessi-moratori/index.html).\n\n"
              "   6) Guide (cartella «guide») - i tassi scritti nel testo e i calcoli\n"
              "      rapidi leggono queste tabelle e si aggiornano da soli. Vanno invece\n"
              "      corretti a mano, nel file della singola guida, quando cambia la\n"
              "      legge: nella guida al decreto ingiuntivo la tabella dei costi\n"
              "      (contributo unificato e compenso medio: i calcoli leggono i numeri\n"
              "      scritti nelle righe, attributi data-cu e data-comp) e la soglia del\n"
              "      giudice di pace (data-gdp, oggi 10000; 30000 dal 31.10.2027, salvo\n"
              "      altri rinvii). La data «Aggiornata il» si aggiorna da sola.\n\n   Regole:",
              'istruzioni per le guide')
if NEWSLETTER:
    js = swap(js,
              "      moratori» con i tassi dell'anno nuovo.\n\n",
              "      moratori» con i tassi dell'anno nuovo.\n\n"
              "   6) Newsletter - ogni due settimane una puntata da Brevo: Campagne,\n"
              "      duplicare l'ultima, cambiare oggetto e testo, inviare. Dopo i\n"
              "      punti 1 e 2 anche l'avviso sui tassi: a metà dicembre il tasso\n"
              "      legale, a inizio gennaio e luglio i moratori.\n\n",
              'istruzioni per la newsletter')
js = swap(js,
          "   Verifica: «Prova con un esempio» deve dare € 2.256,33 e i «Casi di\n"
          "   verifica» in fondo alla pagina devono tornare.",
          "   Verifica: «Prova con un esempio» deve dare € 2.256,33 e i casi della\n"
          "   pagina «Tassi e verifiche» (calcolaprecetti.it/tassi/#verifica),\n"
          "   aperti con «Apri nel calcolo», devono tornare.",
          'verifica nella pagina dei tassi')
js = swap(js,
          "  registro: [ // [data, cosa è cambiato] — le righe più recenti in alto\n",
          "  registro: [ // [data, cosa è cambiato] — le righe più recenti in alto\n"
          "    ['2026-10-08', \"Nuova organizzazione del sito: i termini del precetto hanno una pagina propria; tabelle dei tassi, casi di verifica e registro sono riuniti nella pagina «Tassi e verifiche»; privacy e note legali hanno pagine proprie; nuova pagina «Chi sono».\"],\n",
          'riga del registro')
CASI = '''
/* =====================================================================
   CASI DI VERIFICA (pagina «Tassi e verifiche»)
   Conteggi svolti a mano. "pagina" dice quale calcolo li apre
   (precetto: la home; termini: la pagina dei termini); "dati" sono i
   valori che vengono caricati. Se cambia un tasso usato qui, il conto
   scritto in "conto" e "risultato" va rifatto.
   ===================================================================== */
var CASI = [
  { titolo: 'Interessi legali in un solo anno',
    testo: 'Capitale € 10.000,00, interessi legali dal 01.01.2026 al 30.06.2026, senza spese né compenso di precetto.',
    conto: ['181 giorni al tasso legale 2026 (1,60%):', '10.000,00 × 1,60% × 181 / 365 = 79,34'],
    risultato: 'Interessi € 79,34; totale € 10.079,34.',
    pagina: 'precetto',
    dati: { end: '2026-06-30', items: [{ amount: '10.000,00', type: 'legal', from: '2026-01-01' }], feeMode: 'free', feeFree: '' } },
  { titolo: 'Interessi moratori su più semestri',
    testo: 'Capitale € 1.394,25, interessi moratori ex D.Lgs. 231/2002 dal 25.09.2025 al 21.09.2026, senza spese né compenso di precetto.',
    conto: ['2° semestre 2025, 98 giorni: 1.394,25 × 10,15% × 98 / 365 = 38,00',
            '1° semestre 2026, 181 giorni: 1.394,25 × 10,15% × 181 / 365 = 70,18',
            '2° semestre 2026, 83 giorni: 1.394,25 × 10,40% × 83 / 365 = 32,97'],
    risultato: 'Interessi € 141,15; totale € 1.535,40.',
    pagina: 'precetto',
    dati: { end: '2026-09-21', items: [{ amount: '1.394,25', type: 'mora', from: '2025-09-25' }], feeMode: 'free', feeFree: '' } },
  { titolo: 'Acconto imputato ex art. 1194 c.c.',
    testo: 'Capitale € 5.000,00 con interessi moratori dal 01.01.2026; spese liquidate nel titolo del 15.12.2025 € 400,00; acconto di € 1.000,00 il 01.04.2026; conteggio al 30.06.2026, senza compenso di precetto.',
    conto: ['Interessi dal 01.01 al 01.04.2026, 91 giorni: 5.000,00 × 10,15% × 91 / 365 = 126,53',
            'Acconto: 400,00 alle spese, 126,53 agli interessi, 473,47 al capitale; capitale residuo 4.526,53',
            'Interessi dal 02.04 al 30.06.2026, 90 giorni: 4.526,53 × 10,15% × 90 / 365 = 113,29',
            '5.000,00 + 126,53 + 113,29 + 400,00 − 1.000,00 = 4.639,82'],
    risultato: 'Totale € 4.639,82.',
    pagina: 'precetto',
    dati: { end: '2026-06-30', items: [{ amount: '5.000,00', type: 'mora', from: '2026-01-01' }], spese: '400,00', feeMode: 'free', feeFree: '',
            acconti: [{ date: '2026-04-01', amount: '1.000,00' }], titleDate: '2025-12-15' } },
  { titolo: 'Termini del precetto',
    testo: 'Precetto notificato il 01.10.2026 con il termine di 10 giorni; istanza ex art. 492-bis presentata il 20.10.2026, esito comunicato il 10.11.2026.',
    conto: ['10 giorni: 11.10.2026, domenica, prorogato a lunedì 12.10.2026; esecuzione dal 13.10.2026',
            '90 giorni: 30.12.2026, più 21 giorni di sospensione (dal 20.10 al 10.11.2026) = 20.01.2027'],
    risultato: 'Efficacia fino a mercoledì 20.01.2027.',
    pagina: 'termini',
    dati: { notifica: '2026-10-01', giorni: '10', bis: true, bisFrom: '2026-10-20', bisTo: '2026-11-10' } }
];
'''
js = swap(js, '\nvar Core = (function () {', CASI + '\nvar Core = (function () {', 'casi di verifica condivisi (CASI)')
CONTA = """
/* =====================================================================
   STATISTICHE DELLE VISITE, SENZA COOKIE (pagina «Privacy»)
   Contano le pagine viste e alcune azioni: calcolo fatto, esempio, copia
   per Word, file .docx, stampa, calendario, richiesta di valutazione del credito.
   Non usano cookie né la memoria del browser e non mandano mai i dati
   dei calcoli: solo l'indirizzo della pagina, il sito di provenienza e
   il nome dell'azione (con Umami anche titolo della pagina, lingua del
   browser e risoluzione dello schermo, come fa il suo script). Contano solo sul sito pubblicato (non nelle copie
   in locale né nelle anteprime) e si fermano se il browser chiede di
   non essere tracciato (Do Not Track, Global Privacy Control).
   Il servizio si sceglie in SITO.statistiche, in cima a questo file.
   Per contare un'azione nuova basta l'attributo data-conta="nome" su un
   pulsante o un collegamento.
   ===================================================================== */
var Conta = (function () {
  'use strict';
  var S = (typeof SITO !== 'undefined' && SITO.statistiche) || {}, fatti = {}, nav = window.navigator || {};
  var attivo = (S.servizio === 'plausible' || (S.servizio === 'goatcounter' && /^[a-z0-9-]+$/.test(S.codice || '')) ||
                (S.servizio === 'umami' && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(S.codice || ''))) &&
    location.protocol === 'https:' && location.hostname === SITO.nome &&
    nav.doNotTrack !== '1' && nav.doNotTrack !== 'yes' && window.doNotTrack !== '1' &&
    nav.globalPrivacyControl !== true && !nav.webdriver;
  function provenienza() { // solo il sito esterno da cui si arriva, senza parametri; vuoto per le pagine interne
    var r = document.referrer || '';
    if (!r || r.indexOf(location.protocol + '//' + location.host + '/') === 0) return '';
    return r.split(/[?#]/)[0];
  }
  function invia(nome, evento) {
    if (!attivo) return;
    try {
      if (S.servizio === 'goatcounter') {
        var img = new Image();
        img.src = 'https://' + S.codice + '.goatcounter.com/count?p=' + encodeURIComponent(nome) +
          (evento ? '&e=true' : '&t=' + encodeURIComponent(document.title) + '&r=' + encodeURIComponent(provenienza())) +
          '&rnd=' + Math.random().toString(36).slice(2);
      } else if (S.servizio === 'umami') { // Umami Cloud, stessi dati del suo script (pagina vista: senza «name»)
        if (!window.fetch) return;
        var sc = window.screen || {}, p = { website: S.codice, hostname: location.hostname, language: nav.language || '',
          screen: (sc.width || 0) + 'x' + (sc.height || 0), title: document.title,
          url: location.protocol + '//' + location.host + location.pathname, referrer: evento ? '' : provenienza() };
        if (evento) p.name = nome;
        fetch('https://gateway.umami.is/api/send', { method: 'POST', keepalive: true, credentials: 'omit',
          headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ type: 'event', payload: p }) })['catch'](function () {});
      } else if (window.fetch) {
        fetch('https://plausible.io/api/event', { method: 'POST', keepalive: true, headers: { 'Content-Type': 'text/plain' },
          body: JSON.stringify({ name: evento ? nome : 'pageview', url: location.protocol + '//' + location.host + location.pathname,
                                 domain: SITO.nome, referrer: evento ? null : (provenienza() || null) }) })['catch'](function () {});
      }
    } catch (e) { /* le statistiche non devono mai disturbare i calcoli */ }
  }
  function evento(nome, unaVolta) {
    if (unaVolta) { if (fatti[nome]) return; fatti[nome] = true; }
    invia(nome, true);
  }
  invia(location.pathname, false);
  document.addEventListener('click', function (e) {
    var el = e.target && e.target.closest ? e.target.closest('[data-conta]') : null;
    if (el) evento(el.getAttribute('data-conta'));
  });
  return { evento: evento, attivo: attivo };
})();
"""
js = js.rstrip('\n') + '\n'
assert js.endswith('})();\n'), 'fine di core.js cambiata'
js = js + CONTA
print('  statistiche delle visite senza cookie (Conta)')
# i € 40 dell'art. 6 D.Lgs. n. 231/2002 nel calcolo del precetto (casella nella home), se riconosciuti nel titolo
js = swap(js, "  rimborsoForfettario: 15, cpa: 4, iva: 22,",
          "  rimborsoForfettario: 15, cpa: 4, iva: 22,\n"
          "  forfettario231: 40, // € di risarcimento forfettario delle spese di recupero (art. 6 D.Lgs. n. 231/2002)", 'importo dei 40 euro')
js = swap(js, "  // st: { end, items:[{desc, amount, type, from, domanda, rate}], titolo, spese, compensi,",
          "  // st: { end, items:[{desc, amount, type, from, domanda, rate}], forfait, titolo, spese, compensi,", 'stato: i 40 euro')
js = swap(js, "    var T = toDay(st.titleDate), S = titTot, accTot = 0;\n",
          "    var T = toDay(st.titleDate), S = titTot, accTot = 0;\n"
          "    // € 40 dell'art. 6 D.Lgs. n. 231/2002, se riconosciuti nel titolo: sono spese di recupero, dovute dall'inizio del ritardo;\n"
          "    // negli acconti vengono imputati per primi, prima delle spese liquidate nel titolo (artt. 1193 e 1194 c.c.)\n"
          "    var forfait = st.forfait && list.length ? TABELLE.forfettario231 : 0, F = forfait;\n"
          "    var F0 = list.reduce(function (m, x) { return x.from !== null && (m === null || x.from < m) ? x.from : m; }, null);\n",
          'i 40 euro: importo e decorrenza')
js = swap(js, "      if (S > 0 && (T === null || T <= p.day)) { var vs = r2(Math.min(rest, S)); S = r2(S - vs); rest = r2(rest - vs); rec.spese = vs; }\n",
          "      if (F > 0 && (F0 === null || F0 <= p.day)) { var vf = r2(Math.min(rest, F)); F = r2(F - vf); rest = r2(rest - vf); rec.spese = vf; }\n"
          "      if (S > 0 && (T === null || T <= p.day)) { var vs = r2(Math.min(rest, S)); S = r2(S - vs); rest = r2(rest - vs); rec.spese = r2(rec.spese + vs); }\n",
          'i 40 euro negli acconti')
js = swap(js, "    res.rows = res.rows.concat(titRows);\n",
          "    if (forfait) res.rows.push({ label: 'Risarcimento forfettario ex art. 6 D.Lgs. n. 231/2002', amount: forfait });\n"
          "    res.rows = res.rows.concat(titRows);\n", 'i 40 euro nel prospetto')
js = swap(js, "    res.valore = r2(Math.max(0, capTot + intTot + titTot + extTot - accTot));",
          "    res.valore = r2(Math.max(0, capTot + intTot + forfait + titTot + extTot - accTot));", 'i 40 euro nel valore del credito')
js = swap(js, "    ['2026-10-08', \"Nuova organizzazione del sito:",
          "    ['2026-10-28', \"Nel calcolo delle somme del precetto si possono aggiungere i € 40,00 di risarcimento forfettario "
          "(art. 6 D.Lgs. n. 231/2002), se riconosciuti nel titolo.\"],\n"
          "    ['2026-10-08', \"Nuova organizzazione del sito:", 'riga del registro: i 40 euro')
wr('assets/core.js', js)

# ---------------------------------------------------------------- app.js: solo il calcolo delle somme
print('assets/app.js')
js = url(rd('assets/app.js'), 'intestazione')
js = swap(js, "(function () {\n  'use strict';\n  var C = Core;\n",
          "(function () {\n  'use strict';\n"
          "  // indirizzi della versione precedente (calcolaprecetti.it/#privacy e simili): ora sono pagine\n"
          "  var MOVED = { tassi: '/tassi/', verifica: '/tassi/#verifica', registro: '/tassi/#registro', privacy: '/privacy/', 'note-legali': '/note-legali/', termini: '/termini-precetto/' };\n"
          "  if (MOVED[location.hash.slice(1)]) { location.replace(MOVED[location.hash.slice(1)]); return; }\n"
          "  var C = Core;\n", 'vecchi indirizzi verso le pagine nuove')
js = swap(js, "             acconti: [], titleDate: '', fonti: true,\n"
              "             tNotifica: '', tGiorni: '10', tBis: false, tBisFrom: '', tBisTo: '' };",
          "             acconti: [], titleDate: '', fonti: true };", 'stato senza i termini')
js = swap(js, '  var last = null, lastT = null;', '  var last = null, caseShown = false, shownTotal = null, sweepTimer = null;', 'variabili')
js = swap(js, "    if (empty) return;\n",
          "    if (empty) { shownTotal = null; $('#mbTotal').classList.remove('tot-hl'); return; }\n", 'prospetto vuoto')
js = swap(js, "'<tr class=\"total\"><td>TOTALE COMPLESSIVO</td><td class=\"amt\">' + C.eur(res.total) + '</td></tr>';\n",
          "'<tr class=\"total\"><td>TOTALE COMPLESSIVO</td><td class=\"amt\"><span class=\"tot-hl\">' + C.eur(res.total) + '</span></td></tr>';\n"
          "    animate(res.total);\n", 'totale evidenziato')
js = swap(js, "  function sourcesText(res) { return 'Fonti dei tassi: ' + res.sources.join('; ') + '.'; }\n",
          "  function sourcesText(res) { return 'Fonti dei tassi: ' + res.sources.join('; ') + '.'; }\n\n"
          "  /* ---------- due animazioni minime: il prospetto entra quando compare, l'evidenziatore ripassa il totale quando cambia ---------- */\n"
          "  function sweep(el) { el.classList.remove('sweep'); void el.offsetWidth; el.classList.add('sweep'); }\n"
          "  function animate(total) {\n"
          "    var first = shownTotal === null;\n"
          "    if (first) {\n"
          "      sweep($('#sheet'));\n"
          "      if (window.Conta) Conta.evento('calcolo-somme', true); // statistiche: un calcolo per pagina aperta, senza i dati\n"
          "    }\n"
          "    $('#mbTotal').classList.add('tot-hl');\n"
          "    if (total !== shownTotal) {\n"
          "      clearTimeout(sweepTimer);\n"
          "      sweepTimer = setTimeout(function () { // a calcolo fermo, non a ogni tasto\n"
          "        var t = $('#table tr.total .tot-hl');\n"
          "        if (t) sweep(t);\n"
          "        sweep($('#mbTotal'));\n"
          "      }, first ? 250 : 450);\n"
          "    }\n"
          "    shownTotal = total;\n"
          "  }\n", 'animazioni')
js = swap(js, "  var TEXTS = [['endDate', 'end'], ['spese', 'spese'], ['compensi', 'compensi'], ['feeFree', 'feeFree'], ['titleDate', 'titleDate'],\n"
              "               ['tNotifica', 'tNotifica'], ['tGiorni', 'tGiorni'], ['tBisFrom', 'tBisFrom'], ['tBisTo', 'tBisTo']];\n"
              "  var CHECKS = [['optIva', 'iva'], ['optRf', 'rf'], ['optCpa', 'cpa'], ['optFonti', 'fonti'], ['tBis', 'tBis']];",
          "  var TEXTS = [['endDate', 'end'], ['spese', 'spese'], ['compensi', 'compensi'], ['feeFree', 'feeFree'], ['titleDate', 'titleDate']];\n"
          "  var CHECKS = [['optIva', 'iva'], ['optRf', 'rf'], ['optCpa', 'cpa'], ['optFonti', 'fonti']];", 'campi senza i termini')
js = swap(js, '    renderMoreSummary();\n    renderTermini();\n  }',
          "    renderMoreSummary();\n    if (caseShown) { caseShown = false; $('#caseMsg').hidden = true; } // il caso di verifica resta indicato finché non si cambia un dato\n  }",
          'ricalcolo senza i termini')
js = block(js, '  /* ---------- termini del precetto ---------- */', '  /* ---------- esportazione ---------- */', '',
           'via il calcolo dei termini (ora in termini.js)')
js = block(js, '  /* ---------- testi legali e tabelle ---------- */', '  /* ---------- avvio ---------- */', '''  /* ---------- piè di pagina e contatti ---------- */
  function renderFoot() {
    $$('.js-updated').forEach(function (e) { e.textContent = TABELLE.aggiornamento; });
    $$('.js-titolare').forEach(function (e) { e.textContent = SITO.titolare; });
  }
  function renderContact() {
    $('#mailBtn').href = 'mailto:' + SITO.email + '?subject=' + encodeURIComponent('Suggerimento per ' + SITO.nome);
    $('#mailText').textContent = SITO.email;
  }
  // tabella del compenso del precetto sotto il calcolo: stessi dati e stessa forma della pagina dei tassi (info.js)
  function renderCompenso() {
    var tp = $('#tabPrecetto');
    if (tp) {
      tp.innerHTML = '<thead><tr><th>Valore del credito</th><th class="r">Minimo</th><th class="r">Medio</th><th class="r">Massimo</th></tr></thead><tbody>' +
        TABELLE.precetto.map(function (t, i) {
          var from = i === 0 ? 0.01 : TABELLE.precetto[i - 1][0] + 0.01;
          return '<tr><td>da ' + C.eur(from) + ' a ' + C.eur(t[0]) + '</td><td class="r">' + C.eur(t[1] / 2) + '</td><td class="r"><strong>' +
            C.eur(t[1]) + '</strong></td><td class="r">' + C.eur(t[1] * 1.5) + '</td></tr>';
        }).join('') + '</tbody>';
    }
    $$('.js-accessori').forEach(function (e) {
      e.textContent = 'rimborso forfettario ' + TABELLE.rimborsoForfettario + '%, C.P.A. ' + TABELLE.cpa + '% e, se dovuta, I.V.A. ' + TABELLE.iva + '%';
    });
  }

  /* ---------- casi di verifica: la pagina «Tassi e verifiche» apre /#caso-1, /#caso-2... (dati in core.js, CASI) ---------- */
  function caseFromHash() {
    var m = /^#caso-(\\d+)$/.exec(location.hash), c = m && typeof CASI !== 'undefined' ? CASI[+m[1] - 1] : null;
    if (!c || c.pagina !== 'precetto') return;
    var d = JSON.parse(JSON.stringify(c.dati));
    d.items = (d.items || []).map(function (x) { return Object.assign(newItem(), x); });
    d.acconti = (d.acconti || []).map(function (x) { return Object.assign(newAcconto(), x); });
    d.extras = (d.extras || []).map(function (x) { return Object.assign(newExtra(), x); });
    state = Object.assign(defaults(), d);
    refresh();
    var msg = $('#caseMsg');
    msg.textContent = 'Caso di verifica «' + c.titolo + '». Risultato atteso: ' + c.risultato.charAt(0).toLowerCase() + c.risultato.slice(1);
    msg.hidden = false;
    caseShown = true;
    if (history.replaceState) history.replaceState(null, '', location.pathname + location.search);
    if (innerWidth < 960) $('#prospetto').scrollIntoView({ block: 'start' });
  }

''', 'via testi legali, tabelle e casi (ora nelle loro pagine)')
js = swap(js, "  $('#tIcs').addEventListener('click', doIcs);\n", '', 'via il pulsante del calendario')
js = block(js, "  $$('[data-open]').forEach(function (a) {", "\n\n  if ('IntersectionObserver' in window) {",
           "  renderFoot();\n  renderContact();\n  renderCompenso();\n  refresh();\n  caseFromHash();\n"
           "  window.addEventListener('hashchange', function () { // stessa pagina: indirizzo cambiato a mano o caso aperto di nuovo\n"
           "    if (MOVED[location.hash.slice(1)]) location.replace(MOVED[location.hash.slice(1)]);\n"
           "    else caseFromHash();\n"
           "  });", 'avvio')
for gone in ('renderTermini', 'lastT', 'doIcs', 'openSection', 'renderLegal', 'renderRates', 'renderCases', 'renderRegistro',
             'CASES', 'tNotifica', 'tBis', '#info', 'data-open', 'casesBody'):
    assert gone not in js, 'resta in app.js: ' + gone
# i € 40 dell'art. 6 nel calcolo del precetto
js = swap(js, "             acconti: [], titleDate: '', fonti: true };", "             acconti: [], titleDate: '', fonti: true, forfait: false };", 'stato: i 40 euro')
js = swap(js, "var CHECKS = [['optIva', 'iva'], ['optRf', 'rf'], ['optCpa', 'cpa'], ['optFonti', 'fonti']];",
          "var CHECKS = [['optIva', 'iva'], ['optRf', 'rf'], ['optCpa', 'cpa'], ['optFonti', 'fonti'], ['optForfait', 'forfait']];", 'casella dei 40 euro')
js = swap(js, "'<p class=\"det-note\">Prima alle spese liquidate nel titolo, poi agli interessi",
          "'<p class=\"det-note\">Prima alle spese' + (state.forfait ? ' (i € 40 dell\\'art. 6, poi quelle liquidate nel titolo)' : ' liquidate nel titolo') + ', poi agli interessi",
          'nota sugli acconti con i 40 euro')
# tabelle del dettaglio che scorrono di lato: raggiungibili da tastiera, con un nome per i lettori di schermo
js = swap(js, "return '<div class=\"scroll\"><table class=\"det\">' + (many ?",
          "return '<div class=\"scroll\" tabindex=\"0\" role=\"region\" aria-label=\"' + esc('Dettaglio degli interessi' + (many ? ': ' + d.title : '')) + '\"><table class=\"det\">' + (many ?",
          'tabella degli interessi da tastiera')
js = swap(js, "html += '<div class=\"scroll\"><table class=\"det\"><caption>Imputazione degli acconti",
          "html += '<div class=\"scroll\" tabindex=\"0\" role=\"region\" aria-label=\"Imputazione degli acconti\"><table class=\"det\"><caption>Imputazione degli acconti",
          'tabella degli acconti da tastiera')
wr('assets/app.js', js)

# ---------------------------------------------------------------- numero di versione di stile e script
# Ogni pagina chiama style.css e gli script con ?v=<impronta del file>. Dopo un aggiornamento del sito il browser scarica
# i file nuovi invece di usare quelli che ha in memoria: senza, la pagina nuova può comparire per qualche minuto con lo stile vecchio.
import hashlib  # noqa: E402
import re  # noqa: E402


def impronta(p):
    return hashlib.sha256(io.open(os.path.join(SITE, p), 'rb').read()).hexdigest()[:10]


ASSET = re.compile(r'((?:href|src)="/assets/)(style\.css|[a-z]+\.js)(?:\?v=[0-9a-f]+)?(")')
n = 0
for root, dirs, files in os.walk(SITE):
    dirs[:] = [d for d in dirs if not d.startswith(('.', '_'))]  # né .git né _sorgenti
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            s = io.open(p, encoding='utf-8').read()
            t = ASSET.sub(lambda m: '%s%s?v=%s%s' % (m.group(1), m.group(2), impronta('assets/' + m.group(2)), m.group(3)), s)
            if t != s:
                io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
                n += 1
print('numero di versione di stile e script: %d pagine' % n)

# ---------------------------------------------------------------- controllo finale: nessun vecchio indirizzo
for root, dirs, files in os.walk(SITE):
    dirs[:] = [d for d in dirs if not d.startswith(('.', '_'))]  # né .git né _sorgenti
    for f in files:
        if f.endswith(('.html', '.js', '.css', '.xml')) or f == 'LICENSE':
            p = os.path.join(root, f)
            s = io.open(p, encoding='utf-8').read()
            for old in (OLD_URL, 'href="/#', "data-open"):
                if old in s:
                    print('ATTENZIONE: %s in %s' % (old, os.path.relpath(p, SITE)))
print('ok')

# ---------------------------------------------------------------- passaggio finale: accessibilità, copia statica, sitemap, robots.txt
import subprocess  # noqa: E402
subprocess.run([sys.executable, os.path.join(GEN, 'finalize.py')], check=True)
