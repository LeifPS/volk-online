"""Selbst gezeichnete Pixel-Sprites für die Zeitalter VIII bis XI (KI, Fusion, Weltraum, Sterne).
Einheiten und Gebäude 32x32, Wunder 64x64, Rohstoffe 16x16, Städte 64x56, Zeitalter-Symbole 16x16.
Eine Zeichenfunktion je Motiv; der Schlüssel (z. B. 'einheit:kampfroboter') ist die ID. Jedes Motiv wird in spr._S eingetragen."""
import math, json
import spr
from px import Px, OUT, mixc, hell, dunkel

REG = {}                       # Schlüssel -> Zeichenfunktion
def motiv(key):
    def deko(fn): REG[key] = fn; return fn
    return deko

# ---------------- Paletten ----------------
KI_W = '#e4eaf5'; KI_G = '#aab6cc'; KI_D = '#6a7894'; KI_K = '#2d3446'; KI_B = '#5b8cff'; KI_BH = '#a6c4ff'; KI_C = '#4ee3ff'
FU_W = '#f6f1e6'; FU_G = '#c9c2b4'; FU_D = '#8d8678'; FU_O = '#f2a33a'; FU_OH = '#ffd27a'; FU_OO = '#fff1c2'; FU_R = '#e8553a'; FU_K = '#3a342c'
WR_V = '#8e7cc3'; WR_VH = '#b9abe3'; WR_VD = '#5e4f99'; WR_K = '#262142'; WR_W = '#ece9f5'; WR_G = '#b4b0c6'; WR_F = '#ff9a3a'; WR_FH = '#ffd23f'
ST_W = '#eef4fb'; ST_G = '#bcd0e6'; ST_D = '#7f9cc2'; ST_K = '#2a3a58'; ST_T = '#7be3ff'; ST_TD = '#37a6c9'; ST_Y = '#ffe08a'; ST_P = '#9a7bd6'
HAUT = '#e8b890'

# ---------------- Bausteine ----------------
def mensch(m, rumpf, rumpf2, helm, visier, hose=None, arm=None, gewehr=None, rucksack=None, x=0, schritt=1):
    """Stehende Figur (nach rechts blickend), Mitte ca. x 15.5; x = Verschiebung."""
    hose = hose or rumpf2; arm = arm or rumpf
    for dx, dy in ((0, 0),):
        m.rect(12 + x, 21, 14 + x, 27, hose); m.rect(17 + x, 21, 19 + x, 27 - (0 if schritt else 1), hose)
        m.rect(11 + x, 28, 14 + x, 28, rumpf2); m.rect(17 + x, 28, 20 + x, 28, rumpf2)
    if rucksack: m.rect(8 + x, 12, 10 + x, 20, rucksack)
    m.rect(11 + x, 12, 20 + x, 21, rumpf); m.rect(11 + x, 19, 20 + x, 21, rumpf2); m.rect(11 + x, 12, 20 + x, 13, hell(rumpf, .25))
    m.ell(15.5 + x, 8.5, 3.6, 3.6, helm); m.rect(14 + x, 8, 19 + x, 10, visier); m.set(19 + x, 8, hell(visier, .4))
    m.rect(9 + x, 13, 10 + x, 19, arm)
    m.rect(21 + x, 14, 23 + x, 17, arm)
    if gewehr: gewehr(m, x)

def knarre(farbe, glow=None, lang=7):
    def f(m, x):
        m.rect(21 + x, 16, 22 + x + lang, 17, farbe); m.rect(20 + x, 17, 22 + x, 19, dunkel(farbe, .3))
        if glow: m.set(22 + x + lang, 16, glow); m.set(23 + x + lang, 16, hell(glow, .4))
    return f

def panzerwanne(m, y0, y1, x0, x1, farbe, dk, kette=OUT):
    m.rect(x0, y0, x1, y1, farbe); m.rect(x0, y1 - 1, x1, y1, dk); m.rect(x0, y0, x1, y0, hell(farbe, .3))
    for x in range(x0 + 1, x1, 3): m.set(x, y0 + 1, dk)

def raupen(m, x0, x1, y0, y1, c='#4a4658', c2='#7a7690'):
    m.rect(x0, y0, x1, y1, c)
    for x in range(x0, x1 + 1, 2): m.set(x, y0, c2)
    m.ell(x0 + 1, (y0 + y1) / 2, 1.5, (y1 - y0) / 2, c2); m.ell(x1 - 1, (y0 + y1) / 2, 1.5, (y1 - y0) / 2, c2)

def schweberpads(m, x0, x1, y, c, c2):
    for x in range(x0, x1 + 1): m.set(x, y, c)
    for x in range(x0 + 2, x1 - 1, 3): m.set(x, y + 1, c2); m.set(x, y + 2, mixc(c2, '#ffffff', .5))

def kugelkopf(m, cx, cy, r, c, auge):
    m.ell(cx, cy, r, r, c); m.rect(int(cx - r + 1), int(cy), int(cx + r - 1), int(cy) + 1, '#1b2338'); m.rect(int(cx - 1), int(cy), int(cx + r - 1), int(cy), auge)

def rakete(m, cx, y0, y1, w, farbe, spitze, flamme=True):
    m.rect(cx - w, y0 + 4, cx + w, y1, farbe); m.rect(cx + w - 1, y0 + 4, cx + w, y1, dunkel(farbe, .2))
    m.tri(cx, y0, y0 + 4, w, spitze)
    m.rect(cx - w - 2, y1 - 4, cx - w - 1, y1 + 1, spitze); m.rect(cx + w + 1, y1 - 4, cx + w + 2, y1 + 1, spitze)
    m.rect(cx - 1, y0 + 6, cx, y0 + 7, '#2d3446')
    if flamme:
        m.tri(cx, y1 + 1, y1 + 6, w - 1, WR_F); m.tri(cx, y1 + 1, y1 + 3, w - 2, WR_FH)

# ======================================================================
#  ZEITALTER VIII · KI-ZEITALTER  (blau, Schaltkreise)
# ======================================================================
@motiv('einheit:exoskelett_infanterie')
def _(m):
    mensch(m, KI_G, KI_D, KI_W, KI_C, hose=KI_D, arm=KI_G, gewehr=knarre('#3a4358', KI_C), rucksack=KI_K)
    m.rect(11, 22, 14, 23, KI_B); m.rect(17, 22, 20, 23, KI_B)            # Servo-Gelenke
    m.rect(10, 12, 12, 14, KI_W); m.rect(19, 12, 21, 14, KI_W)           # Schulterplatten
    m.line(12, 24, 12, 27, KI_C); m.line(19, 24, 19, 27, KI_C)
    m.rect(8, 9, 9, 10, KI_C)

@motiv('einheit:kampfroboter')
def _(m):
    m.rect(11, 22, 14, 28, KI_D); m.rect(17, 22, 20, 28, KI_D); m.rect(10, 28, 14, 29, KI_K); m.rect(17, 28, 21, 29, KI_K)
    m.rect(9, 11, 22, 22, KI_G); m.rect(9, 19, 22, 22, KI_D); m.rect(9, 11, 22, 12, KI_W)
    m.rect(12, 14, 19, 18, KI_K); m.rect(13, 15, 18, 16, KI_C); m.set(15, 17, KI_B); m.set(16, 17, KI_B)
    m.rect(11, 5, 20, 10, KI_W); m.rect(12, 7, 19, 8, KI_C); m.rect(11, 9, 20, 10, KI_G); m.rect(15, 2, 16, 4, KI_D); m.set(15, 1, KI_C)
    m.rect(5, 12, 8, 21, KI_D); m.rect(5, 12, 8, 13, KI_W); m.rect(23, 12, 26, 19, KI_D); m.rect(26, 15, 30, 16, '#3a4358'); m.rect(26, 17, 30, 17, KI_K); m.set(30, 15, KI_C)

