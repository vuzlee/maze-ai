# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/09-evaluation/evaluation-overview.
One predictions table (10 rows: id, true label y, model score) drives every figure: sorted for the ranking
question (ROC-AUC), cut at a threshold for the decision question (confusion matrix), binned for the probability
question (reliability). Every number is computed here. Run: python3 evaluation_overview.py"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import decision_tree as dt
from decision_tree import qbox, qring, HL
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RULE, SUNK, BG,
                            tn, M, S, dot, poly, finish)
from tablefig import GR, AM, RD, tint, pill

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/09-evaluation/evaluation-overview/index.html')

# ---------- the predictions table ----------
DATA = [('A', 0, .80), ('B', 0, .35), ('C', 1, .95), ('D', 0, .15), ('E', 1, .70),
        ('F', 0, .55), ('G', 0, .05), ('H', 1, .45), ('I', 1, .85), ('J', 0, .25)]
N = len(DATA); NP = sum(r[1] for r in DATA); NN = N - NP
CY = {1: FI, 0: BR}
SRT = sorted(range(N), key=lambda i: -DATA[i][2])          # table index by rank
RANK = {i: k for k, i in enumerate(SRT)}
THR = .5

def auc(sc):
    w = sum((sc[i] > sc[j]) + .5 * (sc[i] == sc[j]) for i in range(N) for j in range(N)
            if DATA[i][1] == 1 and DATA[j][1] == 0)
    return w, w / (NP * NN)

def conf(sc, t=THR):
    c = dict(TP=0, FP=0, FN=0, TN=0)
    for (_, y, _), s in zip(DATA, sc):
        c[('T' if (s >= t) == y else 'F') + ('P' if s >= t else 'N')] += 1
    return c

def bins(sc):
    out = []
    for lo, hi in ((0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1.01)):
        idx = [i for i in range(N) if lo <= sc[i] < hi]
        out.append((idx, sum(sc[i] for i in idx) / len(idx), sum(DATA[i][1] for i in idx) / len(idx)))
    return out

def ece(sc):
    return sum(len(b[0]) / N * abs(b[1] - b[2]) for b in bins(sc))

SC = [r[2] for r in DATA]; SQ = [round(s * s, 2) for s in SC]
W, AUC = auc(SC); C = conf(SC); P = C['TP'] / (C['TP'] + C['FP']); RC = C['TP'] / (C['TP'] + C['FN'])
B = bins(SC); E1 = ece(SC)
assert (W, NP, NN) == (21, 4, 6) and abs(AUC - .875) < 1e-9
assert C == dict(TP=3, FP=2, FN=1, TN=4) and abs(P - .6) < 1e-9 and abs(RC - .75) < 1e-9
assert [len(b[0]) for b in B] == [3, 3, 4] and abs(E1 - .110) < 1e-6
W2, AUC2 = auc(SQ); C2 = conf(SQ); P2 = C2['TP'] / (C2['TP'] + C2['FP']); R2 = C2['TP'] / (C2['TP'] + C2['FN']); E2 = ece(SQ)
assert AUC2 == AUC and C2 == dict(TP=2, FP=1, FN=2, TN=5) and abs(E2 - .081) < 1e-6

TONE = {AM: 'am', RD: 'rd', GR: 'gr'}
def chip(cx, cy, txt, c=VI, w=None):
    """chip in any colour: semantic ones via tint(), figure accents via tn()"""
    w = w or 16 + len(txt) * 7.2
    fill = tint(TONE[c], '.16') if c in TONE else tn(c, '.14')
    return (R(cx - w / 2, cy - 11, w, 22, BG, 'none', 11) + R(cx - w / 2, cy - 11, w, 22, fill, c, 11, 1.3) +
            T(cx, cy + 4.5, txt, c, mono=True, bold=True))

def f2(v): return ('%.2f' % v).lstrip('0') if v < 1 else '1'
def f3(v): return ('%.3f' % v).lstrip('0')

