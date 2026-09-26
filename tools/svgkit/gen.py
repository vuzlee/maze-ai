# -*- coding: utf-8 -*-
"""Bốn hình cho bài Logistic regression.

Số lấy từ .claude/memory/nhat-ky/so-classical-ml.md — bộ A–F, hai cột
"đã mua trước" + tuổi. Hệ số ĐÃ LÀM TRÒN tái tạo đúng mọi p, nên dùng thẳng.
"""
import math, sys
sys.path.insert(0,'/home/vuzle/Documents/mazeai/tools')
from svgkit.base import esc

ID=['A','B','C','D','E','F']; AGE=[24,28,35,41,52,60]
PREV=[0,0,1,1,1,0]; LAB=[0,0,1,1,0,1]
WP,WA,B0 = 1.22, 0.067, -3.34
def sig(z): return 1/(1+math.exp(-z))
Z=[WP*PREV[i]+WA*AGE[i]+B0 for i in range(6)]
P=[sig(z) for z in Z]
NLL=[-math.log(P[i] if LAB[i] else 1-P[i]) for i in range(6)]
LOSS=sum(NLL)/6
# khớp bảng trong memory
for i,(zz,pp) in enumerate(((-1.73,0.15),(-1.46,0.19),(0.22,0.56),(0.63,0.65),(1.36,0.80),(0.68,0.66))):
    assert abs(Z[i]-zz)<0.006 and abs(P[i]-pp)<0.006, (ID[i],Z[i],P[i])
assert abs(LOSS-0.56)<0.01, LOSS
assert max(range(6),key=lambda i:NLL[i])==4, 'E phải là dòng phạt nặng nhất'
OR_P, OR_A = math.exp(WP), math.exp(10*WA)
assert abs(OR_P-3.38)<0.01 and abs(OR_A-1.95)<0.01

def thresh(t):
    tp=sum(1 for i in range(6) if P[i]>=t and LAB[i])
    fp=sum(1 for i in range(6) if P[i]>=t and not LAB[i])
    fn=sum(1 for i in range(6) if P[i]<t and LAB[i])
    pr=tp/(tp+fp) if tp+fp else 0.0
    rc=tp/(tp+fn) if tp+fn else 0.0
    return tp,fp,fn,pr,rc
TT=[0.5,0.6,0.8]
R=[thresh(t) for t in TT]
assert abs(R[0][3]-0.75)<0.01 and abs(R[0][4]-1.0)<0.01, R[0]
assert abs(R[1][3]-0.67)<0.01 and abs(R[1][4]-0.67)<0.01, R[1]
assert R[2][4]==0.0, R[2]

def n2(v,d=2): return ('%.*f'%(d,v)).replace('.',',')
def sgn(v,d=2): return ('%+.*f'%(d,v)).replace('.',',')
def kf(n,cyc,ramp=6.0,start=2.0):
    ks,cs=[],[]; span=(100.0-start-ramp)/max(n-1,1)
    for i in range(n):
        a=start+i*span; b=a+ramp
        ks.append('@keyframes k%d{0%%{animation-timing-function:ease-in-out;opacity:0}'
                  '%.3f%%{animation-timing-function:ease-in-out;opacity:0}'
                  '%.3f%%{animation-timing-function:ease-in-out;opacity:1}'
                  '100%%{animation-timing-function:ease-in-out;opacity:1}}'%(i+1,a,b))
        cs.append('.k%d{animation:k%d %.1fs linear 1 forwards}'%(i+1,i+1,cyc))
    return ks,cs
def style(parts):
    ks,cs=[],[]
    for k,c in parts: ks+=k; cs+=c
    return ('<style>'+''.join(ks)+'@media (prefers-reduced-motion:no-preference){'
            +''.join(cs)+'}.sy{transform-box:fill-box;transform-origin:50% 100%}'
            '.sy *{vector-effect:non-scaling-stroke}</style>')
def svg(w,h,aria,st,body):
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s" data-anim>%s\n%s\n</svg>'
            %(w,h,esc(aria),st,body))
BL,AM,GR,RD='var(--filled)','var(--probe)','var(--ok)','var(--tomb)'
MU,FA,RU='var(--muted)','var(--faint)','var(--rule-hi)'
def T(x,y,s,c='var(--text)',cls='sv-d',a=None):
    an=' text-anchor="%s"'%a if a else ''
    return '<text class="%s" x="%s" y="%s" fill="%s" style="fill:%s"%s>%s</text>'%(cls,x,y,c,c,an,esc(s))
