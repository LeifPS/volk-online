// Computer-Gegner. Entscheidet immer nur mit Informationen, die der Spieler auch hat (eigene Hand, offene Auslage).
import * as E from './engine.js';
import { waehleStark, setzeBlockHeuristik } from './ki_stark.js';
const { def } = E;
const R = () => E.REGELN();
const rnd = Math.random;
const MEMOS = new WeakMap();
const holeMemo = (s) => { let m = MEMOS.get(s); if (!m) { m = { key: '', n: 0, kampf: false }; MEMOS.set(s, m); } return m; };
const sum = (a) => a.reduce((x, y) => x + y, 0);

export const STUFEN = { leicht: { name: 'Leicht', fehler: 0.28, kampfAb: 6, wunderRes: 3 }, mittel: { name: 'Mittel', fehler: 0.0, kampfAb: 0, wunderRes: 2 }, stark: { name: 'Stark', fehler: 0.0, kampfAb: 0, wunderRes: 2 } };

function bedrohung(s, p) { return Math.max(0, ...E.gegner(s, p).map(o => E.kampfEinheiten(o).length)); }
function landWert(s, p, l) {
  const sym = E.symbole(p), fehlt = {};
  for (const k of p.hand) for (const b of (def(k).braucht || [])) if (!(sym[b] >= 1)) fehlt[b] = (fehlt[b] || 0) + 1 + (def(k).typ === 'einheit' ? 2 : 0);
  return sum(def(l).symbole.map(x => fehlt[x] || 0)) * 3 + def(l).ertrag + rnd() * 0.1;
}
function gebWert(s, p, c) {
  const d = def(c), e = d.effekte, bed = bedrohung(s, p);
  let v = (e.E || 0) * 3.2 + (e.K || 0) * 3.2 + (e.W || 0) * (p.alter < 5 ? 2.2 : 0.5);
  v += (e.S || 0) * (bed >= 2 ? 1.6 : 0.5) + (e.H || 0) * (p.hp < R().stadt_hp ? 1.2 : 0.3);
  v += (e.F || 0) * 2.8 + Math.min(3, e.A || 0) + (e.HL || 0) * 0.6 + ((d.prov || []).length ? 1.5 : 0) + (e.G || 0) * 1.5 + (e.L || 0) * 2 + (e.Z || 0) * 2.2;
  return v / Math.max(1, E.kosten(p, c));
}
function einhWert(s, p, c) {
  const d = def(c); let v = d.staerke + d.fern * 0.8 + sum(Object.values(d.boni)) * 0.5;
  if (d.schluessel.includes('fern') || d.schluessel.includes('belagerung')) v += 1.5;
  if (d.schluessel.includes('ansturm')) v += 1;
  if (d.einkommen || d.ziehen) v = 1.5 + d.einkommen * 2 + d.ziehen;
  if (d.glaube) v += d.glaube * 2.8;
  if (d.schluessel.includes('gruenden')) v = p.hand.some(x => def(x).typ === 'land') ? 3 : 0;
  return v / Math.max(1, E.kosten(p, c));
}
function staatWert(a) { const e = def(a).effekte, d = def(a); return (e.E || 0) * 3 + (e.K || 0) * 3 + (e.W || 0) * 2 + (e.S || 0) * 0.8 + (e.H || 0) * 0.6 + (e.A || 0) + (e.L || 0) * 1.5 + (e.HL || 0) * 0.3 + ((d.prov || []).length ? 1 : 0) + (e.ABLEGEN || 0) * 0.5 + (e.SCHIFF || 0) * 0.3; }
// Erweiterung 3: mögliche Zivilisations-Aktionen mit Wert je Gold
export function civWert(p, d) {
  const e = d.effekte || {}, em = d.einmal || {};
  let v = (e.E || 0) * 3.2 + (e.K || 0) * 3.2 + (e.W || 0) * (p.alter < 5 ? 2.2 : 0.5) + (e.S || 0) * 0.9 + (e.H || 0) * 0.8 + (e.F || 0) * (p.religion ? 2.8 : 0) + Math.min(3, e.A || 0) + (e.HL || 0) * 0.6 + (e.G || 0) * 1.5 + (e.L || 0) * 2 + (e.Z || 0) * 2.2 + (e.SCHIFF || 0) * 0.3;
  v += (em.gold || 0) * 0.9 + (em.ziehen || 0) * 1.3 + (em.heilen || 0) * (p.hp < E.REGELN().stadt_hp - 3 ? 0.5 : 0.1) + (em.aufrichten ? 0.5 : 0);
  return v;
}
export function civOptionen(s, p) {
  const out = []; if (!s.opt.civ || p.civN >= E.daten().civ.pro_zug) return out;
  for (const c of E.daten().regierungen) if (E.civGrund(s, p, c, 'regierung') === null) {
    const alt = p.regierung ? civWert(p, def(p.regierung)) : 0, neu = civWert(p, c);
    if (neu - alt >= 2) out.push({ a: { t: 'regierung', r: c.id }, wert: (neu - alt) / c.kosten, kosten: c.kosten });
  }
  for (const [art, t] of [['pers', 'person'], ['natur', 'natur']]) for (const w of s.civ[art].offen) if (E.civGrund(s, p, w, art) === null) out.push({ a: { t, c: w.i }, wert: civWert(p, def(w)) / def(w).kosten, kosten: def(w).kosten });
  return out;
}
const spielbar = (s, p, c) => E.sperrGrund(s, p, c) === null;
const nichtZivil = (c) => !E.istZivil(c);

