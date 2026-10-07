# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/07-clustering/kmeans-clustering.
Twelve points A..L in three loose groups; every number in a figure is computed here (fixed seeds) and pinned
with assert. Run: python3 kmeans_clustering.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, GH, RULE, BG,
                            M, S, chip, Plane, finish, poly)
from tablefig import GR, AM, RD, pill
from decision_tree import splice

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/07-clustering/kmeans-clustering/index.html')

# ---------- data + algorithm ----------
P = [(1, 2), (2, 1), (2, 4), (3, 2), (5, 8), (4, 7), (6, 9), (6, 6), (8, 2), (9, 4), (9, 1), (7, 3)]
IDS = 'ABCDEFGHIJKL'
INIT = [(3, 8), (5, 5), (9, 8)]

def d2(a, b): return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
def mean(ps): return (sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps))
def assign(X, C): return [min(range(len(C)), key=lambda j: (d2(p, C[j]), j)) for p in X]
def lloyd(X, C):
    """[(assignment, centroids used for it)] until an assignment repeats"""
    out, prev, C = [], None, list(C)
    while True:
        a = assign(X, C); out.append((a, C))
        if a == prev: return out
        prev = a
        C = [mean([p for p, k in zip(X, a) if k == j]) if j in a else C[j] for j in range(len(C))]
def inert(X, a, C): return sum(d2(p, C[k]) for p, k in zip(X, a))
def pp_init(X, k, g, log=None):
    C = [X[g.randrange(len(X))]]
    while len(C) < k:
        D = [min(d2(p, c) for c in C) for p in X]
        if log is not None: log.append(D)
        u, acc = g.random() * sum(D), 0
        for i, dv in enumerate(D):
            acc += dv
            if acc >= u: C.append(X[i]); break
    return C
def best(X, k, n=10, seed=0):
    g, b = random.Random(seed), None
    for _ in range(n):
        a, C = lloyd(X, pp_init(X, k, g))[-1]; I = inert(X, a, C)
        if b is None or I < b[0] - 1e-9: b = (I, a, C)
    return b
def sil(X, a):
    out = []
    for i, p in enumerate(X):
        own = [math.dist(p, q) for j, q in enumerate(X) if a[j] == a[i] and j != i]
        if not own: out.append(0); continue
        A = sum(own) / len(own)
        B = min(sum(math.dist(p, q) for j, q in enumerate(X) if a[j] == c) / a.count(c) for c in set(a) if c != a[i])
        out.append((B - A) / max(A, B))
    return out

RUN = lloyd(P, INIT)
assert len(RUN) == 3 and RUN[1][0] == RUN[2][0]
INS = [inert(P, a, C) for a, C in RUN]
assert [round(v, 2) for v in INS] == [165, 65.56, 22.25]
assert RUN[1][1] == [(5, 8), (4.75, 2.625), (9, 4)] and RUN[2][1] == [(5.25, 7.5), (2, 2.25), (8.25, 2.5)]
assert ''.join('123'[k] for k in RUN[0][0]) == '222211122322' and ''.join('123'[k] for k in RUN[1][0]) == '222211113333'
FINAL_A, FINAL_C = RUN[-1]
# point H (index 7) changes cluster between rounds 1 and 2
H = 7
HD = [[d2(P[H], c) for c in C] for _, C in RUN[:2]]
assert HD[0] == [13, 2, 13] and [round(v, 2) for v in HD[1]] == [5, 12.95, 13]
# random init: three random points, seed 18 -> C, B, H -> stuck
RIDX = random.Random(18).sample(range(12), 3); assert RIDX == [2, 1, 7]
RRUN = lloyd(P, [P[i] for i in RIDX]); RI = inert(P, *RRUN[-1])
assert len(RRUN) == 2 and round(RI, 2) == 86.17
# k-means++: seed 3
PPLOG = []; PPC = pp_init(P, 3, random.Random(3), PPLOG)
assert PPC == [P[3], P[8], P[4]]          # D, then I, then E
PPRUN = lloyd(P, PPC); assert round(inert(P, *PPRUN[-1]), 2) == 22.25 and len(PPRUN) == 2
assert sum(PPLOG[0]) == 279 and sum(PPLOG[1]) == 159
# elbow + silhouette
BEST = {k: best(P, k) for k in range(1, 7)}
ELB = [BEST[k][0] for k in range(1, 7)]
assert [round(v, 2) for v in ELB] == [170.58, 90.25, 22.25, 18, 13.75, 10.67]
SILK = {k: sum(sil(P, BEST[k][1])) / 12 for k in range(2, 7)}
assert [round(SILK[k], 2) for k in range(2, 7)] == [.43, .62, .46, .34, .2]
# silhouette of point C (index 2) in the final 3-cluster split
SC = 2
OWN = [j for j in range(12) if FINAL_A[j] == FINAL_A[SC] and j != SC]
OTH = {c: [j for j in range(12) if FINAL_A[j] == c] for c in set(FINAL_A) if c != FINAL_A[SC]}
OTHM = {c: sum(math.dist(P[SC], P[j]) for j in v) / len(v) for c, v in OTH.items()}
NB = min(OTHM, key=OTHM.get)
SA, SB = sum(math.dist(P[SC], P[j]) for j in OWN) / len(OWN), OTHM[NB]
SS = (SB - SA) / max(SA, SB)
assert OWN == [0, 1, 3] and NB == 0 and round(SA, 2) == 2.49 and round(SB, 2) == 4.87 and round(SS, 2) == .49
assert round(sil(P, FINAL_A)[SC], 6) == round(SS, 6)

# assumptions
STRIP = [(x + .5, 3) for x in range(10)] + [(x + .5, 5.5) for x in range(10)]
STRUE = [0] * 10 + [1] * 10
SI, SA_, SCN = best(STRIP, 2)
assert round(SI, 2) == 71.25 and inert(STRIP, STRUE, [(5, 3), (5, 5.5)]) == 165
assert len(set(SA_[:5])) == 1 and SA_[0] != SA_[5] and SA_[:10] == SA_[10:]     # cut left | right
g = random.Random(5)
BIG = [(round(3.5 + 3.5 * math.cos(t) * math.sqrt(r), 1), round(5 + 3.5 * math.sin(t) * math.sqrt(r), 1))
       for t, r in [(g.uniform(0, 6.28), g.uniform(.05, 1)) for _ in range(14)]]