@motiv('einheit:drohnenschwarm')
def _(m):
    pos = [(8, 9), (17, 6), (24, 12), (12, 18), (21, 21), (5, 23), (27, 24)]
    for i, (x, y) in enumerate(pos):
        m.rect(x - 1, y, x + 3, y + 1, KI_W); m.rect(x, y + 1, x + 2, y + 2, KI_D); m.rect(x - 3, y - 1, x - 2, y - 1, KI_G); m.rect(x + 4, y - 1, x + 5, y - 1, KI_G)
        m.set(x + 1, y + 2, KI_C)
    m.set(10, 12, KI_BH); m.set(22, 16, KI_BH); m.set(16, 25, KI_BH)

@motiv('einheit:autonomer_panzer')
def _(m):
    raupen(m, 4, 27, 22, 27); panzerwanne(m, 15, 22, 5, 26, KI_G, KI_D)
    m.rect(9, 10, 20, 15, KI_W); m.rect(9, 14, 20, 15, KI_G); m.rect(20, 11, 30, 13, KI_D); m.rect(29, 10, 31, 14, KI_K)
    m.rect(11, 12, 16, 13, KI_C); m.rect(6, 17, 10, 18, KI_B); m.rect(22, 17, 25, 18, KI_B)
    m.line(14, 6, 14, 9, KI_D); m.set(14, 5, KI_C)

@motiv('einheit:laserabwehr')
def _(m):
    raupen(m, 6, 25, 24, 28); m.rect(7, 19, 24, 24, KI_G); m.rect(7, 22, 24, 24, KI_D)
    m.rect(13, 14, 18, 19, KI_W); m.poly([(10, 14), (21, 14), (24, 5), (7, 5)], KI_D); m.poly([(11, 13), (20, 13), (22, 7), (9, 7)], KI_G)
    m.ell(15.5, 9, 2.5, 2.5, KI_K); m.set(15, 8, KI_C); m.set(16, 8, KI_C); m.line(16, 8, 28, 1, KI_C); m.line(17, 8, 29, 2, KI_BH); m.glimmer(29, 1, KI_BH)

@motiv('einheit:drohnenjaeger')
def _(m):
    m.poly([(3, 18), (10, 15), (24, 15), (30, 18), (24, 20), (10, 20)], KI_W)
    m.poly([(12, 15), (18, 5), (22, 5), (21, 15)], KI_G); m.poly([(12, 20), (18, 28), (22, 28), (21, 20)], KI_G)
    m.rect(8, 17, 26, 18, KI_B); m.rect(24, 16, 27, 17, KI_C); m.set(29, 18, KI_D)
    m.rect(2, 16, 4, 19, KI_D); m.set(1, 17, KI_BH); m.set(1, 18, KI_B)

@motiv('einheit:lieferdrohnen')
def _(m):
    for x in (6, 22): m.rect(x, 7, x + 4, 8, KI_G); m.rect(x + 1, 8, x + 3, 9, KI_D)
    m.rect(5, 6, 9, 6, KI_BH); m.rect(23, 6, 27, 6, KI_BH)
    m.rect(8, 9, 23, 12, KI_W); m.rect(8, 11, 23, 12, KI_G); m.rect(13, 9, 18, 10, KI_C)
    m.rect(10, 14, 21, 25, '#c9915a'); m.rect(10, 14, 21, 15, '#e0b07a'); m.rect(15, 14, 16, 25, '#8a5a2b'); m.rect(10, 24, 21, 25, '#9a6a3a')
    m.line(10, 12, 10, 14, KI_D); m.line(21, 12, 21, 14, KI_D)
    m.rect(12, 18, 14, 20, KI_B); m.set(13, 19, '#ffffff')

# ---- Gebäude VIII ----
def boden(m, y=29, x0=3, x1=28, c='#6b6a5a', c2='#8a8a76'):
    m.rect(x0, y, x1, y + 1, c); m.rect(x0, y, x1, y, c2)

def fenster_reihen(m, x0, y0, x1, y1, c, c2, abst=3):
    for y in range(y0, y1 + 1, abst):
        for x in range(x0, x1 + 1, abst): m.set(x, y, c if (x + y) % 2 else c2)

@motiv('gebaeude:ki_labor')
def _(m):
    boden(m); m.rect(5, 12, 26, 28, KI_W); m.rect(5, 12, 26, 13, '#ffffff'); m.rect(5, 26, 26, 28, KI_G)
    m.rect(8, 15, 23, 24, KI_K); m.rect(8, 15, 23, 15, KI_B)
    for i, x in enumerate(range(9, 23, 3)): m.rect(x, 17, x + 1, 23, [KI_C, KI_B, KI_BH, KI_C, KI_B][i % 5])
    m.rect(13, 6, 18, 11, KI_G); m.rect(14, 7, 17, 10, KI_K); m.rect(15, 8, 16, 9, KI_C); m.line(15, 2, 15, 5, KI_D); m.glimmer(15, 1, KI_C)
    m.set(8, 9, KI_B); m.set(23, 9, KI_B); m.line(8, 10, 8, 11, KI_G); m.line(23, 10, 23, 11, KI_G)

@motiv('gebaeude:autonome_fabrik')
def _(m):
    boden(m); m.rect(4, 15, 27, 28, KI_G); m.rect(4, 15, 27, 16, KI_W); m.rect(4, 26, 27, 28, KI_D)
    for x in (5, 12, 19): m.poly([(x, 15), (x + 3, 9), (x + 7, 15)], KI_W); m.poly([(x + 1, 15), (x + 3, 11), (x + 6, 15)], KI_BH)
    m.rect(7, 19, 12, 25, KI_K); m.rect(15, 19, 20, 25, KI_K); m.rect(8, 21, 11, 21, KI_C); m.rect(16, 22, 19, 22, KI_C)
    m.rect(22, 18, 26, 25, KI_D); m.line(23, 20, 25, 20, KI_C); m.line(23, 22, 25, 22, KI_B)
    m.rect(14, 2, 16, 8, KI_D); m.rect(13, 2, 17, 3, KI_G); m.set(15, 1, KI_C)
    m.line(9, 17, 9, 19, KI_B)

@motiv('gebaeude:intelligentes_stromnetz')
def _(m):
    boden(m)
    for x, h in ((7, 14), (16, 18), (25, 14)):
        m.rect(x - 1, 28 - h, x, 28, KI_D); m.rect(x - 4, 28 - h, x + 3, 28 - h + 1, KI_G); m.rect(x - 3, 28 - h - 1, x + 2, 28 - h - 1, KI_B)
        m.glimmer(x, 28 - h - 3, KI_C)
    m.line(7, 14, 15, 10, KI_B); m.line(16, 10, 25, 14, KI_B); m.line(7, 15, 15, 11, KI_C); m.line(16, 11, 25, 15, KI_C)
    m.rect(12, 21, 20, 28, KI_W); m.rect(12, 21, 20, 22, KI_G); m.rect(14, 23, 18, 26, KI_K); m.rect(15, 24, 17, 25, KI_C)

@motiv('gebaeude:virtuelles_forum')
def _(m):
    boden(m); m.rect(4, 22, 27, 28, KI_G); m.rect(4, 22, 27, 23, KI_W)
    m.poly([(5, 22), (9, 6), (22, 6), (26, 22)], KI_K); m.poly([(8, 21), (11, 8), (20, 8), (23, 21)], KI_B)
    for i in range(5): m.line(10 + i * 3, 9, 8 + i * 3, 20, KI_BH)
    m.line(10, 12, 21, 12, KI_C); m.line(9, 16, 22, 16, KI_C)
    m.ell(15.5, 14, 3, 3, KI_BH); m.ell(15.5, 14, 1.5, 3, KI_B)

