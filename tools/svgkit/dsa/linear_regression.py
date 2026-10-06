# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/05-classical-ml/linear-regression (visual-first).
Run: python3 linear_regression.py  -> rewrites the lesson body between <header class="hero"> and the replay script."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from linear_algebra import Anim, T, R, L, MU, TX, FA, BR, VI, FI, RO, GH, RULE, RULE_HI, BG, SUNK, tn, M, S, chip, dot, poly, finish, splice
from tablefig import Table, arrow
from calculus_chain import frac
from mlplot import solve
PAGE = os.path.join(HERE, '../../../content/07-machine-learning/05-classical-ml/linear-regression/index.html')

ID = 'ABCDEF'
X = [12, 22, 18, 26, 30, 34]
Y = [-4, -1, 1, 1, 7, 1]
N = 6

def ols(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys)); sxx = sum((x - mx) ** 2 for x in xs)
    return sxy / sxx, my - sxy / sxx * mx

W, B = ols(X, Y)
MX, MY = sum(X) / N, sum(Y) / N
assert round(W, 3) == .308 and round(B, 2) == -6.46
MSE = sum((W * x + B - y) ** 2 for x, y in zip(X, Y)) / N
assert round(MSE, 2) == 5.69

def gd(eta, steps=6):
    sd = math.sqrt(sum((x - MX) ** 2 for x in X) / N); Z = [(x - MX) / sd for x in X]
    a = c = 0.; h = []
    for k in range(steps + 1):
        p = [a * z + c for z in Z]
        h.append((a / sd, c - a * MX / sd, sum((q - y) ** 2 for q, y in zip(p, Y)) / N))
        ga = 2 / N * sum((q - y) * z for q, y, z in zip(p, Y, Z)); gc = 2 / N * sum(q - y for q, y in zip(p, Y))
        a -= eta * ga; c -= eta * gc
    return h

class Plot:
    def __init__(s, px, py, pw, ph, x0, x1, y0, y1):
        s.px, s.py, s.pw, s.ph, s.x0, s.x1, s.y0, s.y1 = px, py, pw, ph, x0, x1, y0, y1
    def X(s, x): return s.px + (x - s.x0) / (s.x1 - s.x0) * s.pw
    def Y(s, y): return s.py + s.ph - (y - s.y0) / (s.y1 - s.y0) * s.ph
    def __call__(s, x, y): return (s.X(x), s.Y(y))
    def axes(s, xt=(), yt=(), xl='', yl='', zero=True):
        o = L(s.px, s.py + s.ph, s.px + s.pw, s.py + s.ph, MU, 1.1) + L(s.px, s.py + s.ph, s.px, s.py - 4, MU, 1.1)
        for v in xt:
            o += L(s.X(v), s.py + s.ph, s.X(v), s.py + s.ph + 4, MU, 1) + T(s.X(v), s.py + s.ph + 16, '%g' % v, FA, mono=True)
        for v in yt:
            o += T(s.px - 7, s.Y(v) + 4, ('%+g' % v if v else '0').replace('-', '−'), FA, 'end', mono=True)
            o += L(s.px, s.Y(v), s.px + s.pw, s.Y(v), RULE, 1, '2 4')
        if zero and s.y0 < 0 < s.y1: o += L(s.px, s.Y(0), s.px + s.pw, s.Y(0), RULE_HI, 1.1)
        if xl: o += M(s.px + s.pw + 8, s.py + s.ph + 5, xl, MU, 'start')
        if yl: o += M(s.px, s.py - 12, yl, MU)
        return o
    def line(s, w, b, c=BR, sw=2.4, dash=None, xa=None, xb=None):
        xa = s.x0 if xa is None else xa; xb = s.x1 if xb is None else xb
        return poly([s(xa, w * xa + b), s(xb, w * xb + b)], c, sw, dash)

def sgn(v, d=2):
    return ('%+.*f' % (d, v)).replace('-', '−')

