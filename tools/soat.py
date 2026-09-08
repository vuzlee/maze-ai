#!/usr/bin/env python3
"""Soát các lỗi build.py không bắt được. Chạy từ gốc kho: python3 tools/soat.py"""
import os,re,json,sys,html as _html
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
            L=len(_html.unescape(line).rstrip())
            if L>92: print(f"   {L} {p.replace('content/','')}"); n+=1; break
        else: continue
        break
print("   tổng:",n); issues+=n
# ── 6. Thuật ngữ bị dịch ─────────────────────────────────────────────────────
# Vào danh sách này khi: dịch ngược ra ĐÚNG MỘT cụm tiếng Anh có tên riêng.
# Từ tiếng Việt thường (sắp xếp, chuẩn hoá, phân cụm, giảm chiều, nhân bản,
# phân trang, lập lịch, hàm đơn điệu) KHÔNG vào — xem chuan/thuat-ngu-chuan.
DICH = {
 'chia để trị':'divide and conquer', 'danh sách liên kết':'linked list',
 'hai con trỏ':'two pointers', 'cửa sổ trượt':'sliding window',
 'quy hoạch động':'dynamic programming', 'vét cạn':'brute force',
 'tham lam':'greedy', 'duyệt cây':'tree traversal',
 'cây nhị phân tìm kiếm':'binary search tree', 'bảng băm':'hash table',
 'đồ thị có hướng':'directed graph', 'đồ thị vô hướng':'undirected graph',
 'cây quyết định':'decision tree', 'hàm mất mát':'loss function',
 'quá khớp':'overfitting', 'lan truyền ngược':'backpropagation',
 'bắt tay ba bước':'three-way handshake', 'cân bằng tải':'load balancing',
 'bộ nhớ ảo':'virtual memory', 'chuyển ngữ cảnh':'context switching',
 'khoá chết':'deadlock', 'điều kiện tranh':'race condition',
 'đa luồng':'multithreading', 'đa tiến trình':'multiprocessing',
 'vòng lặp sự kiện':'event loop', 'thu gom rác':'garbage collection',
 'lề mềm':'soft margin', 'lề cứng':'hard margin',
 'siêu phẳng':'hyperplane',
 'hàng xóm gần nhất':'nearest neighbor', 'hàng xóm':'neighbor',
}
# Chỗ cố ý giữ: nêu tên tiếng Anh rồi chú nghĩa MỘT lần thì được.
MIEN = {('memory-management-gc','thu gom rác'), ('sql-subquery-cte','duyệt cây')}
# Chữ là thuật ngữ ở kệ này nhưng là từ thường ở kệ khác — chỉ soát trong kệ ghi ở đây.
# «hàng xóm»: thuật ngữ của KNN/DBSCAN, nhưng ở DSA và OS nó là từ thường (ô kề, khối liền kề).
KE_RIENG = {'hàng xóm': '05-machine-learning'}
print("\n== 6. Thuật ngữ bị dịch ra tiếng Việt ==")
n=0
for cd,b in B:
    p=b['path']; h=open(p,encoding='utf-8').read(); slug=os.path.basename(os.path.dirname(p))
    # năm mặt: văn xuôi · đầu mục · nhãn SVG · aria-label · data-blurb
    mat = {'văn xuôi': re.sub(r'<(svg|pre|style)[^>]*>.*?</\1>','',h,flags=re.S),
           'nhãn SVG': ' '.join(re.findall(r'<(?:svg|style)[^>]*>.*?</(?:svg|style)>',h,re.S)),
           'aria-label': ' '.join(re.findall(r'aria-label="([^"]*)"',h)),
           'data-blurb': ' '.join(re.findall(r'data-(?:blurb|title)="([^"]*)"',h))}
    for vi,en in DICH.items():
        if (slug,vi) in MIEN: continue
        if vi in KE_RIENG and KE_RIENG[vi] not in p: continue
        for mat_ten,txt in mat.items():
            if vi in txt.lower():
                print(f"   {p.replace('content/','')} [{mat_ten}] «{vi}» -> {en}"); n+=1
print("   tổng:",n); issues+=n

# ── 7. Một bài, một chính tả tên ─────────────────────────────────────────────
# <title> phải MỞ ĐẦU bằng data-title; phụ đề sau dấu — thì được ("— mọi biến thể").
# Sai là khi chính cái TÊN khác nhau (stack-monotonic-queue từng thừa chữ "& queue").
# <h1> tự do hơn nữa: được thay hẳn phụ đề ("DSA — bản đồ").
print("\n== 7. Tên bài lệch giữa <title> và data-title ==")
n=0
for cd,b in B:
    p=b['path']; h=open(p,encoding='utf-8').read()
    def flat(x): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',x.replace('&amp;','&'))).strip().lower()
    dt=flat(re.search(r'data-title="([^"]+)"',h).group(1))
    ti=flat(re.search(r'<title>(.*?)</title>',h,re.S).group(1)).replace(' — mazeai','')
    if not (ti==dt or ti.startswith(dt+" —")): print(f"   {p.replace('content/','')}\n      data-title «{dt}»  ≠  title «{ti}»"); n+=1
print("   tổng:",n); issues+=n

# ── 8. Nợ luật 1: bài dài mà chưa có bản đồ ──────────────────────────────────
# Ngưỡng: >2500 từ HOẶC >10 mục. "Đủ hình" đo theo MỤC, không theo tổng <svg>:
# mọi mục nội dung phải có ít nhất một khối trực quan — và khối trực quan gồm
# cả các khuôn HTML của kit.html, không riêng <svg> (bẫy đã dính 07/09).
VIS=('class="strip','class="flow','class="cmp','class="stack','class="mtx',
     'class="axis','class="seq','class="bars','class="eq','<table','class="probs')
NOFIG=('lỗi hay gặp','hỏi đáp','mẫu code','lab','từ điển bỏ túi','bài leetcode',
       'học theo thứ tự nào','đọc tiếp')
print("\n== 8. Nợ luật 1 — bài dài chưa có figure.gist (dài trước) ==")
no=[]
for cd,b in W:
    p=b['path']; h=open(p,encoding='utf-8').read()
    secs=re.split(r'(?=<section id=)',h)[1:]
    nsec=len(secs); words=len(re.sub(r'<[^>]+>',' ',h).split())
    gist='class="gist"' in h
    miss=0
    for x in secs:
        m=re.search(r'<h2>(.*?)</h2>',x,re.S)
        if not m: continue
        t=_html.unescape(re.sub('<[^>]+>','',m.group(1))).lower()
        if any(k in t for k in NOFIG): continue
        if '<svg' not in x and not any(v in x for v in VIS): miss+=1
    if gist and not miss: continue
    if words>2500 or nsec>10:
        no.append((words,nsec,miss,gist,p))
for w,ns,mi,g,p in sorted(no,reverse=True):
    print(f"   {w:5} từ · {ns:2} mục · {mi:2} mục thiếu hình · {'thiếu hình bóc ô' if g else 'chưa có bản đồ '} · {p.replace('content/','')}")
print("   tổng:",len(no)); issues+=len(no)

print("\n=> tổng số chỗ cần sửa:",issues)
sys.exit(1 if issues else 0)
