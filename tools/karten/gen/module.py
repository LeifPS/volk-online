"""Regelheft Erweiterung 1 (Volkskarten) + Modul-Übersicht (0_Modul_Uebersicht.pdf)."""
import os, sys, json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from lib import *
import religionen as RL
from volk_karten import nach_volk, NAME
S = json.load(open(os.path.join(HIER, '..', 'kartensatz.json')))
AUS = os.path.join(HIER, '..', 'ausgabe'); W, H = A4
INK = hexc('#2b2118')
T = ParagraphStyle('t', fontName='DV', fontSize=9.2, leading=12.4, textColor=INK, spaceAfter=3.2)
B = ParagraphStyle('b', parent=T, leftIndent=9, bulletIndent=0, spaceAfter=1.8)
Sm = ParagraphStyle('s', parent=T, fontSize=7.8, leading=10, textColor=hexc('#6a6458'))
C = ParagraphStyle('c', parent=T, fontSize=8.0, leading=10.2, spaceAfter=0)
CW_ = ParagraphStyle('cw', parent=C, textColor=hexc('#ffffff'))
p = lambda t: Paragraph(t, T); b = lambda t: Paragraph(t, B, bulletText='•')
def h1(t, f): return Paragraph(t, ParagraphStyle('h1', fontName='PXB', fontSize=15, leading=18, textColor=hexc(f), spaceBefore=7, spaceAfter=3.5))
def h2(t): return Paragraph(t, ParagraphStyle('h2', fontName='PXB', fontSize=10.5, leading=13, textColor=INK, spaceBefore=4, spaceAfter=2))

def doc_bauen(pfad, titel, kopf, rechts_t, farbe, story):
    def seite(c, doc):
        c.saveState(); c.setFillColor(hexc('#fbf7ec')); c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(hexc(farbe)); c.rect(0, H - 12 * mm, W, 12 * mm, stroke=0, fill=1)
        links(c, kopf, 15 * mm, H - 8.4 * mm, 'PXB', 11, '#ffffff'); rechts(c, rechts_t, W - 15 * mm, H - 8.2 * mm, 'PX', 9, '#ffffff')
        zentriert(c, 'Seite %d' % doc.page, W / 2, 7 * mm, 'DV', 7, '#9a9488'); c.restoreState()
    d = BaseDocTemplate(pfad, pagesize=A4, title=titel, author='Volk', leftMargin=15 * mm, rightMargin=15 * mm, topMargin=18 * mm, bottomMargin=14 * mm)
    d.addPageTemplates([PageTemplate(id='a', frames=[Frame(15 * mm, 14 * mm, W - 30 * mm, H - 32 * mm, 0, 0, 0, 0)], onPage=seite)])
    d.build(story); return pfad

