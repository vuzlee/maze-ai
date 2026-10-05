# -*- coding: utf-8 -*-
"""Figures for content/07-machine-learning/04-core-concepts/train-val-test-cv.
Run: python3 train_val_test_cv.py -> splices into <!--FIGn--> markers."""
import random
mean = lambda a: sum(a) / len(a)
pstdev = lambda a: (sum((x - mean(a)) ** 2 for x in a) / len(a)) ** .5
from cc_kit import *  # noqa

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/04-core-concepts/train-val-test-cv/index.html')

def blk(x, y, w, h, lab, tone=None, off=False, sub=None):
    if off:
        return R(x, y, w, h, SUNK, RULE_HI, 4) + T(x + w / 2, y + h / 2 + 4, lab, FA)
    fill = tint(tone, '.20') if tone else 'var(--bg)'
    s = R(x, y, w, h, 'var(--bg)', 'none', 4) + R(x, y, w, h, fill, COL[tone] if tone else RULE_HI, 4, 1.4 if tone else 1)
    return s + T(x + w / 2, y + h / 2 + (0 if sub else 4), lab, COL[tone] if tone else TX) + \
        (T(x + w / 2, y + h / 2 + 14, sub, MU) if sub else '')

# ---------- 1.1 Three sets ----------
def f_three():
    f = Fig('cv1-', 680, 250, 'One bar of 100 rows splits into train 60, validation 20 and test 20. Train feeds three '
            'candidate models. Validation scores them and picks model B. Only then the locked test set opens once and '
            'gives the final score.', 'ONE DATASET · THREE JOBS')
    X, W = 0, 660
    f(blk(X, 36, W, 32, 'all data · 100 rows'), hide=1.0)
    parts = [('train · 60', .6, 'bl'), ('val · 20', .2, 'am'), ('test · 20', .2, 'gr')]
    x = X
    xs = []
    for k, (lab, fr, tone) in enumerate(parts):
        w = W * fr - (4 if k < 2 else 0)
        f(blk(x, 36, w, 32, lab, tone), show=1.0 + k * .2)
        xs.append((x, w)); x += W * fr
    # train -> three models
    ms = ['A', 'B', 'C']
    for k, m in enumerate(ms):
        cx = 70 + k * 130
        f(arrow(xs[0][0] + xs[0][1] / 2, 72, cx, 104, BL, 1.2) + blk(cx - 45, 106, 90, 30, 'model ' + m), show=1.9 + k * .2)
    f(T(0, 156, 'fit parameters on train', BL, 'start'), show=2.0)
    vx = xs[1][0] + xs[1][1] / 2
    sc = [.71, .78, .74]
    for k, m in enumerate(ms):
        cx = 70 + k * 130
        f(pill(cx, 176, 'val %.2f' % sc[k], 'am', 70), show=3.0 + k * .3)
    f(arrow(vx, 72, vx, 96, AM, 1.2) + T(vx + 8, 92, 'score each, choose', AM, 'start'), show=2.9)
    f(R(70 + 130 - 50, 100, 100, 104, 'none', AM, 6, 1.6, '4 3'), show=4.0)
    tx = xs[2][0] + xs[2][1] / 2
    f(R(xs[2][0] - 2, 34, xs[2][1] + 4, 36, 'none', GR, 5, 1.6, '4 3') + T(tx, 90, 'locked until the end', GR), show=1.6, hide=4.6)
    f(arrow(tx, 72, tx, 106, GR, 1.4) + blk(tx - 70, 108, 140, 40, 'model B', 'gr', sub='test 0.72 · once'), show=4.8)
    f(T(0, 236, 'train fits · validation chooses · test reports, exactly once', MU, 'start'), show=5.6)
    return f.render()

