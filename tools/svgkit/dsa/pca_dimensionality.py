# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/08-dimensionality/pca-dimensionality.
Eight people, height (cm) and weight (kg); every number in a figure is computed here and pinned with assert.
The scree figure uses a 40 x 6 table drawn from random.Random(2): five columns driven by two hidden factors + one noise column.
Run: python3 pca_dimensionality.py"""
import os, re, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import (Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, GH, RULE, SUNK, BG,
                            tn, M, S, chip, dot, poly, Plane, finish, vec, mcell)
from tablefig import pill
from decision_tree import splice

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/08-dimensionality/pca-dimensionality/index.html')

# ---------- data ----------
IDS = list('ABCDEFGH')
HT = [158, 162, 165, 168, 172, 175, 178, 182]
WT = [58, 57, 66, 63, 74, 72, 82, 88]
N = len(IDS)
MH, MW = sum(HT) / N, sum(WT) / N
assert (MH, MW) == (170, 70)
HC = [int(h - MH) for h in HT]; WC = [int(w - MW) for w in WT]
assert HC == [-12, -8, -5, -2, 2, 5, 8, 12] and WC == [-12, -13, -4, -7, 4, 2, 12, 18]

def cov2(xs, ys):
    n = len(xs); mx, my = sum(xs) / n, sum(ys) / n
    a = sum((x - mx) ** 2 for x in xs) / (n - 1); c = sum((y - my) ** 2 for y in ys) / (n - 1)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (n - 1)
    return a, b, c

def eig2(a, b, c):
    """symmetric [[a, b], [b, c]] -> (l1, l2, v1, v2), v1 with positive components, v2 = v1 turned +90 deg"""
    tr, det = a + c, a * c - b * b
    l1 = tr / 2 + math.sqrt(tr * tr / 4 - det); l2 = tr - l1
    vx, vy = (b, l1 - a) if abs(b) > 1e-12 else ((1, 0) if a >= c else (0, 1))
    nv = math.hypot(vx, vy); vx, vy = vx / nv, vy / nv
    if vx < 0: vx, vy = -vx, -vy
    return l1, l2, (vx, vy), (-vy, vx)

SXX, SXY, SYY = cov2(HC, WC)
assert (sum(h * h for h in HC), sum(h * w for h, w in zip(HC, WC)), sum(w * w for w in WC)) == (474, 612, 866)
assert (round(SXX, 1), round(SXY, 1), round(SYY, 1)) == (67.7, 87.4, 123.7)
L1, L2, V1, V2 = eig2(SXX, SXY, SYY)
assert (round(L1, 1), round(L2, 1)) == (187.5, 3.9)
assert (round(V1[0], 2), round(V1[1], 2)) == (.59, .81) and (round(V2[0], 2), round(V2[1], 2)) == (-.81, .59)
TH = math.degrees(math.atan2(V1[1], V1[0])); assert round(TH, 1) == 53.9
Z1 = [h * V1[0] + w * V1[1] for h, w in zip(HC, WC)]
Z2 = [h * V2[0] + w * V2[1] for h, w in zip(HC, WC)]
assert [round(z, 1) for z in Z1] == [-16.8, -15.2, -6.2, -6.8, 4.4, 4.6, 14.4, 21.6]
assert [round(z, 1) for z in Z2] == [2.6, -1.2, 1.7, -2.5, .7, -2.9, .6, .9]
assert abs(sum(z * z for z in Z1) / 7 - L1) < 1e-9 and abs(sum(z * z for z in Z2) / 7 - L2) < 1e-9
EVR = L1 / (L1 + L2); assert round(EVR, 3) == .980
# C v = lambda v
CV1 = (SXX * V1[0] + SXY * V1[1], SXY * V1[0] + SYY * V1[1])
assert all(abs(CV1[k] - L1 * V1[k]) < 1e-9 for k in (0, 1)) and (round(CV1[0], 1), round(CV1[1], 1)) == (110.5, 151.5)
CU = (SXX, SXY)                                      # C times (1, 0): turns
assert round(math.degrees(math.atan2(CU[1], CU[0])), 1) == 52.2

def var_at(deg):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    return SXX * c * c + 2 * SXY * s * c + SYY * s * s
SCAN = [0, 15, 30, 45, 60, 75, 90]
VSCAN = [var_at(a) for a in SCAN]
assert [round(v) for v in VSCAN] == [68, 115, 157, 183, 185, 164, 124]
assert abs(var_at(TH) - L1) < 1e-9 and all(var_at(a / 10) <= L1 + 1e-9 for a in range(0, 1801))

# reconstruction: x_hat = z1 v1; residual length = |z2|; mean squared error = lambda2
REC = [(z * V1[0], z * V1[1]) for z in Z1]
ERR = sum((h - a) ** 2 + (w - b) ** 2 for (a, b), h, w in zip(REC, HC, WC)) / 7
assert abs(ERR - L2) < 1e-9 and round(ERR, 1) == 3.9

# units: height in mm -> PC1 turns to height; standardised -> 45 deg
MM = cov2([h * 10 for h in HC], WC); LMM = eig2(*MM)
assert round(MM[0]) == 6771 and round(MM[2], 1) == 123.7
assert (round(LMM[2][0], 2), round(LMM[2][1], 2)) == (.99, .13)
TH_MM = math.degrees(math.atan2(LMM[2][1], LMM[2][0])); assert round(TH_MM, 1) == 7.4
SDH, SDW = math.sqrt(SXX), math.sqrt(SYY)
ZH = [h / SDH for h in HC]; ZW = [w / SDW for w in WC]
ZS = cov2(ZH, ZW); LZ = eig2(*ZS)
assert round(ZS[0], 6) == 1 and round(ZS[2], 6) == 1 and round(ZS[1], 2) == .96
assert (round(LZ[2][0], 2), round(LZ[2][1], 2)) == (.71, .71)
assert (round(LZ[0], 2), round(LZ[1], 2)) == (1.96, .04)

# ---------- 6-column table for the scree / cumulative curve ----------
def jacobi(A):
    n = len(A); A = [r[:] for r in A]
    for _ in range(200):
        p, q = max(((i, j) for i in range(n) for j in range(i + 1, n)), key=lambda ij: abs(A[ij[0]][ij[1]]))
        if abs(A[p][q]) < 1e-13: break
        th = .5 * math.atan2(2 * A[p][q], A[q][q] - A[p][p]); c, s = math.cos(th), math.sin(th)
        for k in range(n):
            a, b = A[k][p], A[k][q]; A[k][p], A[k][q] = c * a - s * b, s * a + c * b
        for k in range(n):
            a, b = A[p][k], A[q][k]; A[p][k], A[q][k] = c * a - s * b, s * a + c * b
    return sorted((A[i][i] for i in range(n)), reverse=True)

def six():
    g = random.Random(2); X = []
    for _ in range(40):
        s, t = g.gauss(0, 1), g.gauss(0, 1); e = lambda k: g.gauss(0, k)
        X.append([s + .2 * t + e(.25), .8 * s + .5 * t + e(.3), s + e(.2), .9 * s - .2 * t + e(.3), .7 * s + .4 * t + e(.4), e(1)])
    n = len(X); m = [sum(r[j] for r in X) / n for j in range(6)]
    sd = [math.sqrt(sum((r[j] - m[j]) ** 2 for r in X) / (n - 1)) for j in range(6)]
    Z = [[(r[j] - m[j]) / sd[j] for j in range(6)] for r in X]
    C = [[sum(r[i] * r[j] for r in Z) / (n - 1) for j in range(6)] for i in range(6)]
    return jacobi(C)
EIG6 = six()
assert abs(sum(EIG6) - 6) < 1e-9
assert [round(v, 2) for v in EIG6] == [4.61, .87, .32, .1, .05, .04]
R6 = [v / 6 for v in EIG6]; CUM6 = [sum(R6[:k + 1]) for k in range(6)]
assert [round(c, 3) for c in CUM6[:3]] == [.769, .914, .968]
K95 = next(k + 1 for k, c in enumerate(CUM6) if c >= .95); assert K95 == 3

# ---------- helpers ----------
def fm(v, d=1):
    s = ('%.' + str(d) + 'f') % abs(v)
    return ('−' if v < 0 and float(s) != 0 else '') + s

def cross(P, r, xl='{x}₁', yl='{x}₂', lab=True):
    """axes through the origin of a centred plane"""
    s = L(P.X(-r[0]), P.oy, P.X(r[0]), P.oy, RULE_HI, 1.2) + L(P.ox, P.Y(-r[1]), P.ox, P.Y(r[1]), RULE_HI, 1.2)
    if lab: s += M(P.X(r[0]) + 6, P.oy + 5, xl, MU, 'start') + M(P.ox, P.Y(r[1]) - 8, yl, MU)
    return s

def axis_line(P, v, r, c=FI, sw=2.2, dash=None):
    return L(P.X(-r * v[0]), P.Y(-r * v[1]), P.X(r * v[0]), P.Y(r * v[1]), c, sw, dash)

def pdot(x, y, c=BR, r=4.5):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (x, y, r, c, BG)

def ring(x, y, r, c, sw=1.2):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (x, y, r, c, sw)

def vals_row(t, i, vals, colors=None):
    return t.row(i, vals, colors=colors)

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('pca1-', 720, 0, 'Eight people, centred height x1 and weight x2, plotted as eight points stretched along a diagonal. '
             'The diagonal of most spread is drawn as PC1 and the line across it as PC2. The whole cloud turns until PC1 '
             'lies flat; each point now has new coordinates z1 and z2, which fill two new columns of the table. z2 is '
             'almost zero everywhere, so the points drop onto the z1 axis and the two original columns are replaced by '
             'one, keeping 98 percent of the variance.', 'TURN THE AXES TO THE SPREAD · THEN DROP THE THIN DIRECTION')
    t = Table(0, 30, [('id', 26), ('x₁', 46, 'height'), ('x₂', 46, 'weight'), ('z₁', 46, 'PC1'), ('z₂', 46, 'PC2')])
    f.static(t.head())
    for i, n in enumerate(IDS):
        f.static(t.row(i, [n, fm(HC[i], 0), fm(WC[i], 0), '', '']))
    P = Plane(500, 168, 6.2)
    f.show(cross(P, (24, 21), lab=False) + M(P.X(24) + 6, P.oy + 5, '{x}₁', MU, 'start') + M(P.ox, P.Y(21) - 8, '{x}₂', MU),
           .1, hide=2.4)
    f.show(cross(P, (24, 21), lab=False), 2.4)
    f.show(M(P.X(24) + 6, P.oy + 5, '{z}₁', FI, 'start') + M(P.ox, P.Y(21) - 8, '{z}₂', VI), 4.8)
    f.show(axis_line(P, V1, 26, FI, 2.2, '6 4') + S(P.X(26 * V1[0]) + 6, P.Y(26 * V1[1]) + 4, 'PC1', FI, 'start', True), 1.2, hide=2.4)
    f.show(axis_line(P, V2, 10, VI, 1.8, '6 4') + S(P.X(10 * V2[0]) - 6, P.Y(10 * V2[1]), 'PC2', VI, 'end', True), 1.6, hide=2.4)
    T0, T1 = 2.6, 5.8
    for i in range(N):
        fx, fy = P.X(Z1[i]), P.oy
        pts = [(0, P.X(HC[i]) - fx, P.Y(WC[i]) - fy)]
        for k in range(1, 5):
            ph = math.radians(TH * k / 4); c, s = math.cos(ph), math.sin(ph)
            x, y = HC[i] * c + WC[i] * s, -HC[i] * s + WC[i] * c
            pts.append((T0 + (k - 1) * .45, P.X(x) - fx, P.Y(y) - fy))
        pts.append((T1 + i * .05, 0, 0))
        f.path(pdot(fx, fy, BR, 4.5), pts, .2 + i * .06, d=.45)
    for i in range(N):
        f.show(t.cell(i, 3, fm(Z1[i]), c=FI), 4.6 + i * .08)
        f.show(t.cell(i, 4, fm(Z2[i]), c=VI), 4.6 + i * .08)
    f.show(t.dimcol(1, N) + t.dimcol(2, N) + t.dimcol(4, N), 6.6)
    f.show(t.colbox(3, N, FI), 6.8)
    yb = t.bottom(N) + 26
    f.show(chip(t.cx(3) + 40, yb, '2 columns → 1 · keeps %.0f%% of the variance' % (100 * EVR), FI, 300, False), 7.0)
    return finish(f, yb + 22)

# ---------- 02 Centring ----------
def fig_centre():
    f = Anim('pca2-', 720, 0, 'The table of heights and weights and the same eight people as points. The column means, 170 cm and '
             '70 kg, are marked as a cross in the middle of the cloud. Each value then has its mean subtracted: the cells '
             'change to deviations such as minus 12, and the cloud glides to a new plane where the mean cross sits on the '
             'origin.', 'SUBTRACT EACH COLUMN MEAN · THE CLOUD MOVES TO THE ORIGIN')
    t = Table(0, 30, [('id', 26), ('x₁', 76, 'height cm'), ('x₂', 76, 'weight kg')])
    f.static(t.head())
    for i, n in enumerate(IDS):
        f.static(t.row(i, [n, str(HT[i]), str(WT[i])]))
    s = 5.4
    RX = lambda h: 226 + (h - 155) * s
    RY = lambda w: 262 - (w - 50) * s
    CX = lambda h: 540 + h * s
    CY = lambda w: 160 - w * s
    # raw panel axes
    f.static(L(RX(155), RY(50), RX(186), RY(50), RULE_HI, 1.2) + L(RX(155), RY(50), RX(155), RY(92), RULE_HI, 1.2))
    for h in (160, 170, 180):
        f.static(L(RX(h), RY(50), RX(h), RY(50) + 4, RULE_HI) + T(RX(h), RY(50) + 16, str(h), FA, mono=True))
    for w in (60, 70, 80, 90):
        f.static(T(RX(155) - 6, RY(w) + 4, str(w), FA, 'end', mono=True))
    f.static(S(RX(155), 40, 'raw', MU, bold=True))
    # centred panel axes
    f.static(L(CX(-16), CY(0), CX(16), CY(0), RULE_HI, 1.2) + L(CX(0), CY(-16), CX(0), CY(21), RULE_HI, 1.2))
    for h in (-10, 10):
        f.static(T(CX(h), CY(0) + 15, fm(h, 0), FA, mono=True))
    for w in (-10, 10):
        f.static(T(CX(0) - 6, CY(w) + 4, fm(w, 0), FA, 'end', mono=True))
    f.static(S(CX(-16), 40, 'centred', MU, bold=True) + M(CX(16) + 6, CY(0) + 5, '{x}₁', MU, 'start') +
             M(CX(0), CY(21) - 8, '{x}₂', MU))
    # means
    yb = t.bottom(N) + 22
    f.show(T(t.cx(0), yb, 'mean', MU) + T(t.cx(1), yb, '170', VI, mono=True, bold=True) +
           T(t.cx(2), yb, '70', VI, mono=True, bold=True), 1.0)
    for j in (1, 2):
        f.show(t.colbox(j, N, VI), .9, hide=2.0)
    mx, my = CX(0), CY(0)
    mark = L(mx - 9, my, mx + 9, my, VI, 2) + L(mx, my - 9, mx, my + 9, VI, 2)
    f.path(mark, [(0, RX(170) - mx, RY(70) - my), (2.4, 0, 0)], 1.3, d=1.0)
    f.show(S(RX(170) + 10, RY(70) + 26, 'mean', VI, bold=True), 1.4, hide=2.4)
    for i in range(N):
        x, y = CX(HC[i]), CY(WC[i])
        f.path(pdot(x, y), [(0, RX(HT[i]) - x, RY(WT[i]) - y), (2.4 + i * .08, 0, 0)], .2 + i * .05, d=1.0)
    for i in range(N):
        f.show(t.cell(i, 1, fm(HC[i], 0), c=BR) + t.cell(i, 2, fm(WC[i], 0), c=BR), 2.4 + i * .1)
    f.show(R(t.colx(1) + 1, t.hb - 12, 150, 30, BG, 'none', 2) + T(t.cx(1), t.hb, 'x₁', MU) + T(t.cx(1), t.hb + 13, 'height − 170', FA) +
           T(t.cx(2), t.hb, 'x₂', MU) + T(t.cx(2), t.hb + 13, 'weight − 70', FA), 2.4)
    f.show(R(0, yb - 15, t.w, 22, BG, 'none') + T(t.cx(0), yb, 'mean', MU) + T(t.cx(1), yb, '0', FI, mono=True, bold=True) +
           T(t.cx(2), yb, '0', FI, mono=True, bold=True), 3.6)
    f.show(S(CX(1.5), CY(0) + 30, 'mean = (0, 0)', FI, 'start', True), 3.8)
    return finish(f, max(yb + 14, RY(50) + 24))

# ---------- 3.1 Direction of most spread ----------
def fig_spread():
    f = Anim('pca3-', 720, 0, 'The centred cloud. A line through the origin turns in steps of 15 degrees from flat to upright. At '
             'each angle every point drops a foot onto the line, and the variance of those feet is plotted on the right: '
             '68, 115, 157, 183, 185, 164, 124. The curve peaks between 45 and 60 degrees; the exact top is 53.9 degrees '
             'with variance 187.5. That line is PC1.', 'TURN A LINE · MEASURE THE SPREAD OF THE SHADOWS · KEEP THE WIDEST')
    P = Plane(190, 186, 5.8)
    f.static(cross(P, (25, 24)))
    for i in range(N):
        f.static(pdot(P.X(HC[i]), P.Y(WC[i]), BR, 4))
    GX, GY, GW, GH_ = 450, 60, 240, 200
    gx = lambda a: GX + a / 90 * GW
    gy = lambda v: GY + GH_ - v / 200 * GH_
    f.static(L(GX, gy(0), GX + GW, gy(0), MU, 1.2) + L(GX, gy(0), GX, GY - 6, MU, 1.2))
    for a in (0, 45, 90):
        f.static(T(gx(a), gy(0) + 16, '%d°' % a, FA, mono=True))
    for v in (50, 100, 150, 200):
        f.static(T(GX - 7, gy(v) + 4, str(v), FA, 'end', mono=True) + L(GX, gy(v), GX + GW, gy(v), RULE, 1, '2 4'))
    f.static(S(GX, GY - 16, 'variance of the feet', MU) + S(GX + GW, gy(0) + 32, 'angle of the line', MU, 'end'))
    t0, dt = .6, .9
    prev = None
    for k, (a, v) in enumerate(zip(SCAN, VSCAN)):
        u = (math.cos(math.radians(a)), math.sin(math.radians(a)))
        ts, te = t0 + k * dt, t0 + (k + 1) * dt
        feet = ''.join(pdot(P.X((h * u[0] + w * u[1]) * u[0]), P.Y((h * u[0] + w * u[1]) * u[1]), VI, 3)
                       for h, w in zip(HC, WC))
        f.show(axis_line(P, u, 26, VI, 1.8) + feet + T(P.X(27 * u[0]) + 4, P.Y(27 * u[1]) - 4, '%d°' % a, VI, 'start', mono=True, bold=True),
               ts, hide=te)
        f.show(pdot(gx(a), gy(v), VI, 4), ts + .2)
        if prev: f.show(L(gx(prev[0]), gy(prev[1]), gx(a), gy(v), VI, 1.4), ts + .2)
        f.show(T(gx(a) + (8 if a == 0 else -8 if a == 90 else 0), gy(v) - 10, str(round(v)), VI, 'start' if a == 0 else 'end' if a == 90 else 'middle', mono=True), ts + .2, hide=t0 + len(SCAN) * dt + .2 if a not in (0, 90) else None)
        prev = (a, v)
    TE = t0 + len(SCAN) * dt + .2
    f.show(axis_line(P, V1, 27, FI, 2.6) + S(P.X(27 * V1[0]) + 6, P.Y(27 * V1[1]) - 2, 'PC1', FI, 'start', True), TE)
    f.show(''.join(pdot(P.X(z * V1[0]), P.Y(z * V1[1]), FI, 3) for z in Z1), TE)
    f.show(L(gx(TH), gy(0), gx(TH), gy(L1), FI, 1.2, '3 3') + pdot(gx(TH), gy(L1), FI, 5) +
           T(gx(TH), gy(L1) - 12, 'max %.1f at %.1f°' % (L1, TH), FI, mono=True, bold=True), TE + .3)
    return finish(f, max(gy(0) + 40, P.Y(-24) + 8))

# ---------- 3.2 Projection ----------
def fig_project():
    f = Anim('pca4-', 720, 0, 'The centred cloud with the PC1 line. One point at a time, a dashed line drops from the point at a right '
             'angle onto PC1, a copy of the point slides down it to the foot, and the distance of that foot from the origin '
             'fills the new column z1 of the table: minus 16.8 for A up to 21.6 for H. At the end the two original columns '
             'are greyed and only z1 remains.', 'DROP EACH POINT ONTO PC1 · ITS POSITION ALONG THE LINE IS THE NEW VALUE')
    t = Table(0, 30, [('id', 26), ('x₁', 46, 'height'), ('x₂', 46, 'weight'), ('z₁', 56, 'on PC1')])
    f.static(t.head())
    for i, n in enumerate(IDS):
        f.static(t.row(i, [n, fm(HC[i], 0), fm(WC[i], 0), '']))
    P = Plane(470, 168, 6.2)
    f.static(cross(P, (25, 21)) + axis_line(P, V1, 27, FI, 2.2) + S(P.X(27 * V1[0]) + 6, P.Y(27 * V1[1]) + 4, 'PC1', FI, 'start', True))
    for i in range(N):
        f.static(pdot(P.X(HC[i]), P.Y(WC[i]), BR, 4.5))
    for i in range(N):
        ts = .8 + i * .7
        ox, oy = P.X(HC[i]), P.Y(WC[i]); fx, fy = P.X(Z1[i] * V1[0]), P.Y(Z1[i] * V1[1])
        f.show(t.outline(i, c=VI), ts, hide=ts + .7)
        f.show(L(ox, oy, fx, fy, VI, 1.3, '3 3'), ts)
        f.path(pdot(fx, fy, FI, 3.6), [(0, ox - fx, oy - fy), (ts + .15, 0, 0)], ts, d=.4)
        f.show(t.cell(i, 3, fm(Z1[i]), c=FI), ts + .5)
    TE = .8 + N * .7 + .2
    f.show(t.dimcol(1, N) + t.dimcol(2, N), TE)
    f.show(t.colbox(3, N, FI), TE + .2)
    f.show(S(P.X(-25), P.Y(-21) + 22, 'z₁ = x₁ · 0.59 + x₂ · 0.81', FI, 'start', True), TE + .4)
    return finish(f, max(t.bottom(N) + 14, P.Y(-21) + 30))

# ---------- 3.3 Second component ----------
def fig_pc2():
    f = Anim('pca5-', 720, 0, 'The same cloud with PC1. A second line, PC2, is drawn through the origin at a right angle to PC1. '
             'Every point drops onto PC2; the feet stay close to the origin and fill the column z2, values between minus '
             '2.9 and 2.6. On the right the variance along each axis is compared: 187.5 along PC1, 3.9 along PC2.',
             'PC2 = THE BEST DIRECTION AT A RIGHT ANGLE TO PC1')
    t = Table(0, 30, [('id', 26), ('z₁', 52, 'on PC1'), ('z₂', 52, 'on PC2')])
    f.static(t.head())
    for i, n in enumerate(IDS):
        f.static(t.row(i, [n, fm(Z1[i]), ''], colors={1: FI}))
    P = Plane(330, 168, 6.2)
    f.static(cross(P, (25, 21)) + axis_line(P, V1, 27, FI, 2.2) + S(P.X(27 * V1[0]) + 6, P.Y(27 * V1[1]) + 4, 'PC1', FI, 'start', True))
    for i in range(N):
        f.static(pdot(P.X(HC[i]), P.Y(WC[i]), BR, 4.5))
    f.show(axis_line(P, V2, 14, VI, 2.2) + S(P.X(14 * V2[0]) - 6, P.Y(14 * V2[1]) - 2, 'PC2', VI, 'end', True), .6)
    q = 2.2
    a = (V1[0] * q, V1[1] * q); b = (V2[0] * q, V2[1] * q)
    f.show(poly([P(*a), P(a[0] + b[0], a[1] + b[1]), P(*b)], VI, 1.3), .9)
    for i in range(N):
        ts = 1.6 + i * .35
        ox, oy = P.X(HC[i]), P.Y(WC[i]); fx, fy = P.X(Z2[i] * V2[0]), P.Y(Z2[i] * V2[1])
        f.show(L(ox, oy, fx, fy, VI, 1.1, '3 3'), ts)
        f.path(pdot(fx, fy, VI, 3), [(0, ox - fx, oy - fy), (ts + .1, 0, 0)], ts, d=.4)
        f.show(t.cell(i, 2, fm(Z2[i]), c=VI), ts + .4)
    BX, BY = 520, 70; sc = 160 / L1
    TB = 1.6 + N * .35 + .4
    f.show(S(BX, BY - 14, 'variance along', MU), TB)
    for k, (lab, v, c) in enumerate((('PC1', L1, FI), ('PC2', L2, VI))):
        y = BY + k * 40
        f.show(S(BX, y + 13, lab, c, bold=True) + R(BX + 36, y, max(v * sc, 2), 18, tn(c, '.30'), c, 3, 1.2) +
               T(BX + 42 + v * sc, y + 14, '%.1f' % v, c, 'start', mono=True, bold=True), TB + .2 + k * .4)
    f.show(S(BX, BY + 102, 'PC2 holds what PC1 missed', MU), TB + 1.0)
    return finish(f, max(t.bottom(N) + 14, P.Y(-21) + 16))

# ---------- 4.1 Covariance matrix ----------
def fig_cov():
    f = Anim('pca6-', 720, 0, 'The centred table gains three columns: x1 squared, x1 times x2, and x2 squared, filled row by row. '
             'Their sums, 474, 612 and 866, divided by n minus 1 = 7, travel into a 2 by 2 matrix: 67.7 and 123.7 on the '
             'diagonal, 87.4 in both off-diagonal cells.', 'MULTIPLY THE COLUMNS · AVERAGE · ONE 2 × 2 MATRIX')
    t = Table(0, 30, [('id', 26), ('x₁', 40), ('x₂', 40), ('x₁²', 52), ('x₁x₂', 52), ('x₂²', 52)])
    f.static(t.head())
    for i, n in enumerate(IDS):
        f.static(t.row(i, [n, fm(HC[i], 0), fm(WC[i], 0), '', '', '']))
    for i in range(N):
        ts = .5 + i * .3
        f.show(t.cell(i, 3, str(HC[i] ** 2)) + t.cell(i, 4, fm(HC[i] * WC[i], 0)) + t.cell(i, 5, str(WC[i] ** 2)), ts)
    yb = t.bottom(N) + 20
    sums = (474, 612, 866)
    f.show(T(t.cx(0), yb, 'Σ', MU) + ''.join(T(t.cx(3 + j), yb, str(v), VI, mono=True, bold=True) for j, v in enumerate(sums)), 3.2)
    f.show(T(t.cx(0), yb + 20, '÷ 7', MU) + ''.join(T(t.cx(3 + j), yb + 20, '%.1f' % (v / 7), VI, mono=True, bold=True)
                                                  for j, v in enumerate(sums)), 3.8)
    MX, MY, cw, ch = 520, 110, 70, 40
    f.static(M(MX - 14, MY + ch + 6, '{C} =', TX, 'end'))
    f.static(R(MX - 6, MY - 6, 2 * cw + 12, 2 * ch + 12, 'none', RULE_HI, 6))
    for (r, c) in ((0, 0), (0, 1), (1, 0), (1, 1)):
        f.static(R(MX + c * cw + 2, MY + r * ch + 2, cw - 4, ch - 4, BG, RULE_HI, 4))
    f.static(T(MX + cw / 2, MY - 14, 'x₁', MU) + T(MX + 1.5 * cw, MY - 14, 'x₂', MU) +
             T(MX + 2 * cw + 14, MY + ch / 2 + 4, 'x₁', MU, 'start') + T(MX + 2 * cw + 14, MY + 1.5 * ch + 4, 'x₂', MU, 'start'))
    dest = {3: [(0, 0)], 4: [(0, 1), (1, 0)], 5: [(1, 1)]}
    names = {3: 'var x₁', 4: 'cov', 5: 'var x₂'}
    for k, j in enumerate((3, 4, 5)):
        for (r, c) in dest[j]:
            cx, cy = MX + c * cw + cw / 2, MY + r * ch + ch / 2
            ts = 4.4 + k * .6
            f.path(T(cx, cy + 5, '%.1f' % (sums[j - 3] / 7), FI if j != 4 else VI, mono=True, bold=True),
                   [(0, t.cx(j) - cx, yb + 20 - cy - 5), (ts, 0, 0)], ts - .3, d=.8)
        f.show(S(MX + 2 * cw + 40, MY + 30 + k * 22, names[j] + ' = %.1f' % (sums[j - 3] / 7), FI if j != 4 else VI), 4.4 + k * .6 + .8)
    f.show(S(MX - 30, MY + 2 * ch + 40, 'diagonal = spread of each column', MU) +
           S(MX - 30, MY + 2 * ch + 58, 'off-diagonal = how they move together', MU), 6.6)
    return finish(f, yb + 34)

# ---------- 4.2 Eigenvectors ----------
def fig_eigen():
    f = Anim('pca7-', 720, 0, 'The covariance matrix C applied to three directions drawn on the cloud. The flat direction (1, 0) '
             'comes out turned by 52 degrees. PC1, (0.59, 0.81), comes out along itself, 187.5 times longer. PC2, (−0.81, '
             '0.59), also comes out along itself, 3.9 times longer. Directions that only stretch are the eigenvectors, the '
             'stretch factors are the eigenvalues.', 'C TURNS MOST DIRECTIONS · EIGENVECTORS ONLY STRETCH')
    P = Plane(200, 170, 5.6)
    f.static(cross(P, (26, 24)))
    for i in range(N):
        f.static(pdot(P.X(HC[i]), P.Y(WC[i]), GH, 3.5))
    Lp = 20  # drawn length of a unit direction, in data units
    def arr(v, c, sw=2.4, k=1.0):
        return vec(P.ox, P.oy, P.X(Lp * k * v[0]), P.Y(Lp * k * v[1]), c, sw)
    cu = (CU[0] / math.hypot(*CU), CU[1] / math.hypot(*CU))
    X = 430
    # 1. (1,0) turns
    f.show(arr((1, 0), BR) + S(P.X(Lp) + 4, P.oy + 16, '(1, 0)', BR, 'start', True), .4, hide=3.0)
    f.show(arr(cu, RO, 2) + S(P.X(Lp * cu[0]) + 6, P.Y(Lp * cu[1]), 'C·(1, 0) turned', RO, 'start', True), 1.2, hide=3.0)
    f.show(M(X, 60, '{C}·(1, 0) = (67.7, 87.4)', RO, 'start') + S(X, 80, 'points 52° away: not an eigenvector', MU), 1.4)
    # 2. v1
    f.show(arr(V1, FI, 3) + S(P.X(Lp * V1[0]) + 6, P.Y(Lp * V1[1]) - 4, 'PC1', FI, 'start', True), 3.2)
    f.show(M(X, 120, '{C}·{v}₁ = (110.5, 151.5)', FI, 'start'), 3.8)
    f.show(M(X, 144, '= 187.5 × (0.59, 0.81)', FI, 'start') + S(X, 164, 'same direction: λ₁ = 187.5', FI, 'start', True), 4.4)
    # 3. v2
    f.show(arr(V2, VI, 3, .55) + S(P.X(Lp * .55 * V2[0]) - 6, P.Y(Lp * .55 * V2[1]) - 6, 'PC2', VI, 'end', True), 5.2)
    f.show(M(X, 204, '{C}·{v}₂ = 3.9 × (−0.81, 0.59)', VI, 'start') + S(X, 224, 'same direction: λ₂ = 3.9', VI, 'start', True), 5.8)
    f.show(S(X, 256, 'eigenvectors = the axes · eigenvalues = their variance', MU, 'start', True), 6.6)
    return finish(f, P.Y(-24) + 12)

# ---------- 5.1 Explained variance ratio ----------
def fig_evr():
    f = Anim('pca8-', 720, 0, 'The z1 and z2 columns of the eight people. Their variances are computed under the table: 187.5 and 3.9. '
             'Both numbers travel into one bar of total variance 191.4: PC1 fills 98.0 percent of it, PC2 the remaining 2.0 '
             'percent.', 'VARIANCE OF EACH NEW COLUMN ÷ TOTAL VARIANCE')
    t = Table(0, 30, [('id', 26), ('z₁', 56, 'on PC1'), ('z₂', 56, 'on PC2')])
    f.static(t.head())
    for i, n in enumerate(IDS):
        f.static(t.row(i, [n, fm(Z1[i]), fm(Z2[i])], colors={1: FI, 2: VI}))
    yb = t.bottom(N) + 22
    f.show(T(t.cx(0), yb, 'var', MU) + T(t.cx(1), yb, '%.1f' % L1, FI, mono=True, bold=True) +
           T(t.cx(2), yb, '%.1f' % L2, VI, mono=True, bold=True), .6)
    f.show(t.colbox(1, N, FI) , .4, hide=1.4); f.show(t.colbox(2, N, VI), .4, hide=1.4)
    BX, BY, BW = 220, 120, 460; tot = L1 + L2
    f.static(R(BX, BY, BW, 30, SUNK, RULE_HI, 4) + S(BX, BY + 50, 'total variance %.1f = λ₁ + λ₂' % tot, MU))
    w1 = BW * L1 / tot; w2 = BW * L2 / tot
    f.path(T(BX + w1 / 2, BY - 34, '%.1f' % L1, FI, mono=True, bold=True), [(0, t.cx(1) - BX - w1 / 2, yb - BY + 34), (1.6, 0, 0)], 1.3, d=.8)
    f.show(R(BX, BY, w1, 30, tn(FI, '.30'), FI, 4, 1.4) + T(BX + w1 / 2, BY + 20, 'PC1 %.1f%%' % (100 * L1 / tot), FI, bold=True), 2.4)
    f.path(T(BX + BW - 4, BY - 34, '%.1f' % L2, VI, mono=True, bold=True, a='end'), [(0, t.cx(2) - BX - BW + 4, yb - BY + 34), (3.0, 0, 0)], 2.7, d=.8)
    f.show(R(BX + w1, BY, w2, 30, tn(VI, '.45'), VI, 2, 1.4) + T(BX + BW, BY + 50, 'PC2 %.1f%%' % (100 * L2 / tot), VI, 'end', bold=True), 3.8)
    f.show(S(BX, BY + 86, 'keep z₁ alone: 98% of the spread survives', FI, 'start', True), 4.4)
    return finish(f, yb + 14)

# ---------- 5.2 Scree & cumulative ----------
def fig_scree():
    f = Anim('pca9-', 720, 0, 'A wider table: 40 rows, 6 standardised columns. Its six eigenvalues, 4.61 down to 0.04, are dropped one '
             'at a time into a bar chart as shares of the total 6: 77, 15, 5, 2, 1 and 1 percent. A cumulative line climbs '
             'above the bars: 77, 91, 97 percent. A dashed line at 95 percent is first crossed at the third component, so '
             'three components are kept.', 'ONE BAR PER COMPONENT · STOP WHEN THE RUNNING TOTAL PASSES 95%')
    GX, GY, GW, GH_ = 70, 70, 520, 200
    bw, gap = 60, 12
    bx = lambda k: GX + 20 + k * (bw + gap)
    gy = lambda v: GY + GH_ - v * GH_
    f.static(L(GX, gy(0), GX + GW, gy(0), MU, 1.2) + L(GX, gy(0), GX, GY - 8, MU, 1.2))
    for v in (0, .25, .5, .75, 1):
        f.static(T(GX - 7, gy(v) + 4, '%d%%' % (100 * v), FA, 'end', mono=True) + (L(GX, gy(v), GX + GW, gy(v), RULE, 1, '2 4') if v else ''))
    f.static(S(GX, GY - 20, 'share of total variance', MU))
    # eigenvalue chips along the top-right
    for k in range(6):
        x = bx(k) + bw / 2
        f.static(T(x, gy(0) + 16, 'PC%d' % (k + 1), MU, mono=True, bold=True))
    prev = None
    for k in range(6):
        ts = .6 + k * .9; x = bx(k)
        f.show(T(x + bw / 2, gy(0) + 32, 'λ %.2f' % EIG6[k], BR, mono=True), ts)
        f.show(R(x, gy(R6[k]), bw, max(gy(0) - gy(R6[k]), 1.5), tn(BR, '.30'), BR, 2, 1.2), ts + .4)
        f.show(T(x + bw / 2, gy(0) + 48, '%.0f%%' % (100 * R6[k]), BR, mono=True, bold=True), ts + .4)
        cx, cy = x + bw / 2, gy(CUM6[k])
        if prev: f.show(L(prev[0], prev[1], cx, cy, FI, 2), ts + .9)
        f.show(pdot(cx, cy, FI, 4.5), ts + .9)
        if k < 3: f.show(T(cx - 10, cy - 10, '%.0f%%' % (100 * CUM6[k]), FI, 'end', mono=True, bold=True), ts + .9)
        prev = (cx, cy)
    TE = .6 + 6 * .9 + .4
    f.show(L(GX, gy(.95), GX + GW, gy(.95), RO, 1.4, '6 4') + T(GX + GW + 6, gy(.95) + 4, '95%', RO, 'start', mono=True, bold=True), TE)
    kx = bx(K95 - 1) + bw / 2
    f.show(ring(kx, gy(CUM6[K95 - 1]), 9, FI, 2) + L(kx, gy(CUM6[K95 - 1]) + 10, kx, gy(0), FI, 1.2, '3 3'), TE + .5)
    f.show(pill(kx + 120, gy(.62), 'keep k = %d · %.0f%%' % (K95, 100 * CUM6[K95 - 1]), 'bl', 150), TE + .8)
    f.show(S(GX + GW - 180, gy(.4), 'the bars after the elbow', MU) + S(GX + GW - 180, gy(.4) + 16, 'are mostly noise', MU), TE + 1.1)
    f.static(T(GX - 7, gy(0) + 32, 'λ', FA, 'end', mono=True) + T(GX - 7, gy(0) + 48, 'share', FA, 'end'))
    return finish(f, gy(0) + 58)

# ---------- 06 Reconstruction error ----------
def fig_recon():
    f = Anim('pca10-', 720, 0, 'Only z1 is kept. Each value travels from the origin out along PC1 to the point z1 times v1: the '
             'reconstructed person. A red segment joins it to the real point; its squared length fills the column e '
             'squared. The segments are exactly the z2 values, so the mean squared error, 27.4 divided by 7, is 3.9 — '
             'the variance of the dropped PC2.', 'GO BACK FROM z₁ TO 2-D · WHAT IS MISSING IS THE ERROR')
    t = Table(0, 30, [('id', 26), ('z₁', 52, 'kept'), ('x̂', 82, 'z₁ · v₁'), ('e²', 46, 'error')])
    f.static(t.head())
    for i, n in enumerate(IDS):
        f.static(t.row(i, [n, fm(Z1[i]), '', ''], colors={1: FI}))
    P = Plane(500, 168, 6.2)
    f.static(cross(P, (25, 21)) + axis_line(P, V1, 27, FI, 2) + S(P.X(27 * V1[0]) + 6, P.Y(27 * V1[1]) + 4, 'PC1', FI, 'start', True))
    for i in range(N):
        f.static(pdot(P.X(HC[i]), P.Y(WC[i]), BR, 4.5))
    for i in range(N):
        ts = .6 + i * .55
        rx, ry = P.X(REC[i][0]), P.Y(REC[i][1])
        f.show(t.outline(i, c=VI), ts, hide=ts + .55)
        f.path(pdot(rx, ry, FI, 3.8), [(0, P.ox - rx, P.oy - ry), (ts + .1, 0, 0)], ts, d=.4)
        f.show(t.cell(i, 2, '(%s, %s)' % (fm(REC[i][0]), fm(REC[i][1])), c=FI), ts + .3)
        f.show(L(rx, ry, P.X(HC[i]), P.Y(WC[i]), RO, 1.8), ts + .45)
        f.show(t.cell(i, 3, '%.1f' % (Z2[i] ** 2), c=RO), ts + .5)
    yb = t.bottom(N) + 22; TE = .6 + N * .55 + .2
    tot = sum(z * z for z in Z2); assert round(tot, 1) == 27.4
    f.show(T(t.cx(2), yb, 'mean = %.1f ÷ 7' % tot, MU) + T(t.cx(3), yb, '%.1f' % ERR, RO, mono=True, bold=True), TE)
    f.show(S(P.X(-25), P.Y(-21) + 22, 'error %.1f = λ₂, the variance PC2 held' % ERR, RO, 'start', True), TE + .4)
    return finish(f, max(yb + 14, P.Y(-21) + 30))

# ---------- 7.x Units ----------
def fig_units(kind):
    mm = kind == 'mm'
    pre = 'pca11-' if mm else 'pca12-'
    if mm:
        A = [(h, w) for h, w in zip(HC, WC)]; B = [(h * 10, w) for h, w in zip(HC, WC)]
        sa, sb = 2.4, 2.4; va, vb = V1, LMM[2]; ta, tb_ = TH, TH_MM
        aria = ('The centred cloud drawn at true scale, PC1 tilted 53.9 degrees. Height is then written in millimetres: every '
                'point glides sideways to ten times its distance, the cloud lies almost flat and PC1 turns to 7.4 degrees, '
                'loadings 0.99 on height and 0.13 on weight. Nothing about the people changed, only the unit.')
        cap = 'SAME PEOPLE · HEIGHT IN mm · PC1 TURNS TO HEIGHT'
        rows = (('var x₁', '67.7 cm²', '6771 mm²'), ('var x₂', '123.7 kg²', '123.7 kg²'))
        load = ('PC1 = (0.59, 0.81)', 'PC1 = (0.99, 0.13)'); note = 'PC1 now just copies the column with the biggest numbers'
    else:
        A = [(h * 10, w) for h, w in zip(HC, WC)]; B = list(zip(ZH, ZW))
        sa, sb = 2.4, 62; va, vb = LMM[2], LZ[2]; ta, tb_ = TH_MM, 45.0
        aria = ('The flat millimetre cloud with PC1 at 7.4 degrees. Each column is divided by its standard deviation: the '
                'points glide into a cloud where both axes have variance 1, and PC1 turns to 45 degrees, loadings 0.71 and '
                '0.71. The answer no longer depends on the units.')
        cap = 'DIVIDE EACH COLUMN BY ITS STD · BOTH COUNT EQUALLY'
        rows = (('var x₁', '6771 mm²', '1'), ('var x₂', '123.7 kg²', '1'))
        load = ('PC1 = (0.99, 0.13)', 'PC1 = (0.71, 0.71)'); note = 'the same result whatever unit each column was in'
    f = Anim(pre, 720, 0, aria, cap)
    ox, oy = 360, 140
    f.static(L(70, oy, 650, oy, RULE_HI, 1.2) + L(ox, 30, ox, 250, RULE_HI, 1.2) + M(656, oy + 5, '{x}₁', MU, 'start') + M(ox, 24, '{x}₂', MU))
    def line(v, s, c, sw, dash=None):
        r = 300 / s
        dx, dy = v[0] * min(r, 105 / s / max(abs(v[1]), 1e-6)), v[1] * min(r, 105 / s / max(abs(v[1]), 1e-6))
        return L(ox - dx * s, oy + dy * s, ox + dx * s, oy - dy * s, c, sw, dash)
    f.show(line(va, sa, FI, 2, '6 4'), .1, hide=1.4)
    for (a, b) in zip(A, B):
        x, y = ox + b[0] * sb, oy - b[1] * sb
        f.path(pdot(x, y, BR, 4.5), [(0, ox + a[0] * sa - x, oy - a[1] * sa - y), (1.4, 0, 0)], .2, d=1.4)
    f.show(line(vb, sb, FI, 2.6), 3.0)
    lx = 470; ly = 220
    f.show(S(lx, ly, load[0], MU, bold=True), .2, hide=2.8)
    f.show(S(lx, ly, load[1], FI, bold=True) + S(lx, ly + 18, '%.1f°' % tb_, FI), 3.2)
    TX0 = 0
    for k, (nm, a, b) in enumerate(rows):
        y = 220 + k * 20
        f.static(T(TX0, y, nm, MU, 'start', mono=True))
        f.show(T(TX0 + 60, y, a, MU, 'start', mono=True), .2, hide=1.2)
        f.show(T(TX0 + 60, y, b, RO if (mm and k == 0) else (FI if not mm else MU), 'start', mono=True, bold=True), 1.4)
    f.show(S(TX0, 270, note, FI if not mm else RO, 'start', True), 3.6)
    return finish(f, 282)

# ---------- 08 Not feature selection ----------
def fig_loadings():
    f = Anim('pca13-', 720, 0, 'Left, feature selection on the two columns: x1 is struck out and x2 is kept, unchanged. Right, PCA: '
             'row A\'s height −12 is multiplied by the loading 0.59 and its weight −12 by 0.81; the two products travel '
             'into one cell and add up to z1 = −16.8. The other rows fill the same way. Every z1 value mixes both columns.',
             'SELECTION KEEPS A COLUMN · PCA MIXES ALL OF THEM')
    f.static(S(0, 40, 'feature selection', MU, bold=True))
    tl = Table(0, 48, [('id', 26), ('x₁', 54, 'height'), ('x₂', 54, 'weight')])
    f.static(tl.head())
    for i, n in enumerate(IDS):
        f.static(tl.row(i, [n, fm(HC[i], 0), fm(WC[i], 0)]))
    f.show(tl.dimcol(1, N), .5)
    f.show(tl.colbox(2, N, FI), .8)
    f.show(T(tl.cx(2), tl.bottom(N) + 20, 'kept as is', FI, bold=True) + T(tl.cx(1), tl.bottom(N) + 20, 'dropped', RO, bold=True), 1.0)
    X0 = 250
    f.static(S(X0, 40, 'PCA', MU, bold=True))
    tr = Table(X0, 48, [('id', 26), ('x₁', 44, 'height'), ('x₂', 44, 'weight'), ('z₁', 56, 'PC1')])
    f.static(tr.head())
    for i, n in enumerate(IDS):
        f.static(tr.row(i, [n, fm(HC[i], 0), fm(WC[i], 0), '']))
    # loadings bars
    LX, LY = 520, 84
    f.show(S(LX, LY - 14, 'loadings of PC1', MU), 1.4)
    for k, (nm, v) in enumerate((('height', V1[0]), ('weight', V1[1]))):
        y = LY + k * 30
        f.show(S(LX, y + 13, nm, TX) + R(LX + 52, y, v * 120, 18, tn(FI, '.30'), FI, 3, 1.2) +
               T(LX + 58 + v * 120, y + 14, '%.2f' % v, FI, 'start', mono=True, bold=True), 1.6 + k * .3)
    # row A arithmetic
    ts = 2.6
    f.show(tr.outline(0, c=VI), ts, hide=ts + 2.4)
    py = LY + 110
    f.path(T(LX, py, '−12 × 0.59 = %s' % fm(HC[0] * V1[0], 2), VI, 'start', mono=True, bold=True),
           [(0, tr.cx(1) - LX - 40, tr.ry(0) + 17 - py), (ts + .3, 0, 0)], ts, d=.7)
    f.path(T(LX, py + 22, '−12 × 0.81 = %s' % fm(WC[0] * V1[1], 2), VI, 'start', mono=True, bold=True),
           [(0, tr.cx(2) - LX - 40, tr.ry(0) + 17 - py - 22), (ts + .7, 0, 0)], ts + .4, d=.7)
    f.show(L(LX, py + 32, LX + 150, py + 32, VI, 1) + T(LX, py + 50, 'z₁ = %s' % fm(Z1[0]), FI, 'start', mono=True, bold=True), ts + 1.4)
    f.show(tr.cell(0, 3, fm(Z1[0]), c=FI), ts + 1.9)
    for i in range(1, N):
        f.show(tr.cell(i, 3, fm(Z1[i]), c=FI), ts + 2.4 + i * .12)
    f.show(tr.colbox(3, N, FI), ts + 3.4)
    f.show(T(tr.cx(3), tr.bottom(N) + 20, 'a mix of both', FI, bold=True), ts + 3.4)
    assert (round(HC[0] * V1[0], 2), round(WC[0] * V1[1], 2)) == (-7.07, -9.69) and abs(HC[0] * V1[0] + WC[0] * V1[1] - Z1[0]) < 1e-9
    return finish(f, tr.bottom(N) + 30)

def eqline(*terms):
    return '    <div class="line">\n' + '\n'.join('      ' + t for t in terms) + '\n    </div>'

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Dimensionality reduction</p>
  <h1>PCA &amp; dimensionality <em>reduction</em></h1>
  <p class="lede">PCA turns the axes toward the directions the data spreads most, then drops the thin directions, so a few new columns carry almost everything the old ones said.</p>
</header>

<section id="pca-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Turn the axes until the first one lies along the <em>widest spread</em>; keep the first few new columns.</p>
{p1}
  <ul class="why">
    <li>Eight people, height <span class="mth"><var>x</var><sub>1</sub></span> and weight <span class="mth"><var>x</var><sub>2</sub></span>: two columns that mostly say one thing, "how big".</li>
    <li>The new columns <span class="mth"><var>z</var><sub>1</sub>, <var>z</var><sub>2</sub></span> are the <b>principal components</b>; together they lose nothing, <span class="mth"><var>z</var><sub>1</sub></span> alone loses 2%.</li>
    <li>No labels are used: PCA is unsupervised, it only looks at how the columns spread.</li>
  </ul>
</section>

<section id="pca-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Centring</h2></div>
  <p class="key">Subtract each column's mean first, so every direction is measured <em>from the middle of the cloud</em>.</p>
{p2}
  <ul class="why">
    <li>The axes PCA finds pass through the origin; without centring PC1 would point at the mean instead of along the spread.</li>
    <li>scikit-learn's <code>PCA</code> centres for you; it does <b>not</b> scale (see <a href="#pca-s7">Standardising</a>).</li>
  </ul>
</section>

<section id="pca-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Principal components</h2></div>
  <p class="key">Each component is a direction; each row's new value is <em>where it lands</em> on that direction.</p>
  <div class="subsec" id="pca-s3-1">
    <h3 class="ssh"><b>3.1</b>Direction of most spread</h3>
    <p class="skey">PC1 is the line whose shadows of the points are <em>spread out the most</em>.</p>
{p3}
    <ul class="why">
      <li>Spread is measured as the variance of the feet on the line; at 0° it is just var <span class="mth"><var>x</var><sub>1</sub></span>, at 90° var <span class="mth"><var>x</var><sub>2</sub></span>.</li>
      <li>Most spread is the same line as <b>smallest perpendicular distance</b> to the points — two views of one answer.</li>
    </ul>
  </div>
  <div class="subsec" id="pca-s3-2">
    <h3 class="ssh"><b>3.2</b>Projection</h3>
    <p class="skey">Drop every point onto PC1 at a right angle; its position along the line is its <em>score</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>z</var><sub>1</sub></span><em>score of a row</em></span>
      <span class="op">=</span>
      <span class="t"><span><var>v</var><sub>1</sub> · <var>x</var></span><em>dot product with the unit direction</em></span>
      <span class="op">=</span>
      <span class="t b"><span>0.59 <var>x</var><sub>1</sub> + 0.81 <var>x</var><sub>2</sub></span><em>for these eight people</em></span>
    </div>
  </div>
{p4}
    <ul class="why">
      <li>Two columns in, one column out: <code>fit_transform</code> returns exactly this <span class="mth"><var>z</var><sub>1</sub></span> column.</li>
      <li>New rows use the same <span class="mth"><var>v</var><sub>1</sub></span> and the training mean: fit on the training set only, or the test set leaks in.</li>
    </ul>
  </div>
  <div class="subsec" id="pca-s3-3">
    <h3 class="ssh"><b>3.3</b>Second component</h3>
    <p class="skey">PC2 is the widest direction <em>at a right angle</em> to PC1, and so on for PC3, PC4…</p>
{p5}
    <ul class="why">
      <li>With <span class="mth"><var>d</var></span> columns there are <span class="mth"><var>d</var></span> components, each perpendicular to all before it.</li>
      <li>The scores of different components are <b>uncorrelated</b>: what one says, no other repeats.</li>
    </ul>
  </div>
</section>

<section id="pca-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Covariance &amp; eigenvectors</h2></div>
  <p class="key">The scan in 3.1 is not needed: the components fall straight out of <em>one small matrix</em>.</p>
  <div class="subsec" id="pca-s4-1">
    <h3 class="ssh"><b>4.1</b>Covariance matrix</h3>
    <p class="skey">A <span class="mth"><var>d</var> × <var>d</var></span> table of how every pair of centred columns <em>moves together</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>C</var></span><em>covariance matrix</em></span>
      <span class="op">=</span>
      <span class="t"><span><span class="frac"><i>1</i><i><var>n</var> − 1</i></span> <var>X</var><sup>T</sup><var>X</var></span><em>X centred, n rows</em></span>
      <span class="op">=</span>
      <span class="t b"><span>[ 67.7 &nbsp;87.4 ; &nbsp;87.4 &nbsp;123.7 ]</span><em>height, weight</em></span>
    </div>
  </div>
{p6}
    <ul class="why">
      <li>Diagonal: the variance of each column. Off-diagonal: the covariance; large and positive here because tall people weigh more.</li>
      <li>Symmetric, so its eigenvectors are perpendicular — that is why the components are.</li>
    </ul>
  </div>
  <div class="subsec" id="pca-s4-2">
    <h3 class="ssh"><b>4.2</b>Eigenvectors</h3>
    <p class="skey">The directions <span class="mth"><var>C</var></span> only stretches are the components; the stretch is their <em>variance</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>C</var> <var>v</var><sub><var>k</var></sub></span><em>matrix times direction</em></span>
      <span class="op">=</span>
      <span class="t g"><span><var>λ</var><sub><var>k</var></sub> <var>v</var><sub><var>k</var></sub></span><em>same direction, stretched</em></span>
      <span class="op">,</span>
      <span class="t"><span><var>λ</var><sub>1</sub> = 187.5, &nbsp;<var>λ</var><sub>2</sub> = 3.9</span><em>sorted largest first</em></span>
    </div>
  </div>
{p7}
    <ul class="why">
      <li><span class="mth"><var>λ</var><sub>1</sub></span> is exactly the peak of the curve in 3.1; <span class="mth"><var>v</var><sub>1</sub> = (0.59, 0.81)</span> is the line at 53.9°.</li>
      <li>In practice it is computed by <b>SVD</b> of the centred table, <span class="mth"><var>X</var> = <var>U</var><var>Σ</var><var>V</var><sup>T</sup></span>: the rows of <span class="mth"><var>V</var><sup>T</sup></span> are the components, without ever forming <span class="mth"><var>C</var></span>.</li>
    </ul>
  </div>
</section>

<section id="pca-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Number of components</h2></div>
  <p class="key">Each eigenvalue is the variance one component carries; keep components until <em>enough of the total</em> is kept.</p>
  <div class="subsec" id="pca-s5-1">
    <h3 class="ssh"><b>5.1</b>Explained variance ratio</h3>
    <p class="skey">A component's share is its eigenvalue over the <em>sum of all eigenvalues</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">ratio</b><sub><var>k</var></sub></span><em>share of component k</em></span>
      <span class="op">=</span>
      <span class="t"><span><span class="frac"><i><var>λ</var><sub><var>k</var></sub></i><i>Σ<sub><var>j</var></sub> <var>λ</var><sub><var>j</var></sub></i></span></span><em>total = sum of column variances</em></span>
      <span class="op">=</span>
      <span class="t g"><span><span class="frac"><i>187.5</i><i>191.4</i></span> = 98.0%</span><em>PC1 here</em></span>
    </div>
  </div>
{p8}
    <ul class="why">
      <li>The eigenvalues add up to the total variance of the original columns: nothing is created or lost by turning the axes.</li>
      <li>scikit-learn: <code>explained_variance_ratio_</code>.</li>
    </ul>
  </div>
  <div class="subsec" id="pca-s5-2">
    <h3 class="ssh"><b>5.2</b>Scree &amp; cumulative curve</h3>
    <p class="skey">Plot the shares largest first; keep the <em>smallest k</em> whose running total passes 95%.</p>
{p9}
    <ul class="why">
      <li><code>PCA(n_components=0.95)</code> applies this rule; 90–99% are all common, the right one depends on what comes next.</li>
      <li>The <b>elbow</b> of the scree plot, where bars stop shrinking fast, is the eyeball version of the same choice.</li>
      <li>For plotting, keep 2 or 3 whatever they explain.</li>
    </ul>
  </div>
</section>

<section id="pca-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Reconstruction error</h2></div>
  <p class="key">Map the kept scores back to the original columns; the gap to the real rows is <em>exactly the dropped variance</em>.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>x̂</var></span><em>reconstructed row</em></span>
      <span class="op">=</span>
      <span class="t"><span><var>μ</var> + Σ<sub><var>k</var> ≤ <var>K</var></sub> <var>z</var><sub><var>k</var></sub> <var>v</var><sub><var>k</var></sub></span><em>mean + kept components</em></span>
      <span class="op">,</span>
      <span class="t r"><span><span class="frac"><i>1</i><i><var>n</var> − 1</i></span> Σ<sub><var>i</var></sub> ‖<var>x</var><sub><var>i</var></sub> − <var>x̂</var><sub><var>i</var></sub>‖<sup>2</sup> = Σ<sub><var>k</var> &gt; <var>K</var></sub> <var>λ</var><sub><var>k</var></sub></span><em>error = dropped eigenvalues</em></span>
    </div>
  </div>
{p10}
  <ul class="why">
    <li>PCA is the linear map that makes this error <b>smallest</b> for a given <span class="mth"><var>K</var></span> — the loss it minimises.</li>
    <li><code>inverse_transform</code> does the trip back; a large error on one row flags it as unusual (a simple anomaly score).</li>
    <li>Dropping components helps a model only when what is dropped is mostly noise; nothing guarantees that.</li>
  </ul>
</section>

<section id="pca-s7" class="lesson">
  <div class="sh"><b>07</b><h2>Standardising</h2></div>
  <p class="key">Variance depends on units, so PCA does too: <em>put every column on one scale</em> first.</p>
  <div class="subsec" id="pca-s7-1">
    <h3 class="ssh"><b>7.1</b>Mixed units</h3>
    <p class="skey">Write height in millimetres and its variance grows 100 times; PC1 <em>turns onto height</em>.</p>
{p11}
    <ul class="why">
      <li>The people did not change, only a unit: PCA is answering "which column has the biggest numbers".</li>
      <li>The most common PCA mistake, and a silent one: it still runs and still prints 99% explained.</li>
    </ul>
  </div>
  <div class="subsec" id="pca-s7-2">
    <h3 class="ssh"><b>7.2</b>Standardised</h3>
    <p class="skey">Divide each centred column by its standard deviation; every column has variance 1 and <em>counts equally</em>.</p>
{p12}
    <ul class="why">
      <li>Same as PCA on the <b>correlation</b> matrix: here <span class="mth"><var>r</var> = 0.96</span>, so PC1 keeps 98% (λ = 1.96 of 2).</li>
      <li><code>StandardScaler</code> then <code>PCA</code> in one <code>Pipeline</code>, fitted on the training rows only.</li>
    </ul>
  </div>
</section>

<section id="pca-s8" class="lesson">
  <div class="sh"><b>08</b><h2>PCA is not feature selection</h2></div>
  <p class="key">Feature selection keeps some original columns; every PCA column is <em>a weighted mix of all of them</em>.</p>
{p13}
  <ul class="why">
    <li>The weights, the <b>loadings</b> (<code>components_</code>), say how much each column feeds a component; a name like "size" for PC1 is a guess, not a fact.</li>
    <li>Every original column must still be measured to compute <span class="mth"><var>z</var><sub>1</sub></span>, and tree models gain little from it — use selection when column names must survive.</li>
    <li>PCA only finds straight directions; <b>t-SNE</b> and <b>UMAP</b> unfold curved structure into a 2-D picture, for looking only — their axes and distances mean nothing for a model.</li>
  </ul>
</section>

<script>
/* Figures start when first scrolled into view, play once and hold their final state. Click a figure to replay. */
(function () {
  if (!window.IntersectionObserver || !document.getAnimations) return;
  var svgs = [].slice.call(document.querySelectorAll("figure svg[data-anim]"));
  if (!svgs.length) return;
  function anims(s) {
    return document.getAnimations().filter(function (a) { var t = a.effect && a.effect.target; return t && s.contains(t); });
  }
  function restart(s) { anims(s).forEach(function (a) { a.currentTime = 0; a.play(); }); }
  svgs.forEach(function (s) { anims(s).forEach(function (a) { a.pause(); a.currentTime = 0; }); });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting || e.target.__played) return;
      e.target.__played = true; restart(e.target); io.unobserve(e.target);
    });
  }, { threshold: 0.4 });
  svgs.forEach(function (s) {
    io.observe(s); s.style.cursor = "pointer";
    s.addEventListener("click", function () { restart(s); });
  });
})();
</script>

<footer>Machine learning · Dimensionality reduction · math background in <a href="../../02-math-foundations/linear-algebra/index.html">Linear algebra</a>; often comes one step before <a href="../../07-clustering/clustering-overview/index.html">Clustering</a>.</footer>
'''

assert round(LZ[0] / 2, 2) == .98

def build():
    figs = dict(p1=fig_mental(), p2=fig_centre(), p3=fig_spread(), p4=fig_project(), p5=fig_pc2(), p6=fig_cov(),
                p7=fig_eigen(), p8=fig_evr(), p9=fig_scree(), p10=fig_recon(), p11=fig_units('mm'), p12=fig_units('z'),
                p13=fig_loadings())
    return re.sub(r'\{(p\d+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'Centre the table, turn the axes toward the widest spread, drop each row onto them: covariance '
           'eigenvectors, explained variance and the 95% rule, reconstruction error, and why columns must be standardised.')