SMALL = [(7.5, 4.6), (8.0, 5.4), (7.8, 5.0), (8.1, 4.7)]
UNEQ = BIG + SMALL
UI, UA, UC = best(UNEQ, 2)
SIDE = UA[-1]; STOLEN = [i for i in range(14) if UA[i] == SIDE]
assert len(STOLEN) == 4 and all(UA[i] == SIDE for i in range(14, 18))
UTRUE = inert(UNEQ, [0] * 14 + [1] * 4, [mean(BIG), mean(SMALL)])
assert UI < UTRUE and round(UI, 1) == 57.9 and round(UTRUE, 1) == 82.1
SCL = [(1.0, 300), (1.2, 800), (0.9, 1500), (1.1, 2100), (3.0, 400), (3.2, 1000), (2.9, 1600), (3.1, 2200)]
RAWA = best(SCL, 2)[1]
mx, my = mean(SCL)
sx = math.sqrt(sum((p[0] - mx) ** 2 for p in SCL) / 8); sy = math.sqrt(sum((p[1] - my) ** 2 for p in SCL) / 8)
ZS = [((p[0] - mx) / sx, (p[1] - my) / sy) for p in SCL]
ZA = best(ZS, 2)[1]
assert RAWA[0] == RAWA[1] == RAWA[4] == RAWA[5] != RAWA[2] and ZA[:4] == [ZA[0]] * 4 and ZA[4] != ZA[0]
OUT = (16, 2)
P2 = P + [OUT]
OA, OC = lloyd(P2, FINAL_C)[-1]
assert OA[:12] == FINAL_A and OA[12] == 2 and OC[2] == (9.8, 2.4)

# ---------- drawing ----------
CC = [VI, FI, GR, AM, RO, BR]
RG = {VI: '--violet-a', FI: '--blue-a', GR: '--green-a', AM: '--amber-a', RO: '--rose-a', BR: '--clay-a', RD: '--red-a', GH: '--blue-a'}
def tc(c, a='.16'): return 'rgba(var(%s),%s)' % (RG[c], a)
def chip(cx, cy, s, c=VI, w=None):
    w = w or 16 + len(s) * 7.2
    return (R(cx - w / 2, cy - 11, w, 22, BG, 'none', 11) + R(cx - w / 2, cy - 11, w, 22, tc(c, '.14'), c, 11, 1.3) +
            T(cx, cy + 4.5, s, c, mono=True, bold=True))
def fmt(v): return ('%.2f' % v).rstrip('0').rstrip('.')
def pdot(x, y, c=None, r=5.5):
    if c is None:
        return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, y, r - .6, BG, GH)
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="1.2"/>' % (x, y, r, c, BG)
def cmark(x, y, c, lab=None, s=8.5):
    pts = ' '.join('%.1f,%.1f' % q for q in ((x, y - s), (x + s, y), (x, y + s), (x - s, y)))
    o = ('<polygon points="%s" fill="%s"/>' % (pts, BG) +
         '<polygon points="%s" fill="%s" stroke="%s" stroke-width="2.2" stroke-linejoin="round"/>' % (pts, tc(c, '.30'), c))
    if lab: o += T(x + 11, y + 17, lab, c, 'start', mono=True, bold=True)
    return o
def ring(x, y, c=AM, r=9.5): return '<circle cx="%.1f" cy="%.1f" r="%s" fill="none" stroke="%s" stroke-width="1.8"/>' % (x, y, r, c)
def ccell(t, i, j, s, c):
    x, y, w = t.colx(j) + 3, t.ry(i) + 2, t.cols[j][1] - 6
    return R(x, y, w, t.rh - 4, BG, 'none', 2) + R(x, y, w, t.rh - 4, tc(c, '.22'), c, 2, 1) + T(t.cx(j), t.ry(i) + 15, s, c, bold=True)
def badge(x, y, s, c=AM, w=None):
    w = w or 18 + len(s) * 6.6
    return R(x, y, w, 22, BG, 'none', 5) + R(x, y, w, 22, tc(c, '.14'), c, 5, 1.4) + T(x + w / 2, y + 15, s, c, bold=True)
def grid10(pl, n=10, xl='{x}₁', yl='{x}₂'):
    return pl.grid(0, n, 0, 10, 2, xl=xl, yl=yl)
def table12(x, y, extra):
    t = Table(x, y, [('id', 26), ('x₁', 32), ('x₂', 32)] + extra, step=22, rh=20)
    return t
def rows12(f, t, order=None):
    f.static(t.head())
    for k, i in enumerate(order or range(12)):
        f.static(t.row(k, [IDS[i], '%g' % P[i][0], '%g' % P[i][1]] + [''] * (len(t.cols) - 3)).replace('y="%.1f" style' % (t.ry(k) + 17), 'y="%.1f" style' % (t.ry(k) + 14.5)))
def pts(f, pl, ids=True, c=None, idx=range(12)):
    for i in idx:
        x, y = pl(*P[i])
        f.static(pdot(x, y, c[i] if c else None) + (T(x + 8, y - 6, IDS[i], FA, 'start', mono=True) if ids else ''))
def cpath(f, pl, Cs, times, t0, lab=True, d=.8, hide=None, cols=CC):
    """centroid j drawn at Cs[-1][j]; glides through Cs[k][j] at times[k-1]"""
    for j in range(len(Cs[-1])):
        fx, fy = pl(*Cs[-1][j])
        offs = [(0,) + tuple(a - b for a, b in zip(pl(*Cs[0][j]), (fx, fy)))]
        for k in range(1, len(Cs)):
            ox, oy = pl(*Cs[k][j]); offs.append((times[k - 1], ox - fx, oy - fy))
        f.path(cmark(fx, fy, cols[j], 'c%d' % (j + 1) if lab else None), offs, t0, d=d, hide=hide)

