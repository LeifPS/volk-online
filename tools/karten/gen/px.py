"""Kleines Pixel-Zeichenwerkzeug für die Zeitalter VIII bis XI (Zukunft).
Alle Motive werden im Code aus Formen zusammengesetzt (kein externes Bildmaterial) und deterministisch erzeugt.
'S', 'S-', 'S+', 'S--' sind die Spielerfarbe, alles andere sind feste Farben."""
import math
from relspr import Mal

OUT = '#1c1a26'
def _h(c):
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
def mixc(a, b, t):
    A, B = _h(a), _h(b); return '#%02x%02x%02x' % tuple(round(A[i] + (B[i] - A[i]) * t) for i in range(3))
def hell(c, t=.3): return mixc(c, '#ffffff', t)
def dunkel(c, t=.3): return mixc(c, '#000000', t)

class Px(Mal):
    """Mal mit Linien, Ellipsen, Polygonen, Spiegeln und Farbverlauf-Schattierung."""
    def line(s, x0, y0, x1, y1, c):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) or 1
        for i in range(n + 1): s.set(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)
    def ell(s, cx, cy, rx, ry, c):
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                if ((x - cx) / max(rx, .5)) ** 2 + ((y - cy) / max(ry, .5)) ** 2 <= 1.05: s.set(x, y, c)
    def poly(s, pts, c):
        ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            xs = []
            for i in range(len(pts)):
                (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
                if (y0 <= y < y1) or (y1 <= y < y0): xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(int(round(xs[i])), int(round(xs[i + 1])) + 1): s.set(x, y, c)
    def spiegel(s, achse=15.5):
        """Spiegelt alles, was links der Achse liegt, nach rechts (nur Pixel, die rechts noch leer sind)."""
        for (x, y), c in list(s.p.items()):
            if x <= achse:
                q = (int(round(2 * achse - x)), y)
                if q not in s.p and 0 <= q[0] < s.w: s.p[q] = c
    def verlauf_v(s, x0, y0, x1, y1, oben, unten):
        n = max(1, y1 - y0)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): s.set(x, y, mixc(oben, unten, (y - y0) / n))
    def lichter(s, pts, c):
        for x, y in pts: s.set(x, y, c)
    def schatten_boden(s, cx, y, rx, c='#2a2630'):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            if abs(x - cx) < rx: s.set(x, y, c)
    def glimmer(s, x, y, c1, c2=None):
        s.set(x, y, c1)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): s.set(x + dx, y + dy, c2 or hell(c1, .4))
    def fertig(s, kontur=True):
        if kontur: s.kontur(OUT)
        return s.sprite()

def sterne_hintergrund(m, n=10, seed=1, farbe='#ffffff'):
    import random
    r = random.Random(seed)
    for _ in range(n): m.set(r.randrange(1, m.w - 1), r.randrange(1, m.h - 1), farbe)
