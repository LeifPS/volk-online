// Spieltisch: zeigt den Zustand (egal ob lokal oder online) und sendet Aktionen über ctrl.send(a).
import * as E from './engine.js';
import * as KI from './ki.js';
import { spr, hatSprite } from './sprites.js';
import { kartenArt, kartenZeilen, farbeKarte, braucht, benoetigt, ZA, EFF_LANG, SCHL_TXT, ROH, KLASSE } from './text.js';
const { def } = E;
const esc = (t) => String(t ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const GR = [['#79a84f', '#6f9e48', '#4d7a32'], ['#8fae5a', '#85a552', '#5d7c3a'], ['#9aa860', '#8f9d58', '#667442'], ['#a8a468', '#9d9a60', '#6f6c44'], ['#8f8f86', '#868680', '#5d5d58'], ['#8a9199', '#80878f', '#5a6068'], ['#7a9a96', '#70908c', '#4e6a68']];
const STAPEL_F = { 1: '#b9935a', 2: '#8f6f4e', 3: '#6a7c8c' };

export class Spieltisch {
  constructor(root, overlay, ctrl) {
    this.root = root; this.ov = overlay; this.c = ctrl; this.tab = 'ich'; this.sel = new Set(); this.modalFn = null; this.blk = {}; this.ereigGesehen = 0; this.siegZu = false; this.toastT = null;
    root.onclick = (e) => this.klick(e); overlay.onclick = (e) => { if (e.target === overlay && !this.erzwungen()) { this.modalFn = null; this.render(); } else this.klick(e); };
  }
  get s() { return this.c.s; } get me() { return this.c.me; }
  p(i) { return this.s.sp[i]; }
  meinZug() { return this.s.am === this.me && this.s.phase !== 'ende' && this.s.phase !== 'block'; }
  erzwungen() { const s = this.s; return s.sieger !== null && !this.siegZu || (s.phase === 'block' && s.kampf.ziel === this.me) || this.ereignisOffen(); }
  ereignisOffen() { const s = this.s; return !!(s.letztes && s.letztes.n > this.ereigGesehen && s.sieger === null); }
  blockiert() { return this.erzwungen() || !!this.modalFn; }   // Computer wartet, solange etwas erklärt wird
  toast(t) { const d = document.createElement('div'); d.className = 'toast'; d.textContent = t; document.getElementById('toasts').appendChild(d); setTimeout(() => d.remove(), 2600); }
  async senden(a) { const r = await this.c.send(a); if (!r.ok) this.toast(r.fehler || 'Das geht nicht.'); return r; }

  // ---------------------------------------------------------------- Rendering
  render() {
    const s = this.s, me = this.p(this.me), D = E.daten();
    if (!this.s) return;
    if (this.tab !== 'ich' && this.tab !== 'tisch' && this.tab !== 'log' && !(this.tab >= 0 && this.s.sp[this.tab])) this.tab = 'ich';
    const aktiv = s.sp[s.phase === 'block' ? s.kampf.ziel : s.am];
    const ticker = s.ev.slice(-3).map(e => esc(e.t)).join(' &nbsp;›&nbsp; ');
    const chips = s.sp.map((p, i) => {
      const v = D.voelker.find(x => x.id === p.volk);
      return `<div class="chip ${i === s.am && s.sieger === null ? 'aktiv' : ''} ${String(this.tab) === String(i) || (i === this.me && this.tab === 'ich') ? 'sel' : ''} ${p.tot ? 'tot' : ''}" data-a="tab" data-v="${i === this.me ? 'ich' : i}">
        <div class="n"><span class="pt" style="background:${v.farbe}"></span>${esc(p.name)}${p.ki ? ' 🤖' : ''}</div>
        <div class="w"><span>❤ ${Math.max(0, p.hp)}</span><span>🎭 ${E.kultur(p)}/${E.REGELN().kultur_sieg}</span>${s.opt.rel ? `<span>🔥 ${E.glaube(s, p)}/${s.glaubeZiel}</span>` : ''}<span>🃏 ${p.hand.length}</span></div></div>`;
    }).join('');
    const tabs = [['ich', 'Mein Reich'], ['tisch', 'Tisch'], ...s.sp.map((p, i) => i === this.me ? null : [i, p.name]).filter(Boolean), ['log', 'Verlauf']]
      .map(([k, n]) => `<button class="${String(this.tab) === String(k) ? 'an' : ''}" data-a="tab" data-v="${k}">${esc(n)}</button>`).join('');
    let inhalt = '';
    if (this.tab === 'ich') inhalt = this.reichHtml(this.me); else if (this.tab === 'tisch') inhalt = this.tischHtml(); else if (this.tab === 'log') inhalt = this.logHtml(); else inhalt = this.reichHtml(+this.tab);
    const st = this.buehne ? this.buehne.scrollTop : 0;
    this.root.innerHTML = `<div class="spiel">
      <div class="kopf"><div class="titel">Runde ${s.runde} · ${esc(aktiv.name)} ${s.am === this.me && s.phase !== 'block' ? '(du)' : ''}</div>
        <button class="sek" data-a="regeln">?</button><button class="sek" data-a="menue">☰</button></div>
      <div class="ticker">${ticker || '&nbsp;'}</div>
      <div class="leiste">${chips}</div>
      <div class="tabs">${tabs}</div>
      <div class="buehne">${inhalt}</div>
      <div class="fuss-leiste">${this.aktionsHtml()}<div class="hand ${me.hand.length ? '' : 'leer'}">${this.handHtml()}</div></div></div>`;
    this.buehne = this.root.querySelector('.buehne'); this.buehne.scrollTop = st;
    this.renderModal();
  }
  renderModal() {
    const s = this.s; let html = null;
    if (s.sieger !== null && !this.siegZu) html = this.siegHtml();
    else if (s.phase === 'block' && s.kampf.ziel === this.me) html = this.blockHtml();
    else if (this.ereignisOffen()) html = this.ereignisHtml();
    else if (this.modalFn) { html = this.modalFn(); if (html === null) this.modalFn = null; }
    if (html === null || html === undefined) { this.ov.classList.remove('an'); this.ov.innerHTML = ''; return; }
    this.ov.classList.add('an'); const old = this.ov.querySelector('.sheet'); const sc = old ? old.scrollTop : 0;
    this.ov.innerHTML = `<div class="sheet ${old ? 'still' : ''}">${html}</div>`; const nw = this.ov.querySelector('.sheet'); if (nw) nw.scrollTop = sc;
  }

  // ---------------------------------------------------------------- Karten
  karteHtml(c, p, o = {}) {
    const d = def(c); if (!d) return '';
    const farbe = p ? p.volkF : '#2f6fd0'; const f = farbeKarte(d);
    const rf = d.relkarte ? d.farbe_rel : farbe;
    let kosten = '';
    if (d.typ === 'land') kosten = ''; else if (d.typ === 'wunder') kosten = `${d.kosten}`; else if (p && (d.typ === 'einheit' || d.typ === 'gebaeude')) { const k = E.kostenGesamt(p, c); kosten = `${k === null ? '✖' : k}`; } else if (d.kosten) kosten = d.kosten;
    const bild = d.sprite && hatSprite(d.sprite) ? spr(d.sprite, rf, o.gross ? 3 : (d.typ === 'wunder' ? 1 : 1.5)) : '';
    const deko = d.typ === 'land' && d.deko && hatSprite(d.deko) ? `<div style="position:absolute;inset:0">${spr(d.deko, farbe, 1, 'x')}</div>` : '';
    return `<div class="karte ${o.gross ? 'gross' : ''} ${o.klein ? 'klein' : ''} ${o.cls || ''}" style="--f:${f}" ${o.a ? `data-a="${o.a}" data-v="${o.v ?? c.i}"` : ''}>
      ${c.vk ? '<span class="vk">Volk</span>' : ''}${d.relkarte ? '<span class="rk">Glaube</span>' : ''}
      <div class="k-kopf"><span class="k-name">${esc(d.name)}</span>${kosten !== '' ? `<span class="k-kosten">${spr('ui:gold', '#fff', 1)}${kosten}</span>` : ''}</div>
      <div class="k-bild">${deko}<span style="position:relative">${bild}</span></div>
      <div class="k-art">${esc(kartenArt(d))} · ${d.zeitalter != null && d.typ !== 'land' ? ZA[d.zeitalter] : ''}</div>
      <div class="k-text">${kartenZeilen(d).map(z => `<div>${esc(z)}</div>`).join('')}</div></div>`;
  }
  handHtml() {
    const me = this.p(this.me), s = this.s; if (!me.hand.length) return 'Keine Handkarten.';
    const ord = (c) => { const d = def(c); return (c.vk ? 0 : d.relkarte ? 2 : 1) * 10 + ({ land: 0, einheit: 1, gebaeude: 2 }[d.typ] ?? 3); };
    return me.hand.slice().sort((a, b) => ord(a) - ord(b)).map(c => {
      const ok = this.meinZug() && s.phase === 'aktion' && this.spielbar(c);
      return this.karteHtml(c, me, { a: 'hand', cls: ok ? 'spielbar' : (this.meinZug() && s.phase === 'aktion' ? 'dim' : '') });
    }).join('');
  }
  spielbar(c) {
    const s = this.s, p = this.p(this.me), d = def(c);
    if (d.typ === 'land') return p.landG < E.landErlaubt(p);
    if (d.klasse === 'missionar') return !!p.religion && p.gold >= E.kosten(p, c) && E.gegner(s, p).some(o => !s.missionen.some(m => m.owner === this.me && s.sp[m.host] === o));
    if (d.typ === 'einheit' || d.typ === 'gebaeude') return E.sperrGrund(s, p, c) === null;
    return false;
  }

  // ---------------------------------------------------------------- Aktionsleiste
  aktionsHtml() {
    const s = this.s, p = this.p(this.me);
    if (s.sieger !== null) return `<div class="aktionen"><div class="info">Das Spiel ist vorbei.</div><button data-a="siegzeigen">Ergebnis</button></div>`;
    if (s.phase === 'block') return `<div class="aktionen"><div class="info">${s.kampf.ziel === this.me ? 'Du wirst angegriffen!' : esc(this.p(s.kampf.ziel).name) + ' verteidigt sich …'}</div></div>`;
    if (s.am !== this.me) return `<div class="aktionen"><div class="info">${esc(this.p(s.am).name)} ist am Zug … Gold ${p.gold}</div></div>`;
    if (s.phase === 'ziehen') {
      const bt = [1, 2, 3].filter(st => st <= E.maxStapel(p)).map(st => `<button data-a="ziehe" data-v="${st}">Stapel ${ZA[st - 1]} <small>(${s.stapel[st].length})</small></button>`).join('');
      const rel = p.religion && p.relStapel.length && !p.relBenutzt ? `<button class="gruen" data-a="ziehe" data-v="rel">🔥 Glaubensstapel (${p.relStapel.length})</button>` : '';
      return `<div class="aktionen"><div class="info">Ziehe noch <b>${s.zieh}</b> Karte(n) – Einkommen ist schon gutgeschrieben. Gold: <b>${p.gold}</b></div>${bt}${rel}</div>`;
    }
    const ak = E.aufstiegKosten(p);
    const auswahl = [...this.sel].map(i => E.einheiten(p).find(u => u.i === i)).filter(Boolean);
    let b = '';
    if (auswahl.length) {
      b += E.gegner(s, p).map(o => `<button class="rot" data-a="angriff" data-v="${s.sp.indexOf(o)}" ${E.schutzAktiv(s) ? 'disabled' : ''}>⚔ gegen ${esc(o.name)}</button>`).join('');
      if (auswahl.some(E.kannSchiessen)) b += `<button class="rot" data-a="schiessen">🏹 Schießen</button>`;
      b += `<button class="sek" data-a="selclear">Abwählen</button>`;
    } else {
      if (ak !== null) b += `<button data-a="aufstieg" ${p.gold < ak ? 'disabled' : ''}>⬆ Zeitalter ${ZA[p.alter + 1]} <small>(${ak} 💰)</small></button>`;
      if (s.opt.rel && !p.religion && p.alter >= 1) b += `<button class="sek" data-a="gruenden">🔥 Religion gründen <small>(5 💰)</small></button>`;
      b += `<button class="gruen" data-a="ende">Zug beenden ▸</button>`;
    }
    const info = auswahl.length ? `${auswahl.length} Einheit(en) gewählt${E.schutzAktiv(s) ? ' – Neulingsschutz: noch kein Angriff' : ''}` : `Gold <b>${p.gold}</b> · Einkommen +${E.einkommen(s, p)} · Land ${p.landG}/${E.landErlaubt(p)} gelegt`;
    return `<div class="aktionen"><div class="info">${info}</div>${b}</div>`;
  }

  // ---------------------------------------------------------------- Reich
  statsHtml(p, isMe) {
    const s = this.s, R = E.REGELN();
    const stat = (ico, txt, cls = '') => `<div class="stat ${cls}">${ico}${txt}</div>`;
    return `<div class="stats">
      ${stat(spr('ui:gold', '#fff', 1), `<b>${p.gold}</b> <small>+${E.einkommen(s, p)}/Runde</small>`, 'gold')}
      ${stat(spr('ui:zeitalter', '#fff', 1), `<b>${ZA[p.alter]}</b> <small>${esc(E.daten().zeitalter[p.alter].name)}</small>`)}
      ${stat(spr('ui:kultur', '#fff', 1), `<b>${E.kultur(p)}</b><small>/${R.kultur_sieg} Kultur</small>`)}
      ${s.opt.rel ? stat(spr('rel:glaube', '#fff', 1), `<b>${E.glaube(s, p)}</b><small>/${s.glaubeZiel} Glaube</small>`) : ''}
      ${stat(spr('ui:staerke', '#fff', 1), `<b>${E.schutz(p)}</b><small> Schutz</small>`)}
      ${stat('🃏', `<b>${p.hand.length}</b><small>${isMe ? '/' + (E.handlimit(p)) + ' Limit' : ' Karten'}</small>`)}</div>`;
  }
  reichHtml(pi) {
    const s = this.s, p = this.p(pi), D = E.daten(), R = E.REGELN(), isMe = pi === this.me;
    const v = D.voelker.find(x => x.id === p.volk), rel = p.religion ? D.religionen.find(r => r.id === p.religion) : null;
    const hpPct = Math.max(0, p.hp / R.stadt_hp * 100), hpC = hpPct > 60 ? '' : hpPct > 30 ? 'mid' : 'low';
    const gr = GR[p.alter], n = p.geb.length + p.wunder.length, gro = n < 3 ? 1 : n < 7 ? 2 : 3;
    const ckey = `stadt:stadt@${p.alter}@${gro}`, S = E.schutz(p);
    const stadt = `<div class="stadt"><div class="stadtbild" style="width:192px;height:168px">${spr(ckey, p.volkF, 3)}${S > 0 && hatSprite('stadt:mauer@' + Math.min(3, p.alter)) ? spr('stadt:mauer@' + Math.min(3, p.alter), p.volkF, 3, 'mauer') : ''}</div>
      <div class="hpbalken ${hpC}"><i style="width:${hpPct}%"></i></div><div class="hptxt">❤ ${Math.max(0, p.hp)} / ${R.stadt_hp}${S ? ` · 🛡 ${S}` : ''}</div></div>`;
    const geb = p.geb.map(c => this.kachelHtml(c, p, 'geb')).join('');
    const wun = p.wunder.map(c => this.kachelHtml(c, p, 'wunder')).join('');
    const sta = p.staaten.map(c => this.kachelHtml(c, p, 'staat')).join('');
    const land = p.land.map(c => this.landHtml(c, p)).join('');
    const einh = (arr, cls) => arr.map(u => this.einheitHtml(u, p, isMe, cls)).join('');
    const mis = E.missionenBei(s, p), meine = E.missionenAus(s, p);
    const misHtml = (list, wohin) => list.map(m => { const o = s.sp[wohin ? m.host : m.owner], r = D.religionen.find(x => x.id === s.sp[m.owner].religion); return `<div class="mis" style="--rf:${r.farbe}">${spr(`rel:${r.id}:missionar`, r.farbe, 1)} <span>${wohin ? '→ ' : 'von '}${esc(o.name)}</span>${!wohin && isMe && this.meinZug() && s.phase === 'aktion' ? `<button data-a="ausweisen" data-v="${m.c.i}" style="padding:.1em .5em;font-size:.9em">Ausweisen (${p.religion === 'flammenorden' ? 1 : 2}💰)</button>` : ''}</div>`; }).join('');
    return `<div class="reich">
      <div class="band" style="--vf:${v.farbe}">${spr('stadt:stadtstaat', p.volkF, 1)}<div><div class="vn">${esc(p.name)} – ${esc(v.name)}</div><div class="mini">${esc(v.herrscher)}</div></div><div class="fa">${v.text.map(esc).join(' ')}${rel ? `<br>🔥 <b>${esc(rel.name)}</b>: ${esc(rel.text)}` : ''}</div></div>
      ${this.statsHtml(p, isMe)}
      <div class="plan"><h4>${spr('ui:stadt', '#2b2118', 1)} Stadt & Bezirke</h4>
        <div class="boden" style="--g1:${gr[0]};--g2:${gr[1]};--g3:${gr[2]}">${stadt}${geb}${wun}${sta}</div>
        ${!geb && !wun && !sta ? '<div class="hinweis" style="margin-top:6px">Noch keine Gebäude – spiele Karten aus deiner Hand.</div>' : ''}</div>
      <div class="plan"><h4>🌾 Land (${p.land.length})</h4><div class="reihe">${land || '<span class="hinweis">Noch kein Land.</span>'}</div></div>
      <div class="plan"><h4>⚔ Heer – Front</h4><div class="heer">${einh(p.front, '') || '<span class="hinweis">Keine Einheiten an der Front.</span>'}</div>
        ${p.kaserne.length ? `<h4 style="margin-top:8px">🏕 Kaserne <span class="mini">(ab deinem nächsten Zug an der Front)</span></h4><div class="heer">${einh(p.kaserne, 'neu')}</div>` : ''}</div>
      ${s.opt.rel && (mis.length || meine.length || p.religion) ? `<div class="plan"><h4>🔥 Glaube${rel ? ' – ' + esc(rel.name) : ''}</h4>${rel ? `<div class="mini">${esc(rel.titel)}: ${esc(rel.text)}</div>` : '<div class="hinweis">Noch keine Religion gegründet.</div>'}
        ${mis.length ? `<div class="mini" style="margin-top:6px">Fremde Missionare in dieser Stadt (senken den Glauben):</div><div class="missionen">${misHtml(mis, false)}</div>` : ''}
        ${meine.length ? `<div class="mini" style="margin-top:6px">Entsandte Missionare:</div><div class="missionen">${misHtml(meine, true)}</div>` : ''}</div>` : ''}
      ${!isMe ? `<div class="hinweis">Handkarten: ${p.hand.length} · Einkommen +${E.einkommen(s, p)}</div>` : ''}
    </div>`;
  }
  kachelHtml(c, p, art) {
    const d = def(c), rf = d.relkarte ? d.farbe_rel : p.volkF;
    const ef = art === 'staat' ? [] : E.daten() && (d.typ === 'wunder' ? (d.text || []) : this.kurz(d));
    const sp2 = art === 'staat' ? spr('stadt:stadtstaat', d.farbe, 1) : spr(d.sprite, rf, d.typ === 'wunder' ? 1 : (d.relkarte ? 1.5 : 2));
    return `<div class="kachel ${d.relkarte ? 'rel' : ''} ${art}" style="--rf:${rf}" data-a="info" data-v="${c.id}" data-p="${this.s.sp.indexOf(p)}"><div class="ico">${sp2}</div><b>${esc(d.name)}</b><div class="e">${ef.join ? ef.map(esc).join(' · ') : ''}</div></div>`;
  }
  kurz(d) { const o = []; for (const [k, v] of Object.entries(d.effekte || {})) if (v) o.push((EFF_SHORT[k] || k) + (k === 'SCHIFF' ? '' : ' ') + '+' + v); for (const p of d.prov || []) o.push(ROH[p] || p); return o; }
  landHtml(c, p) {
    const d = def(c);
    return `<div class="kachel land" data-a="info" data-v="${c.id}" data-p="${this.s.sp.indexOf(p)}" style="width:78px"><div class="ico"><div class="t">${d.deko && hatSprite(d.deko) ? spr(d.deko, p.volkF, 1, 'x').replace('class="px x"', 'class="px" style="width:100%;height:100%"') : ''}</div><span class="r">${hatSprite(d.sprite) ? spr(d.sprite, p.volkF, 2) : ''}</span></div><b>${esc(d.name)}</b><div class="e">${d.ertrag ? '+' + d.ertrag + '💰' : ''}${(d.symbole || []).map(x => ' ' + (ROH[x] || x)).join('')}</div></div>`;
  }
  einheitHtml(u, p, isMe, cls) {
    const d = def(u), s = this.s, pi = s.sp.indexOf(p), f = d.relkarte ? d.farbe_rel : p.volkF;
    const waehlbar = isMe && this.meinZug() && s.phase === 'aktion' && E.kannAngreifen(u) && cls !== 'neu';
    return `<div class="einh ${u.t ? 'erschoepft' : ''} ${cls} ${this.sel.has(u.i) ? 'sel' : ''}" data-a="einheit" data-v="${u.i}" data-p="${pi}" data-w="${waehlbar ? 1 : 0}">
      ${spr(d.sprite, f, 2)}<b>${esc(d.name)}</b><div class="st">⚔${d.staerke}${d.fern ? ' 🏹' + d.fern : ''}</div>${u.t ? '<div class="mini">erschöpft</div>' : ''}</div>`;
  }

  // ---------------------------------------------------------------- Tisch
  tischHtml() {
    const s = this.s, p = this.p(this.me), D = E.daten(), R = E.REGELN();
    const aktion = this.meinZug() && s.phase === 'aktion';
    const wun = s.wunderOffen.map(w => { const d = def(w), g = E.sperrGrund(s, p, w); return `<div class="paket">${this.karteHtml(w, p, { a: 'wunderinfo', cls: aktion && !g ? 'spielbar' : '' })}</div>`; }).join('');
    const sta = s.auslage.map(t => { const d = def(t); return `<div class="paket"><div class="kachel staat" data-a="staatinfo" data-v="${t.i}" style="width:96px;padding:4px"><div class="ico" style="height:60px">${spr('stadt:stadtstaat', d.farbe, 1)}</div><b>${esc(d.name)}</b><div class="e">${this.kurz(d).join(' · ') || 'Hafen-Symbol'}</div><div class="e"><b>${d.kosten}</b> 💰 Tribut</div></div></div>`; }).join('');
    const stp = [1, 2, 3].map(st => `<div class="stapelk ${st > E.maxStapel(p) ? 'aus' : ''}" style="--sf:${STAPEL_F[st]}" ${this.meinZug() && s.phase === 'ziehen' && st <= E.maxStapel(p) ? `data-a="ziehe" data-v="${st}"` : ''}>Stapel ${ZA[st - 1]}<small>${s.stapel[st].length} Karten</small><small>ab Zeitalter ${ZA[R.stapel_von_zeitalter.indexOf(st)]}</small></div>`).join('');
    const rels = s.opt.rel ? `<div class="plan"><h4>🔥 Religionen</h4><div class="religionen">${D.religionen.map(r => { const frei = s.relFrei.includes(r.id), inh = s.sp.find(x => x.religion === r.id); return `<div class="relk ${frei ? '' : 'vergeben'}" style="--rf:${r.farbe}">${spr(`rel:${r.id}:emblem`, r.farbe, 1)}<div><b>${esc(r.name)}</b>${esc(r.titel)}: ${esc(r.text)}<div class="mini">${frei ? 'noch frei' : 'gegründet von ' + esc(inh.name)}</div></div></div>`; }).join('')}</div><div class="hinweis" style="margin-top:6px">Gründen: ab Zeitalter II, 5 💰 und 1 Handkarte ablegen. Glaubenssieg bei ${s.glaubeZiel} Glaube.</div></div>` : '';
    return `<div class="tisch">
      <div class="plan"><h4>🏛 Wunder <span class="mini">(tippen zum Bauen)</span></h4><div class="auslage">${wun || '<span class="hinweis">Alle Wunder sind gebaut.</span>'}</div></div>
      <div class="plan"><h4>🏰 Stadtstaaten <span class="mini">(Tribut ${R.tribut_kosten} 💰 – höchstens 2 Verbündete)</span></h4><div class="auslage">${sta || '<span class="hinweis">Keine Stadtstaaten mehr.</span>'}</div></div>
      <div class="plan"><h4>🃏 Kartenstapel</h4><div class="stapel">${stp}</div>${p.religion ? `<div class="hinweis" style="margin-top:6px">Dein Glaubensstapel: ${p.relStapel.length} Karten.</div>` : ''}</div>
      ${rels}
      <div class="plan"><h4>⚡ Ereignisse</h4><div class="hinweis">Nach jeder Runde wird ein Ereignis gezogen. ${E.schutzAktiv(s) ? `<b>Neulingsschutz:</b> bis zum Ereignis ${E.REGELN().schutz_runden} darf niemand angreifen oder schießen (bisher ${s.ereigZ}).` : 'Der Neulingsschutz ist vorbei – Angriffe sind erlaubt.'} Im Stapel: ${s.ereig.length} Karten.</div></div>
    </div>`;
  }
  logHtml() { return `<div class="log">${s2(this.s.ev).slice().reverse().map(e => `<div>${esc(e.t)}</div>`).join('')}</div>`; }

  // ---------------------------------------------------------------- Modals
  kartenSheetKopf(c, p, extra = '') { const d = def(c); return `<div class="kopfz">${this.karteHtml(c, p, { gross: true })}<div class="info"><h3>${esc(d.name)}</h3><div class="mini">${esc(kartenArt(d))}</div><p>${esc(d.beschreibung || d.flavor || '')}</p>${d.flavor && d.beschreibung !== d.flavor ? `<p class="mini"><i>${esc(d.flavor)}</i></p>` : ''}${braucht(d).length ? `<p class="mini">Braucht: ${braucht(d).map(esc).join(', ')}</p>` : ''}${benoetigt(d).length ? `<p class="mini">Voraussetzung: ${benoetigt(d).map(esc).join(', ')}</p>` : ''}${(d.schluessel || []).filter(k => SCHL_TXT[k]).map(k => `<p class="mini">• ${esc(SCHL_TXT[k])}</p>`).join('')}${extra}</div></div>`; }
  handSheet(id) {
    return () => {
      const s = this.s, p = this.p(this.me), c = p.hand.find(x => x.i === id); if (!c) return null; const d = def(c);
      let btns = '', grund = '', ok = '';
      const mein = this.meinZug() && s.phase === 'aktion';
      if (!mein) grund = s.phase === 'ziehen' && s.am === this.me ? 'Ziehe zuerst deine Karten.' : 'Du bist gerade nicht am Zug.';
      if (d.typ === 'land') { if (mein) { if (p.landG >= E.landErlaubt(p)) grund = 'Du hast dein Land für diesen Zug schon gelegt.'; else btns += `<button data-a="land" data-v="${c.i}">🌾 Land legen</button>`; } }
      else if (d.klasse === 'missionar') {
        if (mein) { if (!p.religion) grund = 'Du brauchst zuerst eine Religion.'; else if (p.gold < E.kosten(p, c)) grund = `Zu wenig Gold (${E.kosten(p, c)} nötig).`; else { const z = E.gegner(s, p).filter(o => !s.missionen.some(m => m.owner === this.me && s.sp[m.host] === o)); if (!z.length) grund = 'Bei allen Gegnern ist schon ein Missionar von dir.'; else btns += z.map(o => `<button class="gruen" data-a="mission" data-v="${c.i}" data-z="${s.sp.indexOf(o)}">Zu ${esc(o.name)} senden (${E.kosten(p, c)}💰)</button>`).join(''); } }
      } else if (d.typ === 'einheit' || d.typ === 'gebaeude') { if (mein) { const g = E.sperrGrund(s, p, c); if (g) grund = g; else { btns += `<button data-a="spiele" data-v="${c.i}">${d.typ === 'gebaeude' ? '🔨 Bauen' : '⚔ Ausbilden'} (${E.kostenGesamt(p, c)} 💰)</button>`; const z = E.zukauf(p, c); if (z) ok = `Enthält ${z} Gold für einen fehlenden Rohstoff.`; } } }
      if (mein && !c.vk) { if (p.ablN >= E.REGELN().ablegen_max) { if (!grund) grund = `Du hast schon ${E.REGELN().ablegen_max} Karten abgelegt.`; } else btns += `<button class="sek" data-a="ablegen" data-v="${c.i}">♻ Ablegen${E.ablegenGold(p, c) ? ' (+' + E.ablegenGold(p, c) + ' 💰)' : ''}</button>`; }
      return `${this.kartenSheetKopf(c, p)}${grund ? `<div class="grund">${esc(grund)}</div>` : ''}${ok ? `<div class="ok">${esc(ok)}</div>` : ''}<div class="btns">${btns}<button class="sek" data-a="zu">Schließen</button></div>`;
    };
  }
  infoSheet(id, pi) {
    return () => { const d = def({ id }); const p = this.p(pi); const c = { id, i: 0 }; return `${this.kartenSheetKopf(c, p)}<div class="btns"><button class="sek" data-a="zu">Schließen</button></div>`; };
  }
  wunderSheet(i) {
    return () => {
      const s = this.s, p = this.p(this.me), w = s.wunderOffen.find(x => x.i === i); if (!w) return null; const d = def(w);
      const mein = this.meinZug() && s.phase === 'aktion'; const g = mein ? E.sperrGrund(s, p, w) : 'Du bist gerade nicht am Zug.';
      return `${this.kartenSheetKopf(w, p)}${g ? `<div class="grund">${esc(g)}</div>` : ''}<div class="btns">${!g ? `<button data-a="wunder" data-v="${w.i}">🏛 Bauen (${E.kostenGesamt(p, w)} 💰)</button>` : ''}<button class="sek" data-a="zu">Schließen</button></div>`;
    };
  }
  staatSheet(i) {
    return () => {
      const s = this.s, p = this.p(this.me), t = s.auslage.find(x => x.i === i); if (!t) return null; const d = def(t);
      const mein = this.meinZug() && s.phase === 'aktion'; const g = !mein ? 'Du bist gerade nicht am Zug.' : p.staaten.length >= 2 ? 'Du hast schon 2 Verbündete.' : p.gold < d.kosten ? `Zu wenig Gold (${d.kosten} nötig).` : '';
      return `<div class="kopfz"><div class="kachel staat" style="width:110px;padding:6px"><div class="ico" style="height:60px">${spr('stadt:stadtstaat', d.farbe, 1)}</div><b>${esc(d.name)}</b></div><div class="info"><h3>${esc(d.name)}</h3><p>${esc(d.beschreibung)}</p><p><b>${this.kurz(d).join(' · ') || 'Hafen: Küste'}</b></p><p class="mini">Schwerpunkt: ${esc(d.schwerpunkt)}</p></div></div>${g ? `<div class="grund">${esc(g)}</div>` : ''}<div class="btns">${!g ? `<button data-a="tribut" data-v="${t.i}">🤝 Tribut zahlen (${d.kosten} 💰)</button>` : ''}<button class="sek" data-a="zu">Schließen</button></div>`;
    };
  }
  gruendenSheet() {
    this.gr = { rel: null, c: null };
    return () => {
      const s = this.s, p = this.p(this.me), D = E.daten(); if (p.religion) return null;
      const ops = p.hand.filter(c => !c.vk && !def(c).relkarte);
      const g = p.gold < 5 ? 'Zu wenig Gold (5 nötig).' : p.alter < 1 ? 'Erst ab Zeitalter II.' : !ops.length ? 'Du brauchst eine Handkarte zum Ablegen.' : '';
      return `<h3>🔥 Religion gründen</h3><p class="mini">5 💰 und 1 Handkarte ablegen. Du kannst nur einmal pro Spiel gründen. Jede Religion ist nur einmal vergeben.</p>
        <div class="religionen">${s.relFrei.map(id => { const r = D.religionen.find(x => x.id === id); return `<div class="relk ${this.gr.rel === id ? '' : ''}" data-a="grel" data-v="${id}" style="--rf:${r.farbe};cursor:pointer;${this.gr.rel === id ? 'outline:4px solid #3f8f4a' : ''}">${spr(`rel:${r.id}:emblem`, r.farbe, 1)}<div><b>${esc(r.name)}</b>${esc(r.titel)}: ${esc(r.text)}</div></div>`; }).join('')}</div>
        <h4>Opfere eine Handkarte:</h4><div class="chips">${ops.map(c => `<span class="chipb ${this.gr.c === c.i ? 'an' : ''}" data-a="gopfer" data-v="${c.i}">${esc(def(c).name)}</span>`).join('')}</div>
        ${g ? `<div class="grund">${g}</div>` : ''}<div class="btns"><button class="gruen" data-a="gruendengo" ${g || !this.gr.rel || !this.gr.c ? 'disabled' : ''}>Gründen</button><button class="sek" data-a="zu">Abbrechen</button></div>`;
    };
  }
  schiessenSheet() {
    return () => {
      const s = this.s, p = this.p(this.me); const sh = [...this.sel].map(i => p.front.find(u => u.i === i)).filter(u => u && E.kannSchiessen(u)); if (!sh.length) return null;
      const u = sh[0], d = def(u); const ziele = E.schussZiele(s, p, u);
      const zs = ziele.map(z => { const o = s.sp[z.p], t = E.einheiten(o).find(x => x.i === z.c); return `<button class="rot" data-a="schuss" data-v="${u.i}" data-z="${z.c}" data-p="${z.p}">${esc(o.name)}: ${esc(def(t).name)} (⚔${def(t).staerke})</button>`; }).join('');
      const st = d.schluessel.includes('belagerung') ? E.gegner(s, p).map(o => `<button class="rot" data-a="schuss" data-v="${u.i}" data-stadt="1" data-p="${s.sp.indexOf(o)}">🏰 Stadt von ${esc(o.name)} (${d.fern + (d.boni.stadt || 0)} Schaden)</button>`).join('') : '';
      return `<h3>🏹 ${esc(d.name)} schießt</h3><p class="mini">Fernkampf ${d.fern}. Die Einheit wird dabei erschöpft${d.schluessel.includes('einmalig') ? ' und verbraucht' : ''}.</p>${E.schutzAktiv(s) ? '<div class="grund">Neulingsschutz: Noch darf niemand schießen.</div>' : `<div class="btns">${zs}${st}${!zs && !st ? '<span class="hinweis">Keine Ziele in Reichweite.</span>' : ''}</div>`}<div class="btns"><button class="sek" data-a="zu">Schließen</button></div>`;
    };
  }
  abwerfenSheet() {
    this.ab = new Set();
    return () => {
      const p = this.p(this.me), zu = E.handZaehlt(p).length - E.handlimit(p); if (zu <= 0) return null;
      return `<h3>Handlimit überschritten</h3><p>Lege <b>${zu}</b> Karte(n) ab (Volkskarten zählen nicht mit):</p><div class="chips">${E.handZaehlt(p).map(c => `<span class="chipb ${this.ab.has(c.i) ? 'an' : ''}" data-a="abw" data-v="${c.i}">${esc(def(c).name)}</span>`).join('')}</div><div class="btns"><button class="gruen" data-a="abwgo" ${this.ab.size === zu ? '' : 'disabled'}>Ablegen & Zug beenden</button><button class="sek" data-a="zu">Zurück</button></div>`;
    };
  }
  ereignisHtml() {
    const s = this.s, e = def({ id: s.letztes.id }), D = E.daten();
    const txt = e.art === 'barbaren' ? `Barbaren (Stärke ${'= Zeitalter + ' + (1 + e.plus)}) greifen den Spieler mit dem schwächsten Heer an. Wer eine Einheit mit mindestens dieser Stärke hat, wehrt sie ab und bekommt ${e.beute} Gold; sonst geht eine Einheit verloren oder die Stadt wird getroffen.` : (e.text ? (Array.isArray(e.text) ? e.text.join(' ') : e.text) : '');
    const spk = e.sprite && hatSprite(e.sprite) ? spr(e.sprite, '#888', 3) : '⚡';
    const log = s.ev.filter(x => x.n >= s.letztes.n).map(x => `<div class="mini">${esc(x.t)}</div>`).join('');
    return `<h3>⚡ Ereignis: ${esc(e.name)}</h3><div class="ereignis-karte"><div>${spk}</div><div>${esc(e.beschreibung || e.flavor || '')}<p class="mini">${esc(txt)}</p></div></div><div style="margin-top:8px">${log}</div><div class="btns"><button data-a="ereigok">Weiter</button></div>`;
  }
  blockHtml() {
    const s = this.s, k = s.kampf, a = s.sp[k.von], o = this.p(this.me);
    const atk = k.atk.map(id => a.front.find(x => x.i === id)).filter(Boolean), used = new Set(Object.values(this.blk).filter(v => v != null));
    const rows = atk.map(u => {
      const ud = def(u), sa = E.staerkeGegen(a, u, null, true), dmg = Math.max(1, ud.staerke + (ud.boni.stadt || 0) + (ud.schluessel.includes('ramme') ? ud.staerke : 0) - E.schutz(o));
      const elig = E.einheiten(o).filter(b => E.kannBlocken(b, u));
      const chips = elig.map(b => { const sb = E.staerkeGegen(o, b, u, false), sa2 = E.staerkeGegen(a, u, b, true), an = this.blk[u.i] === b.i, belegt = used.has(b.i) && !an; const erg = sb > sa2 ? '✅ besiegt ihn' : sb === sa2 ? '⚖ beide fallen' : '💀 fällt'; return `<span class="chipb ${an ? 'an' : ''} ${belegt ? 'aus' : ''}" ${belegt ? '' : `data-a="blk" data-v="${u.i}" data-b="${b.i}"`}>${esc(def(b).name)} ⚔${sb} – ${erg}</span>`; }).join('');
      return `<div class="block-reihe"><div class="oben">${spr(ud.sprite, a.volkF, 2)}<div><b>${esc(ud.name)}</b> ⚔${sa}<div class="mini">Ohne Block: <b>${dmg}</b> Schaden an deiner Stadt (❤ ${o.hp})</div></div></div>${elig.length ? `<div class="chips"><span class="chipb ${this.blk[u.i] == null ? 'an' : ''}" data-a="blk" data-v="${u.i}" data-b="">nicht blocken</span>${chips}</div>` : '<div class="mini">Keine Einheit kann blocken.</div>'}</div>`;
    }).join('');
    return `<h3>⚔ ${esc(a.name)} greift an!</h3><p class="mini">Jeder deiner aufrechten Soldaten blockt höchstens einen Angreifer. Der Stärkere gewinnt, bei Gleichstand fallen beide. Unblockierte Angreifer treffen deine Stadt (minus Schutz).</p>${rows}<div class="btns"><button class="gruen" data-a="blockgo">Verteidigen</button><button class="sek" data-a="blkauto">Vorschlag übernehmen</button></div>`;
  }
  siegHtml() {
    const s = this.s, w = s.sp[s.sieger], gewonnen = s.sieger === this.me;
    const rang = s.sp.map((p, i) => ({ p, i })).sort((x, y) => (y.i === s.sieger) - (x.i === s.sieger) || E.kultur(y.p) - E.kultur(x.p));
    return `<div class="sieg"><h2>${gewonnen ? '🏆 Du hast gewonnen!' : esc(w.name) + ' gewinnt'}</h2><p>Sieg durch <b>${esc(s.grund)}</b> in Runde ${s.runde}.</p>
      <div style="text-align:left">${rang.map(({ p }) => `<div class="stat" style="margin:4px 0;width:100%">${p === w ? '👑' : ''} <b>${esc(p.name)}</b> · ${esc(E.daten().voelker.find(v => v.id === p.volk).name)} · ❤ ${Math.max(0, p.hp)} · 🎭 ${E.kultur(p)}${s.opt.rel ? ' · 🔥 ' + E.glaube(s, p) : ''}</div>`).join('')}</div>
      <div class="btns" style="justify-content:center"><button data-a="neu">Neues Spiel</button><button class="sek" data-a="siegzu">Tisch ansehen</button><button class="sek" data-a="menue">Menü</button></div></div>`;
  }

  // ---------------------------------------------------------------- Klicks
  async klick(e) {
    const t = e.target.closest('[data-a]'); if (!t) return; const a = t.dataset.a, v = t.dataset.v, s = this.s, p = this.p(this.me);
    const sheet = (fn) => { this.modalFn = fn; this.render(); };
    switch (a) {
      case 'tab': this.tab = v === 'ich' || v === 'tisch' || v === 'log' ? v : +v; this.render(); break;
      case 'zu': this.modalFn = null; this.render(); break;
      case 'menue': this.c.menue(); break;
      case 'regeln': this.c.regeln(); break;
      case 'neu': this.c.neu(); break;
      case 'siegzeigen': this.siegZu = false; this.render(); break;
      case 'siegzu': this.siegZu = true; this.modalFn = null; this.render(); break;
      case 'ereigok': this.ereigGesehen = s.letztes.n; this.render(); this.c.weiter?.(); break;
      case 'hand': sheet(this.handSheet(+v)); break;
      case 'info': sheet(this.infoSheet(v, +t.dataset.p)); break;
      case 'wunderinfo': sheet(this.wunderSheet(+v)); break;
      case 'staatinfo': sheet(this.staatSheet(+v)); break;
      case 'ziehe': await this.senden({ t: 'ziehe', stapel: v === 'rel' ? 'rel' : +v }); break;
      case 'land': case 'spiele': case 'ablegen': { const r = await this.senden({ t: a, c: +v }); if (r.ok) { this.modalFn = null; this.render(); } break; }
      case 'mission': { const r = await this.senden({ t: 'mission', c: +v, ziel: +t.dataset.z }); if (r.ok) { this.modalFn = null; this.render(); } break; }
      case 'wunder': { const r = await this.senden({ t: 'wunder', c: +v }); if (r.ok) { this.modalFn = null; this.render(); } break; }
      case 'tribut': { const r = await this.senden({ t: 'tribut', c: +v }); if (r.ok) { this.modalFn = null; this.render(); } break; }
      case 'aufstieg': await this.senden({ t: 'aufstieg' }); break;
      case 'ausweisen': await this.senden({ t: 'ausweisen', c: +v }); break;
      case 'gruenden': sheet(this.gruendenSheet()); break;
      case 'grel': this.gr.rel = v; this.render(); break;
      case 'gopfer': this.gr.c = +v; this.render(); break;
      case 'gruendengo': { const r = await this.senden({ t: 'gruenden', rel: this.gr.rel, c: this.gr.c }); if (r.ok) { this.modalFn = null; this.render(); } break; }
      case 'ende': { if (E.handZaehlt(p).length > E.handlimit(p)) { sheet(this.abwerfenSheet()); break; } await this.senden({ t: 'ende' }); this.sel.clear(); break; }
      case 'abw': { const i = +v; this.ab.has(i) ? this.ab.delete(i) : this.ab.add(i); this.render(); break; }
      case 'abwgo': { const r = await this.senden({ t: 'ende', abwerfen: [...this.ab] }); if (r.ok) { this.modalFn = null; this.sel.clear(); this.render(); } break; }
      case 'einheit': {
        const i = +v, pi = +t.dataset.p;
        if (pi === this.me && t.dataset.w === '1') { this.sel.has(i) ? this.sel.delete(i) : this.sel.add(i); this.render(); }
        else { const o = this.p(pi), u = E.einheiten(o).find(x => x.i === i); if (u) sheet(this.infoSheet(u.id, pi)); }
        break;
      }
      case 'selclear': this.sel.clear(); this.render(); break;
      case 'angriff': { const r = await this.senden({ t: 'angriff', ids: [...this.sel], ziel: +v }); if (r.ok) { this.sel.clear(); if (r.loese) this.toast('Kampf: ' + r.loese.map(x => x.stadt ? `${def({ id: x.a }).name} trifft die Stadt (${x.stadt})` : `${def({ id: x.a }).name} ${x.sa}:${x.sb} ${def({ id: x.b }).name}`).join(' · ')); this.render(); } break; }
      case 'schiessen': sheet(this.schiessenSheet()); break;
      case 'schuss': { const m = t.dataset; const r = await this.senden(m.stadt ? { t: 'schuss', c: +v, stadt: true, p: +m.p } : { t: 'schuss', c: +v, p: +m.p, z: +m.z }); if (r.ok) { this.sel.delete(+v); const rest = [...this.sel].filter(i => p.front.find(u => u.i === i && E.kannSchiessen(u))); if (!rest.length) this.modalFn = null; this.render(); } break; }
      case 'blk': { const ai = +v; if (t.dataset.b === '') this.blk[ai] = null; else this.blk[ai] = +t.dataset.b; this.render(); break; }
      case 'blkauto': this.blk = KI.blockWahl(s, this.me, 'stark').z; this.render(); break;
      case 'blockgo': { const r = await this.senden({ t: 'blocke', z: this.blk }); if (r.ok) this.blk = {}; break; }
    }
  }
}
const EFF_SHORT = { E: '💰', K: '🎭', W: '📖', S: '🛡', H: '❤', A: '⚔−', HL: '✋', G: '🔨−', L: '🌾', Z: '🃏', F: '🔥', ABLEGEN: '♻', SCHIFF: '⚓' };
const s2 = (x) => x;