def changes(As):
    """per point: list of (iteration, cluster) when its cluster changes"""
    return [[(k, a[i]) for k, a in enumerate(As) if k == 0 or As[k - 1][i] != a[i]] for i in range(len(As[0]))]

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('km1-', 720, 0, 'Twelve unlabelled points A to L with a table of their coordinates. Three centroids c1, c2, c3 are '
             'placed. Iteration 1: every point takes the colour of its nearest centroid and the table cluster column fills; '
             'inertia 165. Each centroid glides to the mean of its points. Iteration 2: H, I, K and L change colour; inertia '
             '65.56; the centroids glide again. Iteration 3: no point changes, inertia 22.25, the loop stops.',
             'ASSIGN TO THE NEAREST CENTROID · MOVE EACH CENTROID TO THE MEAN · REPEAT')
    pl = Plane(40, 292, 24)
    f.static(grid10(pl))
    t = table12(318, 30, [('cluster', 58)])
    rows12(f, t); pts(f, pl)
    TK = [.9 + k * 4.6 for k in range(3)]
    As = [a for a, _ in RUN]
    for i, ch in enumerate(changes(As)):
        x, y = pl(*P[i])
        for n, (k, c) in enumerate(ch):
            hide = TK[ch[n + 1][0]] + .3 + i * .12 if n + 1 < len(ch) else None
            ts = TK[k] + .3 + i * .12
            f.show(pdot(x, y, CC[c]) + T(x + 8, y - 6, IDS[i], CC[c], 'start', mono=True, bold=True), ts, hide=hide)
            f.show(ccell(t, i, 3, 'c%d' % (c + 1), CC[c]), ts, hide=hide)
    cpath(f, pl, [C for _, C in RUN[:2]] + [RUN[2][1]], [TK[0] + 2.9, TK[1] + 2.9], .4)
    PX = 520
    for k in range(3):
        y = 52 + k * 66
        f.show(R(PX - 6, y - 6, 206, 58, 'none', AM, 6, 1.6), TK[k], hide=TK[k + 1] if k < 2 else TK[2] + 2.4)
        f.show(S(PX, y + 10, 'iteration %d' % (k + 1), TX, bold=True), TK[k])
        f.show(S(PX, y + 30, 'assign', MU), TK[k] + .2)
        f.show(T(PX + 192, y + 30, 'inertia ' + fmt(INS[k]), AM if k < 2 else GR, 'end', mono=True, bold=True), TK[k] + 1.9)
        if k < 2: f.show(S(PX, y + 46, 'update → each mean', MU), TK[k] + 2.7)
        else: f.show(S(PX, y + 46, 'no point changed', GR, bold=True), TK[k] + 2.0)
    f.show(t.colbox(3, 12, GR), TK[2] + 2.0)
    f.show(pill(PX + 100, 262, 'converged · stop', 'gr'), TK[2] + 2.4)
    return finish(f, t.bottom(12) + 10)

# ---------- 2.1 Assign ----------
def fig_assign():
    f = Anim('km2-', 720, 0, 'Point H at (6, 6). Round 1: dashed lines run to the three centroids and their squared distances '
             'are written out: 13 to c1, 2 to c2, 13 to c3. The smallest, 2, is ringed and H turns the colour of c2. The '
             'centroids then move to their means. Round 2: the distances become 5, 12.95 and 13, so H switches to c1.',
             'ONE POINT · SQUARED DISTANCE TO EVERY CENTROID · TAKE THE SMALLEST')
    pl = Plane(40, 292, 24)
    f.static(grid10(pl))
    pts(f, pl, ids=False, idx=[i for i in range(12) if i != H])
    hx, hy = pl(*P[H])
    f.static(pdot(hx, hy) + T(hx + 10, hy + 16, 'H', TX, 'start', mono=True, bold=True))
    TR = [.8, 6.0]
    for r in range(2):
        C = RUN[r][1]; t0 = TR[r]; nxt = TR[1] if r == 0 else None
        for j, c in enumerate(C):
            cx, cy = pl(*c)
            f.show(L(hx, hy, cx, cy, CC[j], 1.4, '4 3'), t0 + .2 + j * .5, hide=nxt)
        y0 = 58 + r * 128
        f.show(S(330, y0, 'round %d' % (r + 1), TX, bold=True) + S(410, y0, 'centroids %s' % ('placed' if r == 0 else 'moved'), MU), t0)
        win = min(range(3), key=lambda j: HD[r][j])
        for j, c in enumerate(C):
            y = y0 + 24 + j * 26
            cs = '(%s, %s)' % (fmt(c[0]), fmt(c[1]))
            s = (T(330, y, 'c%d' % (j + 1), CC[j], 'start', mono=True, bold=True) + T(354, y, cs, MU, 'start', mono=True) +
                 M(452, y, '(6 − %s)² + (6 − %s)² = ' % (fmt(c[0]), fmt(c[1])), TX, 'start') +
                 T(700, y, fmt(HD[r][j]), TX, 'end', mono=True, bold=True))
            f.show(s, t0 + .4 + j * .5)
        yw = y0 + 24 + win * 26
        f.show(R(322, yw - 16, 388, 22, 'none', GR, 5, 1.8), t0 + 2.2)
        f.show(pdot(hx, hy, CC[win], 6.5), t0 + 2.7, hide=nxt)
        f.show(S(330, y0 + 104, 'H → c%d' % (win + 1), CC[win], bold=True), t0 + 2.7)
    cpath(f, pl, [RUN[0][1], RUN[1][1]], [TR[0] + 3.8], .3)
    f.show(ring(hx, hy, AM, 11), .4)
    return finish(f, 306)

# ---------- 2.2 Update ----------
def fig_update():
    f = Anim('km3-', 720, 0, 'The table sorted by the cluster each point took in round 1: E, F, G in c1; A, B, C, D, H, I, K, L '
             'in c2; J alone in c3. A mean row is computed under each group: (5, 8), (4.75, 2.63) and (9, 4). Each mean '
             'travels to the plane and its centroid glides there; c3 jumps from (9, 8) down to J.',
             'EACH CENTROID MOVES TO THE MEAN OF ITS POINTS')
    pl = Plane(40, 300, 24)
    f.static(grid10(pl))
    a0 = RUN[0][0]
    pts(f, pl, c=[CC[k] for k in a0])
    groups = [[i for i in range(12) if a0[i] == j] for j in range(3)]
    t = Table(318, 30, [('cluster', 52), ('id', 26), ('x₁', 46), ('x₂', 46)], step=21, rh=19)
    f.static(t.head())
    row, TM = 0, []
    for j, g in enumerate(groups):
        for i in g:
            f.show(t.row(row, ['', IDS[i], '%g' % P[i][0], '%g' % P[i][1]], colors={1: CC[j]}).replace(
                'y="%.1f" style' % (t.ry(row) + 17), 'y="%.1f" style' % (t.ry(row) + 14)) + ccell(t, row, 0, 'c%d' % (j + 1), CC[j]),
                .2 + row * .06)
            row += 1
        m = RUN[1][1][j]; tm = 1.6 + j * 1.6; TM.append(tm)
        y = t.ry(row)
        f.show(R(t.colx(1), y, 26 + 92, 19, tc(CC[j], '.10'), CC[j], 3, 1.2) + T(t.cx(1), y + 14, 'mean', CC[j], bold=True) +
               T(t.cx(2), y + 14, fmt(m[0]), CC[j], mono=True, bold=True) + T(t.cx(3), y + 14, fmt(m[1]), CC[j], mono=True, bold=True), tm)
        f.show(t.outline(row - len(g), row - 1, 1, 3, CC[j], 1.4), tm - .3, hide=tm + 1.2)
        fx, fy = pl(*m); sx, sy = t.cx(2) + 23, y + 10
        lab = '(%s, %s)' % (fmt(m[0]), fmt(m[1]))
        f.path(chip(fx, fy + 22 if j != 1 else fy + 24, lab, CC[j], 16 + len(lab) * 6.6),
               [(0, sx - fx, sy - fy - 22), (tm + .3, 0, 0)], tm + .1, d=.7, hide=tm + 1.5)
        row += 1
    for j in range(3):
        fx, fy = pl(*RUN[1][1][j]); ox, oy = pl(*RUN[0][1][j])
        f.path(cmark(fx, fy, CC[j], 'c%d' % (j + 1)), [(0, ox - fx, oy - fy), (TM[j] + 1.0, 0, 0)], .3, d=.8)
    return finish(f, max(t.ry(row - 1) + 24, 314))

