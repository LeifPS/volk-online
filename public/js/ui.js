// Spieltisch: zeigt den Zustand (lokal oder online) mit echten Kartenbildern und sendet Aktionen über ctrl.send(a).
import * as E from './engine.js';
import * as KI from './ki.js';
import { spr, ic } from './sprites.js';
import { kk, stapelBild } from './karten.js';
import { kartenArt, braucht, benoetigt, ZA, SCHL_TXT, ROH } from './text.js';
const { def } = E;
const esc = (t) => String(t ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const st = (ico, txt) => `<span>${ic(ico)}${txt}</span>`;

export class Spieltisch {
  constructor(root, overlay, ctrl) {
    this.root = root; this.ov = overlay; this.c = ctrl; this.tab = 'ich'; this.sel = new Set(); this.modalFn = null; this.blk = {}; this.ereigGesehen = 0; this.siegZu = false;
    root.onclick = (e) => this.klick(e); overlay.onclick = (e) => { if (e.target === overlay && !this.erzwungen()) { this.modalFn = null; this.render(); } else this.klick(e); };
  }
  get s() { return this.c.s; } get me() { return this.c.me; }
  p(i) { return this.s.sp[i]; }
  meinZug() { return this.s.am === this.me && this.s.phase !== 'ende' && this.s.phase !== 'block'; }
  erzwungen() { const s = this.s; return s.sieger !== null && !this.siegZu || (s.phase === 'block' && s.kampf.ziel === this.me) || this.ereignisOffen(); }
  ereignisOffen() { const s = this.s; return !!(s.letztes && s.letztes.n > this.ereigGesehen && s.sieger === null); }
  blockiert() { return this.erzwungen() || !!this.modalFn; }
  toast(t) { const d = document.createElement('div'); d.className = 'toast'; d.textContent = t; document.getElementById('toasts').appendChild(d); setTimeout(() => d.remove(), 2600); }
  async senden(a) { const r = await this.c.send(a); if (!r.ok) this.toast(r.fehler || 'Das geht nicht.'); return r; }

  // ---------------------------------------------------------------- Rendering
  render() {
    if (!this.s) return;
    const s = this.s, me = this.p(this.me), D = E.daten();
    if (this.tab !== 'ich' && this.tab !== 'tisch' && this.tab !== 'log' && !(this.tab >= 0 && this.s.sp[this.tab])) this.tab = 'ich';
    const aktiv = s.sp[s.phase === 'block' ? s.kampf.ziel : s.am];
    const ticker = s.ev.slice(-3).map(e => esc(e.t)).join('  ›  ');
    const chips = s.sp.map((p, i) => {
      const v = D.voelker.find(x => x.id === p.volk);
      return `<div class="chip ${i === s.am && s.sieger === null ? 'aktiv' : ''} ${String(this.tab) === String(i) || (i === this.me && this.tab === 'ich') ? 'sel' : ''} ${p.tot ? 'tot' : ''}" data-a="tab" data-v="${i === this.me ? 'ich' : i}">
        <div class="n"><span class="pt" style="background:${v.farbe}"></span>${esc(p.name)}${p.ki ? ic('x:roboter') : ''}</div>
        <div class="w">${st('ui:hp', Math.max(0, p.hp))}${st('ui:kultur', E.kultur(p) + '/' + E.REGELN().kultur_sieg)}${s.opt.rel ? st('rel:glaube', E.glaube(s, p) + '/' + s.glaubeZiel) : ''}${st('x:karten', p.hand.length)}</div></div>`;
    }).join('');
    const tabs = [['ich', 'Mein Reich'], ['tisch', 'Tisch'], ...s.sp.map((p, i) => i === this.me ? null : [i, p.name]).filter(Boolean), ['log', 'Verlauf']]
      .map(([k, n]) => `<button class="${String(this.tab) === String(k) ? 'an' : ''}" data-a="tab" data-v="${k}">${esc(n)}</button>`).join('');
    let inhalt = '';
    if (this.tab === 'ich') inhalt = this.reichHtml(this.me); else if (this.tab === 'tisch') inhalt = this.tischHtml(); else if (this.tab === 'log') inhalt = this.logHtml(); else inhalt = this.reichHtml(+this.tab);
    const stp = this.buehne ? this.buehne.scrollTop : 0, hs = this.handEl ? this.handEl.scrollLeft : 0;
    const av = D.voelker.find(x => x.id === aktiv.volk);
    this.root.innerHTML = `<div class="spiel">
      <div class="kopf"><div class="titel"><span class="punkt" style="background:${av.farbe}"></span>RUNDE ${s.runde} · ${esc(aktiv.name)}${s.am === this.me && s.phase !== 'block' ? ' (DU)' : ''}</div>
        <button data-a="regeln" aria-label="Regeln">${ic('ui:hilfe')}</button><button data-a="menue" aria-label="Menü">${ic('ui:menue')}</button></div>
      <div class="ticker">${ticker || '&nbsp;'}</div>
      <div class="leiste">${chips}</div>
      <div class="tabs">${tabs}</div>
      <div class="buehne">${inhalt}</div>
      <div class="dock">${this.aktionsHtml()}<div class="hand ${me.hand.length ? '' : 'leer'}">${this.handHtml()}</div></div></div>`;
    this.buehne = this.root.querySelector('.buehne'); this.buehne.scrollTop = stp; this.handEl = this.root.querySelector('.hand'); this.handEl.scrollLeft = hs;
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
  fenster(titel, inhalt, zu = true) { return `<div class="fk"><h3>${titel}</h3>${zu ? `<button class="knopf" data-a="zu" aria-label="Schließen" style="min-height:32px;padding:3px 8px">${ic('ui:kreuz')}</button>` : ''}</div><div class="fi">${inhalt}</div>`; }

  // ---------------------------------------------------------------- Karten
  handHtml() {
    const me = this.p(this.me), s = this.s; if (!me.hand.length) return 'Keine Handkarten.';
    const ord = (c) => { const d = def(c); return (c.vk ? 0 : d.relkarte ? 2 : 1) * 10 + ({ land: 0, einheit: 1, gebaeude: 2 }[d.typ] ?? 3); };
    return me.hand.slice().sort((a, b) => ord(a) - ord(b)).map(c => {
      const d = def(c), mein = this.meinZug() && s.phase === 'aktion', ok = mein && this.spielbar(c);
      let badge = ''; if (d.typ === 'einheit' || d.typ === 'gebaeude') { const k = E.kostenGesamt(me, c); badge = `${ic('ui:gold')}${k === null ? ic('ui:kreuz') : k}`; }
      return kk(c, { a: 'hand', cls: ok ? 'spielbar' : (mein ? 'dim' : ''), badge, eager: true });
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
    if (s.am !== this.me) return `<div class="aktionen"><div class="info">${esc(this.p(s.am).name)} ist am Zug · <span>${ic('ui:gold')}<b>${p.gold}</b></span></div></div>`;
    if (s.phase === 'ziehen') {
      const piles = [1, 2, 3].filter(k => k <= E.maxStapel(p)).map(k => stapelBild('rueck_' + k, s.stapel[k].length, { a: 'ziehe', v: k, cls: 'zieh', unten: 'STAPEL ' + ZA[k - 1] })).join('');
      const rel = p.religion && p.relStapel.length && !p.relBenutzt ? stapelBild('rueck_r_' + p.religion, p.relStapel.length, { a: 'ziehe', v: 'rel', cls: 'zieh', unten: 'GLAUBE' }) : '';
      return `<div class="aktionen"><div class="info">Ziehe noch <b>${s.zieh}</b> Karte(n). Tippe auf einen Stapel. <span>${ic('ui:gold')}<b>${p.gold}</b></span></div><div class="zieher">${piles}${rel}</div></div>`;
    }
    const ak = E.aufstiegKosten(p);
    const auswahl = [...this.sel].map(i => E.einheiten(p).find(u => u.i === i)).filter(Boolean);
    let b = '';
    if (auswahl.length) {
      b += E.gegner(s, p).map(o => `<button class="rot" data-a="angriff" data-v="${s.sp.indexOf(o)}" ${E.schutzAktiv(s) ? 'disabled' : ''}>${ic('ui:staerke')}Angriff: ${esc(o.name)}</button>`).join('');
      if (auswahl.some(E.kannSchiessen)) b += `<button class="rot" data-a="schiessen">${ic('ui:fernkampf')}Schießen</button>`;
      b += `<button class="sek" data-a="selclear">Abwählen</button>`;
    } else {
      if (ak !== null) b += `<button data-a="aufstieg" ${p.gold < ak || p.aufN ? 'disabled' : ''}>${ic('ui:befoerderung')}Zeitalter ${ZA[p.alter + 1]} <small>(${ak} ${ic('ui:gold')})</small></button>`;
      if (s.opt.rel && !p.religion && p.alter >= 1) b += `<button class="sek" data-a="gruenden">${ic('rel:glaube')}Religion gründen <small>(5 ${ic('ui:gold')})</small></button>`;
      b += `<button class="gruen" data-a="ende">Zug beenden${ic('ui:pfeil_rechts')}</button>`;
    }
    const info = auswahl.length ? `${auswahl.length} Einheit(en) gewählt${E.schutzAktiv(s) ? ' · Neulingsschutz: noch kein Angriff' : ''}` : `<span>${ic('ui:gold')}<b>${p.gold}</b></span><span>Einkommen +${E.einkommen(s, p)}</span><span>Land ${p.landG}/${E.landErlaubt(p)}</span>`;
    return `<div class="aktionen"><div class="info">${info}</div>${b}</div>`;
  }

  // ---------------------------------------------------------------- Reich (Volkstafel + Karten auf dem Tisch)
  tafelHtml(p, isMe) {
    const s = this.s, R = E.REGELN(), D = E.daten(), v = D.voelker.find(x => x.id === p.volk), rel = p.religion ? D.religionen.find(r => r.id === p.religion) : null;
    const hp = Math.max(0, Math.min(R.stadt_hp, p.hp)), k = Math.min(R.kultur_sieg, E.kultur(p)), ak = E.aufstiegKosten(p);
    const zellen = (n, voll, kl) => Array.from({ length: n }, (_, i) => `<i class="${kl} ${i < voll ? 'an' : ''}"></i>`).join('');
    const zeit = ZA.map((r, i) => `<div class="zz ${i < p.alter ? 'vorbei' : ''} ${i === p.alter ? 'jetzt' : ''}"><b>${r}</b>${i === p.alter + 1 && ak !== null ? `<small>${ak}${ic('ui:gold')}</small>` : ''}</div>`).join('');
    const kz = Array.from({ length: R.kultur_sieg }, (_, i) => `<i class="kz ${i < k ? 'an' : ''} ${i === R.kultur_sieg - 1 ? 'sieg' : ''}">${i === R.kultur_sieg - 1 ? ic('ui:krone') : ''}</i>`).join('');
    const chip = (ico, w, kl, sub) => `<div class="tchip ${kl || ''}">${ic(ico)}<b>${w}</b>${sub ? `<small>${sub}</small>` : ''}</div>`;
    return `<div class="tableau" style="--vf:${v.farbe}">
      <div class="tk"><div class="tstadt">${spr('stadt:stadtstaat', p.volkF, 2)}</div><div class="tname"><div class="vn">${esc(p.name)}</div><div class="mini">${esc(v.name)} · ${esc(v.herrscher)}</div></div>${isMe ? '' : `<div class="mini" style="margin-left:auto">${ic('x:karten')} ${p.hand.length}</div>`}</div>
      <div class="tfa"><b>Volksfähigkeit</b> ${v.text.map(esc).join(' ')}${rel ? `<br><b>${esc(rel.name)}:</b> ${esc(rel.text)}` : ''}</div>
      <div class="tzeile"><div class="tl">${ic('ui:hp')} Lebenspunkte <b>${hp}/${R.stadt_hp}</b></div><div class="tleiste hp">${zellen(R.stadt_hp, hp, 'hz')}</div></div>
      <div class="tzeile"><div class="tl">${ic('ui:kultur')} Kultur <b>${E.kultur(p)}/${R.kultur_sieg}</b> <small>(${R.kultur_sieg} = Sieg)</small></div><div class="tleiste kultur">${kz}</div></div>
      <div class="tzeile"><div class="tl">${ic('ui:zeitalter')} Zeitalter <b>${ZA[p.alter]}</b>${ak !== null ? ` <small>nächster Aufstieg: ${ak} Gold, einmal pro Runde</small>` : ''}</div><div class="tleiste zeit">${zeit}</div></div>
      <div class="tchips">${chip('ui:gold', p.gold, 'gold', '+' + E.einkommen(s, p) + '/Runde')}${chip('ui:schild', E.schutz(p), '', 'Schutz')}${chip('x:karten', p.hand.length, '', isMe ? '/' + E.handlimit(p) : '')}${s.opt.rel && p.religion ? chip('rel:glaube', E.glaube(s, p), '', '/' + s.glaubeZiel) : ''}${chip('ui:gruenden', p.land.length, '', 'Land')}</div></div>`;
  }
  reichHtml(pi) {
    const s = this.s, p = this.p(pi), D = E.daten(), isMe = pi === this.me;
    const v = D.voelker.find(x => x.id === p.volk), rel = p.religion ? D.religionen.find(r => r.id === p.religion) : null;
    const aktion = isMe && this.meinZug() && s.phase === 'aktion';
    const karten = (arr, o = {}) => arr.map(c => kk(c, { a: 'info', data: { p: pi }, v: c.id, ...o })).join('');
    const reihe = (arr, leer, o) => `<div class="reihe ${arr.length > 5 ? 'dicht' : ''}">${arr.length ? karten(arr, o) : `<span class="leer">${leer}</span>`}</div>`;
    const einh = (arr, neu) => arr.map(u => {
      const d = def(u), waehlbar = aktion && E.kannAngreifen(u) && !neu;
      return kk(u, { a: 'einheit', v: u.i, data: { p: pi, w: waehlbar ? 1 : 0, id: u.id }, gedreht: !!u.t, cls: `${this.sel.has(u.i) ? 'sel' : ''} ${neu ? 'neu' : ''}`, unten: u.t ? 'erschöpft' : '' });
    }).join('');
    const mis = E.missionenBei(s, p), meine = E.missionenAus(s, p);
    const misHtml = (list, wohin) => list.map(m => { const o = s.sp[wohin ? m.host : m.owner], r = D.religionen.find(x => x.id === s.sp[m.owner].religion); return `<span class="mis">${spr(`rel:${r.id}:missionar`, r.farbe, 1)}${wohin ? 'zu ' : 'von '}${esc(o.name)}${!wohin && isMe && aktion ? `<button data-a="ausweisen" data-v="${m.c.i}">Ausweisen (${p.religion === 'flammenorden' ? 1 : 2} ${ic('ui:gold')})</button>` : ''}</span>`; }).join('');
    const hand = !isMe && p.hand.length ? `<div class="abschnitt"><h4>${ic('x:karten')} Handkarten <span class="mini">(${p.hand.length})</span></h4><div class="reihe dicht">${p.hand.map(() => kk({ id: '?' }, { rueck: 'rueck_1' })).join('')}</div></div>` : '';
    return `<div>
      ${this.tafelHtml(p, isMe)}
      <div class="abschnitt"><h4>${ic('ui:bau')} Gebäude, Wunder & Verbündete</h4>${reihe([...p.geb, ...p.wunder, ...p.staaten], 'Noch nichts gebaut. Spiele Karten aus deiner Hand.')}</div>
      <div class="abschnitt"><h4>${ic('ui:gruenden')} Land <span class="mini">(${p.land.length})</span></h4>${reihe(p.land, 'Noch kein Land.')}</div>
      <div class="abschnitt"><h4>${ic('ui:staerke')} Heer an der Front</h4><div class="reihe">${p.front.length ? einh(p.front) : '<span class="leer">Keine Einheiten an der Front.</span>'}</div></div>
      ${p.kaserne.length ? `<div class="abschnitt"><h4>${ic('ui:lager')} Kaserne <span class="mini">(rückt im nächsten Zug an die Front)</span></h4><div class="reihe">${einh(p.kaserne, true)}</div></div>` : ''}
      ${s.opt.rel && (mis.length || meine.length || p.religion) ? `<div class="abschnitt"><h4>${ic('rel:glaube')} Glaube</h4>${rel ? `<div class="reihe">${kk({ id: 'reltafel_' + rel.id }, { a: 'info', v: 'reltafel_' + rel.id, data: { p: pi } })}</div>` : ''}
        ${mis.length ? `<div class="note">Fremde Missionare in dieser Stadt senken den Glauben:<br>${misHtml(mis, false)}</div>` : ''}${meine.length ? `<div class="note">Entsandte Missionare:<br>${misHtml(meine, true)}</div>` : ''}</div>` : ''}
      ${hand}</div>`;
  }

  // ---------------------------------------------------------------- Tisch (gemeinsam)
  tischHtml() {
    const s = this.s, p = this.p(this.me), D = E.daten(), R = E.REGELN();
    const aktion = this.meinZug() && s.phase === 'aktion', ziehen = this.meinZug() && s.phase === 'ziehen';
    const wun = s.wunderOffen.map(w => kk(w, { a: 'wunderinfo', v: w.i, cls: aktion && !E.sperrGrund(s, p, w) ? 'spielbar' : '', badge: `${ic('ui:gold')}${E.kostenGesamt(p, w) ?? '-'}` })).join('');
    const sta = s.auslage.map(t => kk(t, { a: 'staatinfo', v: t.i, badge: `${ic('ui:gold')}${def(t).kosten}` })).join('');
    const stp = [1, 2, 3].map(k => stapelBild('rueck_' + k, s.stapel[k].length, { a: ziehen && k <= E.maxStapel(p) ? 'ziehe' : '', v: k, cls: `${k > E.maxStapel(p) ? 'aus' : ''} ${ziehen && k <= E.maxStapel(p) ? 'zieh' : ''}`, unten: `STAPEL ${ZA[k - 1]}` })).join('')
      + stapelBild('rueck_0', s.ereig.length, { unten: 'EREIGNISSE' });
    const rels = s.opt.rel ? `<div class="abschnitt"><h4>${ic('rel:glaube')} Religionen <span class="mini">(gründen ab Zeitalter II · 5 Gold + 1 Handkarte)</span></h4><div class="reihe">${D.religionen.map(r => { const frei = s.relFrei.includes(r.id), inh = s.sp.find(x => x.religion === r.id); return kk({ id: 'reltafel_' + r.id }, { a: 'info', v: 'reltafel_' + r.id, data: { p: this.me }, cls: frei ? '' : 'aus', badge: frei ? 'frei' : esc(inh.name) }); }).join('')}</div></div>` : '';
    return `<div>
      <div class="abschnitt"><h4>${ic('ui:wunder')} Weltwunder <span class="mini">(tippen zum Bauen)</span></h4><div class="reihe">${wun || '<span class="leer">Alle Wunder sind gebaut.</span>'}</div></div>
      <div class="abschnitt"><h4>${ic('ui:stadt')} Stadtstaaten <span class="mini">(Tribut ${R.tribut_kosten} Gold · höchstens 2 Verbündete)</span></h4><div class="reihe">${sta || '<span class="leer">Keine Stadtstaaten mehr.</span>'}</div></div>
      <div class="abschnitt"><h4>${ic('x:karten')} Kartenstapel</h4><div class="stapel-reihe">${stp}</div>${p.religion ? `<div class="note">Dein Glaubensstapel: ${p.relStapel.length} Karten.</div>` : ''}</div>
      ${rels}
      <div class="note">${ic('x:blitz')} Nach jeder Runde wird ein Ereignis aufgedeckt. ${E.schutzAktiv(s) ? `<b>Neulingsschutz:</b> bis zum Ereignis ${R.schutz_runden} darf niemand angreifen oder schießen (bisher ${s.ereigZ}).` : 'Der Neulingsschutz ist vorbei, Angriffe sind erlaubt.'}</div></div>`;
  }
  logHtml() { return `<div class="log pix">${this.s.ev.slice().reverse().map(e => `<div>${esc(e.t)}</div>`).join('')}</div>`; }

  // ---------------------------------------------------------------- Fenster
  kartenSheetKopf(c, p) {
    const d = def(c);
    return `<div class="gross">${kk(c, { eager: true, cls: 'x' })}</div><div class="info">${braucht(d).length ? `<p class="mini">Braucht: ${braucht(d).map(esc).join(', ')}</p>` : ''}${benoetigt(d).length ? `<p class="mini">Voraussetzung: ${benoetigt(d).map(esc).join(', ')}</p>` : ''}</div>`;
  }
  handSheet(id) {
    return () => {
      const s = this.s, p = this.p(this.me), c = p.hand.find(x => x.i === id); if (!c) return null; const d = def(c);
      let btns = '', grund = '', ok = '';
      const mein = this.meinZug() && s.phase === 'aktion';
      if (!mein) grund = s.phase === 'ziehen' && s.am === this.me ? 'Ziehe zuerst deine Karten.' : 'Du bist gerade nicht am Zug.';
      if (d.typ === 'land') { if (mein) { if (p.landG >= E.landErlaubt(p)) grund = 'Du hast dein Land für diesen Zug schon gelegt.'; else btns += `<button class="gruen" data-a="land" data-v="${c.i}">${ic('ui:gruenden')}Land legen</button>`; } }
      else if (d.klasse === 'missionar') {
        if (mein) { if (!p.religion) grund = 'Du brauchst zuerst eine Religion.'; else if (p.gold < E.kosten(p, c)) grund = `Zu wenig Gold (${E.kosten(p, c)} nötig).`; else { const z = E.gegner(s, p).filter(o => !s.missionen.some(m => m.owner === this.me && s.sp[m.host] === o)); if (!z.length) grund = 'Bei allen Gegnern ist schon ein Missionar von dir.'; else btns += z.map(o => `<button class="gruen" data-a="mission" data-v="${c.i}" data-z="${s.sp.indexOf(o)}">Zu ${esc(o.name)} senden (${E.kosten(p, c)} ${ic('ui:gold')})</button>`).join(''); } }
      } else if (d.typ === 'einheit' || d.typ === 'gebaeude') { if (mein) { const g = E.sperrGrund(s, p, c); if (g) grund = g; else { btns += `<button class="gruen" data-a="spiele" data-v="${c.i}">${d.typ === 'gebaeude' ? ic('ui:bau') + 'Bauen' : ic('ui:einheit') + 'Ausbilden'} (${E.kostenGesamt(p, c)} ${ic('ui:gold')})</button>`; const z = E.zukauf(p, c); if (z) ok = `Enthält ${z} Gold für einen fehlenden Rohstoff.`; } } }
      if (mein && !c.vk) { if (p.ablN >= E.REGELN().ablegen_max) { if (!grund) grund = `Du hast schon ${E.REGELN().ablegen_max} Karten abgelegt.`; } else btns += `<button class="sek" data-a="ablegen" data-v="${c.i}">${ic('ui:handel')}Ablegen${E.ablegenGold(p, c) ? ' (+' + E.ablegenGold(p, c) + ' ' + ic('ui:gold') + ')' : ''}</button>`; }
      return this.fenster(esc(d.name), `${this.kartenSheetKopf(c, p)}${grund ? `<div class="grund">${esc(grund)}</div>` : ''}${ok ? `<div class="ok">${esc(ok)}</div>` : ''}<div class="btns">${btns}</div>`);
    };
  }
  infoSheet(id, pi) { return () => { const d = def({ id }) || { name: 'Karte' }; const c = { id, i: 0 }; return this.fenster(esc(d.name), this.kartenSheetKopf(c, this.p(pi))); }; }
  wunderSheet(i) {
    return () => {
      const s = this.s, p = this.p(this.me), w = s.wunderOffen.find(x => x.i === i); if (!w) return null; const d = def(w);
      const mein = this.meinZug() && s.phase === 'aktion'; const g = mein ? E.sperrGrund(s, p, w) : 'Du bist gerade nicht am Zug.';
      return this.fenster(esc(d.name), `${this.kartenSheetKopf(w, p)}${g ? `<div class="grund">${esc(g)}</div>` : ''}<div class="btns">${!g ? `<button class="gruen" data-a="wunder" data-v="${w.i}">${ic('ui:wunder')}Bauen (${E.kostenGesamt(p, w)} ${ic('ui:gold')})</button>` : ''}</div>`);
    };
  }
  staatSheet(i) {
    return () => {
      const s = this.s, p = this.p(this.me), t = s.auslage.find(x => x.i === i); if (!t) return null; const d = def(t);
      const mein = this.meinZug() && s.phase === 'aktion'; const g = !mein ? 'Du bist gerade nicht am Zug.' : p.staaten.length >= 2 ? 'Du hast schon 2 Verbündete.' : p.gold < d.kosten ? `Zu wenig Gold (${d.kosten} nötig).` : '';
      return this.fenster(esc(d.name), `${this.kartenSheetKopf(t, p)}${g ? `<div class="grund">${esc(g)}</div>` : ''}<div class="btns">${!g ? `<button class="gruen" data-a="tribut" data-v="${t.i}">${ic('ui:tribut')}Tribut zahlen (${d.kosten} ${ic('ui:gold')})</button>` : ''}</div>`);
    };
  }
  gruendenSheet() {
    this.gr = { rel: null, c: null };
    return () => {
      const s = this.s, p = this.p(this.me), D = E.daten(); if (p.religion) return null;
      const ops = p.hand.filter(c => !c.vk && !def(c).relkarte);
      const g = p.gold < 5 ? 'Zu wenig Gold (5 nötig).' : p.alter < 1 ? 'Erst ab Zeitalter II.' : !ops.length ? 'Du brauchst eine Handkarte zum Ablegen.' : '';
      return this.fenster(`${ic('rel:glaube')} Religion gründen`, `<p class="mini">5 Gold und 1 Handkarte ablegen. Du kannst nur einmal pro Spiel gründen. Jede Religion ist nur einmal vergeben.</p>
        <h4>Wähle eine Religion:</h4><div class="gr-reihe">${s.relFrei.map(id => kk({ id: 'reltafel_' + id }, { a: 'grel', v: id, cls: this.gr.rel === id ? 'an' : '' })).join('')}</div>
        <h4>Opfere eine Handkarte:</h4><div class="chips">${ops.map(c => `<span class="chipb ${this.gr.c === c.i ? 'an' : ''}" data-a="gopfer" data-v="${c.i}">${esc(def(c).name)}</span>`).join('')}</div>
        ${g ? `<div class="grund">${g}</div>` : ''}<div class="btns"><button class="gruen" data-a="gruendengo" ${g || !this.gr.rel || !this.gr.c ? 'disabled' : ''}>Gründen</button><button class="sek" data-a="zu">Abbrechen</button></div>`, false);
    };
  }
  schiessenSheet() {
    return () => {
      const s = this.s, p = this.p(this.me); const sh = [...this.sel].map(i => p.front.find(u => u.i === i)).filter(u => u && E.kannSchiessen(u)); if (!sh.length) return null;
      const u = sh[0], d = def(u); const ziele = E.schussZiele(s, p, u);
      const zs = ziele.map(z => { const o = s.sp[z.p], t = E.einheiten(o).find(x => x.i === z.c); return `<button class="rot" data-a="schuss" data-v="${u.i}" data-z="${z.c}" data-p="${z.p}">${esc(o.name)}: ${esc(def(t).name)} (${ic('ui:staerke')}${def(t).staerke})</button>`; }).join('');
      const stt = d.schluessel.includes('belagerung') ? E.gegner(s, p).map(o => `<button class="rot" data-a="schuss" data-v="${u.i}" data-stadt="1" data-p="${s.sp.indexOf(o)}">${ic('ui:stadt')}Stadt von ${esc(o.name)} (${d.fern + (d.boni.stadt || 0)} Schaden)</button>`).join('') : '';
      return this.fenster(`${ic('ui:fernkampf')} ${esc(d.name)} schießt`, `<p class="mini">Fernkampf ${d.fern}. Die Einheit wird dabei erschöpft${d.schluessel.includes('einmalig') ? ' und verbraucht' : ''}.</p>${E.schutzAktiv(s) ? '<div class="grund">Neulingsschutz: Noch darf niemand schießen.</div>' : `<div class="btns">${zs}${stt}${!zs && !stt ? '<span class="hinweis">Keine Ziele in Reichweite.</span>' : ''}</div>`}`);
    };
  }
  abwerfenSheet() {
    this.ab = new Set();
    return () => {
      const p = this.p(this.me), zu = E.handZaehlt(p).length - E.handlimit(p); if (zu <= 0) return null;
      return this.fenster('Handlimit überschritten', `<p>Lege <b>${zu}</b> Karte(n) ab (Volkskarten zählen nicht mit):</p><div class="chips">${E.handZaehlt(p).map(c => `<span class="chipb ${this.ab.has(c.i) ? 'an' : ''}" data-a="abw" data-v="${c.i}">${esc(def(c).name)}</span>`).join('')}</div><div class="btns"><button class="gruen" data-a="abwgo" ${this.ab.size === zu ? '' : 'disabled'}>Ablegen & Zug beenden</button><button class="sek" data-a="zu">Zurück</button></div>`, false);
    };
  }
  ereignisHtml() {
    const s = this.s, e = def({ id: s.letztes.id });
    const log = s.ev.filter(x => x.n >= s.letztes.n).map(x => `<div class="mini">${esc(x.t)}</div>`).join('');
    return this.fenster(`${ic('x:blitz')} Ereignis: ${esc(e.name)}`, `<div class="ereignis-wrap"><div class="gross">${kk({ id: s.letztes.id }, { eager: true })}</div><div style="flex:1;min-width:180px">${log}</div></div><div class="btns"><button class="gruen" data-a="ereigok">Weiter${ic('ui:pfeil_rechts')}</button></div>`, false);
  }
  blockHtml() {
    const s = this.s, k = s.kampf, a = s.sp[k.von], o = this.p(this.me);
    const atk = k.atk.map(id => a.front.find(x => x.i === id)).filter(Boolean), used = new Set(Object.values(this.blk).filter(v => v != null));
    const rows = atk.map(u => {
      const ud = def(u), sa = E.staerkeGegen(a, u, null, true), dmg = Math.max(1, ud.staerke + (ud.boni.stadt || 0) + (ud.schluessel.includes('ramme') ? ud.staerke : 0) - E.schutz(o));
      const elig = E.einheiten(o).filter(b => E.kannBlocken(b, u));
      const wahl = elig.map(b => { const sb = E.staerkeGegen(o, b, u, false), sa2 = E.staerkeGegen(a, u, b, true), an = this.blk[u.i] === b.i, belegt = used.has(b.i) && !an; const erg = sb > sa2 ? `${ic('ui:haken')}Sieg` : sb === sa2 ? `${ic('x:waage')}Gleich` : `${ic('x:totenkopf')}Fällt`; return kk(b, { a: 'blk', v: u.i, data: { b: b.i }, cls: `${an ? 'an' : ''} ${belegt ? 'aus' : ''}`, badge: `${ic('ui:staerke')}${sb} ${erg}` }); }).join('');
      return `<div class="block-reihe"><div class="oben">${kk(u, { cls: 'rot' })}<div><b>${esc(ud.name)}</b> ${ic('ui:staerke')}${sa}<div class="mini">Ohne Block: <b>${dmg}</b> Schaden an deiner Stadt (${ic('ui:hp')}${o.hp})</div></div></div>
        ${elig.length ? `<div class="wahl">${wahl}<button class="chipb nein ${this.blk[u.i] == null ? 'an' : ''}" data-a="blk" data-v="${u.i}" data-b="">Nicht blocken</button></div>` : '<div class="mini">Keine Einheit kann blocken.</div>'}</div>`;
    }).join('');
    return this.fenster(`${ic('ui:staerke')} ${esc(a.name)} greift an!`, `<p class="mini">Jeder deiner aufrechten Soldaten blockt höchstens einen Angreifer. Der Stärkere gewinnt, bei Gleichstand fallen beide. Unblockierte Angreifer treffen deine Stadt (minus Schutz).</p>${rows}<div class="btns"><button class="gruen" data-a="blockgo">Verteidigen</button><button class="sek" data-a="blkauto">Vorschlag übernehmen</button></div>`, false);
  }
  siegHtml() {
    const s = this.s, w = s.sp[s.sieger], gewonnen = s.sieger === this.me;
    const rang = s.sp.map((p, i) => ({ p, i })).sort((x, y) => (y.i === s.sieger) - (x.i === s.sieger) || E.kultur(y.p) - E.kultur(x.p));
    return this.fenster('Spielende', `<div class="sieg"><div style="transform:scale(2);margin:10px 0 18px">${ic('ui:krone')}</div><h2>${gewonnen ? 'Du hast gewonnen!' : esc(w.name) + ' gewinnt'}</h2><p>Sieg durch <b>${esc(s.grund)}</b> in Runde ${s.runde}.</p>
      <div class="rang">${rang.map(({ p }) => `<div class="stat">${p === w ? ic('ui:krone') : ''}<b>${esc(p.name)}</b><small>${esc(E.daten().voelker.find(v => v.id === p.volk).name)}</small><span style="margin-left:auto">${ic('ui:hp')}${Math.max(0, p.hp)} ${ic('ui:kultur')}${E.kultur(p)}${s.opt.rel ? ' ' + ic('rel:glaube') + E.glaube(s, p) : ''}</span></div>`).join('')}</div>
      <div class="btns" style="justify-content:center"><button class="gruen" data-a="neu">Neues Spiel</button><button class="sek" data-a="siegzu">Tisch ansehen</button><button class="sek" data-a="menue">Menü</button></div></div>`, false);
  }
  // ---------------------------------------------------------------- Klicks
  async klick(e) {
    const t = e.target.closest('[data-a]'); if (!t || !t.dataset.a) return; const a = t.dataset.a, v = t.dataset.v, s = this.s, p = this.p(this.me);
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
        else sheet(this.infoSheet(t.dataset.id, pi));
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
export const lexikonKarte = (id, o = {}) => kk({ id, st: o.st || 1 }, { a: o.a, v: o.v, cls: o.cls });
