# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/06-tree-models/tree-family-overview.
Same visual language as decision_tree.py and the same seeded data: the six customers for the one-tree
figure, the 300 noisy points from a circular boundary (train seed 1, test seed 2) for everything else.
Single trees, a random forest, gradient-boosted stumps and level-wise / leaf-wise growth are all fitted
here in pure Python, so every error rate in a figure is computed. Run: python3 tree_family_overview.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import decision_tree as dt
from decision_tree import (DATA, LAB, CL, HL, layout, draw_tree, node_at, TREE, grow, pred, err, leaves, sgini,
                           TR, TE, leafp)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, finish)
from tablefig import GR, AM, RD, tint, pill

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/06-tree-models/tree-family-overview/index.html')
BAG, BST = FI, VI          # bagging lane = blue, boosting lane = violet, in every figure from section 03 on

# ---------- models ----------
def boot(P, seed):
    g = random.Random(seed); return [P[g.randrange(len(P))] for _ in P]

def rf_tree(P, g):
    """CART grown to purity, but each split may look at only one randomly drawn column (max_features=1 of 2)."""
    n = len(P); k = sum(q[2] for q in P); node = dict(n=n, k=k)
    if sgini(P) == 0: return node
    first = g.randrange(2); best = None
    for f in (first, 1 - first):
        Sp = sorted(P, key=lambda q: q[f]); lk = 0
        for i in range(1, n):
            lk += Sp[i - 1][2]
            if Sp[i][f] == Sp[i - 1][f]: continue
            l = 1 - (lk / i) ** 2 - (1 - lk / i) ** 2; r = (k - lk) / (n - i); r = 1 - r * r - (1 - r) ** 2
            w = i / n * l + (n - i) / n * r
            if best is None or w < best[0] - 1e-12: best = (w, f, (Sp[i - 1][f] + Sp[i][f]) / 2)
        if best: break        # the drawn column could split; the other one is only a fallback for ties
    if best is None: return node
    _, f, t = best; node.update(f=f, t=t)
    node['L'] = rf_tree([q for q in P if q[f] < t], g); node['R'] = rf_tree([q for q in P if q[f] >= t], g)
    return node

def forest(P, n, seed):
    return [rf_tree(boot(P, seed + i), random.Random(seed + 50000 + i)) for i in range(n)]

def fvote(F, q):
    return int(2 * sum(pred(t, q) for t in F) >= len(F))

def stump(P, r):
    """regression stump on residuals r: best single cut by squared error -> (f, t, vL, vR)"""
    n = len(P); tot = sum(r); best = None
    for f in (0, 1):
        idx = sorted(range(n), key=lambda i: P[i][f]); s = 0
        for k in range(1, n):
            i = idx[k - 1]; s += r[i]
            if P[idx[k]][f] == P[i][f]: continue
            gain = s * s / k + (tot - s) ** 2 / (n - k)     # maximising this = minimising squared error
            if best is None or gain > best[0] + 1e-12:
                best = (gain, f, (P[i][f] + P[idx[k]][f]) / 2, s / k, (tot - s) / (n - k))
    return best[1:]

def boost(P, M, lr):
    F0 = sum(q[2] for q in P) / len(P); Fx = [F0] * len(P); H = []
    for _ in range(M):
        f, t, a, b = stump(P, [q[2] - v for q, v in zip(P, Fx)]); H.append((f, t, a, b))
        Fx = [v + lr * (a if q[f] < t else b) for v, q in zip(Fx, P)]
    return F0, H

def bscore(model, q, n, lr):
    F0, H = model
    return F0 + lr * sum(a if q[f] < t else b for f, t, a, b in H[:n])

def rate(fn, P): return sum(fn(q) != q[2] for q in P) / len(P)

# ---------- numbers ----------
# 02 · two trees on two 90 % subsets of the same training set
SA, SB = random.Random(11).sample(TR, 270), random.Random(12).sample(TR, 270)
TA, TB = grow(SA), grow(SB)
DIS_T = sum(pred(TA, q) != pred(TB, q) for q in TE) / len(TE)
assert err(TA, SA) == 0 and err(TB, SB) == 0
assert round(DIS_T, 3) == .18 and round(err(TA, TE), 3) == .257 and round(err(TB, TE), 3) == .243
FA_, FB_ = forest(SA, 100, 100), forest(SB, 100, 300)
DIS_F = sum(fvote(FA_, q) != fvote(FB_, q) for q in TE) / len(TE)

# 04 / 05 · forest and boosted stumps on the full training set
NS = [1, 2, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000]
RF = forest(TR, 1000, 5000)
RFC = [(n, rate(lambda q: fvote(RF[:n], q), TR), rate(lambda q: fvote(RF[:n], q), TE)) for n in NS]
LR = .3
GB = boost(TR, 1000, LR)
GBC = [(n, rate(lambda q: int(bscore(GB, q, n, LR) >= .5), TR), rate(lambda q: int(bscore(GB, q, n, LR) >= .5), TE))
       for n in NS]
RF_N, GB_N = 300, 50                  # the ensembles drawn in section 04
RF_E = dict((n, te) for n, _, te in RFC)[RF_N]; GB_E = dict((n, te) for n, _, te in GBC)[GB_N]
STUMP1 = grow(TR, maxd=1)
GB_BEST = min(GBC, key=lambda c: (c[2], c[0]))

# 5.2 · level-wise vs leaf-wise growth, same budget of 7 splits
def best_split(P):
    n = len(P); k = sum(q[2] for q in P); best = None
    for f in (0, 1):
        Sp = sorted(P, key=lambda q: q[f]); lk = 0
        for i in range(1, n):
            lk += Sp[i - 1][2]
            if Sp[i][f] == Sp[i - 1][f]: continue
            l = 1 - (lk / i) ** 2 - (1 - lk / i) ** 2; r = (k - lk) / (n - i); r = 1 - r * r - (1 - r) ** 2
            w = i / n * l + (n - i) / n * r
            if best is None or w < best[0] - 1e-12: best = (w, f, (Sp[i - 1][f] + Sp[i][f]) / 2)
    if best is None: return None
    return (n * (sgini(P) - best[0]), best[1], best[2])      # gain weighted by rows reaching the node

