(function () {
  'use strict';
  var C = Core;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var nextId = 1;

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function todayIso() { var d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function newItem() { return { id: nextId++, desc: '', showDesc: false, amount: '', type: 'legal', from: '', domanda: '', rate: '', invDate: '', invTerm: '30' }; }
  function newExtra() { return { id: nextId++, desc: '', amount: '' }; }
  function newAcconto() { return { id: nextId++, date: '', amount: '' }; }
  function defaults() {
    return { end: todayIso(), items: [newItem()], titolo: 'di', spese: '', compensi: '',
             feeMode: 'medio', feeFree: '', rf: true, cpa: true, iva: false, extras: [],
             acconti: [], titleDate: '', fonti: true,
             tNotifica: '', tGiorni: '10', tBis: false, tBisFrom: '', tBisTo: '' };
  }
  var state = defaults();
  var last = null, lastT = null;

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function fmtInput(el) {
    var v = C.parseNum(el.value);
    if (el.value.trim() !== '' && !isNaN(v)) el.value = C.num(v);
  }
  function syncOn(container) {
    $$('label', container).forEach(function (l) {
      var i = l.querySelector('input[type=radio]');
      if (i) l.classList.toggle('on', i.checked);
    });
  }

  /* ---------- voci di capitale ---------- */
  var TYPES = [
    ['legal', 'Legali', 'art. 1284, comma 1, c.c.'],
    ['mora', 'Moratori commerciali', 'D.Lgs. 231/2002: tasso BCE + 8 punti'],
    ['legal1284', 'Legali, poi maggiorati dalla domanda', 'art. 1284, comma 4, c.c.'],
    ['fixed', 'Tasso convenzionale', 'indicato nel titolo o nel contratto'],
    ['none', 'Nessun interesse', '']
  ];

  function itemEl(it, idx, multi) {
    var el = document.createElement('div');
    el.className = 'item';
    el.dataset.type = it.type;
    var nm = 'type-' + it.id;
    el.innerHTML =
      '<div class="item-head"><span class="item-title">Voce ' + (idx + 1) + '</span>' +
      '<button type="button" class="linkbtn" data-act="remove">Rimuovi</button></div>' +
      '<label class="field desc-field"><span class="label">Descrizione <span class="opt">(facoltativa)</span></span>' +
      '<input type="text" data-k="desc" placeholder="Es. fattura n. 12 del 25.08.2025"></label>' +
      '<label class="field"><span class="label">Capitale</span>' +
      '<span class="money"><span class="sign">€</span><input type="text" inputmode="decimal" data-k="amount" data-money="1" placeholder="0,00"></span>' +
      '<span class="hint desc-toggle"><button type="button" class="linkbtn" data-act="desc">Aggiungi una descrizione</button>, per esempio il numero della fattura</span></label>' +
      '<fieldset class="field"><legend>Interessi</legend><div class="choices">' +
        TYPES.map(function (t) {
          return '<label class="choice"><input type="radio" name="' + nm + '" value="' + t[0] + '"><span><span class="t">' + t[1] + '</span>' +
            (t[2] ? '<span class="h">' + t[2] + '</span>' : '') + '</span></label>';
        }).join('') +
      '</div></fieldset>' +
      '<div class="when-rate">' +
        '<label class="field"><span class="label">Decorrenza degli interessi</span><input type="date" data-k="from">' +
        '<span class="hint">Primo giorno in cui maturano gli interessi.</span></label>' +
        '<details class="from-helper when-mora" style="margin:-6px 0 16px"><summary>Calcola la decorrenza dalla fattura</summary>' +
          '<div class="pair">' +
            '<label class="field"><span class="label">Fattura ricevuta il</span><input type="date" data-k="invDate"></label>' +
            '<label class="field"><span class="label">Termine (giorni)</span><input type="text" inputmode="numeric" data-k="invTerm"></label>' +
          '</div>' +
          '<span class="hint">Gli interessi decorrono dal giorno dopo la scadenza. Senza un termine pattuito, la scadenza è a 30 giorni dal ricevimento della fattura (art. 4 D.Lgs. 231/2002).</span>' +
        '</details>' +
        '<label class="field when-1284"><span class="label">Data della domanda giudiziale</span><input type="date" data-k="domanda">' +
        '<span class="hint">Da questa data si applica il tasso dell\'art. 1284, comma 4, c.c.</span></label>' +
        '<label class="field when-fixed"><span class="label">Tasso annuo</span>' +
        '<span class="money pct"><input type="text" inputmode="decimal" data-k="rate" placeholder="0,00"><span class="sign">%</span></span></label>' +
      '</div>';

    var showDesc = multi || it.showDesc;
    el.querySelector('.desc-field').hidden = !showDesc;
    el.querySelector('.desc-toggle').hidden = showDesc;

    $$('[data-k]', el).forEach(function (inp) {
      var k = inp.dataset.k;
      inp.value = it[k] || '';
      inp.addEventListener('input', function () {
        it[k] = inp.value;
        if (k === 'invDate' || k === 'invTerm') {
          var d = C.toDay(it.invDate), t = parseInt(it.invTerm, 10);
          if (d !== null && t >= 0) {
            it.from = C.isoOf(d + t + 1);
            el.querySelector('[data-k=from]').value = it.from;
          }
        }
        recalc();
      });
      if (inp.dataset.money || k === 'rate') inp.addEventListener('blur', function () { fmtInput(inp); it[k] = inp.value; });
    });
    $$('input[type=radio]', el).forEach(function (r) {
      r.checked = r.value === it.type;
      r.addEventListener('change', function () {
        it.type = r.value;
        el.dataset.type = r.value;
        syncOn(el);
        recalc();
      });
    });
    syncOn(el);
    el.querySelector('[data-act=remove]').addEventListener('click', function () {
      state.items = state.items.filter(function (x) { return x.id !== it.id; });
      if (!state.items.length) state.items.push(newItem());
      renderItems();
      recalc();
    });
    el.querySelector('[data-act=desc]').addEventListener('click', function () {
      it.showDesc = true;
      el.querySelector('.desc-field').hidden = false;
      el.querySelector('.desc-toggle').hidden = true;
      el.querySelector('[data-k=desc]').focus();
    });
    return el;
  }

  function renderItems() {
    var box = $('#items'), multi = state.items.length > 1;
    box.innerHTML = '';
    state.items.forEach(function (it, i) { box.appendChild(itemEl(it, i, multi)); });
    box.classList.toggle('multi', multi);
  }

  /* ---------- altre spese ---------- */
  function extraEl(x) {
    var el = document.createElement('div');
    el.className = 'extra-row';
    el.innerHTML =
      '<label class="field"><span class="label">Descrizione</span><input type="text" data-k="desc" placeholder="Imposta di registro"></label>' +
      '<label class="field"><span class="label">Importo</span><span class="money"><span class="sign">€</span>' +
      '<input type="text" inputmode="decimal" data-k="amount" placeholder="0,00"></span></label>' +
      '<button type="button" class="linkbtn" aria-label="Rimuovi la spesa">Rimuovi</button>';
    $$('[data-k]', el).forEach(function (inp) {
      var k = inp.dataset.k;
      inp.value = x[k] || '';
      inp.addEventListener('input', function () { x[k] = inp.value; recalc(); });
      if (k === 'amount') inp.addEventListener('blur', function () { fmtInput(inp); x[k] = inp.value; });
    });
    el.querySelector('button').addEventListener('click', function () {
      state.extras = state.extras.filter(function (y) { return y.id !== x.id; });
      renderExtras();
      recalc();
    });
    return el;
  }
  function renderExtras() {
    var box = $('#extras');
    box.innerHTML = '';
    state.extras.forEach(function (x) { box.appendChild(extraEl(x)); });
  }

  /* ---------- acconti ---------- */
  function accontoEl(p) {
    var el = document.createElement('div');
    el.className = 'pay-row';
    el.innerHTML =
      '<label class="field"><span class="label">Acconto del</span><input type="date" data-k="date"></label>' +
      '<label class="field"><span class="label">Importo</span><span class="money"><span class="sign">€</span>' +
      '<input type="text" inputmode="decimal" data-k="amount" placeholder="0,00"></span></label>' +
      '<button type="button" class="linkbtn" aria-label="Rimuovi l\'acconto">Rimuovi</button>';
    $$('[data-k]', el).forEach(function (inp) {
      var k = inp.dataset.k;
      inp.value = p[k] || '';
      inp.addEventListener('input', function () { p[k] = inp.value; recalc(); });
      if (k === 'amount') inp.addEventListener('blur', function () { fmtInput(inp); p[k] = inp.value; });
    });
    el.querySelector('button').addEventListener('click', function () {
      state.acconti = state.acconti.filter(function (y) { return y.id !== p.id; });
      renderAcconti();
      recalc();
    });
    return el;
  }
  function renderAcconti() {
    var box = $('#acconti');
    box.innerHTML = '';
    state.acconti.forEach(function (p) { box.appendChild(accontoEl(p)); });
    $('#titleDateField').hidden = !state.acconti.length;
    $('#addAcconto').textContent = state.acconti.length ? '+ Aggiungi un altro acconto' : '+ Aggiungi un acconto';
  }

  /* ---------- campi fissi ---------- */
  var TEXTS = [['endDate', 'end'], ['spese', 'spese'], ['compensi', 'compensi'], ['feeFree', 'feeFree'], ['titleDate', 'titleDate'],
               ['tNotifica', 'tNotifica'], ['tGiorni', 'tGiorni'], ['tBisFrom', 'tBisFrom'], ['tBisTo', 'tBisTo']];
  var CHECKS = [['optIva', 'iva'], ['optRf', 'rf'], ['optCpa', 'cpa'], ['optFonti', 'fonti'], ['tBis', 'tBis']];

  function syncStatic() {
    TEXTS.forEach(function (f) { $('#' + f[0]).value = state[f[1]]; });
    CHECKS.forEach(function (c) { $('#' + c[0]).checked = !!state[c[1]]; });
    $$('input[name=titolo]').forEach(function (r) { r.checked = r.value === state.titolo; });
    $$('input[name=feeMode]').forEach(function (r) { r.checked = r.value === state.feeMode; });
    syncOn($('#titoloChips'));
    syncOn($('#feeSeg'));
    $('#feeFreeField').hidden = state.feeMode !== 'free';
  }
  function bindStatic() {
    TEXTS.forEach(function (f) {
      var el = $('#' + f[0]);
      el.addEventListener('input', function () { state[f[1]] = el.value; recalc(); });
      if (el.inputMode === 'decimal') el.addEventListener('blur', function () { fmtInput(el); state[f[1]] = el.value; });
    });
    CHECKS.forEach(function (c) {
      $('#' + c[0]).addEventListener('change', function (e) { state[c[1]] = e.target.checked; recalc(); });
    });
    $$('input[name=titolo]').forEach(function (r) {
      r.addEventListener('change', function () { state.titolo = r.value; syncOn($('#titoloChips')); recalc(); });
    });
    $$('input[name=feeMode]').forEach(function (r) {
      r.addEventListener('change', function () {
        state.feeMode = r.value;
        syncOn($('#feeSeg'));
        $('#feeFreeField').hidden = state.feeMode !== 'free';
        recalc();
      });
    });
    $('#addItem').addEventListener('click', function () {
      state.items.push(newItem());
      renderItems();
      recalc();
      var all = $$('#items .item');
      all[all.length - 1].querySelector('[data-k=amount]').focus();
    });
    $('#addAcconto').addEventListener('click', function () {
      state.acconti.push(newAcconto());
      renderAcconti();
      recalc();
      var rows = $$('#acconti .pay-row');
      rows[rows.length - 1].querySelector('[data-k=date]').focus();
    });
    $('#addExtra').addEventListener('click', function () {
      state.extras.push(newExtra());
      renderExtras();
      recalc();
      var rows = $$('#extras .extra-row');
      rows[rows.length - 1].querySelector('[data-k=desc]').focus();
    });
  }

  /* ---------- risultato ---------- */
  function renderResults(res) {
    var end = C.toDay(state.end);
    $('#resDate').textContent = end === null ? '' : 'al ' + C.fmtDate(end);
    $('#warnings').innerHTML = res.warnings.map(function (w) { return '<p class="warn">' + esc(w) + '</p>'; }).join('');
    var empty = res.empty;
    $('#empty').hidden = !empty;
    $('#sheet').hidden = empty;
    $('#actions').hidden = empty;
    $('#pasteHint').hidden = empty;
    $('#detail').hidden = empty || (!res.details.length && !res.payments.length);
    $('#fontiCheck').hidden = empty || !res.sources.length;
    if (empty) $('#status').textContent = '';
    $('#mbTotal').textContent = C.eur(empty ? 0 : res.total);
    $('#srTotal').textContent = empty ? '' : 'Totale ' + C.eur(res.total);
    if (empty) return;

    $('#table tbody').innerHTML = res.rows.map(function (r) {
      return '<tr' + (r.acconto ? ' class="acc"' : '') + '><td>' + esc(r.label) + '</td><td class="amt">' + C.eur(r.amount) + '</td></tr>';
    }).join('') + '<tr class="total"><td>TOTALE COMPLESSIVO</td><td class="amt">' + C.eur(res.total) + '</td></tr>';
    var showSrc = state.fonti && res.sources.length;
    $('#sources').hidden = !showSrc;
    $('#sources').textContent = showSrc ? sourcesText(res) : '';

    var many = res.details.length > 1;
    var html = res.details.map(function (d) {
      return '<div class="scroll"><table class="det">' + (many ? '<caption>' + esc(d.title) + '</caption>' : '') +
        '<thead><tr><th>Periodo</th><th class="r">Giorni</th><th class="r">Tasso</th><th class="r">Interessi</th></tr></thead><tbody>' +
        d.segments.map(function (s) {
          return '<tr class="segrow"><td>dal ' + C.fmtDate(s.s) + ' al ' + C.fmtDate(s.e) + '</td><td class="r">' + s.days + '</td><td class="r">' +
            C.pct(s.rate) + '</td><td class="r">' + C.eur(s.amount) + '</td></tr>' +
            '<tr class="src"><td colspan="4">' + (d.scaled ? 'Su ' + C.eur(s.cap) + ' – ' : '') + esc(s.src) + '</td></tr>';
        }).join('') + '</tbody><tfoot><tr><td colspan="3">Totale</td><td class="r">' + C.eur(d.total) + '</td></tr></tfoot></table></div>';
    }).join('');
    if (res.payments.length) {
      html += '<div class="scroll"><table class="det"><caption>Imputazione degli acconti (art. 1194 c.c.)</caption>' +
        '<thead><tr><th>Acconto</th><th class="r">Importo</th><th class="r">Spese</th><th class="r">Interessi</th><th class="r">Capitale</th></tr></thead><tbody>' +
        res.payments.map(function (p) {
          return '<tr class="segrow"><td>' + C.fmtDate(p.day) + '</td><td class="r">' + C.eur(p.amount) + '</td><td class="r">' + C.eur(p.spese) +
            '</td><td class="r">' + C.eur(p.interessi) + '</td><td class="r">' + C.eur(p.capitale) + '</td></tr>' +
            '<tr class="src"><td colspan="5">Capitale residuo dopo l\'acconto: ' + C.eur(p.residuo) + (p.eccedenza > 0 ? '; eccedenza non imputata: ' + C.eur(p.eccedenza) : '') + '</td></tr>';
        }).join('') + '</tbody></table></div>' +
        '<p class="det-note">Prima alle spese liquidate nel titolo, poi agli interessi maturati fino al giorno dell\'acconto, infine al capitale; con più voci, prima alla più antica. Dal giorno successivo gli interessi maturano sul capitale residuo.</p>';
    }
    $('#detailBody').innerHTML = html;
  }
  function sourcesText(res) { return 'Fonti dei tassi: ' + res.sources.join('; ') + '.'; }

  function renderFee(res) {
    var sc = res.scaglione, info = $('#feeInfo');
    $$('#feeSeg [data-v]').forEach(function (v) { v.textContent = (!res.empty && sc) ? C.eur(sc[v.dataset.v]) : ''; });
    if (res.empty) info.textContent = 'Lo scaglione dipende dal credito: capitale, interessi e spese del titolo.';
    else if (!sc) info.textContent = 'Il valore supera € 520.000,00: scegli «Libero» e indica il compenso.';
    else info.textContent = 'Valore del credito ' + C.eur(res.valore) + ': scaglione da ' + C.eur(sc.from) + ' a ' + C.eur(sc.to) + ' (D.M. 147/2022).';
  }

  function renderMoreSummary() {
    var fee = { medio: 'Compenso medio', min: 'Compenso minimo', max: 'Compenso massimo', free: 'Compenso libero' }[state.feeMode];
    var acc = state.rf && state.cpa ? 'rimborso forfettario e C.P.A. inclusi' : state.rf ? 'solo rimborso forfettario' : state.cpa ? 'solo C.P.A.' : 'senza accessori';
    var n = state.extras.filter(function (x) { return C.parseNum(x.amount) > 0; }).length;
    $('#moreSummary').textContent = fee + ', ' + acc + (n ? ', ' + n + (n === 1 ? ' altra spesa' : ' altre spese') : '') + '.';
  }

  function recalc() {
    last = C.compute(state);
    renderResults(last);
    renderFee(last);
    renderMoreSummary();
    renderTermini();
  }

  /* ---------- termini del precetto ---------- */
  function dayFull(n) { return C.weekday(n) + ' ' + C.fmtDate(n); }
  function why(n) { var h = C.holiday(n); return h === 'domenica' ? 'di domenica' : h ? 'in un giorno festivo' : 'di sabato'; }
  function renderTermini() {
    $('#tBisFields').hidden = !state.tBis;
    var t = C.termini({ notifica: state.tNotifica, giorni: state.tGiorni, bis: state.tBis, bisFrom: state.tBisFrom, bisTo: state.tBisTo });
    lastT = t;
    $('#tWarnings').innerHTML = t ? t.warnings.map(function (w) { return '<p class="warn">' + esc(w) + '</p>'; }).join('') : '';
    $('#tEmpty').hidden = !!t;
    $('#tOut').hidden = !t;
    $('#tActions').hidden = !t;
    $('#tNote').hidden = !t;
    if (!t) { $('#tOut').innerHTML = ''; return; }
    var out = [];
    out.push(['Scadenza del termine per adempiere (' + t.giorni + ' giorni, art. 480 c.p.c.)',
      dayFull(t.adempiere) + (t.adempiereProrogato !== t.adempiere ? '<span class="n">Cade ' + why(t.adempiere) + ': prorogato a ' + dayFull(t.adempiereProrogato) + ' (art. 155 c.p.c.).</span>' : '')]);
    out.push(["Si può iniziare l'esecuzione dal (art. 482 c.p.c.)", dayFull(t.esecuzioneDal)]);
    if (t.sospeso) {
      out.push(['Efficacia del precetto (art. 481 c.p.c.)', 'Termine sospeso dal ' + C.fmtDate(t.bisFrom) +
        '<span class="n">Istanza ex art. 492-bis c.p.c.: dalla comunicazione dell\'esito restano ' + t.giorniResidui + ' giorni.</span>']);
    } else {
      out.push(["Il precetto perde efficacia se l'esecuzione non inizia entro (art. 481 c.p.c.)",
        dayFull(t.efficacia) +
        (t.efficaciaProrogata !== t.efficacia ? '<span class="n">Cade ' + why(t.efficacia) + ': prorogato a ' + dayFull(t.efficaciaProrogata) + ' (art. 155 c.p.c.). Per prudenza, conviene non attendere la proroga.</span>' : '') +
        (t.sospensione ? '<span class="n">Compresi ' + t.sospensione + ' giorni di sospensione per l\'istanza ex art. 492-bis c.p.c. (dal ' + C.fmtDate(t.bisFrom) + ' al ' + C.fmtDate(t.bisTo) + ').</span>' : '')]);
    }
    $('#tOut').innerHTML = out.map(function (o) { return '<div><dt>' + esc(o[0]) + '</dt><dd>' + o[1] + '</dd></div>'; }).join('');
    renderCalLinks();
  }
  function icsDate(n) { return C.isoOf(n).replace(/-/g, ''); }
  function calEvent() { // evento principale: la scadenza dei 90 giorni
    var t = lastT;
    if (!t || t.sospeso) return null;
    return { day: t.efficacia,
             title: "Precetto: ultimo giorno per iniziare l'esecuzione (art. 481 c.p.c.)",
             desc: 'Precetto notificato il ' + C.fmtDate(t.notifica) + '. Calcolo di ' + SITO.nome + ' da verificare.' };
  }
  function renderCalLinks() {
    var ev = calEvent(), g = $('#tGcal'), o = $('#tOutlook');
    if (!g || !o) return;
    g.hidden = o.hidden = !ev;
    if (!ev) return;
    g.href = 'https://calendar.google.com/calendar/render?action=TEMPLATE' +
      '&text=' + encodeURIComponent(ev.title) +
      '&dates=' + icsDate(ev.day) + '/' + icsDate(ev.day + 1) +
      '&details=' + encodeURIComponent(ev.desc);
    o.href = 'https://outlook.live.com/calendar/0/deeplink/compose?path=' + encodeURIComponent('/calendar/action/compose') +
      '&rru=addevent&allday=true' +
      '&startdt=' + C.isoOf(ev.day) + '&enddt=' + C.isoOf(ev.day + 1) +
      '&subject=' + encodeURIComponent(ev.title) + '&body=' + encodeURIComponent(ev.desc);
  }
  function icsText(s) { return String(s).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,'); }
  function doIcs() {
    var t = lastT;
    if (!t) return;
    var now = new Date(), stamp = now.getUTCFullYear() + pad(now.getUTCMonth() + 1) + pad(now.getUTCDate()) + 'T' + pad(now.getUTCHours()) + pad(now.getUTCMinutes()) + pad(now.getUTCSeconds()) + 'Z';
    var base = 'Precetto notificato il ' + C.fmtDate(t.notifica) + '. Calcolo di ' + SITO.nome + ' da verificare.';
    function ev(day, title, desc, alarm) {
      return ['BEGIN:VEVENT', 'UID:' + icsDate(day) + '-' + Math.random().toString(36).slice(2) + '@' + SITO.nome, 'DTSTAMP:' + stamp,
        'DTSTART;VALUE=DATE:' + icsDate(day), 'DTEND;VALUE=DATE:' + icsDate(day + 1), 'SUMMARY:' + icsText(title), 'DESCRIPTION:' + icsText(desc)]
        .concat(alarm ? ['BEGIN:VALARM', 'TRIGGER:-P7D', 'ACTION:DISPLAY', 'DESCRIPTION:' + icsText('Tra 7 giorni scade il termine per iniziare l\'esecuzione'), 'END:VALARM'] : [])
        .concat(['END:VEVENT']);
    }
    var lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//' + SITO.nome + '//Termini del precetto//IT', 'CALSCALE:GREGORIAN']
      .concat(ev(t.esecuzioneDal, "Precetto: si può iniziare l'esecuzione", base))
      .concat(t.sospeso ? [] : ev(t.efficacia, "Precetto: ultimo giorno per iniziare l'esecuzione (art. 481 c.p.c.)", base, true))
      .concat(['END:VCALENDAR']);
    var blob = new Blob([lines.join('\r\n') + '\r\n'], { type: 'text/calendar;charset=utf-8' });
    var url = URL.createObjectURL(blob), a = document.createElement('a');
    a.href = url;
    a.download = 'termini-precetto-' + C.isoOf(t.notifica) + '.ics';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
  }

  /* ---------- esportazione ---------- */
  var NOTE = 'Salvo errori od omissioni, oltre agli ulteriori interessi maturandi sino al saldo e alle successive occorrende spese.';
  function wordHtml(res) {
    var td = 'border:1px solid #000;padding:3pt 6pt;font-family:Garamond,serif;font-size:12pt;';
    var rows = res.rows.map(function (r) {
      return '<tr><td style="' + td + '" width="75%">' + esc(r.label) + '</td><td style="' + td + 'text-align:right;white-space:nowrap" width="25%">' + C.eur(r.amount) + '</td></tr>';
    }).join('');
    rows += '<tr><td style="' + td + 'font-weight:bold">TOTALE COMPLESSIVO</td><td style="' + td + 'text-align:right;font-weight:bold;white-space:nowrap">' + C.eur(res.total) + '</td></tr>';
    return '<table style="border-collapse:collapse;width:100%" cellspacing="0">' + rows + '</table>' +
      (state.fonti && res.sources.length ? '<p style="font-family:Garamond,serif;font-size:10pt;margin:6pt 0 0">' + esc(sourcesText(res)) + '</p>' : '');
  }
  function plainText(res) {
    return res.rows.map(function (r) { return r.label + '\t' + C.eur(r.amount); }).join('\n') + '\nTOTALE COMPLESSIVO\t' + C.eur(res.total) +
      (state.fonti && res.sources.length ? '\n\n' + sourcesText(res) : '');
  }
  function say(msg) {
    var s = $('#status');
    s.textContent = msg;
    clearTimeout(say.t);
    say.t = setTimeout(function () { s.textContent = ''; }, 5000);
  }
  function fallbackCopy(html) {
    var div = document.createElement('div');
    div.setAttribute('contenteditable', 'true');
    div.style.cssText = 'position:fixed;left:-9999px;top:0;';
    div.innerHTML = html;
    document.body.appendChild(div);
    var range = document.createRange();
    range.selectNodeContents(div);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    sel.removeAllRanges();
    document.body.removeChild(div);
    return ok;
  }
  function copied(ok) { say(ok ? 'Tabella copiata: incollala nel precetto.' : 'Copia non riuscita: usa «Scarica .docx».'); }
  function doCopy() {
    if (!last || last.empty) return;
    var html = wordHtml(last), text = plainText(last);
    if (navigator.clipboard && window.ClipboardItem && window.isSecureContext) {
      navigator.clipboard.write([new ClipboardItem({
        'text/html': new Blob([html], { type: 'text/html' }),
        'text/plain': new Blob([text], { type: 'text/plain' })
      })]).then(function () { copied(true); }, function () { copied(fallbackCopy(html)); });
    } else {
      copied(fallbackCopy(html));
    }
  }
  function doDocx() {
    if (!last || last.empty) return;
    var end = C.toDay(state.end);
    var rows = last.rows.map(function (r) { return { label: r.label, amount: C.eur(r.amount) }; });
    var notes = [{ text: NOTE }];
    if (state.fonti && last.sources.length) notes.push({ text: sourcesText(last), small: true });
    var blob = Docx.build(rows, C.eur(last.total), end === null ? 'Prospetto delle somme' : 'Prospetto delle somme al ' + C.fmtDate(end), notes);
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'prospetto-precetto' + (end === null ? '' : '-' + C.isoOf(end)) + '.docx';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
    say('File Word scaricato.');
  }

  /* ---------- esempio, nuovo calcolo, annulla ---------- */
  function refresh() { syncStatic(); renderItems(); renderExtras(); renderAcconti(); recalc(); }
  function loadExample() {
    var it = newItem();
    it.amount = '1.394,25'; it.type = 'mora'; it.from = '2025-09-25'; it.invDate = '2025-08-25'; it.invTerm = '30';
    state = Object.assign(defaults(), { end: '2026-09-21', items: [it], titolo: 'di', spese: '76,00', compensi: '300,00',
              feeMode: 'medio', feeFree: '', rf: true, cpa: true, iva: true, extras: [] });
    refresh();
  }
  var toastTimer, undoState = null;
  function showToast(text, onUndo) {
    var t = $('#toast');
    $('#toastText').textContent = text;
    t.hidden = false;
    undoState = onUndo;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.hidden = true; undoState = null; }, 7000);
  }
  function newCalc() {
    var prev = JSON.parse(JSON.stringify(state));
    state = defaults();
    refresh();
    showToast('Calcolo azzerato.', function () { state = prev; refresh(); });
  }

  /* ---------- testi legali e tabelle ---------- */
  function v(s) { return /^\[.*\]$/.test(s) ? '<mark style="background:var(--mark)">' + esc(s) + '</mark>' : esc(s); }
  function renderLegal() {
    $('#privacyBody').innerHTML =
      '<h3>Titolare del trattamento</h3><p>' + v(SITO.titolare) + ', contattabile all\'indirizzo ' + v(SITO.email) + '.</p>' +
      '<h3>Quali dati vengono trattati</h3>' +
      '<p>Il sito non usa cookie né altri strumenti di tracciamento e non carica contenuti da siti di terzi. I dati inseriti nel calcolo sono elaborati solo nel tuo browser: non vengono inviati al titolare né a terzi e non vengono conservati, quindi si cancellano chiudendo o ricaricando la pagina.</p>' +
      '<p>Come per qualsiasi sito, il servizio di hosting (' + esc(SITO.hosting) + ') registra nei propri log tecnici alcuni dati di navigazione, come indirizzo IP, data e ora della richiesta, pagina visitata e tipo di browser, per la sicurezza e il funzionamento del servizio. Il titolare non usa questi dati per identificare i visitatori né per profilazione.</p>' +
      '<h3>Se scrivi un suggerimento</h3><p>Se scrivi a ' + v(SITO.email) + ', i dati contenuti nel messaggio (indirizzo email, eventuale nome e contenuto) sono usati solo per rispondere e valutare il suggerimento, sulla base del legittimo interesse (art. 6, par. 1, lett. f, GDPR), e vengono cancellati quando non servono più. La casella di posta è fornita da ' + esc(SITO.fornitoreEmail) + '. Ti chiedo di non inserire nei messaggi dati personali di clienti o di terzi.</p>' +
      '<h3>Finalità e base giuridica</h3><p>Sicurezza e corretto funzionamento del sito, sulla base del legittimo interesse (art. 6, par. 1, lett. f, Reg. UE 2016/679).</p>' +
      '<h3>Destinatari e trasferimenti</h3><p>I dati di navigazione sono trattati dal fornitore di hosting secondo la propria informativa. ' + esc(SITO.trasferimento) + '</p>' +
      '<h3>Collegamenti a Google Calendar e Outlook</h3><p>Nella sezione dei termini del precetto trovi due collegamenti facoltativi che aprono Google Calendar o Outlook.com con la scadenza già compilata. Se li usi, la data e il titolo dell\'appuntamento vengono inviati al servizio scelto, che li tratta come titolare autonomo secondo la propria informativa; non viene inviato nulla finché non li clicchi. Il file da scaricare, invece, resta sul tuo dispositivo.</p>' +
      '<h3>Conservazione</h3><p>I dati di navigazione sono conservati dal fornitore per il tempo necessario alle finalità di sicurezza, secondo le sue politiche.</p>' +
      '<h3>Diritti</h3><p>Puoi esercitare i diritti previsti dagli artt. 15-22 del GDPR (accesso, rettifica, cancellazione, limitazione, opposizione) scrivendo a ' + v(SITO.email) + ' e proporre reclamo al Garante per la protezione dei dati personali (garanteprivacy.it).</p>' +
      '<p>Ultimo aggiornamento: ' + esc(SITO.informativaAggiornata) + '.</p>';
    $('#legalBody').innerHTML =
      '<p>' + esc(SITO.nome) + ' è uno strumento gratuito di ausilio al calcolo delle somme da intimare con l\'atto di precetto. I risultati dipendono dai dati inseriti e dalle tabelle indicate in «Tassi e parametri usati»: vanno sempre verificati prima dell\'uso in un atto e non costituiscono consulenza legale.</p>' +
      '<p>Nei limiti consentiti dalla legge, il titolare non risponde di errori od omissioni derivanti dall\'uso dello strumento.</p>' +
      '<p>Titolare del sito: ' + v(SITO.titolare) + ', ' + v(SITO.email) + '.</p>' +
      '<p>Caratteri tipografici: EB Garamond e Titillium Web, con licenza SIL Open Font License 1.1.</p>';
  }
  function renderRates() {
    var leg = TABELLE.legali.slice().reverse().map(function (r, i, arr) {
      var y = +r[0].slice(0, 4);
      var to = i === 0 ? +TABELLE.legaliPubblicatiFinoAl.slice(0, 4) : +arr[i - 1][0].slice(0, 4) - 1;
      return '<tr><td>' + (to > y ? y + '–' + to : y) + (r[2] ? '<span class="s">' + esc(r[2]) + '</span>' : '') + '</td><td>' + C.pct(r[1]) + '</td></tr>';
    }).join('');
    var rows = [], lastDay = C.toDay(TABELLE.moraPubblicatiFinoAl), endY = +TABELLE.moraPubblicatiFinoAl.slice(0, 4);
    for (var y = endY; y >= 2013; y--) {
      for (var h = 2; h >= 1; h--) {
        var day = C.toDay(y + (h === 1 ? '-01-01' : '-07-01'));
        if (day > lastDay) continue;
        var b = C.rateAt(C.BCE, day), row = C.rowAt(C.BCE, day), own = row && row[0] === day && row[2] ? row[2] : '';
        rows.push('<tr><td>' + h + '° semestre ' + y + '<span class="s">Tasso BCE ' + C.pct(b) + (own ? ' – ' + esc(own) : '') + '</span></td><td>' +
          C.pct(b + TABELLE.maggiorazioneMora) + '</td></tr>');
      }
    }
    var prec = TABELLE.precetto.map(function (t, i) {
      var from = i === 0 ? 0.01 : TABELLE.precetto[i - 1][0] + 0.01;
      return '<tr><td>' + C.eur(from) + ' – ' + C.eur(t[0]) + '</td><td>' + C.eur(t[1]) + '</td></tr>';
    }).join('');
    $('#ratesGrid').innerHTML =
      '<table><caption>Interessi legali</caption><tbody>' + leg + '</tbody></table>' +
      '<table><caption>Interessi moratori</caption><tbody>' + rows.join('') + '</tbody></table>' +
      '<table><caption>Compenso medio del precetto</caption><tbody>' + prec + '</tbody></table>';
    $('#updated').textContent = TABELLE.aggiornamento;
  }
  var CASES = [
    { t: 'Interessi legali in un solo anno',
      d: 'Capitale € 10.000,00, interessi legali dal 01.01.2026 al 30.06.2026, senza spese né compenso di precetto.',
      c: ['181 giorni al tasso legale 2026 (1,60%):', '10.000,00 × 1,60% × 181 / 365 = 79,34'],
      r: 'Interessi € 79,34; totale € 10.079,34.',
      load: function () {
        var it = newItem(); it.amount = '10.000,00'; it.type = 'legal'; it.from = '2026-01-01';
        return Object.assign(defaults(), { end: '2026-06-30', items: [it], feeMode: 'free', feeFree: '' });
      } },
    { t: 'Interessi moratori su più semestri',
      d: 'Capitale € 1.394,25, interessi moratori ex D.Lgs. 231/2002 dal 25.09.2025 al 21.09.2026, senza spese né compenso di precetto.',
      c: ['2° semestre 2025, 98 giorni: 1.394,25 × 10,15% × 98 / 365 = 38,00', '1° semestre 2026, 181 giorni: 1.394,25 × 10,15% × 181 / 365 = 70,18',
          '2° semestre 2026, 83 giorni: 1.394,25 × 10,40% × 83 / 365 = 32,97'],
      r: 'Interessi € 141,15; totale € 1.535,40.',
      load: function () {
        var it = newItem(); it.amount = '1.394,25'; it.type = 'mora'; it.from = '2025-09-25';
        return Object.assign(defaults(), { end: '2026-09-21', items: [it], feeMode: 'free', feeFree: '' });
      } },
    { t: 'Acconto imputato ex art. 1194 c.c.',
      d: 'Capitale € 5.000,00 con interessi moratori dal 01.01.2026; spese liquidate nel titolo del 15.12.2025 € 400,00; acconto di € 1.000,00 il 01.04.2026; conteggio al 30.06.2026, senza compenso di precetto.',
      c: ['Interessi dal 01.01 al 01.04.2026, 91 giorni: 5.000,00 × 10,15% × 91 / 365 = 126,53',
          'Acconto: 400,00 alle spese, 126,53 agli interessi, 473,47 al capitale; capitale residuo 4.526,53',
          'Interessi dal 02.04 al 30.06.2026, 90 giorni: 4.526,53 × 10,15% × 90 / 365 = 113,29',
          '5.000,00 + 126,53 + 113,29 + 400,00 − 1.000,00 = 4.639,82'],
      r: 'Totale € 4.639,82.',
      load: function () {
        var it = newItem(); it.amount = '5.000,00'; it.type = 'mora'; it.from = '2026-01-01';
        var p = newAcconto(); p.date = '2026-04-01'; p.amount = '1.000,00';
        return Object.assign(defaults(), { end: '2026-06-30', items: [it], spese: '400,00', feeMode: 'free', feeFree: '', acconti: [p], titleDate: '2025-12-15' });
      } },
    { t: 'Termini del precetto',
      d: 'Precetto notificato il 01.10.2026 con il termine di 10 giorni; istanza ex art. 492-bis presentata il 20.10.2026, esito comunicato il 10.11.2026.',
      c: ['10 giorni: 11.10.2026, domenica, prorogato a lunedì 12.10.2026; esecuzione dal 13.10.2026',
          '90 giorni: 30.12.2026, più 21 giorni di sospensione (dal 20.10 al 10.11.2026) = 20.01.2027'],
      r: 'Efficacia fino a mercoledì 20.01.2027.',
      termini: true,
      load: function () {
        return Object.assign(JSON.parse(JSON.stringify(state)), { tNotifica: '2026-10-01', tGiorni: '10', tBis: true, tBisFrom: '2026-10-20', tBisTo: '2026-11-10' });
      } }
  ];
  function renderCases() {
    $('#casesBody').innerHTML = '<p>Conteggi svolti a mano, con i tassi indicati in «Tassi e parametri usati». Caricali nel calcolatore e confronta il risultato.</p>' +
      CASES.map(function (c, i) {
        return '<div class="case"><h3>' + esc(c.t) + '</h3><p>' + esc(c.d) + '</p><div class="calc">' +
          c.c.map(function (l) { return '<div>' + esc(l) + '</div>'; }).join('') + '</div><p class="res">' + esc(c.r) + '</p>' +
          '<button type="button" class="linkbtn" data-case="' + i + '">Carica nel calcolatore</button></div>';
      }).join('');
    $$('[data-case]').forEach(function (b) {
      b.addEventListener('click', function () {
        var c = CASES[+b.dataset.case], prev = JSON.parse(JSON.stringify(state));
        state = c.load();
        refresh();
        var target = c.termini ? $('#termini') : ($('#prospetto').getBoundingClientRect().top < 0 || innerWidth < 960 ? $('#prospetto') : $('.intro'));
        target.scrollIntoView({ block: 'start' });
        showToast('Caso caricato: confronta il risultato.', function () { state = prev; refresh(); });
      });
    });
  }
  function renderRegistro() {
    $('#registroBody').innerHTML = '<p>Ogni modifica ai tassi, alle tabelle o ai criteri di calcolo, con la data in cui è stata pubblicata sul sito.</p><ul class="reg">' +
      TABELLE.registro.map(function (r) {
        return '<li><time datetime="' + esc(r[0]) + '">' + C.fmtDate(C.toDay(r[0])) + '</time>' + esc(r[1]) + '</li>';
      }).join('') + '</ul>';
  }
  function renderContact() {
    $('#mailBtn').href = 'mailto:' + SITO.email + '?subject=' + encodeURIComponent('Suggerimento per ' + SITO.nome);
    $('#mailText').textContent = SITO.email;
  }
  function openSection(id) {
    var d = document.getElementById(id);
    if (!d) return;
    d.open = true;
    d.scrollIntoView({ block: 'start' });
  }

  /* ---------- avvio ---------- */
  bindStatic();
  $('#btnExample').addEventListener('click', loadExample);
  $('#emptyExample').addEventListener('click', loadExample);
  $('#btnNew').addEventListener('click', newCalc);
  $('#toastUndo').addEventListener('click', function () {
    if (undoState) undoState();
    undoState = null;
    $('#toast').hidden = true;
  });
  $('#btnCopy').addEventListener('click', doCopy);
  $('#btnDocx').addEventListener('click', doDocx);
  $('#tIcs').addEventListener('click', doIcs);
  $('#btnPrint').addEventListener('click', function () { try { window.print(); } catch (e) { /* non disponibile */ } });
  $$('[data-open]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); openSection(a.dataset.open); history.replaceState(null, '', '#' + a.dataset.open); });
  });
  renderLegal();
  renderContact();
  renderRates();
  renderCases();
  renderRegistro();
  refresh();
  if (location.hash && document.getElementById(location.hash.slice(1)) && document.getElementById(location.hash.slice(1)).tagName === 'DETAILS') openSection(location.hash.slice(1));

  if ('IntersectionObserver' in window) {
    var bar = $('#mobilebar');
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { bar.classList.toggle('hide', en.isIntersecting); });
    }, { threshold: 0.15 }).observe($('#prospetto'));
  }
})();
