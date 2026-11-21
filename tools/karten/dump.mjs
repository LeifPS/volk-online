import { alleSprites, pinselFuer } from '/home/claude/volk/public/js/grafik/sprites.js';
import '/home/claude/volk/public/js/grafik/alle.js';
import * as D from '/home/claude/volk/public/shared/daten/index.js';
import fs from 'node:fs';
const out = {};
const zaehl = {};
for (const s of alleSprites()) {
  zaehl[s.kategorie] = (zaehl[s.kategorie] || 0) + 1;
  const p = pinselFuer(s.kategorie, s.id, { zeitalter: 0 });
  out[s.kategorie + ':' + s.id] = { w: p.w, h: p.h, feld: p.feld };
}
console.log(zaehl);
fs.writeFileSync('/home/claude/volk-online/tools/karten/sprites.json', JSON.stringify(out));
const daten = {
  zeitalter: D.ZEITALTER, einheiten: D.EINHEITEN, gebaeude: D.GEBAEUDE, wunder: D.WUNDER, rohstoffe: D.ROHSTOFFE,
  gelaende: D.GELAENDE, verbesserungen: D.VERBESSERUNGEN, ki: D.KI_VOELKER, staaten: D.STADTSTAATEN, forschungen: D.FORSCHUNGEN.length,
};
fs.writeFileSync('/home/claude/volk-online/tools/karten/daten.json', JSON.stringify(daten));
console.log(Object.fromEntries(Object.entries(daten).map(([k,v])=>[k,Array.isArray(v)?v.length:v])));
// Zusatz: Stadt je Zeitalter/Größe, Mauern
const extra = {};
for (let z = 0; z <= 6; z++) for (const g of [1, 2, 3]) { const p = pinselFuer('stadt', 'stadt', { zeitalter: z, groesse: g }); extra[`stadt:stadt@${z}@${g}`] = { w: p.w, h: p.h, feld: p.feld }; }
for (let z = 0; z <= 3; z++) { const p = pinselFuer('stadt', 'mauer', { zeitalter: z }); extra[`stadt:mauer@${z}`] = { w: p.w, h: p.h, feld: p.feld }; }
const all = JSON.parse(fs.readFileSync('/home/claude/volk-online/tools/karten/sprites.json', 'utf8'));
Object.assign(all, extra);
fs.writeFileSync('/home/claude/volk-online/tools/karten/sprites.json', JSON.stringify(all));
console.log('stadt-varianten', Object.keys(extra).length);
