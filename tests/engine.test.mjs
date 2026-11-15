import fs from 'node:fs';
import * as E from '../public/js/engine.js';
E.setzeDaten(JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))));
const s = E.neuesSpiel([{ name: 'A' }, { name: 'B' }, { name: 'C' }], { seed: 5, vk: true, rel: true });
console.log('Start ok:', s.sp.map(p => p.volk + ':' + p.hand.length), 'Phase', s.phase, 'zieh', s.zieh);
console.log(E.aktion(s, 0, { t: 'ziehe', stapel: 1 }), E.aktion(s, 0, { t: 'ziehe', stapel: 1 }), s.phase);
console.log(E.aktion(s, 0, { t: 'ende' }));