@motiv('gebaeude:laserturm')
def _(m):
    boden(m); m.rect(11, 16, 20, 28, KI_G); m.rect(11, 16, 20, 17, KI_W); m.rect(10, 26, 21, 28, KI_D)
    m.rect(13, 19, 18, 24, KI_K); m.rect(14, 20, 17, 21, KI_C)
    m.poly([(8, 16), (23, 16), (20, 9), (11, 9)], KI_D); m.rect(13, 5, 18, 9, KI_W); m.rect(14, 6, 17, 7, KI_C)
    m.line(15, 1, 15, 4, KI_BH); m.line(16, 1, 16, 4, KI_BH); m.glimmer(15, 0, KI_C)
    m.line(19, 8, 29, 3, KI_C); m.line(19, 9, 29, 4, KI_BH)

@motiv('gebaeude:vertikalfarm')
def _(m):
    boden(m); m.rect(7, 4, 24, 28, KI_W); m.rect(7, 4, 24, 5, '#ffffff'); m.rect(7, 26, 24, 28, KI_G)
    for i, y in enumerate((7, 12, 17, 22)):
        m.rect(8, y, 23, y + 3, '#2f6b33'); m.rect(8, y, 23, y, '#5fbf4a')
        for x in range(9, 23, 3): m.set(x, y - 1 if False else y + 1, '#5fbf4a'); m.set(x, y + 2, '#3d8a3d')
        m.rect(8, y + 4, 23, y + 4, KI_B)
    m.rect(7, 4, 8, 25, KI_G); m.rect(23, 4, 24, 25, KI_G)

# ---- Wunder VIII: Weltgehirn ----
@motiv('wunder:weltgehirn')
def _(m):
    sterne_hintergrund_ki(m)
    m.rect(14, 54, 50, 62, KI_D); m.rect(14, 54, 50, 55, KI_G); m.rect(10, 60, 54, 63, KI_K)
    m.rect(24, 44, 40, 54, KI_G); m.rect(24, 44, 40, 45, KI_W)
    m.ell(32, 30, 20, 16, '#e8a0b8'); m.ell(32, 28, 18, 13, '#f5c0d0')                  # Gehirn
    for dx, dy, rx, ry in ((-9, -4, 8, 6), (8, -5, 8, 6), (-6, 6, 7, 5), (9, 5, 8, 5)): m.ell(32 + dx, 29 + dy, rx, ry, '#f0a8c0')
    for (x0, y0, x1, y1) in ((16, 24, 26, 26), (30, 20, 44, 21), (22, 32, 34, 33), (36, 30, 48, 32)):
        m.line(x0, y0, x1, y1, '#c06888')
    for (x, y) in ((20, 22), (30, 17), (40, 22), (26, 31), (44, 31), (34, 25)): m.glimmer(x, y, KI_C, KI_B)
    m.line(32, 14, 32, 6, KI_BH); m.line(20, 17, 14, 11, KI_BH); m.line(44, 17, 50, 11, KI_BH)
    for x, y in ((32, 5), (13, 10), (51, 10)): m.glimmer(x, y, '#ffffff', KI_C)
    m.rect(20, 46, 21, 53, KI_C); m.rect(42, 46, 43, 53, KI_C); m.rect(28, 50, 36, 51, KI_B)

def sterne_hintergrund_ki(m):
    pass

# ======================================================================
#  ZEITALTER IX · FUSIONSZEITALTER  (Orange, Plasma, weiße Kuppeln)
# ======================================================================
@motiv('einheit:plasmagrenadier')
def _(m):
    mensch(m, FU_W, FU_D, FU_G, FU_OH, hose=FU_D, arm=FU_W, gewehr=None, rucksack=FU_K)
    m.rect(21, 15, 26, 19, FU_K); m.rect(26, 14, 28, 20, FU_D); m.ell(29.5, 17, 2, 2.5, FU_O); m.set(29, 16, FU_OO); m.set(30, 17, FU_OO)
    m.rect(11, 14, 20, 14, FU_O); m.rect(8, 11, 9, 13, FU_O)

@motiv('einheit:schwebepanzer')
def _(m):
    schweberpads(m, 5, 27, 26, FU_D, FU_O)
    m.poly([(3, 25), (6, 17), (26, 17), (29, 25)], FU_W); m.poly([(5, 24), (8, 18), (24, 18), (27, 24)], FU_G)
    m.rect(10, 11, 21, 17, FU_W); m.rect(10, 11, 21, 12, '#ffffff'); m.rect(12, 13, 19, 15, FU_K); m.rect(13, 14, 18, 14, FU_O)
    m.rect(21, 13, 30, 14, FU_D); m.rect(30, 12, 31, 15, FU_K); m.rect(4, 20, 6, 21, FU_O); m.rect(25, 20, 27, 21, FU_O)

@motiv('einheit:railgun_batterie')
def _(m):
    raupen(m, 5, 24, 24, 28); m.rect(5, 19, 24, 24, FU_G); m.rect(5, 22, 24, 24, FU_D)
    m.poly([(8, 20), (14, 20), (26, 5), (30, 7), (18, 20)], FU_W)
    m.poly([(10, 20), (14, 20), (26, 7), (28, 9), (16, 19)], FU_D); m.line(12, 19, 27, 7, FU_O); m.line(14, 19, 28, 8, FU_OH)
    m.glimmer(30, 5, FU_OO, FU_OH); m.rect(7, 20, 9, 22, FU_O)

@motiv('einheit:hyperschallbomber')
def _(m):
    m.poly([(1, 17), (8, 14), (28, 12), (31, 17), (28, 22), (8, 20)], FU_W)
    m.poly([(10, 14), (18, 2), (23, 2), (21, 14)], FU_G); m.poly([(10, 20), (18, 29), (23, 29), (21, 20)], FU_G)
    m.poly([(24, 14), (30, 14), (29, 16), (24, 16)], FU_K)
    m.rect(5, 16, 27, 16, FU_O); m.rect(2, 17, 7, 19, FU_D); m.rect(0, 16, 1, 19, FU_O); m.set(0, 15, FU_OH); m.set(0, 20, FU_OH)

@motiv('einheit:fusionszerstoerer')
def _(m):
    m.poly([(1, 22), (4, 25), (28, 25), (31, 21), (28, 20), (4, 20)], FU_D); m.rect(2, 22, 30, 24, FU_G); m.rect(3, 24, 29, 25, FU_K)
    m.rect(9, 15, 22, 20, FU_W); m.rect(9, 15, 22, 16, '#ffffff'); m.rect(12, 17, 19, 18, FU_K)
    m.poly([(12, 15), (16, 9), (20, 15)], FU_G); m.ell(16, 11, 3, 2.5, FU_O); m.set(15, 10, FU_OO)
    m.rect(24, 17, 28, 18, FU_D); m.rect(28, 16, 29, 19, FU_O); m.line(3, 26, 28, 26, '#2f78b5'); m.rect(1, 22, 3, 23, FU_OH)

@motiv('einheit:hyperloop_kurier')
def _(m):
    m.rect(2, 25, 29, 27, FU_D); m.rect(2, 25, 29, 25, FU_G); m.rect(4, 28, 27, 28, FU_O)
    m.poly([(3, 24), (6, 15), (25, 15), (30, 20), (30, 24)], FU_W); m.rect(5, 22, 29, 24, FU_G)
    m.rect(9, 17, 12, 19, FU_K); m.rect(14, 17, 17, 19, FU_K); m.rect(19, 17, 22, 19, FU_K); m.rect(25, 17, 28, 19, FU_O)
    m.rect(3, 20, 29, 20, FU_O); m.rect(7, 14, 24, 14, FU_OH)

