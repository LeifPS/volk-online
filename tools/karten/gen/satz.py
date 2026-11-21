"""Baut den Kartensatz für "Volk – Das Kartenspiel" aus den Spieldaten des Repos (daten.json).
Alle Namen, Zeitalter, Stärken und Sprites kommen aus dem Spiel; Kosten und Effekte sind auf das Kartenspiel umgerechnet."""
import json, os, math
HIER = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HIER, '..', 'daten.json')))
EIN = {e['id']: e for e in D['einheiten']}
GEB = {e['id']: e for e in D['gebaeude']}
WUN = {e['id']: e for e in D['wunder']}
ROH = {e['id']: e for e in D['rohstoffe']}
import zukunft; zukunft.ergaenze(D)
EIN = {e['id']: e for e in D['einheiten']}
GEB = {e['id']: e for e in D['gebaeude']}
WUN = {e['id']: e for e in D['wunder']}
ROH = {e['id']: e for e in D['rohstoffe']}
ZA = D['zeitalter']
ROEM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']

# ---------------- Regel-Konstanten (werden von Simulation UND Druck benutzt) ----------------
REGELN = dict(
    stadt_hp=25, kultur_sieg=28, start_gold=3, start_hand=5, ziehen=2, handlimit=7,
    basis_einkommen=2,                 # + Zeitalter-Nummer (0..10)
    aufstieg=[6, 8, 10, 12, 14, 16, 18, 20, 22, 24], wissen_sieg=24,    # Kosten Zeitalter 0->1 ... 9->10; Wissenschaftssieg im Sternenzeitalter (XI)
    stapel_von_zeitalter=[1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4],
    ablegen_gold=1, ablegen_max=2, tribut_kosten=6, schutz_runden=3, zukauf_preis=3, zukauf_max=1,
)

STRAT = ['kupfer', 'zinn', 'eisen', 'pferde', 'salpeter', 'kohle', 'oel', 'aluminium', 'uran', 'elefanten'] + zukunft.NEUE_SYMBOLE
KUESTE_LAND = {'fisch', 'wale', 'muscheln', 'perlen', 'deuterium'}

def runde(x): return int(math.floor(x + 0.5))
def stapel_fuer(z): return REGELN['stapel_von_zeitalter'][z]

def kosten_aus_gold(g):
    for grenze, k in [(25, 1), (50, 2), (90, 3), (140, 4), (230, 5), (350, 6), (600, 7), (800, 8), (1100, 9), (1500, 10), (2200, 11), (2800, 12)]:
        if g <= grenze: return k
    return 13

