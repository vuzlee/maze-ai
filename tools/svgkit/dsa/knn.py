# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/05-classical-ml/knn.
Every number is computed here from the six-customer table. Run: python3 knn.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, GH, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, Plane, finish)

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/05-classical-ml/knn/index.html')

# ---------- data ----------
DATA = [('A', 24, 12, 'no', 0), ('B', 28, 22, 'no', -1), ('C', 35, 18, 'buy', 3), ('D', 41, 26, 'buy', 1),
        ('E', 52, 30, 'no', 7), ('F', 60, 34, 'buy', 2)]
X = (25, 35)
AG = [r[1] for r in DATA]; IN = [r[2] for r in DATA]
def _ms(v):
    m = sum(v) / len(v); return m, math.sqrt(sum((a - m) ** 2 for a in v) / len(v))
(MA, SA), (MI, SI) = _ms(AG), _ms(IN)
def z(r): return ((r[1] - MA) / SA, (r[2] - MI) / SI)
ZX = ((X[0] - MA) / SA, (X[1] - MI) / SI)
RAW = {r[0]: math.hypot(r[1] - X[0], r[2] - X[1]) for r in DATA}
SC = {r[0]: math.hypot(z(r)[0] - ZX[0], z(r)[1] - ZX[1]) for r in DATA}
ORD = sorted(SC, key=SC.get)
RORD = sorted(RAW, key=RAW.get)
LAB = {r[0]: r[3] for r in DATA}; VAL = {r[0]: r[4] for r in DATA}
assert ORD == list('DBECFA') and RORD[0] == 'B'
assert round(SC['D'], 2) == 1.76 and round(RAW['B'], 1) == 13.3
def vote(ns):
    b = sum(LAB[n] == 'buy' for n in ns); return b, ('buy' if b * 2 > len(ns) else 'no')
assert vote('D') == (1, 'buy') and vote('DBE') == (1, 'no') and vote('DBECF') == (3, 'buy')
MEAN3 = sum(VAL[n] for n in 'DBE') / 3; MED3 = sorted(VAL[n] for n in 'DBE')[1]
assert round(MEAN3, 2) == 2.33 and MED3 == 1
CL = {'buy': FI, 'no': BR}

def pt(x, y, lab, r=6):
    """buy = solid indigo, no = hollow brand ring"""
    if lab == 'buy': return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, FI)
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="2.2"/>' % (x, y, r - 1, BG, BR)

def legend(x, y):
    return (pt(x, y - 4, 'buy', 5) + S(x + 10, y, 'buy', MU) + pt(x + 50, y - 4, 'no', 5) + S(x + 60, y, 'no', MU))

def star(x, y, c=VI, r=9):
    p = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * .45
        p.append('%.1f,%.1f' % (x + rr * math.cos(a), y + rr * math.sin(a)))
    return '<polygon points="%s" fill="%s"/>' % (' '.join(p), c)

def scatter_plane():
    return Plane(200, 376, 52)  # z in about [-1.5, 1.5] mapped after shift

def zp(P, zz): return P(zz[0] + 1.6, zz[1] + 1.9)