# ---- Gebäude IX ----
@motiv('gebaeude:fusionsreaktor')
def _(m):
    boden(m); m.rect(5, 18, 26, 28, FU_G); m.rect(5, 18, 26, 19, FU_W); m.rect(5, 26, 26, 28, FU_D)
    m.ell(15.5, 17, 11, 12, FU_W); m.rect(4, 17, 27, 29, FU_G); m.ell(15.5, 17, 11, 12, FU_W)
    m.ell(15.5, 15, 7, 7, FU_O); m.ell(15.5, 15, 5, 5, FU_OH); m.ell(15.5, 15, 2.5, 2.5, FU_OO)
    m.ell(15.5, 15, 8.5, 2.2, FU_D); m.ell(15.5, 15, 8.5, 1.2, FU_OH)
    m.rect(5, 22, 26, 24, FU_G); m.rect(7, 23, 24, 23, FU_O); m.glimmer(15, 4, FU_OH, FU_O)

@motiv('gebaeude:quantenrechner')
def _(m):
    boden(m); m.rect(6, 12, 25, 28, '#c8d2e6'); m.rect(6, 12, 25, 13, '#ffffff'); m.rect(6, 26, 25, 28, '#8a96b4')
    m.rect(9, 15, 22, 25, '#222a40'); m.rect(9, 15, 22, 15, '#5b8cff')
    m.ell(15.5, 20, 5, 5, '#3a4a78'); m.ell(15.5, 20, 3.5, 3.5, '#5b8cff'); m.ell(15.5, 20, 1.5, 1.5, '#ffffff')
    for a in range(6):
        ax = 15.5 + math.cos(a * math.pi / 3) * 8; ay = 20 + math.sin(a * math.pi / 3) * 4.5; m.set(ax, ay, FU_OH)
    m.rect(11, 5, 20, 11, '#9aa6c0'); m.rect(13, 3, 18, 5, '#6a7894'); m.line(15, 0, 16, 3, FU_O)

@motiv('gebaeude:energieschild')
def _(m):
    boden(m); m.rect(11, 20, 20, 28, FU_G); m.rect(11, 20, 20, 21, FU_W); m.rect(9, 26, 22, 28, FU_D)
    m.rect(13, 22, 18, 25, FU_K); m.rect(14, 23, 17, 24, FU_O)
    m.ell(15.5, 20, 14, 14, FU_OH)
    for y in range(4, 22):
        for x in range(0, 32):
            if (x - 15.5) ** 2 + (y - 20) ** 2 <= 14.2 ** 2 and (x - 15.5) ** 2 + (y - 20) ** 2 >= 11.6 ** 2: m.set(x, y, FU_OH if (x + y) % 3 else FU_O)
            elif (x - 15.5) ** 2 + (y - 20) ** 2 < 11.6 ** 2 and y < 21 and m.p.get((x, y)) == FU_OH: del m.p[(x, y)]
    m.rect(11, 20, 20, 28, FU_G); m.rect(11, 20, 20, 21, FU_W); m.rect(9, 26, 22, 28, FU_D); m.rect(13, 22, 18, 25, FU_K); m.rect(14, 23, 17, 24, FU_O)
    m.glimmer(15, 9, FU_OO, FU_OH)

@motiv('gebaeude:hyperloop_station')
def _(m):
    boden(m); m.rect(2, 24, 29, 28, FU_D); m.rect(2, 24, 29, 25, FU_G)
    m.ell(15.5, 22, 13, 11, FU_W); m.rect(2, 22, 29, 28, FU_D); m.rect(2, 24, 29, 25, FU_G)
    m.ell(15.5, 22, 13, 11, FU_W)
    m.rect(2, 22, 29, 28, FU_G); m.rect(2, 24, 29, 24, FU_W)
    m.rect(8, 17, 23, 21, FU_K); m.rect(9, 18, 22, 19, FU_O)
    m.rect(5, 25, 26, 27, FU_K); m.rect(6, 26, 25, 26, FU_OH)
    m.rect(14, 4, 17, 11, FU_G); m.rect(15, 5, 16, 6, FU_O)

@motiv('gebaeude:co2_waescher')
def _(m):
    boden(m); m.rect(4, 20, 27, 28, FU_G); m.rect(4, 20, 27, 21, FU_W); m.rect(4, 26, 27, 28, FU_D)
    for x in (6, 14, 22):
        m.rect(x, 7, x + 4, 20, FU_W); m.rect(x, 7, x + 4, 8, '#ffffff'); m.rect(x + 3, 8, x + 4, 20, FU_G)
        for y in (11, 14, 17): m.rect(x + 1, y, x + 2, y, '#5fbf4a')
        m.rect(x, 5, x + 4, 6, FU_D)
    m.rect(8, 23, 22, 24, '#5fbf4a'); m.rect(9, 23, 21, 23, '#9fe08a')
    m.set(8, 3, '#bfe8a8'); m.set(16, 2, '#bfe8a8'); m.set(24, 3, '#bfe8a8')

# ---- Wunder IX: Künstliche Sonne ----
@motiv('wunder:kuenstliche_sonne')
def _(m):
    m.rect(8, 56, 56, 63, '#8d8678'); m.rect(8, 56, 56, 57, '#c9c2b4'); m.rect(4, 60, 60, 63, '#3a342c')
    m.rect(26, 46, 38, 56, '#c9c2b4'); m.rect(26, 46, 38, 47, '#f6f1e6')
    for a in range(16):
        ang = a * math.pi / 8
        for t in range(14, 28):
            m.set(32 + math.cos(ang) * t, 26 + math.sin(ang) * t, '#f2a33a' if a % 2 else '#ffd27a')
    m.ell(32, 26, 14, 14, '#e8553a'); m.ell(32, 26, 11, 11, '#f2a33a'); m.ell(32, 26, 8, 8, '#ffd27a'); m.ell(32, 26, 4.5, 4.5, '#fff1c2')
    m.set(28, 22, '#ffffff'); m.set(29, 22, '#ffffff')
    for a in range(8):
        ang = a * math.pi / 4 + .39
        m.set(32 + math.cos(ang) * 20, 26 + math.sin(ang) * 20, '#fff1c2')
    for x in (12, 20, 44, 52): m.line(x, 46, x + (6 if x < 32 else -6), 56, '#8d8678')
    m.ell(32, 47, 12, 2.5, '#8d8678')

# ======================================================================
#  ZEITALTER X · WELTRAUMZEITALTER  (Violett, Orbit, Mond/Mars)
# ======================================================================
@motiv('einheit:orbital_marine')
def _(m):
    mensch(m, WR_W, WR_G, WR_W, '#7be3ff', hose=WR_G, arm=WR_W, gewehr=knarre('#4a4660', WR_F), rucksack=WR_VD)
    m.ell(15.5, 8.5, 4.3, 4.3, WR_W); m.rect(13, 7, 19, 10, '#2a3a78'); m.rect(14, 8, 18, 8, '#7be3ff')
    m.rect(11, 15, 20, 15, WR_V); m.rect(8, 14, 9, 17, WR_VD); m.rect(6, 12, 7, 12, WR_F)

