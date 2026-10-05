# -*- coding: utf-8 -*-
"""Figures + article for content/07-machine-learning/01-overview/ml-overview (shelf overview).
Run: python3 ml_overview.py  -> rewrites the <article> of the page. Every number comes from the models below."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mlplot import *  # noqa

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/01-overview/ml-overview/index.html')
rnd = random.Random(7)

# ---------- data ----------
# spam: x = 'free' count, y = links; spam when x + y (+ noise) > 10
SP = [(rnd.uniform(.5, 9.5), rnd.uniform(.5, 9.5)) for _ in range(44)]
SY = [1 if a + b + rnd.gauss(0, 1.1) > 10 else 0 for a, b in SP]
def acc(pred, P, Y): return sum(pred(p) == t for p, t in zip(P, Y)) / len(P)
hand = lambda p: 1 if p[0] >= 5 else 0
H = logreg_path(SP, SY, (0, 0, 0), lr=.08, steps=1500)
lw = H[-1]
learned = lambda p: 1 if lw[0] * p[0] + lw[1] * p[1] + lw[2] > 0 else 0
A_HAND, A_LEARN = acc(hand, SP, SY), acc(learned, SP, SY)
assert A_LEARN > A_HAND

# moons-ish data for the model families (train + test)
def moon(n, seed):
    r = random.Random(seed); P, Y = [], []
    for _ in range(n):
        a, b = r.uniform(.4, 9.6), r.uniform(.4, 9.6)
        t = 1 if b > 5 + 2.6 * math.sin((a - 1) * .75) + r.gauss(0, .7) else 0
        P.append((a, b)); Y.append(t)
    return P, Y
MP, MY = moon(70, 11)
TP, TY = moon(400, 12)

def fig_rules():
    f = Anim('mo1-', 720, 366, 'Spam emails as dots: free-word count against links. A person writes the rule "free at least 5 means spam": '
             'a vertical line that misses the diagonal pattern. The learned model starts flat and tilts step by step into the diagonal boundary.',
             'SAME EMAILS · A WRITTEN RULE VS A LEARNED RULE')
    for k, (x0, title) in enumerate([(40, 'a person writes the rule'), (410, 'the machine learns the rule')]):
        pl = Plot(x0, 56, 250, 220, 0, 10, 0, 10)
        f.static(frame_box(pl) + T(x0, 46, title, TX, 'start', 'sv-s'))
        f.static(T(x0 + 125, 296, '“free” count →', MU) + T(x0 - 8, 166, 'links', MU, 'end'))
        for i, (p, t) in enumerate(zip(SP, SY)):
            f.show(dot(*pl.P(*p), tone='am' if t else 'bl'), .2 + i * .02, d=.2)
        if k == 0:
            P0 = pl
        else:
            P1 = pl
    f.show(T(350, 156, '● spam', COL['am']) + T(350, 176, '● normal', COL['bl']), 1.2)
    # hand rule
    t = 1.8
    f.show(L(P0.X(5), P0.py, P0.X(5), P0.py + P0.ph, RD, 2) + T(P0.X(5) + 6, P0.py + 14, 'if free ≥ 5 → spam', RD, 'start'), t)
    wrong = [p for p, y in zip(SP, SY) if hand(p) != y]
    f.show(''.join(ringc(*P0.P(*p), 8, RD) for p in wrong), t + .8)
    f.show(pill(P0.X(5), 304, '%d / %d right = %.2f' % (len(SP) - len(wrong), len(SP), A_HAND), 'rd', 150), t + 1.4)
    # learned: snapshots of the boundary
    t = 4.0
    snaps = [3, 10, 30, 90, 300, len(H) - 1]
    for j, s in enumerate(snaps):
        w = H[s]; seg = clipline(P1, *w)
        last = j == len(snaps) - 1
        if not seg: continue
        (a, b), (c, d) = seg
        g = L(a, b, c, d, GR if last else AM, 2.2 if last else 1.6, None if last else '5 4')
        if not last:
            g += T(P1.px + P1.pw - 6, P1.py + 14, 'step %d' % s, AM, 'end')
        f.show(g, t + j * .7, hide=None if last else t + j * .7 + .7, d=.25)
    t += len(snaps) * .7
    wrong = [p for p, y in zip(SP, SY) if learned(p) != y]
    f.show(''.join(ringc(*P1.P(*p), 8, RD) for p in wrong), t)
    f.show(pill(P1.X(5), 304, '%d / %d right = %.2f' % (len(SP) - len(wrong), len(SP), A_LEARN), 'gr', 150), t + .5)
    return f.render()

# ---------- training loop on a line ----------
LX = [1, 2, 3, 4, 5, 6, 7, 8, 9]
LY = [2.1, 2.4, 3.6, 3.5, 4.6, 5.3, 5.2, 6.4, 6.6]
def gd_line(steps=60, lr=.02):
    w, b = 0.0, sum(LY) / len(LY); hist = []
    for _ in range(steps + 1):
        loss = sum((w * x + b - y) ** 2 for x, y in zip(LX, LY)) / len(LX)
        hist.append((w, b, loss))
        gw = sum(2 * (w * x + b - y) * x for x, y in zip(LX, LY)) / len(LX)
        gb = sum(2 * (w * x + b - y) for x, y in zip(LX, LY)) / len(LX)
        w, b = w - lr * gw, b - lr * gb
    return hist
GL = gd_line(400, .03)

def fig_loop():
    f = Anim('mo2-', 720, 346, 'Nine points and a line. The line starts flat, the vertical gaps to each point are the errors and the loss bar is tall. '
             'Each step tilts the line, the gaps shrink and the loss bar drops.', 'TRAINING · PREDICT, MEASURE THE LOSS, ADJUST, REPEAT')
    pl = Plot(50, 40, 380, 240, 0, 10, 0, 8)
    f.static(pl.axes('x', 'y', [(v, str(v)) for v in (2, 4, 6, 8)], [(v, str(v)) for v in (2, 4, 6)]))
    for i, (x, y) in enumerate(zip(LX, LY)):
        f.show(dot(*pl.P(x, y)), .2 + i * .06, d=.2)
    # loss axis
    bx, by, bh = 560, 40, 240
    Lmax = GL[0][2]
    f.static(L(bx - 30, by + bh, bx + 70, by + bh, MU, 1.2) + T(bx + 20, by + bh + 18, 'loss', MU))
    snaps = [0, 1, 3, 10, 30, 100, 400]
    t = 1.2
    for j, s in enumerate(snaps):
        w, b, loss = GL[s]; last = j == len(snaps) - 1
        c = GR if last else AM
        g = L(*pl.P(0, b), *pl.P(10, w * 10 + b), c, 2.2)
        for x, y in zip(LX, LY):
            g += L(*pl.P(x, y), *pl.P(x, w * x + b), RD if not last else GR, 1.2, '3 2')
        hh = bh * loss / Lmax
        g2 = R(bx, by + bh - hh, 40, hh, tint('gr' if last else 'am', '.25'), c, 3, 1.4) + T(bx + 20, by + bh - hh - 8, '%.2f' % loss, c, mono=True, bold=True)
        g2 += T(bx + 54, by + 20, 'step %d' % s, c, 'start', mono=True, bold=True)
        hide = None if last else t + .9
        f.show(g, t, hide=hide, d=.3); f.show(g2, t, hide=hide, d=.3)
        t += .9 if j < 2 else .75
    f.show(T(240, 318, 'dashed gaps = errors · loss = their squares, averaged', MU), t)
    return f.render()

# ---------- problem types ----------
HS = [(50, 160), (65, 205), (80, 230), (90, 275), (110, 300), (120, 350), (140, 380), (155, 420), (170, 455)]
def fit1(pts):
    n = len(pts); mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
    w = sum((p[0] - mx) * (p[1] - my) for p in pts) / sum((p[0] - mx) ** 2 for p in pts)
    return w, my - w * mx

def fig_regression():
    w, b = fit1(HS)
    f = Anim('mo3-', 720, 336, 'House size against price. A line is fitted through the points; a new house of 130 square metres '
             'gets its price read off the line.', 'REGRESSION · THE LABEL IS A NUMBER')
    pl = Plot(60, 36, 440, 230, 40, 180, 100, 500)
    f.static(pl.axes('size m²', 'price k', [(v, str(v)) for v in (60, 100, 140, 180)], [(v, str(v)) for v in (200, 300, 400)]))
    for i, p in enumerate(HS):
        f.show(dot(*pl.P(*p)), .2 + i * .08, d=.2)
    f.show(L(*pl.P(40, w * 40 + b), *pl.P(180, w * 180 + b), GR, 2.2), 1.4, d=.8)
    xn = 130; yn = w * xn + b
    f.show(L(*pl.P(xn, 100), *pl.P(xn, yn), AM, 1.4, '4 3') + dot(*pl.P(xn, 100), 5, 'am', True) + T(pl.X(xn), pl.Y(100) - 8, 'new', AM), 2.6)
    f.show(L(*pl.P(xn, yn), *pl.P(40, yn), AM, 1.4, '4 3') + dot(*pl.P(xn, yn), 5.5, 'am'), 3.3)
    f.show(pill(600, pl.Y(yn) - 10, 'ŷ = %d k' % round(yn), 'gr', 110), 3.9)
    f.show(T(600, pl.Y(yn) + 30, 'any number is a valid answer', MU), 4.2)
    return f.render()

def fig_classify():
    f = Anim('mo4-', 720, 346, 'The spam dots again. A boundary line splits the plane in two; a new email lands on the spam side and is labelled spam.',
             'CLASSIFICATION · THE LABEL IS A CLASS')
    pl = Plot(60, 36, 260, 260, 0, 10, 0, 10)
    f.static(frame_box(pl) + T(190, 318, '“free” count →', MU) + T(52, 166, 'links', MU, 'end'))
    for i, (p, t) in enumerate(zip(SP, SY)):
        f.show(dot(*pl.P(*p), tone='am' if t else 'bl'), .2 + i * .02, d=.2)
    (a, b), (c, d) = clipline(pl, *lw)
    f.show(L(a, b, c, d, GR, 2.2), 1.4, d=.8)
    f.show(T(pl.X(8.6), pl.Y(9.3), 'spam', COL['am'], bold=True) + T(pl.X(1.4), pl.Y(.7), 'normal', COL['bl'], bold=True), 2.0)
    new = (6.6, 7.0)
    f.path(dot(*pl.P(*new), 6, None, True), [(0, 300, -pl.Y(new[1]) + 60), (2.6, 0, 0)], t0=2.4, d=.9)
    f.show(dot(*pl.P(*new), 6, 'am') + ringc(*pl.P(*new), 11, AM), 3.6)
    z = lw[0] * new[0] + lw[1] * new[1] + lw[2]
    f.show(pill(520, pl.Y(new[1]) - 10, 'spam · p = %.2f' % sig(z), 'gr', 140), 4.0)
    f.show(T(520, pl.Y(new[1]) + 30, 'answer is one of a few classes', MU), 4.3)
    return f.render()

def kmeans(P, C, it=3):
    hist = []
    for _ in range(it):
        lab = [min(range(len(C)), key=lambda k: (p[0] - C[k][0]) ** 2 + (p[1] - C[k][1]) ** 2) for p in P]
        hist.append((list(C), lab))
        C = [(sum(p[0] for p, l in zip(P, lab) if l == k) / max(1, lab.count(k)),
              sum(p[1] for p, l in zip(P, lab) if l == k) / max(1, lab.count(k))) for k in range(len(C))]
    hist.append((list(C), lab))
    return hist
r2 = random.Random(5)
KP = [(r2.gauss(cx, .9), r2.gauss(cy, .9)) for cx, cy in [(2.6, 7.2), (7.4, 7.6), (5.2, 2.6)] for _ in range(12)]
KH = kmeans(KP, [(4.0, 5.5), (6.0, 6.0), (5.0, 4.0)], 2)

def fig_cluster():
    tones = ['bl', 'am', 'gr']
    f = Anim('mo5-', 720, 346, 'Grey dots with no labels. Three centres are dropped in, each dot takes the colour of its nearest centre, '
             'the centres slide to the middle of their dots, and after a few rounds three groups appear.', 'UNSUPERVISED · NO LABELS, FIND THE GROUPS')
    pl = Plot(60, 36, 260, 260, 0, 10, 0, 10)
    f.static(frame_box(pl))
    for i, p in enumerate(KP):
        f.show(dot(*pl.P(*p), tone=None), .2 + i * .02, d=.2, hide=1.6 if True else None)
    t = 1.4
    C0 = KH[0][0]
    for r_, (C, lab) in enumerate(KH[:-1]):
        last = r_ == len(KH) - 2
        g = ''.join(dot(*pl.P(*p), tone=tones[l]) for p, l in zip(KP, lab))
        f.show(g, t + .6, hide=None if last else t + 2.0, d=.3)
        t += 1.4
    # centres slide through the history
    pts = []
    for k in range(3):
        x0, y0 = pl.P(*C0[k])
        path = [(0, 0, 0)] + [(1.4 + 1.4 * (j + 1) - .2, pl.X(KH[j + 1][0][k][0]) - x0, pl.Y(KH[j + 1][0][k][1]) - y0) for j in range(len(KH) - 1)]
        cross = ('<path d="M%.1f %.1f l7 7 m0 -7 l-7 7" stroke="%s" stroke-width="2.6" transform="translate(-3.5,-3.5)"/>' % (x0, y0, COL[tones[k]]) +
                 ringc(x0, y0, 9, COL[tones[k]], 2))
        f.path(cross, path, t0=1.2, d=.6)
    f.show(T(470, 120, 'round 1: nearest centre', MU), 2.0, hide=3.4)
    f.show(T(470, 120, 'centres move to the middle', MU), 3.4, hide=5.0)
    f.show(pill(470, 110, '3 groups found', 'gr', 130), t + .3)
    f.show(T(470, 150, 'nobody told it the groups', MU), t + .5)
    f.show(T(470, 168, '— it found the structure', MU), t + .5)
    return f.render()

def fig_reinforce():
    f = Anim('mo6-', 720, 262, 'A robot on a track of six cells walks right; every step gives reward 0 until the last cell gives +1. '
             'Then the value of each cell is filled in backwards from the goal: 1.00, 0.90, 0.81 and so on.', 'REINFORCEMENT · NO LABELS, ONLY A REWARD AT THE END')
    X0, W, G, Y = 40, 90, 14, 70
    for i in range(6):
        f.static(R(X0 + i * (W + G), Y, W, 50, 'var(--bg)', RULE_HI, 6, 1.2) + T(X0 + i * (W + G) + W / 2, Y + 70, 'cell %d' % i, FA, mono=True))
    f.static(T(X0 + 5 * (W + G) + W / 2, Y - 10, 'goal +1', GR, bold=True))
    cx = lambda i: X0 + i * (W + G) + W / 2
    bot = '<circle cx="%.1f" cy="%.1f" r="12" fill="%s" stroke="%s" stroke-width="1.6"/>' % (cx(0), Y + 25, tint('am', '.3'), AM)
    f.path(bot, [(0, 0, 0)] + [(.8 + i * .55, cx(i) - cx(0), 0) for i in range(1, 6)], t0=.3, d=.4, hide=4.6)
    for i in range(1, 6):
        f.show(T(cx(i), Y + 100, 'r = %s' % ('+1' if i == 5 else '0'), GR if i == 5 else MU, mono=True), .9 + i * .55, hide=4.6)
    t = 4.8
    f.show(T(40, 210, 'value of a cell = reward you can still expect from there, ×0.9 per step', MU, 'start'), t)
    for k, i in enumerate(range(5, -1, -1)):
        v = .9 ** (5 - i)
        f.show(R(X0 + i * (W + G) + 3, Y + 3, W - 6, 44, tint('gr', '%.2f' % (.1 + .3 * v)), 'none', 4) +
               T(cx(i), Y + 30, '%.2f' % v, GR, mono=True, bold=True), t + .3 + k * .45)
    return f.render()

# ---------- model families ----------
def family(pre, title, aria, pred, extra=None, note1='', note2=''):
    f = Anim(pre, 720, 346, aria, title)
    pl = Plot(40, 36, 260, 260, 0, 10, 0, 10)
    f.static(frame_box(pl))
    t = .2
    if extra: t = extra(f, pl)
    t = shade(pl, pred, 25, t, .05, f)
    for i, (p, y) in enumerate(zip(MP, MY)):
        f.static(dot(*pl.P(*p), 4, 'am' if y else 'bl'))
    tr, te = acc(pred, MP, MY), acc(pred, TP, TY)
    f.show(T(360, 70, note1, TX, 'start', 'sv-s'), .3)
    f.show(T(360, 92, note2, MU, 'start'), .3)
    f.show(T(360, 200, 'train accuracy', MU, 'start') + T(560, 200, '%.2f' % tr, TX, 'end', mono=True, bold=True), t + .2)
    f.show(T(360, 226, 'new-data accuracy', MU, 'start') + pill(600, 212, '%.2f' % te, 'gr', 60), t + .5)
    f.show(T(360, 270, 'same 70 dots in every family · 400 new dots to test', FA, 'start'), t + .8)
    return f.render(), tr, te

def fig_families():
    out = {}
    Hm = logreg_path(MP, MY, (0, 0, 0), lr=.05, steps=3000)[-1]
    lin = lambda p: 1 if Hm[0] * p[0] + Hm[1] * p[1] + Hm[2] > 0 else 0
    def ex_lin(f, pl):
        (a, b), (c, d) = clipline(pl, *Hm); f.show(L(a, b, c, d, GR, 2.2), .3, d=.8); return 1.2
    out['lin'] = family('mo7-', 'LINEAR · ONE STRAIGHT BOUNDARY', 'A straight boundary is drawn through the wavy two-class data, then the regions fill in; it cannot follow the wave.',
                        lin, ex_lin, 'assumes a straight boundary', 'weights you can read one by one')
    splits, tp = tree(MP, MY, 4)
    def ex_tree(f, pl):
        t = .3
        for ax, thr, lo, hi in splits:
            if ax == 0: g = L(pl.X(thr), pl.Y(hi[1]), pl.X(thr), pl.Y(lo[1]), AM, 1.8)
            else: g = L(pl.X(lo[0]), pl.Y(thr), pl.X(hi[0]), pl.Y(thr), AM, 1.8)
            f.show(g, t, d=.3); t += .35
        return t + .2
    out['tree'] = family('mo8-', 'TREES · SPLIT, THEN SPLIT AGAIN', 'Axis-parallel cuts appear one by one, each splitting a box in two; the regions become a staircase that follows the wave.',
                         tp, ex_tree, 'assumes yes/no thresholds', 'boxes cut parallel to the axes')
    kp = knn(MP, MY, 5)
    def ex_knn(f, pl):
        q = (5.0, 5.4)
        d = sorted(range(len(MP)), key=lambda i: (MP[i][0] - q[0]) ** 2 + (MP[i][1] - q[1]) ** 2)[:5]
        rad = math.dist(MP[d[-1]], q) / 10 * pl.pw + 6
        f.show(dot(*pl.P(*q), 6, None, True), .3)
        f.show('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="4 3"/>' % (*pl.P(*q), rad, AM), .8, hide=2.6)
        f.show(''.join(ringc(*pl.P(*MP[i]), 7, AM) for i in d), 1.3, hide=2.6)
        v = sum(MY[i] for i in d)
        f.show(T(pl.X(q[0]), pl.Y(q[1]) - 14, '%d vs %d' % (v, 5 - v), AM, bold=True), 1.6, hide=2.6)
        return 2.7
    out['knn'] = family('mo9-', 'NEIGHBOURS · ASK THE CLOSEST POINTS', 'A new point draws a circle around its five nearest neighbours and takes their majority vote; repeating that everywhere gives a ragged boundary.',
                        kp, ex_knn, 'assumes close points share a label', 'k = 5 nearest neighbours vote')
    mp = mlp(MP, MY)
    out['nn'] = family('mo10-', 'NEURAL NETWORK · LEARN THE SHAPE', 'Regions fill in column by column along a smooth curved boundary that follows the wave.',
                       mp, None, 'assumes nothing about the shape', '8 hidden units learn the curve')
    return out

# ---------- generalization ----------
GX = [i / 9 for i in range(10)]
gr = random.Random(4)
GY = [math.sin(2 * math.pi * x) + gr.gauss(0, .3) for x in GX]
TXs = [i / 199 for i in range(200)]
TYs = [math.sin(2 * math.pi * x) + gr.gauss(0, .3) for x in TXs]
def mse(c, X, Y): return sum((peval(c, x) - y) ** 2 for x, y in zip(X, Y)) / len(X)

def fig_fit(pre, deg, title, aria, word, wt='rd'):
    c = polyfit(GX, GY, deg, 0)
    tr, te = mse(c, GX, GY), mse(c, TXs, TYs)
    f = Anim(pre, 720, 326, aria, title)
    pl = Plot(40, 40, 400, 220, 0, 1, -2.2, 2.2)
    f.static(frame_box(pl) + L(pl.px, pl.Y(0), pl.px + pl.pw, pl.Y(0), 'var(--rule)', 1, '2 4'))
    for i, (x, y) in enumerate(zip(GX, GY)):
        f.show(dot(*pl.P(x, y)), .2 + i * .06, d=.2)
    f.show(pl.curve(lambda x: peval(c, x), 0, 1, 200, AM, 2.2, clip=(-2.2, 2.2)), 1.0, d=.8)
    tx = [TXs[i] for i in range(7, 200, 22)]; ty = [TYs[i] for i in range(7, 200, 22)]
    f.show(''.join(dot(*pl.P(x, y), 4, 'gr', True) for x, y in zip(tx, ty)), 2.4)
    f.show(''.join(L(*pl.P(x, y), *pl.P(x, max(-2.2, min(2.2, peval(c, x)))), RD, 1.2, '3 2') for x, y in zip(tx, ty)), 3.0)
    f.static(T(40, 290, '● training points', COL['bl'], 'start') + T(160, 290, '○ new points', COL['gr'], 'start'))
    # error bars
    bx, top = 500, 70; mx = 0.6
    f.static(T(bx, 52, 'error (MSE)', MU, 'start'))
    for k, (lab, v, tone, t) in enumerate([('on training points', tr, 'bl', 2.0), ('on new points', te, wt, 3.4)]):
        y = top + k * 60
        w = 180 * min(v, mx) / mx
        f.show(T(bx, y + 4, lab, MU, 'start') + R(bx, y + 12, max(w, 2), 16, tint(tone, '.25'), COL[tone], 3, 1.2) +
               T(bx + max(w, 2) + 6, y + 25, ('%.2f' % v) + ('+' if v > mx else ''), COL[tone], 'start', mono=True, bold=True), t)
    f.show(pill(590, 210, word, wt, 170), 4.0)
    return f.render(), tr, te

# ---------- learning order ----------
def fig_order():
    ST = [('Math', 'math-foundations'), ('Statistics', ''), ('Core concepts', ''), ('Classical', ''),
          ('Trees', ''), ('Clustering', ''), ('PCA', ''), ('Evaluation', '')]
    sub = ['loss · gradient', 'sample → truth', 'split · overfit', 'linear · SVM · kNN', 'forest · boosting', 'groups, no labels', 'fewer columns', 'right yardstick']
    f = Anim('mo13-', 720, 212, 'A track of eight stops from Math to Evaluation; a marker travels along it and each stop lights up with what it adds.',
             'LEARNING ORDER · EIGHT STOPS')
    X = [50 + i * 88 for i in range(8)]; Y = 80
    f.static(L(X[0], Y, X[-1], Y, RULE_HI, 3))
    t = .5
    for i, x in enumerate(X):
        f.static('<circle cx="%.1f" cy="%.1f" r="9" fill="var(--bg)" stroke="var(--rule-hi)" stroke-width="2"/>' % (x, Y))
        f.static(T(x, Y - (20 if i % 2 == 0 else 34), ST[i][0], TX, 'middle', 'sv-s'))
        if i: f.show(L(X[i - 1], Y, x, Y, BL, 3), t, d=.4); t += .45
        last = i == 7
        f.show('<circle cx="%.1f" cy="%.1f" r="9" fill="%s"/>' % (x, Y, GR if last else BL), t, d=.25)
        f.show(T(x, Y + (30 if i % 2 == 0 else 48), sub[i], GR if last else MU), t + .1)
        t += .3
    f.show(T(40, 186, 'first three stops are the base every model lesson assumes', MU, 'start'), t + .2)
    return f.render()

if __name__ == '__main__':
    F = {}
    F['rules'] = fig_rules(); F['loop'] = fig_loop()
    F['reg'] = fig_regression(); F['cls'] = fig_classify(); F['clu'] = fig_cluster(); F['rl'] = fig_reinforce()
    fam = fig_families()
    F['under'], u_tr, u_te = fig_fit('mo11-', 1, 'UNDERFITTING · TOO SIMPLE FOR THE WAVE',
        'A straight line through ten wavy points misses most of them; new points miss by about as much.', 'too simple')
    F['over'], o_tr, o_te = fig_fit('mo12-', 9, 'OVERFITTING · MEMORISES THE NOISE',
        'A degree-nine curve passes through all ten points but swings wildly between them; new points miss by a lot.', 'memorised')
    F['good'], g_tr, g_te = fig_fit('mo14-', 3, 'GOOD FIT · FOLLOWS THE WAVE, IGNORES THE NOISE',
        'A degree-three curve follows the wave without chasing each point; the error on new points is the lowest of the three.', 'generalises', 'gr')
    F['order'] = fig_order()
    print('hand %.2f learned %.2f' % (A_HAND, A_LEARN))
    for k, (s, tr, te) in fam.items(): print(k, '%.2f %.2f' % (tr, te))
    print('good %.3f %.3f' % (g_tr, g_te)); print('under %.3f %.3f over %.3f %.3f' % (u_tr, u_te, o_tr, o_te))
    import json
    F = {k: palette(v if isinstance(v, str) else v) for k, v in F.items()}
    for k in ('lin', 'tree', 'knn', 'nn'): F[k] = palette(fam[k][0])
    F['_nums'] = dict(hand=A_HAND, learn=A_LEARN, fam={k: v[1:] for k, v in fam.items()}, u=(u_tr, u_te), o=(o_tr, o_te), reg=fit1(HS))
    json.dump(F, open('/tmp/ml/ml-overview-figs.json', 'w'))
