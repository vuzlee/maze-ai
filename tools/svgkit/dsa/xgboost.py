# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/06-tree-models/xgboost.
Same six customers as decision_tree.py. Regression learns spend from a start of 25 (the mean);
classification learns buy from p = 0.5. lambda = 1, eta = 0.3 (the XGBoost defaults) unless a figure
says otherwise. Every number is computed and asserted here. Run: python3 xgboost.py"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from decision_tree import (DATA, COLS, LAB, CL, HL, layout, node_at, qbox, qring, pick, splice, BODY as DT_BODY)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, finish)
from tablefig import GR, tint, pill

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/06-tree-models/xgboost/index.html')
LAM, ETA, BASE, P0 = 1, .3, 25, .5
POS, NEG = FI, VI          # sign of a residual: positive blue, negative violet
import linear_algebra as _la
_la.RGBA.setdefault(GR, '--green-a')   # chip()/tn() in green, the kept / result colour

def fmt(x, nd=2, plus=False):
    s = ('%.' + str(nd) + 'f') % x
    if s.startswith('-'): s = '−' + s[1:]
    if re.fullmatch(r'−?0\.0*', s): s = '0'
    return ('+' + s) if plus and x > 0 else s
def g(x): return fmt(x, 0) if abs(x - round(x)) < 1e-9 else fmt(x, 2)

# ---------- the arithmetic: residual r = -g, Cover = sum of h ----------
def res(r, kind): return (r[5] - BASE) if kind == 'reg' else (r[4] - P0)
def hess(r, kind): return 1 if kind == 'reg' else P0 * (1 - P0)
def SR(rs, kind): return sum(res(r, kind) for r in rs)
def COV(rs, kind): return sum(hess(r, kind) for r in rs)
def sim(rs, kind, lam=LAM): return SR(rs, kind) ** 2 / (COV(rs, kind) + lam)
def out(rs, kind, lam=LAM): return SR(rs, kind) / (COV(rs, kind) + lam)
def scan(rs, kind, lam=LAM):
    o = []
    for c in range(3):
        vs = sorted(set(r[c + 1] for r in rs))
        for a, b in zip(vs, vs[1:]):
            t = (a + b) / 2; Lr = [r for r in rs if r[c + 1] < t]; Rr = [r for r in rs if r[c + 1] >= t]
            o.append((COLS[c], t, sim(Lr, kind, lam) + sim(Rr, kind, lam) - sim(rs, kind, lam),
                      ''.join(r[0] for r in Lr), ''.join(r[0] for r in Rr)))
    return o
def best(sc): return max(sc, key=lambda s: s[2])

AB, CDEF = pick(DATA, 'AB'), pick(DATA, 'CDEF')
RES = {k: [res(r, k) for r in DATA] for k in ('reg', 'cls')}
assert BASE == sum(r[5] for r in DATA) / 6 and RES['reg'] == [-15, -13, 5, 9, 3, 11]
assert RES['cls'] == [-.5, -.5, .5, .5, -.5, .5]
# regression, lambda = 1
assert SR(DATA, 'reg') == 0 and sim(DATA, 'reg') == 0
assert round(sim(AB, 'reg'), 2) == 261.33 and round(sim(CDEF, 'reg'), 2) == 156.8
SC = {k: scan(DATA, k) for k in ('reg', 'cls')}
assert best(SC['reg'])[:2] == ('age', 31.5) and round(best(SC['reg'])[2], 2) == 418.13
assert round(out(AB, 'reg'), 2) == -9.33 and out(CDEF, 'reg') == 5.6
assert SR(AB, 'reg') / 2 == -14 and SR(CDEF, 'reg') / 4 == 7        # lambda = 0: the plain mean
# classification, lambda = 1
assert sim(DATA, 'cls') == 0 and round(sim(AB, 'cls'), 3) == .667 and sim(CDEF, 'cls') == .5
assert best(SC['cls'])[:2] == ('age', 31.5) and round(best(SC['cls'])[2], 3) == 1.167
assert round(out(AB, 'cls'), 3) == -.667 and out(CDEF, 'cls') == .5
assert COV(AB, 'cls') == .5 and COV(CDEF, 'cls') == 1
# the objective of leaf C D E F, regression: G = sum g = -28, H = 4
G_CDEF, H_CDEF = -SR(CDEF, 'reg'), COV(CDEF, 'reg'); assert (G_CDEF, H_CDEF) == (-28, 4)
def obj(w, lam): return G_CDEF * w + .5 * (H_CDEF + lam) * w * w
assert obj(7, 0) == -98 and round(obj(5.6, 1), 6) == -78.4 and round(2 * 78.4, 1) == round(sim(CDEF, 'reg'), 1)
# one round: new prediction = start + eta * w
NEWP = [BASE + ETA * (out(AB, 'reg') if r[0] in 'AB' else out(CDEF, 'reg')) for r in DATA]
NEWR = [r[5] - p for r, p in zip(DATA, NEWP)]
SSE0, SSE1 = sum(x * x for x in RES['reg']), sum(x * x for x in NEWR)
assert SSE0 == 630 and round(SSE1, 1) == 406.1 and round(NEWP[0], 1) == 22.2 and round(NEWP[2], 2) == 26.68
assert round(BASE + ETA * out(CDEF, 'reg'), 2) == 26.68
import math
P_NEW = 1 / (1 + math.exp(-(0 + ETA * out(CDEF, 'cls')))); assert round(P_NEW, 3) == .537
# gamma: classification tree, lambda = 1. Under C D E F the best split ties (age 46.5 / income 28), gain 1/6
L2C = best(scan(CDEF, 'cls')); assert round(L2C[2], 3) == .167 and L2C[3] == 'CD'
assert max(s[2] for s in scan(AB, 'cls')) < 0
CD, EF = pick(DATA, 'CD'), pick(DATA, 'EF')
assert round(out(CD, 'cls'), 2) == .67 and out(EF, 'cls') == 0 and out(DATA, 'cls') == 0
assert round(scan(EF, 'cls')[0][2], 2) == .4   # E F would split again at max_depth 6: the gamma figure uses max_depth 2
GAMMAS = [0, .5, 1.5]
# lambda: three candidate splits of the regression tree, gain at lambda 0 and 1
LCAND = [('age < 31.5', 'root', DATA, 31.5), ('age < 26', 'node A B', AB, 26), ('age < 56', 'node C D E F', CDEF, 56)]
def gain_at(rs, thr, lam):
    return [s for s in scan(rs, 'reg', lam) if s[0] == 'age' and s[1] == thr][0][2]
LG = [(a, b, gain_at(rs, t, 0), gain_at(rs, t, 1)) for a, b, rs, t in LCAND]
assert [round(x[2], 2) for x in LG] == [588, 2, 21.33] and [round(x[3], 2) for x in LG] == [418.13, -64.33, -24.05]
assert max(s[2] for s in scan(AB, 'reg')) < 0 and max(s[2] for s in scan(CDEF, 'reg')) < 0   # lambda 1: depth 1
assert max(s[2] for s in scan(AB, 'reg', 0)) == 2 and round(best(scan(CDEF, 'reg', 0))[2], 2) == 21.33

# ---------- drawing helpers ----------
def vpill(cx, cy, s, c, ids=None, w=None):
    w = w or len(s) * 6.2 + 16
    fill = SUNK if c == MU else tn(c, '.14')
    o = R(cx - w / 2, cy - 11, w, 22, BG, 'none', 11) + R(cx - w / 2, cy - 11, w, 22, fill, RULE_HI if c == MU else c, 11, 1.3)
    o += T(cx, cy + 4, s, c, bold=True, mono=True)
    if ids: o += T(cx, cy + 26, ids, FA, mono=True)
    return o

