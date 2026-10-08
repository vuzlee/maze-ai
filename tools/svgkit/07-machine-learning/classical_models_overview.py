# -*- coding: utf-8 -*-
"""Classical models group overview (2026-10-09): a map of the group, not a lesson.

    01 Six pictures      gallery: each model's own picture (line, sigmoid, shrink, margin, k-NN circle, bells)
    02 Which model       top-down decision tree: label type -> data shape -> model, leaves link
    03 Comparison        the lookup table (kept as HTML table, rows link)
    04 Learning order    the existing figure from dsa/classical_models_overview.py, carried over as is
Dropped: Mental model (f-hat = argmin over a family) and the two-data-shapes figure; the six-models-on-
one-dataset panel is dropped too (each lesson draws its own boundary).
Run: python3 tools/svgkit/07-machine-learning/classical_models_overview.py   (re-runnable)
"""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from overview import Fig, text, gallery, ln, dot, B, V, FL, TINT, VTINT

ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
PAGE = os.path.join(ROOT, 'content/07-machine-learning/05-classical-ml/classical-models-overview/index.html')
L = {'lin': '../linear-regression/index.html', 'log': '../logistic-regression/index.html',
     'rid': '../ridge-lasso-elasticnet/index.html', 'svm': '../svm/index.html',
     'knn': '../knn/index.html', 'nb': '../naive-bayes/index.html'}
R = 'var(--rose)'

def axes(x, y):
    return ln(x, y + 56, x + 136, y + 56, 'var(--rule-hi)') + ln(x, y, x, y + 56, 'var(--rule-hi)')

def g_lin(x, y):
    pts = [(12, 46), (26, 40), (40, 42), (54, 30), (70, 32), (86, 22), (100, 20), (118, 10)]
    o = axes(x, y) + ln(x + 4, y + 50, x + 130, y + 6, V, 1.6)
    for a, b in pts:
        lineY = 50 - (a - 4) * 44 / 126
        o += ln(x + a, y + b, x + a, y + lineY, R, .8, True)
        o += dot(x + a, y + b, '', False, 2.6)
    return o

def g_log(x, y):
    p = ' '.join(f'{x + 4 + i*4.2:.1f},{y + 52 - 46/(1+math.exp(-(i-15)/3)):.1f}' for i in range(31))
    o = axes(x, y) + f'<polyline points="{p}" fill="none" stroke="{V}" stroke-width="1.6"/>'
    o += ln(x + 4, y + 29, x + 134, y + 29, 'var(--muted)', .8, True)
    o += text(x + 134, y + 25, 'p = 0.5', 'sv-d', 'var(--muted)', 'end', ';font-size:8.5px')
    for a in (10, 22, 34, 46): o += dot(x + a, y + 52, '', False, 2.6)
    for a in (88, 104, 118, 128): o += dot(x + a, y + 6, '', True, 2.6)
    return o

def g_rid(x, y):
    o = ln(x, y + 30, x + 136, y + 30, 'var(--rule-hi)')
    ws = [22, -16, 12, -8, 18]
    for i, w in enumerate(ws):
        cx = x + 10 + i * 26
        o += f'<rect x="{cx}" y="{y + 30 - max(w,0):.1f}" width="8" height="{abs(w)}" fill="none" stroke="var(--rule-hi)" stroke-dasharray="2 2"/>'
        sw = w * .45 if i % 2 == 0 else 0
        if sw:
            o += f'<rect x="{cx}" y="{y + 30 - max(sw,0):.1f}" width="8" height="{abs(sw):.1f}" fill="{VTINT}" stroke="{V}"/>'
        else:
            o += text(cx + 4, y + 33.5 + (8 if w > 0 else -10), '0', 'sv-d', R, 'middle', ';font-size:8.5px;font-family:var(--mono)')
    return o + text(x + 136, y + 58, 'shrunk · some exactly 0', 'sv-d', 'var(--muted)', 'end', ';font-size:8.5px')