def grow_budget(P, splits, leafwise):
    """grow by repeatedly splitting one leaf: level-wise = shallowest first, leaf-wise = largest gain first.
    Returns the root; every split node records its split order in 'o'."""
    root = dict(P=P, d=0, n=len(P), k=sum(q[2] for q in P)); open_ = [root]
    for o in range(1, splits + 1):
        cand = [(best_split(u['P']), u) for u in open_ if sgini(u['P']) > 0]
        cand = [(b, u) for b, u in cand if b and b[0] > 1e-12]
        if not cand: break
        if leafwise: b, u = max(cand, key=lambda c: c[0][0])
        else: b, u = min(cand, key=lambda c: (c[1]['d'], -c[0][0]))
        _, f, t = b; u.update(f=f, t=t, o=o)
        for side, keep in (('L', lambda q: q[f] < t), ('R', lambda q: q[f] >= t)):
            Q = [q for q in u['P'] if keep(q)]; u[side] = dict(P=Q, d=u['d'] + 1, n=len(Q), k=sum(q[2] for q in Q))
        open_.remove(u); open_ += [u['L'], u['R']]
    return root

LEVEL, LEAF = grow_budget(TR, 7, False), grow_budget(TR, 7, True)
def gdepth(t): return 0 if 'f' not in t else 1 + max(gdepth(t['L']), gdepth(t['R']))
LV_E, LF_E = err(LEVEL, TE), err(LEAF, TE)
LV_TR, LF_TR = err(LEVEL, TR), err(LEAF, TR)

print('two trees disagree %.3f · two forests %.3f' % (DIS_T, DIS_F))
print('RF', [(n, round(tr, 3), round(te, 3)) for n, tr, te in RFC])
print('GB', [(n, round(tr, 3), round(te, 3)) for n, tr, te in GBC])
print('stump1 test %.3f' % err(STUMP1, TE), 'GB best', GB_BEST)
print('level depth %d test %.3f train %.3f · leaf depth %d test %.3f train %.3f' % (
    gdepth(LEVEL), LV_E, LV_TR, gdepth(LEAF), LF_E, LF_TR))

# ---------- drawing helpers ----------
def raster(x0, y0, size, fn, fill, n=50):
    """region where fn(x, y) is true, painted as merged row runs on an n x n grid"""
    s = ''; c = size / n
    for j in range(n):
        y = 1 - (j + .5) / n; run = None
        for i in range(n + 1):
            on = i < n and fn((i + .5) / n, y)
            if on and run is None: run = i
            if not on and run is not None:
                s += R(x0 + run * c, y0 + j * c, (i - run) * c, c, fill, 'none', 0).replace('/>', ' shape-rendering="crispEdges"/>'); run = None
    return s

def points(x0, y0, size, P, r=2.2):
    s = ''
    for q in P:
        x, y = x0 + q[0] * size, y0 + (1 - q[1]) * size
        s += ('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, FI) if q[2] else
              '<circle cx="%.1f" cy="%.1f" r="%s" fill="none" stroke="%s" stroke-width="1"/>' % (x, y, r - .4, BR))
    return s

def frame(x0, y0, size): return R(x0, y0, size, size, BG, RULE_HI, 4, 1)

def region(x0, y0, size, fn, P=TR, n=50, r=2.2):
    return raster(x0, y0, size, fn, tn(FI, '.20'), n) + points(x0, y0, size, P, r) + R(x0, y0, size, size, 'none', RULE_HI, 4, 1)

def stump_panel(x0, y0, size, f, t, a, b):
    """one stump: its single cut, the side that pushes toward the inner class tinted"""
    s = frame(x0, y0, size)
    for lo, hi, v in ((0, t, a), (t, 1, b)):
        if v > 0:
            if f == 0: s += R(x0 + lo * size, y0, (hi - lo) * size, size, tn(FI, '.20'), 'none', 0)
            else: s += R(x0, y0 + (1 - hi) * size, size, (hi - lo) * size, tn(FI, '.20'), 'none', 0)
    s += (L(x0 + t * size, y0, x0 + t * size, y0 + size, HL, 1.6, '4 3') if f == 0 else
          L(x0, y0 + (1 - t) * size, x0 + size, y0 + (1 - t) * size, HL, 1.6, '4 3'))
    return s + R(x0, y0, size, size, 'none', RULE_HI, 4, 1)

def pct(e): return '%.1f%%' % (100 * e)

# ---------- 01 One tree ----------
def fig_one():
    f = Anim('tf1-', 720, 0, 'The six-customer table on the left. On the right a decision tree grows one level at a time: the root '
             'asks age under 31.5, then income under 28, then age under 56. Every customer lands in a pure leaf, so the tree '
             'gets all six training rows right.', 'A TABLE IN · YES/NO QUESTIONS OUT · ONE LEVEL AT A TIME')
    t = Table(0, 30, [('id', 28), ('age', 42), ('income', 52), ('buy?', 46)])
    f.static(t.head())
    for i, r in enumerate(DATA):
        f.static(t.row(i, [r[0], str(r[1]), str(r[2]), LAB[r[0]]], colors={3: CL[LAB[r[0]]]}))
    f.show(arrow(t.w + 14, 120, t.w + 64, 120, MU, 1.4) + S(t.w + 14, 108, 'fit', MU), .3)
    pos = layout(TREE, 260, 700, 52, 72)
    by_d = {}
    for p in pos: by_d.setdefault(len(p), []).append(p)
    tm = .8
    for d in sorted(by_d):
        s = ''
        for p in by_d[d]:
            n = node_at(TREE, p); x, y = pos[p]
            if d:   # the branch into this node, drawn with the node
                par = pos[p[:-1]]; s += L(par[0], par[1] + 13, x, y - 11, RULE_HI, 1.2)
                mx, my = (par[0] + x) / 2, (par[1] + 13 + y - 11) / 2; yes = p[-1] == 'y'
                s += T(mx + (-14 if yes else 14), my - 6, 'yes' if yes else 'no', FA, 'end' if yes else 'start')
        f.show(s, tm)
        s = ''
        for p in by_d[d]:
            n = node_at(TREE, p); x, y = pos[p]
            s += leafp(x, y, n['leaf'], n['ids']) if 'leaf' in n else dt.qbox(x, y, n['q'])
        f.show(s, tm + .15); tm += 1.1
    assert all(LAB[c] == node_at(TREE, p)['leaf'] for p in pos if 'leaf' in node_at(TREE, p)
               for c in node_at(TREE, p)['ids'].split())
    f.show(pill(97, 244, 'train error 0 / 6', 'gr', 150), tm + .2)
    return finish(f, 300)