def vtree(tree, pos):
    s = ''
    for p, (x, y) in pos.items():
        n = node_at(tree, p)
        if 'leaf' in n: continue
        for ch, word in (('y', 'yes'), ('n', 'no')):
            cx, cy = pos[p + ch]
            s += L(x, y + 13, cx, cy - 11, RULE_HI, 1.2)
            mx, my = (x + cx) / 2, (y + 13 + cy - 11) / 2
            s += T(mx + (-12 if ch == 'y' else 12), my - 4, word, FA, 'end' if ch == 'y' else 'start')
    for p, (x, y) in pos.items():
        n = node_at(tree, p)
        s += vpill(x, y, n['leaf'], n['c'], n.get('ids')) if 'leaf' in n else qbox(x, y, n['q'])
    return s

def rc(v): return POS if v > 0 else NEG if v < 0 else MU

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('xgb1-', 720, 0, 'One boosting round on the six customers. Every prediction starts at 25, the mean spend, so the '
             'residuals are minus 15, minus 13, 5, 9, 3, 11. A tree asks age under 31.5: A and B share a leaf whose value is '
             'minus 9.33, C to F a leaf of plus 5.6, and the split is kept because its Gain of 418 beats gamma. Each prediction '
             'moves by 0.3 times its leaf value, to 22.2 or 26.68, and the squared residuals fall from 630 to 406.',
             'ONE ROUND · RESIDUALS → ONE SCORED TREE → SMALL STEP')
    t = Table(0, 30, [('id', 28), ('age', 38), ('spend', 48, ''), ('ŷ', 48, 'start'), ('r', 48, 'spend − ŷ'),
                      ('ŷ new', 60, 'ŷ + 0.3 w'), ('r new', 60, 'spend − ŷ')])
    def head(j): return T(t.cx(j), t.hb, t.cols[j][0], MU) + (T(t.cx(j), t.hb + 13, t.cols[j][2], FA) if len(t.cols[j]) > 2 else '')
    f.static(head(0) + head(1) + head(2) + L(t.x, t.line, t.x + t.w, t.line))
    for i, r in enumerate(DATA):
        f.show(t.row(i, [r[0], str(r[1]), str(r[5])]), .2 + i * .08)
    f.show(head(3), 1.0)
    for i in range(6): f.show(t.cell(i, 3, str(BASE)), 1.1 + i * .05)
    f.show(head(4), 1.8)
    for i, v in enumerate(RES['reg']): f.show(t.cell(i, 4, fmt(v, 0, True), c=rc(v)), 1.9 + i * .06)
    # the tree
    tree = {'q': 'age < 31.5 ?', 'yes': {'leaf': 'w = ' + fmt(out(AB, 'reg')), 'ids': 'A B', 'c': NEG},
            'no': {'leaf': 'w = +' + fmt(out(CDEF, 'reg')), 'ids': 'C D E F', 'c': POS}}
    pos = layout(tree, 440, 700, 70, 92)
    (rx, ry), (ax, ay), (cx, cy) = pos[''], pos['y'], pos['n']
    f.show(qbox(rx, ry, tree['q']), 2.8)
    f.show(L(rx, ry + 13, ax, ay - 11, RULE_HI, 1.2) + T((rx + ax) / 2 - 12, (ry + ay) / 2 - 2, 'yes', FA, 'end'), 3.3)
    f.show(t.outline(0, 1, 4, 4, NEG, 1.8), 3.3)
    f.show(vpill(ax, ay, tree['yes']['leaf'], NEG, 'A B'), 3.6)
    f.show(L(rx, ry + 13, cx, cy - 11, RULE_HI, 1.2) + T((rx + cx) / 2 + 12, (ry + cy) / 2 - 2, 'no', FA, 'start'), 4.1)
    f.show(t.outline(2, 5, 4, 4, POS, 1.8), 4.1)
    f.show(vpill(cx, cy, tree['no']['leaf'], POS, 'C D E F'), 4.4)
    f.show(S(rx, ry - 26, 'Gain %.0f > γ · keep the split' % best(SC['reg'])[2], GR, 'middle', bold=True), 5.0)
    f.show(head(5), 5.8)
    for i, p in enumerate(NEWP): f.show(t.cell(i, 5, fmt(p, 2 if i > 1 else 1)), 5.9 + i * .06)
    f.show(head(6), 6.8)
    for i, v in enumerate(NEWR): f.show(t.cell(i, 6, fmt(v, 2 if i > 1 else 1, True), c=rc(v)), 6.9 + i * .06)
    yb = t.bottom(6) + 30
    f.show(M(0, yb, 'Σ {r}² : %d → %.1f' % (SSE0, SSE1), TX, 'start') +
           S(150, yb, 'the next tree starts from  r new', MU), 7.8)
    f.show(S(440, 236, 'λ = 1 shrinks w · η = 0.3 scales the step', MU), 5.4)
    return finish(f, yb + 14)

# ---------- 02 Objective ----------
def fig_objective():
    f = Anim('xgb2-', 720, 0, 'The objective of leaf C D E F as a function of its value w: a parabola, minus 28 w plus a half '
             'of H plus lambda times w squared. With lambda 0 the bottom sits at w 7, depth minus 98. With lambda 1 the '
             'parabola is steeper, the bottom moves to 5.6 and rises to minus 78.4. Twice that depth, 156.8, is the '
             'Similarity of the leaf.', 'ONE LEAF · ITS OBJECTIVE IS A PARABOLA IN w')
    w0, w1, v0, v1 = -.5, 9.5, -110, 20
    x0, x1, yt, yb = 50, 420, 40, 270
    PX = lambda w: x0 + (w - w0) / (w1 - w0) * (x1 - x0)
    PY = lambda v: yt + (v1 - v) / (v1 - v0) * (yb - yt)
    f.static(L(x0, PY(0), x1, PY(0), RULE_HI, 1.3) + L(PX(0), yt, PX(0), yb, RULE_HI, 1.3))
    for w in (2, 4, 6, 8): f.static(T(PX(w), PY(0) - 6, str(w), FA, mono=True))
    for v in (-100, -50): f.static(L(x0, PY(v), x1, PY(v), RULE, .8) + T(PX(0) - 6, PY(v) + 4, fmt(v, 0), FA, 'end', mono=True))
    f.static(M(x1, PY(0) + 18, 'leaf value {w}', MU, 'end') + M(PX(0) + 6, yt - 8, 'Obj', MU, 'start'))
    ws = [w0 + i * (w1 - w0) / 80 for i in range(81)]
    f.show(poly([(PX(w), PY(obj(w, 0))) for w in ws], MU, 1.8, '5 4'), .4)
    f.show(L(PX(7), PY(0), PX(7), PY(-98), MU, 1, '2 3') + dot(PX(7), PY(-98), MU, 5, BG) +
           T(PX(7) + 4, PY(0) + 16, '7', MU, 'start', mono=True, bold=True), 1.2)
    f.show(S(460, 270, 'dashed · λ = 0 · bottom at 7, Obj −98', MU), 1.2)
    f.show(poly([(PX(w), PY(obj(w, 1))) for w in ws], FI, 2.4), 2.4)
    f.show(L(PX(5.6), PY(0), PX(5.6), PY(-78.4), GR, 1.2, '4 3') + dot(PX(5.6), PY(-78.4), GR, 5.5, BG) +
           T(PX(5.6) - 4, PY(0) + 16, '5.6', GR, 'end', mono=True, bold=True), 3.2)
    X1 = 460
    f.show(S(X1, 56, 'leaf C D E F', MU, bold=True) + M(X1, 80, '{G} = Σ {g} = −28', TX, 'start') +
           M(X1 + 140, 80, '{H} = 4', TX, 'start'), .2)
    f.show(M(X1, 116, 'Obj({w}) = {G}{w} + ½({H} + {λ}){w}²', TX, 'start'), .6)
    f.show(M(X1, 156, '{w}* = −{G} / ({H} + {λ}) = 28 / 5 = 5.6', GR, 'start'), 3.6)
    f.show(M(X1, 192, 'Obj* = −½ · 28² / 5 = −78.4', GR, 'start'), 4.2)
    f.show(L(X1, 214, 712, 214, RULE, 1), 4.8)
    f.show(S(X1, 236, 'depth × 2 = 28² / 5 = 156.8', FI, bold=True) + S(X1, 254, '= the Similarity of the leaf', MU), 4.8)
    f.show(S(460, 288, 'solid · λ = 1 · bottom at 5.6, Obj −78.4', GR, bold=True), 3.2)
    return finish(f, 298)

