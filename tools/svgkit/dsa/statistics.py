# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/02-math-foundations/statistics.
Run: python3 statistics.py  -> rewrites the lesson body (sections between the hero and the replay script).
Every number in a figure is computed here; asserts pin the ones quoted in the text."""
import os, sys, math, random, zlib, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from engine import Anim, T, R, L, arrow, MU, TX, FA, RULE_HI

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/02-math-foundations/statistics/index.html')
BR, VI, FI, RO, GH = 'var(--brand)', 'var(--violet)', 'var(--filled)', 'var(--rose)', 'var(--ghost)'
RULE = 'var(--rule)'
def ta(tok, a): return 'rgba(var(%s),%s)' % (tok, a)
BRA, VIA, FIA, ROA = (lambda a: ta('--clay-a', a)), (lambda a: ta('--violet-a', a)), (lambda a: ta('--blue-a', a)), (lambda a: ta('--rose-a', a))

def pdf(z, m=0.): return math.exp(-(z - m) ** 2 / 2) / math.sqrt(2 * math.pi)
def Phi(z): return .5 * (1 + math.erf(z / math.sqrt(2)))
def P(d, c, w=2.4, fill='none', dash=None):
    ds = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (d, fill, c, w, ds)
def dot(x, y, c, r=4): return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, c)
def ring(x, y, c, r=7): return '<circle cx="%.1f" cy="%.1f" r="%s" fill="none" stroke="%s" stroke-width="1.8"/>' % (x, y, r, c)
def chip(cx, y, t, c, tint, w=None):
    w = w or 20 + len(t) * 6.3
    return R(cx - w / 2, y, w, 22, 'var(--bg)', 'none', 6) + R(cx - w / 2, y, w, 22, tint, c, 6, 1.3) + T(cx, y + 15, t, c, bold=True)
def sw(x, y, fill, c, t, tc=None):   # legend swatch + text
    return R(x, y - 10, 12, 12, fill, c, 2, 1.2) + T(x + 18, y, t, tc or c, 'start', bold=True)

class Plot:
    def __init__(s, x0, x1, y0, y1, X0, X1, Y0, Y1):
        s.x0, s.x1, s.y0, s.y1, s.X0, s.X1, s.Y0, s.Y1 = x0, x1, y0, y1, X0, X1, Y0, Y1   # y0 = top px, y1 = bottom px
    def px(s, v): return s.x0 + (v - s.X0) / (s.X1 - s.X0) * (s.x1 - s.x0)
    def py(s, v): return s.y1 - (v - s.Y0) / (s.Y1 - s.Y0) * (s.y1 - s.y0)
    def fpath(s, f, a, b, n=160):
        return 'M' + ' L'.join('%.1f %.1f' % (s.px(a + (b - a) * i / n), s.py(f(a + (b - a) * i / n))) for i in range(n + 1))
    def area(s, f, a, b, n=80):
        return s.fpath(f, a, b, n) + ' L%.1f %.1f L%.1f %.1f Z' % (s.px(b), s.py(s.Y0), s.px(a), s.py(s.Y0))
    def xaxis(s, ticks, label=None, fmt=str):
        o = L(s.x0, s.y1, s.x1, s.y1, MU, 1.2)
        for v in ticks:
            o += L(s.px(v), s.y1, s.px(v), s.y1 + 4, MU, 1) + T(s.px(v), s.y1 + 17, fmt(v), FA, mono=True)
        if label: o += T(s.x1 + 8, s.y1 + 4, label, MU, 'start', mono=True)
        return o
    def yaxis(s, ticks, label=None, fmt=str, grid=True):
        o = L(s.x0, s.y1, s.x0, s.y0 - 6, MU, 1.2)
        for v in ticks:
            o += T(s.x0 - 8, s.py(v) + 4, fmt(v), FA, 'end', mono=True)
            if grid: o += L(s.x0, s.py(v), s.x1, s.py(v), RULE, 1, '2 4')
        if label: o += T(s.x0 - 8, s.y0 - 14, label, MU, 'start', mono=True)
        return o

figs = {}

# ---------------- 1.1 p-value ----------------
# timeline: axis .2 · H0 bell 0.6 · observed line slides from 0 to 2.1 (1.6→2.6) · right tail 3.2 ·
# mirror tail 3.9 · tail numbers 4.4 · p sum 5.0 · verdict 5.8
zo = 2.1; tail = 1 - Phi(zo); pval = 2 * tail
assert round(tail, 3) == .018 and round(pval, 3) == .036
f = Anim('pv-', 720, 270, 'Bell curve of the gap between two groups if nothing changed. The observed gap z = 2.1 slides into place; '
         'the area beyond it on both sides is shaded, 0.018 each, so p = 0.036, smaller than 0.05: reject H0.',
         'P-VALUE · HOW RARE IS THIS GAP IF NOTHING CHANGED?', 2.5)
p = Plot(70, 650, 80, 228, -4, 4, 0, .42)
f.show(p.xaxis(range(-3, 4), 'z'), .2)
f.show(P(p.fpath(pdf, -4, 4), BR) + T(p.px(0), 70, 'H₀ · no real difference', BR, bold=True), .6)
f.show(P(p.area(pdf, zo, 4), 'none', 0, VIA('.45')), 3.2)
f.show(P(p.area(pdf, -4, -zo), 'none', 0, VIA('.45')) + L(p.px(-zo), p.y1, p.px(-zo), p.py(pdf(zo)) - 30, VI, 1.3, '4 3'), 3.9)
ln = L(p.px(zo), p.y1, p.px(zo), 66, VI, 2) + chip(p.px(zo), 44, 'observed z = 2.1', VI, VIA('.14'), 128)
f.path(ln, [(0, p.px(0) - p.px(zo), 0), (1.6, 0, 0)], t0=1.2, d=1.0)
f.show(T(p.px(2.95), 214, '0.018', VI, mono=True, bold=True) + T(p.px(-2.95), 214, '0.018', VI, mono=True, bold=True), 4.4)
f.show(T(70, 44, 'p = 0.018 + 0.018 = 0.036', FI, 'start', mono=True, bold=True), 5.0)
f.show(T(70, 64, '0.036 &lt; α = 0.05 → reject H₀', FI, 'start', bold=True), 5.8)
figs['pv'] = f.render()

# ---------------- 1.2 errors ----------------
D = 2.5; zc = 1.96
beta = Phi(zc - D) - Phi(-zc - D); power = 1 - beta
assert round(beta, 2) == .29 and round(power, 2) == .71
f = Anim('er-', 720, 300, 'Two bells: H0 true at 0 and H1 true at 2.5. A cut at 1.96 splits them. The two tails of H0 beyond the cut are '
         'type I errors, alpha 0.05. The part of H1 left of the cut is a type II error, beta 0.29. The rest of H1 is power, 0.71.',
         'TYPE I · TYPE II · POWER — ONE CUT, TWO WORLDS', 2.5)
p = Plot(40, 680, 70, 222, -3.6, 6, 0, .42)
f1 = lambda z: pdf(z, D)
f.show(p.xaxis(range(-3, 7), 'z'), .2)
f.show(P(p.fpath(pdf, -3.6, 6), BR) + T(p.px(0), 60, 'if H₀ is true', BR, bold=True), .6)
f.show(P(p.fpath(f1, -3.6, 6), FI) + T(p.px(D), 60, 'if H₁ is true', FI, bold=True), 1.3)
f.path(L(p.px(zc), p.y1, p.px(zc), 52, VI, 2, '5 3') + T(p.px(zc), 40, 'reject H₀ if |z| > 1.96', VI, bold=True),
       [(0, -40, 0), (2.2, 0, 0)], t0=2.0, d=.7)
f.show(P(p.area(f1, zc, 6), 'none', 0, FIA('.16')), 5.6)
f.show(P(p.area(pdf, zc, 6), 'none', 0, ROA('.55')) + P(p.area(pdf, -3.6, -zc), 'none', 0, ROA('.55')), 3.4)
f.show(P(p.area(f1, -3.6, zc), 'none', 0, VIA('.30')), 4.5)
f.show(sw(40, 270, ROA('.55'), RO, 'type I · false alarm · α = 0.05'), 3.6)
f.show(sw(290, 270, VIA('.30'), VI, 'type II · missed effect · β = 0.29'), 4.7)
f.show(sw(540, 270, FIA('.16'), FI, 'power = 1 − β = 0.71'), 5.8)
figs['er'] = f.render()

# ---------------- 1.3 power vs n ----------------
steps = [(100, 1.0), (400, 2.0), (784, 2.8)]
pw = [1 - Phi(zc - d) + Phi(-zc - d) for _, d in steps]
assert [round(x, 2) for x in pw] == [.17, .52, .80]
for n, d in steps: assert abs(d - math.sqrt(n / 100)) < 1e-9          # shift grows with sqrt(n)
f = Anim('pw-', 720, 290, 'The H1 bell starts at 1.0, close to H0: n = 100 per group, power 0.17. With n = 400 it slides to 2.0, power 0.52. '
         'With n = 784 it reaches 2.8 and 80 percent of it lies beyond the cut: power 0.80.',
         'POWER · MORE SAMPLES PUSH THE TWO BELLS APART', 2.5)
p = Plot(40, 680, 76, 222, -3.6, 6.4, 0, .42)
f.static(p.xaxis(range(-3, 7), 'z'))
f.static(P(p.fpath(pdf, -3.6, 6.4), BR) + T(p.px(-1.6), 120, 'H₀', BR, bold=True))
f.static(L(p.px(zc), p.y1, p.px(zc), 70, VI, 2, '5 3') + T(p.px(zc), 62, 'cut 1.96', VI, bold=True))
dl = 2.8
base = lambda z: pdf(z, dl)
times = [.6, 2.6, 4.6]
for k, ((n, d), pk, t) in enumerate(zip(steps, pw, times)):
    shade = P(p.area(lambda z, d=d: pdf(z, d), zc, 6.4), 'none', 0, FIA('.22'))
    f.show(shade, t + .8, hide=times[k + 1] if k < 2 else None)
    f.show(T(380, 34, 'n = %d per group · shift = %.1f · power = %.2f' % (n, d, pk), FI, 'start', mono=True, bold=True),
           t + .8, hide=times[k + 1] if k < 2 else None, d=.25)
bell = P(p.fpath(base, -3.6 + 0, 6.4), FI) + T(p.px(4.3), 128, 'H₁', FI, 'start', bold=True)
f.path(bell, [(0, p.px(1.0) - p.px(dl), 0), (2.6, p.px(2.0) - p.px(dl), 0), (4.6, 0, 0)], t0=.6, d=.7)
f.static(R(p.x1 + 1, 60, 40, 180, 'var(--sunk)', 'none', 0))           # clip the bell's shifted tail at the plot edge
f.show(T(40, 270, '4× the samples → the bell moves 2× as far · power 0.80 needs n = 784', FI, 'start', bold=True), 6.0)
figs['pw'] = f.render()

# ---------------- 1.4 confidence interval ----------------
MU0, SIG, NS = 50., 10., 25; SE = SIG / math.sqrt(NS); HW = 1.96 * SE
for seed in range(200):
    rnd = random.Random(seed)
    means = [sum(rnd.gauss(MU0, SIG) for _ in range(NS)) / NS for _ in range(20)]
    miss = [abs(m - MU0) > HW for m in means]
    if sum(miss) == 1 and 4 < miss.index(True) < 16: break
assert sum(miss) == 1
f = Anim('ci-', 720, 330, 'Twenty samples of 25 people each, each giving a 95 percent interval around its own mean. Nineteen cross the true '
         'mean 50; one misses it. 95 percent describes the method, not any single interval.',
         'CONFIDENCE INTERVAL · 20 SAMPLES, 20 INTERVALS', 2.5)
p = Plot(80, 600, 64, 276, 42, 58, 0, 20)
f.static(p.xaxis(range(42, 59, 2), 'value'))
f.static(L(p.px(MU0), 50, p.px(MU0), p.y1, FI, 2) + T(p.px(MU0), 42, 'true mean μ = 50', FI, bold=True))
for i, m in enumerate(means):
    y = 68 + i * 10.4; c = RO if miss[i] else BR
    t = .5 + i * .22
    f.show(L(p.px(m - HW), y, p.px(m + HW), y, c, 2.2) + L(p.px(m - HW), y - 3, p.px(m - HW), y + 3, c, 1.5) +
           L(p.px(m + HW), y - 3, p.px(m + HW), y + 3, c, 1.5) + dot(p.px(m), y, c, 3), t, d=.2)
    if miss[i]:
        f.show(T(p.px(m + HW) + 10, y + 4, 'misses μ', RO, 'start', bold=True), t + .3)
f.show(T(80, 318, '19 of 20 cover μ · each interval = mean ± 1.96 × 10/√25 = mean ± 3.9', FI, 'start', bold=True), 5.4)
figs['ci'] = f.render()

# ---------------- 1.5 multiple comparisons ----------------
for seed in range(500):
    rnd = random.Random(seed)
    ps = [rnd.random() for _ in range(20)]
    hits = [i for i, v in enumerate(ps) if v < .05]
    if len(hits) == 1 and 6 < hits[0] < 18 and min(v for v in ps if v >= .05) > .08: break
assert len(hits) == 1
fw = lambda m: 1 - .95 ** m
assert round(fw(20), 2) == .64
f = Anim('mc-', 720, 316, 'Twenty metrics where nothing changed. Their p-values appear one by one; metric 9 dips under 0.05, a false win. '
         'A curve then shows the chance of at least one false win: 64 percent at 20 metrics. Testing each at 0.05 / 20 keeps it near 5 percent.',
         'MULTIPLE COMPARISONS · 20 METRICS, NOTHING REAL', 2.5)
f.static(T(0, 44, 'metric · p-value', MU, 'start'))
CW_, CH_ = 58, 40
for i, v in enumerate(ps):
    x, y = (i % 4) * (CW_ + 6), 56 + (i // 4) * (CH_ + 6)
    t = .4 + i * .18
    f.static(R(x, y, CW_, CH_, 'var(--bg)', RULE_HI, 5, 1) + T(x + 8, y + 14, 'm%d' % (i + 1), FA, 'start', mono=True))
    hit = i in hits
    f.show((R(x, y, CW_, CH_, VIA('.16'), VI, 5, 1.6) if hit else '') +
           T(x + CW_ / 2, y + 31, '%.2f' % v, VI if hit else TX, mono=True, bold=hit), t, d=.2)
hx, hy = (hits[0] % 4) * (CW_ + 6), 56 + (hits[0] // 4) * (CH_ + 6)
p = Plot(330, 660, 60, 240, 0, 40, 0, 1)
t0 = 4.6
f.show(T(0, 304, 'm%d: p = %.2f &lt; 0.05 → a false win' % (hits[0] + 1, ps[hits[0]]), VI, 'start', bold=True), 4.2)
f.show(p.xaxis(range(0, 41, 10), 'metrics') + p.yaxis([.25, .5, .75, 1], 'P(≥ 1 false win)', lambda v: '%d%%' % (v * 100)), t0)
f.show(P(p.fpath(fw, 0, 40), BR), t0 + .6, d=.8)
f.show(L(p.px(20), p.y1, p.px(20), p.py(fw(20)), VI, 1.3, '3 3') + dot(p.px(20), p.py(fw(20)), VI, 5) +
       T(p.px(20) + 10, p.py(fw(20)) + 18, '20 metrics → 64%', VI, 'start', bold=True), t0 + 1.6)
bon = lambda m: 1 - (1 - .05 / max(m, 1)) ** max(m, 1)
f.show(P(p.fpath(bon, 1, 40), FI, 2.4) + T(p.px(40), p.py(bon(40)) - 10, 'test at 0.05 / m → stays near 5%', FI, 'end', bold=True), t0 + 2.6)
figs['mc'] = f.render()

# ---------------- 2.1 confounder ----------------
def corr(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    return sab / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
def fit(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    k = sum((x - ma) * (y - mb) for x, y in zip(a, b)) / sum((x - ma) ** 2 for x in a)
    return k, mb - k * ma
def mk(seed):
    rnd = random.Random(seed); out = []
    for i in range(30):
        temp = (12, 20, 28)[i // 10] + rnd.uniform(-1.5, 1.5)
        out.append((temp, 4 * temp + rnd.gauss(0, 8), 0.5 * temp + rnd.gauss(0, 1.6)))
    return out
for seed in range(500):
    pts = mk(seed)
    r_all = corr([q[1] for q in pts], [q[2] for q in pts])
    bands = [pts[0:10], pts[10:20], pts[20:30]]
    r_band = [corr([q[1] for q in b], [q[2] for q in b]) for b in bands]
    if r_all > .7 and all(abs(r) < .25 for r in r_band): break
assert r_all > .7 and all(abs(r) < .25 for r in r_band), (r_all, r_band)
f = Anim('cf-', 720, 310, 'Thirty days: ice-cream sales against drownings rise together, r = %.2f. Colouring each day by temperature shows the '
         'pattern comes from heat: inside one temperature band the link nearly vanishes. Temperature drives both.' % r_all,
         'CORRELATION · A HIDDEN THIRD VARIABLE DRIVES BOTH', 2.5)
p = Plot(60, 420, 50, 260, 0, 140, 0, 22)
f.static(p.xaxis(range(0, 141, 35), 'ice cream') + p.yaxis([5, 10, 15, 20], 'drownings', grid=False))
for i, (tp, ic, dr) in enumerate(pts):
    f.show(dot(p.px(ic), p.py(dr), BR, 4), .3 + i * .05, hide=3.2, d=.2)
k, b0 = fit([q[1] for q in pts], [q[2] for q in pts])
f.show(L(p.px(10), p.py(k * 10 + b0), p.px(130), p.py(k * 130 + b0), BR, 2, '6 4') +
       T(p.px(130), p.py(k * 130 + b0) - 10, 'r = %.2f' % r_all, BR, 'end', bold=True), 2.0, hide=3.2)
BC = [(GH, 'cool'), (BR, 'mild'), (VI, 'hot')]
for j, (bd, (c, nm)) in enumerate(zip(bands, BC)):
    t = 3.2 + j * .7
    for tp, ic, dr in bd: f.show(dot(p.px(ic), p.py(dr), c, 4.2), t, d=.25)
    kk, bb = fit([q[1] for q in bd], [q[2] for q in bd])
    lo, hi = min(q[1] for q in bd), max(q[1] for q in bd)
    f.show(L(p.px(lo), p.py(kk * lo + bb), p.px(hi), p.py(kk * hi + bb), c, 2.4), t + 2.4)
    f.show(sw(500, 236 + j * 22, {GH: GH, BR: BRA('.55'), VI: VIA('.6')}[c], c, '%s days · r = %.2f' % (nm, r_band[j]), c if c != GH else MU), t + 2.4)
# causal diagram
def node(cx, cy, t, c, tint):
    w = 20 + len(t) * 6.6
    return R(cx - w / 2, cy - 14, w, 28, tint, c, 6, 1.4) + T(cx, cy + 4, t, c, bold=True)
NX = 580
f.show(node(NX, 70, 'temperature', VI, VIA('.14')), 5.6)
f.show(node(490, 160, 'ice cream', BR, BRA('.12')) + node(668, 160, 'drownings', BR, BRA('.12')), 5.6)
f.show(arrow(NX - 20, 86, 505, 144, VI, 1.6) + arrow(NX + 20, 86, 652, 144, VI, 1.6), 6.2)
f.show(L(530, 160, 621, 160, GH, 1.4, '4 3') + T(575, 188, 'no arrow here', MU, bold=True), 6.8)
figs['cf'] = f.render()

# ---------------- 2.2 randomization ----------------
heavy = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0]       # 6 heavy users of 16
assert sum(heavy) == 6
selfB = [i for i in range(16) if (heavy[i] and i != 9) or i in (2,)]   # opt-in: 5 heavy + 1 light → B
rnd = random.Random(3)
for seed in range(400):
    rnd = random.Random(seed); coin = [rnd.random() < .5 for _ in range(16)]
    if sum(coin) == 8 and sum(h for h, c in zip(heavy, coin) if c) == 3: break
assert sum(coin) == 8
f = Anim('rz-', 720, 300, 'Sixteen users, six of them heavy users. Left: users choose; heavy users opt in, so group B holds 5 of the 6 heavy users '
         'and B looks better for a reason that is not the feature. Right: a coin assigns each user; both groups get 3 heavy users.',
         'RANDOMIZATION · BALANCES EVEN WHAT YOU DID NOT MEASURE', 2.5)
f.h = 256
def panel(X, title, toB, t0, cap_):
    f.static(T(X, 44, title, MU, 'start', 'sv-s'))
    f.static(R(X, 100, 150, 92, 'var(--bg)', RULE_HI, 6) + T(X + 75, 116, 'A · old', MU) +
             R(X + 170, 100, 150, 92, 'var(--bg)', RULE_HI, 6) + T(X + 245, 116, 'B · new', MU))
    ia = ib = 0
    for i in range(16):
        sx, sy = X + 10 + i * 19.5, 70
        if i in toB: dx, dy = X + 170 + 18 + (ib % 6) * 23, 138 + (ib // 6) * 26; ib += 1
        else: dx, dy = X + 18 + (ia % 6) * 23, 138 + (ia // 6) * 26; ia += 1
        c = FI if heavy[i] else BRA('.35')
        circ = '<circle cx="%.1f" cy="%.1f" r="8" fill="%s" stroke="%s" stroke-width="1.2"/>' % (dx, dy, c, FI if heavy[i] else BR)
        f.path(circ, [(0, sx - dx, sy - dy), (t0 + i * .08, 0, 0)], t0=.3, d=.8)
    hA = sum(heavy[i] for i in range(16) if i not in toB); hB = sum(heavy[i] for i in toB)
    f.show(T(X + 75, 214, 'heavy: %d of %d' % (hA, 16 - len(toB)), FI, bold=True) +
           T(X + 245, 214, 'heavy: %d of %d' % (hB, len(toB)), FI, bold=True), t0 + 1.9)
    f.show(T(X + 160, 238, cap_[0], cap_[1], bold=True), t0 + 2.4)
    return hA, hB
assert panel(0, 'users choose (opt in)', selfB, 1.2, ('B wins — but B had the heavy users', RO)) == (1, 5)
f.static(L(355, 34, 355, 244, RULE, 1))
assert panel(380, 'coin flip per user', [i for i in range(16) if coin[i]], 4.6, ('same mix → any gap is the feature', FI)) == (3, 3)
f.static(sw(176, 44, FI, FI, 'heavy user', MU) + sw(554, 44, BRA('.35'), BR, 'light user', MU))
figs['rz'] = f.render()

# ---------------- 3.1 design / assignment ----------------
EXP = 'exp2'
names = ['alice', 'bob', 'carol', 'dan', 'erin', 'frank']
hv = [zlib.crc32(('%s:%s' % (n, EXP)).encode()) % 100 for n in names]
assert sum(h < 50 for h in hv) == 3, hv
f = Anim('ab-', 720, 300, 'Six users. Each user id is hashed together with the experiment id into a number from 0 to 99; below 50 goes to A, '
         'otherwise B. The same user gets the same number on every visit, so they always see the same version.',
         'ASSIGNMENT · hash(user_id, experiment_id) % 100', 2.5)
from tablefig import Table
tb = Table(0, 30, [('user_id', 92), ('hash % 100', 96), ('group', 70)])
f.static(tb.head())
for i, n in enumerate(names): f.show(tb.row(i, [n, '', '']), .2 + i * .1)
AX, BX = 380, 560
f.static(R(AX, 60, 150, 170, 'var(--bg)', RULE_HI, 8) + T(AX + 75, 80, 'A · old page', MU, bold=True) +
         R(BX, 60, 150, 170, 'var(--bg)', RULE_HI, 8) + T(BX + 75, 80, 'B · new page', MU, bold=True))
ca = cb = 0
for i, (n, h) in enumerate(zip(names, hv)):
    t = 1.2 + i * .75; y = tb.ry(i)
    f.show(R(tb.colx(1) + 2, y - 1, 92, tb.rh + 2, 'none', VI, 4, 1.6), t, hide=t + .7, d=.15)
    f.show(T(tb.cx(1), y + 17, str(h), VI, mono=True, bold=True), t)
    g = 'A' if h < 50 else 'B'
    f.show(T(tb.cx(2), y + 17, g, FI, mono=True, bold=True), t + .35)
    if g == 'A': dx, dy = AX + 75, 100 + ca * 34; ca += 1
    else: dx, dy = BX + 75, 100 + cb * 34; cb += 1
    c = chip(dx, dy, n, BR, BRA('.12'), 80)
    f.path(c, [(0, tb.cx(0) - dx, y + 2 - dy), (t + .45, 0, 0)], t0=t + .35, d=.5)
f.show(T(0, 270, 'below 50 → A · 50 or more → B · same user → same group on every visit', FI, 'start', bold=True), 6.2)
f.show(T(0, 290, 'a new experiment id reshuffles everyone', MU, 'start'), 6.7)
figs['ab'] = f.render()

# ---------------- 3.2 peeking ----------------
DAYS = 28
def run(r):
    s, out = 0., []
    for d in range(1, DAYS + 1):
        s += r.gauss(0, 1); z = s / math.sqrt(d); out.append(2 * (1 - Phi(abs(z))))
    return out
for seed in range(3000):
    path = run(random.Random(seed))
    first = next((d for d, v in enumerate(path) if v < .05), None)
    if first is not None and 5 <= first <= 10 and path[-1] > .4 and sum(v < .05 for v in path) <= 3: break
sim = random.Random(12345); NRUN = 20000
fp_daily = sum(any(v < .05 for v in run(sim)) for _ in range(NRUN)) / NRUN
fp_end = .05
assert .15 < fp_daily < .35, fp_daily
FPD = round(fp_daily * 100)
f = Anim('pk-', 720, 300, 'An A/A test: both groups get the same page. The p-value is recomputed every day for 28 days. On day %d it dips under '
         '0.05; stopping there declares a fake win. By day 28 it is %.2f. Checking daily makes about %d percent of A/A tests look like wins.'
         % (first + 1, path[-1], FPD), 'PEEKING · AN A/A TEST CHECKED EVERY DAY', 2.5)
p = Plot(70, 620, 56, 236, 1, DAYS, 0, 1)
f.static(p.xaxis([1, 7, 14, 21, 28], 'day') + p.yaxis([.25, .5, .75, 1], 'p-value', lambda v: '%.2f' % v))
f.static(L(p.x0, p.py(.05), p.x1, p.py(.05), VI, 1.4, '5 3') + T(p.x1 + 8, p.py(.05) + 4, 'α = 0.05', VI, 'start', bold=True))
for d in range(1, DAYS):
    t = .4 + d * .16
    f.show(L(p.px(d), p.py(path[d - 1]), p.px(d + 1), p.py(path[d]), BR, 2.2) + dot(p.px(d + 1), p.py(path[d]), BR, 2.6), t, d=.15)
f.show(dot(p.px(1), p.py(path[0]), BR, 2.6), .4)
tf = .4 + first * .16 + .2
f.show(ring(p.px(first + 1), p.py(path[first]), RO, 8), tf)
f.show(T(p.px(first + 1) + 14, p.py(path[first]) - 62, 'day %d: p = %.3f → "B wins!" (fake)' % (first + 1, path[first]), RO, 'start', bold=True), tf + .1)
tl = .4 + DAYS * .16 + .3
f.show(ring(p.px(DAYS), p.py(path[-1]), FI, 8) + T(p.px(DAYS) - 12, p.py(path[-1]) - 14, 'day 28: p = %.2f' % path[-1], FI, 'end', bold=True), tl)
f.show(T(70, 290, 'checked once at day 28 → 5%% false wins · checked every day → %d%%' % FPD, FI, 'start', bold=True), tl + .9)
figs['pk'] = f.render()

# ---------------- 3.3 practical vs statistical ----------------
rows = [('n = 2,000,000', .2, .1), ('n = 40,000', 3.2, .8), ('n = 1,500', 3.2, 4.0)]
def pv_of(m, hw): z = m / (hw / 1.96); return 2 * (1 - Phi(abs(z)))
pvs = [pv_of(m, h) for _, m, h in rows]
assert pvs[0] < .001 and pvs[1] < .001 and .1 < pvs[2] < .13
SHIP = 1.0
f = Anim('ps-', 720, 270, 'Three tests with the ship threshold at +1 percent. Huge sample: +0.2 percent, p below 0.001 but under the threshold, '
         'do not ship. Medium: +3.2 percent plus or minus 0.8, fully above the threshold, ship. Small: +3.2 percent plus or minus 4, crosses zero, unknown.',
         'SIGNIFICANT ≠ WORTH SHIPPING · EFFECT WITH ITS 95% INTERVAL', 2.5)
p = Plot(150, 520, 60, 210, -2, 8, 0, 1)
f.static(p.xaxis(range(-2, 9, 2), 'lift %', lambda v: ('+%d' % v) if v > 0 else str(v)))
f.static(L(p.px(0), 52, p.px(0), p.y1, MU, 1.3) + T(p.px(0), 44, 'no effect', MU))
f.show(L(p.px(SHIP), 52, p.px(SHIP), p.y1, FI, 1.8, '5 3') + T(p.px(SHIP) + 6, 44, 'worth shipping: +1%', FI, 'start', bold=True), .4)
verd = [('p &lt; 0.001 · too small → skip', RO), ('p &lt; 0.001 · clears +1% → ship', FI), ('p = %.2f · crosses 0 → unknown' % pvs[2], MU)]
for i, ((lab, m, hw), (vt, vc)) in enumerate(zip(rows, verd)):
    y = 92 + i * 42; t = 1.2 + i * 1.7
    f.show(T(0, y + 4, lab, TX, 'start', mono=True), t)
    f.show(dot(p.px(m), y, VI, 4.5), t + .2)
    seg = lambda c: L(p.px(m - hw), y, p.px(m + hw), y, c, 2.6) + L(p.px(m - hw), y - 6, p.px(m - hw), y + 6, c, 1.6) + L(p.px(m + hw), y - 6, p.px(m + hw), y + 6, c, 1.6)
    f.show(seg(VI), t + .5, hide=t + 1.2)
    f.show(seg(vc if vc != MU else GH) + dot(p.px(m), y, vc if vc != MU else GH, 4.5), t + 1.2)
    f.show(T(536, y + 4, vt, vc, 'start', bold=True), t + 1.3)
f.show(T(0, 258, 'ask in order: is it different (p) → by how much (interval) → is it worth it (threshold)', FI, 'start', bold=True), 6.8)
figs['ps'] = f.render()

# ---------------- page body ----------------
def eq(*lines):
    o = '  <div class="eq">\n'
    for ln in lines:
        o += '    <div class="line">\n' + ''.join('      %s\n' % part for part in ln) + '    </div>\n'
    return o + '  </div>\n'
def t_(body, note=None, cls=''):
    return '<span class="t%s"><span>%s</span>%s</span>' % (' ' + cls if cls else '', body, '<em>%s</em>' % note if note else '')
OP = lambda s: '<span class="op">%s</span>' % s
FR = lambda a, b: '<span class="frac"><i>%s</i><i>%s</i></span>' % (a, b)
M = lambda s: '<span class="mth">%s</span>' % s

def sub(sid, num, title, skey, fig, bullets=None, eqhtml=''):
    o = '  <div class="subsec" id="%s">\n    <h3 class="ssh"><b>%s</b>%s</h3>\n    <p class="skey">%s</p>\n' % (sid, num, title, skey)
    o += fig + '\n' + eqhtml
    if bullets: o += '    <ul class="why">\n' + ''.join('      <li>%s</li>\n' % b for b in bullets) + '    </ul>\n'
    return o + '  </div>\n'
def sec(n, title, key, body):
    return ('<section id="stats-s%d" class="lesson">\n  <div class="sh"><b>%02d</b><h2>%s</h2></div>\n  <p class="key">%s</p>\n%s</section>\n\n'
            % (n, n, title, key, body))

body = sec(1, 'Testing', 'Assume nothing changed, then ask whether the data is <em>too rare to believe</em>.',
    sub('stats-s1-1', '1.1', 'P-value',
        'The p-value is the share of the “nothing changed” curve that lies at or beyond what you observed.',
        figs['pv'], [
        'It is ' + M('<var>P</var>(data | <var>H</var><sub>0</sub>)') + ', <b>not</b> ' + M('<var>P</var>(<var>H</var><sub>0</sub> | data)') +
        ' — turning one into the other needs <a href="../probability/index.html">Bayes</a> and a base rate.',
        'A large p means <b>failed to reject</b>, not “no difference”.',
        'It says nothing about size: with enough data a 0.01% gap still gives p &lt; 0.05.'],
        eq([t_('<var>z</var>'), OP('='), t_(FR('<var>x̄</var><sub>B</sub> − <var>x̄</var><sub>A</sub>', 'SE'), 'gap in standard errors', 'b')],
           [t_('<var>p</var>'), OP('='), t_('<var>P</var>(|<var>Z</var>| ≥ |<var>z</var>| <span class="op">|</span> <var>H</var><sub>0</sub>)', 'area beyond the observed gap, both tails', 'b')])) +
    sub('stats-s1-2', '1.2', 'Type I and type II errors',
        'One cut splits two worlds: the cut decides how often you cry wolf and how often you miss a wolf.',
        figs['er'], [
        'Type I = false positive, rate ' + M('<var>α</var>') + '; type II = false negative, rate ' + M('<var>β</var>') + '.',
        'Moving the cut right trades fewer false alarms for more misses.',
        'Convention: ' + M('<var>α</var> = 0.05') + ', power ' + M('1 − <var>β</var> = 0.80') + '.']) +
    sub('stats-s1-3', '1.3', 'Power and sample size',
        'More samples shrink the noise, so a real effect sits further from zero and is easier to catch.',
        figs['pw'], [
        'Fix ' + M('<var>α</var>') + ', power and the <b>minimum detectable effect</b> (MDE); the sample size follows.',
        'Halve the MDE and you need <b>four times</b> the sample.',
        'Compute it <b>before</b> the test; if the answer is months, the test is not worth running.'],
        eq([t_('<var>n</var>'), OP('≈'), t_(FR('2 (<var>z</var><sub>1−α/2</sub> + <var>z</var><sub>1−β</sub>)<sup>2</sup> <var>σ</var><sup>2</sup>', 'MDE<sup>2</sup>'),
                                                     'per group: 1.96 and 0.84 for α = 0.05, power 0.80', 'b')])) +
    sub('stats-s1-4', '1.4', 'Confidence interval',
        'A 95% interval comes from a method that covers the true value in 95% of repeated samples.',
        figs['ci'], [
        'The true value is fixed; the <b>interval</b> is what moves from sample to sample.',
        'Its width shrinks with ' + M('√<var>n</var>') + ': four times the data, half the width.',
        'Report the effect <b>with</b> its interval — a p-value only says “different from 0”.'],
        eq([t_('CI'), OP('='), t_('<var>x̄</var>', 'sample mean'), OP('±'), t_('1.96', '95% of a normal'), OP('·'),
            t_(FR('<var>σ</var>', '√<var>n</var>'), 'standard error', 'b')])) +
    sub('stats-s1-5', '1.5', 'Multiple comparisons',
        'Test enough metrics and one will look significant by luck alone.',
        figs['mc'], [
        '20 metrics at ' + M('<var>α</var> = 0.05') + ' give a 64% chance of at least one false win.',
        '<b>Bonferroni</b> tests each at ' + M('<var>α</var> / <var>m</var>') + ' — simple, conservative; Holm is a strictly better variant, BH controls the false discovery rate.',
        'Cheapest fix: fix <b>one primary metric</b> before the test starts.'],
        eq([t_('<var>P</var>(≥ 1 false win)'), OP('='), t_('1 − (1 − <var>α</var>)<sup><var>m</var></sup>', '<var>m</var> independent tests', 'b')],
           [t_('<var>α</var><sub>each</sub>'), OP('='), t_(FR('<var>α</var>', '<var>m</var>'), 'Bonferroni correction')]))
)
body += sec(2, 'Correlation vs causation', 'Two things moving together <em>does not mean</em> one causes the other.',
    sub('stats-s2-1', '2.1', 'Confounder',
        'A hidden third variable can drive both, and the link vanishes once you hold it fixed.',
        figs['cf'], [
        'Other look-alikes: <b>reverse causation</b> (B causes A), <b>selection bias</b>, <b>survivorship bias</b>.',
        'All of them produce the same correlation as a true cause.',
        'Correlation ' + M('<var>r</var>') + ' measures only a linear link, from −1 to 1.']) +
    sub('stats-s2-2', '2.2', 'Randomization',
        'A coin decides who gets the change, so every hidden trait splits evenly between the groups.',
        figs['rz'], [
        'Randomization balances even variables you never measured — no other method can.',
        'When you cannot randomize: difference-in-differences, instrumental variables, regression discontinuity — each adds assumptions you cannot test.'])
)
body += sec(3, 'A/B testing', 'A randomized experiment on live users: <em>split, wait, decide</em>.',
    sub('stats-s3-1', '3.1', 'Experiment design',
        'Hash each user into a group, fix the primary metric and the sample size before the first visitor.',
        figs['ab'], [
        'Split by <b>user</b>, not by visit; include the experiment id in the hash so groups reshuffle per experiment.',
        'One <b>primary metric</b>; the rest are <b>guardrails</b> that only must not get worse.',
        'Run at least one full week — weekend behaviour differs.']) +
    sub('stats-s3-2', '3.2', 'Peeking',
        'Stopping the first time p dips under 0.05 turns noise into wins.',
        figs['pk'], [
        'Early on the gap swings widely, so it almost always crosses the line at some point.',
        'Fix the sample size and look once — or use a method built for looking: <b>sequential testing</b> or Bayesian A/B.']) +
    sub('stats-s3-3', '3.3', 'Statistical vs practical significance',
        'Small p answers “is it different”; only the interval against a threshold answers “is it worth it”.',
        figs['ps'], [
        'Big samples make tiny effects significant.',
        'Set the ship threshold <b>before</b> seeing the result.'])
)

s = open(PAGE).read()
a = s.index('<section id="stats-s1"'); b = s.index('<script>\n/* Figures start')
s = s[:a] + body + s[b:]
s = re.sub(r'<article class="doc"[^>]*>', '<article class="doc" data-progress="1" id="art-stats" data-title="Statistics" data-tag="Math" '
           'data-blurb="Read a p-value, size a test, trust an interval, and run an A/B test without fooling yourself." data-reviewed="2">', s, 1)
open(PAGE, 'w').write(s)
print('ok', len(figs), 'figs', 'fp_daily=%.3f' % fp_daily, 'first=%d end=%.2f' % (first + 1, path[-1]))
