// Anzeige-Texte: Karten, Effekte, Namen
import { def, daten } from './engine.js';
export const EFF_LANG = {
  E: n => `+${n} Einkommen`, K: n => `+${n} Kultur`, W: n => `Aufstieg −${n} Gold`, S: n => `+${n} Schutz (Stadtschaden −${n})`,
  H: n => `Stadt heilt ${n} je Runde`, A: n => `Einheiten −${n} Gold (max. 3)`, HL: n => `Handlimit +${n}`, G: n => `Gebäude −${n} Gold`,
  L: n => `+${n} Land je Zug`, Z: n => `Ziehe +${n} Karte`, F: n => `+${n} Glaube`, ABLEGEN: n => `Ablegen gibt +${n} Gold`, SCHIFF: n => `Schiffe +${n} Stärke`,
};
export const SCHL = { gruenden: 'Gründet Stadt', fern: 'Fernkampf', ansturm: 'Ansturm', tarnung: 'Tarnung', belagerung: 'Belagerung', ramme: 'Ramme', fliegend: 'Fliegend', traeger: 'Träger', luftabwehr: 'Luftabwehr', heilen: 'Heilt', einmalig: 'Einmalig', mission: 'Missionar' };
export const SCHL_TXT = {
  gruenden: 'Legt beim Spielen bis zu 2 Land-Karten aus der Hand sofort aus.', fern: 'Schießt aus der Ferne, ohne zu blocken.', ansturm: 'Beim Angriff +1 Stärke.', tarnung: 'Kann nicht beschossen werden.',
  belagerung: 'Darf die Stadt aus der Ferne beschießen.', ramme: 'Doppelter Schaden an der Stadt.', fliegend: 'Luft-Einheit: nur Luft/Luftabwehr kann sie blocken.', traeger: 'Gibt dir ein Flugfeld (Symbol „Flug“).',
  luftabwehr: 'Kann Luft-Einheiten blocken, +3 gegen sie.', heilen: 'Stadt heilt +1 je Runde.', einmalig: 'Wird nach dem Einsatz verbraucht.', mission: 'Wird zu einem Gegner gesandt und bringt dir Glaube.',
};
export const TAG = { nahkampf: 'Nahkampf', reiter: 'Reiter', see: 'Schiffe', luft: 'Luft', stadt: 'die Stadt', bomber: 'Bomber', u_boot: 'U-Boote', rakete: 'Raketen', belagerung: 'Belagerung' };
export const ROH = { marmor: 'Marmor', stein: 'Stein', holz: 'Holz', eisen: 'Eisen', kupfer: 'Kupfer', zinn: 'Zinn', pferde: 'Pferde', salpeter: 'Salpeter', kohle: 'Kohle', oel: 'Öl', aluminium: 'Aluminium', uran: 'Uran', elefanten: 'Elefanten', lehm: 'Lehm', salz: 'Salz', seltene_erden: 'Seltene Erden', deuterium: 'Deuterium', titan: 'Titan', helium3: 'Helium-3', kueste: 'Küste', flug: 'Flugfeld', bibliothek: 'Bibliothek' };
export const KLASSE = { zivil: 'Zivil', haendler: 'Händler', see_zivil: 'Schiff (zivil)', nahkampf: 'Nahkampf', fernkampf: 'Fernkampf', reiter: 'Reiter', belagerung: 'Belagerung', see_nah: 'Schiff', see_fern: 'Schiff (Fern)', u_boot: 'U-Boot', jaeger: 'Jäger', bomber: 'Bomber', flak: 'Flugabwehr', traeger: 'Träger', rakete: 'Rakete', atom: 'Atomwaffe', spaeher: 'Späher', sanitaeter: 'Sanitäter', missionar: 'Missionar' };
export const ZA = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI'];
export const zaName = (i) => daten().zeitalter[i]?.name || '';
export function effektZeilen(d) {
  const z = [];
  for (const [k, v] of Object.entries(d.effekte || {})) if (v && EFF_LANG[k]) z.push(EFF_LANG[k](v));
  return z;
}
export function kartenArt(d) {
  if (d.typ === 'land') return `Land · ${d.gelaende_name}`;
  if (d.typ === 'gebaeude') return d.relkarte ? `Religion · ${d.sorte === 'heiligtum' ? 'Heiligtum' : d.sorte === 'tempel' ? 'Tempel' : d.sorte === 'halle' ? 'Halle' : 'Stätte'}` : 'Gebäude';
  if (d.typ === 'einheit') return KLASSE[d.klasse] || 'Einheit';
  if (d.typ === 'wunder') return 'Wunder'; if (d.typ === 'stadtstaat') return 'Stadtstaat';
  if (d.typ === 'regierung') return 'Regierung'; if (d.typ === 'person') return 'Große Persönlichkeit'; if (d.typ === 'natur') return 'Naturwunder'; return d.typ;
}
export function kartenZeilen(d) {
  const z = [];
  if (d.typ === 'einheit') {
    if (d.staerke || d.fern) z.push(`Stärke ${d.staerke}` + (d.fern ? ` · Fern ${d.fern}` : ''));
    if (d.einkommen) z.push(`+${d.einkommen} Einkommen`); if (d.ziehen) z.push(`Ziehe +${d.ziehen} Karte`); if (d.glaube) z.push(`+${d.glaube} Glaube`);
    for (const s of d.schluessel) if (SCHL[s] && s !== 'fern') z.push(SCHL[s]);
    for (const [t, n] of Object.entries(d.boni || {})) if (n) z.push(`+${n} gegen ${TAG[t] || t}`);
  } else if (d.typ === 'land') {
    z.push(d.ertrag ? `+${d.ertrag} Gold je Runde` : ''); for (const s of d.symbole || []) z.push('Symbol: ' + (ROH[s] || s));
  } else if (d.typ === 'wunder') { z.push(...effektZeilen(d)); for (const t of d.text || []) z.push(t); }
  else z.push(...effektZeilen(d));
  for (const p of d.prov || []) z.push('Liefert: ' + (ROH[p] || p));
  return z.filter(Boolean);
}
export const braucht = (d) => (d.braucht || []).map(b => ROH[b] || b);
export const benoetigt = (d) => (d.benoetigt || []).map(b => def({ id: b })?.name || b);
export function farbeKarte(d) { const D = daten(); if (d.relkarte) return d.farbe_rel; if (d.volkskarte) return d.farbe_volk; return D.zeitalter[d.zeitalter]?.farbe || '#999'; }
