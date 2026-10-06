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

# ---------- 2.1 Decision function ----------
def fig_score():
    w, b = W0, B0
    rows = [((6.5, 7.5), 'a'), ((7.5, 4), 'b'), ((5, 6), 'c'), ((4, 3.5), 'd'), ((1, 2), 'e')]
    Fs = [w[0] * p[0] + w[1] * p[1] + b for p, _ in rows]
    assert [round(v, 2) for v in Fs] == [2.88, 1.88, 1.0, -1.0, -4.0], Fs
    f = Anim('svm11-', 720, 0, 'The SVM line w·x + b = 0 with w = (0.75, 0.5), b = −5.75. Five points get a score F one by one: '
             '2.88, 1.88, 1.00, −1.00, −4.00. Positive scores fall on the class +1 side, negative on the class −1 side; '
             'the farther from the line, the larger the score.', 'EVERY POINT GETS A SCORE · ITS SIGN PICKS THE SIDE')
    P = Plane(40, 320, 27)
    f.static(frame(P))
    for p, y in zip(X0, Y0): f.static(pt(P, p, y))
    f.static(line(P, w, b, 0, FI, 2.4))
    a1, a2 = seg(P, w, b)
    f.static(M(P.X(8.8), P.Y(1.6), '{F} > 0', FI) + M(P.X(1.6), P.Y(7.6), '{F} &lt; 0', FI))
    t = Table(360, 40, [('point', 70, '(x₁, x₂)'), ('F', 90, 'w·x + b'), ('sign F', 70, ''), ('ŷ', 70, 'class')])
    f.static(t.head())
    for i, (p, nm) in enumerate(rows):
        f.static(t.row(i, ['(%g, %g)' % p, '', '', '']))
    tt = .5
    for i, (p, nm) in enumerate(rows):
        F = Fs[i]
        f.show(t.outline(i, c=VI), tt, hide=tt + 1.3)
        f.show(ring(P, p, VI, 9), tt, hide=tt + 1.3)
        f.show(t.cell(i, 1, '%+.2f' % F), tt + .4)
        f.show(t.cell(i, 2, '+' if F > 0 else '−'), tt + .7)
        f.show(t.cell(i, 3, '+1' if F > 0 else '−1', None, FI), tt + 1.0)
        tt += 1.5
    y0 = t.bottom(5) + 34
    f.show(M(360, y0, '{ŷ} = sign {F}({x})', TX, 'start'), tt)
    f.show(S(360, y0 + 28, '|F| grows with distance from the line,', MU), tt + .5)
    f.show(S(360, y0 + 48, 'but it is a score, not a probability', VI, bold=True), tt + .9)
    return finish(f, 340)

# ---------- 3.1 Hard margin ----------
def fig_hard():
    bad = (6.2, 6.6)
    F = W0[0] * bad[0] + W0[1] * bad[1] + B0
    assert round(-F, 2) == -2.2
    f = Anim('svm12-', 720, 0, 'Hard margin demands y·F ≥ 1 for every point. On the 18 points the widest band is 2.22. A single class −1 '
             'point is added at (6.2, 6.6), deep on the class +1 side: its y·F is −2.20. No line keeps all 19 points on their own '
             'side — the best line still gets one point wrong — so the band disappears and hard margin has no solution.',
             'HARD MARGIN: EVERY POINT MUST BE PAST THE BAND')
    P = Plane(40, 320, 27)
    f.static(frame(P))
    for p, y in zip(X0, Y0): f.static(pt(P, p, y))
    f.show(band(P, W0, B0, FI, '.12') + line(P, W0, B0, 1, BR, 1.2, '4 3') + line(P, W0, B0, -1, BR, 1.2, '4 3') +
           line(P, W0, B0, 0, FI, 2.4), .3, hide=4.4)
    X = 360
    f.show(M(X, 60, '{y}ᵢ {F}({x}ᵢ) ≥ 1   for all {i}', TX, 'start'), .2)
    f.show(S(X, 92, '18 points: all satisfied · band 2.22', FI, bold=True), .9)
    f.show(pt(P, bad, -1), 2.0)
    f.show(ring(P, bad, RO, 11), 2.4)
    f.show(S(X, 134, '+ 1 noisy point of class −1', RO, bold=True), 2.2)
    f.show(M(X, 162, '{y} · {F} = −1 × 2.20 = −2.20 &lt; 1', RO, 'start'), 2.9)
    f.show(S(X, 204, 'no line puts all 19 on their own side', TX), 4.0)
    f.show(S(X, 226, '(best line: 1 point wrong)', MU), 4.4)
    f.show(S(X, 268, 'the band collapses · no solution', RO, bold=True), 5.0)
    f.show(S(X, 296, 'one bad label breaks hard margin', MU), 5.6)
    return finish(f, 340)

