# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/04-core-concepts/overfitting-regularization.
Data: 10 points of y = sin(2*pi*x) + N(0, 0.3^2) (seed 194), validation 60 points (seed 99).
Run: python3 overfitting_regularization.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fitkit_bvof import *  # noqa

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/04-core-concepts/overfitting-regularization/index.html')
rng = random.Random(194)
XS = [(i + .2 + .6 * rng.random()) / 10 for i in range(10)]; YS = [f(x) + rng.gauss(0, SIG) for x in XS]
VX, VY = sample(random.Random(99), 60, fixed=False)
figs = {}
def median(v): v = sorted(v); n = len(v); return (v[n // 2] + v[(n - 1) // 2]) / 2

def errs(w): return mse(w, XS, YS), mse(w, VX, VY)

# ---------- 1.x three fits ----------
def fitfig(pre, d, cap_, aria, verdict, lam=0.0, lasso_w=None):
    w = lasso_w or fit(XS, YS, d, lam); tr, va = errs(w)
    an = Anim(pre, 720, 290, aria, cap_, 2.5)
    p, ax = fit_plot(pre, 30, 40, 430, 200, (-2.0, 2.0))
    an.static(ax)
    for k, (x, y) in enumerate(zip(XS, YS)): an.show(p.dot(x, y, BR, 3.8), .2 + k * .08)
    for k, (x, y) in enumerate(zip(VX[::3], VY[::3])):
        an.show('<circle cx="%.1f" cy="%.1f" r="3" fill="none" stroke="%s" stroke-width="1.2"/>' % (p.px(x), p.py(y), VI), 2.6 + k * .04)
    p.draw(an, curve_pts(lambda x: pred(w, x), n=200), 1.0, 1.4, FI, 2.6, k=14)
    an.static(R(490, 52, 12, 12, BR, 'none', 6) + T(508, 62, 'train point', MU, 'start') +
              '<circle cx="496" cy="82" r="5" fill="none" stroke="%s" stroke-width="1.4"/>' % VI + T(508, 86, 'validation point', MU, 'start'))
    X0, SC = 490, 200 / .6
    for i, (lab, v, c, t) in enumerate((('train error', tr, BR, 2.2), ('validation error', va, VI, 3.6))):
        y = 120 + i * 52
        an.show(T(X0, y, lab, c, 'start'), t)
        an.show(R(X0, y + 8, max(min(v, .6) * SC, 2), 18, c, 'none', 2), t + .1)
        an.show(T(X0 + max(min(v, .6) * SC, 2) + 6, y + 22, '%.3f' % v, c, 'start', bold=True), t + .3)
    an.show(T(X0, 248, verdict, FI, 'start', bold=True), 4.4)
    return an.render(), (tr, va)

figs['F11'], E1 = fitfig('u1-', 1, 'UNDERFIT · WRONG EVERYWHERE', 'A straight line fitted to ten sine-shaped points. It misses the train points and the validation points alike: train error 0.19, validation error 0.34.', 'both high → underfit (high bias)')
figs['F12'], E3 = fitfig('g1-', 3, 'GOOD FIT · FOLLOWS THE SHAPE, NOT THE NOISE', 'A cubic fitted to the same ten points follows the sine shape. Train and validation error are both low and close: 0.04 and 0.12.', 'both low, small gap → good fit')
figs['F13'], E9 = fitfig('o1-', 9, 'OVERFIT · THROUGH EVERY POINT, WRONG BETWEEN THEM', 'A degree-9 polynomial passes exactly through all ten train points and swings between them. Train error is 0, validation error 0.25.', 'train 0, val high → overfit (high variance)')
assert E1[0] > .15 and E1[1] > .3 and E3[1] < .13 and E9[0] < 1e-3 and E9[1] > 2 * E3[1]

# ---------- 2.1 diagnosis quadrant ----------
def quad():
    an = Anim('q2-', 720, 300, 'A two by two grid: train error low or high against validation error low or high. Three models from above drop into their cells: degree 3 into low-low, good fit; degree 9 into low train, high validation, overfit; degree 1 into high-high, underfit. The fourth cell, high train but low validation, means a broken split.', 'TWO NUMBERS · FOUR DIAGNOSES', 2.5)
    X0, Y0, CW, CH = 170, 50, 250, 100
    an.static(T(X0 + CW, 40, 'validation error', MU) + T(X0 + CW / 2, Y0 + 2 * CH + 22, 'low', FA) + T(X0 + 1.5 * CW, Y0 + 2 * CH + 22, 'high', FA))
    an.static(T(X0 - 70, Y0 + CH, 'train', MU, 'middle') + T(X0 - 70, Y0 + CH + 14, 'error', MU, 'middle') +
              T(X0 - 12, Y0 + CH / 2 + 4, 'low', FA, 'end') + T(X0 - 12, Y0 + 1.5 * CH + 4, 'high', FA, 'end'))
    cells = {(0, 0): ('good fit', FI), (0, 1): ('overfit · high variance', VI), (1, 1): ('underfit · high bias', BR), (1, 0): ('broken split / leakage', RO)}
    for (r, c), (lab, col) in cells.items():
        an.static(R(X0 + c * CW, Y0 + r * CH, CW - 6, CH - 6, 'var(--bg)', RULE_HI, 6))
    for k, ((r, c), d, (tr, va), t) in enumerate((((1, 1), 1, E1, .6), ((0, 0), 3, E3, 2.0), ((0, 1), 9, E9, 3.4))):
        lab, col = cells[(r, c)]
        an.path(pill(0, 0, 'degree %d · %.2f / %.2f' % (d, tr, va), None, 170), [(0, 600, 0), (t + .5, X0 + c * CW + CW / 2 - 3, Y0 + r * CH + 52)], t0=t, d=.8)
        an.show(R(X0 + c * CW, Y0 + r * CH, CW - 6, CH - 6, 'rgba(var(--blue-a),.0)', col, 6, 2), t + 1.3)
        an.show(T(X0 + c * CW + CW / 2 - 3, Y0 + r * CH + 30, lab, col, bold=True), t + 1.3)
    lab, col = cells[(1, 0)]
    an.show(T(X0 + CW / 2 - 3, Y0 + CH + 30, lab, col, bold=True) + T(X0 + CW / 2 - 3, Y0 + CH + 52, 'check the split first', MU), 5.0)
    return an.render()
figs['F21'] = quad()

# ---------- 2.2 learning curves ----------
NS = [12, 16, 24, 40, 70, 120, 250, 500, 1000]
GRIDV = [(i + .5) / 400 for i in range(400)]
def lcurve(d, R_=60):
    r = random.Random(7 + d); out = []
    for n in NS:
        tr, va = [], []
        for _ in range(R_):
            xs, ys = sample(r, n, fixed=False); w = fit(xs, ys, d)
            tr.append(mse(w, xs, ys)); va.append(sum((pred(w, x) - f(x)) ** 2 for x in GRIDV) / 400 + SIG ** 2)
        out.append((n, median(tr), median(va)))
    return out
def lcfig(pre, d, cap_, aria, verdict):
    lc = lcurve(d)
    an = Anim(pre, 720, 300, aria, cap_, 2.5)
    p = Plot(pre, 80, 40, 520, 200, (12, 1000), (0, .5), xlog=True)
    an.static(p.clip() + p.axes([(n, str(n)) for n in (12, 40, 120, 500, 1000)], [(v, '%.1f' % v) for v in (.1, .2, .3, .4, .5)], 'training set size n (log scale)', 'error'))
    an.show(p.line([(12, .09), (1000, .09)], GH, 1.6, '5 4') + T(p.px(12) + 6, p.py(.09) - 5, 'noise floor σ²', FA, 'start'), .3)
    tr = [(n, t) for n, t, _ in lc]; va = [(n, min(v, .62)) for n, _, v in lc]
    for k, ((n, a_), (_, b)) in enumerate(zip(tr, va)):
        t = .7 + k * .45
        an.show(p.dot(n, a_, BR, 3.4), t)
        if b < .5: an.show(p.dot(n, b, VI, 3.4), t)
        if k: an.show(p.line(tr[k - 1:k + 1], BR, 2.2) + p.line(va[k - 1:k + 1], VI, 2.2), t - .1)
    te = .7 + len(NS) * .45
    an.show(T(p.px(1000) + 6, p.py(lc[-1][1]) + (14 if d > 1 else 16), 'train', BR, 'start', bold=True), te)
    an.show(T(p.px(1000) + 6, p.py(lc[-1][2]) - 4, 'validation', VI, 'start', bold=True), te)
    g0 = lc[2]; gx = p.px(g0[0])
    an.show(L(gx, p.py(min(g0[2], .5)), gx, p.py(g0[1]), FI, 1.8) + T(gx - 6, (p.py(min(g0[2], .5)) + p.py(g0[1])) / 2 + 4, 'gap %.2f' % (g0[2] - g0[1]), FI, 'end', bold=True), te + .3)
    an.show(T(80, 292, verdict % dict(n=NS[-1], v=lc[-1][2], g=lc[-1][2] - lc[-1][1]), FI, 'start', bold=True), te + .9)
    return an.render(), lc
figs['F22'], LC9 = lcfig('l9-', 9, 'DEGREE 9 · BIG GAP THAT CLOSES WITH DATA', 'Learning curve of a degree-9 polynomial: train error starts near zero and climbs, validation error starts very high and falls; the two meet at the noise floor as n grows to 1000.', 'gap closes → more data helps · at n = %(n)d val %(v).3f, gap %(g).3f')
figs['F23'], LC1 = lcfig('l1-', 1, 'DEGREE 1 · NO GAP, STUCK ABOVE THE FLOOR', 'Learning curve of a straight line: train and validation error meet almost at once around 0.29, far above the noise floor of 0.09, and stay there as n grows.', 'curves meet above the floor → more data is wasted · stronger model needed')
assert LC9[2][2] - LC9[2][1] > .1 and LC9[-1][2] < .1 and LC1[-1][2] > .25 and LC1[2][2] - LC1[2][1] < .08

# ---------- 3.x regularization ----------
def coef_fig(pre, cap_, aria, kind):
    lams = [0, .001, .01, .1] if kind == 'L2' else [.001, .003, .01, .03]
    ws = []
    for lam in lams:
        ws.append(fit(XS, YS, 9, lam) if kind == 'L2' else lasso(lam))
    an = Anim(pre, 720, 330, aria, cap_, 2.5)
    p, ax = fit_plot(pre, 30, 40, 330, 190, (-2.0, 2.0))
    an.static(ax)
    for x, y in zip(XS, YS): an.static(p.dot(x, y, BR, 3.6))
    # coefficient bars
    BX, BY, BW = 410, 135, 300
    an.static(T(BX, 46, 'weights w₁ … w₉', MU, 'start') + L(BX, BY, BX + BW, BY, RULE_HI, 1))
    for j in range(1, 10): an.static(T(BX + (j - .5) * BW / 9, 232, 'w%d' % j, FA, cls='sv-l'))
    t = .4; SC = 80 / 6
    for k, (lam, w) in enumerate(zip(lams, ws)):
        last = k == len(lams) - 1
        hide = None if last else t + 1.6
        an.show(p.line(curve_pts(lambda x: pred(w, x), n=200), FI if last else VI, 2.4), t, hide=hide)
        bars = ''
        for j in range(1, 10):
            v = max(-6, min(6, w[j])); h = abs(v) * SC
            zero = abs(w[j]) < 1e-6
            bx = BX + (j - 1) * BW / 9 + 6
            bars += R(bx, BY - h if v > 0 else BY, BW / 9 - 12, max(h, 1.2), 'var(--ghost)' if zero else (FI if last else VI), 'none', 2)
            if zero and kind == 'L1': bars += T(bx + (BW / 9 - 12) / 2, BY - 6, '0', FA, cls='sv-l')
        an.show(bars, t, hide=hide)
        tr, va = errs(w); nz = sum(abs(c) > 1e-6 for c in w[1:])
        lab = 'λ = %g · train %.3f · val %.3f' % (lam, tr, va) + (' · %d of 9 weights ≠ 0' % nz if kind == 'L1' else ' · largest |w| = %.1f' % max(abs(c) for c in w[1:]))
        an.show(T(30, 268, lab, FI if last else VI, 'start', bold=True), t, hide=hide)
        t += 1.8
    an.show(T(30, 296, ('weights shrink smoothly, none hits zero' if kind == 'L2' else 'weights drop to exactly zero one by one → feature selection'), MU, 'start'), t - 1.2)
    return an.render(), [errs(w) for w in ws], ws

def lasso(lam, it=1500):
    d = 9; X = [feats(x, d) for x in XS]; n = len(XS); w = [0.0] * (d + 1)
    for _ in range(it):
        for j in range(d + 1):
            r = [y - sum(w[k] * X[i][k] for k in range(d + 1) if k != j) for i, y in enumerate(YS)]
            rho = sum(X[i][j] * r[i] for i in range(n)) / n; z = sum(X[i][j] ** 2 for i in range(n)) / n
            w[j] = rho / z if j == 0 else math.copysign(max(abs(rho) - lam, 0), rho) / z
    return w

figs['F31'], E_L2, W_L2 = coef_fig('r2-', 'L2 · SHRINK EVERY WEIGHT', 'A degree-9 polynomial with an L2 penalty. As lambda grows from 0 to 0.1 the wild curve calms into a smooth wave and the nine weight bars shrink towards zero together, none reaching exactly zero.', 'L2')
figs['F32'], E_L1, W_L1 = coef_fig('r1-', 'L1 · SET WEIGHTS TO EXACTLY ZERO', 'A degree-9 polynomial with an L1 penalty. As lambda grows, weight bars disappear one by one to exactly zero; at lambda 0.03 only a few weights remain and the curve is a smooth wave.', 'L1')
assert E_L2[-1][1] < E_L2[0][1] and sum(abs(c) < 1e-6 for c in W_L1[-1][1:]) >= 5

# 3.3 early stopping
def early():
    d = 9; X = [feats(x, d) for x in XS]; n = len(XS); w = [0.0] * (d + 1); hist = []
    marks = sorted(set(int(10 ** (k / 8)) for k in range(0, 49)))
    for it in range(1, marks[-1] + 1):
        r = [sum(a_ * b for a_, b in zip(w, row)) - y for row, y in zip(X, YS)]
        g = [2 * sum(r[i] * X[i][j] for i in range(n)) / n for j in range(d + 1)]
        w = [a_ - .3 * b for a_, b in zip(w, g)]
        if it in marks: hist.append((it, mse(w, XS, YS), mse(w, VX, VY)))
    return hist
EH = early()
def esfig():
    an = Anim('es3-', 720, 300, 'Gradient descent on a degree-9 polynomial, error against training step on a log scale. Train error keeps falling. Validation error falls until about 60 steps, then climbs. A marker drops at the lowest validation point: stop there.', 'EARLY STOPPING · STOP WHEN VALIDATION TURNS UP', 2.5)
    p = Plot('es3-', 80, 40, 520, 200, (1, 10 ** 6), (0, 1.2), xlog=True)
    an.static(p.clip() + p.axes([(10 ** k, '10' + '⁰¹²³⁴⁵⁶'[k]) for k in range(7)], [(v, '%.1f' % v) for v in (.2, .4, .6, .8, 1.0, 1.2)], 'training steps (log scale)', 'error'))
    tr = [(i, a_) for i, a_, _ in EH]; va = [(i, b) for i, _, b in EH]
    p.draw(an, tr, .5, 4.0, BR, 2.4, k=16); p.draw(an, va, .5, 4.0, VI, 2.4, k=16)
    an.show(T(p.px(3), p.py(tr[1][1]) + 20, 'train', BR, 'start', bold=True) + T(p.px(3), p.py(va[1][1]) - 12, 'validation', VI, 'start', bold=True), 4.5)
    bi, bt, bv = min(EH, key=lambda h: h[2])
    an.show(L(p.px(bi), p.py(0), p.px(bi), p.py(bv) - 8, FI, 1.4, '3 3') + '<circle cx="%.1f" cy="%.1f" r="7" fill="none" stroke="%s" stroke-width="2"/>' % (p.px(bi), p.py(bv), FI), 5.0)
    an.show(T(p.px(bi) + 10, p.py(bv) - 14, 'stop at step %d · val %.3f' % (bi, bv), FI, 'start', bold=True), 5.2)
    an.show(T(80, 292, 'keep going to 10⁶ steps → train %.3f, val %.3f' % (EH[-1][1], EH[-1][2]), MU, 'start'), 5.8)
    return an.render(), (bi, bv)
figs['F33'], ES = esfig(); assert ES[1] < EH[-1][2] / 3

# 3.4 dropout
def dropout():
    an = Anim('dr3-', 720, 280, 'A small network: 3 inputs, two hidden layers of 5, one output. In each of three training steps a different random set of hidden neurons is switched off and greyed out, with their connections. At inference every neuron is back on.', 'DROPOUT · A DIFFERENT THINNED NETWORK EACH STEP', 2.5)
    L_ = [3, 5, 5, 1]; XL = [90, 250, 410, 570]
    pos = [[(XL[l], 140 + (i - (n - 1) / 2) * 44) for i in range(n)] for l, n in enumerate(L_)]
    rr = random.Random(4); masks = [[set(rr.sample(range(5), 2)) for _ in range(2)] for _ in range(3)]
    def net(mask, tone):
        o = ''
        for l in range(3):
            for i, a_ in enumerate(pos[l]):
                for j, b in enumerate(pos[l + 1]):
                    off = (l > 0 and mask and i in mask[l - 1]) or (l + 1 in (1, 2) and mask and j in mask[l])
                    o += L(a_[0] + 11, a_[1], b[0] - 11, b[1], 'var(--rule)' if off else tone, .9 if off else 1.1, '2 3' if off else None)
        for l in range(4):
            for i, (x, y) in enumerate(pos[l]):
                off = l in (1, 2) and mask and i in mask[l - 1]
                o += '<circle cx="%d" cy="%.1f" r="11" fill="%s" stroke="%s" stroke-width="1.4"/>' % (x, y, 'var(--sunk)' if off else 'var(--bg)', 'var(--ghost)' if off else tone)
                if off: o += T(x, y + 4, '×', FA)
        return o
    t = .3
    an.show(net(None, BR), t, hide=t + 1.0)
    for k, m in enumerate(masks):
        t += 1.0
        an.show(net(m, VI) + T(640, 140, 'step %d' % (k + 1), VI, 'start', bold=True) + T(640, 158, '4 of 10 off', MU, 'start'), t, hide=t + 1.6)
        t += .6
    t += 1.0
    an.show(net(None, FI) + T(640, 140, 'inference', FI, 'start', bold=True) + T(640, 158, 'all neurons on', MU, 'start'), t)
    an.static(T(90, 272, 'inputs', FA, cls='sv-l') + T(330, 272, 'hidden layers', FA, cls='sv-l') + T(570, 272, 'output', FA, cls='sv-l'))
    return an.render()
figs['F34'] = dropout()

# 3.5 augmentation
def augment():
    an = Anim('ag3-', 720, 250, 'One training image, a small arrow shape on a grid, produces three new samples: flipped, shifted and rotated. Each copy keeps the same label. Four samples now teach the model the shape instead of the exact pixels.', 'DATA AUGMENTATION · ONE SAMPLE → MANY', 2.5)
    G = [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (3, 1), (3, 3), (2, 0), (2, 4)]
    def img(x0, y0, cells, tone):
        o = R(x0, y0, 120, 120, 'var(--bg)', RULE_HI, 4)
        for i in range(1, 6): o += L(x0 + i * 20, y0, x0 + i * 20, y0 + 120, 'var(--rule)', .6) + L(x0, y0 + i * 20, x0 + 120, y0 + i * 20, 'var(--rule)', .6)
        for c, r in cells: o += R(x0 + c * 20 + 1, y0 + r * 20 + 1, 18, 18, tone, 'none', 2)
        return o
    an.static(img(20, 50, G, BR) + T(80, 194, 'original', TX) + pill(80, 204, 'label: arrow', None, 100))
    vars_ = [('flip', [(5 - c, r) for c, r in G]), ('shift', [(c + 1, r + 1) for c, r in G]), ('rotate 90°', [(5 - r, c) for c, r in G])]
    for k, (nm, cells) in enumerate(vars_):
        x0 = 200 + k * 170; t = .6 + k * 1.1
        an.path(img(x0, 50, cells, VI if k < 2 else VI), [(0, 20 - x0, 0), (t + .1, 0, 0)], t0=t, d=.8)
        an.show(T(x0 + 60, 194, nm, VI, bold=True) + pill(x0 + 60, 204, 'label: arrow', None, 100), t + .8)
        an.show(arrow(146, 110 + (k - 1) * 0, x0 - 6, 110, 'var(--rule-hi)', 1, '3 3'), t, hide=t + .9)
    an.show(T(20, 246, '1 labelled sample → 4 · same label, new pixels', FI, 'start', bold=True), 4.2)
    return an.render()
figs['F35'] = augment()

BODY = '''<section id="overfit-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Same ten points, three models: a model can be <em>too simple</em>, <em>about right</em>, or <em>memorize the noise</em>. Only the validation points tell them apart.</p>
  <div class="subsec" id="overfit-s1-1">
    <h3 class="ssh"><b>1.1</b>Underfitting</h3>
    <p class="skey">Too simple: <em>wrong on train and validation alike</em>.</p>
{F11}
  </div>
  <div class="subsec" id="overfit-s1-2">
    <h3 class="ssh"><b>1.2</b>Good fit</h3>
    <p class="skey">Follows the <em>shape</em>, ignores the noise.</p>
{F12}
  </div>
  <div class="subsec" id="overfit-s1-3">
    <h3 class="ssh"><b>1.3</b>Overfitting</h3>
    <p class="skey">Passes through <em>every train point</em> and is wrong between them.</p>
{F13}
    <ul class="why">
      <li>Train error 0 is a warning, not a success: with 10 points a degree-9 polynomial can always hit them all.</li>
      <li>Why simple and flexible models fail in opposite ways: <a href="../bias-variance-tradeoff/index.html">Bias–variance tradeoff</a>.</li>
    </ul>
  </div>
</section>

<section id="overfit-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Diagnosis</h2></div>
  <p class="key">Two numbers, <em>train error and validation error</em>, say what is broken; their curves over <span class="mth"><var>n</var></span> say whether more data will help.</p>
  <div class="subsec" id="overfit-s2-1">
    <h3 class="ssh"><b>2.1</b>Train vs validation error</h3>
    <p class="skey"><em>Level</em> of both numbers is bias, the <em>gap</em> between them is variance.</p>
{F21}
    <ul class="why">
      <li>High train error with low validation error is not a model problem: check the split for leakage — see <a href="../train-val-test-cv/index.html">Train/val/test &amp; cross-validation</a>.</li>
    </ul>
  </div>
  <div class="subsec" id="overfit-s2-2">
    <h3 class="ssh"><b>2.2</b>Learning curve: gap that closes</h3>
    <p class="skey">Train and validation error <em>against training set size</em>: a big gap that shrinks means more data pays off.</p>
{F22}
  </div>
  <div class="subsec" id="overfit-s2-3">
    <h3 class="ssh"><b>2.3</b>Learning curve: curves that meet too high</h3>
    <p class="skey">Curves that meet <em>above the noise floor</em> mean more data is wasted.</p>
{F23}
    <ul class="why">
      <li>Read the <b>gap</b>, not the height: the straight line has lower error at small <span class="mth"><var>n</var></span>, yet it is the model that should not get more data.</li>
      <li>Labeling is expensive; this plot answers "are 10,000 more samples worth it" before you pay.</li>
    </ul>
  </div>
</section>

<section id="overfit-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Regularization</h2></div>
  <p class="key"><b>Regularization</b> deliberately constrains the model so it cannot memorize noise — paying a little train error for a lot less validation error.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>L</var><sub>reg</sub></span></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i>1</i><i><var>n</var></i></span> Σ (<var>ŷ</var><sub>i</sub> − <var>y</var><sub>i</sub>)<sup>2</sup></span><em>data loss: fit the points</em></span>
      <span class="op">+</span>
      <span class="t"><span><var>λ</var> Σ <var>w</var><sub>j</sub><sup>2</sup></span><em>L2 penalty: small weights</em></span>
    </div>
    <div class="line">
      <span class="t"><span><var>L</var><sub>reg</sub></span></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i>1</i><i><var>n</var></i></span> Σ (<var>ŷ</var><sub>i</sub> − <var>y</var><sub>i</sub>)<sup>2</sup></span><em>data loss: fit the points</em></span>
      <span class="op">+</span>
      <span class="t"><span><var>λ</var> Σ |<var>w</var><sub>j</sub>|</span><em>L1 penalty: few weights</em></span>
    </div>
    <dl>
      <dt>λ</dt><dd>regularization strength, chosen on validation data</dd>
      <dt>w<sub>j</sub></dt><dd>model weights; the intercept is not penalized</dd>
    </dl>
  </div>
  <div class="subsec" id="overfit-s3-1">
    <h3 class="ssh"><b>3.1</b>L2 (weight decay)</h3>
    <p class="skey">Penalizing <span class="mth"><var>w</var><sup>2</sup></span> <em>shrinks every weight a little</em>; the curve calms down.</p>
{F31}
    <ul class="why"><li>Default for linear models and neural networks; in deep learning it is called <b>weight decay</b>.</li></ul>
  </div>
  <div class="subsec" id="overfit-s3-2">
    <h3 class="ssh"><b>3.2</b>L1</h3>
    <p class="skey">Penalizing <span class="mth">|<var>w</var>|</span> <em>drives some weights to exactly zero</em>.</p>
{F32}
    <ul class="why"><li>Use it when you suspect most features are useless. Penalty shapes and ElasticNet: <a href="../../05-classical-ml/ridge-lasso-elasticnet/index.html">Ridge, Lasso &amp; ElasticNet</a>.</li></ul>
  </div>
  <div class="subsec" id="overfit-s3-3">
    <h3 class="ssh"><b>3.3</b>Early stopping</h3>
    <p class="skey">Watch validation error during training and <em>stop at its minimum</em>.</p>
{F33}
    <ul class="why"><li>Works for any iterative method — boosting, neural networks — and adds no penalty term.</li></ul>
  </div>
  <div class="subsec" id="overfit-s3-4">
    <h3 class="ssh"><b>3.4</b>Dropout</h3>
    <p class="skey">Switch off <em>random neurons each training step</em>, so no single path can memorize.</p>
{F34}
    <ul class="why"><li>Only during training: forgetting to turn it off at inference makes predictions random. Covered in depth on the deep learning shelf.</li></ul>
  </div>
  <div class="subsec" id="overfit-s3-5">
    <h3 class="ssh"><b>3.5</b>Data augmentation</h3>
    <p class="skey">Make <em>plausible variants</em> of each sample with the same label.</p>
{F35}
    <ul class="why">
      <li>Images: flip, crop, rotate. Text: synonym swap, back-translation. Audio: time shift, noise.</li>
      <li>Simpler still: <b>reduce complexity</b> (lower degree, smaller <code>max_depth</code>, fewer layers) — usually the first thing to try.</li>
    </ul>
  </div>
</section>

''' + REPLAY + '''

<footer>Machine learning · Core concepts · diagnosis and treatment. Error decomposition is in <a href="../bias-variance-tradeoff/index.html">Bias–variance tradeoff</a>; how to split data is in <a href="../train-val-test-cv/index.html">Train/val/test &amp; cross-validation</a>.</footer>
'''

if __name__ == '__main__':
    body = BODY
    for k, v in figs.items():
        assert '{%s}' % k in body, k
        body = body.replace("{%s}" % k, solid_brand(palette(v)))
    s = open(PAGE).read()
    i = s.index('<section'); j = s.index('</article>')
    s = s[:i] + body + '\n      ' + s[j:]
    s = s.replace('data-blurb="Diagnose with numbers, read learning curves to decide whether to add data, the ways to regularize, and why random search beats grid."',
                  'data-blurb="Tell underfit from overfit with train and validation error, read learning curves, then constrain the model with L2, L1, early stopping, dropout or augmentation." data-reviewed="2"')
    open(PAGE, 'w').write(s)
    print('EH', [(i, round(a, 3), round(b, 3)) for i, a, b in EH][::6]); print('ok', E1, E3, E9, ES, LC9[2], LC1[2])
