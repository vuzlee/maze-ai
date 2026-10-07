# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/06-tree-models/adaboost.
Same six customers as decision_tree.py (y = +1 buy / -1 no), boosted with stumps; every number in a figure is
computed here and pinned with assert. The 300 noisy points of decision_tree.py drive the rounds / noise figures.
Run: python3 adaboost.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, finish)
from tablefig import GR, tint, pill
from decision_tree import (DATA, COLS, LAB, CL, HL, pt, legend, TR, TE, splice, layout, draw_tree, node_at, edge_hl,
                           qring, lring, leafp, qbox)

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/06-tree-models/adaboost/index.html')
IDS = [r[0] for r in DATA]
Y = {r[0]: 1 if r[4] else -1 for r in DATA}

# ---------- stumps on the six customers ----------
def stumps(rows=DATA):
    """every column x every threshold x both directions -> (col, thr, s, h); s=+1: buy if value >= thr"""
    out = []
    for c in range(3):
        vs = sorted(set(r[c + 1] for r in rows))
        for a, b in zip(vs, vs[1:]):
            t = (a + b) / 2
            for s in (1, -1):
                out.append((COLS[c], t, s, {r[0]: (s if r[c + 1] >= t else -s) for r in rows}))
    return out
ST = stumps()
def werr(h, w): return sum(w[k] for k in IDS if h[k] != Y[k])

def boost(n):
    w = {k: 1 / 6 for k in IDS}; out = []
    for _ in range(n):
        best = None
        for st in ST:
            if best is None or werr(st[3], w) < werr(best[3], w) - 1e-12: best = st
        e = werr(best[3], w); a = .5 * math.log((1 - e) / e)
        raw = {k: w[k] * math.exp(-a * Y[k] * best[3][k]) for k in IDS}; Z = sum(raw.values())
        out.append(dict(st=best, w=w, err=e, a=a, raw=raw, Z=Z, wrong=[k for k in IDS if best[3][k] != Y[k]]))
        w = {k: raw[k] / Z for k in IDS}
    return out
RD3 = boost(3)
assert [(r['st'][0], r['st'][1], r['st'][2]) for r in RD3] == [('age', 31.5, 1), ('age', 56, 1), ('age', 46.5, -1)]
assert [''.join(r['wrong']) for r in RD3] == ['E', 'CD', 'ABF']
assert [round(r['err'], 4) for r in RD3] == [.1667, .2, .1875]
assert [round(r['a'], 3) for r in RD3] == [.805, .693, .733]
W2 = {k: round(v, 4) for k, v in RD3[1]['w'].items()}
assert W2 == dict(A=.1, B=.1, C=.1, D=.1, E=.5, F=.1)
assert round(RD3[0]['Z'], 3) == .745 and round(sum(RD3[1]['w'][k] for k in RD3[0]['wrong']), 6) == .5
RULES = ['buy if age ≥ 31.5', 'buy if age ≥ 56', 'buy if age < 46.5']
VOTE = {k: [r['a'] * r['st'][3][k] for r in RD3] for k in IDS}
FX = {k: sum(VOTE[k]) for k in IDS}
assert all((FX[k] > 0) == (Y[k] > 0) for k in IDS)                  # three stumps fit all six rows
assert [round(FX[k], 2) for k in 'ACEF'] == [-.76, .84, -.62, .76]
ALONE = [len(r['wrong']) for r in RD3]; assert ALONE == [1, 2, 3]
def F_age(age): return sum(r['a'] * (r['st'][2] if age >= r['st'][1] else -r['st'][2]) for r in RD3)
assert round(F_age(45), 3) == .845 and F_age(45) > 0                 # new customer X, age 45 -> buy
fmt = lambda v: ('−' if v < 0 else '+') + '%.2f' % abs(v)

# ---------- AdaBoost on the 300 noisy points of decision_tree.py ----------
def make_flags(n, seed):
    """the same generator as decision_tree.make, also returning which labels were flipped"""
    g = random.Random(seed); P = []
    for _ in range(n):
        x, y = g.random(), g.random(); c = int((x - .5) ** 2 + (y - .5) ** 2 < .33 ** 2); fl = g.random() < .08
        P.append((x, y, 1 - c if fl else c, fl))
    return P
TRF = make_flags(300, 1); assert [q[:3] for q in TRF] == TR
FLIP = [q[3] for q in TRF]; NFLIP = sum(FLIP); assert NFLIP == 34

def best_stump(P, w):
    best = None; W = sum(w)
    for f in (0, 1):
        idx = sorted(range(len(P)), key=lambda i: P[i][f])
        e = sum(w[i] for i in idx if P[i][2] == 0)         # threshold below everything, buy everywhere
        cands = [(e, -1.0)]
        for k, i in enumerate(idx):
            e += w[i] if P[i][2] == 1 else -w[i]
            if k + 1 < len(idx) and P[idx[k + 1]][f] == P[i][f]: continue
            cands.append((e, (P[i][f] + P[idx[k + 1]][f]) / 2 if k + 1 < len(idx) else 2.0))
        for e, t in cands:
            for s, ee in ((1, e), (-1, W - e)):
                if best is None or ee < best[0] - 1e-12: best = (ee, f, t, s)
    return best

def run(lr, n, keep=None):
    w = [1 / len(TR)] * len(TR); Ftr = [0.0] * len(TR); Fte = [0.0] * len(TE); out, kept = [], None
    for r in range(1, n + 1):
        e, f, t, s = best_stump(TR, w); a = lr * .5 * math.log((1 - e) / e)
        h = lambda q: s if q[f] >= t else -s
        for i, q in enumerate(TR): Ftr[i] += a * h(q)
        for i, q in enumerate(TE): Fte[i] += a * h(q)
        w = [w[i] * math.exp(-a * (2 * q[2] - 1) * h(q)) for i, q in enumerate(TR)]; Z = sum(w); w = [x / Z for x in w]
        out.append((r, sum((Ftr[i] > 0) != q[2] for i, q in enumerate(TR)) / 300,
                    sum((Fte[i] > 0) != q[2] for i, q in enumerate(TE)) / 300))
        if r == keep: kept = w[:]
    return out, kept
