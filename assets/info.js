/*! calcolaprecetti.it - (c) 2026 il titolare indicato nelle Note legali (https://calcolaprecetti.it/note-legali/). Tutti i diritti riservati. Vietata la riproduzione, anche parziale, senza autorizzazione scritta. Licenza: file LICENSE. */
/* Pagine informative: tassi e verifiche, privacy, note legali. Tutto viene da core.js (TABELLE, SITO, CASI). */
(function () {
  'use strict';
  if (typeof Core === 'undefined') return;
  var C = Core;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function todayIso() { var d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  var today = C.toDay(todayIso());

  /* ---------- piè di pagina e contatti ---------- */
  $$('.js-updated').forEach(function (e) { e.textContent = TABELLE.aggiornamento; });
  $$('.js-titolare').forEach(function (e) { e.textContent = SITO.titolare; });
  var ml = $('#mailBtn'), mt = $('#mailText');
  if (ml) ml.href = 'mailto:' + SITO.email + '?subject=' + encodeURIComponent('Suggerimento per ' + SITO.nome);
  if (mt) mt.textContent = SITO.email;

  /* ---------- tassi in vigore ---------- */
  var leg = C.rowAt(C.LEG, today), mora = C.moraNow(today);
  if ($('#nowLegal') && leg) {
    $('#nowLegal').textContent = C.pct(leg[1]);
    $('#nowLegalYear').textContent = new Date(today * 86400000).getUTCFullYear();
    $('#nowLegalSrc').textContent = C.legalSource(today) + '.';
  }
  if ($('#nowMora') && mora.rate !== null) {
    $('#nowMora').textContent = C.pct(mora.rate);
    $('#nowMoraSem').textContent = mora.sem;
    $('#nowMoraSrc').textContent = 'Tasso BCE ' + C.pct(mora.base) + ' + 8 punti. ' + mora.src + '.' +
      (mora.pending ? ' In attesa del comunicato per il semestre in corso.' : '');
  }

  /* ---------- interessi legali dal 1997 ---------- */
  var tl = $('#tabLegali');
  if (tl) {
    var rows = TABELLE.legali.slice().reverse().map(function (r, i, arr) {
      var y = +r[0].slice(0, 4);
      var to = i === 0 ? +TABELLE.legaliPubblicatiFinoAl.slice(0, 4) : +arr[i - 1][0].slice(0, 4) - 1;
      return '<tr><td>' + (to > y ? y + '–' + to : y) + '</td><td class="r"><strong>' + C.pct(r[1]) + '</strong></td><td class="s">' + esc(r[2] || 'Decreto MEF') + '</td></tr>';
    }).join('');
    tl.innerHTML = '<thead><tr><th>Anni</th><th class="r">Tasso</th><th>Fonte</th></tr></thead><tbody>' + rows + '</tbody>';
  }

  /* ---------- interessi moratori dal 2002 ---------- */
  var tm = $('#tabMora');
  if (tm) {
    var out = [], last = C.toDay(TABELLE.moraPubblicatiFinoAl), endY = new Date(last * 86400000).getUTCFullYear(), d2013 = C.toDay('2013-01-01');
    for (var y = endY; y >= 2002; y--) {
      for (var h = 2; h >= 1; h--) {
        var day = C.toDay(y + (h === 1 ? '-01-01' : '-07-01'));
        if (day > last || (y === 2002 && h === 1)) continue;
        var b = C.rateAt(C.BCE, day), row = C.rowAt(C.BCE, day), own = row && row[0] === day && row[2] ? row[2] : '';
        out.push('<tr><td>' + h + '° sem. ' + y + '</td><td class="r">' + C.pct(b) + '</td><td class="r">' +
          (day >= d2013 ? '<strong>' + C.pct(b + TABELLE.maggiorazioneMora) + '</strong>' : '—') + '</td><td class="r">' + C.pct(b + 7) +
          '</td><td class="s">' + esc(own || 'Comunicato MEF') + '</td></tr>');
      }
    }
    tm.innerHTML = '<thead><tr><th>Periodo</th><th class="r">Tasso BCE</th><th class="r">Contratti dal 2013</th>' +
      '<th class="r">Contratti fino al 2012</th><th>Fonte</th></tr></thead><tbody>' + out.join('') + '</tbody>';
  }

  /* ---------- compenso del precetto ---------- */
  var tp = $('#tabPrecetto');
  if (tp) {
    tp.innerHTML = '<thead><tr><th>Valore del credito</th><th class="r">Minimo</th><th class="r">Medio</th><th class="r">Massimo</th></tr></thead><tbody>' +
      TABELLE.precetto.map(function (t, i) {
        var from = i === 0 ? 0.01 : TABELLE.precetto[i - 1][0] + 0.01;
        return '<tr><td>da ' + C.eur(from) + ' a ' + C.eur(t[0]) + '</td><td class="r">' + C.eur(t[1] / 2) + '</td><td class="r"><strong>' +
          C.eur(t[1]) + '</strong></td><td class="r">' + C.eur(t[1] * 1.5) + '</td></tr>';
      }).join('') + '</tbody>';
  }
  $$('.js-accessori').forEach(function (e) {
    e.textContent = 'rimborso forfettario ' + TABELLE.rimborsoForfettario + '%, C.P.A. ' + TABELLE.cpa + '% e, se dovuta, I.V.A. ' + TABELLE.iva + '%';
  });

  /* ---------- casi di verifica ---------- */
  var cb = $('#casiBody');
  if (cb && typeof CASI !== 'undefined') {
    var url = { precetto: cb.dataset.urlPrecetto || '/', termini: cb.dataset.urlTermini || '/termini-precetto/' };
    cb.innerHTML = CASI.map(function (c, i) {
      return '<div class="case"><h3>' + esc(c.titolo) + '</h3><p>' + esc(c.testo) + '</p><div class="calc">' +
        c.conto.map(function (l) { return '<div>' + esc(l) + '</div>'; }).join('') + '</div><p class="res">' + esc(c.risultato) + '</p>' +
        '<a class="linkbtn" href="' + esc(url[c.pagina] + '#caso-' + (i + 1)) + '">' +
        (c.pagina === 'termini' ? 'Apri nel calcolo dei termini' : 'Apri nel calcolo del precetto') + '</a></div>';
    }).join('');
  }

  /* ---------- registro degli aggiornamenti ---------- */
  var rg = $('#registroBody');
  if (rg) {
    rg.innerHTML = '<ul class="reg">' + TABELLE.registro.map(function (r) {
      return '<li><time datetime="' + esc(r[0]) + '">' + C.fmtDate(C.toDay(r[0])) + '</time>' + esc(r[1]) + '</li>';
    }).join('') + '</ul>';
  }

  /* ---------- privacy e note legali ---------- */
  function v(s) { return /^\[.*\]$/.test(s) ? '<mark style="background:var(--mark)">' + esc(s) + '</mark>' : esc(s); }
  var pb = $('#privacyBody');
  if (pb) {
    pb.innerHTML =
      '<h2>Titolare del trattamento</h2><p>' + v(SITO.titolare) + ', contattabile all\'indirizzo ' + v(SITO.email) + '.</p>' +
      '<h2>Quali dati vengono trattati</h2>' +
      '<p>Il sito non usa cookie né altri strumenti di tracciamento e non carica contenuti da siti di terzi. I dati inseriti nei calcoli sono elaborati solo nel tuo browser: non vengono inviati al titolare né a terzi e non vengono conservati, quindi si cancellano chiudendo o ricaricando la pagina.</p>' +
      '<p>Come per qualsiasi sito, il servizio di hosting (' + esc(SITO.hosting) + ') registra nei propri log tecnici alcuni dati di navigazione, come indirizzo IP, data e ora della richiesta, pagina visitata e tipo di browser, per la sicurezza e il funzionamento del servizio. Il titolare non usa questi dati per identificare i visitatori né per profilazione.</p>' +
      '<h2>Se scrivi un suggerimento</h2><p>Se scrivi a ' + v(SITO.email) + ', i dati contenuti nel messaggio (indirizzo email, eventuale nome e contenuto) sono usati solo per rispondere e valutare il suggerimento, sulla base del legittimo interesse (art. 6, par. 1, lett. f, GDPR), e vengono cancellati quando non servono più. La casella di posta è fornita da ' + esc(SITO.fornitoreEmail) + '. Ti chiedo di non inserire nei messaggi dati personali di clienti o di terzi.</p>' +
      '<h2>Finalità e base giuridica</h2><p>Sicurezza e corretto funzionamento del sito, sulla base del legittimo interesse (art. 6, par. 1, lett. f, Reg. UE 2016/679).</p>' +
      '<h2>Destinatari e trasferimenti</h2><p>I dati di navigazione sono trattati dal fornitore di hosting secondo la propria informativa. ' + esc(SITO.trasferimento) + '</p>' +
      '<h2>Collegamenti a Google Calendar e Outlook</h2><p>Nella pagina dei <a href="/termini-precetto/">termini del precetto</a> trovi due collegamenti facoltativi che aprono Google Calendar o Outlook.com con la scadenza già compilata. Se li usi, la data e il titolo dell\'appuntamento vengono inviati al servizio scelto, che li tratta come titolare autonomo secondo la propria informativa; non viene inviato nulla finché non li clicchi. Il file da scaricare, invece, resta sul tuo dispositivo.</p>' +
      '<h2>Collegamenti a LinkedIn</h2><p>I collegamenti alla pagina LinkedIn del sito e al profilo del titolare aprono il sito di LinkedIn, che tratta i dati di chi lo visita secondo la propria informativa. Le pagine di calcolaprecetti.it non caricano nulla da LinkedIn.</p>' +
      '<h2>Conservazione</h2><p>I dati di navigazione sono conservati dal fornitore per il tempo necessario alle finalità di sicurezza, secondo le sue politiche.</p>' +
      '<h2>Diritti</h2><p>Puoi esercitare i diritti previsti dagli artt. 15-22 del GDPR (accesso, rettifica, cancellazione, limitazione, opposizione) scrivendo a ' + v(SITO.email) + ' e proporre reclamo al Garante per la protezione dei dati personali (garanteprivacy.it).</p>' +
      '<p class="hint">Ultimo aggiornamento: ' + esc(SITO.informativaAggiornata) + '.</p>';
  }
  var lb = $('#legalBody');
  if (lb) {
    lb.innerHTML =
      '<p>' + esc(SITO.nome) + ' è uno strumento gratuito di ausilio al calcolo delle somme da intimare con l\'atto di precetto e dei relativi termini. I risultati dipendono dai dati inseriti e dalle tabelle riportate nella pagina <a href="/tassi/">Tassi e verifiche</a>: vanno sempre verificati prima dell\'uso in un atto e non costituiscono consulenza legale.</p>' +
      '<p>Nei limiti consentiti dalla legge, il titolare non risponde di errori od omissioni derivanti dall\'uso dello strumento.</p>' +
      '<p>Titolare del sito: ' + v(SITO.titolare) + ', ' + v(SITO.email) + '.</p>' +
      '<h2>Diritti d\'autore</h2><p>Il codice del sito, i testi, la grafica e il logo sono opere protette dalla legge sul diritto d\'autore (L. 22 aprile 1941, n. 633), compresi i programmi per elaboratore. Tutti i diritti sono riservati al titolare: non è consentito copiarli, modificarli o riutilizzarli, in tutto o in parte, senza autorizzazione scritta. Resta libero l\'uso dello strumento per i propri calcoli. I tassi e i dati normativi riportati provengono da fonti pubbliche.</p>' +
      '<p>Caratteri tipografici: EB Garamond e Titillium Web, con licenza SIL Open Font License 1.1.</p>';
  }
})();
