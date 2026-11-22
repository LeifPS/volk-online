"""Randkorrektur für Sprites: Kein Motiv darf ohne Kontur am Bildrand enden.
Erst wird das Motiv um bis zu 2 Pixel verschoben (wo Platz ist), danach bekommen verbliebene Randpixel die Konturfarbe."""
OUTS = ('#2b2118', '#1c1a26')
AUSNAHMEN = ('za:', 'ui:')

def _rand_n(feld, w, h, outs):
    n = 0
    for i, c in enumerate(feld):
        if c is None or c in outs: continue
        x, y = i % w, i // w
        if x in (0, w - 1) or y in (0, h - 1): n += 1
    return n

def _schiebe(feld, w, h, dx, dy):
    neu = [None] * (w * h); verlust = 0
    for i, c in enumerate(feld):
        if c is None: continue
        x, y = i % w + dx, i // w + dy
        if 0 <= x < w and 0 <= y < h: neu[y * w + x] = c
        else: verlust += 1
    return neu, verlust

def repariere(feld, w, h):
    outs = OUTS
    if not _rand_n(feld, w, h, outs): return feld
    zaehl = {o: sum(1 for c in feld if c == o) for o in OUTS}
    out = max(zaehl, key=zaehl.get) if any(zaehl.values()) else OUTS[0]
    beste = None
    for dy in (0, -1, 1, -2, 2):
        for dx in (0, 1, -1, 2, -2):
            f2, verlust = _schiebe(feld, w, h, dx, dy)
            if verlust and any(c not in outs for c in [feld[i] for i in range(len(feld)) if feld[i] is not None and not (0 <= i % w + dx < w and 0 <= i // w + dy < h)]):
                continue      # nichts außer Kontur darf hinausgeschoben werden
            wert = _rand_n(f2, w, h, outs) * 10 + abs(dx) + abs(dy) + (1 if dy > 0 else 0)
            if beste is None or wert < beste[0]: beste = (wert, f2)
    feld = beste[1]
    # verbliebene Randpixel werden Kontur
    for i, c in enumerate(feld):
        if c is None or c in outs: continue
        x, y = i % w, i // w
        if x in (0, w - 1) or y in (0, h - 1): feld[i] = out
    # Kontur um alle Nicht-Kontur-Pixel ergänzen (verschobene Teile)
    neu = list(feld)
    for i, c in enumerate(feld):
        if c is None or c in outs: continue
        x, y = i % w, i // w
        for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            qx, qy = x + ax, y + ay
            if 0 <= qx < w and 0 <= qy < h and feld[qy * w + qx] is None: neu[qy * w + qx] = out
    return neu

def repariere_sprite(key, sp):
    if key.startswith(AUSNAHMEN): return sp
    sp['feld'] = repariere(list(sp['feld']), sp['w'], sp['h']); return sp

def repariere_json(pfad):
    """public/data/sprites.json (Palette-String-Format) reparieren."""
    import json
    S = json.load(open(pfad)); n = 0
    for k, s in S.items():
        if k.startswith(AUSNAHMEN): continue
        feld = [None if ch == '.' else s['p'][ord(ch) - 48] for ch in s['d']]
        f2 = repariere(list(feld), s['w'], s['h'])
        if f2 == feld: continue
        n += 1; pal = []; d = ''
        for c in f2:
            if c is None: d += '.'; continue
            if c not in pal: pal.append(c)
            d += chr(48 + pal.index(c))
        s['p'] = pal; s['d'] = d
    json.dump(S, open(pfad, 'w'), separators=(',', ':')); return n

if __name__ == '__main__':
    import sys; print(repariere_json(sys.argv[1]), 'Sprites repariert')
