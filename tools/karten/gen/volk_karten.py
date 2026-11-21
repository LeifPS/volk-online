"""Volkskarten: je Volk 7 Sonderkarten (eine pro Zeitalter), die nur dieses Volk bekommt (beim Aufstieg)."""
ROEM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']
KUERZEL = {'nordleute': 'NL', 'sonnenvolk': 'SV', 'goldener_bund': 'GB', 'sternendeuter': 'SD', 'steppenreiter': 'SR'}
FARBE = {'nordleute': '#d62828', 'sonnenvolk': '#ffd60a', 'goldener_bund': '#f77f00', 'sternendeuter': '#7209b7', 'steppenreiter': '#e0218a'}
NAME = {'nordleute': 'Nordleute', 'sonnenvolk': 'Sonnenvolk', 'goldener_bund': 'Goldener Bund', 'sternendeuter': 'Sternendeuter', 'steppenreiter': 'Steppenreiter'}
RAHMEN = {'nordleute': '#b32323', 'sonnenvolk': '#c99a00', 'goldener_bund': '#d96c00', 'sternendeuter': '#6a1fa3', 'steppenreiter': '#c21877'}

def E(volk, z, id, name, kosten, st, fern, klasse, sprite, flavor, tags=(), schl=(), boni=None, einkommen=0, ziehen=0):
    return dict(typ='einheit', volk=volk, id=id, name=name, zeitalter=z, kosten=kosten, staerke=st, fern=fern, klasse=klasse, tags=list(tags),
                schluessel=list(schl), boni=boni or {}, braucht=[], einkommen=einkommen, ziehen=ziehen, sprite='einheit:' + sprite, flavor=flavor)

def G(volk, z, id, name, kosten, effekte, sprite, flavor, prov=()):
    return dict(typ='gebaeude', volk=volk, id=id, name=name, zeitalter=z, kosten=kosten, effekte=effekte, prov=list(prov), braucht=[], benoetigt=[],
                kategorie='volk', sprite='gebaeude:' + sprite, flavor=flavor)

