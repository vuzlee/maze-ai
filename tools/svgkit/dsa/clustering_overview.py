# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/07-clustering/clustering-overview.
One shared toy set (seed 4): two round blobs A and B, a moon curving round B, three outliers. Each family
- k-means, DBSCAN, single-linkage agglomerative, Gaussian mixture - is run on it here in pure Python, so
every label, distance and score in a figure is computed. Run: python3 clustering_overview.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import decision_tree as dt
from linear_algebra import Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, BR, VI, FI, RO, RULE, BG, tn, S, chip, dot, poly, finish
from tablefig import GR, AM, RD, tint, pill

_RGB = {GR: '--green-a', RD: '--red-a', AM: '--amber-a', FI: '--blue-a', VI: '--violet-a', BR: '--clay-a'}
def tn(c, a='.14'): return 'rgba(var(%s),%s)' % (_RGB[c], a)
def chip(cx, cy, s, c=VI, w=None, mono=True):
    w = w or 16 + len(s) * 7.2
    return (R(cx - w / 2, cy - 11, w, 22, BG, 'none', 11) + R(cx - w / 2, cy - 11, w, 22, tn(c), c, 11, 1.3) +
            T(cx, cy + 4.5, s, c, mono=mono, bold=True))

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/07-clustering/clustering-overview/index.html')

# ---------- data ----------
_g = random.Random(4)
A = [(1.8 + _g.gauss(0, .4), 7.8 + _g.gauss(0, .4)) for _ in range(8)]
B = [(6.2 + _g.gauss(0, .35), 5.0 + _g.gauss(0, .35)) for _ in range(8)]
MOON = []
for i in range(14):
    a = math.radians(150 + 210 * i / 13); r = 2.7 + _g.gauss(0, .1)
    MOON.append((6.2 + r * math.cos(a), 5.0 + r * math.sin(a)))
OUT = [(1.2, 2.0), (9.6, 9.4), (4.6, 8.8)]
P = A + B + MOON + OUT; N = len(P)
TRUTH = [0] * 8 + [1] * 8 + [2] * 14 + [-1] * 3      # the shapes as drawn: A, B, moon, noise
SHAPES = [('blob A', range(0, 8)), ('blob B', range(8, 16)), ('moon', range(16, 30)), ('outliers', range(30, 33))]
def d(p, q): return math.hypot(p[0] - q[0], p[1] - q[1])
assert N == 33 and round(min(d(p, q) for p in A for q in B), 2) == 4.11

# ---------- k-means ----------
def kmeans(C):
    hist = [(list(C), None)]
    while True:
        lab = [min(range(3), key=lambda k: d(p, C[k])) for p in P]
        nc = [tuple(sum(P[i][j] for i in range(N) if lab[i] == k) / lab.count(k) for j in (0, 1)) for k in range(3)]
        hist.append((nc, lab))
        if nc == C: return lab, hist
        C = nc
KM, KMH = kmeans([P[0], P[8], P[16]])
def wss(C, lab): return sum(d(P[i], C[lab[i]]) ** 2 for i in range(N))
KMW = [wss(KMH[i][0], KMH[i + 1][1]) for i in range(len(KMH) - 1)]
assert KM == [0] * 8 + [1] * 8 + [0, 2, 2, 2, 2, 2, 2] + [1] * 7 + [2, 1, 0]
assert len(KMH) == 6 and all(a >= b - 1e-9 for a, b in zip(KMW, KMW[1:]))

# ---------- DBSCAN ----------
EPS, MINPTS = 1.0, 3
NB = [[j for j in range(N) if d(P[i], P[j]) <= EPS] for i in range(N)]
CORE = [len(n) >= MINPTS for n in NB]
DB = [-1] * N; DBORDER = []          # (point, cluster, reached-from) in the order DBSCAN labels them
_c = 0
for i in range(N):
    if DB[i] != -1 or not CORE[i]: continue
    DB[i] = _c; DBORDER.append((i, _c, None)); q = [i]
    while q:
        u = q.pop(0)
        if not CORE[u]: continue
        for v in NB[u]:
            if DB[v] == -1: DB[v] = _c; DBORDER.append((v, _c, u)); q.append(v)
    _c += 1
assert DB == TRUTH and sum(CORE) == 28 and not any(CORE[i] for i in range(30, 33))

# ---------- agglomerative, single linkage ----------
def agglo():
    cl = {i: [i] for i in range(N)}; nxt = N; merges = []
    while len(cl) > 1:
        best = None; ks = sorted(cl)
        for x in range(len(ks)):
            for y in range(x + 1, len(ks)):
                a, b = ks[x], ks[y]
                v, i, j = min((d(P[i], P[j]), i, j) for i in cl[a] for j in cl[b])
                if best is None or v < best[0] - 1e-12: best = (v, a, b, i, j)
        v, a, b, i, j = best
        merges.append((v, a, b, nxt, i, j)); cl[nxt] = cl.pop(a) + cl.pop(b); nxt += 1
    return merges
AG = agglo()
CUT = 1.0
BANDS = [.4, .55, .7, CUT]       # height bands for the batched merges below the cut
def cut_labels(h):
    par = list(range(N))
    def f(x):
        while par[x] != x: x = par[x]
        return x
    for v, a, b, n, i, j in AG:
        if v <= h: par[f(i)] = f(j)
    roots = {}; out = []
    for i in range(N): out.append(roots.setdefault(f(i), len(roots)))
    return out
