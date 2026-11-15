// Effekte: Optionen, kleine Chip-Klänge (Web Audio), schwebende Zahlen, Banner, Konfetti, Vibration
import { ic } from './sprites.js';

// ---------------------------------------------------------------- Optionen (werden gespeichert)
const KEY = 'volk.opt';
const reduziert = () => { try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch { return false; } };
export const opt = Object.assign({ ton: true, anim: !reduziert(), vib: true, tempo: 1 }, (() => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } })());
const speichern = () => { try { localStorage.setItem(KEY, JSON.stringify(opt)); } catch { } };
export const TEMPO = [[1.7, 'Langsam'], [1, 'Normal'], [0.45, 'Schnell']];
export const tempoFaktor = () => opt.tempo || 1;
export function wende() { document.body.classList.toggle('keineanim', !opt.anim); }
export function setzeOpt(k, v) {
  if (k === 'tempo') opt.tempo = +v; else opt[k] = v === undefined ? !opt[k] : (v === 'true' ? true : v === 'false' ? false : v);
  speichern(); wende(); if (k === 'ton' && opt.ton) ton('klick');
}
export function optionenInhalt() {
  const an = (b) => (b ? 'an' : '');
  const schalter = (k, name, hin) => `<div class="zeile"><label style="min-width:110px">${name}</label><div class="chips"><span class="chipb ${an(opt[k])}" data-a="opt" data-k="${k}" data-v="true">An</span><span class="chipb ${an(!opt[k])}" data-a="opt" data-k="${k}" data-v="false">Aus</span></div></div>${hin ? `<div class="hinweis" style="margin:-2px 0 6px">${hin}</div>` : ''}`;
  return `${schalter('ton', 'Ton', 'Kleine Chip-Klänge für Karten, Gold, Schaden und Aufstieg.')}
    ${schalter('anim', 'Animationen', 'Karten fliegen ein, Zahlen schweben, Konfetti beim Sieg.')}
    ${'vibrate' in navigator ? schalter('vib', 'Vibration', 'Kurzes Brummen bei Schaden und wenn du dran bist.') : ''}
    <div class="zeile"><label style="min-width:110px">Computer-Tempo</label><div class="chips">${TEMPO.map(([f, n]) => `<span class="chipb ${an(opt.tempo === f)}" data-a="opt" data-k="tempo" data-v="${f}">${n}</span>`).join('')}</div></div>
    <div class="hinweis" style="margin-top:8px">Tasten am PC: <b>Enter</b> Zug beenden · <b>1 2 3</b> Stapel ziehen · <b>A</b> Aufstieg · <b>← →</b> Reiter · <b>M</b> Ton · <b>Esc</b> schließen</div>`;
}

