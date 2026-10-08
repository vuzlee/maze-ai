# -*- coding: utf-8 -*-
"""Figures + body for content/08-deep-learning/02-neural-network/dropout-regularization.
One small tanh network (2-6-6-1, sigmoid output) trained in pure Python with full-batch gradient descent on 24 noisy
points of two interleaved moons (fixed seeds), checked on 200 new points. Every number in a figure comes from these
runs and is pinned with assert. Run: python3 dropout_regularization.py"""
import os, re, sys, math, random, copy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import decision_tree as dt
from linear_algebra import Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, BR, VI, FI, RO, RULE, BG, SUNK, S, dot, poly, finish
from tablefig import GR, AM, RD

PAGE = os.path.join(HERE, '../../../content/08-deep-learning/02-neural-network/dropout-regularization/index.html')
_RGB = {GR: '--green-a', RD: '--red-a', AM: '--amber-a', FI: '--blue-a', VI: '--violet-a', BR: '--clay-a'}
def tn(c, a='.14'): return 'rgba(var(%s),%s)' % (_RGB[c], a)

# ---------- data: two noisy moons ----------
def make(n, seed):
    g = random.Random(seed); P = []
    for i in range(n):
        c = i % 2; t = g.uniform(0, math.pi)
        x, y = (math.cos(t), math.sin(t)) if c == 0 else (1 - math.cos(t), .5 - math.sin(t))
        x += g.gauss(0, .25); y += g.gauss(0, .25)
        P.append(((x + 1) / 3, (y + .75) / 2, 1 - c))
    return P
TR, VA = make(24, 1), make(200, 2)
H = 6

# ---------- the network ----------
def init(seed=3):
    g = random.Random(seed)
    return [[[g.gauss(0, 1) for _ in range(2)] for _ in range(H)], [0.] * H,
            [[g.gauss(0, 1 / math.sqrt(H)) for _ in range(H)] for _ in range(H)], [0.] * H,
            [g.gauss(0, 1 / math.sqrt(H)) for _ in range(H)], 0.]
def sig(z): return 1 / (1 + math.exp(-max(-30, min(30, z))))
def fwd(p, x, m1=None, m2=None):
    W1, b1, W2, b2, w3, b3 = p
    a1 = [math.tanh(W1[j][0] * x[0] + W1[j][1] * x[1] + b1[j]) for j in range(H)]
    h1 = [a * m for a, m in zip(a1, m1)] if m1 else a1
    a2 = [math.tanh(sum(W2[k][j] * h1[j] for j in range(H)) + b2[k]) for k in range(H)]
    h2 = [a * m for a, m in zip(a2, m2)] if m2 else a2
    return a1, h1, a2, h2, sig(sum(a * b for a, b in zip(w3, h2)) + b3)
def loss(p, P):
    s = 0
    for q in P:
        o = min(max(fwd(p, q)[4], 1e-9), 1 - 1e-9); s -= q[2] * math.log(o) + (1 - q[2]) * math.log(1 - o)
    return s / len(P)
def acc(p, P): return sum((fwd(p, q)[4] > .5) == q[2] for q in P) / len(P)
def sqw(p): return sum(w * w for r in p[0] + p[2] for w in r) + sum(w * w for w in p[4])
def step(p, P, lr, wd=0., pd=0., g=None):
    W1, b1, W2, b2, w3, b3 = p
    G = [[[0, 0] for _ in range(H)], [0] * H, [[0] * H for _ in range(H)], [0] * H, [0] * H, 0]
    for q in P:
        m1 = m2 = None
        if pd:
            m1 = [(g.random() >= pd) / (1 - pd) for _ in range(H)]; m2 = [(g.random() >= pd) / (1 - pd) for _ in range(H)]
        a1, h1, a2, h2, o = fwd(p, q, m1, m2); d = o - q[2]
        for k in range(H): G[4][k] += d * h2[k]
        G[5] += d
        d2 = [d * w3[k] * (m2[k] if m2 else 1) * (1 - a2[k] ** 2) for k in range(H)]
        for k in range(H):
            G[3][k] += d2[k]
            for j in range(H): G[2][k][j] += d2[k] * h1[j]
        d1 = [sum(d2[k] * W2[k][j] for k in range(H)) * (m1[j] if m1 else 1) * (1 - a1[j] ** 2) for j in range(H)]
        for j in range(H):
            G[1][j] += d1[j]; G[0][j][0] += d1[j] * q[0]; G[0][j][1] += d1[j] * q[1]
    n = len(P)
    for j in range(H):
        for i in range(2): W1[j][i] -= lr * (G[0][j][i] / n + wd * W1[j][i])
        b1[j] -= lr * G[1][j] / n
        for i in range(H): W2[j][i] -= lr * (G[2][j][i] / n + wd * W2[j][i])
        b2[j] -= lr * G[3][j] / n; w3[j] -= lr * (G[4][j] / n + wd * w3[j])
    p[5] -= lr * G[5] / n