N = 1000
C1, WK = run(1, N, keep=100); C01, _ = run(.1, N)
B1 = min(C1, key=lambda c: c[2]); B01 = min(C01, key=lambda c: c[2])
assert (B1[0], round(B1[2], 3)) == (102, .133) and round(C1[-1][2], 2) == .19 and round(C1[-1][1], 3) == .037
assert (B01[0], round(B01[2], 2)) == (578, .13) and round(C01[-1][2], 3) == .147
assert round(C1[0][2], 3) == .367
HEAVY = sorted(range(300), key=lambda i: -WK[i])[:10]; assert all(FLIP[i] for i in HEAVY)
SHARE0, SHARE = NFLIP / 300, sum(WK[i] for i in range(300) if FLIP[i])
assert round(SHARE0, 2) == .11 and round(SHARE, 2) == .30

def wbar(x, y, w, sc, c=VI, num=True):
    s = R(x, y + 6, max(w * sc, 1.5), 14, tn(c, '.30'), c, 2, 1)
    if num: s += T(x + w * sc + 5, y + 17, ('%.2f' % w).lstrip('0'), MU, 'start', mono=True)
    return s

# ---------- stumps drawn as trees ----------
def stump_tree(rd, w=None):
    col, thr, s, h = rd['st']
    lo = [n for n in IDS if DATA[IDS.index(n)][COLS.index(col) + 1] < thr]; hi = [n for n in IDS if n not in lo]
    ly, ln = ('no', 'buy') if s == 1 else ('buy', 'no')
    assert all(h[n] == (1 if ly == 'buy' else -1) for n in lo) and all(h[n] == (1 if ln == 'buy' else -1) for n in hi)
    return {'q': '%s < %g ?' % (col, thr), 'yes': {'leaf': ly, 'ids': ' '.join(lo)}, 'no': {'leaf': ln, 'ids': ' '.join(hi)}}
TREES = [stump_tree(rd) for rd in RD3]

def tok(x, y, n, w=26):
    c = CL[LAB[n]]
    return R(x, y, w, 20, BG, 'none', 4) + R(x, y, w, 20, tn(c, '.16'), c, 4, 1.2) + T(x + w / 2, y + 14.5, n, c, mono=True, bold=True)

def slots(tree, pos, y_off=22):
    """token top-left per id under its leaf"""
    out = {}
    for ch in 'yn':
        ids = tree['yes' if ch == 'y' else 'no']['ids'].split(); cx, cy = pos[ch]; m = len(ids)
        for k, n in enumerate(ids): out[n] = (cx - (m * 30 - 4) / 2 + k * 30, cy + y_off)
    return out

def drop(f, t, n, sx, sy, lane, t0, hide=None, gap=-34, d=.35):
    """token leaves the id cell to the left gutter, runs down, along a lane under the table, then up into its slot"""
    i = IDS.index(n); x0, y0 = t.colx(0) + 1, t.ry(i) + 3
    f.path(tok(x0, y0, n), [(0, 0, 0), (t0, gap, 0), (t0 + d, gap, lane - y0), (t0 + 2 * d, sx - x0, lane - y0),
                            (t0 + 3 * d, sx - x0, sy - y0)], t0 - .3, d=d, hide=hide)

# ---------- 01 Mental model ----------
def wcol(t, w, sc, prev=None, c=VI):
    """the whole w column redrawn: opaque backing, the previous width as a dashed ghost, the new bar"""
    j = 3; x = t.colx(j) + 4; s = ''
    for i, n in enumerate(IDS):
        y = t.ry(i)
        s += R(t.colx(j) + 1, y + 1, t.cols[j][1] - 2, t.rh - 2, BG, 'none', 2)
        if prev: s += R(x, y + 6, prev[n] * sc, 14, 'none', FA, 2, 1, '3 2')
        cc = RO if prev and w[n] > prev[n] + 1e-9 else c
        s += R(x, y + 6, max(w[n] * sc, 1.5), 14, tn(cc, '.30'), cc, 2, 1)
        s += T(x + max(w[n], prev[n] if prev else 0) * sc + 5, y + 17, ('%.2f' % w[n]).lstrip('0'), MU, 'start', mono=True)
    return s

def fig_mental():
    f = Anim('ada1-', 720, 0, 'Round 1: the six customers each weigh 1/6. The stump age under 31.5 is drawn: A and B drop into its '
             'no-buy leaf, C to F into its buy leaf; E lands wrong, so err is 0.17 and alpha 0.80. E\'s weight grows to 0.50, '
             'the others shrink to 0.10, and that column is round 2\'s input. Round 2: the stump age under 56 gets C and D '
             'wrong, err 0.20, alpha 0.69. Round 3: the stump age under 46.5, buy on the yes side, gets A, B and F wrong, err '
             '0.19, alpha 0.73. At the end the three stumps stand side by side with their alphas, and the sign of their '
             'weighted vote is right on all six rows.',
             'WEIGHTED TABLE → STUMP → MISTAKES GROW HEAVIER → NEXT STUMP · THEN THEY VOTE')
    t = Table(36, 30, [('id', 28), ('age', 40), ('buy?', 46), ('w', 110)])
    sc = 150
    f.static(t.head())
    for i, r in enumerate(DATA):
        f.static(t.row(i, [r[0], str(r[1]), 'buy' if LAB[r[0]] == 'buy' else 'no', ''], colors={2: CL[LAB[r[0]]]}))
    LANE = t.ry(5) + t.rh + 10
    RC = 600
    T0s = [.4 + k * 6.2 for k in range(3)]
    ws = [rd['w'] for rd in RD3]
    f.show(wcol(t, ws[0], sc), .2, hide=T0s[0] + 5.6)
    for k, rd in enumerate(RD3):
        T0 = T0s[k]; nxt = T0s[k + 1] if k < 2 else None
        tree = TREES[k]; pos = layout(tree, 300, 570, 64, 74); sl = slots(tree, pos)
        f.show(S(RC, 44, 'round %d' % (k + 1), TX, bold=True) + S(RC, 62, 'w from the table', MU), T0, hide=nxt)
        f.show(draw_tree(tree, pos, ids=False), T0 + .4, hide=nxt)
        for q, n in enumerate(IDS):
            drop(f, t, n, *sl[n], LANE, T0 + 1.2 + q * .3, nxt)
            tr = T0 + 3.9
        f.show(''.join(R(sl[n][0] - 3, sl[n][1] - 3, 32, 26, 'none', RO, 6, 1.8) + t.outline(IDS.index(n), c=RO, sw=1.6)
                       for n in rd['wrong']), tr, hide=nxt)
        f.show(chip(RC + 50, 100, 'err %.2f' % rd['err'], RO, 100) + S(RC, 124, 'w of the ringed rows', MU), tr + .4, hide=nxt)
        f.show(chip(RC + 50, 152, 'α %.2f' % rd['a'], VI, 100), tr + .8, hide=nxt)
        if k < 2:
            tu = T0 + 5.3
            f.show(S(RC, 186, 'wrong × %.2f' % math.exp(rd['a']), RO, bold=True) +
                   S(RC, 204, 'right × %.2f' % math.exp(-rd['a']), VI) + S(RC, 222, '÷ Z → sum 1', MU), tu, hide=nxt)
            f.show(wcol(t, ws[k + 1], sc, prev=ws[k]), T0 + 5.6, hide=None if k == 1 else T0s[1] + 5.6)
    # three stumps side by side, then the vote
    TS = T0s[2] + 5.4
    y0 = 300
    f.show(L(0, y0 - 26, 720, y0 - 26, RULE, 1), TS - .2)
    for k, rd in enumerate(RD3):
        pos = layout(TREES[k], 10 + k * 240, 230 + k * 240, y0, 54)
        f.show(draw_tree(TREES[k], pos) + chip(pos[''][0], y0 + 104, 'α%s %.2f' % ('₁₂₃'[k], rd['a']), VI, 80), TS + k * .4)
        if k: f.show(T(k * 240, y0 + 108, '+', TX, 'middle', 'sv-d', bold=True), TS + k * .4)
    f.show(M(10, y0 + 146, '{F}({x}) = 0.80 {h}₁ + 0.69 {h}₂ + 0.73 {h}₃  ·  {ŷ} = sign {F}({x})', TX, 'start'), TS + 1.4)
    f.show(pill(640, y0 + 131, '6 / 6 rows right', 'gr'), TS + 1.9)
    assert all((FX[n] > 0) == (Y[n] > 0) for n in IDS)
    return finish(f, y0 + 160)

