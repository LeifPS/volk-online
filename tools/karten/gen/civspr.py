"""Pixel-Sprites der Zivilisations-Erweiterung: Große Persönlichkeiten (Figuren) und Regierungs-Embleme."""
import math, json, os
import spr
from relspr import Mal, OUT, STEIN, STEIN2, STEIN3, GOLD, GOLD2, HOLZ, HOLZ2, WEISS, HAUT, FEUER, FEUER2, WASSER, GRUEN, GRUEN2

HAAR = '#4a3326'; ROT = '#d8432b'; ROT2 = '#9e2a1a'; BLAU = '#4a7fd0'

def figur(rolle):
    W, H = 28, 36; m = Mal(W, H); cx = 13
    # Gewand
    m.rect(cx - 5, 16, cx + 5, 33, 'S'); m.rect(cx - 5, 16, cx - 4, 33, 'S+'); m.rect(cx + 4, 16, cx + 5, 33, 'S-')
    m.tri(cx, 14, 20, 6, 'S'); m.rect(cx - 5, 31, cx + 5, 33, 'S--'); m.rect(cx - 5, 22, cx + 5, 23, 'S--')
    # Kopf
    m.disc(cx, 10, 4.2, HAAR); m.disc(cx, 11, 2.9, HAUT); m.set(cx - 1, 11, OUT); m.set(cx + 1, 11, OUT)
    m.rect(cx + 5, 20, cx + 7, 22, HAUT)       # Hand rechts
    m.rect(cx - 8, 20, cx - 6, 22, HAUT)       # Hand links
    if rolle == 'schriftsteller':
        m.rect(cx - 12, 18, cx - 7, 27, WEISS); m.rect(cx - 12, 18, cx - 7, 18, STEIN2); m.rect(cx - 12, 27, cx - 7, 27, STEIN2)
        for y in (20, 22, 24): m.rect(cx - 11, y, cx - 8, y, STEIN3)
        m.rect(cx + 8, 12, cx + 8, 24, HOLZ); m.set(cx + 8, 11, WEISS); m.set(cx + 9, 10, WEISS)   # Feder
    elif rolle == 'ingenieur':
        m.disc(cx - 10, 24, 4, STEIN3); m.disc(cx - 10, 24, 1.5, 'S+')
        for a in range(8):
            ang = a * math.pi / 4; m.set(cx - 10 + math.cos(ang) * 5, 24 + math.sin(ang) * 5, STEIN3)
        m.rect(cx + 8, 15, cx + 8, 28, HOLZ); m.rect(cx + 6, 14, cx + 10, 16, STEIN2)               # Hammer
        m.rect(cx - 4, 5, cx + 4, 7, GOLD)                                                           # Helm
    elif rolle == 'wissenschaftler':
        m.tri(cx - 10, 17, 26, 4, '#bfe3ff'); m.rect(cx - 11, 14, cx - 9, 17, '#bfe3ff'); m.rect(cx - 12, 13, cx - 8, 13, STEIN2)
        m.rect(cx - 12, 24, cx - 8, 26, GRUEN)
        m.rect(cx + 8, 12, cx + 8, 30, HOLZ2); m.disc(cx + 8, 11, 2.2, GOLD2); m.set(cx + 8, 11, FEUER2)  # Stab/Himmelskugel
    elif rolle == 'general':
        m.rect(cx - 5, 4, cx + 5, 8, STEIN3); m.rect(cx - 1, 0, cx + 1, 4, ROT); m.rect(cx - 5, 8, cx + 5, 8, STEIN2)  # Helm mit Busch
        m.rect(cx + 8, 8, cx + 8, 24, STEIN); m.rect(cx + 6, 24, cx + 10, 25, GOLD2)                # Schwert
        m.rect(cx - 12, 17, cx - 7, 25, 'S+'); m.rect(cx - 12, 17, cx - 12, 25, STEIN3); m.set(cx - 10, 20, WEISS)
    elif rolle == 'haendler':
        m.disc(cx - 10, 24, 4, HOLZ2); m.rect(cx - 12, 19, cx - 8, 20, HOLZ); m.disc(cx - 10, 25, 1.6, GOLD)
        m.rect(cx + 8, 18, cx + 10, 20, GOLD); m.rect(cx + 8, 18, cx + 8, 20, GOLD2)
        m.rect(cx - 5, 5, cx + 5, 6, 'S--')
    elif rolle == 'admiral':
        m.rect(cx - 6, 5, cx + 6, 7, OUT); m.rect(cx - 3, 3, cx + 3, 5, OUT); m.set(cx, 4, GOLD)
        m.rect(cx + 8, 8, cx + 8, 28, STEIN2); m.rect(cx + 5, 10, cx + 11, 10, STEIN2); m.rect(cx + 5, 26, cx + 11, 28, STEIN2)
        m.set(cx + 5, 24, STEIN2); m.set(cx + 11, 24, STEIN2)                                       # Anker
        m.rect(cx - 12, 22, cx - 7, 26, WASSER)
    elif rolle == 'kuenstler':
        m.disc(cx - 10, 23, 4.5, HOLZ); m.set(cx - 12, 22, ROT); m.set(cx - 10, 21, BLAU); m.set(cx - 9, 24, GRUEN); m.set(cx - 11, 25, GOLD)
        m.rect(cx + 8, 12, cx + 8, 26, HOLZ2); m.rect(cx + 8, 10, cx + 8, 11, ROT)                 # Pinsel
        m.rect(cx - 6, 5, cx + 6, 6, 'S+')                                                          # Barett
    elif rolle == 'heilerin':
        m.rect(cx - 1, 25, cx + 1, 29, WEISS); m.rect(cx - 2, 26, cx + 2, 28, WEISS); m.rect(cx, 26, cx, 28, ROT); m.rect(cx - 1, 27, cx + 1, 27, ROT)  # Kreuz
        m.disc(cx - 10, 24, 3, GOLD2); m.disc(cx - 10, 24, 1.6, FEUER2)                             # Lampe
        m.rect(cx - 10, 17, cx - 10, 20, STEIN3)
        m.rect(cx - 5, 5, cx + 5, 7, WEISS)
    elif rolle == 'musiker':
        m.disc(cx - 10, 26, 2.2, OUT); m.rect(cx - 9, 14, cx - 8, 26, OUT); m.rect(cx - 8, 14, cx - 5, 16, OUT)   # Note
        m.rect(cx + 8, 16, cx + 9, 28, HOLZ); m.disc(cx + 8, 28, 3, HOLZ); m.rect(cx + 8, 20, cx + 8, 28, HOLZ2)     # Laute
        m.rect(cx - 5, 5, cx + 5, 6, 'S+')
    m.kontur()
    return m.sprite()