# ---------- 2.3 Inertia ----------
def fig_inertia():
    f = Anim('km4-', 720, 0, 'Each point is joined to its centroid by a line; the squared lengths go into the table column for '
             'that iteration and are summed: 165 in iteration 1, 65.56 in iteration 2, 22.25 in iteration 3. The lines '
             'shorten as the centroids move, and the sum only goes down.',
             'INERTIA = SUM OF SQUARED DISTANCES TO THE OWN CENTROID · IT ONLY GOES DOWN')
    pl = Plane(40, 292, 24)
    f.static(grid10(pl))
    t = Table(318, 30, [('id', 26), ('iter 1', 60), ('iter 2', 60), ('iter 3', 60)], step=22, rh=20)
    f.static(t.head())
    for i in range(12):
        f.static(R(t.x, t.ry(i), t.w, t.rh, BG, RULE_HI, 3, 1) + T(t.cx(0), t.ry(i) + 14.5, IDS[i], TX))
    TK = [.8 + k * 3.6 for k in range(3)]
    As = [a for a, _ in RUN]
    for k, (a, C) in enumerate(RUN):
        nxt = TK[k + 1] if k < 2 else None
        for i in range(12):
            x, y = pl(*P[i]); cx, cy = pl(*C[a[i]])
            f.show(L(x, y, cx, cy, CC[a[i]], 1.5), TK[k] + i * .08, hide=nxt)
            f.show(T(t.cx(k + 1), t.ry(i) + 14.5, fmt(d2(P[i], C[a[i]])), CC[a[i]], mono=True), TK[k] + .3 + i * .08)
        yb = t.ry(12) + 4
        f.show(L(t.colx(k + 1) + 4, yb - 2, t.colx(k + 1) + 56, yb - 2, RULE_HI, 1) +
               T(t.cx(k + 1), yb + 14, fmt(INS[k]), AM if k < 2 else GR, mono=True, bold=True), TK[k] + 1.6)
    f.static(T(t.x + 13, t.ry(12) + 18, 'Σ', MU, 'middle', 'sv-m'))
    for i in range(12):
        f.static(pdot(*pl(*P[i])))
    for i, ch in enumerate(changes(As)):
        x, y = pl(*P[i])
        for n, (k, c) in enumerate(ch):
            hide = TK[ch[n + 1][0]] if n + 1 < len(ch) else None
            f.show(pdot(x, y, CC[c]), TK[k] + i * .08, hide=hide)
    cpath(f, pl, [C for _, C in RUN], [TK[1] - .9, TK[2] - .9], .3, lab=False)
    f.show(pill(t.x + t.w + 60, t.ry(12) - 2, 'only ↓', 'gr'), TK[2] + 2.0)
    return finish(f, t.ry(12) + 30)

# ---------- 3.1 Random init ----------
def runfig(pre, aria, capt, picks, run, final, tone, note2, pp_log=None):
    f = Anim(pre, 720, 0, aria, capt)
    pl = Plane(40, 292, 24)
    f.static(grid10(pl))
    pts(f, pl)
    TP = [.6 + n * .7 for n in range(3)]
    for n, i in enumerate(picks):
        x, y = pl(*P[i]); f.show(ring(x, y, AM, 11), TP[n])
    TA = [3.0, 5.6]
    As = [a for a, _ in run]
    for i, ch in enumerate(changes(As)):
        x, y = pl(*P[i])
        for n, (k, c) in enumerate(ch):
            hide = TA[ch[n + 1][0]] + i * .08 if n + 1 < len(ch) else None
            f.show(pdot(x, y, CC[c]), TA[k] + i * .08, hide=hide)
    Cs = [C for _, C in run]
    cpath(f, pl, Cs, [TA[1] - 1.0] * (len(Cs) - 1), TP[2] + .3)
    return f, pl, TA

def fig_random():
    f, pl, TA = runfig('km5-', 'Three points are drawn at random as the starting centroids: C, B and H, two of them in the same '
                       'lower-left group. The loop runs: the lower-left group is split between c1 and c2, while the top and '
                       'right groups are merged under c3. Nothing changes after one more round, so it stops with inertia '
                       '86.17 instead of the best 22.25.', 'INIT = k RANDOM POINTS · A BAD DRAW STAYS BAD',
                       RIDX, RRUN, None, None, None)
    X = 330
    f.show(S(X, 60, 'pick 3 points at random', TX, bold=True) + S(X, 80, 'C, B, H — two in the same group', MU), .6)
    f.show(S(X, 120, 'run the loop', TX, bold=True) + S(X, 140, 'converges after 2 rounds', MU), TA[0])
    f.show(S(X, 180, 'lower-left group cut in two,', RD) + S(X, 198, 'top and right merged', RD), TA[1] + .6)
    f.show(chip(X + 60, 236, 'inertia ' + fmt(RI), RD, 120), TA[1] + 1.2)
    f.show(S(X + 132, 240, 'best split: ' + fmt(INS[-1]), MU), TA[1] + 1.4)
    f.show(S(X, 278, 'a local minimum: no single step can leave it', MU), TA[1] + 1.8)
    return finish(f, 306)

