# Sorgenti di calcolaprecetti.it

Le pagine del sito, nella radice del repository, sono **generate** da questi file. Non vanno modificate a mano:
la generazione successiva le riscriverebbe e la modifica andrebbe persa. Si cambiano i sorgenti e si rigenera.

GitHub Pages non pubblica le cartelle il cui nome inizia con «_»: questa cartella sta nel repository, non sul sito.

## Come si lavora

1. Modificare i sorgenti (sotto, «Dove si cambia cosa»).
2. Generare il sito: `python3 _sorgenti/genera.py`
3. Controllare: `python3 _sorgenti/controlla.py` (alla fine tutte le righe devono dire «ok»).
4. Guardare le differenze con `git status` e `git diff`: devono cambiare solo i file attesi.
   Se i sorgenti non cambiano, la generazione non cambia nessun file pubblicato.
5. Pubblicare: commit e push sul ramo main. GitHub Pages aggiorna il sito in pochi minuti.

Servono Python 3, Node.js e Playwright con Chromium (per la copia statica delle pagine e per i controlli).

## Dove si cambia cosa

| Cosa | Dove |
|---|---|
| Tassi legali (ogni dicembre), tassi moratori (gennaio e luglio), compenso del precetto, registro degli aggiornamenti | `v5/assets/core.js`, oggetto `TABELLE` (istruzioni in testa al file) |
| Anno nella pagina interessi moratori (ogni gennaio): titolo, descrizione, intestazione | `gen/patch_site.py`, sezione «interessi moratori» |
| Home: titolo e calcolatore | `v5/index.html` |
| Home: descrizione e testi aggiunti alla pagina di partenza | `gen/patch_site.py`, sezione «home» |
| Titoli, descrizioni e testi di termini, tassi, privacy, note legali, chi sono, recupero crediti, valutazione, condizioni, pagina di ringraziamento della valutazione, pagina 404 | `gen/build_pages.py` |
| Home: spiegazione sotto il calcolo, compenso del precetto, domande frequenti | `gen/patch_site.py`, `HOME_FAQ` e `HOME_INFO` |
| Testi delle guide e dell'indice `/guide/` (titoli, descrizioni, paragrafi, domande frequenti, esempi) | `gen/guide_testi.py`; data di prima pubblicazione (`GUIDE_PUBBLICATE`) e modello delle pagine in `gen/build_guides.py` |
| Barra «Per gli avvocati / Per i creditori» e schede di ciascuna parte (`TABS`, `TABS_CREDITORI`, `nav`), piè di pagina, sezioni accese o spente (`GUIDE`, `CHI_SONO`, `VALUTAZIONE`, `NEWSLETTER`), prezzo e modulo della valutazione | `gen/build_guides.py` |
| Dati del titolare | `v5/assets/core.js` (`SITO`: nome, email), `gen/build_guides.py` (`PIVA`), `gen/build_pages.py` (`NOME`, `FORO`, `STUDIO_A`); data dell'informativa in `gen/patch_site.py` |
| Calcolo delle somme del precetto | `v5/assets/app.js` |
| Calcolo degli interessi moratori | `v5/assets/mini.js` |
| Stile | `v5/assets/style.css`, più `gen/pages.css` e `gen/guide.css` (con le guide spente entra solo la parte comune, fino al commento «solo guide») |
| Caratteri: file ridotti in `fonts/`, dichiarazioni `@font-face` in testa a `v5/assets/style.css`, caratteri di riserva | `gen/caratteri.py`, dagli originali in `fonts/` di questa cartella |

## File della radice che si modificano direttamente

Non sono generati: `assets/termini.js` (calcolo dei termini), `assets/info.js` (tabelle, privacy, note legali,
piè di pagina), le immagini (`assets/foto.jpg`, `og-image.png`, icone, `logo.svg`), le licenze dei caratteri
(`fonts/OFL-*.txt`), `CNAME` e i file di verifica di Google e Bing. I file dei caratteri in `fonts/` (`.woff2`) li scrive
`gen/caratteri.py` (sotto).

## Contenuto della cartella

- `genera.py`: comando unico di generazione.
- `controlla.py`: controlli prima di pubblicare (sito servito in locale, contatore delle visite, anteprima).
- `gen/build_guides.py`: parti comuni a tutte le pagine e modello delle pagine delle guide.
- `gen/build_pages.py`: pagine termini, tassi, privacy, note legali, chi sono, valutazione, condizioni, 404.
- `gen/patch_site.py`: home e interessi moratori a partire da `v5/`; script e stile; sitemap di base;
  numero di versione di stile e script; alla fine lancia `finalize.py`.
