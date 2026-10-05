# -*- coding: utf-8 -*-
"""Figures + page body for content/07-machine-learning/05-classical-ml/svm.
Run: python3 svm.py -> rewrites the lesson body between <header class="hero"> and the replay script.
Every number is computed here by a small SMO solver (svm_smo.py)."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from linear_algebra import Anim, T, R, L, MU, TX, FA, BR, VI, FI, RO, GH, RULE, BG, tn, M, S, chip, dot, poly, Plane, finish, vec
from tablefig import Table, RULE_HI, arrow
from svm_smo import smo, wvec, rbf

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/05-classical-ml/svm/index.html')

POS = [(5, 6), (6, 5), (6.5, 7.5), (7.5, 6), (7.5, 4), (8.5, 7.5), (5, 8.5), (9, 5.5), (6.5, 9)]
NEG = [(1, 2), (2, 1), (2.5, 3), (3.5, 1.5), (1.5, 4.5), (3, 5), (4, 3.5), (1, 0.5), (0.5, 3)]
X0 = POS + NEG
Y0 = [1] * 9 + [-1] * 9
A0, B0 = smo(X0, Y0, 1e6)
W0 = wvec(X0, Y0, A0)
SV0 = [i for i in range(18) if A0[i] > 1e-6]
assert [round(v, 3) for v in W0] == [0.75, 0.5] and round(B0, 3) == -5.75 and [X0[i] for i in SV0] == [(5, 6), (3, 5), (4, 3.5)]
NOISE = (4.5, 4.8)
X1, Y1 = X0 + [NOISE], Y0 + [-1]

def frac(cx, cy, num, den, c=TX, w=None):
    w = w or max(len(re.sub(r'[{}]', '', num)), len(re.sub(r'[{}]', '', den))) * 8 + 12
    return M(cx, cy - 7, num, c) + L(cx - w / 2, cy, cx + w / 2, cy, c, 1.1) + M(cx, cy + 17, den, c)

# ---------- plane helpers ----------
def clip(poly_, a, b, c):
    """keep part of polygon with a*x + b*y + c >= 0"""
    out = []
    for i in range(len(poly_)):
        p, q = poly_[i], poly_[(i + 1) % len(poly_)]
        fp, fq = a * p[0] + b * p[1] + c, a * q[0] + b * q[1] + c
        if fp >= 0: out.append(p)
        if fp * fq < 0:
            t = fp / (fp - fq); out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out

BOX = [(0, 0), (10, 0), (10, 10), (0, 10)]

def seg(P, w, b, lvl=0, box=BOX):
    """segment of w.x + b = lvl inside the box"""
    pts = clip(clip(box, w[0], w[1], b - lvl), -w[0], -w[1], -(b - lvl) + 1e-9)
    pts = sorted(set((round(x, 6), round(y, 6)) for x, y in pts))
    return P(*pts[0]), P(*pts[-1])

def line(P, w, b, lvl=0, c=FI, sw=2.4, dash=None, box=BOX):
    a, e = seg(P, w, b, lvl, box)
    return L(a[0], a[1], e[0], e[1], c, sw, dash)

def band(P, w, b, c=FI, al='.12', box=BOX):
    pts = clip(clip(box, w[0], w[1], b + 1), -w[0], -w[1], -b + 1)
    return poly([P(*p) for p in pts] + [P(*pts[0])], 'none', 0, None, tn(c, al))

def frame(P, n=10, xl='{x}₁', yl='{x}₂'):
    x0, y0 = P(0, 0); x1, y1 = P(n, n)
    return (R(x0, y1, x1 - x0, y0 - y1, BG, RULE, 4) + M(x1 + 6, y0 + 5, xl, MU, 'start') + M(x0, y1 - 7, yl, MU))

def pt(P, p, cls, r=4.6):
    x, y = P(*p)
    if cls > 0: return dot(x, y, BR, r)
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="1.8"/>' % (x, y, r - .6, BG, BR)

def ring(P, p, c=VI, r=9):
    x, y = P(*p)
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="none" stroke="%s" stroke-width="1.8"/>' % (x, y, r, c)

def legend(x, y):
    return (dot(x, y, BR, 4.6) + S(x + 10, y + 4, 'class +1') +
            '<circle cx="%.1f" cy="%.1f" r="4" fill="%s" stroke="%s" stroke-width="1.8"/>' % (x + 80, y, BG, BR) + S(x + 90, y + 4, 'class −1'))

def width(w): return 2 / math.hypot(*w)

def minband(w, b, X=X0, Y=Y0):
    """for an arbitrary separating line: widest band it can carry = 2 * min distance"""
    return 2 * min(y * (w[0] * x[0] + w[1] * x[1] + b) for x, y in zip(X, Y)) / math.hypot(*w)

# ---------- 1. Mental model ----------
def fig_mental():
    f = Anim('svm1-', 720, 0, 'Eighteen points in two classes. Three separating lines are tried in turn, each with the widest '
             'empty band it can carry: 0.98, 1.34, then the SVM line with 2.22. The SVM line sits in the middle of the widest '
             'band; the three points touching the band edges are ringed: the support vectors.', 'MANY LINES SEPARATE · SVM KEEPS THE WIDEST EMPTY BAND')
    P = Plane(40, 320, 27)
    f.static(frame(P) + legend(330, 40))
    for p, y in zip(X0, Y0): f.static(pt(P, p, y))
    cands = [((1, 0.2), -5.2), ((2, 1), -13), (W0, B0)]
    wds = [minband(w, b) for w, b in cands]
    assert [round(v, 2) for v in wds] == [0.98, 1.34, 2.22]
    t = .6
    for k, (w, b) in enumerate(cands):
        last = k == 2
        s = math.hypot(*w); half = wds[k] / 2 * s  # band in F units
        wn = (w[0] * 1 / half, w[1] / half); bn = b / half
        hide = None if last else t + 1.6
        f.show(band(P, wn, bn, VI if not last else FI, '.13') + line(P, wn, bn, 1, VI if not last else FI, 1.2, '4 3') +
               line(P, wn, bn, -1, VI if not last else FI, 1.2, '4 3'), t + .3, hide)
        f.show(line(P, w, b, 0, VI if not last else FI, 2.4), t, hide)
        y = 96 + k * 46
        f.show(S(330, y, ['line A', 'line B', 'SVM line'][k], VI if not last else FI, bold=True) +
               R(400, y - 11, wds[k] / 2.22 * 220, 14, tn(VI if not last else FI, '.2'), VI if not last else FI, 3, 1.2) +
               T(400 + wds[k] / 2.22 * 220 + 8, y + 1, 'band %.2f' % wds[k], VI if not last else FI, 'start', 'sv-s'), t + .3)
        t += 2.0
    for i in SV0: f.show(ring(P, X0[i]), t)
    f.show(S(330, 250, '3 points touch the band edges:', VI, bold=True) + S(330, 270, 'the support vectors', VI), t + .2)
    f.show(S(330, 300, 'the line sits exactly in the middle of them', MU), t + .7)
    return finish(f, 340)

# ---------- 2. General formula ----------
def fig_geom():
    w, b = W0, B0
    nw = math.hypot(*w)
    assert round(nw, 3) == 0.901 and round(2 / nw, 2) == 2.22
    f = Anim('svm2-', 720, 0, 'The SVM line w·x + b = 0 with w = (0.75, 0.5) and b = −5.75. The band edges are where the score is '
             '+1 and −1. The arrow w points across the band. Its length is the square root of 0.75 squared plus 0.5 squared, '
             '0.901; the band width is 2 over that, 2.22.', 'THE BAND EDGES ARE SCORE = ±1 · WIDTH = 2 / ‖w‖')
    P = Plane(72, 320, 27)
    f.static(frame(P))
    for p, y in zip(X0, Y0): f.static(pt(P, p, y))
    def at(lvl, yy):
        x = (lvl - b - w[1] * yy) / w[0]
        return P(x, yy)
    p0 = at(0, .5); p1 = at(1, .5); p2 = at(-1, 9.3)
    f.show(line(P, w, b, 0, FI, 2.4) + M(p0[0] - 8, p0[1], '{F} = 0', FI, 'end'), .3)
    f.show(band(P, w, b, FI, '.12') + line(P, w, b, 1, BR, 1.3, '4 3') + line(P, w, b, -1, BR, 1.3, '4 3'), 1.2)
    f.show(M(p1[0] + 8, p1[1], '{F} = +1', BR, 'start') + M(p2[0] - 8, p2[1], '{F} = −1', BR, 'end'), 1.5)
    # perpendicular across the band through the middle point
    c0 = (4.2, 5.2)
    k = (0 - (w[0] * c0[0] + w[1] * c0[1] + b)) / nw ** 2
    m0 = (c0[0] + k * w[0], c0[1] + k * w[1])
    lo = (m0[0] - w[0] / nw ** 2, m0[1] - w[1] / nw ** 2); hi = (m0[0] + w[0] / nw ** 2, m0[1] + w[1] / nw ** 2)
    f.show(vec(*P(*m0), *P(m0[0] + w[0] * 2, m0[1] + w[1] * 2), VI, 2.4) + M(P.X(m0[0] + w[0] * 2) + 8, P.Y(m0[1] + w[1] * 2) - 4, '{w}', VI, 'start'), 2.4)
    f.show(L(*P(*lo), *P(*hi), RO, 2.6) + T(P.X(lo[0]) - 6, P.Y(lo[1]) + 14, 'width', RO, 'end', 'sv-s', bold=True), 5.6)
    X = 380
    f.show(M(X, 60, '{w} = (0.75, 0.5)', TX, 'start') + M(X + 150, 60, '{b} = −5.75', TX, 'start'), 3.2)
    f.show(M(X, 98, '‖{w}‖ = √(0.75² + 0.5²) = √0.8125 = 0.901', TX, 'start'), 4.0)
    f.show(M(X, 150, 'width =', TX, 'start') + frac(X + 92, 145, '2', '‖{w}‖', TX, 40) + M(X + 120, 150, '=', TX) +
           frac(X + 152, 145, '2', '0.901', TX, 44) + M(X + 182, 150, '=', TX), 4.8)
    f.show(R(X + 194, 133, 52, 28, FI, FI, 6) + M(X + 220, 152, '2.22', 'var(--on-fill)'), 5.6)
    f.show(S(X, 206, 'shorter arrow w → wider band', VI, bold=True), 6.4)
    f.show(S(X, 228, 'so “widest band” = “smallest ‖w‖²”, the L2 penalty', MU), 6.8)
    return finish(f, 340)

# ---------- 3. Worked hinge loss ----------
def fig_learn():
    Ac, Bc = smo(X1, Y1, 1)
    w = wvec(X1, Y1, Ac)
    assert [round(v, 2) for v in w] == [0.85, 0.85] and round(Bc, 2) == -8.35
    w, b = (0.85, 0.85), -8.35
    rows = [((6.5, 7.5), 1), ((5, 6), 1), ((3, 5), -1), ((4, 3.5), -1), (NOISE, -1)]
    f = Anim('svm3-', 720, 0, 'Nineteen points, one class −1 point sits among the class +1 side. With C = 1 the model is w = (0.85, 0.85), '
             'b = −8.35. Five points are scored one by one: score F, margin y·F, hinge max(0, 1 − y·F). Points past the band '
             'give hinge 0; the intruding point gives 0.55. Loss = 0.72 + 1 × 0.55 = 1.27.', 'SCORE EACH POINT · ONLY THOSE INSIDE THE BAND PAY')
    t = Table(0, 44, [('point', 82, '(x₁, x₂)'), ('y', 40, 'class'), ('F', 70, 'w·x + b'), ('y·F', 62, 'margin'), ('hinge', 112, 'max(0, 1 − y·F)')])
    f.show(t.head(), .1)
    for i, (p, y) in enumerate(rows):
        f.show(t.row(i, ['(%g, %g)' % p, '%+d' % y, '', '', '']), .2 + i * .1)
    P = Plane(440, 300, 24)
    f.static(frame(P))
    for p, y in zip(X1, Y1): f.static(pt(P, p, y, 4.2))
    f.static(band(P, w, b, FI, '.12') + line(P, w, b, 0, FI, 2.2) + line(P, w, b, 1, BR, 1.1, '4 3') + line(P, w, b, -1, BR, 1.1, '4 3'))
    tt = .9; tot = 0
    for i, (p, y) in enumerate(rows):
        F = w[0] * p[0] + w[1] * p[1] + b; m = y * F; h = max(0, 1 - m); tot += h
        f.show(t.outline(i, c=VI), tt, hide=tt + 1.5)
        f.show(ring(P, p, VI, 9), tt, hide=tt + 1.5)
        f.show(t.cell(i, 2, '%.2f' % F), tt + .4)
        f.show(t.cell(i, 3, '%.2f' % m), tt + .8)
        f.show(t.cell(i, 4, '%.2f' % h, None, RO if h > 0 else FA) if h else t.cell(i, 4, '0', None, FA), tt + 1.2)
        if h:
            f.show(ring(P, p, RO, 9), tt + 1.5)
        tt += 1.7
    assert round(tot, 2) == 0.55
    reg = (w[0] ** 2 + w[1] ** 2) / 2
    assert round(reg, 2) == 0.72
    y0 = t.bottom(5) + 34
    f.show(M(0, y0, '{L} =', TX, 'start') + frac(56, y0 - 5, '‖{w}‖²', '2', TX, 40) + M(80, y0, '+ {C} · Σ hinge', TX, 'start'), tt)
    f.show(M(0, y0 + 40, '= 0.72 + 1 × 0.55 =', TX, 'start'), tt + .8)
    f.show(R(150, y0 + 22, 50, 28, FI, FI, 6) + M(175, y0 + 41, '1.27', 'var(--on-fill)'), tt + 1.4)
    f.show(S(0, y0 + 76, 'every point past the band adds exactly 0', MU), tt + 1.9)
    return finish(f, y0 + 96)

# ---------- 4.1 Support vectors ----------
def fig_sv():
    sx, sy = [X0[i] for i in SV0], [Y0[i] for i in SV0]
    a, b = smo(sx, sy, 1e6); w = wvec(sx, sy, a)
    assert [round(v, 3) for v in w] == [0.75, 0.5] and round(b, 3) == -5.75
    f = Anim('svm4-', 720, 0, 'The SVM line with its band on 18 points. The 15 points that do not touch the band fade out. '
             'Training again on just the 3 support vectors gives the same w = (0.75, 0.5) and b = −5.75: the line does not move.',
             'DELETE EVERY POINT OFF THE BAND · THE LINE STAYS')
    P = Plane(40, 320, 27)
    f.static(frame(P))
    f.static(band(P, W0, B0, FI, '.12') + line(P, W0, B0, 1, BR, 1.2, '4 3') + line(P, W0, B0, -1, BR, 1.2, '4 3'))
    f.static(line(P, W0, B0, 0, FI, 2.4))
    for i, (p, y) in enumerate(zip(X0, Y0)):
        if i in SV0:
            f.static(pt(P, p, y))
        else:
            f.show(pt(P, p, y), 0, hide=1.2 + (i % 9) * .08)
            x, yy = P(*p)
            f.show('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (x, yy, GH), 1.4 + (i % 9) * .08)
    for i in SV0: f.show(ring(P, X0[i]), .5)
    X = 350
    f.show(S(X, 70, '18 points', MU, bold=True), .3)
    f.show(S(X, 100, '− 15 points off the band', GH, bold=True), 1.3)
    f.show(S(X, 130, '= 3 support vectors', VI, bold=True), 2.4)
    f.show(S(X, 176, 'train again on those 3:', MU), 3.2)
    f.show(M(X, 206, '{w} = (0.75, 0.5)', FI, 'start') + M(X + 150, 206, '{b} = −5.75', FI, 'start'), 3.8)
    f.show(S(X, 236, 'identical — the line does not move', FI, bold=True), 4.4)
    f.show(S(X, 276, 'prediction needs only the support vectors', MU), 5.0)
    return finish(f, 340)

# ---------- 4.2 C ----------
def fig_c():
    f = Anim('svm5-', 720, 0, 'The same 19 points with one intruding class −1 point. Left, C = 100: intrusion is expensive, so the band '
             'shrinks to 1.20 to keep the point out, with 3 support vectors. Right, C = 0.1: intrusion is cheap, the band widens to '
             '3.45 and lets the point in, with 7 support vectors.', 'C = PRICE OF ONE UNIT OF INTRUSION')
    res = []
    for k, C in enumerate((100, 0.1)):
        a, b = smo(X1, Y1, C); w = wvec(X1, Y1, a)
        res.append((round(width(w), 2), sum(v > 1e-6 for v in a)))
        P = Plane(30 + k * 360, 330, 25)
        t0 = .4 + k * 2.6
        f.static(frame(P))
        for p, y in zip(X1, Y1): f.static(pt(P, p, y, 4.2))
        f.show(M(P.X(5), 32, '{C} = %g' % C, VI if k == 0 else FI) + S(P.X(5), 50, ['intrusion expensive', 'intrusion cheap'][k], MU, 'middle'), t0)
        f.show(band(P, w, b, FI, '.13') + line(P, w, b, 1, BR, 1.1, '4 3') + line(P, w, b, -1, BR, 1.1, '4 3') + line(P, w, b, 0, FI, 2.3), t0 + .5)
        for i in range(19):
            if a[i] > 1e-6: f.show(ring(P, X1[i], VI, 8), t0 + 1.1)
        f.show(ring(P, NOISE, RO, 11), t0 + 1.5)
        f.show(S(P.X(5), 358, 'band %.2f · %d support vectors' % res[-1], VI if k == 0 else FI, 'middle', True), t0 + 1.7)
    assert res == [(1.2, 3), (3.45, 7)]
    return finish(f, 372)

# ---------- 4.3 Kernel trick ----------
def fig_kernel():
    inner = [(1.1 * math.cos(i * math.pi / 4 + .3), 1.1 * math.sin(i * math.pi / 4 + .3)) for i in range(8)]
    outer = [(3 * math.cos(i * math.pi / 6), 3 * math.sin(i * math.pi / 6)) for i in range(12)]
    f = Anim('svm6-', 720, 0, 'Left, an inner ring of class +1 inside an outer ring of class −1: no straight line separates them. '
             'Each point gets a third coordinate z = x₁² + x₂²: 1.21 for the inner ring, 9 for the outer. Plotted as x₁ against z, '
             'a flat line z = 5 separates them. Back in the plane that line is the circle of radius √5.', 'NO LINE IN 2-D · ADD z = x₁² + x₂² · ONE LINE IN 3-D')
    P = Plane(170, 190, 36)
    f.static(R(P.X(-4), P.Y(4), 288, 288, BG, RULE, 4) + L(P.X(-4), P.Y(0), P.X(4), P.Y(0), RULE) + L(P.X(0), P.Y(-4), P.X(0), P.Y(4), RULE) +
             M(P.X(4) + 6, P.Y(0) + 5, '{x}₁', MU, 'start') + M(P.X(0), P.Y(4) - 7, '{x}₂', MU))
    for p in inner: f.static(pt(P, p, 1))
    for p in outer: f.static(pt(P, p, -1))
    f.show(L(P.X(-4), P.Y(-1.5), P.X(4), P.Y(2.5), RO, 2, '5 4') + S(P.X(0), P.Y(-4) + 20, 'any straight line fails', RO, 'middle', True), .4, hide=2.2)
    Q = Plane(470, 330, 30, 30)   # x1 from -3.5..3.5 , z 0..10
    f.show(R(Q.X(-4), Q.Y(10), 240, 300, BG, RULE, 4) + M(Q.X(4) + 6, Q.Y(0) + 5, '{x}₁', MU, 'start') +
           M(Q.X(-4) - 6, Q.Y(10) + 12, '{z}', MU, 'end') + T(Q.X(-4) - 6, Q.Y(9) + 4, '9', FA, 'end') + T(Q.X(-4) - 6, Q.Y(1.21) + 4, '1.21', FA, 'end'), 2.4)
    f.show(M(Q.X(0), 22, '{z} = {x}₁² + {x}₂²', VI), 2.6)
    for k, (p, c) in enumerate([(p, 1) for p in inner] + [(p, -1) for p in outer]):
        z = p[0] ** 2 + p[1] ** 2
        tx, ty = Q(p[0], z); sx, sy = P(*p)
        f.path(pt(Q, (p[0], z), c), [(0, sx - tx, sy - ty), (3.2 + k * .05, 0, 0)], 3.0 + k * .05, d=.8)
    assert round(1.1 ** 2, 2) == 1.21
    f.show(L(Q.X(-4), Q.Y(5), Q.X(4), Q.Y(5), FI, 2.4) + T(Q.X(4) - 4, Q.Y(5) - 7, 'z = 5', FI, 'end', 'sv-s', bold=True), 5.0)
    r = math.sqrt(5) * P.sx
    f.show('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="2.4"/>' % (P.ox, P.oy, r, FI) +
           S(P.X(0), P.Y(-4) + 20, 'back in 2-D: a circle, radius √5', FI, 'middle', True), 5.8)
    return finish(f, 368)

# ---------- 4.4 gamma ----------
def fig_gamma():
    xs = [1, 2, 3, 4.5, 5.5, 6.5, 8, 9]; ys = [-1, -1, 1, 1, 1, -1, -1, -1]
    X = [(x, 0) for x in xs]
    f = Anim('svm7-', 720, 0, 'Eight points on one axis, three class +1 points in the middle. RBF kernel score F along the axis. '
             'γ = 0.1: one smooth hill covering the middle, the test point at 3.75 scores +2.03, correct. γ = 5: a narrow spike '
             'on each point, the test point between them scores −0.10, wrong.', 'γ = HOW FAR ONE POINT REACHES')
    for k, (g, col) in enumerate(((0.1, FI), (5, RO))):
        a, b = smo(X, ys, 10, rbf(g)); K = rbf(g)
        F = lambda t: sum(a[j] * ys[j] * K(X[j], (t, 0)) for j in range(8)) + b
        P = Plane(40 + k * 350, 210, 30, 34)
        t0 = .4 + k * 3
        f.static(L(P.X(0), P.Y(0), P.X(10), P.Y(0), MU, 1.1) + L(P.X(0), P.Y(-2.4), P.X(0), P.Y(2.6), RULE) +
                 M(P.X(10) + 4, P.Y(0) + 5, '{x}', MU, 'start') + M(P.X(0), P.Y(2.6) - 6, '{F}', MU) +
                 T(P.X(0) - 5, P.Y(0) + 4, '0', FA, 'end'))
        for x, y in zip(xs, ys): f.static(pt(P, (x, 0), y))
        f.show(M(P.X(5), 40, 'γ = %g' % g, col) + S(P.X(5), 58, ['wide reach: smooth', 'short reach: one spike per point'][k], MU, 'middle'), t0)
        pts = [P(i / 20, max(-2.4, F(i / 20))) for i in range(201)]
        for i in range(0, 200, 25):
            f.show(poly(pts[i:i + 26], col, 2.4), t0 + .3 + i / 200 * 1.2, d=.12)
        v = F(3.75)
        good = v > 0
        assert round(v, 2) == (2.03 if k == 0 else -0.10)
        x0, y0 = P(3.75, 0)
        f.show(L(x0, y0 + 26, x0, P.Y(max(-2.4, v)), VI, 1.2, '3 3') + '<rect x="%.1f" y="%.1f" width="10" height="10" fill="%s" transform="rotate(45 %.1f %.1f)"/>' % (x0 - 5, y0 + 21, VI, x0, y0 + 26), t0 + 1.8)
        f.show(S(x0, y0 + 56, 'test x = 3.75 → F = %+.2f' % v, VI, 'middle', True), t0 + 2.1)
        f.show(S(x0, y0 + 76, ['class +1, correct', 'class −1, wrong'][k], FI if good else RO, 'middle', True), t0 + 2.4)
    return finish(f, 300)

# ---------- 5.1 Scaling ----------
def fig_scale():
    a, b = (5, 6), (3, 5)
    f = Anim('svm8-', 720, 0, 'Distance between two points, split into the share from each feature. With both features on the same '
             'scale, x₁ gives 4 and x₂ gives 1. Measure x₁ in units ten times smaller and x₁ gives 400 while x₂ still gives 1: '
             'the margin is measured almost only along x₁.', 'THE MARGIN IS A DISTANCE · THE LARGEST UNIT WINS')
    f.static(M(0, 44, '‖{a} − {b}‖² = (Δ{x}₁)² + (Δ{x}₂)²', TX, 'start'))
    rows = [('same scale', 1, VI), ('x₁ × 10', 10, RO)]
    for k, (lab, s, col) in enumerate(rows):
        y = 100 + k * 110
        d1, d2 = ((a[0] - b[0]) * s) ** 2, (a[1] - b[1]) ** 2
        tot = d1 + d2
        f.show(S(0, y, lab, col, bold=True) + M(0, y + 30, '%g + %g = %g' % (d1, d2, tot), TX, 'start'), .4 + k * 2.4)
        W = 470
        x0 = 220
        f.show(R(x0, y - 14, W, 26, 'none', RULE, 4), .6 + k * 2.4)
        f.show(R(x0, y - 14, W * d1 / tot, 26, tn(BR, '.55'), BR, 4) + T(x0 + W * d1 / tot / 2, y + 4, 'x₁  %.1f%%' % (100 * d1 / tot), 'var(--on-fill)', bold=True), 1.0 + k * 2.4)
        f.show(R(x0 + W * d1 / tot, y - 14, W * d2 / tot, 26, tn(VI, '.6'), VI, 4), 1.4 + k * 2.4)
        lx = x0 + W * d1 / tot + W * d2 / tot / 2
        f.show(L(lx, y + 14, lx, y + 32, VI, 1, '3 3') + T(lx, y + 46, 'x₂  %.1f%%' % (100 * d2 / tot), VI, 'middle', bold=True), 1.6 + k * 2.4)
    f.show(S(0, 330, 'fix: standardize every feature before SVM', FI, bold=True), 5.6)
    return finish(f, 346)

# ---------- 5.2 Large n ----------
def fig_n():
    f = Anim('svm9-', 720, 0, 'A kernel SVM compares every pair of points: an n by n kernel matrix. At 8 bytes per entry, 1,000 points '
             'need 8 MB, 10,000 need 800 MB, 100,000 need 80 GB. Each tenfold more data costs a hundredfold more memory.',
             'n POINTS → n × n PAIRS')
    sizes = [(1000, '8 MB'), (10000, '800 MB'), (100000, '80 GB')]
    for n, s in sizes:
        assert {1000: 8e6, 10000: 8e8, 100000: 8e10}[n] == n * n * 8
    base = 300
    for k, (n, s) in enumerate(sizes):
        side = [12, 48, 192][k]
        x = [30, 110, 260][k]
        t0 = .4 + k * 1.4
        f.show(R(x, base - side, side, side, tn(BR, '.18'), BR, 2, 1.3) +
               (''.join(L(x + i * side / 8, base - side, x + i * side / 8, base, tn(BR, '.4'), .6) + L(x, base - side + i * side / 8, x + side, base - side + i * side / 8, tn(BR, '.4'), .6) for i in range(1, 8)) if k else ''), t0)
        f.show(M(x + side / 2, base + 22, '{n} = %s' % format(n, ','), TX) + T(x + side / 2, base + 42, s, VI if k < 2 else RO, 'middle', 'sv-s', bold=True), t0 + .4)
    f.show(S(490, 120, '10× data → 100× memory', RO, bold=True), 4.6)
    f.show(S(490, 146, 'beyond ~100k rows: use a linear SVM', MU), 5.1)
    f.show(S(490, 166, 'or gradient boosting instead', MU), 5.3)
    f.static(T(250, 330, 'squares drawn ×4 per step for space; true growth is ×100 in area', FA, 'middle'))
    return finish(f, 344)

# ---------- 5.3 No probabilities ----------
def fig_prob():
    pts = [(-0.45, 'noisy point'), (1.0, 'on the band edge'), (3.12, 'deep inside')]
    sig = lambda z: 1 / (1 + math.exp(-z))
    f = Anim('svm10-', 720, 0, 'SVM outputs a score F, a signed distance, not a probability. Three scores −0.45, 1.00 and 3.12. '
             'A sigmoid fitted on held-out data (Platt scaling; here the plain sigmoid for illustration) turns them into 0.39, '
             '0.73 and 0.96.', 'A SCORE IS A DISTANCE · A SIGMOID TURNS IT INTO A PROBABILITY')
    P = Plane(330, 260, 52, 200)
    f.static(L(P.X(-5), P.Y(0), P.X(5), P.Y(0), MU, 1.1) + L(P.X(0), P.Y(0), P.X(0), P.Y(1.05), RULE) +
             M(P.X(5) + 6, P.Y(0) + 5, '{F}', MU, 'start') + T(P.X(0) - 6, P.Y(1) + 4, '1', FA, 'end') + T(P.X(0) - 6, P.Y(.5) + 4, '0.5', FA, 'end') +
             L(P.X(-5), P.Y(1), P.X(5), P.Y(1), RULE, 1, '2 4'))
    for x in range(-4, 5, 2): f.static(T(P.X(x), P.Y(0) + 16, '%d' % x, FA))
    for k, (v, lab) in enumerate(pts):
        f.show(dot(P.X(v), P.Y(0), VI, 5), .3 + k * .3)
    f.show(S(P.X(-5), 40, 'SVM gives only F (and its sign)', MU), .4)
    curve = [P(i / 10 - 5, sig(i / 10 - 5)) for i in range(101)]
    f.show(poly(curve, FI, 2.4) + M(P.X(-4.8), P.Y(.85), '{p} = σ({a}{F} + {b})', FI, 'start'), 1.6)
    for k, (v, lab) in enumerate(pts):
        t0 = 2.6 + k * 1.2
        px, py = P(v, sig(v))
        f.show(L(px, P.Y(0), px, py, VI, 1.2, '3 3') + L(px, py, P.X(5.2), py, VI, 1, '3 3') + dot(px, py, VI, 4.5), t0)
        f.show(T(P.X(5.3), py + 4, '%.2f' % sig(v), FI, 'start', 'sv-s', bold=True), t0 + .4)
    assert [round(sig(v), 2) for v, _ in pts] == [0.39, 0.73, 0.96]
    f.show(S(0, 300, 'fit a and b on held-out data (Platt scaling); scikit-learn: SVC(probability=True)', MU), 6.4)
    return finish(f, 316)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Classical models</p>
  <h1><em>SVM</em></h1>
  <p class="lede">Many lines separate two classes. A support vector machine keeps the one with the widest empty band around it.</p>
  <ul class="ledelist">
    <li>only the few points touching the band decide the line</li>
    <li>a wide band is the L2 penalty in disguise</li>
    <li>a kernel bends the line without computing new coordinates</li>
  </ul>
</header>

<section id="svm-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Of all lines that separate the classes, SVM keeps the one <em>farthest from both sides</em>. The empty band around it is the <em>margin</em>.</p>
{svm1}
  <ul class="why">
    <li>The points touching the band edges are the <b>support vectors</b>; they alone fix the line.</li>
    <li><a href="../logistic-regression/index.html">Logistic regression</a> on separable data has no unique best line; the widest-band rule picks exactly one.</li>
  </ul>
</section>

<section id="svm-s2" class="lesson">
  <div class="sh"><b>02</b><h2>General formula</h2></div>
  <p class="key">A linear score, a sign for the class, and a loss that trades <em>band width</em> against <em>points inside the band</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>F</var>(<var>x</var>)</span></span>
      <span class="op">=</span>
      <span class="t b"><span><var>w</var> · <var>x</var></span><em>weighted sum of features</em></span>
      <span class="op">+</span>
      <span class="t"><span><var>b</var></span><em>bias</em></span>
      <span class="op">,</span>
      <span class="t g"><span><var>ŷ</var> = <b class="fn">sign</b> <var>F</var>(<var>x</var>)</span><em>class +1 or −1</em></span>
    </div>
    <div class="line">
      <span class="t"><span><var>L</var></span></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i>‖<var>w</var>‖<sup>2</sup></i><i>2</i></span></span><em>wide band (L2)</em></span>
      <span class="op">+</span>
      <span class="t p"><span><var>C</var></span><em>price of intrusion</em></span>
      <span class="op">·</span>
      <span class="t r"><span>Σ<sub><var>i</var></sub> <b class="fn">max</b>(0, 1 − <var>y</var><sub><var>i</var></sub> <var>F</var>(<var>x</var><sub><var>i</var></sub>))</span><em>hinge: points not yet past the band</em></span>
    </div>
  </div>
{svm2}
  <ul class="why">
    <li>The band edges are where <span class="mth"><var>F</var> = ±1</span>, so the width is <span class="mth">2 / ‖<var>w</var>‖</span>: maximizing the band is minimizing <span class="mth">‖<var>w</var>‖²</span>, the same penalty as <a href="../ridge-lasso-elasticnet/index.html">Ridge</a>.</li>
    <li><span class="mth"><var>y</var> · <var>F</var>(<var>x</var>)</span> is a point's margin: 1 or more means it is past the band.</li>
  </ul>
</section>

<section id="svm-s3" class="lesson">
  <div class="sh"><b>03</b><h2>How it learns</h2></div>
  <p class="key">Score every point, take its margin, and charge <em>hinge</em> only to points that are not yet past the band.</p>
{svm3}
  <ul class="why">
    <li>Hinge is 0 from margin 1 onward, so most points cost nothing and drop out of the solution.</li>
    <li>The penalty grows linearly with intrusion, so one mislabelled point cannot dominate the loss.</li>
    <li>The solver (SMO in scikit-learn's <code>SVC</code>) finds the <span class="mth"><var>w</var>, <var>b</var></span> with the smallest <span class="mth"><var>L</var></span>.</li>
  </ul>
</section>

<section id="svm-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Key knobs</h2></div>
  <p class="key">Which points matter, how much intrusion is allowed, and how the line bends.</p>

  <div class="subsec" id="svm-s4-1">
    <h3 class="ssh"><b>4.1</b>Support vectors</h3>
    <p class="skey">Remove every point that does not touch the band and train again: <em>the line does not move</em>.</p>
{svm4}
    <ul class="why">
      <li>The model stores only the support vectors, so prediction is cheap.</li>
      <li>The flip side: a single noisy point near the boundary can move the whole line.</li>
    </ul>
  </div>

  <div class="subsec" id="svm-s4-2">
    <h3 class="ssh"><b>4.2</b>C — soft vs hard margin</h3>
    <p class="skey">Large <span class="mth"><var>C</var></span> forbids intrusion and narrows the band; small <span class="mth"><var>C</var></span> allows it and widens the band.</p>
{svm5}
    <ul class="why">
      <li><span class="mth"><var>C</var> → ∞</span> is the <b>hard margin</b>: no point may enter the band. Real data always uses a <b>soft margin</b>.</li>
      <li><span class="mth"><var>C</var></span> plays the role of <span class="mth">1/<var>λ</var></span> in Ridge: large <span class="mth"><var>C</var></span> overfits, small underfits.</li>
    </ul>
  </div>

  <div class="subsec" id="svm-s4-3">
    <h3 class="ssh"><b>4.3</b>Kernel trick</h3>
    <p class="skey">Data no line can split may split cleanly after <em>adding a dimension</em>; a kernel does this without ever computing it.</p>
    <div class="eq">
      <div class="line">
        <span class="t"><span><var>K</var>(<var>a</var>, <var>b</var>)</span><em>kernel</em></span>
        <span class="op">=</span>
        <span class="t b"><span><var>φ</var>(<var>a</var>) · <var>φ</var>(<var>b</var>)</span><em>dot product in the lifted space</em></span>
        <span class="op">=</span>
        <span class="t p"><span><b class="fn">exp</b>(−<var>γ</var> ‖<var>a</var> − <var>b</var>‖<sup>2</sup>)</span><em>RBF, the default</em></span>
      </div>
    </div>
{svm6}
    <ul class="why">
      <li>The solver only needs dot products between pairs of points, so a function <span class="mth"><var>K</var></span> can stand in for the lifted coordinates.</li>
      <li>Common kernels: <b>linear</b>, <b>polynomial</b> <span class="mth">(<var>a</var>·<var>b</var> + 1)<sup><var>d</var></sup></span>, and <b>RBF</b>, whose lifted space is infinite-dimensional.</li>
    </ul>
  </div>

  <div class="subsec" id="svm-s4-4">
    <h3 class="ssh"><b>4.4</b>Gamma</h3>
    <p class="skey"><span class="mth"><var>γ</var></span> sets how far one point's influence reaches in the RBF kernel: small is smooth, large is <em>one spike per point</em>.</p>
{svm7}
    <ul class="why">
      <li>Large <span class="mth"><var>γ</var></span> memorizes the training set and fails between points: overfitting.</li>
      <li>Tune <span class="mth"><var>C</var></span> and <span class="mth"><var>γ</var></span> together on a log grid with <a href="../../04-core-concepts/train-val-test-cv/index.html">cross-validation</a>.</li>
    </ul>
  </div>
</section>

<section id="svm-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Where it breaks</h2></div>
  <p class="key">Everything rests on distances between points and on comparing every pair of points.</p>

  <div class="subsec" id="svm-s5-1">
    <h3 class="ssh"><b>5.1</b>Unscaled features</h3>
    <p class="skey">The margin is a distance, so the feature with the <em>largest unit</em> takes over.</p>
{svm8}
    <ul class="why">
      <li>Always put a <code>StandardScaler</code> before <code>SVC</code> in the pipeline.</li>
    </ul>
  </div>

  <div class="subsec" id="svm-s5-2">
    <h3 class="ssh"><b>5.2</b>Large datasets</h3>
    <p class="skey">A kernel SVM compares every pair of points, so cost grows with <span class="mth"><var>n</var>²</span>.</p>
{svm9}
    <ul class="why">
      <li>SVM shines with few samples and many features (text, genes); medium tabular data usually goes to <a href="../../06-tree-models/gradient-boosting/index.html">gradient boosting</a>.</li>
    </ul>
  </div>

  <div class="subsec" id="svm-s5-3">
    <h3 class="ssh"><b>5.3</b>No probabilities</h3>
    <p class="skey">SVM returns a distance to the line, <em>not a probability</em>; a sigmoid fitted afterwards converts it.</p>
{svm10}
    <ul class="why">
      <li>When calibrated probabilities matter, prefer logistic regression or see <a href="../../09-evaluation/calibration/index.html">Calibration</a>.</li>
      <li>With a kernel there are no readable coefficients either.</li>
    </ul>
  </div>
</section>

'''

def build():
    figs = dict(svm1=fig_mental(), svm2=fig_geom(), svm3=fig_learn(), svm4=fig_sv(), svm5=fig_c(), svm6=fig_kernel(),
                svm7=fig_gamma(), svm8=fig_scale(), svm9=fig_n(), svm10=fig_prob())
    return re.sub(r'\{(svm\d+)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">')
    b = s.index('<script>\n/* Figures start')
    s = s[:a] + body + s[b:]
    s = re.sub(r'data-blurb="[^"]*"( data-reviewed="\d")?', 'data-blurb="%s" data-reviewed="2"' % blurb, s, count=1)
    # drop a duplicated page tail left by an earlier splice
    end = s.index('</html>') + len('</html>')
    s = s[:end] + '\n'
    open(page, 'w').write(s)

if __name__ == '__main__':
    splice(PAGE, build(), 'Separate two classes with the widest empty band: support vectors, hinge loss, C, the kernel trick and gamma.')
    print('ok')