# ---------- shared tree pieces: residual chips that travel from the table into node boxes ----------
from tablefig import AM
from decision_tree import edge_hl
CW = 42                                   # chip pitch inside a node box
def rlab(v, kind): return (fmt(v, 0, True) if kind == 'reg' else fmt(v, 1, True)) if v else '0'
def rchip(cx, cy, v, kind, w=38):
    c = rc(v)
    return (R(cx - w / 2, cy - 10, w, 20, BG, 'none', 10) + R(cx - w / 2, cy - 10, w, 20, tn(c, '.16'), c, 10, 1.2) +
            T(cx, cy + 4, rlab(v, kind), c, mono=True, bold=True))
def nbox(cx, cy, n, c=RULE_HI):
    w = n * CW + 12
    return R(cx - w / 2, cy - 20, w, 40, BG, c, 8, 1.3)
def slot(cx, n, k): return cx - (n - 1) * CW / 2 + k * CW
def sbox(cx, cy, l1, l2, c=RULE_HI, c2=TX):
    w = max(len(l1), len(l2)) * 6.6 + 24
    return (R(cx - w / 2, cy - 20, w, 40, BG, c, 8, 1.3) + T(cx, cy - 4, l1, MU, mono=True, bold=True) +
            T(cx, cy + 13, l2, c2, mono=True, bold=True))
def yesno(x0, y0, x1, y1, ch):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    return T(mx + (-10 if ch == 'y' else 10), my, 'yes' if ch == 'y' else 'no', FA, 'end' if ch == 'y' else 'start')
def glide(f, svg, pts, t0, d=.6):
    """svg is drawn at its final spot; pts = [(t, x, y)] absolute centres, the last one = the final spot"""
    fx, fy = pts[-1][1], pts[-1][2]
    f.path(svg, [(0, pts[0][1] - fx, pts[0][2] - fy)] + [(t, x - fx, y - fy) for t, x, y in pts[1:]], t0, d=d)

ROOT, QY, CHY = (500, 74), 138, 214
KIDS = (('AB', AB, 372), ('CDEF', CDEF, 612))
def covs(rs, kind): return ('%d' % len(rs)) if kind == 'reg' else g(COV(rs, kind))
def simtxt(rs, kind): return '(%s)² / (%s + 1) = %s' % (g(SR(rs, kind)), covs(rs, kind), fmt(sim(rs, kind)) if SR(rs, kind) else '0')
def xtree(f, kind, t_root, t_cut, t_kids, chips_from=None, rtab=None):
    """root box with every residual, the question, two children; chips glide in from table column r (rtab)"""
    rx, ry = ROOT
    f.show(nbox(rx, ry, 6), t_root)
    for i, r in enumerate(DATA):
        v = res(r, kind); src = (rtab.cx(2), rtab.ry(i) + 13)
        glide(f, rchip(slot(rx, 6, i), ry, v, kind), [(0,) + src, (t_root + .4 + i * .15, slot(rx, 6, i), ry)], t_root + .2)
    f.show(L(rx, ry + 20, rx, QY - 13, RULE_HI, 1.2) + qbox(rx, QY, 'age < 31.5 ?'), t_cut)
    for k, (ids, rs, cx) in enumerate(KIDS):
        f.show(L(rx, QY + 13, cx, CHY - 20, RULE_HI, 1.2) + yesno(rx, QY + 13, cx, CHY - 20, 'yn'[k]) + nbox(cx, CHY, len(rs)),
               t_kids + k * .3)
        for j, r in enumerate(rs):
            i = DATA.index(r); v = res(r, kind); src = (rtab.cx(2), rtab.ry(i) + 13); dst = (slot(cx, len(rs), j), CHY)
            way = [] if k == 0 else [(t_kids + .6 + j * .15, dst[0], 168)]
            tt = t_kids + .6 + j * .15 + (.6 if k else 0) + k * .3
            glide(f, rchip(*dst, v, kind), [(0,) + src] + way + [(tt,) + dst], t_kids + .4 + k * .3)
    return t_kids + 2.4

def rtable(kind, extra=()):
    t = Table(0, 30, [('id', 28), ('age', 38), ('r', 50, 'spend − ŷ' if kind == 'reg' else 'y − p')] + list(extra))
    return t

# ---------- 3.1 / 4.1 Similarity ----------
def fig_sim(kind):
    reg = kind == 'reg'
    f = Anim('xgb3-' if reg else 'xgb6-', 720, 0,
             ('The residual column of the table: %s. Every residual slides into the root node, where they sum to 0, '
              'so its Similarity is 0. The table is cut at age 31.5 and the residuals slide again into two child nodes. '
              'A B: %s, sum %s, Similarity %s. C D E F: %s, sum %s, Similarity %s.') %
             ((', '.join(g(v) for v in RES[kind]), ', '.join(g(res(r, kind)) for r in AB), g(SR(AB, kind)), fmt(sim(AB, kind)),
               ', '.join(g(res(r, kind)) for r in CDEF), g(SR(CDEF, kind)), fmt(sim(CDEF, kind)))),
             'RESIDUALS INTO A NODE · SAME SIGN ADDS UP · OPPOSITE SIGNS CANCEL')
    t = rtable(kind)
    f.static(T(t.cx(0), t.hb, 'id', MU) + T(t.cx(1), t.hb, 'age', MU) + T(t.cx(2), t.hb, 'r', MU) +
             T(t.cx(2), t.hb + 13, t.cols[2][2], FA) + L(t.x, t.line, t.x + t.w, t.line))
    for i, r in enumerate(DATA):
        v = res(r, kind)
        f.show(t.row(i, [r[0], str(r[1]), rlab(v, kind)], colors={2: rc(v)}), .2 + i * .08)
    rx, ry = ROOT
    end = xtree(f, kind, 1.0, 3.6, 4.2, rtab=t)
    f.show(M(rx, ry - 30, 'Sim = ' + simtxt(DATA, kind), MU), 2.6)
    yc = t.ry(2) - 2
    f.show(L(-4, yc, t.w + 4, yc, HL, 1.8, '5 4') + R(t.w + 8, yc - 9, 74, 18, BG, 'none', 4) +
           T(t.w + 12, yc + 4, 'age 31.5', HL, 'start', bold=True), 3.4)
    for k, (ids, rs, cx) in enumerate(KIDS):
        f.show(M(cx, CHY + 40, 'Sim = ' + simtxt(rs, kind), FI), end + k * .5)
    yb = CHY + 74
    f.show(S(0, yb, ('Cover = number of rows' if reg else 'Cover = Σ p(1 − p) = 0.25 per row at p = 0.5') +
             ' · λ = 1 in the denominator', MU), end + 1.0)
    return finish(f, yb + 12)

