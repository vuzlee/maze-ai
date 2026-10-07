# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/09-evaluation/calibration.
One held-out predictions table (20 rows: id, score, label) drives the core: bins -> reliability diagram ->
Brier / ECE -> Platt / isotonic -> a cost decision. A seeded 2,000-row toy set drives the "skewed by design"
figures. Every number in a figure is computed here and pinned with assert. Run: python3 calibration.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, finish)
from tablefig import GR, AM, RD, tint, pill
from decision_tree import splice
import linear_algebra as _la
_la.RGBA.setdefault(AM, '--amber-a'); _la.RGBA.setdefault(GR, '--green-a'); _la.RGBA.setdefault(RD, '--red-a')

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/09-evaluation/calibration/index.html')
sig = lambda z: 1 / (1 + math.exp(-z))
logit = lambda p: math.log(p / (1 - p))

# ---------- the held-out table, in score order ----------
SC = [.03, .07, .12, .16, .22, .26, .31, .36, .42, .47, .53, .58, .64, .69, .73, .78, .83, .88, .93, .97]
LB = [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1]
N = 20
ORD = list(range(N)); random.Random(7).shuffle(ORD)            # ORD[r] = sorted index of table row r
ID = {ORD[r]: str(r + 1) for r in range(N)}                     # id shown for sorted index
NB = 5
def binof(s): return min(int(s * NB), NB - 1)
BINS = [[i for i in range(N) if binof(SC[i]) == k] for k in range(NB)]
assert [len(b) for b in BINS] == [4] * 5 and all(BINS[k] == list(range(4 * k, 4 * k + 4)) for k in range(5))
MEAN = [sum(SC[i] for i in b) / 4 for b in BINS]
POS = [sum(LB[i] for i in b) for b in BINS]; RATE = [p / 4 for p in POS]
assert [round(m, 3) for m in MEAN] == [.095, .287, .5, .71, .902] and POS == [1, 1, 2, 3, 3]
GAP = [abs(m - r) for m, r in zip(MEAN, RATE)]
def ece(v):
    out = 0
    for k in range(NB):
        b = [i for i in range(N) if binof(v[i]) == k]
        if b: out += len(b) / N * abs(sum(v[i] for i in b) / len(b) - sum(LB[i] for i in b) / len(b))
    return out
ECE0 = ece(SC); assert round(ECE0, 3) == .077 and round(sum(GAP) / 5, 3) == .077
SQ = [(SC[i] - LB[i]) ** 2 for i in range(N)]
BRIER0 = sum(SQ) / N; assert round(BRIER0, 3) == .214

# ---------- Platt scaling (Newton on log loss) ----------
def platt(s, y):
    A, B = 1.0, 0.0
    for _ in range(60):
        gA = gB = hAA = hAB = hBB = 0
        for x, t in zip(s, y):
            p = sig(A * x + B); w = p * (1 - p)
            gA += (p - t) * x; gB += p - t; hAA += w * x * x; hAB += w * x; hBB += w
        d = hAA * hBB - hAB * hAB
        A -= (hBB * gA - hAB * gB) / d; B -= (-hAB * gA + hAA * gB) / d
    return A, B
PA, PB = platt(SC, LB)
PL = [sig(PA * s + PB) for s in SC]
assert (round(PA, 2), round(PB, 2)) == (3.18, -1.59)
assert (round(PL[0], 2), round(PL[-1], 2)) == (.18, .82)
ECEP = ece(PL); BRIERP = sum((p - y) ** 2 for p, y in zip(PL, LB)) / N
assert round(ECEP, 3) == .023 and round(BRIERP, 3) == .206

# ---------- isotonic regression by pool-adjacent-violators ----------
def pav(y):
    """returns the states after each merge: list of blocks [(start, end_exclusive, mean)]"""
    bl = [[i, i + 1, float(v)] for i, v in enumerate(y)]; states = []; i = 0
    while i < len(bl) - 1:
        if bl[i][2] > bl[i + 1][2] + 1e-12:
            a, b = bl[i], bl[i + 1]; n1, n2 = a[1] - a[0], b[1] - b[0]
            bl[i] = [a[0], b[1], (a[2] * n1 + b[2] * n2) / (n1 + n2)]; del bl[i + 1]
            states.append([tuple(x) for x in bl]); i = max(i - 1, 0)
        else: i += 1
    return states
PAV = pav(LB)
ISO_BL = PAV[-1]
ISO = [next(m for a, b, m in ISO_BL if a <= i < b) for i in range(N)]
assert all(ISO[i] <= ISO[i + 1] + 1e-12 for i in range(N - 1))
assert [(a, b, round(m, 2)) for a, b, m in ISO_BL] == [(0, 1, 0), (1, 2, 0), (2, 9, .29), (9, 14, .6), (14, 19, .8), (19, 20, 1)]
assert len(PAV) == 14
ECEI = ece(ISO); BRIERI = sum((p - y) ** 2 for p, y in zip(ISO, LB)) / N
assert round(ECEI, 3) == 0 and round(BRIERI, 3) == .171

# ---------- a cost decision: voucher costs 4, a buyer is worth 5 -> send if 5p > 4 ----------
COST, GAIN = 4, 5; CUT = COST / GAIN
def decide(v):
    sel = [i for i in range(N) if v[i] > CUT]
    return sel, sum(GAIN * v[i] - COST for i in sel), sum(GAIN * LB[i] - COST for i in sel)
