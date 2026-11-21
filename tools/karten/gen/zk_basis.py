"""Zeichenwerkzeug im Stil der alten Volk-Sprites (warme Kontur, Kästen mit Tiefe, schattierte Kugeln).
Zweite Fassung der Zukunfts-Grafiken. 'S', 'S+', 'S-' = Spielerfarbe."""
import math, random
from px import Px, mixc
import px as _px
def hell(c, t=.3):
    if c.startswith('S'): return 'S+' if t < .6 else '#ffffff'
    return _px.hell(c, t)
def dunkel(c, t=.3):
    if c.startswith('S'): return 'S-' if t < .45 else 'S--'
    return _px.dunkel(c, t)

OUT = '#2b2118'
HAUT = '#e8b58a'; HAUT_D = '#c98f63'; HAAR = '#4a3020'

# Metall
M1 = '#eef1f4'; M2 = '#c7cdd6'; M3 = '#949ca9'; M4 = '#636b78'; M5 = '#3d434e'
# KI (Graphit + Cyan)
KG1 = '#7d8796'; KG2 = '#555e6c'; KG3 = '#363c47'; KG4 = '#23272f'; KC = '#38d6ff'; KCH = '#c8f6ff'; KB = '#3f7bff'
# Fusion (Keramik + Orange)
FW1 = '#fbf6ea'; FW2 = '#e2d9c6'; FW3 = '#b4a88f'; FW4 = '#7d725d'; FO = '#ff9a2e'; FOH = '#ffd166'; FOW = '#fff4cc'; FR = '#e0502e'
# Weltraum (Weiß-Silber + Violett)
WW1 = '#f6f4fb'; WW2 = '#d3cfe0'; WW3 = '#a19cb8'; WW4 = '#6c6787'; WV = '#8e7cc3'; WVH = '#c3b6ee'; WVD = '#5b4c95'; WF = '#ff8a2a'; WFH = '#ffd23f'
# Sterne (Kristall + Perlmutt + Gold)
SK1 = '#e8fbff'; SK2 = '#9eeeff'; SK3 = '#4cc3e6'; SK4 = '#2a7fa8'; SP1 = '#fbf8ff'; SP2 = '#ddd6ee'; SP3 = '#aea4c8'; SGO = '#ffd36b'; SGOD = '#c9962b'
GRAS = '#5ab84a'; GRAS_D = '#3a8a34'; ERDE = '#8a6a44'; WASSER = '#3f8fd8'; WASSER_H = '#8cc8f5'; WASSER_D = '#2a63a8'


