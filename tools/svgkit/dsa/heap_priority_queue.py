"""Figures for content/01-dsa/03-data-structures/heap-priority-queue (visual-first DSA lesson).
Every heap is drawn twice: as a tree and as the flat array under it; a swap moves both.
Writes /tmp/dsa/heap-priority-queue.json  {figure key: <figure> html}."""
import sys, os, json, math, heapq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *

PT, MID, TG = 'var(--brand)', 'var(--violet)', 'var(--filled)'
def vt(a): return 'rgba(var(--violet-a),%s)' % a
def it(a): return 'rgba(var(--blue-a),%s)' % a
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
LH = 20
CW, CH, G = 42, 36, 6
NR = 17   # node radius

class Code2:
    def __init__(s, x, y, lines, w=None):
        s.x, s.y, s.lines = x, y, lines
        s.w = w or max(300, 28 + max(len(l) for l in lines) * 6.7)
    def svg(s):
        o = R(s.x, s.y, s.w, len(s.lines) * LH + 14, 'var(--bg)', RULE_HI, 8)
        for i, l in enumerate(s.lines):
            o += T(s.x + 14, s.y + 22 + i * LH, esc(l).replace(' ', ' '), TX, 'start', mono=True)
        return o
    def bar(s): return R(s.x + 4, s.y + 8, s.w - 8, LH, vt('.13'), 'none', 4) + R(s.x + 4, s.y + 8, 3, LH, MID, 'none', 1.5)
    def h(s): return len(s.lines) * LH + 14

class Bar:
    def __init__(s, code): s.code, s.pts = code, [(0, 0, 0)]
    def at(s, t, i): s.pts.append((t, 0, i * LH))
    def emit(s, f): f.path(s.code.bar(), s.pts, 0, appear=False, d=.3)

class Track:
    """items that are born, slide between absolute positions and die."""
    def __init__(s): s.its = []
    def add(s, fn, pos, t, frm=None):
        s.its.append(dict(fn=fn, base=pos, t0=t, mv=[], die=None, frm=frm)); return len(s.its) - 1
    def move(s, k, pos, t): s.its[k]['mv'].append((t, pos))
    def kill(s, k, t): s.its[k]['die'] = t
    def emit(s, f, d=.5):
        for i in s.its:
            bx, by = i['base']
            pts = [(0, i['frm'][0] - bx, i['frm'][1] - by), (i['t0'] + .3, 0, 0)] if i['frm'] else [(0, 0, 0)]
            pts += [(t, x - bx, y - by) for t, (x, y) in i['mv']]
            f.path(i['fn'](bx, by), pts, i['t0'], hide=i['die'], d=d)

def box(x, y, v, kind='n', w=CW, h=CH, sub=None):
    fill, st, c, sw = {'n': ('var(--bg)', RULE_HI, TX, 1.2), 'g': ('var(--sunk)', 'var(--rule)', 'var(--ghost)', 1),
                       'f': (TG, TG, 'var(--on-fill)', 1.2), 't': (it('.12'), TG, TG, 1.3)}[kind]
    o = R(x, y, w, h, fill, st, 6, sw) + T(x + w / 2, y + h / 2 + 5, esc(v), c, mono=True, bold=kind != 'g')
    if sub is not None: o += T(x + w / 2, y + h + 15, esc(sub), FA, cls='sv-s', mono=True)
    return o
def node(x, y, v, kind='n', r=NR):
    fill, st, c = {'n': ('var(--bg)', RULE_HI), 'g': ('var(--sunk)', 'var(--rule)'), 'f': (TG, TG), 't': (it('.12'), TG)}[kind] + ({'n': TX, 'g': 'var(--ghost)', 'f': 'var(--on-fill)', 't': TG}[kind],)
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1.3"/>' % (x, y, r, fill, st) + T(x, y + 5, esc(v), c, mono=True, bold=kind != 'g')
def nring(x, y, r=NR): return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="2.2"/>' % (x, y, r + 4, vt('.10'), MID)
def ring(x, y, w=CW, h=CH): return R(x - 3, y - 3, w + 6, h + 6, vt('.10'), MID, 8, 2.2)
def ptr_up(cx, y, name, ln=14):
    return arrow(cx, y + ln, cx, y, PT, 1.6, None, 6) + T(cx, y + ln + 13, name, PT, mono=True, bold=True)
def say(f, x, y, txt, t, hide=None, c=TX, bold=False, a='start', mono=True):
    f.show(T(x, y, esc(txt), c, a, mono=mono, bold=bold), t, hide=hide)
def chip(x, y, txt):
    w = 24 + len(txt) * 7
    return R(x, y, w, 24, it('.12'), TG, 12, 1.3) + T(x + w / 2, y + 16, esc(txt), TG, mono=True, bold=True)

class Geo:
    """tree positions above, array cells below; both indexed by heap index."""
    def __init__(s, x0, w, y0, lv, ay, levels=4):
        s.x0, s.w, s.y0, s.lv, s.ay = x0, w, y0, lv, ay
    def p(s, i):
        d = int(math.log2(i + 1)); q = i - (2 ** d - 1)
        return s.x0 + (q + .5) * s.w / 2 ** d, s.y0 + d * s.lv
    def cx(s, i): return s.x0 + i * (CW + G)
    def edge(s, i, c=RULE_HI, sw=1.3):
        (x1, y1), (x2, y2) = s.p((i - 1) // 2), s.p(i)
        dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy)
        return L(x1 + dx / n * NR, y1 + dy / n * NR, x2 - dx / n * NR, y2 - dy / n * NR, c, sw)
    def static(s, f, arr, t0=.2, dt=.08, hide=None, idx=True):
        for i, v in enumerate(arr):
            if i: f.show(s.edge(i), t0 + i * dt, hide=hide)
            x, y = s.p(i)
            f.show(node(x, y, v), t0 + i * dt, hide=hide)
            if s.ay is not None:
                f.show(box(s.cx(i), s.ay, v, sub=i if idx else None), t0 + i * dt, hide=hide)
    def items(s, tr, arr, t0=.2, dt=.08):
        """values as sliding items: returns list of (node id, cell id) per heap index"""
        ids = []
        for i, v in enumerate(arr):
            x, y = s.p(i)
            a = tr.add(lambda x_, y_, v=v: node(x_, y_, v), (x, y), t0 + i * dt)
            b = tr.add(lambda x_, y_, v=v: box(x_, y_, v), (s.cx(i), s.ay), t0 + i * dt) if s.ay is not None else None
            ids.append([a, b])
        return ids
    def idx_labels(s, n): return ''.join(T(s.cx(i) + CW / 2, s.ay + CH + 15, str(i), FA, cls='sv-s', mono=True) for i in range(n))

