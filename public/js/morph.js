// Aktualisiert ein vorhandenes DOM so, dass nur wirklich geänderte Teile angefasst werden.
// Vorteil gegenüber innerHTML: Bilder laden nicht neu (kein Flackern), Scrollstände und Animationen bleiben erhalten.
// Karten haben einen Schlüssel (data-ci), damit sie beim Einfügen/Entfernen mitwandern statt neu zu laden.
const schluessel = (n) => (n.nodeType === 1 ? n.getAttribute('data-ci') : null);

function attribute(alt, neu) {
  for (const a of [...alt.attributes]) if (!neu.hasAttribute(a.name)) alt.removeAttribute(a.name);
  for (const a of neu.attributes) if (alt.getAttribute(a.name) !== a.value) alt.setAttribute(a.name, a.value);
}
function knoten(alt, neu) {
  if (alt.nodeType === 3 || alt.nodeType === 8) { if (alt.nodeValue !== neu.nodeValue) alt.nodeValue = neu.nodeValue; return; }
  attribute(alt, neu);
  if (alt.tagName === 'IMG') return;
  kinder(alt, neu);
}
function kinder(el, neu) {
  const map = new Map();
  for (const n of el.childNodes) { const k = schluessel(n); if (k) map.set(k, n); }
  const nk = [...neu.childNodes];
  nk.forEach((nn, i) => {
    const k = schluessel(nn); let cur = el.childNodes[i];
    if (k && map.has(k)) {
      const m = map.get(k); map.delete(k); if (m !== cur) el.insertBefore(m, cur || null); cur = m;
    } else if (!cur) { el.appendChild(nn.cloneNode(true)); return; }
    else if (k || schluessel(cur) || cur.nodeType !== nn.nodeType || (cur.nodeType === 1 && cur.tagName !== nn.tagName)) { el.insertBefore(nn.cloneNode(true), cur); return; }
    knoten(cur, nn);
  });
  while (el.childNodes.length > nk.length) el.lastChild.remove();
}
export function setHtml(el, html) {
  const t = document.createElement('div'); t.innerHTML = html; kinder(el, t);
}
