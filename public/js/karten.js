// Echte Kartenbilder (1:1 wie die gedruckten Karten). Dateien: karten/<id>.webp, Rückseiten rueck_*.webp, Volkstafeln tafel_<volk>.webp
let NAMEN = new Set();
export async function ladeKartenIndex() { try { NAMEN = new Set(await (await fetch('karten/index.json')).json()); } catch { } }
export const hatBild = (n) => NAMEN.has(n);
export function bildName(c) {
  const id = c.id; if (c.st > 1 && NAMEN.has(`${id}_s${c.st}`)) return `${id}_s${c.st}`;
  return id;
}
export const bildUrl = (name) => `karten/${name}.webp`;
const esc = (t) => String(t ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
// Eine Karte als Bild. o: a/v (Klick), cls, gedreht (erschöpft), rueck (Rückseitenname statt Vorderseite), badge (HTML), data (Zusatz-Attribute), titel
export function kk(c, o = {}) {
  const name = o.rueck || bildName(c);
  const data = Object.entries(o.data || {}).map(([k, v]) => ` data-${k}="${esc(v)}"`).join('');
  return `<div class="kk ${o.gedreht ? 'gedreht' : ''} ${o.cls || ''}" ${o.a ? `data-a="${o.a}" data-v="${esc(o.v ?? c.i)}"` : ''}${data}><img src="${bildUrl(name)}" alt="${esc(o.titel || c.id || '')}" draggable="false" ${o.eager ? '' : 'loading="lazy"'} decoding="async">${o.badge ? `<span class="badge">${o.badge}</span>` : ''}${o.unten ? `<span class="unten">${o.unten}</span>` : ''}</div>`;
}
// Stapel aus Rückseiten (Anzahl als Zähler)
export function stapelBild(rueck, n, o = {}) {
  return `<div class="kk stapelk ${o.cls || ''}" ${o.a ? `data-a="${o.a}" data-v="${esc(o.v)}"` : ''}><img src="${bildUrl(rueck)}" alt="" draggable="false">${n != null ? `<span class="zaehler">${n}</span>` : ''}${o.unten ? `<span class="unten">${o.unten}</span>` : ''}</div>`;
}
