# -*- coding: utf-8 -*-
"""Machine learning shelf overview: gallery, taxonomy tree, AI summers & winters.

    python3 tools/svgkit/07-machine-learning/ml_overview.py   # rewrites figures in place
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from overview import Fig, text, gallery, cell, dot, ln, arr, B, V, FL, TINT, VTINT

PAGE = 'content/07-machine-learning/01-overview/ml-overview/index.html'
C = '../../05-classical-ml/'; T = '../../06-tree-models/'; K = '../../07-clustering/'
D = '../../08-dimensionality/'; CC = '../../04-core-concepts/'; E = '../../09-evaluation/'
M = ';font-size:8.5px'

def t(x, y, s, col='var(--muted)', a='middle', ex=M):
    return text(x, y, s, 'sv-d', col, a, ex)

def pt(x, y, c=0, r=2.6):
    col = [B, V, FL][c]
    fill = ['rgba(var(--clay-a),.25)', 'rgba(var(--violet-a),.3)', 'rgba(var(--blue-a),.25)'][c]
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{col}" stroke-width="1"/>'

def path(d, col=V, w=1.6, dash=False):
    ds = ' stroke-dasharray="3 2"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}"{ds}/>'

def axes(x, y, w=136, h=58):
    return ln(x + 2, y + h, x + w, y + h, 'var(--rule-hi)') + ln(x + 2, y, x + 2, y + h, 'var(--rule-hi)')

# ---- models ----
def d_reg(x, y):
    P = [(12, 46), (26, 42), (38, 36), (52, 38), (66, 28), (80, 26), (94, 20), (108, 16), (122, 10)]
    o = axes(x, y) + path(f'M{x+6},{y+50} L{x+132},{y+6}', V, 1.8)
    return o + ''.join(pt(x + a, y + b + (4 if i % 2 else -3)) for i, (a, b) in enumerate(P))
def d_logit(x, y):
    o = f'<path d="M{x+60},{y} L{x+100},{y+58} L{x+138},{y+58} L{x+138},{y}z" fill="rgba(var(--violet-a),.08)"/>'
    o += path(f'M{x+60},{y} L{x+100},{y+58}', V, 1.8)
    A = [(14, 12), (30, 30), (20, 46), (46, 20), (52, 48), (36, 8)]
    Bb = [(96, 14), (112, 34), (126, 10), (120, 50), (84, 6), (130, 28)]
    return o + ''.join(pt(x + a, y + b, 0) for a, b in A) + ''.join(pt(x + a, y + b, 1) for a, b in Bb)
def d_tree(x, y):
    o = ln(x + 69, y + 12, x + 34, y + 36) + ln(x + 69, y + 12, x + 104, y + 36)
    o += cell(x + 40, y + 2, 58, 15) + t(x + 69, y + 12.5, 'size > 50?', 'var(--text)')
    o += cell(x + 8, y + 36, 52, 15) + t(x + 34, y + 46.5, 'age > 3?', 'var(--text)')
    o += cell(x + 84, y + 36, 40, 15, '', True) + t(x + 104, y + 46.5, 'yes', V)
    o += t(x + 46, y + 28, 'no') + t(x + 92, y + 28, 'yes')
    return o
def d_knn(x, y):
    o = f'<circle cx="{x+69}" cy="{y+29}" r="24" fill="rgba(var(--violet-a),.07)" stroke="{V}" stroke-width="1.2" stroke-dasharray="3 2"/>'
    P = [(52, 18, 1), (84, 20, 1), (60, 44, 0), (86, 40, 1), (20, 10, 0), (118, 12, 0), (16, 48, 0), (124, 50, 1)]
    o += ''.join(pt(x + a, y + b, c) for a, b, c in P)
    return o + f'<rect x="{x+65}" y="{y+25}" width="8" height="8" fill="var(--bg)" stroke="{V}" stroke-width="1.4" transform="rotate(45 {x+69} {y+29})"/>'
def d_svm(x, y):
    o = path(f'M{x+40},{y+58} L{x+98},{y}', V, 1.8)
    o += path(f'M{x+24},{y+58} L{x+82},{y}', 'var(--muted)', 1, True) + path(f'M{x+56},{y+58} L{x+114},{y}', 'var(--muted)', 1, True)
    o += ''.join(pt(x + a, y + b, 0) for a, b in ((10, 20), (20, 44), (30, 10), (52, 18), (40, 42)))
    o += ''.join(pt(x + a, y + b, 1) for a, b in ((104, 22), (118, 44), (126, 14), (86, 42), (100, 54)))
    return o
def d_kmeans(x, y):
    o = ''
    for c, (cx, cy) in enumerate(((26, 18), (104, 16), (66, 46))):
        for dx, dy in ((-10, -4), (8, -8), (-6, 9), (10, 6), (0, -12), (-12, 6)):
            o += pt(x + cx + dx, y + cy + dy, c, 2.2)
        o += f'<path d="M{x+cx-4},{y+cy-4} L{x+cx+4},{y+cy+4} M{x+cx+4},{y+cy-4} L{x+cx-4},{y+cy+4}" stroke="{[B,V,FL][c]}" stroke-width="2"/>'
    return o
def d_pca(x, y):
    o = ''
    for i in range(14):
        a = (i - 6.5) * 8.4
        b = math.sin(i * 2.3) * 8
        o += pt(x + 69 + a * .95 - b * .3, y + 29 - a * .33 - b * .9 + 4, 2, 2.2)
    o += path(f'M{x+6},{y+52} L{x+132},{y+6}', V, 1.8) + path(f'M{x+60},{y+8} L{x+76},{y+50}', 'var(--muted)', 1, True)
    return o + t(x + 136, y + 18, 'PC1', V, 'end')
def d_forest(x, y):
    o = ''
    for k in range(4):
        bx = x + 4 + k * 34
        P = [(bx + 14, y + 6), (bx + 6, y + 24), (bx + 22, y + 24), (bx + 2, y + 42), (bx + 10, y + 42)]
        o += ''.join(ln(*P[a], *P[b]) for a, b in ((0, 1), (0, 2), (1, 3), (1, 4)))
        o += ''.join(dot(px, py, '', k == 1 and i in (0, 1, 4), 3.4) for i, (px, py) in enumerate(P))
    return o + t(x + 69, y + 58, 'vote of many trees')

# ---- measure ----
def d_split(x, y):
    o = ''
    for a, w, lab, hl in ((2, 84, 'train 70%', False), (88, 22, 'val', False), (112, 24, 'test', True)):
        o += f'<rect x="{x+a}" y="{y+18}" width="{w}" height="18" rx="3" fill="{VTINT if hl else TINT}" stroke="{V if hl else B}" stroke-width="1.1"/>'
        o += t(x + a + w / 2, y + 30.5, lab, V if hl else 'var(--text)')
    return o + t(x + 124, y + 52, 'touch once', V)
def d_bv(x, y):
    o = ''
    for k, (cx, sx, sy, off) in enumerate(((34, 4, 4, 14), (104, 12, 12, 0))):
        for r in (22, 14, 6):
            o += f'<circle cx="{x+cx}" cy="{y+28}" r="{r}" fill="none" stroke="var(--rule-hi)" stroke-width="1"/>'
        for i in range(6):
            o += pt(x + cx + off * .7 + math.cos(i * 1.7) * sx, y + 28 - off * .5 + math.sin(i * 2.1) * sy, 1, 2)
    return o + t(x + 34, y + 62, 'high bias') + t(x + 104, y + 62, 'high variance')
def d_fit(x, y):
    P = [(8 + i * 14, 30 - 18 * math.sin(i * .7) + (5 if i % 2 else -5)) for i in range(10)]
    o = path(f'M{x+4},{y+40} L{x+134},{y+18}', 'var(--muted)', 1.1, True)
    d = 'M' + ' L'.join(f'{x+a:.1f},{y+b:.1f}' for a, b in P)
    o += path(d, 'var(--rose)', 1.2)
    o += path('M' + ' L'.join(f'{x+4+i*2.6:.1f},{y+30-18*math.sin((i*2.6-4)/14*.7):.1f}' for i in range(51)), V, 1.8)
    return o + ''.join(pt(x + a, y + b, 0, 2.2) for a, b in P)
def d_cm(x, y):
    o = ''
    for r in range(2):
        for c in range(2):
            on = r == c
            o += cell(x + 34 + c * 40, y + 4 + r * 24, 38, 22, ['TP', 'FN', 'FP', 'TN'][r * 2 + c], on)
    return o + t(x + 26, y + 18, 'yes', 'var(--muted)', 'end') + t(x + 26, y + 42, 'no', 'var(--muted)', 'end')
def d_roc(x, y):
    o = axes(x + 20, y, 100, 56) + path(f'M{x+22},{y+56} L{x+120},{y}', 'var(--muted)', 1, True)
    o += f'<path d="M{x+22},{y+56} C{x+26},{y+10} {x+50},{y+2} {x+120},{y} L{x+120},{y+56}z" fill="rgba(var(--violet-a),.08)"/>'
    o += path(f'M{x+22},{y+56} C{x+26},{y+10} {x+50},{y+2} {x+120},{y}', V, 1.8)
    return o + t(x + 84, y + 40, 'AUC', V)

def d_cv(x, y):
    o = ''
    for r in range(4):
        for c in range(4):
            o += cell(x + 18 + c * 26, y + 2 + r * 14, 25, 12, '', c == r)
    return o
def d_pr(x, y):
    o = axes(x + 20, y, 100, 56)
    o += f'<path d="M{x+22},{y+4} C{x+70},{y+6} {x+96},{y+14} {x+120},{y+50}" fill="none" stroke="{V}" stroke-width="1.8"/>'
    return o + t(x + 12, y + 8, 'P') + t(x + 120, y + 66, 'recall', 'var(--muted)', 'end')
def d_calib(x, y):
    o = axes(x + 20, y, 100, 56) + path(f'M{x+22},{y+56} L{x+120},{y}', 'var(--muted)', 1, True)
    P = [(30, 52), (46, 48), (62, 40), (78, 26), (94, 12), (110, 6)]
    o += path('M' + ' L'.join(f'{x+a},{y+b}' for a, b in P), V, 1.6)
    return o + ''.join(pt(x + a, y + b, 1, 2.2) for a, b in P)

def fig_gallery():
    f = Fig('mlov1', 680, 500, 'THE WHOLE SHELF · EIGHT MODELS, EIGHT WAYS TO MEASURE THEM',
            'Two bands of pictures. Models: a regression line through points, a logistic decision boundary '
            'between two classes, a decision tree asking threshold questions, k-nearest neighbours inside a circle, '
            'an SVM line with its margin, k-means clusters with their centres, a PCA axis along the spread of the '
            'data, and a random forest of small trees voting. Measure: a train, validation and test split, '
            'bias and variance as dots on targets, under- and over-fitted curves against a good fit, a two by two '
            'confusion matrix, a ROC curve with the area under it, a precision–recall curve, k-fold cross-validation and a calibration curve. Each tile links to its lesson.')
    bands = [('MODELS', 'what learns the rule', [
        ('Linear regression', d_reg, C + 'linear-regression/index.html'),
        ('Logistic regression', d_logit, C + 'logistic-regression/index.html'),
        ('Decision tree', d_tree, T + 'decision-tree/index.html'),
        ('k-NN', d_knn, C + 'knn/index.html'),
        ('SVM · margin', d_svm, C + 'svm/index.html'),
        ('k-means', d_kmeans, K + 'kmeans-clustering/index.html'),
        ('PCA', d_pca, D + 'pca-dimensionality/index.html'),
        ('Random forest', d_forest, T + 'random-forest/index.html')]),
        ('MEASURE', 'is the rule any good on new data', [
        ('Train · val · test', d_split, CC + 'train-val-test-cv/index.html'),
        ('Bias · variance', d_bv, CC + 'bias-variance-tradeoff/index.html'),
        ('Under · over-fit', d_fit, CC + 'overfitting-regularization/index.html'),
        ('Confusion matrix', d_cm, E + 'metrics-confusion-matrix/index.html'),
        ('ROC curve', d_roc, E + 'roc-auc-pr/index.html'),
        ('Precision–recall', d_pr, E + 'roc-auc-pr/index.html'),
        ('k-fold CV', d_cv, CC + 'train-val-test-cv/index.html'),
        ('Calibration', d_calib, E + 'calibration/index.html')])]
    f.h = gallery(f, bands) + 6
    return f.svg()

def fig_tax():
    f = Fig('mlov3', 680, 400, 'TAXONOMY · WHAT KIND OF LABEL → WHICH TASK → WHICH MODEL FAMILY',
            'A top-down tree. Machine learning splits by the kind of label. Supervised learning has an answer for '
            'each row; it splits into regression, predicting a number, and classification, predicting a class. '
            'Unsupervised learning has no labels; it splits into clustering and dimensionality reduction. '
            'Reinforcement learning has only a reward after actions. Under each task sit the model families that '
            'solve it: linear and ridge or lasso for regression; logistic, k-NN, SVM, naive Bayes and tree '
            'ensembles for classification; k-means, DBSCAN and HDBSCAN for clustering; PCA for dimensionality.')
    P = {'ml': (340, 54), 'sup': (190, 140), 'uns': (500, 140), 'rl': (630, 140),
         'reg': (80, 226), 'cls': (280, 226), 'clu': (450, 226), 'dim': (590, 226)}
    def bot(k): return (P[k][0], P[k][1] + 20)
    def top(k): return (P[k][0], P[k][1] - 20)
    for a, b, d in (('ml', 'sup', .5), ('ml', 'uns', .5), ('ml', 'rl', .5), ('sup', 'reg', 1.3), ('sup', 'cls', 1.3),
                    ('uns', 'clu', 1.3), ('uns', 'dim', 1.3)):
        f.edge(bot(a), top(b), cls=f.step(d, draw=True))
    a = f.step(.2)
    f.node(*P['ml'], 'Machine learning', 'rules from data', 'brand', a, None, None, w=160, h=42)
    b = f.step(.9)
    f.node(*P['sup'], 'Supervised', 'every row has a label', 'filled', b, CC + 'supervised-unsupervised/index.html', None, w=164, h=40)
    f.node(*P['uns'], 'Unsupervised', 'no labels', 'filled', b, CC + 'supervised-unsupervised/index.html', None, w=124, h=40)
    f.node(*P['rl'], 'Reinforcement', 'reward later', 'plain', b, None, None, w=112, h=40, dashed=True)
    c = f.step(1.7)
    f.node(*P['reg'], 'Regression', 'a number', 'plain', c, None, None, w=124, h=40)
    f.node(*P['cls'], 'Classification', 'a class', 'plain', c, None, None, w=136, h=40)
    f.node(*P['clu'], 'Clustering', 'groups', 'plain', c, K + 'clustering-overview/index.html', None, w=112, h=40)
    f.node(*P['dim'], 'Dimensionality', 'fewer columns', 'plain', c, None, None, w=128, h=40)
    leaves = {
        'reg': [('Linear', C + 'linear-regression/index.html'), ('Ridge · Lasso', C + 'ridge-lasso-elasticnet/index.html'), ('Trees', T + 'tree-family-overview/index.html')],
        'cls': [('Logistic', C + 'logistic-regression/index.html'), ('k-NN', C + 'knn/index.html'), ('SVM', C + 'svm/index.html'),
                ('Naive Bayes', C + 'naive-bayes/index.html'), ('Random forest', T + 'random-forest/index.html'), ('Boosting', T + 'gradient-boosting/index.html')],
        'clu': [('k-means', K + 'kmeans-clustering/index.html'), ('DBSCAN', K + 'dbscan/index.html'), ('HDBSCAN', K + 'hdbscan/index.html')],
        'dim': [('PCA', D + 'pca-dimensionality/index.html')],
    }
    for i, (k, ls) in enumerate(leaves.items()):
        cx, cy = P[k]
        y = cy + 42
        for j, (name, href) in enumerate(ls):
            yy = y + j * 27 if k != 'cls' else y + (j % 3) * 27
            xx = cx if k != 'cls' else cx - 52 + (j // 3) * 104
            f.add(ln(xx, cy + 20, xx, yy - 11, 'var(--rule-hi)', 1) if j in (0, 3) and k == 'cls' or j == 0 else '')
            f.pill(xx, yy, name, 'violet' if k == 'cls' else 'brand', f.step(2.3 + i * .15 + j * .05), href, w=92, anchor='middle')
    f.add(f'<g class="{f.step(3.4)}">' + text(630, 176, 'not on this shelf', 'sv-d', 'var(--faint)') + '</g>')
    f.h = 226 + 42 + 2 * 27 + 24
    return f.svg()

def fig_summers():
    W, H = 680, 284
    f = Fig('mlov4', W, H, 'AI SUMMERS & WINTERS · INTEREST AND FUNDING, 1950–2020',
            'A curve of interest and funding in AI from 1950 to 2020, drawing in from left to right. It rises to a '
            'peak around 1960 with the perceptron, falls into the first AI winter from about 1974 to 1980, rises '
            'to a second peak in the mid 1980s with expert systems, falls into the second winter from about 1987 to '
            '1993, climbs steadily through the 2000s with SVMs, trees and boosting, then shoots up after 2012 with '
            'deep learning. Winters are shaded.')
    x0, x1, yb, yt = 30, 670, 250, 50
    X = lambda yr: x0 + (yr - 1950) / 70 * (x1 - x0)
    pts = [(1950, .08), (1956, .22), (1960, .42), (1965, .38), (1970, .28), (1974, .12), (1978, .09), (1981, .2),
           (1985, .5), (1987, .44), (1990, .14), (1993, .12), (1997, .22), (2002, .3), (2007, .36), (2011, .42),
           (2014, .62), (2017, .84), (2020, .96)]
    Y = lambda v: yb - v * (yb - yt)
    s0 = f.step(.1)
    o = ''
    for a, b, lab in ((1974, 1980, 'first winter'), (1987, 1993, 'second winter')):
        o += f'<rect x="{X(a):.1f}" y="{yt-10}" width="{X(b)-X(a):.1f}" height="{yb-yt+10}" fill="rgba(var(--rose-a),.10)"/>'
        o += text((X(a) + X(b)) / 2, yt + 4, lab, 'sv-d', 'var(--rose)', 'middle', ';font-weight:600')
    o += ln(x0, yb, x1, yb, 'var(--rule-hi)')
    for yr in range(1950, 2021, 10):
        o += ln(X(yr), yb, X(yr), yb + 4, 'var(--rule-hi)') + text(X(yr), yb + 16, str(yr), 'sv-d', 'var(--faint)', 'middle', ';font-family:var(--mono)')
    o += text(x0, 40, 'interest · funding', 'sv-d', 'var(--muted)', 'start')
    f.add(f'<g class="{s0}">{o}</g>')
    # smooth path through points (Catmull-Rom)
    P = [(X(a), Y(v)) for a, v in pts]
    d = f'M{P[0][0]:.1f},{P[0][1]:.1f}'
    for i in range(len(P) - 1):
        p0 = P[i - 1] if i else P[i]; p1, p2 = P[i], P[i + 1]; p3 = P[i + 2] if i + 2 < len(P) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    # the curve draws in slowly, left to right (longer than a normal overview edge)
    f.add('<style>@media (prefers-reduced-motion:no-preference){.mlov4-c{stroke-dasharray:1;stroke-dashoffset:1;'
          'animation:mlov4-c 2.6s ease-in-out .4s 1 forwards}}@keyframes mlov4-c{to{stroke-dashoffset:0}}</style>')
    f.add(f'<path class="mlov4-c" pathLength="1" d="{d}" fill="none" stroke="var(--brand)" stroke-width="2.4"/>')
    peaks = [(1959, .41, 'Perceptron', 'one neuron learns', 1.0),
             (1985, .5, 'Expert systems', 'hand-written rules', 1.6),
             (2000, .28, 'SVMs · trees', 'boosting wins tables', 2.2),
             (2014, .62, 'Deep learning', 'GPUs + big data', 2.8)]
    for yr, v, a, b, dl in peaks:
        x, y = X(yr), Y(v)
        g = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="var(--bg)" stroke="var(--violet)" stroke-width="1.6"/>'
             + ln(x, y - 6, x, y - 22, 'var(--violet)', 1)
             + text(x, y - 38, a, 'sv-s', 'var(--violet)', 'middle', ';font-weight:600')
             + text(x, y - 26, b, 'sv-d', 'var(--muted)', 'middle'))
        f.add(f'<g class="{f.step(dl)}">{g}</g>')
    return f.svg()

def put(html, sec_id, svg):
    i = html.index(f'id="{sec_id}"')
    a = html.index('<svg', i)
    b = html.index('</svg>', a) + 6
    return html[:a] + svg + html[b:]

if __name__ == '__main__':
    s = open(PAGE, encoding='utf-8').read()
    s = put(s, 'mlov-s1', fig_gallery())
    s = put(s, 'mlov-s3', fig_tax())
    s = put(s, 'mlov-s4', fig_summers())
    open(PAGE, 'w', encoding='utf-8').write(s)
    print('ok')
