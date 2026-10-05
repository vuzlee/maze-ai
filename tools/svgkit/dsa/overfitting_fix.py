# -*- coding: utf-8 -*-
"""Targeted fix: merge 1.1-1.3 into one three-panel figure; add L1 .eq in 3.2."""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import overfitting_regularization as O
from fitkit_bvof import *  # noqa

def three():
    an = Anim('uf3-', 900, 360, 'The same ten points fitted three ways side by side: a straight line misses them (underfit), a cubic follows the wave (good fit), a degree-9 polynomial passes through every point and swings between them (overfit). Under each panel the train and validation error.', 'SAME 10 POINTS · THREE MODELS', 2.5)
    an.static(R(30, 330, 12, 12, BR, 'none', 6) + T(48, 340, 'train point', MU, 'start') +
              '<circle cx="146" cy="336" r="5" fill="none" stroke="%s" stroke-width="1.4"/>' % VI + T(158, 340, 'validation point', MU, 'start'))
    specs = ((1, 'UNDERFIT', 'degree 1', 'both high'), (3, 'GOOD FIT', 'degree 3', 'both low, close'), (9, 'OVERFIT', 'degree 9', 'train 0, val high'))
    for i, (d, name, sub, verdict) in enumerate(specs):
        x0 = 40 + i * 290; t0 = .4 + i * 3.2
        w = O.fit(O.XS, O.YS, d); tr, va = O.errs(w)
        p, ax = fit_plot('uf3%d-' % i, x0, 52, 240, 170, (-2.0, 2.0))
        an.static(ax)
        an.show(R(x0 - 12, 26, 264, 290, 'none', BR, 8, 2), t0, hide=t0 + 3.0)
        an.show(T(x0, 42, name, FI, 'start', bold=True) + T(x0 + 240, 42, sub, MU, 'end', mono=True), t0)
        for k, (x, y) in enumerate(zip(O.XS, O.YS)): an.show(p.dot(x, y, BR, 3.4), .1 + k * .04)
        for x, y in zip(O.VX[::3], O.VY[::3]):
            an.show('<circle cx="%.1f" cy="%.1f" r="2.6" fill="none" stroke="%s" stroke-width="1.1"/>' % (p.px(x), p.py(y), VI), t0 + 1.4)
        p.draw(an, curve_pts(lambda x: O.pred(w, x), n=160), t0 + .3, 1.0, FI, 2.2, k=12)
        SC = 150 / .6
        for j, (lab, v, c) in enumerate((('train', tr, BR), ('val', va, VI))):
            y = 248 + j * 24; bw = max(min(v, .6) * SC, 2)
            an.show(T(x0, y + 13, lab, c, 'start', mono=True) + R(x0 + 42, y, bw, 16, c, 'none', 2) +
                    T(x0 + 48 + bw, y + 13, '%.2f%s' % (min(v, 9.99), '' if v <= .6 else ' ›'), c, 'start', bold=True, mono=True), t0 + 1.6 + j * .3)
        an.show(T(x0, 312, verdict, MU, 'start'), t0 + 2.3)
    return an.render()

if __name__ == '__main__':
    s = open(O.PAGE).read()
    a = s.index('  <div class="subsec" id="overfit-s1-1">'); b = s.index('    <ul class="why">', a)
    s = s[:a] + solid_brand(palette(three())) + "\n" + s[b:]
    s = s.replace(solid_brand(palette('')), '')
    eq = '''    <div class="eq">
      <div class="line">
        <span class="t"><span>penalty</span></span>
        <span class="op">=</span>
        <span class="t"><span><var>λ</var> Σ<sub>j</sub> |<var>w</var><sub>j</sub>|</span><em>sum of absolute weights</em></span>
      </div>
    </div>
'''
    k = s.index('<b>3.2</b>L1'); k = s.index('</p>\n', k) + 5
    if 'sum of absolute weights' not in s: s = s[:k] + eq + s[k:]
    open(O.PAGE, 'w').write(s)
