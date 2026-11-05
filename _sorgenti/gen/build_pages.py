#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera le pagine nuove della struttura: termini del precetto, tassi e verifiche, privacy, note legali.

Usano la stessa intestazione, la stessa barra e lo stesso piè di pagina delle guide (build_guides.py).
I numeri (tassi, casi di verifica, registro) e i testi di privacy e note legali non sono qui:
li scrivono nella pagina termini.js e info.js leggendo core.js, così si aggiornano da un solo file.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_guides import (BASE, CHI_SONO, CONTACT_SITO, FOOTER, G3, GUIDE, ICON_OUT, NEWSLETTER, NEWSLETTER_URL, PIVA, SITE, tidy,  # noqa: E402
                          VALUTAZIONE, VALUTAZIONE_CONSEGNA, VALUTAZIONE_PREZZO, VALUTAZIONE_REGIME, VALUTAZIONE_URL,
                          contact, head, nav, tail, write)

CONTACT = contact(CONTACT_SITO)

# Dati strutturati collegati: il sito e il titolare hanno un identificativo stabile (@id), richiamato da ogni pagina.
# La persona è descritta per intero nella pagina «Chi sono»; le altre pagine la richiamano.
SITO_ID = BASE + '/#sito'
PERSONA_ID = BASE + '/chi-sono/#avvocato'
AGG = '__AGGIORNATA__'  # data di ultima modifica della pagina: la scrive finalize.py, la stessa della sitemap


def crumbs_ld(name, path):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": BASE + path}]}


def intro(crumb, h1, text):
    """Apertura della pagina come nelle guide: titolo in Garamond, una parte evidenziata (<mark>), sottotitolo."""
    return '\n'.join([
        '<div class="wrap g-hero solo">',
        '  <div>',
        '    <nav class="crumbs" aria-label="Percorso"><a href="/">Home</a> <span>›</span> %s</nav>' % crumb,
        '    <h1 class="g-title">%s</h1>' % h1,
        '    <p class="g-lead">%s</p>' % text,
        '  </div>',
        '</div>',
    ])


def page(title, desc, path, og, ld, current, body, scripts, noscript=None, autore_box=False):
    kw = {} if noscript is None else {'noscript': noscript}
    if autore_box:  # in fondo al contenuto principale
        i = body.rindex('</main>')
        body = body[:i] + autore() + body[i:]
    ld = con_nodi(ld)
    return '\n'.join([
        head(title, desc, path, og, ld, og_type='website'),
        '<body>',
        nav(current),
        '',
        body.strip('\n'),
        '',
        CONTACT,
        '',
        FOOTER,
        tail(*scripts, **kw),
    ])


def con_nodi(ld):
    """Aggiunge al grafo il sito e, se la pagina non la descrive già per intero, la persona."""
    if '@graph' not in ld:
        return ld
    import json
    testo = json.dumps(ld)
    extra = [{"@type": "WebSite", "@id": SITO_ID, "name": "calcolaprecetti.it", "url": BASE + "/", "inLanguage": "it-IT",
              "publisher": {"@id": PERSONA_ID}}]
    if '"@id": "%s", "name"' % PERSONA_ID not in testo:
        extra.append({k: _person[k] for k in ("@type", "@id", "name", "jobTitle", "url", "memberOf", "workLocation")})
    return dict(ld, **{'@graph': ld['@graph'] + extra})


def autore():
    """Riquadro con chi cura la pagina e la data dell'ultima modifica (la scrive finalize.py)."""
    foto = ('<img src="%s" alt="" width="56" height="56" loading="lazy" decoding="async">' % PHOTO) if PHOTO else ''
    return ('<aside class="autore" aria-label="Chi cura la pagina">%s<p>A cura dell\'<a href="/chi-sono/">avv. %s</a>, '
            'con studio a %s e iscritto all\'Ordine degli Avvocati di %s.<span class="agg">Pagina aggiornata il '
            '<time datetime="__AGGIORNATA__">__AGGIORNATA_IT__</time>.</span></p></aside>\n' % (foto, NOME, STUDIO, FORO))


# =========================================================================== termini del precetto
T_PATH = '/termini-precetto/'
T_TITLE = 'Calcolo della scadenza del precetto: 10 e 90 giorni (artt. 480-481 c.p.c.)'
T_DESC = ('Calcolo gratuito dei termini del precetto: 10 giorni per adempiere, inizio dell\'esecuzione e 90 giorni di efficacia, '
          'con festivi e ricerca dei beni.')
