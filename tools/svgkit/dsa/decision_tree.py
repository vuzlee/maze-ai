# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/06-tree-models/decision-tree.
Every number is computed here: the six-customer table (shared with knn.py) for the worked figures,
a small pure-Python CART on a seeded synthetic set for overfitting and pruning. Run: python3 decision_tree.py"""
import os, re, sys, math, random, copy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, finish)
from tablefig import GR, tint, pill

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/06-tree-models/decision-tree/index.html')

# ---------- the six customers: id, age, income, bought before, buy, spend ----------
DATA = [('A', 24, 12, 0, 0, 10), ('B', 28, 22, 0, 0, 12), ('C', 35, 18, 1, 1, 30), ('D', 41, 26, 1, 1, 34),
        ('E', 52, 30, 1, 0, 28), ('F', 60, 34, 0, 1, 36)]
COLS = ['age', 'income', 'bought before']
LAB = {r[0]: ('buy' if r[4] else 'no') for r in DATA}
CL = {'buy': FI, 'no': BR}
HL = 'var(--brand-hi)'   # the path being walked: app blue, a soft glow, not a brown frame

def gini(rs):
    if not rs: return 0
    p = sum(r[4] for r in rs) / len(rs); return 1 - p * p - (1 - p) ** 2
def var(rs):
    m = sum(r[5] for r in rs) / len(rs); return sum((r[5] - m) ** 2 for r in rs) / len(rs)
def entropy(p):
    return -sum(q * math.log2(q) for q in (p, 1 - p) if q > 0)
def scan(rs, imp):
    """every column x every threshold -> (column, threshold, gain, left ids, right ids)"""
    out = []
    for c in range(3):
        vs = sorted(set(r[c + 1] for r in rs))
        for a, b in zip(vs, vs[1:]):
            t = (a + b) / 2; Lr = [r for r in rs if r[c + 1] < t]; Rr = [r for r in rs if r[c + 1] >= t]
            g = imp(rs) - len(Lr) / len(rs) * imp(Lr) - len(Rr) / len(rs) * imp(Rr)
            out.append((COLS[c], t, g, ''.join(r[0] for r in Lr), ''.join(r[0] for r in Rr)))
    return out
def pick(rs, ids): return [r for r in rs if r[0] in ids]

CS = scan(DATA, gini); RS = scan(DATA, var)
assert max(CS, key=lambda s: s[2])[:2] == ('age', 31.5) and round(max(s[2] for s in CS), 4) == .25
assert max(RS, key=lambda s: s[2])[:2] == ('age', 31.5) and var(DATA) == 105 and round(max(s[2] for s in RS), 4) == 98
assert round(gini(pick(DATA, 'CDEF')), 4) == .375 and round(entropy(.75), 3) == .811
# level 2 of the classification tree is a TIE: income < 28 and age < 46.5 both gain 0.125
L2 = sorted(scan(pick(DATA, 'CDEF'), gini), key=lambda s: -s[2])
assert sorted((s[0], s[1], round(s[2], 4)) for s in L2[:2]) == [('age', 46.5, .125), ('income', 28, .125)] and L2[2][2] < .125
L3 = scan(pick(DATA, 'EF'), gini); assert sorted(round(s[2], 2) for s in L3) == [.5, .5, .5]
assert var(pick(DATA, 'CDEF')) == 10 and var(pick(DATA, 'AB')) == 1
# regression tree, max_depth = 2: AB splits at age 26, CDEF at age 56
assert max(scan(pick(DATA, 'CDEF'), var), key=lambda s: s[2])[:2] == ('age', 56)
RLEAF = [(20, 26, 10), (26, 31.5, 12), (31.5, 56, (30 + 34 + 28) / 3), (56, 90, 36)]
# feature importance of the tree in section 02
IMP = {'age': 6 / 6 * .25 + 2 / 6 * .5, 'income': 4 / 6 * .125, 'bought before': 0}
assert round(IMP['age'] / sum(IMP.values()), 3) == .833

# ---------- a tiny CART on a synthetic set (overfitting, pruning) ----------
def make(n, seed):
    g = random.Random(seed); P = []
    for _ in range(n):
        x, y = g.random(), g.random(); c = int((x - .5) ** 2 + (y - .5) ** 2 < .33 ** 2)
        if g.random() < .08: c = 1 - c
        P.append((x, y, c))
    return P
def sgini(P):
    if not P: return 0
    p = sum(q[2] for q in P) / len(P); return 1 - p * p - (1 - p) ** 2
def grow(P, depth=0, maxd=None, msl=1, box=(0, 1, 0, 1)):
    n = len(P); k = sum(q[2] for q in P); node = dict(n=n, k=k, imp=sgini(P), box=box)
    if (maxd is not None and depth >= maxd) or node['imp'] == 0: return node
    best = None
    for f in (0, 1):
        Sp = sorted(P, key=lambda q: q[f]); lk = 0
        for i in range(1, n):
            lk += Sp[i - 1][2]
            if Sp[i][f] == Sp[i - 1][f] or i < msl or n - i < msl: continue
            l = 1 - (lk / i) ** 2 - (1 - lk / i) ** 2; r = (k - lk) / (n - i); r = 1 - r * r - (1 - r) ** 2
            w = i / n * l + (n - i) / n * r
            if best is None or w < best[0] - 1e-12: best = (w, f, (Sp[i - 1][f] + Sp[i][f]) / 2)
    if best is None or node['imp'] - best[0] <= 1e-12: return node
    _, f, t = best; node.update(f=f, t=t)
    b1 = list(box); b2 = list(box); b1[2 * f + 1] = t; b2[2 * f] = t
    node['L'] = grow([q for q in P if q[f] < t], depth + 1, maxd, msl, tuple(b1))
    node['R'] = grow([q for q in P if q[f] >= t], depth + 1, maxd, msl, tuple(b2))
    return node
def leaves(t): return [t] if 'f' not in t else leaves(t['L']) + leaves(t['R'])
def leafc(t): return 1 if 2 * t['k'] >= t['n'] else 0
def pred(t, q):
    while 'f' in t: t = t['L'] if q[t['f']] < t['t'] else t['R']
    return leafc(t)
def err(t, P): return sum(pred(t, q) != q[2] for q in P) / len(P)
def tdepth(t): return 0 if 'f' not in t else 1 + max(tdepth(t['L']), tdepth(t['R']))
def prune_path(t, N):
    """weakest-link (cost-complexity) pruning -> [(alpha, tree)]"""
    rl = lambda u: u['n'] / N * u['imp']
    t = copy.deepcopy(t); out = [(0.0, copy.deepcopy(t))]
    while 'f' in t:
        best = [None]
        def walk(u):
            if 'f' not in u: return
            a = (rl(u) - sum(rl(v) for v in leaves(u))) / (len(leaves(u)) - 1)
            if best[0] is None or a < best[0][0] - 1e-12: best[0] = (a, u)
            walk(u['L']); walk(u['R'])
        walk(t); a, u = best[0]
        for k in ('f', 't', 'L', 'R'): u.pop(k)
        out.append((a, copy.deepcopy(t)))
    return out

TR, TE = make(300, 1), make(300, 2)
FULL = grow(TR)
DEPTHS = [(d, grow(TR, maxd=d)) for d in range(1, 13)]
CURVE = [(d, err(t, TR), err(t, TE)) for d, t in DEPTHS] + [(tdepth(FULL), 0.0, err(FULL, TE))]
assert len(leaves(FULL)) == 59 and tdepth(FULL) == 16 and round(err(FULL, TE), 3) == .21
BEST_D = min(CURVE, key=lambda c: c[2]); assert BEST_D[0] == 4 and round(BEST_D[2], 3) == .127
D4 = grow(TR, maxd=4); M10 = grow(TR, msl=10)
assert len(leaves(D4)) == 11 and len(leaves(M10)) == 19 and round(err(M10, TE), 3) == .117
PATH = [(a, len(leaves(t)), err(t, TR), err(t, TE)) for a, t in prune_path(FULL, len(TR))]
BEST_A = min(PATH, key=lambda p: (p[3], -p[1]))
assert BEST_A[1] == 9 and round(BEST_A[3], 3) == .103 and round(BEST_A[0], 4) == .0063
assert PATH[-1][1] == 1 and round(PATH[-1][0], 3) == .053

# ---------- drawing helpers ----------
def pt(x, y, lab, r=6):
    if lab == 'buy': return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, FI)
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, r - 1, BG, BR)

def legend(x, y):
    return pt(x, y - 4, 'buy', 5) + S(x + 10, y, 'buy', MU) + pt(x + 50, y - 4, 'no', 5) + S(x + 60, y, 'no', MU)

def qbox(cx, cy, s, c=RULE_HI, sw=1.2):
    w = len(s) * 6.4 + 22
    return R(cx - w / 2, cy - 13, w, 26, BG, c, 6, sw) + T(cx, cy + 4, s, TX, cls='sv-s')

def qring(cx, cy, s, c=HL):
    w = len(s) * 6.4 + 22
    fill = 'var(--brand-soft)' if c == HL else tn(c, '.12')
    return (R(cx - w / 2, cy - 13, w, 26, BG, 'none', 6) + R(cx - w / 2, cy - 13, w, 26, fill, c, 6, 1.8) +
            T(cx, cy + 4, s, c, cls='sv-s', bold=True))

def lring(cx, cy, lab, c=HL):
    """leaf at the end of the walk: the pill redrawn opaque + a ring, so a branch drawn earlier stays behind it"""
    return leafp(cx, cy, lab) + R(cx - 38, cy - 14, 76, 28, 'none', c, 14, 1.8)

def leafp(cx, cy, lab, ids=None, w=70):
    c = CL[lab]
    s = R(cx - w / 2, cy - 11, w, 22, BG, 'none', 11) + R(cx - w / 2, cy - 11, w, 22, tn(c, '.14'), c, 11, 1.3)
    s += T(cx, cy + 4, 'no buy' if lab == 'no' else 'buy', c, bold=True)
    if ids: s += T(cx, cy + 26, ids, FA, mono=True)
    return s

def layout(tree, x0, x1, y0, dy):
    """nested dict tree -> {path: (x, y)}; path is a string of y/n turns from the root"""
    pos, order = {}, []
    def walk(n, p, d):
        if 'leaf' not in n:
            walk(n['yes'], p + 'y', d + 1); walk(n['no'], p + 'n', d + 1)
        else: order.append(p)
        pos[p] = [None, y0 + d * dy]
    walk(tree, '', 0)
    for i, p in enumerate(order): pos[p][0] = x0 + (x1 - x0) * (i + .5) / len(order)
    def setx(n, p):
        if 'leaf' in n: return pos[p][0]
        pos[p][0] = (setx(n['yes'], p + 'y') + setx(n['no'], p + 'n')) / 2; return pos[p][0]
    setx(tree, ''); return pos

def node_at(tree, p):
    for ch in p: tree = tree['yes' if ch == 'y' else 'no']
    return tree

def draw_tree(tree, pos, ids=True):
    s = ''
    for p, (x, y) in pos.items():
        n = node_at(tree, p)
        if 'leaf' in n: continue
        for ch, word in (('y', 'yes'), ('n', 'no')):
            cx, cy = pos[p + ch]; top = cy - 11
            s += L(x, y + 13, cx, top, RULE_HI, 1.2)
            mx, my = (x + cx) / 2, (y + 13 + top) / 2
            s += T(mx + (-14 if ch == 'y' else 14), my - 6, word, FA, 'end' if ch == 'y' else 'start')
    for p, (x, y) in pos.items():
        n = node_at(tree, p)
        s += leafp(x, y, n['leaf'], n.get('ids') if ids else None) if 'leaf' in n else qbox(x, y, n['q'])
    return s

def edge_hl(pos, p, ch, c=HL):
    """highlighted branch; add it BEFORE the highlighted nodes so their opaque boxes cover the line ends"""
    (x, y), (cx, cy) = pos[p], pos[p + ch]
    return L(x, y + 13, cx, cy - 11, c, 2.4)

TREE = {'q': 'age < 31.5 ?', 'yes': {'leaf': 'no', 'ids': 'A B'},
        'no': {'q': 'income < 28 ?', 'yes': {'leaf': 'buy', 'ids': 'C D'},
               'no': {'q': 'age < 56 ?', 'yes': {'leaf': 'no', 'ids': 'E'}, 'no': {'leaf': 'buy', 'ids': 'F'}}}}
TREE_B = {'q': 'age < 31.5 ?', 'yes': {'leaf': 'no', 'ids': 'A B'},
          'no': {'q': 'age < 46.5 ?', 'yes': {'leaf': 'buy', 'ids': 'C D'},
                 'no': {'q': 'age < 56 ?', 'yes': {'leaf': 'no', 'ids': 'E'}, 'no': {'leaf': 'buy', 'ids': 'F'}}}}
X = (45, 31)   # a new customer: age 45, income 31

def walk_x(tree, rec):
    p, out = '', []
    while 'leaf' not in node_at(tree, p):
        q = node_at(tree, p)['q']; col, thr = q.split(' < '); thr = float(thr.rstrip(' ?'))
        v = rec[col]; ch = 'y' if v < thr else 'n'; out.append((p, ch, v, thr, col)); p += ch
    return out, node_at(tree, p)['leaf'], p

XR = {'age': X[0], 'income': X[1]}
assert walk_x(TREE, XR)[1] == 'no' and walk_x(TREE_B, XR)[1] == 'buy'

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('dt1-', 720, 0, 'The six-customer table is cut by a dashed line at age 31.5: A and B stay above and are all no, so '
             'they become a leaf. C, D, E, F slide right and are cut again at income 28: C and D are all buy, a leaf. E and '
             'F slide right once more and are cut at age 56 into two one-row leaves.',
             'CUT THE TABLE · CUT EACH MIXED HALF AGAIN · STOP WHEN A HALF IS PURE')
    cols = [('id', 28), ('age', 42), ('income', 52), ('buy?', 46)]
    tabs = [Table(x, 30, cols) for x in (0, 262, 524)]
    t0 = tabs[0]; W = t0.w; ST = 30
    f.static(t0.head())
    f.show(tabs[1].head(), 3.4); f.show(tabs[2].head(), 6.2)
    moves = {'A': [], 'B': [], 'C': [(1.6, 0, 1), (3.4, 1, 1)], 'D': [(1.6, 0, 1), (3.4, 1, 1)],
             'E': [(1.6, 0, 1), (3.4, 1, 1), (4.6, 1, 2), (6.2, 2, 2)],
             'F': [(1.6, 0, 1), (3.4, 1, 1), (4.6, 1, 2), (6.2, 2, 2), (7.4, 2, 3)]}
    for i, r in enumerate(DATA):
        svg = t0.row(i, [r[0], str(r[1]), str(r[2]), LAB[r[0]]], colors={3: CL[LAB[r[0]]]})
        f.path(svg, [(0, 0, 0)] + [(t, c * 262, k * ST) for t, c, k in moves[r[0]]], .2 + i * .1, d=.6)
    def cut(col, slot, s, t, j):
        tb = tabs[col]; y = tb.ry(slot) + 13
        f.show(tb.colbox(j, 9, HL), t - .4, hide=t + .8)
        f.show(L(tb.x - 6, y, tb.x + W + 6, y, HL, 1.6, '5 4') + R(tb.x + W / 2 - 40, y - 9, 80, 18, BG, 'none', 4) +
               T(tb.x + W / 2, y + 4, s, HL, bold=True), t)
    def leaf(col, s0, s1, lab, t, x=None):
        tb = tabs[col]
        f.show(tb.outline(s0, s1, c=GR, sw=1.8), t)
        cx = x if x is not None else tabs[col + 1].x + 44
        f.show(arrow(tb.x + W + 8, (tb.ry(s0) + tb.ry(s1) + 26) / 2, cx - 40, (tb.ry(s0) + tb.ry(s1) + 26) / 2, GR, 1.3) +
               leafp(cx, (tb.ry(s0) + tb.ry(s1) + 26) / 2, lab), t + .3)
    cut(0, 2, 'age < 31.5', 2.0, 1)
    leaf(0, 0, 1, 'no', 2.6)
    cut(1, 5, 'income < 28', 5.0, 2)
    leaf(1, 3, 4, 'buy', 5.6)
    cut(2, 7, 'age < 56', 7.8, 1)
    for s, lab in ((6, 'no'), (8, 'buy')):
        f.show(tabs[2].outline(s, s, c=GR, sw=1.8), 8.4)
    f.show(T(tabs[2].x + W / 2, tabs[2].ry(9) + 12, 'E → no buy · F → buy', GR, bold=True), 8.7)
    return finish(f, tabs[0].ry(9) + 22)

# ---------- 02 Reading a tree ----------
def fig_read():
    f = Anim('dt2-', 720, 0, 'The tree learned from the six customers. Root: age under 31.5. Internal nodes: income under 28, '
             'age under 56. Four leaves. A new customer aged 45 with income 31 walks from the root: not under 31.5, go no; '
             'income 31 not under 28, go no; age 45 under 56, go yes; the leaf says no buy. Depth is 3.',
             'ONE PREDICTION = ONE WALK FROM ROOT TO LEAF')
    pos = layout(TREE, 130, 640, 56, 72)
    f.static(draw_tree(TREE, pos))
    for d, name in enumerate(('root', 'internal node', 'internal node', 'leaves')):
        f.static(T(0, 56 + d * 72 + 4, 'depth %d' % d, FA, 'start', mono=True) + S(0, 56 + d * 72 + 20, name, MU))
    steps, lab, end = walk_x(TREE, XR)
    f.show(R(0, 318, 230, 26, BG, VI, 6, 1.4) + T(115, 335, 'new customer X · age 45 · income 31', VI, bold=True), .4)
    for k, (p, ch, *_r) in enumerate(steps):
        f.show(edge_hl(pos, p, ch), 2.0 + k * 1.3)
    t = 1.2
    for p, ch, v, thr, col in steps:
        x, y = pos[p]; q = node_at(TREE, p)['q']
        f.show(qring(x, y, q), t)
        op = '<' if ch == 'y' else '≥'
        f.show(T(x + len(q) * 3.2 + 20, y + 4, '%g %s %g' % (v, op, thr), HL, 'start', mono=True, bold=True), t + .3)
        t += 1.3
    x, y = pos[end]
    f.show(lring(x, y, lab), t)
    f.show(chip(400, 331, 'X → no buy', BR, 120), t + .5)
    assert lab == 'no' and len(steps) == 3
    return finish(f, 354)

# ---------- 3.1 Impurity (classification) ----------
def fig_gini():
    f = Anim('dt3-', 720, 0, 'Impurity against the share of buy in a node. Gini rises from 0 at a pure node to 0.5 at fifty-fifty '
             'and back to 0; entropy has the same shape but peaks at 1. The node C, D, E, F has three buy and one no, a share '
             'of 0.75: Gini 0.375, entropy 0.811.', 'IMPURITY OF A NODE · BY ITS SHARE OF buy')
    ox, oy, sx, sy = 50, 250, 360, 190
    P = lambda p, v: (ox + p * sx, oy - v * sy)
    f.static(L(ox, oy, ox + sx, oy, RULE_HI, 1.3) + L(ox, oy, ox, oy - sy - 8, RULE_HI, 1.3))
    for v in (.5, 1):
        f.static(L(ox, P(0, v)[1], ox + sx, P(0, v)[1], RULE, 1) + T(ox - 8, P(0, v)[1] + 4, '%g' % v, FA, 'end', mono=True))
    for p in (0, .5, 1):
        f.static(T(P(p, 0)[0], oy + 16, '%g' % p, FA, mono=True))
    f.static(M(ox + sx, oy + 34, 'share of buy  {p}', MU, 'end'))
    xs = [i / 60 for i in range(61)]
    f.show(poly([P(p, 2 * p * (1 - p)) for p in xs], FI, 2.4), .3)
    f.show(S(P(.5, .5)[0] + 6, P(.5, .5)[1] - 8, 'Gini', FI, bold=True), .5)
    f.show(poly([P(p, entropy(p)) for p in xs], VI, 2.4), 1.1)
    f.show(S(P(.5, 1)[0] + 6, P(.5, 1)[1] - 8, 'entropy', VI, bold=True), 1.3)
    f.show(L(P(.5, 0)[0], oy, P(.5, 0)[0], P(.5, 1)[1], RO, 1, '3 3') + S(P(.5, 0)[0] + 6, oy - 8, 'most mixed', RO), 2.4)
    X0 = 460
    f.show(S(X0, 52, 'node C D E F', MU, bold=True), 3.0)
    for i, n in enumerate('CDEF'):
        f.show(pt(X0 + 10 + i * 24, 72, LAB[n], 7), 3.1 + i * .1)
    f.show(M(X0, 106, '{p} = 3 / 4 = 0.75', TX, 'start'), 3.6)
    f.show(L(P(.75, 0)[0], oy, P(.75, 0)[0], P(.75, entropy(.75))[1], HL, 1.2, '4 3'), 3.6)
    g, e = 1 - .75 ** 2 - .25 ** 2, entropy(.75)
    f.show(dot(*P(.75, g), FI, 5.5, BG), 4.2)
    f.show(M(X0, 146, 'Gini = 1 − 0.75² − 0.25²', TX, 'start') + M(X0 + 20, 170, '= 0.375', FI, 'start'), 4.2)
    f.show(dot(*P(.75, e), VI, 5.5, BG), 5.0)
    f.show(M(X0, 210, 'entropy = − 0.75 log₂ 0.75', TX, 'start') + M(X0 + 58, 232, '− 0.25 log₂ 0.25', TX, 'start') +
           M(X0 + 20, 256, '= 0.811', VI, 'start'), 5.0)
    assert round(g, 3) == .375
    return finish(f, 292)

# ---------- 3.2 / 4.2 Finding a split ----------
def fig_scan(kind):
    reg = kind == 'reg'
    sc = RS if reg else CS
    pre = 'dt7-' if reg else 'dt4-'
    win = max(sc, key=lambda s: s[2])
    f = Anim(pre, 720, 0, ('Rows sorted by age; a dashed line steps down between rows and each position gets a bar for how much '
                           '%s it removes. Income and bought before are scanned the same way. The tallest bar is age under 31.5, '
                           'gain %s.') % ('variance' if reg else 'Gini', '98' if reg else '0.25'),
             'EVERY COLUMN × EVERY THRESHOLD · KEEP THE BIGGEST DROP')
    lc = 'spend' if reg else 'buy?'
    t = Table(0, 30, [('id', 30), ('age', 44), (lc, 52)])
    f.static(t.head())
    for i, r in enumerate(DATA):
        v = str(r[5]) if reg else LAB[r[0]]
        f.show(t.row(i, [r[0], str(r[1]), v], colors={2: TX if reg else CL[LAB[r[0]]]}), .2 + i * .08)
    yl = lambda i: t.ry(i + 1) - 2
    f.path(L(-4, yl(0), t.w + 4, yl(0), HL, 1.8, '5 4'), [(0, 0, 0)] + [(1.0 + i * .6, 0, i * 30) for i in range(1, 5)],
           1.0, d=.3, hide=4.0)
    BX, LX, top, step = 300, 196, 44, 22
    scale = 250 / win[2]
    for k, (col, thr, g, _, _) in enumerate(sc):
        y = top + k * step
        name = 'bought before ?' if col == 'bought before' else '%s < %g' % (col, thr)
        t0 = 1.2 + k * .6 if k < 5 else 4.4 + (k - 5) * .15
        w = max(g * scale, 1.5)
        f.show(T(LX, y + 13, name, TX if col == 'age' else MU, 'start', 'sv-s') +
               R(BX, y + 3, w, 14, tn(FI, '.30'), FI, 2, 1) +
               T(BX + w + 8, y + 14, ('%.1f' % g).rstrip('0').rstrip('.') if reg else '%.2f' % g, MU, 'start', mono=True), t0)
    kw = sc.index(win); y = top + kw * step
    f.show(R(BX, y + 3, win[2] * scale, 14, tint('gr', '.35'), GR, 2, 1.6), 5.6)
    f.show(L(-4, yl(1), t.w + 4, yl(1), GR, 2) , 5.6)
    f.show(pill(BX + win[2] * scale + 80, y + 1, 'best split', 'gr'), 5.9)
    yb = top + len(sc) * step + 26
    if reg:
        f.show(M(0, yb, 'gain = 105 − ( 2/6 · 1 + 4/6 · 10 ) = 98', TX, 'start'), 6.4)
    else:
        f.show(M(0, yb, 'gain = 0.50 − ( 2/6 · 0 + 4/6 · 0.375 ) = 0.25', TX, 'start'), 6.4)
    f.show(S(430, yb, 'impurity before − weighted impurity after', MU), 6.4)
    return finish(f, yb + 16)

# ---------- 3.3 Leaf & boundary ----------
def fig_boundary():
    f = Anim('dt5-', 720, 0, 'The six customers on an age by income plane. The root cut is a vertical line at age 31.5; the left '
             'side becomes a no region. The right side is cut by a horizontal line at income 28; below it is a buy region. '
             'The top right is cut at age 56 into a no and a buy region. Every region is a rectangle with sides parallel to '
             'the axes.', 'EACH LEAF OWNS A RECTANGLE OF THE PLANE')
    a0, a1, i0, i1 = 20, 66, 8, 38
    x0, x1, yb, yt = 50, 420, 270, 40
    PX = lambda a: x0 + (a - a0) / (a1 - a0) * (x1 - x0)
    PY = lambda v: yb - (v - i0) / (i1 - i0) * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for a in (30, 40, 50, 60): f.static(T(PX(a), yb + 15, str(a), FA, mono=True))
    for v in (10, 20, 30): f.static(T(x0 - 7, PY(v) + 4, str(v), FA, 'end', mono=True))
    f.static(S(x1, yb + 32, 'age', MU, 'end') + S(x0, yt - 10, 'income', MU))
    def region(a, b, u, v, lab, t):
        f.show(R(PX(a), PY(v), PX(b) - PX(a), PY(u) - PY(v), tn(CL[lab], '.12'), 'none', 0), t)
    def vcut(a, u, v, s, t):
        f.show(L(PX(a), PY(u), PX(a), PY(v), HL, 2, '6 4') + S(PX(a) + 5, PY(v) + 14, s, HL, bold=True), t)
    def hcut(a, b, v, s, t):
        f.show(L(PX(a), PY(v), PX(b), PY(v), HL, 2, '6 4') + S(PX(b) - 4, PY(v) - 6, s, HL, 'end', bold=True), t)
    vcut(31.5, i0, i1, 'age 31.5', 1.0); region(a0, 31.5, i0, i1, 'no', 1.6)
    hcut(31.5, a1, 28, 'income 28', 2.6); region(31.5, a1, i0, 28, 'buy', 3.2)
    vcut(56, 28, i1, 'age 56', 4.2); region(31.5, 56, 28, i1, 'no', 4.8); region(56, a1, 28, i1, 'buy', 4.8)
    for r in DATA:
        x, y = PX(r[1]), PY(r[2])
        f.static(pt(x, y, LAB[r[0]]) + T(x + 10, y + 4, r[0], MU, 'start', bold=True))
    f.static(legend(x0 + 10, yb + 32))
    X1 = 450
    f.show(S(X1, 56, 'leaf', MU) + S(X1 + 90, 56, 'counts', MU) + S(X1 + 176, 56, 'predict · proba', MU), 5.4)
    rows = [('A B', 0, 2, 'no'), ('C D', 2, 2, 'buy'), ('E', 0, 1, 'no'), ('F', 1, 1, 'buy')]
    for k, (ids, b, n, lab) in enumerate(rows):
        y = 84 + k * 34
        f.show(T(X1, y, ids, TX, 'start', mono=True, bold=True) + S(X1 + 90, y, '%d buy / %d' % (b, n), MU) +
               S(X1 + 176, y, ('buy' if lab == 'buy' else 'no buy'), CL[lab], bold=True) +
               T(X1 + 240, y, '%.2f' % (b / n), MU, 'start', mono=True), 5.6 + k * .3)
    f.show(L(X1, 214, 712, 214, RULE, 1), 7.0)
    f.show(S(X1, 236, 'stopped at depth 2, E and F share a leaf:', MU) +
           S(X1, 256, '1 buy / 2 → proba 0.50', VI, bold=True), 7.2)
    return finish(f, yb + 44)

# ---------- 4.1 Impurity (regression) ----------
def fig_var():
    f = Anim('dt6-', 720, 0, 'Spend values on a number line. All six customers: mean 25, the dots sit far from it, variance 105. '
             'Node C, D, E, F: values 30, 34, 28, 36, mean 32, deviations 2 and 4 each side, variance 10.',
             'IMPURITY OF A NODE · HOW FAR VALUES SIT FROM THEIR MEAN')
    x0, sc = 40, 9.5
    PX = lambda v: x0 + v * sc
    def row(y, ids, t0, label):
        rs = pick(DATA, ids); m = sum(r[5] for r in rs) / len(rs); vv = var(rs)
        f.static(L(PX(0), y, PX(40), y, RULE_HI, 1.3))
        for v in (0, 10, 20, 30, 40): f.static(L(PX(v), y - 3, PX(v), y + 3, RULE_HI, 1) + T(PX(v), y + 17, str(v), FA, mono=True))
        f.static(S(0, y - 62, label, MU, bold=True))
        for k, r in enumerate(sorted(rs, key=lambda r: r[5])):
            f.show(dot(PX(r[5]), y, FI, 5.5, BG) + T(PX(r[5]), y - 10, r[0], MU, bold=True), t0 + k * .12)
        f.show(L(PX(m), y - 50, PX(m), y + 6, HL, 2) + T(PX(m), y - 54, 'mean %g' % m, HL, bold=True), t0 + 1.0)
        for k, r in enumerate(sorted(rs, key=lambda r: r[5])):
            yy = y - 22 - k * 4
            f.show(L(PX(m), yy, PX(r[5]), yy, RO, 1.6), t0 + 1.6 + k * .12)
        f.show(M(450, y - 22, 'mean of (value − %g)²' % m, TX, 'start') + M(470, y + 2, '= %g' % vv, FI, 'start'), t0 + 2.4)
        return vv
    assert row(110, 'ABCDEF', .3, 'all six customers') == 105
    assert row(240, 'CDEF', 3.2, 'node C D E F') == 10
    f.show(S(0, 284, 'squared distance to the mean, averaged: 0 when every value is equal, no upper cap', MU), 6.2)
    return finish(f, 298)

# ---------- 4.3 Leaf & staircase ----------
def fig_stairs():
    f = Anim('dt8-', 720, 0, 'Spend against age for the six customers. The first cut at 31.5 gives two flat levels, 11 and 32. '
             'The second cuts at 26 and 56 refine them into four flat steps: 10, 12, 30.7 and 36. Past the last customer at 60 '
             'the line stays flat: a customer aged 85 still gets 36.', 'EACH LEAF RETURNS ONE NUMBER · THE MEAN OF ITS ROWS')
    a0, a1, x0, x1, yb, yt = 20, 88, 50, 640, 250, 40
    PX = lambda a: x0 + (a - a0) / (a1 - a0) * (x1 - x0)
    PY = lambda v: yb - v / 40 * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for a in (30, 40, 50, 60, 70, 80): f.static(T(PX(a), yb + 15, str(a), FA, mono=True))
    for v in (10, 20, 30, 40): f.static(T(x0 - 7, PY(v) + 4, str(v), FA, 'end', mono=True) + L(x0, PY(v), x1, PY(v), RULE, .8))
    f.static(S(x1, yb + 32, 'age', MU, 'end') + S(x0, yt - 12, 'spend', MU))
    f.static(R(PX(60), yt, PX(a1) - PX(60), yb - yt, tn(RO, '.06'), 'none', 0) + S(PX(74), yb - 12, 'no training data here', RO, 'middle'))
    for r in DATA:
        f.static(dot(PX(r[1]), PY(r[5]), FI, 5, BG) + T(PX(r[1]) + 9, PY(r[5]) + 14, r[0], MU, 'start', bold=True))
    def step(a, b, v, c, w=2.6, dash=None): return L(PX(a), PY(v), PX(b), PY(v), c, w, dash)
    lvl1 = [(20, 31.5, 11), (31.5, 60, 32)]
    for a, b, v in lvl1: f.show(step(a, b, v, VI), .8, hide=3.0)
    f.show(S(PX(25), PY(11) - 10, 'mean 11', VI) + S(PX(44), PY(32) - 10, 'mean 32', VI), 1.0, hide=3.0)
    f.show(S(x0 + 10, yb - 10, 'depth 1 · one cut at 31.5', VI), .8, hide=3.0)
    for k, (a, b, v) in enumerate(RLEAF[:3] + [(56, 60, 36)]):
        f.show(step(a, b, v, GR), 3.2 + k * .3)
    f.show(S(x0 + 10, yb - 10, 'depth 2 · cuts at 26 · 31.5 · 56', GR), 3.2)
    f.show(S(PX(45.5), PY(RLEAF[2][2]) + 17, 'mean %.1f' % RLEAF[2][2], GR, 'middle'), 4.2)
    f.show(step(60, 86, 36, GR, 2, '6 4'), 5.2)
    f.show(dot(PX(85), PY(36), HL, 6, BG) + L(PX(85), PY(36) + 6, PX(85), yb, HL, 1, '3 3'), 5.8)
    f.show(chip(PX(73), PY(36) + 26, 'age 85 → 36', BR, 110), 6.2)
    assert round(RLEAF[2][2], 1) == 30.7
    return finish(f, yb + 44)

# ---------- 5.1 Overfitting ----------
def fig_overfit():
    f = Anim('dt9-', 720, 0, 'Error against tree depth on 300 noisy points. Training error falls all the way to 0 as the tree '
             'deepens. Test error falls until depth 4, 12.7%%, then climbs back to %.0f%% for the full tree of 59 leaves.' %
             (100 * CURVE[-1][2]), 'DEEPER TREE · TRAIN ERROR ↓ · TEST ERROR ↓ THEN ↑')
    x0, x1, yb, yt = 60, 540, 262, 56
    pos = lambda i: x0 + 20 + i * 34
    PY = lambda e: yb - e / .4 * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for e in (.1, .2, .3, .4): f.static(T(x0 - 7, PY(e) + 4, '%d%%' % (e * 100), FA, 'end', mono=True) + L(x0, PY(e), x1, PY(e), RULE, .8))
    for i, c in enumerate(CURVE):
        f.static(T(pos(i) + (12 if i == 12 else 0), yb + 15, 'full' if i == 12 else str(c[0]), FA, mono=True))
    f.static(S(x1, yb + 34, 'max_depth', MU, 'end') + S(x0, yt - 12, 'error', MU))
    xi = lambda i: pos(i) + (12 if i == 12 else 0)
    for i, (d, tr, te) in enumerate(CURVE):
        t = .3 + i * .3
        seg = ''
        if i: seg = L(xi(i - 1), PY(CURVE[i - 1][1]), xi(i), PY(tr), FI, 2) + L(xi(i - 1), PY(CURVE[i - 1][2]), xi(i), PY(te), VI, 2)
        f.show(seg + dot(xi(i), PY(tr), FI, 4) + dot(xi(i), PY(te), VI, 4), t)
    f.show(S(xi(9), PY(CURVE[9][1]) + 18, 'train', FI, 'middle', bold=True) + S(xi(9), PY(CURVE[9][2]) - 10, 'test', VI, 'middle', bold=True), 3.4)
    bi = [c[0] for c in CURVE].index(BEST_D[0])
    t = .3 + len(CURVE) * .3 + .4
    f.show('<circle cx="%.1f" cy="%.1f" r="10" fill="none" stroke="%s" stroke-width="2"/>' % (xi(bi), PY(BEST_D[2]), GR) +
           S(xi(bi), PY(BEST_D[2]) + 28, 'depth 4 · test %.1f%%' % (BEST_D[2] * 100), GR, 'middle', bold=True), t)
    f.show('<circle cx="%.1f" cy="%.1f" r="10" fill="none" stroke="%s" stroke-width="2"/>' % (xi(12), PY(CURVE[-1][2]), RO), t + .6)
    X1 = 560
    f.show(S(X1, 70, 'full tree', RO, bold=True) + S(X1, 90, '59 leaves · depth 16', MU) +
           S(X1, 110, 'train 0%%  ·  test %.0f%%' % (CURVE[-1][2] * 100), RO), t + .6)
    f.show(S(X1, 160, 'the extra leaves', MU) + S(X1, 178, 'memorise the 8% noise', MU), t + 1.2)
    return finish(f, yb + 46)

# ---------- 5.2 Instability ----------
def fig_unstable():
    f = Anim('dt10-', 740, 0, 'At the second level two splits tie: income under 28 and age under 46.5 both gain 0.125. Taking '
             'either gives a tree that fits all six rows. The new customer aged 45 with income 31 gets no buy from the first '
             'tree and buy from the second.', 'TWO SPLITS TIE · TWO TREES · TWO ANSWERS FOR THE SAME X')
    f.static(S(0, 40, 'node C D E F, best splits:', MU))
    for k, (s, c) in enumerate((('income < 28', VI), ('age < 46.5', RO))):
        y = 52 + k * 24
        f.show(T(190, y + 12, s, c, 'start', 'sv-s', bold=True) + R(290, y + 2, 125 * 2, 14, tn(c, '.25'), c, 2, 1.2) +
               T(550, y + 13, '0.125', MU, 'start', mono=True), .3 + k * .4)
    f.show(S(600, 76, '= tie', HL, bold=True), 1.3)
    for k, (tree, c, x0) in enumerate(((TREE, VI, 0), (TREE_B, RO, 380))):
        pos = layout(tree, x0 + 14, x0 + 340, 134, 70)
        t0 = 1.8 + k * 1.4
        f.show(draw_tree(tree, pos), t0)
        steps, lab, end = walk_x(tree, XR)
        for j, (p, ch, *_r) in enumerate(steps):
            f.show(edge_hl(pos, p, ch), 4.8 + k * 1.6 + j * .35)
        for p, *_r in steps:   # path nodes redrawn opaque on top of the branches; the tied node keeps its colour
            f.show(qring(*pos[p], node_at(tree, p)['q'], c) if p == 'n' else qbox(*pos[p], node_at(tree, p)['q']),
                   t0 + .3 if p == 'n' else 4.8 + k * 1.6)
        x, y = pos[end]
        f.show(lring(x, y, lab), 4.8 + k * 1.6 + 1.1)
        f.show(chip(x0 + 175, 394, 'X → ' + ('no buy' if lab == 'no' else 'buy'), CL[lab], 120), 4.8 + k * 1.6 + 1.4)
    f.show(S(360, 430, 'same data · same training error 0 · opposite answers', RO, 'middle', bold=True), 8.4)
    return finish(f, 442)

# ---------- 5.3 Pre-pruning ----------
def panel(f, x0, tree, title, sub, t0, y0=40, size=200):
    s = R(x0, y0, size, size, BG, RULE_HI, 4, 1)
    for lf in leaves(tree):
        a, b, u, v = lf['box']
        if leafc(lf):
            s += R(x0 + a * size, y0 + (1 - v) * size, (b - a) * size, (v - u) * size, tn(FI, '.20'), 'none', 0)
    for lf in leaves(tree):
        a, b, u, v = lf['box']
        s += R(x0 + a * size, y0 + (1 - v) * size, (b - a) * size, (v - u) * size, 'none', tn(FI, '.35'), 0, .6)
    pts = ''
    for q in TR:
        x, y = x0 + q[0] * size, y0 + (1 - q[1]) * size
        pts += ('<circle cx="%.1f" cy="%.1f" r="2.2" fill="%s"/>' % (x, y, FI) if q[2] else
                '<circle cx="%.1f" cy="%.1f" r="1.8" fill="none" stroke="%s" stroke-width="1"/>' % (x, y, BR))
    f.static(R(x0, y0, size, size, BG, RULE_HI, 4, 1))
    f.show(s + pts, t0)
    f.show(S(x0, y0 + size + 22, title, TX, bold=True) +
           S(x0, y0 + size + 40, '%d leaves' % len(leaves(tree)), MU) +
           S(x0, y0 + size + 58, 'train %.1f%% · test %.1f%%' % (100 * err(tree, TR), 100 * err(tree, TE)), MU), t0 + .3)
    if sub: f.show(S(x0, y0 + size + 76, sub, GR if 'best' in sub else RO, bold=True), t0 + .6)

def fig_prepruning():
    f = Anim('dt11-', 720, 0, 'Three trees on the same 300 noisy points from a circular boundary. Unlimited: 59 leaves, many tiny '
             'boxes around single noisy points. max_depth 4: 11 leaves, a blocky circle. min_samples_leaf 10: 19 leaves, '
             'the lowest test error.', 'SAME DATA · STOP THE TREE EARLY · FEWER, BIGGER BOXES')
    panel(f, 0, FULL, 'no limit', 'memorises noise', .3)
    panel(f, 250, D4, 'max_depth = 4', '', 1.6)
    panel(f, 500, M10, 'min_samples_leaf = 10', 'best test here', 2.9)
    return finish(f, 330)

# ---------- 5.4 Post-pruning ----------
def fig_postpruning():
    f = Anim('dt12-', 720, 0, 'Grow the full tree, then raise alpha. Each step removes the weakest branch, so the number of leaves '
             'falls from 59 to 1. Training error rises steadily; test error falls to 10.3 percent at 9 leaves, alpha 0.0063, '
             'then rises again when too much is cut.', 'GROW FULLY · THEN RAISE α · ONE BRANCH CUT AT A TIME')
    x0, x1, yb, yt = 60, 560, 262, 56
    PX = lambda n: x1 - (n - 1) / 58 * (x1 - x0)
    PY = lambda e: yb - e / .4 * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for e in (.1, .2, .3, .4): f.static(T(x0 - 7, PY(e) + 4, '%d%%' % (e * 100), FA, 'end', mono=True) + L(x0, PY(e), x1, PY(e), RULE, .8))
    for n in (59, 40, 20, 9, 1): f.static(T(PX(n), yb + 15, str(n), FA, mono=True))
    f.static(S(x0, yb + 34, 'number of leaves', MU) + S(x0, yt - 12, 'error', MU))
    f.static(arrow(x1 - 10, yb + 30, x1 - 120, yb + 30, HL, 1.4) + S(x1 - 128, yb + 34, 'α grows', HL, 'end'))
    for i, (a, n, tr, te) in enumerate(PATH):
        t = .3 + i * .25; seg = ''
        if i:
            pa = PATH[i - 1]
            seg = L(PX(pa[1]), PY(pa[2]), PX(n), PY(tr), FI, 2) + L(PX(pa[1]), PY(pa[3]), PX(n), PY(te), VI, 2)
        f.show(seg + dot(PX(n), PY(tr), FI, 3.6) + dot(PX(n), PY(te), VI, 3.6), t)
    f.show(S(PX(59) - 4, PY(PATH[0][3]) - 12, 'test', VI, 'end', bold=True) + S(PX(59) - 4, PY(0) - 8, 'train', FI, 'end', bold=True), .5)
    t = .3 + len(PATH) * .25 + .4
    a, n, tr, te = BEST_A
    f.show('<circle cx="%.1f" cy="%.1f" r="10" fill="none" stroke="%s" stroke-width="2"/>' % (PX(n), PY(te), GR), t)
    X1 = 580
    f.show(S(X1, 70, 'α = 0', MU, bold=True) + S(X1, 88, '59 leaves · test %.0f%%' % (PATH[0][3] * 100), MU), t - .4)
    f.show(S(X1, 130, 'α = %.4f' % a, GR, bold=True) + S(X1, 148, '%d leaves · test %.1f%%' % (n, te * 100), GR), t)
    f.show(S(X1, 190, 'α = %.3f' % PATH[-1][0], RO, bold=True) + S(X1, 208, '1 leaf · test %.0f%%' % (PATH[-1][3] * 100), RO), t + .5)
    return finish(f, yb + 46)

# ---------- 06 Feature importance ----------
def fig_importance():
    f = Anim('dt13-', 720, 0, 'Each question node in the tree earns its column some importance: the share of rows reaching it '
             'times the gain. Root on age: 6 of 6 times 0.25. Income node: 4 of 6 times 0.125. Age 56 node: 2 of 6 times 0.5. '
             'Summed and normalised: age 83 percent, income 17 percent, bought before 0.',
             'EACH QUESTION NODE PAYS ITS COLUMN · SHARE OF ROWS × GAIN')
    pos = layout(TREE, 0, 300, 50, 66)
    f.static(draw_tree(TREE, pos, ids=False))
    contrib = [('', 'age', 6, .25), ('n', 'income', 4, .125), ('nn', 'age', 2, .5)]
    colc = {'age': FI, 'income': VI, 'bought before': BR}
    for k, (p, col, n, g) in enumerate(contrib):
        x, y = pos[p]; t = .5 + k * 1.0
        f.show(qring(x, y, node_at(TREE, p)['q'], colc[col]), t)
        f.show(M(316, 66 + k * 46, '%d/6 × %g = %.3f' % (n, g, n / 6 * g), colc[col], 'start') +
               S(316, 84 + k * 46, '%s node' % col, MU), t + .3)
    tot = sum(IMP.values())
    X1, yb = 500, 70
    for k, col in enumerate(('age', 'income', 'bought before')):
        y = yb + k * 46; v = IMP[col] / tot; t = 3.6 + k * .4
        f.show(S(X1, y, col, TX, bold=True) + R(X1, y + 8, 160, 14, SUNK, 'none', 3) +
               R(X1, y + 8, max(v * 160, 1.5), 14, tn(colc[col], '.45'), colc[col], 3, 1.2) +
               T(X1 + 166, y + 20, '%.0f%%' % (v * 100), colc[col], 'start', mono=True, bold=True), t)
    f.show(S(316, 210, 'bought before tied at the last node but lost the tie → 0%', RO), 5.2)
    return finish(f, 270)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Tree models</p>
  <h1>Decision <em>tree</em></h1>
  <p class="lede">A decision tree cuts the table in two on one column, then cuts each mixed half again — a chain of <b>yes/no questions</b> that ends in an answer.</p>
</header>

<section id="dtree-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Cut the rows on <em>one column at one threshold</em>; repeat on every half that is still mixed.</p>
{dt1}
  <ul class="why">
    <li>The same six customers as <a href="../../05-classical-ml/knn/index.html">KNN</a>: age, income, bought before, and whether they buy.</li>
    <li>A half where every row has the same label is <b>pure</b>: it stops and becomes a leaf.</li>
  </ul>
</section>

<section id="dtree-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Reading a tree</h2></div>
  <p class="key">Every cut becomes a question node; a prediction <em>walks one path</em> from the root to a leaf.</p>
{dt2}
  <ul class="why">
    <li><b>Root</b> is the first question, <b>internal nodes</b> ask the next ones, <b>leaves</b> give the answer; the longest path is the <b>depth</b>.</li>
    <li>Each path is an if-else rule (<code>export_text</code> prints them), so the model can be read line by line.</li>
  </ul>
</section>

<section id="dtree-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Classification</h2></div>
  <p class="key">The label is a class: score how <em>mixed</em> a node is, pick the cut that unmixes it most, read the leaves.</p>
  <div class="subsec" id="dtree-s3-1">
    <h3 class="ssh"><b>3.1</b>Impurity</h3>
    <p class="skey">One number for how mixed a node is: <em>0 when pure</em>, highest at fifty-fifty.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">Gini</b></span><em>chance two random rows differ</em></span>
      <span class="op">=</span>
      <span class="t"><span>1 − Σ<sub><var>k</var></sub> <var>p</var><sub><var>k</var></sub><sup>2</sup></span><em>p<sub>k</sub> = share of class k</em></span>
    </div>
    <div class="line">
      <span class="t"><span><b class="fn">H</b></span><em>entropy</em></span>
      <span class="op">=</span>
      <span class="t"><span>− Σ<sub><var>k</var></sub> <var>p</var><sub><var>k</var></sub> log<sub>2</sub> <var>p</var><sub><var>k</var></sub></span><em>bits of surprise</em></span>
    </div>
  </div>
{dt3}
    <ul class="why">
      <li>The drop in entropy after a cut is called <b>information gain</b> — section 3.2.</li>
      <li><code>criterion="gini"</code> (default, CART) or <code>"entropy"</code> (ID3, C4.5): they almost always pick the same cut.</li>
    </ul>
  </div>
  <div class="subsec" id="dtree-s3-2">
    <h3 class="ssh"><b>3.2</b>Finding a split</h3>
    <p class="skey">Try <em>every column × every threshold</em>, keep the cut with the largest gain.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">gain</b></span><em>what the cut removes</em></span>
      <span class="op">=</span>
      <span class="t"><span><b class="fn">I</b>(<var>S</var>)</span><em>impurity before</em></span>
      <span class="op">−</span>
      <span class="t b"><span><span class="frac"><i><var>n</var><sub>L</sub></i><i><var>n</var></i></span> <b class="fn">I</b>(<var>S</var><sub>L</sub>)</span><em>left half, by size</em></span>
      <span class="op">−</span>
      <span class="t b"><span><span class="frac"><i><var>n</var><sub>R</sub></i><i><var>n</var></i></span> <b class="fn">I</b>(<var>S</var><sub>R</sub>)</span><em>right half, by size</em></span>
    </div>
  </div>
{dt4}
    <ul class="why">
      <li><b class="fn">I</b> is Gini or entropy; with entropy the gain is the <b>information gain</b>. Thresholds sit halfway between neighbouring values.</li>
      <li><b>Greedy</b>: the best cut now, never a worse cut that would pay off later.</li>
      <li>Only comparisons inside one column, so <b>no scaling</b> is needed; a yes/no column is the threshold 0.5.</li>
    </ul>
  </div>
  <div class="subsec" id="dtree-s3-3">
    <h3 class="ssh"><b>3.3</b>Leaf &amp; boundary</h3>
    <p class="skey">A leaf answers with its <em>majority class</em>; on the plane, every leaf is a rectangle.</p>
{dt5}
    <ul class="why">
      <li><code>predict</code> returns the majority class, <code>predict_proba</code> the class shares inside the leaf.</li>
      <li>Every cut is parallel to an axis, so a diagonal boundary needs a staircase of many small boxes.</li>
    </ul>
  </div>
</section>

<section id="dtree-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Regression</h2></div>
  <p class="key">The label is a number: same algorithm, only <em>the impurity</em> and <em>what a leaf returns</em> change.</p>
  <div class="subsec" id="dtree-s4-1">
    <h3 class="ssh"><b>4.1</b>Impurity</h3>
    <p class="skey">A node is "mixed" when its values are <em>spread out</em>: impurity is their variance.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">Var</b>(<var>S</var>)</span><em>impurity of a node</em></span>
      <span class="op">=</span>
      <span class="t"><span><span class="frac"><i>1</i><i><var>n</var></i></span> Σ<sub><var>i</var></sub> (<var>y</var><sub><var>i</var></sub> − <var>ȳ</var>)<sup>2</sup></span><em>ȳ = mean of the node</em></span>
    </div>
  </div>
{dt6}
    <ul class="why">
      <li>Plug it into the same gain formula as 3.2; a leaf then answers with <span class="mth"><var>ȳ</var></span>.</li>
      <li><code>criterion="squared_error"</code> is the default; <code>"absolute_error"</code> uses distance to the median and is less pulled by outliers.</li>
    </ul>
  </div>
  <div class="subsec" id="dtree-s4-2">
    <h3 class="ssh"><b>4.2</b>Finding a split</h3>
    <p class="skey">The same scan as 3.2: <em>every column × every threshold</em>, keep the biggest drop in variance.</p>
{dt7}
    <ul class="why">
      <li>Same cut as the classification tree here, age 31.5 — but only by coincidence: the label column decides the cuts.</li>
    </ul>
  </div>
  <div class="subsec" id="dtree-s4-3">
    <h3 class="ssh"><b>4.3</b>Leaf &amp; staircase</h3>
    <p class="skey">A leaf answers with the <em>mean</em> of its rows, so the prediction is a staircase.</p>
{dt8}
    <ul class="why">
      <li>Only as many distinct predictions as leaves: the curve is flat between cuts.</li>
      <li><b>No extrapolation</b>: beyond the training range the tree repeats the last step.</li>
    </ul>
  </div>
</section>

<section id="dtree-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Reining it in</h2></div>
  <p class="key">Left alone, a tree splits until every leaf is pure: <em>it memorises the training rows</em>.</p>
  <div class="subsec" id="dtree-s5-1">
    <h3 class="ssh"><b>5.1</b>Overfitting</h3>
    <p class="skey">Every extra level lowers training error; past some depth, <em>test error climbs</em>.</p>
{dt9}
    <ul class="why">
      <li><code>max_depth</code> defaults to unlimited: an unconstrained tree always reaches 0 training error, which proves nothing.</li>
    </ul>
  </div>
  <div class="subsec" id="dtree-s5-2">
    <h3 class="ssh"><b>5.2</b>Instability</h3>
    <p class="skey">A tiny change — a tie, one row — <em>changes a cut, and everything under it</em>.</p>
{dt10}
    <ul class="why">
      <li>Drop row C and the root itself ties between age and income; small data changes, a different tree.</li>
      <li>This high variance is what <a href="../random-forest/index.html">Random forest</a> averages away by growing many trees.</li>
    </ul>
  </div>
  <div class="subsec" id="dtree-s5-3">
    <h3 class="ssh"><b>5.3</b>Pre-pruning</h3>
    <p class="skey">Stop growing early: <em>forbid a split</em> that is too deep or leaves too few rows.</p>
{dt11}
    <ul class="why">
      <li><code>max_depth</code>, <code>min_samples_leaf</code>, <code>min_impurity_decrease</code> — cheap, but a stopped branch is never looked at again.</li>
    </ul>
  </div>
  <div class="subsec" id="dtree-s5-4">
    <h3 class="ssh"><b>5.4</b>Post-pruning</h3>
    <p class="skey">Grow fully, then cut back the branches that <em>cost more leaves than they earn</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">R</b><sub>α</sub>(<var>T</var>)</span><em>cost of tree T</em></span>
      <span class="op">=</span>
      <span class="t b"><span><b class="fn">R</b>(<var>T</var>)</span><em>impurity of the leaves on train</em></span>
      <span class="op">+</span>
      <span class="t p"><span><var>α</var> · |<var>T</var>|</span><em>price per leaf</em></span>
    </div>
  </div>
{dt12}
    <ul class="why">
      <li>Set with <code>ccp_alpha</code>; <code>cost_complexity_pruning_path</code> lists every useful α. Choose it by cross-validation.</li>
    </ul>
  </div>
</section>

<section id="dtree-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Feature importance</h2></div>
  <p class="key">A column is important when its cuts <em>removed a lot of impurity</em> for many rows.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">imp</b>(<var>j</var>)</span><em>importance of column j</em></span>
      <span class="op">∝</span>
      <span class="t"><span>Σ<sub><var>t</var> ∈ <var>j</var></sub></span><em>nodes that split on j</em></span>
      <span class="t b"><span><span class="frac"><i><var>n</var><sub><var>t</var></sub></i><i><var>n</var></i></span></span><em>share of rows reaching it</em></span>
      <span class="op">·</span>
      <span class="t g"><span><b class="fn">gain</b><sub><var>t</var></sub></span><em>impurity it removed</em></span>
    </div>
  </div>
{dt13}
  <ul class="why">
    <li>Normalised to sum to 1; read it from <code>feature_importances_</code>.</li>
    <li>It describes this tree, not the world: a column that loses a tie, or is correlated with a winner, scores low.</li>
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

<footer>Machine learning · Tree models · next lesson in the branch: <a href="../random-forest/index.html">Random forest</a>.</footer>
'''

def build():
    figs = dict(dt1=fig_mental(), dt2=fig_read(), dt3=fig_gini(), dt4=fig_scan('cls'), dt5=fig_boundary(),
                dt6=fig_var(), dt7=fig_scan('reg'), dt8=fig_stairs(), dt9=fig_overfit(), dt10=fig_unstable(),
                dt11=fig_prepruning(), dt12=fig_postpruning(), dt13=fig_importance())
    return re.sub(r'\{(dt\d+)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">'); b = s.index('</article>')
    s = s[:a] + body + '      ' + s[b:]
    s = re.sub(r'data-blurb="[^"]*"( data-reviewed="\d")?', 'data-blurb="%s" data-reviewed="2"' % blurb, s, count=1)
    open(page, 'w').write(s)

if __name__ == '__main__':
    splice(PAGE, build(), 'Cut the table on one column at a time: Gini or variance picks the cut, leaves vote or average, '
           'and depth limits or pruning stop the tree memorising.')
