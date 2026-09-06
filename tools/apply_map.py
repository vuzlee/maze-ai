#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chuyen mot bai nhom D sang khuon mental model.

Nhom D = bai con muc "Tong ket mot hinh" o CUOI. Luat 1 doi nguoc lai: hinh
tong ket chinh la MENTAL MODEL, nen no phai dung DAU bai, va moi muc duoi la
mot lan boc tach chinh ban do do ra — to sang o dang hoc.

Dung:  from tools.apply_map import run
       run(path, boxes, panels, label, hi_of={sid: chi_so_o}, skip={sid})

  boxes   [(tieu_de, [dong_phu...], mau)]  — cac o cua ban do, thu tu tren xuong
  panels  {chi_so_o: (dau_de_panel, [(dong, dong_phu, mau)...])}
          chi_so 0 = ban do tong (khong o nao sang), dung cho muc Mental model
  hi_of   muc nao to sang o nao. Muc khong co trong day thi khong nhan hinh.
  skip    muc DA co hinh rieng day tot — dung chen them (bay thu tu: mot muc
          hai hinh la pham luat "moi muc mot hinh"; muon ca hai thi TACH MUC).

Mau: 'p' probe · 'b' filled · 'g' ok · 'r' tomb · 'n' muted.
"""
import re,collections,sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'svgkit'))
from mapgen import build

FIG='  <figure class="%s">\n%s\n  <figcaption>%s</figcaption>\n  </figure>\n'

def run(path, boxes, panels, label, hi_of, caps, key1, skip=()):
    s=open(path,encoding='utf-8').read()
    pre=re.search(r'<section id="([a-z0-9-]+)-s\d+"',s).group(1)
    R={i:build(boxes,i,h,rows,label) for i,(h,rows) in panels.items()}

    new=(f'<section id="{pre}-s0" class="lesson">\n'
         f'  <div class="sh"><b>00</b><h2>Mental model</h2></div>\n'
         f'  <p class="key">{key1}</p>\n\n'+FIG%('gist',R[0],caps[0])+'</section>\n\n')
    i=s.index(f'<section id="{pre}-s1"'); s=s[:i]+new+s[i:]

    for sid,k in hi_of.items():
        if sid in skip: continue
        i=s.index(f'<section id="{sid}"')
        j=s.index('</div>',s.index('<div class="sh">',i))+len('</div>')
        s=s[:j]+'\n\n'+FIG%('scrollx',R[k],caps[k])+s[j:]

    m=re.search(r'<section id="([^"]+)"[^>]*>\s*<div class="sh"><b>\d+</b><h2>[^<]*T&#7893;ng k&#7871;t[^<]*</h2>',s)
    if not m: m=re.search(r'<section id="([^"]+)"[^>]*>\s*<div class="sh"><b>\d+</b><h2>[^<]*Tổng kết[^<]*</h2>',s)
    if m:
        i=m.start(); j=s.index('</section>',i)+len('</section>')
        while s[j:j+1]=='\n': j+=1
        s=s[:i]+s[j:]
    assert 'Tổng kết' not in s and 'T&#7893;ng k&#7871;t' not in s, 'con muc Tong ket'

    pos=[x.start() for x in re.finditer(rf'<section id="{pre}-s\d+"',s)]
    for n in range(len(pos),0,-1):
        st=pos[n-1]; seg=s[st:st+340]
        seg=re.sub(rf'<section id="{pre}-s\d+"',f'<section id="{pre}-s{n}"',seg,count=1)
        seg=re.sub(r'<b>\d+</b>','<b>%02d</b>'%n,seg,count=1)
        s=s[:st]+seg+s[st+340:]
        pos=[x.start() for x in re.finditer(rf'<section id="{pre}-s\d+"',s)]
    open(path,'w',encoding='utf-8').write(s)

    ids=re.findall(r'<section id="([^"]+)"',s)
    nums=re.findall(r'<div class="sh"><b>(\d+)</b>',s)
    svg=[x.group(0).count('<svg') for x in re.finditer(r'<section id="[^"]+".*?</section>',s,re.S)]
    dup=[k for k,v in collections.Counter(ids).items() if v>1]
    ok = not dup and nums==['%02d'%i for i in range(1,len(nums)+1)]
    print(('OK ' if ok else 'LECH ')+os.path.basename(os.path.dirname(path)),
          '| muc',len(ids),'| svg',svg)
    return ok
