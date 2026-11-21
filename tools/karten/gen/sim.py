"""Simulation von "Volk – Das Kartenspiel": prüft mit einfachen Computer-Spielern, dass die Regeln aufgehen
(Spiele enden, Zeitalter-Aufstieg lohnt sich, beide Siegwege kommen vor, keine Sackgassen)."""
import json, os, random, sys, copy, statistics
from collections import Counter
HIER = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HIER, '..', 'kartensatz.json')))
R = S['regeln']
TUNE = {}

def kopiere(k): return dict(k)
class Spieler:
    def __init__(s, name, volk, rng):
        s.name = name; s.volk = volk; s.rng = rng
        s.hand = []; s.land = []; s.geb = []; s.wunder = []; s.staaten = []
        s.front = []; s.kaserne = []; s.gold = R['start_gold']; s.hp = R['stadt_hp']; s.alter = 0
        s.land_gespielt = 0; s.ablegen_n = 0; s.tot = False
        s.religion = None; s.rel_stapel = []; s.mis_aus = []; s.mis_bei = []; s.rel_runde = 0
    # --- Auswertung der Auslage ---
    def alle_effekte(s):
        e = Counter()
        for k in s.geb + s.wunder + s.staaten:
            for a, b in k.get('effekte', {}).items(): e[a] += b
        if s.religion == 'mondgilde': e['HL'] += 2
        elif s.religion == 'hain': e['H'] += 2
        elif s.religion == 'berggeister': e['S'] += 2
        elif s.religion == 'sternenorakel': e['W'] += 1
        return e
    def glaube(s):
        if not s.religion: return 0
        g = 1 + s.alle_effekte()['F'] + sum(u.get('glaube', 0) for u in s.einheiten())
        g += len(s.mis_aus) * s.opt.get('wind_mis', 1) if False else len(s.mis_aus)
        g -= max(0, len(s.mis_bei) - (1 if s.religion == 'berggeister' and not TUNE.get('berg_normal') else 0))
        if s.religion == 'hain' and not TUNE.get('hain_normal'): g += len(s.land) // 3
        return max(0, g)
    def symbole(s):
        sym = Counter()
        for l in s.land:
            for x in l['symbole']: sym[x] += 1
        for k in s.geb + s.wunder + s.staaten:
            for x in k.get('prov', []): sym[x] += 1
        for u in s.front + s.kaserne:
            if 'traeger' in u['schluessel']: sym['flug'] += 1
        if s.volk == 'nordleute': sym['kueste'] += 1
        if s.volk == 'steppenreiter' and TUNE.get('step') == 'pferde': sym['pferde'] += 1
        return sym
    def einheiten(s): return s.front + s.kaserne
    def kampf_einheiten(s): return [u for u in s.einheiten() if u['staerke'] > 0 and u['klasse'] not in ('zivil', 'haendler', 'see_zivil')]
    def kultur(s): return s.alle_effekte()['K']
    def schutz(s): return s.alle_effekte()['S']
    def heilung(s): return s.alle_effekte()['H'] + sum(1 for u in s.einheiten() if 'heilen' in u['schluessel'])
    def einkommen(s):
        e = R['basis_einkommen'] + s.alter + sum(l['ertrag'] for l in s.land) + s.alle_effekte()['E']
        e += sum(u.get('einkommen', 0) + (1 if s.volk == 'goldener_bund' and u.get('einkommen') else 0) for u in s.einheiten())
        if s.volk == 'sonnenvolk' and len(s.land) >= 3: e += 1
        if s.volk == 'steppenreiter' and TUNE.get('step') == 'eink': e += 1
        if s.volk == 'steppenreiter' and TUNE.get('step') == 'eink2' and any('reiter' in u['tags'] for u in s.einheiten()): e += 1
        if s.religion == 'sonnenkult': e += s.glaube() // 3
        if s.religion == 'gezeiten' and s.symbole()['kueste']: e += 1
        return e
    def handlimit(s): return R['handlimit'] + s.alle_effekte()['HL']
    def kosten(s, k):
        c = k['kosten']
        if k['typ'] == 'einheit':
            red = min(3, s.alle_effekte()['A'])
            if k['klasse'] in ('zivil', 'haendler', 'see_zivil', 'spaeher', 'missionar'): red = 0
            c -= red
            if s.volk == 'nordleute' and 'see' in k['tags']: c -= 1
            if s.religion == 'gezeiten' and 'see' in k['tags']: c -= 1
            if s.religion == 'windwanderer' and 'mission' in k['schluessel']: c -= 1
            if s.volk == 'steppenreiter' and 'reiter' in k['tags']: c -= 1
            c = max(1, c)
        elif k['typ'] == 'gebaeude':
            c = max(1, c - s.alle_effekte()['G'])
        return c
    def aufstieg_kosten(s):
        if s.alter >= 6: return None
        c = R['aufstieg'][s.alter] - s.alle_effekte()['W'] - (1 if s.volk == 'sternendeuter' else 0)
        return max(1, c)
    def zukauf(s, k):
        """Kosten für fehlende Rohstoffe (3 Gold je Rohstoff, höchstens 1 pro Karte); None = nicht spielbar (Küste/Flug fehlt, oder 2 Rohstoffe fehlen)."""
        sym = s.symbole(); fehlt = 0
        for b in k.get('braucht', []):
            if sym[b] >= 1: continue
            if b in ('kueste', 'flug'): return None
            fehlt += 1
        return None if fehlt > R['zukauf_max'] else fehlt * R['zukauf_preis']
    def kann_spielen(s, k):
        if k['typ'] in ('einheit', 'gebaeude', 'wunder') and k['zeitalter'] > s.alter: return False
        z = s.zukauf(k)
        if z is None: return False
        if s.gold < (s.kosten(k) if k['typ'] != 'wunder' else k['kosten']) + z: return False
        for b in k.get('benoetigt', []):
            if not any(g['id'] == b for g in s.geb): return False
        if k['typ'] == 'gebaeude' and any(g['id'] == k['id'] for g in s.geb): return False
        if k['typ'] == 'einheit' and 'einmalig' not in k['schluessel'] and False: return False
        return True