# ---------- 1 Mental model ----------
def fig_mental():
    f = Anim('lr1-', 720, 0, 'Six customers A to F in a table, income x and extra spending y. Each row becomes a dot on the plane. '
             'A straight line is drawn through the cloud, then a vertical gap from each dot to the line shows its error. '
             'The best line has w = 0.31 and b = −6.46.', 'EACH ROW A DOT · ONE LINE THROUGH THEM')
    t = Table(0, 40, [('id', 40), ('x', 60, 'income'), ('y', 60, 'spending')])
    f.static(t.head())
    P = Plot(250, 44, 400, 220, 10, 36, -6, 8)
    f.static(P.axes(xt=(10, 20, 30), yt=(-4, 0, 4, 8), xl='{x}', yl='{y}'))
    for i in range(N):
        t0 = .3 + i * .45
        f.static(t.row(i, [ID[i], str(X[i]), sgn(Y[i], 0)]))
        f.show(t.outline(i, c=VI), t0, hide=t0 + .45)
        f.show(dot(*P(X[i], Y[i]), BR, 5) + T(P.X(X[i]) + 9, P.Y(Y[i]) - 6, ID[i], BR, 'start', bold=True), t0 + .2)
    t1 = .3 + N * .45 + .3
    f.show(P.line(W, B, FI, 2.6), t1)
    f.show(M(P.X(35), P.Y(W * 35 + B) - 14, '{ŷ} = {w}{x} + {b}', FI, 'end'), t1 + .3)
    for i in range(N):
        px, py = P(X[i], Y[i]); ly = P.Y(W * X[i] + B)
        f.show(L(px, py, px, ly, VI, 1.8, '4 3'), t1 + 1 + i * .25)
    f.show(S(P.px + 8, P.py + P.ph + 40, 'dashed gap = error of one row', VI), t1 + 1.2)
    f.show(R(10, t.bottom(N) + 20, 170, 28, tn(FI, '.14'), FI, 14, 1.3) + M(95, t.bottom(N) + 39, '{w} = 0.31    {b} = −6.46', FI), t1 + 3)
    return finish(f, 312)

# ---------- 2 General formula: squared errors ----------
def fig_loss():
    f = Anim('lr2-', 720, 0, 'For the fitted line, each row gets its error ŷ minus y, then the error is squared and drawn as a '
             'square on the plot. The six squares are summed to 34.11 and divided by 6: MSE = 5.69.', 'MSE = AVERAGE AREA OF THE ERROR SQUARES')
    P = Plot(40, 40, 330, 230, 10, 36, -6, 8)
    f.static(P.axes(xt=(10, 20, 30), yt=(-4, 0, 4, 8), xl='{x}', yl='{y}') + P.line(W, B, FI, 2.2))
    for i in range(N): f.static(dot(*P(X[i], Y[i]), BR, 4.5))
    t = Table(440, 30, [('id', 36), ('ŷ − y', 80, 'error'), ('(ŷ − y)²', 90, 'squared')])
    f.static(t.head())
    k = P.ph / (P.y1 - P.y0)
    tot = 0
    for i in range(N):
        e = W * X[i] + B - Y[i]; tot += e * e
        t0 = .5 + i * .9
        f.static(t.row(i, [ID[i], '', '']))
        f.show(t.outline(i, c=VI), t0, hide=t0 + .9)
        px, py = P(X[i], Y[i]); s = abs(e) * k
        f.show(R(px, min(py, py - e * k), s, s, tn(VI, '.16'), VI, 1, 1.2), t0 + .1)
        f.show(T(t.cx(1), t.ry(i) + 17, sgn(e), VI, mono=True), t0 + .2)
        f.show(T(t.cx(2), t.ry(i) + 17, '%.2f' % (e * e), TX, mono=True), t0 + .5)
    assert round(tot, 2) == 34.11
    yb = t.bottom(N) + 26
    te = .5 + N * .9
    f.show(M(t.x, yb, 'Σ = %.2f' % tot, TX, 'start'), te)
    f.show(M(t.x, yb + 34, 'MSE =', TX, 'start') + frac(t.x + 88, yb + 30, '34.11', '6', TX, 46) + M(t.x + 120, yb + 34, '=', TX, 'start'), te + .6)
    f.show(R(t.x + 136, yb + 14, 52, 28, FI, FI, 6) + M(t.x + 162, yb + 34, '5.69', 'var(--on-fill)'), te + 1.2)
    return finish(f, 360)

