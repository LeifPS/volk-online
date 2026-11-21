"""Vorschau der neuen Zukunfts-Sprites: python3 zk_vorschau.py ausgabe.png praefix [skala] [alt_vergleich]"""
import sys, json, importlib
from PIL import Image, ImageDraw
from zk_basis import Bild
MODS = ['zk_einheiten', 'zk_gebaeude', 'zk_welt']
def alle():
    neu = {}
    for n in MODS:
        try: neu.update(importlib.import_module(n).NEU)
        except ModuleNotFoundError: pass
    return neu
GROESSE = lambda k: (64, 64) if k.startswith('wunder:') else (16, 16) if k.startswith(('rohstoff:', 'za:')) else (64, 56) if k.startswith('stadt:') else (32, 32)
def zeichne(key, fn):
    w, h = GROESSE(key); m = Bild(w, h); fn(m); return m.fertig(kontur=not key.startswith('za:'))
def rgb(h):
    h = h.lstrip('#'); h = ''.join(c * 2 for c in h) if len(h) == 3 else h; return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def mix(a, b, t): return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
F = rgb('#2f6fd0'); T = {'S': F, 'S-': mix(F, (0, 0, 0), .35), 'S+': mix(F, (255, 255, 255), .35), 'S--': mix(F, (0, 0, 0), .6)}
def bild(sp):
    im = Image.new('RGBA', (sp['w'], sp['h']), (0, 0, 0, 0)); px = im.load()
    for i, c in enumerate(sp['feld']):
        if c: px[i % sp['w'], i // sp['w']] = (T[c] if c in T else rgb(c)) + (255,)
    return im
if __name__ == '__main__':
    out, pre = sys.argv[1], sys.argv[2]; sc = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    neu = alle(); keys = [k for k in neu if k.startswith(pre)]
    ims = [(k, bild(zeichne(k, neu[k]))) for k in keys]
    cols = 8 if ims[0][1].width <= 32 else 4
    cw = max(i.width for _, i in ims) * sc + 10; ch = max(i.height for _, i in ims) * sc + 20
    rows = (len(ims) + cols - 1) // cols
    W = Image.new('RGB', (cw * cols, ch * rows), (236, 230, 214)); d = ImageDraw.Draw(W)
    for n, (k, im) in enumerate(ims):
        x = (n % cols) * cw; y = (n // cols) * ch; j = im.resize((im.width * sc, im.height * sc), Image.NEAREST)
        W.paste(j, (x + 5, y + 5), j); d.text((x + 5, y + ch - 14), k.split(':')[1][:22], fill=(0, 0, 0))
    W.save(out); print(len(ims))
