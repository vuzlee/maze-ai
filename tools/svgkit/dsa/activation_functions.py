# -*- coding: utf-8 -*-
"""Figures + body for content/08-deep-learning/02-neural-network/activation-functions.
Every number is computed here: two 2x2 layers that merge into one, each activation and its derivative on the
same three inputs, a value pushed through six sigmoid layers and its gradient pulled back, one ReLU neuron that
never recovers next to a leaky one that does (trained in pure Python), and sigmoid / softmax output heads.
Run: python3 activation_functions.py"""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import decision_tree as dt
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, BR, VI, FI, RULE, SUNK, BG, M, S,
                            Plane, mcell, dot, poly, finish)
from tablefig import GR, AM, RD, Table

PAGE = os.path.join(HERE, '../../../content/08-deep-learning/02-neural-network/activation-functions/index.html')
_RGB = {GR: '--green-a', RD: '--red-a', AM: '--amber-a', FI: '--blue-a', VI: '--violet-a', BR: '--clay-a'}
def tn(c, a='.14'): return 'rgba(var(%s),%s)' % (_RGB[c], a)
def N(v, d=2): return (('%.' + str(d) + 'f') % v).replace('-', '−')
def chip(cx, cy, s, c=FI, w=None):
    w = w or 16 + len(s) * 7.2
    return (R(cx - w / 2, cy - 11, w, 22, BG, 'none', 11) + R(cx - w / 2, cy - 11, w, 22, tn(c), c, 11, 1.3) +
            T(cx, cy + 4.5, s, c, mono=True, bold=True))
def num(x, y, s, c=TX, bold=False, a='middle'): return T(x, y, s, c, a, mono=True, bold=bold)

# ---------- the functions ----------
sig = lambda z: 1 / (1 + math.exp(-z))
SLOPE = 0.1                                   # leaky slope drawn here (PyTorch default is 0.01)
Phi = lambda z: .5 * (1 + math.erf(z / math.sqrt(2)))
pdf = lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
FN = {
    'sigmoid': (sig, lambda z: sig(z) * (1 - sig(z))),
    'tanh': (math.tanh, lambda z: 1 - math.tanh(z) ** 2),
    'relu': (lambda z: max(z, 0), lambda z: 1.0 if z > 0 else 0.0),
    'leaky': (lambda z: z if z > 0 else SLOPE * z, lambda z: 1.0 if z > 0 else SLOPE),
    'gelu': (lambda z: z * Phi(z), lambda z: Phi(z) + z * pdf(z)),
}
ZIN = (-2, .5, 2)
def maxslope(k): return max(FN[k][1](i / 100) for i in range(-600, 601))
assert round(maxslope('sigmoid'), 3) == .25 and round(maxslope('tanh'), 3) == 1 and maxslope('relu') == 1
assert round(maxslope('gelu'), 2) == 1.13
assert round(FN['sigmoid'][1](-2), 3) == .105 and round(FN['gelu'][0](-2), 3) == -.046
ELU = lambda z: z if z > 0 else math.exp(z) - 1
SILU = lambda z: z * sig(z)
assert round(ELU(-2), 3) == -.865 and round(SILU(-2), 3) == -.238

# ---------- 01 two linear layers collapse ----------
def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
W1 = [[1, -1], [2, 1]]; W2 = [[1, 1], [-1, 2]]; XV = [[1], [2]]
H = mm(W1, XV); Y = mm(W2, H); W = mm(W2, W1); YW = mm(W, XV)
HR = [[max(v[0], 0)] for v in H]; YR = mm(W2, HR)
assert H == [[-1], [4]] and Y == [[3], [9]] and W == [[3, 0], [3, 3]] and YW == Y
assert HR == [[0], [4]] and YR == [[4], [8]] and YR != YW