figs = {}
H = [1, 3, 2, 7, 4, 5, 8]

# ---------------------------------------------------------------- m1 · a tree stored in an array
def m1():
    W = 760; g = Geo(330, 400, 64, 62, 248)
    f = Anim('hp-m1-', W, 0, 'Min-heap 1 3 2 7 4 5 8 drawn as a tree and as the array under it. Index 0 is the root; index 1 and 2 are its children. For i = 1 the children sit at 2i+1 = 3 and 2i+2 = 4, the parent at (i-1)//2 = 0; for i = 2 the children are 5 and 6. No pointers are stored: the index arithmetic is the tree.',
             'A HEAP IS A TREE STORED IN A FLAT ARRAY', 3)
    rules = ['parent(i)   = (i - 1) // 2', 'left(i)     = 2*i + 1', 'right(i)    = 2*i + 2']
    code = Code2(0, 40, rules, 260); f.static(code.svg()); bar = Bar(code); tr = Track()
    for i, v in enumerate(H):
        f.show(box(g.cx(i), g.ay, v, sub=i), .2 + i * .05)
    for i, v in enumerate(H):   # nodes appear in index order: level by level, left to right
        x, y = g.p(i)
        if i: f.show(g.edge(i), 1.0 + i * .35)
        f.show(node(x, y, v) + T(x + NR + 4, y - NR + 2, str(i), FA, 'start', cls='sv-s', mono=True), 1.0 + i * .35)
    t = 4.0
    ip = tr.add(lambda x, y: ptr_up(g.cx(1) + CW / 2, g.ay + CH + 22, 'i'), (0, 0), t)
    for k, i in enumerate((1, 2)):
        if k: tr.move(ip, (g.cx(2) - g.cx(1), 0), t)
        x, y = g.p(i)
        f.show(nring(x, y) + ring(g.cx(i), g.ay), t + .3, hide=t + 4.4)
        say(f, 0, 150, 'i = %d · value %d' % (i, H[i]), t + .3, hide=t + 4.4, c=PT)
        for j, (ln, tgt) in enumerate(((0, (i - 1) // 2), (1, 2 * i + 1), (2, 2 * i + 2))):
            tt = t + 1.0 + j * 1.0
            bar.at(tt, ln)
            tx, ty = g.p(tgt)
            f.show(R(g.cx(tgt) - 3, g.ay - 3, CW + 6, CH + 6, 'none', MID, 8, 1.6, '4 3')
                   + '<circle cx="%.1f" cy="%.1f" r="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="4 3"/>' % (tx, ty, NR + 4, MID), tt + .1, hide=t + 4.4)
            expr = ['(%d - 1) // 2 = %d', '2*%d + 1 = %d', '2*%d + 2 = %d'][j] % (i, tgt)
            say(f, 0, 178 + j * 22, ['parent ', 'left   ', 'right  '][j].replace(' ', '\u00a0') + expr, tt + .1, hide=t + 4.4, c=MID)
        t += 4.8
    tr.kill(ip, t)
    tr.emit(f); bar.emit(f)
    x, y = g.p(0)
    f.show(node(x, y, 1, 'f'), t)
    f.show(R(g.cx(0), g.ay, CW, CH, TG, TG, 6, 1.2) + T(g.cx(0) + CW / 2, g.ay + 23, '1', 'var(--on-fill)', mono=True, bold=True), t)
    f.show(T(x + NR + 8, y + 5, '✓ min', TG, 'start', mono=True, bold=True), t + .2)
    f.show(T(0, 150, 'no pointers stored · the index arithmetic is the tree', TG, 'start', bold=True), t + .3)
    f.h = 340
    return f.render()
figs['m1'] = m1()

# ---------------------------------------------------------------- m2 · the heap rule
def m2():
    g = Geo(330, 400, 64, 62, 248)
    f = Anim('hp-m2-', 760, 0, 'Min-heap 1 3 2 7 4 5 8. Each parent is checked against its children: 1 against 3 and 2, 3 against 7 and 4, 2 against 5 and 8. Every parent is smaller, so the root holds the minimum. Siblings 3 and 2 are not in order, and that is allowed: the heap is only half sorted.',
             'THE HEAP RULE · EVERY PARENT ≤ ITS CHILDREN', 3)
    code = Code2(0, 40, ['for i in range(len(h)):', '    for c in (2*i + 1, 2*i + 2):', '        if c < len(h):', '            assert h[i] <= h[c]'])
    f.static(code.svg()); bar = Bar(code); tr = Track()
    g.static(f, H)
    t = 1.6; ip = None
    for i in range(3):
        bar.at(t, 0)
        if ip is None: ip = tr.add(lambda x, y: ptr_up(g.cx(0) + CW / 2, g.ay + CH + 22, 'i'), (0, 0), t)
        else: tr.move(ip, (g.cx(i) - g.cx(0), 0), t)
        x, y = g.p(i)
        f.show(nring(x, y) + ring(g.cx(i), g.ay), t, hide=t + 2.6)
        for j, c in enumerate((2 * i + 1, 2 * i + 2)):
            tt = t + .6 + j * .8
            bar.at(tt, 1); bar.at(tt + .3, 3)
            f.show(g.edge(c, MID, 2.2), tt, hide=t + 2.6)
            say(f, g.x0 + j * 210, 364, 'h[%d] = %d ≤ h[%d] = %d ✓' % (i, H[i], c, H[c]), tt + .3, hide=t + 2.6)
        t += 3.0
    tr.kill(ip, t)
    tr.emit(f); bar.emit(f)
    say(f, g.x0, 364, 'siblings 3 and 2 are not in order — that is allowed', t, hide=t + 2.2, c=MU, mono=False)
    t += 2.4
    x, y = g.p(0)
    f.show(node(x, y, 1, 'f'), t)
    f.show(R(g.cx(0), g.ay, CW, CH, TG, TG, 6, 1.2) + T(g.cx(0) + CW / 2, g.ay + 23, '1', 'var(--on-fill)', mono=True, bold=True), t)
    f.show(T(x + NR + 8, y + 5, '✓ min', TG, 'start', mono=True, bold=True), t + .2)
    f.show(T(g.x0, 364, 'every parent ≤ its children → the root is the minimum', TG, 'start', bold=True), t + .3)
    f.h = 382
    return f.render()
figs['m2'] = m2()

# ---------------------------------------------------------------- p1 · peek
def p1():
    g = Geo(330, 400, 64, 62, 248)
    f = Anim('hp-p1-', 760, 0, 'Min-heap of 7 values. Reading the minimum is reading h[0], the root: one step, whatever the size.',
             'PEEK · THE MINIMUM IS ALWAYS h[0]', 3)
    code = Code2(0, 40, ['x = h[0]'], 230); f.static(code.svg())
    g.static(f, H)
    f.show(chip(0, 120, 'smallest?'), 1.0)
    f.show(code.bar(), 1.8)
    x, y = g.p(0)
    f.show(nring(x, y) + ring(g.cx(0), g.ay), 2.3, hide=3.8)
    say(f, g.x0, 364, 'h[0] = 1 · 1 step', 2.4, hide=3.8, c=MID)
    t = 4.0
    f.show(node(x, y, 1, 'f'), t)
    f.show(R(g.cx(0), g.ay, CW, CH, TG, TG, 6, 1.2) + T(g.cx(0) + CW / 2, g.ay + 23, '1', 'var(--on-fill)', mono=True, bold=True), t)
    f.show(T(x + NR + 8, y + 5, '✓ found', TG, 'start', mono=True, bold=True), t + .2)
    f.show(T(g.x0, 364, 'min = 1 · 1 step at any size · O(1)', TG, 'start', bold=True), t + .3)
    f.h = 382
    return f.render()
figs['p1'] = p1()

# ---------------------------------------------------------------- p2 · push = sift up
def p2():
    g = Geo(340, 400, 58, 54, 268)
    arr = H[:]; x_new = 0
    LS = ['h.append(x); i = len(h) - 1', 'while i > 0 and h[(i - 1) // 2] > h[i]:', '    p = (i - 1) // 2', '    h[i], h[p] = h[p], h[i]', '    i = p']
    code = Code2(0, 40, LS);
    f = Anim('hp-p2-', 760, 0, 'Push 0 into min-heap 1 3 2 7 4 5 8. 0 is appended at index 7, the child of 7. It is smaller than its parent, so they swap, in the tree and in the array at once: 0 rises past 7, then 3, then 1, and stops at the root. 3 swaps for 8 values: one path, O(log n).',
             'PUSH · APPEND AT THE END, THEN SIFT UP', 3)
    f.static(code.svg()); bar = Bar(code); tr = Track()
    ids = g.items(tr, arr)
    for i in range(1, len(arr)): f.show(g.edge(i), .2 + i * .08)
    f.static(g.idx_labels(8))
    f.show(chip(0, 170, 'push 0'), 1.0)
    t = 2.0
    bar.at(t, 0)
    arr.append(x_new); n = len(arr) - 1
    nx, ny = g.p(n)
    f.show(g.edge(n), t + .4)
    a = tr.add(lambda x_, y_: node(x_, y_, x_new), (nx, ny), t + .2, frm=(nx, ny + 40))
    b = tr.add(lambda x_, y_: box(x_, y_, x_new), (g.cx(n), g.ay), t + .2, frm=(g.cx(n), g.ay + 40))
    ids.append([a, b])
    ip = tr.add(lambda x_, y_: ptr_up(g.cx(n) + CW / 2, g.ay + CH + 22, 'i'), (0, 0), t + .6)
    t += 1.4; i = n; swaps = 0
    while True:
        bar.at(t, 1)
        if i == 0:
            say(f, g.x0, 392, 'i = 0 → reached the root', t, hide=t + 1.0); t += 1.2; break
        p = (i - 1) // 2
        (px, py), (cx_, cy_) = g.p(p), g.p(i)
        f.show(nring(px, py) + nring(cx_, cy_), t, hide=t + 1.6)
        f.show(g.edge(i, MID, 2.2), t, hide=t + 1.6)
        big = arr[p] > arr[i]
        say(f, g.x0, 392, 'parent h[%d] = %d %s %d → %s' % (p, arr[p], '>' if big else '≤', arr[i], 'swap' if big else 'stop'), t, hide=t + 1.6)
        if not big: t += 1.8; break
        bar.at(t + .8, 3)
        tr.move(ids[p][0], (cx_, cy_), t + 1.0); tr.move(ids[i][0], (px, py), t + 1.0)
        tr.move(ids[p][1], (g.cx(i), g.ay), t + 1.0); tr.move(ids[i][1], (g.cx(p), g.ay), t + 1.0)
        ids[p], ids[i] = ids[i], ids[p]; arr[p], arr[i] = arr[i], arr[p]; swaps += 1
        bar.at(t + 1.6, 4)
        tr.move(ip, (g.cx(p) - g.cx(n), 0), t + 1.7)
        t += 2.4; i = p
    tr.kill(ip, t)
    tr.emit(f); bar.emit(f)
    x, y = g.p(0)
    f.show(node(x, y, 0, 'f'), t)
    f.show(R(g.cx(0), g.ay, CW, CH, TG, TG, 6, 1.2) + T(g.cx(0) + CW / 2, g.ay + 23, '0', 'var(--on-fill)', mono=True, bold=True), t)
    f.show(T(x + NR + 8, y + 5, '✓ new min', TG, 'start', mono=True, bold=True), t + .2)
    f.show(T(g.x0, 392, '%d swaps for %d values · one path up the tree · O(log n)' % (swaps, len(arr)), TG, 'start', bold=True), t + .3)
    assert arr == [0, 1, 2, 3, 4, 5, 8, 7], arr
    f.h = 408
    return f.render()
figs['p2'] = p2()

# ---------------------------------------------------------------- p3 · pop = sift down
def p3():
    g = Geo(340, 400, 64, 62, 248)
    arr = H[:]
    LS = ['top = h[0]; h[0] = h.pop()', 'i = 0', 'while 2*i + 1 < len(h):', '    c = smaller child of i', '    if h[i] <= h[c]: break',
          '    h[i], h[c] = h[c], h[i]; i = c', 'return top']
    code = Code2(0, 40, LS)
    f = Anim('hp-p3-', 760, 0, 'Pop from min-heap 1 3 2 7 4 5 8. The root 1 is taken out. The last value 8 moves into the root, in the tree and in the array. 8 is compared with its smaller child: it swaps with 2, then with 5, and stops at a leaf. 1 is returned after 2 swaps: one path, O(log n).',
             'POP · TAKE THE ROOT, MOVE THE LAST VALUE UP, SIFT DOWN', 3)
    f.static(code.svg()); bar = Bar(code); tr = Track()
    ids = g.items(tr, arr)
    for i in range(1, len(arr)):
        if i == 6: continue
        f.show(g.edge(i), .2 + i * .08)
    f.static(g.idx_labels(6))
    f.show(T(g.cx(6) + CW / 2, g.ay + CH + 15, '6', FA, cls='sv-s', mono=True), .2, hide=4.0)
    f.show(chip(0, 210, 'pop min'), 1.0)
    t = 2.0
    bar.at(t, 0)
    rx, ry = g.p(0)
    f.show(nring(rx, ry), t, hide=t + .8)
    # root leaves to the side, cell 0 leaves too
    OX, OY = 100, 270
    tr.move(ids[0][0], (OX + 40, OY), t + .6); tr.kill(ids[0][1], t + .6)
    f.show(T(OX, OY + 5, 'top =', MU, 'end', mono=True), t + .8)
    # last value goes to the root; edge 6 disappears
    f.show(g.edge(6), .2 + 6 * .08, hide=t + 1.5)
    lx, ly = g.p(6)
    tr.move(ids[6][0], (rx, ry), t + 1.5); tr.move(ids[6][1], (g.cx(0), g.ay), t + 1.5)
    ids[0] = ids[6]; ids.pop(); arr[0] = arr.pop()
    t += 2.6
    bar.at(t, 1)
    ip = tr.add(lambda x_, y_: ptr_up(g.cx(0) + CW / 2, g.ay + CH + 22, 'i'), (0, 0), t)
    t += .8; i = 0; swaps = 0; n = len(arr)
    while True:
        bar.at(t, 2)
        if 2 * i + 1 >= n:
            say(f, g.x0, 364, 'i = %d has no children → stop' % i, t, hide=t + 1.2); t += 1.4; break
        bar.at(t + .3, 3)
        kids = [c for c in (2 * i + 1, 2 * i + 2) if c < n]
        c = min(kids, key=lambda c: arr[c])
        for k in kids:
            kx, ky = g.p(k); f.show(nring(kx, ky), t + .3, hide=t + 1.0)
        say(f, g.x0, 364, 'children %s → smaller is h[%d] = %d' % (' and '.join(str(arr[k]) for k in kids), c, arr[c]), t + .3, hide=t + 1.0)
        bar.at(t + 1.1, 4)
        (ix, iy), (cx_, cy_) = g.p(i), g.p(c)
        f.show(nring(ix, iy) + nring(cx_, cy_) + g.edge(c, MID, 2.2), t + 1.1, hide=t + 2.4)
        big = arr[i] > arr[c]
        say(f, g.x0, 364, 'h[%d] = %d %s %d → %s' % (i, arr[i], '>' if big else '≤', arr[c], 'swap' if big else 'stop'), t + 1.1, hide=t + 2.4)
        if not big: t += 2.6; break
        bar.at(t + 1.9, 5)
        tr.move(ids[i][0], (cx_, cy_), t + 2.0); tr.move(ids[c][0], (ix, iy), t + 2.0)
        tr.move(ids[i][1], (g.cx(c), g.ay), t + 2.0); tr.move(ids[c][1], (g.cx(i), g.ay), t + 2.0)
        ids[i], ids[c] = ids[c], ids[i]; arr[i], arr[c] = arr[c], arr[i]; swaps += 1
        tr.move(ip, (g.cx(c) - g.cx(0), 0), t + 2.6)
        t += 3.2; i = c
    bar.at(t, 6); tr.kill(ip, t)
    tr.emit(f); bar.emit(f)
    t += .3
    f.show(node(OX + 40, OY, 1, 'f'), t)
    f.show(T(OX + 40, OY + NR + 18, '✓ returned', TG, mono=True, bold=True), t + .2)
    f.show(T(g.x0, 364, '%d swaps for %d values · one path down the tree · O(log n)' % (swaps, len(H)), TG, 'start', bold=True), t + .3)
    assert arr == [2, 3, 5, 7, 4, 8], arr
    f.h = 382
    return f.render()
figs['p3'] = p3()

# ---------------------------------------------------------------- p4 · search
def p4():
    g = Geo(330, 400, 64, 62, 248)
    target = 5; ans = H.index(target)
    code = Code2(0, 40, ['for i in range(len(h)):', '    if h[i] == t: return i', 'return -1'])
    f = Anim('hp-p4-', 760, 0, 'Search for 5 in min-heap 1 3 2 7 4 5 8. The heap rule does not say whether 5 is left or right, so i walks the array cell by cell: 1, 3, 2, 7, 4 grey out, 5 is found at index 5 after 6 checks. Search is O(n).',
             'SEARCH · THE RULE DOES NOT SAY LEFT OR RIGHT, SO CHECK EVERY CELL', 3)
    f.static(code.svg()); bar = Bar(code); tr = Track()
    g.static(f, H)
    ax, ay = g.p(ans)
    f.show(R(g.cx(ans) - 4, g.ay - 4, CW + 8, CH + 8, 'none', TG, 8, 1.4, '4 3'), 1.0)
    f.path(chip(g.cx(ans) - 30, g.ay - 34, 'target = 5'), [(0, 0, 0), (2.2, 10 - (g.cx(ans) - 30), 150 - (g.ay - 34))], 1.0)
    t = 3.2; ip = None
    for i, v in enumerate(H):
        bar.at(t, 0)
        if ip is None: ip = tr.add(lambda x_, y_: ptr_up(g.cx(0) + CW / 2, g.ay + CH + 22, 'i'), (0, 0), t)
        else: tr.move(ip, (g.cx(i) - g.cx(0), 0), t)
        bar.at(t + .5, 1)
        x, y = g.p(i)
        f.show(nring(x, y) + ring(g.cx(i), g.ay), t + .5, hide=t + 1.5)
        hit = v == target
        say(f, g.x0, 364, 'h[%d] = %d %s 5%s' % (i, v, '==' if hit else '≠', '' if hit else ' → next cell'), t + .5, hide=t + 1.5 if not hit else t + 1.8)
        if hit: break
        f.show(node(x, y, v, 'g') + box(g.cx(i), g.ay, v, 'g'), t + 1.2)
        t += 1.7
    tr.kill(ip, t + 1.8)
    tr.emit(f); bar.emit(f)
    t += 2.0
    f.show(node(ax, ay, 5, 'f') + box(g.cx(ans), g.ay, 5, 'f'), t)
    f.show(T(ax, ay + NR + 16, '✓ found', TG, mono=True, bold=True), t + .2)
    f.show(T(g.x0, 364, 'found at index %d · %d checks for %d cells · O(n)' % (ans, ans + 1, len(H)), TG, 'start', bold=True), t + .3)
    f.h = 382
    return f.render()
figs['p4'] = p4()

# ---------------------------------------------------------------- p5 · height = log n
def p5():
    f = Anim('hp-p5-', 760, 0, 'A full tree fills level by level: 1, 2, 4, 8 nodes, so 15 values fit in 4 levels. Push and pop walk one path, at most one swap per level. A graph of levels against n: the straight O(n) line climbs, log2 n stays almost flat: a million values need 20 levels.',
             'WHY O(log n) · EACH LEVEL DOUBLES, SO THE PATH STAYS SHORT', 3)
    g = Geo(20, 400, 44, 44, None)
    t = .3
    for d in range(4):
        for i in range(2 ** d - 1, 2 ** (d + 1) - 1):
            x, y = g.p(i)
            f.show((g.edge(i) if i else '') + '<circle cx="%.1f" cy="%.1f" r="9" fill="var(--bg)" stroke="%s" stroke-width="1.3"/>' % (x, y, RULE_HI), t + (i - 2 ** d + 1) * .05)
        f.show(T(440, g.p(2 ** d - 1)[1] + 4, 'level %d · %d nodes' % (d + 1, 2 ** d), PT, 'start', mono=True), t)
        t += .9
    # one path from root to a leaf
    path = [0, 2, 5, 12]
    for k, i in enumerate(path):
        x, y = g.p(i)
        f.show('<circle cx="%.1f" cy="%.1f" r="9" fill="%s" stroke="%s" stroke-width="2.2"/>' % (x, y, vt('.18'), MID) + (g.edge(i, MID, 2.4).replace(str(NR), '9') if i else ''), t + k * .4)
    f.show(T(600, 130, '15 values', TX, 'start', mono=True, bold=True) + T(600, 150, '→ 4 levels', MID, 'start', mono=True, bold=True), t + 1.6)
    t += 2.6
    gx, gy, gw, gh = 60, 236, 560, 170
    NMAX, SMAX = 64, 8
    px = lambda n: gx + n / NMAX * gw; py = lambda s: gy + gh - s / SMAX * gh
    ax = L(gx, gy + gh, gx + gw + 10, gy + gh, MU, 1.2) + L(gx, gy + gh, gx, gy - 6, MU, 1.2)
    for n_ in (16, 32, 48, 64): ax += T(px(n_), gy + gh + 16, str(n_), FA, cls='sv-s', mono=True) + L(px(n_), gy + gh, px(n_), gy + gh + 4, MU, 1)
    for s_ in (2, 4, 6, 8): ax += T(gx - 8, py(s_) + 4, str(s_), FA, 'end', cls='sv-s', mono=True) + L(gx, py(s_), gx + gw, py(s_), 'var(--rule)', 1, '2 4')
    ax += T(gx + gw + 14, gy + gh + 4, 'n', MU, 'start', mono=True) + T(gx - 8, gy - 12, 'swaps per push / pop', MU, 'start', mono=True)
    f.show(ax, t)
    f.show('<path d="M%.1f %.1f L%.1f %.1f" fill="none" stroke="var(--ghost)" stroke-width="2"/>' % (px(0), py(0), px(SMAX), py(SMAX)) + T(px(SMAX) + 8, py(SMAX) + 12, 'O(n) · scan every value', MU, 'start'), t + .8)
    pts = [(n_, math.log2(n_ + 1)) for n_ in [i * .5 for i in range(129)]]
    d = 'M' + ' L'.join('%.1f %.1f' % (px(a_), py(b_)) for a_, b_ in pts)
    f.show('<path d="%s" fill="none" stroke="%s" stroke-width="2.6"/>' % (d, TG) + T(px(64) - 4, py(6) - 12, 'log₂ n levels', TG, 'end', bold=True), t + 1.8, d=.8)
    for k, n_ in enumerate((3, 7, 15, 31, 63)):
        f.show('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (px(n_), py(math.log2(n_ + 1)), MID), t + 2.4 + k * .25)
    f.show(T(px(15) + 8, py(4) + 18, '15 → 4', MID, 'start', mono=True, bold=True) + T(px(63) - 4, py(6) + 20, '63 → 6', MID, 'end', mono=True, bold=True), t + 3.8)
    f.show(T(gx + gw, gy + gh + 38, '✓ double n → one more level · n = 10⁶ → 20 swaps at most', TG, 'end', bold=True), t + 4.3)
    f.h = gy + gh + 50
    return f.render()
figs['p5'] = p5()

# ---------------------------------------------------------------- pattern helpers: heap state redrawn per step
def heap_state(f, g, arr, t0, t1, kinds=None, dt=0):
    kinds = kinds or {}
    for i, v in enumerate(arr):
        x, y = g.p(i)
        f.show((g.edge(i) if i else '') + node(x, y, v, kinds.get(i, 'n')), t0 + i * dt, hide=t1)
        if g.ay is not None: f.show(box(g.cx(i), g.ay, v, kinds.get(i, 'n')), t0 + i * dt, hide=t1)

# ---------------------------------------------------------------- q1 · top K with a min-heap of size K
def q1():
    a = [5, 1, 9, 3, 7, 2, 8]; k = 3
    LS = ['h = []', 'for x in a:', '    if len(h) < k: heappush(h, x)', '    elif x > h[0]: heapreplace(h, x)', 'return h[0]']
    code = Code2(0, 40, LS); X0 = code.w + 26
    AY = 66
    g = Geo(X0 + 40, 220, 200, 50, 296)
    f = Anim('hp-q1-', 760, 0, 'Keep the 3 largest of 5 1 9 3 7 2 8 in a min-heap of size 3. The first three are pushed. After that each value is compared with the root, the smallest of the three kept: 3 beats 1, 7 beats 3, 2 loses to 5, 8 beats 5. The root, 7, is the 3rd largest.',
             'TOP K · A MIN-HEAP OF SIZE K, THE ROOT IS THE ONE TO BEAT', 3)
    f.static(code.svg()); bar = Bar(code); tr = Track()
    cx = lambda i: X0 + i * (CW + G)
    for i, v in enumerate(a): f.show(box(cx(i), AY, v, sub=i), .2 + i * .05)
    f.show(T(X0, 180, 'heap · size ≤ 3', MU, 'start'), .7)
    f.show(chip(cx(len(a)) - G - 120, 24, 'k = 3 largest'), .9)
    STY = 380
    bar.at(1.2, 0)
    t = 2.0; h = []; prev = None; ip = None; states = []
    for i, x in enumerate(a):
        bar.at(t, 1)
        if ip is None: ip = tr.add(lambda x_, y_: ptr_up(cx(0) + CW / 2, AY + CH + 22, 'i'), (0, 0), t)
        else: tr.move(ip, (i * (CW + G), 0), t)
        t += .6
        if len(h) < k:
            bar.at(t, 2); heapq.heappush(h, x)
            say(f, X0, STY, 'size %d < 3 → push %d' % (len(h) - 1, x), t, hide=t + 1.2)
        else:
            bar.at(t, 3)
            rx, ry = g.p(0)
            f.show(nring(rx, ry) + ring(g.cx(0), g.ay), t, hide=t + 1.2)
            if x > h[0]:
                say(f, X0, STY, '%d > root %d → replace the root' % (x, h[0]), t, hide=t + 1.2)
                heapq.heapreplace(h, x)
            else:
                say(f, X0, STY, '%d ≤ root %d → skip' % (x, h[0]), t, hide=t + 1.2)
                f.show(box(cx(i), AY, x, 'g', sub=i), t + .6)
                t += 1.4; continue
        if prev is not None: prev[1] = t + .6
        prev = [t + .6, None, h[:]]
        states.append(prev)
        t += 1.4
    for t0, t1, arr in states: heap_state(f, g, arr, t0, t1)
    bar.at(t, 4); tr.kill(ip, t)
    tr.emit(f); bar.emit(f)
    rx, ry = g.p(0)
    f.show(node(rx, ry, h[0], 'f') + R(g.cx(0), g.ay, CW, CH, TG, TG, 6, 1.2) + T(g.cx(0) + CW / 2, g.ay + 23, str(h[0]), 'var(--on-fill)', mono=True, bold=True), t + .3)
    f.show(T(rx + NR + 8, ry + 5, '✓ 3rd largest', TG, 'start', mono=True, bold=True), t + .5)
    f.show(T(X0, STY, 'kept %s · answer = root = %d · O(n log k)' % (sorted(h), h[0]), TG, 'start', bold=True), t + .6)
    assert sorted(h) == [7, 8, 9]
    f.h = STY + 28
    return f.render()
figs['q1'] = q1()

# ---------------------------------------------------------------- q2 · merge k sorted lists
def q2():
    ls = [[1, 4, 9], [2, 3, 8], [5, 6]]
    LS = ['h = [(l[0], j, 0) for j, l in enumerate(ls)]', 'heapify(h)', 'while h:', '    v, j, p = heappop(h); out.append(v)',
          '    if p + 1 < len(ls[j]):', '        heappush(h, (ls[j][p + 1], j, p + 1))']
    code = Code2(0, 40, LS); X0 = code.w + 26
    f = Anim('hp-q2-', 800, 0, 'Three sorted lists 1 4 9, 2 3 8 and 5 6. The heap holds the front value of each list. Pop the smallest into the output, then push the next value from the same list. The output fills in order: 1 2 3 4 5 6 8 9.',
             'MERGE K SORTED LISTS · THE HEAP HOLDS ONE FRONT VALUE PER LIST', 3)
    f.static(code.svg()); bar = Bar(code); tr = Track()
    LY = [56, 100, 144]
    cx = lambda i: X0 + 30 + i * (CW + G)
    for j, l in enumerate(ls):
        f.show(T(X0, LY[j] + 23, 'L%d' % j, MU, 'start', mono=True), .2 + j * .2)
        for p, v in enumerate(l): f.show(box(cx(p), LY[j], v), .2 + j * .2 + p * .05)
    g = Geo(X0 + 230, 160, 74, 50, None)
    f.show(T(X0 + 230, 54, 'heap', MU, 'start'), .8)
    OY = 236
    f.show(T(X0, OY - 8, 'out', MU, 'start', mono=True), .9)
    ocx = lambda i: X0 + i * (CW + G)
    STY = 316
    bar.at(1.4, 0)
    h = [(l[0], j, 0) for j, l in enumerate(ls)]; heapq.heapify(h)
    t = 2.2; states = []; prev = None
    def snap(t):
        nonlocal prev
        if prev: prev[1] = t
        prev = [t, None, [e for e in h]]; states.append(prev)
    for j in range(3): f.show(ring(cx(0), LY[j]), t, hide=t + 1.0)
    bar.at(t + .5, 1)
    snap(t + .6)
    say(f, X0, STY, 'heap = the front of each list', t, hide=t + 1.2)
    t += 1.6; out = 0
    while h:
        bar.at(t, 2); bar.at(t + .3, 3)
        v, j, p = h[0]
        rx, ry = g.p(0)
        f.show(nring(rx, ry), t + .3, hide=t + 1.0)
        say(f, X0, STY, 'pop %d (from L%d) → out' % (v, j), t + .3, hide=t + 1.2)
        heapq.heappop(h)
        f.show(box(cx(p), LY[j], v, 'g'), t + .9)
        tr.add(lambda x_, y_, v=v: box(x_, y_, v, 't'), (ocx(out), OY), t + .9, frm=(rx - CW / 2, ry - CH / 2))
        out += 1
        snap(t + .9)
        if p + 1 < len(ls[j]):
            bar.at(t + 1.4, 4); bar.at(t + 1.7, 5)
            f.show(ring(cx(p + 1), LY[j]), t + 1.7, hide=t + 2.4)
            say(f, X0, STY, 'push next of L%d: %d' % (j, ls[j][p + 1]), t + 1.7, hide=t + 2.4)
            heapq.heappush(h, (ls[j][p + 1], j, p + 1)); snap(t + 2.2)
            t += 2.8
        else:
            bar.at(t + 1.4, 4)
            say(f, X0, STY, 'L%d is empty → nothing to push' % j, t + 1.4, hide=t + 2.2)
            t += 2.4
    for t0, t1, st in states:
        if st: heap_state(f, g, [e[0] for e in st], t0, t1)
    tr.emit(f); bar.emit(f)
    for i, v in enumerate(sorted(sum(ls, []))): f.show(box(ocx(i), OY, v, 'f'), t)
    f.show(T(X0, STY, '✓ merged in order · each value in and out of a heap of size k · O(n log k)', TG, 'start', bold=True), t + .2)
    f.h = STY + 28
    return f.render()
figs['q2'] = q2()

# ---------------------------------------------------------------- q3 · last stone weight (max-heap simulation)
def q3():
    s = [2, 7, 4, 1, 8, 1]
    LS = ['h = [-s for s in stones]; heapify(h)', 'while len(h) > 1:', '    y, x = -heappop(h), -heappop(h)', '    if y > x: heappush(h, -(y - x))', 'return -h[0] if h else 0']
    code = Code2(0, 40, LS); X0 = code.w + 26
    g = Geo(X0 + 10, 380, 60, 56, 246)
    f = Anim('hp-q3-', 760, 0, 'Stones 2 7 4 1 8 1 in a max-heap. Each round the two heaviest are popped and smashed; the difference goes back. 8 and 7 leave 1; 4 and 2 leave 2; 2 and 1 leave 1; 1 and 1 leave nothing. The last stone weighs 1.',
             'ALWAYS TAKE THE LARGEST · A MAX-HEAP RUNS THE SIMULATION', 3)
    f.static(code.svg()); bar = Bar(code)
    def mx(a):   # max-heap layout via negation
        h = [-v for v in a]; heapq.heapify(h); return [-v for v in h]
    h = [-v for v in s]; heapq.heapify(h)
    STY = 340
    say(f, X0, STY, 'max-heap: the heaviest stone is the root', 1.0, hide=2.4, mono=False, c=MU)
    bar.at(.6, 0)
    t = 0.2; states = []; cur = [t, None, [-v for v in h]]; states.append(cur)
    t = 2.6
    rnd = 0
    while len(h) > 1:
        bar.at(t, 1); bar.at(t + .3, 2)
        arr = [-v for v in h]
        # ring the two largest: root and its larger child
        y = arr[0]; c = max((i for i in (1, 2) if i < len(arr)), key=lambda i: arr[i])
        x = arr[c]
        for i in (0, c):
            px, py = g.p(i); f.show(nring(px, py) + ring(g.cx(i), g.ay), t + .3, hide=t + 1.4)
        y_ = -heapq.heappop(h); x_ = -heapq.heappop(h); assert (y_, x_) == (y, x)
        if y > x:
            bar.at(t + 1.0, 3); heapq.heappush(h, -(y - x))
            say(f, X0, STY, 'smash %d and %d → push %d - %d = %d' % (y, x, y, x, y - x), t + .3, hide=t + 2.2)
        else:
            say(f, X0, STY, 'smash %d and %d → equal, both gone' % (y, x), t + .3, hide=t + 2.2)
        cur[1] = t + 1.4; cur = [t + 1.5, None, [-v for v in h]]; states.append(cur)
        t += 2.6
    bar.at(t, 4)
    for t0, t1, arr in states: heap_state(f, g, arr, t0, t1, dt=.05 if t0 < 1 else 0)
    bar.emit(f)
    rx, ry = g.p(0)
    f.show(node(rx, ry, 1, 'f') + box(g.cx(0), g.ay, 1, 'f'), t + .3)
    f.show(T(rx + NR + 8, ry + 5, '✓ last stone', TG, 'start', mono=True, bold=True), t + .5)
    f.show(T(X0, STY, 'last stone = 1 · each round 2 pops + 1 push · O(n log n)', TG, 'start', bold=True), t + .6)
    f.h = STY + 28
    return f.render()
figs['q3'] = q3()

# ---------------------------------------------------------------- q4 · two heaps for the running median
def q4():
    stream = [5, 2, 8, 1, 9]
    LS = ['heappush(small, -x)', 'heappush(large, -heappop(small))', 'if len(large) > len(small):', '    heappush(small, -heappop(large))',
          'med = -small[0] if len(small) > len(large) \\', '      else (-small[0] + large[0]) / 2']
    code = Code2(0, 40, LS); X0 = code.w + 26
    W = 760; MIDX = X0 + (W - X0) / 2
    f = Anim('hp-q4-', W, 0, 'Running median of 5 2 8 1 9. A max-heap small keeps the smaller half, a min-heap large the larger half, sizes within one. Their tops meet at the middle line. Each new value goes into small, small passes its top to large, and large gives one back if it grew bigger. Medians: 5, 3.5, 5, 3.5, 5.',
             'RUNNING MEDIAN · TWO HEAPS MEET IN THE MIDDLE', 3)
    f.static(code.svg()); bar = Bar(code); tr = Track()
    AY = 60; cx = lambda i: X0 + i * (CW + G)
    for i, v in enumerate(stream): f.show(box(cx(i), AY, v, sub=i), .2 + i * .05)
    HY = 196
    f.show(L(MIDX, HY - 30, MIDX, HY + CH + 30, MID, 1.4, '4 3'), .8)
    f.show(T(MIDX - 8, HY - 14, 'small · max-heap · top →', MU, 'end') + T(MIDX + 8, HY - 14, '← top · min-heap · large', MU, 'start'), .8)
    STY = 312
    lo, hi = [], []
    def draw(t0, t1):
        L_ = sorted(-v for v in lo); Hh = sorted(hi)
        for k, v in enumerate(reversed(L_)):   # top next to the line
            f.show(box(MIDX - 8 - (k + 1) * (CW + G) + G, HY, v, 't' if k == 0 else 'n'), t0, hide=t1)
        for k, v in enumerate(Hh):
            f.show(box(MIDX + 8 + k * (CW + G), HY, v, 't' if k == 0 else 'n'), t0, hide=t1)
    t = 2.0; prev = None; ip = None; meds = []
    for i, x in enumerate(stream):
        if ip is None: ip = tr.add(lambda x_, y_: ptr_up(cx(0) + CW / 2, AY + CH + 22, 'i'), (0, 0), t)
        else: tr.move(ip, (i * (CW + G), 0), t)
        bar.at(t, 0); heapq.heappush(lo, -x)
        say(f, X0, STY, 'push %d into small' % x, t, hide=t + .9)
        if prev: draw(prev, t + .2)
        draw(t + .2, t + 1.0)
        bar.at(t + 1.0, 1); y = -heapq.heappop(lo); heapq.heappush(hi, y)
        say(f, X0, STY, 'small top %d → large' % y, t + 1.0, hide=t + 1.9)
        draw(t + 1.0, t + 1.9)
        t2 = t + 1.9
        bar.at(t2, 2)
        if len(hi) > len(lo):
            bar.at(t2 + .3, 3); z = heapq.heappop(hi); heapq.heappush(lo, -z)
            say(f, X0, STY, 'large is bigger → its top %d back to small' % z, t2 + .3, hide=t2 + 1.2)
            draw(t2 + .3, t2 + 1.2); t2 += 1.2
        else:
            say(f, X0, STY, 'sizes balanced', t2 + .2, hide=t2 + .9); t2 += .9
        bar.at(t2, 4)
        med = -lo[0] if len(lo) > len(hi) else (-lo[0] + hi[0]) / 2
        meds.append(med)
        # ring the tops
        f.show(ring(MIDX - 8 - CW, HY) + (ring(MIDX + 8, HY) if len(hi) == len(lo) else ''), t2, hide=t2 + 1.3)
        say(f, X0, STY, 'median = %s' % (('%d' % med) if med == int(med) else med), t2, hide=t2 + 1.3, c=MID)
        prev = t2
        t = t2 + 1.6
    draw(prev, None)
    tr.kill(ip, t); tr.emit(f); bar.emit(f)
    f.show(R(MIDX - 8 - CW, HY, CW, CH, TG, TG, 6, 1.2) + T(MIDX - 8 - CW / 2, HY + 23, str(-lo[0]), 'var(--on-fill)', mono=True, bold=True), t)
    f.show(T(MIDX - 8 - CW / 2, HY + CH + 18, '✓ median', TG, mono=True, bold=True), t + .2)
    f.show(T(X0, STY, 'medians %s · each new value O(log n), the median O(1)' % ', '.join(('%d' % m) if m == int(m) else str(m) for m in meds), TG, 'start', bold=True), t + .3)
    assert meds == [5, 3.5, 5, 3.5, 5], meds
    f.h = STY + 28
    return f.render()
figs['q4'] = q4()

# ---------------------------------------------------------------- q5 · Dijkstra
def q5():
    LS = ['dist = {s: 0}; h = [(0, s)]', 'while h:', '    d, u = heappop(h)', '    if d > dist[u]: continue', '    for v, w in g[u]:',
          '        if d + w < dist.get(v, inf):', '            dist[v] = d + w; heappush(h, (d + w, v))']
    code = Code2(0, 40, LS); X0 = code.w + 26
    W = 800
    f = Anim('hp-q5-', W, 0, 'Dijkstra from A on a weighted graph. The heap holds (distance, node) pairs. Pop the closest node, then try every edge out of it and push any shorter distance. A is settled at 0, C at 1, B at 3 through C, D at 4, E at 7. The old entry (4, B) pops later and is skipped as stale.',
             'DIJKSTRA · THE HEAP ALWAYS HANDS OUT THE CLOSEST NODE', 3)
    f.static(code.svg()); bar = Bar(code)
    P = {'A': (0, 1), 'B': (1, 0), 'C': (1, 2), 'D': (2, 1), 'E': (3, 1)}
    gx = lambda n: X0 + 24 + P[n][0] * 100; gy = lambda n: 70 + P[n][1] * 66
    E = [('A', 'B', 4), ('A', 'C', 1), ('C', 'B', 2), ('B', 'D', 1), ('C', 'D', 5), ('D', 'E', 3)]
    adj = {n: [] for n in P}
    for a, b, w in E: adj[a].append((b, w)); adj[b].append((a, w))
    def eline(a, b, c=RULE_HI, sw=1.4):
        x1, y1, x2, y2 = gx(a), gy(a), gx(b), gy(b); dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy)
        return L(x1 + dx / n * NR, y1 + dy / n * NR, x2 - dx / n * NR, y2 - dy / n * NR, c, sw)
    for a, b, w in E:
        f.show(eline(a, b) + R((gx(a) + gx(b)) / 2 - 8, (gy(a) + gy(b)) / 2 - 9, 16, 16, 'var(--page)', 'none', 3) + T((gx(a) + gx(b)) / 2, (gy(a) + gy(b)) / 2 + 4, str(w), MU, mono=True), .3)
    for n in P: f.show(node(gx(n), gy(n), n), .2)
    HY = 254
    f.show(T(X0, HY - 10, 'heap (dist, node) · smallest first', MU, 'start'), .8)
    STY = 330
    # dist labels with show/hide
    dl = {n: [] for n in P}
    def setd(n, v, t):
        if dl[n]: dl[n][-1][2] = t
        dl[n].append([v, t, None])
    for n in P: setd(n, '∞' if n != 'A' else '0', .6)
    bar.at(1.2, 0)
    h = [(0, 'A')]; dist = {'A': 0}; t = 2.0; settled = []
    hs = []; prev = None
    def snap(t):
        nonlocal prev
        if prev: prev[1] = t
        prev = [t, None, sorted(h)]; hs.append(prev)
    snap(1.4)
    while h:
        bar.at(t, 1); bar.at(t + .3, 2)
        d, u = heapq.heappop(h)
        f.show(ring(X0, HY), t + .3, hide=t + 1.0)
        f.show(nring(gx(u), gy(u)), t + .3, hide=t + 1.4)
        snap(t + 1.0)
        bar.at(t + .8, 3)
        if d > dist[u]:
            say(f, X0, STY, 'pop (%d, %s) · %d > dist[%s] = %d → stale, skip' % (d, u, d, u, dist[u]), t + .3, hide=t + 1.6)
            t += 2.0; continue
        say(f, X0, STY, 'pop (%d, %s) → %s is settled at %d' % (d, u, u, d), t + .3, hide=t + 1.4)
        f.show(node(gx(u), gy(u), u, 't'), t + 1.0); settled.append(u)
        t += 1.5
        for v, w in adj[u]:
            if v in settled: continue
            bar.at(t, 4); bar.at(t + .3, 5)
            f.show(eline(u, v, MID, 2.4), t, hide=t + 1.0)
            better = d + w < dist.get(v, math.inf)
            say(f, X0, STY, '%d + %d = %d %s %s → %s' % (d, w, d + w, '<' if better else '≥', dist.get(v, '∞'), 'push (%d, %s)' % (d + w, v) if better else 'no change'), t + .3, hide=t + 1.0)
            if better:
                bar.at(t + .6, 6); dist[v] = d + w; heapq.heappush(h, (d + w, v)); setd(v, str(d + w), t + .7); snap(t + .7)
            t += 1.2
    bar.at(t, 1)
    for t0, t1, st in hs:
        for k, (d, n) in enumerate(st):
            f.show(box(X0 + k * 58, HY, '%d·%s' % (d, n), w=52), t0, hide=t1)
    for n, lst in dl.items():
        for v, t0, t1 in lst:
            f.show(T(gx(n), gy(n) - NR - 6, v, PT, mono=True, bold=True), t0, hide=t1)
    bar.emit(f)
    for n in P: f.show(node(gx(n), gy(n), n, 'f'), t + (.1 if n == 'E' else 0))
    f.show(T(X0, STY, '✓ dist A 0 · B 3 · C 1 · D 4 · E 7 · O((V + E) log V)', TG, 'start', bold=True), t + .3)
    assert dist == {'A': 0, 'B': 3, 'C': 1, 'D': 4, 'E': 7}, dist
    f.h = STY + 28
    return f.render()
figs['q5'] = q5()

os.makedirs('/tmp/dsa', exist_ok=True)
json.dump(figs, open('/tmp/dsa/heap-priority-queue.json', 'w'))
print('figures:', list(figs))
