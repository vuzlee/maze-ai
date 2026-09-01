#!/usr/bin/env python3
"""Soát các lỗi build.py không bắt được. Chạy từ gốc kho: python3 tools/soat.py"""
import os,re,json,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
cat=open('assets/catalog.js',encoding='utf-8').read()
data=json.loads(re.search(r'=\s*(\[.*\])\s*;?\s*$',cat,re.S).group(1))
B=[(c['dir'],b) for c in data for g in c['groups'] for b in g['books']]
W=[(cd,b) for cd,b in B if not b.get('skeleton')]
SK={os.path.dirname(b['path']) for cd,b in B if b.get('skeleton')}
tok={x.upper() for x in re.findall(r'#[0-9A-Fa-f]{6}',open('assets/style.css',encoding='utf-8').read())}
issues=0
print("== 1. Link trỏ vào bài còn là khung — bấm vào ra trang rỗng ==")
n=0
for cd,b in W:
    p=b['path']; h=open(p,encoding='utf-8').read()
    for href in re.findall(r'href="(\.\.[^"]+)"',h):
        t=os.path.normpath(os.path.join(os.path.dirname(p),href.split('#')[0]))
        t=t[:-11] if t.endswith('/index.html') else t
        if t in SK: print("  ",p.replace('content/',''),"->",t.replace('content/','')); n+=1
print("   tổng:",n); issues+=n
# 2 mau la
print("\n== 2. Màu lạ, không có trong bảng token của style.css ==")
n=0
for cd,b in B:
    p=b['path']; h=open(p,encoding='utf-8').read()
    for m in re.finditer(r'#[0-9a-fA-F]{6}',h):
        if m.group(0).upper() not in tok:
            print("  ",p.replace('content/',''),m.group(0)); n+=1
print("   tổng:",n); issues+=n
# 3 clay trong hinh
print("\n== 3. Màu thương hiệu clay dùng trong hình (cấm) ==")
n=0
for cd,b in B:
    p=b['path']; h=open(p,encoding='utf-8').read()
    for m in re.finditer(r'(?:fill|stroke)="(#(?:E0855C|EE9E7A|C96A44))"',h,re.I):
        print("  ",p.replace('content/',''),m.group(1)); n+=1
print("   tổng:",n); issues+=n
# 4 dau muc dem so
print("\n== 4. Đầu mục đếm số ==")
n=0
for cd,b in W:
    p=b['path']
    for x in re.findall(r'<div class="sh"><b>\d+</b><h2>(.*?)</h2>',open(p,encoding='utf-8').read()):
        t=re.sub('<[^>]+>','',x).strip()
        if re.match(r'(Hai|Ba|Bốn|Năm|Sáu|Bảy|Tám|Chín|Mười)\b',t):
            print("  ",p.replace('content/',''),"|",t); n+=1
print("   tổng:",n); issues+=n
# 5 dong code dai
print("\n== 5. Dòng code dài quá 92 ký tự — dễ tràn ngang trên mobile ==")
n=0
for cd,b in W:
    p=b['path']; h=open(p,encoding='utf-8').read()
    for blk in re.findall(r'<pre[^>]*>(.*?)</pre>',h,re.S):
        for line in re.sub('<[^>]+>','',blk).split('\n'):
            L=len(line.replace('&lt;','<').replace('&gt;','>').replace('&amp;','&').rstrip())
            if L>92: print(f"   {L} {p.replace('content/','')}"); n+=1; break
        else: continue
        break
print("   tổng:",n); issues+=n
print("\n=> tổng số chỗ cần sửa:",issues)
sys.exit(1 if issues else 0)
