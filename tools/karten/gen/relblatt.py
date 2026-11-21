"""Druckbögen der Religions-Erweiterung: 3_Erweiterung_Goetter_und_Glaube_Karten.pdf (8 Religionsblätter + 1 Ereignisblatt)."""
import os, sys, json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from lib import *
import karten, relspr
from karten import PAPIER, geruest, typzeile, fuss, text_block
import religionen as RL

AUS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, '..', 'ausgabe')
os.makedirs(AUS, exist_ok=True)
PW, PH = A4
RX, RY = (PW - 3 * CW) / 2, (PH - 3 * CH) / 2
REL, RKARTEN = RL.baue()
RELD = {r['id']: r for r in REL}
EVFARBE = '#5e2f6b'
FG = lambda f: '#ffffff' if sum(spr._rgb(f)[i] * w for i, w in enumerate((.299, .587, .114))) < 150 else '#2b2118'

def ruecken(c, rid):
    r = RELD[rid]; f = r['rahmen']; fv = r['farbe']
    c.setFillColor(hexc(f)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 3.2 * mm, 3.2 * mm, CW - 6.4 * mm, CH - 6.4 * mm, 2.2 * mm, fill=hell(fv, .88))
    rrect(c, 5.2 * mm, 5.2 * mm, CW - 10.4 * mm, CH - 10.4 * mm, 1.6 * mm, stroke=f, lw=.9)
    zentriert(c, 'GLAUBE', CW / 2, CH - 21 * mm, 'PXB', 27, dunkel(f, .2))
    zentriert(c, 'Götter & Glaube', CW / 2, CH - 28 * mm, 'PX', 9.5, dunkel(f, .2))
    zentriert(c, 'ERWEITERUNG 2', CW / 2, CH - 34 * mm, 'SS', 5.6, dunkel(f, .1))
    zeichne_bild(c, 'rel:%s:emblem' % rid, 17 * mm, 40 * mm, CW - 34 * mm, 30 * mm, farbe=fv, zuschnitt=True)
    zeichne_bild(c, 'rel:%s:staette' % rid, 14 * mm, 14 * mm, CW - 28 * mm, 20 * mm, farbe=fv, zuschnitt=True) if False else None
    nm = r['name'].upper(); s = fit(c, nm, 'PXB', 11, 6.5, CW - 14 * mm)
    zentriert(c, nm, CW / 2, 21 * mm, 'PXB', s, dunkel(f, .2))
    zentriert(c, 'Erweiterung', CW / 2, 14.6 * mm, 'DV', 5.6, dunkel(f, .1))

def ruecken_ereignis(c):
    f = EVFARBE; fv = '#a05fc0'
    c.setFillColor(hexc(f)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 3.2 * mm, 3.2 * mm, CW - 6.4 * mm, CH - 6.4 * mm, 2.2 * mm, fill=hell(fv, .88))
    rrect(c, 5.2 * mm, 5.2 * mm, CW - 10.4 * mm, CH - 10.4 * mm, 1.6 * mm, stroke=f, lw=.9)
    zentriert(c, 'GLAUBE', CW / 2, CH - 21 * mm, 'PXB', 27, dunkel(f, .1))
    zentriert(c, 'Götter & Glaube · Ereignisse', CW / 2, CH - 28 * mm, 'PX', 8.4, dunkel(f, .1))
    zentriert(c, 'ERWEITERUNG 2', CW / 2, CH - 34 * mm, 'SS', 5.6, dunkel(f, .1))
    zeichne_bild(c, 'rel:glaube_gross', 17 * mm, 28 * mm, CW - 34 * mm, 38 * mm, farbe=fv, zuschnitt=True)
    zentriert(c, 'ERWEITERUNG 2 · mischen unter', CW / 2, 17.5 * mm, 'DV', 5.4, dunkel(f, .1))
    zentriert(c, 'die Ereigniskarten des Grundspiels', CW / 2, 14 * mm, 'DV', 5.4, dunkel(f, .1))

