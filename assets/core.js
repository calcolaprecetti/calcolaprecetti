/* =====================================================================
   DATI DEL SITO (informativa privacy, note legali, contatti)
   Per cambiare titolare o email basta modificare queste righe.
   ===================================================================== */
var SITO = {
  nome: 'calcolaprecetti.it',
  titolare: 'a.m.',
  email: 'info@calcolaprecetti.it',
  hosting: 'GitHub Pages, servizio di GitHub, Inc.',
  trasferimento: "Il fornitore ha sede negli Stati Uniti: il trasferimento avviene sulla base delle garanzie previste dal Capo V del GDPR, come indicato nell'informativa privacy del fornitore.",
  fornitoreEmail: "OVH SAS, con server nell'Unione europea",
  informativaAggiornata: '22.09.2026'
};
/* =====================================================================
   TABELLE DA AGGIORNARE
   ---------------------------------------------------------------------
   Su GitHub: apri la cartella «assets», poi il file «core.js», matita,
   modifica, poi «Commit changes». Basta questo file: vale per tutte le
   pagine del sito. Le modifiche si vedono online entro dieci minuti.

   1) Interessi moratori - ogni gennaio e ogni luglio (comunicato MEF in G.U.)
      Aggiungere in "bce" una riga con il primo giorno del semestre, il
      TASSO DI RIFERIMENTO BCE del comunicato (senza gli 8 punti, li
      aggiunge il programma) e la fonte, anche se il tasso non cambia:
          ['2027-01-01', 2.40, 'Comunicato MEF, G.U. n. 12 del 16.01.2027'],
      Poi portare "moraPubblicatiFinoAl" all'ultimo giorno del semestre
      (es. '2027-06-30').

   2) Interessi legali - ogni dicembre (decreto MEF in G.U. entro il 15/12)
      Aggiungere in "legali" una riga come:
          ['2027-01-01', 1.60, 'D.M. 10.12.2026, G.U. n. 290 del 14.12.2026'],
      e portare "legaliPubblicatiFinoAl" a '2027-12-31'.

   3) Compenso del precetto - solo se un nuovo decreto cambia i parametri
      forensi: correggere i valori medi in "precetto".

   4) Registro - aggiungere IN CIMA a "registro" una riga con la data e
      cosa è cambiato; aggiornare "aggiornamento" (mese a fondo pagina).

   Regole: decimali con il punto (2.40, non 2,40); date AAAA-MM-GG;
   testi tra apostrofi (se il testo contiene un apostrofo, racchiuderlo
   tra virgolette doppie); virgola a fine riga come nelle righe presenti.
   Verifica: «Prova con un esempio» deve dare € 2.256,33 e i «Casi di
   verifica» in fondo alla pagina devono tornare.
   ===================================================================== */