SEND_T = '''    <aside class="send" aria-labelledby="sendTitle">
      <p class="send-l">Da mandare al cliente</p>
      <h2 id="sendTitle">Il cliente chiede cosa succede dopo la notifica?</h2>
      <p>Mandagli la guida: spiega i 10 e i 90 giorni senza gergo, a chi ha ricevuto il precetto e a chi l'ha fatto notificare, con le date calcolate sul suo caso. Aprila e copia il collegamento.</p>
      <ul>
        <li><a href="''' + G3 + '''">Precetto notificato: cosa succede adesso e cosa fare</a><span>Cosa può fare chi lo riceve, cosa deve fare chi lo ha notificato, quando parte il pignoramento.</span></li>
      </ul>
    </aside>
'''
T_BODY = '''
''' + intro('Termini del precetto', 'Termini del precetto: <mark>10 e 90 giorni</mark>',
            "Dalla data di notifica: quando scade il termine per adempiere, da quando si può iniziare l'esecuzione e fino a quando il precetto resta efficace, anche con la ricerca dei beni.") + '''

<main class="wrap page">
  <section class="answer" aria-label="In breve">
    <div class="answer-item">
      <span class="answer-lab">Termine per adempiere</span>
      <strong class="answer-val">10 giorni</strong>
      <span class="answer-note">Non meno di dieci dalla notifica (art. 480 c.p.c.). Prima l'esecuzione non può iniziare (art. 482).</span>
    </div>
    <div class="answer-item">
      <span class="answer-lab">Efficacia del precetto</span>
      <strong class="answer-val">90 giorni</strong>
      <span class="answer-note">Dalla notifica (art. 481 c.p.c.). Il termine si sospende con l'istanza di ricerca dei beni e con l'opposizione al precetto.</span>
    </div>
  </section>

  <section class="panel termini" id="termini" aria-labelledby="tTitle">
    <div class="termini-grid">
      <div>
        <h2 id="tTitle">Calcola i termini</h2>
        <p class="hint" style="margin-top:0">Indica la data di notifica: le scadenze compaiono mentre scrivi.</p>
        <div class="pair">
          <label class="field"><span class="label">Notificato il</span><input type="date" id="tNotifica"></label>
          <label class="field"><span class="label">Termine per adempiere</span><span class="money days"><input type="text" inputmode="numeric" id="tGiorni"><span class="sign">giorni</span></span></label>
        </div>
        <span class="hint">Per la PEC conta la ricevuta di consegna; per la posta, la consegna o la compiuta giacenza.</span>
        <label class="check" style="margin-top:12px"><input type="checkbox" id="tBis"><span>Ho presentato l'istanza di ricerca dei beni (art. 492-bis c.p.c.)</span></label>
        <div id="tBisFields" hidden>
          <div class="pair" style="margin-top:10px">
            <label class="field"><span class="label">Istanza presentata il</span><input type="date" id="tBisFrom"></label>
            <label class="field"><span class="label">Esito comunicato il</span><input type="date" id="tBisTo"></label>
          </div>
          <span class="hint">Esito: verbale delle ricerche, comunicazione di mancata esecuzione o rigetto. Se non è ancora arrivato, lascia vuoto.</span>
        </div>
      </div>
      <div class="termini-out">
        <p class="case-msg" id="tCase" hidden></p>
        <div class="warnings" id="tWarnings"></div>
        <p class="empty" id="tEmpty">Indica la data di notifica per vedere le scadenze.</p>
        <dl class="tlist" id="tOut" hidden></dl>
        <div class="cal" id="tActions" hidden>
          <div class="actions">
            <button type="button" class="btn btn-secondary" id="tIcs" data-conta="calendario">Scarica per il calendario</button>
            <a class="btn btn-secondary" id="tGcal" data-conta="calendario" target="_blank" rel="noopener noreferrer">Google Calendar</a>
            <a class="btn btn-secondary" id="tOutlook" data-conta="calendario" target="_blank" rel="noopener noreferrer">Outlook.com</a>
          </div>
          <p class="hint">Il file contiene entrambe le date e un promemoria sette giorni prima: sul computer aprilo dalla cartella dei download, sul telefono toccalo, e il calendario chiede conferma. I due collegamenti aprono invece il sito del servizio con la scadenza dei 90 giorni già compilata, da salvare con un clic: la data e il titolo dell'appuntamento vengono inviati a Google o a Microsoft.</p>
        </div>
        <p class="hint" id="tNote" hidden>Termini calcolati escludendo il giorno della notifica; se la scadenza cade di sabato o in un giorno festivo è prorogata al primo giorno non festivo (art. 155 c.p.c.). Il termine di 90 giorni non è soggetto alla sospensione feriale. Non sono considerate le festività locali né la sospensione per opposizione al precetto (art. 481, comma 2, c.p.c.).</p>
      </div>
    </div>
  </section>

  <article class="prose">
    <h2>Come si contano</h2>
    <p>Il giorno della notifica non si conta: i termini partono dal giorno successivo (art. 155, comma 1, c.p.c.). Per la notifica a mezzo PEC vale la ricevuta di avvenuta consegna; per quella a mezzo posta, la consegna del plico o il perfezionamento per compiuta giacenza.</p>
    <p>Se l'ultimo giorno cade di sabato o in un giorno festivo, la scadenza è prorogata al primo giorno non festivo (art. 155, commi 4 e 5, c.p.c.). Il calcolo considera le festività nazionali, non quelle del santo patrono.</p>

    <h2>Il termine per adempiere: 10 giorni</h2>
    <p>Il precetto intima di adempiere entro un termine non minore di dieci giorni (art. 480 c.p.c.): se nell'atto ne hai indicato uno più lungo, scrivilo nel calcolo. Prima della scadenza l'esecuzione non può iniziare (art. 482 c.p.c.), salvo che il presidente del tribunale, se c'è pericolo nel ritardo, autorizzi l'esecuzione immediata.</p>

    <h2>L'efficacia: 90 giorni</h2>
    <p>Se l'esecuzione non inizia entro novanta giorni dalla notifica, il precetto diventa inefficace (art. 481, comma 1, c.p.c.) e va notificato di nuovo. Il termine non è soggetto alla sospensione feriale.</p>
    <p>Se il debitore propone opposizione al precetto, il termine resta sospeso e riprende a decorrere a norma dell'art. 627 c.p.c. (art. 481, comma 2): questa sospensione il calcolo non la considera.</p>

    <h2>La ricerca dei beni con modalità telematiche</h2>
    <p>L'istanza ex art. 492-bis c.p.c. si presenta dopo la scadenza del termine per adempiere e sospende il termine di novanta giorni fino alla comunicazione dell'esito: il verbale delle ricerche, la comunicazione di mancata esecuzione o il rigetto. Nel calcolo spunta l'opzione e indica le due date. Se l'esito non è ancora arrivato, lascia vuota la seconda: vedrai quanti giorni resteranno dalla comunicazione.</p>

''' + (SEND_T if GUIDE else '') + '''
    <h2>Le somme da intimare</h2>
    <p>Prima della notifica, il <a href="/">calcolo delle somme del precetto</a> prepara il prospetto: capitale, interessi, spese liquidate nel titolo, acconti e compenso per l'atto, con la tabella pronta da incollare in Word.</p>
  </article>
</main>
'''
T_LD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebApplication", "name": "Termini del precetto", "url": BASE + T_PATH, "isPartOf": {"@id": SITO_ID},
     "author": {"@id": PERSONA_ID}, "dateModified": AGG,
     "description": "Calcolo dei termini del precetto: 10 giorni per adempiere, inizio dell'esecuzione e 90 giorni di efficacia, "
                    "con la proroga dei festivi e la sospensione per la ricerca dei beni.",
     "applicationCategory": "BusinessApplication", "operatingSystem": "Tutti", "inLanguage": "it-IT", "isAccessibleForFree": True,
     "browserRequirements": "Richiede JavaScript", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
    crumbs_ld('Termini del precetto', T_PATH)]}


# =========================================================================== tassi, fonti e verifiche
X_PATH = '/tassi/'
X_TITLE = 'Tassi legali e moratori: tabelle, fonti e verifiche'
X_DESC = ('Le tabelle usate dai calcoli: interessi legali dal 1997, moratori dal 2002 e compenso del precetto (D.M. 147/2022), '
          'con le fonti e i casi di verifica.')
