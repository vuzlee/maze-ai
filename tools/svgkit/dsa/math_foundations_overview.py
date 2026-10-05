# -*- coding: utf-8 -*-
"""Figures for content/07-machine-learning/02-math-foundations/math-foundations-overview.
Run: python3 math_foundations_overview.py -> /tmp/ml/math-foundations-overview-figs.json (spliced by a small build script)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mlplot import *  # noqa

rnd = random.Random(3)
XS = [1, 2, 3, 4, 5, 6, 7, 8]
YS = [1.2 + .6 * x + rnd.gauss(0, .45) for x in XS]
def mse(w, b): return sum((w * x + b - y) ** 2 for x, y in zip(XS, YS)) / len(XS)
B0 = sum(YS) / len(YS) - .6 * sum(XS) / len(XS)   # hold b at a sensible value, vary w only
def L1(w): return mse(w, B0)
def dL(w): return sum(2 * (w * x + B0 - y) * x for x, y in zip(XS, YS)) / len(XS)

# ---------- 1. the chain ----------
def fig_chain():
    f = Anim('mf1-', 720, 318, 'Data points appear; a bell curve sits on each point around a candidate line (probability); the squared gaps add up into one loss number; '
             'the loss curve over the slope appears and a ball rolls down it to the minimum (calculus); the line settles at the best slope.',
             'TWO JOBS · WRITE DOWN THE LOSS, THEN FIND ITS MINIMUM')
    pl = Plot(40, 40, 280, 200, 0, 9, 0, 7)
    f.static(pl.axes('x', 'y', [(v, str(v)) for v in (2, 4, 6, 8)], [(v, str(v)) for v in (2, 4, 6)]))
    for i, (x, y) in enumerate(zip(XS, YS)):
        f.show(dot(*pl.P(x, y)), .2 + i * .06, d=.2)
    # candidate line w = 0.2, gaussian bells around it (probability)
    w0 = .2
    t = 1.0
    f.show(L(*pl.P(0, B0), *pl.P(9, w0 * 9 + B0), AM, 2, '5 4'), t, hide=5.4)
    bells = ''
    for x, y in zip(XS, YS):
        mu = w0 * x + B0
        pts = [(pl.X(x) + 18 * math.exp(-((v) ** 2) / (2 * .5 ** 2)), pl.Y(mu + v)) for v in [i / 20 - 1.5 for i in range(61)]]
        bells += poly(pts, AM, 1.2) + L(*pl.P(x, y), *pl.P(x, mu), RD, 1.2, '3 2')
    f.show(bells, t + .6, hide=5.4)
    f.show(T(180, 304, 'probability: each point is the line plus noise', AM), t + .8, hide=5.4)
    # loss curve
    lp = Plot(420, 40, 270, 200, -.1, 1.3, 0, max(L1(-.1), L1(1.3)) * 1.05)
    f.show(lp.axes('slope w', 'loss', [(0, '0'), (.5, '0.5'), (1, '1')], []), 2.6)
    f.show(lp.curve(L1, -.1, 1.3, 140, BL, 2.2), 3.0, d=.8)
    # ball rolls (gradient descent, computed)
    w = w0; path = [w]
    for _ in range(12):
        w = w - .012 * dL(w); path.append(w)
    bx0, by0 = lp.P(path[0], L1(path[0]))
    ball = '<circle cx="%.1f" cy="%.1f" r="7" fill="%s" stroke="%s" stroke-width="1.6"/>' % (bx0, by0 - 7, tint('am', '.5'), AM)
    pts = [(0, 0, 0)] + [(4.0 + k * .28, lp.X(path[k]) - bx0, lp.Y(L1(path[k])) - by0) for k in range(1, len(path))]
    f.path(ball, pts, t0=3.7, d=.28)
    f.show(T(555, 304, 'calculus: roll downhill to the lowest loss', AM), 4.0)
    wb = path[-1]
    f.show(L(*pl.P(0, B0), *pl.P(9, wb * 9 + B0), GR, 2.4), 7.6)
    f.show(L(lp.X(wb), lp.Y(L1(wb)), lp.X(wb), lp.py + lp.ph, GR, 1.2, '3 3') + pill(lp.X(wb), lp.py - 22, 'w = %.2f' % wb, 'gr', 70), 7.6)
    return f.render(), wb

# ---------- 2.1 probability: bell -> loss ----------
def fig_prob():
    f = Anim('mf2-', 720, 318, 'A bell curve of noise. A point near the centre gets high probability, a point far out gets low probability; '
             'taking minus the log turns those into small and large loss, and the minus-log curve over the gap is exactly a parabola: the squared error.',
             'PROBABILITY · A NOISE ASSUMPTION BECOMES THE LOSS')
    pl = Plot(40, 40, 300, 200, -3, 3, 0, .45)
    phi = lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    f.static(pl.axes('gap = y − ŷ', 'p(gap)', [(-2, '−2'), (0, '0'), (2, '2')], []))
    f.show(pl.curve(phi, -3, 3, 120, BL, 2.2), .3, d=.8)
    for k, (z, tone) in enumerate([(.4, 'gr'), (2.0, 'rd')]):
        t = 1.4 + k * 1.2
        f.show(L(*pl.P(z, 0), *pl.P(z, phi(z)), COL[tone], 1.6, '3 2') + dot(*pl.P(z, phi(z)), 5, tone) +
               T(pl.X(z) + 8, pl.Y(phi(z)) - 6, 'p = %.2f' % phi(z), COL[tone], 'start', mono=True), t)
    lp = Plot(420, 40, 270, 200, -3, 3, 0, 5.5)
    nll = lambda z: -math.log(phi(z)) - (-math.log(phi(0)))
    f.show(lp.axes('gap', '−log p', [(-2, '−2'), (0, '0'), (2, '2')], []), 3.6)
    f.show(lp.curve(nll, -3, 3, 120, GR, 2.4), 4.0, d=.8)
    for z, tone in [(.4, 'gr'), (2.0, 'rd')]:
        f.show(dot(*lp.P(z, nll(z)), 5, tone) + T(lp.X(z) + (-10 if z > 1 else 10), lp.Y(nll(z)) - 8, 'loss %.2f' % nll(z), COL[tone], 'end' if z > 1 else 'start', mono=True), 5.0)
    f.show(T(555, 304, '= ½ · gap² — the squared error', GR, bold=True), 5.6)
    return f.render()

# ---------- 2.2 linear algebra: rows x weights ----------
def fig_linalg():
    f = Anim('mf3-', 720, 250, 'A table of three houses with two features becomes a matrix X; a weight vector w slides next to it; '
             'each row is multiplied by w and summed, filling the prediction vector one entry at a time.', 'LINEAR ALGEBRA · ONE MATRIX PRODUCT PREDICTS EVERY ROW')
    X = [[80, 2], [120, 3], [60, 1]]; w = [3, 20]
    y = [sum(a * b for a, b in zip(r, w)) for r in X]
    cw, ch = 60, 34; x0, y0 = 40, 70
    f.static(T(x0 + cw, y0 - 16, 'X  (size, rooms)', MU) + T(x0 + 2 * cw + 70, y0 - 16, 'w', MU) + T(x0 + 2 * cw + 210, y0 - 16, 'ŷ = X w', MU))
    for i, r in enumerate(X):
        for j, v in enumerate(r):
            f.show(cell(x0 + j * cw, y0 + i * ch, v, cw - 4, h=ch - 4), .2 + i * .15, d=.25)
    wx = x0 + 2 * cw + 50
    for j, v in enumerate(w):
        f.path(cell(wx, y0 + j * ch, v, 40, 'am', h=ch - 4), [(0, 60, 0), (.9, 0, 0)], t0=.8, d=.6)
    f.static(T(wx - 18, y0 + 52, '×', MU, cls='sv-s') + T(wx + 70, y0 + 52, '=', MU, cls='sv-s'))
    yx = x0 + 2 * cw + 180
    for i, r in enumerate(X):
        t = 2.0 + i * 1.3
        f.show(R(x0 - 3, y0 + i * ch - 3, 2 * cw - 2, ch + 2, 'none', AM, 4, 1.6), t, hide=t + 1.2)
        f.show(T(yx + 150, y0 + i * ch + 20, '%d·%d + %d·%d' % (r[0], w[0], r[1], w[1]), AM, 'start', mono=True), t, hide=t + 1.2)
        f.show(cell(yx, y0 + i * ch, y[i], 60, 'gr', h=ch - 4), t + .6)
    f.show(T(40, 210, 'thousands of rows, one line of code: X @ w', MU, 'start'), 6.2)
    return f.render()

# ---------- 2.3 calculus: slope ----------
def fig_calc():
    f = Anim('mf4-', 720, 300, 'The loss curve; at three points a tangent line shows the slope: steep and negative, gentle, then zero at the bottom. '
             'An arrow points against the slope at each, the step shrinks as the slope flattens.', 'CALCULUS · THE SLOPE SAYS WHICH WAY IS DOWN')
    lp = Plot(60, 40, 440, 210, -.1, 1.3, 0, max(L1(-.1), L1(1.3)) * 1.05)
    f.static(lp.axes('slope w', 'loss', [(0, '0'), (.5, '0.5'), (1, '1')], []))
    f.show(lp.curve(L1, -.1, 1.3, 140, BL, 2.2), .2, d=.8)
    wmin = .6
    for _ in range(200): wmin -= .005 * dL(wmin)
    pts = [(.05, 'steep slope → big step'), (.38, 'gentle slope → small step'), (wmin, 'slope 0 → stop')]
    for k, (w, lab) in enumerate(pts):
        t = 1.3 + k * 1.5; g = dL(w); last = k == 2
        dx = .18
        a = lp.P(w - dx, L1(w) - g * dx); b = lp.P(w + dx, L1(w) + g * dx)
        c = GR if last else AM
        s = L(*a, *b, c, 1.8) + dot(*lp.P(w, L1(w)), 5, 'gr' if last else 'am')
        if not last:
            s += arrow(lp.X(w), lp.Y(L1(w)) + 16, lp.X(w - .002 * g * 12), lp.Y(L1(w)) + 16, AM, 1.8)
        f.show(s, t, hide=None if last else t + 1.4)
        f.show(T(560, 100 + k * 26, 'slope %s' % ('%+.1f' % g if abs(g) > .05 else '0'), c, 'start', mono=True, bold=True) + T(640, 100 + k * 26, lab.split('→')[1].strip(), MU, 'start'), t)
    return f.render(), wmin

# ---------- 2.4 statistics: sample means -> CI ----------
SEED = 1
def fig_stats():
    f = Anim('mf5-', 720, 312, 'A population of values; seven samples of 30 are drawn and their means drop onto an axis as dots; '
             'each sample mean gets an interval of plus or minus two standard errors; most intervals cover the true mean line.',
             'STATISTICS · FROM A SAMPLE BACK TO THE TRUTH')
    r = random.Random(SEED)
    MU_, SD, N = 50, 12, 30
    se = SD / math.sqrt(N)
    pl = Plot(40, 50, 480, 200, 40, 60, 0, 7)
    f.static(L(pl.px, pl.py + pl.ph, pl.px + pl.pw, pl.py + pl.ph, MU, 1.2))
    for v in (40, 45, 50, 55, 60):
        f.static(T(pl.X(v), pl.py + pl.ph + 16, str(v), FA, mono=True))
    f.show(L(pl.X(MU_), pl.py - 6, pl.X(MU_), pl.py + pl.ph, GR, 1.6, '5 4') + T(pl.X(MU_), pl.py - 12, 'true mean 50', GR, bold=True), .3)
    hits = 0
    for k in range(7):
        m = sum(r.gauss(MU_, SD) for _ in range(N)) / N
        y = pl.py + 14 + k * 26
        t = 1.0 + k * .9
        ok = abs(m - MU_) <= 2 * se; hits += ok
        tone = 'bl' if ok else 'rd'
        f.path(dot(pl.X(m), y, 5, tone), [(0, 0, -y + 30), (t + .2, 0, 0)], t0=t, d=.4)
        f.show(L(pl.X(m - 2 * se), y, pl.X(m + 2 * se), y, COL[tone], 2) + L(pl.X(m - 2 * se), y - 5, pl.X(m - 2 * se), y + 5, COL[tone], 2) +
               L(pl.X(m + 2 * se), y - 5, pl.X(m + 2 * se), y + 5, COL[tone], 2) + T(pl.X(60) + 12, y + 4, 'sample %d: %.1f' % (k + 1, m), COL[tone], 'start', mono=True), t + .7)
    f.show(T(40, 294, '%d of 7 intervals cover the truth · ±2 SE ≈ 95%% confidence' % hits, MU, 'start'), 6.6)
    return f.render()

if __name__ == '__main__':
    F = {}
    F['chain'], wb = fig_chain(); F['prob'] = fig_prob(); F['lin'] = fig_linalg(); F['calc'], wm = fig_calc(); F['stats'] = fig_stats()
    print('gd w %.3f true-min %.3f' % (wb, wm))
    json.dump({k: palette(v) for k, v in F.items()}, open('/tmp/ml/math-foundations-overview-figs.json', 'w'))