# ---------- 3.1 Closed form ----------
def fig_closed():
    f = Anim('lr3-', 720, 0, 'The closed form on the six rows. First the means x̄ = 23.67 and ȳ = 0.83. Each row gets x − x̄, y − ȳ, '
             'their product and (x − x̄) squared. The two column sums 99.67 and 323.33 give w = 0.308, then b = ȳ − w x̄ = −6.46.',
             'CLOSED FORM · TWO SUMS, ONE DIVISION')
    t = Table(4, 40, [('id', 34), ('x', 44), ('y', 44), ('x − x̄', 70), ('y − ȳ', 70), ('product', 76), ('(x − x̄)²', 82)])
    f.static(t.head())
    f.show(M(560, 64, '{x̄} = 23.67', BR, 'start') + M(560, 88, '{ȳ} = 0.83', BR, 'start'), .3)
    for i in range(N):
        dx, dy = X[i] - MX, Y[i] - MY
        t0 = 1.0 + i * .7
        f.static(t.row(i, [ID[i], str(X[i]), sgn(Y[i], 0), '', '', '', '']))
        f.show(t.outline(i, c=VI), t0, hide=t0 + .7)
        f.show(T(t.cx(3), t.ry(i) + 17, sgn(dx), TX, mono=True) + T(t.cx(4), t.ry(i) + 17, sgn(dy), TX, mono=True), t0 + .15)
        f.show(T(t.cx(5), t.ry(i) + 17, sgn(dx * dy), VI, mono=True) + T(t.cx(6), t.ry(i) + 17, '%.2f' % (dx * dx), BR, mono=True), t0 + .35)
    te = 1.0 + N * .7
    yb = t.bottom(N)
    f.show(L(t.colx(5), yb + 6, t.colx(6) + 82, yb + 6, MU, 1) + M(t.cx(5), yb + 24, '99.67', VI) + M(t.cx(6), yb + 24, '323.33', BR) +
           M(t.colx(5) - 10, yb + 24, 'Σ', MU, 'end'), te)
    y2 = yb + 76
    f.show(M(0, y2 + 5, '{w} =', TX, 'start') + frac(80, y2, 'Σ({x}−{x̄})({y}−{ȳ})', 'Σ({x}−{x̄})²', TX, 130) + M(150, y2 + 5, '=', TX, 'start') +
           frac(196, y2, '99.67', '323.33', TX, 56), te + .6)
    f.show(M(234, y2 + 5, '=', TX, 'start') + R(250, y2 - 14, 60, 28, FI, FI, 6) + M(280, y2 + 6, '0.308', 'var(--on-fill)'), te + 1.4)
    f.show(M(360, y2 + 5, '{b} = {ȳ} − {w}{x̄} = 0.83 − 0.308 · 23.67 =', TX, 'start'), te + 2.2)
    f.show(R(640, y2 - 14, 62, 28, FI, FI, 6) + M(671, y2 + 6, '−6.46', 'var(--on-fill)'), te + 2.8)
    return finish(f, y2 + 40)

# ---------- 3.2 Gradient descent ----------
def fig_gd():
    h = gd(.3)
    assert round(h[-1][0], 3) == .307 and round(h[0][2], 1) == 11.5
    f = Anim('lr4-', 720, 0, 'Gradient descent from w = 0, b = 0. Each step the table gets a new row with w, b and the loss, and '
             'the line on the plot turns toward the dots. The loss falls 11.50, 6.62, 5.83 … 5.69 and w settles at 0.307, the '
             'same answer as the closed form.', 'GRADIENT DESCENT · EACH STEP TURNS THE LINE A LITTLE')
    t = Table(0, 40, [('step', 46), ('w', 66), ('b', 66), ('MSE', 66)])
    f.static(t.head())
    P = Plot(310, 44, 360, 230, 10, 36, -6, 8)
    f.static(P.axes(xt=(10, 20, 30), yt=(-4, 0, 4, 8), xl='{x}', yl='{y}'))
    for i in range(N): f.static(dot(*P(X[i], Y[i]), BR, 4.5))
    for k, (w, b, l) in enumerate(h):
        t0 = .4 + k * 1.0
        last = k == len(h) - 1
        f.show(t.row(k, [str(k), '%.3f' % w, sgn(b), '%.2f' % l], colors={3: FI if last else TX}), t0)
        f.show(t.outline(k, c=VI), t0, hide=None if last else t0 + 1.0)
        f.show(P.line(w, b, FI if last else VI, 2.4), t0 + .1, hide=None if last else t0 + 1.0)
        if not last: f.show(P.line(w, b, GH, 1.2, '3 4'), t0 + 1.0)
    f.show(S(P.px, P.py + P.ph + 40, 'grey dashes = earlier steps', MU), .4 + len(h) * 1.0)
    return finish(f, 330)

