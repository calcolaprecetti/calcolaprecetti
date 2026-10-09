/*! calcolaprecetti.it - (c) 2026 il titolare indicato nelle Note legali (https://calcolaprecetti.it/note-legali/). Tutti i diritti riservati. Vietata la riproduzione, anche parziale, senza autorizzazione scritta. Licenza: file LICENSE. */
/* Pagina dei termini del precetto: 10 e 90 giorni (artt. 480-482 c.p.c.), sospensione ex art. 492-bis, calendario */
(function () {
  'use strict';
  if (typeof Core === 'undefined') return;
  var C = Core;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function vuoto() { return { notifica: '', giorni: '10', bis: false, bisFrom: '', bisTo: '' }; }
  var st = vuoto(), lastT = null;
  var FIELDS = [['tNotifica', 'notifica'], ['tGiorni', 'giorni'], ['tBisFrom', 'bisFrom'], ['tBisTo', 'bisTo']];

  function sync() {
    FIELDS.forEach(function (f) { $('#' + f[0]).value = st[f[1]]; });
    $('#tBis').checked = !!st.bis;
  }

  function dayFull(n) { return C.weekday(n) + ' ' + C.fmtDate(n); }
  function why(n) { var h = C.holiday(n); return h === 'domenica' ? 'di domenica' : h ? 'in un giorno festivo' : 'di sabato'; }
  function render() {
    $('#tBisFields').hidden = !st.bis;
    var t = C.termini({ notifica: st.notifica, giorni: st.giorni, bis: st.bis, bisFrom: st.bisFrom, bisTo: st.bisTo });
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

  /* ---------- calendario: file .ics nel browser, collegamenti a Google Calendar e Outlook.com ---------- */
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

  /* ---------- caso di verifica aperto dalla pagina «Tassi e verifiche» (#caso-4; dati in core.js, CASI) ---------- */
  function caseFromHash() {
    var m = /^#caso-(\d+)$/.exec(location.hash), c = m && typeof CASI !== 'undefined' ? CASI[+m[1] - 1] : null;
    if (!c || c.pagina !== 'termini') return;
    st = Object.assign(vuoto(), JSON.parse(JSON.stringify(c.dati)));
    sync();
    render();
    var msg = $('#tCase');
    msg.textContent = 'Caso di verifica «' + c.titolo + '». Risultato atteso: ' + c.risultato.charAt(0).toLowerCase() + c.risultato.slice(1);
    msg.hidden = false;
    if (history.replaceState) history.replaceState(null, '', location.pathname + location.search);
    (innerWidth < 860 ? $('.termini-out') : $('#termini')).scrollIntoView({ block: 'start' }); // sul telefono, direttamente ai risultati
  }
  function changed() { // cambiando un dato, l'indicazione del caso di verifica non vale più
    $('#tCase').hidden = true;
    render();
  }

  /* ---------- avvio ---------- */
  FIELDS.forEach(function (f) {
    var el = $('#' + f[0]);
    el.addEventListener('input', function () { st[f[1]] = el.value; changed(); });
  });
  $('#tBis').addEventListener('change', function (e) { st.bis = e.target.checked; changed(); });
  $('#tIcs').addEventListener('click', doIcs);
  $$('.js-updated').forEach(function (e) { e.textContent = TABELLE.aggiornamento; });
  if (typeof SITO !== 'undefined') {
    $$('.js-titolare').forEach(function (e) { e.textContent = SITO.titolare; });
    var ml = $('#mailBtn'), mt = $('#mailText');
    if (ml) ml.href = 'mailto:' + SITO.email + '?subject=' + encodeURIComponent('Suggerimento per ' + SITO.nome);
    if (mt) mt.textContent = SITO.email;
  }
  sync();
  render();
  caseFromHash();
  window.addEventListener('hashchange', caseFromHash);
})();
