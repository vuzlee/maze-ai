# -*- coding: utf-8 -*-
"""Figures + body for content/08-deep-learning/02-neural-network/normalization.
Every number is computed here: one 4x4 activation tensor for BatchNorm / LayerNorm, seeded Gaussian batches for
running statistics and batch-size noise, and a seeded pure-Python 8-layer ReLU MLP for the per-layer diagnosis.
Run: python3 normalization.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, BR, VI, FI, RO, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, finish, mcell)
from tablefig import GR, AM, RD, tint, Table

PAGE = os.path.join(HERE, '../../../content/08-deep-learning/02-neural-network/normalization/index.html')
HL = 'var(--brand-hi)'
EPS = 1e-5

# ---------- the activation tensor: 4 rows x 4 features ----------
A = [[1, 10, 2, 40], [3, 14, 2, 60], [5, 12, 6, 20], [7, 16, 6, 80]]
def stats(v):
    m = sum(v) / len(v); return m, math.sqrt(sum((a - m) ** 2 for a in v) / len(v))
def norm(v):
    m, s = stats(v); return [(a - m) / math.sqrt(s * s + EPS) for a in v]
COLS = [[r[j] for r in A] for j in range(4)]
BN = [norm(c) for c in COLS]                 # BN[j][i]
LN = [norm(r) for r in A]                    # LN[i][j]
CST = [stats(c) for c in COLS]; RST = [stats(r) for r in A]
assert [round(m, 2) for m, _ in CST] == [4, 13, 4, 50] and [round(s, 2) for _, s in CST] == [2.24, 2.24, 2, 22.36]
assert [round(m, 2) for m, _ in RST] == [13.25, 19.75, 10.75, 27.25]
assert [round(x, 2) for x in BN[0]] == [-1.34, -0.45, 0.45, 1.34] and [round(x, 2) for x in LN[0]] == [-0.77, -0.21, -0.71, 1.69]
for v in BN + LN:
    m, s = stats(v); assert abs(m) < 1e-9 and abs(s - 1) < 1e-5
GAM, BET = 2, 1
Y1 = [GAM * x + BET for x in BN[0]]
assert [round(y, 2) for y in Y1] == [-1.68, 0.11, 1.89, 3.68]

def f2(x):
    s = '%.2f' % x
    s = s.rstrip('0').rstrip('.') if '.' in s else s
    return s.replace('-', '−')

# ---------- running statistics: one feature, true mean 5, std 2, batches of 4 ----------
g = random.Random(5)
STEPS, MOM = 30, .1
rm, rv, RUN, BMEAN = 0.0, 1.0, [], []
for _ in range(STEPS):
    b = [g.gauss(5, 2) for _ in range(4)]
    m = sum(b) / 4; v = sum((a - m) ** 2 for a in b) / 3
    rm = (1 - MOM) * rm + MOM * m; rv = (1 - MOM) * rv + MOM * v
    BMEAN.append(m); RUN.append(rm)
XQ = 7.0
XHAT = (XQ - rm) / math.sqrt(rv + EPS)
assert round(RUN[-1], 2) == round(rm, 2) and 4.4 < rm < 5.2, rm

# ---------- batch-size noise: 12 batch means of N(0,1) samples ----------
g = random.Random(3)
NOISE = {}
for B in (2, 32):
    ms = [sum(g.gauss(0, 1) for _ in range(B)) / B for _ in range(12)]
    NOISE[B] = (ms, stats(ms)[1])
assert round(NOISE[2][1], 2) == .67 and round(NOISE[32][1], 2) == .15
assert all(-1.6 < m < 1.6 for B in NOISE for m in NOISE[B][0])

# ---------- diagnosis: 8-layer ReLU MLP, weights N(0, 1/n), with and without LayerNorm ----------
def run(use_ln, seed=7, n=32, layers=8, batch=64):
    g = random.Random(seed)
    X = [[g.gauss(0, 1) for _ in range(n)] for _ in range(batch)]
    out = []
    for _ in range(layers):
        W = [[g.gauss(0, 1 / math.sqrt(n)) for _ in range(n)] for _ in range(n)]
        Z = [[sum(x[i] * W[i][j] for i in range(n)) for j in range(n)] for x in X]
        if use_ln: Z = [norm(z) for z in Z]
        X = [[max(0, a) for a in z] for z in Z]
        out.append(stats([a for r in X for a in r])[1])
    return out
PLAIN, WITHLN = run(False), run(True)
assert round(PLAIN[0], 2) == .60 and PLAIN[-1] < .04 and all(a > b for a, b in zip(PLAIN, PLAIN[1:]))
assert all(.55 < s < .62 for s in WITHLN)

# ---------- helpers ----------
def glide(f, svg, pts, t0, d=.6):
    """f.path, but the item finishes fading in at its start point before it moves (engine merges equal times)."""
    return f.path(svg, pts, min(t0, pts[1][0] - .35), d=d)
CW, CH = 52, 30
def grid_cells(x0, y0, vals, fmt=str, tone=None):
    s = ''
    for i, row in enumerate(vals):
        for j, v in enumerate(row):
            s += cell(x0 + j * CW, y0 + i * CH, fmt(v), tone)
    return s
def cell(x, y, v, tone=None):
    if tone: return R(x + 1, y + 1, CW - 2, CH - 2, BG, 'none', 4) + R(x + 1, y + 1, CW - 2, CH - 2, tn(tone, '.12'), tone, 4, 1.3) + \
        T(x + CW / 2, y + CH / 2 + 4.5, v, tone, mono=True, bold=True)
    return R(x + 1, y + 1, CW - 2, CH - 2, BG, RULE_HI, 4, 1) + T(x + CW / 2, y + CH / 2 + 4.5, v, TX, mono=True)
def gchip(cx, cy, s, c, w=None):
    w = w or 14 + len(s) * 6.6
    return (R(cx - w / 2, cy - 10, w, 20, BG, 'none', 10) + R(cx - w / 2, cy - 10, w, 20, tint(c, '.16'), {'am': AM, 'gr': GR, 'rd': RD, 'bl': FI}[c], 10, 1.2) +
            T(cx, cy + 4, s, {'am': AM, 'gr': GR, 'rd': RD, 'bl': FI}[c], mono=True, bold=True))

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('nm1-', 720, 0, 'Four activations of one feature, 1, 3, 5 and 7, sit on a number line. Their mean 4 is marked and '
             'their standard deviation 2.24 is drawn as a bracket. The four points slide down to a second line where they '
             'become minus 1.34, minus 0.45, 0.45 and 1.34: mean 0, spread 1. They slide once more to a third line through '
             'y = 2 x-hat + 1, landing at minus 1.68, 0.11, 1.89 and 3.68.',
             'MEASURE THE GROUP · SHIFT AND SQUEEZE TO 0 / 1 · LET γ, β SET A NEW SCALE')
    X0, X1 = 170, 650
    lines = [(78, 0, 8, 'x', 'raw activations'), (178, -2, 2, 'x̂', '(x − μ) / σ'), (278, -3, 5, 'y', 'γ x̂ + β')]
    def px(k, v):
        _, a, b, _, _ = lines[k]; return X0 + (v - a) / (b - a) * (X1 - X0)
    for k, (y, a, b, nm, sub) in enumerate(lines):
        f.static(L(X0 - 10, y, X1 + 10, y, RULE_HI, 1.3) + M(0, y + 5, '{%s}' % nm, TX, 'start') + S(28, y + 5, sub, MU))
        for v in range(a, b + 1):
            f.static(L(px(k, v), y - 4, px(k, v), y + 4, RULE_HI, 1) + T(px(k, v), y + 18, f2(v), FA, mono=True))
    vals = COLS[0]; mu, sd = CST[0]
    for i, v in enumerate(vals):
        f.static(dot(px(0, v), 78, FI, 6) + T(px(0, v), 64, str(v), FI, mono=True, bold=True))
    f.show(L(px(0, mu), 44, px(0, mu), 92, AM, 1.6, '4 3') + gchip(px(0, mu), 36, 'μ = 4', 'am', 64), .6)
    f.show(L(px(0, mu - sd), 104, px(0, mu + sd), 104, AM, 1.8) + L(px(0, mu - sd), 99, px(0, mu - sd), 109, AM, 1.8) +
           L(px(0, mu + sd), 99, px(0, mu + sd), 109, AM, 1.8) + T(px(0, mu + sd) + 8, 108, 'σ = %s' % f2(sd), AM, 'start', mono=True, bold=True), 1.4)
    for i, v in enumerate(vals):
        xh = BN[0][i]
        glide(f, dot(px(1, xh), 178, FI, 6), [(0, px(0, v) - px(1, xh), -100), (2.4 + i * .15, 0, 0)], 2.4 + i * .15, d=.8)
        f.show(T(px(1, xh), 164, f2(xh), FI, mono=True, bold=True), 3.4)
    f.show(gchip(px(1, 0), 136, 'mean 0 · std 1', 'gr', 120), 3.6)
    for i, y in enumerate(Y1):
        xh = BN[0][i]
        glide(f, dot(px(2, y), 278, VI, 6), [(0, px(1, xh) - px(2, y), -100), (4.6 + i * .15, 0, 0)], 4.6 + i * .15, d=.8)
        f.show(T(px(2, y), 264, f2(y), VI, mono=True, bold=True), 5.6)
    f.show(gchip(X0 + 40, 236, 'γ = 2 · β = 1', 'bl', 112), 4.3)
    return finish(f, 306)

# ---------- 02 BatchNorm / LayerNorm: same tensor, different axis ----------
def fig_axis(kind):
    bn = kind == 'bn'
    pre = 'nm2-' if bn else 'nm3-'
    aria = ('The 4 by 4 activation tensor, rows are samples in the batch, columns are features. Each column in turn is '
            'outlined; its mean and standard deviation are written under it, and its four normalised values slide into '
            'the output grid. Every output column ends with mean 0 and std 1.') if bn else \
           ('The same 4 by 4 tensor, rows are now tokens, columns are features. Each row in turn is outlined; its mean and '
            'standard deviation are written beside it, and its four normalised values slide into the output grid. Every '
            'output row ends with mean 0 and std 1.')
    f = Anim(pre, 720, 0, aria, 'STATISTICS DOWN EACH COLUMN · ACROSS THE BATCH' if bn else 'STATISTICS ALONG EACH ROW · INSIDE ONE TOKEN')
    xa, xb, y0 = 80, 440, 62
    f.static(T(xa + 2 * CW, 40, 'input x', MU) + T(xb + 2 * CW, 40, 'output x̂', MU))
    for j in range(4):
        f.static(M(xa + j * CW + CW / 2, y0 - 6, '{f}%s' % '₁₂₃₄'[j], FA) + M(xb + j * CW + CW / 2, y0 - 6, '{f}%s' % '₁₂₃₄'[j], FA))
    for i in range(4):
        f.static(T(xa - 8, y0 + i * CH + 19, ('sample %d' if bn else 'token %d') % (i + 1), MU, 'end'))
    f.static(grid_cells(xa, y0, A))
    f.static(L(xb - 1, y0, xb - 1, y0 + 4 * CH, RULE, 1))
    for k in range(4):
        t = .5 + k * 1.9
        if bn:
            f.show(R(xa + k * CW - 1, y0 - 2, CW + 2, 4 * CH + 4, 'none', HL, 5, 2), t, hide=t + 1.7)
            m, s = CST[k]; cx = xa + k * CW + CW / 2
            f.show(gchip(cx, y0 + 4 * CH + 18, 'μ ' + f2(m), 'am', CW - 4), t + .3)
            f.show(gchip(cx, y0 + 4 * CH + 42, 'σ ' + f2(s), 'am', CW - 4), t + .6)
            for i in range(4):
                glide(f, cell(xb + k * CW, y0 + i * CH, f2(BN[k][i]), FI), [(0, xa - xb, 0), (t + .9 + i * .08, 0, 0)], t + .9, d=.7)
            ox = xb + k * CW + CW / 2
            f.show(gchip(ox, y0 + 4 * CH + 18, 'μ 0', 'gr', CW - 4) + gchip(ox, y0 + 4 * CH + 42, 'σ 1', 'gr', CW - 4), t + 1.6)
        else:
            f.show(R(xa - 2, y0 + k * CH - 1, 4 * CW + 4, CH + 2, 'none', HL, 5, 2), t, hide=t + 1.7)
            m, s = RST[k]; cy = y0 + k * CH + CH / 2
            f.show(gchip(xa + 4 * CW + 76, cy, 'μ %s · σ %s' % (f2(m), f2(s)), 'am', 132), t + .3)
            for j in range(4):
                glide(f, cell(xb + j * CW, y0 + k * CH, f2(LN[k][j]), FI), [(0, xa - xb, 0), (t + .9 + j * .08, 0, 0)], t + .9, d=.7)
            f.show(gchip(xb + 4 * CW + 30, cy, '0 · 1', 'gr', 48), t + 1.6)
    yb = y0 + 4 * CH + (62 if bn else 24)
    f.show(S(xb, yb + 10, 'f₄ was 20–80, f₁ was 1–7 · now the same scale' if bn else 'each token rescaled on its own · no other row used', GR, 'start', True), 8.2)
    return finish(f, yb + 24)

# ---------- 3.1 Train vs inference ----------
def fig_running():
    f = Anim('nm4-', 720, 0, 'One feature across 30 training batches of 4 samples. Each batch mean is a dot; the running mean '
             'starts at 0 and is updated after every batch with momentum 0.1, so it climbs towards about %.1f. At model.eval() '
             'it freezes: a single test sample x = 7 is normalised with the frozen mean and variance, giving %.2f.' % (rm, XHAT),
             'TRAIN: BATCH STATS + UPDATE A RUNNING AVERAGE · EVAL: USE THE FROZEN AVERAGE')
    x0, yb, yt = 50, 250, 50
    PX = lambda k: x0 + 10 + k * 14
    PY = lambda v: yb - v / 9 * (yb - yt)
    xe = PX(STEPS) + 2
    f.static(L(x0, yb, xe + 150, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for v in (0, 3, 6, 9): f.static(T(x0 - 7, PY(v) + 4, str(v), FA, 'end', mono=True) + (L(x0, PY(v), xe + 150, PY(v), RULE, .8) if v else ''))
    for k in (0, 9, 19, 29): f.static(T(PX(k), yb + 15, str(k + 1), FA, mono=True))
    f.static(S(PX(15), yb + 34, 'training batch', MU, 'middle'))
    for k in range(STEPS):
        t = .3 + k * .15
        f.show(dot(PX(k), PY(BMEAN[k]), FI, 3.2), t)
        seg = L(PX(k - 1) if k else x0, PY(RUN[k - 1]) if k else PY(0), PX(k), PY(RUN[k]), AM, 2.2)
        f.show(seg, t + .05)
    f.show(S(PX(1), PY(9.6), '• batch mean μ_B', FI, 'start', True) + S(PX(12), PY(9.6), '— running mean', AM, 'start', True), 1.0)
    te = .3 + STEPS * .15 + .3
    f.show(L(xe, yt - 8, xe, yb, MU, 1.4, '4 3') + T(xe + 6, yt - 8, 'model.eval()', MU, 'start', mono=True, bold=True), te)
    f.show(L(xe, PY(rm), xe + 150, PY(rm), AM, 2.2, '6 4') + T(xe + 150, PY(rm) - 8, 'frozen μ = %.2f' % rm, AM, 'end', mono=True, bold=True), te + .4)
    glide(f, dot(xe + 90, PY(XQ), RO, 5) + T(xe + 100, PY(XQ) + 4, 'x = 7', RO, 'start', mono=True, bold=True),
           [(0, 60, 0), (te + 1, 0, 0)], te + .9, d=.6)
    f.show(gchip(xe + 75, PY(2.2), 'x̂ = %s' % f2(XHAT), 'gr', 96), te + 1.8)
    f.show(T(xe + 75, PY(1.2), '(7 − %.2f) / √%.2f' % (rm, rv), MU, mono=True), te + 1.8)
    return finish(f, yb + 44)

# ---------- 3.2 Batch size ----------
def fig_batchsize():
    f = Anim('nm5-', 720, 0, 'Twelve batches drawn from data whose true mean is 0. With batch size 2 the twelve batch means '
             'scatter widely, spread 0.67. With batch size 32 they huddle near 0, spread 0.15. BatchNorm divides by these '
             'noisy estimates.', 'THE BATCH MEAN IS AN ESTIMATE · SMALL BATCH = NOISY ESTIMATE')
    X0, X1 = 150, 630
    px = lambda v: X0 + (v + 1.6) / 3.2 * (X1 - X0)
    rows = [(2, 100), (32, 210)]
    for B, y in rows:
        f.static(L(X0 - 8, y, X1 + 8, y, RULE_HI, 1.3) + T(0, y + 4, 'batch of %d' % B, TX, 'start', bold=True))
        for v in (-1.5, -1, -.5, 0, .5, 1, 1.5):
            f.static(L(px(v), y - 4, px(v), y + 4, RULE_HI, 1) + T(px(v), y + 18, f2(v), FA, mono=True))
        f.static(L(px(0), y - 46, px(0), y + 6, GR, 1.4, '4 3'))
    f.static(T(px(0), 44, 'true mean 0', GR, bold=True))
    for r, (B, y) in enumerate(rows):
        ms, sd = NOISE[B]
        for k, m in enumerate(ms):
            t = .4 + r * 2.6 + k * .14
            yy = y - 8 - (sum(1 for q in ms[:k] if abs(px(q) - px(m)) < 10)) * 9
            glide(f, dot(px(m), yy, FI, 4), [(0, 0, -36 - (yy - y)), (t + .1, 0, 0)], t, d=.5)
        tt = .4 + r * 2.6 + 2.1
        f.show(L(px(-sd), y + 30, px(sd), y + 30, AM, 2) + L(px(-sd), y + 25, px(-sd), y + 35, AM, 2) + L(px(sd), y + 25, px(sd), y + 35, AM, 2) +
               T(px(sd) + 8, y + 34, 'spread %.2f' % sd, AM, 'start', mono=True, bold=True), tt)
    f.show(S(0, 270, 'spread ≈ 1 / √batch · use GroupNorm or LayerNorm when the batch is tiny', MU), 5.8)
    return finish(f, 282)

# ---------- 04 Why Transformers use LayerNorm ----------
def fig_transformer():
    f = Anim('nm6-', 720, 0, 'A batch of two sentences, five tokens and three tokens plus two padding rows, four features each. '
             'BatchNorm on feature 1 mixes eight tokens from both sentences and the two pads. LayerNorm outlines one token '
             'row at a time and needs nothing else. At inference with one token, BatchNorm has a single value, std 0; '
             'LayerNorm still has its four features.', 'BATCHNORM MIXES SENTENCES AND PADS · LAYERNORM STAYS INSIDE ONE TOKEN')
    cw, ch, x0, y0 = 40, 22, 90, 50
    rows = [('A', i, False) for i in range(5)] + [('B', i, i >= 3) for i in range(5)]
    def ry(r): return y0 + r * ch + (10 if r >= 5 else 0)
    for r, (sn, i, pad) in enumerate(rows):
        f.static(T(x0 - 8, ry(r) + 15, 'pad' if pad else '%s · t%d' % (sn, i + 1), FA if pad else MU, 'end'))
        for j in range(4):
            f.static(R(x0 + j * cw + 1, ry(r) + 1, cw - 2, ch - 2, SUNK if pad else tn(FI, '.10'), RULE_HI, 3, 1))
    f.static(T(x0 + 2 * cw, y0 - 10, 'features', MU))
    yb = ry(9) + ch
    f.show(R(x0 - 1, y0 - 2, cw + 2, yb - y0 + 4, 'none', RD, 4, 2), .5, hide=2.8)
    for r in (8, 9): f.show(R(x0 + 1, ry(r) + 1, cw - 2, ch - 2, tn(RO, '.2'), RD, 3, 1.4), 1.0, hide=2.8)
    f.show(gchip(x0 + 2 * cw, yb + 22, 'BN · 8 tokens + 2 pads', 'rd', 176), 1.2, hide=2.8)
    for r, (_, _, pad) in enumerate(rows):
        if pad: continue
        f.show(R(x0 - 1, ry(r) - 1, 4 * cw + 2, ch + 2, 'none', GR, 4, 2), 3.0 + r * .2, hide=3.2 + r * .2 + .3)
    f.show(gchip(x0 + 2 * cw, yb + 22, 'LN · each token alone', 'gr', 176), 3.0)
    X = 440; Y = 90
    f.static(L(X - 40, 40, X - 40, yb + 30, RULE, 1) + T(X + 2 * cw, 60, 'inference · batch of 1 token', MU))
    for j in range(4): f.static(R(X + j * cw + 1, Y + 1, cw - 2, ch - 2, tn(FI, '.10'), RULE_HI, 3, 1))
    f.show(R(X - 1, Y - 2, cw + 2, ch + 4, 'none', RD, 4, 2) + gchip(X + cw / 2 + 50, Y + 50, 'BN · 1 value → σ = 0', 'rd', 160), 5.4)
    f.show(R(X - 3, Y - 4, 4 * cw + 6, ch + 8, 'none', GR, 5, 2) + gchip(X + cw / 2 + 50, Y + 80, 'LN · 4 values → fine', 'gr', 160), 6.4)
    return finish(f, yb + 40)

# ---------- 05 Pre-LN / Post-LN ----------
def fig_place(kind):
    post = kind == 'post'
    pre = 'nm7-' if post else 'nm8-'
    f = Anim(pre, 720, 0, ('Two stacked Transformer blocks in Post-LN order: the residual line goes up, the side branch f '
                           'rejoins at a plus, then LayerNorm sits ON the residual line. A forward dot climbs up; then the '
                           'gradient dot descends the residual line and has to pass through both LayerNorm boxes.') if post else
             ('Two stacked Transformer blocks in Pre-LN order: LayerNorm sits inside the side branch before f, the residual '
              'line is bare. A forward dot climbs up; then the gradient dot descends the residual line straight to the input '
              'without touching any LayerNorm.'),
             'POST-LN · LAYERNORM ON THE RESIDUAL LINE' if post else 'PRE-LN · LAYERNORM INSIDE THE BRANCH, RESIDUAL LINE BARE')
    xm, xf = 200, 340
    bot, top = 400, 46
    blocks = [400, 230]
    def box(x, y, s, c, w=86):
        return R(x - w / 2, y - 14, w, 28, BG, 'none', 6) + R(x - w / 2, y - 14, w, 28, tn(c, '.12'), c, 6, 1.4) + T(x, y + 4, s, c, bold=True)
    def plus(x, y):
        return '<circle cx="%.1f" cy="%.1f" r="10" fill="%s" stroke="%s" stroke-width="1.4"/>' % (x, y, BG, MU) + T(x, y + 4.5, '+', TX, bold=True)
    f.static(L(xm, bot + 20, xm, top, RULE_HI, 2.2) + T(xm, bot + 36, 'input', MU) + T(xm, top - 8, 'output → loss', MU))
    lnys = []
    for y0 in blocks:
        ys, yp = y0 - 22, y0 - 120
        f.static(L(xm, ys, xf, ys, RULE_HI, 1.4) + L(xf, ys, xf, yp, RULE_HI, 1.4) + arrow(xf, yp, xm + 11, yp, RULE_HI, 1.4))
        if post:
            f.static(box(xf, y0 - 70, 'f', BR) + plus(xm, yp))
            lnys.append(y0 - 150); f.static(box(xm, y0 - 150, 'LN', VI, 60))
        else:
            f.static(box(xf, y0 - 50, 'LN', VI, 60) + box(xf, y0 - 92, 'f', BR) + plus(xm, yp))
        f.static(T(xf + 56, y0 - 66 if post else y0 - 88, 'attention / MLP', FA, 'start'))
    f.static(T(xm - 20, (bot + top) / 2, 'residual', MU, 'end'))
    f.path(dot(xm, top + 6, FI, 6), [(0, 0, bot - top), (.6, 0, 0)], .4, d=2.2, hide=3.1)
    t = 3.4; stops = sorted(lnys)
    pts = [(0, 0, -(bot - top))]; cur = top
    if post:
        for k, y in enumerate(stops):
            pts.append((t, 0, y - bot)); t += 1.2
            f.show(R(xm - 34, y - 18, 68, 36, 'none', RD, 8, 2.2) + T(xm + 40, y + 4, '× ∂LN/∂x', RD, 'start', mono=True, bold=True), t - .3)
            t += .2
        pts.append((t, 0, 0))
    else:
        pts.append((t, 0, 0))
    f.path(dot(xm, bot, RD, 6), pts, 3.3, d=1.0)
    te = t + 1.2
    f.show(gchip(560, 200, 'gradient passes 2 LN' if post else 'gradient passes 0 LN', 'rd' if post else 'gr', 170), te)
    f.show(S(475, 230, 'deep stack → needs LR warmup' if post else 'stable at 100+ layers', MU), te + .3)
    return finish(f, bot + 46)

# ---------- 06 Diagnosis ----------
def fig_diag():
    f = Anim('nm9-', 720, 0, 'An 8-layer ReLU network with weights drawn at variance 1 over n is run on 64 random inputs. Layer by '
             'layer the standard deviation of the activations is written into a table and plotted. Without a norm it falls '
             'from %.2f to %.3f; with LayerNorm it stays near %.2f in every layer.' % (PLAIN[0], PLAIN[-1], WITHLN[-1]),
             'ONE NUMBER PER LAYER · STD OF THE ACTIVATIONS · DIES OUT OR STAYS PUT')
    t = Table(0, 30, [('layer', 50), ('no norm', 76), ('LayerNorm', 84)])
    f.static(t.head())
    x0, x1, yb, yt = 290, 690, 280, 50
    PX = lambda l: x0 + 20 + l * 50
    PY = lambda s: yb - s / .7 * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for s in (.2, .4, .6): f.static(T(x0 - 7, PY(s) + 4, '%.1f' % s, FA, 'end', mono=True) + L(x0, PY(s), x1, PY(s), RULE, .8))
    for l in range(8): f.static(T(PX(l), yb + 15, str(l + 1), FA, mono=True))
    f.static(S(x1, yb + 34, 'layer', MU, 'end') + S(x0, yt - 10, 'std of activations', MU))
    for l in range(8):
        tt = .4 + l * .7
        f.show(t.row(l, [str(l + 1), '%.3f' % PLAIN[l], '%.3f' % WITHLN[l]], colors={1: RD, 2: GR}), tt)
        seg = ''
        if l: seg = L(PX(l - 1), PY(PLAIN[l - 1]), PX(l), PY(PLAIN[l]), RD, 2) + L(PX(l - 1), PY(WITHLN[l - 1]), PX(l), PY(WITHLN[l]), GR, 2)
        f.show(seg + dot(PX(l), PY(PLAIN[l]), RD, 4) + dot(PX(l), PY(WITHLN[l]), GR, 4), tt + .35)
    f.show(S(PX(5), PY(WITHLN[5]) - 12, 'LayerNorm', GR, 'middle', True) + S(PX(6), PY(PLAIN[6]) + 24, 'no norm', RD, 'middle', True), 6.2)
    return finish(f, max(yb + 44, t.bottom(8) + 10))

BODY = r'''<header class="hero">
  <p class="eyebrow">Deep learning · Neural network</p>
  <h1>Normalization — BatchNorm &amp; <em>LayerNorm</em></h1>
  <p class="lede">A norm layer re-centres a group of activations to mean 0 and spread 1, then lets two learned numbers set the scale back — BatchNorm and LayerNorm differ only in <b>which group</b>.</p>
</header>

<section id="norm-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Measure a group's <em>mean and spread</em>, shift and squeeze it to 0 and 1, then rescale with <em>γ, β</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>x̂</var></span><em>normalised</em></span>
      <span class="op">=</span>
      <span class="t"><span><span class="frac"><i><var>x</var> − <var>μ</var></i><i>√(<var>σ</var><sup>2</sup> + <var>ε</var>)</i></span></span><em>μ, σ² of the group</em></span>
      <span class="op">,</span>
      <span class="t p"><span><var>y</var> = <var>γ</var> <var>x̂</var> + <var>β</var></span><em>learned scale and shift</em></span>
    </div>
  </div>
{nm1}
  <ul class="why">
    <li>Deep stacks drift: each layer's activations shrink or blow up (section 06). The norm re-pins them every layer.</li>
    <li><span class="mth"><var>γ</var></span> starts at 1, <span class="mth"><var>β</var></span> at 0, so the network can undo the norm if that helps; <span class="mth"><var>ε</var></span> only guards against dividing by 0.</li>
  </ul>
</section>

<section id="norm-s2" class="lesson">
  <div class="sh"><b>02</b><h2>BatchNorm vs LayerNorm</h2></div>
  <p class="key">Same formula, same tensor: the only difference is <em>the axis the statistics run along</em>.</p>
  <div class="subsec" id="norm-s2-1">
    <h3 class="ssh"><b>2.1</b>BatchNorm</h3>
    <p class="skey">One <em>μ, σ per feature</em>, computed down the column, across the samples of the batch.</p>
{nm2}
    <ul class="why">
      <li>Each sample's output depends on the other samples in the batch — the root of section 03.</li>
      <li>The default in CNNs: statistics per channel, over batch × height × width. A bias right before it is redundant (<code>bias=False</code>).</li>
    </ul>
  </div>
  <div class="subsec" id="norm-s2-2">
    <h3 class="ssh"><b>2.2</b>LayerNorm</h3>
    <p class="skey">One <em>μ, σ per token</em>, computed along the row, across its own features.</p>
{nm3}
    <ul class="why">
      <li>No other row is used, so training and inference compute exactly the same thing.</li>
      <li><b>RMSNorm</b> drops the mean: <span class="mth"><var>y</var> = <var>γ</var> <var>x</var> / √(mean(<var>x</var><sup>2</sup>) + <var>ε</var>)</span>; slightly cheaper, same quality — used in LLaMA and most new LLMs.</li>
    </ul>
  </div>
</section>

<section id="norm-s3" class="lesson">
  <div class="sh"><b>03</b><h2>BatchNorm and its batch</h2></div>
  <p class="key">BatchNorm's statistics are <em>estimates from one batch</em>: they need a stand-in at test time and enough samples to be trusted.</p>
  <div class="subsec" id="norm-s3-1">
    <h3 class="ssh"><b>3.1</b>Train vs inference</h3>
    <p class="skey">Training uses the batch's own stats and updates a <em>running average</em>; <code>eval()</code> freezes it.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>μ</var><sub>run</sub></span><em>running mean</em></span>
      <span class="op">←</span>
      <span class="t"><span>(1 − <var>m</var>) <var>μ</var><sub>run</sub></span><em>old estimate</em></span>
      <span class="op">+</span>
      <span class="t b"><span><var>m</var> <var>μ</var><sub><var>B</var></sub></span><em>this batch · m = 0.1</em></span>
    </div>
  </div>
{nm4}
    <ul class="why">
      <li>Forgetting <code>model.eval()</code> keeps using batch stats: one sample's prediction then depends on its neighbours.</li>
      <li>The running variance is updated the same way; both are buffers, not learned parameters.</li>
    </ul>
  </div>
  <div class="subsec" id="norm-s3-2">
    <h3 class="ssh"><b>3.2</b>Batch size</h3>
    <p class="skey">A batch of 2 gives a <em>noisy μ and σ</em>; the noise goes straight into every normalised value.</p>
{nm5}
    <ul class="why">
      <li>A little noise regularises; below about 8 samples per GPU it hurts. Fixes: GroupNorm, SyncBatchNorm, or LayerNorm.</li>
    </ul>
  </div>
</section>

<section id="norm-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Why Transformers use LayerNorm</h2></div>
  <p class="key">Sentences have <em>different lengths</em> and generation runs <em>one token at a time</em>: only a per-token norm survives both.</p>
{nm6}
  <ul class="why">
    <li>BatchNorm would average padding into the statistics and break at batch 1; LayerNorm never looks outside the token.</li>
  </ul>
</section>

<section id="norm-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Where to put the norm</h2></div>
  <p class="key">In a residual block the norm either sits <em>on the residual line</em> or <em>inside the branch</em> — the gradient feels the difference.</p>
  <div class="subsec" id="norm-s5-1">
    <h3 class="ssh"><b>5.1</b>Post-LN</h3>
    <p class="skey">Add first, then normalise: <em>every block's LN cuts the residual line</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>x</var><sub><var>l</var>+1</sub></span><em>block output</em></span>
      <span class="op">=</span>
      <span class="t p"><span><b class="fn">LN</b>(<var>x</var><sub><var>l</var></sub> + <var>f</var>(<var>x</var><sub><var>l</var></sub>))</span><em>norm on the sum</em></span>
    </div>
  </div>
{nm7}
    <ul class="why">
      <li>The original Transformer and BERT. Deep stacks need a careful learning-rate warmup or they diverge.</li>
    </ul>
  </div>
  <div class="subsec" id="norm-s5-2">
    <h3 class="ssh"><b>5.2</b>Pre-LN</h3>
    <p class="skey">Normalise the branch input, then add: <em>the residual line stays bare</em> from loss to input.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>x</var><sub><var>l</var>+1</sub></span><em>block output</em></span>
      <span class="op">=</span>
      <span class="t"><span><var>x</var><sub><var>l</var></sub></span><em>untouched</em></span>
      <span class="op">+</span>
      <span class="t p"><span><var>f</var>(<b class="fn">LN</b>(<var>x</var><sub><var>l</var></sub>))</span><em>norm inside the branch</em></span>
    </div>
  </div>
{nm8}
    <ul class="why">
      <li>GPT-2 onwards, LLaMA, almost every modern LLM; one extra LN after the last block. Why a bare path helps is the residual argument in <a href="../backpropagation/index.html">Backpropagation</a>.</li>
    </ul>
  </div>
</section>

<section id="norm-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Diagnosing with statistics</h2></div>
  <p class="key">Print the <em>std of the activations per layer</em>: shrinking to 0 or growing without bound is the symptom a norm fixes.</p>
{nm9}
  <ul class="why">
    <li>Log it with forward hooks on a few batches; a healthy net keeps a similar order of magnitude in every layer.</li>
    <li>Setting the right magnitude at step 0 is <a href="../weight-initialization/index.html">Weight initialization</a>; the norm keeps it right during training.</li>
  </ul>
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

<footer>Deep learning · Neural network · next lesson in the group: <a href="../dropout-regularization/index.html">Dropout &amp; regularization</a>.</footer>
'''

def build():
    figs = dict(nm1=fig_mental(), nm2=fig_axis('bn'), nm3=fig_axis('ln'), nm4=fig_running(), nm5=fig_batchsize(),
                nm6=fig_transformer(), nm7=fig_place('post'), nm8=fig_place('pre'), nm9=fig_diag())
    return re.sub(r'\{(nm\d+)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">'); b = s.index('</article>')
    s = s[:a] + body + '\n      ' + s[b:]
    m = re.search(r'<article class="doc"[^>]*>', s)
    tag = m.group(0)
    tag = re.sub(r' data-(skeleton|reviewed|progress)="[^"]*"', '', tag)
    tag = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s" data-progress="1"' % blurb, tag)
    s = s[:m.start()] + tag + s[m.end():]
    open(page, 'w').write(s)

if __name__ == '__main__':
    splice(PAGE, build(), 'Shift a group of activations to mean 0 and spread 1, then rescale: BatchNorm groups down the batch, '
           'LayerNorm along one token, and where the norm sits decides how the gradient flows.')
    print('ok running mean %.3f var %.3f xhat %.3f' % (rm, rv, XHAT))
