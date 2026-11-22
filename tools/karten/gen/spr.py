import json, os
from PIL import Image
_S = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'sprites.json')))
import rand as _rand
for _k in list(_S): _rand.repariere_sprite(_k, _S[_k])
def _rgb(h):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(c*2 for c in h)
    return tuple(int(h[i:i+2],16) for i in (0,2,4))
def _mix(a,b,t): return tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def toene(farbe):
    f=_rgb(farbe)
    return {'S':f,'S-':_mix(f,(0,0,0),.35),'S+':_mix(f,(255,255,255),.35),'S--':_mix(f,(0,0,0),.6)}
def hat(k): return k in _S
def sprite(key, farbe='#2f6fd0'):
    s=_S[key]; t=toene(farbe); w,h=s['w'],s['h']
    im=Image.new('RGBA',(w,h),(0,0,0,0)); px=im.load()
    for i,c in enumerate(s['feld']):
        if not c: continue
        rgb = t[c] if c in t else _rgb(c)
        px[i%w,i//w]=rgb+(255,)
    return im
def bbox_crop(im):
    b=im.getbbox()
    return im.crop(b) if b else im