@motiv('einheit:kampfshuttle')
def _(m):
    m.poly([(2, 20), (8, 12), (22, 12), (29, 17), (29, 22), (22, 24), (8, 24)], WR_W)
    m.poly([(12, 12), (16, 4), (21, 4), (20, 12)], WR_G); m.poly([(12, 24), (16, 30), (21, 30), (20, 24)], WR_G)
    m.poly([(22, 13), (28, 17), (22, 17)], '#2a3a78'); m.rect(23, 14, 26, 15, '#7be3ff')
    m.rect(6, 18, 22, 19, WR_V); m.rect(1, 17, 3, 22, WR_VD); m.set(0, 19, WR_F); m.set(0, 20, WR_FH); m.rect(4, 20, 8, 21, WR_F)

@motiv('einheit:orbitalkanone')
def _(m):
    m.rect(6, 25, 25, 28, WR_VD); m.rect(6, 25, 25, 25, WR_V); m.rect(9, 20, 22, 25, WR_G); m.rect(9, 20, 22, 21, WR_W)
    m.ell(15.5, 18, 6, 6, WR_W); m.ell(15.5, 18, 4, 4, WR_V); m.ell(15.5, 18, 2, 2, WR_FH)
    m.rect(18, 15, 30, 17, WR_G); m.rect(18, 15, 30, 15, WR_W); m.rect(29, 14, 31, 18, WR_K); m.line(27, 16, 31, 12, WR_FH)
    m.rect(11, 8, 12, 14, WR_G); m.rect(10, 7, 13, 8, WR_V); m.set(11, 5, WR_FH)

@motiv('einheit:marsrover_panzer')
def _(m):
    for x in (6, 14, 22): m.ell(x + 2, 25, 3.5, 3.5, '#4a4658'); m.ell(x + 2, 25, 1.5, 1.5, '#9a96b0')
    m.rect(4, 17, 28, 24, '#b5532c'); m.rect(4, 17, 28, 18, '#d97a4a'); m.rect(4, 22, 28, 24, '#8a3a1c')
    m.rect(9, 10, 19, 17, WR_W); m.rect(9, 10, 19, 11, '#ffffff'); m.rect(11, 12, 17, 15, '#2a3a78'); m.rect(12, 13, 16, 13, '#7be3ff')
    m.rect(19, 12, 29, 14, WR_G); m.rect(28, 11, 30, 15, WR_K); m.line(24, 10, 24, 6, WR_V); m.glimmer(24, 5, WR_FH)

@motiv('einheit:raumjaeger')
def _(m):
    m.poly([(2, 17), (10, 12), (26, 14), (31, 17), (26, 20), (10, 22)], WR_W)
    m.poly([(11, 12), (16, 3), (20, 3), (19, 13)], WR_V); m.poly([(11, 22), (16, 30), (20, 30), (19, 21)], WR_V)
    m.rect(5, 16, 28, 17, WR_VD); m.poly([(20, 14), (26, 16), (20, 16)], '#2a3a78'); m.set(23, 15, '#7be3ff')
    m.rect(0, 15, 3, 19, WR_F); m.rect(0, 16, 1, 18, WR_FH); m.rect(15, 1, 16, 3, WR_W); m.rect(15, 30, 16, 31, WR_W)

@motiv('einheit:asteroidenfrachter')
def _(m):
    m.ell(23, 19, 7, 6, '#7a7690'); m.ell(22, 18, 5, 4, '#9a96b0'); m.set(21, 16, '#5e5a74'); m.set(24, 20, '#5e5a74'); m.set(25, 17, '#5e5a74')
    m.rect(2, 14, 16, 22, WR_W); m.rect(2, 14, 16, 15, '#ffffff'); m.rect(2, 20, 16, 22, WR_G)
    m.poly([(16, 15), (20, 18), (16, 21)], WR_V); m.rect(4, 17, 9, 18, '#2a3a78'); m.rect(5, 17, 8, 17, '#7be3ff')
    m.rect(0, 16, 2, 20, WR_F); m.rect(11, 22, 13, 26, WR_VD); m.rect(10, 26, 14, 27, WR_F)
    m.line(15, 14, 15, 10, WR_G); m.set(15, 9, WR_FH)

# ---- Gebäude X ----
@motiv('gebaeude:raumhafen')
def _(m):
    boden(m); m.rect(2, 26, 29, 28, '#5e5a74'); m.rect(2, 26, 29, 26, '#8a86a0')
    for x in range(4, 29, 5): m.rect(x, 27, x + 2, 27, '#ffffff')
    rakete(m, 22, 4, 21, 3, WR_W, WR_V, flamme=False); m.rect(19, 22, 25, 25, WR_VD); m.rect(18, 25, 26, 25, WR_G)
    m.rect(23, 9, 26, 10, '#2a3a78'); m.line(26, 14, 28, 25, WR_G); m.line(18, 14, 16, 25, WR_G)
    m.rect(4, 18, 14, 26, WR_G); m.rect(4, 18, 14, 19, WR_W); m.rect(6, 21, 12, 23, '#2a3a78'); m.rect(7, 22, 11, 22, '#7be3ff'); m.rect(8, 15, 10, 17, WR_VD); m.set(9, 14, WR_FH)

@motiv('gebaeude:mondbasis')
def _(m):
    m.rect(0, 25, 31, 29, '#9a96b0'); m.rect(0, 25, 31, 25, '#c8c4d8'); m.set(4, 27, '#7a7690'); m.set(9, 28, '#7a7690'); m.set(26, 27, '#7a7690')
    m.ell(11, 22, 8, 7, '#e6e2f2'); m.rect(3, 22, 19, 25, '#b4b0c6'); m.ell(11, 22, 8, 7, '#e6e2f2'); m.rect(3, 23, 19, 25, '#b4b0c6')
    m.rect(8, 20, 14, 22, '#2a3a78'); m.rect(9, 21, 13, 21, '#7be3ff')
    m.ell(24, 23, 5, 4.5, '#e6e2f2'); m.rect(19, 23, 29, 25, '#b4b0c6'); m.rect(22, 21, 26, 22, '#2a3a78')
    m.rect(18, 22, 20, 23, '#8a86a0'); m.line(11, 15, 11, 12, WR_G); m.glimmer(11, 11, WR_FH)
    m.set(27, 4, '#ffffff'); m.set(5, 6, '#ffffff'); m.set(15, 3, '#ffffff')

@motiv('gebaeude:orbitalstation')
def _(m):
    m.set(3, 4, '#ffffff'); m.set(27, 5, '#ffffff'); m.set(6, 26, '#ffffff'); m.set(26, 27, '#ffffff')
    m.rect(13, 10, 18, 22, WR_W); m.rect(13, 10, 18, 11, '#ffffff'); m.rect(14, 13, 17, 15, '#2a3a78'); m.rect(15, 14, 16, 14, '#7be3ff')
    m.rect(11, 5, 20, 9, WR_G); m.rect(11, 23, 20, 27, WR_G)
    m.rect(0, 12, 11, 20, '#e2a830'); m.rect(0, 12, 11, 13, '#ffd23f'); m.rect(20, 12, 31, 20, '#e2a830'); m.rect(20, 12, 31, 13, '#ffd23f')
    for x in (3, 7): m.line(x, 12, x, 20, '#9a6a18')
    for x in (24, 28): m.line(x, 12, x, 20, '#9a6a18')
    m.rect(11, 15, 12, 16, WR_G); m.rect(19, 15, 20, 16, WR_G)

