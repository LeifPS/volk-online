"""Rückseite, Info- und Übersichtskarte für die Volkskarten + Druckbogen 1_Grundspiel_Volkskarten.pdf (11 Karten je Volk)."""
import os, sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from lib import *
import karten
from karten import PAPIER
from volk_karten import nach_volk, RAHMEN, FARBE, NAME, ROEM

AUS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, '..', 'ausgabe')
os.makedirs(AUS, exist_ok=True)
PW, PH = A4
RX, RY = (PW - 3 * CW) / 2, (PH - 3 * CH) / 2
VOELKER = {v['id']: v for v in SATZ['voelker']}
FG = lambda f: '#ffffff' if sum(spr._rgb(f)[i] * w for i, w in enumerate((.299, .587, .114))) < 150 else '#2b2118'

def ruecken(c, vid):
    f = RAHMEN[vid]; fv = FARBE[vid]
    c.setFillColor(hexc(f)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 3.2 * mm, 3.2 * mm, CW - 6.4 * mm, CH - 6.4 * mm, 2.2 * mm, fill=hell(fv, .88))
    rrect(c, 5.2 * mm, 5.2 * mm, CW - 10.4 * mm, CH - 10.4 * mm, 1.6 * mm, stroke=f, lw=.9)
    zentriert(c, 'VOLK', CW / 2, CH - 21 * mm, 'PXB', 30, dunkel(f, .2))
    zentriert(c, 'Volkskarten', CW / 2, CH - 28 * mm, 'PX', 10.5, dunkel(f, .2))
    zeichne_bild(c, 'stadt:stadt@2@3', 11 * mm, 24 * mm, CW - 22 * mm, 30 * mm, farbe=fv, zuschnitt=True)
    nm = VOELKER[vid]['name'].upper()
    s = fit(c, nm, 'PXB', 11, 7, CW - 14 * mm)
    zentriert(c, nm, CW / 2, 15.5 * mm, 'PXB', s, dunkel(f, .2))
    zentriert(c, 'nur für dieses Volk', CW / 2, 10.8 * mm, 'DV', 5.6, dunkel(f, .1))
    zentriert(c, 'GRUNDSPIEL', CW / 2, CH - 34 * mm, 'SS', 5.6, dunkel(f, .1))

def info(c, vid):
    v = VOELKER[vid]; f = RAHMEN[vid]; fv = FARBE[vid]
    c.setFillColor(hexc(f)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 2.2 * mm, 2.2 * mm, CW - 4.4 * mm, CH - 4.4 * mm, 2.2 * mm, fill=PAPIER)
    c.setFillColor(hexc(fv)); c.rect(2.2 * mm, CH - 17 * mm, CW - 4.4 * mm, 14.8 * mm, stroke=0, fill=1)
    nm = v['name']; s = fit(c, nm, 'PXB', 12, 7, CW - 12 * mm)
    zentriert(c, nm, CW / 2, CH - 9.2 * mm, 'PXB', s, FG(fv))
    zentriert(c, 'Herrscher: ' + v['herrscher'], CW / 2, CH - 14.2 * mm, 'DV', 5.6, FG(fv))
    zeichne_bild(c, 'stadt:stadt@0@2', 12 * mm, 52 * mm, CW - 24 * mm, 20 * mm, farbe=fv, zuschnitt=True)
    zentriert(c, 'VOLKSFÄHIGKEIT', CW / 2, 48.5 * mm, 'PXB', 8.5, dunkel(f, .25))
    ab = [v['text'][0], ('i', v['beschreibung'])]
    karten.text_block(c, ab, 5.0 * mm, 46.0 * mm, CW - 10.0 * mm, 22 * mm)
    zentriert(c, 'Start: 3 Gold · 5 Karten · Volkskarte I', CW / 2, 8.2 * mm, 'DV', 5.4, '#6a6458')
    karten.fuss(c, 'VK-' + vid[:2].upper(), 0, f, 0)

