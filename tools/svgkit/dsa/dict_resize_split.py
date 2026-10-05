"""Resize figures for content/02-python/03-builtin-structures/dict-hash-table, section dh-s4."""
import sys,os,json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from engine import *
PT,MID,TG,RS='var(--brand)','var(--violet)','var(--filled)','var(--rose)'
LH=20
class Code2:
    def __init__(s,x,y,lines,w): s.x,s.y,s.lines,s.w=x,y,lines,w
    def svg(s):
        o=R(s.x,s.y,s.w,len(s.lines)*LH+14,'var(--bg)',RULE_HI,8)
        for i,l in enumerate(s.lines): o+=T(s.x+14,s.y+22+i*LH,l,TX,'start',mono=True)
        return o
    def bar(s): return R(s.x+4,s.y+8,s.w-8,LH,'rgba(var(--violet-a),.13)','none',4)+R(s.x+4,s.y+8,3,LH,MID,'none',1.5)
def slot(x,y,w,v='',c=None):
    if c is None: return R(x,y,w,34,'none',RULE_HI,4,1.2,'4 3')
    return R(x,y,w,34,'var(--bg)','none',4)+R(x,y,w,34,'rgba(var(--blue-a),.12)' if c==PT else 'rgba(var(--violet-a),.14)',c,4,1.5)+T(x+w/2,y+22,v,c,mono=True,bold=True)
def badge(x,y,txt,c,w=150):
    return R(x,y,w,26,'var(--bg)','none',13)+R(x,y,w,26,'var(--bg)',c,13,1.4)+T(x+w/2,y+18,txt,c,mono=True,bold=True)
KEYS=[('a',4,12),('c',2,10),('d',7,7),('e',0,8),('f',5,13)]
figs={}
# 4.1 load factor
code=Code2(0,40,["d['a'] = 1","d['c'] = 2","d['d'] = 3","d['e'] = 4","d['f'] = 5","d['g'] = 6"],170)
f=Anim('dh-s41-',680,230,'Six keys go into an eight-slot table one per line. After each insert the used count rises: 1/8 up to 5/8. The sixth insert would make 6/8, past two thirds, so the table must grow.','LOAD FACTOR · USED SLOTS ÷ TABLE SIZE',1.6)
f.static(code.svg())
X0,Y0,W=230,90,52
f.static(''.join(slot(X0+i*W,Y0,W) for i in range(8)))
f.static(''.join(T(X0+i*W+W/2,Y0+52,str(i),FA,mono=True) for i in range(8)))
f.static(T(X0,Y0-14,'8 slots',MU,'start'))
t=.6
for n,(k,s8,_) in enumerate(KEYS):
    f.show(slot(X0+s8*W,Y0,W,"'%s'"%k,PT),t)
    f.show(badge(X0,Y0+72,'%d/8 used'%(n+1),PT),t+.1,hide=t+1.6)
    t+=1.6
f.show(badge(X0,Y0+72,'6/8 > 2/3 → grow',RS,190),t+.1)
f.path(code.bar(),[(0,0,0)]+[(.6+i*1.6,0,i*LH) for i in range(6)],.5)
figs['a']=f.render()
# 4.2 resize & rehash
f=Anim('dh-s42-',800,250,'A sixteen-slot table appears under the old eight-slot one. Each key is rehashed: hash modulo 16 gives a different slot than hash modulo 8, so every key moves to a new place. The old table is then dropped.','RESIZE · 8 → 16 SLOTS, EVERY KEY REHASHED',1.6)
X8,Y8,W8=70,50,52; X16,Y16,W16=70,160,44
f.static(T(X8-10,Y8+22,'8',MU,'end',mono=True)+T(X16-10,Y16+22,'16',MU,'end',mono=True))
f.show(''.join(slot(X8+i*W8,Y8,W8) for i in range(8)),0,hide=7.0)
f.show(''.join(slot(X16+i*W16,Y16,W16) for i in range(16)),.4)
f.show(''.join(T(X16+i*W16+W16/2,Y16+52,str(i),FA,mono=True) for i in range(16)),.4)
t=1.2
for k,s8,s16 in KEYS:
    ox,nx=X8+s8*W8,X16+s16*W16
    f.show(slot(ox,Y8,W8,"'%s'"%k,MID),0,hide=t+.1)
    f.path(slot(ox,Y8,W8,"'%s'"%k,MID),[(0,0,0),(t,nx-ox,Y16-Y8)],0,hide=t+.9)
    f.show(slot(nx,Y16,W16,"'%s'"%k,PT),t+.7)
    t+=1.1
f.show(T(X16,Y16+80,'hash % 16 ≠ hash % 8 → every key gets a new slot',TG,'start',bold=True),t)
f.show(T(X8,Y8+22,'old table dropped',FA,'start'),7.3)
figs['b']=f.render()
json.dump(figs,open('/tmp/dh/figs.json','w'))
