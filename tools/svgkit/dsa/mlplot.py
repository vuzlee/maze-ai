# -*- coding: utf-8 -*-
"""Small plotting helpers shared by the ML overview generators (ml_overview, math_foundations_overview,
core_concepts_overview). Written with the old semantic names, then palette() swaps them to the
analogous blue-violet family: BL -> --brand (data), AM -> --violet (now), GR -> --filled (result),
RD -> --rose (wrong)."""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from engine import *  # noqa  (Anim, T, R, L, arrow, pill, tint, cap, COL, AM, GR, RD, BL, MU, TX, FA, RULE_HI)

GH = 'var(--ghost)'

def palette(s):
    for a, b in [('--filled)', '@B)'), ('--blue-a)', '@BA)'), ('--ok)', '--filled)'), ('--green-a)', '--blue-a)'),
                 ('--tomb)', '--rose)'), ('--red-a)', '--rose-a)'), ('--probe)', '--violet)'), ('--amber-a)', '--violet-a)'),
                 ('@B)', '--brand)'), ('@BA)', '--clay-a)')]:
        s = s.replace(a, b)
    return s

def dot(x, y, r=4.5, tone='bl', hollow=False):
    c = COL[tone] if tone else MU
    f = 'var(--bg)' if hollow else (tint(tone, '.55') if tone else 'var(--bg)')
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1.4"/>' % (x, y, r, f, c)

def ringc(x, y, r=8, c=RD, sw=1.6):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (x, y, r, c, sw)

def poly(pts, c=BL, sw=2.2, dash=None, fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<path d="M%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"%s/>' % (
        ' L'.join('%.1f %.1f' % p for p in pts), fill, c, sw, d)

class Plot:
    """Axes box: data (x0..x1, y0..y1) -> pixels (px, py, pw, ph); origin bottom-left."""
    def __init__(s, px, py, pw, ph, x0, x1, y0, y1):
        s.px, s.py, s.pw, s.ph, s.x0, s.x1, s.y0, s.y1 = px, py, pw, ph, x0, x1, y0, y1
    def X(s, x): return s.px + (x - s.x0) / (s.x1 - s.x0) * s.pw
    def Y(s, y): return s.py + s.ph - (y - s.y0) / (s.y1 - s.y0) * s.ph
    def P(s, x, y): return (s.X(x), s.Y(y))
    def axes(s, xl='', yl='', xt=(), yt=(), grid=True):
        o = L(s.px, s.py + s.ph, s.px + s.pw, s.py + s.ph, MU, 1.2) + L(s.px, s.py + s.ph, s.px, s.py - 4, MU, 1.2)
        for v, lab in xt:
            o += L(s.X(v), s.py + s.ph, s.X(v), s.py + s.ph + 4, MU, 1) + T(s.X(v), s.py + s.ph + 16, lab, FA, mono=True)
        for v, lab in yt:
            o += T(s.px - 7, s.Y(v) + 4, lab, FA, 'end', mono=True)
            if grid: o += L(s.px, s.Y(v), s.px + s.pw, s.Y(v), 'var(--rule)', 1, '2 4')
        if xl: o += T(s.px + s.pw, s.py + s.ph + 32, xl, MU, 'end')
        if yl: o += T(s.px - 4, s.py - 10, yl, MU, 'start')
        return o
    def curve(s, f, a, b, n=120, c=BL, sw=2.2, dash=None, clip=None):
        pts = []
        for i in range(n + 1):
            x = a + (b - a) * i / n; y = f(x)
            if clip: y = max(min(y, clip[1]), clip[0])
            pts.append(s.P(x, y))
        return poly(pts, c, sw, dash)

def solve(A, b):
    """Gaussian elimination with partial pivoting (no numpy here)."""
    n = len(A); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[c][c]:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * b_ for a, b_ in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]

def polyfit(xs, ys, deg, lam=1e-9):
    k = deg + 1
    A = [[sum(x ** (i + j) for x in xs) + (lam if i == j else 0) for j in range(k)] for i in range(k)]
    b = [sum(y * x ** i for x, y in zip(xs, ys)) for i in range(k)]
    return solve(A, b)

def peval(c, x): return sum(ci * x ** i for i, ci in enumerate(c))

def splice(page, article):
    s = open(page, encoding='utf-8').read()
    s = re.sub(r'<article .*?</article>', lambda m: article, s, flags=re.S)
    open(page, 'w', encoding='utf-8').write(s)

def replay():
    s = open(os.path.join(HERE, '../../../content/01-dsa/04-algorithms/binary-search/index.html'), encoding='utf-8').read()
    return re.search(r'<script>\n/\* Figures start.*?</script>', s, re.S).group(0)

# ---------- tiny models (pure python; numbers in figures come from here) ----------
def sig(z): return 1 / (1 + math.exp(-max(min(z, 40), -40)))

def logreg_path(P, y, w, lr=.05, steps=400):
    """Full-batch logistic GD on 2-D points; returns the parameter history [(w1,w2,b), ...]."""
    w = list(w); hist = [tuple(w)]
    for _ in range(steps):
        g = [0, 0, 0]
        for (a, b_), t in zip(P, y):
            e = sig(w[0] * a + w[1] * b_ + w[2]) - t
            g[0] += e * a; g[1] += e * b_; g[2] += e
        w = [wi - lr * gi / len(P) for wi, gi in zip(w, g)]
        hist.append(tuple(w))
    return hist

