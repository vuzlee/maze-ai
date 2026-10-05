# -*- coding: utf-8 -*-
"""Figures for content/07-machine-learning/04-core-concepts/feature-engineering.
Run: python3 feature_engineering.py -> splices into <!--FIGn--> markers.
Every table figure animates the transformation column by column."""
import math
from cc_kit import *  # noqa

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/04-core-concepts/feature-engineering/index.html')
mean = lambda a: sum(a) / len(a)

# ---------- 1. Mental model: raw row -> feature row ----------
def f_mental():
    f = Fig('fe1-', 700, 230, 'One raw customer row: city Paris, income blank, age 34, signup date 2024-03-09. Four arrows '
            'turn it into numbers a model can read: city becomes three 0/1 columns, the blank income becomes the median '
            'plus a missing flag, age is scaled to 0.2, and the date becomes day of week 6.', 'RAW ROW IN · NUMBERS OUT')
    raw = Table(0, 30, [('city', 70), ('income', 70), ('age', 50), ('signup', 90)], 'raw')
    f(raw.head()); f(raw.row(0, ['Paris', '—', '34', '2024-03-09']))
    out = Table(0, 130, [('Paris', 46), ('Rome', 46), ('Oslo', 46), ('income', 62), ('missing', 58), ('age', 50), ('weekday', 64)], 'features')
    f(out.head(), show=.6)
    f(out.row(0, ['', '', '', '', '', '', '']), show=.6)
    steps = [(0, [(0, '1', 'gr'), (1, '0', None), (2, '0', None)], 'encode'),
             (1, [(3, '42k', 'gr'), (4, '1', 'gr')], 'impute'),
             (2, [(5, '0.2', 'gr')], 'scale'),
             (3, [(6, '6', 'gr')], 'create')]
    for k, (j, cells, lab) in enumerate(steps):
        t = 1.2 + k * 1.2
        f(raw.colbox(j, 1, AM), show=t, hide=t + 1.1)
        x0 = raw.cx(j); x1 = out.cx(cells[0][0])
        f(arrow(x0, raw.bottom(1) + 4, x1, out.y + 14, AM, 1.3), show=t + .2, hide=t + 1.1, d=.2)
        f(T(420, 122, 'step %d of 4 · %s' % (k + 1, lab), AM, 'start', 'sv-s'), show=t, hide=t + 1.1, d=.2)
        for jj, v, tone in cells:
            f(out.cell(0, jj, v, tone), show=t + .5, d=.25)
    f(raw.dimcol(0, 1) + raw.dimcol(1, 1) + raw.dimcol(2, 1) + raw.dimcol(3, 1), show=6.0)
    f(T(0, 214, 'every column the model sees is a number with a meaning', MU, 'start'), show=6.2)
    return f.render()

# ---------- 2.x Categorical ----------
CITIES = ['Paris', 'Rome', 'Oslo', 'Rome', 'Paris']
def f_onehot():
    f = Fig('fe2-', 700, 230, 'Five rows with a city column. Three new columns Paris, Rome, Oslo appear. Row by row, a 1 '
            'lights up in the column of that row\'s city and the rest get 0. The city column is then greyed out: it is '
            'replaced by three 0/1 columns with no order between them.', 'ONE 0/1 COLUMN PER VALUE')
    t = Table(0, 30, [('city', 80), ('Paris', 70), ('Rome', 70), ('Oslo', 70)])
    f(t.head())
    for i, c in enumerate(CITIES):
        f(t.row(i, [c, '', '', '']))
    names = ['Paris', 'Rome', 'Oslo']
    for i, c in enumerate(CITIES):
        tt = .6 + i * .7
        f(t.outline(i, i, 0, 3, AM), show=tt, hide=tt + .7, d=.15)
        for j, n in enumerate(names):
            f(t.cell(i, j + 1, '1' if n == c else '0', 'gr' if n == c else None), show=tt + .3, d=.2)
    f(t.dimcol(0, 5), show=4.4)
    f(T(330, 80, '3 values → 3 columns', MU, 'start') + T(330, 100, 'no fake order between cities', GR, 'start', 'sv-s'), show=4.6)
    f(T(330, 140, 'cost: 1000 values → 1000 columns', MU, 'start'), show=5.2)
    return f.render()

