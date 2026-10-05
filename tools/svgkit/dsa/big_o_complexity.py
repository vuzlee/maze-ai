"""Figures for content/01-dsa/02-foundations/big-o-complexity. Writes /tmp/dsa/big-o-complexity.json and splices the page.
Measured numbers (µs, CPython 3.12) come from the previous version of the lesson (git HEAD)."""
import sys, os, json, re, math, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graph_bigo_kit import *
figs = {}

def draw_curve(S, pts, t, c, sw=2.4, dur=1.4, dash=None):
    """Draw a polyline piece by piece so it visibly grows left to right."""
    n = len(pts) - 1; k = max(1, n // 24)
    segs = [pts[i:i + k + 1] for i in range(0, n, k)]
    d_ = ' stroke-dasharray="%s"' % dash if dash else ''
    for m, sg in enumerate(segs):
        d = 'M' + ' L'.join('%.1f %.1f' % p for p in sg)
        S.at(t + m * dur / len(segs), '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"%s/>' % (d, c, sw, d_), d=.08)

def axes(gx, gy, gw, gh, xt, yt, xl, yl, px, py):
    s = L(gx, gy + gh, gx + gw + 8, gy + gh, MU, 1.2) + L(gx, gy + gh, gx, gy - 8, MU, 1.2)
    for v, lab in xt: s += L(px(v), gy + gh, px(v), gy + gh + 4, MU, 1) + T(px(v), gy + gh + 17, lab, FA, cls='sv-s', mono=True)
    for v, lab in yt: s += L(gx, py(v), gx + gw, py(v), 'var(--rule)', 1, '2 4') + T(gx - 7, py(v) + 4, lab, FA, 'end', cls='sv-s', mono=True)
    s += T(gx + gw + 8, gy + gh + 32, xl + ' →', MU, 'end', mono=True) + T(gx + 6, gy - 4, yl, MU, 'start', mono=True)
    return s

# ---------- 1.1 growth curves ----------
def growth():
    S = Story('bm1-', 720, 'Graph of operations against n from 0 to 20. Curves draw one after another: log n stays near the floor, n is a straight line, n log n bends up, n squared shoots up, and 2 to the n leaves the chart at n = 9. At n = 20 the ring reads off: log n 4, n 20, n log n 86, n squared 400, 2 to the n about a million.',
              'GROWTH · HOW THE WORK GROWS AS n GROWS')
    gx, gy, gw, gh = 50, 40, 430, 240; NM, YM = 20, 420
    px = lambda n: gx + n / NM * gw; py = lambda v: gy + gh - min(v, YM) / YM * gh
    S.at(.2, axes(gx, gy, gw, gh, [(v, str(v)) for v in (0, 5, 10, 15, 20)], [(v, str(v)) for v in (100, 200, 300, 400)], 'n', 'operations', px, py))
    fs = [('log n', lambda n: math.log2(n) if n >= 1 else 0, GH, 1.0),
          ('n', lambda n: n, it('.55'), 1.0),
          ('n log n', lambda n: n * math.log2(n) if n >= 1 else 0, PT, 1.0),
          ('n²', lambda n: n * n, MID, 1.0),
          ('2ⁿ', lambda n: 2 ** n, TG, 1.0)]
    t = 1.0
    RX = 540
    S.sx, S.sy = RX, 120
    S.static(T(RX, 70, 'at n = 20', MU, 'start'))
    for k, (nm, f, c, _) in enumerate(fs):
        top = NM
        if nm == '2ⁿ': top = math.log2(YM)
        pts = [(px(n), py(f(n))) for n in [i * top / 48 for i in range(49)]]
        if nm == '2ⁿ': pts.append((px(top), gy - 2))
        draw_curve(S, pts, t, c, 2.6 if k >= 2 else 2.2, 1.2)
        LP = {'log n': (px(20) + 6, py(math.log2(20)) + 4), 'n': (px(13), py(13) - 9), 'n log n': (px(14) - 30, py(14 * math.log2(14)) - 10),
              'n²': (px(17) - 34, py(17 * 17)), '2ⁿ': (px(top) + 8, gy + 6)}
        lab = T(LP[nm][0], LP[nm][1], nm, c, 'start', mono=True, bold=True)
        S.at(t + 1.2, lab)
        v = f(20)
        S.at(t + 1.4, T(RX, 96 + k * 26, nm, c, 'start', mono=True, bold=True) + T(RX + 160, 96 + k * 26, '{:,}'.format(round(v)), c, 'end', mono=True, bold=True))
        t += 2.0
    S.at(t + .2, T(RX, 96 + 5 * 26 + 10, 'same n = 20,', TG, 'start', bold=True) + T(RX, 96 + 5 * 26 + 28, 'a million times apart', TG, 'start', bold=True))
    S.at(t + .6, T(gx + gw, gy + gh + 40, 'Big-O names the curve, not the seconds', TG, 'end', bold=True))
    return S.render(gy + gh + 50)
figs['m1'] = growth()

# ---------- 1.2 constants: the crossover ----------
def crossover():
    data = [(8, 1.2, 4.5), (32, 10.2, 24.3), (64, 43.5, 52.8), (80, 72.3, 66.5), (128, 177, 115)]
    S = Story('bm2-', 740, 'Measured time to sort n numbers in Python: insertion sort, O(n squared), against merge sort, O(n log n). At n = 8, 32 and 64 insertion sort is faster. The lines cross near n = 80 and from there merge sort wins for good: at n = 1,000 it is 11 times faster, at 4,000 41 times.',
              'MEASURED · INSERTION SORT O(n²) vs MERGE SORT O(n log n)')
    gx, gy, gw, gh = 50, 40, 380, 220; NM, YM = 140, 200
    px = lambda n: gx + n / NM * gw; py = lambda v: gy + gh - v / YM * gh
    S.at(.2, axes(gx, gy, gw, gh, [(v, str(v)) for v in (0, 32, 64, 96, 128)], [(v, str(v)) for v in (50, 100, 150, 200)], 'n', 'µs', px, py))
    S.static(T(gx + 40, gy + 22, '● O(n²) insertion', MID, 'start', mono=True, bold=True) + T(gx + 40, gy + 40, '● O(n log n) merge', PT, 'start', mono=True, bold=True))
    RX = 470; S.sx, S.sy = RX, 100
    t = 1.2; prev = None
    for k, (n, a, b) in enumerate(data):
        S.at(t, L(px(n), gy + gh, px(n), gy, vt('.35'), 1, '3 3'), hide=t + 1.6)
        S.at(t + .3, circ(px(n), py(a), 4.5, MID) + circ(px(n), py(b), 4.5, PT))
        if prev:
            S.at(t + .5, L(px(prev[0]), py(prev[1]), px(n), py(a), MID, 2.2) + L(px(prev[0]), py(prev[2]), px(n), py(b), PT, 2.2))
        w = 'insertion faster' if a < b else 'merge faster'
        S.say(t + .3, 'n = %d: %g µs vs %g µs' % (n, a, b), 0, TX)
        S.say(t + .3, '→ %s' % w, 1, MID if a < b else PT, True)
        prev = (n, a, b); t += 1.8
    S.at(t, R(px(80) - 12, py(70) - 12, 24, 24, 'none', TG, 12, 1.6) + T(px(80) + 16, py(70) + 22, 'cross ≈ 80', TG, 'start', mono=True, bold=True))
    S.say(t + .3, 'n = 1,000 → merge 11× faster', 0, TG, True)
    S.say(t + .3, 'n = 4,000 → merge 41× faster', 1, TG, True)
    S.at(t + .8, T(RX, S.sy + 60, 'lower order wins for every', MU, 'start') + T(RX, S.sy + 78, 'n past the cross, forever', MU, 'start'))
    return S.render(gy + gh + 40)
figs['m2'] = crossover()

# ---------- 2.1 lookup table: which order fits n = 1e5 ----------
def lookup():
    rows = [('n!', '≤ 12', lambda n: math.factorial(int(n)) if n < 30 else 1e300, 'every permutation'),
            ('2ⁿ', '≤ 20', lambda n: 2 ** n if n < 1000 else 1e300, 'every subset'),
            ('n³', '≤ 500', lambda n: n ** 3, 'triple loop, Floyd'),
            ('n²', '≤ 5,000', lambda n: n ** 2, 'double loop, 2-D DP'),
            ('n log n', '≤ 10⁶', lambda n: n * math.log2(n), 'sort, heap, binary search'),
            ('n', '≤ 10⁷', lambda n: n, 'one pass, two pointers'),
            ('log n', '≥ 10⁹', lambda n: math.log2(n), 'binary search on the answer')]
    n = 10 ** 5; BUD = 1e8
    S = Story('bp1-', 720, 'Lookup table: seven orders, the largest n each allows, and what it usually means. Goal: the problem says n up to 10 to the 5. Ring walks down the rows computing the work at n = 10 to the 5 against a budget of 10 to the 8 per second. n factorial, 2 to the n, n cubed and n squared exceed the budget and grey out. n log n gives 1.7 million: it fits, and is the answer.',
              'LOOKUP TABLE · BUDGET ≈ 10⁸ SIMPLE STEPS PER SECOND')
    X0, Y0, RH = 0, 70, 32
    cols = [(0, 'order', 80), (84, 'n allowed', 90), (178, 'usually', 220), (410, 'work at n = 100,000', 200)]
    S.static(''.join(T(X0 + x + 8, Y0 - 10, h, MU, 'start') for x, h, w in cols) + L(X0, Y0 - 4, 640, Y0 - 4, 'var(--rule-hi)', 1))
    def row(k, st):
        nm, lim, f, use = rows[k]; y = Y0 + k * RH
        fill, tc = {'plain': ('var(--bg)', TX), 'grey': ('var(--sunk)', GH), 'ans': (TG, 'var(--on-fill)'), 'seen': (it('.14'), TG)}[st]
        return R(X0, y, 400, RH - 6, fill, 'var(--rule)' if st == 'grey' else (TG if st in ('ans', 'seen') else RULE_HI), 6, 1.2) + \
            T(X0 + 8, y + 17, nm, tc, 'start', mono=True, bold=True) + T(X0 + 92, y + 17, lim, tc, 'start', mono=True) + T(X0 + 186, y + 17, use, tc if st != 'plain' else MU, 'start')
    for k in range(len(rows)): S.at(.2 + k * .12, row(k, 'plain'), key='r%d' % k)
    S.at(1.4, chip(470, 0, 'n = 10⁵ → which?', a='start'))
    S.sx, S.sy = X0, Y0 + 7 * RH + 24
    t = 2.6; rp = []; ans = None
    def fmt(v):
        if v > 1e15: return '> 10¹⁵'
        e = int(math.floor(math.log10(v))); m = v / 10 ** e
        return '%.1f × 10%s' % (m, ''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(c)] for c in str(e))) if e >= 3 else '%d' % round(v)
    for k, (nm, lim, f, use) in enumerate(rows):
        y = Y0 + k * RH
        if not rp: rp = [(0, 0, 0)]; rt0 = t
        else: rp.append((t, 0, k * RH))
        v = f(n); ok = v <= BUD
        S.at(t + .3, T(X0 + 418, y + 17, fmt(v), TX if ok else GH, 'start', mono=True, bold=ok))
        S.say(t + .3, '%s at n = 10⁵ = %s %s 10⁸ → %s' % (nm, fmt(v), '≤' if ok else '>', 'fits' if ok else 'too slow'), 0, TX if ok else MU)
        if not ok:
            S.at(t + .8, row(k, 'grey'), key='r%d' % k); t += 1.4
        else:
            ans = k; break
    S.path(R(X0 - 3, Y0 - 3, 406, RH, 'none', MID, 8, 2.2), rp, rt0, hide=t + .8, d=.35)
    assert ans == 4
    S.at(t + .8, row(4, 'ans'), key='r4')
    S.at(t + 1.0, T(X0 + 418 + 100, Y0 + 4 * RH + 17, '✓ fits', TG, 'start', mono=True, bold=True))
    S.say(t + 1.2, 'n ≤ 10⁵ → aim for O(n log n) · pure Python ≈ 5 × 10⁷ steps/s', 0, TG, True)
    return S.render(S.sy + 12)
