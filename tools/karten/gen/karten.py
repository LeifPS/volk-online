"""Zeichnet Kartenvorder- und -rückseiten (63 x 88 mm) für "Volk – Das Kartenspiel"."""
from lib import *

PAPIER = '#fbf7ec'
TYPFARBE = {'einheit': '#8c3b32', 'gebaeude': '#7d5d2e', 'land': '#3f8a3a', 'wunder': '#b08410', 'ereignis_barbaren': '#6b2d2d', 'ereignis_wetter': '#3d5f82', 'hilfe': '#4a5560'}
TYPNAME = {'einheit': 'EINHEIT', 'gebaeude': 'GEBÄUDE', 'land': 'LAND', 'wunder': 'WELTWUNDER', 'stadtstaat': 'STADTSTAAT'}
STAPELFARBE = {1: '#b9935a', 2: '#a05a4a', 3: '#4f7c8c', 4: '#5f6fc4', 0: '#5b3f7a'}
STAPELNAME = {1: 'STAPEL I · Antike & Klassik', 2: 'STAPEL II · Mittelalter & Renaissance', 3: 'STAPEL III · Industrie bis Atomzeit', 4: 'STAPEL IV · KI bis Sternenzeit', 0: 'WELT · Wunder, Stadtstaaten, Ereignisse'}
KLASSENNAME = {'zivil': 'Zivil', 'spaeher': 'Späher', 'haendler': 'Handel', 'nahkampf': 'Nahkampf', 'fernkampf': 'Fernkampf', 'reiter': 'Reiter', 'belagerung': 'Belagerung',
               'flak': 'Luftabwehr', 'sanitaeter': 'Sanitäter', 'see_zivil': 'Handelsschiff', 'see_nah': 'Kriegsschiff', 'see_fern': 'Kriegsschiff (Fernkampf)',
               'u_boot': 'U-Boot', 'traeger': 'Träger', 'transport': 'Transport', 'jaeger': 'Jagdflugzeug', 'bomber': 'Bomber', 'rakete': 'Rakete', 'atom': 'Atomwaffe'}
ZIELNAME = {'reiter': 'Reiter', 'luft': 'Fliegende', 'see': 'Schiffe', 'nahkampf': 'Nahkämpfer', 'u_boot': 'U-Boote', 'stadt': 'die Stadt', 'bomber': 'Bomber', 'rakete': 'Raketen', 'belagerung': 'Belagerer'}
SCHLUESSEL_TEXT = {
    'ansturm': 'Ansturm: +1 Stärke, wenn die Einheit angreift.',
    'ramme': 'Ramme: Macht doppelten Schaden an einer Stadt.',
    'fern': 'Schuss: Ist Fern mindestens so hoch wie die Stärke des Ziels, wird die Einheit zerstört. Kein Gegenschlag.',
    'belagerung': 'Belagerung: Darf auch die Stadt beschießen (Schaden = Fern, nicht blockbar).',
    'fliegend': 'Fliegend: Nur Fliegende und Luftabwehr dürfen blocken.',
    'luftabwehr': 'Luftabwehr: Blockt und beschießt Fliegende, +3 Stärke gegen sie.',
    'tarnung': 'Tarnung: Kann nicht beschossen werden.',
    'traeger': 'Träger: Deine Fliegenden brauchen kein Flugfeld.',
    'einmalig': 'Einmalig: Nach dem Einsatz ablegen.',
    'heilen': 'Heilen: Deine Stadt heilt zu Zugbeginn 1 Lebenspunkt mehr.',
    'mission': 'Mission: Lege den Missionar zu einem Gegner (höchstens 1 je Gegner). Du bekommst +1 Glaube, er verliert 1 Glaube. Er kann den Missionar für 2 Gold ausweisen (zurück auf deine Hand).',
    'gruenden': 'Gründen: Spiele sofort bis zu 2 Land-Karten aus deiner Hand. Danach ablegen.',
}
EFFEKT_ICON = {'E': 'gold', 'K': 'kultur', 'W': 'wissenschaft', 'S': 'schild', 'H': 'hp', 'A': 'einheit', 'HL': 'karte_tausch', 'G': 'bau', 'L': 'gruenden', 'Z': 'lexikon', 'F': 'rel:glaube', 'ABLEGEN': 'handel', 'SCHIFF': 'see'}
EFFEKT_TEXT = {
    'E': 'Einkommen +{n}: Du nimmst zu Zugbeginn {n} Gold mehr.',
    'K': 'Kultur {n}: Zählt für den Kultursieg.',
    'W': 'Wissen {n}: Der Zeitalter-Aufstieg kostet {n} Gold weniger.',
    'S': 'Schutz {n}: Jeder Treffer auf deine Stadt macht {n} weniger Schaden (mindestens 1).',
    'H': 'Heilung {n}: Deine Stadt heilt zu Zugbeginn {n} Lebenspunkte.',
    'A': 'Ausbildung {n}: Einheiten kosten {n} Gold weniger (mindestens 1).',
    'HL': 'Handlimit +{n}: Du darfst {n} Handkarte mehr behalten.',
    'G': 'Bauherr: Deine Gebäude kosten 1 Gold weniger (mindestens 1).',
    'L': 'Landwirtschaft: Du darfst 1 Land mehr pro Runde spielen.',
    'Z': 'Wissen: Du ziehst jede Runde 1 Karte mehr.',
    'F': 'Glaube {n}: Zählt für den Glaubenssieg.',
    'ABLEGEN': 'Händler: Karten ablegen bringt 2 Gold statt 1.',
    'SCHIFF': 'Seefahrt: Deine Schiffe haben +1 Stärke.',
}
PROV_TEXT = {'kueste': 'Zählt als Küste.', 'flug': 'Zählt als Flugfeld.'}
from satz import GELAENDE_FARBE
GEBAEUDE_NAMEN = {g['id']: g['name'] for g in __import__('satz').D['gebaeude']}
ART_NAME = {'bonus': 'Nahrung', 'bau': 'Baumaterial', 'strategisch': 'Strategischer Rohstoff', 'luxus': 'Luxusgut'}

