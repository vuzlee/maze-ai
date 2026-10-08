# -*- coding: utf-8 -*-
"""Model evaluation group overview (2026-10-09): a map of the group, not a lesson.

    01 Which metric      top-down tree: task -> one question -> metric; leaves link to the owning lesson
    02 Offline to online offline metric -> A/B test -> business metric (no child lesson owns it), redrawn
                         in the overview palette
    03 Learning order
Dropped: Mental model and "Three questions" 2.1-2.3 (ranking / decision / probability) - owned by
roc-auc-pr, metrics-confusion-matrix and calibration.
Run: python3 tools/svgkit/07-machine-learning/evaluation_overview.py   (re-runnable)
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from overview import Fig, text, arr, B, V, FL

ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
PAGE = os.path.join(ROOT, 'content/07-machine-learning/09-evaluation/evaluation-overview/index.html')
M, ROC, CAL = '../metrics-confusion-matrix/index.html', '../roc-auc-pr/index.html', '../calibration/index.html'

def which():
    f = Fig('evov1', 680, 300, 'WHICH METRIC · TASK → ONE QUESTION → METRIC',
            'A top-down tree. The root asks what the task is. Binary classification asks how the score is used: '
            'to rank, read ROC-AUC, or PR-AUC when positives are rare; to make a cut, read precision, recall and F1 '
            'at the threshold; as a probability, read calibration error and log loss. Multiclass asks whether some '
            'classes are rare: no gives accuracy, yes gives macro-F1. Regression asks whether big errors are very '
            'bad: no gives MAE, yes gives RMSE. Ranking asks whether only the top of the list matters: no gives '
            'MAP, yes gives NDCG at k. Leaves link to the lesson that owns the metric.')
    f.node(340, 50, 'What is the task?', '', 'filled', f.step(.2), None, None, w=160, h=34)
    cols = [('Binary', 'how is the score used?', 128, [('ROC, PR-AUC', 'rank', ROC), ('P · R · F1', 'a cut', M + '#metrics-s3'),
                                                      ('ECE, log loss', 'a probability', CAL)], 246),
            ('Multiclass', 'rare classes?', 336, [('accuracy', 'no', M + '#metrics-s6'), ('macro-F1', 'yes', M + '#metrics-s6')], 136),
            ('Regression', 'big errors very bad?', 482, [('MAE', 'no', M + '#metrics-s7'), ('RMSE', 'yes', M + '#metrics-s7')], 136),
            ('Ranking', 'only the top counts?', 620, [('MAP', 'no', None), ('NDCG', 'yes', None)], 120)]
    for i, (task, q, cx, leaves, cw) in enumerate(cols):
        t = .5 + i * .15
        f.edge((340, 67), (cx, 108), cls=f.step(t, draw=True))
        f.node(cx, 126, task, '', 'plain', f.step(t + .2), None, None, w=min(cw - 8, 120), h=34)
        f.add(f'<g class="{f.step(t + .3)}"><line x1="{cx}" y1="143" x2="{cx}" y2="160" stroke="var(--rule-hi)" stroke-width="1.4"/>'
              + text(cx, 174, q, 'sv-d', V, 'middle', ';font-style:italic') + '</g>')
        n = len(leaves); lw = (cw - (n - 1) * 6) / n; x0 = cx - cw / 2
        for j, (name, cond, href) in enumerate(leaves):
            lx = x0 + j * (lw + 6) + lw / 2
            f.edge((cx, 182), (lx, 226), cls=f.step(t + .6, draw=True))
            f.add(f'<g class="{f.step(t + .6)}">' + text(lx, 220, cond, 'sv-d', 'var(--muted)', 'middle', ';font-size:9.5px') + '</g>') if False else None
            dashed = href is None
            inner = (f'<rect class="nd" x="{lx - lw/2:.1f}" y="226" width="{lw:.1f}" height="44" rx="9" fill="var(--bg)" '
                     f'stroke="{"var(--rule-hi)" if dashed else B}" stroke-width="1.3"{" stroke-dasharray=\"4 3\"" if dashed else ""}/>'
                     + text(lx, 245, name, 'sv-s', 'var(--brand-hi)' if href else 'var(--text)', 'middle', ';font-weight:600;font-size:10px')
                     + text(lx, 260, cond, 'sv-d', 'var(--muted)', 'middle', ';font-size:9.5px'))
            if href:
                inner = f'<a href="{href}">{inner}</a>'
            f.add(f'<g class="{f.step(t + .8)}">{inner}</g>')
    f.add(f'<g class="{f.step(1.6)}">' + text(680, 290, 'dashed = no lesson in this group', 'sv-d', 'var(--muted)', 'end', ';font-size:9.5px') + '</g>')
    return f.svg()

def online():
    f = Fig('evov2', 680, 150, 'OFFLINE METRIC → A/B TEST → BUSINESS METRIC',
            'Three boxes left to right. The offline metric, scored on a test set, for example ROC-AUC 0.875. Then an A/B '
            'test on live users, half on the old model and half on the new. Then the business metric of the product: '
            'clicks or revenue. Under the first arrow: does it carry over? Under the second: is the gap real?')
    boxes = [('Offline metric', 'test set · ROC-AUC .875', 'filled'), ('A/B test', 'live users · old 50% / new 50%', 'violet'),
             ('Business metric', 'product · clicks, revenue', 'brand')]
    w = 196
    for i, (n, sub, tone) in enumerate(boxes):
        cx = i * 242 + w / 2
        f.node(cx, 74, n, sub, tone, f.step(.3 + i * .5), None, None, w=w, h=50)
        if i:
            x1 = (i - 1) * 242 + w + 4
            f.add(f'<g class="{f.step(.1 + i * .5)}">' + arr(x1, 74, x1 + 38) + '</g>')
    f.add(f'<g class="{f.step(1.6)}">' + text(219, 122, 'does it carry over?', 'sv-d', V, 'middle', ';font-style:italic')
          + text(461, 122, 'is the gap real?', 'sv-d', V, 'middle', ';font-style:italic') + '</g>')
    return f.svg()

def order():
    f = Fig('evov3', 680, 104, 'LEARNING ORDER · COUNTS FIRST, THEN THE CURVE, THEN THE VALUES',
            'Three stops in a row, each a link: Metric and confusion matrix, ROC-AUC and PR curve, Probability calibration.')
    stops = [('Metric & confusion matrix', 'one cut, four cells', M), ('ROC-AUC & PR curve', 'every cut at once', ROC),
             ('Probability calibration', 'is 0.8 really 80%?', CAL)]
    w, gap = 200, 40
    for i, (n, sub, href) in enumerate(stops):
        cx = i * (w + gap) + w / 2
        if i:
            f.add(f'<line class="{f.step(.4 + i * .35, draw=True)}" pathLength="1" x1="{cx - w/2 - gap + 2}" y1="62" '
                  f'x2="{cx - w/2 - 2}" y2="62" stroke="var(--rule-hi)" stroke-width="1.6"/>')
        f.node(cx, 62, n, sub, 'plain', f.step(.3 + i * .35), href, None, w=w, h=44)
    return f.svg()

BODY = '''<header class="hero">
  <p class="eyebrow">Machine learning · Model evaluation</p>
  <h1>Model evaluation <em>overview</em></h1>
  <p class="lede">One table of predictions answers <b>three separate questions</b> — is the order right, is the cut right, are the probabilities right — and each needs its own metric. This page picks the metric; the lessons explain it.</p>
</header>

<section id="evov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Which metric</h2></div>
  <p class="key">Task type first, then <em>one question about the data</em>, gives the main metric.</p>
<figure class="gist">
{f1}
</figure>
  <ul class="why">
    <li>With rare positives ROC-AUC stays high because its false-positive rate divides by the huge pile of 0s — read PR-AUC (<a href="../roc-auc-pr/index.html#roc-s4">Rare positives</a>).</li>
    <li>When FP and FN have known costs, pick the threshold that minimises <b>expected cost</b> (<a href="../metrics-confusion-matrix/index.html#metrics-s5">Threshold by cost</a>).</li>
    <li>Ranking metrics (MAP, NDCG@k) belong to search and recommendation systems. Measure on data the model never saw — <a href="../../04-core-concepts/train-val-test-cv/index.html">Train, validation &amp; test</a>.</li>
  </ul>
</section>

<section id="evov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Offline to online</h2></div>
  <p class="key">Every metric above is <em>offline</em>: it scores the model, not the product.</p>
<figure class="gist">
{f2}
</figure>
  <ul class="why">
    <li>A higher AUC often fails to move the product; check early that the offline metric tracks the business one.</li>
    <li>Whether the gap is real or noise is a statistics question — <a href="../../02-math-foundations/statistics/index.html#stats-s3">A/B testing</a>.</li>
  </ul>
</section>

<section id="evov-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Learning order</h2></div>
  <p class="key">Counts at one threshold first, then <em>every threshold at once</em>, then the score values themselves.</p>
<figure class="gist">
{f3}
</figure>
</section>

'''

def build():
    s = open(PAGE, encoding='utf-8').read()
    a = s.index('<header class="hero">')
    b = s.index('<script>\n/* Figures start')
    s = s[:a] + BODY.format(f1=which(), f2=online(), f3=order()) + s[b:]
    blurb = ('The model evaluation group on one page: a top-down guide from task to the right metric, how offline '
             'metrics meet the product, and the order to learn them.')
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s"' % blurb, s, count=1)
    open(PAGE, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    build(); print('ok')