COLS = [('id', 34), ('y', 34, 'true'), ('score', 56, 'model')]
def table(x=0, y=44): return Table(x, y, COLS)
def rowsvg(t, i, sc=None):
    r = DATA[i]
    return t.row(i, [r[0], str(r[1]), f2(r[2] if sc is None else sc[i])], colors={1: CY[r[1]]})

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('ev1-', 720, 0, 'The ten-row predictions table. A second score column, the score squared, fills in row by row. '
             'Then three results are computed for both columns: ROC-AUC stays 0.875, precision and recall at threshold 0.5 '
             'change, and calibration error changes.', 'ONE TABLE · THREE QUESTIONS · CHANGE THE SCORES, SEE WHICH ANSWER MOVES')
    t = Table(0, 30, COLS + [('score²', 60, 'same order')])
    f.static(t.head())
    for i in range(N):
        r = DATA[i]
        f.static(t.row(i, [r[0], str(r[1]), f2(r[2]), ''], colors={1: CY[r[1]]}))
        f.show(t.cell(i, 3, f2(SQ[i]), c=VI), .4 + i * .12)
    f.show(t.colbox(3, N, VI), .3, hide=1.8)
    X0 = 260; rt = Table(X0, 30, [('question', 150, 'what of the score it uses'), ('score', 90), ('score²', 90)])
    f.show(rt.head(), 1.9)
    res = [('ranking', 'order only', 'ROC-AUC', f3(AUC), f3(AUC), GR),
           ('decision', 'one cut at .5', 'P · R', '%s · %s' % (f2(P), f2(RC)), '%s · %s' % (f2(P2), f2(R2)), RD),
           ('probability', 'the value', 'ECE', f3(E1), f3(E2), RD)]
    for k, (q, use, m, a, b, c) in enumerate(res):
        y = rt.ry(2 * k)
        t0 = 2.3 + k * 1.1
        f.show(R(X0, y, rt.w, 56, BG, RULE_HI, 3) + T(rt.cx(0), y + 20, q, TX, bold=True) + T(rt.cx(0), y + 38, use, MU) +
               T(rt.cx(1), y + 48, m, FA) + T(rt.cx(2), y + 48, m, FA), t0)
        f.show(T(rt.cx(1), y + 26, a, TX, mono=True, bold=True), t0 + .3)
        f.show(T(rt.cx(2), y + 26, b, c, mono=True, bold=True), t0 + .6)
    yb = rt.ry(6)
    f.show(S(X0, yb + 14, 'squaring keeps the order, so ranking cannot see it;', GR, 'start', True), 5.8)
    f.show(S(X0, yb + 32, 'the cut and the probabilities both move', RD, 'start', True), 6.2)
    return finish(f, max(t.bottom(N), yb + 40) + 8)

# shared stage for 2.x: unsorted table on the left, rows glide to a new arrangement at X1
X1, STEP = 150, 30
def stage(f, pre_hold=.2):
    t = table(); t2 = table(X1)
    f.show(t.head(), 0, hide=3.4, d=.01)
    return t, t2

# ---------- 2.1 Ranking ----------
def fig_rank():
    f = Anim('ev2-', 720, 0, 'The ten rows glide into score order. An amber box walks down the sorted list: every true-1 row '
             'steps the ROC curve up, every true-0 row steps it right. The area under the staircase is 21 of 24 cells, '
             'ROC-AUC 0.875.', 'SORT BY SCORE · WALK DOWN · EACH 1 STEPS UP, EACH 0 STEPS RIGHT')
    t, t2 = stage(f)
    f.show(t2.head() + T(t2.x + t2.w / 2, 36, 'sorted', MU), .9)
    for i in range(N):
        f.path(rowsvg(t, i), [(0, 0, 0), (.4 + .3 * RANK[i], X1, (RANK[i] - i) * STEP)], .05, d=.3)
    PX, PY, S_ = 380, 290, 240
    def P_(fx, ty): return (PX + fx * S_, PY - ty * S_)
    grid = ''
    for k in range(NN + 1): grid += L(PX + k * S_ / NN, PY, PX + k * S_ / NN, PY - S_, RULE, 1)
    for k in range(NP + 1): grid += L(PX, PY - k * S_ / NP, PX + S_, PY - k * S_ / NP, RULE, 1)
    f.show(grid + L(PX, PY, PX + S_, PY, RULE_HI, 1.3) + L(PX, PY, PX, PY - S_, RULE_HI, 1.3) +
           L(PX, PY, PX + S_, PY - S_, FA, 1, '4 4') +
           S(PX + S_ / 2, PY + 20, 'false-positive rate · 0s passed', MU, 'middle') +
           S(PX - 10, PY - S_ - 10, 'true-positive rate · 1s passed', MU, 'start') +
           T(PX - 6, PY + 4, '0', FA, 'end') + T(PX - 6, PY - S_ + 4, '1', FA, 'end') + T(PX + S_, PY + 15, '1', FA), 3.6)
    t0 = 4.0; dtk = .55; fx = ty = 0; pts = [P_(0, 0)]; area = []
    box = R(X1 - 3, t2.ry(0) - 3, t2.w + 6, t2.rh + 6, 'none', AM, 4, 1.8)
    f.path(box, [(0, 0, 0)] + [(t0 + k * dtk, 0, k * STEP) for k in range(1, N)], t0 - .2, d=.3, hide=t0 + N * dtk)
    for k, i in enumerate(SRT):
        y = DATA[i][1]; tk = t0 + k * dtk + .25
        a = P_(fx, ty)
        if y: ty += 1 / NP
        else:
            fx += 1 / NN
            area.append(ty)
        b = P_(fx, ty); pts.append(b)
        if not y and ty > 0:
            f.show(R(a[0], b[1], b[0] - a[0], PY - b[1], tn(FI, '.12'), 'none', 0), tk)
        f.show(L(a[0], a[1], b[0], b[1], CY[y], 3), tk)
    assert abs(sum(area) / NN - AUC) < 1e-9
    te = t0 + N * dtk + .2
    f.show(dot(*P_(0, 0), AM, 4) + dot(*P_(1, 1), AM, 4), te - .4)
    f.show(chip(PX + S_ * .62, PY - S_ * .32, 'AUC = 21 / 24 = %s' % f3(AUC), FI), te)
    return finish(f, PY + 34)

