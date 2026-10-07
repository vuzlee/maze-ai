# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/09-evaluation/roc-auc-pr.
One predictions table of ten rows (id, true label, score), sorted by score. The threshold steps down one row at a
time; every number drawn (confusion-matrix counts, TPR/FPR, precision/recall, AUC, AP, pair counts) is computed
here and pinned with assert. The rare-positive table repeats every negative ten times with a fixed jitter.
Run: python3 roc_auc_pr.py"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, finish)
from tablefig import GR, tint, pill
from decision_tree import splice, BODY as DT_BODY
import linear_algebra as _la
_la.RGBA.setdefault(GR, '--green-a')

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/09-evaluation/roc-auc-pr/index.html')
SCRIPT = DT_BODY[DT_BODY.index('<script>'):DT_BODY.index('</script>') + len('</script>')]

# ---------- the predictions table ----------
ROWS = [('A', 1, .95), ('B', 1, .88), ('C', 0, .80), ('D', 1, .72), ('E', 0, .64),
        ('F', 1, .55), ('G', 0, .47), ('H', 0, .38), ('I', 0, .26), ('J', 0, .12)]
assert ROWS == sorted(ROWS, key=lambda r: -r[2])
NP = sum(r[1] for r in ROWS); NN = len(ROWS) - NP; assert (NP, NN) == (4, 6)
PC, NC = FI, BR          # positive = data blue, negative = neutral brand surface
LBL = lambda y: '1' if y else '0'

def sweep(rows):
    """threshold just below row k-1 for k = 0..n: (TP, FP, FN, TN) per step"""
    P = sum(r[1] for r in rows); N = len(rows) - P; out = [(0, 0, P, N)]; tp = fp = 0
    for r in rows:
        tp += r[1]; fp += 1 - r[1]; out.append((tp, fp, P - tp, N - fp))
    return out
SW = sweep(ROWS)
ROC = [(fp / NN, tp / NP) for tp, fp, _, _ in SW]
PR = [(tp / NP, tp / (tp + fp)) for tp, fp, _, _ in SW[1:]]
assert SW[5] == (3, 2, 1, 4) and SW[-1] == (4, 6, 0, 0)

def auc(rows):
    pts = [(fp, tp) for tp, fp, _, _ in sweep(rows)]; P = pts[-1][1]; N = pts[-1][0]
    return sum((b[0] - a[0]) * (a[1] + b[1]) / 2 for a, b in zip(pts, pts[1:])) / P / N
def pairs(rows):
    pos = [r for r in rows if r[1]]; neg = [r for r in rows if not r[1]]
    return sum(p[2] > n[2] for p in pos for n in neg), len(pos) * len(neg)
def ap(rows):
    P = sum(r[1] for r in rows); tp = 0; s = 0
    for k, r in enumerate(rows, 1):
        if r[1]: tp += 1; s += tp / k / P
    return s
AUC = auc(ROWS); GOOD, ALL = pairs(ROWS)
assert (GOOD, ALL) == (21, 24) and abs(AUC - 21 / 24) < 1e-12 and AUC == .875
AP = ap(ROWS); PREC_AT_P = [SW[i + 1][0] / (i + 1) for i, r in enumerate(ROWS) if r[1]]
assert [round(p, 3) for p in PREC_AT_P] == [1, 1, .75, .667] and round(AP, 3) == .854
# positives above each negative = the column heights of the ROC area
ABOVE = [sum(1 for p in ROWS if p[1] and p[2] > n[2]) for n in ROWS if not n[1]]
assert ABOVE == [2, 3, 4, 4, 4, 4] and sum(ABOVE) == GOOD

# rare positives: the same model, every negative ten times (fixed jitter keeps the ordering)
RARE = sorted([r for r in ROWS if r[1]] + [(r[0] + str(k), 0, round(r[2] + (k - 4.5) * .007, 4))
                                           for r in ROWS if not r[1] for k in range(10)], key=lambda r: -r[2])
