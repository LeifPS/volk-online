"""Selbst gezeichnete Pixel-Sprites für die Religions-Erweiterung (Tempel, Gläubige, Symbole).
Werden als 'rel:…' in spr._S eingetragen; 'S', 'S-', 'S+', 'S--' = Religionsfarbe."""
import spr

OUT = '#2b2118'; STEIN = '#d9cfba'; STEIN2 = '#b9ac92'; STEIN3 = '#8c7f68'; GOLD = '#f2c14e'; GOLD2 = '#c9962b'; HOLZ = '#8a5a2b'; HOLZ2 = '#6b4420'
WEISS = '#fbf7ec'; HAUT = '#e8b890'; WASSER = '#5aa9e6'; WASSER2 = '#2f78b5'; GRUEN = '#4f9a4a'; GRUEN2 = '#2f6b33'; FEUER = '#ff8a1f'; FEUER2 = '#ffd23f'

class Mal:
    def __init__(s, w, h): s.w = w; s.h = h; s.p = {}
    def set(s, x, y, c):
        x = int(x); y = int(y)
        if 0 <= x < s.w and 0 <= y < s.h: s.p[(x, y)] = c
    def rect(s, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1): s.set(x, y, c)
    def disc(s, cx, cy, r, c):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + .3: s.set(x, y, c)
    def tri(s, cx, ytop, ybot, halb, c):          # Dreieck, Spitze oben
        n = ybot - ytop
        for y in range(ytop, ybot + 1):
            w = halb * (y - ytop) / max(1, n)
            for x in range(int(round(cx - w)), int(round(cx + w)) + 1): s.set(x, y, c)
    def kontur(s, c=OUT):
        neu = {}
        for (x, y) in list(s.p):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, y + dy)
                if q not in s.p and 0 <= q[0] < s.w and 0 <= q[1] < s.h: neu[q] = c
        s.p.update(neu)
    def sprite(s):
        feld = [None] * (s.w * s.h)
        for (x, y), c in s.p.items(): feld[y * s.w + x] = c
        return dict(w=s.w, h=s.h, feld=feld)

def emblem_zeichnen(m, name, cx, cy, r, hell='S+', mitte='S', dunkel='S-'):
    """Religionssymbole; (cx, cy) = Mitte, r = Radius in Pixeln."""
    if name == 'sonne':
        for k in range(8):
            import math
            a = k * math.pi / 4
            for t in range(int(r * .65), int(r * 1.05) + 1): m.set(cx + math.cos(a) * t, cy + math.sin(a) * t, GOLD2)
        m.disc(cx, cy, r * .55, GOLD); m.set(cx - 1, cy - 1, FEUER2)
    elif name == 'mond':
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + .3 and (x - (cx + r * .55)) ** 2 + (y - (cy - r * .25)) ** 2 > (r * .85) ** 2: m.set(x, y, WEISS)
    elif name == 'baum':
        m.rect(cx - 1, cy + 1, cx, cy + r, HOLZ)
        m.disc(cx - .5, cy - r * .3, r * .75, GRUEN); m.disc(cx - .5 - r * .35, cy, r * .45, GRUEN2); m.disc(cx - .5 + r * .35, cy, r * .45, GRUEN2)
    elif name == 'welle':
        for i, y in enumerate((cy - r * .5, cy, cy + r * .5)):
            for x in range(int(cx - r), int(cx + r) + 1):
                import math
                m.set(x, y + round(math.sin((x - cx) * .9 + i) * 1.2), WASSER if i != 1 else WASSER2)
                m.set(x, y + 1 + round(math.sin((x - cx) * .9 + i) * 1.2), WASSER2 if i != 1 else WASSER)
    elif name == 'berg':
        m.tri(cx, int(cy - r), int(cy + r * .8), r, STEIN3); m.tri(cx + r * .3, int(cy - r * .1), int(cy + r * .8), r * .6, STEIN2)
        m.tri(cx - r * .1, int(cy - r), int(cy - r * .5), r * .3, WEISS)
    elif name == 'flamme':
        m.disc(cx, cy + r * .3, r * .7, FEUER); m.tri(cx, int(cy - r), int(cy + r * .2), r * .6, FEUER)
        m.disc(cx, cy + r * .4, r * .38, FEUER2); m.tri(cx, int(cy - r * .2), int(cy + r * .3), r * .3, FEUER2)
    elif name == 'stern':
        import math
        pts = []
        for k in range(10):
            rr = r if k % 2 == 0 else r * .45; a = -math.pi / 2 + k * math.pi / 5
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                inside = False; j = len(pts) - 1
                for i in range(len(pts)):
                    xi, yi = pts[i]; xj, yj = pts[j]
                    if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi): inside = not inside
                    j = i
                if inside: m.set(x, y, GOLD)
        m.disc(cx, cy, r * .25, FEUER2)
    elif name == 'wind':
        import math
        for k in range(3):
            y0 = cy - r * .6 + k * r * .6
            for t in range(int(r * 2)):
                x = cx - r + t; m.set(x, y0 + round(math.sin(t * .6 + k) * 1.1), WEISS if k != 1 else '#cfe8ff')
            m.disc(cx + r * .9, y0 + 1, 1.2, WEISS)
    elif name == 'flamme_glaube':
        emblem_zeichnen(m, 'flamme', cx, cy, r)