# ---------- 3.2 k-means++ ----------
def fig_pp():
    f = Anim('km6-', 720, 0, 'k-means++ picks D at random as the first centroid. Every point gets its squared distance D² to the '
             'nearest chosen centroid, drawn as a bar; the next centroid is drawn with probability proportional to the bar, '
             'and I, far away, is picked. The bars are recomputed against D and I; E is picked. The loop then reaches '
             'inertia 22.25, the best split.', 'NEXT CENTROID DRAWN WITH PROBABILITY ∝ D² · FAR POINTS WIN')
    pl = Plane(40, 292, 24)
    f.static(grid10(pl)); pts(f, pl)
    t = Table(318, 30, [('id', 26), ('D² to {D}', 130), ('D² to {D, I}', 130)], step=22, rh=20)
    f.static(t.head())
    for i in range(12):
        f.static(R(t.x, t.ry(i), t.w, t.rh, BG, RULE_HI, 3, 1) + T(t.cx(0), t.ry(i) + 14.5, IDS[i], TX))
    TS = [1.6, 4.6]
    picks = [3, 8, 4]
    f.show(ring(*pl(*P[3]), AM, 11) + T(t.x + t.w + 10, t.ry(3) + 14.5, '1st: random', AM, 'start', bold=True), .5)
    for s, D in enumerate(PPLOG):
        tot = sum(D); sc = 70 / max(D)
        for i in range(12):
            x = t.colx(s + 1) + 6; y = t.ry(i)
            w = max(D[i] * sc, 0)
            f.show(R(x, y + 5, max(w, .8), 10, tc(FI, '.30'), FI, 2, 1) +
                   T(x + w + 5, y + 14, '%d' % D[i], MU, 'start', mono=True), TS[s] + i * .07)
            if i == 3 and s == 1: pass
        f.show(T(t.cx(s + 1), t.ry(12) + 16, 'Σ %d' % tot, MU, mono=True), TS[s] + 1.0)
        n = picks[s + 1]; x, y = t.colx(s + 1) + 6, t.ry(n)
        f.show(t.outline(n, n, s + 1, s + 1, AM, 1.8), TS[s] + 1.6)
        f.show(T(t.x + t.w + 10, y + 14.5, '%s: p = %d/%d' % ('2nd' if s == 0 else '3rd', D[n], tot), AM, 'start', bold=True), TS[s] + 1.8)
        f.show(ring(*pl(*P[n]), AM, 11), TS[s] + 2.0)
    TA = 7.6
    a = PPRUN[-1][0]
    for i in range(12):
        f.show(pdot(*pl(*P[i]), CC[a[i]]), TA + i * .06)
    cpath(f, pl, [C for _, C in PPRUN], [TA + .9], TS[1] + 2.2)
    f.show(chip(t.x + t.w + 70, t.ry(10) + 10, 'inertia 22.25', GR, 120), TA + 1.8)
    return finish(f, t.ry(12) + 26)

# ---------- 4.1 Elbow ----------
def fig_elbow():
    f = Anim('km7-', 720, 0, 'The twelve points are clustered with k = 1, 2, 3, 4, 5 and 6 in turn; for each k the points '
             'recolour, the centroids appear, and the inertia is plotted as the next point of a curve: 170.6, 90.2, 22.2, '
             '18, 13.8, 10.7. The curve drops steeply until k = 3 and flattens after it: the elbow is ringed at k = 3.',
             'RUN k = 1 … 6 · PLOT INERTIA · PICK THE BEND')
    pl = Plane(30, 262, 21)
    f.static(pl.grid(0, 10, 0, 10, 2, labels=False))
    for i in range(12): f.static(pdot(*pl(*P[i]), r=5))
    X0, X1, Y0, Y1 = 330, 690, 262, 40
    XK = lambda k: X0 + (k - 1) * (X1 - X0) / 5
    YV = lambda v: Y0 - v / 180 * (Y0 - Y1)
    f.static(L(X0 - 14, Y0, X1 + 10, Y0, RULE_HI, 1.3) + L(X0 - 14, Y0, X0 - 14, Y1, RULE_HI, 1.3))
    for k in range(1, 7): f.static(T(XK(k), Y0 + 16, str(k), FA, mono=True))
    for v in (0, 50, 100, 150): f.static(T(X0 - 20, YV(v) + 4, str(v), FA, 'end', mono=True) + L(X0 - 14, YV(v), X1 + 10, YV(v), RULE, 1))
    f.static(M(X1 + 10, Y0 + 34, '{k}', MU, 'end') + S(X0 - 14, Y1 - 12, 'inertia', MU))
    TK = [.6 + n * 1.7 for n in range(6)] + [11.2]
    seq = list(range(1, 7)) + [3]
    for n, k in enumerate(seq):
        I, a, C = BEST[k]; t0 = TK[n]; nxt = TK[n + 1] if n + 1 < len(TK) else None
        s = ''.join(pdot(*pl(*P[i]), CC[a[i]], 5) for i in range(12))
        s += ''.join(cmark(*pl(*c), CC[j], s=7) for j, c in enumerate(C))
        s += S(30, 290, 'k = %d' % k, TX, bold=True)
        f.show(s, t0, hide=nxt)
        if n < 6:
            x, y = XK(k), YV(I)
            if k > 1: f.show(L(XK(k - 1), YV(BEST[k - 1][0]), x, y, FI, 2), t0 + .6)
            f.show('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s"/>' % (x, y, FI) +
                   T(x + 8, y - 8, fmt(round(I, 1)), MU, 'start', mono=True), t0 + .8)
    f.show(ring(XK(3), YV(ELB[2]), GR, 11) + S(XK(3) + 14, YV(ELB[2]) + 26, 'elbow: k = 3', GR, bold=True), TK[6])
    return finish(f, 300)

