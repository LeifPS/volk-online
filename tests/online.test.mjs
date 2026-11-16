// Integrationstest gegen einen laufenden Worker (npx wrangler dev --port 8788): 2 Menschen + Computer spielen eine ganze Partie.
import fs from 'node:fs';
import * as E from '../public/js/engine.js';
import * as K from '../public/js/ki.js';
E.setzeDaten(JSON.parse(fs.readFileSync(new URL('../public/data/satz.json', import.meta.url))));
const BASIS = process.argv[2] || 'localhost:8788';
const tok = () => 'tok' + Math.random().toString(36).slice(2, 14);
class Klient {
  constructor(code, name, erstelle, cfg) { this.code = code; this.name = name; this.token = tok(); this.erstelle = erstelle; this.cfg = cfg; this.n = 0; this.wait = new Map(); this.lobby = null; this.s = null; this.me = -1; this.fehler = []; this.bereit = new Promise(r => this.r = r); }
  verbinde() { this.ws = new WebSocket(`ws://${BASIS}/ws/raum/${this.code}`); this.ws.onopen = () => this.ws.send(JSON.stringify({ t: 'hallo', token: this.token, name: this.name, erstelle: this.erstelle, cfg: this.cfg, code: this.code })); this.ws.onmessage = (e) => this.nach(JSON.parse(e.data)); return this.bereit; }
  nach(m) { if (m.t === 'lobby') { this.lobby = m; this.r(); } else if (m.t === 'zustand') { this.s = m.s; this.me = m.me; this.phase = m.phase; this.r(); this.handeln(); } else if (m.t === 'ergebnis') { this.wait.get(m.id)?.(m); this.wait.delete(m.id); } else if (m.t === 'fehler') { this.fehler.push(m.text); this.r(); } }
  senden(o) { this.ws.send(JSON.stringify(o)); }
  aktion(a) { return new Promise(res => { const id = ++this.n; this.wait.set(id, res); this.senden({ t: 'a', id, a }); }); }
  async handeln() {
    if (this.busy || !this.s || this.s.sieger !== null) return; const s = this.s, actor = E.akteur(s); if (actor !== this.me) return;
    this.busy = true; await new Promise(r => setTimeout(r, 5));
    try { const a = K.waehle(this.s, this.me, 'mittel'); const r = await this.aktion(a); if (!r.ok) this.fehler.push('Aktion abgelehnt: ' + JSON.stringify(a) + ' ' + r.fehler); } finally { this.busy = false; }
    setTimeout(() => this.handeln(), 5);
  }
}
const code = 'T' + Math.random().toString(36).slice(2, 6).toUpperCase();
const a = new Klient(code, 'Anna', true, { max: 4, vk: true, rel: true }); await a.verbinde();
const b = new Klient(code, 'Ben', false); await b.verbinde();
console.log('Lobby:', a.lobby.code, b.lobby.sitze.map(x => x.name));
a.senden({ t: 'ki', stufe: 'mittel' }); a.senden({ t: 'ki', stufe: 'stark' }); await new Promise(r => setTimeout(r, 300));
const c = new Klient(code, 'Cleo', false); await c.verbinde(); console.log('Voll-Fehler:', c.fehler);
a.senden({ t: 'start' });
const t0 = Date.now();
while (!(a.s && a.s.sieger !== null) && Date.now() - t0 < 170000) await new Promise(r => setTimeout(r, 500));
console.log('Ende:', a.s?.sieger, a.s?.grund, 'Runde', a.s?.runde, 'Dauer s', Math.round((Date.now() - t0) / 1000));
console.log('Sicht Anna fremde Hand verborgen:', a.s.sp[1].hand.every(h => h.id === '?'), '| eigene sichtbar:', a.s.sp[0].hand.every(h => h.id !== '?'));
console.log('Fehler:', a.fehler, b.fehler);
process.exit(0);
