// "Stark": 1-Zug-Vorausschau. Für jede mögliche Aktion wird der Spielzustand kopiert, die Aktion ausgeführt
// (bei Angriffen samt der wahrscheinlichen Verteidigung) und das Ergebnis mit einer Bewertungsfunktion beurteilt.
// Die Gewichte (PARAM) wurden per Selbstspiel-Turnier (Kreuzentropie-Methode) gegen die Stufe "Mittel" abgestimmt.
import * as E from './engine.js';
import { PARAM as PARAM_STANDARD } from './ki_params.js';
const { def } = E;
let PARAM = PARAM_STANDARD;
export const setzeParam = (p) => { PARAM = p; };
export const holeParam = () => PARAM;
const klon = (s) => structuredClone(s);
const sum = (a) => a.reduce((x, y) => x + y, 0);

// ---------- Bewertung eines Spielers ----------
function restRunden(s) { return Math.max(PARAM.tMin, PARAM.tBasis - s.runde * PARAM.tFall); }
function bedrohung(s, p) {          // erwarteter Schaden, den die Gegner mir im nächsten Umlauf zufügen könnten
  if (s.ereigZ + 1 < E.REGELN().schutz_runden) return 0;
  const bl = E.einheiten(p).filter(u => !u.t && def(u).staerke >= 1 && !E.istZivil(u)).map(u => def(u).staerke).sort((a, b) => b - a), S = E.schutz(p); let worst = 0;
  for (const o of E.gegner(s, p)) {
    const at = E.einheiten(o).filter(u => def(u).staerke >= 1 && !E.istZivil(u)).map(u => def(u).staerke + (def(u).schluessel.includes('ansturm') ? 1 : 0)).sort((a, b) => b - a);
    const frei = bl.slice(); let dmg = 0;
    for (const a of at) { let k = -1; for (let i = frei.length - 1; i >= 0; i--) if (frei[i] >= a) { k = i; break; } if (k >= 0) frei.splice(k, 1); else dmg += Math.max(1, a - S); }
    for (const u of E.einheiten(o)) { const d = def(u); if (d.schluessel.includes('belagerung') && d.fern) dmg += Math.max(1, d.fern - S) * 0.6; }
    worst = Math.max(worst, dmg);
  }
  return worst;
}
export function wert(s, i) {
  const p = s.sp[i]; if (p.tot || p.hp <= 0) return -1e6; if (s.sieger !== null && s.grund === 'Wissenschaft') return s.sieger === i ? 1e6 : -1e6; const R = E.REGELN(), T = restRunden(s), e = E.effekte(p);
  const k = E.kultur(p); if (k >= R.kultur_sieg) return 1e6;
  let g = 0; if (s.opt.rel && p.religion) { g = E.glaube(s, p); if (g >= s.glaubeZiel) return 1e6; }
  let v = PARAM.wK * k + PARAM.wK2 * k * k / R.kultur_sieg + (k >= R.kultur_sieg - 3 ? PARAM.wKnah * (k - (R.kultur_sieg - 4)) : 0);
  v += PARAM.wE * E.einkommen(s, p) * T + PARAM.wG * p.gold + PARAM.wA * p.alter;
  v += PARAM.wLand * p.land.length + PARAM.wSym * Object.keys(E.symbole(p)).length;
  v += PARAM.wGeb * p.geb.length + PARAM.wStaat * p.staaten.length;
  v += (PARAM.wZ * e.Z + PARAM.wL * e.L + PARAM.wG2 * e.G + PARAM.wAus * e.A + PARAM.wW * e.W + PARAM.wHL * e.HL) * T * 0.5;
  // Heer und Verteidigung
  const kampf = E.kampfEinheiten(p); const st = kampf.map(u => def(u).staerke + def(u).fern * 0.5);
  v += PARAM.wHeer * Math.min(sum(st), PARAM.heerMax) + PARAM.wHeerN * Math.min(kampf.length, 5);
  v += PARAM.wFern * sum(kampf.filter(u => E.kannSchiessen(u)).map(u => def(u).fern));
  const dmg = bedrohung(s, p); v -= PARAM.wDmg * Math.min(dmg, p.hp) + (dmg >= p.hp ? PARAM.wTod : 0);
  v += PARAM.wHP * Math.min(p.hp, R.stadt_hp) - PARAM.wHPnied * Math.max(0, 10 - p.hp) ** 2 / 10;
  v += PARAM.wSchutz * e.S * Math.min(2, E.gegner(s, p).length) + PARAM.wHeil * E.heilung(p) * T * 0.3;
  v += PARAM.wHand * Math.min(E.handZaehlt(p).length, E.handlimit(p)) + PARAM.wVK * p.hand.filter(c => c.vk).length;
  // Glaube
  if (s.opt.rel) {
    if (p.religion) { v += PARAM.wRel + PARAM.wF * g + PARAM.wF2 * g * g / s.glaubeZiel + (g >= s.glaubeZiel - 3 ? PARAM.wKnah * (g - (s.glaubeZiel - 4)) : 0); v += PARAM.wRelKarte * p.relStapel.length; v += PARAM.wMis * E.missionenAus(s, p).length - PARAM.wMisFremd * E.missionenBei(s, p).length; }
  }
  return v;
}
function gesamt(s, i, ohneGegner) {
  const me = wert(s, i); if (me >= 1e6 || me <= -1e6) return me;
  const gs = s.sp.map((_, j) => j).filter(j => j !== i && !s.sp[j].tot); if (!gs.length) return me;
  const w = gs.map(j => wert(s, j)); if (w.some(x => x >= 1e6)) return -1e6 + me * 0.001;
  return me - PARAM.lambda * (sum(w) / gs.length) - PARAM.lambdaMax * Math.max(...w);
}