def fig_collapse():
    f = Anim('act1-', 720, 0, 'Top row: x = (1, 2) goes through W1 to h = (−1, 4), then through W2 to y = (3, 9). Middle row: '
             'W1 and W2 slide down and merge into one matrix W = W2 W1 = [[3, 0], [3, 3]]; the same x through W alone gives '
             'the same y = (3, 9), so the two layers were one. Bottom row: a ReLU between them turns h into (0, 4) and '
             'y becomes (4, 8), which no single matrix W reproduces.',
             'NO ACTIVATION · TWO LAYERS = ONE MATRIX · A ReLU BREAKS THE MERGE')
    w, h = 34, 28
    XS = {'x': 70, 'W1': 150, 'h': 270, 'W2': 380, 'y': 500}
    def col(x, y, V, c=None, fill=None):
        return ''.join(mcell(x, y + i * h, V[i][0], w, h, c, fill) for i in range(2))
    def mat(x, y, A, c=None):
        return ''.join(mcell(x + j * w, y + i * h, A[i][j], w, h, c) for i in range(2) for j in range(2))
    def arr(x1, x2, y): return arrow(x1 + 6, y + h, x2 - 6, y + h, MU, 1.2)
    YA, YB, YC = 44, 150, 256
    # row A: two layers
    f.static(S(0, YA - 12, 'two layers', MU, bold=True))
    f.static(col(XS['x'], YA, XV) + M(XS['x'] + w / 2, YA + 2 * h + 18, '{x}', MU))
    f.static(mat(XS['W1'], YA, W1) + M(XS['W1'] + w, YA + 2 * h + 18, '{W}₁', MU))
    f.static(mat(XS['W2'], YA, W2) + M(XS['W2'] + w, YA + 2 * h + 18, '{W}₂', MU))
    f.static(arr(XS['x'] + w, XS['W1'], YA) + arr(XS['W1'] + 2 * w, XS['h'], YA) + arr(XS['h'] + w, XS['W2'], YA) +
             arr(XS['W2'] + 2 * w, XS['y'], YA))
    f.path(col(XS['W1'] + w / 2, YA, XV, FI, tn(FI, '.10')), [(0, XS['x'] - XS['W1'] - w / 2, 0), (.8, 0, 0)], .4, d=.6, hide=1.5)
    f.show(col(XS['h'], YA, H) + M(XS['h'] + w / 2, YA + 2 * h + 18, '{h}', MU), 1.5)
    f.path(col(XS['W2'] + w / 2, YA, H, FI, tn(FI, '.10')), [(0, XS['h'] - XS['W2'] - w / 2, 0), (2.0, 0, 0)], 1.7, d=.6, hide=2.7)
    f.show(col(XS['y'], YA, Y, FI, tn(FI, '.10')) + M(XS['y'] + w / 2, YA + 2 * h + 18, '{y}', MU), 2.7)
    # row B: merge
    f.show(S(0, YB - 12, 'merged', MU, bold=True), 3.2)
    MX = 275
    f.path(mat(MX - 2 * w - 4, YB, W1), [(0, XS['W1'] - MX + 2 * w + 4, YA - YB), (3.4, 0, 0)], 3.2, d=.8, hide=4.6)
    f.path(mat(MX + 4, YB, W2), [(0, XS['W2'] - MX - 4, YA - YB), (3.4, 0, 0)], 3.2, d=.8, hide=4.6)
    f.show(mat(MX - w, YB, W, BR) + M(MX, YB + 2 * h + 18, '{W} = {W}₂{W}₁', BR), 4.6)
    f.static(col(XS['x'], YB, XV) + M(XS['x'] + w / 2, YB + 2 * h + 18, '{x}', MU))
    f.show(arr(XS['x'] + w, MX - w, YB) + arr(MX + w, XS['y'], YB), 4.6)
    f.path(col(MX - w / 2, YB, XV, FI, tn(FI, '.10')), [(0, XS['x'] - MX + w / 2, 0), (5.4, 0, 0)], 5.2, d=.6, hide=6.1)
    f.show(col(XS['y'], YB, YW, GR, tn(GR, '.12')), 6.1)
    f.show(chip(XS['y'] + w + 86, YB + h, 'same y · one layer', GR, 150), 6.4)
    # row C: with ReLU
    f.show(S(0, YC - 12, 'with ReLU between', MU, bold=True), 7.2)
    f.show(col(XS['x'], YC, XV) + mat(XS['W1'], YC, W1) + mat(XS['W2'], YC, W2) +
           arr(XS['x'] + w, XS['W1'], YC) + arr(XS['W1'] + 2 * w, XS['h'] - 20, YC) + arr(XS['h'] + w, XS['W2'], YC), 7.3)
    f.show(col(XS['h'] - 20, YC, H) + T(XS['h'] - 20 + w / 2, YC + 2 * h + 18, 'h', FA), 7.8)
    f.show(arrow(XS['h'] + 18, YC + h, XS['h'] + 34, YC + h, AM, 1.4) + T(XS['h'] + 26, YC - 8, 'ReLU', AM, bold=True), 8.3)
    f.show(col(XS['h'] + 2 + w - 30 + 26, YC, HR) , 8.6)  # placeholder overwritten below
    return f, (XS, YC, w, h, col)

def fig_collapse_done():
    f, (XS, YC, w, h, col) = fig_collapse()
    # replace the placeholder: relu output column sits at h-x + 40
    f.items.pop()
    RX = XS['h'] + 40
    f.show(mcell(RX, YC, 0, w, h, RD, tn(RD, '.12')) + mcell(RX, YC + h, 4, w, h) + T(RX + w / 2, YC + 2 * h + 18, 'ReLU(h)', FA), 8.6)
    f.show(arrow(RX + w + 6, YC + h, XS['W2'] - 6, YC + h, MU, 1.2), 8.6)
    f.show(arrow(XS['W2'] + 2 * w + 6, YC + h, XS['y'] - 6, YC + h, MU, 1.2), 9.2)
    f.show(col(XS['y'], YC, YR, RD, tn(RD, '.12')), 9.4)
    f.show(chip(XS['y'] + w + 86, YC + h, 'y = (4, 8) ≠ W x', RD, 150), 9.8)
    return finish(f, YC + 2 * h + 12)

# ---------- 02 one figure per function ----------
FACTS = {'sigmoid': ('range (0, 1)', 'largest slope 0.25'), 'tanh': ('range (−1, 1)', 'largest slope 1'),
         'relu': ('range [0, ∞)', 'slope 0 or 1'), 'leaky': ('range (−∞, ∞)', 'slope %g or 1' % SLOPE),
         'gelu': ('range [−0.17, ∞)', 'largest slope 1.13')}
