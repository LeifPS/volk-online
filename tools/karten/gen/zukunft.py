"""Die vier Zeitalter nach der Atomzeit: VIII KI-Zeitalter, IX Fusionszeitalter, X Weltraumzeitalter, XI Sternenzeitalter.
Alle Karten dieser Zeitalter liegen im Stapel IV. Grafiken: zukunft_spr.py / zukunft_spr2.py (selbst gezeichnet).
Zeitalter-Indizes 7..10. Werte wurden nach der Selbstspiel-Simulation eingestellt (siehe ENTSCHEIDUNGEN.md)."""

ZA_NEU = [
    dict(id='ki', name='KI-Zeitalter', farbe='#5b8cff', stil='smart', beschreibung='Glastürme mit Dachgärten, Roboter, Drohnen und lernende Maschinen.'),
    dict(id='fusion', name='Fusionszeitalter', farbe='#f2a33a', stil='fusion', beschreibung='Weiße Kuppeln mit Lichtbändern, Plasma und saubere Energie.'),
    dict(id='weltraum', name='Weltraumzeitalter', farbe='#8e7cc3', stil='orbital', beschreibung='Raumhäfen, Orbitalstationen, Mond und Mars.'),
    dict(id='sterne', name='Sternenzeitalter', farbe='#e6eef7', stil='stern', beschreibung='Antimaterie, Sternenschiffe und kristalline Türme.'),
]
ROH_NEU = [
    dict(id='seltene_erden', name='Seltene Erden', art='strategisch', gelaende=['huegel', 'gebirge'], zweck='Roboter, Drohnen und KI-Gebäude.'),
    dict(id='deuterium', name='Deuterium', art='strategisch', gelaende=['kueste'], zweck='Fusionsreaktoren und Plasmawaffen.'),
    dict(id='titan', name='Titan', art='strategisch', gelaende=['gebirge'], zweck='Raumschiffe und Orbitalbauten.'),
    dict(id='helium3', name='Helium-3', art='strategisch', gelaende=['kristallgebirge'], zweck='Sternenschiffe und Antimaterie.'),
]
NEUE_SYMBOLE = ['seltene_erden', 'deuterium', 'titan', 'helium3']

def E(z, id, name, k, st, fern, klasse, braucht=(), tags=(), schl=(), boni=None, einkommen=0, ziehen=0, text=''):
    return dict(typ='einheit', id=id, name=name, zeitalter=z, kosten=k, staerke=st, fern=fern, klasse=klasse, tags=list(tags), schluessel=list(schl),
                boni=boni or {}, braucht=list(braucht), einkommen=einkommen, ziehen=ziehen, sprite='einheit:' + id, beschreibung=text)

def G(z, id, name, k, eff, kat, text, braucht=(), benoetigt=(), prov=()):
    return dict(typ='gebaeude', id=id, name=name, zeitalter=z, kosten=k, effekte=eff, prov=list(prov), braucht=list(braucht), benoetigt=list(benoetigt),
                kategorie=kat, sprite='gebaeude:' + id, beschreibung=text)