AGL = cut_labels(CUT)
AGD = [TRUTH[i] if AGL.count(AGL[i]) > 1 else -1 for i in range(N)]   # singletons = noise; ids aligned by the assert below
assert [round(m[0], 2) for m in AG[-7:]] == [.81, .82, 1.63, 1.88, 2.52, 3.03, 4.44]
assert sorted([AGL.count(c) for c in set(AGL)]) == [1, 1, 1, 8, 8, 14]
assert all((AGL[i] == AGL[j]) == (TRUTH[i] == TRUTH[j] and TRUTH[i] >= 0) or i == j for i in range(N) for j in range(N))

# ---------- Gaussian mixture, EM from the k-means centres ----------
def pdf(p, m, s):
    a, b, dd = s[0][0], s[0][1], s[1][1]; det = a * dd - b * b; x = p[0] - m[0]; y = p[1] - m[1]
    return math.exp(-(dd * x * x - 2 * b * x * y + a * y * y) / det / 2) / (2 * math.pi * math.sqrt(det))
def gmm(mu, iters):
    mu = [list(m) for m in mu]; Sg = [[[1, 0], [0, 1]] for _ in range(3)]; w = [1 / 3] * 3; hist = []
    for it in range(iters + 1):
        Rs = []
        for p in P:
            v = [w[k] * pdf(p, mu[k], Sg[k]) for k in range(3)]; t = sum(v); Rs.append([x / t for x in v])
        ll = sum(math.log(sum(w[k] * pdf(p, mu[k], Sg[k]) for k in range(3))) for p in P)
        hist.append(([m[:] for m in mu], [[r[:] for r in s] for s in Sg], ll, Rs))
        if it == iters: break
        for k in range(3):
            nk = sum(r[k] for r in Rs); w[k] = nk / N
            mu[k] = [sum(Rs[i][k] * P[i][j] for i in range(N)) / nk for j in (0, 1)]
            Sg[k] = [[sum(Rs[i][k] * (P[i][a] - mu[k][a]) * (P[i][b] - mu[k][b]) for i in range(N)) / nk + 1e-3 * (a == b)
                      for b in (0, 1)] for a in (0, 1)]
    return hist
GSTEPS = [0, 1, 2, 4, 8, 16]
GH = gmm(KMH[-1][0], GSTEPS[-1])
GLAB = [max(range(3), key=lambda k: r[k]) for r in GH[-1][3]]
GSOFT = [max(r) for r in GH[-1][3]]
assert all(b[2] >= a[2] - 1e-9 for a, b in zip(GH, GH[1:]))
print('gmm labels', GLAB, [round(x, 2) for x in GSOFT], 'll', [round(GH[s][2], 1) for s in GSTEPS])

def ellipse(m, s, k=2.0):
    """k-sigma ellipse of a 2x2 covariance -> (cx, cy, rx, ry, angle deg) in data units"""
    a, b, c = s[0][0], s[0][1], s[1][1]; tr = (a + c) / 2; q = math.sqrt(((a - c) / 2) ** 2 + b * b)
    l1, l2 = tr + q, tr - q; ang = math.degrees(math.atan2(l1 - a, b)) if abs(b) > 1e-12 else (0 if a >= c else 90)
    return m[0], m[1], k * math.sqrt(l1), k * math.sqrt(l2), ang

# ---------- silhouette ----------
def ab(L, i):
    own = [j for j in range(N) if L[j] == L[i] and j != i]
    a = sum(d(P[i], P[j]) for j in own) / len(own)
    bs = {c: sum(d(P[i], P[j]) for j in range(N) if L[j] == c) / L.count(c) for c in set(L) if c >= 0 and c != L[i]}
    cb = min(bs, key=bs.get); return a, bs[cb], cb
def sil(L):
    out = {}
    for i in range(N):
        if L[i] < 0 or L.count(L[i]) < 2: continue
        a, b, _ = ab(L, i); out[i] = (b - a) / max(a, b)
    return out
SK = sil(KM); SKM = sum(SK.values()) / len(SK)
SD = sil(DB); SDM = sum(SD.values()) / len(SD)
I1, I2 = 12, 23
assert KM[I1] == 1 and KM[I2] == 1 and TRUTH[I2] == 2
assert round(SK[I1], 2) == .45 and round(SK[I2], 2) == -.01
assert round(SKM, 2) == .46 and round(SDM, 2) == .37 and len(SD) == 30