assert round(min(FN['gelu'][0](i / 100) for i in range(-400, 400)), 2) == -.17

def fig_fn(k, pre, title):
    fz, dfz = FN[k]
    rows = [(z, fz(z), dfz(z)) for z in ZIN]
    aria = ('The %s curve is drawn on z from −3 to 3, then its derivative as a dashed curve. Three inputs z = −2, 0.5 and '
            '2 rise from the axis to the curve; each output and each slope travels into the table: %s.') % (
        title, '; '.join('z %s gives %s, slope %s' % (N(z, 1), N(a), N(d)) for z, a, d in rows))
    f = Anim(pre, 720, 0, aria, '%s · CURVE, SLOPE, THREE INPUTS' % title.upper())
    P = Plane(200, 190, 55, 50)
    f.static(P.grid(-3, 3, -1, 3, 1, True, xl='{z}'))
    pts = [P(i / 20, fz(i / 20)) for i in range(-60, 61)]
    for i in range(0, 120, 12): f.show(poly(pts[i:i + 13], FI, 2.6), .2 + i / 120 * .9, d=.1)
    dpts = [P(i / 20, dfz(i / 20)) for i in range(-60, 61)]
    for i in range(0, 120, 12): f.show(poly(dpts[i:i + 13], AM, 1.8, '5 3'), 1.3 + i / 120 * .7, d=.1)
    tb = Table(430, 34, [('z', 70), ('φ(z)', 90), ('φ′(z)', 90)])
    f.static(T(tb.cx(0), tb.hb, 'z', MU) + T(tb.cx(1), tb.hb, 'φ(z)  output', FI, bold=True) +
             T(tb.cx(2), tb.hb, 'φ′(z)  slope', AM, bold=True) + L(tb.x, tb.line, tb.x + tb.w, tb.line))
    t = 2.4
    for i, (z, a, d) in enumerate(rows):
        f.show(tb.row(i, [N(z, 1), '', '']), t)
        f.show(dot(P.X(z), P.Y(0), BR, 4), t)
        f.path(dot(P.X(z), P.Y(a), FI, 5, BG), [(0, 0, P.Y(0) - P.Y(a)), (t + .4, 0, 0)], t + .2, d=.5)
        cx, cy = tb.cx(1), tb.ry(i) + 17
        f.path(num(cx, cy, N(a), FI, True), [(0, P.X(z) + 14 - cx, P.Y(a) - cy), (t + 1.0, 0, 0)], t + .9, d=.6)
        f.show(L(P.X(z), P.Y(0), P.X(z), P.Y(d), AM, 1, '2 3') +
               '<circle cx="%.1f" cy="%.1f" r="6" fill="none" stroke="%s" stroke-width="1.8"/>' % (P.X(z), P.Y(d), AM), t + 1.6)
        cx = tb.cx(2)
        f.path(num(cx, cy, N(d), AM, True), [(0, P.X(z) + 14 - cx, P.Y(d) - cy), (t + 2.0, 0, 0)], t + 1.9, d=.6)
        t += 2.6
    a, b = FACTS[k]
    f.show(chip(tb.x + 62, 172, a, FI, 124) + chip(tb.x + 192, 172, b, AM, 132), t)
    return finish(f, 272)

# ---------- 03 six sigmoid layers ----------
A = [1.0]
for _ in range(6): A.append(sig(A[-1]))
D = [sig(z) * (1 - sig(z)) for z in A[:6]]           # local slope of layer k (input A[k-1])
G = [1.0]
for d in reversed(D): G.append(G[-1] * d)
G = G[::-1]                                            # G[k] = gradient arriving at the input of layer k+1; G[6] = 1
assert [round(v, 3) for v in A] == [1, .731, .675, .663, .660, .659, .659]
assert round(G[0], 6) == .000109 and round(G[5], 3) == .225 and round(D[0], 3) == .197