// ---------------------------------------------------------------- Klänge
let ctx = null;
function ac() {
  if (!ctx) { try { ctx = new (window.AudioContext || window.webkitAudioContext)(); } catch { return null; } }
  if (ctx.state === 'suspended') ctx.resume().catch(() => { });
  return ctx;
}
addEventListener('pointerdown', () => { if (opt.ton) ac(); }, { passive: true });
const KLANG = {
  klick: [[660, 0, .04, 'square', .035]],
  karte: [[320, 0, .05, 'triangle'], [520, .045, .07, 'triangle']],
  land: [[196, 0, .07, 'triangle'], [262, .06, .09, 'triangle']],
  gold: [[988, 0, .05, 'square', .05], [1319, .055, .11, 'square', .05]],
  schaden: [[190, 0, .09, 'sawtooth', .08], [120, .08, .16, 'sawtooth', .08]],
  heilung: [[523, 0, .07, 'triangle'], [784, .07, .12, 'triangle']],
  kultur: [[784, 0, .07, 'triangle'], [1175, .07, .13, 'triangle']],
  aufstieg: [[523, 0, .09], [659, .09, .09], [784, .18, .09], [1047, .27, .22]],
  zug: [[440, 0, .07, 'square', .05], [660, .08, .13, 'square', .05]],
  ereignis: [[392, 0, .1], [330, .1, .1], [262, .2, .18]],
  fehler: [[150, 0, .12, 'square', .05]],
  sieg: [[523, 0, .1], [659, .1, .1], [784, .2, .1], [1047, .3, .1], [784, .42, .1], [1047, .52, .3]],
  niederlage: [[392, 0, .16, 'triangle'], [330, .17, .16, 'triangle'], [262, .34, .16, 'triangle'], [196, .51, .34, 'triangle']],
};
export function ton(name) {
  if (!opt.ton) return; const c = ac(); const n = KLANG[name]; if (!c || !n) return;
  const t0 = c.currentTime + 0.01;
  for (const [f, d0, dur, typ = 'square', vol = .06] of n) {
    const o = c.createOscillator(), g = c.createGain();
    o.type = typ; o.frequency.setValueAtTime(f, t0 + d0);
    g.gain.setValueAtTime(0.0001, t0 + d0); g.gain.exponentialRampToValueAtTime(vol, t0 + d0 + 0.008); g.gain.exponentialRampToValueAtTime(0.0001, t0 + d0 + dur);
    o.connect(g); g.connect(c.destination); o.start(t0 + d0); o.stop(t0 + d0 + dur + 0.03);
  }
}
export const vibriere = (ms) => { if (opt.vib && navigator.vibrate) { try { navigator.vibrate(ms); } catch { } } };

// ---------------------------------------------------------------- Schwebende Zahl über einem Element
const belegt = new WeakMap();
export function schwebe(el, text, art = 'gold') {
  if (!opt.anim || !el) return; const r = el.getBoundingClientRect(); if (!r.width) return;
  const n = belegt.get(el) || 0; belegt.set(el, n + 1); setTimeout(() => belegt.set(el, Math.max(0, (belegt.get(el) || 1) - 1)), 700);
  const d = document.createElement('div'); d.className = 'schwebe f-' + art; d.innerHTML = text;
  d.style.left = Math.min(innerWidth - 44, Math.max(44, r.left + r.width / 2)) + 'px'; d.style.top = (r.top + Math.min(r.height, 24) / 2 - n * 18) + 'px'; d.style.animationDelay = (n * 0.12) + 's';
  document.body.appendChild(d); setTimeout(() => d.remove(), 1700);
}

// ---------------------------------------------------------------- Banner in der Bildschirmmitte
export function banner(html, kl = '') {
  if (!opt.anim) return; document.querySelector('.fxbanner')?.remove();
  const d = document.createElement('div'); d.className = 'fxbanner ' + kl; d.innerHTML = html; document.body.appendChild(d); setTimeout(() => d.remove(), 1800);
}

// ---------------------------------------------------------------- Konfetti aus Pixel-Quadraten
export function konfetti(n = 90) {
  if (!opt.anim) return; document.querySelector('.fxbanner')?.remove(); const w = document.createElement('div'); w.className = 'konfetti'; const F = ['#f1c40f', '#e0533d', '#5fbf4a', '#5aa0e6', '#a77de0', '#f0952f', '#f0ead6'];
  for (let i = 0; i < n; i++) {
    const p = document.createElement('i'); const s = 5 + Math.floor(Math.random() * 3) * 2;
    p.style.cssText = `left:${Math.random() * 100}%;width:${s}px;height:${s}px;background:${F[i % F.length]};--dx:${Math.round((Math.random() - .5) * 160)}px;--t:${(2.2 + Math.random() * 2).toFixed(2)}s;animation-delay:${(Math.random() * .9).toFixed(2)}s`;
    w.appendChild(p);
  }
  document.body.appendChild(w); setTimeout(() => w.remove(), 5200);
}

export const tonSymbol = () => ic(opt.ton ? 'ui:ton_an' : 'ui:ton_aus');