def f_ordinal():
    f = Fig('fe3-', 700, 240, 'A size column small, large, medium, small, large is mapped to 1, 3, 2, 1, 3 one row at a time. '
            'Then a number line shows small at 1, medium at 2, large at 3, where the order is real. Below, the same trick on '
            'cities puts Rome between Paris and Oslo, an order that does not exist.', 'MAP VALUES TO RANKS · ONLY WHEN ORDER IS REAL')
    sz = ['small', 'large', 'medium', 'small', 'large']; rk = {'small': 1, 'medium': 2, 'large': 3}
    t = Table(0, 30, [('size', 80), ('size_rank', 90)])
    f(t.head())
    for i, s in enumerate(sz):
        f(t.row(i, [s, '']))
    for i, s in enumerate(sz):
        tt = .5 + i * .5
        f(t.outline(i, i, 0, 0, AM), show=tt, hide=tt + .5, d=.15)
        f(t.cell(i, 1, str(rk[s]), 'gr'), show=tt + .25, d=.2)
    X0, X1, Y = 300, 640, 70
    f(L(X0, Y, X1, Y, RULE_HI, 1.4), show=3.2)
    for k, n in enumerate(['small', 'medium', 'large']):
        x = X0 + 20 + k * 150
        f(dot(x, Y, 'gr', 6) + T(x, Y - 12, n, GR) + T(x, Y + 20, str(k + 1), MU), show=3.4 + k * .2)
    f(T(X0, Y + 44, 'real order → ranks are fine', GR, 'start', 'sv-s'), show=4.2)
    Y2 = 170
    f(L(X0, Y2, X1, Y2, RULE_HI, 1.4), show=5.0)
    for k, n in enumerate(['Paris', 'Rome', 'Oslo']):
        x = X0 + 20 + k * 150
        f(dot(x, Y2, 'rd', 6) + T(x, Y2 - 12, n, RD) + T(x, Y2 + 20, str(k + 1), MU), show=5.2 + k * .2)
    f(T(X0, Y2 + 44, 'no order → model reads Rome as "between"', RD, 'start', 'sv-s'), show=6.0)
    return f.render()

def f_target():
    rows = [('A', 1), ('A', 0), ('A', 1), ('B', 0), ('B', 1), ('Z', 0)]
    f = Fig('fe4-', 700, 272, 'Six rows of product id and label. Group A has labels 1, 0, 1 and encodes to their mean 0.67; '
            'group B has 0, 1 and encodes to 0.50. Group Z has a single row with label 0, so its encoded value 0.00 is just '
            'its own label copied, which leaks the answer into the feature.', 'REPLACE EACH VALUE BY ITS GROUP\'S MEAN LABEL')
    t = Table(0, 30, [('product', 80), ('label', 70), ('encoded', 90)])
    f(t.head())
    for i, (p, y) in enumerate(rows):
        f(t.row(i, [p, str(y), '']))
    grp = {}
    for p, y in rows:
        grp.setdefault(p, []).append(y)
    tt = .6
    for p in ['A', 'B', 'Z']:
        idx = [i for i, r in enumerate(rows) if r[0] == p]
        f(t.outline(idx[0], idx[-1], 0, 1, AM), show=tt, hide=tt + 1.1, d=.15)
        m = mean(grp[p])
        f(T(330, t.ry(idx[0]) + 17, 'mean(%s) = %.2f' % (', '.join(map(str, grp[p])), m), AM, 'start'), show=tt + .2, hide=tt + 1.1)
        for i in idx:
            f(t.cell(i, 2, '%.2f' % m, 'rd' if p == 'Z' else 'gr'), show=tt + .6, d=.2)
        tt += 1.3
    f(leader(t.x + t.w, t.ry(5) + 13, 330, t.ry(5) + 13, 'one row: encoded = its own label → leak', RD), show=tt)
    f(T(0, 252, 'fix: compute means inside each fold, leave the row out, smooth small groups toward the global mean', MU, 'start'), show=tt + .8)
    return f.render()

