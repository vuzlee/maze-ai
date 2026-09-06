#!/usr/bin/env python3
"""Soat MOI tieu chi cua chuan-bai-mau.md cung mot luot, cho ca 5 ke co noi dung.

    python3 tools/audit.py            # bang tom tat + danh sach bai chua dat
    python3 tools/audit.py <slug>     # chi tiet mot bai

Sau moi dot sua PHAI chay lai chinh script nay roi moi duoc ghi "xong" vao
.claude/memory/nhat-ky/ban-do-ver-bai-toan-kho.md. Dung tu nghi ra metric moi:
bai hoc cua dot 06/09 va 07/09 la moi metric roi rac deu bo sot mot truc.

Sau tieu chi, moi bai phai dat CA SAU:
  gist@s1  §01 chua <figure class="gist">        (mental model cua ca bai)
  ten      §01 phai ten "Mental model"
  gist=1   ca bai dung MOT figure.gist
  TK       khong con muc "Tong ket mot hinh"     (no da thanh §01)
  thieu    moi muc noi dung co it nhat mot khoi truc quan
  C        duoi 12 muc
"""
import re,html,glob,os,json,collections
VIS=['class="strip','class="flow','class="cmp','class="stack','class="mtx',
     'class="axis','class="seq','class="bars','class="eq','<table','class="probs']
NOFIG=('lỗi hay gặp','hỏi đáp','mẫu code','lab','từ điển bỏ túi','bài leetcode',
       'học theo thứ tự nào','đọc tiếp')
rows=[]
for p in sorted(glob.glob('content/0[1-5]*/*/*/index.html')):
    s=open(p,encoding='utf-8').read()
    if 'data-skeleton="1"' in s: continue
    ke=p.split('/')[1]; slug=p.split('/')[3]
    secs=re.split(r'(?=<section id=)',s)[1:]
    if not secs: continue
    n=len(secs); bad=[]
    heads=[html.unescape(re.search(r'<h2>(.*?)</h2>',x,re.S).group(1)) for x in secs]
    # L1a: gist o §01
    g1='figure class="gist"' in secs[0]
    # L1b: het Tong ket
    tk=any('tổng kết' in h.lower() for h in heads)
    # L1c: moi muc noi dung co hinh
    miss=[]
    for x,h in zip(secs,heads):
        if any(k in h.lower() for k in NOFIG): continue
        if x.count('<svg')==0 and not any(v in x for v in VIS): miss.append(h[:28])
    # L1d: ten §01
    m1 = heads[0].strip().lower().startswith('mental model')
    # C: >=12 muc
    lc = n>=12
    # gist duy nhat
    ng=s.count('figure class="gist"')
    rows.append(dict(ke=ke,slug=slug,n=n,g1=g1,tk=tk,miss=miss,m1=m1,lc=lc,ng=ng,h1=heads[0][:34]))
ok=[r for r in rows if r['g1'] and not r['tk'] and not r['miss'] and r['m1'] and not r['lc'] and r['ng']==1]
print('TONG bai co noi dung:',len(rows),' DAT HET:',len(ok))
c=collections.Counter()
for r in rows:
    if not r['g1']: c['thieu gist@s1']+=1
    if r['tk']: c['con Tong ket']+=1
    if r['miss']: c['muc thieu hinh']+=1
    if not r['m1']: c['§01 chua ten Mental model']+=1
    if r['lc']: c['>=12 muc (luat C)']+=1
    if r['ng']!=1: c['so gist != 1']+=1
for k,v in c.most_common(): print(f'  {v:4}  {k}')
json.dump(rows,open('/tmp/audit.json','w'))

# --- danh sach bai chua dat -------------------------------------------------
def probs(x):
    q=[]
    if not x['g1']: q.append('gist@s1')
    if x['tk']: q.append('TK')
    if x['miss']: q.append('thieu%d'%len(x['miss']))
    if not x['m1']: q.append('ten')
    if x['lc']: q.append('C%d'%x['n'])
    if x['ng']!=1: q.append('gist=%d'%x['ng'])
    return q

if __name__=='__main__':
    import sys
    arg=sys.argv[1] if len(sys.argv)>1 else None
    print('\n=== BAI CHUA DAT ===')
    for x in sorted(rows,key=lambda z:(z['ke'],z['slug'])):
        if arg and arg not in (x['ke'],x['slug']): continue
        q=probs(x)
        if q: print(f"{x['ke'][:12]:13}{x['slug']:30}{','.join(q):26}{x['h1']}")