# ---------- 02 High variance ----------
def fig_variance():
    f = Anim('tf2-', 720, 0, 'Two trees grown to purity on two random 90 percent samples of the same 300 noisy points. Both get '
             'their own training rows 100 percent right, but their regions differ in many small boxes. The third panel '
             'paints in red where the two trees disagree: %s of the test points fall there.' % pct(DIS_T),
             'SAME DATA · DROP A DIFFERENT 10% · A DIFFERENT TREE')
    size, y0 = 200, 40
    for k, (tree, P, name, e, x0) in enumerate(((TA, SA, 'tree A', err(TA, TE), 0), (TB, SB, 'tree B', err(TB, TE), 250))):
        t0 = .3 + k * 1.6
        f.static(frame(x0, y0, size))
        f.show(region(x0, y0, size, lambda x, y, t=tree: pred(t, (x, y)), P), t0)
        f.show(S(x0, y0 + size + 22, name + ' · 90% sample', TX, bold=True) +
               S(x0, y0 + size + 40, '%d leaves · train 0%%' % len(leaves(tree)), MU) +
               S(x0, y0 + size + 58, 'test error ' + pct(e), MU), t0 + .3)
    x0 = 500
    f.static(frame(x0, y0, size))
    f.show(raster(x0, y0, size, lambda x, y: pred(TA, (x, y)) != pred(TB, (x, y)), tint('rd', '.22')) +
           R(x0, y0, size, size, 'none', RULE_HI, 4, 1), 3.6)
    dis = [q for q in TE if pred(TA, q) != pred(TB, q)]
    f.show(''.join('<circle cx="%.1f" cy="%.1f" r="2.4" fill="%s"/>' % (x0 + q[0] * size, y0 + (1 - q[1]) * size, RD)
                   for q in dis), 4.4)
    assert len(dis) == round(DIS_T * len(TE))
    f.show(S(x0, y0 + size + 22, 'A and B disagree', RD, bold=True) +
           S(x0, y0 + size + 40, 'red zone · test points in it', MU) +
           S(x0, y0 + size + 58, '%d of %d = %s' % (len(dis), len(TE), pct(DIS_T)), RD, bold=True), 4.8)
    names = ('x', 'y')
    def top(t): return [(t['f'], t['t']), (t['L']['f'], t['L']['t']), (t['R']['f'], t['R']['t'])]
    tops = [top(TA), top(TB)]
    for k, (tree, x0) in enumerate(((TA, 0), (TB, 250))):
        yt = y0 + size + 92; cx = x0 + size / 2; t0 = 5.4 + k * .8
        q = ['%s < %.2f ?' % (names[fc], th) for fc, th in tops[k]]
        diff = [tops[0][j] != tops[1][j] for j in range(3)]
        s = ''
        for side, j in ((-1, 1), (1, 2)):
            s += L(cx, yt + 13, cx + side * 52, yt + 46, RULE_HI, 1.2)
            s += T(cx + side * 52, yt + 90, '+%d leaves' % len(leaves(tree['L' if side < 0 else 'R'])), FA, mono=True)
        s += dt.qbox(cx, yt, q[0]) if not diff[0] else dt.qring(cx, yt, q[0], RO)
        for side, j in ((-1, 1), (1, 2)):
            s += dt.qbox(cx + side * 52, yt + 58, q[j]) if not diff[j] else dt.qring(cx + side * 52, yt + 58, q[j], RO)
        f.show(s, t0)
    assert tops[0][0] == tops[1][0] and tops[0][1:] != tops[1][1:]
    f.show(S(500, y0 + size + 108, 'same root question', MU) + S(500, y0 + size + 126, 'different questions below it', RO, bold=True) +
           S(500, y0 + size + 144, 'outlined = differs between A and B', MU), 6.4)
    return finish(f, y0 + size + 186)

# ---------- 03 Timeline ----------
EVENTS = [(1984, 'CART', 'one'), (1993, 'C4.5', 'one'), (1996, 'Bagging', 'bag'), (1997, 'AdaBoost', 'bst'),
          (2001, 'Random forest', 'bag'), (2001, 'Gradient boosting', 'bst'), (2014, 'XGBoost', 'bst'),
          (2017, 'LightGBM', 'bst'), (2017, 'CatBoost', 'bst')]
def fig_timeline():
    f = Anim('tf3-', 720, 0, 'A time axis from 1980 to 2020 with three lanes. One tree: CART 1984, C4.5 1993. Bagging: Bagging '
             '1996, Random forest 2001. Boosting: AdaBoost 1997, Gradient boosting 2001, XGBoost 2014, LightGBM and CatBoost 2017. After '
             '1996 every new name is a way to combine trees, and after 2001 only the boosting lane keeps growing.',
             'ONE TREE → MANY TREES IN PARALLEL · MANY TREES IN SERIES')
    X = lambda yr: 140 + (yr - 1980) / 40 * 560
    lanes = {'one': (66, TX, 'one tree'), 'bag': (130, BAG, 'bagging'), 'bst': (194, BST, 'boosting')}
    yb = 252
    f.static(L(X(1980), yb, X(2020), yb, RULE_HI, 1.3))
    for yr in range(1980, 2021, 10):
        f.static(L(X(yr), yb - 3, X(yr), yb + 3, RULE_HI, 1) + T(X(yr), yb + 17, str(yr), FA, mono=True))
    for key, (y, c, name) in lanes.items():
        f.static(S(0, y + 4, name, c, bold=True) + L(X(1980), y, X(2020), y, RULE, 1, '2 4'))
    order = sorted(EVENTS, key=lambda e: e[0]); prev = {}; t = .4
    for yr, name, lane in order:
        y, c, _ = lanes[lane]
        seg = L(X(prev[lane]), y, X(yr), y, c, 2.2) if lane in prev else ''
        if lane != 'one' and lane not in prev:          # a lane is born from the single tree
            seg = L(X(1984), lanes['one'][0], X(yr), y, c, 1.4, '4 3')
        f.show(seg, t)
        up = name not in ('Gradient boosting', 'LightGBM', 'AdaBoost', 'Bagging')
        anc = {'CatBoost': 'start', 'XGBoost': 'end', 'LightGBM': 'start', 'AdaBoost': 'end', 'Bagging': 'end', 'Gradient boosting': 'start'}.get(name, 'middle')
        dx = {'end': 4, 'start': -4}.get(anc, 0)
        f.show(dot(X(yr), y, c, 5.5, BG) + T(X(yr) + dx, y - 12 if up else y + 22, name, c, anc, bold=True) +
               T(X(yr) + dx, (y - 12 if up else y + 22) + (-12 if up else 12), str(yr), FA, anc, mono=True), t + .2)
        prev[lane] = yr; t += .7
    assert [e[0] for e in order] == sorted(e[0] for e in EVENTS)
    return finish(f, yb + 28)