@motiv('gebaeude:helium3_raffinerie')
def _(m):
    boden(m); m.rect(3, 22, 28, 28, WR_G); m.rect(3, 22, 28, 23, WR_W); m.rect(3, 26, 28, 28, WR_VD)
    for x, h in ((7, 14), (15, 17), (23, 12)):
        m.rect(x - 3, 22 - h, x + 3, 22, WR_W); m.ell(x, 22 - h, 3.5, 2, '#ffffff'); m.rect(x - 3, 22 - h + 3, x + 3, 22 - h + 3, WR_V)
        m.rect(x + 1, 22 - h + 2, x + 3, 21, WR_G)
    m.rect(5, 24, 26, 24, '#7be3ff'); m.rect(9, 18, 13, 20, WR_K); m.rect(10, 19, 12, 19, '#7be3ff')
    m.rect(14, 2, 15, 9, WR_G); m.set(14, 1, '#bfe8ff')

@motiv('gebaeude:kolonie_kuppel')
def _(m):
    boden(m); m.ell(15.5, 22, 14, 18, '#bfe8ff'); m.rect(1, 22, 30, 29, '#7a7690'); m.rect(1, 25, 30, 26, '#9a96b0'); m.ell(15.5, 22, 14, 18, '#bfe8ff')
    m.rect(1, 23, 30, 28, '#7a7690'); m.rect(1, 23, 30, 23, '#9a96b0')
    m.ell(15.5, 21, 11, 14, '#d6f0ff')
    m.rect(1, 23, 30, 28, '#7a7690'); m.rect(1, 23, 30, 23, '#9a96b0')
    m.rect(8, 15, 11, 23, '#6aa86a'); m.ell(9.5, 14, 2.5, 2.5, '#4f9a4a'); m.rect(15, 18, 18, 23, '#e6e2f2'); m.rect(16, 19, 17, 20, '#2a3a78')
    m.rect(21, 17, 24, 23, '#6aa86a'); m.ell(22.5, 16, 2.5, 2.5, '#4f9a4a')
    m.set(11, 8, '#ffffff'); m.set(12, 8, '#ffffff'); m.set(10, 9, '#ffffff')

# ---- Wunder X: Weltraumaufzug ----
@motiv('wunder:weltraumaufzug')
def _(m):
    import random
    r = random.Random(7)
    for _ in range(14): m.set(r.randrange(1, 63), r.randrange(1, 40), '#ffffff')
    m.ell(32, 80, 52, 24, '#2f78b5'); m.ell(32, 82, 50, 22, '#3d9a5a')
    m.ell(14, 66, 14, 5, '#e6eef7'); m.ell(50, 68, 12, 4, '#e6eef7')
    m.rect(2, 62, 61, 63, '#2f78b5')
    m.poly([(28, 61), (30, 22), (34, 22), (36, 61)], '#b4b0c6'); m.poly([(30, 61), (31, 22), (33, 22), (34, 61)], '#ece9f5')
    m.line(31, 22, 31, 61, '#ffffff'); m.line(33, 22, 33, 61, '#b9abe3')
    for y in range(26, 60, 4): m.rect(29, y, 35, y, '#8e7cc3')
    m.rect(26, 14, 38, 22, '#ece9f5'); m.rect(26, 14, 38, 15, '#ffffff'); m.rect(26, 20, 38, 22, '#8e7cc3')
    m.rect(20, 16, 25, 18, '#e2a830'); m.rect(39, 16, 44, 18, '#e2a830'); m.rect(20, 16, 25, 16, '#ffd23f'); m.rect(39, 16, 44, 16, '#ffd23f')
    m.ell(32, 12, 6, 3, '#8e7cc3'); m.rect(31, 5, 32, 11, '#b4b0c6'); m.glimmer(31, 4, '#ffd23f')
    m.rect(29, 36, 35, 40, '#5e4f99'); m.rect(30, 37, 34, 38, '#7be3ff')
    m.rect(22, 56, 42, 62, '#8e7cc3'); m.rect(22, 56, 42, 57, '#b9abe3'); m.rect(18, 60, 46, 62, '#5e4f99')

# ======================================================================
#  ZEITALTER XI · STERNENZEITALTER  (Weiß, Kristall, Nebel)
# ======================================================================
@motiv('einheit:sternenkrieger')
def _(m):
    mensch(m, ST_W, ST_G, ST_W, ST_T, hose=ST_G, arm=ST_W, gewehr=None, rucksack=ST_D)
    m.rect(11, 15, 20, 15, ST_T); m.rect(10, 12, 12, 13, ST_Y); m.rect(19, 12, 21, 13, ST_Y)
    m.rect(23, 15, 24, 17, ST_D); m.poly([(24, 16), (25, 4), (27, 4), (28, 16)], ST_T); m.line(26, 5, 26, 15, ST_W); m.glimmer(26, 3, '#ffffff', ST_T)

@motiv('einheit:sternenkreuzer')
def _(m):
    m.poly([(0, 17), (8, 13), (24, 11), (31, 17), (24, 23), (8, 21)], ST_W)
    m.poly([(8, 13), (14, 5), (19, 5), (17, 12)], ST_G); m.poly([(8, 21), (14, 29), (19, 29), (17, 22)], ST_G)
    m.rect(6, 16, 26, 18, ST_D); m.rect(8, 17, 24, 17, ST_T); m.ell(24, 17, 2.5, 2, ST_Y); m.set(23, 16, '#ffffff')
    m.rect(0, 16, 2, 18, ST_T); m.set(0, 17, '#ffffff'); m.rect(13, 12, 14, 13, ST_Y); m.rect(13, 22, 14, 23, ST_Y)

@motiv('einheit:antimaterie_rakete')
def _(m):
    rakete(m, 15, 1, 22, 4, ST_W, ST_P, flamme=False)
    m.rect(12, 10, 19, 11, ST_D); m.ell(15.5, 15, 2.5, 2.5, ST_P); m.ell(15.5, 15, 1.5, 1.5, '#ffffff'); m.set(15, 14, ST_T)
    m.poly([(15, 23), (10, 30), (21, 30)], ST_T); m.poly([(15, 23), (13, 28), (18, 28)], '#ffffff'); m.set(15, 31, ST_T)

@motiv('einheit:nanoschwarm')
def _(m):
    import random
    r = random.Random(3)
    for _ in range(46):
        x = int(16 + r.gauss(0, 6)); y = int(18 + r.gauss(0, 6))
        m.set(x, y, ST_G if r.random() < .5 else ST_T)
    m.ell(16, 18, 7, 6, ST_G); m.ell(16, 18, 5, 4, ST_W); m.ell(16, 18, 3, 2.5, ST_T); m.set(15, 17, '#ffffff')
    for x, y in ((5, 10), (26, 8), (4, 26), (27, 25), (16, 4), (16, 30)): m.rect(x, y, x + 1, y + 1, ST_G)
    for x, y in ((9, 14), (22, 12), (8, 22), (23, 22)): m.set(x, y, ST_Y)

@motiv('einheit:schildfregatte')
def _(m):
    for y in range(3, 33):
        for x in range(0, 32):
            d = (x - 14) ** 2 + (y - 18) ** 2
            if 10.4 ** 2 <= d <= 12.4 ** 2 and x >= 12: m.set(x, y, ST_T if (x + y) % 3 else '#ffffff')
    m.poly([(2, 20), (8, 12), (24, 12), (28, 17), (24, 24), (8, 25)], ST_W)
    m.poly([(24, 12), (28, 17), (24, 24)], ST_G); m.rect(6, 17, 22, 19, ST_D); m.rect(8, 18, 20, 18, ST_T)
    m.rect(0, 16, 2, 20, ST_Y); m.set(0, 18, '#ffffff'); m.rect(9, 9, 11, 12, ST_D); m.set(10, 8, ST_Y); m.rect(15, 20, 18, 22, ST_P)

