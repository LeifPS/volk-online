// Start, Menü, Spieleinstellungen, lokaler Spielverlauf gegen den Computer.
import * as E from './engine.js';
import * as KI from './ki.js';
import { ladeSprites, spr } from './sprites.js';
import { Spieltisch } from './ui.js';
import { regelnSeite } from './regeln.js';
const app = document.getElementById('app'), overlay = document.getElementById('overlay');
let D = null, tisch = null, ctrl = null;
const esc = (t) => String(t ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const ls = { get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { } }, del(k) { try { localStorage.removeItem(k); } catch { } } };

async function start() {
  const [satz] = await Promise.all([fetch('data/satz.json').then(r => r.json()), ladeSprites()]);
  D = satz; E.setzeDaten(D); menue();
  const raum = new URLSearchParams(location.search).get('raum'); if (raum) { history.replaceState(null, '', location.pathname); import('./online.js').then(m => m.onlineMenue(app, D, menue, starteOnline, raum.toUpperCase())); }
}

// ---------------------------------------------------------------- Menü
function menue() {
  overlay.classList.remove('an'); overlay.innerHTML = ''; ctrl?.stop(); ctrl = null; tisch = null;
  const save = ls.get('volk.save', null), weiter = save && save.s && save.s.sieger === null;
  const helden = D.voelker.map(v => spr('stadt:stadtstaat', v.farbe, 1)).join('');
  app.innerHTML = `<div class="menue"><h1>VOLK</h1><div class="unter">Das Kartenspiel – baue dein Volk, steige durch die Zeitalter auf</div>
    <div class="hero">${helden}</div>
    <div class="btns">
      ${weiter ? `<button class="gruen" id="b-weiter">▶ Weiterspielen <small>(Runde ${save.s.runde})</small></button>` : ''}
      <button id="b-ki">🤖 Gegen den Computer</button>
      <button id="b-on" class="sek">🌐 Online spielen</button>
      <button id="b-regeln" class="sek">📜 Regeln & Karten</button>
    </div>
    <div class="fuss">Grundspiel · Erweiterung 1: Volkskarten · Erweiterung 2: Götter & Glaube</div></div>`;
  document.getElementById('b-ki').onclick = setup;
  document.getElementById('b-regeln').onclick = () => regelnSeite(app, D, menue);
  document.getElementById('b-on').onclick = () => import('./online.js').then(m => m.onlineMenue(app, D, menue, starteOnline));
  if (weiter) document.getElementById('b-weiter').onclick = () => starteLokal(save.cfg, save.s);
}

// ---------------------------------------------------------------- Einstellungen
function setup() {
  const c = Object.assign({ name: 'Spieler', gegner: 2, volk: ['', '', '', ''], stufe: ['mittel', 'mittel', 'mittel'], vk: false, rel: false }, ls.get('volk.setup', {}));
  const zeichne = () => {
    const vopt = (sel) => `<option value="">Zufällig</option>${D.voelker.map(v => `<option value="${v.id}" ${sel === v.id ? 'selected' : ''}>${esc(v.name)}</option>`).join('')}`;
    const sitze = Array.from({ length: c.gegner }, (_, i) => `<div class="sitz"><b>Gegner ${i + 1}</b><select data-k="volk" data-i="${i + 1}">${vopt(c.volk[i + 1])}</select><select data-k="stufe" data-i="${i}">${['leicht', 'mittel', 'stark'].map(st => `<option value="${st}" ${c.stufe[i] === st ? 'selected' : ''}>${KI.STUFEN[st].name}</option>`).join('')}</select></div>`).join('');
    app.innerHTML = `<div class="menue"><h2 style="color:#fff">Spiel einrichten</h2>
      <div class="karte-panel"><div class="zeile"><label>Dein Name</label><input type="text" id="s-name" maxlength="16" value="${esc(c.name)}"></div>
        <div class="zeile"><label>Dein Volk</label><select data-k="volk" data-i="0">${vopt(c.volk[0])}</select></div>
        <div class="zeile"><label>Gegner</label><div class="chips">${[1, 2, 3].map(n => `<span class="chipb ${c.gegner === n ? 'an' : ''}" data-g="${n}">${n}</span>`).join('')}</div></div>
        ${sitze}</div>
      <div class="karte-panel"><h3>Spielmodule</h3>
        <div class="modul fest an"><span class="haken">✓</span><div><b>Grundspiel</b><small>Land, Gebäude, Einheiten, Wunder, Stadtstaaten und Ereignisse. Sieg durch Eroberung oder Kultur (16).</small></div></div>
        <div class="modul ${c.vk ? 'an' : ''}" data-m="vk"><span class="haken">${c.vk ? '✓' : ''}</span><div><b>Erweiterung 1: Volkskarten</b><small>Jedes Volk hat 7 eigene Karten – eine für jedes Zeitalter.</small></div></div>
        <div class="modul ${c.rel ? 'an' : ''}" data-m="rel"><span class="haken">${c.rel ? '✓' : ''}</span><div><b>Erweiterung 2: Götter & Glaube</b><small>Gründe eine von 8 Religionen, sende Missionare, gewinne durch Glaube (${c.vk ? D.glaube_sieg_vk : D.glaube_sieg}).</small></div></div></div>
      <div class="btns"><button id="s-los">Spiel starten</button><button class="sek" id="s-zu">Zurück</button></div></div>`;
    app.querySelectorAll('[data-g]').forEach(e => e.onclick = () => { c.gegner = +e.dataset.g; zeichne(); });
    app.querySelectorAll('[data-m]').forEach(e => e.onclick = () => { c[e.dataset.m] = !c[e.dataset.m]; zeichne(); });
    app.querySelectorAll('select').forEach(e => e.onchange = () => { const i = +e.dataset.i; if (e.dataset.k === 'volk') c.volk[i] = e.value; else c.stufe[i] = e.value; });
    app.querySelector('#s-name').oninput = (e) => c.name = e.target.value;
    document.getElementById('s-zu').onclick = menue;
    document.getElementById('s-los').onclick = () => { c.name = (c.name || 'Spieler').trim() || 'Spieler'; ls.set('volk.setup', c); starteLokal(c); };
  };
  zeichne();
}

