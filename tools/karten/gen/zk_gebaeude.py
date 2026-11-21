"""Gebäude der Zeitalter VIII–XI, zweite Fassung (32x32, Kästen mit Tiefe wie die alten Gebäude)."""
import random
from zk_basis import *

NEU = {}
def motiv(key):
    def deko(fn): NEU[key] = fn; return fn
    return deko

R = lambda n: random.Random(n)


def turm(m, x, yb, w, h, d, f, glas, licht=None, seed=1, dx=2, dy=2, rahmen=None):
    m.kasten(x, yb, w, h, d, f)
    m.fenster(x + 1, yb - h + 3, x + w - 2, yb - 2, dx, dy, glas, licht, rahmen, R(seed))
    m.seitenfenster(x, yb, w, h, d, dunkel(glas, .25))


def dachgarten(m, x, y, w):
    m.rect(x, y, x + w - 1, y, GRAS); m.rect(x, y - 1, x + w - 1, y - 1, GRAS_D)
    for i in range(x, x + w, 3): m.set(i, y - 2, GRAS); m.set(i + 1, y - 2, '#8fd86e')


# ======================= VIII · KI-Zeitalter =======================
@motiv('gebaeude:ki_labor')
def _(m):
    m.kasten(1, 30, 24, 14, 4, M2)
    m.fenster(3, 19, 22, 27, 3, 4, KG3)
    for x in range(3, 23, 3): m.rect(x, 19, x + 1, 21, KC); m.rect(x, 23, x + 1, 25, KB)
    m.rect(1, 17, 24, 17, 'S'); m.rect(1, 28, 24, 28, M3)
    m.kasten(8, 15, 9, 4, 2, M1)
    m.kugel(12.5, 9, 4, 3.5, KC); m.kugel(12.5, 9, 2, 1.8, KCH, glanz=False)                  # KI-Kern
    m.line(12, 5, 12, 2, M4); m.set(12, 1, KC)
    m.rect(10, 26, 14, 30, KG3); m.rect(11, 27, 13, 30, KB)


@motiv('gebaeude:autonome_fabrik')
def _(m):
    m.kasten(1, 30, 22, 12, 4, KG1, seite=KG3, dach=M2)
    for x in range(1, 23, 5):                                                                   # Sheddach
        m.ppoly([(x, 18), (x + 4, 14), (x + 4, 18)], M2); m.set(x + 3, 16, KC)
    m.rect(3, 21, 20, 24, KG4); m.rect(4, 22, 19, 22, KC)                                       # Fließband-Fenster
    for x in range(5, 19, 4): m.rect(x, 23, x + 1, 24, M3)
    m.rect(14, 26, 19, 30, KG3); m.rect(15, 26, 18, 26, 'S')
    m.rect(25, 8, 27, 26, KG2); m.rect(25, 8, 27, 8, KG1); m.rect(24, 6, 28, 7, M4); m.set(26, 5, KC)
    m.line(4, 27, 9, 27, 'S'); m.rect(3, 28, 10, 28, 'S-')


@motiv('gebaeude:intelligentes_stromnetz')
def _(m):
    for (x, h) in ((4, 22), (22, 17)):
        m.rect(x + 1, 30 - h, x + 2, 30, M4); m.line(x - 2, 30, x + 1, 30 - h + 5, M4); m.line(x + 5, 30, x + 2, 30 - h + 5, M4)
        m.rect(x - 2, 30 - h + 3, x + 5, 30 - h + 3, M4); m.rect(x - 1, 30 - h + 7, x + 4, 30 - h + 7, M4)
        for dx in (-2, 5): m.set(x + dx, 30 - h + 4, KC)
    for i in range(18):                                                                          # Leitungen mit Datenpunkten
        x = 6 + i; y = 12 + int((i - 9) ** 2 / 20)
        m.set(x, y, M5); m.set(x, y + 4, M5)
        if i % 4 == 1: m.set(x, y, KC); m.set(x, y + 4, KCH)
    m.kasten(9, 30, 10, 7, 3, KG1); m.rect(11, 25, 16, 27, KG4); m.rect(12, 26, 15, 26, KC); m.rect(9, 29, 18, 29, 'S')
    m.ppoly([(13, 22), (15, 18), (14, 21), (16, 21), (13, 25), (14, 22)], '#ffd23f')


