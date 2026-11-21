// Die Erweiterungen "Zivilisation" und "Götter & Glaube" sind vorerst abgeschaltet: Optionen werden ignoriert.
import fs from 'node:fs';
import * as E from '../public/js/engine.js';
E.setzeDaten(JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))));
let fehler = 0; const ok = (c, t) => { if (!c) { fehler++; console.log('FEHLER:', t); } };
const s = E.neuesSpiel([{ name: 'A' }, { name: 'B' }], { civ: true, rel: true, vk: false, seed: 7 });
ok(!s.civ && !s.opt.civ, 'Zivilisation bleibt aus, auch wenn sie verlangt wird');
ok(!s.opt.rel && s.relFrei.length === 0, 'Götter & Glaube bleibt aus');
ok(s.opt.vk && s.sp.every(p => p.hand.some(c => c.vk)), 'Volkskarten sind immer dabei');
while (s.phase === 'ziehen') E.aktion(s, s.am, { t: 'ziehe', stapel: 1 });
const p = s.sp[s.am];
ok(!E.aktion(s, s.am, { t: 'gruenden', rel: 'x', c: p.hand[0].i }).ok, 'Religion gründen nicht möglich');
ok(!E.aktion(s, s.am, { t: 'regierung', r: 'oligarchie' }).ok, 'Regierung nicht möglich');
console.log(fehler ? fehler + ' Fehler' : 'Erweiterungen-aus-Tests bestanden');