def f_hash():
    vals = ['p-1042', 'p-77', 'p-9310', 'p-5', 'p-2288']
    B = 4
    hv = lambda s: sum(ord(c) * (i + 1) for i, c in enumerate(s)) % B
    bk = [hv(v) for v in vals]
    f = Fig('fe5-', 700, 248, 'Five product ids go through a hash function and each lands in one of four fixed buckets: '
            '%s. Two ids share a bucket, a collision. The column count stays four no matter how many ids appear.' %
            ', '.join('%s to %d' % (v, b) for v, b in zip(vals, bk)), 'HASH ANY VALUE INTO A FIXED NUMBER OF COLUMNS')
    for i, v in enumerate(vals):
        f(pill(60, 40 + i * 34, v, None, 80))
    f(R(220, 60, 110, 110, tint('bl', '.10'), BL, 8) + T(275, 120, 'hash % 4', BL, 'middle', 'sv-s'))
    for b in range(B):
        f(R(430 + b * 64, 90, 56, 46, 'var(--bg)', RULE_HI, 5) + T(430 + b * 64 + 28, 156, 'col %d' % b, MU))
    cnt = [0] * B
    for i, (v, b) in enumerate(zip(vals, bk)):
        t = .6 + i * .8
        f(pill(60, 40 + i * 34, v, 'am', 80), show=t, hide=t + .8, d=.15)
        f(arrow(102, 50 + i * 34, 218, 115, AM, 1.2), show=t, hide=t + .8, d=.15)
        f(arrow(332, 115, 430 + b * 64 + 28, 92, AM, 1.2), show=t + .3, hide=t + .8, d=.15)
        cnt[b] += 1
        f(dot(430 + b * 64 + 16 + (cnt[b] - 1) * 24, 113, 'gr' if cnt[b] == 1 else 'rd', 7), show=t + .5, d=.2)
    col = [b for b in range(B) if cnt[b] > 1]
    assert col, bk
    f(T(430 + col[0] * 64 + 28, 186, 'collision', RD), show=4.8)
    f(T(0, 228, 'new ids need no new columns · cost: collisions, and columns lose their meaning', MU, 'start'), show=5.2)
    return f.render()

# ---------- 3.x Missing ----------
def f_impute():
    inc = [40, None, 55, 38, None, 61]
    known = sorted(v for v in inc if v is not None)
    med = (known[1] + known[2]) / 2
    f = Fig('fe6-', 700, 266, 'An income column with two blanks. The known values 40, 55, 38, 61 are ringed and their median '
            '%g is computed. The blanks fill with %g, and a new was_missing column gets 1 on those two rows and 0 '
            'elsewhere, so the model still knows they were blank.' % (med, med), 'FILL THE BLANK · KEEP A FLAG')
    t = Table(0, 30, [('id', 50), ('income', 80), ('was_missing', 100)])
    f(t.head())
    for i, v in enumerate(inc):
        f(t.row(i, [str(i + 1), '—' if v is None else '%dk' % v, '']))
        if v is None:
            f(t.cell(i, 1, '—', 'rd'))
    for i, v in enumerate(inc):
        if v is not None:
            f(t.outline(i, i, 1, 1, AM), show=.6 + i * .15, hide=2.4, d=.15)
    f(T(280, 80, 'median of known = %gk' % med, AM, 'start', 'sv-s'), show=1.4)
    for i, v in enumerate(inc):
        if v is None:
            f(t.cell(i, 1, '%gk' % med, 'gr'), show=2.6, d=.3)
    for i, v in enumerate(inc):
        f(t.cell(i, 2, '1' if v is None else '0', 'gr' if v is None else None), show=3.4 + i * .12, d=.2)
    f(T(280, 120, 'flag keeps the fact "it was blank"', GR, 'start', 'sv-s'), show=4.4)
    f(T(280, 140, 'median, not mean: one huge income cannot drag it', MU, 'start'), show=5.0)
    assert med == 47.5
    return f.render()