DR, DP = decide(SC), decide(PL)
assert len(DR[0]) == 4 and round(DR[1], 2) == 2.05 and DR[2] == -1
assert len(DP[0]) == 1 and round(DP[1], 2) == .09 and DP[2] == 1
TOP5R = sorted(range(N), key=lambda i: -SC[i])[:5]; TOP5P = sorted(range(N), key=lambda i: -PL[i])[:5]
assert TOP5R == TOP5P

# ---------- toy set for "skewed by design" ----------
g = random.Random(11)
TOY = []
for _ in range(2000):
    p = .03 + .94 * g.random(); TOY.append((p, int(g.random() < p), [int(g.random() < .2 + .6 * p) for _ in range(10)]))
def toybins(score):
    out = []
    for k in range(NB):
        b = [r for r in TOY if binof(r[0]) == k]
        out.append((sum(r[0] for r in b) / len(b), sum(score(r) for r in b) / len(b), sum(r[1] for r in b) / len(b)))
    return out
MODELS = {
    'nb': toybins(lambda r: sig(3 * logit(r[0]))),
    'rf': toybins(lambda r: sum(r[2]) / 10),
    'svm': toybins(lambda r: .8 * logit(r[0])),
    'b1': toybins(lambda r: sig(1.4 * logit(r[0]))),
    'b2': toybins(lambda r: sig(2.2 * logit(r[0]))),
    'b3': toybins(lambda r: sig(3.2 * logit(r[0]))),
}
nb, rf, sv, b3 = MODELS['nb'], MODELS['rf'], MODELS['svm'], MODELS['b3']
assert nb[0][1] < nb[0][0] - .05 and nb[4][1] > nb[4][0] + .05           # pushed to the ends
assert rf[0][1] > rf[0][0] + .1 and rf[4][1] < rf[4][0] - .1             # pulled to the middle
assert sv[0][1] < 0 and sv[4][1] > 1                                     # margins leave [0, 1]
assert all(abs(r[2] - r[0]) < .04 for r in nb)                           # rates sit near the true p
MAXV = max(sum(r[2]) for r in TOY); MINV = min(sum(r[2]) for r in TOY)
SHARE01 = sum(sum(r[2]) in (0, 10) for r in TOY) / len(TOY)
assert round(SHARE01, 3) == .017 and round(sig(3 * logit(.75)), 2) == .96

# ---------- drawing helpers ----------
def tok(x, y, s, lab, w=34):
    c = FI if lab else BR
    fill = tn(FI, '.20') if lab else BG
    return R(x, y, w, 18, BG, 'none', 4) + R(x, y, w, 18, fill, c, 4, 1.3) + T(x + w / 2, y + 13, s, c, mono=True, bold=True)

def lab_dot(x, y, lab, r=5):
    if lab: return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, FI)
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, r - 1, BG, BR)

def f2(v): return ('%.2f' % v).replace('0.', '.', 1) if 0 <= v < 1 else '%.2f' % v

class Dia:
    """reliability-diagram frame: data in [lo, hi] on both axes"""
    def __init__(self, x0, y0, size, lo=0, hi=1):
        self.x0, self.y0, self.sz, self.lo, self.hi = x0, y0, size, lo, hi
    def X(self, v): return self.x0 + (v - self.lo) / (self.hi - self.lo) * self.sz
    def Y(self, v): return self.y0 + self.sz - (v - self.lo) / (self.hi - self.lo) * self.sz
    def frame(self, xl='mean score', yl='positive rate', diag=True):
        s = R(self.x0, self.y0, self.sz, self.sz, BG, RULE_HI, 2, 1)
        for k in range(1, 5):
            v = k / 5
            s += L(self.X(v), self.y0, self.X(v), self.y0 + self.sz, RULE, 1) + L(self.x0, self.Y(v), self.x0 + self.sz, self.Y(v), RULE, 1)
        for v in (0, .5, 1):
            s += T(self.X(v), self.y0 + self.sz + 14, '%g' % v, FA, mono=True)
            s += T(self.x0 - 6, self.Y(v) + 4, '%g' % v, FA, 'end', mono=True)
        s += S(self.x0 + self.sz / 2, self.y0 + self.sz + 30, xl, MU, 'middle')
        s += S(self.x0, self.y0 - 8, yl, MU, 'start')
        if diag:
            s += L(self.X(0), self.Y(0), self.X(1), self.Y(1), GR, 1.6, '6 4')
            s += T(self.X(.98), self.Y(1) + 16, 'perfect', GR, 'end', bold=True)
        return s