# ---------- 02 Stump ----------
def cands(w):
    """per column x threshold: the better direction's weighted err"""
    out = []
    for st in ST[::2]:
        e = werr(st[3], w); out.append((st[0], st[1], min(e, 1 - e)))
    return out

def fig_stump():
    w1, w2 = RD3[0]['w'], RD3[1]['w']
    c1, c2 = cands(w1), cands(w2)
    assert min(c1, key=lambda c: c[2])[:2] == ('age', 31.5) and round(min(c[2] for c in c1), 2) == .17
    assert min(c2, key=lambda c: c[2])[:2] == ('age', 56) and round(min(c[2] for c in c2), 2) == .2
    assert [c[:2] for c in c2 if round(c[2], 4) == .2] == [('age', 56), ('income', 32)]
    assert round(dict(((c[0], c[1]), c[2]) for c in c2)[('age', 31.5)], 2) == .5
    f = Anim('ada2-', 720, 0, 'Every column and threshold is tried and scored by the total weight of the rows it gets wrong. '
             'Round 1, all weights 1/6: the best cut is age 31.5, wrong on E only, err 0.17. It becomes a stump: one question, '
             'age under 31.5, and two leaves; A and B drop into the no-buy leaf, C to F into the buy leaf, E is ringed. '
             'Round 2, E weighs 0.50: the same cut now scores 0.50, and the best cut moves to age 56, wrong on C and D, '
             'err 0.20; income 32 ties. The new stump sends A to E to no buy and F to buy, with C and D ringed.',
             'TRY EVERY CUT · THE LIGHTEST MISTAKES WIN · THE WINNER BECOMES A STUMP')
    OX = 34
    t = Table(OX, 44, [('id', 28), ('age', 40), ('income', 52), ('buy?', 46), ('w', 44)])
    f.static(t.head())
    for i, r in enumerate(DATA):
        f.static(t.row(i, [r[0], str(r[1]), str(r[2]), 'buy' if LAB[r[0]] == 'buy' else 'no', '.17'],
                       colors={3: CL[LAB[r[0]]]}))
    LX, BX, top, step, sc = 282, 382, 66, 21, 440
    PH = 7.8
    f.show(S(LX, 40, 'round 1 · every w = 1/6', HL, bold=True), .3, hide=PH)
    f.show(S(LX, 40, 'round 2 · w after round 1', HL, bold=True), PH + .3)
    for i, n in enumerate(IDS):
        v = ('%.2f' % w2[n]).lstrip('0')
        f.show(t.cell(i, 4, v, c=VI if w2[n] > .2 else TX), PH + .2 + i * .05)
    ybot = top + len(c1) * step + 8
    LANE, SY = ybot + 14, ybot + 52
    for ph, cs, t0 in ((1, c1, .8), (2, c2, PH + .9)):
        hid = PH if ph == 1 else None
        best = min(cs, key=lambda c: c[2]); kb = cs.index(best)
        for k, (col, thr, e) in enumerate(cs):
            y = top + k * step
            if ph == 1: f.static(T(LX, y + 13, 'bought before' if col == 'bought before' else '%s < %g' % (col, thr),
                                   TX if col == 'age' else MU, 'start', 'sv-s'))
            bar = R(BX, y + 3, e * sc, 14, tn(RO, '.26'), RO, 2, 1) + T(BX + e * sc + 6, y + 14, '%.2f' % e, MU, 'start', mono=True)
            f.show(bar, t0 + k * .22, hide=hid)
        y = top + kb * step; tw = t0 + len(cs) * .22 + .3
        f.show(R(BX, y + 3, best[2] * sc, 14, BG, 'none', 2) + R(BX, y + 3, best[2] * sc, 14, tint('gr', '.35'), GR, 2, 1.6) +
               pill(BX + best[2] * sc + 80, y + 1, 'lowest err', 'gr'), tw, hide=hid)
        if ph == 2:
            ki = [c[:2] for c in cs].index(('income', 32)); yi = top + ki * step
            f.show(S(BX + .2 * sc + 44, yi + 14, 'tie · first kept', MU), tw + .2)
        sl = {31.5: 2, 56: 5}[best[1]]; yc = t.ry(sl) - 2
        rd = RD3[ph - 1]; assert (rd['st'][0], rd['st'][1]) == best[:2] and round(rd['err'], 6) == round(best[2], 6)
        wr = [IDS.index(n) for n in rd['wrong']]
        ring = L(OX - 4, yc, OX + t.w + 4, yc, GR, 2, '5 4') + ''.join(t.outline(i, i, c=RO, sw=1.8) for i in wr)
        f.show(ring, tw + .3, hide=hid)
        eq = ('err = {w}_E = 0.17' if ph == 1 else 'err = {w}_C + {w}_D = 0.10 + 0.10 = 0.20')
        f.show(M(OX, t.ry(6) + 22, eq.replace('_E', '<tspan dy="3" font-size="10">E</tspan><tspan dy="-3"> </tspan>')
                 .replace('_C', '<tspan dy="3" font-size="10">C</tspan><tspan dy="-3"> </tspan>')
                 .replace('_D', '<tspan dy="3" font-size="10">D</tspan><tspan dy="-3"> </tspan>'), TX, 'start'),
               tw + .6, hide=hid)
        # the winner drawn as a stump; rows drop into its leaves
        tree = TREES[ph - 1]; pos = layout(tree, 120, 560, SY, 70); sl2 = slots(tree, pos)
        ts = tw + 1.0
        f.show(arrow(BX + best[2] * sc / 2, top + kb * step + 20, pos[''][0] + 60, SY - 14, GR, 1.2, '3 3') +
               draw_tree(tree, pos, ids=False), ts, hide=hid)
        for q, n in enumerate(IDS):
            drop(f, t, n, *sl2[n], LANE, ts + .6 + q * .25, hid)
        f.show(''.join(R(sl2[n][0] - 3, sl2[n][1] - 3, 32, 26, 'none', RO, 6, 1.8) for n in rd['wrong']) +
               S(pos['n'][0] + 90, pos['n'][1] + 4, 'ringed = wrong', RO), ts + .6 + 6 * .25 + 1.1, hide=hid)
    return finish(f, SY + 70 + 50)

