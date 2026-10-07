# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/09-evaluation/metrics-confusion-matrix.
One predictions table (12 rows: id, true label, score) drives every classification figure; a 3-class
table drives multiclass; five (x, y, y_hat) rows with one outlier drive the regression metrics.
Every number in a figure is computed here and pinned with assert. Run: python3 metrics_confusion_matrix.py"""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, finish)
from tablefig import GR, RD, AM, tint, pill
from decision_tree import HL, splice, BODY as DT_BODY
import linear_algebra as _la
_la.RGBA.setdefault(GR, '--green-a'); _la.RGBA.setdefault(RD, '--red-a')

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/09-evaluation/metrics-confusion-matrix/index.html')
SCRIPT = DT_BODY[DT_BODY.index('<script>'):DT_BODY.index('</script>') + len('</script>')]

# ---------- the predictions table: id, true label (1 = pos), model score ----------
ROWS = [('A', 1, .55), ('B', 0, .15), ('C', 1, .95), ('D', 0, .45), ('E', 0, .80), ('F', 1, .20),
        ('G', 1, .70), ('H', 0, .05), ('I', 0, .48), ('J', 1, .40), ('K', 0, .30), ('L', 1, .85)]
SROWS = sorted(ROWS, key=lambda r: -r[2])           # sorted by score, high first
N = len(ROWS)

def cell_of(r, t):
    """(row, col) in the matrix: rows = actual pos / neg, cols = predicted pos / neg (sklearn layout)"""
    return (0 if r[1] else 1, 0 if r[2] >= t else 1)
def counts(t, rows=ROWS):
    c = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
    for r in rows: c[cell_of(r, t)] += 1
    return c[(0, 0)], c[(1, 0)], c[(0, 1)], c[(1, 1)]   # TP, FP, FN, TN
def prf(t):
    tp, fp, fn, tn = counts(t)
    p = tp / (tp + fp) if tp + fp else float('nan'); r = tp / (tp + fn)
    return p, r, (2 * p * r / (p + r) if p + r else 0)
def f2(x): return '%.2f' % x

TP, FP, FN, TN = counts(.5)
assert (TP, FP, FN, TN) == (4, 1, 2, 5)
ACC, PREC, REC, SPEC = (TP + TN) / N, TP / (TP + FP), TP / (TP + FN), TN / (TN + FP)
F1 = 2 * PREC * REC / (PREC + REC)
assert (f2(ACC), f2(PREC), f2(REC), f2(SPEC), f2(F1)) == ('0.75', '0.80', '0.67', '0.83', '0.73')
# threshold slide: 0.5 -> 0.6 -> 0.35
STAGES = [.5, .6, .35]
assert [counts(t) for t in STAGES] == [(4, 1, 2, 5), (3, 1, 3, 5), (5, 3, 1, 3)]
assert [f2(prf(t)[0]) + '/' + f2(prf(t)[1]) for t in STAGES] == ['0.80/0.67', '0.75/0.50', '0.62/0.83']
# F1 vs the plain mean for three thresholds
F1ROWS = [(.9,) + prf(.9), (.5,) + prf(.5), (0,) + prf(0)]
assert [(f2(p), f2(r), f2(f)) for _, p, r, f in F1ROWS] == [('1.00', '0.17', '0.29'), ('0.80', '0.67', '0.73'),
                                                             ('0.50', '1.00', '0.67')]
# cost: an FP costs 1, an FN costs 3; candidate thresholds = 0, the midpoints between sorted scores, 1
CFP, CFN = 1, 3
ASC = sorted(ROWS, key=lambda r: r[2]); SC = [r[2] for r in ASC]
CANDS = [0] + [(a + b) / 2 for a, b in zip(SC, SC[1:])] + [1]
COST = []
for t in CANDS:
    _tp, fp, fn, _tn = counts(t); COST.append((t, fp, fn, fp * CFP + fn * CFN))
GMIN = min(range(len(COST)), key=lambda g: COST[g][3])
assert GMIN == 2 and COST[GMIN][1:] == (4, 0, 4) and round(CANDS[GMIN], 3) == .175
G05 = 7; assert CANDS[6] < .5 < CANDS[7] and counts(CANDS[7]) == counts(.5) and COST[G05][3] == 7
assert max(c[3] for c in COST) == 18
# imbalanced: 95 negatives, 5 positives, a model that always says "neg"
assert (0 + 95) / 100 == .95
# multiclass: 12 rows, true / predicted
CLS = ['cat', 'dog', 'bird']
MC = [(1, 'cat', 'cat'), (2, 'cat', 'cat'), (3, 'cat', 'dog'), (4, 'cat', 'cat'), (5, 'cat', 'cat'), (6, 'cat', 'cat'),
      (7, 'dog', 'dog'), (8, 'dog', 'cat'), (9, 'dog', 'dog'), (10, 'dog', 'dog'), (11, 'bird', 'cat'), (12, 'bird', 'cat')]
CM3 = [[sum(1 for _, a, p in MC if a == CLS[i] and p == CLS[j]) for j in range(3)] for i in range(3)]
assert CM3 == [[5, 1, 0], [1, 3, 0], [2, 0, 0]]
PER = []
for k in range(3):
    tp = CM3[k][k]; fp = sum(CM3[i][k] for i in range(3)) - tp; fn = sum(CM3[k]) - tp
    PER.append((CLS[k], tp, fp, fn, 2 * tp / (2 * tp + fp + fn), sum(CM3[k])))
MACRO = sum(p[4] for p in PER) / 3
WEIGHTED = sum(p[4] * p[5] for p in PER) / 12
STP, SFP, SFN = (sum(p[i] for p in PER) for i in (1, 2, 3))
MICRO = 2 * STP / (2 * STP + SFP + SFN)
assert [f2(p[4]) for p in PER] == ['0.71', '0.75', '0.00'] and (STP, SFP, SFN) == (8, 4, 4)
assert (f2(MACRO), f2(WEIGHTED), f2(MICRO)) == ('0.49', '0.61', '0.67') and MICRO == 8 / 12
# regression: x, y, y_hat (the model is y_hat = 2x + 1); row 5 is the outlier
RG = [(1, 4, 3), (2, 4, 5), (3, 8, 7), (4, 8, 9), (5, 19, 11)]
assert all(h == 2 * x + 1 for x, _, h in RG)
RES = [y - h for _, y, h in RG]; assert RES == [1, -1, 1, -1, 8]
MAE = sum(abs(r) for r in RES) / 5; MSE = sum(r * r for r in RES) / 5; RMSE = math.sqrt(MSE)
YBAR = sum(y for _, y, _ in RG) / 5
SST = sum((y - YBAR) ** 2 for _, y, _ in RG); SSE = sum(r * r for r in RES); R2 = 1 - SSE / SST
assert (MAE, MSE, round(RMSE, 2), YBAR, round(SST, 1), SSE, round(R2, 2)) == (2.4, 13.6, 3.69, 8.6, 151.2, 68, .55)
assert sum(abs(r) for r in RES[:4]) / 4 == 1 and math.sqrt(sum(r * r for r in RES[:4]) / 4) == 1

# ---------- drawing helpers ----------
KIND = {(0, 0): ('TP', GR, 'gr'), (0, 1): ('FN', RD, 'rd'), (1, 0): ('FP', RD, 'rd'), (1, 1): ('TN', GR, 'gr')}
RGBA_OK = {GR: '--green-a', RD: '--red-a'}
def tt(c, a): return 'rgba(var(%s),%s)' % (RGBA_OK[c], a)

def idchip(cx, cy, s, pos, c=None):
    """one prediction row as a chip: filled blue = truly pos, hollow brand = truly neg"""
    w = 14 + len(s) * 7
    if c is None: c = FI if pos else BR
    if pos:
        return R(cx - w / 2, cy - 10, w, 20, c, c, 10, 1.3) + T(cx, cy + 4, s, 'var(--on-fill)', bold=True)
    return R(cx - w / 2, cy - 10, w, 20, BG, c, 10, 1.3) + T(cx, cy + 4, s, c, bold=True)

def mark(x, y, pos, r=6):
    if pos: return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, FI)
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, r - 1, BG, BR)

def legend(x, y):
    return mark(x, y - 4, 1, 5) + S(x + 10, y, 'truly pos', MU) + mark(x + 82, y - 4, 0, 5) + S(x + 92, y, 'truly neg', MU)

class Mat:
    """2 x 2 confusion matrix: rows = actual pos / neg, columns = predicted pos / neg"""
    def __init__(s, x, y, cw, ch, names=('pos', 'neg')):
        s.x, s.y, s.cw, s.ch, s.names = x, y, cw, ch, names
    def at(s, r, c): return s.x + c * s.cw, s.y + r * s.ch
    def frame(s, tags=True):
        o = T(s.x + s.cw, s.y - 30, 'predicted', MU, cls='sv-s')
        for j, n in enumerate(s.names): o += T(s.x + (j + .5) * s.cw, s.y - 10, n, TX, bold=True)
        o += T(s.x - 50, s.y + s.ch, 'actual', MU, cls='sv-s')
        for i, n in enumerate(s.names): o += T(s.x - 12, s.y + (i + .5) * s.ch + 4, n, TX, 'end', bold=True)
        for (i, j), (nm, c, _) in KIND.items():
            x, y = s.at(i, j)
            o += R(x + 2, y + 2, s.cw - 4, s.ch - 4, tt(c, '.07'), tt(c, '.55'), 6, 1.2)
            if tags: o += T(x + 12, y + 20, nm, c, 'start', bold=True)
        return o
    def slot(s, i, j, k):
        x, y = s.at(i, j)
        return x + 24 + (k % 3) * 30, y + 42 + (k // 3) * 26
    def cnt(s, i, j, n, c=None):
        x, y = s.at(i, j); c = c or KIND[(i, j)][1]
        return T(x + s.cw - 14, y + 22, str(n), c, 'end', cls='sv-t', bold=True)
    def cntpos(s, i, j):
        x, y = s.at(i, j); return x + s.cw - 18, y + 18
    def ring(s, i, j, c=HL, dash=None, sw=2.2):
        x, y = s.at(i, j)
        return R(x - 1, y - 1, s.cw + 2, s.ch + 2, 'none', c, 7, sw, dash)

def toks(cx, y, items):
    """centre a row of math tokens on cx; items = [(text, colour)] -> [(x, text, colour)], width"""
    ws = [14 if t in ('+', '−', '·', '×') else len(t) * 7.6 + 6 for t, _ in items]
    x = cx - sum(ws) / 2; out = []
    for w, (t, c) in zip(ws, items):
        out.append((x + w / 2, t, c)); x += w
    return out, sum(ws)

def frac(cx, cy, num, den, c=TX):
    """stacked fraction in LaTeX style (strings with {v} for italic variables)"""
    w = max(len(re.sub(r'[{}]', '', num)), len(re.sub(r'[{}]', '', den))) * 7.4 + 12
    return M(cx, cy - 7, num, c) + L(cx - w / 2, cy, cx + w / 2, cy, c, 1.1) + M(cx, cy + 17, den, c), w

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('cm1-', 720, 0, 'Twelve predictions, each with an id, a true label and a model score, are listed by score, highest first. '
             'A threshold line at 0.5 slides down the table: rows above it get the predicted label pos, rows below get neg. '
             'Then each row drops as a chip into one of the four cells of a two by two matrix, rows actual pos or neg, '
             'columns predicted pos or neg: 4 true positives, 1 false positive, 2 false negatives, 5 true negatives.',
             'SCORE → THRESHOLD → PREDICTED LABEL → ONE OF FOUR CELLS')
    t = Table(0, 30, [('id', 30), ('true', 50), ('score', 50), ('predicted', 66)], step=26, rh=22)
    f.static(t.head())
    for j, r in enumerate(SROWS):
        f.show(t.row(j, [r[0], 'pos' if r[1] else 'neg', f2(r[2])], colors={1: FI if r[1] else BR}), .2 + j * .08)
    k = sum(1 for r in ROWS if r[2] >= .5); yl = t.ry(k) - 2
    f.path(L(-4, yl, t.w + 4, yl, HL, 1.8, '5 4') + R(t.w + 8, yl - 10, 52, 20, BG, HL, 5, 1.2) +
           T(t.w + 34, yl + 4, 't = 0.5', HL, bold=True), [(0, 0, -k * 26), (1.4, 0, 0)], 1.2, d=1.0)
    for j, r in enumerate(SROWS):
        p = r[2] >= .5
        f.show(t.cell(j, 3, 'pos' if p else 'neg', c=FI if p else BR), 2.8 + j * .1)
    m = Mat(352, 96, 174, 120)
    f.static(m.frame())
    f.static(legend(352, 370))
    slots = {}
    for j, r in enumerate(SROWS):
        i, c = cell_of(r, .5); kk = slots.get((i, c), 0); slots[(i, c)] = kk + 1
        sx, sy = m.slot(i, c, kk)
        x0, y0 = t.cx(0), t.ry(j) + 11
        ts = 4.6 + j * .45
        f.path(idchip(sx, sy, r[0], r[1]), [(0, x0 - sx, y0 - sy), (ts, 0, 0)], ts - .3, d=.45)
    for (i, c), n in zip([(0, 0), (1, 0), (0, 1), (1, 1)], (TP, FP, FN, TN)):
        f.show(m.cnt(i, c, n), 10.4)
    return finish(f, 384)

# ---------- 02 metrics, one figure kind ----------
NAMES = {(0, 0): 'TP', (1, 0): 'FP', (0, 1): 'FN', (1, 1): 'TN'}
VAL = {(0, 0): TP, (1, 0): FP, (0, 1): FN, (1, 1): TN}

def fig_metric(pre, name, num, den, question, aria):
    f = Anim(pre, 720, 0, aria, question)
    m = Mat(110, 84, 140, 112)
    f.static(m.frame())
    sl = {}
    for r in SROWS:
        i, c = cell_of(r, .5); kk = sl.get((i, c), 0); sl[(i, c)] = kk + 1
        f.static(idchip(*m.slot(i, c, kk), r[0], r[1]))
    for ij in VAL: f.static(m.cnt(*ij, VAL[ij]))
    for k, ij in enumerate(den):
        f.show(m.ring(*ij, HL, '5 4', 1.8), .6 + k * .2)
    for k, ij in enumerate(num):
        f.show(m.ring(*ij, HL, None, 2.6), 1.4 + k * .2)
    CX = 545
    sym, w = frac(CX, 104, ' + '.join(NAMES[ij] for ij in num), ' + '.join(NAMES[ij] for ij in den))
    f.static(M(CX - w / 2 - 10, 109, name + ' =', TX, 'end') + sym)
    # numbers travel from the cells into the fraction
    nt, nw = toks(CX, 0, sum([[(str(VAL[ij]), KIND[ij][1])] + ([('+', TX)] if k < len(num) - 1 else [])
                              for k, ij in enumerate(num)], []))
    dt, dw = toks(CX, 0, sum([[(str(VAL[ij]), KIND[ij][1])] + ([('+', TX)] if k < len(den) - 1 else [])
                              for k, ij in enumerate(den)], []))
    Y = 200
    f.show(L(CX - max(nw, dw) / 2 - 4, Y, CX + max(nw, dw) / 2 + 4, Y, TX, 1.1), 2.0)
    def fly(ts, yb, cells, t0):
        ci = 0
        for x, s, c in ts:
            if s == '+':
                f.show(M(x, yb, '+', TX), t0 + .6); continue
            ij = cells[ci]; ci += 1
            px, py = m.cntpos(*ij)
            f.path(M(x, yb, s, c), [(0, px - x, py - yb + 4), (t0 + ci * .35, 0, 0)], t0 + ci * .35 - .3, d=.8)
    fly(nt, Y - 7, num, 2.2)
    fly(dt, Y + 17, den, 2.2 + len(num) * .35 + .4)
    tv = sum(VAL[ij] for ij in num) / sum(VAL[ij] for ij in den)
    tend = 2.2 + (len(num) + len(den)) * .35 + 1.6
    f.show(M(CX + max(nw, dw) / 2 + 14, Y + 5, '=', TX, 'start'), tend)
    f.show(chip(CX + max(nw, dw) / 2 + 60, Y + 1, f2(tv), GR if False else FI, 58), tend + .2)
    return finish(f, 330), tv

def fig_accuracy():
    s, v = fig_metric('cm2-', 'accuracy', [(0, 0), (1, 1)], [(0, 0), (1, 0), (0, 1), (1, 1)],
                      'ALL FOUR CELLS · HOW MANY ROWS ARE RIGHT',
                      'The confusion matrix from the mental model, rows A to L in their cells. All four cells are outlined: '
                      'the denominator is every row. The two diagonal cells, TP 4 and TN 5, are outlined solid. Their counts '
                      'travel into the fraction: 4 plus 5 over 4 plus 1 plus 2 plus 5, accuracy 0.75.')
    assert f2(v) == '0.75'; return s

def fig_precision():
    s, v = fig_metric('cm3-', 'precision', [(0, 0)], [(0, 0), (1, 0)],
                      'THE PREDICTED-pos COLUMN · OF WHAT I FLAGGED, HOW MUCH IS RIGHT',
                      'The confusion matrix with rows A to L in their cells. The predicted pos column is outlined: TP 4 and '
                      'FP 1, the five rows the model flagged. TP is outlined solid. The counts travel into the fraction 4 over '
                      '4 plus 1: precision 0.80.')
    assert f2(v) == '0.80'; return s

def fig_recall():
    s, v = fig_metric('cm4-', 'recall', [(0, 0)], [(0, 0), (0, 1)],
                      'THE ACTUAL-pos ROW · OF THE TRUE POSITIVES, HOW MANY I CAUGHT',
                      'The confusion matrix with rows A to L in their cells. The actual pos row is outlined: TP 4 and FN 2, '
                      'the six truly positive rows. TP is outlined solid. The counts travel into the fraction 4 over 4 plus 2: '
                      'recall 0.67.')
    assert f2(v) == '0.67'; return s

def fig_specificity():
    s, v = fig_metric('cm5-', 'specificity', [(1, 1)], [(1, 0), (1, 1)],
                      'THE ACTUAL-neg ROW · OF THE TRUE NEGATIVES, HOW MANY I LEFT ALONE',
                      'The confusion matrix with rows A to L in their cells. The actual neg row is outlined: FP 1 and TN 5, '
                      'the six truly negative rows. TN is outlined solid. The counts travel into the fraction 5 over 1 plus 5: '
                      'specificity 0.83.')
    assert f2(v) == '0.83'; return s

def fig_f1():
    f = Anim('cm6-', 720, 0, 'Three thresholds on the same table, each a row with a 0 to 1 axis. Precision and recall are marked. '
             'A tick marks their plain mean; then the F1 dot slides from the mean toward the smaller of the two. Threshold '
             '0.9: precision 1.00, recall 0.17, mean 0.58, F1 0.29. Threshold 0.5: 0.80 and 0.67, mean 0.73, F1 0.73. '
             'Threshold 0, flag everyone: 0.50 and 1.00, mean 0.75, F1 0.67.',
             'F1 = HARMONIC MEAN · IT SLIDES TOWARD THE SMALLER VALUE')
    X0, W = 210, 440
    P = lambda v: X0 + v * W
    for k, (t, p, r, f1) in enumerate(F1ROWS):
        y = 80 + k * 92; t0 = .4 + k * 2.4
        f.static(S(0, y - 4, 'threshold %g' % t, TX, bold=True) +
                 S(0, y + 14, {.9: 'flags C only', .5: 'the matrix above', 0: 'flags all 12'}[t], MU))
        f.static(L(X0, y, X0 + W, y, RULE_HI, 1.3))
        for v in (0, .5, 1):
            f.static(L(P(v), y - 4, P(v), y + 4, RULE_HI, 1) + T(P(v), y + 22, '%g' % v, FA, mono=True))
        lo, hi = sorted((p, r))
        f.show(L(P(lo), y, P(hi), y, RULE, 4), t0)
        f.show(dot(P(p), y, VI, 6, BG) + T(P(p), y - 13, 'P %s' % f2(p), VI, bold=True), t0)
        f.show(dot(P(r), y, BR, 6, BG) + T(P(r), y - 13, 'R %s' % f2(r), BR, bold=True), t0 + .3)
        mn = (p + r) / 2
        f.show(L(P(mn), y - 30, P(mn), y + 8, MU, 1.2, '3 3') + T(P(mn), y - 34, 'mean %s' % f2(mn), MU, 'middle'), t0 + .8)
        lab = 'F1 %s' % f2(f1)
        f.path(dot(P(f1), y, GR, 6.5, BG) + T(P(f1), y + 38, lab, GR, bold=True), [(0, P(mn) - P(f1), 0), (t0 + 1.3, 0, 0)],
               t0 + 1.1, d=.8)
    return finish(f, 80 + 2 * 92 + 50)

# ---------- 03 Threshold ----------
def fig_threshold():
    f = Anim('cm7-', 720, 0, 'The twelve rows by score next to the matrix. The threshold starts at 0.5: TP 4, FP 1, FN 2, TN 5, '
             'precision 0.80, recall 0.67. It moves up to 0.6: row A drops from TP to FN, giving precision 0.75, '
             'recall 0.50. It moves down to 0.35: A, G and J are caught, I and D become false positives; precision 0.62, '
             'recall 0.83. Each stage adds a row to the table below the matrix.',
             'MOVE THE LINE · ROWS CHANGE CELLS · PRECISION AND RECALL TRADE')
    t = Table(0, 30, [('id', 30), ('true', 50), ('score', 50)], step=26, rh=22)
    f.static(t.head())
    for j, r in enumerate(SROWS):
        f.static(t.row(j, [r[0], 'pos' if r[1] else 'neg', f2(r[2])], colors={1: FI if r[1] else BR}))
    bnd = [sum(1 for r in ROWS if r[2] >= s) for s in STAGES]
    T1, T2 = 2.6, 6.4
    yl = lambda k: t.ry(k) - 2
    f.path(L(-4, 0, t.w + 4, 0, HL, 1.8, '5 4'), [(0, 0, yl(bnd[0])), (T1, 0, yl(bnd[1])), (T2, 0, yl(bnd[2]))], 0, d=.8)
    for k, (s, a, b) in enumerate(zip(STAGES, (0, T1, T2), (T1, T2, None))):
        f.show(R(t.w + 8, yl(bnd[k]) - 10, 52, 20, BG, HL, 5, 1.2) + T(t.w + 34, yl(bnd[k]) + 4, 't = %g' % s, HL, bold=True),
               a + (.9 if k else 0), hide=(b if b else None))
    m = Mat(330, 70, 174, 104)
    f.static(m.frame())
    pos = []
    for s in STAGES:
        sl, d = {}, {}
        for r in SROWS:
            ij = cell_of(r, s); kk = sl.get(ij, 0); sl[ij] = kk + 1; d[r[0]] = m.slot(*ij, kk)
        pos.append(d)
    moved = lambda k, r: pos[k][r[0]] != pos[k - 1][r[0]]
    for r in SROWS:
        fx, fy = pos[2][r[0]]
        pts = [(0, pos[0][r[0]][0] - fx, pos[0][r[0]][1] - fy)]
        pts.append((T1 + 1.0, pos[1][r[0]][0] - fx, pos[1][r[0]][1] - fy))
        pts.append((T2 + 1.0, 0, 0))
        f.path(idchip(fx, fy, r[0], r[1]), pts, 0, d=.9)
    tb = Table(330, 300, [('t', 54), ('TP', 46), ('FP', 46), ('FN', 46), ('TN', 46), ('precision', 64), ('recall', 46)],
               step=26, rh=22)
    f.static(tb.head())
    for k, (s, a, b) in enumerate(zip(STAGES, (0, T1, T2), (T1, T2, None))):
        tp, fp, fn, tn = counts(s); p, r, _ = prf(s)
        for (i, j), n in zip([(0, 0), (1, 0), (0, 1), (1, 1)], (tp, fp, fn, tn)):
            f.show(m.cnt(i, j, n), a + (2.0 if k else .3), hide=(b + 1.0 if b else None))
        f.show(tb.row(k, ['%g' % s, str(tp), str(fp), str(fn), str(tn), f2(p), f2(r)], colors={5: VI, 6: BR}),
               a + (2.4 if k else .6))
    f.static(legend(330, 410))
    assert bnd == [5, 4, 8]
    return finish(f, 420)

# ---------- 04 Imbalanced data ----------
def fig_imbalance():
    f = Anim('cm8-', 720, 0, 'A hundred people as dots: 95 truly negative, 5 truly positive. The model always predicts neg. '
             'The block of 95 negatives slides into the TN cell, the five positives into the FN cell; the predicted pos '
             'column stays empty. Accuracy is 0 plus 95 over 100, 0.95. Recall is 0 over 5, 0: the model catches nobody.',
             'ACCURACY PARADOX · 95 NEG, 5 POS, A MODEL THAT ALWAYS SAYS neg')
    sp = 9
    neg = ''.join(mark(4 + (k % 19) * sp, 4 + (k // 19) * sp, 0, 3.4) for k in range(95))
    posg = ''.join(mark(4, 4 + k * sp, 1, 3.6) for k in range(5))
    PX, PY = 0, 70
    f.static(S(0, 54, '100 rows', MU, bold=True))
    m = Mat(330, 70, 190, 112)
    f.static(m.frame())
    tnx, tny = m.at(1, 1); fnx, fny = m.at(0, 1)
    TX0, TY0 = tnx + 12, tny + 40
    FX0, FY0 = fnx + 30, fny + 36
    f.show(chip(95, 158, 'model: always neg', VI, 150, mono=False), .8)
    f.path('<g transform="translate(%.1f,%.1f)">%s</g>' % (FX0, FY0, posg), [(0, PX + 19 * sp + 8 - FX0, PY - FY0), (1.8, 0, 0)],
           0, d=1.0)
    f.path('<g transform="translate(%.1f,%.1f)">%s</g>' % (TX0, TY0, neg), [(0, PX - TX0, PY - TY0), (2.6, 0, 0)], 0, d=1.0)
    for (i, j), n in zip([(0, 0), (1, 0), (0, 1), (1, 1)], (0, 0, 5, 95)):
        f.show(m.cnt(i, j, n), 3.8)
    f.static(legend(0, 210))
    Y = 330
    a, _ = frac(130, Y, '0 + 95', '100')
    f.show(M(52, Y + 5, 'accuracy =', TX, 'end') + a + M(170, Y + 5, '=', TX) + chip(206, Y + 1, '0.95', GR, 50), 4.6)
    b, _ = frac(370, Y, '0', '0 + 5')
    f.show(M(340, Y + 5, 'recall =', TX, 'end') + b + M(402, Y + 5, '=', TX) + chip(430, Y + 1, '0', RD, 34), 5.6)
    f.show(S(490, Y - 4, 'precision = 0 / 0', MU) + S(490, Y + 14, 'undefined: nothing flagged', RD, bold=True), 6.4)
    f.show(m.ring(1, 1, HL, '5 4', 1.8), 4.6, hide=5.5)
    f.show(m.ring(0, 0, HL, '5 4', 1.8) + m.ring(0, 1, HL, '5 4', 1.8), 5.6)
    return finish(f, 360)

# ---------- 05 Threshold by cost ----------
def fig_cost():
    f = Anim('cm9-', 720, 0, 'The twelve rows as dots on a line, sorted by score, low to high. A threshold line steps through every '
             'gap from the far left, flag everyone, to the far right, flag no one. At each stop, false positives cost 1 '
             'each and false negatives 3 each, and a stacked cost bar grows under the line. Flag everyone costs 6; the '
             'default 0.5 costs 7; the cheapest stop is between 0.15 and 0.20, threshold 0.175: 4 false positives, '
             '0 false negatives, cost 4. The line returns there.',
             'COST PER THRESHOLD = FP × 1 + FN × 3 · KEEP THE CHEAPEST')
    DX = lambda i: 110 + i * 48
    GX = lambda g: 86 + g * 48
    for i, r in enumerate(ASC):
        f.static(mark(DX(i), 70, r[1], 7) + T(DX(i), 52, r[0], MU, bold=True) + T(DX(i), 94, f2(r[2]), FA, mono=True))
    f.static(S(0, 74, 'rows by score', MU) + S(GX(12) + 10, 74, 'flag →', MU) )
    BASE, U = 270, 7
    f.static(L(GX(0) - 18, BASE, GX(12) + 18, BASE, RULE_HI, 1.2))
    f.static(S(0, 292, 'FP × 1', RD, bold=True) + S(0, 310, 'FN × 3', VI, bold=True) + S(0, BASE - 4, 'cost', MU, bold=True))
    ts = [1.0 + g * .5 for g in range(13)]
    fin = ts[-1] + 1.2
    f.path(L(GX(GMIN), 36, GX(GMIN), 104, HL, 2, '5 4'),
           [(0, GX(0) - GX(GMIN), 0)] + [(t, GX(g) - GX(GMIN), 0) for g, t in enumerate(ts) if g] + [(fin, 0, 0)], .6, d=.35)
    for g, (t, fp, fn, c) in enumerate(COST):
        x = GX(g); hf, hn = fp * CFP * U, fn * CFN * U
        s = ''
        if hf: s += R(x - 11, BASE - hf, 22, hf, tt(RD, '.22'), RD, 2, 1)
        if hn: s += R(x - 11, BASE - hf - hn, 22, hn, tn(VI, '.22'), VI, 2, 1)
        s += T(x, BASE - hf - hn - 6, str(c), TX, mono=True, bold=True)
        s += T(x, 292, str(fp), RD, mono=True) + T(x, 310, str(fn), VI, mono=True)
        f.show(s, ts[g] + .3)
    xm = GX(GMIN); hm = COST[GMIN][3] * U
    f.show(R(xm - 15, BASE - hm - 22, 30, hm + 26, 'none', GR, 5, 2) + pill(xm, 324, 'cheapest · t = 0.175', 'gr', 140), fin + .3)
    x5 = GX(G05)
    f.show(T(x5, 340, '0.5 default · cost 7', MU), ts[G05] + .4)
    return finish(f, 350)

# ---------- 06 Multiclass ----------
CC = {'cat': FI, 'dog': VI, 'bird': 'var(--probe)'}
class Mat3:
    def __init__(s, x, y, cw, ch): s.x, s.y, s.cw, s.ch = x, y, cw, ch
    def at(s, i, j): return s.x + j * s.cw, s.y + i * s.ch
    def frame(s, small=False):
        o = T(s.x + 1.5 * s.cw, s.y - 30, 'predicted', MU, cls='sv-s')
        for j, n in enumerate(CLS): o += T(s.x + (j + .5) * s.cw, s.y - 10, n, CC[n], bold=True)
        o += T(s.x - 56, s.y + 1.5 * s.ch + 4, 'actual', MU, cls='sv-s', a='end') if not small else ''
        for i, n in enumerate(CLS): o += T(s.x - 10, s.y + (i + .5) * s.ch + 4, n, CC[n], 'end', bold=True)
        for i in range(3):
            for j in range(3):
                c = GR if i == j else RD; x, y = s.at(i, j)
                o += R(x + 2, y + 2, s.cw - 4, s.ch - 4, tt(c, '.07'), tt(c, '.5'), 6, 1.2)
        return o
    def slot(s, i, j, k):
        x, y = s.at(i, j); return x + 24 + (k % 3) * 30, y + 38 + (k // 3) * 24
    def cnt(s, i, j, n, big=False):
        x, y = s.at(i, j); c = GR if i == j else RD
        if big: return T(x + s.cw / 2, y + s.ch / 2 + 6, str(n), c if n else FA, cls='sv-t', bold=True)
        return T(x + s.cw - 12, y + 20, str(n), c if n else FA, 'end', cls='sv-t', bold=True)

def fig_multi():
    f = Anim('cm10-', 720, 0, 'Twelve predictions over three classes, cat, dog and bird, listed by true class. Each row drops as a '
             'chip into the cell of its actual class row and predicted class column, one actual class at a time. '
             'Cat: five on the diagonal, one predicted dog. Dog: three right, one predicted cat. Bird: both predicted cat. '
             'The diagonal holds the 8 correct rows.', 'ROWS = ACTUAL CLASS · COLUMNS = PREDICTED · FILLED ROW BY ROW')
    t = Table(0, 30, [('id', 30), ('true', 50), ('pred', 50)], step=26, rh=22)
    f.static(t.head())
    for j, (i, a, p) in enumerate(MC):
        f.static(t.row(j, [str(i), a, p], colors={1: CC[a], 2: CC[p] if p == a else RD}))
    m = Mat3(300, 80, 134, 90)
    f.static(m.frame())
    sl = {}
    tt0 = 1.0
    for j, (i, a, p) in enumerate(MC):
        ij = (CLS.index(a), CLS.index(p)); kk = sl.get(ij, 0); sl[ij] = kk + 1
        sx, sy = m.slot(*ij, kk); x0, y0 = t.cx(0), t.ry(j) + 11
        ts = tt0 + j * .45 + CLS.index(a) * .6
        f.path(idchip(sx, sy, str(i), True, CC[a]), [(0, x0 - sx, y0 - sy), (ts, 0, 0)], ts - .3, d=.45)
    tc = tt0 + 12 * .45 + 1.8
    for i in range(3):
        for j in range(3):
            f.show(m.cnt(i, j, CM3[i][j]), tc + i * .3)
    f.show(T(m.x + 3 * m.cw + 8, m.y + 3 * m.ch + 4, 'diagonal = 8 right', GR, 'end' if False else 'start', bold=True), tc + 1.2)
    return finish(f, 362)

def fig_average():
    f = Anim('cm11-', 720, 0, 'The three by three matrix. For each class in turn its column and row are outlined and one row of a '
             'table is filled: cat TP 5, FP 3, FN 1, F1 0.71, 6 rows; dog TP 3, FP 1, FN 1, F1 0.75, 4 rows; bird TP 0, FP 0, '
             'FN 2, F1 0, 2 rows. The three F1 values travel down into the macro average, 0.49. The weighted average by '
             'row count is 0.61. Micro pools TP 8, FP 4, FN 4 into one F1, 0.67, equal to accuracy.',
             'ONE F1 PER CLASS · THREE WAYS TO AVERAGE THEM')
    m = Mat3(70, 70, 64, 52)
    f.static(m.frame(small=True))
    for i in range(3):
        for j in range(3): f.static(m.cnt(i, j, CM3[i][j], big=True))
    tb = Table(320, 40, [('class', 56), ('TP', 44), ('FP', 44), ('FN', 44), ('F1', 60), ('rows', 50)], step=28, rh=24)
    f.static(tb.head())
    for k, (c, tp, fp, fn, f1, n) in enumerate(PER):
        t0 = .5 + k * 1.4
        x, y = m.at(0, k)
        f.show(R(x, m.y - 2, m.cw, 3 * m.ch + 4, 'none', HL, 6, 2) +
               R(m.x - 2, m.y + k * m.ch, 3 * m.cw + 4, m.ch, 'none', HL, 6, 1.6, '5 4'), t0, hide=t0 + 1.2)
        f.show(tb.row(k, [c, str(tp), str(fp), str(fn), f2(f1), str(n)], colors={0: CC[c], 4: GR if f1 else RD}), t0 + .4)
    Y = 246; ta = 5.0
    f.static(S(0, Y + 5, 'macro', TX, bold=True) + S(0, Y + 21, 'each class counts the same', MU))
    items = [('(', TX)] + sum([[(f2(p[4]), GR if p[4] else RD)] + ([('+', TX)] if k < 2 else []) for k, p in enumerate(PER)], []) + [(')', TX)]
    xs, w = toks(300, 0, items)
    for k, (x, s, c) in enumerate(xs):
        if s in '()+':
            f.show(M(x, Y + 5, s, TX), ta); continue
        ki = [q for q in xs if q[1] not in '()+'].index((x, s, c))
        fx, fy = tb.cx(4), tb.ry(ki) + 17
        f.path(M(x, Y + 5, s, c), [(0, fx - x, fy - Y - 5), (ta + ki * .3, 0, 0)], ta + ki * .3 - .3, d=.8)
    f.show(M(300 + w / 2 + 8, Y + 5, '/ 3  =', TX, 'start') + chip(300 + w / 2 + 92, Y + 1, f2(MACRO), RD, 52), ta + 1.6)
    Y2 = Y + 46
    f.show(S(0, Y2 + 5, 'weighted', TX, bold=True) + S(0, Y2 + 21, 'big classes count more', MU) +
           M(300, Y2 + 5, '(6 · 0.71 + 4 · 0.75 + 2 · 0) / 12  =', TX) + chip(474, Y2 + 1, f2(WEIGHTED), VI, 52), ta + 2.6)
    Y3 = Y2 + 46
    f.show(S(0, Y3 + 5, 'micro', TX, bold=True) + S(0, Y3 + 21, 'pool the counts, then one F1', MU) +
           M(300, Y3 + 5, '2 · 8 / (2 · 8 + 4 + 4)  =', TX) + chip(434, Y3 + 1, f2(MICRO), BR, 52) +
           S(470, Y3 + 5, '= accuracy 8 / 12', MU), ta + 3.6)
    return finish(f, Y3 + 34)

# ---------- 07 Regression ----------
PX = lambda x, x0=270, sp=55: x0 + (x - 1) * sp
PY = lambda v: 260 - v * 10

def plot_base(f, x0=270, sp=55):
    f.static(L(x0 - 30, PY(0), x0 + 4 * sp + 30, PY(0), RULE_HI, 1.3) + L(x0 - 30, PY(0), x0 - 30, PY(20) - 6, RULE_HI, 1.3))
    for v in (0, 10, 20):
        f.static(T(x0 - 36, PY(v) + 4, str(v), FA, 'end', mono=True))
    for x in range(1, 6): f.static(T(PX(x, x0, sp), PY(0) + 16, str(x), FA, mono=True))
    f.static(poly([(PX(.6, x0, sp), PY(2 * .6 + 1)), (PX(5.4, x0, sp), PY(2 * 5.4 + 1))], FI, 1.8) +
             M(PX(1.6, x0, sp) - 6, PY(4.2) - 10, '{ŷ} = 2{x} + 1', FI, 'end'))
    for x, y, h in RG: f.static(dot(PX(x, x0, sp), PY(y), TX, 4.5))

def reg_table(f, last, vals, cols=None):
    cols = cols or [('x', 30), ('y', 36), ('ŷ', 36), (last, 60)]
    t = Table(0, 40, cols, step=30, rh=24)
    f.static(t.head())
    for i, (x, y, h) in enumerate(RG):
        f.static(t.row(i, [str(x), str(y), str(h)] + ['' for _ in cols[3:]], colors={1: RD} if i == 4 else None))
    return t

def fig_mae():
    f = Anim('cm12-', 720, 0, 'Five rows with x, true y and prediction y-hat from the line y-hat = 2x + 1; row 5 is an outlier with y '
             '19 against 11. Each residual is drawn as a vertical segment from the line to the point, and its absolute value '
             'fills the last table column: 1, 1, 1, 1, 8. The five segments slide right and stack into one column of '
             'height 12. Divided by 5 rows: MAE 2.4. Without row 5 it would be 1.', 'MAE · LINE UP THE ERRORS, AVERAGE THEIR LENGTH')
    t = reg_table(f, '|y − ŷ|', None)
    plot_base(f)
    SX = 640; cum = 0
    f.static(L(SX - 20, PY(0), SX + 20, PY(0), RULE_HI, 1.2))
    for i, ((x, y, h), r) in enumerate(zip(RG, RES)):
        t0 = .4 + i * .5
        lo, hi = min(y, h), max(y, h)
        seg = lambda X, Y0, Y1: L(X, Y0, X, Y1, RO, 3)
        f.show(seg(PX(x), PY(hi), PY(lo)), t0)
        f.show(t.cell(i, 3, str(abs(r)), c=RO), t0 + .2)
        fy1 = PY(0) - cum * 10; fy0 = fy1 - abs(r) * 10
        f.path(seg(SX, fy0, fy1) + L(SX - 6, fy1, SX + 6, fy1, RO, 1), [(0, PX(x) - SX, PY(hi) - fy0), (3.4 + i * .4, 0, 0)],
               3.2 + i * .4, d=.8)
        cum += abs(r)
    f.show(T(SX, PY(cum) - 10, 'Σ |y − ŷ| = 12', RO, bold=True), 6.0)
    Y = 316
    a, _ = frac(170, Y, '12', '5')
    f.show(M(140, Y + 5, 'MAE =', TX, 'end') + a + M(196, Y + 5, '=', TX) + chip(230, Y + 1, '2.4', RO, 44), 6.6)
    f.show(S(300, Y + 5, 'without row 5:  4 / 4 = 1', MU), 7.4)
    return finish(f, 346)

def fig_mse():
    f = Anim('cm13-', 720, 0, 'The same five rows and line. Each residual becomes a square with that side: four small squares of area '
             '1 and one big square of area 64 for the outlier. The squares slide right and stack: total area 68. Divided by '
             '5: MSE 13.6; its square root, RMSE, is 3.69, against MAE 2.4. Without row 5 both RMSE and MAE are 1, so the '
             'single outlier moves RMSE further.', 'MSE · SQUARE EACH ERROR · ONE BIG ERROR OWNS THE SUM')
    t = reg_table(f, '(y − ŷ)²', None)
    plot_base(f)
    SX = 610; cum = 0
    f.static(L(SX - 10, PY(0), SX + 90, PY(0), RULE_HI, 1.2))
    for i, ((x, y, h), r) in enumerate(zip(RG, RES)):
        t0 = .4 + i * .5; s = abs(r) * 10; hi = max(y, h)
        sq = lambda X, Y0: R(X, Y0, s, s, tn(RO, '.20'), RO, 1, 1.2) + (T(X + s / 2, Y0 + s / 2 + 5, '64', RO, cls='sv-t', bold=True) if s > 20 else '')
        f.show(L(PX(x), PY(hi), PX(x), PY(hi) + s, RO, 2), t0)
        f.show(sq(PX(x), PY(hi)), t0 + .15)
        f.show(t.cell(i, 3, str(r * r), c=RO), t0 + .3)
        fy0 = PY(0) - cum * 10 - s
        f.path(sq(SX, fy0), [(0, PX(x) - SX, PY(hi) - fy0), (3.4 + i * .4, 0, 0)], 3.2 + i * .4, d=.8)
        cum += abs(r)
    f.show(T(SX + 40, PY(cum) - 10, 'Σ (y − ŷ)² = 68', RO, bold=True), 6.0)
    Y = 316
    a, _ = frac(170, Y, '68', '5')
    f.show(M(140, Y + 5, 'MSE =', TX, 'end') + a + M(196, Y + 5, '=', TX) + chip(234, Y + 1, '13.6', RO, 50), 6.6)
    f.show(M(320, Y + 5, 'RMSE = √13.6 =', TX, 'start') + chip(455, Y + 1, '3.69', RO, 50), 7.3)
    f.show(S(500, Y - 2, 'MAE 2.4 on the same rows', MU) + S(500, Y + 14, 'without row 5: both 1', MU), 8.0)
    return finish(f, 346)

def fig_r2():
    f = Anim('cm14-', 720, 0, 'The same five rows. First the baseline that always predicts the mean, y-bar 8.6, a dashed line: the '
             'squares from it to each point add up to SST 151.2. Then the model line: its squares add up to SSE 68. The two '
             'totals travel into R squared = 1 minus 68 over 151.2 = 0.55: the model removes 55 percent of the squared '
             'error of the mean.', 'R² · HOW MUCH OF THE MEAN’S SQUARED ERROR THE MODEL REMOVES')
    cols = [('x', 30), ('y', 36), ('ŷ', 36), ('(y − ȳ)²', 62), ('(y − ŷ)²', 62)]
    t = reg_table(f, None, None, cols)
    x0, sp = 370, 50
    plot_base(f, x0, sp)
    f.static(L(x0 - 30, PY(YBAR), x0 + 4 * sp + 30, PY(YBAR), VI, 1.6, '6 4') + M(x0 + 4 * sp + 34, PY(YBAR) + 18, '{ȳ} = 8.6', VI, 'end'))
    for i, (x, y, h) in enumerate(RG):
        t0 = .4 + i * .4; d = y - YBAR; s = abs(d) * 10; top = PY(max(y, YBAR))
        f.show(R(PX(x, x0, sp), top, s, s, tn(VI, '.12'), VI, 1, 1.1), t0)
        f.show(t.cell(i, 3, ('%.2f' % (d * d)).rstrip('0').rstrip('.'), c=VI), t0 + .2)
    f.show(T(712, 44, 'SST = 151.2', VI, 'end', bold=True), 2.6)
    for i, ((x, y, h), r) in enumerate(zip(RG, RES)):
        t0 = 3.2 + i * .4; s = abs(r) * 10; top = PY(max(y, h))
        f.show(R(PX(x, x0, sp), top, s, s, tn(RO, '.22'), RO, 1, 1.4), t0)
        f.show(t.cell(i, 4, str(r * r), c=RO), t0 + .2)
    f.show(T(712, 62, 'SSE = 68', RO, 'end', bold=True), 5.4)
    Y = 318; tg = 6.2
    f.static(M(110, Y + 5, '{R}² = 1 −', TX, 'end'))
    f.static(L(126, Y, 190, Y, TX, 1.1))
    f.path(M(158, Y - 7, '68', RO), [(0, 712 - 20 - 158, 62 - Y + 7), (tg, 0, 0)], tg - .3, d=.9)
    f.path(M(158, Y + 17, '151.2', VI), [(0, 712 - 40 - 158, 44 - Y - 17), (tg + .5, 0, 0)], tg + .2, d=.9)
    f.show(M(204, Y + 5, '=', TX) + chip(240, Y + 1, '0.55', GR, 50), tg + 1.6)
    f.show(S(300, Y - 2, '1: perfect · 0: no better than ȳ', MU) + S(300, Y + 14, 'below 0: worse than ȳ', RD), tg + 2.2)
    return finish(f, 346)

# ---------- equations ----------
def eqf(name, num, den, note, cls=''):
    return ('  <div class="eq">\n    <div class="line">\n      <span class="t"><span><b class="fn">%s</b></span></span>\n'
            '      <span class="op">=</span>\n      <span class="t%s"><span><span class="frac"><i>%s</i><i>%s</i></span></span><em>%s</em></span>\n'
            '    </div>\n  </div>\n') % (name, (' ' + cls) if cls else '', num, den, note)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Model evaluation</p>
  <h1>Metric &amp; <em>confusion matrix</em></h1>
  <p class="lede">A threshold turns scores into labels, the labels sort every row into <b>four cells</b>, and every classification metric is a ratio of those cells.</p>
</header>

<section id="metrics-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Score, cut at a threshold, compare with the truth: <em>each row lands in one of four cells</em>.</p>
{cm1}
  <ul class="why">
    <li><b>TP</b> caught, <b>FN</b> missed, <b>FP</b> false alarm, <b>TN</b> rightly left alone. <code>confusion_matrix(y_true, y_pred)</code> puts actual classes on the rows, predicted on the columns.</li>
    <li>The model gives the score; the <b>threshold</b> is a separate choice on top of it — section 03.</li>
  </ul>
</section>

<section id="metrics-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Metrics from the cells</h2></div>
  <p class="key">Each metric picks <em>which cells go on top and which go underneath</em>.</p>
  <div class="subsec" id="metrics-s2-1">
    <h3 class="ssh"><b>2.1</b>Accuracy</h3>
    <p class="skey">The diagonal over everything: <em>what share of rows are right</em>.</p>
{eqacc}
{cm2}
    <ul class="why">
      <li>Counts TN like any other cell, so when negatives dominate it says little — section 04.</li>
    </ul>
  </div>
  <div class="subsec" id="metrics-s2-2">
    <h3 class="ssh"><b>2.2</b>Precision &amp; recall</h3>
    <p class="skey">Both put <em>TP on top</em>; they differ in what they divide by — a column or a row.</p>
    <div class="subsec" id="metrics-s2-2-1">
      <h3 class="ssh"><b>2.2.1</b>Precision</h3>
      <p class="skey">Down the <em>predicted-pos column</em>: of the rows I flagged, how many are truly pos.</p>
{eqprec}
{cm3}
      <ul class="why">
        <li>Pays for <b>false alarms</b> (FP): put it first when a wrong flag is expensive — blocking a real customer, spam-filtering a real email.</li>
      </ul>
    </div>
    <div class="subsec" id="metrics-s2-2-2">
      <h3 class="ssh"><b>2.2.2</b>Recall</h3>
      <p class="skey">Along the <em>actual-pos row</em>: of the truly pos rows, how many I caught.</p>
{eqrec}
{cm4}
      <ul class="why">
        <li>Pays for <b>misses</b> (FN): put it first when a miss is expensive — cancer screening, machine faults. Also called <b>sensitivity</b> or <b>TPR</b>.</li>
      </ul>
    </div>
  </div>
  <div class="subsec" id="metrics-s2-3">
    <h3 class="ssh"><b>2.3</b>Specificity</h3>
    <p class="skey">Recall for the negatives: along the <em>actual-neg row</em>, how many I left alone.</p>
{eqspec}
{cm5}
    <ul class="why">
      <li>Also <b>TNR</b>; <span class="mth">1 − specificity</span> is the <b>FPR</b>, the x-axis of the <a href="../roc-auc-pr/index.html">ROC curve</a>.</li>
      <li><b>Balanced accuracy</b> = (recall + specificity) / 2 weighs both classes equally.</li>
    </ul>
  </div>
  <div class="subsec" id="metrics-s2-4">
    <h3 class="ssh"><b>2.4</b>F1</h3>
    <p class="skey">One number for precision and recall: their <em>harmonic mean</em>, pulled toward the smaller one.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>F</var><sub>1</sub></span></span>
      <span class="op">=</span>
      <span class="t"><span><span class="frac"><i>2 <var>P</var> <var>R</var></i><i><var>P</var> + <var>R</var></i></span></span><em>harmonic mean</em></span>
      <span class="op">;</span>
      <span class="t p"><span><var>F</var><sub><var>β</var></sub> = <span class="frac"><i>(1 + <var>β</var><sup>2</sup>) <var>P</var> <var>R</var></i><i><var>β</var><sup>2</sup> <var>P</var> + <var>R</var></i></span></span><em>β = 2: recall counts double</em></span>
    </div>
  </div>
{cm6}
    <ul class="why">
      <li>A model that is great on one and useless on the other cannot hide behind a plain average.</li>
      <li>F1 still assumes an FP and an FN <b>cost the same</b> — rarely true; section 05 prices them instead.</li>
    </ul>
  </div>
</section>

<section id="metrics-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Threshold</h2></div>
  <p class="key">Raise the threshold and rows leave the predicted-pos column: <em>precision tends up, recall goes down</em>.</p>
{cm7}
  <ul class="why">
    <li>Recall can only fall as the threshold rises; precision usually rises but can dip, as from 0.6 to 0.35 here.</li>
    <li>0.5 is a library default, not a property of the model. Serve the <b>score</b> and keep the threshold in config.</li>
    <li>Tracing every threshold gives the <a href="../roc-auc-pr/index.html">ROC and PR curves</a>.</li>
  </ul>
</section>

<section id="metrics-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Imbalanced data</h2></div>
  <p class="key">When one class is rare, saying "no" to everyone scores <em>high accuracy and zero recall</em>.</p>
{cm8}
  <ul class="why">
    <li>Ask for the class ratio before reading any number: at 95 : 5 the floor for accuracy is already 0.95.</li>
    <li>Report precision, recall, PR-AUC or balanced accuracy instead; they never use TN as their only evidence.</li>
  </ul>
</section>

<section id="metrics-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Threshold by cost</h2></div>
  <p class="key">Price each error, <em>add up the bill at every threshold</em>, keep the cheapest.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">cost</b>(<var>t</var>)</span><em>bill at threshold t</em></span>
      <span class="op">=</span>
      <span class="t r"><span><var>c</var><sub>FP</sub> · #FP(<var>t</var>)</span><em>price of a false alarm × count</em></span>
      <span class="op">+</span>
      <span class="t p"><span><var>c</var><sub>FN</sub> · #FN(<var>t</var>)</span><em>price of a miss × count</em></span>
    </div>
  </div>
{cm9}
  <ul class="why">
    <li>A miss costing 3× a false alarm pushes the best threshold <b>below 0.5</b>, here to 0.175.</li>
    <li>The answer is in money; when prices change, re-pick the threshold — no retraining. Pick it on validation data, not test.</li>
  </ul>
</section>

<section id="metrics-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Multiclass</h2></div>
  <p class="key">K classes give a K × K matrix and <em>one precision, recall and F1 per class</em>.</p>
  <div class="subsec" id="metrics-s6-1">
    <h3 class="ssh"><b>6.1</b>K × K matrix</h3>
    <p class="skey">Row = actual class, column = predicted: <em>the diagonal is right</em>, everything else is a confusion.</p>
{cm10}
    <ul class="why">
      <li>For one class, its column minus the diagonal is FP, its row minus the diagonal is FN — one-vs-rest.</li>
      <li>Off-diagonal cells show <b>which</b> classes are mixed up: here every bird is called a cat.</li>
    </ul>
  </div>
  <div class="subsec" id="metrics-s6-2">
    <h3 class="ssh"><b>6.2</b>Averaging</h3>
    <p class="skey">Three per-class F1s become one number by <em>macro, weighted or micro</em> averaging.</p>
{cm11}
    <ul class="why">
      <li><b>macro</b> exposes the failing rare class (0.49); <b>weighted</b> and <b>micro</b> let the big classes hide it.</li>
      <li>For single-label tasks micro-F1 equals accuracy, so it inherits the flaw of section 04. Set with <code>average="macro"</code>.</li>
    </ul>
  </div>
</section>

<section id="metrics-s7" class="lesson">
  <div class="sh"><b>07</b><h2>Regression metrics</h2></div>
  <p class="key">The label is a number: every metric starts from the <em>residual</em> <span class="mth"><var>y</var> − <var>ŷ</var></span>.</p>
  <div class="subsec" id="metrics-s7-1">
    <h3 class="ssh"><b>7.1</b>MAE</h3>
    <p class="skey">Average <em>length</em> of the residuals, in the unit of <span class="mth"><var>y</var></span>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">MAE</b></span></span>
      <span class="op">=</span>
      <span class="t"><span><span class="frac"><i>1</i><i><var>n</var></i></span> Σ<sub><var>i</var></sub> |<var>y</var><sub><var>i</var></sub> − <var>ŷ</var><sub><var>i</var></sub>|</span><em>mean absolute residual</em></span>
    </div>
  </div>
{cm12}
    <ul class="why">
      <li>Every unit of error counts the same, so one outlier moves it only in proportion.</li>
      <li><b>MAPE</b> divides each residual by <span class="mth">|<var>y</var>|</span>: it explodes near <span class="mth"><var>y</var> = 0</span> and favours under-prediction.</li>
    </ul>
  </div>
  <div class="subsec" id="metrics-s7-2">
    <h3 class="ssh"><b>7.2</b>MSE &amp; RMSE</h3>
    <p class="skey">Average <em>area</em> of the residual squares; the root brings it back to the unit of <span class="mth"><var>y</var></span>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">MSE</b></span></span>
      <span class="op">=</span>
      <span class="t"><span><span class="frac"><i>1</i><i><var>n</var></i></span> Σ<sub><var>i</var></sub> (<var>y</var><sub><var>i</var></sub> − <var>ŷ</var><sub><var>i</var></sub>)<sup>2</sup></span><em>mean squared residual</em></span>
      <span class="op">;</span>
      <span class="t r"><span><b class="fn">RMSE</b> = √<b class="fn">MSE</b></span><em>same unit as y</em></span>
    </div>
  </div>
{cm13}
    <ul class="why">
      <li>Squaring makes one error of 8 weigh as much as 64 errors of 1: RMSE ≥ MAE, and the gap grows with outliers.</li>
      <li>MSE is the loss most regressors minimise; minimising it predicts the <b>mean</b>, minimising MAE the <b>median</b>.</li>
    </ul>
  </div>
  <div class="subsec" id="metrics-s7-3">
    <h3 class="ssh"><b>7.3</b>R²</h3>
    <p class="skey">Squared error of the model <em>against the squared error of always predicting the mean</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>R</var><sup>2</sup></span></span>
      <span class="op">=</span>
      <span class="t"><span>1 −</span></span>
      <span class="t r"><span><span class="frac"><i><b class="fn">SSE</b></i><i><b class="fn">SST</b></i></span></span><em>Σ(y − ŷ)² over Σ(y − ȳ)²</em></span>
    </div>
  </div>
{cm14}
    <ul class="why">
      <li>Unitless, but SST is the spread of <b>this</b> test set: do not compare R² across two datasets.</li>
      <li>It can be negative — the model is then worse than the constant <span class="mth"><var>ȳ</var></span>.</li>
    </ul>
  </div>
</section>

{script}

<footer>Machine learning · Model evaluation · read on: <a href="../roc-auc-pr/index.html">ROC-AUC &amp; PR curve</a>, then <a href="../calibration/index.html">Probability calibration</a>.</footer>
'''

def build():
    figs = dict(cm1=fig_mental(), cm2=fig_accuracy(), cm3=fig_precision(), cm4=fig_recall(), cm5=fig_specificity(),
                cm6=fig_f1(), cm7=fig_threshold(), cm8=fig_imbalance(), cm9=fig_cost(), cm10=fig_multi(),
                cm11=fig_average(), cm12=fig_mae(), cm13=fig_mse(), cm14=fig_r2(), script=SCRIPT,
                eqacc=eqf('accuracy', 'TP + TN', 'TP + FP + FN + TN', 'right rows over all rows'),
                eqprec=eqf('precision', 'TP', 'TP + FP', 'predicted-pos column', 'g'),
                eqrec=eqf('recall', 'TP', 'TP + FN', 'actual-pos row', 'b'),
                eqspec=eqf('specificity', 'TN', 'TN + FP', 'actual-neg row', 'b'))
    return re.sub(r'\{([a-z0-9]+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'A threshold sorts every prediction into four cells; accuracy, precision, recall, specificity and F1 '
           'are ratios of them, priced errors pick the threshold, and MAE, RMSE and R² do the same job for numbers.')
