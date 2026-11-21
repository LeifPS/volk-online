// Reichs-Ansicht: Die Stadt steht in der Mitte (Aussehen nach Zeitalter), jede Karte in der Auslage liegt als Hex-Tile
// rund um die Stadt. Die Tiles sind wie im Echtzeit-Volk gebaut (48x40 Pixel, Pixelrauschen, Gelände-Deko darüber).
import * as E from './engine.js';
import { spriteUrl, spriteGroesse } from './sprites.js';

const W = 48, H = 40, DY = 30;            // Tile-Größe und Zeilenabstand (Perspektive B wie im Echtzeit-Volk)
const GELAENDE = {                       // Farben aus dem Echtzeit-Volk: [Grund, hell, dunkel], Seitenfarbe
  grasland: ['#6aa84f', '#78b85a', '#5f9a47'], ebene: ['#a8b45a', '#b5c068', '#9ba64f'], wald: ['#4a8c44', '#3f7d3a', '#559a4e'],
  dschungel: ['#37a05a', '#2f8f4e', '#3fb066'], savanne: ['#c9b458', '#d4c066', '#bba84c'], huegel: ['#8fa456', '#9cb062', '#82964b'],
  gebirge: ['#9a9a9a', '#8c8c8c', '#a8a8a8'], wueste: ['#e0c27a', '#ebcf8c', '#d4b56a'], tundra: ['#8e9a7e', '#9aa68a', '#838f73'],
  kueste: ['#4c9ad8', '#58a6e0', '#4290cf'], kristallgebirge: ['#8f86b8', '#9d95c6', '#8178a9'], stadt: ['#7d9a55', '#89a661', '#728e4d'], leer: ['#161c2b', '#1a2132', '#131827'],
};
const RAND = { land: '#2f4a28', geb: '#3a2f20', wunder: '#e8b92f', staat: '#3a2f20', civ: '#8a6be0', stadt: '#4d3f2a', leer: '#2a3350' };

const rgb = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
const hash = (x, y, s) => { let h = (x * 374761393 + y * 668265263 + s * 2147483647) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
const innen = (x, y) => { const dx = Math.abs(x + 0.5 - W / 2), dy = Math.abs(y + 0.5 - H / 2); return dx <= W / 2 && dy <= H / 2 - dx * (H / 4) / (W / 2); };

const cache = new Map();
/** Pixel-Hexfeld als Bild-URL. pal: Farben, rand: Randfarbe, dick: 2 Pixel Rand (für besondere Karten), seed: Rauschen. */
function tileUrl(pal, rand, dick, seed) {
  const id = pal.join() + rand + dick + seed; if (cache.has(id)) return cache.get(id);
  const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
  const cx = cv.getContext('2d'), im = cx.createImageData(W, H), farben = pal.map(rgb), rc = rgb(rand);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    if (!innen(x, y)) continue;
    const rd1 = !innen(x - 1, y) || !innen(x + 1, y) || !innen(x, y - 1) || !innen(x, y + 1);
    const rd2 = dick && (!innen(x - 2, y) || !innen(x + 2, y) || !innen(x, y - 2) || !innen(x, y + 2) || !innen(x - 1, y - 1) || !innen(x + 1, y + 1) || !innen(x - 1, y + 1) || !innen(x + 1, y - 1));
    let c;
    if (rd1) c = rc;
    else if (rd2) c = rc.map(v => Math.min(255, v * 0.8));
    else {
      const n = hash(x, y, seed + 7); c = farben[n < 0.68 ? 0 : n < 0.86 ? 1 : 2];
      // oben links heller, unten rechts dunkler (wie im Echtzeit-Volk)
      const f = !innen(x - 2, y - 2) ? 1.08 : !innen(x + 2, y + 2) ? 0.88 : 1; c = c.map(v => Math.min(255, v * f));
    }
    const o = (y * W + x) * 4; im.data[o] = c[0]; im.data[o + 1] = c[1]; im.data[o + 2] = c[2]; im.data[o + 3] = 255;
  }
  cx.putImageData(im, 0, 0); const u = cv.toDataURL(); cache.set(id, u); return u;
}

/** Axiale Koordinaten des n-ten Platzes (0-basiert) auf den Ringen um die Stadt. */
export function platzKoord(n) {
  let k = 1; while (n >= 3 * k * (k + 1)) k++;
  let j = n - 3 * k * (k - 1), q = k, r = 0;
  const wege = [[-1, 1], [-1, 0], [0, -1], [1, -1], [1, 0], [0, 1]];
  for (const [dq, dr] of wege) { const m = Math.min(j, k); q += dq * m; r += dr * m; j -= m; if (j <= 0) break; }
  return [q, r];
}
const ringVon = (n) => { let k = 1; while (n >= 3 * k * (k + 1)) k++; return k; };

const img = (key, farbe, x, y, kl = '') => { const u = spriteUrl(key, farbe); if (!u) return ''; const [w, h] = spriteGroesse(key); return `<img class="px sp ${kl}" src="${u}" width="${w}" height="${h}" style="left:${x}px;top:${y}px" alt="" draggable="false">`; };