@motiv('gebaeude:vertikalfarm')
def _(m):
    m.kasten(5, 30, 16, 27, 4, M2)
    for i, y in enumerate(range(6, 28, 5)):
        m.rect(6, y, 19, y + 3, '#cfeaff'); m.rect(6, y + 3, 19, y + 3, M3)
        for x in range(7, 19, 2): m.set(x, y + 2, GRAS); m.set(x + (i % 2), y + 1, GRAS_D)
        if i % 2: m.set(9, y + 1, '#ff6a5a'); m.set(15, y + 1, '#ff6a5a')
        for k in (2, 4): m.set(20 + k, y + 2 - k, GRAS)
    dachgarten(m, 9, 2, 12)
    m.rect(5, 30, 20, 30, 'S'); m.rect(11, 27, 14, 30, KG3)


@motiv('gebaeude:virtuelles_forum')
def _(m):
    m.kasten(1, 30, 24, 7, 4, M2)
    for x in range(3, 24, 3): m.rect(x, 25, x + 1, 30, M1); m.set(x + 1, 30, M3)
    m.rect(1, 23, 24, 23, 'S')
    m.kugel(13, 13, 10, 8.5, '#3d6fe0', '#8fb6ff', '#2a4aa8', nur_oben=True)                   # Holo-Kuppel
    for y in range(6, 21, 3):
        for x in range(4, 23):
            if (x - 13) ** 2 / 100 + (y - 13) ** 2 / 72 <= 1 and y < 14: m.set(x, y, KC if (x + y) % 4 == 0 else None) if (x + y) % 4 == 0 else None
    m.rect(3, 13, 23, 22, '#3d6fe0'); m.rect(3, 14, 23, 14, KC)
    for x in range(5, 22, 4): m.rect(x, 16, x + 1, 20, KCH); m.rect(x, 18, x + 1, 18, KB)
    m.funkeln(28, 4, KC)


@motiv('gebaeude:laserturm')
def _(m):
    m.kasten(5, 30, 18, 6, 3, KG2, seite=KG4, dach=KG1)
    m.rect(6, 27, 21, 27, 'S')
    m.ppoly([(9, 25), (10, 12), (18, 12), (19, 25)], KG1); m.rect(17, 12, 19, 25, KG3)
    m.rect(11, 16, 16, 18, KG4); m.rect(12, 17, 15, 17, KC)
    m.kugel(14, 9, 5, 4, M2)
    m.rect(17, 7, 27, 9, KG3); m.rect(17, 7, 27, 7, KG1); m.rect(27, 6, 28, 10, M4)
    for x in range(29, 32): m.set(x, 8, KCH if x % 2 else KC)
    m.set(14, 4, KC); m.line(14, 4, 14, 2, M4)


# ======================= IX · Fusionszeitalter =======================
@motiv('gebaeude:fusionsreaktor')
def _(m):
    m.kasten(1, 30, 24, 8, 4, FW2)
    m.rect(1, 25, 24, 25, 'S'); m.rect(4, 27, 21, 29, FW3)
    m.kugel(13, 15, 10, 9, FW1, nur_oben=True)                                                # Tokamak-Kuppel
    m.rect(3, 15, 23, 22, FW1); m.rect(19, 15, 23, 22, FW2)
    m.ell(13, 16, 8, 2.2, FR); m.ell(13, 16, 6.5, 1.2, FO); m.rect(9, 16, 17, 16, FOW)          # Plasmaring
    m.rect(3, 19, 23, 19, FW3); m.fenster(5, 21, 21, 21, 3, 1, FOH)
    for x in (27, 29): m.rect(x, 12, x, 28, FW3)
    m.rect(26, 11, 30, 11, FW4); m.glut(28, 9, FOH)


