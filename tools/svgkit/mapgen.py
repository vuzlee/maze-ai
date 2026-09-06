# -*- coding: utf-8 -*-
"""Ban do N o + panel phai, dung chung cho cac bai nhom D."""
CL={'p':('var(--probe)','amber-a'),'b':('var(--filled)','blue-a'),
    'g':('var(--ok)','green-a'),'r':('var(--tomb)','red-a'),'n':('var(--muted)','blue-a')}
def build(boxes,hi,head,rows,label,W=340):
    """boxes: [(title,[dong,...],mau)] ; hi: 1-based, 0 = khong to (muc 01)"""
    o=[];y=26
    ys=[]
    for i,(t,ds,c) in enumerate(boxes,1):
        h=26+15*len(ds)
        ys.append((y,h))
        cc,aa=CL[c]
        if i==hi:
            o.append(f'<rect x="0" y="{y}" width="{W}" height="{h}" rx="6" fill="rgba(var(--{aa}),.10)" stroke="{cc}" stroke-width="1.6"/>')
            o.append(f'<text class="sv-t" x="13" y="{y+20}" fill="{cc}">{t}</text>'); dc='var(--muted)'
        else:
            o.append(f'<rect x="0" y="{y}" width="{W}" height="{h}" rx="6" fill="none" stroke="var(--rule)" stroke-width="1"/>')
            o.append(f'<text class="sv-t" x="13" y="{y+20}" fill="var(--dim)">{t}</text>'); dc='var(--dim)'
        for j,d in enumerate(ds):
            o.append(f'<text class="sv-d" x="13" y="{y+38+j*15}" fill="{dc}">{d}</text>')
        y+=h
        if i<len(boxes):
            o.append(f'<line x1="{W/2}" y1="{y}" x2="{W/2}" y2="{y+10}" stroke="var(--rule-hi)" stroke-width="1.2"/>'
                     f'<polygon points="{W/2},{y+18} {W/2-4.2},{y+10} {W/2+4.2},{y+10}" fill="var(--rule-hi)"/>')
            y+=22
    colh=y
    if hi:
        by,bh=ys[hi-1]; cc,_=CL[boxes[hi-1][2]]
        o.append(f'<line x1="{W}" y1="{by+bh/2}" x2="{W+32}" y2="{by+bh/2}" stroke="{cc}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    px=W+32; pw=860-px
    o.append(f'<text class="sv-hv" x="{px}" y="18">{head}</text>')
    py=28
    for t,sub,c in rows:
        cc,aa=CL[c]; h=54 if sub else 34
        o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{h}" rx="5" fill="rgba(var(--{aa}),.10)" stroke="{cc}" stroke-width="1"/>')
        o.append(f'<text class="sv-t" x="{px+16}" y="{py+22}" fill="{cc}">{t}</text>')
        if sub: o.append(f'<text class="sv-s" x="{px+16}" y="{py+40}" fill="var(--dim)">{sub}</text>')
        py+=h+8
    H=max(colh,py)+4
    return f'<svg viewBox="0 0 860 {H}" role="img" aria-label="{label}">\n'+'\n'.join(o)+'\n</svg>'