# ---------- 4.1 MSE vs MAE ----------
def fig_mae():
    Y2 = Y[:]; Y2[4] = 20
    w2, b2 = ols(X, Y2)
    assert round(w2, 3) == .563
    wm, bm = 0.35714285714285715, -8.285714285714285   # least absolute deviation, same before and after (passes through 2 points)
    for ys in (Y, Y2):
        best = min(sum(abs(wm * x + bm - y) for x, y in zip(X, ys)) - sum(abs(((ys[j] - ys[i]) / (X[j] - X[i])) * (x - X[i]) + ys[i] - y)
                   for x, y in zip(X, ys)) for i in range(N) for j in range(i + 1, N))
        assert best <= 1e-9
    f = Anim('lr5-', 720, 0, 'Six dots with the MSE line (w = 0.31) and the MAE line (w = 0.36). Customer E\'s y moves from 7 up to 20. '
             'The MSE line swings up to w = 0.56; the MAE line does not move.', 'ONE DOT MOVES · MSE LINE SWINGS, MAE LINE STAYS')
    P = Plot(40, 40, 420, 270, 10, 36, -6, 21)
    f.static(P.axes(xt=(10, 20, 30), yt=(0, 10, 20), xl='{x}', yl='{y}'))
    for i in range(N):
        if i != 4: f.static(dot(*P(X[i], Y[i]), BR, 4.5))
    ex, ey = P(X[4], Y[4]); _, ey2 = P(X[4], 20)
    f.path(dot(ex, ey2, RO, 5.5) + T(ex + 10, ey2 - 6, 'E', RO, 'start', bold=True), [(0, 0, ey - ey2), (2.4, 0, 0)], 0, appear=False, d=1.0)
    f.show(P.line(W, B, VI, 2.4), .4, hide=3.4)
    f.show(P.line(w2, b2, VI, 2.4), 3.4)
    f.show(P.line(W, B, GH, 1.2, '3 4'), 3.4)
    f.show(P.line(wm, bm, FI, 2.4), 1.0)
    lx = 490
    f.show(L(lx, 70, lx + 24, 70, VI, 2.4) + M(lx + 32, 75, 'MSE', VI, 'start'), .4)
    f.show(M(lx + 80, 75, '{w} = 0.31', MU, 'start'), .4, hide=3.4)
    f.show(M(lx + 80, 75, '{w} = 0.56', VI, 'start'), 3.6)
    f.show(L(lx, 110, lx + 24, 110, FI, 2.4) + M(lx + 32, 115, 'MAE', FI, 'start') + M(lx + 80, 115, '{w} = 0.36', FI, 'start'), 1.0)
    f.show(S(lx, 160, 'E: y = 7 → 20', RO), 2.2)
    f.show(S(lx, 200, 'MSE pays e², so one far dot', MU) + S(lx, 218, 'pulls the whole line', MU), 4.0)
    f.show(S(lx, 248, 'MAE pays |e|: the line', MU) + S(lx, 266, 'follows the middle dots', MU), 4.6)
    return finish(f, 352)

# ---------- 4.2 Learning rate ----------
def fig_eta():
    a, b = gd(.3), gd(1.05)
    assert round(a[-1][2], 2) == 5.69 and round(b[-1][2], 2) == 23.93
    f = Anim('lr6-', 720, 0, 'Loss after each gradient-descent step for two learning rates. With η = 0.3 the loss falls from 11.5 '
             'to 5.7 and rests. With η = 1.05 each step overshoots, and the loss climbs to 23.9.', 'SAME DATA, ONLY η CHANGES')
    for k, (h, eta, c, word) in enumerate(((a, '0.3', FI, 'falls, then rests'), (b, '1.05', RO, 'overshoots, climbs'))):
        P = Plot(50 + k * 350, 50, 280, 200, 0, 6, 0, 25)
        f.static(P.axes(xt=range(7), yt=(0, 10, 20), xl='step', yl='MSE') + M(P.px + P.pw / 2, 30, 'η = %s' % eta, c))
        pts = [P(i, l) for i, (_, _, l) in enumerate(h)]
        t0 = .4 + k * 3.2
        for i, p in enumerate(pts):
            if i: f.show(poly(pts[i - 1:i + 1], c, 2.4), t0 + i * .4, d=.2)
            f.show(dot(*p, c, 4), t0 + i * .4)
        f.show(T(pts[-1][0], pts[-1][1] - 12, '%.1f' % h[-1][2], c, mono=True, bold=True), t0 + 2.6)
        f.show(S(P.px + P.pw / 2, P.py + P.ph + 46, word, c, 'middle', True), t0 + 2.8)
    return finish(f, 312)

