# -*- coding: utf-8 -*-
"""Extra figures for probability: CDF (1.2) and common distributions (1.3).
Run: python3 probability_fix.py -> /tmp/ml/probability-fix.json"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probability import *  # noqa  (regenerates the main json too; harmless)

def ncdf(x): return .5 * (1 + math.erf(x / math.sqrt(2)))

def fcdf():
    F = Fig('pcd-', 720, 420, 'Top left: the eleven bars of the sum of two dice. Bottom left: each bar is added in turn to a running total, '
            'building a staircase that climbs from 0 to 1. Top right: a bell-shaped density; a moving line sweeps left to right and '
            'the shaded area behind it grows. Bottom right: that area, plotted as it grows, traces an S-shaped curve from 0 to 1.',
            'DISCRETE · BARS ADD UP TO A STAIRCASE')
    F(T(410, 14, 'CONTINUOUS · AREA TRACES AN S-CURVE', MU, 'start', 'sv-hv'))
    pm = {s: sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s) / 36 for s in range(2, 13)}
    A = Plot(40, 44, 280, 120, (1.3, 12.7), (0, 7 / 36))
    F(A.axes([(v, str(v)) for v in range(2, 13)], [(6 / 36, '6/36')]))
    for k, s in enumerate(range(2, 13)):
        F(A.bar(s, pm[s], 18, BRA('.22'), BR), show=.3 + k * .06)
    Cd = Plot(40, 232, 280, 120, (1.3, 12.7), (0, 1))
    F(Cd.axes([(v, str(v)) for v in range(2, 13)], [(.5, '0.5'), (1, '1')], 'x'))
    F(T(44, 226, 'F(x) = P(X ≤ x)', FI, 'start', 'sv-s'))
    t = 1.2; cum = 0
    for s in range(2, 13):
        prev = cum; cum += pm[s]
        F(R(A.px(s) - 12, A.py(pm[s]) - 3, 24, A.py(0) - A.py(pm[s]) + 6, 'none', VI, 3, 2), show=t, hide=t + .4, d=.12)
        x1 = min(Cd.px(s + 1), Cd.px(12.7))
        F(L(Cd.px(s), Cd.py(prev), Cd.px(s), Cd.py(cum), VI, 1.2, '2 2') + L(Cd.px(s), Cd.py(cum), x1, Cd.py(cum), FI, 2.4)
          + C(Cd.px(s), Cd.py(cum), 3, FI), show=t + .1, d=.15)
        t += .45
    assert abs(cum - 1) < 1e-9
    F(T(Cd.px(7) + 8, Cd.py(21 / 36) + 16, 'F(7) = 21/36', FI, 'start'), show=t)
    # continuous
    B = Plot(410, 44, 280, 120, (-3.2, 3.2), (0, .42))
    F(B.axes([(v, str(v)) for v in (-3, -2, -1, 0, 1, 2, 3)], []), show=t + .2)
    F(P(B.curve(npdf, -3.2, 3.2), BR, 2.2), show=t + .2)
    D = Plot(410, 232, 280, 120, (-3.2, 3.2), (0, 1))
    F(D.axes([(v, str(v)) for v in (-3, -2, -1, 0, 1, 2, 3)], [(.5, '0.5'), (1, '1')], 'x'), show=t + .2)
    F(T(414, 226, 'F(x) = area to the left of x', FI, 'start', 'sv-s'), show=t + .2)
    t += .8; n = 24; xs = [-3.2 + 6.4 * i / n for i in range(n + 1)]
    for i in range(n):
        a_, b_ = xs[i], xs[i + 1]; tt = t + i * .12
        F(area(B.curve(npdf, a_, b_, 4), B.py(0), FIA('.25')), show=tt, d=.1)
        F(P(D.curve(ncdf, a_, b_, 4), FI, 2.4), show=tt, d=.1)
        last = i == n - 1
        F(L(B.px(b_), B.py(0) + 2, B.px(b_), B.py(.42), VI, 1.4) + L(D.px(b_), D.py(0), D.px(b_), D.py(ncdf(b_)), VI, 1, '2 2'),
          show=tt, hide=None if last else tt + .12, d=.06)
    t += n * .12
    F(T(D.px(0) + 8, D.py(.5) + 16, 'F(0) = 0.5', FI, 'start'), show=t + .2)
    F(T(0, 408, 'adding bars gives jumps; adding area gives a smooth climb — both end at 1, and the slope of F is f', MU, 'start'), show=t + .6)
    return F.render()

def comb(n, k): return math.comb(n, k)

def fdist():
    F = Fig('pdi-', 720, 540, 'Five common distributions drawn in turn from their formulas. Bernoulli with p 0.3: two bars, 0.7 and 0.3. '
            'Binomial with n 10 and p 0.5: a symmetric hump of bars peaking at 5. Poisson with rate 3: bars skewed right, peaking at 2 and 3. '
            'Uniform from 0 to 1: a flat line. Gaussian with mean 0 and sd 1: a bell, then bands within one, two and three standard '
            'deviations shade in, holding 68, 95 and 99.7 percent.', 'COMMON DISTRIBUTIONS · DRAWN FROM THEIR FORMULAS')
    panels = []
    W, H = 190, 110
    def head(x, y, name, form, stats, t):
        F(T(x, y, name, TX, 'start', 'sv-s', bold=True), show=t)
        F(T(x, y + 16, form, MU, 'start'), show=t)
        F(T(x, y + H + 78, stats, FI, 'start', mono=True), show=t + .9)
    def bars(Pl, d, t, bw):
        for k, (v, p) in enumerate(d):
            F(Pl.bar(v, p, bw, BRA('.22'), BR), show=t + .2 + k * .05)
    # Bernoulli
    x0, y0, t = 10, 40, .3
    head(x0, y0, 'Bernoulli(p = 0.3)', 'P(1) = p, P(0) = 1 − p', 'E = p · Var = p(1 − p)', t)
    A = Plot(x0 + 20, y0 + 40, W - 30, H, (-.6, 1.6), (0, 1))
    F(A.axes([(0, '0'), (1, '1')], [(.5, '0.5'), (1, '1')]), show=t)
    bars(A, [(0, .7), (1, .3)], t, 40)
    # Binomial
    x0, t = 250, 1.8
    d = [(k, comb(10, k) * .5 ** 10) for k in range(11)]; assert abs(sum(p for _, p in d) - 1) < 1e-12
    head(x0, y0, 'Binomial(n = 10, p = 0.5)', 'P(k) = C(n,k) pᵏ (1 − p)ⁿ⁻ᵏ', 'E = np · Var = np(1 − p)', t)
    A = Plot(x0 + 20, y0 + 40, W - 30, H, (-.7, 10.7), (0, .3))
    F(A.axes([(0, '0'), (5, '5'), (10, '10')], [(.25, '0.25')]), show=t)
    bars(A, d, t, 10)
    # Poisson
    x0, t = 490, 3.3
    d = [(k, math.exp(-3) * 3 ** k / math.factorial(k)) for k in range(11)]
    head(x0, y0, 'Poisson(λ = 3)', 'P(k) = λᵏ e^(−λ) / k!', 'E = λ · Var = λ', t)
    A = Plot(x0 + 20, y0 + 40, W - 30, H, (-.7, 10.7), (0, .3))
    F(A.axes([(0, '0'), (5, '5'), (10, '10')], [(.25, '0.25')]), show=t)
    bars(A, d, t, 10)
    # Uniform
    x0, y0, t = 10, 290, 4.8
    head(x0, y0, 'Uniform(a = 0, b = 1)', 'f(x) = 1 / (b − a) on [a, b]', 'E = (a+b)/2 · Var = (b−a)²/12', t)
    A = Plot(x0 + 20, y0 + 40, W - 30, H, (-.4, 1.4), (0, 1.4))
    F(A.axes([(0, '0'), (1, '1')], [(1, '1')]), show=t)
    F(area([(A.px(0), A.py(1)), (A.px(1), A.py(1))], A.py(0), BRA('.18')) + L(A.px(0), A.py(1), A.px(1), A.py(1), BR, 2.2)
      + L(A.px(-.4), A.py(0), A.px(0), A.py(0), BR, 2.2) + L(A.px(1), A.py(0), A.px(1.4), A.py(0), BR, 2.2), show=t + .3)
    # Gaussian with bands
    x0, t = 250, 6.2
    F(T(x0, y0, 'Gaussian(μ = 0, σ = 1)', TX, 'start', 'sv-s', bold=True), show=t)
    F(T(x0, y0 + 16, 'f(x) = e^(−(x−μ)²/2σ²) / (σ√2π)', MU, 'start'), show=t)
    F(T(x0 + 440, y0, 'E = μ · Var = σ²', FI, 'end', mono=True), show=t + .9)
    G = Plot(x0 + 20, y0 + 40, 380, H, (-3.6, 3.6), (0, .42))
    F(L(G.x, G.py(0), G.x + G.w, G.py(0), MU, 1.1), show=t)
    for v in (-3, -2, -1, 0, 1, 2, 3): F(T(G.px(v), G.py(.42) - 2, ('%+dσ' % v) if v else 'μ', FA, cls='sv-l') + L(G.px(v), G.py(.40), G.px(v), G.py(0), 'var(--rule)', 1, '2 4'), show=t)
    tb = draw(F, G.curve(npdf, -3.6, 3.6), t + .3, BR, 1.0)
    for k, (al, lab) in enumerate([('.30', '68%'), ('.18', '95%'), ('.10', '99.7%')], 1):
        p = ncdf(k) - ncdf(-k); assert abs(p * 100 - float(lab[:-1])) < .5
        tk = tb + .3 + (k - 1) * .8
        F(area(G.curve(npdf, -k, -k + 1 if k > 1 else 0, 20), G.py(0), FIA(al)) +
          area(G.curve(npdf, k - 1 if k > 1 else 0, k, 20), G.py(0), FIA(al)), show=tk)
        yb = G.py(0) + 26 + k * 0  # labels row under ticks
        yb = G.py(0) + 14 + k * 13
        F(L(G.px(-k), yb, G.px(k), yb, FI, 1.4) + L(G.px(-k), yb - 4, G.px(-k), yb + 4, FI, 1.4) + L(G.px(k), yb - 4, G.px(k), yb + 4, FI, 1.4) +
          T(G.px(k) + 8, yb + 4, lab, FI, 'start', 'sv-l'), show=tk)
    F(T(0, 532, 'counts → bars (PMF) · measurements → curves (PDF) · each shape is one formula with one or two knobs', MU, 'start'), show=tb + 3)
    return F.render()

json.dump({'CDF': fcdf(), 'DIST': fdist()}, open('/tmp/ml/probability-fix.json', 'w'))
print('fix ok')
