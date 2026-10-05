"""Figures for content/01-dsa/04-algorithms/greedy. Writes /tmp/dsa/greedy.json."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from algo4 import *

figs = {}

# ---------------------------------------------------------------- coins (1.1 + 1.2)
def coin_run(f, coins, amount, X0, y, t, label, cw=46):
    """greedy coin run on one row; returns (t, picks, row drawer)"""
    A = Arr(X0, y, coins, cw, 34, 8); A.reserve(f)
    rem = amount; picks = []; RX = X0 + len(coins) * (cw + 8) + 40
    f.static(lab(0, y + 22, label, MU) + lab(0, y + 74, 'taken', MU))
    f.show(chip(RX, y + 5 - 0, 'left = %d' % rem, PT), t, hide=t + 1.0); t += 1.1
    while rem:
        k = next(i for i, c in enumerate(coins) if c <= rem)
        f.show(A.ring(k), t, hide=t + 1.4)
        nr = rem - coins[k]
        f.show(st(RX, y + 22, 'biggest ≤ %d is %d → %d − %d = %d' % (rem, coins[k], rem, coins[k], nr), TX), t, hide=t + 1.4)
        # coin drops into the result row
        px = X0 + len(picks) * 44
        f.path(box(A.xl(k) + 4, y, coins[k], cw - 8, 34, 'b', True), [(0, 0, 0), (t + .5, px - A.xl(k) - 4, 52)], t + .3, d=.5)
        picks.append(coins[k]); rem = nr; t += 1.7
    A.commit(f, .2, idxs=False)
    return t, picks, RX

def coins_ok():
    f = Anim('gr-m1-', 760, 150, 'Make 41 with coins 25 10 5 1. Each step takes the biggest coin that still fits: 25, 10, 5, 1. Four coins, the best possible.',
             'TAKE THE BEST NOW · MAKE 41 WITH COINS 25 10 5 1', 3); f.h = 190
    f.show(chip(130, 22, 'goal: fewest coins for 41'), .4)
    t, picks, RX = coin_run(f, [25, 10, 5, 1], 41, 130, 60, 1.8, 'coins')
    assert picks == [25, 10, 5, 1]
    for k, v in enumerate(picks): f.show(box(130 + k * 44, 112, v, 38, 34, 'f', True), t + k * .06)
    f.show(st(130 + 4 * 44 + 10, 134, '✓ 4 coins', TG, True), t + .4)
    f.show(lab(130, 178, 'one choice per step, never undone · O(number of coins)', TG, bold=True), t + .6)
    return f.render()
figs['m1'] = coins_ok()

def coins_bad():
    f = Anim('gr-m2-', 760, 260, 'Make 6 with coins 4 3 1. Greedy takes 4, then 1, then 1: three coins. The best answer is 3 + 3: two coins. '
             'Greedy was wrong, and nothing in its run warned you.', 'WHEN GREEDY FAILS · MAKE 6 WITH COINS 4 3 1', 3)
    f.show(chip(130, 22, 'goal: fewest coins for 6'), .4)
    t, picks, RX = coin_run(f, [4, 3, 1], 6, 130, 60, 1.8, 'greedy')
    assert picks == [4, 1, 1]
    f.show(st(130 + 3 * 44 + 10, 134, '3 coins', MU, True), t)
    t += .8
    y2 = 172
    f.show(lab(0, y2 + 22, 'best', MU), t)
    f.show(st(130, y2 + 22, 'try 3 + 3 instead', TX), t, hide=t + 1.5)
    t += 1.6
    for k in range(3): f.show(box(130 + k * 44, 112, picks[k], 38, 34, 'g', True), t)
    for k, v in enumerate((3, 3)): f.show(box(130 + k * 44, y2, v, 38, 34, 'f', True), t + k * .1)
    f.show(st(130 + 2 * 44 + 10, y2 + 22, '✓ 2 coins', TG, True), t + .4)
    f.show(lab(130, y2 + 66, 'the biggest coin was not safe here → use dynamic programming', TG, bold=True), t + .7)
    return f.render()
figs['m2'] = coins_bad()

# ---------------------------------------------------------------- timeline helper
class Line:
    def __init__(s, x0, y0, u, tmax, rh=30):
        s.x0, s.y0, s.u, s.tmax, s.rh = x0, y0, u, tmax, rh
    def X(s, v): return s.x0 + v * s.u
    def bar(s, row, a, b, name, st_='n'):
        x, y, w, h = s.X(a), s.y0 + row * s.rh, (b - a) * s.u, s.rh - 8
        fill, stroke, tc = {'n': ('var(--bg)', RULE_HI, TX), 'g': ('var(--sunk)', 'var(--rule)', GH),
                            'f': (TG, TG, ON), 'b': (it('.12'), TG, TG)}[st_]
        o = R(x, y, w, h, 'var(--bg)', 'none', 5) if st_ in 'b' else ''
        return o + R(x, y, w, h, fill, stroke, 5, 1.2) + T(x + w / 2, y + h / 2 + 4, esc(name), tc, cls='sv-s', mono=True, bold=True)
    def ring(s, row, a, b): return ring(s.X(a), s.y0 + row * s.rh, (b - a) * s.u, s.rh - 8, 6)
    def axis(s, rows):
        y = s.y0 + rows * s.rh + 4
        o = L(s.X(0), y, s.X(s.tmax), y, MU, 1)
        for v in range(0, s.tmax + 1, 2): o += L(s.X(v), y, s.X(v), y + 4, MU, 1) + T(s.X(v), y + 16, str(v), FA, cls='sv-s', mono=True)
        return o

# ---------------------------------------------------------------- 1.3 exchange argument
def exchange():
    iv = [('A', 0, 3), ('B', 1, 4), ('C', 4, 7), ('D', 8, 10), ('E', 5, 9)]
    rows = {'A': 0, 'B': 1, 'C': 2, 'E': 3, 'D': 4}
    f = Anim('gr-m3-', 760, 260, 'Why "earliest end first" is safe. A best schedule keeps B, C, D. A ends earliest of all. '
             'Swap B for A: A ends before B did, so it clashes with nothing; still three meetings. So some best answer starts with A.',
             'WHY IT IS SAFE · SWAP ONE PICK OF A BEST ANSWER', 3.2); f.h = 262
    Ln = Line(150, 40, 46, 10)
    for k, (nm, a, b) in enumerate(iv): f.show(Ln.bar(rows[nm], a, b, nm), .2 + k * .1)
    f.show(Ln.axis(5), .2)
    f.static(lab(0, 60, 'meetings', MU))
    t = 1.6
    f.show(st(Ln.X(0), 246, 'a best answer keeps B, C, D (3 meetings)', PT, True), t, hide=t + 2.0)
    for nm in 'BCD':
        _, a, b = next(x for x in iv if x[0] == nm)
        f.show(Ln.bar(rows[nm], a, b, nm, 'b'), t + .3, hide=t + 4.8 if nm == 'B' else None)
    t += 2.4
    f.show(Ln.ring(0, 0, 3), t, hide=t + 2.2)
    f.show(st(Ln.X(0), 246, 'greedy picks A: it ends first, at 3', TX), t, hide=t + 2.2)
    t += 2.4
    f.show(Ln.bar(1, 1, 4, 'B', 'g'), t)
    f.show(Ln.bar(0, 0, 3, 'A', 'b'), t)
    f.show(L(Ln.X(3), 36, Ln.X(3), 40 + 5 * 30, MID, 1.6, '4 3') + L(Ln.X(4), 36, Ln.X(4), 40 + 5 * 30, MID, 1.6, '4 3'), t + .2, hide=t + 2.4)
    f.show(st(Ln.X(0), 246, 'swap B → A: A ends at 3 ≤ 4 where B ended → no new clash', TX), t, hide=t + 2.4)
    t += 2.6
    for nm, r, a, b in (('A', 0, 0, 3), ('C', 2, 4, 7), ('D', 4, 8, 10)): f.show(Ln.bar(r, a, b, nm, 'f'), t)
    f.show(lab(Ln.X(0), 246, '✓ still 3 meetings → taking the earliest end never loses the best answer', TG, bold=True), t + .4)
    return f.render()
figs['m3'] = exchange()

# ---------------------------------------------------------------- 2.1 smallest that fits (assign cookies)
def cookies():
    g = [1, 2, 4]; s = [1, 2, 3]
    lines = ['g.sort(); s.sort()', 'i = j = 0', 'while i < len(g) and j < len(s):', '    if s[j] >= g[i]: i += 1', '    j += 1', 'return i']
    code = Code2(0, 40, lines)
    X0 = code.w + 60
    f = Anim('gr-q1-', 760, 0, 'Children need 1 2 4, cookies are 1 2 3, both sorted. Give each child the smallest cookie that fits: 1 to 1, 2 to 2, '
             'cookie 3 is too small for 4. Two children fed.', 'SMALLEST THAT FITS · CHILDREN [1 2 4] · COOKIES [1 2 3]', 3.2)
    f.static(code.svg())
    G = Arr(X0, 96, g, 46, 34, 30); S = Arr(X0, 200, s, 46, 34, 30)
    G.reserve(f)
    f.static(lab(X0 - 14, 117, 'need g', MU, 'end') + lab(X0 - 14, 221, 'cookie s', MU, 'end'))
    f.show(chip(X0, 24, 'goal: feed the most children'), .9)
    pi = Ptr(G, 'i', 0, up=True); pj = Ptr(S, 'j', 0)
    t = 2.2; bar = [(t, 0), (t + .5, 1)]; t += 1.2; i = j = 0; SY = 306; ov = []
    while i < 3 and j < 3:
        bar.append((t, 2)); bar.append((t + .4, 3))
        f.show(G.ring(i) + S.ring(j), t + .2, hide=t + 1.9)
        if s[j] >= g[i]:
            f.show(st(X0, SY, 's[%d] = %d ≥ g[%d] = %d → feed, i += 1' % (j, s[j], i, g[i]), TX), t + .2, hide=t + 1.9)
            f.show(L(G.cx(i), 96 + 34, S.cx(j), 200, TG, 2), t + .9)
            ov.append((G.cell(i, 'b', 0), t + .9)); ov.append((S.cell(j, 'b', 0), t + .9))
            i += 1; pi.to(t + 1.5, i)
        else:
            f.show(st(X0, SY, 's[%d] = %d < g[%d] = %d → too small, skip it' % (j, s[j], i, g[i]), TX), t + .2, hide=t + 1.9)
            ov.append((S.cell(j, 'g', 0), t + .9))
        bar.append((t + 1.1, 4)); j += 1
        if j < 3: pj.to(t + 1.5, j)
        t += 2.2
    bar.append((t, 2)); bar.append((t + .4, 5)); end = t + .6
    G.commit(f, .2, idxs=False); S.commit(f, .2, idxs=False)
    pi.commit(f, 2.6, hide=end); pj.commit(f, 2.6, hide=end)
    for o, a in ov: f.show(o, a)
    code.run(f, bar)
    for k in range(2): f.show(G.cell(k, 'f', 0) + S.cell(k, 'f', 0), end + k * .08)
    f.show(st(G.xl(2) + 60, 117, '✓ 2 fed', TG, True), end + .3)
    f.show(lab(X0, SY, 'answer i = 2 · sort O(n log n), match O(n)', TG, bold=True), end + .5)
    f.h = SY + 16
    return f.render()
figs['q1'] = cookies()

# ---------------------------------------------------------------- 2.2 sort by end point (non-overlapping intervals)
def by_end():
    iv = [(1, 2), (2, 3), (3, 4), (1, 3)]
    ivs = sorted(iv, key=lambda x: x[1])
    names = {(1, 2): 'a', (2, 3): 'b', (1, 3): 'c', (3, 4): 'd'}
    lines = ['iv.sort(key=lambda x: x[1])', 'end, removed = -inf, 0', 'for s, e in iv:', '    if s >= end: end = e', '    else: removed += 1']
    code = Code2(0, 40, lines)
    X0 = code.w + 50
    f = Anim('gr-q2-', 760, 0, 'Intervals [1,2] [2,3] [3,4] [1,3] sorted by end. Keep an interval when it starts at or after the last kept end, '
             'else remove it. [1,3] starts at 1 before end 2: removed. Answer: 1 removal.', 'SORT BY END POINT · FEWEST REMOVALS TO STOP OVERLAPS', 3.2)
    f.static(code.svg())
    Ln = Line(X0, 88, 80, 4, 34)
    f.show(chip(X0, 24, 'goal: fewest intervals removed'), .9)
    t0 = .3
    for k, (a, b) in enumerate(iv):
        f.path(Ln.bar(k, a, b, '%s [%d,%d]' % (names[(a, b)], a, b)), [(0, 0, 0), (2.7, 0, (ivs.index((a, b)) - k) * Ln.rh)], t0 + k * .1)
    f.show(Ln.axis(4), .2)
    t = 2.4; bar = [(t, 0)]
    f.show(st(X0, 274, 'sort by end → a, b, c, d', PT, True), t, hide=t + 1.6)
    t += 2.0; bar.append((t, 1)); t += .5
    end = None; removed = 0; out = []
    endline = None
    for k, (a, b) in enumerate(ivs):
        bar.append((t, 2)); bar.append((t + .4, 3))
        f.show(Ln.ring(k, a, b), t + .2, hide=t + 2.0)
        if end is None or a >= end:
            f.show(st(X0, 274, ('s = %d ≥ end = %s' % (a, end if end is not None else '-inf')) + ' → keep, end = %d' % b, TX), t + .2, hide=t + 2.0)
            out.append((Ln.bar(k, a, b, '%s [%d,%d]' % (names[(a, b)], a, b), 'b'), t + 1.0))
            end = b; endline = (endline or []) + [(t + 1.0, end)]
        else:
            bar.append((t + .8, 4))
            f.show(st(X0, 274, 's = %d < end = %d → overlap, remove' % (a, end), TX), t + .2, hide=t + 2.0)
            out.append((Ln.bar(k, a, b, '%s [%d,%d]' % (names[(a, b)], a, b), 'g'), t + 1.0)); removed += 1
        t += 2.3
    fin = t
    code.run(f, bar)
    for o, a_ in out: f.show(o, a_)
    e0 = endline[0][1]
    f.path(L(Ln.X(e0), 78, Ln.X(e0), 88 + 4 * 34, PT, 1.8, '4 3') + T(Ln.X(e0), 74, "end", PT, mono=True, bold=True),
           [(0, 0, 0)] + [(tt, (v - e0) * Ln.u, 0) for tt, v in endline[1:]], endline[0][0], hide=fin)
    f.items.insert(1, f.items.pop())  # behind the bars
    for k, (a, b) in enumerate(ivs):
        if not (a == 1 and b == 3): f.show(Ln.bar(k, a, b, '%s [%d,%d]' % (names[(a, b)], a, b), 'f'), fin)
    assert removed == 1
    f.show(lab(X0, 274, '✓ removed = 1 · earliest end leaves the most room', TG, bold=True), fin + .4)
    f.h = 286
    return f.render()
figs['q2'] = by_end()

# ---------------------------------------------------------------- 2.3 reach farthest (jump game)
def reach():
    a = [2, 1, 3, 0, 1, 0, 2]; n = len(a)
    lines = ['reach = 0', 'for i, x in enumerate(a):', '    if i > reach: return False', '    reach = max(reach, i + x)', 'return True']
    code = Code2(0, 40, lines)
    X0 = code.w + 40; CY = 110
    f = Anim('gr-q3-', 760, 0, 'Jump game on 2 1 3 0 1 0 2: a[i] is the longest jump from i. Walk left to right keeping the farthest reachable index. '
             'Reach grows to 2, then 5, then 8, which covers the last index 6: reachable.', 'REACH FARTHEST · CAN YOU JUMP TO THE LAST CELL?', 3.2)
    f.static(code.svg())
    A = Arr(X0, CY, a, 44, 36, 8); A.reserve(f)
    f.show(goal_ring(A.xl(n - 1), CY, 44, 36), 1.0)
    f.path(chip(A.xl(n - 1) - 40, CY - 40, 'last cell'), [(0, 0, 0), (2.0, X0 - A.xl(n - 1) + 40, 24 - (CY - 40))], 1.0)
    t = 3.0; bar = [(t, 0)]; SY = CY + 120; r = 0; i_p = Ptr(A, 'i', 0)
    rp = [(0, 0, 0)]
    def arc(i, j):
        x1, x2 = A.cx(i), A.cx(min(j, n - 1)); h = 16 + (j - i) * 7
        return '<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="1.6"/>' % (x1, CY - 4, (x1 + x2) / 2, CY - 4 - h * 2, x2, CY - 4, MID)
    f.show(st(X0, SY, 'reach = 0', PT, True), t, hide=t + 1.0); t += 1.2
    for i, x in enumerate(a):
        bar.append((t, 1)); i_p.to(t, i)
        f.show(A.ring(i), t + .3, hide=t + 1.9)
        bar.append((t + .5, 2))
        nr = max(r, i + x)
        bar.append((t + .9, 3))
        if x: f.show(arc(i, i + x), t + .9, hide=t + 2.0)
        f.show(st(X0, SY, 'i = %d ≤ reach %d · i + a[i] = %d + %d = %d → reach = %d' % (i, r, i, x, i + x, nr), TX), t + .3, hide=t + 1.9)
        if nr != r: rp.append((t + 1.4, min(nr, n) * (A.w + A.g), 0)); r = nr
        t += 2.2
        if r >= n - 1: break
    bar.append((t, 4)); end = t + .3
    code.run(f, bar)
    RX = A.xl(0) - A.g / 2
    f.path(L(RX, CY - 8, RX, CY + 66, PT, 2, '4 3') + T(RX, CY + 80, 'reach', PT, mono=True, bold=True), rp, 4.2, hide=end)
    i_p.commit(f, 4.2, hide=end)
    A.commit(f, .2)
    f.show(A.cell(n - 1, 'f', 0), end)
    f.show(T(A.cx(n - 1), CY + 66, '✓ found', TG, mono=True, bold=True), end + .3)
    f.show(lab(X0, SY, 'reach 8 ≥ 6 → the last cell is reachable · one pass, O(n)', TG, bold=True), end + .5)
    f.h = max(code.y + code.h(), SY + 12) + 6
    return f.render()
figs['q3'] = reach()

# ---------------------------------------------------------------- 2.4 take every gain (stock II)
def gains():
    p = [7, 1, 5, 3, 6, 4]; n = len(p)
    lines = ['profit = 0', 'for i in range(1, len(p)):', '    if p[i] > p[i-1]:', '        profit += p[i] - p[i-1]']
    code = Code2(0, 40, lines)
    X0 = code.w + 50
    f = Anim('gr-q4-', 760, 0, 'Stock prices 7 1 5 3 6 4, buy and sell as often as you like. Add every rise between neighbours: 1 to 5 is +4, 3 to 6 is +3. Profit 7.',
             'TAKE EVERY GAIN · PRICES 7 1 5 3 6 4', 3.2)
    f.static(code.svg())
    # prices as columns
    BW, G, base, sc = 44, 12, 230, 18
    cx = lambda i: X0 + i * (BW + G) + BW / 2
    for i, v in enumerate(p):
        f.show(R(cx(i) - BW / 2, base - v * sc, BW, v * sc, 'var(--bg)', RULE_HI, 4, 1.2) + T(cx(i), base - v * sc - 6, str(v), TX, mono=True, bold=True)
               + idx(cx(i), base + 16, i), .2 + i * .06)
    f.show(chip(X0, 24, 'goal: max profit'), .9)
    t = 2.2; bar = [(t, 0)]; prof = 0; SY = base + 66; ip = [(0, 0, 0)]
    f.show(st(X0, SY, 'profit = 0', PT, True), t, hide=t + 1.0); t += 1.2
    rises = []
    for i in range(1, n):
        bar.append((t, 1)); ip.append((t, (i - 1) * (BW + G), 0)); bar.append((t + .4, 2))
        x0 = cx(i - 1) - BW / 2; top = base - max(p[i], p[i - 1]) * sc
        f.show(ring(x0, top, 2 * BW + G, base - top, 6), t + .3, hide=t + 1.9)
        if p[i] > p[i - 1]:
            prof += p[i] - p[i - 1]; bar.append((t + .8, 3))
            f.show(st(X0, SY, 'p[%d] = %d > %d → profit += %d → %d' % (i, p[i], p[i - 1], p[i] - p[i - 1], prof), TX), t + .3, hide=t + 1.9)
            rises.append(i)
            f.show(arrow(cx(i - 1) + 10, base - p[i - 1] * sc - 20, cx(i) - 12, base - p[i] * sc - 14, MID, 2, None, 7) +
                   T((cx(i - 1) + cx(i)) / 2 - 14, base - p[i] * sc - 18, '+%d' % (p[i] - p[i - 1]), MID, mono=True, bold=True), t + .9)
        else:
            f.show(st(X0, SY, 'p[%d] = %d ≤ %d → no gain, skip' % (i, p[i], p[i - 1]), TX), t + .3, hide=t + 1.9)
        t += 2.2
    end = t
    code.run(f, bar + [(end, 1)])
    f.path(ptr(cx(1), base + 18, 'i', PT, 10), [(0, 0, 0)] + ip[2:], 3.4, hide=end)
    for i in rises:
        f.show(R(cx(i) - BW / 2, base - p[i] * sc, BW, p[i] * sc, TG, TG, 4, 1.2), end)
    assert prof == 7
    f.show(lab(X0, SY, '✓ profit = 4 + 3 = 7 · every rise is a buy-then-sell', TG, bold=True), end + .4)
    f.h = max(code.y + code.h(), SY + 12) + 6
    return f.render()
figs['q4'] = gains()

# ---------------------------------------------------------------- 2.5 greedy + heap (task scheduler)
def tasks():
    cnt = {'A': 3, 'B': 2, 'C': 1}; nidle = 2
    f = Anim('gr-q5-', 760, 250, 'Tasks A A A B B C, the same task needs 2 slots of rest. Each round, take up to 3 different tasks, the ones with the most left first (a max-heap). '
             'Round 1: A B C. Round 2: A B, then idle. Round 3: A. Total 7 slots.', 'GREEDY + HEAP · TASKS A×3 B×2 C×1 · REST n = 2', 3.2); f.h = 190
    f.static(lab(0, 40, 'heap: most left first', MU))
    HX, HY = 8, 54
    rows = {}
    def hrow(order, c, t, hide):
        for k, nm in enumerate(order):
            y = HY + k * 40
            f.show(box(HX, y, nm, 40, 32) + R(HX + 50, y + 8, c[nm] * 30, 16, it('.18'), TG, 3, 1) + T(HX + 56 + c[nm] * 30, y + 21, str(c[nm]), TX, 'start', mono=True), t, hide=hide)
    c = dict(cnt); t = .3; slots = []
    TX0, TY = 250, 80; SW = 52
    f.show(chip(TX0, 22, 'goal: fewest slots'), .9)
    t = 1.8; SY = 172
    rnd = 0
    while any(c.values()):
        rnd += 1
        order = sorted([k for k in c if c[k]], key=lambda k: -c[k])
        hrow(order, c, t, t + 2.4)
        take = order[:nidle + 1]
        f.show(ring(HX, HY, 40, 40 * len(take) - 8, 6), t + .4, hide=t + 2.2)
        rest = sum(c.values()) - len(take)
        pad = (nidle + 1 - len(take)) if rest else 0
        f.show(st(TX0, SY, 'round %d: take %s%s' % (rnd, ' '.join(take), ' + %d idle' % pad if pad else ''), TX), t + .4, hide=t + 2.2)
        for k, nm in enumerate(take + ['idle'] * pad):
            sx = TX0 + len(slots) * (SW + 4)
            f.show(box(sx, TY, nm, SW, 34, 'b' if nm != 'idle' else 'g', True) + idx(sx + SW / 2, TY + 50, len(slots) + 1), t + 1.0 + k * .2)
            slots.append(nm)
        for nm in take: c[nm] -= 1
        t += 2.6
    f.show(st(HX, HY + 20, '(empty)', GH), t)
    assert len(slots) == 7
    for k, nm in enumerate(slots):
        if nm != 'idle': f.show(box(TX0 + k * (SW + 4), TY, nm, SW, 34, 'f', True), t + k * .05)
    f.show(st(TX0 + 7 * (SW + 4) + 4, TY + 22, '✓ 7', TG, True), t + .4)
    f.show(lab(TX0, SY, 'A B C · A B idle · A = 7 slots · heap pop/push O(log k) each', TG, bold=True), t + .6)
    return f.render()
figs['q5'] = tasks()

os.makedirs('/tmp/dsa', exist_ok=True)
json.dump(pad(figs), open('/tmp/dsa/greedy.json', 'w'))
print({k: len(v) for k, v in figs.items()})
