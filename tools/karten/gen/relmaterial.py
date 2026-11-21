"""Material + Regelheft der Religions-Erweiterung."""
import os, sys, json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from lib import *
import relspr, religionen as RL
from satz import D as _D
S = json.load(open(os.path.join(HIER, '..', 'kartensatz.json')))
AUS = os.path.join(HIER, '..', 'ausgabe'); GS = RL.GLAUBE_SIEG
VOELKER = S['voelker']

def material():
    pf = os.path.join(AUS, '3_Erweiterung_Goetter_und_Glaube_Material.pdf')
    W, H = landscape(A4)
    c = canvas.Canvas(pf, pagesize=(W, H)); c.setTitle('Volk Götter & Glaube – Glaubensleisten und Marker')
    c.setFillColor(hexc('#fbf7ec')); c.rect(0, 0, W, H, stroke=0, fill=1)
    zentriert(c, 'GLAUBENSLEISTEN', W / 2, H - 14 * mm, 'PXB', 17, '#6b1f3a')
    zentriert(c, 'Lege den Glaubensmarker auf dein aktuelles Glaubens-Feld. Bei %d gewinnst du sofort (mit Erweiterung 1: %d). Ausschneiden und neben die Volkstafel legen.' % (GS, RL.GLAUBE_SIEG_VK), W / 2, H - 20 * mm, 'DV', 7.6, '#6a6458')
    n = 13; zw = 17.5 * mm; x0 = (W - n * zw) / 2
    for i, v in enumerate(VOELKER[:5]):
        y = H - 36 * mm - i * 31 * mm; f = v['farbe']
        rrect(c, x0 - 22 * mm, y - 21 * mm, n * zw + 22 * mm + 3 * mm, 25 * mm, 2 * mm, fill=hell(f, .9), stroke=f, lw=1)
        links(c, v['name'].upper(), x0 - 19 * mm, y - 4 * mm, 'PXB', 8, dunkel(f, .3))
        zeichne_bild(c, 'rel:glaube_gross', x0 - 19 * mm, y - 18 * mm, 11 * mm, 11 * mm, farbe='#d8432b', zuschnitt=True)
        for k in range(n):
            x = x0 + k * zw; ziel = (k == GS); ziel_vk = (k == RL.GLAUBE_SIEG_VK)
            rrect(c, x + .8 * mm, y - 19 * mm, zw - 1.6 * mm, 20 * mm, 1.6 * mm, fill='#ffe9a8' if ziel else ('#ffd9cf' if ziel_vk else '#ffffff'), stroke=f, lw=.9 if not (ziel or ziel_vk) else 1.8)
            zentriert(c, str(k), x + zw / 2, y - 8.5 * mm, 'PXB', 14 if k < 10 else 12, '#2b2118')
            if ziel: zentriert(c, 'SIEG', x + zw / 2, y - 15.5 * mm, 'SS', 5.5, '#a02a14')
            if ziel_vk: zentriert(c, 'mit ERW. 1', x + zw / 2, y - 15.5 * mm, 'SS', 4.2, '#a02a14')
    c.showPage()
    c.setFillColor(hexc('#fbf7ec')); c.rect(0, 0, W, H, stroke=0, fill=1)
    zentriert(c, 'GLAUBENSMARKER & RELIGIONS-HILFE', W / 2, H - 14 * mm, 'PXB', 17, '#6b1f3a')
    zentriert(c, 'Marker ausschneiden (Kreise, Ø 18 mm). Für jedes Volk 1 Marker, dazu 4 Reserve.', W / 2, H - 20 * mm, 'DV', 7.6, '#6a6458')
    x = 22 * mm; y = H - 42 * mm
    for i, v in enumerate(VOELKER[:5]):
        for k in range(2):
            cx = x + i * 40 * mm + k * 20 * mm + 9 * mm
            kreis(c, cx, y, 9 * mm, fill=v['farbe'], stroke=dunkel(v['farbe'], .4), lw=1)
            zeichne_bild(c, 'rel:glaube_gross', cx - 6 * mm, y - 6 * mm, 12 * mm, 12 * mm, farbe='#ffffff', zuschnitt=True)
    y2 = y - 14 * mm
    zentriert(c, 'ÜBERSICHT DER 8 RELIGIONEN', W / 2, y2, 'PXB', 11, '#6b1f3a')
    y2 -= 5 * mm
    for i, r in enumerate(RL.REL):
        col, row = i % 2, i // 2
        bx = 18 * mm + col * 133 * mm; by = y2 - (row + 1) * 25 * mm
        rrect(c, bx, by, 128 * mm, 22.5 * mm, 2 * mm, fill=hell(r['farbe'], .88), stroke=r['rahmen'], lw=1)
        zeichne_bild(c, 'rel:%s:tempel' % r['id'], bx + 2 * mm, by + 1.5 * mm, 19 * mm, 19.5 * mm, farbe=r['farbe'], zuschnitt=True)
        links(c, r['name'], bx + 24 * mm, by + 16.5 * mm, 'PXB', 9, dunkel(r['rahmen'], .3))
        absatz(c, r['titel'] + ': ' + r['text'], bx + 24 * mm, by + 12.5 * mm, 101 * mm, 'DV', 6.3, 7.6, '#2b2118') if 'absatz' in globals() else None
    c.save(); return pf