def run(p, ep, lr=1.0, wd=0., pd=0., every=20, snaps=()):
    g = random.Random(103); hist, S_ = [], {}
    for e in range(ep + 1):
        if e % every == 0: hist.append((e, loss(p, TR), loss(p, VA)))
        if e in snaps: S_[e] = copy.deepcopy(p)
        if e == ep: break
        step(p, TR, lr, wd, pd, g)
    return hist, S_

EP = 1500
HIST, SN = run(init(), EP, snaps=(40, 1500))          # plain network: memorises
DHIST, DSN = run(init(), EP, pd=.5, snaps=(1500,))    # dropout 0.5
BEST = min(HIST, key=lambda r: r[2])
assert BEST[0] == 40 and round(BEST[2], 3) == .301 and round(HIST[-1][1], 3) == .061 and round(HIST[-1][2], 3) == .817
assert round(acc(SN[1500], TR), 3) == .917 and acc(SN[1500], VA) == .845 and acc(SN[40], VA) == .885
assert round(DHIST[-1][2], 3) == .398 and acc(DSN[1500], VA) == .89
# early stopping, patience 200 epochs (10 checks of 20)
PAT = 200
def early(h):
    best, bi = 1e9, 0
    for i, (e, a, v) in enumerate(h):
        if v < best: best, bi = v, i
        elif e - h[bi][0] >= PAT: return bi, i
ES_BEST, ES_STOP = early(HIST); assert HIST[ES_BEST][0] == 40 and HIST[ES_STOP][0] == 240
# weight decay: continue the memorising network with lambda = 0.01 and watch ||w||^2 shrink
WD = .01
WP = copy.deepcopy(SN[1500]); WSN = [(0, copy.deepcopy(WP))]
for k in range(1, 5):
    for _ in range(100): step(WP, TR, 1.0, WD)
    WSN.append((100 * k, copy.deepcopy(WP)))
WROW = [(e, sqw(p), loss(p, VA), acc(p, VA)) for e, p in WSN]
assert [round(r[1]) for r in WROW] == [200, 44, 24, 21, 20] and round(WROW[-1][2], 3) == .292
# dropout masks for 2.1: three training steps on one row
X0 = TR[0]; DP = DSN[1500]
MG = random.Random(7)
MASKS = []
for _ in range(3):
    m1 = [(MG.random() >= .5) * 2 for _ in range(H)]; m2 = [(MG.random() >= .5) * 2 for _ in range(H)]
    MASKS.append((m1, m2, fwd(DP, X0, m1, m2)))
assert [round(m[2][4], 2) for m in MASKS] == [.30, .04, .21]
OUT_EVAL = fwd(DP, X0)[4]; assert round(OUT_EVAL, 2) == .04

# ---------- drawing helpers ----------
def pt(x, y, c, r=4.5):
    if c: return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, FI)
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1.8"/>' % (x, y, r - .6, BG, BR)
class Box:
    """data square x in [-.15,1.2], y in [-.2,1.1] -> a px x px panel"""
    def __init__(s, x, y, w=180, h=170): s.x, s.y, s.w, s.h = x, y, w, h
    def X(s, v): return s.x + (v + .15) / 1.35 * s.w
    def Y(s, v): return s.y + s.h - (v + .2) / 1.3 * s.h
    def frame(s): return R(s.x, s.y, s.w, s.h, 'none', RULE_HI, 4, 1)
    def shade(s, p, n=24):
        o = ''
        cw, ch = s.w / n, s.h / n
        for i in range(n):
            for j in range(n):
                x = -.15 + (i + .5) / n * 1.35; y = -.2 + (j + .5) / n * 1.3
                c = fwd(p, (x, y))[4] > .5
                o += R(s.x + i * cw, s.y + s.h - (j + 1) * ch, cw + .3, ch + .3, BG, 'none', 0)
                o += R(s.x + i * cw, s.y + s.h - (j + 1) * ch, cw + .3, ch + .3, tn(FI, '.16') if c else tn(BR, '.10'), 'none', 0)
        return o
    def points(s, P=TR): return ''.join(pt(s.X(q[0]), s.Y(q[1]), q[2]) for q in P)