# ---------- drawing helpers ----------
CC = [FI, VI, GR]                 # cluster colours; noise = hollow red
PS, PX0, PY0 = 26, 6, 34          # plot scale (px per data unit) and origin
def X(x, x0=PX0): return x0 + x * PS
def Y(y, y0=PY0): return y0 + (10 - y) * PS
PW = 10 * PS
def frame(x0=PX0, y0=PY0): return R(x0, y0, PW, 9 * PS, BG, RULE_HI, 4, 1)
def pt(i, c=None, x0=PX0, y0=PY0, r=3.6):
    x, y = X(P[i][0], x0), Y(P[i][1], y0)
    if c is None: return '<circle cx="%.1f" cy="%.1f" r="%s" fill="var(--bg)" stroke="%s" stroke-width="1.2"/>' % (x, y, r, RULE_HI)
    if c == 'noise':
        return ('<circle cx="%.1f" cy="%.1f" r="%s" fill="var(--bg)" stroke="%s" stroke-width="1.6"/>' % (x, y, r + .6, RD) +
                L(x - 2.4, y - 2.4, x + 2.4, y + 2.4, RD, 1.3) + L(x - 2.4, y + 2.4, x + 2.4, y - 2.4, RD, 1.3))
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="var(--bg)" stroke-width="1"/>' % (x, y, r + .4, c)
def labcol(l): return 'noise' if l < 0 else CC[l]
def cross(x, y, c, s=6):
    return ('<circle cx="%.1f" cy="%.1f" r="8" fill="var(--bg)" stroke="%s" stroke-width="1.8"/>' % (x, y, c) +
            L(x - s, y, x + s, y, c, 2) + L(x, y - s, x, y + s, c, 2))
def badge(f, x, y, steps):
    """'now running' strip: one line per step, each shown in turn and hidden when the next starts"""
    f.static(T(x, y, 'now', MU, 'start', cls='sv-hv'))
    for k, (t, s, end) in enumerate(steps):
        w = 330
        f.show(R(x + 34, y - 15, w, 22, BG, 'none', 5) + R(x + 34, y - 15, w, 22, tint('am', '.12'), AM, 5, 1.3) +
               T(x + 44, y, s, AM, 'start', cls='sv-s', bold=True), t, hide=end)
def verdict(f, x, y, lab, t):
    """four shape chips; green when the family's labels reproduce that shape exactly, red otherwise"""
    f.static(T(x, y - 18, 'which shapes it caught', MU, 'start', cls='sv-hv'))
    ok = []
    for k, (name, idx) in enumerate(SHAPES):
        idx = list(idx)
        if name == 'outliers': good = all(lab[i] < 0 for i in idx)
        else:
            c = lab[idx[0]]; mem = [j for j in range(N) if lab[j] == c]
            good = c >= 0 and all(lab[i] == c for i in idx) and len(idx) >= .75 * len(mem)   # whole shape, and most of its cluster
        ok.append(good)
        cx = x + 44 + k * 92
        f.show(pill(cx, y, ('✓ ' if good else '✗ ') + name, 'gr' if good else 'rd', 84), t + k * .25)
    return ok
OKS = {}

def base_points(f):
    f.static(frame() + ''.join(pt(i) for i in range(N)))

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('co1-', 720, 0, '33 unlabelled points on a plane. One point is picked; dashed lines run from it to its three '
             'nearest neighbours, all short, and to one far point, long. Then the points take colours as the groups a person '
             'sees: a round blob top left, a round blob in the middle, a moon curving round it, and three lone outliers '
             'marked as noise. Clustering is the search for that colouring with no labels given.',
             'NO LABELS · ONLY DISTANCES · FIND THE GROUPS')
    base_points(f)
    i0 = 3; near = sorted(range(N), key=lambda j: d(P[i0], P[j]))[1:4]; far = 25
    x0, y0 = X(P[i0][0]), Y(P[i0][1])
    f.show('<circle cx="%.1f" cy="%.1f" r="9" fill="none" stroke="%s" stroke-width="1.8"/>' % (x0, y0, AM), .4, hide=4.2)
    for k, j in enumerate(near):
        f.show(L(x0, y0, X(P[j][0]), Y(P[j][1]), GR, 1.5, '3 3'), .9 + k * .2, hide=4.2)
    f.show(L(x0, y0, X(P[far][0]), Y(P[far][1]), RD, 1.4, '3 3'), 1.8, hide=4.2)
    xr = PX0 + PW + 40
    f.show(T(xr, 70, 'near: %.1f · %.1f · %.1f' % tuple(d(P[i0], P[j]) for j in near), GR, 'start', cls='sv-s', bold=True), 1.3, hide=4.2)
    f.show(T(xr, 92, 'far: %.1f' % d(P[i0], P[far]), RD, 'start', cls='sv-s', bold=True), 2.0, hide=4.2)
    f.show(T(xr, 120, 'close points should share a group', MU, 'start', cls='sv-s'), 2.6, hide=4.2)
    t = 4.6
    for k, (name, idx) in enumerate(SHAPES):
        c = 'noise' if k == 3 else CC[k]
        f.show(''.join(pt(i, c) for i in idx), t)
        col = RD if k == 3 else CC[k]
        f.show(dot(xr + 6, 70 + k * 28 - 4, col, 5) + T(xr + 20, 70 + k * 28, '%s · %d points' % (name, len(idx)), col,
                                                     'start', cls='sv-s', bold=True), t)
        t += .7
    f.show(T(xr, 70 + 4 * 28 + 10, 'the answer a person sees', MU, 'start', cls='sv-s') +
           T(xr, 70 + 4 * 28 + 30, 'no algorithm is given these colours', MU, 'start', cls='sv-s'), t)
    assert max(d(P[i0], P[j]) for j in near) < 1 and d(P[i0], P[far]) > 5
    return finish(f, PY0 + 9 * PS + 10)