# ---------- 2.2 Decision ----------
def fig_decide():
    f = Anim('ev3-', 720, 0, 'The ten rows glide into score order. A dashed threshold line slides down to 0.5. Rows above it '
             'are predicted 1, rows below predicted 0; each row then drops into its cell of the 2 by 2 confusion matrix: '
             '3 TP, 2 FP, 1 FN, 4 TN. Precision 3 of 5 is 0.60, recall 3 of 4 is 0.75.',
             'SORT · SLIDE THE THRESHOLD · DROP EACH ROW INTO ITS CELL')
    t, t2 = stage(f)
    f.show(t2.head() + T(t2.x + t2.w / 2, 36, 'sorted', MU), .9)
    cut = sum(1 for s in SC if s >= THR)
    assert cut == 5
    yc = t2.ry(cut) - 2
    line = (L(X1 - 8, 0, X1 + t2.w + 8, 0, AM, 1.8, '5 4') + R(X1 + t2.w + 10, -9, 54, 18, BG, AM, 4, 1.2) +
            T(X1 + t2.w + 37, 4, 't = .5', AM, bold=True))
    f.path(line, [(0, 0, t2.ry(0) - 2), (4.0, 0, yc)], 3.6, d=1.4)
    MX, MY, CW, GAP = 380, 70, 128, 6
    CH = {1: 4 + max(C['TP'], C['FN']) * 28 + 4, 0: 4 + max(C['FP'], C['TN']) * 28 + 4}
    cx = {1: MX, 0: MX + CW + GAP}; cyy = {1: MY, 0: MY + CH[1] + GAP}
    names = {(1, 1): 'TP', (1, 0): 'FN', (0, 1): 'FP', (0, 0): 'TN'}
    mat = T(cx[1] + CW / 2, MY - 10, 'predicted 1', MU) + T(cx[0] + CW / 2, MY - 10, 'predicted 0', MU)
    mat += T(MX - 8, cyy[1] + CH[1] / 2 + 4, 'true 1', FI, 'end') + T(MX - 8, cyy[0] + CH[0] / 2 + 4, 'true 0', BR, 'end')
    for (y, p), nm in names.items():
        ok = y == p
        mat += R(cx[p], cyy[y], CW, CH[y], tint('gr' if ok else 'rd', '.08'), GR if ok else RD, 6, 1.4)
    f.show(mat, 5.6)
    fill = {k: 0 for k in names}; t0 = 6.2
    for k, i in enumerate(SRT):
        y = DATA[i][1]; p = int(SC[i] >= THR); slot = fill[(y, p)]; fill[(y, p)] += 1
        tx = cx[p] + (CW - t.w) / 2; ty = cyy[y] + 4 + slot * 28
        f.path(rowsvg(t, i), [(0, 0, 0), (.4 + .3 * k, X1, (k - i) * STEP), (t0 + k * .3, tx, ty - t.ry(i))], .05, d=.6)
    tm = t0 + N * .3 + .5
    for (y, p), nm in names.items():
        n = C[nm]; ok = y == p
        f.show(pill(cx[p] + CW - 26, cyy[y] + CH[y] - 24, '%s %d' % (nm, n), 'gr' if ok else 'rd', 46), tm)
    yb = cyy[0] + CH[0] + 28
    f.show(M(MX, yb, 'precision = TP / (TP + FP) = 3 / 5 = %s' % f2(P), TX, 'start'), tm + .5)
    f.show(M(MX, yb + 24, 'recall = TP / (TP + FN) = 3 / 4 = %s' % f2(RC), TX, 'start'), tm + 1)
    return finish(f, max(yb + 34, t.bottom(N) + 10))