# ---------- 3.1 alpha ----------
def alpha(e): return .5 * math.log((1 - e) / e)

def fig_alpha():
    f = Anim('ada3-', 720, 0, 'The vote weight alpha against the stump error. At err 0.5, a coin flip, alpha is 0. Below 0.5 '
             'alpha rises, and runs to infinity as err goes to 0; above 0.5 it turns negative. The three rounds sit at err '
             '0.17, 0.20 and 0.19, giving alpha 0.80, 0.69 and 0.73.', 'VOTE WEIGHT α · BY THE STUMP\'S ERROR')
    x0, sx, yz, sy = 50, 600, 236, 84
    PX = lambda e: x0 + e * sx
    PY = lambda a: yz - a * sy
    f.static(R(PX(.5), PY(2.1), PX(.6) - PX(.5), PY(-.45) - PY(2.1), tn(RO, '.07'), 'none', 0))
    f.static(L(x0, PY(-.45), x0, PY(2.1), RULE_HI, 1.3) + L(x0, yz, PX(.6), yz, RULE_HI, 1.3))
    for a in (1, 2):
        f.static(L(x0, PY(a), PX(.6), PY(a), RULE, 1) + T(x0 - 8, PY(a) + 4, str(a), FA, 'end', mono=True))
    f.static(T(x0 - 8, yz + 4, '0', FA, 'end', mono=True))
    for e in (.1, .2, .3, .4, .5): f.static(L(PX(e), PY(-.45), PX(e), PY(-.45) + 4, RULE_HI, 1) + T(PX(e), PY(-.45) + 16, '%g' % e, FA, mono=True))
    f.static(L(x0, PY(-.45), PX(.6), PY(-.45), RULE_HI, 1.3))
    f.static(M(PX(.6), PY(-.45) + 34, 'err', MU, 'end') + M(x0, PY(2.1) - 8, '{α}', MU))
    f.static(S(PX(.55), PY(1.6), 'worse than', RO, 'middle') + S(PX(.55), PY(1.6) + 15, 'a coin flip', RO, 'middle'))
    es = [.018 + i * (.6 - .018) / 80 for i in range(81)]
    f.show(poly([(PX(e), PY(alpha(e))) for e in es], HL, 2.4), .3)
    f.show(dot(PX(.5), yz, RO, 5, BG) + S(PX(.5) + 8, yz - 10, 'err 0.5 → α = 0', RO), 1.2)
    X1 = 470
    f.show(S(X1, 64, 'round', MU) + S(X1 + 66, 64, 'err', MU) + S(X1 + 140, 64, 'α', MU) + L(X1, 72, 712, 72, RULE, 1), 1.8)
    for k, rd in enumerate(RD3):
        t0 = 2.4 + k * 1.2; e, a = rd['err'], rd['a']; y = 94 + k * 26
        f.show(L(PX(e), PY(-.45), PX(e), PY(a), RO, 1.2, '3 3') + L(x0, PY(a), PX(e), PY(a), HL, 1.2, '3 3') +
               '<circle cx="%.1f" cy="%.1f" r="9" fill="none" stroke="%s" stroke-width="1.8"/>' % (PX(e), PY(a), HL),
               t0, hide=t0 + 1.2 if k < 2 else None)
        f.show(dot(PX(e), PY(a), HL, 4.5, BG), t0 + .2)
        f.show(T(X1 + 16, y, str(k + 1), TX, 'middle', mono=True, bold=True) + T(X1 + 66, y, '%.2f' % e, RO, 'start', mono=True) +
               T(X1 + 140, y, '%.2f' % a, HL, 'start', mono=True, bold=True), t0 + .3)
    f.show(S(X1, 196, 'fewer weighted mistakes', MU) + S(X1, 214, '→ a louder vote', HL, bold=True), 6.4)
    return finish(f, PY(-.45) + 44)

