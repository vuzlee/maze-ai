# -*- coding: utf-8 -*-
"""Figures + body for content/08-deep-learning/02-neural-network/perceptron-mlp.
Every number is computed here in pure Python: the perceptron rule on AND (fixed start weights), the same rule
failing on XOR, and a 2-2-1 sigmoid network trained on XOR with full-batch gradient descent (seed 1).
Run: python3 perceptron_mlp.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, FI, RULE, BG, M, S, finish
from mlplot import Plot, clipline, frame_box, ringc, pill, tint, AM, GR, RD

PAGE = os.path.join(HERE, '../../../content/08-deep-learning/02-neural-network/perceptron-mlp/index.html')
X4 = [(0, 0), (0, 1), (1, 0), (1, 1)]
AND = [0, 0, 0, 1]; XOR = [0, 1, 1, 0]
ETA = .5
def step(z): return 1 if z > 0 else 0
def sig(z): return 1 / (1 + math.exp(-z))
def r2(v): return round(v + 0.0, 2)
def fm(v, n=1):
    s = ('%.' + str(n) + 'f') % v
    if s.startswith('-'): s = '−' + s[1:]
    return '0.0' if s in ('−0.0', '−0.00') else s

# ---------- perceptron rule ----------
def perceptron(Y, w, b, epochs):
    w = list(w); visits, hist = [], []
    for ep in range(epochs):
        for i, ((a, c), y) in enumerate(zip(X4, Y)):
            yh = step(w[0] * a + w[1] * c + b)
            old = (tuple(w), b)
            if yh != y:
                e = y - yh; w = [r2(w[0] + ETA * e * a), r2(w[1] + ETA * e * c)]; b = r2(b + ETA * e)
            visits.append((ep, i, yh, old, (tuple(w), b)))
        wrong = sum(step(w[0] * a + w[1] * c + b) != y for (a, c), y in zip(X4, Y))
        hist.append(((tuple(w), b), wrong))
        if Y is AND and all(v[3] == v[4] for v in visits[-4:]): break
    return visits, hist

W0, B0 = (0.2, 1.0), -0.4
AV, AH = perceptron(AND, W0, B0, 10)
WA, BA = AH[-1][0]
assert len(AV) == 12 and (WA, BA) == ((0.7, 0.5), -0.9) and AH[-1][1] == 0
assert sum(v[2] != AND[v[1]] for v in AV) == 3
ZA = [r2(WA[0] * a + WA[1] * c + BA) for a, c in X4]
assert ZA == [-0.9, -0.4, -0.2, 0.3]

XV, XH = perceptron(XOR, (1.0, -1.0), -0.3, 100)
assert min(h[1] for h in XH) >= 1 and len(XH) == 100
XW = [h[1] for h in XH[:5]]

# ---------- 2-2-1 sigmoid MLP on XOR ----------
def train_xor(seed=1, lr=2.0, epochs=3000):
    g = random.Random(seed)
    W1 = [[g.uniform(-1, 1) for _ in range(2)] for _ in range(2)]; b1 = [g.uniform(-1, 1) for _ in range(2)]
    W2 = [g.uniform(-1, 1) for _ in range(2)]; b2 = 0.0
    for _ in range(epochs):
        G = [[0, 0], [0, 0]]; gb = [0, 0]; g2 = [0, 0]; gb2 = 0
        for (a, c), t in zip(X4, XOR):
            h = [sig(W1[i][0] * a + W1[i][1] * c + b1[i]) for i in range(2)]
            e = sig(W2[0] * h[0] + W2[1] * h[1] + b2) - t; gb2 += e
            for i in range(2):
                g2[i] += e * h[i]; d = e * W2[i] * h[i] * (1 - h[i])
                G[i][0] += d * a; G[i][1] += d * c; gb[i] += d
        for i in range(2):
            W2[i] -= lr * g2[i] / 4; b1[i] -= lr * gb[i] / 4
            W1[i][0] -= lr * G[i][0] / 4; W1[i][1] -= lr * G[i][1] / 4
        b2 -= lr * gb2 / 4
    rd = lambda v: round(v, 1)
    return [[rd(v) for v in w] for w in W1], [rd(v) for v in b1], [rd(v) for v in W2], rd(b2)

W1, B1, W2, B2 = train_xor()
assert (W1, B1, W2, B2) == ([[-7.4, 7.2], [7.2, -7.4]], [-3.9, -3.9], [13.8, 13.8], -6.8)
def fwd(a, c):
    z = [W1[i][0] * a + W1[i][1] * c + B1[i] for i in range(2)]
    h = [sig(v) for v in z]
    zo = W2[0] * h[0] + W2[1] * h[1] + B2
    return z, h, zo, sig(zo)
HID = [fwd(a, c)[1] for a, c in X4]
OUT = [fwd(a, c)[3] for a, c in X4]
assert [round(o) for o in OUT] == XOR
assert [[round(v, 2) for v in h] for h in HID] == [[0.02, 0.02], [0.96, 0.0], [0.0, 0.96], [0.02, 0.02]]
FZ, FHh, FZO, FO = fwd(1, 0)
assert [round(v, 1) for v in FZ] == [-11.3, 3.3] and round(FZO, 1) == 6.5 and round(FO, 2) == 1.0

# parameter counts
def params(sizes): return [(a, b, a * b, b) for a, b in zip(sizes, sizes[1:])]
SMALL = params([2, 2, 1]); BIG = params([784, 128, 10])
assert sum(p[2] + p[3] for p in SMALL) == 9 and sum(p[2] + p[3] for p in BIG) == 101770

# ---------- drawing helpers ----------
TONE = {FI: 'bl', AM: 'am', GR: 'gr', RD: 'rd'}
def chip(cx, cy, s, c=FI, w=None):
    w = w or 16 + len(s) * 7.2
    return (R(cx - w / 2, cy - 11, w, 22, BG, 'none', 11) + R(cx - w / 2, cy - 11, w, 22, tint(TONE[c], '.14'), c, 11, 1.3) +
            T(cx, cy + 4.5, s, c, mono=True, bold=True))

def pt(x, y, t, r=7):
    if t: return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, FI)
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, r - 1, BG, BR)

def node(x, y, s='', r=16, c=TX, fill=BG, sw=1.5):
    o = '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, y, r, fill, c, sw)
    return o + (M(x, y + 5, s, c) if s else '')

def ring(x, y, r=21, c=AM): return ringc(x, y, r, c, 2.2)

def legend(x, y):
    return pt(x, y - 4, 1, 5) + S(x + 10, y, 'class 1', MU) + pt(x + 70, y - 4, 0, 5) + S(x + 80, y, 'class 0', MU)

def plane(f, px, py, size=200, xl='{x}₁', yl='{x}₂', lo=-.4, hi=1.4):
    pl = Plot(px, py, size, size, lo, hi, lo, hi)
    f.static(frame_box(pl) + M(pl.px + size / 2, pl.py + size + 22, xl, MU) + M(pl.px - 14, pl.py + size / 2 + 5, yl, MU, 'end'))
    for v in (0, 1):
        f.static(T(pl.X(v), pl.py + size + 13, str(v), FA, mono=True) + T(pl.px - 5, pl.Y(v) + 4, str(v), FA, 'end', mono=True))
    return pl

def seg(pl, w, b, c=AM, sw=2.2, dash=None):
    s = clipline(pl, w[0], w[1], b); assert s, (w, b)
    (a, bb), (c2, d) = s
    return L(a, bb, c2, d, c, sw, dash)

def badge(x, y, s, c=AM, w=None):
    w = w or len(s) * 6.6 + 20
    return R(x, y - 13, w, 22, BG, 'none', 4) + R(x, y - 13, w, 22, tint('am' if c == AM else 'gr', '.12'), c, 4, 1.2) + T(x + w / 2, y + 2, s, c, bold=True)

# ---------- 01 Mental model: one neuron ----------
def fig_neuron():
    f = Anim('mlp1-', 720, 0, 'One neuron with weights 0.7 and 0.5 and bias minus 0.9. Each row of the AND table in turn: its two inputs '
             'travel to the input circles, become weight times input on the two edges, meet in the sum box with the bias to give z, '
             'pass the step, and the output 0 or 1 flies back into the prediction column. z is minus 0.9, minus 0.4, minus 0.2 and 0.3, '
             'so only the row 1, 1 fires; all four predictions match the AND column.',
             'ONE ROW IN · WEIGHTED SUM + BIAS · STEP · ONE BIT OUT')
    t = Table(0, 40, [('x₁', 40), ('x₂', 40), ('AND', 46), ('ŷ', 44)])
    f.static(t.head())
    for i, (a, c) in enumerate(X4):
        f.static(t.row(i, [str(a), str(c), str(AND[i]), '']))
    I = [(300, 92), (300, 172)]; SX, SY, SW, SH = 470, 132, 104, 44
    stx, ox = 600, 680
    for k, (x, y) in enumerate(I):
        f.static(L(x + 16, y, SX - SW / 2, SY + (-10 if k == 0 else 10), RULE_HI, 2))
        f.static(R((x + SX - SW / 2) / 2 - 22 + 8, (y + SY) / 2 + (-24 if k == 0 else 12), 44, 18, BG, 'none', 4) +
                 M((x + SX - SW / 2) / 2 + 8, (y + SY) / 2 + (-11 if k == 0 else 25), '{w}%s = %s' % ('₁₂'[k], fm(WA[k])), BR))
        f.static(node(x, y, '{x}%s' % '₁₂'[k]))
    f.static(L(SX, 70, SX, SY - SH / 2, RULE_HI, 1.5) + node(SX, 58, '{b}', 14) + T(SX + 20, 62, '= ' + fm(BA), BR, 'start', mono=True))
    f.static(R(SX - SW / 2, SY - SH / 2, SW, SH, BG, TX, 8, 1.5) + M(SX, SY - 4, 'Σ + {b}', MU))
    f.static(arrow(SX + SW / 2, SY, stx - 20, SY, RULE_HI, 1.5) + R(stx - 20, SY - 18, 40, 36, BG, TX, 6, 1.5) +
             '<path d="M%.1f %.1f H%.1f V%.1f H%.1f" fill="none" stroke="%s" stroke-width="1.8"/>' % (stx - 13, SY + 9, stx, SY - 9, stx + 13, TX) +
             T(stx, SY + 34, 'step', FA) + arrow(stx + 20, SY, ox - 17, SY, RULE_HI, 1.5) + node(ox, SY, '{ŷ}'))
    t0 = .6
    for i, (a, c) in enumerate(X4):
        hide = t0 + 2.5 if i < 3 else None
        f.show(t.outline(i, c=AM), t0, hide=t0 + 2.5)
        for k, v in enumerate((a, c)):
            sx, sy = t.cx(k), t.ry(i) + 13; x, y = I[k]
            f.path(chip(x, y - 28, str(v), FI, 26), [(0, sx - x, sy - y + 28), (t0 + .2, 0, 0)], t0, d=.5, hide=t0 + 1.0)
            ex, ey = SX - SW / 2 - 24, SY + (-26 if k == 0 else 26)
            p = WA[k] * v
            f.path(chip(ex, ey, fm(p), AM, 44), [(0, x + 30 - ex, y - ey), (t0 + 1.0, 0, 0)], t0 + .8, d=.5, hide=t0 + 1.8)
        f.show(R(SX - SW / 2 + 3, SY + 1, SW - 6, 18, BG, 'none', 3) + M(SX, SY + 15, '{z} = ' + fm(ZA[i]), AM), t0 + 1.6, hide=hide)
        y_ = step(ZA[i]); ok = y_ == AND[i]
        f.path(chip(ox, SY - 30, str(y_), GR if ok else RD, 26), [(0, 0, 0), (t0 + 2.1, t.cx(3) - ox, t.ry(i) + 13 - SY + 30)], t0 + 1.9, d=.5)
        t0 += 2.8
    f.static(T(0, t.ry(4) + 30, '0.7·1 + 0.5·1 − 0.9 = 0.3 > 0 → fires', MU, 'start', mono=True))
    return finish(f, t.ry(4) + 44)

# ---------- 02 Perceptron learning rule on AND ----------
def fig_learn():
    f = Anim('mlp2-', 720, 0, 'The perceptron rule on the AND table, starting from w = 0.2, 1.0 and b = minus 0.4. Rows are visited in order; '
             'each prediction appears in the table, green when right, red when wrong. On a wrong row the change eta times y minus y-hat '
             'times x flies into the weight cells and the line on the plane swings to its new place. Three mistakes, then a full pass '
             'with no mistake: w = 0.7, 0.5, b = minus 0.9, and only the point 1, 1 lies on the firing side.',
             'PREDICT · WRONG → NUDGE THE WEIGHTS · THE LINE SWINGS')
    t = Table(0, 40, [('x₁', 40), ('x₂', 40), ('y', 40), ('ŷ', 44)])
    f.static(t.head())
    for i, (a, c) in enumerate(X4): f.static(t.row(i, [str(a), str(c), str(AND[i]), '']))
    wy = t.ry(4) + 40
    names = ['{w}₁', '{w}₂', '{b}']; cx = [20, 82, 144]
    for j in range(3):
        f.static(M(cx[j], wy - 8, names[j], MU) + R(cx[j] - 26, wy, 52, 26, BG, RULE_HI, 4))
    def wcell(j, v, c=TX): return R(cx[j] - 25, wy + 1, 50, 24, BG, 'none', 4) + T(cx[j], wy + 18, fm(v), c, mono=True, bold=c != TX)
    f.static(M(0, wy + 56, '{w} ← {w} + {η} ({y} − {ŷ}) {x}', MU, 'start') + T(0, wy + 76, 'η = 0.5 · bias uses x = 1', FA, 'start'))
    pl = plane(f, 430, 40, 220)
    for (a, c), y in zip(X4, AND): f.static(pt(*pl.P(a, c), y))
    f.static(legend(470, 312))
    tt = .6
    vals = [W0[0], W0[1], B0]
    wst = [[(wcell(j, vals[j]), 0)] for j in range(3)]
    lst = [(seg(pl, W0, B0), 0)]
    yst = {}
    for ep, i, yh, old, new in AV:
        a, c = X4[i]; ok = yh == AND[i]
        hold = .7 if ok else 2.0
        f.show(t.outline(i, c=AM), tt, hide=tt + hold)
        f.show(badge(220, 90, 'epoch %d · row %d' % (ep + 1, i + 1), AM, 120), tt, hide=tt + hold)
        yst.setdefault(i, []).append((t.cell(i, 3, str(yh), 'gr' if ok else 'rd'), tt + .15))
        if not ok:
            e = AND[i] - yh; d = [ETA * e * a, ETA * e * c, ETA * e]
            vals2 = [new[0][0], new[0][1], new[1]]
            for j in range(3):
                if d[j] == 0: continue
                sx, sy = t.x + t.w + 30, t.ry(i) + 13
                f.path(chip(cx[j], wy + 13, ('+' if d[j] > 0 else '−') + fm(abs(d[j])), AM, 46),
                       [(0, sx - cx[j], sy - wy - 13), (tt + .6, 0, 0)], tt + .4, d=.6, hide=tt + 1.3)
                wst[j].append((wcell(j, vals2[j], AM), tt + 1.3))
            (w0, b0), (w1, b1) = old, new
            n = 4
            for k in range(1, n):
                u = k / n
                wi = (w0[0] + (w1[0] - w0[0]) * u, w0[1] + (w1[1] - w0[1]) * u); bi = b0 + (b1 - b0) * u
                lst.append((seg(pl, wi, bi, AM, 1.6, '4 3'), tt + 1.3 + (k - 1) * .15))
            lst.append((seg(pl, w1, b1), tt + 1.3 + (n - 1) * .15))
            tt += 2.3
        else:
            tt += .9
    def seq(states):
        for k, (svg, ton) in enumerate(states):
            hide = states[k + 1][1] if k + 1 < len(states) else None
            if ton == 0 and hide is None: f.static(svg)
            elif ton == 0: f.show(svg, 0, hide=hide, d=.01)
            else: f.show(svg, ton, hide=hide, d=.1)
    seq(lst)
    for j in range(3):
        wst[j][-1] = (wcell(j, [WA[0], WA[1], BA][j], GR), wst[j][-1][1]); seq(wst[j])
    for i in yst: seq(yst[i])
    f.show(pill(250, 300, 'a full pass, no mistake', 'gr', 170), tt)
    return finish(f, max(wy + 86, 330))

# ---------- 03 XOR ----------
def fig_xor():
    f = Anim('mlp3-', 720, 0, 'The same rule on XOR: 0, 1 and 1, 0 are class 1, the corners 0, 0 and 1, 1 class 0. After each pass the line '
             'is drawn and the points on the wrong side are ringed in red; the log on the right fills one row per pass. Every pass '
             'leaves at least one point wrong, and after 100 passes the rule has still not stopped.',
             'XOR · EVERY LINE LEAVES A POINT ON THE WRONG SIDE')
    pl = plane(f, 40, 40, 220)
    for (a, c), y in zip(X4, XOR): f.static(pt(*pl.P(a, c), y))
    f.static(legend(80, 312))
    lx = 380
    f.static(T(lx, 46, 'pass', MU, 'start') + T(lx + 70, 46, 'w₁', MU, 'start') + T(lx + 125, 46, 'w₂', MU, 'start') +
             T(lx + 180, 46, 'b', MU, 'start') + T(lx + 230, 46, 'wrong', MU, 'start') + L(lx, 54, lx + 300, 54))
    tt = .6
    for k in range(5):
        (w, b), wrong = XH[k]; last = k == 4
        g = seg(pl, w, b) + ''.join(ringc(*pl.P(a, c), 13, RD, 2) for (a, c), y in zip(X4, XOR) if step(w[0] * a + w[1] * c + b) != y)
        f.show(g, tt, hide=None if last else tt + 1.2)
        y = 78 + k * 28
        f.show(T(lx + 10, y, str(k + 1), TX, 'start', mono=True) + T(lx + 70, y, fm(w[0]), TX, 'start', mono=True) +
               T(lx + 125, y, fm(w[1]), TX, 'start', mono=True) + T(lx + 180, y, fm(b), TX, 'start', mono=True) +
               T(lx + 245, y, str(wrong), RD, 'start', mono=True, bold=True), tt + .2)
        tt += 1.4
    f.show(T(lx + 10, 78 + 5 * 28, '…', FA, 'start', mono=True) + T(lx + 10, 78 + 6 * 28, '100', TX, 'start', mono=True) +
           T(lx + 70, 78 + 6 * 28, 'never 0 wrong', RD, 'start'), tt)
    f.show(pill(530, 300, 'no single line fits XOR', 'rd', 180), tt + .5)
    return finish(f, 330)

# ---------- 04 hidden layer ----------
def net(x0, y0, labels, gap=120, vgap=80, wl=True, hl=(None, None)):
    pos = [[(x0, y0), (x0, y0 + vgap)], [(x0 + gap, y0), (x0 + gap, y0 + vgap)], [(x0 + 2 * gap, y0 + vgap / 2)]]
    s = ''
    for i in range(2):
        for j in range(2):
            w = W1[i][j]
            s += L(pos[0][j][0] + 16, pos[0][j][1], pos[1][i][0] - 16, pos[1][i][1], FI if w > 0 else RD, '%.1f' % (.8 + abs(w) * .2), None if w > 0 else '5 3')
    for i in range(2):
        s += L(pos[1][i][0] + 16, pos[1][i][1], pos[2][0][0] - 16, pos[2][0][1], FI, '%.1f' % (.8 + abs(W2[i]) * .12))
    for l, ps in enumerate(pos):
        for i, (x, y) in enumerate(ps): s += node(x, y, labels[l][i])
    return s, pos

def fig_hidden_lines():
    f = Anim('mlp4-', 720, 0, 'A 2-2-1 network trained on XOR. Hidden neuron h1 is ringed: its line is drawn on the input plane, and the point '
             '0, 1 on its firing side gets h1 = 0.96 while the others get 0.02 or 0.00. Then h2: its line is the mirror image, and only '
             '1, 0 gets h2 = 0.96. Two lines, one band between them holding the two class-1 points.',
             'EACH HIDDEN NEURON DRAWS ITS OWN LINE')
    pl = plane(f, 40, 40, 220)
    for (a, c), y in zip(X4, XOR): f.static(pt(*pl.P(a, c), y))
    f.static(legend(80, 312))
    s, pos = net(430, 90, [['{x}₁', '{x}₂'], ['{h}₁', '{h}₂'], ['{ŷ}']])
    f.static(s + T(550, 300, 'solid = positive weight · dashed = negative', FA))
    tt = .6
    for i in range(2):
        hx, hy = pos[1][i]
        f.show(ring(hx, hy), tt, hide=tt + 2.4)
        f.show(seg(pl, W1[i], B1[i], AM if i == 0 else GR, 2.2, None if i == 0 else '6 4') +
               M(pl.X(.55 if i == 0 else 1.25), pl.Y(1.25 if i == 0 else .55), '{h}%s' % '₁₂'[i], AM if i == 0 else GR), tt + .4)
        f.show(T(hx + 26, hy + (-22 if i == 0 else 34), '%s · %s' % (fm(W1[i][0]), fm(W1[i][1])) + ' · b ' + fm(B1[i]), MU, 'start', mono=True), tt + .2)
        for k, (a, c) in enumerate(X4):
            v = HID[k][i]; x, y = pl.P(a, c)
            dx = -36 if a == 0 else 36; dy = (-15 if i == 0 else 17)
            f.show(R(x + dx - 18, y + dy - 11, 36, 16, BG, 'none', 3) + T(x + dx, y + dy + 1, fm(v, 2), AM if i == 0 else GR, mono=True, bold=v > .5), tt + .9 + k * .2)
        tt += 2.6
    return finish(f, 330)

def fig_hidden_space():
    f = Anim('mlp5-', 720, 0, 'Left: the four XOR points on the input plane. Right: the hidden plane with axes h1 and h2. Each point glides '
             'to its hidden coordinates: 0, 1 goes to 0.96, 0.00; 1, 0 to 0.00, 0.96; both 0, 0 and 1, 1 land on 0.02, 0.02. The output '
             'neuron then draws one straight line, h1 + h2 = 0.49, on the hidden plane: class 1 above it, class 0 below. All four are right.',
             'INPUT SPACE → HIDDEN SPACE · THERE ONE LINE IS ENOUGH')
    pi = plane(f, 40, 50, 220)
    ph = plane(f, 440, 50, 220, '{h}₁', '{h}₂', -.2, 1.2)
    f.static(M(150, 42, 'input space', MU) + M(550, 42, 'hidden space', MU))
    for (a, c), y in zip(X4, XOR): f.static(R(0, 0, 0, 0, 'none', 'none') + '<circle cx="%.1f" cy="%.1f" r="6" fill="none" stroke="%s" stroke-dasharray="2 2"/>' % (*pi.P(a, c), RULE_HI))
    off = {0: (-8, 0), 3: (8, 0)}  # (0,0) and (1,1) land on the same spot: drawn side by side
    for k, ((a, c), y) in enumerate(zip(X4, XOR)):
        hx, hy = ph.P(*HID[k]); o = off.get(k, (0, 0)); hx += o[0]; hy += o[1]
        sx, sy = pi.P(a, c)
        f.path(pt(hx, hy, y), [(0, sx - hx, sy - hy), (.8 + k * .5, 0, 0)], 0, appear=False, d=1.0)
        lab = '(%d,%d)' % (a, c)
        if k in (1, 2):
            f.show(T(hx + (-10 if k == 1 else 12), hy + (-12 if k == 1 else 4), lab, FA, 'end' if k == 1 else 'start', mono=True), 1.9 + k * .5)
    f.show(T(ph.X(.02), ph.Y(.02) + 24, '(0,0) (1,1)', FA, mono=True), 3.4)
    thr = -B2 / W2[0]; assert round(thr, 2) == .49
    f.show(seg(ph, W2, B2, AM, 2.4) + M(ph.X(.0) + 6, ph.Y(.62), '{h}₁ + {h}₂ = %s' % fm(thr, 2), AM, 'start'), 3.9)
    f.show(arrow(270, 160, 395, 160, RULE_HI, 1.4) + T(332, 150, 'hidden layer', MU), .2)
    f.show(pill(550, 304, '4 of 4 right', 'gr', 120), 4.8)
    return finish(f, 344)

# ---------- 05 forward pass ----------
def fig_forward():
    f = Anim('mlp6-', 720, 0, 'A forward pass through the trained 2-2-1 network for the input 1, 0. The inputs 1 and 0 travel along the four '
             'first-layer edges, each multiplied by its weight; each hidden neuron adds its bias, giving z1 = minus 11.3 and z2 = 3.3, '
             'and the sigmoid turns them into h1 = 0.00 and h2 = 0.96. Those travel on to the output: z = 6.5, sigmoid 1.00, '
             'so the prediction is 1, which is XOR of 1 and 0.',
             'FORWARD PASS · NUMBERS FLOW LEFT TO RIGHT')
    x0, y0, gap, vg = 60, 104, 250, 150
    P = [[(x0, y0), (x0, y0 + vg)], [(x0 + gap, y0), (x0 + gap, y0 + vg)], [(x0 + 2 * gap, y0 + vg / 2)]]
    edges = [(0, j, 1, i, W1[i][j]) for i in range(2) for j in range(2)] + [(1, i, 2, 0, W2[i]) for i in range(2)]
    for l1, j, l2, i, w in edges:
        (a, b), (c, d) = P[l1][j], P[l2][i]
        f.static(L(a + 18, b, c - 18, d, RULE_HI, 1.6))
        # weight label near the destination end, on the line
        u = .78; lx, ly = a + (c - a) * u, b + (d - b) * u
        f.static(R(lx - 20, ly - 9, 40, 18, BG, 'none', 4) + T(lx, ly + 4, fm(w), FI if w > 0 else RD, mono=True))
    labs = [['{x}₁', '{x}₂'], ['{h}₁', '{h}₂'], ['{ŷ}']]
    for l, ps in enumerate(P):
        for i, (x, y) in enumerate(ps): f.static(node(x, y, labs[l][i], 18))
    for i in range(2):
        f.static(T(P[1][i][0], P[1][i][1] + (-28 if i == 0 else 38), 'b = ' + fm(B1[i]), FA, mono=True))
    f.static(T(P[2][0][0], P[2][0][1] - 28, 'b = ' + fm(B2), FA, mono=True))
    XIN = (1, 0); tt = .5
    for j in range(2):
        x, y = P[0][j]
        f.show(chip(x - 44, y, str(XIN[j]), FI, 26), tt)
    tt += .6
    # layer 1: products travel along edges, stop before the hidden node
    for i in range(2):
        for j in range(2):
            (a, b), (c, d) = P[0][j], P[1][i]
            u = .45; ex, ey = a + (c - a) * u, b + (d - b) * u
            v = W1[i][j] * XIN[j]
            f.path(chip(ex, ey, fm(v), AM, 44), [(0, a + 30 - ex, b - ey), (tt + .2, 0, 0)], tt, d=.7, hide=tt + 2.0)
    tt += 1.3
    for i in range(2):
        x, y = P[1][i]
        yy = y + (-56 if i == 0 else 66)
        f.show(R(x - 72, yy - 13, 144, 22, BG, 'none', 4) + M(x, yy + 3, '{z} = %s → {σ} = %s' % (fm(FZ[i]), fm(FHh[i], 2)), AM), tt + i * .3)
    tt += 1.2
    for i in range(2):
        (a, b), (c, d) = P[1][i], P[2][0]
        u = .45; ex, ey = a + (c - a) * u, b + (d - b) * u
        f.path(chip(ex, ey, fm(W2[i] * FHh[i]), AM, 44), [(0, a + 30 - ex, b - ey), (tt + .2, 0, 0)], tt, d=.7, hide=tt + 2.0)
    tt += 1.3
    x, y = P[2][0]
    f.show(R(x - 72, y + 34, 144, 22, BG, 'none', 4) + M(x, y + 50, '{z} = %s → {σ} = %s' % (fm(FZO), fm(FO, 2)), AM), tt)
    f.show(pill(x, y + 70, 'ŷ = 1 = XOR(1, 0)', 'gr', 140), tt + .6)
    return finish(f, 344)

# ---------- 06 layers and parameters ----------
def fig_params():
    f = Anim('mlp7-', 720, 0, 'Counting parameters. In the 2-2-1 network the first layer of edges is outlined: 2 inputs times 2 neurons is '
             '4 weights, plus 2 biases, and that row flies into the table. The second layer: 2 weights plus 1 bias. Total 9. '
             'Below, the same count for a 784-128-10 digit classifier: 100,352 + 128, then 1,280 + 10, total 101,770.',
             'PARAMETERS = WEIGHTS (n_in × n_out) + BIASES (n_out), PER LAYER')
    s, pos = net(40, 70, [['', ''], ['', ''], ['']], 110, 80)
    f.static(s + T(40, 205, '2', MU) + T(150, 205, '2', MU) + T(260, 205, '1', MU) + T(150, 225, 'neurons per layer', FA))
    t = Table(340, 34, [('layer', 90), ('weights', 90), ('biases', 70), ('params', 80)])
    f.static(t.head())
    rows = [('2 → 2', SMALL[0]), ('2 → 1', SMALL[1]), None, ('784 → 128', BIG[0]), ('128 → 10', BIG[1]), None]
    tt = .6
    boxes = [(40 + 12, 46, 110 - 24, 128), (150 + 12, 46, 110 - 24, 128)]
    tot = 0
    for k, r in enumerate(rows):
        if r is None:
            total = 9 if k == 2 else 101770
            f.show(t.row(k, ['total', '', '', '{:,}'.format(total)], 'gr'), tt); tt += .8; continue
        name, (a, b, nw, nb) = r
        vals = [name, '%d × %d = {:,}'.format(nw) % (a, b) if nw < 1000 else '{:,}'.format(nw), str(nb), '{:,}'.format(nw + nb)]
        if k < 2:
            bx, by, bw, bh = boxes[k]
            f.show(R(bx, by, bw, bh, 'none', AM, 8, 1.8, '5 3'), tt, hide=tt + 1.4)
            f.path(t.row(k, vals), [(0, bx + bw / 2 - 340 - t.w / 2, by + bh / 2 - t.ry(k) - 13), (tt + .5, 0, 0)], tt + .2, d=.7)
        else:
            f.show(t.row(k, vals), tt + .2)
        tt += 1.6
    assert all(p[2] == p[0] * p[1] for p in SMALL + BIG)
    return finish(f, t.ry(6) + 10)

BODY = r'''<header class="hero">
  <p class="eyebrow">Deep learning · Neural network</p>
  <h1>Perceptron &amp; <em>MLP</em></h1>
  <p class="lede">One neuron is a weighted sum, a bias and a threshold — a single straight line; XOR shows why you need <b>a hidden layer</b> of them.</p>
</header>

<section id="mlp-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">A neuron multiplies each input by a weight, adds a bias, and <em>fires if the sum is above zero</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>ŷ</var></span><em>0 or 1</em></span>
      <span class="op">=</span>
      <span class="t p"><span><b class="fn">step</b></span><em>1 if z &gt; 0</em></span>
      <span class="t b"><span>(<var>w</var><sub>1</sub><var>x</var><sub>1</sub> + <var>w</var><sub>2</sub><var>x</var><sub>2</sub> + <var>b</var>)</span><em>z: weighted sum + bias</em></span>
    </div>
  </div>
{f1}
  <ul class="why">
    <li>This is Rosenblatt's <b>perceptron</b> (1958); the step is the first <a href="../activation-functions/index.html">activation function</a>.</li>
    <li><span class="mth"><var>z</var> = 0</span> is a straight line on the input plane: one side fires, the other does not.</li>
  </ul>
</section>

<section id="mlp-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Perceptron learning rule</h2></div>
  <p class="key">On every wrong row, <em>move each weight by η · error · input</em>; stop after a pass with no mistake.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>w</var></span></span>
      <span class="op">←</span>
      <span class="t"><span><var>w</var></span><em>old weight</em></span>
      <span class="op">+</span>
      <span class="t p"><span><var>η</var></span><em>learning rate</em></span>
      <span class="t r"><span>(<var>y</var> − <var>ŷ</var>)</span><em>error: +1, 0 or −1</em></span>
      <span class="t b"><span><var>x</var></span><em>input on that edge</em></span>
    </div>
  </div>
{f2}
  <ul class="why">
    <li>Right rows change nothing; a wrong row pushes the line toward its own side.</li>
    <li>If some line separates the classes, the rule is guaranteed to find one in a finite number of mistakes.</li>
  </ul>
</section>

<section id="mlp-s3" class="lesson">
  <div class="sh"><b>03</b><h2>The XOR problem</h2></div>
  <p class="key">XOR puts each class on opposite corners: <em>no straight line separates them</em>, so the rule never stops.</p>
{f3}
  <ul class="why">
    <li>Minsky and Papert (1969) made this limit famous; funding for neural networks dried up — the first AI winter.</li>
    <li>The fix is not a better rule but more neurons: lines combined in a second layer.</li>
  </ul>
</section>

<section id="mlp-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Hidden layer</h2></div>
  <p class="key">A <b>multilayer perceptron</b> (MLP) feeds the outputs of several neurons into the next neuron.</p>
  <div class="subsec" id="mlp-s4-1">
    <h3 class="ssh"><b>4.1</b>Hidden neurons</h3>
    <p class="skey">Each hidden neuron is one perceptron: <em>it draws its own line</em> and outputs how far a point is on its firing side.</p>
{f4}
    <ul class="why">
      <li>The step is replaced by a smooth sigmoid <span class="mth"><var>σ</var></span>, so outputs are between 0 and 1 and the weights can be trained by <a href="../backpropagation/index.html">backpropagation</a>.</li>
      <li>These weights came from 3,000 gradient-descent steps on the four rows, seed 1 — nobody picked them by hand.</li>
    </ul>
  </div>
  <div class="subsec" id="mlp-s4-2">
    <h3 class="ssh"><b>4.2</b>Hidden space</h3>
    <p class="skey">The hidden outputs are new coordinates; there <em>XOR becomes separable</em> and the output neuron cuts it with one line.</p>
{f5}
    <ul class="why">
      <li>Folded back onto the input plane, that one line becomes the band between the two hidden lines.</li>
      <li>This is what "learning features" means: the hidden layer moves the data until the last layer's job is easy.</li>
    </ul>
  </div>
</section>

<section id="mlp-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Forward pass</h2></div>
  <p class="key">A prediction is <em>one sweep left to right</em>: every layer is a matrix product, a bias, then <span class="mth"><var>σ</var></span>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b>h</b></span><em>hidden outputs</em></span>
      <span class="op">=</span>
      <span class="t p"><span><var>σ</var></span><em>applied to each entry</em></span>
      <span class="t b"><span>(<var>W</var><sub>1</sub><b>x</b> + <b>b</b><sub>1</sub>)</span><em>W<sub>1</sub>: one row of weights per hidden neuron</em></span>
      <span class="op">,</span>
      <span class="t g"><span><var>ŷ</var> = <var>σ</var>(<b>w</b><sub>2</sub> · <b>h</b> + <var>b</var><sub>2</sub>)</span><em>the output neuron</em></span>
    </div>
  </div>
{f6}
  <ul class="why">
    <li>A batch of inputs is a matrix <span class="mth"><var>X</var></span>: the same pass becomes <span class="mth"><var>σ</var>(<var>X</var><var>W</var><sup>T</sup> + <b>b</b>)</span>, one GPU call per layer.</li>
    <li>Without <span class="mth"><var>σ</var></span> two layers collapse into one matrix — still one straight line.</li>
  </ul>
</section>

<section id="mlp-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Layers and parameters</h2></div>
  <p class="key">Each layer owns a weight matrix and a bias vector: <em>inputs × outputs + outputs</em> numbers to learn.</p>
{f7}
  <ul class="why">
    <li><b>Depth</b> = number of weight layers; <b>width</b> = neurons per layer. Most parameters sit next to the widest layers.</li>
    <li><b>Universal approximation</b>: one hidden layer, wide enough, can approximate any continuous function — but it says nothing about how wide, or whether training finds it.</li>
  </ul>
</section>

{script}

<footer>Deep learning · Neural network · next lesson in the group: <a href="../activation-functions/index.html">Activation functions</a>.</footer>
'''

def build():
    import decision_tree as dt
    src = open(dt.PAGE).read()
    script = re.search(r'<script>\n/\* Figures start.*?</script>', src, re.S).group(0)
    figs = dict(f1=fig_neuron(), f2=fig_learn(), f3=fig_xor(), f4=fig_hidden_lines(), f5=fig_hidden_space(),
                f6=fig_forward(), f7=fig_params(), script=script)
    return re.sub(r'\{(f\d|script)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">'); b = s.index('</article>')
    s = s[:a] + body + '\n      ' + s[b:]
    s = re.sub(r'<article class="doc"[^>]*>', lambda m: re.sub(r' data-(skeleton|reviewed|progress)="\d"', '', m.group(0)), s, count=1)
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s" data-progress="1"' % blurb, s, count=1)
    open(page, 'w').write(s)

if __name__ == '__main__':
    print('AND w', WA, BA, 'XOR wrong', XW, 'MLP', W1, B1, W2, B2)
    splice(PAGE, build(), 'One neuron is a weighted sum, a bias and a step — one straight line; the perceptron rule learns AND, '
           'fails on XOR, and a 2-2-1 MLP solves it by moving the points into a hidden space.')
