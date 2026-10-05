# -*- coding: utf-8 -*-
"""Figures for content/07-machine-learning/04-core-concepts/supervised-unsupervised.
Run: python3 supervised_unsupervised.py -> splices into <!--FIGn--> markers."""
import random
from cc_kit import *  # noqa

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/04-core-concepts/supervised-unsupervised/index.html')

rng = random.Random(7)
A = [(2.2 + rng.gauss(0, .75), 2.6 + rng.gauss(0, .7)) for _ in range(9)]
B = [(5.9 + rng.gauss(0, .75), 5.6 + rng.gauss(0, .7)) for _ in range(9)]
PTS = [(x, y, 0) for x, y in A] + [(x, y, 1) for x, y in B]
TONE = {0: 'bl', 1: 'gr'}

def plot(x0=40, y0=36, w=300, h=220):
    return Plot(x0, y0, w, h, (0, 8.5), (0, 8.5))

def mark(P, x, y, c, r=6):
    tone = TONE[c] if c is not None else None
    if c == 1:  # class 1 = square, so shape also tells the classes apart
        X, Y = P.p(x, y)
        return R(X - r, Y - r, 2 * r, 2 * r, tint('gr', '.55'), GR, 2, 1.6)
    return dot(*P.p(x, y), tone, r)

# ---------- 1.1 Supervised ----------
def f_sup():
    f = Fig('su1-', 680, 300, 'Eighteen points appear grey, then each one receives its label: nine circles, nine squares. '
            'A straight boundary is learned between them. A new point with no label appears, is ringed, and is '
            'predicted as a square because it falls on the square side.', 'EVERY SAMPLE COMES WITH ITS ANSWER')
    P = plot()
    f(P.axes('feature 1', 'feature 2'))
    for i, (x, y, c) in enumerate(PTS):
        f(dot(*P.p(x, y)), show=.2 + i * .04, hide=1.4 + i * .06, d=.2)
        f(mark(P, x, y, c), show=1.4 + i * .06, d=.25)
    f(T(380, 70, 'labels', MU, 'start'), show=1.3)
    f(T(380, 92, '● class 0', BL, 'start') + T(470, 92, '■ class 1', GR, 'start'), show=1.6)
    # boundary x + y = 8.4
    a, b = P.p(0.9, 7.5), P.p(7.5, 0.9)
    f(L(a[0], a[1], b[0], b[1], AM, 2, '6 4'), show=3.0, d=.6)
    f(T(380, 128, 'learn a boundary', AM, 'start', 'sv-s'), show=3.0, hide=4.4)
    nx, ny = 5.4, 4.6
    f(dot(*P.p(nx, ny)) + T(P.px(nx) + 12, P.py(ny) - 8, '?', TX, 'start', bold=True), show=4.2, hide=5.6)
    f(ring(*P.p(nx, ny), 13), show=4.4)
    f(T(380, 128, 'new sample · no label', AM, 'start', 'sv-s'), show=4.4, hide=5.6)
    X, Y = P.p(nx, ny)
    f(R(X - 6, Y - 6, 12, 12, tint('gr', '.55'), GR, 2, 1.6), show=5.6)
    f(T(380, 128, 'predicted: class 1', GR, 'start', 'sv-s'), show=5.6)
    f(T(380, 160, 'loss = how far each prediction', MU, 'start') + T(380, 176, 'is from its given answer', MU, 'start'), show=6.2)
    return f.render()

