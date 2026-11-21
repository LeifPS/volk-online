"""Erweiterung 3 · Zivilisation: Regierungen, Große Persönlichkeiten, Naturwunder (Daten)."""

MODUL_NAME = 'ZIVILISATION'
FARBEN = {'regierung': '#5b4a94', 'person': '#2c7a68', 'natur': '#8a5f24'}
RAHMEN = {'regierung': '#3f2f73', 'person': '#1b5a4a', 'natur': '#5f3f12'}

# (id, name, zeitalter, kosten, effekte, sprite-Emblem, flavor, zusatztext)
REGIERUNGEN = [
    ('haeuptlingstum', 'Häuptlingstum', 0, 3, {'E': 1, 'S': 1}, 'zelt', 'Ein Ältester spricht, und alle folgen.', None),
    ('klass_republik', 'Klassische Republik', 1, 7, {'E': 2, 'W': 1}, 'saeulen', 'Wer wählen darf, baut auch gern mit.', None),
    ('oligarchie', 'Oligarchie', 1, 7, {'A': 1, 'S': 2}, 'schild', 'Wenige führen, viele marschieren.', None),
    ('monarchie', 'Monarchie', 2, 9, {'S': 2, 'HL': 1, 'H': 1}, 'krone', 'Die Krone ist schwer, aber sie hält das Reich.', None),
    ('handelsrepublik', 'Handelsrepublik', 2, 9, {'E': 3, 'G': 1}, 'muenze', 'Hier zählt nur, was der Markt sagt.', None),
    ('theokratie', 'Theokratie', 2, 9, {'K': 1, 'H': 2, 'F': 1}, 'tempel', 'Der Priester ist auch der Richter.', None),
    ('demokratie', 'Demokratie', 4, 14, {'K': 2, 'E': 2, 'H': 1}, 'urne', 'Jede Stimme ist ein Stein im Fundament.', None),
    ('kommunismus', 'Kommunismus', 4, 14, {'E': 3, 'S': 3, 'A': 1}, 'stern', 'Alles gehört allen, und alle arbeiten.', None),
]

# (id, name, rolle, zeitalter, kosten, effekte (dauerhaft), einmalig (Sofortwirkung), flavor)
PERSONEN = [
    ('homer', 'Homer', 'schriftsteller', 0, 5, {'K': 1}, None, 'Seine Verse überleben jedes Reich.'),
    ('imhotep', 'Imhotep', 'ingenieur', 0, 6, {'G': 1, 'H': 1}, None, 'Baumeister der Pharaonen und Heiler dazu.'),
    ('hypatia', 'Hypatia', 'wissenschaftler', 1, 6, {'W': 2}, None, 'Sie las die Sterne wie andere ein Buch.'),
    ('sunzi', 'Sunzi', 'general', 1, 4, {}, {'ziehen': 2, 'aufrichten': 1}, 'Die beste Schlacht ist die, die man nicht schlagen muss.'),
    ('marco_polo', 'Marco Polo', 'haendler', 1, 3, {}, {'gold': 6}, 'Er kam mit Seide zurück und mit noch mehr Geschichten.'),
    ('themistokles', 'Themistokles', 'admiral', 1, 6, {'SCHIFF': 1, 'E': 1}, None, 'Hölzerne Mauern, die auf dem Wasser kämpfen.'),
    ('michelangelo', 'Michelangelo', 'kuenstler', 2, 8, {'K': 2, 'E': 1}, None, 'Aus einem Block Marmor holte er den Menschen heraus.'),
    ('leonardo', 'Leonardo da Vinci', 'ingenieur', 3, 10, {'W': 1, 'A': 1, 'G': 1}, None, 'Zu viele Ideen für ein einziges Leben.'),
    ('adam_smith', 'Adam Smith', 'haendler', 3, 9, {'E': 3}, None, 'Die unsichtbare Hand greift auch in deine Kasse.'),
    ('newton', 'Isaac Newton', 'wissenschaftler', 3, 10, {'W': 3}, None, 'Ein Apfel fiel, und die Welt bekam Gesetze.'),
    ('nightingale', 'Florence Nightingale', 'heilerin', 4, 7, {}, {'heilen': 8, 'ziehen': 1}, 'Wo sie mit der Lampe ging, wurde es hell und besser.'),
    ('mozart', 'Mozart', 'musiker', 4, 11, {'K': 3, 'E': 1}, None, 'Er schrieb Musik, als wäre sie schon immer da gewesen.'),
    ('einstein', 'Albert Einstein', 'wissenschaftler', 5, 15, {'W': 3, 'Z': 1}, None, 'Alles ist relativ, außer dem Siegesdurst.'),
    ('turing', 'Alan Turing', 'wissenschaftler', 6, 16, {'W': 4, 'E': 2}, None, 'Er fragte, ob Maschinen denken können, und baute die erste Antwort.'),
]