# ---------------- Einheiten (25) ----------------
EINHEITEN = [
    # VIII KI-Zeitalter (Index 7)
    E(7, 'exoskelett_infanterie', 'Exoskelett-Infanterie', 12, 12, 0, 'nahkampf', ['seltene_erden'], tags=['nahkampf'], text='Soldaten in kraftverstärkten Anzügen. Schnell zu Fuß und schwer zu stoppen.'),
    E(7, 'kampfroboter', 'Kampfroboter', 13, 13, 0, 'nahkampf', ['seltene_erden', 'eisen'], tags=['nahkampf'], boni={'belagerung': 2}, text='Unermüdliche Maschinen, die keine Angst kennen. Besonders gefährlich für Geschütze.'),
    E(7, 'drohnenschwarm', 'Drohnenschwarm', 12, 8, 12, 'fernkampf', ['seltene_erden'], schl=['fern'], text='Hunderte kleine Drohnen, die gleichzeitig angreifen und sich nicht abschütteln lassen.'),
    E(7, 'autonomer_panzer', 'Autonomer Panzer', 14, 14, 0, 'reiter', ['oel', 'seltene_erden'], tags=['reiter'], schl=['ansturm'], text='Ein Panzer ohne Besatzung. Er rechnet schneller, als jeder Kommandant befehlen kann.'),
    E(7, 'drohnenjaeger', 'Drohnenjäger', 13, 11, 11, 'jaeger', ['seltene_erden', 'aluminium', 'flug'], tags=['luft'], schl=['fern', 'fliegend'], boni={'bomber': 2}, text='Eine selbststeuernde Jagdmaschine, die Bomber schon beim Start erkennt.'),
    E(7, 'lieferdrohnen', 'Lieferdrohnen', 6, 1, 0, 'haendler', [], einkommen=3, text='Tausend Pakete pro Stunde – ganz ohne Fahrer, Straße und Pause.'),
    # IX Fusionszeitalter (Index 8)
    E(8, 'plasmagrenadier', 'Plasmagrenadier', 14, 14, 0, 'nahkampf', ['deuterium', 'seltene_erden'], tags=['nahkampf'], boni={'stadt': 1}, text='Gepanzerte Grenadiere mit Plasmawerfern. Mauern schmelzen vor ihnen.'),
    E(8, 'schwebepanzer', 'Schwebepanzer', 15, 15, 0, 'reiter', ['seltene_erden', 'deuterium'], tags=['reiter'], schl=['ansturm'], text='Ein Panzer auf Magnetfeldern. Kein Hügel, kein Fluss hält ihn auf.'),
    E(8, 'railgun_batterie', 'Railgun-Batterie', 15, 9, 15, 'belagerung', ['seltene_erden', 'deuterium'], tags=['belagerung'], schl=['belagerung'], text='Magnetische Schienen schleudern Geschosse mit mehrfacher Schallgeschwindigkeit.'),
    E(8, 'laserabwehr', 'Laserabwehr', 13, 11, 0, 'flak', ['seltene_erden'], schl=['luftabwehr'], boni={'luft': 3, 'rakete': 3}, text='Lichtblitze finden jedes Ziel am Himmel, bevor es die Stadt erreicht.'),
    E(8, 'fusionszerstoerer', 'Fusionszerstörer', 15, 14, 0, 'see_nah', ['deuterium', 'kueste'], tags=['see'], boni={'u_boot': 2}, text='Ein Kriegsschiff mit Fusionsantrieb. Es fährt monatelang ohne Treibstoff.'),
    E(8, 'schildfregatte', 'Schildfregatte', 15, 10, 14, 'see_fern', ['deuterium', 'kueste'], tags=['see'], schl=['fern'], text='Ein Energieschild schützt Rumpf und Besatzung vor fast allen Treffern.'),
    E(8, 'hyperloop_kurier', 'Hyperloop-Kurier', 7, 1, 0, 'haendler', [], einkommen=3, text='Waren in Kapseln, die durch Vakuumröhren schießen. Von Küste zu Küste in Minuten.'),
    # X Weltraumzeitalter (Index 9)
    E(9, 'raumjaeger', 'Raumjäger', 16, 14, 14, 'jaeger', ['titan', 'flug'], tags=['luft'], schl=['fern', 'fliegend'], boni={'bomber': 2}, text='Ein wendiger Jäger, der aus dem Orbit startet und in Sekunden überall ist.'),
    E(9, 'orbital_marine', 'Orbital-Marine', 16, 17, 0, 'nahkampf', ['titan', 'seltene_erden'], tags=['nahkampf'], text='Elitesoldaten, die in Landekapseln aus dem Orbit abspringen.'),
    E(9, 'kampfshuttle', 'Kampfshuttle', 17, 11, 16, 'bomber', ['titan', 'flug'], tags=['luft', 'bomber'], schl=['belagerung', 'fliegend'], boni={'stadt': 1}, text='Ein Raumgleiter mit Bombenschacht. Er wirft seine Last aus 100 Kilometern Höhe ab.'),
    E(9, 'hyperschallbomber', 'Hyperschallbomber', 17, 10, 17, 'bomber', ['deuterium', 'flug'], tags=['luft', 'bomber'], schl=['belagerung', 'fliegend', 'tarnung'], boni={'stadt': 1}, text='Schneller als jede Abwehr. Wenn man ihn hört, ist er schon vorbei.'),
    E(9, 'marsrover_panzer', 'Marsrover-Panzer', 17, 17, 0, 'reiter', ['titan', 'seltene_erden'], tags=['reiter'], schl=['ansturm'], text='Gebaut für Marsstaub und Eiswüsten. Auf der Erde ist er fast unaufhaltsam.'),
    E(9, 'asteroidenfrachter', 'Asteroidenfrachter', 14, 1, 0, 'haendler', ['titan'], einkommen=4, text='Er bringt Eisen, Titan und Wasser von fernen Asteroiden. Das Geschäft des Jahrhunderts.'),
    E(9, 'terraformer', 'Terraformer', 11, 1, 0, 'zivil', [], einkommen=3, text='Eine Maschine, die tote Welten in Gärten verwandelt – und alte Böden in Paradiese.'),
    # XI Sternenzeitalter (Index 10)
    E(10, 'sternenkreuzer', 'Sternenkreuzer', 21, 18, 18, 'jaeger', ['helium3', 'flug'], tags=['luft'], schl=['fern', 'fliegend'], boni={'bomber': 2, 'rakete': 2}, text='Ein Schlachtkreuzer, der zwischen den Sternen kreuzt. Sein Schatten allein erschreckt Flotten.'),
    E(10, 'sternenkrieger', 'Sternenkrieger', 20, 21, 0, 'nahkampf', ['titan', 'helium3'], tags=['nahkampf'], text='Eine Rüstung aus Titan, ein Reaktor auf dem Rücken, und der Mut von tausend Generationen.'),
    E(10, 'nanoschwarm', 'Nanoschwarm', 19, 12, 18, 'fernkampf', ['seltene_erden', 'titan'], schl=['fern', 'tarnung'], text='Eine Wolke aus winzigen Maschinen. Man sieht sie nicht, bis sie zugreifen.'),
    E(10, 'orbitalkanone', 'Orbitalkanone', 22, 10, 21, 'belagerung', ['helium3', 'titan'], tags=['belagerung'], schl=['belagerung'], text='Ein Geschütz im All. Es braucht keine Reichweite, nur einen klaren Himmel.'),
    E(10, 'antimaterie_rakete', 'Antimaterie-Rakete', 24, 0, 22, 'rakete', ['helium3', 'flug'], tags=['luft', 'rakete'], schl=['belagerung', 'fliegend', 'einmalig'], text='Sprengkopf mit gespeicherter Antimaterie. Ein Gramm reicht für eine ganze Metropole.'),
]