KARTEN = [
 # ---- Die Nordleute (Seefahrer) ----
 E('nordleute', 0, 'nl_drachenboot', 'Drachenboot', 3, 3, 0, 'see_nah', 'galeere', 'Der Drachenkopf am Bug erscheint aus dem Nebel, bevor man die Ruder hört.', tags=['see'], schl=['ansturm']),
 G('nordleute', 1, 'nl_leuchtfeuer', 'Leuchtfeuer der Nordküste', 5, dict(E=2, K=1), 'leuchtturm', 'Wer das Feuer sieht, findet nach Hause – und wer es löscht, findet nie wieder heim.'),
 E('nordleute', 2, 'nl_langschiff', 'Langschiff-Flotte', 5, 4, 5, 'see_fern', 'galeasse', 'Ein Pfeilhagel von jedem Ruderplatz, und die Küste hat keine Chance.', tags=['see'], schl=['fern']),
 G('nordleute', 3, 'nl_werftdock', 'Dock der Jarle', 8, dict(A=1, E=2), 'trockendock', 'Wo ein Schiff vom Stapel läuft, wartet das nächste schon auf Kiel und Planken.'),
 E('nordleute', 4, 'nl_panzerschiff', 'Eisenwolf', 8, 8, 0, 'see_nah', 'panzerschiff', 'Unter dem Namen der alten Schiffe fährt eine Burg aus Eisen über die See.', tags=['see']),
 G('nordleute', 5, 'nl_nordhafen', 'Nordhafen', 12, dict(E=4, K=2), 'grosshafen', 'Eisfrei das ganze Jahr: Kräne, Kais und das Lied der Möwen.'),
 E('nordleute', 6, 'nl_traeger', 'Polarträger', 12, 7, 0, 'traeger', 'supertraeger', 'Eine schwimmende Insel mit Landebahn – die Jarle nennen sie „Wal“.', tags=['see'], schl=['traeger']),
 # ---- Das Sonnenvolk (Bauern) ----
 G('sonnenvolk', 0, 'sv_brunnen', 'Sonnenbrunnen', 3, dict(E=1, H=1), 'brunnen', 'Das Wasser ist kühl, die Erde warm, und beides gehört allen.'),
 G('sonnenvolk', 1, 'sv_bad', 'Sonnenbad', 6, dict(K=2, H=1), 'badehaus', 'Hier verhandeln Fürstinnen und Bauern im selben warmen Wasser.'),
 G('sonnenvolk', 2, 'sv_speicher', 'Sonnenspeicher', 6, dict(E=1, L=1), 'speicherhaus', 'Hohe Dächer, tiefe Keller – der Speicher ist nie leer, wenn die Felder reichen.'),
 G('sonnenvolk', 3, 'sv_manufaktur', 'Webhaus der Sonne', 8, dict(E=3, K=1), 'manufaktur', 'Goldgelbe Tücher, die man erkennt, ehe der Händler den Mund aufmacht.'),
 E('sonnenvolk', 4, 'sv_heiler', 'Sonnenheiler', 5, 3, 0, 'sanitaeter', 'sanitaeter', 'Sie kennen jedes Kraut und jeden Brauch. Wer bei ihnen liegt, steht bald wieder.', schl=['heilen']),
 G('sonnenvolk', 5, 'sv_kuehlhaus', 'Erntekammer', 11, dict(E=3, H=2), 'kuehlhaus', 'Die Ernte des Sommers reicht für den ganzen Winter und für das Fest dazwischen.'),
 G('sonnenvolk', 6, 'sv_solar', 'Sonnenfeld', 15, dict(E=6, K=2), 'solarkraftwerk', 'Das Licht, das einst die Felder nährte, läuft jetzt durch Drähte.'),
 # ---- Der Goldene Bund (Händler) ----
 E('goldener_bund', 0, 'gb_kontorkahn', 'Kontorkahn', 4, 1, 0, 'see_zivil', 'arbeitsboot', 'Ein kleines Boot, ein großes Hauptbuch.', tags=['see'], einkommen=1),
 G('goldener_bund', 1, 'gb_kontor', 'Kontor', 5, dict(E=1, G=1), 'werkstatt', 'Waagen, Siegel und eine Tür, die erst nach dem Geschäft aufgeht.'),
 G('goldener_bund', 2, 'gb_lagerhaus', 'Gildenlagerhaus', 6, dict(E=1, HL=2), 'lagerhaus', 'Sicherheit hat ihren Preis, und der Bund verkauft sie.'),
 E('goldener_bund', 3, 'gb_handelsflotte', 'Handelsflotte', 7, 2, 0, 'see_zivil', 'karavelle', 'Zwölf Segel am Horizont – zwölf Verträge im Wind.', tags=['see'], einkommen=2),
 G('goldener_bund', 4, 'gb_bahnhof', 'Gildenbahnhof', 10, dict(E=1, K=1, Z=1), 'bahnhof', 'Pünktlich wie ein Wechsel – und mindestens so einträglich.'),
 E('goldener_bund', 5, 'gb_konvoi', 'Gildenkonvoi', 9, 2, 0, 'haendler', 'lastwagenkonvoi', 'Planen, Plomben, Papiere: Alles ist da, nur kein Zoll.', einkommen=2),
 G('goldener_bund', 6, 'gb_kontor2', 'Selbstbuchendes Kontor', 15, dict(E=5, K=1, G=1), 'robotfabrik', 'Maschinen zählen schneller als Menschen – aber der Bund bleibt der Auftraggeber.'),
 # ---- Die Sternendeuter (Forscher) ----
 G('sternendeuter', 0, 'sd_turm', 'Sternenturm', 3, dict(W=1, K=1, S=1), 'wachturm', 'Der erste, der hier nachts Wache hielt, sah mehr Sterne als Feinde.'),
 G('sternendeuter', 1, 'sd_schmiede', 'Astrolabienschmiede', 6, dict(W=2, K=1), 'bronzeschmiede', 'Aus Bronze wird Himmelskunde: jede Skala ein Versprechen an die Zukunft.'),
 G('sternendeuter', 2, 'sd_archiv', 'Sternenarchiv', 7, dict(W=1, Z=1, E=1), 'depot', 'Tausend Tafeln, nach Himmelsrichtung geordnet.'),
 G('sternendeuter', 3, 'sd_labor', 'Alchemistenlabor', 9, dict(W=2, E=2, K=1, S=1), 'pulvermuehle', 'Es knallt, es dampft, und manchmal entsteht Wissen.'),
 G('sternendeuter', 4, 'sd_warte', 'Große Himmelswarte', 10, dict(W=2, E=2, K=1), 'sternwarte', 'Das Rohr zeigt weiter, als der Verstand reicht – das ist der Sinn.'),
 E('sternendeuter', 5, 'sd_kundschafter', 'Sternkundschafter', 7, 2, 0, 'spaeher', 'fernaufklaerer', 'Sie fliegen höher als alle anderen, denn sie wollen zu den Sternen.', ziehen=2),
 G('sternendeuter', 6, 'sd_raketen', 'Himmelsbahnhof', 16, dict(W=3, K=3), 'raketenbasis', 'Am Ende der Rechnung steht ein Feuerstrahl und eine Frage.'),
 # ---- Die Steppenreiter (Krieger) ----
 E('steppenreiter', 0, 'sr_pferdebogner', 'Pferdebogner', 2, 2, 3, 'fernkampf', 'berittener_bogenschuetze', 'Aus dem Galopp getroffen – ehe der Staub sich legt.', tags=['reiter'], schl=['fern']),
 G('steppenreiter', 1, 'sr_zeltlager', 'Zeltlager des Khans', 5, dict(A=1, HL=1, K=2, E=1), 'stall', 'Wo die Zelte stehen, ist Heimat. Morgen steht dort Gras.'),
 G('steppenreiter', 2, 'sr_pferdezucht', 'Pferdezucht', 8, dict(A=1, E=3), 'gestuet', 'Ein Pferd gehört niemandem und trägt dennoch jeden – außer Fremde.'),
 E('steppenreiter', 3, 'sr_leibreiter', 'Leibreiter des Khans', 8, 7, 0, 'reiter', 'ritter', 'Sie reiten vor dem Wind her und sind schon da, wenn er ankommt.', tags=['reiter'], schl=['ansturm']),
 G('steppenreiter', 4, 'sr_stahlwerk', 'Waffenschmiede der Khane', 10, dict(A=1, S=2, K=1, E=1), 'stahlwerk', 'Die Hufe sind aus Stahl, der Wille aus Stein.'),
 E('steppenreiter', 5, 'sr_hubschrauber', 'Stahlpferd-Schwadron', 11, 10, 0, 'reiter', 'kampfhubschrauber', 'Das Pferd ist geblieben, nur die Mähne dreht sich jetzt.', tags=['reiter'], schl=['ansturm']),
 E('steppenreiter', 6, 'sr_panzerhorde', 'Panzerhorde', 12, 12, 0, 'reiter', 'panzergrenadier', 'Die Steppe bebt wieder, wenn der Khan ruft.', tags=['reiter'], schl=['ansturm']),
]
import zukunft
KARTEN += zukunft.VOLKSKARTEN
for k in KARTEN:
    k['nr'] = '%s-%s' % (KUERZEL[k['volk']], ROEM[k['zeitalter']])
    k['rahmen'] = RAHMEN[k['volk']]; k['farbe_volk'] = FARBE[k['volk']]; k['volk_name'] = NAME[k['volk']]
    k['stapel'] = 0; k['kopien'] = 1; k['beschreibung'] = k['flavor']
    k['volkskarte'] = True
def nach_volk():
    d = {}
    for k in KARTEN: d.setdefault(k['volk'], []).append(k)
    for v in d.values(): v.sort(key=lambda k: k['zeitalter'])
    return d