# ---------- 3.2 New weights ----------
def fig_weights():
    rd = RD3[0]; a = rd['a']
    up, dn = math.exp(a), math.exp(-a)
    assert round(up, 3) == 2.236 and round(dn, 3) == .447
    nw = RD3[1]['w']
    f = Anim('ada4-', 720, 0, 'Round 1 weights, 1/6 each. Five rows the stump got right are multiplied by e to the minus alpha, '
             '0.45; the wrong row E by e to the alpha, 2.24. The new weights sum to Z = 0.745; dividing by Z gives 0.10 for '
             'each right row and 0.50 for E: the wrong rows now hold exactly half the weight.',
             'RIGHT ROWS SHRINK · WRONG ROWS GROW · RESCALE TO SUM 1')
    t = Table(0, 44, [('id', 28), ('buy?', 46), ('h₁', 64, 'age ≥ 31.5')])
    f.static(t.head())
    for i, n in enumerate(IDS):
        f.static(t.row(i, [n, 'buy' if LAB[n] == 'buy' else 'no', ''], colors={1: CL[LAB[n]]}))
    C1, C2, C3, sc = 164, 370, 560, 260
    f.static(S(C1, 36, 'w', TX, bold=True) + S(C1, 54, 'round 1', MU))
    for i, n in enumerate(IDS): f.show(wbar(C1, t.ry(i), rd['w'][n], sc), .3 + i * .05)
    for i, n in enumerate(IDS): f.show(pt(t.cx(2), t.ry(i) + 13, 'buy' if rd['st'][3][n] > 0 else 'no', 5), 1.0)
    wi = IDS.index('E')
    f.show(t.outline(wi, wi, c=RO, sw=1.8), 1.6)
    f.show(M(C2, 36, '{w} · {e}<tspan dy="-6" font-size="10">−<tspan class="v">α y h</tspan></tspan>', TX, 'start') + S(C2, 54, 'α = %.2f' % a, HL), 2.2)
    for i, n in enumerate(IDS):
        ok = n not in rd['wrong']; t0 = 2.6 + (0 if ok else 1.0)
        f.show(arrow(C1 + 70, t.ry(i) + 13, C2 - 76, t.ry(i) + 13, RULE_HI, 1.1) +
               T(C2 - 40, t.ry(i) + 17, '× %.2f' % (dn if ok else up), MU if ok else RO, 'middle', mono=True, bold=not ok), t0)
        f.show(wbar(C2, t.ry(i), rd['raw'][n], sc, RO if not ok else VI), t0 + .3)
    yb = t.ry(6) + 14
    f.show(M(C2, yb, '{Z} = sum = %.3f' % rd['Z'], TX, 'start'), 4.4)
    f.show(S(C3, 36, 'new w', TX, bold=True) + S(C3, 54, '÷ Z', MU), 5.0)
    for i, n in enumerate(IDS): f.show(wbar(C3, t.ry(i), nw[n], sc, RO if n == 'E' else VI), 5.3 + i * .05)
    f.show(S(C3, yb, 'E holds 0.50 = half', RO, bold=True), 6.2)
    f.static(S(C1, yb, 'sum = 1', MU))
    return finish(f, yb + 12)

# ---------- 4.1 Adding up rounds ----------
XAGE = 45
def walk1(tree, age):
    thr = float(tree['q'].split(' < ')[1].rstrip(' ?')); ch = 'y' if age < thr else 'n'
    return ch, thr, tree['yes' if ch == 'y' else 'no']['leaf']

def fig_vote():
    f = Anim('ada5-', 720, 0, 'A new customer X, age 45, walks each of the three stumps. Stump 1, age under 31.5: no, so the buy '
             'leaf, vote +0.80. Stump 2, age under 56: yes, the no-buy leaf, vote −0.69. Stump 3, age under 46.5: yes, the '
             'buy leaf, vote +0.73. The three votes travel into one sum: F = +0.84. Its sign is positive, so X is predicted '
             'buy, even though one stump said no.', 'X WALKS EVERY STUMP · EACH LEAF SENDS ±α · THE SIGN OF THE SUM DECIDES')
    Y0, SX, SY = 66, 300, 268
    f.static(R(0, SY - 13, 170, 26, BG, VI, 6, 1.4) + T(85, SY + 4, 'new customer X · age 45', VI, bold=True))
    votes = []
    for k, rd in enumerate(RD3):
        tree = TREES[k]; x0 = 10 + k * 240
        pos = layout(tree, x0, x0 + 220, Y0, 70)
        f.static(draw_tree(tree, pos) + S(x0, Y0 + 4, 'stump %d' % (k + 1), MU, bold=True))
        ch, thr, lab = walk1(tree, XAGE); v = rd['a'] * (1 if lab == 'buy' else -1); votes.append(v)
        t0 = .8 + k * 2.0
        x, y = pos['']; q = tree['q']
        f.show(qring(x, y, q), t0)
        f.show(T(x, y - 20, '45 %s %g' % ('<' if ch == 'y' else '≥', thr), HL, mono=True, bold=True), t0 + .3)
        f.show(edge_hl(pos, '', ch) + lring(*pos[ch], lab), t0 + .8)
        lx, ly = pos[ch]; c = CL[lab]
        tgt = (SX - 76 + k * 76, SY)
        f.path(chip(lx, ly + 46, fmt(v), c, 58), [(0, 0, 0), (t0 + 1.5, tgt[0] - lx, tgt[1] - ly - 46)], t0 + 1.1, d=.9)
    F = sum(votes); assert round(F, 3) == round(F_age(XAGE), 3) == .845 and F > 0
    assert [round(v, 2) for v in votes] == [.8, -.69, .73]
    tS = 7.6
    f.static(R(SX - 118, SY - 26, 236, 52, 'none', RULE_HI, 8, 1.2, '4 3') + S(SX - 118, SY - 34, 'sum of the votes', MU))
    f.show(T(SX - 38, SY + 5, '+', TX, 'middle', 'sv-d', bold=True) + T(SX + 38, SY + 5, '+', TX, 'middle', 'sv-d', bold=True), tS - .4)
    f.show(arrow(SX + 122, SY, SX + 150, SY, TX, 1.4) + chip(SX + 200, SY, 'F = ' + fmt(F), FI, 96), tS)
    f.show(arrow(SX + 250, SY, SX + 290, SY, TX, 1.4) + S(SX + 270, SY - 16, 'sign', MU, 'middle'), tS + .6)
    f.show(pill(SX + 350, SY - 10, 'X → buy', 'bl'), tS + 1.0)
    f.static(legend(0, SY + 48))
    return finish(f, SY + 60)

