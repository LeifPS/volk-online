"""Einheiten der Zeitalter VIII–XI, zweite Fassung (32x32, Stil der alten Sprites)."""
from zk_basis import *

NEU = {}
def motiv(key):
    def deko(fn): NEU[key] = fn; return fn
    return deko


def panzer(m, rumpf, rumpf_d, turm, rohr_c, akzent, kette=True, schweben=False, rohr_l=10, camo=None):
    if kette:
        m.kette(4, 27, 25, 30)
    if schweben:
        m.platte(5, 25, 26, 26, rumpf_d)
        for x in (7, 12, 19, 24):
            m.rect(x - 1, 27, x + 1, 27, akzent); m.set(x, 28, hell(akzent, .5)); m.set(x, 29, hell(akzent, .75))
    # Wanne
    m.ppoly([(3, 24), (6, 19), (27, 19), (29, 22), (28, 24)], rumpf)
    m.rect(5, 23, 27, 24, rumpf_d)
    m.rect(8, 21, 22, 21, 'S'); m.rect(8, 22, 22, 22, 'S-')
    if camo:
        for (x, y) in camo: m.set(x, y, rumpf_d)
    # Turm
    m.ppoly([(9, 18), (11, 13), (21, 13), (23, 16), (23, 18)], turm)
    m.rect(10, 17, 23, 18, dunkel(turm, .25))
    m.rect(22, 15, 22 + rohr_l, 16, rohr_c); m.rect(22, 15, 22 + rohr_l, 15, hell(rohr_c, .3))
    m.rect(13, 14, 16, 15, akzent); m.set(13, 14, hell(akzent, .5))


# ======================= VIII · KI-Zeitalter =======================
@motiv('einheit:exoskelett_infanterie')
def _(m):
    figur(m, ruest=KG1, helm=KG2, visier=KC, hose=KG2, stiefel=KG4, rucksack=KG3, schulter=KG1,
          waffe=gewehr(KG4, KC, 8))
    # Exoskelett-Streben an Beinen und Rücken
    for y in (23, 26): m.set(12, y, KC); m.set(18, y, KC)
    m.rect(9, 11, 9, 13, KG4); m.set(9, 10, KC)
    m.rect(11, 19, 11, 21, KG4)


@motiv('einheit:kampfroboter')
def _(m):
    # Beine (Zweibeiner mit Knie nach hinten)
    for bx, c in ((10, KG3), (17, KG2)):
        m.rect(bx, 21, bx + 3, 24, c); m.rect(bx - 1, 25, bx + 2, 28, c); m.platte(bx - 2, 29, bx + 4, 30, KG4)
        m.kugel(bx + 1.5, 24.5, 1.6, 1.6, M3, glanz=False)
    # Rumpf
    m.ppoly([(7, 20), (8, 10), (23, 10), (25, 15), (24, 20)], KG1)
    m.rect(8, 19, 24, 20, KG3)
    m.rect(11, 12, 19, 16, KG4); m.rect(12, 13, 18, 13, KC); m.rect(12, 14, 18, 15, KB); m.set(15, 14, KCH)
    m.rect(8, 17, 22, 17, 'S'); m.rect(8, 18, 22, 18, 'S-')
    # Kopf
    m.kugel(15.5, 6.5, 4.2, 3.3, KG2); m.rect(15, 6, 20, 7, KG4); m.rect(16, 6, 19, 6, KC); m.set(20, 6, KCH)
    m.line(12, 3, 11, 0, M3); m.set(11, 0, KC)
    # Waffenarm
    m.platte(23, 12, 26, 18, KG2); m.rect(26, 13, 31, 15, KG3); m.rect(26, 13, 31, 13, KG1); m.set(31, 14, KC)
    m.platte(4, 12, 7, 18, KG3); m.rect(4, 19, 6, 21, KG4)


@motiv('einheit:drohnenschwarm')
def _(m):
    def drohne(cx, cy, gross=1):
        m.rect(cx - 4, cy - 1, cx - 2, cy - 1, M3); m.rect(cx + 2, cy - 1, cx + 4, cy - 1, M3)
        m.set(cx - 3, cy - 2, M4); m.set(cx + 3, cy - 2, M4)
        m.kugel(cx, cy, 2.2, 1.6, KG1, glanz=False); m.set(cx, cy + 1, KC); m.set(cx - 1, cy, 'S')
    for p in ((7, 5), (19, 4), (27, 9), (12, 11), (5, 16), (22, 15), (14, 20), (27, 21), (8, 24)): drohne(*p)
    for x, y in ((7, 7), (12, 13), (22, 17), (14, 22)): m.set(x, y + 1, KCH)
    m.schatten(16, 29, 10)