figs['p1'] = lookup()

# ---------- 2.2 amortized append ----------
def amortized():
    N = 16
    S = Story('bp2-', 740, 'A Python list appends 16 values. Capacity starts at 1 and doubles when full: 1, 2, 4, 8, 16. A normal append costs 1; an append that finds the list full copies everything first, costing 2, 3, 5 and 9. Bars show the cost of each append. Total 31 for 16 appends, under 2 per append: amortized O(1).',
              'AMORTIZED · APPEND INTO A LIST THAT DOUBLES WHEN FULL')
    X0, Y0, CW = 0, 52, 36
    cx = lambda i: X0 + i * (CW + 4)
    S.static(T(X0, Y0 - 10, 'memory (capacity doubles: 1, 2, 4, 8, 16)', MU, 'start'))
    BY = Y0 + 160; BH = 10   # bar chart baseline and unit height
    S.static(L(X0, BY, X0 + N * (CW + 4), BY, MU, 1.2) + T(X0, BY - 100, 'cost of each append', MU, 'start'))
    S.sx, S.sy = X0, BY + 46
    cap = 0; t = .8; total = 0
    def slots(c, tt):
        S.at(tt, ''.join(R(cx(i), Y0, CW, 32, 'var(--bg)', RULE_HI, 5, 1) for i in range(c)), key='cap')
    for i in range(N):
        cost = 1
        if i == cap:
            newc = max(1, cap * 2)
            if cap:
                g = ''.join(bring(cx(j), Y0, CW, 32) for j in range(cap))
                S.at(t, g, hide=t + .9)
                S.say(t, 'full at %d → new block of %d, copy %d' % (cap, newc, cap), 0, MID)
                cost += cap
            slots(newc, t + .5)
            # re-draw existing values on top of the new block
            S.at(t + .5, ''.join(box(cx(j), Y0, j + 1, 'plain', CW, 32, True) for j in range(i)), key='vals')
            cap = newc; t += 1.1 if cost > 1 else .6
        S.at(t, box(cx(i), Y0, i + 1, 'seen', CW, 32, True), hide=t + .5)
        S.at(t + .4, ''.join(box(cx(j), Y0, j + 1, 'plain', CW, 32, True) for j in range(i + 1)), key='vals')
        if cost == 1: S.say(t, 'append %d → free slot, cost 1' % (i + 1), 0, TX)
        total += cost
        hb = cost * BH
        S.at(t + .2, R(cx(i) + 8, BY - hb, CW - 16, hb, TG if cost > 1 else it('.35'), 'none', 2) + (T(cx(i) + CW / 2, BY - hb - 5, str(cost), TG, cls='sv-s', mono=True, bold=True) if cost > 1 else ''))
        S.at(t + .2, T(cx(i) + CW / 2, BY + 14, str(i + 1), FA, cls='sv-s', mono=True))
        t += .7 if cost == 1 else 1.0
    assert total == 31 and cap == 16
    S.at(t, R(X0 + N * (CW + 4) - 230, BY - 96 - 14, 230, 24, TG, TG, 8) + T(X0 + N * (CW + 4) - 115, BY - 96 + 3, 'total 31 for 16 = under 2 each', 'var(--on-fill)', mono=True, bold=True))
    S.say(t + .2, 'amortized O(1) · a single append can still be O(n)', 0, TG, True)
    S.at(t + .4, T(X0, S.sy + 22, 'measured on 2,000,000 appends: 92 growths, worst call 981× the median', MU, 'start'))
    return S.render(S.sy + 32)
