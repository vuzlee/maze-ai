# -*- coding: utf-8 -*-
"""Figures + page body for content/07-machine-learning/05-classical-ml/classical-models-overview.
Run: python3 classical_models_overview.py -> rewrites the lesson body. Pure Python: the six models are
fitted here on the same toy data, so every boundary and accuracy in the figures is computed, not drawn."""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from engine import Anim
from tablefig import T, R, L, arrow, MU, TX, FA, RULE_HI
from linear_algebra import M, S, chip, poly, BR, VI, FI, RO, GH, RULE, SUNK, BG, tn

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/05-classical-ml/classical-models-overview/index.html')
CLS = (BR, VI)          # class 0, class 1

# ---------------- data ----------------
def moons(n, seed, noise=.2):
    r = random.Random(seed); P = []
    for i in range(n):
        c = i % 2; t = r.uniform(0, math.pi)
        x, y = (math.cos(t), math.sin(t)) if c == 0 else (1 - math.cos(t), .5 - math.sin(t))
        P.append((x + r.gauss(0, noise), y + r.gauss(0, noise), c))
    return P
def blobs(n, seed):
    r = random.Random(seed)
    return [(r.gauss(-.6 if i % 2 == 0 else .6, .45), r.gauss(-.4 if i % 2 == 0 else .4, .45), i % 2) for i in range(n)]
def ring(n, seed):
    r = random.Random(seed); P = []
    for i in range(n):
        c = i % 2; a = r.uniform(0, 2 * math.pi); rad = r.gauss(.5, .15) if c == 0 else r.gauss(1.3, .15)
        P.append((rad * math.cos(a), rad * math.sin(a), c))
    return P

# ---------------- models (pure python) ----------------
def solve(A, b):
    n = len(b); A = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        p = max(range(i, n), key=lambda k: abs(A[k][i])); A[i], A[p] = A[p], A[i]
        for k in range(n):
            if k != i:
                f = A[k][i] / A[i][i]
                A[k] = [a - f * c for a, c in zip(A[k], A[i])]
    return [A[i][n] / A[i][i] for i in range(n)]
def feats(x, y): return [1.0, x, y]
def linreg(D, lam=0.0):
    X = [feats(x, y) for x, y, _ in D]; Y = [2 * c - 1 for *_, c in D]
    A = [[sum(r[i] * r[j] for r in X) + (lam if i == j and i > 0 else 0) for j in range(3)] for i in range(3)]
    w = solve(A, [sum(r[i] * t for r, t in zip(X, Y)) for i in range(3)])
    return lambda x, y: int(sum(a * b for a, b in zip(w, feats(x, y))) > 0)
def logreg(D, it=3000, lr=.5):
    w = [0.0] * 3
    for _ in range(it):
        g = [0.0] * 3
        for x, y, c in D:
            f = feats(x, y); p = 1 / (1 + math.exp(-sum(a * b for a, b in zip(w, f))))
            for i in range(3): g[i] += (p - c) * f[i] / len(D)
        w = [a - lr * b for a, b in zip(w, g)]
    return lambda x, y: int(sum(a * b for a, b in zip(w, feats(x, y))) > 0)
def knn(D, k=5):
    def f(x, y):
        nb = sorted(D, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)[:k]
        return int(sum(p[2] for p in nb) * 2 > k)
    return f
def gnb(D):
    st = {}
    for c in (0, 1):
        pts = [p for p in D if p[2] == c]; m = []
        for j in (0, 1):
            v = [p[j] for p in pts]; mu = sum(v) / len(v); m.append((mu, sum((a - mu) ** 2 for a in v) / len(v)))
        st[c] = (len(pts) / len(D), m)
    def lp(c, x, y):
        pr, m = st[c]
        return math.log(pr) + sum(-.5 * math.log(2 * math.pi * s) - (v - mu) ** 2 / (2 * s) for v, (mu, s) in zip((x, y), m))
    return lambda x, y: int(lp(1, x, y) > lp(0, x, y))