@motiv('einheit:autonomer_panzer')
def _(m):
    panzer(m, KG1, KG3, KG2, KG3, KC, rohr_l=9)
    m.rect(24, 17, 26, 17, KC)                                    # Sensorleiste
    m.line(18, 12, 18, 9, M3); m.set(18, 8, KC); m.rect(10, 11, 12, 12, KG3); m.set(11, 11, KC)
    for x in (6, 10, 14, 18, 22): m.set(x, 20, KG2)


@motiv('einheit:drohnenjaeger')
def _(m):
    # Draufsicht, nach rechts, mit Schatten
    m.schatten(15, 29, 11)
    m.ppoly([(3, 14), (9, 12), (24, 12), (30, 14), (24, 16), (9, 16)], KG1)          # Rumpf
    m.ppoly([(11, 12), (17, 3), (20, 3), (19, 12)], KG2)                               # Flügel oben
    m.ppoly([(11, 16), (19, 16), (20, 25), (17, 25)], KG3)                              # Flügel unten
    m.ppoly([(3, 12), (6, 8), (8, 8), (7, 12)], KG2); m.ppoly([(3, 16), (7, 16), (8, 20), (6, 20)], KG3)
    m.rect(21, 13, 25, 14, KC); m.rect(22, 13, 24, 13, KCH)
    m.rect(17, 5, 18, 5, 'S'); m.rect(17, 22, 18, 22, 'S'); m.rect(12, 14, 18, 14, 'S-')
    m.flamme(2, 14, 3, 'l', 0)


@motiv('einheit:lieferdrohnen')
def _(m):
    for (cx, cy) in ((10, 9), (22, 17)):
        for dx in (-6, 6):
            m.rect(cx + dx - 3, cy - 4, cx + dx + 3, cy - 4, M2); m.set(cx + dx, cy - 3, M4)
        m.rect(cx - 6, cy - 3, cx + 6, cy - 3, KG3)
        m.kugel(cx, cy - 1, 3.5, 2.2, M2); m.set(cx + 2, cy - 1, KC)
        m.line(cx, cy + 1, cx, cy + 2, M4)
        m.kasten(cx - 3, cy + 6, 6, 4, 2, '#c99a5e')                               # Paket
        m.rect(cx - 3, cy + 4, cx + 2, cy + 4, '#a87a42'); m.rect(cx - 1, cy + 3, cx, cy + 6, 'S')
    m.schatten(16, 29, 9)


# ======================= IX · Fusionszeitalter =======================
@motiv('einheit:plasmagrenadier')
def _(m):
    def werfer(m, x):
        m.platte(14 + x, 16, 25 + x, 19, FW2); m.rect(25 + x, 16, 28 + x, 19, FW3); m.rect(28 + x, 17, 29 + x, 18, FO)
        m.set(30 + x, 17, FOH); m.set(30 + x, 18, FOW); m.set(31 + x, 17, FOH)
        m.rect(17 + x, 17, 21 + x, 18, FO); m.rect(17 + x, 17, 21 + x, 17, FOH)
        m.rect(19 + x, 20, 20 + x, 22, FW4)
    figur(m, ruest=FW1, helm=FW2, visier=FO, hose=FW3, stiefel=FW4, rucksack=FW3, schulter=FW1, waffe=werfer)
    m.rect(8, 12, 10, 14, FO); m.set(9, 12, FOW)                                       # Plasmatank
    m.rect(8, 15, 10, 15, FR)


@motiv('einheit:schwebepanzer')
def _(m):
    panzer(m, FW1, FW3, FW2, FW4, FO, kette=False, schweben=True, rohr_l=9)
    m.rect(29, 14, 31, 17, FO); m.set(31, 15, FOW); m.set(31, 16, FOW)
    for x in (7, 11, 15, 19, 23): m.set(x, 20, FW3)