def pdot(x, y, c=AM, r=6):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, r, c, BG)

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('cal1-', 720, 0, 'A held-out table of 20 rows with an id, the model score and the true label. Each row sends a '
             'token with its score into one of five score bins, 0 to 0.2 up to 0.8 to 1; each bin gets four rows. Every bin '
             'then shows its mean score and the share of its rows that were really positive: 0.10 and 1 of 4, 0.29 and 1 of 4, '
             '0.51 and 2 of 4, 0.71 and 3 of 4, 0.90 and 3 of 4. Each bin becomes one point on the reliability diagram, x the '
             'mean score, y the positive rate. The dashed diagonal is perfect calibration; the low bins sit above it and the '
             'high bins below it: the model is too sure at both ends.',
             'ROWS → SCORE BINS → MEAN SCORE vs POSITIVE RATE → ONE POINT PER BIN')
    t = Table(0, 30, [('id', 30), ('score', 50), ('label', 46)], step=22, rh=19)
    f.static(t.head())
    for r in range(N):
        i = ORD[r]
        f.static(t.row(r, [str(r + 1), f2(SC[i]), str(LB[i])], colors={2: FI if LB[i] else BR}))
    BX0, BW = 160, 172; GX = 138
    by = lambda k: t.ry(4 * k)
    for k in range(NB):
        y = by(k)
        f.static(R(BX0, y, BW, 4 * 22 - 4, SUNK, RULE_HI, 6, 1) +
                 T(BX0 + 8, y + 14, '%.1f – %.1f' % (k / 5, (k + 1) / 5), MU, 'start', mono=True))
    fill = [0] * NB; t0 = .5; d = .16; stp = .52
    order = sorted(range(N), key=lambda r: r)        # table order: unsorted scores
    for q, r in enumerate(order):
        i = ORD[r]; k = binof(SC[i]); j = 3 - fill[k]; fill[k] += 1
        x0, y0 = t.colx(1) + 8, t.ry(r)
        sx, sy = BX0 + 8 + j * 40, by(k) + 22
        ts = t0 + q * stp
        f.path(tok(x0, y0, f2(SC[i]), LB[i]), [(0, 0, 0), (ts, GX - x0, 0), (ts + d, GX - x0, sy - y0),
                                                (ts + 2 * d, sx - x0, sy - y0)], ts - .25, d=d)
        f.show(t.outline(r, c=AM, sw=1.4), ts - .25, hide=ts + .45)
    ta = t0 + N * stp + .3
    D = Dia(420, 70, 270)
    f.static(D.frame())
    for k in range(NB):
        y = by(k) + 60
        f.show(T(BX0 + 8, y, 'mean ' + f2(MEAN[k]), AM, 'start', bold=True) +
               T(BX0 + BW - 8, y + 0, 'rate %d/4' % POS[k], FI, 'end', bold=True), ta + k * .25)
    tp = ta + 1.6
    for k in range(NB):
        x1, y1 = BX0 + BW + 4, by(k) + 44
        px, py = D.X(MEAN[k]), D.Y(RATE[k])
        f.path(pdot(x1, y1), [(0, 0, 0), (tp + k * .7, px - x1, py - y1)], tp + k * .7 - .3, d=.55)
    te = tp + NB * .7 + .2
    f.show(poly([(D.X(m), D.Y(r)) for m, r in zip(MEAN, RATE)], AM, 1.8), te)
    for k in range(NB):
        f.show(L(D.X(MEAN[k]), D.Y(MEAN[k]), D.X(MEAN[k]), D.Y(RATE[k]), RD, 2), te + .3)
    f.show(S(D.x0 + 8, D.Y(.9), 'above the line: under-confident', MU) + S(D.x0 + D.sz - 8, D.Y(.08), 'below the line: over-confident', MU, 'end'), te + .6)
    return finish(f, t.ry(N - 1) + 26)

# ---------- 2.1 Brier ----------
def fig_brier():
    f = Anim('cal2-', 720, 0, 'The same 20 rows in score order. For each row the gap between its score and its 0 or 1 label is '
             'squared and drawn as a bar: row 19 with score 0.93 and label 0 has the longest bar, 0.86. The 20 squares travel '
             'into a sum of 4.28, divided by 20 gives a Brier score of 0.214.',
             'EVERY ROW: (SCORE − LABEL)² · AVERAGE THEM')
    t = Table(0, 30, [('id', 30), ('score', 50), ('label', 46), ('(p − y)²', 60)], step=22, rh=19)
    f.static(t.head())
    for i in range(N):
        f.static(t.row(i, [ID[i], f2(SC[i]), str(LB[i]), ''], colors={2: FI if LB[i] else BR}))
    BX, sc = 210, 260
    f.static(L(BX, t.ry(0) - 4, BX, t.ry(N - 1) + 22, RULE_HI, 1))
    for i in range(N):
        y = t.ry(i); ts = .4 + i * .3
        f.show(R(BX, y + 3, max(SQ[i] * sc, 1.5), 13, tn(RO, '.28'), RO, 2, 1) +
               T(BX + SQ[i] * sc + 6, y + 14, f2(SQ[i]), MU, 'start', mono=True), ts)
        f.show(T(t.cx(3), y + 14, f2(SQ[i]), RO, mono=True), ts + .1)
    big = max(range(N), key=lambda i: SQ[i]); assert ID and SC[big] == .93 and round(SQ[big], 2) == .86
    f.show(t.outline(big, c=AM), 6.6)
    tot = sum(SQ); assert round(tot, 2) == 4.28
    f.show(R(560, 210, 150, 80, BG, AM, 8, 1.6) + T(635, 236, 'Σ = %.2f' % tot, TX, mono=True) +
           T(635, 256, '÷ 20', MU, mono=True) + T(635, 280, 'Brier %.3f' % BRIER0, AM, mono=True, bold=True), 7.2)
    f.show(S(560, 316, 'always 0.25 would score 0.25', MU), 7.8)
    return finish(f, t.ry(N - 1) + 26)