# ---------- 4.2 Boundary ----------
def fig_boundary():
    f = Anim('ada6-', 720, 0, 'All three stumps cut on age. Each is a step of height alpha: stump 1 up at 31.5, stump 2 up at 56, '
             'stump 3 down at 46.5. Added, the score F against age is a staircase: below zero before 31.5, above it to 46.5, '
             'below it to 56, above it after. A new customer aged 45 lands at +0.84, buy.',
             'THREE STEPS ADD UP TO ONE STAIRCASE · ITS SIGN IS THE BOUNDARY')
    a0, a1, x0, x1 = 20, 66, 104, 600
    PX = lambda a: x0 + (a - a0) / (a1 - a0) * (x1 - x0)
    rows = [64, 118, 172]; ms = 15
    for k, rd in enumerate(RD3):
        y = rows[k]; c, thr, s = rd['st'][0], rd['st'][1], rd['st'][2]; a = rd['a']
        f.static(L(x0, y, x1, y, RULE, 1, '2 3') + M(x0 - 14, y + 5, '{α}%s{h}%s' % ('₁₂₃'[k], '₁₂₃'[k]), MU, 'end'))
        lo, hi = -s * a, s * a
        p = [(PX(a0), y - lo * ms), (PX(thr), y - lo * ms), (PX(thr), y - hi * ms), (PX(a1), y - hi * ms)]
        t0 = .4 + k * .8
        f.show(poly(p, HL, 2) + T(PX(a1) + 6, y - hi * ms + 4, fmt(hi), CL['buy' if hi > 0 else 'no'], 'start', mono=True) +
               T(PX(a0) + 2, y - lo * ms + (-6 if lo > 0 else 14), fmt(lo), CL['buy' if lo > 0 else 'no'], 'start', mono=True), t0)
    yz, my = 308, 62
    PY = lambda v: yz - v * my
    edges = [a0, 31.5, 46.5, 56, a1]
    vals = [F_age((u + v) / 2) for u, v in zip(edges, edges[1:])]
    assert [round(v, 2) for v in vals] == [-.76, .84, -.62, .76]
    for u, v, fv in zip(edges, edges[1:], vals):
        lab = 'buy' if fv > 0 else 'no'
        f.show(R(PX(u), PY(1.1), PX(v) - PX(u), PY(-1.1) - PY(1.1), tn(CL[lab], '.10'), 'none', 0), 3.6)
    for thr in (31.5, 46.5, 56):
        f.show(L(PX(thr), rows[0] - 16, PX(thr), PY(-1.1), HL, 1, '3 4'), 2.8)
        f.static(T(PX(thr), PY(-1.1) + 30, '%g' % thr, HL, mono=True))
    f.static(L(x0, yz, x1, yz, RULE_HI, 1.3) + M(x0 - 14, yz + 5, '{F}', TX, 'end'))
    f.static(L(x0, PY(-1.1), x1, PY(-1.1), RULE_HI, 1.3))
    for a in (30, 40, 50, 60): f.static(T(PX(a), PY(-1.1) + 15, str(a), FA, mono=True))
    f.static(S(x1, PY(-1.1) + 30, 'age', MU, 'end'))
    p = []
    for u, v, fv in zip(edges, edges[1:], vals): p += [(PX(u), PY(fv)), (PX(v), PY(fv))]
    f.show(poly(p, TX, 2.6), 3.0)
    for (u, v, fv) in zip(edges, edges[1:], vals):
        f.show(T((PX(u) + PX(v)) / 2, PY(fv) + (-8 if fv > 0 else 16), fmt(fv), CL['buy' if fv > 0 else 'no'], mono=True, bold=True), 3.4)
    for r in DATA:
        f.show(pt(PX(r[1]), yz, LAB[r[0]], 5.5) + T(PX(r[1]) + (9 if r[0] != 'E' else -9), yz + (16 if FX[r[0]] > 0 else -8),
                                                    r[0], MU, 'start' if r[0] != 'E' else 'end', bold=True), 4.2)
    X1 = 626
    f.show(dot(PX(45), PY(F_age(45)), VI, 6, BG) + L(PX(45), PY(F_age(45)) + 6, PX(45), yz - 6, VI, 1.2, '3 3'), 5.2)
    f.show(S(X1, 250, 'new customer X', VI, bold=True) + S(X1, 268, 'age 45', MU) + chip(X1 + 40, 292, 'F = ' + fmt(F_age(45)), VI, 86), 5.4)
    f.show(chip(X1 + 40, 324, 'X → buy', FI, 86), 5.9)
    f.static(legend(X1, PY(-1.1) + 30))
    return finish(f, PY(-1.1) + 42)