# ---------- 1.2 Unsupervised ----------
def f_unsup():
    f = Fig('su2-', 680, 300, 'The same eighteen points, but grey with no labels. Two group centres start at random spots, '
            'slide toward the dense areas in two steps, and each point takes the colour of its nearest centre. '
            'Two groups are found, but nothing says what they mean.', 'NO ANSWERS · ONLY STRUCTURE')
    P = plot()
    f(P.axes('feature 1', 'feature 2'))
    for i, (x, y, c) in enumerate(PTS):
        f(dot(*P.p(x, y)), show=.2 + i * .04, hide=3.8, d=.2)
    # two k-means steps
    cen = [(1.5, 6.8), (6.8, 1.8)]
    hist = [cen]
    for _ in range(3):
        grp = [[], []]
        for x, y, _c in PTS:
            k = min((0, 1), key=lambda j: (x - cen[j][0]) ** 2 + (y - cen[j][1]) ** 2)
            grp[k].append((x, y))
        cen = [(sum(p[0] for p in g) / len(g), sum(p[1] for p in g) / len(g)) for g in grp]
        hist.append(cen)
    lab = [min((0, 1), key=lambda j: (x - cen[j][0]) ** 2 + (y - cen[j][1]) ** 2) for x, y, _ in PTS]
    assert len(set(zip(lab, [c for *_, c in PTS]))) == 2  # clusters recover the hidden groups
    for j in range(2):
        for k, h in enumerate(hist):
            hx, hy = P.p(*h[j])
            last = k == len(hist) - 1
            s = (L(hx - 7, hy - 7, hx + 7, hy + 7, AM, 2.4) + L(hx - 7, hy + 7, hx + 7, hy - 7, AM, 2.4))
            if k == 0:
                f(s, show=1.2, hide=2.0, d=.05)
            else:
                px, py = P.p(*hist[k - 1][j])
                f(s, show=1.2 + k * .8, hide=None if last else 1.2 + (k + 1) * .8, d=.05,
                  move=(1.2 + k * .8, px - hx, py - hy, .6))
    for i, (x, y, c) in enumerate(PTS):
        f(mark(P, x, y, lab[i]), show=3.8, d=.4)
    f(T(380, 70, 'move centres to the middle', AM, 'start', 'sv-s') + T(380, 88, 'of their nearest points', AM, 'start', 'sv-s'),
      show=1.2, hide=3.8)
    f(T(380, 70, '2 groups found', GR, 'start', 'sv-s'), show=4.2)
    f(T(380, 92, 'but no names on them —', MU, 'start') + T(380, 108, 'a human decides what they mean', MU, 'start'), show=4.6)
    f(T(380, 150, 'nothing to score against:', MU, 'start') + T(380, 166, 'no right answer per sample', MU, 'start'), show=5.2)
    return f.render()

# ---------- 1.3 Reinforcement ----------
def f_rl():
    f = Fig('su3-', 680, 214, 'An agent walks across a row of seven cells, one action at a time. Every step returns reward 0. '
            'Only on reaching the last cell does it receive reward +1. Then the reward flows back and tints every '
            'step on the path, because the agent must work out which earlier actions earned it.',
            'THE SIGNAL ARRIVES LATE, AFTER MANY ACTIONS')
    n, cw, x0, y0 = 7, 70, 40, 60
    for i in range(n):
        f(R(x0 + i * (cw + 8), y0, cw, 44, 'var(--bg)', RULE_HI, 6))
    gx = x0 + (n - 1) * (cw + 8)
    f(T(gx + cw / 2, y0 - 10, 'goal', MU) + T(x0 + cw / 2, y0 - 10, 'start', MU))
    _ag = lambda i: '<circle cx="%.1f" cy="%.1f" r="11" fill="%s" stroke="%s" stroke-width="1.8"/>' % (x0 + cw / 2, y0 + 22, tint('am', '.30'), AM)
    for i in range(n):
        t = .5 + i * .7
        last = i == n - 1
        cx = x0 + i * (cw + 8) + cw / 2
        f('<circle cx="%.1f" cy="%.1f" r="11" fill="%s" stroke="%s" stroke-width="1.8"/>' % (cx, y0 + 22, tint('am', '.30'), AM),
          show=t, hide=None if last else t + .7, d=.2)
        rw = '+1' if last else '0'
        f(T(cx, y0 + 66, 'reward ' + rw, GR if last else FA, 'middle', 'sv-s' if last else 'sv-d'), show=t + .25, d=.2)
    te = .5 + n * .7 + .3
    for i in range(n - 1, -1, -1):
        x = x0 + i * (cw + 8)
        a = .08 + .5 * (0.8 ** (n - 1 - i))
        f(R(x + 3, y0 + 3, cw - 6, 38, tint('gr', '%.2f' % a), 'none', 4), show=te + (n - 1 - i) * .25, d=.3)
    f(arrow(gx - 6, y0 + 92, x0 + 20, y0 + 92, GR, 1.4), show=te, d=.6)
    f(T(x0, y0 + 112, 'credit flows back: which earlier actions earned the reward?', GR, 'start', 'sv-s'), show=te + .4)
    f(T(x0, y0 + 136, 'no answer per action · one delayed score per episode', MU, 'start'), show=te + 1.6)
    return f.render()

