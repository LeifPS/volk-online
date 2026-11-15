// Regeln, Bedienung, Völker, Religionen und Karten-Lexikon
import * as E from './engine.js';
import { spr, ic } from './sprites.js';
import { lexikonKarte } from './ui.js';
import { SCHL, SCHL_TXT, ZA, kartenArt, braucht, benoetigt } from './text.js';
const esc = (t) => String(t ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const li = (...a) => `<ul>${a.map(x => `<li>${x}</li>`).join('')}</ul>`;

function grundspiel(D) {
  const R = D.regeln;
  return `<h2>Worum geht es?</h2><p>Du führst ein Volk durch <b>sieben Zeitalter</b> – von der Antike bis zur Atomzeit. Du legst Land, baust Gebäude, bildest Einheiten aus, kaufst Weltwunder und gewinnst Stadtstaaten als Verbündete. Wer als Erste/r <b>${R.kultur_sieg} Kultur</b> erreicht, gewinnt – oder wer als Letzte/r übrig bleibt.</p>
  <h2>Start</h2>${li(`Du hast <b>${R.start_gold} Gold</b>, <b>${R.stadt_hp} Lebenspunkte</b> (${ic('ui:hp')}) und ${R.start_hand} Handkarten vom Stapel I.`, 'Es gibt <b>3 Kartenstapel</b> (I, II, III), 8 Weltwunder (3 liegen offen) und 12 Stadtstaaten (3 liegen offen).', 'Jedes Volk hat eine eigene Fähigkeit (Reiter „Völker“).')}
  <h2>Dein Zug</h2>
  <h3>1 · Aufwecken</h3><p>Alle erschöpften Einheiten stehen wieder auf. Einheiten aus der <b>Kaserne</b> rücken an die <b>Front</b>. Deine Stadt heilt Lebenspunkte (Gebäude und Sanitäter).</p>
  <h3>2 · Einkommen</h3><p>Du bekommst automatisch <b>${R.basis_einkommen} + Zeitalter-Nummer</b> (I = 0 … VII = 6) <b>+ Ertrag aller Länder + Einkommen</b> von Gebäuden, Wundern, Verbündeten und Händlern. Gold hat keine Obergrenze.</p>
  <h3>3 · Ziehen</h3><p>Ziehe <b>${R.ziehen} Karten</b>. Du darfst vom Stapel deines Zeitalters oder von einem niedrigeren ziehen: Zeitalter I–II → Stapel I, III–IV → Stapel II, V–VII → Stapel III. Du kannst die Karten auf mehrere Stapel verteilen.</p>
  <h3>4 · Aktionen</h3><p>In beliebiger Reihenfolge und so oft du magst:</p>
  ${li('<b>Land</b> legen – eine Karte pro Zug, gratis. Land bringt dauerhaft Gold und Rohstoff-Symbole.', '<b>Karte spielen</b> (Tippen auf die Handkarte): Goldkosten zahlen. Das Zeitalter der Karte darf nicht höher sein als deins. Einheiten kommen in die Kaserne, Gebäude in dein Reich (jedes Gebäude nur einmal).', `<b>Wunder bauen</b> (Reiter „Tisch“): Gold zahlen, Rohstoff und Zeitalter müssen passen.`, `<b>Aufstieg</b> ins nächste Zeitalter: ${R.aufstieg.join(' / ')} Gold (Kosten für I→II, II→III …).`, `<b>Tribut</b>: ${R.tribut_kosten} Gold an einen offenen Stadtstaat – er wird dein Verbündeter (höchstens 2).`, `<b>Ablegen für Gold</b>: bis zu ${R.ablegen_max} Handkarten, je ${R.ablegen_gold} Gold.`, '<b>Angreifen oder schießen</b> (siehe Kampf).')}
  <h3>5 · Zugende</h3><p>Du darfst höchstens <b>${R.handlimit} Handkarten</b> behalten – den Rest legst du ab. Wenn alle gespielt haben, wird <b>ein Ereignis</b> aufgedeckt.</p>
  <h2>Rohstoffe</h2><p>Viele Karten „brauchen“ Symbole (Holz, Stein, Marmor, Eisen, Pferde …). Du besitzt ein Symbol, wenn eines deiner Länder, Gebäude oder Verbündeten es liefert. Symbole werden <b>nicht verbraucht</b>. Fehlt genau ein Symbol, kaufst du es für <b>${R.zukauf_preis} Gold</b> automatisch dazu. Küste und Flugfeld kann man nicht kaufen.</p>
  <h2>Kampf</h2>${li(`<b>Neulingsschutz:</b> Bis ${R.schutz_runden} Ereignisse aufgedeckt wurden, darf niemand angreifen oder schießen.`, '<b>Angriff:</b> Tippe auf deine aufrechten Einheiten an der Front, dann auf „gegen …“. Die Angreifer erschöpfen sich.', '<b>Blocken:</b> Der Verteidiger darf jeden Angreifer mit höchstens <b>einer</b> aufrechten Einheit blocken (auch aus der Kaserne). Die höhere <b>Stärke</b> gewinnt, bei Gleichstand fallen beide. Zivile Einheiten (Siedler, Händler, Handelsschiffe) und Luft-Einheiten (nur von Luft/Luftabwehr) können nicht blocken bzw. werden nicht geblockt.', `<b>Stadttreffer:</b> Ein nicht geblockter Angreifer verursacht seine Stärke als Schaden, minus dem <b>Schutz</b> deiner Gebäude (mindestens 1). Bei 0 ${ic('ui:hp')} scheidest du aus.`, '<b>Schuss:</b> Einheiten mit Fernkampf zerstören ein Ziel, wenn ihre Fern-Zahl mindestens dessen Stärke erreicht. Belagerer dürfen auch die Stadt beschießen. Kein Gegenschlag.')}
  <h2>Schlüsselwörter</h2><div class="reg-tab">${Object.entries(SCHL_TXT).filter(([k]) => k !== 'mission').map(([k, v]) => `<div><b>${esc(SCHL[k])}</b></div><div>${esc(v)}</div>`).join('')}</div>
  <h2>Ereignisse</h2><p>Nach jeder Runde wird ein Ereignis aufgedeckt. <b>Wetter</b> trifft alle (z. B. Ernte, Seuche, Diebe). <b>Barbaren</b> überfallen den Spieler mit dem schwächsten Heer: Ihre Stärke ist <i>dein Zeitalter + 1 + Bonus</i>. Hast du eine Einheit, die mindestens so stark ist, wehrt sie den Überfall ab und du bekommst Beute – sonst fällt eine Einheit, oder (ohne Einheit) trifft es Stadt oder Gold.</p>
  <div class="reg-tab">${D.ereignisse.map(e => `<div><b>${esc(e.name)}</b></div><div>${esc(e.beschreibung || '')}${e.text ? ' ' + esc(e.text.join(' ')) : ''}</div>`).join('')}</div>
  <h2>Siegbedingungen</h2>${li(`<b>Kultur:</b> ${R.kultur_sieg} Kultur (aus Gebäuden, Wundern, Verbündeten) – sofort bei Erreichen.`, `<b>Eroberung:</b> Alle anderen Städte sind bei 0 ${ic('ui:hp')}.`)}`;
}
function volkskarten(D) {
  const vs = D.voelker;
  return `<h2>Erweiterung 1: Volkskarten</h2><p>Jedes Volk bekommt <b>7 eigene Karten</b> – eine für jedes Zeitalter. Es sind besondere Einheiten und Gebäude, die nur dieses Volk hat.</p>
  ${li('<b>Start:</b> Zu deinen Handkarten bekommst du die <b>Volkskarte I</b>.', '<b>Aufstieg:</b> Bei jedem Aufstieg kommt die Volkskarte des neuen Zeitalters auf deine Hand.', 'Volkskarten zählen <b>nicht</b> zum Handlimit und lassen sich <b>nicht ablegen</b>. Wird eine zerstört, kehrt sie auf deine Hand zurück.', 'Mit „Götter & Glaube“ genügen 12 statt 13 Glaube zum Sieg – und beim Gründen einer Religion darfst du keine Volkskarte opfern.')}
  <h2>Alle 35 Volkskarten</h2>${vs.map(v => `<h3>${esc(v.name)}</h3><div class="lex-gitter">${D.volkskarten.filter(k => k.volk === v.id).map(k => lexikonKarte(k.id, { farbe: v.farbe, klein: true, a: 'lex', v: k.id })).join('')}</div>`).join('')}`;
}
function glaube(D) {
  const R = D.regeln;
  return `<h2>Erweiterung 2: Götter & Glaube</h2><p>Acht Religionen, neue Gebäude, Missionare – und ein dritter Siegweg: der <b>Glaubenssieg</b>.</p>
  <h3>Religion gründen</h3>${li('Ab <b>Zeitalter II</b> darfst du einmal pro Spiel eine Religion gründen: <b>5 Gold</b> zahlen und <b>1 Handkarte</b> opfern.', 'Jede Religion gibt es nur <b>einmal</b> – wer zuerst gründet, wählt.', 'Du bekommst einen eigenen <b>Glaubensstapel</b> mit 7 Karten (Heiligtum, Tempel, Halle, Stätte, Prophet, 2 Missionare). Beim Ziehen darfst du <b>1 Karte pro Zug</b> davon nehmen.', 'Jede Religion hat eine <b>dauerhafte Fähigkeit</b>.')}
  <h3>Glaube</h3><p><b>Dein Glaube</b> = 1 + Glaube deiner Religionsgebäude und Propheten + eigene Missionare bei Gegnern − fremde Missionare in deiner Stadt. Mit <b>${D.glaube_sieg} Glaube</b> (mit Volkskarten ${D.glaube_sieg_vk}) gewinnst du sofort.</p>
  <h3>Missionare</h3>${li('Ein Missionar kostet Gold und wird zu einem <b>Gegner</b> gesandt (höchstens einer pro Gegner). Er erhöht deinen Glauben und senkt den des Gegners.', 'Der Gegner kann ihn für <b>2 Gold</b> ausweisen – der Missionar kehrt dann auf deine Hand zurück.', 'Stirbt ein Spieler, kehren alle beteiligten Missionare heim.')}
  <h3>Glaube-Ereignisse</h3><p>6 zusätzliche Ereignisse (Pilgerzug, Prophezeiung, Ketzerjagd, Fest, Heilung, Glaubenskrieg) werden unter die Ereignisse gemischt.</p>
  <h2>Die 8 Religionen</h2><div class="reg-tab">${D.religionen.map(r => `<div style="color:${r.rahmen}"><b>${spr(`rel:${r.id}:emblem`, r.farbe, 1)} ${esc(r.name)}</b></div><div><b>${esc(r.titel)}:</b> ${esc(r.text)}<br><i class="mini">${esc(r.flavor)}</i></div>`).join('')}</div>
  <h2>Alle Glaubenskarten</h2><div class="lex-gitter">${D.relkarten.map(k => lexikonKarte(k.id, { farbe: k.farbe_rel, klein: true, a: 'lex', v: k.id })).join('')}</div>`;
}
function voelkerSeite(D) {
  return `<h2>Die fünf Völker</h2>${D.voelker.map(v => `<div class="band" style="--vf:${v.farbe};margin:8px 0">${spr('stadt:stadtstaat', v.farbe, 1)}<div><div class="vn">${esc(v.name)}</div><div class="mini">${esc(v.herrscher)}</div></div><div class="fa">${esc(v.beschreibung)}<br><b>${v.text.map(esc).join(' ')}</b></div></div>`).join('')}`;
}
function bedienung() {
  return `<h2>So bedienst du das Spiel</h2>${li('<b>Zug beginnen:</b> Tippe auf einen Kartenstapel unten, um zu ziehen. Dein Einkommen bekommst du automatisch.', '<b>Karte spielen:</b> Tippe auf eine Handkarte. Grün umrandete Karten kannst du gerade spielen; sonst steht im Fenster, was fehlt.', '<b>Wunder & Tribut:</b> Reiter „Tisch“.', '<b>Angreifen:</b> Reiter „Mein Reich“ → aufrechte Einheiten antippen → „Angriff“. <b>Schießen:</b> Fernkämpfer antippen → „Schießen“.', '<b>Verteidigen:</b> Wenn dich jemand angreift, öffnet sich ein Fenster. Wähle je Angreifer einen Blocker – oder nimm den Vorschlag.', '<b>Gegner ansehen:</b> Oben auf den Namen tippen. Du siehst ihre Gebäude, Land und Heer; ihre Handkarten sind verdeckt.', '<b>Zug beenden:</b> Grüner Knopf. Hast du zu viele Karten, legst du vorher ab.')}
  <h2>Unterschiede zum Papierspiel</h2>${li('Der Rechner führt Aufwecken, Einkommen, Ereignisse, Barbaren und den Neulingsschutz selbst aus.', 'Im Winter legt der Rechner automatisch deine schwächste Handkarte ab.', 'Die Computer-Gegner gibt es in drei Stufen: <b>Leicht</b> (macht Fehler), <b>Mittel</b> und <b>Stark</b>.')}`;
}
function lexikon(D) {
  const alle = [].concat(D.karten.map(k => ({ ...k, kat: k.typ })), D.wunder.map(k => ({ ...k, kat: 'wunder' })), D.staaten.map(k => ({ ...k, kat: 'staat' })), D.volkskarten.map(k => ({ ...k, kat: 'volk' })), D.relkarten.map(k => ({ ...k, kat: 'glaube' })));
  return alle;
}

export function regelnSeite(app, D, zurueck, start = 'grund') {
  const tabs = [['grund', 'Grundspiel'], ['volk', 'Volkskarten'], ['glaube', 'Götter & Glaube'], ['voelker', 'Völker'], ['lex', 'Karten-Lexikon'], ['bed', 'Bedienung']];
  let tab = start, kat = 'alle', suche = '';
  const zeichne = () => {
    let inh;
    if (tab === 'grund') inh = grundspiel(D); else if (tab === 'volk') inh = volkskarten(D); else if (tab === 'glaube') inh = glaube(D); else if (tab === 'voelker') inh = voelkerSeite(D); else if (tab === 'bed') inh = bedienung();
    else {
      const kats = [['alle', 'Alle'], ['land', 'Land'], ['einheit', 'Einheiten'], ['gebaeude', 'Gebäude'], ['wunder', 'Wunder'], ['staat', 'Stadtstaaten'], ['volk', 'Volkskarten'], ['glaube', 'Glaube']];
      const liste = lexikon(D).filter(k => (kat === 'alle' || k.kat === kat) && (!suche || (k.name + ' ' + (k.beschreibung || '') + ' ' + (k.flavor || '')).toLowerCase().includes(suche.toLowerCase())));
      inh = `<h2>Karten-Lexikon</h2><input type="text" id="lex-s" placeholder="Karte suchen …" value="${esc(suche)}" style="width:100%;margin-bottom:6px"><div class="chips" style="margin-bottom:8px">${kats.map(([k, n]) => `<span class="chipb ${kat === k ? 'an' : ''}" data-kat="${k}">${n}</span>`).join('')}</div><div class="mini">${liste.length} Karten</div><div class="lex-gitter">${liste.map(k => lexikonKarte(k.id, { st: k.stapel, a: 'lex', v: k.id })).join('')}</div>`;
    }
    app.innerHTML = `<div class="spiel regeln"><div class="kopf"><div class="titel">${ic('ui:lexikon')} Regeln & Karten</div><button class="sek" id="r-zu">${ic('ui:pfeil_links')}Zurück</button></div>
      <div class="tabs">${tabs.map(([k, n]) => `<button class="${tab === k ? 'an' : ''}" data-tab="${k}">${n}</button>`).join('')}</div>
      <div class="buehne"><div class="plan reg">${inh}</div></div></div>`;
    document.getElementById('r-zu').onclick = zurueck;
    app.querySelectorAll('[data-tab]').forEach(e => e.onclick = () => { tab = e.dataset.tab; zeichne(); });
    app.querySelectorAll('[data-kat]').forEach(e => e.onclick = () => { kat = e.dataset.kat; zeichne(); });
    const si = document.getElementById('lex-s'); if (si) { si.oninput = () => { suche = si.value; const pos = si.selectionStart; zeichne(); const n = document.getElementById('lex-s'); n.focus(); n.setSelectionRange(pos, pos); }; }
    app.querySelectorAll('[data-a="lex"]').forEach(e => e.onclick = () => lexSheet(D, e.dataset.v));
  };
  zeichne();
}
function lexSheet(D, id) {
  const ov = document.getElementById('overlay'), d = E.def({ id }); if (!d) return;
  ov.innerHTML = `<div class="sheet"><div class="fk"><h3>${esc(d.name)}</h3><button class="knopf" id="lex-zu" aria-label="Schließen" style="min-height:32px;padding:3px 8px">${ic('ui:kreuz')}</button></div><div class="fi"><div class="gross">${lexikonKarte(id, { cls: 'x' }).replace('loading="lazy"', '')}</div><div class="info"><div class="mini">${esc(kartenArt(d))}${d.zeitalter != null && d.typ !== 'land' ? ' · Zeitalter ' + ZA[d.zeitalter] : ''}</div>${braucht(d).length ? `<p class="mini">Braucht: ${braucht(d).map(esc).join(', ')}</p>` : ''}${benoetigt(d).length ? `<p class="mini">Voraussetzung: ${benoetigt(d).map(esc).join(', ')}</p>` : ''}</div></div></div>`;
  ov.classList.add('an'); const zu = () => { ov.classList.remove('an'); ov.innerHTML = ''; ov.onclick = null; };
  document.getElementById('lex-zu').onclick = zu; ov.onclick = (e) => { if (e.target === ov) zu(); };
}