# ---------- 04 Kernel identity ----------
def fig_identity():
    a, c = (1, 2), (3, 1)
    phi = lambda v: (v[0] ** 2, math.sqrt(2) * v[0] * v[1], v[1] ** 2)
    pa, pc = phi(a), phi(c)
    d3 = sum(u * v for u, v in zip(pa, pc)); d2 = a[0] * c[0] + a[1] * c[1]
    assert round(d3, 6) == 25 and d2 ** 2 == 25
    f = Anim('svm13-', 720, 0, 'Two points a = (1, 2) and b = (3, 1). Route one lifts each into 3D with φ(x) = (x₁², √2·x₁x₂, x₂²): '
             'φ(a) = (1, 2.83, 4), φ(b) = (9, 4.24, 1), and their dot product 9 + 12 + 4 = 25. Route two stays in 2D: '
             'a·b = 3 + 2 = 5, squared is 25. Same number, without ever computing the 3D coordinates.',
             'TWO ROUTES TO THE SAME NUMBER')
    f.static(M(0, 46, '{a} = (1, 2)', TX, 'start') + M(110, 46, '{b} = (3, 1)', TX, 'start'))
    f.static(M(260, 46, 'φ({x}) = ({x}₁², √2·{x}₁{x}₂, {x}₂²)', MU, 'start'))
    Y1 = 96
    f.show(S(0, Y1, 'lift to 3D, then dot', VI, bold=True), .4)
    f.show(M(0, Y1 + 32, 'φ({a}) = (1, 2.83, 4)', TX, 'start'), .9)
    f.show(M(0, Y1 + 60, 'φ({b}) = (9, 4.24, 1)', TX, 'start'), 1.4)
    f.show(M(230, Y1 + 46, 'φ({a})·φ({b}) = 9 + 12 + 4 =', TX, 'start'), 2.2)
    f.show(R(420, Y1 + 27, 46, 28, FI, FI, 6) + M(443, Y1 + 46, '25', 'var(--on-fill)'), 2.9)
    Y2 = 232
    f.show(L(0, Y2 - 34, 700, Y2 - 34, RULE), 3.4)
    f.show(S(0, Y2, 'kernel: stay in 2D', VI, bold=True), 3.6)
    f.show(M(0, Y2 + 34, '{K}({a}, {b}) = ({a}·{b})² = (3 + 2)² = 5² =', TX, 'start'), 4.2)
    f.show(R(222, Y2 + 15, 46, 28, FI, FI, 6) + M(245, Y2 + 34, '25', 'var(--on-fill)'), 4.9)
    f.show(S(290, Y2 + 34, 'same number, no 3D coordinates', FI, bold=True), 5.4)
    return finish(f, 290)

