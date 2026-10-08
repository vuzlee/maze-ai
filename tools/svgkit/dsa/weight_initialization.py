# -*- coding: utf-8 -*-
"""Figures + body for content/08-deep-learning/02-neural-network/weight-initialization.
Every number is computed here: a 2-3-1 sigmoid network on XOR trained in pure Python (constant vs random
init), and a 10-layer, 64-wide network fed 128 Gaussian inputs (seed 1) for the activation spread per layer.
Run: python3 weight_initialization.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, BR, VI, FI, RO, RULE, SUNK, BG, tn, M, S, chip, dot, finish
from tablefig import GR, RD, AM, tint, pill, Table

PAGE = os.path.join(HERE, '../../../content/08-deep-learning/02-neural-network/weight-initialization/index.html')

# ---------- XOR, 2-3-1 sigmoid network, full batch, lr 1 ----------
sig = lambda z: 1 / (1 + math.exp(-z))
XOR = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]

def forward(W, b, V, c, x):
    h = [sig(W[j][0] * x[0] + W[j][1] * x[1] + b[j]) for j in range(3)]
    return h, sig(sum(v * hh for v, hh in zip(V, h)) + c)

def grads(W, b, V, c):
    gW = [[0, 0] for _ in range(3)]; gb = [0] * 3; gV = [0] * 3; gc = 0; loss = 0
    for x, y in XOR:
        h, o = forward(W, b, V, c, x)
        loss += -(y * math.log(o) + (1 - y) * math.log(1 - o)) / 4
        d = (o - y) / 4; gc += d
        for j in range(3):
            gV[j] += d * h[j]; dh = d * V[j] * h[j] * (1 - h[j])
            gb[j] += dh; gW[j][0] += dh * x[0]; gW[j][1] += dh * x[1]
    return gW, gb, gV, gc, loss

def train(W, V, steps, snaps):
    b = [0.] * 3; c = 0.; out = {}
    for s in range(steps + 1):
        gW, gb, gV, gc, loss = grads(W, b, V, c)
        if s in snaps: out[s] = ([r[:] for r in W], V[:], loss)
        if s == steps: break
        for j in range(3):
            V[j] -= gV[j]; b[j] -= gb[j]; W[j][0] -= gW[j][0]; W[j][1] -= gW[j][1]
        c -= gc
    return out

SNAPS = (0, 1, 100, 2000)
CON = train([[.5, .5] for _ in range(3)], [.5] * 3, 2000, SNAPS)
g = random.Random(3)
RW = [[g.gauss(0, 1), g.gauss(0, 1)] for _ in range(3)]; RV = [g.gauss(0, 1) for _ in range(3)]
RND = train(RW, RV, 2000, SNAPS)
for s in SNAPS:   # the symmetry never breaks: three identical rows
    W = CON[s][0]; assert all(abs(W[j][k] - W[0][k]) < 1e-12 for j in range(3) for k in range(2))
H0, O0 = forward([[.5, .5]] * 3, [0] * 3, [.5] * 3, 0, (0, 1))
G0 = grads([[.5, .5] for _ in range(3)], [0] * 3, [.5] * 3, 0)[0]
assert round(H0[0], 2) == .62 and round(O0, 2) == .72 and len({round(r[1], 12) for r in G0}) == 1
ZG = grads([[0, 0] for _ in range(3)], [0] * 3, [0] * 3, 0)
assert all(v == 0 for v in ZG[0][0] + ZG[1] + ZG[2]) and ZG[3] == 0   # zero init on XOR: nothing moves
assert round(CON[2000][2], 2) == .49 and round(RND[2000][2], 3) == .008

# ---------- deep net: 10 layers of 64, 128 Gaussian inputs, seed 1 ----------
N, B, LAYERS = 64, 128, 10
relu = lambda z: z if z > 0 else 0.

def deep(act, std, seed=1):
    g = random.Random(seed)
    X = [[g.gauss(0, 1) for _ in range(N)] for _ in range(B)]
    out = []
    for _ in range(LAYERS):
        W = [[g.gauss(0, std) for _ in range(N)] for _ in range(N)]
        Z = [[sum(w * x for w, x in zip(Wr, xr)) for Wr in W] for xr in X]
        X = [[act(z) for z in zr] for zr in Z]
        zs = [z for zr in Z for z in zr]
        m = sum(zs) / len(zs)
        out.append((zs, math.sqrt(sum((z - m) ** 2 for z in zs) / len(zs))))
    return out

HE, XAV = math.sqrt(2 / N), math.sqrt(1 / N)
RUNS = {'small': deep(relu, .5 * HE), 'large': deep(relu, 2 * HE), 'he': deep(relu, HE),
        'xr': deep(relu, XAV), 'tx': deep(math.tanh, XAV), 'tn': deep(math.tanh, 1.0)}
SD = {k: [s for _, s in v] for k, v in RUNS.items()}
assert round(SD['small'][0], 2) == .70 and SD['small'][-1] < .005
assert round(SD['large'][-1]) == 1753 and round(SD['he'][0], 2) == 1.40 and round(SD['he'][-1], 2) == 1.71
assert 7.4 < min(SD['tn']) and max(SD['tn']) < 8
assert round(SD['xr'][-1], 3) == .054 and round(SD['tx'][0], 2) == .99 and round(SD['tx'][-1], 2) == .25

def hist(zs, lo=-3, hi=3, nb=12):
    w = (hi - lo) / nb; c = [0] * (nb + 2)
    for z in zs:
        c[0 if z < lo else nb + 1 if z >= hi else 1 + int((z - lo) / w)] += 1
    return [k / len(zs) for k in c]

# ---------- the 1/n rule, measured ----------
def var_sum(n, vw, trials=40000, seed=7):
    g = random.Random(seed); zs = []
    for _ in range(trials):
        zs.append(sum(g.gauss(0, math.sqrt(vw)) * g.gauss(0, 1) for _ in range(n)))
    m = sum(zs) / trials
    return sum((z - m) ** 2 for z in zs) / trials
VA, VB = var_sum(4, 1), var_sum(4, .25)
assert abs(VA - 4) < .1 and abs(VB - 1) < .03

# ---------- helpers ----------
def neuron(x, y, c=TX, fill=BG, r=14):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, y, r, fill, c)

f2 = lambda v: '%.2f' % v

# ---------- 01 Symmetry ----------
def fig_symmetry():
    f = Anim('wi1-', 720, 0, 'A network with two inputs, three hidden neurons and one output, every weight set to 0.5. The input '
             '0, 1 flows forward: all three hidden neurons get the same value 0.62 and the output is 0.72. The loss is computed, '
             'and the gradient flows back: each hidden neuron receives the same gradient. A table of the hidden weights fills '
             'in at epochs 0, 1, 100 and 2000: the three neurons stay identical, and the loss stalls at 0.49. The same '
             'network started from random weights ends with three different neurons and loss 0.008.',
             'SAME START · SAME VALUE · SAME GRADIENT · SAME NEURON FOREVER')
    IN = [(40, 100), (40, 190)]; HD = [(180, 70), (180, 145), (180, 220)]; OUT = (320, 145)
    def edges(Wh, Vo, c):
        s = ''
        for j, (hx, hy) in enumerate(HD):
            for k, (ix, iy) in enumerate(IN):
                s += L(ix + 14, iy, hx - 14, hy, c, '%.1f' % min(.8 + .45 * abs(Wh[j][k]), 4.5))
            s += L(hx + 14, hy, OUT[0] - 14, OUT[1], c, '%.1f' % min(.8 + .45 * abs(Vo[j]), 4.5))
        return s
    f.show(edges([[.5, .5]] * 3, [.5] * 3, RULE_HI), .1, hide=7.6)
    f.show(edges(CON[2000][0], CON[2000][1], FI), 7.6)
    for p, lab in zip(IN, ('x₁', 'x₂')):
        f.static(neuron(*p) + T(p[0] - 24, p[1] + 4, lab, MU, 'end', 'sv-m'))
    for j, p in enumerate(HD):
        f.static(neuron(*p, FI, tn(FI, '.14')) + T(p[0], p[1] + 4, 'h%s' % '₁₂₃'[j], FI, cls='sv-m'))
    f.static(neuron(*OUT) + T(OUT[0], OUT[1] + 4, 'ŷ', TX, cls='sv-m'))
    f.static(S(40, 262, 'every weight starts at 0.5', MU))
    # forward
    f.show(chip(40, 76, '0', VI, 28) + chip(40, 166, '1', VI, 28), .5, hide=3.2)
    for j, (hx, hy) in enumerate(HD):
        f.path(chip(hx, hy - 24, f2(H0[j]), VI, 44), [(0, 40 - hx, 166 - hy + 24), (1.2, 0, 0)], .9, d=.8, hide=3.2)
    f.path(chip(OUT[0], OUT[1] - 24, f2(O0), VI, 44), [(0, -140, 0), (2.4, 0, 0)], 2.1, d=.6, hide=3.2)
    # loss and backward
    l0 = CON[0][2]
    f.show(R(280, 196, 82, 40, BG, RD, 6, 1.4) + T(321, 212, 'loss', RD, bold=True) + T(321, 228, f2(l0), RD, mono=True), 3.0, hide=7.4)
    gtxt = '∂ %.3f' % G0[0][1]
    for j, (hx, hy) in enumerate(HD):
        f.path(chip(hx, hy + 24, gtxt, RO, 64), [(0, OUT[0] - hx, OUT[1] - hy + 50), (3.9, 0, 0)], 3.6, d=.8, hide=7.4)
    f.show(T(180, 262, 'same gradient for all three', RD, bold=True), 4.8, hide=7.4)
    # table of hidden weights
    tb = Table(410, 30, [('epoch', 52), ('h₁', 76, 'w₁, w₂'), ('h₂', 76, 'w₁, w₂'), ('h₃', 76, 'w₁, w₂')])
    f.static(tb.head())
    for i, s in enumerate(SNAPS):
        W = CON[s][0]
        f.show(tb.row(i, [str(s)] + ['%s, %s' % (f2(W[j][0]), f2(W[j][1])) for j in range(3)], colors={1: FI, 2: FI, 3: FI}),
               5.4 + i * .7)
    f.show(tb.outline(0, 3, 1, 3, RD, 1.8), 8.4)
    f.show(pill(tb.x + 140, tb.ry(4) + 6, 'three copies of one neuron · loss %s' % f2(CON[2000][2]), 'rd', 260), 8.6)
    W = RND[2000][0]
    yr = tb.ry(4) + 46
    f.show(T(tb.x, yr - 6, 'same network, random start, epoch 2000', MU, 'start', 'sv-s'), 9.4)
    f.show(R(tb.x, yr, tb.w, 26, tint('gr', '.12'), GR, 3, 1) + T(tb.cx(0), yr + 17, 'rand', GR) +
           ''.join(T(tb.cx(j + 1), yr + 17, '%.1f, %.1f' % (W[j][0], W[j][1]), GR) for j in range(3)), 9.6)
    f.show(pill(tb.x + 140, yr + 34, 'three different features · loss %.3f' % RND[2000][2], 'gr', 260), 10.0)
    return finish(f, yr + 60)

# ---------- spread strips (2.1, 2.2, 4.1, 4.2) ----------
X0, CW = 120, 59
def strip_row(f, y0, key, label, sub, tone, verdict, t0):
    c = {'gr': GR, 'rd': RD, 'bl': FI}[tone]
    top, bh = y0 + 26, 9          # 14 bins of 9 px: overflow, 12 bins of 0.5 from -3 to 3, overflow
    yb = lambda k: top + (13 - k) * bh
    f.static(T(0, y0 + 40, label, TX, 'start', 'sv-s', bold=True) + S(0, y0 + 56, sub, MU))
    f.static(T(X0 - 10, yb(0) + 7, '< −3', FA, 'end', mono=True) + T(X0 - 10, yb(7) + 4, '0', FA, 'end', mono=True) +
             T(X0 - 10, yb(13) + 7, '> 3', FA, 'end', mono=True))
    for l in range(LAYERS):
        x = X0 + l * CW
        f.static(T(x + 26, y0 + 14, 'layer %d' % (l + 1), FA) + R(x, top, 52, 14 * bh, SUNK, 'none', 3) +
                 L(x, yb(6), x + 52, yb(6), RULE, 1))
    for l in range(LAYERS):
        x = X0 + l * CW; t = t0 + .6 + l * .5
        h = hist(RUNS[key][l][0]); s = ''
        for k, v in enumerate(h):
            if v < .002: continue
            over = k in (0, 13)
            w = min(v * 140, 50)
            cc = RD if over else c
            s += R(x + 1, yb(k) + 1, w, bh - 2, tn(FI, '.35') if not over and tone == 'bl' else tint('rd' if over else tone, '.45'), cc, 1, .8)
        sd = SD[key][l]
        s += T(x + 26, top + 14 * bh + 16, ('σ %.3f' % sd) if sd < .1 else ('σ %d' % round(sd)) if sd >= 10 else ('σ %.2f' % sd),
               c if l == LAYERS - 1 else TX, mono=True, bold=(l == LAYERS - 1))
        f.show(s, t)
    f.path(dot(X0 + 26, top - 6, VI, 4.5), [(0, 0, 0)] + [(t0 + .6 + l * .5, l * CW, 0) for l in range(1, LAYERS)], t0 + .3, d=.4,
           hide=t0 + .6 + LAYERS * .5)
    f.show(pill(50, y0 + 70, verdict, tone, 96), t0 + .8 + LAYERS * .5)
    return top + 14 * bh + 24

def fig_strip(pre, rows, aria, cap):
    f = Anim(pre, 720, 0, aria, cap)
    y = 26; t = 0
    for r in rows:
        y = strip_row(f, y, *r, t) + 18; t += 6.0
    return finish(f, y - 10)

def fig_small():
    return fig_strip('wi2-', [('small', 'std ½ · √(2/n)', 'ReLU, n = 64', 'rd', 'vanished')],
                     'Ten layers side by side. Each column is a histogram of the 8192 pre-activations of one layer, values from minus 3 '
                     'to 3. A dot steps from layer to layer and each histogram appears as the signal arrives. With weights half the '
                     'right size the spread halves every layer: 0.70, 0.35, 0.17, down to 0.002 at layer 10, a single spike at zero.',
                     'SPREAD OF z PER LAYER · WEIGHTS TOO SMALL')

def fig_large():
    return fig_strip('wi3-', [('large', 'std 2 · √(2/n)', 'ReLU, n = 64', 'rd', 'exploded')],
                     'The same ten histograms with weights twice the right size. The spread doubles every layer: 2.8, 5.6, 11, up to '
                     '1753 at layer 10. From layer 3 on almost every value falls outside minus 3 to 3 and piles into the red overflow '
                     'bins at the top and bottom.', 'SPREAD OF z PER LAYER · WEIGHTS TOO LARGE')

def fig_xavier():
    return fig_strip('wi5-', [('tn', 'std 1', 'tanh, n = 64', 'rd', 'saturated'),
                              ('tx', 'Xavier · √(1/n)', 'tanh, n = 64', 'gr', 'in range')],
                     'Two rows of ten histograms for a tanh network. Top, weights drawn with std 1: the spread is about 8 from the first '
                     'layer, so most values sit in the red overflow bins where tanh is flat. Bottom, Xavier weights: the spread starts '
                     'at 0.99 and stays inside the range, easing to 0.25 by layer 10.', 'SPREAD OF z PER LAYER · tanh · NAIVE vs XAVIER')

def fig_he():
    return fig_strip('wi6-', [('xr', 'Xavier · √(1/n)', 'ReLU, n = 64', 'rd', 'fading'),
                              ('he', 'He · √(2/n)', 'ReLU, n = 64', 'gr', 'stable')],
                     'Two rows of ten histograms for a ReLU network. Top, Xavier weights: ReLU zeroes half the values, so the spread '
                     'shrinks every layer, 0.99 down to 0.054. Bottom, He weights, twice the variance: the spread holds near 1.4 '
                     'through all ten layers.', 'SPREAD OF z PER LAYER · ReLU · XAVIER vs HE')

# ---------- 03 The 1/n rule ----------
def fig_rule():
    f = Anim('wi4-', 720, 0, 'One neuron with four inputs. Each input times its weight is a term whose variance is drawn as a bar. '
             'With weights of variance 1 the four unit bars travel to the right and stack into Var(z) = 4, four times the input '
             'line. With weights of variance one quarter the four bars are a quarter tall and stack to exactly 1, on the line.',
             'VARIANCE OF A SUM = SUM OF THE VARIANCES')
    IN = [(30, 60 + i * 52) for i in range(4)]; NE = (210, 138)
    for i, p in enumerate(IN):
        f.static(L(p[0] + 13, p[1], NE[0] - 16, NE[1], RULE_HI, 1.3) + neuron(*p, TX, BG, 13) +
                 T(p[0], p[1] + 4, 'x%s' % '₁₂₃₄'[i], TX, cls='sv-m'))
    f.static(neuron(*NE, FI, tn(FI, '.14'), 16) + T(NE[0], NE[1] + 5, 'z', FI, cls='sv-m'))
    f.static(S(0, 278, 'Var(x) = 1 for every input · n = 4', MU))
    U, base = 36, 262
    cols = [(340, 1, VA, 'rd', 'Var(w) = 1'), (520, .25, VB, 'gr', 'Var(w) = 1/n = 1/4')]
    f.static(L(300, base, 690, base, RULE_HI, 1.3) + L(300, base - U, 690, base - U, AM, 1.4, '5 4') +
             T(692, base - U + 4, 'Var(x)', AM, 'start', 'sv-s', bold=True))
    for ci, (cx, vw, meas, tone, lab) in enumerate(cols):
        t0 = .6 + ci * 4.2; c = GR if tone == 'gr' else RD
        h = vw * U
        f.show(T(cx + 20, base + 18, lab, MU, cls='sv-s'), t0)
        for i, p in enumerate(IN):
            mx, my = p[0] + 64, p[1]
            bar = R(cx, base - (i + 1) * h, 40, h, tint(tone, '.30'), c, 2, 1.1)
            f.path(bar, [(0, mx - 20 - cx, my - h / 2 - (base - (i + 1) * h)), (t0 + 1.0 + i * .45, 0, 0)], t0 + .2 + i * .1, d=.7)
        f.show(T(cx + 20, base - 4 * h - 10, 'Var(z) = %.2f' % meas, c, cls='sv-s', bold=True), t0 + 3.2)
    f.show(pill(605, 40, '× n too big', 'rd', 90) + pill(605, 66, 'Var(w) = 1/n keeps it', 'gr', 150), 9.0)
    return finish(f, 290)

BODY = r'''<header class="hero">
  <p class="eyebrow">Deep learning · Neural network</p>
  <h1>Weight <em>initialization</em></h1>
  <p class="lede">Start every weight <b>random, different and the right size</b>, so neurons learn different things and the signal neither fades nor blows up across layers.</p>
</header>

<section id="wi-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Symmetry</h2></div>
  <p class="key">Neurons that start equal compute the same value, get the same gradient, and <em>stay equal forever</em>.</p>
{f1}
  <ul class="why">
    <li>Zero is the worst constant: on XOR every gradient is exactly 0 and nothing moves at all.</li>
    <li>Random weights break the tie; <b>biases can start at 0</b>, the weights already make each neuron different.</li>
  </ul>
</section>

<section id="wi-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Scale</h2></div>
  <p class="key">Each layer multiplies the spread of the signal by a factor; ten layers raise it to the <em>tenth power</em>.</p>
  <div class="subsec" id="wi-s2-1">
    <h3 class="ssh"><b>2.1</b>Too small</h3>
    <p class="skey">A factor below 1 shrinks the spread to <em>a spike at zero</em>.</p>
{f2}
    <ul class="why">
      <li>Every later layer sees almost the same input, and gradients shrink the same way: <b>vanishing gradients</b>.</li>
    </ul>
  </div>
  <div class="subsec" id="wi-s2-2">
    <h3 class="ssh"><b>2.2</b>Too large</h3>
    <p class="skey">A factor above 1 blows the spread up until values <em>overflow</em>.</p>
{f3}
    <ul class="why">
      <li>Sigmoid and tanh saturate, ReLU passes huge values on; gradients explode and the loss turns <code>NaN</code>: <b>exploding gradients</b>.</li>
    </ul>
  </div>
</section>

<section id="wi-s3" class="lesson">
  <div class="sh"><b>03</b><h2>The 1/n rule</h2></div>
  <p class="key">A neuron sums <var>n</var> terms, so the variance grows <em>n times</em> — shrink each weight's variance by n to cancel it.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span>Var(<var>z</var>)</span><em>spread after the layer</em></span>
      <span class="op">=</span>
      <span class="t b"><span><var>n</var></span><em>inputs summed</em></span>
      <span class="op">·</span>
      <span class="t p"><span>Var(<var>w</var>)</span><em>weight spread</em></span>
      <span class="op">·</span>
      <span class="t g"><span>Var(<var>x</var>)</span><em>spread before</em></span>
    </div>
    <div class="line">
      <span class="t"><span>Var(<var>z</var>) = Var(<var>x</var>)</span><em>keep the spread</em></span>
      <span class="op">⇒</span>
      <span class="t g"><span>Var(<var>w</var>) = <span class="frac"><i>1</i><i><var>n</var></i></span></span><em>std = √(1/n)</em></span>
    </div>
  </div>
{f4}
  <ul class="why">
    <li>Assumes weights and inputs are independent with mean 0 — true at the start, which is all init has to get right.</li>
    <li>After training starts the weights move; keeping the spread steady from then on is the job of <a href="../normalization/index.html">normalization</a>.</li>
  </ul>
</section>

<section id="wi-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Xavier and He</h2></div>
  <p class="key">The same rule, corrected for <em>what the activation does</em> to the spread.</p>
  <div class="subsec" id="wi-s4-1">
    <h3 class="ssh"><b>4.1</b>Xavier / Glorot</h3>
    <p class="skey">For <em>tanh and sigmoid</em>: average the forward need (1/n<sub>in</sub>) and the backward need (1/n<sub>out</sub>).</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span>Var(<var>w</var>)</span><em>Xavier</em></span>
      <span class="op">=</span>
      <span class="t g"><span><span class="frac"><i>2</i><i><var>n</var><sub>in</sub> + <var>n</var><sub>out</sub></i></span></span><em>= 1/n when the layer is square</em></span>
    </div>
  </div>
{f5}
    <ul class="why">
      <li>tanh is roughly linear near 0, so the plain 1/n rule holds; drawn too wide, values land where tanh is flat and its gradient is ~0.</li>
      <li>Keras <code>Dense</code> uses Xavier-uniform by default.</li>
    </ul>
  </div>
  <div class="subsec" id="wi-s4-2">
    <h3 class="ssh"><b>4.2</b>He / Kaiming</h3>
    <p class="skey">For <em>ReLU</em>: it zeroes half the values and halves the variance, so double the weight variance.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span>Var(<var>w</var>)</span><em>He</em></span>
      <span class="op">=</span>
      <span class="t g"><span><span class="frac"><i>2</i><i><var>n</var><sub>in</sub></i></span></span><em>the 2 undoes ReLU's half</em></span>
    </div>
  </div>
{f6}
    <ul class="why">
      <li>Use it for ReLU and its relatives (Leaky ReLU, GELU) — see <a href="../activation-functions/index.html">activation functions</a>.</li>
      <li>PyTorch <code>nn.Linear</code> defaults to a Kaiming-uniform variant (<code>a=√5</code>): U(−1/√n<sub>in</sub>, 1/√n<sub>in</sub>), a bit smaller than He; call <code>nn.init.kaiming_normal_</code> to get He exactly.</li>
    </ul>
  </div>
</section>

{script}

<footer>Deep learning · Neural network · next: <a href="../normalization/index.html">Normalization</a> keeps the spread steady during training.</footer>
'''

def replay_script():
    s = open(os.path.join(HERE, '../../../content/07-machine-learning/06-tree-models/decision-tree/index.html')).read()
    a = s.index('<script>\n/* Figures start'); b = s.index('</script>', a) + len('</script>')
    return s[a:b]

def build():
    figs = dict(f1=fig_symmetry(), f2=fig_small(), f3=fig_large(), f4=fig_rule(), f5=fig_xavier(), f6=fig_he(), script=replay_script())
    return re.sub(r'\{(f\d|script)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">'); b = s.index('</article>')
    s = s[:a] + body + '\n      ' + s[b:]
    s = re.sub(r'<article class="doc"[^>]*>', lambda m: re.sub(r' data-(skeleton|reviewed|progress)="\d"', '', m.group(0)), s, count=1)
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s" data-progress="1"' % blurb, s, count=1)
    s = s.replace('<script src="lab.js"></script>\n', '')
    open(page, 'w').write(s)

if __name__ == '__main__':
    print('tanh std1', [round(v, 2) for v in SD['tn']])
    splice(PAGE, build(), 'Zero or equal weights keep neurons identical; too small or too large weights make the signal fade or '
           'explode across layers; Var(w) = 1/n fixes the scale, Xavier for tanh, He for ReLU.')
