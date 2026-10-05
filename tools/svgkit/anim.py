# -*- coding: utf-8 -*-
"""Hình ĐỘNG dựng theo bước: mỗi bước một nhóm `<g>`, hiện dần rồi giữ tới 100%.

Thêm 2026-09-26 khi dựng lại sáu hình của bài Memory management & GC. Bản cũ
của bài đó cho mọi bước dùng CHUNG một toạ độ, nên bước sau phải tắt bước trước
bằng `100%{opacity:0}` — khung cuối chỉ còn 4/17 nhóm và bản "giảm chuyển động"
gần như trống. Khuôn ở đây chặn cả hai lỗi:

  * `kf()` không sinh mốc tắt — bước nào hiện rồi thì giữ tới hết.
  * `opacity:0` ban đầu nằm TRONG `@media (prefers-reduced-motion:no-preference)`,
    không phải trên thẻ `<g>`. Tắt hoạt hoạ là mọi nhóm hiện đủ (bẫy #1 của
    `.claude/memory/chuan/hinh-dong.md`).

Cách dùng: gom phần tử theo bước bằng `Fig.add(n, ...)` — `n=0` là nền luôn hiện
— rồi `Fig.render(w, h, aria, secs)`. Bố cục phải cho mỗi bước một hàng/cột
RIÊNG, không thì luật "giữ tới 100%" vô nghĩa.
"""
import sys

VBW = 860
CLAY, AM, GR, RD = 'var(--clay)', 'var(--probe)', 'var(--ok)', 'var(--tomb)'
MU, FA, RU = 'var(--muted)', 'var(--faint)', 'var(--rule-hi)'
MONO = 'font-family:ui-monospace,SFMono-Regular,Menlo,monospace'

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def T(x, y, s, c='var(--text)', cls='sv-d', a=None):
    an = ' text-anchor="%s"' % a if a else ''
    return ('<text class="%s" x="%s" y="%s" fill="%s" style="fill:%s"%s>%s</text>'
            % (cls, x, y, c, c, an, esc(s)))

def M(x, y, s, c, a=None):
    """Chữ mono — dùng cho code và tên biến."""
    an = ' text-anchor="%s"' % a if a else ''
    return ('<text class="sv-d" x="%s" y="%s" style="fill:%s;%s"%s>%s</text>'
            % (x, y, c, MONO, an, esc(s)))

def RC(x, y, w, h, st, rgb=None, al='.14', sw='1.5', rx=6, dash=None):
    f = 'rgba(var(--%s),%s)' % (rgb, al) if rgb else 'none'
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, rx, f, st, sw, d))

def LN(x1, y1, x2, y2, c=RU, sw='1.4', dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
            'stroke-width="%s"%s/>' % (x1, y1, x2, y2, c, sw, d))

def ARROW(x1, y1, x2, y2, c, sw='1.5', dash=None):
    """Đường + đầu mũi tên tam giác ở đầu (x2,y2)."""
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    h, w = 9.0, 4.4
    bx, by = x2 - h * math.cos(a), y2 - h * math.sin(a)
    p = ' '.join('%.1f,%.1f' % q for q in [
        (x2, y2), (bx - w * math.sin(a), by + w * math.cos(a)),
        (bx + w * math.sin(a), by - w * math.cos(a))])
    return (LN(x1, y1, bx, by, c, sw, dash)
            + '<polygon points="%s" fill="%s"/>' % (p, c))

def ROUTE(pts, c, sw='1.5', dash=None):
    """Đường gấp khúc qua các điểm, ĐẦU MŨI TÊN ở đoạn cuối.

    Vẽ từng đoạn bằng ARROW rồi thôi là sai: ARROW đặt đầu mũi tên ở cuối MỌI
    đoạn, nên đoạn cua giữa chừng cũng mọc mũi tên chỉ vào khoảng không. Ở đây
    chỉ đoạn cuối mới có đầu mũi tên, và nó phải đâm vào mép ô đích.
    """
    e = [LN(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], c, sw, dash)
         for i in range(len(pts) - 2)]
    e.append(ARROW(pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], c, sw, dash))
    return e

def PILL(x, y, name, c, w=46, h=24, dead=False):
    """Ô tên. dead=True: viền đứt, chữ mờ — cái tên đã bị xoá."""
    e = [RC(x, y, w, h, c, None if dead else 'amber-a', '.16', '1.4',
            rx=h / 2, dash='4 3' if dead else None)]
    e.append(M(x + w / 2, y + h / 2 + 5, name, FA if dead else c, 'middle'))
    return e

def DOTS(x, y, n, c, r=3.6, gap=11):
    """refcnt vẽ thành chấm — đếm được bằng mắt, không cần đọc chữ."""
    e = []
    for i in range(n):
        e.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>'
                 % (x + i * gap, y, r, c))
    return e

def OBJ(x, y, label, n, c=CLAY, w=132, h=46, rgb='clay-a', dead=False):
    """Object trong heap: tên kiểu + dải chấm refcnt + số."""
    col = RD if dead else c
    e = [RC(x, y, w, h, col, 'red-a' if dead else rgb, '.14', '1.6',
            dash='4 3' if dead else None)]
    e.append(M(x + 11, y + 20, label, col))
    dc = RD if (dead or n == 0) else AM
    e += DOTS(x + 13, y + 34, n, dc)
    e.append(T(x + w - 10, y + 38, 'refcnt %d' % n, dc, a='end'))
    return e