# ---------- 3.2 / 4.2 Gain & split ----------
def fig_scan(kind):
    reg = kind == 'reg'
    sc = SC[kind]; win = best(sc)
    a, b = sim(AB, kind), sim(CDEF, kind)
    f = Anim('xgb4-' if reg else 'xgb7-', 720, 0,
             ('Rows sorted by age with their residuals; a dashed line steps down between rows and each position gets a bar for '
              'its Gain. Income and bought before are scanned the same way. The tallest bar is age under 31.5, Gain %s. '
              'The winner is drawn as a tree: root Similarity 0, children %s and %s, Gain on the question.')
             % (fmt(win[2]), fmt(a, 1), fmt(b, 1)), 'EVERY COLUMN × EVERY THRESHOLD · KEEP THE LARGEST GAIN')
    t = Table(0, 30, [('id', 30), ('age', 44), ('r', 52)])
    f.static(t.head())
    for i, r in enumerate(DATA):
        v = res(r, kind)
        f.show(t.row(i, [r[0], str(r[1]), rlab(v, kind)], colors={2: rc(v)}), .2 + i * .08)
    yl = lambda i: t.ry(i + 1) - 2
    f.path(L(-4, yl(0), t.w + 4, yl(0), HL, 1.8, '5 4'), [(0, 0, 0)] + [(1.0 + i * .6, 0, i * 30) for i in range(1, 5)],
           1.0, d=.3, hide=4.0)
    BX, LX, top, step = 300, 196, 44, 22
    scale = 250 / win[2]
    for k, (col, thr, gn, _, _) in enumerate(sc):
        y = top + k * step
        name = 'bought before ?' if col == 'bought before' else '%s < %g' % (col, thr)
        t0 = 1.2 + k * .6 if k < 5 else 4.4 + (k - 5) * .15
        w = max(gn * scale, 1.5)
        f.show(T(LX, y + 13, name, TX if col == 'age' else MU, 'start', 'sv-s') +
               R(BX, y + 3, w, 14, tn(FI, '.30'), FI, 2, 1) +
               T(BX + w + 8, y + 14, fmt(gn, 1 if reg else 2), MU, 'start', mono=True), t0)
    kw = sc.index(win); y = top + kw * step
    f.show(R(BX, y + 3, win[2] * scale, 14, tint('gr', '.35'), GR, 2, 1.6), 5.6)
    f.show(L(-4, yl(1), t.w + 4, yl(1), GR, 2), 5.6)
    f.show(pill(BX + win[2] * scale + 92, y + 1, 'best split', 'gr'), 5.9)
    # the winner as a tree
    y0 = top + len(sc) * step + 30
    nd = 1 if reg else 2
    rx, qy, ky = 230, y0 + 70, y0 + 140
    f.show(L(LX - 10, y0 - 12, 712, y0 - 12, RULE, 1), 6.3)
    f.show(sbox(rx, y0 + 20, 'A B C D E F', 'Sim 0', c2=MU), 6.5)
    f.show(L(rx, y0 + 40, rx, qy - 13, RULE_HI, 1.2) + qbox(rx, qy, 'age < 31.5 ?', GR, 1.8), 6.9)
    for k, (ids, rs, cx) in enumerate((('A B', AB, rx - 130), ('C D E F', CDEF, rx + 130))):
        f.show(L(rx, qy + 13, cx, ky - 20, RULE_HI, 1.2) + yesno(rx, qy + 13, cx, ky - 20, 'yn'[k]) +
               sbox(cx, ky, ids, 'Sim ' + fmt(sim(rs, kind), nd), c2=FI), 7.3 + k * .3)
    f.show(M(rx + 70, qy - 12, 'Gain = %s + %s − 0 = %s' % (fmt(a, nd), fmt(b, nd), fmt(win[2], nd)), GR, 'start'), 8.2)
    f.show(S(rx + 70, qy + 6, 'Sim(A B) + Sim(C D E F) − Sim(all six)', MU), 8.2)
    assert round(a + b - sim(DATA, kind), 6) == round(win[2], 6)
    return finish(f, ky + 30)

# ---------- 3.3 / 4.3 Output value ----------
def fig_output(kind):
    reg = kind == 'reg'
    newv = (lambda w: BASE + ETA * w) if reg else (lambda w: 1 / (1 + math.exp(-(ETA * w))))
    nf = (lambda v: fmt(v, 2)) if reg else (lambda v: fmt(v, 3))
    f = Anim('xgb5-' if reg else 'xgb8-', 720, 0,
             ('The tree from 3.2 with its residuals in each leaf. Each leaf value is the residual sum over Cover plus lambda: '
              '%s for A B, %s for C D E F. The value travels from the leaf into column w of every row of that leaf, and the '
              'new %s is computed from it: %s for A and B, %s for C to F.')
             % (fmt(out(AB, kind)), fmt(out(CDEF, kind)), 'prediction 25 + 0.3 w' if reg else 'probability σ(0.3 w)',
                nf(newv(out(AB, kind))), nf(newv(out(CDEF, kind)))),
             'LEAF VALUE = Σ r / (COVER + λ) · IT FLOWS BACK INTO THE TABLE')
    t = rtable(kind, [('w', 58, 'leaf value'), ('ŷ new' if reg else 'p new', 66, 'ŷ + 0.3 w' if reg else 'σ(0.3 w)')])
    def head(j): return T(t.cx(j), t.hb, t.cols[j][0], MU) + (T(t.cx(j), t.hb + 13, t.cols[j][2], FA) if len(t.cols[j]) > 2 else '')
    f.static(head(0) + head(1) + head(2) + head(3) + head(4) + L(t.x, t.line, t.x + t.w, t.line))
    for i, r in enumerate(DATA):
        v = res(r, kind)
        f.static(t.row(i, [r[0], str(r[1]), rlab(v, kind)], colors={2: rc(v)}))
    rx, ry = ROOT
    f.static(L(rx, QY - 40, rx, QY - 13, RULE_HI, 1.2) + qbox(rx, QY - 40, 'age < 31.5 ?'))
    QQ = QY - 40; KY = CHY - 60
    t1 = .3
    for k, (ids, rs, cx) in enumerate(KIDS):
        f.static(L(rx, QQ + 13, cx, KY - 20, RULE_HI, 1.2) + yesno(rx, QQ + 13, cx, KY - 20, 'yn'[k]) + nbox(cx, KY, len(rs)))
        for j, r in enumerate(rs):
            f.static(rchip(slot(cx, len(rs), j), KY, res(r, kind), kind))
        w = out(rs, kind); c = rc(w)
        f.show(M(cx, KY + 40, 'w = %s / (%s + 1) = %s' % (g(SR(rs, kind)), covs(rs, kind), fmt(w, 2, True)), c), t1)
        f.show(chip(cx, KY + 66, fmt(w, 2, True), c, 64), t1 + .5)
        for j, r in enumerate(rs):
            # one chip in flight at a time: the next leaves only after this one has landed
            i = DATA.index(r); dst = (t.cx(3), t.ry(i) + 13); tt = t1 + 1.2 + j * 1.4
            glide(f, chip(*dst, fmt(w, 2, True), c, 52),
                  [(0, cx, KY + 66), (tt, cx, KY + 94), (tt + .4, 286, KY + 94), (tt + .8, 286, dst[1]), (tt + 1.2, ) + dst],
                  tt - .25, d=.4)
            f.show(t.cell(i, 4, nf(newv(w))), tt + 1.25)
        t1 += 1.2 + len(rs) * 1.4 + .4
    yb = KY + 124
    lam0 = (SR(AB, kind) / COV(AB, kind), SR(CDEF, kind) / COV(CDEF, kind))
    f.show(S(0, yb, 'λ = 0 would give %s and %s%s · λ = 1 pulls both toward 0' %
             (g(lam0[0]), fmt(lam0[1], 0, True), ', the plain means' if reg else ', outside the residuals'), MU), t1)
    if reg: assert round(newv(out(CDEF, kind)), 2) == 26.68 and round(newv(out(AB, kind)), 2) == 22.2
    else: assert round(newv(out(CDEF, kind)), 3) == .537 and round(newv(out(AB, kind)), 3) == .45
    return finish(f, yb + 12)