class Bild(Px):
    def kasten(s, x, yb, w, h, d, f, seite=None, dach=None, kante=True):
        """Kasten mit Tiefe nach rechts oben: Front (x..x+w-1, yb-h+1..yb), Seite rechts, Dach oben."""
        seite = seite or dunkel(f, .32); dach = dach or hell(f, .3)
        s.rect(x, yb - h + 1, x + w - 1, yb, f)
        for k in range(1, d + 1):
            s.rect(x + w - 1 + k, yb - h + 1 - k, x + w - 1 + k, yb - k, seite)
            s.rect(x + k, yb - h + 1 - k, x + w - 2 + k, yb - h + 1 - k, dach)
        if kante: s.rect(x, yb - h + 1, x + w - 1, yb - h + 1, hell(f, .12))
        return (x, yb - h + 1, x + w - 1, yb)

    def fenster(s, x0, y0, x1, y1, dx, dy, glas, licht=None, rahmen=None, rnd=None):
        for y in range(y0, y1 + 1, dy):
            for x in range(x0, x1 + 1, dx):
                c = glas
                if licht and rnd is not None and rnd.random() < .3: c = licht
                s.set(x, y, c)
                if rahmen: s.set(x, y + 1, rahmen)

    def seitenfenster(s, x, yb, w, h, d, glas, ab=2):
        """Fensterreihen auf der Seitenfläche eines Kastens."""
        for k in range(2, d + 1, 2):
            for y in range(yb - h + 1 - k + ab, yb - k - 1, 2): s.set(x + w - 1 + k, y, glas)

    def kugel(s, cx, cy, rx, ry, f, licht=None, schatten=None, glanz=True, nur_oben=False):
        licht = licht or hell(f, .35); schatten = schatten or dunkel(f, .28)
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            if nur_oben and y > cy: continue
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                u = (x - cx) / max(rx, .5); v = (y - cy) / max(ry, .5)
                if u * u + v * v > 1.02: continue
                t = u * .7 + v * .7
                c = licht if t < -.55 else schatten if t > .38 else f
                s.set(x, y, c)
        if glanz:
            s.set(round(cx - rx * .45), round(cy - ry * .5), hell(f, .75))
            if rx > 3: s.set(round(cx - rx * .45) + 1, round(cy - ry * .5), hell(f, .6))

    def platte(s, x0, y0, x1, y1, f, oben=True, unten=True):
        s.rect(x0, y0, x1, y1, f)
        if oben: s.rect(x0, y0, x1, y0, hell(f, .3))
        if unten and y1 > y0: s.rect(x0, y1, x1, y1, dunkel(f, .3))

    def ppoly(s, pts, f, licht=None, schatten=None):
        """Polygon mit Licht oben links (oberste Pixelreihe heller, unterste dunkler)."""
        s.poly(pts, f)
        ys = [p[1] for p in pts]; y0, y1 = int(min(ys)), int(max(ys))
        sl = set((x, y) for (x, y), c in s.p.items() if c == f and y0 <= y <= y1)
        for (x, y) in sl:
            if (x, y - 1) not in sl: s.p[(x, y)] = licht or hell(f, .3)
            elif (x, y + 1) not in sl: s.p[(x, y)] = schatten or dunkel(f, .3)

    def kette(s, x0, x1, y0, y1, c='#4a4a4f', rad='#8a8a8f', zahn='#2e2e33'):
        s.rect(x0 + 1, y0, x1 - 1, y1, c); s.rect(x0, y0 + 1, x1, y1 - 1, c)
        for x in range(x0 + 1, x1, 2): s.set(x, y0, zahn); s.set(x, y1, zahn)
        r = (y1 - y0) / 2 - 1
        for x in range(x0 + 2, x1 - 1, max(3, int(r * 2 + 2))):
            s.kugel(x + r, (y0 + y1) / 2, r, r, rad, glanz=False); s.set(round(x + r), round((y0 + y1) / 2), zahn)

    def wasser(s, y=28, x0=0, x1=31):
        s.rect(x0, y, x1, y + 2, WASSER); s.rect(x0, y + 2, x1, y + 2, WASSER_D)
        for x in range(x0 + 1, x1, 4): s.set(x, y, WASSER_H); s.set(x + 1, y, WASSER_H)
        for x in range(x0 + 3, x1, 6): s.set(x, y + 1, WASSER_H)

    def schatten(s, cx, y, rx, c='#3a3226'):
        for x in range(int(cx - rx), int(cx + rx) + 1): s.set(x, y, c)
        for x in range(int(cx - rx + 2), int(cx + rx - 1)): s.set(x, y + 1, c)

    def funkeln(s, x, y, c='#ffe9a8', gross=False):
        s.set(x, y, '#ffffff')
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): s.set(x + dx, y + dy, c)
        if gross:
            for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)): s.set(x + dx, y + dy, c)

    def glut(s, x, y, c, r=1):
        s.set(x, y, '#ffffff')
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if (dx or dy) and abs(dx) + abs(dy) <= r: s.set(x + dx, y + dy, c)

    def flamme(s, x, y, laenge, nach='l', dick=1):
        """Triebwerksflamme ab (x, y) nach links ('l') oder unten ('u')."""
        for i in range(laenge):
            c = '#ffffff' if i == 0 else WFH if i < laenge * .5 else WF
            w = max(0, dick - (i * dick) // laenge)
            if nach == 'l':
                s.rect(x - i, y - w, x - i, y + w, c)
            else:
                s.rect(x - w, y + i, x + w, y + i, c)

    def linie_dunkel(s, pts, c=OUT):
        for (a, b) in zip(pts, pts[1:]): s.line(a[0], a[1], b[0], b[1], c)

    def fertig(s, kontur=True):
        if kontur: s.kontur(OUT)
        return s.sprite()


# ---------------- Figuren ----------------
def figur(m, x=0, ruest=M3, ruest_d=None, helm=M2, visier=KC, hose=None, stiefel=M5, haut=True, waffe=None,
          rucksack=None, schulter=None, guertel='S', brust='S', schritt=0, haare=None):
    """Stehende Figur im Profil nach rechts, Füße auf y 30. x = Verschiebung."""
    ruest_d = ruest_d or dunkel(ruest, .3); hose = hose or ruest_d
    X = lambda v: v + x
    # Beine
    m.rect(X(12), 22, X(14), 28, dunkel(hose, .15)); m.rect(X(16 + schritt), 22, X(18 + schritt), 28, hose)
    m.rect(X(11), 29, X(14), 30, stiefel); m.rect(X(16 + schritt), 29, X(19 + schritt), 30, stiefel)
    m.set(X(16 + schritt), 24, hell(hose, .25)); m.set(X(16 + schritt), 25, hell(hose, .25))
    # Rumpf
    if rucksack: m.platte(X(8), 13, X(10), 21, rucksack)
    m.rect(X(11), 13, X(19), 21, ruest); m.rect(X(11), 13, X(19), 13, hell(ruest, .3)); m.rect(X(11), 13, X(11), 21, hell(ruest, .15))
    m.rect(X(18), 14, X(19), 21, ruest_d)
    if brust: m.rect(X(13), 15, X(16), 17, brust); m.rect(X(13), 15, X(16), 15, 'S+' if brust == 'S' else hell(brust, .3))
    if guertel: m.rect(X(11), 21, X(19), 21, guertel if guertel != 'S' else 'S-')
    if schulter: m.kugel(X(16), 14, 2.6, 1.8, schulter, glanz=False)
    # Kopf
    if haut:
        m.rect(X(14), 9, X(18), 12, HAUT); m.rect(X(14), 12, X(18), 12, HAUT_D); m.set(X(17), 10, OUT)
        m.kugel(X(15.5), 7.5, 4, 3.3, helm, glanz=True); m.rect(X(12), 8, X(14), 11, helm)
        if visier: m.rect(X(16), 8, X(19), 8, visier); m.set(X(19), 8, hell(visier, .5))
    else:
        m.kugel(X(15.5), 8.5, 4, 4, helm)
        if visier: m.rect(X(16), 8, X(19), 10, visier); m.rect(X(16), 8, X(19), 8, hell(visier, .5))
    # Arm vorn
    m.rect(X(15), 15, X(17), 18, ruest); m.rect(X(17), 18, X(20), 19, ruest_d); m.rect(X(20), 18, X(21), 19, HAUT if haut else ruest_d)
    if waffe: waffe(m, x)


def gewehr(lauf=M5, akzent=KC, lang=8, dick=1, kolben=None):
    def f(m, x):
        y = 17
        m.rect(13 + x, y, 21 + x + lang, y + dick, lauf); m.rect(13 + x, y, 21 + x + lang, y, hell(lauf, .25))
        m.rect(12 + x, y, 14 + x, y + 2, kolben or dunkel(lauf, .2)); m.rect(19 + x, y + dick + 1, 20 + x, y + dick + 3, dunkel(lauf, .2))
        if akzent:
            m.rect(16 + x, y + 1, 18 + x, y + 1, akzent); m.set(22 + x + lang, y, akzent); m.set(23 + x + lang, y, hell(akzent, .5))
    return f


def sterne(m, n, seed, c='#ffffff', rand=1):
    r = random.Random(seed)
    for _ in range(n): m.set(r.randrange(rand, m.w - rand), r.randrange(rand, m.h // 2), c)