def axes(x0, y0, w, h, ym, xlab, ylab):
    s = L(x0, y0 + h, x0 + w, y0 + h, RULE_HI, 1) + L(x0, y0, x0, y0 + h, RULE_HI, 1)
    for v in (0, .2, .4, .6, .8, 1.0):
        if v <= ym: s += T(x0 - 6, y0 + h - v / ym * h + 3.5, '%g' % v, FA, 'end', mono=True) + L(x0, y0 + h - v / ym * h, x0 + w, y0 + h - v / ym * h, RULE, .7)
    return s + T(x0, y0 - 8, ylab, MU, 'start', cls='sv-d') + T(x0 + w, y0 + h + 16, xlab, FA, 'end', cls='sv-d')
def grow(f, pts, c, t0, dur, K=10):
    """a curve built segment by segment with a dot riding its tip"""
    n = len(pts); seg = dur / K
    for k in range(K):
        a, b = round(k * (n - 1) / K), round((k + 1) * (n - 1) / K)
        f.show(poly(pts[a:b + 1], c, 2), t0 + k * seg, d=seg)
    ex, ey = pts[-1]
    f.path(dot(ex, ey, c, 4), [(0, pts[0][0] - ex, pts[0][1] - ey)] +
           [(t0 + k * seg, pts[round((k + 1) * (n - 1) / K)][0] - ex, pts[round((k + 1) * (n - 1) / K)][1] - ey) for k in range(K)], t0, d=seg)
def ring(x, y, c, r=9): return '<circle cx="%.1f" cy="%.1f" r="%s" fill="none" stroke="%s" stroke-width="2"/>' % (x, y, r, c)

# network layout 2-6-6-1
NX = [30, 140, 250, 350]; NY0, NSP = 60, 36
def npos(l, i):
    n = (2, H, H, 1)[l]; return NX[l], NY0 + (H - 1) * NSP / 2 + (i - (n - 1) / 2) * NSP
def neuron(x, y, c=RULE_HI, fill=BG, dash=None, r=15):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<circle cx="%.1f" cy="%.1f" r="%d" fill="%s" stroke="%s" stroke-width="1.6"%s/>' % (x, y, r, fill, c, d)
def net_edges(p, on1=None, on2=None, c=RULE_HI, scale=.9):
    s = ''
    W1, _, W2, _, w3, _ = p
    for j in range(H):
        for i in range(2):
            if on1 is None or on1[j]:
                (x1, y1), (x2, y2) = npos(0, i), npos(1, j); s += L(x1 + 15, y1, x2 - 15, y2, c, min(.3 + abs(W1[j][i]) * scale * .35, 5))
    for k in range(H):
        for j in range(H):
            if (on1 is None or on1[j]) and (on2 is None or on2[k]):
                (x1, y1), (x2, y2) = npos(1, j), npos(2, k); s += L(x1 + 15, y1, x2 - 15, y2, c, min(.3 + abs(W2[k][j]) * scale * .35, 5))
    for k in range(H):
        if on2 is None or on2[k]:
            (x1, y1), (x2, y2) = npos(2, k), npos(3, 0); s += L(x1 + 15, y1, x2 - 15, y2, c, min(.3 + abs(w3[k]) * scale * .35, 5))
    return s
def net_nodes(on1=None, on2=None):
    s = ''
    for l, on in ((0, None), (1, on1), (2, on2), (3, None)):
        for i in range((2, H, H, 1)[l]):
            x, y = npos(l, i)
            s += neuron(x, y, FA, BG, '3 3') if on is not None and not on[i] else neuron(x, y)
    return s
def fmt(v): return ('%.1f' % v).replace('-', '−').replace('−0.0', '0.0')

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('drop1-', 720, 0, 'A 2-6-6-1 network trained on 24 noisy points, checked on 200 new points. The loss curves grow '
             'epoch by epoch: training loss falls to %.3f, validation loss is lowest at epoch %d (%.3f) and then climbs to '
             '%.3f. The decision regions on the left change from a smooth curve at epoch 40 to a wiggly border that wraps '
             'around single noisy points by epoch 1500.' % (HIST[-1][1], BEST[0], BEST[2], HIST[-1][2]),
             'TRAIN LOSS ↓ · VALIDATION LOSS ↓ THEN ↑ · BORDER WRAPS THE NOISE')
    B = Box(0, 44, 200, 190)
    f.show(B.shade(SN[40]), .3, hide=4.4)
    f.show(B.shade(SN[1500]), 4.4)
    f.static(B.frame() + B.points())
    f.show(S(0, 254, 'epoch 40 · smooth border', GR, bold=True), .5, hide=4.4)
    f.show(S(0, 254, 'epoch 1500 · wraps single points', RD, bold=True), 4.6)
    x0, y0, w, h, ym = 290, 54, 300, 170, 1.0
    f.static(axes(x0, y0, w, h, ym, 'epoch 0 → 1500', 'loss'))
    px = lambda e: x0 + e / EP * w; py = lambda v: y0 + h - min(v, ym) / ym * h
    grow(f, [(px(e), py(a)) for e, a, v in HIST], FI, .6, 4.2)
    grow(f, [(px(e), py(v)) for e, a, v in HIST], VI, .6, 4.2)
    f.show(S(px(EP) + 8, py(HIST[-1][1]) + 4, 'train %.3f' % HIST[-1][1], FI, bold=True), 4.9)
    f.show(S(px(EP) + 8, py(HIST[-1][2]) + 4, 'val %.3f' % HIST[-1][2], VI, bold=True), 4.9)
    f.show(ring(px(BEST[0]), py(BEST[2]), GR) + S(px(BEST[0]) + 14, py(BEST[2]) + 22, 'best: epoch %d · %.3f' % BEST[::2], GR, bold=True), 5.3)
    f.show(S(x0, 262, 'accuracy: train %.1f%% · new points %.1f%%' % (100 * acc(SN[1500], TR), 100 * acc(SN[1500], VA)), RD, bold=True), 5.7)
    return finish(f, 272)