# ---------- 2.1 Logged labels ----------
def f_logged():
    f = Fig('su4-', 680, 260, 'An orders table has a returned column full of question marks. Over the next days return '
            'events arrive from the shop system and fill the column: yes for two orders, no for the others once 30 days '
            'pass. Labels came for free, but only after waiting.', 'THE BUSINESS PROCESS WRITES THE LABEL')
    t = Table(0, 30, [('order', 70), ('item', 90), ('price', 70), ('returned?', 100, 'label')])
    f(t.head())
    rows = [('1', 'shoes', '80'), ('2', 'lamp', '35'), ('3', 'coat', '120'), ('4', 'mug', '9'), ('5', 'bag', '60')]
    ret = {0: 'yes', 2: 'yes'}
    for i, r in enumerate(rows):
        f(t.row(i, list(r) + ['?']), show=.2 + i * .12)
    f(t.colbox(3, 5, AM), show=1.0, hide=5.4)
    tm = 1.4
    for i in sorted(ret):
        y = t.ry(i) + 3
        f(pill(560, y, 'return event #%s' % rows[i][0], 'am', 130), show=tm, hide=tm + 1.0, move=(tm, 0, 0, .1), d=.2)
        f(arrow(492, y + 10, t.x + t.w + 4, y + 10, AM, 1.3), show=tm + .2, hide=tm + 1.0, d=.2)
        f(t.cell(i, 3, 'yes', 'gr'), show=tm + .7, d=.25)
        tm += 1.2
    f(T(430, 230, 'day 30 · no event = no', MU, 'start'), show=tm)
    for i in range(5):
        if i not in ret:
            f(t.cell(i, 3, 'no', 'bl'), show=tm + .3 + i * .1, d=.25)
    f(T(0, 230, 'free labels · but you wait 30 days for each', GR, 'start', 'sv-s'), show=tm + 1.0)
    return f.render()

# ---------- 2.2 Hand labels ----------
def f_hand():
    f = Fig('su5-', 680, 240, 'Six photos are labelled by two people. Labeller A writes cat, dog, cat, cat, dog, cat. '
            'Labeller B agrees on five and disagrees on the fourth photo. Agreement is 5 of 6, about 83 percent, which '
            'caps how well any model trained on these labels can score.', 'TWO PEOPLE · SAME SIX PHOTOS')
    a = ['cat', 'dog', 'cat', 'cat', 'dog', 'cat']
    b = ['cat', 'dog', 'cat', 'dog', 'dog', 'cat']
    agree = sum(x == y for x, y in zip(a, b))
    assert agree == 5
    x0, cw = 120, 80
    f(T(0, 66, 'photo', MU, 'start') + T(0, 112, 'labeller A', MU, 'start') + T(0, 152, 'labeller B', MU, 'start'))
    for i in range(6):
        x = x0 + i * (cw + 10)
        f(R(x, 40, cw, 40, SUNK, RULE_HI, 4) + T(x + cw / 2, 65, 'photo %d' % (i + 1), FA), show=.2 + i * .1)
        f(R(x, 92, cw, 30, 'var(--bg)', RULE_HI, 4) + T(x + cw / 2, 112, a[i], TX), show=.9 + i * .3)
        same = a[i] == b[i]
        f(R(x, 132, cw, 30, 'var(--bg)' if same else tint('rd', '.16'), RULE_HI if same else RD, 4, 1 if same else 1.6) +
          T(x + cw / 2, 152, b[i], TX if same else RD), show=3.0 + i * .3)
    xx = x0 + 3 * (cw + 10)
    f(R(xx - 4, 36, cw + 8, 130, 'none', AM, 6, 1.6, '4 3'), show=5.0)
    f(T(xx + cw / 2, 184, 'disagree', RD, 'middle', 'sv-s'), show=5.0)
    f(T(0, 214, 'agreement 5 / 6 ≈ 83%  →  no model can be checked above that', GR, 'start', 'sv-s'), show=5.8)
    return f.render()

