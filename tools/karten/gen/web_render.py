"""Rendert alle Karten 1:1 wie im Druck als WebP für die Website (public/karten/)."""
import os, sys, subprocess, shutil, json
from reportlab.pdfgen import canvas
from PIL import Image
from lib import *
import karten, volkblatt, relblatt, tafel, civ
from volk_karten import nach_volk
import religionen as RL

AUS = sys.argv[1]; BREITE = int(sys.argv[2]) if len(sys.argv) > 2 else 520
os.makedirs(AUS, exist_ok=True)
TMP = '/tmp/webkarten'; shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
liste = []   # (dateiname, funktion, (breite_pt, hoehe_pt))
seen = set()
def add(name, fn, gr=(CW, CH)):
    assert name not in seen, name; seen.add(name); liste.append((name, fn, gr))

for k in SATZ['karten'] + SATZ['wunder'] + SATZ['staaten'] + SATZ['ereignisse']:
    nm = k['id'] if k['id'] not in seen else '%s_s%d' % (k['id'], k['stapel'])
    add(nm, lambda c, k=dict(k): karten.zeichne_vorn(c, k))
d = nach_volk()
for vid, ks in d.items():
    for k in ks: add(k['id'], lambda c, k=dict(k): karten.zeichne_vorn(c, k))
    add('info_' + vid, lambda c, vid=vid: volkblatt.info(c, vid))
    add('liste_' + vid, lambda c, vid=vid: volkblatt.liste(c, vid))
    add('rueck_v_' + vid, lambda c, vid=vid: volkblatt.ruecken(c, vid))
for k in relblatt.RKARTEN: add(k['id'], lambda c, k=dict(k): karten.zeichne_vorn(c, k))
for r in relblatt.REL:
    rid = r['id']
    add('reltafel_' + rid, lambda c, rid=rid: relblatt.tafelkarte(c, rid))
    add('relliste_' + rid, lambda c, rid=rid: relblatt.uebersicht(c, rid))
    add('rueck_r_' + rid, lambda c, rid=rid: relblatt.ruecken(c, rid))
for e in SATZ.get('rel_ereignisse', []):
    add(e['id'], lambda c, e=e: relblatt.ereigniskarte(c, e))
add('rueck_rev', relblatt.ruecken_ereignis)
import civblatt
_R, _P, _N = civ.baue()
for k in _R + _P + _N: add(k['id'], lambda c, k=dict(k): karten.zeichne_vorn(c, k))
for t in ('regierung', 'person', 'natur'): add('rueck_c_' + t, lambda c, t=t: civblatt.ruecken(c, t))
for st in (1, 2, 3, 0): add('rueck_%d' % st, lambda c, st=st: karten.zeichne_ruecken(c, st))
for v in SATZ['voelker']:
    add('tafel_' + v['id'], lambda c, v=v: tafel.tafel_vorn(c, v), (tafel.PW, tafel.PH))

print(len(liste), 'Bilder')
for n, (name, fn, (w, h)) in enumerate(liste):
    pdf = os.path.join(TMP, 'p.pdf'); c = canvas.Canvas(pdf, pagesize=(w, h))
    p = c.beginPath(); p.rect(0, 0, w, h); c.clipPath(p, stroke=0, fill=0)
    fn(c); c.showPage(); c.save()
    breite = BREITE * (1.9 if w > CW else 1)
    dpi = breite / (w / 72)
    subprocess.run(['pdftoppm', '-r', '%.2f' % dpi, '-png', '-singlefile', pdf, os.path.join(TMP, 'o')], check=True)
    im = Image.open(os.path.join(TMP, 'o.png')).convert('RGB')
    im.save(os.path.join(AUS, name + '.webp'), 'WEBP', quality=88, method=6)
    if n % 40 == 0: print(n, name, im.size, flush=True)
json.dump([l[0] for l in liste], open(os.path.join(AUS, 'index.json'), 'w'))
