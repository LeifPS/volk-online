import sys, statistics
from collections import Counter
import sim
def messe(n, spiele, **kw):
    w = Counter(); a = Counter(); gr = Counter(); runden = []; kult = Counter()
    for i in range(spiele):
        g = sim.Spiel(n, 1000 + i, kw).spiele_durch()
        for p in g.sp: a[p.volk] += 1
        if g.sieger: w[g.sieger.volk] += 1; gr[g.grund] += 1
        else: gr['kein'] += 1
        runden.append(g.runde)
    print(f'n={n} {kw} Runden Median {statistics.median(runden)} Sieg {dict(gr)}')
    print('  Siegquote je Volk (Soll %.0f%%):' % (100 / n), {v: round(100 * w[v] / a[v]) for v in sorted(a)})
for n in (2, 3, 4):
    messe(n, int(sys.argv[1]) if len(sys.argv) > 1 else 400, ohne_volkskarten=True)
    messe(n, int(sys.argv[1]) if len(sys.argv) > 1 else 400)