# ---------- 1 Mental model ----------
def fig_mental():
    f = Anim('kn1-', 720, 0, 'Six customers on a plane of age and income, solid for buy and hollow for no. A new customer X '
             'appears; a dashed circle grows until it holds the three nearest customers D, B and E; they vote one buy '
             'against two no, so X is predicted no.', 'PREDICT = FIND THE k NEAREST ROWS, LET THEM DECIDE')
    P = scatter_plane()
    f.static(L(P.X(0), P.Y(0), P.X(3.6), P.Y(0), RULE_HI, 1.3) + L(P.X(0), P.Y(0), P.X(0), P.Y(6.4), RULE_HI, 1.3) +
             S(P.X(3.6), P.Y(0) + 18, 'age (scaled)', MU, 'end') + S(P.X(0) - 4, P.Y(6.4) - 6, 'income (scaled)', MU))
    f.static(legend(P.X(0) + 10, 416))
    for i, r in enumerate(DATA):
        x, y = zp(P, z(r))
        f.show(pt(x, y, r[3]) + T(x + 11, y + 4, r[0], MU, 'start', bold=True), .2 + i * .15)
    xx, xy = zp(P, ZX)
    f.show(star(xx, xy) + T(xx - 10, xy + 4, 'X', VI, 'end', bold=True), 1.4)
    rad = (SC['E'] + SC['C']) / 2 * 52
    for k, n in enumerate('DBE'):
        r = [d for d in DATA if d[0] == n][0]; x, y = zp(P, z(r)); t = 2.4 + k * .7
        f.show(L(xx, xy, x, y, VI, 1.4, '4 3'), t, hide=t + .6)
        f.show('<circle cx="%.1f" cy="%.1f" r="11" fill="none" stroke="%s" stroke-width="1.8"/>' % (x, y, VI), t + .4)
    f.show('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="1.6" stroke-dasharray="5 4"/>' % (xx, xy, rad, tn(VI, '.06'), VI), 4.6)
    X0 = 440
    f.show(S(X0, 70, '1 · the table is the model — nothing is fitted', MU), .6)
    f.show(S(X0, 110, '2 · a new row X arrives with no label', MU), 1.4)
    f.show(S(X0, 150, '3 · take the k = 3 nearest rows', MU), 2.4)
    for k, n in enumerate('DBE'):
        f.show(pt(X0 + 12 + k * 64, 180, LAB[n]) + T(X0 + 26 + k * 64, 184, n, TX, 'start', bold=True) +
               S(X0 + 4 + k * 64, 204, LAB[n], CL[LAB[n]]), 2.8 + k * .7)
    f.show(S(X0, 240, '4 · they vote: 1 buy · 2 no', MU), 5.0)
    f.show(chip(X0 + 60, 272, 'X → no', FI, 110), 5.7)
    return finish(f, 430)

# ---------- 2 General formula: distance worked ----------
def fig_dist():
    f = Anim('kn2-', 720, 0, 'Distance from X to customer B, worked step by step: the age difference squared is 9, the income '
             'difference squared is 169, they add to 178 and the square root is 13.3.', 'ONE DISTANCE, STEP BY STEP')
    t = Table(0, 40, [('row', 50), ('x₁', 70, 'age'), ('x₂', 70, 'income')])
    f.static(t.head() + t.row(0, ['X', '25', '35'], colors={0: VI}) + t.row(1, ['B', '28', '22']))
    XM = 250
    f.show(M(XM, 64, '{d}(X, B) = √( ({x}₁ − {b}₁)² + ({x}₂ − {b}₂)² )', MU, 'start'), .3)
    f.show(t.outline(0, 1, 1, 1, VI), 1.0, hide=2.4)
    f.show(M(XM, 100, '(25 − 28)² = (−3)² = 9', TX, 'start'), 1.3)
    f.show(t.outline(0, 1, 2, 2, VI), 2.4, hide=3.8)
    f.show(M(XM, 130, '(35 − 22)² = 13² = 169', TX, 'start'), 2.7)
    f.show(M(XM, 160, '9 + 169 = 178', TX, 'start'), 3.9)
    f.show(M(XM, 190, '√178 = 13.3', TX, 'start'), 4.6)
    assert round(math.sqrt(178), 1) == round(RAW['B'], 1)
    f.show(chip(XM + 50, 226, 'd = 13.3', FI, 96), 5.3)
    f.show(S(0, 196, 'repeat for every row → one distance each', MU), 5.9)
    f.show(S(0, 216, 'd columns → d squared terms', MU), 6.3)
    return finish(f, 250)