@motiv('gebaeude:quantenrechner')
def _(m):
    m.kasten(2, 30, 20, 9, 4, FW2)
    m.rect(2, 24, 21, 24, 'S'); m.rect(4, 26, 19, 29, FW4); m.fenster(5, 27, 18, 28, 2, 1, FOH, KC, None, R(4))
    # Kryo-Kronleuchter (goldene Etagen)
    for i, (y, w) in enumerate(((19, 7), (15, 5), (11, 4), (8, 2))):
        m.rect(12 - w, y, 12 + w, y + 1, SGO); m.rect(12 - w, y + 1, 12 + w, y + 1, SGOD)
        if i < 3:
            for x in range(12 - w + 1, 12 + w, 2): m.line(x, y - 2, x, y - 1, FW3)
    m.line(12, 3, 12, 7, FW3); m.glut(12, 2, KC)
    m.rect(26, 14, 29, 30, FW1); m.rect(28, 14, 29, 30, FW3); m.rect(26, 13, 29, 13, FW2)
    m.rect(27, 17, 27, 26, KC)


@motiv('gebaeude:co2_waescher')
def _(m):
    m.kasten(1, 30, 26, 10, 3, FW2)
    for x in range(3, 26, 3): m.rect(x, 22, x + 1, 28, FW4); m.set(x, 23, '#9fe3ff')       # Lamellen-Filter
    m.rect(1, 20, 26, 20, 'S')
    for (x, h) in ((5, 8), (13, 12), (21, 9)):
        m.kasten(x, 19, 5, h, 2, FW1); m.rect(x + 1, 19 - h + 2, x + 3, 19 - h + 2, GRAS)
    for (x, y) in ((8, 6), (15, 3), (23, 6), (17, 1), (11, 2)): m.set(x, y, '#cff5ff'); m.set(x + 1, y, '#ffffff')
    m.set(29, 16, GRAS); m.set(28, 15, GRAS_D)


@motiv('gebaeude:energieschild')
def _(m):
    m.kasten(10, 30, 9, 9, 3, FW2)
    m.rect(11, 23, 17, 23, 'S'); m.rect(12, 25, 16, 29, FW4); m.rect(13, 26, 15, 27, FO)
    m.rect(13, 13, 15, 21, FW3); m.kugel(14, 12, 3, 3, FO); m.set(14, 12, FOW)
    for y in range(2, 31):                                                                       # Schildkuppel
        for x in range(0, 32):
            u = (x - 14) / 14; v = (y - 30) / 28
            q = u * u + v * v
            if .84 < q <= 1.0: m.set(x, y, FOH if (x + y) % 2 else '#fff0b8')
            elif .6 < q <= .84 and (x * 3 + y) % 9 == 0: m.set(x, y, '#ffe9a0')


@motiv('gebaeude:hyperloop_station')
def _(m):
    m.kasten(4, 30, 20, 11, 4, FW1)
    m.rect(5, 22, 22, 25, '#bfe6ff'); m.rect(5, 22, 22, 22, '#e8f7ff')
    for x in range(7, 22, 4): m.rect(x, 23, x, 25, FW3)
    m.rect(4, 27, 23, 27, 'S'); m.rect(12, 26, 15, 30, FW4)
    m.kugel(14, 18, 10, 4, FW2, nur_oben=True)                                                 # geschwungenes Dach
    m.rect(0, 9, 31, 13, '#bfe6ff'); m.rect(0, 9, 31, 9, FW1); m.rect(0, 13, 31, 13, FW3)      # Röhre
    m.ppoly([(9, 12), (11, 10), (20, 10), (23, 11.5), (20, 12)], FW1); m.rect(12, 11, 18, 11, FO)
    for x in (2, 29): m.rect(x, 14, x + 1, 30, FW3)