# ---------- 3.4 Prediction: a new customer walks every tree ----------
D2 = [r[:5] + (nr + BASE,) for r, nr in zip(DATA, NEWR)]      # spend shifted so that res() = r new
W2 = best(scan(D2, 'reg'))
AB2, CDEF2 = [r for r in D2 if r[0] in 'AB'], [r for r in D2 if r[0] in 'CDEF']
assert W2[:2] == ('age', 31.5) and round(W2[2], 2) == 257.64
assert max(s[2] for s in scan(AB2, 'reg')) < 0 and max(s[2] for s in scan(CDEF2, 'reg')) < 0
TW = [(out(AB, 'reg'), out(CDEF, 'reg')), (out(AB2, 'reg'), out(CDEF2, 'reg'))]
assert round(TW[1][0], 2) == -7.47 and round(TW[1][1], 2) == 4.26
YX = BASE + ETA * TW[0][1] + ETA * TW[1][1]; assert round(YX, 2) == 27.96
def fig_predict():
    f = Anim('xgb12-', 720, 0, 'Two trees after two rounds. Tree 1 was fit to the first residuals, tree 2 to what was left. Both '
             'ask age under 31.5. A new customer X aged 45 walks each tree: not under 31.5, go no, to the leaf C D E F: plus 5.6 '
             'in tree 1 and plus 4.26 in tree 2. The two leaf values drop into the sum: 25 plus 0.3 times 5.6 plus 0.3 times '
             '4.26 is 27.96.', 'PREDICTION = START + η × (SUM OF ONE LEAF PER TREE)')
    f.static(chip(84, 46, 'new X · age 45', VI, 130))
    slots = (196, 352); yq = 278
    for k, (wl, wr) in enumerate(TW):
        x0 = 190 + k * 270 if False else 10 + k * 360
        tree = {'q': 'age < 31.5 ?', 'yes': {'leaf': 'w = ' + fmt(wl), 'c': rc(wl)}, 'no': {'leaf': 'w = ' + fmt(wr, 2, True), 'c': rc(wr)}}
        pos = layout(tree, x0, x0 + 340, 100, 90)
        f.static(S(x0 + 170, 72, 'tree %d · fit to %s' % (k + 1, 'r' if k == 0 else 'r new'), MU, 'middle', bold=True))
        f.static(vtree(tree, pos))
        t0 = .6 + k * 2.6
        f.show(edge_hl(pos, '', 'n'), t0 + .6)
        f.show(qring(*pos[''], tree['q']), t0)
        f.show(T(pos[''][0] + 60, pos[''][1] + 4, '45 ≥ 31.5', HL, 'start', mono=True, bold=True), t0 + .2)
        x, y = pos['n']
        f.show(vpill(x, y, tree['no']['leaf'], rc(wr)) + R(x - 44, y - 14, 88, 28, 'none', HL, 14, 1.8), t0 + 1.2)
        glide(f, chip(slots[k], yq, fmt(wr, 2, True), rc(wr), 64), [(0, x, y + 30), (t0 + 1.8, slots[k], yq)], t0 + 1.5)
    f.static(M(150, yq + 5, '{ŷ}(X) = 25 + 0.3 ×', TX, 'end') + M(274, yq + 5, '+ 0.3 ×', TX) +
             M(392, yq + 5, '= 25 + %s + %s = %s' % (fmt(ETA * TW[0][1]), fmt(ETA * TW[1][1]), fmt(YX)), GR, 'start'))
    f.static(S(0, yq + 34, 'every tree adds one leaf value, scaled by η = 0.3; 100 trees means 100 walks', MU))
    return finish(f, yq + 46)

# ---------- 3.5 Missing values: a learned default direction ----------
MISS = {'B', 'E'}
def miss_gain(t, left):
    Lr = [r for r in DATA if (r[0] in MISS and left) or (r[0] not in MISS and r[2] < t)]
    Rr = [r for r in DATA if r not in Lr]
    return sim(Lr, 'reg') + sim(Rr, 'reg') - sim(DATA, 'reg'), Lr, Rr
KN = sorted(set(r[2] for r in DATA if r[0] not in MISS))
MG = [((a + b) / 2, side, miss_gain((a + b) / 2, side == 'yes')) for a, b in zip(KN, KN[1:]) for side in ('yes', 'no')]
MW = max(MG, key=lambda m: m[2][0])
assert MW[0] == 15 and MW[1] == 'yes' and MW[2][0] == 312.5
assert [m[2][0] for m in MG if m[0] == 15 and m[1] == 'no'] == [150]
def fig_missing():
    f = Anim('xgb13-', 720, 0, 'The income of B and E is missing. The split income under 15 is scored with the known rows only, '
             'then twice more: missing rows sent to yes gives Gain 312.5, sent to no gives 150. Yes wins, so the node stores '
             'yes as its default direction and B and E slide into the yes child with A.',
             'MISSING VALUES · TRY BOTH SIDES · KEEP THE BETTER ONE AS THE DEFAULT')
    t = Table(0, 30, [('id', 28), ('income', 52), ('r', 50, 'spend − ŷ')])
    f.static(T(t.cx(0), t.hb, 'id', MU) + T(t.cx(1), t.hb, 'income', MU) + T(t.cx(2), t.hb, 'r', MU) +
             T(t.cx(2), t.hb + 13, t.cols[2][2], FA) + L(t.x, t.line, t.x + t.w, t.line))
    for i, r in enumerate(DATA):
        v = res(r, 'reg'); m = r[0] in MISS
        f.static(t.row(i, [r[0], '—' if m else str(r[2]), rlab(v, 'reg')], colors={1: AM if m else TX, 2: rc(v)}))
        if m: f.static(R(t.colx(1) + 3, t.ry(i) + 2, 46, 22, 'none', AM, 3, 1.3, '3 3'))
    rx, qy, ky = 500, 60, 170
    Lr, Rr = MW[2][1], MW[2][2]
    f.static(qbox(rx, qy, 'income < 15 ?'))
    for k, (rs, cx) in enumerate(((Lr, 372), (Rr, 612))):
        f.static(L(rx, qy + 13, cx, ky - 20, RULE_HI, 1.2) + yesno(rx, qy + 13, cx, ky - 20, 'yn'[k]) + nbox(cx, ky, len(rs)))
        tt = .4
        for j, r in enumerate(rs):
            i = DATA.index(r); dst = (slot(cx, len(rs), j), ky); src = (t.cx(2), t.ry(i) + 13)
            if r[0] in MISS: continue
            glide(f, rchip(*dst, res(r, 'reg'), 'reg'), [(0,) + src, (tt + .3,) + dst], tt); tt += .3
    f.show(R(222, 218, 360, 56, BG, RULE, 6, 1) + M(234, 240, 'missing → yes :  Gain = %s' % fmt(MW[2][0], 1), GR, 'start'), 2.2)
    f.show(M(234, 262, 'missing → no :  Gain = %s' % fmt(150, 1), MU, 'start'), 2.8)
    f.show(edge_hl({'': (rx, qy), 'y': (372, ky - 9)}, '', 'y', AM) + T(380, 130, 'default', AM, 'end', bold=True), 3.6)
    for j, r in enumerate(Lr):
        if r[0] not in MISS: continue
        i = DATA.index(r); dst = (slot(372, len(Lr), j), ky); src = (t.cx(2), t.ry(i) + 13)
        glide(f, rchip(*dst, res(r, 'reg'), 'reg'), [(0,) + src, (4.4 + j * .2,) + dst], 4.1)
    f.show(S(0, 300, 'the scan only sorts the rows that have a value; missing rows are added to one side as a block', MU), 5.4)
    return finish(f, 312)