def RC(x,y,w,h,st,rgb=None,al='.12',sw='1.3',rx=4,dash=None):
    f='rgba(var(--%s),%s)'%(rgb,al) if rgb else 'none'
    d=' stroke-dasharray="%s"'%dash if dash else ''
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"%s/>'%(x,y,w,h,rx,f,st,sw,d))
def LN(x1,y1,x2,y2,c=RU,sw='1.2',dash=None):
    d=' stroke-dasharray="%s"'%dash if dash else ''
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            %(x1,y1,x2,y2,c,sw,d))
OUT='/tmp/lg/'
print('loss=%.3f  OR=%.2f/%.2f  t0.5 pr/rc=%.2f/%.2f'%(LOSS,OR_P,OR_A,R[0][3],R[0][4]))

# ═══════════════ HÌNH 1 — bản đồ bài, 3 ô
e=[]; BW,BX=252,[0,292,584]
HEAD=[('02','Công thức tổng quát','x → z → p: đường thẳng cho','điểm số, sigmoid ép điểm số','về khoảng 0–1.'),
      ('03','Từ bảng tới xác suất','Sáu khách đi qua công thức,','mỗi người ra một p và một','mức phạt của log loss.'),
      ('05','Odds ratio và ngưỡng','Hệ số đọc bằng odds ratio.','Ngưỡng cắt là quyết định','nghiệp vụ, không phải model.')]
for i,(num,tt,a,b,c) in enumerate(HEAD):
    x=BX[i]; e.append('<g class="k%d">'%(i+1))
    if i: e.append(LN(x-32,104,x-12,104,RU)+'<polygon points="%d,104 %d,99.8 %d,108.2" fill="%s"/>'%(x-4,x-12,x-12,RU))
    e.append(T(x,22,tt,AM)); e.append(RC(x,30,BW,150,RU,rx=6,sw='1.4'))
    e.append(T(x+12,52,num,AM,'sv-l'))
    for j,ln in enumerate((a,b,c)): e.append(T(x+12,80+j*22,ln,MU))
    e.append('</g>')
open(OUT+'h1.svg','w',encoding='utf-8').write(svg(836,196,
 'Bản đồ bài: mục 02 công thức tổng quát, x ra z ra p, đường thẳng cho điểm số rồi sigmoid ép điểm số về '
 'khoảng 0 tới 1; mục 03 sáu khách đi qua công thức, mỗi người ra một xác suất p và một mức phạt của log '
 'loss; mục 05 hệ số đọc bằng odds ratio, còn ngưỡng cắt là quyết định nghiệp vụ chứ không phải của model.',
 style([kf(3,5.0,ramp=7.0)]),'\n'.join(e)))

# ═══════════════ HÌNH 2 — ba ô cùng trục z (gộp ba hình rời của bản cũ)
e=[]
PW,PH,PY0 = 248, 168, 40
XS=[PX for PX in (12,306,600)]
def zx(x0,zz): return x0+(zz+6)/12*PW
for k,(x0,title) in enumerate(zip(XS,('Điểm số z không bị chặn','Sigmoid ép z về (0, 1)','Log loss phạt khi sai mà chắc'))):
    e.append('<g class="k%d">'%(k+1))
    e.append(T(x0,26,title,AM))
    e.append(RC(x0,PY0,PW,PH,RU,rx=6,sw='1.2'))
    e.append('</g>')
# ô 1: đường thẳng z chạy ra ngoài dải 0-1
e.append('<g class="k1">')
x0=XS[0]; base=PY0+PH-30; top=PY0+24
e.append(LN(x0+8,base,x0+PW-8,base,FA,'1'))
e.append(LN(x0+8,top,x0+PW-8,top,FA,'1','4 4'))
e.append(T(x0+PW-12,base+18,'z',FA,'sv-d','end'))
e.append(T(x0+12,base+18,'0',FA)); e.append(T(x0+12,top-6,'1',FA))
e.append(LN(x0+14,base+34,x0+PW-14,top-16,BL,'1.8'))
e.append(T(x0+12,PY0+PH+30,'vượt cả 0 lẫn 1 — không đọc thành xác suất được',MU))
e.append('</g>')
# ô 2: sigmoid
e.append('<g class="k2">')
x0=XS[1]; b2=PY0+PH-24; t2=PY0+18
pts=[]
for n in range(61):
    zz=-6+12*n/60
    pts.append('%.1f,%.1f'%(zx(x0,zz), b2-(b2-t2)*sig(zz)))