# ---------- 2.3 Probability ----------
def fig_prob():
    f = Anim('ev4-', 720, 0, 'The ten rows glide into three score bins: below 1/3, 1/3 to 2/3, above 2/3. For each bin the mean '
             'score and the share of true 1s are computed and plotted as one dot on a reliability diagram; the dashed '
             'diagonal is perfect calibration. All three dots sit below it: the model is a little over-confident.',
             'BIN BY SCORE · MEAN SCORE VS SHARE OF 1s · ONE DOT PER BIN')
    t, t2 = stage(f)
    f.show(T(X1 + t2.w / 2, 36, 'binned', MU), .9)
    PX, PY, S_ = 440, 290, 230
    ax = (L(PX, PY, PX + S_, PY, RULE_HI, 1.3) + L(PX, PY, PX, PY - S_, RULE_HI, 1.3) +
          L(PX, PY, PX + S_, PY - S_, FA, 1, '4 4') + S(PX + S_ / 2, PY + 20, 'mean score in bin', MU, 'middle') +
          S(PX - 10, PY - S_ - 10, 'share of true 1s', MU, 'start') +
          T(PX - 6, PY + 4, '0', FA, 'end') + T(PX - 6, PY - S_ + 4, '1', FA, 'end') + T(PX + S_, PY + 15, '1', FA))
    for k in (1, 2): ax += L(PX + k * S_ / 3, PY, PX + k * S_ / 3, PY - S_, RULE, 1, '2 3')
    f.show(ax, 3.4)
    # bins top to bottom: high, mid, low
    order = [2, 1, 0]; slot = 0; base = t.ry(0); BG_ = 16; tb = 4.0
    for g, bi in enumerate(order):
        idx, mean, obs = B[bi]
        idx = sorted(idx, key=lambda i: -SC[i])
        y0 = base + slot * STEP + g * BG_
        lab = ['0 – ⅓', '⅓ – ⅔', '⅔ – 1'][bi]
        f.show(R(X1 - 4, y0 - 4, t.w + 8, len(idx) * STEP + 4, 'none', RULE_HI, 5, 1, '3 3') +
               T(X1 + t.w + 10, y0 + 12, lab, FA, 'start'), .8)
        for k, i in enumerate(idx):
            f.path(rowsvg(t, i), [(0, 0, 0), (.4 + .3 * (slot + k), X1, y0 + k * STEP - t.ry(i))], .05, d=.3)
        tg = tb + g * 1.2
        f.show(R(X1 - 4, y0 - 4, t.w + 8, len(idx) * STEP + 4, 'none', AM, 5, 1.8), tg, hide=tg + 1.1)
        ccx, ccy = PX + mean * S_, PY - obs * S_
        lx, ly = X1 + t.w + 10, y0 + 30
        txt = '%s · %s' % (f2(mean), f2(obs))
        f.path(chip(0, 0, txt, AM), [(0, lx + 40, ly), (tg + .4, ccx + 46, ccy - 4)], tg, d=.5, hide=tg + 1.1)
        f.show(L(ccx, ccy, ccx, PY - mean * S_, RD, 1.4, '3 2') + dot(ccx, ccy, VI, 6, BG) +
               (T(ccx - 10, ccy - 8, txt, VI, 'end', bold=True) if bi else T(ccx + 12, ccy - 6, txt, VI, 'start', bold=True)), tg + .9)
        slot += len(idx)
    f.show(chip(PX + S_ * .7, PY - S_ * .14, 'ECE = %s' % f3(E1), RD), tb + 3.9)
    return finish(f, PY + 34)

# ---------- 03 Choosing a metric ----------
TASKS = [('binary', [('positives rare?', [('no', 'ROC-AUC · accuracy'), ('yes', 'PR-AUC + P / R at threshold')])]),
         ('multiclass', [('rare classes?', [('no', 'accuracy'), ('yes', 'macro-F1')])]),
         ('regression', [('big errors very bad?', [('no', 'MAE'), ('yes', 'RMSE')])]),
         ('ranking', [('top of the list only?', [('no', 'MAP'), ('yes', 'NDCG · Precision@k')])])]
