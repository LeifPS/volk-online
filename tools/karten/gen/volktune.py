import sys, copy, json
from collections import Counter
import sim
BASE = copy.deepcopy(sim.S['volkskarten'])
def lauf(n, spiele):
    w = Counter(); a = Counter()
    for i in range(spiele):
        g = sim.Spiel(n, 5000 + i, {}).spiele_durch()
        for p in g.sp: a[p.volk] += 1
        if g.sieger: w[g.sieger.volk] += 1
    return {v[:4]: round(100 * w[v] / a[v]) for v in sorted(a)}
def mit(aendere, n=4, spiele=500):
    sim.S['volkskarten'] = copy.deepcopy(BASE)
    for k in sim.S['volkskarten']: aendere(k)
    return lauf(n, spiele)
def setze(volk, id=None, **kw):
    def f(k):
        if k['volk'] == volk and (id is None or k['id'] == id):
            for a, b in kw.items():
                if a in ('effekte', 'boni'): k[a] = dict(k[a], **b)
                else: k[a] = b
    return f
def kette(*fs):
    return lambda k: [f(k) for f in fs]
if __name__ == '__main__':
    print('basis', mit(lambda k: None))
    print('gold ohne ziehen', mit(setze('goldener_bund', ziehen=0)))
    print('steppen +E', mit(kette(setze('steppenreiter', 'sr_zeltlager', effekte={'E': 2}), setze('steppenreiter', 'sr_stahlwerk', effekte={'E': 2}))))
    print('steppen einkommen units', mit(setze('steppenreiter', 'sr_pferdebogner', einkommen=1)))
