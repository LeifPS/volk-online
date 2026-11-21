"""Zukunfts-Sprites Teil 2: Volkskarten-Motive VIII bis XI (20 Stück) und Stadt-Optik je Zeitalter (VIII bis XI, je 3 Größen)."""
import math, random
from px import Px, OUT, mixc, hell, dunkel
from zukunft_spr import *
from zukunft_spr import motiv, boden, rakete, mensch, knarre, raupen

# ====================== Volkskarten · Gebäude ======================
def warte(m, w, g, d, glow, hoch=1):
    boden(m); m.rect(5, 20, 26, 28, g); m.rect(5, 20, 26, 21, w); m.rect(5, 26, 26, 28, d)
    m.ell(15.5, 19, 9, 9, w); m.rect(5, 19, 26, 28, g); m.ell(15.5, 19, 9, 9, w)
    m.rect(5, 20, 26, 28, g); m.rect(5, 20, 26, 21, w); m.rect(5, 26, 26, 28, d)
    m.poly([(12, 12), (20, 12), (24, 5), (16, 3)], d); m.rect(18, 4, 27, 7, g); m.rect(25, 3, 29, 8, glow)
    m.rect(11, 14, 20, 17, glow); m.rect(12, 15, 19, 15, hell(glow, .5))

@motiv('gebaeude:sd_ki_observatorium')
def _(m): warte(m, KI_W, KI_G, KI_D, KI_C)
@motiv('gebaeude:sd_quantenwarte')
def _(m):
    warte(m, FU_W, FU_G, FU_D, FU_O); m.glimmer(8, 10, FU_OH); m.glimmer(24, 12, FU_OH)
@motiv('gebaeude:sd_orbitalteleskop')
def _(m):
    m.set(3, 4, '#ffffff'); m.set(28, 6, '#ffffff'); m.set(6, 27, '#ffffff')
    m.rect(8, 10, 23, 19, WR_W); m.rect(8, 10, 23, 11, '#ffffff'); m.rect(8, 17, 23, 19, WR_G); m.ell(23, 14.5, 3, 5.5, '#2a3a78'); m.ell(23, 14.5, 1.5, 3.5, '#7be3ff')
    m.rect(0, 11, 6, 18, '#e2a830'); m.rect(0, 11, 6, 12, '#ffd23f'); m.rect(25, 22, 31, 29, '#e2a830'); m.rect(25, 22, 31, 23, '#ffd23f')
    m.rect(14, 19, 17, 22, WR_VD); m.rect(10, 22, 21, 24, WR_V); m.line(12, 24, 12, 27, WR_G); m.line(19, 24, 19, 27, WR_G)
@motiv('gebaeude:sd_sternenpforte')
def _(m):
    boden(m); m.rect(3, 27, 28, 28, ST_D)
    m.ell(15.5, 16, 12, 12, ST_W); m.ell(15.5, 16, 8.5, 8.5, ST_K); m.ell(15.5, 16, 7, 7, ST_P); m.ell(15.5, 16, 5, 5, ST_T); m.ell(15.5, 16, 2.5, 2.5, '#ffffff')
    m.rect(3, 22, 28, 28, ST_G); m.rect(3, 26, 28, 28, ST_D); m.rect(3, 22, 8, 23, ST_W); m.rect(23, 22, 28, 23, ST_W)
    m.glimmer(15, 3, ST_Y); m.set(6, 6, ST_Y); m.set(25, 6, ST_Y)

@motiv('gebaeude:nl_ki_hafen')
def _(m):
    boden(m); m.rect(0, 25, 31, 29, '#2f78b5'); m.rect(0, 25, 31, 25, '#5aa9e6')
    m.rect(2, 22, 29, 25, KI_D); m.rect(2, 22, 29, 22, KI_G)
    m.rect(5, 10, 8, 22, KI_G); m.rect(5, 9, 18, 10, KI_W); m.rect(15, 10, 18, 22, KI_G); m.rect(6, 11, 7, 13, KI_C)
    m.line(17, 11, 26, 20, KI_D); m.line(18, 11, 27, 20, KI_D); m.rect(25, 19, 29, 22, '#c9915a'); m.rect(25, 19, 29, 19, '#e0b07a')
    m.rect(10, 16, 13, 22, KI_B); m.set(11, 17, KI_C); m.line(7, 7, 7, 9, KI_D); m.glimmer(7, 6, KI_C)