# ---------- 04 Ensembles on the six customers: bagging / boosting (same figure kind) ----------
TCOLS = ['age', 'income', 'bought before']
def toy_cart(rs, d=0, maxd=2):
    """Gini CART on rows of DATA; returns a decision_tree-style dict (q / yes / no, leaf / ids)."""
    k = sum(r[4] for r in rs)
    if d == maxd or k in (0, len(rs)):
        assert 2 * k != len(rs)
        return {'leaf': 'buy' if 2 * k > len(rs) else 'no', 'ids': ' '.join(sorted(r[0] for r in rs))}
    best = None
    for c in range(3):
        vs = sorted(set(r[c + 1] for r in rs))
        for a, b in zip(vs, vs[1:]):
            t = (a + b) / 2; Lr = [r for r in rs if r[c + 1] < t]; Rr = [r for r in rs if r[c + 1] >= t]
            w = len(Lr) * dt.gini(Lr) + len(Rr) * dt.gini(Rr)
            if best is None or w < best[0] - 1e-9: best = (w, c, t, Lr, Rr)
    _, c, t, Lr, Rr = best
    return {'q': '%s < %g ?' % (TCOLS[c], t), 'yes': toy_cart(Lr, d + 1, maxd), 'no': toy_cart(Rr, d + 1, maxd)}

BAG_SEED = 7
_g = random.Random(BAG_SEED)
BAGS = [[DATA[_g.randrange(6)] for _ in range(6)] for _ in range(3)]
BTREES = [toy_cart(b) for b in BAGS]
BVOTES = [dt.walk_x(t, dt.XR)[1] for t in BTREES]
assert [''.join(r[0] for r in b) for b in BAGS] == ['CBDFAA', 'EACEAE', 'BAADDA']
assert BVOTES == ['buy', 'no', 'buy']
assert all('bought' not in str(t) for t in BTREES)
BAG_ANS = 'buy' if BVOTES.count('buy') * 2 > 3 else 'no'
assert BAG_ANS == 'buy'

# boosting: squared-error gradient boosting with stumps, learning rate 1, F0 = mean of y
def toy_stump(r):
    best = None
    for c in range(3):
        vs = sorted(set(d[c + 1] for d in DATA))
        for a, b in zip(vs, vs[1:]):
            t = (a + b) / 2; Li = [i for i, d in enumerate(DATA) if d[c + 1] < t]; Ri = [i for i in range(6) if i not in Li]
            ml = sum(r[i] for i in Li) / len(Li); mr = sum(r[i] for i in Ri) / len(Ri)
            sse = sum((r[i] - ml) ** 2 for i in Li) + sum((r[i] - mr) ** 2 for i in Ri)
            if best is None or sse < best[0] - 1e-9: best = (sse, TCOLS[c], t, ml, mr, Li)
    return best[1:]
F0 = sum(d[4] for d in DATA) / 6
BF = [[F0] * 6]; BR_ = []; BSTUMPS = []
for _ in range(3):
    F = BF[-1]; r = [d[4] - F[i] for i, d in enumerate(DATA)]; BR_.append(r)
    col, t, a, b, Li = toy_stump(r); BSTUMPS.append((col, t, a, b, Li))
    BF.append([F[i] + (a if i in Li else b) for i in range(6)])
BR_.append([d[4] - BF[-1][i] for i, d in enumerate(DATA)])
assert [(s[0], s[1]) for s in BSTUMPS] == [('age', 31.5), ('age', 46.5), ('age', 56)]
assert [round(v, 3) for v in BF[-1]] == [.025, .025, .775, .775, .4, 1.0]
assert all((v >= .5) == bool(d[4]) for v, d in zip(BF[-1], DATA))
XSUM = [F0] + [a if dt.XR[c] < t else b for c, t, a, b, _ in BSTUMPS]
assert [round(v, 3) for v in XSUM] == [.5, .25, .125, -.1] and round(sum(XSUM), 3) == .775

def num(v):
    s = '%g' % round(v, 3)
    return s.replace('-', '−')
def sgn(v): return ('+ ' if v >= 0 else '− ') + ('%g' % round(abs(v), 3))