NOTIFY = '''  <p class="notify">Vuoi sapere quando cambiano? <a href="/newsletter/">Iscriviti alla newsletter: avvisi sui tassi e un consiglio pratico ogni due settimane</a></p>
'''
X_BODY = '''
''' + intro('Tassi e verifiche', 'Tassi, fonti e <mark>verifiche</mark>',
            'Le tabelle e i criteri usati dai calcoli del sito, con la fonte di ogni valore. Per controllare i risultati ci sono quattro casi svolti a mano, da aprire direttamente nel calcolo.') + '''

<main class="wrap page">
  <section class="answer" aria-label="Tassi in vigore">
    <div class="answer-item">
      <span class="answer-lab">Interesse legale <span id="nowLegalYear"></span></span>
      <strong class="answer-val" id="nowLegal">—</strong>
      <span class="answer-note" id="nowLegalSrc">Decreto del Ministro dell'economia (art. 1284 c.c.).</span>
    </div>
    <div class="answer-item">
      <span class="answer-lab">Interessi moratori, <span id="nowMoraSem">ultimo semestre pubblicato</span></span>
      <strong class="answer-val" id="nowMora">BCE + 8 punti</strong>
      <span class="answer-note" id="nowMoraSrc">Tasso di riferimento della BCE più otto punti (D.Lgs. 231/2002).</span>
    </div>
  </section>
''' + (NOTIFY if NEWSLETTER else '') + '''  <nav class="jump" aria-label="In questa pagina">
    <a href="#criteri">Criteri di calcolo</a>
    <a href="#legali">Interessi legali</a>
    <a href="#moratori">Interessi moratori</a>
    <a href="#compenso">Compenso del precetto</a>
    <a href="#verifica">Casi di verifica</a>
    <a href="#registro">Registro</a>
  </nav>

  <article class="prose">
    <section id="criteri" aria-labelledby="hCriteri">
      <h2 id="hCriteri">Come calcola il sito</h2>
      <ul class="crit">
        <li><strong>Interessi</strong> su 365 giorni, per periodi: anno solare per i legali, semestre per i moratori. Ogni periodo è arrotondato al centesimo; il primo e l'ultimo giorno sono compresi. Gli interessi sono semplici: non si calcolano interessi sugli interessi.</li>
        <li><strong>Acconti</strong> imputati ex art. 1194 c.c.: prima alle spese liquidate nel titolo, poi agli interessi maturati, infine al capitale; con più voci, prima alla più antica (art. 1193 c.c.). Dal giorno dopo l'acconto gli interessi maturano sul capitale residuo.</li>
        <li><strong>Compenso del precetto</strong> secondo i parametri del D.M. 55/2014, con i valori del D.M. 147/2022, sullo scaglione del credito residuo: capitale, interessi e spese, al netto degli acconti. Rimborso forfettario sui compensi, C.P.A. su compensi e rimborso, I.V.A. sul totale.</li>
        <li><strong>Termini del precetto</strong> calcolati escludendo il giorno della notifica; le scadenze che cadono di sabato o in un giorno festivo nazionale sono prorogate al primo giorno non festivo (art. 155 c.p.c.).</li>
      </ul>
    </section>

    <section id="legali" aria-labelledby="hLegali">
      <h2 id="hLegali">Interessi legali</h2>
      <p>Il tasso è fissato ogni anno con decreto del Ministro dell'economia e delle finanze, pubblicato in Gazzetta Ufficiale entro il 15 dicembre dell'anno precedente (art. 1284, comma 1, c.c.).</p>
      <div class="scroll"><table class="det rates" id="tabLegali"></table></div>
      <p class="tab-note">Dalla domanda giudiziale, se le parti non hanno fissato la misura degli interessi, si applica il tasso delle transazioni commerciali (art. 1284, comma 4, c.c.): nel calcolo delle somme è la voce «Legali, poi maggiorati dalla domanda».</p>
    </section>

    <section id="moratori" aria-labelledby="hMoratori">
      <h2 id="hMoratori">Interessi moratori</h2>
      <p>Tasso di riferimento della BCE in vigore il primo giorno del semestre, comunicato dal Ministero dell'economia in Gazzetta Ufficiale, più otto punti per i contratti conclusi dal 1° gennaio 2013 e più sette per quelli conclusi prima, dall'8 agosto 2002 (D.Lgs. 231/2002). Per i prodotti agricoli e alimentari si aggiungono altri quattro punti: il calcolo con tutte le opzioni è nella pagina <a href="/interessi-moratori/">Calcolo interessi moratori</a>.</p>
      <div class="scroll"><table class="det rates" id="tabMora"></table></div>
    </section>

    <section id="compenso" aria-labelledby="hCompenso">
      <h2 id="hCompenso">Compenso del precetto</h2>
      <p>Valori medi dei parametri forensi per l'atto di precetto (D.M. 55/2014, aggiornato dal D.M. 147/2022), per scaglione di valore del credito. Il minimo e il massimo sono il valore medio ridotto o aumentato del 50% (art. 4, comma 1).</p>
      <div class="scroll"><table class="det rates" id="tabPrecetto"></table></div>
      <p class="tab-note">Sul compenso si aggiungono <span class="js-accessori">rimborso forfettario, C.P.A. e, se dovuta, I.V.A.</span>.</p>
    </section>

    <section id="verifica" aria-labelledby="hVerifica">
      <h2 id="hVerifica">Casi di verifica</h2>
      <p>Conteggi svolti a mano con i tassi delle tabelle qui sopra. Aprili nel calcolo e confronta il risultato: se qualcosa non torna, scrivimi.</p>
      <div id="casiBody" data-url-precetto="/" data-url-termini="/termini-precetto/"></div>
    </section>

    <section id="registro" aria-labelledby="hRegistro">
      <h2 id="hRegistro">Registro degli aggiornamenti</h2>
      <p>Ogni modifica ai tassi, alle tabelle o ai criteri di calcolo, con la data in cui è stata pubblicata sul sito.</p>
      <div id="registroBody"></div>
    </section>
  </article>
</main>
'''
X_LD = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "name": "Tassi, fonti e verifiche", "url": BASE + X_PATH, "description": X_DESC, "inLanguage": "it-IT",
     "isPartOf": {"@id": SITO_ID}, "author": {"@id": PERSONA_ID}, "dateModified": AGG},
    crumbs_ld('Tassi e verifiche', X_PATH)]}


# =========================================================================== privacy e note legali
NOSCRIPT_TEXT = 'Il testo si carica con JavaScript: attivalo nel browser, oppure scrivi a info@calcolaprecetti.it per riceverlo.'
P_PATH = '/privacy/'
P_BODY = intro('Privacy', 'Informativa <mark>privacy</mark>',
               'Come vengono trattati i dati di chi usa il sito. In breve: nessun cookie, i dati dei calcoli restano sul tuo dispositivo '
               'e le visite si contano solo in forma aggregata.') + '''

<main class="wrap page">
  <article class="prose legal-page" id="privacyBody"''' + (' data-newsletter="1"' if NEWSLETTER else '') + (' data-valutazione="1"' if VALUTAZIONE else '') + '''><noscript><p>''' + NOSCRIPT_TEXT + '''</p></noscript></article>
</main>
'''
L_PATH = '/note-legali/'
L_BODY = intro('Note legali', 'Note <mark>legali</mark>', "Chi cura il sito, i limiti dello strumento e i diritti d'autore.") + '''

<main class="wrap page">
  <article class="prose legal-page" id="legalBody"''' + (' data-valutazione="1"' if VALUTAZIONE else '') + '''><noscript><p>''' + NOSCRIPT_TEXT + '''</p></noscript></article>
</main>
'''


# =========================================================================== chi sono (variante «sito unico»)
def ph(t):
    return '<span class="ph">[%s]</span>' % t


C_PATH = '/chi-sono/'
NOME = 'Alessandro Moro'
FORO = 'Vicenza'
LINKEDIN_PERSONALE = 'https://www.linkedin.com/in/alessandro-moro-524b7115a/'
STUDIO = 'Bassano del Grappa'  # città dello studio: titoli, testi e dati strutturati
STUDIO_A = STUDIO + ' (VI)'
C_TITLE = 'Avv. %s, avvocato a %s (VI)' % (NOME, STUDIO)
C_DESC = 'Avv. %s, avvocato a %s del Foro di %s: recupero crediti, chi cura calcolaprecetti.it e come scrivergli.' % (NOME, STUDIO, FORO)
PHOTO = '/assets/foto.jpg' if os.path.exists(os.path.join(SITE, 'assets', 'foto.jpg')) else None
C_PHOTO = ('<img class="chi-photo" src="%s" alt="Avv. %s" width="112" height="112">' % (PHOTO, NOME) if PHOTO else
           '<div class="chi-photo" role="img" aria-label="Spazio per la foto"><span>Foto</span></div>')
C_LINKEDIN = ('<a href="%s" target="_blank" rel="noopener noreferrer">Il mio profilo</a>' % LINKEDIN_PERSONALE
              if LINKEDIN_PERSONALE else ph('collegamento al profilo'))
VAL_CHI = ('      <p>Se hai un credito da recuperare, nella pagina <a href="/recupero-crediti/" data-conta="recupero-da-chi">Recupero crediti a Vicenza e Bassano del Grappa</a> '
           'trovi come lavoro; se prima vuoi un parere scritto, c\'è la <a href="/valutazione-credito/">valutazione del credito</a>.</p>\n')
