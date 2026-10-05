"""Figures for content/01-dsa/04-algorithms/dynamic-programming. Writes /tmp/dsa/dynamic-programming.json."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from algo4 import *
from backtracking import Tree  # noqa  (decision-tree layout)

figs = {}

class Table:
    """dp table drawn as cells; fill(): ring the cell, arrows from the cells it reads, formula, value appears."""
    def __init__(s, f, x0, y0, rows, cols, w=40, h=34, g=6):
        s.f, s.x0, s.y0, s.rows, s.cols, s.w, s.h, s.g = f, x0, y0, rows, cols, w, h, g
    def xy(s, r, c): return s.x0 + c * (s.w + s.g), s.y0 + r * (s.h + s.g)
    def ctr(s, r, c):
        x, y = s.xy(r, c); return x + s.w / 2, y + s.h / 2
    def empty(s, t=.2, skip=()):
        for r in range(s.rows):
            for c in range(s.cols):
                if (r, c) in skip: continue
                x, y = s.xy(r, c); s.f.show(R(x, y, s.w, s.h, 'var(--bg)', RULE_HI, 5, 1.2), t + (r * s.cols + c) * .015)
    def val(s, r, c, v, t, kind='n'):
        x, y = s.xy(r, c); s.f.show(box(x, y, v, s.w, s.h, kind, True), t)
    def arrow_from(s, src, dst):
        (x1, y1), (x2, y2) = s.ctr(*src), s.ctr(*dst)
        if src[0] == dst[0] and getattr(s, 'arcs', False):   # same row: arc over (or under) the row
            dn = s.arcs == 'below'; sg = 1 if dn else -1
            top = s.xy(*src)[1] + (s.h + 2 if dn else -2); h = 10 + abs(dst[1] - src[1]) * 7
            ax, bx = x1 + (6 if x2 > x1 else -6), x2 - (6 if x2 > x1 else -6)
            mx = (ax + bx) / 2; qy = top + sg * h * 2
            ang = math.atan2(top - qy, bx - mx)
            hx, hy = bx - 6 * math.cos(ang), top - 6 * math.sin(ang)
            w = 3
            return ('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="1.8"/>' % (ax, top, mx, qy, hx, hy, MID) +
                    '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>' % (bx, top, hx - w * math.sin(ang), hy + w * math.cos(ang), hx + w * math.sin(ang), hy - w * math.cos(ang), MID))
        a = math.atan2(y2 - y1, x2 - x1)
        # leave the source box edge, stop at the dest box edge
        def edge_pt(x, y, a, out):
            dx, dy = math.cos(a), math.sin(a)
            k = min((s.w / 2 + 1) / abs(dx) if dx else 1e9, (s.h / 2 + 1) / abs(dy) if dy else 1e9)
            return (x + dx * k, y + dy * k) if out else (x - dx * k, y - dy * k)
        ax, ay = edge_pt(x1, y1, a, True); bx, by = edge_pt(x2, y2, a, False)
        if math.hypot(bx - ax, by - ay) < 8:  # adjacent: short arrow still visible
            pass
        return arrow(ax, ay, bx, by, MID, 1.8, None, 6)
    def fill(s, r, c, v, reads, t, d=1.6, text=None, sx=0, sy=0, kind='b'):
        x, y = s.xy(r, c)
        s.f.show(ring(x, y, s.w, s.h, 7), t, hide=t + d - .4)
        if reads: s.f.show(''.join(s.arrow_from(p, (r, c)) for p in reads), t + .15, hide=t + d - .4)
        if text: s.f.show(st(sx, sy, text, TX), t, hide=t + d - .4)
        s.val(r, c, v, t + d * .5, kind)
        return t + d

# ---------------------------------------------------------------- 1.1 overlapping subproblems (fib 5)
def overlap():
    f = Anim('dp-m1-', 760, 360, 'Plain recursion for fib(5) builds a tree of 15 calls; fib(3) is computed twice, fib(2) three times. '
             'With a memo, each fib(k) is computed once and later calls just read it: 6 values.', 'SAME QUESTION, ASKED AGAIN · fib(5)', 3.2)
    tr = Tree(30, 70, 44, 58, 17)
    cnt = [0]
    def build(nid, k, parent):
        tr.add(nid, parent, 'f%d' % k)
        if k >= 2: build(nid + 'L', k - 1, nid); build(nid + 'R', k - 2, nid)
    build('r', 5, None); tr.layout('r')
    order = []
    def dfs(n):
        order.append(n)
        for k in tr.kids[n]: dfs(k)
    dfs('r')
    f.show(chip(30, 22, 'goal: fib(5)'), .4)
    t = 1.2
    for k, n in enumerate(order):
        if n != 'r': f.show(tr.edge(n), t + k * .18)
        f.show(tr.node(n, 'n'), t + k * .18)
    t += len(order) * .18 + .6
    f.show(st(30, 340, '%d calls without memo' % len(order), PT, True), t, hide=t + 1.6)
    # highlight repeats
    seen = set(); first = {}
    MX = 520
    f.show(T(MX + 64, 46, 'memo', MU, cls='sv-s', bold=True), t)
    for k in range(6):
        f.show(R(MX + 44 + 0, 56 + k * 40, 40, 32, 'var(--bg)', RULE_HI, 5, 1.2) + T(MX + 30, 56 + k * 40 + 21, 'f%d' % k, FA, 'end', cls='sv-s', mono=True), t)
    t += 1.8
    fibv = [0, 1, 1, 2, 3, 5]
    # post-order compute: first time a value is finished it goes into memo; repeats grey out
    post = []
    def po(n):
        for k in tr.kids[n]: po(k)
        post.append(n)
    po('r')
    repeats = 0
    done = set()
    def skip_sub(n):
        for k in tr.kids[n]: skip_sub(k); f.show(tr.node(k, 'g'), tt[0])
    tt = [t]
    def walk(n):
        k = int(tr.lab[n][1:])
        if k in done:
            nonlocal repeats
            repeats += 1
            f.show(nring(*tr.pos[n], 17), tt[0], hide=tt[0] + 1.0)
            f.show(st(30, 340, 'f%d again → read the memo, skip its subtree' % k, TX), tt[0], hide=tt[0] + 1.0)
            f.show(tr.node(n, 'v'), tt[0] + .3)
            for c in tr.kids[n]:
                f.show(tr.edge(c, 'var(--rule)', 1), tt[0] + .5)
                skip_sub(c); f.show(tr.node(c, 'g'), tt[0] + .5)
            tt[0] += 1.2
            return
        for c in tr.kids[n]: walk(c)
        done.add(k)
        f.show(tr.node(n, 'b'), tt[0])
        f.show(box(MX + 44, 56 + k * 40, fibv[k], 40, 32, 'b', True), tt[0] + .2)
        tt[0] += .5
    walk('r')
    t = tt[0] + .3
    f.show(tr.node('r', 'f'), t)
    f.show(box(MX + 44, 56 + 5 * 40, 5, 40, 32, 'f', True), t)
    f.show(lab(30, 340, '✓ fib(5) = 5 · 6 values computed once instead of %d calls' % len(order), TG, bold=True), t + .4)
    assert len(order) == 15
    return f.render()
figs['m1'] = overlap()

# ---------------------------------------------------------------- 1.2 fill the table (climbing stairs)
def stairs():
    n = 7
    lines = ['dp = [0] * (n + 1)', 'dp[0] = dp[1] = 1', 'for i in range(2, n + 1):', '    dp[i] = dp[i-1] + dp[i-2]', 'return dp[n]']
    code = Code2(0, 40, lines)
    X0 = code.w + 40
    f = Anim('dp-m2-', 760, 0, 'Climbing stairs with steps of 1 or 2: dp[i] = ways to reach step i. dp[0] = dp[1] = 1. Each cell adds the two cells before it: 1 1 2 3 5 8 13 21.',
             'FILL THE TABLE · dp[i] = WAYS TO REACH STEP i', 3.2)
    f.static(code.svg())
    Tb = Table(f, X0, 100, 1, n + 1, 44, 36, 8); Tb.arcs = True
    Tb.empty(.3)
    for c in range(n + 1): f.show(idx(Tb.ctr(0, c)[0], 100 + 52, c), .3)
    f.show(goal_ring(*Tb.xy(0, n), 44, 36), 1.0)
    gx = Tb.xy(0, n)[0]
    f.path(chip(gx - 40, 60, 'dp[7] = ?'), [(0, 0, 0), (2.0, X0 - gx + 40, 24 - 60)], 1.0)
    t = 3.0; bar = [(t, 0)]; dp = [1, 1]
    SY = 190
    bar.append((t + .5, 1))
    Tb.val(0, 0, 1, t + .7, 'b'); Tb.val(0, 1, 1, t + .7, 'b')
    f.show(st(X0, SY, 'base: dp[0] = dp[1] = 1', PT, True), t + .5, hide=t + 1.6); t += 1.8
    ip = None
    for i in range(2, n + 1):
        dp.append(dp[i - 1] + dp[i - 2])
        bar.append((t, 2)); bar.append((t + .3, 3))
        d = 2.0 if i < 5 else 1.2
        t = Tb.fill(0, i, dp[i], [(0, i - 1), (0, i - 2)], t + .2, d, 'dp[%d] = dp[%d] + dp[%d] = %d + %d = %d' % (i, i - 1, i - 2, dp[i - 1], dp[i - 2], dp[i]), X0, SY)
    # arrows between adjacent cells arc above
    bar.append((t, 4)); end = t + .3
    code.run(f, bar)
    Tb.val(0, n, dp[n], end, 'f')
    f.show(T(Tb.ctr(0, n)[0], 100 + 70, '✓ found', TG, mono=True, bold=True), end + .3)
    f.show(lab(X0, SY, 'dp[7] = 21 · each cell once, O(1) work → O(n)', TG, bold=True), end + .5)
    assert dp[n] == 21
    f.h = max(code.y + code.h(), SY + 12) + 6
    return f.render()
figs['m2'] = stairs()

# ---------------------------------------------------------------- 1.3 cost: calls without vs with memo
def cost():
    f = Anim('dp-m3-', 760, 330, 'Calls needed for fib(n). Plain recursion grows like 1.6 to the n: 177 calls at n = 10, 21,891 at n = 20. '
             'With memo or a table it is n + 1 cells. DP cost = number of states × work per state.', 'COST · CELLS × WORK PER CELL', 3)
    gx, gy, gw, gh = 70, 50, 560, 220
    NM, YM = 20, 5
    px = lambda n: gx + n / NM * gw; py = lambda v: gy + gh - v / YM * gh
    ax = axes(gx, gy, gw, gh, (5, 10, 15, 20), (), 'n', 'calls', px, py)
    for e in range(0, 6): ax += T(gx - 8, py(e) + 4, '10' + '⁰¹²³⁴⁵'[e], FA, 'end', cls='sv-s', mono=True) + L(gx, py(e), gx + gw, py(e), 'var(--rule)', 1, '2 4')
    f.show(ax, .3)
    def calls(n):
        a = [1, 1]
        for k in range(2, n + 1): a.append(a[-1] + a[-2] + 1)
        return a[n]
    plain = [(n, math.log10(calls(n))) for n in range(1, 21)]
    memo = [(n, math.log10(n + 1)) for n in range(1, 21)]
    t = 1.2
    f.show(poly([(px(n), py(v)) for n, v in plain], GH, 2.4) + lab(px(20) + 6, py(plain[-1][1]) + 4, 'plain', MU, bold=True), t, d=.8)
    t += 1.4
    f.show(poly([(px(n), py(v)) for n, v in memo], TG, 2.6) + lab(px(20) + 6, py(memo[-1][1]) + 4, 'memo', TG, bold=True), t, d=.8)
    t += 1.2
    for k, n in enumerate((10, 20)):
        f.show(dot(px(n), py(math.log10(calls(n))), MID) + dot(px(n), py(math.log10(n + 1)), MID), t + k * .4)
    assert calls(10) == 177 and calls(20) == 21891
    f.show(st(px(10) - 6, py(math.log10(177)) - 10, '177', MID, True, 'end') + st(px(20) - 6, py(math.log10(21891)) - 10, '21,891', MID, True, 'end') +
           st(px(10), py(math.log10(11)) + 20, '11', MID, True) + st(px(20), py(math.log10(21)) + 20, '21', MID, True), t + 1.0)
    f.show(lab(gx + gw, gy + gh + 40, 'log scale · DP cost = number of cells × work per cell', TG, 'end', True), t + 1.6)
    return f.render()
figs['m3'] = cost()

# ---------------------------------------------------------------- 2.1 take or skip (house robber)
def robber():
    a = [2, 7, 9, 3, 1]; n = len(a)
    lines = ['dp[0], dp[1] = a[0], max(a[0], a[1])', 'for i in range(2, n):', '    dp[i] = max(dp[i-1],', '                dp[i-2] + a[i])', 'return dp[n-1]']
    code = Code2(0, 40, lines)
    X0 = code.w + 70
    f = Anim('dp-q1-', 760, 0, 'House robber on 2 7 9 3 1, no two neighbours. dp[i] = best loot up to house i = max(skip: dp[i-1], take: dp[i-2] + a[i]). '
             'Row fills 2 7 11 11 12; answer 12.', 'TAKE OR SKIP · HOUSES 2 7 9 3 1, NO TWO NEIGHBOURS', 3.2)
    f.static(code.svg())
    A = Tb0 = Table(f, X0, 80, 1, n, 48, 34, 10)
    Tb = Table(f, X0, 140, 1, n, 48, 34, 10); Tb.arcs = 'below'
    f.static(lab(X0 - 12, 101, 'a', MU, 'end') + lab(X0 - 12, 161, 'dp', MU, 'end'))
    for c in range(n): f.show(box(*A.xy(0, c), a[c], 48, 34, 'n', True) + idx(A.ctr(0, c)[0], 72, c), .3 + c * .05)
    Tb.empty(.6)
    f.show(chip(X0, 22, 'goal: most loot'), 1.0)
    dp = [a[0], max(a[0], a[1])]
    t = 2.2; SY = 262; bar = [(t, 0)]
    Tb.val(0, 0, dp[0], t + .3, 'b'); Tb.val(0, 1, dp[1], t + .5, 'b')
    f.show(st(X0, SY, 'dp[0] = 2 · dp[1] = max(2, 7) = 7', PT, True), t, hide=t + 1.4); t += 1.6
    for i in range(2, n):
        skip, take = dp[i - 1], dp[i - 2] + a[i]; dp.append(max(skip, take))
        bar += [(t, 1), (t + .3, 2)]
        x, y = A.xy(0, i)
        f.show(ring(x, y, 48, 34, 7), t + .2, hide=t + 2.2)
        t = Tb.fill(0, i, dp[i], [(0, i - 1), (0, i - 2)], t + .2, 2.2,
                    'max(skip %d, take %d + %d = %d) = %d' % (skip, dp[i - 2], a[i], take, dp[i]), X0, SY)
    bar.append((t, 4)); end = t + .3
    code.run(f, bar)
    Tb.val(0, n - 1, dp[-1], end, 'f')
    f.show(T(Tb.ctr(0, n - 1)[0], 140 + 52, '✓ found', TG, mono=True, bold=True), end + .3)
    f.show(lab(X0, SY + 6, 'best = 12 (2 + 9 + 1) · O(n) time', TG, bold=True), end + .5)
    assert dp == [2, 7, 11, 11, 12]
    f.h = max(code.y + code.h(), SY + 16) + 6
    return f.render()
figs['q1'] = robber()

# ---------------------------------------------------------------- 2.2 knapsack (coin change)
def coins():
    cs = [1, 3, 4]; A_ = 6
    lines = ['dp = [0] + [inf] * amount', 'for x in range(1, amount + 1):', '    for c in coins:', '        if c <= x:', '            dp[x] = min(dp[x], dp[x-c] + 1)', 'return dp[amount]']
    code = Code2(0, 40, lines)
    X0 = code.w + 40
    f = Anim('dp-q2-', 760, 0, 'Coin change for 6 with coins 1 3 4. dp[x] = fewest coins for amount x = 1 + min of dp[x−c] over each coin c. '
             'Fills 0 1 2 1 1 2 2: amount 6 needs 2 coins (3 + 3), where greedy needed 3.', 'KNAPSACK · FEWEST COINS FOR 6 · COINS 1 3 4', 3.2)
    f.static(code.svg())
    Tb = Table(f, X0, 100, 1, A_ + 1, 44, 36, 8); Tb.arcs = True
    Tb.empty(.3)
    for c in range(A_ + 1): f.show(idx(Tb.ctr(0, c)[0], 152, c), .3)
    f.show(goal_ring(*Tb.xy(0, A_), 44, 36), 1.0)
    gx = Tb.xy(0, A_)[0]
    f.path(chip(gx - 40, 60, 'dp[6] = ?'), [(0, 0, 0), (2.0, X0 - gx + 40, 24 - 60)], 1.0)
    dp = [0] + [None] * A_
    t = 3.0; SY = 200; bar = [(t, 0)]
    Tb.val(0, 0, 0, t + .3, 'b'); t += 1.0
    for x in range(1, A_ + 1):
        opts = [(dp[x - c] + 1, c) for c in cs if c <= x]
        best = min(opts); dp[x] = best[0]
        bar += [(t, 1), (t + .3, 2), (t + .5, 3), (t + .7, 4)]
        d = 2.2 if x in (3, 6) or x == 1 else 1.3
        text = 'dp[%d] = 1 + min(%s) = %d' % (x, ', '.join('dp[%d]' % (x - c) for c in cs if c <= x), dp[x])
        t = Tb.fill(0, x, dp[x], [(0, x - c) for c in cs if c <= x], t + .1, d, text, X0, SY)
    bar.append((t, 5)); end = t + .3
    code.run(f, bar)
    Tb.val(0, A_, 2, end, 'f')
    f.show(T(Tb.ctr(0, A_)[0], 172, '✓ found', TG, mono=True, bold=True), end + .3)
    f.show(lab(X0, SY + 6, '6 = 3 + 3 → 2 coins · amount × coins cells of work', TG, bold=True), end + .5)
    assert dp == [0, 1, 2, 1, 1, 2, 2]
    f.h = max(code.y + code.h(), SY + 16) + 6
    return f.render()
figs['q2'] = coins()

# ---------------------------------------------------------------- 2.3 two strings (LCS)
def lcs():
    A, B = 'ACE', 'ABCDE'
    f = Anim('dp-q3-', 760, 330, 'Longest common subsequence of ACE and ABCDE. Table rows are letters of ACE, columns letters of ABCDE, with a zero row and column. '
             'Equal letters take the diagonal + 1, otherwise the max of up and left. Bottom-right = 3.', 'TWO STRINGS · LCS OF "ACE" AND "ABCDE"', 3.2); f.h = 300
    R_, C_ = len(A) + 1, len(B) + 1
    Tb = Table(f, 70, 80, R_, C_, 40, 32, 20)
    for c in range(C_):
        f.static(T(Tb.ctr(0, c)[0], 70, '·' if c == 0 else B[c - 1], MU, mono=True, bold=True))
    for r in range(R_):
        f.static(T(52, Tb.ctr(r, 0)[1] + 4, '·' if r == 0 else A[r - 1], MU, mono=True, bold=True))
    Tb.empty(.3)
    f.show(goal_ring(*Tb.xy(R_ - 1, C_ - 1), 40, 32), 1.0)
    gx, gy = Tb.xy(R_ - 1, C_ - 1)
    f.path(chip(gx - 30, gy + 44, 'LCS = ?'), [(0, 0, 0), (2.0, 70 - gx + 30, 22 - gy - 44)], 1.0)
    dp = [[0] * C_ for _ in range(R_)]
    t = 3.0; SX, SY = 460, 110
    for c in range(C_): Tb.val(0, c, 0, t + c * .05, 'b')
    for r in range(1, R_): Tb.val(r, 0, 0, t + .3 + r * .05, 'b')
    f.show(st(SX, SY, 'empty prefix → 0', PT, True), t, hide=t + 1.2); t += 1.4
    for r in range(1, R_):
        for c in range(1, C_):
            if A[r - 1] == B[c - 1]:
                dp[r][c] = dp[r - 1][c - 1] + 1; reads = [(r - 1, c - 1)]
                txt = '%s = %s → diagonal + 1 = %d' % (A[r - 1], B[c - 1], dp[r][c])
            else:
                dp[r][c] = max(dp[r - 1][c], dp[r][c - 1]); reads = [(r - 1, c), (r, c - 1)]
                txt = '%s ≠ %s → max(up %d, left %d) = %d' % (A[r - 1], B[c - 1], dp[r - 1][c], dp[r][c - 1], dp[r][c])
            d = 1.9 if r == 1 else 1.0
            t = Tb.fill(r, c, dp[r][c], reads, t, d, txt, SX, SY)
    end = t + .2
    assert dp[-1][-1] == 3
    Tb.val(R_ - 1, C_ - 1, 3, end, 'f')
    f.show(lab(SX, SY, '✓ LCS = 3 ("ACE") · (n+1)(m+1) cells, O(1) each', TG, bold=True), end + .3)
    return f.render()
figs['q3'] = lcs()

# ---------------------------------------------------------------- 2.4 grid (unique paths)
def paths():
    R_, C_ = 3, 5
    f = Anim('dp-q4-', 760, 230, 'Unique paths in a 3 by 5 grid moving only right or down. Top row and left column are 1. Every other cell = cell above + cell left. Bottom-right = 15.',
             'GRID · PATHS MOVING ONLY RIGHT OR DOWN · 3 × 5', 3.2); f.h = 240
    Tb = Table(f, 40, 56, R_, C_, 50, 38, 22)
    Tb.empty(.3)
    f.show(goal_ring(*Tb.xy(R_ - 1, C_ - 1), 50, 38), 1.0)
    SX, SY = 440, 90
    f.show(chip(SX, 22, 'goal: paths to bottom-right'), 1.2)
    t = 2.4; dp = [[1] * C_ for _ in range(R_)]
    for c in range(C_): Tb.val(0, c, 1, t + c * .06, 'b')
    for r in range(1, R_): Tb.val(r, 0, 1, t + .3 + r * .06, 'b')
    f.show(st(SX, SY, 'first row / column: one way → 1', PT, True), t, hide=t + 1.3); t += 1.5
    for r in range(1, R_):
        for c in range(1, C_):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
            d = 2.0 if r == 1 and c < 3 else 1.1
            t = Tb.fill(r, c, dp[r][c], [(r - 1, c), (r, c - 1)], t, d, 'up %d + left %d = %d' % (dp[r - 1][c], dp[r][c - 1], dp[r][c]), SX, SY)
    end = t + .2
    assert dp[-1][-1] == 15
    Tb.val(R_ - 1, C_ - 1, 15, end, 'f')
    f.show(lab(SX, SY, '✓ 15 paths · each cell = up + left', TG, bold=True), end + .3)
    return f.render()
figs['q4'] = paths()

# ---------------------------------------------------------------- 2.5 subsequence (LIS)
def lis():
    a = [2, 5, 3, 7, 4, 8]; n = len(a)
    f = Anim('dp-q5-', 760, 250, 'Longest increasing subsequence of 2 5 3 7 4 8. dp[i] = longest one ending at i = 1 + max dp[j] over earlier j with a[j] < a[i]. '
             'Fills 1 2 2 3 3 4; answer 4, e.g. 2 3 7 8.', 'SUBSEQUENCE · LONGEST INCREASING · 2 5 3 7 4 8', 3.2); f.h = 284
    X0 = 60
    A = Table(f, X0, 70, 1, n, 50, 34, 14); Tb = Table(f, X0, 150, 1, n, 50, 34, 14); Tb.arcs = 'below'
    f.static(lab(X0 - 12, 91, 'a', MU, 'end') + lab(X0 - 12, 171, 'dp', MU, 'end'))
    for c in range(n): f.show(box(*A.xy(0, c), a[c], 50, 34, 'n', True) + idx(A.ctr(0, c)[0], 62, c), .3 + c * .05)
    Tb.empty(.6)
    f.show(chip(X0, 22, 'goal: longest increasing run (gaps allowed)'), 1.0)
    dp = []; t = 2.4; SY = 270
    for i in range(n):
        js = [j for j in range(i) if a[j] < a[i]]
        dp.append(1 + max([dp[j] for j in js], default=0))
        x, y = A.xy(0, i)
        d = 2.2 if i in (1, 3, 5) else 1.6
        f.show(ring(x, y, 50, 34, 7), t, hide=t + d - .4)
        for j in js: f.show(R(*A.xy(0, j), 50, 34, vt('.10'), MID, 6, 1.4), t + .15, hide=t + d - .4)
        txt = ('a[%d] = %d · smaller before it: %s → 1 + %d = %d' % (i, a[i], ' '.join(str(a[j]) for j in js), max(dp[j] for j in js), dp[i])) if js else 'a[%d] = %d · nothing smaller before it → 1' % (i, a[i])
        t = Tb.fill(0, i, dp[i], [(0, j) for j in js if dp[j] == dp[i] - 1][:2], t, d, txt, X0, SY)
    end = t + .2
    assert dp == [1, 2, 2, 3, 3, 4]
    Tb.val(0, n - 1, 4, end, 'f')
    f.show(T(Tb.ctr(0, n - 1)[0], 150 + 52, '✓ found', TG, mono=True, bold=True), end + .3)
    f.show(lab(X0, SY, '✓ LIS = 4 (2 3 7 8) · n² pairs checked → O(n²)', TG, bold=True), end + .3)
    return f.render()
figs['q5'] = lis()

os.makedirs('/tmp/dsa', exist_ok=True)
json.dump(pad(figs), open('/tmp/dsa/dynamic-programming.json', 'w'))
print({k: len(v) for k, v in figs.items()})
