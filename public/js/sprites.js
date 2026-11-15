// Pixel-Sprites: kompakte Palette-Strings → Canvas → Data-URL (gecacht). Tokens S, S-, S+, S-- = Spielerfarbe.
let SP = {};
const cache = new Map();
export async function ladeSprites() { SP = await (await fetch('data/sprites.json')).json(); eigene(); }
// Selbst gepixelte Zusatzsymbole (12x12). Zeichen: # Kontur, w hell, g grau, b blau, G grün, r rot, y gelb, o orange, k dunkel
const FARBEN = { '#': '#1a1a24', w: '#e8ecf4', g: '#9aa3b8', b: '#5aa0e6', G: '#5fbf4a', r: '#e0533d', y: '#f1c40f', o: '#f0952f', k: '#4a5068', p: '#a77de0' };
const EIGENE = {
  'x:kopie': ['................', '.#########......', '.#ggggggg#......', '.#ggggggg#......', '.#ggggggg#......', '.#ggg#########..', '.#ggg#wwwwwww#..', '.#ggg#wwwwwww#..', '.#ggg#wkkkkkw#..', '.#ggg#wwwwwww#..', '.#####wkkkkkw#..', '.....#wwwwwww#..', '.....#wkkkkkw#..', '.....#wwwwwww#..', '.....#########..', '................'],
  'x:roboter': ['.....##.....', '.....##.....', '..########..', '.#wwwwwwww#.', '.#w#ww#www#.', '.#wwwwwwww#.', '.#w######w#.', '..########..', '.#bb#bb#bb#.', '.#bb#bb#bb#.', '..##....##..', '............'],
  'x:erde': ['....####....', '..##bbbb##..', '.#bGGbbbb#.', '.#bGGGbbbb#.', '#bbGGGGbbb##'.slice(0, 12), '#bbbGGGbGb#.'.padEnd(12, '#'), '#bbbbGGGGb#.'.padEnd(12, '#'), '.#bbbbGGb#..', '.#bbbbbbb#..', '..##bbbb##..', '....####....', '............'],
  'x:link': ['............', '..###.......', '.#www#......', '#w###w#.....', '#w#.#w#.##..', '#w###w####w#'.slice(0, 12), '.#www#w#.#w#', '..###.#w#w#.', '.....#w###..', '......###...', '............', '............'],
  'x:teilen': ['................', '.......##.......', '......#ww#......', '.....#wwww#.....', '....#wwwwww#....', '...###wwww###...', '......#ww#......', '......#ww#......', '......#ww#......', '.#....#ww#....#.', '.#............#.', '.#............#.', '.##############.', '................', '................', '................'],
  'x:los': ['............', '..##........', '..#G##......', '..#GGG##....', '..#GGGGG##..', '..#GGGGGGG#.', '..#GGGGG##..', '..#GGG##....', '..#G##......', '..##........', '............', '............'],
  'x:totenkopf': ['...######...', '..#wwwwww#..', '.#wwwwwwww#.', '.#w##ww##w#.', '.#w##ww##w#.', '.#wwwwwwww#.', '..#wwrrww#..', '...#wwww#...', '...#w#w#w#..', '...######...', '............', '............'],
  'x:waage': ['................', '.......yy.......', '.......##.......', '.#############..', '.#.....##.....#.', '.#.....##.....#.', '.#.....##.....#.', '#y#....##....#y#', 'yyy....##....yyy', '###....##....###', '.......##.......', '.......##.......', '....########....', '................', '................', '................'],
  'x:blitz': ['................', '.........####...', '........#yyy#...', '.......#yyy#....', '......#yyy#.....', '.....#yyy#......', '....#yyyyyyy#...', '.....####yyy#...', '........#yyy#...', '.......#yyy#....', '......#yyy#.....', '......#yy#......', '.....#yy#.......', '.....#y#........', '.....##.........', '................'],
  'x:punkt': ['............', '............', '....####....', '...#GGGG#...', '..#GGGGGG#..', '..#GGGGGG#..', '..#GGGGGG#..', '...#GGGG#...', '....####....', '............', '............', '............'],
  'x:getrennt': ['............', '............', '....####....', '...#gggg#...', '..#gggggg#..', '..#gggggg#..', '..#gggggg#..', '...#gggg#...', '....####....', '............', '............', '............'],
  'x:karten': ['................', '.....#########..', '.....#ggggggg#..', '.....#ggggggg#..', '..#########gg#..', '..#wwwwwww#gg#..', '..#wwwwwww#gg#..', '..#wrrwrrw#gg#..', '..#wwwrwww#gg#..', '..#wwrrrww#gg#..', '..#wrwrwrw#gg#..', '..#wwrrrww####..', '..#wwwrwww#.....', '..#wwwwwww#.....', '..#########.....', '................'],
  'x:hand': ['....#.#.#...', '...#w#w#w##.', '...#w#w#w#w#', '.#.#wwwwwwww', '#w##wwwwwww#', '#ww#wwwwwww#', '.#wwwwwwww#.', '..#wwwwwww#.', '...#wwwww#..', '....######..', '............', '............'],
};
function eigene() {
  for (const [k, rows] of Object.entries(EIGENE)) {
    const w = 16, h = 16, pal = Object.values(FARBEN), idx = Object.keys(FARBEN), off = rows.length >= 16 ? 0 : 2; let d = '';
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const ch = (rows[y - off] || '')[x - off] || '.'; d += ch === '.' ? '.' : String.fromCharCode(48 + idx.indexOf(ch)); }
    SP[k] = { w, h, p: pal, d };
  }
}
// Symbol als Pixel-Bild (kleinste Einheit: 1 Sprite-Pixel = scale Bildschirm-Pixel)
export function ic(key, scale = 1) { return spr(key.includes(':') ? key : 'ui:' + key, '#ffffff', scale, 'ic'); }
export const hatSprite = (k) => k in SP;
const rgb = (h) => { h = h.replace('#', ''); if (h.length === 3) h = [...h].map(c => c + c).join(''); return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16)); };
const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
function toene(f) { const c = rgb(f); return { 'S': c, 'S-': mix(c, [0, 0, 0], .35), 'S+': mix(c, [255, 255, 255], .35), 'S--': mix(c, [0, 0, 0], .6) }; }
export function spriteUrl(key, farbe = '#2f6fd0') {
  const id = key + '|' + farbe; if (cache.has(id)) return cache.get(id);
  const s = SP[key]; if (!s) { cache.set(id, ''); return ''; }
  const t = toene(farbe), cv = document.createElement('canvas'); cv.width = s.w; cv.height = s.h;
  const cx = cv.getContext('2d'), im = cx.createImageData(s.w, s.h), pal = s.p.map(c => t[c] || rgb(c));
  for (let i = 0; i < s.d.length; i++) { const ch = s.d.charCodeAt(i); if (ch === 46) continue; const c = pal[ch - 48]; im.data[i * 4] = c[0]; im.data[i * 4 + 1] = c[1]; im.data[i * 4 + 2] = c[2]; im.data[i * 4 + 3] = 255; }
  cx.putImageData(im, 0, 0); const u = cv.toDataURL(); cache.set(id, u); return u;
}
export const spriteGroesse = (k) => SP[k] ? [SP[k].w, SP[k].h] : [16, 16];
// <img>-HTML; scale = Pixelvergrößerung
export function spr(key, farbe, scale = 2, extra = '') {
  const u = spriteUrl(key, farbe); if (!u) return '';
  const [w, h] = spriteGroesse(key);
  return `<img class="px ${extra}" src="${u}" width="${w * scale}" height="${h * scale}" alt="" draggable="false">`;
}