# ---------- 2.2 ECE ----------
def fig_ece():
    f = Anim('cal3-', 720, 0, 'The five bins from the mental model become points on the diagram. A red vertical gap is drawn '
             'from each point to the diagonal: 0.16, 0.04, 0, 0.04, 0.15. Each gap travels into the table, is weighted by '
             '4 of 20 rows, and the weighted sum is the ECE, 0.077.',
             'EACH BIN: |MEAN SCORE − POSITIVE RATE| · WEIGHT BY ITS SHARE OF ROWS')
    D = Dia(40, 40, 260)
    f.static(D.frame())
    t = Table(380, 40, [('bin', 64), ('n', 30), ('mean', 54), ('rate', 50), ('gap', 60)], step=30, rh=26)
    f.static(t.head())
    for k in range(NB):
        f.static(t.row(k, ['%.1f–%.1f' % (k / 5, (k + 1) / 5), '4', f2(MEAN[k]), '%d/4' % POS[k], ''],
                       colors={2: AM, 3: FI}))
        f.static(pdot(D.X(MEAN[k]), D.Y(RATE[k])))
    for k in range(NB):
        ts = .6 + k * 1.0
        x, y1, y2 = D.X(MEAN[k]), D.Y(MEAN[k]), D.Y(RATE[k])
        f.show(L(x, y1, x, y2, RD, 2.4), ts)
        f.show(t.outline(k, c=AM), ts, hide=ts + .95)
        lbl = T(x + 10, (y1 + y2) / 2 + 4, f2(GAP[k]), RD, 'start', mono=True, bold=True)
        tx, ty = t.cx(4), t.ry(k) + 17
        f.path(R(x + 6, (y1 + y2) / 2 - 9, 44, 18, BG, 'none', 3) + lbl,
               [(0, 0, 0), (ts + .4, tx - x - 22, ty - (y1 + y2) / 2 - 4)], ts + .1, d=.5)
    yb = t.ry(NB) + 30
    f.show(M(380, yb, '{ECE} = 4/20 · ( %s )' % ' + '.join(f2(g) for g in GAP), TX, 'start'), 6.0)
    f.show(chip(470, yb + 34, 'ECE %.3f' % ECE0, AM, 120), 6.6)
    assert [round(g, 3) for g in GAP] == [.155, .037, 0, .04, .152]
    return finish(f, max(yb + 50, D.y0 + D.sz + 40))

# ---------- 03 skewed by design ----------
SKEW = {
    'nb': ('cal4-', 'one feature counted three times → odds cubed', 'pushed to 0 and 1'),
    'rf': ('cal5-', 'share of 10 trees voting yes', 'pulled to the middle'),
    'b': ('cal7-', 'more rounds → sharper scores', 'pushed further each round'),
}
def fig_skew(key):
    if key == 'svm': return fig_svm()
    pre, mech, res = SKEW[key]
    f = Anim(pre, 720, 0, '', mech.upper() + ' · ' + res.upper())
    D = Dia(60, 44, 270)
    f.static(D.frame())
    stages = [MODELS['b1'], MODELS['b2'], MODELS['b3']] if key == 'b' else [MODELS[key]]
    base = stages[0]
    tags = ['sharpen ×1.4', 'sharpen ×2.2', 'sharpen ×3.2'] if key == 'b' else ['model']
    # start: a calibrated model would put each bin at its true p; then the model's scores slide the points sideways
    for k in range(NB):
        p, _, rate = base[k]
        pts = [(0, 0, 0)]
        for si, st in enumerate(stages):
            pts.append((1.6 + si * 1.8, D.X(st[k][1]) - D.X(p), 0))
        f.path(pdot(D.X(p), D.Y(rate)), pts, .3 + k * .15, d=.9)
        f.show('<circle cx="%.1f" cy="%.1f" r="5" fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="2 2"/>'
               % (D.X(p), D.Y(rate), FA), 1.4)
    for si, st in enumerate(stages):
        tt = 2.6 + si * 1.8; nxt = 2.6 + (si + 1) * 1.8 if si < len(stages) - 1 else None
        f.show(poly([(D.X(r[1]), D.Y(r[2])) for r in st], AM, 1.6), tt, hide=nxt - .5 if nxt else None)
        if key == 'b':
            f.show(chip(450, 110, tags[si], AM, 110), tt - 1.0, hide=(tt + .8) if si < len(stages) - 1 else None)
    # right: the mechanism in numbers, one row per bin
    tx = 380
    t = Table(tx, 160 if key == 'b' else 60, [('true p', 64), ('score', 64), ('rate', 64)], step=26, rh=22)
    f.static(t.head())
    last = stages[-1]
    for k in range(NB):
        f.show(t.row(k, [f2(last[k][0]), f2(last[k][1]), f2(last[k][2])], colors={1: AM, 2: FI}), 1.0 + k * .12)
    if key == 'nb':
        f.show(S(tx, t.ry(NB) + 24, 'true odds 3 : 1 → model sees 27 : 1', MU) +
               S(tx, t.ry(NB) + 42, 'p 0.75 → score %.2f' % sig(3 * logit(.75)), AM, bold=True), 4.2)
    if key == 'rf':
        f.show(S(tx, t.ry(NB) + 24, 'score 0 or 1 needs all 10 trees to agree', MU) +
               S(tx, t.ry(NB) + 42, 'rows with 0 or 10 votes: %.1f%%' % (100 * SHARE01), AM, bold=True), 4.2)
    if key == 'b':
        f.show(S(tx, t.ry(NB) + 24, 'labels do not change; only the scores spread', MU), 6.8)
    f.aria = {'nb': 'Five bins of a 2,000-row set start on the diagonal, where a calibrated model would put them. Naive Bayes '
                    'counts one feature three times, so it cubes the odds: the low bins slide left toward 0 and the high bins '
                    'right toward 1, while the real positive rate stays put. A true 0.75 becomes a score of 0.96.',
              'rf': 'Five bins start on the diagonal. A random forest score is the share of 10 trees voting yes, and the trees '
                    'rarely agree, so the low bins slide right and the high bins left, toward the middle: an S on its side.',
              'b': 'Five bins start on the diagonal. The scores are sharpened in three stages, as more boosting rounds would do and the '
                   'points slide further toward 0 and 1 at every stage, while the real positive rates do not move.'}[key]
    f.static(S(720, D.y0 + D.sz + 56, NOTE, FA, 'end'))
    return finish(f, D.y0 + D.sz + 62)