var TABELLE = {
  aggiornamento: 'settembre 2026',
  legali: [ // [dal, tasso %, fonte]
    ['1997-01-01', 5, 'L. 23.12.1996, n. 662, art. 2, comma 185'],
    ['1999-01-01', 2.5, 'D.M. 10.12.1998'],
    ['2001-01-01', 3.5, 'D.M. 11.12.2000'],
    ['2002-01-01', 3, 'D.M. 11.12.2001'],
    ['2004-01-01', 2.5, 'D.M. 01.12.2003'],
    ['2008-01-01', 3, 'D.M. 12.12.2007'],
    ['2010-01-01', 1, 'D.M. 04.12.2009'],
    ['2011-01-01', 1.5, 'D.M. 07.12.2010'],
    ['2012-01-01', 2.5, 'D.M. 12.12.2011'],
    ['2014-01-01', 1, 'D.M. 12.12.2013'],
    ['2015-01-01', 0.5, 'D.M. 11.12.2014'],
    ['2016-01-01', 0.2, 'D.M. 11.12.2015, G.U. n. 291 del 15.12.2015'],
    ['2017-01-01', 0.1, 'D.M. 07.12.2016, G.U. n. 291 del 14.12.2016'],
    ['2018-01-01', 0.3, 'D.M. 13.12.2017, G.U. n. 292 del 15.12.2017'],
    ['2019-01-01', 0.8, 'D.M. 12.12.2018, G.U. n. 291 del 15.12.2018'],
    ['2020-01-01', 0.05, 'D.M. 12.12.2019, G.U. n. 293 del 14.12.2019'],
    ['2021-01-01', 0.01, 'D.M. 11.12.2020, G.U. n. 310 del 15.12.2020'],
    ['2022-01-01', 1.25, 'D.M. 13.12.2021'],
    ['2023-01-01', 5, 'D.M. 13.12.2022, G.U. n. 292 del 15.12.2022'],
    ['2024-01-01', 2.5, "D.M. 29.11.2023, G.U. n. 288 dell'11.12.2023"],
    ['2025-01-01', 2, 'D.M. 10.12.2024, G.U. n. 294 del 16.12.2024'],
    ['2026-01-01', 1.6, 'D.M. 10.12.2025, G.U. n. 289 del 13.12.2025']
  ],
  legaliPubblicatiFinoAl: '2026-12-31',
  bce: [ // [dal, tasso di riferimento BCE %, fonte] — al moratorio si aggiungono 8 punti
    ['2013-01-01', 0.75], ['2013-07-01', 0.50], ['2014-01-01', 0.25], ['2014-07-01', 0.15],
    ['2015-01-01', 0.05], ['2016-07-01', 0.00], ['2023-01-01', 2.50], ['2023-07-01', 4.00],
    ['2024-01-01', 4.50],
    ['2024-07-01', 4.25, 'Comunicato MEF, G.U. n. 176 del 29.07.2024'],
    ['2025-01-01', 3.15, 'Comunicato MEF, G.U. n. 63 del 17.03.2025'],
    ['2025-07-01', 2.15, 'Comunicato MEF, G.U. del 14.07.2025'],
    ['2026-01-01', 2.15, 'Comunicato MEF, G.U. n. 15 del 20.01.2026'],
    ['2026-07-01', 2.40, 'Comunicato MEF, G.U. n. 163 del 16.07.2026']
  ],
  maggiorazioneMora: 8,
  moraPubblicatiFinoAl: '2026-12-31',
  precetto: [ // [valore fino a €, compenso medio €] — min -50%, max +50%
    [5200, 142], [26000, 236], [52000, 331], [260000, 425], [520000, 567]
  ],
  rimborsoForfettario: 15, cpa: 4, iva: 22,
  registro: [ // [data, cosa è cambiato] — le righe più recenti in alto
    ['2026-09-25', "Sito diviso in più pagine: motore di calcolo, tassi e stile ora in file condivisi nella cartella assets. Nuova pagina dedicata agli interessi moratori del D.Lgs. 231/2002."],
    ['2026-09-24', "Aggiunti gli acconti con imputazione ex art. 1194 c.c., la fonte di ogni tasso (decreti MEF e comunicati in G.U.), i casi di verifica e il calcolo dei termini del precetto."],
    ['2026-09-22', "Pubblicazione del sito. Interessi legali dal 1997 al 2026 (ultimo: 1,60% dal 01.01.2026); interessi moratori dal 2013 al 2° semestre 2026 (ultimo: tasso BCE 2,40%, mora 10,40% dal 01.07.2026); compenso del precetto secondo il D.M. 147/2022."]
  ]
};