/** Beschreibung eines Tiles: Boden, Rand, Sprites. */
function tileAus(c, d, p) {
  const farbe = p.volkF;
  if (d.typ === 'land') {
    const g = GELAENDE[d.gelaende] ? d.gelaende : 'grasland', wasser = g === 'kueste';
    const deko = !wasser && d.deko ? img(d.deko, farbe, 0, 0) : '';
    const roh = d.sprite ? `<span class="rohs">${img(d.sprite, farbe, 0, 0)}</span>` : '';
    return { pal: GELAENDE[g], rand: RAND.land, dick: 0, html: deko + roh, kind: 'land' };
  }
  if (d.typ === 'natur') return { pal: GELAENDE[GELAENDE[d.gelaende] ? d.gelaende : 'grasland'], rand: RAND.civ, dick: 1, html: img(d.sprite, farbe, 0, 0), kind: 'natur' };
  if (d.typ === 'wunder') return { pal: GELAENDE.stadt, rand: RAND.wunder, dick: 1, html: img(d.sprite, farbe, -8, -30), kind: 'wunder' };
  if (d.typ === 'stadtstaat') return { pal: GELAENDE.stadt, rand: dunkler(d.farbe || '#3a2f20'), dick: 1, html: img(d.sprite, d.farbe || farbe, -8, -25), kind: 'staat' };
  if (d.typ === 'regierung') return { pal: GELAENDE.stadt, rand: RAND.civ, dick: 1, html: img(d.sprite, farbe, 8, 4), kind: 'civ' };
  if (d.typ === 'person') return { pal: GELAENDE.stadt, rand: RAND.civ, dick: 1, html: img(d.sprite, farbe, 10, -1), kind: 'civ' };
  return { pal: GELAENDE.stadt, rand: RAND.geb, dick: 0, html: img(d.sprite, d.farbe_rel || d.farbe_volk || farbe, 8, 3), kind: 'geb' };
}
const dunkler = (h) => '#' + rgb(h).map(v => Math.round(v * 0.55).toString(16).padStart(2, '0')).join('');

/**
 * Reichs-Hexkarte für Spieler p (Index pi). breite = verfügbare Breite in Pixeln.
 * Tippen auf ein Tile: data-a="info" (öffnet die Karte wie bisher).
 */
export function hexReich(p, pi, breite, neu = new Set()) {
  E.reichOrdnen(p);
  const karten = E.reichKarten(p), nach = new Map(karten.map(c => [c.pl, c]));
  const maxPl = karten.length ? Math.max(...karten.map(c => c.pl)) : -1, ring = Math.max(1, ringVon(Math.max(0, maxPl)));
  const felder = [{ q: 0, r: 0, mitte: true }];
  for (let n = 0; n < 3 * ring * (ring + 1); n++) { const [q, r] = platzKoord(n); felder.push({ q, r, n, c: nach.get(n) }); }
  for (const f of felder) { f.x = W * (f.q + f.r / 2); f.y = DY * f.r; }
  const minX = Math.min(...felder.map(f => f.x)) - 8, maxX = Math.max(...felder.map(f => f.x)) + W + 8;
  const minY = Math.min(...felder.map(f => f.y)) - 30, maxY = Math.max(...felder.map(f => f.y)) + H + 2;
  const bw = Math.ceil(maxX - minX), bh = Math.ceil(maxY - minY);
  const vh = breite / bw, sk = Math.max(0.5, vh >= 2 ? Math.floor(vh) : vh >= 1 ? Math.floor(vh * 2) / 2 : vh);
  const teile = felder.sort((a, b) => a.y - b.y || a.x - b.x).map(f => {
    const l = Math.round(f.x - minX), t = Math.round(f.y - minY), seed = ((f.q * 7 + f.r * 13) & 3) + 1;
    if (f.mitte) {
      const g = Math.min(3, 1 + (karten.length >= 3 ? 1 : 0) + (karten.length >= 9 ? 1 : 0));
      return `<div class="hx mitte" style="left:${l}px;top:${t}px;z-index:${f.y + 100}"><img class="px base" src="${tileUrl(GELAENDE.stadt, RAND.stadt, 1, 9)}" width="${W}" height="${H}" alt="">${img(`stadt:stadt@${p.alter}@${g}`, p.volkF, -8, -25)}</div>`;
    }
    if (!f.c) return `<div class="hx leer" style="left:${l}px;top:${t}px;z-index:${f.y}"><img class="px base" src="${tileUrl(GELAENDE.leer, RAND.leer, 0, seed)}" width="${W}" height="${H}" alt=""></div>`;
    const d = E.def(f.c), a = tileAus(f.c, d, p);
    return `<div class="hx ${a.kind}${neu.has(f.c.i) ? ' neu' : ''}" data-a="info" data-v="${f.c.id}" data-p="${pi}" style="left:${l}px;top:${t}px;z-index:${f.y + 100}" title="${d.name}"><img class="px base" src="${tileUrl(a.pal, a.rand, a.dick, seed)}" width="${W}" height="${H}" alt="">${a.html}</div>`;
  }).join('');
  return `<div class="hkw" style="width:${Math.round(bw * sk)}px;height:${Math.round(bh * sk)}px"><div class="hk" style="width:${bw}px;height:${bh}px;transform:scale(${sk})">${teile}</div></div>`;
}
