# -*- coding: utf-8 -*-
"""Figures + body for content/08-deep-learning/02-neural-network/neural-network-overview.
One tiny network (2-2-1 on XOR) and a deeper stack of the same layers, trained / run in pure Python with fixed
seeds. Each subsection breaks the network one way and shows the failure; every number is computed here and pinned
with assert. Run: python3 neural_network_overview.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import decision_tree as dt
from linear_algebra import Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, BR, VI, FI, RO, RULE, BG, S, dot, poly, finish
from tablefig import GR, AM, RD, Table

PAGE = os.path.join(HERE, '../../../content/08-deep-learning/02-neural-network/neural-network-overview/index.html')
_RGB = {GR: '--green-a', RD: '--red-a', AM: '--amber-a', FI: '--blue-a', VI: '--violet-a', BR: '--clay-a'}
def tn(c, a='.14'): return 'rgba(var(%s),%s)' % (_RGB[c], a)
def chip(cx, cy, s, c=VI, w=None):
    w = w or 16 + len(s) * 7.2
    return (R(cx - w / 2, cy - 11, w, 22, BG, 'none', 11) + R(cx - w / 2, cy - 11, w, 22, tn(c), c, 11, 1.3) +
            T(cx, cy + 4.5, s, c, mono=True, bold=True))
def node(x, y, s='', c=RULE_HI, fill=BG, r=17, tc=TX):
    return ('<circle cx="%.1f" cy="%.1f" r="%d" fill="%s"/>' % (x, y, r, BG) +
            '<circle cx="%.1f" cy="%.1f" r="%d" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, y, r, fill, c, ) +
            (T(x, y + 4, s, tc, mono=True, bold=True) if s else ''))

# ---------- the XOR network ----------
XS = [(0, 0), (0, 1), (1, 0), (1, 1)]; YS = [0, 1, 1, 0]
sig = lambda z: 1 / (1 + math.exp(-z))

def init(seed):
    g = random.Random(seed)
    W = [[g.gauss(0, 1) for _ in range(2)] for _ in range(2)]; V = [g.gauss(0, 1) for _ in range(2)]
    return dict(W=W, b=[0.0, 0.0], V=V, c=0.0)

def fwd(P, x, act='tanh'):
    z = [P['W'][j][0] * x[0] + P['W'][j][1] * x[1] + P['b'][j] for j in range(2)]
    h = [math.tanh(v) if act == 'tanh' else v for v in z]
    return h, sig(P['V'][0] * h[0] + P['V'][1] * h[1] + P['c'])

def loss(P, act='tanh'):
    s = 0
    for x, y in zip(XS, YS):
        p = fwd(P, x, act)[1]; p = min(max(p, 1e-12), 1 - 1e-12)
        s -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return s / 4

def grads(P, rows, act='tanh'):
    """backprop over the given rows, mean"""
    G = dict(W=[[0, 0], [0, 0]], b=[0, 0], V=[0, 0], c=0)
    for x, y in rows:
        h, p = fwd(P, x, act); d = p - y; G['c'] += d / len(rows)
        for j in range(2):
            G['V'][j] += d * h[j] / len(rows)
            dh = d * P['V'][j] * ((1 - h[j] ** 2) if act == 'tanh' else 1)
            G['b'][j] += dh / len(rows); G['W'][j][0] += dh * x[0] / len(rows); G['W'][j][1] += dh * x[1] / len(rows)
    return G

def train(seed=0, act='tanh', ep=2000, lr=.5):
    P = init(seed); hist = []
    for e in range(ep + 1):
        hist.append(loss(P, act))
        if e == ep: break
        G = grads(P, list(zip(XS, YS)), act)
        for j in range(2):
            P['V'][j] -= lr * G['V'][j]; P['b'][j] -= lr * G['b'][j]
            for k in range(2): P['W'][j][k] -= lr * G['W'][j][k]
        P['c'] -= lr * G['c']
        if hist[-1] > 1e3 or hist[-1] != hist[-1]: pass
    return P, hist

PT, HT = train()                       # the trained XOR net
_, HL = train(act='linear')            # same net, no nonlinearity
assert HT[-1] < .01 and abs(HL[-1] - math.log(2)) < 1e-3, (HT[-1], HL[-1])
PRED = [fwd(PT, x)[1] for x in XS]
assert [round(p) for p in PRED] == YS
LR = {lr: train(lr=lr, ep=600)[1] for lr in (.05, .5, 30)}
assert LR[.05][-1] > .35 and LR[.5][-1] < .02 and LR[30][-1] > 10, [LR[k][-1] for k in LR]

PNAMES = ['w₁₁', 'w₁₂', 'w₂₁', 'w₂₂', 'b₁', 'b₂', 'v₁', 'v₂', 'c']
def flat(P): return [P['W'][0][0], P['W'][0][1], P['W'][1][0], P['W'][1][1], P['b'][0], P['b'][1], P['V'][0], P['V'][1], P['c']]
def unflat(v): return dict(W=[[v[0], v[1]], [v[2], v[3]]], b=[v[4], v[5]], V=[v[6], v[7]], c=v[8])
P0 = init(0)
GB = flat(grads(P0, list(zip(XS, YS))))
EPS = 1e-4; L0 = loss(P0)
GN = []
for k in range(9):
    v = flat(P0); v[k] += EPS; GN.append((loss(unflat(v)) - L0) / EPS)
assert all(abs(a - b) < 1e-3 for a, b in zip(GB, GN)), (GB, GN)

# ---------- the deep stack (32 wide, 8 layers) ----------
def deep(seed, std, act, norm=False, Lyr=8, n=32):
    g = random.Random(seed); x = [[g.gauss(0, 1) for _ in range(n)] for _ in range(64)]; out = []
    for l in range(Lyr):
        W = [[g.gauss(0, std) for _ in range(n)] for _ in range(n)]
        x = [[sum(W[i][k] * r[k] for k in range(n)) for i in range(n)] for r in x]
        if norm:
            nx = []
            for r in x:
                m = sum(r) / n; s = math.sqrt(sum((u - m) ** 2 for u in r) / n) + 1e-5
                nx.append([(u - m) / s for u in r])
            x = nx
        x = [[act(v) for v in r] for r in x]
        a = [v for r in x for v in r]; m = sum(a) / len(a); out.append(math.sqrt(sum((v - m) ** 2 for v in a) / len(a)))
    return out
relu = lambda v: max(0.0, v)
INIT_BAD = deep(1, .05, math.tanh); INIT_OK = deep(1, 1 / math.sqrt(32), math.tanh)
assert INIT_BAD[-1] < 1e-4 and min(INIT_OK) > .2, (INIT_BAD, INIT_OK)
NORM_BAD = deep(1, .5, relu); NORM_OK = deep(1, .5, relu, True)
assert NORM_BAD[-1] > 100 and all(.5 < v < .7 for v in NORM_OK), (NORM_BAD, NORM_OK)

# ---------- overfitting: 12 noisy points, 32 hidden units ----------
def pts(seed, n):
    g = random.Random(seed); out = []
    for _ in range(n):
        x = g.uniform(-1, 1); out.append((x, math.sin(3 * x) + g.gauss(0, .35)))
    return out
TR, VA = pts(1, 12), pts(2, 60)
def fit(p, ep=3000, H=32, lr=.05, seed=0):
    g = random.Random(seed)
    W = [g.gauss(0, 1.5) for _ in range(H)]; b = [g.gauss(0, 1) for _ in range(H)]
    V = [g.gauss(0, 1 / math.sqrt(H)) for _ in range(H)]; c = 0
    def f(x): return sum(V[j] * math.tanh(W[j] * x + b[j]) for j in range(H)) + c
    tr, va = [], []
    for e in range(ep):
        if e % 100 == 0:
            tr.append(sum((f(x) - y) ** 2 for x, y in TR) / len(TR)); va.append(sum((f(x) - y) ** 2 for x, y in VA) / len(VA))
        gW = [0] * H; gb = [0] * H; gV = [0] * H; gc = 0
        for x, y in TR:
            m = [(1 if g.random() > p else 0) / (1 - p) for _ in range(H)] if p else [1] * H
            hs = [math.tanh(W[j] * x + b[j]) for j in range(H)]
            o = sum(V[j] * hs[j] * m[j] for j in range(H)) + c; d = 2 * (o - y) / len(TR); gc += d
            for j in range(H):
                gV[j] += d * hs[j] * m[j]; dh = d * V[j] * m[j] * (1 - hs[j] ** 2); gW[j] += dh * x; gb[j] += dh
        for j in range(H): W[j] -= lr * gW[j]; b[j] -= lr * gb[j]; V[j] -= lr * gV[j]
        c -= lr * gc
    return tr, va
DR0 = fit(0); DR5 = fit(.5)
assert DR0[1][-1] > DR0[1][2] and DR0[0][-1] < .13 and DR5[1][-1] < DR0[1][-1] - .2, (DR0[1][-1], DR5[1][-1])

# ---------- drawing helpers ----------
def netpos(ox, oy, gap=130, sp=90):
    I = [(ox, oy), (ox, oy + sp)]; Hn = [(ox + gap, oy), (ox + gap, oy + sp)]; O = (ox + 2 * gap, oy + sp / 2)
    return I, Hn, O
def edges(I, Hn, O, P=None, c=RULE_HI):
    s = ''
    for j in range(2):
        for k in range(2):
            w = abs(P['W'][j][k]) if P else 1
            s += L(I[k][0] + 17, I[k][1], Hn[j][0] - 17, Hn[j][1], c, min(.8 + w * .45, 4.5))
        w = abs(P['V'][j]) if P else 1
        s += L(Hn[j][0] + 17, Hn[j][1], O[0] - 17, O[1], c, min(.8 + w * .3, 4.5))
    return s

def curve(f, x0, y0, w, h, vals, c, ymax, t0, dur, ymin=0, label=None, lx=None, log=False):
    """vals drawn left to right, a dot gliding along as the line grows"""
    n = len(vals)
    def Y(v):
        if log: v = math.log10(max(v, 1e-3)); lo, hi = math.log10(max(ymin, 1e-3)), math.log10(ymax)
        else: lo, hi = ymin, ymax
        return y0 + h - (min(v, hi) - lo) / (hi - lo) * h
    P = [(x0 + i * w / (n - 1), Y(v)) for i, v in enumerate(vals)]
    K = 8; step = (n - 1) / K; seg_t = dur / K
    for k in range(K):
        a, b = int(round(k * step)), int(round((k + 1) * step))
        f.show(poly(P[a:b + 1], c, 2), t0 + k * seg_t, d=seg_t)
    ex, ey = P[-1]
    f.path(dot(ex, ey, c, 4), [(0, P[0][0] - ex, P[0][1] - ey)] +
           [(t0 + (k + 1) * seg_t - seg_t, P[int(round((k + 1) * step))][0] - ex, P[int(round((k + 1) * step))][1] - ey)
            for k in range(K)], t0, d=seg_t)
    if label: f.show(T(lx or ex + 8, ey + 4, label, c, 'start', cls='sv-s', bold=True), t0 + dur)
    return P

def axes(f, x0, y0, w, h, ylab, xlab, ticks):
    s = L(x0, y0 + h, x0 + w, y0 + h, RULE_HI, 1) + L(x0, y0, x0, y0 + h, RULE_HI, 1)
    for v, y in ticks: s += T(x0 - 6, y + 3.5, v, FA, 'end', mono=True) + L(x0 - 3, y, x0, y, RULE_HI, 1)
    s += T(x0, y0 - 8, ylab, MU, 'start', cls='sv-d') + T(x0 + w, y0 + h + 16, xlab, FA, 'end', cls='sv-d')
    f.static(s)

def badge(f, x, y, steps):
    for t, s, e in steps:
        f.show(R(x, y - 13, 3, 18, AM, 'none', 1.5) + T(x + 10, y + 1, s, AM, 'start', cls='sv-s', bold=True), t, hide=e)

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('nno1-', 720, 0, 'A 2-2-1 network trained on XOR. Each of the four rows in turn: its two inputs fly from the '
             'table into the input neurons, the two hidden neurons light up with their tanh values, the output neuron '
             'shows the probability p, and p flies back into the table. All four predictions round to the right label: %s.'
             % ', '.join('%.2f' % p for p in PRED), 'ONE ROW IN · NUMBERS FLOW ALONG THE EDGES · ONE PROBABILITY OUT')
    I, Hn, O = netpos(40, 80)
    f.static(edges(I, Hn, O, PT) + ''.join(node(*p) for p in I + Hn) + node(*O) +
             T(I[0][0], 50, 'input', MU, cls='sv-d') + T(Hn[0][0], 50, 'hidden · tanh', MU, cls='sv-d') +
             T(O[0], 50, 'output · sigmoid', MU, cls='sv-d'))
    t = Table(400, 40, [('x₁', 56), ('x₂', 56), ('y', 56), ('p', 80)])
    f.static(t.head() + ''.join(t.row(i, [str(XS[i][0]), str(XS[i][1]), str(YS[i]), '']) for i in range(4)))
    t0 = .5; D = 2.4
    for i in range(4):
        e = t0 + D - .1
        f.show(t.outline(i), t0, hide=e)
        for k in range(2):
            sx, sy = t.cx(k), t.ry(i) + 13
            f.path(node(*I[k], str(XS[i][k]), FI, tn(FI, '.18'), tc=FI),
                   [(0, sx - I[k][0], sy - I[k][1]), (t0 + .3, 0, 0)],
                   t0, d=.6, hide=e)
        h, p = fwd(PT, XS[i])
        for j in range(2): f.show(node(*Hn[j], '%.2f' % h[j], VI, tn(VI, '.15'), r=19, tc=VI), t0 + 1.25, hide=e)
        c = GR if round(p) == YS[i] else RD
        f.show(node(*O, '%.2f' % p, c, tn(c, '.15'), r=19, tc=c), t0 + 1.55, hide=e)
        tx, ty = t.cx(3), t.ry(i) + 13
        f.path(chip(tx, ty, '%.2f' % p, c, 54), [(0, O[0] - tx, O[1] - ty), (t0 + 1.85, 0, 0)], t0 + 1.65, d=.5)
        t0 += D
    f.show(T(400, t.bottom(4) + 26, 'loss on all four rows %.3f · every p rounds to y' % HT[-1], GR, 'start', cls='sv-s', bold=True), t0)
    return finish(f, 240)

# ---------- 2.1 one neuron: a line ----------
def line_err(a, b, c):
    return sum((1 if a * x + b * y + c > 0 else 0) != t for (x, y), t in zip(XS, YS))
BEST = min(line_err(math.cos(th), math.sin(th), c / 10) for th in [k * math.pi / 36 for k in range(72)] for c in range(-20, 21))
assert BEST == 1
LINES = [((1, 1, -.5), 'x₁ + x₂ > 0.5'), ((1, 1, -1.5), 'x₁ + x₂ > 1.5'), ((1, -1, -.5), 'x₁ − x₂ > 0.5')]
assert [line_err(*l) for l, _ in LINES] == [1, 3, 1]
def fig_line():
    f = Anim('nno2-', 720, 0, 'XOR: four points, (0,1) and (1,0) are class 1, (0,0) and (1,1) class 0. One neuron draws one '
             'straight line. Three lines are tried in turn and each leaves at least one point on the wrong side, ringed in '
             'red. A search over 2,952 lines finds none with fewer than %d mistake.' % BEST,
             'ONE NEURON = ONE STRAIGHT LINE · XOR NEEDS TWO')
    ox, oy, S_ = 70, 230, 170
    X = lambda v: ox + v * S_; Y = lambda v: oy - v * S_
    f.static(R(X(-.15), Y(1.15), 1.3 * S_, 1.3 * S_, 'none', RULE, 4) + T(X(1.15), oy + 34, 'x₁', MU, 'end') + T(X(-.15) - 6, Y(1.1), 'x₂', MU, 'end'))
    for (x, y), t in zip(XS, YS):
        c = VI if t else FI
        f.static(dot(X(x), Y(y), c, 8, BG) + T(X(x) + (24 if x else -24), Y(y) + 4, str(t), c, mono=True, bold=True))
    t0 = .5; D = 2.2; steps = []
    for k, ((a, b, c), lab) in enumerate(LINES):
        e = t0 + D if k < 2 else None
        # line a x + b y + c = 0 across the box
        if b == 0: continue
        lo_, hi_ = -.15, 1.15; cand = []
        for xx in (lo_, hi_):
            yy = -(a * xx + c) / b
            if lo_ - 1e-9 <= yy <= hi_ + 1e-9: cand.append((xx, yy))
        for yy in (lo_, hi_):
            xx = -(b * yy + c) / a
            if lo_ - 1e-9 <= xx <= hi_ + 1e-9: cand.append((xx, yy))
        p1, p2 = cand[0], cand[-1]
        f.show(L(X(p1[0]), Y(p1[1]), X(p2[0]), Y(p2[1]), AM, 2), t0, hide=e)
        bad = [i for i, ((x, y), tt) in enumerate(zip(XS, YS)) if (1 if a * x + b * y + c > 0 else 0) != tt]
        f.show(''.join('<circle cx="%.1f" cy="%.1f" r="14" fill="none" stroke="%s" stroke-width="2"/>' % (X(XS[i][0]), Y(XS[i][1]), RD)
                       for i in bad), t0 + .6, hide=e)
        f.show(T(410, 120 + k * 34, lab, TX, 'start', mono=True) + T(560, 120 + k * 34, '%d wrong' % len(bad), RD, 'start', cls='sv-s', bold=True), t0 + .6)
        t0 += D
    f.show(T(410, 250, 'best of 2,952 lines: %d wrong' % BEST, RD, 'start', cls='sv-s', bold=True) +
           T(410, 270, 'two hidden neurons = two lines → 0 wrong', GR, 'start', cls='sv-s', bold=True), t0)
    f.static(T(410, 84, 'the rule the neuron learns', MU, 'start', cls='sv-d'))
    return finish(f, 290)

# ---------- 2.2 nonlinearity: loss curves tanh vs linear ----------
def fig_act():
    f = Anim('nno3-', 720, 0, 'The same 2-2-1 network trained on XOR twice for 2,000 steps. With tanh in the hidden layer the '
             'loss falls from %.2f to %.3f. With no activation the two layers multiply into one straight line and the loss '
             'flattens at %.3f, which is ln 2: the network answers 0.5 for every row.' % (HT[0], HT[-1], HL[-1]),
             'NO ACTIVATION · TWO LAYERS COLLAPSE INTO ONE · LOSS STUCK AT ln 2')
    x0, y0, w, h = 60, 46, 480, 180; ym = .9
    axes(f, x0, y0, w, h, 'loss', 'training step 0 → 2,000', [('%g' % v, y0 + h - v / ym * h) for v in (0, .3, .6, .9)])
    curve(f, x0, y0, w, h, HL[::50], RD, ym, .4, 3, label='linear · %.3f' % HL[-1])
    curve(f, x0, y0, w, h, HT[::50], GR, ym, .4, 3, label='tanh · %.3f' % HT[-1])
    return finish(f, 250)

# ---------- 2.3 gradients: nudge each weight vs one backward pass ----------
def fig_grad():
    f = Anim('nno4-', 720, 0, 'The 9 parameters of the XOR network at their random start. Left column: nudge one parameter, '
             'run all four rows forward again, see how the loss moved; the pass counter climbs to 10. Right column: one '
             'forward and one backward pass send every gradient back along the edges at once. The two columns agree to 3 decimals.',
             'NUDGE EACH WEIGHT: ONE PASS PER WEIGHT · BACKPROP: ALL GRADIENTS IN ONE BACKWARD PASS')
    I, Hn, O = netpos(30, 70, 110, 100)
    f.static(edges(I, Hn, O) + ''.join(node(*p) for p in I + Hn) + node(*O) + R(O[0] + 40, O[1] - 18, 60, 36, BG, AM, 6, 1.4) +
             T(O[0] + 70, O[1] + 4, 'loss', AM, cls='sv-s', bold=True) + L(O[0] + 17, O[1], O[0] + 40, O[1], AM, 1.4))
    t = Table(400, 30, [('param', 64), ('nudge', 100), ('backprop', 100)], step=22, rh=19)
    f.static(t.head() + ''.join(t.row(i, [PNAMES[i], '', ''], ) for i in range(9)))
    eds = [(I[0], Hn[0]), (I[1], Hn[0]), (I[0], Hn[1]), (I[1], Hn[1]), (Hn[0], Hn[0]), (Hn[1], Hn[1]), (Hn[0], O), (Hn[1], O), (O, O)]
    t0 = .4; D = .75
    for k in range(9):
        a, b = eds[k]; mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - (22 if a == b else 0)
        f.show(chip(mx, my, '+ε', AM, 34), t0, hide=t0 + D - .05)
        f.show(t.cell(k, 1, '%+.3f' % GN[k]).replace('<text', '<text').replace('font', 'font'), t0 + .4)
        f.show(T(30, 40, '', MU), t0)
        f.show(T(30, 250, 'forward passes: %d' % (k + 2), RD, 'start', cls='sv-s', bold=True),
               t0, hide=t0 + D if k < 8 else None)
        t0 += D
    t1 = t0 + .4
    # backward wave: gradients travel output → hidden → input
    gx = O[0] + 70
    for j in range(2):
        f.path(chip(Hn[j][0], Hn[j][1] - 28, '∂', VI, 26), [(0, gx - Hn[j][0], O[1] - Hn[j][1] + 28 + (2 * j - 1) * 16), (t1 + .2 + j * .25, 0, 0)], t1 + j * .25, d=.7, hide=t1 + 1.6)
        for k in range(2):
            ex, ey = I[k][0] + (Hn[j][0] - I[k][0]) * .3, I[k][1] + (Hn[j][1] - I[k][1]) * .3
            ts = t1 + .9 + (2 * j + k) * .2
            f.path(chip(ex, ey, '∂', VI, 26), [(0, Hn[j][0] - 30 - ex, Hn[j][1] + (k - .5) * 30 - ey), (ts + .1, 0, 0)], ts, d=.6, hide=t1 + 2.6)
    f.show(''.join(t.cell(k, 2, '%+.3f' % GB[k], c=VI) for k in range(9)), t1 + 2.4)
    f.show(T(250, 250, 'backprop: 2 passes', GR, 'start', cls='sv-s', bold=True), t1 + 2.4)
    return finish(f, 262)

# ---------- 2.4 / 2.5 activation scale per layer (8 layers) ----------
def fig_layers(pre, bad, ok, blab, olab, cap, aria, lo, hi):
    f = Anim(pre, 720, 0, aria, cap)
    x0, y0, w, h = 70, 50, 600, 160
    def Y(v): return y0 + h - (math.log10(max(v, lo)) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * h
    tk = [10 ** e for e in range(int(round(math.log10(lo))), int(round(math.log10(hi))) + 1)]
    axes(f, x0, y0, w, h, 'spread of activations (std, log scale)', 'layer', [(('%g' % v), Y(v)) for v in tk])
    f.static(L(x0, Y(1), x0 + w, Y(1), RULE, 1, '4 3'))
    bw = 26; gap = w / 8
    for l in range(8):
        cx = x0 + gap * (l + .5)
        f.static(T(cx, y0 + h + 16, str(l + 1), FA, mono=True))
        tt = .4 + l * .5
        for s, (vals, c) in enumerate(((bad, RD), (ok, GR))):
            x = cx - bw - 2 + s * (bw + 4); v = vals[l]; top = Y(v)
            f.show(R(x, top, bw, y0 + h - top, tn(c, '.25'), c, 2, 1.2), tt + s * .2)
            f.show(T(x + bw / 2, top - 5, ('%.2f' % v) if v >= .01 else ('%.0e' % v).replace('e-0', 'e-'), c, mono=True), tt + s * .2 + .2)
    f.show(R(x0 + 10, y0 + h + 30, 12, 12, tn(RD, '.25'), RD, 2) + T(x0 + 28, y0 + h + 40, blab, RD, 'start', cls='sv-s', bold=True) +
           R(x0 + 330, y0 + h + 30, 12, 12, tn(GR, '.25'), GR, 2) + T(x0 + 348, y0 + h + 40, olab, GR, 'start', cls='sv-s', bold=True), 4.6)
    return finish(f, y0 + h + 52)

# ---------- 2.6 / 2.7 training curves ----------
def fig_lr():
    f = Anim('nno7-', 720, 0, 'The XOR network trained for 600 steps with three learning rates. 0.05 creeps from %.2f to %.2f; '
             '0.5 drops to %.3f; 30 jumps out of the valley at the first steps and stays at %.1f.' % (
                 LR[.05][0], LR[.05][-1], LR[.5][-1], LR[30][-1]), 'SAME NETWORK · SAME GRADIENTS · ONLY THE STEP SIZE CHANGES')
    x0, y0, w, h = 60, 46, 470, 180; lo, hi = .01, 20
    def Y(v): return y0 + h - (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * h
    axes(f, x0, y0, w, h, 'loss (log scale)', 'training step 0 → 600', [('%g' % v, Y(v)) for v in (.01, .1, 1, 10)])
    for k, (lr, c, lab) in enumerate(((30, RD, 'lr 30 · diverges'), (.05, AM, 'lr 0.05 · too slow'), (.5, GR, 'lr 0.5 · %.3f' % LR[.5][-1]))):
        curve(f, x0, y0, w, h, LR[lr][::20], c, hi, .4 + k * .3, 3, ymin=lo, label=lab, log=True)
    return finish(f, 250)

def fig_drop():
    f = Anim('nno8-', 720, 0, 'A 32-unit network fitted to 12 noisy points for 3,000 steps, checked on 60 new points. Without '
             'dropout the training error falls to %.2f while the error on new points rises from %.2f to %.2f: it memorises '
             'the noise. With dropout 0.5 the new-point error ends at %.2f.' % (DR0[0][-1], DR0[1][2], DR0[1][-1], DR5[1][-1]),
             'TRAINING ERROR FALLS · ERROR ON NEW DATA TELLS THE TRUTH')
    ym = .8; w, h, y0 = 230, 160, 60
    for p, (tr, va), x0, ttl in ((0, DR0, 50, 'no dropout'), (1, DR5, 390, 'dropout 0.5')):
        f.static(T(x0, 40, ttl, TX, 'start', cls='sv-s', bold=True))
        axes(f, x0, y0, w, h, '', 'step 0 → 3,000', [('%g' % v, y0 + h - v / ym * h) for v in (0, .4, .8)])
        curve(f, x0, y0, w, h, tr, FI, ym, .4 + p * 3.4, 3, label='train %.2f' % tr[-1])
        curve(f, x0, y0, w, h, va, RD if p == 0 else GR, ym, .4 + p * 3.4, 3, label='new %.2f' % va[-1])
    return finish(f, 245)

# ---------- 03 Learning order ----------
ORDER = [('Perceptron & MLP', 'neurons in layers', '../perceptron-mlp/index.html', 'one line'),
         ('Activation functions', 'bend the line', '../activation-functions/index.html', 'collapse'),
         ('Backpropagation', 'all gradients at once', '../backpropagation/index.html', 'slow'),
         ('Weight initialization', 'right starting scale', '../weight-initialization/index.html', 'fades'),
         ('Normalization', 'rescale every layer', '../normalization/index.html', 'explodes'),
         ('Optimizer', 'good step size', '../optimizer-overview/index.html', 'diverges'),
         ('Dropout', 'stop memorising', '../dropout-regularization/index.html', 'memorises')]
def fig_order():
    f = Anim('nno9-', 720, 0, 'Seven lessons read top to bottom. Each row: the lesson, the failure it fixes in red, and what '
             'it adds. A green tick appears as each is added to the network, ending with a network that trains deep, fast and '
             'generalises.', 'READ TOP TO BOTTOM · EACH LESSON FIXES ONE FAILURE')
    f.static(T(40, 40, 'lesson', MU, 'start', cls='sv-d') + T(260, 40, 'without it', MU, 'start', cls='sv-d') +
             T(420, 40, 'what it adds', MU, 'start', cls='sv-d') + L(0, 48, 700, 48, RULE_HI, 1))
    for k, (name, adds, _, fail) in enumerate(ORDER):
        y = 58 + k * 32; t = .3 + k * .5
        f.show(R(0, y, 700, 26, BG, RULE_HI, 4) + T(14, y + 17, str(k + 1), BR, 'start', mono=True, bold=True) +
               T(40, y + 17, name, TX, 'start', cls='sv-s', bold=True), t)
        f.show(T(260, y + 17, fail, RD, 'start', cls='sv-s'), t + .15)
        f.show(T(420, y + 17, adds, GR, 'start', cls='sv-s') + T(680, y + 18, '✓', GR, mono=True, bold=True), t + .3)
    return finish(f, 58 + 7 * 32 + 6)

SCRIPT = re.search(r'<script>.*?</script>', dt.BODY, re.S).group(0)
def link(i): return '<a href="%s">%s</a>' % (ORDER[i][2], ORDER[i][0])

BODY = r'''<header class="hero">
  <p class="eyebrow">Deep learning · Neural network</p>
  <h1>Neural network <em>overview</em></h1>
  <p class="lede">A deep network is neurons in layers plus six fixes, each one patching the failure that appears as the network gets deeper.</p>
</header>

<section id="nnov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Numbers enter on the left, are <em>weighted, summed and bent</em> in each layer, and leave as one prediction.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>h</var></span><em>next layer</em></span>
      <span class="op">=</span>
      <span class="t p"><span><var>φ</var></span><em>activation</em></span>
      <span class="op">(</span>
      <span class="t b"><span><var>W</var><var>x</var> + <var>b</var></span><em>weighted sum of the layer before</em></span>
      <span class="op">)</span>
    </div>
  </div>
{f1}
  <ul class="why">
    <li>The same 2-2-1 network on XOR runs through every figure below; the deeper figures stack 8 such layers, 32 neurons wide.</li>
    <li>Training = change the weights until the loss is small. Each subsection below removes one piece and shows what breaks.</li>
  </ul>
</section>

<section id="nnov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>What breaks without each piece</h2></div>
  <p class="key">Take one piece away and the network fails <em>in its own visible way</em>; that failure is why the piece exists.</p>
  <div class="subsec" id="nnov-s2-1">
    <h3 class="ssh"><b>2.1</b>Neurons in layers</h3>
    <p class="skey">One neuron draws <em>one straight line</em>, and XOR cannot be split by one line.</p>
{f2}
    <ul class="why"><li>Full lesson: {l0}.</li></ul>
  </div>
  <div class="subsec" id="nnov-s2-2">
    <h3 class="ssh"><b>2.2</b>Nonlinearity</h3>
    <p class="skey">Without an activation, layers of weighted sums <em>multiply into one</em>, so depth buys nothing.</p>
{f3}
    <ul class="why"><li>Full lesson: {l1}.</li></ul>
  </div>
  <div class="subsec" id="nnov-s2-3">
    <h3 class="ssh"><b>2.3</b>Gradient flow</h3>
    <p class="skey">Learning needs the gradient of every weight; nudging them one by one costs <em>one pass per weight</em>.</p>
{f4}
    <ul class="why"><li>A real model has millions of weights; backprop still needs one backward pass. Full lesson: {l2}.</li></ul>
  </div>
  <div class="subsec" id="nnov-s2-4">
    <h3 class="ssh"><b>2.4</b>Starting scale</h3>
    <p class="skey">Weights that start too small shrink the signal <em>layer after layer</em> until nothing reaches the end.</p>
{f5}
    <ul class="why"><li>Gradients shrink the same way on the way back, so early layers stop learning. Full lesson: {l3}.</li></ul>
  </div>
  <div class="subsec" id="nnov-s2-5">
    <h3 class="ssh"><b>2.5</b>Stable activations</h3>
    <p class="skey">With ReLU and slightly large weights the signal <em>doubles every layer</em>; rescaling each layer holds it steady.</p>
{f6}
    <ul class="why"><li>The green run rescales each row of activations to mean 0, std 1 before ReLU. Full lesson: {l4}.</li></ul>
  </div>
  <div class="subsec" id="nnov-s2-6">
    <h3 class="ssh"><b>2.6</b>Good steps</h3>
    <p class="skey">Gradients give the direction; the <em>step size</em> decides whether training crawls, converges or blows up.</p>
{f7}
    <ul class="why"><li>Momentum and Adam adapt the step per weight. Full lesson: {l5}.</li></ul>
  </div>
  <div class="subsec" id="nnov-s2-7">
    <h3 class="ssh"><b>2.7</b>No memorising</h3>
    <p class="skey">A big network on little data <em>memorises the noise</em>: training error falls while error on new data rises.</p>
{f8}
    <ul class="why"><li>Dropout switches off random neurons each step so no single one can memorise. Full lesson: {l6}.</li></ul>
  </div>
</section>

<section id="nnov-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Learning order</h2></div>
  <p class="key">Read the lessons <em>in the order the failures appear</em>.</p>
{f9}
  <ul class="why">
    <li>{l0} → {l1} → {l2} → {l3} → {l4} → {l5} → {l6}.</li>
    <li>Next group: <a href="../../04-cnn/convolution-basics/index.html">Convolution</a>.</li>
  </ul>
</section>

{script}

<footer>Deep learning · Neural network · next lesson in the group: <a href="../perceptron-mlp/index.html">Perceptron &amp; MLP</a>.</footer>
'''

def build():
    figs = dict(
        f1=fig_mental(), f2=fig_line(), f3=fig_act(), f4=fig_grad(),
        f5=fig_layers('nno5-', INIT_BAD, INIT_OK, 'weights std 0.05 · fades to 0', 'std 1/√n (Xavier) · stays alive',
                      'TANH · 8 LAYERS · ONLY THE STARTING WEIGHT SCALE DIFFERS',
                      'Eight tanh layers, 32 neurons wide, 64 random inputs. Bars grow layer by layer. With weights drawn at '
                      'std 0.05 the spread of activations falls from %.2f to %.0e by layer 8. With std 1/sqrt(32) it stays '
                      'between %.2f and %.2f.' % (INIT_BAD[0], INIT_BAD[-1], min(INIT_OK), max(INIT_OK)), 1e-5, 10),
        f6=fig_layers('nno6-', NORM_BAD, NORM_OK, 'ReLU · std 0.5 · explodes', 'same + rescale each layer',
                      'RELU · 8 LAYERS · WITH AND WITHOUT RESCALING EACH LAYER',
                      'Eight ReLU layers with weights at std 0.5. Without rescaling the spread grows from %.2f to %.0f by '
                      'layer 8. Rescaling each layer to mean 0 and std 1 keeps it near %.2f in every layer.' % (
                          NORM_BAD[0], NORM_BAD[-1], NORM_OK[-1]), .1, 1000),
        f7=fig_lr(), f8=fig_drop(), f9=fig_order(), script=SCRIPT)
    figs.update({'l%d' % i: link(i) for i in range(7)})
    return re.sub(r'\{(f\d|l\d|script)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">'); b = s.index('</article>')
    s = s[:a] + body + '      ' + s[b:]
    s = re.sub(r'<article class="doc"[^>]*>', lambda m: re.sub(r' data-(skeleton|reviewed|progress)="\d"', '', m.group(0)), s, count=1)
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s" data-progress="1"' % blurb, s, count=1)
    open(page, 'w').write(s)

if __name__ == '__main__':
    splice(PAGE, build(), 'One tiny network made deeper step by step: what breaks without layers, activation, backprop, '
           'initialization, normalization, a good optimizer and dropout, and the order to learn them.')
