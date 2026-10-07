# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/06-tree-models/gradient-boosting.
Same six customers and drawing helpers as decision_tree.py. Every number is computed here:
regression boosts `spend` from the mean, classification boosts the log-odds of `buy` from the base rate,
both with one-split trees (stumps) and eta = 0.5; a seeded noisy sine set gives the early-stopping curve.
Run: python3 gradient_boosting.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from decision_tree import DATA, HL, scan, var, qbox, qring, splice
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, VI, FI, RO, RULE, BG,
                            tn, M, S, dot, poly, finish)
from tablefig import AM, GR, tint, pill

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/06-tree-models/gradient-boosting/index.html')
IDS = [r[0] for r in DATA]
Y = {r[0]: r[5] for r in DATA}     # spend
B = {r[0]: r[4] for r in DATA}     # buy
ETA = .5
sig = lambda z: 1 / (1 + math.exp(-z))

def stump(res):
    """best one-split tree on the residual column -> (column, threshold, gain, left ids, right ids)"""
    rows = [r[:5] + (res[r[0]],) for r in DATA]
    return max(scan(rows, var), key=lambda s: s[2])

# ---------- regression: F0 = mean spend, r = y - F, leaf = mean r ----------
def boost_reg(eta, n):
    F = {k: sum(Y.values()) / 6 for k in IDS}; hist = []
    for _ in range(n + 1):
        res = {k: Y[k] - F[k] for k in IDS}
        hist.append((dict(F), res, sum(v * v for v in res.values()) / 6))
        c, t, g, lft, rgt = stump(res)
        lv = {s: sum(res[i] for i in s) / len(s) for s in (lft, rgt)}
        F = {k: F[k] + eta * lv[lft if k in lft else rgt] for k in IDS}
    return hist
REG = boost_reg(ETA, 4)
assert REG[0][0]['A'] == 25 and [REG[0][1][k] for k in IDS] == [-15, -13, 5, 9, 3, 11]
assert [round(h[2], 3) for h in REG] == [105, 31.5, 13.125, 8.166, 4.957]
S1 = stump(REG[0][1]); assert S1[:2] == ('age', 31.5) and S1[3:] == ('AB', 'CDEF') and S1[2] == 98
RLV = {'AB': -14, 'CDEF': 7}
assert [REG[1][0][k] for k in IDS] == [18, 18, 28.5, 28.5, 28.5, 28.5]
assert [REG[1][1][k] for k in IDS] == [-8, -6, 1.5, 5.5, -.5, 7.5]

# ---------- classification: F0 = log-odds of the base rate, p = sigma(F), r = y - p, leaf = sum r / sum p(1-p) ----------
def boost_cls(eta, n):
    F0 = math.log(sum(B.values()) / (6 - sum(B.values())))
    F = {k: F0 for k in IDS}; hist = []
    for _ in range(n + 1):
        p = {k: sig(F[k]) for k in IDS}; res = {k: B[k] - p[k] for k in IDS}
        ll = -sum(math.log(p[k]) if B[k] else math.log(1 - p[k]) for k in IDS) / 6
        hist.append((dict(F), p, res, ll))
        c, t, g, lft, rgt = stump(res)
        lv = {s: sum(res[i] for i in s) / sum(p[i] * (1 - p[i]) for i in s) for s in (lft, rgt)}
        F = {k: F[k] + eta * lv[lft if k in lft else rgt] for k in IDS}
    return hist
CLS = boost_cls(ETA, 1)
assert CLS[0][0]['A'] == 0 and all(CLS[0][1][k] == .5 for k in IDS)
assert [CLS[0][2][k] for k in IDS] == [-.5, -.5, .5, .5, -.5, .5]
S2 = stump(CLS[0][2]); assert S2[:2] == ('age', 31.5) and S2[3:] == ('AB', 'CDEF') and round(S2[2], 4) == .125
CLV = {'AB': -1 / .5, 'CDEF': 1 / 1}
assert [CLS[1][0][k] for k in IDS] == [-1, -1, .5, .5, .5, .5]
assert round(CLS[0][3], 3) == .693 and round(CLS[1][3], 3) == .504
assert [round(CLS[1][1][k], 3) for k in 'AC'] == [.269, .622]

# ---------- learning rate: train MSE against number of trees on the six customers ----------
ETAS = (1, .5, .1)
ECURVE = {e: [h[2] for h in boost_reg(e, 30)] for e in ETAS}
REACH = {e: next(i for i, v in enumerate(ECURVE[e]) if v <= 5) for e in ETAS}
assert REACH == {1: 2, .5: 4, .1: 27}

# ---------- early stopping: depth-3 trees, eta 0.1, 40 noisy train points, 400 validation points ----------
def tree(xs, rs, d):
    n = len(xs)
    if d == 0 or n < 4: return ('l', sum(rs) / n)
    o = sorted(range(n), key=lambda i: xs[i]); best = None; Sm = sum(rs); SL = 0
    for k in range(1, n):
        SL += rs[o[k - 1]]
        if xs[o[k]] == xs[o[k - 1]] or k < 2 or n - k < 2: continue
        sc = SL * SL / k + (Sm - SL) ** 2 / (n - k)
        if best is None or sc > best[0]: best = (sc, (xs[o[k - 1]] + xs[o[k]]) / 2)
    if best is None: return ('l', Sm / n)
    t = best[1]; Li = [i for i in range(n) if xs[i] < t]; Ri = [i for i in range(n) if xs[i] >= t]
    return ('n', t, tree([xs[i] for i in Li], [rs[i] for i in Li], d - 1), tree([xs[i] for i in Ri], [rs[i] for i in Ri], d - 1))
def tpred(t, x):
    while t[0] == 'n': t = t[2] if x < t[1] else t[3]
    return t[1]
def mk(n, seed):
    g = random.Random(seed)
    out = []
    for _ in range(n):
        x = g.random(); out.append((x, 3 * math.sin(2 * math.pi * x) + g.gauss(0, 1)))
    return out
TRN, VAL = mk(40, 1), mk(400, 101)
def es_curve(n=200, eta=.1):
    Ft, Fv, out = [0] * len(TRN), [0] * len(VAL), []
    for _ in range(n + 1):
        out.append((sum((p[1] - f) ** 2 for p, f in zip(TRN, Ft)) / len(TRN), sum((p[1] - f) ** 2 for p, f in zip(VAL, Fv)) / len(VAL)))
        t = tree([p[0] for p in TRN], [p[1] - f for p, f in zip(TRN, Ft)], 3)
        Ft = [f + eta * tpred(t, p[0]) for p, f in zip(TRN, Ft)]; Fv = [f + eta * tpred(t, p[0]) for p, f in zip(VAL, Fv)]
    return out
ES = es_curve()
BEST = min(range(len(ES)), key=lambda i: ES[i][1])
assert BEST == 17 and round(ES[BEST][1], 2) == 1.41 and round(ES[-1][1], 2) == 2.04 and ES[-1][0] < .2

def chip(cx, cy, s, c=VI, w=None):
    """linear_algebra.chip, but also for the amber and green tones"""
    w = w or 16 + len(s) * 7.2
    fill = tint('am', '.14') if c == AM else tint('gr', '.14') if c == GR else tn(c, '.14')
    return (R(cx - w / 2, cy - 11, w, 22, BG, 'none', 11) + R(cx - w / 2, cy - 11, w, 22, fill, c, 11, 1.3) +
            T(cx, cy + 4.5, s, c, mono=True, bold=True))