def stern5(m, cx, cy, r, c):
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * .42; pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr))
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            inside = False; j = len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]; xj, yj = pts[j]
                if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi): inside = not inside
                j = i
            if inside: m.set(x, y, c)

def emblem(name):
    N = 32; m = Mal(N, N); cx = 15.5
    if name == 'zelt':
        m.tri(15, 5, 27, 12, 'S'); m.tri(15, 14, 27, 5, WEISS); m.rect(14, 22, 17, 27, 'S--')
        m.rect(15, 1, 15, 5, HOLZ); m.rect(16, 1, 17, 3, FEUER); m.set(18, 2, FEUER2)
        m.rect(5, 27, 26, 28, HOLZ2)
    elif name == 'saeulen':
        m.tri(15, 4, 11, 13, STEIN)
        m.rect(3, 11, 28, 12, STEIN2)
        for x in (5, 12, 19, 26): m.rect(x - 1, 13, x + 1, 25, WEISS); m.rect(x - 1, 13, x - 1, 25, STEIN)
        m.rect(2, 26, 29, 28, STEIN2); m.rect(1, 29, 30, 30, STEIN)
        m.set(15, 7, GOLD)
    elif name == 'schild':
        for y in range(4, 27):
            w = 10 if y < 16 else max(0, 10 - (y - 16))
            m.rect(15 - w, y, 15 + w, y, 'S')
        m.rect(5, 4, 25, 6, 'S+'); m.rect(14, 8, 17, 24, WEISS); m.rect(8, 12, 23, 14, WEISS)
        m.rect(14, 8, 14, 24, STEIN2)
    elif name == 'krone':
        m.rect(5, 14, 26, 24, GOLD); m.rect(5, 14, 5, 24, GOLD2); m.rect(26, 14, 26, 24, GOLD2)
        for x0 in (5, 14, 23): m.tri(x0 + 1, 6, 14, 3, GOLD)
        m.rect(5, 22, 26, 24, GOLD2)
        m.set(10, 18, ROT); m.set(15, 17, BLAU); m.set(21, 18, GRUEN)
        for x in (6, 15, 24): m.disc(x, 6, 1.4, FEUER2)
    elif name == 'muenze':
        for k, (x, y) in enumerate(((10, 22), (20, 22), (15, 14))):
            m.disc(x, y, 6.2, GOLD2); m.disc(x, y - 1, 5.2, GOLD); m.set(x, y - 1, FEUER2); m.rect(x - 1, y - 3, x - 1, y + 1, GOLD2)
    elif name == 'tempel':
        m.tri(15, 5, 12, 12, STEIN); m.rect(3, 12, 28, 13, STEIN2)
        for x in (6, 12, 19, 25): m.rect(x - 1, 14, x, 25, WEISS)
        m.rect(2, 26, 29, 28, STEIN2); m.disc(15, 10, 2.2, GOLD); m.disc(15, 10, 1.1, FEUER2)
        m.rect(14, 0, 16, 1, GOLD); m.rect(5, 2, 6, 3, GOLD); m.rect(25, 2, 26, 3, GOLD)
    elif name == 'urne':
        m.rect(5, 12, 26, 27, HOLZ); m.rect(5, 12, 26, 14, HOLZ2); m.rect(11, 12, 20, 12, OUT); m.rect(5, 25, 26, 27, HOLZ2)
        m.rect(10, 4, 19, 12, WEISS); m.rect(11, 6, 17, 6, STEIN3); m.rect(11, 8, 17, 8, STEIN3); m.rect(11, 10, 15, 10, STEIN3)
        m.rect(12, 18, 19, 22, 'S')
        m.set(14, 20, WEISS); m.set(15, 21, WEISS); m.set(16, 20, WEISS); m.set(17, 19, WEISS)
    elif name == 'stern':
        stern5(m, 15.5, 16.5, 14, ROT); stern5(m, 15.5, 17, 8.5, FEUER2)
    m.kontur()
    return m.sprite()