# ---------- 2.3 Behaviour labels ----------
def f_behav():
    f = Fig('su6-', 680, 250, 'Five users watched the same video. Bars grow to show the share each one watched: 95, 30, 85, '
            '10 and 60 percent. A rule line at 80 percent turns behaviour into a label: two users count as liked, three as '
            'not liked. The label is cheap but approximate.', 'WATCH TIME BECOMES A LABEL')
    w = [95, 30, 85, 10, 60]
    x0, bw, y0 = 90, 420, 44
    sc = bw / 100
    for i, v in enumerate(w):
        y = y0 + i * 34
        f(T(0, y + 16, 'user %d' % (i + 1), MU, 'start'))
        f(R(x0, y, bw, 22, SUNK, 'none', 3))
        f(R(x0, y, v * sc, 22, tint('bl', '.45'), BL, 3, 1), show=.3 + i * .2, move=(.3 + i * .2, -v * sc / 2, 0, .6))
        f(T(x0 + v * sc + 6, y + 16, '%d%%' % v, TX, 'start'), show=.9 + i * .2)
    tx = x0 + 80 * sc
    f(L(tx, y0 - 10, tx, y0 + 5 * 34, AM, 1.6, '5 4') + T(tx, y0 - 14, 'rule: ≥ 80% = liked', AM), show=2.4)
    for i, v in enumerate(w):
        y = y0 + i * 34
        lk = v >= 80
        f(pill(600, y + 1, 'liked' if lk else 'not liked', 'gr' if lk else None, 86), show=3.0 + i * .25)
    f(T(0, 230, 'cheap and plentiful · but someone may watch to the end and still dislike it', MU, 'start'), show=4.6)
    return f.render()

# ---------- 3.1 Regression ----------
XS = [1.0, 1.8, 2.5, 3.1, 3.9, 4.6, 5.4, 6.2, 7.0]
YS = [2.1, 2.4, 3.6, 3.3, 4.6, 4.9, 5.2, 6.4, 6.5]
def fit():
    n = len(XS); mx = sum(XS) / n; my = sum(YS) / n
    w = sum((x - mx) * (y - my) for x, y in zip(XS, YS)) / sum((x - mx) ** 2 for x in XS)
    return w, my - w * mx
def f_reg():
    w, b = fit()
    mse = sum((w * x + b - y) ** 2 for x, y in zip(XS, YS)) / len(XS)
    f = Fig('su7-', 680, 300, 'Nine houses plotted by size and price. A straight line is fitted. For each house a vertical '
            'stick shows the gap between the true price and the line. The gaps are squared and averaged: MSE %.2f. '
            'The output is a number on a continuous scale.' % mse, 'OUTPUT IS A NUMBER')
    P = Plot(50, 36, 320, 220, (0, 8), (0, 8))
    f(P.axes('size', 'price'))
    for i, (x, y) in enumerate(zip(XS, YS)):
        f(dot(*P.p(x, y), 'bl'), show=.2 + i * .08)
    f(P.curve(lambda x: w * x + b, .4, 7.6, 2, GR, 2.4), show=1.2, d=.6)
    for i, (x, y) in enumerate(zip(XS, YS)):
        yh = w * x + b
        f(L(P.px(x), P.py(y), P.px(x), P.py(yh), AM, 1.6), show=2.2 + i * .25, d=.2)
    f(T(410, 70, 'ŷ = line at that size', GR, 'start', 'sv-s'), show=1.4)
    f(T(410, 96, 'error = y − ŷ  (violet sticks)', AM, 'start', 'sv-s'), show=2.2)
    f(T(410, 130, 'square each error, average:', MU, 'start'), show=4.6)
    f(T(410, 152, 'MSE = %.2f' % mse, GR, 'start', 'sv-s'), show=5.0)
    f(T(410, 190, 'measured by RMSE, MAE, R²', MU, 'start'), show=5.6)
    return f.render()