@motiv('einheit:railgun_batterie')
def _(m):
    m.kette(3, 20, 25, 30)
    m.ppoly([(2, 24), (4, 19), (21, 19), (23, 24)], FW2); m.rect(3, 23, 22, 24, FW3)
    m.rect(5, 21, 18, 21, 'S'); m.rect(5, 22, 18, 22, 'S-')
    m.kasten(7, 18, 8, 5, 2, FW1)
    # lange Doppelschiene schräg nach rechts oben
    for i in range(18):
        x, y = 12 + i, 16 - i * 0.6
        m.set(x, round(y) - 2, FW4); m.set(x, round(y) - 1, FO if i % 3 else FOH); m.set(x, round(y), FW4)
    m.glut(30, 5, FOH)
    m.kugel(11, 14, 3, 2.5, FW3)


@motiv('einheit:laserabwehr')
def _(m):
    m.kette(5, 26, 25, 30)
    m.ppoly([(4, 24), (6, 19), (25, 19), (27, 24)], FW2); m.rect(5, 23, 26, 24, FW3)
    m.rect(7, 21, 23, 21, 'S'); m.rect(7, 22, 23, 22, 'S-')
    m.kugel(15.5, 15, 6, 4.5, FW1, nur_oben=False)
    m.rect(10, 17, 21, 18, FW3)
    for i, (x0, y0) in enumerate(((13, 11), (18, 11))):
        m.line(x0, y0, x0 + 8, y0 - 8, FW4); m.line(x0 + 1, y0, x0 + 9, y0 - 8, FW3)
        m.glut(x0 + 9, y0 - 9, FO)
    m.rect(13, 14, 18, 15, FO); m.rect(14, 14, 17, 14, FOW)


@motiv('einheit:fusionszerstoerer')
def _(m):
    m.wasser(28)
    m.ppoly([(1, 22), (29, 22), (31, 23), (27, 28), (4, 28)], FW2); m.rect(4, 26, 27, 27, FW3)
    m.rect(3, 23, 29, 23, 'S'); m.rect(4, 24, 28, 24, 'S-')
    m.kasten(8, 21, 10, 5, 2, FW1); m.fenster(9, 18, 17, 18, 2, 1, KC)
    m.kasten(12, 16, 5, 4, 2, FW1); m.rect(13, 13, 16, 13, FOW)
    m.line(15, 11, 15, 6, FW4); m.rect(13, 7, 17, 7, FW4); m.set(15, 5, FO)
    m.kugel(23, 19, 3, 2.5, FW1, nur_oben=True); m.rect(23, 18, 29, 18, FW4)       # Turm vorn
    m.kugel(5, 19, 2.5, 2.2, FO, nur_oben=True); m.set(5, 17, FOW)                   # Reaktorkuppel


@motiv('einheit:schildfregatte')
def _(m):
    m.wasser(28)
    # Schild-Kuppel (Pixel-Schraffur)
    for y in range(4, 24):
        for x in range(2, 30):
            u = (x - 15.5) / 14; v = (y - 23) / 19
            if .85 < u * u + v * v <= 1.02: m.set(x, y, '#9fe3ff' if (x + y) % 2 else '#d8f6ff')
    m.ppoly([(4, 22), (26, 22), (29, 23), (25, 28), (6, 28)], FW2); m.rect(6, 26, 25, 27, FW3)
    m.rect(5, 23, 27, 23, 'S'); m.rect(6, 24, 26, 24, 'S-')
    m.kasten(10, 21, 9, 6, 2, FW1); m.fenster(11, 17, 17, 17, 2, 1, KC)
    m.kugel(14.5, 12, 3, 3, '#7fd8ff'); m.line(14, 15, 14, 16, FW4)


@motiv('einheit:hyperloop_kurier')
def _(m):
    # Röhre auf Stelzen, Kapsel darin
    for x in (4, 15, 26): m.rect(x, 22, x + 1, 30, FW3); m.rect(x - 1, 30, x + 2, 30, FW4)
    m.rect(0, 13, 31, 21, '#bfe6ff'); m.rect(0, 13, 31, 13, FW1); m.rect(0, 21, 31, 21, FW3)
    for x in range(1, 31, 5): m.set(x, 14, '#ffffff')
    m.ppoly([(4, 20), (6, 15), (22, 15), (28, 17.5), (22, 20)], FW1)
    m.rect(8, 16, 18, 17, KC); m.rect(9, 16, 17, 16, KCH)
    m.rect(6, 19, 22, 19, 'S')
    for x in range(0, 4): m.set(x, 17, FOH)


