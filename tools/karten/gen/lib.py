"""Gemeinsame Zeichenhilfen: Schriften, Sprites als Bilder, Texte, Farben."""
import os, io, json
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.lib import colors
from reportlab.lib.units import mm
import spr
import zukunft_spr
zukunft_spr.lade()

HIER = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HIER, '..', 'fonts')
pdfmetrics.registerFont(TTFont('PX', os.path.join(FD, 'pixelzahl-500.ttf')))
pdfmetrics.registerFont(TTFont('PXB', os.path.join(FD, 'pixelzahl-700.ttf')))
pdfmetrics.registerFont(TTFont('VT', os.path.join(FD, 'vt323-400.ttf')))
pdfmetrics.registerFont(TTFont('SS', os.path.join(FD, 'silkscreen-700.ttf')))
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf'))
pdfmetrics.registerFont(TTFont('DVB', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVI', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Oblique.ttf'))

CW, CH = 63 * mm, 88 * mm
SATZ = json.load(open(os.path.join(HIER, '..', 'kartensatz.json')))
ZA = SATZ['zeitalter']
ROEM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']
R = SATZ['regeln']

def hexc(h): return colors.HexColor(h)
def mix(a, b, t):
    A = spr._rgb(a); B = spr._rgb(b)
    return '#%02x%02x%02x' % tuple(round(A[i] + (B[i] - A[i]) * t) for i in range(3))
THEMA = {'pixel': False}   # True = digitales Pixel-Design (nur für web_render)
def stufenrect(c, x, y, w, h, u, fill=None, stroke=None, lw=.4):
    """Rechteck mit treppenförmigen Ecken (Pixel-UI-Look)."""
    p = c.beginPath()
    pts = [(2*u,0),(w-2*u,0),(w-2*u,u),(w-u,u),(w-u,2*u),(w,2*u),(w,h-2*u),(w-u,h-2*u),(w-u,h-u),(w-2*u,h-u),(w-2*u,h),(2*u,h),(2*u,h-u),(u,h-u),(u,h-2*u),(0,h-2*u),(0,2*u),(u,2*u),(u,u),(2*u,u)]
    p.moveTo(x+pts[0][0], y+pts[0][1])
    for a,b in pts[1:]: p.lineTo(x+a, y+b)
    p.close()
    c.saveState()
    if fill: c.setFillColor(hexc(fill))
    if stroke: c.setStrokeColor(hexc(stroke)); c.setLineWidth(lw)
    c.drawPath(p, stroke=1 if stroke else 0, fill=1 if fill else 0)
    c.restoreState()

def hell(c, t=.5): return mix(c, '#ffffff', t)
def dunkel(c, t=.35): return mix(c, '#000000', t)

_bild = {}
def bild(key, farbe='#2f6fd0', zuschnitt=True, faktor=10):
    """Sprite als hochskaliertes (Nearest) Bild + Seitenverhältnis. Liefert (ImageReader, breite_px, hoehe_px)."""
    k = (key, farbe, zuschnitt, faktor)
    if k in _bild: return _bild[k]
    im = spr.sprite(key, farbe)
    if zuschnitt: im = spr.bbox_crop(im)
    w, h = im.size
    big = im.resize((w * faktor, h * faktor), Image.NEAREST)
    buf = io.BytesIO(); big.save(buf, 'PNG'); buf.seek(0)
    _bild[k] = (ImageReader(buf), w, h)
    return _bild[k]

def zeichne_bild(c, key, x, y, breite, hoehe, farbe='#2f6fd0', zuschnitt=True, ausrichtung='mitte', faktor=10, ganzzahl=False):
    """Zeichnet ein Sprite in die Box (x,y,breite,hoehe) so groß wie möglich (Seitenverhältnis bleibt)."""
    ir, w, h = bild(key, farbe, zuschnitt, faktor)
    s = min(breite / w, hoehe / h)
    dw, dh = w * s, h * s
    if ausrichtung == 'mitte': ox, oy = (breite - dw) / 2, (hoehe - dh) / 2
    elif ausrichtung == 'unten': ox, oy = (breite - dw) / 2, 0
    else: ox, oy = 0, 0
    c.drawImage(ir, x + ox, y + oy, dw, dh, mask='auto')
    return s

def icon(c, name, x, y, groesse, farbe='#2f6fd0'):
    """ui-Symbol (16x16) mit linker unterer Ecke (x,y)."""
    zeichne_bild(c, name if ':' in name else 'ui:' + name, x, y, groesse, groesse, farbe, zuschnitt=False, faktor=8)

def text_passt(text, font, size, breite): return pdfmetrics.stringWidth(text, font, size) <= breite
def fit(c, text, font, maxsize, minsize, breite):
    s = maxsize
    while s > minsize and not text_passt(text, font, s, breite): s -= .25
    return s
def zentriert(c, text, x, y, font, size, farbe='#222222'):
    c.setFillColor(hexc(farbe)); c.setFont(font, size); c.drawCentredString(x, y, text)