# ---------------- Einheiten ----------------
# id: (Kopien)  -- Auswahl pro Stapel
EINHEITEN_AUSWAHL = {
    # Antike
    'siedler': 1, 'arbeiter': 1, 'spaeher': 2, 'krieger': 3, 'speertraeger': 2, 'schleuderer': 1, 'bogenschuetze': 2,
    'streitwagen': 1, 'rammbock': 1, 'boot': 1, 'karawane': 1,
    # Klassik
    'schwertkaempfer': 2, 'legionaer': 1, 'hoplit': 1, 'kompositbogenschuetze': 1, 'reiter': 2, 'kriegselefant': 1,
    'katapult': 1, 'trireme': 1, 'handelsschiff': 1,
    # Mittelalter
    'langschwertkaempfer': 1, 'pikenier': 1, 'armbrustschuetze': 1, 'langbogenschuetze': 1, 'ritter': 2, 'trebuchet': 1,
    'kundschafter': 1, 'handelstross': 1, 'feldscher': 1, 'kogge': 1,
    # Renaissance
    'musketier': 2, 'landsknecht': 1, 'arkebusier': 1, 'kuerassier': 1, 'kanone': 1, 'entdecker': 1, 'galeone': 1, 'fregatte': 1,
    # Industrie
    'gewehrschuetze': 2, 'feldgeschuetz': 1, 'kavallerie': 1, 'leichter_panzer': 1, 'artillerie': 1, 'flak': 1, 'ingenieur': 1,
    'doppeldecker': 1, 'tauchboot': 1,
    # Moderne
    'infanterie': 2, 'panzer': 1, 'schwerer_panzer': 1, 'maschinengewehr': 1, 'haubitze': 1, 'flakpanzer': 1, 'jagdflugzeug': 1,
    'bomber': 1, 'zerstoerer': 1, 'schlachtschiff': 1, 'u_boot': 1, 'flugzeugtraeger': 1,
    # Atomzeit
    'moderne_infanterie': 1, 'moderner_kampfpanzer': 1, 'raketenwerfer': 1, 'raketenartillerie': 1, 'flugabwehrraketen': 1,
    'duesenjaeger': 1, 'tarnkappenbomber': 1, 'raketenkreuzer': 1, 'lenkrakete': 1, 'atomwaffe': 1, 'atom_u_boot': 1,
}
# Handarbeit: Kosten-Korrekturen und Sondereffekte (Karten-Ebene)
EINHEIT_SONDER = {
    'siedler':   dict(kosten=2, schluessel=['gruenden']),
    'arbeiter':  dict(kosten=2, einkommen=1),
    'ingenieur': dict(kosten=6, einkommen=2),
    'spaeher':   dict(kosten=1, ziehen=1),
    'kundschafter': dict(kosten=3, ziehen=2),
    'entdecker': dict(kosten=5, ziehen=2),
    'karawane':  dict(kosten=3, einkommen=1),
    'handelsschiff': dict(kosten=4, einkommen=2),
    'handelstross': dict(kosten=5, einkommen=2),
    'feldscher': dict(kosten=4),
    'atomwaffe': dict(kosten=18, fern=12, staerke=0),
    'lenkrakete': dict(kosten=8),
    'rammbock':  dict(kosten=3),
}
def einheit_karte(eid):
    e = EIN[eid]
    s = EINHEIT_SONDER.get(eid, {})
    c = s.get('staerke', max(1, runde(e['staerke'] / 10)) if e['staerke'] > 0 else 0)
    f = s.get('fern', runde(e['fern'] / 10) if e['fern'] > 0 else 0)
    if e['klasse'] in ('zivil', 'haendler', 'see_zivil'): c = max(c, 1) if eid not in ('siedler',) else 1
    if eid in ('siedler', 'arbeiter', 'ingenieur', 'karawane', 'handelsschiff', 'handelstross'): c = 1
    kosten = s.get('kosten', kosten_aus_gold(e['kosten']['gold']))
    schluessel, tags = [], set()
    kl = e['klasse']; fa = e['faehigkeiten']
    if kl == 'reiter' and eid != 'kampfhubschrauber': schluessel.append('ansturm')
    if eid == 'rammbock': schluessel.append('ramme'); tags.add('belagerung')
    if f > 0 and kl in ('fernkampf', 'see_fern', 'u_boot', 'jaeger'): schluessel.append('fern')
    if f > 0 and kl in ('belagerung', 'bomber', 'rakete', 'atom'): schluessel.append('belagerung'); tags.add('belagerung')
    if kl in ('jaeger', 'bomber', 'rakete', 'atom'): schluessel.append('fliegend'); tags.add('luft')
    if kl == 'flak': schluessel.append('luftabwehr')
    if kl in ('see_nah', 'see_fern', 'u_boot', 'traeger', 'see_zivil', 'transport'): tags.add('see')
    if 'tarnung' in fa: schluessel.append('tarnung')
    if kl == 'traeger': schluessel.append('traeger')
    if 'einmalig' in fa: schluessel.append('einmalig')
    if kl == 'sanitaeter': schluessel.append('heilen')
    schluessel += s.get('schluessel', [])
    if kl == 'bomber': tags.add('bomber')
    if kl == 'rakete': tags.add('rakete')
    if kl == 'u_boot': tags.add('u_boot')
    if kl == 'reiter': tags.add('reiter')
    if kl in ('nahkampf',): tags.add('nahkampf')
    # Boni gegen Klassen
    boni = {}
    for b in e['boni']:
        g = b['gegen']; w = max(1, runde(b['wert'] / 10))
        if g == 'luft': g = 'luft'
        boni[g] = boni.get(g, 0) + w
    # benötigte Symbole
    braucht = []
    for m in STRAT:
        if m in e['kosten'] and m not in braucht: braucht.append(m)
    braucht = braucht[:2]
    if 'see' in tags and kl != 'see_zivil' or kl == 'see_zivil': braucht.append('kueste')
    if 'luft' in tags and kl != 'rakete' and eid not in ('atomwaffe',): braucht.append('flug')
    if eid in ('lenkrakete', 'marschflugkoerper', 'atomwaffe'): braucht.append('flug')
    if eid == 'flugzeugtraeger' or eid == 'supertraeger': braucht = [b for b in braucht if b != 'flug']
    return dict(typ='einheit', id=eid, name=e['name'], zeitalter=e['zeitalter'], kosten=kosten, staerke=c, fern=f,
                klasse=kl, tags=sorted(tags), schluessel=schluessel, boni=boni, braucht=braucht,
                einkommen=s.get('einkommen', 0), ziehen=s.get('ziehen', 0), sprite='einheit:' + eid,
                beschreibung=e['beschreibung'])