# ---------- 3.2 Classification ----------
CX = [0.6, 1.3, 2.0, 2.6, 3.3, 3.7, 4.4, 4.9, 5.6, 6.3, 7.1]
CY = [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1]
def f_cls():
    sig = lambda x: 1 / (1 + math.exp(-1.9 * (x - 3.6)))
    f = Fig('su8-', 680, 300, 'Eleven emails plotted by a spam score feature, each sitting at 0 (not spam) or 1 (spam). An '
            'S-shaped curve gives the probability of spam. One new email is read off the curve at 0.82, above the 0.5 '
            'threshold, so it is labelled spam. The output is one of two classes.', 'OUTPUT IS ONE OF k CLASSES')
    P = Plot(50, 36, 320, 220, (0, 8), (-.08, 1.08))
    f(P.axes('feature', 'P(spam)', yt=((0, '0'), (.5, '0.5'), (1, '1'))))
    for i, (x, y) in enumerate(zip(CX, CY)):
        f(mark(P, x, y, y), show=.2 + i * .07)
    f(P.curve(sig, .2, 7.8, 80, GR, 2.4), show=1.3, d=.7)
    f(L(P.px(0), P.py(.5), P.px(8), P.py(.5), FA, 1, '4 4'), show=2.2)
    nx = 4.4
    p = sig(nx)
    f(L(P.px(nx), P.py(0), P.px(nx), P.py(p), AM, 1.5, '3 3') + L(P.px(0), P.py(p), P.px(nx), P.py(p), AM, 1.5, '3 3') +
      ring(*P.p(nx, p), 8), show=3.0, d=.4)
    f(T(410, 70, 'curve = probability of class 1', GR, 'start', 'sv-s'), show=1.4)
    f(T(410, 96, 'threshold 0.5', MU, 'start'), show=2.2)
    f(T(410, 130, 'new email: P = %.2f' % p, AM, 'start', 'sv-s'), show=3.2)
    f(T(410, 152, '%.2f ≥ 0.5  →  spam' % p, GR, 'start', 'sv-s'), show=3.8)
    f(T(410, 190, 'measured by precision, recall, AUC', MU, 'start'), show=4.6)
    assert abs(p - .82) < .01, p
    return f.render()