# ---------- 1.2 Why a separate test set ----------
def f_luck():
    rng = random.Random(3)
    true = .70
    vals = [true + rng.gauss(0, .025) for _ in range(100)]
    best = max(vals)
    f = Fig('cv2-', 680, 270, 'One hundred configurations that are all truly 0.70 good get validation scores that scatter '
            'around 0.70 by luck. The highest one, %.2f, is picked. Measured on the untouched test set, the same '
            'configuration scores 0.70: the validation winner was mostly luck.' % best, 'PICK THE BEST OF 100 · GET THE LUCKIEST')
    P = Plot(40, 40, 600, 150, (.62, .80), (0, 24))
    bins = [0] * 18
    xs = [.62 + .01 * i for i in range(19)]
    f(P.axes('validation score', '', xt=[(v, '%.2f' % v) for v in (.62, .66, .70, .74, .78)]))
    cnt = {}
    for k, v in enumerate(sorted(vals, key=lambda _: rng.random())):
        b = min(17, max(0, int((v - .62) / .01)))
        cnt[b] = cnt.get(b, 0) + 1
        x = P.px(.62 + .01 * b + .005); y = P.py(cnt[b] - .5)
        f(dot(x, y, 'bl', 4.2), show=.3 + k * .025, d=.15)
    f(L(P.px(true), P.y0 - 6, P.px(true), P.y0 + P.h, GR, 1.6, '5 4') + T(P.px(true) + 8, P.y0 + 4, 'true quality 0.70', GR, 'start'), show=3.0)
    bb = min(17, int((best - .62) / .01))
    bx = P.px(.62 + .01 * bb + .005)
    f(ring(bx, P.py(cnt[bb] - .5), 9) + T(bx + 14, P.py(cnt[bb] - .5) - 14, 'winner %.2f' % best, AM, 'start'), show=3.8)
    f(T(0, 250, 'validation says %.2f' % best, AM, 'start', 'sv-s'), show=4.4)
    f(T(200, 250, '→ fresh test set says 0.70', GR, 'start', 'sv-s'), show=5.2)
    assert best > .75
    return f.render()

# ---------- 2.1 k-fold ----------
def f_kfold():
    sc = [.81, .78, .84, .80, .77]
    m = mean(sc); sd = pstdev(sc)
    f = Fig('cv3-', 680, 326, 'Five rows of five blocks. In row j the j-th block is validation and the other four train, so the validation block slides one step per row. '
            'Each row writes its score at the right: 0.81, 0.78, 0.84, 0.80, 0.77. They are averaged to %.2f with spread %.2f.' % (m, sd),
            'k = 5 · EVERY BLOCK IS VALIDATED ONCE')
    X, bw, bh, Y0 = 70, 84, 30, 36
    for r in range(5):
        y = Y0 + r * (bh + 8); t = .4 + r * .9
        f(T(X - 10, y + bh / 2 + 4, 'fold %d' % (r + 1), MU, 'end', mono=True), show=t, d=.2)
        for j in range(5):
            x = X + j * (bw + 4)
            f(blk(x, y, bw, bh, 'val', 'am') if j == r else blk(x, y, bw, bh, 'train', 'bl'), show=t + (.15 if j == r else 0), d=.2)
        f(pill(X + 5 * (bw + 4) + 40, y + 5, '%.2f' % sc[r], 'am', 52), show=t + .5, d=.2)
    t = 5.2; ym = Y0 + 5 * (bh + 8) + 8
    f(L(X + 5 * (bw + 4) + 10, ym - 4, X + 5 * (bw + 4) + 70, ym - 4, MU, 1.2), show=t, d=.2)
    f(pill(X + 5 * (bw + 4) + 40, ym + 2, 'mean %.2f' % m, 'gr', 90) + T(X + 5 * (bw + 4) + 40, ym + 40, '± %.2f spread' % sd, GR), show=t + .2)
    f(T(0, 306, 'no single lucky split decides the number · the spread says how much to trust it', MU, 'start'), show=t + 1.0)
    return f.render()

# ---------- 2.2 Stratified ----------
def fold_dots(f, y, groups, t, label, ymark=None):
    """groups: per fold a list of tones; five folds side by side."""
    f(T(0, y + 19, label, MU, 'start'), show=t)
    for j, g in enumerate(groups):
        x = 130 + j * 108
        f(R(x, y, 100, 28, 'var(--bg)', RULE_HI, 4), show=t)
        for q, tone in enumerate(g):
            f(dot(x + 14 + q * 18, y + 14, tone, 6), show=t + .3 + j * .2 + q * .03, d=.2)

