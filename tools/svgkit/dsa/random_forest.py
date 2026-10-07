# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/06-tree-models/random-forest.
Built on decision_tree.py: the same six customers A-F for a toy forest of three trees, and the same
300 noisy points (circle boundary) for the measured numbers. Every number is computed here.
Run: python3 random_forest.py"""
import os, re, sys, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from decision_tree import (DATA, LAB, CL, HL, gini, var, pt, legend, qbox, qring, lring, leafp, layout, node_at,
                           edge_hl, make, TR, TE, FULL, err, splice)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, finish)
from tablefig import GR, tint, pill

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/06-tree-models/random-forest/index.html')
ROW = {r[0]: r for r in DATA}
COLN = ['age', 'income', 'bought before']

# ---------- the toy forest: three bootstrap bags of the six customers ----------
_g = random.Random(5842)
BAGS = [''.join(DATA[_g.randrange(6)][0] for _ in range(6)) for _ in range(3)]
assert BAGS == ['BFDBCF', 'DAAEDA', 'ACCABB']
OOB = [''.join(c for c in 'ABCDEF' if c not in b) for b in BAGS]
assert OOB == ['AE', 'BCF', 'DEF']

def rows(ids): return [ROW[c] for c in ids]
def side(rs, c, t): return frozenset(r[0] for r in rs if r[c + 1] < t)

def best_split(rs, cols, imp):
    """best (gain, col, thr) over the given columns; the first best wins; a tie between two DIFFERENT
    partitions is refused, so the figures never depend on how a tie is broken"""
    cs = []
    for c in cols:
        vs = sorted(set(r[c + 1] for r in rs))
        for a, b in zip(vs, vs[1:]):
            t = (a + b) / 2; Lr = [r for r in rs if r[c + 1] < t]; Rr = [r for r in rs if r[c + 1] >= t]
            cs.append((round(imp(rs) - len(Lr) / len(rs) * imp(Lr) - len(Rr) / len(rs) * imp(Rr), 9), c, t))
    m = max(g for g, _, _ in cs)
    w = [x for x in cs if x[0] == m]
    ids = frozenset(r[0] for r in rs)
    assert len(set(min(side(rs, c, t), ids - side(rs, c, t), key=sorted) for _, c, t in w)) == 1, 'real tie'
    return w[0]

def col_best(rs, c, imp):
    return max((x for x in [best_split(rs, [c], imp)]), key=lambda x: x[0])

def qtext(c, t):
    return 'never bought ?' if c == 2 else '%s < %g ?' % (COLN[c], t)

def grow(ids_list, draws, imp, done, leafval):
    """draws: iterator of the columns each split may look at (preorder)."""
    rs = ids_list
    if done(rs): return {'leaf': leafval(rs), 'ids': ' '.join(r[0] for r in rs), 'rows': rs}
    S = next(draws); g, c, t = best_split(rs, S, imp)
    return {'q': qtext(c, t), 'c': c, 't': t, 'g': g, 'S': S, 'n': len(rs),
            'yes': grow([r for r in rs if r[c + 1] < t], draws, imp, done, leafval),
            'no': grow([r for r in rs if r[c + 1] >= t], draws, imp, done, leafval)}

pure = lambda rs: len(set(r[4] for r in rs)) == 1
same = lambda rs: len(set(r[5] for r in rs)) == 1
cls_leaf = lambda rs: 'buy' if rs[0][4] else 'no'
reg_leaf = lambda rs: sum(r[5] for r in rs) / len(rs)
# the two columns each split drew (max_features = 2 of 3), in preorder
DRAWN = [[(1, 2), (0, 1)], [(0, 1), (0, 1)], [(1, 2)]]
CT = [grow(rows(b), iter(d), gini, pure, cls_leaf) for b, d in zip(BAGS, DRAWN)]
RT = [grow(rows(b), iter([(0, 1, 2)] * 9), var, same, reg_leaf) for b in BAGS]   # regression: every column

def walk(tree, rec):
    p, out = '', []
    while 'leaf' not in node_at(tree, p):
        n = node_at(tree, p); ch = 'y' if rec[n['c']] < n['t'] else 'n'; out.append((p, ch)); p += ch
    return out, node_at(tree, p)['leaf'], p

def nodes(t): return [] if 'leaf' in t else [t] + nodes(t['yes']) + nodes(t['no'])
X = (45, 31, 0)          # new customer: age 45, income 31, never bought
VOTES = [walk(t, X)[1] for t in CT]
MEANS = [walk(t, X)[1] for t in RT]
assert [n['q'] for n in nodes(CT[0])] == ['income < 24 ?', 'age < 31.5 ?']
assert [n['q'] for n in nodes(CT[1])] == ['age < 32.5 ?', 'age < 46.5 ?'] and [n['q'] for n in nodes(CT[2])] == ['never bought ?']
assert VOTES == ['buy', 'buy', 'no'] and MEANS == [34, 34, 30] and round(sum(MEANS) / 3, 1) == 32.7
assert [n['q'] for n in nodes(RT[0])] == ['age < 31.5 ?', 'age < 38 ?', 'age < 50.5 ?']
# random features at the root of tree 1: age would win with every column
G1 = [col_best(rows(BAGS[0]), c, gini) for c in range(3)]
assert [(round(g, 3), t) for g, _, t in G1] == [(.444, 31.5), (.222, 24), (.111, .5)]
# out-of-bag votes
OOBV = []
for r in DATA:
    vs = [(k, walk(t, r[1:4])[1]) for k, (t, o) in enumerate(zip(CT, OOB)) if r[0] in o]
    nb = sum(v == 'buy' for _, v in vs); assert 2 * nb != len(vs)
    OOBV.append((r[0], vs, 'buy' if 2 * nb > len(vs) else 'no'))
OOB_OK = sum(v == LAB[i] for i, _, v in OOBV)
assert OOB_OK == 4 and [i for i, _, v in OOBV if v != LAB[i]] == ['E', 'F']
# MDI of the toy forest: per tree, sum share-of-rows x gain per column, normalise, then average the trees
def mdi(t):
    s = [0, 0, 0]
    for n in nodes(t): s[n['c']] += n['n'] / 6 * n['g']
    return [v / sum(s) for v in s]
TMDI = [mdi(t) for t in CT]
FMDI = [sum(m[j] for m in TMDI) / 3 for j in range(3)]
assert [[round(v, 2) for v in m] for m in TMDI] == [[.5, .5, 0], [1, 0, 0], [0, 0, 1]]
assert [round(v, 3) for v in FMDI] == [.5, .167, .333]

# ---------- a real forest on the 300 noisy points of decision_tree.py ----------
def g2(k, n): p = k / n; return 1 - p * p - (1 - p) ** 2
def bgrow(P, rng, mf, nf, imp):
    n = len(P); k = sum(q[-1] for q in P); node = dict(n=n, k=k)
    if k == 0 or k == n: return node
    feats = rng.sample(range(nf), mf); best = None
    while True:
        for f in feats:
            Sp = sorted(P, key=lambda q: q[f]); lk = 0
            for i in range(1, n):
                lk += Sp[i - 1][-1]
                if Sp[i][f] == Sp[i - 1][f]: continue
                w = i / n * g2(lk, i) + (n - i) / n * g2(k - lk, n - i)
                if best is None or w < best[0] - 1e-12: best = (w, f, (Sp[i - 1][f] + Sp[i][f]) / 2)
        if best is not None and g2(k, n) - best[0] > 1e-12: break
        rest = [f for f in range(nf) if f not in feats]     # like sklearn: keep looking if the drawn ones fail
        if not rest: return node
        feats = rest
    w, f, t = best; node.update(f=f, t=t); imp[f] += n * (g2(k, n) - w)
    node['L'] = bgrow([q for q in P if q[f] < t], rng, mf, nf, imp)
    node['R'] = bgrow([q for q in P if q[f] >= t], rng, mf, nf, imp)
    return node
def bpr(t, q):
    while 'f' in t: t = t['L'] if q[t['f']] < t['t'] else t['R']
    return t['k'] / t['n']
def forest(P, B, mf, nf, seed):
    rng = random.Random(seed); F = []
    for _ in range(B):
        bag = [P[rng.randrange(len(P))] for _ in P]; imp = [0] * nf
        t = bgrow(bag, rng, mf, nf, imp); F.append((t, [v / sum(imp) for v in imp]))
    return F
def acc(F, P): return sum((sum(bpr(t, q) for t, _ in F) / len(F) > .5) == q[-1] for q in P) / len(P)

E_TREE = err(FULL, TE)
E_BAG = 1 - acc(forest(TR, 100, 2, 2, 11), TE)
E_RF = 1 - acc(forest(TR, 100, 1, 2, 11), TE)
assert round(E_TREE, 3) == .21 and round(E_BAG, 3) == .15 and round(E_RF, 3) == .137
# feature importance: add a column of pure noise, max_features = 1 (sqrt of 3, rounded down, as in sklearn)
_n = random.Random(5)
TR3 = [(x, y, _n.random(), c) for x, y, c in TR]; TE3 = [(x, y, _n.random(), c) for x, y, c in TE]
F3 = forest(TR3, 100, 1, 3, 11)
BMDI = [sum(m[j] for _, m in F3) / len(F3) for j in range(3)]
BASE = acc(F3, TE3)
def shuffled(j, r):
    col = [q[j] for q in TE3]; random.Random(100 + r).shuffle(col)
    return [tuple(col[i] if k == j else q[k] for k in range(4)) for i, q in enumerate(TE3)]
PACC = [sum(acc(F3, shuffled(j, r)) for r in range(5)) / 5 for j in range(3)]
PERM = [BASE - a for a in PACC]
assert round(BASE, 3) == .85 and [round(v, 3) for v in BMDI] == [.369, .403, .228]
assert [round(v, 3) for v in PERM] == [.177, .18, -.012]

# ---------- drawing helpers ----------
def cellid(x, y, c, w=22):
    lab = LAB[c]
    return R(x, y, w, 22, BG, 'none', 4) + R(x, y, w, 22, tn(CL[lab], '.14'), CL[lab], 4, 1.2) + T(x + w / 2, y + 15.5, c, CL[lab], bold=True)

def numleaf(cx, cy, v, ids=None, w=50, c=VI):
    s = R(cx - w / 2, cy - 11, w, 22, BG, 'none', 11) + R(cx - w / 2, cy - 11, w, 22, tn(c, '.14'), c, 11, 1.3)
    s += T(cx, cy + 4, '%g' % v, c, bold=True, mono=True)
    if ids: s += T(cx, cy + 26, ids, FA, mono=True)
    return s

def nring(cx, cy, v, w=50):
    return numleaf(cx, cy, v, w=w) + R(cx - w / 2 - 3, cy - 14, w + 6, 28, 'none', HL, 14, 1.8)

def draw_t(tree, pos, ids=True, reg=False):
    s = ''
    for p, (x, y) in pos.items():
        n = node_at(tree, p)
        if 'leaf' in n: continue
        for ch, word in (('y', 'yes'), ('n', 'no')):
            cx, cy = pos[p + ch]; top = cy - 11
            s += L(x, y + 13, cx, top, RULE_HI, 1.2)
            mx, my = (x + cx) / 2, (y + 13 + top) / 2
            s += T(mx + (-12 if ch == 'y' else 12), my - 4, word, FA, 'end' if ch == 'y' else 'start')
    for p, (x, y) in pos.items():
        n = node_at(tree, p)
        if 'leaf' not in n: s += qbox(x, y, n['q'])
        elif reg: s += numleaf(x, y, n['leaf'], n['ids'] if ids else None)
        else: s += leafp(x, y, n['leaf'], n['ids'] if ids else None)
    return s

def xbadge(cx, y):
    s = 'new customer X · age 45 · income 31 · never bought'
    return R(cx - 150, y, 300, 26, BG, VI, 6, 1.4) + T(cx, y + 17, s, VI, bold=True)

TX0 = (0, 245, 490)   # three tree columns, 230 px each

# ---------- 01 Mental model ----------
def leaf_slots(tree, ids):
    """for each bag slot: (leaf path, index inside that leaf), rows kept in bag order"""
    out, cnt = [], {}
    for c in ids:
        p = walk(tree, ROW[c][1:4])[2]; out.append((p, cnt.get(p, 0))); cnt[p] = cnt.get(p, 0) + 1
    return out

def tree_parts(tree, pos, lw=52):
    """[(depth, svg)] edges + node of every non-root node, the root at depth 0; leaves without ids"""
    parts = []
    for p, (x, y) in pos.items():
        n = node_at(tree, p); s = ''
        if p:
            px, py = pos[p[:-1]]; ch = p[-1]
            s += L(px, py + 13, x, y - 11, RULE_HI, 1.2)
            mx, my = (px + x) / 2, (py + 13 + y - 11) / 2
            s += T(mx + (-10 if ch == 'y' else 10), my - 3, 'yes' if ch == 'y' else 'no', FA, 'end' if ch == 'y' else 'start')
        s += leafp(x, y, n['leaf'], w=lw) if 'leaf' in n else qbox(x, y, n['q'])
        parts.append((len(p), s))
    return parts

def sring(cx, cy, lab, w=52):
    return leafp(cx, cy, lab, w=w) + R(cx - w / 2 - 3, cy - 14, w + 6, 28, 'none', HL, 14, 1.8)

def fig_mental():
    f = Anim('rf1-', 720, 0, 'The six-customer table. Three times, six rows are copied from it at random, with repeats, and '
             'slide into a bag: B F D B C F, then D A A E D A, then A C C A B B. Each bag grows its own tree: the root '
             'appears, then its children, and the bag rows drop into the leaves. The three roots ask different questions: '
             'income under 24, age under 32.5, never bought. A new customer X walks all three trees; they answer buy, buy, '
             'no buy, and the three votes slide into a tally: two to one, so the forest says buy.',
             'ONE BAG OF ROWS PER TREE · EACH BAG GROWS A TREE · EVERY TREE VOTES')
    t = Table(0, 30, [('id', 26), ('age', 38), ('income', 48), ('buy?', 42)])
    f.static(t.head())
    for i, r in enumerate(DATA):
        f.static(t.row(i, [r[0], str(r[1]), str(r[2]), LAB[r[0]]], colors={3: CL[LAB[r[0]]]}))
    CW, X0, BY, RY, DY, CS = 178, 186, 40, 104, 58, 18
    ends, walks = [], []
    for k, b in enumerate(BAGS):
        x0 = X0 + k * CW; cx = x0 + CW / 2; t0 = .3 + k * 2.6
        f.show(T(cx, BY - 6, 'bag %d' % (k + 1), MU, bold=True), t0)
        pos = layout(CT[k], x0, x0 + CW, RY, DY)
        tg = t0 + 1.4
        for d, svg in tree_parts(CT[k], pos):
            f.show(svg, tg + d * .35)
        deep = max(len(p) for p in pos)
        tdrop = tg + deep * .35 + .4
        slots = leaf_slots(CT[k], b)
        for i, c in enumerate(b):
            j = 'ABCDEF'.index(c); tt = t0 + .1 + i * .18
            bx = cx - 3 * 24 + i * 24 + 1
            lp, li = slots[i]; lx, ly = pos[lp]
            nl = sum(1 for q, _ in slots if q == lp)
            fx = lx - nl * CS / 2 + li * CS + .5; fy = ly + 15
            f.show(t.outline(j, j, c=HL, sw=1.6), tt, hide=tt + .3, d=.15)
            f.path(cellid(fx, fy, c, CS - 1), [(0, 1 - fx, t.ry(j) + 2 - fy), (tt, bx - fx, BY - fy),
                                                (tdrop + i * .06, 0, 0)], tt, d=.5)
        f.show(R(cx - 74, BY - 2, 148, 26, 'none', RULE, 5, 1, '3 3'), t0, hide=tdrop + .5)
        steps, out, end = walk(CT[k], X)
        walks.append((pos, steps, end, out)); ends.append(pos[end])
    tw = 8.6
    f.show(xbadge(360, 262), tw - .4)
    for k, (pos, steps, end, out) in enumerate(walks):
        tk = tw + k * .3
        for j, (p, ch) in enumerate(steps):
            f.show(edge_hl(pos, p, ch), tk + j * .5 + .3)
        for j, (p, ch) in enumerate(steps):
            f.show(qring(*pos[p], node_at(CT[k], p)['q']), tk + j * .5)
        f.show(sring(*pos[end], out), tk + len(steps) * .5)
    tv = tw + 2.2; YT = 316
    f.show(S(196, YT + 4, 'votes', MU, 'end', True), tv)
    for k in range(3):
        fx = 236 + k * 64; ex, ey = ends[k]
        f.path(leafp(fx, YT, VOTES[k], w=56), [(0, ex - fx, ey - YT), (tv + .3 + k * .25, 0, 0)], tv, d=.6)
    f.show(S(410, YT + 4, '2 buy · 1 no', TX, 'start', True), tv + 1.4)
    f.show(chip(600, YT, 'X → buy', FI, 110), tv + 1.9)
    return finish(f, YT + 22)

# ---------- 02 Bootstrap ----------
def fig_bootstrap():
    f = Anim('rf2-', 720, 0, 'The original six rows on the left. Six draws, with replacement, fill the bag of tree 1: B, F, D, '
             'B again, C, F again. Each draw outlines the source row and slides a copy into the next slot; a dot next to the '
             'source counts how often it was picked. B and F have two dots, A and E none: they are out-of-bag for tree 1. '
             'Bags 2 and 3 below leave out B C F and D E F.', 'SIX DRAWS WITH REPLACEMENT · REPEATS IN · SOME ROWS LEFT OUT')
    cols = [('id', 28), ('age', 40), ('income', 48), ('bought', 52), ('buy?', 44)]
    o = Table(0, 26, cols, title='ORIGINAL TABLE'); b = Table(300, 26, cols, title='BAG OF TREE 1')
    f.static(o.head() + b.head())
    vals = lambda r: [r[0], str(r[1]), str(r[2]), 'yes' if r[3] else 'no', LAB[r[0]]]
    for i, r in enumerate(DATA):
        f.static(o.row(i, vals(r), colors={4: CL[LAB[r[0]]]}))
    for k in range(6): f.static(R(b.x, b.ry(k), b.w, b.rh, 'none', RULE, 3, 1, '3 3'))
    seen = {}
    for k, c in enumerate(BAGS[0]):
        j = 'ABCDEF'.index(c); t = .6 + k * .95; m = seen.get(c, 0); seen[c] = m + 1
        f.show(o.outline(j, j, c=HL, sw=1.8), t, hide=t + .8, d=.2)
        f.path(b.row(k, vals(ROW[c]), colors={4: CL[LAB[c]]}), [(0, -b.x, o.ry(j) - b.ry(k)), (t + .3, 0, 0)], t, d=.5)
        f.show(dot(o.x + o.w + 12 + m * 11, o.ry(j) + 13, HL, 4), t + .3)
    assert seen == {'B': 2, 'F': 2, 'D': 1, 'C': 1}
    t = 6.6
    for c in OOB[0]:
        j = 'ABCDEF'.index(c)
        f.show(o.outline(j, j, c=FA, sw=1.4, dash='4 3') + S(o.x + o.w + 8, o.ry(j) + 17, 'not drawn', RO), t)
    f.show(S(540, 92, 'B, F drawn twice', TX, bold=True) + S(540, 112, 'A, E never drawn', RO, bold=True) +
           S(540, 132, '→ out-of-bag for tree 1', MU), t + .3)
    f.show(M(540, 178, 'one row is left out', MU, 'start') + M(540, 200, 'with chance (5/6)⁶ = %.0f%%' % (100 * (5 / 6) ** 6), TX, 'start') +
           M(540, 224, 'large {n}: (1 − 1/{n})ⁿ → 37%', TX, 'start'), t + .8)
    yb = o.bottom(6) + 30
    for k in (1, 2):
        y = yb + (k - 1) * 34; tt = 7.8 + (k - 1) * .6
        f.show(S(0, y + 15, 'bag %d' % (k + 1), MU, bold=True) + ''.join(cellid(52 + i * 24, y, c) for i, c in enumerate(BAGS[k])) +
               S(214, y + 15, 'out-of-bag', MU) + ''.join(cellid(290 + i * 24, y, c) for i, c in enumerate(OOB[k])), tt)
    assert round((5 / 6) ** 6, 3) == .335
    return finish(f, yb + 62)

# ---------- 03 Random features ----------
def fig_features():
    f = Anim('rf3-', 720, 0, 'The bag of tree 1 and the best cut each column can make at the root: age under 31.5 gains 0.444, '
             'income under 24 gains 0.222, bought before gains 0.111. With every column allowed, age wins. Then the split draws '
             'only two columns, income and bought before; age is greyed out, and income under 24 wins with 0.222. Below, the '
             'three trees end up with three different roots.', 'EACH SPLIT MAY ONLY LOOK AT A RANDOM FEW COLUMNS')
    cols = [('id', 28), ('age', 40), ('income', 48), ('bought', 52), ('buy?', 44)]
    t = Table(0, 26, cols, title='BAG OF TREE 1')
    f.static(t.head())
    for i, c in enumerate(BAGS[0]):
        r = ROW[c]; f.static(t.row(i, [c, str(r[1]), str(r[2]), 'yes' if r[3] else 'no', LAB[c]], colors={4: CL[LAB[c]]}))
    LX, BX, top, step = 262, 382, 70, 36
    sc = 220 / G1[0][0]
    f.static(S(LX, 48, 'best cut per column · Gini gain', MU))
    names = ['age < 31.5', 'income < 24', 'bought before ?']
    for c, (g, _, _) in enumerate(G1):
        y = top + c * step
        f.show(T(LX, y + 13, names[c], TX, 'start', 'sv-s') + R(BX, y + 2, g * sc, 16, tn(FI, '.30'), FI, 2, 1) +
               T(BX + g * sc + 8, y + 15, '%.3f' % g, MU, 'start', mono=True), .4 + c * .4)
    f.show(R(BX, top + 2, G1[0][0] * sc, 16, 'none', HL, 2, 2) + S(BX + 4, top - 6, 'all columns → age wins', HL, bold=True), 1.9, hide=3.4)
    # the draw
    f.show(S(LX, top + 3 * step + 10, 'draw 2 of 3 columns:  income, bought before', HL, bold=True), 3.4)
    f.show(t.dimcol(1, 6) + R(LX - 6, top - 2, 720 - LX + 6, step - 4, SUNK, 'none', 3).replace('/>', ' opacity=".82"/>') +
           S(BX + G1[0][0] * sc - 4, top + 15, 'not drawn', RO, 'end', True), 3.8)
    f.show(t.colbox(2, 6, HL) + t.colbox(3, 6, HL), 3.8)
    for c in (1, 2):
        y = top + c * step
        f.show(R(LX - 6, y - 2, 720 - LX + 6, step - 4, 'none', HL, 4, 1.4), 4.2)
    f.show(R(BX, top + step + 2, G1[1][0] * sc, 16, tint('gr', '.35'), GR, 2, 1.6), 5.0)
    yb = t.bottom(6) + 34
    f.show(S(0, yb, 'the three roots', MU, bold=True), 5.4)
    # the winning question leaves its bar and drops into the root slot of tree 1
    sx, sy = BX + G1[1][0] * sc + 80, top + step + 10
    f.path(qbox(140, yb + 26, CT[0]['q'], GR, 1.6), [(0, sx - 140, sy - yb - 26), (5.8, 0, 0)], 5.2, d=.9)
    for k in range(3):
        x = 140 + k * 200; tt = 6.8 + k * .4
        S_ = CT[k]['S']
        f.show((qbox(x, yb + 26, CT[k]['q']) if k else '') +
               S(x, yb + 58, 'tree %d drew %s, %s' % (k + 1, COLN[S_[0]].split()[0], COLN[S_[1]].split()[0]), FA, 'middle'), tt)
    return finish(f, yb + 70)

# ---------- 4.1 / 4.2 Aggregating ----------
def fig_agg(reg):
    trees = RT if reg else CT
    pre = 'rf5-' if reg else 'rf4-'
    outs = MEANS if reg else VOTES
    if reg:
        aria = ('Three regression trees, one per bag, every leaf a spend value. X walks each tree from the root: tree 1 ends at '
                '34, tree 2 at 34, tree 3 at 30. The three numbers slide down and are averaged: (34 + 34 + 30) / 3 = 32.7.')
        cap = 'THREE TREES · THREE WALKS · THE MEAN OF THEIR NUMBERS'
    else:
        aria = ('The three trees of the forest, each with its bag of rows under the leaves. X walks each tree: tree 1 asks '
                'income under 24, no, and lands on buy; tree 2 asks age under 32.5, no, then age under 46.5, yes, and lands on '
                'buy; tree 3 asks never bought, yes, and lands on no buy. The votes slide down: two buy, one no, so X gets buy.')
        cap = 'THREE TREES · THREE WALKS · THE MAJORITY VOTE'
    f = Anim(pre, 720, 0, aria, cap)
    f.static(xbadge(360, 26))
    dy = 58; y0 = 110
    hl_edges, hl_nodes, ends = [], [], []
    deep = 0
    for k, (tree, x0) in enumerate(zip(trees, TX0)):
        pos = layout(tree, x0, x0 + 230, y0, dy)
        deep = max(deep, max(y for _, y in pos.values()))
        f.static(S(x0 + 115, 82, 'tree %d' % (k + 1), MU, 'middle', True))
        f.static(draw_t(tree, pos, reg=reg))
        steps, out, end = walk(tree, X)
        tk = .8 + k * 1.9
        for j, (p, ch) in enumerate(steps):
            hl_edges.append((edge_hl(pos, p, ch), tk + j * .6 + .35))
            hl_nodes.append((qring(*pos[p], node_at(tree, p)['q']), tk + j * .6))
        x, y = pos[end]
        hl_nodes.append((nring(x, y, out) if reg else lring(x, y, out), tk + len(steps) * .6))
        ends.append((x0 + 115, tk + len(steps) * .6 + .3))
    for s, t in hl_edges: f.show(s, t)
    for s, t in hl_nodes: f.show(s, t)
    ya = deep + 50
    for k, (cx, t) in enumerate(ends):
        c = VI if reg else CL[outs[k]]
        f.show(chip(cx, ya, 'tree %d → %s' % (k + 1, ('%g' % outs[k]) if reg else ('buy' if outs[k] == 'buy' else 'no buy')), c, 130), t)
    yt = ya + 46
    tt = 7.0
    f.show(L(0, yt - 22, 720, yt - 22, RULE, 1), tt - .2)
    for k in range(3):
        fx = 300 + k * 60
        lab = outs[k]
        svg = numleaf(fx, yt, lab, w=46) if reg else leafp(fx, yt, lab, w=54)
        f.path(svg, [(0, ends[k][0] - fx, ya - yt), (tt + .4 + k * .25, 0, 0)], tt, d=.6)
    if reg:
        f.show(T(270, yt + 4, 'mean (', TX, 'end', 'sv-m') + T(450, yt + 4, ') = 32.7', TX, 'start', 'sv-m'), tt + 1.4)
        f.show(chip(620, yt, 'X → spend 32.7', VI, 136), tt + 2.0)
    else:
        f.show(S(270, yt + 4, 'votes', MU, 'end', True) + S(458, yt + 4, '2 buy · 1 no', TX, 'start', True), tt + 1.4)
        f.show(chip(620, yt, 'X → buy', FI, 110), tt + 2.0)
    return finish(f, yt + 22)

# ---------- 05 Why it works ----------
def fig_var():
    f = Anim('rf6-', 720, 0, 'Variance of the averaged prediction against the number of trees, for one tree variance of 1. When '
             'the trees are alike, rho 0.8, the curve drops a little and flattens at 0.8. When they differ, rho 0.2, it drops '
             'fast and flattens at 0.2. At 10 trees: 0.82 against 0.28. More trees only shrink the part above the floor.',
             'VARIANCE OF THE FOREST · BY NUMBER OF TREES · TWO VALUES OF ρ')
    x0, x1, yb, yt, Bmax = 56, 470, 250, 50, 40
    PX = lambda B: x0 + (B - 1) / (Bmax - 1) * (x1 - x0)
    PY = lambda v: yb - v * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt - 8, RULE_HI, 1.3))
    for v in (.5, 1):
        f.static(L(x0, PY(v), x1, PY(v), RULE, .8) + T(x0 - 7, PY(v) + 4, '%g' % v, FA, 'end', mono=True))
    for B in (1, 10, 20, 30, 40): f.static(T(PX(B), yb + 15, str(B), FA, mono=True))
    f.static(M(x1, yb + 36, 'number of trees  {B}', MU, 'end') + M(x0, yt - 16, 'variance  (one tree: {σ}² = 1)', MU, 'start'))
    vb = lambda rho, B: rho + (1 - rho) / B
    for k, (rho, c, lab) in enumerate(((.8, RO, 'trees alike'), (.2, GR, 'trees differ'))):
        t = .4 + k * 2.0
        f.show(poly([(PX(B), PY(vb(rho, B))) for B in range(1, Bmax + 1)], c, 2.4), t)
        f.show(L(x0, PY(rho), x1, PY(rho), c, 1.2, '5 4') + M(x1 + 10, PY(rho) + 5, '{ρ} = %g' % rho, c, 'start') +
               S(x1 + 70, PY(rho) + 4, lab, c, bold=True), t + .8)
    for k, (rho, c) in enumerate(((.8, RO), (.2, GR))):
        v = vb(rho, 10)
        f.show(dot(PX(10), PY(v), c, 5, BG) + T(PX(10) + 9, PY(v) - 8, '%.2f' % v, c, 'start', mono=True, bold=True), 4.6 + k * .3)
    assert round(vb(.8, 10), 2) == .82 and round(vb(.2, 10), 2) == .28
    f.show(S(x1 + 10, 114, 'dashed = floor ρσ²:', MU) + S(x1 + 10, 132, 'no number of trees', MU) + S(x1 + 10, 150, 'gets below it', MU), 5.4)
    f.show(S(x1 + 10, 172, 'random features lower ρ', HL, bold=True) + S(x1 + 10, 190, '→ a lower floor', HL, bold=True), 6.0)
    return finish(f, yb + 46)

# ---------- 06 OOB score ----------
def fig_oob():
    f = Anim('rf7-', 720, 0, 'One row per customer. Each row is sent only to the trees whose bag did not contain it, and their '
             'votes decide. A: tree 1 says no, right. B: tree 2 says no, right. C: tree 2 says buy, right. D: tree 3 says buy, '
             'right. E: trees 1 and 3 say buy, wrong. F: trees 2 and 3 say no, wrong. Four of six right: OOB score 0.67.',
             'EACH ROW IS VOTED ON ONLY BY THE TREES THAT NEVER SAW IT')
    t = Table(0, 26, [('row', 34), ('not in bag of', 104), ('their votes', 112), ('OOB vote', 78), ('true', 62), ('', 40)])
    f.static(t.head())
    for i, r in enumerate(DATA):
        f.static(t.row(i, [r[0], '', '', '', LAB[r[0]], ''], colors={4: CL[LAB[r[0]]]}))
    RX = 470
    f.static(S(RX, 42, 'bag', MU, bold=True) + S(RX + 170, 42, 'out-of-bag', MU, bold=True))
    for k in range(3):
        y = 58 + k * 34
        f.show(S(RX, y + 15, '%d' % (k + 1), MU, bold=True) + ''.join(cellid(RX + 14 + i * 22, y, c, 20) for i, c in enumerate(BAGS[k])) +
               ''.join(cellid(RX + 170 + i * 22, y, c, 20) for i, c in enumerate(OOB[k])), .3 + k * .3)
    for i, (rid, vs, v) in enumerate(OOBV):
        tt = 1.6 + i * .9
        f.show(t.outline(i, i, c=HL, sw=1.8), tt, hide=tt + .85, d=.2)
        for k, _ in vs:
            j = OOB[k].index(rid)
            f.show(R(RX + 170 + j * 22 - 2, 58 + k * 34 - 2, 24, 26, 'none', HL, 5, 1.8), tt, hide=tt + .85, d=.2)
        f.show(T(t.cx(1), t.ry(i) + 17, ', '.join('tree %d' % (k + 1) for k, _ in vs), TX), tt + .1)
        vc = CL[v]
        f.show(T(t.cx(2), t.ry(i) + 17, ' · '.join('buy' if w == 'buy' else 'no' for _, w in vs), vc, bold=True), tt + .3)
        f.show(t.cell(i, 3, 'buy' if v == 'buy' else 'no buy', None, c=vc), tt + .5)
        ok = v == LAB[rid]
        f.show(t.cell(i, 5, '✓' if ok else '✗', 'gr' if ok else 'rd'), tt + .7)
    f.show(pill(RX + 120, t.ry(4) + 3, 'OOB score = 4 / 6 = %.2f' % (OOB_OK / 6), 'gr', 190), 7.3)
    return finish(f, t.bottom(6) + 12)

# ---------- 7.1 MDI ----------
def fig_mdi():
    f = Anim('rf8-', 720, 0, 'The three trees again. In each, every question node pays its column the share of rows reaching it '
             'times its gain. Tree 1: income 6/6 times 0.222, age 3/6 times 0.444, so half and half. Tree 2: both nodes on age, '
             'all age. Tree 3: one node on bought before. Each tree is normalised to 1, then the forest averages: age 0.50, '
             'income 0.17, bought before 0.33.', 'EACH NODE PAYS ITS COLUMN · NORMALISE PER TREE · AVERAGE THE TREES')
    colc = [FI, VI, RO]
    y0, dy = 46, 54
    for k, (tree, x0) in enumerate(zip(CT, TX0)):
        pos = layout(tree, x0, x0 + 230, y0, dy)
        f.static(draw_t(tree, pos, ids=False))
        tk = .4 + k * 1.4
        for j, n in enumerate(nodes(tree)):
            p = next(q for q in pos if 'leaf' not in node_at(tree, q) and node_at(tree, q) is n)
            f.show(qring(*pos[p], n['q'], colc[n['c']]), tk + j * .5)
            f.show(M(x0 + 10, 196 + j * 22, '%s  %d/6 × %.3f' % (COLN[n['c']].split()[0], n['n'], n['g']), colc[n['c']], 'start'), tk + j * .5 + .2)
        f.show(S(x0 + 10, 248, '→ ' + ' · '.join('%s %.0f%%' % (COLN[j].split()[0], 100 * v) for j, v in enumerate(TMDI[k]) if v), TX, bold=True),
               tk + len(nodes(tree)) * .5 + .2)
    f.show(L(0, 264, 720, 264, RULE, 1) + S(0, 292, 'forest = mean of the three trees', MU, bold=True) +
           S(0, 310, 'each tree pays 1/3 of its shares', FA), 5.2)
    BW = 260
    for j in range(3):
        y = 278 + j * 28
        f.show(S(380, y + 13, COLN[j], TX, 'end', True) + R(392, y + 2, BW / 3, 14, 'none', RULE, 3, 1, '3 3'), 5.3)
    # every node's share (rows x gain, normalised in its tree, / 3) leaves the node and glides into its column's bar
    tt, fill = 5.7, [0, 0, 0]
    for k, (tree, x0) in enumerate(zip(CT, TX0)):
        pos = layout(tree, x0, x0 + 230, y0, dy); tot = sum(n['n'] / 6 * n['g'] for n in nodes(tree))
        for p in sorted((q for q in pos if 'leaf' not in node_at(tree, q)), key=len):
            n = node_at(tree, p); j = n['c']; v = n['n'] / 6 * n['g'] / tot / 3
            y = 278 + j * 28; bx = 392 + fill[j] * BW; w = v * BW; fill[j] += v; nx, ny = pos[p]
            f.path(R(bx, y + 2, w, 14, tn(colc[j], '.40'), colc[j], 3, 1.2) + T(bx + w / 2, y + 13, 'T%d' % (k + 1), colc[j], mono=True),
                   [(0, nx - w / 2 - bx, ny - 7 - y - 2), (tt + .3, 0, 0)], tt, d=.8)
            tt += .45
    assert [round(v, 3) for v in fill] == [round(v, 3) for v in FMDI]
    for j in range(3):
        y = 278 + j * 28
        f.show(T(392 + FMDI[j] * BW + 8, y + 14, '%.2f' % FMDI[j], colc[j], 'start', mono=True, bold=True), tt + .6)
    return finish(f, 278 + 3 * 28 + 6)

# ---------- 7.2 Permutation ----------
def fig_perm():
    P = [3, 0, 4, 1, 2]   # display shuffle of the five shown noise cells
    f = Anim('rf9-', 720, 0, 'The 300 noisy points with a third column of pure random noise. Five test rows are shown. The forest '
             'scores %.1f percent on the test set. The noise column is shuffled; accuracy stays at %.1f percent, so noise '
             'matters for nothing. Right: MDI still gives noise %.0f percent of the importance; permutation gives x %.3f, '
             'y %.3f and noise %.3f.' % (100 * BASE, 100 * PACC[2], 100 * BMDI[2], PERM[0], PERM[1], PERM[2]),
             'SHUFFLE ONE COLUMN · HOW MUCH ACCURACY IS LOST')
    t = Table(0, 26, [('x', 50), ('y', 50), ('noise', 56), ('label', 48)], title='TEST ROWS (5 OF 300)')
    f.static(t.head())
    for i in range(5):
        q = TE3[i]; f.static(t.row(i, ['%.2f' % q[0], '%.2f' % q[1], '', str(q[3])]))
    for i in range(5):
        j = P[i]   # cell of row i ends in slot j
        f.path(t.cell(j, 2, '%.2f' % TE3[i][2]), [(0, 0, t.ry(i) - t.ry(j)), (1.8, 0, 0)], .2, d=.8)
    f.show(t.colbox(2, 5, HL), 1.4)
    yb = t.bottom(5)
    f.static(S(0, yb + 24, 'accuracy', MU) + T(72, yb + 24, '%.1f%%' % (100 * BASE), TX, 'start', mono=True, bold=True))
    f.show(S(0, yb + 46, 'noise shuffled', HL, bold=True) + T(110, yb + 46, '%.1f%%' % (100 * PACC[2]), HL, 'start', mono=True, bold=True), 2.8)
    f.show(S(0, yb + 66, 'nothing lost → importance ≈ 0', GR, bold=True), 3.3)
    BX, sc = 380, 300
    f.static(R(BX, 32, 14, 10, SUNK, RULE_HI, 2, 1) + S(BX + 20, 42, 'MDI share', MU) +
             R(BX + 110, 32, 14, 10, tn(FI, '.40'), FI, 2, 1.2) + S(BX + 130, 42, 'permutation: accuracy drop', MU))
    names = ['x', 'y', 'noise']
    for j in range(3):
        y = 62 + j * 52; t0 = 3.9 + j * .5
        f.static(S(BX - 12, y + 22, names[j], TX, 'end', True))
        f.show(R(BX, y + 2, BMDI[j] * sc, 14, SUNK, RULE_HI, 2, 1) + T(BX + BMDI[j] * sc + 6, y + 14, '%.2f' % BMDI[j], MU, 'start', mono=True), t0)
        w = PERM[j] * sc
        f.show(R(BX + min(w, 0), y + 22, max(abs(w), 2), 14, tn(FI, '.40'), FI, 2, 1.2) +
               T(BX + max(w, 0) + 6, y + 34, '%+.3f' % PERM[j], FI, 'start', mono=True, bold=True), t0 + .25)
    f.show(L(BX, 56, BX, 62 + 2 * 52 + 42, RULE_HI, 1), 3.9)
    f.show(S(BX, 62 + 3 * 52 + 12, 'noise: MDI %.0f%% · permutation ≈ 0' % (100 * BMDI[2]), RO, bold=True), 5.8)
    assert sorted(P) == list(range(5))
    return finish(f, max(yb + 80, 62 + 3 * 52 + 26))

# ---------- 08 Hyperparameters ----------
MF = [(mf, 1 - acc(forest(TR3, 100, mf, 3, 11), TE3)) for mf in (1, 2, 3)]
assert [round(e, 3) for _, e in MF] == [.15, .143, .137]
def fig_hyper():
    f = Anim('rf10-', 720, 0, 'Test error of a 100-tree forest on the 300 noisy points with a noise column, for max_features 1, 2 '
             'and 3 of 3 columns: %.1f, %.1f and %.1f percent. All three lie within one percentage point of each other.'
             % tuple(100 * e for _, e in MF), 'TEST ERROR · 100 TREES · BY max_features')
    x0, yb, sc = 120, 190, 900
    f.static(L(x0 - 20, yb, 560, yb, RULE_HI, 1.3) + L(x0 - 20, yb, x0 - 20, yb - .16 * sc, RULE_HI, 1.3))
    for v in (.05, .10, .15):
        f.static(L(x0 - 20, yb - v * sc, 560, yb - v * sc, RULE, .8, '3 3') + T(x0 - 28, yb - v * sc + 4, '%d%%' % (100 * v), FA, 'end', mono=True))
    f.static(T(x0 - 28, yb + 4, '0%', FA, 'end', mono=True))
    for k, (mf, e) in enumerate(MF):
        x = x0 + k * 150; h = e * sc; t = .4 + k * .6
        f.static(T(x + 30, yb + 18, 'max_features = %d' % mf, MU, mono=True))
        f.path(R(x, yb - h, 60, h, tn(FI, '.30'), FI, 3, 1.2) + T(x + 30, yb - h - 8, '%.1f%%' % (100 * e), FI, mono=True, bold=True),
               [(0, 0, 12), (t + .1, 0, 0)], t, d=.5)
    f.static(S(x0 - 20, yb + 44, 'axis from 0: the three errors differ by under one point · 1 = sqrt(3) rounded down, the default', MU))
    return finish(f, yb + 58)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Tree models</p>
  <h1>Random <em>forest</em></h1>
  <p class="lede">A random forest grows many <a href="../decision-tree/index.html">decision trees</a>, each on its own random sample of rows and columns, and lets them <b>vote</b>.</p>
</header>

<section id="rf-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">One tree is unstable; <em>many different trees</em>, each trained on its own random bag of rows, vote it away.</p>
{rf1}
  <ul class="why">
    <li>The same six customers as <a href="../decision-tree/index.html">Decision tree</a>; there a tie made one tree answer no and another buy for X.</li>
    <li>Two sources of randomness make the trees differ: the <b>bag</b> of rows (section 02) and the <b>columns</b> each split may see (section 03).</li>
  </ul>
</section>

<section id="rf-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Bootstrap</h2></div>
  <p class="key">Each tree gets n rows drawn <em>with replacement</em> from the n training rows: some repeat, some are left out.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">P</b>(row left out)</span><em>never drawn in n draws</em></span>
      <span class="op">=</span>
      <span class="t"><span>(1 − <span class="frac"><i>1</i><i><var>n</var></i></span>)<sup><var>n</var></sup></span><em>miss it every time</em></span>
      <span class="op">→</span>
      <span class="t g"><span><span class="frac"><i>1</i><i><var>e</var></i></span> ≈ 0.37</span><em>for large n</em></span>
    </div>
  </div>
{rf2}
  <ul class="why">
    <li>The rows a tree never saw are its <b>out-of-bag</b> rows, about a third of the table — section 06 uses them.</li>
    <li>Bootstrap + averaging is <b>bagging</b> (bootstrap aggregating); <code>bootstrap=True</code> is the default.</li>
  </ul>
</section>

<section id="rf-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Random features</h2></div>
  <p class="key">At <em>every split</em>, a tree may only choose among a random few columns, so one strong column cannot win every root.</p>
{rf3}
  <ul class="why">
    <li>The draw is redone at every node: the left child of tree 1 draws again and splits on age.</li>
    <li><code>max_features</code> sets how many: <code>"sqrt"</code> (<span class="mth">√<var>p</var></span>) is the classifier default; the regressor uses all <span class="mth"><var>p</var></span> unless told otherwise.</li>
    <li>With every column allowed it is plain bagging; the column draw is what makes it a <b>random forest</b>.</li>
  </ul>
</section>

<section id="rf-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Aggregating</h2></div>
  <p class="key">A new row walks <em>every tree</em>; the forest combines their answers into one.</p>
  <div class="subsec" id="rf-s4-1">
    <h3 class="ssh"><b>4.1</b>Classification: vote</h3>
    <p class="skey">Each tree answers with its leaf's class; the <em>majority</em> wins.</p>
{rf4}
    <ul class="why">
      <li>sklearn averages the trees' <code>predict_proba</code> (soft vote) and takes the top class; with pure leaves that is the same as counting votes.</li>
    </ul>
  </div>
  <div class="subsec" id="rf-s4-2">
    <h3 class="ssh"><b>4.2</b>Regression: mean</h3>
    <p class="skey">Each tree answers with its leaf's number; the forest returns the <em>mean</em>.</p>
{rf5}
    <ul class="why">
      <li>The same bags, but each tree is a regression tree on spend; the mean of several staircases is a smoother staircase.</li>
      <li>Still no extrapolation: every tree repeats its last step, so their mean does too.</li>
    </ul>
  </div>
</section>

<section id="rf-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Why it works</h2></div>
  <p class="key">Averaging <em>B trees</em> shrinks variance, but only down to how alike the trees are.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">Var</b>(forest)</span><em>B trees, each of variance σ²</em></span>
      <span class="op">=</span>
      <span class="t r"><span><var>ρ</var> <var>σ</var><sup>2</sup></span><em>floor: ρ = correlation of two trees</em></span>
      <span class="op">+</span>
      <span class="t g"><span><span class="frac"><i>(1 − <var>ρ</var>) <var>σ</var><sup>2</sup></i><i><var>B</var></i></span></span><em>vanishes as B grows</em></span>
    </div>
  </div>
{rf6}
  <ul class="why">
    <li>Bootstrap and random features lower <span class="mth"><var>ρ</var></span>; trees are grown deep (low bias, high <span class="mth"><var>σ</var><sup>2</sup></span>) because averaging only removes variance, not <a href="../../04-core-concepts/bias-variance-tradeoff/index.html">bias</a>.</li>
    <li>On the 300 noisy points from Decision tree: one full tree {E_TREE} test error, 100 bagged trees {E_BAG}, a random forest of 100 trees {E_RF}.</li>
    <li>More trees never overfit; past a few hundred they only cost time (<code>n_estimators</code>, default 100).</li>
  </ul>
</section>

<section id="rf-s6" class="lesson">
  <div class="sh"><b>06</b><h2>OOB score</h2></div>
  <p class="key">Score each row with only the trees that <em>never saw it</em>: a free validation set.</p>
{rf7}
  <ul class="why">
    <li><code>oob_score=True</code>, then read <code>oob_score_</code>; with enough trees it lands close to <a href="../../04-core-concepts/train-val-test-cv/index.html">cross-validation</a> at no extra training.</li>
    <li>It assumes rows are independent: on time series a bag mixes past and future, and the score is too kind.</li>
  </ul>
</section>

<section id="rf-s7" class="lesson">
  <div class="sh"><b>07</b><h2>Feature importance</h2></div>
  <p class="key">Two ways to ask which column matters: <em>what its splits removed</em>, or <em>what is lost without it</em>.</p>
  <div class="subsec" id="rf-s7-1">
    <h3 class="ssh"><b>7.1</b>MDI</h3>
    <p class="skey">Mean decrease in impurity: the <a href="../decision-tree/index.html">tree importance</a> of each tree, <em>averaged over the forest</em>.</p>
{rf8}
    <ul class="why">
      <li>Free with training; read it from <code>feature_importances_</code>.</li>
      <li>Measured on the training bags, so it rewards columns with many distinct values, even pure noise.</li>
    </ul>
  </div>
  <div class="subsec" id="rf-s7-2">
    <h3 class="ssh"><b>7.2</b>Permutation</h3>
    <p class="skey">Shuffle one column on held-out rows; the <em>drop in accuracy</em> is its importance.</p>
{rf9}
    <ul class="why">
      <li><code>sklearn.inspection.permutation_importance</code>; shuffle a few times and average.</li>
      <li>Two correlated columns share the credit: shuffle one, the other still carries the signal, and both look weak.</li>
    </ul>
  </div>
</section>

<section id="rf-s8" class="lesson">
  <div class="sh"><b>08</b><h2>Hyperparameters</h2></div>
  <p class="key">Four knobs matter; the defaults are <em>usually close</em> to the best.</p>
{rf10}
  <ul class="why">
    <li><code>n_estimators</code>: more trees never hurt accuracy, only time (section 05).</li>
    <li><code>max_features</code>: fewer columns per split, less alike trees (lower <span class="mth"><var>ρ</var></span>) but weaker ones.</li>
    <li><code>max_depth</code>, <code>min_samples_leaf</code>: trees are grown deep by default; raise <code>min_samples_leaf</code> to smooth noisy leaves and shrink the model.</li>
    <li><b>Extra Trees</b> (<code>ExtraTreesClassifier</code>) also draws each split's <em>threshold</em> at random instead of searching it: faster, trees even less alike.</li>
  </ul>
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

<footer>Machine learning · Tree models · next lesson in the branch: <a href="../adaboost/index.html">AdaBoost</a>, which grows trees one after another instead of side by side.</footer>
'''

def build():
    figs = dict(rf1=fig_mental(), rf2=fig_bootstrap(), rf3=fig_features(), rf4=fig_agg(False), rf5=fig_agg(True),
                rf6=fig_var(), rf7=fig_oob(), rf8=fig_mdi(), rf9=fig_perm(), rf10=fig_hyper())
    s = re.sub(r'\{(rf\d+)\}', lambda m: figs[m.group(1)], BODY)
    for k, v in (('{E_TREE}', E_TREE), ('{E_BAG}', E_BAG), ('{E_RF}', E_RF)):
        s = s.replace(k, '%.1f%%' % (100 * v))
    return s

if __name__ == '__main__':
    splice(PAGE, build(), 'Many decision trees, each on a bootstrap bag of rows with random columns at every split, vote or '
           'average; out-of-bag rows score the forest for free.')