def tafelkarte(c, rid):
    r = RELD[rid]; f = r['rahmen']; fv = r['farbe']
    c.setFillColor(hexc(f)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 2.2 * mm, 2.2 * mm, CW - 4.4 * mm, CH - 4.4 * mm, 2.2 * mm, fill=PAPIER)
    c.setFillColor(hexc(fv)); c.rect(2.2 * mm, CH - 15.5 * mm, CW - 4.4 * mm, 13.3 * mm, stroke=0, fill=1)
    nm = r['name']; s = fit(c, nm, 'PXB', 12, 7, CW - 22 * mm)
    zentriert(c, nm, CW / 2, CH - 9.4 * mm, 'PXB', s, FG(fv))
    zentriert(c, 'RELIGION · TAFEL', CW / 2, CH - 13.6 * mm, 'SS', 4.6, FG(fv))
    icon(c, 'rel:%s:symbol' % rid, 5.0 * mm, CH - 13.2 * mm, 8 * mm) if False else None
    zeichne_bild(c, 'rel:%s:symbol' % rid, 4.6 * mm, CH - 13.4 * mm, 8.6 * mm, 8.6 * mm, farbe=fv, zuschnitt=False)
    zeichne_bild(c, 'rel:%s:staette' % rid, 14 * mm, 48 * mm, CW - 28 * mm, 22.5 * mm, farbe=fv, zuschnitt=True)
    zentriert(c, 'FÄHIGKEIT: ' + r['titel'].upper(), CW / 2, 44.5 * mm, 'PXB', 7.6, dunkel(f, .2))
    ab = [r['text'], 'Gründen (1× pro Spiel, ab Zeitalter II): 5 Gold zahlen, 1 Handkarte ablegen. Du bekommst diese Tafel, 1 Glaube und die 7 Religionskarten als Religionsstapel.', ('i', r['flavor'])]
    text_block(c, ab, 5.0 * mm, 42.5 * mm, CW - 10.0 * mm, 33 * mm)
    fuss(c, 'RT-' + rid[:2].upper(), 0, f, 2)

def uebersicht(c, rid):
    r = RELD[rid]; f = r['rahmen']; fv = r['farbe']
    c.setFillColor(hexc(f)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 2.2 * mm, 2.2 * mm, CW - 4.4 * mm, CH - 4.4 * mm, 2.2 * mm, fill=PAPIER)
    zentriert(c, 'RELIGIONSSTAPEL', CW / 2, CH - 8.3 * mm, 'PXB', 9.5, dunkel(f, .25))
    zentriert(c, r['name'], CW / 2, CH - 12.8 * mm, 'DV', 5.4, '#6a6458')
    y = CH - 16.5 * mm
    sort = {'heiligtum': 'Heiligtum', 'tempel': 'Tempel', 'halle': 'Pilgerhalle', 'staette': 'Heilige Stätte', 'prophet': 'Prophet', 'missionar': 'Missionar (2×)'}
    zeilen = [k for k in RKARTEN if k['religion'] == rid and not k['id'].endswith('missionar2')]
    for k in zeilen:
        za_icon(c, k['zeitalter'], 8.5 * mm, y - 2.1 * mm, 5.6 * mm)
        s = fit(c, k['name'], 'DVB', 7.0, 5.0, 31 * mm)
        links(c, k['name'], 13.5 * mm, y - 3.0 * mm, 'DVB', s, '#2b2118')
        g = k.get('glaube') or k.get('effekte', {}).get('F', 0)
        links(c, sort[k['sorte']] + (' · Glaube %d' % g if g else ' · Mission'), 13.5 * mm, y - 6.3 * mm, 'DV', 4.8, '#7a7468')
        kreis(c, CW - 9 * mm, y - 2.3 * mm, 2.9 * mm, fill='#fff3c4', stroke=dunkel(f, .1), lw=.6)
        zentriert(c, str(k['kosten']), CW - 9 * mm, y - 3.9 * mm, 'PXB', 6.8, '#2b2118')
        y -= 8.7 * mm
    zentriert(c, 'Ziehe 1 Karte pro Zug von hier.', CW / 2, 15.2 * mm, 'DV', 4.8, '#6a6458')
    zentriert(c, 'Abgelegte Karten kommen unter den Stapel.', CW / 2, 12.2 * mm, 'DV', 4.8, '#6a6458')
    zentriert(c, 'Jede Religion gibt es nur 1× im Spiel.', CW / 2, 9.2 * mm, 'DV', 4.8, '#6a6458')

def spr_za(z):
    from lib import ZA
    return ZA[z]['farbe']

EVBILD = {'pilgerzug': 'rel:windwanderer:missionar', 'prophezeiung': 'rel:sternenorakel:prophet', 'ketzerjagd': 'rel:flammenorden:emblem', 'fest': 'rel:sonnenkult:staette', 'heilung': 'rel:hain:prophet', 'glaubenskrieg': 'rel:berggeister:emblem'}
EVFARBEN = {'pilgerzug': '#4fb3a9', 'prophezeiung': '#7b3fb5', 'ketzerjagd': '#d8432b', 'fest': '#e8a317', 'heilung': '#2f8f4e', 'glaubenskrieg': '#7a6a58'}
def ereigniskarte(c, e):
    f = EVFARBE
    ax, ay, aw, ah = geruest(c, f, hell(EVFARBEN[e['id']], .8), e['name'], None, None, 'icon', 'rel:glaube', rechts_farbe='#6b1f3a')
    zeichne_bild(c, EVBILD[e['id']], ax + 8 * mm, ay + 1.5 * mm, aw - 16 * mm, ah - 3 * mm, farbe=EVFARBEN[e['id']], zuschnitt=True)
    typzeile(c, 'EREIGNIS · GLAUBE', f)
    ab = [e['text'], 'Gilt sofort für alle Spieler. Danach ablegen.', ('i', e['flavor'])]
    text_block(c, ab, 5.0 * mm, 38.0 * mm, CW - 10.0 * mm, 28 * mm)
    fuss(c, 'GE-' + e['id'][:3].upper(), 0, f, 2)