# ======================= X · Weltraumzeitalter =======================
@motiv('gebaeude:raumhafen')
def _(m):
    m.rect(0, 26, 31, 30, WW3); m.rect(0, 26, 31, 26, WW2); m.rect(0, 30, 31, 30, WW4)
    for x in range(2, 31, 6): m.rect(x, 28, x + 2, 28, '#ffd23f')
    m.kasten(1, 25, 11, 8, 3, WW1); m.fenster(2, 20, 10, 23, 2, 3, WV); m.rect(1, 25, 11, 25, 'S')
    m.ppoly([(17, 25), (17, 10), (20, 4), (23, 10), (23, 25)], WW1); m.rect(21, 10, 23, 25, WW2)  # Rakete
    m.ppoly([(17, 20), (14, 25), (17, 25)], WV); m.ppoly([(23, 20), (26, 25), (23, 25)], WVD)
    m.rect(17, 14, 23, 14, 'S'); m.set(19, 8, WVD); m.set(20, 8, WVD)
    m.rect(27, 6, 28, 25, WW4); for_ = [m.rect(25, y, 27, y, WW4) for y in (10, 16, 22)]


@motiv('gebaeude:orbitalstation')
def _(m):
    sterne(m, 4, 21)
    m.kugel(16, 32, 18, 6, '#3f8fd8', glanz=False)                                             # Erde unten
    m.set(8, 28, GRAS); m.set(9, 28, GRAS); m.set(20, 27, GRAS); m.set(21, 27, '#ffffff')
    m.rect(2, 12, 29, 13, WW3)                                                                   # Träger
    for x0 in (1, 23):
        m.rect(x0, 5, x0 + 7, 20, '#2a3f8c')
        for y in range(6, 20, 3): m.rect(x0 + 1, y, x0 + 6, y, '#5f86e8')
    m.kugel(15.5, 12.5, 5, 4.5, WW1); m.rect(11, 16, 20, 18, WW2); m.rect(12, 17, 19, 17, 'S')
    m.fenster(13, 11, 18, 11, 2, 1, WV)
    m.rect(15, 4, 16, 8, WW3); m.set(15, 3, WFH)


@motiv('gebaeude:mondbasis')
def _(m):
    sterne(m, 5, 23)
    m.kugel(25, 5, 3, 3, '#4f8fe0'); m.set(24, 4, GRAS)                                        # Erde am Himmel
    m.rect(0, 26, 31, 30, '#b9b4c4'); m.rect(0, 26, 31, 26, '#d8d4e0')
    for (x, y) in ((4, 28), (20, 29), (27, 27)): m.ell(x, y, 2, .8, '#8e88a0')
    m.kugel(9, 26, 8, 7, WW1, nur_oben=True); m.rect(2, 22, 16, 26, WW1)
    m.kugel(23, 26, 6, 5, WW2, nur_oben=True)
    m.rect(14, 22, 19, 25, WW3); m.rect(15, 23, 18, 23, WV)                                     # Verbindungsgang
    m.fenster(5, 22, 13, 22, 3, 1, '#ffd23f'); m.rect(3, 25, 15, 25, 'S')
    m.rect(26, 12, 26, 21, WW4); m.ppoly([(24, 11), (29, 9), (29, 13)], WW3)                    # Antenne


@motiv('gebaeude:kolonie_kuppel')
def _(m):
    m.rect(0, 27, 31, 30, '#c46a3a'); m.rect(0, 27, 31, 27, '#e08a52')
    m.kugel(15.5, 27, 15, 14, '#cfeeff', '#ffffff', '#9ccbe6', nur_oben=True)
    for y in range(14, 27, 4): m.rect(1, y, 30, y, '#e8f7ff') if False else None
    m.kasten(5, 26, 6, 9, 2, WW1); m.kasten(14, 26, 5, 13, 2, WW2); m.kasten(21, 26, 5, 7, 2, WW1)
    m.fenster(6, 19, 10, 25, 2, 2, WV); m.fenster(15, 15, 18, 25, 2, 2, WV)
    for x in (4, 12, 20, 27): m.set(x, 25, GRAS); m.set(x + 1, 24, GRAS_D)
    m.rect(1, 26, 30, 26, 'S'); m.set(9, 16, '#ffffff'); m.set(8, 17, '#ffffff')
    for i in range(-14, 15, 7):
        for y in range(14, 27):
            x = 15.5 + i * ((27 - y) / 14) ** .3 if False else None