# ---------- 3 Table to prediction ----------
def fig_table():
    f = Anim('kn3-', 720, 0, 'The six customers get a distance to X one row at a time, then re-sort by distance; the top '
             'three rows D, B and E are outlined and vote: one buy, two no, so X is no.', 'DISTANCE → SORT → TOP k → VOTE')
    cols = [('id', 40), ('age', 56, 'scaled'), ('income', 66, 'scaled'), ('buy?', 56), ('d', 70, 'to X')]
    t = Table(0, 36, cols)
    f.static(t.head())
    f.static(S(0, 30, 'X = (25, 35M) · columns already scaled', MU) if False else '')
    idx = {r[0]: i for i, r in enumerate(DATA)}
    for i, r in enumerate(DATA):
        zz = z(r)
        f.path(t.row(0, [r[0], '%.2f' % zz[0], '%.2f' % zz[1], r[3]], colors={3: CL[r[3]]}) +
               T(t.cx(4), t.ry(0) + 17, '%.2f' % SC[r[0]], VI, bold=True).replace('<text', '<text class="d"') ,
               [(0, 0, t.ry(i) - t.ry(0)), (3.6, 0, t.ry(ORD.index(r[0])) - t.ry(0))], .2 + i * .1, d=.8)
    # distance cells appear: cover them with a mask that hides
    for i, r in enumerate(DATA):
        f.show(R(t.colx(4) + 2, t.ry(i) + 2, 66, 22, BG, 'none'), 0, hide=.9 + i * .35, d=.05)
    f.show(t.colbox(4, 6, VI), .9, hide=3.3)
    f.show(S(t.x + t.w + 20, t.ry(2), 'sort rows by d', VI), 3.4, hide=4.6)
    f.show(t.outline(0, 2, c=VI, sw=2), 4.8)
    f.show(S(t.x + t.w + 20, t.ry(1) + 4, 'top k = 3', VI, bold=True), 4.8)
    for i in range(3, 6):
        f.show(R(t.x, t.ry(i), t.w, t.rh, SUNK, 'none').replace('/>', ' opacity=".7"/>'), 5.2)
    b, ans = vote('DBE')
    xr = t.x + t.w + 20
    f.show(S(xr, t.ry(3) + 6, 'votes: %d buy · %d no' % (b, 3 - b), MU), 5.8)
    f.show(chip(xr + 50, t.ry(4) + 18, 'X → ' + ans, FI, 100), 6.4)
    return finish(f, t.bottom(6) + 12)

# ---------- 4.1 k ----------
def fig_k():
    f = Anim('kn4-', 720, 0, 'The six rows sorted by distance: D buy, B no, E no, C buy, F buy, A no. Brackets for k equal to '
             '1, 3 and 5 take the first k rows and give buy, no and buy.', 'SAME SORTED ROWS · THREE VALUES OF k')
    W, x0, y0 = 62, 90, 40
    for i, n in enumerate(ORD):
        f.show(R(x0 + i * W, y0, W - 6, 40, BG, RULE_HI, 5) + pt(x0 + i * W + 16, y0 + 20, LAB[n]) +
               T(x0 + i * W + 36, y0 + 25, n, TX, bold=True) + T(x0 + i * W + 28, y0 + 56, '%.2f' % SC[n], FA, mono=True), .2 + i * .15)
    f.static(S(0, y0 + 25, 'nearest →', MU) + S(0, y0 + 56, 'd', MU))
    for j, k in enumerate((1, 3, 5)):
        y = 120 + j * 52; t0 = 1.4 + j * 1.6; b, ans = vote(ORD[:k])
        f.show(S(0, y + 18, 'k = %d' % k, VI, bold=True), t0)
        f.show(R(x0 - 2, y, k * W - 2, 28, tn(VI, '.10'), VI, 5, 1.6), t0 + .2)
        f.show(S(x0 + k * W + 6, y + 18, '%d buy · %d no' % (b, k - b), VI), t0 + .5)
        f.show(chip(560, y + 14, ans, FI, 64), t0 + .9)
    f.show(S(0, 290, 'small k follows single points (noisy) · large k drifts to the majority class', MU), 6.4)
    return finish(f, 316)