def f_strat():
    plain = [2, 0, 1, 0, 2]
    strat = [1, 1, 1, 1, 1]
    assert sum(plain) == sum(strat) == 5
    f = Fig('cv4-', 680, 240, 'Twenty-five rows, five of them the rare class. Random folds put two rare rows in one fold and '
            'none in two others. Stratified folds deal the rare rows out first, one per fold, so every fold keeps the same '
            '1 in 5 ratio.', 'KEEP THE CLASS RATIO IN EVERY FOLD')
    for j in range(5):
        f(T(180 + j * 108, 36, 'fold %d' % (j + 1), FA))
    gr = lambda r: ['rd'] * r + ['bl'] * (5 - r)
    fold_dots(f, 48, [gr(r) for r in plain], .2, 'random')
    for j, r in enumerate(plain):
        if r == 0:
            f(T(180 + j * 108, 96, 'no rare row', RD), show=1.6)
        if r == 2:
            f(T(180 + j * 108, 96, '2 rare rows', RD), show=1.6)
    fold_dots(f, 128, [gr(r) for r in strat], 2.6, 'stratified')
    f(T(180 + 2 * 108, 176, 'one rare row in every fold', GR), show=4.0)
    f(T(0, 214, '● rare class (fraud, disease) · ● common class', MU, 'start'), show=.2)
    return f.render()

# ---------- 2.3 Group ----------
def f_group():
    f = Fig('cv5-', 680, 270, 'Rows from three patients, Ann, Ben and Cal, each with several scans. A random split puts some '
            'of Ann\'s scans in train and some in validation, so the model recognises Ann instead of learning the disease. '
            'Group split moves all of a patient\'s rows to one side.', 'ALL ROWS OF ONE PATIENT STAY TOGETHER')
    pts = ['Ann'] * 4 + ['Ben'] * 3 + ['Cal'] * 3
    rnd = ['tr', 'va', 'tr', 'va', 'tr', 'tr', 'va', 'tr', 'tr', 'tr']
    grp = ['tr' if p != 'Cal' else 'va' for p in pts]
    tone = {'Ann': 'am', 'Ben': None, 'Cal': 'bl'}
    def side(y, assign, t, title):
        f(T(0, y - 8, title, MU, 'start', 'sv-s'), show=t)
        f(R(0, y, 400, 46, 'var(--bg)', RULE_HI, 6) + T(10, y + 28, 'train', MU, 'start'), show=t)
        f(R(420, y, 240, 46, 'var(--bg)', RULE_HI, 6) + T(430, y + 28, 'val', MU, 'start'), show=t)
        cnt = {'tr': 0, 'va': 0}
        for i, (p, a) in enumerate(zip(pts, assign)):
            x = (60 if a == 'tr' else 470) + cnt[a] * 42
            cnt[a] += 1
            f(R(x, y + 9, 36, 28, tint(tone[p], '.20') if tone[p] else 'var(--bg)', COL[tone[p]] if tone[p] else RULE_HI, 4, 1.2) + T(x + 18, y + 28, p, COL[tone[p]] if tone[p] else TX),
              show=t + .3 + i * .08, move=(t + .3 + i * .08, 330 - x, -30, .6))
    side(46, rnd, .2, 'random split')
    f(T(420, 116, 'Ann is on both sides → the model memorises Ann', RD, 'start'), show=2.0)
    side(160, grp, 3.0, 'group split')
    f(T(420, 230, 'Cal never seen in training → honest score', GR, 'start'), show=5.0)
    return f.render()

# ---------- 2.4 Time ----------
def f_time():
    f = Fig('cv6-', 680, 214, 'Six months of data on a time axis. Round one trains on months 1 to 3 and validates on month 4. '
            'Round two trains on months 1 to 4 and validates on month 5. Round three trains on 1 to 5 and validates on '
            'month 6. Validation is always after training, never shuffled.', 'TRAIN ON THE PAST · VALIDATE ON THE FUTURE')
    X, bw = 90, 90
    for m in range(6):
        f(T(X + m * (bw + 4) + bw / 2, 38, 'month %d' % (m + 1), FA))
    f(arrow(X, 196, X + 6 * (bw + 4), 196, FA, 1.2) + T(X - 10, 200, 'time', MU, 'end'))
    for r in range(3):
        y = 50 + r * 44
        t = .4 + r * 1.3
        f(T(0, y + 20, 'round %d' % (r + 1), MU, 'start'), show=t)
        for m in range(3 + r):
            f(blk(X + m * (bw + 4), y, bw, 28, 'train', 'bl'), show=t + m * .1)
        f(blk(X + (3 + r) * (bw + 4), y, bw, 28, 'val', 'am'), show=t + .6)
        for m in range(4 + r, 6):
            f(blk(X + m * (bw + 4), y, bw, 28, 'unused', off=True), show=t + .6)
    return f.render()

