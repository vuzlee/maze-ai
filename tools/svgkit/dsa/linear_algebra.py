# -*- coding: utf-8 -*-
"""Figures + page body for content/07-machine-learning/02-math-foundations/linear-algebra.
Run: python3 linear_algebra.py  -> rewrites the lesson body between <header class="hero"> and the replay script.
Also exports the small plotting helpers used by calculus.py."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from engine import Anim
from tablefig import T, R, L, arrow, MU, TX, FA, RULE_HI, Table

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/02-math-foundations/linear-algebra/index.html')

BR, VI, FI, RO, GH = 'var(--brand)', 'var(--violet)', 'var(--filled)', 'var(--rose)', 'var(--ghost)'
RULE, SUNK, BG = 'var(--rule)', 'var(--sunk)', 'var(--bg)'
RGBA = {BR: '--clay-a', VI: '--violet-a', FI: '--blue-a', RO: '--rose-a'}

def tn(c, a='.14'):
    return 'rgba(var(%s),%s)' % (RGBA[c], a)

def M(x, y, s, c=TX, a='middle'):
    """Math text in SVG: variables written as {v} -> italic tspan."""
    s = re.sub(r'\{([^}]*)\}', r'<tspan class="v">\1</tspan>', s)
    return '<text class="sv-m" x="%.1f" y="%.1f" style="fill:%s" text-anchor="%s">%s</text>' % (x, y, c, a, s)

def S(x, y, s, c=MU, a='start', bold=False):
    return T(x, y, s, c, a, 'sv-s', bold=bold)

def chip(cx, cy, s, c=VI, w=None, mono=True):
    w = w or 16 + len(s) * 7.2
    return (R(cx - w / 2, cy - 11, w, 22, BG, 'none', 11) + R(cx - w / 2, cy - 11, w, 22, tn(c, '.14'), c, 11, 1.3) +
            T(cx, cy + 4.5, s, c, mono=mono, bold=True))

def dot(x, y, c=BR, r=4.5, stroke=None):
    st = ' stroke="%s" stroke-width="1.5"' % stroke if stroke else ''
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"%s/>' % (x, y, r, c, st)

def ball(x, y, c=VI, r=8):
    return dot(x, y, c, r, BG)

def vec(x1, y1, x2, y2, c=BR, sw=2.2):
    return arrow(x1, y1, x2, y2, c, sw, None, 9)

def poly(pts, c=BR, sw=2.4, dash=None, fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<path d="M%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"%s/>' % (
        ' L'.join('%.1f %.1f' % p for p in pts), fill, c, sw, d)

class Plane:
    """Cartesian plane: data (x, y) -> svg px."""
    def __init__(self, ox, oy, sx, sy=None):
        self.ox, self.oy, self.sx, self.sy = ox, oy, sx, sy if sy is not None else sx
    def __call__(self, x, y):
        return (self.ox + x * self.sx, self.oy - y * self.sy)
    def X(self, x): return self.ox + x * self.sx
    def Y(self, y): return self.oy - y * self.sy
    def grid(self, x0, x1, y0, y1, step=1, labels=True, xl=None, yl=None):
        s = ''
        k = x0
        while k <= x1 + 1e-9:
            s += L(self.X(k), self.Y(y0), self.X(k), self.Y(y1), RULE, 1)
            k += step
        k = y0
        while k <= y1 + 1e-9:
            s += L(self.X(x0), self.Y(k), self.X(x1), self.Y(k), RULE, 1)
            k += step
        if x0 <= 0 <= x1: s += L(self.X(0), self.Y(y0), self.X(0), self.Y(y1), RULE_HI, 1.3)
        if y0 <= 0 <= y1: s += L(self.X(x0), self.Y(0), self.X(x1), self.Y(0), RULE_HI, 1.3)
        if labels:
            k = x0
            while k <= x1 + 1e-9:
                if k != 0: s += T(self.X(k), self.Y(min(max(0, y0), y1)) + 15, '%g' % k, FA, cls='sv-d')
                k += step
            k = y0
            while k <= y1 + 1e-9:
                if k != 0: s += T(self.X(min(max(0, x0), x1)) - 7, self.Y(k) + 4, '%g' % k, FA, 'end', 'sv-d')
                k += step
        if xl: s += M(self.X(x1) + 8, self.Y(max(0, y0)) + 5, xl, MU, 'start')
        if yl: s += M(self.X(max(0, x0)), self.Y(y1) - 8, yl, MU)
        return s

def mcell(x, y, v, w=34, h=28, c=None, fill=None):
    """matrix cell"""
    return (R(x, y, w, h, fill or BG, c or RULE_HI, 4, 1.5 if c else 1) +
            T(x + w / 2, y + h / 2 + 5, str(v), c or TX, mono=True, bold=bool(c)))

def matrix(x, y, A, w=34, h=28, name=None, c=None):
    s = ''
    for i, row in enumerate(A):
        for j, v in enumerate(row):
            s += mcell(x + j * w, y + i * h, v, w, h)
    if name: s += M(x + len(A[0]) * w / 2, y - 9, name, c or MU)
    return s

def finish(f, h):
    f.h = h
    return f.render()

# ---------- 1. Mental model ----------
def fig_mental():
    rows = [('A', 3, 1), ('B', 1, 2), ('C', 2, 3)]
    f = Anim('la1-', 720, 0, 'A table with three rows A, B, C and two feature columns. Each row in turn is outlined, its two '
             'numbers fly to the plane and an arrow is drawn from the origin to that point. The whole table is the '
             'matrix X with 3 rows and 2 columns.', 'ONE ROW = ONE ARROW · THE WHOLE TABLE = ONE MATRIX')
    t = Table(0, 44, [('row', 50), ('x₁', 64, 'visits'), ('x₂', 64, 'spend')])
    f.show(t.head(), .1)
    for i, r in enumerate(rows):
        f.show(t.row(i, [r[0], str(r[1]), str(r[2])]), .3 + i * .15)
    P = Plane(330, 260, 52)
    f.show(P.grid(0, 4, 0, 4, xl='{x}₁', yl='{x}₂'), .6)
    for i, (n, a, b) in enumerate(rows):
        t0 = 1.4 + i * 1.8
        f.show(t.outline(i, c=VI), t0, hide=t0 + 1.6)
        tx, ty = P(a, b)
        sx, sy = t.x + t.w + 40, t.ry(i) + 13
        f.path(chip(tx + 34, ty - 14, '(%d, %d)' % (a, b), VI), [(0, sx - tx - 34, sy - ty + 14), (t0 + .5, 0, 0)], t0 + .2, d=.7, hide=t0 + 1.7)
        f.show(vec(P.ox, P.oy, tx, ty, VI, 2.4), t0 + 1.2, hide=t0 + 1.7)
        f.show(vec(P.ox, P.oy, tx, ty, BR, 2.2) + dot(tx, ty, BR, 3.5) + T(tx + 10, ty - 6, n, BR, 'start', bold=True), t0 + 1.7)
    te = 1.4 + 3 * 1.8
    yb = t.bottom(3)
    f.show(R(-2, t.ry(0) - 4, t.w + 4, yb - t.ry(0) + 8, 'none', FI, 6, 1.8) +
           M(0, yb + 26, '{X} · 3 × 2', FI, 'start') + S(0, yb + 46, '3 rows (samples) × 2 columns (features)', MU), te)
    f.show(S(330, 296, '3 samples = 3 arrows in a 2-D space · d features → d-D space', FI, 'start', True), te + .5)
    return finish(f, 312)

# ---------- 2.1 Length ----------
def fig_norm():
    f = Anim('la2-', 720, 0, 'The vector a = (3, 4). Its horizontal part, 3, is drawn, then its vertical part, 4, then the '
             'arrow itself as the hypotenuse: length 5, since 3 squared plus 4 squared is 25.', 'LENGTH = PYTHAGORAS ON THE COMPONENTS')
    P = Plane(80, 270, 50)
    f.static(P.grid(0, 5, 0, 4.6, labels=True, xl='{x}₁', yl='{x}₂'))
    a = (3, 4)
    ex, ey = P(*a)
    f.show(L(P.ox, P.oy, ex, P.oy, VI, 3) + M((P.ox + ex) / 2, P.oy + 34, '{a}₁ = 3', VI), .5)
    f.show(L(ex, P.oy, ex, ey, VI, 3) + M(ex + 12, (P.oy + ey) / 2 + 4, '{a}₂ = 4', VI, 'start'), 1.4)
    f.show(vec(P.ox, P.oy, ex, ey, BR, 2.6) + M(ex - 6, ey - 10, '{a}', BR), 2.3)
    n = math.hypot(*a)
    assert n == 5
    X = 430
    f.show(M(X, 110, '3² + 4² = 9 + 16 = 25', TX, 'start'), 3.2)
    f.show(M(X, 140, '√25 = 5', TX, 'start'), 3.9)
    f.show(chip(X + 60, 180, '‖a‖ = 5', FI, 110, False), 4.6)
    f.show(L(P.ox, P.oy, ex, ey, FI, 4).replace('/>', ' stroke-linecap="round"/>'), 4.6)
    f.show(S(X, 222, 'same rule in 784-D: square, add, root', MU), 5.2)
    return finish(f, 300)

# ---------- 2.2 Dot product ----------
def fig_dot():
    a, b = (3, 1), (2, 3)
    dp = a[0] * b[0] + a[1] * b[1]
    assert dp == 9
    f = Anim('la3-', 720, 0, 'Vectors a = (3, 1) and b = (2, 3). Pair by pair: 3 times 2 is 6, 1 times 3 is 3; the sum is 9. '
             'On the plane, b casts a shadow onto a; the dot product is that shadow times the length of a.',
             'MULTIPLY PAIR BY PAIR, THEN ADD')
    t = Table(0, 44, [('', 40), ('a', 56), ('b', 56), ('a·b', 70)])
    f.show(t.head(), .1)
    for i in range(2):
        f.show(t.row(i, ['%d' % (i + 1), str(a[i]), str(b[i]), '']), .3)
    for i in range(2):
        t0 = 1.0 + i * 1.2
        f.show(t.outline(i, j0=1, j1=2, c=VI), t0, hide=t0 + 1.1)
        f.show(t.cell(i, 3, '%d × %d = %d' % (a[i], b[i], a[i] * b[i]), None, VI), t0 + .5)
    y = t.bottom(2) + 30
    f.show(L(t.colx(3), y - 20, t.colx(3) + 70, y - 20, RULE_HI) + chip(t.cx(3), y, 'sum = %d' % dp, FI, 86), 3.6)
    P = Plane(400, 250, 52)
    f.show(P.grid(0, 4, 0, 3.6, xl='{x}₁', yl='{x}₂'), .2)
    ax, ay = P(*a); bx, by = P(*b)
    f.show(vec(P.ox, P.oy, ax, ay, BR) + M(ax + 4, ay - 10, '{a}', BR, 'start'), .4)
    f.show(vec(P.ox, P.oy, bx, by, BR) + M(bx + 4, by - 8, '{b}', BR, 'start'), .6)
    # projection of b on a
    na = math.hypot(*a); k = dp / na ** 2
    qx, qy = P(a[0] * k, a[1] * k)
    f.show(L(bx, by, qx, qy, VI, 1.5, '4 3'), 4.4)
    f.show(L(P.ox, P.oy, qx, qy, VI, 5).replace('/>', ' stroke-linecap="round" opacity=".7"/>') +
           S(qx - 20, qy + 34, 'shadow of b on a = %.2f' % (dp / na), VI), 5.0)
    f.show(S(0, 214, 'a · b = shadow × ‖a‖ = %.2f × %.2f = %d' % (dp / na, na, dp), FI, 'start', True), 5.8)
    f.show(S(0, 236, 'positive: same side · 0: perpendicular · negative: opposite', MU), 6.3)
    return finish(f, 290)

# ---------- 2.3 Cosine ----------
def fig_cos():
    f = Anim('la4-', 720, 0, 'Vector a is fixed. Vector b, twice as long, turns around: at 0 degrees the cosine is 1, at 60 it '
             'is 0.5, at 90 it is 0, at 180 it is minus 1. A marker slides along a scale from 1 to minus 1; length never '
             'changes the value.', 'COSINE = DIRECTION ONLY · LENGTH IS DIVIDED OUT')
    P = Plane(190, 160, 50)
    f.static(P.grid(-3, 3, -2.6, 2.6, labels=False))
    base = 20
    ax, ay = P(1.6 * math.cos(math.radians(base)), 1.6 * math.sin(math.radians(base)))
    f.static(vec(P.ox, P.oy, ax, ay, BR, 2.6) + M(ax + 10, ay + 14, '{a}', BR, 'start'))
    # scale on the right
    SX0, SX1, SY = 460, 650, 120
    sc = lambda c: SX1 - (c + 1) / 2 * (SX1 - SX0)   # cos 1 on the left
    sc = lambda c: SX0 + (1 - c) / 2 * (SX1 - SX0)
    s = L(SX0, SY, SX1, SY, RULE_HI, 2)
    for c, lab in [(1, '1 · same'), (0, '0 · unrelated'), (-1, '−1 · opposite')]:
        s += L(sc(c), SY - 6, sc(c), SY + 6, RULE_HI, 1.5) + T(sc(c), SY + 24, lab, MU, cls='sv-d')
    f.static(S(SX0, 84, 'cos θ', MU) + s)
    angs = [0, 60, 90, 180]
    marks = []
    for k, d in enumerate(angs):
        t0 = .8 + k * 1.6
        th = math.radians(base + d)
        bx, by = P(2.4 * math.cos(th), 2.4 * math.sin(th))
        last = k == len(angs) - 1
        cv = math.cos(math.radians(d))
        f.show(vec(P.ox, P.oy, bx, by, VI, 2.4) + M(bx + (10 if bx >= P.ox else -10), by - 6, '{b}', VI, 'start' if bx >= P.ox else 'end'),
               t0, hide=None if last else t0 + 1.5)
        # arc
        r = 26; a0 = math.radians(base); a1 = th
        pts = [(P.ox + r * math.cos(a0 + (a1 - a0) * i / 20), P.oy - r * math.sin(a0 + (a1 - a0) * i / 20)) for i in range(21)]
        f.show(poly(pts, VI, 1.3) if d else '', t0, hide=None if last else t0 + 1.5)
        f.show(S(SX0, 190, 'θ = %d° → cos θ = %s' % (d, ('%.2f' % cv).replace('-', '−').replace('0.00', '0').replace('−0', '0')), VI, 'start', True),
               t0 + .3, hide=None if last else t0 + 1.5)
        marks.append((t0 + .3, sc(cv) - sc(1), 0))
    f.path(R(sc(1) - 6, SY - 12, 12, 24, VI, 'none', 3), marks, .8, d=.6)
    f.show(S(SX0, 222, 'b is 1.5× longer than a — no effect', MU), 6.4)
    f.show(S(SX0, 244, 'search & RAG: rank by cosine to the query', FI, 'start', True), 6.9)
    return finish(f, 300)

# ---------- 3.1 Row times column ----------
def fig_matmul():
    A = [[1, 2, 0], [0, 1, 3]]
    B = [[2, 1], [1, 0], [4, 1]]
    C = [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(2)] for i in range(2)]
    assert C == [[4, 1], [13, 3]]
    f = Anim('la5-', 720, 0, 'A 2 by 3 matrix A times a 3 by 2 matrix B. For each result cell, a row of A and a column of B '
             'are outlined and their dot product fills the cell: 4, 1, 13, 3.', 'EACH CELL = ROW OF A · COLUMN OF B')
    w, h = 40, 30
    AX, AY = 0, 120
    BX, BY = 170, 48
    AY = BY + 3 * h + 14
    CX, CY = BX, AY
    f.static(matrix(AX, AY, A, w, h, '{A} · 2 × 3') + matrix(BX, BY, B, w, h))
    f.static(M(BX + 2 * w + 12, BY + 50, '{B} · 3 × 2', MU, 'start'))
    f.static(M(AX + 3 * w + 14, AY + h + 5, '×', MU))
    for i in range(2):
        for j in range(2):
            f.static(R(CX + j * w, CY + i * h, w, h, SUNK, RULE, 4, 1))
    f.static(M(CX + w, CY + 2 * h + 22, '{C} = {A}{B} · 2 × 2', MU))
    t0 = .6
    for i in range(2):
        for j in range(2):
            f.show(R(AX - 3, AY + i * h - 3, 3 * w + 6, h + 6, tn(VI, '.08'), VI, 5, 2), t0, hide=t0 + 1.6)
            f.show(R(BX + j * w - 3, BY - 3, w + 6, 3 * h + 6, tn(VI, '.08'), VI, 5, 2), t0, hide=t0 + 1.6)
            terms = ' + '.join('%d·%d' % (A[i][k], B[k][j]) for k in range(3))
            f.show(S(330, 186, 'row %d · column %d' % (i + 1, j + 1), VI, 'start', True) +
                   T(330, 210, '%s = %d' % (terms, C[i][j]), TX, 'start', mono=True), t0 + .2, hide=t0 + 1.6)
            f.show(mcell(CX + j * w, CY + i * h, C[i][j], w, h, FI, tn(FI, '.12')), t0 + 1.0)
            t0 += 1.8
    f.show(S(330, 186, '4 cells = 4 dot products', FI, 'start', True) +
           S(330, 210, 'a GPU runs all of them in parallel', MU), t0)
    return finish(f, AY + 2 * h + 44)

# ---------- 3.2 Shapes ----------
def fig_shapes():
    f = Anim('la6-', 720, 0, 'Shapes as blocks. X is n by d, W is d by k. The two inner d sizes match and cancel; the result is n '
             'by k. Second row: a 3-column X times a W with 2 rows — the inner sizes differ, so the product does not exist.',
             'READ THE SHAPES FIRST · INNER SIZES MUST MATCH')
    u = 22
    def block(x, y, r, c, name, col=BR, fill=None):
        return (R(x, y, c * u, r * u, fill or tn(col, '.10'), col, 4, 1.5) + M(x + c * u / 2, y + r * u / 2 + 5, name, col))
    Y1 = 44
    # X: 4x3, W: 3x2 -> 4x2
    f.show(block(0, Y1, 4, 3, '{X}'), .2)
    f.show(T(3 * u / 2, Y1 + 4 * u + 18, 'n × d', MU, mono=True), .2)
    f.show(T(3 * u + 22, Y1 + 2 * u + 5, '·', MU, cls='sv-n'), .2)
    f.show(block(3 * u + 44, Y1, 3, 2, '{W}'), .5)
    f.show(T(3 * u + 44 + u, Y1 + 4 * u + 18, 'd × k', MU, mono=True), .5)
    # highlight inner sizes
    f.show(R(3 * u / 2 + 4, Y1 + 4 * u + 6, 14, 17, tn(VI, '.16'), VI, 3) + R(3 * u + 44 + u - 18, Y1 + 4 * u + 6, 14, 17, tn(VI, '.16'), VI, 3), 1.3, hide=2.5)
    f.show(L(3 * u / 2 + 2, Y1 + 4 * u + 14, 3 * u / 2 + 20, Y1 + 4 * u + 14, VI, 1.5) +
           L(3 * u + 44 + u - 20, Y1 + 4 * u + 14, 3 * u + 44 + u - 2, Y1 + 4 * u + 14, VI, 1.5), 2.3)
    f.show(S(0, Y1 + 4 * u + 40, 'inner d = d ✓ — they cancel', VI, 'start', True), 2.3)
    RX = 3 * u + 44 + 2 * u + 50
    f.show(T(RX - 22, Y1 + 2 * u + 5, '=', MU, cls='sv-n'), 2.9)
    f.show(block(RX, Y1, 4, 2, '{XW}', FI, tn(FI, '.14')), 2.9)
    f.show(T(RX + u, Y1 + 4 * u + 18, 'n × k', FI, mono=True, bold=True), 2.9)
    X2 = 330
    f.show(S(X2, Y1 + 10, 'n rows of d features', MU) + S(X2, Y1 + 30, '→ the same n rows, now with k features', MU), 3.4)
    f.show(S(X2, Y1 + 62, 'a layer with 512 → 256 units:', TX) +
           T(X2, Y1 + 82, '(32 × 512) · (512 × 256) → (32 × 256)', FI, 'start', mono=True, bold=True), 4.0)
    # mismatch
    Y2 = 210
    f.show(block(0, Y2, 4, 3, '{X}', GH, SUNK) + T(3 * u / 2, Y2 + 4 * u + 18, '4 × 3', MU, mono=True), 5.0)
    f.show(T(3 * u + 22, Y2 + 2 * u + 5, '·', MU, cls='sv-n'), 5.0)
    f.show(block(3 * u + 44, Y2, 2, 5, '{V}', GH, SUNK) + T(3 * u + 44 + 5 * u / 2, Y2 + 4 * u + 18, '2 × 5', MU, mono=True), 5.0)
    f.show(R(3 * u / 2 + 4, Y2 + 4 * u + 6, 14, 17, tn(RO, '.16'), RO, 3) + R(3 * u + 44 + 5 * u / 2 - 18, Y2 + 4 * u + 6, 14, 17, tn(RO, '.16'), RO, 3), 5.8)
    f.show(S(X2, Y2 + 40, '✕ inner sizes 3 ≠ 2 → shape error', RO, 'start', True) +
           S(X2, Y2 + 60, 'the most common bug in ML code', MU), 6.4)
    return finish(f, Y2 + 4 * u + 40)

# ---------- 3.3 Transformation ----------
def fig_transform():
    A = [[2, 1], [0, 1]]
    f = Anim('la7-', 720, 0, 'The matrix A with columns (2, 0) and (1, 1). The basis arrow i moves to (2, 0), the first column; '
             'the arrow j moves to (1, 1), the second column. The unit square becomes a slanted parallelogram: every point '
             'moves with the grid.', 'A MATRIX MOVES SPACE · ITS COLUMNS ARE WHERE i AND j LAND')
    P = Plane(70, 230, 56)
    f.static(P.grid(-1, 3, -1, 3, labels=True))
    sq = [P(0, 0), P(1, 0), P(1, 1), P(0, 1)]
    img = lambda x, y: (A[0][0] * x + A[0][1] * y, A[1][0] * x + A[1][1] * y)
    pg = [P(*img(*q)) for q in [(0, 0), (1, 0), (1, 1), (0, 1)]]
    f.show(poly(sq + [sq[0]], BR, 1.4, None, tn(BR, '.16')), .2, hide=4.6)
    f.show(poly(sq + [sq[0]], GH, 1.2, '4 3'), 4.6)
    ix, iy = P(1, 0); jx, jy = P(0, 1)
    f.show(vec(P.ox, P.oy, ix, iy, BR, 2.6) + M(ix - 2, iy + 22, '{i}', BR), .4, hide=1.6)
    f.show(vec(P.ox, P.oy, jx, jy, BR, 2.6) + M(jx - 14, jy + 4, '{j}', BR), .4, hide=3.0)
    # matrix on the right with column highlight
    MX, MY = 420, 70
    f.static(M(MX - 22, MY + 34, '{A} =', TX, 'end') + matrix(MX, MY, A, 44, 32))
    f.show(R(MX - 3, MY - 3, 50, 70, 'none', VI, 5, 2), 1.0, hide=2.4)
    f.show(R(MX + 41, MY - 3, 50, 70, 'none', VI, 5, 2), 2.4, hide=3.8)
    i2 = P(*img(1, 0)); j2 = P(*img(0, 1))
    f.show(vec(P.ox, P.oy, ix, iy, VI, 2.6), 1.0, hide=1.6)
    f.path(dot(ix, iy, VI, 5), [(0, 0, 0), (1.6, i2[0] - ix, i2[1] - iy)], 1.0, d=.8, hide=2.6)
    f.show(vec(P.ox, P.oy, i2[0], i2[1], VI, 2.6) + M(i2[0] + 14, i2[1] - 8, '{Ai}', VI, 'start'), 2.4)
    f.show(S(MX - 50, 190, 'column 1 → where i lands: (2, 0)', VI, 'start'), 1.6, hide=None)
    f.path(dot(jx, jy, VI, 5), [(0, 0, 0), (3.0, j2[0] - jx, j2[1] - jy)], 2.4, d=.8, hide=4.0)
    f.show(vec(P.ox, P.oy, j2[0], j2[1], VI, 2.6) + M(j2[0] + 10, j2[1] - 4, '{Aj}', VI, 'start'), 3.8)
    f.show(S(MX - 50, 212, 'column 2 → where j lands: (1, 1)', VI, 'start'), 3.0)
    f.show(poly(pg + [pg[0]], FI, 1.8, None, tn(FI, '.16')), 4.6)
    f.show(S(MX - 50, 244, 'the whole grid follows: square → parallelogram', FI, 'start', True), 5.0)
    return finish(f, 276)

# ---------- 4.1 Rank ----------
def fig_rank():
    f = Anim('la8-', 720, 0, 'Two panels, nine grid points each. Left, A with independent columns: points move to a slanted '
             'lattice that still fills the plane, rank 2. Right, B whose second column is twice the first: every point '
             'lands on one line, rank 1. One dimension is lost for good.', 'RANK = HOW MANY DIMENSIONS SURVIVE')
    pts = [(x, y) for y in (-1, 0, 1) for x in (-1, 0, 1)]
    panels = [(170, [[2, 1], [0, 2]], 'rank 2 · still a plane', FI), (520, [[1, 2], [2, 4]], 'rank 1 · flattened to a line', RO)]
    for k, (cx, A, lab, col) in enumerate(panels):
        P = Plane(cx, 186, 17)
        f.static(P.grid(-6, 6, -6, 6, step=1, labels=False))
        name = '{A}' if k == 0 else '{B}'
        f.static(M(cx - 130, 34, name + ' = ', TX, 'start') + matrix(cx - 98, 18, A, 30, 24))
        if k == 1:
            f.show(R(cx - 98 + 30 - 2, 16, 34, 52, 'none', VI, 4, 1.8) + S(cx - 98 + 74, 46, 'column 2 = 2 × column 1', VI), 1.0)
        t0 = 1.6 + k * .2
        for (x, y) in pts:
            nx, ny = A[0][0] * x + A[0][1] * y, A[1][0] * x + A[1][1] * y
            sx, sy = P(x, y); ex, ey = P(nx, ny)
            f.path(dot(ex, ey, col if k else BR, 4.5), [(0, sx - ex, sy - ey), (t0 + 1.0, 0, 0)], .3, d=1.4)
        if k == 1:
            l0, l1 = P(-3, -6), P(3, 6)
            f.show(L(l0[0], l0[1], l1[0], l1[1], RO, 1.4, '4 3'), 3.4)
        f.show(S(cx, 310, lab, col, 'middle', True), 3.6 + k * .4)
    f.show(S(345, 334, 'columns that copy other columns add no new direction', MU, 'middle'), 4.6)
    return finish(f, 350)

# ---------- 4.2 Low rank ----------
def fig_lowrank():
    d, r = 8, 2
    f = Anim('la9-', 720, 0, 'An 8 by 8 matrix W of 64 numbers. It is rebuilt as a tall 8 by 2 matrix B times a wide 2 by 8 '
             'matrix A: 16 plus 16 is 32 numbers. At LLM scale, d 4096 and r 8, that is 0.4 percent of the original.',
             'LOW RANK = A BIG MATRIX AS TWO THIN ONES')
    u = 16
    WX, WY = 0, 40
    for i in range(d):
        for j in range(d):
            f.show(R(WX + j * u, WY + i * u, u - 2, u - 2, tn(BR, '.22'), 'none', 2), .1 + (i + j) * .04)
    f.show(M(WX + d * u / 2, WY + d * u + 22, '{W} · 8 × 8 = 64', BR), .8)
    f.show(T(WX + d * u + 20, WY + d * u / 2 + 5, '≈', MU, cls='sv-n'), 1.8)
    BX = WX + d * u + 44
    for i in range(d):
        for j in range(r):
            f.show(R(BX + j * u, WY + i * u, u - 2, u - 2, tn(VI, '.30'), 'none', 2), 2.0 + i * .05)
    f.show(M(BX + r * u / 2, WY + d * u + 22, '{B} · 8 × 2', VI), 2.4)
    AX = BX + r * u + 18
    for i in range(r):
        for j in range(d):
            f.show(R(AX + j * u, WY + i * u, u - 2, u - 2, tn(VI, '.30'), 'none', 2), 2.8 + j * .05)
    f.show(M(AX + d * u / 2, WY + r * u + 22, '{A} · 2 × 8', VI), 3.2)
    f.show(S(AX, WY + 100, '8·2 + 2·8 = 32 numbers', VI, 'start', True), 3.8)
    f.show(S(AX, WY + 120, 'half of 64, and the gap grows with d', MU), 4.2)
    D, Rr = 4096, 8
    full, lo = D * D, 2 * D * Rr
    assert full == 16777216 and lo == 65536
    X3 = 470
    f.show(S(X3, 60, 'LoRA on one LLM layer', MU, 'start', True), 4.8)
    f.show(T(X3, 84, 'full  4096 × 4096 = %s' % format(full, ','), TX, 'start', mono=True), 5.0)
    f.show(T(X3, 106, 'r=8   2·4096·8 = %s' % format(lo, ','), VI, 'start', mono=True), 5.6)
    f.show(chip(X3 + 90, 140, 'train %.1f%% of the weights' % (100 * lo / full), FI, 200, False), 6.2)
    return finish(f, WY + d * u + 40)

# ---------- 5.1 Eigenvector ----------
def fig_eigen():
    A = [[2, 1], [1, 2]]
    f = Anim('la10-', 720, 0, 'Sixteen arrows of length 1 around a circle. The matrix A = [[2, 1], [1, 2]] moves every tip; the '
             'circle becomes an ellipse. Most arrows turn. Two directions do not: along (1, 1) the arrow is stretched 3 times, '
             'along (1, −1) it keeps its length, 1 times.', 'MOST ARROWS TURN · EIGENVECTORS ONLY STRETCH')
    P = Plane(230, 175, 44)
    f.static(P.grid(-3, 3, -3, 3, labels=False))
    n = 16
    for k in range(n):
        th = 2 * math.pi * k / n
        x, y = math.cos(th), math.sin(th)
        nx, ny = A[0][0] * x + A[0][1] * y, A[1][0] * x + A[1][1] * y
        sx, sy = P(x, y); ex, ey = P(nx, ny)
        eig = k in (2, 6, 10, 14)
        f.show(L(P.ox, P.oy, sx, sy, RULE_HI, 1.2), .2, hide=1.6)
        f.show(L(P.ox, P.oy, ex, ey, GH if not eig else FI, 1.2 if not eig else 2.4), 3.0 if not eig else 4.6)
        f.path(dot(ex, ey, FI if eig else BR, 4), [(0, sx - ex, sy - ey), (1.6, 0, 0)], .2, d=1.2)
    # one turning example: k=0
    x, y = 1, 0
    f.show(vec(P.ox, P.oy, *P(1, 0), VI, 2.4), 3.4)
    f.show(vec(P.ox, P.oy, *P(2, 1), VI, 2.4) + S(P(2, 1)[0] + 8, P(2, 1)[1] + 4, 'turned', VI), 3.8)
    e1 = P(3 / math.sqrt(2), 3 / math.sqrt(2)); e2 = P(1 / math.sqrt(2), -1 / math.sqrt(2))
    f.show(S(e1[0] + 8, e1[1] - 2, '×3', FI, 'start', True), 5.0)
    f.show(S(e2[0] + 8, e2[1] + 14, '×1', FI, 'start', True), 5.0)
    X = 470
    f.static(M(X, 50, '{A} =', TX, 'start') + matrix(X + 40, 34, A, 34, 26))
    f.show(S(X, 120, 'circle → ellipse', MU), 1.8)
    f.show(S(X, 150, 'v₁ = (1, 1)   λ₁ = 3', FI, 'start', True), 5.4)
    f.show(S(X, 172, 'v₂ = (1, −1)  λ₂ = 1', FI, 'start', True), 5.7)
    f.show(S(X, 204, 'the ellipse axes are the eigenvectors', MU), 6.2)
    return finish(f, 352)

# ---------- 5.2 PCA ----------
def lcg(seed):
    s = seed
    while True:
        s = (1103515245 * s + 12345) % 2 ** 31
        yield s / 2 ** 31

def gauss(g):
    u1, u2 = next(g) or 1e-9, next(g)
    return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

def fig_pca():
    g = lcg(7)
    pts = []
    for _ in range(22):
        a, b = gauss(g), gauss(g)
        pts.append((1.6 * a + .25 * b, .9 * a + .45 * b))
    mx = sum(p[0] for p in pts) / len(pts); my = sum(p[1] for p in pts) / len(pts)
    pts = [(x - mx, y - my) for x, y in pts]
    n = len(pts)
    sxx = sum(x * x for x, _ in pts) / (n - 1); syy = sum(y * y for _, y in pts) / (n - 1); sxy = sum(x * y for x, y in pts) / (n - 1)
    tr, det = sxx + syy, sxx * syy - sxy * sxy
    l1 = tr / 2 + math.sqrt(tr * tr / 4 - det); l2 = tr - l1
    vx, vy = sxy, l1 - sxx; nv = math.hypot(vx, vy); vx, vy = vx / nv, vy / nv
    share = l1 / (l1 + l2)
    assert .85 < share < .99, share
    f = Anim('la11-', 720, 0, 'A cloud of 22 points stretched along a diagonal. The covariance matrix gives two eigenvectors: PC1 along '
             'the stretch and PC2 across it. Every point drops onto the PC1 line; one coordinate now keeps %d percent of '
             'the variance.' % round(100 * share), 'PCA · KEEP THE DIRECTION WITH THE MOST SPREAD')
    P = Plane(220, 175, 42)
    f.static(P.grid(-4, 4, -3.3, 3.3, labels=False, xl='{x}₁', yl='{x}₂'))
    for k, (x, y) in enumerate(pts):
        f.show(dot(*P(x, y), BR, 4), .1 + k * .03)
    a1 = P(-4 * vx, -4 * vy); b1 = P(4 * vx, 4 * vy)
    f.show(L(a1[0], a1[1], b1[0], b1[1], FI, 2.4) + S(b1[0] + 6, b1[1] + 4, 'PC1', FI, 'start', True), 1.4)
    a2 = P(1.6 * vy, -1.6 * vx); b2 = P(-1.6 * vy, 1.6 * vx)
    f.show(L(a2[0], a2[1], b2[0], b2[1], VI, 1.8, '5 4') + S(b2[0] - 6, b2[1] - 4, 'PC2', VI, 'end', True), 2.0)
    for k, (x, y) in enumerate(pts):
        s = x * vx + y * vy
        px, py = P(s * vx, s * vy); ox, oy = P(x, y)
        f.path(dot(px, py, FI, 3.6), [(0, ox - px, oy - py), (3.2 + k * .04, 0, 0)], 3.0, d=.8)
    X = 460
    f.show(S(X, 60, 'eigenvalues of the covariance', MU), 1.4)
    f.show(T(X, 84, 'λ₁ = %.2f  along PC1' % l1, FI, 'start', mono=True, bold=True), 1.6)
    f.show(T(X, 106, 'λ₂ = %.2f  along PC2' % l2, VI, 'start', mono=True), 2.1)
    f.show(T(X, 140, 'kept = %.2f / %.2f = %d%%' % (l1, l1 + l2, round(100 * share)), FI, 'start', mono=True, bold=True), 4.6)
    f.show(S(X, 166, '2 columns → 1, almost nothing lost', MU), 5.0)
    return finish(f, 330)

FIGS = {}

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Math foundations</p>
  <h1><em>Linear algebra</em></h1>
  <p class="lede">Data is a matrix, a model is a transformation. Three things to remember:</p>
  <ul class="ledelist">
    <li>the dot product measures <b>how much two arrows agree</b></li>
    <li>a matrix <b>moves the whole space</b>; its columns say where the axes land</li>
    <li>an eigenvector is <b>a direction that is only stretched</b> — the root of PCA</li>
  </ul>
</header>

<section id="linalg-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">One row of data is <em>one arrow</em>; the whole table is <em>one matrix</em>.</p>
{la1}
  <ul class="why">
    <li>A 28×28 image is one arrow in 784-D; a word embedding is one arrow in a few hundred dimensions.</li>
    <li>Shapes are written rows × columns: <span class="mth"><var>X</var></span> is <span class="mth"><var>n</var> × <var>d</var></span>, samples × features.</li>
  </ul>
</section>

<section id="linalg-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Vectors</h2></div>
  <p class="key">Three numbers describe a pair of arrows: <em>length</em>, <em>dot product</em> and <em>cosine</em>.</p>

  <div class="subsec" id="linalg-s2-1">
    <h3 class="ssh"><b>2.1</b>Length (norm)</h3>
    <p class="skey">The length of an arrow is Pythagoras applied to its components.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span>‖<var>a</var>‖</span></span>
      <span class="op">=</span>
      <span class="t b"><span>√(<var>a</var><sub>1</sub><sup>2</sup> + <var>a</var><sub>2</sub><sup>2</sup> + … + <var>a</var><sub><var>n</var></sub><sup>2</sup>)</span><em>square each component, add, take the root</em></span>
    </div>
  </div>
{la2}
    <ul class="why">
      <li>This is the L2 norm; Euclidean distance between two points is the norm of their difference.</li>
      <li>The same norm reappears as the L2 penalty in Ridge and weight decay.</li>
    </ul>
  </div>

  <div class="subsec" id="linalg-s2-2">
    <h3 class="ssh"><b>2.2</b>Dot product</h3>
    <p class="skey">Multiply pair by pair and add: one number for how far one arrow goes along the other.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>a</var> · <var>b</var></span></span>
      <span class="op">=</span>
      <span class="t b"><span><var>a</var><sub>1</sub><var>b</var><sub>1</sub> + <var>a</var><sub>2</sub><var>b</var><sub>2</sub> + … + <var>a</var><sub><var>n</var></sub><var>b</var><sub><var>n</var></sub></span><em>multiply each pair, then add up</em></span>
    </div>
  </div>
{la3}
    <ul class="why">
      <li>A linear model predicts with exactly one dot product: <span class="mth"><var>ŷ</var> = <var>w</var> · <var>x</var> + <var>b</var></span>.</li>
      <li>Large-valued features dominate the sum — scale features before linear models, KNN and SVM.</li>
    </ul>
  </div>

  <div class="subsec" id="linalg-s2-3">
    <h3 class="ssh"><b>2.3</b>Cosine similarity</h3>
    <p class="skey">Divide the dot product by both lengths and only the angle is left.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span>cos <var>θ</var></span></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i><var>a</var> · <var>b</var></i><i>‖<var>a</var>‖ ‖<var>b</var>‖</i></span></span><em>dot product with both lengths divided out</em></span>
    </div>
  </div>
{la4}
    <ul class="why">
      <li>Two texts of very different length can still score 1 if they point the same way.</li>
      <li>Semantic search, recommenders and RAG retrieval rank candidates by cosine to the query vector.</li>
    </ul>
  </div>
</section>

<section id="linalg-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Matrix multiplication</h2></div>
  <p class="key">Matrix multiplication is <em>many dot products at once</em>, and it <em>moves the whole space</em>.</p>

  <div class="subsec" id="linalg-s3-1">
    <h3 class="ssh"><b>3.1</b>Row times column</h3>
    <p class="skey">Each cell of the result is one row of the left matrix dotted with one column of the right.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>C</var><sub><var>ij</var></sub></span></span>
      <span class="op">=</span>
      <span class="t b"><span>Σ<sub><var>k</var></sub> <var>A</var><sub><var>ik</var></sub> <var>B</var><sub><var>kj</var></sub></span><em>row <var>i</var> of A · column <var>j</var> of B</em></span>
    </div>
  </div>
{la5}
    <ul class="why">
      <li>Order matters: <span class="mth"><var>AB</var> ≠ <var>BA</var></span>, and <span class="mth"><var>BA</var></span> may not even exist.</li>
      <li>Matrix form exists to run fast: GPUs parallelize it, Python loops do not.</li>
    </ul>
  </div>

  <div class="subsec" id="linalg-s3-2">
    <h3 class="ssh"><b>3.2</b>Shapes</h3>
    <p class="skey">Read the shapes before the contents: the inner sizes must match and then disappear.</p>
{la6}
    <ul class="why">
      <li>Every dense layer and every attention projection reads as <span class="mth">(<var>n</var> × <var>d</var>) · (<var>d</var> × <var>k</var>) → (<var>n</var> × <var>k</var>)</span>.</li>
      <li>Writing the shape next to each multiplication catches mismatches before the code runs.</li>
    </ul>
  </div>

  <div class="subsec" id="linalg-s3-3">
    <h3 class="ssh"><b>3.3</b>Matrix as a transformation</h3>
    <p class="skey">A matrix moves every point of space; its columns are where the two axis arrows land.</p>
{la7}
    <ul class="why">
      <li>A neural network layer is such a move followed by a non-linear bend (the activation).</li>
    </ul>
  </div>
</section>

<section id="linalg-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Rank</h2></div>
  <p class="key">Rank is <em>the number of truly independent columns</em> — the dimensions that survive the transformation.</p>

  <div class="subsec" id="linalg-s4-1">
    <h3 class="ssh"><b>4.1</b>Lost dimensions</h3>
    <p class="skey">When one column copies another, the matrix flattens space and the lost dimension cannot come back.</p>
{la8}
    <ul class="why">
      <li>A rank-deficient matrix cannot be inverted: two duplicate features leave linear regression without a unique solution.</li>
      <li>Ridge fixes this by adding a little to the diagonal.</li>
    </ul>
  </div>

  <div class="subsec" id="linalg-s4-2">
    <h3 class="ssh"><b>4.2</b>Low-rank factorization</h3>
    <p class="skey">A big matrix with low rank can be stored as two thin matrices multiplied together.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>W</var></span><em>d × d</em></span>
      <span class="op">≈</span>
      <span class="t b"><span><var>B</var></span><em>d × r</em></span>
      <span class="op">·</span>
      <span class="t b"><span><var>A</var></span><em>r × d, with r ≪ d</em></span>
    </div>
  </div>
{la9}
    <ul class="why">
      <li>Real data is almost always low-rank — columns are tangled — which is what makes compression and dimensionality reduction work.</li>
      <li><a href="../../../10-llm/02-training/peft-lora-qlora/index.html">LoRA</a> fine-tunes an LLM by learning only such a low-rank update.</li>
    </ul>
  </div>
</section>

<section id="linalg-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Eigenvectors</h2></div>
  <p class="key">A few directions are <em>only stretched, never turned</em> — they describe a matrix better than its numbers.</p>

  <div class="subsec" id="linalg-s5-1">
    <h3 class="ssh"><b>5.1</b>Eigenvalue &amp; eigenvector</h3>
    <p class="skey">Apply the matrix to every direction: the ones that keep their line are eigenvectors.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>A</var> <var>v</var></span><em>apply the matrix</em></span>
      <span class="op">=</span>
      <span class="t b"><span><var>λ</var> <var>v</var></span><em>same direction, length × λ</em></span>
    </div>
  </div>
{la10}
    <ul class="why">
      <li>Only square matrices have eigenvectors; rectangular ones use SVD — the same idea, and how PCA is computed in practice.</li>
    </ul>
  </div>

  <div class="subsec" id="linalg-s5-2">
    <h3 class="ssh"><b>5.2</b>PCA</h3>
    <p class="skey">The eigenvectors of the covariance matrix are the directions in which the data spreads most.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span>variance kept</span></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i><var>λ</var><sub>1</sub> + … + <var>λ</var><sub><var>k</var></sub></i><i><var>λ</var><sub>1</sub> + … + <var>λ</var><sub><var>d</var></sub></i></span></span><em>eigenvalues kept over all eigenvalues</em></span>
    </div>
  </div>
{la11}
    <ul class="why">
      <li>A direction where the data barely varies cannot tell points apart, so dropping it costs little.</li>
      <li>Scale features first, or the column with the largest units takes over PC1. Full lesson: <a href="../../08-dimensionality/pca-dimensionality/index.html">PCA</a>.</li>
    </ul>
  </div>
</section>

'''

def build():
    figs = dict(la1=fig_mental(), la2=fig_norm(), la3=fig_dot(), la4=fig_cos(), la5=fig_matmul(), la6=fig_shapes(),
                la7=fig_transform(), la8=fig_rank(), la9=fig_lowrank(), la10=fig_eigen(), la11=fig_pca())
    return BODY.format(**{k: v for k, v in figs.items()}) if False else re.sub(r'\{(la\d+)\}', lambda m: figs[m.group(1)], BODY)

def splice(page, body, blurb):
    s = open(page).read()
    a = s.index('<header class="hero">')
    b = s.index('<script>\n/* Figures start')
    s = s[:a] + body + s[b:]
    s = re.sub(r'data-blurb="[^"]*"( data-reviewed="\d")?', 'data-blurb="%s" data-reviewed="2"' % blurb, s, count=1)
    open(page, 'w').write(s)

if __name__ == '__main__':
    splice(PAGE, build(), 'Vectors, dot product, matrix multiplication, rank and eigenvectors — the shapes every model is built from.')