def fig_vanish():
    f = Anim('act7-', 720, 0, 'A value 1.0 passes through six sigmoid layers left to right: 0.73, 0.68, 0.66, 0.66, 0.66, 0.66. '
             'Then the gradient starts at 1 on the right and travels back; every layer multiplies it by its slope, at most '
             '0.25, so the bars shrink: 0.22, 0.050, 0.011, 0.0025, 0.00056, 0.00011 at the first layer. The same chain '
             'with ReLU on positive inputs multiplies by 1 and every bar stays 1.',
             'FORWARD THROUGH 6 SIGMOIDS · GRADIENT BACK · × SLOPE EACH LAYER')
    xs = [30] + [120 + k * 92 for k in range(6)] + [680]
    YN = 64
    f.static(L(xs[0], YN, xs[-1], YN, RULE_HI, 1.2))
    f.static(R(xs[0] - 20, YN - 14, 40, 28, BG, RULE_HI, 6) + T(xs[0], YN + 4, 'x', TX, mono=True, bold=True))
    for k in range(1, 7):
        f.static('<circle cx="%.1f" cy="%d" r="18" fill="%s" stroke="%s" stroke-width="1.6"/>' % (xs[k], YN, BG, BR) +
                 T(xs[k], YN + 5, 'σ', BR, cls='sv-s', bold=True) + T(xs[k], YN - 26, 'layer %d' % k, FA))
    f.static(R(xs[7] - 20, YN - 14, 40, 28, BG, RULE_HI, 6) + T(xs[7], YN + 4, 'L', TX, mono=True, bold=True))
    f.static(num(xs[0], YN + 36, N(A[0]), FI, True))
    # forward
    f.path(dot(xs[7] - 30, YN, FI, 6, BG), [(0, xs[0] - xs[7] + 30, 0)] + [(.6 + k * .5, xs[k + 1] - xs[7] + 30, 0) for k in range(6)]
           + [(3.6, 0, 0)], .3, d=.4, hide=4.2)
    for k in range(1, 7): f.show(num(xs[k], YN + 36, N(A[k]), FI, True), .6 + (k - 1) * .5 + .4)
    # backward bars
    B1, B2, HMAX = 232, 340, 64
    f.static(S(0, 150, 'sigmoid · gradient reaching each layer', MU, bold=True) + S(0, 268, 'ReLU · same chain, z > 0', MU, bold=True))
    f.static(L(xs[1] - 30, B1, xs[-1] + 26, B1, RULE_HI) + L(xs[1] - 30, B2, xs[-1] + 26, B2, RULE_HI))
    t0 = 4.4
    f.path(dot(xs[1] + 30, YN, AM, 6, BG), [(0, xs[7] - xs[1] - 30, 0)] + [(t0 + .5 + j * .7, xs[6 - j] - xs[1] - 30, 0) for j in range(6)]
           + [(t0 + 4.7, 0, 0)], t0, d=.5, hide=t0 + 5.4)
    def bar(x, base, v, c):
        hh = max(v * HMAX, 1.5)
        return R(x - 13, base - hh, 26, hh, tn(c, '.35'), c, 2, 1.2)
    f.show(bar(xs[7], B1, 1, AM) + num(xs[7], B1 + 15, '1', AM, True) + bar(xs[7], B2, 1, GR) + num(xs[7], B2 + 15, '1', GR, True), t0)
    for j in range(6):
        k = 6 - j; t = t0 + .5 + j * .7 + .5
        g = G[k - 1]
        f.show(T(xs[k], YN + 52, '× %s' % N(D[k - 1]), AM, mono=True), t - .2)
        s = ('%.2f' if g >= .1 else '%.3f' if g >= .01 else '%.4f' if g >= .001 else '%.5f') % g
        f.show(bar(xs[k], B1, g, RD if g < .01 else AM) + num(xs[k], B1 + 15, s, RD if g < .01 else AM, True), t)
        f.show(bar(xs[k], B2, 1, GR) + num(xs[k], B2 + 15, '1', GR, True), t)
    f.show(chip(390, 146, '1 → 0.0001 in six layers', RD, 190), t0 + 5.2)
    return finish(f, B2 + 26)

# ---------- 04 dying ReLU ----------
DX = [.5, 1, 1.5, 2]; DY = DX
def train_neuron(alpha, steps=400, lr=.1, w=.6, b=-3.0):
    hist = {}
    for e in range(steps + 1):
        hist[e] = (w, b)
        gw = gb = 0
        for x, y in zip(DX, DY):
            z = w * x + b; hgt = z if z > 0 else alpha * z; dh = 1 if z > 0 else alpha
            gw += 2 * (hgt - y) * dh * x / 4; gb += 2 * (hgt - y) * dh / 4
        w -= lr * gw; b -= lr * gb
    return hist
HR0 = train_neuron(0.0); HL0 = train_neuron(SLOPE)
ZD = [.6 * x - 3 for x in DX]
STEPS = (0, 50, 100, 400)
assert all(HR0[s] == (.6, -3.0) for s in STEPS)
assert [tuple(round(v, 2) for v in HL0[s]) for s in STEPS] == [(.6, -3), (2.0, -1.56), (1.65, -1.02), (1.0, -0.0)]
assert all(z < 0 for z in ZD)

