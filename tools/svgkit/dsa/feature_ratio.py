# -*- coding: utf-8 -*-
"""Feature engineering 5.1 Ratios and interactions — general form, worked row by row.
Run: python3 feature_ratio.py -> replaces the figure inside subsection 5.1 of the page."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from linear_algebra import Anim, T, R, L, MU, TX, FA, BR, VI, FI, RO, RULE, RULE_HI, BG, tn, M, S, finish
PAGE = os.path.join(HERE, '../../../content/07-machine-learning/04-core-concepts/feature-engineering/index.html')

ROWS = [(120, 400), (60, 300), (200, 500), (90, 100)]

def fig():
    f = Anim('fer-', 720, 0, 'Two raw columns x1 and x2 become two new ones: the ratio x1 / x2 and the product x1 times x2. '
             'Each row is computed in turn, with the arithmetic shown beside it. The last row has the smallest x1 but the '
             'largest ratio, 0.90.', 'TWO COLUMNS → NEW FEATURES · x₁ / x₂ AND x₁ · x₂')
    cols = [(40, 'x₁', 'debt'), (130, 'x₂', 'income'), (240, 'x₁ / x₂', 'ratio'), (350, 'x₁ · x₂', 'interaction')]
    Y0, RH = 92, 34
    for k, (cx, sym, name) in enumerate(cols):
        new = k >= 2
        c = VI if new else TX
        f.show(M(cx, 52, sym.replace('x', '{x}'), c), .2 + (.5 if new else 0))
        f.show(T(cx, 70, name, MU, cls='sv-d'), .2 + (.5 if new else 0))
    f.static(L(0, 78, 400, 78, RULE_HI, 1.2))
    for i, (a, b) in enumerate(ROWS):
        y = Y0 + i * RH
        f.static(R(0, y - 22, 400, 30, BG, RULE_HI, 4, 1) + T(40, y - 2, str(a), TX, mono=True) + T(130, y - 2, str(b), TX, mono=True))
    t = 1.2
    for i, (a, b) in enumerate(ROWS):
        y = Y0 + i * RH
        last = i == len(ROWS) - 1
        f.show(R(-3, y - 25, 182, 36, tn(VI, '.08'), VI, 6, 1.8), t, hide=t + 1.3)
        f.show(M(430, y - 2, '%d / %d = %.2f' % (a, b, a / b), VI, 'start'), t + .2, hide=t + 1.3)
        f.show(M(570, y - 2, '%d · %d' % (a, b), MU, 'start'), t + .2, hide=t + 1.3)
        tone = RO if last else FI
        f.show(R(192, y - 20, 96, 26, tn(tone, '.14'), tone, 4, 1.2) + T(240, y - 2, '%.2f' % (a / b), tone, mono=True), t + .6)
        f.show(R(302, y - 20, 96, 26, tn(BR, '.12'), BR, 4, 1.2) + T(350, y - 2, '{:,}'.format(a * b), BR, mono=True), t + .8)
        t += 1.4
    yl = Y0 + 3 * RH
    f.show(L(240, yl + 8, 240, yl + 22, RO, 1, '3 3') + T(240, yl + 36, 'smallest x₁, highest ratio', RO, cls='sv-d'), t)
    f.show(T(0, 262, 'general form', MU, 'start') + M(100, 262, '{x}′ = {f}({x}₁, {x}₂)', TX, 'start'), t + .5)
    f.show(T(0, 284, 'ratio · product · difference — any rule a linear model cannot build on its own', MU, 'start'), t + .7)
    return finish(f, 300)

if __name__ == '__main__':
    h = open(PAGE).read()
    m = re.search(r'(<div class="subsec" id="[a-z-]+-s5-1">.*?)(<figure class="gist">.*?</figure>)', h, re.S)
    if not m:
        sys.exit('subsection 5.1 not found')
    h = h[:m.start(2)] + fig() + h[m.end(2):]
    open(PAGE, 'w').write(h)
    print('ok')