# ---------- 4.1 Linear kernel ----------
def fig_linear():
    f = Anim('svm14-', 720, 0, 'The linear kernel K = x·x′ keeps the original two features. The score is a sum over the three support '
             'vectors, which collapses to w·x + b with w = (0.75, 0.5) and b = −5.75: a straight boundary.',
             'LINEAR KERNEL · NO LIFT · A STRAIGHT BOUNDARY')
    P = Plane(40, 320, 27)
    f.static(frame(P))
    for p, y in zip(X0, Y0): f.static(pt(P, p, y))
    for i in SV0: f.show(ring(P, X0[i]), .3)
    f.show(band(P, W0, B0, FI, '.10') + line(P, W0, B0, 0, FI, 2.4), 2.6)
    X = 360
    f.show(M(X, 70, '{F}({x}) = Σ αᵢ {y}ᵢ ({x}ᵢ · {x}) + {b}', TX, 'start'), .6)
    f.show(S(X, 98, 'sum over the 3 support vectors', MU), 1.0)
    f.show(M(X, 140, '= {w} · {x} + {b}', TX, 'start'), 1.8)
    f.show(M(X, 168, '{w} = Σ αᵢ {y}ᵢ {x}ᵢ = (0.75, 0.5)', TX, 'start'), 2.2)
    f.show(S(X, 214, 'linear in x → a straight line', FI, bold=True), 2.8)
    f.show(S(X, 240, 'use it when features are many (text)', MU), 3.4)
    assert [round(v, 3) for v in W0] == [0.75, 0.5]
    return finish(f, 340)

# ---------- 4.2 Polynomial kernel: lift to 3D ----------
def fig_poly():
    inner = [(1.1 * math.cos(i * math.pi / 4 + .3), 1.1 * math.sin(i * math.pi / 4 + .3)) for i in range(8)]
    outer = [(3 * math.cos(i * math.pi / 6), 3 * math.sin(i * math.pi / 6)) for i in range(12)]
    pts = [(p, 1) for p in inner] + [(p, -1) for p in outer]
    best = 0
    for k in range(180):
        th = k * math.pi / 180; u = (math.cos(th), math.sin(th))
        for bb in [i / 20 for i in range(-80, 81)]:
            for s in (1, -1):
                best = max(best, sum(1 for p, y in pts if s * (u[0] * p[0] + u[1] * p[1] + bb) * y > 0))
    good3 = sum(1 for p, y in pts if (p[0] ** 2 + p[1] ** 2 < 5) == (y > 0))
    assert best == 13 and good3 == 20
    f = Anim('svm15-', 720, 0, 'Left, an inner ring of class +1 inside an outer ring of class −1: the best straight line gets only 13 of '
             '20 right. Each point is lifted to a height z = x₁² + x₂²: 1.21 for the inner ring, 9 for the outer. In 3D a flat plane '
             'at z = 5 separates them, 20 of 20. Back in the plane, that cut is a circle of radius √5.',
             'NO LINE IN 2D · LIFT WITH z = x₁² + x₂² · A FLAT PLANE IN 3D')
    P = Plane(150, 200, 30)
    f.static(R(P.X(-4), P.Y(4), 240, 240, BG, RULE, 4) + L(P.X(-4), P.Y(0), P.X(4), P.Y(0), RULE) + L(P.X(0), P.Y(-4), P.X(0), P.Y(4), RULE) +
             M(P.X(4) + 6, P.Y(0) + 5, '{x}₁', MU, 'start') + M(P.X(0), P.Y(4) - 7, '{x}₂', MU) + S(P.X(0), 30, '2D', MU, 'middle', True))
    for p, y in pts: f.static(pt(P, p, y))
    f.show(L(P.X(-4), P.Y(-1.2), P.X(4), P.Y(2.0), RO, 2, '5 4'), .4, hide=2.6)
    f.show(S(P.X(0), P.Y(-4) + 22, 'best straight line: 13 / 20', RO, 'middle', True), .7, hide=2.6)
    # oblique 3D: screen = (ox + 24 x1 + 11 x2, oy - 16 z + 7 x2)  wait: depth goes up-right
    ox, oy = 540, 300
    Q = lambda x1, x2, z: (ox + 25 * x1 + 12 * x2, oy - 7 * x2 - 19 * z)
    fl = [Q(-3.6, -3.6, 0), Q(3.6, -3.6, 0), Q(3.6, 3.6, 0), Q(-3.6, 3.6, 0)]
    f.show(poly(fl + [fl[0]], RULE_HI, 1, None, 'var(--sunk)') + M(Q(3.6, -3.6, 0)[0] + 6, Q(3.6, -3.6, 0)[1] + 4, '{x}₁', MU, 'start') +
           M(Q(3.6, 3.6, 0)[0] + 6, Q(3.6, 3.6, 0)[1] + 4, '{x}₂', MU, 'start') +
           vec(*Q(-3.6, -3.6, 0), Q(-3.6, -3.6, 9.6)[0], Q(-3.6, -3.6, 9.6)[1], MU, 1.2) +
           M(Q(-3.6, -3.6, 9.6)[0] - 6, Q(-3.6, -3.6, 9.6)[1] + 4, '{z}', MU, 'end') + S(ox, 30, '3D', MU, 'middle', True), 2.8)
    f.show(M(ox, 54, '{z} = {x}₁² + {x}₂²', VI), 3.0)
    order = sorted(range(len(pts)), key=lambda k: -pts[k][0][1])  # back to front
    for n, k in enumerate(order):
        p, y = pts[k]; z = p[0] ** 2 + p[1] ** 2
        bx, by = Q(p[0], p[1], 0); tx, ty = Q(p[0], p[1], z)
        f.show(L(bx, by, tx, ty, tn(BR, '.45'), 1) + '<circle cx="%.1f" cy="%.1f" r="1.6" fill="%s"/>' % (bx, by, GH), 3.4 + n * .04)
        f.path(pt(lambda u, v: (u, v), (tx, ty), y), [(0, bx - tx, by - ty), (3.6 + n * .04, 0, 0)], 3.4 + n * .04, d=.7)
    pl = [Q(-3.6, -3.6, 5), Q(3.6, -3.6, 5), Q(3.6, 3.6, 5), Q(-3.6, 3.6, 5)]
    f.show(poly(pl + [pl[0]], FI, 1.6, None, tn(FI, '.16')), 5.4)
    f.show(T(pl[1][0] + 8, pl[1][1] + 4, 'plane z = 5', FI, 'start', 'sv-s', bold=True), 5.6)
    f.show(S(ox, 352, 'flat plane: 20 / 20', FI, 'middle', True), 5.9)
    r = math.sqrt(5) * P.sx
    f.show('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="2.4"/>' % (P.ox, P.oy, r, FI), 6.8)
    f.show(S(P.X(0), P.Y(-4) + 22, 'back in 2D: a circle, radius √5', FI, 'middle', True), 7.1)
    return finish(f, 366)