# ---------- 4.2 vote or mean ----------
def fig_combine():
    f = Anim('kn5-', 720, 0, 'The same three neighbours D, B and E. Classification counts labels: one buy, two no, answer no. '
             'Regression averages the values 1, minus 1 and 7: 7 over 3 is 2.33; the median is 1 because 7 is an outlier.',
             'SAME k NEIGHBOURS · ONLY THE COMBINING STEP CHANGES')
    t = Table(0, 40, [('id', 44), ('label', 64), ('value', 64)])
    f.static(t.head())
    for i, n in enumerate('DBE'):
        f.show(t.row(i, [n, LAB[n], '%+d' % VAL[n]], colors={1: CL[LAB[n]]}), .2 + i * .2)
    X1 = 240
    f.show(t.colbox(1, 3, VI), 1.2, hide=2.8)
    f.show(S(X1, 60, 'classification · vote', MU, bold=True), 1.2)
    f.show(M(X1, 88, 'buy: 1 · no: 2', TX, 'start'), 1.7)
    f.show(chip(X1 + 150, 84, 'ŷ = no', FI, 80, False), 2.3)
    f.show(t.colbox(2, 3, VI), 2.9)
    f.show(S(X1, 130, 'regression · mean', MU, bold=True), 2.9)
    y = 162
    f.show(M(X1, y + 4, '{ŷ} =', TX, 'start'), 3.4)
    f.show(M(X1 + 66, y - 6, '1 + (−1) + 7', TX) + L(X1 + 30, y, X1 + 102, y, TX, 1) + M(X1 + 66, y + 15, '3', TX), 3.4)
    f.show(M(X1 + 112, y + 4, '=', TX, 'start') + M(X1 + 144, y - 6, '7', TX) + L(X1 + 134, y, X1 + 154, y, TX, 1) + M(X1 + 144, y + 15, '3', TX), 4.1)
    f.show(chip(X1 + 220, y, 'ŷ = 2.33', FI, 92, False), 4.7)
    f.show(S(X1, 216, 'regression · median', MU, bold=True), 5.4)
    f.show(M(X1, 244, 'sorted: −1, 1, 7 → middle = 1', TX, 'start'), 5.9)
    f.show(chip(X1 + 300, 240, 'ŷ = 1.00', FI, 92, False), 6.4)
    f.show(t.outline(2, 2, 2, 2, RO), 7.0)
    f.show(S(0, 200, 'E = +7 is an outlier:', RO) + S(0, 218, 'it drags the mean,', RO) + S(0, 236, 'not the median', RO), 7.0)
    return finish(f, 262)

# ---------- 4.3 metric ----------
def fig_metric():
    f = Anim('kn6-', 720, 0, 'Points a at (1, 1) and b at (4, 3). Euclidean distance is the straight line, 3.61. Manhattan '
             'distance walks the grid, 3 plus 2 equals 5. Cosine distance ignores length and measures the angle between '
             'the two arrows from the origin.', 'THREE WAYS TO MEASURE "CLOSE"')
    P = Plane(50, 250, 46)
    f.static(P.grid(0, 5, 0, 4, labels=True, xl='{x}₁', yl='{x}₂'))
    a, b = P(1, 1), P(4, 3)
    f.static(dot(*a, BR, 5) + M(a[0] - 4, a[1] - 10, '{a}', BR) + dot(*b, BR, 5) + M(b[0] + 12, b[1] - 6, '{b}', BR))
    X1 = 340
    f.show(L(a[0], a[1], b[0], b[1], VI, 2.6), .6)
    f.show(S(X1, 62, 'Euclidean (L2) · straight line', VI, bold=True), .6)
    f.show(M(X1, 88, '√(3² + 2²) = √13 = 3.61', TX, 'start'), 1.1)
    f.show(poly([a, (b[0], a[1]), b], FI, 2.6, '6 4'), 2.2)
    f.show(S(X1, 128, 'Manhattan (L1) · along the grid', FI, bold=True), 2.2)
    f.show(M(X1, 154, '|3| + |2| = 5', TX, 'start'), 2.7)
    o = P(0, 0)
    f.show(arrow(o[0], o[1], a[0] - 4, a[1] + 4, MU, 1.3) + arrow(o[0], o[1], b[0] - 5, b[1] + 4, MU, 1.3), 3.8)
    ang_a, ang_b = math.atan2(1, 1), math.atan2(3, 4); rr = 40
    pa = (o[0] + rr * math.cos(ang_a), o[1] - rr * math.sin(ang_a)); pb = (o[0] + rr * math.cos(ang_b), o[1] - rr * math.sin(ang_b))
    f.show('<path d="M%.1f %.1f A%d %d 0 0 0 %.1f %.1f" fill="none" stroke="%s" stroke-width="2.4"/>' % (pb[0], pb[1], rr, rr, pa[0], pa[1], RO) +
           M(o[0] + rr + 12, o[1] - 24, 'θ', RO, 'start'), 4.1)
    cos = (4 + 3) / (math.hypot(1, 1) * 5)
    f.show(S(X1, 194, 'Cosine · only the angle', RO, bold=True), 4.1)
    f.show(M(X1, 220, '1 − cos θ = 1 − %.2f = %.2f' % (cos, 1 - cos), TX, 'start'), 4.6)
    f.show(S(X1, 250, 'text and embeddings: length ≈ document size, angle ≈ topic', MU), 5.3)
    return finish(f, 290)

