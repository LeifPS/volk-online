"""Volkstafeln (A4 quer, Vorderseite = Tafel, Rückseite = Spielhilfe) und Spielmarken."""
import os, sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from lib import *
import karten

AUS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, '..', 'ausgabe')
os.makedirs(AUS, exist_ok=True)
PW, PH = landscape(A4)
FM = lambda f: '#ffffff' if sum(spr._rgb(f)[i] * w for i, w in enumerate((.299, .587, .114))) < 150 else '#2b2118'

def tafel_vorn(c, v):
    f = v['farbe']; fg = FM(f)
    c.setFillColor(hexc(PAPIER := '#fbf7ec')); c.rect(0, 0, PW, PH, stroke=0, fill=1)
    c.setFillColor(hexc(f)); c.rect(0, PH - 30 * mm, PW, 30 * mm, stroke=0, fill=1)
    links(c, v['name'].upper(), 14 * mm, PH - 19 * mm, 'PXB', 30, fg)
    rechts(c, 'Herrscher: ' + v['herrscher'], PW - 14 * mm, PH - 13 * mm, 'PX', 12, fg)
    rechts(c, 'Volkstafel · VOLK – Grundspiel', PW - 14 * mm, PH - 22 * mm, 'DV', 7.5, fg)
    zeichne_bild(c, 'stadt:stadt@0@3', 12 * mm, 120 * mm, 70 * mm, 54 * mm, farbe=f, zuschnitt=True)
    rrect(c, 88 * mm, 122 * mm, 195 * mm, 50 * mm, 3 * mm, fill=hell(f, .86), stroke=f, lw=1.2)
    links(c, 'VOLKSFÄHIGKEIT', 94 * mm, 164 * mm, 'PXB', 13, dunkel(f, .4))
    y = absatz(c, v['text'][0], 94 * mm, 161 * mm, 183 * mm, 'DVB', 11.5, 14.5, '#2b2118')
    absatz(c, v['beschreibung'], 94 * mm, 141 * mm, 183 * mm, 'DVI', 9.5, 12, '#5a5448')
    absatz(c, 'Start: 3 Gold · 5 Handkarten von Stapel I · Lebenspunkte 25 · Kultur 0 · Zeitalter I', 94 * mm, 128 * mm, 183 * mm, 'DV', 8, 10, '#5a5448')
    # Lebenspunkte
    icon(c, 'hp', 12 * mm, 105.5 * mm, 7 * mm)
    links(c, 'STADT · LEBENSPUNKTE', 20 * mm, 108 * mm, 'PXB', 11, '#2b2118')
    links(c, 'Herz-Marker auf deine aktuellen Lebenspunkte. Bei 0 ist deine Stadt erobert.', 80 * mm, 108.3 * mm, 'DV', 7.2, '#6a6458')
    bw = 10.3 * mm; x0 = 13 * mm
    for i in range(1, 26):
        x = x0 + (i - 1) * bw
        rrect(c, x, 94 * mm, bw - .8 * mm, 10 * mm, 1.2 * mm, fill='#ffe3e0' if i % 5 == 0 else '#ffffff', stroke='#b5483b', lw=.7)
        zentriert(c, str(i), x + (bw - .8 * mm) / 2, 97.2 * mm, 'PXB', 8.5 if i < 10 else 8, '#b5483b')
    # Kultur
    icon(c, 'kultur', 12 * mm, 80.5 * mm, 7 * mm)
    links(c, 'KULTUR', 20 * mm, 83 * mm, 'PXB', 11, '#2b2118')
    links(c, 'Kultur-Marker: Summe der Kultur auf deinen Gebäuden, Wundern und Verbündeten.', 80 * mm, 83.3 * mm, 'DV', 7.2, '#6a6458')
    n_k = R['kultur_sieg']; kw = (271 * mm) / (n_k + 1); x0 = 13 * mm
    for i in range(0, n_k + 1):
        x = x0 + i * kw
        sieg = i == n_k
        rrect(c, x, 66 * mm, kw - .9 * mm, 12.5 * mm, 1.5 * mm, fill='#ffe9a8' if sieg else '#ffffff', stroke='#7a4fb5', lw=.7)
        zentriert(c, str(i), x + (kw - .9 * mm) / 2, 70.6 * mm, 'PXB', 11 if i < 10 else 10, '#7a4fb5')
    zentriert(c, 'SIEG', x0 + n_k * kw + (kw - .9 * mm) / 2, 75.3 * mm, 'SS', 4.6, '#b8860b')
    # Zeitalter
    icon(c, 'zeitalter', 12 * mm, 52.8 * mm, 7 * mm)
    links(c, 'ZEITALTER', 20 * mm, 55.3 * mm, 'PXB', 11, '#2b2118')
    links(c, 'Setze deinen Zeitalter-Marker. Nach jedem Aufstieg bekommst du +1 Einkommen und besseren Zugriff auf die Stapel.', 53 * mm, 55.6 * mm, 'DV', 7.2, '#6a6458')
    gap = 1.0 * mm; x0 = 12 * mm; cw_ = (PW - 2 * x0 - 10 * gap) / 11
    for z in range(11):
        x = x0 + z * (cw_ + gap); zf = ZA[z]['farbe']
        rrect(c, x, 8 * mm, cw_, 42 * mm, 2 * mm, fill=hell(zf, .84), stroke=zf, lw=1)
        za_icon(c, z, x + 2 * mm, 43.6 * mm, 5.6 * mm)
        nm = ZA[z]['name']; sz = fit(c, nm, 'PXB', 7.6, 4.6, cw_ - 3.5 * mm)
        links(c, nm, x + 2 * mm, 37.6 * mm, 'PXB', sz, '#2b2118')
        zeichne_bild(c, 'stadt:stadt@%d@2' % z, x + 1.8 * mm, 24.6 * mm, cw_ - 3.6 * mm, 11.6 * mm, farbe=zf, zuschnitt=True)
        auf = ('Aufstieg: %d Gold' % R['aufstieg'][z]) if z < 10 else ('Sieg: %d Gold' % R['wissen_sieg'])
        links(c, 'Einkommen: %d+' % (R['basis_einkommen'] + z), x + 2 * mm, 21.4 * mm, 'DV', 5.2, '#4a443a')
        links(c, auf, x + 2 * mm, 17.8 * mm, 'DVB', 5.2, '#4a443a')
        stp = karten.STAPELNAME[R['stapel_von_zeitalter'][z]].split(' · ')[0]
        links(c, 'zieht: ' + stp.title(), x + 2 * mm, 14.2 * mm, 'DV', 4.8, '#7a7468')
        c.saveState(); c.setStrokeColor(hexc(dunkel(zf, .2))); c.setLineWidth(.6); c.setDash(1.2, 1.2)
        c.circle(x + cw_ / 2, 11 * mm, 0.01 * mm, stroke=0, fill=0); c.restoreState()
    zentriert(c, 'VOLK – Grundspiel · Marker aus dem Marker-Bogen', PW / 2, 3.6 * mm, 'DV', 5.5, '#9a9488')