# ---------- 4.3 RBF kernel ----------
def fig_rbf():
    xs = [1, 2, 3, 4.5, 5.5, 6.5, 8, 9]; ys = [-1, -1, 1, 1, 1, -1, -1, -1]
    X = [(x, 0) for x in xs]
    f = Anim('svm16-', 720, 0, 'Eight points on one axis, three class +1 points in the middle. In the RBF kernel each point puts a bump '
             'on the axis, up for class +1 and down for class −1; the score F is their weighted sum. γ = 0.1: wide bumps, one smooth '
             'hill over the middle, the test point at 3.75 scores +2.03, correct. γ = 5: narrow bumps, one spike per point, the test '
             'point between them scores −0.10, wrong.', 'EACH POINT A BUMP · F = THEIR WEIGHTED SUM · γ SETS THE WIDTH')
    for k, (g, col) in enumerate(((0.1, FI), (5, RO))):
        a, b = smo(X, ys, 10, rbf(g)); K = rbf(g)
        F = lambda t: sum(a[j] * ys[j] * K(X[j], (t, 0)) for j in range(8)) + b
        P = Plane(40 + k * 350, 160, 30, 26)
        t0 = .4 + k * 4.2
        f.static(L(P.X(0), P.Y(0), P.X(10), P.Y(0), MU, 1.1) + L(P.X(0), P.Y(-3.3), P.X(0), P.Y(2.6), RULE) +
                 M(P.X(10) + 4, P.Y(0) + 5, '{x}', MU, 'start') + M(P.X(0), P.Y(2.6) - 6, '{F}', MU) +
                 T(P.X(0) - 5, P.Y(0) + 4, '0', FA, 'end'))
        for x, y in zip(xs, ys): f.static(pt(P, (x, 0), y))
        f.show(M(P.X(5), 40, 'γ = %g' % g, col) + S(P.X(5), 58, ['wide bumps: one smooth hill', 'narrow bumps: one spike per point'][k], MU, 'middle'), t0)
        for j in range(8):
            bump = [P(i / 20, ys[j] * K(X[j], (i / 20, 0))) for i in range(201)]
            f.show(poly(bump, GH, 1, '3 3'), t0 + .3 + j * .1)
        pts = [P(i / 20, F(i / 20)) for i in range(201)]
        for i in range(0, 200, 25):
            f.show(poly(pts[i:i + 26], col, 2.4), t0 + 1.4 + i / 200 * 1.2, d=.12)
        v = F(3.75)
        assert round(v, 2) == (2.03 if k == 0 else -0.10)
        x0, y0 = P(3.75, 0)
        f.show(L(x0, y0 + 26, x0, P.Y(v), VI, 1.2, '3 3') + '<rect x="%.1f" y="%.1f" width="10" height="10" fill="%s" transform="rotate(45 %.1f %.1f)"/>' % (x0 - 5, y0 + 21, VI, x0, y0 + 26), t0 + 2.9)
        f.show(S(x0, 268, 'test x = 3.75 → F = %+.2f' % v, VI, 'middle', True), t0 + 3.2)
        f.show(S(x0, 288, ['class +1, correct', 'class −1, wrong (overfit)'][k], FI if v > 0 else RO, 'middle', True), t0 + 3.5)
    return finish(f, 300)

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
    <li><a href="../logistic-regression/index.html">Logistic regression</a> on separable data has no unique best line; the widest-band rule picks exactly one.</li>
    <li>A wide band is regularization: a slightly shifted new point still lands on the right side.</li>
  </ul>
