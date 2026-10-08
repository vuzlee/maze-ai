# -*- coding: utf-8 -*-
"""Figures + body for content/08-deep-learning/01-overview/dl-overview (shelf overview).
Every number is computed here in pure Python with fixed seeds: a 2-4-1 network trained on XOR-shaped
points, the perceptron rule failing on XOR, a 2-2-1 network solving it, a 3x3 kernel over a 6x6 image
and a one-unit RNN over four inputs. Run: python3 dl_overview.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from mlplot import (Anim, T, R, L, arrow, pill, tint, COL, AM, GR, RD, BL, MU, TX, FA, RULE_HI,
                    Plot, dot, ringc, poly, clipline, frame_box, palette, sig)

PAGE = os.path.join(HERE, '../../../content/08-deep-learning/01-overview/dl-overview/index.html')
RULE, BG = 'var(--rule)', 'var(--bg)'

# ---------- a tiny MLP (tanh hidden, sigmoid out, full-batch GD) ----------
def train(X, Y, H, seed, epochs, lr, snaps):
    g = random.Random(seed)
    W1 = [[g.gauss(0, 1) for _ in range(2)] for _ in range(H)]; b1 = [g.gauss(0, .5) for _ in range(H)]
    W2 = [g.gauss(0, 1) for _ in range(H)]; b2 = 0.0
    out, curve = {}, []
    for ep in range(epochs + 1):
        gW1 = [[0, 0] for _ in range(H)]; gb1 = [0] * H; gW2 = [0] * H; gb2 = 0; loss = 0
        for (a, b), t in zip(X, Y):
            h = [math.tanh(W1[j][0] * a + W1[j][1] * b + b1[j]) for j in range(H)]
            o = sig(sum(W2[j] * h[j] for j in range(H)) + b2)
            loss -= t * math.log(max(o, 1e-12)) + (1 - t) * math.log(max(1 - o, 1e-12))
            e = o - t; gb2 += e
            for j in range(H):
                gW2[j] += e * h[j]; dh = e * W2[j] * (1 - h[j] ** 2)
                gW1[j][0] += dh * a; gW1[j][1] += dh * b; gb1[j] += dh
        loss /= len(X); curve.append(loss)
        if ep in snaps: out[ep] = ([r[:] for r in W1], b1[:], W2[:], b2, loss)
        n = len(X)
        for j in range(H):
            W2[j] -= lr * gW2[j] / n; b1[j] -= lr * gb1[j] / n
            W1[j][0] -= lr * gW1[j][0] / n; W1[j][1] -= lr * gW1[j][1] / n
        b2 -= lr * gb2 / n
    return out, curve

def prob(m, a, b):
    W1, b1, W2, b2, _ = m
    return sig(sum(W2[j] * math.tanh(W1[j][0] * a + W1[j][1] * b + b1[j]) for j in range(len(W2))) + b2)

# XOR-shaped point cloud in [-1, 1]^2: class 1 where x*y < 0
_g = random.Random(8)
XP, XY = [], []
for cx, cy in [(-.55, -.55), (.55, .55), (-.55, .55), (.55, -.55)]:
    for _ in range(7):
        XP.append((cx + _g.gauss(0, .17), cy + _g.gauss(0, .17))); XY.append(1 if cx * cy < 0 else 0)
SN = [0, 40, 120, 400, 1500]
MM, MCURVE = train(XP, XY, 4, 2, SN[-1], .5, set(SN))
def acc(m): return sum((prob(m, *p) > .5) == t for p, t in zip(XP, XY))
ACC = [acc(MM[s]) for s in SN]
assert len(XP) == 28 and ACC[-1] == 28 and ACC[0] < 20, ACC
assert MCURVE[-1] < .1 < MCURVE[0], (MCURVE[0], MCURVE[-1])

def net_svg(x0, y0, sizes, W=None, gap=110, vgap=58, labels=None, tone='bl'):
    """Neuron circles in layers; W[l][i][j] = weight from neuron j of layer l to neuron i of layer l+1."""
    pos = []
    for l, n in enumerate(sizes):
        top = y0 + (max(sizes) - n) * vgap / 2
        pos.append([(x0 + l * gap, top + i * vgap) for i in range(n)])
    s = ''
    for l in range(len(sizes) - 1):
        for i, (x2, y2) in enumerate(pos[l + 1]):
            for j, (x1, y1) in enumerate(pos[l]):
                w = W[l][i][j] if W else 1
                sw = min(.6 + 1.3 * abs(w), 5.5)
                s += L(x1 + 13, y1, x2 - 13, y2, COL[tone] if W else RULE_HI, '%.1f' % sw, None if w >= 0 else '4 3')
    for l, ps in enumerate(pos):
        for i, (x, y) in enumerate(ps):
            s += '<circle cx="%.1f" cy="%.1f" r="13" fill="%s" stroke="%s" stroke-width="1.5"/>' % (x, y, BG, TX)
            if labels and labels[l]: s += T(x, y + 4.5, labels[l][i], TX, 'middle', 'sv-m')
    return s, pos

def shade_grid(pl, f_, n=18, tone1='am', tone0='bl'):
    cw, ch = pl.pw / n, pl.ph / n; g = ''
    for i in range(n):
        for j in range(n):
            x = pl.x0 + (i + .5) / n * (pl.x1 - pl.x0); y = pl.y0 + (j + .5) / n * (pl.y1 - pl.y0)
            c = f_(x, y)
            g += R(pl.px + i * cw, pl.py + pl.ph - (j + 1) * ch, cw + .3, ch + .3, tint(tone1 if c else tone0, '.16'), 'none', 0)
    return g

# ---------- 01 mental model ----------
def fig_mental():
    f = Anim('dlo1-', 720, 420, 'A network of two inputs, four hidden neurons and one output sits next to 28 dots in four corners: '
             'top-left and bottom-right are one class, the other two corners the other. Training runs; at each snapshot the edges thicken or thin '
             'as the weights change, the coloured regions of the plot reshape, and the loss curve below is drawn further. '
             'At epoch 1500 the regions cover all four corners and every dot is right.',
             'A TINY NETWORK LEARNS · DOTS → WEIGHTS → BOUNDARY')
    pl = Plot(420, 46, 270, 270, -1.2, 1.2, -1.2, 1.2)
    f.static(frame_box(pl) + T(pl.px + pl.pw / 2, pl.py + pl.ph + 20, 'x₁', MU, cls='sv-m') + T(pl.px - 10, pl.py + pl.ph / 2, 'x₂', MU, 'end', 'sv-m'))
    lab = [['x₁', 'x₂'], ['', '', '', ''], ['ŷ']]
    base, pos = net_svg(60, 60, [2, 4, 1], None, 120, 50, lab)
    f.static(T(60, 40, 'input', MU) + T(180, 40, 'hidden', MU) + T(300, 40, 'output', MU))
    for i, (p, t) in enumerate(zip(XP, XY)):
        f.show(dot(*pl.P(*p), 4.5, 'am' if t else 'bl'), .2 + i * .025, d=.2)
    # loss curve frame
    lp = Plot(60, 300, 260, 70, 0, SN[-1], 0, MCURVE[0] * 1.05)
    f.static(L(lp.px, lp.py + lp.ph, lp.px + lp.pw, lp.py + lp.ph, MU, 1.2) + L(lp.px, lp.py + lp.ph, lp.px, lp.py - 4, MU, 1.2) +
             T(lp.px - 6, lp.py + 6, 'loss', MU, 'end') + T(lp.px + lp.pw, lp.py + lp.ph + 16, 'epoch %d' % SN[-1], FA, 'end', mono=True))
    t = 1.2; step = 1.3
    for k, s in enumerate(SN):
        last = k == len(SN) - 1; m = MM[s]
        W = [[m[0][i] for i in range(4)], [m[2]]]
        edges, _ = net_svg(60, 60, [2, 4, 1], W, 120, 50)
        hide = None if last else t + step - .3
        f.show(shade_grid(pl, lambda a, b: prob(m, a, b) > .5), t, hide=hide, d=.3)
        f.show(edges, t, hide=hide, d=.3)
        a, b0 = (SN[k - 1] if k else 0), s
        if k:
            seg = [lp.P(e, MCURVE[e]) for e in range(a, b0 + 1, 5)]
            f.show(poly(seg, GR, 2), t, d=.4)
        tone = 'gr' if last else 'am'
        f.show(R(395, 344, 300, 40, BG, 'none', 0) + T(420, 362, 'epoch %d' % s, COL[tone], 'start', mono=True, bold=True) +
               T(420, 378, 'loss %.2f' % m[4], MU, 'start', mono=True) +
               pill(640, 351, '%d / 28 right' % ACC[k], tone, 100), t, hide=hide, d=.3)
        t += step
    f.static(base)
    f.static(T(130, 285, 'solid = positive weight · dashed = negative · width = size', FA))
    return f.render()

# ---------- 02 one neuron vs a hidden layer, on XOR ----------
XOR = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]
def perceptron(epochs=6):
    w = [.6, -.4, .1]; hist = []
    for _ in range(epochs):
        for (a, b), t in XOR:
            y = 1 if w[0] * a + w[1] * b + w[2] > 0 else 0
            w = [w[0] + .5 * (t - y) * a, w[1] + .5 * (t - y) * b, w[2] + .5 * (t - y)]
        wrong = sum((1 if w[0] * a + w[1] * b + w[2] > 0 else 0) != t for (a, b), t in XOR)
        hist.append((tuple(w), wrong))
    return hist
PH = perceptron()
assert min(h[1] for h in PH) >= 1
def xor_net():
    X = [p for p, _ in XOR]; Y = [t for _, t in XOR]
    for seed in range(50):
        m, c = train(X, Y, 2, seed, 3000, 1.0, {3000})
        m = m[3000]
        if all((prob(m, *p) > .5) == t for p, t in XOR) and c[-1] < .05: return seed, m, c
SEED2, XN, XC = xor_net()
assert XC[-1] < .05

def xor_plot(f, x0):
    pl = Plot(x0, 50, 230, 230, -.4, 1.4, -.4, 1.4)
    f.static(frame_box(pl) + T(pl.px + pl.pw / 2, pl.py + pl.ph + 20, 'x₁', MU, cls='sv-m') + T(pl.px - 10, pl.py + pl.ph / 2, 'x₂', MU, 'end', 'sv-m'))
    for (a, b), t in XOR:
        f.static(T(pl.X(a), pl.Y(b) + (32 if b == 0 else -20), '(%d,%d)' % (a, b), FA, mono=True))
    return pl

def fig_perceptron():
    f = Anim('dlo2-', 720, 330, 'The four XOR points: (0,1) and (1,0) are one class, (0,0) and (1,1) the other. A single neuron draws one line and '
             'the perceptron rule moves it after each pass; every line it tries leaves at least one point on the wrong side, ringed in red.',
             'ONE NEURON · ONE STRAIGHT LINE')
    pl = xor_plot(f, 60)
    for (a, b), t in XOR: f.static(dot(*pl.P(a, b), 8, 'am' if t else 'bl'))
    n, pos = net_svg(440, 110, [2, 1], None, 140, 80, [['x₁', 'x₂'], ['ŷ']])
    f.static(n + T(510, 80, 'ŷ = step(w₁x₁ + w₂x₂ + b)', MU, cls='sv-m'))
    t = .6
    for k, (w, wrong) in enumerate(PH[:5]):
        last = k == 4; seg = clipline(pl, *w)
        hide = None if last else t + .9
        g = ''
        if seg: (a, b), (c, d) = seg; g += L(a, b, c, d, AM, 2.2)
        g += ''.join(ringc(*pl.P(*p), 13, RD, 2) for p, tt in XOR if (1 if w[0] * p[0] + w[1] * p[1] + w[2] > 0 else 0) != tt)
        g += T(440, 240, 'pass %d' % (k + 1), AM, 'start', mono=True, bold=True) + T(440, 262, '%d of 4 wrong' % wrong, RD, 'start', mono=True)
        g = R(436, 222, 250, 48, BG, 'none', 0) + g
        f.show(g, t, hide=hide, d=.3); t += .9
    f.show(pill(560, 286, 'no line fits XOR', 'rd', 160), t)
    return f.render()

def fig_hidden():
    W1, b1, W2, b2, _ = XN
    f = Anim('dlo3-', 720, 330, 'The same four XOR points. Two hidden neurons each draw their own line; the output neuron combines them, '
             'so the region between the two lines becomes one class and the corners the other. All four points are right.',
             'A HIDDEN LAYER · TWO LINES, COMBINED')
    pl = xor_plot(f, 60)
    n, pos = net_svg(440, 110, [2, 2, 1], [[W1[0], W1[1]], [W2]], 110, 80, [['x₁', 'x₂'], ['h₁', 'h₂'], ['ŷ']])
    f.static(n)
    f.show(shade_grid(pl, lambda a, b: prob(XN, a, b) > .5, 20), 2.4, d=.6)
    for (a, b), t in XOR: f.static(dot(*pl.P(a, b), 8, 'am' if t else 'bl'))
    for j in range(2):
        (a, b), (c, d) = clipline(pl, W1[j][0], W1[j][1], b1[j])
        f.show(L(a, b, c, d, BL, 2, '6 4') + T((a + c) / 2 + 8, (b + d) / 2 - 6, 'h%s' % '₁₂'[j], BL, 'start', 'sv-m'), .6 + j * .8)
        f.show(ringc(*pos[1][j], 18, AM, 2), .6 + j * .8, hide=1.4 + j * .8)
    f.show(ringc(*pos[2][0], 18, AM, 2), 2.4)
    f.show(pill(560, 286, '4 of 4 right', 'gr', 140), 3.2)
    return f.render()

# ---------- 03 the shared timeline ----------
TL = [('1958', 'Perceptron', 'learns weights from data instead of hand rules', 0),
      ('1969', 'XOR limit', 'one neuron = one straight line → AI winter', 2),
      ('1986', 'Backpropagation', 'hidden layers can be trained → MLP', 0),
      ('1989', 'CNN', 'shares one small filter across the whole image', 0),
      ('1991', 'Vanishing gradients', 'deep and long nets stop learning', 2),
      ('1997', 'LSTM', 'gates carry the signal across long sequences', 0),
      ('2010', 'ReLU · init · GPU', 'gradients survive depth; training takes days, not months', 0),
      ('2012', 'AlexNet', 'data + GPU + ReLU beat hand-made features on ImageNet', 0),
      ('2015', 'ResNet', 'skip connections let 100+ layers train', 0),
      ('2015', 'Attention', 'no single fixed-size vector between encoder and decoder', 0),
      ('2017', 'Transformer', 'drops recurrence: the whole sequence trains in parallel', 1),
      ('2020', 'Scale', 'loss falls predictably with more data, parameters, compute', 1),
      ('2021', 'Mixture of Experts', 'more parameters, same compute per token', 1),
      ('2023', 'SSM · Mamba', 'linear time on very long sequences', 1)]
HERE_UNTIL = 9
def fig_timeline():
    rh, y0 = 29, 56
    h = y0 + len(TL) * rh + 30
    f = Anim('dlo4-', 720, h, 'A vertical timeline of fourteen milestones from the perceptron in 1958 to Mamba in 2023. A marker walks down it; '
             'each row lights up with the bottleneck it removed, and the two walls (XOR, vanishing gradients) light up in red. '
             'Rows up to attention belong to this shelf and stay bright; Transformer, scale, mixture of experts and Mamba stay dimmed, '
             'they belong to the next shelves.', 'ONE TIMELINE · EACH STEP REMOVES THE LAST BOTTLENECK')
    xl = 110
    f.static(L(xl, y0 - 8, xl, y0 + (len(TL) - 1) * rh + 8, RULE_HI, 3))
    yb = y0 + HERE_UNTIL * rh + rh / 2
    f.static(L(20, yb, 700, yb, RULE_HI, 1, '4 4') + T(700, y0 - 16, 'this shelf', BL, 'end', bold=True) +
             T(700, y0 + len(TL) * rh + 10, 'dimmed: Transformer & LLM shelves', FA, 'end'))
    t = .4
    for i, (yr, name, why, kind) in enumerate(TL):
        y = y0 + i * rh; dim = kind == 1
        c = FA if dim else (RD if kind == 2 else TX)
        f.static(T(xl - 18, y + 5, yr, FA, 'end', mono=True))
        f.static('<circle cx="%d" cy="%.1f" r="6" fill="%s" stroke="%s" stroke-width="1.6"/>' % (xl, y, BG, RULE_HI))
        g = ('<circle cx="%d" cy="%.1f" r="6" fill="%s"/>' % (xl, y, RD if kind == 2 else (RULE_HI if dim else BL)) +
             T(xl + 22, y + 5, name, c, 'start', 'sv-s', bold=not dim) + T(xl + 210, y + 5, why, FA if dim else (RD if kind == 2 else MU), 'start'))
        f.show(g, t, d=.3)
        t += .32 if dim else .45
    f.path('<circle cx="%d" cy="%d" r="10" fill="none" stroke="%s" stroke-width="2.2"/>' % (xl, y0, AM),
           [(0, 0, 0)] + [(.4 + sum(.45 for _ in range(k)), 0, k * rh) for k in range(1, HERE_UNTIL + 1)], t0=.2, d=.3)
    return f.render()

# ---------- 04 branches ----------
def fig_dense():
    x = [1.0, .5, -1.0]; W = [[.8, -.4, .3], [-.5, .9, .2], [.4, .6, -.7]]
    z = [sum(w * v for w, v in zip(r, x)) for r in W]; h = [max(0, v) for v in z]
    o = .7 * h[0] + .5 * h[1] - .6 * h[2]
    assert [round(v, 2) for v in z] == [.30, -.25, 1.40] and [round(v, 2) for v in h] == [.30, 0, 1.40] and round(o, 2) == -.63
    f = Anim('dlo5-', 720, 260, 'Three input values travel along every edge into three hidden neurons; each neuron adds its weighted inputs, '
             'negative sums are cut to zero, and the hidden values travel on into one output.', 'DENSE (MLP) · EVERY INPUT TO EVERY NEURON')
    n, pos = net_svg(120, 60, [3, 3, 1], [W, [[.7, .5, -.6]]], 230, 70)
    f.static(n)
    t = .4
    for j, (px, py) in enumerate(pos[0]):
        f.static(T(px - 22, py + 5, '%.1f' % x[j], TX, 'end', mono=True, bold=True))
    for j, (px, py) in enumerate(pos[0]):
        for i, (qx, qy) in enumerate(pos[1]):
            f.path(R(px - 13, py - 9, 26, 18, tint('bl', '.25'), BL, 9, 1) + T(px, py + 4, '%.1f' % x[j], BL, mono=True),
                   [(0, 0, 0), (t + j * .9 + .4, qx - px, qy - py)], t0=t + j * .9, d=.7, hide=t + j * .9 + 1.2)
    t += 3.4
    for i, (qx, qy) in enumerate(pos[1]):
        f.show(R(qx + 18, qy - 34, 64, 20, BG, RULE_HI, 4, 1) + T(qx + 50, qy - 20, 'z %.2f' % z[i], MU, mono=True), t)
        f.show('<circle cx="%.1f" cy="%.1f" r="13" fill="%s" stroke="%s" stroke-width="1.5"/>' % (qx, qy, tint('gr' if h[i] else 'rd', '.3'), GR if h[i] else RD) +
               T(qx, qy + 4, '%.1f' % h[i], GR if h[i] else RD, mono=True, bold=True), t + .6)
    t += 1.4
    ox, oy = pos[2][0]
    for i, (qx, qy) in enumerate(pos[1]):
        f.path(R(qx - 13, qy - 9, 26, 18, tint('gr', '.25'), GR, 9, 1) + T(qx, qy + 4, '%.1f' % h[i], GR, mono=True),
               [(0, 0, 0), (t + .4, ox - qx, oy - qy)], t0=t, d=.8, hide=t + 1.3)
    t += 1.5
    f.show(T(ox + 24, oy + 5, 'ŷ = %.2f' % o, AM, 'start', mono=True, bold=True), t)
    f.static(T(250, 245, 'hidden = ReLU(W·x): sums below zero become 0', FA))
    return f.render()

IMG = [[0, 0, 0, 1, 1, 1]] * 6
KER = [[1, 0, -1]] * 3
CONV = [[sum(IMG[r + i][c + j] * KER[i][j] for i in range(3) for j in range(3)) for c in range(4)] for r in range(4)]
assert CONV[0] == [0, -3, -3, 0]
def fig_conv():
    f = Anim('dlo6-', 720, 290, 'A six by six image, dark on the left and bright on the right. A three by three filter slides over it one step '
             'at a time; at each stop it multiplies and sums, and the number drops into a four by four feature map. '
             'The map lights up exactly in the two middle columns where the edge is.', 'CONVOLUTION · ONE SMALL FILTER SLIDES OVER THE IMAGE')
    cs = 34; ix, iy = 40, 50; ox, oy = 470, 84
    for r in range(6):
        for c in range(6):
            f.static(R(ix + c * cs, iy + r * cs, cs, cs, tint('bl', '.35') if IMG[r][c] else BG, RULE_HI, 0) +
                     T(ix + c * cs + cs / 2, iy + r * cs + 22, str(IMG[r][c]), TX, mono=True))
    for r in range(4):
        for c in range(4):
            f.static(R(ox + c * cs, oy + r * cs, cs, cs, BG, RULE_HI, 0))
    f.static(T(ix + 3 * cs, iy - 12, 'image', MU) + T(ox + 2 * cs, oy - 12, 'feature map', MU))
    f.static(T(330, 70, 'filter', MU) + ''.join(T(304 + j * 26, 92 + i * 22, '%+d' % KER[i][j] if KER[i][j] else '0', AM, mono=True) for i in range(3) for j in range(3)))
    t = .5; dt = .32; path = [(0, 0, 0)]
    for k in range(16):
        r, c = divmod(k, 4)
        if k: path.append((t, c * cs, r * cs))
        v = CONV[r][c]
        f.show(R(ox + c * cs + 1, oy + r * cs + 1, cs - 2, cs - 2, tint('am' if v else 'bl', '.3') if v else BG, 'none', 0) +
               T(ox + c * cs + cs / 2, oy + r * cs + 22, str(v), AM if v else MU, mono=True, bold=bool(v)), t + .25, d=.15)
        t += dt
    f.path(R(ix, iy, 3 * cs, 3 * cs, 'none', AM, 2, 2.6), path, t0=.2, d=.22)
    f.show(T(ox + 2 * cs, oy + 4 * cs + 26, 'the edge, found by 9 shared weights', GR), t + .2)
    return f.render()

RX = [1.0, -.5, .8, .2]; RW, RU = .7, 1.2
RH = []
_h = 0.0
for v in RX: _h = math.tanh(RW * _h + RU * v); RH.append(_h)
assert [round(v, 2) for v in RH] == [.83, -.02, .74, .64], RH
def fig_rnn():
    f = Anim('dlo7-', 720, 250, 'Four inputs arrive one after another. The same cell reads each input together with the memory h from the step before, '
             'and the new h travels right into the next step. The last h summarises the whole sequence.', 'RECURRENCE · THE SAME CELL, STEP BY STEP')
    X0, G = 70, 160; y = 110
    t = .4
    for k, v in enumerate(RX):
        cx = X0 + k * G
        f.static(R(cx - 36, y - 26, 72, 52, BG, RULE_HI, 8, 1.4) + T(cx, y + 5, 'cell', FA))
        f.static(T(cx, 222, 'x%s = %.1f' % ('₁₂₃₄'[k], v), TX, mono=True) + arrow(cx, 204, cx, y + 30, MU, 1.3))
        f.path(R(cx - 22, 182, 44, 18, tint('bl', '.25'), BL, 9, 1) + T(cx, 195, '%.1f' % v, BL, mono=True),
               [(0, 0, 0), (t + .3, 0, -(182 - y - 40))], t0=t, d=.5, hide=t + .9)
        f.show(R(cx - 30, y - 12, 60, 24, BG, 'none', 0) + T(cx, y + 5, 'h %.2f' % RH[k], GR, mono=True, bold=True), t + .9)
        if k < 3:
            f.static(arrow(cx + 38, y, cx + G - 38, y, MU, 1.3))
            f.path(R(cx - 26, y - 52, 52, 18, tint('gr', '.25'), GR, 9, 1) + T(cx, y - 39, '%.2f' % RH[k], GR, mono=True),
                   [(0, 0, 0), (t + 1.3, G, 0)], t0=t + 1.0, d=.6, hide=t + 2.1)
        t += 2.0
    f.static(T(X0 - 6, 50, 'h = tanh(0.7·h + 1.2·x)', MU, 'start', 'sv-m'))
    f.show(pill(X0 + 3 * G, 30, 'sums the sequence', 'gr', 150), t)
    return f.render()

# ---------- 05 learning order ----------
ORDER = [('Perceptron & MLP', '../../02-neural-network/perceptron-mlp/index.html'),
         ('Activation functions', '../../02-neural-network/activation-functions/index.html'),
         ('Backpropagation', '../../02-neural-network/backpropagation/index.html'),
         ('Weight initialization', '../../02-neural-network/weight-initialization/index.html'),
         ('Normalization', '../../02-neural-network/normalization/index.html'),
         ('Optimizer', '../../03-optimizer/optimizer-overview/index.html'),
         ('Dropout', '../../02-neural-network/dropout-regularization/index.html'),
         ('Convolution', '../../04-cnn/convolution-basics/index.html'),
         ('CNN · MobileNet', '../../04-cnn/cnn-mobilenet/index.html'),
         ('RNN', '../../05-sequence/rnn/index.html'),
         ('LSTM & GRU', '../../05-sequence/lstm-gru/index.html'),
         ('Training recipe', '../../06-training/training-recipe-debug/index.html'),
         ('Generative models', '../../07-generative/generative-models/index.html'),
         ('→ Transformer shelf', '../../../09-transformer/01-overview/architecture-overview/index.html')]
for _, href in ORDER: assert os.path.exists(os.path.join(os.path.dirname(PAGE), href)), href
GROUPS = [(0, 7, 'Neural network'), (7, 9, 'CNN'), (9, 11, 'Sequence'), (11, 13, 'Training · generative'), (13, 14, 'next shelf')]
def fig_order():
    rows = [ORDER[:7], ORDER[7:]]
    f = Anim('dlo8-', 720, 260, 'Fourteen stops in two rows. A marker travels from Perceptron and MLP through the neural-network basics, '
             'then convolution, sequence models, the training recipe and generative models, and ends at the Transformer shelf.',
             'LEARNING ORDER · ONE NETWORK FIRST, THEN SHAPES OF DATA')
    X = [60 + i * 100 for i in range(7)]; Y = [86, 196]
    t = .4; k = 0
    for r, row in enumerate(rows):
        f.static(L(X[0], Y[r], X[len(row) - 1], Y[r], RULE_HI, 3))
        for i, (name, href) in enumerate(row):
            last = k == len(ORDER) - 1
            f.static('<circle cx="%d" cy="%d" r="9" fill="%s" stroke="%s" stroke-width="2"/>' % (X[i], Y[r], BG, RULE_HI))
            words = name.split(' ', 1) if len(name) > 13 else [name]
            lbl = ''.join(T(X[i], Y[r] - 20 - 14 * (len(words) - 1 - j), w_, TX if not last else GR, 'middle', 'sv-s') for j, w_ in enumerate(words))
            f.static('<a href="%s">%s</a>' % (href, lbl))
            f.show('<circle cx="%d" cy="%d" r="9" fill="%s"/>' % (X[i], Y[r], GR if last else BL), t, d=.25)
            t += .3; k += 1
    for a, b, g in GROUPS:
        r = 0 if a < 7 else 1; i0, i1 = a - 7 * r, b - 1 - 7 * r
        f.static(L(X[i0] - 10, Y[r] + 24, X[i1] + 10, Y[r] + 24, MU, 1) + T((X[i0] + X[i1]) / 2, Y[r] + 40, g, FA))
    return f.render()

BODY = r'''<header class="hero">
  <p class="eyebrow">Deep learning · first lesson of the shelf</p>
  <h1>Deep learning <em>overview</em></h1>
  <p class="lede">A neural network stacks simple neurons into layers and lets gradient descent find the features; each milestone since 1958 removed <b>one bottleneck that stopped the last one</b>.</p>
</header>

<section id="dlov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Dots go in, weights move, and <em>the boundary bends itself</em> into the shape of the data — nobody writes the features.</p>
{f1}
  <ul class="why">
    <li>Continues <a href="../../../07-machine-learning/01-overview/ml-overview/index.html">Machine learning</a>: same loop of predict, loss, adjust — the model is now layers of neurons.</li>
    <li>Each hidden neuron learns one simple cut; the output combines them into a shape no single line can make.</li>
  </ul>
</section>

<section id="dlov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Why layers</h2></div>
  <p class="key">One neuron can only draw a straight line; <em>a hidden layer combines lines</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>a</var></span><em>neuron output</em></span>
      <span class="op">=</span>
      <span class="t p"><span><var>σ</var></span><em>activation</em></span>
      <span class="t b"><span>(<var>w</var> · <var>x</var> + <var>b</var>)</span><em>weighted sum + bias</em></span>
    </div>
  </div>
  <div class="subsec" id="dlov-s2-1">
    <h3 class="ssh"><b>2.1</b>Perceptron</h3>
    <p class="skey">One neuron, one line: on XOR <em>some point is always on the wrong side</em>.</p>
{f2}
    <ul class="why">
      <li>Minsky and Papert showed this limit in 1969; funding dried up — the first AI winter.</li>
    </ul>
  </div>
  <div class="subsec" id="dlov-s2-2">
    <h3 class="ssh"><b>2.2</b>Hidden layer</h3>
    <p class="skey">Two neurons draw two lines, the output <em>keeps the band between them</em>.</p>
{f3}
    <ul class="why">
      <li>Training hidden weights needs backpropagation (1986) and a smooth activation instead of a step.</li>
    </ul>
  </div>
</section>

<section id="dlov-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Timeline</h2></div>
  <p class="key">Every milestone is <em>the fix for the wall the previous one hit</em>.</p>
{f4}
  <ul class="why">
    <li>The 2012 jump needed three things at once: ImageNet-sized data, GPUs, and ReLU-style training tricks.</li>
    <li>This shelf ends where attention appears; the same timeline continues in the <a href="../../../09-transformer/01-overview/architecture-overview/index.html">Architecture overview</a>.</li>
  </ul>
</section>

<section id="dlov-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Main branches</h2></div>
  <p class="key">The layer type follows <em>the shape of the data</em>: a row, a grid, or a sequence.</p>
  <div class="subsec" id="dlov-s4-1">
    <h3 class="ssh"><b>4.1</b>Dense · MLP</h3>
    <p class="skey">Every input reaches every neuron: <em>for a row of numbers</em> with no order between them.</p>
{f5}
    <ul class="why">
      <li>Lessons: <a href="../../02-neural-network/perceptron-mlp/index.html">Perceptron &amp; MLP</a>. On plain tables, gradient-boosted trees usually still win.</li>
    </ul>
  </div>
  <div class="subsec" id="dlov-s4-2">
    <h3 class="ssh"><b>4.2</b>Convolution · CNN</h3>
    <p class="skey">One small filter is reused at every position: <em>for images and other grids</em>.</p>
{f6}
    <ul class="why">
      <li>Lessons: <a href="../../04-cnn/convolution-basics/index.html">Convolution</a>, <a href="../../04-cnn/cnn-mobilenet/index.html">CNN · MobileNet</a>.</li>
    </ul>
  </div>
  <div class="subsec" id="dlov-s4-3">
    <h3 class="ssh"><b>4.3</b>Recurrence · RNN</h3>
    <p class="skey">One cell is reused at every step, carrying a memory: <em>for sequences</em>.</p>
{f7}
    <ul class="why">
      <li>Lessons: <a href="../../05-sequence/rnn/index.html">RNN</a>, <a href="../../05-sequence/lstm-gru/index.html">LSTM &amp; GRU</a>. Steps run one after another, so training is slow — what the Transformer later fixed.</li>
    </ul>
  </div>
</section>

<section id="dlov-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Learning order</h2></div>
  <p class="key">Learn to train <em>one plain network</em> first; CNN and RNN are the same training with a different layer.</p>
{f8}
  <ul class="why">
    <li>Every stop is a link. The last one opens the <a href="../../../09-transformer/01-overview/architecture-overview/index.html">Transformer shelf</a>.</li>
  </ul>
</section>

{script}

<footer>Deep learning · first lesson of the shelf · next: <a href="../../02-neural-network/neural-network-overview/index.html">Neural network overview</a>.</footer>
'''

def build():
    import decision_tree as dt  # noqa: reuse its replay script
    src = open(dt.PAGE).read()
    script = re.search(r'<script>\n/\* Figures start.*?</script>', src, re.S).group(0)
    figs = dict(f1=fig_mental(), f2=fig_perceptron(), f3=fig_hidden(), f4=fig_timeline(), f5=fig_dense(),
                f6=fig_conv(), f7=fig_rnn(), f8=fig_order())
    figs = {k: palette(v) for k, v in figs.items()}
    figs['script'] = script
    return re.sub(r'\{(f\d|script)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">'); b = s.index('</article>')
    s = s[:a] + body + '\n      ' + s[b:]
    s = re.sub(r'<article class="doc"[^>]*>', lambda m: re.sub(r' data-(skeleton|reviewed|progress)="\d"', '', m.group(0)), s, count=1)
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s" data-progress="1"' % blurb, s, count=1)
    open(page, 'w').write(s)

if __name__ == '__main__':
    print('mental acc', ACC, 'loss %.3f -> %.3f' % (MCURVE[0], MCURVE[-1]), 'perceptron', [h[1] for h in PH], 'xor seed', SEED2)
    splice(PAGE, build(), 'One shared timeline from the perceptron to attention, each step removing a bottleneck; a tiny network '
           'learning XOR; dense, convolution and recurrence layers; and the order to learn this shelf.')