# ---------- 4.3 Feature scaling ----------
def fig_scale():
    f = Anim('lr7-', 720, 0, 'Loss contours seen from above. Left, unscaled features: the valley is a long thin ellipse and gradient '
             'descent zigzags across it, still far from the centre after 12 steps. Right, scaled features: the contours are '
             'circles and the path goes straight to the centre in a few steps.', 'LOSS SEEN FROM ABOVE · UNSCALED VS SCALED')
    def run(a, c, eta, p, n):
        out = [p]
        for _ in range(n):
            p = (p[0] - eta * a * p[0], p[1] - eta * c * p[1]); out.append(p)
        return out
    cases = [(170, 'unscaled', 1, 25, .075, (-3.6, 1.4), RO), (530, 'scaled', 1, 1, .45, (-2.6, 2.6), FI)]
    for cx, word, a, c, eta, p0, col in cases:
        cy, s = 170, 40
        f.static(M(cx, 40, word, col))
        for lev in (1, 3, 6, 10):
            rx, ry = math.sqrt(2 * lev / a) * s, math.sqrt(2 * lev / c) * s
            if rx > 165: continue
            f.static('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="1"/>' % (cx, cy, rx, ry, RULE_HI))
        f.static(dot(cx, cy, BR, 4) + T(cx + 8, cy + 16, 'min', BR, 'start'))
        pts = [(cx + x * s, cy - y * s) for x, y in run(a, c, eta, p0, 12)]
        t0 = .4 if word == 'unscaled' else 4.4
        f.show(dot(*pts[0], VI, 5), t0)
        for i in range(1, len(pts)):
            f.show(arrow(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1], col, 1.6, None, 6) if math.dist(pts[i - 1], pts[i]) > 8
                   else poly(pts[i - 1:i + 1], col, 1.6), t0 + i * .28, d=.15)
        f.show(S(cx, 290, '12 steps, still zigzagging' if word == 'unscaled' else 'straight to the centre', col, 'middle', True), t0 + 3.5)
    f.show(S(170, 312, 'one η too big for one axis, too small for the other', MU, 'middle'), 4.2)
    return finish(f, 326)

# ---------- 5.1 Curved relationship ----------
def curve_data():
    xs = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ys = [round(.25 * (x - 5) ** 2 + .4 * x, 2) for x in xs]
    return xs, ys

def fig_curve():
    xs, ys = curve_data(); w, b = ols(xs, ys)
    res = [y - (w * x + b) for x, y in zip(xs, ys)]
    assert res[0] > 0 and res[4] < 0 and res[-1] > 0
    f = Anim('lr8-', 720, 0, 'Left: dots that bend like a U, with the best straight line through them. Right: the residuals y minus ŷ '
             'plotted against ŷ. They form a U: positive at both ends, negative in the middle. A straight line cannot follow a bend.',
             'A BEND THE LINE CANNOT FOLLOW')
    P = Plot(40, 40, 280, 220, 0, 10, 0, 8)
    f.static(P.axes(xt=(0, 5, 10), yt=(0, 4, 8), xl='{x}', yl='{y}', zero=False))
    for i, (x, y) in enumerate(zip(xs, ys)): f.show(dot(*P(x, y), BR, 4.5), .2 + i * .1)
    f.show(P.line(w, b, FI, 2.4), 1.3)
    Q = Plot(420, 40, 260, 220, 0, 6, -2, 2.5)
    f.static(Q.axes(xt=(0, 3, 6), yt=(-2, 0, 2), xl='{ŷ}', yl='{y} − {ŷ}'))
    pts = []
    for i, (x, r) in enumerate(zip(xs, res)):
        p = Q(w * x + b, r); pts.append(p)
        f.show(dot(*p, VI, 4.5), 2.2 + i * .3)
    f.show(poly(pts, VI, 1.4, '4 3'), 2.2 + len(xs) * .3 + .2)
    f.show(S(Q.px + Q.pw / 2, 300, 'U-shaped residuals = missing curve', VI, 'middle', True), 5.4)
    f.show(S(P.px + P.pw / 2, 300, 'fix: add x² as a feature', MU, 'middle'), 6.0)
    return finish(f, 330)

# ---------- 5.2 Uneven spread ----------
def fig_funnel():
    xs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sign = [1, -1, -1, 1, 1, -1, 1, -1, -1, 1]
    ys = [x + .28 * x * s for x, s in zip(xs, sign)]
    w, b = ols(xs, ys)
    res = [y - (w * x + b) for x, y in zip(xs, ys)]
    assert max(abs(r) for r in res[-3:]) > 3 * max(abs(r) for r in res[:3])
    f = Anim('lr9-', 720, 0, 'Left: dots whose scatter grows with x, and the fitted line. Right: residuals against ŷ open like a '
             'funnel, small at the left and large at the right. The line is still fine, but its error bars are wrong.',
             'ERROR THAT GROWS WITH THE PREDICTION')
    P = Plot(40, 40, 280, 220, 0, 11, 0, 14)
    f.static(P.axes(xt=(0, 5, 10), yt=(0, 7, 14), xl='{x}', yl='{y}', zero=False))
    for i, (x, y) in enumerate(zip(xs, ys)): f.show(dot(*P(x, y), BR, 4.5), .2 + i * .1)
    f.show(P.line(w, b, FI, 2.4), 1.4)
    Q = Plot(420, 40, 260, 220, 0, 11, -4, 4)
    f.static(Q.axes(xt=(0, 5, 10), yt=(-4, 0, 4), xl='{ŷ}', yl='{y} − {ŷ}'))
    for i, (x, r) in enumerate(zip(xs, res)):
        f.show(dot(*Q(w * x + b, r), VI, 4.5), 2.2 + i * .25)
    f.show(poly([Q(0.5, .3), Q(10.8, 3.6)], VI, 1.2, '4 3') + poly([Q(0.5, -.3), Q(10.8, -3.6)], VI, 1.2, '4 3'), 5.0)
    f.show(S(Q.px + Q.pw / 2, 300, 'funnel = spread grows with ŷ', VI, 'middle', True), 5.4)
    f.show(S(P.px + P.pw / 2, 300, 'fix: predict log y, or weight rows', MU, 'middle'), 6.0)
    return finish(f, 330)