def g_svm(x, y):
    o = ''
    for k, dash, col in ((-12, True, 'var(--muted)'), (0, False, V), (12, True, 'var(--muted)')):
        o += ln(x + 30 + k, y + 58, x + 106 + k, y - 2, col, 1.5 if not dash else .9, dash)
    for a, b in ((10, 14), (22, 30), (8, 40), (36, 12), (51, 23)):
        o += dot(x + a, y + b, '', False, 3)
    for a, b in ((102, 50), (118, 30), (128, 46), (88, 52), (85, 34)):
        o += dot(x + a, y + b, '', True, 3)
    return o + f'<circle cx="{x+51}" cy="{y+23}" r="6" fill="none" stroke="{FL}" stroke-dasharray="2 2"/>'

def g_knn(x, y):
    o = f'<circle cx="{x+68}" cy="{y+28}" r="24" fill="rgba(var(--blue-a),.06)" stroke="{FL}" stroke-dasharray="3 2"/>'
    for a, b, h in ((52, 18, 1), (80, 14, 1), (60, 44, 0), (84, 38, 1), (74, 26, 1), (20, 12, 0), (16, 46, 0), (118, 16, 1), (122, 48, 0), (34, 30, 0)):
        o += dot(x + a, y + b, '', bool(h), 3)
    return o + f'<rect x="{x+65}" y="{y+25}" width="6" height="6" fill="var(--bg)" stroke="{FL}" stroke-width="1.4"/>'

def g_nb(x, y):
    o = ln(x, y + 54, x + 136, y + 54, 'var(--rule-hi)')
    for mu, col in ((44, B), (92, V)):
        p = ' '.join(f'{x + i*4.4:.1f},{y + 54 - 44*math.exp(-((i*4.4-mu)/16)**2/2):.1f}' for i in range(32))
        o += f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="1.5"/>'
    return o + text(x + 44, y + 6, 'A', 'sv-d', B, 'middle', ';font-weight:600') + text(x + 92, y + 6, 'B', 'sv-d', V, 'middle', ';font-weight:600')

def pictures():
    f = Fig('clsov1', 680, 0, 'SIX MODELS · EACH ONE’S OWN PICTURE',
            'Six tiles, one per model, each a link to its lesson. Linear regression: a line through points with '
            'residuals. Logistic regression: an S-shaped sigmoid from 0 to 1 with the 0.5 threshold. Ridge and Lasso: '
            'weight bars shrunk toward zero, some exactly zero. SVM: a separating line with the widest margin on both '
            'sides and a support vector circled. KNN: a query point and a circle around its nearest neighbours. Naive '
            'Bayes: one bell curve per class.')
    items = [('Linear regression', g_lin, L['lin']), ('Logistic regression', g_log, L['log']),
             ('Ridge / Lasso', g_rid, L['rid']), ('SVM', g_svm, L['svm']),
             ('KNN', g_knn, L['knn']), ('Naive Bayes', g_nb, L['nb'])]
    bot = gallery(f, [('ONE PICTURE PER MODEL', 'click a tile for the lesson', items)], top=40, cols=3, tw=221, th=104)
    f.h = bot + 6
    return f.svg()

