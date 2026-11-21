// Wissenschaftssieg: Im Sternenzeitalter (XI, Index 10) kostet der "nächste Aufstieg" 24 Gold und gewinnt sofort.
import fs from 'node:fs';
import * as E from '../public/js/engine.js';
E.setzeDaten(JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))));
let fehler = 0; const ok = (c, t) => { if (!c) { fehler++; console.log('FEHLER:', t); } };
const start = () => { const s = E.neuesSpiel([{ name: 'A' }, { name: 'B' }], { seed: 3 }); while (s.phase === 'ziehen') E.aktion(s, s.am, { t: 'ziehe', stapel: 1 }); return s; };
{ const s = start(), pi = s.am, p = s.sp[pi]; p.alter = 10; p.gold = 23; p.aufN = 0;
  ok(E.wissenSiegMoeglich(p) && E.aufstiegKosten(p) === 24, 'Kosten 24 im Sternenzeitalter');
  let r = E.aktion(s, pi, { t: 'aufstieg' }); ok(!r.ok && s.sieger === null, 'mit 23 Gold kein Sieg');
  p.gold = 24; p.aufN = 1; r = E.aktion(s, pi, { t: 'aufstieg' }); ok(!r.ok && s.sieger === null, 'nicht in der Runde, in der man aufgestiegen ist');
  p.aufN = 0; r = E.aktion(s, pi, { t: 'aufstieg' }); ok(r.ok && s.sieger === pi && s.grund === 'Wissenschaft' && p.gold === 0, 'Sieg mit 24 Gold');
  ok(!E.aktion(s, pi, { t: 'ende' }).ok, 'danach ist das Spiel vorbei'); }
{ const s = start(), pi = s.am, p = s.sp[pi]; p.alter = 9; p.gold = 60; p.aufN = 0;
  const r = E.aktion(s, pi, { t: 'aufstieg' }); ok(r.ok && p.alter === 10 && s.sieger === null, 'Aufstieg ins Sternenzeitalter gewinnt noch nicht');
  const r2 = E.aktion(s, pi, { t: 'aufstieg' }); ok(!r2.ok && s.sieger === null, 'am selben Tag kein zweiter Aufstieg'); }
{ const s = start(), pi = s.am, p = s.sp[pi]; p.alter = 3; p.gold = 99; p.aufN = 0; ok(E.aufstiegKosten(p) !== 24 && !E.wissenSiegMoeglich(p), 'vorher kein Wissenschaftssieg'); }
{ const s = start(), pi = s.am, p = s.sp[pi]; p.alter = 6; p.gold = 99; p.aufN = 0; ok(!E.wissenSiegMoeglich(p) && E.aufstiegKosten(p) !== 24, 'in der Atomzeit (VII) noch kein Wissenschaftssieg');
  const r = E.aktion(s, pi, { t: 'aufstieg' }); ok(r.ok && p.alter === 7 && s.sieger === null, 'Atomzeit -> KI-Zeitalter'); }
console.log(fehler ? fehler + ' Fehler' : 'Wissenschaftssieg-Tests bestanden');