NOTE = 'illustration: scores reshaped by the mechanism, not a trained model'

def fig_svm():
    f = Anim('cal6-', 720, 0, 'Five bins start on the diagonal of the reliability diagram. An SVM outputs a signed distance '
             'to its boundary, so the points drop down onto a margin axis that runs from about minus 1.8 to plus 1.7: the two '
             'outer bins land outside the 0 to 1 range entirely. The numbers are distances, not probabilities.',
             'SVM SCORE = SIGNED DISTANCE TO THE BOUNDARY · NOT ON A 0–1 SCALE')
    D = Dia(60, 44, 200)
    f.static(D.frame())
    ay = D.y0 + D.sz + 74; lo, hi = -3, 3
    AX = lambda v: 40 + (v - lo) / (hi - lo) * 640
    s = L(AX(lo), ay, AX(hi), ay, RULE_HI, 1.4)
    for v in range(lo, hi + 1):
        s += L(AX(v), ay - 4, AX(v), ay + 4, RULE_HI, 1) + T(AX(v), ay + 18, '%+d' % v if v else '0', FA, mono=True)
    s += R(AX(0), ay - 10, AX(1) - AX(0), 20, tint('gr', '.10'), GR, 3, 1, '3 2') + T((AX(0) + AX(1)) / 2, ay - 14, '0 – 1', GR)
    s += S(AX(hi), ay + 36, 'margin w·x + b', MU, 'end')
    f.static(s)
    for k in range(NB):
        p, m, rate = sv[k]
        x0, y0 = D.X(p), D.Y(rate)
        f.path(pdot(x0, y0), [(0, 0, 0), (1.4 + k * .5, AX(m) - x0, ay - y0)], .3 + k * .1, d=.8)
        f.show(T(AX(m), ay - 26, ('%+.1f' % m).replace('-0.0', '0.0'), AM, mono=True, bold=True), 2.3 + k * .5)
    t = Table(330, 44, [('true p', 64), ('margin', 64), ('rate', 64)], step=24, rh=20)
    f.static(t.head())
    for k in range(NB):
        f.show(t.row(k, [f2(sv[k][0]), '%+.2f' % sv[k][1], f2(sv[k][2])], colors={1: AM, 2: FI}), .6 + k * .1)
    f.show(S(560, 80, 'ordered well,', MU) + S(560, 98, 'but no 0–1 meaning', MU) + S(560, 124, '→ Platt maps it', AM, bold=True), 5.2)
    f.static(S(720, ay + 56, NOTE, FA, 'end'))
    return finish(f, ay + 62)

# ---------- 4.x fixes ----------
def fit_frame(f, P):
    s = R(P['x0'], P['y0'], P['w'], P['h'], BG, RULE_HI, 2, 1)
    for v in (0, .5, 1):
        s += L(P['x0'], P['Y'](v), P['x0'] + P['w'], P['Y'](v), RULE, 1) + T(P['x0'] - 6, P['Y'](v) + 4, '%g' % v, FA, 'end', mono=True)
        s += T(P['X'](v), P['y0'] + P['h'] + 14, '%g' % v, FA, mono=True)
    s += S(P['x0'] + P['w'] / 2, P['y0'] + P['h'] + 30, 'raw score', MU, 'middle') + S(P['x0'], P['y0'] - 8, 'calibrated probability', MU)
    f.static(s)

def mkP(x0=50, y0=40, w=400, h=240):
    return dict(x0=x0, y0=y0, w=w, h=h, X=lambda v: x0 + v * w, Y=lambda v: y0 + h - v * h)

def side_chips(f, t, new, ece_new, brier_new, x=520):
    f.show(S(x, 70, 'same 5 bins, re-scored', MU), t)
    f.show(chip(x + 70, 100, 'ECE %.3f' % ECE0, RD, 130), t + .2, hide=t + 1.2)
    f.show(chip(x + 70, 100, 'ECE %.3f' % ece_new, GR, 130), t + 1.2)
    f.show(chip(x + 70, 136, 'Brier %.3f' % brier_new, GR, 130), t + 1.4)
    f.show(S(x, 170, 'order unchanged', MU) + S(x, 188, '→ AUC unchanged', MU), t + 1.8)