figs['p2'] = amortized()

# ---------- 2.3 space: the recursion stack ----------
def space():
    lines = ['def total(i):', '    if i == n: return 0', '    return a[i] + total(i + 1)']
    a = [3, 1, 4, 1]; n = len(a)
    S = Story('bp3-', 0, 'Recursive sum of 3, 1, 4, 1. Each call waits for the next, so frames pile up: total(0) to total(4), five frames for n = 4. Then they return one by one: 0, 1, 5, 6, 9. The peak height is the extra memory: O(n). A loop would keep one variable: O(1).',
              'SPACE · THE RECURSION STACK COUNTS AS MEMORY')
    code = S.setcode(0, 40, lines)
    X0 = code.w + 40; CW = 40
    S.f.w = int(X0 + 230 + 150 + 150)
    for i, v in enumerate(a):
        S.at(.2 + i * .06, box(X0 + i * (CW + 6), 40, v, 'plain', CW, 32) + T(X0 + i * (CW + 6) + CW / 2, 88, str(i), FA, cls='sv-s', mono=True))
    SX, FW, FH = X0 + 230, 150, 28; SB = 260
    S.static(T(SX, SB + 20, 'call stack', MU, 'start') + L(SX - 6, SB, SX + FW + 6, SB, MU, 1.4))
    S.sx, S.sy = X0, 150; S.sw = 225
    S.at(1.0, chip(SX, 8, 'peak memory?', a='start'))
    fy = lambda k: SB - 4 - (k + 1) * (FH + 4)
    t = 2.0; ip = []
    for i in range(n + 1):
        S.line(t, 0); S.line(t + .3, 1)
        S.at(t, box(SX, fy(i), 'total(%d)' % i, 'plain', FW, FH, True), key='f%d' % i)
        S.say(t, 'total(%d) · %d frame%s' % (i, i + 1, '' if i == 0 else 's'), 0, PT)
        if i < n:
            if not ip: ip = [(0, 0, 0)]; it0 = t
            else: ip.append((t, i * (CW + 6), 0))
            S.line(t + .7, 2); S.say(t + .7, 'i ≠ n → wait for total(%d)' % (i + 1), 1, MU)
        else:
            S.say(t + .7, 'i == n → return 0', 1, TX)
        t += 1.3
    S.path(arrow(X0 + CW / 2, 120, X0 + CW / 2, 102, PT, 1.6, None, 6) + T(X0 + CW / 2 - 14, 124, 'i', PT, mono=True, bold=True), ip, it0, hide=t)
    S.at(t, R(SX + FW + 14, fy(n), 4, (n + 1) * (FH + 4) - 4, MID, 'none', 2) + T(SX + FW + 24, fy(n) + 18, 'peak 5', MID, 'start', mono=True, bold=True))
    t += 1.0
    acc = 0
    for i in range(n, -1, -1):
        r = acc if i == n else acc + a[i]
        acc = r
        S.line(t, 1 if i == n else 2)
        S.at(t, box(SX, fy(i), 'total(%d) = %d' % (i, r), 'seen', FW, FH, True), key='f%d' % i)
        S.say(t, 'total(%d) returns %d' % (i, r), 0, TX)
        S.say(t, '', 1)
        if i > 0: S.at(t + .6, box(SX, fy(i), 'total(%d) = %d' % (i, r), 'grey', FW, FH, True), key='f%d' % i)
        t += 1.0
    assert acc == 9
    S.at(t, box(SX, fy(0), 'total(0) = 9', 'ans', FW, FH, True), key='f0')
    S.say(t + .2, '✓ sum = 9 · peak 5 frames', 0, TG, True)
    S.at(t + .4, T(X0, S.sy + 50, 'n = 4 → 5 frames → O(n) space', TG, 'start', mono=True, bold=True))
    S.say(t + .2, 'a for-loop: one variable, O(1)', 1, MU)
    return S.render(SB + 30)