@motiv('gebaeude:sternenwerft')
def _(m):
    sterne(m, 4, 25)
    for x in (2, 28): m.rect(x, 3, x + 1, 29, WW4); m.rect(x, 3, x + 1, 3, WW2)
    m.rect(2, 3, 29, 4, WW3); m.rect(2, 3, 29, 3, WW2); m.rect(2, 28, 29, 29, WW4)
    for x in range(5, 28, 4): m.set(x, 5, '#ffd23f')
    m.ppoly([(6, 17), (10, 12), (24, 12), (27, 17), (24, 22), (10, 22)], WW1); m.rect(10, 20, 24, 22, WW3)
    m.rect(12, 15, 22, 15, 'S'); m.rect(22, 15, 25, 17, WVD)
    for (x, y) in ((14, 12), (18, 22), (9, 18)): m.glut(x, y, WFH, 0)
    m.line(16, 5, 16, 11, WW4); m.rect(14, 8, 18, 9, WW3)


@motiv('gebaeude:helium3_raffinerie')
def _(m):
    m.rect(0, 28, 31, 30, '#b9b4c4')
    m.kasten(1, 28, 13, 12, 3, WW2); m.fenster(3, 19, 12, 25, 3, 3, WV); m.rect(1, 27, 13, 27, 'S')
    for (x, r) in ((22, 5), ):
        m.kugel(x, 15, r, r, '#e6eef7'); m.rect(x - 1, 20, x, 28, WW4); m.rect(x - 4, 28, x + 4, 28, WW4)
        m.rect(x - 2, 14, x + 2, 15, WV)
    m.kugel(27, 23, 3.5, 3.5, '#e6eef7'); m.rect(26, 26, 27, 28, WW4)
    m.rect(13, 22, 18, 22, WW4); m.rect(4, 10, 6, 16, WW3); m.glut(5, 8, '#9fe3ff')
    m.set(21, 12, '#ffffff')


# ======================= XI · Sternenzeitalter =======================
@motiv('gebaeude:terraforming_station')
def _(m):
    m.rect(0, 27, 13, 30, '#c46a3a'); m.rect(14, 27, 31, 30, GRAS); m.rect(14, 27, 31, 27, '#8fd86e'); m.rect(0, 27, 13, 27, '#e08a52')
    m.kasten(7, 26, 15, 10, 4, SP1, seite=SP3, dach=SK1); m.fenster(9, 19, 20, 24, 3, 3, SK3)
    m.rect(7, 26, 21, 26, 'S')
    m.ppoly([(11, 16), (14, 2), (17, 16)], SK2); m.ppoly([(14, 2), (17, 16), (15, 16)], SK3); m.set(13, 8, SK1)
    for (x, y) in ((22, 10), (25, 6), (27, 12), (4, 12)): m.set(x, y, '#9fe3ff')
    for x in (16, 20, 24, 28): m.set(x, 26, GRAS_D); m.set(x + 1, 25, GRAS)


@motiv('gebaeude:antimaterie_fabrik')
def _(m):
    m.kasten(1, 30, 22, 13, 4, SP2, seite=SP3, dach=SP1)
    m.rect(1, 21, 22, 21, 'S')
    for x in (4, 10, 16):
        m.rect(x, 23, x + 3, 29, SP3); m.kugel(x + 1.5, 25.5, 1.4, 2, '#d070ff', glanz=False); m.set(x + 1, 25, '#ffffff')
    m.kugel(12, 11, 6, 6, '#b85cf0', '#e8b8ff', '#7a30b8'); m.kugel(12, 11, 2.6, 2.6, '#ffffff', glanz=False)
    for (dx, dy) in ((-8, 0), (8, 0), (0, -8)): m.set(12 + dx, 11 + dy, '#d070ff')
    m.ell(12, 11, 9, 2, '#d070ff') if False else None
    for x in range(3, 22): m.set(x, 11 + (1 if x % 2 else 0) * 0, SGO) if abs(x - 12) > 6 else None
    m.rect(26, 6, 28, 26, SP3); m.rect(26, 6, 28, 6, SP1); m.glut(27, 4, '#d070ff')