def fig_choose():
    f = Anim('ev5-', 720, 0, 'A decision flow: task type first, then one question about the data, then the main metric. '
             'An example, fraud detection with 1 percent positives, travels the path: binary, positives rare, yes, so '
             'PR-AUC plus precision and recall at the chosen threshold.',
             'TASK → ONE QUESTION → MAIN METRIC · EXAMPLE: FRAUD, 1% POSITIVE')
    X0, XT, XQ, XL = 52, 170, 340, 580
    ys = [62 + k * 76 for k in range(4)]
    s = ''
    nodes = ''
    for k, (task, qs) in enumerate(TASKS):
        y = ys[k]; q, leaves = qs[0]
        s += L(X0 + 40, ys[0] + 114, XT - 44, y, RULE_HI, 1.2)
        s += L(XT + 44, y, XQ - 74, y, RULE_HI, 1.2)
        for j, (ans, m) in enumerate(leaves):
            ly = y - 17 + j * 34
            s += L(XQ + 74, y, XL - 100, ly, RULE_HI, 1.2) + T(XQ + 100, (y + ly) / 2 + (-4 if j == 0 else 12), ans, FA)
            nodes += pill(XL, ly - 10, m, None, 196)
        nodes += qbox(XT, y, task) + qbox(XQ, y, q)
    nodes += qbox(X0, ys[0] + 114, 'task?')
    f.static(s + nodes)
    ex = 0; ey = ys[ex]; ly = ey + 17
    hl = [(L(X0 + 40, ys[0] + 114, XT - 44, ey, HL, 2.4) + qring(X0, ys[0] + 114, 'task?'), 1.0),
          (qring(XT, ey, 'binary'), 1.6), (L(XT + 44, ey, XQ - 74, ey, HL, 2.4) + qring(XQ, ey, 'positives rare?'), 2.4),
          (L(XQ + 74, ey, XL - 100, ly, HL, 2.4) + pill(XL, ly - 10, 'PR-AUC + P / R at threshold', 'am', 196), 3.2)]
    for svg, tt in hl: f.show(svg, tt)
    tok = chip(0, 0, 'fraud · 1%', AM, 88)
    f.path(tok, [(0, X0, ys[0] + 114 - 30), (.9, XT, ey - 28), (2.2, XQ, ey - 28), (3.0, XL, ly - 30)], .4, d=.6, hide=3.7)
    return finish(f, ys[3] + 40)

# ---------- 04 Offline to online ----------
def fig_online():
    f = Anim('ev6-', 720, 0, 'Three boxes left to right. The predictions table produces an offline metric. The new model then '
             'goes to an A/B test: users are split, half see the old model and half the new one. The test reports a '
             'business metric such as clicks or revenue; only that decides the launch.',
             'OFFLINE METRIC → A/B TEST → BUSINESS METRIC')
    bx = [(0, 'offline metric', 'test set', 'ROC-AUC .875'), (250, 'A/B test', 'live users', 'old 50% · new 50%'),
          (500, 'business metric', 'product', 'clicks · revenue')]
    BW, BH, Y = 200, 92, 56
    tcs = [.3, 1.6, 2.9]
    for k, (x, a, b, c) in enumerate(bx):
        col = [FI, AM, GR][k]
        f.show(R(x, Y, BW, BH, BG, 'none', 8) + R(x, Y, BW, BH, tn(FI, '.06') if k == 0 else tint('am' if k == 1 else 'gr', '.08'),
               col, 8, 1.6) + T(x + BW / 2, Y + 26, a, col, bold=True) + T(x + BW / 2, Y + 46, b, MU) +
               T(x + BW / 2, Y + 72, c, TX, mono=True), tcs[k])
        if k:
            f.show(arrow(x - 46, Y + BH / 2, x - 4, Y + BH / 2, MU, 1.4), tcs[k] - .4)
    f.show(T(225, Y + BH + 26, 'does it carry over?', MU), 1.4)
    f.show(T(475, Y + BH + 26, 'is the gap real?', MU), 2.7)
    pk = chip(0, 0, 'model B', VI, 70)
    f.path(pk, [(0, 100, Y - 20), (1.1, 350, Y - 20), (2.4, 600, Y - 20)], .6, d=.7)
    return finish(f, Y + BH + 40)