# ---------- 5.3 Correlated columns ----------
X2 = [11.0, 19.7, 16.3, 23.5, 26.8, 30.3]
def fit2(idx):
    rows = [(1, X[i], X2[i], Y[i]) for i in idx]
    A = [[sum(r[i] * r[j] for r in rows) for j in range(3)] for i in range(3)]
    return solve(A, [sum(r[i] * r[3] for r in rows) for i in range(3)])

def fig_collinear():
    c1, c2 = fit2(range(6)), fit2([0, 2, 3, 4, 5])
    p1 = [c1[0] + c1[1] * a + c1[2] * b for a, b in zip(X, X2)]
    p2 = [c2[0] + c2[1] * a + c2[2] * b for a, b in zip(X, X2)]
    assert c1[1] < 0 < c2[1] and c1[2] > 0 > c2[2]
    shift = max(abs(a - b) for a, b in zip(p1, p2))
    f = Anim('lr10-', 720, 0, 'Two columns x1 and x2 that are almost copies of each other. Fit on all six rows: w1 = −1.23, w2 = +1.75. '
             'Drop row B and refit: w1 = +2.31, w2 = −2.29, both signs flip. The predictions next to each row barely change.',
             'TWO NEAR-COPY COLUMNS · WEIGHTS FLIP, PREDICTIONS STAY')
    t = Table(0, 40, [('id', 36), ('x₁', 56, 'income'), ('x₂', 56, 'other unit'), ('y', 46), ('ŷ all', 70), ('ŷ no B', 70)])
    f.static(t.head())
    for i in range(N): f.static(t.row(i, [ID[i], str(X[i]), '%.1f' % X2[i], sgn(Y[i], 0), '', '']))
    f.show(t.colbox(1, N, VI) if hasattr(t, 'colbox') else '', .3, hide=1.6)
    f.show(t.colbox(2, N, VI) if hasattr(t, 'colbox') else '', .3, hide=1.6)
    f.show(S(t.colx(1), t.bottom(N) + 22, 'x₂ ≈ 0.9 · x₁, correlation 0.9999', VI), .5)
    cx = 450
    f.show(S(cx, 70, 'fit on all 6 rows', MU), 1.8)
    f.show(M(cx, 100, '{w}₁ = %s,   {w}₂ = %s' % (sgn(c1[1]), sgn(c1[2])), BR, 'start'), 2.0)
    for i in range(N): f.show(T(t.cx(4), t.ry(i) + 17, sgn(p1[i], 1), BR, mono=True), 2.3 + i * .08)
    f.show(R(t.x + 1, t.ry(1) + 1, t.colx(4) - t.x - 4, t.rh - 2, SUNK, 'none', 3) + T(t.cx(0), t.ry(1) + 17, 'B', GH) + L(t.x + 6, t.ry(1) + 13, t.colx(4) - 6, t.ry(1) + 13, GH, 1.2), 3.4)
    f.show(S(cx, 150, 'drop row B, refit', MU), 3.6)
    f.show(M(cx, 180, '{w}₁ = %s,   {w}₂ = %s' % (sgn(c2[1]), sgn(c2[2])), RO, 'start'), 4.0)
    for i in range(N): f.show(T(t.cx(5), t.ry(i) + 17, sgn(p2[i], 1), FI, mono=True), 4.4 + i * .08)
    f.show(S(cx, 224, 'both weights flip sign', RO, bold=True), 5.0)
    f.show(S(cx, 246, 'predictions move at most %.1f' % shift, FI, bold=True), 5.4)
    return finish(f, t.bottom(N) + 44)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Classical models</p>
  <h1>Linear <em>regression</em></h1>
  <p class="lede">Draw the straight line that misses a cloud of points by the least. The model learns two numbers, <span class="mth"><var>w</var></span> and <span class="mth"><var>b</var></span>; every choice lives in what "misses by the least" means. Use it to read a relationship, or as the baseline before stronger models.</p>