@motiv('gebaeude:gravitationsschild')
def _(m):
    for (x, h) in ((4, 18), (24, 18)):
        m.ppoly([(x - 2, 30), (x, 30 - h), (x + 3, 30 - h), (x + 5, 30)], SP2); m.rect(x + 2, 30 - h, x + 5, 30, SP3)
        m.kugel(x + 1.5, 30 - h - 2, 2.5, 2.5, SK2); m.set(x + 1, 30 - h - 3, '#ffffff')
    m.rect(0, 30, 31, 30, SP3); m.rect(8, 29, 23, 29, 'S')
    for i, y in enumerate(range(4, 26, 4)):                                                      # Schwerkraftwellen
        for x in range(7, 25):
            yy = y + round(1.5 * math.sin((x + i * 2) / 2.2))
            m.set(x, yy, SK2 if (x + i) % 3 else SK1)


@motiv('gebaeude:kristallturm')
def _(m):
    m.kasten(4, 30, 22, 4, 3, SP2, seite=SP3, dach=SP1); m.rect(4, 29, 25, 29, 'S')
    for (x, y0, w) in ((14, 1, 4), (7, 9, 3), (21, 11, 3)):
        m.ppoly([(x - w, 26), (x - w, y0 + w * 2), (x, y0), (x + w, y0 + w * 2), (x + w, 26)], SK2)
        m.ppoly([(x, y0), (x + w, y0 + w * 2), (x + w, 26), (x, 26)], SK3)
        m.line(x - w + 1, y0 + w * 2 + 1, x - w + 1, 24, SK1)
    m.funkeln(28, 4); m.funkeln(3, 6)


# ======================= Volkskarten · Gebäude =======================
def warte(m, f1, f2, f3, glas, kuppel):
    m.kasten(3, 30, 22, 10, 4, f1, seite=f3, dach=f2); m.fenster(5, 23, 23, 27, 3, 4, glas)
    m.rect(3, 21, 24, 21, 'S')
    m.kugel(14, 19, 9, 8, kuppel, nur_oben=True)
    m.ppoly([(13, 14), (17, 12), (27, 4), (29, 7), (19, 15)], f3); m.rect(26, 3, 30, 7, f2); m.rect(28, 4, 30, 6, glas)


@motiv('gebaeude:sd_ki_observatorium')
def _(m):
    warte(m, M2, M1, M4, KC, '#d8dde3'); m.rect(10, 15, 18, 15, KC); m.funkeln(5, 5, KCH)

@motiv('gebaeude:sd_quantenwarte')
def _(m):
    warte(m, FW2, FW1, FW4, FO, FW1); m.rect(10, 15, 18, 15, FO); m.funkeln(4, 6); m.funkeln(9, 2)

@motiv('gebaeude:sd_orbitalteleskop')
def _(m):
    sterne(m, 5, 27)
    m.ppoly([(8, 18), (8, 11), (24, 9), (24, 20)], WW1); m.rect(8, 17, 24, 20, WW3)
    m.kugel(24, 14.5, 3, 5.5, '#2a3a78', glanz=False); m.kugel(24.5, 14.5, 1.6, 3.4, '#7be3ff')
    m.rect(9, 13, 21, 13, 'S')
    for (x0, y0) in ((1, 10), (12, 22)):
        m.rect(x0, y0, x0 + 6, y0 + 7, '#2a3f8c')
        for y in range(y0 + 1, y0 + 7, 2): m.rect(x0 + 1, y, x0 + 5, y, '#5f86e8')
    m.line(7, 14, 8, 14, WW4); m.line(15, 21, 15, 22, WW4)

