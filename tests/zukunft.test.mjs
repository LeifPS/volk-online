// Daten- und Regeltests für 11 Zeitalter, Stapel IV und Volkskarten im Grundspiel.
import fs from 'node:fs';
import * as E from '../public/js/engine.js';
const D = JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url)));
const SP = JSON.parse(fs.readFileSync(new URL('../public/data/sprites.json', import.meta.url)));
E.setzeDaten(D);
let fehler = 0; const ok = (c, t) => { if (!c) { fehler++; console.log('FEHLER:', t); } };
const R = D.regeln;
ok(D.zeitalter.length === 11, '11 Zeitalter');
ok(R.aufstieg.length === 10 && R.stapel_von_zeitalter.length === 11, 'Aufstiegskosten und Stapel für 11 Zeitalter');
ok(R.kultur_sieg === 28, 'Kultursieg 28');
ok(R.aufstieg.every((x, i) => i === 0 || x > R.aufstieg[i - 1]), 'Aufstiegskosten steigen');
// jedes Zeitalter hat Karten
for (let z = 0; z < 11; z++) { const n = D.karten.filter(k => k.zeitalter === z && k.typ !== 'land').length; ok(n >= 5, `Zeitalter ${z + 1} hat genug Karten (${n})`); }
// Stapel passt zum Zeitalter
for (const k of D.karten) ok(k.stapel === R.stapel_von_zeitalter[k.zeitalter], `Stapel von ${k.id}`);
for (const z of [7, 8, 9, 10]) ok(D.wunder.filter(w => w.zeitalter === z).length === 1, `genau ein Wunder in Zeitalter ${z + 1}`);
// Karten: gültige Felder, Sprites vorhanden, eindeutige IDs (Land ausgenommen wegen Kopien in mehreren Stapeln)
const sprites = new Set(Object.keys(SP));
const ids = new Set();
for (const k of [...D.karten, ...D.wunder, ...D.volkskarten]) {
  if (k.typ !== 'land') { ok(!ids.has(k.id), 'doppelte ID ' + k.id); ids.add(k.id); }
  ok(sprites.has(k.sprite), `Sprite ${k.sprite} fehlt`);
  ok(k.kosten >= 0 && Number.isFinite(k.kosten), 'Kosten ' + k.id);
  if (k.typ === 'einheit') ok(k.staerke >= 0 && k.fern >= 0 && Array.isArray(k.braucht) && k.braucht.length <= 3, 'Einheitenwerte ' + k.id);
}
// Symbole: jede gebrauchte Rohstoff-Marke wird von irgendeiner Land-Karte oder einem Gebäude geliefert
const liefert = new Set([...D.karten.filter(k => k.typ === 'land').flatMap(k => k.symbole), ...D.karten.flatMap(k => k.prov || []), ...D.volkskarten.flatMap(k => k.prov || []), ...D.staaten.flatMap(k => k.prov || [])]);
for (const k of [...D.karten, ...D.wunder, ...D.volkskarten]) for (const b of k.braucht || []) ok(liefert.has(b), `Symbol ${b} (${k.id}) ist nirgends erhältlich`);
for (const r of ['seltene_erden', 'deuterium', 'titan', 'helium3']) ok(D.karten.some(k => k.typ === 'land' && k.symbole.includes(r)), 'Land mit ' + r);
for (const k of D.karten.filter(k => k.typ === 'gebaeude')) for (const b of k.benoetigt || []) ok(D.karten.some(x => x.id === b), `${k.id} benötigt unbekanntes ${b}`);
for (const w of D.wunder) for (const b of w.benoetigt || []) ok(D.karten.some(x => x.id === b), `${w.id} benötigt unbekanntes ${b}`);
// Volkskarten: je Volk genau 11, je Zeitalter genau eine
for (const v of D.voelker) { const l = D.volkskarten.filter(k => k.volk === v.id); ok(l.length === 11 && l.every((k, i) => l.some(x => x.zeitalter === i)), `11 Volkskarten ${v.id}`); }
// Zeitalter VII gibt wieder Wissen
const g = (id) => D.karten.find(k => k.id === id);
ok(g('rechenzentrum').effekte.W === 4 && !g('rechenzentrum').effekte.E, 'Rechenzentrum W4');
ok(g('raumfahrtzentrum').effekte.W === 3 && g('raumfahrtzentrum').effekte.K === 3, 'Raumfahrtzentrum K3 W3');
ok(D.wunder.find(w => w.id === 'internationale_raumstation').effekte.W === 3, 'ISS W3');
ok(D.volkskarten.find(k => k.id === 'sd_raketen').effekte.W === 3, 'Himmelsbahnhof W3');
// Spielstart
const s = E.neuesSpiel([{ name: 'A' }, { name: 'B' }], { seed: 5 });
ok(s.stapel[4].length === D.karten.filter(k => k.stapel === 4).reduce((a, k) => a + k.kopien, 0), 'Stapel IV gefüllt');
ok(s.sp.every(p => p.hand.filter(c => c.vk).length === 1), 'Volkskarte I auf der Hand');
const p = s.sp[0];
ok(E.maxStapel(p) === 1, 'am Anfang nur Stapel I');
// Aufstieg durch alle Zeitalter: Volkskarte des neuen Zeitalters kommt dazu, Stapel IV ab VIII
p.gold = 999; E.aktion(s, 0, { t: 'ziehe', stapel: 1 }); E.aktion(s, 0, { t: 'ziehe', stapel: 1 });
for (let z = 1; z <= 10; z++) {
  p.aufN = 0; const vorher = p.hand.filter(c => c.vk).length;
  const r = E.aktion(s, 0, { t: 'aufstieg' }); ok(r.ok, `Aufstieg ${z}: ${r.fehler}`);
  ok(p.alter === z, 'Zeitalter ' + z); ok(p.hand.filter(c => c.vk).length === vorher + 1, 'Volkskarte ' + z);
  ok(E.maxStapel(p) === R.stapel_von_zeitalter[z], 'Stapelzugang ' + z);
}
ok(E.wissenSiegMoeglich(p) && E.aufstiegKosten(p) === R.wissen_sieg, 'im letzten Zeitalter: Wissenschaftssieg');
// Karten VIII–XI sind erst nach dem Aufstieg spielbar
{ const t = E.neuesSpiel([{ name: 'A' }, { name: 'B' }], { seed: 9 }); const q = t.sp[0]; const k = E.neuesSpiel && D.karten.find(x => x.id === 'sternenkreuzer');
  const kz = { i: 9999, id: 'sternenkreuzer' }; q.hand.push(kz); q.gold = 99; ok(!!E.sperrGrund(t, q, kz), 'Sternenkreuzer in Antike gesperrt'); q.alter = 10; ok(!E.sperrGrund(t, q, kz) || /Rohstoff|Flug|Symbol|fehl/i.test(E.sperrGrund(t, q, kz)), 'Sternenkreuzer in XI nicht wegen Zeitalter gesperrt: ' + E.sperrGrund(t, q, kz)); }
console.log(fehler ? fehler + ' Fehler' : 'Zukunft-Tests bestanden');
process.exit(fehler ? 1 : 0);
