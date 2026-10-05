# -*- coding: utf-8 -*-
"""Calculus 2.1 chain rule and 2.2 vanishing/exploding, redrawn as worked math.
Run: python3 calculus_chain.py  -> replaces the ca3- and ca4- figures in the page."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from linear_algebra import Anim, T, R, L, MU, TX, FA, BR, VI, FI, RO, RULE, BG, tn, M, S, dot, poly, Plane, finish
PAGE = os.path.join(HERE, '../../../content/07-machine-learning/02-math-foundations/calculus/index.html')

def frac(cx, cy, num, den, c=TX, w=None):
    """A stacked fraction in LaTeX style: numerator, rule, denominator, centred on (cx, cy)."""
    w = w or max(len(re.sub(r'\{|\}', '', num)), len(re.sub(r'\{|\}', '', den))) * 9 + 12
    return M(cx, cy - 7, num, c) + L(cx - w / 2, cy, cx + w / 2, cy, c, 1.1) + M(cx, cy + 17, den, c)

def hl(cx, cy, w, h=50, c=VI):
    return R(cx - w / 2, cy - h / 2 + 2, w, h, tn(c, '.12'), c, 8, 1.6)

def fig_chain():
    f = Anim('cc1-', 720, 0, 'The chain rule worked out. u = 2x + 1 and y = u squared, at x = 3. First u = 7 and y = 49 are '
             'computed. Then dy/dx is written as dy/du times du/dx; each factor is filled in: dy/du = 2u = 14, du/dx = 2. '
             'The product gives dy/dx = 28.', 'CHAIN RULE · y = (2x + 1)² AT x = 3')
    # line 1: the two functions + forward values
    f.static(M(40, 50, '{u} = 2{x} + 1', TX, 'start') + M(220, 50, '{y} = {u}²', TX, 'start'))
    f.show(M(40, 80, '{x} = 3  →  {u} = 7  →  {y} = 49', BR, 'start'), .5)
    # line 2: the product of fractions
    Y = 150
    xs = {'lhs': 70, 'eq1': 120, 'a': 175, 'dot': 232, 'b': 290, 'eq2': 350}
    f.show(frac(xs['lhs'], Y, 'd{y}', 'd{x}') + M(xs['eq1'], Y + 5, '=') + frac(xs['a'], Y, 'd{y}', 'd{u}') +
           M(xs['dot'], Y + 5, '·') + frac(xs['b'], Y, 'd{u}', 'd{x}'), 1.4)
    # step: dy/du
    t = 2.6
    f.show(hl(xs['a'], Y, 70), t, hide=t + 1.6)
    f.show(M(xs['a'], Y + 62, '2{u} = 2·7 = 14', VI), t + .3)
    f.show(L(xs['a'], Y + 30, xs['a'], Y + 46, VI, 1.2, '3 3'), t + .3)
    t += 1.8
    f.show(hl(xs['b'], Y, 70), t, hide=t + 1.6)
    f.show(M(xs['b'] + 30, Y + 62, '2', VI), t + .3)
    f.show(L(xs['b'], Y + 30, xs['b'] + 24, Y + 46, VI, 1.2, '3 3'), t + .3)
    t += 1.8
    f.show(M(xs['eq2'], Y + 5, '=', TX) + M(xs['eq2'] + 18, Y + 5, '14 · 2', TX, 'start'), t)
    f.show(M(xs['eq2'] + 80, Y + 5, '=', TX) + R(xs['eq2'] + 96, Y - 16, 48, 32, FI, FI, 6) +
           M(xs['eq2'] + 120, Y + 6, '28', 'var(--on-fill)'), t + .8)
    # check by expanding
    f.show(M(40, 260, 'check: {y} = (2{x}+1)²  ⇒  {y}′ = 2(2{x}+1)·2 = 4(7) = 28  ✓', MU, 'start'), t + 1.8)
    return finish(f, 284)

def fig_vanish():
    f = Anim('cc2-', 720, 0, 'The gradient after n layers is a product of n slopes, about c to the power n. Three small plots: '
             'c = 0.5 decays toward 0, c = 1 stays flat, c = 1.4 grows exponentially to about 29 at n = 10.',
             'n SLOPES MULTIPLIED · ≈ cⁿ')
    N = 10
    panels = [(.5, VI, '{c} = 0.5', 'vanishes', 1.0), (1.0, BR, '{c} = 1', 'stable', 1.6), (1.4, RO, '{c} = 1.4', 'explodes', 30)]
    for k, (c, col, lab, word, ymax) in enumerate(panels):
        x0, W, H, y0 = 30 + k * 236, 190, 150, 210
        P = Plane(x0, y0, W / N, H / ymax)
        f.static(L(x0, y0, x0 + W + 6, y0, MU, 1.1) + L(x0, y0, x0, y0 - H - 6, MU, 1.1))
        f.static(M(x0 + W + 12, y0 + 5, '{n}', MU, 'start') + T(x0, y0 + 16, '0', FA, cls='sv-d') + T(x0 + W, y0 + 16, '10', FA, cls='sv-d'))
        f.static(T(x0 - 6, P.Y(1) + 4, '1', FA, 'end', 'sv-d') + L(x0, P.Y(1), x0 + W, P.Y(1), RULE, 1, '2 4'))
        t0 = .5 + k * 1.4
        f.show(M(x0 + W / 2, 52, lab, col), t0)
        pts = [P(n / 10, c ** (n / 10)) for n in range(N * 10 + 1)]
        for i in range(0, len(pts) - 1, 10):
            f.show(poly(pts[i:i + 11], col, 2.6), t0 + .2 + i / len(pts), d=.08)
        f.show(dot(*pts[-1], col, 4.5), t0 + 1.2)
        f.show(T(x0 + W / 2, 246, word, col, cls='sv-s', bold=True), t0 + 1.3)
    assert round(1.4 ** 10) == 29
    return finish(f, 262)

if __name__ == '__main__':
    h = open(PAGE).read()
    for pre, fn in (('cc1-', fig_chain), ('cc2-', fig_vanish)):
        m = re.search(r'<figure class="gist">\s*<svg[^>]*><style>@keyframes %sa1.*?</figure>' % pre, h, re.S)
        if not m:
            sys.exit('figure %s not found' % pre)
        h = h[:m.start()] + fn() + h[m.end():]
    open(PAGE, 'w').write(h)
    print('ok')