# ---------- 2.1 / 2.2 Dropout at training / inference ----------
def fig_train():
    f = Anim('drop2-', 720, 0, 'The same network on one training row, three training steps with dropout p = 0.5. At each step '
             'a new random mask switches off about half of the hidden neurons: they turn dashed and their edges vanish. Each '
             'surviving activation is multiplied by 1 / (1 − p) = 2. The output changes from step to step: %s.' %
             ', '.join('%.2f' % m[2][4] for m in MASKS), 'EACH STEP · A NEW RANDOM MASK · SURVIVORS × 1/(1−p) = 2')
    f.static(T(NX[0], 30, 'x', MU, cls='sv-d') + T(NX[1], 30, 'hidden 1', MU, cls='sv-d') +
             T(NX[2], 30, 'hidden 2', MU, cls='sv-d') + T(NX[3], 30, 'p', MU, cls='sv-d'))
    TS = [.4, 3.0, 5.6]
    for k, (m1, m2, out) in enumerate(MASKS):
        t, e = TS[k], (TS[k + 1] if k < 2 else None)
        f.show(net_edges(DP, m1, m2), t + .5, hide=e)
        f.show(net_nodes(m1, m2), t, hide=e)
        a1, h1, a2, h2, o = out
        g = ''
        for l, (A, Hh, m) in ((1, (a1, h1, m1)), (2, (a2, h2, m2))):
            for i in range(H):
                x, y = npos(l, i)
                if m[i]: g += T(x, y + 3.5, fmt(Hh[i]), FI, mono=True, bold=True)
                else: g += T(x, y + 3.5, '0', FA, mono=True)
        f.show(g, t + 1.1, hide=e)
        ox, oy = npos(3, 0)
        f.show(neuron(ox, oy, AM, tn(AM, '.14'), r=17) + T(ox, oy + 3.5, '%.2f' % o, AM, mono=True, bold=True), t + 1.6, hide=e)
        y = 60 + k * 62
        f.show(R(420, y, 290, 50, BG, RULE_HI, 6) + T(434, y + 20, 'step %d' % (k + 1), TX, 'start', cls='sv-s', bold=True) +
               T(434, y + 38, 'off: %d + %d of 12 · ×2 on the rest' % (m1.count(0), m2.count(0)), MU, 'start', cls='sv-d') +
               T(700, y + 30, 'p = %.2f' % o, AM, 'end', mono=True, bold=True), t + 1.6)
    for i, (x0, y0) in enumerate([npos(0, 0), npos(0, 1)]):
        f.static(T(x0, y0 + 3.5, '%.2f' % X0[i], TX, mono=True))
    f.show(S(420, 270, 'a different thinned network every step', MU), 7.6)
    return finish(f, 290)

def fig_eval():
    a1, h1, a2, h2, o = fwd(DP, X0)
    f = Anim('drop3-', 720, 0, 'The same trained network on the same row at inference. Every neuron is on, no mask and no '
             'scaling; the activations flow layer by layer and the output is %.2f, the same every time it is run.' % o,
             'INFERENCE · ALL NEURONS ON · NO SCALING · SAME ANSWER EVERY TIME')
    f.static(T(NX[0], 30, 'x', MU, cls='sv-d') + T(NX[1], 30, 'hidden 1', MU, cls='sv-d') +
             T(NX[2], 30, 'hidden 2', MU, cls='sv-d') + T(NX[3], 30, 'p', MU, cls='sv-d'))
    f.show(net_edges(DP), .4)
    f.static(net_nodes())
    for i, (x0, y0) in enumerate([npos(0, 0), npos(0, 1)]):
        f.static(T(x0, y0 + 3.5, '%.2f' % X0[i], TX, mono=True))
    for l, A in ((1, a1), (2, a2)):
        f.show(''.join(T(npos(l, i)[0], npos(l, i)[1] + 3.5, fmt(A[i]), FI, mono=True, bold=True) for i in range(H)), .6 + l * .7)
    ox, oy = npos(3, 0)
    f.show(neuron(ox, oy, GR, tn(GR, '.14'), r=17) + T(ox, oy + 3.5, '%.2f' % o, GR, mono=True, bold=True), 2.4)
    for k in range(3):
        y = 60 + k * 62
        f.show(R(420, y, 290, 50, BG, RULE_HI, 6) + T(434, y + 20, 'run %d' % (k + 1), TX, 'start', cls='sv-s', bold=True) +
               T(434, y + 38, 'off: 0 of 12 · no scaling', MU, 'start', cls='sv-d') +
               T(700, y + 30, 'p = %.2f' % o, GR, 'end', mono=True, bold=True), 2.8 + k * .5)
    f.show(S(420, 270, 'model.eval() — one fixed network', MU), 4.4)
    return finish(f, 290)