def num(v, nd=None):
    """signed figure number with a real minus sign"""
    s = ('%g' % v) if nd is None else ('%.*f' % (nd, v))
    return s.replace('-', '−')
def snum(v, nd=None):
    return ('+' if v > 0 else '') + num(v, nd)

def frac(x, y, a, b, c=TX, w=None):
    """SVG fraction: numerator at y-7, bar at y, denominator at y+11 (equations.md)"""
    w = w or max(len(a), len(b)) * 7 + 8
    return M(x + w / 2, y - 5, a, c) + L(x, y, x + w, y, c, 1) + M(x + w / 2, y + 14, b, c)

def rounds(kind, n=3):
    """the first n trees of the boosting run: split, leaf ids, leaf values, F and r before and after"""
    out = []
    for m in range(n):
        if kind == 'reg':
            F, res, Fn, rn = REG[m][0], REG[m][1], REG[m + 1][0], REG[m + 1][1]
            c, t, _, lft, rgt = stump(res); g = {s: sum(res[i] for i in s) / len(s) for s in (lft, rgt)}
        else:
            F, p, res = CLSH[m][:3]; Fn, rn = CLSH[m + 1][0], CLSH[m + 1][2]
            c, t, _, lft, rgt = stump(res); g = {s: sum(res[i] for i in s) / sum(p[i] * (1 - p[i]) for i in s) for s in (lft, rgt)}
        out.append(dict(col=c, thr=t, L=lft, R=rgt, g=g, F=F, res=res, Fn=Fn, rn=rn))
    return out
CLSH = boost_cls(ETA, 3)
RR, CR = rounds('reg'), rounds('cls')
assert [(r['col'], r['thr'], r['L']) for r in RR] == [('age', 31.5, 'AB'), ('age', 31.5, 'AB'), ('age', 56, 'ABCDE')]
assert [(r['col'], r['thr'], r['L']) for r in CR] == [('age', 31.5, 'AB'), ('age', 31.5, 'AB'), ('age', 56, 'ABCDE')]
assert [round(v, 3) for r in RR for v in r['g'].values()] == [-14, 7, -7, 3.5, -1.15, 5.75]
assert [round(v, 3) for r in CR for v in r['g'].values()] == [-2, 1, -1.368, .543, -.399, 1.462]
def predict(rs, F0, age):
    """X walks every tree: [(went left?, leaf value)] and the final F"""
    steps = [(age < r['thr'], r['g'][r['L'] if age < r['thr'] else r['R']]) for r in rs]
    return steps, F0 + sum(ETA * v for _, v in steps)
XAGE = 45
PR_REG, FX_REG = predict(RR, 25, XAGE); PR_CLS, FX_CLS = predict(CR, 0, XAGE)
assert [s[0] for s in PR_REG] == [False, False, True] and round(FX_REG, 3) == 29.675
assert round(FX_CLS, 3) == .572 and round(sig(FX_CLS), 2) == .64
# the r column of the mental-model table after each tree matches the full run
assert all(round(RR[m]['Fn']['A'], 3) == round(REG[m + 1][0]['A'], 3) for m in range(3))

def fm(v): return num(round(v, 3))
def sfm(v): return snum(round(v, 3))

def tok(cx, cy, s, c=RO):
    """a row travelling as a small token: id + value"""
    w = len(s) * 6.6 + 14
    return (R(cx - w / 2, cy - 9, w, 18, BG, 'none', 9) + R(cx - w / 2, cy - 9, w, 18, tint('am', '.14') if c == AM else tn(c, '.12'), c, 9, 1.1) +
            T(cx, cy + 4, s, c, mono=True, bold=True))

def stump_svg(cx, ry, ly, q, dx=38):
    s = L(cx, ry + 13, cx - dx, ly - 11, RULE_HI, 1.2) + L(cx, ry + 13, cx + dx, ly - 11, RULE_HI, 1.2)
    s += T(cx - dx / 2 - 8, (ry + ly) / 2 + 2, 'yes', FA, 'end') + T(cx + dx / 2 + 8, (ry + ly) / 2 + 2, 'no', FA, 'start')
    return s + qbox(cx, ry, q)

# ---------- 01 Mental model ----------
def fig_mental():
    # timeline per tree m (T = 1.2 + 4.6 m): T r column ringed + stump; T+.5 rows leave the r column as tokens and
    # slide into the leaves; T+1.6 leaf = mean r; T+2.4 each token becomes eta*leaf and flies back into F;
    # T+3.4 F updated; T+3.9 r recomputed. Trees are placed right to left so nothing flies over an earlier tree.
    f = Anim('gb1-', 720, 0, 'A table of six customers with spend y, prediction F starting at the mean 25, and residual r. Tree 1 '
             'asks age under 31.5: the rows slide out of the r column into its two leaves, A and B with minus 15 and minus 13, '
             'C to F with 5, 9, 3, 11. Each leaf takes the mean, minus 14 and 7, and half of it flies back into the F column: '
             'F becomes 18 and 28.5, and r is recomputed. Tree 2 is fitted on the new r the same way, then tree 3 splits at '
             'age 56. The model is 25 plus half of every tree; the mean squared error falls 105, 31.5, 13.1, 8.2.',
             'r LEAVES THE TABLE · A TREE AVERAGES IT · η × LEAF RETURNS INTO F · REPEAT')
    t = Table(0, 30, [('id', 28), ('age', 38), ('y', 44, 'spend'), ('F', 56, 'prediction'), ('r', 56, 'y − F')])
    f.static(t.head())
    for i, k in enumerate(IDS):
        f.static(t.row(i, [k, str(DATA[i][1]), str(Y[k])], colors={2: FI}))
        f.show(t.cell(i, 3, '25', c=VI), .3 + i * .04)
        f.show(t.cell(i, 4, sfm(REG[0][1][k]), c=RO), .6 + i * .04)
    CX = [335, 480, 625]; RY, LY, TY = 66, 128, 156
    LANE, GAP, RT = 254, 246, 5.8   # tokens travel: own row -> gap right of the table -> lane under the trees -> up into the leaf
    def route(x0, y0, x1, y1, t, back=False):
        pts = [(x0, y0), (GAP, y0), (GAP, LANE), (x1, LANE), (x1, y1)] if not back else \
              [(x0, y0), (x0, LANE), (GAP, LANE), (GAP, y1), (x1, y1)]
        fx, fy = pts[-1]
        return [(0, pts[0][0] - fx, pts[0][1] - fy)] + [(t + n * .42, x - fx, y - fy) for n, (x, y) in enumerate(pts[1:])]
    for m, rd in enumerate(RR):
        T0 = 1.2 + m * RT; cx = CX[m]
        f.show(t.colbox(4, 6, HL), T0, hide=T0 + 2.0)
        f.show(S(cx, 40, 'tree %d · fit on r' % (m + 1), MU, 'middle', bold=True) +
               stump_svg(cx, RY, LY, '%s < %g ?' % (rd['col'], rd['thr'])), T0)
        for side, g in (('L', rd['L']), ('R', rd['R'])):
            lx = cx - 38 if side == 'L' else cx + 38
            f.show(S(lx, LY + 26, ' '.join(g), FA, 'middle'), T0 + 4.6)
            for j, k in enumerate(g):
                i = IDS.index(k); fy = TY + j * 20; sx, sy = t.cx(4), t.ry(i) + 13
                tg = T0 + .3 + i * .08
                f.path(tok(lx, fy, '%s %s' % (k, sfm(rd['res'][k]))), route(sx, sy, lx, fy, tg), tg - .1, d=.4,
                       hide=T0 + 2.9)
                f.show(t.cell(i, 4, ''), tg + .1)
                step = ETA * rd['g'][g]; tb = T0 + 3.0 + i * .08
                # the chip sits at its final place in the F cell; the path brings it there from the leaf
                fx_, fy_ = t.cx(3), sy
                pts = route(lx, fy, fx_, fy_, tb, back=True)
                f.path(chip(fx_, fy_, sfm(step), AM, 58), pts, T0 + 2.8, d=.4, hide=T0 + 4.8 + i * .06)
                f.show(t.cell(i, 3, fm(rd['Fn'][k]), c=VI), T0 + 4.7 + i * .06)
                f.show(t.cell(i, 4, sfm(rd['rn'][k]), c=RO), T0 + 5.2 + i * .06)
            f.show(chip(lx, LY, sfm(rd['g'][g]), AM, 64), T0 + 2.3)
    tE = 1.2 + 3 * RT
    f.show(S(0, 284, 'η = 0.5 · leaf = mean r', MU), .3)
    f.show(M(480, 284, '{F} = 25 + {η}·tree₁ + {η}·tree₂ + {η}·tree₃', VI), tE)
    f.show(S(480, 306, 'MSE  105 → 31.5 → 13.1 → 8.2', RO, 'middle', bold=True), tE + .4)
    return finish(f, 316)

