"""Regelheft (A4 hochkant) mit reportlab-Platypus."""
import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, KeepTogether, Table, TableStyle
from lib import *
from karten import SCHLUESSEL_TEXT

AUS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, '..', 'ausgabe')
os.makedirs(AUS, exist_ok=True)
W, H = A4
INK = hexc('#2b2118')
T = ParagraphStyle('t', fontName='DV', fontSize=9.2, leading=12.4, textColor=INK, spaceAfter=3.2)
B = ParagraphStyle('b', parent=T, leftIndent=9, bulletIndent=0, spaceAfter=1.8)
H1 = ParagraphStyle('h1', fontName='PXB', fontSize=15, leading=18, textColor=hexc('#b5483b'), spaceBefore=7, spaceAfter=3.5)
H2 = ParagraphStyle('h2', fontName='PXB', fontSize=10.5, leading=13, textColor=INK, spaceBefore=4, spaceAfter=2)
S = ParagraphStyle('s', parent=T, fontSize=7.8, leading=10, textColor=hexc('#6a6458'))
C = ParagraphStyle('c', parent=T, fontSize=8.4, leading=11, spaceAfter=0)

def p(t): return Paragraph(t, T)
def b(t): return Paragraph(t, B, bulletText='•')

def seite(c, doc):
    c.saveState()
    c.setFillColor(hexc('#fbf7ec')); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(hexc('#b5483b')); c.rect(0, H - 12 * mm, W, 12 * mm, stroke=0, fill=1)
    links(c, 'VOLK – DAS KARTENSPIEL', 15 * mm, H - 8.4 * mm, 'PXB', 11, '#ffffff')
    rechts(c, 'GRUNDSPIEL · Regeln', W - 15 * mm, H - 8.2 * mm, 'PX', 9, '#ffffff')
    zentriert(c, 'Seite %d' % doc.page, W / 2, 7 * mm, 'DV', 7, '#9a9488')
    c.restoreState()

def titel(c, doc):
    seite(c, doc)
    c.saveState()
    zeichne_bild(c, 'stadt:stadt@2@3', 15 * mm, H - 68 * mm, 55 * mm, 48 * mm, farbe='#b5483b', zuschnitt=True)
    links(c, 'VOLK', 76 * mm, H - 40 * mm, 'PXB', 44, '#b5483b')
    links(c, 'Das Kartenspiel für 2–4 Völker', 77 * mm, H - 50 * mm, 'PX', 13, '#2b2118')
    links(c, 'GRUNDSPIEL · 11 Zeitalter von der Antike bis zu den Sternen', 77 * mm, H - 64.5 * mm, 'SS', 7.5, '#b5483b')
    links(c, 'Ab 10 Jahren · ca. 45–75 Minuten · Karten, Tafeln und Marker zum Ausdrucken', 77 * mm, H - 57 * mm, 'DV', 7.8, '#6a6458')
    c.restoreState()

