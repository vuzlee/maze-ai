# -*- coding: utf-8 -*-
"""Figures + body for content/08-deep-learning/02-neural-network/backpropagation.
Every number is computed here: a tiny computational graph, a 2-2-1 sigmoid network on one sample
(forward, backward, one update), softmax + cross-entropy on three logits, gradient norms through
10 random layers (fixed seed) and a finite-difference check. Run: python3 backpropagation.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, finish)
from tablefig import GR, AM
import linear_algebra as _la
_la.RGBA.update({AM: '--amber-a', GR: '--green-a'})   # amber/green tints for chips (no change to the module file)

PAGE = os.path.join(HERE, '../../../content/08-deep-learning/02-neural-network/backpropagation/index.html')
FW, BW = FI, AM          # forward values blue, gradients amber (the "pointer / answer" colour)
ON = 'var(--on-fill)'

def sig(z): return 1 / (1 + math.exp(-z))
def f2(v): return ('%.2f' % v).replace('-', '−')
def f3(v): return ('%.3f' % v).replace('-', '−')
def f4(v): return ('%.4f' % v).replace('-', '−')

# ---------- 01 graph: f = (x + y) · z ----------
GX, GY, GZ = -2, 5, -4
GQ = GX + GY; GF = GQ * GZ
G_DZ, G_DQ = GQ, GZ; G_DX = G_DQ * 1; G_DY = G_DQ * 1
assert (GQ, GF, G_DZ, G_DQ, G_DX, G_DY) == (3, -12, 3, -4, -4, -4)
# ---------- 2.1 chain: u = 2x + 1, y = u², x = 3 ----------
CU = 2 * 3 + 1; CYv = CU ** 2; C_DU = 2 * CU; C_DX = C_DU * 2
assert (CU, CYv, C_DU, C_DX) == (7, 49, 14, 28)
# ---------- 2.2 fan-out: u = x·y, f = u + x, x = 3, y = 2 ----------
BU = 3 * 2; BF = BU + 3; B_D1 = 1 * 2; B_D2 = 1; B_DX = B_D1 + B_D2
assert (BU, BF, B_DX) == (6, 9, 3)
h = 1e-6; assert abs(((3 + h) * 2 + 3 + h - (3 * 2 + 3)) / h - 3) < 1e-6

# ---------- 03 the 2-2-1 network ----------
X = [1.0, 0.5]; Y = 1; LR = 0.5
W1 = [[0.5, -0.3], [0.8, 0.2]]; B1 = [0.1, -0.1]; W2 = [0.7, -0.4]; B2 = 0.2
def forward(W1, B1, W2, B2):
    z1 = [W1[i][0] * X[0] + W1[i][1] * X[1] + B1[i] for i in range(2)]; a1 = [sig(v) for v in z1]
    z2 = W2[0] * a1[0] + W2[1] * a1[1] + B2; a2 = sig(z2)
    return z1, a1, z2, a2, -(Y * math.log(a2) + (1 - Y) * math.log(1 - a2))
Z1, A1, Z2, A2, LOSS = forward(W1, B1, W2, B2)
D2 = A2 - Y
GW2 = [D2 * a for a in A1]
D1 = [W2[i] * D2 * A1[i] * (1 - A1[i]) for i in range(2)]
GW1 = [[D1[i] * x for x in X] for i in range(2)]
NW1 = [[W1[i][j] - LR * GW1[i][j] for j in range(2)] for i in range(2)]
NB1 = [B1[i] - LR * D1[i] for i in range(2)]
NW2 = [W2[i] - LR * GW2[i] for i in range(2)]; NB2 = B2 - LR * D2
LOSS2 = forward(NW1, NB1, NW2, NB2)[-1]
assert [round(v, 2) for v in Z1] == [.45, .8] and [round(v, 3) for v in A1] == [.611, .69]
assert round(Z2, 3) == .351 and round(A2, 3) == .587 and round(LOSS, 3) == .533
assert round(D2, 3) == -.413 and [round(v, 3) for v in GW2] == [-.252, -.285]
assert [round(v, 4) for v in D1] == [-.0687, .0353]
assert round(NW2[0], 3) == .826 and round(NW1[0][0], 3) == .534 and round(LOSS2, 3) == .387

# ---------- 04 softmax + cross-entropy ----------
LOG = [2.0, 1.0, 0.1]; EX = [math.exp(v) for v in LOG]; P = [e / sum(EX) for e in EX]; OH = [1, 0, 0]
GP = [p - y for p, y in zip(P, OH)]; CE = -math.log(P[0])
assert [round(v, 2) for v in EX] == [7.39, 2.72, 1.11] and [round(v, 3) for v in P] == [.659, .242, .099]
assert round(CE, 3) == .417 and round(GP[0], 3) == -.341 and abs(sum(GP)) < 1e-12
# numeric check of dCE/dz0
hh = 1e-6; zz = [LOG[0] + hh] + LOG[1:]
assert abs((-math.log(math.exp(zz[0]) / sum(math.exp(v) for v in zz)) - CE) / hh - GP[0]) < 1e-5

# ---------- 05 gradient size per layer through 10 layers ----------
def grad_norms(act, dact, var, n=32, depth=10, seed=7):
    g = random.Random(seed); hv = [g.gauss(0, 1) for _ in range(n)]; Ws, Zs = [], []
    for _ in range(depth):
        W = [[g.gauss(0, math.sqrt(var / n)) for _ in range(n)] for _ in range(n)]
        z = [sum(W[i][j] * hv[j] for j in range(n)) for i in range(n)]; hv = [act(v) for v in z]
        Ws.append(W); Zs.append(z)
    gr = [g.gauss(0, 1) for _ in range(n)]; out = []
    for l in range(depth - 1, -1, -1):
        d = [gr[i] * dact(Zs[l][i]) for i in range(n)]
        gr = [sum(Ws[l][i][j] * d[i] for i in range(n)) for j in range(n)]
        out.append(math.sqrt(sum(v * v for v in gr) / n))
    return out[::-1]          # index 0 = layer 1 (closest to the input)
relu = lambda z: max(z, 0.0); drelu = lambda z: 1.0 if z > 0 else 0.0
GN_SIG = grad_norms(sig, lambda z: sig(z) * (1 - sig(z)), 1)
GN_HE = grad_norms(relu, drelu, 2)
GN_BIG = grad_norms(relu, drelu, 6)
assert GN_SIG[0] < 1e-6 and 0.2 < GN_SIG[-1] < 0.3
assert all(0.8 < v < 1.5 for v in GN_HE) and GN_BIG[0] > 200 and GN_BIG[-1] < 2

# ---------- 06 gradient check on w11 ----------
def loss_w(w): return forward([[w, W1[0][1]], W1[1]], B1, W2, B2)[-1]
ANA = GW1[0][0]
NUM = {hh: (loss_w(.5 + hh) - loss_w(.5 - hh)) / (2 * hh) for hh in (.3, 1e-2, 1e-4)}
REL = {hh: abs(v - ANA) / max(abs(v), abs(ANA)) for hh, v in NUM.items()}
assert round(ANA, 5) == -.06874 and round(NUM[.3], 4) == -.0684 and REL[1e-4] < 1e-6 and REL[.3] > 1e-3

# ---------- drawing helpers ----------
def node(cx, cy, s, c=RULE_HI, r=22, fill=None, tc=TX, bold=False):
    return ('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' %
            (cx, cy, r, fill or BG, c, 1.6 if c != RULE_HI else 1.2) + T(cx, cy + 5, s, tc, mono=True, bold=bold))
def op(cx, cy, s):
    return ('<circle cx="%.1f" cy="%.1f" r="18" fill="%s" stroke="%s" stroke-width="1.3"/>' % (cx, cy, SUNK, RULE_HI) +
            T(cx, cy + 6, s, TX, bold=True))
def packet(f, x1, y1, x2, y2, s, c, t, d=.8, w=None, hide=None):
    """a value chip that rides from (x1,y1) to (x2,y2) and stays there (or fades at hide)"""
    f.path(chip(x1, y1, s, c, w), [(0, 0, 0), (t + .1, x2 - x1, y2 - y1)], t, d=d, hide=hide)
def edge(p, q, r=22, c=RULE_HI, sw=1.3, head=True):
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    x1, y1 = p[0] + r * math.cos(a), p[1] + r * math.sin(a); x2, y2 = q[0] - r * math.cos(a), q[1] - r * math.sin(a)
    return arrow(x1, y1, x2, y2, c, sw, None, 7) if head else L(x1, y1, x2, y2, c, sw)
def at(p, q, k): return (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)
def box(cx, cy, w, hgt, s, c=RULE_HI, tc=TX):
    return R(cx - w / 2, cy - hgt / 2, w, hgt, BG, c, 6, 1.4) + T(cx, cy + 4, s, tc, bold=True)

# ---------- 01 Mental model: a computational graph ----------
def fig_graph():
    f = Anim('bp1-', 720, 0, 'A computational graph of f = (x + y) times z with x = -2, y = 5, z = -4. Forward, blue values ride '
             'left to right: x and y enter the plus node, q = 3; q and z enter the times node, f = -12. Backward, amber '
             'gradients ride right to left: df/df = 1 starts at f; the times node sends z = -4 to q and q = 3 to z; the plus '
             'node passes -4 unchanged to both x and y. Each gradient is the incoming gradient times the local derivative.',
             'FORWARD: VALUES → · BACKWARD: GRADIENTS ← · EACH NODE MULTIPLIES BY ITS LOCAL DERIVATIVE')
    px, py, pz = (60, 80), (60, 200), (60, 300); pp, pq, pm, pf = (290, 140), (405, 180), (520, 220), (660, 220)
    for p, n in ((px, 'x'), (py, 'y'), (pz, 'z')): f.static(M(p[0] - 34, p[1] + 5, '{%s}' % n, MU, 'end'))
    f.static(edge(px, pp, 18) + edge(py, pp, 18) + edge(pp, pm, 18) + edge(pz, pm, 18) + edge(pm, pf, 18))
    f.static(op(pp[0], pp[1], '+') + op(pm[0], pm[1], '×') + M(pf[0] + 30, pf[1] + 5, '{f}', MU, 'start'))
    f.static(M(pq[0], pq[1] - 26, '{q}', MU))
    # forward
    for p, v in ((px, GX), (py, GY), (pz, GZ)): f.show(chip(p[0], p[1], str(v).replace('-', '−'), FW, 40), .3)
    packet(f, px[0], px[1], *at(px, pp, .62), str(GX).replace('-', '−'), FW, 1.0, w=40)
    packet(f, py[0], py[1], *at(py, pp, .62), str(GY), FW, 1.0, w=40)
    f.show(chip(pq[0], pq[1], '3', FW, 40), 2.0)
    packet(f, pz[0], pz[1], *at(pz, pm, .35), '−4', FW, 2.6, w=40)
    f.show(chip(pf[0], pf[1], '−12', FW, 48), 3.6)
    # local derivatives under the ops
    f.show(M(pm[0], pm[1] + 42, '∂{f}/∂{q} = {z}', MU) + M(pm[0], pm[1] + 60, '∂{f}/∂{z} = {q}', MU), 4.4)
    f.show(M(pp[0], pp[1] + 42, '∂{q}/∂{x} = ∂{q}/∂{y} = 1', MU), 4.4)
    # backward: gradients ride below the edges
    off = 24
    f.show(chip(pf[0], pf[1] + 34, '1', BW, 36), 5.2)
    packet(f, pf[0], pf[1] + 34, pm[0] + 46, pm[1] + 34, '1', BW, 5.8, w=36, hide=6.8)
    packet(f, pm[0] + 46, pm[1] + 34, pq[0], pq[1] + 34, '1 · −4 = −4', BW, 6.8, w=94)
    packet(f, pm[0] + 46, pm[1] + 34, pz[0] + 30, pz[1] + 34, '∂f/∂z = 1 · 3 = 3', BW, 7.6, w=140)
    f.show(T(pq[0], pq[1] + 58, '∂f/∂q', BW, cls='sv-d'), 7.6)
    packet(f, pq[0], pq[1] + 34, px[0] + 30, px[1] + 34, '∂f/∂x = −4 · 1', BW, 8.6, w=124)
    packet(f, pq[0], pq[1] + 34, py[0] + 30, py[1] + 34, '∂f/∂y = −4 · 1', BW, 9.4, w=124)
    return finish(f, 360)

# ---------- 2.1 along a path ----------
def fig_chain():
    f = Anim('bp2-', 720, 0, 'A chain x to u = 2x + 1 to y = u squared, at x = 3. Forward the values 3, 7, 49 ride right. Each '
             'link has a local derivative: du/dx = 2, dy/du = 2u = 14. Backward, the gradient starts at 1, is multiplied by '
             '14 at the first link and by 2 at the next, and arrives at x as 28.', 'ALONG ONE PATH · MULTIPLY THE LOCAL DERIVATIVES')
    ps = [(70, 110), (330, 110), (590, 110)]
    for (p, q), lab in zip(zip(ps, ps[1:]), ('×2 + 1', '( )²')):
        f.static(edge(p, q, 26) + T((p[0] + q[0]) / 2, p[1] - 12, lab, MU, mono=True))
    for p, n in zip(ps, 'xuy'): f.static(M(p[0], p[1] - 40, '{%s}' % n, MU))
    for k, (p, v) in enumerate(zip(ps, (3, CU, CYv))):
        f.show(node(p[0], p[1], str(v), FW, 24, tn(FI, '.12'), FW, True), .3 + k * 1.0)
    f.show(M(200, 168, 'd{u}/d{x} = 2', MU) + M(460, 168, 'd{y}/d{u} = 2{u} = 14', MU), 3.4)
    f.show(chip(590, 220, '1', BW, 40), 4.2)
    packet(f, 590, 220, 330, 220, '1 · 14', BW, 5.0, w=64)
    f.show(chip(330, 254, '= 14', BW, 56), 6.0)
    packet(f, 330, 254, 70, 254, '14 · 2', BW, 6.8, w=64)
    f.show(chip(70, 288, '= 28', BW, 56), 7.8)
    f.show(M(380, 296, 'd{y}/d{x} = d{y}/d{u} · d{u}/d{x} = 28', BW, 'start'), 8.4)
    return finish(f, 316)

# ---------- 2.2 where paths merge ----------
def fig_fanout():
    f = Anim('bp3-', 720, 0, 'x = 3 is used twice: u = x times y with y = 2, and f = u + x. Backward, the gradient 1 at f splits '
             'into two paths. Through u it becomes 1 times y = 2; the direct path carries 1. Both arrive at x and add: 2 + 1 = 3.',
             'ONE INPUT, TWO PATHS · THE GRADIENTS ADD')
    px, py, pm, pp, pf = (70, 200), (70, 90), (300, 90), (480, 200), (640, 200)
    f.static(edge(px, pm, 22) + edge(py, pm, 22) + edge(pm, pp, 18) + edge(px, pp, 22) + edge(pp, pf, 18))
    f.static(op(pm[0], pm[1], '×') + op(pp[0], pp[1], '+') + M(px[0] - 34, px[1] + 5, '{x}', MU, 'end') +
             M(py[0] - 34, py[1] + 5, '{y}', MU, 'end') + M(pf[0] + 32, pf[1] + 5, '{f}', MU, 'start'))
    f.show(node(px[0], px[1], '3', FW, 22, tn(FI, '.12'), FW, True) + node(py[0], py[1], '2', FW, 22, tn(FI, '.12'), FW, True), .3)
    f.show(chip(pm[0] + 60, pm[1] - 30, '6', FW, 36), 1.1)
    f.show(chip(pf[0], pf[1], '9', FW, 36), 1.9)
    f.show(chip(pf[0], pf[1] + 34, '1', BW, 36), 2.8)
    packet(f, pf[0], pf[1] + 34, 390, 112, '1 · 2 = 2', BW, 3.6, w=80)
    packet(f, pf[0], pf[1] + 34, 270, 234, '1', BW, 3.6, w=36)
    packet(f, 390, 112, 150, 160, '2', BW, 5.0, w=36, d=.8)
    packet(f, 270, 234, 150, 234, '1', BW, 5.0, w=36)
    f.show(chip(150, 270, '2 + 1 = 3', BW, 84), 6.2)
    f.show(M(210, 300, '∂{f}/∂{x} = sum over every path from {f} to {x}', BW, 'start'), 6.8)
    return finish(f, 316)

# ---------- 03 the network ----------
NX = [(70, 80), (70, 240)]; NH = [(330, 80), (330, 240)]; NO = (560, 160); NL = (668, 160)
def net_base(f, ws=(W1, W2), labels=True, wcol=MU):
    for i, p in enumerate(NX): f.static(M(p[0] - 30, p[1] + 5, '{x}' + '₁₂'[i], MU, 'end'))
    for i, p in enumerate(NH): f.static(M(p[0] + 26, p[1] + (-18 if i == 0 else 30), '{h}' + '₁₂'[i], MU, 'start'))
    f.static(M(NO[0], NO[1] - 32, 'ŷ', MU))
    edges = []
    for i in range(2):
        for j in range(2): edges.append((NX[j], NH[i], ws[0][i][j], 'w%d%d' % (i + 1, j + 1)))
    for i in range(2): edges.append((NH[i], NO, ws[1][i], 'v%d' % (i + 1)))
    return edges
def wlab(p, q, s, c=MU):
    x, y = at(p, q, .2 if p[0] < 200 else .25)
    return R(x - 20, y - 9, 40, 17, BG, 'none', 3) + T(x, y + 4, s, c, mono=True)
def glab(p, q): return at(p, q, .68 if p[0] < 200 else .62)
def ew(w): return 1 + 3.2 * abs(w)

def fig_forward():
    f = Anim('bp4-', 720, 0, 'Forward pass of a 2-2-1 sigmoid network on one sample x = (1, 0.5), label y = 1. The inputs ride '
             'along the four first-layer edges; hidden neuron 1 gets z = 0.45, a = 0.611; neuron 2 gets z = 0.80, a = 0.690. '
             'Those ride to the output: z = 0.351, prediction 0.587. The prediction enters the loss box: '
             'L = -log 0.587 = 0.533.', 'FORWARD · NUMBERS RIDE THE EDGES LEFT TO RIGHT · ONE LOSS AT THE END')
    E = net_base(f)
    for p, q, w, n in E: f.static(edge(p, q, 22, RULE_HI, ew(w)) + wlab(p, q, f2(w)))
    f.static(edge(NO, (NL[0] - 18, NL[1]), 22, RULE_HI, 1.2) + T(NL[0] + 10, NL[1] - 30, 'loss', MU, cls='sv-d'))
    for i, p in enumerate(NX): f.show(node(p[0], p[1], ('%g' % X[i]), FW, 22, tn(FI, '.12'), FW, True), .3)
    for k, i in enumerate(range(2)):
        t = 1.0 + k * 1.8
        for j in range(2):
            p = NX[j]; q = NH[i]; e = at(p, q, .8)
            f.path(dot(p[0], p[1], FW, 5), [(0, 0, 0), (t + .1, e[0] - p[0], e[1] - p[1])], t, d=.7, hide=t + 1.0)
        f.show(node(NH[i][0], NH[i][1], f2(A1[i]), FW, 22, tn(FI, '.12'), FW, True), t + .9)
        f.show(T(NH[i][0], NH[i][1] + 40, 'z = %s' % f2(Z1[i]), FW, cls='sv-d'), t + .9)
    t = 4.8
    for i in range(2):
        p = NH[i]; e = at(p, NO, .8)
        f.path(dot(p[0], p[1], FW, 5), [(0, 0, 0), (t + .1, e[0] - p[0], e[1] - p[1])], t, d=.7, hide=t + 1.0)
    f.show(node(NO[0], NO[1], f3(A2), FW, 24, tn(FI, '.12'), FW, True) + T(NO[0], NO[1] + 42, 'z = %s' % f3(Z2), FW, cls='sv-d'), t + .9)
    packet(f, NO[0], NO[1], NL[0] + 10, NL[1], f3(A2), FW, 6.6, w=50)
    f.show(R(NL[0] - 18, NL[1] - 18, 56, 36, BG, RO, 6, 1.6) + T(NL[0] + 10, NL[1] + 5, f3(LOSS), RO, mono=True, bold=True), 7.6)
    f.show(M(NL[0] + 38, NL[1] + 46, '{L} = −log ŷ', RO, 'end') + T(NL[0] + 38, NL[1] + 64, 'y = 1', MU, 'end', cls='sv-d'), 7.9)
    f.static(T(0, 300, 'biases  b₁ = (0.1, −0.1)  ·  b₂ = 0.2', FA, 'start', cls='sv-d'))
    return finish(f, 312)

def fig_backward():
    f = Anim('bp5-', 720, 0, 'Backward pass on the same network. The error at the output is a - y = -0.413. It rides back along '
             'each output edge; multiplied by the hidden activation it becomes the gradient of that weight: -0.252 and -0.285. '
             'Multiplied by the weight and the sigmoid slope it becomes the hidden errors -0.0687 and 0.0353, which ride back '
             'to the inputs and give the four first-layer gradients.', 'BACKWARD · ONE ERROR AT THE OUTPUT · EVERY EDGE GETS ITS ∂L/∂w')
    E = net_base(f)
    for p, q, w, n in E: f.static(edge(p, q, 22, RULE_HI, ew(w)) + wlab(p, q, f2(w), FA))
    for i, p in enumerate(NX): f.static(node(p[0], p[1], '%g' % X[i], RULE_HI, 22, None, MU))
    for i, p in enumerate(NH): f.static(node(p[0], p[1], f2(A1[i]), RULE_HI, 22, None, MU))
    f.static(node(NO[0], NO[1], f3(A2), RULE_HI, 24, None, MU))
    f.static(edge(NO, (NL[0] - 18, NL[1]), 22, RULE_HI, 1.2) + R(NL[0] - 18, NL[1] - 18, 56, 36, BG, RO, 6, 1.4) +
             T(NL[0] + 10, NL[1] + 5, f3(LOSS), RO, mono=True))
    f.show(chip(NO[0], NO[1] + 46, 'δ = %s' % f3(D2), BW, 84), .5)
    f.show(T(NO[0], NO[1] + 72, 'ŷ − y', BW, cls='sv-d'), .8)
    t = 1.6
    for i in range(2):
        g = glab(NH[i], NO)
        packet(f, NO[0], NO[1], g[0], g[1], f3(GW2[i]), BW, t, w=54)
    f.show(T(450, 300, '∂L/∂v = δ · h', BW, cls='sv-d'), t + 1.0)
    t = 3.4
    for i in range(2):
        f.show(chip(NH[i][0], NH[i][1] + (-44 if i == 0 else 44), 'δ = ' + f4(D1[i]), BW, 92) if False else chip(NH[i][0] - 10, NH[i][1] + (-48 if i == 0 else 48), 'δ = ' + f4(D1[i]), BW, 92), t + i * .3)
        # (chips sit between the two hidden nodes, clear of the edge labels at 0.68)
    f.show(T(330, 160, 'δ = v · δ_out · σ′(z)', BW, cls='sv-d'), t + .6)
    t = 5.0
    for i in range(2):
        for j in range(2):
            g = glab(NX[j], NH[i])
            packet(f, NH[i][0], NH[i][1], g[0], g[1], f3(GW1[i][j]), BW, t + i * .9, w=54)
    f.show(T(140, 300, '∂L/∂w = δ · x', BW, cls='sv-d'), t + 2.0)
    return finish(f, 312)

def fig_update():
    f = Anim('bp6-', 720, 0, 'One gradient step with learning rate 0.5. Each weight label changes to w - 0.5 times its gradient: '
             'v1 0.70 to 0.83, v2 -0.40 to -0.26, w11 0.50 to 0.53 and so on; edges thicken or thin with the new size. A '
             'second forward pass gives loss 0.387 instead of 0.533.', 'UPDATE · w ← w − η · ∂L/∂w · η = 0.5')
    E = net_base(f); EN = net_base(Anim('x', 1, 1, ''), (NW1, NW2))
    for i, p in enumerate(NX): f.static(node(p[0], p[1], '%g' % X[i], RULE_HI, 22, None, MU))
    for i, p in enumerate(NH): f.static(node(p[0], p[1], 'h' + '₁₂'[i], RULE_HI, 22, None, MU))
    f.static(node(NO[0], NO[1], 'ŷ', RULE_HI, 24, None, MU) + edge(NO, (NL[0] - 18, NL[1]), 22, RULE_HI, 1.2))
    order = [4, 5, 0, 1, 2, 3]
    for k, ix in enumerate(order):
        p, q, w, n = E[ix]; nw = EN[ix][2]; t = .6 + k * .7
        old = edge(p, q, 22, RULE_HI, ew(w)); new = edge(p, q, 22, GR if abs(nw) > abs(w) else VI, ew(nw))
        f.show(old, 0, hide=t); f.show(new, t)
        f.show(wlab(p, q, f2(w)), 0, hide=t)
        f.show(wlab(p, q, f2(nw), GR if abs(nw) > abs(w) else VI), t)
    for p, q, w, n in E: pass
    f.static(R(NL[0] - 18, NL[1] - 18, 56, 36, BG, RO, 6, 1.4))
    f.show(T(NL[0] + 10, NL[1] + 5, f3(LOSS), RO, mono=True, bold=True), 0, hide=5.4)
    f.show(T(NL[0] + 10, NL[1] + 5, f3(LOSS2), GR, mono=True, bold=True), 5.6)
    f.show(T(NL[0] + 10, NL[1] + 40, 'was ' + f3(LOSS), MU, cls='sv-d'), 5.8)
    f.static(T(0, 300, 'thicker = bigger |w| after the step', GR, 'start', cls='sv-d') +
             T(250, 300, 'thinner = smaller |w|', VI, 'start', cls='sv-d'))
    assert sum(abs(a) > abs(b) for a, b in zip([NW1[0][0], NW1[0][1], NW1[1][0], NW1[1][1]] + NW2,
                                                [W1[0][0], W1[0][1], W1[1][0], W1[1][1]] + W2)) >= 1
    return finish(f, 312)

# ---------- 04 softmax + cross-entropy ----------
def fig_softmax():
    f = Anim('bp7-', 720, 0, 'Three classes cat, dog, bird with logits 2.0, 1.0, 0.1. Each logit moves right and becomes its '
             'exponential: 7.39, 2.72, 1.11; divided by their sum 11.21 these become probabilities 0.659, 0.242, 0.099. The '
             'true class is cat, one-hot 1, 0, 0. Subtracting gives the gradient -0.341, 0.242, 0.099: push cat up, the others down.',
             'LOGITS → PROBABILITIES → GRADIENT  p − y')
    cols = [('class', 60), ('logit z', 90), ('e^z', 90), ('p', 90), ('y', 70), ('∂L/∂z = p − y', 130)]
    tb = Table(40, 30, cols); f.static(tb.head())
    names = ('cat', 'dog', 'bird')
    for i, n in enumerate(names): f.static(tb.row(i, [n], j0=0) if False else '')
    for i in range(3):
        f.static(R(tb.x, tb.ry(i), tb.w, tb.rh, BG, RULE, 3, 1) + T(tb.cx(0), tb.ry(i) + 17, names[i], TX))
    stages = [(1, ['%.1f' % v for v in LOG], TX, .3), (2, ['%.2f' % v for v in EX], TX, 1.6), (3, [f3(v) for v in P], FW, 3.0)]
    for j, vals, c, t in stages:
        for i in range(3):
            if j > 1:
                src = tb.cx(j - 1); dst = tb.cx(j)
                f.path(T(src, tb.ry(i) + 17, stages[j - 2][1][i], MU, mono=True),
                       [(0, 0, 0), (t + .1, dst - src, 0)], t, d=.6, hide=t + .7)
            f.show(T(tb.cx(j), tb.ry(i) + 17, vals[i], c, mono=True, bold=(j == 3)), t + .7 if j > 1 else t)
    f.show(T(tb.cx(2), tb.ry(3) + 14, 'sum %.2f' % sum(EX), MU, cls='sv-d'), 2.4)
    for i in range(3): f.show(T(tb.cx(4), tb.ry(i) + 17, str(OH[i]), GR, mono=True, bold=OH[i] == 1), 4.4)
    for i in range(3):
        f.path(T(tb.cx(3), tb.ry(i) + 8, f3(P[i]), MU, mono=True), [(0, 0, 0), (5.4, tb.cx(5) - tb.cx(3) - 30, 0)], 5.3, d=.7, hide=6.2)
        f.show(tb.cell(i, 5, f3(GP[i]), 'am'), 6.2)
    f.show(tb.outline(0, 0, 4, 4, GR, 1.6), 4.6)
    # bars for p
    bx, by = 120, 210
    f.static(T(40, by + 4, 'p', MU, 'start', cls='sv-s') + L(bx, by - 14, bx, by + 74, RULE_HI, 1))
    for i in range(3):
        f.show(R(bx, by - 8 + i * 28, 320 * P[i], 16, tn(FI, '.25'), FI, 2, 1) +
               T(bx - 8, by + 4 + i * 28, names[i], MU, 'end', cls='sv-d'), 3.6 + i * .15)
        g = GP[i]; x0 = 560
        f.show(R(x0 + min(0, g) * 240, by - 8 + i * 28, abs(g) * 240, 16, tn(AM, '.2'), AM, 2, 1.2), 6.6 + i * .15)
    f.static(L(560, by - 14, 560, by + 74, RULE_HI, 1) + T(560, by + 92, '0', FA, mono=True) +
             T(470, by + 92, '← raise this logit', AM, cls='sv-d') + T(650, by + 92, 'lower →', AM, cls='sv-d'))
    f.show(M(40, by + 116, '{L} = −log {p}_cat = −log 0.659 = 0.417', RO, 'start'), 7.4)
    return finish(f, by + 128)

# ---------- 05 gradient size per layer ----------
def fig_layers(pre, data, c, title, aria, word):
    f = Anim(pre, 720, 0, aria, title)
    x0, yb, H = 70, 256, 180; lo, hi = -7, 3
    Yv = lambda v: yb - (math.log10(v) - lo) / (hi - lo) * H
    f.static(L(x0, yb, x0 + 600, yb, RULE_HI, 1.3) + L(x0, yb, x0, yb - H - 6, RULE_HI, 1.3))
    for e in range(lo, hi + 1, 2):
        f.static(L(x0, Yv(10 ** e), x0 + 600, Yv(10 ** e), RULE if e else MU, 1 if e else 1.2, None if e else '4 3') +
                 T(x0 - 8, Yv(10 ** e) + 4, '1' if e == 0 else '10%s' % ('⁻' + '⁰¹²³⁴⁵⁶⁷'[-e] if e < 0 else '⁰¹²³⁴⁵⁶⁷'[e]), FA, 'end', mono=True))
    f.static(S(x0, yb - H - 16, 'gradient size  (log scale)', MU) + S(x0 + 600, yb + 34, 'layer  (1 = next to the input)', MU, 'end'))
    bw = 38
    for k in range(10):
        f.static(T(x0 + 30 + k * 58 + bw / 2, yb + 16, str(k + 1), FA, mono=True))
    # backward goes from layer 10 down to layer 1
    for n, k in enumerate(range(9, -1, -1)):
        v = data[k]; x = x0 + 30 + k * 58; top = Yv(v); t = .4 + n * .45
        f.show(R(x, min(top, yb), bw, abs(yb - top), tn(c, '.22'), c, 2, 1.2), t)
        lab = ('%.0e' % v).replace('e-0', 'e−').replace('e+0', 'e') if (v < .01 or v >= 100) else ('%.2f' % v if v < 10 else '%.0f' % v)
        f.show(T(x + bw / 2, top - 6, lab, c, mono=True), t + .1)
    f.path(arrow(x0 + 600, 36, x0 + 540, 36, BW, 1.6) + T(x0 + 610, 40, 'backward', BW, 'start', cls='sv-d'), [(0, 0, 0), (.5, -330, 0)], .2, d=4.4)
    f.show(T(x0 + 600, yb - H - 16, word, c, 'end', cls='sv-s', bold=True), 5.2)
    return finish(f, yb + 46)

# ---------- 06 gradient check ----------
def fig_check():
    f = Anim('bp11-', 720, 0, 'The loss of the 2-2-1 network as only w11 changes, built point by point from w = 0.2 to 0.8. Two '
             'points at w = 0.5 plus and minus h = 0.3 are joined by a secant; its slope, -0.0684, is the numeric gradient. The '
             'analytic gradient from backprop, -0.0687, is the tangent. With h = 0.0001 they agree to 7 digits.',
             'NUMERIC SLOPE  vs  BACKPROP GRADIENT · ONE WEIGHT')
    x0, x1, yb, yt = 60, 420, 260, 50; w0, w1 = .1, .9
    ws = [w0 + i * .05 for i in range(17)]; ls = [loss_w(w) for w in ws]
    l0, l1 = .47, .60
    PX = lambda w: x0 + (w - w0) / (w1 - w0) * (x1 - x0); PY = lambda v: yb - (v - l0) / (l1 - l0) * (yb - yt)
    assert l0 < min(ls) and max(ls) < l1
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for w in (.2, .5, .8): f.static(T(PX(w), yb + 15, '%g' % w, FA, mono=True))
    for v in (.5, .55, .6): f.static(T(x0 - 7, PY(v) + 4, '%g' % v, FA, 'end', mono=True))
    f.static(M(x1, yb + 34, '{w}₁₁', MU, 'end') + M(x0, yt - 12, '{L}', MU))
    for i, (w, v) in enumerate(zip(ws, ls)):
        t = .3 + i * .12
        f.show(dot(PX(w), PY(v), FW, 3) + (L(PX(ws[i - 1]), PY(ls[i - 1]), PX(w), PY(v), FW, 1.6) if i else ''), t)
    hh = .3; a, b = .5 - hh, .5 + hh
    for w in (a, b):
        f.show(L(PX(w), yb, PX(w), PY(loss_w(w)), MU, 1, '3 3') + dot(PX(w), PY(loss_w(w)), VI, 5, BG), 2.8)
    f.show(T(PX(a), yb - 6, 'w − h', VI, 'start', cls='sv-d') + T(PX(b), yb - 6, 'w + h', VI, 'end', cls='sv-d'), 2.9)
    f.show(L(PX(a), PY(loss_w(a)), PX(b), PY(loss_w(b)), VI, 2, '6 4'), 3.6)
    s = ANA; ext = .3
    f.show(L(PX(.5 - ext), PY(loss_w(.5) - s * ext), PX(.5 + ext), PY(loss_w(.5) + s * ext), BW, 2) + dot(PX(.5), PY(loss_w(.5)), BW, 5, BG), 4.6)
    X2 = 460
    f.show(S(X2, 60, 'numeric (secant)', VI, bold=True) + M(X2, 82, '({L}(w+h) − {L}(w−h)) / 2h', MU, 'start'), 3.8)
    f.show(S(X2, 112, 'analytic (backprop)', BW, bold=True) + M(X2, 134, 'δ₁ · {x}₁ = ' + fx(ANA, 5), MU, 'start'), 4.8)
    tb = Table(X2, 152, [('h', 70), ('numeric', 90), ('rel. error', 90)]); f.show(tb.head(), 5.4)
    for i, hv in enumerate((.3, 1e-2, 1e-4)):
        f.show(tb.row(i, ['%g' % hv, fx(NUM[hv], 5 if i < 2 else 7), '%.0e' % REL[hv]], tone='gr' if REL[hv] < 1e-6 else None), 5.8 + i * .5)
    return finish(f, 290)
def fx(v, n): return ('%.*f' % (n, v)).replace('-', '−')

BODY = r'''<header class="hero">
  <p class="eyebrow">Deep learning · Neural network</p>
  <h1><em>Backpropagation</em></h1>
  <p class="lede">Backpropagation runs the network forward once, then sends one error backwards, multiplying by each step's local derivative, so <b>every weight gets its gradient in a single sweep</b>.</p>
</header>

<section id="backprop-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Values flow <em>forward</em> through a graph of small operations; gradients flow <em>backward</em>, each node multiplying by its own local derivative.</p>
{bp1}
  <ul class="why">
    <li>Each node only knows its <b>local derivative</b> (a × node sends back the other input, a + node passes the gradient through).</li>
    <li>The forward pass must <b>store</b> its values: the backward pass needs <span class="mth"><var>q</var></span> and <span class="mth"><var>z</var></span> again.</li>
    <li>One backward sweep costs about as much as one forward pass, whatever the number of weights — that is why it beats perturbing weights one by one.</li>
  </ul>
</section>

<section id="backprop-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Chain rule</h2></div>
  <p class="key">The gradient from the loss to any value is <em>a product along each path</em>, summed over paths.</p>
  <div class="subsec" id="backprop-s2-1">
    <h3 class="ssh"><b>2.1</b>Along a path</h3>
    <p class="skey">Composed functions: <em>multiply</em> the local derivatives link by link.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><span class="frac"><i>d<var>y</var></i><i>d<var>x</var></i></span></span><em>what we want</em></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i>d<var>y</var></i><i>d<var>u</var></i></span></span><em>outer link</em></span>
      <span class="op">·</span>
      <span class="t p"><span><span class="frac"><i>d<var>u</var></i><i>d<var>x</var></i></span></span><em>inner link</em></span>
    </div>
  </div>
{bp2}
  </div>
  <div class="subsec" id="backprop-s2-2">
    <h3 class="ssh"><b>2.2</b>Where paths merge</h3>
    <p class="skey">A value used twice gets gradients from both uses: <em>add</em> them.</p>
{bp3}
    <ul class="why">
      <li>This is why frameworks <b>accumulate</b> into <code>.grad</code> — and why you call <code>optimizer.zero_grad()</code> before each step.</li>
    </ul>
  </div>
</section>

<section id="backprop-s3" class="lesson">
  <div class="sh"><b>03</b><h2>A 2-2-1 network by hand</h2></div>
  <p class="key">Two inputs, two sigmoid hidden neurons, one sigmoid output, log loss, one sample with <span class="mth"><var>y</var> = 1</span>.</p>
  <div class="subsec" id="backprop-s3-1">
    <h3 class="ssh"><b>3.1</b>Forward pass</h3>
    <p class="skey">Each neuron sums its weighted inputs and squashes them; the output enters <em>the loss</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>z</var> = Σ <var>w</var><var>x</var> + <var>b</var></span><em>weighted sum</em></span>
      <span class="op">,</span>
      <span class="t b"><span><var>a</var> = σ(<var>z</var>)</span><em>activation</em></span>
      <span class="op">,</span>
      <span class="t r"><span><var>L</var> = −log <var>ŷ</var></span><em>log loss for y = 1</em></span>
    </div>
  </div>
{bp4}
  </div>
  <div class="subsec" id="backprop-s3-2">
    <h3 class="ssh"><b>3.2</b>Backward pass</h3>
    <p class="skey">An error <span class="mth"><var>δ</var></span> starts at the output and rides back; <em>each weight's gradient is δ times the input on its edge</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>δ</var><sub>out</sub> = <var>ŷ</var> − <var>y</var></span><em>sigmoid + log loss</em></span>
      <span class="op">,</span>
      <span class="t b"><span><var>δ</var><sub><var>h</var></sub> = <var>v</var> · <var>δ</var><sub>out</sub> · σ′(<var>z</var>)</span><em>one layer back</em></span>
      <span class="op">,</span>
      <span class="t p"><span><span class="frac"><i>∂<var>L</var></i><i>∂<var>w</var></i></span> = <var>δ</var> · <var>input</var></span><em>gradient of an edge</em></span>
    </div>
  </div>
{bp5}
    <ul class="why">
      <li><span class="mth">σ′(<var>z</var>) = <var>a</var>(1 − <var>a</var>)</span>, so the stored activations are all the backward pass needs.</li>
      <li>In matrix form one layer is <span class="mth"><var>δ</var><sub><var>l</var></sub> = (<var>W</var><sup>⊤</sup><var>δ</var><sub><var>l</var>+1</sub>) ⊙ σ′(<var>z</var>)</span> and <span class="mth">∂<var>L</var>/∂<var>W</var> = <var>δ</var> <var>a</var><sup>⊤</sup></span>: every gradient has the shape of its weight.</li>
    </ul>
  </div>
  <div class="subsec" id="backprop-s3-3">
    <h3 class="ssh"><b>3.3</b>Update</h3>
    <p class="skey">Step every weight <em>against its gradient</em>; the next forward pass has a lower loss.</p>
{bp6}
    <ul class="why">
      <li>Here one step takes the loss from {loss} to {loss2}. How the step is sized — momentum, Adam — belongs to <a href="../../03-optimizer/optimizer-overview/index.html">Optimizer</a>.</li>
    </ul>
  </div>
</section>

<section id="backprop-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Softmax + cross-entropy</h2></div>
  <p class="key">For many classes the output error is just as simple: <em>probabilities minus the one-hot label</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>p</var><sub><var>k</var></sub> = <span class="frac"><i><var>e</var><sup><var>z</var><sub><var>k</var></sub></sup></i><i>Σ<sub><var>j</var></sub> <var>e</var><sup><var>z</var><sub><var>j</var></sub></sup></i></span></span><em>softmax</em></span>
      <span class="op">,</span>
      <span class="t r"><span><var>L</var> = −log <var>p</var><sub><var>y</var></sub></span><em>cross-entropy</em></span>
      <span class="op">⇒</span>
      <span class="t b"><span><span class="frac"><i>∂<var>L</var></i><i>∂<var>z</var></i></span> = <var>p</var> − <var>y</var></span><em>the gradient on the logits</em></span>
    </div>
  </div>
{bp7}
  <ul class="why">
    <li>The messy derivative of softmax cancels against the log: no division, no exponent in the gradient.</li>
    <li>Use the fused loss (<code>nn.CrossEntropyLoss</code> on raw logits); a separate softmax then log is numerically unstable.</li>
  </ul>
</section>

<section id="backprop-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Vanishing &amp; exploding gradients</h2></div>
  <p class="key">The gradient reaching layer 1 is a product of one factor per layer: <em>slightly below 1 shrinks it, slightly above 1 blows it up</em>.</p>
  <div class="subsec" id="backprop-s5-1">
    <h3 class="ssh"><b>5.1</b>Vanishing — sigmoid</h3>
    <p class="skey">σ′ is at most 0.25, so each layer <em>cuts the gradient by 4× or more</em>.</p>
{bp8}
    <ul class="why">
      <li>The first layers barely move: training looks stuck although the last layers learn.</li>
    </ul>
  </div>
  <div class="subsec" id="backprop-s5-2">
    <h3 class="ssh"><b>5.2</b>Stable — ReLU + He init</h3>
    <p class="skey">ReLU's slope is 1 where active; with weights of variance <span class="mth">2/<var>n</var></span> <em>each layer keeps the size</em>.</p>
{bp9}
    <ul class="why">
      <li>Why <span class="mth">2/<var>n</var></span> works is in <a href="../weight-initialization/index.html">Weight initialization</a>; <a href="../normalization/index.html">Normalization</a> and residual connections keep it stable during training.</li>
    </ul>
  </div>
  <div class="subsec" id="backprop-s5-3">
    <h3 class="ssh"><b>5.3</b>Exploding — weights too large</h3>
    <p class="skey">Same ReLU net with weights of variance <span class="mth">6/<var>n</var></span>: <em>each layer multiplies the gradient by about 1.7</em>.</p>
{bp10}
    <ul class="why">
      <li>Symptom: loss jumps to <code>nan</code>. Quick fix: <b>gradient clipping</b> (<code>clip_grad_norm_</code>), common in RNNs and Transformers.</li>
    </ul>
  </div>
</section>

<section id="backprop-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Gradient checking</h2></div>
  <p class="key">Nudge one weight both ways and measure the slope: <em>it must match backprop's number</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><span class="frac"><i>∂<var>L</var></i><i>∂<var>w</var></i></span></span><em>from backprop</em></span>
      <span class="op">≈</span>
      <span class="t p"><span><span class="frac"><i><var>L</var>(<var>w</var> + <var>h</var>) − <var>L</var>(<var>w</var> − <var>h</var>)</i><i>2<var>h</var></i></span></span><em>central difference</em></span>
    </div>
  </div>
{bp11}
  <ul class="why">
    <li>Relative error below about 1e−6 in float64 means the backward code is right; a big <span class="mth"><var>h</var></span> measures the curve, not the slope.</li>
    <li>Two forward passes per weight: use it on a tiny net to test code, never to train.</li>
    <li>When a model will not learn, check in order: overfit <b>one batch</b> to near-zero loss → loss at step 0 ≈ log(classes) → no <code>nan</code> → gradient size per layer → learning rate.</li>
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

<footer>Deep learning · Neural network · next lesson: <a href="../weight-initialization/index.html">Weight initialization</a>.</footer>
'''

def build():
    sig_aria = ('Gradient size per layer in a 10-layer sigmoid network, measured backward from layer 10 to layer 1. It falls '
                'from %.2f at layer 10 to about %.0e at layer 1.' % (GN_SIG[-1], GN_SIG[0]))
    he_aria = ('Gradient size per layer in a 10-layer ReLU network with He initialisation: every bar stays between %.2f and %.2f.'
               % (min(GN_HE), max(GN_HE)))
    big_aria = ('Gradient size per layer in a 10-layer ReLU network with weights three times too large in variance: it grows '
                'from %.1f at layer 10 to about %.0f at layer 1.' % (GN_BIG[-1], GN_BIG[0]))
    figs = dict(bp1=fig_graph(), bp2=fig_chain(), bp3=fig_fanout(), bp4=fig_forward(), bp5=fig_backward(), bp6=fig_update(),
                bp7=fig_softmax(),
                bp8=fig_layers('bp8-', GN_SIG, RO, 'SIGMOID · 10 LAYERS · GRADIENT SIZE AS IT TRAVELS BACK', sig_aria, 'vanishes toward layer 1'),
                bp9=fig_layers('bp9-', GN_HE, GR, 'RELU + HE INIT · 10 LAYERS · GRADIENT SIZE AS IT TRAVELS BACK', he_aria, 'stays near 1'),
                bp10=fig_layers('bp10-', GN_BIG, AM, 'RELU, VARIANCE 6/n · 10 LAYERS · GRADIENT SIZE AS IT TRAVELS BACK', big_aria, 'explodes toward layer 1'),
                bp11=fig_check(), loss=f3(LOSS), loss2=f3(LOSS2))
    return re.sub(r'\{(bp\d+|loss2?)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">'); b = s.index('</article>')
    s = s[:a] + body + '      ' + s[b:]
    m = re.search(r'<article class="doc"[^>]*>', s); tag = m.group(0)
    tag = re.sub(r' data-(skeleton|reviewed|progress)="[^"]*"', '', tag)
    tag = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s" data-progress="1"' % blurb, tag)
    s = s[:m.start()] + tag + s[m.end():]
    s = s.replace('<script src="lab.js"></script>\n', '')
    open(page, 'w').write(s)

if __name__ == '__main__':
    splice(PAGE, build(), 'A tiny graph and a 2-2-1 network worked by hand: values flow forward, one error flows back through '
           'the chain rule, softmax + cross-entropy gives p − y, gradients vanish or explode across layers, and finite differences check it all.')
