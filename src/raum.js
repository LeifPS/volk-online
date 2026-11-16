// Ein Spielraum = ein Durable Object. Hält Lobby, Spielzustand (maßgeblich!) und die Computer-Spieler.
import { DurableObject } from 'cloudflare:workers';
import * as E from '../public/js/engine.js';
import * as KI from '../public/js/ki.js';
import satz from '../public/data/satz.json';
E.setzeDaten(satz);

const ABWESEND_MS = 40_000;      // Mensch ist getrennt → Computer vertritt ihn
const BLOCK_MS = 90_000;         // Verteidiger antwortet nicht → automatischer Block
const AUFRAEUMEN_MS = 6 * 3600_000;
const SCHNELL_WARTEN_MS = 20_000;
const san = (t, n = 16) => String(t ?? '').replace(/[<>&"]/g, '').trim().slice(0, n);

export class Raum extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env); this.env = env; this.socks = new Map(); this.d = null; this.timer = null; this.warteSeit = null;
    ctx.blockConcurrencyWhile(async () => { this.d = (await ctx.storage.get('d')) || null; if (this.d && this.d.phase === 'spiel') this.takt(); });
  }
  async speichern() { await this.ctx.storage.put('d', this.d); await this.ctx.storage.setAlarm(Date.now() + AUFRAEUMEN_MS); }
  async alarm() { if (!this.socks.size) { await this.ctx.storage.deleteAll(); this.d = null; } else await this.ctx.storage.setAlarm(Date.now() + AUFRAEUMEN_MS); }

  async fetch(request) {
    const pair = new WebSocketPair(); const [client, server] = Object.values(pair); server.accept();
    const info = { token: null, idx: -1 }; this.socks.set(server, info);
    server.addEventListener('message', (e) => this.nachricht(server, info, e.data).catch(err => { console.error(err); this.senden(server, { t: 'fehler', text: 'Serverfehler.' }); }));
    const zu = () => { this.socks.delete(server); if (info.token && this.d) { const st = this.d.sitze.find(x => x.token === info.token); if (st && !this.verbunden(st.token)) st.weg = Date.now(); this.lobbyUpdate(); this.alleSenden(); } };
    server.addEventListener('close', zu); server.addEventListener('error', zu);
    return new Response(null, { status: 101, webSocket: client });
  }
  verbunden(token) { for (const i of this.socks.values()) if (i.token === token) return true; return false; }
  senden(ws, o) { try { ws.send(JSON.stringify(o)); } catch { } }

  // ----- Nachrichten
  async nachricht(ws, info, roh) {
    let m; try { m = JSON.parse(roh); } catch { return; }
    if (m.t === 'ping') return this.senden(ws, { t: 'pong' });
    if (m.t === 'hallo') return this.hallo(ws, info, m);
    if (!info.token || !this.d) return this.senden(ws, { t: 'fehler', text: 'Nicht verbunden.' });
    const d = this.d, idx = d.sitze.findIndex(x => x.token === info.token), host = idx === 0;
    switch (m.t) {
      case 'volk': { if (d.phase !== 'lobby') return; const v = m.volk && satz.voelker.some(x => x.id === m.volk) ? m.volk : ''; if (v && d.sitze.some((x, i) => i !== idx && x.volk === v)) return this.senden(ws, { t: 'fehler', text: 'Dieses Volk ist schon vergeben.' }); d.sitze[idx].volk = v; break; }
      case 'name': d.sitze[idx].name = san(m.name) || d.sitze[idx].name; break;
      case 'einst': {
        if (!host || d.phase !== 'lobby' || d.schnell) return; if (m.opt) d.opt = { vk: !!m.opt.vk, rel: !!m.opt.rel, civ: !!m.opt.civ };
        if (m.max) d.max = Math.max(d.sitze.length, Math.min(4, Math.max(2, +m.max | 0))); break;
      }
      case 'ki': { if (!host || d.phase !== 'lobby' || d.schnell || d.sitze.length >= d.max) return; const stufe = ['leicht', 'mittel', 'stark'].includes(m.stufe) ? m.stufe : 'mittel'; d.sitze.push({ token: null, name: 'Computer', volk: '', ki: stufe, weg: 0 }); break; }
      case 'kiweg': { if (!host || d.phase !== 'lobby') return; const i = +m.i; if (d.sitze[i] && d.sitze[i].ki) d.sitze.splice(i, 1); break; }
      case 'raus': { if (!host || d.phase !== 'lobby') return; const i = +m.i; if (i > 0 && d.sitze[i]) { const tk = d.sitze[i].token; d.sitze.splice(i, 1); for (const [w, inf] of this.socks) if (inf.token === tk && tk) { this.senden(w, { t: 'fehler', text: 'Du wurdest aus dem Raum entfernt.', raus: true }); inf.token = null; } } break; }
      case 'start': { if (!host || d.phase !== 'lobby') return; if (d.sitze.length < 2) return this.senden(ws, { t: 'fehler', text: 'Mindestens 2 Spieler nötig (Computer zählen mit).' }); this.starten(); break; }
      case 'revanche': { if (!host || d.phase !== 'ende') return; d.phase = 'lobby'; d.s = null; d.sitze = d.sitze.filter(x => !x.ki || true); break; }
      case 'a': {
        if (d.phase !== 'spiel' || idx < 0) return; const s = d.s; const actor = E.akteur(s);
        const r = E.aktion(s, idx, m.a || {}); this.senden(ws, { t: 'ergebnis', id: m.id, ok: r.ok, fehler: r.fehler, loese: r.loese });
        if (!r.ok) return; this.nachAktion(); return;
      }
      default: return;
    }
    await this.speichern(); this.lobbyUpdate(); this.alleSenden();
  }
  async hallo(ws, info, m) {
    const token = san(m.token, 40); if (token.length < 8) return this.senden(ws, { t: 'fehler', text: 'Ungültige Kennung.' });
    const name = san(m.name) || 'Spieler';
    if (!this.d) {
      if (!m.erstelle) return this.senden(ws, { t: 'fehler', text: 'Diesen Raum gibt es nicht.', weg: true });
      const c = m.cfg || {}; this.d = { phase: 'lobby', opt: { vk: !!c.vk, rel: !!c.rel, civ: !!c.civ }, max: [2, 3, 4].includes(+c.max) ? +c.max : 4, schnell: !!c.schnell, sitze: [], s: null, startAt: 0, code: san(m.code, 8).toUpperCase() };
    } else if (m.erstelle && !this.d.sitze.some(x => x.token === token)) return this.senden(ws, { t: 'fehler', text: 'Code schon belegt.', belegt: true });
    const d = this.d; let st = d.sitze.find(x => x.token === token);
    if (!st) {
      if (d.phase !== 'lobby') return this.senden(ws, { t: 'fehler', text: 'Dieses Spiel läuft schon.', weg: true });
      if (d.sitze.length >= d.max) return this.senden(ws, { t: 'fehler', text: 'Der Raum ist voll.', weg: true });
      st = { token, name, volk: '', ki: null, weg: 0 }; d.sitze.push(st);
      if (d.schnell && d.sitze.length >= 2 && !d.startAt) d.startAt = Date.now() + SCHNELL_WARTEN_MS;
    } else { st.name = name || st.name; st.weg = 0; }
    info.token = token; info.idx = d.sitze.indexOf(st);
    await this.speichern(); this.lobbyUpdate(); this.alleSenden(); this.takt();
  }

  // ----- Spiel
  starten() {
    const d = this.d; const liste = d.sitze.map((x, i) => ({ name: x.ki ? '' : x.name, volk: x.volk || undefined, ki: x.ki || null }));
    const s = E.neuesSpiel(liste, d.opt);
    s.sp.forEach((p, i) => { const st = d.sitze[i]; if (st.ki) { const v = satz.voelker.find(x => x.id === p.volk); p.name = v.herrscher.split(' ').slice(0, 2).join(' '); p.ki = st.ki; } p.volk && (st.volk = p.volk); });
    d.s = s; d.phase = 'spiel'; d.startAt = 0; this.lobbyUpdate(false); this.takt();
  }
  nachAktion() {
    const d = this.d; if (d.s.sieger !== null) d.phase = 'ende';
    this.speichern(); this.alleSenden(); this.takt();
  }
  takt() {
    if (this.timer || !this.d) return; this.timer = setTimeout(() => { this.timer = null; this.tick().catch(e => console.error(e)); }, 800);
  }
  async tick() {
    const d = this.d; if (!d) return; const jetzt = Date.now();
    if (d.phase === 'lobby') {
      if (d.schnell && d.sitze.length >= 2 && d.startAt && jetzt >= d.startAt - (d.sitze.length >= d.max ? SCHNELL_WARTEN_MS - 3000 : 0)) {
        while (d.sitze.length < d.max) d.sitze.push({ token: null, name: 'Computer', volk: '', ki: 'mittel', weg: 0 });
        this.starten(); await this.speichern(); this.alleSenden(); return;
      }
      if (d.schnell && d.sitze.length >= 2) { this.alleSenden(); this.takt(); } return;
    }
    if (d.phase !== 'spiel') return; const s = d.s; if (s.sieger !== null) { d.phase = 'ende'; await this.speichern(); this.alleSenden(); return; }
    const actor = E.akteur(s), st = d.sitze[actor];
    const mensch = !st.ki; const abwesend = mensch && (!this.verbunden(st.token) && jetzt - (st.weg || jetzt) > ABWESEND_MS);
    const key = actor + ':' + s.seq; if (!this.warteSeit || this.warteSeit.key !== key) this.warteSeit = { key, t: jetzt };
    const blockZeit = mensch && (s.phase === 'block' || s.phase === 'wahl') && jetzt - this.warteSeit.t > BLOCK_MS;
    if (st.ki || abwesend || blockZeit) {
      const stufe = st.ki || 'mittel'; const a = KI.waehle(s, actor, stufe); let r = E.aktion(s, actor, a);
      if (!r.ok) { console.warn('KI-Fehler', JSON.stringify(a), r.fehler); r = E.aktion(s, actor, s.phase === 'block' ? { t: 'blocke', z: {} } : s.phase === 'wahl' ? E.wahlStandard(s, actor) : s.phase === 'ziehen' ? { t: 'ziehe', stapel: 1 } : { t: 'ende', abwerfen: E.handZaehlt(s.sp[actor]).slice(0, Math.max(0, E.handZaehlt(s.sp[actor]).length - E.handlimit(s.sp[actor]))).map(c => c.i) }); if (!r.ok) E.aktion(s, actor, { t: 'ende' }); }
      await this.speichern(); this.alleSenden();
      this.timer = setTimeout(() => { this.timer = null; this.tick().catch(e => console.error(e)); }, a.t === 'ziehe' ? 350 : a.t === 'angriff' || a.t === 'schuss' || a.t === 'blocke' || a.t === 'abwehr' ? 1300 : a.t === 'ende' ? 900 : 650);
    } else this.timer = setTimeout(() => { this.timer = null; this.tick().catch(e => console.error(e)); }, 2000);
  }

  // ----- Ausgabe
  lobbyDaten(info) {
    const d = this.d, jetzt = Date.now();
    return { t: 'lobby', code: d.code, ich: info.idx, host: info.idx === 0, opt: d.opt, max: d.max, schnell: d.schnell, startIn: d.startAt ? Math.max(0, Math.ceil((d.startAt - jetzt) / 1000)) : null, glaubeZiel: d.opt.vk ? satz.glaube_sieg_vk : satz.glaube_sieg, sitze: d.sitze.map((x, i) => ({ name: x.name, volk: x.volk, ki: x.ki, verbunden: !!x.ki || this.verbunden(x.token) })) };
  }
  alleSenden() {
    if (!this.d) return;
    for (const [ws, info] of this.socks) {
      if (!info.token) continue; info.idx = this.d.sitze.findIndex(x => x.token === info.token); if (info.idx < 0) continue;
      if (this.d.phase === 'lobby') this.senden(ws, this.lobbyDaten(info));
      else this.senden(ws, { t: 'zustand', me: info.idx, s: E.sicht(this.d.s, info.idx), phase: this.d.phase, host: info.idx === 0, sitze: this.d.sitze.map(x => ({ name: x.name, ki: x.ki, verbunden: !!x.ki || this.verbunden(x.token) })) });
    }
  }
  async lobbyUpdate(offen) {
    const d = this.d; if (!d || !d.schnell) return;
    try { await this.env.LOBBY.get(this.env.LOBBY.idFromName('haupt')).fetch(new Request('https://lobby/update', { method: 'POST', body: JSON.stringify({ code: d.code, n: d.sitze.length, offen: offen !== false && d.phase === 'lobby' && d.sitze.length < d.max }) })); } catch { }
  }
}