e.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.8"/>'%(' '.join(pts),AM))
e.append(LN(x0+8,b2,x0+PW-8,b2,FA,'1')); e.append(LN(x0+8,t2,x0+PW-8,t2,FA,'1','4 4'))
e.append(T(x0+12,b2+16,'0',FA)); e.append(T(x0+12,t2-6,'1',FA))
e.append(T(x0+PW-12,b2+16,'z',FA,'sv-d','end'))
e.append(T(x0+12,PY0+PH+30,'hai đầu bẹt: z đổi nhiều mà p gần như đứng yên',MU))
e.append('</g>')
# ô 3: -log p
e.append('<g class="k3">')
x0=XS[2]; b3=PY0+PH-24; t3=PY0+18
pts=[]
for n in range(1,61):
    pp=n/61.0
    v=min(3.2,-math.log(pp))
    pts.append('%.1f,%.1f'%(x0+12+(PW-24)*pp, b3-(b3-t3)*v/3.2))
e.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.8"/>'%(' '.join(pts),RD))
e.append(LN(x0+8,b3,x0+PW-8,b3,FA,'1'))
e.append(T(x0+12,b3+16,'p = 0',FA)); e.append(T(x0+PW-12,b3+16,'p = 1',FA,'sv-d','end'))
e.append(T(x0+12,PY0+PH+30,'p càng lệch nhãn, mức phạt càng vọt lên',MU))
e.append('</g>')
open(OUT+'h2.svg','w',encoding='utf-8').write(svg(860,PY0+PH+44,
 'Ba ô cùng một trục điểm số z. Ô thứ nhất: đường thẳng z bằng w nhân x cộng b vượt cả mốc 0 lẫn mốc 1 '
 'nên không đọc thẳng thành xác suất được. Ô thứ hai: đường cong sigmoid ép z về khoảng 0 tới 1, hai đầu '
 'bẹt ra nên z đổi nhiều mà p gần như đứng yên. Ô thứ ba: mức phạt trừ log p vọt lên rất nhanh khi p lệch '
 'khỏi nhãn thật, còn gần như bằng 0 khi p đúng và chắc.',
 style([kf(3,5.0,ramp=7.0)]),'\n'.join(e)))
print('h1 h2 ok')

# ═══════════════ HÌNH 3 — bảng: sáu khách → z → p → −log p, dòng phạt nặng tô đỏ
e=[]
X0=10
e.append('<g class="k1">')
e.append(T(0,22,'Sáu khách đi qua w·x + b rồi qua sigmoid',AM))
e.append(T(0,44,'hai cột: đã mua trước (w = 1,22) và tuổi (w = 0,067/năm), b = −3,34',MU))
e.append('</g>')
TY=72
COLS=[('khách',X0+8,None),('đã mua trước',X0+180,'end'),('tuổi',X0+260,'end'),
      ('z',X0+350,'end'),('p',X0+430,'end'),('nhãn thật',X0+540,'end'),('mức phạt',X0+650,'end')]
e.append('<g class="k1">'+''.join(T(x,TY,h,FA,'sv-d',a) for h,x,a in COLS)+'</g>')
MXL=max(NLL)
for i in range(6):
    y=TY+14+i*28
    heavy = NLL[i]>1.0
    col = RD if heavy else (GR if NLL[i]<0.5 else AM)
    rgb = 'red-a' if heavy else ('green-a' if NLL[i]<0.5 else 'amber-a')
    e.append('<g class="k%d">'%(i%4+2))
    e.append(RC(X0-6,y,780,22,col,rgb,'.14' if heavy else '.10',rx=3,sw='1.1' if heavy else '1'))
    e.append(T(X0+8,y+16,ID[i],'var(--text)','sv-t'))
    e.append(T(X0+180,y+16,'có' if PREV[i] else 'không',MU,'sv-d','end'))
    e.append(T(X0+260,y+16,str(AGE[i]),MU,'sv-d','end'))
    e.append(T(X0+350,y+16,sgn(Z[i]),MU,'sv-d','end'))
    e.append(T(X0+430,y+16,n2(P[i]),col,'sv-t','end'))
    e.append(T(X0+540,y+16,'mua' if LAB[i] else 'không mua',MU,'sv-d','end'))
    e.append(T(X0+650,y+16,n2(NLL[i]),col,'sv-t','end'))
    bw=max(3.0,120*NLL[i]/MXL)
    e.append(RC(X0+662,y+6,bw,12,col,rgb,'.30',rx=2,sw='1'))
    e.append('</g>')