def symbol(name, groesse=16, rahmen=True, kreis='S'):
    m = Mal(groesse, groesse)
    if rahmen:
        m.disc(groesse / 2 - .5, groesse / 2 - .5, groesse / 2 - 1.2, kreis)
        m.kontur()
    emblem_zeichnen(m, name, groesse / 2 - .5, groesse / 2 - .5, groesse * (.28 if rahmen else .4))
    if not rahmen: m.kontur()
    return m.sprite()

# ---------------- Gebäude ----------------
STILE = {'sonnenkult': 'ziggurat', 'mondgilde': 'kuppel', 'hain': 'steine', 'gezeiten': 'welle', 'berggeister': 'berg', 'flammenorden': 'flamme', 'sternenorakel': 'stern', 'windwanderer': 'zelt'}
EMBLEM = {'sonnenkult': 'sonne', 'mondgilde': 'mond', 'hain': 'baum', 'gezeiten': 'welle', 'berggeister': 'berg', 'flammenorden': 'flamme', 'sternenorakel': 'stern', 'windwanderer': 'wind'}

def sockel(m, cx, y, halb, stufen):
    for i in range(stufen):
        w = halb - i * 2; yy = y - i * 2
        m.rect(cx - w, yy - 1, cx + w, yy, STEIN if i % 2 == 0 else STEIN2)
    return y - stufen * 2

def saeulen(m, x0, x1, y0, y1, abstand=4):
    for x in range(x0, x1 + 1, abstand): m.rect(x, y0, x, y1, WEISS); m.set(x, y0, STEIN2)