# ---------- 4.1 Self-supervised ----------
def f_self():
    words = ['the', 'cat', 'sat', 'on', 'the', 'mat']
    f = Fig('su9-', 680, 230, 'The sentence the cat sat on the mat. One word at a time is hidden behind a mask: sat, then '
            'mat, then cat. The model guesses the hidden word and the hidden word itself is the label, so every sentence '
            'ever written yields labels for free. The label counter climbs to three.', 'HIDE A WORD · THE WORD IS THE LABEL')
    x0, cw = 0, 78
    for i, wd in enumerate(words):
        f(R(x0 + i * (cw + 8), 44, cw, 34, 'var(--bg)', RULE_HI, 5) + T(x0 + i * (cw + 8) + cw / 2, 66, wd, TX, mono=True))
    f(T(560, 64, 'labels: 0', MU, 'start'), hide=1.6)
    for k, j in enumerate([2, 5, 1]):
        t = .6 + k * 1.8
        x = x0 + j * (cw + 8)
        f(R(x, 44, cw, 34, 'var(--bg)', 'none', 5) + R(x, 44, cw, 34, tint('am', '.22'), AM, 5, 1.6) +
          T(x + cw / 2, 66, '[MASK]', AM, mono=True), show=t, hide=t + 1.6, d=.2)
        f(arrow(x + cw / 2, 84, x + cw / 2, 112, AM, 1.4), show=t + .3, d=.2)
        f(T(x + cw / 2, 106 + 26, 'model guesses', FA), show=t + .3, hide=t + 1.0, d=.2)
        f(pill(x + cw / 2, 118, words[j], 'gr', 60), show=t + 1.0, d=.2)
        f(T(560, 64, 'labels: %d' % (k + 1), GR if k == 2 else MU, 'start'), show=t + 1.0, hide=None if k == 2 else t + 1.8 + .6, d=.2)
    f(T(0, 184, 'any text becomes training pairs · no human labels at all', GR, 'start', 'sv-s'), show=6.2)
    f(T(0, 204, 'next-word prediction in LLMs is the same trick', MU, 'start'), show=6.8)
    return f.render()

# ---------- 4.2 Semi-supervised ----------
def f_semi():
    f = Fig('sua-', 680, 300, 'Eighteen grey points, only two of them labelled: one circle, one square. In three waves the '
            'labels spread to the nearest unlabelled points as pseudo-labels, until every point has one. A model then '
            'trains on all eighteen.', 'TWO LABELS · SIXTEEN PSEUDO-LABELS')
    P = plot()
    f(P.axes('feature 1', 'feature 2'))
    seeds = [0, 9]
    for i, (x, y, c) in enumerate(PTS):
        if i not in seeds:
            f(dot(*P.p(x, y)), show=.2)
    for s in seeds:
        x, y, c = PTS[s]
        f(mark(P, x, y, c, 7), show=.6)
        f(ring(*P.p(x, y), 12, GR, '0'), show=.6)
    # spread by distance to own seed, three waves
    d = lambda i: math.dist(PTS[i][:2], PTS[seeds[PTS[i][2]]][:2])
    rest = sorted((i for i in range(18) if i not in seeds), key=d)
    waves = [rest[:6], rest[6:12], rest[12:]]
    for k, wv in enumerate(waves):
        for i in wv:
            x, y, c = PTS[i]
            f(mark(P, x, y, c, 5), show=1.6 + k * 1.1, d=.4)
        f(T(380, 120 + k * 22, 'wave %d · %d pseudo-labels' % (k + 1, len(wv)), AM if k < 2 else GR, 'start'), show=1.6 + k * 1.1)
    f(T(380, 70, '2 real labels (ringed)', GR, 'start', 'sv-s'), show=.6)
    f(T(380, 92, 'neighbours copy the nearest label', MU, 'start'), show=1.4)
    f(T(380, 210, 'risk: a wrong early guess', RD, 'start') + T(380, 226, 'gets copied again and again', RD, 'start'), show=5.2)
    return f.render()

