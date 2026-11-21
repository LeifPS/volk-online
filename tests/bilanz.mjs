// Balance-Werkzeug: viele Selbstspiele, dann Siegarten, Länge, erreichte Zeitalter, Nutzung der Stapel-IV-Karten.
// Aufruf: node tests/bilanz.mjs [Spiele je Größe] [Stufe leicht|mittel|stark] [Spielergrößen z. B. 2,3,4]
import fs from 'node:fs';
import * as E from '../public/js/engine.js';
import * as K from '../public/js/ki.js';
const D = JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))); // Zum Ausprobieren: Regelwerte per Umgebungsvariable überschreiben, z. B. KULTUR=22 WISSEN=24 AUFSTIEG=6,8,10,...
if (process.env.KULTUR) D.regeln.kultur_sieg = +process.env.KULTUR;
if (process.env.WISSEN) D.regeln.wissen_sieg = +process.env.WISSEN;
if (process.env.AUFSTIEG) D.regeln.aufstieg = process.env.AUFSTIEG.split(',').map(Number);
E.setzeDaten(D);
const N = +process.argv[2] || 100, STUFE = process.argv[3] || 'mittel', GR = (process.argv[4] || '2,3,4').split(',').map(Number);
const med = (a) => { a = [...a].sort((x, y) => x - y); return a[a.length >> 1]; };
for (const n of GR) {
  const grund = {}, runden = [], maxAlter = [], endAlter = Array(11).fill(0), gewVolk = {}, spVolk = {}, gewRoute = {}, nutz = {}; let fehler = 0, zuLang = 0;
  for (let i = 0; i < N; i++) {
    const s = E.neuesSpiel(Array.from({ length: n }, (_, j) => ({ name: 'S' + (j + 1) })), { seed: 1000 + i });
    let zug = 0, bad = false;
    while (s.sieger === null) {
      const pi = E.akteur(s); const a = K.waehle(s, pi, STUFE); const r = E.aktion(s, pi, a);
      if (!r.ok) { fehler++; bad = true; break; }
      if (++zug > 12000 || s.runde > 80) { s.grund = 'zu lang'; zuLang++; break; }
    }
    if (bad) continue;
    grund[s.grund] = (grund[s.grund] || 0) + 1; runden.push(s.runde);
    maxAlter.push(Math.max(...s.sp.map(p => p.alter))); for (const p of s.sp) endAlter[p.alter]++;
    for (const p of s.sp) { spVolk[p.volk] = (spVolk[p.volk] || 0) + 1; }
    if (s.sieger !== null && s.sieger !== undefined && s.sp[s.sieger]) { const w = s.sp[s.sieger]; gewVolk[w.volk] = (gewVolk[w.volk] || 0) + 1; }
    for (const p of s.sp) for (const c of [...p.geb, ...p.front, ...p.kaserne, ...p.wunder]) { const d = E.def(c); if (d.zeitalter >= 7) nutz[d.id] = (nutz[d.id] || 0) + 1; }
  }
  const pct = (x) => Math.round(100 * x / N);
  console.log(`\n== ${n} Spieler, ${N} Spiele, Stufe ${STUFE}: Fehler ${fehler}, zu lang ${zuLang}`);
  console.log('Siegarten', JSON.stringify(grund), '| Runden Median', med(runden), 'Mittel', (runden.reduce((a, b) => a + b, 0) / runden.length).toFixed(1), 'Max', Math.max(...runden));
  console.log('Höchstes Zeitalter im Spiel (Median)', med(maxAlter) + 1, '| Endzeitalter je Spieler (I..XI):', endAlter.join(' '));
  console.log('Gewinn je Volk (% der Spiele, in denen es mitspielte)', Object.keys(spVolk).map(v => v.slice(0, 4) + ':' + Math.round(100 * (gewVolk[v] || 0) / spVolk[v])).join(' '));
  const gesamt = D.karten.filter(k => k.zeitalter >= 7 && k.typ !== 'land').map(k => k.id).concat(D.wunder.filter(w => w.zeitalter >= 7).map(w => w.id));
  const tot = gesamt.filter(id => !nutz[id]); console.log('Neue Karten nie gespielt:', tot.length ? tot.join(', ') : 'keine', `(${gesamt.length - tot.length}/${gesamt.length} gespielt)`);
}
