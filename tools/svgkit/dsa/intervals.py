"""Intervals lesson figures: bars on a number line; sort, then merge / sweep.
Writes /tmp/dsa/intervals.json. Builds on engine.py + arrkit.py."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arrkit import *  # noqa

BH = 26
class Line:
    """number line: x = x0 + v * u; bars on rows from y0, row pitch p."""
    def __init__(s, x0, u, y0, p=36): s.x0, s.u, s.y0, s.p = x0, u, y0, p
    def x(s, v): return s.x0 + v * s.u
    def y(s, r): return s.y0 + r * s.p
    def bar(s, a, b, r, kind='n', lbl=True):
        return box(s.x(a), s.y(r), '[%d,%d]' % (a, b) if lbl else '', kind, max(s.u * (b - a), 6), BH)
    def ring(s, a, b, r): return ring(s.x(a), s.y(r), max(s.u * (b - a), 6), BH)
    def axis(s, lo, hi, y, step=1):
        o = L(s.x(lo), y, s.x(hi), y, MU, 1.2)
        for v in range(lo, hi + 1, step):
            o += L(s.x(v), y, s.x(v), y + 4, MU, 1) + idx(s.x(v), y + 17, v)
        return o
    def cursor(s, v, top, bot, name, c=PT):
        return L(s.x(v), top, s.x(v), bot, c, 1.6, '4 3') + T(s.x(v), top - 6, name, c, mono=True, bold=True)

figs = {}

# ---------- m1: sort, then only neighbours matter
f = Anim('iv-m1-', 760, 300, 'Four intervals drawn as bars in input order: [8,10], [1,3], [15,18], [2,6]. They slide into order by start: [1,3], [2,6], [8,10], [15,18]. Then each bar is compared only with the one above it: [2,6] starts at 2, before 3, so it touches; [8,10] starts after 6; [15,18] starts after 10. Three checks for four bars.', 'SORT BY START · THEN COMPARE WITH THE PREVIOUS BAR ONLY', 2.5)
ln = Line(40, 34, 40, 38)
iv = [(8, 10), (1, 3), (15, 18), (2, 6)]
order = sorted(range(4), key=lambda k: iv[k])
f.static(ln.axis(0, 19, ln.y(4) + 4, 1))
f.show(st(0, 260, 'input order: bars jump around'), 1.0, hide=2.0)
t = 2.2
for k, (a, b) in enumerate(iv):
    r = order.index(k)
    f.path(ln.bar(a, b, k), [(0, 0, 0), (t, 0, (r - k) * ln.p)], .2 + k * .15)
f.show(st(0, 260, 'a.sort()  →  by start: 1, 2, 8, 15', MID), t, hide=t + 1.6)
srt = sorted(iv)
t += 1.8
for k in range(1, 4):
    (pa, pb), (a, b) = srt[k - 1], srt[k]
    over = a <= pb
    f.show(ln.ring(a, b, k), t, hide=t + 1.6)
    f.show(L(ln.x(pb), ln.y(k - 1) + BH, ln.x(pb), ln.y(k) + BH, MID, 1.4, '3 3'), t, hide=t + 1.6)
    f.show(st(0, 260, 'start %d %s end %d of previous → %s' % (a, '≤' if over else '>', pb, 'they overlap' if over else 'no overlap'), MID), t, hide=t + 1.6)
    t += 1.8
for k, (a, b) in enumerate(srt): f.show(ln.bar(a, b, k, 'b'), t)
f.show(st(0, 260, '✓ 3 checks for 4 bars · sorting made the neighbours the only candidates', TG, True), t + .2)
figs['m1'] = f.render()

# ---------- m2: cost, all pairs vs neighbours
f = Anim('iv-m2-', 760, 330, 'Without sorting, six intervals need every pair compared: 15 checks, n squared over two. After sorting only the 5 neighbour pairs are checked. A graph then shows n squared over two climbing far above n log n, the cost of the sort.', 'COST · EVERY PAIR vs. SORT + NEIGHBOURS', 3)
xs = [30 + k * 44 for k in range(6)]
def node(k, kind='n'): return box(xs[k] - 16, 40, str(k), kind, 32, 28)
for k in range(6): f.show(node(k), .2 + k * .06)
t = 1.0; c = 0
for a_ in range(6):
    for b_ in range(a_ + 1, 6):
        c += 1
        h = 14 + (b_ - a_) * 9
        mx = (xs[a_] + xs[b_]) / 2
        f.show('<path d="M%.1f 72 Q%.1f %.1f %.1f 72" fill="none" stroke="%s" stroke-width="1.3"/>' % (xs[a_], mx, 72 + 2 * h, xs[b_], MID), t, hide=6.0)
        f.show(st(0, 160, 'no sort: pair %d of 15' % c, MID), t, hide=t + .18 if c < 15 else 6.0)
        t += .22
f.show(st(0, 182, 'every pair → n(n−1)/2 = 15 checks', MU), t, hide=6.0)
t = 6.2
f.show(st(0, 160, 'sorted: only neighbours → n − 1 = 5 checks', TG, True), t)
for k in range(5):
    f.show('<path d="M%.1f 72 Q%.1f 90 %.1f 72" fill="none" stroke="%s" stroke-width="1.8"/>' % (xs[k], xs[k] + 22, xs[k + 1], TG), t + .2 + k * .2)
gx, gy, gw, gh = 380, 40, 300, 200
NM, SM = 32, 500
px = lambda n: gx + n / NM * gw; py = lambda v: gy + gh - min(v, SM) / SM * gh
t += 1.6
f.show(axes(gx, gy, gw, gh, [8, 16, 24, 32], [100, 200, 300, 400, 500], 'n', 'checks', px, py), t)
import math
sq = [(n, n * (n - 1) / 2) for n in [x / 2 for x in range(2, 65)] if n * (n - 1) / 2 <= SM]
nl = [(n, n * math.log2(n)) for n in [x / 2 for x in range(2, 65)]]
f.show(poly([(px(a), py(b)) for a, b in sq], 'var(--ghost)', 2) + lab(px(sq[-1][0]) - 10, py(sq[-1][1]) + 4, 'n²/2 every pair', MU, 'end'), t + .6)
f.show(poly([(px(a), py(b)) for a, b in nl], TG, 2.6) + lab(px(32) - 4, py(160) - 10, 'n log n sort', TG, 'end', True), t + 1.4)
for k, n in enumerate((8, 16, 32)): f.show(dot(px(n), py(n * math.log2(n))), t + 2.0 + k * .25)
f.show(lab(gx + gw, gy + gh + 40, 'n = 32: 496 pair checks vs 160 for the sort', TG, 'end', True), t + 2.8)
figs['m2'] = f.render()

# ---------- p1: merge with code
L1 = ['a.sort()', 'res = []', 'for s, e in a:', '  if res and s <= res[-1][1]:', '    res[-1][1] = max(res[-1][1], e)', '  else:', '    res.append([s, e])']
code = Code2(0, 40, L1, 290)
f = Anim('iv-p1-', 820, 0, 'Sorted intervals [1,3], [2,6], [8,10], [9,12], [15,18]. Each bar is ringed in turn. [1,3] starts the result. [2,6] starts at 2, before the last end 3, so the last result grows to [1,6]. [8,10] starts after 6 and is appended. [9,12] overlaps, so the result becomes [8,12]. [15,18] is appended. Final: three merged bars.', 'MERGE · GROW THE LAST RESULT OR START A NEW ONE', 3)
f.static(code.svg())
ln = Line(320, 26, 40, 34)
iv = [(1, 3), (2, 6), (8, 10), (9, 12), (15, 18)]
RY = 5
for k, (a, b) in enumerate(iv): f.show(ln.bar(a, b, k), .2 + k * .1)
f.static(lab(ln.x(0) - 8, ln.y(RY) + 18, 'res', PT, 'end', True) + ln.axis(0, 18, ln.y(RY) + BH + 8, 2))
SY = max(code.y + code.h(), ln.y(RY) + BH + 30) + 22
code.at(.8, 0); code.at(1.4, 1)
t = 2.2; res = []; hist = []   # hist[r] = list of (t, svg)
for k, (a, b) in enumerate(iv):
    code.at(t, 2)
    f.show(ln.ring(a, b, k), t, hide=t + 2.6)
    code.at(t + .8, 3)
    if res and a <= res[-1][1]:
        f.show(st(0, SY, 'start %d ≤ last end %d → overlap' % (a, res[-1][1]), MID), t + .8, hide=t + 2.6)
        code.at(t + 1.6, 4)
        ra, rb = res[-1]; nb = max(rb, b)
        f.show(st(0, SY + 22, 'end = max(%d, %d) = %d' % (rb, b, nb), PT, True), t + 1.6, hide=t + 2.6)
        res[-1] = [ra, nb]; hist[-1].append((t + 2.0, ln.bar(ra, nb, RY, 'b')))
    else:
        f.show(st(0, SY, ('start %d > last end %d → new result' % (a, res[-1][1])) if res else 'res is empty → new result', MID), t + .8, hide=t + 2.6)
        code.at(t + 1.6, 5); code.at(t + 2.0, 6)
        res.append([a, b]); hist.append([(t + 2.0, ln.bar(a, b, RY, 'b'))])
    f.show(ln.bar(a, b, k, 'g'), t + 2.4)
    t += 3.0
code.emit(f)
for hs in hist: states(f, hs, end=t + .1)
for a, b in res: f.show(ln.bar(a, b, RY, 'f'), t + .1)
f.show(st(0, SY, '✓ 5 intervals → 3 merged: ' + ' '.join('[%d,%d]' % tuple(r) for r in res), TG, True), t + .3)
f.h = SY + 34
figs['p1'] = f.render()

# ---------- p2: keep the most, sort by end
L2 = ['a.sort(key=lambda x: x[1])', 'cnt, end = 0, -inf', 'for s, e in a:', '  if s >= end:', '    cnt += 1; end = e']
code = Code2(0, 40, L2, 260)
f = Anim('iv-p2-', 820, 0, 'Intervals sorted by end: [1,3], [2,4], [3,5], [1,8], [6,9]. Keep [1,3], end = 3. [2,4] starts at 2 before 3: dropped. [3,5] starts at 3: kept, end = 5. [1,8] starts before 5: dropped. [6,9] kept. Three kept, two removed.', 'KEEP THE MOST · SORT BY END, TAKE WHAT FITS', 3)
f.static(code.svg())
ln = Line(290, 30, 40, 34)
iv = [(1, 3), (2, 4), (3, 5), (1, 8), (6, 9)]
for k, (a, b) in enumerate(iv): f.show(ln.bar(a, b, k), .2 + k * .1)
AY = ln.y(5) + 4
f.static(ln.axis(0, 10, AY, 1))
SY = max(code.y + code.h(), AY + 30) + 22
code.at(.8, 0); code.at(1.4, 1)
end = None; t = 2.2; cnt = 0; cur_pts = []; kept = []
for k, (a, b) in enumerate(iv):
    code.at(t, 2); code.at(t + .7, 3)
    f.show(ln.ring(a, b, k), t, hide=t + 2.4)
    ok = end is None or a >= end
    f.show(st(0, SY, 'start %d ≥ end %s → keep' % (a, '-inf' if end is None else end) if ok else 'start %d < end %d → overlap, drop' % (a, end), MID), t + .7, hide=t + 2.4)
    if ok:
        code.at(t + 1.4, 4); cnt += 1; kept.append(k)
        f.show(ln.bar(a, b, k, 'b'), t + 1.5)
        if end is None: cur_pts = [(0, ln.x(b) - ln.x(0), 0)]; t_end0 = t + 1.5
        else: cur_pts.append((t + 1.5, ln.x(b) - ln.x(0), 0))
        end = b
        f.show(st(0, SY + 22, 'cnt = %d · end = %d' % (cnt, end), PT, True), t + 1.5, hide=t + 2.4)
    else:
        f.show(ln.bar(a, b, k, 'g'), t + 1.5)
    t += 2.7
code.emit(f)
f.path(ln.cursor(0, ln.y(0) - 4, AY, 'end'), cur_pts, t_end0, d=.5, hide=t)
for k in kept: f.show(ln.bar(*iv[k], k, 'f'), t + .1)
f.show(st(0, SY, '✓ kept %d, removed %d · an early end leaves the most room' % (cnt, len(iv) - cnt), TG, True), t + .3)
f.h = SY + 34
figs['p2'] = f.render()

# ---------- p3: sweep line, meeting rooms
f = Anim('iv-p3-', 760, 0, 'Meetings [0,30], [5,10], [15,20], [5,25] become events: +1 at each start, -1 at each end. A cursor sweeps left to right; the running count goes 1, 3, 2, 3, 2, 1, 0. The peak 3 is the number of rooms needed.', 'SWEEP LINE · +1 AT A START, −1 AT AN END', 3)
ln = Line(60, 21, 40, 34)
iv = [(0, 30), (5, 10), (15, 20), (5, 25)]
for k, (a, b) in enumerate(iv): f.show(ln.bar(a, b, k), .2 + k * .1)
AY = ln.y(4) + 4
f.static(ln.axis(0, 30, AY, 5))
EY = AY + 44
ev = sorted([(a, 1) for a, b in iv] + [(b, -1) for a, b in iv])
t = 1.2
f.show(lab(0, EY + 4, 'events', MU), t)
for k, (x, d) in enumerate(ev):
    f.show(T(ln.x(x) + (k % 2) * 0, EY + (12 if d < 0 else -4) , '+1' if d > 0 else '−1', PT if d > 0 else MU, mono=True, bold=True), t + .2 + k * .12)
SY = EY + 50
t = 3.0; cur = best = 0; pts = []; bx = None
groups = []
for x, d in ev:
    if groups and groups[-1][0] == x: groups[-1][1] += d
    else: groups.append([x, d])
for x, d in groups:
    cur += d
    if not pts: pts = [(0, 0, 0)]; t0 = t
    else: pts.append((t, ln.x(x) - ln.x(groups[0][0]), 0))
    f.show(st(0, SY, 'time %d: count %+d → %d' % (x, d, cur), MID), t + .4, hide=t + 1.5)
    if cur > best:
        best = cur; bx = x
        f.show(st(0, SY + 22, 'peak so far = %d' % best, PT, True), t + .4, hide=t + 1.5)
    t += 1.6
f.path(ln.cursor(groups[0][0], ln.y(0) - 4, AY, 'x', MID), pts, t0, d=.5, hide=t)
f.show(L(ln.x(bx), ln.y(0) - 4, ln.x(bx), AY, TG, 2), t + .1)
for k, (a, b) in enumerate(iv):
    if a <= bx < b: f.show(ln.bar(a, b, k, 'f'), t + .1)
f.show(st(0, SY, '✓ peak %d at time %d → %d rooms needed' % (best, bx, best), TG, True), t + .3)
f.h = SY + 34
figs['p3'] = f.render()

# ---------- p4: two lists, two pointers
f = Anim('iv-p4-', 760, 0, 'List A [0,2], [5,10], [13,23] and list B [1,5], [8,12], [15,24]. Pointer i walks A, j walks B. At each step the overlap is max of starts to min of ends; the bar that ends first is advanced. Intersections: [1,2], [5,5], [8,10], [15,23].', 'TWO LISTS · OVERLAP = [max start, min end], ADVANCE THE ONE THAT ENDS FIRST', 3)
ln = Line(60, 25, 50, 44)
A = [(0, 2), (5, 10), (13, 23)]; B = [(1, 5), (8, 12), (15, 24)]
f.static(lab(0, ln.y(0) + 18, 'A', MU, bold=True) + lab(0, ln.y(1) + 18, 'B', MU, bold=True) + lab(0, ln.y(2) + 18, 'out', PT, bold=True))
for k, (a, b) in enumerate(A): f.show(ln.bar(a, b, 0), .2 + k * .1)
for k, (a, b) in enumerate(B): f.show(ln.bar(a, b, 1), .5 + k * .1)
AY = ln.y(3) - 6
f.static(ln.axis(0, 24, AY, 2))
SY = AY + 46
i = j = 0; t = 1.8; ipts = []; jpts = []; out = []
while i < len(A) and j < len(B):
    (a1, b1), (a2, b2) = A[i], B[j]
    f.show(ln.ring(a1, b1, 0) + ln.ring(a2, b2, 1), t, hide=t + 2.2)
    lo_, hi_ = max(a1, a2), min(b1, b2)
    f.show(st(0, SY, 'max(%d,%d) = %d · min(%d,%d) = %d → %s' % (a1, a2, lo_, b1, b2, hi_, '[%d,%d]' % (lo_, hi_) if lo_ <= hi_ else 'no overlap'), MID), t + .5, hide=t + 2.2)
    if lo_ <= hi_: out.append((lo_, hi_)); f.show(ln.bar(lo_, hi_, 2, 'b', hi_ - lo_ >= 2), t + 1.0)
    if b1 < b2:
        f.show(st(0, SY + 22, 'A ends first → i += 1', PT, True), t + 1.3, hide=t + 2.2); f.show(ln.bar(a1, b1, 0, 'g'), t + 1.6); i += 1
    else:
        f.show(st(0, SY + 22, 'B ends first → j += 1', PT, True), t + 1.3, hide=t + 2.2); f.show(ln.bar(a2, b2, 1, 'g'), t + 1.6); j += 1
    t += 2.4
for a, b in out:
    f.show(ln.bar(a, b, 2, 'f', b - a >= 2) + ('' if b - a >= 2 else T(ln.x((a + b) / 2), ln.y(2) - 6, '[%d,%d]' % (a, b), TG, mono=True, bold=True)), t + .1)
f.show(st(0, SY, '✓ ' + ' '.join('[%d,%d]' % o for o in out) + ' · one pass, O(n + m)', TG, True), t + .3)
f.h = SY + 34
figs['p4'] = f.render()

json.dump(figs, open('/tmp/dsa/intervals.json', 'w'))
print(list(figs))