SCRIPT = re.search(r'<script>.*?</script>', dt.BODY, re.S).group(0)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Model evaluation</p>
  <h1>Model evaluation <em>overview</em></h1>
  <p class="lede">One table of predictions answers <b>three separate questions</b> — is the order right, is the cut right, are the probabilities right — and each needs its own metric.</p>
</header>

<section id="evov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">"Is the model good" is three questions; <em>change the scores without changing their order</em> and only one answer stays put.</p>
{ev1}
  <ul class="why">
    <li>Every metric in this group reads the same table: <b>id, true label, score</b>.</li>
    <li>A model can rank well and still be badly calibrated, or calibrated and badly cut — report the metric that matches how the score is used.</li>
  </ul>
</section>

<section id="evov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Three questions</h2></div>
  <p class="key">Same ten rows, rearranged three ways: <em>sorted, cut, binned</em>.</p>
  <div class="subsec" id="evov-s2-1">
    <h3 class="ssh"><b>2.1</b>Ranking</h3>
    <p class="skey">Are the 1s <em>above</em> the 0s? Uses only the order of the scores.</p>
{ev2}
    <ul class="why">
      <li>ROC-AUC = the chance a random 1 scores above a random 0 — here {w} of {pairs} pairs.</li>
      <li>No threshold involved; with rare positives read the PR curve instead — <a href="../roc-auc-pr/index.html">ROC-AUC &amp; PR curve</a>.</li>
    </ul>
  </div>
  <div class="subsec" id="evov-s2-2">
    <h3 class="ssh"><b>2.2</b>Decision</h3>
    <p class="skey">Is the <em>cut</em> in the right place? Uses one threshold, then counts.</p>
{ev3}
    <ul class="why">
      <li>Every count metric — accuracy, precision, recall, F1 — comes from these four cells.</li>
      <li>Move the threshold and all of them change — <a href="../metrics-confusion-matrix/index.html">Metric &amp; confusion matrix</a>.</li>
    </ul>
  </div>
  <div class="subsec" id="evov-s2-3">
    <h3 class="ssh"><b>2.3</b>Probability</h3>
    <p class="skey">Does a score of 0.8 mean <em>8 in 10 are 1</em>? Uses the score value itself.</p>
{ev4}
    <ul class="why">
      <li>ECE = the bin-size-weighted gap between dot and diagonal; log loss and Brier score also judge the values.</li>
      <li>Fixing it does not change the order — <a href="../calibration/index.html">Probability calibration</a>.</li>
    </ul>
  </div>
</section>

<section id="evov-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Choosing a metric</h2></div>
  <p class="key">Task type first, then <em>one question about the data</em>, gives the main metric.</p>
{ev5}
  <ul class="why">
    <li>With rare positives ROC-AUC stays high because its false-positive rate divides by the huge pile of 0s.</li>
    <li>When the score feeds a later calculation (pricing, risk), add log loss or Brier score; when FP and FN have known costs, minimise <b>expected cost</b>.</li>
    <li>Measure on data the model never saw — <a href="../../04-core-concepts/train-val-test-cv/index.html">Train, validation &amp; test</a>.</li>
  </ul>
</section>

<section id="evov-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Offline to online</h2></div>
  <p class="key">Every metric above is <em>offline</em>: it scores the model, not the product.</p>
{ev6}
  <ul class="why">
    <li>A higher AUC often fails to move the product; check early that the offline metric tracks the business one.</li>
    <li>Whether the gap is real or noise is a statistics question — <a href="../../02-math-foundations/statistics/index.html#stats-s3">A/B testing</a>.</li>
  </ul>
</section>

{script}

<footer>Machine learning · Model evaluation · next lesson: <a href="../metrics-confusion-matrix/index.html">Metric &amp; confusion matrix</a>.</footer>
'''

def build():
    figs = dict(ev1=fig_mental(), ev2=fig_rank(), ev3=fig_decide(), ev4=fig_prob(), ev5=fig_choose(), ev6=fig_online(),
                w='%d' % W, pairs='%d' % (NP * NN), script=SCRIPT)
    return re.sub(r'\{(ev\d|w|pairs|script)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    dt.splice(PAGE, build(), 'One table of predictions, three questions: sorted for ranking (ROC-AUC), cut for decisions '
              '(confusion matrix), binned for probabilities (calibration), plus a flow for choosing the metric.')
