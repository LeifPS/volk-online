"""Pixel-Symbole der Erweiterungen (16x16) für die Fußzeile der Karten: 1 Volkskarten, 2 Götter & Glaube, 3 Zivilisation."""
import spr, relspr
from relspr import Mal

def _aus(zeilen, farben):
    m = Mal(16, 16)
    for y, z in enumerate(zeilen):
        for x, ch in enumerate(z):
            if ch != '.': m.set(x, y, farben[ch])
    m.kontur('#1c1a26')
    return m.sprite()

# 1 · Volkskarten: Volksbanner an einer Stange
FAHNE = [
    '................',
    '.......YY.......',
    '.......YY.......',
    '.....DHHHHHH....',
    '.....DBBBLBBBB..',
    '.....DBBLLLBBBB.',
    '.....DBBBLBBBB..',
    '.....DBBBBBBB...',
    '.....DBBBBB.....',
    '.....DBBB.......',
    '.....D..........',
    '.....D..........',
    '.....D..........',
    '....DDD.........',
    '...MMMMM........',
    '................',
]
# 3 · Zivilisation: Tempel mit vier Säulen
TEMPEL = [
    '................',
    '.......PP.......',
    '......PPPP......',
    '.....PPLLPP.....',
    '....PPLLLLPP....',
    '...PPPPPPPPPP...',
    '..LLLLLLLLLLLL..',
    '...SC.SC.SC.SC..',
    '...SC.SC.SC.SC..',
    '...SC.SC.SC.SC..',
    '...SC.SC.SC.SC..',
    '...SC.SC.SC.SC..',
    '..LLLLLLLLLLLL..',
    '.PPPPPPPPPPPPPP.',
    '................',
    '................',
]
def lade():
    spr._S['mod:1'] = _aus(FAHNE, dict(Y='#f2c14e', D='#6b4420', H='#9ccbe0', B='#2f6f8f', L='#5fa8c9', M='#8c7f68'))
    spr._S['mod:2'] = spr._S['rel:glaube']
    spr._S['mod:3'] = _aus(TEMPEL, dict(P='#6a52b8', L='#efe9f8', S='#e2d9f0', C='#b3a5d6'))
lade()