- `gen/finalize.py`: accessibilità, precaricamento dei due caratteri principali, copia statica per i crawler
  (`prerender.js`), sitemap con le date (`lastmod.json`, si aggiorna da sola), `robots.txt`.
- `gen/prerender.js`: scrive nell'HTML i contenuti che le pagine producono con JavaScript.
- `gen/pages.css`, `gen/guide.css`: parti del foglio di stile.
- `gen/guide.js`: script delle guide, copiato in `assets/` solo quando le guide sono accese.
- `gen/guide_testi.py`: testi delle tre guide e dell'indice `/guide/`.
- `gen/calc.js`: ricalcola con il motore del sito (`assets/core.js`) gli esempi numerici delle guide: `node _sorgenti/gen/calc.js`.
- `gen/preview.py`: anteprima delle pagine in file autosufficienti, in una cartella temporanea fuori dal repository.
- `gen/check.js`, `gen/check_site.js`, `gen/test_conta.js`: controlli, lanciati da `controlla.py`.
- `gen/facsimile.html`, `gen/build_facsimile.js`: immagine del facsimile del parere (`assets/facsimile-parere.webp`).
  Si rigenera solo se cambia il facsimile: `node _sorgenti/gen/build_facsimile.js`.
- `gen/caratteri.py`: riduce i caratteri originali (`fonts/` di questa cartella) alle lettere latine e alle funzioni
  tipografiche usate, con un file a parte per il latino esteso che il browser scarica solo se serve; scrive le dichiarazioni
  `@font-face` e i caratteri di riserva (Times New Roman, Arial, Noto Serif, Roboto ridimensionati per occupare lo stesso
  spazio, così la pagina non si sposta mentre arrivano i caratteri). Si lancia solo se cambiano i caratteri o i pesi usati:
  `python3 _sorgenti/gen/caratteri.py`, poi si genera il sito. Le misure dei caratteri di riserva valgono per questi caratteri.
- `fonts/`: caratteri originali (EB Garamond variabile, Titillium Web) con le licenze SIL Open Font License 1.1.
- `v5/`: pagine e script di partenza (home, interessi moratori, `app.js`, `core.js`, `mini.js`, `docx.js`,
  `style.css`, `LICENSE`). La generazione riparte ogni volta da qui.

## Misura delle visite e delle richieste

- Statistiche: Umami, senza cookie (`v5/assets/core.js`, `Conta`). Le azioni si contano con l'attributo `data-conta="nome"`
  su pulsanti e collegamenti: calcoli, copie, rimandi dagli strumenti ai servizi (`recupero-da-home`, `recupero-da-interessi`,
  `valutazione-da-interessi`, `valutazione-da-recupero`, ...), contatto (`contatto-recupero`), barra in alto (`vai-creditori`).
- Richieste di valutazione completate: il modulo su Tally, a fine compilazione, porta a `/valutazione-credito/grazie/`
  (pagina non indicizzata, fuori dalla sitemap); ogni visita a quella pagina in Umami è una richiesta pagata.
- Ogni mese: Search Console › Rendimento (ultimi 28 giorni, esportazione CSV) e Umami nello stesso periodo. Confrontare i clic
  da Google con le visite che arrivano da google.com (uno scarto che cresce indica un problema del contatore) e seguire il
  percorso: pagine viste → rimandi ai servizi → `inizia-valutazione` → visite alla pagina di ringraziamento.

## Guide

Le tre guide (fattura non pagata, decreto ingiuntivo, precetto notificato) e l'indice `/guide/` sono accese
(`GUIDE = True` in `gen/build_guides.py`) e stanno nella parte «Per i creditori», con la scheda «Guide» prima di «Chi sono».
I testi sono in `gen/guide_testi.py`, rivisti dal titolare il 10.11.2026. La barra per gli avvocati in cima alle guide
(«Sei un avvocato? … copia il collegamento») è spenta: `CONDIVIDI = False` in `gen/build_guides.py`.
La data «Aggiornata il» di ogni guida si scrive da sola, come per le altre pagine (dalla sitemap, `gen/lastmod.json`);
la data di prima pubblicazione è `GUIDE_PUBBLICATE` e non va cambiata. Se si modificano gli esempi numerici, controllarli
con `node _sorgenti/gen/calc.js`; poi generare, controllare e pubblicare come sopra.

I sorgenti sono coperti dalla stessa licenza del repository (file `LICENSE`: tutti i diritti riservati).