# ---------- 2.1 Centroid: k-means ----------
XR = PX0 + PW + 34
def fig_kmeans():
    f = Anim('co2-', 720, 0, 'k-means with k = 3 on the shared points. Three centroid crosses start on three points. Each round '
             'every point takes the colour of its nearest cross, then each cross glides to the mean of its points. After %d '
             'rounds nothing moves. The within-cluster squared distance drops each round, %s. Both blobs are caught, but '
             'the moon is cut in three pieces and every outlier is forced into a cluster.' % (
                 len(KMH) - 2, ', '.join('%.0f' % w for w in KMW)),
             'CENTROID · NEAREST CROSS · MOVE CROSS TO MEAN · REPEAT')
    base_points(f)
    rounds = len(KMH) - 1; t = .6; steps = []; D = 2.0
    cs = [(X(c[0]), Y(c[1])) for c in KMH[0][0]]
    # the chart that is built round by round
    cx0, cy0, cw, ch = XR + 10, 120, 300, 110
    f.static(T(XR, 104, 'within-cluster squared distance', MU, 'start', cls='sv-hv') +
             L(cx0, cy0 + ch, cx0 + cw, cy0 + ch, RULE_HI, 1) + L(cx0, cy0, cx0, cy0 + ch, RULE_HI, 1))
    wmax = KMW[0] * 1.05
    def cp(r): return cx0 + 30 + r * (cw - 60) / (rounds - 1), cy0 + ch - KMW[r] / wmax * ch
    for r in range(rounds):
        C, _ = KMH[r]; lab = KMH[r + 1][1]; end = t + D if r < rounds - 1 else None
        steps.append((t, 'round %d · each point → nearest cross' % (r + 1), t + D * .5))
        f.show(''.join(pt(i, CC[lab[i]]) for i in range(N)), t, hide=end)
        x, y = cp(r)
        f.show(dot(x, y, AM, 4) + T(x, cy0 + ch + 14, str(r + 1), FA, mono=True) +
               (L(*cp(r - 1), x, y, AM, 1.4) if r else '') + T(x, y - 9, '%.0f' % KMW[r], AM, mono=True), t + .4)
        steps.append((t + D * .5, 'round %d · move each cross to its mean' % (r + 1), t + D if r < rounds - 1 else None))
        t += D
    badge(f, XR, 52, steps)
    for k in range(3):
        pts = [(0, cs[k][0] - X(KMH[-1][0][k][0]), cs[k][1] - Y(KMH[-1][0][k][1]))]
        for r in range(1, rounds):
            pts.append((.6 + (r - 1) * D + D * .5, X(KMH[r][0][k][0]) - X(KMH[-1][0][k][0]), Y(KMH[r][0][k][1]) - Y(KMH[-1][0][k][1])))
        fx, fy = X(KMH[-1][0][k][0]), Y(KMH[-1][0][k][1])
        f.path(cross(fx, fy, CC[k]), pts, .3, d=.8)
    f.show(T(cx0 + cw - 30, cy0 + ch + 30, 'round', FA, 'end', cls='sv-d'), t)
    OKS['KM'] = verdict(f, XR, 290, KM, t + .2)
    return finish(f, max(PY0 + 9 * PS + 10, 312))

# ---------- 2.2 Density: DBSCAN ----------
def fig_dbscan():
    f = Anim('co3-', 720, 0, 'DBSCAN with eps = %g and min points = %d. An eps circle lands on the first core point and its '
             'neighbours take its colour; the circle glides on from neighbour to neighbour, so the colour spreads through the '
             'whole blob, then the next blob, then all the way round the moon. Points with no dense neighbourhood stay '
             'noise and get a red cross. All four shapes come out right, the moon in one piece.' % (EPS, MINPTS),
             'DENSITY · CORE POINT + EPS CIRCLE · SPREAD THROUGH NEIGHBOURS')
    base_points(f)
    seq = [o for o in DBORDER]
    T0, dt_ = .6, .17; tt = {}
    for k, (i, c, src) in enumerate(seq): tt[i] = T0 + k * dt_ + c * .5
    rr = EPS * PS
    # one circle per cluster, gliding over the core points in the order they spread
    for c in range(3):
        cores = [i for i, cc, _ in seq if cc == c and CORE[i]]
        lx, ly = X(P[cores[-1]][0]), Y(P[cores[-1]][1])
        pts = [(0, X(P[cores[0]][0]) - lx, Y(P[cores[0]][1]) - ly)]
        for i in cores[1:]:
            pts.append((tt[i], X(P[i][0]) - lx, Y(P[i][1]) - ly))
        end = max(tt[i] for i, cc, _ in seq if cc == c) + .6
        f.path('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="1.4" stroke-dasharray="4 3"/>' % (
            lx, ly, rr, tn(CC[c], '.08'), AM), pts, tt[cores[0]] - .3, d=dt_ * .9, hide=end)
    for i, c, src in seq:
        f.show(pt(i, CC[c], r=3.6 if CORE[i] else 2.8), tt[i] + .1, d=.2)
    tn_ = max(tt.values()) + .9
    f.show(''.join(pt(i, 'noise') for i in range(N) if DB[i] < 0), tn_)
    st = [min(tt[i] for i, cc, _ in seq if cc == c) for c in range(3)] + [tn_]
    steps = [(.3, 'core point · ≥ %d points within eps' % MINPTS, st[0] + .8)]
    steps += [(st[0] + .8 if c == 0 else st[c], 'cluster %d spreads through neighbours' % (c + 1), st[c + 1]) for c in range(3)]
    steps.append((tn_, 'nobody reached · noise', None))
    badge(f, XR, 52, steps)
    # tally built as points are labelled
    f.static(T(XR, 104, 'points labelled so far', MU, 'start', cls='sv-hv'))
    for c in range(3):
        n = DB.count(c); y = 126 + c * 30
        f.show(dot(XR + 8, y - 4, CC[c], 5) + T(XR + 22, y, 'cluster %d' % (c + 1), CC[c], 'start', cls='sv-s', bold=True), .3)
        ids = [i for i, cc, _ in seq if cc == c]
        for k, i in enumerate(ids):
            f.show('<rect x="%.1f" y="%.1f" width="12" height="14" rx="2" fill="%s"/>' % (XR + 92 + k * 15, y - 11, CC[c]), tt[i] + .1, d=.2)
    yN = 126 + 3 * 30
    f.show(T(XR + 22, yN, 'noise · %d points' % DB.count(-1), RD, 'start', cls='sv-s', bold=True) + dot(XR + 8, yN - 4, RD, 5), tn_)
    OKS['DB'] = verdict(f, XR, 290, DB, tn_ + .4)
    return finish(f, max(PY0 + 9 * PS + 10, 312))