# ---------- folding a cut branch back into its node ----------
def vparts(tree, pos):
    nodes, edges = {}, {}
    for p, (x, y) in pos.items():
        n = node_at(tree, p)
        nodes[p] = vpill(x, y, n['leaf'], n['c'], n.get('ids')) if 'leaf' in n else qbox(x, y, n['q'])
        if p:
            px, py = pos[p[:-1]]
            edges[p] = L(px, py + 13, x, y - 11, RULE_HI, 1.2) + yesno(px, py + 13, x, y - 11, p[-1])
    return nodes, edges
def fold_tree(f, tree, pos, cuts, t0, tf):
    """draw tree at t0; every node under a cut slides up into the cut node at tf and vanishes; cuts = {path: merged leaf}"""
    nodes, edges = vparts(tree, pos)
    under = lambda p: next((c for c in cuts if p.startswith(c) and p != c), None)
    for p, e in edges.items():
        f.show(e, t0, hide=tf if under(p) is not None else None)
    for p, s in nodes.items():
        c = under(p)
        if c is not None:
            f.path(s, [(0, 0, 0), (tf, pos[c][0] - pos[p][0], pos[c][1] - pos[p][1])], t0, d=.8, hide=tf + .8)
        elif p in cuts: f.show(s, t0, hide=tf + .7)
        else: f.show(s, t0)
    for c, leaf in cuts.items():
        f.show(vpill(*pos[c], leaf['leaf'], leaf['c'], leaf.get('ids')), tf + .9)
def glab(pos, p, s, c):
    x, y = pos[p]
    if not p: return S(x, y - 22, s, c, 'middle', bold=True)
    return S(x - 10, y - 20, s, c, 'end', bold=True) if p[-1] == 'y' else S(x + 10, y - 20, s, c, 'start', bold=True)

# ---------- 5.1 gamma ----------
def fig_gamma():
    f = Anim('xgb9-', 720, 0, 'The classification tree grown to max_depth 2, gains 1.17 at the root and 0.17 under C D E F. With '
             'gamma 0 both splits stay. With gamma 0.5 the lower split, gain 0.17, is cut: leaves C D and E F slide back up '
             'into their parent, which becomes one leaf of 0.5. With gamma 1.5 the root, gain 1.17, is cut too: everything '
             'folds into one leaf of 0.', 'max_depth = 2 · KEEP A SPLIT ONLY IF  GAIN − γ > 0')
    gr, gl = best(SC['cls'])[2], L2C[2]
    lv = lambda rs, ids: {'leaf': 'w = ' + (fmt(out(rs, 'cls'), 2, True) if out(rs, 'cls') else '0'), 'ids': ids,
                          'c': rc(out(rs, 'cls'))}
    T3 = {'q': 'age < 31.5 ?', 'yes': lv(AB, 'A B'), 'no': {'q': 'age < 46.5 ?', 'yes': lv(CD, 'C D'), 'no': lv(EF, 'E F')}}
    lines = [('both gains > 0', '3 leaves', GR), ('%.2f − 0.5 < 0 · cut' % gl, '2 leaves', RO),
             ('%.2f − 1.5 < 0 · cut' % gr, '1 leaf', RO)]
    cutsets = [{}, {'n': lv(CDEF, 'C D E F')}, {'': lv(DATA, 'A B C D E F')}]
    for k, (gam, (l1, l2, c), cuts) in enumerate(zip(GAMMAS, lines, cutsets)):
        x0 = k * 242; t0 = .3 + k * 2.8
        f.show(R(x0, 30, 236, 290, BG, RULE, 6, 1) + T(x0 + 118, 52, 'γ = %g' % gam, HL, mono=True, bold=True), t0)
        pos = layout(T3, x0 + 4, x0 + 232, 104, 70)
        fold_tree(f, T3, pos, cuts, t0 + .2, t0 + 1.4)
        for p, gn in (('', gr), ('n', gl)):
            keep = gn > gam
            if k == 2 and p == 'n': continue
            f.show(glab(pos, p, 'Gain %.2f' % gn, GR if keep else RO), t0 + .6)
        for p in cuts:
            f.show(R(pos[p][0] - 46, pos[p][1] - 15, 92, 30, 'none', RO, 15, 1.6, '4 3'), t0 + 2.2)
        f.show(S(x0 + 118, 290, l1, c, 'middle', bold=True) + S(x0 + 118, 308, l2, MU, 'middle'), t0 + 1.0)
    assert gl < .5 < gr < 1.5
    return finish(f, 330)

# ---------- 5.2 lambda ----------
CDE = pick(DATA, 'CDE')
def fig_lambda():
    f = Anim('xgb10-', 720, 0, 'The same regression tree scored twice. With lambda 0 every split has a positive gain, 588 at the '
             'root, 2 under A B and 21.3 under C D E F, and the leaves are plain means: minus 15, minus 13, 5.67, 11. With '
             'lambda 1 the gains become 418, minus 64.3 and minus 24.1: the two lower splits fold back and the tree keeps two '
             'leaves, minus 9.33 and plus 5.6.', 'λ LOWERS EVERY GAIN AND SHRINKS EVERY LEAF · SMALL NODES THE MOST')
    def lv(rs, ids, lam):
        w = out(rs, 'reg', lam); return {'leaf': 'w = ' + fmt(w, 2 if w != int(w) else 0, True), 'ids': ids, 'c': rc(w)}
    for k, lam in enumerate((0, 1)):
        x0 = k * 364; t0 = .3 + k * 2.6
        tree = {'q': 'age < 31.5 ?', 'yes': {'q': 'age < 26 ?', 'yes': lv(pick(DATA, 'A'), 'A', lam), 'no': lv(pick(DATA, 'B'), 'B', lam)},
                'no': {'q': 'age < 56 ?', 'yes': lv(CDE, 'C D E', lam), 'no': lv(pick(DATA, 'F'), 'F', lam)}}
        f.show(R(x0, 30, 356, 290, BG, RULE, 6, 1) + T(x0 + 178, 52, 'λ = %d' % lam, HL, mono=True, bold=True), t0)
        pos = layout(tree, x0 + 4, x0 + 352, 104, 74)
        cuts = {} if lam == 0 else {'y': lv(AB, 'A B', 1), 'n': lv(CDEF, 'C D E F', 1)}
        fold_tree(f, tree, pos, cuts, t0 + .2, t0 + 1.6)
        for (q, node, a, b), p in zip(LG, ('', 'y', 'n')):
            gn = a if lam == 0 else b
            f.show(glab(pos, p, 'Gain ' + (g(gn) if gn == int(gn) else fmt(gn, 1)), GR if gn > 0 else RO), t0 + .7)
        for p in cuts:
            f.show(R(pos[p][0] - 46, pos[p][1] - 15, 92, 30, 'none', RO, 15, 1.6, '4 3'), t0 + 2.4)
        f.show(S(x0 + 178, 300, ('3 splits · 4 leaves · leaf = mean of r' if lam == 0 else
                                 '2 gains &lt; 0 · cut · 2 leaves, pulled toward 0'), GR if lam == 0 else RO, 'middle', bold=True), t0 + 1.2)
    f.show(M(0, 346, 'A B:   225/(1+{λ}) + 169/(1+{λ}) − 784/(2+{λ})', TX, 'start') +
           S(430, 346, 'λ = 0 → 2  ·  λ = 1 → −64.3', MU), 5.8)
    assert out(CDE, 'reg', 0) == 17 / 3 and out(pick(DATA, 'F'), 'reg', 0) == 11
    return finish(f, 358)