</section>

<section id="svm-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Hyperplane &amp; margin</h2></div>
  <p class="key">The line is a <em>hyperplane</em> <span class="mth"><var>w</var> · <var>x</var> + <var>b</var> = 0</span>; the margin is the band between the two parallel lines where the score is ±1.</p>

  <div class="subsec" id="svm-s2-1">
    <h3 class="ssh"><b>2.1</b>Decision function</h3>
    <p class="skey">Every point gets a score <span class="mth"><var>F</var>(<var>x</var>)</span>; its <em>sign</em> says which side of the line it is on.</p>
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
    </div>
{svm11}
    <ul class="why">
      <li>SVM returns a score (a signed distance), not a probability; a sigmoid fitted afterwards (<b>Platt scaling</b>, <code>SVC(probability=True)</code>) converts it — or use logistic regression, see <a href="../../09-evaluation/calibration/index.html">Calibration</a>.</li>
    </ul>
  </div>

  <div class="subsec" id="svm-s2-2">
    <h3 class="ssh"><b>2.2</b>Margin width</h3>
    <p class="skey">The band edges are <span class="mth"><var>F</var> = ±1</span>, so the band is <em>wider when <span class="mth">‖<var>w</var>‖</span> is shorter</em>.</p>
    <div class="eq">
      <div class="line">
        <span class="t"><span>margin</span></span>
        <span class="op">=</span>
        <span class="t b"><span><span class="frac"><i>2</i><i>‖<var>w</var>‖</i></span></span><em>shorter w, wider band</em></span>
      </div>
    </div>
{svm2}
    <ul class="why">
      <li>Widest band = smallest <span class="mth">‖<var>w</var>‖²</span>, the same penalty as <a href="../ridge-lasso-elasticnet/index.html">Ridge</a>.</li>
      <li>The margin is a distance, so the feature with the largest unit dominates it: <b>standardize features</b> (<code>StandardScaler</code>) before <code>SVC</code>.</li>
    </ul>
  </div>

  <div class="subsec" id="svm-s2-3">
    <h3 class="ssh"><b>2.3</b>Support vectors</h3>
    <p class="skey">Remove every point that does not touch the band and train again: <em>the line does not move</em>.</p>
{svm4}
    <ul class="why">
      <li>The model stores only the support vectors (3 of 18 here), so it is compact and prediction is fast.</li>
      <li>The flip side: a single noisy point near the boundary can move the whole line.</li>
    </ul>
  </div>
