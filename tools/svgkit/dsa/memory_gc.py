"""Mental-model figures for content/02-python/02-language-core/memory-management-gc."""
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
def obj(x,y,label,w=110,h=44,c=PT,fill='var(--bg)'):
    return R(x,y,w,h,fill,c,8,1.6)+T(x+w/2,y+27,label,c,mono=True,bold=True)
def count(x,y,n,c=MID):   # refcount badge, opaque so a newer value hides the older
    return R(x-26,y-12,52,24,'var(--bg)','none',12)+R(x-26,y-12,52,24,'rgba(var(--violet-a),.10)',c,12,1.3)+T(x,y+4,'refs %d'%n,c,mono=True,bold=True)
def tagname(x,y,n): return R(x-18,y-12,36,24,'var(--bg)',PT,6,1.4)+T(x,y+5,n,PT,mono=True,bold=True)

figs={}
# 1.1 reference counting
code=Code2(0,40,['a = [1, 2]','b = a','del a','del b'],200)
f=Anim('gc-m1-',700,240,'Code on the left runs line by line. a = [1, 2] creates a list with one name, refs 1. b = a adds a second name, refs 2. del a removes one arrow, refs 1. del b removes the last, refs 0, and the list is freed on that line.','REFERENCE COUNTING · FREED THE MOMENT THE COUNT HITS 0',2.5)
f.static(code.svg())
OX,OY=420,150; ocx=OX+55
f.show(obj(OX,OY,'[1, 2]'),.6)
# names a (left) and b (right) above the object
ax,bx,ny=OX-40,OX+150,70
a_name=tagname(ax,ny,'a')+arrow(ax+10,ny+12,ocx-14,OY-2,PT,1.5)
b_name=tagname(bx,ny,'b')+arrow(bx-10,ny+12,ocx+14,OY-2,PT,1.5)
f.show(a_name,.8,hide=5.6)
f.show(count(ocx,OY+70,1),.9,hide=3.0)
f.show(b_name,3.0,hide=8.2)
f.show(count(ocx,OY+70,2),3.1,hide=5.6)
f.show(count(ocx,OY+70,1),5.7,hide=8.2)
f.show(count(ocx,OY+70,0,RS),8.3)
f.show(obj(OX,OY,'[1, 2]',c='var(--ghost)',fill='var(--sunk)')+T(OX+120,OY+27,'freed now',RS,'start',bold=True),8.5)
f.show(T(240,OY+76,'count = number of arrows in',MU,'start'),1.4,hide=8.2)
f.path(code.bar(),[(0,0,0),(3.0,0,LH),(5.6,0,2*LH),(8.2,0,3*LH)],.5)
figs['m1']=f.render()

# 1.2 cycle + gc
code=Code2(0,40,['x = Node()','y = Node()','x.next = y; y.next = x','del x, y','gc.collect()'],236)
f=Anim('gc-m2-',720,300,'Two nodes point at each other. After del x, y no name points in, but each node is still pointed to by the other, so both counts stay at 1 and counting alone never frees them. gc.collect() finds the unreachable cycle, cuts it, both counts drop to 0 and both are freed.','A CYCLE · COUNTING ALONE NEVER REACHES 0',2.5)
f.static(code.svg())
X1,X2,Y=300,520,150; w=100
f.show(obj(X1,Y,'Node X',w),.6); f.show(obj(X2,Y,'Node Y',w),2.6)
f.show(tagname(X1+50,80,'x')+arrow(X1+50,92,X1+50,Y-2,PT,1.5),.8,hide=7.4)
f.show(tagname(X2+50,80,'y')+arrow(X2+50,92,X2+50,Y-2,PT,1.5),2.8,hide=7.4)
link='<path d="M%d %d Q%d %d %d %d" fill="none" stroke="%s" stroke-width="1.6"/>'
L1=link%(X1+w,Y+14,(X1+w+X2)/2,Y-8,X2-4,Y+14,PT)+arrow(X2-12,Y+12,X2-2,Y+14,PT,1.6,None,6)
L2=link%(X2,Y+32,(X1+w+X2)/2,Y+54,X1+w+4,Y+32,PT)+arrow(X1+w+12,Y+34,X1+w+2,Y+32,PT,1.6,None,6)
f.show(L1+L2,4.8,hide=11.8)
for (cx_,ln) in ((X1+50,0),(X2+50,0)): pass
# counts under each node
cy=Y+80
f.show(count(X1+50,cy,1),.9,hide=4.8); f.show(count(X2+50,cy,1),2.9,hide=4.8)
f.show(count(X1+50,cy,2),4.9,hide=7.4); f.show(count(X2+50,cy,2),4.9,hide=7.4)
f.show(count(X1+50,cy,1,RS),7.5,hide=11.8); f.show(count(X2+50,cy,1,RS),7.5,hide=11.8)
f.show(T(X1,cy+34,'no name points in — but still refs 1 each: stuck',RS,'start',bold=True),7.8,hide=10.2)
f.show(R(X1-14,Y-20,X2+w-X1+28,104,'rgba(var(--violet-a),.06)',MID,10,1.8,'5 4')+T(X1-14,Y-28,'gc.collect(): unreachable cycle',MID,'start',bold=True),10.2,hide=11.8)
f.show(count(X1+50,cy,0,RS),11.9); f.show(count(X2+50,cy,0,RS),11.9)
f.show(obj(X1,Y,'Node X',w,c='var(--ghost)',fill='var(--sunk)')+obj(X2,Y,'Node Y',w,c='var(--ghost)',fill='var(--sunk)'),12.0)
f.show(T(X1,cy+34,'cycle cut → both freed',TG,'start',bold=True),12.2)
f.path(code.bar(),[(0,0,0),(2.6,0,LH),(4.8,0,2*LH),(7.4,0,3*LH),(10.2,0,4*LH)],.5)
figs['m2']=f.render()
json.dump(figs,open('/tmp/gc/figs.json','w'))