# ---------- 5.3 min_child_weight ----------
def fig_mcw():
    f = Anim('xgb11-', 720, 0, 'The root split age under 31.5 checked against min_child_weight 1. Regression: each row adds 1 to '
             'Cover, A B has 2 and C D E F has 4, both pass and the split stays. Classification: each row adds 0.25, A B has '
             '0.5 and fails, so the two children fold back into the root, which stays one leaf of 0.',
             'A CHILD NEEDS COVER ≥ min_child_weight = 1')
    for k, kind in enumerate(('reg', 'cls')):
        x0 = k * 364; t0 = .3 + k * 2.8
        f.show(R(x0, 30, 356, 270, BG, RULE, 6, 1) + T(x0 + 178, 52, 'regression · h = 1' if k == 0 else
               'classification · h = 0.25', HL, mono=True, bold=True), t0)
        rx, qy, ky = x0 + 178, 96, 196
        f.show(qbox(rx, qy, 'age < 31.5 ?'), t0, hide=(t0 + 2.4) if k else None)
        each = '1' if k == 0 else '0.25'
        for j, (ids, rs, cx) in enumerate((('A B', AB, x0 + 88), ('C D E F', CDEF, x0 + 268))):
            cv = COV(rs, kind); ok = cv >= 1
            box = (L(rx, qy + 13, cx, ky - 20, RULE_HI, 1.2) + yesno(rx, qy + 13, cx, ky - 20, 'yn'[j]))
            node = sbox(cx, ky, ids, 'Cover %d × %s = %s' % (len(rs), each, g(cv)), GR if ok else RO, GR if ok else RO)
            if k == 0:
                f.show(box, t0 + .3); f.show(node, t0 + .5 + j * .3)
            else:
                f.show(box, t0 + .3, hide=t0 + 1.8)
                f.path(node, [(0, 0, 0), (t0 + 1.8, rx - cx, qy - ky)], t0 + .5 + j * .3, d=.8, hide=t0 + 2.6)
            f.show(pill(cx, ky + 30, 'ok' if ok else 'too small', 'gr' if ok else 'rd'), t0 + 1.1 + j * .2,
                   hide=(t0 + 1.8) if k else None)
        if k:
            f.show(vpill(rx, qy, 'w = 0', MU, 'A B C D E F'), t0 + 2.6)
            f.show(S(rx, 150, 'A B: Cover 0.5 &lt; 1', RO, 'middle'), t0 + 2.8)
            f.show(S(rx, 270, 'split not allowed · one leaf', RO, 'middle', bold=True), t0 + 2.8)
        else:
            f.show(S(rx, 270, 'both children pass · split kept', GR, 'middle', bold=True), t0 + 1.6)
    assert [COV(AB, 'reg'), COV(CDEF, 'reg'), COV(AB, 'cls'), COV(CDEF, 'cls')] == [2, 4, .5, 1]
    return finish(f, 310)

# ---------- body ----------
EQ_OBJ = r'''  <div class="eq">
    <div class="line">
      <span class="t"><span>Obj</span><em>what each tree minimises</em></span>
      <span class="op">=</span>
      <span class="t b"><span>Σ<sub><var>i</var></sub> <var>l</var>(<var>y</var><sub><var>i</var></sub>, <var>ŷ</var><sub><var>i</var></sub>)</span><em>loss of every row</em></span>
      <span class="op">+</span>
      <span class="t p"><span><var>γ</var><var>T</var></span><em>price per leaf</em></span>
      <span class="op">+</span>
      <span class="t r"><span>½ <var>λ</var> Σ<sub><var>j</var></sub> <var>w</var><sub><var>j</var></sub><sup>2</sup></span><em>price on leaf size</em></span>
    </div>
    <div class="line">
      <span class="t"><span>Obj</span><em>loss as a parabola per leaf</em></span>
      <span class="op">≈</span>
      <span class="t b"><span>Σ<sub><var>j</var></sub> [ <var>G</var><sub><var>j</var></sub><var>w</var><sub><var>j</var></sub> + ½ (<var>H</var><sub><var>j</var></sub> + <var>λ</var>) <var>w</var><sub><var>j</var></sub><sup>2</sup> ]</span><em>G, H = Σ g, Σ h in leaf j</em></span>
      <span class="op">+</span>
      <span class="t p"><span><var>γ</var><var>T</var></span><em>price per leaf</em></span>
    </div>
    <div class="line">
      <span class="t g"><span><var>w</var><sub><var>j</var></sub><sup>*</sup></span><em>bottom of the parabola</em></span>
      <span class="op">=</span>
      <span class="t g"><span>− <span class="frac"><i><var>G</var><sub><var>j</var></sub></i><i><var>H</var><sub><var>j</var></sub> + <var>λ</var></i></span></span><em>Output value</em></span>
    </div>
  </div>'''

def eq_sim(cov):
    return r'''  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">Similarity</b></span><em>score of one node</em></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i>(Σ<sub><var>i</var></sub> <var>r</var><sub><var>i</var></sub>)<sup>2</sup></i><i>%s + <var>λ</var></i></span></span><em>r = residual · denominator = Cover + λ</em></span>
    </div>
  </div>''' % cov

def eq_out(cov):
    return r'''  <div class="eq">
    <div class="line">
      <span class="t g"><span><b class="fn">Output</b></span><em>value the leaf returns</em></span>
      <span class="op">=</span>
      <span class="t g"><span><span class="frac"><i>Σ<sub><var>i</var></sub> <var>r</var><sub><var>i</var></sub></i><i>%s + <var>λ</var></i></span></span><em>the w* of section 02</em></span>
    </div>
  </div>''' % cov

COV_REG = '<var>n</var>'
COV_CLS = 'Σ<sub><var>i</var></sub> <var>p</var><sub><var>i</var></sub>(1 − <var>p</var><sub><var>i</var></sub>)'

EQ_GAIN = r'''  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">Gain</b></span><em>what the split earns</em></span>
      <span class="op">=</span>
      <span class="t b"><span><b class="fn">Sim</b><sub>L</sub></span><em>left child</em></span>
      <span class="op">+</span>
      <span class="t b"><span><b class="fn">Sim</b><sub>R</sub></span><em>right child</em></span>
      <span class="op">−</span>
      <span class="t"><span><b class="fn">Sim</b><sub>node</sub></span><em>before the split</em></span>
    </div>
  </div>'''

SCRIPT = DT_BODY[DT_BODY.index('<script>'):DT_BODY.index('</script>') + len('</script>')]

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Tree models</p>
  <h1><em>XGBoost</em></h1>
  <p class="lede">XGBoost is gradient boosting whose every tree is grown by <b>one scored formula</b>: residuals summed per node decide the splits and the leaf values, with γ and λ keeping both small.</p>
</header>

<section id="xgb-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Each round fits one tree to the residuals, but <em>a formula</em> picks its splits and its leaf values.</p>
{x1}
  <ul class="why">
    <li>The same six customers as <a href="../decision-tree/index.html">Decision tree</a>; here the target is spend.</li>
    <li>Residuals, the small step <span class="mth"><var>η</var></span> and adding trees up are <a href="../gradient-boosting/index.html">Gradient boosting</a>; this lesson is only how XGBoost grows one tree.</li>
  </ul>
</section>

<section id="xgb-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Objective</h2></div>
  <p class="key">Loss plus a <em>price per leaf</em> and a <em>price on leaf size</em>; each leaf's part is a parabola with a known bottom.</p>
{eqobj}
{x2}
  <ul class="why">
    <li><span class="mth"><var>g</var></span>, <span class="mth"><var>h</var></span> are the slope and curvature of the loss at each row; the loss enters only through them.</li>
    <li>Squared error gives <span class="mth"><var>g</var> = −<var>r</var></span>, <span class="mth"><var>h</var> = 1</span>; log loss gives <span class="mth"><var>g</var> = −<var>r</var></span>, <span class="mth"><var>h</var> = <var>p</var>(1 − <var>p</var>)</span>. <span class="mth"><var>H</var></span> is called <b>Cover</b>.</li>
  </ul>
