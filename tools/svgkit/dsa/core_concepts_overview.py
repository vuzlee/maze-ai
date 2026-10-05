# -*- coding: utf-8 -*-
"""Figures for content/07-machine-learning/04-core-concepts/core-concepts-overview.
Run: python3 core_concepts_overview.py -> /tmp/ml/core-concepts-overview-figs.json. Every number is computed here."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mlplot import *  # noqa
sys.path.insert(0, os.path.dirname(HERE))
from tablefig import Table

# noisy sine data shared by figures 1 and 5
def make(n, seed, noise=.3):
    r = random.Random(seed); X = [r.random() for _ in range(n)]
    return X, [math.sin(2 * math.pi * x) + r.gauss(0, noise) for x in X]
TRX, TRY = make(30, 1)
VAX, VAY = make(300, 2)
def mse(c, X, Y): return sum((peval(c, x) - y) ** 2 for x, y in zip(X, Y)) / len(X)
DEG = list(range(1, 10))
S = 40   # average over 40 training samples of 15 points, so the curves show the trend, not one draw
CURV = []
for d in DEG:
    a = b = 0
    for s in range(100, 100 + S):
        X, Y = make(15, s)
        c = polyfit(X, Y, d, 1e-10)
        a += mse(c, X, Y) / S; b += min(5, mse(c, VAX, VAY)) / S
    CURV.append((d, a, b))
BEST = min(CURV, key=lambda r: r[2])

# ---------- 1. mental model: memorising scores perfectly on what it has seen ----------
def fig_mental():
    f = Anim('cc1-', 720, 300, 'Thirty training points; a 1-nearest-neighbour model copies each one, so its error on them is zero. '
             'New points then arrive and the same model misses many of them; the error bar on new points rises.',
             'A MODEL THAT MEMORISES · PERFECT ON WHAT IT HAS SEEN')
    pl = Plot(40, 40, 380, 220, 0, 1, -2, 2)
    f.static(frame_box(pl))
    srt = sorted(zip(TRX, TRY))
    for i, (x, y) in enumerate(srt):
        f.show(dot(*pl.P(x, y)), .2 + i * .03, d=.2)
    # 1-NN prediction = step function through the points
    pts = []
    mids = [0] + [(srt[i][0] + srt[i + 1][0]) / 2 for i in range(len(srt) - 1)] + [1]
    for i, (x, y) in enumerate(srt):
        pts += [pl.P(mids[i], y), pl.P(mids[i + 1], y)]
    f.show(poly(pts, AM, 1.8), 1.4, d=.8)
    def nn(x): return min(srt, key=lambda p: abs(p[0] - x))[1]
    tr = 0.0; te = sum((nn(x) - y) ** 2 for x, y in zip(VAX, VAY)) / len(VAX)
    new = list(zip(VAX, VAY))[:14]
    f.show(''.join(dot(*pl.P(x, y), 4, 'gr', True) for x, y in new), 3.4)
    f.show(''.join(L(*pl.P(x, y), *pl.P(x, nn(x)), RD, 1.2, '3 2') for x, y in new), 4.0)
    bx = 480
    f.static(T(bx, 60, 'error (MSE)', MU, 'start'))
    f.show(T(bx, 92, 'on training points', MU, 'start') + R(bx, 100, 2, 16, tint('bl', '.3'), COL['bl'], 2, 1.2) + T(bx + 10, 113, '%.2f' % tr, COL['bl'], 'start', mono=True, bold=True), 2.4)
    f.show(T(bx, 152, 'on new points', MU, 'start') + R(bx, 160, 180 * te / .4, 16, tint('rd', '.25'), COL['rd'], 3, 1.2) + T(bx + 180 * te / .4 + 6, 173, '%.2f' % te, COL['rd'], 'start', mono=True, bold=True), 4.6)
    f.show(T(bx, 220, 'only the second number', TX, 'start', 'sv-s') + T(bx, 238, 'says if it learned', TX, 'start', 'sv-s'), 5.4)
    return f.render(), te

# ---------- 2.1 problem type: label column decides loss ----------
def fig_types():
    f = Anim('cc2-', 720, 226, 'Two tables with the same features. The first label column holds numbers and is tagged regression with squared error; '
             'the second holds yes/no and is tagged classification with log loss.', 'PROBLEM TYPE · THE LABEL COLUMN DECIDES THE LOSS')
    rows = [('80', '2', '310', 'no'), ('120', '3', '455', 'yes'), ('60', '1', '205', 'no'), ('95', '2', '340', 'yes')]
    for k, (x0, lab, j, tag, loss) in enumerate([(0, 'price', 2, 'regression', 'squared error'), (370, 'churn', 3, 'classification', 'log loss')]):
        t = Table(x0, 30, [('size', 70), ('rooms', 70), (lab, 90)])
        f.static(t.head())
        for i, r in enumerate(rows):
            f.show(t.row(i, [r[0], r[1], '']), .2 + i * .1, d=.25)
        t0 = 1.0 + k * 2.2
        f.show(t.colbox(2, 4, AM), t0, hide=t0 + 1.6)
        for i, r in enumerate(rows):
            f.show(t.cell(i, 2, r[j], 'am'), t0 + .2 + i * .15, d=.25)
        y = t.bottom(4) + 16
        f.show(pill(x0 + 70, y, tag, 'gr', 130) + T(x0 + 160, y + 14, '→ ' + loss, GR, 'start', bold=True), t0 + 1.2)
    return f.render()

# ---------- 2.2 bias-variance: two targets ----------
def fig_bv():
    f = Anim('cc3-', 720, 290, 'Two targets. Shots at the left target land tightly together but off centre: high bias. Shots at the right target '
             'centre on the bull but scatter widely: high variance.', 'BIAS VS VARIANCE · SHOTS FROM MODELS TRAINED ON DIFFERENT SAMPLES')
    r = random.Random(9)
    for k, (cx, mx, my, sd, name, sub) in enumerate([(160, 34, -26, 6, 'high bias', 'tight, but off centre'), (520, 0, 0, 30, 'high variance', 'centred, but scattered')]):
        cy = 145
        tg = ''.join('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="var(--rule-hi)" stroke-width="1.2"/>' % (cx, cy, rr, 'var(--bg)' if i % 2 == 0 else 'var(--sunk)')
                     for i, rr in enumerate((90, 66, 42, 18)))
        f.static(tg + '<circle cx="%d" cy="%d" r="4" fill="%s"/>' % (cx, cy, GR))
        for i in range(8):
            x, y = cx + mx + r.gauss(0, sd), cy + my + r.gauss(0, sd)
            t = .5 + k * 3.0 + i * .22
            f.path(dot(x, y, 5, 'am'), [(0, 0, -(y - 30)), (t + .1, 0, 0)], t0=t, d=.25)
        f.show(T(cx, 262, name, COL['rd'], bold=True) + T(cx, 280, sub, MU), 2.6 + k * 3.0)
    return f.render()

# ---------- 2.3 train / val / test: k-fold ----------
def fig_kfold():
    f = Anim('cc4-', 720, 220, 'The data bar is split: a test block is locked away on the right; the rest is cut into five folds. '
             'The validation block slides across the five folds, one score per round, and the five scores are averaged.',
             'SPLITTING DATA · 5-FOLD CROSS-VALIDATION, TEST LOCKED AWAY')
    X0, W, Y = 40, 104, 70
    r = random.Random(4); sc = [round(.80 + r.uniform(-.04, .04), 2) for _ in range(5)]
    f.static(T(X0, Y - 14, 'training data', MU, 'start'))
    for i in range(5):
        f.show(R(X0 + i * W, Y, W - 4, 40, tint('bl', '.12'), COL['bl'], 4, 1.2) + T(X0 + i * W + W / 2 - 2, Y + 25, 'fold %d' % (i + 1), COL['bl']), .2 + i * .1)
    f.show(R(X0 + 5 * W + 20, Y, 110, 40, 'var(--sunk)', RULE_HI, 4, 1.2, '4 3') + T(X0 + 5 * W + 75, Y + 25, 'test 🔒', MU) + T(X0 + 5 * W + 75, Y - 14, 'held out', MU), .9)
    val = R(X0, Y - 4, W - 4, 48, 'var(--bg)', 'none', 5) + R(X0, Y - 4, W - 4, 48, tint('am', '.25'), AM, 5, 2) + T(X0 + W / 2 - 2, Y + 25, 'val', AM, bold=True)
    pts = [(0, 0, 0)] + [(1.6 + i * 1.0, i * W, 0) for i in range(1, 5)]
    f.path(val, pts, t0=1.4, d=.5)
    for i in range(5):
        f.show(T(X0 + i * W + W / 2 - 2, Y + 70, '%.2f' % sc[i], AM, mono=True, bold=True), 1.9 + i * 1.0)
    f.static(T(X0 - 4, Y + 70, 'score', MU, 'end'))
    m = sum(sc) / 5
    f.show(pill(X0 + 2.5 * W, Y + 100, 'mean %.2f ± %.2f' % (m, (sum((s - m) ** 2 for s in sc) / 4) ** .5), 'gr', 150), 7.0)
    f.show(T(X0 + 5 * W + 75, Y + 70, 'opened once,', MU) + T(X0 + 5 * W + 75, Y + 86, 'at the very end', MU), 7.4)
    return f.render(), sc

# ---------- 2.4 overfitting: error vs complexity ----------
def fig_curve():
    f = Anim('cc5-', 720, 314, 'Error against polynomial degree. The training error falls with every degree; the validation error falls, '
             'bottoms out, then rises again: past that point the model is memorising.', 'OVERFITTING · TRAINING ERROR KEEPS FALLING, VALIDATION ERROR TURNS UP')
    f.static(T(60, 300, '15 training points · averaged over %d samples' % S, FA, 'start'))
    ymax = 1.8
    pl = Plot(60, 40, 480, 210, 1, 9, 0, ymax)
    f.static(pl.axes('model complexity (degree)', 'error', [(d, str(d)) for d in range(1, 10)], [(.5, '0.5'), (1, '1.0'), (1.5, '1.5')]))
    cl = lambda v: min(v, ymax)
    tr = [pl.P(d, cl(a)) for d, a, _ in CURV]; va = [pl.P(d, cl(b)) for d, _, b in CURV]
    f.show(poly(tr, BL, 2.4), .4, d=1.0)
    f.show(T(tr[-1][0] + 8, tr[-1][1] + 4, 'train', COL['bl'], 'start', bold=True), 1.2)
    f.show(poly(va, AM, 2.4), 1.8, d=1.0)
    f.show(T(va[-1][0] + 8, va[-1][1] + 4, 'validation', AM, 'start', bold=True), 2.6)
    for k, (d, a, b) in enumerate(CURV):
        f.show(dot(*pl.P(d, cl(a)), 3.5, 'bl') + dot(*pl.P(d, cl(b)), 3.5, 'am'), .4 + k * .1, d=.2)
    bx, by = pl.P(BEST[0], BEST[2])
    f.show(L(bx, by, bx, pl.py + pl.ph, GR, 1.4, '4 3') + ringc(bx, by, 9, GR, 2) + pill(bx, pl.py - 2, 'best: degree %d' % BEST[0], 'gr', 120), 3.4)
    f.show(T(pl.X(1.4), pl.py + 30, '← underfit', MU, 'start') + T(pl.X(8.8), pl.py + 30, 'overfit →', RD, 'end'), 4.0)
    return f.render()

# ---------- 2.5 feature engineering: table transforms column by column ----------
def fig_fe():
    f = Anim('cc6-', 720, 244, 'A raw table with a city column and a size column. The city column is replaced by three 0/1 columns, one per city; '
             'then the size column is rescaled to mean 0 and spread 1.', 'FEATURE ENGINEERING · TURN RAW COLUMNS INTO NUMBERS A MODEL CAN USE')
    city = ['Paris', 'Rome', 'Oslo', 'Paris']; size = [80, 120, 60, 100]
    m = sum(size) / 4; sd = (sum((s - m) ** 2 for s in size) / 4) ** .5
    z = ['%+.1f' % ((s - m) / sd) for s in size]
    raw = Table(0, 30, [('city', 80), ('size', 70)])
    f.static(raw.head())
    for i in range(4): f.static(raw.row(i, [city[i], str(size[i])]))
    f.static(arrow(170, 100, 220, 100, MU, 1.4))
    out = Table(240, 30, [('Paris', 66), ('Rome', 66), ('Oslo', 66), ('size', 80, 'scaled')])
    f.show(out.head(), .3)
    for i in range(4): f.show(out.row(i, ['', '', '', '']), .3, d=.25)
    t = 1.0
    f.show(raw.colbox(0, 4, AM), t, hide=t + 2.2)
    for j, c in enumerate(('Paris', 'Rome', 'Oslo')):
        for i in range(4):
            on = city[i] == c
            f.show(out.cell(i, j, '1' if on else '0', 'gr' if on else None, None if on else FA), t + .3 + j * .5, d=.25)
    f.show(T(560, 210, 'one-hot: no fake order', MU, 'end'), t + 1.8)
    t = 3.6
    f.show(raw.colbox(1, 4, AM), t, hide=t + 1.6)
    for i in range(4):
        f.show(out.cell(i, 3, z[i], 'gr'), t + .3 + i * .15, d=.25)
    f.show(T(560, 230, 'scaled: mean 0, spread 1', MU, 'end'), t + 1.0)
    return f.render()

if __name__ == '__main__':
    F = {}
    F['mental'], te1 = fig_mental(); F['types'] = fig_types(); F['bv'] = fig_bv(); F['kfold'], sc = fig_kfold(); F['curve'] = fig_curve(); F['fe'] = fig_fe()
    print('1nn test %.3f' % te1, 'best', BEST, 'scores', sc)
    for r in CURV: print('%2d %.3f %.3f' % r)
    json.dump({k: palette(v) for k, v in F.items()}, open('/tmp/ml/core-concepts-overview-figs.json', 'w'))
