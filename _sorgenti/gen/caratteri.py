#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Caratteri del sito: file ridotti e dichiarazioni @font-face.

Parte dai caratteri originali in _sorgenti/fonts/ e scrive in fonts/, la cartella pubblicata:
- per ogni carattere due file: uno con l'alfabeto latino di base e il latino-1 (tutte le lettere dell'italiano,
  punteggiatura, €), che le pagine scaricano sempre, e uno con il latino esteso (lettere come ł, ő, č), che il browser
  scarica solo se nella pagina c'è una di quelle lettere;
- solo le funzioni tipografiche che le pagine usano: legature, crenatura, cifre allineate e tabellari
  (font-variant-numeric). Via maiuscoletto, svolazzi, frazioni, alternative stilistiche;
- EB Garamond con i soli pesi da 400 a 600, quelli usati (testo, titoli, totali del prospetto).

Scrive poi in v5/assets/style.css, tra i due commenti che delimitano il blocco, le dichiarazioni @font-face:
- quelle dei caratteri del sito, con l'intervallo di caratteri (unicode-range) di ogni file;
- quelle dei caratteri di riserva: i caratteri installati sui dispositivi (Times New Roman e Arial su Windows,
  Mac e iPhone; Noto Serif e Roboto su Android), ridimensionati per occupare lo stesso spazio di quelli del sito.
  Servono nel primo istante, prima che arrivino i caratteri del sito: il testo va a capo quasi negli stessi punti
  e la pagina non si sposta quando cambia il carattere.

Si lancia solo se cambiano i caratteri originali o i pesi usati: python3 _sorgenti/gen/caratteri.py
A parità di file di partenza il risultato è sempre identico.