NL_CHI = ('      <p>Ogni due settimane scrivo un consiglio pratico sul recupero crediti: lo ricevi con la '
          '<a href="/newsletter/">newsletter</a>.</p>\n')
C_BODY = '\n'.join([
    '<div class="wrap g-hero solo">',
    '  <div>',
    '    <nav class="crumbs" aria-label="Percorso"><a href="/">Home</a> <span>›</span> Chi sono</nav>',
    '    <div class="chi-head">',
    '      ' + C_PHOTO,
    '      <div>',
    '        <h1 class="g-title">Avv. <mark>%s</mark></h1>' % NOME,
    '        <p class="g-lead">Avvocato a %s, del Foro di %s.</p>' % (STUDIO, FORO),
    '      </div>',
    '    </div>',
    '  </div>',
    '</div>',
]) + '''

<main class="wrap page">
  <div class="chi">
    <article class="prose">
      <p>calcolaprecetti.it è nato da un'esigenza che conosco bene: rifare a ogni precetto lo stesso conto, tra interessi da dividere per semestre, acconti da imputare e tabelle dei compensi. L'ho pensato come un aiuto per i colleghi: è gratuito, non chiede registrazioni e indica la fonte di ogni tasso.</p>
      <p>Nella mia attività di avvocato mi occupo, tra le altre materie, anche di recupero crediti. Per il mio percorso professionale ti rimando al mio <a href="''' + LINKEDIN_PERSONALE + '''" target="_blank" rel="noopener noreferrer">profilo LinkedIn</a>.</p>
''' + (VAL_CHI if VALUTAZIONE else '') + (NL_CHI if NEWSLETTER else '') + '''      <p>Se hai un'idea per migliorare il sito, o vuoi contattarmi per altro, scrivimi a <a href="mailto:info@calcolaprecetti.it">info@calcolaprecetti.it</a>: ti rispondo volentieri.</p>
    </article>
    <aside class="chi-card" aria-labelledby="hContatti">
      <h2 id="hContatti">Contatti</h2>
      <dl>
        <div><dt>Email</dt><dd><a href="mailto:info@calcolaprecetti.it">info@calcolaprecetti.it</a></dd></div>
        <div><dt>LinkedIn</dt><dd>''' + C_LINKEDIN + '''</dd></div>
        <div><dt>Studio</dt><dd>a ''' + STUDIO_A + '''</dd></div>
        <div><dt>Ordine</dt><dd>Ordine degli Avvocati di ''' + FORO + '''</dd></div>
      </dl>
    </aside>
  </div>
</main>
'''
_person = {"@type": "Person", "@id": PERSONA_ID, "name": NOME, "jobTitle": "Avvocato", "url": BASE + '/chi-sono/',
           "memberOf": {"@type": "Organization", "name": "Ordine degli Avvocati di " + FORO}}
if PHOTO:
    _person["image"] = BASE + PHOTO
if LINKEDIN_PERSONALE:
    _person["sameAs"] = [LINKEDIN_PERSONALE]
_person["workLocation"] = {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": "Bassano del Grappa",
                                                         "addressRegion": "VI", "addressCountry": "IT"}}
C_LD = {"@context": "https://schema.org", "@graph": [
    {"@type": "ProfilePage", "url": BASE + C_PATH, "inLanguage": "it-IT", "isPartOf": {"@id": SITO_ID}, "dateModified": AGG,
     "mainEntity": _person},
    crumbs_ld('Chi sono', C_PATH)]}


# =========================================================================== newsletter
N_PATH = '/newsletter/'
N_TITLE = 'Newsletter sul recupero crediti: un consiglio pratico ogni due settimane'
N_DESC = ("Ogni due settimane un consiglio pratico sul recupero crediti, scritto da un avvocato: precetto, notifiche, "
          "pignoramenti, interessi. In più gli avvisi quando cambiano il tasso legale e quello dei moratori. Gratuita.")
N_OG = "Un consiglio pratico sul recupero crediti ogni due settimane, più gli avvisi quando cambiano i tassi."
if NEWSLETTER_URL:
    N_BTN = ('<a class="btn btn-primary" href="%s" target="_blank" rel="noopener noreferrer" data-conta="iscrizione-newsletter">'
             'Iscriviti alla newsletter%s</a>' % (NEWSLETTER_URL, ICON_OUT))
else:  # anteprima: il modulo di Brevo non c'è ancora
    N_BTN = ('<a class="btn btn-primary" href="#iscriviti" data-conta="iscrizione-newsletter">Iscriviti alla newsletter</a>\n'
             '      <p class="ph-note">%s</p>' % ph('qui andrà il collegamento al modulo di iscrizione di Brevo'))
N_AUTORE = ('<a href="/chi-sono/">l\'avv. %s</a>' % NOME) if CHI_SONO else "l'avv. %s" % NOME
N_BODY = intro('Newsletter', 'Recupero crediti, <mark>ogni due settimane</mark>',
               "Un'email ogni due settimane con un consiglio pratico per recuperare i crediti senza errori, più gli avvisi "
               "quando cambiano i tassi. Si legge in tre minuti.") + """

<main class="wrap page">
  <div class="chi nl">
    <aside class="nl-card" id="iscriviti" aria-labelledby="hIscriviti">
      <p class="send-l">Iscrizione gratuita</p>
      <h2 id="hIscriviti">Ricevi la newsletter</h2>
      <p>Un'email ogni due settimane, più gli avvisi sui tassi. Ti cancelli quando vuoi.</p>
      """ + N_BTN + """
      <p class="hint">Si apre la pagina di iscrizione di Brevo, il servizio che spedisce le email.</p>
    </aside>
    <article class="prose">
      <h2>Cosa ricevi</h2>
      <ul class="crit">
        <li><strong>Ogni due settimane, un consiglio pratico</strong>: una regola da non sbagliare, un termine da tenere d'occhio, un errore frequente, un modo per risparmiare tempo.</li>
        <li><strong>Gli avvisi sui tassi</strong>: a metà dicembre il tasso legale dell'anno nuovo, a inizio gennaio e a inizio luglio quello degli interessi moratori, con i calcoli del sito già aggiornati.</li>
        <li><strong>Le novità del sito</strong>: calcoli nuovi e, quando ci saranno, guide e kit a pagamento.</li>
      </ul>
      <h2>Alcuni temi</h2>
      <ul class="crit">
        <li>Precetto alle imprese: quando la notifica via PEC è obbligatoria</li>
        <li>Pignoramento presso terzi: l'avviso di iscrizione a ruolo da non dimenticare</li>
        <li>I 40 euro di risarcimento forfettario: quando spettano e come chiederli</li>
        <li>Acconti ricevuti: come imputarli senza perdere interessi</li>
        <li>Ricerca dei beni con modalità telematiche: quando conviene chiederla</li>
        <li>Il debitore è fallito: come recuperare almeno l'IVA</li>
      </ul>
      <h2>Come funziona l'iscrizione</h2>
      <p>Ti iscrivi su una pagina di Brevo, il servizio che conserva l'elenco degli iscritti e spedisce le email. Scrivi il tuo indirizzo, ricevi un'email e confermi con un clic: senza la conferma non ricevi nulla. Ti cancelli quando vuoi, con il collegamento in fondo a ogni email. Il tuo indirizzo non viene ceduto a nessuno.</p>
      <p>La scrive """ + N_AUTORE + """, del Foro di """ + FORO + """. Come vengono trattati i dati lo trovi nell'<a href="/privacy/#newsletter">informativa privacy</a>.</p>
    </article>
  </div>
</main>
"""


