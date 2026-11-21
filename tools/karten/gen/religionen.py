"""Erweiterung „Götter & Glaube“: 8 Religionen mit je 6 Kartensorten (7 Karten), 6 Ereigniskarten."""
ROEM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
EMBLEM = {'sonnenkult': 'sonne', 'mondgilde': 'mond', 'hain': 'baum', 'gezeiten': 'welle', 'berggeister': 'berg', 'flammenorden': 'flamme', 'sternenorakel': 'stern', 'windwanderer': 'wind'}
GLAUBE_SIEG = 13      # nur Grundspiel + Religion
GLAUBE_SIEG_VK = 12   # zusammen mit der Volkskarten-Erweiterung
GRUENDEN_KOSTEN = 5

# id, Name, Farbe, Rahmen(dunkler), Fähigkeit (Titel, Text), Flavor, [Heiligtum, Tempel, Halle, Stätte, Prophet] je (Name, Effekte, Flavor)
REL = [
 dict(id='sonnenkult', name='Pfad der Sonne', farbe='#e8a317', rahmen='#b87d00', titel='Sonnensegen', text='Du bekommst +1 Einkommen je 3 Glaube.',
      flavor='Wer dem Licht folgt, dem wächst die Ernte von selbst.',
      karten=[('Sonnenaltar', dict(F=1, E=1), 'Ein Stein, auf den der erste Morgenstrahl fällt.'), ('Sonnentempel', dict(F=2, E=1), 'Die Stufen sind warm, auch wenn die Nacht kalt war.'),
              ('Halle der Morgenröte', dict(F=2, E=2), 'Vor dem Tor wird nicht gebettelt, sondern gesungen.'), ('Große Sonnenpyramide', dict(F=3, K=2), 'Von ihrer Spitze sieht man den Anfang des Tages.'),
              ('Sonnenprophet', None, 'Sein Gewand leuchtet, wenn er spricht.')]),
 dict(id='mondgilde', name='Mondgilde', farbe='#5b6fb5', rahmen='#3a4d8f', titel='Nachtwache', text='Dein Handlimit ist +2, du ziehst 1 Karte mehr pro Zug, und beim Ablegen für Gold bekommst du 1 Gold mehr.',
      flavor='Die Gilde lernt im Dunkeln, was dem Tag verborgen bleibt.',
      karten=[('Mondschrein', dict(F=1, HL=1), 'Ein stilles Becken, in dem sich der Mond spiegelt.'), ('Mondtempel', dict(F=2, HL=1), 'Der Raum ist rund und das Licht silbern.'),
              ('Silberhalle', dict(F=2, HL=2), 'Hier wird erst nach Mitternacht Rat gehalten.'), ('Mondobservatorium', dict(F=3, W=1, K=1), 'Wer lange genug hinaufsieht, rechnet bald mit Gezeiten.'),
              ('Mondweise', None, 'Sie kennen die Nächte besser als ihre eigenen Hände.')]),
 dict(id='hain', name='Hain der Alten', farbe='#2f8f4e', rahmen='#1f6b36', titel='Heilende Haine', text='Deine Stadt heilt +2 Lebenspunkte pro Runde. Je 3 Land-Karten bringen dir 1 Glaube.',
      flavor='Was im Hain wächst, heilt, und was heilt, bleibt.',
      karten=[('Heiliger Baum', dict(F=1, H=1), 'Man hängt ihm Bänder um und Sorgen ab.'), ('Steinkreis', dict(F=2, H=1), 'Die Steine stehen länger als jede Erinnerung.'),
              ('Quellenhalle', dict(F=2, H=2), 'Das Wasser schmeckt nach Moos und nach Frieden.'), ('Urwald-Heiligtum', dict(F=3, H=2, K=1), 'Es gibt keinen Weg hinein, nur Einladungen.'),
              ('Druide', None, 'Er kennt jedes Kraut, aber verrät nur die harmlosen.')]),
 dict(id='gezeiten', name='Gezeitenglaube', farbe='#1f8fbf', rahmen='#136a94', titel='Segen des Meeres', text='Schiffe kosten 1 Gold weniger. Mit Küste bekommst du +1 Einkommen.',
      flavor='Was das Meer gibt, nimmt es wieder – und gibt mehr.',
      karten=[('Gezeitenschrein', dict(F=1, E=1), 'Er steht dort, wo die Flut ihre Linie malt.'), ('Muscheltempel', dict(F=2, G=1), 'Jede Schale, die man findet, wird dem Tempel gebracht.'),
              ('Perlenhalle', dict(F=2, E=2), 'Im Dämmerlicht glänzen die Wände wie das Meer selbst.'), ('Tiefseetempel', dict(F=3, E=2, K=1), 'Man sagt, die Glocke läutet noch unter Wasser.'),
              ('Sturmrufer', None, 'Der Wind gehorcht ihm, wenn er höflich bittet.')]),
 dict(id='berggeister', name='Berggeister', farbe='#7a6a58', rahmen='#54483a', titel='Felsenfest', text='Deine Stadt hat +2 Schutz. Der erste Missionar bei dir kostet dich keinen Glauben.',
      flavor='Berge vergessen nichts, deshalb fürchten wir sie.',
      karten=[('Felsaltar', dict(F=2, S=1), 'Ein einzelner Fels, glatt vom Streicheln der Pilger.'), ('Bergtempel', dict(F=2, S=1), 'In den Fels gehauen, damit er nicht fortgetragen wird.'),
              ('Halle der Gipfel', dict(F=2, S=2), 'Ihre Mauern sind dicker als jeder Zweifel.'), ('Himmelsberg', dict(F=3, S=2, K=1), 'Wolken umkreisen ihn wie Gläubige.'),
              ('Bergwächter', None, 'Er steht so still, dass der Berg ihn fast vergisst.')]),
 dict(id='flammenorden', name='Flammenorden', farbe='#d8432b', rahmen='#a02a14', titel='Heiliger Zorn', text='Deine Einheiten mit Ansturm erhalten +1 Stärke zusätzlich. Missionare bei dir auszuweisen kostet dich nur 1 Gold.',
      flavor='Aus der Glut wächst der Mut – und die Entschlossenheit.',
      karten=[('Feuerschale', dict(F=1, A=1), 'Sie brennt, solange jemand glaubt.'), ('Flammentempel', dict(F=2, A=1), 'Die Hitze am Tor prüft die Gesinnung.'),
              ('Halle der Glut', dict(F=2, A=1, S=1), 'Ein ewiges Feuer, von vielen Händen genährt.'), ('Ewige Flamme', dict(F=3, A=1, K=1), 'Sie wurde nie gelöscht und nie gestohlen.'),
              ('Flammenprediger', None, 'Seine Rede wärmt, aber man sollte nicht zu nah stehen.')]),
 dict(id='sternenorakel', name='Sternenorakel', farbe='#7b3fb5', rahmen='#552b85', titel='Himmelszeichen', text='Der Aufstieg ins nächste Zeitalter kostet 1 Gold weniger.',
      flavor='Alles, was geschieht, wurde vorher geschrieben – und manchmal gelesen.',
      karten=[('Orakelstein', dict(F=1, W=1), 'Er schweigt, bis die Sterne antworten.'), ('Sternentempel', dict(F=2, W=1), 'Das Dach hat ein Loch, damit der Himmel hineinsehen kann.'),
              ('Halle der Konstellationen', dict(F=2, Z=1), 'Auf dem Boden liegen die Sterne, wie sie fielen.'), ('Himmelsobservatorium', dict(F=3, W=2, K=1), 'Ihr Fernrohr zeigt zuerst, was kommt.'),
              ('Orakel', None, 'Sie antwortet knapp, aber nie falsch.')]),
 dict(id='windwanderer', name='Windwanderer', farbe='#4fb3a9', rahmen='#2f857c', titel='Pilgerwinde', text='Deine Missionare kosten 1 Gold weniger.',
      flavor='Wer wandert, hört den Wind – und der Wind kennt alle Wege.',
      karten=[('Windfahne', dict(F=1, E=1), 'Sie zeigt nicht, woher der Wind kommt, sondern wohin.'), ('Windpavillon', dict(F=2, HL=1), 'Sieben Seiten offen, damit nichts ausgesperrt bleibt.'),
              ('Karawanenschrein', dict(F=2, E=2), 'Wer hier rastet, zahlt mit einer Geschichte.'), ('Zelt der tausend Winde', dict(F=3, E=2, K=1), 'Es steht nirgends, und man findet es trotzdem.'),
              ('Windpilger', None, 'Er geht, und wo er geht, bleibt etwas zurück.')]),
]
PROPHET = {'sonnenkult': dict(staerke=2, schl=['heilen'], einkommen=0, ziehen=0), 'mondgilde': dict(staerke=2, schl=[], einkommen=0, ziehen=1),
           'hain': dict(staerke=2, schl=['heilen'], einkommen=0, ziehen=0), 'gezeiten': dict(staerke=4, schl=[], einkommen=0, ziehen=0),
           'berggeister': dict(staerke=5, schl=[], einkommen=0, ziehen=0), 'flammenorden': dict(staerke=4, schl=['ansturm'], einkommen=0, ziehen=0),
           'sternenorakel': dict(staerke=1, schl=[], einkommen=0, ziehen=2), 'windwanderer': dict(staerke=2, schl=[], einkommen=1, ziehen=0)}