# ---------- 03 Weight decay ----------
def fig_wd():
    f = Anim('drop4-', 720, 0, 'The memorising network from section 01 keeps training, now with weight decay lambda = 0.01. '
             'Every 100 steps the edges get thinner and the sum of squared weights falls: %s. The border on the right '
             'loses its wiggles and validation loss falls from %.3f to %.3f.' % (
                 ', '.join('%.0f' % r[1] for r in WROW), WROW[0][2], WROW[-1][2]),
             'EACH STEP SHRINKS EVERY WEIGHT A LITTLE · THE BORDER SMOOTHS')
    TS = [.3 + k * 1.4 for k in range(5)]
    B = Box(420, 44, 200, 190)
    for k, (e, p) in enumerate(WSN):
        hide = TS[k + 1] if k < 4 else None
        f.show(net_edges(p, c=tn(FI, '.55'), scale=2.4), TS[k], hide=hide)
        f.show(B.shade(p, 20), TS[k], hide=hide)
    f.static(net_nodes() + B.frame() + B.points())
    f.static(T(14, 282, 'steps', MU, 'start', cls='sv-d') + T(14, 300, '‖w‖²', MU, 'start', cls='sv-d') +
             T(14, 318, 'val loss', MU, 'start', cls='sv-d'))
    for k, (e, w2, vl, ac) in enumerate(WROW):
        x = 110 + k * 60
        f.show(T(x, 282, '+%d' % e, TX, mono=True) + T(x, 300, '%.0f' % w2, AM if k < 4 else GR, mono=True, bold=True) +
               T(x, 318, '%.3f' % vl, VI, mono=True), TS[k] + .2)
    f.show(S(420, 258, 'λ = 0.01 · val accuracy %.1f%% → %.1f%%' % (100 * WROW[0][3], 100 * WROW[-1][3]), GR, bold=True), TS[4] + .4)
    return finish(f, 328)

# ---------- 04 Early stopping ----------
def fig_early():
    f = Anim('drop5-', 720, 0, 'Validation loss checked every 20 epochs. The best value so far is held in a box; it improves '
             'until epoch %d (%.3f). The patience counter then runs for %d epochs without improvement; at epoch %d training '
             'stops and the weights saved at epoch %d are restored.' % (HIST[ES_BEST][0], HIST[ES_BEST][2], PAT,
                                                                       HIST[ES_STOP][0], HIST[ES_BEST][0]),
             'KEEP THE BEST CHECKPOINT · STOP AFTER 200 EPOCHS WITHOUT GAIN')
    h = HIST[:ES_STOP + 1]
    x0, y0, w, hh, ym = 50, 50, 380, 190, .8
    em = h[-1][0]
    f.static(axes(x0, y0, w, hh, ym, 'epoch 0 → %d' % em, 'validation loss'))
    px = lambda e: x0 + e / em * w; py = lambda v: y0 + hh - min(v, ym) / ym * hh
    best = 1e9; t = .4; dt_ = .35
    for i, (e, a, v) in enumerate(h):
        ti = t + i * dt_
        seg = L(px(h[i - 1][0]), py(h[i - 1][2]), px(e), py(v), VI, 2) if i else ''
        f.show(seg + dot(px(e), py(v), VI, 3.5), ti, d=.25)
    # best-so-far marker gliding to each new best
    bests = []
    for i, (e, a, v) in enumerate(h):
        if v < best: best = v; bests.append(i)
    be = h[bests[-1]]
    f.path(ring(px(be[0]), py(be[2]), GR), [(0, px(h[0][0]) - px(be[0]), py(h[0][2]) - py(be[2]))] +
           [(t + i * dt_, px(h[i][0]) - px(be[0]), py(h[i][2]) - py(be[2])) for i in bests[1:]], t, d=.25)
    f.static(T(470, 64, 'best so far', MU, 'start', cls='sv-d') + T(470, 124, 'epochs without gain', MU, 'start', cls='sv-d'))
    best = 1e9; bi = 0
    for i, (e, a, v) in enumerate(h):
        ti = t + i * dt_; nx = t + (i + 1) * dt_ if i < len(h) - 1 else None
        if v < best:
            best, bi = v, i
            f.show(R(470, 72, 200, 28, BG, GR, 5, 1.4) + T(480, 91, 'epoch %d · %.3f' % (e, v), GR, 'start', mono=True, bold=True),
                   ti, hide=t + (bests[bests.index(i) + 1]) * dt_ if bi != bests[-1] else None, d=.2)
        f.show(R(470, 132, 200, 28, BG, RULE_HI, 5) + T(480, 151, '%d / %d' % (e - h[bi][0], PAT),
               RD if e - h[bi][0] >= PAT else AM, 'start', mono=True, bold=True), ti, hide=nx, d=.15)
    te = t + len(h) * dt_
    f.show(L(px(em), y0, px(em), y0 + hh, RD, 1.6, '5 4') + T(px(em) - 4, y0 + 12, 'stop', RD, 'end', cls='sv-s', bold=True), te)
    f.path(R(0, 0, 150, 26, tn(GR, '.14'), GR, 5, 1.4) + T(75, 17, 'weights of epoch %d' % be[0], GR, mono=True, bold=True),
           [(te + .4, px(be[0]) - 20, py(be[2]) - 50), (te + .9, 470, 200)], te + .4, d=.8)
    f.show(T(470, 246, 'restored → final model', GR, 'start', cls='sv-s', bold=True), te + 1.8)
    return finish(f, 272)