# =========================================================================== valutazione del credito
V_PATH = '/valutazione-credito/'
V_TITLE = 'Valutazione del credito: parere scritto di un avvocato'
V_DESC = ("Dieci domande sul tuo credito, senza dire chi è il debitore: un avvocato ti dice per iscritto se regge, quanto vale "
          "e che strada conviene. Prezzo fisso.")
V_OG = "Un parere scritto e firmato da un avvocato su come recuperare il tuo credito, sui fatti che descrivi, a prezzo fisso."
def eur(x):  # 22.88 -> '22,88'
    return ('%.2f' % x).replace('.', ',')


V_GG = VALUTAZIONE_CONSEGNA
if VALUTAZIONE_PREZZO:  # importi calcolati dal compenso e dal regime fiscale
    _p = float(VALUTAZIONE_PREZZO)
    _cpa = round(_p * 0.04, 2)
    if VALUTAZIONE_REGIME == 'ordinario':
        _iva = round((_p + _cpa) * 0.22, 2)
        _tot = _p + _cpa + _iva
        V_FISCO = '%s € di IVA' % eur(_iva)
        V_FISCO_COND = 'più IVA del 22%% (%s €)' % eur(_iva)
    else:
        _bollo = 2.0 if _p + _cpa > 77.47 else 0.0
        _tot = _p + _cpa + _bollo
        V_FISCO = ('2,00 € di marca da bollo, senza IVA' if _bollo else 'senza IVA')
        V_FISCO_COND = ('più marca da bollo da 2 €, senza IVA' if _bollo else 'senza IVA')
    V_PREZZO = eur(_p)
    V_TOTALE = eur(_tot)
    V_NOTE = ('%s € di compenso più %s € di contributo previdenziale (C.P.A. 4%%), %s. Prezzo fisso, concordato prima di iniziare.'
              % (V_PREZZO, eur(_cpa), V_FISCO))
    V_COMPENSO = ('%s € più contributo previdenziale (C.P.A.) del 4%%, %s: in totale %s €, pagato in anticipo.'
                  % (V_PREZZO, V_FISCO_COND, V_TOTALE))
else:  # anteprima senza prezzo
    V_PREZZO = V_TOTALE = ph('prezzo')
    V_NOTE = 'più contributo previdenziale (C.P.A.) del 4% e, se dovuta, IVA. Prezzo fisso, concordato prima di iniziare.'
    V_COMPENSO = V_PREZZO + ' € più contributo previdenziale (C.P.A.) del 4% e, se dovuta, IVA, pagato in anticipo.'
if VALUTAZIONE_URL:
    V_BTN = ('<a class="btn btn-primary" href="%s" target="_blank" rel="noopener noreferrer" data-conta="inizia-valutazione">'
             'Inizia la valutazione%s</a>' % (VALUTAZIONE_URL, ICON_OUT))
else:  # anteprima: il questionario su Tally non c'è ancora
    V_BTN = ('<a class="btn btn-primary" href="#richiedi" data-conta="inizia-valutazione">Inizia la valutazione</a>\n'
             '      <p class="ph-note">%s</p>' % ph('qui andrà il collegamento al questionario su Tally'))
V_AUTORE = ('<a href="/chi-sono/">avv. %s</a>' % NOME) if CHI_SONO else 'avv. %s' % NOME
V_BODY = intro('Valutazione del credito', 'Valutazione del <mark>credito</mark>',
               "Rispondi a dieci domande sul tuo credito, senza dirmi chi è il debitore: entro " + V_GG + " ricevi un "
               "parere scritto e firmato da un avvocato su come recuperarlo, con costi e tempi stimati.") + """

<main class="wrap page">
  <div class="chi svc">
    <aside class="svc-card" id="richiedi" aria-labelledby="hRichiedi">
      <p class="send-l" id="hRichiedi">Parere scritto e firmato</p>
      <p class="svc-price">""" + V_TOTALE + """ €</p>
      <p class="svc-note">""" + V_NOTE + """</p>
      <ul class="svc-list">
        <li>Consegna entro """ + V_GG + """ dal pagamento</li>
        <li>Non servono nomi né dati del debitore: bastano i fatti</li>
        <li>Se poi mi <a href="/recupero-crediti/" data-conta="recupero-da-valutazione">affidi il recupero</a>, il costo del parere viene scalato dal compenso</li>
      </ul>
      """ + V_BTN + """
      <p class="hint">Il questionario si apre su Tally, il servizio che raccoglie le risposte. Si paga con carta, tramite Stripe.</p>
    </aside>
    <article class="prose">
      <h2>Cosa ricevi</h2>
      <p>Un parere scritto, in PDF, firmato da me, che risponde a cinque domande.</p>
      <ul class="crit">
        <li><strong>Il credito regge?</strong> Prova scritta, prescrizione, eventuali contestazioni del debitore.</li>
        <li><strong>Quanto vale oggi?</strong> Capitale, interessi, risarcimento forfettario di 40 € dove spetta, spese.</li>
        <li><strong>Quale strada conviene?</strong> Diffida, decreto ingiuntivo, insinuazione al passivo o accordo con il debitore.</li>
        <li><strong>Quanto costa e quanto ci vuole?</strong> Una stima delle spese e dei tempi della strada indicata.</li>
        <li><strong>Quante probabilità ci sono di incassare?</strong> In base a quello che mi dici della situazione del debitore.</li>
      </ul>
      <p>Il parere si basa sui fatti che descrivi: non esamino documenti e non faccio ricerche sul debitore. Più la descrizione è precisa, più il parere è utile. Non è una garanzia di risultato.</p>
      <figure class="svc-fac">
        <img src="/assets/facsimile-parere.webp" width="640" height="905" loading="lazy" decoding="async" alt="Facsimile della prima pagina di un parere: intestazione, titolo, sintesi e le prime quattro domande, con i dati del caso sfocati">
        <figcaption>Facsimile della prima pagina. Le parti sfocate cambiano da caso a caso.</figcaption>
      </figure>

      <h2>Come funziona</h2>
      <ol class="steps">
        <li><strong>Rispondi a dieci domande.</strong> Sul credito e sulla situazione del debitore, senza indicare chi è: bastano i fatti. Servono una decina di minuti.</li>
        <li><strong>Accetti le condizioni e paghi.</strong> In fondo al questionario leggi le condizioni del parere, le accetti con le caselle e paghi con carta. Ricevi subito la ricevuta del pagamento e, prima che inizi il lavoro, un'email di conferma con le condizioni.</li>
        <li><strong>Ricevi il parere.</strong> Entro """ + V_GG + """ dal pagamento, in PDF firmato, per email, con la fattura.</li>
      </ol>

      <h2>Cosa ti chiedo</h2>
      <ul class="crit">
        <li>che tipo di debitore è (privato, impresa o ente pubblico) e dove si trova;</li>
        <li>quanto ti deve, da dove nasce il credito e quando doveva pagare;</li>
        <li>quali documenti hai;</li>
        <li>cosa hai già fatto per recuperarlo e come ha reagito il debitore;</li>
        <li>le garanzie, come fideiussioni o assegni;</li>
        <li>cosa sai della sua situazione: lavoro, immobili, attività;</li>
        <li>cosa vuoi sapere soprattutto;</li>
        <li>i tuoi dati per la fattura.</li>
      </ul>
      <p>Non ti chiedo nomi né dati del debitore, e ti chiedo di non scriverli.</p>

      <h2>Domande frequenti</h2>
      <h3>Perché non mi chiedi chi è il debitore?</h3>
      <p>Perché il parere riguarda i fatti, non le persone: così non mi passi dati di altri. Se poi decidi di affidarmi il recupero, il nome mi serve per verificare i conflitti di interessi e per agire.</p>
      <h3>Il parere mi impegna ad affidarti il recupero?</h3>
      <p>No. È un parere a sé: decidi tu cosa fare dopo.</p>
      <h3>Mi puoi garantire che recupererò il credito?</h3>
      <p>No. Il parere ti dice quanto è probabile incassare e quanto costa provarci, così decidi con i numeri davanti.</p>
      <h3>E le visure sul debitore?</h3>
      <p>Per farle bisogna sapere chi è il debitore, quindi non rientrano nel parere. Se mi affidi il recupero, valutiamo insieme se servono.</p>
      <h3>Chi legge le mie risposte?</h3>
      <p>Solo io. Le raccoglie e le conserva per mio conto Tally, società con sede in Belgio e server in Europa, e sono coperte dal segreto professionale.</p>
    </article>
  </div>
</main>
"""