</section>

<section id="svm-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Hard &amp; soft margin</h2></div>
  <p class="key">Hard margin forbids any point inside the band. Soft margin allows it and charges a penalty. Real data always uses soft.</p>

  <div class="subsec" id="svm-s3-1">
    <h3 class="ssh"><b>3.1</b>Hard margin</h3>
    <p class="skey">Widest band such that <em>every</em> point is on its own side and past the band.</p>
    <div class="eq">
      <div class="line">
        <span class="t"><span><b class="fn">min</b> <span class="frac"><i>‖<var>w</var>‖<sup>2</sup></i><i>2</i></span></span><em>widest band</em></span>
        <span class="op">s.t.</span>
        <span class="t r"><span><var>y</var><sub><var>i</var></sub> <var>F</var>(<var>x</var><sub><var>i</var></sub>) ≥ 1</span><em>every point past the band</em></span>
      </div>
    </div>
{svm12}
    <ul class="why">
      <li>Works only when the classes separate perfectly; one mislabelled point leaves no solution.</li>
    </ul>
  </div>

  <div class="subsec" id="svm-s3-2">
    <h3 class="ssh"><b>3.2</b>Soft margin &amp; hinge</h3>
    <p class="skey">Score every point, take its margin <span class="mth"><var>y</var> · <var>F</var></span>, and charge <em>hinge</em> only to points not yet past the band.</p>
    <div class="eq">
      <div class="line">
        <span class="t"><span><var>L</var></span></span>
        <span class="op">=</span>
        <span class="t b"><span><span class="frac"><i>‖<var>w</var>‖<sup>2</sup></i><i>2</i></span></span><em>wide band (L2)</em></span>
        <span class="op">+</span>
        <span class="t p"><span><var>C</var></span><em>price of intrusion</em></span>
        <span class="op">·</span>
        <span class="t r"><span>Σ<sub><var>i</var></sub> <b class="fn">max</b>(0, 1 − <var>y</var><sub><var>i</var></sub> <var>F</var>(<var>x</var><sub><var>i</var></sub>))</span><em>hinge</em></span>
      </div>
    </div>
{svm3}
    <ul class="why">
      <li>Hinge is 0 from margin 1 onward, so points past the band cost nothing and drop out of the solution.</li>
      <li>Counting mistakes has zero slope everywhere; hinge is its sloped stand-in, and it grows linearly, so label noise hurts less than with AdaBoost's exponential loss.</li>
    </ul>
  </div>

  <div class="subsec" id="svm-s3-3">
    <h3 class="ssh"><b>3.3</b>C</h3>
    <p class="skey">Large <span class="mth"><var>C</var></span> makes intrusion expensive: narrow band, close to hard margin. Small <span class="mth"><var>C</var></span> makes it cheap: wide band.</p>
{svm5}
    <ul class="why">
      <li><span class="mth"><var>C</var></span> plays the role of <span class="mth">1/<var>λ</var></span> in Ridge: large <span class="mth"><var>C</var></span> overfits, small underfits; <span class="mth"><var>C</var> → ∞</span> is hard margin.</li>
      <li>Tune <span class="mth"><var>C</var></span> (and <span class="mth"><var>γ</var></span> for RBF) together on a log grid with <a href="../../04-core-concepts/train-val-test-cv/index.html">cross-validation</a>.</li>
    </ul>
  </div>
</section>

