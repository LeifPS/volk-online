// Online-Modus: Raum-Code, Schnellsuche, Lobby, Wiederverbinden.
import * as E from './engine.js';
import { Spieltisch } from './ui.js';
import { spr, ic } from './sprites.js';
import { kk } from './karten.js';
import { regelnSeite } from './regeln.js';
const esc = (t) => String(t ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const ls = { get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { } }, del(k) { try { localStorage.removeItem(k); } catch { } } };
const CODE_ZEICHEN = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
const neuerCode = () => Array.from({ length: 5 }, () => CODE_ZEICHEN[Math.floor(Math.random() * CODE_ZEICHEN.length)]).join('');
function holeToken() { let t = ls.get('volk.token', null); if (!t) { t = 'v' + Array.from(crypto.getRandomValues(new Uint8Array(12)), b => b.toString(16).padStart(2, '0')).join(''); ls.set('volk.token', t); } return t; }

let sitzung = null;     // aktive Verbindung
export function offeneSitzung() { return ls.get('volk.on', null); }

export function onlineMenue(app, D, zurueck, _start, vorCode) {
  const c = Object.assign({ name: ls.get('volk.setup', {}).name || 'Spieler', max: 2, vk: false, rel: false, civ: false }, ls.get('volk.onsetup', {}));
  const alt = offeneSitzung();
  const zeichne = (fehler = '') => {
    app.innerHTML = `<div class="menue"><h2>${ic('x:erde')} Online spielen</h2>
      <div class="karte-panel"><div class="zeile"><label>Dein Name</label><input type="text" id="o-name" maxlength="16" value="${esc(c.name)}"></div>
        ${fehler ? `<div class="grund" style="background:#ffe3df;border:2px solid #c44536;border-radius:8px;padding:6px 9px">${esc(fehler)}</div>` : ''}</div>
      ${alt ? `<div class="btns"><button class="gruen" id="o-zurueck">${ic('ui:pfeil_links')}Zurück in Raum ${esc(alt.code)}</button></div>` : ''}
      <div class="karte-panel"><h3>Freunde einladen</h3><div class="btns" style="grid-template-columns:1fr"><button id="o-neu" class="gruen">${ic('ui:plus')}Neuen Raum erstellen</button></div>
        <div class="zeile" style="margin-top:10px"><label>Raum-Code</label><input type="text" id="o-code" maxlength="6" placeholder="z. B. K7QM2" value="${esc(vorCode || '')}" style="text-transform:uppercase;flex:1"><button id="o-bei">Beitreten</button></div></div>
      <div class="karte-panel"><h3>Schnellsuche</h3><div class="hinweis" style="margin-bottom:6px">Du kommst in einen offenen Raum mit passenden Einstellungen. Freie Plätze füllt der Computer auf, wenn nach 20 Sekunden niemand kommt.</div>
        <div class="zeile"><label>Spieler</label><div class="chips">${[2, 3, 4].map(n => `<span class="chipb ${c.max === n ? 'an' : ''}" data-max="${n}">${n}</span>`).join('')}</div></div>
        <div class="modul ${c.vk ? 'an' : ''}" data-m="vk"><span class="haken">${c.vk ? ic('ui:haken') : ''}</span><div><b>Volkskarten</b><small>Erweiterung 1</small></div></div>
        <div class="modul ${c.rel ? 'an' : ''}" data-m="rel"><span class="haken">${c.rel ? ic('ui:haken') : ''}</span><div><b>Götter & Glaube</b><small>Erweiterung 2</small></div></div>
        <div class="modul ${c.civ ? 'an' : ''}" data-m="civ"><span class="haken">${c.civ ? ic('ui:haken') : ''}</span><div><b>Zivilisation</b><small>Erweiterung 3</small></div></div>
        <div class="btns" style="grid-template-columns:1fr"><button id="o-schnell">${ic('x:blitz')}Schnellsuche starten</button></div></div>
      <div class="btns"><button class="sek" id="o-zu">Zurück</button></div></div>`;
    document.getElementById('o-zu').onclick = zurueck;
    const name = () => { c.name = (document.getElementById('o-name').value || 'Spieler').trim() || 'Spieler'; ls.set('volk.onsetup', c); const s = ls.get('volk.setup', {}); s.name = c.name; ls.set('volk.setup', s); return c.name; };
    app.querySelectorAll('[data-max]').forEach(e => e.onclick = () => { name(); c.max = +e.dataset.max; zeichne(); });
    app.querySelectorAll('[data-m]').forEach(e => e.onclick = () => { name(); c[e.dataset.m] = !c[e.dataset.m]; zeichne(); });
    if (alt) document.getElementById('o-zurueck').onclick = () => verbinde(app, D, zurueck, { code: alt.code, name: name(), erstelle: false });
    document.getElementById('o-neu').onclick = () => verbinde(app, D, zurueck, { code: neuerCode(), name: name(), erstelle: true, cfg: { max: 4, vk: false, rel: false, civ: false }, versuche: 5 });
    document.getElementById('o-bei').onclick = () => { const code = document.getElementById('o-code').value.trim().toUpperCase(); if (code.length < 3) return zeichne('Bitte einen Raum-Code eingeben.'); verbinde(app, D, zurueck, { code, name: name(), erstelle: false }); };
    document.getElementById('o-schnell').onclick = async () => {
      name(); try { const r = await (await fetch('/api/schnell', { method: 'POST', body: JSON.stringify({ max: c.max, vk: c.vk, rel: c.rel, civ: c.civ }) })).json(); verbinde(app, D, zurueck, { code: r.code, name: c.name, erstelle: r.neu, cfg: { max: c.max, vk: c.vk, rel: c.rel, civ: c.civ, schnell: true } }); } catch { zeichne('Die Schnellsuche ist gerade nicht erreichbar.'); }
    };
  };
  zeichne();
}