// ---------------------------------------------------------------- Lokales Spiel
function starteLokal(cfg, gespeichert) {
  let s = gespeichert;
  if (!s) {
    const sp = [{ name: cfg.name, volk: cfg.volk[0] || undefined }];
    for (let i = 0; i < cfg.gegner; i++) sp.push({ name: 'Computer ' + (i + 1), volk: cfg.volk[i + 1] || undefined, ki: cfg.stufe[i] });
    s = E.neuesSpiel(sp, { vk: cfg.vk, rel: cfg.rel });
    s.sp.forEach((p, i) => { if (i > 0) { const v = D.voelker.find(x => x.id === p.volk); p.name = v.herrscher.split(' ').slice(0, 2).join(' ') + ' 🤖'; p.name = p.name.replace(' 🤖', ''); } });
  }
  ctrl = new LokalCtrl(s, cfg); tisch = new Spieltisch(app, overlay, ctrl); ctrl.view = tisch;
  tisch.ereigGesehen = s.letztes ? s.letztes.n : 0;
  tisch.render(); ctrl.weiter();
}
class LokalCtrl {
  constructor(s, cfg) { this.s = s; this.cfg = cfg; this.me = 0; this.t = null; }
  stop() { clearTimeout(this.t); this.gestoppt = true; }
  speichern() { ls.set('volk.save', { cfg: this.cfg, s: this.s }); }
  async send(a) {
    const r = E.aktion(this.s, this.me, a); if (r.ok) { this.speichern(); this.view.render(); this.weiter(); } return r;
  }
  weiter(ms = 420) { clearTimeout(this.t); this.t = setTimeout(() => this.tick(), ms); }
  tick() {
    const s = this.s; if (this.gestoppt || s.sieger !== null) { if (s.sieger !== null) { this.speichern(); this.view.render(); } return; }
    const actor = s.phase === 'block' ? s.kampf.ziel : s.am; if (actor === this.me) return;
    if (this.view.erzwungen()) { this.weiter(300); return; }
    const stufe = s.sp[actor].ki || 'mittel';
    let a = KI.waehle(s, actor, stufe), r = E.aktion(s, actor, a);
    if (!r.ok) { console.warn('KI-Fehler', a, r.fehler); r = E.aktion(s, actor, s.phase === 'block' ? { t: 'blocke', z: {} } : s.phase === 'ziehen' ? { t: 'ziehe', stapel: 1 } : { t: 'ende', abwerfen: E.handZaehlt(s.sp[actor]).slice(0, Math.max(0, E.handZaehlt(s.sp[actor]).length - E.handlimit(s.sp[actor]))).map(c => c.i) }); if (!r.ok) { E.aktion(s, actor, { t: 'ende' }); } }
    this.speichern(); this.view.render();
    this.weiter(a.t === 'ziehe' ? 260 : a.t === 'angriff' || a.t === 'schuss' || a.t === 'blocke' ? 1100 : a.t === 'ende' ? 700 : 520);
  }
  menue() { menue(); }
  regeln() { regelnSeite(app, D, () => { tisch.render(); }); }
  neu() { ls.del('volk.save'); starteLokal(this.cfg); }
}
function starteOnline() { }
window.volk = { E, KI, get tisch() { return tisch; }, get ctrl() { return ctrl; } };
start().catch(e => { app.innerHTML = `<div class="laden">Fehler beim Laden: ${esc(e.message)}</div>`; console.error(e); });