def spalte(c, x, y, breite, bloecke):
    for kopf, absaetze in bloecke:
        links(c, kopf, x, y - 4 * mm, 'PXB', 10.5, '#2b2118'); y -= 7.6 * mm
        for a in absaetze:
            if isinstance(a, tuple): t, fnt = a[1], 'DVI'
            else: t, fnt = a, 'DV'
            if len(t) > 3 and t.startswith('• '):
                y2 = absatz(c, t, x, y, breite, fnt, 7.4, 9.0, '#2b2118', fett_bis=True) if False else None
            h = absatz_hoehe(t, breite, fnt, 7.4, 9.0)
            absatz(c, t, x, y, breite, fnt, 7.4, 9.0, '#2b2118', fett_bis=True)
            y -= h + 1.8 * mm
        y -= 2.4 * mm
    return y

SPIELHILFE = [
    [('DEIN ZUG', [
        '1. Aufwecken: Alle Einheiten aufrichten. Einheiten aus der Kaserne an die Front. Deine Stadt heilt (Heilung + Sanitäter).',
        '2. Einkommen: 2 + Zeitalter-Nummer (I = 0 … VII = 6) + Ertrag aller Land-Karten + Einkommen von Gebäuden, Wundern, Verbündeten und Handels-Einheiten. Nimm so viel Gold.',
        '3. Ziehen: 2 Karten vom Stapel deines Zeitalters (I–II: Stapel I · III–IV: Stapel II · V–VII: Stapel III · VIII–XI: Stapel IV) oder von einem niedrigeren. Du darfst aufteilen.',
        '4. Aktionen in beliebiger Reihenfolge, so oft du kannst: 1 Land spielen (gratis) · Karten spielen · Wunder kaufen · Aufstieg (1× pro Runde) · Tribut · Karten ablegen · Angreifen.',
        '5. Zugende: Höchstens 7 Handkarten (+ Handlimit-Bonus), den Rest ablegen. Nach der letzten Spielerin / dem letzten Spieler der Runde wird 1 Ereigniskarte aufgedeckt. Die Krone wandert weiter.']),
     ('KARTEN SPIELEN', [
         'Zahle die Goldkosten (Zahl im Kreis links oben). Das Zeitalter der Karte darf nicht höher sein als deines.',
         'Einheiten kommen in die Kaserne (neu), Gebäude in deine Auslage. Jedes Gebäude gibt es nur 1× pro Spieler. Steht „Benötigt“ darauf, muss das Gebäude schon in deiner Auslage liegen.']) ],
    [('ROHSTOFFE', [
        '„braucht“-Symbole: Du brauchst ein Land, Gebäude oder einen Verbündeten mit diesem Symbol. Fehlt dir 1 Rohstoff, darfst du ihn für 3 Gold zukaufen (höchstens 1 je Karte). Küste und Flugfeld kann man nicht zukaufen.']),
     ('KAMPF', [
         'Angreifen: Aufrechte Einheiten an der Front greifen die Stadt eines Gegners an und werden dann gedreht (erschöpft). Erschöpfte Einheiten können nicht blocken. Einheiten in der Kaserne dürfen blocken, aber nicht angreifen.',
         'Blocken: Der Verteidiger blockt jeden Angreifer mit höchstens 1 aufrechten Einheit. Höhere Stärke gewinnt, die andere wird abgelegt. Gleichstand: beide ablegen. Nicht geblockte Angreifer: Die Stadt verliert so viele Lebenspunkte wie die Stärke, minus Schutz (mindestens 1).',
         'Schuss: Fernkämpfer zerstören 1 gegnerische Einheit, wenn Fern mindestens so hoch ist wie deren Stärke. Kein Gegenschlag. Belagerer dürfen stattdessen die Stadt beschießen (Schaden = Fern, nicht blockbar).',
         'Fliegend, Luftabwehr, Tarnung, Ansturm, Ramme: siehe Karte.']),
     ('NEULINGSSCHUTZ', ['Solange noch keine 3 Ereigniskarten aufgedeckt wurden, darf niemand angreifen oder schießen. Barbaren ignorieren den Schutz!'])],
    [('SIEG', [
        'Du gewinnst sofort, wenn du %d Kultur erreichst, alle anderen Städte erobert sind (Lebenspunkte 0) – oder wenn du im Sternenzeitalter %d Gold für den Aufstieg zahlst (Wissenschaft).' % (R['kultur_sieg'], R['wissen_sieg'])]),
     ('WUNDER', ['Offen ausliegend. Kaufe sie mit Gold, Marmor-Symbol und passendem Zeitalter. Jedes Wunder gibt es nur 1× im Spiel und bringt Kultur.']),
     ('STADTSTAATEN', ['Drei liegen offen aus. Zahle 6 Gold Tribut in deinem Zug und lege dir eine davon vor dich (höchstens 2 Verbündete). Dann wird eine neue offen gelegt.']),
     ('EREIGNISSE UND BARBAREN', [
         'Wetter-Ereignisse gelten für alle. Bei Barbaren wird der Spieler mit den wenigsten Kampfeinheiten überfallen: Stärke = Zeitalter-Nummer + Zahl auf der Karte. Er stellt 1 Einheit entgegen (gleich stark oder stärker: gewonnen + Beute, sonst verloren). Ohne Einheit: Schaden an der Stadt bzw. Goldverlust.']),
     ('ABLEGEN FÜR GOLD', ['Bis zu 2 Handkarten pro Zug ablegen: je 1 Gold.'])],
]