# ---------- 02 Residual as gradient ----------
def fig_gradient():
    # timeline: 0.3 loss curve; 1.0 point at F = 25 + tangent; 2.0 residual arrow to y; 3.2 tree step; 4.2 new point + smaller tangent
    f = Anim('gb2-', 720, 0, 'The squared loss of customer A, whose spend is 10, drawn against the prediction F. At F = 25 the '
             'curve slopes up by 15; the negative slope, minus 15, points left toward y = 10, and that is the residual y minus F. '
             'The tree gives A the leaf value minus 14, half of it is added, and F moves to 18, where the slope is only 8.',
             'THE RESIDUAL IS THE DOWNHILL DIRECTION OF THE LOSS')
    yA = Y['A']; ox, oy = 50, 262
    PX = lambda F: ox + F * 13; PY = lambda v: oy - v * 1.75
    Lf = lambda F: .5 * (yA - F) ** 2
    F0 = REG[0][0]['A']; r0 = REG[0][1]['A']; h = RLV['AB']; F1 = F0 + ETA * h
    assert (F0, r0, h, F1, Lf(F0), Lf(F1)) == (25, -15, -14, 18, 112.5, 32)
    f.static(L(ox, oy, PX(31), oy, RULE_HI, 1.3) + L(ox, oy, ox, PY(124), RULE_HI, 1.3))
    for F in (0, 10, 18, 25, 30): f.static(T(PX(F), oy + 15, str(F), FA, mono=True))
    f.static(M(PX(31) + 6, oy + 4, '{F}', MU, 'start') + M(ox + 4, PY(124) - 6, 'loss {L} = ½ ({y} − {F})²', MU, 'start'))
    f.show(poly([(PX(F / 4), PY(Lf(F / 4))) for F in range(0, 105)], FI, 2.4), .3)
    f.show(dot(PX(yA), oy, GR, 5.5, BG) + S(PX(yA) + 8, oy - 8, 'y = 10', GR, bold=True), .6)
    tang = lambda F, a: L(PX(F - a), PY(Lf(F) - (F - yA) * a), PX(F + a), PY(Lf(F) + (F - yA) * a), MU, 1.4, '5 3')
    f.show(dot(PX(F0), PY(Lf(F0)), VI, 6, BG) + tang(F0, 1.8), 1.0, hide=4.2)
    f.show(L(PX(F0), PY(Lf(F0)) + 6, PX(F0), oy + 56, VI, 1, '3 3'), 1.0)
    f.show(arrow(PX(F0), oy + 34, PX(yA) + 2, oy + 34, RO, 2.2) + S(PX(yA) - 6, oy + 38, 'r = −15', RO, 'end', bold=True), 2.0)
    f.show(arrow(PX(F0), oy + 56, PX(F1) + 2, oy + 56, AM, 2.2) + S(PX(F1) - 6, oy + 60, 'η · h = −7', AM, 'end', bold=True), 3.2)
    f.show('<circle cx="%.1f" cy="%.1f" r="5" fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="2 2"/>' % (PX(F0), PY(Lf(F0)), VI) +
           dot(PX(F1), PY(Lf(F1)), VI, 6, BG) + tang(F1, 3.5) + L(PX(F1), PY(Lf(F1)) + 6, PX(F1), oy + 56, VI, 1, '3 3'), 4.2)
    X1 = 470
    rows = [(.9, M(X1, 70, 'slope  ∂{L}/∂{F} = {F} − {y} = 15', TX, 'start')),
            (1.9, M(X1, 104, '{r} = −∂{L}/∂{F} = {y} − {F} = −15', RO, 'start')),
            (3.0, M(X1, 138, 'tree leaf for A:  {h} = −14', AM, 'start')),
            (3.6, M(X1, 172, '{F} ← 25 + 0.5 · (−14) = 18', VI, 'start')),
            (4.6, S(X1, 210, 'slope at 18 is 8: closer to y,', MU) + S(X1, 228, 'smaller residual, smaller step', MU))]
    for t, s in rows: f.show(s, t)
    return finish(f, oy + 72)

# ---------- 3.1 / 4.1 Residual ----------
def fig_resid(kind):
    reg = kind == 'reg'
    # timeline: 0.2 rows; 1.0 F0 rule; 1.4 F0 cells (+ p cells); 2.4.. outline walks rows, r cell + bar per row
    pre = 'gb3-' if reg else 'gb6-'
    if reg:
        cols = [('id', 30), ('age', 40), ('spend', 54, 'y'), ('F₀', 54, 'start'), ('r', 64, 'y − F')]
        F0, res = REG[0][0], REG[0][1]
        aria = ('The six customers with their spend. The first prediction F zero is the mean spend, 25, for every row. '
                'The residual is spend minus 25: minus 15, minus 13, 5, 9, 3, 11, drawn as bars left and right of zero.')
        cap = 'START WITH THE MEAN · RESIDUAL = WHAT IT STILL MISSES'
        start = (M(0, 270, '{F}₀ = mean of {y} = 150 / 6 = 25', VI, 'start'))
        assert sum(Y.values()) == 150
    else:
        cols = [('id', 30), ('age', 40), ('buy', 44, 'y'), ('F₀', 54, 'log-odds'), ('p', 48, 'σ(F)'), ('r', 58, 'y − p')]
        F0, res = CLS[0][0], CLS[0][2]
        aria = ('The six customers with buy as 1 or 0. Three of six buy, so the first prediction is log of 3 over 3, a log-odds '
                'of 0 for every row, and the probability is 0.5. The residual is buy minus 0.5: plus or minus 0.5, drawn as bars.')
        cap = 'START AT THE BASE RATE · RESIDUAL = LABEL − PROBABILITY'
        start = M(0, 270, '{F}₀ = log(3 / 3) = 0  →  {p} = σ(0) = 0.5', VI, 'start')
    f = Anim(pre, 720, 0, aria, cap)
    t = Table(0, 30, cols); f.static(t.head())
    jF, jr = 3, len(cols) - 1
    for i, k in enumerate(IDS):
        yv = str(Y[k]) if reg else str(B[k])
        f.show(t.row(i, [k, str(DATA[i][1]), yv], colors={2: FI}), .2 + i * .08)
    f.show(start, 1.0)
    for i, k in enumerate(IDS):
        f.show(t.cell(i, jF, num(F0[k]), c=VI), 1.4 + i * .05)
        if not reg: f.show(t.cell(i, 4, '%.1f' % CLS[0][1][k], c=VI), 1.8 + i * .05)
    T0 = 2.4 if reg else 2.8
    f.path(t.outline(0, c=HL), [(0, 0, 0)] + [(T0 + i * .5, 0, i * t.step) for i in range(1, 6)], T0 - .3, d=.3, hide=T0 + 3.0)
    BX = t.w + 160; sc = 140 / max(abs(v) for v in res.values())
    f.static(L(BX, t.ry(0) - 6, BX, t.ry(5) + t.rh + 4, RULE_HI, 1.2) + T(BX, t.ry(0) - 12, '0', FA, mono=True))
    for i, k in enumerate(IDS):
        v = res[k]; y = t.ry(i) + 6; w = abs(v) * sc
        f.show(t.cell(i, jr, snum(v), c=RO) + R(BX if v > 0 else BX - w, y, w, 14, tn(RO, '.28'), RO, 2, 1), T0 + .2 + i * .5)
    f.show(S(BX - 140, 268, 'left: %s too high · right: too low' % ('F' if reg else 'p'), MU), T0 + 3.4)
    return finish(f, 280)

