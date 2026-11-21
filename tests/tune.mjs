// Abstimmung der Gewichte der Stufe "Stark" per Kreuzentropie-Methode (CEM) im Selbstspiel gegen "Mittel".
// Aufruf: node tests/tune.mjs [Generationen] [Population] [Spiele je Kandidat]
import { Worker, isMainThread, parentPort, workerData } from 'node:worker_threads';
import fs from 'node:fs';
import os from 'node:os';
const DATEI = new URL('./params.json', import.meta.url);
if (!isMainThread) {
  const E = await import('../public/js/engine.js'); const K = await import('../public/js/ki.js'); const S = await import('../public/js/ki_stark.js');
  E.setzeDaten(JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))));
  parentPort.on('message', ({ id, param, seeds, spiele }) => {
    S.setzeParam(param); let score = 0, ges = 0;
    for (let j = 0; j < spiele; j++) {
      const n = [2, 3, 4][j % 3], pos = Math.floor(j / 3) % n, st = Array.from({ length: n }, (_, k) => k === pos ? 'stark' : 'mittel'), c = j % 4;
      const s = E.neuesSpiel(st.map((_, i) => ({ name: 'S' + i })), { seed: seeds + j }); let z = 0, ok = true;
      while (s.sieger === null) { const pi = E.akteur(s); const r = E.aktion(s, pi, K.waehle(s, pi, st[pi])); if (!r.ok || ++z > 5000 || s.runde > 50) { ok = false; break; } }
      if (!ok) continue; ges++; score += (s.sieger === pos ? 1 : 0) - 1 / n;
    }
    parentPort.postMessage({ id, score: score / Math.max(1, ges), ges });
  });
} else {
  const { PARAM } = await import('../public/js/ki_params.js');
  const GEN = +process.argv[2] || 15, POP = +process.argv[3] || 14, SP = +process.argv[4] || 90, ELITE = Math.max(3, Math.round(POP * 0.25));
  let start = PARAM; try { start = JSON.parse(fs.readFileSync(DATEI)); } catch { }
  const keys = Object.keys(PARAM); let mu = Object.fromEntries(keys.map(k => [k, start[k] ?? PARAM[k]])), sg = Object.fromEntries(keys.map(k => [k, (Math.abs(mu[k]) * 0.35 + 0.15) * (+process.env.SG || 1)]));
  const nw = Math.min(os.cpus().length, 4), pool = Array.from({ length: nw }, () => new Worker(new URL(import.meta.url))), warte = new Map(); let nid = 0;
  pool.forEach(w => w.on('message', m => { warte.get(m.id)(m); warte.delete(m.id); }));
  const rolle = pool.map(() => Promise.resolve());
  const eval1 = (param, seeds, k) => new Promise(res => { const id = ++nid; warte.set(id, res); pool[k % nw].postMessage({ id, param, seeds, spiele: SP }); });
  const gauss = () => { let u = 0, v = 0; while (!u) u = Math.random(); while (!v) v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
  for (let g = 0; g < GEN; g++) {
    const t0 = Date.now(), seeds = 50000 + g * 997;
    const pop = Array.from({ length: POP }, (_, i) => i === 0 ? { ...mu } : Object.fromEntries(keys.map(k => [k, Math.max(0, mu[k] + sg[k] * gauss())])));
    const res = await Promise.all(pop.map((p, i) => eval1(p, seeds, i)));
    const rang = res.map((r, i) => ({ i, s: r.score })).sort((a, b) => b.s - a.s), elite = rang.slice(0, ELITE).map(r => pop[r.i]);
    for (const k of keys) { const m = elite.reduce((a, e) => a + e[k], 0) / ELITE; const v = Math.sqrt(elite.reduce((a, e) => a + (e[k] - m) ** 2, 0) / ELITE); mu[k] = 0.6 * m + 0.4 * mu[k]; sg[k] = Math.max(0.05 + Math.abs(mu[k]) * 0.06, 0.6 * v + 0.4 * sg[k]); }
    fs.writeFileSync(DATEI, JSON.stringify(Object.fromEntries(Object.entries(mu).map(([k, v]) => [k, +v.toFixed(3)])), null, 1));
    console.log(`Gen ${g + 1}/${GEN}: Bestwert ${rang[0].s.toFixed(3)} (Mittelwert-Kandidat ${res[0].score.toFixed(3)}), Ø ${(res.reduce((a, r) => a + r.score, 0) / POP).toFixed(3)}, ${Math.round((Date.now() - t0) / 1000)} s`);
  }
  pool.forEach(w => w.terminate()); process.exit(0);
}
