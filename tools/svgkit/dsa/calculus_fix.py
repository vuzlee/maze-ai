# -*- coding: utf-8 -*-
"""Targeted fix for calculus: new 1.3 Common derivatives (sigmoid figure) + convex formulas and chord.
Run: python3 calculus_fix.py  (edits the page in place, idempotent)."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from calculus import (Anim, T, L, MU, FA, BR, VI, FI, RO, S, M, dot, ball, poly, Plane, finish, curve, PAGE, fig_convex as _fc)

sig = lambda x: 1 / (1 + math.exp(-x))
def fig_sigmoid():
    f = Anim('ca8-', 720, 0, 'The sigmoid curve and, below it, its derivative computed as sigma times one minus sigma. A probe slides '
             'from x = -4 to 4; its tangent slope is read off as the height of the derivative curve: 0.018, 0.105, 0.25 at the '
             'center, then back down. The slope is largest at 0 and nearly flat in the tails.', 'SIGMOID AND ITS SLOPE σ′ = σ(1 − σ)')
    P = Plane(270, 200, 38, 150)
    f.static(L(P.X(-6), P.Y(0), P.X(6), P.Y(0), MU, 1.2) + L(P.X(0), P.Y(0) + 4, P.X(0), P.Y(1) - 8, MU, 1))
    for k in (-4, -2, 2, 4):
        f.static(T(P.X(k), P.Y(0) + 16, str(k), FA, cls='sv-d'))
    f.static(L(P.X(-6), P.Y(1), P.X(6), P.Y(1), 'var(--rule)', 1, '3 4') + T(P.X(-6) - 6, P.Y(1) + 4, '1', FA, 'end', 'sv-d'))
    f.static(poly(curve(P, sig, -6, 6), BR, 2.4) + S(P.X(3.2), P.Y(sig(3.2)) - 12, 'σ(x)', BR, 'start', True))
    d = lambda x: sig(x) * (1 - sig(x))
    f.show(poly(curve(P, d, -6, 6), FI, 2.4) + S(P.X(1.4), P.Y(.25) - 8, 'σ′(x)', FI, 'start', True), .4, d=.6)
    xs = [-4, -2, 0, 2, 4]
    b0 = P(xs[0], sig(xs[0]))
    t0s = [1.2 + 1.3 * i for i in range(len(xs))]
    f.path(ball(*b0, VI, 7), [(0, 0, 0)] + [(t, P.X(x) - b0[0], P.Y(sig(x)) - b0[1]) for t, x in zip(t0s[1:], xs[1:])], t0s[0] - .3, d=.5)
    for i, (t, x) in enumerate(zip(t0s, xs)):
        last = i == len(xs) - 1
        hide = None if last else t0s[i + 1]
        m = d(x); px, py = P(x, sig(x)); qx, qy = P(x, m)
        a, b = P(x - 1.2, sig(x) - 1.2 * m), P(x + 1.2, sig(x) + 1.2 * m)
        f.show(L(a[0], a[1], b[0], b[1], VI, 2) + L(px, py + 8, qx, qy - 6, VI, 1, '2 3') + dot(qx, qy, FI, 5), t + .4, hide=hide)
        f.show(T(560, 90, 'x = %g' % x, VI, 'start', mono=True, bold=True) +
               T(560, 114, 'σ = %.3f' % sig(x), BR, 'start', mono=True) +
               T(560, 138, 'slope = %.3f' % m, FI, 'start', mono=True, bold=True), t + .4, hide=hide)
    f.show(S(30, 248, 'steepest at x = 0, where σ′ = 0.25 — the most a sigmoid can pass back', FI, 'start', True), t0s[-1] + 1.2)
    f.show(S(30, 270, 'in the flat tails σ′ ≈ 0: the source of vanishing gradients', MU), t0s[-1] + 1.6)
    return finish(f, 286)

def fig_convex():
    """Existing figure + a chord on the convex bowl that stays above the curve."""
    src = _fc()
    f1 = lambda w: .35 * (w - 3) ** 2 + .5
    P = Plane(30, 196, 52, 30)
    a, b = P(.9, f1(.9)), P(5.2, f1(5.2))
    g = Anim('ca7c-', 10, 10, '')
    g.show(L(a[0], a[1], b[0], b[1], VI, 2, '6 4') + dot(*a, VI, 4) + dot(*b, VI, 4), 7.0)
    xm = 2.4; cm = P(xm, f1(.9) + (f1(5.2) - f1(.9)) * (xm - .9) / 4.3); km = P(xm, f1(xm))
    g.show(L(cm[0], cm[1], km[0], km[1], FI, 2) + S(cm[0] - 6, cm[1] - 8, 'chord ≥ curve', VI, 'end', True), 7.5)
    r = g.render()
    style = re.search(r'<style>(.*?)</style>', r, re.S).group(1)
    body = re.search(r'</style>\n(.*)\n</svg>', r, re.S).group(1)
    src = src.replace('</style>', style + '</style>', 1).replace('\n</svg>', '\n' + body + '\n</svg>', 1)
    return src.replace('reaches the deeper global minimum.', 'reaches the deeper global minimum. A dashed chord joins two points on the '
                       'convex bowl and stays above the curve everywhere between them.')

EQ_D = '''  <div class="eq">
    <div class="line">
      <span class="t"><span>(<var>x</var><sup><var>n</var></sup>)′</span></span><span class="op">=</span>
      <span class="t b"><span><var>n</var> <var>x</var><sup><var>n</var>−1</sup></span><em>power rule</em></span>
    </div>
    <div class="line">
      <span class="t"><span>(<var>e</var><sup><var>x</var></sup>)′</span></span><span class="op">=</span>
      <span class="t b"><span><var>e</var><sup><var>x</var></sup></span><em>its own slope</em></span>
    </div>
    <div class="line">
      <span class="t"><span>(log <var>x</var>)′</span></span><span class="op">=</span>
      <span class="t b"><span><span class="frac"><i>1</i><i><var>x</var></i></span></span><em>behind log-loss gradients</em></span>
    </div>
    <div class="line">
      <span class="t"><span><var>σ</var>′(<var>x</var>)</span></span><span class="op">=</span>
      <span class="t g"><span><var>σ</var>(<var>x</var>) (1 − <var>σ</var>(<var>x</var>))</span><em>sigmoid: reuses its own output</em></span>
    </div>
  </div>
'''
EQ_C = '''  <div class="eq">
    <div class="line">
      <span class="t"><span><var>f</var>″(<var>x</var>)</span></span><span class="op">≥</span>
      <span class="t"><span>0</span><em>curve bends upward everywhere</em></span>
    </div>
    <div class="line">
      <span class="t b"><span><var>f</var>(<var>t</var><var>x</var> + (1−<var>t</var>)<var>y</var>)</span><em>curve between x and y</em></span>
      <span class="op">≤</span>
      <span class="t p"><span><var>t</var> <var>f</var>(<var>x</var>) + (1−<var>t</var>) <var>f</var>(<var>y</var>)</span><em>chord between them, 0 ≤ t ≤ 1</em></span>
    </div>
  </div>
'''

if __name__ == '__main__':
    s = open(PAGE).read()
    s = re.sub(r'\n  <div class="subsec" id="calc-s1-3">.*?\n  </div>\n(?=</section>)', '\n', s, flags=re.S)
    new = ('  <div class="subsec" id="calc-s1-3">\n    <h3 class="ssh"><b>1.3</b>Common derivatives</h3>\n'
           '    <p class="skey">Four slopes cover most of ML; the sigmoid one reuses the value already computed.</p>\n' + EQ_D +
           fig_sigmoid() + '\n    <ul class="why">\n      <li>Chain these with the chain rule below and you can differentiate any layer by hand.</li>\n'
           '      <li>σ′ never exceeds 0.25, so a deep stack of sigmoids shrinks the gradient at every layer.</li>\n    </ul>\n  </div>\n')
    i = s.index('</section>', s.index('id="calc-s1-2"'))
    s = s[:i] + new + s[i:]
    a = s.index('<figure', s.index('id="calc-s4"')); b = s.index('</figure>', a) + len('</figure>')
    s = s[:a] + fig_convex() + s[b:]
    if 'f</var>″(' not in s[s.index('id="calc-s4"'):]:
        s = s.replace(s[a:a + 0], '', 1)
        s = s[:a] + EQ_C + s[a:]
    open(PAGE, 'w').write(s); print('ok')