def fig_platt():
    f = Anim('cal8-', 720, 0, 'The 20 held-out rows sit at their raw score, positives on the line at 1 and negatives on the '
             'line at 0. A sigmoid with A 3.18 and B minus 1.59 is fitted to them by log loss and drawn. Every row then rises '
             'or falls onto the curve: its calibrated probability, from 0.18 for the lowest score to 0.82 for the highest. '
             'Re-scored with the same bins, ECE drops from 0.077 to 0.023.',
             'FIT ONE SIGMOID ON HELD-OUT SCORES · EVERY ROW MOVES ONTO IT')
    P = mkP(); fit_frame(f, P)
    for i in range(N):
        x = P['X'](SC[i]); y = P['Y'](LB[i])
        f.path(lab_dot(x, y, LB[i]), [(0, 0, 0), (2.4 + i * .12, 0, P['Y'](PL[i]) - y)], .2 + i * .04, d=.6)
    curve = [(P['X'](v / 100), P['Y'](sig(PA * v / 100 + PB))) for v in range(0, 101, 2)]
    f.show(poly(curve, AM, 2.2), 1.3)
    f.show(M(P['x0'] + 12, P['y0'] + 24, '{p} = σ( 3.18 {s} − 1.59 )', AM, 'start'), 1.6)
    side_chips(f, 5.4, PL, ECEP, BRIERP)
    return finish(f, P['y0'] + P['h'] + 44)

def fig_iso():
    f = Anim('cal9-', 720, 0, 'The same 20 rows on the same axes. Pool adjacent violators walks them in score order: whenever a '
             'row sits higher than the row after it, the two pool into one block at their average, and a block keeps pooling '
             'backwards while it is still higher than the block before it. After %d merges the blocks only go up: a step '
             'function. Re-scored with the same bins, ECE on these rows becomes %.3f — it fits these exact rows.' % (len(PAV), ECEI),
             'POOL ADJACENT VIOLATORS · MERGE UNTIL EVERY STEP GOES UP')
    P = mkP(); fit_frame(f, P)
    dt = .85; t0 = 1.0
    val = [float(v) for v in LB]
    tracks = [[(0, 0, 0)] for _ in range(N)]
    for si, st in enumerate(PAV):
        ts = t0 + si * dt
        for a, b, m in st:
            for i in range(a, b):
                if abs(m - val[i]) > 1e-9:
                    tracks[i].append((ts, 0, P['Y'](m) - P['Y'](LB[i]))); val[i] = m
    prev = [(i, i + 1, float(LB[i])) for i in range(N)]
    for si, st in enumerate(PAV):
        ts = t0 + si * dt
        new = [blk for blk in st if blk not in prev]
        for a, b, m in new:
            x1, x2 = P['X'](SC[a]) - 8, P['X'](SC[b - 1]) + 8
            f.show(R(x1, P['Y'](m) - 9, x2 - x1, 18, 'none', RD, 9, 1.4), ts + .38, hide=ts + dt - .05, d=.12)
        prev = st
    for i in range(N):
        f.path(lab_dot(P['X'](SC[i]), P['Y'](LB[i]), LB[i]), tracks[i], .2 + i * .04, d=.35)
    te = t0 + len(PAV) * dt + .2
    steps = []
    for a, b, m in ISO_BL:
        xa = P['X'](SC[a - 1] / 2 + SC[a] / 2) if a else P['x0']
        xb = P['X'](SC[b - 1] / 2 + SC[b] / 2) if b < N else P['x0'] + P['w']
        if steps: steps.append((xa, steps[-1][1]))
        steps += [(xa, P['Y'](m)), (xb, P['Y'](m))]
    f.show(poly(steps, AM, 2.2), te)
    f.show(T(P['x0'] + 12, P['y0'] + 22, '%d blocks · %d merges' % (len(ISO_BL), len(PAV)), AM, 'start', bold=True), te + .2)
    side_chips(f, te + .6, ISO, ECEI, BRIERI)
    f.show(S(520, 222, '0 on the rows it was fit on:', RD) + S(520, 240, 'measure it on other rows', RD), te + 2.6)
    return finish(f, P['y0'] + P['h'] + 44)