# ---------- 5.1 scale ----------
def fig_scale():
    f = Anim('kn7-', 720, 0, 'Two rankings of the same customers by distance to X. In raw units the wide age column dominates '
             'and B is nearest, answer no. After scaling both columns to the same spread, D is nearest, answer buy.',
             'SAME DATA, SAME X · SCALING FLIPS THE NEAREST ROW')
    def rank(x, title, ds, order, t0, fmt):
        t = Table(x, 40, [('id', 40), ('d', 64), ('buy?', 56)], title)
        f.show(t.head(), t0)
        for i, n in enumerate(order):
            f.show(t.row(i, [n, fmt % ds[n], LAB[n]], colors={2: CL[LAB[n]]}), t0 + .3 + i * .18)
        f.show(t.outline(0, c=VI, sw=2), t0 + 1.6)
        f.show(chip(x + 80, t.bottom(6) + 24, 'k = 1 → ' + LAB[order[0]], FI, 120), t0 + 2.0)
        return t
    t = rank(0, 'RAW UNITS', RAW, RORD, .2, '%.1f')
    rank(380, 'SCALED (z-SCORE)', SC, ORD, 3.0, '%.2f')
    xm = 210
    f.show(S(xm, 80, 'age spans 24–60', MU) + S(xm, 98, 'income 12–34', MU), 1.2)
    f.show(R(xm, 108, 36 * 3, 8, tn(VI, '.5'), 'none', 2) + R(xm, 120, 22 * 3, 8, tn(BR, '.5'), 'none', 2), 1.4)
    f.show(S(xm, 146, 'wider column', VI) + S(xm, 162, 'decides alone', VI), 1.8)
    f.show(M(xm, 214, '{z} =', TX, 'start') + M(xm + 60, 204, '{x} − {μ}', TX) + L(xm + 38, 209, xm + 82, 209, TX, 1) + M(xm + 60, 224, '{σ}', TX), 3.0)
    f.show(S(xm, 248, 'every column spread 1', MU), 3.2)
    return finish(f, t.bottom(6) + 44)

# ---------- 5.2 curse ----------
CURSE = []
for d in (2, 10, 100, 500):
    rng = random.Random(1); Pn = [[rng.random() for _ in range(d)] for _ in range(500)]
    ds = sorted(math.dist(Pn[0], p) for p in Pn[1:]); CURSE.append((d, ds[0] / ds[-1]))
def fig_curse():
    f = Anim('kn8-', 720, 0, 'Bars for 2, 10, 100 and 500 dimensions with 500 random points: the ratio of nearest to farthest '
             'distance rises from %.2f to %.2f, %.2f and %.2f, approaching 1, where every point is equally far.' % tuple(c[1] for c in CURSE),
             '500 RANDOM POINTS · NEAREST ÷ FARTHEST DISTANCE')
    x0, yb, H, W = 70, 230, 180, 90
    f.static(L(x0 - 10, yb, x0 + 4 * 130, yb, RULE_HI, 1.3))
    f.static(L(x0 - 10, yb - H, x0 + 4 * 130, yb - H, RO, 1.2, '5 4') + S(x0 + 4 * 130 + 6, yb - H + 4, '= 1: all equally far', RO))
    for i, (d, r) in enumerate(CURSE):
        x = x0 + i * 130; h = r * H; t0 = .4 + i * .8
        f.path(R(x, yb - h, W, h, tn(VI if i == 3 else BR, '.35'), VI if i == 3 else BR, 3, 1.3), [(0, 0, 20), (t0, 0, 0)], t0, d=.5)
        f.show(T(x + W / 2, yb - h - 8, '%.2f' % r, TX, mono=True, bold=True), t0 + .4)
        f.static(S(x + W / 2, yb + 18, '%d dims' % d, MU, 'middle'))
    f.show(S(0, yb + 48, 'nearest is barely nearer than farthest → the k "nearest" are close to a random pick', VI), 3.8)
    return finish(f, yb + 62)