# ---------- 3.2 / 4.2 Tree on the residual ----------
def fig_leaf(kind):
    reg = kind == 'reg'
    # timeline: 0.2 rows; 1.0 cut line; 1.6 root; 2.2 group AB + left leaf; 3.4 group CDEF + right leaf
    pre = 'gb4-' if reg else 'gb7-'
    if reg:
        res, sp = REG[0][1], S1
        cols = [('id', 30), ('age', 40), ('r', 64, 'residual')]
        aria = ('The residual column sorted by age. The best cut, the same scan as a regression tree, is age under 31.5. '
                'The left leaf holds A and B, the mean of minus 15 and minus 13 is minus 14. The right leaf holds C, D, E, F, '
                'the mean of 5, 9, 3, 11 is 7.')
        cap = 'A REGRESSION TREE ON r · EACH LEAF = MEAN r'
        lv = RLV; calc = {'AB': ('−15 − 13', '2', '−14'), 'CDEF': ('5 + 9 + 3 + 11', '4', '7')}
        assert {s: sum(res[k] for k in s) / len(s) for s in lv} == lv
    else:
        res, sp = CLS[0][2], S2; p = CLS[0][1]
        cols = [('id', 30), ('age', 40), ('r', 58, 'residual'), ('p(1−p)', 64, 'curvature')]
        aria = ('The residual column with p times one minus p, 0.25 on every row. The best cut is again age under 31.5. '
                'Left leaf A and B: sum of residuals minus 1 over sum of curvature 0.5 gives minus 2. Right leaf C, D, E, F: '
                '1 over 1 gives plus 1.')
        cap = 'A REGRESSION TREE ON r · EACH LEAF = Σ r / Σ p(1 − p)'
        lv = CLV; calc = {'AB': ('−0.5 − 0.5', '0.25 + 0.25', '−2'), 'CDEF': ('0.5 + 0.5 − 0.5 + 0.5', '4 × 0.25', '+1')}
        assert {s: sum(res[k] for k in s) / sum(p[k] * (1 - p[k]) for k in s) for s in lv} == lv
    f = Anim(pre, 720, 0, aria, cap)
    t = Table(0, 30, cols); f.static(t.head())
    for i, k in enumerate(IDS):
        vals = [k, str(DATA[i][1]), snum(res[k])] + ([] if reg else ['%.2f' % (p[k] * (1 - p[k]))])
        f.show(t.row(i, vals, colors={2: RO}), .2 + i * .08)
    yc = t.ry(2) - 2
    f.show(L(-4, yc, t.w + 4, yc, HL, 1.8, '5 4') + R(t.w + 8, yc - 9, 74, 18, BG, 'none', 4) +
           T(t.w + 12, yc + 4, 'age < 31.5', HL, 'start', bold=True), 1.0)
    rx, ry = 500, 60; lx = {'AB': 395, 'CDEF': 605}; ly = 140
    f.show(L(rx, ry + 13, lx['AB'], ly - 12, RULE_HI, 1.2) + L(rx, ry + 13, lx['CDEF'], ly - 12, RULE_HI, 1.2) +
           T(438, 104, 'yes', FA, 'end') + T(562, 104, 'no', FA, 'start') + qbox(rx, ry, 'age < 31.5 ?'), 1.6)
    for g, (i0, i1, t0) in {'AB': (0, 1, 2.2), 'CDEF': (2, 5, 3.4)}.items():
        a, b, v = calc[g]
        f.show(t.outline(i0, i1, c=AM, sw=1.8), t0 - .2)
        for j, k in enumerate(g):
            i = IDS.index(k); tx = lx[g] + (j - (len(g) - 1) / 2) * 57; ty = ly + 32
            sx, sy = t.cx(2), t.ry(i) + 13; tg = t0 + j * .15
            f.path(tok(tx, ty, '%s %s' % (k, snum(res[k]))), [(0, sx - tx, sy - ty), (tg, 0, 0)], tg - .1, d=.7)
        f.show(chip(lx[g], ly, v, AM, 58), t0 + 1.0)
        w = max(len(a), len(b)) * 7 + 8
        f.show(M(lx[g] - w / 2 - 6, ly + 84, '{γ} =', AM, 'end') + frac(lx[g] - w / 2, ly + 80, a, b, AM, w), t0 + 1.2)
    f.show(S(330, 266, 'best of every column × threshold · drop in variance of r = %s' % ('98' if reg else '0.125'), MU), 4.8)
    return finish(f, 280)