# ---------- 4.3 Transfer learning ----------
def f_transfer():
    f = Fig('sub-', 680, 262, 'A network of four layers was trained on millions of images. Its layers are locked. A new '
            'small head is added on top. Two hundred labelled photos flow in, and only the head is trained; the locked '
            'layers just reuse what they learned.', 'REUSE A MODEL TRAINED ON MILLIONS')
    x0 = 200
    names = ['edges', 'textures', 'parts', 'objects']
    for i, n in enumerate(names):
        y = 190 - i * 38
        f(R(x0, y, 200, 30, tint('bl', '.14'), BL, 5) + T(x0 + 100, y + 20, n, BL), show=.2 + i * .15)
    f(T(x0 + 214, 196, 'pretrained on millions of images', MU, 'start'), show=.8)
    f(T(x0 + 214, 140, 'locked · not updated', MU, 'start'), show=1.6)
    f(R(x0 - 4, 70, 208, 154, 'none', FA, 6, 1, '4 3'), show=1.6)
    f(R(x0 + 40, 32, 120, 30, tint('am', '.22'), AM, 5, 1.6) + T(x0 + 100, 52, 'new head', AM, 'middle', 'sv-s'), show=2.4)
    f(T(x0 + 174, 52, 'trained', AM, 'start'), show=2.4)
    for k in range(4):
        t = 3.0 + k * .45
        f(pill(x0 - 90, 120, '200 photos', 'bl', 90), show=t, hide=None if k == 3 else t + .4, move=(t, -40, 0, .35), d=.15)
    f(arrow(x0 - 42, 130, x0 - 8, 130, BL, 1.3), show=3.0)
    for k in range(3):
        f(R(x0 + 40, 32, 120, 30, tint('am', '.10'), 'none', 5), show=3.4 + k * .5, hide=3.6 + k * .5, d=.15)
    f(T(0, 240, 'small labelled set · strong start · the default for images and text', GR, 'start', 'sv-s'), show=5.0)
    return f.render()

# ---------- 4.4 Active learning ----------
def f_active():
    f = Fig('suc-', 680, 300, 'Grey unlabelled points sit around a boundary learned from a few labels. The model rings the '
            'point nearest the boundary, the one it is least sure of, and asks a human. The answer comes back, the point '
            'is coloured, and the boundary shifts. This repeats twice more.', 'ASK ONLY ABOUT THE DOUBTFUL POINTS')
    P = plot()
    f(P.axes('feature 1', 'feature 2'))
    lab = {0: 0, 9: 1, 3: 0, 12: 1}
    for i, (x, y, c) in enumerate(PTS):
        f(mark(P, x, y, c) if i in lab else dot(*P.p(x, y)), show=.2)
    # boundary x + y = s ; queries = unlabelled points with smallest |x+y-s|
    s = 7.4
    t = 1.0
    unl = [i for i in range(18) if i not in lab]
    for k in range(3):
        a, b = P.p(max(0, s - 8.2), min(8.2, s)), P.p(min(8.2, s), max(0, s - 8.2))
        f(L(a[0], a[1], b[0], b[1], MU, 1.6, '6 4'), show=t, hide=t + 1.7, d=.3)
        q = min(unl, key=lambda i: abs(PTS[i][0] + PTS[i][1] - s)); unl.remove(q)
        x, y, c = PTS[q]
        f(ring(*P.p(x, y), 12), show=t + .5, hide=t + 1.7)
        f(pill(450, 92, 'ask human: point %d?' % (k + 1), 'am', 150), show=t + .5, hide=t + 1.3, d=.2)
        f(mark(P, x, y, c), show=t + 1.3, d=.3)
        lab[q] = c
        sa = [PTS[i][0] + PTS[i][1] for i in lab if PTS[i][2] == 0]
        sb = [PTS[i][0] + PTS[i][1] for i in lab if PTS[i][2] == 1]
        s = (max(sa) + min(sb)) / 2
        t += 1.8
    a, b = P.p(max(0, s - 8.2), min(8.2, s)), P.p(min(8.2, s), max(0, s - 8.2))
    f(L(a[0], a[1], b[0], b[1], GR, 2, '6 4'), show=t, d=.3)
    f(T(380, 140, '7 labels instead of 18', GR, 'start', 'sv-s'), show=t + .2)
    f(T(380, 162, 'boundary settles where it matters', MU, 'start'), show=t + .5)
    f(T(380, 200, 'cost: the labelled set is skewed to', MU, 'start') + T(380, 216, 'hard cases · not a fair test set', MU, 'start'), show=t + 1.0)
    return f.render()

if __name__ == '__main__':
    splice(PAGE, [f_sup(), f_unsup(), f_rl(), f_logged(), f_hand(), f_behav(), f_reg(), f_cls(),
                  f_self(), f_semi(), f_transfer(), f_active()])