def ksvm(D, gamma=2.0, lam=.01, T=6000, seed=3):
    r = random.Random(seed); n = len(D); a = [0] * n
    K = lambda i, x, y: math.exp(-gamma * ((D[i][0] - x) ** 2 + (D[i][1] - y) ** 2))
    Y = [2 * c - 1 for *_, c in D]
    for t in range(1, T + 1):
        i = r.randrange(n); s = sum(a[j] * Y[j] * K(j, D[i][0], D[i][1]) for j in range(n) if a[j]) / (lam * t)
        if Y[i] * s < 1: a[i] += 1
    sv = [j for j in range(n) if a[j]]
    return lambda x, y: int(sum(a[j] * Y[j] * K(j, x, y) for j in sv) > 0)
def acc(f, D): return sum(f(x, y) == c for x, y, c in D) / len(D)

# ---------------- drawing ----------------
class Box:
    def __init__(s, x, y, w, h, x0, x1, y0, y1):
        s.x, s.y, s.w, s.h, s.x0, s.x1, s.y0, s.y1 = x, y, w, h, x0, x1, y0, y1
    def P(s, a, b): return (s.x + (a - s.x0) / (s.x1 - s.x0) * s.w, s.y + s.h - (b - s.y0) / (s.y1 - s.y0) * s.h)
    def frame(s): return R(s.x, s.y, s.w, s.h, BG, RULE_HI, 4, 1)
    def pts(s, D, r=2.6):
        return ''.join('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (*s.P(x, y), r, tn(CLS[c], '.55'), CLS[c]) for x, y, c in D)
    def region(s, f, n=44):
        """predicted class painted as run-length strips per grid row (class-1 side only, faint)."""
        o = ''; cw, ch = s.w / n, s.h / n
        G = [[f(s.x0 + (j + .5) / n * (s.x1 - s.x0), s.y1 - (i + .5) / n * (s.y1 - s.y0)) for j in range(n)] for i in range(n)]
        f = lambda xx, yy, _G=G: None
        for i in range(n):
            yv = s.y1 - (i + .5) / n * (s.y1 - s.y0); run = None
            for j in range(n + 1):
                v = G[i][j] if j < n else -1
                if run is None or v != run[1]:
                    if run is not None:
                        o += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (
                            s.x + run[0] * cw, s.y + i * ch, (j - run[0]) * cw + .3, ch + .3, tn(CLS[run[1]], '.20'))
                    run = (j, v)
        for i in range(n):
            for j in range(n):
                if j + 1 < n and G[i][j] != G[i][j + 1]:
                    o += L(s.x + (j + 1) * cw, s.y + i * ch, s.x + (j + 1) * cw, s.y + (i + 1) * ch, VI, 1.8)
                if i + 1 < n and G[i][j] != G[i + 1][j]:
                    o += L(s.x + j * cw, s.y + (i + 1) * ch, s.x + (j + 1) * cw, s.y + (i + 1) * ch, VI, 1.8)
        return o

def fig_mental():
    tr_b, te_b, tr_r, te_r = blobs(60, 1), blobs(400, 2), ring(60, 3), ring(400, 4)
    lb, lr_, kr = logreg(tr_b), logreg(tr_r), knn(tr_r)
    ab, ar, ak = acc(lb, te_b), acc(lr_, te_r), acc(kr, te_r)
    f = Anim('cm1-', 720, 0, 'Two datasets of 60 points. On the left the two classes are separated by a straight border: a linear '
             'model draws its straight boundary and scores %d%%. On the right one class forms a ring around the other: the same '
             'linear model still draws a straight boundary and scores %d%%; 5-nearest-neighbours bends around the ring and scores %d%%. '
             'Below each panel, test accuracy as the training set grows from 60 to 6,000 points: on the straight data both models '
             'end near the top; on the ring the linear model stays flat near 50%% while 5-NN climbs.'
             % (ab * 100, ar * 100, ak * 100), 'SAME MODEL, TWO DATA SHAPES · THE ASSUMPTION DECIDES')
    A = Box(0, 54, 300, 200, -2, 2, -1.8, 1.8); B = Box(380, 54, 300, 200, -1.9, 1.9, -1.8, 1.8)
    f.static(A.frame() + B.frame())
    f.static(S(0, 44, 'data A · straight border', MU) + S(380, 44, 'data B · ring', MU))
    f.show(A.pts(tr_b), .2); f.show(B.pts(tr_r), .5)
    f.show(A.region(lb), 1.4, d=.6)
    f.show(chip(150, 280, 'linear · %d%%' % round(ab * 100), FI, 130), 2.2)
    f.show(B.region(lr_), 3.2, d=.6)
    f.show(chip(470, 280, 'linear · %d%%' % round(ar * 100), RO, 130), 4.0)
    f.show(B.frame() + B.region(kr) + B.pts(tr_r), 5.2, d=.6)
    f.show(chip(610, 280, '5-NN · %d%%' % round(ak * 100), FI, 120), 6.0)
    # accuracy vs training size: same models, 60 -> 600 -> 6000 points (computed)
    NS = (60, 600, 6000); curves = {}
    for key, gen, seed, te in (('A', blobs, 11, te_b), ('B', ring, 21, te_r)):
        la, ka = [], []
        for k, n in enumerate(NS):
            tr = gen(n, seed + k)
            la.append(acc(logreg(tr, it=600), te)); ka.append(acc(knn(tr), te))
        curves[key] = (la, ka)
    assert curves['B'][0][-1] < .6 and curves['B'][1][-1] > .9, curves
    py0, ph = 352, 120
    for key, bx, t0 in (('A', 0, 7.0), ('B', 380, 8.4)):
        la, ka = curves[key]
        X = lambda k: bx + 46 + k * 95
        Y = lambda a: py0 + ph - (a - .4) / .6 * ph
        ax = (L(bx + 40, py0, bx + 40, py0 + ph, RULE_HI, 1) + L(bx + 40, py0 + ph, bx + 246, py0 + ph, RULE_HI, 1) +
              ''.join(L(bx + 40, Y(v), bx + 246, Y(v), RULE, .8, '2 3') + T(bx + 34, Y(v) + 4, '%d%%' % (v * 100), MU, 'end')
                      for v in (.4, .6, .8, 1.0)) +
              ''.join(T(X(k), py0 + ph + 16, '%s' % format(n, ','), MU) for k, n in enumerate(NS)) +
              T(bx + 143, py0 + ph + 32, 'training points', MU))
        f.static(S(bx, py0 - 14, 'test accuracy as data grows ×100', MU))
        f.static(ax)
        def line(vals, c):
            return (poly([(X(k), Y(v)) for k, v in enumerate(vals)], c, 2) +
                    ''.join('<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (X(k), Y(v), c) for k, v in enumerate(vals)))
        lc = FI if key == 'A' else RO
        f.show(line(la, lc) + T(bx + 254, Y(la[-1]) + 4, 'linear %d%%' % round(la[-1] * 100), lc, 'start', bold=True), t0)
        f.show(line(ka, VI) + T(bx + 254, Y(ka[-1]) + 4 + (12 if abs(Y(ka[-1]) - Y(la[-1])) < 14 and ka[-1] < la[-1] else (-12 if abs(Y(ka[-1]) - Y(la[-1])) < 14 else 0)),
               '5-NN %d%%' % round(ka[-1] * 100), VI, 'start', bold=True), t0 + .7)
    f.show(S(380, py0 + ph + 56, 'linear stays flat: data cannot bend a line', MU), 9.6)
    f.show(S(0, py0 + ph + 56, 'assumption fits: 60 points reach the top', MU), 8.0)
    f.h = py0 + ph + 70
    return f.render(), (ab, ar, ak, curves)

MODELS = [('Linear regression', 'straight line', lambda D: linreg(D)),
          ('Logistic regression', 'straight line', lambda D: logreg(D)),
          ('Ridge / Lasso', 'straight line, small w', lambda D: linreg(D, 40.0)),
          ('Kernel SVM', 'widest band, bent by kernel', lambda D: ksvm(D)),
          ('KNN (k = 5)', 'neighbours vote', lambda D: knn(D)),
          ('Naive Bayes', 'one bell per class', lambda D: gnb(D))]

def fig_lookup():
    tr, te = moons(120, 7), moons(600, 8)
    fs = [(n, a, m(tr)) for n, a, m in MODELS]
    scores = [acc(g, te) for *_, g in fs]
    f = Anim('cm2-', 720, 0, 'The same two-moons dataset in six panels. Panel by panel each model paints the region it would '
             'label as the second class: linear regression, logistic regression and ridge draw straight cuts; kernel SVM and '
             'KNN bend around the moons; Gaussian naive Bayes may curve but here stays almost straight. Test accuracy under each: ' +
             ', '.join('%s %d%%' % (n, round(s * 100)) for (n, _, _), s in zip(fs, scores)) + '.',
             'SIX MODELS, ONE DATASET · THE SHAPE OF THE BOUNDARY IS THE ASSUMPTION')
    W, H, GX, GY = 220, 140, 30, 96
    for k, ((name, ass, g), sc) in enumerate(zip(fs, scores)):
        col, row = k % 3, k // 3
        bx, by = col * (W + GX), 52 + row * (H + GY)
        b = Box(bx, by, W, H, -1.6, 2.6, -1.2, 1.7)
        f.static(b.frame() + T(bx, by - 10, name, TX, 'start', 'sv-t'))
        f.show(b.pts(tr, 2.2), .2 + k * .08)
        t0 = 1.0 + k * 1.3
        f.show(R(bx - 3, by - 3, W + 6, H + 6, 'none', VI, 6, 2), t0, hide=t0 + 1.2)
        f.show(b.region(g), t0 + .2, d=.5)
        good = sc >= .9
        f.show(S(bx, by + H + 20, ass, MU) + chip(bx + W - 34, by + H + 15, '%d%%' % round(sc * 100), FI if good else BR, 54), t0 + .7)
    f.show(S(0, 52 + 2 * (H + GY) - 10, 'only kernel SVM and KNN bend around the moons · % = test accuracy on 600 new points', MU), 1.0 + 6 * 1.3)
    f.h = 52 + 2 * (H + GY) + 2
    return f.render(), scores

# small glyphs for the learning-order chain
def glyph(kind, cx, cy, c):
    if kind == 'line':
        pts = [(-18, 8), (-8, 2), (0, 4), (9, -5), (17, -9)]
        return ''.join('<circle cx="%.1f" cy="%.1f" r="2.2" fill="%s"/>' % (cx + a, cy + b, c) for a, b in pts) + L(cx - 22, cy + 10, cx + 22, cy - 11, c, 1.6)
    if kind == 'sig':
        return poly([(cx + x, cy - 12 * math.tanh(x / 6)) for x in range(-22, 23, 2)], c, 1.8)
    if kind == 'pen':
        return ('<circle cx="%d" cy="%d" r="11" fill="none" stroke="%s" stroke-width="1.6"/>' % (cx - 13, cy, c) +
                poly([(cx + 13, cy - 11), (cx + 24, cy), (cx + 13, cy + 11), (cx + 2, cy), (cx + 13, cy - 11)], c, 1.6))
    if kind == 'svm':
        return (L(cx - 20, cy + 12, cx + 4, cy - 12, c, 1.8) + L(cx - 12, cy + 16, cx + 12, cy - 8, c, 1, '3 2') + L(cx - 28, cy + 8, cx - 4, cy - 16, c, 1, '3 2'))
    if kind == 'knn':
        return ('<circle cx="%d" cy="%d" r="14" fill="none" stroke="%s" stroke-width="1.2" stroke-dasharray="3 2"/>' % (cx, cy, c) +
                ''.join('<circle cx="%.1f" cy="%.1f" r="2.4" fill="%s"/>' % (cx + a, cy + b, c) for a, b in [(-7, -5), (6, -7), (8, 5), (-5, 8), (0, 0)]))
    if kind == 'nb':
        return (poly([(cx - 22 + x, cy + 10 - 20 * math.exp(-((x - 12) / 6) ** 2)) for x in range(0, 45, 2)], c, 1.6) +
                poly([(cx - 22 + x, cy + 10 - 14 * math.exp(-((x - 30) / 7) ** 2)) for x in range(0, 45, 2)], c, 1.2, '3 2'))

def fig_order():
    f = Anim('cm3-', 720, 0, 'The learning order as a chain. Linear regression comes first, then logistic regression, both required. '
             'From there three branches open: ridge and lasso then SVM, KNN, and naive Bayes, in any order. Each box carries what '
             'it teaches.', 'LEARNING ORDER · TWO REQUIRED STEPS, THEN THREE FREE BRANCHES')
    BW, BH = 156, 108
    nodes = {'lin': (0, 150, 'Linear regression', ('loss, gradient descent,', 'coefficients first appear'), 'line'),
             'log': (190, 150, 'Logistic regression', ('same line, new wrapper', 'and loss → classifier'), 'sig'),
             'rid': (390, 32, 'Ridge / Lasso', ('penalize weight size —', 'reused in SVM, boosting, NN'), 'pen'),
             'svm': (570, 32, 'SVM', ('after Ridge: max margin', 'is L2 in geometry'), 'svm'),
             'knn': (390, 170, 'KNN', ('high variance, curse', 'of dimensionality'), 'knn'),
             'nb':  (390, 308, 'Naive Bayes', ('Bayes → classifier with no', 'optimization; text baseline'), 'nb')}
    def box(k, c, t):
        x, y, name, sub, g = nodes[k]
        return (R(x, y, BW, BH, BG, 'none', 8) + R(x, y, BW, BH, tn(c, '.08'), c, 8, 1.5) + glyph(g, x + BW / 2, y + 28, c) +
                T(x + BW / 2, y + 64, name, c, bold=True) + T(x + BW / 2, y + 81, sub[0], MU) + T(x + BW / 2, y + 95, sub[1], MU))
    def edge(a, b, t):
        xa, ya = nodes[a][0] + BW, nodes[a][1] + BH / 2; xb, yb = nodes[b][0], nodes[b][1] + BH / 2
        if ya == yb: return arrow(xa + 4, ya, xb - 4, yb, MU, 1.4)
        mx = (xa + xb) / 2
        return poly([(xa + 4, ya), (mx, ya), (mx, yb), (xb - 8, yb)], MU, 1.4) + arrow(xb - 12, yb, xb - 4, yb, MU, 1.4)
    f.show(box('lin', BR, 0), .3)
    f.show(edge('lin', 'log', 0), 1.0); f.show(box('log', BR, 0), 1.3)
    f.show(T(173, 138, 'required, in this order', VI, bold=True) + L(0, 128, 346, 128, VI, 1.4, '4 3'), 1.8)
    t = 2.6
    for k in ('rid', 'knn', 'nb'):
        f.show(edge('log', k, 0), t); f.show(box(k, FI, 0), t + .3); t += .7
    f.show(edge('rid', 'svm', 0), t + .2); f.show(box('svm', FI, 0), t + .5)
    f.show(S(570, 200, 'the three branches:', MU) + S(570, 218, 'any order', MU), t + 1.1)
    f.h = 430
    return f.render()

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · opening the Classical models group</p>
  <h1>Classical models — <em>lookup table</em></h1>
  <p class="lede">None of these six models <b>was created to fix another</b>. They are six different <em>assumptions</em> about the shape of the data — choosing a model means choosing an assumption.</p>
</header>

<section id="clsov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Every model takes the same table and returns the same kind of prediction; <em>they differ only in the family of shapes <span class="mth"><var>f</var></span> is allowed to take.</em></p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>f̂</var></span><em>the fitted model</em></span>
      <span class="op">=</span>
      <span class="t"><span><b class="fn">argmin</b><sub><var>f</var> ∈ <var>𝓕</var></sub></span><em>search only inside 𝓕</em></span>
      <span class="t b"><span>Σ<sub><var>i</var></sub> <var>L</var>(<var>y</var><sub><var>i</var></sub>, <var>f</var>(<var>x</var><sub><var>i</var></sub>))</span><em>loss on the training rows</em></span>
    </div>
    <dl>
      <dt>𝓕</dt><dd>the assumption: straight lines, neighbour votes, bells per class…</dd>
      <dt>L</dt><dd>squared error, log loss, hinge loss — each model's own</dd>
    </dl>
  </div>
{cm1}
  <ul class="why">
    <li>So read the lookup table by the <b>Believes that…</b> column first: which assumption does your data look like?</li>
    <li>The plots below the panels: on the ring, 100× more data leaves the linear model flat near 50% while 5-NN climbs past 99% — <b>change the model, not the data size</b>.</li>
    <li>A loose assumption (KNN) bends anywhere but pays in variance and needs more data as dimensions grow — <a href="../../04-core-concepts/bias-variance-tradeoff/index.html">bias–variance</a> seen from model choice.</li>
  </ul>
</section>

<section id="clsov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Lookup table</h2></div>
  <p class="key">Fit all six on the same data and the assumption becomes visible: <em>only two of them can bend around curved classes.</em></p>
{cm2}
  <table>
    <tr><th>Model</th><th>Believes that…</th><th>Cost</th><th>Pick when</th></tr>
    <tr><td><b><a href="../linear-regression/index.html">Linear regression</a></b></td><td>the label is a weighted sum of features</td><td>cheap, closed form</td><td>numeric label, you need to <b>explain each coefficient</b></td></tr>
    <tr><td><b><a href="../logistic-regression/index.html">Logistic regression</a></b></td><td>the log-odds are a weighted sum of features</td><td>cheap</td><td>classification with <b>trustworthy probabilities</b> — the default baseline</td></tr>
    <tr><td><b><a href="../ridge-lasso-elasticnet/index.html">Ridge / Lasso</a></b></td><td>as above, and the weights should be small</td><td>cheap</td><td>many features, multicollinearity, <b>automatic feature selection</b></td></tr>
    <tr><td><b><a href="../svm/index.html">SVM</a></b></td><td>classes are split by a wide band — a kernel lets it <em>bend</em></td><td>O(n²)–O(n³), <b>slow on large data</b></td><td><b>few samples, many dimensions</b> — text, biology</td></tr>
    <tr><td><b><a href="../knn/index.html">KNN</a></b></td><td>nearby points share a label</td><td>free to train, <b>slow to predict</b></td><td>few dimensions, distance has a clear meaning</td></tr>
    <tr><td><b><a href="../naive-bayes/index.html">Naive Bayes</a></b></td><td>features are independent given the class</td><td>cheapest — counting</td><td>text, <b>very sparse</b> data, very few samples</td></tr>
  </table>
  <ul class="why">
    <li>All six <b>need scaled features</b> (Naive Bayes the least) — the group's most common silent bug; see <a href="../../04-core-concepts/feature-engineering/index.html">Feature engineering</a>.</li>
    <li>On large tabular data all six usually lose to <a href="../../06-tree-models/tree-family-overview/index.html">tree ensembles</a>; they stay as baselines and as the place the core ideas first appear.</li>
  </ul>
</section>

<section id="clsov-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Learning order</h2></div>
  <p class="key">The first two lessons are <em>required, in order</em>; the other four open from there.</p>
{cm3}
  <ul class="why">
    <li>Start: <a href="../linear-regression/index.html">Linear regression</a>. Prerequisites: <a href="../../02-math-foundations/calculus/index.html">calculus</a> and <a href="../../04-core-concepts/bias-variance-tradeoff/index.html">bias–variance</a>.</li>
  </ul>
</section>

'''

if __name__ == '__main__':
    m1, a = fig_mental(); m2, sc = fig_lookup(); m3 = fig_order()
    print('mental', a, 'lookup', [round(s, 3) for s in sc])
    body = BODY.replace('{cm1}', m1).replace('{cm2}', m2).replace('{cm3}', m3)
    s = open(PAGE).read()
    i = s.index('<header class="hero">'); j = s.index('<footer>')
    rep = open(os.path.join(HERE, '../../../content/01-dsa/04-algorithms/binary-search/index.html')).read()
    scr = rep[rep.index('<script>\n/* Figures start'):]; scr = scr[:scr.index('</script>') + 9] + '\n\n'
    s = s[:i] + body + scr + s[j:]
    s = re.sub(r'data-blurb="[^"]*"( data-reviewed="\d")?', 'data-blurb="Six classical models fitted on the same data: only kernel SVM and KNN bend around curved classes — the shape they assume decides when to pick which." data-reviewed="2"', s, count=1)
    open(PAGE, 'w').write(s)