figs['p3'] = space()

# ---------- 2.4 hidden loops in one line ----------
def hidden():
    rows = [('x in list', 9412, 'x in set'), ('min(a); a.remove(x)', 713, 'heapq'), ('a.insert(0, x)', 511, 'deque.appendleft'),
            ('f(a[1:]) in recursion', 124, 'pass an index'), ('s += "a" in a loop', 1.8, '"".join(parts)')]
    S = Story('bp4-', 720, 'Five lines that look like one step. Measured at n = 100,000 against the right tool: x in list is 9,412 times slower than x in set; min and remove 713 times slower than heapq; insert at 0 is 511 times slower than deque appendleft; slicing in recursion 124 times slower than passing an index; string += only 1.8 times, thanks to a CPython shortcut.',
              'LINES THAT HIDE A LOOP · MEASURED SLOWDOWN vs THE RIGHT TOOL (LOG SCALE)')
    X0, Y0, RH, BX, BW = 6, 50, 40, 200, 300
    px = lambda v: BX + math.log10(v) / 4 * BW
    for e in range(5): S.static(L(px(10 ** e), Y0 - 8, px(10 ** e), Y0 + 5 * RH - 6, 'var(--rule)', 1, '2 4') + T(px(10 ** e), Y0 + 5 * RH + 10, '%s×' % ['1', '10', '100', '1,000', '10,000'][e], FA, cls='sv-s', mono=True))
    t = .6
    for k, (code, x, fix) in enumerate(rows):
        y = Y0 + k * RH
        S.at(t, T(X0, y + 18, code, TX, 'start', mono=True))
        S.at(t + .2, bring(X0 - 6, y - 2, 190, 30), hide=t + 1.4)
        S.at(t + .4, R(BX, y + 4, px(x) - BX, 20, TG if x > 100 else it('.35'), 'none', 3), d=.6)
        S.at(t + 1.0, T(px(x) + 8, y + 19, '{:,}×'.format(x) if x >= 10 else '%g×' % x, TG if x > 100 else MU, 'start', mono=True, bold=True))
        S.at(t + 1.2, T(BX + BW + 100, y + 18, '→ ' + fix, PT, 'start', mono=True))
        t += 1.7
    S.at(t, T(BX + BW + 100, Y0 + 5 * RH + 10, 'each looks O(1), is O(n)', TG, 'start', bold=True))
    return S.render(Y0 + 5 * RH + 20)