# ---------- 05 Data augmentation ----------
IMG = ['.....', '.###.', '.#...', '.##..', '.#...', '.....']  # a small "F" on a 5x6 grid
IMG = [r + '.' for r in IMG]
def flip(g): return [r[::-1] for r in g]
def shift(g, dx): return [('.' * dx + r)[:len(r)] for r in g]
def crop(g):  # cut a 4x5 window and blow it back to 6x6 by nearest neighbour
    sub = [r[1:5] for r in g[1:6]]
    return [''.join(sub[min(int(i * 5 / 6), 4)][min(int(j * 4 / 6), 3)] for j in range(6)) for i in range(6)]
AUG = [('original', IMG), ('flip', flip(IMG)), ('shift +1', shift(IMG, 1)), ('crop + resize', crop(IMG))]
assert all(len(g) == 6 and all(len(r) == 6 for r in g) for _, g in AUG)
assert sum(r.count('#') for r in IMG) == 7 and AUG[1][1][1] == '..###.' and AUG[2][1][1] == '..###.'
def grid(x, y, g, c=FI, u=11):
    s = R(x - 1, y - 1, 6 * u + 2, 6 * u + 2, BG, RULE_HI, 3, 1)
    for i, r in enumerate(g):
        for j, ch in enumerate(r):
            if ch == '#': s += R(x + j * u, y + i * u, u, u, c, 'none', 1)
            else: s += R(x + j * u, y + i * u, u, u, SUNK, RULE, 0, .4)
    return s
def fig_aug():
    f = Anim('drop6-', 720, 0, 'One labelled image, a letter F on a 6 by 6 grid, is copied three times. One copy is flipped, '
             'one shifted right by one pixel, one cropped and resized. Each copy slides into the training table as a new '
             'row with the same label F, so one example becomes four.', 'ONE IMAGE → MANY TRAINING ROWS · SAME LABEL')
    f.static(T(20, 40, 'source', MU, 'start', cls='sv-d'))
    f.static(grid(20, 52, IMG))
    f.static(T(300, 40, 'training rows', MU, 'start', cls='sv-d') + T(410, 40, 'transform', MU, 'start', cls='sv-d') +
             T(560, 40, 'label', MU, 'start', cls='sv-d') + L(300, 46, 640, 46, RULE_HI, 1))
    for k, (name, g) in enumerate(AUG):
        y = 54 + k * 80; t0 = .4 + k * 1.3
        if k == 0: f.path(grid(300, y, g), [(0, 20 - 300, 52 - y), (t0 + .4, 0, 0)], t0, d=.8)
        else:
            f.path(grid(300, y, IMG), [(0, 20 - 300, 52 - y), (t0 + .4, 0, 0)], t0, d=.8, hide=t0 + 1.2)
            f.show(grid(300, y, g, VI), t0 + 1.3)
        f.show(T(410, y + 38, name, TX if k == 0 else VI, 'start', cls='sv-s', bold=True), t0 + 1.0)
        f.show(R(560, y + 24, 30, 22, tn(GR, '.14'), GR, 5, 1.2) + T(575, y + 39, 'F', GR, mono=True, bold=True), t0 + 1.1)
    f.show(S(20, 160, '1 labelled image', MU) + S(20, 178, '→ 4 rows, all label F', GR, bold=True), 5.8)
    return finish(f, 54 + 4 * 80)