# ---------- 3.3 / 4.3 Update ----------
def fig_update(kind):
    reg = kind == 'reg'
    # timeline: 0.2 rows with F0 + ghost of old residual bars; 1.0 eta*h cells; 2.0 F1; (2.6 p1); 3.2 r1 + new bars; 4.2 loss pill
    pre = 'gb5-' if reg else 'gb8-'
    if reg:
        F0, F1, r0, r1 = REG[0][0], REG[1][0], REG[0][1], REG[1][1]
        cols = [('id', 30), ('F₀', 48), ('η · h', 56, 'η = 0.5'), ('F₁', 48), ('y', 40), ('r₁', 58, 'y − F₁')]
        aria = ('Half of each leaf value is added: minus 7 for A and B, plus 3.5 for C to F. F one becomes 18 and 28.5. The new '
                'residuals minus 8, minus 6, 1.5, 5.5, minus 0.5, 7.5 are shorter than the old ones shown as dashed outlines. '
                'Mean squared error falls from 105 to 31.5.')
        cap = 'ADD η × THE TREE · RESIDUALS SHRINK · NEXT TREE FITS THE NEW r'
        loss = 'MSE 105 → 31.5'
    else:
        F0, F1, r0, r1, p1 = CLS[0][0], CLS[1][0], CLS[0][2], CLS[1][2], CLS[1][1]
        cols = [('id', 30), ('F₀', 44), ('η · h', 56, 'η = 0.5'), ('F₁', 44), ('p₁', 50, 'σ(F₁)'), ('y', 34), ('r₁', 58, 'y − p₁')]
        aria = ('Half of each leaf value is added to the log-odds: minus 1 for A and B, plus 0.5 for C to F. The probabilities '
                'become 0.27 and 0.62. The new residuals are shorter than the old ones shown as dashed outlines, except for E, '
                'a non-buyer sharing the buyers\' leaf, whose residual grows to minus 0.62. Log loss still falls from 0.693 to 0.504.')
        cap = 'ADD η × THE TREE TO THE LOG-ODDS · p MOVES TOWARD y, EXCEPT E'
        loss = 'log loss 0.693 → 0.504'
    f = Anim(pre, 720, 0, aria, cap)
    t = Table(0, 30, cols); f.static(t.head())
    j = {c[0]: n for n, c in enumerate(cols)}
    for i, k in enumerate(IDS):
        f.show(t.row(i, [k, num(F0[k])], colors={1: VI}), .2 + i * .08)
        f.show(t.cell(i, j['y'], str(Y[k] if reg else B[k]), c=FI), .2 + i * .08)
    BX = t.w + 150; sc = 100 / max(abs(v) for v in list(r0.values()) + list(r1.values()))
    f.static(L(BX, t.ry(0) - 6, BX, t.ry(5) + t.rh + 4, RULE_HI, 1.2) + T(BX, t.ry(0) - 12, '0', FA, mono=True))
    for i, k in enumerate(IDS):
        v = r0[k]; y = t.ry(i) + 6; w = abs(v) * sc
        f.show(R(BX if v > 0 else BX - w, y, w, 14, 'none', RO, 2, 1, '3 2'), .4)
    lvs = RLV if reg else CLV; cx = 645; RY, LY = 62, 124
    f.static(S(cx, 38, 'tree 1 from %s' % ('3.2' if reg else '4.2'), MU, 'middle', bold=True) + stump_svg(cx, RY, LY, 'age < 31.5 ?'))
    for g, lx in (('AB', cx - 38), ('CDEF', cx + 38)):
        f.static(chip(lx, LY, snum(lvs[g]), AM, 50) + S(lx, LY + 26, ' '.join(g) if g == 'AB' else 'C–F', FA, 'middle'))
        f.show(S(lx, LY + 46, '× 0.5', AM, 'middle', bold=True), .6)
    for i, k in enumerate(IDS):
        step = F1[k] - F0[k]; lx = cx - 38 if k in 'AB' else cx + 38; ty = LY + 66
        sx, sy = t.cx(j['η · h']), t.ry(i) + 13; tg = 1.0 + i * .22
        f.path(chip(lx, ty, snum(step), AM, 52), [(0, 0, 0), (tg, sx - lx, sy - ty)], .8, d=.8, hide=tg + .9)
        f.show(t.cell(i, j['η · h'], snum(step), c=AM), tg + .75)
    for i, k in enumerate(IDS):
        f.show(t.cell(i, j['F₁'], num(F1[k], None if reg else 1), c=VI), 2.9 + i * .08)
        if not reg: f.show(t.cell(i, j['p₁'], '%.2f' % p1[k], c=VI), 3.4 + i * .08)
    for i, k in enumerate(IDS):
        v = r1[k]; y = t.ry(i) + 6; w = abs(v) * sc
        f.show(t.cell(i, j['r₁'], snum(v, None if reg else 2), c=RO) +
               R(BX if v > 0 else BX - w, y, w, 14, tn(RO, '.28'), RO, 2, 1), 4.0 + i * .1)
    f.show(S(BX - 100, 266, 'dashed: r₀ · filled: r₁', MU), 4.6)
    if not reg:
        assert abs(r1['E']) > abs(r0['E']) and all(abs(r1[k]) < abs(r0[k]) for k in IDS if k != 'E')
        yE = t.ry(4) + 13
        f.show(R(BX - abs(r1['E']) * sc - 4, yE - 11, abs(r1['E']) * sc + 8, 22, 'none', AM, 4, 1.6), 4.8)
        f.show(S(BX - 100, 286, 'E: a non-buyer in the buyers\' leaf, so its r grows', AM, bold=True), 4.8)
    f.show(pill(cx, 252, loss, 'gr'), 5.0)
    return finish(f, 300 if not reg else 280)

# ---------- 3.4 / 4.4 Prediction ----------
def fig_predict(kind):
    reg = kind == 'reg'
    # timeline: 0.3 X card; tree m at 1.0 + 1.5 m: X token walks root -> leaf, leaf ringed, eta*leaf drops into the sum row
    pre = 'gb11-' if reg else 'gb12-'
    rs, steps, FX = (RR, PR_REG, FX_REG) if reg else (CR, PR_CLS, FX_CLS)
    F0 = 25 if reg else 0
    if reg:
        aria = ('New customer X, aged 45, walks the three trees from section 3. Tree 1, age under 31.5: no, leaf 7, half is 3.5. '
                'Tree 2, the same question: no, leaf 3.5, half is 1.75. Tree 3, age under 56: yes, leaf minus 1.15, half is '
                'minus 0.575. The start value 25 plus the three steps gives a predicted spend of 29.675.')
        cap = 'X WALKS EVERY TREE · THE η × LEAVES ADD UP ON TOP OF F₀'
    else:
        aria = ('New customer X, aged 45, walks the three classification trees. The log-odds start at 0; the leaves give plus 1, '
                'plus 0.54 and minus 0.40, half of each is added: 0.5, 0.27, minus 0.20. The sum, 0.57, goes through the sigmoid: '
                'a probability of buy of 0.64, so predict buy.')
        cap = 'X WALKS EVERY TREE · LOG-ODDS ADD UP · σ GIVES THE PROBABILITY'
    f = Anim(pre, 720, 0, aria, cap)
    f.show(R(0, 30, 200, 26, BG, VI, 6, 1.4) + T(100, 47, 'new customer X · age 45', VI, bold=True), .3)
    CX = [130, 360, 590]; RY, LY, SY = 112, 180, 246
    f.static(S(22, SY - 18, 'F₀', MU, 'middle') + chip(22, SY, num(F0), VI, 40))
    nd = None if reg else 2
    for m, (rd, (left, v)) in enumerate(zip(rs, steps)):
        cx = CX[m]; T0 = 1.0 + m * 1.6
        f.static(S(cx, 74, 'tree %d' % (m + 1), MU, 'middle', bold=True) + stump_svg(cx, RY, LY, '%s < %g ?' % (rd['col'], rd['thr']), 52))
        for side in ('L', 'R'):
            g = rd[side]; lx = cx - 52 if side == 'L' else cx + 52
            f.static(chip(lx, LY, sfm(rd['g'][g]) if reg else snum(rd['g'][g], 2), AM, 62))
        lx = cx - 52 if left else cx + 52
        f.show(L(cx, RY + 13, lx, LY - 11, HL, 2.4) + qring(cx, RY, '%s < %g ?' % (rd['col'], rd['thr'])), T0 + .3)
        f.show(T(cx, RY - 20, '45 %s %g' % ('<' if left else '≥', rd['thr']), HL, 'middle', mono=True, bold=True), T0 + .4)
        f.path(chip(lx, RY - 22, 'X', VI, 26), [(0, 0, 0), (T0 + .4, 0, LY - RY + 22)], T0 - .1, d=.6, hide=T0 + 1.2)
        f.show(R(lx - 35, LY - 14, 70, 28, 'none', HL, 14, 1.8), T0 + 1.0)
        f.show(S(cx - 84, SY + 4, '+', MU, 'middle', bold=True) + chip(cx, SY, '0.5 × %s = %s' % (fm(v) if reg else num(v, 2), snum(round(ETA * v, 3)) if reg else snum(ETA * v, 2)), AM, 150), T0 + 1.1)
    tE = 1.0 + 3 * 1.6
    if reg:
        f.show(M(360, 294, '{F}(X) = 25 + 3.5 + 1.75 − 0.575 = 29.675', VI) , tE)
        f.show(chip(360, 322, 'predicted spend ≈ 29.7', GR, 200), tE + .5)
        assert [round(ETA * v, 3) for _, v in steps] == [3.5, 1.75, -.575]
    else:
        f.show(M(360, 294, '{F}(X) = 0 + 0.5 + 0.27 − 0.20 = 0.57', VI), tE)
        f.show(chip(360, 322, 'p = σ(0.57) = 0.64 → buy', GR, 220), tE + .5)
        assert [round(ETA * v, 2) for _, v in steps] == [.5, .27, -.2]
    return finish(f, 342)