figs['p4'] = hidden()

# ---------- 3.x code shapes ----------
def single():
    lines = ['s = 0', 'for x in a:', '    s += x']
    a = [5, 2, 7, 1, 3, 8]
    S = Story('bq1-', 0, 'A single loop over six numbers. Pointer i slides one cell per step and the line s += x runs once per cell: six runs for n = 6. Work grows in step with n: O(n).',
              'ONE LOOP · THE BODY RUNS ONCE PER ITEM')
    code = S.setcode(0, 40, lines)
    X0 = code.w + 40; CW = 42
    S.f.w = 680
    for i, v in enumerate(a): S.at(.2 + i * .05, box(X0 + i * (CW + 6), 50, v, 'plain', CW, 34) + T(X0 + i * (CW + 6) + CW / 2, 102, str(i), FA, cls='sv-s', mono=True))
    S.at(1.0, chip(530, 24, 'how many runs?', a='start'))
    S.sx, S.sy = X0, 160
    t = 2.0; S.line(t, 0); S.say(t, 's = 0 · runs = 0', 0, PT); s = 0; ip = []
    t += 1.0
    for i, v in enumerate(a):
        S.line(t, 1); S.line(t + .3, 2)
        if not ip: ip = [(0, 0, 0)]; it0 = t
        else: ip.append((t, i * (CW + 6), 0))
        S.at(t + .3, bring(X0 + i * (CW + 6), 50, CW, 34), hide=t + 1.0)
        s += v
        S.say(t + .3, 's += a[%d] = %d → s = %d · runs = %d' % (i, v, s, i + 1), 0, TX)
        S.at(t + 1.0, box(X0 + i * (CW + 6), 50, v, 'seen', CW, 34))
        t += 1.2
    S.path(arrow(X0 + CW / 2, 136, X0 + CW / 2, 112, PT, 1.6, None, 6) + T(X0 + CW / 2 + 10, 132, 'i', PT, 'start', mono=True, bold=True), ip, it0, hide=t)
    S.at(t, ''.join(box(X0 + i * (CW + 6), 50, v, 'ans', CW, 34) for i, v in enumerate(a)))
    S.say(t + .2, '✓ 6 runs for n = 6 → O(n)', 0, TG, True)
    return S.render(max(40 + code.h(), S.sy + 14) + 8)