# ======================= X · Weltraumzeitalter =======================
@motiv('einheit:raumjaeger')
def _(m):
    sterne(m, 4, 3)
    m.ppoly([(4, 15), (10, 12), (22, 12), (30, 15), (22, 18), (10, 18)], WW1)
    m.ppoly([(8, 12), (14, 4), (17, 4), (18, 12)], WW2); m.ppoly([(8, 18), (18, 18), (17, 26), (14, 26)], WW3)
    m.rect(14, 5, 16, 5, 'S'); m.rect(14, 25, 16, 25, 'S'); m.rect(10, 15, 20, 15, 'S-')
    m.rect(21, 14, 25, 15, WV); m.rect(22, 14, 24, 14, WVH)
    m.rect(5, 13, 7, 17, WW4); m.flamme(4, 15, 4, 'l', 1)
    m.set(16, 4, WVH); m.set(16, 26, WVH)


@motiv('einheit:orbital_marine')
def _(m):
    figur(m, ruest=WW1, helm=WW1, visier='#ffcf5a', hose=WW2, stiefel=WW4, haut=False, rucksack=WW3, schulter=WW2,
          waffe=gewehr(WW4, WV, 8))
    m.rect(8, 21, 10, 22, WF); m.set(9, 23, WFH)                                         # Sprungdüse
    m.rect(14, 8, 15, 10, WW3)


@motiv('einheit:kampfshuttle')
def _(m):
    m.schatten(16, 29, 12)
    m.ppoly([(2, 20), (5, 13), (20, 11), (27, 14), (31, 19), (27, 22), (4, 22)], WW1)
    m.rect(4, 21, 28, 22, WW3)
    m.ppoly([(8, 20), (14, 16), (22, 16), (24, 23), (9, 23)], WW2)                         # Flügel
    m.rect(22, 13, 27, 15, WVD); m.rect(23, 13, 26, 13, WVH)                               # Cockpit
    m.rect(6, 17, 20, 17, 'S'); m.rect(6, 18, 20, 18, 'S-')
    m.ppoly([(3, 13), (6, 6), (9, 6), (8, 13)], WW2)                                       # Leitwerk
    m.flamme(1, 17, 3, 'l', 1); m.rect(23, 24, 24, 26, WW4); m.rect(8, 23, 9, 26, WW4)


@motiv('einheit:hyperschallbomber')
def _(m):
    m.schatten(15, 29, 12)
    m.ppoly([(2, 15), (8, 12), (26, 13.5), (31, 15), (26, 16.5), (8, 18)], WW3)
    m.ppoly([(6, 12), (18, 13), (20, 2), (17, 2)], WW4); m.ppoly([(6, 18), (17, 28), (20, 28), (18, 17)], dunkel(WW4, .2))
    m.rect(22, 14, 26, 15, WV); m.rect(9, 15, 20, 15, 'S'); m.rect(17, 3, 18, 4, 'S'); m.rect(17, 26, 18, 27, 'S')
    m.flamme(1, 13, 3, 'l', 0); m.flamme(1, 17, 3, 'l', 0)
    for x in range(10, 24, 3): m.set(x, 14, WW2)


@motiv('einheit:marsrover_panzer')
def _(m):
    for x in (7, 15, 23):
        m.kugel(x, 26.5, 3.4, 3.4, '#5a5450', glanz=False); m.kugel(x, 26.5, 1.4, 1.4, WW2, glanz=False)
    m.rect(4, 22, 27, 22, WW4)
    m.ppoly([(3, 22), (5, 16), (26, 16), (28, 22)], WW1); m.rect(4, 21, 27, 22, WW3)
    m.rect(6, 18, 24, 18, 'S'); m.rect(6, 19, 24, 19, 'S-')
    m.kugel(13, 13, 5, 3.5, WW2); m.rect(14, 12, 29, 13, WW4); m.rect(14, 12, 29, 12, WW3); m.set(30, 12, WF)
    m.rect(5, 8, 5, 15, WW4); m.ppoly([(2, 6), (8, 6), (8, 8), (2, 8)], '#3b6fd8'); m.set(3, 7, '#9cc4ff')
    m.rect(0, 30, 31, 30, '#c46a3a')


