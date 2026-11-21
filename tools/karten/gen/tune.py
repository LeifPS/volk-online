import sim, statistics, itertools, sys, json
from collections import Counter
R = sim.R
KARTEN = {k['id']: k for k in sim.S['karten']}
def messen(n, spiele=250):
    res = sim.lauf(n, spiele)
    runden = [g.runde for g in res]; gr = Counter(g.grund or 'KEIN' for g in res)
    alter = statistics.mean(max(p.alter for p in g.sp) for g in res)
    spät = 0; ges = 0
    for g in res:
        for k, v in g.log.items():
            if k.startswith('gespielt:') and k[9:] in KARTEN and KARTEN[k[9:]]['typ'] != 'land':
                ges += v; spät += v if KARTEN[k[9:]]['zeitalter'] >= 4 else 0
    return f"R{statistics.median(runden):.0f}/{max(runden)} K{100*gr['Kultur']//spiele}% E{100*gr['Eroberung']//spiele}% Alter{alter:.1f} spät{100*spät//max(1,ges)}%"
def setze(**kw): R.update(kw)
if __name__ == '__main__':
    for aufst, ks, hp in [([4,6,8,10,12,14],12,25), ([3,4,5,6,7,8],14,25), ([3,4,5,6,7,8],16,25), ([3,4,6,7,8,10],15,25), ([3,5,6,8,9,10],16,20), ([3,4,5,6,7,8],16,20), ([2,3,4,5,6,7],16,25), ([2,3,4,5,6,7],18,25)]:
        setze(aufstieg=aufst, kultur_sieg=ks, stadt_hp=hp)
        print(f'Aufstieg {aufst} Kultur {ks} HP {hp}:', '2p', messen(2), '| 3p', messen(3), '| 4p', messen(4))