# ---------- 06 Label smoothing ----------
LS_EPS = .1; LS_K = 3
LS_T = [LS_EPS / LS_K + (1 - LS_EPS) * (1 if k == 2 else 0) for k in range(LS_K)]
assert [round(v, 3) for v in LS_T] == [.033, .033, .933]
def fig_ls():
    f = Anim('drop7-', 720, 0, 'A one-hot target for three classes, cat 0, dog 0, fox 1. With label smoothing epsilon = 0.1 '
             'the bars move to 0.033, 0.033 and 0.933: the model is no longer pushed to an infinitely confident output.',
             'TARGET 1 / 0 → 0.933 / 0.033 · ε = 0.1 SPREAD OVER THE CLASSES')
    names = ['cat', 'dog', 'fox']; yb, hh = 210, 150
    f.static(L(40, yb, 400, yb, RULE_HI, 1.2))
    for k in range(3):
        x = 70 + k * 110
        f.static(T(x + 30, yb + 18, names[k], MU, cls='sv-s'))
        hard = 1 if k == 2 else 0
        # bar drawn at its smoothed height; scale from the hard height via a gliding cap
        f.show(R(x, yb - hard * hh, 60, max(hard * hh, 1), tn(RD, '.18'), RD, 2, 1.2) +
               T(x + 30, yb - hard * hh - 6, '%d' % hard, RD, mono=True, bold=True), .3, hide=2.4)
        v = LS_T[k]
        f.show(R(x, yb - v * hh, 60, v * hh, tn(GR, '.18'), GR, 2, 1.2) + T(x + 30, yb - v * hh - 6, '%.3f' % v, GR, mono=True, bold=True), 2.4, d=.8)
    f.show(S(450, 80, 'one-hot target', RD, bold=True) + S(450, 98, 'loss keeps pushing fox → 1', MU), .5)
    f.show(S(450, 140, 'smoothed, ε = 0.1', GR, bold=True) + S(450, 158, '(1 − ε)·one-hot + ε / K', MU), 2.6)
    return finish(f, 236)

SCRIPT = re.search(r'<script>.*?</script>', dt.BODY, re.S).group(0)