@motiv('einheit:asteroidenfrachter')
def _(m):
    sterne(m, 3, 5)
    m.kugel(25, 8, 5.5, 4.5, '#8a7a68'); m.set(23, 7, '#5a4c3e'); m.set(27, 10, '#5a4c3e'); m.set(26, 6, '#5a4c3e')
    m.line(20, 11, 14, 15, WW4)                                                            # Greifarm
    m.ppoly([(2, 14), (16, 14), (20, 18), (20, 24), (2, 24)], WW2); m.rect(2, 23, 20, 24, WW4)
    for x in range(4, 16, 4): m.kasten(x, 22, 3, 5, 1, '#d8a04a')
    m.rect(2, 16, 16, 16, 'S'); m.rect(16, 19, 19, 21, WVD); m.rect(17, 19, 18, 19, WVH)
    m.rect(0, 17, 1, 22, WW4); m.flamme(0, 19, 1, 'l', 1)


@motiv('einheit:terraformer')
def _(m):
    m.kette(3, 28, 25, 30)
    m.ppoly([(2, 24), (4, 17), (27, 17), (29, 24)], WW2); m.rect(3, 23, 28, 24, WW4)
    m.rect(5, 19, 26, 19, 'S'); m.rect(5, 20, 26, 20, 'S-')
    m.kasten(6, 16, 9, 7, 2, WW1); m.fenster(8, 11, 13, 11, 2, 1, WV)
    for x, h in ((20, 13), (24, 9)):
        m.rect(x, 16 - h, x + 2, 16, WW3); m.rect(x, 16 - h, x + 2, 16 - h, WW1)
    for (x, y) in ((22, 1), (26, 0), (21, 0), (27, 3), (24, 1)): m.set(x, y, GRAS)
    m.set(23, 2, '#a8e890'); m.set(25, 5, '#a8e890'); m.set(25, 3, GRAS)


# ======================= XI · Sternenzeitalter =======================
@motiv('einheit:sternenkreuzer')
def _(m):
    sterne(m, 5, 7)
    m.ppoly([(1, 17), (6, 12), (24, 11), (31, 16), (24, 21), (6, 21)], SP1)
    m.rect(6, 19, 24, 21, SP3)
    m.ppoly([(8, 12), (14, 6), (22, 6), (20, 12)], SP2); m.ppoly([(8, 21), (20, 21), (22, 27), (14, 27)], SP3)
    m.rect(9, 15, 22, 15, SK3); m.rect(9, 15, 22, 15, SK2); m.rect(10, 16, 21, 16, SK4)
    for x in range(10, 22, 3): m.set(x, 15, SK1)
    m.rect(24, 14, 27, 16, SGO); m.set(25, 14, '#fff3c4')
    m.rect(9, 18, 21, 18, 'S'); m.rect(15, 7, 19, 7, 'S'); m.rect(15, 26, 19, 26, 'S')
    m.rect(1, 14, 4, 19, SP3); m.glut(0, 15, SK2); m.glut(0, 18, SK2)


@motiv('einheit:sternenkrieger')
def _(m):
    figur(m, ruest=SP1, helm=SK2, visier=SGO, hose=SP2, stiefel=SP3, haut=False, schulter=SK2,
          waffe=gewehr(SP3, SK2, 9))
    # Kristallflügel hinten
    m.ppoly([(10, 13), (2, 4), (4, 14)], SK2); m.ppoly([(10, 15), (1, 12), (5, 19)], SK3)
    m.set(5, 8, SK1); m.set(4, 14, SK1)


@motiv('einheit:nanoschwarm')
def _(m):
    import random
    r = random.Random(11)
    for i in range(140):
        a = r.random() * 6.28; d = r.random() ** .6 * 13
        x = 16 + math.cos(a) * d * 1.05; y = 15 + math.sin(a) * d * .8
        m.set(x, y, SK3 if d > 9 else SK2 if d > 5 else SK1)
    m.kugel(16, 15, 3, 3, SGO); m.set(16, 15, '#ffffff')
    for x, y in ((6, 10), (25, 19), (11, 23), (24, 8)): m.set(x, y, 'S')
    m.schatten(16, 29, 9)


@motiv('einheit:orbitalkanone')
def _(m):
    sterne(m, 4, 9)
    m.kugel(16, 26, 13, 6, '#4a7fd0', glanz=False)                                         # Planetenrand unten
    for x in range(4, 28, 5): m.set(x, 22, '#7fb2ee')
    m.kasten(7, 17, 10, 6, 3, SP2)
    m.rect(5, 10, 6, 17, SK3); m.rect(20, 7, 21, 17, SK3)                                  # Solarflügel
    m.rect(2, 9, 8, 10, SK4); m.rect(18, 6, 24, 7, SK4)
    m.rect(9, 13, 15, 13, 'S')
    m.line(12, 11, 12, 21, SGO); m.rect(11, 18, 13, 20, SP3)
    for y in range(21, 26): m.set(12, y, '#ffffff' if y % 2 else SK2)