# ---------- 2.3 Hierarchical: agglomerative ----------
def fig_agglo():
    f = Anim('co4-', 720, 0, 'Single-linkage agglomerative clustering. Every point starts as its own cluster. The two closest '
             'clusters are joined, again and again: a short grey link appears on the plot and the same merge rises in the '
             'dendrogram on the right at its height. The last joins are long: %s. A cut line at height %g leaves six '
             'pieces - blob A, blob B, the whole moon and three lone points, which are the outliers.' % (
                 ', '.join('%.2f' % m[0] for m in AG[-4:]), CUT),
             'HIERARCHICAL · JOIN THE TWO CLOSEST · RECORD THE HEIGHT · CUT')
    base_points(f)
    # dendrogram geometry: leaves in tree order
    kids = {m[3]: (m[1], m[2], m[0]) for m in AG}
    order = []
    def walk(n):
        if n < N: order.append(n)
        else: walk(kids[n][0]); walk(kids[n][1])
    walk(AG[-1][3])
    gx0, gx1, gyb, gyt, HMAX = XR + 10, 712, 290, 96, 4.6
    lx = {n: gx0 + (gx1 - gx0) * (k + .5) / N for k, n in enumerate(order)}
    hy = lambda h: gyb - h / HMAX * (gyb - gyt)
    f.static(L(gx0 - 6, gyb, gx1, gyb, RULE_HI, 1) + L(gx0 - 6, gyt, gx0 - 6, gyb, RULE_HI, 1) +
             T(gx0 - 10, gyt + 4, '%.1f' % HMAX, FA, 'end', mono=True) + T(gx0 - 10, gyb + 4, '0', FA, 'end', mono=True) +
             T(gx0 - 2, gyt - 8, 'merge height', MU, 'start', cls='sv-hv'))
    for n in order:
        c = labcol(TRUTH[n])
        f.static(dot(lx[n], gyb + 6, RD if c == 'noise' else c, 2.4))
    hgt = {n: 0 for n in range(N)}; t = .6; mt = []
    for v, a, b, n, i, j in AG:
        lx[n] = (lx[a] + lx[b]) / 2; hgt[n] = v
        seg = (L(lx[a], hy(hgt[a]), lx[a], hy(v), TX, 1.1) + L(lx[b], hy(hgt[b]), lx[b], hy(v), TX, 1.1) +
               L(lx[a], hy(v), lx[b], hy(v), TX, 1.1))
        link = L(X(P[i][0]), Y(P[i][1]), X(P[j][0]), Y(P[j][1]), MU if v <= CUT else RD, 1.6 if v <= CUT else 1.2,
                 None if v <= CUT else '4 3')
        if v <= CUT:          # small merges play in batches, one batch per height band
            b = next(k for k, e in enumerate(BANDS) if v <= e); tb = .6 + b * .9
            f.show(seg + link, tb, d=.5); mt.append(tb); t = .6 + len(BANDS) * .9
        else:
            f.show(seg + link, t, d=.4); mt.append(t); t += .9
    yc = hy(CUT)
    f.show(L(gx0 - 6, yc, gx1, yc, AM, 1.8, '6 4') + T(gx1, yc - 6, 'cut at %g' % CUT, AM, 'end', cls='sv-s', bold=True), t + .3)
    for i in range(N): f.show(pt(i, labcol(AGD[i])), t + .8)
    steps = [(.3, 'join the closest · short merges in height bands', mt[N - 7]), (mt[N - 7], 'long joins · whole shapes merge', t + .3),
             (t + .3, 'cut the tree · %d pieces' % len(set(AGL)), None)]
    badge(f, XR, 52, steps)
    OKS['AGD'] = verdict(f, XR, 334, AGD, t + 1.0)
    return finish(f, 358)

# ---------- 2.4 Distribution: Gaussian mixture ----------
def ell_svg(m, s, c, sw=1.6, dash=None):
    cx, cy, rx, ry, ang = ellipse(m, s)
    da = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.1f %.1f %.1f)" fill="%s" stroke="%s" '
            'stroke-width="%s"%s/>' % (X(cx), Y(cy), rx * PS, ry * PS, -ang, X(cx), Y(cy), tn(c, '.06'), c, sw, da))