# ---------------- Gebäude ----------------
# kosten, Effekte (E Einkommen, K Kultur, W Wissen(Aufstieg billiger), S Schutz, H Heilung, A Ausbildung(Einheiten billiger), HL Handlimit,
#                  L zusätzliches Land, Z zusätzliche Karte ziehen, prov Symbole)
G = lambda **kw: kw
GEBAEUDE_AUSWAHL = {
    # Antike
    'kornspeicher': G(k=2, H=1), 'toepferei': G(k=2, E=1, n=2), 'schrein': G(k=2, K=1), 'denkmal': G(k=3, K=1, E=1, braucht=['stein']),
    'bibliothek': G(k=3, W=1), 'stadtmauer_holz': G(k=2, S=1, braucht=['holz']), 'kaserne': G(k=3, A=1, braucht=['holz']), 'lager': G(k=2, HL=1),
    # Klassik
    'markt': G(k=4, E=2, n=2, braucht=['holz']), 'tempel': G(k=5, K=2, braucht=['marmor']), 'aquaedukt': G(k=5, H=2, braucht=['stein']),
    'stadtmauer_stein': G(k=5, S=2, braucht=['stein']), 'werft': G(k=4, prov=['kueste'], A=0, E=1, braucht=['holz']),
    'muenzpraegeanstalt': G(k=6, E=3), 'kolosseum': G(k=6, K=2, braucht=['stein']), 'campus': G(k=6, W=2),
    # Mittelalter
    'kathedrale': G(k=8, K=3, braucht=['marmor']), 'universitaet': G(k=7, W=2, benoetigt=['bibliothek']), 'theater': G(k=6, K=2, braucht=['marmor']),
    'burgturm': G(k=6, S=2, E=0, braucht=['stein']), 'waffenkammer': G(k=7, A=1, braucht=['eisen']), 'heilhaus': G(k=6, H=3),
    'hafen': G(k=8, E=3, prov=['kueste']), 'karawanserei': G(k=7, E=3), 'sternwarte': G(k=6, W=2, braucht=['stein']),
    # Renaissance
    'festungsmauer': G(k=9, S=4, braucht=['stein']), 'bank': G(k=9, E=4, benoetigt=['markt']), 'opernhaus': G(k=9, K=3, benoetigt=['theater'], braucht=['marmor']),
    'akademie': G(k=9, W=3, benoetigt=['universitaet']), 'handelskompanie': G(k=9, E=4), 'schlossgarten': G(k=7, K=2, H=1),
    # Industrie
    'fabrik': G(k=12, E=5, braucht=['kohle']), 'boerse': G(k=12, E=5, benoetigt=['bank']), 'krankenhaus': G(k=10, H=4),
    'museum': G(k=11, K=4, braucht=['marmor']), 'flugfeld': G(k=8, prov=['flug']), 'militaerakademie': G(k=11, A=2, braucht=['eisen']),
    'schule': G(k=9, W=3), 'zoo': G(k=8, K=2, E=1),
    # Moderne
    'forschungslabor': G(k=12, W=4, benoetigt=['universitaet']), 'flughafen': G(k=12, E=4, prov=['flug']), 'betonbunker': G(k=14, S=6, braucht=['eisen']),
    'stadion': G(k=12, K=4), 'einkaufszentrum': G(k=14, E=6), 'rundfunkhaus': G(k=13, K=5), 'raffinerie': G(k=14, E=6, braucht=['oel']),
    # Atomzeit
    'kernkraftwerk': G(k=18, E=8, braucht=['uran']), 'rechenzentrum': G(k=16, W=4, benoetigt=['forschungslabor']),
    'raumfahrtzentrum': G(k=18, K=3, W=3, benoetigt=['forschungslabor']), 'medienzentrum': G(k=16, K=5, benoetigt=['rundfunkhaus']),
    'containerhafen': G(k=18, E=8, braucht=['kueste']), 'solarkraftwerk': G(k=14, E=6), 'klinikum': G(k=16, H=6),
}
def gebaeude_karte(gid):
    g = GEB[gid]; a = GEBAEUDE_AUSWAHL[gid]
    eff = {k: a[k] for k in ('E', 'K', 'W', 'S', 'H', 'A', 'HL') if a.get(k)}
    return dict(typ='gebaeude', id=gid, name=g['name'], zeitalter=g['zeitalter'], kosten=a['k'], effekte=eff,
                prov=a.get('prov', []), braucht=a.get('braucht', []), benoetigt=a.get('benoetigt', []),
                kategorie=g['kategorie'], sprite='gebaeude:' + gid, beschreibung=g['beschreibung'])