@motiv('gebaeude:sd_sternenpforte')
def _(m):
    m.kasten(2, 30, 26, 4, 2, SP2, seite=SP3, dach=SP1); m.rect(2, 29, 27, 29, 'S')
    m.kugel(15, 15, 12, 12, SP1, glanz=False); m.kugel(15, 15, 9, 9, '#3a2f6e', glanz=False)
    for r, c in ((7.5, '#6a4ab8'), (5.5, SK3), (3.5, SK2), (1.5, '#ffffff')): m.kugel(15, 15, r, r, c, glanz=False)
    for a in range(0, 360, 45):
        x = 15 + 10.5 * math.cos(math.radians(a)); y = 15 + 10.5 * math.sin(math.radians(a)); m.set(x, y, SGO)

@motiv('gebaeude:nl_ki_hafen')
def _(m):
    m.wasser(28)
    m.rect(0, 25, 31, 27, '#8a6a44'); m.rect(0, 25, 31, 25, '#a8865a')
    m.kasten(2, 24, 12, 10, 3, KG1); m.fenster(3, 17, 12, 22, 2, 3, KC); m.rect(2, 24, 13, 24, 'S')
    m.rect(19, 4, 21, 24, '#f2c14e'); m.rect(19, 4, 30, 6, '#f2c14e'); m.rect(19, 4, 30, 4, '#ffe08a')
    m.line(28, 7, 28, 14, M5); m.kasten(25, 18, 5, 4, 1, 'S')
    m.rect(22, 21, 24, 24, KG3); m.set(23, 21, KC); m.rect(5, 12, 9, 13, KG3); m.set(7, 11, KC)

@motiv('gebaeude:nl_orbitalwerft')
def _(m):
    sterne(m, 4, 29)
    for x in (2, 28): m.rect(x, 4, x + 1, 28, WW4)
    m.rect(2, 4, 29, 5, WW3); m.rect(2, 27, 29, 28, WW4)
    m.ppoly([(6, 17), (24, 17), (27, 15), (25, 21), (8, 21)], '#6a4a30'); m.rect(8, 20, 25, 21, '#4a3020')
    m.rect(7, 17, 25, 17, 'S')
    m.rect(14, 9, 15, 16, '#6a4a30'); m.ppoly([(16, 9), (23, 15), (16, 15)], '#e6e2d6'); m.rect(16, 11, 21, 11, '#d8302a')
    m.ppoly([(25, 11), (29, 14), (26, 15)], '#d8302a')
    for (x, y) in ((10, 13), (20, 23)): m.glut(x, y, WFH, 0)

@motiv('gebaeude:sv_gewaechshaus')
def _(m):
    m.kasten(7, 30, 14, 26, 4, '#cfeeff', seite='#9ccbe6', dach='#ffffff')
    for y in range(7, 29, 4):
        m.rect(7, y, 20, y, M3)
        for x in range(8, 20, 2): m.set(x, y - 1, GRAS); m.set(x + 1, y - 2, GRAS_D if y % 8 else '#ffd23f')
    for x in (10, 14, 18): m.rect(x, 5, x, 29, M2)
    dachgarten(m, 9, 2, 13); m.set(15, 0, '#ffd23f'); m.rect(7, 30, 20, 30, 'S')
    m.kugel(4, 27, 3, 3, GRAS); m.rect(4, 28, 4, 30, ERDE)

@motiv('gebaeude:sv_sonnenreaktor')
def _(m):
    m.kasten(2, 30, 24, 8, 4, FW1, seite=FW3, dach=FW2); m.rect(2, 24, 25, 24, 'S')
    for x in range(4, 25, 4): m.rect(x, 26, x + 2, 29, '#3a5fb8'); m.set(x, 26, '#8fb2ff')
    m.kugel(14, 11, 7, 7, FO, FOH, FR); m.kugel(13, 10, 3.5, 3.5, FOW, glanz=False)
    for a in range(0, 360, 30):
        x = 14 + 9.5 * math.cos(math.radians(a)); y = 11 + 9.5 * math.sin(math.radians(a))
        if y < 21: m.set(x, y, FOH)
    m.rect(13, 18, 14, 22, FW3)