def fig_gmm():
    f = Anim('co5-', 720, 0, 'A Gaussian mixture with three components, started from the k-means centres. Each EM round every '
             'point gets a probability for each component, shown as its colour and how solid it is, and each ellipse '
             'reshapes to the points it holds. The log-likelihood rises round by round, %s. The ellipses lean and stretch, '
             'but an ellipse cannot bend, so the moon is still split and outliers still belong somewhere.' % (
                 ', '.join('%.0f' % GH[s][2] for s in GSTEPS)),
             'DISTRIBUTION · SOFT MEMBERSHIP · RESHAPE ELLIPSES · REPEAT')
    base_points(f)
    cx0, cy0, cw, ch = XR + 10, 120, 300, 110
    f.static(T(XR, 104, 'log-likelihood of the data', MU, 'start', cls='sv-hv') +
             L(cx0, cy0 + ch, cx0 + cw, cy0 + ch, RULE_HI, 1) + L(cx0, cy0, cx0, cy0 + ch, RULE_HI, 1))
    lo, hi = GH[0][2] - 4, GH[-1][2] + 4
    def cp(k): return cx0 + 30 + k * (cw - 60) / (len(GSTEPS) - 1), cy0 + ch - (GH[GSTEPS[k]][2] - lo) / (hi - lo) * ch
    t = .6; D = 1.6; steps = []
    for k, s in enumerate(GSTEPS):
        mu, Sg, ll, Rs = GH[s]; end = t + D if k < len(GSTEPS) - 1 else None
        pts = ''
        for i in range(N):
            c = max(range(3), key=lambda q: Rs[i][q]); x, y = X(P[i][0]), Y(P[i][1])
            pts += ('<circle cx="%.1f" cy="%.1f" r="4" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="1"/>' %
                    (x, y, CC[c], max(Rs[i][c], .15) ** 2, CC[c]))
        f.show(pts + ''.join(ell_svg(mu[q], Sg[q], CC[q]) for q in range(3)), t, hide=end)
        x, y = cp(k)
        f.show(dot(x, y, AM, 4) + T(x, cy0 + ch + 14, str(s), FA, mono=True) + (L(*cp(k - 1), x, y, AM, 1.4) if k else ''), t + .3)
        steps.append((t, 'round %d · probabilities, then reshape' % s if s else 'start · round ellipses at k-means centres', end))
        t += D
    f.show(T(cx0 + 30, cp(0)[1] - 9, '%.0f' % GH[0][2], AM, 'middle', mono=True) +
           T(cp(len(GSTEPS) - 1)[0], cp(len(GSTEPS) - 1)[1] + 18, '%.0f' % GH[-1][2], AM, 'middle', mono=True), t - D + .4)
    f.show(T(cx0 + cw - 30, cy0 + ch + 30, 'EM round', FA, 'end', cls='sv-d'), t)
    badge(f, XR, 52, steps)
    OKS['GLAB'] = verdict(f, XR, 290, GLAB, t)
    return finish(f, max(PY0 + 9 * PS + 10, 312))