def f_mnar():
    # new customers have no history; blank is a strong signal of churn
    rows = [('old', '12', 0), ('new', '—', 1), ('old', '30', 0), ('new', '—', 1), ('old', '8', 1), ('new', '—', 1)]
    f = Fig('fe7-', 700, 266, 'A table of customers with orders last year and a churned label. The three blanks all belong to '
            'new customers, and all three churned. Counting shows churn is 3 of 3 among blanks but 1 of 3 among filled '
            'rows: being blank is itself a strong signal, which a fill-only approach would erase.', 'BEING BLANK CAN BE THE SIGNAL')
    t = Table(0, 30, [('customer', 90), ('orders last yr', 110), ('churned', 80)])
    f(t.head())
    for i, (c, o, y) in enumerate(rows):
        f(t.row(i, [c, o, str(y)]))
    blanks = [i for i, r in enumerate(rows) if r[1] == '—']
    for k, i in enumerate(blanks):
        f(t.cell(i, 1, '—', 'am'), show=.6 + k * .3, d=.2)
        f(t.cell(i, 2, '1', 'rd'), show=1.8 + k * .3, d=.2)
    br = sum(rows[i][2] for i in blanks); fr = sum(r[2] for r in rows if r[1] != '—')
    assert (br, fr) == (3, 1)
    X0 = 330
    f(T(X0, 60, 'churn rate', MU, 'start'), show=2.8)
    for k, (lab, v, tone) in enumerate([('blank', 3 / 3, 'rd'), ('filled', 1 / 3, 'bl')]):
        y = 74 + k * 40
        f(T(X0, y + 17, lab, MU, 'start') + R(X0 + 60, y, 260, 24, SUNK, 'none', 3), show=3.0)
        f(R(X0 + 60, y, 260 * v, 24, tint(tone, '.45'), COL[tone], 3, 1) + T(X0 + 66 + 260 * v, y + 17, '%d%%' % round(v * 100), COL[tone], 'start'),
          show=3.2 + k * .4, move=(3.2 + k * .4, -130 * v, 0, .6))
    f(T(X0, 190, 'fill the blank and add a was_missing flag;', MU, 'start') + T(X0, 206, 'filling alone erases this signal', MU, 'start'), show=4.6)
    return f.render()

# ---------- 4.x Scaling ----------
def f_distance():
    a = (30000, 30); b = (32000, 55)
    d_raw = math.dist(a, b)
    share = (2000 ** 2) / (2000 ** 2 + 25 ** 2)
    f = Fig('fe8-', 700, 250, 'Two customers: income 30,000 and 32,000, age 30 and 55. The squared income gap, 4,000,000, '
            'fills almost the whole distance bar; the age gap, 625, is a sliver. After standardising both columns the two '
            'gaps become comparable bars.', 'LARGE UNITS DROWN SMALL ONES')
    t = Table(0, 30, [('', 40), ('income', 90), ('age', 60)])
    f(t.head()); f(t.row(0, ['A', '30,000', '30'])); f(t.row(1, ['B', '32,000', '55']))
    X0, W = 260, 400
    f(T(X0, 50, 'share of the squared distance', MU, 'start'), show=.6)
    f(T(X0, 76, 'raw', MU, 'start') + R(X0 + 50, 62, W - 50, 22, SUNK, 'none', 3), show=.8)
    w1 = (W - 50) * share
    f(R(X0 + 50, 62, w1, 22, tint('rd', '.40'), RD, 3, 1), show=1.2, move=(1.2, -w1 / 2, 0, .7))
    f(R(X0 + 50 + w1, 62, max(2, (W - 50) - w1), 22, tint('bl', '.6'), BL, 1, 1), show=1.9)
    f(T(X0 + 50, 104, 'income %.2f%% · age %.2f%%' % (share * 100, (1 - share) * 100), RD, 'start'), show=2.0)
    # standardised: assume sd income 8000, sd age 12
    gi, ga = 2000 / 8000, 25 / 12
    sh2 = gi ** 2 / (gi ** 2 + ga ** 2)
    f(T(X0, 156, 'scaled', MU, 'start') + R(X0 + 50, 142, W - 50, 22, SUNK, 'none', 3), show=3.0)
    w2 = (W - 50) * sh2
    f(R(X0 + 50, 142, w2, 22, tint('bl', '.40'), BL, 3, 1), show=3.4, move=(3.4, -w2 / 2, 0, .6))
    f(R(X0 + 50 + w2, 142, (W - 50) - w2, 22, tint('gr', '.40'), GR, 3, 1), show=3.8, move=(3.8, ((W - 50) - w2) / 2, 0, .6))
    f(T(X0 + 50, 184, 'income %d%% · age %d%% — the age gap now counts' % (round(sh2 * 100), round((1 - sh2) * 100)), GR, 'start'), show=4.4)
    f(T(0, 236, 'needed by KNN, SVM, k-means, regularised linear models, neural networks · not by trees', MU, 'start'), show=5.0)
    return f.render()