# =========================================================================== condizioni del parere (pagina propria, collegata dal piè di pagina)
K_PATH = '/condizioni-parere/'
K_DESC = ("Condizioni della valutazione del credito: oggetto del parere, compenso, tempi, recesso, "
          "dati personali e informazioni dovute dall'avvocato.")
K_BODY = intro('<a href="/valutazione-credito/">Valutazione del credito</a> <span>›</span> Condizioni del parere', 'Condizioni del <mark>parere</mark>',
               "Sono le condizioni della valutazione del credito, che accetti in fondo al questionario prima di pagare.") + """

<main class="wrap page">
  <article class="prose legal-page" aria-label="Condizioni del parere">
    <ol class="terms">
      <li><strong>Oggetto.</strong> Parere scritto sui fatti descritti nel questionario. Non comprende l'esame di documenti, ricerche sul debitore, contatti con lui, diffide, atti giudiziari o altre attività. Chiedere il parere non significa conferirmi un mandato ad agire per tuo conto.</li>
      <li><strong>A chi è rivolto.</strong> A privati e piccole imprese. Per banche, assicurazioni, enti pubblici e imprese con più di 50 dipendenti o ricavi annui oltre 10 milioni di euro preparo un preventivo su misura: se la richiesta arriva da uno di loro, rimborso per intero quanto pagato.</li>
      <li><strong>Compenso.</strong> """ + V_COMPENSO + """ La fattura elettronica è emessa alla data del pagamento. Se entro sei mesi mi affidi il recupero dello stesso credito, il compenso del parere è scalato da quello del recupero.</li>
      <li><strong>Tempi.</strong> Il parere è consegnato entro """ + V_GG + """ dal pagamento. Se servono chiarimenti, il termine decorre dalla tua risposta.</li>
      <li><strong>Fatti descritti.</strong> Il parere vale per i fatti così come li descrivi, che dichiari veri e completi per quanto ti risulta. Se i fatti sono diversi, le conclusioni possono cambiare.</li>
      <li><strong>Conflitto di interessi.</strong> Non conosco il nome del debitore. Se dai fatti riconosco una persona che assisto, non posso rendere il parere e ti rimborso per intero. Se poi mi affidi il recupero, verifico i conflitti prima di accettare.</li>
      <li><strong>Recesso.</strong> Se sei un consumatore puoi recedere entro 14 giorni dalla richiesta, scrivendo a <a href="mailto:info@calcolaprecetti.it">info@calcolaprecetti.it</a>: basta una dichiarazione esplicita, oppure il modulo tipo di recesso che trovi nell'email di conferma. Se chiedi di iniziare subito, dopo la consegna del parere il recesso non è più possibile (art. 59, comma 1, lett. a, Codice del consumo); se recedi prima, ti rimborso il compenso trattenendo solo un importo proporzionale all'attività già svolta.</li>
      <li><strong>Informazioni dovute dall'avvocato.</strong> Gli estremi della mia polizza per la responsabilità professionale te li indico nell'email di conferma. Per le controversie sul credito esistono strumenti alternativi al giudizio, come la mediazione e la negoziazione assistita, di cui il parere tiene conto; per le cause, chi ha i requisiti di reddito può chiedere il patrocinio a spese dello Stato.</li>
      <li><strong>Dati personali.</strong> Tratto i tuoi dati come descritto nell'<a href="/privacy/#valutazione">informativa privacy</a>, nel rispetto del segreto professionale. Non inserire nomi o dati del debitore o di altre persone.</li>
      <li><strong>Avvocato.</strong> """ + V_AUTORE + """, iscritto all'Ordine degli Avvocati di """ + FORO + """, P.IVA """ + PIVA + """, studio a """ + STUDIO_A + """.</li>
    </ol>
    <p class="hint">Per chiedere il parere: <a href="/valutazione-credito/">Valutazione del credito</a>.</p>
  </article>
</main>
"""


# =========================================================================== recupero crediti (servizio, parte «Per i creditori»)
R_PATH = '/recupero-crediti/'
R_LUOGO = 'Vicenza e Bassano del Grappa'  # dove si cerca un avvocato per il recupero crediti: titolo, intestazione, rimandi
R_TITLE = 'Avvocato recupero crediti a ' + R_LUOGO
R_DESC = ('Avvocato a Bassano del Grappa, Foro di Vicenza: recupero crediti per imprese, professionisti e privati, dalla '
          'diffida al pignoramento. Preventivo scritto.')
R_OG = ('Recupero crediti a ' + R_LUOGO + ' per imprese, professionisti e privati: diffida, decreto ingiuntivo, precetto '
        'e pignoramento.')