# ---------- 03 Silhouette ----------
def fig_sil():
    f = Anim('co6-', 720, 0, 'Silhouette on the k-means labels. One point in blob B is picked: lines to every other point of its '
             'own cluster give a, the mean distance %.2f; lines to the nearest other cluster give b, %.2f; s = (b - a) / max(a, b) '
             '= %.2f. Then a moon point that k-means put in the same cluster: a = %.2f, b = %.2f, s = %.2f, it sits on the '
             'border. Every point gets its s as a bar; their mean is %.2f. DBSCAN on the same points scores only %.2f '
             'although it found the true shapes.' % (ab(KM, I1)[0], ab(KM, I1)[1], SK[I1], ab(KM, I2)[0], ab(KM, I2)[1],
                                                    SK[I2], SKM, SDM),
             'NO ANSWER KEY · HOW CLOSE TO MY OWN · HOW FAR FROM THE NEXT')
    f.static(frame() + ''.join(pt(i, CC[KM[i]]) for i in range(N)))
    t = .5
    rows = []
    for n, i in enumerate((I1, I2)):
        a, b, cb = ab(KM, i); s = SK[i]; x0, y0 = X(P[i][0]), Y(P[i][1]); end = t + 4.4
        own = [j for j in range(N) if KM[j] == KM[i] and j != i]; oth = [j for j in range(N) if KM[j] == cb]
        f.show('<circle cx="%.1f" cy="%.1f" r="9" fill="none" stroke="%s" stroke-width="2"/>' % (x0, y0, AM), t, hide=end)
        f.show(''.join(L(x0, y0, X(P[j][0]), Y(P[j][1]), GR, .9) for j in own), t + .4, hide=t + 1.8)
        f.show(''.join(L(x0, y0, X(P[j][0]), Y(P[j][1]), RD, .9, '3 3') for j in oth), t + 1.9, hide=t + 3.3)
        yr = 74 + n * 74
        f.show(T(XR, yr, 'point %s' % ('in blob B' if n == 0 else 'on the moon'), TX, 'start', cls='sv-s', bold=True), t)
        # a and b values travel from the point to the row
        for k, (nm, v, c, tv) in enumerate((('a', a, GR, t + 1.2), ('b', b, RD, t + 2.7))):
            tx, ty = XR + 20 + k * 92, yr + 26
            chipsvg = chip(tx + 34, ty - 4, '%s = %.2f' % (nm, v), c, 82)
            f.path(chipsvg, [(0, x0 - tx - 34, y0 - ty + 4), (tv + .2, 0, 0)], tv, d=.7)
        f.show(chip(XR + 252, yr + 22, 's = %.2f' % s, GR if s > .25 else AM, 84), t + 3.8)
        t += 4.6
    # bars: every point's s, sorted within cluster
    bx0, by0, U = XR + 30, 232, 80          # s axis from -0.2 to 1, U px per unit
    zy = by0 + U; bw0 = 330
    def sy(v): return zy - v * U
    f.static(T(XR, by0 - 14, 'every point · its s', MU, 'start', cls='sv-hv'))
    f.static(L(bx0, sy(1), bx0, sy(-.2), RULE_HI, 1) + ''.join(
        L(bx0 - 3, sy(v), bx0, sy(v), RULE_HI, 1) + T(bx0 - 6, sy(v) + 3.5, ('%g' % v).replace('-', '−'), FA, 'end', mono=True)
        for v in (1, .5, 0, -.2)) + L(bx0, zy, bx0 + bw0, zy, TX, 1.1))
    order = sorted(SK, key=lambda i: (KM[i], -SK[i])); bw = bw0 / len(order)
    bars = ''
    for k, i in enumerate(order):
        v = SK[i]; h = max(abs(v) * U, 2 if v >= 0 else 5); y = zy - h if v >= 0 else zy
        bars += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (bx0 + k * bw + .5, y, bw - 1, h, CC[KM[i]] if v >= 0 else RD)
    neg = [i for i in SK if SK[i] < 0]
    assert min(SK.values()) > -.2 and len(neg) >= 1
    f.show(bars, t)
    f.show(T(bx0 + bw0 + 4, zy + 14, '%d below 0 · wrong side' % len(neg), RD, 'end', cls='sv-d'), t + .4)
    f.show(L(bx0, sy(SKM), bx0 + bw0, sy(SKM), AM, 1.4, '5 3') +
           T(bx0 + bw0, sy(SKM) - 6, 'mean %.2f' % SKM, AM, 'end', cls='sv-s', bold=True), t + .6)
    f.show(T(XR, sy(-.2) + 30, 'k-means %.2f · DBSCAN on the true shapes %.2f' % (SKM, SDM), RD, 'start', cls='sv-s', bold=True), t + 1.4)
    by0, bh = sy(-.2), 0
    return finish(f, max(PY0 + 9 * PS + 10, by0 + bh + 44))

# ---------- 04 Learning order ----------
LESSONS = [('K-means', 'round blobs, k given', FI), ('DBSCAN', 'any shape + noise', VI), ('HDBSCAN', 'mixed densities', GR)]
def fig_order():
    f = Anim('co7-', 720, 0, 'Three lessons as boxes, left to right: K-means, DBSCAN, HDBSCAN. An arrow from each to the next is '
             'labelled with the weakness it fixes: k-means splits the moon, so DBSCAN drops centroids; one eps cannot fit '
             'two densities, so HDBSCAN tries every eps. Agglomerative and Gaussian mixture sit below as side branches '
             'covered in this overview.', 'READ LEFT TO RIGHT · EACH LESSON FIXES THE ONE BEFORE')
    W, H, y = 170, 50, 40; xs = [0, 270, 540]
    fixes = ['splits the moon →', 'one eps for all →']
    t = .3
    for k, (name, sub, c) in enumerate(LESSONS):
        x = xs[k]
        f.show(R(x, y, W, H, BG, 'none', 6) + R(x, y, W, H, tn(c, '.10'), c, 6, 1.6) +
               T(x + 14, y + 21, str(k + 1), c, 'start', mono=True, bold=True) + T(x + 30, y + 21, name, c, 'start', bold=True) +
               T(x + 30, y + 38, sub, MU, 'start', cls='sv-d'), t)
        if k < 2:
            f.show(arrow(x + W + 6, y + H / 2, xs[k + 1] - 8, y + H / 2, MU, 1.4) +
                   T((x + W + xs[k + 1]) / 2, y + H / 2 - 9, fixes[k][:-2], RD, 'middle', cls='sv-d'), t + .6)
        t += 1.2
    for k, (name, sub) in enumerate((('Agglomerative', 'section 2.3 · no own lesson'), ('Gaussian mixture', 'section 2.4 · no own lesson'))):
        x = 100 + k * 330; yy = 130
        f.show(R(x, yy, 190, 40, BG, RULE_HI, 6, 1, '4 3') + T(x + 14, yy + 17, name, TX, 'start', bold=True) +
               T(x + 14, yy + 32, sub, FA, 'start', cls='sv-d'), t + k * .4)
    return finish(f, 180)

SCRIPT = re.search(r'<script>.*?</script>', dt.BODY, re.S).group(0)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Clustering</p>
  <h1>Clustering <em>overview</em></h1>
  <p class="lede">With no labels, a clustering method decides what "a group" means — a centre, a dense region, a chain of near points, or a bell curve — and that choice decides <b>which shapes it can find</b>.</p>
</header>

