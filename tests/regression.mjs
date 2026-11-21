// Regressionstest: feste Seeds müssen immer dieselben Partien ergeben (Sieger, Siegart, Runde). Erkennt unbeabsichtigte Regeländerungen.
// Neue Referenz schreiben nach bewussten Regeländerungen: node tests/regression.mjs --neu
import fs from 'node:fs';
// Die KI hält Math.random beim Laden fest: erst einen umlenkbaren Zufallsstrom einsetzen, dann die Module laden.
let _a = 1; Math.random = () => { let t = (_a += 0x6D2B79F5) >>> 0; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
const E = await import('../public/js/engine.js'); const K = await import('../public/js/ki.js');
E.setzeDaten(JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))));
const DATEI = new URL('./regression.json', import.meta.url);
const fest = (seed) => { _a = seed >>> 0; };
const ergebnis = [];
for (const n of [2, 3, 4]) for (let seed = 1; seed <= 8; seed++) {
  fest(seed * 31 + n);
  const s = E.neuesSpiel(Array.from({ length: n }, (_, i) => ({ name: 'S' + i })), { seed }); let z = 0;
  while (s.sieger === null && z++ < 9000) { const pi = E.akteur(s); const r = E.aktion(s, pi, K.waehle(s, pi, 'mittel')); if (!r.ok) throw new Error('Fehler in Partie ' + n + '/' + seed + ': ' + r.fehler); }
  ergebnis.push([n, seed, s.sieger, s.grund, s.runde]);
}
if (process.argv.includes('--neu')) { fs.writeFileSync(DATEI, JSON.stringify(ergebnis)); console.log('Referenz geschrieben:', ergebnis.length, 'Partien'); }
else {
  const ref = JSON.parse(fs.readFileSync(DATEI)); const diff = ergebnis.filter((e, i) => JSON.stringify(e) !== JSON.stringify(ref[i]));
  if (diff.length) { console.log('FEHLER: Abweichungen in', diff.length, 'Partien, z. B.', JSON.stringify(diff[0]), 'statt', JSON.stringify(ref[ergebnis.indexOf(diff[0])])); process.exit(1); }
  console.log('Regressionstest bestanden (' + ergebnis.length + ' feste Partien)');
}