# ---------------- Gebäude (21) ----------------
GEBAEUDE = [
    # VIII
    G(7, 'ki_labor', 'KI-Labor', 18, dict(W=4, E=1), 'wissen', 'Maschinen forschen rund um die Uhr und stellen sich ihre Fragen selbst.', ['seltene_erden']),
    G(7, 'autonome_fabrik', 'Autonome Fabrik', 18, dict(E=8), 'produktion', 'Kein Mensch im Gebäude. Das Licht ist aus, die Produktion läuft.', ['seltene_erden']),
    G(7, 'intelligentes_stromnetz', 'Intelligentes Stromnetz', 15, dict(E=5), 'produktion', 'Das Netz verteilt jede Kilowattstunde dorthin, wo sie gerade gebraucht wird.'),
    G(7, 'vertikalfarm', 'Vertikalfarm', 15, dict(E=3, H=3), 'nahrung', 'Salat im Hochhaus: zwanzig Etagen Ernte, ganz ohne Acker.'),
    G(7, 'virtuelles_forum', 'Virtuelles Forum', 19, dict(K=6), 'kultur', 'Der Marktplatz der Zukunft: Millionen Stimmen in einem gemeinsamen Raum.'),
    G(7, 'laserturm', 'Laserturm', 16, dict(S=7), 'verteidigung', 'Ein Turm, der Angreifer schon am Horizont aus dem Himmel brennt.', ['seltene_erden']),
    # IX
    G(8, 'fusionsreaktor', 'Fusionsreaktor', 22, dict(E=10), 'produktion', 'Eine kleine Sonne im Keller: viel Energie, kein Abfall und kaum Risiko.', ['deuterium']),
    G(8, 'quantenrechner', 'Quantenrechner', 21, dict(W=5, E=1), 'wissen', 'Er probiert alle Antworten gleichzeitig und weiß dann, welche stimmt.', [], ['ki_labor']),
    G(8, 'co2_waescher', 'CO2-Wäscher', 17, dict(K=3, H=2), 'zufriedenheit', 'Riesige Filter holen das Gas aus der Luft. Der Himmel wird wieder blau.'),
    G(8, 'energieschild', 'Energieschild', 20, dict(S=8), 'verteidigung', 'Eine unsichtbare Kuppel aus Licht, an der selbst Raketen abprallen.', ['deuterium']),
    G(8, 'hyperloop_station', 'Hyperloop-Station', 20, dict(E=5, K=2), 'infrastruktur', 'Abfahrt alle zwei Minuten. Ankunft vor der Abfahrt – gefühlt jedenfalls.'),
    # X
    G(9, 'raumhafen', 'Raumhafen', 22, dict(E=6), 'infrastruktur', 'Hier starten Raumschiffe. Er zählt als Flugfeld für deine Einheiten.', ['titan'], prov=['flug']),
    G(9, 'orbitalstation', 'Orbitalstation', 24, dict(W=5, K=2), 'wissen', 'Ein Labor im Orbit. Alle Forscher der Erde teilen sich die Aussicht.', [], ['raumhafen']),
    G(9, 'mondbasis', 'Mondbasis', 23, dict(E=7, K=1), 'infrastruktur', 'Eine Siedlung unter der Mondoberfläche. Von hier aus ist alles nur noch ein Sprung.', ['titan']),
    G(9, 'kolonie_kuppel', 'Kolonie-Kuppel', 22, dict(E=3, H=4, K=2), 'zufriedenheit', 'Unter dem Glas wachsen Bäume und Hoffnung auf fremden Welten.'),
    G(9, 'sternenwerft', 'Sternenwerft', 25, dict(A=2, E=4), 'militaer', 'Hier entstehen die Schiffe, die die Erde verlassen. Einheiten werden billiger.', ['titan']),
    G(9, 'helium3_raffinerie', 'Helium-3-Raffinerie', 23, dict(E=9), 'produktion', 'Der Mond liefert den Staub, die Raffinerie den Brennstoff für die Sterne.', ['helium3']),
    # XI
    G(10, 'terraforming_station', 'Terraforming-Station', 28, dict(E=7, H=5, K=3), 'nahrung', 'Sie macht aus Wüstenplaneten fruchtbares Land.', ['helium3']),
    G(10, 'antimaterie_fabrik', 'Antimaterie-Fabrik', 30, dict(E=12), 'produktion', 'Ein Gramm pro Jahr, gespeichert in Magnetfallen. Mehr Energie gibt es nicht.', ['helium3']),
    G(10, 'gravitationsschild', 'Gravitationsschild', 26, dict(S=10), 'verteidigung', 'Die Schwerkraft selbst wird zur Mauer: Nichts kommt hindurch.', ['titan']),
    G(10, 'kristallturm', 'Kristallturm', 27, dict(K=7), 'kultur', 'Ein Turm aus gewachsenem Kristall. Sein Leuchten ist im ganzen Land zu sehen.'),
]

