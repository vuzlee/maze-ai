import sys; import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from tablefig import T,R,L,arrow,pill,tint,cap,COL,AM,GR,RD,BL,MU,TX,FA,RULE_HI
class Anim:
    """Timeline figure. key(t, op, dx, dy) frames per item; static render = final frame."""
    def __init__(s,pre,w,h,aria,caption=None,hold=2.0):
        s.pre,s.w,s.h,s.aria,s.hold=pre,w,h,aria,hold; s.items=[]
        if caption: s.items.append((cap(0,14,caption),None))
    def static(s,svg): s.items.append((svg,None)); return s
    def show(s,svg,t,hide=None,d=.35):
        fr=[(0,0,0,0),(t,0,0,0),(t+d,1,0,0)]
        if hide is not None: fr+=[(hide,1,0,0),(hide+d,0,0,0)]
        s.items.append((svg,fr)); return s
    def path(s,svg,pts,t0=0,appear=True,d=.6,hide=None):
        """pts=[(t,dx,dy)] item visible from t0, glides between offsets."""
        fr=[(0,0 if appear else 1,pts[0][1],pts[0][2]),(t0,0 if appear else 1,pts[0][1],pts[0][2]),(t0+.3,1,pts[0][1],pts[0][2])]
        last=pts[0]
        for t,dx,dy in pts[1:]:
            fr+=[(t,1,last[1],last[2]),(t+d,1,dx,dy)]; last=(t,dx,dy)
        if hide is not None: fr+=[(hide,1,last[1],last[2]),(hide+.3,0,last[1],last[2])]
        s.items.append((svg,fr)); return s
    def render(s):
        TT=max([f[0] for _,fr in s.items if fr for f in fr]+[0])+s.hold
        kfs,css,body=[],[],[];k=0
        for svg,fr in s.items:
            if not fr: body.append(svg); continue
            k+=1; nm='%sa%d'%(s.pre,k); fr=sorted(fr,key=lambda f:f[0])
            if fr[-1][0]<TT: fr.append((TT,)+fr[-1][1:])
            seen={};
            for f in fr: seen[round(100*f[0]/TT,3)]=f
            kfs.append('@keyframes %s{%s}'%(nm,''.join('%.3f%%{animation-timing-function:ease-in-out;opacity:%.2f;transform:translate(%.1fpx,%.1fpx)}'%(p,f[1],f[2],f[3]) for p,f in sorted(seen.items()))))
            css.append('.%s{animation:%s %.2fs linear 1 forwards}'%(nm,nm,TT))
            e=fr[-1]; a=(' opacity="0"' if e[1]==0 else '')+(' transform="translate(%.1f,%.1f)"'%(e[2],e[3]) if (e[2] or e[3]) else '')
            body.append('<g class="%s"%s>%s</g>'%(nm,a,svg))
        st=''.join(kfs)+'@media (prefers-reduced-motion:no-preference){%s}'%''.join(css)
        ar=s.aria.replace('&','&amp;').replace('"','&quot;')
        return '<figure class="gist">\n<svg viewBox="0 0 %d %d" role="img" aria-label="%s" data-anim><style>%s</style>\n%s\n</svg>\n</figure>'%(s.w,s.h,ar,st,'\n'.join(body))

MONO=True
def cell(x,y,v,w=40,tone=None,h=34):
    return R(x,y,w,h,tint(tone) if tone else 'var(--bg)',COL[tone] if tone else RULE_HI,4,1.3 if tone else 1)+T(x+w/2,y+h/2+5,str(v),COL[tone] if tone else TX,mono=True)
def grey(x,y,w=40,v='',h=34):
    return R(x,y,w,h,'var(--sunk)',RULE_HI,4,1)+T(x+w/2,y+h/2+5,str(v),FA,mono=True)
def tag(x,y,t,c):   # pointer below a cell: arrow up + label
    return arrow(x,y+20,x,y+3,c,1.5,None,6)+T(x,y+34,t,c,mono=True,bold=True)
def tagup(x,y,t,c): # pointer above a cell
    return T(x,y-22,t,c,mono=True,bold=True)+arrow(x,y-17,x,y-3,c,1.5,None,6)
class Code:
    def __init__(s,x,y,lines,w):
        s.x,s.y,s.lines,s.w=x,y,lines,w
    def svg(s):
        o=R(s.x,s.y,s.w,len(s.lines)*19+12,'var(--bg)',RULE_HI,6)
        for i,l in enumerate(s.lines):
            n=len(l)-len(l.lstrip()); o+=T(s.x+12,s.y+21+i*19,' '*n+l.lstrip().replace('<','&lt;').replace('>','&gt;'),TX,'start',mono=True)
        return o
    def bar(s,i,tone='am'):
        y=s.y+7+i*19
        return R(s.x+3,y,s.w-6,19,tint(tone,'.20'),'none',2)+R(s.x+3,y,3,19,COL[tone],'none',1)
