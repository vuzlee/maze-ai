# -*- coding: utf-8 -*-
"""Figures + page body for content/07-machine-learning/02-math-foundations/calculus.
Run: python3 calculus.py"""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, BR, VI, FI, RO, GH, RULE, SUNK, BG,
                            tn, M, S, chip, dot, ball, poly, Plane, finish, splice)

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/02-math-foundations/calculus/index.html')

def curve(P, fn, x0, x1, n=120):
    return [P(x0 + (x1 - x0) * i / n, fn(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]

def axes(P, x0, x1, y0, y1, xl='{w}', yl='{L}'):
    a = L(P.X(x0), P.Y(y0), P.X(x1) + 10, P.Y(y0), MU, 1.2) + L(P.X(x0), P.Y(y0), P.X(x0), P.Y(y1) - 6, MU, 1.2)
    return a + M(P.X(x1) + 16, P.Y(y0) + 5, xl, MU, 'start') + M(P.X(x0), P.Y(y1) - 12, yl, MU)

# ---------- 1.1 Derivative = slope ----------
def fig_slope():
    fn = lambda x: .5 * x * x
    f = Anim('ca1-', 720, 0, 'The curve y = x squared over 2. A point sits at x = 2. A second point at x = 2 + h joins it with a '
             'secant line; h shrinks from 2 to 1 to 0.5 to 0.1, and the secant turns into the tangent. Its slope '
             'settles at 2, the derivative at x = 2.', 'DERIVATIVE = SLOPE OF THE TANGENT')
    P = Plane(60, 280, 70, 28)
    f.static(axes(P, 0, 4.2, 0, 8.6, '{x}', '{y}'))
    for k in range(1, 5):
        f.static(T(P.X(k), P.Y(0) + 16, str(k), FA, cls='sv-d'))
    f.static(poly(curve(P, fn, 0, 4.1), BR, 2.4))
    x0 = 2
    px, py = P(x0, fn(x0))
    hs = [2, 1, .5, .1]
    for k, h in enumerate(hs):
        t0 = .8 + k * 1.5
        last = k == len(hs) - 1
        x1 = x0 + h
        m = (fn(x1) - fn(x0)) / h
        a, b = P(x0 - .9, fn(x0) - .9 * m), P(x0 + 1.9, fn(x0) + 1.9 * m)
        f.show(L(a[0], a[1], b[0], b[1], FI if last else VI, 2 if last else 1.5, None if last else '5 3'), t0, hide=None if last else t0 + 1.4)
        if not last:
            q = P(x1, fn(x1))
            f.show(dot(q[0], q[1], VI, 5) + L(px, py, q[0], py, VI, 1, '2 3') + L(q[0], py, q[0], q[1], VI, 1, '2 3'),
                   t0, hide=t0 + 1.4)
        f.show(T(400, 120, 'h = %g' % h, VI, 'start', mono=True, bold=True) +
               T(400, 144, 'slope = %.2f' % m, FI if last else VI, 'start', mono=True, bold=True), t0, hide=None if last else t0 + 1.4)
    f.static(dot(px, py, BR, 5.5))
    f.show(S(400, 186, 'h → 0 : the secant becomes the tangent', MU), 6.0)
    f.show(S(400, 208, 'derivative of x²/2 at x = 2 is 2', FI, 'start', True), 6.4)
    f.show(S(400, 236, 'slope > 0 : going right goes up', MU), 6.8)
    return finish(f, 306)

# ---------- 1.2 Gradient ----------
def fig_gradient():
    fx = lambda x, y: (x * x + 3 * y * y)
    f = Anim('ca2-', 720, 0, 'Contour lines of the loss L = w1 squared + 3 w2 squared, a bowl seen from above. At the point (2, 1) '
             'the slope along w1 is 4 and along w2 is 6; the two arrows add up to the gradient (4, 6), which points '
             'straight uphill, across the contours. Its opposite points downhill.', 'GRADIENT = ALL SLOPES IN ONE ARROW')
    P = Plane(200, 175, 38)
    f.static(P.grid(-4, 4, -3.6, 3.6, labels=False, xl='{w}₁', yl='{w}₂'))
    for k, c in enumerate((1, 3, 6, 11, 16)):
        a, b = math.sqrt(c), math.sqrt(c / 3)
        pts = [P(a * math.cos(2 * math.pi * i / 72), b * math.sin(2 * math.pi * i / 72)) for i in range(73)]
        f.static(poly(pts, BR, 1.2).replace('/>', ' opacity="%.2f"/>' % (.35 + .1 * k)))
    f.static(dot(*P(0, 0), BR, 3.5))
    w = (2, 1)
    g = (2 * w[0], 6 * w[1])
    assert g == (4, 6)
    p = P(*w)
    sc = .25
    f.show(dot(*p, VI, 5.5), .4)
    ex = P(w[0] + g[0] * sc, w[1])
    f.show(arrow(p[0], p[1], ex[0], ex[1], VI, 2) + T(ex[0] + 6, ex[1] + 14, '∂L/∂w₁ = 4', VI, 'start', 'sv-d'), 1.2)
    ey = P(w[0], w[1] + g[1] * sc)
    f.show(arrow(p[0], p[1], ey[0], ey[1], VI, 2) + T(ey[0] - 6, ey[1] + 4, '∂L/∂w₂ = 6', VI, 'end', 'sv-d'), 2.0)
    eg = P(w[0] + g[0] * sc, w[1] + g[1] * sc)
    f.show(L(ex[0], ex[1], eg[0], eg[1], VI, 1, '3 3') + L(ey[0], ey[1], eg[0], eg[1], VI, 1, '3 3'), 2.8)
    f.show(arrow(p[0], p[1], eg[0], eg[1], FI, 2.8, None, 10) + T(eg[0] + 8, eg[1] + 4, '∇L', FI, 'start', bold=True), 3.2)
    dn = P(w[0] - g[0] * .12, w[1] - g[1] * .12)
    f.show(arrow(p[0], p[1], dn[0], dn[1], RO, 2.4, '5 3', 9) + T(dn[0] - 6, dn[1] + 16, '−∇L', RO, 'end', bold=True), 4.4)
    X = 430
    f.show(S(X, 70, 'at w = (2, 1)', MU), .4)
    f.show(T(X, 96, '∇L = (4, 6)', FI, 'start', mono=True, bold=True), 3.2)
    f.show(S(X, 126, '∇L points straight uphill,', MU) + S(X, 144, 'across the contour lines', MU), 3.6)
    f.show(S(X, 176, '−∇L: the fastest way down', RO, 'start', True), 4.6)
    f.show(S(X, 206, 'long arrow = steep · short = near the bottom', MU), 5.2)
    return finish(f, 330)

# ---------- 2. Chain rule ----------
def fig_chain():
    x = 3
    u = 2 * x + 1          # 7
    y = u * u              # 49
    du_dx, dy_du = 2, 2 * u
    assert (u, y, dy_du * du_dx) == (7, 49, 28)
    f = Anim('ca3-', 720, 0, 'A pipeline of two boxes. Forward: x = 3 enters u = 2x + 1 and becomes 7, then y = u squared and '
             'becomes 49. Backward: each box hands its local slope back: 14 from the second box, times 2 from the first, '
             'gives dy/dx = 28.', 'CHAIN RULE · VALUES FLOW FORWARD, SLOPES MULTIPLY BACKWARD')
    Y = 70
    xs = [40, 270, 500, 680]
    boxes = [(155, 'u = 2x + 1', 'local slope 2'), (385, 'y = u²', 'local slope 2u = 14')]
    for cx, lab, _ in boxes:
        f.static(R(cx - 70, Y, 140, 56, BG, RULE_HI, 8, 1.3) + M(cx, Y + 33, re.sub(r'([xyu])', r'{\1}', lab), TX))
    for k, (a, b) in enumerate([(70, 85), (225, 315), (455, 560)]):
        f.static(arrow(a, Y + 28, b, Y + 28, RULE_HI, 1.4))
    vals = [('x = 3', 40), ('u = 7', 270), ('y = 49', 610)]
    # forward
    for k, (s, cx) in enumerate(vals):
        t0 = .5 + k * 1.1
        if k:
            f.path(chip(cx, Y + 28 - 22, s, BR), [(0, -60 if k == 1 else -90, 0), (t0, 0, 0)], t0 - .3, d=.7)
        else:
            f.show(chip(cx, Y + 28 - 22, s, BR, 60), t0)
        if k:
            f.show(R(boxes[k - 1][0] - 72, Y - 2, 144, 60, 'none', VI, 9, 2), t0 - .5, hide=t0 + .4)
    f.show(S(0, Y - 24, 'forward', BR, 'start', True), .5)
    # backward
    YB = Y + 100
    f.show(S(0, YB + 70, 'backward', FI, 'start', True), 4.0)
    f.show(R(boxes[1][0] - 72, Y - 2, 144, 60, 'none', FI, 9, 2), 4.2, hide=5.2)
    f.show(T(boxes[1][0], YB, 'dy/du = 2u = 14', FI, mono=True, bold=True), 4.4)
    f.show(arrow(560, YB + 30, 455, YB + 30, FI, 1.6), 4.4)
    f.show(R(boxes[0][0] - 72, Y - 2, 144, 60, 'none', FI, 9, 2), 5.4, hide=6.4)
    f.show(T(boxes[0][0], YB, 'du/dx = 2', FI, mono=True, bold=True), 5.6)
    f.show(arrow(315, YB + 30, 225, YB + 30, FI, 1.6), 5.6)
    f.show(chip(boxes[1][0], YB + 30, '× 14', FI, 54), 4.6)
    f.show(chip(boxes[0][0], YB + 30, '× 2', FI, 48), 5.8)
    f.show(T(xs[0] - 40, YB + 30 + 5, '', FI), 6.6)
    f.show(chip(560, YB + 70 - 5, 'dy/dx = 14 × 2 = 28', FI, 180), 6.8)
    f.show(S(0, YB + 104, 'a deep network = many boxes; backprop multiplies one slope per layer', MU), 7.4)
    return finish(f, YB + 120)

# ---------- 2.2 Vanishing / exploding ----------
def fig_vanish():
    f = Anim('ca4-', 720, 0, 'The gradient after passing back through n layers, each multiplying it by a factor. With factor 0.5 '
             'it shrinks toward zero within ten layers; with 1.0 it stays flat; with 1.5 it explodes past 50.',
             'MULTIPLY MANY SLOPES · THE PRODUCT VANISHES OR EXPLODES')
    P = Plane(70, 270, 50, 6.4)
    N = 10
    f.static(axes(P, 0, N, 0, 32, 'layers', 'gradient size'))
    for k in range(0, N + 1, 2):
        f.static(T(P.X(k), P.Y(0) + 16, str(k), FA, cls='sv-d'))
    for v in (10, 20, 30):
        f.static(T(P.X(0) - 8, P.Y(v) + 4, str(v), FA, 'end', 'sv-d') + L(P.X(0), P.Y(v), P.X(N), P.Y(v), RULE, 1, '2 4'))
    lines = [(.5, VI, 'factor 0.5 → vanishes to 0.001'), (1.0, BR, 'factor 1.0 → stays 1'), (1.4, RO, 'factor 1.4 → explodes to 29')]
    for k, (fac, c, lab) in enumerate(lines):
        pts = [(n, fac ** n) for n in range(N + 1)]
        t0 = .6 + k * 1.6
        f.show(poly([P(a, b) for a, b in pts], c, 2.4), t0, d=.8)
        for a, b in pts:
            f.show(dot(*P(a, b), c, 3.2), t0 + .1 * a)
        ex = pts[-1]
        f.show(L(110, 60 + k * 22, 130, 60 + k * 22, c, 2.4) + S(138, 64 + k * 22, lab, c, 'start', True), t0 + .9)
    assert round(1.4 ** 10) == 29 and round(.5 ** 10, 3) == .001
    f.show(S(70, 300, 'ReLU, careful init, normalization and skip connections all keep the factor near 1', MU), 5.4)
    return finish(f, 316)

# ---------- 3.1 Gradient descent ----------
def fig_gd():
    fn = lambda w: (w - 3) ** 2 + 1
    d = lambda w: 2 * (w - 3)
    eta = .3
    ws = [0.2]
    for _ in range(6):
        ws.append(ws[-1] - eta * d(ws[-1]))
    f = Anim('ca5-', 720, 0, 'The loss curve L = (w − 3) squared + 1. A ball starts at w = 0.2. At each step the tangent shows the '
             'slope, and the ball moves against it by learning rate 0.3 times the slope. Steps get shorter as the slope '
             'flattens; the ball settles at the bottom, w = 3.', 'GRADIENT DESCENT · A BALL ROLLING DOWNHILL')
    P = Plane(60, 270, 64, 24)
    f.static(axes(P, 0, 6, 0, 10.2))
    for k in range(1, 7):
        f.static(T(P.X(k), P.Y(0) + 16, str(k), FA, cls='sv-d'))
    f.static(poly(curve(P, fn, 0, 6), BR, 2.4))
    f.static(L(P.X(3), P.Y(0), P.X(3), P.Y(1), FI, 1, '3 3'))
    pts = [(0, 0, 0)]
    b0 = P(ws[0], fn(ws[0]))
    t = .8
    for k in range(len(ws) - 1):
        w, w2 = ws[k], ws[k + 1]
        m = d(w)
        a, b = P(w - .7, fn(w) - .7 * m), P(w + .7, fn(w) + .7 * m)
        f.show(L(a[0], a[1], b[0], b[1], VI, 1.6), t, hide=t + 1.0, d=.2)
        f.show(T(440, 60, 'step %d' % (k + 1), MU, 'start', 'sv-s') +
               T(440, 84, 'slope = %.2f' % m, VI, 'start', mono=True, bold=True) +
               T(440, 106, 'w = %.2f − 0.3 × %.2f = %.2f' % (w, m, w2), TX, 'start', mono=True), t, hide=t + 1.0 if k < len(ws) - 2 else None, d=.2)
        f.show(dot(*P(w, fn(w)), VI, 2.6), t + .5)
        q = P(w2, fn(w2))
        pts.append((t + .4, q[0] - b0[0], q[1] - b0[1]))
        t += 1.1
    f.path(ball(*b0, VI, 8), pts, .3, d=.6)
    f.show(S(440, 150, 'steps shrink as the slope flattens', MU), t)
    f.show(S(440, 172, 'w → 3, the bottom of the loss', FI, 'start', True), t + .3)
    return finish(f, 300)

# ---------- 3.2 Learning rate ----------
def fig_lr():
    fn = lambda w: (w - 3) ** 2 + 1
    d = lambda w: 2 * (w - 3)
    f = Anim('ca6-', 720, 0, 'Three small copies of the same loss curve, each with a ball starting at w = 0.5. Learning rate 0.05: tiny '
             'steps, still far from the bottom after six. 0.4: reaches the bottom. 0.95: overshoots and bounces from side '
             'to side.', 'LEARNING RATE · TOO SMALL, RIGHT, TOO LARGE')
    cases = [(.05, 'η = 0.05 · too slow', VI), (.4, 'η = 0.4 · converges', FI), (.95, 'η = 0.95 · bounces', RO)]
    for k, (eta, lab, c) in enumerate(cases):
        P = Plane(20 + k * 236, 214, 34, 18)
        f.static(L(P.X(0), P.Y(0), P.X(6), P.Y(0), MU, 1) + poly(curve(P, fn, .2, 5.8), BR, 2))
        ws = [.5]
        for _ in range(6):
            ws.append(ws[-1] - eta * d(ws[-1]))
        b0 = P(ws[0], fn(ws[0]))
        pts = [(0, 0, 0)]
        for i, w in enumerate(ws[1:]):
            q = P(w, fn(w))
            f.show(dot(*P(ws[i], fn(ws[i])), c, 2.6), .6 + i * .7)
            pts.append((.6 + i * .7, q[0] - b0[0], q[1] - b0[1]))
        f.path(ball(*b0, c, 7), pts, .3, d=.5)
        f.show(S(P.X(3), 240, lab, c, 'middle', True), 5.0)
        f.show(T(P.X(3), 260, 'after 6 steps w = %.2f' % ws[-1], MU, mono=True), 5.3)
    return finish(f, 276)

# ---------- 4. Convex ----------
def fig_convex():
    f1 = lambda w: .35 * (w - 3) ** 2 + .5
    f2 = lambda w: .08 * (w - 1) * (w - 2.2) * (w - 4) * (w - 5.4) + 1.6
    f = Anim('ca7-', 720, 0, 'Left, a convex bowl: two balls started from opposite sides both roll to the single bottom. Right, a '
             'curve with two dips: a ball started on the left settles in the shallow local dip, a ball started on the right '
             'reaches the deeper global minimum.', 'CONVEX: ONE BOTTOM · NON-CONVEX: THE START DECIDES')
    for k, (fn, lab, x0) in enumerate([(f1, 'convex', 30), (f2, 'non-convex', 380)]):
        P = Plane(x0, 196, 52, 30)
        f.static(L(P.X(0), P.Y(0), P.X(6), P.Y(0), MU, 1) + poly(curve(P, fn, .2 if k == 0 else .75, 5.8 if k == 0 else 5.65), BR, 2.4))
        f.static(S(x0, 40, lab, MU, 'start', True))
        h = 1e-4
        for j, (s, c) in enumerate([(.5, VI), (5.5, VI)] if k == 0 else [(.85, VI), (5.5, VI)]):
            ws = [s]
            for _ in range(80):
                g = (fn(ws[-1] + h) - fn(ws[-1] - h)) / (2 * h)
                ws.append(ws[-1] - .08 / (0.35 if k == 0 else .5) * g * .5)
            keep = ws[::8]
            b0 = P(s, fn(s))
            pts = [(0, 0, 0)] + [(.6 + i * .45, P(w, fn(w))[0] - b0[0], P(w, fn(w))[1] - b0[1]) for i, w in enumerate(keep[1:])]
            f.path(ball(*b0, c, 7), pts, .3 + j * .2, d=.4)
            end = ws[-1]
            if k == 1:
                glob = end > 4
                e = P(end, fn(end))
                f.show(S(e[0], e[1] + 26, 'global min' if glob else 'local min', FI if glob else RO, 'middle', True), 5.6)
                f.show(dot(e[0], e[1] + 0, FI if glob else RO, 4), 5.6)
        if k == 0:
            e = P(3, f1(3))
            f.show(S(e[0], e[1] + 30, 'same bottom', FI, 'middle', True) + dot(*e, FI, 4), 5.6)
    f.show(S(30, 250, 'linear & logistic regression, SVM: convex — any start ends at the same answer', MU), 6.2)
    f.show(S(30, 270, 'neural networks: non-convex — but in high dimensions most stops are escapable saddles', MU), 6.5)
    return finish(f, 290)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Math foundations</p>
  <h1><em>Calculus</em></h1>
  <p class="lede">All of training is walking downhill. Three things to remember:</p>
  <ul class="ledelist">
    <li>a derivative is <b>a slope</b>; the gradient collects every slope into <b>one arrow pointing uphill</b></li>
    <li>the chain rule <b>multiplies slopes backward</b> through a pipeline — that is backpropagation</li>
    <li>gradient descent <b>steps against the gradient</b>; on a convex loss it always finds the one bottom</li>
  </ul>
</header>

<section id="calc-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Derivatives</h2></div>
  <p class="key">A derivative answers one question: <em>nudge the input a little — how much does the output move?</em></p>

  <div class="subsec" id="calc-s1-1">
    <h3 class="ssh"><b>1.1</b>Derivative = slope</h3>
    <p class="skey">Join two points on the curve, slide them together, and the line's slope becomes the derivative.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>f</var> ′(<var>x</var>)</span></span>
      <span class="op">=</span>
      <span class="t b"><span><b class="fn">lim</b><sub><var>h</var>→0</sub> <span class="frac"><i><var>f</var>(<var>x</var> + <var>h</var>) − <var>f</var>(<var>x</var>)</i><i><var>h</var></i></span></span><em>rise over run, with the run shrinking to zero</em></span>
    </div>
  </div>
{ca1}
    <ul class="why">
      <li>Positive slope: increasing the input raises the output. Zero slope: a flat spot — a bottom, a top or a saddle.</li>
      <li>Nobody derives these by hand in ML: autograd in PyTorch and JAX computes them.</li>
    </ul>
  </div>

  <div class="subsec" id="calc-s1-2">
    <h3 class="ssh"><b>1.2</b>Gradient</h3>
    <p class="skey">With many parameters, take one slope per parameter; together they form an arrow that points uphill.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span>∇<var>L</var></span></span>
      <span class="op">=</span>
      <span class="t b"><span>( <span class="frac"><i>∂<var>L</var></i><i>∂<var>w</var><sub>1</sub></i></span> , … , <span class="frac"><i>∂<var>L</var></i><i>∂<var>w</var><sub><var>n</var></sub></i></span> )</span><em>one partial slope per parameter</em></span>
    </div>
  </div>
{ca2}
    <ul class="why">
      <li>A partial slope <span class="mth">∂<var>L</var>/∂<var>w</var><sub>1</sub></span> moves one parameter and holds the rest still.</li>
      <li>The gradient's length carries information: long on a steep wall, near zero at the bottom.</li>
    </ul>
  </div>
</section>

<section id="calc-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Chain rule</h2></div>
  <p class="key">A model is <em>a pipeline of functions</em>, so its slope is <em>the product of each stage's slope</em>.</p>

  <div class="subsec" id="calc-s2-1">
    <h3 class="ssh"><b>2.1</b>Pipeline</h3>
    <p class="skey">Values flow forward through the boxes; slopes flow backward and multiply.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><span class="frac"><i><var>dy</var></i><i><var>dx</var></i></span></span></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i><var>dy</var></i><i><var>du</var></i></span></span><em>slope of the outer box</em></span>
      <span class="op">·</span>
      <span class="t b"><span><span class="frac"><i><var>du</var></i><i><var>dx</var></i></span></span><em>slope of the inner box</em></span>
    </div>
  </div>
{ca3}
    <ul class="why">
      <li><a href="../../../08-deep-learning/02-neural-network/backpropagation/index.html">Backpropagation</a> is this rule applied to a computation graph, one box per operation.</li>
      <li>Each backward step reuses the value saved in the forward pass — that is why training stores activations.</li>
    </ul>
  </div>

  <div class="subsec" id="calc-s2-2">
    <h3 class="ssh"><b>2.2</b>Vanishing &amp; exploding gradients</h3>
    <p class="skey">Multiply many slopes and the product drifts to zero or to infinity.</p>
{ca4}
    <ul class="why">
      <li>Vanishing: early layers stop learning. Exploding: the loss jumps to <code>NaN</code>.</li>
      <li>Gradient clipping caps the exploding case; the fixes for both live in the deep-learning shelf.</li>
    </ul>
  </div>
</section>

<section id="calc-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Gradient descent</h2></div>
  <p class="key">Repeat one move: <em>compute the gradient, step against it</em>.</p>

  <div class="subsec" id="calc-s3-1">
    <h3 class="ssh"><b>3.1</b>Update rule</h3>
    <p class="skey">The ball moves against the slope, by the learning rate times the slope.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>w</var></span><em>new weight</em></span>
      <span class="op">←</span>
      <span class="t"><span><var>w</var></span><em>old weight</em></span>
      <span class="op">−</span>
      <span class="t b"><span><var>η</var></span><em>learning rate</em></span>
      <span class="op">·</span>
      <span class="t b"><span>∇<var>L</var>(<var>w</var>)</span><em>gradient: points uphill</em></span>
    </div>
  </div>
{ca5}
    <ul class="why">
      <li>Mini-batch SGD computes the gradient on a small batch: a noisier direction but many more steps per second.</li>
      <li><a href="../../06-tree-models/gradient-boosting/index.html">Gradient boosting</a> borrows this idea: each new tree fits the remaining gradient.</li>
    </ul>
  </div>

  <div class="subsec" id="calc-s3-2">
    <h3 class="ssh"><b>3.2</b>Learning rate</h3>
    <p class="skey">The same curve and the same start — only <span class="mth"><var>η</var></span> changes.</p>
{ca6}
    <ul class="why">
      <li>Too large: the loss bounces or diverges. Too small: training crawls.</li>
      <li>In practice <span class="mth"><var>η</var></span> is tuned first and often decays during training; Adam adapts it per parameter.</li>
    </ul>
  </div>
</section>

<section id="calc-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Convex functions</h2></div>
  <p class="key">A convex function has <em>exactly one bottom</em> — every downhill walk ends there.</p>
{ca7}
  <ul class="why">
    <li>Convex: every stopping point is the global optimum. Non-convex: the result depends on the start.</li>
    <li>This is the real boundary between classical models and deep learning.</li>
  </ul>
</section>

'''

def build():
    figs = dict(ca1=fig_slope(), ca2=fig_gradient(), ca3=fig_chain(), ca4=fig_vanish(), ca5=fig_gd(), ca6=fig_lr(), ca7=fig_convex())
    return re.sub(r'\{(ca\d+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'Slopes, gradients, the chain rule and gradient descent — how a model learns by walking downhill.')