@motiv('einheit:terraformer')
def _(m):
    m.rect(5, 12, 26, 22, ST_W); m.rect(5, 12, 26, 13, '#ffffff'); m.rect(5, 19, 26, 22, ST_G)
    m.rect(8, 15, 14, 17, '#2a3a78'); m.rect(9, 16, 13, 16, ST_T); m.rect(17, 14, 24, 18, ST_D)
    m.ell(15.5, 27, 12, 3.5, '#3d9a5a'); m.ell(15.5, 27, 8, 2, '#5fbf4a'); m.set(10, 25, '#9fe08a'); m.set(22, 26, '#9fe08a')
    m.rect(4, 22, 6, 25, ST_D); m.rect(25, 22, 27, 25, ST_D); m.rect(11, 22, 20, 24, ST_P); m.rect(12, 23, 19, 23, ST_T)
    m.line(9, 8, 9, 11, ST_G); m.glimmer(9, 7, ST_Y); m.line(22, 7, 22, 11, ST_G); m.glimmer(22, 6, ST_T)

# ---- Gebäude XI ----
@motiv('gebaeude:antimaterie_fabrik')
def _(m):
    boden(m); m.rect(4, 17, 27, 28, ST_G); m.rect(4, 17, 27, 18, ST_W); m.rect(4, 26, 27, 28, ST_D)
    m.ell(15.5, 12, 11, 8, ST_W); m.rect(4, 12, 27, 18, ST_G); m.ell(15.5, 12, 11, 8, ST_W)
    m.ell(15.5, 12, 7, 5.5, ST_K); m.ell(15.5, 12, 4.5, 3.5, ST_P); m.ell(15.5, 12, 2, 1.5, '#ffffff')
    m.rect(7, 21, 24, 24, ST_K); m.rect(8, 22, 23, 22, ST_T); m.rect(8, 23, 23, 23, ST_P); m.glimmer(15, 5, '#ffffff', ST_P)

@motiv('gebaeude:terraforming_station')
def _(m):
    boden(m); m.ell(15.5, 24, 14, 4, '#3d9a5a'); m.ell(15.5, 24, 10, 2.5, '#5fbf4a')
    m.rect(12, 10, 19, 24, ST_W); m.rect(12, 10, 19, 11, '#ffffff'); m.rect(17, 11, 19, 24, ST_G)
    for y in (14, 18, 22): m.rect(12, y, 19, y, ST_T)
    m.ell(15.5, 8, 5, 3, ST_G); m.line(15, 2, 15, 6, ST_D); m.glimmer(15, 1, ST_T)
    m.rect(5, 20, 9, 23, ST_G); m.rect(22, 20, 26, 23, ST_G); m.set(7, 18, '#9fe08a'); m.set(24, 18, '#9fe08a'); m.set(7, 17, '#5fbf4a'); m.set(24, 17, '#5fbf4a')

@motiv('gebaeude:sternenwerft')
def _(m):
    boden(m); m.rect(2, 24, 29, 28, ST_D); m.rect(2, 24, 29, 25, ST_G)
    for x in (4, 24): m.rect(x, 6, x + 3, 24, ST_G); m.rect(x, 6, x + 3, 7, ST_W); m.rect(x + 2, 7, x + 3, 24, ST_D)
    m.rect(4, 6, 27, 9, ST_W); m.rect(4, 6, 27, 6, '#ffffff'); m.rect(4, 9, 27, 9, ST_D)
    m.poly([(10, 24), (11, 14), (15, 8), (20, 14), (21, 24)], ST_W); m.poly([(13, 24), (14, 14), (15, 10), (17, 14), (18, 24)], ST_G)
    m.rect(14, 17, 17, 18, ST_T); m.rect(14, 21, 17, 22, ST_P)
    m.line(8, 10, 8, 24, ST_Y); m.line(23, 10, 23, 24, ST_Y)

@motiv('gebaeude:kristallturm')
def _(m):
    boden(m)
    for (cx, h, w) in ((9, 14, 3), (22, 12, 3), (15, 24, 5)):
        m.poly([(cx - w, 28), (cx - w + 1, 28 - h + 4), (cx, 28 - h), (cx + w - 1, 28 - h + 4), (cx + w, 28)], ST_T)
        m.poly([(cx, 28 - h), (cx + w - 1, 28 - h + 4), (cx + w, 28), (cx, 28)], ST_TD)
        m.line(cx - 1, 28 - h + 5, cx - 1, 26, '#ffffff')
    m.rect(3, 27, 28, 28, ST_G); m.glimmer(15, 1, '#ffffff', ST_T); m.set(4, 8, ST_Y); m.set(27, 7, ST_Y)

@motiv('gebaeude:gravitationsschild')
def _(m):
    boden(m); m.rect(10, 18, 21, 28, ST_G); m.rect(10, 18, 21, 19, ST_W); m.rect(9, 26, 22, 28, ST_D)
    m.rect(13, 21, 18, 24, ST_K); m.rect(14, 22, 17, 23, ST_P)
    m.ell(15.5, 14, 13, 12, ST_P); m.ell(15.5, 14, 11, 10, ST_K)
    m.ell(15.5, 14, 8, 7, ST_P); m.ell(15.5, 14, 6.5, 5.5, ST_K); m.ell(15.5, 14, 3.5, 3, ST_T); m.ell(15.5, 14, 1.5, 1.5, '#ffffff')
    m.rect(10, 18, 21, 28, ST_G); m.rect(10, 18, 21, 19, ST_W); m.rect(9, 26, 22, 28, ST_D); m.rect(13, 21, 18, 24, ST_K); m.rect(14, 22, 17, 23, ST_P)

# ---- Wunder XI: Sternenarche ----
@motiv('wunder:sternenarche')
def _(m):
    import random
    r = random.Random(11)
    m.ell(14, 14, 18, 12, '#3a2f66'); m.ell(14, 14, 13, 8, '#5e4f99'); m.ell(14, 14, 7, 4, '#9a7bd6')
    for _ in range(30): m.set(r.randrange(1, 63), r.randrange(1, 40), '#ffffff')
    m.poly([(2, 34), (12, 24), (50, 24), (62, 34), (50, 44), (12, 44)], '#eef4fb')
    m.poly([(12, 24), (22, 12), (36, 12), (42, 24)], '#bcd0e6'); m.poly([(12, 44), (22, 54), (36, 54), (42, 44)], '#bcd0e6')
    m.rect(8, 32, 56, 36, '#7f9cc2'); m.rect(10, 34, 54, 34, '#7be3ff')
    for x in range(14, 52, 6): m.rect(x, 28, x + 2, 29, '#7be3ff'); m.rect(x, 39, x + 2, 40, '#7be3ff')
    m.ell(50, 34, 7, 5, '#ffe08a'); m.ell(50, 34, 4, 3, '#fff6d0'); m.set(48, 32, '#ffffff')
    m.ell(26, 20, 7, 5, '#2a3a58'); m.ell(26, 20, 5, 3, '#6fd0a0'); m.set(24, 19, '#bfe8a8'); m.set(28, 21, '#bfe8a8')
    m.rect(0, 31, 6, 37, '#7be3ff'); m.rect(0, 33, 3, 35, '#ffffff'); m.set(0, 34, '#ffffff'); m.rect(7, 29, 9, 39, '#bcd0e6')
    m.rect(22, 50, 26, 58, '#7f9cc2'); m.rect(36, 50, 40, 58, '#7f9cc2')
    for a in range(8):
        ang = a * math.pi / 4
        m.set(14 + math.cos(ang) * 22, 14 + math.sin(ang) * 14, '#ffe08a')