def gini(ys):
    if not ys: return 0
    p = sum(ys) / len(ys); return 2 * p * (1 - p)

def tree(P, y, depth, lo=(0, 0), hi=(10, 10), out=None):
    """Greedy CART. Returns the list of splits in build order: (axis, thr, lo, hi) and a predict fn."""
    out = [] if out is None else out
    def build(idx, d, lo, hi):
        ys = [y[i] for i in idx]
        leaf = 1 if sum(ys) * 2 > len(ys) else 0
        if d == 0 or gini(ys) == 0: return ('leaf', leaf)
        best = None
        for ax in (0, 1):
            vals = sorted(set(P[i][ax] for i in idx))
            for a, b_ in zip(vals, vals[1:]):
                thr = (a + b_) / 2
                L_ = [i for i in idx if P[i][ax] < thr]; R_ = [i for i in idx if P[i][ax] >= thr]
                sc = len(L_) * gini([y[i] for i in L_]) + len(R_) * gini([y[i] for i in R_])
                if best is None or sc < best[0] - 1e-9: best = (sc, ax, thr, L_, R_)
        if best is None or best[0] >= len(idx) * gini(ys) - 1e-9: return ('leaf', leaf)
        _, ax, thr, L_, R_ = best
        out.append((ax, thr, lo, hi))
        hl = list(hi); hl[ax] = thr; lr_ = list(lo); lr_[ax] = thr
        return ('split', ax, thr, build(L_, d - 1, lo, tuple(hl)), build(R_, d - 1, tuple(lr_), hi))
    root = build(list(range(len(P))), depth, lo, hi)
    def pred(p, n=root):
        while n[0] == 'split': n = n[3] if p[n[1]] < n[2] else n[4]
        return n[1]
    return out, pred

def knn(P, y, k):
    def pred(p):
        d = sorted(range(len(P)), key=lambda i: (P[i][0] - p[0]) ** 2 + (P[i][1] - p[1]) ** 2)[:k]
        return 1 if sum(y[i] for i in d) * 2 > k else 0
    return pred

def mlp(P, y, H=8, epochs=3000, lr=.8, seed=3):
    rnd = random.Random(seed)
    W1 = [[rnd.gauss(0, 1) for _ in range(2)] for _ in range(H)]; b1 = [0.0] * H
    W2 = [rnd.gauss(0, 1) for _ in range(H)]; b2 = 0.0
    X = [((a - 5) / 5, (b_ - 5) / 5) for a, b_ in P]
    for _ in range(epochs):
        gW1 = [[0, 0] for _ in range(H)]; gb1 = [0] * H; gW2 = [0] * H; gb2 = 0
        for (a, b_), t in zip(X, y):
            h = [math.tanh(W1[j][0] * a + W1[j][1] * b_ + b1[j]) for j in range(H)]
            o = sig(sum(W2[j] * h[j] for j in range(H)) + b2); e = o - t
            gb2 += e
            for j in range(H):
                gW2[j] += e * h[j]; dh = e * W2[j] * (1 - h[j] ** 2)
                gW1[j][0] += dh * a; gW1[j][1] += dh * b_; gb1[j] += dh
        n = len(X)
        for j in range(H):
            W2[j] -= lr * gW2[j] / n; b1[j] -= lr * gb1[j] / n
            W1[j][0] -= lr * gW1[j][0] / n; W1[j][1] -= lr * gW1[j][1] / n
        b2 -= lr * gb2 / n
    def prob(p):
        a, b_ = (p[0] - 5) / 5, (p[1] - 5) / 5
        h = [math.tanh(W1[j][0] * a + W1[j][1] * b_ + b1[j]) for j in range(H)]
        return sig(sum(W2[j] * h[j] for j in range(H)) + b2)
    return lambda p: 1 if prob(p) > .5 else 0

def shade(pl, pred, n=25, t0=0., dt=.06, fig=None):
    """Decision regions as a grid of cells, revealed column by column on fig (an Anim)."""
    cw, ch = pl.pw / n, pl.ph / n
    for i in range(n):
        g = ''
        for j in range(n):
            x = pl.x0 + (i + .5) / n * (pl.x1 - pl.x0); yv = pl.y0 + (j + .5) / n * (pl.y1 - pl.y0)
            c = pred((x, yv))
            g += R(pl.px + i * cw, pl.py + pl.ph - (j + 1) * ch, cw + .3, ch + .3,
                   tint('gr', '.20') if c else tint('bl', '.10'), 'none', 0)
        fig.show(g, t0 + i * dt, d=.2)
    return t0 + n * dt

def clipline(pl, w1, w2, b):
    """Segment of w1*x + w2*y + b = 0 inside the plot box (data coords) -> pixel endpoints or None."""
    pts = []
    if abs(w2) > 1e-9:
        for x in (pl.x0, pl.x1):
            y = -(w1 * x + b) / w2
            if pl.y0 - 1e-9 <= y <= pl.y1 + 1e-9: pts.append((x, y))
    if abs(w1) > 1e-9:
        for y in (pl.y0, pl.y1):
            x = -(w2 * y + b) / w1
            if pl.x0 - 1e-9 <= x <= pl.x1 + 1e-9: pts.append((x, y))
    pts = sorted(set((round(a, 6), round(c, 6)) for a, c in pts))
    if len(pts) < 2: return None
    return pl.P(*pts[0]), pl.P(*pts[-1])

def frame_box(pl):
    return R(pl.px, pl.py, pl.pw, pl.ph, 'var(--bg)', RULE_HI, 4, 1)