var Core = (function () {
  var DAY = 86400000;

  function toDay(s) {
    if (!s) return null;
    var p = String(s).split('-');
    if (p.length !== 3) return null;
    var y = +p[0], m = +p[1], d = +p[2];
    if (!y || !m || !d) return null;
    return Math.round(Date.UTC(y, m - 1, d) / DAY);
  }
  function parts(n) {
    var dt = new Date(n * DAY);
    return { y: dt.getUTCFullYear(), m: dt.getUTCMonth() + 1, d: dt.getUTCDate(), w: dt.getUTCDay() };
  }
  function dayOf(y, m, d) { return Math.round(Date.UTC(y, m - 1, d) / DAY); }
  function fmtDate(n) {
    var p = parts(n);
    return (p.d < 10 ? '0' : '') + p.d + '.' + (p.m < 10 ? '0' : '') + p.m + '.' + p.y;
  }
  function isoOf(n) {
    var p = parts(n);
    return p.y + '-' + (p.m < 10 ? '0' : '') + p.m + '-' + (p.d < 10 ? '0' : '') + p.d;
  }
  var WD = ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'];
  function weekday(n) { return WD[parts(n).w]; }

  function r2(x) { return Math.round(x * 100 + (x >= 0 ? 1e-7 : -1e-7)) / 100; }

  function parseNum(s) {
    if (s === null || s === undefined) return NaN;
    s = String(s).trim().replace(/[€%\s\u00a0]/g, '');
    if (!s) return NaN;
    var hasComma = s.indexOf(',') >= 0, hasDot = s.indexOf('.') >= 0;
    if (hasComma && hasDot) s = s.replace(/\./g, '').replace(',', '.');
    else if (hasComma) s = s.replace(',', '.');
    else if (hasDot) {
      var pp = s.split('.');
      if (pp.length > 2 || (pp[1] && pp[1].length === 3)) s = s.replace(/\./g, '');
    }
    var v = Number(s);
    return isFinite(v) ? v : NaN;
  }

  // Formattazione italiana fissa (1.394,25), indipendente dal browser
  function num(x) {
    var neg = x < 0, t = Math.abs(r2(x)).toFixed(2).split('.');
    return (neg ? '-' : '') + t[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ',' + t[1];
  }
  function eur(x) { return (r2(x) < 0 ? '–\u00a0' : '') + '€\u00a0' + num(Math.abs(x)); }
  function pct(x) { return num(x) + '%'; }

  var LEG = TABELLE.legali.map(function (r) { return [toDay(r[0]), r[1], r[2] || '']; });
  var BCE = TABELLE.bce.map(function (r) { return [toDay(r[0]), r[1], r[2] || '']; });
  var LEG_LAST = toDay(TABELLE.legaliPubblicatiFinoAl);
  var MORA_LAST = toDay(TABELLE.moraPubblicatiFinoAl);

  function rowAt(table, day) {
    var r = null;
    for (var i = 0; i < table.length; i++) {
      if (table[i][0] <= day) r = table[i]; else break;
    }
    return r;
  }
  function rateAt(table, day) { var r = rowAt(table, day); return r ? r[1] : null; }

  function semStart(day) { var p = parts(day); return dayOf(p.y, p.m <= 6 ? 1 : 7, 1); }
  function semName(day) { var p = parts(day); return (p.m <= 6 ? '1°' : '2°') + ' semestre ' + p.y; }
  function moraSource(day) {
    var s = semStart(day);
    for (var i = 0; i < BCE.length; i++) if (BCE[i][0] === s && BCE[i][2]) return BCE[i][2];
    return 'Comunicato MEF (art. 5 D.Lgs. 231/2002)';
  }
  function legalSource(day) { var r = rowAt(LEG, day); return r && r[2] ? r[2] : 'Decreto MEF'; }

  // Divide [s, e] per anno (legali) o per semestre (moratori)
  function split(kind, s, e) {
    var out = [];
    while (s <= e) {
      var p = parts(s), next;
      if (kind === 'legal') next = dayOf(p.y + 1, 1, 1);
      else next = p.m <= 6 ? dayOf(p.y, 7, 1) : dayOf(p.y + 1, 1, 1);
      var end = Math.min(e, next - 1);
      out.push([s, end]);
      s = end + 1;
    }
    return out;
  }

  function interest(cap, type, from, to, opt) {
    var res = { segments: [], total: 0, warnings: [] };
    if (type === 'none' || !(cap > 0) || to === null) return res;
    if (from === null) { res.warnings.push('missingFrom'); return res; }
    if (from > to) { res.warnings.push('fromAfterEnd'); return res; }
    var pieces = [];
    if (type === 'legal1284') {
      var d = opt.domanda;
      if (d === null) { res.warnings.push('missingDomanda'); pieces.push(['legal', from, to]); }
      else {
        if (d > from) pieces.push(['legal', from, Math.min(to, d - 1)]);
        if (d <= to) pieces.push(['mora', Math.max(d, from), to]);
      }
    } else if (type === 'fixed') {
      if (!(opt.rate >= 0)) { res.warnings.push('missingRate'); return res; }
      pieces.push(['fixed', from, to]);
    } else {
      pieces.push([type, from, to]);
    }
    pieces.forEach(function (pc) {
      var kind = pc[0];
      if (pc[1] > pc[2]) return;
      var segs = kind === 'fixed' ? [[pc[1], pc[2]]] : split(kind, pc[1], pc[2]);
      segs.forEach(function (sg) {
        var rate, src = '', base = null;
        if (kind === 'fixed') { rate = opt.rate; src = 'Tasso convenzionale indicato'; }
        else if (kind === 'legal') {
          rate = rateAt(LEG, sg[0]);
          src = 'Tasso legale ' + parts(sg[0]).y + ': ' + legalSource(sg[0]);
        } else {
          base = rateAt(BCE, sg[0]);
          rate = base === null ? null : base + TABELLE.maggiorazioneMora;
          if (base !== null) src = 'Tasso BCE ' + pct(base) + ' + ' + TABELLE.maggiorazioneMora + ' punti (' + semName(sg[0]) +
            (type === 'legal1284' ? ', art. 1284, comma 4, c.c.' : '') + '): ' + moraSource(sg[0]);
        }
        if (rate === null) { res.warnings.push(kind === 'legal' ? 'legalTooOld' : 'moraTooOld'); return; }
        if (kind === 'legal' && sg[0] > LEG_LAST) res.warnings.push('future');
        if (kind === 'mora' && sg[0] > MORA_LAST) res.warnings.push('future');
        var days = sg[1] - sg[0] + 1;
        var amount = r2(cap * rate / 100 * days / 365);
        res.segments.push({ kind: kind, s: sg[0], e: sg[1], days: days, rate: rate, amount: amount, cap: cap, src: src });
        res.total = r2(res.total + amount);
      });
    });
    return res;
  }

  function accessori(compenso, o) {
    var rows = [];
    var rf = o.rf ? r2(compenso * TABELLE.rimborsoForfettario / 100) : 0;
    if (o.rf) rows.push({ label: 'Rimborso forfettario ' + TABELLE.rimborsoForfettario + '% su ' + eur(compenso), amount: rf });
    var b1 = r2(compenso + rf);
    var cpa = o.cpa ? r2(b1 * TABELLE.cpa / 100) : 0;
    if (o.cpa) rows.push({ label: 'C.P.A. ' + TABELLE.cpa + '% su ' + eur(b1), amount: cpa });
    var b2 = r2(b1 + cpa);
    var iva = o.iva ? r2(b2 * TABELLE.iva / 100) : 0;
    if (o.iva) rows.push({ label: 'I.V.A. ' + TABELLE.iva + '% su ' + eur(b2), amount: iva });
    return { rows: rows, total: r2(b2 + iva) };
  }

  function scaglione(valore) {
    var prev = 0;
    for (var i = 0; i < TABELLE.precetto.length; i++) {
      var t = TABELLE.precetto[i];
      if (valore <= t[0]) return { from: prev === 0 ? 0.01 : prev + 0.01, to: t[0], medio: t[1], min: r2(t[1] * 0.5), max: r2(t[1] * 1.5) };
      prev = t[0];
    }
    return null;
  }

  var TITOLO = { di: 'nel decreto ingiuntivo', sent: 'nella sentenza', ord: "nell'ordinanza", altro: 'nel titolo' };

  function interestLabel(it, cap, s, e, domanda, scaled) {
    var tail = scaled ? ' dal ' + fmtDate(s) + ' al ' + fmtDate(e) + ', sul capitale a scalare dopo gli acconti'
                      : ' su ' + eur(cap) + ' dal ' + fmtDate(s) + ' al ' + fmtDate(e);
    switch (it.type) {
      case 'mora': return 'Interessi di mora ex D.Lgs. n. 231/2002' + tail;
      case 'legal': return 'Interessi legali ex art. 1284, comma 1, c.c.' + tail;
      case 'legal1284':
        return 'Interessi' + tail + ' (legali' + (domanda !== null && domanda <= e ? '; dal ' + fmtDate(Math.max(domanda, s)) + ' ex art. 1284, comma 4, c.c.' : '') + ')';
      case 'fixed': return 'Interessi al tasso convenzionale del ' + pct(parseNum(it.rate)) + tail;
    }
    return 'Interessi' + tail;
  }

  var MSG = {
    missingFrom: 'indica da quando decorrono gli interessi.',
    fromAfterEnd: 'la decorrenza è successiva alla data del conteggio, quindi non maturano interessi.',
    missingDomanda: 'indica la data della domanda giudiziale; per ora gli interessi sono calcolati tutti al tasso legale.',
    missingRate: 'indica il tasso convenzionale.',
    moraTooOld: 'i tassi moratori in tabella partono dal 01.01.2013; per i periodi precedenti usa un tasso convenzionale.',
    legalTooOld: 'i tassi legali in tabella partono dal 01.01.1997.',
    future: "per i periodi successivi all'ultimo tasso pubblicato è stato usato l'ultimo disponibile."
  };

  // st: { end, items:[{desc, amount, type, from, domanda, rate}], titolo, spese, compensi,
  //       feeMode:'medio'|'min'|'max'|'free', feeFree, rf, cpa, iva, extras:[{desc, amount}],
  //       acconti:[{date, amount}], titleDate }
  function compute(st) {
    var res = { rows: [], details: [], warnings: [], total: 0, empty: true, fee: null, valore: 0, payments: [], sources: [] };
    var end = toDay(st.end);
    if (end === null) res.warnings.push('Indica la data del conteggio.');

    // voci di capitale
    var list = [];
    st.items.forEach(function (it, i) {
      var cap = parseNum(it.amount);
      if (!(cap > 0)) return;
      list.push({ it: it, i: i, cap0: cap, C: cap, I: 0, tot: 0, segs: [], warn: {},
                  from: toDay(it.from), t: toDay(it.from), dom: toDay(it.domanda), rate: parseNum(it.rate) });
    });
    res.empty = !list.length;
    var multi = list.length > 1;
    list.forEach(function (x, k) {
      x.name = (x.it.desc || '').trim() || (multi ? 'Capitale (voce ' + (x.i + 1) + ')' : 'Capitale');
      x.prefix = multi ? 'Voce ' + (x.i + 1) + ': ' : '';
    });
    function warnItem(x, w) {
      if (x.warn[w]) return;
      x.warn[w] = 1;
      res.warnings.push(x.prefix + MSG[w].charAt(0).toUpperCase() + MSG[w].slice(1));
    }
    function accrue(x, d) {
      if (x.it.type === 'none' || end === null) return;
      if (x.t === null) { warnItem(x, 'missingFrom'); return; }
      if (x.t > d) return;
      var r = interest(x.C, x.it.type, x.t, d, { domanda: x.dom, rate: x.rate });
      r.warnings.forEach(function (w) { warnItem(x, w); });
      x.segs = x.segs.concat(r.segments);
      x.I = r2(x.I + r.total);
      x.tot = r2(x.tot + r.total);
      x.t = d + 1;
    }

    // spese liquidate nel titolo
    var prep = TITOLO[st.titolo] || TITOLO.altro;
    var spese = parseNum(st.spese), comp = parseNum(st.compensi);
    var titRows = [], titTot = 0;
    if (spese > 0) { titRows.push({ label: 'Spese liquidate ' + prep, amount: spese }); titTot = r2(titTot + spese); }
    if (comp > 0) {
      titRows.push({ label: 'Compensi liquidati ' + prep, amount: comp });
      var a = accessori(comp, st);
      titRows = titRows.concat(a.rows);
      titTot = r2(titTot + a.total);
    }

    // acconti: imputazione ex art. 1194 c.c. (spese, interessi, capitale)
    var pays = [];
    (st.acconti || []).forEach(function (p) {
      var v = parseNum(p.amount), d = toDay(p.date);
      if (!(v > 0)) return;
      if (d === null) { res.warnings.push("Indica la data dell'acconto di " + eur(v) + '.'); return; }
      if (end !== null && d > end) { res.warnings.push("L'acconto del " + fmtDate(d) + ' è successivo alla data del conteggio: non è stato considerato.'); return; }
      pays.push({ day: d, amount: r2(v) });
    });
    pays.sort(function (p, q) { return p.day - q.day; });
    var T = toDay(st.titleDate), S = titTot, accTot = 0;
    if (pays.length && titTot > 0 && T === null)
      res.warnings.push('Indica la data del titolo: per ora gli acconti sono imputati anche alle spese liquidate nel titolo, qualunque sia la loro data.');
    var ordered = list.slice().sort(function (p, q) {
      var a1 = p.from === null ? Infinity : p.from, b1 = q.from === null ? Infinity : q.from;
      return a1 - b1 || p.i - q.i;
    });
    pays.forEach(function (p) {
      list.forEach(function (x) { accrue(x, p.day); });
      var rest = p.amount, rec = { day: p.day, amount: p.amount, spese: 0, interessi: 0, capitale: 0, eccedenza: 0, residuo: 0 };
      if (S > 0 && (T === null || T <= p.day)) { var vs = r2(Math.min(rest, S)); S = r2(S - vs); rest = r2(rest - vs); rec.spese = vs; }
      ordered.forEach(function (x) { var vi = r2(Math.min(rest, x.I)); x.I = r2(x.I - vi); rest = r2(rest - vi); rec.interessi = r2(rec.interessi + vi); });
      ordered.forEach(function (x) { var vc = r2(Math.min(rest, x.C)); x.C = r2(x.C - vc); rest = r2(rest - vc); rec.capitale = r2(rec.capitale + vc); });
      rec.eccedenza = rest;
      rec.residuo = r2(list.reduce(function (t, x) { return t + x.C; }, 0));
      if (rest > 0) res.warnings.push("L'acconto del " + fmtDate(p.day) + ' supera il dovuto a quella data di ' + eur(rest) + ": l'eccedenza non è stata imputata.");
      accTot = r2(accTot + p.amount - rest);
      res.payments.push(rec);
    });
    list.forEach(function (x) {
      if (end === null || x.it.type === 'none') return;
      if (x.from !== null && x.from > end) { warnItem(x, 'fromAfterEnd'); return; }
      accrue(x, end);
    });

    // righe del prospetto
    var capTot = 0, intTot = 0, seenSrc = {};
    list.forEach(function (x) {
      capTot = r2(capTot + x.cap0);
      res.rows.push({ label: x.name, amount: x.cap0 });
      if (!x.segs.length) return;
      var s = x.segs[0].s, e = x.segs[x.segs.length - 1].e;
      var scaled = x.segs.some(function (g) { return g.cap !== x.cap0; });
      res.rows.push({ label: interestLabel(x.it, x.cap0, s, e, x.dom, scaled), amount: x.tot });
      res.details.push({ title: x.name, cap: x.cap0, segments: x.segs, total: x.tot, scaled: scaled });
      intTot = r2(intTot + x.tot);
      x.segs.forEach(function (g) { if (g.src && !seenSrc[g.src]) { seenSrc[g.src] = 1; res.sources.push(g.src); } });
    });
    res.rows = res.rows.concat(titRows);
    res.payments.forEach(function (p) {
      var v = r2(p.amount - p.eccedenza);
      if (v > 0) res.rows.push({ label: 'A dedurre: acconto del ' + fmtDate(p.day) + ' (imputazione ex art. 1194 c.c.)', amount: -v, acconto: true });
    });

    var extTot = 0, extraRows = [];
    (st.extras || []).forEach(function (x) {
      var v = parseNum(x.amount);
      if (v > 0) { extraRows.push({ label: (x.desc || '').trim() || 'Altre spese', amount: v }); extTot = r2(extTot + v); }
    });

    res.valore = r2(Math.max(0, capTot + intTot + titTot + extTot - accTot));
    var sc = scaglione(res.valore);
    res.scaglione = sc;
    var fee = 0, estinto = !res.empty && pays.length && res.valore <= 0;
    if (estinto) res.warnings.push('Con gli acconti il credito risulta interamente pagato: non ci sono somme da intimare.');
    if (estinto) fee = 0;
    else if (st.feeMode === 'free') fee = parseNum(st.feeFree) > 0 ? r2(parseNum(st.feeFree)) : 0;
    else if (sc) fee = st.feeMode === 'min' ? sc.min : st.feeMode === 'max' ? sc.max : sc.medio;
    else if (!res.empty) res.warnings.push('Il valore supera € 520.000,00: indica il compenso del precetto come importo libero.');
    if (res.empty) fee = 0;
    res.fee = fee;
    if (fee > 0) {
      res.rows.push({ label: 'Compenso atto di precetto (D.M. n. 55/2014 e s.m.i.)', amount: fee });
      res.rows = res.rows.concat(accessori(fee, st).rows);
    }
    res.rows = res.rows.concat(extraRows);
    res.total = r2(res.rows.reduce(function (t, r) { return t + r.amount; }, 0));
    return res;
  }

  /* ---------- termini del precetto (artt. 480, 481, 492-bis c.p.c.) ---------- */
  function easter(y) { // algoritmo gregoriano anonimo
    var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4,
        f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30,
        i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451);
    var month = Math.floor((h + l - 7 * m + 114) / 31), day = ((h + l - 7 * m + 114) % 31) + 1;
    return dayOf(y, month, day);
  }
  var FISSE = [[1, 1], [1, 6], [4, 25], [5, 1], [6, 2], [8, 15], [11, 1], [12, 8], [12, 25], [12, 26]];
  function holiday(n) { // festività nazionali (senza i patroni locali)
    var p = parts(n);
    if (p.w === 0) return 'domenica';
    for (var i = 0; i < FISSE.length; i++) if (FISSE[i][0] === p.m && FISSE[i][1] === p.d) return 'festivo';
    if (p.y >= 2026 && p.m === 10 && p.d === 4) return 'festivo';
    if (n === easter(p.y) + 1) return 'festivo';
    return '';
  }
  function proroga(n) { // art. 155, commi 4 e 5, c.p.c.: festivo o sabato → primo giorno non festivo
    var d = n;
    while (holiday(d) || parts(d).w === 6) d++;
    return d;
  }
  function termini(o) {
    var n = toDay(o.notifica);
    if (n === null) return null;
    var out = { notifica: n, warnings: [] };
    var g = parseInt(o.giorni, 10);
    if (!(g > 0)) g = 10;
    if (g < 10) out.warnings.push('Il termine per adempiere non può essere inferiore a 10 giorni, salvo autorizzazione (art. 482 c.p.c.).');
    out.giorni = g;
    out.adempiere = n + g;
    out.adempiereProrogato = proroga(out.adempiere);
    out.esecuzioneDal = out.adempiereProrogato + 1;
    out.sospensione = 0;
    out.sospeso = false;
    if (o.bis) {
      var a = toDay(o.bisFrom), b = toDay(o.bisTo);
      if (a === null) out.warnings.push("Indica la data di deposito dell'istanza ex art. 492-bis.");
      else if (a <= n) out.warnings.push("La data dell'istanza è anteriore o uguale alla notifica: controlla le date.");
      else if (b === null) { out.sospeso = true; out.bisFrom = a; out.giorniResidui = 90 - (a - n); }
      else if (b < a) out.warnings.push("La comunicazione dell'esito è anteriore al deposito dell'istanza: controlla le date.");
      else { out.sospensione = b - a; out.bisFrom = a; out.bisTo = b; }
    }
    out.efficacia = n + 90 + out.sospensione;
    out.efficaciaProrogata = proroga(out.efficacia);
    return out;
  }

  return { compute: compute, interest: interest, toDay: toDay, fmtDate: fmtDate, isoOf: isoOf, parseNum: parseNum,
           eur: eur, num: num, pct: pct, r2: r2, scaglione: scaglione, rateAt: rateAt, rowAt: rowAt, LEG: LEG, BCE: BCE,
           moraSource: moraSource, legalSource: legalSource, termini: termini, weekday: weekday, holiday: holiday, easter: easter };
})();