# ---------- 4.2 Silhouette ----------
def fig_sil():
    f = Anim('km8-', 720, 0, 'In the 3-cluster split, point C is joined to the other points of its own cluster, mean distance '
             'a = 2.49, and to the points of the nearest other cluster, mean distance b = 4.87; its silhouette is (b − a) / '
             'max(a, b) = 0.49. Averaging this over all twelve points for each k gives bars 0.43, 0.62, 0.46, 0.34 and 0.20 '
             'for k = 2 to 6; the tallest, k = 3, is marked.', 'NEAR MY OWN CLUSTER, FAR FROM THE NEXT ONE · AVERAGE OVER POINTS')
    pl = Plane(30, 262, 21)
    f.static(pl.grid(0, 10, 0, 10, 2, labels=False))
    cx, cy = pl(*P[SC])
    for j in OWN: f.show(L(cx, cy, *pl(*P[j]), CC[FINAL_A[SC]], 1.6), .6 + .2 * OWN.index(j))
    for j in OTH[NB]: f.show(L(cx, cy, *pl(*P[j]), CC[NB], 1.3, '4 3'), 2.0 + .2 * OTH[NB].index(j))
    for i in range(12):
        f.static(pdot(*pl(*P[i]), CC[FINAL_A[i]], 5) + T(pl(*P[i])[0] + 7, pl(*P[i])[1] - 6, IDS[i], FA, 'start', mono=True))
    f.static(ring(cx, cy, AM, 10))
    X = 260
    f.show(M(X, 60, '{a} = %.2f' % SA, CC[FINAL_A[SC]], 'start') + S(X + 66, 60, 'mean to own cluster', MU), 1.4)
    f.show(M(X, 84, '{b} = %.2f' % SB, CC[NB], 'start') + S(X + 66, 84, 'mean to nearest other', MU), 2.9)
    f.show(M(X, 112, '{s} = (%.2f − %.2f) / %.2f = %.2f' % (SB, SA, SB, SS), AM, 'start'), 3.6)
    B0, BX, BW = 262, 470, 40
    f.static(L(BX - 10, B0, 712, B0, RULE_HI, 1.3))
    f.show(S(BX - 10, 150, 'mean s over the 12 points', MU), 4.4)
    for n, k in enumerate(range(2, 7)):
        v = SILK[k]; h = v * 150; x = BX + n * 48
        good = k == 3
        f.show(R(x, B0 - h, BW, h, tc(GR if good else FI, '.30'), GR if good else FI, 2, 1.3) +
               T(x + BW / 2, B0 - h - 6, '%.2f' % v, GR if good else MU, mono=True, bold=good) +
               T(x + BW / 2, B0 + 16, 'k=%d' % k, FA, mono=True), 4.8 + n * .5)
    f.show(S(BX + 48 + BW / 2, 304, 'best: k = 3', GR, 'middle', bold=True), 7.6)
    return finish(f, 312)

# ---------- 5 assumptions ----------
def recolor_fig(pre, aria, capt, X, true, got, cen, plx, notes, bad=(), xmax=10, sc=24):
    f = Anim(pre, 720, 0, aria, capt)
    pl = Plane(40, 292, sc)
    f.static(pl.grid(0, xmax, 0, 10, 2, xl='{x}₁', yl='{x}₂'))
    for i, p in enumerate(X):
        f.show(pdot(*pl(*p), CC[true[i]]), .3 + i * .02, hide=2.4 + i * .06)
        f.show(pdot(*pl(*p), CC[got[i]]), 2.4 + i * .06)
    f.show(S(plx, 60, 'true groups', TX, bold=True) + S(plx, 80, notes[0], MU), .4)
    f.show(S(plx, 120, 'k-means', TX, bold=True) + S(plx, 140, notes[1], MU), 2.2)
    for j, c in enumerate(cen): f.show(cmark(*pl(*c), CC[j]), 2.4 + len(X) * .06 + .2)
    for i in bad: f.show(ring(*pl(*X[i]), RD, 9), 4.2)
    f.show(S(plx, 186, notes[2], RD, bold=True) + S(plx, 206, notes[3], MU), 4.4)
    return f, pl

def fig_round():
    f, pl = recolor_fig('km9-', 'Two long horizontal strips of ten points each are the true groups. k-means with k = 2 ignores '
                        'them and cuts the plane into a left and a right half, because that split has a lower inertia, 71.25, '
                        'than the true one, 165.', 'LONG CLUSTERS · K-MEANS CUTS ACROSS THEM',
                        STRIP, STRUE, SA_, SCN, 330, ['two long strips, top and bottom', 'k = 2: left half | right half',
                                                       'inertia %s < %s of the true split' % (fmt(SI), 165),
                                                       'round blobs are cheaper than long ones'])
    return finish(f, 306)

def fig_size():
    f, pl = recolor_fig('km10-', 'A big cloud of fourteen points and a small group of four. k-means with k = 2 moves the boundary '
                        'into the big cloud: four of its points go to the small cluster, ringed in red, because that lowers the '
                        'inertia from 82.1 to 57.9.', 'UNEQUAL SIZES · THE BIG CLUSTER LOSES ITS EDGE',
                        UNEQ, [0] * 14 + [1] * 4, UA if UA[-1] == 1 else [1 - v for v in UA],
                        UC if UA[-1] == 1 else UC[::-1], 330,
                        ['14 points and 4 points', 'k = 2: boundary halfway between centroids',
                         '4 points of the big cloud stolen', 'inertia %s < %s of the true split' % (fmt(round(UI, 1)), fmt(round(UTRUE, 1)))],
                        bad=STOLEN)
    return finish(f, 306)

def fig_scale():
    f = Anim('km11-', 720, 0, 'Eight points with x1 in years (about 1 to 3) and x2 in dollars (300 to 2200). Drawn to the same '
             'scale, all eight sit on one vertical line and k-means splits them by x2 only: low and high. After standardising '
             'each column to mean 0 and spread 1, the points glide apart into two columns and k-means splits them by x1.',
             'DISTANCE ADDS RAW UNITS · STANDARDISE FIRST')
    X0, YB, H = 60, 280, 230
    rawy = lambda v: YB - v / 2400 * H
    zx = lambda v: X0 + 110 + v * 70
    zy = lambda v: YB - H / 2 - v * 70
    raw = f.static
    TG, TR = 3.6, 5.4
    f.show(L(X0, YB, X0, YB - H, RULE_HI, 1.3) + ''.join(T(X0 - 6, rawy(v) + 4, str(v), FA, 'end', mono=True) for v in (0, 1000, 2000)) +
           S(X0 + 8, YB - H - 6, 'x₂ in $ · x₁ in years, same scale', MU), .2, hide=TG)
    f.show(L(zx(-2), zy(0), zx(2), zy(0), RULE_HI, 1.2) + L(zx(0), zy(-1.7), zx(0), zy(1.7), RULE_HI, 1.2) +
           S(zx(2) + 6, zy(0) + 4, 'z₁', MU) + S(zx(0) + 6, zy(1.7), 'z₂', MU), TG + .4)
    for i, p in enumerate(SCL):
        fx, fy = zx(ZS[i][0]), zy(ZS[i][1])
        rx, ry = X0 + p[0] * H / 2400, rawy(p[1])
        f.path(pdot(fx, fy, CC[RAWA[i]]), [(0, rx - fx, ry - fy), (TG + .2, 0, 0)], 1.2 + i * .08, d=1.2, hide=TR + i * .06)
        f.show(pdot(fx, fy, CC[ZA[i] if ZA[0] == RAWA[0] else 1 - ZA[i]]), TR + i * .06)
    X = 420
    f.show(S(X, 60, 'raw units', TX, bold=True) + S(X, 80, 'a $ gap of 500 dwarfs a 2-year gap', MU) +
           S(X, 100, 'k-means splits by x₂ only', RD, bold=True), 1.6)
    f.show(badge(X, 128, 'standardise: (x − mean) / std'), TG - .4)
    f.show(S(X, 186, 'same units: z-scores', TX, bold=True) + S(X, 206, 'the split follows x₁, the real gap', GR, bold=True), TR + .6)
    return finish(f, 300)