# ---------------- Wunder (4) ----------------
WUNDER = {
    'weltgehirn': dict(name='Weltgehirn', z=7, k=50, K=3, W=4, E=3, benoetigt=['ki_labor'], braucht=['seltene_erden'], text=[],
                       beschreibung='Alle Rechner der Welt denken gemeinsam. Dein Reich lernt schneller, als es fragen kann.'),
    'kuenstliche_sonne': dict(name='Künstliche Sonne', z=8, k=58, K=3, E=8, H=2, benoetigt=['fusionsreaktor'], braucht=['deuterium'], text=[],
                              beschreibung='Ein Fusionsstern am Himmel. Es wird nie wieder Nacht auf deinen Feldern.'),
    'weltraumaufzug': dict(name='Weltraumaufzug', z=9, k=66, K=3, E=4, Z=1, benoetigt=['raumhafen'], braucht=['titan'], text=['Du ziehst jede Runde 1 Karte mehr.'],
                           beschreibung='Ein Seil bis in den Orbit. Der Weg ins All kostet nur noch Strom.'),
    'sternenarche': dict(name='Sternenarche', z=10, k=74, K=4, E=5, H=4, benoetigt=['sternenwerft'], braucht=['helium3'], text=[],
                         beschreibung='Ein Schiff für ein ganzes Volk. Die Zukunft beginnt dort, wo die Karte endet.'),
}

