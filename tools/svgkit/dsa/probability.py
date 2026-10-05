# -*- coding: utf-8 -*-
"""Figures for content/07-machine-learning/02-math-foundations/probability.
Run: python3 probability.py -> writes /tmp/ml/probability-figs.json (FIG1..FIG11). Every curve is computed."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from tablefig import T, R, L, arrow, Fig, MU, TX, FA, RULE_HI

BR, VI, FI, RO, GH = 'var(--brand)', 'var(--violet)', 'var(--filled)', 'var(--rose)', 'var(--ghost)'
def a(tok, x): return 'rgba(var(--%s),%s)' % (tok, x)
BRA, VIA, FIA, ROA = (lambda x: a('clay-a', x)), (lambda x: a('violet-a', x)), (lambda x: a('blue-a', x)), (lambda x: a('rose-a', x))

def C(x, y, r, fill, stroke='none', sw=1):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, y, r, fill, stroke, sw)
def P(pts, c, sw=2, dash=None, fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<path d="M%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"%s/>' % (
        ' L'.join('%.1f %.1f' % p for p in pts), fill, c, sw, d)
def area(pts, y0, fill):
    pts = [(pts[0][0], y0)] + pts + [(pts[-1][0], y0)]
    return '<path d="M%sZ" fill="%s" stroke="none"/>' % (' L'.join('%.1f %.1f' % p for p in pts), fill)

class Plot:
    def __init__(s, x, y, w, h, xr, yr):
        s.x, s.y, s.w, s.h, s.xr, s.yr = x, y, w, h, xr, yr
    def px(s, v): return s.x + (v - s.xr[0]) / (s.xr[1] - s.xr[0]) * s.w
    def py(s, v): return s.y + s.h - (v - s.yr[0]) / (s.yr[1] - s.yr[0]) * s.h
    def axes(s, xt=(), yt=(), xl='', yl=''):
        o = L(s.x, s.y + s.h, s.x + s.w + 6, s.y + s.h, MU, 1.1) + L(s.x, s.y + s.h, s.x, s.y - 6, MU, 1.1)
        for v, lab in xt:
            o += L(s.px(v), s.y + s.h, s.px(v), s.y + s.h + 4, MU, 1) + T(s.px(v), s.y + s.h + 16, lab, FA, cls='sv-l')
        for v, lab in yt:
            o += L(s.x, s.py(v), s.x + s.w, s.py(v), 'var(--rule)', 1, '2 4') + T(s.x - 6, s.py(v) + 4, lab, FA, 'end', cls='sv-l')
        if xl: o += T(s.x + s.w + 6, s.y + s.h + 30, xl, MU, 'end')
        if yl: o += T(s.x + 4, s.y - 10, yl, MU, 'start')
        return o
    def curve(s, f, a_, b_, n=120):
        return [(s.px(a_ + (b_ - a_) * i / n), s.py(f(a_ + (b_ - a_) * i / n))) for i in range(n + 1)]
    def bar(s, v, p, bw, fill, stroke):
        x0 = s.px(v) - bw / 2
        return R(x0, s.py(p), bw, s.py(0) - s.py(p), fill, stroke, 2, 1.2)

def draw(F, pts, t, c, dur=1.2, sw=2.2, dash=None, k=16, hide=None):
    """A curve that grows left to right: consecutive pieces fade in."""
    n = len(pts) - 1; step = max(1, n // k); i = 0; j = 0
    segs = []
    while i < n:
        segs.append(pts[i:min(n, i + step) + 1]); i += step
    for m, sg in enumerate(segs):
        F(P(sg, c, sw, dash), show=t + m * dur / len(segs), hide=hide, d=.08)
    return t + dur

def npdf(x, m=0, s=1): return math.exp(-(x - m) ** 2 / (2 * s * s)) / (s * math.sqrt(2 * math.pi))

class LCG:
    def __init__(s, seed): s.v = seed
    def u(s):
        s.v = (1103515245 * s.v + 12345) % (2 ** 31); return s.v / 2 ** 31
    def n(s):
        return math.sqrt(-2 * math.log(1 - s.u())) * math.cos(2 * math.pi * s.u())

figs = {}

# ---------- 1.1 random variable & distribution ----------
def f11():
    F = Fig('pd1-', 720, 300, 'Left: the sum of two dice is a discrete random variable. Its eleven bars rise one by one, '
            'from 2 to 12, the tallest at 7 with 6 of 36. Right: a continuous variable has a smooth bell curve; the '
            'region between minus one and plus one fills in and holds 68 percent of the area.',
            'DISCRETE · BARS (PMF)')
    F(T(410, 14, 'CONTINUOUS · AREA UNDER A CURVE (PDF)', MU, 'start', 'sv-hv'))
    A = Plot(40, 60, 280, 180, (1.3, 12.7), (0, 7 / 36))
    F(A.axes([(v, str(v)) for v in range(2, 13)], [(2 / 36, '2/36'), (4 / 36, '4/36'), (6 / 36, '6/36')], 'sum of two dice'))
    pm = {s: sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s) / 36 for s in range(2, 13)}
    assert abs(sum(pm.values()) - 1) < 1e-9 and pm[7] == 6 / 36
    for k, s in enumerate(range(2, 13)):
        F(A.bar(s, pm[s], 18, BRA('.22'), BR), show=.4 + k * .18)
    F(R(A.px(7) - 13, A.py(pm[7]) - 4, 26, A.py(0) - A.py(pm[7]) + 8, 'none', VI, 4, 2), show=2.8)
    F(T(A.px(7), A.py(pm[7]) - 10, 'P(7) = 6/36', VI, cls='sv-s'), show=2.8)
    B = Plot(410, 60, 280, 180, (-3.2, 3.2), (0, .42))
    F(B.axes([(v, str(v)) for v in (-3, -2, -1, 0, 1, 2, 3)], [], 'x', ), show=3.4)
    t = draw(F, B.curve(npdf, -3.2, 3.2), 3.6, BR, 1.4)
    F(area(B.curve(npdf, -1, 1, 60), B.py(0), FIA('.22')), show=t + .3)
    F(L(B.px(-1), B.py(0), B.px(-1), B.py(npdf(-1)), FI, 1.4) + L(B.px(1), B.py(0), B.px(1), B.py(npdf(1)), FI, 1.4), show=t + .3)
    F(T(B.px(0), B.py(.14), 'area 0.68', FI, cls='sv-s'), show=t + .7)
    F(T(B.px(1.9), B.py(.36), 'height ≠ probability', MU), show=t + 1.2)
    F(T(0, 292, 'a probability is a bar height for counts, an area for a continuum', MU, 'start'), show=t + 1.6)
    return F.render()

# ---------- 1.2 expectation ----------
def f12():
    xs = list(range(7)); ps = [.10, .30, .22, .16, .10, .07, .05]
    assert abs(sum(ps) - 1) < 1e-9
    mu = sum(x * p for x, p in zip(xs, ps)); assert abs(mu - 2.27) < 1e-9
    F = Fig('pe1-', 720, 300, 'Items in a basket, 0 to 6, with their probabilities as bars. A ring visits each bar and adds '
            'value times probability to a running sum: 0, 0.30, 0.74, 1.22, 1.62, 1.97, 2.27. A balance point then slides '
            'under the bars and stops at 2.27, where they balance. The tallest bar, the mode, is at 1.', 'EXPECTATION · THE BALANCE POINT')
    A = Plot(60, 50, 440, 180, (-.6, 6.6), (0, .32))
    F(A.axes([(x, str(x)) for x in xs], [(.1, '0.10'), (.2, '0.20'), (.3, '0.30')], 'items in basket'))
    for k, (x, p) in enumerate(zip(xs, ps)):
        F(A.bar(x, p, 40, BRA('.22'), BR), show=.3 + k * .1)
    s = 0; t = 1.4
    for k, (x, p) in enumerate(zip(xs, ps)):
        s += x * p
        F(R(A.px(x) - 24, A.py(p) - 4, 48, A.py(0) - A.py(p) + 8, VIA('.08'), VI, 4, 2), show=t, hide=t + .65, d=.15)
        F(T(A.px(x), A.py(p) - 10, '%d × %.2f' % (x, p), VI, cls='sv-s'), show=t, hide=t + .65, d=.15)
        F(T(540, 112, 'sum = %.2f' % s, VI if k < 6 else FI, 'start', 'sv-s', mono=True), show=t + .2,
          hide=None if k == 6 else t + .75, d=.15)
        t += .75
    F(T(540, 80, 'running sum of x × P(x)', MU, 'start'), show=1.4)
    y0 = A.py(0)
    tri = '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>' % (A.px(mu), y0 + 4, A.px(mu) - 9, y0 + 18, A.px(mu) + 9, y0 + 18, FI)
    F(tri + T(A.px(mu), y0 + 46, 'E[X] = %.2f' % mu, FI, cls='sv-s'), show=t + .2, move=(t + .2, A.px(0) - A.px(mu), 0, 1.4))
    F(L(A.px(1), A.py(.30) - 14, A.px(1), A.py(.30) - 2, MU, 1) + T(A.px(1), A.py(.30) - 18, 'mode = 1', MU), show=t + 2.0)
    F(T(540, 160, 'mean 2.27 is not', MU, 'start') + T(540, 176, 'the most common value', MU, 'start'), show=t + 2.4)
    return F.render()

# ---------- 1.3 variance ----------
def f13():
    rows = [('narrow', [3, 4, 5, 6, 7], [.1, .2, .4, .2, .1]), ('wide', list(range(1, 10)), [.1, .1, .1, .1, .2, .1, .1, .1, .1])]
    F = Fig('pv1-', 720, 318, 'Two distributions with the same mean 5. Narrow: values 3 to 7. Wide: values 1 to 9. For each '
            'bar a line measures its distance from the mean and the squared distance appears above it. Weighted and '
            'summed: variance 1.2 for the narrow one, 6.0 for the wide one; the standard deviation bracket is 1.10 and 2.45 wide.',
            'VARIANCE · AVERAGE SQUARED DISTANCE FROM THE MEAN')
    t = .3
    for r, (nm, xs, ps) in enumerate(rows):
        assert abs(sum(ps) - 1) < 1e-9
        mu = sum(x * p for x, p in zip(xs, ps)); var = sum((x - mu) ** 2 * p for x, p in zip(xs, ps))
        assert abs(mu - 5) < 1e-9
        A = Plot(60, 46 + r * 140, 420, 90, (.4, 9.6), (0, .42))
        F(A.axes([(x, str(x)) for x in range(1, 10)]) + T(10, A.y + 50, nm, MU, 'start', 'sv-s'), show=t)
        for k, (x, p) in enumerate(zip(xs, ps)):
            F(A.bar(x, p, 30, BRA('.22'), BR), show=t + .1 + k * .06)
        F(L(A.px(mu), A.y - 6, A.px(mu), A.py(0), FI, 1.4, '4 3') + (T(A.px(mu) + 6, A.y + 2, 'mean', FI, 'start') if r == 0 else ''), show=t + .8)
        t += 1.4
        for k, (x, p) in enumerate(zip(xs, ps)):
            if x == mu: continue
            yb = A.py(p) - 4
            F(L(A.px(mu), yb, A.px(x), yb, VI, 1.4) + T(A.px(x), yb - 5, '%d' % ((x - mu) ** 2), VI, cls='sv-l'), show=t, d=.2)
            t += .22
        sd = math.sqrt(var)
        yb = A.py(0) + 24
        F(L(A.px(mu - sd), yb, A.px(mu + sd), yb, FI, 2) + L(A.px(mu - sd), yb - 5, A.px(mu - sd), yb + 5, FI, 2) +
          L(A.px(mu + sd), yb - 5, A.px(mu + sd), yb + 5, FI, 2), show=t + .2)
        F(T(510, A.y + 40, 'Var = %.1f' % var, FI, 'start', 'sv-s', mono=True) + T(510, A.y + 60, 'sd = √Var = %.2f' % sd, FI, 'start', 'sv-s', mono=True), show=t + .3)
        t += 1.2
    F(T(510, 66, 'violet = squared distance', VI, 'start'), show=1.7)
    return F.render()

# ---------- 1.4 covariance & correlation ----------
def f14():
    g = LCG(7)
    def pearson(pts):
        n = len(pts); mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
        sxy = sum((x - mx) * (y - my) for x, y in pts); sx = math.sqrt(sum((x - mx) ** 2 for x, _ in pts)); sy = math.sqrt(sum((y - my) ** 2 for _, y in pts))
        return sxy / (sx * sy)
    xs = [-1 + 2 * i / 29 for i in range(30)]
    sets = [('rises together', [(x, .9 * x + .25 * g.n()) for x in xs]),
            ('no link', [(x, .6 * g.n()) for x in xs]),
            ('one up, other down', [(x, -.8 * x + .35 * g.n()) for x in xs]),
            ('U shape', [(x, 1.6 * x * x - .55 + .08 * g.n()) for x in xs])]
    rs = [pearson(p) for _, p in sets]
    assert rs[0] > .85 and abs(rs[1]) < .3 and rs[2] < -.75 and abs(rs[3]) < .15
    F = Fig('pc1-', 720, 270, 'Four scatter plots appear one after another. Rising together: r = %.2f. No link: r = %.2f. '
            'One up, the other down: r = %.2f. A U shape: a strong relationship, yet r = %.2f, because correlation only sees straight lines.'
            % tuple(rs), 'CORRELATION r · HOW WELL A STRAIGHT LINE FITS, FROM −1 TO 1')
    t = .3
    for k, (nm, pts) in enumerate(sets):
        A = Plot(10 + k * 180, 50, 150, 150, (-1.25, 1.25), (-1.6, 1.6))
        F(R(A.x, A.y, A.w, A.h, 'var(--bg)', 'var(--rule)', 4) + T(A.x + A.w / 2, A.y + A.h + 20, nm, MU), show=t)
        for i, (x, y) in enumerate(pts):
            F(C(A.px(x), A.py(max(-1.55, min(1.55, y))), 3, BRA('.55')), show=t + .2 + i * .02, d=.12)
        r = rs[k]; c = RO if k == 3 else FI
        if k < 3:
            F(L(A.px(-1.1), A.py(-1.1 * r), A.px(1.1), A.py(1.1 * r), VI, 1.8), show=t + 1.0)
        else:
            F(P(A.curve(lambda x: 1.6 * x * x - .55, -1.1, 1.1, 40), VI, 1.8, '4 3'), show=t + 1.0)
        F(T(A.x + A.w / 2, A.y + A.h + 42, 'r = %+.2f' % r, c, cls='sv-s', mono=True), show=t + 1.2)
        t += 1.8
    F(T(10 + 3 * 180 + 75, 262, 'linked, but r misses it', RO), show=t)
    return F.render()

# ---------- 2.1 conditional probability ----------
def f21():
    F = Fig('pq1-', 720, 300, 'One hundred shoppers as a 10 by 10 grid. 20 of them buy: P(buy) = 0.20. Then we learn the '
            'shopper added an item to the cart: the 25 cart shoppers are outlined and the other 75 fade to grey. 15 of the 25 '
            'buy, so P(buy given cart) = 15 / 25 = 0.60.', 'CONDITIONING · SHRINK THE WORLD TO WHERE B IS TRUE')
    G = 24; X0, Y0 = 30, 44
    cart = set(range(25))
    buy = set(list(range(15)) + [31, 44, 58, 72, 87])
    assert len(buy) == 20 and len(buy & cart) == 15
    pos = lambda i: (X0 + (i % 10) * G + G / 2, Y0 + (i // 10) * G + G / 2)
    for i in range(100):
        x, y = pos(i)
        F(C(x, y, 8, 'var(--bg)', RULE_HI, 1.2), show=.2 + (i // 10) * .06)
    for k, i in enumerate(sorted(buy)):
        x, y = pos(i)
        F(C(x, y, 8, FI), show=1.2 + k * .05, d=.2)
    RX = 300
    F(T(RX, 70, 'all 100 shoppers', MU, 'start') + T(RX, 92, 'P(buy) = 20 / 100 = 0.20', FI, 'start', 'sv-s', mono=True), show=2.4)
    t = 3.6
    F(T(RX, 132, 'B: added to cart · 25 shoppers', VI, 'start'), show=t)
    F('<path d="M%.1f %.1f H%.1f V%.1f H%.1f V%.1f H%.1f Z" fill="none" stroke="%s" stroke-width="2.2" stroke-linejoin="round"/>' % (
        X0 - 2, Y0 - 2, X0 + 10 * G + 2, Y0 + 2 * G, X0 + 5 * G + 2, Y0 + 3 * G + 2, X0 - 2, VI), show=t)
    for i in range(25, 100):
        x, y = pos(i)
        F(C(x, y, 8, 'var(--sunk)', 'var(--rule)', 1) + (C(x, y, 4, GH) if i in buy else ''), show=t + 1.0 + (i // 10) * .05, d=.25)
    F(T(RX, 172, 'look only inside B', MU, 'start') + T(RX, 194, 'P(buy | cart) = 15 / 25 = 0.60', VI, 'start', 'sv-s', mono=True), show=t + 2.0)
    F(T(RX, 236, 'same shopper, new information: 0.20 → 0.60', FI, 'start'), show=t + 3.0)
    return F.render()

# ---------- 2.2 Bayes ----------
def f22():
    N, prev, sens, fpr = 100000, .001, .99, .05
    sick = round(N * prev); well = N - sick; tp = round(sick * sens); fp = round(well * fpr)
    post = tp / (tp + fp)
    assert (sick, tp, fp) == (100, 99, 4995) and abs(post - .0194) < .001
    F = Fig('pb1-', 720, 330, 'The test is 99 percent accurate on sick people. Of 100,000 people, 100 are sick and 99,900 are well. '
            '99 sick people test positive and so do 4,995 well people (5 percent). The positives line up as one bar: the sick '
            'part is a sliver of 1.9 percent. So P(positive given sick) = 99 percent but P(sick given positive) = 1.9 percent.',
            'BAYES · FLIP THE CONDITION, COUNT THE BASE RATE')
    def box(x, y, w, t1, t2, c, fill):
        return R(x - w / 2, y, w, 40, fill, c, 6, 1.4) + T(x, y + 17, t1, c, cls='sv-s') + T(x, y + 32, t2, MU, cls='sv-l')
    F(box(360, 34, 150, '100,000 people', 'prevalence 1 in 1,000', RULE_HI, 'var(--bg)'), show=.2)
    F(arrow(330, 76, 190, 104, MU) + arrow(390, 76, 530, 104, MU), show=.8)
    F(box(160, 106, 130, '%d sick' % sick, 'base rate 0.1%', FI, FIA('.10')), show=1.0)
    F(box(560, 106, 130, '{:,} well'.format(well), '99.9%', BR, BRA('.10')), show=1.2)
    F(arrow(160, 148, 160, 176, MU) + T(168, 166, '99% test +', MU, 'start', 'sv-l'), show=2.0)
    F(arrow(560, 148, 560, 176, MU) + T(568, 166, '5% test +', MU, 'start', 'sv-l'), show=2.6)
    F(box(160, 178, 130, '%d positive' % tp, 'true positives', FI, FIA('.10')), show=2.2)
    F(box(560, 178, 130, '{:,} positive'.format(fp), 'false positives', RO, ROA('.10')), show=2.8)
    BX, BW, BY = 40, 640, 254
    ws = BW * tp / (tp + fp)
    F(T(BX, BY - 8, 'every positive test, side by side', MU, 'start'), show=3.8)
    F(R(BX, BY, ws, 26, FI, FI, 0, 1), show=4.0, move=(4.0, 160 - BX, 178 - BY, .9))
    F(R(BX + ws, BY, BW - ws, 26, ROA('.22'), RO, 0, 1), show=4.2, move=(4.2, 560 - (BX + ws) - (BW - ws) / 2, 178 - BY, .9))
    F(L(BX + ws / 2, BY + 28, BX + ws / 2, BY + 44, FI, 1, '3 3') + T(BX + 8, BY + 56, 'sick: %d of %s = %.1f%%' % (tp, '{:,}'.format(tp + fp), 100 * post), FI, 'start', 'sv-s'), show=5.4)
    F(T(BX + BW, BY + 56, 'P(positive | sick) = 99%  ·  P(sick | positive) = 1.9%', VI, 'end', 'sv-s'), show=6.4)
    return F.render()

# ---------- 3.1 LLN ----------
def _lln(sd):
    g = LCG(sd); s = 0
    for i in range(400): s += 1 + int(g.u() * 6)
    return abs(s / 400 - 3.5)
SEED = min(range(1, 60), key=_lln)
def f31():
    g = LCG(SEED); n = 400; s = 0; run = []
    for i in range(1, n + 1):
        s += 1 + int(g.u() * 6); run.append(s / i)
    F = Fig('pl1-', 720, 290, 'A die is rolled 400 times. The running average jumps around at first, then the line settles '
            'onto the dashed expectation 3.5. After 400 rolls the average is %.2f.' % run[-1], 'LAW OF LARGE NUMBERS · THE AVERAGE SETTLES ON E[X]')
    A = Plot(60, 46, 560, 190, (0, n), (1, 6))
    F(A.axes([(v, str(v)) for v in (1, 100, 200, 300, 400)], [(v, str(v)) for v in range(1, 7)], 'number of rolls', 'running average'))
    F(L(A.px(0), A.py(3.5), A.px(n), A.py(3.5), FI, 1.4, '5 4') + T(A.px(n) + 8, A.py(3.5) + 4, 'E[X] = 3.5', FI, 'start', 'sv-s'), show=.4)
    pts = [(A.px(i + 1), A.py(v)) for i, v in enumerate(run)]
    early = pts[:12]
    for k in range(1, 12):
        F(P(early[k - 1:k + 1], VI, 2), show=1.0 + k * .18, d=.1)
        F(C(*early[k], 3.2, VI), show=1.0 + k * .18, hide=1.0 + (k + 1) * .18, d=.1)
    F(T(A.px(14), A.py(run[0]) + 4, 'first rolls swing', VI, 'start'), show=1.4, hide=3.4)
    t = draw(F, pts[11:], 3.4, VI, 2.6, 2, k=30)
    F(C(*pts[-1], 4, FI) + T(A.px(n) + 8, A.py(run[-1]) + 20, 'avg = %.2f' % run[-1], FI, 'start', 'sv-s', mono=True), show=t + .2)
    return F.render()

# ---------- 3.2 CLT ----------
def f32():
    vals = [1, 2, 3, 4, 5, 6]; ps = [.40, .25, .15, .10, .06, .04]
    mu = sum(v * p for v, p in zip(vals, ps)); sd = math.sqrt(sum((v - mu) ** 2 * p for v, p in zip(vals, ps)))
    def dist(n):
        d = {0: 1.0}
        for _ in range(n):
            e = {}
            for s, q in d.items():
                for v, p in zip(vals, ps): e[s + v] = e.get(s + v, 0) + q * p
            d = e
        return {s / n: q for s, q in d.items()}
    def hist(n):
        bw = 1 / n if n <= 5 else .1
        h = {}
        for m, q in dist(n).items():
            b = round((m - 1) / bw - (1e-9 if n > 5 else 0)) if n <= 5 else int((m - 1) / bw + 1e-9)
            h[b] = h.get(b, 0) + q
        return h, bw
    F = Fig('pt1-', 720, 300, 'A lopsided source: values 1 to 6, most mass at 1. Average n draws and plot the averages. '
            'n = 1 is the lopsided source itself; n = 2 is still skewed; n = 5 is nearly symmetric; at n = 30 the bars match '
            'a bell curve centred on the mean %.2f and narrower by the square root of n.' % mu, 'CENTRAL LIMIT THEOREM · AVERAGES BECOME A BELL')
    t = .3
    for k, n in enumerate([1, 2, 5, 30]):
        h, BW = hist(n); assert abs(sum(h.values()) - 1) < 1e-9
        top = max(h.values())
        A = Plot(14 + k * 178, 52, 150, 150, (1, 6), (0, top * 1.08))
        F(A.axes([(v, str(v)) for v in (1, 2, 3, 4, 5, 6)]) + T(A.x + A.w / 2, 238, 'n = %d' % n, VI if n == 30 else MU, cls='sv-s'), show=t)
        pw = A.w / 5 * BW
        for b in sorted(h):
            q = h[b]
            if q < 1e-4: continue
            x0 = A.px(1 + b * BW) - (pw / 2 if n <= 5 else 0)
            x0 = max(A.x, x0); x1 = min(A.x + A.w, A.px(1 + b * BW) + (pw / 2 if n <= 5 else pw))
            F(R(x0 + .5, A.py(q), min(x1 - x0 - 1, 22), A.py(0) - A.py(q), BRA('.30'), BR, 1, .8), show=t + .2 + b * .02, d=.2)
        if n >= 5:
            s = sd / math.sqrt(n)
            pts = A.curve(lambda m: npdf(m, mu, s) * BW, 1, 6, 150)
            if n > 5: pts = [(x + pw / 2, y) for x, y in pts]
            pts = [(x, max(y, A.y - 4)) for x, y in pts]
            F(P(pts, FI, 2), show=t + 1.1)
        t += 1.6
    F(L(14 + 3 * 178 + 150 * (mu - 1) / 5, 50, 14 + 3 * 178 + 150 * (mu - 1) / 5, 202, VI, 1.2, '3 3'), show=t)
    F(T(0, 270, 'the source stays lopsided; only the average turns into a bell, with spread σ / √n', MU, 'start'), show=t + .4)
    return F.render()

# ---------- 4.1 MLE ----------
def f41():
    flips = 'HHTHHHTHHT'; h = flips.count('H'); assert h == 7
    Lk = lambda p: p ** 7 * (1 - p) ** 3 * 1000
    F = Fig('pm1-', 720, 296, 'Ten coin flips land 7 heads and 3 tails. The likelihood curve p to the 7 times 1 minus p cubed is '
            'drawn over p from 0 to 1. A probe tries p = 0.3, 0.5, 0.9 and reads the height at each; the highest point is '
            'at p = 0.7, the maximum likelihood estimate.', 'MAXIMUM LIKELIHOOD · PICK THE p THAT MAKES THE DATA MOST LIKELY')
    for i, c in enumerate(flips):
        x = 40 + i * 30
        F(C(x, 52, 11, FIA('.16') if c == 'H' else 'var(--bg)', FI if c == 'H' else RULE_HI, 1.3) + T(x, 56, c, FI if c == 'H' else MU, cls='sv-s', mono=True), show=.2 + i * .1)
    F(T(345, 56, '7 heads · 3 tails', MU, 'start'), show=1.3)
    A = Plot(70, 96, 460, 160, (0, 1), (0, 2.4))
    F(A.axes([(v / 10, '%.1f' % (v / 10)) for v in range(0, 11, 1)], [(1, '1'), (2, '2')], 'p = chance of heads', 'likelihood × 10⁻³'), show=1.4)
    t = draw(F, A.curve(Lk, 0, 1, 160), 1.8, BR, 1.4)
    t += .3; prev = None
    tries = [.3, .5, .9, .7]
    for k, p in enumerate(tries):
        last = k == len(tries) - 1
        c = FI if last else VI
        g = L(A.px(p), A.py(0), A.px(p), A.py(Lk(p)), c, 1.6, None if last else '3 3') + C(A.px(p), A.py(Lk(p)), 5, c)
        F(g, show=t, hide=None if last else t + 1.1, d=.2)
        F(T(570, 166, 'p = %.1f' % p, c, 'start', 'sv-s', mono=True) +
          T(570, 184, 'L = %.2f' % Lk(p), c, 'start', 'sv-s', mono=True), show=t, hide=None if last else t + 1.1, d=.2)
        t += 1.25
    F(T(A.px(.7), A.py(Lk(.7)) - 12, 'p̂ = 7 / 10', FI, cls='sv-s'), show=t)
    assert max(range(101), key=lambda i: Lk(i / 100)) == 70
    return F.render()

# ---------- 4.2 MSE & log loss ----------
def f42():
    F = Fig('pz1-', 720, 330, 'Left: a bell-shaped error density; take minus its log and it becomes the parabola e squared over two — '
            'the squared error. A probe slides from error 0 to 2: density falls, loss rises. Right: for a true label 1, the loss '
            'is minus log p; as the predicted p slides from 0.9 down to 0.1 the loss climbs from 0.11 to 2.30.',
            'NORMAL ERROR → MSE')
    F(T(450, 14, 'BERNOULLI LABEL → LOG LOSS', MU, 'start', 'sv-hv'))
    A1 = Plot(50, 50, 260, 80, (-3, 3), (0, .42))
    A2 = Plot(50, 170, 260, 100, (-3, 3), (0, 4.6))
    F(A1.axes([], [], '', 'error density (Normal)'))
    F(A2.axes([(v, str(v)) for v in (-3, -2, -1, 0, 1, 2, 3)], [(2, '2'), (4, '4')], 'error e = y − ŷ', 'loss = e² / 2'), show=1.8)
    t = draw(F, A1.curve(npdf, -3, 3), .4, BR, 1.0)
    F(arrow(330, 104, 330, 186, VI, 1.4) + T(338, 150, '− log', VI, 'start', 'sv-s'), show=1.6)
    t = draw(F, A2.curve(lambda e: e * e / 2, -3, 3), 2.0, FI, 1.2)
    for k, e in enumerate([0, 1, 2]):
        last = k == 2; tt = t + .3 + k * 1.0
        F(C(A1.px(e), A1.py(npdf(e)), 4.5, VI) + L(A1.px(e), A1.py(npdf(e)), A2.px(e), A2.py(e * e / 2), VI, 1, '3 3') + C(A2.px(e), A2.py(e * e / 2), 4.5, VI),
          show=tt, hide=None if last else tt + .9, d=.2)
    B = Plot(450, 60, 250, 210, (0, 1), (0, 2.6))
    F(B.axes([(v / 10, '%.1f' % (v / 10)) for v in (0, 2, 4, 6, 8, 10)], [(1, '1'), (2, '2')], 'predicted p for the true class', 'loss = −log p'), show=.4)
    t2 = draw(F, B.curve(lambda p: -math.log(p), .075, 1, 120), .8, FI, 1.2)
    for k, p in enumerate([.9, .5, .1]):
        last = k == 2; tt = t + .3 + k * 1.0
        F(C(B.px(p), B.py(-math.log(p)), 5, VI) + T(B.px(p) + (12 if p < .5 else -12), B.py(-math.log(p)) + 1, 'loss %.2f' % -math.log(p), VI, 'start' if p < .5 else 'end', 'sv-l'),
          show=tt, hide=None if last else tt + .9, d=.2)
    F(T(B.px(.55), B.py(1.9), 'confident and wrong', RO, cls='sv-s'), show=t + 2.6)
    F(T(B.px(.55), B.py(1.9) + 14, 'costs the most', RO), show=t + 2.6)
    return F.render()

# ---------- 4.3 MAP ----------
def f43():
    s0 = 1.0; m1 = 2.0
    def post(sl):
        prec = 1 / s0 ** 2 + 1 / sl ** 2; m = (m1 / sl ** 2) / prec; return m, math.sqrt(1 / prec)
    F = Fig('pp1-', 720, 330, 'The weight w on an axis. A prior bell centred at 0 says weights should be small. With little data '
            'the likelihood is a wide bell at 2; the posterior, their product, peaks at %.2f, pulled toward 0. With much more data '
            'the likelihood narrows at 2 and the posterior peak moves to %.2f, close to the data.' % (post(.8)[0], post(.25)[0]),
            'MAP · PRIOR × LIKELIHOOD → POSTERIOR')
    A = Plot(60, 50, 480, 210, (-2.5, 3.5), (0, 1.8))
    F(A.axes([(v, str(v)) for v in range(-2, 4)], [(.5, '0.5'), (1, '1.0'), (1.5, '1.5')], 'weight w', 'density'))
    t = draw(F, A.curve(lambda w: npdf(w, 0, s0), -2.5, 3.5), .4, BR, 1.0, dash='6 4')
    F(T(A.px(-1.6), A.py(.3), 'prior', BR, 'end', 'sv-s'), show=t)
    RX = 570
    F(T(RX, 70, 'prior: weights near 0', BR, 'start'), show=t)
    for k, (sl, lab) in enumerate([(.8, 'little data'), (.25, 'much more data')]):
        last = k == 1; t0 = 1.8 + k * 4.4
        hide = None if last else t0 + 4.0
        F(T(RX, 104, lab, MU, 'start', 'sv-s'), show=t0, hide=hide, d=.2)
        td = draw(F, A.curve(lambda w: npdf(w, m1, sl), -2.5, 3.5), t0, VI, .9, hide=hide)
        F(T(RX, 124, 'likelihood at w = 2', VI, 'start'), show=td, hide=hide, d=.2)
        m, s = post(sl)
        pts = A.curve(lambda w: npdf(w, m, s), -2.5, 3.5)
        F(area(pts, A.py(0), FIA('.18')) + P(pts, FI, 2.2), show=td + .5, hide=hide, d=.3)
        F(L(A.px(m), A.py(npdf(m, m, s)), A.px(m), A.py(0), FI, 1.4, '3 3'), show=td + 1.0, hide=hide, d=.2)
        F(T(RX, 156, 'posterior peak', FI, 'start') + T(RX, 176, 'w = %.2f' % m, FI, 'start', 'sv-s', mono=True), show=td + 1.0, hide=hide, d=.2)
    F(T(0, 316, 'little data: the prior pulls w toward 0 (regularization) · much data: the likelihood wins', MU, 'start'), show=1.8 + 4.4 + 2.6)
    return F.render()

ALL = [f11, f12, f13, f14, f21, f22, f31, f32, f41, f42, f43]
for i, fn in enumerate(ALL, 1):
    figs['FIG%d' % i] = fn()
os.makedirs('/tmp/ml', exist_ok=True)
json.dump(figs, open('/tmp/ml/probability-figs.json', 'w'))
print('ok', len(figs))