def links(c, text, x, y, font, size, farbe='#222222'):
    c.setFillColor(hexc(farbe)); c.setFont(font, size); c.drawString(x, y, text)
def rechts(c, text, x, y, font, size, farbe='#222222'):
    c.setFillColor(hexc(farbe)); c.setFont(font, size); c.drawRightString(x, y, text)

def absatz(c, text, x, y_oben, breite, font='DV', size=6.3, lead=None, farbe='#222222', fett_bis=None):
    """Mehrzeiliger Text ab y_oben nach unten. fett_bis: Zeichen bis zu denen (z. B. 'Ansturm:') fett gesetzt wird. Gibt y unten zurück."""
    lead = lead or size * 1.17
    zeilen = simpleSplit(text, font, size, breite)
    y = y_oben - size
    first = True
    for z in zeilen:
        if first and fett_bis and ':' in z:
            k = z.index(':') + 1
            c.setFillColor(hexc(farbe)); c.setFont('DVB', size); c.drawString(x, y, z[:k])
            w = pdfmetrics.stringWidth(z[:k], 'DVB', size)
            c.setFont(font, size); c.drawString(x + w, y, z[k:])
        else:
            c.setFillColor(hexc(farbe)); c.setFont(font, size); c.drawString(x, y, z)
        first = False; y -= lead
    return y + size - lead + lead  # y der Unterkante der letzten Zeile

def absatz_hoehe(text, breite, font='DV', size=6.3, lead=None):
    lead = lead or size * 1.17
    return len(simpleSplit(text, font, size, breite)) * lead

def rrect(c, x, y, w, h, r, fill=None, stroke=None, lw=.4):
    c.saveState()
    if fill: c.setFillColor(hexc(fill))
    if stroke: c.setStrokeColor(hexc(stroke)); c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, stroke=1 if stroke else 0, fill=1 if fill else 0)
    c.restoreState()
def kreis(c, x, y, r, fill=None, stroke=None, lw=.5):
    c.saveState()
    if fill: c.setFillColor(hexc(fill))
    if stroke: c.setStrokeColor(hexc(stroke)); c.setLineWidth(lw)
    c.circle(x, y, r, stroke=1 if stroke else 0, fill=1 if fill else 0)
    c.restoreState()

SYMBOL_NAMEN = {'holz': 'Holz', 'stein': 'Stein', 'marmor': 'Marmor', 'kupfer': 'Kupfer', 'zinn': 'Zinn', 'eisen': 'Eisen', 'pferde': 'Pferde',
                'salpeter': 'Salpeter', 'kohle': 'Kohle', 'oel': 'Öl', 'aluminium': 'Aluminium', 'uran': 'Uran', 'elefanten': 'Elefanten',
                'seltene_erden': 'Seltene Erden', 'deuterium': 'Deuterium', 'titan': 'Titan', 'helium3': 'Helium-3',
                'kueste': 'Küste', 'flug': 'Flugfeld'}
def symbol_icon(s): return {'kueste': 'see', 'flug': 'luft'}.get(s, s)


# ---- Zeitalter-Symbole I–VII (16x16 Pixelart, von Leif geliefert) ----
_ZA_DATEIEN = ['epoche_1_I.png', 'epoche_2_II.png', 'epoche_3_III.png', 'epoche_4_IV.png', 'epoche_5_V.png', 'epoche_6_VI.png', 'epoche_7_VII.png',
               'epoche_8_VIII.png', 'epoche_9_IX.png', 'epoche_10_X.png', 'epoche_11_XI.png']
_za_bild = {}
def za_png(z, faktor=12, pfad=False):
    """Zeitalter-Symbol z (0..6) als scharf hochskaliertes Bild (Nearest). pfad=True: Datei für <img> in Absätzen."""
    k = (z, faktor, pfad)
    if k in _za_bild: return _za_bild[k]
    im = Image.open(os.path.join(HIER, '..', 'epochen', _ZA_DATEIEN[z])).convert('RGBA')
    im = im.resize((16 * faktor, 16 * faktor), Image.NEAREST)
    if pfad:
        import tempfile
        f = os.path.join(tempfile.gettempdir(), 'za_%d.png' % z); im.save(f); r = f
    else:
        b = io.BytesIO(); im.save(b, 'PNG'); b.seek(0); r = ImageReader(b)
    _za_bild[k] = r
    return r
def za_icon(c, z, cx, cy, s):
    """Zeichnet das Symbol des Zeitalters z (0..6) mit Mittelpunkt (cx, cy) und Kantenlänge s."""
    c.drawImage(za_png(z), cx - s / 2, cy - s / 2, s, s, mask='auto')
def za_inline(z, h=11):
    """Für Paragraph-Text: <img>-Tag mit dem Zeitalter-Symbol."""
    return '<img src="%s" width="%d" height="%d" valign="middle"/>' % (za_png(z, pfad=True), h, h)