export function ziehWahl(s, pi) {
  const p = s.sp[pi], hoch = E.maxStapel(p), i = (E.REGELN().ziehen + E.effekte(p).Z + (p.religion === 'mondgilde' ? 1 : 0)) - s.zieh;
  if (p.religion && p.relStapel.length && !p.relBenutzt) return { t: 'ziehe', stapel: 'rel' };
  let st = hoch; if (hoch > 1 && (p.land.length < 3 + p.alter || rnd() < 0.35) && i % 2 === 1) st = hoch - 1;
  if (!s.stapel[st].length && !s.ablage[st].length) st = [3, 2, 1].find(x => x <= hoch && (s.stapel[x].length || s.ablage[x].length)) || 1;
  return { t: 'ziehe', stapel: st };
}

export function blockWahl(s, pi, stufe = 'mittel') {
  const o = s.sp[pi], k = s.kampf, p = s.sp[k.von], z = {};
  const atk = k.atk.map(id => p.front.find(x => x.i === id)).filter(Boolean).sort((a, b) => def(b).staerke - def(a).staerke);
  let verf = E.einheiten(o).filter(b => !b.t && def(b).staerke >= 1 && !E.istZivil(b));
  for (const a of atk) {
    const kand = verf.filter(b => E.kannBlocken(b, a)), sa = E.staerkeGegen(p, a, null, true);
    const sw = (b) => E.staerkeGegen(p, a, b, true), sv = (b) => E.staerkeGegen(o, b, a, false);
    const gew = kand.filter(b => sv(b) > sw(b)), gl = kand.filter(b => sv(b) === sw(b));
    let b = null;
    if (STUFEN[stufe].fehler && rnd() < STUFEN[stufe].fehler) { z[a.i] = null; continue; }
    if (gew.length) b = gew.reduce((m, x) => def(x).staerke < def(m).staerke ? x : m);
    else if (gl.length && (def(a).staerke >= 2 || o.hp <= 8)) b = gl[0];
    else if (kand.length && o.hp <= def(a).staerke + 2) b = kand.reduce((m, x) => def(x).staerke < def(m).staerke ? x : m);
    if (b) { verf = verf.filter(x => x !== b); z[a.i] = b.i; } else z[a.i] = null;
  }
  return { t: 'blocke', z };
}