R_BODY = intro('Recupero crediti', '<mark>Recupero crediti</mark> a ' + R_LUOGO,
               "Sono avvocato a Bassano del Grappa, iscritto all'Ordine di Vicenza. Assisto imprese, professionisti e privati "
               "che devono recuperare un credito: dalla lettera di diffida al decreto ingiuntivo, fino al precetto e al "
               "pignoramento. Prima di iniziare ricevi un preventivo scritto.") + """

<main class="wrap page">
  <div class="chi svc">
    <aside class="svc-card" id="affida" aria-labelledby="hAffida">
      <p class="send-l" id="hAffida">Affidami il recupero</p>
      <p class="svc-lead">Scrivimi chi sei, quanto ti devono e da quando, e chi è il debitore: il nome mi serve per verificare che non ci siano conflitti di interessi.</p>
      <ul class="svc-list">
        <li>Preventivo scritto prima di iniziare</li>
        <li>Studio a """ + STUDIO_A + """</li>
        <li>Anche a distanza: atti, depositi e notifiche sono telematici</li>
      </ul>
      <a class="btn btn-primary" href="mailto:info@calcolaprecetti.it?subject=Recupero%20crediti" data-conta="contatto-recupero">Scrivimi un'email</a>
      <p class="svc-mail" aria-live="polite">Il pulsante apre il programma di posta. Se usi la posta nel browser, scrivi a <a href="mailto:info@calcolaprecetti.it?subject=Recupero%20crediti" data-conta="contatto-recupero">info@calcolaprecetti.it</a> <button type="button" class="linkbtn" data-copia="info@calcolaprecetti.it" data-conta="copia-email-recupero">Copia l'indirizzo</button></p>
      <p class="hint">Nel primo messaggio non servono documenti: se servono, te li chiedo io.</p>
      <p class="svc-alt">Vuoi prima sapere se conviene? Con la <a href="/valutazione-credito/" data-conta="valutazione-da-recupero">valutazione del credito</a> ricevi un parere scritto a prezzo fisso, senza dirmi chi è il debitore.</p>
    </aside>
    <article class="prose">
      <h2>Per chi</h2>
      <ul class="crit">
        <li><strong>Imprese e professionisti</strong> con fatture non pagate da altre imprese o da enti pubblici: oltre al capitale spettano gli interessi moratori (tasso BCE più 8 punti) e 40 € di risarcimento forfettario (D.Lgs. 231/2002). Puoi calcolarli con lo strumento degli <a href="/interessi-moratori/">interessi moratori</a>.</li>
        <li><strong>Professionisti</strong> con compensi non pagati da clienti privati.</li>
        <li><strong>Privati</strong>: prestiti, canoni di locazione, somme riconosciute da una sentenza o da un accordo.</li>
      </ul>

      <h2>Come si recupera un credito</h2>
      <p class="tl-nota">Le fasi, una dopo l'altra, con i tempi di ciascuna. Sono indicativi: dipendono dal debitore, dal tribunale e da cosa si riesce a pignorare. Se il debitore paga dopo la diffida, ci si ferma lì.</p>
      <ol class="tl">
        <li><span class="tl-t">Valutazione</span><span class="tl-q">Pochi giorni dai documenti</span>
          <span class="tl-d">Guardo i documenti: prova scritta del credito, scadenze, prescrizione, eventuali contestazioni. E cosa si sa del debitore, perché un credito vale quanto la possibilità di incassarlo.</span></li>
        <li><span class="tl-t">Diffida</span><span class="tl-q">Termine per pagare: di solito 10–15 giorni</span>
          <span class="tl-d">Una lettera dell'avvocato con un termine per pagare: mette in mora il debitore e interrompe la prescrizione.</span></li>
        <li><span class="tl-t">Decreto ingiuntivo</span><span class="tl-q">Da qualche settimana a qualche mese, secondo il tribunale; poi 40 giorni per l'opposizione</span>
          <span class="tl-d">Se il debitore non paga e c'è una prova scritta del credito, il giudice ordina il pagamento senza udienza. In alcuni casi il decreto è esecutivo subito.</span></li>
        <li><span class="tl-t">Precetto</span><span class="tl-q">10 giorni per pagare; il pignoramento va iniziato entro 90 giorni</span>
          <span class="tl-d">Con il titolo esecutivo (sentenza, decreto ingiuntivo esecutivo, assegno o cambiale) si intima al debitore di pagare (artt. 480 e 481 c.p.c.). Le somme e le scadenze le calcolo con gli <a href="/">strumenti di questo sito</a>.</span></li>
        <li><span class="tl-t">Pignoramento</span><span class="tl-q">Da alcuni mesi, per conti e stipendi, a qualche anno, per gli immobili</span>
          <span class="tl-d">Pignoramento del conto corrente, dello stipendio o di altri crediti verso terzi, di beni mobili o immobili. I beni si possono cercare anche nelle banche dati pubbliche (art. 492-bis c.p.c.).</span></li>
        <li class="tl-fine"><span class="tl-t">Incasso</span><span class="tl-q">Alla fine della procedura; lo stipendio a rate mensili</span>
          <span class="tl-d">Nel pignoramento presso terzi paga direttamente chi doveva le somme al debitore, come la banca o il datore di lavoro; se si vendono beni, si incassa il ricavato della vendita.</span></li>
      </ol>
      <p>Se il debitore è insolvente e si apre una procedura come la liquidazione giudiziale, il credito si fa valere con la domanda di ammissione al passivo.</p>

      <h2>Costi</h2>
      <ul class="crit">
        <li>Prima di iniziare ricevi un preventivo scritto, con compenso, spese e contributi indicati separatamente.</li>
        <li>Le spese liquidate nel decreto ingiuntivo e quelle del precetto sono a carico del debitore: se paga, le recuperi; se non paga, restano a carico tuo.</li>
        <li>Se prima hai chiesto la <a href="/valutazione-credito/">valutazione del credito</a>, il costo del parere viene scalato dal compenso.</li>
        <li>L'incasso non si può garantire: dipende da chi è il debitore e da cosa possiede. Prima di iniziare ti dico cosa è realistico aspettarsi.</li>
      </ul>

      <h2>A Vicenza, a Bassano del Grappa e fuori provincia</h2>
      <p>Lo studio è a """ + STUDIO_A + """ e sono iscritto all'Ordine degli Avvocati di """ + FORO + """: seguo il recupero crediti di imprese, professionisti e privati di Bassano, di Vicenza e della provincia.</p>
      <p>Per Bassano del Grappa il tribunale è oggi quello di Vicenza, che nel 2013 ha assorbito quello di Bassano.</p>
      <p>Spesso il credito si può far valere qui anche se il debitore sta altrove: quando la somma è già determinata, per esempio un prezzo concordato, il pagamento va fatto al domicilio del creditore, e il decreto ingiuntivo si può chiedere al giudice di quel luogo (art. 1182 c.c. e art. 20 c.p.c.). Se il debitore è un consumatore, invece, è competente il giudice del luogo in cui abita.</p>
      <p>Seguo pratiche anche fuori provincia: atti, depositi e notifiche sono telematici e ci si può sentire a distanza.</p>
    </article>
  </div>
</main>
"""


# =========================================================================== valutazione: pagina dopo il questionario (Tally vi reindirizza)
# Non indicizzata: serve a contare in Umami le richieste completate (pagina vista /valutazione-credito/grazie/).
Y_PATH = '/valutazione-credito/grazie/'
Y_DESC = 'Richiesta di valutazione del credito ricevuta: cosa succede adesso.'
Y_BODY = intro('<a href="/valutazione-credito/">Valutazione del credito</a> <span>›</span> Richiesta ricevuta',
               'Richiesta <mark>ricevuta</mark>', 'Grazie: ho ricevuto la richiesta e il pagamento.') + """

<main class="wrap page">
  <article class="prose">
    <p>Entro """ + V_GG + """ dal pagamento ti mando un'email con il parere e la valutazione del tuo credito, in PDF firmato, insieme alla fattura.</p>
    <p>Per qualsiasi domanda scrivimi a <a href="mailto:info@calcolaprecetti.it">info@calcolaprecetti.it</a>. Anche nei messaggi, non indicare nomi o dati del debitore.</p>
    <p>avv. """ + NOME + """</p>
    <p class="after"><a href="/recupero-crediti/" data-conta="recupero-da-grazie">Come lavoro se poi mi affidi il recupero</a></p>
  </article>
</main>
"""