# ---------- 5.3 slow prediction ----------
def fig_cost():
    f = Anim('kn9-', 720, 0, 'Fit only stores the rows, with no work. Predicting one new row scans every stored row, six rows '
             'times two columns here; a million rows with a hundred columns would cost a hundred million operations per query.',
             'FIT IS FREE · EVERY PREDICTION SCANS ALL n ROWS')
    t = Table(0, 40, [('id', 40), ('age', 50), ('income', 60)])
    f.static(t.head())
    for i, r in enumerate(DATA):
        f.show(t.row(i, [r[0], str(r[1]), str(r[2])]), .2 + i * .1)
    f.show(S(t.w + 30, t.ry(0) + 16, 'fit(): store the table · 0 work', MU), .9)
    f.path(t.outline(0, c=VI, sw=2), [(0, 0, 0)] + [(1.8 + i * .45, 0, t.ry(i) - t.ry(0)) for i in range(1, 6)], 1.6, d=.3)
    for i in range(6):
        f.show(R(t.w + 30, t.ry(i) + 30 if False else 120, 0, 0, BG, 'none'), 0)
    for i in range(6):
        f.show(T(t.w + 230, 105, str(2 * (i + 1)), VI, 'start', mono=True, bold=True), 1.7 + i * .45, hide=None if i == 5 else 2.15 + i * .45)
    f.show(S(t.w + 30, 100, 'predict(X): operations so far', MU), 1.6)
    f.show(M(t.w + 30, 156, '{n} · {d} = 6 · 2 = 12 per query', TX, 'start'), 4.4)
    f.show(M(t.w + 30, 184, '10⁶ rows · 100 columns = 10⁸ per query', RO, 'start'), 5.0)
    f.show(S(t.w + 30, 212, 'fix: an index (KD-tree, ball tree, HNSW) skips most rows', FI), 5.6)
    return finish(f, t.bottom(6) + 12)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Classical models</p>
  <h1>KNN — <em>k nearest neighbours</em></h1>
  <p class="lede">KNN learns nothing: it keeps the training table and, for each new row, lets the <b>k most similar rows</b> decide.</p>
</header>

<section id="knn-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">To predict a new row, find the <em>k rows closest to it</em> in the stored data and let them decide.</p>
{kn1}
  <ul class="why">
    <li>Nothing is fitted, so KNN is called a <b>lazy learner</b> or non-parametric model.</li>
    <li>The boundary has no fixed shape: it follows the data, wiggles and all.</li>
  </ul>
</section>

<section id="knn-s2" class="lesson">
  <div class="sh"><b>02</b><h2>General formula</h2></div>
  <p class="key">Two pieces: a <em>distance</em> between rows, and a rule that <em>combines</em> the labels of the k nearest.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>d</var>(<var>x</var>, <var>x</var><sub><var>j</var></sub>)</span><em>distance to row j</em></span>
      <span class="op">=</span>
      <span class="t b"><span>√<span class="op">(</span>Σ<sub><var>m</var></sub> (<var>x</var><sub><var>m</var></sub> − <var>x</var><sub><var>jm</var></sub>)<sup>2</sup><span class="op">)</span></span><em>sum over columns m</em></span>
    </div>
    <div class="line">
      <span class="t"><span><var>ŷ</var></span><em>prediction</em></span>
      <span class="op">=</span>
      <span class="t g"><span><b class="fn">mode</b> { <var>y</var><sub><var>j</var></sub> : <var>j</var> ∈ <var>N</var><sub><var>k</var></sub>(<var>x</var>) }</span><em>classification: most common label</em></span>
      <span class="op">or</span>
      <span class="t b"><span><span class="frac"><i>1</i><i><var>k</var></i></span> Σ<sub><var>j</var> ∈ <var>N</var><sub><var>k</var></sub>(<var>x</var>)</sub> <var>y</var><sub><var>j</var></sub></span><em>regression: mean value</em></span>
    </div>
    <dl>
      <dt><var>N</var><sub><var>k</var></sub>(<var>x</var>)</dt><dd>the k rows with the smallest distance to x</dd>
      <dt>loss</dt><dd>none — no parameter is trained, so there is no loss and no gradient</dd>
    </dl>
  </div>
{kn2}
  <ul class="why">
    <li>The raw distance 13.3 is in mixed units (years and millions); section 4.4 shows why that matters.</li>
  </ul>