</header>

<section id="lr-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Each row is a dot; linear regression finds <em>the one line</em> whose vertical gaps to the dots are smallest overall.</p>
{lr1}
  <ul class="why">
    <li>Running example: six customers A–F, <span class="mth"><var>x</var></span> is income, <span class="mth"><var>y</var></span> is extra spending.</li>
    <li>Every result below comes from that one assumption: the relationship is a straight line.</li>
  </ul>
</section>

<section id="lr-s2" class="lesson">
  <div class="sh"><b>02</b><h2>General formula</h2></div>
  <p class="key">The prediction is <em>a weighted sum of the features</em>; the loss is the average squared gap.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>ŷ</var></span><em>prediction</em></span>
      <span class="op">=</span>
      <span class="t b"><span><var>w</var><sub>1</sub><var>x</var><sub>1</sub> + … + <var>w</var><sub><var>d</var></sub><var>x</var><sub><var>d</var></sub></span><em>one weight per feature</em></span>
      <span class="op">+</span>
      <span class="t"><span><var>b</var></span><em>intercept</em></span>
    </div>
    <div class="line">
      <span class="t"><span><b class="fn">MSE</b></span><em>loss</em></span>
      <span class="op">=</span>
      <span class="t p"><span><span class="frac"><i>1</i><i><var>n</var></i></span> <span class="op">Σ</span> (<var>ŷ</var><sub><var>i</var></sub> − <var>y</var><sub><var>i</var></sub>)<sup>2</sup></span><em>average squared error over n rows</em></span>
    </div>
  </div>
{lr2}
  <ul class="why">
    <li>Squaring makes every gap positive and punishes big gaps far more than small ones.</li>
    <li>Learning = finding the <span class="mth"><var>w</var>, <var>b</var></span> with the smallest MSE: section 03.</li>
  </ul>
</section>

<section id="lr-s3" class="lesson">
  <div class="sh"><b>03</b><h2>How it learns</h2></div>
  <p class="key">Two routes to the same line: <em>solve it in one shot</em>, or <em>walk downhill</em> step by step.</p>
  <div class="subsec" id="lr-s3-1">
    <h3 class="ssh"><b>3.1</b>Closed form</h3>
    <p class="skey">Set the gradient to zero and solve: with one feature it is <em>two sums and a division</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t b"><span><var>w</var> = <span class="frac"><i><span class="op">Σ</span>(<var>x</var><sub><var>i</var></sub> − <var>x̄</var>)(<var>y</var><sub><var>i</var></sub> − <var>ȳ</var>)</i><i><span class="op">Σ</span>(<var>x</var><sub><var>i</var></sub> − <var>x̄</var>)<sup>2</sup></i></span></span><em>how x and y move together, over how much x moves</em></span>
      <span class="op">,</span>
      <span class="t"><span><var>b</var> = <var>ȳ</var> − <var>w</var><var>x̄</var></span><em>the line passes through the means</em></span>
    </div>
  </div>
{lr3}
    <ul class="why">
      <li>With many features the same idea is the normal equation <span class="mth"><var>w</var> = (<var>X</var><sup>T</sup><var>X</var>)<sup>−1</sup><var>X</var><sup>T</sup><var>y</var></span>.</li>
      <li>Exact and one-shot, but the matrix inverse gets slow as the number of features grows.</li>
    </ul>
  </div>
  <div class="subsec" id="lr-s3-2">
    <h3 class="ssh"><b>3.2</b>Gradient descent</h3>
    <p class="skey">Start anywhere, then move each weight <em>against its gradient</em> until the loss stops falling.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>w</var><sub><var>j</var></sub></span><em>new weight</em></span>
      <span class="op">←</span>
      <span class="t"><span><var>w</var><sub><var>j</var></sub></span><em>old weight</em></span>
      <span class="op">−</span>
      <span class="t p"><span><var>η</var></span><em>learning rate</em></span>
      <span class="op">·</span>
      <span class="t b"><span><span class="frac"><i>2</i><i><var>n</var></i></span> <span class="op">Σ</span> (<var>ŷ</var><sub><var>i</var></sub> − <var>y</var><sub><var>i</var></sub>) <var>x</var><sub><var>ij</var></sub></span><em>gradient: error times that feature</em></span>
    </div>
  </div>
{lr4}
    <ul class="why">
      <li>After six steps <span class="mth"><var>w</var> = 0.307</span>: the same line as the closed form.</li>
      <li>Scales to millions of rows and features; the same update trains <a href="../logistic-regression/index.html">Logistic regression</a> and neural networks.</li>
    </ul>
  </div>
