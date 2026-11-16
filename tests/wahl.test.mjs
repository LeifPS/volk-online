// Prüft die Entscheidungen bei Ereignissen: Barbarenabwehr (nur aufrechte Einheiten, auch ablehnen) und Winter (Karte selbst wählen)
import fs from 'node:fs';
import * as E from '../public/js/engine.js';
E.setzeDaten(JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))));
let fehler = 0; const ok = (c, t) => { if (!c) { fehler++; console.log('FEHLER:', t); } };
const D = JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url)));

function spiel() {
  const s = E.neuesSpiel([{ name: 'A' }, { name: 'B', ki: 'mittel' }], {});
  return s;
}
// Zug beenden, bis der Ereignisschritt kommt: Ereigniskarte vorher oben auf den Stapel legen
function bisEreignis(s, id) {
  const idx = s.ereig.findIndex(c => c.id === id) >= 0 ? s.ereig.findIndex(c => c.id === id) : -1;
  if (idx < 0) { const k = s.ereigAblage.findIndex(c => c.id === id); const c = s.ereigAblage.splice(k, 1)[0]; s.ereig.push(c); }
  else { const c = s.ereig.splice(idx, 1)[0]; s.ereig.push(c); }
  let n = 0; const z0 = s.ereigZ;
  while (s.phase !== 'wahl' && s.ereigZ === z0 && s.sieger === null && n++ < 40) {
    const pi = E.akteur(s);
    if (s.phase === 'ziehen') E.aktion(s, pi, { t: 'ziehe', stapel: 1 }); else E.aktion(s, pi, { t: 'ende', abwerfen: E.handZaehlt(s.sp[pi]).slice(0, Math.max(0, E.handZaehlt(s.sp[pi]).length - E.handlimit(s.sp[pi]))).map(c => c.i) });
  }
}
// --- Winter
{
  const s = spiel(); s.sp.forEach(p => { p.hand.length = 0; });
  for (const p of s.sp) for (let i = 0; i < 3; i++) p.hand.push({ i: s.nid++, id: s.stapel[1][0].id });
  // Hand wird beim Ziehen größer; Ereignis kommt nach Spieler 2
  bisEreignis(s, 'winter');
  ok(s.phase === 'wahl' && s.wahl.art === 'winter', 'Winter: Phase wahl erwartet, ist ' + s.phase);
  if (s.phase === 'wahl') {
    const q0 = s.wahl.q.slice(), n = q0.length; ok(n >= 1, 'Winter: mindestens ein Betroffener');
    const pi = E.akteur(s), p = s.sp[pi], vorher = E.handZaehlt(p).length;
    ok(!E.aktion(s, 1 - pi, { t: 'winterab', c: E.handZaehlt(p)[0].i }).ok || n > 1 && false, 'Winter: falscher Spieler darf nicht');
    ok(!E.aktion(s, pi, { t: 'winterab', c: 999999 }).ok, 'Winter: ungültige Karte abgelehnt');
    ok(!E.aktion(s, pi, { t: 'ende' }).ok, 'Winter: andere Aktion abgelehnt');
    const wahlK = E.handZaehlt(p)[1].i; const r = E.aktion(s, pi, { t: 'winterab', c: wahlK }); ok(r.ok, 'Winter: Wahl ok');
    ok(E.handZaehlt(p).length === vorher - 1 && !p.hand.some(c => c.i === wahlK), 'Winter: gewählte Karte abgelegt');
    let g = 0; while (s.phase === 'wahl' && g++ < 5) { const a = E.akteur(s); E.aktion(s, a, E.wahlStandard(s, a)); }
    ok(s.phase === 'ziehen', 'Winter: danach geht das Spiel weiter (Phase ' + s.phase + ')');
  }
}
// --- Barbaren
for (const [id, tapp] of [['steppennomaden', false], ['bergclan', true], ['bergclan', false]]) {
  const s = spiel();
  // Spieler 0 hat 1 starke und 1 schwache Einheit, Spieler 1 hat mehr Einheiten (soll nicht betroffen sein)
  const mk = (kid) => ({ i: s.nid++, id: kid, t: 0 });
  const stark = D.karten.filter(k => k.typ === 'einheit' && k.staerke >= 4 && !(k.klasse === 'zivil'))[0], schwach = D.karten.find(k => k.typ === 'einheit' && k.staerke === 1 && k.klasse !== 'zivil');
  const a = s.sp[0]; a.front.push(mk(schwach.id)); a.front.push(mk(stark.id));
  const b = s.sp[1]; for (let i = 0; i < 4; i++) b.front.push(mk(schwach.id));
  if (tapp) a.front.forEach(u => { u.t = 1; });
  const gold0 = a.gold, hp0 = a.hp;
  bisEreignis(s, id);
  const e = D.ereignisse.find(x => x.id === id);
  if (tapp) { // alle getappt: keine Entscheidung, Folge sofort
    ok(s.phase !== 'wahl' || s.wahl.q[0] !== 0, id + ' (getappt): keine Wahl für Spieler 0');
    ok(a.front.length === 2, id + ' (getappt): Einheiten bleiben (kein Weakest-Kill)');
    continue;
  }
  ok(s.phase === 'wahl' && s.wahl.art === 'barb' && s.wahl.q[0] === 0, id + ': Spieler 0 soll entscheiden (Phase ' + s.phase + ')');
  if (s.phase !== 'wahl') continue;
  const B = E.barbStaerke(a, e);
  ok(!E.aktion(s, 0, { t: 'abwehr', u: 999999 }).ok, id + ': ungültige Einheit abgelehnt');
  // Ablehnen: Folge
  const s2 = JSON.parse(JSON.stringify(s)); const a2 = s2.sp[0];
  ok(E.aktion(s2, 0, { t: 'abwehr', u: null }).ok, id + ': ablehnen ok');
  if (e.folge === 'stadt') ok(a2.hp < hp0 || E.schutz(a2) >= B, id + ': Stadt nimmt Schaden'); else ok(a2.gold < gold0 || gold0 === 0, id + ': Gold weg');
  ok(a2.front.length === 2, id + ': Einheiten bleiben beim Ablehnen');
  // Schwache Einheit schicken: geht verloren (wenn B > ihre Stärke)
  const s3 = JSON.parse(JSON.stringify(s)); const a3 = s3.sp[0]; const sw = a3.front[0];
  ok(E.aktion(s3, 0, { t: 'abwehr', u: sw.i }).ok, id + ': schwach abwehren ok');
  ok(!a3.front.some(u => u.i === sw.i) && a3.hp === hp0, id + ': schwache Einheit verloren, Stadt unversehrt');
  // Starke Einheit schicken: Beute
  const a4 = s.sp[0], st = a4.front[1];
  ok(E.aktion(s, 0, { t: 'abwehr', u: st.i }).ok, id + ': stark abwehren ok');
  const gewinn = E.staerkeGegen(a4, st, null, false) >= B;
  ok(gewinn ? a4.gold >= gold0 + e.beute : true, id + ': Beute bei Sieg');
  ok(a4.front.some(u => u.i === st.i) === gewinn, id + ': Einheit ' + (gewinn ? 'bleibt' : 'geht verloren'));
  ok(s.phase === 'ziehen' || s.phase === 'wahl', id + ': Phase danach ' + s.phase);
}
console.log(fehler ? `${fehler} Fehler` : 'Alle Entscheidungstests bestanden');
process.exit(fehler ? 1 : 0);
