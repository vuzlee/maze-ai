"""Section 03 (Inheritance & MRO) figures for content/02-python/06-oop/oop-python."""
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
def box(x,y,label,c=PT,w=70,h=36,fill='var(--bg)'):
    return R(x,y,w,h,fill,c,8,1.6)+T(x+w/2,y+23,label,c,mono=True,bold=True)
def lit(x,y,label,c,w=70,h=36,al='.14'):
    return R(x,y,w,h,'var(--bg)','none',8)+R(x,y,w,h,'rgba(var(--%s),%s)'%({MID:'violet-a',TG:'green-a',RS:'red-a'}.get(c,'blue-a'),al),c,8,2)+T(x+w/2,y+23,label,c,mono=True,bold=True)
# diamond geometry (right side)
P={'D':(470,50),'B':(380,120),'C':(560,120),'A':(470,190)}
def ctr(k,top): x,y=P[k]; return (x+35,y+(0 if top else 36))
def edge(a,b,c=RULE_HI,sw=1.4): return arrow(*ctr(a,False),*ctr(b,True),c,sw)
figs={}
# --- 3.1 the diamond
code=Code2(0,40,['class A: ...','class B(A): ...','class C(A): ...','class D(B, C): ...'],220)
f=Anim('oop-s31-',700,290,'Four class lines run one by one. A sits at the bottom; B and C both inherit A; D inherits B and C. That gives two paths from D up to A, through B and through C: the diamond. The open question is whether A runs once or twice.','DIAMOND · TWO PATHS FROM D TO A',2.5)
f.static(code.svg())
f.show(box(*P['A'],'A'),.6)
f.show(box(*P['B'],'B')+edge('B','A'),2.4)
f.show(box(*P['C'],'C')+edge('C','A'),4.2)
f.show(box(*P['D'],'D')+edge('D','B')+edge('D','C'),6.0)
f.show(edge('D','B',MID,2.2)+edge('B','A',MID,2.2)+T(408,186,'path 1',MID,'end',bold=True),7.8)
f.show(edge('D','C',MID,2.2)+edge('C','A',MID,2.2)+T(602,186,'path 2',MID,'start',bold=True),8.8)
f.show(T(505,258,'does A run once or twice?',MU,'middle',bold=True),9.8)
f.path(code.bar(),[(0,0,0),(2.4,0,LH),(4.2,0,2*LH),(6.0,0,3*LH)],.5)
figs['31']=f.render()
# --- 3.2 C3 order
f=Anim('oop-s32-',700,230,'C3 linearization turns the diamond into one line. D comes first because a subclass comes before its parents. Then B before C, keeping the base order D(B, C). A comes only after both B and C, and every class appears exactly once. Result: D, B, C, A, object.','C3 LINEARIZATION · ONE LINE, EACH CLASS ONCE',2.5)
SX,SY,SW=40,60,110
for i in range(5): f.static(R(SX+i*(SW+16),SY,SW,36,'none',RULE_HI,8,1.3,'4 3'))
names=['D','B','C','A','object']
rules=['rule 1 · a subclass comes BEFORE its parents','rule 2 · base order kept: D(B, C) → B before C','rule 2 · then C','rule 1 · A only after both B and C','object always last']
for i,n in enumerate(names):
    t=.8+i*1.8
    f.show(lit(SX+i*(SW+16),SY,n,PT,SW),t)
    f.show(T(SX,SY+74,rules[i],MID,'start',bold=True),t,hide=(t+1.8 if i<4 else None))
f.show(T(SX,SY+74,'every class appears EXACTLY ONCE → A runs once',TG,'start',bold=True),.8+5*1.8)
for i in range(4): f.show(arrow(SX+i*(SW+16)+SW+2,SY+18,SX+(i+1)*(SW+16)-2,SY+18,MU,1.3,None,6),.8+(i+1)*1.8)
f.show(T(SX,SY+120,'D.__mro__ = (D, B, C, A, object)',TG,'start',mono=True,bold=True),.8+5*1.8+.3)
figs['32']=f.render()
# --- 3.3 super() follows MRO
code=Code2(0,40,['D().go()','  D.go → super().go()','  B.go → super().go()','  C.go → super().go()','  A.go'],250)
f=Anim('oop-s33-',700,240,'Calling D().go() walks the MRO. D.go calls super(), which moves to B. B.go calls super(), and that goes to C, not to A, because C is next in the MRO. C.go calls super() and reaches A, which runs once.','super() = THE NEXT CLASS IN THE MRO, NOT "THE PARENT"',2.5)
f.static(code.svg())
MX,MY,MW=272,60,76
for i,n in enumerate(['D','B','C','A','object']): f.static(box(MX+i*(MW+6),MY,n,PT,MW))
f.static(T(MX,MY-12,'D.__mro__',MU,'start',mono=True))
for i in range(4):
    t=.6+i*2.2
    f.show(lit(MX+i*(MW+6),MY,['D','B','C','A'][i],MID if i<3 else TG,MW),t)
f.show(arrow(MX+MW+MW/2+6,MY+64,MX+2*(MW+6)+MW/2,MY+64,MID,2)+L(MX+MW+MW/2+6,MY+40,MX+MW+MW/2+6,MY+64,MID,2)+L(MX+2*(MW+6)+MW/2,MY+64,MX+2*(MW+6)+MW/2,MY+40,MID,2)+T(MX+MW+6,MY+92,'B\'s super() → C, not A',MID,'start',bold=True),2.8+.4)
f.show(T(MX,MY+150,'D → B → C → A: A runs only ONCE',TG,'start',bold=True),.6+3*2.2+.4)
f.path(code.bar(),[(0,0,0),(.6,0,LH),(2.8,0,2*LH),(5.0,0,3*LH),(7.2,0,4*LH)],.3)
figs['33']=f.render()
json.dump(figs,open('/tmp/oop/figs.json','w'))