def fig_dying():
    f = Anim('act8-', 720, 0, 'One ReLU neuron with w = 0.6 and b = −3 meets four rows x = 0.5, 1, 1.5, 2. Every pre-activation '
             'z is negative, from −2.7 to −1.8; each z travels onto the flat part of the ReLU curve, so every output is 0 and '
             'every gradient is 0. Training for 400 steps leaves w and b exactly at 0.60 and −3.00. The same neuron with a '
             'leaky slope 0.1 gets a small gradient and moves to w = 1.00, b = 0.00.',
             'EVERY ROW LANDS ON THE FLAT PART · GRADIENT 0 · NO UPDATE')
    tb = Table(0, 34, [('x', 40), ('z', 56), ('ReLU', 50), ('grad', 50)])
    f.static(tb.head())
    P = Plane(400, 170, 50, 42)
    f.static(L(P.X(-3), P.Y(0), P.X(1.5), P.Y(0), RULE_HI, 1.2) + L(P.X(0), P.Y(-.3), P.X(0), P.Y(1.6), RULE_HI, 1.2) +
             M(P.X(1.5) + 6, P.Y(0) + 5, '{z}', MU, 'start'))
    for k in (-2, -1, 1): f.static(T(P.X(k), P.Y(0) + 15, N(k, 0), FA))
    f.static(poly([P(-3, 0), P(0, 0), P(1.5, 1.5)], FI, 2.6) + T(P.X(1.1), P.Y(1.5) + 2, 'ReLU', FI, 'end', bold=True))
    f.static(T(P.X(-1.5), P.Y(0) - 52, 'w = 0.6 · b = −3', MU, mono=True))
    t = .4
    for i, (x, z) in enumerate(zip(DX, ZD)):
        f.show(tb.row(i, [N(x, 1), N(z, 1), '', '']), t)
        f.path(dot(P.X(z), P.Y(0), RD, 5, BG), [(0, tb.cx(1) - P.X(z), tb.ry(i) + 13 - P.Y(0)), (t + .5, 0, 0)], t + .3, d=.7)
        f.show(tb.cell(i, 2, '0', 'rd') + tb.cell(i, 3, '0', 'rd'), t + 1.3)
        t += 1.1
    f.show(R(P.X(-3) - 4, P.Y(0) - 8, P.X(0) - P.X(-3) + 8, 16, 'none', RD, 8, 1.6) + T(P.X(-1.5), P.Y(0) + 32, 'flat · slope 0', RD, bold=True), t + .4)
    T2 = Table(506, 34, [('step', 44), ('ReLU', 82, 'w, b'), ('leaky 0.1', 82, 'w, b')])
    f.show(T2.head(), t + .8)
    t += 1.2
    for i, s in enumerate(STEPS):
        r = HR0[s]; l = HL0[s]
        f.show(T2.row(i, [str(s), '%s, %s' % (N(r[0]), N(r[1])), '%s, %s' % (N(l[0]), N(abs(l[1]) if abs(l[1]) < .005 else l[1]))],
                      colors={1: RD if s else TX, 2: GR if s else TX}), t)
        t += .7
    f.show(T(T2.cx(1), T2.ry(4) + 18, 'never moves', RD, bold=True) + T(T2.cx(2), T2.ry(4) + 18, 'fits y = x', GR, bold=True), t)
    return finish(f, max(T2.ry(4) + 28, P.Y(0) + 44))

# ---------- 05 output heads ----------
OZ = [-1.5, .4, 2.2]; OP = [sig(z) for z in OZ]
assert [round(p, 3) for p in OP] == [.182, .599, .900]
SZ = [2.0, 1.0, .1]; SE = [math.exp(z) for z in SZ]; SS = sum(SE); SP = [e / SS for e in SE]
assert [round(e, 2) for e in SE] == [7.39, 2.72, 1.11] and round(SS, 2) == 11.21
assert [round(p, 3) for p in SP] == [.659, .242, .099] and abs(sum(SP) - 1) < 1e-12

