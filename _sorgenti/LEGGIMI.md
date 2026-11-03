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
| Titoli, descrizioni e testi di termini, tassi, privacy, note legali, chi sono, valutazione, condizioni, pagina 404 | `gen/build_pages.py` |
| Barra in alto, piè di pagina, sezioni accese o spente (`GUIDE`, `CHI_SONO`, `VALUTAZIONE`, `NEWSLETTER`), prezzo e modulo della valutazione | `gen/build_guides.py` |
| Dati del titolare | `v5/assets/core.js` (`SITO`: nome, email), `gen/build_guides.py` (`PIVA`), `gen/build_pages.py` (`NOME`, `FORO`, `STUDIO_A`); data dell'informativa in `gen/patch_site.py` |
| Calcolo delle somme del precetto | `v5/assets/app.js` |
| Calcolo degli interessi moratori | `v5/assets/mini.js` |
| Stile | `v5/assets/style.css`, più `gen/pages.css` e `gen/guide.css` |

## File della radice che si modificano direttamente

Non sono generati: `assets/termini.js` (calcolo dei termini), `assets/info.js` (tabelle, privacy, note legali,
piè di pagina), le immagini (`assets/foto.jpg`, `og-image.png`, icone, `logo.svg`), i caratteri (`fonts/`),
`CNAME` e i file di verifica di Google e Bing.

## Contenuto della cartella

- `genera.py`: comando unico di generazione.
- `controlla.py`: controlli prima di pubblicare (sito servito in locale, contatore delle visite, anteprima).
- `gen/build_guides.py`: parti comuni a tutte le pagine e modello delle pagine delle guide.
- `gen/build_pages.py`: pagine termini, tassi, privacy, note legali, chi sono, valutazione, condizioni, 404.
- `gen/patch_site.py`: home e interessi moratori a partire da `v5/`; script e stile; sitemap di base;
  numero di versione di stile e script; alla fine lancia `finalize.py`.
- `gen/finalize.py`: accessibilità, copia statica per i crawler (`prerender.js`), sitemap con le date
  (`lastmod.json`, si aggiorna da sola), `robots.txt`.
- `gen/prerender.js`: scrive nell'HTML i contenuti che le pagine producono con JavaScript.
- `gen/pages.css`, `gen/guide.css`: parti del foglio di stile.
- `gen/guide.js`: script delle guide, copiato in `assets/` solo quando le guide sono accese.
- `gen/preview.py`: anteprima delle pagine in file autosufficienti, in una cartella temporanea fuori dal repository.
- `gen/check.js`, `gen/check_site.js`, `gen/test_conta.js`: controlli, lanciati da `controlla.py`.
- `gen/facsimile.html`, `gen/build_facsimile.js`: immagine del facsimile del parere (`assets/facsimile-parere.webp`).
  Si rigenera solo se cambia il facsimile: `node _sorgenti/gen/build_facsimile.js`.
- `v5/`: pagine e script di partenza (home, interessi moratori, `app.js`, `core.js`, `mini.js`, `docx.js`,
  `style.css`, `LICENSE`). La generazione riparte ogni volta da qui.

## Guide: bozze fuori dal repository

I testi delle tre guide (fattura non pagata, decreto ingiuntivo, precetto notificato) sono bozze da rivedere e non
stanno nel repository: sono nel file `guide_testi.py`, consegnato a parte insieme a `calc.js` (verifica degli
esempi delle guide con il motore di calcolo). Per pubblicarle:

1. rivedere i testi;
2. copiare `guide_testi.py` e `calc.js` in `_sorgenti/gen/` e togliere la riga di `guide_testi.py` da `_sorgenti/.gitignore`;
3. mettere `GUIDE = True` in `gen/build_guides.py`;
4. generare, controllare e pubblicare come sopra.

I sorgenti sono coperti dalla stessa licenza del repository (file `LICENSE`: tutti i diritti riservati).
