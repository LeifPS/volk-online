import fs from 'node:fs';
import * as E from '../public/js/engine.js';
import * as K from '../public/js/ki.js';
E.setzeDaten(JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))));
export function spiele(n, seed, opt, stufen) {
  const s = E.neuesSpiel(Array.from({ length: n }, (_, i) => ({ name: 'S' + (i + 1) })), { seed, ...opt });
  let zug = 0;
  while (s.sieger === null) {
    const pi = E.akteur(s);
    const a = K.waehle(s, pi, stufen[pi] || 'mittel'); const r = E.aktion(s, pi, a);
    if (!r.ok) { console.log('FEHLER', s.phase, JSON.stringify(a), r.fehler); return null; }
    if (++zug > 6000 || s.runde > 60) { s.grund = 'zu lang'; break; }
  }
  return s;
}
if (process.argv[1].endsWith('selfplay.mjs')) {
  const N = +process.argv[2] || 100;
  for (const n of [2, 3, 4]) for (const [vk, rel] of [[0, 0], [1, 0], [0, 1], [1, 1]]) {
    const gr = {}, w = {}, a = {}; const rn = []; let fe = 0;
    for (let i = 0; i < N; i++) { const s = spiele(n, 100 + i, { vk: !!vk, rel: !!rel }, []); if (!s) { fe++; continue; } gr[s.grund] = (gr[s.grund] || 0) + 1; rn.push(s.runde); for (const p of s.sp) a[p.volk] = (a[p.volk] || 0) + 1; if (s.sieger !== null) { const v = s.sp[s.sieger].volk; w[v] = (w[v] || 0) + 1; } }
    rn.sort((x, y) => x - y);
    console.log(`n=${n} VK=${vk} REL=${rel} Fehler=${fe}`, JSON.stringify(gr), 'Median', rn[rn.length >> 1], 'Quote', Object.keys(a).sort().map(v => v.slice(0, 4) + ':' + Math.round(100 * (w[v] || 0) / a[v])).join(' '));
  }
}