# ---------- 3.1 Fit on train only ----------
def f_scaler():
    tr = [10, 20, 30, 40]; te = [90]
    mt = mean(tr); ma = mean(tr + te)
    f = Fig('cv7-', 680, 260, 'Train values 10, 20, 30, 40 and one test value 90. Wrong way: the scaler computes its mean '
            'over all five values, 38, so the test row has already shaped the training data. Right way: the mean is '
            'computed on train only, 25, and then applied to the test row.', 'THE SCALER MUST NOT SEE THE TEST ROWS')
    def row(y, title, cols, tone_mean, mean, t, wrong):
        f(T(0, y + 18, title, RD if wrong else GR, 'start', 'sv-s'), show=t)
        for i, v in enumerate(tr + te):
            x = 150 + i * 62
            test = i == 4
            f(blk(x, y, 54, 28, str(v), 'gr' if test else 'bl'), show=t)
        n = 5 if wrong else 4
        f(R(146, y - 4, n * 62 - 2, 36, 'none', AM, 5, 1.6, '4 3'), show=t + .5)
        f(T(150 + 5 * 62 + 20, y + 18, 'mean = %g' % mean, RD if wrong else GR, 'start', 'sv-s'), show=t + 1.0)
    f(T(150 + 4 * 62 + 27, 36, 'test', GR), show=.2)
    row(48, 'wrong', None, 'rd', ma, .2, True)
    f(T(150, 106, 'the test row already moved the mean → score looks better than it is', RD, 'start'), show=1.6)
    row(140, 'right', None, 'gr', mt, 2.6, False)
    f(T(150, 198, 'fit on train, then only apply to test', GR, 'start'), show=3.8)
    f(T(0, 240, 'same rule for imputing, feature selection, resampling: fit inside each fold', MU, 'start'), show=4.6)
    assert mt == 25 and ma == 38
    return f.render()

# ---------- 3.2 Features from the future ----------
def f_future():
    f = Fig('cv8-', 680, 272, 'A time line with a prediction moment marked now. Features age and last month spend are known '
            'before now and pass. The feature cancel reason is only filled in after the customer leaves, after now, so it '
            'is struck out as leakage.', 'IS THE VALUE KNOWN AT PREDICTION TIME?')
    X0, X1, NOW = 40, 640, 380
    f(arrow(X0, 200, X1, 200, FA, 1.2) + T(X1, 220, 'time', MU, 'end'))
    f(L(NOW, 40, NOW, 206, AM, 2) + T(NOW + 8, 50, 'now · predict churn', AM, 'start', 'sv-s'), show=.3)
    feats = [('age', 120, True), ('last month spend', 230, True), ('cancel reason', 480, False)]
    for k, (n, x, ok) in enumerate(feats):
        y = 60 + k * 44
        t = 1.0 + k * 1.0
        f(L(x, y + 26, x, 200, RULE_HI, 1, '2 3') + '<circle cx="%d" cy="200" r="4" fill="%s"/>' % (x, BL), show=t)
        f(pill(x, y, n, 'bl' if ok else 'rd', 18 + len(n) * 6.6), show=t)
        f(T(x + 12 + len(n) * 3.3, y + 14, '✓ known' if ok else '✕ only after leaving', GR if ok else RD, 'start'), show=t + .5)
        f(T(X0, 256, 'a column filled in after the event leaks the answer', MU, 'start'), show=4.0)
    return f.render()

if __name__ == '__main__':
    splice(PAGE, [f_three(), f_luck(), f_kfold(), f_strat(), f_group(), f_time(), f_scaler(), f_future()])