@motiv('gebaeude:nl_orbitalwerft')
def _(m):
    boden(m); m.rect(2, 24, 29, 28, WR_VD); m.rect(2, 24, 29, 24, WR_V)
    for x in (4, 24): m.rect(x, 8, x + 3, 24, WR_G); m.rect(x, 8, x + 3, 9, WR_W)
    m.rect(4, 8, 27, 11, WR_W); m.rect(4, 11, 27, 11, WR_G)
    m.poly([(11, 24), (11, 17), (15, 12), (20, 17), (20, 24)], WR_W); m.rect(14, 16, 17, 18, '#2a3a78'); m.rect(15, 17, 16, 17, '#7be3ff')
    m.rect(9, 20, 10, 24, WR_F); m.rect(21, 20, 22, 24, WR_F)
@motiv('gebaeude:sv_gewaechshaus')
def _(m):
    boden(m); m.rect(3, 14, 28, 28, '#cfe8d8'); m.poly([(3, 14), (15.5, 4), (28, 14)], '#bfe8d0'); m.rect(3, 14, 28, 14, KI_G); m.rect(3, 27, 28, 28, KI_D)
    for x in (9, 15, 21): m.line(x, 14, x, 27, KI_G)
    m.line(3, 14, 15, 4, KI_G); m.line(28, 14, 16, 4, KI_G)
    for x in (5, 11, 17, 23): m.rect(x, 20, x + 3, 27, '#4f9a4a'); m.rect(x, 20, x + 3, 21, '#8fd87a'); m.set(x + 1, 22, '#ffd23f')
    m.rect(6, 8, 7, 9, KI_B)
@motiv('gebaeude:sv_sonnenreaktor')
def _(m):
    boden(m); m.rect(4, 21, 27, 28, FU_G); m.rect(4, 21, 27, 22, FU_W); m.rect(4, 26, 27, 28, FU_D)
    m.ell(15.5, 20, 11, 15, '#ffd27a'); m.rect(4, 21, 27, 28, FU_G); m.rect(4, 21, 27, 22, FU_W); m.rect(4, 26, 27, 28, FU_D)
    m.ell(15.5, 12, 8, 8, '#ffd23f'); m.ell(15.5, 12, 5.5, 5.5, FU_O); m.ell(15.5, 12, 2.5, 2.5, FU_OO)
    for a in range(10): ang = a * math.pi / 5; m.set(15.5 + math.cos(ang) * 11, 12 + math.sin(ang) * 11, FU_OH)
    m.rect(4, 21, 27, 28, FU_G); m.rect(4, 21, 27, 22, FU_W); m.rect(4, 26, 27, 28, FU_D); m.rect(11, 23, 20, 25, FU_K); m.rect(12, 24, 19, 24, FU_O)
@motiv('gebaeude:sv_gartenwelt')
def _(m):
    boden(m); m.ell(15.5, 12, 13, 11, '#cfe8ff'); m.rect(2, 12, 29, 28, '#7a7690'); m.ell(15.5, 12, 13, 11, '#d6f0ff')
    m.ell(15.5, 12, 10, 8, '#e8f6ff'); m.rect(2, 20, 29, 28, '#7a7690'); m.rect(2, 20, 29, 21, '#9a96b0')
    m.ell(9, 19, 5, 4, '#4f9a4a'); m.ell(22, 19, 5, 4, '#4f9a4a'); m.ell(15.5, 17, 4, 5, '#6fc060')
    m.rect(14, 14, 17, 20, '#8a5a2b'); m.ell(15.5, 12, 4.5, 4, '#3d8a3d'); m.set(14, 11, '#ff8a8a'); m.set(17, 12, '#ffd23f'); m.set(15, 14, '#ff8a8a')
    m.set(5, 17, '#ff8aa8'); m.set(26, 18, '#ffd23f')