# ---------------- Land-Karten (Stapel IV): (Rohstoff, Gelände, Kopien) ----------------
LAND_NEU = [
    ('seltene_erden', 'huegel', 3), ('deuterium', 'kueste', 3), ('titan', 'gebirge', 3), ('helium3', 'kristallgebirge', 2),
    ('aluminium', 'wueste', 1), ('oel', 'tundra', 1), ('eisen', 'tundra', 1), ('uran', 'huegel', 1),
    ('edelsteine', 'huegel', 1), ('gold_erz', 'wueste', 1), ('marmor', 'ebene', 1), ('stein', 'wueste', 1),
]

# ---------------- Volkskarten (je Volk 4 neue: VIII–XI) ----------------
def VE(volk, z, id, name, k, st, fern, klasse, flavor, tags=(), schl=(), boni=None, einkommen=0, ziehen=0):
    return dict(typ='einheit', volk=volk, id=id, name=name, zeitalter=z, kosten=k, staerke=st, fern=fern, klasse=klasse, tags=list(tags),
                schluessel=list(schl), boni=boni or {}, braucht=(['flug'] if 'fliegend' in schl else []), einkommen=einkommen, ziehen=ziehen, sprite='einheit:' + id, flavor=flavor)
def VG(volk, z, id, name, k, eff, flavor, prov=()):
    return dict(typ='gebaeude', volk=volk, id=id, name=name, zeitalter=z, kosten=k, effekte=eff, prov=list(prov), braucht=[], benoetigt=[],
                kategorie='volk', sprite='gebaeude:' + id, flavor=flavor)

