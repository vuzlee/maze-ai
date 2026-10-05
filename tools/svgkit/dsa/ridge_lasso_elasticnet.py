# -*- coding: utf-8 -*-
"""Figures + page body for content/07-machine-learning/05-classical-ml/ridge-lasso-elasticnet.
Run: python3 ridge_lasso_elasticnet.py -> rewrites the lesson body (hero .. replay script).
Data: 6 standardized rows, x1 and x2 nearly identical (corr 0.9999), x3 x4 noise, y = 2 x1 + noise.
Coefficients below were computed by exact ridge solves and coordinate-descent lasso on that table."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, MU, TX, FA, BR, VI, FI, RO, GH, RULE, RULE_HI, BG, SUNK,
                            tn, M, S, chip, dot, poly, Plane, finish, splice)
from tablefig import Table, arrow
PAGE = os.path.join(HERE, '../../../content/07-machine-learning/05-classical-ml/ridge-lasso-elasticnet/index.html')

X1 = [-0.84, 0.36, 1.44, -0.40, -1.46, 0.90]
Y = [-0.82, 0.17, 2.19, -0.85, -2.15, 1.47]
XY = [round(a * b, 2) for a, b in zip(X1, Y)]
XX = [round(a * a, 2) for a in X1]
SXY, SXX = round(sum(XY), 2), round(sum(XX), 2)
assert (SXY, SXX) == (8.70, 6.01), (SXY, SXX)
def w1d(lam): return SXY / (SXX + lam)
assert [round(w1d(l), 2) for l in (0, 1, 10, 100)] == [1.45, 1.24, 0.54, 0.08]

OLS = [17.22, -15.57, 0.32, 0.23]
RIDGE1 = [0.71, 0.70, 0.02, 0.14]
PATH = {-3: [2.86, -1.24, 0.10, 0.27], -2: [1.03, 0.57, 0.07, 0.27], -1: [0.82, 0.77, 0.06, 0.25],
        0: [0.71, 0.70, 0.02, 0.14], 1: [0.38, 0.38, -0.04, -0.07], 2: [0.08, 0.08, -0.01, -0.03]}
SSE = {-3: 0.06, -2: 0.08, -1: 0.08, 0: 0.24, 1: 3.03, 2: 10.26}
ENET = {0: [0.64, 0.64, -0.01, 0.07], .5: [0.63, 0.63, 0.0, 0.0], 1: [1.28, 0.0, 0.0, 0.0]}
DROP = [(1, [1.32, 0.0]), (4, [1.18, 0.0]), (6, [0.0, 1.22])]
FEAT = [('{x}₁', 'income'), ('{x}₂', 'income, other unit'), ('{x}₃', 'noise'), ('{x}₄', 'noise')]

def frac(cx, cy, num, den, c=TX, w=None):
    w = w or max(len(re.sub(r'[{}]', '', num)), len(re.sub(r'[{}]', '', den))) * 7.5 + 12
    return M(cx, cy - 7, num, c) + L(cx - w / 2, cy, cx + w / 2, cy, c, 1.1) + M(cx, cy + 17, den, c)

def vbar(x, y0, v, sc, c, w=34, fill=None):
    h = abs(v) * sc
    y = y0 - h if v >= 0 else y0
    return R(x - w / 2, y, w, max(h, 1.5), fill or tn(c, '.22'), c, 3, 1.3)

# ---------- 1. Mental model ----------
def fig_mental():
    f = Anim('rl1-', 720, 0, 'Four coefficient bars. Fitted with no penalty, x1 shoots to +17.2 and x2 to −15.6: the two '
             'nearly identical columns cancel each other. Adding the penalty lambda times the sum of squared weights '
             'pulls every bar back: 0.71, 0.70, 0.02, 0.14, while the training error barely moves.',
             'NO PENALTY → HUGE CANCELLING WEIGHTS · PENALTY → SMALL WEIGHTS')
    Y0, SC = 160, 5.6
    xs = [90 + k * 92 for k in range(4)]
    f.static(L(30, Y0, 420, Y0, RULE_HI, 1.2))
    for x, (sym, name) in zip(xs, FEAT):
        f.static(M(x, 276, sym, TX) + T(x, 292, name, FA, cls='sv-d'))
    f.show(S(30, 44, 'no penalty: minimize error only', BR, bold=True), .3, hide=4.6)
    for k, (x, v) in enumerate(zip(xs, OLS)):
        ty = Y0 - abs(v) * SC - 6 if v >= 0 else Y0 + abs(v) * SC + 16
        f.show(vbar(x, Y0, v, SC, BR) + T(x, ty, '%+.2f' % v, BR, mono=True), .7 + k * .3, hide=4.6)
    f.show(R(xs[0] - 34, 46, xs[1] - xs[0] + 68, 222, 'none', VI, 6, 1.6, '5 4') +
           S(xs[1] + 44, 70, '+17.2 and −15.6 cancel:', VI) + S(xs[1] + 44, 86, 'x₁ ≈ x₂, so any pair', VI) +
           S(xs[1] + 44, 102, 'with the same sum fits', VI), 2.3, hide=4.6)
    f.show(R(495, 146, 130, 28, tn(VI, '.12'), VI, 14, 1.3) + M(560, 165, 'add  {λ} Σ {w}²', VI), 4.4)
    for k, (x, v, g) in enumerate(zip(xs, RIDGE1, OLS)):
        f.show(vbar(x, Y0, g, SC, GH, fill='none'), 4.8)
        ty = Y0 - abs(v) * SC - 8 if v >= 0 else Y0 + abs(v) * SC + 16
        f.show(vbar(x, Y0, v, SC, FI) + T(x, ty, '%+.2f' % v, FI, mono=True, bold=True), 5.1 + k * .25)
    f.show(M(560, 210, 'Σ {w}² : 539 → 1.0', FI) + M(560, 236, 'train error : 0.004 → 0.24', MU), 6.4)
    return finish(f, 304)

# ---------- 2. General formula, worked ----------
def fig_worked():
    f = Anim('rl2-', 720, 0, 'Ridge with one feature worked on six rows. Each row gets x times y and x squared. The sums are '
             '8.70 and 6.01. The ridge weight is the sum of x y over the sum of x squared plus lambda: 1.45 with lambda 0, '
             '1.24 with lambda 1, 0.54 with lambda 10. A plot shows the three fitted lines flattening.',
             'RIDGE, ONE FEATURE · w = Σ xy / (Σ x² + λ)')
    t = Table(0, 30, [('row', 40), ('x', 62, 'x₁'), ('y', 62), ('x · y', 70), ('x²', 62)], step=28, rh=24)
    f.static(t.head())
    for i in range(6):
        f.show(t.row(i, [str(i + 1), '%.2f' % X1[i], '%.2f' % Y[i], '', '']), .2 + i * .08)
    tt = 1.0
    for i in range(6):
        f.show(t.outline(i, c=VI), tt, hide=tt + .55, d=.2)
        f.show(t.cell(i, 3, '%.2f' % XY[i]) + t.cell(i, 4, '%.2f' % XX[i]), tt + .25, d=.2)
        tt += .55
    yb = t.bottom(6) if hasattr(t, 'bottom') else t.ry(6)
    f.show(L(t.colx(3), yb + 4, t.x + t.w, yb + 4, TX, 1.2) + T(t.colx(0) + 20, yb + 22, 'Σ', MU) +
           T(t.cx(3), yb + 22, '8.70', BR, mono=True, bold=True) + T(t.cx(4), yb + 22, '6.01', BR, mono=True, bold=True), tt + .1)
    # formula
    fx = 420
    f.show(M(fx, 52, '{w}  =', TX, 'start') + frac(fx + 92, 48, 'Σ {x}{y}', 'Σ {x}² + {λ}', TX, 84), tt + .7)
    rows = [(0, BR), (1, VI), (10, FI)]
    for k, (lam, c) in enumerate(rows):
        y = 116 + k * 50
        t0 = tt + 1.4 + k * 1.1
        f.show(M(fx, y + 5, '{λ} = %d :' % lam, c, 'start') + frac(fx + 120, y, '8.70', '6.01 + %d' % lam, TX, 70) +
               M(fx + 170, y + 5, '= %.2f' % w1d(lam), c, 'start'), t0)
    # mini plot
    P = Plane(150, 370, 60, 24)
    tp = tt + 4.8
    f.show(L(P.X(-1.6), P.Y(0), P.X(1.6), P.Y(0), RULE_HI, 1) + L(P.X(0), P.Y(-2.3), P.X(0), P.Y(2.3), RULE_HI, 1) +
           M(P.X(1.6) + 8, P.Y(0) + 5, '{x}', MU, 'start') + M(P.X(0) + 8, P.Y(2.3) + 4, '{y}', MU, 'start') +
           ''.join(dot(*P(a, b), BR, 3.2) for a, b in zip(X1, Y)), tp - .5)
    for k, (lam, c) in enumerate(rows):
        w = w1d(lam)
        f.show(poly([P(-1.55, -1.55 * w), P(1.55, 1.55 * w)], c, 2.2) + M(P.X(1.6) + 6, P.Y(1.55 * w) + 4 + {0: -6, 1: 4, 2: 8}[k], '{λ} = %d' % lam, c, 'start'), tp + k * .5)
    f.show(S(360, 374, 'larger λ → flatter line', FI, 'start', True), tp + 1.6)
    return finish(f, 432)

# ---------- 3. geometry ----------
def fig_geom(pre, kind):
    lasso = kind == 'l1'
    cc, A = ((2, .3), 2.2)
    sol = (1.2, 0.0) if lasso else (1.178, 0.229)
    k_end = (sol[0] - cc[0]) ** 2 + A * (sol[1] - cc[1]) ** 2
    aria = ('Weight plane w1, w2. The unpenalized solution sits at (2, 0.3). The allowed region for the ' +
            ('L1 penalty is a diamond with corners on the axes. Error contours grow from the solution until one touches '
             'the diamond, at its corner (1.2, 0): w2 is exactly 0.' if lasso else
             'L2 penalty is a circle. Error contours grow from the solution until one touches the circle at (1.18, 0.23): '
             'both weights shrink but neither is 0.'))
    f = Anim(pre, 720, 0, aria, ('L1 · THE CONTOUR HITS A CORNER → w₂ = 0' if lasso else 'L2 · THE CONTOUR TOUCHES A ROUND EDGE → BOTH ≠ 0'))
    P = Plane(150, 200, 78)
    f.static(L(P.X(-1.7), P.Y(0), P.X(2.9), P.Y(0), RULE_HI, 1.2) + L(P.X(0), P.Y(-1.7), P.X(0), P.Y(1.7), RULE_HI, 1.2) +
             M(P.X(2.9) + 8, P.Y(0) + 5, '{w}₁', MU, 'start') + M(P.X(0), P.Y(1.7) - 8, '{w}₂', MU))
    f.show(dot(*P(*cc), BR, 4.5) + L(P.X(cc[0]), P.Y(cc[1]), P.X(cc[0]) + 70, P.Y(1.45), BR, 1, '3 3') +
           M(P.X(cc[0]) + 74, P.Y(1.45) + 4, 'ŵ', BR, 'start') + S(P.X(cc[0]) + 88, P.Y(1.45) + 4, 'no penalty', BR), .3)
    r = 1.2
    shape = (poly([P(r, 0), P(0, r), P(-r, 0), P(0, -r), P(r, 0)], FI, 2, fill=tn(FI, '.10')) if lasso else
             '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="2"/>' % (P.X(0), P.Y(0), r * P.sx, tn(FI, '.10'), FI))
    f.show(shape, 1.0)
    f.show(M(P.X(-0.9), P.Y(-1.35), ('|{w}₁| + |{w}₂| ≤ {t}' if lasso else '{w}₁² + {w}₂² ≤ {t}'), FI), 1.3)
    ks = [k_end * .12, k_end * .4, k_end]
    for i, k in enumerate(ks):
        rx, ry = math.sqrt(k) * P.sx, math.sqrt(k / A) * P.sy
        last = i == len(ks) - 1
        f.show('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="%s"/>' %
               (P.X(cc[0]), P.Y(cc[1]), rx, ry, VI if last else RULE_HI, 1.8 if last else 1.2), 2.0 + i * .7)
    f.show(S(P.X(cc[0]), P.Y(-1.3), 'error contours grow', VI, 'middle'), 2.2)
    tx, ty = P(*sol)
    f.show('<circle cx="%.1f" cy="%.1f" r="9" fill="none" stroke="%s" stroke-width="2"/>' % (tx, ty, VI) + dot(tx, ty, FI, 5), 4.2)
    # right panel: the two weights
    bx, Y0, SC = 520, 190, 60
    f.show(L(bx - 40, Y0, bx + 140, Y0, RULE_HI, 1.2) + M(bx, Y0 + 22, '{w}₁', TX) + M(bx + 100, Y0 + 22, '{w}₂', TX), 4.6)
    f.show(vbar(bx, Y0, sol[0], SC, FI, 40) + T(bx, Y0 - sol[0] * SC - 8, '%.2f' % sol[0], FI, mono=True, bold=True), 4.9)
    if lasso:
        f.show(L(bx + 80, Y0, bx + 120, Y0, VI, 3) + T(bx + 100, Y0 - 10, '0 exactly', VI, bold=True), 5.2)
        f.show(S(bx + 50, 244, 'the corner sits on an axis', MU, 'middle') + S(bx + 50, 262, '→ feature x₂ is dropped', FI, 'middle', True), 5.7)
    else:
        f.show(vbar(bx + 100, Y0, sol[1], SC, FI, 40) + T(bx + 100, Y0 - sol[1] * SC - 8, '%.2f' % sol[1], FI, mono=True, bold=True), 5.2)
        f.show(S(bx + 50, 244, 'a circle has no corner', MU, 'middle') + S(bx + 50, 262, '→ both shrink, none hits 0', FI, 'middle', True), 5.7)
    return finish(f, 340)

# ---------- 3.3 Elastic Net ----------
def fig_enet():
    f = Anim('rl5-', 720, 0, 'The same four features fitted by Elastic Net at three mixes rho. rho 0 (pure ridge): all four '
             'weights small, none zero. rho 0.5: the twin columns stay together at 0.63 each and both noise columns hit 0. '
             'rho 1 (pure lasso): one twin takes all the weight 1.28 and the other drops to 0.',
             'ELASTIC NET · SLIDE ρ FROM PURE L2 TO PURE L1')
    # slider
    sx0, sx1, sy = 120, 600, 46
    f.static(L(sx0, sy, sx1, sy, RULE_HI, 3) + M(sx0, sy + 22, '{ρ} = 0', MU) + M((sx0 + sx1) / 2, sy + 22, '0.5', MU) +
             M(sx1, sy + 22, '1', MU) + S(sx0 - 14, sy + 4, 'L2', MU, 'end') + S(sx1 + 14, sy + 4, 'L1', MU))
    knob = '<circle cx="%.1f" cy="%.1f" r="8" fill="%s" stroke="%s" stroke-width="2"/>' % (sx0, sy, BG, VI)
    half = (sx1 - sx0) / 2
    f.path(knob, [(0, 0, 0), (2.6, half, 0), (5.0, 2 * half, 0)], .3, d=.8)
    Y0, SC = 210, 70
    for g, rho in enumerate((0, .5, 1)):
        gx = sx0 + g * half
        t0 = .8 + g * 2.4
        ws = ENET[rho]
        f.static(L(gx - 82, Y0, gx + 82, Y0, RULE_HI, 1))
        for k, v in enumerate(ws):
            x = gx - 60 + k * 40
            f.static(M(x, Y0 + 22, FEAT[k][0], MU))
            if abs(v) < .005:
                f.show(L(x - 12, Y0, x + 12, Y0, VI, 3) + T(x, Y0 - 8, '0', VI, mono=True, bold=True), t0 + .2 + k * .12)
            else:
                c = FI if (rho == .5 and k < 2) else BR
                f.show(vbar(x, Y0, v, SC, c, 26) + T(x, Y0 - abs(v) * SC - 6, '%.2f' % v, c, mono=True) if v > 0 else
                       vbar(x, Y0, v, SC, c, 26) + T(x, Y0 - 8, '%.2f' % v, c, mono=True),
                       t0 + .2 + k * .12)
        notes = {0: ('nothing is 0', MU), .5: ('twins kept together,', FI), 1: ('one twin takes all', RO)}
        f.show(S(gx, Y0 + 50, notes[rho][0], notes[rho][1], 'middle', True), t0 + .9)
        if rho == .5:
            f.show(S(gx, Y0 + 68, 'noise dropped', FI, 'middle', True), t0 + 1.0)
    return finish(f, 292)

# ---------- 4.1 lambda path ----------
def fig_path():
    f = Anim('rl6-', 720, 0, 'Ridge weights as lambda sweeps from 0.001 to 100 on a log scale. At 0.001 the twin weights are '
             'still 2.86 and −1.24; by 0.1 they agree at about 0.8; at 100 every weight is near 0. The training error stays '
             'under 0.3 until lambda 1 and then climbs to 3.0 and 10.3.', 'SWEEP λ ON A LOG SCALE')
    P = Plane(380, 170, 90, 34)
    f.static(L(P.X(-3), P.Y(0), P.X(2), P.Y(0), RULE_HI, 1.2) + L(P.X(-3), P.Y(-1.4), P.X(-3), P.Y(3.1), RULE_HI, 1.2))
    for e in range(-3, 3):
        f.static(T(P.X(e), 262, '10' + {-3: '⁻³', -2: '⁻²', -1: '⁻¹', 0: '⁰', 1: '¹', 2: '²'}[e], FA, cls='sv-d'))
    f.static(M(P.X(2) + 14, 266, '{λ}', MU, 'start') +
             T(P.X(-3) - 8, P.Y(0) + 4, '0', FA, 'end'))
    f.static(S(P.X(-3) - 10, 290, 'train error', MU, 'end'))
    cols = [BR, VI, GH, GH]
    names = ['{w}₁', '{w}₂', '{w}₃', '{w}₄']
    es = list(range(-3, 3))
    for e0 in range(-3, 2):
        t0 = .6 + (e0 + 3) * .9
        for j in range(4):
            a, b = PATH[e0][j], PATH[e0 + 1][j]
            f.show(poly([P(e0, a), P(e0 + 1, b)], cols[j], 2.4 if j < 2 else 1.4), t0, d=.6)
    for e in es:
        t0 = .6 + (e + 3) * .9
        f.show(T(P.X(e), 290, '%.2f' % SSE[e], RO if SSE[e] > 1 else FI, mono=True, bold=SSE[e] > 1), t0)
    marker = L(P.X(-3), P.Y(3.1), P.X(-3), P.Y(-1.4), VI, 1.4, '4 3')
    f.path(marker, [(0, 0, 0)] + [(.6 + k * .9, (k + 1) * P.sx, 0) for k in range(5)], .3, d=.6, hide=5.6)
    for j in range(2):
        f.show(M(P.X(-3) - 10, P.Y(PATH[-3][j]) + 5, names[j], cols[j], 'end'), .5)
    f.show(R(P.X(-1.2), P.Y(3.0), P.X(.4) - P.X(-1.2), 220, tn(FI, '.08'), 'none', 4) +
           S(P.X(-.4), P.Y(3.0) + 16, 'sweet spot', FI, 'middle', True), 6.0)
    f.show(R(P.X(1.3), P.Y(3.0), P.X(2.15) - P.X(1.3), 220, tn(RO, '.08'), 'none', 4) +
           S(P.X(1.72), P.Y(3.0) + 16, 'underfit', RO, 'middle', True), 6.5)
    return finish(f, 304)

# ---------- 4.2 standardize ----------
def fig_scale():
    big = SXY / 100, SXX / 10000
    w0 = big[0] / big[1]; w1 = big[0] / (big[1] + 1)
    assert round(w0) == 145 and round(w1, 3) == 0.087
    f = Anim('rl7-', 720, 0, 'The same feature in two units, lambda = 1. In standard units the sums are 8.70 and 6.01, the '
             'weight goes from 1.45 to 1.24, keeping 86 percent. Measured in hundreds, the sums become 0.087 and 0.0006, '
             'the weight should be 145 but ridge gives 0.087, keeping 0.06 percent: the feature is wiped out only '
             'because of its unit.', 'SAME FEATURE, TWO UNITS · λ = 1')
    rows = [('standardized {x}', '8.70', '6.01', w1d(0), w1d(1), FI),
            ('{x} / 100', '0.087', '0.0006', w0, w1, RO)]
    for k, (lab, a, b, wa, wb, c) in enumerate(rows):
        y = 70 + k * 110
        t0 = .4 + k * 3.2
        f.show(M(0, y + 5, lab, TX, 'start'), t0)
        f.show(M(150, y + 5, 'no penalty:', MU, 'start') + frac(268, y, a, b, TX, 64) + M(310, y + 5, '= %s' % ('%.2f' % wa if wa < 10 else '%.0f' % wa), BR, 'start'), t0 + .5)
        f.show(M(150, y + 55, 'ridge:', MU, 'start') + frac(268, y + 50, a, b + ' + 1', TX, 84) +
               M(318, y + 55, '= %s' % ('%.2f' % wb if wb > .5 else '%.3f' % wb), c, 'start'), t0 + 1.4)
        keep = wb / wa
        bx, bw = 470, 220
        f.show(R(bx, y + 18, bw, 18, SUNK, RULE_HI, 3) + R(bx, y + 18, max(bw * keep, 2), 18, tn(c, '.35'), c, 3, 1.3) +
               S(bx, y + 8, 'weight kept', MU) + T(bx + bw, y + 54, '%s%%' % ('%.0f' % (keep * 100) if keep > .5 else '%.2f' % (keep * 100)), c, 'end', mono=True, bold=True), t0 + 2.2)
    f.show(S(0, 300, 'λ punishes the raw number, so a small unit means a big weight means a big penalty → scale first', VI, bold=True), 7.4)
    return finish(f, 316)

# ---------- 5.1 lasso flips ----------
def fig_flip():
    f = Anim('rl8-', 720, 0, 'Lasso is refit three times, each time leaving out one of the six rows. Leaving out row 1 or row 4, '
             'lasso keeps x1 (1.32, 1.18) and sets x2 to 0. Leaving out row 6, it flips: x1 is 0 and x2 gets 1.22. '
             'The predictions are almost the same, only the chosen twin changes.', 'LASSO PICKS ONE TWIN · DROP ONE ROW AND IT FLIPS')
    Y0, SC = 210, 70
    for g, (drop, ws) in enumerate(DROP):
        gx = 120 + g * 240
        t0 = .4 + g * 2.2
        for i in range(6):
            x = gx - 75 + i * 26
            out = i + 1 == drop
            f.static(R(x, 40, 22, 22, BG, RULE_HI, 3) + T(x + 11, 55, str(i + 1), TX, mono=True))
            if out:
                f.show(R(x, 40, 22, 22, SUNK, GH, 3) + T(x + 11, 55, str(i + 1), GH, mono=True) +
                       L(x + 2, 60, x + 20, 42, RO, 1.4), t0)
        f.show(S(gx, 82, 'without row %d' % drop, MU, 'middle'), t0)
        f.static(L(gx - 60, Y0, gx + 60, Y0, RULE_HI, 1) + M(gx - 30, Y0 + 22, '{x}₁', MU) + M(gx + 30, Y0 + 22, '{x}₂', MU))
        flip = ws[0] == 0
        for k, v in enumerate(ws):
            x = gx - 30 + k * 60
            if v == 0:
                f.show(L(x - 16, Y0, x + 16, Y0, VI, 3) + T(x, Y0 - 8, '0', VI, mono=True, bold=True), t0 + .6)
            else:
                c = RO if flip else BR
                f.show(vbar(x, Y0, v, SC, c, 34) + T(x, Y0 - v * SC - 8, '%.2f' % v, c, mono=True, bold=True), t0 + .6)
        if flip:
            f.show(S(gx, Y0 + 50, 'the other twin wins', RO, 'middle', True), t0 + 1.2)
    f.show(S(0, 290, 'x₁ and x₂ carry the same signal, so lasso\'s choice says nothing about which one matters', VI, bold=True), 7.4)
    return finish(f, 304)

# ---------- 5.2 too much lambda ----------
def fig_under():
    def sse(w): return sum((b - w * a) ** 2 for a, b in zip(X1, Y))
    lams = [(0, BR), (10, VI), (100, RO)]
    vals = [round(sse(w1d(l)), 2) for l, _ in lams]
    f = Anim('rl9-', 720, 0, 'The six points with the one-feature ridge line for lambda 0, 10 and 100. The line flattens toward '
             'y = 0 and the training error grows from %.2f to %.2f to %.2f: the penalty now beats the data.' % tuple(vals),
             'λ TOO LARGE · THE LINE FLATTENS TO ZERO')
    P = Plane(200, 150, 72, 30)
    f.static(L(P.X(-1.8), P.Y(0), P.X(1.8), P.Y(0), RULE_HI, 1.2) + L(P.X(0), P.Y(-2.6), P.X(0), P.Y(2.6), RULE_HI, 1.2) +
             M(P.X(1.8) + 8, P.Y(0) + 5, '{x}', MU, 'start') + M(P.X(0) + 8, P.Y(2.6) + 4, '{y}', MU, 'start'))
    f.show(''.join(dot(*P(a, b), BR, 4) for a, b in zip(X1, Y)), .3)
    for k, (lam, c) in enumerate(lams):
        w = w1d(lam)
        t0 = 1.0 + k * 1.6
        f.show(poly([P(-1.7, -1.7 * w), P(1.7, 1.7 * w)], c, 2.4), t0, hide=None if k == 2 else t0 + 1.5)
        y = 70 + k * 46
        f.show(M(450, y, '{λ} = %d' % lam, c, 'start') + M(530, y, '{w} = %.2f' % w, TX, 'start') +
               T(700, y, 'error %.2f' % vals[k], c, 'end', mono=True, bold=k == 2), t0)
    f.show(S(450, 250, 'all weights near 0 → predicts the mean', RO, bold=True), 6.0)
    assert vals[0] < vals[1] < vals[2]
    return finish(f, 280)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Classical models</p>
  <h1>Ridge, Lasso &amp; <em>Elastic Net</em></h1>
  <p class="lede">Keep the linear model, add one term to the loss that charges for large weights. The shape of that term decides whether weights shrink or vanish.</p>
</header>

<section id="rlen-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">With correlated or noisy features, the error-only fit hides the data in <em>huge weights that cancel each other</em>. A penalty on weight size pulls them back.</p>
{F1}
  <ul class="why">
    <li>Running example: 6 standardized rows; <span class="mth"><var>x</var><sub>1</sub></span> and <span class="mth"><var>x</var><sub>2</sub></span> are the same income in two units, <span class="mth"><var>x</var><sub>3</sub></span>, <span class="mth"><var>x</var><sub>4</sub></span> are noise.</li>
    <li>Huge cancelling weights flip wildly when a few rows change: that is high variance (<a href="../../04-core-concepts/bias-variance-tradeoff/index.html">Bias–variance tradeoff</a>).</li>
    <li>The same idea is weight decay in neural networks and <span class="mth"><var>λ</var></span> on leaf values in <a href="../../06-tree-models/xgboost/index.html">XGBoost</a>.</li>
  </ul>
</section>

<section id="rlen-s2" class="lesson">
  <div class="sh"><b>02</b><h2>General formula</h2></div>
  <p class="key">The loss is the old error plus <em>λ times a penalty on the weights</em>. Only the penalty changes between the three methods.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>J</var>(<var>w</var>)</span><em>what training minimizes</em></span>
      <span class="op">=</span>
      <span class="t"><span><span class="op">Σ</span> (<var>y</var><sub><var>i</var></sub> − <var>ŷ</var><sub><var>i</var></sub>)<sup>2</sup></span><em>squared error, as in linear regression</em></span>
      <span class="op">+</span>
      <span class="t p"><span><var>λ</var></span><em>penalty strength ≥ 0</em></span>
      <span class="op">·</span>
      <span class="t b"><span><var>P</var>(<var>w</var>)</span><em>penalty on weight size</em></span>
    </div>
    <div class="line">
      <span class="t b"><span><var>P</var><sub>Ridge</sub> = <span class="op">Σ</span> <var>w</var><span class="ss"><sup>2</sup><sub><var>j</var></sub></span></span><em>L2: shrinks all</em></span>
      <span class="op">·</span>
      <span class="t b"><span><var>P</var><sub>Lasso</sub> = <span class="op">Σ</span> |<var>w</var><sub><var>j</var></sub>|</span><em>L1: zeros some</em></span>
      <span class="op">·</span>
      <span class="t b"><span><var>P</var><sub>EN</sub> = <var>ρ</var> <span class="op">Σ</span> |<var>w</var><sub><var>j</var></sub>| + <span class="frac"><i>1 − <var>ρ</var></i><i>2</i></span> <span class="op">Σ</span> <var>w</var><span class="ss"><sup>2</sup><sub><var>j</var></sub></span></span><em>a mix of both</em></span>
    </div>
  </div>
  <p class="skey">With one feature, ridge has a closed form you can do by hand: <em>λ is simply added to the denominator</em>.</p>
{F2}
  <ul class="why">
    <li>λ = 0 gives back plain <a href="../linear-regression/index.html">linear regression</a>; λ → ∞ drives every weight to 0.</li>
    <li>The intercept is not penalized: it only shifts the line, it adds no complexity.</li>
    <li>In scikit-learn λ is called <code>alpha</code>; in <code>LogisticRegression</code> it is <code>C = 1/λ</code>, so larger C means a weaker penalty.</li>
  </ul>
</section>

<section id="rlen-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Three penalties</h2></div>
  <p class="key">Picture the penalty as a region the weights must stay inside; the answer is where <em>the smallest error contour first touches it</em>.</p>
  <div class="subsec" id="rlen-s3-1">
    <h3 class="ssh"><b>3.1</b>Ridge · L2</h3>
    <p class="skey">The region is a circle: smooth everywhere, so the touching point is almost never on an axis — <em>every weight shrinks, none becomes 0</em>.</p>
{F3}
    <ul class="why">
      <li>Correlated features share the weight evenly (0.71 and 0.70 in section 01).</li>
      <li>Has a closed form, so it is fast; trade-off: it never drops a feature.</li>
    </ul>
  </div>
  <div class="subsec" id="rlen-s3-2">
    <h3 class="ssh"><b>3.2</b>Lasso · L1</h3>
    <p class="skey">The region is a diamond with <em>corners on the axes</em>; the contour usually touches a corner, where one weight is exactly 0.</p>
{F4}
    <ul class="why">
      <li>A weight of exactly 0 means the feature is not used: selection happens during training (a <em>sparse</em> model).</li>
      <li>No closed form: solved iteratively (coordinate descent). Trade-off: at most <span class="mth"><var>n</var></span> features kept when features outnumber rows.</li>
    </ul>
  </div>
  <div class="subsec" id="rlen-s3-3">
    <h3 class="ssh"><b>3.3</b>Elastic Net</h3>
    <p class="skey">A mix set by <span class="mth"><var>ρ</var></span> (<code>l1_ratio</code>): the L1 part zeros useless features, the L2 part <em>keeps correlated twins together</em>.</p>
{F5}
    <ul class="why">
      <li><span class="mth"><var>ρ</var> = 0</span> is ridge, <span class="mth"><var>ρ</var> = 1</span> is lasso.</li>
      <li>Use it when features come in correlated groups or outnumber rows; trade-off: two knobs to tune instead of one.</li>
    </ul>
  </div>
</section>

<section id="rlen-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Knobs</h2></div>
  <p class="key">Two settings decide whether the penalty helps: <em>how strong it is</em>, and <em>what units the features are in</em>.</p>
  <div class="subsec" id="rlen-s4-1">
    <h3 class="ssh"><b>4.1</b>Penalty strength λ</h3>
    <p class="skey">Small λ already tames the weights while the error barely moves; large λ <em>flattens everything</em>.</p>
{F6}
    <ul class="why">
      <li>Sweep λ on a log scale (0.001, 0.01 … 100); a linear sweep skips the useful small values.</li>
      <li>Pick λ by cross-validation (<code>RidgeCV</code>, <code>LassoCV</code>), never on the test set — see <a href="../../04-core-concepts/train-val-test-cv/index.html">Train/val/test &amp; CV</a>.</li>
    </ul>
  </div>
  <div class="subsec" id="rlen-s4-2">
    <h3 class="ssh"><b>4.2</b>Standardize first</h3>
    <p class="skey">The penalty charges the raw weight, so a feature in small units needs a big weight and <em>gets crushed for its unit alone</em>.</p>
{F7}
    <ul class="why">
      <li>Scale every feature to mean 0, std 1 before fitting (<code>StandardScaler</code> in a pipeline).</li>
      <li>Fit the scaler on the training split only, then apply it to validation and test.</li>
    </ul>
  </div>
</section>

<section id="rlen-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Where it breaks</h2></div>
  <p class="key">The penalty buys stable predictions; it does not buy <em>trustworthy feature choices</em> or a free lunch at any λ.</p>
  <div class="subsec" id="rlen-s5-1">
    <h3 class="ssh"><b>5.1</b>Lasso flips between twins</h3>
    <p class="skey">With two correlated features lasso keeps one <em>arbitrarily</em>; a small change in the data swaps which.</p>
{F8}
    <ul class="why">
      <li>Do not read lasso's kept list as "the important features".</li>
      <li>Fix: Elastic Net keeps the group together, or check stability across bootstrap refits.</li>
    </ul>
  </div>
  <div class="subsec" id="rlen-s5-2">
    <h3 class="ssh"><b>5.2</b>Too much penalty underfits</h3>
    <p class="skey">Past the sweet spot, λ outweighs the data and the model <em>drifts toward predicting the mean</em>.</p>
{F9}
    <ul class="why">
      <li>Rising validation error at large λ is bias, not variance (<a href="../../04-core-concepts/overfitting-regularization/index.html">Overfitting &amp; regularization</a>).</li>
      <li>A penalty cannot fix a model that is too simple: a curve still needs curved features.</li>
    </ul>
  </div>
</section>

'''

def build():
    figs = dict(F1=fig_mental(), F2=fig_worked(), F3=fig_geom('rl3-', 'l2'), F4=fig_geom('rl4-', 'l1'), F5=fig_enet(),
                F6=fig_path(), F7=fig_scale(), F8=fig_flip(), F9=fig_under())
    return re.sub(r'\{(F\d)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'Add a penalty on weight size to linear regression: L2 shrinks every weight, L1 sets some to exactly 0, Elastic Net mixes both.')
    print('ok')