@motiv('gebaeude:gb_quantenboerse')
def _(m):
    boden(m); m.rect(4, 12, 27, 28, '#c8d2e6'); m.rect(4, 12, 27, 13, '#ffffff'); m.rect(4, 26, 27, 28, '#8a96b4')
    m.rect(7, 15, 24, 24, '#222a40'); m.rect(7, 15, 24, 15, FU_O)
    m.line(8, 22, 12, 19, '#5fbf4a'); m.line(12, 19, 15, 21, '#5fbf4a'); m.line(15, 21, 19, 17, '#5fbf4a'); m.line(19, 17, 23, 18, '#5fbf4a')
    m.line(8, 17, 12, 20, FU_R); m.line(12, 20, 17, 18, FU_R); m.line(17, 18, 23, 22, FU_R)
    m.rect(10, 7, 21, 11, '#e6c25a'); m.rect(10, 7, 21, 7, '#fff0a0'); m.rect(13, 8, 18, 10, '#222a40'); m.rect(14, 9, 17, 9, FU_OH)
@motiv('gebaeude:gb_sternenmarkt')
def _(m):
    boden(m); m.rect(2, 25, 29, 28, ST_D); m.rect(2, 25, 29, 25, ST_G)
    for i, (x, c) in enumerate(((3, ST_P), (11, ST_T), (19, ST_Y))):
        m.rect(x, 14, x + 8, 25, ST_W); m.rect(x, 14, x + 8, 15, c); m.poly([(x - 1, 14), (x + 4, 8), (x + 9, 14)], c)
        m.rect(x + 2, 18, x + 6, 25, ST_K); m.rect(x + 3, 19, x + 5, 20, ST_Y)
    m.glimmer(7, 5, ST_Y); m.glimmer(15, 3, '#ffffff', ST_T); m.glimmer(23, 5, ST_Y)
@motiv('gebaeude:sr_plasmaschmiede')
def _(m):
    boden(m); m.rect(4, 14, 27, 28, FU_D); m.rect(4, 14, 27, 15, FU_G); m.rect(4, 26, 27, 28, FU_K)
    m.poly([(4, 14), (8, 8), (23, 8), (27, 14)], FU_K); m.rect(8, 8, 23, 9, FU_G)
    m.rect(8, 17, 23, 25, FU_K); m.rect(9, 18, 22, 24, FU_R); m.rect(10, 19, 21, 23, FU_O); m.rect(12, 20, 19, 22, FU_OH); m.rect(14, 21, 17, 21, FU_OO)
    m.rect(13, 2, 18, 8, FU_D); m.glimmer(15, 1, FU_OH, FU_O)
    for x in (6, 24): m.rect(x, 22, x + 1, 27, FU_G)

# ====================== Volkskarten · Einheiten ======================
@motiv('einheit:nl_fusionsschiff')
def _(m):
    m.poly([(1, 21), (5, 25), (27, 25), (31, 19), (27, 17), (5, 17)], '#2d4a78'); m.rect(2, 20, 30, 23, '#5aa9e6'); m.rect(2, 20, 30, 20, '#d6f0ff')
    m.poly([(0, 19), (3, 19), (3, 25), (1, 22)], FU_W); m.rect(9, 11, 21, 17, FU_W); m.rect(9, 11, 21, 12, '#ffffff'); m.rect(12, 13, 18, 14, FU_K)
    m.ell(15, 9, 3, 2.5, FU_O); m.set(14, 8, FU_OO); m.rect(24, 14, 29, 17, FU_G); m.rect(24, 14, 29, 14, FU_W); m.rect(5, 24, 27, 25, '#2f78b5')
@motiv('einheit:nl_sternensegler')
def _(m):
    m.poly([(2, 23), (6, 27), (26, 27), (30, 22)], ST_D); m.rect(3, 22, 29, 24, ST_W); m.rect(4, 24, 28, 26, ST_G)
    m.line(15, 22, 15, 3, ST_D)
    m.poly([(16, 4), (28, 20), (16, 20)], ST_T); m.poly([(16, 4), (22, 13), (16, 13)], '#ffffff')
    m.poly([(14, 8), (5, 20), (14, 20)], ST_Y); m.poly([(14, 8), (10, 14), (14, 14)], '#fff6d0'); m.glimmer(15, 2, '#ffffff', ST_T)
