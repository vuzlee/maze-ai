# -*- coding: utf-8 -*-
"""Figures + page body for content/07-machine-learning/05-classical-ml/logistic-regression.
Run: python3 logistic_regression.py  -> rewrites the lesson body between <header class="hero"> and the replay script."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, BR, VI, FI, RO, GH, RULE, RULE_HI, SUNK, BG,
                            tn, M, S, dot, poly, Plane, finish)

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/05-classical-ml/logistic-regression/index.html')
ONF = 'var(--on-fill)'

# ---------- running example: 6 customers, x = age, y = bought ----------
W, B = 0.074, -2.95
DATA = [('A', 24, 0), ('B', 28, 0), ('C', 35, 1), ('D', 41, 1), ('E', 52, 0), ('F', 60, 1)]
sig = lambda z: 1 / (1 + math.exp(-z))
ROWS = []
for n, x, y in DATA:
    z = W * x + B; p = sig(z); l = -math.log(p if y else 1 - p)
    ROWS.append((n, x, y, z, p, l))
MEAN = sum(r[5] for r in ROWS) / 6
assert '%.2f' % ROWS[4][4] == '0.71' and '%.2f' % ROWS[4][5] == '1.24', ROWS[4]

def N(v, d=2, sign=False):
    s = ('%+.' + str(d) + 'f') % v if sign else ('%.' + str(d) + 'f') % v
    return s.replace('-', '−')

def num(x, y, s, c=TX, a='middle', bold=False):
    return T(x, y, s, c, a, 'sv-d', mono=True, bold=bold).replace('class="sv-d"', 'class="sv-d" font-size="12"')

def frac(cx, cy, n, d, c=TX, w=None):
    w = w or max(len(re.sub(r'[{}]', '', n)), len(re.sub(r'[{}]', '', d))) * 8 + 12
    return M(cx, cy - 7, n, c) + L(cx - w / 2, cy, cx + w / 2, cy, c, 1.1) + M(cx, cy + 17, d, c)

def box(x, y, w, h, c=FI, txt=None, tc=ONF):
    if c == BR:
        s = R(x, y, w, h, tn(BR, '.16'), BR, 6, 1.4); tc = BR
    else:
        s = R(x, y, w, h, c, c, 6)
    return s + (M(x + w / 2, y + h / 2 + 5, txt, tc) if txt else '')

def hl(x, y, w, h, c=VI):
    return R(x, y, w, h, tn(c, '.10'), c, 6, 1.6)

# ---------- 1. Mental model: x -> z -> p -> label ----------
def fig_mental():
    f = Anim('lr1-', 720, 0, 'Six customers A to F sit on a z axis by their score z = w x + b, from about minus 1.2 to plus 1.5. '
             'Each one rises to the sigmoid curve and reads off a probability p between 0 and 1. A threshold at 0.5 '
             'then turns p into a label: D, E and F are predicted to buy.', 'x → SCORE z → PROBABILITY p → LABEL')
    P = Plane(250, 250, 62, 190)
    f.static(L(P.X(-3), P.Y(0), P.X(3), P.Y(0), MU, 1.1) + L(P.X(-3), P.Y(0), P.X(-3), P.Y(1) - 10, MU, 1.1))
    f.static(M(P.X(3) + 8, P.Y(0) + 5, '{z}', MU, 'start') + M(P.X(-3), P.Y(1) - 16, '{p}', MU))
    f.static(T(P.X(-3) - 6, P.Y(1) + 4, '1', FA, 'end') + T(P.X(-3) - 6, P.Y(0) + 4, '0', FA, 'end') +
             L(P.X(-3), P.Y(1), P.X(3), P.Y(1), RULE, 1, '2 4'))
    for k in (-2, 0, 2):
        f.static(T(P.X(k), P.Y(0) + 15, N(k, 0) if k else '0', FA))
    pts = [P(z / 20, sig(z / 20)) for z in range(-60, 61)]
    for i in range(0, 120, 12):
        f.show(poly(pts[i:i + 13], BR, 2.4), .3 + i / 120 * .9, d=.1)
    f.show(M(P.X(1.9), P.Y(sig(1.9)) - 14, '{p} = σ({z})', BR), 1.3)
    t = 1.8
    lx = 530
    f.static(T(lx, 50, 'customer', MU) + T(lx + 70, 50, 'p', MU) + T(lx + 140, 50, 'label', MU) + L(lx - 30, 57, lx + 175, 57))
    for i, (n, x, y, z, p, l) in enumerate(ROWS):
        zx, py = P.X(z), P.Y(p)
        f.show(dot(zx, P.Y(0), BR, 4) + T(zx, P.Y(0) + 28 + (i % 2) * 12, n, BR, bold=True), t + i * .12)
        tt = t + 1 + i * .55
        f.path(dot(zx, py, VI, 5.5), [(tt, 0, P.Y(0) - py), (tt + .05, 0, 0)], t0=tt - .3, d=.45)
        f.show(L(P.X(-3), py, zx, py, VI, 1, '3 3'), tt + .5)
        f.show(T(lx, 78 + i * 26, n, TX, bold=True) + num(lx + 70, 78 + i * 26, N(p)), tt + .5)
    t = t + 1 + 6 * .55 + .4
    f.show(L(P.X(-3), P.Y(.5), P.X(3), P.Y(.5), VI, 1.6, '6 4') + T(P.X(-3) + 6, P.Y(.5) - 6, 'threshold 0.5', VI, 'start', 'sv-s', bold=True), t)
    for i, r in enumerate(ROWS):
        buy = r[4] >= .5
        cx, cy = lx + 140, 74 + i * 26
        f.show(R(cx - 26, cy - 11, 52, 20, FI if buy else SUNK, FI if buy else RULE_HI, 10) +
               T(cx, cy + 3.5, 'buy' if buy else 'no', ONF if buy else GH, bold=True), t + .5 + i * .15)
    return finish(f, 300)

# ---------- 2. General formula worked on one customer ----------
def fig_worked():
    n, x, y, z, p, l = ROWS[4]
    ez = math.exp(-z)
    f = Anim('lr2-', 720, 0, 'The formula worked on customer E, age 52, who did not buy. z = 0.074 times 52 minus 2.95 = 0.90. '
             'p = 1 over 1 plus e to the minus 0.90 = 1 over 1.41 = 0.71. Because y = 0 only the second log-loss term '
             'survives: L = minus log of 1 minus 0.71 = minus log 0.29 = 1.24, a large loss for a confident wrong answer.',
             'ONE CUSTOMER THROUGH THE FORMULA · E, AGE 52, DID NOT BUY')
    f.static(M(30, 52, 'customer E:   {x} = 52,   {y} = 0', BR, 'start'))
    # line 1: z
    Y1 = 100
    f.show(M(30, Y1, '{z}  =  {w}·{x} + {b}', TX, 'start'), .5)
    f.show(M(150, Y1, '=  0.074 · 52 − 2.95', VI, 'start'), 1.2)
    f.show(M(300, Y1, '=', TX, 'start') + box(318, Y1 - 18, 58, 26, BR, N(z)), 2.0)
    # line 2: p
    Y2 = 170
    f.show(M(30, Y2 + 5, '{p}  =', TX, 'start') + frac(115, Y2, '1', '1 + {e}<tspan dy="-6" font-size="10">−<tspan class="v">z</tspan></tspan>', TX, 74), 2.8)
    f.show(M(170, Y2 + 5, '=', TX, 'start') + frac(240, Y2, '1', '1 + {e}<tspan dy="-6" font-size="10">−0.90</tspan>', VI, 92), 3.5)
    f.show(M(305, Y2 + 5, '=', TX, 'start') + frac(352, Y2, '1', N(1 + ez), VI, 50), 4.2)
    f.show(M(395, Y2 + 5, '=', TX, 'start') + box(413, Y2 - 13, 58, 26, BR, N(p)), 4.9)
    # line 3: loss
    Y3 = 250
    f.show(M(30, Y3, '{L}  =  −[ {y} log {p} + (1 − {y}) log(1 − {p}) ]', TX, 'start'), 5.7)
    f.show(R(66, Y3 + 12, 118, 3, RULE_HI, 'none', 1) + S(125, Y3 + 30, 'y = 0: drops out', FA, 'middle'), 6.4)
    f.show(M(30, Y3 + 62, '=  −log(1 − 0.71)  =  −log 0.29  =', VI, 'start'), 7.1)
    f.show(box(290, Y3 + 44, 64, 26, RO, N(l)), 7.9)
    f.show(S(30, Y3 + 98, 'the model was sure E would buy, and was wrong: big loss', RO), 8.3)
    return finish(f, 370)

# ---------- 3.1 forward pass on the table ----------
COLS = [('', 34), ('x', 52), ('y', 40), ('z', 66), ('p', 60), ('L', 60)]
def colx(j, x0=20): return x0 + sum(c[1] for c in COLS[:j])
def colc(j, x0=20): return colx(j, x0) + COLS[j][1] / 2

def fig_forward():
    f = Anim('lr3-', 720, 0, 'The six customers as a table with columns x (age), y (bought), z, p and the log loss L. '
             'Row by row z, p and L are filled in; a bar on the right shows each loss. Customer E has the longest bar, 1.24. '
             'The mean of the L column, 0.60, is the loss the model minimises.', 'FORWARD PASS · ROW BY ROW')
    top = 64
    heads = [('', ''), ('x', 'age'), ('y', 'bought'), ('z', 'w·x + b'), ('p', 'σ(z)'), ('L', 'log loss')]
    for j, (h, sub) in enumerate(heads):
        if h: f.static(M(colc(j), 40, '{%s}' % h, MU) + T(colc(j), 54, sub, FA))
    f.static(L(20, 60, colx(6), 60))
    BX, SC = 420, 100
    f.static(L(BX, top - 4, BX, top + 6 * 30, RULE_HI, 1) + T(BX, 54, 'loss per customer', MU, 'start'))
    t = .5
    for i, (n, x, y, z, p, l) in enumerate(ROWS):
        ry = top + i * 30
        f.static(R(20, ry, colx(6) - 20, 26, BG, RULE_HI, 3) + T(colc(0), ry + 17, n, TX, bold=True) +
                 num(colc(1), ry + 17, str(x)) + num(colc(2), ry + 17, str(y)))
        f.show(R(17, ry - 3, colx(6) - 14, 32, 'none', VI, 5, 1.6), t, hide=t + 1.0)
        f.show(num(colc(3), ry + 17, N(z, sign=True)), t + .25)
        f.show(num(colc(4), ry + 17, N(p)), t + .5)
        bad = i == 4
        f.show(num(colc(5), ry + 17, N(l), RO if bad else TX, bold=bad), t + .75)
        f.show(R(BX, ry + 5, l * SC, 16, tn(RO, '.25') if bad else tn(BR, '.22'), RO if bad else BR, 3, 1), t + .75)
        t += 1.05
    f.show(S(BX + ROWS[4][5] * SC + 8, top + 4 * 30 + 17, 'E: p = 0.71, did not buy', RO), t)
    yb = top + 6 * 30 + 14
    f.show(L(colx(5), yb - 6, colx(6), yb - 6, TX, 1) + M(colx(4) - 6, yb + 16, '{L} = mean =', TX, 'end') +
           box(colx(5) + 2, yb, 56, 24, FI, N(MEAN)), t + .6)
    f.show(L(BX + MEAN * SC, top - 4, BX + MEAN * SC, top + 6 * 30, FI, 1.4, '4 3') + S(BX + MEAN * SC + 5, yb + 16, 'mean', FI), t + 1.1)
    assert '%.2f' % MEAN == '0.60', MEAN
    return finish(f, yb + 34)

# ---------- 3.2 one gradient step ----------
def fig_gradient():
    f = Anim('lr4-', 720, 0, 'One gradient-descent step from w = 0, b = 0. Every p is 0.5. The p minus y column is plus 0.5 for '
             'non-buyers and minus 0.5 for buyers; times x gives 12, 14, minus 17.5, minus 20.5, 26, minus 30. Their mean is '
             'the slope dL/dw = minus 2.67. The update w = 0 minus 0.01 times minus 2.67 = 0.027 raises w, so older '
             'customers get higher p.', 'ONE GRADIENT STEP · START AT w = 0, b = 0')
    cols = [('', 34), ('x', 50), ('y', 40), ('p', 50), ('p − y', 66), ('(p − y)·x', 86)]
    xs = [20]
    for c in cols: xs.append(xs[-1] + c[1])
    cc = lambda j: xs[j] + cols[j][1] / 2
    for j, (h, w) in enumerate(cols):
        if h: f.static(M(cc(j), 50, re.sub(r'([a-z])', r'{\1}', h), MU))
    f.static(L(20, 58, xs[-1], 58))
    top, g = 62, []
    t = .5
    f.show(R(xs[3] + 1, 44 - 6, cols[3][1] - 2, 6 * 30 + 26, 'none', VI, 4, 1.4), .4, hide=1.4)
    for i, (n, x, y, *_r) in enumerate(ROWS):
        ry = top + i * 30
        d = .5 - y; g.append(d * x)
        f.static(R(20, ry, xs[-1] - 20, 26, BG, RULE_HI, 3) + T(cc(0), ry + 17, n, TX, bold=True) + num(cc(1), ry + 17, str(x)) +
                 num(cc(2), ry + 17, str(y)))
        f.show(num(cc(3), ry + 17, '0.50'), .5)
        f.show(num(cc(4), ry + 17, N(d, 1, True), VI), 1.6 + i * .15)
        f.show(num(cc(5), ry + 17, N(d * x, 1, True), VI), 2.8 + i * .2)
    f.show(R(xs[4] + 1, 44 - 6, cols[4][1] - 2, 6 * 30 + 26, 'none', VI, 4, 1.4), 1.5, hide=2.6)
    f.show(R(xs[5] + 1, 44 - 6, cols[5][1] - 2, 6 * 30 + 26, 'none', VI, 4, 1.4), 2.7, hide=4.3)
    gw = sum(g) / 6
    assert '%.2f' % gw == '-2.67', gw
    # right: the worked update
    X = 400
    f.show(frac(X + 26, 80, '∂{L}', '∂{w}') + M(X + 58, 85, '=', TX, 'start') + frac(X + 84, 80, '1', '6') +
           M(X + 100, 85, 'Σ ({p} − {y})·{x}', TX, 'start'), 4.5)
    f.show(M(X + 58, 135, '=  −16 / 6  =', VI, 'start') + box(X + 166, 117, 60, 26, VI, N(gw)), 5.3)
    f.show(M(X, 200, '{w}  ←  {w} − {η}', TX, 'start') + frac(X + 112, 195, '∂{L}', '∂{w}'), 6.3)
    f.show(M(X + 30, 250, '=  0 − 0.01 · (−2.67)  =', VI, 'start') + box(X + 216, 232, 64, 26, FI, '+0.027'), 7.1)
    f.show(S(X, 288, 'slope < 0, so w goes up: older customers get a higher p', FI), 7.9)
    return finish(f, 300)

# ---------- 4.1 why sigmoid ----------
def fig_sigmoid():
    xs = [r[1] for r in ROWS]; ys = [r[2] for r in ROWS]
    mx, my = sum(xs) / 6, sum(ys) / 6
    a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); c = my - a * mx
    f = Anim('lr5-', 720, 0, 'The same six customers plotted as age against bought (0 or 1), extended to ages 0 to 100. Left: a '
             'straight line fitted by least squares crosses below 0 for young ages and above 1 for old ages, which is not a '
             'probability. Right: the sigmoid curve stays between 0 and 1 for every age.', 'A LINE LEAVES [0, 1] · SIGMOID NEVER DOES')
    for k, (title, kind) in enumerate((('straight line', 'line'), ('sigmoid', 'sig'))):
        x0 = 50 + k * 350
        P = Plane(x0, 220, 2.8, 140)
        f.static(L(x0, P.Y(0), x0 + 290, P.Y(0), MU, 1.1) + L(x0, P.Y(-.45), x0, P.Y(1.45), MU, 1.1) +
                 L(x0, P.Y(1), x0 + 290, P.Y(1), RULE, 1, '2 4') + T(x0 - 6, P.Y(1) + 4, '1', FA, 'end') +
                 T(x0 - 6, P.Y(0) + 4, '0', FA, 'end') + T(x0 + 290, P.Y(0) + 16, 'age 100', FA, 'end') +
                 T(x0 + 145, 44, title, BR if kind == 'line' else FI, cls='sv-s', bold=True))
        f.static(R(x0 + 1, P.Y(1.45), 289, P.Y(1) - P.Y(1.45), tn(RO, '.07'), 'none', 0) +
                 R(x0 + 1, P.Y(0), 289, P.Y(-.45) - P.Y(0), tn(RO, '.07'), 'none', 0))
        for (n, x, y, *_r) in ROWS:
            f.static(dot(P.X(x), P.Y(y), BR if y else BG, 4.5, BR))
        t0 = .6 + k * 2.6
        if kind == 'line':
            pts = [P(x, a * x + c) for x in range(0, 101, 2)]
            col = BR
        else:
            pts = [P(x, sig(W * x + B)) for x in range(0, 101, 2)]
            col = FI
        for i in range(0, 50, 5):
            f.show(poly(pts[i:i + 6], col, 2.4), t0 + i / 50 * 1.2, d=.12)
        if kind == 'line':
            lo, hi = a * 0 + c, a * 100 + c
            f.show(dot(*P(0, lo), RO, 5) + S(x0 + 8, P.Y(lo) + 4, '%s at age 0' % N(lo), RO), t0 + 1.4)
            f.show(dot(*P(100, hi), RO, 5) + S(x0 + 280, P.Y(hi) + 4, '%s at age 100' % N(hi), RO, 'end'), t0 + 1.8)
        else:
            f.show(S(x0 + 150, P.Y(.5) + 30, 'always between 0 and 1', FI), t0 + 1.4)
    assert a * 100 + c > 1.05 and c < -0.05
    return finish(f, 292)

# ---------- 4.2 why log loss ----------
def fig_logloss():
    f = Anim('lr6-', 720, 0, 'Loss for a buyer (y = 1) as a function of the predicted p. Log loss, minus log p, shoots up to 3.9 at '
             'p = 0.02; squared error (1 minus p) squared stays below 1. The push each loss gives to z at p = 0.02: log loss '
             'gives p minus y = minus 0.98, squared error gives 2 (p minus y) p (1 minus p) = minus 0.04, almost nothing.',
             'A BUYER PREDICTED AT p = 0.02 · HOW HARD EACH LOSS PUSHES BACK')
    P = Plane(60, 250, 300, 50)
    f.static(L(60, 250, 370, 250, MU, 1.1) + L(60, 250, 60, 40, MU, 1.1) + M(378, 255, '{p}', MU, 'start') +
             T(P.X(1), 266, '1', FA) + T(P.X(0), 266, '0', FA) + T(54, P.Y(4) + 4, '4', FA, 'end') + T(54, P.Y(1) + 4, '1', FA, 'end') +
             L(60, P.Y(1), 360, P.Y(1), RULE, 1, '2 4'))
    ll = [P(p / 100, -math.log(p / 100)) for p in range(2, 101)]
    se = [P(p / 100, (1 - p / 100) ** 2) for p in range(0, 101)]
    for i in range(0, 99, 11):
        f.show(poly(ll[i:i + 12], FI, 2.6), .5 + i / 99, d=.1)
    f.show(M(P.X(.12) + 6, P.Y(2.3), '−log {p}', FI, 'start'), 1.5)
    for i in range(0, 100, 10):
        f.show(poly(se[i:i + 11], BR, 2.2, '6 4'), 1.9 + i / 100, d=.1)
    f.show(M(P.X(.3), P.Y(.5) - 12, '(1 − {p})²', BR, 'start'), 2.9)
    p = .02
    f.show(L(P.X(p), 250, P.X(p), P.Y(-math.log(p)), VI, 1.2, '3 3') + dot(P.X(p), P.Y(-math.log(p)), VI, 5) +
           dot(P.X(p), P.Y((1 - p) ** 2), VI, 5) + S(P.X(p) + 8, P.Y(-math.log(p)) + 4, 'p = 0.02, wrong and sure', VI), 3.6)
    # right: gradient push
    X = 420
    g_ll, g_se = p - 1, 2 * (p - 1) * p * (1 - p)
    f.show(S(X, 60, 'push on z  =  ∂L / ∂z', MU), 4.4)
    f.show(M(X, 100, 'log loss:  {p} − {y}', FI, 'start') + num(X + 260, 100, N(g_ll), FI, 'end', True), 4.8)
    f.show(R(X, 112, abs(g_ll) * 260, 18, tn(FI, '.30'), FI, 3), 5.3)
    f.show(M(X, 170, 'squared:  2({p} − {y}) {p}(1 − {p})', BR, 'start') + num(X + 260, 170, N(g_se), BR, 'end', True), 6.1)
    f.show(R(X, 182, max(abs(g_se) * 260, 3), 18, tn(BR, '.30'), BR, 3), 6.6)
    f.show(S(X, 222, 'the p(1 − p) factor ≈ 0 at the worst mistakes', RO), 7.2)
    f.show(S(X, 240, 'log loss cancels it, so learning never stalls', FI), 7.7)
    assert '%.2f' % g_se == '-0.04'
    return finish(f, 276)

# ---------- 4.3 odds ratio ----------
def fig_odds():
    w = .7
    p0 = .30; lo0 = math.log(p0 / (1 - p0)); lo1 = lo0 + w; p1 = sig(lo1); o0, o1 = p0 / (1 - p0), p1 / (1 - p1)
    f = Anim('lr7-', 720, 0, 'One coefficient w = 0.7 read on three scales, for a customer who flips from never bought to bought before. '
             'Log-odds moves from minus 0.85 to minus 0.15: add 0.7. Odds move from 0.43 to 0.86: multiply by e to the 0.7, '
             'about 2.0. Probability moves from 0.30 to 0.46: no tidy rule.', 'ONE COEFFICIENT, THREE SCALES · w = 0.7')
    rows = [('log-odds', '{w}·{x} + {b}', -2, 1, lo0, lo1, '+ 0.7', 'add w'),
            ('odds', '{p} / (1 − {p})', 0, 1.2, o0, o1, '× 2.01', 'multiply by eʷ'),
            ('probability', '{p}', 0, 1, p0, p1, '0.30 → 0.46', 'no tidy rule')]
    X0, X1 = 200, 560
    for i, (name, form, a, b, v0, v1, op, rule) in enumerate(rows):
        y = 70 + i * 80
        sx = lambda v: X0 + (v - a) / (b - a) * (X1 - X0)
        f.static(T(30, y + 4, name, TX, 'start', 'sv-s', bold=True) + M(30, y + 24, form, MU, 'start') +
                 L(X0, y, X1, y, RULE_HI, 1.4))
        for k in ([a, 0, b] if a < 0 else [a, b]):
            f.static(L(sx(k), y - 4, sx(k), y + 4, MU, 1) + T(sx(k), y + 18, N(k, 1) if k % 1 else '%d' % k, FA))
        t = .6 + i * .3
        f.show(dot(sx(v0), y, BR, 6) + num(sx(v0), y - 12, N(v0), BR), t)
        t2 = 2.0 + i * 1.6
        f.show(arrow(sx(v0) + 7, y, sx(v1) - 8, y, VI, 2, None, 8), t2)
        f.show(dot(sx(v1), y, FI, 6) + num(sx(v1), y - 12, N(v1), FI, bold=True), t2 + .4)
        f.show(R(590, y - 20, 116, 40, tn(RO if i == 2 else VI, '.10'), RO if i == 2 else VI, 6) +
               M(648, y - 2, op, RO if i == 2 else VI) + T(648, y + 13, rule, RO if i == 2 else VI), t2 + .8)
    f.static(T(200, 44, 'before: never bought', BR, 'start', 'sv-s') + T(400, 44, 'after: bought before', FI, 'start', 'sv-s'))
    assert '%.2f' % p1 == '0.46' and '%.2f' % (o1 / o0) == '2.01'
    return finish(f, 272)

# ---------- 4.4 threshold ----------
def fig_threshold():
    f = Anim('lr8-', 720, 0, 'The six customers on a probability axis; filled dots bought, hollow dots did not. A threshold mark slides '
             'from 0.35 to 0.5 to 0.75; everyone to its right is flagged as a buyer. At 0.35 all 3 buyers are caught with 1 false '
             'alarm (E). At 0.5, 2 of 3 buyers and 1 false alarm. At 0.75, only 1 of 3 buyers and no false alarm.',
             'MOVE THE THRESHOLD · WHO GETS FLAGGED')
    X0, X1, Y = 40, 680, 120
    sx = lambda p: X0 + p * (X1 - X0)
    f.static(L(X0, Y, X1, Y, MU, 1.2))
    for k in (0, .25, .5, .75, 1):
        f.static(L(sx(k), Y - 4, sx(k), Y + 4, MU, 1) + (T(sx(k), Y + 44, '%g' % k, FA) if k in (0, 1) else ''))
    for (n, x, y, z, p, l) in ROWS:
        f.static(dot(sx(p), Y, BR if y else BG, 7, BR) + T(sx(p), Y - 16, n, TX, bold=True) + num(sx(p), Y + 24, N(p), MU))
    f.static(dot(X0 + 4, 40, BR, 5, BR) + T(X0 + 14, 44, 'bought', MU, 'start', 'sv-s') +
             dot(X0 + 84, 40, BG, 5, BR) + T(X0 + 94, 44, 'did not', MU, 'start', 'sv-s'))
    cuts = [.35, .5, .75]
    t = .6
    for k, c in enumerate(cuts):
        flagged = [r for r in ROWS if r[4] >= c]
        tp = sum(r[2] for r in flagged); fp = len(flagged) - tp
        hide = t + 2.4 if k < 2 else None
        f.show(R(sx(c), Y - 34, X1 - sx(c) + 6, 58, tn(VI, '.10'), 'none', 4) + L(sx(c), Y - 40, sx(c), Y + 30, VI, 2) +
               T(sx(c), Y - 46, 'threshold %g' % c, VI, cls='sv-s', bold=True), t, hide=hide)
        f.show(T(360, 200, 'caught %d of 3 buyers  ·  %d false alarm%s' % (tp, fp, '' if fp == 1 else 's'),
                 FI, cls='sv-s', bold=True), t + .5, hide=hide)
        t += 2.8
    f.show(T(360, 226, 'lower it to miss fewer buyers · raise it to cut false alarms', MU, cls='sv-s'), t - .5)
    return finish(f, 240)

# ---------- 4.5 softmax ----------
def fig_softmax():
    zs = [2.0, 1.0, 0.1]; es = [math.exp(z) for z in zs]; S_ = sum(es); ps = [e / S_ for e in es]
    f = Anim('lr9-', 720, 0, 'Three classes cat, dog and bird get one score each: 2.0, 1.0 and 0.1. Exponentiate: 7.39, 2.72 and 1.11, '
             'summing to 11.21. Divide each by the sum: probabilities 0.66, 0.24 and 0.10, which add to 1.',
             'MORE THAN TWO CLASSES · SOFTMAX')
    names = ['cat', 'dog', 'bird']
    stages = [('score {z}', zs, 2.5, BR), ('{e}<tspan dy="-6" font-size="10" class="v">z</tspan>', es, 8, VI), ('{p} = {e}<tspan dy="-6" font-size="10" class="v">z</tspan><tspan dy="6"> / 11.21</tspan>', ps, 1, FI)]
    for i, n in enumerate(names):
        f.static(T(60, 84 + i * 50, n, TX, 'end', 'sv-s', bold=True))
    for k, (title, vals, mx, col) in enumerate(stages):
        x0 = 80 + k * 210
        t = .5 + k * 2.2
        f.show(M(x0 + 70, 50, title, col), t)
        for i, v in enumerate(vals):
            f.show(R(x0, 70 + i * 50, max(v / mx * 150, 2), 22, tn(col, '.25'), col, 3) +
                   num(x0 + v / mx * 150 + 6, 86 + i * 50, N(v), col, 'start', k == 2), t + .3 + i * .2)
        if k:
            f.show(arrow(x0 - 44, 150, x0 - 14, 150, MU, 1.3), t - .1)
    f.show(S(500, 236, 'sum = 1.00 · the biggest score still wins', FI), 7.2)
    assert ['%.2f' % p for p in ps] == ['0.66', '0.24', '0.10']
    return finish(f, 250)

# ---------- 5.1 curved boundary ----------
def fig_curve():
    f = Anim('lr10-', 720, 0, 'Two features x1 and x2. Buyers (filled) sit in the middle, '
             'non-buyers in a ring around them. Any straight line leaves errors on both sides. Adding the feature '
             'x1 squared plus x2 squared lets the same linear model draw a circle that separates them.', 'A STRAIGHT BOUNDARY CANNOT WRAP A CLUSTER')
    inner = [(.8 * math.cos(a), .8 * math.sin(a)) for a in [k * 1.1 for k in range(6)]] + [(.2, -.1), (-.3, .3)]
    outer = [(2.1 * math.cos(a), 2.1 * math.sin(a)) for a in [k * .63 + .2 for k in range(10)]]
    for k in range(2):
        cx0 = 180 + k * 360
        P = Plane(cx0, 150, 45)
        f.static(L(P.X(-2.8), P.Y(0), P.X(2.8), P.Y(0), RULE, 1) + L(P.X(0), P.Y(2.6), P.X(0), P.Y(-2.6), RULE, 1) +
                 M(P.X(2.8) + 6, P.Y(0) + 5, '{x}<tspan dy="4" font-size="10">1</tspan>', MU, 'start') +
                 M(P.X(0) + 6, P.Y(2.6) + 4, '{x}<tspan dy="4" font-size="10">2</tspan>', MU, 'start'))
        for (a, b) in inner: f.static(dot(*P(a, b), BR, 4.5, BR))
        for (a, b) in outer: f.static(dot(*P(a, b), BG, 4.5, BR))
        if k == 0:
            f.show(L(P.X(-1.2), P.Y(2.6), P.X(1.9), P.Y(-2.6), RO, 2, '6 4'), .8)
            f.show(T(cx0, 290, 'any line: mistakes on both sides', RO, cls='sv-s', bold=True), 1.3)
        else:
            f.show(T(cx0 + 60, 34, 'add the feature', VI, 'start', 'sv-s'), 2.4)
            f.show(M(cx0 + 60, 54, '{x}₁² + {x}₂²', VI, 'start'), 2.6)
            pts = [P(1.45 * math.cos(a / 20 * math.pi), 1.45 * math.sin(a / 20 * math.pi)) for a in range(41)]
            for i in range(0, 40, 5):
                f.show(poly(pts[i:i + 6], FI, 2.4), 3.3 + i / 40, d=.12)
            f.show(T(cx0, 290, 'still linear in the new feature: a circle', FI, cls='sv-s', bold=True), 4.5)
    f.static(L(360, 40, 360, 280, RULE, 1))
    return finish(f, 300)

# ---------- 5.2 perfect separation ----------
def fig_separation():
    f = Anim('lr11-', 720, 0, 'Non-buyers at x = 1, 2, 3 and buyers at x = 4, 5, 6: perfectly separable. Gradient descent keeps '
             'raising w: the sigmoid gets steeper at w = 1, 3 and 10 and the log loss falls from 0.21 to 0.02 to almost 0. '
             'w never stops growing; L2 regularization stops it.', 'PERFECTLY SEPARABLE DATA · w NEVER STOPS GROWING')
    P = Plane(60, 230, 70, 180)
    f.static(L(60, 230, 540, 230, MU, 1.1) + L(60, 230, 60, 30, MU, 1.1) + M(548, 235, '{x}', MU, 'start') +
             T(54, P.Y(1) + 4, '1', FA, 'end') + T(54, P.Y(0) + 4, '0', FA, 'end') + L(60, P.Y(1), 540, P.Y(1), RULE, 1, '2 4'))
    for x in range(1, 7):
        y = 1 if x > 3 else 0
        f.static(dot(P.X(x), P.Y(y), BR if y else BG, 5.5, BR) + T(P.X(x), 246, str(x), FA))
    t = .6
    out = []
    for k, w in enumerate((1, 3, 10)):
        loss = sum(-math.log(sig(w * (x - 3.5)) if x > 3 else 1 - sig(w * (x - 3.5))) for x in range(1, 7)) / 6
        out.append(loss)
        pts = [P(x / 20, sig(w * (x / 20 - 3.5))) for x in range(0, 141)]
        last = k == 2
        col = VI if last else BR
        hide = t + 2.0
        for i in range(0, 140, 14):
            f.show(poly(pts[i:i + 15], col, 2.4), t + i / 140 * .8, d=.1, hide=None if last else hide)
        f.show(M(600, 90, '{w} = %d' % w, col) + M(600, 120, '{L} = %s' % N(loss, 3), col), t + .4, hide=None if last else hide)
        t += 2.4
    f.show(S(568, 160, 'w → ∞,  L → 0', RO, 'start', True), t - 1.2)
    f.show(S(568, 180, 'fix: L2 keeps w finite', FI, 'start', True), t - .6)
    assert out[0] > out[1] > out[2]
    return finish(f, 260)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Classical models</p>
  <h1>Logistic <em>regression</em></h1>
  <p class="lede">Take the straight line of <a href="../linear-regression/index.html">linear regression</a>, squash its score into a probability with a <b>sigmoid</b>, and train it with <b>log loss</b> instead of MSE.</p>
</header>

<section id="logreg-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Every sample goes <em>x → z → p</em>: a linear score, squashed into a probability. A threshold you choose turns p into a label.</p>
{lr1}
  <ul class="why">
    <li>Running example all lesson: six customers A–F, <span class="mth"><var>x</var></span> is age, the label is bought or not.</li>
    <li>The model stops at <span class="mth"><var>p</var></span>; the label step is a business decision (section 4.4).</li>
  </ul>
</section>

<section id="logreg-s2" class="lesson">
  <div class="sh"><b>02</b><h2>General formula</h2></div>
  <p class="key">The score <span class="mth"><var>z</var></span> is the <em>linear part</em>, the sigmoid turns it into a probability, and log loss charges for <em>confidence in the wrong answer</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t b"><span><var>z</var> = <var>w</var>·<var>x</var> + <var>b</var></span><em>score, from −∞ to +∞</em></span>
      <span class="op">,</span>
      <span class="t p"><span><var>p</var> = <span class="frac"><i>1</i><i>1 + <var>e</var><sup>−<var>z</var></sup></i></span></span><em>sigmoid σ(z): squashed into (0, 1)</em></span>
    </div>
    <div class="line">
      <span class="t"><span><var>L</var></span><em>log loss</em></span>
      <span class="op">=</span>
      <span class="t r"><span>− <span class="frac"><i>1</i><i><var>n</var></i></span> Σ<sub><var>i</var></sub> [ <var>y</var><sub><var>i</var></sub> <b class="fn">log</b> <var>p</var><sub><var>i</var></sub> + (1 − <var>y</var><sub><var>i</var></sub>) <b class="fn">log</b>(1 − <var>p</var><sub><var>i</var></sub>) ]</span><em>y is 0 or 1, so only one of the two terms survives</em></span>
    </div>
  </div>
{lr2}
  <ul class="why">
    <li><span class="mth"><var>L</var></span> is also called <b>binary cross-entropy</b>; it is the negative log-likelihood of the labels.</li>
    <li>A confident right answer costs almost 0; a confident wrong answer costs without limit.</li>
  </ul>
</section>

<section id="logreg-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Learning on a table</h2></div>
  <p class="key">Training repeats two passes: <em>forward</em> fills p and the loss row by row, <em>backward</em> turns the errors into a slope and nudges w.</p>
  <div class="subsec" id="logreg-s3-1">
    <h3 class="ssh"><b>3.1</b>Forward pass</h3>
    <p class="skey">Each row becomes <em>z, then p, then its loss</em>; the model's loss is the mean of the last column.</p>
{lr3}
    <ul class="why">
      <li>Customer E (52, did not buy) costs most: the model is sure older customers buy.</li>
      <li>One feature means one flat boundary, so no w can fit E without hurting the others.</li>
    </ul>
  </div>
  <div class="subsec" id="logreg-s3-2">
    <h3 class="ssh"><b>3.2</b>Gradient step</h3>
    <p class="skey">The slope is the mean of <em>error × input</em>, the same shape as in linear regression with ŷ replaced by p.</p>
    <div class="eq">
      <div class="line">
        <span class="t"><span><span class="frac"><i>∂<var>L</var></i><i>∂<var>w</var></i></span></span></span>
        <span class="op">=</span>
        <span class="t g"><span><span class="frac"><i>1</i><i><var>n</var></i></span> Σ<sub><var>i</var></sub> (<var>p</var><sub><var>i</var></sub> − <var>y</var><sub><var>i</var></sub>) · <var>x</var><sub><var>i</var></sub></span><em>error times input, averaged</em></span>
        <span class="op">,</span>
        <span class="t p"><span><var>w</var> ← <var>w</var> − <var>η</var> <span class="frac"><i>∂<var>L</var></i><i>∂<var>w</var></i></span></span><em>step against the slope, learning rate η</em></span>
      </div>
    </div>
{lr4}
    <ul class="why">
      <li>There is no closed form like the normal equation; the loss is convex, so gradient descent reaches the single minimum.</li>
      <li>Scale the features first, or a feature like age dominates the slope.</li>
    </ul>
  </div>
</section>

<section id="logreg-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Key choices</h2></div>
  <p class="key">Two design choices make it work, and three knobs decide <em>how you read and use</em> the output.</p>
  <div class="subsec" id="logreg-s4-1">
    <h3 class="ssh"><b>4.1</b>Sigmoid</h3>
    <p class="skey">A straight line <em>does not stop at 0 and 1</em>; the sigmoid does, for any input.</p>
{lr5}
    <ul class="why">
      <li>The sigmoid only rescales the score; the boundary <span class="mth"><var>z</var> = 0</span> is still a straight line or flat plane.</li>
    </ul>
  </div>
  <div class="subsec" id="logreg-s4-2">
    <h3 class="ssh"><b>4.2</b>Log loss</h3>
    <p class="skey">With a sigmoid, MSE <em>stops pushing</em> exactly on the worst mistakes; log loss keeps pushing.</p>
{lr6}
    <ul class="why">
      <li>MSE with a sigmoid is also non-convex; log loss is convex, so the start point does not matter.</li>
      <li>Regularize like any linear model: add L1 or L2 as in <a href="../ridge-lasso-elasticnet/index.html">Ridge, Lasso &amp; Elastic Net</a>. In scikit-learn <code>C</code> is 1/λ.</li>
    </ul>
  </div>
  <div class="subsec" id="logreg-s4-3">
    <h3 class="ssh"><b>4.3</b>Odds ratio</h3>
    <p class="skey">The linear part is the <em>log-odds</em>, so one more unit of x <em>multiplies</em> the odds by <span class="mth"><var>e</var><sup><var>w</var></sup></span>.</p>
    <div class="eq">
      <div class="line">
        <span class="t"><span><b class="fn">log</b> <span class="frac"><i><var>p</var></i><i>1 − <var>p</var></i></span></span><em>log-odds</em></span>
        <span class="op">=</span>
        <span class="t b"><span><var>w</var>·<var>x</var> + <var>b</var></span><em>the linear part</em></span>
        <span class="op">,</span>
        <span class="t p"><span><var>e</var><sup><var>w</var></sup></span><em>odds ratio: odds multiply by this per unit of x</em></span>
      </div>
    </div>
{lr7}
    <ul class="why">
      <li>Add on log-odds, multiply on odds, no tidy rule on probability.</li>
      <li>For a non-specialist audience just say "from 30% to 46%".</li>
    </ul>
  </div>
  <div class="subsec" id="logreg-s4-4">
    <h3 class="ssh"><b>4.4</b>Decision threshold</h3>
    <p class="skey">The cut from p to a label is a <em>business decision</em>, not a model parameter.</p>
{lr8}
    <ul class="why">
      <li>0.5 is nothing special; choose by the cost of a missed buyer versus a false alarm.</li>
      <li>Measuring the trade-off: <a href="../../09-evaluation/metrics-confusion-matrix/index.html">precision and recall</a>, and <a href="../../09-evaluation/roc-auc-pr/index.html">ROC and PR curves</a> over every threshold.</li>
    </ul>
  </div>
  <div class="subsec" id="logreg-s4-5">
    <h3 class="ssh"><b>4.5</b>Softmax for many classes</h3>
    <p class="skey">With K classes, give each its own score and <em>exponentiate then normalise</em>; with two classes this is the sigmoid again.</p>
{lr9}
    <ul class="why">
      <li>Called multinomial logistic regression; the loss becomes cross-entropy over K classes.</li>
      <li>The other option, one-vs-rest, trains K separate binary models.</li>
    </ul>
  </div>
</section>

<section id="logreg-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Where it breaks</h2></div>
  <p class="key">Every weakness comes from the same place as every strength: <em>one straight line through a sigmoid</em>.</p>
  <div class="subsec" id="logreg-s5-1">
    <h3 class="ssh"><b>5.1</b>Curved boundary</h3>
    <p class="skey">The boundary is always straight in the inputs; a curve needs <em>features you build by hand</em>.</p>
{lr10}
    <ul class="why">
      <li>Squares and interactions are covered in <a href="../../04-core-concepts/feature-engineering/index.html">Feature engineering</a>; tree models find such shapes on their own.</li>
    </ul>
  </div>
  <div class="subsec" id="logreg-s5-2">
    <h3 class="ssh"><b>5.2</b>Perfect separation</h3>
    <p class="skey">If a line splits the classes perfectly, the loss keeps falling as <em>w grows forever</em>.</p>
{lr11}
    <ul class="why">
      <li>Symptom: huge coefficients and probabilities stuck at 0 or 1; regularization or more data fixes it.</li>
      <li>The trade-off overall: trustworthy probabilities and readable coefficients, but less accuracy than <a href="../../06-tree-models/gradient-boosting/index.html">gradient boosting</a> on tabular data.</li>
    </ul>
  </div>
</section>

'''

def build():
    figs = dict(lr1=fig_mental(), lr2=fig_worked(), lr3=fig_forward(), lr4=fig_gradient(), lr5=fig_sigmoid(), lr6=fig_logloss(),
                lr7=fig_odds(), lr8=fig_threshold(), lr9=fig_softmax(), lr10=fig_curve(), lr11=fig_separation())
    return re.sub(r'\{(lr\d+)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">')
    b = s.index('<script>\n/* Figures start')
    s = s[:a] + body + s[b:]
    s = re.sub(r'data-blurb="[^"]*"( data-reviewed="\d")?', 'data-blurb="%s" data-reviewed="2"' % blurb, s, count=1)
    open(page, 'w').write(s)

if __name__ == '__main__':
    splice(PAGE, build(), 'A straight line squashed by a sigmoid into a probability, trained with log loss, read through odds ratios and cut by a threshold you choose.')
    print('ok')
