# -*- coding: utf-8 -*-
"""Ridge/Lasso 03 overview figure: the classic three-panel picture (L1 diamond, L2 circle, L1+L2 rounded
diamond) with filled error contours around the unpenalized optimum, growing until they touch the region.
Every touching point is computed. Run: python3 ridge_lasso_regions.py -> puts the figure under section 03's .key."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from linear_algebra import Anim, T, R, L, MU, TX, FA, BR, VI, FI, RO, RULE_HI, BG, tn, M, S, dot, poly, finish
PAGE = os.path.join(HERE, '../../../content/07-machine-learning/05-classical-ml/ridge-lasso-elasticnet/index.html')

# error  E(w) = (w - c)^T Q (w - c),  Q rotated ellipse (long axis tilted ~40 deg, like the reference)
C = (1.2, 2.0)
ANG = math.radians(30)
A_LONG, A_SHORT = 1.0, 2.5           # curvature along / across the long axis
ca, sa = math.cos(ANG), math.sin(ANG)
def err(w1, w2):
    d1, d2 = w1 - C[0], w2 - C[1]
    u = d1 * ca + d2 * sa
    v = -d1 * sa + d2 * ca
    return A_LONG * u * u + A_SHORT * v * v

def norm(kind, w1, w2, rho=.5):
    if kind == 'l1': return abs(w1) + abs(w2)
    if kind == 'l2': return math.sqrt(w1 * w1 + w2 * w2)
    return rho * (abs(w1) + abs(w2)) + (1 - rho) * math.sqrt(w1 * w1 + w2 * w2)

def boundary(kind, t, n=720):
    """Points on {norm = t}, by bisection along each ray."""
    pts = []
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        dx, dy = math.cos(a), math.sin(a)
        lo, hi = 0, 3 * t
        for _ in range(40):
            m = (lo + hi) / 2
            if norm(kind, m * dx, m * dy) < t: lo = m
            else: hi = m
        pts.append((lo * dx, lo * dy))
    return pts

def touch(kind, t):
    b = boundary(kind, t, 2880)
    return min(b, key=lambda p: err(*p))

def ellipse_pts(k, n=120):
    """Level set err = k around C."""
    out = []
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        u, v = math.sqrt(k / A_LONG) * math.cos(a), math.sqrt(k / A_SHORT) * math.sin(a)
        out.append((C[0] + u * ca - v * sa, C[1] + u * sa + v * ca))
    return out

def fig():
    T_ = 1.0
    panels = [('l1', 'L1 · Lasso', 'hits the corner → θ₁ = 0', 'sparse'),
              ('l2', 'L2 · Ridge', 'round edge → both shrink', 'shrink'),
              ('en', 'L1 + L2 · Elastic Net', 'rounded corner → near the axis', 'both')]
    f = Anim('rlr-', 720, 0, 'Three panels with axes theta 1 and theta 2. In each, the unpenalized optimum sits up and to the '
             'right with filled elliptical error contours around it. The allowed region is a diamond for L1, a circle for L2 '
             'and a diamond with rounded sides for L1 plus L2. The contours grow outward until the first one touches the region: '
             'for L1 at the top corner, where theta 1 is exactly 0; for L2 on the curved edge, where both are non-zero; '
             'for Elastic Net near the corner.', 'THE CONTOUR GROWS UNTIL IT FIRST TOUCHES THE ALLOWED REGION')
    W, OX0, OY, SC = 236, 74, 196, 46
    for k, (kind, name, note, tag) in enumerate(panels):
        ox = OX0 + k * W
        X = lambda a: ox + a * SC
        Y = lambda b: OY - b * SC
        P = lambda p: (X(p[0]), Y(p[1]))
        t0 = .4 + k * 2.4
        # axes
        f.static(L(X(-1.45), Y(0), X(3.1), Y(0), MU, 1.1) + L(X(0), Y(-1.25), X(0), Y(3.6), MU, 1.1) +
                 M(X(3.1) + 4, Y(0) + 15, 'θ₁', MU, 'start') + M(X(0) - 6, Y(3.6) + 4, 'θ₂', MU, 'end'))
        # region
        reg = boundary(kind, T_, 360)
        f.show(poly([P(p) for p in reg], FI, 1.8, fill=tn(FI, '.22')), t0)
        tp = touch(kind, T_)
        k_end = err(*tp)
        # filled contours, outer (light) to inner (dark), all inside k_end so they never cross the region
        levels = [k_end * s for s in (1.0, .62, .36, .18, .07)]
        alphas = ['.10', '.16', '.24', '.34', '.48']
        for j, (lv, al) in enumerate(zip(levels, alphas)):
            pts = [P(p) for p in ellipse_pts(lv)]
            last = j == 0
            f.show(poly(pts, VI if last else 'var(--rule-hi)', 1.6 if last else .8, fill=tn(VI, al)),
                   t0 + .5 + (len(levels) - 1 - j) * .3)
        f.show(dot(*P(C), 'var(--on-fill)', 3.5) + M(X(C[0]) + 52, Y(C[1]) - 36, 'θ̂', VI, 'start') + L(X(C[0]) + 4, Y(C[1]) - 4, X(C[0]) + 48, Y(C[1]) - 32, VI, 1, '2 2'), t0 + .4)
        # touching point
        tx, ty = P(tp)
        f.show('<circle cx="%.1f" cy="%.1f" r="8" fill="none" stroke="%s" stroke-width="2"/>' % (tx, ty, FI) +
               dot(tx, ty, FI, 4.5), t0 + 2.0)
        f.show(T(ox + .8 * SC, 272, name, TX, cls='sv-s', bold=True), t0)
        f.show(T(ox + .8 * SC, 290, note, FI, cls='sv-d'), t0 + 2.1)
    # sanity: L1 touch is on the theta2 axis, L2 touch is off both axes
    t1, t2 = touch('l1', T_), touch('l2', T_)
    assert abs(t1[0]) < 1e-2 and abs(t1[1] - 1) < 1e-2, t1
    assert t2[0] > .25 and t2[1] > .25, t2
    assert touch('en', T_)[0] < t2[0] - .08
    return finish(f, 308)

if __name__ == '__main__':
    h = open(PAGE).read()
    svg = fig()
    if 'rlr-a1' in h:
        h = re.sub(r'<figure class="gist">\s*<svg[^>]*><style>@keyframes rlr-a1.*?</figure>', lambda m: svg, h, count=1, flags=re.S)
    else:
        m = re.search(r'(<div class="sh"><b>03</b><h2>[^<]*</h2></div>\s*<p class="key">.*?</p>)', h, re.S)
        if not m: sys.exit('section 03 not found')
        h = h[:m.end()] + '\n' + svg + '\n' + h[m.end():]
    open(PAGE, 'w').write(h)
    print('ok', touch('l1', 1.0), touch('l2', 1.0), touch('en', 1.0))