def which():
    f = Fig('clsov2', 680, 330, 'WHICH MODEL · READ TOP DOWN',
            'A top-down decision tree. Start: what is the label? A number leads to linear regression, or to Ridge '
            'and Lasso when there are many correlated features. A class leads to a second question: what does the '
            'data look like? Text or very sparse counts lead to Naive Bayes. Few samples with many dimensions lead '
            'to SVM. Few dimensions with a curved border lead to KNN. Otherwise, or when you need probabilities, '
            'logistic regression. Every leaf links to its lesson.')
    a = f.step(.2)
    f.node(340, 56, 'What is the label?', '', 'filled', a, None, None, w=170, h=36)
    P = {'num': (110, 136), 'cls': (455, 136)}
    for k, lab in (('num', 'a number'), ('cls', 'a class')):
        f.edge((340, 74), (P[k][0], P[k][1] - 18), cls=f.step(.5, draw=True))
        f.add(f'<g class="{f.step(.7)}">' + text((340 + P[k][0]) / 2 + (-10 if k == 'num' else 10), 100, lab, 'sv-d', V,
                                                'end' if k == 'num' else 'start', ';font-style:italic') + '</g>')
    b = f.step(.9)
    f.node(*P['num'], 'Many correlated features?', '', 'plain', b, None, None, w=196, h=36)
    f.node(*P['cls'], 'What does the data look like?', '', 'plain', b, None, None, w=212, h=36)
    leaves = [('lin', 'Linear regr.', 'no', L['lin']), ('rid', 'Ridge / Lasso', 'yes', L['rid']),
              ('nb', 'Naive Bayes', 'text · sparse', L['nb']), ('svm', 'SVM', 'small n, wide', L['svm']),
              ('knn', 'KNN', 'few dims, curved', L['knn']), ('log', 'Logistic regr.', 'else · need p', L['log'])]
    w, gap = 106, 8.8
    for i, (k, name, cond, href) in enumerate(leaves):
        x = i * (w + gap) + w / 2
        src = P['num'] if k in ('lin', 'rid') else P['cls']
        t = 1.3 + i * .2
        f.edge((src[0], src[1] + 18), (x, 250 - 22), cls=f.step(t, draw=True))
        f.node(x, 250, name, cond, 'violet' if k == 'log' else 'plain', f.step(t + .3), href, None, w=w, h=44)
    f.h = 290
    return f.svg()

BODY = '''<header class="hero">
  <p class="eyebrow">Machine learning · Classical models</p>
  <h1>Classical models <em>overview</em></h1>
  <p class="lede">None of these six models <b>was created to fix another</b>. They are six different <em>assumptions</em> about the shape of the data — this page is the map; each picture opens its lesson.</p>
</header>

<section id="clsov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Six pictures</h2></div>
  <p class="key">Each model is one picture you can draw from memory: <em>a line, an S-curve, shrunk weights, a margin, a circle of neighbours, a bell per class</em>.</p>
<figure class="gist">
{f1}
</figure>
  <ul class="why">
    <li>The picture is the assumption: a model can only fit data that looks like its picture.</li>
  </ul>
</section>

<section id="clsov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Which model</h2></div>
  <p class="key">Two questions pick the model: <em>what is the label</em>, then <em>what does the data look like</em>.</p>
<figure class="gist">
{f2}
</figure>
  <ul class="why">
    <li>All six <b>need scaled features</b> (Naive Bayes the least) — the group's most common silent bug; see <a href="../../04-core-concepts/feature-engineering/index.html">Feature engineering</a>.</li>
    <li>On large tabular data all six usually lose to <a href="../../06-tree-models/tree-family-overview/index.html">tree ensembles</a>; they stay as baselines.</li>
  </ul>
</section>

<section id="clsov-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Comparison</h2></div>
  <p class="key">Read the <em>Believes that…</em> column first: which assumption does your data look like?</p>
{table}
</section>

<section id="clsov-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Learning order</h2></div>
  <p class="key">The first two lessons are <em>required, in order</em>; the other four open from there.</p>
<figure class="gist">
{f4}
</figure>
  <ul class="why">
    <li>Start: <a href="../linear-regression/index.html">Linear regression</a>. Prerequisites: <a href="../../02-math-foundations/calculus/index.html">calculus</a> and <a href="../../04-core-concepts/bias-variance-tradeoff/index.html">bias–variance</a>.</li>
  </ul>
</section>

'''

def build():
    s = open(PAGE, encoding='utf-8').read()
    a = s.index('<header class="hero">')
    b = s.index('<script>\n/* Figures start')
    old = s[a:b]
    table = re.search(r'  <table>.*?</table>', old, re.S).group(0)
    ordsec = old[old.index('<h2>Learning order</h2>'):]
    f4 = re.search(r'<svg.*?</svg>', ordsec, re.S).group(0)
    s = s[:a] + BODY.format(f1=pictures(), f2=which(), table=table, f4=f4) + s[b:]
    blurb = ('The classical models group on one page: each model’s own picture, a top-down guide to which model '
             'to pick, a comparison table and the order to learn them.')
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s"' % blurb, s, count=1)
    open(PAGE, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    build(); print('ok')
