// Turnier: Stufe A gegen Stufe B. Beispiel: node tests/duell.mjs stark mittel 2 60
import fs from 'node:fs';
import * as E from '../public/js/engine.js';
import * as K from '../public/js/ki.js';
import * as S from '../public/js/ki_stark.js';
E.setzeDaten(JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))));
export function partie(stufen, seed, opt) {
  const s = E.neuesSpiel(stufen.map((_, i) => ({ name: 'S' + i })), { seed, ...opt }); let z = 0;
  while (s.sieger === null) { const pi = s.phase === 'block' ? s.kampf.ziel : s.am; const a = K.waehle(s, pi, stufen[pi]); const r = E.aktion(s, pi, a); if (!r.ok) { return { fehler: JSON.stringify(a) + r.fehler }; } if (++z > 5000 || s.runde > 50) return { s, remis: true }; }
  return { s };
}
export function turnier(A, B, n, spiele, param, opts) {
  if (param) S.setzeParam(param);
  let sieg = 0, ges = 0, fehler = 0, remis = 0, zeit = 0; const gr = {};
  for (let i = 0; i < spiele; i++) {
    const pos = i % n, stufen = Array.from({ length: n }, (_, j) => j === pos ? A : B); const opt = opts || { vk: i % 3 === 1 || i % 4 === 3, rel: i % 2 === 1 };
    const t0 = Date.now(); const r = partie(stufen, 1000 + i, opt); zeit += Date.now() - t0;
    if (r.fehler) { fehler++; console.log('FEHLER', r.fehler); continue; } if (r.remis) { remis++; continue; }
    ges++; if (r.s.sieger === pos) sieg++; gr[r.s.grund] = (gr[r.s.grund] || 0) + 1;
  }
  return { rate: sieg / Math.max(1, ges), sieg, ges, fehler, remis, ms: zeit / spiele, gr };
}
if (process.argv[1].endsWith('duell.mjs')) {
  const [A, B, n, N] = [process.argv[2] || 'stark', process.argv[3] || 'mittel', +process.argv[4] || 3, +process.argv[5] || 40];
  const r = turnier(A, B, n, N); console.log(`${A} vs ${B} (${n} Spieler, 1 gegen ${n - 1}):`, JSON.stringify(r), 'Erwartung bei Gleichstand', (100 / n).toFixed(0) + '%');
}