assert len(RARE) == 64 and sum(r[1] for r in RARE) == 4
RAUC, RAP = auc(RARE), ap(RARE)
assert abs(RAUC - AUC) < 1e-12 and round(RAP, 3) == .599
RSW = sweep(RARE); RN = 60
RROC = [(fp / RN, tp / NP) for tp, fp, _, _ in RSW]
RPR = [(tp / NP, tp / (tp + fp)) for tp, fp, _, _ in RSW[1:]]
K6 = [i for i, r in enumerate(RARE) if r[0] == 'F'][0] + 1          # threshold 0.60 in the rare table
assert RSW[K6 - 1] == (3, 20, 1, 40) and RSW[K6 - 1][1] / RN == SW[5][1] / NN
f2 = lambda v: ('%.2f' % v)

# ---------- shared drawing ----------
TB = lambda: Table(50, 30, [('id', 30), ('y', 34), ('score', 54)], step=28, rh=24)
def trow(t, i):
    r = ROWS[i]; c = PC if r[1] else NC
    return t.row(i, [r[0], LBL(r[1]), '%.2f' % r[2]], colors={1: c})
def tline(t, k):
    """y of the threshold line just below row k-1 (k = 0: above every row)"""
    return t.ry(k) - 2
def thr(k):
    if k == 0: return 1.0
    if k == len(ROWS): return 0.0
    return (ROWS[k - 1][2] + ROWS[k][2]) / 2
def tbar(t, k, c=VI):
    y = tline(t, k)
    return (L(t.x - 4, y, t.x + t.w + 4, y, c, 1.8, '5 3') + R(0, y - 9, 44, 18, BG, c, 4, 1.2) +
            T(22, y + 4, 't %.2f' % (thr(k) + 1e-9), c, mono=True, bold=True))
def tok(x, y, rid, y1):
    c = PC if y1 else NC
    return R(x, y, 18, 16, BG, 'none', 3) + R(x, y, 18, 16, tn(c, '.20' if y1 else '.10'), c, 3, 1.2) + \
        T(x + 9, y + 12, rid, c, mono=True, bold=True)

