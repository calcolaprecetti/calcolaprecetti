/*! calcolaprecetti.it - (c) 2026 il titolare indicato nelle Note legali (https://calcolaprecetti.it/note-legali/). Tutti i diritti riservati. Vietata la riproduzione, anche parziale, senza autorizzazione scritta. Licenza: file LICENSE. */
/* Pagine delle guide: dati del piè di pagina, collegamento da mandare al cliente, tassi in vigore scritti nel testo e i tre calcoli rapidi
   (data-quick="mora", "termini", "costi"). Usa il motore e le tabelle di core.js: qui non ci sono tassi. */
(function () {
  'use strict';
  if (typeof Core === 'undefined') return;
  var C = Core;
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function todayIso() { var d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  var MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
  function dayMonth(n) { var d = new Date(n * 86400000), g = d.getUTCDate(); return g + (g === 1 ? '°' : '') + ' ' + MESI[d.getUTCMonth()] + ' ' + d.getUTCFullYear(); }
  function longDate(n) { return C.weekday(n) + ' ' + dayMonth(n); }
  function giorni(n) { return n === 1 ? '1 giorno' : n + ' giorni'; }
  function fmtMoney(el) { var v = C.parseNum(el.value); el.value = isFinite(v) ? C.num(v) : ''; }
  var today = C.toDay(todayIso());

  /* ---------- piè di pagina e contatti ---------- */
  $$('.js-updated').forEach(function (e) { e.textContent = TABELLE.aggiornamento; });
  if (typeof SITO !== 'undefined') {
    $$('.js-titolare').forEach(function (e) { e.textContent = SITO.titolare; });
    var ml = document.getElementById('mailBtn'), mt = document.getElementById('mailText');
    if (ml) ml.href = 'mailto:' + SITO.email + '?subject=' + encodeURIComponent('Suggerimento per ' + SITO.nome);
    if (mt) mt.textContent = SITO.email;
  }

  /* ---------- barra per gli avvocati: copia o condividi il collegamento della guida ---------- */
  var cl = $('#copyLink'), sh = $('#shareLink'), cm = $('#copyMsg');
  if (cl && cm) {
    var link = function () { return location.href.split('#')[0]; };
    var done = function (ok) {
      cm.textContent = ok ? 'Collegamento copiato: incollalo nella mail o nel messaggio.' : 'Copia questo collegamento: ' + link();
    };
    var legacy = function () { // browser senza appunti asincroni
      var ta = document.createElement('textarea'), ok = false;
      ta.value = link();
      ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;left:-9999px;top:0';
      document.body.appendChild(ta);
      ta.select();
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      done(ok);
    };
    cl.addEventListener('click', function () {
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(link()).then(function () { done(true); }, legacy);
      else legacy();
    });
    if (sh && navigator.share) {
      sh.hidden = false;
      sh.addEventListener('click', function () {
        navigator.share({ title: document.title, url: link() }).catch(function (e) {
          if (!e || e.name !== 'AbortError') cl.click(); // condivisione non disponibile: si copia il collegamento
        });
      });
    }
  }

  /* ---------- tassi in vigore, scritti nel testo ---------- */
  var now = C.moraNow(today), legale = C.rateAt(C.LEG, today);
  if (now.rate !== null) $$('.js-mora-rate').forEach(function (e) { e.textContent = C.pct(now.rate); });
  if (legale !== null) $$('.js-legal-rate').forEach(function (e) { e.textContent = C.pct(legale); });

  /* ---------- quanto ti spetta oggi: interessi di mora e 40 euro ---------- */
  var qm = $('[data-quick=mora]');
  if (qm) {
    var cap = $('#qCap'), scad = $('#qScad'), outM = $('#qOutMora');
    var runM = function () {
      var v = C.parseNum(cap.value), s = C.toDay(scad.value);
      if (!(v > 0) || s === null) { outM.innerHTML = '<p class="empty">Scrivi l\'importo della fattura e la data di scadenza.</p>'; return; }
      if (s >= today) { outM.innerHTML = '<p class="empty">La fattura non è ancora scaduta: gli interessi partono dal giorno dopo la scadenza.</p>'; return; }
      var r = C.interest(v, 'mora', s + 1, today, {});
      var note = [];
      if (r.warnings.indexOf('moraTooOld') >= 0) note.push('I tassi in tabella partono dal 1° luglio 2002: i periodi precedenti non sono contati.');
      if (r.warnings.indexOf('pre2013') >= 0) note.push('Per i contratti conclusi prima del 2013 il tasso è più basso di un punto: usa il calcolo completo.');
      if (r.warnings.indexOf('future') >= 0) note.push('Per il semestre in corso il tasso non è ancora pubblicato: è stato usato l\'ultimo disponibile.');
      var tot = C.r2(v + r.total + 40);
      outM.innerHTML =
        '<dl class="totals">' +
        '<div><dt>Giorni di ritardo</dt><dd>' + (today - s) + '</dd></div>' +
        '<div><dt>Interessi di mora a oggi</dt><dd>' + C.eur(r.total) + '</dd></div>' +
        '<div><dt>Risarcimento forfettario</dt><dd>' + C.eur(40) + '</dd></div>' +
        '<div class="big"><dt>Totale che puoi chiedere</dt><dd>' + C.eur(tot) + '</dd></div>' +
        '</dl>' +
        '<p class="hint">Calcolo ' + (/^(8|11) /.test(dayMonth(today)) ? 'all\'' : 'al ') + dayMonth(today) + ', con il tasso di ogni semestre. I € 40 spettano per ogni fattura: qui sono contati una volta.</p>' +
        note.map(function (m) { return '<p class="warn">' + esc(m) + '</p>'; }).join('');
    };
    cap.addEventListener('input', runM);
    cap.addEventListener('blur', function () { fmtMoney(cap); });
    scad.addEventListener('input', runM);
    runM();
  }

  /* ---------- le date del precetto: 10 e 90 giorni ---------- */
  var qt = $('[data-quick=termini]');
  if (qt) {
    var nt = $('#qNotifica'), outT = $('#qOutTermini');
    if (!nt.value) nt.value = todayIso();
    var perche = function (n) { var h = C.holiday(n); return h === 'domenica' ? 'di domenica' : h ? 'in un giorno festivo' : 'di sabato'; };
    var runT = function () {
      var t = C.termini({ notifica: nt.value, giorni: '10', bis: false });
      if (!t) { outT.innerHTML = '<p class="empty">Indica la data di notifica.</p>'; return; }
      var n = today - t.notifica, stato;
      if (n < 0) stato = 'La data indicata è nel futuro.';
      else if (n === 0) stato = 'Notifica di oggi: per pagare restano ' + giorni(t.adempiereProrogato - today) + '.';
      else if (today <= t.adempiereProrogato) stato = 'Oggi è il giorno ' + n + ': per pagare ' + (t.adempiereProrogato === today ? 'è l\'ultimo giorno' : 'restano ' + giorni(t.adempiereProrogato - today)) + '.';
      else if (today <= t.efficaciaProrogata) stato = 'Oggi è il giorno ' + n + ': il pignoramento può già iniziare. Al termine dei 90 giorni ' + (t.efficaciaProrogata === today ? 'manca solo oggi' : 'mancano ' + giorni(t.efficaciaProrogata - today)) + '.';
      else stato = 'I 90 giorni sono passati: se il pignoramento non è iniziato, serve un nuovo precetto.';
      outT.innerHTML =
        '<p class="g-today">' + esc(stato) + '</p>' +
        '<dl class="tlist">' +
        '<div><dt>Ultimo giorno per pagare</dt><dd>' + longDate(t.adempiereProrogato) +
          (t.adempiereProrogato !== t.adempiere ? '<span class="n">Il decimo giorno, ' + dayMonth(t.adempiere) + ', cade ' + perche(t.adempiere) + '.</span>' : '') + '</dd></div>' +
        '<div><dt>Il pignoramento può iniziare da</dt><dd>' + longDate(t.esecuzioneDal) + '</dd></div>' +
        '<div><dt>Il precetto scade</dt><dd>' + longDate(t.efficaciaProrogata) +
          (t.efficaciaProrogata !== t.efficacia ? '<span class="n">Il novantesimo giorno, ' + dayMonth(t.efficacia) + ', cade ' + perche(t.efficacia) + '.</span>' : '') + '</dd></div>' +
        '</dl>';
    };
    nt.addEventListener('input', runT);
    runT();
  }

  /* ---------- quanto costa il decreto ingiuntivo: legge i numeri dalla tabella della pagina ---------- */
  var qc = $('[data-quick=costi]');
  if (qc) {
    var val = $('#qValore'), outC = $('#qOutCosti'), trs = $$('#costiTable tbody tr');
    var gdp = +qc.dataset.gdp, forf = +qc.dataset.forf, esente = +qc.dataset.esente;
    var runC = function () {
      var v = C.parseNum(val.value), row = null;
      trs.forEach(function (tr) { tr.classList.remove('on'); });
      if (!(v > 0)) { outC.innerHTML = '<p class="empty">Scrivi l\'importo del credito.</p>'; return; }
      for (var i = 0; i < trs.length; i++) {
        var max = trs[i].dataset.max ? +trs[i].dataset.max : Infinity;
        if (v <= max) { row = trs[i]; break; }
      }
      if (!row) return;
      row.classList.add('on');
      var pace = v <= gdp, cu = +row.dataset.cu, f = pace && v <= esente ? 0 : forf, comp = row.dataset.comp ? +row.dataset.comp : null;
      outC.innerHTML =
        '<dl class="totals">' +
        '<div><dt>Decide</dt><dd>' + (pace ? 'il giudice di pace' : 'il tribunale') + '</dd></div>' +
        '<div><dt>Contributo unificato</dt><dd>' + C.eur(cu) + '</dd></div>' +
        '<div><dt>Anticipazione forfettaria</dt><dd>' + (f ? C.eur(f) : 'non dovuta') + '</dd></div>' +
        '<div class="big"><dt>Costi vivi da anticipare</dt><dd>' + C.eur(cu + f) + '</dd></div>' +
        '</dl>' +
        '<p class="hint">' + (comp === null
          ? 'Oltre € 520.000,00 il compenso si calcola con gli aumenti previsti dai parametri.'
          : 'Compenso che il giudice può mettere a carico del debitore: in media ' + C.eur(comp) + ', da ' + C.eur(comp / 2) + ' a ' + C.eur(comp * 1.5) +
            ', più rimborso forfettario, cassa avvocati e IVA.') + '</p>';
    };
    val.addEventListener('input', runC);
    val.addEventListener('blur', function () { fmtMoney(val); });
    runC();
  }
})();
