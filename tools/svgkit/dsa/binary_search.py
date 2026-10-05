import sys,os,json,math; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from engine import *
PT,MID,TG='var(--brand)','var(--violet)','var(--filled)'
def vt(a): return 'rgba(var(--violet-a),%s)'%a
def it(a): return 'rgba(var(--blue-a),%s)'%a
LH=20
class Code2:
    def __init__(s,x,y,lines,w): s.x,s.y,s.lines,s.w=x,y,lines,w
    def svg(s):
        o=R(s.x,s.y,s.w,len(s.lines)*LH+14,'var(--bg)',RULE_HI,8)
        for i,l in enumerate(s.lines):
            n=len(l)-len(l.lstrip())
            o+=T(s.x+14,s.y+22+i*LH,' '*n+l.lstrip().replace('<','&lt;').replace('>','&gt;'),TX,'start',mono=True)
        return o
    def bar(s): return R(s.x+4,s.y+8,s.w-8,LH,vt('.13'),'none',4)+R(s.x+4,s.y+8,3,LH,MID,'none',1.5)
    def h(s): return len(s.lines)*LH+14

def search(pre,caption,aria,vals,goal,check,lines,answer,mode='find',dt=4.2,W=None):
    LI=dict(w=1,m=2,c=3,r=4,l=5) if mode=='find' else dict(w=2,m=3,c=4,r=5,l=4,e=6)
    n=len(vals); CW,G=42,6
    cw=max(300,28+max(len(l) for l in lines)*6.7); code=Code2(0,40,lines,cw); X0=cw+26
    W=W or max(760,X0+n*(CW+G)+10)
    cxl=lambda i:X0+i*(CW+G); cx=lambda i:cxl(i)+CW/2
    CY=96
    f=Anim(pre,W,0,aria,caption,3.2); f.static(code.svg())
    for i,v in enumerate(vals):
        f.show(R(cxl(i),CY,CW,36,'var(--bg)',RULE_HI,6,1.2)+T(cx(i),CY+23,str(v),TX,mono=True,bold=True)+T(cx(i),CY+52,str(i),FA,cls='sv-s',mono=True),.2+i*.05)
    # goal: chip born on the answer cell, then floats up to the corner; dashed outline stays
    gx=cx(answer)
    chip=R(gx-60,CY-36,120,24,it('.12'),TG,12,1.3)+T(gx,CY-19,goal,TG,mono=True,bold=True)
    if mode=='find':
        f.show(R(cxl(answer)-4,CY-4,CW+8,44,'none',TG,8,1.4,'4 3'),1.0)
        f.path(chip,[(0,0,0),(2.2,X0+60-gx,26-(CY-36))],1.0)
    else:
        f.show(R(X0,26,24+len(goal)*7,24,it('.12'),TG,12,1.3)+T(X0+12,42,goal,TG,'start',mono=True,bold=True),1.0)
    sb=code.bar(); bar_pts=[(0,0,0)]
    def line(t,i): bar_pts.append((t,0,i*LH))
    SY=CY+128
    t=3.0; f.show(T(X0,SY,'l = 0 · r = %d'%(n-1),PT,'start',mono=True),t,hide=t+1.1)
    lo,hi=0,n-1; t+=1.2; lo_p=[(0,0,0)]; hi_p=[(0,0,0)]; mid_p=[]; m0=None; steps=0; best=None; best_p=[]
    PY=CY+62
    while lo<=hi:
        steps+=1; m=(lo+hi)//2; m0=m if m0 is None else m0
        line(t,LI['w']); line(t+.6,LI['m'])
        mid_p.append((t+.6,(m-m0)*(CW+G),0))
        f.show(T(X0,SY,'mid = (%d + %d) // 2 = %d'%(lo,hi,m),MID,'start',mono=True),t+.6,hide=t+dt-.3)
        r,txt=check(m)
        line(t+1.4,LI['c'])
        f.show(R(cxl(m)-3,CY-3,CW+6,42,vt('.10'),MID,8,2.2),t+1.4,hide=t+dt-.3)
        f.show(T(X0,SY+22,txt,TX,'start',mono=True),t+1.4,hide=t+dt-.3)
        if r=='eq': steps_t=t+2.2; break
        right=(r=='right') or (r is False)
        if mode=='first' and r is True:
            if best is None: best=(m,t+2.4); best_p=[(t+2.4,0,0)]
            else: best_p.append((t+2.4,(m-best[0])*(CW+G),0))
        line(t+2.2,LI['r'] if right else LI['l'])
        drop=range(lo,m+1) if right else range(m,hi+1)
        for i in drop: f.show(R(cxl(i),CY,CW,36,'var(--sunk)','var(--rule)',6,1)+T(cx(i),CY+23,str(vals[i]),'var(--ghost)',mono=True)+T(cx(i),CY+52,str(i),FA,cls='sv-s',mono=True),t+2.6)
        if right: lo=m+1; lo_p.append((t+2.8,lo*(CW+G),0))
        else: hi=m-1; hi_p.append((t+2.8,(hi-(n-1))*(CW+G),0))
        f.show(T(X0,SY+44,('l = %d'%lo) if right else ('r = %d'%hi),PT,'start',mono=True,bold=True),t+2.8,hide=t+dt-.3)
        t+=dt
    else:
        steps_t=t; line(t,LI['w'])
    end=steps_t if mode=='find' else t
    if mode=='first': line(end+.3,LI['e'])
    f.path(sb,bar_pts,.0,appear=False,d=.35)
    lab=lambda i,s,ln: arrow(cx(i),PY+ln,cx(i),PY,PT,1.6,None,6)+T(cx(i),PY+ln+13,s,PT,mono=True,bold=True)
    f.path(lab(0,'l',14),lo_p,3.0,hide=end)
    f.path(lab(n-1,'r',30),hi_p,3.0,hide=end)
    f.path(T(cx(m0),CY-14,'mid',MID,mono=True,bold=True),mid_p,mid_p[0][0],hide=end+.2 if mode=='find' else end)
    if best: f.path(R(cxl(best[0])-6,CY-6,CW+12,48,'none',TG,9,1.6),best_p,best[1],hide=end)
    # found effect
    a=answer
    f.show(R(cxl(a),CY,CW,36,TG,TG,6,1.2)+T(cx(a),CY+23,str(vals[a]),'var(--on-fill)',mono=True,bold=True),end+.2)
    f.show(T(cx(a),PY+26,'✓ found',TG,mono=True,bold=True),end+.4)
    f.show(T(X0,SY,'%s · %d steps for %d cells'%({'find':'found at index %d'%a}.get(mode,'answer = index %d'%a),steps,n),TG,'start',bold=True),end+.5)
    f.h=max(code.y+code.h(),SY+56)+8
    return f.render()