@motiv('einheit:sv_mondgaertner')
def _(m):
    mensch(m, WR_W, WR_G, WR_W, '#7be3ff', hose=WR_G, arm=WR_W, gewehr=None, rucksack='#4f9a4a')
    m.rect(22, 20, 26, 27, '#8a5a2b'); m.rect(21, 18, 27, 20, '#4f9a4a'); m.set(22, 17, '#ff8aa8'); m.set(25, 17, '#ffd23f'); m.set(24, 16, '#6fc060')
    m.ell(15.5, 8.5, 4.3, 4.3, WR_W); m.rect(13, 7, 19, 10, '#2a3a78'); m.rect(14, 8, 18, 8, '#7be3ff')
@motiv('einheit:gb_lieferflotte')
def _(m):
    for (x, y) in ((3, 7), (14, 3), (20, 13), (6, 17)):
        m.rect(x, y, x + 5, y + 1, KI_W); m.rect(x + 1, y + 1, x + 4, y + 2, KI_D); m.rect(x - 1, y - 1, x + 6, y - 1, KI_BH)
        m.rect(x + 1, y + 3, x + 4, y + 6, '#e6c25a'); m.rect(x + 1, y + 3, x + 4, y + 3, '#fff0a0'); m.set(x + 2, y + 1, KI_C)
    m.rect(3, 26, 28, 27, KI_D); m.rect(3, 26, 28, 26, KI_G); m.rect(10, 21, 22, 25, '#e6c25a'); m.rect(10, 21, 22, 21, '#fff0a0'); m.rect(15, 21, 16, 25, '#9a6a18')
@motiv('einheit:gb_orbitalfrachter')
def _(m):
    m.rect(3, 12, 26, 22, WR_W); m.rect(3, 12, 26, 13, '#ffffff'); m.rect(3, 20, 26, 22, WR_G)
    for i, x in enumerate((5, 11, 17)): m.rect(x, 14, x + 4, 19, ['#e6c25a', '#c9915a', '#9a96b0'][i]); m.rect(x, 14, x + 4, 14, '#ffffff')
    m.poly([(26, 13), (31, 17), (26, 21)], WR_V); m.rect(27, 16, 29, 17, '#7be3ff'); m.rect(0, 14, 2, 20, WR_F); m.rect(0, 16, 1, 18, WR_FH)
    m.rect(8, 22, 10, 25, WR_VD); m.rect(18, 22, 20, 25, WR_VD)
@motiv('einheit:sr_roboterreiter')
def _(m):
    m.rect(5, 20, 9, 28, KI_D); m.rect(20, 20, 24, 28, KI_D); m.rect(4, 28, 10, 29, KI_K); m.rect(19, 28, 25, 29, KI_K)
    m.rect(4, 12, 26, 21, KI_G); m.rect(4, 12, 26, 13, KI_W); m.rect(4, 18, 26, 21, KI_D)
    m.poly([(22, 13), (30, 6), (30, 12), (26, 15)], KI_G); m.rect(28, 7, 29, 8, KI_C)
    m.rect(11, 5, 17, 11, KI_W); m.rect(12, 7, 16, 8, KI_C); m.rect(13, 11, 15, 12, KI_G); m.rect(8, 10, 9, 14, KI_B)
    m.rect(17, 9, 23, 10, KI_D); m.rect(22, 7, 24, 12, KI_C)
@motiv('einheit:sr_marsreiter')
def _(m):
    m.ell(8, 25, 4, 4, '#4a4658'); m.ell(8, 25, 1.8, 1.8, '#9a96b0'); m.ell(24, 25, 4, 4, '#4a4658'); m.ell(24, 25, 1.8, 1.8, '#9a96b0')
    m.rect(3, 15, 29, 23, '#b5532c'); m.rect(3, 15, 29, 16, '#d97a4a'); m.rect(3, 21, 29, 23, '#8a3a1c')
    m.poly([(22, 15), (30, 9), (31, 15)], '#d97a4a'); m.rect(24, 11, 27, 13, '#2a3a78'); m.rect(25, 12, 26, 12, '#7be3ff')
    mensch_klein(m)
def mensch_klein(m):
    m.rect(9, 7, 14, 14, WR_W); m.ell(11.5, 5, 3, 3, WR_W); m.rect(11, 4, 14, 6, '#2a3a78'); m.rect(14, 10, 19, 11, WR_G); m.rect(19, 9, 20, 12, WR_F)