figs['q1'] = single()

def nested():
    lines = ['for i in range(n):', '    for j in range(i + 1, n):', '        check(a[i], a[j])']
    n = 5
    S = Story('bq2-', 0, 'Two nested loops over n = 5 items, checking every pair once. A 5 by 5 grid of pairs: i picks the row, j slides along it, each check fills one cell above the diagonal. Rows hold 4, 3, 2, 1, 0 checks: 10 in total, n times n minus 1 over 2, about half of n squared: O(n squared).',
              'LOOP INSIDE A LOOP · EVERY PAIR (i, j)')
    code = S.setcode(0, 40, lines)
    X0 = code.w + 60; Y0 = 50; C = 38
    S.f.w = int(X0 + n * C + 230)
    for k in range(n):
        S.static(T(X0 - 12, Y0 + k * C + 24, str(k), MU, mono=True) + T(X0 + k * C + C / 2, Y0 - 8, str(k), MU, mono=True))
    S.static(T(X0 - 30, Y0 + n * C / 2, 'i', PT, mono=True, bold=True) + T(X0 + n * C / 2, Y0 - 26, 'j', PT, mono=True, bold=True))
    for i in range(n):
        for j in range(n): S.at(.2 + (i * n + j) * .02, R(X0 + j * C, Y0 + i * C, C - 4, C - 4, 'var(--bg)', RULE_HI, 5, 1), key='c%d%d' % (i, j))
    RX = X0 + n * C + 24
    S.at(1.0, chip(RX, 24, 'how many checks?', a='start'))
    S.sx, S.sy = RX, Y0 + 50; S.sw = 200
    t = 2.0; cnt = 0; rp = []
    for i in range(n):
        S.line(t, 0)
        S.at(t, R(X0 - 3, Y0 + i * C - 3, n * C + 2, C + 2, 'none', PT, 7, 1.6), key='row')
        for j in range(i + 1):
            S.at(t + .2, R(X0 + j * C, Y0 + i * C, C - 4, C - 4, 'var(--sunk)', 'var(--rule)', 5, 1), key='c%d%d' % (i, j))
        S.say(t, 'i = %d: j runs %d..%d' % (i, i + 1, n - 1) if i < n - 1 else 'i = %d: j has nothing left' % i, 0, PT)
        t += .7
        for j in range(i + 1, n):
            S.line(t, 1); S.line(t + .15, 2)
            cnt += 1
            if not rp: rp = [(0, 0, 0)]; rt0 = t
            else: rp.append((t, (j - 1) * C, i * C))
            S.at(t + .15, R(X0 + j * C, Y0 + i * C, C - 4, C - 4, it('.18'), TG, 5, 1.2) + T(X0 + j * C + C / 2 - 2, Y0 + i * C + 22, str(cnt), TG, cls='sv-s', mono=True, bold=True), key='c%d%d' % (i, j))
            S.say(t + .15, 'check (%d, %d) · checks = %d' % (i, j, cnt), 1, TX)
            t += .55
        t += .3
    S.off('row', t)
    S.path(bring(X0 + 1 * C, Y0, C - 4, C - 4), rp, rt0, hide=t, d=.25)
    assert cnt == n * (n - 1) // 2 == 10
    S.at(t, R(RX, Y0 + 104, 170, 28, TG, TG, 8) + T(RX + 85, Y0 + 123, 'n(n − 1)/2 = 10', 'var(--on-fill)', mono=True, bold=True))
    S.say(t + .2, '', 0)
    S.say(t + .2, '', 1)
    S.at(t + .3, T(RX, Y0 + 158, '✓ ≈ n²/2 → O(n²)', TG, 'start', mono=True, bold=True) + T(RX, Y0 + 180, 'n = 10⁵ → 5 × 10⁹', MU, 'start', mono=True))
    return S.render(max(40 + code.h(), Y0 + n * C) + 14)
figs['q2'] = nested()