# ---------- 5.1 Rounds & learning rate ----------
def fig_rounds():
    f = Anim('ada7-', 720, 0, 'Error against the number of rounds, log scale, on 300 noisy points. With learning rate 1, training '
             'error keeps falling to %.1f%%; test error is lowest, %.1f%%, near round %d, then drifts up to %.0f%% by round %d. With '
             'learning rate 0.1 every vote is ten times smaller: the curve needs about %d rounds to reach %.0f%% and rises '
             'more slowly.' % (100 * C1[-1][1], 100 * B1[2], B1[0], 100 * C1[-1][2], N, B01[0], 100 * B01[2]),
             'MORE ROUNDS · TRAIN ERROR ↓ · TEST ERROR ↓ THEN SLOWLY ↑')
    x0, x1, yb, yt = 60, 540, 262, 50
    PX = lambda r: x0 + math.log10(r) / 3 * (x1 - x0)
    PY = lambda e: yb - e / .4 * (yb - yt)
    f.static(L(x0, yb, x1, yb, RULE_HI, 1.3) + L(x0, yb, x0, yt, RULE_HI, 1.3))
    for e in (.1, .2, .3, .4): f.static(T(x0 - 7, PY(e) + 4, '%d%%' % (e * 100), FA, 'end', mono=True) + L(x0, PY(e), x1, PY(e), RULE, .8))
    for r in (1, 10, 100, 1000): f.static(T(PX(r), yb + 15, str(r), FA, mono=True))
    f.static(S(x1, yb + 34, 'n_estimators (rounds)', MU, 'end') + S(x0, yt - 12, 'error', MU))
    keep = sorted(set(int(round(10 ** (i / 40))) for i in range(121)))
    def chunks(C, j, c, w, dash, t0, dt):
        pts = [(PX(r), PY(C[r - 1][j])) for r in keep]; n = 10
        for k in range(n):
            seg = pts[k * len(pts) // n: (k + 1) * len(pts) // n + 1]
            f.show(poly(seg, c, w, dash), t0 + k * dt)
    chunks(C1, 1, FI, 2, None, .4, .25)
    chunks(C1, 2, VI, 2.2, None, .4, .25)
    chunks(C01, 2, VI, 2, '5 4', 3.4, .25)
    top1 = min(PY(C1[r - 1][2]) for r in range(150, 450))
    f.show(S(PX(400), PY(C1[399][1]) + 18, 'train · rate 1', FI, 'middle', bold=True) +
           S(PX(260), top1 - 10, 'test · rate 1', VI, 'middle', bold=True), 3.0)
    f.show(S(PX(30), PY(C01[29][2]) - 10, 'test · rate 0.1', VI, 'middle'), 6.0)
    ring = '<circle cx="%.1f" cy="%.1f" r="9" fill="none" stroke="%s" stroke-width="2"/>'
    f.show(ring % (PX(B1[0]), PY(B1[2]), GR), 6.6)
    f.show(ring % (PX(N), PY(C1[-1][2]), RO), 7.0)
    X1 = 566
    f.show(S(X1, 66, 'rate 1', TX, bold=True) + S(X1, 84, 'best: round %d · %.1f%%' % (B1[0], 100 * B1[2]), GR) +
           S(X1, 102, 'round %d · %.0f%%' % (N, 100 * C1[-1][2]), RO), 6.8)
    f.show(S(X1, 142, 'rate 0.1', TX, bold=True) + S(X1, 160, 'best: round %d · %.0f%%' % (B01[0], 100 * B01[2]), GR) +
           S(X1, 178, 'round %d · %.1f%%' % (N, 100 * C01[-1][2]), MU), 7.4)
    return finish(f, yb + 46)

# ---------- 5.2 Label noise ----------
def fig_noise():
    f = Anim('ada8-', 720, 0, 'The 300 training points, %d of them with a flipped label. Round 1: every point weighs the same. '
             'After 100 rounds the dots are drawn by weight: the biggest ones are the flipped labels, and all ten heaviest '
             'rows are flipped. Their share of the total weight grows from 11 to 30 percent.' % NFLIP,
             'WRONG LABELS STAY WRONG · THEIR WEIGHT KEEPS GROWING')
    size, y0 = 200, 40
    def panel(x0, w, t0, title):
        f.static(R(x0, y0, size, size, BG, RULE_HI, 4, 1))
        s = ''
        for i, q in enumerate(TRF):
            x, y = x0 + q[0] * size, y0 + (1 - q[1]) * size
            r = 2.0 if w is None else max(1.0, 2.3 * math.sqrt(w[i] * 300))
            s += ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" fill-opacity=".85"/>' % (x, y, r, FI) if q[2] else
                  '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="1"/>' % (x, y, max(r - .4, .8), BR))
        f.show(s, t0)
        f.show(S(x0, y0 + size + 22, title, TX, bold=True), t0 + .2)
    panel(0, None, .3, 'round 1 · equal weights')
    rings = ''.join('<circle cx="%.1f" cy="%.1f" r="5" fill="none" stroke="%s" stroke-width="1.3"/>' %
                    (q[0] * size, y0 + (1 - q[1]) * size, RO) for q in TRF if q[3])
    f.show(rings, 1.2)
    f.show(S(0, y0 + size + 40, '%d rows with a flipped label' % NFLIP, RO), 1.4)
    panel(250, WK, 2.4, 'after 100 rounds · size = weight')
    f.show(''.join('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="1.6"/>' %
                   (250 + TRF[i][0] * size, y0 + (1 - TRF[i][1]) * size, 2.3 * math.sqrt(WK[i] * 300) + 3, RO) for i in HEAVY), 3.4)
    f.show(S(250, y0 + size + 40, 'the 10 heaviest: all flipped', RO), 3.6)
    X1 = 500
    f.show(S(X1, 56, 'weight on the flipped rows', MU, bold=True), 4.2)
    for k, (lab, v, c, t0) in enumerate((('round 1', SHARE0, MU, 4.4), ('round 100', SHARE, RO, 5.0))):
        y = 76 + k * 46
        f.show(S(X1, y + 12, lab, TX) + R(X1 + 70, y, 140, 16, SUNK, 'none', 3) +
               R(X1 + 70, y, max(v * 140 / .4, 1.5), 16, tn(RO, '.35'), RO, 3, 1.2) +
               T(X1 + 70 + v * 140 / .4 + 6, y + 13, '%.0f%%' % (v * 100), c, 'start', mono=True, bold=True), t0)
    f.show(S(X1, 198, 'every round they are still wrong,', MU) + S(X1, 216, 'so every round they grow', MU), 5.6)
    f.static(legend(X1, y0 + size + 22))
    return finish(f, y0 + size + 50)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Tree models</p>
  <h1>Ada<em>Boost</em></h1>
  <p class="lede">AdaBoost trains one-cut trees one after another, each aimed at the rows the previous ones got wrong, then lets them vote — the fewer a stump's mistakes, the louder its vote.</p>
</header>

<section id="ada-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Fit a stump, <em>make its mistakes heavier</em>, fit the next stump on the reweighted rows; at the end the stumps vote.</p>
{a1}
  <ul class="why">
    <li>The same six customers as <a href="../decision-tree/index.html">Decision tree</a>, with <span class="mth"><var>y</var> = +1</span> for buy and <span class="mth">−1</span> for no.</li>
    <li>A <b>stump</b> is a depth-1 tree, one question and two leaves: weak alone, each one wrong on 1–3 rows here.</li>
    <li>Row weights are the only thing passed from one round to the next.</li>
  </ul>
</section>

<section id="ada-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Stump</h2></div>
  <p class="key">Try every column × threshold; score each cut by the <em>total weight</em> of the rows it gets wrong.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">err</b></span><em>weighted error of the stump</em></span>
      <span class="op">=</span>
      <span class="t"><span>Σ<sub><var>i</var></sub> <var>w</var><sub><var>i</var></sub></span><em>row weights, sum 1</em></span>
      <span class="op">·</span>
      <span class="t r"><span>[ <var>h</var>(<var>x</var><sub><var>i</var></sub>) ≠ <var>y</var><sub><var>i</var></sub> ]</span><em>1 if the stump is wrong</em></span>
    </div>
  </div>
{a2}
  <ul class="why">
    <li>Same scan as a decision-tree split, but scored by weighted mistakes instead of Gini. Equal weights at the start, <span class="mth">1/<var>n</var></span>.</li>
    <li>The cut that was best in round 1 scores 0.50 in round 2: the weights force a <b>different</b> stump every round.</li>
  </ul>
</section>