def gebaeude(rel, stufe):
    """stufe 0 = Heiligtum, 1 = Tempel, 2 = Pilgerhalle, 3 = Heilige Stätte"""
    W, H = 44, 40; m = Mal(W, H); cx = W // 2; stil = STILE[rel]
    gr = [6, 9, 15, 13][stufe]; hoch = [7, 11, 9, 15][stufe]
    y = H - 2
    st = [1, 2, 1, 3][stufe]
    y = sockel(m, cx, y, gr + 3, st)
    if stil == 'ziggurat':
        n = [2, 3, 3, 5][stufe]; yy = y
        for i in range(n):
            w = gr - i * (gr // max(1, n)) ; h = 3 if stufe < 3 else 4
            m.rect(cx - w, yy - h, cx + w, yy - 1, 'S' if i % 2 == 0 else 'S+'); m.rect(cx - w, yy - 1, cx + w, yy - 1, 'S-')
            yy -= h
        m.rect(cx - 1, yy - 3, cx + 1, yy - 1, STEIN)
        emblem_zeichnen(m, 'sonne', cx, yy - 6, 3 + stufe)
    elif stil == 'kuppel':
        m.rect(cx - gr, y - hoch, cx + gr, y - 1, WEISS); m.rect(cx + gr - 1, y - hoch, cx + gr, y - 1, STEIN2)
        saeulen(m, cx - gr + 1, cx + gr - 1, y - hoch + 1, y - 2, 4)
        r = gr + 1; cy = y - hoch
        for yy in range(cy - r, cy + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r + 1: m.set(xx, yy, 'S+' if xx < cx - r // 3 else ('S-' if xx > cx + r // 2 else 'S'))
        emblem_zeichnen(m, 'mond', cx, cy - r - 3, 3)
        if stufe >= 2:
            for dx in (-gr - 3, gr + 3): m.rect(cx + dx - 2, y - hoch + 1, cx + dx + 2, y - 1, WEISS); m.tri(cx + dx, y - hoch - 5, y - hoch, 3, 'S')
    elif stil == 'steine':
        import random
        rnd = random.Random(stufe * 7 + 3)
        n = [3, 5, 7, 9][stufe]
        for i in range(n):
            x = cx - gr + int((2 * gr) * i / max(1, n - 1)); h = rnd.randint(7, 12) + stufe
            m.rect(x - 1, y - h, x + 1, y - 1, STEIN3 if i % 2 else STEIN2); m.rect(x - 1, y - h, x - 1, y - 1, STEIN)
        if stufe >= 1: m.rect(cx - gr + 2, y - 15 - stufe, cx + gr - 2, y - 13 - stufe, STEIN3)
        emblem_zeichnen(m, 'baum', cx, y - 7, 5 + stufe)
    elif stil == 'welle':
        m.rect(cx - gr, y - hoch, cx + gr, y - 1, 'S+'); saeulen(m, cx - gr + 1, cx + gr - 1, y - hoch + 1, y - 2, 3)
        for i in range(2 + (stufe > 1)):
            yy = y - hoch - i * 4; w = gr + 4 - i * 3
            m.rect(cx - w, yy - 3, cx + w, yy, 'S' if i % 2 == 0 else 'S-')
            for k in (cx - w, cx + w): m.set(k, yy + 1, 'S-')
        for x in range(cx - gr - 2, cx + gr + 3): m.set(x, y, WASSER if x % 4 < 2 else WASSER2)
        emblem_zeichnen(m, 'welle', cx, y - hoch - 12 - (stufe > 1) * 3, 3)
    elif stil == 'berg':
        h = [11, 15, 16, 24][stufe]; w = gr + 3
        m.tri(cx, y - h, y - 1, w, STEIN3)
        m.tri(cx + 2, y - h + 3, y - 1, w - 3, STEIN2)
        m.tri(cx, y - h, y - h + 5, 4, WEISS)
        m.rect(cx - 2, y - 7, cx + 2, y - 1, OUT); m.rect(cx - 1, y - 6, cx + 1, y - 1, 'S')
        m.rect(cx, y - h - 5, cx, y - h, HOLZ); m.rect(cx + 1, y - h - 5, cx + 4, y - h - 3, 'S')
    elif stil == 'flamme':
        h = [9, 14, 12, 22][stufe]; w = [3, 4, 9, 5][stufe]
        for yy in range(y - h, y):
            ww = w + (yy - (y - h)) // 5
            m.rect(cx - ww, yy, cx + ww, yy, 'S' if (yy % 4) else 'S-'); m.set(cx - ww, yy, 'S+')
        m.rect(cx - w - 2, y - h - 2, cx + w + 2, y - h, STEIN3)
        emblem_zeichnen(m, 'flamme', cx, y - h - 6, 4 + (stufe > 2))
        if stufe == 2:
            for dx in (-gr + 2, gr - 2): m.rect(cx + dx - 1, y - 8, cx + dx + 1, y - 1, 'S'); emblem_zeichnen(m, 'flamme', cx + dx, y - 11, 2)
    elif stil == 'stern':
        r = gr + 1; cy = y - hoch
        m.rect(cx - gr, cy, cx + gr, y - 1, STEIN); m.rect(cx + gr - 1, cy, cx + gr, y - 1, STEIN2)
        for yy in range(cy - r, cy + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r + 1: m.set(xx, yy, 'S' if abs(xx - cx) > 1 else OUT)
        m.rect(cx - 1, cy - r + 1, cx, cy - 2, STEIN2) if False else None
        for k in range(1, r, 3): m.set(cx - r + k, cy - 2, 'S+')
        emblem_zeichnen(m, 'stern', cx, cy - r - 4, 3 + (stufe > 1))
        for dx in range(-gr + 2, gr - 1, 5): m.rect(cx + dx, cy + 2, cx + dx + 1, cy + 4, WASSER)
    elif stil == 'zelt':
        h = [9, 13, 10, 18][stufe]; w = gr + 3
        m.tri(cx, y - h - 3, y - 2, w, 'S'); m.tri(cx + 2, y - h - 1, y - 2, w - 3, 'S+')
        for k in range(cx - w, cx + w + 1, 3): m.set(k, y - 1, 'S-')
        m.rect(cx - 2, y - 7, cx + 2, y - 1, OUT)
        m.rect(cx, y - h - 8, cx, y - h - 3, HOLZ2); m.rect(cx + 1, y - h - 8, cx + 6, y - h - 6, WEISS)
        if stufe >= 2:
            for dx in (-w - 1, w + 1): m.rect(cx + dx, y - 12, cx + dx, y - 1, HOLZ2); m.rect(cx + dx + (1 if dx < 0 else -4), y - 12, cx + dx + (4 if dx < 0 else 0), y - 10, 'S+')
    m.kontur()
    return m.sprite()

def figur(rel, art):
    """art 'missionar' (Wanderer mit Stab und Bündel) oder 'prophet' (Gewand, Heiligenschein, Buch)"""
    W, H = 28, 36; m = Mal(W, H); cx = 13
    if art == 'prophet': m.disc(cx, 6, 6.5, GOLD); m.disc(cx, 6, 4.6, 'S+'); 
    m.rect(cx - 5, 16, cx + 5, 33, 'S'); m.rect(cx - 5, 16, cx - 4, 33, 'S+'); m.rect(cx + 4, 16, cx + 5, 33, 'S-')
    m.tri(cx, 14, 20, 6, 'S'); m.rect(cx - 5, 31, cx + 5, 33, 'S--')
    m.disc(cx, 10, 4.2, 'S-'); m.disc(cx, 11, 2.7, HAUT); m.set(cx - 1, 11, OUT); m.set(cx + 1, 11, OUT)
    m.rect(cx - 5, 22, cx + 5, 23, 'S--')
    if art == 'missionar':
        m.rect(cx + 7, 4, cx + 7, 34, HOLZ); m.rect(cx + 8, 4, cx + 11, 7, 'S+'); m.set(cx + 8, 4, WEISS)
        m.rect(cx - 10, 20, cx - 6, 26, HOLZ2); m.rect(cx - 10, 20, cx - 6, 21, HOLZ)
        m.rect(cx + 5, 20, cx + 7, 22, HAUT)
    else:
        m.rect(cx - 9, 20, cx - 4, 26, WEISS); m.rect(cx - 9, 20, cx - 9, 26, GOLD2); m.rect(cx - 7, 22, cx - 5, 22, STEIN3); m.rect(cx - 7, 24, cx - 5, 24, STEIN3)
        m.rect(cx + 5, 19, cx + 8, 21, HAUT)
        emblem_zeichnen(m, EMBLEM[rel], cx + 1, 27, 2.6)
    m.kontur()
    return m.sprite()

def strahlenkranz(n):
    """Glaubenssymbol: weißer Ring mit Strahlen, blaue Mitte (Variante 3)."""
    import math
    m = Mal(n, n); cx = cy = n / 2 - .5; BL = '#5aa0e6'; WS = '#f4f6fb'
    ra, ri, rm, strahl = (4.6, 3.0, 1.4, (5.7, 6.6)) if n == 16 else (6.2, 4.2, 1.9, (7.3, 8.0, 8.7, 9.4))
    for y in range(n):
        for x in range(n):
            d = math.hypot(x - cx, y - cy)
            if ri <= d <= ra: m.set(x, y, WS)
            elif d < ri: m.set(x, y, BL if d > rm else WS)
    for a in range(8):
        ang = a * math.pi / 4
        for r in strahl:
            px, py = round(cx + math.cos(ang) * r), round(cy + math.sin(ang) * r)
            m.set(px, py, WS)
            if a % 2 == 1 and n > 16: m.set(px + (1 if math.cos(ang) < 0 else -1), py, WS)   # Diagonalen verbinden
    m.kontur('#1a1a24')
    return m.sprite()

def lade():
    for rel in STILE:
        for st, n in enumerate(('heiligtum', 'tempel', 'halle', 'staette')): spr._S['rel:%s:%s' % (rel, n)] = gebaeude(rel, st)
        for a in ('missionar', 'prophet'): spr._S['rel:%s:%s' % (rel, a)] = figur(rel, a)
        spr._S['rel:%s:symbol' % rel] = symbol(EMBLEM[rel], 16)
        spr._S['rel:%s:emblem' % rel] = symbol(EMBLEM[rel], 24, rahmen=False)
    spr._S['rel:glaube'] = strahlenkranz(16)
    spr._S['rel:glaube_gross'] = strahlenkranz(24)
    spr._S['rel:mission'] = symbol('wind', 16, kreis='#2f857c')
lade()