def fig_outlier():
    f = Anim('km12-', 720, 0, 'The twelve points in their three clusters. A single outlier appears far to the right at (16, 2) and '
             'joins c3; c3 glides from (8.25, 2.5) to (9.8, 2.4), pulled away from its own four points.',
             'ONE OUTLIER DRAGS THE MEAN')
    pl = Plane(30, 220, 16)
    f.static(pl.grid(0, 18, 0, 10, 2, xl='{x}₁', yl='{x}₂'))
    for i in range(12): f.static(pdot(*pl(*P[i]), CC[FINAL_A[i]], 5))
    for j in range(2): f.static(cmark(*pl(*FINAL_C[j]), CC[j], 'c%d' % (j + 1), 7.5))
    ox, oy = pl(*OUT)
    f.show(pdot(ox, oy, CC[2], 5) + ring(ox, oy, RD, 10) + S(ox - 20, oy - 16, 'outlier', RD, bold=True), 1.0)
    fx, fy = pl(*OC[2]); sx, sy = pl(*FINAL_C[2])
    f.static(cmark(sx, sy, GH, None, 7.5).replace('stroke-width="2.2"', 'stroke-width="1.4" stroke-dasharray="3 2"'))
    f.path(cmark(fx, fy, CC[2], 'c3', 7.5), [(0, sx - fx, sy - fy), (2.0, 0, 0)], .3, d=1.0)
    X = 340
    f.show(S(X, 60, 'c3 = mean of I, J, K, L = (8.25, 2.5)', MU), .3)
    f.show(S(X, 86, 'add one far point:', TX, bold=True) + S(X, 106, 'mean of five = (9.8, 2.4)', RD, bold=True), 2.2)
    f.show(S(X, 140, 'the centroid now sits between', MU) + S(X, 158, 'its cluster and the outlier', MU), 2.8)
    return finish(f, 250)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Clustering</p>
  <h1>K-means <em>clustering</em></h1>
  <p class="lede">K-means splits unlabelled points into <b>k groups</b> by repeating two steps: give every point to its nearest centroid, then move every centroid to the mean of its points.</p>
</header>

<section id="kmeans-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Place k centroids; <em>assign</em> each point to the nearest, <em>move</em> each centroid to its points' mean, repeat until nothing changes.</p>
{km1}
  <ul class="why">
    <li>No labels: the clusters are whatever the two steps settle on, and <span class="mth"><var>k</var></span> is chosen by you.</li>
    <li>Every round lowers the same score, <b>inertia</b>, so the loop always stops — usually after a handful of rounds.</li>
  </ul>
</section>

<section id="kmeans-s2" class="lesson">
  <div class="sh"><b>02</b><h2>The loop</h2></div>
  <p class="key">Two steps, each one <em>lowers inertia</em> while the other is held fixed.</p>
  <div class="subsec" id="kmeans-s2-1">
    <h3 class="ssh"><b>2.1</b>Assign step</h3>
    <p class="skey">Each point goes to the centroid with the <em>smallest squared distance</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>c</var>(<var>x</var>)</span><em>cluster of point x</em></span>
      <span class="op">=</span>
      <span class="t b"><span><b class="fn">argmin</b><sub><var>j</var></sub> ‖<var>x</var> − <var>μ</var><sub><var>j</var></sub>‖<sup>2</sup></span><em>nearest centroid μ<sub>j</sub></em></span>
    </div>
  </div>
{km2}
    <ul class="why">
      <li>A point can <b>switch cluster</b> when the centroids move: H goes from c2 to c1 in round 2.</li>
      <li>Euclidean distance, so every column counts in its own units — see 5.3.</li>
    </ul>
  </div>
  <div class="subsec" id="kmeans-s2-2">
    <h3 class="ssh"><b>2.2</b>Update step</h3>
    <p class="skey">Each centroid moves to the <em>mean</em> of the points assigned to it.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>μ</var><sub><var>j</var></sub></span><em>new centroid</em></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i>1</i><i>|<var>C</var><sub><var>j</var></sub>|</i></span> Σ<sub><var>x</var> ∈ <var>C</var><sub><var>j</var></sub></sub> <var>x</var></span><em>mean of its points</em></span>
    </div>
  </div>
{km3}
    <ul class="why">
      <li>The mean is the point with the smallest sum of squared distances to the group — that is why this step lowers inertia.</li>
      <li><b>Mini-batch k-means</b> runs the same update on a small random batch per step: much faster on millions of rows, slightly worse inertia.</li>
    </ul>
  </div>
  <div class="subsec" id="kmeans-s2-3">
    <h3 class="ssh"><b>2.3</b>Inertia</h3>
    <p class="skey">The score k-means minimises: <em>squared distance of every point to its own centroid</em>, summed.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">WCSS</b></span><em>inertia</em></span>
      <span class="op">=</span>
      <span class="t b"><span>Σ<sub><var>j</var>=1</sub><sup><var>k</var></sup> Σ<sub><var>x</var> ∈ <var>C</var><sub><var>j</var></sub></sub> ‖<var>x</var> − <var>μ</var><sub><var>j</var></sub>‖<sup>2</sup></span><em>within-cluster sum of squares</em></span>
    </div>
  </div>
{km4}
    <ul class="why">
      <li>It can only go down, so the loop stops when an assign step changes nothing (<code>inertia_</code> in scikit-learn).</li>
      <li>It always falls as <span class="mth"><var>k</var></span> grows, so it cannot choose <span class="mth"><var>k</var></span> by itself — section 4.</li>
    </ul>
  </div>
</section>

