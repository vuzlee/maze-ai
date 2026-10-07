# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/06-tree-models/lightgbm.
Every number is computed here. The mental model reuses the six customers of decision_tree.py, regression
on spend from a start of 25 (residual = spend - 25, as in xgboost.py). Everything else runs on a seeded
synthetic set of 300 customers (age 20-70, income 10-40): a pure-Python histogram GBDT with squared loss,
lambda = 0 (LightGBM's default), 10 bins per column, 100 rounds at learning rate 0.1.
Gain of a split = XGBoost's Gain with lambda = 0:  G_L^2/H_L + G_R^2/H_R - G^2/H  (h = 1 per row).
Run: python3 lightgbm.py"""
import os, re, sys, math, random, bisect
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from decision_tree import DATA, HL, layout, node_at, qbox, splice, BODY as DT_BODY
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, GH, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, finish)
from tablefig import GR, AM, tint, pill
import linear_algebra as _la
_la.RGBA.setdefault(GR, '--green-a'); _la.RGBA.setdefault(AM, '--amber-a')

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/06-tree-models/lightgbm/index.html')
POS, NEG = FI, VI          # sign of a residual: positive blue, negative violet (as in xgboost.py)

def g1(x):
    s = '%.1f' % x
    return s[:-2] if s.endswith('.0') else s
def sg(x):
    return ('+' if x > 0 else '−' if x < 0 else '') + g1(abs(x))

# =====================================================================================================
# 01 · the six customers, leaf-wise with num_leaves = 4
# =====================================================================================================
BASE = 25
assert sum(r[5] for r in DATA) / 6 == BASE
RES = {r[0]: r[5] - BASE for r in DATA}
def scan6(ids):
    """best split of a group of the six customers -> (gain, column, threshold, left ids, right ids); ties keep age"""
    out = None
    for c, name in ((1, 'age'), (2, 'income')):
        rs = sorted([r for r in DATA if r[0] in ids], key=lambda r: r[c])
        for i in range(1, len(rs)):
            Lr, Rr = rs[:i], rs[i:]
            gl, gr = sum(RES[r[0]] for r in Lr), sum(RES[r[0]] for r in Rr)
            g = gl * gl / len(Lr) + gr * gr / len(Rr) - (gl + gr) ** 2 / len(rs)
            if out is None or g > out[0] + 1e-9:
                out = (g, name, (rs[i - 1][c] + rs[i][c]) / 2, ''.join(sorted(r[0] for r in Lr)), ''.join(sorted(r[0] for r in Rr)))
    return out
def leafwise6(budget):
    leaves, rounds = ['ABCDEF'], []
    while len(leaves) < budget:
        cand = [(scan6(l), l) for l in leaves if len(l) > 1]
        (g, col, thr, a, b), l = max(cand, key=lambda c: c[0][0])
        rounds.append(([(x, scan6(x)[0] if len(x) > 1 else None) for x in leaves], l, col, thr, g))
        k = leaves.index(l); leaves[k:k + 1] = [a, b]
    return rounds, leaves
ROUNDS6, LEAVES6 = leafwise6(4)
assert [(r[1], r[2], r[3], round(r[4], 2)) for r in ROUNDS6] == [
    ('ABCDEF', 'age', 31.5, 588), ('CDEF', 'age', 56, 21.33), ('CDE', 'age', 46.5, 10.67)]
assert LEAVES6 == ['AB', 'CD', 'E', 'F'] and scan6('AB')[0] == 2
assert dict(ROUNDS6[2][0]) == {'AB': 2, 'CDE': scan6('CDE')[0], 'F': None}
LV6 = {l: sum(RES[c] for c in l) / len(l) for l in LEAVES6}
assert LV6 == {'AB': -14, 'CD': 7, 'E': 3, 'F': 11}
# level-wise with the same budget would have split A B (gain 2) before C D E
TREE6 = {'q': 'age < 31.5 ?', 'ids': 'ABCDEF', 'yes': {'leaf': 1, 'ids': 'AB'},
         'no': {'q': 'age < 56 ?', 'ids': 'CDEF',
                'yes': {'q': 'age < 46.5 ?', 'ids': 'CDE', 'yes': {'leaf': 1, 'ids': 'CD'}, 'no': {'leaf': 1, 'ids': 'E'}},
                'no': {'leaf': 1, 'ids': 'F'}}}

# =====================================================================================================
# the 300 synthetic customers
# =====================================================================================================
def make(n, seed):
    g = random.Random(seed); P = []
    for _ in range(n):
        age, inc = 20 + 50 * g.random(), 10 + 30 * g.random()
        f = 6 * math.sin(2 * math.pi * (age - 20) / 50) if inc >= 25 else 0
        P.append((age, inc, 20 + f + g.gauss(0, 1.5)))
    return P
TR, TE = make(300, 7), make(300, 8)
LO, WD, NB = (20, 10), (50, 30), 10
COLN = ('age', 'income')
def binof(p, f, B=NB): return min(max(int((p[f] - LO[f]) / WD[f] * B), 0), B - 1)
def edge(f, e, B=NB): return LO[f] + WD[f] * e / B
BTR = [(binof(p, 0), binof(p, 1)) for p in TR]
MEAN = sum(p[2] for p in TR) / len(TR)
R0 = [p[2] - MEAN for p in TR]
SSE0 = sum(r * r for r in R0)

def best(rows, r, w=None, bins=BTR, nb=(NB, NB), msl=1):
    """histogram split search: sum of g*w and of w per bin, one left-to-right pass -> (gain, column, edge)"""
    w = w or [1] * len(r)
    Gt = sum(r[i] * w[i] for i in rows); Ht = sum(w[i] for i in rows); n = len(rows); out = None
    for f in (0, 1):
        G, H, N = [0.0] * nb[f], [0.0] * nb[f], [0] * nb[f]
        for i in rows: b = bins[i][f]; G[b] += r[i] * w[i]; H[b] += w[i]; N[b] += 1
        gl = hl = 0; nl = 0
        for b in range(nb[f] - 1):
            gl += G[b]; hl += H[b]; nl += N[b]
            if nl < msl or n - nl < msl or hl == 0 or Ht - hl == 0: continue
            g = gl * gl / hl + (Gt - gl) ** 2 / (Ht - hl) - Gt * Gt / Ht
            if out is None or g > out[0] + 1e-12: out = (g, f, b + 1)
    return out

# ---------- 2.1 / 2.2 one tree, 8 leaves, level-wise vs leaf-wise ----------
def grow8(mode, budget=8):
    root = dict(rows=list(range(300)), d=0); leaves = [root]; k = 0
    while len(leaves) < budget:
        c = [(best(l['rows'], R0), l) for l in leaves]
        c = [x for x in c if x[0]]
        if mode == 'leaf':
            b, lf = max(c, key=lambda x: x[0][0])
        else:
            dm = min(l['d'] for _, l in c); b, lf = [x for x in c if x[1]['d'] == dm][0]
        g, f, e = b; k += 1
        lf.update(g=g, f=f, t=edge(f, e), order=k)
        lf['L'] = dict(rows=[i for i in lf['rows'] if BTR[i][f] < e], d=lf['d'] + 1)
        lf['R'] = dict(rows=[i for i in lf['rows'] if BTR[i][f] >= e], d=lf['d'] + 1)
        j = leaves.index(lf); leaves[j:j + 1] = [lf['L'], lf['R']]
    sse = sum(sum((R0[i] - sum(R0[j] for j in l['rows']) / len(l['rows'])) ** 2 for i in l['rows']) for l in leaves)
    return root, leaves, sse
def nodes(t, out=None):
    out = [] if out is None else out; out.append(t)
    if 'L' in t: nodes(t['L'], out); nodes(t['R'], out)
    return out
LEVEL, LEVEL_LV, LEVEL_SSE = grow8('level')
LEAF, LEAF_LV, LEAF_SSE = grow8('leaf')
def gains(t): return sorted((n['order'], round(n['g'])) for n in nodes(t) if 'g' in n)
assert round(SSE0) == 2858 and round(LEVEL_SSE) == 941 and round(LEAF_SSE) == 763
assert [g for _, g in gains(LEVEL)] == [906, 503, 326, 6, 72, 8, 97]
assert [g for _, g in gains(LEAF)] == [906, 503, 326, 97, 121, 72, 72]
assert max(l['d'] for l in LEVEL_LV) == 3 and max(l['d'] for l in LEAF_LV) == 4
assert {l['d'] for l in LEVEL_LV} == {3} and {l['d'] for l in LEAF_LV} == {2, 3, 4}
assert abs(SSE0 - sum(n['g'] for n in nodes(LEVEL) if 'g' in n) - LEVEL_SSE) < 1e-6
WASTE = 20   # level-wise splits below this gain: forced only because they sit on the same level

# ---------- 3.1 exact scan vs 10 bins, at the root ----------
def exact_best():
    out = None; Gt = sum(R0)
    for f in (0, 1):
        rs = sorted(range(300), key=lambda i: TR[i][f]); gl = 0
        for k in range(1, 300):
            gl += R0[rs[k - 1]]
            g = gl * gl / k + (Gt - gl) ** 2 / (300 - k) - Gt * Gt / 300
            if out is None or g > out[0]: out = (g, f, (TR[rs[k - 1]][f] + TR[rs[k]][f]) / 2)
    return out
EX = exact_best(); BN = best(list(range(300)), R0)
assert EX[1] == 0 and round(EX[2], 1) == 45.1 and round(EX[0]) == 918
assert BN[1] == 0 and edge(0, BN[2]) == 45 and round(BN[0]) == 906
assert len(set(p[0] for p in TR)) == 300           # 299 gaps between sorted ages
AGE_CNT = [sum(1 for b in BTR if b[0] == k) for k in range(NB)]

# ---------- 3.2 histogram subtraction on income, after the root split age < 45 ----------
def hist(rows, f=1): return [sum(1 for i in rows if BTR[i][f] == k) for k in range(NB)]
ALL = list(range(300))
OLD = [i for i in ALL if BTR[i][0] >= BN[2]]; YOUNG = [i for i in ALL if BTR[i][0] < BN[2]]
HP, HS = hist(ALL), hist(OLD); HD = [a - b for a, b in zip(HP, HS)]
assert len(OLD) == 146 and len(YOUNG) == 154 and HD == hist(YOUNG)

# ---------- 04 GOSS ----------
GA, GB = .2, .1
ORDER = sorted(ALL, key=lambda i: -abs(R0[i]))
TOP = ORDER[:int(GA * 300)]; REST = ORDER[int(GA * 300):]
SAMP = random.Random(1).sample(REST, int(GB * 300))
WGT = (1 - GA) / GB
def goss_gain(scale):
    w = [0] * 300
    for i in TOP: w[i] = 1
    for i in SAMP: w[i] = WGT if scale else 1
    return best(TOP + SAMP, R0, w)
GW, GU = goss_gain(True), goss_gain(False)
assert WGT == 8 and len(TOP) == 60 and len(SAMP) == 30
assert GW[1:] == BN[1:] and GU[1:] == BN[1:] and round(GW[0]) == 952 and round(GU[0]) == 1496

# ---------- 05 EFB: one-hot city of the six customers ----------
CITY = {'A': 'Paris', 'B': 'Rome', 'C': 'Paris', 'D': 'Oslo', 'E': 'Rome', 'F': None}
CITIES = ('Paris', 'Rome', 'Oslo')
ONEHOT = {r[0]: [int(CITY[r[0]] == c) for c in CITIES] for r in DATA}
assert all(sum(v) <= 1 for v in ONEHOT.values())       # never two non-zeros in one row: no conflict
BUNDLE = {k: sum((j + 1) * x for j, x in enumerate(v)) for k, v in ONEHOT.items()}
assert [BUNDLE[r[0]] for r in DATA] == [1, 2, 1, 3, 2, 0]

# ---------- 06 boosting runs ----------
def exact_bins():
    cuts = [sorted(set(p[f] for p in TR)) for f in (0, 1)]
    bf = lambda p, f: max(bisect.bisect_right(cuts[f], p[f]) - 1, 0)
    return bf, (len(cuts[0]), len(cuts[1]))
def boost(nl=31, msl=20, maxd=None, B=NB, rounds=100, lr=.1):
    if B is None: bf, nb = exact_bins()
    else: bf, nb = (lambda p, f: binof(p, f, B)), (B, B)
    btr = [(bf(p, 0), bf(p, 1)) for p in TR]; bte = [(bf(p, 0), bf(p, 1)) for p in TE]
    def tree(r):
        root = dict(rows=list(range(300)), d=0); leaves = [root]
        ev = lambda l: l.__setitem__('b', best(l['rows'], r, None, btr, nb, msl) if maxd is None or l['d'] < maxd else None)
        ev(root)
        while len(leaves) < nl:
            c = [l for l in leaves if l['b'] and l['b'][0] > 1e-9]
            if not c: break
            lf = max(c, key=lambda l: l['b'][0]); _, f, e = lf['b']; lf['f'], lf['e'] = f, e
            lf['L'] = dict(rows=[i for i in lf['rows'] if btr[i][f] < e], d=lf['d'] + 1)
            lf['R'] = dict(rows=[i for i in lf['rows'] if btr[i][f] >= e], d=lf['d'] + 1)
            leaves.remove(lf); leaves += [lf['L'], lf['R']]; ev(lf['L']); ev(lf['R'])
        for l in leaves: l['v'] = sum(r[i] for i in l['rows']) / len(l['rows'])
        return root, len(leaves)
    def pred(t, b):
        while 'f' in t: t = t['L'] if b[t['f']] < t['e'] else t['R']
        return t['v']
    ptr, pte, most = [MEAN] * 300, [MEAN] * 300, 0
    for _ in range(rounds):
        r = [TR[i][2] - ptr[i] for i in range(300)]
        t, k = tree(r); most = max(most, k)
        ptr = [ptr[i] + lr * pred(t, btr[i]) for i in range(300)]
        pte = [pte[i] + lr * pred(t, bte[i]) for i in range(300)]
    rm = lambda P, p: math.sqrt(sum((P[i][2] - p[i]) ** 2 for i in range(300)) / 300)
    return rm(TR, ptr), rm(TE, pte), most
r3 = lambda x: tuple(round(v, 3) for v in x[:2])
BINRUN = {B: r3(boost(B=B)) for B in (None, 10, 5)}
assert BINRUN == {None: (1.075, 1.79), 10: (1.475, 1.696), 5: (1.984, 2.159)}
NLV = [2, 4, 8, 16, 31, 64]
NLC = [boost(nl=n, msl=1) for n in NLV]
MSV = [1, 2, 5, 10, 20, 40, 80]
MSC = [boost(nl=64, msl=m) for m in MSV]
MDV = [1, 2, 3, 4, 6, 8, None]
MDC = [boost(nl=64, msl=1, maxd=d) for d in MDV]
assert [round(c[1], 3) for c in NLC] == [2.691, 1.685, 1.722, 1.799, 1.843, 1.856]
assert [round(c[1], 3) for c in MSC] == [1.856, 1.851, 1.781, 1.715, 1.696, 1.846, 2.125]
assert [round(c[1], 3) for c in MDC] == [2.691, 1.748, 1.695, 1.739, 1.858, 1.853, 1.856]
assert [c[2] for c in MDC] == [2, 4, 8, 16, 55, 64, 64]

# =====================================================================================================
# drawing
# =====================================================================================================
def grp(cx, cy, ids, c=RULE_HI, sw=1.2, fill=BG):
    """a leaf that still holds rows: a pill with the row ids"""
    s = ' '.join(ids); w = len(s) * 7.2 + 20
    return R(cx - w / 2, cy - 12, w, 24, BG, 'none', 12) + R(cx - w / 2, cy - 12, w, 24, fill, c, 12, sw) + \
        T(cx, cy + 4, s, TX, mono=True, bold=True)
def gring(cx, cy, ids, c=HL):
    s = ' '.join(ids); w = len(s) * 7.2 + 20
    return R(cx - w / 2 - 4, cy - 16, w + 8, 32, 'none', c, 15, 2)

# ---------- 01 Mental model ----------
TW = 20                                   # one customer token + gap
def tokx(n, j): return -(n * TW - 4) / 2 + j * TW + 8
def box6(x, y, ids):
    w = len(ids) * TW + 8
    return R(x - w / 2, y - 12, w, 24, BG, 'none', 12) + R(x - w / 2, y - 12, w, 24, 'var(--brand-soft)', RULE_HI, 12, 1.2)
def ring6(x, y, ids, c=HL):
    w = len(ids) * TW + 8
    return R(x - w / 2 - 4, y - 16, w + 8, 32, 'none', c, 15, 2)
def tok(cx, cy, i):
    c = POS if RES[i] > 0 else NEG
    return R(cx - 8, cy - 9, 16, 18, BG, 'none', 4) + R(cx - 8, cy - 9, 16, 18, tn(c, '.16'), c, 4, 1.2) + \
        T(cx, cy + 4, i, c, mono=True, bold=True)

def fig_mental():
    f = Anim('lgb1-', 720, 0, 'The table of six customers with their residuals, spend minus 25. Each customer slides out of the '
             'table into one root leaf. Each round every leaf shows the gain of its best split and only the leaf with the '
             'largest gain is split; its customers slide down into the two new leaves. Round 1: the only leaf, gain 588, '
             'split at age 31.5. Round 2: A B offers 2, C D E F offers 21.3, so C D E F is split at age 56. Round 3: A B '
             'offers 2, C D E offers 10.7, F is one row, so C D E is split at age 46.5. Four leaves reached, num_leaves is 4, '
             'stop. A B is never split. Leaf values, the mean residual: A B minus 14, C D plus 7, E plus 3, F plus 11.',
             'EACH ROUND · EVERY LEAF BIDS ITS BEST GAIN · ONLY THE TOP BID IS SPLIT')
    t = Table(0, 30, [('id', 30), ('age', 42), ('residual', 66)])
    f.static(t.head())
    for i, r in enumerate(DATA):
        v = RES[r[0]]
        f.static(t.row(i, [r[0], str(r[1]), sg(v)], colors={2: POS if v > 0 else NEG}))
    pos = layout(TREE6, 200, 712, 56, 76)
    pid = {node_at(TREE6, p)['ids']: p for p in pos}
    BID = [2.2, 4.2, 6.4]
    TS = {'': 3.0, 'n': 5.2, 'ny': 7.4}
    END = 8.4
    par = lambda p: p[:-1]
    # leaf containers: the root fades in, every child glides out of its parent when the parent is split
    for p, (x, y) in pos.items():
        n = node_at(TREE6, p)
        if p == '':
            f.show(box6(x, y, n['ids']), .4, hide=TS[p])
        else:
            px, py = pos[par(p)]; s0 = TS[par(p)]
            f.path(box6(x, y, n['ids']), [(0, px - x, py - y), (s0 + .35, 0, 0)], s0, d=.6, hide=TS.get(p))
        if 'q' in n:
            s0 = TS[p]
            f.show(qbox(x, y, n['q']), s0 + .35)
            for ch in 'yn':
                cx, cy = pos[p + ch]
                f.show(L(x, y + 13, cx, cy - 12, RULE_HI, 1.2) +
                       T((x + cx) / 2 + (-12 if ch == 'y' else 12), (y + cy) / 2 - 2, 'yes' if ch == 'y' else 'no', FA,
                         'end' if ch == 'y' else 'start'), s0 + .5)
    # bids under the leaves, one set per round; the winner gets a ring
    for k, (bids, win, col, thr, g) in enumerate(ROUNDS6):
        tb = BID[k]; nxt = BID[k + 1] if k + 1 < len(BID) else END
        for ids, gv in bids:
            x, y = pos[pid[ids]]
            txt = 'gain %s' % g1(gv) if gv is not None else '1 row'
            c = HL if ids == win else (FA if gv is None else MU)
            f.show(T(x, y + 28, txt, c, mono=True, bold=ids == win), tb, hide=TS[pid[win]] if ids == win else nxt)
        x, y = pos[pid[win]]
        f.show(ring6(x, y, win), tb + .5, hide=TS[pid[win]])
    # the customers: out of the table into the root, then down into the chosen leaf at every split
    for i, r in enumerate(DATA):
        c = r[0]; x0, y0 = t.x + t.w + 18, t.ry(i) + 13
        leafp_ = [p for p in pos if 'leaf' in node_at(TREE6, p) and c in node_at(TREE6, p)['ids']][0]
        pts = [(0, 0, 0)]
        for d in range(len(leafp_) + 1):
            p = leafp_[:d]; ids = node_at(TREE6, p)['ids']; x, y = pos[p]
            tt = .8 + .12 * i if p == '' else TS[par(p)] + .35
            pts.append((tt, x + tokx(len(ids), ids.index(c)) - x0, y - y0))
        f.path(tok(x0, y0, c), pts, .3, d=.6)
    # leaf values
    for ids, v in LV6.items():
        x, y = pos[pid[ids]]
        f.show(chip(x, y + 31, sg(v), POS if v > 0 else NEG, 52), END + .4 + .15 * LEAVES6.index(ids))
    # round log under the table
    for k, (bids, win, col, thr, g) in enumerate(ROUNDS6):
        f.show(S(0, 262 + k * 20, 'round %d · split %s' % (k + 1, ' '.join(win)), HL, bold=True), TS[pid[win]])
    f.show(S(0, 330, '4 leaves = num_leaves → stop', GR, bold=True), END)
    f.show(S(0, 350, 'leaf value = mean residual', MU), END + .4)
    return finish(f, max(pos['nyy'][1] + 52, 362))


# ---------- 2.1 / 2.2 Level-wise ↔ leaf-wise ----------
def tpos(root, x0, x1, y0, dy):
    order = []
    def walk(n):
        if 'L' in n: walk(n['L']); walk(n['R'])
        else: order.append(n)
    walk(root)
    for i, n in enumerate(order): n['x'] = x0 + (x1 - x0) * (i + .5) / len(order)
    def setx(n):
        n['y'] = y0 + n['d'] * dy
        if 'L' in n: n['x'] = (setx(n['L']) + setx(n['R'])) / 2
        return n['x']
    setx(root)

def fig_growth(mode):
    lw = mode == 'leaf'
    root, lv, sse = (LEAF, LEAF_LV, LEAF_SSE) if lw else (LEVEL, LEVEL_LV, LEVEL_SSE)
    pre = 'lgb3-' if lw else 'lgb2-'
    gs = gains(root)
    aria = ('Leaf-wise growth of one tree on 300 customers with a budget of 8 leaves. Each split goes to the leaf with the '
            'largest gain: %s. The tree gets 4 levels deep on one side and stays shallow on the other. Squared error falls '
            'from 2858 to %d.' if lw else
            'Level-wise growth of one tree on 300 customers with a budget of 8 leaves. Every node on a level is split before '
            'the next level starts, in order: %s. Two splits on the last level gain only 6 and 8 but are made anyway. '
            'Squared error falls from 2858 to %d.') % (', '.join(str(g) for _, g in gs), round(sse))
    f = Anim(pre, 720, 0, aria, 'SPLIT THE LEAF WITH THE LARGEST GAIN · WHEREVER IT IS' if lw else
             'SPLIT EVERY NODE OF A LEVEL · THEN GO ONE LEVEL DOWN')
    tpos(root, 10, 710, 52, 74)
    t_of = lambda k: .4 + (k - 1) * .9
    ns = nodes(root)
    for n in ns:
        n['ta'] = .2 if n is root else None
    for n in ns:
        if 'g' in n:
            n['L']['ta'] = n['R']['ta'] = t_of(n['order']) + .4; n['L']['par'] = n['R']['par'] = n
    for n in ns:
        x, y = n['x'], n['y']; ts = t_of(n['order']) if 'g' in n else None
        lab = str(len(n['rows']))
        pill_ = R(x - 20, y - 11, 40, 22, BG, 'none', 11) + R(x - 20, y - 11, 40, 22, 'var(--brand-soft)', RULE_HI, 11, 1) + \
            T(x, y + 4, lab, MU, mono=True)
        if n is root: f.show(pill_, n['ta'], hide=ts)
        else:
            px, py = n['par']['x'], n['par']['y']; t0 = n['ta'] - .4
            f.path(pill_, [(0, px - x, py - y), (t0 + .35, 0, 0)], t0, d=.6, hide=ts)
        if 'g' in n:
            q = '%s < %g' % (COLN[n['f']], n['t'])
            weak = n['g'] < WASTE
            c = RO if weak else RULE_HI
            for ch in (n['L'], n['R']):
                f.show(L(x, y + 13, ch['x'], ch['y'] - 11, RULE_HI, 1.2), ts + .5)
            w = len(q) * 6.4 + 22
            f.show(qbox(x, y, q, c, 1.8 if weak else 1.2), ts + .3)
            bx = x - w / 2 - 12
            f.show('<circle cx="%.1f" cy="%.1f" r="9" fill="%s" stroke="%s" stroke-width="1.2"/>' % (bx, y, BG, AM) +
                   T(bx, y + 4, str(n['order']), AM, mono=True, bold=True), ts)
            f.show(T(x + w / 2 + 5, y + 4, '%d' % round(n['g']), RO if weak else MU, 'start', mono=True, bold=weak), ts + .1)
    yb = max(l['y'] for l in lv) + 40
    tE = t_of(7) + 1.0
    f.static(T(0, yb, 'circle = leaf, number of rows in it', FA, 'start', 'sv-s'))
    if not lw:
        f.show(T(0, yb + 22, 'red gain: a split made only because its node sits on the current level', RO, 'start', 'sv-s'), t_of(4) + .3)
    else:
        f.show(T(0, yb + 22, 'leaves end at depth %s: deep only where the gain is' % ' to '.join(str(d) for d in (min(l['d'] for l in lv), max(l['d'] for l in lv))), HL, 'start', 'sv-s'), t_of(5) + .3)
    f.show(T(718, yb, '8 leaves · squared error 2858 → %d' % round(sse), GR if lw else TX, 'end', 'sv-s', bold=True), tE)
    return finish(f, yb + 34)

# ---------- 3.1 Bins ----------
SAMPLE6 = TR[:6]
SB6 = [binof(p, 0) for p in SAMPLE6]
assert SB6 == [3, 5, 0, 0, 4, 6]
def fig_bins():
    f = Anim('lgb4-', 720, 0, 'A table of raw ages, six of the 300 customers. Each age slides into the 5-year bin that holds it: '
             '36.2 into bin 35 to 40, 46.8 into 45 to 50, 22.9 and 23.5 into 20 to 25, 41.2 into 40 to 45, 51.4 into 50 to 55, '
             'and the table gets a bin column. Over all 300 rows the ten bins hold 33, 39, 32, 31, 19, 32, 28, 24, 32 and 30 '
             'rows. An exact scan would try every gap between two sorted ages, 299 thresholds, best at 45.1 with gain 918. With '
             'bins only the 9 bin edges are candidates, best at age 45 with gain 906.',
             'BUCKET EACH COLUMN ONCE · THEN ONLY THE BIN EDGES ARE CANDIDATES')
    t = Table(0, 30, [('row', 34), ('age', 50), ('bin', 44)])
    f.static(t.head())
    for i, p in enumerate(SAMPLE6):
        f.static(t.row(i, [str(i + 1), '%.1f' % p[0], '']))
    x0, x1 = 170, 710
    PX = lambda a: x0 + (a - 20) / 50 * (x1 - x0)
    bw = PX(25) - PX(20); yb = 150
    f.static(S(x0, 42, 'age bins · 5 years each', MU, bold=True))
    for k in range(NB):
        a = PX(20 + 5 * k)
        f.static(R(a + 2, yb, bw - 4, 26, 'var(--brand-soft)', RULE_HI, 3, 1))
    for a in range(20, 71, 5): f.static(T(PX(a), yb + 42, str(a), FA, mono=True))
    # each sample age slides from its cell into its bin
    stack = {}
    for i, (p, k) in enumerate(zip(SAMPLE6, SB6)):
        h = stack.get(k, 0); stack[k] = h + 1
        tt = .6 + .7 * i
        cx, cy = PX(20 + 5 * k) + bw / 2, yb - 16 - 24 * h
        sx, sy = t.cx(1), t.ry(i) + 13
        c = R(cx - 22, cy - 10, 44, 20, BG, 'none', 4) + R(cx - 22, cy - 10, 44, 20, tn(FI, '.14'), FI, 4, 1.2) + \
            T(cx, cy + 4, '%.1f' % p[0], FI, mono=True, bold=True)
        f.path(c, [(0, sx - cx, sy - cy), (tt + .3, 0, 0)], tt, d=.7)
        f.show(t.outline(i, c=HL, sw=1.6), tt, hide=tt + 1.0)
        f.show(t.cell(i, 2, '%d–%d' % (20 + 5 * k, 25 + 5 * k), 'bl'), tt + 1.0)
    tc = .6 + .7 * 6 + .6
    for k in range(NB):
        a = PX(20 + 5 * k)
        f.show(R(a + 2, yb, bw - 4, 26, 'var(--brand-soft)', RULE_HI, 3, 1) + T(a + bw / 2, yb + 18, str(AGE_CNT[k]), TX, mono=True),
               tc + .08 * k)
    f.show(S(x1, 42, 'rows per bin, all 300', MU, 'end'), tc)
    # candidates
    te = tc + 1.4
    for k in range(1, NB):
        f.show(L(PX(20 + 5 * k), yb - 4, PX(20 + 5 * k), yb + 30, AM, 1.6), te)
    f.show(L(PX(45), yb - 6, PX(45), yb + 32, GR, 2.6), te + .8)
    ya = 254
    f.show(S(0, ya + 4, 'exact', MU, bold=True) + S(0, ya + 22, '299 candidates · best 45.1 · gain %d' % round(EX[0]), MU), te + 1.2)
    ages = sorted(p[0] for p in TR); gaps = [(a + b) / 2 for a, b in zip(ages, ages[1:])]
    assert len(gaps) == 299
    f.show(''.join(L(PX(g), ya - 8, PX(g), ya + 8, FA, .6) for g in gaps), te + 1.2)
    yc = 300
    f.show(S(0, yc + 4, 'bins', AM, bold=True) + S(0, yc + 22, '9 candidates · best 45 · gain %d' % round(BN[0]), GR, bold=True), te + .8)
    f.show(''.join(L(PX(20 + 5 * k), yc - 8, PX(20 + 5 * k), yc + 8, AM, 1.6) for k in range(1, NB)) +
           L(PX(45), yc - 10, PX(45), yc + 10, GR, 2.6), te + .8)
    assert sum(AGE_CNT) == 300
    return finish(f, yc + 32)

# ---------- 3.2 Histogram subtraction ----------
def fig_subtract():
    f = Anim('lgb5-', 720, 0, 'Income histograms after the root split at age 45. The parent histogram of all 300 rows is already '
             'built. Only the smaller child, age 45 and over with 146 rows, is scanned to build its histogram. The other child, '
             'under 45 with 154 rows, is the parent minus the scanned child, bin by bin, without touching a row.',
             'SCAN THE SMALLER CHILD · THE SIBLING = PARENT − CHILD')
    x0, bw, hs = 196, 50, 1.25
    rows = [('parent · all 300 rows', 'built one level up', HP, MU, .3),
            ('age ≥ 45 · 146 rows', 'scanned', HS, FI, 1.2),
            ('age < 45 · 154 rows', '= parent − scanned', HD, GR, 3.0)]
    for r, (name, sub, H, c, t0) in enumerate(rows):
        yb = 100 + r * 96
        f.static(L(x0, yb, x0 + NB * bw, yb, RULE_HI, 1))
        f.show(S(0, yb - 26, name, c if r else TX, bold=True) + S(0, yb - 8, sub, MU), t0)
        for k, v in enumerate(H):
            x = x0 + k * bw
            t = t0 + (.1 * k if r < 2 else .25 * k)
            f.show(R(x + 6, yb - v * hs, bw - 12, v * hs, tn(c, '.22') if c != MU else SUNK, c if c != MU else RULE_HI, 2, 1.2) +
                   T(x + bw / 2, yb - v * hs - 5, str(v), c if c != MU else MU, mono=True), t)
            if r == 2:
                f.show(R(x + 2, yb - 70, bw - 4, 18, tn(AM, '.14'), AM, 3, 1) +
                       T(x + bw / 2, yb - 57, '%d−%d' % (HP[k], HS[k]), AM, mono=True), t - .2, hide=t + .5)
    for k in range(NB):
        f.static(T(x0 + k * bw + bw / 2, 100 + 2 * 96 + 16, '%g' % edge(1, k), FA, mono=True))
    f.static(S(x0 + NB * bw, 100 + 2 * 96 + 34, 'income bins', MU, 'end'))
    f.show(S(0, 100 + 2 * 96 + 34, '146 rows scanned, not 300', GR, bold=True), 6.0)
    return finish(f, 100 + 2 * 96 + 46)

# ---------- 04 GOSS ----------
def fig_goss():
    f = Anim('lgb6-', 720, 0, 'The 300 rows sorted by the size of their gradient, one thin bar each. GOSS keeps the 60 largest, '
             'the top 20 percent. From the other 240 it draws 30 at random and weights each by 8, so they stand for the 210 '
             'skipped rows. The split search on these 90 rows picks age under 45, the same split as all 300 rows, with gain '
             '952 against 906. Without the weight of 8 the gain would read 1496.',
             'KEEP ROWS WITH BIG GRADIENTS · SAMPLE THE SMALL ONES · WEIGHT THEM UP')
    x0, bw, yb, hs = 40, 2.1, 236, 13.5
    f.static(L(x0, yb, x0 + 300 * bw, yb, RULE_HI, 1) + S(x0, 40, '|gradient| = |residual|, largest first', MU))
    rk = {i: k for k, i in enumerate(ORDER)}
    bar = lambda i, c: R(x0 + rk[i] * bw, yb - abs(R0[i]) * hs, bw - .4, abs(R0[i]) * hs, c, 'none', 0)
    f.show(''.join(bar(i, GH) for i in ORDER), .2)
    f.show(''.join(bar(i, FI) for i in TOP), 1.2)
    xt = x0 + 60 * bw
    f.show(L(x0, 54, x0, 62, FI, 1.2) + L(x0, 58, xt, 58, FI, 1.2) + L(xt, 54, xt, 62, FI, 1.2) +
           S(x0, 76, 'top 20% · all 60 kept', FI, bold=True), 1.4)
    f.show(''.join(bar(i, VI) for i in SAMP), 2.4)
    for i in SAMP:
        x = x0 + rk[i] * bw + bw / 2
        f.show(L(x, yb + 4, x, yb + 12, VI, 1.2), 2.6)
    f.show(L(xt + 6, 104, xt + 6, 112, VI, 1.2) + L(xt + 6, 108, x0 + 300 * bw, 108, VI, 1.2) +
           L(x0 + 300 * bw, 104, x0 + 300 * bw, 112, VI, 1.2) +
           S(xt + 6, 126, 'random 30 of the other 240 · each weighted × 8', VI, bold=True), 2.6)
    f.show(S(x0 + 300 * bw, 196, 'grey: 210 rows skipped', FA, 'end'), 3.4)
    t = Table(0, 266, [('rows searched', 230), ('best split', 150), ('gain', 90)])
    f.show(t.head(), 4.0)
    rws = [('all 300', BN, None, 4.2), ('GOSS · 90 rows · weight × 8', GW, 'gr', 4.8), ('GOSS · 90 rows · no weight', GU, 'rd', 5.4)]
    for k, (name, b, tone, tt) in enumerate(rws):
        f.show(t.row(k, [name, '%s < %g' % (COLN[b[1]], edge(b[1], b[2])), '%d' % round(b[0])], tone), tt)
    f.show(S(490, t.ry(1) + 17, '← same split, gain on scale', GR, bold=True), 5.0)
    f.show(S(490, t.ry(2) + 17, '← small gradients under-counted', RO, bold=True), 5.6)
    return finish(f, t.ry(3) + 6)

# ---------- 05 EFB ----------
def fig_efb():
    f = Anim('lgb7-', 720, 0, 'The six customers with a one-hot city: columns Paris, Rome, Oslo. No row has a 1 in two of them, '
             'so they never conflict. Rome values are shifted by 1 and Oslo values by 2, then the three columns slide into one '
             'bundle column: A 1, B 2, C 1, D 3, E 2, F 0. One histogram of 4 bins replaces three histograms; each city keeps '
             'its own range of bins.', 'COLUMNS THAT ARE NEVER NON-ZERO TOGETHER · SHARE ONE COLUMN')
    t = Table(0, 30, [('id', 36), ('Paris', 64), ('Rome', 64), ('Oslo', 64)])
    b = Table(470, 30, [('id', 36), ('city bundle', 110)])
    f.static(t.head())
    for i, r in enumerate(DATA):
        v = ONEHOT[r[0]]
        f.show(t.row(i, [r[0]] + [str(x) for x in v], colors={j + 1: (TX if x else FA) for j, x in enumerate(v)}), .2 + .08 * i)
    # check rows: one non-zero at most
    for i, r in enumerate(DATA):
        tt = 1.0 + .25 * i
        f.show(t.outline(i, c=HL, sw=1.6), tt, hide=tt + .25)
        f.show(T(t.x + t.w + 14, t.ry(i) + 17, '✓', GR, 'start', bold=True), tt + .1)
    f.show(S(t.x + t.w + 34, t.ry(2) + 17, 'at most one 1 per row', GR, bold=True) +
           S(t.x + t.w + 34, t.ry(3) + 13, '→ no conflict', GR), 2.6)
    # offsets
    OFF = {1: 3.2, 2: 3.8}
    for j in (1, 2):
        f.show(T(t.cx(j + 1), t.ry(6) + 16, '+%d' % j, AM, mono=True, bold=True), OFF[j] - .2)
        for i, r in enumerate(DATA):
            if ONEHOT[r[0]][j]:
                f.show(t.cell(i, j + 1, str(j + 1), 'am'), OFF[j])
    # slide into the bundle
    f.show(b.head(), 4.4)
    for i, r in enumerate(DATA): f.show(b.row(i, [r[0], '']), 4.4 + .05 * i)
    for i, r in enumerate(DATA):
        v = BUNDLE[r[0]]
        jj = v if v else 1
        dx = t.cx(jj) - b.cx(1)
        cw = t.cols[jj][1] - 6; cx = b.cx(1)
        f.show(R(b.colx(1) + 3, b.ry(i) + 2, b.cols[1][1] - 6, b.rh - 4, tint('am', '.08') if v else BG,
                 AM if v else RULE_HI, 2, 1), 5.6 + .12 * i)
        chipc = R(cx - cw / 2, b.ry(i) + 2, cw, b.rh - 4, BG, 'none', 2) + \
            R(cx - cw / 2, b.ry(i) + 2, cw, b.rh - 4, tint('am', '.20') if v else BG, AM if v else RULE_HI, 2, 1) + \
            T(cx, b.ry(i) + 17, str(v), AM if v else FA, mono=True, bold=bool(v))
        f.path(chipc, [(0, dx, 0), (4.8 + .12 * i, 0, 0)], 4.6, d=.8)
    f.show(S(b.x, b.ry(6) + 18, '0 = no city · 1 Paris · 2 Rome · 3 Oslo', MU), 6.2)
    f.show(S(b.x, b.ry(6) + 38, '3 histograms → 1 histogram of 4 bins', GR, bold=True), 6.6)
    return finish(f, t.ry(6) + 50)

# ---------- 5.x native categorical split ----------
CITYC = {'A': 'Rome', 'B': 'Rome', 'C': 'Paris', 'D': 'Oslo', 'E': 'Paris', 'F': 'Oslo'}   # a city column of its own
CATS = sorted(set(CITYC.values()))
CG = {c: sum(RES[k] for k, v in CITYC.items() if v == c) for c in CATS}
CN = {c: sum(1 for v in CITYC.values() if v == c) for c in CATS}
CORD = sorted(CATS, key=lambda c: CG[c] / CN[c])
def cat_best():
    ids = list(CITYC); Gt = sum(RES[k] for k in ids); n = len(ids); out = None
    for j in range(1, len(CORD)):
        left = CORD[:j]; gl = sum(CG[c] for c in left); nl = sum(CN[c] for c in left)
        g = gl * gl / nl + (Gt - gl) ** 2 / (n - nl) - Gt * Gt / n
        if out is None or g > out[0]: out = (g, left)
    return out
CB = cat_best()
assert CORD == ['Rome', 'Paris', 'Oslo'] and {c: CG[c] / CN[c] for c in CATS} == {'Oslo': 10, 'Paris': 4, 'Rome': -14}
assert CB[1] == ['Rome'] and CB[0] == 588
CRIGHT = [c for c in CORD if c not in CB[1]]

def fig_cat():
    f = Anim('lgb11-', 720, 0, 'The six customers with a city column and their residuals. Grouping by city gives the mean residual '
             'per city: Rome minus 14, Paris plus 4, Oslo plus 10. The cities are sorted by that mean and only the cuts in that '
             'order are tried, as on a numeric column: Rome against Paris and Oslo gains 588, Rome and Paris against Oslo 300. '
             'The node becomes city in Paris or Oslo: C D E F go yes, A B go no.',
             'SORT THE CATEGORIES BY MEAN GRADIENT · THEN CUT LIKE A NUMBER')
    t = Table(0, 30, [('id', 30), ('city', 60), ('residual', 66)])
    f.static(t.head())
    ids = 'ABCDEF'
    for i, k in enumerate(ids):
        v = RES[k]; f.static(t.row(i, [k, CITYC[k], sg(v)], colors={2: POS if v > 0 else NEG}))
    g = Table(220, 30, [('city', 60), ('rows', 44), ('mean', 56)])
    f.show(g.head(), .4)
    for j, c in enumerate(CORD):
        tt = .8 + 1.0 * j
        rows = [i for i, k in enumerate(ids) if CITYC[k] == c]
        f.show(''.join(t.outline(i, c=HL, sw=1.6) for i in rows), tt, hide=tt + .9)
        m = CG[c] / CN[c]
        f.show(g.row(j, [c, str(CN[c]), sg(m)], colors={2: POS if m > 0 else NEG}), tt + .4)
    tc = .8 + 3.0 + .2
    cuts = []
    for j in range(1, 3):
        left = CORD[:j]; gl = sum(CG[c] for c in left); nl = sum(CN[c] for c in left)
        cuts.append(gl * gl / nl + gl * gl / (6 - nl))      # total residual is 0
    assert [round(c) for c in cuts] == [588, 300]
    for j, gv in enumerate(cuts):
        yc = g.ry(j + 1) - 2; tt = tc + .9 * j; best_ = j == 0
        f.show(L(g.x - 6, yc, g.x + g.w + 6, yc, HL if best_ else FA, 1.6, '5 4') +
               T(g.x + g.w + 12, yc + 4, 'gain %d' % round(gv), HL if best_ else FA, 'start', mono=True, bold=best_), tt)
    tn_ = tc + 2.0
    q = 'city ∈ {Paris, Oslo} ?'
    nx, ny = 600, 70
    f.show(qbox(nx, ny, q), tn_)
    for ch, lab, cx in (('y', 'CDEF', 555), ('n', 'AB', 665)):
        f.show(L(nx, ny + 13, cx, 138, RULE_HI, 1.2) + T((nx + cx) / 2 + (-12 if ch == 'y' else 12), 108,
               'yes' if ch == 'y' else 'no', FA, 'end' if ch == 'y' else 'start') + grp(cx, 150, lab), tn_ + .4)
    f.show(S(nx, 196, 'one cut · not one per city', GR, 'middle', bold=True), tn_ + .8)
    return finish(f, t.ry(6) + 8)

# ---------- 6.x Reining it in ----------
def fig_curve(pre, xs, cs, xname, best_i, aria, caption, ticks=None, note=None):
    f = Anim(pre, 720, 0, aria, caption)
    x0, x1, yb, yt = 60, 560, 262, 56
    PY = lambda e: yb - e / 3 * (yb - yt)
    pos = lambda i: x0 + 30 + i * (x1 - x0 - 60) / (len(xs) - 1)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for e in (1, 2, 3): f.static(T(x0 - 7, PY(e) + 4, '%g' % e, FA, 'end', mono=True) + L(x0, PY(e), x1, PY(e), RULE, .8))
    for i, v in enumerate(xs):
        f.static(T(pos(i), yb + 15, 'none' if v is None else str(v), FA, mono=True))
        if ticks: f.static(T(pos(i), yb + 30, str(ticks[i]), MU, mono=True))
    f.static(S(x1, yb + (48 if ticks else 34), xname, MU, 'end') + S(x0, yt - 12, 'RMSE', MU))
    if ticks: f.static(S(x0 - 56, yb + 30, 'leaves', MU))
    for i, c in enumerate(cs):
        t = .3 + i * .35; seg = ''
        if i: seg = L(pos(i - 1), PY(cs[i - 1][0]), pos(i), PY(c[0]), FI, 2) + L(pos(i - 1), PY(cs[i - 1][1]), pos(i), PY(c[1]), VI, 2)
        f.show(seg + dot(pos(i), PY(c[0]), FI, 4) + dot(pos(i), PY(c[1]), VI, 4), t)
    tl = .3 + len(cs) * .35
    lx = len(cs) - 1
    yt_, yr_ = PY(cs[lx][1]), PY(cs[lx][0])
    if yr_ - yt_ < 18: yt_, yr_ = (yt_ + yr_) / 2 - 9, (yt_ + yr_) / 2 + 9
    f.show(S(pos(lx) + 8, yr_ + 4, 'train', FI, 'start', bold=True) +
           S(pos(lx) + 8, yt_ + 4, 'test', VI, 'start', bold=True), tl)
    bx, by = pos(best_i), PY(cs[best_i][1])
    f.show('<circle cx="%.1f" cy="%.1f" r="10" fill="none" stroke="%s" stroke-width="2"/>' % (bx, by, GR) +
           S(bx, by - 16, 'test %.2f' % cs[best_i][1], GR, 'middle', bold=True), tl + .5)
    X1 = 590
    for k, (s, c, b) in enumerate(note):
        f.show(S(X1, 76 + k * 20, s, c, bold=b), tl + .8 + .2 * k)
    return finish(f, yb + (60 if ticks else 46))

def fig_numleaves():
    bi = min(range(len(NLC)), key=lambda i: NLC[i][1]); assert NLV[bi] == 4
    return fig_curve('lgb8-', NLV, NLC, 'num_leaves', bi,
                     'Train and test RMSE of 100 boosted trees against num_leaves, from 2 to 64, min_data_in_leaf 1. Train RMSE '
                     'keeps falling. Test RMSE is best at 4 leaves, %.2f, and climbs to %.2f at 64.' % (NLC[bi][1], NLC[-1][1]),
                     'MORE LEAVES PER TREE · TRAIN ↓ · TEST ↓ THEN ↑',
                     note=[('num_leaves = %d' % NLV[bi], GR, True), ('test %.2f' % NLC[bi][1], GR, False),
                           ('', MU, False), ('num_leaves = 64', RO, True), ('test %.2f' % NLC[-1][1], RO, False),
                           ('train %.2f' % NLC[-1][0], RO, False)])

def fig_mindata():
    bi = min(range(len(MSC)), key=lambda i: MSC[i][1]); assert MSV[bi] == 20
    return fig_curve('lgb9-', MSV, MSC, 'min_data_in_leaf', bi,
                     'Train and test RMSE of 100 boosted trees with up to 64 leaves, against min_data_in_leaf from 1 to 80. '
                     'At 1 a leaf may hold one row and test RMSE is %.2f. At 20 it is best, %.2f. At 80 every tree is too coarse, '
                     '%.2f.' % (MSC[0][1], MSC[bi][1], MSC[-1][1]),
                     'EVERY LEAF MUST HOLD AT LEAST N ROWS',
                     note=[('1 row per leaf', RO, True), ('test %.2f' % MSC[0][1], RO, False), ('', MU, False),
                           ('20 rows (default)', GR, True), ('test %.2f' % MSC[bi][1], GR, False), ('', MU, False),
                           ('80 rows', RO, True), ('test %.2f · too coarse' % MSC[-1][1], RO, False)])

def fig_maxdepth():
    bi = min(range(len(MDC)), key=lambda i: MDC[i][1]); assert MDV[bi] == 3
    return fig_curve('lgb10-', MDV, MDC, 'max_depth', bi,
                     'Train and test RMSE of 100 boosted trees with num_leaves 64, against max_depth from 1 to none. Under each '
                     'depth, the most leaves any tree reached: 2, 4, 8, 16, then 55 and 64, so depth d caps a tree at 2 to the d '
                     'leaves. Test RMSE is best at depth 3, %.2f.' % MDC[bi][1],
                     'A DEPTH LIMIT CAPS THE LEAVES AT 2ᵈ', ticks=[c[2] for c in MDC],
                     note=[('max_depth = 3', GR, True), ('≤ 8 leaves · test %.2f' % MDC[bi][1], GR, False), ('', MU, False),
                           ('max_depth ≥ 6', RO, True), ('2⁶ = 64 ≥ num_leaves', RO, False), ('the limit does nothing', RO, False)])

# =====================================================================================================
BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Tree models</p>
  <h1>Light<em>GBM</em></h1>
  <p class="lede">LightGBM is gradient boosting that grows each tree <b>one best leaf at a time</b> and searches splits over <b>a few bins</b> instead of every value — much faster, but the leaf count is now yours to rein in.</p>
</header>

<section id="lgbm-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Every leaf bids the gain of its best split; each round, <em>only the top bid is split</em>, until the tree has <code>num_leaves</code> leaves.</p>
{f1}
  <ul class="why">
    <li>The same six customers and residuals (spend − 25) as <a href="../xgboost/index.html">XGBoost</a>; a bid is XGBoost's Gain with <span class="mth"><var>λ</var> = 0</span>, LightGBM's default.</li>
    <li>The budget is a number of leaves (default 31), not a depth, so the tree grows lopsided toward where the error is.</li>
  </ul>
</section>

<section id="lgbm-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Growing a tree</h2></div>
  <p class="key">Same 8-leaf budget, same gain formula: only <em>which node is split next</em> changes.</p>
  <div class="subsec" id="lgbm-s2-1">
    <h3 class="ssh"><b>2.1</b>Level-wise</h3>
    <p class="skey">Split every node of a level, <em>useful or not</em>, then move one level down.</p>
{f2}
    <ul class="why">
      <li>The rule of <a href="../xgboost/index.html">XGBoost</a> by default: a balanced tree, depth set by <code>max_depth</code>.</li>
    </ul>
  </div>
  <div class="subsec" id="lgbm-s2-2">
    <h3 class="ssh"><b>2.2</b>Leaf-wise</h3>
    <p class="skey">Split the one leaf with <em>the largest gain</em>, wherever it sits.</p>
{f3}
    <ul class="why">
      <li>Same 8 leaves, less error left: %(lvl)d → %(lf)d, because no split is spent on a node with gain 6.</li>
      <li>Nothing stops one branch from going very deep — section 06.</li>
    </ul>
  </div>
</section>

<section id="lgbm-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Histogram binning</h2></div>
  <p class="key">Bucket every column into bins once; from then on a split search works on <em>per-bin sums</em>, not on rows.</p>
  <div class="subsec" id="lgbm-s3-1">
    <h3 class="ssh"><b>3.1</b>Bins</h3>
    <p class="skey">Candidates drop from <em>every gap between values</em> to every bin edge.</p>
{f4}
    <ul class="why">
      <li>Each bin stores the sum of gradients and of hessians; one left-to-right pass gives the gain of every edge.</li>
      <li><code>max_bin</code> defaults to 255. Boosting 100 trees here: exact test RMSE %(ex).2f, 10 bins %(b10).2f, 5 bins %(b5).2f — coarse bins also smooth, too coarse loses the cut.</li>
    </ul>
  </div>
  <div class="subsec" id="lgbm-s3-2">
    <h3 class="ssh"><b>3.2</b>Histogram subtraction</h3>
    <p class="skey">After a split, build the histogram of <em>the smaller child only</em>; the sibling is a subtraction.</p>
{f5}
    <ul class="why">
      <li>Works because a parent's bins are exactly its two children's bins added up — for counts and gradient sums alike.</li>
    </ul>
  </div>
</section>

<section id="lgbm-s4" class="lesson">
  <div class="sh"><b>04</b><h2>GOSS</h2></div>
  <p class="key">Rows the model already fits have <em>small gradients</em>; keep the big ones, sample the rest and weight them up.</p>
{f6}
  <ul class="why">
    <li>Gradient-based One-Side Sampling: <code>top_rate</code> 0.2 and <code>other_rate</code> 0.1 here; the weight is (1 − 0.2) / 0.1 = 8.</li>
    <li>Without the weight the big gradients dominate the sums and the gain is overstated.</li>
  </ul>
</section>

<section id="lgbm-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Sparse and categorical columns</h2></div>
  <p class="key">Fewer columns to scan, and categories split <em>without one-hot</em>.</p>
  <div class="subsec" id="lgbm-s5-1">
    <h3 class="ssh"><b>5.1</b>EFB</h3>
    <p class="skey">Sparse columns that are <em>never non-zero in the same row</em> can share one column, shifted so their values do not mix.</p>
{f7}
    <ul class="why">
      <li>Exclusive Feature Bundling: fewer columns means fewer histograms to build; each city still gets its own splits from its own bins.</li>
      <li>One-hot columns are the typical case. A few rows where two columns clash are tolerated, up to <code>max_conflict_rate</code>.</li>
    </ul>
  </div>
  <div class="subsec" id="lgbm-s5-2">
    <h3 class="ssh"><b>5.2</b>Native categorical split</h3>
    <p class="skey">Sort the categories by <em>mean gradient</em>, then try only the cuts in that order — one node sends a whole group of categories left.</p>
{f11}
    <ul class="why">
      <li>Declare the column with <code>categorical_feature</code> (or pandas <code>category</code> dtype); <span class="mth"><var>k</var></span> categories give <span class="mth"><var>k</var> − 1</span> cuts, not <span class="mth">2<sup><var>k</var>−1</sup></span> subsets.</li>
      <li>Missing values need no imputing: at each split the rows with no value are tried on both sides and sent where the gain is larger, and that direction is stored in the node.</li>
    </ul>
  </div>
</section>

<section id="lgbm-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Reining it in</h2></div>
  <p class="key">Leaf-wise growth has no level to stop at: with few rows, <em>a tree chases noise</em> unless you limit it.</p>
  <div class="subsec" id="lgbm-s6-1">
    <h3 class="ssh"><b>6.1</b>num_leaves</h3>
    <p class="skey">The main knob: <em>leaves per tree</em>, the budget of section 01.</p>
{f8}
    <ul class="why">
      <li>Default 31. On 300 noisy rows the best here is 4; large data supports many more.</li>
    </ul>
  </div>
  <div class="subsec" id="lgbm-s6-2">
    <h3 class="ssh"><b>6.2</b>min_data_in_leaf</h3>
    <p class="skey">Forbid a split that would leave <em>too few rows</em> in a child.</p>
{f9}
    <ul class="why">
      <li>Default 20 (<code>min_child_samples</code> in the scikit-learn API): with 64 leaves allowed, it alone brings test RMSE from %(m1).2f to %(m20).2f.</li>
    </ul>
  </div>
  <div class="subsec" id="lgbm-s6-3">
    <h3 class="ssh"><b>6.3</b>max_depth</h3>
    <p class="skey">A depth limit caps a tree at <span class="mth">2<sup><var>d</var></sup></span> leaves — it only acts when that is below <code>num_leaves</code>.</p>
{f10}
    <ul class="why">
      <li>Default none. Keep <code>num_leaves</code> &lt; <span class="mth">2<sup>max_depth</sup></span>, or setting <code>max_depth</code> changes nothing.</li>
      <li>The usual tuning set: <code>num_leaves</code> and <code>min_data_in_leaf</code> for tree size, <code>learning_rate</code> (default 0.1) traded against the number of rounds, and <code>feature_fraction</code> / <code>bagging_fraction</code> (with <code>bagging_freq</code>) to sample columns and rows per tree.</li>
    </ul>
  </div>
</section>
''' % dict(lvl=round(LEVEL_SSE), lf=round(LEAF_SSE), ex=BINRUN[None][1], b10=BINRUN[10][1], b5=BINRUN[5][1],
           m1=MSC[0][1], m20=MSC[4][1])

SCRIPT = DT_BODY[DT_BODY.index('<script>'):DT_BODY.index('</script>') + len('</script>')]
FOOTER = ('<footer>Machine learning · Tree models · last lesson of the group; next: '
          '<a href="../../07-clustering/clustering-overview/index.html">Clustering overview</a>.</footer>\n')

def build():
    figs = dict(f1=fig_mental(), f2=fig_growth('level'), f3=fig_growth('leaf'), f4=fig_bins(), f5=fig_subtract(),
                f6=fig_goss(), f7=fig_efb(), f11=fig_cat(), f8=fig_numleaves(), f9=fig_mindata(), f10=fig_maxdepth())
    return re.sub(r'\{(f\d+)\}', lambda m: figs[m.group(1)], BODY) + '\n' + SCRIPT + '\n\n' + FOOTER

if __name__ == '__main__':
    splice(PAGE, build(), 'Gradient boosting that splits the one leaf with the largest gain and scans bins instead of values; '
           'GOSS and EFB cut rows and columns, num_leaves and min_data_in_leaf rein it in.')