def fig_head(kind):
    soft = kind == 'soft'
    if soft:
        f = Anim('act10-', 720, 0, 'One image, three classes cat, dog, bird with logits 2.0, 1.0, 0.1. Each logit travels into '
                 'exp: 7.39, 2.72, 1.11. The three exps travel down into one sum, 11.21. Each exp divided by the sum travels '
                 'to the probability column: 0.66, 0.24, 0.10, bars that add up to 1. The largest, cat, is the prediction.',
                 'ONE ROW · LOGITS → exp → DIVIDE BY THE SUM → PROBABILITIES THAT ADD TO 1')
        names, Z = ('cat', 'dog', 'bird'), SZ
        cols = [('class', 70), ('logit z', 80), ('exp(z)', 90), ('p', 80)]
    else:
        f = Anim('act9-', 720, 0, 'Three emails with logits −1.5, 0.4 and 2.2. Each logit travels through the sigmoid on its own '
                 'and becomes a probability of spam: 0.18, 0.60, 0.90. A threshold at 0.5 gives no, spam, spam.',
                 'EACH ROW ON ITS OWN · LOGIT → σ → P(spam) → LABEL')
        names, Z = ('email 1', 'email 2', 'email 3'), OZ
        cols = [('row', 70), ('logit z', 80), ('p = σ(z)', 100)]
    tb = Table(0, 34, cols)
    f.static(tb.head())
    BX, BW = tb.x + tb.w + 30, 180
    f.static(T(BX + BW / 2, tb.hb, 'probability', MU) + L(BX, tb.line, BX + BW, tb.line) +
             L(BX + BW, tb.line + 2, BX + BW, tb.ry(2) + tb.rh + 2, RULE, 1, '2 3') + T(BX + BW, tb.ry(2) + tb.rh + 16, '1', FA))
    t = .3
    for i, (n, z) in enumerate(zip(names, Z)):
        f.show(tb.row(i, [n, N(z, 1)] + [''] * (len(cols) - 2)), t); t += .25
    Pv = SP if soft else OP
    mid = [SE[i] if soft else OP[i] for i in range(3)]
    t += .3
    for i in range(3):
        cy = tb.ry(i) + 17
        f.path(num(tb.cx(2), cy, N(mid[i]), BR if soft else FI, True), [(0, tb.cx(1) - tb.cx(2), 0), (t + .3, 0, 0)], t, d=.6)
        t += .9
    if soft:
        SY = tb.ry(3) + 30
        f.show(R(tb.cx(2) - 55, SY - 15, 110, 30, BG, BR, 6, 1.4) + num(tb.cx(2), SY + 5, 'Σ = %s' % N(SS), BR, True), t + .6)
        for i in range(3):
            f.path(num(tb.cx(2), SY + 5, N(SE[i]), BR), [(0, 0, tb.ry(i) + 17 - SY - 5), (t, 0, 0)], t - .1, d=.6, hide=t + .7)
        t += 1.4
        for i in range(3):
            cy = tb.ry(i) + 17
            f.show(T(tb.cx(3) - 40, cy, '÷', MU, mono=True), t)
            f.path(num(tb.cx(3), cy, N(SP[i]), FI, True), [(0, tb.cx(2) - tb.cx(3), SY + 5 - cy), (t + .3, 0, 0)], t, d=.7)
            t += .9
    for i in range(3):
        y = tb.ry(i) + 4
        f.show(R(BX, y, BW, 18, SUNK, 'none', 3) + R(BX, y, max(Pv[i] * BW, 1.5), 18, tn(FI, '.40'), FI, 3, 1.2), t + i * .2)
    t += .9
    LX = BX + BW + 60
    if soft:
        best = max(range(3), key=lambda i: SP[i])
        f.show(tb.outline(best, best, c=GR, sw=1.8) + chip(LX, tb.ry(best) + 13, 'cat', GR, 60), t)
        f.show(S(BX, tb.ry(3) + 20, 'bars add up to %s' % N(sum(SP)), FI, bold=True), t + .4)
        return finish(f, tb.ry(3) + 52)
    f.show(L(BX + BW / 2, tb.line + 2, BX + BW / 2, tb.ry(2) + tb.rh + 2, VI, 1.6, '5 3') +
           T(BX + BW / 2, tb.ry(2) + tb.rh + 16, 'threshold 0.5', VI, bold=True), t)
    for i in range(3):
        y = tb.ry(i) + 13; yes = OP[i] >= .5
        f.show(chip(LX, y, 'spam' if yes else 'no', GR if yes else MU_C, 60), t + .5 + i * .2)
    return finish(f, tb.ry(3) + 30)
MU_C = BR

SCRIPT = re.search(r'<script>.*?</script>', dt.BODY, re.S).group(0)

def EQ(*lines):
    return '  <div class="eq">\n' + ''.join('    <div class="line">\n%s\n    </div>\n' % l for l in lines) + '  </div>'
def t_(s, em, cls=''): return '      <span class="t%s"><span>%s</span><em>%s</em></span>' % (' ' + cls if cls else '', s, em)
def op(s): return '      <span class="op">%s</span>' % s

def fn_eq(lhs, rhs, em, dl, drhs, dem):
    return EQ('\n'.join([t_(lhs, 'activation', 'g'), op('='), t_(rhs, em, 'g')]),
              '\n'.join([t_(dl, 'slope', 'p'), op('='), t_(drhs, dem, 'p')]))

V = lambda s: '<var>%s</var>' % s
FR = lambda a, b: '<span class="frac"><i>%s</i><i>%s</i></span>' % (a, b)
EQS = {
 'sigmoid': fn_eq('σ(%s)' % V('z'), FR('1', '1 + ' + V('e') + '<sup>−' + V('z') + '</sup>'), 'squashes into (0, 1)',
                  'σ′(%s)' % V('z'), 'σ(%s) (1 − σ(%s))' % (V('z'), V('z')), 'at most 0.25, at z = 0'),
 'tanh': fn_eq('<b class="fn">tanh</b>(%s)' % V('z'), '2σ(2%s) − 1' % V('z'), 'a sigmoid stretched to (−1, 1)',
               '<b class="fn">tanh</b>′(%s)' % V('z'), '1 − <b class="fn">tanh</b><sup>2</sup>(%s)' % V('z'), 'at most 1, at z = 0'),
 'relu': fn_eq('<b class="fn">ReLU</b>(%s)' % V('z'), '<b class="fn">max</b>(0, %s)' % V('z'), 'negatives cut to 0',
               '<b class="fn">ReLU</b>′(%s)' % V('z'), '1 if %s &gt; 0, else 0' % V('z'), 'all or nothing'),
 'leaky': fn_eq('<b class="fn">LeakyReLU</b>(%s)' % V('z'), '<b class="fn">max</b>(%s, %s)' % (V('αz'), V('z')), 'α small, e.g. 0.01',
                '<b class="fn">LeakyReLU</b>′(%s)' % V('z'), '1 if %s &gt; 0, else %s' % (V('z'), V('α')), 'never exactly 0'),
 'gelu': fn_eq('<b class="fn">GELU</b>(%s)' % V('z'), '%s · Φ(%s)' % (V('z'), V('z')), 'Φ = normal CDF: keep z with probability Φ(z)',
               '<b class="fn">GELU</b>′(%s)' % V('z'), 'Φ(%s) + %s φ<sub>N</sub>(%s)' % (V('z'), V('z'), V('z')), 'φ<sub>N</sub> = normal density'),
}

