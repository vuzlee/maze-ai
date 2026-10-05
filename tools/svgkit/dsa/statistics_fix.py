# -*- coding: utf-8 -*-
"""Targeted fix for statistics: new 1.4 Sample mean and standard error (+ figure), power = 1 - beta line.
Run: python3 statistics_fix.py  (edits the page in place)."""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from engine import Anim, T, R, L, MU, FA
PAGE = os.path.join(HERE, '../../../content/07-machine-learning/02-math-foundations/statistics/index.html')
BR, VI, FI = 'var(--brand)', 'var(--violet)', 'var(--filled)'
def dot(x, y, c, r=4): return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" fill-opacity=".75"/>' % (x, y, r, c)

def fig_se():
    MU0, SIG = 50., 10.
    f = Anim('se-', 720, 300, 'Forty repeated samples are drawn at each size n = 4, 16 and 64 from a population with mean 50 and '
             'standard deviation 10; each sample mean is one dot. The dots spread out by about 5 at n = 4, 2.5 at n = 16 and 1.25 '
             'at n = 64: the standard error sigma over root n halves every time n is multiplied by four.',
             'STANDARD ERROR · THE SPREAD OF x̄ SHRINKS AS n GROWS', 1.5)
    x0, x1, lo, hi = 90, 520, 35., 65.
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    f.static(L(x0, 250, x1, 250, MU, 1.2))
    for v in range(35, 66, 5):
        f.static(L(X(v), 250, X(v), 254, MU, 1) + T(X(v), 267, str(v), FA, mono=True))
    f.static(L(X(MU0), 42, X(MU0), 250, FI, 1.6, '4 3') + T(X(MU0), 34, 'μ = 50', FI, bold=True))
    rnd = random.Random(7)
    for k, n in enumerate((4, 16, 64)):
        y = 80 + k * 62; t = .5 + k * 2.0
        se = SIG / math.sqrt(n)
        f.static(T(x0 - 14, y + 4, 'n = %d' % n, MU, 'end', mono=True, bold=True))
        means = [sum(rnd.gauss(MU0, SIG) for _ in range(n)) / n for _ in range(40)]
        for i, m in enumerate(means):
            jit = ((i * 7) % 5 - 2) * 4
            f.show(dot(X(max(lo, min(hi, m))), y + jit, BR), t + i * .025, d=.2)
        sd = math.sqrt(sum((m - MU0) ** 2 for m in means) / 39)
        f.show(R(X(MU0 - se), y - 16, X(MU0 + se) - X(MU0 - se), 32, 'rgba(var(--violet-a),.12)', VI, 4, 1.2) +
               T(x1 + 14, y + 4, 'SE = 10/√%d = %.2f' % (n, se), VI, 'start', mono=True, bold=True), t + 1.3)
        assert abs(sd - se) / se < .35, (n, sd, se)
    return f.render()

EQ = '''  <div class="eq">
    <div class="line">
      <span class="t"><span><var>x̄</var></span></span><span class="op">=</span>
      <span class="t b"><span><span class="frac"><i>1</i><i><var>n</var></i></span> Σ <var>x</var><sub><var>i</var></sub></span><em>sample mean</em></span>
    </div>
    <div class="line">
      <span class="t"><span><var>s</var><sup>2</sup></span></span><span class="op">=</span>
      <span class="t b"><span><span class="frac"><i>1</i><i><var>n</var> − 1</i></span> Σ (<var>x</var><sub><var>i</var></sub> − <var>x̄</var>)<sup>2</sup></span><em>sample variance: n − 1 because x̄ was fitted to the data</em></span>
    </div>
    <div class="line">
      <span class="t"><span>SE</span></span><span class="op">=</span>
      <span class="t p"><span><span class="frac"><i><var>σ</var></i><i>√<var>n</var></i></span></span><em>spread of x̄; use s when σ is unknown</em></span>
    </div>
  </div>
'''
s = open(PAGE).read()
if 'id="stats-s1-6"' not in s:
    s = s.replace('id="stats-s1-5"', 'id="stats-s1-6"').replace('<b>1.5</b>Multiple', '<b>1.6</b>Multiple')
    s = s.replace('id="stats-s1-4"', 'id="stats-s1-5"').replace('<b>1.4</b>Confidence', '<b>1.5</b>Confidence')
    new = ('  <div class="subsec" id="stats-s1-4">\n    <h3 class="ssh"><b>1.4</b>Sample mean and standard error</h3>\n'
           '    <p class="skey">One sample gives one mean; repeat the sample and the means scatter by σ/√n.</p>\n' + fig_se() + '\n' + EQ +
           '    <ul class="why">\n      <li>Standard deviation describes the <b>data</b>; standard error describes the <b>estimate</b>.</li>\n'
           '      <li>Four times the data halves the SE — the √n behind every sample-size formula.</li>\n    </ul>\n  </div>\n')
    i = s.index('  <div class="subsec" id="stats-s1-5">')
    s = s[:i] + new + s[i:]
    pw = '''    <div class="line">
      <span class="t"><span>power</span></span><span class="op">=</span>
      <span class="t g"><span>1 − <var>β</var></span><em>chance of catching a real effect</em></span>
    </div>
'''
    j = s.index('<div class="eq">', s.index('id="stats-s1-3"')) + len('<div class="eq">\n')
    s = s[:j] + pw + s[j:]
open(PAGE, 'w').write(s); print('ok')