@motiv('einheit:antimaterie_rakete')
def _(m):
    m.rect(14, 24, 18, 30, SP3); m.rect(10, 30, 22, 30, SP3)                               # Startgestell
    m.ppoly([(13, 25), (13, 9), (16, 3), (19, 9), (19, 25)], SP1)
    m.rect(17, 9, 19, 25, SP2)
    m.ppoly([(13, 20), (9, 26), (13, 26)], SK3); m.ppoly([(19, 20), (23, 26), (19, 26)], SK4)
    m.kugel(16, 14, 2.4, 2.4, '#d070ff'); m.set(16, 14, '#ffffff')                         # Antimaterie-Kern
    m.rect(13, 19, 19, 19, 'S'); m.rect(13, 20, 19, 20, 'S-')
    m.set(15, 5, SGO); m.set(16, 4, SGO)
    for x, y in ((8, 12), (24, 10), (22, 16)): m.set(x, y, '#d070ff')


# ======================= Volkskarten · Einheiten =======================
@motiv('einheit:nl_fusionsschiff')
def _(m):
    m.wasser(28)
    m.ppoly([(1, 21), (29, 21), (31, 22), (26, 28), (4, 28)], '#6a4a30'); m.rect(4, 26, 27, 27, '#4a3020')
    for x in range(3, 29, 3): m.set(x, 23, '#8a6a44')
    m.rect(3, 22, 29, 22, 'S'); m.rect(4, 24, 27, 24, 'S-')
    m.kasten(9, 20, 12, 5, 2, FW1); m.fenster(10, 17, 20, 17, 2, 1, KC)
    m.kugel(15, 12, 4, 3.5, FO); m.kugel(15, 12, 2, 2, FOW, glanz=False)                  # Reaktor-Sonne
    m.rect(25, 12, 26, 20, '#6a4a30'); m.ppoly([(26, 6), (30, 12), (26, 12)], '#d8302a')    # Drachenkopf-Mast
    m.set(27, 9, '#ffd166')


@motiv('einheit:nl_sternensegler')
def _(m):
    sterne(m, 4, 13)
    m.ppoly([(3, 23), (28, 23), (25, 27), (6, 27)], SP2); m.rect(6, 26, 25, 27, SP3)
    m.rect(4, 24, 27, 24, 'S')
    m.rect(15, 3, 16, 23, SP3)
    m.ppoly([(17, 4), (28, 20), (17, 20)], SK2); m.ppoly([(17, 4), (21, 10), (17, 12)], SK1)
    m.ppoly([(14, 6), (5, 20), (14, 20)], SGO); m.ppoly([(14, 6), (11, 12), (14, 13)], '#fff0b0')
    m.set(16, 2, SK1); m.glut(4, 28, SK2); m.glut(27, 28, SK2)


@motiv('einheit:sv_mondgaertner')
def _(m):
    m.rect(2, 29, 29, 30, '#b9b4c4'); m.set(6, 29, '#8e88a0'); m.set(22, 30, '#8e88a0')
    figur(m, x=-3, ruest=WW1, helm='#cfe9ff', visier=None, hose=WW2, stiefel=WW4, haut=True, rucksack='#ffd23f')
    m.kugel(12.5, 8, 5, 5, '#bfe6ff'); m.rect(11, 9, 15, 11, HAUT); m.set(14, 9, OUT)       # Glashelm
    m.set(10, 5, '#ffffff'); m.set(11, 4, '#ffffff')
    # Pflanze im Topf
    m.kasten(21, 28, 6, 4, 2, '#c46a3a'); m.rect(23, 18, 23, 24, GRAS_D)
    for (x, y) in ((22, 18), (24, 17), (21, 20), (25, 20), (23, 16), (22, 22), (25, 22)): m.set(x, y, GRAS)
    m.set(23, 15, '#ff8ab0')


