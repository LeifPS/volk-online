"""Kontaktbogen der neuen Zukunfts-Sprites: python3 vorschau.py <ausgabe.png> [praefix ...]"""
import sys
import spr, zukunft_spr
from PIL import Image
zukunft_spr.lade()
out = sys.argv[1]; pre = tuple(sys.argv[2:]) or ('',)
keys = [k for k in zukunft_spr.REG if k.startswith(pre) or any(p in k for p in pre if p)]
S = 4; col = 8
cells = []
for k in keys:
    t = spr.sprite(k, '#2f6fd0'); cells.append((k, t))
cw = max(t.width for _, t in cells) * S + 6; ch = max(t.height for _, t in cells) * S + 6
rows = (len(cells) + col - 1) // col
sheet = Image.new('RGBA', (col * cw, rows * ch), (96, 110, 92, 255))
for i, (k, t) in enumerate(cells):
    t4 = t.resize((t.width * S, t.height * S), Image.NEAREST); sheet.paste(t4, ((i % col) * cw + 3, (i // col) * ch + 3), t4)
sheet.save(out); print(len(cells), sheet.size)
print([k for k, _ in cells])
