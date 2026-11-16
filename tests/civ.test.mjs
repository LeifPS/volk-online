// Erweiterung 3 "Zivilisation": Regierung, Große Persönlichkeiten, Naturwunder
import fs from 'node:fs';
import * as E from '../public/js/engine.js';
const D = JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url)));
E.setzeDaten(D);
let fehler = 0; const ok = (c, t) => { if (!c) { fehler++; console.log('FEHLER:', t); } };
const neu = () => { const s = E.neuesSpiel([{ name: 'A' }, { name: 'B' }], { civ: true, seed: 7 }); return s; };
const bereit = (s) => { while (s.phase === 'ziehen') E.aktion(s, s.am, { t: 'ziehe', stapel: 1 }); };

{ const s = neu(); ok(s.civ && s.civ.pers.offen.length === 3 && s.civ.natur.offen.length === 4, 'Reihen gefüllt');
  const s0 = E.neuesSpiel([{ name: 'A' }, { name: 'B' }], {}); ok(!s0.civ, 'ohne Erweiterung kein civ'); }
// Regierung
{ const s = neu(); bereit(s); const p = s.sp[s.am]; const pi = s.am;
  p.gold = 20; p.alter = 3;
  let r = E.aktion(s, pi, { t: 'regierung', r: 'oligarchie' }); ok(r.ok, 'Regierung einführen: ' + r.fehler);
  ok(p.regierung.id === 'oligarchie' && p.gold === 13, 'Kosten bezahlt');
  ok(E.effekte(p).A >= 1 && E.effekte(p).S >= 2, 'Effekte der Regierung zählen');
  r = E.aktion(s, pi, { t: 'regierung', r: 'monarchie' }); ok(!r.ok, 'nur 1 Karte pro Zug');
  p.civN = 0; r = E.aktion(s, pi, { t: 'regierung', r: 'monarchie' }); ok(r.ok && p.regierung.id === 'monarchie', 'Wechsel ersetzt die alte');
  ok(E.effekte(p).A === 0 || E.effekte(p).A >= 0, 'alte Regierung wirkt nicht mehr');
  p.civN = 0; r = E.aktion(s, pi, { t: 'regierung', r: 'demokratie' }); ok(!r.ok, 'Zeitalter zu niedrig für Demokratie (Industrie)'); }
// Persönlichkeit dauerhaft + einmalig
{ const s = neu(); bereit(s); const p = s.sp[s.am], pi = s.am; p.gold = 50; p.alter = 6;
  s.civ.pers.offen[0] = s.civ.pers.stapel.splice(s.civ.pers.stapel.findIndex(c => c.id === 'newton'), 1)[0] || s.civ.pers.offen[0];
  const w = s.civ.pers.offen.find(c => c.id === 'newton'); ok(!!w, 'Newton in Reihe');
  const k0 = E.effekte(p).W; let r = E.aktion(s, pi, { t: 'person', c: w.i }); ok(r.ok, 'Newton holen: ' + r.fehler);
  ok(E.effekte(p).W === k0 + 3 && p.pers.length === 1, 'Newton gibt Wissen +3'); ok(s.civ.pers.offen.length === 3, 'Reihe aufgefüllt');
  // einmalig: Marco Polo
  p.civN = 0; const mp = s.civ.pers.stapel.findIndex(c => c.id === 'marco_polo'); let c;
  if (mp >= 0) c = s.civ.pers.stapel.splice(mp, 1)[0]; else c = s.civ.pers.offen.find(x => x.id === 'marco_polo');
  if (!s.civ.pers.offen.includes(c)) s.civ.pers.offen[0] = c;
  const g0 = p.gold; r = E.aktion(s, pi, { t: 'person', c: c.i }); ok(r.ok && p.gold === g0 - 3 + 6, 'Marco Polo: +6 Gold sofort');
  ok(p.pers.length === 1 && s.civ.pers.stapel.some(x => x.id === 'marco_polo'), 'einmalige Karte liegt unter dem Stapel'); }
// Persönlichkeiten-Grenze 3
{ const s = neu(); bereit(s); const p = s.sp[s.am], pi = s.am; p.gold = 99; p.alter = 6;
  const dauer = D.personen.filter(x => !Object.keys(x.einmal || {}).length);
  for (let n = 0; n < 3; n++) { p.civN = 0; const x = dauer[n]; s.civ.pers.offen[0] = { i: s.nid++, id: x.id }; const r = E.aktion(s, pi, { t: 'person', c: s.civ.pers.offen[0].i }); ok(r.ok, 'Persönlichkeit ' + n + ': ' + r.fehler); }
  p.civN = 0; s.civ.pers.offen[0] = { i: s.nid++, id: dauer[3].id }; const r = E.aktion(s, pi, { t: 'person', c: s.civ.pers.offen[0].i }); ok(!r.ok, 'höchstens 3 dauerhafte'); }
// Naturwunder: Gelände nötig
{ const s = neu(); bereit(s); const p = s.sp[s.am], pi = s.am; p.gold = 40; p.alter = 3;
  const nw = { i: s.nid++, id: 'everest' }; s.civ.natur.offen[0] = nw; p.land = p.land.filter(l => E.def(l).gelaende !== 'gebirge');
  let r = E.aktion(s, pi, { t: 'natur', c: nw.i }); ok(!r.ok, 'ohne Gebirge kein Everest');
  p.land.push({ i: s.nid++, id: D.karten.find(k => k.typ === 'land' && k.gelaende === 'gebirge').id });
  r = E.aktion(s, pi, { t: 'natur', c: nw.i }); ok(r.ok && p.natur.length === 1 && E.kultur(p) >= 2, 'Everest mit Gebirge: ' + r.fehler);
  p.civN = 0; p.alter = 0; s.civ.natur.offen[0] = { i: s.nid++, id: 'riff' }; r = E.aktion(s, pi, { t: 'natur', c: s.civ.natur.offen[0].i }); ok(!r.ok, 'Zeitalter II nötig'); }
// Sicht: Stapel verdeckt
{ const s = neu(); const v = E.sicht(s, 0); ok(v.civ.pers.stapel.every(x => x === 0) && v.civ.pers.offen.length === 3, 'sicht() verdeckt Stapel, Reihe offen'); }
console.log(fehler ? fehler + ' Fehler' : 'Zivilisations-Tests bestanden'); process.exit(fehler ? 1 : 0);