Licenza dei caratteri: SIL Open Font License 1.1 (fonts/OFL-*.txt), che permette di modificarli e ridistribuirli con la
stessa licenza. Nessuno dei due dichiara un nome riservato (Reserved Font Name), quindi i file ridotti tengono il nome originale.
"""
import io
import os
import re

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

GEN = os.path.dirname(os.path.abspath(__file__))
SORGENTI = os.path.dirname(GEN)
SITE = os.path.dirname(SORGENTI)
ORIGINALI = os.path.join(SORGENTI, 'fonts')
USCITA = os.path.join(SITE, 'fonts')
STILE = os.path.join(SORGENTI, 'v5', 'assets', 'style.css')
INIZIO = '/* caratteri: blocco scritto da gen/caratteri.py, non modificarlo a mano */\n'
FINE = '/* fine dei caratteri */\n'

CARATTERI = [  # file originale, famiglia, peso dichiarato in @font-face, pesi tenuti (solo per i caratteri variabili)
    ('EBGaramond', 'EB Garamond', '400 600', (400, 600)),
    ('TitilliumWeb-Regular', 'Titillium Web', '400', None),
    ('TitilliumWeb-SemiBold', 'Titillium Web', '600', None),
    ('TitilliumWeb-Bold', 'Titillium Web', '700', None),
]
# funzioni tipografiche tenute: quelle che il browser applica da sé e le cifre chieste dallo stile (lining-nums, tabular-nums)
FUNZIONI = ['ccmp', 'locl', 'mark', 'mkmk', 'kern', 'liga', 'clig', 'calt', 'rlig', 'rclt', 'rvrn', 'lnum', 'tnum']

# Caratteri di riserva. Il rapporto di larghezza è quello tra il testo delle pagine scritto con il carattere del sito e lo
# stesso testo scritto con il carattere installato (frequenza delle lettere misurata sulle pagine del sito, novembre 2026):
# per EB Garamond sui titoli (peso 500), per Titillium sul testo (peso 400). Se si cambiano i caratteri, va rimisurato.
RISERVA = [  # famiglia di riserva, nomi del carattere installato (local), carattere del sito di riferimento, rapporto di larghezza
    ('EB Garamond riserva', ['Times New Roman', 'TimesNewRomanPSMT', 'Liberation Serif', 'LiberationSerif', 'Tinos'], 'EBGaramond', 0.982),
    ('EB Garamond riserva Noto', ['Noto Serif', 'NotoSerif', 'NotoSerif-Regular'], 'EBGaramond', 0.832),
    ('Titillium riserva', ['Arial', 'ArialMT', 'Liberation Sans', 'LiberationSans', 'Arimo'], 'TitilliumWeb-Regular', 0.939),
    ('Titillium riserva Roboto', ['Roboto', 'Roboto-Regular', 'Roboto Regular'], 'TitilliumWeb-Regular', 0.942),
]


def latino_di_base(c):
    """Caratteri del primo file: latino di base e latino-1, ı, Œ œ, punteggiatura generale, €, ™."""
    return c < 0x100 or c in (0x131, 0x152, 0x153, 0x20AC, 0x2122) or 0x2000 <= c <= 0x206F


def intervalli(codici):
    """Da un insieme di codici al valore di unicode-range: U+20-7E,U+A0-FF,..."""
    s = sorted(codici)
    out = []
    a = b = s[0]
    for c in s[1:] + [None]:
        if c is not None and c == b + 1:
            b = c
            continue
        out.append('U+%X' % a if a == b else 'U+%X-%X' % (a, b))
        if c is not None:
            a = b = c
    return ','.join(out)


def riduci(nome, codici, pesi, dst):
    o = subset.Options()
    o.layout_features = FUNZIONI
    o.name_IDs = ['*']  # tutti i nomi, compreso il copyright
    o.name_languages = ['*']
    o.name_legacy = True
    o.notdef_outline = True
    o.flavor = 'woff2'
    font = subset.load_font(os.path.join(ORIGINALI, nome + '.woff2'), o, lazy=False)
    s = subset.Subsetter(o)
    s.populate(unicodes=sorted(codici))
    s.subset(font)
    if pesi:  # dopo la riduzione: limita l'asse dei pesi del carattere variabile
        font = instancer.instantiateVariableFont(font, {'wght': pesi}, updateFontNames=False)
    subset.save_font(font, dst, o)
    return set(TTFont(dst).getBestCmap())


def metriche(nome):
    """Ascendente, discendente e interlinea del carattere, come le usa il browser (typo se il carattere lo chiede, se no hhea)."""
    t = TTFont(os.path.join(ORIGINALI, nome + '.woff2'))
    u, o, h = t['head'].unitsPerEm, t['OS/2'], t['hhea']
    if o.fsSelection & (1 << 7):  # USE_TYPO_METRICS
        return o.sTypoAscender / u, -o.sTypoDescender / u, o.sTypoLineGap / u
    return h.ascent / u, -h.descent / u, h.lineGap / u


def pct(x):
    return ('%.2f' % (100 * x)).rstrip('0').rstrip('.') + '%'


os.makedirs(USCITA, exist_ok=True)
regole, copertura = [], {}
for nome, famiglia, peso, pesi in CARATTERI:
    tutti = set(TTFont(os.path.join(ORIGINALI, nome + '.woff2')).getBestCmap())
    base = {c for c in tutti if latino_di_base(c)}
    esteso = tutti - base
    copertura[nome] = set()
    for suff, codici in (('', base), ('-ext', esteso)):
        if not codici:
            continue
        dst = os.path.join(USCITA, nome + suff + '.woff2')
        mappa = riduci(nome, codici, pesi, dst)
        assert mappa == codici, '%s%s: caratteri persi nella riduzione: %s' % (nome, suff, intervalli(codici - mappa))
        copertura[nome] |= mappa
        regole.append('@font-face{font-family:"%s";src:url("/fonts/%s%s.woff2") format("woff2");font-weight:%s;font-style:normal;'
                      'font-display:swap;unicode-range:%s}' % (famiglia, nome, suff, peso, intervalli(mappa)))
        print('%-28s %7d byte  (originale %d)  %d caratteri' % (nome + suff + '.woff2', os.path.getsize(dst),
              os.path.getsize(os.path.join(ORIGINALI, nome + '.woff2')), len(mappa)))
# caratteri di riserva: solo per i caratteri che quelli del sito hanno, così gli altri (→, −) restano come prima
for famiglia, locali, nome, r in RISERVA:
    asc, disc, gap = metriche(nome)
    regole.append('@font-face{font-family:"%s";src:%s;size-adjust:%s;ascent-override:%s;descent-override:%s;line-gap-override:%s;'
                  'unicode-range:%s}' % (famiglia, ','.join('local("%s")' % n for n in locali), pct(r), pct(asc / r), pct(disc / r),
                                         pct(gap / r), intervalli(copertura[nome])))
blocco = INIZIO + '\n'.join(regole) + '\n' + FINE

css = io.open(STILE, encoding='utf-8').read()
assert css.count(INIZIO) == 1 and css.count(FINE) == 1, 'v5/assets/style.css: delimitatori del blocco dei caratteri non trovati'
a, b = css.index(INIZIO), css.index(FINE) + len(FINE)
nuovo = css[:a] + blocco + css[b:]
if nuovo != css:
    io.open(STILE, 'w', encoding='utf-8', newline='\n').write(nuovo)
    print('v5/assets/style.css: dichiarazioni dei caratteri aggiornate')
else:
    print('v5/assets/style.css: dichiarazioni dei caratteri già aggiornate')
for f in sorted(os.listdir(USCITA)):  # file di prima rimasti senza uso
    if f.endswith('.woff2') and '"/fonts/%s"' % f not in blocco:
        print('ATTENZIONE: fonts/%s non è più dichiarato in style.css' % f)
