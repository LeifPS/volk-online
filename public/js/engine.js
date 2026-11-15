// Regel-Engine für "Volk – Das Kartenspiel" (Grundspiel + Erweiterung 1 Volkskarten + Erweiterung 2 Götter & Glaube).
// Reine Logik ohne DOM: läuft im Browser (gegen Computer) und im Cloudflare Worker (online, maßgeblich).
// Der Zustand ist reines JSON. Alle Änderungen laufen über aktion(s, spielerIdx, a).

let D = null, ID = {}, R = null;
export function setzeDaten(daten) {
  D = daten; R = D.regeln; ID = {};
  for (const l of [D.karten, D.volkskarten, D.relkarten, D.wunder, D.staaten, D.ereignisse]) for (const k of l) ID[k.id] = k;
  for (const e of D.rel_ereignisse) ID[e.id] = Object.assign({ typ: 'ereignis', art: 'rel', plus: 0 }, e);
}
export const daten = () => D;
export const def = (c) => ID[c.id];
export const REGELN = () => R;
export const ZIVIL = ['zivil', 'haendler', 'see_zivil'];

// ---------- Zufall (mulberry32, Zustand im Spielzustand) ----------
function zuf(s) { let t = (s.rng += 0x6D2B79F5) >>> 0; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }
export const zufall = zuf;
function mische(s, a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(zuf(s) * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
const neu = (s, id, extra) => Object.assign({ i: s.nid++, id }, extra || {});

// ---------- Spiel erzeugen ----------
// spieler: [{name, volk?, ki?}], opt: {vk:true/false, rel:true/false, seed}
export function neuesSpiel(spieler, opt = {}) {
  const s = { v: 1, rng: (opt.seed ?? Math.floor(Math.random() * 2 ** 31)) >>> 0, nid: 1, seq: 0, ev: [], opt: { vk: !!opt.vk, rel: !!opt.rel }, runde: 1, am: 0, phase: 'ziehen', sieger: null, grund: null, ereigZ: 0 };
  const volkIds = D.voelker.map(v => v.id); const frei = mische(s, volkIds.filter(v => !spieler.some(p => p.volk === v)));
  s.sp = spieler.map((p, i) => ({ name: p.name, ki: p.ki || null, volk: p.volk || frei.pop(), volkF: '', hand: [], land: [], geb: [], wunder: [], staaten: [], front: [], kaserne: [], gold: R.start_gold, hp: R.stadt_hp, alter: 0, landG: 0, ablN: 0, tot: false, religion: null, relStapel: [], relBenutzt: false }));
  for (const p of s.sp) p.volkF = D.voelker.find(v => v.id === p.volk).farbe;
  s.stapel = { 1: [], 2: [], 3: [] }; s.ablage = { 1: [], 2: [], 3: [] };
  for (const k of D.karten) for (let n = 0; n < k.kopien; n++) s.stapel[k.stapel].push(neu(s, k.id));
  for (const st of [1, 2, 3]) mische(s, s.stapel[st]);
  s.wunderStapel = D.wunder.map(w => neu(s, w.id)); s.wunderOffen = [];
  s.staatStapel = mische(s, D.staaten.map(x => neu(s, x.id))); s.auslage = [];
  s.ereig = D.ereignisse.map(e => neu(s, e.id)); if (s.opt.rel) for (const e of D.rel_ereignisse) s.ereig.push(neu(s, e.id));
  mische(s, s.ereig); s.ereigAblage = [];
  s.missionen = []; s.relFrei = s.opt.rel ? D.religionen.map(r => r.id) : [];
  s.glaubeZiel = s.opt.vk ? D.glaube_sieg_vk : D.glaube_sieg;
  for (const p of s.sp) { for (let k = 0; k < R.start_hand; k++) ziehe(s, p, 1); volkskarte(s, p); }
  for (let k = 0; k < 3; k++) { wunderNach(s); if (s.staatStapel.length) s.auslage.push(s.staatStapel.pop()); }
  log(s, 'start', 'Das Spiel beginnt.');
  zugStart(s);
  return s;
}
function wunderNach(s) { if (s.wunderStapel.length) s.wunderOffen.push(s.wunderStapel.shift()); }
function log(s, k, t, p, extra) { s.ev.push(Object.assign({ n: ++s.seq, k, t, p: p ?? null }, extra || {})); if (s.ev.length > 80) s.ev.splice(0, s.ev.length - 80); }

// ---------- Hilfsfunktionen ----------
export const P = (s, i) => s.sp[i];
export function ziehe(s, p, st) {
  if (!s.stapel[st].length) { s.stapel[st] = mische(s, s.ablage[st].splice(0)); }
  if (!s.stapel[st].length) return null;
  const c = s.stapel[st].pop(); p.hand.push(c); return c;
}
function volkskarte(s, p) {
  if (!s.opt.vk) return;
  const k = D.volkskarten.find(x => x.volk === p.volk && x.zeitalter === p.alter);
  if (k) p.hand.push(neu(s, k.id, { vk: 1 }));
}
export function legeAb(s, p, c) {
  const d = def(c); c.t = 0;
  if (d.relkarte) { p.relStapel.unshift(c); return; }
  if (c.vk) { p.hand.push(c); return; }
  if (d.stapel) s.ablage[d.stapel].push(c);
}
export const lebende = (s) => s.sp.filter(p => !p.tot);
export const gegner = (s, p) => s.sp.filter(o => o !== p && !o.tot);
export const einheiten = (p) => p.front.concat(p.kaserne);
export const istZivil = (c) => ZIVIL.includes(def(c).klasse);
export const kampfEinheiten = (p) => einheiten(p).filter(u => def(u).staerke > 0 && !istZivil(u));
export function effekte(p) {
  const e = {};
  for (const c of p.geb.concat(p.wunder, p.staaten)) for (const [a, b] of Object.entries(def(c).effekte || {})) e[a] = (e[a] || 0) + b;
  if (p.religion === 'mondgilde') e.HL = (e.HL || 0) + 2; else if (p.religion === 'hain') e.H = (e.H || 0) + 2;
  else if (p.religion === 'berggeister') e.S = (e.S || 0) + 2; else if (p.religion === 'sternenorakel') e.W = (e.W || 0) + 1;
  return new Proxy(e, { get: (t, k) => t[k] || 0 });
}
export function missionenBei(s, p) { return s.missionen.filter(m => s.sp[m.host] === p); }
export function missionenAus(s, p) { return s.missionen.filter(m => s.sp[m.owner] === p); }
export function glaube(s, p) {
  if (!p.religion) return 0;
  let g = 1 + effekte(p).F + einheiten(p).reduce((a, u) => a + (def(u).glaube || 0), 0);
  g += missionenAus(s, p).length - Math.max(0, missionenBei(s, p).length - (p.religion === 'berggeister' ? 1 : 0));
  if (p.religion === 'hain') g += Math.floor(p.land.length / 3);
  return Math.max(0, g);
}
export function symbole(p) {
  const sym = {}; const add = (x) => { sym[x] = (sym[x] || 0) + 1; };
  for (const l of p.land) for (const x of def(l).symbole) add(x);
  for (const c of p.geb.concat(p.wunder, p.staaten)) for (const x of (def(c).prov || [])) add(x);
  for (const u of einheiten(p)) if (def(u).schluessel.includes('traeger')) add('flug');
  if (p.volk === 'nordleute') add('kueste');
  return sym;
}
export const kultur = (p) => effekte(p).K;
export const schutz = (p) => effekte(p).S;
export const heilung = (p) => effekte(p).H + einheiten(p).filter(u => def(u).schluessel.includes('heilen')).length;
export function einkommen(s, p) {
  const e = effekte(p);
  let g = R.basis_einkommen + p.alter + p.land.reduce((a, l) => a + def(l).ertrag, 0) + e.E;
  g += einheiten(p).reduce((a, u) => a + ((def(u).einkommen || 0) + (p.volk === 'goldener_bund' && def(u).einkommen ? 1 : 0)), 0);
  if (p.volk === 'sonnenvolk' && p.land.length >= 3) g += 1;
  if (p.religion === 'sonnenkult') g += Math.floor(glaube(s, p) / 3);
  if (p.religion === 'gezeiten' && symbole(p).kueste) g += 1;
  return g;
}
export const handlimit = (p) => R.handlimit + effekte(p).HL;
export const handZaehlt = (p) => p.hand.filter(c => !c.vk);
export function kosten(p, c) {
  const d = def(c); let k = d.kosten;
  if (d.typ === 'einheit') {
    let red = Math.min(3, effekte(p).A);
    if (['zivil', 'haendler', 'see_zivil', 'spaeher', 'missionar'].includes(d.klasse)) red = 0;
    k -= red;
    if (p.volk === 'nordleute' && d.tags.includes('see')) k--;
    if (p.religion === 'gezeiten' && d.tags.includes('see')) k--;
    if (p.religion === 'windwanderer' && d.schluessel.includes('mission')) k--;
    if (p.volk === 'steppenreiter' && d.tags.includes('reiter')) k--;
    k = Math.max(1, k);
  } else if (d.typ === 'gebaeude') k = Math.max(1, k - effekte(p).G);
  return k;
}
export function aufstiegKosten(p) {
  if (p.alter >= 6) return null;
  return Math.max(1, R.aufstieg[p.alter] - effekte(p).W - (p.volk === 'sternendeuter' ? 1 : 0));
}
// Kosten für fehlende Rohstoffe; null = nicht spielbar
export function zukauf(p, c) {
  const sym = symbole(p); let fehlt = 0;
  for (const b of (def(c).braucht || [])) { if ((sym[b] || 0) >= 1) continue; if (b === 'kueste' || b === 'flug') return null; fehlt++; }
  return fehlt > R.zukauf_max ? null : fehlt * R.zukauf_preis;
}
export function kostenGesamt(p, c) { const z = zukauf(p, c); return z === null ? null : (def(c).typ === 'wunder' ? def(c).kosten : kosten(p, c)) + z; }
// Grund, warum eine Karte nicht gespielt werden kann (null = ok)
export function sperrGrund(s, p, c) {
  const d = def(c);
  if (['einheit', 'gebaeude', 'wunder'].includes(d.typ) && d.zeitalter > p.alter) return 'Dein Zeitalter ist zu niedrig.';
  const z = zukauf(p, c);
  if (z === null) { const fehl = (d.braucht || []).filter(b => !(symbole(p)[b] >= 1)); return fehl.some(b => b === 'kueste' || b === 'flug') ? 'Es fehlt Küste/Flugfeld.' : 'Es fehlen mindestens 2 Rohstoffe.'; }
  if (p.gold < kostenGesamt(p, c)) return 'Zu wenig Gold (' + kostenGesamt(p, c) + ' nötig).';
  for (const b of (d.benoetigt || [])) if (!p.geb.some(g => g.id === b)) return 'Benötigt: ' + def({ id: b }).name + '.';
  if (d.typ === 'gebaeude' && p.geb.some(g => g.id === c.id)) return 'Du hast dieses Gebäude schon.';
  return null;
}
export function ablegenGold(p, c) { return def(c).relkarte ? 0 : R.ablegen_gold + (p.volk === 'goldener_bund' || effekte(p).ABLEGEN ? 1 : 0) + (p.religion === 'mondgilde' ? 1 : 0); }
export const landErlaubt = (p) => 1 + effekte(p).L;
export const schutzAktiv = (s) => s.ereigZ < R.schutz_runden;

// ---------- Zugablauf ----------
function zugStart(s) {
  const p = s.sp[s.am]; s.phase = 'ziehen';
  for (const u of p.front.concat(p.kaserne)) u.t = 0;
  p.front = p.front.concat(p.kaserne); p.kaserne = [];
  p.hp = Math.min(R.stadt_hp, p.hp + heilung(p));
  const g = einkommen(s, p); p.gold += g;
  log(s, 'zug', p.name + ' ist am Zug (+' + g + ' Gold).', s.am, { gold: g });
  p.landG = 0; p.ablN = 0; p.relBenutzt = false;
  s.zieh = R.ziehen + effekte(p).Z + (p.religion === 'mondgilde' ? 1 : 0);
  ziehCheck(s);
}
function ziehCheck(s) {
  const p = s.sp[s.am];
  const quelle = [1, 2, 3].some(st => st <= maxStapel(p) && (s.stapel[st].length || s.ablage[st].length)) || (p.religion && p.relStapel.length && !p.relBenutzt);
  if (s.zieh <= 0 || !quelle) { s.zieh = 0; s.phase = 'aktion'; }
}
export const maxStapel = (p) => R.stapel_von_zeitalter[p.alter];
function pruefeSieg(s) {
  if (s.sieger !== null) return true;
  for (const p of s.sp) if (!p.tot && p.hp <= 0) { p.tot = true; log(s, 'tot', p.name + ' ist besiegt.', s.sp.indexOf(p)); for (const m of s.missionen.filter(m => s.sp[m.host] === p || s.sp[m.owner] === p)) missionEnde(s, m); }
  const l = lebende(s);
  if (l.length === 1) { s.sieger = s.sp.indexOf(l[0]); s.grund = 'Eroberung'; s.phase = 'ende'; log(s, 'sieg', l[0].name + ' gewinnt durch Eroberung!', s.sieger); return true; }
  const reihe = [s.am, ...s.sp.map((_, i) => i).filter(i => i !== s.am)];
  for (const i of reihe) { const p = s.sp[i]; if (p.tot) continue;
    if (kultur(p) >= R.kultur_sieg) { s.sieger = i; s.grund = 'Kultur'; }
    else if (s.opt.rel && p.religion && glaube(s, p) >= s.glaubeZiel) { s.sieger = i; s.grund = 'Glaube'; }
    if (s.sieger !== null) { s.phase = 'ende'; log(s, 'sieg', p.name + ' gewinnt durch ' + s.grund + '!', i); return true; } }
  return false;
}
function missionEnde(s, m) { s.missionen.splice(s.missionen.indexOf(m), 1); m.c.t = 0; s.sp[m.owner].hand.push(m.c); log(s, 'mission', 'Ein Missionar von ' + s.sp[m.owner].name + ' kehrt heim.', m.owner); }
function schadenStadt(s, o, dmg, quelle) { const d = Math.max(1, dmg - schutz(o)); o.hp -= d; log(s, 'schaden', o.name + ' verliert ' + d + ' Lebenspunkte' + (quelle ? ' (' + quelle + ')' : '') + '.', s.sp.indexOf(o), { d }); return d; }

// ---------- Hauptschnittstelle ----------
export function aktion(s, pi, a) {
  const f = (t) => ({ ok: false, fehler: t });
  if (s.sieger !== null) return f('Das Spiel ist vorbei.');
  const p = s.sp[pi]; if (!p || p.tot) return f('Ungültiger Spieler.');
  if (s.phase === 'block') {
    if (a.t !== 'blocke') return f('Zuerst muss geblockt werden.');
    if (pi !== s.kampf.ziel) return f('Du bist nicht der Verteidiger.');
    return blocke(s, a);
  }
  if (pi !== s.am) return f('Du bist nicht am Zug.');
  if (s.phase === 'ziehen') {
    if (a.t !== 'ziehe') return f('Du musst zuerst Karten ziehen.');
    const st = a.stapel;
    if (st === 'rel') {
      if (!p.religion || !p.relStapel.length || p.relBenutzt) return f('Kein Religionsstapel verfügbar.');
      p.hand.push(p.relStapel.pop()); p.relBenutzt = true;
    } else {
      if (![1, 2, 3].includes(st) || st > maxStapel(p)) return f('Diesen Stapel darfst du noch nicht nutzen.');
      if (!ziehe(s, p, st)) return f('Der Stapel ist leer.');
    }
    s.zieh--; ziehCheck(s);
    return { ok: true };
  }
  const k = p.hand.find(c => c.i === a.c);
  switch (a.t) {
    case 'land': {
      if (!k || def(k).typ !== 'land') return f('Das ist keine Land-Karte.');
      if (p.landG >= landErlaubt(p)) return f('Du hast dein Land für diesen Zug schon gespielt.');
      p.hand.splice(p.hand.indexOf(k), 1); p.land.push(k); p.landG++; log(s, 'land', p.name + ' legt ' + def(k).name + '.', pi, { c: k.id }); return { ok: true };
    }
    case 'spiele': {
      if (!k) return f('Karte nicht auf der Hand.');
      const d = def(k); if (!['einheit', 'gebaeude'].includes(d.typ)) return f('Diese Karte kannst du so nicht spielen.');
      if (d.klasse === 'missionar') return f('Missionare werden mit „Mission“ ausgesandt.');
      const g = sperrGrund(s, p, k); if (g) return f(g);
      p.gold -= kostenGesamt(p, k); p.hand.splice(p.hand.indexOf(k), 1);
      if (d.typ === 'gebaeude') p.geb.push(k);
      else if (d.schluessel.includes('gruenden')) { for (let n = 0; n < 2; n++) { const l = p.hand.find(c => def(c).typ === 'land'); if (l) { p.hand.splice(p.hand.indexOf(l), 1); p.land.push(l); } } legeAb(s, p, k); }
      else { k.t = 0; p.kaserne.push(k); for (let n = 0; n < (d.ziehen || 0); n++) ziehe(s, p, maxStapel(p)); }
      log(s, 'spiele', p.name + ' spielt ' + d.name + '.', pi, { c: k.id }); pruefeSieg(s); return { ok: true };
    }
    case 'wunder': {
      const w = s.wunderOffen.find(x => x.i === a.c); if (!w) return f('Dieses Wunder ist nicht offen.');
      const g = sperrGrund(s, p, w); if (g) return f(g);
      p.gold -= kostenGesamt(p, w); s.wunderOffen.splice(s.wunderOffen.indexOf(w), 1); p.wunder.push(w); wunderNach(s);
      log(s, 'wunder', p.name + ' baut das Wunder ' + def(w).name + '!', pi, { c: w.id }); pruefeSieg(s); return { ok: true };
    }
    case 'aufstieg': {
      const kst = aufstiegKosten(p); if (kst === null) return f('Du bist schon im letzten Zeitalter.'); if (p.gold < kst) return f('Zu wenig Gold.');
      p.gold -= kst; p.alter++; volkskarte(s, p); log(s, 'aufstieg', p.name + ' steigt ins Zeitalter ' + (p.alter + 1) + ' auf.', pi, { alter: p.alter }); return { ok: true };
    }
    case 'tribut': {
      const t = s.auslage.find(x => x.i === a.c); if (!t) return f('Stadtstaat nicht verfügbar.');
      if (p.staaten.length >= 2) return f('Du hast schon 2 Verbündete.'); if (p.gold < def(t).kosten) return f('Zu wenig Gold.');
      p.gold -= def(t).kosten; s.auslage.splice(s.auslage.indexOf(t), 1); p.staaten.push(t); if (s.staatStapel.length) s.auslage.push(s.staatStapel.pop());
      log(s, 'tribut', p.name + ' verbündet sich mit ' + def(t).name + '.', pi, { c: t.id }); pruefeSieg(s); return { ok: true };
    }
    case 'ablegen': {
      if (!k) return f('Karte nicht auf der Hand.'); if (k.vk) return f('Volkskarten kann man nicht ablegen.');
      if (p.ablN >= R.ablegen_max) return f('Du hast schon ' + R.ablegen_max + ' Karten abgelegt.');
      p.hand.splice(p.hand.indexOf(k), 1); const rel = def(k).relkarte; legeAb(s, p, k); p.ablN++;
      const gg = rel ? 0 : ablegenGold(p, k);
      p.gold += gg; log(s, 'ablegen', p.name + ' legt eine Karte ab' + (gg ? ' (+' + gg + ' Gold)' : '') + '.', pi); return { ok: true };
    }
    case 'gruenden': {
      if (!s.opt.rel) return f('Die Erweiterung „Götter & Glaube“ ist nicht aktiv.'); if (p.religion) return f('Du hast schon eine Religion.');
      if (p.alter < 1) return f('Religionen kann man ab Zeitalter II gründen.'); if (p.gold < 5) return f('Zu wenig Gold (5 nötig).');
      if (!s.relFrei.includes(a.rel)) return f('Diese Religion ist nicht frei.');
      const opfer = p.hand.find(c => c.i === a.c); if (!opfer || opfer.vk || def(opfer).relkarte) return f('Wähle eine Handkarte zum Ablegen (keine Volkskarte).');
      p.gold -= 5; p.hand.splice(p.hand.indexOf(opfer), 1); legeAb(s, p, opfer);
      s.relFrei.splice(s.relFrei.indexOf(a.rel), 1); p.religion = a.rel;
      p.relStapel = mische(s, D.relkarten.filter(x => x.religion === a.rel).map(x => neu(s, x.id)));
      p.relStapel = p.relStapel; log(s, 'religion', p.name + ' gründet ' + D.religionen.find(r => r.id === a.rel).name + '!', pi, { rel: a.rel }); pruefeSieg(s); return { ok: true };
    }
    case 'mission': {
      if (!k || def(k).klasse !== 'missionar') return f('Das ist kein Missionar.'); if (!p.religion) return f('Du brauchst eine Religion.');
      const ziel = s.sp[a.ziel]; if (!ziel || ziel === p || ziel.tot) return f('Ungültiges Ziel.');
      if (s.missionen.some(m => m.owner === pi && m.host === a.ziel)) return f('Dort ist schon ein Missionar von dir.');
      if (p.gold < kosten(p, k)) return f('Zu wenig Gold.');
      p.gold -= kosten(p, k); p.hand.splice(p.hand.indexOf(k), 1); s.missionen.push({ c: k, owner: pi, host: a.ziel });
      log(s, 'mission', p.name + ' schickt einen Missionar zu ' + ziel.name + '.', pi); pruefeSieg(s); return { ok: true };
    }
    case 'ausweisen': {
      const m = s.missionen.find(x => x.c.i === a.c && x.host === pi); if (!m) return f('Kein Missionar bei dir.');
      const kst = p.religion === 'flammenorden' ? 1 : 2; if (p.gold < kst) return f('Zu wenig Gold (' + kst + ' nötig).');
      p.gold -= kst; missionEnde(s, m); return { ok: true };
    }
    case 'schuss': return schuss(s, pi, a);
    case 'angriff': return angriff(s, pi, a);
    case 'ende': {
      const zuviel = handZaehlt(p).length - handlimit(p);
      if (zuviel > 0) {
        const ids = a.abwerfen || []; if (ids.length !== zuviel) return f('Du musst ' + zuviel + ' Karte(n) ablegen.');
        for (const id of ids) { const c = p.hand.find(x => x.i === id); if (!c || c.vk) return f('Ungültige Karte zum Ablegen.'); }
        for (const id of ids) { const c = p.hand.find(x => x.i === id); p.hand.splice(p.hand.indexOf(c), 1); legeAb(s, p, c); }
      }
      naechster(s); return { ok: true };
    }
  }
  return f('Unbekannte Aktion.');
}

function naechster(s) {
  if (pruefeSieg(s)) return;
  const n = s.sp.length; let i = s.am, wrap = false;
  do { i = (i + 1) % n; if (i <= s.am) wrap = true; } while (s.sp[i].tot);
  s.am = i;
  if (wrap) { ereignis(s); if (s.sieger !== null) return; s.runde++; if (s.sp[s.am].tot) { do { s.am = (s.am + 1) % n; } while (s.sp[s.am].tot); } }
  zugStart(s);
}

// ---------- Kampf ----------
export function staerkeGegen(p, u, g, angriff) {
  const d = def(u); let st = d.staerke;
  if (angriff && d.schluessel.includes('ansturm')) st += (p.volk === 'steppenreiter' ? 2 : 1) + (p.religion === 'flammenorden' ? 1 : 0);
  if (g) for (const t of def(g).tags) st += (d.boni[t] || 0);
  if (g && d.schluessel.includes('luftabwehr') && def(g).tags.includes('luft')) st += 3;
  if (d.tags.includes('see')) st += effekte(p).SCHIFF;
  return st;
}
export function kannBlocken(b, a) {
  const db = def(b), da = def(a);
  if (b.t || db.staerke < 1 || ZIVIL.includes(db.klasse)) return false;
  if (da.tags.includes('luft') && !(db.tags.includes('luft') || db.schluessel.includes('luftabwehr'))) return false;
  return true;
}
export function kannAngreifen(u) { const d = def(u); return !u.t && d.staerke > 0 && !ZIVIL.includes(d.klasse); }
export function kannSchiessen(u) { const d = def(u); return !u.t && d.fern >= 1 && (d.schluessel.includes('fern') || d.schluessel.includes('belagerung')); }
export function schussZiele(s, p, u) {
  const d = def(u), res = [];
  for (const o of gegner(s, p)) for (const t of kampfEinheiten(o)) {
    const dt = def(t); if (dt.schluessel.includes('tarnung')) continue;
    if (dt.tags.includes('luft') && !(d.tags.includes('luft') || d.schluessel.includes('luftabwehr'))) continue;
    let fe = d.fern; for (const g of dt.tags) fe += (d.boni[g] || 0);
    if (fe >= dt.staerke) res.push({ p: s.sp.indexOf(o), c: t.i });
  }
  return res;
}
function entferne(s, p, u) { let x = p.front.indexOf(u); if (x >= 0) p.front.splice(x, 1); else { x = p.kaserne.indexOf(u); if (x >= 0) p.kaserne.splice(x, 1); } }
function schuss(s, pi, a) {
  const p = s.sp[pi], f = (t) => ({ ok: false, fehler: t });
  if (schutzAktiv(s)) return f('Neulingsschutz: Noch darf niemand angreifen oder schießen.');
  const u = p.front.find(x => x.i === a.c); if (!u || !kannSchiessen(u)) return f('Diese Einheit kann nicht schießen.');
  const d = def(u);
  if (a.stadt) {
    if (!d.schluessel.includes('belagerung')) return f('Nur Belagerer dürfen die Stadt beschießen.');
    const o = s.sp[a.p]; if (!o || o === p || o.tot) return f('Ungültiges Ziel.');
    u.t = 1; schadenStadt(s, o, d.fern + (d.boni.stadt || 0), d.name);
  } else {
    const o = s.sp[a.p]; if (!o || o === p || o.tot) return f('Ungültiges Ziel.');
    const t = einheiten(o).find(x => x.i === a.z); if (!t || !schussZiele(s, p, u).some(z => z.c === t.i)) return f('Das Ziel ist nicht erreichbar.');
    entferne(s, o, t); legeAb(s, o, t); u.t = 1; log(s, 'schuss', d.name + ' von ' + p.name + ' zerstört ' + def(t).name + '.', pi, { c: t.id });
  }
  if (d.schluessel.includes('einmalig')) { entferne(s, p, u); legeAb(s, p, u); }
  pruefeSieg(s); return { ok: true };
}
function angriff(s, pi, a) {
  const p = s.sp[pi], f = (t) => ({ ok: false, fehler: t });
  if (schutzAktiv(s)) return f('Neulingsschutz: Noch darf niemand angreifen oder schießen.');
  const o = s.sp[a.ziel]; if (!o || o === p || o.tot) return f('Ungültiges Ziel.');
  const atk = (a.ids || []).map(id => p.front.find(x => x.i === id));
  if (!atk.length || atk.some(u => !u || !kannAngreifen(u))) return f('Wähle aufrechte Einheiten an der Front.');
  for (const u of atk) u.t = 1;
  s.kampf = { von: pi, ziel: a.ziel, atk: atk.map(u => u.i) }; log(s, 'angriff', p.name + ' greift ' + o.name + ' mit ' + atk.length + ' Einheit(en) an!', pi, { ziel: a.ziel });
  // keine möglichen Blocker → sofort lösen
  const blockerMoeglich = einheiten(o).some(b => atk.some(x => kannBlocken(b, x)));
  if (!blockerMoeglich) return { ok: true, loese: loeseKampf(s, {}) };
  s.phase = 'block'; return { ok: true };
}
function blocke(s, a) {
  const k = s.kampf, o = s.sp[k.ziel], zuordnung = a.z || {}, benutzt = new Set();
  for (const [ai, bi] of Object.entries(zuordnung)) {
    if (bi === null || bi === undefined) continue;
    const at = s.sp[k.von].front.find(x => x.i === +ai) || s.sp[k.von].kaserne.find(x => x.i === +ai); const bl = einheiten(o).find(x => x.i === bi);
    if (!k.atk.includes(+ai) || !at || !bl || benutzt.has(bi) || !kannBlocken(bl, at)) return { ok: false, fehler: 'Ungültige Blockzuordnung.' };
    benutzt.add(bi);
  }
  loeseKampf(s, zuordnung); return { ok: true };
}
function loeseKampf(s, zuordnung) {
  const k = s.kampf, p = s.sp[k.von], o = s.sp[k.ziel]; s.kampf = null; s.phase = 'aktion';
  const res = [];
  for (const id of k.atk) {
    const at = p.front.find(x => x.i === id); if (!at) continue; const da = def(at);
    const bid = zuordnung[id]; const bl = bid ? einheiten(o).find(x => x.i === bid) : null;
    if (bl) {
      const sa = staerkeGegen(p, at, bl, true), sb = staerkeGegen(o, bl, at, false);
      if (sa >= sb) { entferne(s, o, bl); legeAb(s, o, bl); }
      if (sb >= sa) { entferne(s, p, at); legeAb(s, p, at); }
      res.push({ a: at.id, b: bl.id, sa, sb }); log(s, 'duell', def(at).name + ' (' + sa + ') gegen ' + def(bl).name + ' (' + sb + ')' + (sa > sb ? ': Angreifer siegt.' : sa < sb ? ': Verteidiger siegt.' : ': beide fallen.'), k.von, { a: at.id, b: bl.id, sa, sb });
    } else { const dmg = da.staerke + (da.boni.stadt || 0) + (da.schluessel.includes('ramme') ? da.staerke : 0); schadenStadt(s, o, dmg, da.name); res.push({ a: at.id, stadt: dmg }); }
  }
  pruefeSieg(s); return res;
}

// Einfache Kartenbewertung (Winter: schwächste Karte wird abgelegt)
export function kartenWert(p, c) {
  const d = def(c); if (d.typ === 'land') return p.land.length < 8 ? 5 : 1;
  if (d.zeitalter > p.alter + 1) return 0.5; return 2 + (d.typ === 'einheit' ? 3 : 2);
}

// ---------- Ereignisse ----------
function ereignis(s) {
  if (!s.ereig.length) s.ereig = mische(s, s.ereigAblage.splice(0));
  if (!s.ereig.length) return;
  const c = s.ereig.pop(); s.ereigAblage.push(c); s.ereigZ++; const e = def(c), l = lebende(s);
  s.letztes = { id: e.id, n: s.seq + 1 };
  log(s, 'ereignis', 'Ereignis: ' + e.name, null, { c: e.id });
  const nm = (p) => s.sp.indexOf(p);
  if (e.art === 'rel') {
    const mit = l.filter(p => p.religion);
    if (e.id === 'pilgerzug') for (const p of mit) p.gold += Math.max(1, Math.floor(glaube(s, p) / 3));
    else if ((e.id === 'prophezeiung' || e.id === 'glaubenskrieg') && mit.length) {
      const m = Math.max(...mit.map(p => glaube(s, p))); const t = mit.filter(p => glaube(s, p) === m);
      if (t.length === 1) { if (e.id === 'prophezeiung') for (let n = 0; n < 2; n++) ziehe(s, t[0], maxStapel(t[0])); else t[0].gold = Math.max(0, t[0].gold - 3); }
    } else if (e.id === 'ketzerjagd') for (const m of s.missionen.slice()) missionEnde(s, m);
    else if (e.id === 'fest') for (const p of l) { if (p.religion) p.gold += 2; else ziehe(s, p, maxStapel(p)); }
    else if (e.id === 'heilung') for (const p of l) p.hp = Math.min(R.stadt_hp, p.hp + 3);
  } else if (e.art === 'barbaren') {
    const m = Math.min(...l.map(p => kampfEinheiten(p).length));
    for (const p of l.filter(p => kampfEinheiten(p).length === m)) {
      const B = p.alter + 1 + e.plus, bl = kampfEinheiten(p).sort((a, b) => def(a).staerke - def(b).staerke);
      if (bl.length) {
        const gut = bl.find(u => def(u).staerke >= B);
        if (gut) { p.gold += e.beute; log(s, 'barb', p.name + ' wehrt die Barbaren ab (+' + e.beute + ' Gold).', nm(p)); }
        else { const u = bl[0]; entferne(s, p, u); legeAb(s, p, u); log(s, 'barb', 'Die Barbaren besiegen ' + def(u).name + ' von ' + p.name + '.', nm(p)); }
      } else { if (e.folge === 'stadt') schadenStadt(s, p, B, 'Barbaren'); else { p.gold = Math.max(0, p.gold - B); log(s, 'barb', p.name + ' verliert ' + B + ' Gold an die Barbaren.', nm(p)); } }
    }
  } else {
    if (e.id === 'regenzeit') for (const p of l) p.gold += 2;
    else if (e.id === 'winter') for (const p of l) { const z = handZaehlt(p); if (z.length) { const c = z.reduce((m, x) => kartenWert(p, x) < kartenWert(p, m) ? x : m); p.hand.splice(p.hand.indexOf(c), 1); legeAb(s, p, c); log(s, 'winter', p.name + ' legt im Winter eine Karte ab.', nm(p)); } }
    else if (e.id === 'seuche') for (const p of l) { if (heilung(p) < 2) p.hp -= 2; }
    else if (e.id === 'sonnenwende') { const m = Math.max(...l.map(kultur)); const t = l.filter(p => kultur(p) === m); if (t.length === 1) t[0].gold += 2; }
    else if (e.id === 'diebe') { const m = Math.max(...l.map(p => p.gold)); for (const p of l.filter(p => p.gold === m)) p.gold = Math.max(0, p.gold - 3); }
    else if (e.id === 'messe') for (const p of l) ziehe(s, p, maxStapel(p));
  }
  pruefeSieg(s);
}

// ---------- Sicht eines Spielers (für Online: verborgene Infos entfernen) ----------
export function sicht(s, me) {
  const c = JSON.parse(JSON.stringify(s)); c.rng = 0;
  for (const k of [1, 2, 3]) { c.stapel[k] = new Array(c.stapel[k].length).fill(0); c.ablage[k] = new Array(c.ablage[k].length).fill(0); }
  c.wunderStapel = new Array(c.wunderStapel.length).fill(0); c.staatStapel = new Array(c.staatStapel.length).fill(0);
  c.ereig = new Array(c.ereig.length).fill(0); c.ereigAblage = c.ereigAblage.map(x => x);
  c.sp.forEach((p, i) => { if (i !== me) { p.hand = p.hand.map(() => ({ i: 0, id: '?' })); p.relStapel = new Array(p.relStapel.length).fill(0); } });
  return c;
}