<section id="kmeans-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Initialisation</h2></div>
  <p class="key">The loop only goes downhill, so <em>where it starts</em> decides which minimum it ends in.</p>
  <div class="subsec" id="kmeans-s3-1">
    <h3 class="ssh"><b>3.1</b>Random init</h3>
    <p class="skey">k random points as centroids: two can land in <em>one group</em>, and the loop never repairs it.</p>
{km5}
    <ul class="why">
      <li>A <b>local minimum</b>: every single assign or update step would raise inertia, yet a better split exists.</li>
      <li><code>n_init</code> runs the whole loop several times from different starts and keeps the lowest inertia.</li>
    </ul>
  </div>
  <div class="subsec" id="kmeans-s3-2">
    <h3 class="ssh"><b>3.2</b>k-means++</h3>
    <p class="skey">Pick the first centroid at random, each next one with probability <em>∝ D²</em>, its squared distance to the nearest chosen centroid.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>p</var>(<var>x</var>)</span><em>chance x is the next centroid</em></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i><var>D</var>(<var>x</var>)<sup>2</sup></i><i>Σ<sub><var>x′</var></sub> <var>D</var>(<var>x′</var>)<sup>2</sup></i></span></span><em>far points are likely</em></span>
    </div>
  </div>
{km6}
    <ul class="why">
      <li>Spreads the starts over the groups, so the loop usually begins near the best split; it is scikit-learn's default <code>init="k-means++"</code>.</li>
      <li>Still random: keep <code>n_init</code> above 1 and fix <code>random_state</code> to reproduce a run.</li>
    </ul>
  </div>
</section>

<section id="kmeans-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Choosing k</h2></div>
  <p class="key">Run k-means for several <span class="mth"><var>k</var></span> and score each split; the score must <em>not</em> reward more clusters by itself.</p>
  <div class="subsec" id="kmeans-s4-1">
    <h3 class="ssh"><b>4.1</b>Elbow</h3>
    <p class="skey">Plot inertia against <span class="mth"><var>k</var></span>; pick the <em>bend</em> where adding a cluster stops paying off.</p>
{km7}
    <ul class="why">
      <li>Inertia keeps falling to 0 at <span class="mth"><var>k</var> = <var>n</var></span>; only the change in slope matters.</li>
      <li>On real data the bend is often soft — confirm it with the silhouette.</li>
    </ul>
  </div>
  <div class="subsec" id="kmeans-s4-2">
    <h3 class="ssh"><b>4.2</b>Silhouette</h3>
    <p class="skey">For each point compare <em>a</em>, mean distance to its own cluster, with <em>b</em>, mean distance to the nearest other cluster.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>s</var>(<var>x</var>)</span><em>from −1 to 1</em></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i><var>b</var> − <var>a</var></i><i><b class="fn">max</b>(<var>a</var>, <var>b</var>)</i></span></span><em>1 = well inside, 0 = on a border, &lt; 0 = wrong cluster</em></span>
    </div>
  </div>
{km8}
    <ul class="why">
      <li>Pick the <span class="mth"><var>k</var></span> with the highest mean <span class="mth"><var>s</var></span> (<code>silhouette_score</code>); it does not grow with <span class="mth"><var>k</var></span>.</li>
      <li>Costs all pairwise distances, so on large data score a sample.</li>
    </ul>
  </div>
</section>

<section id="kmeans-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Hidden assumptions</h2></div>
  <p class="key">K-means never raises an error: when its assumptions fail it still returns a <em>confident wrong split</em>.</p>
  <div class="subsec" id="kmeans-s5-1">
    <h3 class="ssh"><b>5.1</b>Round clusters</h3>
    <p class="skey">Inertia favours <em>compact, round</em> groups, so long or curved clusters get cut across.</p>
{km9}
    <ul class="why">
      <li>Every boundary is a straight line halfway between two centroids; rings, moons and strips cannot be drawn with them.</li>
      <li>For arbitrary shapes use <a href="../dbscan/index.html">DBSCAN</a>; for stretched ellipses a Gaussian mixture.</li>
    </ul>
  </div>
  <div class="subsec" id="kmeans-s5-2">
    <h3 class="ssh"><b>5.2</b>Equal sizes</h3>
    <p class="skey">The boundary sits <em>halfway between centroids</em>, whatever the cluster sizes, so a big cluster loses its edge.</p>
{km10}
    <ul class="why">
      <li>Moving a few points from a wide cluster to a tight one lowers inertia, so the loop does it.</li>
    </ul>
  </div>
  <div class="subsec" id="kmeans-s5-3">
    <h3 class="ssh"><b>5.3</b>Feature scale</h3>
    <p class="skey">Distance adds raw units, so the column with the <em>largest numbers</em> decides the clusters.</p>
{km11}
    <ul class="why">
      <li>Put <code>StandardScaler</code> before <code>KMeans</code> in a pipeline, exactly as for <a href="../../05-classical-ml/knn/index.html">KNN</a>.</li>
      <li>With many columns distances crowd together; reduce with <a href="../../08-dimensionality/pca-dimensionality/index.html">PCA</a> first.</li>
    </ul>
  </div>
  <div class="subsec" id="kmeans-s5-4">
    <h3 class="ssh"><b>5.4</b>Outliers</h3>
    <p class="skey">Every point must join a cluster, and the mean <em>follows</em> a far point.</p>
{km12}
    <ul class="why">
      <li>Remove outliers first, or use k-medoids (a real point as centre) or <a href="../dbscan/index.html">DBSCAN</a>, which labels them noise.</li>
    </ul>
  </div>
</section>

<script>
/* Figures start when first scrolled into view, play once and hold their final state. Click a figure to replay. */
(function () {
  if (!window.IntersectionObserver || !document.getAnimations) return;
  var svgs = [].slice.call(document.querySelectorAll("figure svg[data-anim]"));
  if (!svgs.length) return;
  function anims(s) {
    return document.getAnimations().filter(function (a) { var t = a.effect && a.effect.target; return t && s.contains(t); });
  }
  function restart(s) { anims(s).forEach(function (a) { a.currentTime = 0; a.play(); }); }
  svgs.forEach(function (s) { anims(s).forEach(function (a) { a.pause(); a.currentTime = 0; }); });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting || e.target.__played) return;
      e.target.__played = true; restart(e.target); io.unobserve(e.target);
    });
  }, { threshold: 0.4 });
  svgs.forEach(function (s) {
    io.observe(s); s.style.cursor = "pointer";
    s.addEventListener("click", function () { restart(s); });
  });
})();
</script>

<footer>Machine learning · Clustering · for clusters of any shape and for noise go next to <a href="../dbscan/index.html">DBSCAN</a>; the map of the families is in <a href="../clustering-overview/index.html">Clustering overview</a>.</footer>
'''

def build():
    figs = dict(km1=fig_mental(), km2=fig_assign(), km3=fig_update(), km4=fig_inertia(), km5=fig_random(), km6=fig_pp(),
                km7=fig_elbow(), km8=fig_sil(), km9=fig_round(), km10=fig_size(), km11=fig_scale(), km12=fig_outlier())
    return re.sub(r'\{(km\d+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'Assign every point to its nearest centroid, move every centroid to the mean, repeat: inertia, '
           'k-means++ starts, the elbow and silhouette for k, and the four assumptions that make it split wrongly.')