BODY = r'''<header class="hero">
  <p class="eyebrow">Deep learning · Neural network</p>
  <h1>Activation <em>functions</em></h1>
  <p class="lede">An activation function bends each layer's weighted sum, and without that bend a deep network <b>collapses into one linear map</b>.</p>
</header>

<section id="act-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Two linear layers multiply into <em>one matrix</em>; a nonlinear φ between them stops the merge.</p>
''' + EQ('\n'.join([t_('%s<sub>2</sub>(%s<sub>1</sub>%s)' % (V('W'), V('W'), V('x')), 'two layers, no φ', 'r'), op('='),
                    t_('(%s<sub>2</sub>%s<sub>1</sub>)%s' % (V('W'), V('W'), V('x')), 'regroup'), op('='),
                    t_('%s%s' % (V('W'), V('x')), 'one layer', 'r')]),
         '\n'.join([t_(V('h'), 'layer output'), op('='), t_('φ', 'applied to every number', 'p'), op('('),
                    t_('%s%s + %s' % (V('W'), V('x'), V('b')), 'weighted sum z', 'b'), op(')')])) + r'''
{f1}
  <ul class="why">
    <li>Any number of stacked linear layers is still one line, so a network without φ cannot even solve XOR — see <a href="../neural-network-overview/index.html">Neural network overview</a>.</li>
    <li>φ works element by element on <span class="mth"><var>z</var></span>; what it does to the <b>slope</b> φ′ matters as much as its shape, because backprop multiplies by φ′ at every layer.</li>
  </ul>
</section>

<section id="act-s2" class="lesson">
  <div class="sh"><b>02</b><h2>The common functions</h2></div>
  <p class="key">Each one is a curve and a slope; the same three inputs <em>z = −2, 0.5, 2</em> go through all of them.</p>
  <div class="subsec" id="act-s2-1">
    <h3 class="ssh"><b>2.1</b>Sigmoid</h3>
    <p class="skey">Squashes any z into <em>(0, 1)</em>; flat at both ends.</p>
{eq_sigmoid}
{f2}
    <ul class="why">
      <li>Slope is at most 0.25 and nearly 0 for |z| &gt; 4: the <b>saturation</b> behind section 03.</li>
      <li>Outputs are all positive, so the next layer's gradients all share one sign and zig-zag. Today it lives in output layers and gates (LSTM), not hidden layers.</li>
    </ul>
  </div>
  <div class="subsec" id="act-s2-2">
    <h3 class="ssh"><b>2.2</b>Tanh</h3>
    <p class="skey">A sigmoid stretched to <em>(−1, 1)</em> and centred on zero.</p>
{eq_tanh}
{f3}
    <ul class="why">
      <li>Zero-centred outputs and a slope up to 1 train faster than sigmoid, but it still saturates for large |z|.</li>
      <li>The default inside RNN and LSTM cells.</li>
    </ul>
  </div>
  <div class="subsec" id="act-s2-3">
    <h3 class="ssh"><b>2.3</b>ReLU</h3>
    <p class="skey">Keep positive z, <em>cut negatives to 0</em>.</p>
{eq_relu}
{f4}
    <ul class="why">
      <li>Slope exactly 1 for every positive z: no saturation on that side, and it costs one comparison. The default for hidden layers since AlexNet (2012).</li>
      <li>Slope 0 for every negative z — a neuron stuck there stops learning (section 04). Pair it with He initialization.</li>
    </ul>
  </div>
  <div class="subsec" id="act-s2-4">
    <h3 class="ssh"><b>2.4</b>Leaky ReLU &amp; ELU</h3>
    <p class="skey">ReLU with a <em>small slope on the negative side</em>, so the gradient never dies.</p>
{eq_leaky}
{f5}
    <ul class="why">
      <li>Drawn with α = 0.1 to be visible; PyTorch's default is 0.01. <b>PReLU</b> learns α.</li>
      <li><b>ELU</b> bends smoothly to −1 instead of a straight line: ELU(−2) = <span class="mth">%s</span>, slope <span class="mth"><var>e</var><sup><var>z</var></sup></span> for z &lt; 0.</li>
    </ul>
  </div>
  <div class="subsec" id="act-s2-5">
    <h3 class="ssh"><b>2.5</b>GELU</h3>
    <p class="skey">A <em>smooth ReLU</em>: z weighted by the chance a normal draw is below it.</p>
{eq_gelu}
{f6}
    <ul class="why">
      <li>The activation inside the Transformer feed-forward block: BERT, GPT-2/3, ViT all use GELU.</li>
      <li><b>SiLU / Swish</b> is the same idea with σ in place of Φ: <span class="mth"><var>z</var> · σ(<var>z</var>)</span>, SiLU(−2) = <span class="mth">%s</span>; SwiGLU in LLaMA builds on it.</li>
    </ul>
  </div>
</section>

<section id="act-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Saturation &amp; vanishing gradients</h2></div>
  <p class="key">The gradient reaching layer 1 is a <em>product of slopes</em>; slopes below 1 shrink it layer by layer.</p>
''' + EQ('\n'.join([t_(FR('∂' + V('L'), '∂' + V('a') + '<sub>0</sub>'), 'gradient at the first layer', 'r'), op('='),
                    t_('φ′(%s<sub>1</sub>) · φ′(%s<sub>2</sub>) ⋯ φ′(%s<sub>6</sub>)' % (V('z'), V('z'), V('z')), 'one slope per layer, here ≤ 0.25 each', 'p'),
                    op('·'), t_(FR('∂' + V('L'), '∂' + V('a') + '<sub>6</sub>'), 'gradient at the output')])) + r'''
{f7}
  <ul class="why">
    <li>With weights the factor is <span class="mth"><var>w</var> · φ′</span>; the full story, and its opposite (exploding), is in <a href="../backpropagation/index.html">Backpropagation</a>.</li>
    <li>ReLU's slope of 1 lets the gradient pass unchanged, which is why deep nets switched to it.</li>
  </ul>
</section>

<section id="act-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Dying ReLU</h2></div>
  <p class="key">A neuron whose z is <em>negative for every row</em> outputs 0, gets gradient 0, and never recovers.</p>
{f8}
  <ul class="why">
    <li>Usually caused by a too-large learning rate or a large negative bias knocking the neuron past every row; check the share of zeros per layer.</li>
    <li>Fixes: a smaller learning rate, Leaky ReLU / GELU, and <a href="../weight-initialization/index.html">He initialization</a>, which is sized for ReLU.</li>
  </ul>
</section>

<section id="act-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Output layer</h2></div>
  <p class="key">Hidden layers use ReLU or GELU; the last layer uses <em>whatever turns logits into the answer's shape</em>.</p>
  <div class="subsec" id="act-s5-1">
    <h3 class="ssh"><b>5.1</b>Binary: sigmoid</h3>
    <p class="skey">One logit per row becomes <em>one probability</em> of the positive class.</p>
''' + EQ('\n'.join([t_(V('p'), 'P(class 1)', 'g'), op('='), t_('σ(%s)' % V('z'), 'z = the raw output, the logit', 'b')])) + r'''
{f9}
    <ul class="why">
      <li>Also for <b>multi-label</b> (an image can be cat <i>and</i> dog): one sigmoid per label, each on its own.</li>
      <li>Train on the logit with <code>BCEWithLogitsLoss</code>; it applies σ inside, more stably.</li>
    </ul>
  </div>
  <div class="subsec" id="act-s5-2">
    <h3 class="ssh"><b>5.2</b>Multiclass: softmax</h3>
    <p class="skey">K logits become <em>K probabilities that add up to 1</em>.</p>
''' + EQ('\n'.join([t_(V('p') + '<sub>' + V('k') + '</sub>', 'P(class k)', 'g'), op('='),
                    t_(FR(V('e') + '<sup>' + V('z') + '<sub>' + V('k') + '</sub></sup>',
                          'Σ<sub>' + V('j') + '</sub> ' + V('e') + '<sup>' + V('z') + '<sub>' + V('j') + '</sub></sup>'), 'exp, then divide by the sum', 'b')])) + r'''
{f10}
    <ul class="why">
      <li>Exactly one class is right. <code>CrossEntropyLoss</code> takes the raw logits — adding a softmax before it applies softmax twice.</li>
      <li>Regression keeps the output <b>linear</b> (no φ); a positive target can use softplus or exp.</li>
    </ul>
  </div>
</section>

''' + SCRIPT + r'''

<footer>Deep learning · Neural network · next lesson in the group: <a href="../backpropagation/index.html">Backpropagation</a>.</footer>
'''
BODY = BODY.replace('%s', N(ELU(-2), 3), 1).replace('%s', N(SILU(-2), 3), 1)