def halving():
    lines = ['steps = 0', 'while n > 1:', '    n //= 2', '    steps += 1']
    N = 16
    S = Story('bq3-', 0, 'A loop that halves n each pass. Sixteen cells: after each pass half of what is left greys out, 16, 8, 4, 2, 1. Four passes: log2 of 16. Doubling n to 32 adds only one pass: O(log n).',
              'HALVING LOOP · n SHRINKS BY HALF EACH PASS')
    code = S.setcode(0, 40, lines)
    X0 = code.w + 40; CW = 24
    S.f.w = 680
    for i in range(N): S.at(.2 + i * .03, R(X0 + i * (CW + 3), 50, CW, 30, 'var(--bg)', RULE_HI, 4, 1.2))
    Y_ = 50
    S.at(1.0, chip(530, 10, 'how many passes?', a='start'))
    S.sx, S.sy = X0, 130
    n = N; steps = 0; t = 2.0; S.line(t, 0); S.say(t, 'n = 16 · steps = 0', 0, PT)
    rp = []
    t += 1.0
    while n > 1:
        S.line(t, 1); S.line(t + .4, 2)
        S.at(t + .4, R(X0 - 3, 47, n * (CW + 3) + 3, 36, 'none', MID, 6, 2.2), hide=t + 1.2)
        half = n // 2
        for i in range(half, n): S.at(t + .8, R(X0 + i * (CW + 3), 50, CW, 30, 'var(--sunk)', 'var(--rule)', 4, 1))
        S.line(t + 1.0, 3); steps += 1
        S.say(t + .4, 'n = %d // 2 = %d · steps = %d' % (n, half, steps), 0, TX)
        n = half; t += 1.6
    assert steps == 4
    S.at(t, R(X0, 50, CW, 30, TG, TG, 4, 1.2))
    S.say(t + .2, '✓ 4 passes = log₂ 16 → O(log n)', 0, TG, True)
    S.at(t + .5, T(X0, S.sy + 24, 'n = 32 → 5 passes · n = 10⁶ → 20', MU, 'start', mono=True))
    return S.render(max(40 + code.h(), S.sy + 34) + 8)
figs['q3'] = halving()

def rectree():
    lines = ['def fib(n):', '    if n < 2: return n', '    return fib(n - 1) + fib(n - 2)']
    S = Story('bq4-', 0, 'Call tree of fib(5). Each call that is not a base case splits into two. Levels appear one by one with 1, 2, 4, 6 and 2 calls: 15 calls in total. Doubling per level means about 2 to the n calls: O(2 to the n).',
              'RECURSION TREE · BRANCHES ^ DEPTH')
    code = S.setcode(0, 40, lines)
    X0 = code.w + 30
    W = 380
    S.f.w = int(X0 + W + 130)
    # build tree with x positions by leaf order
    nodes = []
    def build(n, d):
        idx = len(nodes); nodes.append([n, d, None, []])
        if n >= 2:
            nodes[idx][3] = [build(n - 1, d + 1), build(n - 2, d + 1)]
        return idx
    build(5, 0)
    leaves = [k for k in range(len(nodes)) if not nodes[k][3]]
    LW = W / len(leaves)
    def setx(k):
        if not nodes[k][3]: nodes[k][2] = X0 + leaves.index(k) * LW + LW / 2
        else:
            for c in nodes[k][3]: setx(c)
            nodes[k][2] = sum(nodes[c][2] for c in nodes[k][3]) / len(nodes[k][3])
    setx(0)
    Y0, DY, r = 48, 50, 14
    S.at(1.0, chip(0, 150, 'how many calls?', a='start'))
    depth = max(n[1] for n in nodes)
    t = 1.8; tot = 0
    for d in range(depth + 1):
        lvl = [k for k in range(len(nodes)) if nodes[k][1] == d]
        S.line(t, 2 if d else 0)
        for k in lvl:
            n, _, x, ch = nodes[k]; y = Y0 + d * DY
            for c in ch: S.at(t + .5, L(x, y + r, nodes[c][2], y + DY - r, RULE_HI, 1.2))
            base = n < 2
            S.at(t, circ(x, y, r, 'var(--bg)') + circ(x, y, r, 'var(--sunk)' if base else 'var(--bg)', 'var(--rule)' if base else RULE_HI, 1.2) + T(x, y + 4, str(n), GH if base else TX, cls='sv-s', mono=True, bold=not base))
        tot += len(lvl)
        S.at(t, T(X0 + W + 20, Y0 + d * DY + 4, '%d call%s' % (len(lvl), '' if len(lvl) == 1 else 's'), PT, 'start', mono=True, bold=True))
        t += 1.3
    assert tot == 15
    S.static(T(X0 + W + 20, Y0 - 22 + 0, '', MU))
    S.at(t, R(X0 + W + 14, Y0 + (depth + 1) * DY - 14, 100, 26, TG, TG, 8) + T(X0 + W + 64, Y0 + (depth + 1) * DY + 4, 'total 15', 'var(--on-fill)', mono=True, bold=True))
    S.sx, S.sy = 0, 210; S.sw = X0 - 20
    S.say(t + .3, '✓ ×2 per level → O(2ⁿ)', 0, TG, True)
    S.at(t + .5, T(0, S.sy + 22, 'grey = base case, no split', MU, 'start') + T(0, S.sy + 42, 'fib(40) → 3 × 10⁸ calls', MU, 'start'))
    return S.render(max(Y0 + (depth + 1) * DY + 22, S.sy + 50))