@motiv('einheit:sr_sternenhorde')
def _(m):
    for (x, y, k) in ((3, 12, 0), (13, 7, 1), (22, 14, 2)):
        m.poly([(x, y + 4), (x + 3, y), (x + 8, y), (x + 9, y + 3), (x + 5, y + 6)], ST_W); m.poly([(x + 3, y), (x + 8, y), (x + 9, y + 3), (x + 6, y + 2)], ST_G)
        m.rect(x + 3, y + 2, x + 6, y + 3, ST_T); m.rect(x - 2, y + 3, x - 1, y + 4, ST_Y); m.set(x - 3, y + 3, '#ffffff')
        m.rect(x + 1, y + 6, x + 7, y + 6, ST_D)
    m.rect(2, 26, 29, 27, ST_D); m.rect(2, 26, 29, 26, ST_G); m.rect(8, 22, 22, 25, ST_P); m.rect(9, 23, 21, 23, ST_T)

# ====================== Städte (64x56) ======================
def _basis(m, farbe='#8a8a96', licht='#b8b8c8'):
    for y, rx in ((50, 26), (49, 28), (48, 29), (47, 30)): m.ell(32, y, rx, 4, farbe)
    m.ell(32, 47, 30, 6, farbe); m.ell(32, 46, 28, 4.5, licht)