def chip(c, x, y, ikon, text, hoehe=7.4 * mm, farbe='#222222', schrift='PXB', size=12):
    """Symbol + Zahl. Gibt Breite zurück."""
    ic = hoehe * .86
    icon(c, ikon, x, y + (hoehe - ic) / 2, ic)
    if THEMA['pixel'] and farbe == '#222222': farbe = '#ffffff'
    c.setFillColor(hexc(farbe)); c.setFont(schrift, size)
    c.drawString(x + ic + .6 * mm, y + hoehe / 2 - size * .17, text)
    return ic + .6 * mm + pdfmetrics.stringWidth(text, schrift, size) + 1.4 * mm

def text_block(c, absaetze, x, y_oben, breite, hoehe, farbe='#222222'):
    """Absätze (Text; optional ('i', text) für kursiv) mit automatischer Schriftgröße in die Box setzen."""
    px = THEMA['pixel']
    FN, FB, FI = ('VT', 'VT', 'VT') if px else ('DV', 'DVB', 'DVI')
    if px and farbe == '#222222': farbe = '#e6ebf7'
    kursivf = '#8fa0c8' if px else '#5a5448'; markf = '#ffd86b' if px else farbe
    for size in ((9.6, 9.0, 8.4, 7.8, 7.3, 6.8, 6.3, 5.8, 5.4) if px else (7.4, 7.0, 6.6, 6.2, 5.9, 5.6, 5.3, 5.0, 4.7)):
        lead = size * (1.0 if px else 1.16); gap = size * .38
        tot = 0
        for a in absaetze:
            t, f = (a[1], FI) if isinstance(a, tuple) else (a, FN)
            tot += len(simpleSplit(t, f, size, breite)) * lead + gap
        if tot - gap <= hoehe: break
    y = y_oben
    for a in absaetze:
        kursiv = isinstance(a, tuple); t = a[1] if kursiv else a
        zeilen = simpleSplit(t, FI if kursiv else FN, size, breite)
        for i, z in enumerate(zeilen):
            y -= lead
            if i == 0 and not kursiv and ':' in z and z.index(':') < 22:
                k = z.index(':') + 1
                c.setFillColor(hexc(markf)); c.setFont(FB, size); c.drawString(x, y, z[:k])
                c.setFillColor(hexc(farbe)); c.setFont(FN, size); c.drawString(x + pdfmetrics.stringWidth(z[:k], FB, size), y, z[k:])
            else:
                c.setFillColor(hexc(kursivf if kursiv else farbe)); c.setFont(FI if kursiv else FN, size); c.drawString(x, y, z)
        y -= gap
    return size

