# -*- coding: utf-8 -*-
"""Figures + body for content/08-deep-learning/03-optimizer/optimizer-overview.
One toy for every figure: eight rows (x1, x2, y) drawn with a fixed seed, a linear model y^ = w1 x1 + w2 x2 and
its mean squared error. Because x2 has a third of the spread of x1, the loss over (w1, w2) is a long thin valley.
Every optimiser runs here in pure Python from the same start (-1, -1.5) for the same twelve steps; every number
in a figure is computed below and pinned with assert. Run: python3 optimizer_overview.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, RULE, SUNK, BG,
                            tn, M, S, chip, dot, ball, poly, Plane, finish)
from tablefig import GR, AM, RD, tint, pill
from decision_tree import BODY as DT_BODY

PAGE = os.path.join(HERE, '../../../content/08-deep-learning/03-optimizer/optimizer-overview/index.html')

# ---------- data and loss ----------
_g = random.Random(7)
D = []
for _ in range(8):
    a = _g.uniform(-1, 1); b = _g.uniform(-1, 1) * .33
    D.append((round(a, 2), round(b, 2), round(1.5 * a + 2 * b + _g.gauss(0, .15), 2)))
assert D[0] == (-0.35, -0.23, -1.02) and D[7] == (0.72, -0.14, 0.79)

def grad(w, rows):
    g1 = g2 = 0
    for x1, x2, y in rows:
        r = w[0] * x1 + w[1] * x2 - y; g1 += 2 * r * x1; g2 += 2 * r * x2
    return g1 / len(rows), g2 / len(rows)
def loss(w): return sum((w[0] * a + w[1] * b - y) ** 2 for a, b, y in D) / len(D)

A = [[sum(r[i] * r[j] for r in D) / len(D) for j in range(2)] for i in range(2)]
bv = [sum(r[i] * r[2] for r in D) / len(D) for i in range(2)]
_det = A[0][0] * A[1][1] - A[0][1] ** 2
WSTAR = ((A[1][1] * bv[0] - A[0][1] * bv[1]) / _det, (A[0][0] * bv[1] - A[0][1] * bv[0]) / _det)
LMIN = loss(WSTAR)
_tr = A[0][0] + A[1][1]; _q = math.sqrt(_tr * _tr / 4 - _det)
LAM1, LAM2 = _tr / 2 + _q, _tr / 2 - _q
assert round(WSTAR[0], 2) == 1.41 and round(WSTAR[1], 2) == 2.19 and round(LAM1 / LAM2, 1) == 8.5
W0 = (-1.0, -1.5); N = 12
assert round(loss(W0), 2) == 2.68

def run(step, n=N):
    w = W0; st = {}; P = [w]; G = []
    for t in range(1, n + 1):
        g = grad(w, D); G.append(g); w = step(w, g, st, t); P.append(w)
    return P, G
def gd(lr): return lambda w, g, s, t: (w[0] - lr * g[0], w[1] - lr * g[1])
def gds(lrs): return lambda w, g, s, t: (w[0] - lrs[t - 1] * g[0], w[1] - lrs[t - 1] * g[1])
def mom(lr, b):
    def f(w, g, s, t):
        v = s.get('v', (0, 0)); v = (b * v[0] + g[0], b * v[1] + g[1]); s['v'] = v; s.setdefault('V', []).append(v)
        return (w[0] - lr * v[0], w[1] - lr * v[1])
    return f
def rms(lr, b=.9):
    def f(w, g, s, t):
        v = s.get('s', (0, 0)); v = tuple(b * v[i] + (1 - b) * g[i] ** 2 for i in range(2)); s['s'] = v
        s.setdefault('E', []).append(tuple(lr / math.sqrt(v[i]) for i in range(2)))
        return tuple(w[i] - lr * g[i] / (math.sqrt(v[i]) + 1e-8) for i in range(2))
    return f
def adam(lr, b1=.9, b2=.999):
    def f(w, g, s, t):
        m = s.get('m', (0, 0)); v = s.get('v', (0, 0))
        m = tuple(b1 * m[i] + (1 - b1) * g[i] for i in range(2)); v = tuple(b2 * v[i] + (1 - b2) * g[i] ** 2 for i in range(2))
        s['m'] = m; s['v'] = v
        return tuple(w[i] - lr * (m[i] / (1 - b1 ** t)) / (math.sqrt(v[i] / (1 - b2 ** t)) + 1e-8) for i in range(2))
    return f
def osc(P):   # how many times w1 reverses direction
    return sum(1 for i in range(1, len(P) - 1) if (P[i + 1][0] - P[i][0]) * (P[i][0] - P[i - 1][0]) < 0)

GD2, GG2 = run(gd(2))
assert round(loss(GD2[-1]), 4) == .0149
LR_CASES = [(.5, 'too small', VI), (2, 'about right', GR), (3.6, 'too large', RD)]
LR_RUNS = {lr: run(gd(lr))[0] for lr, _, _ in LR_CASES}
assert round(loss(LR_RUNS[.5][-1]), 4) == .1727 and round(loss(LR_RUNS[3.6][-1]), 1) == 10.6

# mini-batch: batch of 2 rows, same lr 2, seed 7
def sgd_run(seed=7, lr=2, bs=2):
    r = random.Random(seed); w = W0; P = [w]; Bs = []
    for _ in range(N):
        B = sorted(r.sample(range(len(D)), bs)); Bs.append(B)
        g = grad(w, [D[i] for i in B]); w = (w[0] - lr * g[0], w[1] - lr * g[1]); P.append(w)
    return P, Bs
SGD, SGB = sgd_run()
assert round(loss(SGD[-1]), 4) == .0127

# schedule: linear warmup 2 steps to a peak of 3.6, then cosine down to 0 at step 12
PEAK, WU = 3.6, 2
SCHED = [PEAK * t / WU if t <= WU else PEAK * .5 * (1 + math.cos(math.pi * (t - WU) / (N - WU))) for t in range(1, N + 1)]
SCH, _ = run(gds(SCHED))
assert round(loss(SCH[-1]), 4) == .0184 and SCHED[1] == 3.6 and SCHED[-1] < 1e-9

# momentum
MLR, MB = 1.5, .5
_ms = {}
def _mom_keep(w, g, s, t): return mom(MLR, MB)(w, g, _ms, t)
MOM, _ = run(_mom_keep); MV = _ms['V']
GD15, _ = run(gd(MLR))
assert round(loss(MOM[-1]), 4) == .0033
MOM_L, GD15_L = loss(MOM[-1]), loss(GD15[-1])
assert MOM_L < GD15_L / 5

# RMSProp
RLR = .3
_rs = {}
RMS, RG = run(lambda w, g, s, t: rms(RLR)(w, g, _rs, t)); RE = _rs['E']
assert round(loss(RMS[-1]), 4) == .0071
assert round(RE[0][0], 2) == .60 and round(RE[0][1], 2) == 2.28

# Adam
ALR = .25
ADAM, AG = run(adam(ALR))
assert round(loss(ADAM[-1]), 4) == .0379
g1 = AG[0][0]; m1 = .1 * g1; v1 = .001 * g1 * g1; mh = m1 / .1; vh = v1 / .001
STEP_C = ALR * mh / math.sqrt(vh); STEP_U = ALR * m1 / math.sqrt(v1)
assert round(g1, 2) == -1.59 and round(m1, 3) == -.159 and round(v1, 5) == .00251 and round(STEP_C, 2) == -.25
assert round(STEP_U, 2) == -.79 and round(ADAM[1][0] - W0[0], 2) == .25 and round(ADAM[1][1] - W0[1], 2) == .25

# AdamW: two weights, one with large noisy gradients, one with tiny; same decay lambda = 0.1, lr 0.01, 100 steps
def wd_run(mode, sig, w=1.0, lam=.1, lr=.01, n=100, b1=.9, b2=.999):
    m = v = 0; out = [w]
    for t in range(1, n + 1):
        g = sig * (1 if t % 2 else -1) + (lam * w if mode == 'l2' else 0)
        m = b1 * m + (1 - b1) * g; v = b2 * v + (1 - b2) * g * g
        u = (m / (1 - b1 ** t)) / (math.sqrt(v / (1 - b2 ** t)) + 1e-8)
        w = w - lr * u - (lr * lam * w if mode == 'w' else 0); out.append(w)
    return out
WD = {(md, s): wd_run(md, s) for md in ('l2', 'w') for s in (1, .01)}
assert round(WD['l2', 1][-1], 3) == .890 and round(WD['l2', .01][-1], 3) == .230
assert round(WD['w', 1][-1], 3) == .889 and round(WD['w', .01][-1], 3) == .889

# ---------- drawing helpers ----------
def f2(x): return ('%.2f' % x).replace('-', '−')
def f3(x): return ('%.3f' % x).replace('-', '−')
def f4(x): return ('%.4f' % x).replace('-', '−')

class Surf:
    """The loss valley seen from above: contour ellipses of L(w1, w2), clipped to a panel."""
    def __init__(self, pre, x, y, w, h, w1=(-1.6, 4.4), w2=(-2.2, 3.0)):
        self.pre, self.x, self.y, self.w, self.h = pre, x, y, w, h
        sx = w / (w1[1] - w1[0]); sy = h / (w2[1] - w2[0])
        self.P = Plane(x - w1[0] * sx, y + w2[1] * sy, sx, sy)
        self.b = (w1, w2)
    def inside(self, p, m=4):
        X, Y = self.P(*p); return self.x + m <= X <= self.x + self.w - m and self.y + m <= Y <= self.y + self.h - m
    def svg(self, levels=(.02, .07, .16, .32, .6, 1.0, 1.6, 2.4, 3.6, 5.2)):
        cid = self.pre + 'clip'
        s = R(self.x, self.y, self.w, self.h, SUNK, RULE, 6, 1)
        # eigenvectors of A
        a, b, d = A[0][0], A[0][1], A[1][1]
        e1 = (b, LAM1 - a); n1 = math.hypot(*e1); e1 = (e1[0] / n1, e1[1] / n1); e2 = (-e1[1], e1[0])
        g = ''
        for k, c in enumerate(levels):
            r1, r2 = math.sqrt(c / LAM1), math.sqrt(c / LAM2)
            pts = []
            for i in range(97):
                th = 2 * math.pi * i / 96
                u, v = r1 * math.cos(th), r2 * math.sin(th)
                pts.append(self.P(WSTAR[0] + u * e1[0] + v * e2[0], WSTAR[1] + u * e1[1] + v * e2[1]))
            runs, cur = [], []
            for p in pts:
                if self.x + 1 <= p[0] <= self.x + self.w - 1 and self.y + 1 <= p[1] <= self.y + self.h - 1: cur.append(p)
                else:
                    if len(cur) > 1: runs.append(cur)
                    cur = []
            if len(cur) > 1: runs.append(cur)
            for rr in runs: g += poly(rr, BR, 1.1).replace('/>', ' opacity="%.2f"/>' % (.55 - .035 * k))
        s += g
        X, Y = self.P(*WSTAR)
        s += L(X - 5, Y - 5, X + 5, Y + 5, GR, 2) + L(X - 5, Y + 5, X + 5, Y - 5, GR, 2)
        X, Y = self.P(*W0)
        s += '<circle cx="%.1f" cy="%.1f" r="4" fill="none" stroke="%s" stroke-width="1.5"/>' % (X, Y, MU)
        s += M(self.x + self.w / 2, self.y + self.h + 20, '{w}₁ →', MU)
        s += M(self.x - 10, self.y + self.h / 2, '{w}₂', MU, 'end')
        return s
    def legend(self, y):
        x = self.x
        return ('<circle cx="%.1f" cy="%.1f" r="4" fill="none" stroke="%s" stroke-width="1.5"/>' % (x + 4, y - 4, MU) +
                S(x + 13, y, 'start', MU) + L(x + 62, y - 9, x + 72, y + 1, GR, 2) + L(x + 62, y + 1, x + 72, y - 9, GR, 2) +
                S(x + 79, y, 'minimum', MU))

def walk(f, sf, path, c, t0, dt, r=7, trail=2.2, stop=None, d=.5):
    """ball glides along path one step per dt; the trail segment appears as the ball arrives.
    stop = last index to draw (for a run that leaves the panel)."""
    P = sf.P; n = len(path) - 1 if stop is None else stop
    b0 = P(*path[0]); pts = [(0, 0, 0)]
    for k in range(1, n + 1):
        a, b = P(*path[k - 1]), P(*path[k])
        tk = t0 + (k - 1) * dt
        f.show(L(a[0], a[1], b[0], b[1], c, trail) + dot(b[0], b[1], c, 2.6), tk + d * .6)
        pts.append((tk, b[0] - b0[0], b[1] - b0[1]))
    f.path(ball(b0[0], b0[1], c, r), pts, max(t0 - .5, .1), d=d)
    return t0 + (n - 1) * dt + d

def ghost(sf, path, c=FA, dash='4 3', stop=None):
    pts = [sf.P(*p) for p in (path if stop is None else path[:stop + 1])]
    return poly(pts, c, 1.4, dash) + ''.join(dot(x, y, c, 1.8) for x, y in pts[1:])

def tick(f, x, y, k, t, dt, last):
    f.show(R(x, y - 13, 66, 19, BG, 'none', 4) + T(x, y, 'step %d / %d' % (k, N), MU, 'start', 'sv-s', bold=True),
           t, hide=None if last else t + dt)

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('opt1-', 720, 0, 'The loss of a two-weight model drawn from above as contour lines: a long thin valley with the '
             'minimum marked by a green cross. A ball starts at w = (−1, −1.5). At each of twelve steps an arrow shows the '
             'step minus learning rate 2 times the gradient, the ball glides along it, and a row with the new w1, w2 and loss '
             'is added to the table on the right. The loss falls from 2.68 to 0.0149.',
             'READ THE GRADIENT · TAKE ONE STEP · REPEAT')
    sf = Surf('opt1-', 20, 34, 300, 260)
    f.static(sf.svg() + sf.legend(330))
    t = Table(400, 30, [('step', 46), ('w₁', 64), ('w₂', 64), ('loss', 74)], step=19, rh=17)
    f.static(t.head())
    def row(k, w, c=TX):
        y = t.ry(k)
        return (R(t.x, y, t.w, t.rh, BG, 'none') + T(t.cx(0), y + 13, str(k), MU, mono=True) +
                T(t.cx(1), y + 13, f2(w[0]), c, mono=True) + T(t.cx(2), y + 13, f2(w[1]), c, mono=True) +
                T(t.cx(3), y + 13, f4(loss(w)), c, mono=True, bold=True))
    f.static(row(0, W0))
    dt, t0 = .75, 1.0
    for k in range(1, N + 1):
        a, b = sf.P(*GD2[k - 1]), sf.P(*GD2[k])
        tk = t0 + (k - 1) * dt
        f.show(arrow(a[0], a[1], b[0], b[1], AM, 2, None, 8), tk - .35, hide=tk + .45, d=.2)
        f.show(row(k, GD2[k], FI if k == N else TX), tk + .45)
    walk(f, sf, GD2, VI, t0, dt)
    te = t0 + N * dt
    f.show(M(400, t.ry(N) + 34, '{w} ← {w} − {η} ∇{L}   ·   {η} = 2', TX, 'start'), .5)
    assert round(loss(GD2[-1]), 4) == .0149
    return finish(f, max(t.ry(N) + 46, 346))

# ---------- 2.1 Mini-batch ----------
def fig_minibatch():
    f = Anim('opt2-', 720, 0, 'The same valley. The dashed grey path is full-batch gradient descent, which averages the gradient '
             'over all eight rows. The violet ball uses only two rows per step: in the table on the right the two sampled rows '
             'light up, the gradient comes from them alone, and the ball takes a noisier step. After twelve steps both end '
             'near the minimum.', 'EACH STEP SEES 2 OF 8 ROWS · NOISY BUT CHEAP')
    sf = Surf('opt2-', 20, 34, 300, 260)
    f.static(sf.svg() + sf.legend(330))
    f.show(ghost(sf, GD2) + S(sf.x + 150, 330, '- - full batch', FA), .3)
    t = Table(420, 30, [('row', 40), ('x₁', 60), ('x₂', 60), ('y', 60)], step=26, rh=22)
    f.static(t.head())
    for i, r in enumerate(D):
        f.static(R(t.x, t.ry(i), t.w, t.rh, BG, RULE_HI, 3, 1) + T(t.cx(0), t.ry(i) + 15, str(i + 1), MU, mono=True) +
                 ''.join(T(t.cx(j + 1), t.ry(i) + 15, f2(r[j]), TX, mono=True) for j in range(3)))
    dt, t0 = .8, 1.2
    for k, B in enumerate(SGB):
        tk = t0 + k * dt - .45; last = k == N - 1
        for i in B:
            f.show(t.outline(i, c=VI, sw=2), tk, hide=None if last else tk + dt - .05, d=.15)
        f.show(R(t.x, t.ry(8) + 6, t.w, 22, BG, 'none') +
               T(t.x, t.ry(8) + 21, 'step %d · rows %d and %d' % (k + 1, B[0] + 1, B[1] + 1), VI, 'start', 'sv-s', bold=True),
               tk, hide=None if last else tk + dt - .05, d=.15)
    walk(f, sf, SGD, VI, t0, dt)
    te = t0 + N * dt
    f.show(S(t.x, t.ry(8) + 48, 'loss after 12 steps', MU) +
           T(t.x, t.ry(8) + 68, 'mini-batch %s · full batch %s' % (f4(loss(SGD[-1])), f4(loss(GD2[-1]))), TX, 'start', mono=True), te)
    return finish(f, max(t.ry(8) + 80, 346))

# ---------- 2.2 Learning rate ----------
def fig_lr():
    f = Anim('opt3-', 720, 0, 'Three copies of the valley, each with a ball starting at the same point and taking twelve plain '
             'gradient steps. Learning rate 0.5: small steps that are still far from the minimum. 2: reaches the valley floor. '
             '3.6: every step overshoots across the narrow valley further than the last, and the ball leaves the picture; the '
             'loss grows to 10.6.', 'SAME GRADIENT · THREE STEP SIZES')
    out = {}
    for k, (lr, lab, c) in enumerate(LR_CASES):
        sf = Surf('opt3%d-' % k, 14 + k * 242, 34, 210, 182, w1=(-3.2, 6.2))
        f.static(sf.svg(levels=(.02, .1, .32, .8, 1.6, 2.8, 4.4)))
        path = LR_RUNS[lr]
        stop = None
        for i, p in enumerate(path):
            if not sf.inside(p): stop = i - 1; break
        end = walk(f, sf, path, c, .8, .6, r=6, trail=1.8, stop=stop)
        y = sf.y + sf.h + 44
        f.show(T(sf.x + sf.w / 2, y, 'η = %g · %s' % (lr, lab), c, cls='sv-s', bold=True), .4)
        if stop is not None:
            a = sf.P(*path[stop]); b = sf.P(*path[stop + 1])
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            f.show(arrow(a[0], a[1], a[0] + 30 * math.cos(ang), a[1] + 30 * math.sin(ang), RD, 2, '4 3', 8), end)
            f.show(T(sf.x + sf.w / 2, y + 20, 'left at step %d · loss %.1f at 12' % (stop + 1, loss(path[-1])), RD, mono=True), end + .4)
            out['stop'] = stop
        else:
            f.show(T(sf.x + sf.w / 2, y + 20, 'loss after 12 = %s' % f4(loss(path[-1])), c, mono=True), end + .2)
    assert out['stop'] >= 2
    return finish(f, 34 + 182 + 72)

# ---------- 2.3 Schedule ----------
def fig_schedule():
    f = Anim('opt4-', 720, 0, 'Left: the valley. The red dashed path is a constant learning rate of 3.6, which diverged in the '
             'previous figure. Right: a schedule is drawn one point per step: the rate climbs linearly to 3.6 over two warmup '
             'steps, then follows a cosine down to 0 at step 12. Each time a point appears, the ball takes one step of that '
             'size and settles to loss 0.0184.', 'WARMUP TO THE PEAK · COSINE DOWN TO ZERO')
    sf = Surf('opt4-', 20, 34, 300, 260)
    f.static(sf.svg() + sf.legend(330))
    cp = LR_RUNS[3.6]; stop = next(i - 1 for i, p in enumerate(cp) if not sf.inside(p))
    f.show(ghost(sf, cp, RD, '4 3', stop) + S(sf.x + 150, 330, '- - constant 3.6', RD), .3)
    # schedule plot
    x0, x1, yb, yt = 400, 690, 250, 60
    PX = lambda k: x0 + (k - 0) / N * (x1 - x0); PY = lambda v: yb - v / 4 * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.2) + L(x0, yb, x0, yt - 6, RULE_HI, 1.2))
    for v in (1, 2, 3, 4): f.static(L(x0, PY(v), x1, PY(v), RULE, .8) + T(x0 - 7, PY(v) + 4, str(v), FA, 'end', mono=True))
    for k in (2, 4, 6, 8, 10, 12): f.static(T(PX(k), yb + 15, str(k), FA, mono=True))
    f.static(S(x1, yb + 32, 'step', MU, 'end') + M(x0, yt - 14, 'learning rate {η}', MU, 'start'))
    f.static(L(PX(WU), yb, PX(WU), yt, FA, 1, '3 3') + S(PX(WU) + 4, yt + 8, 'warmup ends', FA))
    dt, t0 = .8, 1.2
    prev = (PX(0), PY(0))
    for k, v in enumerate(SCHED, 1):
        tk = t0 + (k - 1) * dt - .4
        p = (PX(k), PY(v))
        f.show(L(prev[0], prev[1], p[0], p[1], AM, 2.2) + dot(p[0], p[1], AM, 4, BG), tk)
        f.show(R(x0 + 120, yb - 46, 150, 20, BG, 'none') +
               T(x0 + 270, yb - 32, 'step %d · η = %s' % (k, f2(v)), AM, 'end', mono=True, bold=True), tk,
               hide=None if k == N else tk + dt - .05, d=.15)
        prev = p
    walk(f, sf, SCH, VI, t0, dt)
    f.show(T(x0, yb + 58, 'loss after 12: scheduled %s · constant 3.6 → %.1f' % (f4(loss(SCH[-1])), loss(cp[-1])), TX, 'start', mono=True),
           t0 + N * dt)
    return finish(f, 346)

# ---------- 3.1 Momentum ----------
def side_eq(f, x, y, lines):
    for i, s in enumerate(lines): f.static(M(x, y + i * 22, s, TX, 'start'))

def fig_momentum():
    f = Anim('opt5-', 720, 0, 'The valley. Grey dashed: plain gradient descent with learning rate 1.5, creeping along the floor. '
             'Violet: momentum with the same rate and beta 0.5. At every step an amber arrow shows the velocity, the running sum '
             'of past gradients: across the valley the gradients flip sign and cancel, along it they add up, so the arrow grows '
             'along the floor and the ball reaches the minimum.', 'VELOCITY = PAST GRADIENTS ADDED UP · ACROSS-VALLEY PARTS CANCEL')
    sf = Surf('opt5-', 20, 34, 300, 260)
    f.static(sf.svg() + sf.legend(330))
    f.show(ghost(sf, GD15) + S(sf.x + 150, 330, '- - plain GD', FA), .3)
    X = 380
    side_eq(f, X, 56, ['{v} ← {β}{v} + ∇{L}', '{w} ← {w} − {η}{v}'])
    f.static(S(X, 110, 'η = 1.5 · β = 0.5', MU))
    dt, t0 = .8, 1.2
    sc = MLR
    for k in range(1, N + 1):
        tk = t0 + (k - 1) * dt
        a = sf.P(*MOM[k - 1]); v = MV[k - 1]
        b = sf.P(MOM[k - 1][0] - sc * v[0], MOM[k - 1][1] - sc * v[1])
        last = k == N
        f.show(arrow(a[0], a[1], b[0], b[1], AM, 2.4, None, 9), tk - .4, hide=tk + .5, d=.2)
        f.show(R(X, 136, 330, 46, BG, 'none') +
               T(X, 150, 'step %d' % k, MU, 'start', 'sv-s', bold=True) +
               T(X, 172, 'v = (%s, %s)' % (f2(v[0]), f2(v[1])), AM, 'start', mono=True, bold=True), tk - .4,
               hide=None if last else tk + dt - .4, d=.15)
    walk(f, sf, MOM, VI, t0, dt)
    te = t0 + N * dt
    f.show(S(X, 220, 'loss after 12 steps, same η', MU) +
           T(X, 242, 'plain GD  %s' % f4(GD15_L), FA, 'start', mono=True) +
           T(X, 262, 'momentum  %s' % f4(MOM_L), VI, 'start', mono=True, bold=True), te)
    return finish(f, 346)

# ---------- 3.2 RMSProp ----------
def fig_rmsprop():
    f = Anim('opt6-', 720, 0, 'The valley. Grey dashed: plain gradient descent, rate 2. Violet: RMSProp with rate 0.3. On the right '
             'two bars show the step size each weight actually gets, 0.3 divided by the root of its running squared gradient. '
             'w1 has steep gradients, so its bar stays short, about 0.6; w2 has gentle ones, so its bar is about 2.3 and grows: '
             'the ball heads straight down the valley instead of across it.', 'ONE STEP SIZE PER WEIGHT · SHRUNK WHERE THE GRADIENT IS BIG')
    sf = Surf('opt6-', 20, 34, 300, 260)
    f.static(sf.svg() + sf.legend(330))
    f.show(ghost(sf, GD2) + S(sf.x + 150, 330, '- - plain GD', FA), .3)
    X = 380
    side_eq(f, X, 56, ['{s} ← 0.9 {s} + 0.1 (∇{L})²', '{w} ← {w} − ({η} / √{s}) ∇{L}'])
    f.static(S(X, 110, 'η = 0.3 · effective step per weight:', MU))
    BX, BW = X + 40, 220; sc = BW / 3
    for j, yy in enumerate((140, 186)):
        f.static(M(X, yy + 13, '{w}%s' % '₁₂'[j], TX, 'start') + R(BX, yy, BW, 18, BG, RULE, 3, 1))
    for v in (1, 2, 3): f.static(L(BX + v * sc, 136, BX + v * sc, 208, RULE, .8, '2 3') + T(BX + v * sc, 224, str(v), FA, mono=True))
    dt, t0 = .8, 1.2
    for k in range(1, N + 1):
        tk = t0 + (k - 1) * dt - .4; last = k == N; e = RE[k - 1]
        s = ''
        for j, yy in enumerate((140, 186)):
            s += R(BX, yy, e[j] * sc, 18, tn(FI, '.30'), FI, 3, 1.2) + R(BX + BW + 6, yy, 40, 18, BG, 'none') + \
                 T(BX + BW + 8, yy + 13, f2(e[j]), FI, 'start', mono=True, bold=True)
        f.show(s, tk, hide=None if last else tk + dt, d=.2)
        f.show(R(X, 240, 120, 18, BG, 'none') + T(X, 254, 'step %d' % k, MU, 'start', 'sv-s', bold=True), tk,
               hide=None if last else tk + dt - .05, d=.15)
    walk(f, sf, RMS, VI, t0, dt)
    f.show(T(X, 286, 'loss after 12: RMSProp %s · GD %s' % (f4(loss(RMS[-1])), f4(loss(GD2[-1]))), TX, 'start', mono=True), t0 + N * dt)
    return finish(f, 346)

# ---------- 3.3 Adam ----------
def fig_adam():
    f = Anim('opt7-', 720, 0, 'The valley. Grey dashed: plain gradient descent, rate 2. On the right, the first Adam step for w1 '
             'is computed line by line: gradient −1.59, m = 0.1 times that = −0.159, v = 0.001 times its square = 0.00251. '
             'Both are tiny because they start at 0; dividing by 1 − 0.9 and 1 − 0.999 restores −1.59 and 2.51, so the step is '
             '0.25. Without the correction it would be 0.79. Then the violet ball runs twelve Adam steps.',
             'MOMENTUM (m) + RMSPROP (v) + BIAS CORRECTION')
    sf = Surf('opt7-', 20, 34, 300, 260)
    f.static(sf.svg() + sf.legend(330))
    f.show(ghost(sf, GD2) + S(sf.x + 150, 330, '- - plain GD', FA), .3)
    X = 372
    f.static(S(X, 50, 'step 1, weight w₁ · η = 0.25 · β₁ = 0.9 · β₂ = 0.999', MU))
    lines = [('{g} = ∂{L}/∂{w}₁', f3(g1), TX), ('{m} = 0.1 · {g}', f3(m1), AM), ('{v} = 0.001 · {g}²', '%.5f' % v1, FI),
             ('{m̂} = {m} / (1 − 0.9)', f3(mh), AM), ('{v̂} = {v} / (1 − 0.999)', '%.3f' % vh, FI),
             ('step = {η} · {m̂} / √{v̂}', f2(STEP_C), GR)]
    for i, (lhs, val, c) in enumerate(lines):
        y = 82 + i * 28; t = .6 + i * .7
        f.show(M(X, y, lhs, TX, 'start'), t)
        f.show(T(X + 300, y, '= ' + val, c, 'end', mono=True, bold=True), t + .3)
    f.show(T(X, 82 + 6 * 28 + 4, 'no correction: η · m / √v = %s' % f2(STEP_U), RD, 'start', mono=True), .6 + 6 * .7)
    t0 = .6 + 7 * .7 + .4
    walk(f, sf, ADAM, VI, t0, .7)
    f.show(T(X, 300, 'loss after 12: Adam %s · GD %s' % (f4(loss(ADAM[-1])), f4(loss(GD2[-1]))), TX, 'start', mono=True), t0 + N * .7)
    return finish(f, 346)

# ---------- 04 AdamW ----------
def fig_adamw():
    f = Anim('opt8-', 720, 0, 'Two weights both start at 1.0 and get the same weight decay 0.1 for 100 Adam steps. Weight a has large '
             'gradients, weight b tiny ones. Top: decay added to the gradient (L2 inside Adam). Adam divides it by each weight\'s '
             'gradient size, so a barely shrinks, to 0.890, while b collapses to 0.230. Bottom: AdamW subtracts the decay from '
             'the weight directly; a and b both shrink to 0.889.', 'SAME DECAY ON EVERY WEIGHT ONLY IF IT SKIPS THE ADAM DIVISION')
    BX, BW = 200, 420
    rows = [('l2', 'L2 inside Adam', 46), ('w', 'AdamW', 186)]
    marks = [0, 25, 50, 75, 100]
    for md, name, y0 in rows:
        f.static(T(0, y0 + 4, name, TX, 'start', 'sv-s', bold=True))
        for j, (sig, lab) in enumerate(((1, 'a · big gradients'), (.01, 'b · tiny gradients'))):
            yy = y0 + 20 + j * 40
            f.static(S(0, yy + 14, lab, MU) + R(BX, yy, BW, 20, BG, RULE, 3, 1))
            for v in (.25, .5, .75, 1):
                f.static(L(BX + v * BW, yy - 2, BX + v * BW, yy + 22, RULE, .8, '2 3'))
            path = WD[md, sig]
            for k, st in enumerate(marks):
                w = path[st]; t = .6 + k * 1.1; last = k == len(marks) - 1
                c = (RD if (md == 'l2' and sig == .01) else GR) if last else FI
                f.show(R(BX, yy, w * BW, 20, tn(FI, '.25') if not last else (tint('rd', '.25') if c == RD else tint('gr', '.25')), c, 3, 1.3) +
                       R(BX + BW + 6, yy, 60, 20, BG, 'none') + T(BX + BW + 10, yy + 14, f3(w), c, 'start', mono=True, bold=True),
                       t, hide=None if last else t + 1.1, d=.25)
    for v in (0, .5, 1): f.static(T(BX + v * BW, 290, '%g' % v, FA, mono=True))
    for k, st in enumerate(marks):
        t = .6 + k * 1.1
        f.show(R(BX, 38, 200, 18, BG, 'none') + T(BX, 52, 'after %d steps' % st, VI, 'start', 'sv-s', bold=True), t,
               hide=None if k == len(marks) - 1 else t + 1.1, d=.2)
    return finish(f, 300)

BODY = r'''<header class="hero">
  <p class="eyebrow">Deep learning · Optimizer</p>
  <h1>Optimizer <em>overview</em></h1>
  <p class="lede">An optimizer turns the gradient into a step; momentum remembers past steps, RMSProp gives each weight its own step size, and <b>Adam</b> does both.</p>
</header>

<section id="optim-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Every optimizer reads the gradient at the current weights and <em>turns it into one step</em>; they differ only in that rule.</p>
{o1}
  <ul class="why">
    <li>The toy for the whole lesson: eight rows, a model <span class="mth"><var>ŷ</var> = <var>w</var><sub>1</sub><var>x</var><sub>1</sub> + <var>w</var><sub>2</sub><var>x</var><sub>2</sub></span>, mean squared error. <var>x</var><sub>2</sub> has a third of the spread of <var>x</var><sub>1</sub>, so the loss is a long thin valley — the shape that makes optimizers differ.</li>
    <li>Where the gradient comes from is <a href="../../02-neural-network/backpropagation/index.html">Backpropagation</a>; this lesson only decides what to do with it.</li>
  </ul>
</section>

<section id="optim-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Gradient descent</h2></div>
  <p class="key">Step against the gradient: <em>which rows</em> it is computed on and <em>how far</em> to step are the two knobs.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>w</var><sub><var>t</var>+1</sub></span><em>new weights</em></span>
      <span class="op">=</span>
      <span class="t"><span><var>w</var><sub><var>t</var></sub></span><em>current weights</em></span>
      <span class="op">−</span>
      <span class="t p"><span><var>η</var></span><em>learning rate</em></span>
      <span class="t g"><span>∇<var>L</var><sub><var>B</var></sub>(<var>w</var><sub><var>t</var></sub>)</span><em>gradient on batch B</em></span>
    </div>
  </div>
  <div class="subsec" id="optim-s2-1">
    <h3 class="ssh"><b>2.1</b>Mini-batch SGD</h3>
    <p class="skey">Compute the gradient on a <em>small random batch</em> instead of all rows: each step is noisier but far cheaper.</p>
{o2}
    <ul class="why">
      <li>Full batch = every row per step; <b>SGD</b> strictly = one row; in practice "SGD" means a <b>mini-batch</b> of 32–4096 rows.</li>
      <li>The noise is not only a cost: it shakes the weights out of sharp, narrow dips, which tends to generalise better.</li>
    </ul>
  </div>
  <div class="subsec" id="optim-s2-2">
    <h3 class="ssh"><b>2.2</b>Learning rate</h3>
    <p class="skey">Too small crawls, too large <em>overshoots across the valley</em> further each step and diverges.</p>
{o3}
    <ul class="why">
      <li>The narrow direction sets the limit: plain GD diverges once <span class="mth"><var>η</var></span> passes 2 / (largest curvature), even while the long direction still crawls.</li>
      <li>A loss that jumps to <code>nan</code> in the first few hundred steps is almost always this — lower the rate or add warmup.</li>
    </ul>
  </div>
  <div class="subsec" id="optim-s2-3">
    <h3 class="ssh"><b>2.3</b>Learning-rate schedule</h3>
    <p class="skey">Change <span class="mth"><var>η</var></span> over time: <em>warm up</em> from small, then <em>decay</em> — a peak that diverges as a constant now converges.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>η</var><sub><var>t</var></sub></span><em>after warmup</em></span>
      <span class="op">=</span>
      <span class="t p"><span><var>η</var><sub>peak</sub></span><em>top rate</em></span>
      <span class="op">·</span>
      <span class="t g"><span>½ (1 + <b class="fn">cos</b>(π <span class="frac"><i><var>t</var> − <var>t</var><sub>w</sub></i><i><var>T</var> − <var>t</var><sub>w</sub></i></span>))</span><em>cosine from 1 down to 0</em></span>
    </div>
  </div>
{o4}
    <ul class="why">
      <li>Warmup protects the first steps, when the weights are random and Adam's statistics are still empty; then a large rate makes fast progress and the decay lets the weights settle.</li>
      <li>Linear warmup + cosine decay is the default for transformers; step decay (×0.1 at fixed epochs) is the older CNN recipe.</li>
    </ul>
  </div>
</section>

<section id="optim-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Momentum and adaptive steps</h2></div>
  <p class="key">Keep running averages of past gradients: <em>the average itself</em> smooths direction, <em>the average of squares</em> sets the size.</p>
  <div class="subsec" id="optim-s3-1">
    <h3 class="ssh"><b>3.1</b>Momentum</h3>
    <p class="skey">Step along a <em>velocity</em> that adds up past gradients: zig-zag parts cancel, the steady direction grows.</p>
{o5}
    <ul class="why">
      <li><span class="mth"><var>β</var></span> = 0.9 is the usual default; with <span class="mth"><var>β</var></span> = 0.5 here the velocity remembers about two steps.</li>
      <li>SGD + momentum (often <b>Nesterov</b>, which reads the gradient one step ahead) is still the standard for training CNNs on images.</li>
    </ul>
  </div>
  <div class="subsec" id="optim-s3-2">
    <h3 class="ssh"><b>3.2</b>RMSProp</h3>
    <p class="skey">Divide each weight's step by the <em>root of its recent squared gradients</em>: steep directions slow down, flat ones speed up.</p>
{o6}
    <ul class="why">
      <li><b>AdaGrad</b> came first and sums all past squares, so its steps only ever shrink; RMSProp replaces the sum with a decaying average.</li>
      <li>The ratio of the two bars is the valley's elongation, undone per weight — no single learning rate can do that.</li>
    </ul>
  </div>
  <div class="subsec" id="optim-s3-3">
    <h3 class="ssh"><b>3.3</b>Adam</h3>
    <p class="skey">Momentum's <span class="mth"><var>m</var></span> for direction, RMSProp's <span class="mth"><var>v</var></span> for size, and a <em>bias correction</em> because both start at zero.</p>
  <div class="eq">
    <div class="line">
      <span class="t p"><span><var>m</var> ← <var>β</var><sub>1</sub><var>m</var> + (1 − <var>β</var><sub>1</sub>) <var>g</var></span><em>average gradient</em></span>
      <span class="op">·</span>
      <span class="t g"><span><var>v</var> ← <var>β</var><sub>2</sub><var>v</var> + (1 − <var>β</var><sub>2</sub>) <var>g</var><sup>2</sup></span><em>average squared gradient</em></span>
    </div>
    <div class="line">
      <span class="t"><span><var>w</var> ← <var>w</var> − <var>η</var> <span class="frac"><i><var>m̂</var></i><i>√<var>v̂</var> + <var>ε</var></i></span></span><em>update</em></span>
      <span class="op">,</span>
      <span class="t r"><span><var>m̂</var> = <span class="frac"><i><var>m</var></i><i>1 − <var>β</var><sub>1</sub><sup><var>t</var></sup></i></span> , <var>v̂</var> = <span class="frac"><i><var>v</var></i><i>1 − <var>β</var><sub>2</sub><sup><var>t</var></sup></i></span></span><em>bias correction</em></span>
    </div>
  </div>
{o7}
    <ul class="why">
      <li>On step 1 the corrected ratio is just the sign of the gradient, so every weight moves by exactly <span class="mth"><var>η</var></span>: Adam's step size is set by <span class="mth"><var>η</var></span>, not by the gradient's scale.</li>
      <li>Defaults <span class="mth"><var>β</var><sub>1</sub></span> = 0.9, <span class="mth"><var>β</var><sub>2</sub></span> = 0.999, <span class="mth"><var>ε</var></span> = 10<sup>−8</sup>; it needs little tuning, which is why it is the default for transformers and most new models.</li>
    </ul>
  </div>
</section>

<section id="optim-s4" class="lesson">
  <div class="sh"><b>04</b><h2>AdamW</h2></div>
  <p class="key">Apply weight decay <em>to the weight directly</em>, outside Adam's division, so every weight decays at the same rate.</p>
  <div class="eq">
    <div class="line">
      <span class="t r"><span><var>g</var> ← ∇<var>L</var> + <var>λ</var><var>w</var></span><em>L2 inside Adam: decay gets divided by √v̂</em></span>
    </div>
    <div class="line">
      <span class="t g"><span><var>w</var> ← <var>w</var> − <var>η</var> <span class="frac"><i><var>m̂</var></i><i>√<var>v̂</var> + <var>ε</var></i></span> − <var>η</var><var>λ</var><var>w</var></span><em>AdamW: decay applied as is</em></span>
    </div>
  </div>
{o8}
  <ul class="why">
    <li>With plain SGD the two are identical; only an adaptive optimizer rescales the penalty. Why decay helps at all is in <a href="../../02-neural-network/dropout-regularization/index.html">Dropout &amp; regularization</a>.</li>
    <li>AdamW with <span class="mth"><var>λ</var></span> ≈ 0.01–0.1, warmup and cosine decay is the standard recipe for LLMs; biases and norm weights are usually excluded from decay.</li>
  </ul>
</section>

'''

def build():
    figs = dict(o1=fig_mental(), o2=fig_minibatch(), o3=fig_lr(), o4=fig_schedule(), o5=fig_momentum(),
                o6=fig_rmsprop(), o7=fig_adam(), o8=fig_adamw())
    body = re.sub(r'\{(o\d+)\}', lambda m: figs[m.group(1)], BODY)
    a = DT_BODY.index('<script>\n/* Figures start'); b = DT_BODY.index('</script>', a) + len('</script>')
    return (body + DT_BODY[a:b] + '\n\n<footer>Deep learning · Optimizer · next lesson in the branch: '
            '<a href="../sgd/index.html">SGD &amp; mini-batch</a>.</footer>\n')

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">'); b = s.index('</article>')
    s = s[:a] + body + '\n      ' + s[b:]
    m = re.search(r'<article [^>]*>', s); tag = m.group(0)
    tag = re.sub(r' data-(skeleton|reviewed|progress)="\d"', '', tag)
    tag = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s"' % blurb, tag).replace('>', ' data-progress="1">', 1) if False else \
        re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s" data-progress="1"' % blurb, tag)
    s = s[:m.start()] + tag + s[m.end():]
    open(page, 'w').write(s)

if __name__ == '__main__':
    splice(PAGE, build(), 'Twelve steps on one loss valley: mini-batch noise, learning rate and schedule, momentum, RMSProp, '
           'Adam with bias correction, and why AdamW decays weights outside the Adam division.')
