"""Wunder (64x64), Städte (64x56), Rohstoffe (16x16) und Zeitalter-Symbole (16x16) für VIII–XI, zweite Fassung."""
import random
from zk_basis import *

NEU = {}
def motiv(key):
    def deko(fn): NEU[key] = fn; return fn
    return deko


def wiese(m, y=56, c=GRAS, cd=GRAS_D, h=None):
    m.rect(0, y, 63, 63, c); m.rect(0, y, 63, y, hell(c, .3)); m.rect(0, 62, 63, 63, cd)
    for x in range(2, 62, 7): m.set(x, y + 2, cd); m.set(x + 3, y + 4, hell(c, .2))


def baeumchen(m, x, y):
    m.rect(x, y, x, y + 2, ERDE); m.kugel(x, y - 2, 2.2, 2.6, GRAS_D, glanz=False); m.set(x - 1, y - 3, GRAS)


# ============================ Wunder ============================
@motiv('wunder:weltgehirn')
def _(m):
    wiese(m, 57)
    m.kasten(6, 57, 44, 9, 6, M2)                                                                 # Sockel
    m.fenster(8, 51, 48, 55, 3, 4, KC, KCH, None, random.Random(3))
    m.rect(6, 49, 49, 49, 'S')
    m.kasten(14, 47, 28, 9, 4, KG1, seite=KG3, dach=M2); m.fenster(16, 41, 40, 45, 2, 2, KB, KC, None, random.Random(4))
    m.rect(25, 30, 31, 38, KG2); m.rect(30, 30, 31, 38, KG3)                                       # Hals
    m.kugel(28, 18, 15, 14, '#2a3f8c', '#4f78e8', '#1a2658', glanz=False)                           # Glaskugel
    r = random.Random(7); pts = []
    for gy in range(7, 31, 5):
        for gx in range(16, 42, 5):
            x, y = gx + r.uniform(-1.5, 1.5), gy + r.uniform(-1.5, 1.5)
            if ((x - 28) / 12.5) ** 2 + ((y - 18) / 11.5) ** 2 < 1: pts.append((x, y))
    for i, a in enumerate(pts):                                                                    # Neuronennetz
        for b in pts[i + 1:]:
            if (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 < 52: m.line(a[0], a[1], b[0], b[1], '#3a6ad8')
    for (x, y) in pts:
        if r.random() < .55: m.glut(round(x), round(y), KC, 1)
        m.set(x, y, '#ffffff')
    m.set(20, 9, '#ffffff'); m.set(21, 8, '#ffffff'); m.set(19, 11, '#cfe0ff')
    m.line(28, 4, 28, 1, M4); m.set(28, 0, KC)
    for x in (3, 52): baeumchen(m, x + 2, 54)
    m.funkeln(55, 8, KCH, True); m.funkeln(6, 14, KCH)


@motiv('wunder:kuenstliche_sonne')
def _(m):
    wiese(m, 57)
    m.kasten(4, 57, 50, 10, 6, FW2, seite=FW3, dach=FW1)
    m.fenster(6, 50, 52, 54, 4, 4, FOH)
    m.rect(4, 48, 53, 48, 'S')
    for x in (12, 40):                                                                              # Haltemasten
        m.ppoly([(x, 46), (x + 2, 18), (x + 5, 18), (x + 7, 46)], FW1); m.rect(x + 5, 18, x + 7, 46, FW3)
    m.kugel(29, 22, 13, 13, FO, FOH, FR, glanz=False)                                               # Sonne
    m.kugel(26, 19, 7, 7, FOH, FOW, FO, glanz=False); m.kugel(25, 18, 3, 3, FOW, '#ffffff', FOH, glanz=False)
    for a in range(0, 360, 20):
        x = 29 + 17 * math.cos(math.radians(a)); y = 22 + 17 * math.sin(math.radians(a))
        if y < 40: m.set(x, y, FOH); m.set(29 + 18.5 * math.cos(math.radians(a)), 22 + 18.5 * math.sin(math.radians(a)), FO) if a % 40 == 0 and y < 38 else None
    for x in range(10, 50):                                                                         # Magnetring
        y = 29 + round(4 * math.sqrt(max(0, 1 - ((x - 29.5) / 20) ** 2)))
        m.set(x, y, FW4); m.set(x, y + 1, FW3)
    for x in (2, 58): baeumchen(m, x + 1, 54)


@motiv('wunder:weltraumaufzug')
def _(m):
    sterne(m, 10, 41)
    for (x, y) in ((8, 6), (50, 12), (12, 24)): m.funkeln(x, y, WVH)
    m.rect(0, 56, 63, 63, '#4f9ae0'); m.rect(0, 56, 63, 56, WASSER_H); m.rect(0, 62, 63, 63, WASSER_D)  # Meer
    m.ppoly([(16, 58), (20, 52), (44, 52), (48, 58)], WW2); m.rect(18, 56, 46, 58, WW4)                # Plattform
    m.kasten(23, 52, 16, 7, 4, WW1); m.fenster(25, 47, 37, 50, 3, 3, WV); m.rect(23, 52, 38, 52, 'S')
    m.rect(31, 2, 32, 45, WW3); m.rect(31, 2, 31, 45, WW1)                                           # Seil
    m.kugel(31.5, 4, 7, 4, WW1); m.rect(25, 5, 38, 6, WW3); m.rect(26, 3, 37, 3, WV)                 # Gegengewicht-Station
    m.rect(21, 4, 24, 5, '#2a3f8c'); m.rect(39, 4, 42, 5, '#2a3f8c')
    for (y, c) in ((30, WV), (16, WF)):                                                               # Kletterkabinen
        m.kasten(28, y, 6, 5, 2, WW2); m.rect(29, y - 3, 32, y - 2, c); m.set(30, y - 3, hell(c, .5))
    for x in range(3, 62, 9): m.set(x, 59, '#ffffff')


@motiv('wunder:sternenarche')
def _(m):
    sterne(m, 12, 43)
    for (x, y) in ((6, 8), (56, 6), (52, 30)): m.funkeln(x, y, SGO, True)
    m.rect(0, 58, 63, 63, SP3); m.rect(0, 58, 63, 58, SP2)
    m.kasten(10, 58, 40, 4, 4, SP2, seite=SP3, dach=SP1); m.rect(10, 57, 49, 57, 'S')
    for x in (14, 44): m.rect(x, 30, x + 2, 54, SP3); m.rect(x, 30, x + 2, 30, SP1)                  # Startarme
    # Arche: langer Perlmutt-Rumpf, senkrecht startend
    m.ppoly([(22, 52), (20, 22), (23, 10), (29, 3), (35, 10), (38, 22), (36, 52)], SP1)
    m.ppoly([(29, 3), (35, 10), (38, 22), (36, 52), (30, 52)], SP2)
    m.ppoly([(22, 40), (12, 52), (22, 52)], SK3); m.ppoly([(36, 40), (46, 52), (36, 52)], SK4)
    for y in range(16, 46, 6): m.rect(25, y, 33, y + 2, SK2); m.rect(25, y, 33, y, SK1); m.set(31, y + 1, SK3)
    m.rect(21, 38, 37, 38, 'S'); m.rect(21, 39, 37, 39, 'S-')
    m.kugel(29, 11, 3, 3, SGO); m.set(28, 10, '#fff3c4')
    for x in (25, 29, 33): m.flamme(x, 53, 4, 'u', 1)


# ============================ Städte ============================
def platz(m, rx, cy=46, c='#9aa0b0'):
    m.kugel(32, cy, rx, 7, c, hell(c, .25), dunkel(c, .25), glanz=False)
    m.ell(32, cy - 1, rx - 2, 5, hell(c, .18))


def glasturm(m, x, yb, w, h, d, glas, rahmen, seed, garten=False, spitze=None):
    m.kasten(x, yb, w, h, d, glas, seite=dunkel(glas, .3), dach=hell(glas, .35))
    for y in range(yb - h + 3, yb - 1, 3): m.rect(x, y, x + w - 1, y, rahmen)
    r = random.Random(seed)
    for y in range(yb - h + 4, yb - 1, 3):
        for xx in range(x + 1, x + w - 1, 2):
            if r.random() < .25: m.set(xx, y, '#fff3a0')
    m.seitenfenster(x, yb, w, h, d, hell(glas, .2))
    if garten:
        for i in range(1, d + 1): m.rect(x + i, yb - h + 1 - i, x + w - 2 + i, yb - h + 1 - i, GRAS if i % 2 else GRAS_D)
        m.rect(x, yb - h + 1, x + w - 1, yb - h + 1, '#8fd86e')
    if spitze: m.line(x + w // 2 + 1, yb - h - d, x + w // 2 + 1, yb - h - d - spitze, M4); m.set(x + w // 2 + 1, yb - h - d - spitze - 1, KC)


def kuppelhaus(m, cx, yb, rx, ry, f, band):
    m.kugel(cx, yb, rx, ry, f, nur_oben=True); m.rect(cx - rx, yb - 1, cx + rx, yb, dunkel(f, .2))
    m.rect(cx - rx + 1, yb - ry // 2, cx + rx - 1, yb - ry // 2, band)


def kristall(m, x, yb, w, h):
    m.ppoly([(x - w, yb), (x - w, yb - h + w * 2), (x, yb - h), (x + w, yb - h + w * 2), (x + w, yb)], SK2)
    m.ppoly([(x, yb - h), (x + w, yb - h + w * 2), (x + w, yb), (x, yb)], SK3)
    m.line(x - w + 1, yb - h + w * 2 + 1, x - w + 1, yb - 2, SK1)


def stadt(m, z, g):
    rx = [16, 22, 28][g - 1]
    if z == 7:
        platz(m, rx, c='#a9b3c4')
        bauten = {1: [(-10, 9, 18, 0), (2, 8, 26, 1), (-2, 7, 13, 2)],
                  2: [(-18, 8, 15, 0), (-6, 9, 24, 1), (6, 8, 33, 1), (14, 7, 16, 0), (-12, 7, 11, 2), (2, 8, 12, 2)],
                  3: [(-24, 8, 14, 0), (-14, 8, 22, 1), (-3, 9, 30, 1), (8, 8, 38, 1), (18, 8, 20, 0), (-18, 7, 11, 2), (-6, 8, 13, 2), (6, 8, 12, 2), (16, 7, 10, 2)]}[g]
        for i, (dx, w, h, reihe) in enumerate(bauten):
            yb = 44 + reihe * 3
            glasturm(m, 32 + dx - w // 2, yb, w, h, 3, ['#5d9ae8', '#6aa8f0', '#4f88d8'][i % 3], '#d8e8ff', i + z * 7,
                     garten=(i % 2 == 0), spitze=(4 if h > 25 else None))
        m.rect(32 - rx + 6, 48, 32 + rx - 6, 48, 'S')
    elif z == 8:
        platz(m, rx, c='#c8bfa8')
        tuerme = {1: [(-6, 8, 16), (5, 8, 24)], 2: [(-16, 7, 14), (-5, 8, 22), (6, 9, 26), (16, 7, 17)],
                  3: [(-23, 7, 13), (-14, 8, 21), (-3, 9, 28), (8, 9, 30), (19, 8, 22)]}[g]
        hoechster = max(tuerme, key=lambda t: t[2])
        for (dx, w, h) in tuerme:
            x = 32 + dx - w // 2
            m.kasten(x, 44, w, h, 3, FW1, seite=FW3, dach=FW2)
            for y in range(44 - h + 3, 43, 4): m.rect(x, y, x + w - 1, y, FOH); m.set(x + w, y - 1, FO)
            m.fenster(x + 1, 44 - h + 5, x + w - 2, 42, 2, 4, '#9fd0f0')
        x = 32 + hoechster[0] - hoechster[1] // 2 + hoechster[1] // 2 + 1; yt = 44 - hoechster[2] - 3
        m.line(x, yt, x, yt - 4, FW4); m.kugel(x, yt - 8, 4, 4, FO, FOH, FR); m.set(x - 1, yt - 9, FOW)
        kuppeln = {1: [(-10, 6), (10, 5)], 2: [(-18, 6), (-2, 7), (17, 6)], 3: [(-22, 6), (-9, 7), (5, 8), (20, 6)]}[g]
        for (dx, r) in kuppeln: kuppelhaus(m, 32 + dx, 49, r, r * .9, FW1, FO)
        m.rect(32 - rx + 6, 51, 32 + rx - 6, 51, 'S')
    elif z == 9:
        platz(m, rx, c='#a9a2c0')
        hoch = [20, 28, 36][g - 1]
        m.rect(31, 1, 32, 44 - hoch, WW3); m.rect(31, 1, 31, 44 - hoch, WW1)                     # Aufzugseil
        m.kugel(31.5, 2, 4, 1.6, WW1, glanz=False)
        bauten = {1: [(-9, 7, 12), (9, 6, 10)], 2: [(-17, 6, 11), (-8, 7, 16), (10, 7, 18), (18, 6, 10)],
                  3: [(-23, 6, 10), (-14, 7, 17), (-6, 6, 12), (9, 7, 22), (18, 7, 14), (24, 5, 9)]}[g]
        for (dx, w, h) in bauten:
            x = 32 + dx - w // 2
            m.kasten(x, 44, w, h, 3, WW1, seite=WW3, dach=WW2); m.fenster(x + 1, 44 - h + 3, x + w - 2, 42, 2, 3, WV, '#ffd23f', None, random.Random(dx + g))
        m.kasten(28, 45, 6, hoch, 3, WW1, seite=WW3, dach=WW2); m.fenster(29, 45 - hoch + 3, 32, 43, 2, 3, WVD)  # Aufzugsturm
        m.ppoly([(40 + g * 2, 44), (40 + g * 2, 30 - g * 2), (42 + g * 2, 26 - g * 2), (44 + g * 2, 30 - g * 2), (44 + g * 2, 44)], WW1)
        m.set(42 + g * 2, 33 - g * 2, WVD); m.rect(40 + g * 2, 38, 44 + g * 2, 38, 'S')
        kuppeln = {1: [(-8, 6), (8, 5)], 2: [(-17, 6), (-3, 5), (15, 7)], 3: [(-21, 7), (-8, 5), (6, 6), (20, 7)]}[g]
        for (dx, r) in kuppeln: kuppelhaus(m, 32 + dx, 49, r, r * .9, '#cfeeff', WV)
        m.rect(32 - rx + 6, 51, 32 + rx - 6, 51, 'S')
        m.funkeln(8, 6, WVH); m.funkeln(56, 10, WVH)
    else:
        platz(m, rx, c='#bcd0e6')
        teile = {1: [(-7, 3, 18), (4, 4, 26), (12, 3, 14)],
                 2: [(-16, 3, 16), (-7, 4, 26), (4, 5, 36), (14, 3, 20), (21, 2, 12)],
                 3: [(-24, 3, 14), (-16, 4, 24), (-7, 4, 32), (4, 5, 42), (14, 4, 28), (22, 3, 18), (-1, 3, 16)]}[g]
        for (dx, w, h) in teile: kristall(m, 32 + dx, 47, w, h)
        m.rect(32 - rx + 6, 50, 32 + rx - 6, 50, 'S')
        m.funkeln(6, 8, SGO, True); m.funkeln(58, 6, SGO)


for _z in (7, 8, 9, 10):
    for _g in (1, 2, 3):
        NEU['stadt:stadt@%d@%d' % (_z, _g)] = (lambda z, g: (lambda m: stadt(m, z, g)))(_z, _g)


# ============================ Rohstoffe ============================
@motiv('rohstoff:seltene_erden')
def _(m):
    m.kugel(8, 12.5, 7, 3, '#8a7a68', glanz=False)
    m.ppoly([(2, 13), (3, 6), (5, 3), (7, 6), (7, 13)], '#e070b0'); m.ppoly([(5, 3), (7, 6), (7, 13), (5, 13)], '#a8407e')
    m.ppoly([(7, 13), (8, 5), (10, 2), (13, 5), (13, 13)], '#5ad8c8'); m.ppoly([(10, 2), (13, 5), (13, 13), (10, 13)], '#2a9a8e')
    m.set(3, 7, '#ffd0ea'); m.set(9, 6, '#d0fff6'); m.set(9, 7, '#d0fff6')

@motiv('rohstoff:deuterium')
def _(m):
    m.ppoly([(8, 1), (13, 8), (13, 11), (11, 14), (5, 14), (3, 11), (3, 8)], '#5aa9e6')
    m.ppoly([(8, 1), (13, 8), (13, 11), (11, 14), (8, 14)], '#2f78b5')
    m.set(5, 8, '#d6f0ff'); m.set(5, 9, '#d6f0ff'); m.set(6, 6, '#d6f0ff')
    m.rect(7, 9, 8, 12, '#ffffff'); m.set(9, 10, '#ffffff'); m.set(9, 11, '#ffffff')         # D

@motiv('rohstoff:titan')
def _(m):
    for (y, x) in ((10, 1), (5, 4)):
        m.ppoly([(x, y + 4), (x + 2, y), (x + 11, y), (x + 9, y + 4)], '#b8c4d4')
        m.rect(x + 1, y + 1, x + 9, y + 1, '#e8eef6'); m.rect(x, y + 4, x + 9, y + 4, '#6a7890')
        m.ppoly([(x + 9, y + 4), (x + 11, y), (x + 11, y + 3), (x + 10, y + 4)], '#7a88a0')
        m.set(x + 4, y + 2, '#8fa0bc')

@motiv('rohstoff:helium3')
def _(m):
    m.rect(5, 2, 10, 3, '#6a7890'); m.rect(6, 1, 9, 1, '#8fa0bc')
    m.kugel(7.5, 9, 5.5, 5.5, '#bfe6ff', '#ffffff', '#7fb8e6')
    m.kugel(7.5, 9.5, 2.5, 2.5, '#c3b6ee', '#ffffff', '#8e7cc3', glanz=False)
    m.set(5, 6, '#ffffff'); m.set(4, 7, '#ffffff')


# ============================ Zeitalter-Symbole ============================
GLYPHE = {
    'I': ['DD'] * 9,
    'V3': ['D.D', 'D.D', 'D.D', 'D.D', 'D.D', 'DDD', '.D.', '.D.', '.D.'],
    'X': ['DD..DD', 'DD..DD', '.DDDD.', '..DD..', '..DD..', '..DD..', '.DDDD.', 'DD..DD', 'DD..DD'],
}
ZA_FARBEN = {7: ('#1f3478', '#5b8cff', '#8fb2ff', '#3a5cc0', '#fff6dc'),
             8: ('#7a4510', '#f2a33a', '#ffc46a', '#c47a1c', '#fff6dc'),
             9: ('#3a2d6e', '#8e7cc3', '#b2a4e2', '#6a5aa4', '#fff6dc'),
             10: ('#4a5a78', '#d8e4f2', '#f6faff', '#a8b8d0', '#2a3a58')}
ZA_ZEICHEN = {7: [('V3', 2), ('I', 6), ('I', 9), ('I', 12)], 8: [('I', 3), ('X', 6)], 9: [('X', 5)], 10: [('X', 3), ('I', 10)]}

def za(m, z):
    A, B, C, E, D = ZA_FARBEN[z]
    m.rect(1, 0, 14, 15, A); m.rect(0, 1, 15, 14, A)
    m.rect(1, 1, 14, 14, B); m.rect(2, 1, 13, 1, C); m.rect(1, 14, 14, 14, E)
    for (g, x0) in ZA_ZEICHEN[z]:
        for dy, zeile in enumerate(GLYPHE[g]):
            for dx, ch in enumerate(zeile):
                if ch == 'D': m.set(x0 + dx, 3 + dy, D)

for _z in (7, 8, 9, 10):
    NEU['za:%d' % _z] = (lambda z: (lambda m: za(m, z)))(_z)