def baue():
    karten = []; religionen = []
    for r in REL:
        rid = r['id']; k = []
        zs = [0, 1, 3, 4]; kosten = [3, 6, 8, 11]; sorten = ['heiligtum', 'tempel', 'halle', 'staette']
        for i in range(4):
            n, e, fl = r['karten'][i]
            k.append(dict(typ='gebaeude', id='%s_%s' % (rid, sorten[i]), name=n, zeitalter=zs[i], kosten=kosten[i], effekte=e, prov=[], braucht=[], benoetigt=[], kategorie='religion', sprite='rel:%s:%s' % (rid, sorten[i]), flavor=fl, sorte=sorten[i]))
        pn, _, pfl = r['karten'][4]; P = PROPHET[rid]
        k.append(dict(typ='einheit', id='%s_prophet' % rid, name=pn, zeitalter=2, kosten=6, staerke=P['staerke'], fern=0, klasse='nahkampf', tags=[], schluessel=P['schl'], boni={}, braucht=[],
                      einkommen=P['einkommen'], ziehen=P['ziehen'], glaube=1, sprite='rel:%s:prophet' % rid, flavor=pfl, sorte='prophet'))
        for j in range(2):
            k.append(dict(typ='einheit', id='%s_missionar%d' % (rid, j + 1), name='Missionar', zeitalter=1, kosten=3, staerke=0, fern=0, klasse='missionar', tags=[], schluessel=['mission'], boni={}, braucht=[],
                          einkommen=0, ziehen=0, glaube=0, sprite='rel:%s:missionar' % rid, flavor='Mit leichtem Gepäck und schwerem Glauben.', sorte='missionar'))
        for c in k:
            c.update(religion=rid, rahmen=r['rahmen'], farbe_rel=r['farbe'], rel_name=r['name'], stapel=0, kopien=1, beschreibung=c['flavor'], relkarte=True)
            c['nr'] = '%s-%s' % (rid[:2].upper(), {'heiligtum': 'H', 'tempel': 'T', 'halle': 'P', 'staette': 'S', 'prophet': 'R', 'missionar': 'M'}[c['sorte']] + ('2' if c['id'].endswith('2') else ''))
        karten += k
        religionen.append({a: b for a, b in r.items() if a != 'karten'} | dict(emblem=EMBLEM[rid]))
    return religionen, karten