def MAT(x, y, vals, st, rgb, cw=46, ch=30, hl=(), al='.13'):
    """Ma trận vẽ thành LƯỚI Ô THẬT, kèm hai dấu ngoặc vuông.

    Luật B của `.claude/memory/chuan/toi-thieu-de-hieu.md`: bài nào có một cấu
    trúc dữ liệu đứng tên thì phải vẽ đúng hình dạng vật đó. Vẽ ma trận bằng một
    ô chữ nhật gắn nhãn "X · n×d" là vẽ QUAN HỆ, không phải vẽ vật — người học
    chưa từng nhìn thấy cái bảng số. `hl` là tập (dòng, cột) tô đậm hơn.
    """
    nr, nc = len(vals), len(vals[0])
    w, h = nc * cw, nr * ch
    e = []
    for i, row in enumerate(vals):
        for j, v in enumerate(row):
            cx, cy = x + j * cw, y + i * ch
            e.append(RC(cx, cy, cw, ch, st, rgb, '.30' if (i, j) in hl else al,
                        '1.1', rx=3))
            e.append(M(cx + cw / 2, cy + ch / 2 + 5, str(v), st, 'middle'))
    b = 7.0
    for sx, d in ((x, 1), (x + w, -1)):
        e.append(LN(sx, y - 3, sx, y + h + 3, st, '1.6'))
        e.append(LN(sx, y - 3, sx + d * b, y - 3, st, '1.6'))
        e.append(LN(sx, y + h + 3, sx + d * b, y + h + 3, st, '1.6'))
    return e

def SIZE(x, y, w, s, c):
    """Nhãn kích thước dưới một ma trận — đọc shape trước, nội dung sau."""
    return [T(x + w / 2, y, s, c, 'sv-l', a='middle')]

def AX(x, y, w, h, c=RU):
    """Trục toạ độ hai chiều: gốc ở góc dưới trái, y tăng LÊN trên."""
    return [LN(x, y, x + w, y, c, '1.2'), LN(x, y, x, y - h, c, '1.2')]

def BIN(x, y, w, h, c, label):
    return [RC(x, y, w, h, c, 'red-a' if c == RD else 'green-a', '.06', '1.4',
               dash='5 3'), T(x, y - 8, label, c)]

def CROSS(x, y, c, s=9):
    return [LN(x - s, y - s, x + s, y + s, c, '2.4'),
            LN(x + s, y - s, x - s, y + s, c, '2.4')]

def BADGE(x, y, s, c, w=None, mono=True):
    w = w or 11 * len(s) + 22
    return [RC(x, y, w, 26, c, ('green-a' if c == GR else
                                'red-a' if c == RD else 'amber-a'), '.16', '1.6', rx=5),
            (M if mono else T)(x + 11, y + 18, s, c)]

def CAP(y, head, hc, subs):
    """Vạch màu + câu chốt + các dòng nhỏ. Trả về (elems, y đáy)."""
    e = [RC(0, y, 3, 20, hc, ('amber-a' if hc == AM else 'red-a' if hc == RD
                              else 'green-a'), '1', '0', rx=1.5),
         T(14, y + 15, head, hc)]
    yy = y + 32
    for s in subs:
        e.append(T(14, yy, s, MU))
        yy += 18
    return e, yy

# ── dòng thời gian ────────────────────────────────────────────────────────
def kf(steps, cyc, ramp=5.5, start=2.0, pref='k'):
    """Mỗi bước hiện dần rồi GIỮ TỚI 100%. Không mốc tắt — đó là cả điểm."""
    ks, cs = [], []
    span = (100.0 - start - ramp) / max(steps - 1, 1)
    for i in range(steps):
        a = start + i * span
        ks.append('@keyframes %s%d{0%%{animation-timing-function:ease-in-out;opacity:0}'
                  '%.3f%%{animation-timing-function:ease-in-out;opacity:0}'
                  '%.3f%%{animation-timing-function:ease-in-out;opacity:1}'
                  '100%%{animation-timing-function:ease-in-out;opacity:1}}'
                  % (pref, i + 1, a, a + ramp))
        # opacity:0 ban đầu nằm TRONG media query, không phải trên thẻ <g>:
        # tắt hoạt hoạ thì mọi nhóm hiện đủ (bẫy #1 của hinh-dong.md).
        cs.append('.%s%d{opacity:0;animation:%s%d %.1fs linear 1 forwards}'
                  % (pref, i + 1, pref, i + 1, cyc))
    return ('<style>' + ''.join(ks) + '@media (prefers-reduced-motion:no-preference){'
            + ''.join(cs) + '}</style>')

class Fig:
    """Gom phần tử theo BƯỚC. Bước 1 hiện trước, bước cuối hiện sau."""
    def __init__(self):
        self.steps = {}
        self.base = []
    def add(self, step, *elems):
        for e in elems:
            (self.base if step == 0 else self.steps.setdefault(step, [])).extend(
                e if isinstance(e, list) else [e])
    def render(self, w, h, aria, secs, pref=None):
        # @keyframes là TOÀN CỤC cho cả trang, <svg> không giới hạn nó. Hai hình
        # cùng dùng tên "k1" thì bản sau ghi đè bản trước và mọi hình trong bài
        # chạy theo mốc của hình cuối. Nên mỗi hình phải có tiền tố riêng.
        n = max(self.steps) if self.steps else 1
        pref = pref or ('s%d_k' % Fig._seq())
        body = '\n'.join(self.base)
        for i in range(1, n + 1):
            body += '\n<g class="%s%d">%s</g>' % (pref, i, ''.join(self.steps.get(i, [])))
        return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s" data-anim>%s\n%s\n</svg>'
                % (w, h, esc(aria), kf(n, secs, pref=pref), body))

    _n = [0]
    @classmethod
    def _seq(cls):
        cls._n[0] += 1
        return cls._n[0]
