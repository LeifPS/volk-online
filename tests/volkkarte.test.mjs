// Volkskarten zählen zum Handlimit und lassen sich gegen Gold ablegen (verlassen dann das Spiel).
import * as E from '../public/js/engine.js';
import fs from 'node:fs';
E.setzeDaten(JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))));
let fehler = 0; const ok = (b, m) => { if (!b) { console.error('FEHLER:', m); fehler++; } };
const s = E.neuesSpiel(['A', 'B'], { vk: true });
const pi = E.akteur(s), p = s.sp[pi];
E.aktion(s, pi, { t: 'ziehe', stapel: 1 }); E.aktion(s, pi, { t: 'ziehe', stapel: 1 });
const vk = p.hand.find(c => c.vk); ok(!!vk, 'Volkskarte auf der Hand');
ok(E.handZaehlt(p).length === p.hand.length, 'Volkskarten zählen zum Handlimit');
const gold = p.gold, n = p.hand.length;
const r = E.aktion(s, pi, { t: 'ablegen', c: vk.i });
ok(r.ok, 'Volkskarte ablegen: ' + JSON.stringify(r));
ok(p.gold === gold + E.ablegenGold(p, vk) && p.gold > gold, 'Gold fürs Ablegen');
ok(p.hand.length === n - 1 && !p.hand.some(c => c.i === vk.i), 'Karte weg');
ok(!Object.values(s.ablage).some(a => a.some(c => c.i === vk.i)), 'nicht im Ablagestapel');
// Zugende: zu viele Karten, Volkskarte darf mit abgeworfen werden
const vk2 = E.neuesSpiel(['A', 'B'], { vk: true }); const q = E.akteur(vk2), pp = vk2.sp[q];
E.aktion(vk2, q, { t: 'ziehe', stapel: 1 }); E.aktion(vk2, q, { t: 'ziehe', stapel: 1 });
while (pp.hand.length < E.handlimit(pp) + 1) pp.hand.push({ ...pp.hand.find(c => !c.vk), i: 9000 + pp.hand.length });
const v = pp.hand.find(c => c.vk);
ok(!E.aktion(vk2, q, { t: 'ende', abwerfen: [] }).ok, 'zu viele Karten: Ende ohne Abwerfen verboten');
ok(E.aktion(vk2, q, { t: 'ende', abwerfen: [v.i] }).ok, 'Volkskarte darf beim Zugende abgeworfen werden');
if (fehler) process.exit(1); console.log('Volkskarten-Tests bestanden');