</section>

<section id="xgb-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Regression</h2></div>
  <p class="key">Squared error: residual <em>spend − ŷ</em>, every row adds 1 to Cover.</p>
  <div class="subsec" id="xgb-s3-1">
    <h3 class="ssh"><b>3.1</b>Similarity</h3>
    <p class="skey">How well one value fits a node: <em>large when residuals agree in sign</em>, 0 when they cancel.</p>
{eqsimreg}
{x3}
    <ul class="why">
      <li>It is the depth of the parabola's bottom, times 2: section 02.</li>
    </ul>
  </div>
  <div class="subsec" id="xgb-s3-2">
    <h3 class="ssh"><b>3.2</b>Gain &amp; split</h3>
    <p class="skey">Try <em>every column × every threshold</em>; keep the split whose children gain the most Similarity.</p>
{eqgain}
{x4}
    <ul class="why">
      <li>The same greedy scan as <a href="../decision-tree/index.html">Decision tree</a>; only the score changes.</li>
      <li>The root has Similarity 0 because the start value 25 is the mean: the residuals sum to 0.</li>
    </ul>
  </div>
  <div class="subsec" id="xgb-s3-3">
    <h3 class="ssh"><b>3.3</b>Output value</h3>
    <p class="skey">A leaf returns its residual sum over <em>Cover + λ</em>: the mean, pulled toward 0.</p>
{eqoutreg}
{x5}
    <ul class="why">
      <li>The tree adds <span class="mth"><var>η</var> × <var>w</var></span> to the prediction; the next tree learns what is left.</li>
    </ul>
  </div>
</section>

<section id="xgb-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Classification</h2></div>
  <p class="key">Log loss: residual <em>y − p</em>, every row adds <em>p(1 − p)</em> to Cover; leaves speak log-odds.</p>
  <div class="subsec" id="xgb-s4-1">
    <h3 class="ssh"><b>4.1</b>Similarity</h3>
    <p class="skey">Same score, new Cover: <em>large when residuals agree in sign</em>, 0 when they cancel.</p>
{eqsimcls}
{x6}
    <ul class="why">
      <li>Every prediction starts at <span class="mth"><var>p</var> = 0.5</span>, so residuals are ±0.5 and each row adds 0.25 to Cover.</li>
    </ul>
  </div>
  <div class="subsec" id="xgb-s4-2">
    <h3 class="ssh"><b>4.2</b>Gain &amp; split</h3>
    <p class="skey">The same Gain formula and the same scan as 3.2, on the new Similarity.</p>
{x7}
    <ul class="why">
      <li>Same winner as regression here, age 31.5 — the residual column decides, and both happen to split there.</li>
      <li>This split needs <code>min_child_weight=0</code>: under the default 1, leaf A B (Cover 0.5) is too light — section 7.3.</li>
    </ul>
  </div>
  <div class="subsec" id="xgb-s4-3">
    <h3 class="ssh"><b>4.3</b>Output value</h3>
    <p class="skey">A leaf returns residual sum over <em>Cover + λ</em>, in <em>log-odds</em>; σ turns it back into a probability.</p>
{eqoutcls}
{x8}
    <ul class="why">
      <li>This is one Newton step on the log loss, not a mean: the λ = 0 value −2 lies outside the residuals.</li>
    </ul>
  </div>
</section>

<section id="xgb-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Prediction</h2></div>
  <p class="key">A new row walks <em>every tree</em> to one leaf; the prediction is the start plus <em>η × the sum</em> of those leaf values.</p>
{x12}
  <ul class="why">
    <li><span class="mth"><var>η</var></span> (<code>learning_rate</code>, default 0.3) is the shrinkage of <a href="../gradient-boosting/index.html">Gradient boosting</a>: each tree moves the prediction only part of the way.</li>
    <li>Each tree is grown to at most <code>max_depth</code> (default 6) levels.</li>
  </ul>
</section>

<section id="xgb-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Missing values</h2></div>
  <p class="key">Every split learns a <em>default direction</em>: rows with a missing value go to whichever side gives the larger Gain.</p>
{x13}
  <ul class="why">
    <li>Called the sparsity-aware split: no imputation needed, and zeros in a sparse matrix can be treated the same way.</li>
    <li>At prediction time a row missing that column follows the stored default arrow.</li>
  </ul>
</section>

<section id="xgb-s7" class="lesson">
  <div class="sh"><b>07</b><h2>Reining it in</h2></div>
  <p class="key">The penalties sit inside the score, so <em>the tree stops itself</em> when a split is not worth its price.</p>
  <div class="subsec" id="xgb-s7-1">
    <h3 class="ssh"><b>7.1</b>γ — pruning</h3>
    <p class="skey">Every leaf costs <span class="mth"><var>γ</var></span>: a split whose <em>Gain is below γ</em> is cut, bottom up.</p>
{x9}
    <ul class="why">
      <li><code>gamma</code> (alias <code>min_split_loss</code>), default 0. The library drops the ½, so Gain is compared with <span class="mth"><var>γ</var></span> directly.</li>
      <li>The tree is grown to <code>max_depth</code> first, then pruned bottom up.</li>
    </ul>
  </div>
  <div class="subsec" id="xgb-s7-2">
    <h3 class="ssh"><b>7.2</b>λ — shrinking</h3>
    <p class="skey"><span class="mth"><var>λ</var></span> sits in every denominator: <em>leaf values and gains shrink</em>, most in small nodes.</p>
{x10}
    <ul class="why">
      <li><code>reg_lambda</code>, default 1; <code>reg_alpha</code> adds an L1 price that can set a leaf to exactly 0.</li>
      <li>With λ = 1 the regression tree here stops at depth 1 on its own, even with γ = 0.</li>
    </ul>
  </div>
  <div class="subsec" id="xgb-s7-3">
    <h3 class="ssh"><b>7.3</b>min_child_weight</h3>
    <p class="skey">A child must carry <em>Cover ≥ min_child_weight</em>; otherwise the split is not allowed.</p>
{x11}
    <ul class="why">
      <li>In classification Cover shrinks as <span class="mth"><var>p</var></span> nears 0 or 1, so confident nodes stop splitting; section 04 assumes <code>min_child_weight=0</code>.</li>
      <li>Further brakes are <a href="../gradient-boosting/index.html">Gradient boosting</a>'s: small <span class="mth"><var>η</var></span>, early stopping, and random subsets — <code>subsample</code> (rows per tree) and <code>colsample_bytree</code> (columns per tree), both default 1.</li>
    </ul>
  </div>
</section>

{script}

<footer>Machine learning · Tree models · next lesson in the branch: <a href="../lightgbm/index.html">LightGBM</a>.</footer>
'''

def build():
    figs = dict(x1=fig_mental(), x2=fig_objective(), x3=fig_sim('reg'), x4=fig_scan('reg'), x5=fig_output('reg'),
                x6=fig_sim('cls'), x7=fig_scan('cls'), x8=fig_output('cls'), x9=fig_gamma(), x10=fig_lambda(), x11=fig_mcw(), x12=fig_predict(), x13=fig_missing(),
                eqobj=EQ_OBJ, eqsimreg=eq_sim(COV_REG), eqsimcls=eq_sim(COV_CLS), eqoutreg=eq_out(COV_REG),
                eqoutcls=eq_out(COV_CLS), eqgain=EQ_GAIN, script=SCRIPT)
    return re.sub(r'\{([a-z0-9]+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'Gradient boosting with a scored tree: Similarity, Gain and Output value from residual sums and '
           'Cover, with γ, λ and min_child_weight built into the objective.')