def tafel_hinten(c, v):
    f = v['farbe']
    c.setFillColor(hexc('#fbf7ec')); c.rect(0, 0, PW, PH, stroke=0, fill=1)
    c.setFillColor(hexc(f)); c.rect(0, PH - 14 * mm, PW, 14 * mm, stroke=0, fill=1)
    links(c, 'SPIELHILFE', 14 * mm, PH - 10 * mm, 'PXB', 18, FM(f))
    rechts(c, 'VOLK – Grundspiel', PW - 14 * mm, PH - 9.5 * mm, 'PX', 11, FM(f))
    xs = [12 * mm, 106 * mm, 200 * mm]
    for x, bl in zip(xs, SPIELHILFE):
        spalte(c, x, PH - 20 * mm, 84 * mm, bl)

def marke(c, x, y, r, rand, fuell='#ffffff'):
    c.saveState(); c.setFillColor(hexc(fuell)); c.setStrokeColor(hexc(rand)); c.setLineWidth(1.6)
    c.circle(x, y, r, stroke=1, fill=1); c.restoreState()
    c.saveState(); c.setStrokeColor(hexc('#bdb6a6')); c.setLineWidth(.25); c.circle(x, y, r + 1.2 * mm, stroke=1, fill=0); c.restoreState()  # Schneidelinie

