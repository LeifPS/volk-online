import sys; sys.path.insert(0,'.')
import sim
from collections import Counter
def messe(n, spiele, **kw):
    gr = Counter(); lg = Counter(); rn = []; w = Counter(); a = Counter(); rw = Counter(); ra = Counter()
    for i in range(spiele):
        g = sim.Spiel(n, 100 + i, dict(religion=True, **kw)).spiele_durch(); gr[g.grund] += 1; rn.append(g.runde); lg.update(g.log)
        for p in g.sp:
            a[p.volk] += 1
            if p.religion: ra[p.religion] += 1
        if g.sieger: w[g.sieger.volk] += 1
        if g.sieger and g.sieger.religion: rw[g.sieger.religion] += 1
    print(f'n={n} {kw} Sieg {dict(gr)} Runden-Median {sorted(rn)[len(rn)//2]} pro Spiel', {k: round(v / spiele, 1) for k, v in lg.items() if k in ('gegruendet', 'mission', 'ausweisung', 'rel_gezogen')})
    print('   Volk-Siegquote', {v[:4]: round(100 * w[v] / a[v]) for v in sorted(a)})
    print('   Religion: Siege/Gründungen', {r[:5]: f'{rw[r]}/{ra[r]}' for r in sorted(ra)})
if __name__ == '__main__':
    for n in (2, 3, 4): messe(n, int(sys.argv[1]) if len(sys.argv) > 1 else 300)