figs={}
a=[3,8,12,16,23,31,40,47,52,60,71]
def cf(i):
    v=a[i]
    if v==23: return 'eq','a[%d] = 23 == 23'%i
    return ('right','a[%d] = %d < 23 → go right'%(i,v)) if v<23 else ('left','a[%d] = %d > 23 → go left'%(i,v))
L1=['l, r = 0, len(a) - 1','while l <= r:','    mid = (l + r) // 2','    if a[mid] == t: return mid','    if a[mid] < t: l = mid + 1','    else:          r = mid - 1']
figs['m1']=search('m1-','FIND 23 IN A SORTED LIST','Sorted list of 11 numbers; the target 23 is marked at index 4. l starts at 0, r at 10. mid 5 holds 31, too big: right half greys out and r moves to 4. mid 2 holds 12, too small: l moves to 3. mid 3 holds 16: l moves to 4. mid 4 holds 23: found in 4 steps. The highlighted code line follows each step.',a,'target = 23',cf,L1,4)

# 1.2 sorted vs unsorted
f=Anim('m2-',760,190,'Sorted list: asking a[i] >= 23 gives no no no no yes yes yes yes, one switch. Unsorted list: the answers flip back and forth, so dropping half is unsafe.','WHY SORTED? · ASK "a[i] ≥ 23" OF EVERY CELL',2.5)
s=[3,8,12,16,23,31,40,47]; u=[31,8,47,16,3,23,12,40]
for row,(arr,lab,y) in enumerate([(s,'sorted',40),(u,'unsorted',112)]):
    f.static(T(0,y+22,lab,MU,'start'))
    b=.3+row*3.2
    for i,v in enumerate(arr):
        x=90+i*56
        f.show(R(x,y,48,32,'var(--bg)',RULE_HI,6,1.2)+T(x+24,y+21,str(v),TX,mono=True,bold=True),b+i*.04)
        ok=v>=23
        f.show(R(x+9,y+38,30,18,TG if ok else 'var(--sunk)',TG if ok else RULE_HI,9,1)+T(x+24,y+51,'yes' if ok else 'no','var(--on-fill)' if ok else FA,cls='sv-s'),b+.6+i*.18)
    if row==0:
        f.show(L(90+4*56-4,y-6,90+4*56-4,y+60,MID,2.4),b+2.2)
        f.show(T(90+8*56+6,y+22,'✓ one switch — drop half safely',TG,'start',bold=True),b+2.4)
    else:
        for i in (1,4,6): f.show(L(90+i*56-4,y-6,90+i*56-4,y+60,MID,1.4,'3 3'),b+2.2)
        f.show(T(90+8*56+6,y+22,'✗ many switches — unsafe',MU,'start',bold=True),b+2.4)