</section>

<section id="knn-s3" class="lesson">
  <div class="sh"><b>03</b><h2>From table to prediction</h2></div>
  <p class="key">Predicting is <em>sorting by distance</em>, keeping the top k rows and counting their votes.</p>
{kn3}
  <ul class="why">
    <li>New customer X: age 25, income 35M; both columns scaled before measuring.</li>
    <li>Training is free, so every prediction pays: <span class="mth"><var>O</var>(<var>n</var> · <var>d</var>)</span> per query and the whole table stays in memory; large sets need an index (KD-tree, HNSW).</li>
  </ul>
</section>

<section id="knn-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Knobs</h2></div>
  <p class="key">The model is exactly three choices: <em>how many</em> neighbours, <em>how to combine</em> them, and <em>what "close" means</em>.</p>
  <div class="subsec" id="knn-s4-1">
    <h3 class="ssh"><b>4.1</b>Number of neighbours k</h3>
    <p class="skey">Same sorted rows, different k, <em>different answer</em>: k sits right on the bias–variance axis.</p>
{kn4}
    <ul class="why">
      <li>k = 1 memorises noise (high variance, training error 0 — meaningless); k = n always predicts the majority (high bias).</li>
      <li>Pick k by cross-validation; an odd k avoids ties with two classes; <code>weights="distance"</code> lets nearer rows count more.</li>
    </ul>
  </div>
  <div class="subsec" id="knn-s4-2">
    <h3 class="ssh"><b>4.2</b>Vote, mean or median</h3>
    <p class="skey">Classification takes the <em>most common label</em>; regression takes the <em>mean</em>, or the <em>median</em> when outliers sit among the neighbours.</p>
{kn5}
    <ul class="why">
      <li>For long-tailed targets use the median, the same story as MAE vs MSE in <a href="../linear-regression/index.html">Linear regression</a>.</li>
      <li>In sklearn: <code>KNeighborsClassifier</code> votes, <code>KNeighborsRegressor</code> averages.</li>
    </ul>
  </div>
  <div class="subsec" id="knn-s4-3">
    <h3 class="ssh"><b>4.3</b>Distance metric</h3>
    <p class="skey">"Close" is a choice: <em>choosing the metric is choosing the model</em>.</p>
{kn6}
    <ul class="why">
      <li>Euclidean for continuous columns of the same kind; Manhattan is less hurt by one huge difference; cosine for text and embeddings.</li>
    </ul>
  </div>
  <div class="subsec" id="knn-s4-4">
    <h3 class="ssh"><b>4.4</b>Feature scaling</h3>
    <p class="skey">The column with the widest range <em>decides the distance alone</em> unless you scale first.</p>
{kn7}
    <ul class="why">
      <li>Fit the scaler on the training set only, then apply it to new rows.</li>
      <li>Trees compare one column at a time, so they do not care; every distance-based model does.</li>
    </ul>
  </div>
</section>

<section id="knn-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Curse of dimensionality</h2></div>
  <p class="key">As dimensions grow, <em>every point is about equally far from every other</em>, and "nearest" loses its meaning.</p>
{kn8}
  <ul class="why">
    <li>Hits every distance-based model (k-means, RBF-kernel SVM); reduce dimensions first (<a href="../../08-dimensionality/pca-dimensionality/index.html">PCA</a>, feature selection).</li>
    <li>KNN fits a quick baseline or low-dimensional similarity search; with many rows or columns prefer trees or boosting.</li>
  </ul>
</section>

'''

def build():
    figs = dict(kn1=fig_mental(), kn2=fig_dist(), kn3=fig_table(), kn4=fig_k(), kn5=fig_combine(), kn6=fig_metric(),
                kn7=fig_scale(), kn8=fig_curse())
    return re.sub(r'\{(kn\d+)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">'); b = s.index('<script>\n/* Figures start')
    s = s[:a] + body + s[b:]
    s = re.sub(r'data-blurb="[^"]*"( data-reviewed="\d")?', 'data-blurb="%s" data-reviewed="2"' % blurb, s, count=1)
    open(page, 'w').write(s)

if __name__ == '__main__':
    splice(PAGE, build(), 'No training at all: KNN stores the table and lets the k nearest rows vote, so k, the distance and scaling decide everything.')