BODY = r'''<header class="hero">
  <p class="eyebrow">Deep learning · Neural network</p>
  <h1>Dropout &amp; <em>regularization</em></h1>
  <p class="lede">A network big enough to learn the pattern is big enough to memorise the noise, so training adds a few deliberate handicaps.</p>
</header>

<section id="drop-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Training loss keeps falling while <em>validation loss turns back up</em>: the network has started memorising.</p>
{f1}
  <ul class="why">
    <li>The general idea — overfitting, bias–variance, why fewer effective parameters help — is in <a href="../../../07-machine-learning/04-core-concepts/overfitting-regularization/index.html">Overfitting &amp; regularization</a>; this lesson is the deep-learning toolbox.</li>
    <li>Every tool below makes memorising harder: <b>noise in the network</b> (dropout), <b>small weights</b> (weight decay), <b>less time</b> (early stopping), <b>more data</b> (augmentation).</li>
  </ul>
</section>

<section id="drop-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Dropout</h2></div>
  <p class="key">Switch off random neurons <em>only while training</em>; at inference use the whole network.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>h̃</var></span><em>what the next layer sees</em></span>
      <span class="op">=</span>
      <span class="t"><span><span class="frac"><i><var>m</var> ⊙ <var>h</var></i><i>1 − <var>p</var></i></span></span><em>m ~ Bernoulli(1 − p) per neuron</em></span>
    </div>
  </div>

  <div class="subsec" id="drop-s2-1">
    <h3 class="ssh"><b>2.1</b>At training</h3>
    <p class="skey">Each step draws a <em>new mask</em>; survivors are scaled by 1/(1 − p) so the expected sum stays the same.</p>
{f2}
    <ul class="why">
      <li>No neuron can rely on one particular partner, so features must work on their own — like training many thinned networks that share weights.</li>
      <li>This is <b>inverted dropout</b>: the scaling happens at training, so inference needs no change. Typical <var>p</var>: 0.1–0.5.</li>
    </ul>
  </div>

  <div class="subsec" id="drop-s2-2">
    <h3 class="ssh"><b>2.2</b>At inference</h3>
    <p class="skey">No mask, <em>no scaling</em>: the full network gives one fixed answer.</p>
{f3}
    <ul class="why">
      <li>The full network approximates the average of all the thinned ones.</li>
      <li>Classic bug: forgetting <code>model.eval()</code> leaves dropout on, and predictions change on every call.</li>
    </ul>
  </div>
</section>

<section id="drop-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Weight decay</h2></div>
  <p class="key">Add a cost for large weights, so every step <em>shrinks each weight a little</em> toward 0.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>L</var><sub>total</sub></span><em>what is minimised</em></span>
      <span class="op">=</span>
      <span class="t"><span><var>L</var><sub>data</sub></span><em>cross-entropy</em></span>
      <span class="op">+</span>
      <span class="t g"><span><span class="frac"><i><var>λ</var></i><i>2</i></span> ‖<var>w</var>‖<sup>2</sup></span><em>L2 penalty</em></span>
    </div>
    <div class="line">
      <span class="t"><span><var>w</var></span><em>update</em></span>
      <span class="op">←</span>
      <span class="t"><span><var>w</var> − <var>η</var> ∇<var>L</var><sub>data</sub></span><em>usual gradient step</em></span>
      <span class="op">−</span>
      <span class="t g"><span><var>η</var> <var>λ</var> <var>w</var></span><em>the decay</em></span>
    </div>
  </div>
{f4}
  <ul class="why">
    <li>Small weights mean a smoother function: a tanh with small inputs is almost linear, so the border cannot bend around single points.</li>
    <li>With plain SGD the two lines are the same thing. With Adam they are not — the penalty gets rescaled per weight — which is why <a href="../../03-optimizer/optimizer-overview/index.html#optim-s4">AdamW</a> applies the decay directly to the weights.</li>
  </ul>
</section>

<section id="drop-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Early stopping</h2></div>
  <p class="key">Watch validation loss, keep the <em>best checkpoint</em>, stop when it has not improved for a while.</p>
{f5}
  <ul class="why">
    <li><b>Patience</b> = how long to wait without improvement; validation loss is noisy, so never stop at the first rise.</li>
    <li>Almost free and works with every other tool; the validation set must not be used for anything else.</li>
  </ul>
</section>

<section id="drop-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Data augmentation</h2></div>
  <p class="key">Make new training rows by <em>transforming old ones</em> in ways that do not change the label.</p>
{f6}
  <ul class="why">
    <li>Images: flip, shift, crop, rotate, colour jitter; text: synonym swap, back-translation; audio: noise, time shift.</li>
    <li>Only transforms the label survives: a flipped cat is a cat, a flipped "6" may be a "9".</li>
    <li>Applied fresh every epoch, so the network rarely sees the exact same input twice.</li>
  </ul>
</section>

<section id="drop-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Label smoothing</h2></div>
  <p class="key">Replace the hard 1/0 target by <em>a little less than 1</em>, so the network stops chasing infinite confidence.</p>
{f7}
  <ul class="why">
    <li>Common in large classifiers and Transformers (ε ≈ 0.1); also tends to improve <a href="../../../07-machine-learning/09-evaluation/calibration/index.html">calibration</a>.</li>
    <li><b>Batch norm</b> also regularises a little: each sample is normalised with statistics of a random mini-batch, which adds noise — see <a href="../normalization/index.html">Normalization</a>.</li>
  </ul>
</section>

{script}

<footer>Deep learning · Neural network · next group: <a href="../../03-optimizer/optimizer-overview/index.html">Optimizer</a>.</footer>
'''

def build():
    figs = dict(f1=fig_mental(), f2=fig_train(), f3=fig_eval(), f4=fig_wd(), f5=fig_early(), f6=fig_aug(), f7=fig_ls(),
                script=SCRIPT)
    return re.sub(r'\{(f\d|script)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">'); b = s.index('</article>')
    s = s[:a] + body + '      ' + s[b:]
    s = re.sub(r'<article class="doc"[^>]*>', lambda m: re.sub(r' data-(skeleton|reviewed|progress)="\d"', '', m.group(0)), s, count=1)
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s" data-progress="1"' % blurb, s, count=1)
    open(page, 'w').write(s)

if __name__ == '__main__':
    print('best', BEST, 'final', HIST[-1], 'drop', DHIST[-1], acc(DSN[1500], VA))
    print('masks', [round(m[2][4], 3) for m in MASKS], 'eval', round(OUT_EVAL, 3))
    print('wd', [(e, round(a, 1), round(b, 3), c) for e, a, b, c in WROW], 'es', HIST[ES_BEST][0], HIST[ES_STOP][0])
    splice(PAGE, build(), 'Dropout at training vs inference, weight decay, early stopping, data augmentation and label '
           'smoothing on one small network that memorises noise.')
