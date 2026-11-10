// Verifica degli esempi numerici delle guide con il motore del sito (assets/core.js): node _sorgenti/gen/calc.js
// core.js gira nel browser: qui bastano finte window, document e navigator.
global.window = global;
global.document = { addEventListener() {}, removeEventListener() {}, querySelector() { return null; }, querySelectorAll() { return []; }, getElementById() { return null; }, readyState: 'complete', documentElement: { lang: 'it' }, referrer: '', title: '' };
global.navigator = { doNotTrack: '1', globalPrivacyControl: true, sendBeacon() { return true; } };
global.location = { hostname: 'localhost', pathname: '/', search: '', hash: '', href: 'http://localhost/' };
global.addEventListener = () => {};
const fs = require('fs');
const code = fs.readFileSync(require('path').resolve(__dirname, '..', '..', 'assets', 'core.js'), 'utf8');
const { Core: C, TABELLE, SITO } = new Function(code + '; return {Core: Core, TABELLE: TABELLE, SITO: SITO};')();
const d = s => C.toDay(s);
function mora(cap, from, to) {
  const r = C.interest(cap, 'mora', d(from), d(to), {});
  console.log(`\nMORA ${cap} dal ${from} al ${to}: totale ${C.num(r.total)} warnings=${r.warnings}`);
  r.segments.forEach(s => console.log(`  ${C.fmtDate(s.s)}-${C.fmtDate(s.e)} gg ${s.days} tasso ${C.pct(s.rate)} = ${C.num(s.amount)}`));
  return r;
}
// tassi in vigore
const today = d('2026-10-06');
console.log('moraNow', C.moraNow(today));
console.log('legale oggi', C.rateAt(C.LEG, today));

// Guida 1: fattura 8.000 scaduta il 31.03.2026, conteggio al 06.10.2026
let r = mora(8000, '2026-04-01', '2026-10-06');
console.log('tot con 40:', C.num(8000 + r.total + 40));
// alternativa: fattura 5.000 scaduta 30.04.2026
r = mora(5000, '2026-05-01', '2026-10-06');
console.log('tot con 40:', C.num(5000 + r.total + 40));
// un anno di ritardo su 10.000
r = mora(10000, '2025-10-07', '2026-10-06');

// Guida 2: termini
function term(n) {
  const t = C.termini({ notifica: n, giorni: '10', bis: false });
  console.log(`\nTERMINI notifica ${n} (${C.weekday(d(n))}): 10° giorno ${C.fmtDate(t.adempiere)} (${C.weekday(t.adempiere)}) -> prorogato ${C.fmtDate(t.adempiereProrogato)} (${C.weekday(t.adempiereProrogato)}); esecuzione dal ${C.fmtDate(t.esecuzioneDal)} (${C.weekday(t.esecuzioneDal)}); efficacia ${C.fmtDate(t.efficacia)} (${C.weekday(t.efficacia)}) -> ${C.fmtDate(t.efficaciaProrogata)} (${C.weekday(t.efficaciaProrogata)})`);
}
['2026-10-01','2026-10-02','2026-10-05','2026-10-06','2026-10-07','2026-10-08','2026-10-09','2026-10-12','2026-10-13'].forEach(term);

// Guida 3: accessori sul compenso medio del monitorio (5.200-26.000): 567
function acc(comp, iva) {
  const rf = C.r2(comp * 0.15), b1 = C.r2(comp + rf), cpa = C.r2(b1 * 0.04), b2 = C.r2(b1 + cpa), i = iva ? C.r2(b2 * 0.22) : 0;
  return { comp, rf, cpa, senzaIva: b2, iva: i, tot: C.r2(b2 + i) };
}
[473, 567, 1370, 2242, 4394].forEach(c => console.log(c, JSON.stringify(acc(c, true))));
// precetto dell'esempio: capitale 8.000 mora dal 01.04.2026, DI con spese 145,50 e compensi 567, conteggio 06.10.2026
const st = { end: '2026-10-06', items: [{ desc: '', amount: '8000', type: 'mora', from: '2026-04-01', domanda: '', rate: '' }],
  titolo: 'di', spese: '145,50', compensi: '567', feeMode: 'medio', feeFree: '', rf: true, cpa: true, iva: false, extras: [], acconti: [], titleDate: '' };
const res = C.compute(st);
console.log('\nPRECETTO esempio:'); res.rows.forEach(x => console.log('  ' + x.label + ' = ' + C.num(x.amount)));
console.log('  TOTALE', C.num(res.total), 'valore', res.valore, 'fee', res.fee);