VOLKSKARTEN = [
    # Nordleute
    VG('nordleute', 7, 'nl_ki_hafen', 'KI-Hafen', 19, dict(E=6, K=2), 'Kräne ohne Fahrer, Schiffe ohne Wartezeit – und die Möwen sind die Einzigen, die noch schreien.'),
    VE('nordleute', 8, 'nl_fusionsschiff', 'Fusionsschiff', 16, 15, 0, 'see_nah', 'Der Reaktor glüht wie eine Sonne im Rumpf. Das Meer kennt keinen Winter mehr.', tags=['see'], boni={'u_boot': 2}),
    VG('nordleute', 9, 'nl_orbitalwerft', 'Orbitalwerft', 21, dict(A=2, E=4, K=1), 'Die Jarle bauen ihre Langschiffe jetzt im Orbit – und sie nennen sie immer noch Drachen.', prov=['flug']),
    VE('nordleute', 10, 'nl_sternensegler', 'Sternensegler', 22, 18, 16, 'jaeger', 'Segel aus Licht, Kiel aus Titan. Die Nordleute haben endlich einen Horizont, der nie endet.', tags=['luft'], schl=['fern', 'fliegend'], boni={'rakete': 2}),
    # Sonnenvolk
    VG('sonnenvolk', 7, 'sv_gewaechshaus', 'Gewächshaus-Turm', 17, dict(E=4, H=3, K=1), 'Zwanzig Etagen Sonne, Tomaten bis unters Dach und überall der Duft von Erde.'),
    VG('sonnenvolk', 8, 'sv_sonnenreaktor', 'Sonnenreaktor', 20, dict(E=8, K=2), 'Das Volk der Sonne hat sich eine eigene gebaut – und teilt sie mit allen.'),
    VE('sonnenvolk', 9, 'sv_mondgaertner', 'Mondgärtner', 14, 4, 0, 'sanitaeter', 'Auf dem Mond blüht der erste Garten. Er heilt jeden, der ihn betritt.', schl=['heilen'], einkommen=2),
    VG('sonnenvolk', 10, 'sv_gartenwelt', 'Gartenwelt', 27, dict(E=9, H=4, K=3, L=1), 'Ein ganzer Planet als Garten. Es gibt keine Wüste mehr, nur noch Wege dazwischen.'),
    # Goldener Bund
    VE('goldener_bund', 7, 'gb_lieferflotte', 'Lieferdrohnen-Flotte', 11, 2, 0, 'haendler', 'Hunderte Drohnen, jede mit Siegel und Rechnung. Der Bund liefert schneller als ein Gedanke.', einkommen=3),
    VG('goldener_bund', 8, 'gb_quantenboerse', 'Quantenbörse', 22, dict(E=7, K=1, G=1), 'Jeder Preis ist schon bekannt, ehe das Geschäft beginnt – und der Bund hat ihn nie zu hoch gesetzt.'),
    VE('goldener_bund', 9, 'gb_orbitalfrachter', 'Orbitalfrachter', 14, 3, 0, 'haendler', 'Ein Frachter zwischen Erde und Mond. Seine Ladung zahlt sich schon vor dem Landen aus.', einkommen=4),
    VG('goldener_bund', 10, 'gb_sternenmarkt', 'Sternenmarkt', 28, dict(E=11, K=2, HL=2), 'Ein Basar zwischen den Sternen: Händler aus tausend Welten, eine Währung – Gold.'),
    # Sternendeuter
    VG('sternendeuter', 7, 'sd_ki_observatorium', 'KI-Observatorium', 18, dict(W=4, K=1, E=1), 'Die Maschine zählt Sterne und sagt dem Forscher, welche er noch nicht gefunden hat.'),
    VG('sternendeuter', 8, 'sd_quantenwarte', 'Quantenwarte', 21, dict(W=4, E=2, K=1), 'Ein Teleskop, das nicht schaut, sondern fragt. Und der Himmel antwortet.'),
    VG('sternendeuter', 9, 'sd_orbitalteleskop', 'Orbitalteleskop', 24, dict(W=5, K=2, Z=1), 'Über allen Wolken sieht man weiter, als je ein Mensch geträumt hat.'),
    VG('sternendeuter', 10, 'sd_sternenpforte', 'Sternenpforte', 30, dict(W=6, K=3, Z=1), 'Ein Tor, durch das man nicht geht, sondern fällt – direkt zwischen die Sterne.'),
    # Steppenreiter
    VE('steppenreiter', 7, 'sr_roboterreiter', 'Roboterreiter', 13, 13, 0, 'reiter', 'Das Pferd ist aus Stahl und trägt den Khan trotzdem so frei wie früher den Wind.', tags=['reiter'], schl=['ansturm']),
    VG('steppenreiter', 8, 'sr_plasmaschmiede', 'Plasmaschmiede', 21, dict(A=2, S=2, K=1, E=2), 'In der Plasmaschmiede glüht, was früher Stahl war. Jede Klinge ein Funke.'),
    VE('steppenreiter', 9, 'sr_marsreiter', 'Marsreiter', 18, 17, 0, 'reiter', 'Rotes Land, roter Staub, und der Khan reitet voran. Die Steppe hat jetzt einen neuen Namen.', tags=['reiter'], schl=['ansturm']),
    VE('steppenreiter', 10, 'sr_sternenhorde', 'Sternenhorde', 22, 22, 0, 'reiter', 'Zehntausend Reiter zwischen den Sternen. Wer sie sieht, hat nichts mehr zu fürchten – außer dem Khan.', tags=['reiter'], schl=['ansturm']),
]

# Rückgängig gemachte Wissens-Streichung (Z VII wie vor dem Patch cbf4d10)
ATOM_WISSEN = {
    'rechenzentrum': dict(W=4),
    'raumfahrtzentrum': dict(K=3, W=3),
}
ATOM_WUNDER_ISS = dict(K=3, W=3, Z=1)
ATOM_VOLK = {'sd_raketen': dict(W=3, K=3)}

def ergaenze(D):
    """Trägt Zeitalter, Rohstoffe, Gebäude und Wunder in die Spieldaten ein (für Namen/Typen im Generator)."""
    D['zeitalter'].extend(ZA_NEU)
    D['rohstoffe'].extend(dict(id=r['id'], name=r['name'], art=r['art'], gelaende=r['gelaende'], zweck=r['zweck']) for r in ROH_NEU)
    D['gebaeude'].extend(dict(id=g['id'], name=g['name'], zeitalter=g['zeitalter'], kategorie=g['kategorie'], beschreibung=g['beschreibung']) for g in GEBAEUDE)
    D['wunder'].extend(dict(id=k, name=w['name'], zeitalter=w['z'], kategorie='wunder', beschreibung=w['beschreibung']) for k, w in WUNDER.items())
    D['einheiten'].extend(dict(id=e['id'], name=e['name'], zeitalter=e['zeitalter'], klasse=e['klasse'], beschreibung=e['beschreibung']) for e in EINHEITEN)