NAMEN_R = ['zelt', 'saeulen', 'schild', 'krone', 'muenze', 'tempel', 'urne', 'stern']
NAMEN_P = ['schriftsteller', 'ingenieur', 'wissenschaftler', 'general', 'haendler', 'admiral', 'kuenstler', 'heilerin', 'musiker']
def lade():
    for n in NAMEN_R: spr._S['civ:reg_' + n] = emblem(n)
    for n in NAMEN_P: spr._S['civ:person_' + n] = figur(n)
lade()

def webexport(pfad):
    """Fügt die Civ-Sprites in die sprites.json der Website ein (Palette-String-Format)."""
    out = {}
    for key in [k for k in spr._S if k.startswith('civ:')]:
        sp = spr._S[key]; pal = []; d = ''
        for c in sp['feld']:
            if c is None: d += '.'; continue
            if c not in pal: pal.append(c)
            d += chr(48 + pal.index(c))
        out[key] = dict(w=sp['w'], h=sp['h'], p=pal, d=d)
    b = json.load(open(pfad)); b.update(out); json.dump(b, open(pfad, 'w'), separators=(',', ':')); return len(out)

if __name__ == '__main__':
    from PIL import Image
    ks = [k for k in spr._S if k.startswith('civ:')]; S = 6
    im = Image.new('RGB', (8 * 34 * S, 3 * 40 * S + 10), (214, 205, 180)); x = y = 0
    for i, k in enumerate(ks):
        t = spr.sprite(k, '#2c7a68'); t = t.resize((t.width * S, t.height * S), Image.NEAREST)
        im.paste(t, ((i % 8) * 34 * S, (i // 8) * 40 * S), t)
    im.save('/tmp/rel/civspr.png'); print(len(ks))