def build():
    figs = dict(f1=fig_collapse_done(), f2=fig_fn('sigmoid', 'act2-', 'Sigmoid'), f3=fig_fn('tanh', 'act3-', 'Tanh'),
                f4=fig_fn('relu', 'act4-', 'ReLU'), f5=fig_fn('leaky', 'act5-', 'Leaky ReLU'),
                f6=fig_fn('gelu', 'act6-', 'GELU'), f7=fig_vanish(), f8=fig_dying(), f9=fig_head('sig'), f10=fig_head('soft'))
    figs.update({'eq_' + k: v for k, v in EQS.items()})
    return re.sub(r'\{((?:f|eq_)[a-z0-9]+)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">'); b = s.index('</article>')
    s = s[:a] + body + '      ' + s[b:]
    s = re.sub(r'<article class="doc"[^>]*>', lambda m: re.sub(r' data-(skeleton|reviewed|progress)="\d"', '', m.group(0)), s, count=1)
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s" data-progress="1"' % blurb, s, count=1)
    open(page, 'w').write(s)

if __name__ == '__main__':
    splice(PAGE, build(), 'Why a network needs a bend: sigmoid, tanh, ReLU, Leaky ReLU and GELU with their slopes, '
           'vanishing gradients, dying ReLU, and sigmoid or softmax at the output.')