export function waehle(s, pi, stufe = 'mittel') {
  if (s.phase === 'wahl') return E.wahlStandard(s, pi);   // Barbaren abwehren / Winter ablegen
  if (stufe === 'stark') return waehleStarkWrap(s, pi);
  return waehleMittel(s, pi, stufe);
}
function waehleStarkWrap(s, pi) {
  if (s.phase === 'ziehen') return ziehWahl(s, pi);
  const memo = holeMemo(s); const key = s.runde + ':' + s.am + ':' + s.phase; if (s.phase === 'block') return waehleStark(s, pi);
  const k2 = s.runde + ':' + s.am; if (memo.key !== k2) { memo.key = k2; memo.n = 0; } memo.n++;
  const p = s.sp[pi]; if (memo.n > 45) return ende(s, p);
  const a = waehleStark(s, pi); return a || ende(s, p);
}
setzeBlockHeuristik((s, pi) => blockWahl(s, pi, 'mittel'));
function waehleMittel(s, pi, stufe = 'mittel') {
  const p = s.sp[pi], cfg = STUFEN[stufe] || STUFEN.mittel;
  if (s.phase === 'block' && s.kampf.ziel === pi) return blockWahl(s, pi, stufe);
  if (s.phase === 'ziehen') return ziehWahl(s, pi);
  const memo = holeMemo(s); const key = s.runde + ':' + s.am; if (memo.key !== key) { memo.key = key; memo.n = 0; memo.kampf = false; } memo.n++;
  if (memo.n > 70) return ende(s, p);
  // Wissenschaftssieg: in der Atomzeit sofort bezahlen, wenn möglich
  if (E.wissenSiegMoeglich(p) && E.aufstiegErlaubt(p) && p.gold >= E.aufstiegKosten(p)) return { t: 'aufstieg' };
  // Wissenschaftssieg vorbereiten: im letzten Zeitalter Gold sparen, wenn der Sieg in Reichweite ist und keine Gefahr droht
  if (E.wissenSiegMoeglich(p) && E.aufstiegErlaubt(p)) {
    const fehl = E.aufstiegKosten(p) - p.gold;
    if (fehl > 0 && fehl <= 2 * E.einkommen(s, p) && bedrohung(s, p) < p.hp - 2) {
      if (!memo.kampf) { const a = kampf(s, pi, cfg); if (a) return a; memo.kampf = true; }
      return ende(s, p);
    }
  }
  // Missionare ausweisen
  const bei = E.missionenBei(s, p);
  if (bei.length && s.opt.rel) {
    const kst = p.religion === 'flammenorden' ? 1 : 2;
    const gefahr = bei.find(m => E.glaube(s, s.sp[m.owner]) >= s.glaubeZiel - 4);   // Missionar eines Spielers, der dem Glaubenssieg nahe ist
    if (gefahr && p.gold >= kst + 1) return { t: 'ausweisen', c: gefahr.c.i };
    if (p.gold >= 8 && E.einkommen(s, p) >= 6) return { t: 'ausweisen', c: bei[0].c.i };
  }
  if (cfg.fehler && rnd() < cfg.fehler * 0.4) return ende(s, p);
  // 1. Land
  const ls = p.hand.filter(c => def(c).typ === 'land');
  if (ls.length && p.landG < E.landErlaubt(p)) return { t: 'land', c: ls.reduce((m, x) => landWert(s, p, x) > landWert(s, p, m) ? x : m).i };
  // Religion gründen
  if (s.opt.rel && !p.religion && s.relFrei.length && p.alter >= 1 && p.gold >= 7 && p.hand.length >= 2 && s.runde >= 2) {
    const op = p.hand.filter(c => !c.vk && !def(c).relkarte); if (op.length) return { t: 'gruenden', rel: s.relFrei[Math.floor(rnd() * s.relFrei.length)], c: op.reduce((m, x) => E.kartenWert(p, x) < E.kartenWert(p, m) ? x : m).i };
  }
  if (s.opt.rel && p.religion) {
    const ms = p.hand.filter(c => def(c).klasse === 'missionar' && p.gold >= E.kosten(p, c));
    if (ms.length) { const ziele = E.gegner(s, p).filter(o => !s.missionen.some(m => s.sp[m.owner] === p && s.sp[m.host] === o)); if (ziele.length) { const o = ziele.reduce((m, x) => E.glaube(s, x) > E.glaube(s, m) ? x : m); return { t: 'mission', c: ms[0].i, ziel: s.sp.indexOf(o) }; } }
  }
  // 2. Wunder
  for (const w of s.wunderOffen.slice().sort((a, b) => def(a).kosten - def(b).kosten)) {
    const z = E.zukauf(p, w), d = def(w);
    if (d.zeitalter <= p.alter && z !== null && p.gold >= d.kosten + z + (E.kultur(p) >= E.REGELN().kultur_sieg - 3 ? 0 : cfg.wunderRes) && spielbar(s, p, w)) return { t: 'wunder', c: w.i };
  }
  // 3. Heer
  const army = E.kampfEinheiten(p).length, wunsch = Math.min(6, Math.max(s.runde >= 2 ? 2 : 1, bedrohung(s, p) + 1));
  const kand = p.hand.filter(c => def(c).typ === 'einheit' && def(c).klasse !== 'missionar' && spielbar(s, p, c) && nichtZivil(c) && def(c).staerke > 0 && !def(c).schluessel.includes('gruenden'));
  if (army < wunsch && kand.length) return { t: 'spiele', c: kand.reduce((m, x) => einhWert(s, p, x) + def(x).staerke * 0.15 > einhWert(s, p, m) + def(m).staerke * 0.15 ? x : m).i };
  // 4. Wirtschaft
  const wk = p.hand.filter(c => def(c).typ === 'einheit' && spielbar(s, p, c) && (def(c).einkommen || def(c).ziehen || def(c).schluessel.includes('gruenden')) && einhWert(s, p, c) >= 0.6);
  if (wk.length && s.runde <= 18) return { t: 'spiele', c: wk.reduce((m, x) => einhWert(s, p, x) > einhWert(s, p, m) ? x : m).i };
  // 5. Gebäude
  const gk = p.hand.filter(c => def(c).typ === 'gebaeude' && spielbar(s, p, c) && gebWert(s, p, c) >= 0.45);
  if (gk.length) return { t: 'spiele', c: gk.reduce((m, x) => gebWert(s, p, x) > gebWert(s, p, m) ? x : m).i };
  // 5b. Zivilisation (Regierung, Persönlichkeiten, Naturwunder)
  { const co = civOptionen(s, p).filter(o => o.wert >= 0.45 && p.gold >= o.kosten + (E.kultur(p) >= E.REGELN().kultur_sieg - 3 ? 0 : 1)).sort((a, b) => b.wert - a.wert); if (co.length) return co[0].a; }
  // 6. Aufstieg
  const ak = E.aufstiegKosten(p); if (ak !== null && E.aufstiegErlaubt(p) && p.gold >= ak) return { t: 'aufstieg' };
  // 7. Tribut
  for (const a of s.auslage) if (p.gold >= def(a).kosten && p.staaten.length < 2 && staatWert(a) >= 1) return { t: 'tribut', c: a.i };
  // 8. weitere Einheiten
  const k2 = p.hand.filter(c => def(c).typ === 'einheit' && def(c).klasse !== 'missionar' && spielbar(s, p, c) && def(c).staerke > 0 && nichtZivil(c) && !def(c).schluessel.includes('gruenden'));
  if (k2.length && army < 9 && p.gold >= 3) return { t: 'spiele', c: k2.reduce((m, x) => einhWert(s, p, x) > einhWert(s, p, m) ? x : m).i };
  // Kampf
  if (!memo.kampf) { const a = kampf(s, pi, cfg); if (a) return a; memo.kampf = true; }
  // Ablegen für Gold
  if (p.ablN < E.REGELN().ablegen_max && p.hand.length > 3) {
    const tot = p.hand.find(c => !c.vk && !def(c).relkarte && ((def(c).typ !== 'land' && def(c).zeitalter > p.alter + 1) || (def(c).typ === 'gebaeude' && p.geb.some(g => g.id === c.id))));
    if (tot) return { t: 'ablegen', c: tot.i };
  }
  return ende(s, p);
}
function ende(s, p) {
  const zuviel = E.handZaehlt(p).length - E.handlimit(p);
  if (zuviel <= 0) return { t: 'ende' };
  const ids = E.handZaehlt(p).sort((a, b) => E.kartenWert(p, a) - E.kartenWert(p, b)).slice(0, zuviel).map(c => c.i);
  return { t: 'ende', abwerfen: ids };
}
function kampf(s, pi, cfg) {
  const p = s.sp[pi]; if (E.schutzAktiv(s) || s.runde < cfg.kampfAb) return null;
  const gegn = E.gegner(s, p); if (!gegn.length) return null;
  const ziel = gegn.reduce((m, o) => (o.hp - 0.5 * E.kampfEinheiten(o).length) < (m.hp - 0.5 * E.kampfEinheiten(m).length) ? o : m), zi = s.sp.indexOf(ziel);
  // Schüsse (einer pro Aufruf)
  for (const u of p.front.filter(E.kannSchiessen)) {
    const d = def(u), ziele = E.schussZiele(s, p, u), stadt = d.schluessel.includes('belagerung');
    if (stadt && (!ziele.length || ziel.hp <= d.fern + 3)) return { t: 'schuss', c: u.i, stadt: true, p: zi };
    if (ziele.length) { const best = ziele.reduce((m, z) => { const t = (o) => def(s.sp[o.p].front.concat(s.sp[o.p].kaserne).find(x => x.i === o.c)); return (def({ id: t(z).id }).staerke + t(z).fern * 0.5) > (t(m).staerke + t(m).fern * 0.5) ? z : m; }); return { t: 'schuss', c: u.i, p: best.p, z: best.c }; }
  }
  // Angriff
  const bereit = p.front.filter(u => E.kannAngreifen(u) && !(def(u).schluessel.includes('fern') && ['fernkampf', 'see_fern', 'u_boot', 'jaeger'].includes(def(u).klasse)) && !(def(u).schluessel.includes('belagerung') && def(u).fern > 0) && !def(u).schluessel.includes('luftabwehr')).sort((a, b) => def(b).staerke - def(a).staerke);
  if (!bereit.length) return null;
  const gb = E.einheiten(ziel).filter(b => !b.t && def(b).staerke >= 1 && !E.istZivil(b));
  const maxb = Math.max(0, ...gb.map(b => def(b).staerke + (def(b).schluessel.includes('ansturm') ? 2 : 0)));
  const bed = Math.max(0, ...gegn.map(o => E.kampfEinheiten(o).length)), daheim = Math.floor((bed + 1) / 2), ang = [];
  for (const u of bereit) { if (bereit.length - ang.length <= daheim && gb.length) break; if (!gb.length || E.staerkeGegen(p, u, null, true) > maxb || ziel.hp <= 6) ang.push(u); }
  if (!ang.length) return null;
  return { t: 'angriff', ids: ang.map(u => u.i), ziel: zi };
}
