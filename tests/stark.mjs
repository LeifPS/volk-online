// Wie gut ist "Stark" gegen "Mittel"? (Siegquote des starken Spielers, Zufallsniveau = 1/Spieleranzahl)
import fs from 'node:fs';
import * as E from '../public/js/engine.js';
import * as K from '../public/js/ki.js';
const D = JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url)));
if (process.env.KULTUR) D.regeln.kultur_sieg = +process.env.KULTUR;
if (process.env.WISSEN) D.regeln.wissen_sieg = +process.env.WISSEN;
E.setzeDaten(D);
const N = +process.argv[2] || 60;
for (const n of [2, 3, 4]) {
  let w = 0, ges = 0; const gr = {};
  for (let j = 0; j < N; j++) {
    const pos = j % n, st = Array.from({ length: n }, (_, k) => k === pos ? 'stark' : 'mittel');
    const s = E.neuesSpiel(st.map((_, i) => ({ name: 'S' + i })), { seed: 7000 + j }); let z = 0, ok = true;
    while (s.sieger === null) { const pi = E.akteur(s); const r = E.aktion(s, pi, K.waehle(s, pi, st[pi])); if (!r.ok || ++z > 8000 || s.runde > 60) { ok = false; break; } }
    if (!ok) continue; ges++; if (s.sieger === pos) w++; gr[s.grund] = (gr[s.grund] || 0) + 1;
  }
  console.log(`n=${n}: Stark gewinnt ${Math.round(100 * w / ges)} % (Zufall ${Math.round(100 / n)} %)`, JSON.stringify(gr));
}