def liste(c, vid):
    f = RAHMEN[vid]; fv = FARBE[vid]; ks = nach_volk()[vid]
    c.setFillColor(hexc(f)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 2.2 * mm, 2.2 * mm, CW - 4.4 * mm, CH - 4.4 * mm, 2.2 * mm, fill=PAPIER)
    zentriert(c, 'DEINE VOLKSKARTEN', CW / 2, CH - 8.3 * mm, 'PXB', 9.5, dunkel(f, .25))
    y = CH - 12.5 * mm
    for k in ks:
        za_icon(c, k['zeitalter'], 8.3 * mm, y - 2.0 * mm, 5.0 * mm)
        s = fit(c, k['name'] + ' (E)', 'DVB', 6.4, 4.8, 33 * mm)
        links(c, k['name'] + (' (E)' if k['typ'] == 'einheit' else ' (G)'), 13.5 * mm, y - 3.0 * mm, 'DVB', s, '#2b2118')
        kreis(c, CW - 9 * mm, y - 2.3 * mm, 2.5 * mm, fill='#fff3c4', stroke=dunkel(f, .1), lw=.6)
        zentriert(c, str(k['kosten']), CW - 9 * mm, y - 3.9 * mm, 'PXB', 6.0 if k['kosten'] < 10 else 5.2, '#2b2118')
        y -= 5.3 * mm
    zentriert(c, 'E = Einheit, G = Gebäude. Beim Aufstieg bekommst du die Karte.', CW / 2, 11.0 * mm, 'DV', 4.8, '#6a6458')
    zentriert(c, 'Sie zählt zum Handlimit, lässt sich ablegen (Gold)', CW / 2, 8.6 * mm, 'DV', 4.8, '#6a6458')
    zentriert(c, 'und ist weg, wenn sie zerstört wird.', CW / 2, 5.9 * mm, 'DV', 4.8, '#6a6458')

def vorn(c, k):
    t = k['typ']
    if t == 'info': info(c, k['volk'])
    elif t == 'liste': liste(c, k['volk'])
    else: karten.zeichne_vorn(c, k)

def schreibe():
    pfad = os.path.join(AUS, '1_Grundspiel_Volkskarten.pdf')
    c = canvas.Canvas(pfad, pagesize=A4); c.setTitle('Volk Volkskarten'); c.setAuthor('Volk')
    d = nach_volk(); reihenfolge = [v['id'] for v in SATZ['voelker']]
    teile = []
    for vid in reihenfolge:
        alle = [dict(info=1, typ='info', volk=vid)] + [dict(k) for k in d[vid]] + [dict(typ='liste', volk=vid)]
        for j in range(0, len(alle), 9): teile.append((vid, alle[j:j + 9], j // 9 + 1, (len(alle) + 8) // 9))
    for n, (vid, teil, bj, bn) in enumerate(teile, 1):
        for seite in ('rueck', 'vorn'):
            for i, k in enumerate(teil):
                col, row = i % 3, i // 3
                x = RX + col * CW; y = PH - RY - (row + 1) * CH
                c.saveState(); c.translate(x, y)
                p = c.beginPath(); p.rect(0, 0, CW, CH); c.clipPath(p, stroke=0, fill=0)
                if seite == 'rueck': ruecken(c, vid)
                else: vorn(c, k)
                c.restoreState()
            c.setFillColor(hexc('#9a9488')); c.setFont('DV', 5.5)
            c.drawCentredString(PW / 2, PH - 9 * mm, 'Volkskarten %s · Teil %d von %d · Blatt %d von %d · %s' % (VOELKER[vid]['name'], bj, bn, n, len(teile), 'RÜCKSEITE (zuerst drucken, dann Blatt wenden)' if seite == 'rueck' else 'VORDERSEITE'))
            c.showPage()
    c.save(); return pfad

if __name__ == '__main__':
    print(schreibe(), 'ok')