# ---------- 5.3 Subsampling ----------
def sub_curve(seed, n=200, eta=.1, frac_=.5):
    g = random.Random(seed); Ft, Fv, out = [0] * len(TRN), [0] * len(VAL), []
    for _ in range(n + 1):
        out.append(sum((p[1] - fv) ** 2 for p, fv in zip(VAL, Fv)) / len(VAL))
        idx = g.sample(range(len(TRN)), int(frac_ * len(TRN)))
        t = tree([TRN[i][0] for i in idx], [TRN[i][1] - Ft[i] for i in idx], 3)
        Ft = [fv + eta * tpred(t, p[0]) for p, fv in zip(TRN, Ft)]; Fv = [fv + eta * tpred(t, p[0]) for p, fv in zip(VAL, Fv)]
    return out
SUB = sub_curve(3); SBEST = min(range(len(SUB)), key=lambda i: SUB[i])
assert SBEST == 18 and round(SUB[SBEST], 2) == 1.23 and round(SUB[-1], 2) == 1.96
G = random.Random(7); SAMP = [sorted(G.sample(IDS, 3)) for _ in range(3)]

def fig_sub():
    # timeline: tree m at 0.5 + 1.4 m: three rows lit in the table, they slide into a small box "tree m"; others greyed
    f = Anim('gb13-', 720, 0, ('Each round draws a random half of the rows without replacement and fits the tree on those alone: '
             'tree 1 sees %s, tree 2 sees %s, tree 3 sees %s. On the 40 noisy points with depth-3 trees and eta 0.1, half-row '
             'sampling gets a best validation error of %.2f against %.2f with every row.') %
             (' '.join(SAMP[0]), ' '.join(SAMP[1]), ' '.join(SAMP[2]), SUB[SBEST], ES[BEST][1]),
             'EACH TREE SEES A RANDOM HALF OF THE ROWS · subsample = 0.5')
    t = Table(0, 30, [('id', 30), ('age', 40), ('y', 46, 'spend')]); f.static(t.head())
    for i, k in enumerate(IDS): f.static(t.row(i, [k, str(DATA[i][1]), str(Y[k])], colors={2: FI}))
    for m, smp in enumerate(SAMP):
        T0 = .5 + m * 1.5; bx = 190 + m * 175
        f.static(R(bx, 52, 140, 128, 'none', RULE_HI, 8, 1.2, '4 3') + S(bx + 70, 46, 'tree %d' % (m + 1), MU, 'middle', bold=True))
        for i, k in enumerate(IDS):
            if k in smp: f.show(t.outline(i, c=AM), T0, hide=T0 + 1.2)
        for j, k in enumerate(smp):
            i = IDS.index(k); tx, ty = bx + 70, 76 + j * 34
            f.path(tok(tx, ty, k, AM), [(0, t.cx(0) - tx, t.ry(i) + 13 - ty), (T0 + .3 + j * .1, 0, 0)], T0, d=.7)
        f.static(S(bx + 70, 196, 'skips ' + ' '.join(k for k in IDS if k not in smp), FA, 'middle'))
    f.show(S(190, 236, 'best validation MSE · all rows %.2f · half the rows %.2f' % (ES[BEST][1], SUB[SBEST]), GR, bold=True), 5.0)
    f.show(S(190, 256, 'less data per tree = more varied trees = less overfit, and faster', MU), 5.2)
    return finish(f, 268)

# ---------- 5.1 Learning rate ----------
def curves(f, series, PX, PY, t0, chunks=10, dt=.25):
    """reveal each polyline in chunks; series = [(points, colour)]"""
    for pts, c in series:
        n = len(pts); cut = [round(k * (n - 1) / chunks) for k in range(chunks + 1)]
        for k in range(chunks):
            f.show(poly([(PX(x), PY(y)) for x, y in pts[cut[k]:cut[k + 1] + 1]], c, 2.2), t0 + k * dt, d=.25)

def fig_eta():
    # timeline: 0.3.. three curves drawn left to right; 3.2 MSE 5 line; 3.6 crossing dots
    f = Anim('gb9-', 720, 0, 'Training MSE on the six customers against the number of stumps, for three learning rates. With eta 1 '
             'the error drops below 5 after 2 trees, with 0.5 after 4, with 0.1 only after 27. Eta times the number of trees '
             'stays around 2 to 3.', 'SMALLER η · SMALLER STEPS · MORE TREES FOR THE SAME FIT')
    x0, x1, yb, yt = 60, 520, 250, 40
    PX = lambda m: x0 + m / 30 * (x1 - x0); PY = lambda v: yb - v / 105 * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for v in (25, 50, 75, 100): f.static(T(x0 - 7, PY(v) + 4, str(v), FA, 'end', mono=True) + L(x0, PY(v), x1, PY(v), RULE, .8))
    for m in (0, 5, 10, 15, 20, 25, 30): f.static(T(PX(m), yb + 15, str(m), FA, mono=True))
    f.static(S(x1, yb + 32, 'number of trees', MU, 'end') + S(x0, yt - 12, 'train MSE', MU))
    col = {1: FI, .5: VI, .1: AM}
    curves(f, [(list(enumerate(ECURVE[e])), col[e]) for e in ETAS], PX, PY, .3, 10, .28)
    f.show(L(x0, PY(5), x1, PY(5), GR, 1.2, '5 4') + S(x1 + 6, PY(5) + 4, 'MSE 5', GR), 3.2)
    X1 = 560
    for k, e in enumerate(ETAS):
        m = REACH[e]
        f.show(dot(PX(m), PY(ECURVE[e][m]), col[e], 5, BG), 3.6 + k * .4)
        f.show(S(X1, 70 + k * 40, 'η = %g' % e, col[e], bold=True) +
               S(X1, 88 + k * 40, '%d trees · η × trees = %g' % (m, round(e * m, 1)), MU), 3.6 + k * .4)
    return finish(f, yb + 44)