// ---------- Kandidaten ----------
function kandidaten(s, pi) {
  const p = s.sp[pi], R = E.REGELN(), out = [];
  if (p.landG < E.landErlaubt(p)) { const ids = new Set(); for (const c of p.hand) if (def(c).typ === 'land' && !ids.has(c.id)) { ids.add(c.id); out.push({ t: 'land', c: c.i }); } }
  const gesehen = new Set();
  for (const c of p.hand) { const d = def(c); if ((d.typ === 'einheit' || d.typ === 'gebaeude') && d.klasse !== 'missionar' && !gesehen.has(c.id) && E.sperrGrund(s, p, c) === null) { gesehen.add(c.id); out.push({ t: 'spiele', c: c.i }); } }
  for (const w of s.wunderOffen) if (E.sperrGrund(s, p, w) === null) out.push({ t: 'wunder', c: w.i });
  const ak = E.aufstiegKosten(p); if (ak !== null && E.aufstiegErlaubt(p) && p.gold >= ak) out.push({ t: 'aufstieg' });
  if (p.staaten.length < 2) for (const t of s.auslage) if (p.gold >= def(t).kosten) out.push({ t: 'tribut', c: t.i });
  if (p.ablN < R.ablegen_max) { const ids = new Set(); for (const c of p.hand) if (!c.vk && !ids.has(c.id)) { ids.add(c.id); out.push({ t: 'ablegen', c: c.i }); } }
  if (s.opt.civ) for (const x of civOpt(s, p)) out.push(x);
  if (s.opt.rel) {
    if (!p.religion && p.alter >= 1 && p.gold >= 5 && s.relFrei.length) { const op = p.hand.filter(c => !c.vk && !def(c).relkarte).sort((a, b) => E.kartenWert(p, a) - E.kartenWert(p, b)).slice(0, 2); for (const r of s.relFrei) for (const o of op) out.push({ t: 'gruenden', rel: r, c: o.i }); }
    if (p.religion) for (const c of p.hand) if (def(c).klasse === 'missionar' && p.gold >= E.kosten(p, c)) for (const o of E.gegner(s, p)) if (!s.missionen.some(m => m.owner === pi && s.sp[m.host] === o)) out.push({ t: 'mission', c: c.i, ziel: s.sp.indexOf(o) });
    const kst = p.religion === 'flammenorden' ? 1 : 2; for (const m of E.missionenBei(s, p)) if (p.gold >= kst) out.push({ t: 'ausweisen', c: m.c.i });
  }
  if (!E.schutzAktiv(s)) {
    for (const u of p.front.filter(E.kannSchiessen)) {
      const d = def(u); for (const z of E.schussZiele(s, p, u)) out.push({ t: 'schuss', c: u.i, p: z.p, z: z.c });
      if (d.schluessel.includes('belagerung')) for (const o of E.gegner(s, p)) out.push({ t: 'schuss', c: u.i, stadt: true, p: s.sp.indexOf(o) });
    }
    const bereit = p.front.filter(E.kannAngreifen).sort((a, b) => def(b).staerke - def(a).staerke);
    if (bereit.length) for (const o of E.gegner(s, p)) { const zi = s.sp.indexOf(o), seen = new Set(); for (let k = 1; k <= bereit.length; k++) { for (const sub of [bereit.slice(0, k), bereit.slice(bereit.length - k)]) { const key = sub.map(u => u.i).sort().join(','); if (!seen.has(key)) { seen.add(key); out.push({ t: 'angriff', ids: sub.map(u => u.i), ziel: zi }); } } } }
  }
  return out;
}
function civOpt(s, p) {
  const out = []; if (p.civN >= E.daten().civ.pro_zug) return out;
  for (const c of E.daten().regierungen) if (E.civGrund(s, p, c, 'regierung') === null) out.push({ t: 'regierung', r: c.id });
  for (const [art, t] of [['pers', 'person'], ['natur', 'natur']]) for (const w of s.civ[art].offen) if (E.civGrund(s, p, w, art) === null) out.push({ t, c: w.i });
  return out;
}
function ausfuehren(s, pi, a, verteidiger) {
  const s2 = klon(s), r = E.aktion(s2, pi, a); if (!r.ok) return null;
  if (s2.phase === 'block') { const z = verteidiger(s2, s2.kampf.ziel); E.aktion(s2, s2.kampf.ziel, { t: 'blocke', z }); }
  for (let n = 0; s2.phase === 'wahl' && n < 12; n++) { const w = E.akteur(s2); E.aktion(s2, w, E.wahlStandard(s2, w)); }
  return s2;
}