def marker_pdf(pfad):
    c = canvas.Canvas(pfad, pagesize=A4); c.setTitle('Volk Spielmarken')
    W, H = A4
    # Seite 1: Gold
    def gold_seite(anzahl1, anzahl5):
        pass
    links(c, 'GOLD · Münzen ausschneiden', 12 * mm, H - 13 * mm, 'PXB', 14, '#2b2118')
    x0, y0 = 20 * mm, H - 30 * mm
    # Münzen zu 1 (Ø 17 mm) – 11 pro Reihe
    r1 = 8.5 * mm; r5 = 11 * mm
    n = 0
    for row in range(7):
        for col in range(9):
            x = 15 * mm + r1 + col * (2 * r1 + 2.8 * mm); y = H - 25 * mm - r1 - row * (2 * r1 + 2.8 * mm)
            marke(c, x, y, r1, '#b8860b', '#fff0b0')
            zeichne_bild(c, 'ui:gold', x - 4.6 * mm, y - 1.5 * mm, 9.2 * mm, 6 * mm, zuschnitt=False) if False else None
            icon(c, 'gold', x - 4.2 * mm, y - 4.6 * mm, 8.4 * mm)
            n += 1
    ytop = H - 25 * mm - 7 * (2 * r1 + 2.8 * mm)
    links(c, '5er-Münzen (Ø 22 mm)', 12 * mm, ytop - 2 * mm, 'PXB', 10, '#2b2118')
    for row in range(4):
        for col in range(7):
            x = 15 * mm + r5 + col * (2 * r5 + 3 * mm); y = ytop - 8 * mm - r5 - row * (2 * r5 + 3 * mm)
            marke(c, x, y, r5, '#5b6b8c', '#dfe6f2')
            icon(c, 'gold', x - 5 * mm, y - 1.0 * mm, 10 * mm)
            zentriert(c, "5", x, y - 8.2 * mm, "PXB", 14, '#2b2118')
    zentriert(c, '63 Münzen zu 1 · 28 Münzen zu 5 · mehr als genug für 4 Spieler', W / 2, 8 * mm, 'DV', 6, '#9a9488')
    c.showPage()
    # Seite 2: Völker-Marker
    links(c, 'VÖLKER-MARKER · pro Volk Herz, Kultur, Zeitalter', 12 * mm, H - 13 * mm, 'PXB', 14, '#2b2118')
    y = H - 30 * mm
    for v in SATZ['voelker']:
        f = v['farbe']
        links(c, v['name'], 14 * mm, y - 1 * mm, 'PXB', 11, '#2b2118')
        for i, (ik, txt) in enumerate((('hp', 'Lebenspunkte'), ('kultur', 'Kultur'), ('zeitalter', 'Zeitalter'))):
            x = 74 * mm + i * 34 * mm
            marke(c, x, y - 4 * mm, 10 * mm, f, '#ffffff')
            icon(c, ik, x - 5.5 * mm, y - 4 * mm - 5.5 * mm + 1 * mm, 11 * mm)
            zentriert(c, txt, x, y - 4 * mm - 8.2 * mm, 'DV', 4.8, dunkel(f, .3))
        y -= 29 * mm
    # Krone
    links(c, 'Startspieler-Krone', 14 * mm, y - 1 * mm, 'PXB', 11, '#2b2118')
    marke(c, 74 * mm, y - 4 * mm, 11 * mm, '#b8860b', '#fff0b0'); icon(c, 'krone', 74 * mm - 6.5 * mm, y - 4 * mm - 5.5 * mm, 13 * mm)
    zentriert(c, 'Wer die Krone hat, deckt am Rundenende die Ereigniskarte auf.', W / 2 + 25 * mm, y - 12 * mm, 'DV', 6, '#6a6458')
    zentriert(c, 'Schneide die Marker entlang der feinen grauen Linie aus.', W / 2, 8 * mm, 'DV', 6, '#9a9488')
    c.showPage(); c.save()

if __name__ == '__main__':
    pfad = os.path.join(AUS, '1_Grundspiel_Volkstafeln.pdf')
    c = canvas.Canvas(pfad, pagesize=landscape(A4)); c.setTitle('Volk Volkstafeln')
    for v in SATZ['voelker']:
        c.setFillColor(hexc('#9a9488')); c.setFont('DV', 5.5)
        tafel_hinten(c, v); c.setFillColor(hexc('#9a9488')); c.drawCentredString(PW / 2, 4 * mm, 'Rückseite (zuerst drucken) · ' + v['name']); c.showPage()
        tafel_vorn(c, v); c.showPage()
    c.save()
    marker_pdf(os.path.join(AUS, '1_Grundspiel_Spielmarken.pdf'))
    print('ok')
