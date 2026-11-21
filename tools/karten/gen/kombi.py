import sys; sys.path.insert(0,'.')
import sim
from collections import Counter
def lauf(n, spiele, vk, rel):
    gr = Counter(); rn = []; w = Counter(); a = Counter(); fehler = 0; ende = 0
    for i in range(spiele):
        opt = {}
        if not vk: opt['ohne_volkskarten'] = True
        if rel: opt['religion'] = True
        try:
            g = sim.Spiel(n, 500 + i, opt).spiele_durch()
        except Exception as e:
            fehler += 1; print('FEHLER', n, vk, rel, repr(e)); continue
        gr[g.grund] += 1; rn.append(g.runde)
        for p in g.sp: a[p.volk] += 1
        if g.sieger: w[g.sieger.volk] += 1
    rn.sort()
    q = {v[:4]: round(100 * w[v] / a[v]) for v in sorted(a)}
    print(f'n={n} VK={int(vk)} REL={int(rel)} | Sieg {dict(gr)} | Runden Median {rn[len(rn)//2]} Max {rn[-1]} | Fehler {fehler} | Quote {q}')
if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    for n in (2, 3, 4):
        for vk in (False, True):
            for rel in (False, True): lauf(n, N, vk, rel)
