"""Erzeugt die Druckbögen der Karten: je Blatt erst die Rückseite, dann die Vorderseite (A4, 3 x 3 Karten à 63 x 88 mm, ohne Schnittmarken)."""
import os, sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import karten
from lib import *

AUS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, '..', 'ausgabe')
os.makedirs(AUS, exist_ok=True)
PW, PH = A4
RX, RY = (PW - 3 * CW) / 2, (PH - 3 * CH) / 2
TYPREIHE = {'einheit': 0, 'gebaeude': 1, 'land': 2}
ROEM_ST = {1: 'I', 2: 'II', 3: 'III'}

def alle_karten():
    stapel = {1: [], 2: [], 3: []}
    for k in SATZ['karten']:
        for i in range(k['kopien']): stapel[k['stapel']].append(dict(k))
    for st in stapel:
        stapel[st].sort(key=lambda k: (TYPREIHE[k['typ']], k['zeitalter'], k['name']))
        zaehler = {}
        for n, k in enumerate(stapel[st], 1): k['nr'] = '%s-%03d' % (ROEM_ST[st], n)
    welt = [dict(w) for w in SATZ['wunder']] + [dict(s) for s in SATZ['staaten']] + [dict(e) for e in SATZ['ereignisse']]
    for n, k in enumerate(welt, 1): k['nr'] = 'W-%02d' % n
    return stapel, welt

def schreibe(dateiname, karten_liste, ruecken_stapel, titel):
    pfad = os.path.join(AUS, dateiname)
    c = canvas.Canvas(pfad, pagesize=A4); c.setTitle(titel); c.setAuthor('Volk')
    n_blatt = (len(karten_liste) + 8) // 9
    for b in range(n_blatt):
        teil = karten_liste[b * 9:(b + 1) * 9]
        for seite in ('rueck', 'vorn'):
            for i, k in enumerate(teil):
                col, row = i % 3, i // 3
                x = RX + col * CW; y = PH - RY - (row + 1) * CH
                c.saveState(); c.translate(x, y)
                p = c.beginPath(); p.rect(0, 0, CW, CH); c.clipPath(p, stroke=0, fill=0)
                if seite == 'rueck': karten.zeichne_ruecken(c, ruecken_stapel)
                else: karten.zeichne_vorn(c, k)
                c.restoreState()
            c.setFillColor(hexc('#9a9488')); c.setFont('DV', 5.5)
            c.drawCentredString(PW / 2, PH - 9 * mm, '%s · Blatt %d von %d · %s' % (titel, b + 1, n_blatt, 'RÜCKSEITE (zuerst drucken, dann Blatt wenden)' if seite == 'rueck' else 'VORDERSEITE'))
            c.showPage()
    c.save()
    return pfad, n_blatt

if __name__ == '__main__':
    stapel, welt = alle_karten()
    erg = []
    for st, name in ((1, 'Stapel_I'), (2, 'Stapel_II'), (3, 'Stapel_III')):
        erg.append(schreibe('1_Grundspiel_Karten_%s.pdf' % name, stapel[st], st, 'Volk Karten Stapel ' + ROEM_ST[st]))
    erg.append(schreibe('1_Grundspiel_Karten_Welt.pdf', welt, 0, 'Volk Karten Welt (Wunder, Stadtstaaten, Ereignisse)'))
    for p, n in erg: print(os.path.basename(p), n, 'Blätter', round(os.path.getsize(p) / 1e6, 1), 'MB')