def regelkarte(c, titel, absaetze, nr):
    f = '#6b1f3a'
    c.setFillColor(hexc(f)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 2.2 * mm, 2.2 * mm, CW - 4.4 * mm, CH - 4.4 * mm, 2.2 * mm, fill=PAPIER)
    zeichne_bild(c, 'rel:glaube_gross', CW / 2 - 6 * mm, CH - 18.5 * mm, 12 * mm, 12 * mm, farbe='#d8432b', zuschnitt=True)
    zentriert(c, titel, CW / 2, CH - 22.5 * mm, 'PXB', 9.2, '#2b2118')
    text_block(c, absaetze, 5.0 * mm, CH - 26 * mm, CW - 10.0 * mm, CH - 36 * mm)
    fuss(c, nr, 0, f, 2)

REGELKARTEN = [
 ('SO GEWINNST DU', ['Glaube = alle Glaube-Flammen auf deinen Karten + 1 für deine Religion + 1 für jeden Missionar, den du bei Gegnern hast – 1 für jeden fremden Missionar bei dir.',
                     'Sobald dein Glaube <GS> erreicht, gewinnst du sofort (mit Erweiterung 1: <GSV>). Das ist ein weiterer Siegweg neben Kultur, Eroberung und Wissenschaft.',
                     ('i', 'Glaube zählt nur, wenn du eine Religion hast.')], 'GR-1'),
 ('RELIGION GRÜNDEN', ['Einmal pro Spiel, in deinem Zug, ab Zeitalter II: Zahle 5 Gold und lege 1 Handkarte ab. Nimm eine freie Religionstafel.',
                       'Mische ihre 7 Karten als deinen Religionsstapel. Du darfst bei jedem Ziehen 1 Karte von dort nehmen. Abgelegte Religionskarten kommen unter den Stapel.',
                       ('i', 'Jede Religion gibt es nur einmal im Spiel.')], 'GR-2'),
 ('MISSIONEN', ['Spiele einen Missionar (Kosten zahlen) und lege ihn zu einem Gegner (höchstens 1 je Gegner). Du bekommst +1 Glaube, der Gegner verliert 1 Glaube.',
                'Ausweisen: Der Gegner darf in seinem Zug 2 Gold zahlen, dann geht der Missionar zurück auf die Hand seines Besitzers.',
                ('i', 'Missionare greifen nicht an und blocken nicht.')], 'GR-3'),
]

def schreibe():
    pfad = os.path.join(AUS, '3_Erweiterung_Goetter_und_Glaube_Karten.pdf')
    c = canvas.Canvas(pfad, pagesize=A4); c.setTitle('Volk Götter & Glaube – Karten'); c.setAuthor('Volk')
    gs = str(RL.GLAUBE_SIEG)
    def blatt(titel, rueck, fronten):
        for seite in ('r', 'v'):
            for i, fn in enumerate(fronten):
                col, row = i % 3, i // 3
                c.saveState(); c.translate(RX + col * CW, PH - RY - (row + 1) * CH)
                p = c.beginPath(); p.rect(0, 0, CW, CH); c.clipPath(p, stroke=0, fill=0)
                (rueck if seite == 'r' else fn)(c)
                c.restoreState()
            c.setFillColor(hexc('#9a9488')); c.setFont('DV', 5.5)
            c.drawCentredString(PW / 2, PH - 9 * mm, '%s · %s' % (titel, 'RÜCKSEITE (zuerst drucken, dann Blatt wenden)' if seite == 'r' else 'VORDERSEITE'))
            c.showPage()
    for n, r in enumerate(REL):
        rid = r['id']; k = {x['id']: x for x in RKARTEN if x['religion'] == rid}
        folge = [k[rid + '_heiligtum'], k[rid + '_tempel'], k[rid + '_halle'], k[rid + '_staette'], k[rid + '_prophet'], k[rid + '_missionar1'], k[rid + '_missionar2']]
        fr = [lambda c, rid=rid: tafelkarte(c, rid)] + [lambda c, x=x: karten.zeichne_vorn(c, x) for x in folge] + [lambda c, rid=rid: uebersicht(c, rid)]
        blatt('Religion %s · Blatt %d von 9' % (r['name'], n + 1), lambda c, rid=rid: ruecken(c, rid), fr)
    fr = [lambda c, e=e: ereigniskarte(c, e) for e in RL.EREIGNISSE] + [lambda c, t=t, a=a, nr=nr: regelkarte(c, t, [x.replace('<GS>', gs).replace('<GSV>', str(RL.GLAUBE_SIEG_VK)) if isinstance(x, str) else x for x in a], nr) for t, a, nr in REGELKARTEN]
    blatt('Glaube-Ereignisse & Regelkarten · Blatt 9 von 9', ruecken_ereignis, fr)
    c.save(); return pfad

if __name__ == '__main__':
    print(schreibe(), 'ok')