def fig_bagging():
    f = Anim('tf4-', 720, 0, 'The six-customer table. Three bags are drawn from it with replacement: rows slide out, some twice, '
             'some not at all. A tree is grown on each bag, in parallel: %s. The new customer X, age 45, income 31, walks '
             'each tree: the votes are buy, no buy, buy. They slide into a tally: two buy against one no buy, so the forest '
             'says buy. On the 300 noisy points one deep tree has test error %s, %d bagged trees %s.' % (
                 '; '.join(t['q'] for t in BTREES), pct(err(dt.FULL, TE)), RF_N, pct(RF_E)),
             'SAMPLE ROWS · ONE TREE PER BAG · IN PARALLEL · VOTE')
    tb = Table(0, 30, [('id', 28), ('age', 40), ('income', 48), ('buy?', 46)])
    f.static(tb.head())
    for i, r in enumerate(DATA):
        f.static(tb.row(i, [r[0], str(r[1]), str(r[2]), LAB[r[0]]], colors={3: CL[LAB[r[0]]]}))
    CW, CH = 44, 20
    span = [(180, 334), (334, 565), (565, 720)]          # width shared by leaf count: 2 + 3 + 2
    assert [len(dt.leaves(t)) if False else str(t).count("'leaf'") for t in BTREES] == [2, 3, 2]
    xs = [a for a, b in span]; ctr = [(a + b) / 2 for a, b in span]
    for k, bag in enumerate(BAGS):
        cx0 = ctr[k]; t0 = .4 + k * 1.5
        f.show(T(cx0, 42, 'bag %d' % (k + 1), BAG, bold=True), t0)
        for j, r in enumerate(bag):
            cx = cx0 + (j % 3 - 1) * (CW + 5); cy = 62 + (j // 3) * 26
            lab = LAB[r[0]]; c = CL[lab]
            chipsvg = (R(cx - CW / 2, cy - CH / 2, CW, CH, BG, 'none', 4) + R(cx - CW / 2, cy - CH / 2, CW, CH, tn(c, '.12'), c, 4, 1.1) +
                       T(cx - 12, cy + 4, r[0], TX, bold=True) + T(cx + 8, cy + 4, 'buy' if lab == 'buy' else 'no', c))
            i = DATA.index(r); sx, sy = tb.x + tb.w / 2, tb.ry(i) + 13
            f.path(chipsvg, [(0, sx - cx, sy - cy), (t0 + .2 + j * .18, 0, 0)], t0 + j * .18, d=.55)
        dup = [n for n in 'ABCDEF' if sum(r[0] == n for r in bag) > 1]
        miss = [n for n in 'ABCDEF' if all(r[0] != n for r in bag)]
        f.show(T(cx0, 110, 'twice: %s · out: %s' % (' '.join(dup) or '–', ' '.join(miss) or '–'), FA, mono=True), t0 + 1.4)
    pos = []
    for k, tree in enumerate(BTREES):
        p = layout(tree, span[k][0], span[k][1], 150, 56); pos.append(p)
        f.show(arrow(ctr[k], 116, ctr[k], 132, BAG, 1.2), 5.0 + k * .3)
        f.show(draw_tree(tree, p), 5.2 + k * .3)
    f.show(S(xs[0], 316, 'grown in parallel · no tree sees the others', BAG, bold=True), 6.2, hide=7.0)
    f.show(R(0, tb.ry(5) + 40, 170, 24, BG, VI, 6, 1.4) + T(85, tb.ry(5) + 56, 'X · age 45 · income 31', VI, bold=True), 7.0)
    slots = [(14 + k * 62, 340) for k in range(3)]
    f.show(S(0, 322, 'votes', MU, bold=True), 7.0)
    t = 7.6
    for k, tree in enumerate(BTREES):
        steps, lab, end = dt.walk_x(tree, dt.XR); p = pos[k]
        for j, (q, ch, *_r) in enumerate(steps):
            f.show(dt.edge_hl(p, q, ch), t + j * .4)
        for j, (q, *_r) in enumerate(steps):
            f.show(dt.qring(*p[q], node_at(tree, q)['q']), t + j * .4)
        x, y = p[end]; tl = t + len(steps) * .4
        f.show(dt.lring(x, y, lab), tl)
        vw = 54
        v = chip(0, 0, 'buy' if lab == 'buy' else 'no', CL[lab], vw, mono=False)
        sx, sy = slots[k]
        sx += vw / 2
        f.path('<g transform="translate(%.1f,%.1f)">%s</g>' % (sx, sy, v), [(0, x - sx, y - sy), (tl + .5, 0, 0)], tl + .3, d=.8)
        t = tl + .9
    nb = BVOTES.count('buy')
    f.show(chip(85, 374, '%d buy · %d no → buy' % (nb, 3 - nb), FI, 168), 13.4)
    f.show(S(200, 378, 'on the 300 points: one deep tree %s → %d bagged trees %s' % (pct(err(dt.FULL, TE)), RF_N, pct(RF_E)),
             MU), 13.8)
    assert RF_E < err(dt.FULL, TE)
    return finish(f, 392)

def stump_draw(cx, y, q, a, b, dy=60):
    s = ''
    for side, v in ((-1, a), (1, b)):
        lx = cx + side * 40
        s += L(cx, y + 13, lx, y + dy - 11, RULE_HI, 1.2)
        s += T((cx + lx) / 2 + side * 12, y + dy / 2 - 2, 'yes' if side < 0 else 'no', FA, 'end' if side < 0 else 'start')
        s += chip(lx, y + dy, num(v), VI, 58)
    return s + dt.qbox(cx, y, q)

def fig_boosting():
    f = Anim('tf5-', 720, 0, 'The six-customer table with y as 0 or 1, the running score F, starting at the mean 0.5, and the '
             'leftover y minus F. Stump 1 is fitted to the leftover column: age under 31.5, leaves %s and %s. Each leaf value '
             'travels to its rows and is added to F; the leftover column is recomputed and the rows still wrong are outlined. '
             'Stump 2, age under 46.5, and stump 3, age under 56, repeat this on the updated column, until all six rows are '
             'right. The new customer X, age 45, walks the three stumps in order: 0.5 + 0.25 + 0.125 − 0.1 = 0.775, buy. '
             'On the 300 points one stump has test error %s, %d stumps %s.' % (
                 num(BSTUMPS[0][2]), num(BSTUMPS[0][3]), pct(err(STUMP1, TE)), GB_N, pct(GB_E)),
             'FIT A STUMP TO WHAT IS LEFT · ADD IT · REPEAT · IN SERIES')
    tb = Table(0, 30, [('id', 28), ('age', 40), ('y', 34), ('F', 54), ('y − F', 54)])
    f.static(tb.head())
    for i, r in enumerate(DATA):
        f.static(tb.row(i, [r[0], str(r[1]), str(r[4]), num(BF[0][i]), num(BR_[0][i])], colors={2: CL[LAB[r[0]]]}))
    xs = [318 + k * 160 for k in range(3)]
    gap = tb.w + 16
    for k, (col, th, a, b, Li) in enumerate(BSTUMPS):
        t0 = .6 + k * 7.0; cx = xs[k]
        f.show(tb.colbox(4, 6, HL), t0, hide=t0 + 1.4)
        f.show(T(cx, 44, 'stump %d · fits y − F' % (k + 1), VI, bold=True), t0 + .4)
        f.show(stump_draw(cx, 74, '%s < %g ?' % (col, th), a, b), t0 + .6)
        if k: f.show(arrow(xs[k - 1] + 74, 74, cx - 56, 74, VI, 1.2), t0 + .4)
        for i in range(6):
            left = i in Li; lx = cx + (-40 if left else 40); ly = 134
            v = a if left else b; tx, ty = tb.cx(3), tb.ry(i) + 13; ts = t0 + 1.3 + i * .8
            cs = chip(0, 0, num(v), VI, 46)
            # leaf -> down to the lane under the stumps -> left to the gap -> to the row -> into the F cell
            # one chip at a time leaves the leaf: drop to its own row's height, slide left, into the F cell
            pts = [(0, lx - tx, ly - ty), (ts, lx - tx, 0), (ts + .4, gap - tx, 0), (ts + .8, 0, 0)]
            f.path('<g transform="translate(%.1f,%.1f)">%s</g>' % (tx, ty, cs), pts, ts - .3, d=.35, hide=ts + 1.3)
            f.show(tb.cell(i, 3, num(BF[k + 1][i]), 'bl'), ts + 1.2)
            f.show(tb.cell(i, 4, num(BR_[k + 1][i])), ts + 1.5)
        wrong = [i for i in range(6) if (BF[k + 1][i] >= .5) != bool(DATA[i][4])]
        tw = t0 + 6.4
        for i in wrong:
            f.show(tb.outline(i, c=RD, sw=1.8), tw, hide=(t0 + 7.0) if k < 2 else None)
        if k == 2:
            assert not wrong
            f.show(pill(tb.w / 2, tb.ry(5) + 34, 'F ≥ 0.5 ↔ y = 1 · 6 / 6 right', 'gr', 200), tw)
    assert [i for i in range(6) if (BF[1][i] >= .5) != bool(DATA[i][4])] == [4]
    tx0 = 21.6
    f.show(R(0, 270, 170, 24, BG, HL, 6, 1.4) + T(85, 286, 'X · age 45 · income 31', HL, bold=True), tx0)
    f.show(S(250, 280, 'X:', MU, bold=True) + chip(296, 276, 'F0 ' + num(F0), BR, 62), tx0)
    for k, (col, th, a, b, Li) in enumerate(BSTUMPS):
        t = tx0 + .5 + k * 1.1; cx = xs[k]
        yes = dt.XR[col] < th; lx = cx + (-40 if yes else 40)
        f.show(L(cx, 87, lx, 123, HL, 2.4), t)
        f.show(dt.qring(cx, 74, '%s < %g ?' % (col, th)), t)
        f.show(chip(lx, 134, num(XSUM[k + 1]), VI, 58) + R(lx - 32, 120, 64, 28, 'none', HL, 14, 1.8), t + .3)
        sx = 370 + k * 70
        f.path('<g transform="translate(%.1f,276)">%s</g>' % (sx, chip(0, 0, sgn(XSUM[k + 1]), VI, 62)),
               [(0, lx - sx, 134 - 276), (t + .5, 0, 0)], t + .3, d=.6)
    f.show(chip(640, 276, '= %s → buy' % num(sum(XSUM)), FI, 120), tx0 + 4.2)
    f.show(S(250, 318, 'on the 300 points: one stump %s → %d stumps %s' % (pct(err(STUMP1, TE)), GB_N, pct(GB_E)), MU),
           tx0 + 4.6)
    assert GB_E < err(STUMP1, TE)
    return finish(f, 330)

# ---------- 5.1 Bagging vs boosting ----------
def fig_curves():
    f = Anim('tf6-', 720, 0, 'Test error against the number of trees on a log scale, same 300 points. Random forest falls from '
             '%s with one tree and then stays flat: more trees never hurt. Boosted stumps start at %s, fall faster to %s at '
             '%d stumps, then climb back to %s at 1000: they need early stopping.' % (
                 pct(RFC[0][2]), pct(GBC[0][2]), pct(GB_BEST[2]), GB_BEST[0], pct(GBC[-1][2])),
             'MORE TREES · FOREST FLATTENS · BOOSTING OVERSHOOTS')
    x0, x1, yb, yt = 60, 560, 262, 50
    PX = lambda n: x0 + math.log10(n) / 3 * (x1 - x0)
    PY = lambda e: yb - e / .4 * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for e in (.1, .2, .3, .4):
        f.static(T(x0 - 7, PY(e) + 4, '%d%%' % (e * 100), FA, 'end', mono=True) + L(x0, PY(e), x1, PY(e), RULE, .8))
    for n in (1, 10, 100, 1000): f.static(T(PX(n), yb + 15, str(n), FA, mono=True))
    f.static(S(x1, yb + 34, 'number of trees', MU, 'end') + S(x0, yt - 12, 'test error', MU))
    for k, (curve, c) in enumerate(((RFC, BAG), (GBC, BST))):
        for i, (n, tr, te) in enumerate(curve):
            t = .3 + k * 3.6 + i * .22
            seg = L(PX(curve[i - 1][0]), PY(curve[i - 1][2]), PX(n), PY(te), c, 2.2) if i else ''
            f.show(seg + dot(PX(n), PY(te), c, 3.6), t)
    f.show('<circle cx="%.1f" cy="%.1f" r="10" fill="none" stroke="%s" stroke-width="2"/>' % (PX(GB_BEST[0]), PY(GB_BEST[2]), GR) +
           S(PX(GB_BEST[0]), PY(GB_BEST[2]) + 28, 'stop here · %d stumps · %s' % (GB_BEST[0], pct(GB_BEST[2])), GR, 'middle', bold=True), 7.4)
    f.show(L(PX(GB_BEST[0]), PY(GB_BEST[2]) - 10, PX(GB_BEST[0]), yt, GR, 1, '3 3'), 7.4)
    X1 = 590
    f.show(S(X1, 90, 'random forest', BAG, bold=True) + S(X1, 108, '1 tree %s' % pct(RFC[0][2]), MU) +
           S(X1, 126, '1000 trees %s' % pct(RFC[-1][2]), MU), 3.4)
    f.show(S(X1, 168, 'boosted stumps', BST, bold=True) + S(X1, 186, '1 stump %s' % pct(GBC[0][2]), MU) +
           S(X1, 204, '1000 stumps %s' % pct(GBC[-1][2]), RD), 7.0)
    assert RFC[-1][2] <= RFC[0][2] - .05 and GBC[-1][2] > GB_BEST[2] + .03 and GB_BEST[2] < min(c[2] for c in RFC)
    return finish(f, yb + 46)

# ---------- 5.2 XGBoost vs LightGBM: level-wise vs leaf-wise ----------
def tree_pos(t, x0, x1, y0, dy):
    order, pos = [], {}
    def walk(u, p):
        if 'f' in u: walk(u['L'], p + 'L'); walk(u['R'], p + 'R')
        else: order.append(p)
        pos[p] = [None, y0 + len(p) * dy, u]
    walk(t, '')
    for i, p in enumerate(order): pos[p][0] = x0 + (x1 - x0) * (i + .5) / len(order)
    def setx(p):
        u = pos[p][2]
        if 'f' not in u: return pos[p][0]
        pos[p][0] = (setx(p + 'L') + setx(p + 'R')) / 2; return pos[p][0]
    setx(''); return pos

def fig_growth():
    f = Anim('tf7-', 720, 0, 'Two trees grown with the same budget of 7 splits, numbered in the order they happen. Level-wise, as '
             'in XGBoost: split every node on one level before going deeper, a balanced tree of depth %d. Leaf-wise, as in '
             'LightGBM: always split the leaf with the biggest gain, a lopsided tree of depth %d. Test error %s versus %s.' % (
                 gdepth(LEVEL), gdepth(LEAF), pct(LV_E), pct(LF_E)),
             'SAME 7 SPLITS · LEVEL BY LEVEL OR BIGGEST GAIN FIRST')
    dy = 46
    for k, (tree, x0, x1, name, sub, e, tr) in enumerate(((LEVEL, 0, 340, 'level-wise', 'XGBoost default', LV_E, LV_TR),
                                                          (LEAF, 380, 720, 'leaf-wise', 'LightGBM default', LF_E, LF_TR))):
        pos = tree_pos(tree, x0 + 10, x1 - 10, 64, dy)
        f.static(S(x0, 40, name, TX, bold=True) + S(x0 + 80, 40, '· ' + sub, MU))
        f.static(dot(pos[''][0], pos[''][1], RULE_HI, 4))
        splits = sorted((pos[p][2]['o'], p) for p in pos if 'f' in pos[p][2])
        for o, p in splits:
            x, y, u = pos[p]; t = .4 + k * 5.0 + (o - 1) * .6
            s = ''
            for ch in 'LR':
                cx, cy, v = pos[p + ch]
                s += L(x, y, cx, cy, RULE_HI, 1.3) + dot(cx, cy, RULE_HI, 4)
            f.show(s, t)
            f.show(R(x - 10, y - 10, 20, 20, BG, 'none', 10) + '<circle cx="%.1f" cy="%.1f" r="10" fill="%s" stroke="%s" '
                   'stroke-width="1.4"/>' % (x, y, tn(BST, '.14'), BST) + T(x, y + 4, str(o), BST, mono=True, bold=True), t)
        yl = 64 + max(gdepth(LEVEL), gdepth(LEAF)) * dy + 34
        f.show(S(x0, yl, 'depth %d · %d leaves' % (gdepth(tree), len(leaves(tree))), MU) +
               S(x0, yl + 18, 'train %s · test %s' % (pct(tr), pct(e)), TX, bold=True), .4 + k * 5.0 + 4.4)
    assert gdepth(LEVEL) == 4 and gdepth(LEAF) == 6 and LF_TR < LV_TR and len(leaves(LEVEL)) == len(leaves(LEAF)) == 8
    return finish(f, 64 + max(gdepth(LEVEL), gdepth(LEAF)) * dy + 66)

# ---------- 06 Learning order ----------
ORDER = [('Decision tree', '../decision-tree/index.html', 'one'), ('Random forest', '../random-forest/index.html', 'bag'),
         ('AdaBoost', '../adaboost/index.html', 'bst'), ('Gradient boosting', '../gradient-boosting/index.html', 'bst'),
         ('XGBoost', '../xgboost/index.html', 'bst'), ('LightGBM', '../lightgbm/index.html', 'bst')]
def fig_order():
    f = Anim('tf8-', 720, 0, 'Six lessons as boxes. Decision tree first, outlined as the start. From it two lanes: the bagging lane '
             'holds Random forest; the boosting lane runs AdaBoost, Gradient boosting, then XGBoost and LightGBM side by side. '
             'Boxes light up in reading order, 1 to 6.', 'START WITH ONE TREE · THEN EACH LANE ADDS ONE IDEA')
    W, H = 128, 34
    P = {'Decision tree': (0, 104), 'Random forest': (196, 46), 'AdaBoost': (196, 162), 'Gradient boosting': (350, 162),
         'XGBoost': (504, 128), 'LightGBM': (504, 196)}
    colr = {'one': AM, 'bag': BAG, 'bst': BST}
    f.static(S(196, 34, 'bagging', BAG, bold=True) + S(196, 150, 'boosting', BST, bold=True))
    def box(name, k, lane):
        x, y = P[name]; c = colr[lane]
        return (R(x, y, W, H, BG, 'none', 6) + R(x, y, W, H, tn(c, '.12') if lane != 'one' else tint('am', '.14'), c, 6, 1.6) +
                T(x + 18, y + 22, str(k), c, mono=True, bold=True) + T(x + 30, y + 22, name, c, 'start', bold=True))
    def edge(a, b, c):
        (xa, ya), (xb, yb) = P[a], P[b]
        return arrow(xa + W, ya + H / 2, xb - 6, yb + H / 2, c, 1.4)
    t = .3
    for k, (name, _, lane) in enumerate(ORDER, 1):
        f.show(box(name, k, lane), t)
        if name == 'Random forest': f.show(edge('Decision tree', name, BAG), t - .3)
        if name == 'AdaBoost': f.show(edge('Decision tree', name, BST), t - .3)
        if name == 'Gradient boosting': f.show(edge('AdaBoost', name, BST), t - .3)
        if name in ('XGBoost', 'LightGBM'): f.show(edge('Gradient boosting', name, BST), t - .3)
        t += .9
    f.show(S(0, 252, 'each box needs only the boxes to its left', MU), t)
    return finish(f, 262)

SCRIPT = re.search(r'<script>.*?</script>', dt.BODY, re.S).group(0)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Tree models</p>
  <h1>Tree <em>models</em> overview</h1>
  <p class="lede">One tree is easy to read but fragile, so the whole branch is about <b>combining many trees</b> — in parallel (bagging) or in series (boosting).</p>
</header>

<section id="treeintro-s1" class="lesson">
  <div class="sh"><b>01</b><h2>One tree</h2></div>
  <p class="key">The first idea: no formula, just <em>yes/no questions on one column at a time</em>.</p>
{tf1}
  <ul class="why">
    <li>Mixed columns, no scaling, thresholds and interactions for free — why trees rule tabular data.</li>
    <li>How the questions are chosen: <a href="../decision-tree/index.html">Decision tree</a>.</li>
  </ul>
</section>

<section id="treeintro-s2" class="lesson">
  <div class="sh"><b>02</b><h2>High variance</h2></div>
  <p class="key">A full-grown tree <em>memorises its sample</em>: drop a few rows and it draws different boxes.</p>
{tf2}
  <ul class="why">
    <li>Each tree is wrong in its own places — so many of them can <b>cancel each other out</b>.</li>
    <li>Combining many weak models into one is called an <b>ensemble</b>.</li>
  </ul>
</section>

<section id="treeintro-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Timeline</h2></div>
  <p class="key">After 1996 every new name is <em>a way to combine trees</em>, not a new kind of tree.</p>
{tf3}
  <ul class="why">
    <li>Bagging stopped at one big name; boosting kept being refined.</li>
    <li>XGBoost, LightGBM and CatBoost (2017) are gradient boosting made faster and regularised, not new algorithms; CatBoost's own twist is <b>ordered boosting</b> and native handling of categorical columns.</li>
  </ul>
</section>

<section id="treeintro-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Ensembles</h2></div>
  <p class="key">Two cures for two weaknesses: <em>average deep trees</em> or <em>add up shallow ones</em>.</p>
  <div class="subsec" id="treeintro-s4-1">
    <h3 class="ssh"><b>4.1</b>Bagging</h3>
    <p class="skey">Grow many deep trees on <em>bootstrap samples</em>, in parallel, and let them vote.</p>
{tf4}
    <ul class="why">
      <li>Two forests grown on the two samples of section 02 disagree on only <b>{dis_f}</b> of test points, against {dis_t} for two trees.</li>
      <li>A random forest also lets each split see only a random subset of columns — <a href="../random-forest/index.html">Random forest</a>.</li>
    </ul>
  </div>
  <div class="subsec" id="treeintro-s4-2">
    <h3 class="ssh"><b>4.2</b>Boosting</h3>
    <p class="skey">Grow many shallow trees <em>one after another</em>, each fitted to what is still wrong, and add them up.</p>
{tf5}
    <ul class="why">
      <li>Re-weight the wrong rows: <a href="../adaboost/index.html">AdaBoost</a>. Fit the remaining error directly: <a href="../gradient-boosting/index.html">Gradient boosting</a>.</li>
      <li>Each step is scaled by a <b>learning rate</b> ({lr} for the 300 points; 1 in the six-row toy so the numbers stay readable), so no single tree decides much.</li>
    </ul>
  </div>
</section>

<section id="treeintro-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Comparison</h2></div>
  <p class="key">Pick the lane by <em>what the single tree lacks</em>; inside boosting, pick the library by data size.</p>
  <div class="subsec" id="treeintro-s5-1">
    <h3 class="ssh"><b>5.1</b>Bagging vs boosting</h3>
    <p class="skey">More trees is <em>always safe</em> for a forest; boosting <em>overshoots</em> and needs early stopping.</p>
{tf6}
  <table>
    <tr><th></th><th>Bagging · random forest</th><th>Boosting · GBM, XGBoost, LightGBM, CatBoost</th></tr>
    <tr><td>Base tree</td><td>deep, fully grown</td><td>shallow, 1–6 levels</td></tr>
    <tr><td>Built</td><td>in parallel, independent</td><td>in series, each on the leftover error</td></tr>
    <tr><td>Cures</td><td>variance</td><td>bias</td></tr>
    <tr><td>Tuning</td><td>defaults are near-best</td><td>learning rate, depth, early stopping</td></tr>
    <tr><td>Noisy labels</td><td>tolerates them</td><td>later trees chase them</td></tr>
  </table>
    <ul class="why">
      <li>Quick, robust baseline: random forest. Highest score with a good validation set: boosting.</li>
    </ul>
  </div>
  <div class="subsec" id="treeintro-s5-2">
    <h3 class="ssh"><b>5.2</b>XGBoost vs LightGBM</h3>
    <p class="skey">Same gradient boosting objective; they differ in <em>which leaf they split next</em>.</p>
{tf7}
    <ul class="why">
      <li>Leaf-wise spends every split where the gain is biggest, so it reaches lower error with the same budget — but its deep branches can memorise small data, so cap <code>num_leaves</code> and <code>min_data_in_leaf</code>.</li>
      <li>LightGBM also bins values into histograms and takes categorical columns directly: choose it for millions of rows or frequent retraining.</li>
    </ul>
  </div>
</section>

<section id="treeintro-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Learning order</h2></div>
  <p class="key">Start with one tree; each lesson after it <em>adds exactly one idea</em>.</p>
{tf8}
  <ul class="why">
    <li><a href="../decision-tree/index.html">Decision tree</a> → <a href="../random-forest/index.html">Random forest</a> → <a href="../adaboost/index.html">AdaBoost</a> → <a href="../gradient-boosting/index.html">Gradient boosting</a> → <a href="../xgboost/index.html">XGBoost</a> · <a href="../lightgbm/index.html">LightGBM</a>.</li>
    <li>Skip straight to XGBoost and you only learn which function to call.</li>
  </ul>
</section>

{script}

<footer>Machine learning · Tree models · next lesson in the branch: <a href="../decision-tree/index.html">Decision tree</a>.</footer>
'''

def build():
    figs = dict(tf1=fig_one(), tf2=fig_variance(), tf3=fig_timeline(), tf4=fig_bagging(), tf5=fig_boosting(),
                tf6=fig_curves(), tf7=fig_growth(), tf8=fig_order(), dis_f=pct(DIS_F), dis_t=pct(DIS_T), lr='%g' % LR,
                script=SCRIPT)
    return re.sub(r'\{(tf\d+|dis_f|dis_t|lr|script)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    dt.splice(PAGE, build(), 'One tree memorises and flips with the data; bagging averages deep trees, boosting adds up '
              'shallow ones. Timeline, comparison and learning order of the branch.')