# (id, name, gelaende, kosten, effekte, deko-Sprite, flavor)
NATURWUNDER = [
    ('everest', 'Mount Everest', 'gebirge', 12, {'K': 2, 'S': 2}, 'deko:gebirge', 'Das Dach der Welt – wer es sieht, vergisst seine Sorgen.'),
    ('riff', 'Großes Barriereriff', 'kueste', 12, {'E': 2, 'K': 1, 'H': 1}, 'deko:korallenriff', 'Ein Garten aus Farben unter der Wasserlinie.'),
    ('uluru', 'Uluru', 'wueste', 11, {'K': 1, 'H': 2, 'S': 1}, 'deko:wueste', 'Ein roter Fels, der Geschichten bewahrt.'),
    ('kilimandscharo', 'Kilimandscharo', 'savanne', 11, {'E': 2, 'H': 2}, 'deko:savanne', 'Schnee auf dem Gipfel, Herden zu seinen Füßen.'),
    ('yosemite', 'Yosemite-Tal', 'wald', 11, {'K': 1, 'E': 1, 'H': 2}, 'deko:wald', 'Wasserfälle, so hoch, dass sie als Nebel ankommen.'),
    ('quelle', 'Quelle der Jugend', 'grasland', 12, {'H': 4, 'E': 1}, 'deko:oase', 'Wer trinkt, wird nicht jünger – aber gesünder.'),
    ('pantanal', 'Pantanal', 'dschungel', 11, {'E': 2, 'K': 1, 'H': 1}, 'deko:dschungel', 'Das größte Sumpfgebiet der Welt, voller Leben.'),
    ('eyja', 'Eyjafjallajökull', 'tundra', 11, {'K': 1, 'S': 3}, 'deko:vulkan', 'Ein Gletscher mit Feuer im Bauch.'),
    ('viktoriasee', 'Viktoriasee', 'ebene', 11, {'E': 3, 'H': 1}, 'deko:ebene', 'Fischer und Händler leben von seinen Ufern.'),
]
GELAENDE_NAME = {'gebirge': 'Gebirge', 'kueste': 'Küste', 'wueste': 'Wüste', 'savanne': 'Savanne', 'wald': 'Wald', 'grasland': 'Grasland', 'dschungel': 'Dschungel', 'tundra': 'Tundra', 'ebene': 'Ebene', 'huegel': 'Hügel'}
ROLLEN = {'schriftsteller': 'Schriftsteller', 'ingenieur': 'Ingenieur', 'wissenschaftler': 'Wissenschaftler', 'general': 'General', 'haendler': 'Händler', 'admiral': 'Admiral', 'kuenstler': 'Künstler', 'heilerin': 'Heilerin', 'musiker': 'Musiker'}
ROLLENFARBE = {'schriftsteller': '#8a5a2b', 'ingenieur': '#c9772b', 'wissenschaftler': '#3f6fb5', 'general': '#b32323', 'haendler': '#c9a227', 'admiral': '#2a5f8a', 'kuenstler': '#8e3fa8', 'heilerin': '#2f8f4e', 'musiker': '#a83f6b'}

def einmal_text(e):
    t = []
    if e.get('gold'): t.append('du bekommst %d Gold' % e['gold'])
    if e.get('ziehen'): t.append('ziehe %d Karte%s' % (e['ziehen'], 'n' if e['ziehen'] > 1 else ''))
    if e.get('aufrichten'): t.append('richte alle deine Einheiten auf')
    if e.get('heilen'): t.append('deine Stadt heilt %d Lebenspunkte' % e['heilen'])
    s = ', '.join(t); return 'Sofort: ' + s[0].upper() + s[1:] + '. Danach kommt die Karte unter den Stapel.'

def baue():
    reg = [dict(typ='regierung', id=i, name=n, zeitalter=z, kosten=k, effekte=e, sprite='civ:reg_' + sp, flavor=fl, beschreibung=fl, farbe=FARBEN['regierung'], rahmen=RAHMEN['regierung'],
                nr='RG-%d' % (j + 1), stapel=0, kopien=1, civ=True) for j, (i, n, z, k, e, sp, fl, _) in enumerate(REGIERUNGEN)]
    per = [dict(typ='person', id=i, name=n, rolle=r, rolle_name=ROLLEN[r], zeitalter=z, kosten=k, effekte=e, einmal=em or {}, sprite='civ:person_' + r, flavor=fl, beschreibung=fl,
                farbe=ROLLENFARBE[r], rahmen=RAHMEN['person'], nr='GP-%d' % (j + 1), stapel=0, kopien=1, civ=True) for j, (i, n, r, z, k, e, em, fl) in enumerate(PERSONEN)]
    nat = [dict(typ='natur', id=i, name=n, gelaende=g, gelaende_name=GELAENDE_NAME[g], zeitalter=1, kosten=k, effekte=e, sprite=sp, flavor=fl, beschreibung=fl,
                farbe=FARBEN['natur'], rahmen=RAHMEN['natur'], nr='NW-%d' % (j + 1), stapel=0, kopien=1, civ=True) for j, (i, n, g, k, e, sp, fl) in enumerate(NATURWUNDER)]
    return reg, per, nat

if __name__ == '__main__':
    r, p, n = baue(); print(len(r), len(p), len(n))