figs['m2']=f.render()

# 1.3 halving -> log graph
f=Anim('m3-',760,380,'Sixteen cells grey out half at a time: 16, 8, 4, 2, 1, four steps. Then a graph: steps against n. Linear search climbs a straight line; binary search follows log2 n, almost flat: 20 steps at a million.','O(log n) · HALVE UNTIL ONE CELL IS LEFT',3)
N=16;w=40;g=4;X=0
for i in range(N): f.show(R(X+i*(w+g),36,w,28,'var(--bg)',RULE_HI,5,1.2),.2+i*.03)
left=list(range(N)); t=1.4; cnt=[16]; ln=None
while len(left)>1:
    k=len(left)//2; drop=left[k:] if len(cnt)%2 else left[:k]
    left=[i for i in left if i not in drop]
    for i in drop: f.show(R(X+i*(w+g),36,w,28,'var(--sunk)','var(--rule)',5,1),t)
    cnt.append(len(left))
    f.show(T(X,88,'  →  '.join(map(str,cnt)),PT,'start',mono=True,bold=True),t,hide=t+1.2 if len(left)>1 else None); t+=1.2
f.show(R(X+left[0]*(w+g),36,w,28,TG,TG,5,1.2),t-1.1)
f.show(T(X+340,88,'4 halvings = log₂ 16',TG,'start',bold=True),t-.8)
# graph
gx,gy,gw,gh=60,120,560,210   # origin bottom-left at (gx, gy+gh)
NMAX,SMAX=64,8
px=lambda n:gx+n/NMAX*gw; py=lambda s:gy+gh-s/SMAX*gh
t+=.4
ax=L(gx,gy+gh,gx+gw+10,gy+gh,MU,1.2)+L(gx,gy+gh,gx,gy-6,MU,1.2)
for n_ in (16,32,48,64): ax+=T(px(n_),gy+gh+16,str(n_),FA,cls='sv-s',mono=True)+L(px(n_),gy+gh,px(n_),gy+gh+4,MU,1)
for s_ in (2,4,6,8): ax+=T(gx-8,py(s_)+4,str(s_),FA,'end',cls='sv-s',mono=True)+L(gx,py(s_),gx+gw,py(s_),'var(--rule)',1,'2 4')
ax+=T(gx+gw+14,gy+gh+4,'n',MU,'start',mono=True)+T(gx-8,gy-12,'steps',MU,'start',mono=True)
f.show(ax,t)
lin='M%.1f %.1f L%.1f %.1f'%(px(0),py(0),px(SMAX),py(SMAX))
f.show('<path d="%s" fill="none" stroke="var(--ghost)" stroke-width="2"/>'%lin+T(px(SMAX)+8,py(SMAX)+12,'O(n) linear scan',MU,'start'),t+.8)
pts=[(n_,math.log2(n_)) for n_ in [1+i*0.5 for i in range(127)]]
d='M'+' L'.join('%.1f %.1f'%(px(a_),py(b_)) for a_,b_ in pts)
f.show('<path d="%s" fill="none" stroke="%s" stroke-width="2.6"/>'%(d,TG)+T(px(64)-4,py(6)-10,'log₂ n',TG,'end',bold=True),t+1.8,d=.8)
for k,n_ in enumerate((2,4,8,16,32,64)):
    f.show('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>'%(px(n_),py(math.log2(n_)),MID),t+2.4+k*.25)