@motiv('gebaeude:sv_gartenwelt')
def _(m):
    sterne(m, 5, 31)
    m.kugel(15.5, 16, 12, 12, '#4f9ae0', '#9cd0ff', '#2a5fa8')
    for (x, y, w) in ((9, 9, 5), (15, 14, 6), (8, 19, 4), (19, 21, 4), (18, 8, 3)):
        m.rect(x, y, x + w, y + 1, GRAS); m.rect(x + 1, y + 2, x + w - 1, y + 2, GRAS_D)
    m.set(12, 10, '#ffd23f'); m.set(18, 15, '#ff8ab0'); m.set(10, 20, '#ffd23f')
    m.ell(15.5, 16, 15, 2.5, '#ffd23f') if False else None
    for x in range(0, 32):
        y = 17 + round((x - 15.5) * .25)
        if abs(x - 15.5) > 11: m.set(x, y, SGO)
    m.funkeln(5, 4, SGO)

@motiv('gebaeude:gb_quantenboerse')
def _(m):
    m.kasten(2, 30, 22, 18, 4, '#f6efd8', seite='#c9b88a', dach='#fffbea')
    for x in range(4, 23, 4): m.rect(x, 18, x + 1, 29, '#e2d4a8'); m.rect(x, 18, x, 29, '#fffbea')
    m.ppoly([(1, 13), (13, 6), (25, 13)], '#f2c14e'); m.rect(1, 13, 25, 14, '#c9962b')
    m.rect(5, 15, 21, 16, '#3a2f2a')
    for i, x in enumerate(range(6, 21)): m.set(x, 16 - (1 if (x * 7) % 5 > 2 else 0), '#5ad85a' if i % 4 else '#ff5a4a')
    m.kugel(13, 10, 2, 2, KC); m.set(13, 10, '#ffffff'); m.rect(2, 30, 25, 30, 'S')
    m.rect(11, 25, 15, 30, '#6a4a30')

@motiv('gebaeude:gb_sternenmarkt')
def _(m):
    sterne(m, 4, 33)
    m.kugel(15.5, 24, 14, 5, SP2, glanz=False); m.kugel(15.5, 23, 13, 4, SP1, glanz=False)
    for (x, c) in ((5, '#ff7a5a'), (12, '#f2c14e'), (19, SK2), (26, '#9a7bd6')):
        m.ppoly([(x - 3, 21), (x, 16), (x + 3, 21)], c); m.rect(x - 2, 21, x + 2, 24, dunkel(c, .2)) if False else None
        m.rect(x - 3, 21, x + 3, 21, dunkel(c, .3)); m.rect(x - 2, 22, x + 2, 24, SP2); m.set(x, 23, c)
    m.rect(15, 4, 16, 15, SP3); m.kugel(15.5, 4, 2.5, 2.5, SGO); m.rect(4, 26, 27, 26, 'S')

@motiv('gebaeude:sr_plasmaschmiede')
def _(m):
    m.kasten(2, 30, 20, 13, 4, '#7a5a40', seite='#4a3020', dach='#9a7a58')
    m.rect(2, 21, 21, 21, 'S')
    m.rect(5, 23, 13, 30, '#2a1a10'); m.rect(6, 24, 12, 30, FR); m.rect(7, 25, 11, 30, FO); m.rect(8, 27, 10, 30, FOW)
    m.kasten(15, 29, 5, 3, 1, M4); m.rect(15, 26, 19, 26, M3)                                     # Amboss
    m.rect(23, 4, 26, 26, '#5a4030'); m.rect(23, 4, 26, 4, '#7a5a40')
    for (x, y) in ((24, 2), (25, 0), (22, 1)): m.set(x, y, FOH)
    m.line(17, 20, 20, 16, M5); m.rect(19, 14, 22, 16, M4); m.glut(14, 24, FOH, 0)