# ---------- 5.2 Early stopping ----------
def fig_stop():
    # timeline: 0.3.. train + validation curves; 3.4 best ring + stop line; 4.0 shaded overfit zone
    n = len(ES) - 1
    f = Anim('gb10-', 720, 0, ('Depth-3 trees with eta 0.1 on 40 noisy points. Training error keeps falling toward 0. Error on 400 '
             'held-out points is lowest after %d trees, %.2f, then climbs back to %.2f by %d trees: the later trees fit the noise.') %
             (BEST, ES[BEST][1], ES[-1][1], n), 'WATCH A VALIDATION SET · STOP WHERE ITS ERROR IS LOWEST')
    x0, x1, yb, yt = 60, 520, 250, 40
    PX = lambda m: x0 + m / n * (x1 - x0); PY = lambda v: yb - v / 6 * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for v in (2, 4, 6): f.static(T(x0 - 7, PY(v) + 4, str(v), FA, 'end', mono=True) + L(x0, PY(v), x1, PY(v), RULE, .8))
    for m in (0, 50, 100, 150, 200): f.static(T(PX(m), yb + 15, str(m), FA, mono=True))
    f.static(S(x1, yb + 32, 'number of trees', MU, 'end') + S(x0, yt - 12, 'MSE', MU))
    f.show(R(PX(BEST), yt, PX(n) - PX(BEST), yb - yt, tn(RO, '.06'), 'none', 0) +
           S((PX(BEST) + PX(n)) / 2, yt + 18, 'more trees · fits the noise', RO, 'middle'), 4.0)
    curves(f, [([(m, ES[m][0]) for m in range(n + 1)], FI), ([(m, ES[m][1]) for m in range(n + 1)], VI)], PX, PY, .3, 10, .28)
    f.show(S(PX(n) - 4, PY(ES[-1][0]) - 8, 'train', FI, 'end', bold=True) + S(PX(n) - 4, PY(ES[-1][1]) - 10, 'validation', VI, 'end', bold=True), 3.0)
    f.show(L(PX(BEST), yb, PX(BEST), yt + 26, GR, 1.4, '4 3') +
           '<circle cx="%.1f" cy="%.1f" r="9" fill="none" stroke="%s" stroke-width="2"/>' % (PX(BEST), PY(ES[BEST][1]), GR), 3.4)
    X1 = 560
    f.show(S(X1, 80, 'stop at %d trees' % BEST, GR, bold=True) + S(X1, 98, 'validation %.2f' % ES[BEST][1], GR), 3.6)
    f.show(S(X1, 140, 'keep going to %d' % n, RO, bold=True) + S(X1, 158, 'validation %.2f' % ES[-1][1], RO) +
           S(X1, 176, 'train %.2f' % ES[-1][0], FI), 4.2)
    return finish(f, yb + 44)

EQ_UPDATE = r'''    <div class="eq">
    <div class="line">
      <span class="t"><span><var>F</var><sub><var>m</var></sub>(<var>x</var>)</span><em>prediction after m trees</em></span>
      <span class="op">=</span>
      <span class="t"><span><var>F</var><sub><var>m</var>−1</sub>(<var>x</var>)</span><em>what the earlier trees say</em></span>
      <span class="op">+</span>
      <span class="t p"><span><var>η</var> · <var>h</var><sub><var>m</var></sub>(<var>x</var>)</span><em>new tree, scaled by the learning rate</em></span>
    </div>
  </div>'''

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Tree models</p>
  <h1>Gradient <em>boosting</em></h1>
  <p class="lede">Gradient boosting adds <b>shallow trees one after another</b>, each one fitted to what the trees before it still get wrong, and adds only a fraction <span class="mth"><var>η</var></span> of each.</p>
</header>

<section id="gb-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Start from one guess; every round a small tree learns the <em>residual</em> and moves the prediction <em>part of the way</em> toward the truth.</p>
{gb1}
  <ul class="why">
    <li>The same six customers as the <a href="../decision-tree/index.html">Decision tree</a>; every tree here is a single split (a <b>stump</b>), <span class="mth"><var>η</var> = 0.5</span>.</li>
    <li>Trees are <b>added</b>, not averaged: the prediction is the start value plus <span class="mth"><var>η</var></span> × every tree.</li>
    <li><a href="../random-forest/index.html">Random forest</a> grows deep trees in parallel; boosting grows shallow ones in sequence.</li>
  </ul>
</section>

<section id="gb-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Residual as gradient</h2></div>
  <p class="key">The residual is the <em>negative gradient of the loss</em>, so each tree is one step of gradient descent on the predictions.</p>
''' + EQ_UPDATE + r'''
  <div class="eq">
    <div class="line">
      <span class="t r"><span><var>r</var><sub><var>i</var></sub></span><em>pseudo-residual of row i</em></span>
      <span class="op">=</span>
      <span class="t"><span>− <span class="frac"><i>∂ <var>L</var>(<var>y</var><sub><var>i</var></sub>, <var>F</var>)</i><i>∂ <var>F</var></i></span></span><em>downhill direction of the loss</em></span>
    </div>
  </div>
{gb2}
  <ul class="why">
    <li>Pick a loss <span class="mth"><var>L</var></span>; it decides the start value, the residual and the leaf value. Everything else is the same loop.</li>
    <li>The tree is always a <b>regression tree</b> on <span class="mth"><var>r</var></span>, even when the task is classification.</li>
  </ul>
</section>

<section id="gb-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Regression</h2></div>
  <p class="key">Squared loss <span class="mth">½(<var>y</var> − <var>F</var>)²</span>: the residual is the plain <em>error</em>, and a leaf returns its <em>mean</em>.</p>
  <div class="subsec" id="gb-s3-1">
    <h3 class="ssh"><b>3.1</b>Residual</h3>
    <p class="skey">Start every row at the <em>mean of y</em>; the residual is what that guess misses.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>F</var><sub>0</sub></span><em>start value</em></span>
      <span class="op">=</span>
      <span class="t"><span><var>ȳ</var></span><em>mean of y</em></span>
      <span class="op">,</span>
      <span class="t r"><span><var>r</var><sub><var>i</var></sub> = <var>y</var><sub><var>i</var></sub> − <var>F</var>(<var>x</var><sub><var>i</var></sub>)</span><em>error of row i</em></span>
    </div>
  </div>
{gb3}
    <ul class="why">
      <li>The mean is the single number with the lowest squared loss, so it is the best tree with zero splits.</li>
    </ul>
  </div>
  <div class="subsec" id="gb-s3-2">
    <h3 class="ssh"><b>3.2</b>Tree on the residual</h3>
    <p class="skey">Grow a small regression tree with <em>r as the label</em>; each leaf returns the mean residual.</p>
  <div class="eq">
    <div class="line">
      <span class="t p"><span><var>γ</var><sub><var>j</var></sub></span><em>value of leaf j</em></span>
      <span class="op">=</span>
      <span class="t"><span><span class="frac"><i>Σ<sub><var>i</var> ∈ <var>j</var></sub> <var>r</var><sub><var>i</var></sub></i><i><var>n</var><sub><var>j</var></sub></i></span></span><em>mean residual in the leaf</em></span>
    </div>
  </div>
{gb4}
    <ul class="why">
      <li>The split search is exactly the variance scan of the <a href="../decision-tree/index.html">Decision tree</a>, run on <span class="mth"><var>r</var></span> instead of <span class="mth"><var>y</var></span>.</li>
      <li>Trees are kept shallow: <code>max_depth</code> 3 to 6 in practice, one split here.</li>
    </ul>
  </div>
  <div class="subsec" id="gb-s3-3">
    <h3 class="ssh"><b>3.3</b>Update</h3>
    <p class="skey">Add <em>η × the leaf value</em> to every row, recompute the residual, fit the next tree.</p>
''' + EQ_UPDATE.replace('    <div class="eq">', '  <div class="eq">') + r'''
{gb5}
    <ul class="why">
      <li>The next tree sees the new residual column: <span class="mth"><var>r</var><sub>1</sub></span> replaces <span class="mth"><var>r</var><sub>0</sub></span>, the table and the loop stay the same.</li>
    </ul>
  <div class="subsec" id="gb-s3-4">
    <h3 class="ssh"><b>3.4</b>Prediction</h3>
    <p class="skey">A new row walks <em>every tree</em>; its prediction is <span class="mth"><var>F</var><sub>0</sub></span> plus <span class="mth"><var>η</var></span> × each leaf it lands in.</p>
{gb11}
    <ul class="why">
      <li>The trees never vote: their scaled leaf values are <b>summed</b>, so a later tree can pull the answer back down (tree 3 here).</li>
    </ul>
  </div>