def volkregeln():
    F = '#2f6f8f'; st = []
    st += [h1('Volkskarten', F), p('<b>Erweiterung 1</b> gibt jedem Volk <b>7 eigene Karten</b>, eine für jedes Zeitalter: besondere Einheiten und Gebäude, die es nur bei diesem Volk gibt. Sie braucht nur das Grundspiel und lässt sich mit Erweiterung 2 (Götter &amp; Glaube) beliebig kombinieren. Erkennbar sind alle Karten an der <b>blauen Fahne</b> unten rechts und am farbigen Rahmen der Volksfarbe.')]
    st += [h2('Material'), b('<b>2_Erweiterung_Volkskarten_Karten</b>: 5 Blätter, je Volk 1 Rückseite, 1 Infokarte, 1 Übersichtskarte und 7 Volkskarten (35 Volkskarten insgesamt).'), b('Die Volkskarten liegen getrennt vom Grundspiel. Jede Spielerin und jeder Spieler bekommt nur die 9 Karten des eigenen Volkes (Rückseite mit Volksfarbe).')]
    st += [h2('Was sich gegenüber dem Grundspiel ändert'), b('<b>Start:</b> Du nimmst zu deinen 5 Handkarten zusätzlich die <b>Volkskarte I</b> auf die Hand.'), b('<b>Aufstieg:</b> Beim Aufstieg ins Zeitalter II bis VII nimmst du die Volkskarte des neuen Zeitalters auf die Hand.'), b('<b>Spielen:</b> Wie jede andere Karte: Gold zahlen, Einheiten in die Kaserne, Gebäude in die Auslage (jedes nur 1× je Spieler). Rohstoffe brauchst du dafür nicht.'), b('<b>Handlimit:</b> Volkskarten zählen zum Handlimit. Du kannst sie wie jede andere Karte gegen Gold ablegen (Ablegen-Regel des Grundspiels) – eine abgelegte Volkskarte ist aus dem Spiel.'), b('<b>Zerstört:</b> Wird eine Volkskarten-Einheit zerstört (oder ist sie einmalig verbraucht), ist sie aus dem Spiel. Sie kommt weder auf die Hand noch auf den Ablagestapel.'), b('Alles andere (Zug, Kampf, Siege, Ereignisse) bleibt wie im Grundspiel.')]
    st += [h2('Zusammen mit Erweiterung 2 (Götter &amp; Glaube)'), b('Beide Erweiterungen stören sich nicht. Mit Erweiterung 2 genügen <b>12 statt 13 Glaube</b> zum Sieg, weil Volkskarten das Spiel beschleunigen.'), b('Beim Gründen einer Religion darfst du keine Volkskarte als abzulegende Handkarte wählen.'), b('Volkskarten bringen keinen Glauben.')]
    st += [h2('Alle 35 Volkskarten')]
    rows = [[Paragraph('<b>Zeitalter</b>', C)] + [Paragraph('<b>%s</b>' % v['name'], C) for v in S['voelker']]]
    nv = nach_volk(); ro = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
    for z in range(7):
        rows.append([Paragraph(za_inline(z, 12), C)] + [Paragraph('%s <font color="#7a7468">(%s, %d)</font>' % (nv[v['id']][z]['name'], 'E' if nv[v['id']][z]['typ'] == 'einheit' else 'G', nv[v['id']][z]['kosten']), C) for v in S['voelker']])
    t = Table(rows, colWidths=[17 * mm] + [32.6 * mm] * 5, repeatRows=1)
    t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), .4, hexc('#c9bfa6')), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BACKGROUND', (0, 0), (-1, 0), hexc('#d8e6ee'))]))
    st += [t, Paragraph('E = Einheit, G = Gebäude, Zahl = Goldkosten.', Sm)]
    st += [h2('Hinweis zum Test'), Paragraph('Die Erweiterung wurde nur mit Computer-Spielern durchgerechnet (je 120 Partien je Spielerzahl), noch nicht von Menschen gespielt oder gedruckt getestet. Mit Volkskarten dauern Partien etwa eine Runde kürzer (Median 11–12 statt 12–13) und enden fast immer mit Kultursieg. Zu dritt und zu viert lagen die Völker bei etwa 22–48 % Siegen (4 Spieler: ideal wären 25 %). Zu zweit schnitt die Sternendeuter-Seite am schwächsten ab.', Sm)]
    return doc_bauen(os.path.join(AUS, '2_Erweiterung_Volkskarten_Regeln.pdf'), 'Volk – Erweiterung 1 – Volkskarten', 'VOLK – VOLKSKARTEN', 'ERWEITERUNG 1 · Regeln', F, st)