f.show(T(px(16)+8,py(4)+16,'16 → 4',MID,'start',mono=True,bold=True)+T(px(64)-4,py(6)+20,'64 → 6',MID,'end',mono=True,bold=True),t+4)
f.show(T(gx+gw,gy+gh+38,'double n → only one more step · n = 10⁶ → 20 steps',TG,'end',bold=True),t+4.4)
figs['m3']=f.render()

FIRST=['l, r = 0, len(a) - 1','ans = -1','while l <= r:','    mid = (l + r) // 2','    if ok(mid): ans, r = mid, mid - 1','    else:       l = mid + 1','return ans']
# reorder line indices for 'first' mode: while=2, mid=3, check=4/5... adapt by mapping
def first(pre,cap,aria,vals,goal,okf,okname,answer):
    lines=[l.replace('ok(mid)',okname) for l in FIRST]
    def ck(i): r,txt=okf(i); return r,txt
    return search(pre,cap,aria,vals,goal,ck,lines,answer,'first')
b=[1,3,3,3,5,8,9]
def lb(i): v=b[i]; return (v>=3,'a[%d] = %d ≥ 3 ✓ → record, go left'%(i,v) if v>=3 else 'a[%d] = %d < 3 → go right'%(i,v))
piles=[3,6,7,11]; sp=list(range(1,12))
def hrs(s): return sum(math.ceil(p/s) for p in piles)
def ks(i): s=sp[i];h=hrs(s); return (h<=8,'speed %d → %d h ≤ 8 ✓ → record, go slower'%(s,h) if h<=8 else 'speed %d → %d h > 8 → go faster'%(s,h))
r=[4,5,6,7,0,1,2]
def rm(i): v=r[i]; return (v<=2,'a[%d] = %d ≤ 2 ✓ → record, go left'%(i,v) if v<=2 else 'a[%d] = %d > 2 → go right'%(i,v))
p=[1,3,2,4,6,5,2]
def pk(i):
    if i==len(p)-1: return True,'last cell ✓'
    return (p[i]>p[i+1],'%d > %d downhill ✓ → record, go left'%(p[i],p[i+1]) if p[i]>p[i+1] else '%d < %d uphill → go right'%(p[i],p[i+1]))
figs['q1']=(b,'first a[i] ≥ 3',lb,'a[mid] >= 3',1,'q1-','LOWER BOUND · FIRST INDEX WITH a[i] ≥ 3','Sorted list 1 3 3 3 5 8 9; the answer, the first 3 at index 1, is marked. Every a[mid] >= 3 is recorded and the search goes left; it ends at index 1.')
figs['q2']=(sp,'min speed',ks,'fits(mid)',3,'q2-','SEARCH THE ANSWER · CELLS = POSSIBLE SPEEDS · piles [3,6,7,11] in 8 h','Koko: cells are speeds 1 to 11. Each mid speed is tested; fast enough is recorded and the search goes slower. Minimum speed 4.')
figs['q3']=(r,'minimum',rm,'a[mid] <= a[-1]',4,'q3-','ROTATED LIST · FIND THE MINIMUM · compare with the last value','Rotated list 4 5 6 7 0 1 2. a[mid] <= 2 means mid is in the right run: record and go left. Ends at index 4, value 0.')
figs['q4']=(p,'a peak',pk,'a[mid] > a[mid+1]',4,'q4-','PEAK · GOING DOWNHILL MEANS A PEAK IS HERE OR LEFT','Unsorted list 1 3 2 4 6 5 2. Downhill at mid: record and go left; uphill: go right. Ends at index 4, value 6.')
for k in ('q1','q2','q3','q4'):
    vals,goal,okf,okn,ans,pre,cap,aria=figs[k]
    figs[k]=first(pre,cap,aria,vals,goal,okf,okn,ans)
json.dump(figs,open('/tmp/binary-search-figs.json','w'))