</section>

<section id="gb-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Classification</h2></div>
  <p class="key">Log loss: <span class="mth"><var>F</var></span> is the <em>log-odds</em>, the residual is <em>label − probability</em>, and a leaf divides by the curvature.</p>
  <div class="subsec" id="gb-s4-1">
    <h3 class="ssh"><b>4.1</b>Residual</h3>
    <p class="skey">Start every row at the <em>log-odds of the base rate</em>; the residual is <span class="mth"><var>y</var> − <var>p</var></span>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>p</var></span><em>probability of buy</em></span>
      <span class="op">=</span>
      <span class="t"><span><b class="fn">σ</b>(<var>F</var>)</span><em>sigmoid of the log-odds</em></span>
      <span class="op">,</span>
      <span class="t r"><span><var>r</var><sub><var>i</var></sub> = <var>y</var><sub><var>i</var></sub> − <var>p</var><sub><var>i</var></sub></span><em>negative gradient of log loss</em></span>
    </div>
  </div>
{gb6}
    <ul class="why">
      <li>The trees add up in <b>log-odds</b>, which can be any number; only at the end does <span class="mth"><b class="fn">σ</b></span> turn it into a probability — as in <a href="../../05-classical-ml/logistic-regression/index.html">Logistic regression</a>.</li>
    </ul>
  </div>
  <div class="subsec" id="gb-s4-2">
    <h3 class="ssh"><b>4.2</b>Tree on the residual</h3>
    <p class="skey">The same regression tree on <span class="mth"><var>r</var></span>; the leaf value is <em>one Newton step</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t p"><span><var>γ</var><sub><var>j</var></sub></span><em>value of leaf j</em></span>
      <span class="op">=</span>
      <span class="t"><span><span class="frac"><i>Σ<sub><var>i</var> ∈ <var>j</var></sub> <var>r</var><sub><var>i</var></sub></i><i>Σ<sub><var>i</var> ∈ <var>j</var></sub> <var>p</var><sub><var>i</var></sub>(1 − <var>p</var><sub><var>i</var></sub>)</i></span></span><em>gradient over curvature</em></span>
    </div>
  </div>
{gb7}
    <ul class="why">
      <li>A residual of 0.5 means little in log-odds; dividing by <span class="mth"><var>p</var>(1 − <var>p</var>)</span> converts it into the right log-odds step.</li>
      <li>With squared loss the curvature is 1 per row, so the same formula gives the mean of 3.2.</li>
    </ul>
  </div>
  <div class="subsec" id="gb-s4-3">
    <h3 class="ssh"><b>4.3</b>Update</h3>
    <p class="skey">Add <em>η × the leaf value</em> to the log-odds, map back with <span class="mth"><b class="fn">σ</b></span>, recompute the residual.</p>
''' + EQ_UPDATE.replace('    <div class="eq">', '  <div class="eq">') + r'''
{gb8}
    <ul class="why">
      <li>More than two classes: one tree per class per round, one log-odds per class, softmax at the end.</li>
    </ul>
  <div class="subsec" id="gb-s4-4">
    <h3 class="ssh"><b>4.4</b>Prediction</h3>
    <p class="skey">The same walk, summed in <em>log-odds</em>; <span class="mth"><b class="fn">σ</b></span> turns the sum into a probability.</p>
{gb12}
    <ul class="why">
      <li><code>predict_proba</code> returns <span class="mth"><b class="fn">σ</b>(<var>F</var>)</span>; <code>predict</code> says buy when it is at least 0.5.</li>
    </ul>
  </div>
</section>

<section id="gb-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Learning rate &amp; stopping</h2></div>
  <p class="key">The two knobs that matter most: <em>how big each step is</em> and <em>how many steps to take</em>.</p>
  <div class="subsec" id="gb-s5-1">
    <h3 class="ssh"><b>5.1</b>Learning rate</h3>
    <p class="skey">A smaller <span class="mth"><var>η</var></span> takes smaller steps, so it needs <em>more trees</em> for the same fit.</p>
{gb9}
    <ul class="why">
      <li><code>learning_rate</code> and <code>n_estimators</code> trade off: halve one, roughly double the other.</li>
      <li>Small steps generalise better, because no single tree can push the model far: the usual recipe is <span class="mth"><var>η</var></span> 0.05–0.1 and many trees.</li>
    </ul>
  </div>
  <div class="subsec" id="gb-s5-2">
    <h3 class="ssh"><b>5.2</b>Early stopping</h3>
    <p class="skey">Keep adding trees while a <em>validation error</em> still falls; stop when it turns up.</p>
{gb10}
    <ul class="why">
      <li>Training error always keeps falling, so it cannot tell you when to stop — see <a href="../../04-core-concepts/train-val-test-cv/index.html">Train, validation &amp; test</a>.</li>
      <li>Set <code>n_estimators</code> high as a ceiling and let <code>n_iter_no_change</code> (or <code>early_stopping_rounds</code>) pick the number.</li>
    </ul>
  <div class="subsec" id="gb-s5-3">
    <h3 class="ssh"><b>5.3</b>Subsampling</h3>
    <p class="skey">Fit each tree on a <em>random fraction of the rows</em>: <b>stochastic gradient boosting</b>.</p>
{gb13}
    <ul class="why">
      <li><code>subsample</code> 0.5–0.8 is typical; below 1 it also gives an out-of-bag error estimate for free.</li>
      <li>Shallow trees are the other brake: <code>max_depth</code> 3 is the usual default, because each tree only needs to fix part of the error.</li>
    </ul>
  </div>
</section>

<script>
/* Figures start when first scrolled into view, play once and hold their final state. Click a figure to replay. */
(function () {
  if (!window.IntersectionObserver || !document.getAnimations) return;
  var svgs = [].slice.call(document.querySelectorAll("figure svg[data-anim]"));
  if (!svgs.length) return;
  function anims(s) {
    return document.getAnimations().filter(function (a) { var t = a.effect && a.effect.target; return t && s.contains(t); });
  }
  function restart(s) { anims(s).forEach(function (a) { a.currentTime = 0; a.play(); }); }
  svgs.forEach(function (s) { anims(s).forEach(function (a) { a.pause(); a.currentTime = 0; }); });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting || e.target.__played) return;
      e.target.__played = true; restart(e.target); io.unobserve(e.target);
    });
  }, { threshold: 0.4 });
  svgs.forEach(function (s) {
    io.observe(s); s.style.cursor = "pointer";
    s.addEventListener("click", function () { restart(s); });
  });
})();
</script>

<footer>Machine learning · Tree models · next lesson in the branch: <a href="../xgboost/index.html">XGBoost</a>.</footer>
'''

def build():
    figs = dict(gb1=fig_mental(), gb2=fig_gradient(), gb3=fig_resid('reg'), gb4=fig_leaf('reg'), gb5=fig_update('reg'),
                gb6=fig_resid('cls'), gb7=fig_leaf('cls'), gb8=fig_update('cls'), gb9=fig_eta(), gb10=fig_stop(),
                gb11=fig_predict('reg'), gb12=fig_predict('cls'), gb13=fig_sub())
    return re.sub(r'\{(gb\d+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'Shallow trees added one after another, each fitted to the residual (the negative gradient of the loss) '
           'and scaled by η: regression, classification, prediction, learning rate, early stopping and subsampling.')