def civregeln():
    import civ as CV
    F = '#3f2f73'; st = []
    reg, per, nat = CV.baue()
    eff = {'E': 'Einkommen', 'K': 'Kultur', 'W': 'Wissen', 'S': 'Schutz', 'H': 'Heilung', 'A': 'Ausbildung', 'HL': 'Handlimit', 'G': 'Bauherr', 'L': 'Land', 'Z': 'Ziehen', 'F': 'Glaube', 'SCHIFF': 'Seefahrt'}
    st += [h1('Zivilisation', F), p('<b>Erweiterung 3</b> bringt drei neue Kartenarten: <b>Regierungen</b>, <b>Große Persönlichkeiten</b> und <b>Naturwunder</b>. Sie braucht nur das Grundspiel und lässt sich mit den anderen Erweiterungen beliebig kombinieren. Erkennbar am <b>Tempel-Symbol</b> unten rechts.')]
    st += [h2('Aufbau'), b('Regierungen offen neben das Spielfeld legen (alle 8, jeder Spieler darf jede wählen).'), b('Persönlichkeiten mischen, <b>3 offen</b> auslegen, Rest als Stapel. Naturwunder mischen, <b>4 offen</b> auslegen, Rest als Stapel.'), b('Wird eine offene Karte genommen, kommt sofort eine neue vom Stapel nach.')]
    st += [h2('Regeln'), b('Pro Zug darfst du <b>höchstens 1 Karte</b> dieser Erweiterung nehmen.'), b('<b>Regierung:</b> ab dem genannten Zeitalter für ihre Kosten einführen. Sie liegt dauerhaft vor dir. Eine neue Regierung <b>ersetzt</b> die alte (volle Kosten).'), b('<b>Große Persönlichkeit:</b> Kosten zahlen, Zeitalter muss erreicht sein. Dauerhafte bleiben liegen (<b>höchstens 3</b>). Einmalige (Sunzi, Marco Polo, Florence Nightingale) wirken sofort und kommen dann unter den Stapel.'), b('<b>Naturwunder:</b> nur ab <b>Zeitalter II</b> und nur, wenn du eine Land-Karte mit dem passenden Gelände ausliegen hast.')]
    rows = [[Paragraph('<b>Karte</b>', C), Paragraph('<b>Ab Zeitalter · Kosten</b>', C), Paragraph('<b>Wirkung</b>', C)]]
    for k in reg + per + nat:
        e = ', '.join('%s %s' % (eff.get(a, a), v) for a, v in (k.get('effekte') or {}).items())
        rows.append([Paragraph(k['name'], C), Paragraph('%s · %s Gold' % (k.get('zeitalter', 0) + 1, k.get('kosten', '')), C), Paragraph((CV.einmal_text(k['einmal']) if k.get('einmal') else '') or e or (k.get('beschreibung') or ''), C)])
    t = Table(rows, colWidths=[45 * mm, 38 * mm, 97 * mm], repeatRows=1)
    t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), .4, hexc('#c9bfa6')), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BACKGROUND', (0, 0), (-1, 0), hexc('#ddd6ee'))]))
    st += [h2('Alle Karten'), t]
    st += [h2('Hinweis zum Test'), Paragraph('Nur mit Computer-Spielern durchgerechnet, noch nicht von Menschen gespielt oder gedruckt getestet. Starke Computer-Spieler gewinnen mit dieser Erweiterung etwas häufiger durch Kultur.', Sm)]
    return doc_bauen(os.path.join(AUS, '4_Erweiterung_Zivilisation_Regeln.pdf'), 'Volk – Erweiterung 3 – Zivilisation', 'VOLK – ZIVILISATION', 'ERWEITERUNG 3 · Regeln', F, st)