# ---------------- Land ----------------
GELAENDE_FARBE = {'grasland': '#a7d37a', 'ebene': '#d6d98e', 'wald': '#6fae62', 'dschungel': '#4f9a5a', 'savanne': '#d9c46f', 'huegel': '#b5b98a',
                  'gebirge': '#a9adb5', 'wueste': '#ecd9a0', 'tundra': '#c3cfc3', 'schnee': '#e6eef4', 'sumpf': '#8fae8a', 'kueste': '#9fd3e6',
                  'salzebene': '#eee8dc', 'oase': '#c3e29a', 'kristallgebirge': '#b6a6d8'}
LAND_AUSWAHL = [  # (rohstoff, gelaende, stapel, kopien)
    ('weizen', 'ebene', 1, 1), ('reis', 'grasland', 1, 1), ('rinder', 'grasland', 1, 1), ('schafe', 'huegel', 1, 1), ('wild', 'wald', 1, 1),
    ('fisch', 'kueste', 1, 1), ('holz', 'wald', 1, 3), ('stein', 'huegel', 1, 2), ('marmor', 'gebirge', 1, 1), ('kupfer', 'huegel', 1, 1),
    ('zinn', 'gebirge', 1, 1), ('pferde', 'savanne', 1, 1), ('eisen', 'gebirge', 1, 1), ('wein', 'huegel', 1, 1), ('elefanten', 'savanne', 1, 1),
    ('pferde', 'ebene', 2, 1), ('eisen', 'huegel', 2, 2), ('salpeter', 'wueste', 2, 2), ('kohle', 'huegel', 2, 1), ('marmor', 'huegel', 2, 1),
    ('stein', 'huegel', 2, 1), ('holz', 'wald', 2, 1), ('gewuerze', 'dschungel', 2, 1), ('seide', 'wald', 2, 1), ('silber', 'tundra', 2, 1),
    ('perlen', 'kueste', 2, 1), ('wale', 'kueste', 2, 1),
    ('kohle', 'grasland', 3, 1), ('oel', 'wueste', 3, 2), ('aluminium', 'huegel', 3, 2), ('uran', 'tundra', 3, 2), ('eisen', 'gebirge', 3, 1),
    ('stein', 'ebene', 3, 1), ('marmor', 'gebirge', 3, 1), ('gold_erz', 'gebirge', 3, 1), ('edelsteine', 'dschungel', 3, 1), ('kakao', 'dschungel', 3, 1),
] + [(r, g, 4, n) for r, g, n in zukunft.LAND_NEU]
LAND_ZEIT = {1: 0, 2: 2, 3: 4, 4: 7}
def land_karte(r, gel, stapel):
    ro = ROH[r]; ertrag = 1
    if ro['art'] == 'luxus': ertrag = 3 if r == 'gold_erz' else 2
    sym = []
    if r in STRAT or r in ('holz', 'stein', 'marmor'): sym.append(r)
    if r in KUESTE_LAND: sym.append('kueste')
    gn = {g['id']: g['name'] for g in D['gelaende']}[gel]
    return dict(typ='land', id='land_' + r + '_' + gel, name=ro['name'], gelaende=gel, gelaende_name=gn, art=ro['art'], zeitalter=LAND_ZEIT[stapel],
                ertrag=ertrag, symbole=sym, sprite='rohstoff:' + r, deko='deko:' + gel if ('deko:' + gel) in json.load(open(os.path.join(HIER, '..', 'sprites.json'))) else None, kosten=0)