BY=TY+14+6*28+12
e.append('<g class="k6">')
e.append(T(0,BY+16,'E tự tin nhất (p = %s) mà nhãn thật là không mua — nên chịu mức phạt nặng nhất %s'%(n2(P[4]),n2(NLL[4])),RD,'sv-t'))
e.append(T(0,BY+38,'log loss là trung bình cột cuối: %s'%n2(LOSS),MU))
e.append('</g>')
open(OUT+'h3.svg','w',encoding='utf-8').write(svg(812,BY+52,
 'Bảng sáu khách A đến F chạy qua công thức với hai cột đã mua trước hệ số 1,22 và tuổi hệ số 0,067 mỗi '
 'năm, b bằng trừ 3,34. Mỗi dòng hiện dần: cột z, cột p, nhãn thật, rồi mức phạt trừ log p kèm một thanh '
 'dài theo mức phạt. A và B có p thấp 0,15 và 0,19 đúng với nhãn không mua nên phạt nhẹ. C, D và F có p '
 'trên 0,5 đúng với nhãn mua nên cũng nhẹ. Riêng E có p cao nhất bằng 0,80 mà nhãn thật là không mua, nên '
 'chịu mức phạt nặng nhất 1,59. Log loss là trung bình cột cuối, bằng 0,56.',
 style([kf(6,7.0,ramp=6.0)]),'\n'.join(e)))

# ═══════════════ HÌNH 4 — quét ngưỡng (thay cho lab)
e=[]
ORD=sorted(range(6),key=lambda i:P[i])
e.append('<g class="k1">')
e.append(T(0,22,'Cùng sáu xác suất đó, chỉ đổi chỗ cắt',AM))
e.append('</g>')
AX,AXW,AY = 40, 560, 74
e.append('<g class="k1">')
e.append(LN(AX,AY,AX+AXW,AY,RU,'1.2'))
for v in (0,0.5,1.0):
    e.append(LN(AX+AXW*v,AY-5,AX+AXW*v,AY+5,FA,'1'))
    e.append(T(AX+AXW*v,AY+22,n2(v,1),FA,'sv-d','middle'))
e.append(T(AX+AXW/2,AY+42,'xác suất p',FA,'sv-d','middle'))
for i in ORD:
    c = GR if LAB[i] else RD
    rgb='green-a' if LAB[i] else 'red-a'
    x=AX+AXW*P[i]
    e.append('<circle cx="%.1f" cy="%.1f" r="6" fill="rgba(var(--%s),.30)" stroke="%s" stroke-width="1.5"/>'%(x,AY,rgb,c))
    e.append(T(x,AY-14 if ORD.index(i)%2==0 else AY+38,ID[i],c,'sv-d','middle'))
e.append(T(0,44,'xanh = mua thật · đỏ = không mua',MU))
e.append('</g>')
for n,(t,(tp,fp,fn,pr,rc)) in enumerate(zip(TT,R)):
    y=132+n*52
    e.append('<g class="k%d">'%(n+2))
    e.append(LN(AX+AXW*t,AY-20,AX+AXW*t,AY+8,AM,'1.6','4 3'))
    e.append(RC(0,y,724,42,AM if n==0 else RU,'amber-a' if n==0 else None,'.08',rx=4,sw='1.1'))
    e.append(T(16,y+26,'ngưỡng %s'%n2(t,1),AM,'sv-t'))
    e.append(T(150,y+26,'bắt đúng %d'%tp,GR))
    e.append(T(270,y+26,'báo nhầm %d'%fp,RD if fp else MU))
    e.append(T(400,y+26,'bỏ sót %d'%fn,RD if fn else MU))
    e.append(T(520,y+26,'precision %s'%n2(pr),MU))
    e.append(T(650,y+26,'recall %s'%n2(rc),MU))
    e.append('</g>')
BY2=132+3*52+8
e.append('<g class="k5">')
e.append(T(0,BY2+18,'Nâng ngưỡng thì bớt báo nhầm nhưng bỏ sót nhiều hơn — không có mức nào đúng sẵn',GR,'sv-t'))
e.append(T(0,BY2+40,'chọn theo chi phí của hai loại lỗi trong bài toán cụ thể',MU))
e.append('</g>')
open(OUT+'h4.svg','w',encoding='utf-8').write(svg(736,BY2+54,
 'Sáu xác suất của A đến F nằm trên một trục từ 0 tới 1, chấm xanh là khách mua thật và chấm đỏ là khách '
 'không mua. Ba vạch cắt lần lượt hiện ra. Ngưỡng 0,5 bắt đúng cả 3 người mua, báo nhầm 1 là E, không bỏ '
 'sót ai, precision 0,75 và recall 1,00. Ngưỡng 0,6 bắt đúng 2, báo nhầm 1, bỏ sót 1, precision và recall '
 'cùng bằng 0,67. Ngưỡng 0,8 bỏ sót cả 3 người mua nên recall về 0. Nâng ngưỡng thì bớt báo nhầm nhưng bỏ '
 'sót nhiều hơn, không có mức nào đúng sẵn, phải chọn theo chi phí của hai loại lỗi.',
 style([kf(5,6.5,ramp=6.0)]),'\n'.join(e)))
print('h3 h4 ok')