INK = hexc('#2b2118')
T = ParagraphStyle('t', fontName='DV', fontSize=9.2, leading=12.4, textColor=INK, spaceAfter=3.2)
B = ParagraphStyle('b', parent=T, leftIndent=9, bulletIndent=0, spaceAfter=1.8)
H1 = ParagraphStyle('h1', fontName='PXB', fontSize=15, leading=18, textColor=hexc('#6b1f3a'), spaceBefore=7, spaceAfter=3.5)
H2 = ParagraphStyle('h2', fontName='PXB', fontSize=10.5, leading=13, textColor=INK, spaceBefore=4, spaceAfter=2)
Sm = ParagraphStyle('s', parent=T, fontSize=7.8, leading=10, textColor=hexc('#6a6458'))
C = ParagraphStyle('c', parent=T, fontSize=8.2, leading=10.6, spaceAfter=0)
p = lambda t: Paragraph(t, T); b = lambda t: Paragraph(t, B, bulletText='•')

def regelheft():
    pf = os.path.join(AUS, '3_Erweiterung_Goetter_und_Glaube_Regeln.pdf'); W, H = A4
    def seite(c, doc):
        c.saveState(); c.setFillColor(hexc('#fbf7ec')); c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(hexc('#6b1f3a')); c.rect(0, H - 12 * mm, W, 12 * mm, stroke=0, fill=1)
        links(c, 'VOLK – GÖTTER & GLAUBE', 15 * mm, H - 8.4 * mm, 'PXB', 11, '#ffffff'); rechts(c, 'ERWEITERUNG 2 · Regeln', W - 15 * mm, H - 8.2 * mm, 'PX', 9, '#ffffff')
        zentriert(c, 'Seite %d' % doc.page, W / 2, 7 * mm, 'DV', 7, '#9a9488'); c.restoreState()
    doc = BaseDocTemplate(pf, pagesize=A4, title='Volk – Götter & Glaube', author='Volk', leftMargin=15 * mm, rightMargin=15 * mm, topMargin=18 * mm, bottomMargin=14 * mm)
    doc.addPageTemplates([PageTemplate(id='a', frames=[Frame(15 * mm, 14 * mm, W - 30 * mm, H - 32 * mm, 0, 0, 0, 0)], onPage=seite)])
    st = []
    st += [Paragraph('Götter &amp; Glaube', H1), p('<b>Erweiterung 2</b> fügt dem Grundspiel <b>8 Religionen</b>, neue Gebäude, Missionare und einen <b>weiteren Siegweg</b> hinzu: den <b>Glaubenssieg</b>. Sie braucht nur das Grundspiel. Alles andere bleibt, wie im Grundspiel-Regelheft beschrieben. Erkennbar sind alle Karten am <b>Strahlenkranz</b> unten rechts.')]
    st += [Paragraph('Vorbereitung', H2), b('Mischt die <b>6 Glaube-Ereigniskarten</b> unter den Ereignisstapel des Grundspiels.'), b('Legt die 8 <b>Religionstafeln</b> offen in die Tischmitte. Jede Religion gibt es nur einmal. Die übrigen Karten jeder Religion (7 Stück) bleiben bei ihrer Tafel, bis sie jemand gründet.'), b('Jeder nimmt eine <b>Glaubensleiste</b> und einen Glaubensmarker seiner Farbe.')]
    st += [Paragraph('Glaube und Sieg', H2), p('Glaube hast du nur, wenn du eine Religion gegründet hast. Er ist die Summe aus:'),
           b('allen <b>Glaube-Flammen</b> auf deinen Gebäuden und Einheiten,'), b('<b>+1</b> für deine Religion selbst,'), b('<b>+1</b> für jeden deiner Missionare bei einem Gegner,'), b('<b>–1</b> für jeden fremden Missionar bei dir.'),
           p('Erreichst du <b>%d Glaube</b>, gewinnst du sofort, auch mitten im Zug. Spielst du zusätzlich mit <b>Erweiterung 1 (Volkskarten)</b>, genügen <b>%d Glaube</b>, denn mit Volkskarten geht das Spiel schneller. Kultursieg, Wissenschaftssieg und Eroberung gelten weiter.' % (GS, RL.GLAUBE_SIEG_VK))]
    st += [Paragraph('Religion gründen', H2), p('Einmal pro Spiel, in deinem Zug, ab <b>Zeitalter II</b>: Zahle <b>5 Gold</b> und lege <b>1 Handkarte</b> ab. Nimm eine freie Religionstafel und mische ihre 7 Karten als deinen <b>Religionsstapel</b>. Du darfst jetzt bei jedem Ziehen <b>1 Karte</b> von diesem Stapel statt vom normalen Stapel nehmen. Legst du eine Religionskarte ab, kommt sie unter den Religionsstapel (sie bringt kein Gold).'),
           p('Religionsgebäude und Prophet spielst du wie andere Karten (Kosten zahlen, in deine Auslage). Heiligtum ist Zeitalter I, Tempel II, Pilgerhalle IV, Heilige Stätte V, Prophet III.')]
    st += [Paragraph('Missionare', H2), p('Ein Missionar (Zeitalter II, 3 Gold) kommt <b>zu einem Gegner</b>: Lege ihn neben dessen Stadt. Je Gegner darf nur 1 Missionar von dir liegen. Du bekommst +1 Glaube, der Gegner verliert 1. Er kann ihn in seinem Zug für <b>2 Gold ausweisen</b>, dann geht der Missionar auf deine Hand zurück. Missionare kämpfen nicht.')]
    st += [Paragraph('Die 8 Religionen', H1)]
    rows = [[Paragraph('<b>Religion</b>', C), Paragraph('<b>Fähigkeit</b>', C), Paragraph('<b>Gebäude (Glaube · Wirkung)</b>', C)]]
    nm = {'F': 'Glaube', 'E': 'Eink.', 'K': 'Kultur', 'W': 'Wissen', 'S': 'Schutz', 'H': 'Heilung', 'A': 'Ausb.', 'HL': 'Handl.', 'G': 'Bauherr', 'Z': 'Ziehen'}
    for r in RL.REL:
        g = '; '.join('%s (%s)' % (n, ', '.join('%s %d' % (nm[k], v) for k, v in e.items())) for n, e, _ in r['karten'][:4])
        rows.append([Paragraph('<b>%s</b>' % r['name'], C), Paragraph('<b>%s:</b> %s' % (r['titel'], r['text']), C), Paragraph(g, C)])
    t = Table(rows, colWidths=[30 * mm, 64 * mm, 86 * mm], repeatRows=1)
    t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), .4, hexc('#c9bfa6')), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BACKGROUND', (0, 0), (-1, 0), hexc('#ecdcc0'))] + [('BACKGROUND', (0, i), (0, i), hexc(RL.REL[i - 1]['farbe']).clone(alpha=.35)) for i in range(1, 9)]))
    st += [t, Spacer(1, 4)]
    st += [Paragraph('Glaube-Ereignisse', H2), p('Sie werden wie normale Ereignisse aufgedeckt und gelten für alle. <b>Pilgerzug:</b> Religiöse bekommen Gold. <b>Prophezeiung:</b> Wer den meisten Glauben hat, zieht 2 Karten. <b>Ketzerjagd:</b> Alle Missionare gehen zurück auf die Hand. <b>Heiliges Fest:</b> Religiöse +2 Gold, alle anderen ziehen 1 Karte. <b>Wundersame Heilung:</b> alle Städte heilen 3. <b>Glaubenskrieg:</b> Wer den meisten Glauben hat, zahlt 3 Gold. Bei Gleichstand um den meisten Glauben passiert nichts.')]
    st += [Paragraph('Zusammen mit Erweiterung 1 (Volkskarten)', H2), p('Beide Erweiterungen stören sich nicht. Glaubensziel: 13, mit Volkskarten 12. Als Handkarte zum Gründen darfst du keine Volkskarte ablegen (auch wenn man Volkskarten sonst gegen Gold ablegen kann). Volkskarten bringen keinen Glauben und zählen zum Handlimit; Religionskarten auf der Hand zählen ebenfalls dazu.')]
    st += [Paragraph('Hinweis zum Test', H2), Paragraph('Die Erweiterung wurde nur mit Computer-Spielern durchgerechnet (je 120 Partien je Spielerzahl), noch nicht von Menschen gespielt oder gedruckt getestet. Weil das Grundspiel jetzt schon bei <b>12 Kultur</b> endet, gewinnt der Glaubenssieg selten: <b>zu dritt und zu viert in etwa jeder 10. bis 15. Partie</b>, <b>zu zweit</b> fast nie. Wer den Glaubenssieg öfter erleben will, senkt das Glaubensziel um 1–2. Die Religionen liegen nicht ganz gleichauf; die Stichprobe ist aber zu klein für eine Rangliste.', Sm)]
    doc.build(st); return pf

if __name__ == '__main__':
    print(material()); print(regelheft())