XV = [2, 4, 5, 6, 8, 40]
def f_scalers():
    mu = mean(XV); sd = (sum((x - mu) ** 2 for x in XV) / len(XV)) ** .5
    z = [(x - mu) / sd for x in XV]
    mm = [(x - min(XV)) / (max(XV) - min(XV)) for x in XV]
    f = Fig('fe9-', 700, 280, 'Six values 2, 4, 5, 6, 8 and an outlier 40 on a raw number line. Standardisation slides them '
            'to mean 0 and spread 1. Min-max slides them into 0 to 1, where the outlier sits at 1 and the other five are '
            'squeezed near 0.', 'SAME SIX VALUES · TWO SCALERS')
    lines = [('raw', XV, (0, 42), ['0', '20', '40']), ('standard', z, (-1, 3), ['-1', '0', '1', '2', '3']), ('min-max', mm, (0, 1), ['0', '0.5', '1'])]
    X0, W = 120, 520
    for k, (lab, vals, (a, b), ticks) in enumerate(lines):
        y = 60 + k * 80
        t = .3 + k * 1.6
        f(T(0, y + 4, lab, MU, 'start', 'sv-s') + L(X0, y, X0 + W, y, RULE_HI, 1.2), show=t)
        for q, tk in enumerate(ticks):
            v = a + (b - a) * q / (len(ticks) - 1)
            f(L(X0 + (v - a) / (b - a) * W, y - 4, X0 + (v - a) / (b - a) * W, y + 4, RULE_HI) +
              T(X0 + (v - a) / (b - a) * W, y + 20, tk, FA), show=t)
        for i, v in enumerate(vals):
            x = X0 + (v - a) / (b - a) * W
            out = i == 5
            if k == 0:
                f(dot(x, y, 'am' if out else 'bl', 6), show=t + .1 * i)
            else:
                pv = lines[k - 1][1][i]; pa, pb = lines[k - 1][2]
                px = X0 + (pv - pa) / (pb - pa) * W
                f(dot(x, y, 'am' if out else 'bl', 6), show=t + .2, move=(t + .2, px - x, -80, .9))
    f(T(0, 160, 'mean 0 · sd 1', GR, 'start'), show=2.4)
    f(T(X0, 220 + 34, 'outlier at 1 · the other five squeezed below %.2f' % max(mm[:5]), RD, 'start'), show=4.0)
    return f.render()

# ---------- 5.x New features ----------
def f_ratio():
    rows = [(120, 400), (60, 300), (200, 500), (90, 100)]
    f = Fig('fea-', 700, 240, 'A table with debt and income. A new column debt over income is computed row by row: 0.30, 0.20, '
            '0.40, 0.90. The fourth row, small in both raw columns, has by far the highest ratio, a risk neither raw column '
            'showed alone.', 'A RATIO SHOWS WHAT NEITHER COLUMN SHOWS')
    t = Table(0, 30, [('debt', 80), ('income', 80), ('debt / income', 110, 'new')])
    f(t.head())
    for i, (d, n) in enumerate(rows):
        f(t.row(i, [str(d), str(n), '']))
    f(t.colbox(2, 4, AM), show=.4, hide=3.6)
    for i, (d, n) in enumerate(rows):
        tt = .6 + i * .7
        f(t.outline(i, i, 0, 1, AM), show=tt, hide=tt + .7, d=.15)
        r = d / n
        f(t.cell(i, 2, '%.2f' % r, 'rd' if r > .5 else 'gr'), show=tt + .35, d=.2)
    f(leader(t.x + t.w, t.ry(3) + 13, 300, t.ry(3) + 13, 'smallest debt · highest risk', RD), show=3.6)
    f(T(300, 70, 'linear models only add columns —', MU, 'start') + T(300, 88, 'a ratio must be handed to them', MU, 'start'), show=4.2)
    return f.render()