# ---------------- Wunder ----------------
WUNDER_KARTEN = {
    'pyramiden': dict(k=10, K=3, G=1, text=['Deine Gebäude kosten 1 Gold weniger (mindestens 1).']),
    'grosse_bibliothek': dict(k=14, K=3, W=2, benoetigt=['bibliothek'], text=[]),
    'koloss': dict(k=14, K=3, E=3, braucht=['kueste'], text=[]),
    'grosse_mauer': dict(k=18, K=3, S=3, text=[]),
    'taj_mahal': dict(k=22, K=4, text=['Dein Gold-Vorrat darf nie durch Ereignisse sinken.']),
    'kristallpalast': dict(k=28, K=3, E=2, L=1, text=['Du darfst jede Runde 1 zusätzliches Land spielen.']),
    'freiheitsstatue': dict(k=34, K=3, E=4, text=[]),
    'internationale_raumstation': dict(k=42, K=3, W=3, Z=1, text=['Du ziehst jede Runde 1 Karte mehr.']),
}
def wunder_karte(wid):
    w = WUN[wid]; a = WUNDER_KARTEN[wid]
    eff = {k: a[k] for k in ('E', 'K', 'W', 'S', 'G', 'L', 'Z') if a.get(k)}
    return dict(typ='wunder', id=wid, name=w['name'], zeitalter=w['zeitalter'], kosten=a['k'], effekte=eff, braucht=['marmor'] + a.get('braucht', []),
                benoetigt=a.get('benoetigt', []), text=a['text'], sprite='wunder:' + wid, beschreibung=w['beschreibung'], kopien=1)

# ---------------- Stadtstaaten ----------------
STAAT_EFFEKT = {
    'salzhafen': dict(E=1), 'goldbrueck': dict(ABLEGEN=1), 'eulenstein': dict(W=1), 'sternwacht': dict(HL=1, Z=0), 'eisenfurt': dict(A=1),
    'falkenwall': dict(S=2), 'lautenheim': dict(K=1), 'rosenau': dict(K=1, H=1), 'moewenkap': dict(SCHIFF=1), 'tiefenhafen': dict(prov=['kueste']),
    'aehrenstedt': dict(H=2), 'honigtal': dict(L=1),
}
def staat_karte(s):
    eff = dict(STAAT_EFFEKT[s['id']])
    prov = eff.pop('prov', [])
    return dict(typ='stadtstaat', id=s['id'], name=s['name'], schwerpunkt=s['schwerpunkt'], farbe=s['farbe'], effekte=eff, prov=prov, zeitalter=0,
                kosten=REGELN['tribut_kosten'], sprite='stadt:stadtstaat', beschreibung=s['beschreibung'], kopien=1)