@motiv('einheit:gb_lieferflotte')
def _(m):
    for (cx, cy) in ((8, 7), (22, 6), (15, 17)):
        m.rect(cx - 6, cy - 3, cx + 6, cy - 3, KG3); m.rect(cx - 7, cy - 4, cx - 4, cy - 4, M2); m.rect(cx + 4, cy - 4, cx + 7, cy - 4, M2)
        m.kugel(cx, cy - 1, 3, 2, '#f2c14e'); m.set(cx + 1, cy - 1, KC)
        m.kasten(cx - 2, cy + 5, 5, 4, 1, '#c99a5e'); m.rect(cx, cy + 2, cx, cy + 5, 'S')
    m.kugel(26, 25, 3, 3, '#f2c14e'); m.set(26, 25, '#c9962b'); m.set(25, 24, '#fff3c4')    # Münze
    m.schatten(15, 29, 9)


@motiv('einheit:gb_orbitalfrachter')
def _(m):
    sterne(m, 4, 17)
    m.ppoly([(2, 13), (22, 12), (28, 16), (22, 21), (2, 20)], WW1); m.rect(2, 19, 22, 21, WW3)
    for x in (5, 10, 15):
        m.kasten(x, 19, 4, 5, 1, '#f2c14e'); m.set(x + 1, 16, '#c9962b')
    m.rect(22, 15, 26, 17, WVD); m.rect(23, 15, 25, 15, WVH)
    m.rect(3, 14, 20, 14, 'S')
    m.rect(0, 14, 1, 19, WW4); m.flamme(0, 16, 1, 'l', 1)


def reiter(m, tier, tier_d, tier_h, mann, mann_h, auge, beine='lauf'):
    # Reittier (Robo-Pferd) nach rechts
    for (x, c) in ((8, tier_d), (11, tier), (20, tier_d), (23, tier)):
        m.rect(x, 22, x + 1, 28, c); m.rect(x - 1, 29, x + 1, 30, M5)
    m.ppoly([(6, 22), (7, 16), (24, 16), (25, 22)], tier); m.rect(7, 21, 24, 22, tier_d)
    m.ppoly([(22, 17), (25, 9), (30, 10), (30, 13), (26, 15), (25, 18)], tier)                # Hals + Kopf
    m.set(28, 11, auge); m.set(29, 11, hell(auge, .5))
    m.line(6, 17, 2, 21, tier_h); m.line(5, 17, 1, 20, tier_d)                                # Schweif
    m.rect(10, 18, 20, 18, 'S'); m.rect(10, 19, 20, 19, 'S-')
    # Reiter
    m.rect(12, 7, 18, 15, mann); m.rect(12, 7, 18, 7, hell(mann, .3)); m.rect(17, 8, 18, 15, dunkel(mann, .3))
    m.rect(13, 14, 15, 18, dunkel(mann, .2))
    m.kugel(15.5, 4, 3, 2.8, mann_h); m.rect(16, 4, 18, 4, auge)
    m.rect(17, 10, 23, 11, M4); m.rect(23, 6, 23, 14, M3); m.set(23, 5, auge)                 # Lanze


@motiv('einheit:sr_roboterreiter')
def _(m): reiter(m, KG1, KG3, KC, '#9a6a3a', KG2, KC)

@motiv('einheit:sr_marsreiter')
def _(m):
    reiter(m, WW1, WW3, WV, '#b8562e', '#bfe6ff', '#ffcf5a')
    m.rect(0, 30, 31, 30, '#c46a3a')

@motiv('einheit:sr_sternenhorde')
def _(m):
    sterne(m, 5, 19)
    for (dx, dy, s) in ((-6, -2, .9), (6, 1, 1)):
        pass
    # Drei Sternenreiter auf Gleitern hintereinander
    for i, (x, y) in enumerate(((2, 6), (10, 13), (17, 20))):
        m.ppoly([(x, y + 6), (x + 2, y + 4), (x + 12, y + 4), (x + 14, y + 6), (x + 12, y + 7), (x + 2, y + 7)], SP1)
        m.rect(x + 2, y + 7, x + 12, y + 7, SP3); m.set(x, y + 6, SK2); m.glut(x - 1, y + 6, SK2, 0)
        m.rect(x + 5, y, x + 8, y + 3, 'S'); m.rect(x + 5, y, x + 8, y, 'S+')
        m.kugel(x + 6.5, y - 2, 1.8, 1.8, SK2, glanz=False); m.set(x + 7, y - 2, SGO)
        m.line(x + 9, y + 1, x + 13, y - 2, SGO)
