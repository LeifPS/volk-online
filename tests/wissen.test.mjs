// Wissenschaftssieg: In der Atomzeit kostet der "nächste Aufstieg" 20 Gold und gewinnt sofort.
import fs from 'node:fs';
import * as E from '../public/js/engine.js';
E.setzeDaten(JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))));
let fehler = 0; const ok = (c, t) => { if (!c) { fehler++; console.log('FEHLER:', t); } };
const start = () => { const s = E.neuesSpiel([{ name: 'A' }, { name: 'B' }], { seed: 3 }); while (s.phase === 'ziehen') E.aktion(s, s.am, { t: 'ziehe', stapel: 1 }); return s; };
{ const s = start(), pi = s.am, p = s.sp[pi]; p.alter = 6; p.gold = 19; p.aufN = 0;
  ok(E.wissenSiegMoeglich(p) && E.aufstiegKosten(p) === 20, 'Kosten 20 in der Atomzeit');
  let r = E.aktion(s, pi, { t: 'aufstieg' }); ok(!r.ok && s.sieger === null, 'mit 19 Gold kein Sieg');
  p.gold = 20; p.aufN = 1; r = E.aktion(s, pi, { t: 'aufstieg' }); ok(!r.ok && s.sieger === null, 'nicht in der Runde, in der man aufgestiegen ist');
  p.aufN = 0; r = E.aktion(s, pi, { t: 'aufstieg' }); ok(r.ok && s.sieger === pi && s.grund === 'Wissenschaft' && p.gold === 0, 'Sieg mit 20 Gold');
  ok(!E.aktion(s, pi, { t: 'ende' }).ok, 'danach ist das Spiel vorbei'); }
{ const s = start(), pi = s.am, p = s.sp[pi]; p.alter = 5; p.gold = 60; p.aufN = 0;
  const r = E.aktion(s, pi, { t: 'aufstieg' }); ok(r.ok && p.alter === 6 && s.sieger === null, 'Aufstieg in die Atomzeit gewinnt noch nicht');
  const r2 = E.aktion(s, pi, { t: 'aufstieg' }); ok(!r2.ok && s.sieger === null, 'am selben Tag kein zweiter Aufstieg'); }
{ const s = start(), pi = s.am, p = s.sp[pi]; p.alter = 3; p.gold = 99; p.aufN = 0; ok(E.aufstiegKosten(p) !== 20 && !E.wissenSiegMoeglich(p), 'vorher kein Wissenschaftssieg'); }
console.log(fehler ? fehler + ' Fehler' : 'Wissenschaftssieg-Tests bestanden');