def f_curve():
    # x and y = x^2 data; linear fit on x vs on x^2
    xs = [-3, -2, -1, 0, 1, 2, 3]
    ys = [x * x for x in xs]
    f = Fig('feb-', 700, 280, 'Points shaped like a U: y equals x squared. A straight line fitted on x stays flat and misses '
            'them all. After adding the column x squared, the same linear model draws the U through every point.',
            'ADD x² · A STRAIGHT-LINE MODEL BENDS')
    P = Plot(50, 36, 300, 200, (-3.5, 3.5), (-1, 10))
    f(P.axes('x', 'y'))
    for i, (x, y) in enumerate(zip(xs, ys)):
        f(dot(*P.p(x, y), 'bl'), show=.2 + i * .08)
    my = mean(ys)
    f(P.curve(lambda x: my, -3.3, 3.3, 2, RD, 2), show=1.2, hide=3.4)
    f(T(400, 70, 'model on x: ŷ = %.1f (flat)' % my, RD, 'start', 'sv-s'), show=1.4, hide=3.4)
    t = Table(400, 96, [('x', 50), ('x²', 60, 'new')])
    f(t.head(), show=2.4)
    for i, x in enumerate([-2, 0, 3]):
        f(t.row(i, [str(x), '']), show=2.4)
        f(t.cell(i, 1, str(x * x), 'gr'), show=2.7 + i * .2)
    f(P.curve(lambda x: x * x, -3.15, 3.15, 80, GR, 2.4), show=3.6, d=.6)
    f(T(400, 70, 'model on x²: ŷ = x² fits every point', GR, 'start', 'sv-s'), show=3.8)
    f(T(400, 244, 'same idea: log(x) for skewed columns', MU, 'start'), show=4.6)
    assert my == 4
    return f.render()

def f_time():
    ts = ['2024-03-09 21:40', '2024-03-11 08:15', '2024-03-15 13:05']
    import datetime
    d = [datetime.datetime.strptime(s, '%Y-%m-%d %H:%M') for s in ts]
    wd = [x.strftime('%a') for x in d]; hr = [x.hour for x in d]
    ref = datetime.datetime(2024, 3, 20)
    ago = [(ref - x).days for x in d]
    f = Fig('fec-', 700, 196, 'A raw timestamp column is split column by column into weekday %s, hour %s and days since, %s, '
            'counted up to the prediction date. A raw timestamp is a growing number; the parts carry cycles and recency.'
            % (', '.join(wd), ', '.join(map(str, hr)), ', '.join(map(str, ago))), 'ONE TIMESTAMP · THREE USEFUL COLUMNS')
    t = Table(0, 30, [('timestamp', 150), ('weekday', 80), ('hour', 60), ('days since', 90)])
    f(t.head())
    for i, s in enumerate(ts):
        f(t.row(i, [s, '', '', '']))
    cols = [wd, [str(h) for h in hr], [str(a) for a in ago]]
    for j, vals in enumerate(cols):
        tt = .6 + j * 1.2
        f(t.colbox(j + 1, 3, AM), show=tt, hide=tt + 1.1)
        for i, v in enumerate(vals):
            f(t.cell(i, j + 1, v, 'gr'), show=tt + .3 + i * .15, d=.2)
    f(t.dimcol(0, 3), show=4.4)
    f(T(0, 172, 'days since is cut at the prediction date (2024-03-20) — never later, or it leaks', MU, 'start'), show=4.6)
    assert wd == ['Sat', 'Mon', 'Fri'] and ago == [10, 8, 4]
    return f.render()

if __name__ == '__main__':
    splice(PAGE, [f_mental(), f_onehot(), f_ordinal(), f_target(), f_hash(), f_impute(), f_mnar(),
                  f_distance(), f_scalers(), f_ratio(), f_curve(), f_time()])