# ---------------- Ereignisse ----------------
BARBAREN = {
    'waldraeuber': dict(plus=1, folge='stadt', beute=2, einheit='bogenschuetze'),
    'bergclan': dict(plus=2, folge='stadt', beute=3, einheit='speertraeger'),
    'steppennomaden': dict(plus=2, folge='gold', beute=3, einheit='reiter'),
    'piratenbucht': dict(plus=2, folge='gold', beute=4, einheit='galeone'),
    'sumpfvolk': dict(plus=1, folge='stadt', beute=2, einheit='schleuderer'),
    'eisnomaden': dict(plus=3, folge='stadt', beute=4, einheit='krieger'),
}
WETTER = [
    dict(id='regenzeit', name='Gute Ernte', icon='ui:regen', text=['Alle Spieler nehmen 2 Gold.']),
    dict(id='winter', name='Strenger Winter', icon='ui:schnee', text=['Jeder Spieler legt 1 Handkarte seiner Wahl ab (falls er eine hat).']),
    dict(id='seuche', name='Seuche', icon='ui:gift', text=['Jede Stadt verliert 2 Lebenspunkte.', 'Wer Heilung 2 oder mehr hat, bleibt verschont.']),
    dict(id='sonnenwende', name='Sonnenwende', icon='ui:tag', text=['Wer die meiste Kultur hat, nimmt 2 Gold.', '(Bei Gleichstand bekommt niemand etwas.)']),
    dict(id='diebe', name='Nacht der Diebe', icon='ui:nacht', text=['Wer das meiste Gold hat, verliert 3 Gold.', '(Bei Gleichstand verlieren alle Beteiligten.)']),
    dict(id='messe', name='Handelsmesse', icon='ui:handel', text=['Jeder Spieler zieht 1 Karte.']),
]
def barbaren_karte(b):
    a = BARBAREN[b['id']]
    return dict(typ='ereignis', art='barbaren', id=b['id'], name=b['name'], plus=a['plus'], folge=a['folge'], beute=a['beute'],
                sprite='deko:barbarenlager', sprite2='einheit:' + a['einheit'], beschreibung=b['beschreibung'], zeitalter=0, kosten=0)

VOELKER = {
    'nordleute': dict(text=['Seefahrer: Schiffe kosten 1 Gold weniger (mindestens 1) und brauchen keine Küste.']),
    'sonnenvolk': dict(text=['Bauern: Hast du 3 oder mehr Land-Karten, bekommst du 1 Gold zusätzlich Einkommen.']),
    'goldener_bund': dict(text=['Händler: Karten ablegen bringt dir 2 Gold statt 1. Handels-Einheiten bringen 1 Einkommen mehr.']),
    'sternendeuter': dict(text=['Forscher: Der Aufstieg in ein neues Zeitalter kostet dich 1 Gold weniger.']),
    'steppenreiter': dict(text=['Krieger: Reiter kosten 1 Gold weniger (mindestens 1) und bekommen Ansturm +2 statt +1.']),
}

