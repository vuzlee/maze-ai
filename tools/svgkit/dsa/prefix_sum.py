"""Prefix sum lesson figures. Uses arrkit.py (shared, do not edit). Writes /tmp/dsa/prefix-sum.json."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arrkit import *  # noqa

figs = {}
def cellx(x, y, v, kind='n', w=CW, h=CH): return box(x, y, v, kind, w, h)

# ---------- m1: build the prefix row -------------------------------------------------
A = [3, 1, 4, 1, 5, 2]; PRE = [0]
for x in A: PRE.append(PRE[-1] + x)
def build_fig():
    code = Code2(0, 40, ['pre = [0] * (n + 1)', 'for i in range(n):', '    pre[i+1] = pre[i] + a[i]'], 250)
    X0 = 290; W = X0 + 7 * P + 20
    f = Anim('m1-', W, 300, 'Array 3 1 4 1 5 2. The prefix row starts as seven zeros; each step adds a[i] to pre[i] and writes it into pre[i+1], ending with pre = 0 3 4 8 9 14 16.', 'BUILD THE RUNNING TOTAL · ONE PASS')
    f.static(code.svg())
    a = Row(X0 + P / 2, 90, A); p = Row(X0, 170, [0] * 7)
    f.show(lab(X0 - 8, 113, 'a', MU, 'end', True), .2); f.show(lab(X0 - 8, 193, 'pre', MU, 'end', True), .2)
    a.draw(f, .2); p.draw(f, .6)
    f.show(chip(X0, 22, 'pre[i] = sum of a[0..i-1]'), 1.2)
    code.at(1.0, 0); t = 2.0
    ip = Ptr(a, 'i', 0, up=True)
    seq = []
    for i, x in enumerate(A):
        code.at(t, 1); code.at(t + .6, 2)
        if i: ip.to(t, i)
        seq.append((t + .6, st(X0, 270, 'pre[%d] = pre[%d] + a[%d] = %d + %d = %d' % (i + 1, i, i, PRE[i], x, PRE[i + 1]), MID)))
        f.show(a.ring(i) + p.ring(i), t + .6, hide=t + 2.0)
        f.show(p.cell(i + 1, 'f' if i == len(A) - 1 else 'b', PRE[i + 1]), t + 1.3)
        t += 2.2
    seq.append((t, st(X0, 270, '✓ pre[6] = 16 = sum of all · 6 additions for 6 cells', TG, True)))
    states(f, seq); ip.emit(f, 1.6); code.emit(f)
    return f.render()
figs['m1'] = build_fig()

# ---------- m2: cost, concrete then graph ------------------------------------------
def cost_fig():
    W = 760; f = Anim('m2-', W, 330, 'Answering q range sums on 6 cells: a loop costs up to 6 additions per query, so 6q in total; the prefix row costs 6 once plus 1 subtraction per query. The graph draws 6q as a steep line and 6 + q as a nearly flat one.', 'COST OF q QUERIES ON n = 6 CELLS')
    gx, gy, gw, gh = 70, 60, 520, 210
    px = lambda q: gx + q * gw / 10; py = lambda w: gy + gh - w * gh / 60
    f.show(axes(gx, gy, gw, gh, [0, 2, 4, 6, 8, 10], [0, 20, 40, 60], 'q', 'work', px, py), .2)
    f.show(poly([(px(0), py(0)), (px(10), py(60))], GH, 2.2) + lab(px(10) - 6, py(60) + 18, 'loop: n · q', MU, 'end', True), 1.0, d=.8)
    f.show(poly([(px(0), py(6)), (px(10), py(16))], TG, 2.8) + lab(px(10), py(16) - 10, 'prefix: n + q', TG, 'end', True), 2.2, d=.8)
    for k, q in enumerate((2, 4, 6, 8, 10)):
        f.show(dot(px(q), py(6 * q), MID) + dot(px(q), py(6 + q), TG), 3.4 + k * .3)
    f.show(st(px(10) + 12, py(60) + 4, '60', MID, True) + st(px(10) + 12, py(16) + 4, '16', TG, True), 5.0)
    f.show(st(gx, gy + gh + 46, 'build O(n) once · then each query O(1)', TG, True), 5.6)
    return f.render()
figs['m2'] = cost_fig()

# ---------- q1: range sum query ----------------------------------------------------
def query_fig():
    code = Code2(0, 40, ['def query(l, r):', '    return pre[r+1] - pre[l]'], 250)
    X0 = 290; W = X0 + 7 * P + 20
    f = Anim('q1-', W, 312, 'Array 3 1 4 1 5 2 with its prefix row. Query l = 1, r = 3: pre[4] = 9 minus pre[1] = 3 gives 6. Query l = 2, r = 5: pre[6] = 16 minus pre[2] = 4 gives 12.', 'RANGE SUM = TWO CELLS SUBTRACTED')
    f.static(code.svg())
    a = Row(X0 + P / 2, 80, A); p = Row(X0, 170, PRE)
    f.show(lab(X0 - 8, 103, 'a', MU, 'end', True) + lab(X0 - 8, 193, 'pre', MU, 'end', True), .2)
    a.draw(f, .2); p.draw(f, .5)
    t = 1.4
    for k, (l, r) in enumerate([(1, 3), (2, 5)]):
        end = t + 6.0 if k == 0 else None
        ans = PRE[r + 1] - PRE[l]
        f.show(a.goal(l, r), t, hide=end)
        f.show(chip(X0, 22, 'sum a[%d..%d]' % (l, r)), t, hide=end)
        lp = Ptr(a, 'l', l, up=True); rp = Ptr(a, 'r', r, up=True)
        lp.emit(f, t + .5, hide=end); rp.emit(f, t + .5, hide=end)
        code.at(t + 1.0, 0) if k == 0 else None; code.at(t + 1.6, 1)
        f.show(p.ring(r + 1) + p.ring(l), t + 1.6, hide=end)
        f.show(st(X0, 270, 'pre[%d] - pre[%d] = %d - %d = %d' % (r + 1, l, PRE[r + 1], PRE[l], ans), MID), t + 1.6, hide=end)
        for i in range(len(A)):
            if not l <= i <= r: f.show(a.cell(i, 'g'), t + 2.6, hide=end)
        for i in range(l, r + 1): f.show(a.cell(i, 'f'), t + 3.4, hide=end)
        f.show(st(X0, 294, '✓ %d · 1 subtraction' % ans, TG, True), t + 3.4, hide=end)
        t += 6.4
    code.emit(f)
    return f.render()
figs['q1'] = query_fig()

# ---------- q2: prefix + hash map ---------------------------------------------------
def hash_fig():
    B = [2, -1, 1, 2]; K = 2
    code = Code2(0, 40, ['seen = {0: 1}', 's = ans = 0', 'for x in a:', '    s += x', '    ans += seen.get(s - k, 0)', '    seen[s] = seen.get(s, 0) + 1'], 280)
    X0 = 320; W = 780
    f = Anim('q2-', W, 330, 'Array 2 -1 1 2, k = 2. Running sums 2 1 2 4. At each step the map is asked how many earlier sums equal s - k: 1, 0, 1, 2. Total 4 subarrays sum to 2.', 'COUNT SUBARRAYS WITH SUM k = 2 · NEGATIVES ALLOWED')
    f.static(code.svg())
    a = Row(X0, 70, B); a.draw(f, .2)
    f.show(lab(X0 - 8, 93, 'a', MU, 'end', True), .2)
    f.show(chip(X0, 22, 'count, sum = 2'), .8)
    MY = 190; keys = [0, 2, 1, 4]
    kx = lambda j: X0 + j * (CW + 20)
    f.show(lab(X0 - 8, MY + 23, 'sum', MU, 'end', True) + lab(X0 - 8, MY + 63, 'count', MU, 'end', True), 1.0)
    def entry(j, c, kind='n', t=0, hide=None):
        f.show(box(kx(j), MY, keys[j], kind) + box(kx(j), MY + 40, c, kind), t, hide=hide)
    code.at(1.0, 0); entry(0, 1, 'n', 1.0); code.at(1.6, 1)
    ip = Ptr(a, 'i', 0); seen = {0: 1}; s = ans = 0; t = 2.4; seq = []
    for i, x in enumerate(B):
        code.at(t, 2); code.at(t + .4, 3)
        if i: ip.to(t, i)
        f.show(a.ring(i), t + .4, hide=t + 3.0)
        s0 = s; s += x; need = s - K; c = seen.get(need, 0)
        seq.append((t + .4, st(X0, 300, 's = %d + %d = %d · need s - k = %d' % (s0, x, s, need), MID)))
        code.at(t + 1.2, 4)
        if c:
            j = keys.index(need)
            f.show(ring(kx(j), MY, CW, 76), t + 1.2, hide=t + 2.2)
        ans += c
        f.show(st(X0 + 270, 300, ('seen %d × %d → ans = %d' % (need, c, ans)) if c else 'no %d yet → ans = %d' % (need, ans), TX), t + 1.2, hide=t + 2.95)
        code.at(t + 2.2, 5)
        seen[s] = seen.get(s, 0) + 1
        entry(keys.index(s), seen[s], 'b', t + 2.2)
        t += 3.2
    seq.append((t, st(X0, 300, '✓ ans = 4 subarrays: [2] [2,-1,1] [-1,1,2] [2]', TG, True)))
    states(f, seq); ip.emit(f, 2.0); code.emit(f)
    return f.render()
figs['q2'] = hash_fig()

# ---------- q3: 2D rectangle -------------------------------------------------------
def grid_fig():
    G2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Pt = [[0] * 4 for _ in range(4)]
    for r in range(3):
        for c in range(3): Pt[r + 1][c + 1] = G2[r][c] + Pt[r][c + 1] + Pt[r + 1][c] - Pt[r][c]
    W = 720; f = Anim('q3-', W, 340, '3 by 3 grid 1 to 9; target rectangle rows 1-2, columns 1-2. From the prefix table: 45 whole block, minus 6 above, minus 12 left, plus 1 for the corner removed twice, gives 28.', 'RECTANGLE SUM = FOUR CORNERS OF THE 2D PREFIX TABLE')
    gx0, py0 = 40, 300; Y = 118
    gc = lambda r, c: (gx0 + c * P, Y + r * P)
    pc = lambda r, c: (py0 + c * P, Y - P + r * P)
    f.show(lab(gx0, Y - 16, 'grid', MU, 'start', True) + lab(py0 + P, Y - P - 16 + P - 0, '', MU), .1)
    for r in range(3):
        for c in range(3):
            x, y = gc(r, c); f.show(box(x, y, G2[r][c]), .2 + (r * 3 + c) * .05)
    f.show(lab(py0, Y - P - 14, 'P[r][c] = sum of the block above-left', MU, 'start', True), .9)
    for r in range(4):
        for c in range(4):
            x, y = pc(r, c); f.show(box(x, y, Pt[r][c]), .9 + (r * 4 + c) * .04)
    x, y = gc(1, 1); f.show(goal_ring(x, y, CW + P, CH + P), 1.8)
    f.show(chip(gx0, 260, 'sum rows 1-2, cols 1-2'), 1.8)
    steps = [((3, 3), '+ P[3][3] = 45 · the whole block', []),
             ((1, 3), '- P[1][3] = 6 · strip above', [(0, 0), (0, 1), (0, 2)]),
             ((3, 1), '- P[3][1] = 12 · strip left', [(1, 0), (2, 0)]),
             ((1, 1), '+ P[1][1] = 1 · corner removed twice', [])]
    t = 2.8; tot = 0; seq = []
    for k, ((r, c), txt, grey_) in enumerate(steps):
        x, y = pc(r, c)
        f.show(ring(x, y), t, hide=t + 1.9)
        tot += Pt[r][c] * (1 if txt[0] == '+' else -1)
        seq.append((t, st(py0, 310, txt + ' → %d' % tot, MID)))
        for (gr, gcn) in grey_:
            gxx, gyy = gc(gr, gcn); f.show(box(gxx, gyy, G2[gr][gcn], 'g'), t + .8)
        t += 2.2
    for r in (1, 2):
        for c in (1, 2):
            x, y = gc(r, c); f.show(box(x, y, G2[r][c], 'f'), t)
    seq.append((t, st(py0, 310, '✓ 45 - 6 - 12 + 1 = 28 · four lookups', TG, True)))
    states(f, seq)
    return f.render()
figs['q3'] = grid_fig()

# ---------- q4: difference array ---------------------------------------------------
def diff_fig():
    code = Code2(0, 40, ['diff = [0] * (n + 1)', 'for l, r, v in ups:', '    diff[l] += v; diff[r+1] -= v', 'run = 0', 'for i in range(n):', '    run += diff[i]; res[i] = run'], 290)
    X0 = 340; W = X0 + 6 * P + 30
    f = Anim('q4-', W, 330, 'Five zero cells; add 2 to range 1..3 and 3 to range 2..4. Each update touches only two cells of diff: +2 at 1, -2 at 4, +3 at 2, -3 at 5. One running sum then gives 0 2 5 5 3.', 'ADD v TO A RANGE · TWO CELLS PER UPDATE')
    f.static(code.svg())
    d = Row(X0, 80, [0] * 6); res = Row(X0, 190, [0] * 5)
    f.show(lab(X0 - 8, 103, 'diff', MU, 'end', True) + lab(X0 - 8, 213, 'res', MU, 'end', True), .2)
    d.draw(f, .2); res.draw(f, .5)
    code.at(1.0, 0); t = 1.6; D = [0] * 6; seq = []
    for k, (l, r, v) in enumerate([(1, 3, 2), (2, 4, 3)]):
        code.at(t, 1); code.at(t + .5, 2)
        f.show(chip(X0, 22, '+%d on %d..%d' % (v, l, r)), t, hide=t + 2.6)
        f.show(res.goal(l, r), t, hide=t + 2.6)
        D[l] += v; D[r + 1] -= v
        f.show(d.ring(l) + d.ring(r + 1), t + .5, hide=t + 2.6)
        seq.append((t + .5, st(X0, 300, 'diff[%d] += %d · diff[%d] -= %d' % (l, v, r + 1, v), MID)))
        f.show(d.cell(l, 'b', D[l]) + d.cell(r + 1, 'b', D[r + 1]), t + 1.2)
        t += 3.0
    code.at(t, 3); seq.append((t, st(X0, 300, 'run = 0', PT)))
    t += .8; ip = Ptr(d, 'i', 0); run = 0
    for i in range(5):
        code.at(t, 4); code.at(t + .4, 5)
        if i: ip.to(t, i)
        run += D[i]
        f.show(d.ring(i), t + .4, hide=t + 1.6)
        seq.append((t + .4, st(X0, 300, 'run += diff[%d] = %d → res[%d] = %d' % (i, D[i], i, run), MID)))
        f.show(res.cell(i, 'f' if i == 4 else 'b', run), t + 1.0)
        t += 1.8
    seq.append((t, st(X0, 300, '✓ res = 0 2 5 5 3 · O(1) per update', TG, True)))
    states(f, seq); ip.emit(f, 8.0, hide=t); code.emit(f)
    return f.render()
figs['q4'] = diff_fig()

# ---------- q5: product except self -------------------------------------------------
def prod_fig():
    A2 = [1, 2, 3, 4]
    code = Code2(0, 40, ['ans, left = [1] * n, 1', 'for i in range(n):', '    ans[i] = left; left *= a[i]', 'right = 1', 'for i in reversed(range(n)):', '    ans[i] *= right; right *= a[i]'], 290)
    X0 = 340; W = X0 + 4 * P + 200
    f = Anim('q5-', W, 330, 'Array 1 2 3 4. Left pass writes the product of everything before i: 1 1 2 6. Right pass multiplies by the product of everything after i, giving 24 12 8 6.', 'PRODUCT OF ALL OTHERS · PREFIX FROM BOTH SIDES')
    f.static(code.svg())
    a = Row(X0, 80, A2); o = Row(X0, 190, [1] * 4)
    f.show(lab(X0 - 8, 103, 'a', MU, 'end', True) + lab(X0 - 8, 213, 'ans', MU, 'end', True), .2)
    a.draw(f, .2); o.draw(f, .5)
    f.show(chip(X0 + 4 * P + 10, 22 + 70, 'no division'), .9)
    code.at(1.0, 0); t = 1.8; seq = []; ip = Ptr(a, 'i', 0, up=True); left = 1; cur = [1] * 4
    for i in range(4):
        code.at(t, 1); code.at(t + .4, 2)
        if i: ip.to(t, i)
        cur[i] = left
        f.show(a.ring(i), t + .4, hide=t + 1.6)
        seq.append((t + .4, st(X0, 290, 'ans[%d] = left = %d · left = %d × %d = %d' % (i, left, left, A2[i], left * A2[i]), MID)))
        f.show(o.cell(i, 'b', cur[i]), t + 1.0); left *= A2[i]; t += 1.8
    code.at(t, 3); right = 1; t += .6
    for i in reversed(range(4)):
        code.at(t, 4); code.at(t + .4, 5); ip.to(t, i)
        cur[i] *= right
        f.show(a.ring(i), t + .4, hide=t + 1.6)
        seq.append((t + .4, st(X0, 290, 'ans[%d] × right %d = %d · right = %d' % (i, right, cur[i], right * A2[i]), MID)))
        f.show(o.cell(i, 'f', cur[i]), t + 1.0); right *= A2[i]; t += 1.8
    seq.append((t, st(X0, 290, '✓ ans = 24 12 8 6 · two passes, O(n)', TG, True)))
    states(f, seq); ip.emit(f, 1.6); code.emit(f)
    return f.render()
figs['q5'] = prod_fig()

json.dump(figs, open('/tmp/dsa/prefix-sum.json', 'w'))
print({k: len(v) for k, v in figs.items()})