# ---------- 05 when it is needed ----------
def fig_cost():
    f = Anim('cal10-', 720, 0, 'The 20 rows sorted by score, with the raw score and the Platt probability side by side. A '
             'voucher costs 4 and a buyer is worth 5, so send it when 5 p is above 4, that is p above 0.8. On raw scores 4 '
             'rows clear the line; the model promises a profit of 2.05, but only 3 of them buy, a real result of minus 1. On '
             'calibrated probabilities 1 row clears it, promises 0.09 and really earns 1. The top-5 rows are the same in both '
             'columns, so a ranking-only use would not notice any difference.',
             'SEND IF 5 · p > 4 · RAW SCORES OVERPROMISE · THE TOP 5 IS THE SAME EITHER WAY')
    order = sorted(range(N), key=lambda i: -SC[i])[:10]
    t = Table(0, 30, [('id', 30), ('raw', 54), ('Platt', 54), ('label', 46)], step=24, rh=20)
    f.static(t.head())
    for r, i in enumerate(order):
        f.static(t.row(r, [ID[i], f2(SC[i]), f2(PL[i]), str(LB[i])], colors={3: FI if LB[i] else BR}))
    f.static(T(t.x + t.w / 2, t.ry(10) + 14, '… 10 lower rows', FA))
    def cutline(j, n, c):
        y = t.ry(n) - 3
        return L(t.colx(j) + 2, y, t.colx(j) + t.cols[j][1] - 2, y, c, 2.2)
    nR, nP = len(DR[0]), len(DP[0])
    f.show(t.colbox(1, nR, AM, head=False) + cutline(1, nR, AM), .8)
    f.show(T(t.colx(1) + 27, t.ry(nR) + 15, '> 0.8', AM, bold=True).replace('y="', 'y="', 1), .9, hide=3.6)
    xR = 300
    f.show(S(xR, 50, 'raw scores · %d sent' % nR, AM, bold=True), 1.0)
    f.show(S(xR, 74, 'promised  Σ(5p − 4) = %+.2f' % DR[1], MU), 1.5)
    for k, i in enumerate(DR[0]):
        r = order.index(i)
        f.show(t.outline(r, r, 3, 3, c=GR if LB[i] else RD), 2.0 + k * .3)
    f.show(S(xR, 98, 'real  5 · %d buyers − 4 · %d = ' % (sum(LB[i] for i in DR[0]), nR), MU) +
           pill(xR + 160, 85, '%+d' % DR[2], 'rd', 40), 3.4)
    f.show(t.colbox(2, nP, AM, head=False) + cutline(2, nP, AM), 4.2)
    f.show(S(xR, 140, 'Platt probabilities · %d sent' % nP, AM, bold=True), 4.4)
    f.show(S(xR, 164, 'promised  %+.2f' % DP[1], MU), 4.8)
    f.show(S(xR, 188, 'real  5 · %d − 4 · %d = ' % (sum(LB[i] for i in DP[0]), nP), MU) + pill(xR + 160, 175, '%+d' % DP[2], 'gr', 40), 5.3)
    f.show(R(-4, t.ry(0) - 4, t.w + 8, t.ry(4) + 24 - t.ry(0) + 6, 'none', VI, 6, 1.6, '5 3'), 6.3)
    f.show(S(xR, 236, 'top 5 by raw = top 5 by Platt', VI, bold=True) +
           S(xR, 256, 'ranking only (call the top k): no calibration needed', MU), 6.6)
    return finish(f, t.ry(10) + 26)