// ---------- Hauptfunktion ----------
let blockHeuristik = null;
export const setzeBlockHeuristik = (f) => { blockHeuristik = f; };
export function waehleStark(s, pi, memo) {
  const p = s.sp[pi];
  if (s.phase === 'block') return blockStark(s, pi);
  const basis = gesamt(s, pi); let beste = null, bw = basis + PARAM.schwelle;
  const kand = kandidaten(s, pi);
  for (const a of kand) {
    const s2 = ausfuehren(s, pi, a, (st, d) => blockHeuristik(st, d).z); if (!s2) continue;
    let w = gesamt(s2, pi);
    if (a.t === 'angriff') w += PARAM.angriffBonus;
    if (w > bw) { bw = w; beste = a; }
  }
  return beste;
}
// Verteidigung: alle sinnvollen Zuordnungen durchprobieren, beste nach Bewertung nehmen
function blockStark(s, pi) {
  const k = s.kampf, a = s.sp[k.von], o = s.sp[pi];
  const atk = k.atk.map(id => a.front.find(x => x.i === id)).filter(Boolean);
  const bl = E.einheiten(o).filter(b => !b.t && def(b).staerke >= 1 && !E.istZivil(b));
  const opts = atk.map(u => [null, ...bl.filter(b => E.kannBlocken(b, u)).map(b => b.i)]);
  let alle = [{}], n = 0;
  for (let i = 0; i < atk.length; i++) { const neu = []; for (const z of alle) for (const b of opts[i]) { if (b !== null && Object.values(z).includes(b)) continue; neu.push({ ...z, [atk[i].i]: b }); } alle = neu.length > 150 ? neu.slice(0, 150) : neu; }
  const heur = blockHeuristik(s, pi).z; alle.push(heur);
  let best = heur, bw = -Infinity;
  for (const z of alle) { const s2 = klon(s); const r = E.aktion(s2, pi, { t: 'blocke', z }); if (!r.ok) continue; const w = gesamt(s2, pi); if (w > bw) { bw = w; best = z; } }
  return { t: 'blocke', z: best };
}