# =========================================================================== pagina «non trovata» (404.html)
# GitHub Pages la mostra per ogni indirizzo che non esiste: tutti i collegamenti sono assoluti.
E_DESC = "L'indirizzo che hai aperto non esiste o è cambiato: ecco le pagine di calcolaprecetti.it."
E_BODY = intro('Pagina non trovata', 'Pagina <mark>non trovata</mark>',
               "L'indirizzo che hai aperto non esiste o è cambiato. Puoi ripartire da una di queste pagine.") + '''

<main class="wrap page">
  <article class="prose">
    <ul class="crit">
      <li><a href="/">Calcolo delle somme del precetto</a></li>
      <li><a href="/termini-precetto/">Termini del precetto: 10 e 90 giorni</a></li>
      <li><a href="/interessi-moratori/">Calcolo degli interessi moratori</a></li>
      <li><a href="/tassi/">Tassi e verifiche</a></li>
      <li><a href="/recupero-crediti/">Recupero crediti</a></li>
''' + ('      <li><a href="/valutazione-credito/">Valutazione del credito</a></li>\n' if VALUTAZIONE else '') + ('      <li><a href="/chi-sono/">Chi sono</a></li>\n' if CHI_SONO else '') + '''    </ul>
  </article>
</main>
'''


def simple_ld(name, path, desc):
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": name, "url": BASE + path, "description": desc, "inLanguage": "it-IT", "isPartOf": {"@id": SITO_ID}},
        crumbs_ld(name, path)]}


if __name__ == '__main__':
    P_DESC = ('Informativa privacy di calcolaprecetti.it: nessun cookie, i dati dei calcoli restano nel browser, statistiche delle visite'
              + (', newsletter' if NEWSLETTER else '') + ' e valutazione del credito.')
    L_DESC = "Note legali di calcolaprecetti.it: titolare del sito, limiti dello strumento di calcolo e diritti d'autore."
    pages = [
        (T_PATH, page(T_TITLE, T_DESC, T_PATH, 'I 10 e i 90 giorni del precetto, con la proroga dei festivi e la sospensione per la ricerca dei beni.',
                      T_LD, 'termini', T_BODY, ['termini.js'], autore_box=True)),
        (X_PATH, page(X_TITLE, X_DESC, X_PATH, 'Interessi legali e moratori, compenso del precetto: le tabelle del sito con le fonti e i casi di verifica.',
                      X_LD, 'tassi', X_BODY, ['info.js'], autore_box=True)),
        (P_PATH, page('Informativa privacy – calcolaprecetti.it', P_DESC, P_PATH, P_DESC, simple_ld('Informativa privacy', P_PATH, P_DESC),
                      'altro', P_BODY, ['info.js'], noscript='')),
        (L_PATH, page('Note legali – calcolaprecetti.it', L_DESC, L_PATH, L_DESC, simple_ld('Note legali', L_PATH, L_DESC),
                      'altro', L_BODY, ['info.js'], noscript='')),
    ]
    if CHI_SONO:
        pages.append((C_PATH, page(C_TITLE, C_DESC, C_PATH, C_DESC, C_LD,
                                   'chi', C_BODY, ['info.js'], noscript='')))  # info.js: piè di pagina e contatti
    if VALUTAZIONE:
        V_SERVIZIO = {"@type": "Service", "@id": BASE + V_PATH + '#servizio', "name": "Valutazione del credito",
                      "serviceType": "Parere scritto di un avvocato sul recupero di un credito", "description": V_DESC,
                      "url": BASE + V_PATH, "provider": {"@id": PERSONA_ID}, "areaServed": {"@type": "Country", "name": "Italia"}}
        if VALUTAZIONE_PREZZO:
            V_SERVIZIO["offers"] = {"@type": "Offer", "price": V_TOTALE.replace(',', '.'), "priceCurrency": "EUR", "url": BASE + V_PATH}
        V_LD = {"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "name": "Valutazione del credito", "url": BASE + V_PATH, "description": V_DESC, "inLanguage": "it-IT",
             "isPartOf": {"@id": SITO_ID}, "dateModified": AGG, "mainEntity": {"@id": BASE + V_PATH + '#servizio'}},
            V_SERVIZIO, crumbs_ld('Valutazione del credito', V_PATH)]}
        pages.append((V_PATH, page(V_TITLE, V_DESC, V_PATH, V_OG, V_LD,
                                   'valutazione', V_BODY, ['info.js'], noscript='', autore_box=True)))
        pages.append((K_PATH, page('Condizioni del parere – calcolaprecetti.it', K_DESC, K_PATH, K_DESC,
                                   simple_ld('Condizioni del parere', K_PATH, K_DESC), 'valutazione', K_BODY, ['info.js'], noscript='')))
    R_LD = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": "Recupero crediti a " + R_LUOGO, "url": BASE + R_PATH, "description": R_DESC, "inLanguage": "it-IT",
         "isPartOf": {"@id": SITO_ID}, "dateModified": AGG, "mainEntity": {"@id": BASE + R_PATH + '#servizio'}},
        {"@type": "Service", "@id": BASE + R_PATH + '#servizio', "name": "Recupero crediti",
         "serviceType": "Assistenza legale per il recupero crediti", "description": R_DESC, "url": BASE + R_PATH,
         "provider": {"@id": PERSONA_ID},
         "areaServed": [{"@type": "City", "name": "Bassano del Grappa"}, {"@type": "City", "name": "Vicenza"},
                        {"@type": "AdministrativeArea", "name": "Provincia di Vicenza"}, {"@type": "Country", "name": "Italia"}]},
        crumbs_ld('Recupero crediti', R_PATH)]}
    pages.append((R_PATH, page(R_TITLE, R_DESC, R_PATH, R_OG, R_LD,
                               'recupero', R_BODY, ['info.js'], noscript='', autore_box=True)))
    if VALUTAZIONE:  # pagina dopo il questionario: fuori dalla sitemap e non indicizzata
        y = page('Richiesta ricevuta – calcolaprecetti.it', Y_DESC, Y_PATH, Y_DESC, simple_ld('Richiesta ricevuta', Y_PATH, Y_DESC),
                 'valutazione', Y_BODY, ['info.js'], noscript='')
        canon_y = '<link rel="canonical" href="%s%s">\n' % (BASE, Y_PATH)
        assert y.count(canon_y) == 1
        pages.append((Y_PATH, y.replace(canon_y, '<meta name="robots" content="noindex">\n')))
    import shutil
    for flag, folder in ((NEWSLETTER, 'newsletter'), (VALUTAZIONE, 'valutazione-credito'), (VALUTAZIONE, 'condizioni-parere')):
        if not flag:  # funzione spenta: nel sito non resta la sua pagina
            shutil.rmtree(os.path.join(SITE, folder), ignore_errors=True)
    if NEWSLETTER:
        pages.append((N_PATH, page(N_TITLE + ' – calcolaprecetti.it', N_DESC, N_PATH, N_OG, simple_ld('Newsletter', N_PATH, N_DESC),
                                   'newsletter', N_BODY, ['info.js'], noscript='')))
    for path, text in pages:
        f = write(path, text)
        print('%-22s %6d byte' % (path, os.path.getsize(f)))
    nf = page('Pagina non trovata – calcolaprecetti.it', E_DESC, '/404.html', E_DESC,
              {'@context': 'https://schema.org', '@type': 'WebPage', 'name': 'Pagina non trovata', 'inLanguage': 'it-IT'},
              'altro', E_BODY, ['info.js'], noscript='')
    canon = '<link rel="canonical" href="%s/404.html">\n' % BASE
    assert nf.count(canon) == 1
    nf = nf.replace(canon, '<meta name="robots" content="noindex">\n')  # da non indicizzare
    io.open(os.path.join(SITE, '404.html'), 'w', encoding='utf-8', newline='\n').write(tidy(nf))
    print('%-22s %6d byte' % ('/404.html', os.path.getsize(os.path.join(SITE, '404.html'))))