</section>

<section id="lr-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Key knobs</h2></div>
  <p class="key">Three choices change the result: <em>which loss</em>, <em>how big a step</em>, and <em>whether features share a scale</em>.</p>
  <div class="subsec" id="lr-s4-1">
    <h3 class="ssh"><b>4.1</b>MSE or MAE</h3>
    <p class="skey">MSE squares the gap, so <em>one far dot tilts the whole line</em>; MAE takes the absolute gap and ignores it.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">MAE</b></span><em>loss</em></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i>1</i><i><var>n</var></i></span> <span class="op">Σ</span> |<var>ŷ</var><sub><var>i</var></sub> − <var>y</var><sub><var>i</var></sub>|</span><em>average absolute error</em></span>
    </div>
  </div>
{lr5}
    <ul class="why">
      <li>MSE estimates the mean, MAE the median; MSE has a closed form, MAE needs an iterative solver.</li>
      <li>Huber loss is the middle ground: squared for small gaps, absolute for large ones.</li>
    </ul>
  </div>
  <div class="subsec" id="lr-s4-2">
    <h3 class="ssh"><b>4.2</b>Learning rate</h3>
    <p class="skey">Too large an <span class="mth"><var>η</var></span> <em>overshoots the bottom</em> and the loss climbs instead of falling.</p>
{lr6}
    <ul class="why">
      <li>Too small an <span class="mth"><var>η</var></span> heads the right way but takes forever.</li>
      <li>Try a few values on a log scale (0.001, 0.01, 0.1) and watch the loss curve.</li>
    </ul>
  </div>
  <div class="subsec" id="lr-s4-3">
    <h3 class="ssh"><b>4.3</b>Feature scaling</h3>
    <p class="skey">Features on different scales stretch the loss into <em>a long thin valley</em> that gradient descent zigzags across.</p>
{lr7}
    <ul class="why">
      <li>Standardize every column (mean 0, std 1) before gradient descent; the closed form does not care.</li>
      <li>How to scale: <a href="../../04-core-concepts/feature-engineering/index.html">Feature engineering</a>.</li>
    </ul>
  </div>
</section>

<section id="lr-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Reading coefficients</h2></div>
  <p class="key">A coefficient reads as a sentence — but when two columns say the same thing, <em>they share the weight arbitrarily</em> and the signs flip (multicollinearity).</p>
{lr10}
  <ul class="why">
    <li><span class="mth"><var>w</var> = 0.31</span> means one unit more income goes with 0.31 more spending — it needs the units, "other columns held fixed", and is a relationship in the data, not a cause.</li>
    <li>It breaks reading coefficients, not predicting. Measure it with VIF (above 5–10 is a worry); absurdly large weights flag it and overfitting alike — fix by dropping or merging copies, or with <a href="../ridge-lasso-elasticnet/index.html">Ridge, Lasso &amp; Elastic Net</a>.</li>
  </ul>
</section>

<section id="lr-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Four assumptions</h2></div>
  <p class="key">Linearity, independence, even spread and normal residuals are needed for <em>p-values and confidence intervals</em>; for prediction checked on a test set they matter much less. Plot residuals against ŷ to see the first ones.</p>
  <div class="subsec" id="lr-s6-1">
    <h3 class="ssh"><b>6.1</b>Linearity</h3>
    <p class="skey">If the truth bends, the residuals <em>bend too</em>: a U instead of a flat band.</p>
{lr8}
    <ul class="why">
      <li>The model underfits no matter how much data you add; add curved features such as <span class="mth"><var>x</var><sup>2</sup></span> or use a tree model.</li>
    </ul>
  </div>
  <div class="subsec" id="lr-s6-2">
    <h3 class="ssh"><b>6.2</b>Even spread</h3>
    <p class="skey">When errors grow with the prediction, <em>the residuals fan out</em> like a funnel (heteroscedasticity).</p>
{lr9}
    <ul class="why">
      <li>Predictions stay usable; confidence intervals and p-values do not.</li>
      <li>The other two cannot be seen in this plot: independent rows (check how the data was collected) and normal residuals (Q-Q plot).</li>
    </ul>
  </div>
</section>

'''

def build():
    figs = dict(lr1=fig_mental(), lr2=fig_loss(), lr3=fig_closed(), lr4=fig_gd(), lr5=fig_mae(), lr6=fig_eta(),
                lr7=fig_scale(), lr8=fig_curve(), lr9=fig_funnel(), lr10=fig_collinear())
    return re.sub(r'\{(lr\d+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'Fit the straight line with the smallest squared error — closed form or gradient descent, the knobs that change it, reading coefficients, and the four assumptions.')
    print('ok')
