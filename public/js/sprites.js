// Pixel-Sprites: kompakte Palette-Strings → Canvas → Data-URL (gecacht). Tokens S, S-, S+, S-- = Spielerfarbe.
let SP = {};
const cache = new Map();
export async function ladeSprites() { SP = await (await fetch('data/sprites.json')).json(); }
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