EREIGNISSE = [
 dict(id='pilgerzug', name='Pilgerzug', text='Wer eine Religion hat, bekommt 1 Gold je 3 Glaube (mindestens 1).', flavor='Hunderte Füße, ein Ziel.'),
 dict(id='prophezeiung', name='Prophezeiung', text='Wer den meisten Glauben hat (nicht bei Gleichstand), zieht 2 Karten.', flavor='Es steht geschrieben, und jemand hat es gelesen.'),
 dict(id='ketzerjagd', name='Ketzerjagd', text='Alle Missionen enden: Jeder Missionar geht zurück auf die Hand seines Besitzers.', flavor='Plötzlich will niemand mehr fremde Götter sehen.'),
 dict(id='fest', name='Heiliges Fest', text='Wer eine Religion hat, bekommt 2 Gold. Alle anderen ziehen 1 Karte.', flavor='Es gibt Brot für alle, aber Lieder nur für manche.'),
 dict(id='heilung', name='Wundersame Heilung', text='Alle Städte heilen 3 Lebenspunkte.', flavor='Niemand weiß, wer sie gebracht hat.'),
 dict(id='glaubenskrieg', name='Glaubenskrieg', text='Wer den meisten Glauben hat (nicht bei Gleichstand), zahlt 3 Gold.', flavor='Wo Götter streiten, zahlen die Menschen.'),
]
if __name__ == '__main__':
    rel, k = baue(); print(len(rel), len(k))
