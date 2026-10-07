# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/07-clustering/dbscan.
Fourteen points (a curved cluster A-G, a blob H-L, two lonely points M N), eps = 1.6, min_samples = 4.
A pure-Python DBSCAN computes every count, type, join order and k-distance shown; all pinned with assert.
Run: python3 dbscan.py"""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, VI, FI, RO, GH, RULE, BG, tn, M, S, chip, dot,
                            poly, finish)
from tablefig import AM, GR, tint, pill
from decision_tree import HL, splice, BODY as DT_BODY

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/07-clustering/dbscan/index.html')
SCRIPT = re.search(r'<script>.*?</script>', DT_BODY, re.S).group(0)

# ---------- data ----------
ARC = [(round(3.5 + 2.0 * math.cos(math.radians(205 - k * 22)), 1), round(3.0 + 2.0 * math.sin(math.radians(205 - k * 22)), 1))
       for k in range(7)]
BLOB = [(7.0, 6.0), (7.8, 6.2), (7.2, 6.8), (7.9, 7.0), (9.2, 7.4)]
NOISE = [(1.4, 7.6), (5.2, 8.4)]
P = ARC + BLOB + NOISE
IDS = 'ABCDEFGHIJKLMN'
EPS, MS = 1.6, 4
assert ARC == [(1.7, 2.2), (1.5, 2.9), (1.6, 3.7), (2.0, 4.3), (2.6, 4.8), (3.3, 5.0), (4.1, 4.9)]

def nbrs(Pt, eps):
    return [[j for j in range(len(Pt)) if math.dist(Pt[i], Pt[j]) <= eps] for i in range(len(Pt))]

def dbscan(Pt, eps, ms):
    """-> labels (None = noise), core flags, join events [(cluster, point, parent)], spread order of cores"""
    nb = nbrs(Pt, eps); core = [len(x) >= ms for x in nb]; lab = [None] * len(Pt); ev = []; spread = []; c = 0
    for i in range(len(Pt)):
        if lab[i] is not None or not core[i]: continue
        lab[i] = c; ev.append((c, i, None)); q = [i]
        while q:
            p = q.pop(0)
            if not core[p]: continue
            spread.append(p)
            for j in nb[p]:
                if lab[j] is None: lab[j] = c; ev.append((c, j, p)); q.append(j)
        c += 1
    return lab, core, ev, spread

NB = nbrs(P, EPS)
LAB, CORE, EV, SPREAD = dbscan(P, EPS, MS)
CNT = [len(x) for x in NB]
TYPE = ['core' if CORE[i] else ('border' if LAB[i] is not None else 'noise') for i in range(14)]
assert CNT == [3, 4, 5, 5, 5, 4, 3, 4, 4, 4, 5, 2, 1, 1]
assert ''.join(t[0] for t in TYPE) == 'bccccccbccccbnn'[:0] + 'bcccccbccccbnn'
assert LAB == [0] * 7 + [1] * 5 + [None, None]
BORDER_CORE = {i: min((j for j in NB[i] if CORE[j]), key=lambda j: math.dist(P[i], P[j])) for i in range(14) if TYPE[i] == 'border'}
assert {IDS[k]: IDS[v] for k, v in BORDER_CORE.items()} == {'A': 'B', 'G': 'F', 'L': 'K'}
assert [(IDS[p], IDS[q] if q is not None else '-') for _, p, q in EV] == [
    ('B', '-'), ('A', 'B'), ('C', 'B'), ('D', 'B'), ('E', 'C'), ('F', 'D'), ('G', 'E'),
    ('H', '-'), ('I', 'H'), ('J', 'H'), ('K', 'H'), ('L', 'K')]
assert ''.join(IDS[s] for s in SPREAD) == 'BCDEFHIJK'

# k-distance: distance to the 4th nearest point, the point itself counted (as sklearn does for min_samples)
KD = [sorted(math.dist(p, q) for q in P)[MS - 1] for p in P]
KS = sorted(range(14), key=lambda i: (KD[i], i))
assert [round(KD[i], 2) for i in KS] == [.85, .85, 1.35, 1.35, 1.48, 1.48, 1.49, 1.49, 1.49, 2.09, 2.12, 2.18, 3.04, 3.35]
assert ''.join(IDS[i] for i in KS[9:]) == 'LAGNM'
# min_samples sweep at eps 1.6
SWEEP = {}
for m in (2, 3, 4, 5, 6):
    lb, co, _, _ = dbscan(P, EPS, m)
    SWEEP[m] = ['core' if co[i] else ('border' if lb[i] is not None else 'noise') for i in range(14)]
    SWEEP[m] = (SWEEP[m], len(set(x for x in lb if x is not None)), lb.count(None))
assert [(sum(t == 'core' for t in SWEEP[m][0]), SWEEP[m][1], SWEEP[m][2]) for m in (2, 3, 4, 5, 6)] == [
    (12, 2, 2), (11, 2, 2), (9, 2, 2), (4, 2, 2), (0, 0, 14)]

# different densities: two tight grids, one loose grid
D1 = [(1.0 + .5 * (i % 3), 3.0 + .5 * (i // 3)) for i in range(9)]
D2 = [(3.2 + .5 * (i % 3), 3.0 + .5 * (i // 3)) for i in range(9)]
SP = [(6.6 + 1.5 * (i % 3), 2.0 + 1.5 * (i // 3)) for i in range(9)]
DQ = D1 + D2 + SP
DEN = {e: dbscan(DQ, e, MS)[0] for e in (.6, 1.6)}
assert DEN[.6] == [0] * 9 + [1] * 9 + [None] * 9
assert DEN[1.6] == [0] * 18 + [1] * 9
assert round(min(math.dist(p, q) for p in D1 for q in D2), 2) == 1.2

# ---------- drawing ----------
CC = [FI, VI]                 # cluster colours
SC = 42
def PX(x): return (x - 1.0) * SC + 10
def PY(y): return 64 + (8.6 - y) * SC

def lpos(i):
    """label spot pushed away from the cluster, so edges never cross it"""
    x, y = PX(P[i][0]), PY(P[i][1])
    if i < 7:
        a = math.atan2(P[i][1] - 3.0, P[i][0] - 3.5); return x + 15 * math.cos(a), y - 15 * math.sin(a) + 4, 'middle'
    o = {7: (-12, 14, 'end'), 8: (10, 16, 'start'), 9: (-11, -6, 'end'), 10: (6, -10, 'start'), 11: (10, -8, 'start')}.get(i, (9, -7, 'start'))
    return x + o[0], y + o[1], o[2]

def lab(i, c):
    x, y, a = lpos(i); return T(x, y, IDS[i], c, a, bold=True)

def neutral(i):
    x, y = PX(P[i][0]), PY(P[i][1])
    return dot(x, y, BG, 5, MU) + lab(i, MU)

def typed(i, kind, c=FI):
    x, y = PX(P[i][0]), PY(P[i][1])
    if kind == 'core': s = dot(x, y, c, 6.5, BG)
    elif kind == 'border': s = dot(x, y, BG, 6.5) + '<circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x, y, BG, c)
    else: s = dot(x, y, BG, 6.5) + dot(x, y, GH, 5)
    return s + lab(i, c if kind != 'noise' else FA)

def ring(i, eps=EPS, c=HL):
    x, y = PX(P[i][0]), PY(P[i][1])
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="1.6" stroke-dasharray="5 4"/>'
            % (x, y, eps * SC, 'rgba(var(--blue-a),.05)', c) + dot(x, y, c, 2))

def glide(f, pts, t0, d=.4, hide=None):
    """eps circle drawn at the first point, gliding to the next ones at the given times"""
    i0 = pts[0][1]
    f.path(ring(i0), [(0, 0, 0)] + [(t, PX(P[i][0]) - PX(P[i0][0]), PY(P[i][1]) - PY(P[i0][1])) for t, i in pts[1:]],
           t0, d=d, hide=hide)

class Tab:
    def __init__(s, x, y, cols, step=21, rh=18):
        s.x, s.y, s.cols, s.step, s.rh = x, y, cols, step, rh; s.w = sum(c[1] for c in cols); s.r0 = y + 12
    def cx(s, j): return s.x + sum(c[1] for c in s.cols[:j]) + s.cols[j][1] / 2
    def colx(s, j): return s.x + sum(c[1] for c in s.cols[:j])
    def ry(s, i): return s.r0 + i * s.step
    def head(s):
        return ''.join(T(s.cx(j), s.y, c[0], MU) for j, c in enumerate(s.cols)) + L(s.x, s.y + 6, s.x + s.w, s.y + 6)
    def row(s, i, vals, colors=None):
        y = s.ry(i); o = R(s.x, y, s.w, s.rh, BG, RULE_HI, 3, 1)
        return o + ''.join(T(s.cx(j), y + 13, v, (colors or {}).get(j, TX), mono=j > 0) for j, v in enumerate(vals))
    def cell(s, i, j, v, c=TX, fill=None):
        x, y, w = s.colx(j) + 2, s.ry(i) + 2, s.cols[j][1] - 4
        o = R(x, y, w, s.rh - 4, BG, 'none', 2)
        if fill: o += R(x, y, w, s.rh - 4, fill, 'none', 2)
        return o + T(s.cx(j), s.ry(i) + 13, v, c, bold=True)
    def outline(s, i, c=AM):
        return R(s.x - 2, s.ry(i) - 2, s.w + 4, s.rh + 4, 'none', c, 4, 1.6)

TC = {'core': FI, 'border': FI, 'noise': FA}
def tcell(t, i, kind):
    return t.cell(i, 4, kind, TC[kind], tn(FI, '.14') if kind == 'core' else None)

def ptable(x=430):
    return Tab(x, 40, [('id', 30), ('x', 38), ('y', 38), ('nbrs', 46), ('type', 64)])

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('db1-', 700, 0, 'Fourteen points. A dashed circle of radius eps around D holds five points: crowded. A circle '
             'around M holds only M: alone. Crowded points connect through their circles: the curved run A to G becomes '
             'cluster 1, the blob H to L cluster 2, and M and N stay grey as noise. No number of clusters was given.',
             'DRAW A CIRCLE OF RADIUS eps · CROWDED CIRCLES CHAIN INTO A CLUSTER')
    for i in range(14): f.static(neutral(i))
    D, Mi = IDS.index('D'), IDS.index('M')
    f.show(ring(D), .6, hide=3.0)
    f.show(S(430, 80, 'circle around D: 5 points inside', FI, bold=True) + S(430, 98, '≥ min_samples 4 → crowded', MU), 1.0)
    f.show(ring(Mi, c=RO), 2.0, hide=3.6)
    f.show(S(430, 130, 'circle around M: only M', RO, bold=True) + S(430, 148, '→ alone', MU), 2.4)
    t = 3.8; end = {}
    for c, p, q in EV:
        if q is not None: f.show(L(PX(P[q][0]), PY(P[q][1]), PX(P[p][0]), PY(P[p][1]), CC[c], 1.6), t)
        t += .32; end[c] = t
        if p == 6: t += .5
    for c, p, q in EV: f.show(typed(p, TYPE[p], CC[c]), end[c] - (.32 * (7 if c == 0 else 5)) + .32 * [e[1] for e in EV if e[0] == c].index(p) + .1)
    f.show(typed(12, 'noise') + typed(13, 'noise'), t + .3)
    y0 = 210
    f.show(chip(525, y0, 'cluster 1 · 7 points · curved', FI, 190, False), end[0] + .2)
    f.show(chip(525, y0 + 34, 'cluster 2 · 5 points', VI, 190, False), end[1] + .2)
    f.show(pill(525, y0 + 68 - 10, 'noise · M, N', None, 190), t + .6)
    f.show(S(430, y0 + 112, 'eps = 1.6 · min_samples = 4 · no k given', MU), t + 1.0)
    assert CNT[D] == 5 and CNT[Mi] == 1
    return finish(f, 376)

# ---------- 2.x point types ----------
def fig_types(kind):
    pre = {'core': 'db2-', 'border': 'db3-', 'noise': 'db4-'}[kind]
    t = ptable()
    aria = {'core': 'The eps circle glides over all fourteen points. At each one the number of points inside, itself '
                    'included, is written into the neighbours column. Nine points reach 4 or more and are marked core: '
                    'B to F and H to K.',
            'border': 'The nine core points are already marked. The circle visits the remaining points A, G and L: each '
                      'circle contains a core point (B, F and K), so each becomes border.',
            'noise': 'Core and border points are marked. The circle visits M and N: neither circle contains any other '
                     'point, let alone a core point, so both become noise.'}[kind]
    capn = {'core': 'COUNT THE POINTS IN EACH CIRCLE · 4 OR MORE → CORE',
            'border': 'NOT CORE, BUT A CORE POINT IS INSIDE ITS CIRCLE → BORDER',
            'noise': 'NOT CORE, NO CORE POINT INSIDE ITS CIRCLE → NOISE'}[kind]
    f = Anim(pre, 700, 0, aria, capn)
    f.static(t.head())
    order = ['core', 'border', 'noise'].index(kind)
    for i in range(14):
        known = order > ['core', 'border', 'noise'].index(TYPE[i])
        f.static(t.row(i, [IDS[i], '%.1f' % P[i][0], '%.1f' % P[i][1], str(CNT[i]) if order else '', TYPE[i] if known else ''],
                       colors={4: TC[TYPE[i]]}))
        f.static(typed(i, TYPE[i]) if known else neutral(i))
    if kind == 'core':
        visit = list(range(14)); t0, dt = .5, .5
    else:
        visit = [i for i in range(14) if TYPE[i] == kind]; t0, dt = .5, 1.6
    glide(f, [(t0 + k * dt, i) for k, i in enumerate(visit)], t0 - .2, hide=t0 + len(visit) * dt + .2)
    for k, i in enumerate(visit):
        tk = t0 + k * dt + .45
        f.show(t.outline(i), tk - .1, hide=tk + dt - .15)
        if kind == 'core':
            dx, dy = PX(P[i][0]) - t.cx(3), PY(P[i][1]) + 20 - (t.ry(i) + 9)
            f.path(t.cell(i, 3, str(CNT[i]), FI if CNT[i] >= MS else TX), [(0, dx, dy), (tk + .15, 0, 0)], tk - .05, d=.35)
            if CORE[i]:
                f.show(tcell(t, i, 'core'), tk + .5); f.show(typed(i, 'core'), tk + .5)
        else:
            if kind == 'border':
                j = BORDER_CORE[i]
                f.show(L(PX(P[i][0]), PY(P[i][1]), PX(P[j][0]), PY(P[j][1]), FI, 2), tk + .2)
                f.show(typed(j, 'core'), tk + .2)
                f.show(S(t.x + t.w + 8, t.ry(i) + 13, 'core %s inside' % IDS[j], FI), tk + .4)
            else:
                f.show(S(t.x + t.w + 8, t.ry(i) + 13, 'nothing inside', FA), tk + .4)
                assert CNT[i] == 1
            f.show(tcell(t, i, kind), tk + .8); f.show(typed(i, kind), tk + .8)
    if kind == 'core':
        assert sum(CORE) == 9
    return finish(f, t.ry(13) + t.rh + 8)

# ---------- 03 Expansion ----------
def fig_expand():
    f = Anim('db5-', 700, 0, 'All points start grey with their types known. Take the first unvisited core point, B: it '
             'becomes cluster 1 and its circle pulls in A, C and D. C pulls in E, D pulls in F, E pulls in G. A and G are '
             'border: they join but their circles are not used. No core point is left unvisited in that region, so the next '
             'unvisited core, H, starts cluster 2: I, J and K join, K pulls in L. M and N are never reached and stay noise.',
             'START AT AN UNVISITED CORE · SPREAD THROUGH CORE CIRCLES · BORDER JOINS BUT STOPS')
    t = Tab(430, 40, [('#', 26), ('id', 30), ('from', 44), ('type', 56), ('cluster', 56)])
    f.static(t.head())
    for i in range(14): f.static(neutral(i))
    # time slots follow the BFS: each spread core gets one slot, its joins happen in that slot
    times, first, tm = {}, {}, .6
    for k, (c, p, q) in enumerate(EV):
        if q is None: tm += .5; times[k] = tm; tm += .5
    tm = .6; k = 0
    for s_ in SPREAD:
        if EV[k][1] == s_ and EV[k][2] is None: tm += .5; times[k] = tm; tm += .4; k += 1
        first[s_] = tm; tm += .45
        while k < len(EV) and EV[k][2] == s_: times[k] = tm; tm += .35; k += 1
        tm += .15
    assert k == len(EV)
    for c in (0, 1):
        cores = [x for x in SPREAD if LAB[x] == c]
        last = max(times[j] for j, e in enumerate(EV) if e[0] == c)
        f.path(ring(cores[0], c=CC[c]), [(0, 0, 0)] + [(first[x] - .4, PX(P[x][0]) - PX(P[cores[0]][0]), PY(P[x][1]) - PY(P[cores[0]][1]))
                                                         for x in cores[1:]], first[cores[0]] - .3, d=.4, hide=last + .5)
    for k, (c, p, q) in enumerate(EV):
        tk = times[k]
        if q is not None:
            f.show(L(PX(P[q][0]), PY(P[q][1]), PX(P[p][0]), PY(P[p][1]), CC[c], 2), tk)
        f.show(typed(p, TYPE[p], CC[c]), tk + .1)
        f.show(t.row(k, [str(k + 1), IDS[p], IDS[q] if q is not None else 'start', TYPE[p], str(c + 1)],
                     colors={1: CC[c], 3: CC[c] if TYPE[p] == 'core' else MU, 4: CC[c]}), tk + .1)
    # redraw join points on top of the edges at the very end so dots sit above the lines
    for k, (c, p, q) in enumerate(EV): f.show(typed(p, TYPE[p], CC[c]), tm + .1)
    f.show(typed(12, 'noise') + typed(13, 'noise'), tm + .3)
    f.show(S(t.x, t.ry(12) + 22, 'M, N never reached → noise', FA, bold=True), tm + .5)
    return finish(f, max(376, t.ry(12) + 30))

# ---------- 4.1 eps: k-distance plot ----------
def fig_kdist():
    f = Anim('db6-', 700, 0, 'For every point, the distance to its 4th nearest point, itself counted, is written in a table. '
             'Each value then flies into a plot, sorted from smallest to largest: nine values stay between 0.85 and 1.49, '
             'then the curve bends up: 2.09, 2.12, 2.18 for the border points L, A, G and 3.04, 3.35 for the noise points '
             'N and M. eps is set just above the bend, at 1.6.',
             'DISTANCE TO THE 4th NEAREST POINT · SORTED · eps AT THE KNEE')
    t = Tab(0, 40, [('id', 30), ('d₄', 52)])
    f.static(t.head())
    for i in range(14): f.static(t.row(i, [IDS[i], '%.2f' % KD[i]]))
    x0, x1, yb, yt = 170, 680, 330, 50
    PXk = lambda r: x0 + 20 + r * 34
    PYk = lambda v: yb - v / 3.5 * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for v in (1, 2, 3):
        f.static(L(x0, PYk(v), x1, PYk(v), RULE, .8) + T(x0 - 7, PYk(v) + 4, str(v), FA, 'end', mono=True))
    f.static(S(x1, yb + 30, 'points sorted by d₄ →', MU, 'end') + S(x0, yt - 12, 'd₄', MU))
    for r, i in enumerate(KS):
        f.static(T(PXk(r), yb + 15, IDS[i], FA, bold=True))
        tk = .6 + r * .35
        c = FI if TYPE[i] == 'core' else (VI if TYPE[i] == 'border' else RO)
        dx, dy = t.cx(1) + 30 - PXk(r), t.ry(i) + 9 - PYk(KD[i])
        f.show(t.outline(i), tk - .15, hide=tk + .3)
        f.path(dot(PXk(r), PYk(KD[i]), c, 5, BG), [(0, dx, dy), (tk + .1, 0, 0)], tk - .1, d=.4)
    tl = .6 + 14 * .35 + .3
    f.show(poly([(PXk(r), PYk(KD[i])) for r, i in enumerate(KS)], MU, 1.4), tl)
    f.show(L(x0, PYk(EPS), x1, PYk(EPS), AM, 1.6, '6 4') + S(x0 + 6, PYk(EPS) - 6, 'eps = 1.6 · just above the knee', AM, bold=True), tl + .6)
    f.show('<circle cx="%.1f" cy="%.1f" r="12" fill="none" stroke="%s" stroke-width="1.8"/>' % (PXk(8.5), PYk(1.8), AM), tl + .9)
    f.show(S(PXk(9) - 12, PYk(2.9), 'steep: border L A G, noise N M', MU, 'end'), tl + 1.3)
    f.show(S(PXk(0) - 6, PYk(.85) + 22, 'flat: core points, neighbours close', MU), tl + 1.3)
    return finish(f, yb + 40)

# ---------- 4.2 min_samples ----------
def fig_minsamples():
    f = Anim('db7-', 700, 0, 'The fourteen points typed again at eps 1.6 for min_samples from 2 to 6. At 2, twelve points are '
             'core; at 3, eleven; at 4, nine; at 5, only four; in every case two clusters and two noise points. At 6 no '
             'point has six neighbours: no core, everything is noise. The rule of thumb gives 3 (dimensions plus one) or 4 '
             '(two times dimensions) for two-dimensional data.',
             'SAME POINTS · SAME eps · RAISE min_samples → FEWER CORE POINTS')
    X0, W = 104, 22
    for j, n in enumerate(IDS): f.static(T(X0 + j * W, 40, n, MU, bold=True))
    f.static(S(0, 40, 'min_samples', MU) + S(X0 + 14 * W + 6, 40, 'core · clusters · noise', MU))
    f.static(L(0, 48, 690, 48, RULE_HI))
    for k, m in enumerate((2, 3, 4, 5, 6)):
        y = 72 + k * 40; tk = .5 + k * 1.2; types, nc, nn = SWEEP[m]
        f.show(T(40, y + 4, str(m), TX, mono=True, bold=True) + R(0, y - 15, 690, 30, 'none', AM, 5, 1.6), tk, hide=tk + 1.1)
        f.show(T(40, y + 4, str(m), TX, mono=True, bold=True), tk)
        for j, ty in enumerate(types):
            x = X0 + j * W
            if ty == 'core': s = dot(x, y, FI, 7, BG)
            elif ty == 'border': s = '<circle cx="%.1f" cy="%.1f" r="5.5" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x, y, BG, FI)
            else: s = dot(x, y, GH, 5.5)
            f.show(s, tk + .15 + j * .04)
        f.show(T(X0 + 14 * W + 6, y + 4, '%d · %d · %d' % (sum(t == 'core' for t in types), nc, nn), RO if nc == 0 else TX,
                 'start', mono=True), tk + .8)
    for m, s in ((3, 'dim + 1'), (4, '2 · dim  ← used here')):
        k = m - 2; f.show(S(X0 + 14 * W + 104, 72 + k * 40 + 4, s, AM, bold=True), 6.6)
    y = 72 + 5 * 40
    f.static(dot(X0, y, FI, 6, BG) + S(X0 + 12, y + 4, 'core', MU) + '<circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="%s" stroke-width="2.2"/>' % (X0 + 70, y, BG, FI) +
             S(X0 + 82, y + 4, 'border', MU) + dot(X0 + 150, y, GH, 5) + S(X0 + 162, y + 4, 'noise', MU))
    return finish(f, y + 16)

# ---------- 05 Different densities ----------
def fig_density():
    f = Anim('db8-', 720, 0, 'Two tight groups 1.2 apart and one loose grid with spacing 1.5. With eps 0.6 the tight groups '
             'are two clusters but every loose point is noise. With eps 1.6 the loose grid becomes a cluster, but the two '
             'tight groups merge into one. No single eps gives three clusters.',
             'ONE eps FOR THE WHOLE DATA · TIGHT AND LOOSE CLUSTERS CANNOT BOTH FIT')
    s = 30
    for k, e in enumerate((.6, 1.6)):
        ox, oy = k * 370, 0
        X = lambda x: ox + 6 + (x - .6) * s
        Y = lambda y: oy + 200 - (y - 1.5) * s
        f.static(S(ox, 44, 'eps = %g' % e, TX, bold=True))
        for p in DQ: f.static(dot(X(p[0]), Y(p[1]), BG, 4.5, MU))
        t0 = .5 + k * 3.6
        for p, c in ((DQ[4], FI), (DQ[22], RO if e < 1 else VI)):
            f.show('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="5 4"/>'
                   % (X(p[0]), Y(p[1]), e * s, HL), t0, hide=t0 + 1.6)
        lab = DEN[e]
        for g in (0, 1, None):
            idx = [i for i, l in enumerate(lab) if l == g]
            col = GH if g is None else CC[g]
            f.show(''.join(dot(X(DQ[i][0]), Y(DQ[i][1]), BG, 6) + dot(X(DQ[i][0]), Y(DQ[i][1]), col, 4.5 if g is None else 5.5) for i in idx),
                   t0 + 1.8 + (0 if g is None else g) * .5 + (1.0 if g is None else 0))
        y = 236
        if e < 1:
            f.show(chip(ox + 60, y, 'tight: 2 clusters ✓', FI, 140, False), t0 + 2.8)
            f.show(chip(ox + 230, y, 'loose: all noise ✗', RO, 140, False), t0 + 3.0)
        else:
            f.show(chip(ox + 60, y, 'tight: merged ✗', RO, 140, False), t0 + 2.8)
            f.show(chip(ox + 230, y, 'loose: 1 cluster ✓', VI, 140, False), t0 + 3.0)
    f.show(S(0, 276, 'eps small enough to split the tight groups is too small for the loose one → HDBSCAN varies it', MU), 8.4)
    return finish(f, 290)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Clustering</p>
  <h1><em>DBSCAN</em></h1>
  <p class="lede">DBSCAN draws a circle of radius <b>eps</b> around every point and chains the crowded circles together, so a cluster takes any shape and lonely points are left out as noise.</p>
</header>

<section id="dbscan-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">A cluster is a <em>crowded region</em>: crowded points whose circles overlap belong together, whatever the shape.</p>
{db1}
  <ul class="why">
    <li>Two settings: the radius <b>eps</b> and <b>min_samples</b>, how many points make a circle crowded. The number of clusters comes out, it is not put in.</li>
    <li>The curved run is one cluster here; <a href="../kmeans-clustering/index.html">K-means</a> would cut it into round pieces and force M and N into a cluster.</li>
    <li>Used where shapes are odd and outliers matter: GPS traces, hot spots on a map, anomaly flags (label <code>-1</code>).</li>
  </ul>
</section>

<section id="dbscan-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Point types</h2></div>
  <p class="key">Count the points inside each circle; the count <em>and who is inside</em> give every point one of three types.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>N</var><sub><var>ε</var></sub>(<var>p</var>)</span><em>neighbourhood of p</em></span>
      <span class="op">=</span>
      <span class="t b"><span>{ <var>q</var> : ‖<var>p</var> − <var>q</var>‖ ≤ <var>ε</var> }</span><em>points inside the circle, p included</em></span>
    </div>
    <div class="line">
      <span class="t"><span><var>p</var> is core</span><em>crowded</em></span>
      <span class="op">⇔</span>
      <span class="t p"><span>|<var>N</var><sub><var>ε</var></sub>(<var>p</var>)| ≥ min_samples</span><em>enough points inside</em></span>
    </div>
  </div>
  <div class="subsec" id="dbscan-s2-1">
    <h3 class="ssh"><b>2.1</b>Core point</h3>
    <p class="skey">At least <em>min_samples</em> points inside its circle, itself included.</p>
{db2}
    <ul class="why">
      <li>Only core points spread a cluster; they form its dense inside.</li>
      <li>scikit-learn counts the point itself, so min_samples = 4 means the point plus three others.</li>
    </ul>
  </div>
  <div class="subsec" id="dbscan-s2-2">
    <h3 class="ssh"><b>2.2</b>Border point</h3>
    <p class="skey">Not crowded itself, but <em>a core point lies inside its circle</em>.</p>
{db3}
    <ul class="why">
      <li>Border points sit on the edge of a cluster: they belong to it but do not extend it.</li>
    </ul>
  </div>
  <div class="subsec" id="dbscan-s2-3">
    <h3 class="ssh"><b>2.3</b>Noise point</h3>
    <p class="skey">Not crowded and <em>no core point inside its circle</em>: it belongs to no cluster.</p>
{db4}
    <ul class="why">
      <li>Noise gets the label <code>-1</code> in <code>labels_</code>; DBSCAN is never forced to place every point.</li>
    </ul>
  </div>
</section>

<section id="dbscan-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Expansion</h2></div>
  <p class="key">Start at an unvisited core point and <em>spread neighbour by neighbour</em>, like a BFS; only core points pass it on.</p>
{db5}
  <ul class="why">
    <li>The chain is what lets a cluster bend: A and G are far apart but linked through B…F (<a href="../../../01-dsa/04-algorithms/graph-bfs-dfs-topo/index.html">BFS</a> over the "inside my circle" graph).</li>
    <li>A border point within reach of two clusters goes to the one that reaches it first, so it depends on the data order; core points never do.</li>
    <li>No loss is optimised and nothing is learned: there is no <code>predict</code> for new points, only <code>fit_predict</code>.</li>
  </ul>
</section>

<section id="dbscan-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Choosing the parameters</h2></div>
  <p class="key">Pick <em>min_samples</em> from the number of dimensions, then read <em>eps</em> off the data.</p>
  <div class="subsec" id="dbscan-s4-1">
    <h3 class="ssh"><b>4.1</b>eps · k-distance plot</h3>
    <p class="skey">Sort every point's distance to its k-th nearest point (k = min_samples); put eps <em>at the knee</em>.</p>
{db6}
    <ul class="why">
      <li>Flat part: points inside a cluster. Steep part: edges and outliers. The knee separates them.</li>
      <li>eps is a distance, so <b>scale the features first</b> (<code>StandardScaler</code>); otherwise the column with the largest units decides.</li>
    </ul>
  </div>
  <div class="subsec" id="dbscan-s4-2">
    <h3 class="ssh"><b>4.2</b>min_samples</h3>
    <p class="skey">Rule of thumb: at least <em>dimensions + 1</em>, often <em>2 × dimensions</em>; raise it for noisy data.</p>
{db7}
    <ul class="why">
      <li>Too small (1 or 2): every stray pair is a cluster. Too large: whole clusters drop to noise.</li>
      <li>Change min_samples and redo the k-distance plot: k follows it.</li>
    </ul>
  </div>
</section>

<section id="dbscan-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Different densities</h2></div>
  <p class="key">One eps serves the whole data set, so a <em>tight cluster and a loose cluster</em> cannot both be found.</p>
{db8}
  <ul class="why">
    <li>The same wall in high dimensions: distances bunch together and no eps separates crowded from lonely.</li>
    <li><a href="../hdbscan/index.html">HDBSCAN</a> tries every eps at once and keeps the clusters that last longest.</li>
  </ul>
</section>

''' + SCRIPT + r'''

<footer>Machine learning · Clustering · continues from <a href="../kmeans-clustering/index.html">K-means</a>; the density blind spot is fixed in <a href="../hdbscan/index.html">HDBSCAN</a>.</footer>
'''

def build():
    figs = dict(db1=fig_mental(), db2=fig_types('core'), db3=fig_types('border'), db4=fig_types('noise'),
                db5=fig_expand(), db6=fig_kdist(), db7=fig_minsamples(), db8=fig_density())
    return re.sub(r'\{(db\d+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'Draw a circle of radius eps around every point: crowded circles chain into clusters of any '
           'shape, points left alone are noise; eps is read off the k-distance plot.')