doc = BaseDocTemplate(os.path.join(AUS, '1_Grundspiel_Regelheft.pdf'), pagesize=A4, title='Volk – Grundspiel – Regelheft', author='Leif Schmale')
rand = 16 * mm
doc.addPageTemplates([
    PageTemplate('titel', [Frame(rand, 14 * mm, W - 2 * rand, H - 14 * mm - 76 * mm, id='f1', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=titel),
    PageTemplate('normal', [Frame(rand, 14 * mm, W - 2 * rand, H - 14 * mm - 18 * mm, id='f2', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=seite)])
from reportlab.platypus import NextPageTemplate


def za_tabelle():
    kopf = [Paragraph('<b>Symbol</b>', T), Paragraph('<b>Zeitalter</b>', T), Paragraph('<b>Aufstieg kostet</b>', T), Paragraph('<b>Grundeinkommen</b>', T), Paragraph('<b>Zieht von</b>', T)]
    rows = [kopf]
    for z in range(11):
        rows.append([Paragraph(za_inline(z, 16), T), Paragraph('<b>%s</b>' % ZA[z]['name'], T),
                     Paragraph(('%d Gold' % R['aufstieg'][z]) if z < 10 else '%d Gold = <b>Wissenschaftssieg</b>' % R['wissen_sieg'], T), Paragraph('%d' % (R['basis_einkommen'] + z), T),
                     Paragraph('Stapel ' + ['I', 'II', 'III', 'IV'][R['stapel_von_zeitalter'][z] - 1], T)])
    tb = Table(rows, colWidths=[20 * mm, 38 * mm, 40 * mm, 38 * mm, 30 * mm], hAlign='LEFT')
    tb.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), .4, hexc('#c9bfa6')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('BACKGROUND', (0, 0), (-1, 0), hexc('#efe6d0')), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
    return tb

n = []
n += [Paragraph('Worum geht es?', H1),
 p('Jede Spielerin und jeder Spieler führt ein Volk durch elf Zeitalter – von der Antike bis zum Sternenzeitalter. Du baust Gebäude, stellst Einheiten auf, kaufst Weltwunder und gewinnst Stadtstaaten als Verbündete. '
   'Wer als Erste/r <b>%d Kultur</b> erreicht, gewinnt. Oder du eroberst alle gegnerischen Städte. Oder du erreichst das Sternenzeitalter und zahlst dort <b>%d Gold</b> für den Aufstieg ins nächste Zeitalter (Wissenschaftssieg).' % (R['kultur_sieg'], R['wissen_sieg'])),
 Paragraph('Material', H1),
 b('<b>4 Kartenstapel</b> (1_Grundspiel_Karten_Stapel_I bis IV) mit Einheiten, Gebäuden und Land. Jede Karte hat eine Zeitalter-Zahl und eine Stapel-Nummer.'),
 b('<b>Welt-Karten</b> (1_Grundspiel_Karten_Welt): 12 Weltwunder, 12 Stadtstaaten, 12 Ereigniskarten (Barbaren und Wetter).'),
 b('<b>5 Völker</b>: je 1 Volkstafel und <b>11 Volkskarten</b> (1_Grundspiel_Volkskarten) – eine besondere Einheit oder ein besonderes Gebäude für jedes Zeitalter, nur für dieses Volk.'),
 b('<b>Volkstafeln</b> mit Lebenspunkte-, Kultur- und Zeitalter-Leiste (1_Grundspiel_Volkstafeln) – dazu Spielmarken: Gold, Marker, Krone (1_Grundspiel_Spielmarken).'),
 b('Erkennbar sind alle Grundspiel-Karten an der Fußzeile <b>„VOLK · Grundspiel“</b>.'),
 b('Druck: Karten 63 × 88 mm, 9 Stück pro A4-Blatt. Erst die Rückseiten drucken, dann dasselbe Blatt wenden und die Vorderseiten drucken (lange Kante wenden).'),
 Paragraph('Die elf Zeitalter', H1), za_tabelle(), Spacer(1, 3 * mm),
 Paragraph('Aufbau', H1),
 b('Mische die vier Stapel getrennt und lege sie in die Mitte, die Weltwunder sortiert nach Zeitalter daneben. Decke die ersten 3 Wunder auf.'),
 b('Mische die Ereigniskarten (verdeckt) und die 12 Stadtstaaten. Decke 3 Stadtstaaten auf.'),
 b('Jede/r wählt eine Volkstafel, nimmt die Marker in der Volksfarbe: Herz auf <b>25</b>, Kultur auf <b>0</b>, Zeitalter-Marker auf %s (<b>Antike</b>).' % za_inline(0)),
 b('Startvermögen: <b>3 Gold</b>. Ziehe 5 Karten vom Stapel I und nimm dazu deine <b>Volkskarte I</b>. Wer zuletzt etwas gebaut hat, nimmt die Krone (Startspieler).'),
 Paragraph('Dein Zug', H1),
 Paragraph('1 · Aufwecken', H2),
 p('Richte alle gedrehten (erschöpften) Einheiten auf. Einheiten in der <b>Kaserne</b> rücken an die <b>Front</b>. Deine Stadt heilt 1 Lebenspunkt (mehr mit Heilen-Karten).'),
 Paragraph('2 · Einkommen', H2),
 p('Nimm Gold: <b>2 + Zeitalter-Nummer</b> (I = 0 … XI = 10) <b>+ Ertrag aller Land-Karten + Einkommen</b> von Gebäuden, Wundern, Verbündeten und Handels-Einheiten. Es gibt keine Obergrenze für Gold.'),
 Paragraph('3 · Ziehen', H2),
 p('Ziehe 2 Karten. Du darfst vom Stapel deines Zeitalters ziehen oder von einem niedrigeren: Zeitalter I–II → Stapel I, III–IV → Stapel II, V–VII → Stapel III, VIII–XI → Stapel IV. Du darfst die Karten auf mehrere Stapel verteilen. '
   'Sind die Stapel leer, mische die Ablage neu.'),
 Paragraph('4 · Aktionen', H2),
 p('In beliebiger Reihenfolge und so oft du magst:'),
 b('<b>1 Land</b> pro Zug gratis spielen (Rohstoff- oder Geländekarte). Land gibt dauerhaft Gold und Rohstoff-Symbole.'),
 b('<b>Karten spielen</b>: Goldkosten (Zahl im Kreis oben links) zahlen. Das Zeitalter der Karte darf nicht höher sein als deines. Einheiten kommen in die Kaserne, Gebäude in deine Auslage; jedes Gebäude nur 1× je Spieler. Steht „Benötigt“ auf der Karte, muss das genannte Gebäude schon liegen.'),
 b('<b>Wunder kaufen</b>: Gold zahlen, Rohstoff und Zeitalter passen. Das Wunder liegt vor dir; ein neues wird aufgedeckt.'),
 b('<b>Aufstieg</b> ins nächste Zeitalter: Gold laut Zeitalter-Leiste (%s). Dein Zeitalter-Marker rückt vor. <b>Pro Runde darfst du nur einmal aufsteigen.</b> Bei jedem Aufstieg bekommst du die <b>Volkskarte</b> des neuen Zeitalters. Im Sternenzeitalter kostet der letzte Aufstieg %d Gold und gewinnt das Spiel.' % (' / '.join(str(x) for x in R['aufstieg']), R['wissen_sieg'])),
 b('<b>Tribut</b>: %d Gold an einen offenen Stadtstaat zahlen → er wird dein Verbündeter (max. 2).' % R['tribut_kosten']),
 b('<b>Ablegen für Gold</b>: bis zu %d Handkarten ablegen, je %d Gold.' % (R['ablegen_max'], R['ablegen_gold'])),
 b('<b>Angreifen</b> (siehe Kampf).'),
 Paragraph('5 · Zugende', H2),
 p('Höchstens <b>%d Handkarten</b>, den Rest ablegen. Dann gibt die Krone weiter. Wenn alle gespielt haben (Rundenende), deckt die Startspielerin / der Startspieler <b>1 Ereigniskarte</b> auf und führt sie aus.' % R['handlimit']),
 Paragraph('Rohstoffe', H1),
 p('Viele Karten zeigen „braucht“-Symbole (Holz, Stein, Marmor, Eisen, Pferde, …). Du hast ein Symbol, wenn eines deiner Länder, Gebäude oder Verbündeten es zeigt. '
   'Es wird nicht verbraucht – mehrere Karten dürfen dasselbe Symbol nutzen. Fehlt dir genau 1 Symbol, darfst du es für <b>%d Gold</b> zukaufen (höchstens 1 je Karte). Küste und Flugfeld kann man nicht zukaufen.' % R['zukauf_preis']),
 Paragraph('Kampf', H1),
 p('Der Kampf ist der Weg zum Sieg, wenn die Kultur nicht reicht – oder die Antwort, wenn jemand dich bedroht.'),
 b('<b>Neulingsschutz:</b> Solange noch keine %d Ereigniskarten aufgedeckt wurden, darf niemand angreifen oder schießen. Barbaren ignorieren den Schutz.' % R['schutz_runden']),
 b('<b>Angreifen:</b> Wähle beliebig viele aufrechte Einheiten an der Front und benenne die Stadt eines Gegners. Die Angreifer werden gedreht.'),
 b('<b>Blocken:</b> Der Verteidiger darf jeden Angreifer mit höchstens 1 seiner aufrechten Einheiten blocken (auch aus der Kaserne). Höhere <b>Stärke</b> gewinnt – die andere Einheit wird abgelegt. Gleichstand: beide ablegen.'),
 b('<b>Treffer auf die Stadt:</b> Jeder nicht geblockte Angreifer verursacht Schaden in Höhe seiner Stärke, abzüglich <b>Schutz</b> deiner Gebäude (mindestens 1). Der Herz-Marker sinkt. Bei 0 ist die Stadt erobert; die Spielerin / der Spieler scheidet aus.'),
 b('<b>Schuss:</b> Einheiten mit <b>Fern</b> (blaue Zahl) dürfen statt anzugreifen eine gegnerische Einheit beschießen: ist Fern ≥ Stärke des Ziels, wird es zerstört. Kein Gegenschlag. Sie werden danach gedreht.'),
 Paragraph('Schlüsselwörter', H1)]
rows = [[Paragraph('<b>%s</b>' % t.split(':')[0], C), Paragraph(t.split(':', 1)[1].strip(), C)] for kk, t in SCHLUESSEL_TEXT.items() if kk != 'mission']
tab = Table(rows, colWidths=[27 * mm, W - 2 * rand - 27 * mm], hAlign='LEFT')
tab.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -1), .3, hexc('#d9d1bf')), ('TOPPADDING', (0, 0), (-1, -1), 2.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2), ('LEFTPADDING', (0, 0), (-1, -1), 1)]))
n += [tab,
 Paragraph('Ereignisse', H1),
 p('Am Rundenende wird eine Ereigniskarte aufgedeckt.'),
 b('<b>Wetter</b> gilt für alle Spieler (z. B. Ernte, Dürre, Sturm).'),
 b('<b>Barbaren:</b> Ein Lager überfällt die Spielerin / den Spieler mit den <b>wenigsten Kampfeinheiten</b> (bei Gleichstand den mit dem niedrigsten Zeitalter). Barbarenstärke = Zeitalter-Nummer des Opfers + Zahl auf der Karte. Das Opfer <b>darf</b> eine aufrechte (nicht getappte) Einheit entgegenstellen: ist sie gleich stark oder stärker, gewinnt sie und das Opfer erhält die Beute (Gold); sonst wird sie abgelegt, dafür entfällt die Folge. Wer nicht abwehren will oder keine aufrechte Einheit hat, erleidet die Folge (Schaden an der Stadt oder Goldverlust).'),
 Paragraph('Weltwunder und Stadtstaaten', H1),
 p('<b>Weltwunder</b> kosten viel, bringen aber Kultur und starke Boni. Jedes gibt es nur einmal im Spiel; wer es zuerst kauft, behält es. '
   '<b>Stadtstaaten</b> bleiben bei dir, solange du sie hältst: sie geben dauerhafte Boni (Gold, Kultur, Schutz …). Du kannst höchstens 2 Verbündete haben.'),
 Paragraph('Die Völker', H1)]