# ======================================================================
#  Rohstoffe (16x16)
# ======================================================================
def _kristall(m, cx, cy, c1, c2, c3):
    m.poly([(cx - 4, cy + 4), (cx - 3, cy - 2), (cx, cy - 6), (cx + 3, cy - 2), (cx + 4, cy + 4)], c1)
    m.poly([(cx, cy - 6), (cx + 3, cy - 2), (cx + 4, cy + 4), (cx, cy + 4)], c2); m.set(cx - 2, cy - 1, c3); m.set(cx - 2, cy, c3)

@motiv('rohstoff:seltene_erden')
def _(m):
    _kristall(m, 6, 10, '#d46aa8', '#9a3e7a', '#ffd0ee'); _kristall(m, 11, 11, '#6ad4d0', '#2f8f95', '#d0fffa')
    m.set(8, 3, '#ffffff'); m.set(3, 5, '#ffffff'); m.set(13, 6, '#ffffff')

@motiv('rohstoff:deuterium')
def _(m):
    m.poly([(8, 1), (13, 9), (13, 12), (11, 14), (5, 14), (3, 12), (3, 9)], '#5aa9e6'); m.poly([(8, 1), (13, 9), (13, 12), (11, 14), (8, 14)], '#2f78b5')
    m.set(6, 8, '#d6f0ff'); m.set(6, 9, '#d6f0ff'); m.set(7, 6, '#d6f0ff')
    m.rect(6, 11, 10, 12, '#ffffff'); m.set(7, 11, '#2f78b5'); m.set(9, 11, '#2f78b5')

@motiv('rohstoff:titan')
def _(m):
    m.poly([(2, 12), (4, 5), (9, 3), (14, 7), (13, 13)], '#9aa6b8'); m.poly([(9, 3), (14, 7), (13, 13), (8, 13)], '#6a768a')
    m.poly([(4, 5), (9, 3), (10, 5), (5, 7)], '#d8dfe8'); m.rect(5, 9, 6, 10, '#d8dfe8'); m.rect(10, 9, 11, 10, '#4a5468')
    m.set(8, 7, '#ffffff')

@motiv('rohstoff:helium3')
def _(m):
    m.ell(8, 9, 5, 5.5, '#e6eef7'); m.ell(8, 9, 3.5, 4, '#bfe8ff'); m.set(6, 7, '#ffffff'); m.set(7, 6, '#ffffff')
    m.rect(6, 3, 9, 4, '#7f9cc2'); m.rect(7, 2, 8, 2, '#7f9cc2'); m.rect(5, 9, 11, 9, '#8e7cc3'); m.rect(7, 8, 9, 10, '#5e4f99')
    m.set(7, 9, '#ffffff'); m.set(8, 9, '#ffffff')

# ======================================================================
#  Zeitalter-Symbole VIII–XI (16x16)
# ======================================================================
def _ikon(m, rand, innen, glanz, zeichen):
    m.rect(1, 1, 14, 14, rand); m.rect(2, 2, 13, 13, innen); m.rect(2, 2, 13, 2, glanz); m.rect(2, 2, 2, 13, glanz)
    for (x, y, c) in zeichen: m.set(x, y, c)

@motiv('za:7')       # KI: Chip mit Schaltkreislinien
def _(m):
    m.rect(1, 1, 14, 14, '#2d3a66'); m.rect(2, 2, 13, 13, '#5b8cff'); m.rect(2, 2, 13, 2, '#a6c4ff'); m.rect(2, 2, 2, 13, '#a6c4ff')
    m.rect(5, 5, 10, 10, '#1d2748'); m.rect(6, 6, 9, 9, '#4ee3ff'); m.rect(7, 7, 8, 8, '#ffffff')
    for p in (4, 7, 10): m.set(p, 3, '#e4eaf5'); m.set(p, 12, '#e4eaf5'); m.set(3, p, '#e4eaf5'); m.set(12, p, '#e4eaf5')

@motiv('za:8')       # Fusion: Plasmaring
def _(m):
    m.rect(1, 1, 14, 14, '#7a4a14'); m.rect(2, 2, 13, 13, '#f2a33a'); m.rect(2, 2, 13, 2, '#ffd27a'); m.rect(2, 2, 2, 13, '#ffd27a')
    m.ell(7.5, 7.5, 4.8, 4.8, '#e8553a'); m.ell(7.5, 7.5, 3.4, 3.4, '#ffd27a'); m.ell(7.5, 7.5, 1.6, 1.6, '#fff1c2'); m.set(5, 5, '#ffffff')

@motiv('za:9')       # Weltraum: Ringplanet
def _(m):
    m.rect(1, 1, 14, 14, '#2f2858'); m.rect(2, 2, 13, 13, '#8e7cc3'); m.rect(2, 2, 13, 2, '#b9abe3'); m.rect(2, 2, 2, 13, '#b9abe3')
    m.ell(7.5, 7.5, 3.2, 3.2, '#ece9f5'); m.ell(7.5, 8.2, 6, 1.6, '#262142'); m.ell(7.5, 8.2, 5.2, 1.0, '#ffd23f')
    m.ell(7.5, 7.5, 3.2, 2.1, '#ece9f5'); m.set(6, 6, '#ffffff'); m.set(3, 3, '#ffffff'); m.set(12, 11, '#ffffff')

@motiv('za:10')      # Sterne: Vierzack-Stern
def _(m):
    m.rect(1, 1, 14, 14, '#3a5078'); m.rect(2, 2, 13, 13, '#e6eef7'); m.rect(2, 2, 13, 2, '#ffffff'); m.rect(2, 2, 2, 13, '#ffffff')
    m.poly([(7.5, 2), (9, 6), (13, 7.5), (9, 9), (7.5, 13), (6, 9), (2, 7.5), (6, 6)], '#7be3ff')
    m.poly([(7.5, 4), (8.4, 6.6), (11, 7.5), (8.4, 8.4), (7.5, 11), (6.6, 8.4), (4, 7.5), (6.6, 6.6)], '#ffffff'); m.set(7, 7, '#ffe08a')

# ======================================================================
#  Register
# ======================================================================
GROESSE = lambda k: (64, 64) if k.startswith('wunder:') else (16, 16) if k.startswith(('rohstoff:', 'za:')) else (64, 56) if k.startswith('stadt:') else (32, 32)

def lade():
    import zukunft_spr2  # noqa  (erste Fassung, nur noch als Rückfall)
    from zk_basis import Bild
    import zk_einheiten, zk_gebaeude, zk_welt          # zweite Fassung im Stil der alten Sprites
    for mod in (zk_einheiten, zk_gebaeude, zk_welt): REG.update(mod.NEU)
    for key, fn in REG.items():
        w, h = GROESSE(key); m = Bild(w, h); fn(m)
        import rand
        spr._S[key] = rand.repariere_sprite(key, m.fertig(kontur=not key.startswith('za:')))
    for r in ('seltene_erden', 'deuterium', 'titan', 'helium3'): spr._S['ui:' + r] = spr._S['rohstoff:' + r]

def webexport(pfad, praefixe=None):
    """Fügt alle neuen Sprites in die sprites.json der Website ein (Palette-String-Format)."""
    out = {}
    for key in list(REG) + ['ui:' + r for r in ('seltene_erden', 'deuterium', 'titan', 'helium3')]:
        sp = spr._S[key]; pal = []; d = ''
        for c in sp['feld']:
            if c is None: d += '.'; continue
            if c not in pal: pal.append(c)
            d += chr(48 + pal.index(c))
        out[key] = dict(w=sp['w'], h=sp['h'], p=pal, d=d)
    b = json.load(open(pfad)); b.update(out); json.dump(b, open(pfad, 'w'), separators=(',', ':')); return len(out)