def _turm(m, cx, y0, w, h, farbe, dunkel_, fenster, krone=None, glas=False):
    m.rect(cx, y0 - h, cx + w, y0, farbe); m.rect(cx + w - 2, y0 - h, cx + w, y0, dunkel_); m.rect(cx, y0 - h, cx + w, y0 - h, hell(farbe, .45))
    for yy in range(y0 - h + 3, y0 - 1, 3):
        for xx in range(cx + 2, cx + w - 2, 3): m.set(xx, yy, fenster if (xx + yy) % 2 == 0 else mixc(fenster, dunkel_, .5))
    if krone == 'antenne': m.rect(cx + w // 2, y0 - h - 5, cx + w // 2, y0 - h - 1, dunkel_); m.set(cx + w // 2, y0 - h - 6, '#ff6a6a')
    elif krone == 'garten': m.rect(cx - 1, y0 - h - 2, cx + w + 1, y0 - h, '#4f9a4a'); m.rect(cx, y0 - h - 3, cx + w, y0 - h - 2, '#6fc060'); m.set(cx + 2, y0 - h - 4, '#ff8aa8')

def _kuppel(m, cx, y0, r, farbe, band, glow):
    m.ell(cx, y0, r, r * .95, farbe)
    m.rect(cx - r, y0, cx + r, y0 + 5, mixc(farbe, '#000000', .12)); m.rect(cx - r, y0 + 1, cx + r, y0 + 1, band)
    m.rect(cx - r + 2, y0 + 3, cx + r - 2, y0 + 3, glow); m.set(cx - r // 2, y0 - r // 2, '#ffffff'); m.set(cx - r // 2 + 1, y0 - r // 2, '#ffffff')
    for k in range(0, 181, 6):                                   # dunkler Rand je Kuppel, damit Kuppeln nicht verschmelzen
        a = math.radians(180 + k); m.set(cx + math.cos(a) * (r + 1), y0 + math.sin(a) * (r * .95 + 1), '#6f6a5e')
    m.rect(cx - r - 1, y0, cx - r - 1, y0 + 5, '#6f6a5e'); m.rect(cx + r + 1, y0, cx + r + 1, y0 + 5, '#6f6a5e')

def stadt_ki(m, g):
    _basis(m, '#8895ad', '#b8c4da')
    plan = [(30, 12, 22), (16, 8, 16), (42, 9, 17), (10, 8, 11), (50, 8, 12), (22, 7, 13), (36, 7, 12)][:[3, 5, 7][g - 1]]
    for (x, w, h) in sorted(plan, key=lambda p: p[2]):
        _turm(m, x, 44 if x > 30 else 45, w, h, KI_W if x % 2 else '#cdd7ea', KI_G, KI_B, krone='garten' if x % 3 else 'antenne')
    for (x, y) in ((8, 14), (52, 20), (30, 6)): m.rect(x, y, x + 3, y, KI_G); m.set(x + 1, y + 1, KI_C)
    m.rect(26, 43, 38, 46, KI_G)

def stadt_fusion(m, g):
    _basis(m, '#a89c88', '#d6cdb8')
    # Fusionsturm in der Mitte (leuchtender Reaktor) hinter den Kuppeln
    m.rect(29, 14, 35, 40, FU_G); m.rect(29, 14, 35, 15, FU_W); m.rect(34, 15, 35, 40, FU_D); m.ell(32, 22, 6, 6, FU_O); m.ell(32, 22, 4, 4, FU_OH); m.ell(32, 22, 2, 2, FU_OO)
    m.rect(26, 38, 38, 42, FU_W)
    plan = [(32, 11), (14, 9), (50, 9), (22, 8), (42, 8), (6, 6), (58, 6)][:[3, 5, 7][g - 1]]
    plan = [p for p in plan if p[0] != 32] if g >= 2 else plan
    for (x, r) in sorted(plan, key=lambda p: -p[1]): _kuppel(m, x, 44 - r // 2, r, FU_W, FU_G, FU_O)
    m.rect(8, 48, 56, 48, FU_O); m.rect(10, 49, 54, 49, FU_OH)

def stadt_weltraum(m, g):
    _basis(m, '#7a7690', '#aaa6c0')
    for (x, r) in sorted([(14, 8), (50, 9)], key=lambda p: p[1])[:1 + (g > 1)]: _kuppel(m, x, 42, r, '#d6f0ff', WR_G, WR_V)
    rakete(m, 32, 6 if g == 3 else 14, 40, 4, WR_W, WR_V, flamme=False); m.rect(28, 41, 36, 45, WR_VD); m.rect(26, 45, 38, 45, WR_G)
    m.line(36, 16, 44, 40, WR_G) if g >= 2 else None
    if g >= 2: m.rect(40, 36, 48, 44, WR_W); m.rect(40, 36, 48, 37, '#ffffff'); m.rect(42, 40, 46, 41, '#2a3a78')
    if g >= 3: m.rect(4, 34, 10, 44, WR_G); m.rect(4, 34, 10, 35, WR_W); m.rect(6, 28, 8, 34, WR_VD); m.glimmer(7, 27, WR_FH)
    for (x, y) in ((8, 8), (56, 12), (50, 4)): m.set(x, y, '#ffffff')

def stadt_sterne(m, g):
    _basis(m, '#8aa0bd', '#c4d6ea')
    kr = [(32, 40, 5), (18, 28, 4), (46, 30, 4), (10, 20, 3), (54, 22, 3), (25, 22, 3), (39, 24, 3)][:[3, 5, 7][g - 1]]
    for (cx, h, w) in sorted(kr, key=lambda p: p[1]):
        y0 = 45 if cx > 30 else 46
        m.poly([(cx - w, y0), (cx - w + 1, y0 - h + 6), (cx, y0 - h), (cx + w - 1, y0 - h + 6), (cx + w, y0)], ST_T)
        m.poly([(cx, y0 - h), (cx + w - 1, y0 - h + 6), (cx + w, y0), (cx, y0)], ST_TD); m.line(cx - 1, y0 - h + 8, cx - 1, y0 - 3, '#ffffff')
    if g >= 2:
        for (x, y) in ((8, 36), (50, 40)): m.ell(x + 3, y, 6, 1.6, ST_W); m.rect(x, y, x + 6, y + 1, ST_G); m.set(x + 3, y - 3, ST_Y); m.line(x + 3, y - 2, x + 3, y, ST_D)
    for (x, y) in ((6, 8), (58, 10), (30, 4), (16, 14)): m.glimmer(x, y, ST_Y) if x % 2 == 0 else m.set(x, y, '#ffffff')

for _g in (1, 2, 3):
    for _z, _f in ((7, stadt_ki), (8, stadt_fusion), (9, stadt_weltraum), (10, stadt_sterne)):
        def _mk(m, f=_f, g=_g): f(m, g)
        motiv('stadt:stadt@%d@%d' % (_z, _g))(_mk)
