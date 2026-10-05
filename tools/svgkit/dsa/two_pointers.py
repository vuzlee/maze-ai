"""Figures for content/01-dsa/04-algorithms/two-pointers. Uses arrkit.py (do not edit it)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arrkit import *  # noqa

OUT = {}
DT = 2.6

def converge():
    a, tg = [2, 3, 5, 8, 11, 15, 19], 16
    f = Anim('tp-m1-', 660, 270, 'Sorted list 2 3 5 8 11 15 19, find two numbers summing to 16. l starts at 0, r at 6. 2+19=21 too big: r moves left. 2+15=17: r left. 2+11=13 too small: l right. 3+11=14: l right. 5+11=16: found at indices 2 and 4 in 5 steps.',
             'TWO SUM ON A SORTED LIST · TARGET 16', 2.5)
    code = Code2(0, 40, ['l, r = 0, len(a) - 1', 'while l < r:', '    s = a[l] + a[r]', '    if s == t: return l, r',
                         '    if s < t: l += 1', '    else: r -= 1'], 250)
    f.static(code.svg())
    row = Row(290, 92, a); row.draw(f, .2)
    f.show(chip(560, 34, 'target 16'), .8)
    L_ = Ptr(row, 'l', 0); R_ = Ptr(row, 'r', 6)
    code.at(1.2, 0)
    l, r, t, seq_st, seq_v = 0, 6, 1.8, [], []
    rings = []
    n = 0
    while True:
        n += 1
        s = a[l] + a[r]
        code.at(t, 2)
        seq_st.append((t, st(290, 214, 's = a[%d] + a[%d] = %d + %d = %d' % (l, r, a[l], a[r], s))))
        rings.append((t, row.ring(l) + row.ring(r)))
        if s == tg:
            code.at(t + 1, 3)
            seq_v.append((t + 1, st(290, 238, '%d == 16 → found' % s, MID, True)))
            tf = t + 2.2
            break
        if s < tg:
            code.at(t + 1, 4)
            seq_v.append((t + 1, st(290, 238, '%d < 16 → a[%d] is too small for any r: l += 1' % (s, l), MID, True)))
            f.show(row.cell(l, 'g'), t + 1.4); l += 1; L_.to(t + 1.6, l)
        else:
            code.at(t + 1, 5)
            seq_v.append((t + 1, st(290, 238, '%d > 16 → a[%d] is too big for any l: r -= 1' % (s, r), MID, True)))
            f.show(row.cell(r, 'g'), t + 1.4); r -= 1; R_.to(t + 1.6, r)
        t += DT
    states(f, rings, tf)
    states(f, seq_st, tf)
    states(f, seq_v, tf)
    L_.emit(f, 1.2); R_.emit(f, 1.2)
    code.emit(f)
    f.show(row.cell(l, 'f') + row.cell(r, 'f'), tf)
    f.show(lab(row.cx(l), 76, '✓ found', TG, 'middle', True) + lab(row.cx(r), 76, '✓ found', TG, 'middle', True), tf)
    f.show(st(290, 214, 'found at indices %d and %d · %d steps for 7 cells' % (l, r, n), TG, True), tf + .2)
    OUT['m1'] = f.render()

def cost():
    f = Anim('tp-m2-', 660, 420, 'Ten cells: every step greys out exactly one end cell, so the pointers meet after 9 steps. A graph of steps against n: two pointers follow the straight line n, while checking every pair grows as n squared over 2.',
             'O(n) · EVERY STEP DROPS ONE CELL FOR GOOD', 2.5)
    row = Row(80, 50, [3, 6, 9, 12, 15, 18, 21, 24, 27, 30])
    row.draw(f, .2)
    L_ = Ptr(row, 'l', 0); R_ = Ptr(row, 'r', 9, up=True)
    l, r, t = 0, 9, 1.2
    cnt = []
    k = 0
    while l < r:
        k += 1
        if k % 2: f.show(row.cell(r, 'g'), t); r -= 1; R_.to(t + .1, r)
        else: f.show(row.cell(l, 'g'), t); l += 1; L_.to(t + .1, l)
        cnt.append((t, st(80, 170, 'steps: %d · cells left: %d' % (k, r - l + 1), MID, True)))
        t += .8
    states(f, cnt)
    L_.emit(f, .8); R_.emit(f, .8)
    f.show(st(330, 170, '→ n cells, at most n - 1 steps', TG, True), t)
    gx, gy, gw, gh = 80, 210, 440, 150
    px = lambda v: gx + v / 40 * gw
    py = lambda v: gy + gh - v / 800 * gh
    t += .6
    f.show(axes(gx, gy, gw, gh, [0, 10, 20, 30, 40], [0, 200, 400, 600, 800], 'n', 'steps', px, py), t)
    t += .6
    pts1 = [(px(n), py(n)) for n in range(0, 41, 2)]
    pts2 = [(px(n), py(n * (n - 1) / 2)) for n in range(0, 41) if n * (n - 1) / 2 <= 800]
    for i in range(1, len(pts1)):
        f.show(poly(pts1[i - 1:i + 1], PT, 2.6), t + i * .08, d=.12)
    t2 = t + len(pts1) * .08 + .3
    for i in range(1, len(pts2)):
        f.show(poly(pts2[i - 1:i + 1], MID, 2.2, '5 4'), t2 + i * .06, d=.12)
    t3 = t2 + len(pts2) * .06 + .2
    for n in (10, 20, 30, 40):
        f.show(dot(px(n), py(n), PT), t3)
    for n in (10, 20, 30, 40):
        if n * (n - 1) / 2 <= 800: f.show(dot(px(n), py(n * (n - 1) / 2), MID), t3)
    f.show(lab(px(40) + 8, py(40) - 6, 'two pointers: n', PT, bold=True), t3)
    f.show(lab(pts2[-1][0] + 8, pts2[-1][1] + 4, 'every pair: n²/2', MID, bold=True), t3)
    f.show(st(gx, 408, 'n = 40: 39 steps instead of 780 pairs', TG, True), t3 + .4)
    OUT['m2'] = f.render()

def water():
    h = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    f = Anim('tp-p1-', 660, 350, 'Container with most water, heights 1 8 6 2 5 4 8 3 7. l at 0, r at 8. Each step the water area is min height times width; the lower side moves inward because it can never do better. Best area 49 between index 1 and 8.',
             'CONTAINER WITH MOST WATER · MOVE THE LOWER SIDE', 2.5)
    x0, w, g, base, u = 120, 34, 14, 230, 18
    X = lambda i: x0 + i * (w + g)
    CX = lambda i: X(i) + w / 2
    def bar(i, kind):
        fill, stc, tc = {'n': ('var(--bg)', RULE_HI, TX), 'g': ('var(--sunk)', 'var(--rule)', GH), 'f': (TG, TG, ON)}[kind]
        return R(X(i), base - h[i] * u, w, h[i] * u, fill, stc, 4, 1.2) + T(CX(i), base - 5, str(h[i]), tc, mono=True, bold=True)
    for i in range(9):
        f.show(bar(i, 'n') + idx(CX(i), base + 16, i), .2 + i * .05)
    f.show(chip(520, 34, 'best = ?'), .7)
    class P2:
        def __init__(s, name, k): s.name, s.k0, s.pts = name, k, [(0, 0, 0)]
        def to(s, t, k): s.pts.append((t, (k - s.k0) * (w + g), 0))
        def emit(s, hide=None): f.path(ptr_dn(CX(s.k0), base + 22, s.name), s.pts, 1.0, d=.5, hide=hide)
    Lp, Rp = P2('l', 0), P2('r', 8)
    l, r, t, best, bi = 0, 8, 1.4, 0, None
    water_s, stat, verd, chips = [], [], [], []
    while l < r:
        hh = min(h[l], h[r]); area = hh * (r - l)
        water_s.append((t, R(X(l) + w, base - hh * u, X(r) - X(l) - w, hh * u, vt('.14'), MID, 2, 1.4)))
        stat.append((t, st(120, 316, 'area = min(%d, %d) × (%d - %d) = %d' % (h[l], h[r], r, l, area))))
        if area > best:
            best, bi = area, (l, r); chips.append((t + .6, chip(520, 34, 'best = %d' % best)))
        if h[l] < h[r]:
            verd.append((t + .7, st(120, 338, 'a[l] = %d is lower → l += 1' % h[l], MID, True)))
            f.show(bar(l, 'g'), t + 1.2); l += 1; Lp.to(t + 1.3, l)
        else:
            verd.append((t + .7, st(120, 338, 'a[r] = %d is not higher → r -= 1' % h[r], MID, True)))
            f.show(bar(r, 'g'), t + 1.2); r -= 1; Rp.to(t + 1.3, r)
        t += 2.0
    states(f, water_s, t); states(f, stat, t); states(f, verd, t)
    f.show(chip(520, 34, 'best = ?'), .7, hide=chips[0][0] - .05)
    states(f, chips)
    Lp.emit(t); Rp.emit(t)
    a_, b_ = bi
    f.show(R(X(a_) + w, base - 7 * u, X(b_) - X(a_) - w, 7 * u, it('.16'), TG, 2, 1.4) + bar(a_, 'f') + bar(b_, 'f'), t)
    f.show(lab(CX(a_), base - h[a_] * u - 8, '✓', TG, 'middle', True) + lab(CX(b_), base - h[b_] * u - 8, '✓', TG, 'middle', True), t)
    f.show(st(120, 316, '✓ best area 49 between index 1 and 8 · 8 steps, not 36 pairs', TG, True), t + .2)
    OUT['p1'] = f.render()

def dedup():
    a = [1, 1, 2, 2, 2, 3, 4, 4]
    f = Anim('tp-p2-', 680, 290, 'Remove duplicates in place from 1 1 2 2 2 3 4 4. slow marks where the next kept value is written, fast reads every cell. A duplicate is skipped and greys out; a new value is copied to slow and slow moves right. Result 1 2 3 4, length 4.',
             'REMOVE DUPLICATES IN PLACE · SLOW WRITES, FAST READS', 2.5)
    code = Code2(0, 40, ['slow = 1', 'for fast in range(1, len(a)):', '    if a[fast] != a[slow - 1]:', '        a[slow] = a[fast]',
                         '        slow += 1', 'return slow'], 262)
    f.static(code.svg())
    row = Row(290, 100, a); row.draw(f, .2)
    f.show(chip(560, 34, 'keep unique'), .7)
    S = Ptr(row, 'slow', 1, up=True); F = Ptr(row, 'fast', 1)
    code.at(1.0, 0)
    cur = list(a); slow, t = 1, 1.6
    rings, stat, verd = [], [], []
    for fast in range(1, 8):
        code.at(t, 1); code.at(t + .5, 2)
        if fast > 1: F.to(t, fast)
        rings.append((t + .5, row.ring(fast) + row.ring(slow - 1)))
        stat.append((t + .5, st(290, 240, 'a[fast=%d] = %d  vs  a[slow-1=%d] = %d' % (fast, cur[fast], slow - 1, cur[slow - 1]))))
        if cur[fast] != cur[slow - 1]:
            code.at(t + 1.3, 3)
            verd.append((t + 1.3, st(290, 264, 'new value → a[%d] = %d, slow += 1' % (slow, cur[fast]), MID, True)))
            cur[slow] = cur[fast]
            f.show(row.cell(slow, 'b', cur[slow]), t + 1.5)
            code.at(t + 1.9, 4)
            slow += 1; S.to(t + 1.9, slow)
            t += 2.7
        else:
            verd.append((t + 1.3, st(290, 264, 'duplicate → skip', MID, True)))
            f.show(row.cell(fast, 'g', cur[fast]), t + 1.5)
            t += 2.1
    code.at(t, 5)
    states(f, rings, t); states(f, stat, t); states(f, verd, t)
    S.emit(f, 1.0); F.emit(f, 1.0, hide=t)
    code.emit(f)
    for i in range(8):
        f.show(row.cell(i, 'f', cur[i]) if i < slow else row.cell(i, 'g', cur[i]), t + .2)
    f.show(lab((row.xl(0) + row.right() - (8 - slow) * P) / 2, 168, '✓ length %d' % slow, TG, 'middle', True), t + .3)
    f.show(st(290, 240, 'a[:4] = 1 2 3 4 · one pass, no extra list', TG, True), t + .4)
    OUT['p2'] = f.render()

converge(); cost(); water(); dedup()
json.dump(OUT, open('/tmp/dsa/two-pointers.json', 'w'))
print({k: len(v) for k, v in OUT.items()})