figs['q4'] = rectree()

os.makedirs('/tmp/dsa', exist_ok=True)
json.dump(figs, open('/tmp/dsa/big-o-complexity.json', 'w'))
print({k: len(v) for k, v in figs.items()})

# ---------- splice ----------
PAGE = 'content/01-dsa/02-foundations/big-o-complexity/index.html'
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))

def sub(sid, num, title, skey, fig, sig=None):
    s = '  <div class="subsec" id="%s">\n    <h3 class="ssh"><b>%s</b>%s</h3>\n    <p class="skey">%s</p>\n%s\n' % (sid, num, title, skey, figs[fig])
    if sig: s += '    <p class="sig">Signals: %s</p>\n' % sig
    return s + '  </div>\n'

O = lambda x: '<span class="mth">O(%s)</span>' % x
n_ = '<var>n</var>'
art = '''<article class="doc" id="art-bigo" data-title="Big-O" data-tag="Foundations" data-blurb="How the work grows with n, which order fits a given n, and how to read the order off the shape of the code.">
        <header class="hero">
  <p class="eyebrow">DSA · foundations</p>
  <h1><em>Big-O</em></h1>
  <p class="lede">Read the limit on ''' + n_ + ''', know at once what is allowed.</p>
</header>

<section id="bigo-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Big-O is <em>the shape of the growth</em>, not a number of seconds.</p>
''' + sub('bigo-s1-1', '1.1', 'Growth curves', 'Same ' + n_ + ', very different work — <em>the curve decides</em>.', 'm1') \
    + sub('bigo-s1-2', '1.2', 'Constants are dropped', 'A lower order is not faster at every ' + n_ + ' — <em>only past the crossing</em>.', 'm2') + '''</section>

<section id="bigo-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Properties</h2></div>
  <p class="key">What to memorize — <em>the budget, the averages, the hidden costs</em>.</p>
''' + sub('bigo-s2-1', '2.1', 'Which order fits n', 'About <em>10⁸ simple steps per second</em>: pick the highest order that stays under it.', 'p1') \
    + sub('bigo-s2-2', '2.2', 'Amortized cost', 'Rare expensive steps, <em>averaged over all of them</em>, can still be ' + O('1') + '.', 'p2') \
    + sub('bigo-s2-3', '2.3', 'Space', 'Count <em>extra</em> memory — the recursion stack counts too.', 'p3') \
    + sub('bigo-s2-4', '2.4', 'Lines that hide a loop', 'One line can be ' + O(n_) + ' — <em>the code does not show it</em>.', 'p4') + '''</section>

<section id="bigo-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Patterns</h2></div>
  <p class="key">Count how often <em>the innermost line</em> runs — the code shape tells you.</p>
''' + sub('bigo-s3-1', '3.1', 'One loop', 'One pass over the input → ' + O(n_) + '.', 'q1',
          'one <code>for</code> over the input · two pointers that only move forward · sequential loops add, still ' + O(n_)) \
    + sub('bigo-s3-2', '3.2', 'Loop inside a loop', 'Every pair → <em>multiply</em> → ' + O(n_ + '²') + '.', 'q2',
          'a <code>for</code> inside a <code>for</code> over the same input · "every pair"') \
    + sub('bigo-s3-3', '3.3', 'Halving loop', 'Cut the work in half each pass → ' + O('<b class="fn">log</b> ' + n_) + '.', 'q3',
          '<code>n //= 2</code> · <code>l</code>/<code>r</code> closing on a middle · heap push/pop, balanced tree depth') \
    + sub('bigo-s3-4', '3.4', 'Recursion tree', 'Calls = <em>branches<sup>depth</sup></em>.', 'q4',
          'a function calling itself twice · no memo → ' + O('2<sup><var>n</var></sup>') + ' · halve and merge → ' + O(n_ + ' <b class="fn">log</b> ' + n_)) + '''</section>

''' + REPLAY + '''

<footer>DSA · Big-O · timings measured on CPython 3.12.</footer>

      </article>'''
splice(os.path.join(ROOT, PAGE), art)
print('spliced', PAGE)