BODY = '''<header class="hero">
  <p class="eyebrow">Machine learning · Model evaluation</p>
  <h1>Probability <em>calibration</em></h1>
  <p class="lede">A model is calibrated when, of all the rows it scores 0.7, about 70% really are positive — and many models that rank well are not.</p>
</header>

<section id="cal-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Bin the rows by score; in each bin compare the <em>mean score</em> with the <em>share really positive</em>.</p>
{c1}
  <ul class="why">
    <li>That plot is the <b>reliability diagram</b>; on the diagonal the score means what it says.</li>
    <li>Below the diagonal the model is over-confident, above it under-confident. This model is both, at opposite ends.</li>
    <li>It is a third question after <a href="../metrics-confusion-matrix/index.html">is the decision right</a> and <a href="../roc-auc-pr/index.html">is the ranking right</a>: AUC only sees order, so it cannot see this.</li>
  </ul>
</section>

<section id="cal-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Scores for calibration</h2></div>
  <p class="key">Two numbers summarise the diagram, both computed from the same 20 rows.</p>
  <div class="subsec" id="cal-s2-1">
    <h3 class="ssh"><b>2.1</b>Brier score</h3>
    <p class="skey">The mean squared gap between each <em>score</em> and its <em>0/1 label</em>; lower is better.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">Brier</b></span><em>per-row squared error</em></span>
      <span class="op">=</span>
      <span class="t"><span><span class="frac"><i>1</i><i><var>n</var></i></span> Σ<sub><var>i</var></sub> (<var>p</var><sub><var>i</var></sub> − <var>y</var><sub><var>i</var></sub>)<sup>2</sup></span><em>score minus label, squared</em></span>
    </div>
  </div>
{c2}
    <ul class="why">
      <li>No bins needed. It mixes calibration with how well the model separates, so a sharper model also lowers it.</li>
      <li><code>brier_score_loss</code> in scikit-learn; log loss is its sibling with a harsher penalty on confident mistakes.</li>
    </ul>
  </div>
  <div class="subsec" id="cal-s2-2">
    <h3 class="ssh"><b>2.2</b>ECE</h3>
    <p class="skey">Expected calibration error: each bin's <em>gap to the diagonal</em>, weighted by its share of rows.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">ECE</b></span><em>pure calibration</em></span>
      <span class="op">=</span>
      <span class="t"><span>Σ<sub><var>b</var></sub> <span class="frac"><i><var>n</var><sub><var>b</var></sub></i><i><var>n</var></i></span></span><em>share of rows in bin b</em></span>
      <span class="op">·</span>
      <span class="t r"><span>| <span class="mth">mean</span><sub><var>b</var></sub> − <span class="mth">rate</span><sub><var>b</var></sub> |</span><em>gap to the diagonal</em></span>
    </div>
  </div>
{c3}
    <ul class="why">
      <li>The value depends on the bins: few rows per bin make it noisy, so with little data use equal-count bins.</li>
      <li><code>calibration_curve</code> returns the points of the diagram; ECE is the weighted sum of their gaps.</li>
    </ul>
  </div>
</section>

<section id="cal-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Skewed by design</h2></div>
  <p class="key">The skew is predictable from how a model makes its score; <a href="../../05-classical-ml/logistic-regression/index.html">logistic regression</a> trains on log loss and comes out close to the diagonal.</p>
  <div class="subsec" id="cal-s3-1">
    <h3 class="ssh"><b>3.1</b>Naive Bayes</h3>
    <p class="skey">Correlated features are counted as independent evidence, so scores are <em>pushed to 0 and 1</em>.</p>
{c4}
    <ul class="why">
      <li>Each copy of the same evidence multiplies the odds again — see <a href="../../05-classical-ml/naive-bayes/index.html">Naive Bayes</a>.</li>
    </ul>
  </div>
  <div class="subsec" id="cal-s3-2">
    <h3 class="ssh"><b>3.2</b>Random forest</h3>
    <p class="skey">The score is a vote share, and trees rarely all agree, so scores are <em>pulled to the middle</em>.</p>
{c5}
    <ul class="why">
      <li>Bagging averages away the extremes — see <a href="../../06-tree-models/random-forest/index.html">Random forest</a>.</li>
    </ul>
  </div>
  <div class="subsec" id="cal-s3-3">
    <h3 class="ssh"><b>3.3</b>SVM</h3>
    <p class="skey">The output is a <em>distance to the boundary</em>, not a probability at all.</p>
{c6}
    <ul class="why">
      <li><code>SVC(probability=True)</code> runs Platt scaling internally — see <a href="../../05-classical-ml/svm/index.html">SVM</a>.</li>
    </ul>
  </div>
  <div class="subsec" id="cal-s3-4">
    <h3 class="ssh"><b>3.4</b>Boosting &amp; deep nets</h3>
    <p class="skey">Training keeps pushing the loss down on the training rows, so scores get <em>sharper than the truth</em>.</p>
{c7}
    <ul class="why">
      <li>Boosting adds trees that keep moving the score away from 0.5; long-trained neural nets do the same, saying 0.99 when the truth is 0.8.</li>
    </ul>
  </div>
</section>

<section id="cal-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Fixing it</h2></div>
  <p class="key">Learn a <em>monotonic map</em> from old score to new probability; order is kept, so AUC does not change.</p>
  <div class="subsec" id="cal-s4-1">
    <h3 class="ssh"><b>4.1</b>Platt scaling</h3>
    <p class="skey">Fit <em>one sigmoid</em> on held-out scores; two parameters.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>p</var></span><em>calibrated</em></span>
      <span class="op">=</span>
      <span class="t b"><span><var>σ</var>( <var>A</var> <var>s</var> + <var>B</var> )</span><em>A, B fit by log loss on held-out rows</em></span>
    </div>
  </div>
{c8}
    <ul class="why">
      <li>Two numbers: a few hundred rows are enough. It can only fix an S-shaped skew — right for SVM and over-confident models.</li>
    </ul>
  </div>
  <div class="subsec" id="cal-s4-2">
    <h3 class="ssh"><b>4.2</b>Isotonic regression</h3>
    <p class="skey">Fit the best <em>non-decreasing step function</em>; any monotonic skew.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">min</b><sub><var>f</var></sub> Σ<sub><var>i</var></sub> (<var>y</var><sub><var>i</var></sub> − <var>f</var>(<var>s</var><sub><var>i</var></sub>))<sup>2</sup></span><em>squared error</em></span>
      <span class="op">,</span>
      <span class="t"><span><var>f</var> non-decreasing</span><em>never goes down</em></span>
    </div>
  </div>
{c9}
    <ul class="why">
      <li>One step per pooled block: it bends to any shape, and with under ~1,000 rows it fits their noise — prefer Platt then.</li>
    </ul>
  </div>
  <ul class="why">
    <li>Always fit the map on rows the model did not train on: on training rows it relearns the same over-confidence. <code>CalibratedClassifierCV(method="sigmoid" | "isotonic")</code> does this with cross-validation.</li>
  </ul>
</section>

<section id="cal-s5" class="lesson">
  <div class="sh"><b>05</b><h2>When it is needed</h2></div>
  <p class="key">Calibrate when the <em>number itself</em> feeds a decision; if only the order is used, skip it.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">act if</b> <var>p</var> · <span class="mth">gain</span></span><em>expected value</em></span>
      <span class="op">&gt;</span>
      <span class="t"><span><span class="mth">cost</span></span><em>here 5 · p &gt; 4</em></span>
    </div>
  </div>
{c10}
  <ul class="why">
    <li>Expected cost, thresholds set from money, risk scores shown to people, inputs to another model: calibrate.</li>
    <li>Top-k lists and AUC: the order is all that is used, and calibration never changes it.</li>
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

<footer>Machine learning · Model evaluation · the third axis, after the <a href="../metrics-confusion-matrix/index.html">confusion matrix</a> and <a href="../roc-auc-pr/index.html">ROC-AUC &amp; PR curve</a>.</footer>
'''

def build():
    figs = dict(c1=fig_mental(), c2=fig_brier(), c3=fig_ece(), c4=fig_skew('nb'), c5=fig_skew('rf'), c6=fig_svm(),
                c7=fig_skew('b'), c8=fig_platt(), c9=fig_iso(), c10=fig_cost())
    return re.sub(r'\{(c\d+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    if '-n' in sys.argv:
        print(ECE0, BRIER0, PA, PB, ECEP, BRIERP, ECEI, BRIERI, len(PAV), ISO_BL, DR, DP, SHARE01)
        for k, v in MODELS.items(): print(k, [tuple(round(x, 3) for x in r) for r in v])
        sys.exit()
    splice(PAGE, build(), 'Bin the predictions, compare mean score with the real positive rate on a reliability diagram, '
           'score it with Brier and ECE, and fix skewed models with Platt scaling or isotonic regression.')