// ---------------------------------------------------------------- Verbindung
function verbinde(app, D, zurueck, cfg) {
  sitzung?.schliessen();
  sitzung = new Sitzung(app, D, zurueck, cfg); sitzung.oeffnen();
}
class Sitzung {
  constructor(app, D, zurueck, cfg) { this.app = app; this.D = D; this.zurueck = zurueck; this.cfg = cfg; this.token = holeToken(); this.ws = null; this.s = null; this.me = -1; this.n = 0; this.wait = new Map(); this.ansicht = null; this.tisch = null; this.zu = false; this.versuch = 0; this.lobby = null; this.status = 'Verbinde …'; }
  schliessen() { this.zu = true; clearInterval(this.ping); try { this.ws?.close(); } catch { } this.tisch = null; }
  oeffnen() {
    const proto = location.protocol === 'https:' ? 'wss' : 'ws';
    this.ws = new WebSocket(`${proto}://${location.host}/ws/raum/${this.cfg.code}`);
    this.ws.onopen = () => { this.versuch = 0; this.ws.send(JSON.stringify({ t: 'hallo', token: this.token, name: this.cfg.name, erstelle: this.cfg.erstelle, cfg: this.cfg.cfg, code: this.cfg.code })); clearInterval(this.ping); this.ping = setInterval(() => { try { this.ws.send('{"t":"ping"}'); } catch { } }, 20000); };
    this.ws.onmessage = (e) => this.nachricht(JSON.parse(e.data));
    this.ws.onclose = () => { clearInterval(this.ping); if (this.zu) return; this.getrennt(); };
    this.ws.onerror = () => { };
    if (!this.lobby && !this.s) this.zeigeStatus('Verbinde mit Raum ' + this.cfg.code + ' …');
  }
  getrennt() {
    if (this.zu) return; this.versuch++;
    if (this.versuch > 8) { this.zeigeStatus('Verbindung verloren.', true); return; }
    this.banner('Verbindung verloren – verbinde neu … (' + this.versuch + ')'); setTimeout(() => { if (!this.zu) { this.cfg.erstelle = false; this.oeffnen(); } }, Math.min(5000, 800 * this.versuch));
  }
  banner(t) { const el = document.getElementById('toasts'); const d = document.createElement('div'); d.className = 'toast'; d.textContent = t; el.appendChild(d); setTimeout(() => d.remove(), 2500); }
  zeigeStatus(t, knopf) { if (this.s) return; this.app.innerHTML = `<div class="menue"><h2>${ic('x:erde')} Online</h2><div class="karte-panel"><p>${esc(t)}</p></div>${knopf ? '<div class="btns"><button id="x-zu">Zurück</button></div>' : ''}</div>`; if (knopf) document.getElementById('x-zu').onclick = () => { this.schliessen(); this.zurueck(); }; }
  senden(o) { try { this.ws.send(JSON.stringify(o)); } catch { } }
  nachricht(m) {
    if (m.t === 'fehler') {
      if (m.belegt && this.cfg.versuche > 1) { this.cfg.versuche--; this.cfg.code = neuerCode(); this.zu = true; try { this.ws.close(); } catch { } this.zu = false; return this.oeffnen(); }
      if (m.weg || m.raus) { ls.del('volk.on'); this.schliessen(); this.app.innerHTML = `<div class="menue"><h2>${ic('x:erde')} Online</h2><div class="karte-panel"><p>${esc(m.text)}</p></div><div class="btns"><button id="x-zu">Zurück</button></div></div>`; document.getElementById('x-zu').onclick = this.zurueck; return; }
      if (this.tisch) this.tisch.toast(m.text); else this.banner(m.text); return;
    }
    if (m.t === 'lobby') { ls.set('volk.on', { code: this.cfg.code }); this.cfg.code = m.code || this.cfg.code; this.lobby = m; this.s = null; this.tisch = null; this.lobbyZeigen(); }
    else if (m.t === 'zustand') { ls.set('volk.on', { code: this.cfg.code }); this.lobby = null; this.me = m.me; this.host = m.host; this.sitze = m.sitze; const neu = !this.s; this.s = m.s; if (neu || !this.tisch) this.tischStarten(); else this.tisch.render(); }
    else if (m.t === 'ergebnis') { this.wait.get(m.id)?.(m); this.wait.delete(m.id); }
  }
  // Steuerung für den Spieltisch
  async send(a) { return new Promise(res => { const id = ++this.n; this.wait.set(id, res); this.senden({ t: 'a', id, a }); setTimeout(() => { if (this.wait.delete(id)) res({ ok: false, fehler: 'Keine Antwort vom Server.' }); }, 8000); }); }
  stop() { }
  menue() { if (confirm('Den Online-Raum verlassen? Du kannst über „Zurück in Raum“ wieder beitreten.')) { this.schliessen(); this.zurueck(); } }
  regeln() { regelnSeite(this.app, this.D, () => this.tisch?.render()); }
  neu() { if (this.host) this.senden({ t: 'revanche' }); else this.tisch.toast('Nur der Gastgeber kann eine neue Runde starten.'); }
  tischStarten() {
    const ov = document.getElementById('overlay'); this.tisch = new Spieltisch(this.app, ov, this); this.tisch.ereigGesehen = this.s.letztes ? this.s.letztes.n : 0; this.tisch.render();
  }
  // ---------------------------------------------------------------- Lobby
  lobbyZeigen() {
    const L = this.lobby, D = this.D, ov = document.getElementById('overlay'); ov.classList.remove('an'); ov.innerHTML = '';
    const link = location.origin + '/?raum=' + L.code;
    const mein = L.sitze[L.ich] || {};
    const vopt = (sel) => `<option value="">Zufällig</option>${D.voelker.map(v => `<option value="${v.id}" ${sel === v.id ? 'selected' : ''} ${L.sitze.some((x, i) => i !== L.ich && x.volk === v.id) ? 'disabled' : ''}>${esc(v.name)}</option>`).join('')}`;
    const sitze = Array.from({ length: L.max }, (_, i) => { const x = L.sitze[i]; if (!x) return `<div class="sitz" style="opacity:.5"><b>Platz ${i + 1}</b><span>frei</span><span></span></div>`; const v = D.voelker.find(q => q.id === x.volk);
      return `<div class="sitz"><b>${x.ki ? ic('x:roboter') : ic(x.verbunden ? 'x:punkt' : 'x:getrennt')} ${esc(x.name)}${i === 0 ? ic('ui:krone') : ''}${i === L.ich ? ' (du)' : ''}</b><span>${i === L.ich ? `<select id="l-volk">${vopt(x.volk)}</select>` : esc(v ? v.name : 'Volk: zufällig') + (x.ki ? ' · ' + esc(x.ki) : '')}</span><span>${L.host && i > 0 ? `<button class="sek" data-raus="${i}" data-ki="${x.ki ? 1 : 0}" style="padding:.2em .6em">${x.ki ? 'Entfernen' : 'Rauswerfen'}</button>` : ''}</span></div>`; }).join('');
    this.app.innerHTML = `<div class="menue"><h2>${ic('x:erde')} Raum</h2>
      <div class="karte-panel" style="text-align:center"><div class="mini">Raum-Code</div><div class="codebox">${esc(L.code)}</div>
        <div class="btns" style="grid-template-columns:1fr 1fr;margin-top:6px"><button id="l-copy" class="sek">${ic('x:kopie')}Link kopieren</button><button id="l-share" class="sek">${ic('x:teilen')}Teilen</button></div></div>
      <div class="karte-panel"><h3>Spieler (${L.sitze.length}/${L.max})</h3>${sitze}
        ${L.host && !L.schnell && L.sitze.length < L.max ? `<div class="zeile"><label>Computer</label><div class="chips">${['leicht', 'mittel', 'stark'].map(s => `<span class="chipb" data-addki="${s}">+ ${s}</span>`).join('')}</div></div>` : ''}
        ${L.host && !L.schnell ? `<div class="zeile"><label>Plätze</label><div class="chips">${[2, 3, 4].map(n => `<span class="chipb ${L.max === n ? 'an' : ''} ${n < L.sitze.length ? 'aus' : ''}" data-max="${n}">${n}</span>`).join('')}</div></div>` : ''}
        ${L.schnell && L.startIn !== null ? `<p class="hinweis">Das Spiel startet in <b>${L.startIn}</b> s – freie Plätze füllt der Computer.</p>` : L.schnell ? '<p class="hinweis">Warte auf Mitspieler …</p>' : ''}</div>
      <div class="karte-panel"><h3>Module</h3>
        <div class="modul fest an"><span class="haken">${ic('ui:haken')}</span><div><b>Grundspiel</b></div></div>
        <div class="modul ${L.opt.vk ? 'an' : ''} ${L.host && !L.schnell ? '' : 'fest'}" data-m="vk"><span class="haken">${L.opt.vk ? ic('ui:haken') : ''}</span><div><b>Erweiterung 1: Volkskarten</b></div></div>
        <div class="modul ${L.opt.rel ? 'an' : ''} ${L.host && !L.schnell ? '' : 'fest'}" data-m="rel"><span class="haken">${L.opt.rel ? ic('ui:haken') : ''}</span><div><b>Erweiterung 2: Götter & Glaube</b><small>Glaubenssieg bei ${L.glaubeZiel}</small></div></div>
        <div class="modul ${L.opt.civ ? 'an' : ''} ${L.host && !L.schnell ? '' : 'fest'}" data-m="civ"><span class="haken">${L.opt.civ ? ic('ui:haken') : ''}</span><div><b>Erweiterung 3: Zivilisation</b><small>Regierungen, Persönlichkeiten, Naturwunder</small></div></div></div>
      <div class="btns">${L.host ? `<button class="gruen" id="l-start" ${L.sitze.length < 2 ? 'disabled' : ''}>${ic('x:los')}Spiel starten</button>` : '<div class="hinweis" style="color:#fff">Der Gastgeber startet das Spiel.</div>'}<button class="sek" id="l-weg">Raum verlassen</button></div></div>`;
    document.getElementById('l-copy').onclick = async () => { try { await navigator.clipboard.writeText(link); this.banner('Link kopiert'); } catch { prompt('Link:', link); } };
    document.getElementById('l-share').onclick = async () => { if (navigator.share) { try { await navigator.share({ title: 'Volk – Das Kartenspiel', text: 'Spiel mit mir Volk! Raum-Code: ' + L.code, url: link }); } catch { } } else document.getElementById('l-copy').click(); };
    document.getElementById('l-weg').onclick = () => { ls.del('volk.on'); this.schliessen(); this.zurueck(); };
    const v = document.getElementById('l-volk'); if (v) v.onchange = () => this.senden({ t: 'volk', volk: v.value });
    const st = document.getElementById('l-start'); if (st) st.onclick = () => this.senden({ t: 'start' });
    this.app.querySelectorAll('[data-addki]').forEach(e => e.onclick = () => this.senden({ t: 'ki', stufe: e.dataset.addki }));
    this.app.querySelectorAll('[data-raus]').forEach(e => e.onclick = () => this.senden(e.dataset.ki === '1' ? { t: 'kiweg', i: +e.dataset.raus } : { t: 'raus', i: +e.dataset.raus }));
    this.app.querySelectorAll('[data-max]').forEach(e => e.onclick = () => this.senden({ t: 'einst', max: +e.dataset.max }));
    if (L.host && !L.schnell) this.app.querySelectorAll('[data-m]').forEach(e => e.onclick = () => this.senden({ t: 'einst', opt: { ...L.opt, [e.dataset.m]: !L.opt[e.dataset.m] } }));
    if (L.schnell && L.startIn !== null) { clearTimeout(this.cd); this.cd = setTimeout(() => { if (this.lobby === L && L.startIn > 0) { L.startIn--; this.lobbyZeigen(); } }, 1000); }
  }
}