voelker = [[Paragraph('<b>%s</b>' % v['name'], C), Paragraph(v['text'][0], C)] for v in SATZ['voelker']]
tab2 = Table(voelker, colWidths=[34 * mm, W - 2 * rand - 34 * mm], hAlign='LEFT')
tab2.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -1), .3, hexc('#d9d1bf')), ('TOPPADDING', (0, 0), (-1, -1), 2.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2), ('LEFTPADDING', (0, 0), (-1, -1), 1)]))
n += [tab2,
 Paragraph('Siegbedingungen', H1),
 b('<b>Kultur:</b> %d Kultur – sofort bei Erreichen, auch mitten im Zug.' % R['kultur_sieg']),
 b('<b>Eroberung:</b> Alle anderen Städte haben 0 Lebenspunkte.'),
 b('<b>Wissenschaft:</b> Du bist im Sternenzeitalter und zahlst %d Gold für den Aufstieg ins „nächste Zeitalter“ – du gewinnst sofort. Wer erst in dieser Runde ins Sternenzeitalter aufgestiegen ist, kann frühestens in der nächsten Runde gewinnen (ein Aufstieg pro Runde).' % R['wissen_sieg']),
 Paragraph('Varianten und Tipps', H1),
 b('<b>Zu zweit:</b> Nur 2 Stadtstaaten aufdecken. <b>Zu viert:</b> Wunder und Stadtstaaten sind knapp – Tempo zählt.'),
 b('<b>Einsteiger:</b> Spielt ohne Neulingsschutz-Zähler und ohne Barbaren-Karten, bis alle die Regeln kennen.'),
 Paragraph('Volkskarten', H1),
 p('Volkskarten zählen zum Handlimit. Du darfst sie wie andere Karten gegen Gold ablegen – abgelegt oder zerstört ist die Karte aus dem Spiel und kommt nicht zurück. Die Erweiterungen „Götter &amp; Glaube“ und „Zivilisation“ sind vorerst nicht Teil des Spiels.'),
 Spacer(1, 4),
 Paragraph('Hinweis: Die Regeln wurden mit Computer-Simulationen (Spielroboter, je 200 Partien) auf Ausgewogenheit geprüft: Partien dauern im Median etwa 16 bis 20 Runden. Je nach Spielerzahl entscheidet mal die Kultur, mal die Wissenschaft, zu zweit auch oft die Eroberung. In echten Runden getestet ist es noch nicht. Wenn etwas hakt: Hausregeln erlaubt – sagt gern, was ihr ändern würdet!', S)]
story = [NextPageTemplate('normal')] + n
doc.build(story)
print('ok')
