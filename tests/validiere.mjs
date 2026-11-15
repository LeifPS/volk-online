import fs from 'node:fs';
import { turnier } from './duell.mjs';
const p = process.argv[2] ? JSON.parse(fs.readFileSync(process.argv[2])) : null;
const N = +process.argv[3] || 90;
for (const n of [2, 3, 4]) { const r = turnier('stark', 'mittel', n, N, p); console.log(`${n} Spieler: stark gewinnt ${(r.rate * 100).toFixed(0)} % (Zufall ${(100 / n).toFixed(0)} %) – ${r.sieg}/${r.ges}, Fehler ${r.fehler}, Remis ${r.remis}, ${Math.round(r.ms)} ms/Partie`, JSON.stringify(r.gr)); }