<section id="ada-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Round update</h2></div>
  <p class="key">From the stump's err come two numbers: <em>its vote</em> and <em>the next round's weights</em>.</p>
  <div class="subsec" id="ada-s3-1">
    <h3 class="ssh"><b>3.1</b>Vote weight α</h3>
    <p class="skey">The fewer weighted mistakes, the <em>larger</em> the stump's vote; a coin flip gets none.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>α</var></span><em>vote of this stump</em></span>
      <span class="op">=</span>
      <span class="t b"><span>½ <b class="fn">ln</b> <span class="frac"><i>1 − err</i><i>err</i></span></span><em>odds of being right</em></span>
    </div>
  </div>
{a3}
    <ul class="why">
      <li>err must stay below 0.5; a stump with err 0 would get an infinite vote, which is why the learner must be weak.</li>
      <li>More than two classes: <b>SAMME</b> uses <span class="mth"><var>α</var> = <b class="fn">ln</b>((1 − err)/err) + <b class="fn">ln</b>(<var>K</var> − 1)</span>, so err only has to beat random guessing, <span class="mth">1 − 1/<var>K</var></span>; scikit-learn's <code>AdaBoostClassifier</code> uses it (for two classes it is the formula above times 2, same vote).</li>
    </ul>
  </div>
  <div class="subsec" id="ada-s3-2">
    <h3 class="ssh"><b>3.2</b>New weights</h3>
    <p class="skey">Wrong rows are multiplied by <em>e<sup>α</sup></em>, right rows by <em>e<sup>−α</sup></em>, then all are rescaled to sum 1.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>w</var><sub><var>i</var></sub></span><em>next round</em></span>
      <span class="op">←</span>
      <span class="t"><span><span class="frac"><i><var>w</var><sub><var>i</var></sub> · <var>e</var><sup>−<var>α</var> <var>y</var><sub><var>i</var></sub> <var>h</var>(<var>x</var><sub><var>i</var></sub>)</sup></i><i><var>Z</var></i></span></span><em>y·h = +1 right, −1 wrong</em></span>
    </div>
  </div>
{a4}
    <ul class="why">
      <li><span class="mth"><var>Z</var></span> is just the sum that brings the weights back to 1.</li>
      <li>After every update the wrong rows hold <b>exactly half</b> the weight, so the last stump is now a coin flip.</li>
      <li>These two rules are what minimising the exponential loss <span class="mth">Σ <var>e</var><sup>−<var>y</var><var>F</var></sup></span> gives — the bridge to <a href="../gradient-boosting/index.html">Gradient boosting</a>.</li>
    </ul>
  </div>
</section>

<section id="ada-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Weighted vote</h2></div>
  <p class="key">The model is the <em>sum of the signed votes</em> <span class="mth"><var>α</var><sub><var>t</var></sub> <var>h</var><sub><var>t</var></sub></span>; its sign is the answer.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>F</var>(<var>x</var>)</span><em>score</em></span>
      <span class="op">=</span>
      <span class="t b"><span>Σ<sub><var>t</var></sub> <var>α</var><sub><var>t</var></sub> <var>h</var><sub><var>t</var></sub>(<var>x</var>)</span><em>each stump votes ±α</em></span>
      <span class="op">,</span>
      <span class="t"><span><var>ŷ</var> = <b class="fn">sign</b> <var>F</var>(<var>x</var>)</span><em>buy if positive</em></span>
    </div>
  </div>
  <div class="subsec" id="ada-s4-1">
    <h3 class="ssh"><b>4.1</b>Adding up rounds</h3>
    <p class="skey">Stumps that are each wrong somewhere are <em>right together</em>, because they are wrong in different places.</p>
{a5}
    <ul class="why">
      <li>Each stump alone is wrong on 1–3 of the six rows; the vote of the three is wrong on none, because they are wrong in different places.</li>
      <li><code>decision_function</code> returns <span class="mth"><var>F</var></span>; <code>predict_proba</code> squashes it into a share.</li>
    </ul>
  </div>
  <div class="subsec" id="ada-s4-2">
    <h3 class="ssh"><b>4.2</b>Boundary</h3>
    <p class="skey">Every stump is one step; their sum is a <em>staircase</em>, and its zero crossings are the boundary.</p>
{a6}
    <ul class="why">
      <li>Three stumps on one column give a boundary that no single stump can draw: buy, no, buy along age.</li>
      <li>Stumps on different columns add up to axis-parallel blocks on the plane, like a tree but softer at the edges.</li>
    </ul>
  </div>
</section>

<section id="ada-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Reining it in</h2></div>
  <p class="key">Every round makes the training rows fit better; what to watch is <em>how many rounds</em> and <em>what they chase</em>.</p>
  <div class="subsec" id="ada-s5-1">
    <h3 class="ssh"><b>5.1</b>Rounds &amp; learning rate</h3>
    <p class="skey">Test error falls, flattens, then <em>creeps back up</em>; a smaller learning rate slows the whole curve.</p>
{a7}
    <ul class="why">
      <li><code>n_estimators</code> (default 50) is the number of rounds; <code>learning_rate</code> multiplies every <span class="mth"><var>α</var></span>.</li>
      <li>Lower the rate, raise the rounds, and pick the pair by cross-validation; <code>staged_predict</code> scores every round in one pass.</li>
    </ul>
  </div>
  <div class="subsec" id="ada-s5-2">
    <h3 class="ssh"><b>5.2</b>Label noise</h3>
    <p class="skey">A row with a wrong label is <em>wrong every round</em>, so its weight only grows.</p>
{a8}
    <ul class="why">
      <li>Exponential loss punishes a confident mistake without limit: the model spends its rounds on broken rows.</li>
      <li>With noisy labels prefer <a href="../random-forest/index.html">Random forest</a> or gradient boosting with a gentler loss.</li>
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

<footer>Machine learning · Tree models · next lesson in the branch: <a href="../gradient-boosting/index.html">Gradient boosting</a>.</footer>
'''

def build():
    figs = dict(a1=fig_mental(), a2=fig_stump(), a3=fig_alpha(), a4=fig_weights(), a5=fig_vote(), a6=fig_boundary(),
                a7=fig_rounds(), a8=fig_noise())
    return re.sub(r'\{(a\d+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'Stumps trained one after another: each round makes the rows predicted wrong heavier, scores the '
           'stump with α from its weighted error, and the stumps take a weighted vote.')