class Mat:
    """2x2 confusion matrix: columns predicted +/-, rows true 1/0"""
    def __init__(s, x, y, w=112, h=58):
        s.x, s.y, s.w, s.h = x, y, w, h
    def cell(s, r, c): return s.x + c * s.w, s.y + s.h * r
    def frame(s):
        o = T(s.x + s.w / 2, s.y - 8, 'predicted +', MU) + T(s.x + 1.5 * s.w, s.y - 8, 'predicted −', MU)
        o += T(s.x - 8, s.y + s.h / 2 + 4, 'y = 1', PC, 'end', bold=True) + T(s.x - 8, s.y + 1.5 * s.h + 4, 'y = 0', NC, 'end', bold=True)
        for r in range(2):
            for c in range(2):
                x, y = s.cell(r, c); o += R(x, y, s.w, s.h, BG, RULE_HI, 4, 1)
        return o
    def slot(s, r, c, n):
        x, y = s.cell(r, c); return x + 6 + (n % 5) * 21, y + 20 + (n // 5) * 18
    def counts(s, q):
        tp, fp, fn, tn_ = q; o = ''
        for (r, c), name, v in (((0, 0), 'TP', tp), ((0, 1), 'FN', fn), ((1, 0), 'FP', fp), ((1, 1), 'TN', tn_)):
            x, y = s.cell(r, c)
            o += R(x + 3, y + 3, 60, 14, BG, 'none', 2) + T(x + 6, y + 14, '%s %d' % (name, v), TX, 'start', mono=True, bold=True)
        return o

class Plot:
    def __init__(s, x, y, size, xl, yl, title):
        s.x, s.y, s.S, s.xl, s.yl, s.title = x, y, size, xl, yl, title
    def __call__(s, a, b): return s.x + a * s.S, s.y + s.S - b * s.S
    def frame(s, diag=False):
        o = R(s.x, s.y, s.S, s.S, BG, RULE_HI, 2, 1)
        for v in (.25, .5, .75):
            o += L(s.x + v * s.S, s.y, s.x + v * s.S, s.y + s.S, RULE, 1) + L(s.x, s.y + v * s.S, s.x + s.S, s.y + v * s.S, RULE, 1)
        for v in (0, .5, 1):
            o += T(s.x + v * s.S, s.y + s.S + 14, '%g' % v, FA, cls='sv-d') + T(s.x - 6, s.y + s.S - v * s.S + 4, '%g' % v, FA, 'end', 'sv-d')
        o += T(s.x + s.S / 2, s.y + s.S + 30, s.xl, MU) + T(s.x, s.y - 8, s.yl, MU, 'start')
        o += T(s.x + s.S, s.y - 8, s.title, TX, 'end', bold=True)
        if diag: o += L(s.x, s.y + s.S, s.x + s.S, s.y, FA, 1.2, '4 4') + T(s.x + s.S * .62, s.y + s.S * .45, 'random', FA, 'start', 'sv-d')
        return o
    def base(s, v, txt):
        x0, y = s(0, v); x1, _ = s(1, v)
        return L(x0, y, x1, y, RO, 1.4, '5 3') + T(x0 + 6, y - 5, txt, RO, 'start', 'sv-d', bold=True)

# ---------- 01 Mental model: one threshold -> one matrix -> one point ----------
def fig_mental():
    K = 5
    f = Anim('roc1-', 720, 0, 'A table of ten predictions A to J, sorted by score, with the true label y. A threshold line at 0.60 '
             'sits under row E: the five rows above it are predicted positive. Each row in turn slides into the '
             'confusion matrix cell it belongs to: A, B and D into TP, C and E into FP, F into FN, G to J into TN. From the '
             'cells, TPR is 3 of 4 = 0.75 and FPR is 2 of 6 = 0.33, and that pair becomes one point on the ROC plane.',
             'ONE THRESHOLD → ONE CONFUSION MATRIX → ONE POINT')
    t = TB(); f.static(t.head())
    for i in range(10): f.static(trow(t, i))
    f.show(tbar(t, K), .4)
    f.show(t.outline(0, K - 1, c=VI, sw=1.4, dash='4 3'), .8)
    m = Mat(222, 70); f.show(m.frame(), .2)
    n = {}
    for i, (rid, y1, s) in enumerate(ROWS):
        r, c = (0 if y1 else 1), (0 if i < K else 1)
        k = n.get((r, c), 0); n[(r, c)] = k + 1
        sx, sy = m.slot(r, c, k); x0, y0 = t.colx(0) + 6, t.ry(i) + 4
        t0 = 1.3 + i * .35
        f.path(tok(sx, sy, rid, y1), [(0, x0 - sx, y0 - sy), (t0, 0, 0)], t0 - .25, d=.55)
    f.show(m.counts(SW[K]), 5.0)
    tp, fp, fn, tn_ = SW[K]; assert (tp, fp) == (3, 2)
    f.show(chip(m.x + m.w, 214, 'TPR = TP / 4 = 3/4 = %s' % f2(tp / NP), PC, 220), 5.6)
    f.show(chip(m.x + m.w, 244, 'FPR = FP / 6 = 2/6 = %s' % f2(fp / NN), NC, 220), 6.0)
    p = Plot(500, 50, 200, 'FPR', 'TPR', 'ROC plane'); f.show(p.frame(diag=True), .2)
    px, py = p(fp / NN, tp / NP)
    f.path(dot(px, py, VI, 6, BG) + T(px + 10, py + 16, '(%s, %s)' % (f2(fp / NN), f2(tp / NP)), VI, 'start', mono=True, bold=True),
           [(0, m.x + m.w + 110 - px, 230 - py), (6.8, 0, 0)], 6.5, d=.8)
    return finish(f, 330)

# ---------- 02 Sweep: ROC and PR, one function ----------
def fig_sweep(kind):
    roc = kind == 'roc'; pre = 'roc2-' if roc else 'roc3-'
    pts = ROC if roc else [None] + PR
    aria = ('The threshold line starts above row A and steps down one row at a time. Each step one token moves from the '
            'predicted-minus column of the confusion matrix to the predicted-plus column, the counts update, and the ')
    aria += ('pair FPR, TPR becomes one point on the ROC plane, joined to the previous one; ten steps trace the curve from '
             '(0, 0) to (1, 1).' if roc else
             'pair recall, precision becomes one point on the PR plane, joined to the previous one; precision falls toward '
             'the dashed baseline at 0.40, the share of positives.')
    f = Anim(pre, 720, 0, aria, 'THRESHOLD STEPS DOWN ONE ROW · ONE MATRIX · ONE %s POINT PER STEP' % ('ROC' if roc else 'PR'))
    t = TB(); f.static(t.head())
    for i in range(10): f.static(trow(t, i))
    m = Mat(222, 70); f.static(m.frame())
    p = Plot(500, 50, 200, 'FPR' if roc else 'recall', 'TPR' if roc else 'precision', 'ROC curve' if roc else 'PR curve')
    f.static(p.frame(diag=roc))
    if not roc: f.static(p.base(NP / len(ROWS), 'positive rate 0.40'))
    DT = 1.15; T0 = .8
    # threshold line: final spot = below every row
    yk = [tline(t, k) for k in range(11)]
    f.path(L(t.x - 4, yk[10], t.x + t.w + 4, yk[10], VI, 1.8, '5 3'),
           [(0, 0, yk[0] - yk[10])] + [(T0 + k * DT, 0, yk[k] - yk[10]) for k in range(1, 11)], .2, d=.45)
    for k in range(11):
        y = yk[k]; tk = .2 if k == 0 else T0 + k * DT + .45
        f.show(R(0, y - 9, 44, 18, BG, VI, 4, 1.2) + T(22, y + 4, 't %.2f' % (thr(k) + 1e-9), VI, mono=True, bold=True),
               tk, hide=None if k == 10 else T0 + (k + 1) * DT, d=.2)
    # tokens: start in the predicted-minus column, slide to predicted-plus when the line passes their row
    seen = {0: 0, 1: 0}; arr = {0: 0, 1: 0}
    for i, (rid, y1, s) in enumerate(ROWS):
        r = 0 if y1 else 1
        x0, y0 = m.slot(r, 1, seen[r]); seen[r] += 1
        x1, y1_ = m.slot(r, 0, arr[r]); arr[r] += 1
        f.path(tok(x1, y1_, rid, y1), [(0, x0 - x1, y0 - y1_), (T0 + (i + 1) * DT + .1, 0, 0)], .3, d=.5)
    for k in range(11):
        tk = .3 if k == 0 else T0 + k * DT + .5
        nxt = None if k == 10 else T0 + (k + 1) * DT + .5
        f.show(m.counts(SW[k]), tk, hide=nxt, d=.2)
        tp, fp = SW[k][0], SW[k][1]
        if roc: a, b = 'TPR %d/4 = %s' % (tp, f2(tp / NP)), 'FPR %d/6 = %s' % (fp, f2(fp / NN))
        elif k: a, b = 'recall %d/4 = %s' % (tp, f2(tp / NP)), 'precision %d/%d = %s' % (tp, tp + fp, f2(tp / (tp + fp)))
        else: a, b = 'recall 0/4 = 0.00', 'precision 0/0 · no point'
        f.show(chip(m.x + m.w, 214, a, PC, 220) + chip(m.x + m.w, 244, b, NC if roc else VI, 220), tk, hide=nxt, d=.2)
        if pts[k] is None: continue
        px, py = p(*pts[k])
        if k and pts[k - 1] is not None:
            f.show(L(*p(*pts[k - 1]), px, py, VI, 2.4), tk + .55)
        f.show(dot(px, py, VI, 3.6), tk + .3)
    if roc: f.show(chip(p.x + p.S / 2, p.y + p.S + 52, 'AUC = %.3f' % AUC, VI, 110), T0 + 11 * DT)
    else: f.show(chip(p.x + p.S / 2, p.y + p.S + 52, 'AP = %.3f' % AP, VI, 110), T0 + 11 * DT)
    return finish(f, 360)

# ---------- 3.1 AUC as area / 3.3 AP as area: same walk down the table ----------
def fig_area(kind):
    roc = kind == 'roc'; pre = 'roc4-' if roc else 'roc6-'
    aria = ('Walking down the table: a positive row moves the ROC curve up by 1/4, a negative row moves it right by 1/6 and '
            'shades a column whose height is the number of positives already passed. Columns of 2, 3, 4, 4, 4 and 4 '
            'quarters add up to 21 of 24 cells, AUC 0.875.' if roc else
            'Walking down the table: every row adds a PR point; at each positive row recall moves right by 1/4 and a bar '
            'of that width is shaded at the precision there: 1, 1, 0.75 and 0.67. Their average is AP 0.854.')
    f = Anim(pre, 720, 0, aria, 'WALK THE ROWS · EACH %s ADDS ONE SHADED STRIP' % ('NEGATIVE' if roc else 'POSITIVE'))
    t = TB(); f.static(t.head())
    for i in range(10): f.static(trow(t, i))
    p = Plot(330, 50, 240, 'FPR' if roc else 'recall', 'TPR' if roc else 'precision', 'ROC-AUC' if roc else 'average precision')
    f.static(p.frame(diag=roc))
    if not roc: f.static(p.base(.4, 'baseline 0.40'))
    DT = .9; tp = fp = 0; terms = []
    prev = (0, 0) if roc else None
    for i, (rid, y1, s) in enumerate(ROWS):
        t0 = .6 + i * DT
        f.show(t.outline(i, c=VI, sw=1.6), t0, hide=t0 + DT, d=.2)
        tp += y1; fp += 1 - y1
        if roc:
            cur = (fp / NN, tp / NP)
            if not y1:
                x0, _ = p(prev[0], 0); x1, yb = p(cur[0], 0); _, ytop = p(0, cur[1])
                f.show(R(x0, ytop, x1 - x0, yb - ytop, tn(VI, '.18'), 'none', 0) +
                       T((x0 + x1) / 2, yb - 6, str(ABOVE[fp - 1]), VI, mono=True, bold=True), t0 + .35)
                f.show(T(t.x + t.w + 8, t.ry(i) + 16, '%d P above' % ABOVE[fp - 1], VI, 'start', mono=True, bold=True), t0 + .2)
                terms.append(ABOVE[fp - 1])
        else:
            cur = (tp / NP, tp / (tp + fp))
            if y1:
                x0, yb = p(cur[0] - .25, 0); x1, ytop = p(cur[0], cur[1])
                f.show(R(x0, ytop, x1 - x0, yb - ytop, tn(VI, '.18'), 'none', 0) +
                       T((x0 + x1) / 2, yb - 6, f2(cur[1]), VI, mono=True, bold=True), t0 + .35)
                f.show(T(t.x + t.w + 8, t.ry(i) + 16, 'P = %d/%d' % (tp, tp + fp), VI, 'start', mono=True, bold=True), t0 + .2)
                terms.append(cur[1])
        if prev is not None: f.show(L(*p(*prev), *p(*cur), VI, 2.4), t0 + .3)
        f.show(dot(*p(*cur), VI, 3.4), t0 + .3)
        prev = cur
    te = .6 + 10 * DT + .3
    if roc:
        assert terms == ABOVE
        f.show(M(p.x + p.S + 20, 140, '(2+3+4+4+4+4) / 24', TX, 'start'), te)
        f.show(M(p.x + p.S + 20, 166, '= 21/24 = 0.875', VI, 'start'), te + .4)
        f.show(S(p.x + p.S + 20, 192, 'cells under the curve', MU), te + .4)
    else:
        assert [round(v, 4) for v in terms] == [round(v, 4) for v in PREC_AT_P]
        f.show(M(p.x + p.S + 20, 140, '(1 + 1 + 0.75 + 0.67) / 4', TX, 'start'), te)
        f.show(M(p.x + p.S + 20, 166, '= %.3f' % AP, VI, 'start'), te + .4)
        f.show(S(p.x + p.S + 20, 192, 'strip width 1/4 each', MU), te + .4)
    return finish(f, 340)

# ---------- 3.2 AUC as ranking: every positive vs every negative ----------
def fig_pairs():
    f = Anim('roc5-', 720, 0, 'The four positives A, B, D, F form the rows of a grid and the six negatives C, E, G, H, I, J its '
             'columns, each with its score. Column by column every cell is filled: green when the positive scores above '
             'the negative, red when not. Only B and A lose to nobody; C beats D and F, E beats F. 21 of 24 cells are '
             'green: 21/24 = 0.875, the same number as the area.', 'PICK ONE POSITIVE AND ONE NEGATIVE · IS THE POSITIVE SCORED HIGHER?')
    pos = [r for r in ROWS if r[1]]; neg = [r for r in ROWS if not r[1]]
    X0, Y0, CW, CH = 120, 74, 62, 40
    f.static(T(X0 + 3 * CW, 40, 'negatives (y = 0)', NC, bold=True) + T(X0 - 70, Y0 - 12, 'positives', PC, 'start', bold=True))
    for j, n in enumerate(neg):
        f.static(T(X0 + j * CW + CW / 2, Y0 - 12, '%s %.2f' % (n[0], n[2]), NC, mono=True, bold=True))
    for i, q in enumerate(pos):
        f.static(T(X0 - 10, Y0 + i * CH + CH / 2 + 4, '%s %.2f' % (q[0], q[2]), PC, 'end', mono=True, bold=True))
        for j in range(6): f.static(R(X0 + j * CW, Y0 + i * CH, CW, CH, BG, RULE_HI, 3, 1))
    good = 0
    for j, n in enumerate(neg):
        t0 = .6 + j * 1.1
        f.show(R(X0 + j * CW - 2, Y0 - 28, CW + 4, 4 * CH + 32, 'none', VI, 5, 1.6), t0, hide=t0 + 1.1, d=.2)
        for i, q in enumerate(pos):
            ok = q[2] > n[2]; good += ok; c = GR if ok else RO
            x, y = X0 + j * CW, Y0 + i * CH
            f.show(R(x + 4, y + 4, CW - 8, CH - 8, tn(c, '.16'), c, 4, 1.2) +
                   T(x + CW / 2, y + CH / 2 + 4, '>' if ok else '&lt;', c, mono=True, bold=True), t0 + .15 + i * .15)
        f.show(T(X0 + j * CW + CW / 2, Y0 + 4 * CH + 18, '%d' % sum(q[2] > n[2] for q in pos), VI, mono=True, bold=True), t0 + .8)
    assert good == GOOD == 21
    te = .6 + 6 * 1.1 + .3
    f.show(M(X0 + 6 * CW + 30, Y0 + 50, 'green pairs / all pairs', TX, 'start'), te)
    f.show(M(X0 + 6 * CW + 30, Y0 + 78, '= 21 / 24 = 0.875 = AUC', VI, 'start'), te + .4)
    f.show(S(X0 + 6 * CW + 30, Y0 + 104, 'column sums 2 3 4 4 4 4 =', MU) +
           S(X0 + 6 * CW + 30, Y0 + 122, 'the strips of the area figure', MU), te + .8)
    return finish(f, Y0 + 4 * CH + 34)

# ---------- 04 Rare positives ----------
def fig_rare():
    f = Anim('roc7-', 720, 0, 'The ten-row table is shown, then every negative row is copied ten times, giving 4 positives '
             'and 60 negatives with the same ordering. At threshold 0.60 the small table has FP 2 of 6 and the large one '
             'FP 20 of 60: FPR is 0.33 in both, but precision drops from 3 of 5 to 3 of 23. The ROC curves of the two '
             'tables lie exactly on top of each other, AUC 0.875 both. The PR curve of the large table falls well below '
             'the small one, AP 0.854 down to 0.599, and its baseline drops from 0.40 to 0.06.',
             'SAME MODEL · TEN TIMES MORE NEGATIVES · ROC STAYS · PR DROPS')
    t = TB(); f.static(t.head())
    for i in range(10): f.static(trow(t, i))
    for i, r in enumerate(ROWS):
        if not r[1]:
            f.show(chip(t.x + t.w + 26, t.ry(i) + 12, '×10', NC, 40), .5 + i * .12)
    f.show(T(t.x, t.ry(9) + 44, '4 positives · 6 → 60 negatives', TX, 'start', bold=True), 1.9)
    f.show(T(t.x, t.ry(9) + 62, 't 0.60: FP 2 → 20', NC, 'start', mono=True), 2.3)
    f.show(T(t.x, t.ry(9) + 78, 'FPR 2/6 = 20/60 = 0.33', NC, 'start', mono=True), 2.6)
    f.show(T(t.x, t.ry(9) + 94, 'precision 3/5 → 3/23', RO, 'start', mono=True, bold=True), 2.9)
    assert round(3 / 23, 2) == .13
    a = Plot(270, 50, 190, 'FPR', 'TPR', 'ROC'); b = Plot(520, 50, 190, 'recall', 'precision', 'PR')
    f.static(a.frame(diag=True) + b.frame())
    f.static(b.base(.4, '0.40'))
    f.show(b.base(4 / 64, '0.06'), 6.0)
    f.static(poly([a(*q) for q in ROC], FA, 2.2, '5 3') + poly([b(*q) for q in PR], FA, 2.2, '5 3'))
    # the 64-row curves traced in eight chunks
    ch = 8; T0 = 3.4
    for k in range(ch):
        i0, i1 = len(RROC) * k // ch, len(RROC) * (k + 1) // ch
        f.show(poly([a(*q) for q in RROC[max(i0 - 1, 0):i1 + 1]], VI, 2.4), T0 + k * .35, d=.25)
        j0, j1 = len(RPR) * k // ch, len(RPR) * (k + 1) // ch
        f.show(poly([b(*q) for q in RPR[max(j0 - 1, 0):j1 + 1]], VI, 2.4), T0 + k * .35, d=.25)
    te = T0 + ch * .35 + .4
    f.show(chip(a.x + a.S / 2, a.y + a.S + 52, 'AUC 0.875 → 0.875', VI, 150), te)
    f.show(chip(b.x + b.S / 2, b.y + b.S + 52, 'AP %.3f → %.3f' % (AP, RAP), RO, 150), te + .3)
    f.static(L(270, 330, 290, 330, FA, 2.2, '5 3') + S(296, 334, '10 rows', MU) + L(370, 330, 390, 330, VI, 2.4) + S(396, 334, '64 rows', MU))
    return finish(f, 342)

EQ_ROC = '''  <div class="eq">
    <div class="line">
      <span class="t g"><span><b class="fn">TPR</b> = <span class="frac"><i>TP</i><i>TP + FN</i></span></span><em>share of positives caught</em></span>
      <span class="op">,</span>
      <span class="t b"><span><b class="fn">FPR</b> = <span class="frac"><i>FP</i><i>FP + TN</i></span></span><em>share of negatives flagged</em></span>
    </div>
  </div>'''
EQ_PR = '''  <div class="eq">
    <div class="line">
      <span class="t g"><span><b class="fn">recall</b> = <span class="frac"><i>TP</i><i>TP + FN</i></span></span><em>same as TPR</em></span>
      <span class="op">,</span>
      <span class="t p"><span><b class="fn">precision</b> = <span class="frac"><i>TP</i><i>TP + FP</i></span></span><em>share of flags that are right</em></span>
    </div>
  </div>'''
EQ_AP = '''  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">AP</b></span><em>average precision</em></span>
      <span class="op">=</span>
      <span class="t g"><span>Σ<sub><var>k</var></sub> (<var>R</var><sub><var>k</var></sub> − <var>R</var><sub><var>k</var>−1</sub>)</span><em>recall step, 1/4 at each positive</em></span>
      <span class="op">·</span>
      <span class="t p"><span><var>P</var><sub><var>k</var></sub></span><em>precision at that row</em></span>
    </div>
  </div>'''

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Model evaluation</p>
  <h1>ROC-AUC &amp; PR <em>curve</em></h1>
  <p class="lede">Slide the threshold down a table of scores one row at a time, turn every confusion matrix into one point, and the points trace two curves that judge the ranking without fixing a threshold.</p>
</header>

<section id="roc-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">A model gives <em>scores</em>; a threshold turns them into one confusion matrix, and the matrix into one point.</p>
{r1}
  <ul class="why">
    <li>Ten predictions, sorted by score: four true positives (<span class="mth"><var>y</var> = 1</span>), six negatives. The same table drives every figure below.</li>
    <li>Rows above the line are predicted positive. Lower the line and more rows cross it: one matrix, one point per position — counts and rates as in <a href="../metrics-confusion-matrix/index.html">Metric &amp; confusion matrix</a>.</li>
    <li>The curves judge the <b>ranking</b> only; picking the threshold is still a cost decision, and trusting the scores as probabilities is <a href="../calibration/index.html">Probability calibration</a>.</li>
  </ul>
</section>

<section id="roc-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Threshold sweep</h2></div>
  <p class="key">Step the threshold down one row at a time; each step moves <em>one row</em> into the predicted-positive column.</p>
  <div class="subsec" id="roc-s2-1">
    <h3 class="ssh"><b>2.1</b>ROC curve</h3>
    <p class="skey">Plot <em>TPR against FPR</em>: a positive row steps the curve up, a negative row steps it right.</p>
''' + EQ_ROC + '''
{r2}
    <ul class="why">
      <li>Both rates divide within one class: TPR by the 4 positives, FPR by the 6 negatives.</li>
      <li>The diagonal is a random ranking; a perfect one goes straight up to (0, 1) first.</li>
    </ul>
  </div>
  <div class="subsec" id="roc-s2-2">
    <h3 class="ssh"><b>2.2</b>PR curve</h3>
    <p class="skey">Plot <em>precision against recall</em> from the same steps: a negative row only pulls precision down.</p>
''' + EQ_PR + '''
{r3}
    <ul class="why">
      <li>At the first step there is no point: nothing is flagged yet, so precision is 0/0.</li>
      <li>The <b>baseline is the positive rate</b>, here 4/10 = 0.40 — flag everything and precision equals it. It is not 0.5.</li>
    </ul>
  </div>
</section>

<section id="roc-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Area under the curve</h2></div>
  <p class="key">Each curve shrinks to <em>one number</em>: the area under it.</p>
  <div class="subsec" id="roc-s3-1">
    <h3 class="ssh"><b>3.1</b>ROC-AUC as area</h3>
    <p class="skey">Each negative adds a strip whose height is the <em>positives already passed</em>.</p>
{r4}
    <ul class="why">
      <li>0.5 is a random ranking, 1 a perfect one; <code>roc_auc_score</code> computes it.</li>
    </ul>
  </div>
  <div class="subsec" id="roc-s3-2">
    <h3 class="ssh"><b>3.2</b>ROC-AUC as ranking</h3>
    <p class="skey">AUC is the chance that a random positive is <em>scored above</em> a random negative.</p>
{r5}
    <ul class="why">
      <li>Each column of the grid is one strip of the area: the same 21 of 24, read as pairs.</li>
      <li>Only the order of the scores matters; squash or stretch them and AUC does not move. A tie counts half.</li>
    </ul>
  </div>
  <div class="subsec" id="roc-s3-3">
    <h3 class="ssh"><b>3.3</b>Average precision</h3>
    <p class="skey">Each positive adds a strip of width 1/4 whose height is the <em>precision at that row</em>.</p>
''' + EQ_AP + '''
{r6}
    <ul class="why">
      <li><code>average_precision_score</code> computes exactly this sum; it is the usual "PR-AUC" and avoids the optimistic straight-line interpolation of <code>auc(recall, precision)</code>.</li>
      <li>Compare it with the baseline, not with 0.5: 0.30 on data with 1% positives is a strong model.</li>
    </ul>
  </div>
</section>

<section id="roc-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Rare positives</h2></div>
  <p class="key">Add many more negatives and <em>ROC does not move</em>, while precision and the PR curve fall.</p>
{r7}
  <ul class="why">
    <li>FPR divides by the negatives, so ten times more false alarms on ten times more negatives is the same rate; precision counts the alarms themselves.</li>
    <li>When positives are rare and every alert costs work — fraud, disease, search — report AP; ROC-AUC reads "excellent" while most alerts are wrong.</li>
    <li>ROC-AUC is comparable across datasets with different class ratios; AP is not, because its baseline moves with the ratio.</li>
  </ul>
</section>

''' + SCRIPT + '''

<footer>Machine learning · Model evaluation · continues from <a href="../metrics-confusion-matrix/index.html">Metric &amp; confusion matrix</a>; the third axis is <a href="../calibration/index.html">Probability calibration</a>.</footer>
'''

def build():
    figs = dict(r1=fig_mental(), r2=fig_sweep('roc'), r3=fig_sweep('pr'), r4=fig_area('roc'), r5=fig_pairs(),
                r6=fig_area('pr'), r7=fig_rare())
    return re.sub(r'\{(r\d+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'Slide the threshold down a sorted table of scores: each step is one confusion matrix and one '
           'point, tracing the ROC and PR curves; AUC is the share of correctly ordered pairs, and rare positives sink PR but not ROC.')