def geruest(c, frame, art_tint, titel, links_wert=None, links_icon='gold', rechts_art=None, rechts_wert=None, rechts_farbe='#888888', zeitalter=None):
    """Rahmen, Kopfzeile, Artbox. Gibt (art_x, art_y, art_w, art_h) in Punkt zurück."""
    px = THEMA['pixel']
    if px:
        u = .62 * mm
        c.setFillColor(hexc('#12131c')); c.rect(0, 0, CW, CH, stroke=0, fill=1)
        stufenrect(c, .9 * mm, .9 * mm, CW - 1.8 * mm, CH - 1.8 * mm, u, fill=hell(frame, .12))
        stufenrect(c, 2.3 * mm, 2.3 * mm, CW - 4.6 * mm, CH - 4.6 * mm, u, fill='#232840')
        c.setFillColor(hexc('#343c62')); c.rect(2.3 * mm + 2 * u, CH - 2.3 * mm - u, CW - 4.6 * mm - 4 * u, u, stroke=0, fill=1)      # Licht oben
        c.setFillColor(hexc('#161a2c')); c.rect(2.3 * mm + 2 * u, 2.3 * mm, CW - 4.6 * mm - 4 * u, u, stroke=0, fill=1)               # Schatten unten
        stufenrect(c, 3.4 * mm, CH - 11.1 * mm, CW - 6.8 * mm, 9.0 * mm, u * .8, fill='#2f3760')                                      # Titelband
    else:
        c.setFillColor(hexc(frame)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
        rrect(c, 2.2 * mm, 2.2 * mm, CW - 4.4 * mm, CH - 4.4 * mm, 2.2 * mm, fill=PAPIER)
    # Kopfzeile
    cy = CH - 6.4 * mm
    if links_wert is not None:
        icon(c, links_icon, 8.0 * mm - 3.3 * mm, cy - 3.3 * mm, 6.6 * mm)
        # Zahl auf dem Symbol mit Kontur
        s = str(links_wert)
        c.saveState()
        sz0 = 11 if len(s) < 2 else (9.5 if len(s) < 3 else 7.5)
        x0_ = 8.0 * mm - pdfmetrics.stringWidth(s, 'PXB', sz0) / 2
        c.saveState()
        c.setStrokeColor(hexc('#fff3c4' if not px else '#5a3d00')); c.setLineWidth(1.5)
        t1 = c.beginText(x0_, cy - 1.3 * mm); t1.setTextRenderMode(1); t1.setFont('PXB', sz0); t1.textOut(s); c.drawText(t1)
        c.restoreState()
        c.setFillColor(hexc('#2b2118' if not px else '#fff3c4'))
        t2 = c.beginText(x0_, cy - 1.3 * mm); t2.setFont('PXB', sz0); t2.textOut(s); c.drawText(t2)
        c.restoreState()
    if rechts_art == 'alter' and zeitalter is not None:
        za_icon(c, zeitalter, CW - 8.0 * mm, cy, 7.2 * mm)
    elif rechts_art == 'stapel':
        # Stapel = die Zeitalter, aus denen er zieht: I+II / III+IV / V+VI+VII als Symbole
        zs = {1: [0, 1], 2: [2, 3], 3: [4, 5, 6], 4: [7, 8, 9, 10]}.get(rechts_wert, [0])
        sz = 6.4 * mm if len(zs) == 2 else (4.8 * mm if len(zs) == 3 else 3.9 * mm); xr = CW - 4.6 * mm
        for z in reversed(zs):
            za_icon(c, z, xr - sz / 2, cy, sz); xr -= sz + .2 * mm
    elif rechts_art == 'icon':
        if px: stufenrect(c, CW - 8.0 * mm - 3.9 * mm, cy - 3.9 * mm, 7.8 * mm, 7.8 * mm, .6 * mm, fill=rechts_farbe)
        else: kreis(c, CW - 8.0 * mm, cy, 3.9 * mm, fill=rechts_farbe, stroke=dunkel(rechts_farbe, .4), lw=.8)
        icon(c, rechts_wert, CW - 8.0 * mm - 2.8 * mm, cy - 2.8 * mm, 5.6 * mm)
    elif rechts_art == 'zahl':
        if px: stufenrect(c, CW - 8.0 * mm - 3.9 * mm, cy - 3.9 * mm, 7.8 * mm, 7.8 * mm, .6 * mm, fill=rechts_farbe)
        else: kreis(c, CW - 8.0 * mm, cy, 3.9 * mm, fill=rechts_farbe, stroke=dunkel(rechts_farbe, .4), lw=.8)
        zentriert(c, rechts_wert, CW - 8.0 * mm, cy - 1.45 * mm, 'PXB', 9.5, '#ffffff')
    s = fit(c, titel, 'PXB', 10.5, 6.2, (33 if rechts_art == 'stapel' else 38) * mm)
    zentriert(c, titel, CW / 2, cy - s * .17, 'PXB', s, '#f4f6fb' if px else '#2b2118')
    # Artbox
    ax, ay, aw, ah = 4.2 * mm, 44.3 * mm, CW - 8.4 * mm, 32.0 * mm
    if px:
        stufenrect(c, ax - .5 * mm, ay - .5 * mm, aw + 1.0 * mm, ah + 1.0 * mm, .6 * mm, fill='#0e0f16')
        c.setFillColor(hexc(art_tint)); c.rect(ax + .5 * mm, ay + .5 * mm, aw - 1.0 * mm, ah - 1.0 * mm, stroke=0, fill=1)
        c.setFillColor(hexc(dunkel(art_tint, .06))); c.rect(ax + .5 * mm, ay + .5 * mm, aw - 1.0 * mm, ah * .30, stroke=0, fill=1)
        return ax, ay, aw, ah
    c.setFillColor(hexc(art_tint)); c.rect(ax, ay, aw, ah, stroke=0, fill=1)
    c.setFillColor(hexc(dunkel(art_tint, .06))); c.rect(ax, ay, aw, ah * .30, stroke=0, fill=1)   # Bodenband
    c.setStrokeColor(hexc(dunkel(frame, .15))); c.setLineWidth(.7); c.rect(ax, ay, aw, ah, stroke=1, fill=0)
    return ax, ay, aw, ah

def typzeile(c, text, farbe):
    zentriert(c, text, CW / 2, 40.6 * mm, 'SS', 5.2, hell(farbe, .55) if THEMA['pixel'] else farbe)

MODUL = {1: ('ERWEITERUNG 1 · VOLKSKARTEN', '#2f6f8f'), 2: ('ERWEITERUNG 2 · GÖTTER & GLAUBE', '#6b1f3a'), 3: ('ERWEITERUNG 3 · ZIVILISATION', '#3f2f73')}
def fuss(c, nr, stapel, frame, modul=0):
    """Fußzeile. modul 0 = Grundspiel (schlichter Text), 1/2/3 = Pixel-Symbol der Erweiterung."""
    gf, gz = ('PX', '#7d88ac') if THEMA['pixel'] else ('DV', '#8a8374')
    links(c, nr, 5.0 * mm, 4.1 * mm, gf, 4.2, gz)
    if not modul:
        rechts(c, 'VOLK · Grundspiel', CW - 5.0 * mm, 4.1 * mm, gf, 4.2, gz)
    else:
        g = 6.6 * mm   # Pixel-Symbol der Erweiterung statt Schild
        icon(c, 'mod:%d' % modul, CW - 4.4 * mm - g, 2.0 * mm, g)

def symbol_chips(c, braucht, x_rechts, y, hoehe=7.4 * mm):
    """Rechtsbündig: 'Braucht'-Symbole."""
    if not braucht: return
    ic = hoehe * .78
    gesamt = len(braucht) * (ic + .8 * mm)
    x = x_rechts - gesamt
    links(c, 'braucht', x - 9.6 * mm, y + hoehe / 2 - 1.0 * mm, 'PX' if THEMA['pixel'] else 'DV', 4.4, '#8f9bc0' if THEMA['pixel'] else '#7a7468')
    for b in braucht:
        icon(c, symbol_icon(b), x, y + (hoehe - ic) / 2, ic); x += ic + .8 * mm

import re
import relspr, civspr, modspr
_VERBOTEN = re.compile(r'(\d|%|Feld|schneller|forsch|Forsch|Produktion|Bauauftr|Bauzeit|Handelsroute|Nahrung|Einwohner|Gold|Kultur|Zufrieden|mehr |weniger|stärker|Lager|Tempo|Sicht|Zeitalter|Stadt)')
def flavor(text, maxlen=95):
    """Erster Satz der Spielbeschreibung, nur wenn er keine Mechanik des Echtzeitspiels nennt."""
    if not text: return None
    satz = re.split(r'(?<=[.!?])\s', text.strip())[0]
    if _VERBOTEN.search(satz) or len(satz) > maxlen: return None
    return satz

def kartenname(k, art):
    if k.get('relkarte'): return '%s · %s' % (k['rel_name'].upper(), art)
    return 'VOLKSKARTE · %s · %s' % (k['volk_name'].upper(), art)

def zeichne_einheit(c, k):
    vk = k.get('volkskarte') or k.get('relkarte'); fr = k.get('rahmen') or TYPFARBE['einheit']; zf = ZA[k['zeitalter']]['farbe']
    ax, ay, aw, ah = geruest(c, fr, hell(zf, .82), k['name'], k['kosten'], 'gold', 'alter', zeitalter=k['zeitalter'])
    zeichne_bild(c, k['sprite'], ax + 1 * mm, ay + 1.2 * mm, aw - 2 * mm, ah - 2.4 * mm, ausrichtung='mitte', **({'farbe': k.get('farbe_volk') or k['farbe_rel']} if vk else {}))
    typzeile(c, kartenname(k, 'EINHEIT') if vk else 'EINHEIT · ' + KLASSENNAME.get(k['klasse'], k['klasse']).upper(), fr)
    # Stärke / Fern
    y = 31.6 * mm; x = 5.0 * mm
    zivil = k['klasse'] in ('zivil', 'haendler', 'see_zivil')
    if k['klasse'] == 'missionar': x += chip(c, x, y, 'rel:mission', '+1')
    elif not zivil or k['staerke']:
        if k['staerke'] > 0 or k['fern'] == 0:
            x += chip(c, x, y, 'staerke', str(k['staerke']))
    if k.get('glaube'): x += chip(c, x, y, 'rel:glaube', str(k['glaube']))
    if k['fern'] > 0:
        x += chip(c, x, y, 'fernkampf', str(k['fern']))
    symbol_chips(c, k['braucht'], CW - 5.0 * mm, y)
    # Text
    ab = []
    if zivil: ab.append('Zivil: Kann weder angreifen noch blocken.')
    for s in k['schluessel']:
        if s in SCHLUESSEL_TEXT: ab.append(SCHLUESSEL_TEXT[s])
    if k.get('glaube'): ab.append('Glaube %d: Zählt für den Glaubenssieg.' % k['glaube'])
    if k['einkommen']: ab.append('Einkommen +%d: Bleibt liegen und bringt dir jede Runde %d Gold.' % (k['einkommen'], k['einkommen']))
    if k['ziehen']: ab.append('Spähen: Beim Ausspielen ziehst du %d Karte%s.' % (k['ziehen'], 'n' if k['ziehen'] > 1 else ''))
    for g, w in sorted(k['boni'].items()):
        ab.append('Gegen %s +%d Stärke.' % (ZIELNAME.get(g, g), w))
    if not vk and 'see' in k['tags'] and k['klasse'] != 'see_zivil': ab.append('Schiff: Braucht eine Küste.')
    if not vk and k['klasse'] == 'see_zivil': ab.append('Schiff: Braucht eine Küste.')
    if 'luft' in k['tags'] and k['id'] not in ('lenkrakete', 'atomwaffe', 'marschflugkoerper'): ab.append('Flugfeld: Braucht ein Flugfeld oder einen Träger.')
    if k['id'] in ('lenkrakete', 'atomwaffe'): ab.append('Start: Braucht ein Flugfeld oder einen Träger.')
    if k['id'] == 'atomwaffe': ab.append('Der Einschlag trifft die Stadt mit 12 Schaden (Schutz zählt).')
    if k['klasse'] == 'nahkampf' and not zivil and not vk: ab.insert(0, 'Nahkämpfer: Greift die Stadt an oder blockt Angreifer.')
    if not ab and not vk: ab.append('Nahkämpfer: Greift die Stadt an oder blockt Angreifer.')
    f = k['flavor'] if vk else flavor(k['beschreibung'])
    if f: ab.append(('i', f))
    text_block(c, ab, 5.0 * mm, 30.0 * mm, CW - 10.0 * mm, 21.5 * mm)
    fuss(c, k.get('nr', ''), k['stapel'], fr, 2 if k.get('relkarte') else 0)

def zeichne_gebaeude(c, k):
    vk = k.get('volkskarte') or k.get('relkarte'); fr = k.get('rahmen') or TYPFARBE['gebaeude']; zf = ZA[k['zeitalter']]['farbe']
    kost = k['kosten']
    ax, ay, aw, ah = geruest(c, fr, hell(zf, .78), k['name'], kost, 'gold', 'alter', zeitalter=k['zeitalter'])
    zeichne_bild(c, k['sprite'], ax + 1 * mm, ay + 1.2 * mm, aw - 2 * mm, ah - 2.4 * mm, **({'farbe': k.get('farbe_volk') or k['farbe_rel']} if vk else {}))
    typzeile(c, kartenname(k, 'GEBÄUDE') if vk else 'GEBÄUDE', fr)
    y = 31.6 * mm; x = 5.0 * mm
    for key in ('F', 'E', 'K', 'W', 'S', 'H', 'A', 'HL', 'G', 'L', 'Z'):
        if k['effekte'].get(key): x += chip(c, x, y, EFFEKT_ICON[key], ('+' if key in ('E', 'HL') else '') + str(k['effekte'][key]))
    for pv in k['prov']: x += chip(c, x, y, symbol_icon(pv), SYMBOL_NAMEN[pv], schrift='DVB', size=7.2)
    symbol_chips(c, k['braucht'], CW - 5.0 * mm, y)
    ab = []
    for key in ('F', 'E', 'K', 'W', 'S', 'H', 'A', 'HL', 'G', 'L', 'Z'):
        if k['effekte'].get(key): ab.append(EFFEKT_TEXT[key].format(n=k['effekte'][key]))
    for p in k['prov']: ab.append(PROV_TEXT[p])
    if k['benoetigt']: ab.append('Benötigt: ' + ' und '.join(GEBAEUDE_NAMEN[b] for b in k['benoetigt']) + ' in deiner Auslage.')
    if not k['effekte'] and not k['prov']: ab.append('Baue es, um neue Möglichkeiten freizuschalten.')
    f = k['flavor'] if vk else flavor(k['beschreibung'])
    if f: ab.append(('i', f))
    text_block(c, ab, 5.0 * mm, 30.0 * mm, CW - 10.0 * mm, 21.5 * mm)
    fuss(c, k.get('nr', ''), k['stapel'], fr, 2 if k.get('relkarte') else 0)

def zeichne_land(c, k):
    fr = TYPFARBE['land']; gc = GELAENDE_FARBE[k['gelaende']]
    ax, ay, aw, ah = geruest(c, fr, gc, k['name'], '+%d' % k['ertrag'], 'gold', 'stapel', k['stapel'])
    if k.get('deko'):
        zeichne_bild(c, k['deko'], ax + .5 * mm, ay + .8 * mm, aw - 1 * mm, ah - 1.6 * mm, zuschnitt=True, ausrichtung='unten')
    # Rohstoff auf Plakette
    pr = 9.5 * mm; px_, py_ = ax + aw / 2, ay + ah * .52
    kreis(c, px_ + 11 * mm, ay + 10.5 * mm, 8.2 * mm, fill='#fffaf0', stroke=dunkel(fr, .1), lw=1.1)
    zeichne_bild(c, k['sprite'], px_ + 11 * mm - 6.2 * mm, ay + 10.5 * mm - 6.2 * mm, 12.4 * mm, 12.4 * mm, zuschnitt=True)
    typzeile(c, 'LAND · ' + k['gelaende_name'].upper() + ' · ' + ART_NAME.get(k['art'], '').upper(), fr)
    y = 31.6 * mm; x = 5.0 * mm
    x += chip(c, x, y, 'gold', '+%d' % k['ertrag'])
    for s in k['symbole']:
        x += chip(c, x, y, symbol_icon(s), SYMBOL_NAMEN[s], schrift='DVB', size=7.2)
    ab = ['Ertrag +%d: Dieses Land bringt dir zu Zugbeginn %d Gold.' % (k['ertrag'], k['ertrag'])]
    for s in k['symbole']:
        if s == 'kueste': ab.append('Küste: Hier dürfen Schiffe und Häfen entstehen.')
        else: ab.append('Rohstoff %s: Karten, die %s brauchen, kannst du ohne Zukauf spielen.' % (SYMBOL_NAMEN[s], SYMBOL_NAMEN[s]))
    if k['art'] == 'luxus': ab.append('Luxusgut: Es bringt mehr Gold als gewöhnliches Land.')
    ab.append('Pro Runde darfst du 1 Land spielen.')
    text_block(c, ab, 5.0 * mm, 30.0 * mm, CW - 10.0 * mm, 21.5 * mm)
    fuss(c, k.get('nr', ''), k['stapel'], fr)

def zeichne_wunder(c, k):
    fr = TYPFARBE['wunder']; zf = ZA[k['zeitalter']]['farbe']
    ax, ay, aw, ah = geruest(c, fr, hell(zf, .8), k['name'], k['kosten'], 'gold', 'alter', zeitalter=k['zeitalter'])
    zeichne_bild(c, k['sprite'], ax + 1 * mm, ay + .8 * mm, aw - 2 * mm, ah - 1.6 * mm, zuschnitt=True)
    typzeile(c, 'WELTWUNDER · NUR EINMAL IM SPIEL', fr)
    y = 31.6 * mm; x = 5.0 * mm
    eng = sum(1 for key in ('K', 'E', 'W', 'S', 'G', 'L', 'Z') if k['effekte'].get(key)) >= 3 and k['braucht']
    for key in ('K', 'E', 'W', 'S', 'G', 'L', 'Z'):
        if k['effekte'].get(key): x += chip(c, x, y, EFFEKT_ICON[key], ('+' if key in ('E', 'L') else '') + str(k['effekte'][key]), **(dict(hoehe=6.2 * mm, size=10) if eng else {}))
    symbol_chips(c, k['braucht'], CW - 5.0 * mm, y)
    ab = []
    for key in ('K', 'E', 'W', 'S'):
        if k['effekte'].get(key): ab.append(EFFEKT_TEXT[key].format(n=k['effekte'][key]))
    ab += k['text']
    if k['benoetigt']: ab.append('Benötigt: ' + ' und '.join(GEBAEUDE_NAMEN[b] for b in k['benoetigt']) + ' in deiner Auslage.')
    ab.append(('i', k['beschreibung']))
    text_block(c, ab, 5.0 * mm, 30.0 * mm, CW - 10.0 * mm, 21.5 * mm)
    fuss(c, k.get('nr', ''), 0, fr)

def zeichne_staat(c, k):
    farbe = k['farbe']; fr = dunkel(farbe, .35) if farbe.lower() not in ('#111111',) else '#333333'
    ax, ay, aw, ah = geruest(c, fr, hell(farbe, .8), k['name'], k['kosten'], 'gold', 'icon', 'diplomatie', rechts_farbe=dunkel(farbe, .15))
    zeichne_bild(c, k['sprite'], ax + 1 * mm, ay + .8 * mm, aw - 2 * mm, ah - 1.6 * mm, farbe=farbe, zuschnitt=True)
    SW = {'handel': 'Handel', 'forschung': 'Forschung', 'militaer': 'Militär', 'kultur': 'Kultur', 'seefahrt': 'Seefahrt', 'nahrung': 'Nahrung'}
    typzeile(c, 'STADTSTAAT · ' + SW[k['schwerpunkt']].upper(), fr)
    y = 31.6 * mm; x = 5.0 * mm
    for key in ('E', 'K', 'W', 'S', 'H', 'A', 'HL', 'L', 'ABLEGEN', 'SCHIFF'):
        if k['effekte'].get(key): x += chip(c, x, y, EFFEKT_ICON[key], ('+' if key in ('E', 'HL', 'L') else '') + (str(k['effekte'][key]) if key not in ('L', 'ABLEGEN', 'SCHIFF') else ''))
    for p in k['prov']: x += chip(c, x, y, symbol_icon(p), SYMBOL_NAMEN[p], schrift='DVB', size=7.2)
    ab = ['Tribut: Zahle %d Gold in deinem Zug, um dich zu verbünden (höchstens 2 Stadtstaaten pro Spieler). Lege die Karte vor dich.' % k['kosten'], 'Solange du verbündet bist:']
    for key in ('E', 'K', 'W', 'S', 'H', 'A', 'HL', 'L', 'ABLEGEN', 'SCHIFF'):
        if k['effekte'].get(key): ab.append(EFFEKT_TEXT[key].format(n=k['effekte'][key]))
    for p in k['prov']: ab.append('Dein Hafen: ' + PROV_TEXT[p] + ' Schiffe brauchen keine eigene Küste.' if p == 'kueste' else PROV_TEXT[p])
    ab.append(('i', k['beschreibung']))
    text_block(c, ab, 5.0 * mm, 30.0 * mm, CW - 10.0 * mm, 21.5 * mm)
    fuss(c, '', 0, fr)

def zeichne_ereignis(c, k):
    if k['art'] == 'barbaren':
        fr = TYPFARBE['ereignis_barbaren']
        ax, ay, aw, ah = geruest(c, fr, '#e8dcc8', k['name'], None, None, 'zahl', '+%d' % k['plus'], rechts_farbe='#8a2a2a')
        zeichne_bild(c, k['sprite'], ax + .5 * mm, ay + .8 * mm, aw * .62, ah - 1.6 * mm, zuschnitt=True, ausrichtung='unten')
        zeichne_bild(c, k['sprite2'], ax + aw * .60, ay + 1.2 * mm, aw * .38, ah - 2.4 * mm, zuschnitt=True, ausrichtung='mitte')
        icon(c, 'krieg', 8.0 * mm - 3.6 * mm, CH - 6.4 * mm - 3.6 * mm, 7.2 * mm)
        typzeile(c, 'EREIGNIS · BARBAREN', fr)
        y = 31.6 * mm
        chip(c, 5.0 * mm, y, 'staerke', 'Zeitalter+%d' % k['plus'], schrift='PXB', size=9)
        chip(c, 36.0 * mm, y, 'gold', 'Beute %d' % k['beute'], schrift='PXB', size=9)
        folge = 'Die Stadt nimmt Schaden in Höhe der Barbaren-Stärke (Schutz zählt, mindestens 1).' if k['folge'] == 'stadt' else 'Der Spieler verliert Gold in Höhe der Barbaren-Stärke.'
        ab = ['Überfall: Der Spieler mit den wenigsten Kampfeinheiten wird angegriffen (bei Gleichstand alle Betroffenen). Barbaren ignorieren den Neulingsschutz!',
              'Stärke der Barbaren = Zeitalter-Nummer (I = 1 … VII = 7) des Spielers + %d.' % k['plus'],
              'Abwehr (freiwillig): Das Opfer darf 1 aufrechte (ungetappte) Einheit entgegenstellen. Gleich stark oder stärker: Barbaren besiegt, %d Gold Beute. Sonst geht die Einheit verloren.' % k['beute'],
              'Ohne Abwehr: ' + folge]
        text_block(c, ab, 5.0 * mm, 30.0 * mm, CW - 10.0 * mm, 21.5 * mm)
    else:
        fr = TYPFARBE['ereignis_wetter']
        ax, ay, aw, ah = geruest(c, fr, '#dfe9f2', k['name'], None, None, None)
        zeichne_bild(c, k['icon'], ax + 5 * mm, ay + 2 * mm, aw - 10 * mm, ah - 4 * mm, zuschnitt=True)
        typzeile(c, 'EREIGNIS · WELT', fr)
        ab = list(k['text']) + [('i', 'Das Ereignis gilt sofort für alle Spieler. Danach wird die Karte abgelegt.')]
        text_block(c, ab, 5.0 * mm, 38.0 * mm, CW - 10.0 * mm, 28 * mm)
    fuss(c, '', 0, fr)

def zeichne_hilfe(c, seite, nr):
    fr = TYPFARBE['hilfe']
    c.setFillColor(hexc(fr)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 2.2 * mm, 2.2 * mm, CW - 4.4 * mm, CH - 4.4 * mm, 2.2 * mm, fill=PAPIER)
    if seite == 'vorn':
        zentriert(c, 'DEIN ZUG', CW / 2, CH - 9 * mm, 'PXB', 12, '#2b2118')
        sch = [('1', 'Aufwecken', 'Einheiten aufrichten, Kaserne → Front, Stadt heilt.', 'befoerderung'),
               ('2', 'Einkommen', '2 + Zeitalter (0–6) + Land + Gebäude + Wunder + Verbündete.', 'gold'),
               ('3', 'Ziehen', '2 Karten vom Stapel deines Zeitalters oder einem niedrigeren.', 'karte_tausch'),
               ('4', 'Aktionen', '1 Land, Karten spielen, Aufstieg, Tribut, Ablegen (1 Gold, 2×), Angreifen.', 'bau'),
               ('5', 'Ende', 'Handlimit 7. Nach der Runde: Ereigniskarte aufdecken.', 'zeit')]
        y = CH - 12.5 * mm
        for n, t, d, ik in sch:
            kreis(c, 7.4 * mm, y - 3.4 * mm, 3.2 * mm, fill=fr)
            zentriert(c, n, 7.4 * mm, y - 4.5 * mm, 'PXB', 8.5, '#ffffff')
            links(c, t, 12.3 * mm, y - 2.4 * mm, 'PXB', 8, '#2b2118')
            hh = absatz_hoehe(d, 40.0 * mm, 'DV', 5.4)
            absatz(c, d, 12.3 * mm, y - 3.0 * mm, 40.0 * mm, 'DV', 5.4)
            y -= max(9.6 * mm, hh + 4.2 * mm)
        rrect(c, 5 * mm, 6.2 * mm, CW - 10 * mm, 12.5 * mm, 1.5 * mm, fill='#efe6c8')
        absatz(c, 'Sieg: %d Kultur oder alle anderen Städte erobert.' % R['kultur_sieg'], 7 * mm, 18.0 * mm, CW - 14 * mm, 'DVB', 5.8)
        absatz(c, 'Neulingsschutz: Runde 1–%d kein Angriff.' % R['schutz_runden'], 7 * mm, 12.3 * mm, CW - 14 * mm, 'DV', 5.4)
    else:
        zentriert(c, 'ZEITALTER', CW / 2, CH - 9 * mm, 'PXB', 12, '#2b2118')
        y = CH - 12.8 * mm
        links(c, 'Aufstieg kostet', 6 * mm, y - 1.5 * mm, 'DV', 5.2, '#6a6458')
        rechts(c, 'Einkommen', CW - 6 * mm, y - 1.5 * mm, 'DV', 5.2, '#6a6458')
        y -= 3.5 * mm
        for z in range(7):
            za_icon(c, z, 8.0 * mm, y - 3.4 * mm, 6.4 * mm)
            links(c, ZA[z]['name'], 13 * mm, y - 4.4 * mm, 'PXB', 7.4, '#2b2118')
            if z < 6:
                rechts(c, str(R['aufstieg'][z]) + ' Gold → ' + ROEM[z + 1], 41 * mm, y - 4.4 * mm, 'DV', 5.2, '#4a443a')
            rechts(c, '%d + Land …' % (R['basis_einkommen'] + z), CW - 6 * mm, y - 4.4 * mm, 'DV', 5.2, '#4a443a')
            y -= 7.4 * mm
        absatz(c, 'Stapel I: Zeitalter I–II, Stapel II: III–IV, Stapel III: V–VII. Gespielt wird nur bis zum eigenen Zeitalter.', 6 * mm, y + 0.5 * mm, CW - 12 * mm, 'DV', 5.0)
        absatz(c, 'Fehlt 1 Rohstoff: für 3 Gold zukaufen.', 6 * mm, 11.6 * mm, CW - 12 * mm, 'DVB', 5.2)
    zentriert(c, 'VOLK · Spielhilfe %d' % nr, CW / 2, 4.1 * mm, 'DV', 4.2, '#8a8374')

# ---------------- Rückseiten ----------------
RUECKEN_STADT = {1: 'stadt:stadt@1@2', 2: 'stadt:stadt@3@2', 3: 'stadt:stadt@5@2', 4: 'stadt:stadt@8@2', 0: 'stadt:stadtstaat'}
def zeichne_ruecken(c, stapel):
    f = STAPELFARBE[stapel]
    c.setFillColor(hexc(f)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 3.2 * mm, 3.2 * mm, CW - 6.4 * mm, CH - 6.4 * mm, 2.2 * mm, fill=hell(f, .9))
    rrect(c, 5.2 * mm, 5.2 * mm, CW - 10.4 * mm, CH - 10.4 * mm, 1.6 * mm, stroke=f, lw=.9)
    zentriert(c, 'VOLK', CW / 2, CH - 21 * mm, 'PXB', 30, dunkel(f, .35))
    zentriert(c, 'Das Kartenspiel', CW / 2, CH - 28 * mm, 'PX', 9.5, dunkel(f, .25))
    zentriert(c, 'GRUNDSPIEL', CW / 2, 6.8 * mm, 'SS', 5.2, dunkel(f, .3))
    farbe = '#ff0054' if stapel == 0 else '#2f6fd0'
    zeichne_bild(c, RUECKEN_STADT[stapel], 12 * mm, 21 * mm, CW - 24 * mm, 31 * mm, farbe=('#7a4fb5' if stapel == 0 else farbe), zuschnitt=True)
    zentriert(c, STAPELNAME[stapel].split(' · ')[0], CW / 2, 16.5 * mm, 'PXB', 10, dunkel(f, .35))
    zentriert(c, STAPELNAME[stapel].split(' · ')[1], CW / 2, 11.4 * mm, 'DV', 5.6, dunkel(f, .3))

CIVTYP = {'regierung': 'REGIERUNG', 'person': 'GROSSE PERSÖNLICHKEIT', 'natur': 'NATURWUNDER'}
def zeichne_civ(c, k):
    t = k['typ']; fr = k['rahmen']; f = k['farbe']
    ax, ay, aw, ah = geruest(c, fr, hell(f, .78), k['name'], k['kosten'], 'gold', 'alter', zeitalter=k['zeitalter'])
    if t == 'natur':
        zeichne_bild(c, k['sprite'], ax + .5 * mm, ay + .8 * mm, aw - 1 * mm, ah - 1.6 * mm, zuschnitt=True, ausrichtung='unten')
    elif t == 'person':
        zeichne_bild(c, k['sprite'], ax + 1 * mm, ay + 1.0 * mm, aw - 2 * mm, ah - 2.0 * mm, farbe=f, zuschnitt=True, ausrichtung='mitte')
    else:
        zeichne_bild(c, k['sprite'], ax + 4 * mm, ay + 1.5 * mm, aw - 8 * mm, ah - 3.0 * mm, farbe=f, zuschnitt=True, ausrichtung='mitte')
    zus = ('REGIERUNG · AB ZEITALTER ' + ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'][k['zeitalter']]) if t == 'regierung' else ('PERSÖNLICHKEIT · ' + k['rolle_name'].upper()) if t == 'person' else ('NATURWUNDER · ' + k['gelaende_name'].upper())
    typzeile(c, zus, fr)
    y = 31.6 * mm; x = 5.0 * mm
    for key in ('F', 'E', 'K', 'W', 'S', 'H', 'A', 'HL', 'G', 'L', 'Z', 'SCHIFF'):
        if k['effekte'].get(key): x += chip(c, x, y, EFFEKT_ICON[key], ('+' if key in ('E', 'HL') else '') + str(k['effekte'][key]))
    em = k.get('einmal') or {}
    if em.get('gold'): x += chip(c, x, y, 'gold', '+%d' % em['gold'])
    if em.get('ziehen'): x += chip(c, x, y, 'karte_tausch', '+%d' % em['ziehen'])
    if em.get('heilen'): x += chip(c, x, y, 'hp', '+%d' % em['heilen'])
    ab = []
    if t == 'regierung': ab.append('Regierung: Zahle %d Gold in deinem Zug und lege die Karte vor dich. Eine neue Regierung ersetzt die alte (1 Wechsel pro Zug).' % k['kosten'])
    elif t == 'person': ab.append('Persönlichkeit: Zahle %d Gold, um sie aus der offenen Reihe zu holen (höchstens 1 Karte dieser Erweiterung pro Zug).' % k['kosten'])
    else: ab.append('Naturwunder: Du brauchst Zeitalter II und eine Land-Karte mit dem Gelände %s in deiner Auslage. Zahle %d Gold.' % (k['gelaende_name'], k['kosten']))
    for key in ('F', 'E', 'K', 'W', 'S', 'H', 'A', 'HL', 'G', 'L', 'Z', 'SCHIFF'):
        if k['effekte'].get(key): ab.append(EFFEKT_TEXT[key].format(n=k['effekte'][key]))
    if em:
        import civ as _c; ab.append(_c.einmal_text(em))
    elif t == 'person': ab.append('Dauerhaft: Bleibt vor dir liegen (höchstens 3 Persönlichkeiten).')
    ab.append(('i', k['flavor']))
    text_block(c, ab, 5.0 * mm, 30.0 * mm, CW - 10.0 * mm, 21.5 * mm)
    fuss(c, k.get('nr', ''), 0, fr, 3)

def zeichne_vorn(c, k):
    t = k['typ']
    if t in ('regierung', 'person', 'natur'): return zeichne_civ(c, k)
    if t == 'einheit': zeichne_einheit(c, k)
    elif t == 'gebaeude': zeichne_gebaeude(c, k)
    elif t == 'land': zeichne_land(c, k)
    elif t == 'wunder': zeichne_wunder(c, k)
    elif t == 'stadtstaat': zeichne_staat(c, k)
    elif t == 'ereignis': zeichne_ereignis(c, k)
    elif t == 'hilfe': zeichne_hilfe(c, k['seite'], k['nr_h'])