<section id="svm-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Kernel trick</h2></div>
  <p class="key">The solver only needs dot products between pairs of points, so a function <span class="mth"><var>K</var>(<var>x</var>, <var>x</var>′) = <var>φ</var>(<var>x</var>) · <var>φ</var>(<var>x</var>′)</span> can stand in for <em>lifting the points into more dimensions</em>.</p>
{svm13}
  <ul class="why">
    <li>A kernel compares every pair of points: an <span class="mth"><var>n</var> × <var>n</var></span> matrix, so training slows down sharply beyond a few tens of thousands of rows. SVM shines with few samples and many features (text, genes); medium tabular data usually goes to <a href="../../06-tree-models/gradient-boosting/index.html">gradient boosting</a>.</li>
  </ul>

  <div class="subsec" id="svm-s4-1">
    <h3 class="ssh"><b>4.1</b>Linear kernel</h3>
    <p class="skey">No lift at all: the score stays linear in <span class="mth"><var>x</var></span>, so the boundary is <em>straight</em>.</p>
    <div class="eq">
      <div class="line">
        <span class="t"><span><var>K</var>(<var>x</var>, <var>x</var>′)</span></span>
        <span class="op">=</span>
        <span class="t b"><span><var>x</var> · <var>x</var>′</span><em>plain dot product</em></span>
      </div>
    </div>
{svm14}
  </div>

  <div class="subsec" id="svm-s4-2">
    <h3 class="ssh"><b>4.2</b>Polynomial kernel</h3>
    <p class="skey">Adds squared and cross terms. Two rings no line can split sit at <em>different heights</em> after adding <span class="mth"><var>x</var><sub>1</sub><sup>2</sup> + <var>x</var><sub>2</sub><sup>2</sup></span>, and a flat plane separates them.</p>
    <div class="eq">
      <div class="line">
        <span class="t"><span><var>K</var>(<var>x</var>, <var>x</var>′)</span></span>
        <span class="op">=</span>
        <span class="t b"><span>(<var>x</var> · <var>x</var>′ + <var>c</var>)<sup><var>d</var></sup></span><em>degree d</em></span>
      </div>
    </div>
{svm15}
    <ul class="why">
      <li>Degree 2 in 2D already means 6 terms: <span class="mth">1, <var>x</var><sub>1</sub>, <var>x</var><sub>2</sub>, <var>x</var><sub>1</sub><sup>2</sup>, <var>x</var><sub>2</sub><sup>2</sup>, <var>x</var><sub>1</sub><var>x</var><sub>2</sub></span>; the kernel never writes them out.</li>
    </ul>
  </div>

  <div class="subsec" id="svm-s4-3">
    <h3 class="ssh"><b>4.3</b>RBF kernel</h3>
    <p class="skey">Each point puts a <em>bump</em> around itself; the score is their weighted sum, so the boundary wraps each region. <span class="mth"><var>γ</var></span> sets the bump width.</p>
    <div class="eq">
      <div class="line">
        <span class="t"><span><var>K</var>(<var>x</var>, <var>x</var>′)</span></span>
        <span class="op">=</span>
        <span class="t b"><span><var>e</var><sup>−<var>γ</var>‖<var>x</var> − <var>x</var>′‖<sup>2</sup></sup></span><em>1 at the point, fades with distance</em></span>
      </div>
    </div>
{svm16}
    <ul class="why">
      <li>Small <span class="mth"><var>γ</var></span> is smooth; large <span class="mth"><var>γ</var></span> memorizes the training points and fails between them (overfitting). RBF is the default kernel in <code>SVC</code>.</li>
      <li>Rewrite <span class="mth"><var>K</var> = <var>e</var><sup>−<var>γ</var>‖<var>x</var>‖²</sup> <var>e</var><sup>−<var>γ</var>‖<var>x</var>′‖²</sup> <var>e</var><sup>2<var>γ</var> <var>x</var>·<var>x</var>′</sup></span> and expand the last factor by Taylor, <span class="mth"><var>e</var><sup><var>t</var></sup> = 1 + <var>t</var> + <var>t</var>²/2! + …</span>: the terms never end, so the lifted space is <b>infinite-dimensional</b> and only the kernel can reach it.</li>
    </ul>
  </div>
</section>

'''

def build():
    figs = dict(svm1=fig_mental(), svm2=fig_geom(), svm3=fig_learn(), svm4=fig_sv(), svm5=fig_c(), svm11=fig_score(),
                svm12=fig_hard(), svm13=fig_identity(), svm14=fig_linear(), svm15=fig_poly(), svm16=fig_rbf())
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
    splice(PAGE, build(), 'Separate two classes with the widest empty band: margin, support vectors, hard and soft margin, hinge loss, C, and linear, polynomial and RBF kernels.')
    print('ok')