class Spiel:
    def __init__(s, n, seed, optionen=None):
        s.rng = random.Random(seed); s.opt = optionen or {}; TUNE.clear(); TUNE.update(s.opt)
        völker = [v['id'] for v in S['voelker']]; s.rng.shuffle(völker)
        s.sp = [Spieler(f'S{i+1}', völker[i], s.rng) for i in range(n)]
        s.stapel = {1: [], 2: [], 3: []}; s.ablage = {1: [], 2: [], 3: []}
        for k in S['karten']:
            for _ in range(k['kopien']): s.stapel[k['stapel']].append(kopiere(k))
        for st in s.stapel.values(): s.rng.shuffle(st)
        s.wunder = [kopiere(w) for w in S['wunder']]
        s.staaten = [kopiere(x) for x in S['staaten']]; s.rng.shuffle(s.staaten)
        s.auslage = [s.staaten.pop() for _ in range(3)]
        s.ereignisse = [kopiere(e) for e in S['ereignisse']]; s.rng.shuffle(s.ereignisse); s.ereig_ablage = []
        s.vk = {} if s.opt.get('ohne_volkskarten') else {}
        for k in S.get('volkskarten', []): s.vk.setdefault(k['volk'], {})[k['zeitalter']] = k
        for p in s.sp:
            for _ in range(R['start_hand']): s.ziehe(p, 1)
            s.volkskarte(p)
        s.rel = bool(s.opt.get('religion')); s.glaube_ziel = s.opt.get('glaube_sieg') or (S.get('glaube_sieg_vk', 12) if not s.opt.get('ohne_volkskarten') else S.get('glaube_sieg', 13))
        if s.rel:
            s.rel_frei = [x['id'] for x in S['religionen']]
            s.relkarten = {}
            for k in S['relkarten']: s.relkarten.setdefault(k['religion'], []).append(k)
            for e in S['rel_ereignisse']: s.ereignisse.append(dict(e, art='rel', plus=0)); 
            s.rng.shuffle(s.ereignisse)
        s.runde = 0; s.sieger = None; s.grund = None; s.log = Counter()
    def ziehe(s, p, st):
        if not s.stapel[st]:
            s.stapel[st] = s.ablage[st]; s.ablage[st] = []; s.rng.shuffle(s.stapel[st])
        if s.stapel[st]: p.hand.append(s.stapel[st].pop()); return True
        return False
    def volkskarte(s, p):
        if s.opt.get('ohne_volkskarten'): return
        k = s.vk.get(p.volk, {}).get(p.alter)
        if k: k = dict(k); k['volk_karte'] = True; p.hand.append(k)
    def lege_ab(s, p, k):
        if k.get('relkarte'): k['tapped'] = False; p.rel_stapel.insert(0, k); return
        if k.get('volk_karte'): k['tapped'] = False; p.hand.append(k); return
        s.ablage[k['stapel']].append(k) if k['stapel'] else None
    def lebende(s): return [p for p in s.sp if not p.tot]

    # ---- Zug ----
    def zug(s, p):
        p.aufgestiegen = False   # pro Runde nur ein Aufstieg
        # Aufwecken
        for u in s.sp[0].front[:0]: pass
        for u in p.front: u['tapped'] = False
        for u in p.kaserne: u['tapped'] = False
        p.front += p.kaserne; p.kaserne = []
        if s.rel and p.mis_bei and (p.gold >= s.opt.get('ausweis_ab', 5) or (p.religion == 'flammenorden' and not s.opt.get('flamme_normal'))):
            for m in list(p.mis_bei):
                if p.religion == 'flammenorden' and not s.opt.get('flamme_normal') and p.gold >= 2: p.gold -= 1; s.mission_ende(m); s.log['ausweisung'] += 1
                elif p.gold >= 3: p.gold -= 2; s.mission_ende(m); s.log['ausweisung'] += 1
        p.hp = min(R['stadt_hp'], p.hp + p.heilung())
        p.gold += p.einkommen()
        # Ziehen
        n = R['ziehen'] + p.alle_effekte()['Z'] + (1 if p.religion == 'mondgilde' and not s.opt.get('mond_normal') else 0)
        hoch = R['stapel_von_zeitalter'][p.alter]
        for i in range(n):
            if s.rel and p.religion and p.rel_stapel and i < s.opt.get('rel_zuege', 1):
                k = p.rel_stapel.pop(); p.hand.append(k); s.log['rel_gezogen'] += 1; continue
            st = hoch
            if hoch > 1 and (len(p.land) < 3 + p.alter or s.rng.random() < .35) and i % 2 == 1: st = hoch - 1
            s.ziehe(p, st)
        p.land_gespielt = 0; p.ablegen_n = 0
        s.bot_aktionen(p)
        if p.tot or s.sieger: return
        # Handlimit
        while len([c for c in p.hand if not c.get('volk_karte')]) > p.handlimit():
            k = min([c for c in p.hand if not c.get('volk_karte')], key=lambda c: s.wert_karte(p, c)); p.hand.remove(k); s.lege_ab(p, k)
        s.pruefe_sieg()

    def mission_ende(s, m):
        m['host'].mis_bei.remove(m); m['owner'].mis_aus.remove(m); k = m['k']; k['tapped'] = False; m['owner'].hand.append(k)
    def gruende(s, p):
        wahl = s.opt.get('rel_wahl')
        rid = s.rng.choice(s.rel_frei) if not wahl else (wahl if wahl in s.rel_frei else s.rng.choice(s.rel_frei))
        s.rel_frei.remove(rid); p.gold -= s.opt.get('gruenden_kosten', 5)
        kand = [c for c in p.hand if not c.get('volk_karte') and not c.get('relkarte')]
        if kand: k = min(kand, key=lambda c: s.wert_karte(p, c)); p.hand.remove(k); s.lege_ab(p, k)
        p.religion = rid; p.rel_stapel = [dict(k) for k in s.relkarten[rid]]; s.rng.shuffle(p.rel_stapel)
        s.log['gegruendet'] += 1; s.log['rel_' + rid] += 1
    def sende(s, p, k):
        ziele = [o for o in s.gegner(p) if sum(1 for m in o.mis_bei if m['owner'] is p) < 1]
        if not ziele: return False
        host = max(ziele, key=lambda o: (o.glaube(), s.rng.random()))
        p.gold -= p.kosten(k); p.hand.remove(k)
        m = dict(owner=p, host=host, k=k); p.mis_aus.append(m); host.mis_bei.append(m); s.log['mission'] += 1
        return True
    def pruefe_sieg(s):
        for p in s.lebende():
            if p.hp <= 0: p.tot = True; s.log['eliminiert'] += 1
        l = s.lebende()
        if len(l) == 1 and not s.sieger: s.sieger = l[0]; s.grund = 'Eroberung'; return
        for p in l:
            if p.kultur() >= R['kultur_sieg'] and not s.sieger: s.sieger = p; s.grund = 'Kultur'; return
            if s.rel and p.religion and p.glaube() >= s.glaube_ziel and not s.sieger: s.sieger = p; s.grund = 'Glaube'; return

    # ---- Bot ----
    def wert_karte(s, p, k):
        if k['typ'] == 'land': return 5 if len(p.land) < 8 else 1
        if k['zeitalter'] > p.alter + 1: return 0.5
        return 2 + (3 if k['typ'] == 'einheit' else 2)
    def bedrohung(s, p):
        return max([sum(1 for u in o.kampf_einheiten()) for o in s.lebende() if o is not p] + [0])
    def gegner(s, p): return [o for o in s.lebende() if o is not p]
    def spiele(s, p, k, ablage_ok=True):
        c = s.kosten_von(p, k) + (p.zukauf(k) or 0)
        p.gold -= c; p.hand.remove(k); s.log['gespielt:' + k['id']] += 1
        if k['typ'] == 'einheit':
            if 'gruenden' in k['schluessel']:
                for _ in range(2):
                    l = [x for x in p.hand if x['typ'] == 'land']
                    if l: s.lege_land(p, s.beste_land(p, l))
                s.lege_ab(p, k); return
            k['tapped'] = False
            p.kaserne.append(k)
            for _ in range(k.get('ziehen', 0)): s.ziehe(p, R['stapel_von_zeitalter'][p.alter])
        elif k['typ'] == 'gebaeude': p.geb.append(k)
        elif k['typ'] == 'wunder': p.wunder.append(k); s.wunder.remove(k); s.log['wunder'] += 1
    def kosten_von(s, p, k): return p.kosten(k) if k['typ'] != 'wunder' else k['kosten']
    def lege_land(s, p, l): p.hand.remove(l); p.land.append(l); p.land_gespielt += 1
    def beste_land(s, p, kandidaten):
        sym = p.symbole(); fehlt = Counter()
        for k in p.hand:
            for b in k.get('braucht', []):
                if sym[b] < 1: fehlt[b] += 1 + (2 if k['typ'] == 'einheit' else 0)
        return max(kandidaten, key=lambda l: sum(fehlt[x] for x in l['symbole']) * 3 + l['ertrag'] + s.rng.random() * .1)
    def land_erlaubt(s, p): return 1 + p.alle_effekte()['L'] + sum(1 for t in p.staaten if t['effekte'].get('L'))
    def gebaeude_wert(s, p, k):
        e = k['effekte']; bed = s.bedrohung(p)
        v = e.get('E', 0) * 3.2 + e.get('K', 0) * 3.2 + e.get('W', 0) * (2.2 if p.alter < 5 else 0.5)
        v += e.get('S', 0) * (1.6 if bed >= 2 else .5) + e.get('H', 0) * (1.2 if p.hp < R['stadt_hp'] else .3)
        v += e.get('F', 0) * s.opt.get('f_wert', 2.8) + min(3, e.get('A', 0)) * 1.0 + e.get('HL', 0) * .6 + (1.5 if k['prov'] else 0) + e.get('G', 0) * 1.5 + e.get('L', 0) * 2.0 + e.get('Z', 0) * 2.2
        return v / max(1, s.kosten_von(p, k))
    def einheit_wert(s, p, k):
        v = k['staerke'] + k['fern'] * .8 + sum(k['boni'].values()) * .5
        if 'fern' in k['schluessel'] or 'belagerung' in k['schluessel']: v += 1.5
        if 'ansturm' in k['schluessel']: v += 1
        if k['einkommen'] or k['ziehen']: v = 1.5 + k['einkommen'] * 2 + k['ziehen']
        if k.get('glaube'): v += k['glaube'] * s.opt.get('f_wert', 2.8)
        if 'gruenden' in k['schluessel']: v = 3 if any(x['typ'] == 'land' for x in p.hand) else 0
        return v / max(1, s.kosten_von(p, k))
    def bot_aktionen(s, p):
        for _ in range(25):
            if s.sieger: return
            gemacht = False
            # 1. Land
            ls = [x for x in p.hand if x['typ'] == 'land']
            if ls and p.land_gespielt < s.land_erlaubt(p):
                s.lege_land(p, s.beste_land(p, ls)); continue
            if s.rel and not p.religion and s.rel_frei and p.alter >= s.opt.get('rel_alter', 1) and p.gold >= s.opt.get('gruenden_kosten', 5) + s.opt.get('rel_reserve', 2) and len(p.hand) >= 2 and s.runde >= s.opt.get('rel_ab_runde', 2):
                s.gruende(p); continue
            if s.rel and p.religion:
                ms = [k for k in p.hand if 'mission' in k.get('schluessel', []) and p.gold >= p.kosten(k) + s.opt.get('mis_reserve', 0)]
                if ms and s.sende(p, ms[0]): continue
            # 2. Wunder
            for w in sorted(s.wunder, key=lambda w: w['kosten']):
                if s.kann_wunder(p, w):
                    # Wunder: Kosten/Nutzen – nur wenn danach nicht pleite oder Kultur-Sieg naht
                    p.gold -= w['kosten'] + (p.zukauf(w) or 0); p.wunder.append(w); s.wunder.remove(w); s.log['wunder'] += 1; gemacht = True; break
            if gemacht: continue
            # 3. Heer
            army = len(p.kampf_einheiten()); wunsch = min(6, max(2 if s.runde >= 2 else 1, s.bedrohung(p) + 1))
            kand = [k for k in p.hand if k['typ'] == 'einheit' and p.kann_spielen(k) and k['klasse'] not in ('zivil', 'haendler', 'see_zivil') and k['staerke'] > 0
                    and 'gruenden' not in k['schluessel']]
            if army < wunsch and kand:
                k = max(kand, key=lambda k: s.einheit_wert(p, k) + k['staerke'] * .15)
                s.spiele(p, k); continue
            # 4. Wirtschaft: Einheiten mit Einkommen/Ziehen, Siedler
            wk = [k for k in p.hand if k['typ'] == 'einheit' and p.kann_spielen(k) and (k['einkommen'] or k['ziehen'] or 'gruenden' in k['schluessel'])]
            wk = [k for k in wk if s.einheit_wert(p, k) >= .6]
            if wk and s.runde <= 18:
                s.spiele(p, max(wk, key=lambda k: s.einheit_wert(p, k))); continue
            # 5. Gebäude
            gk = [k for k in p.hand if k['typ'] == 'gebaeude' and p.kann_spielen(k)]
            gk = [k for k in gk if s.gebaeude_wert(p, k) >= .45]
            if gk:
                s.spiele(p, max(gk, key=lambda k: s.gebaeude_wert(p, k))); continue
            # 6. Aufstieg
            ak = p.aufstieg_kosten()
            if ak is not None and p.gold >= ak and not p.aufgestiegen:
                p.gold -= ak; p.alter += 1; p.aufgestiegen = True; s.log['aufstieg'] += 1; s.volkskarte(p); continue
            # 7. Tribut
            for a in list(s.auslage):
                if p.gold >= a['kosten'] and len(p.staaten) < 2 and s.staat_wert(p, a) >= 1.0:
                    p.gold -= a['kosten']; p.staaten.append(a); s.auslage.remove(a)
                    if s.staaten: s.auslage.append(s.staaten.pop())
                    s.log['tribut'] += 1; gemacht = True; break
            if gemacht: continue
            # 8. weitere Einheiten, wenn Gold übrig
            kand2 = [k for k in p.hand if k['typ'] == 'einheit' and p.kann_spielen(k) and k['staerke'] > 0 and k['klasse'] not in ('zivil', 'haendler', 'see_zivil') and 'gruenden' not in k['schluessel']]
            if kand2 and army < 9 and p.gold >= 3:
                s.spiele(p, max(kand2, key=lambda k: s.einheit_wert(p, k))); continue
            break
        s.kampf(p)
        # Ablegen für Gold
        while p.ablegen_n < R['ablegen_max'] and len(p.hand) > 3:
            toter = [k for k in p.hand if not k.get('volk_karte') and (k['typ'] != 'land' and k['zeitalter'] > p.alter + 1) or (k['typ'] == 'gebaeude' and any(g['id'] == k['id'] for g in p.geb))]
            if not toter: break
            k = toter[0]; p.hand.remove(k); s.lege_ab(p, k); p.gold += (2 if p.volk == 'goldener_bund' else R['ablegen_gold']) + (1 if p.religion == 'mondgilde' else 0); p.ablegen_n += 1
        s.pruefe_sieg()
    def staat_wert(s, p, a):
        e = a['effekte']
        return e.get('E', 0) * 3 + e.get('K', 0) * 3 + e.get('W', 0) * 2 + e.get('S', 0) * .8 + e.get('H', 0) * .6 + e.get('A', 0) * 1 + e.get('L', 0) * 1.5 + e.get('HL', 0) * .3 + (1 if a['prov'] else 0) + e.get('ABLEGEN', 0) * .5 + e.get('SCHIFF', 0) * .3
    def kann_wunder(s, p, w):
        z = p.zukauf(w)
        if w['zeitalter'] > p.alter or z is None or p.gold < w['kosten'] + z + (0 if p.kultur() >= R['kultur_sieg'] - 3 else 2): return False
        if any(not any(g['id'] == b for g in p.geb) for b in w['benoetigt']): return False
        return True

    # ---- Kampf ----
    def staerke_gegen(s, p, u, gegner, angriff):
        st = u['staerke']
        if angriff and 'ansturm' in u['schluessel']: st += (2 if p.volk == 'steppenreiter' else 1) + (1 if p.religion == 'flammenorden' else 0)
        for t in gegner['tags']: st += u['boni'].get(t, 0)
        if 'luftabwehr' in u['schluessel'] and 'luft' in gegner['tags']: st += 3
        return st
    def schluesse(s, p):
        return [u for u in p.front if not u.get('tapped')]
    def kann_blocken(s, b, a):
        if b.get('tapped') or b['staerke'] < 1 or b['klasse'] in ('zivil', 'haendler', 'see_zivil'): return False
        if 'luft' in a['tags'] and not ('luft' in b['tags'] or 'luftabwehr' in b['schluessel']): return False
        return True
    def schaden_stadt(s, o, dmg):
        dmg = max(1, dmg - o.schutz()); o.hp -= dmg; s.log['stadtschaden'] += dmg
    def kampf(s, p):
        if s.sieger or s.runde <= R.get('schutz_runden', 0): return
        gegn = s.gegner(p)
        if not gegn: return
        ziel = min(gegn, key=lambda o: (o.hp - 0.5 * len(o.kampf_einheiten()), s.rng.random()))
        # 1. Schüsse
        for u in [x for x in p.front if not x.get('tapped')]:
            if not ('fern' in u['schluessel'] or 'belagerung' in u['schluessel']) or u['fern'] < 1: continue
            kandidaten = []
            for o in gegn:
                for t in o.kampf_einheiten():
                    if 'tarnung' in t['schluessel']: continue
                    if 'luft' in t['tags'] and not ('luft' in u['tags'] or 'luftabwehr' in u['schluessel']): continue
                    f = u['fern'] + sum(u['boni'].get(g, 0) for g in t['tags'])
                    if f >= t['staerke']: kandidaten.append((t['staerke'] + t['fern'] * .5, o, t))
            stadt_ok = 'belagerung' in u['schluessel']
            if stadt_ok and (not kandidaten or ziel.hp <= u['fern'] + 3 or p.kultur() < 0):
                s.schaden_stadt(ziel, u['fern'] + u['boni'].get('stadt', 0)); u['tapped'] = True; s.log['schuss_stadt'] += 1
                if 'einmalig' in u['schluessel']: p.front.remove(u); s.lege_ab(p, u)
            elif kandidaten:
                _, o, t = max(kandidaten, key=lambda x: x[0])
                (o.front if t in o.front else o.kaserne).remove(t); s.lege_ab(o, t); u['tapped'] = True; s.log['schuss_einheit'] += 1
                if 'einmalig' in u['schluessel']: p.front.remove(u); s.lege_ab(p, u)
        # 2. Nahkampf-Angriffe (alle kampfstarken, nicht-Fernkämpfer bevorzugt)
        bereit = [u for u in p.front if not u.get('tapped') and u['staerke'] > 0 and u['klasse'] not in ('zivil', 'haendler', 'see_zivil')
                  and not ('fern' in u['schluessel'] and u['klasse'] in ('fernkampf', 'see_fern', 'u_boot', 'jaeger'))
                  and not ('belagerung' in u['schluessel'] and u['fern'] > 0) and 'luftabwehr' not in u['schluessel']]
        bereit.sort(key=lambda u: -u['staerke'])
        gegner_block = [b for b in ziel.einheiten() if not b.get('tapped') and b['staerke'] >= 1 and b['klasse'] not in ('zivil', 'haendler', 'see_zivil')]
        maxb = max([b['staerke'] + (2 if 'ansturm' in b['schluessel'] else 0) for b in gegner_block] + [0])
        eigene_bed = max([len(o.kampf_einheiten()) for o in gegn] + [0])
        daheim = max(0, (eigene_bed + 1) // 2 - 0)
        angreifer = []
        for u in bereit:
            if len(bereit) - len(angreifer) <= daheim and gegner_block: break
            vorteil = s.staerke_gegen(p, u, {'tags': []}, True) > maxb
            if not gegner_block or vorteil or ziel.hp <= 6: angreifer.append(u)
        if not angreifer: return
        for u in angreifer: u['tapped'] = True
        verfuegbar = list(gegner_block); s.log['angriffe'] += len(angreifer)
        for a in sorted(angreifer, key=lambda u: -u['staerke']):
            if a not in p.front: continue
            kand = [b for b in verfuegbar if s.kann_blocken(b, a)]
            # Verteidiger wählt: einen Blocker, der gewinnt (oder wenn Stadt in Gefahr, einen Opfer-Blocker)
            gewinner = [b for b in kand if s.staerke_gegen(ziel, b, a, False) > s.staerke_gegen(p, a, b, True)]
            gleich = [b for b in kand if s.staerke_gegen(ziel, b, a, False) == s.staerke_gegen(p, a, b, True)]
            blocker = None
            if gewinner: blocker = min(gewinner, key=lambda b: b['staerke'])
            elif gleich and (a['staerke'] >= 2 or ziel.hp <= 8): blocker = gleich[0]
            elif kand and ziel.hp <= a['staerke'] + 2: blocker = min(kand, key=lambda b: b['staerke'])
            if blocker:
                verfuegbar.remove(blocker)
                sa = s.staerke_gegen(p, a, blocker, True); sb = s.staerke_gegen(ziel, blocker, a, False)
                if sa >= sb: (ziel.front if blocker in ziel.front else ziel.kaserne).remove(blocker); s.lege_ab(ziel, blocker); s.log['einheit_tot'] += 1
                if sb >= sa: p.front.remove(a); s.lege_ab(p, a); s.log['einheit_tot'] += 1
            else:
                d = a['staerke'] + a['boni'].get('stadt', 0) + (a['staerke'] if 'ramme' in a['schluessel'] else 0)
                s.schaden_stadt(ziel, d)
        s.pruefe_sieg()

    # ---- Ereignis ----
    def ereignis(s):
        if not s.ereignisse:
            s.ereignisse = s.ereig_ablage; s.ereig_ablage = []; s.rng.shuffle(s.ereignisse)
        if not s.ereignisse: return
        e = s.ereignisse.pop(); s.ereig_ablage.append(e); l = s.lebende()
        s.log['ereignis_' + e['art']] += 1
        if e['art'] == 'rel':
            i = e['id']; mit = [p for p in l if p.religion]
            if i == 'pilgerzug':
                for p in mit: p.gold += max(1, p.glaube() // 3)
            elif i in ('prophezeiung', 'glaubenskrieg') and mit:
                m = max(p.glaube() for p in mit); t = [p for p in mit if p.glaube() == m]
                if len(t) == 1:
                    if i == 'prophezeiung':
                        for _ in range(2): s.ziehe(t[0], R['stapel_von_zeitalter'][t[0].alter])
                    else: t[0].gold = max(0, t[0].gold - 3)
            elif i == 'ketzerjagd':
                for p in l:
                    for m in list(p.mis_aus): s.mission_ende(m)
            elif i == 'fest':
                for p in l:
                    if p.religion: p.gold += 2
                    else: s.ziehe(p, R['stapel_von_zeitalter'][p.alter])
            elif i == 'heilung':
                for p in l: p.hp = min(R['stadt_hp'], p.hp + 3)
            s.pruefe_sieg(); return
        if e['art'] == 'barbaren':
            m = min(len(p.kampf_einheiten()) for p in l)
            for p in [p for p in l if len(p.kampf_einheiten()) == m]:
                B = p.alter + 1 + e['plus']
                bl = [u for u in p.kampf_einheiten()]
                if bl:
                    gut = [u for u in bl if u['staerke'] >= B]
                    if gut:
                        p.gold += e['beute']; s.log['barb_abgewehrt'] += 1
                    else:
                        u = max(bl, key=lambda u: u['staerke']); (p.front if u in p.front else p.kaserne).remove(u); s.lege_ab(p, u); s.log['barb_opfer'] += 1
                else:
                    if e['folge'] == 'stadt': s.schaden_stadt(p, B)
                    else: p.gold = max(0, p.gold - B)
                    s.log['barb_treffer'] += 1
        else:
            i = e['id']
            if i == 'regenzeit':
                for p in l: p.gold += 2
            elif i == 'winter':
                for p in l:
                    if p.hand: k = min([c for c in p.hand if not c.get('volk_karte')] or p.hand, key=lambda c: s.wert_karte(p, c)); p.hand.remove(k); s.lege_ab(p, k)
            elif i == 'seuche':
                for p in l:
                    if p.heilung() < 2: p.hp -= 2
            elif i == 'sonnenwende':
                m = max(p.kultur() for p in l); t = [p for p in l if p.kultur() == m]
                if len(t) == 1: t[0].gold += 2
            elif i == 'diebe':
                m = max(p.gold for p in l); t = [p for p in l if p.gold == m]
                for p in t: p.gold = max(0, p.gold - 3)
            elif i == 'messe':
                for p in l: s.ziehe(p, R['stapel_von_zeitalter'][p.alter])
        s.pruefe_sieg()

    def spiele_durch(s, max_runden=60):
        while not s.sieger and s.runde < max_runden:
            s.runde += 1
            for p in s.sp:
                if p.tot or s.sieger: continue
                s.zug(p)
            if s.sieger: break
            s.ereignis()
        return s

def lauf(n, spiele, seed0=1, **kw):
    res = []
    for i in range(spiele):
        g = Spiel(n, seed0 + i, kw).spiele_durch()
        res.append(g)
    return res

if __name__ == '__main__':
    for n in (2, 3, 4):
        res = lauf(n, int(sys.argv[1]) if len(sys.argv) > 1 else 200)
        runden = [g.runde for g in res]
        gr = Counter(g.grund or 'KEIN SIEGER' for g in res)
        alter = [max(p.alter for p in g.sp) for g in res]
        print(f'--- {n} Spieler: Runden Median {statistics.median(runden)} (min {min(runden)}, max {max(runden)}), Sieg: {dict(gr)}')
        print('    höchstes Zeitalter bei Ende (Schnitt):', round(statistics.mean(alter), 1), ' Kultur Sieger (Schnitt):', round(statistics.mean([g.sieger.kultur() for g in res if g.sieger and g.grund == 'Kultur'] or [0]), 1))
        log = Counter()
        for g in res: log.update(g.log)
        print('    pro Spiel:', {k: round(v / len(res), 1) for k, v in sorted(log.items())})
        print('    Siege nach Volk:', dict(Counter(g.sieger.volk for g in res if g.sieger)))
