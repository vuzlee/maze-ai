"""Split figures for content/02-python/08-performance/performance-profiling, section prof-s3."""
import sys,os,json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from engine import *
PT,MID,TG='var(--brand)','var(--violet)','var(--filled)'
LH=20
class Code2:
    def __init__(s,x,y,lines,w): s.x,s.y,s.lines,s.w=x,y,lines,w
    def svg(s):
        o=R(s.x,s.y,s.w,len(s.lines)*LH+14,'var(--bg)',RULE_HI,8)
        for i,l in enumerate(s.lines): o+=T(s.x+14,s.y+22+i*LH,l,TX,'start',mono=True)
        return o
    def bar(s): return R(s.x+4,s.y+8,s.w-8,LH,'rgba(var(--violet-a),.13)','none',4)+R(s.x+4,s.y+8,3,LH,MID,'none',1.5)
def box(x,y,v,c,fill='var(--bg)'): return R(x,y,44,34,fill,c,5,1.4)+T(x+22,y+22,str(v),c,mono=True,bold=True)
figs={}
code=Code2(0,40,['a = [1, 2, 3, 4, 5]','[x*2 for x in a]','b = np.array(a)','b * 2'],230)
f=Anim('pf-s31a-',760,250,'Code on the left runs line by line. The list comprehension visits 1, 2, 3, 4, 5 one at a time, a ring stepping across and writing 2, 4, 6, 8, 10 one result per step through the interpreter. Then b * 2 rings the whole NumPy array once and all five results appear together, computed in C.','ONE INTERPRETER STEP PER ITEM vs ONE CALL',2.5)
f.static(code.svg())
X0,Y0=290,60; dx=50
f.static(T(X0-12,Y0+22,'a',MU,'end',mono=True))
for i,v in enumerate([1,2,3,4,5]): f.static(box(X0+i*dx,Y0,v,PT))
Y1,Y2=Y0+66,Y0+136
f.static(T(X0-12,Y1+22,'loop',MU,'end',mono=True)+T(X0-12,Y2+22,'NumPy',MU,'end',mono=True))
for i in range(5): f.static(R(X0+i*dx,Y1,44,34,'var(--sunk)',RULE_HI,5,1)+R(X0+i*dx,Y2,44,34,'var(--sunk)',RULE_HI,5,1))
ring=R(X0-4,Y0-4,52,42,'none',MID,6,2.2)
t0=1.6
f.path(ring,[(t0,0,0)]+[(t0+1.1*i,i*dx,0) for i in range(1,5)],t0,hide=t0+5.2)
for i,v in enumerate([2,4,6,8,10]): f.show(box(X0+i*dx,Y1,v,PT),t0+.4+1.1*i)
f.show(T(X0+5*dx+10,Y1+22,'5 trips through the interpreter',MU,'start'),t0+4.8)
t1=8.4
f.show(R(X0-6,Y0-6,5*dx+2,46,'none',MID,7,2.2),t1,hide=t1+1.6)
for i,v in enumerate([2,4,6,8,10]): f.show(box(X0+i*dx,Y2,v,TG),t1+.6)
f.show(T(X0+5*dx+10,Y2+22,'one call, the loop runs in C',TG,'start',bold=True),t1+.9)
f.path(code.bar(),[(0,0,0),(t0,0,LH),(7.2,0,2*LH),(t1,0,3*LH)],.5)
figs['a']=f.render()
# measured cost
f=Anim('pf-s31b-',700,170,'Doubling 1 million numbers: the list comprehension takes 30.33 ms, NumPy takes 0.66 ms, 46 times faster, and the array uses 8 MB versus about 36 MB for the list.','DOUBLING 1 MILLION NUMBERS',1.5)
BX,W=170,420; s=W/30.33
f.show(R(BX,40,W,24,'rgba(var(--clay-a),.18)',PT,3,1.3)+T(0,57,'list comprehension',PT,'start')+T(BX+W+10,57,'30.33 ms',PT,'start',mono=True,bold=True),.4)
f.show(R(BX,80,max(0.66*s,3),24,'rgba(var(--blue-a),.25)',TG,3,1.3)+T(0,97,'NumPy',TG,'start')+T(BX+0.66*s+12,97,'0.66 ms',TG,'start',mono=True,bold=True),1.4)
f.show(R(0,124,3,20,MID,'none',1.5)+T(14,139,'46× faster · and lighter: 8 MB vs ~36 MB',MID,'start',bold=True),2.4)
figs['b']=f.render()
json.dump(figs,open('/tmp/pf/figs.json','w'))