<section id="clov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Only distances are given; <em>close points should share a group</em>, and a few points belong to none.</p>
{co1}
  <ul class="why">
    <li>The same 33 points run through every figure below: two round blobs, a moon, three outliers.</li>
    <li>Distance needs features on one scale — standardise first (<a href="../../04-core-concepts/feature-engineering/index.html">Feature engineering</a>).</li>
  </ul>
</section>

<section id="clov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Families</h2></div>
  <p class="key">Four definitions of a group; run each on the same points and see <em>which shapes it catches</em>.</p>
  <div class="subsec" id="clov-s2-1">
    <h3 class="ssh"><b>2.1</b>Centroid · k-means</h3>
    <p class="skey">A group is <em>the points nearest one centre</em>; move the centres to the means until nothing changes.</p>
{co2}
    <ul class="why">
      <li>Fast and simple, but you choose <var>k</var>, every group comes out round, and outliers are forced in.</li>
      <li>Full lesson: <a href="../kmeans-clustering/index.html">K-means</a>.</li>
    </ul>
  </div>
  <div class="subsec" id="clov-s2-2">
    <h3 class="ssh"><b>2.2</b>Density · DBSCAN</h3>
    <p class="skey">A group is <em>a dense region</em>, grown from core points through their eps-neighbours; the rest is noise.</p>
{co3}
    <ul class="why">
      <li>No <var>k</var>, any shape, real noise — paid for with one <code>eps</code> that must suit every cluster.</li>
      <li>Full lessons: <a href="../dbscan/index.html">DBSCAN</a>, then <a href="../hdbscan/index.html">HDBSCAN</a> for clusters of different density.</li>
    </ul>
  </div>
  <div class="subsec" id="clov-s2-3">
    <h3 class="ssh"><b>2.3</b>Hierarchical · agglomerative</h3>
    <p class="skey">Start with every point alone, <em>join the two closest groups</em> again and again, and cut the record of joins — the <b>dendrogram</b> — at a height.</p>
{co4}
    <ul class="why">
      <li>"Closest groups" needs a <b>linkage</b>: <b>single</b> (nearest pair), <b>complete</b> (farthest pair), <b>average</b> (mean of all pairs) or <b>Ward</b> (smallest rise in within-cluster variance). Single follows chains like the moon; Ward makes round groups like k-means.</li>
      <li>One tree gives every number of clusters at once, but all pairwise distances cost O(<var>n</var><sup>2</sup>) memory — fine for thousands of points, not millions.</li>
    </ul>
  </div>
  <div class="subsec" id="clov-s2-4">
    <h3 class="ssh"><b>2.4</b>Distribution · Gaussian mixture</h3>
    <p class="skey">A group is <em>one bell curve</em>; every point gets a probability for each, and EM reshapes the curves to fit.</p>
{co5}
    <ul class="why">
      <li>A <b>Gaussian mixture model</b> (GMM) is k-means with soft membership and stretched, tilted ellipses instead of circles; fitted by <b>EM</b> (expectation–maximisation).</li>
      <li>The price: still <var>k</var> given, still convex shapes, and many more parameters that can collapse onto a few points.</li>
    </ul>
  </div>
</section>

<section id="clov-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Silhouette</h2></div>
  <p class="key">No answer key, so score each point by <em>how close it is to its own group</em> against <em>the nearest other group</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>s</var>(<var>i</var>)</span><em>from −1 to 1</em></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i><var>b</var>(<var>i</var>) − <var>a</var>(<var>i</var>)</i><i><b class="fn">max</b>(<var>a</var>(<var>i</var>), <var>b</var>(<var>i</var>))</i></span></span><em>a = mean distance inside · b = to the nearest other cluster</em></span>
    </div>
  </div>
{co6}
  <ul class="why">
    <li>Near 1: well inside its group. Near 0: on a border. Below 0: probably in the wrong group.</li>
    <li>Silhouette rewards round, separated groups — it ranks k-means above DBSCAN here although DBSCAN found the true shapes. Use it to compare settings of one method, not families.</li>
    <li>Cluster numbers are arbitrary: two runs may call the same group 0 and 2.</li>
  </ul>
</section>

<section id="clov-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Learning order</h2></div>
  <p class="key">Three lessons, each born to fix <em>where the one before breaks</em>.</p>
{co7}
  <ul class="why">
    <li><a href="../kmeans-clustering/index.html">K-means</a> → <a href="../dbscan/index.html">DBSCAN</a> → <a href="../hdbscan/index.html">HDBSCAN</a>.</li>
    <li>For many features, read <a href="../../08-dimensionality/pca-dimensionality/index.html">PCA</a> too: in high dimensions every distance looks alike.</li>
  </ul>
</section>

{script}

<footer>Machine learning · Clustering · next lesson in the group: <a href="../kmeans-clustering/index.html">K-means</a>.</footer>
'''

def build():
    figs = dict(co1=fig_mental(), co2=fig_kmeans(), co3=fig_dbscan(), co4=fig_agglo(), co5=fig_gmm(), co6=fig_sil(),
                co7=fig_order(), script=SCRIPT)
    assert OKS == dict(KM=[True, False, False, False], DB=[True] * 4, AGD=[True] * 4, GLAB=[True, False, False, False]), OKS
    return re.sub(r'\{(co\d+|script)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    dt.splice(PAGE, build(), 'Four ways to define a group - centroid, density, hierarchical, distribution - run on the same '
              'points to show which shapes each catches, plus the silhouette score and the learning order.')
