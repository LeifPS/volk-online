"""Druck der Erweiterung 3 · Zivilisation: 4_Erweiterung_Zivilisation_Karten.pdf und _Regeln.pdf"""
import os, sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from lib import *
import karten, civ
from karten import PAPIER, geruest, typzeile, fuss, text_block

AUS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, '..', 'ausgabe')
os.makedirs(AUS, exist_ok=True)
PW, PH = A4
RX, RY = (PW - 3 * CW) / 2, (PH - 3 * CH) / 2
REG, PER, NAT = civ.baue()

def ruecken(c, typ):
    f = civ.RAHMEN[typ]; fv = civ.FARBEN[typ]
    c.setFillColor(hexc(f)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 3.2 * mm, 3.2 * mm, CW - 6.4 * mm, CH - 6.4 * mm, 2.2 * mm, fill=hell(fv, .88))
    rrect(c, 5.2 * mm, 5.2 * mm, CW - 10.4 * mm, CH - 10.4 * mm, 1.6 * mm, stroke=f, lw=.9)
    titel = {'regierung': 'STAAT', 'person': 'GENIES', 'natur': 'NATUR'}[typ]
    zentriert(c, titel, CW / 2, CH - 21 * mm, 'PXB', 27, dunkel(f, .2))
    zentriert(c, 'Zivilisation', CW / 2, CH - 28 * mm, 'PX', 9.5, dunkel(f, .2))
    zentriert(c, 'ERWEITERUNG 3', CW / 2, CH - 34 * mm, 'SS', 5.6, dunkel(f, .1))
    key, kw = {'regierung': ('civ:reg_krone', (30, 26)), 'person': ('civ:person_wissenschaftler', (22, 32)), 'natur': ('deko:gebirge', (34, 22))}[typ]
    zeichne_bild(c, key, (CW - kw[0] * mm) / 2, 38 * mm - (kw[1] * mm - 26 * mm) / 2 - 14 * mm, kw[0] * mm, kw[1] * mm, farbe=fv, zuschnitt=True)
    nm = {'regierung': 'REGIERUNGEN', 'person': 'GROSSE PERSÖNLICHKEITEN', 'natur': 'NATURWUNDER'}[typ]
    s = fit(c, nm, 'PXB', 10, 5.5, CW - 14 * mm)
    zentriert(c, nm, CW / 2, 14.6 * mm, 'PXB', s, dunkel(f, .2))

def regelkarte(c, titel, absaetze, nr):
    f = civ.RAHMEN['regierung']
    c.setFillColor(hexc(f)); c.rect(0, 0, CW, CH, stroke=0, fill=1)
    rrect(c, 2.2 * mm, 2.2 * mm, CW - 4.4 * mm, CH - 4.4 * mm, 2.2 * mm, fill=PAPIER)
    zeichne_bild(c, 'civ:reg_krone', CW / 2 - 6 * mm, CH - 18.5 * mm, 12 * mm, 12 * mm, farbe=civ.FARBEN['regierung'], zuschnitt=True)
    zentriert(c, titel, CW / 2, CH - 22.5 * mm, 'PXB', 9.2, '#2b2118')
    text_block(c, absaetze, 5.0 * mm, CH - 26 * mm, CW - 10.0 * mm, CH - 36 * mm)
    fuss(c, nr, 0, f, 3)

REGELKARTEN = [('SO SPIELST DU CIV', [
    'Pro Zug darfst du höchstens <b>1 Karte</b> dieser Erweiterung nehmen.',
    'Regierung: Zahle ihre Kosten (ab dem genannten Zeitalter). Sie ersetzt deine alte.',
    'Persönlichkeit: Aus der offenen Reihe von 3, Kosten zahlen. Dauerhafte liegen vor dir (höchstens 3), einmalige wirken sofort.',
    'Naturwunder: Aus der offenen Reihe von 4. Du brauchst Zeitalter II und Land mit dem passenden Gelände.',
    ('i', 'Kultur, Einkommen und alle anderen Werte zählen wie bei Gebäuden.')], 'ZR-1')]

def blatt(c, titel, rueck, fronten):
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

def regelkarte_text(a):
    return [x.replace('<b>', '').replace('</b>', '') if isinstance(x, str) else x for x in a]

def schreibe():
    pfad = os.path.join(AUS, '4_Erweiterung_Zivilisation_Karten.pdf')
    c = canvas.Canvas(pfad, pagesize=A4); c.setTitle('Volk Zivilisation – Karten'); c.setAuthor('Volk')
    fr = [lambda c, k=k: karten.zeichne_vorn(c, k) for k in REG] + [lambda c, t=t, a=a, nr=nr: regelkarte(c, t, regelkarte_text(a), nr) for t, a, nr in REGELKARTEN]
    blatt(c, 'Regierungen · Blatt 1 von 4 (Satz je Spieler drucken)', lambda c: ruecken(c, 'regierung'), fr)
    blatt(c, 'Große Persönlichkeiten · Blatt 2 von 4', lambda c: ruecken(c, 'person'), [lambda c, k=k: karten.zeichne_vorn(c, k) for k in PER[:9]])
    blatt(c, 'Große Persönlichkeiten · Blatt 3 von 4', lambda c: ruecken(c, 'person'), [lambda c, k=k: karten.zeichne_vorn(c, k) for k in PER[9:]])
    blatt(c, 'Naturwunder · Blatt 4 von 4', lambda c: ruecken(c, 'natur'), [lambda c, k=k: karten.zeichne_vorn(c, k) for k in NAT])
    c.save(); return pfad

if __name__ == '__main__':
    print(schreibe(), 'ok')
