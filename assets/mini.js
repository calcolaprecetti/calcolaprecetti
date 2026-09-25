/* Calcolatore compatto delle pagine per argomento: legge la configurazione da data-mini */
(function () {
  'use strict';
  var C = Core, box = document.getElementById('mini');
  if (!box || typeof C === 'undefined') return;
  var cfg = JSON.parse(box.dataset.mini || '{}'), type = cfg.type || 'mora';
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function todayIso() { var d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }

  var st = { cap: '', from: '', to: todayIso(), rate: '', forfait: false, fattura: '', giorni: '30' };

  function fmtInput(el) { var v = C.parseNum(el.value); el.value = isFinite(v) ? C.num(v) : ''; }

  function calc() {
    var cap = C.parseNum(st.cap), from = C.toDay(st.from), to = C.toDay(st.to);
    var out = $('#miniOut'), warn = $('#miniWarn'), empty = $('#miniEmpty');
    var msgs = [];
    if (!(cap > 0) || from === null || to === null) {
      empty.hidden = false; out.hidden = true; warn.innerHTML = '';
      $('#miniActions').hidden = true;
      return;
    }
    empty.hidden = true;
    var r = C.interest(cap, type, from, to, { rate: C.parseNum(st.rate), domanda: null });
    r.warnings.forEach(function (w) {
      if (w === 'fromAfterEnd') msgs.push('La decorrenza è successiva alla data finale: non maturano interessi.');
      if (w === 'moraTooOld') msgs.push('I tassi in tabella partono dal 01.01.2013.');
      if (w === 'legalTooOld') msgs.push('I tassi in tabella partono dal 01.01.1997.');
      if (w === 'future') msgs.push("Per i periodi successivi all'ultimo tasso pubblicato è stato usato l'ultimo disponibile.");
    });
    warn.innerHTML = msgs.map(function (m) { return '<p class="warn">' + esc(m) + '</p>'; }).join('');
    var forfait = st.forfait ? 40 : 0;
    var tot = C.r2(cap + r.total + forfait);
    out.hidden = false;
    $('#miniActions').hidden = false;
    var srcs = [], seen = {};
    r.segments.forEach(function (s) { if (s.src && !seen[s.src]) { seen[s.src] = 1; srcs.push(s.src); } });
    $('#miniTable').innerHTML =
      '<thead><tr><th>Periodo</th><th class="r">Giorni</th><th class="r">Tasso</th><th class="r">Interessi</th></tr></thead><tbody>' +
      r.segments.map(function (s) {
        return '<tr class="segrow"><td>dal ' + C.fmtDate(s.s) + ' al ' + C.fmtDate(s.e) + '</td><td class="r">' + s.days +
          '</td><td class="r">' + C.pct(s.rate) + '</td><td class="r">' + C.eur(s.amount) + '</td></tr>' +
          '<tr class="src"><td colspan="4">' + esc(s.src) + '</td></tr>';
      }).join('') + '</tbody><tfoot><tr><td colspan="3">Totale interessi</td><td class="r">' + C.eur(r.total) + '</td></tr></tfoot>';
    $('#miniTotals').innerHTML =
      '<div><dt>Interessi maturati</dt><dd>' + C.eur(r.total) + '</dd></div>' +
      (forfait ? '<div><dt>Risarcimento forfettario (art. 6)</dt><dd>' + C.eur(forfait) + '</dd></div>' : '') +
      '<div class="big"><dt>Capitale e interessi</dt><dd>' + C.eur(tot) + '</dd></div>';
    $('#miniSources').textContent = srcs.length ? 'Fonti dei tassi: ' + srcs.join('; ') + '.' : '';
    last = { cap: cap, r: r, forfait: forfait, tot: tot, srcs: srcs, from: from, to: to };
  }
  var last = null;

  function rowsForCopy() {
    var rows = [['Capitale', C.eur(last.cap)]];
    last.r.segments.forEach(function (s) {
      rows.push(['Interessi dal ' + C.fmtDate(s.s) + ' al ' + C.fmtDate(s.e) + ' (' + s.days + ' giorni, ' + C.pct(s.rate) + ')', C.eur(s.amount)]);
    });
    if (last.forfait) rows.push(['Risarcimento forfettario ex art. 6 D.Lgs. n. 231/2002', C.eur(last.forfait)]);
    return rows;
  }
  function htmlTable() {
    var td = 'border:1px solid #000;padding:4pt 6pt;font-family:Garamond,serif;font-size:12pt;';
    var body = rowsForCopy().map(function (r) {
      return '<tr><td style="' + td + '">' + esc(r[0]) + '</td><td style="' + td + 'text-align:right;white-space:nowrap">' + r[1] + '</td></tr>';
    }).join('');
    body += '<tr><td style="' + td + 'font-weight:bold">TOTALE</td><td style="' + td + 'text-align:right;font-weight:bold;white-space:nowrap">' + C.eur(last.tot) + '</td></tr>';
    return '<table style="border-collapse:collapse;width:100%" cellspacing="0">' + body + '</table>' +
      (last.srcs.length ? '<p style="font-family:Garamond,serif;font-size:10pt;margin:6pt 0 0">Fonti dei tassi: ' + esc(last.srcs.join('; ')) + '.</p>' : '');
  }
  function plain() {
    return rowsForCopy().map(function (r) { return r[0] + '\t' + r[1]; }).join('\n') + '\nTOTALE\t' + C.eur(last.tot);
  }
  function copy() {
    if (!last) return;
    var btn = $('#miniCopy'), old = btn.textContent;
    function done(ok) { btn.textContent = ok ? 'Copiato' : 'Copia non riuscita'; setTimeout(function () { btn.textContent = old; }, 1800); }
    if (navigator.clipboard && window.ClipboardItem) {
      navigator.clipboard.write([new ClipboardItem({
        'text/html': new Blob([htmlTable()], { type: 'text/html' }),
        'text/plain': new Blob([plain()], { type: 'text/plain' })
      })]).then(function () { done(true); }, function () { fallback(); });
    } else fallback();
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = plain();
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      done(ok);
    }
  }

  /* ---------- campi ---------- */
  $$('[data-s]').forEach(function (el) {
    var k = el.dataset.s;
    if (el.type === 'checkbox') {
      el.checked = !!st[k];
      el.addEventListener('change', function () { st[k] = el.checked; calc(); });
    } else {
      el.value = st[k] || '';
      el.addEventListener('input', function () { st[k] = el.value; calc(); });
      if (el.dataset.money !== undefined) el.addEventListener('blur', function () { fmtInput(el); st[k] = el.value; });
    }
  });
  var fat = $('#miniFattura');
  if (fat) {
    fat.addEventListener('click', function () {
      var d = C.toDay(st.fattura), g = parseInt(st.giorni, 10);
      if (d === null || !(g >= 0)) { $('#miniFatturaMsg').textContent = 'Indica la data della fattura e i giorni di termine.'; return; }
      var start = d + g + 1;
      st.from = C.isoOf(start);
      $('[data-s=from]').value = st.from;
      $('#miniFatturaMsg').textContent = 'Decorrenza: ' + C.fmtDate(start) + ' (giorno successivo alla scadenza).';
      calc();
    });
  }
  if ($('#miniCopy')) $('#miniCopy').addEventListener('click', copy);

  /* ---------- tabella dei tassi della pagina ---------- */
  var tbl = document.getElementById('ratesTable');
  if (tbl) {
    var rows = [], y0 = 2013, last2 = C.toDay(TABELLE.moraPubblicatiFinoAl), p = new Date(last2 * 86400000);
    for (var y = p.getUTCFullYear(); y >= y0; y--) {
      for (var h = 2; h >= 1; h--) {
        var day = C.toDay(y + '-' + (h === 1 ? '01-01' : '07-01'));
        if (day > last2) continue;
        var b = C.rateAt(C.BCE, day), row = C.rowAt(C.BCE, day), own = row && row[0] === day && row[2] ? row[2] : '';
        rows.push('<tr><td>' + h + '° semestre ' + y + '</td><td class="r">' + C.pct(b) + '</td><td class="r"><strong>' +
          C.pct(b + TABELLE.maggiorazioneMora) + '</strong></td><td class="s">' + esc(own || '—') + '</td></tr>');
      }
    }
    tbl.innerHTML = '<thead><tr><th>Periodo</th><th class="r">Tasso BCE</th><th class="r">Tasso di mora</th><th>Fonte</th></tr></thead><tbody>' +
      rows.join('') + '</tbody>';
  }
  var upd = document.getElementById('updated');
  if (upd) upd.textContent = TABELLE.aggiornamento;
  var ml = document.getElementById('mailBtn');
  if (ml && typeof SITO !== 'undefined') {
    ml.href = 'mailto:' + SITO.email + '?subject=' + encodeURIComponent('Suggerimento per ' + SITO.nome);
    if ($('#mailText')) $('#mailText').textContent = SITO.email;
  }
  calc();
})();