# ---------------- Zusammenbau ----------------
def baue():
    karten = []
    def add(k, stapel, kopien):
        k['stapel'] = stapel; k['kopien'] = kopien; karten.append(k)
    for eid, n in EINHEITEN_AUSWAHL.items():
        k = einheit_karte(eid); add(k, stapel_fuer(k['zeitalter']), n)
    for gid in GEBAEUDE_AUSWAHL:
        k = gebaeude_karte(gid); add(k, stapel_fuer(k['zeitalter']), 1)
    for r, gel, st, n in LAND_AUSWAHL:
        add(land_karte(r, gel, st), st, n)
    for e in zukunft.EINHEITEN:
        k = dict(e, einkommen=e['einkommen']); add(k, 4, 2 if e['id'] == 'exoskelett_infanterie' else 1)
    for g in zukunft.GEBAEUDE: add(dict(g), 4, 1)
    wunder = [wunder_karte(w) for w in WUNDER_KARTEN]
    for wid, w in zukunft.WUNDER.items():
        eff = {kk: w[kk] for kk in ('E', 'K', 'W', 'S', 'G', 'L', 'Z', 'H') if w.get(kk)}
        wunder.append(dict(typ='wunder', id=wid, name=w['name'], zeitalter=w['z'], kosten=w['k'], effekte=eff, braucht=['marmor'] + w['braucht'],
                           benoetigt=w['benoetigt'], text=w['text'], sprite='wunder:' + wid, beschreibung=w['beschreibung'], kopien=1))
    staaten = [staat_karte(s) for s in D['staaten']]
    ereignisse = [barbaren_karte({'id': b['id'], 'name': b['name'], 'beschreibung': b['beschreibung']}) for b in
                  [{'id': i, 'name': n, 'beschreibung': bs} for i, n, bs in [
                      ('waldraeuber', 'Räuberlager im Wald', 'Gesetzlose verstecken sich zwischen den Bäumen und überfallen Händler und Arbeiter.'),
                      ('bergclan', 'Bergclan', 'Ein wilder Clan in den Bergen. Die Krieger kommen herab, um Herden zu stehlen.'),
                      ('steppennomaden', 'Nomadenlager', 'Berittene Plünderer, die schnell kommen und schnell wieder verschwinden.'),
                      ('piratenbucht', 'Piratenbucht', 'Ein Unterschlupf von Seeräubern. Ihre Schiffe lauern Handelsschiffen an der Küste auf.'),
                      ('sumpfvolk', 'Sumpfhütten', 'Im Nebel des Moores leben Ausgestoßene, die sich mit Bögen und Fallen wehren.'),
                      ('eisnomaden', 'Eisnomaden', 'Zähe Jäger aus dem ewigen Eis. Sie ziehen im Winter nach Süden, auf der Suche nach Beute.')]]]
    for w in WETTER: ereignisse.append(dict(typ='ereignis', art='wetter', id=w['id'], name=w['name'], icon=w['icon'], text=w['text'], zeitalter=0, kosten=0))
    voelker = []
    for v in D['ki']:
        voelker.append(dict(typ='volk', id=v['id'], name=v['name'], herrscher=v['herrscher'], farbe=v['farbe'], beschreibung=v['beschreibung'],
                            text=VOELKER[v['id']]['text'], persoenlichkeit=v['persoenlichkeit']))
    for w in wunder: w['stapel'] = 0
    for s in staaten: s['stapel'] = 0
    for e in ereignisse: e['stapel'] = 0; e['kopien'] = 1
    from volk_karten import KARTEN as VOLKSKARTEN
    import civ as _C; _cr, _cp, _cn = _C.baue()
    import religionen as _R; _rel = _R.baue(); _REVT = _R.EREIGNISSE; _GS = _R.GLAUBE_SIEG
    return dict(regeln=REGELN, karten=karten, wunder=wunder, staaten=staaten, ereignisse=ereignisse, voelker=voelker, zeitalter=ZA, volkskarten=VOLKSKARTEN, religionen=_rel[0], relkarten=_rel[1], rel_ereignisse=_REVT, glaube_sieg=_GS, glaube_sieg_vk=_R.GLAUBE_SIEG_VK,
                regierungen=_cr, personen=_cp, naturwunder=_cn, civ=dict(pers_offen=3, natur_offen=4, pers_max=3, pro_zug=1, natur_zeitalter=1))

if __name__ == '__main__':
    s = baue()
    json.dump(s, open(os.path.join(HIER, '..', 'kartensatz.json'), 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    z = Counter()
    for k in s['karten']: z[(k['stapel'], k['typ'])] += k['kopien']
    for st in (1, 2, 3, 4): print('Stapel', st, {t: z[(st, t)] for t in ('einheit', 'gebaeude', 'land')}, 'gesamt', sum(z[(st, t)] for t in ('einheit', 'gebaeude', 'land')))
    print('Wunder', len(s['wunder']), 'Stadtstaaten', len(s['staaten']), 'Ereignisse', len(s['ereignisse']), 'Völker', len(s['voelker']))
    print('Einzelkarten (Duplikate gezählt):', sum(k['kopien'] for k in s['karten']) + len(s['wunder']) + len(s['staaten']) + len(s['ereignisse']))
