/*! calcolaprecetti.it - (c) 2026 il titolare indicato nelle Note legali (https://calcolaprecetti.it/note-legali/). Tutti i diritti riservati. Vietata la riproduzione, anche parziale, senza autorizzazione scritta. Licenza: file LICENSE. */
(function () {
  'use strict';
  // indirizzi della versione precedente (calcolaprecetti.it/#privacy e simili): ora sono pagine
  var MOVED = { tassi: '/tassi/', verifica: '/tassi/#verifica', registro: '/tassi/#registro', privacy: '/privacy/', 'note-legali': '/note-legali/', termini: '/termini-precetto/' };
  if (MOVED[location.hash.slice(1)]) { location.replace(MOVED[location.hash.slice(1)]); return; }
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
             acconti: [], titleDate: '', fonti: true };
  }
  var state = defaults();
  var last = null, caseShown = false, shownTotal = null, sweepTimer = null;

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
  var TEXTS = [['endDate', 'end'], ['spese', 'spese'], ['compensi', 'compensi'], ['feeFree', 'feeFree'], ['titleDate', 'titleDate']];
  var CHECKS = [['optIva', 'iva'], ['optRf', 'rf'], ['optCpa', 'cpa'], ['optFonti', 'fonti']];

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
    if (empty) { shownTotal = null; $('#mbTotal').classList.remove('tot-hl'); return; }

    $('#table tbody').innerHTML = res.rows.map(function (r) {
      return '<tr' + (r.acconto ? ' class="acc"' : '') + '><td>' + esc(r.label) + '</td><td class="amt">' + C.eur(r.amount) + '</td></tr>';
    }).join('') + '<tr class="total"><td>TOTALE COMPLESSIVO</td><td class="amt"><span class="tot-hl">' + C.eur(res.total) + '</span></td></tr>';
    animate(res.total);
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

  /* ---------- due animazioni minime: il prospetto entra quando compare, l'evidenziatore ripassa il totale quando cambia ---------- */
  function sweep(el) { el.classList.remove('sweep'); void el.offsetWidth; el.classList.add('sweep'); }
  function animate(total) {
    var first = shownTotal === null;
    if (first) sweep($('#sheet'));
    $('#mbTotal').classList.add('tot-hl');
    if (total !== shownTotal) {
      clearTimeout(sweepTimer);
      sweepTimer = setTimeout(function () { // a calcolo fermo, non a ogni tasto
        var t = $('#table tr.total .tot-hl');
        if (t) sweep(t);
        sweep($('#mbTotal'));
      }, first ? 250 : 450);
    }
    shownTotal = total;
  }

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
    if (caseShown) { caseShown = false; $('#caseMsg').hidden = true; } // il caso di verifica resta indicato finché non si cambia un dato
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

  /* ---------- piè di pagina e contatti ---------- */
  function renderFoot() {
    $$('.js-updated').forEach(function (e) { e.textContent = TABELLE.aggiornamento; });
    $$('.js-titolare').forEach(function (e) { e.textContent = SITO.titolare; });
  }
  function renderContact() {
    $('#mailBtn').href = 'mailto:' + SITO.email + '?subject=' + encodeURIComponent('Suggerimento per ' + SITO.nome);
    $('#mailText').textContent = SITO.email;
  }

  /* ---------- casi di verifica: la pagina «Tassi e verifiche» apre /#caso-1, /#caso-2... (dati in core.js, CASI) ---------- */
  function caseFromHash() {
    var m = /^#caso-(\d+)$/.exec(location.hash), c = m && typeof CASI !== 'undefined' ? CASI[+m[1] - 1] : null;
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
  $('#btnPrint').addEventListener('click', function () { try { window.print(); } catch (e) { /* non disponibile */ } });
  renderFoot();
  renderContact();
  refresh();
  caseFromHash();
  window.addEventListener('hashchange', function () { // stessa pagina: indirizzo cambiato a mano o caso aperto di nuovo
    if (MOVED[location.hash.slice(1)]) location.replace(MOVED[location.hash.slice(1)]);
    else caseFromHash();
  });

  if ('IntersectionObserver' in window) {
    var bar = $('#mobilebar');
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { bar.classList.toggle('hide', en.isIntersecting); });
    }, { threshold: 0.15 }).observe($('#prospetto'));
  }
})();