def uebersicht():
    st = []
    mods = [('GRUNDSPIEL', '#b5483b', 'Pflicht. Komplett spielbar allein.', ['1_Grundspiel_Regelheft', '1_Grundspiel_Karten_Stapel_I / II / III', '1_Grundspiel_Karten_Welt', '1_Grundspiel_Volkstafeln', '1_Grundspiel_Spielmarken'], 'Fußzeile „VOLK · Grundspiel“'),
            ('ERWEITERUNG 1 · VOLKSKARTEN', '#2f6f8f', 'Optional. Jedes Volk bekommt 7 eigene Karten.', ['2_Erweiterung_Volkskarten_Regeln', '2_Erweiterung_Volkskarten_Karten'], 'Symbol unten rechts: blaue Fahne'),
            ('ERWEITERUNG 2 · GÖTTER & GLAUBE', '#6b1f3a', 'Optional. 8 Religionen, Missionare, Glaubenssieg.', ['3_Erweiterung_Goetter_und_Glaube_Regeln', '3_Erweiterung_Goetter_und_Glaube_Karten', '3_Erweiterung_Goetter_und_Glaube_Material'], 'Symbol unten rechts: Strahlenkranz')]
    st += [h1('Module: Was brauche ich?', '#b5483b'), p('Das Spiel besteht aus <b>einem Grundspiel</b> und <b>drei Erweiterungen</b>. Die Erweiterungen brauchen nur das Grundspiel und sind unabhängig voneinander: Du kannst nur das Grundspiel spielen oder beliebige Erweiterungen dazunehmen. Kein Modul ändert die Karten eines anderen.')]
    mods.append(('ERWEITERUNG 3 · ZIVILISATION', '#3f2f73', 'Optional. 8 Regierungen, 14 Große Persönlichkeiten, 9 Naturwunder.', ['4_Erweiterung_Zivilisation_Regeln', '4_Erweiterung_Zivilisation_Karten'], 'Symbol unten rechts: Tempel'))
    rows = []
    for n, f, w, d, k in mods:
        rows.append([Paragraph('<b>%s</b>' % n, CW_), Paragraph('<b>%s</b><br/>%s' % (w, '<br/>'.join('• ' + x for x in d)), C), Paragraph('Erkennen:<br/><b>%s</b>' % k, C)])
    t = Table(rows, colWidths=[40 * mm, 100 * mm, 40 * mm])
    ts = [('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('GRID', (0, 0), (-1, -1), .4, hexc('#c9bfa6')), ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]
    for i, (n, f, *_ ) in enumerate(mods): ts.append(('BACKGROUND', (0, i), (0, i), hexc(f)))
    t.setStyle(TableStyle(ts)); st += [t, Spacer(1, 6)]
    st += [h1('Die 4 Möglichkeiten', '#b5483b')]
    gz, gv = RL.GLAUBE_SIEG, RL.GLAUBE_SIEG_VK
    hdr = ['Du spielst', 'Start & Aufstieg', 'Siegwege', 'Besonderes']
    rr = [hdr,
          ['Nur Grundspiel', '5 Handkarten, kein Zusatz beim Aufstieg', 'Kultur 12 · Eroberung · Wissenschaft', 'Regelheft Grundspiel genügt'],
          ['Grundspiel + Erw. 1 (Volkskarten)', '+ Volkskarte I zu Beginn, + Volkskarte bei jedem Aufstieg', 'Kultur 12 · Eroberung · Wissenschaft', 'Partien etwas kürzer'],
          ['Grundspiel + Erw. 2 (Götter & Glaube)', '5 Handkarten; Religion gründen (5 Gold, ab Zeitalter II)', 'Kultur 12 · Eroberung · Wissenschaft · Glaube %d' % gz, 'Glaube-Ereignisse unter die Ereigniskarten mischen'],
          ['Alle drei', 'Volkskarten wie bei Erw. 1; Religion wie bei Erw. 2', 'Kultur 12 · Eroberung · Wissenschaft · Glaube %d' % gv, 'Beim Gründen keine Volkskarte ablegen']]
    rr = [[Paragraph(('<b>%s</b>' if i == 0 or j == 0 else '%s') % x, C) for j, x in enumerate(r)] for i, r in enumerate(rr)]
    t = Table(rr, colWidths=[42 * mm, 50 * mm, 42 * mm, 46 * mm], repeatRows=1)
    t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), .4, hexc('#c9bfa6')), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BACKGROUND', (0, 0), (-1, 0), hexc('#ecdcc0')), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    st += [t, Spacer(1, 4)]
    st += [h1('Aufbau in Kurzform', '#b5483b'), b('<b>Immer:</b> Aufbau laut Grundspiel-Regelheft.'), b('<b>Mit Erw. 1:</b> Jede/r nimmt die 9 Karten des eigenen Volkes (farbige Rückseite). Die Volkskarte I kommt zu Spielbeginn auf die Hand.'), b('<b>Mit Erw. 2:</b> 8 Religionstafeln offen in die Mitte, die 6 Glaube-Ereigniskarten unter die Ereigniskarten mischen, jede/r nimmt eine Glaubensleiste samt Marker.'), b('<b>Aufräumen:</b> Grundspiel-Karten haben Stapel-Rückseiten (braun, rot, blau, lila), Erw.-1-Karten tragen die Volksfarbe und „ERWEITERUNG 1“, Erw.-2-Karten die Religionsfarbe und „ERWEITERUNG 2“. Darum lässt sich nach dem Spiel alles schnell wieder sortieren.')]
    st += [h1('Getestet?', '#b5483b'), Paragraph('Alle vier Kombinationen wurden mit Computer-Spielern durchgespielt (je 2, 3 und 4 Spieler, je 120 Partien): keine Abstürze, keine hängenden Partien. Weil Kultur jetzt schon bei 12 gewinnt, fiel ein Glaubenssieg nur selten (zu dritt und zu viert in unter 10 % der Partien, zu zweit fast nie). Von Menschen gespielt oder gedruckt getestet wurde noch nichts.', Sm)]
    return doc_bauen(os.path.join(AUS, '0_Modul_Uebersicht.pdf'), 'Volk – Modul-Übersicht', 'VOLK – DAS KARTENSPIEL', 'Modul-Übersicht', '#4a5560', st)

if __name__ == '__main__': print(volkregeln(), civregeln(), uebersicht())
