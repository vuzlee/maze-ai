# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/07-clustering/hdbscan.
Twelve points A..L: a tight group ABC + DEF, a looser group GHIJ, two strays K and L. A small pure-Python HDBSCAN
(core distance -> mutual reachability -> Kruskal MST -> single-linkage tree -> condensed tree -> excess of mass)
computes every number in the figures; asserts pin them. Run: python3 hdbscan.py"""
import os, re, sys, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import Anim, T, R, L, MU, TX, FA, RULE_HI, Table, BR, VI, FI, RO, GH, RULE, BG, M, S, finish
from tablefig import GR, AM, RD, pill
from kmeans_clustering import pdot, tc, ring, chip, fmt, ccell
from decision_tree import splice

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/07-clustering/hdbscan/index.html')

# ---------- data ----------
P = {'A': (0.5, 1.4), 'B': (0.9, 1.1), 'C': (0.5, 0.9), 'D': (2.1, 1.3), 'E': (2.5, 1.5), 'F': (2.4, 1.0),
     'G': (4.9, 1.0), 'H': (6.3, 0.4), 'I': (5.6, 2.0), 'J': (6.7, 1.6), 'K': (3.4, 4.4), 'L': (9.4, 4.2)}
N = list(P)
def d(a, b): return math.dist(P[a], P[b])

# ---------- the algorithm ----------
def hdbscan(ms, mcs):
    core = {p: sorted(d(p, q) for q in N)[ms - 1] for p in N}          # k-th neighbour, the point itself counts
    mr = lambda a, b: max(core[a], core[b], d(a, b))
    E = sorted((mr(a, b), a, b) for a, b in itertools.combinations(N, 2))
    par = {p: p for p in N}
    def find(x):
        while par[x] != x: x = par[x]
        return x
    mst, skipped = [], []
    for w, a, b in E:
        if find(a) != find(b): par[find(a)] = find(b); mst.append((w, a, b))
        else: skipped.append((w, a, b))
        if len(mst) == len(N) - 1: break
    def comps(nodes, edges):
        adj = {n: [] for n in nodes}
        for _, a, b in edges: adj[a].append(b); adj[b].append(a)
        seen, out = set(), []
        for n in sorted(nodes):
            if n in seen: continue
            st, c = [n], set()
            while st:
                x = st.pop()
                if x not in c: c.add(x); st += adj[x]
            seen |= c; out.append(c)
        return out
    cl = []
    def run(nodes, edges, birth, cid):
        c = dict(id=cid, pts=set(nodes), birth=birth, out={}, ch=[]); cl.append(c)
        nodes, edges = set(nodes), sorted(edges)
        while edges:
            w, a, b = edges.pop(); lam = 1 / w
            cs = comps(nodes, edges); big = [x for x in cs if len(x) >= mcs]
            if len(big) >= 2:
                for p in nodes: c['out'][p] = lam
                for x in sorted(big, key=min):
                    c['ch'].append(run(x, [e for e in edges if e[1] in x], lam, cid + str(len(c['ch']) + 1)))
                return c
            for x in cs:
                if len(x) < mcs:
                    for p in x: c['out'][p] = lam
                    nodes -= x; edges = [e for e in edges if e[1] not in x]
            if not big: break
        return c
    root = run(N, mst, 0, 'R')
    stab = lambda c: sum(l - c['birth'] for l in c['out'].values())
    def sel(c):
        if not c['ch']: return stab(c), [c]
        s, Lc = 0, []
        for ch in c['ch']:
            a, b = sel(ch); s += a; Lc += b
        if c is root or s > stab(c): return s, Lc
        return stab(c), [c]
    chosen = sel(root)[1]
    return dict(core=core, mr=mr, mst=mst, skipped=skipped, cl=cl, root=root, stab=stab, chosen=chosen)

def name(c): return ''.join(sorted(c['pts']))
H3 = hdbscan(3, 3)
CORE, MST, CL, STAB = H3['core'], H3['mst'], {c['id']: c for c in H3['cl']}, H3['stab']
r3 = lambda v: round(v, 3)
assert [r3(CORE[p]) for p in N] == [.5, .5, .5, .447, .51, .51, 1.523, 1.523, 1.221, 1.265, 3.256, 4.391]
assert [(r3(w), a + b) for w, a, b in MST] == [(.5, 'AB'), (.5, 'AC'), (.51, 'DE'), (.51, 'DF'), (1.217, 'BD'),
       (1.265, 'IJ'), (1.523, 'GH'), (1.523, 'GI'), (2.452, 'EG'), (3.256, 'EK'), (4.391, 'IL')]
assert H3['skipped'][0][1:] == ('B', 'C')                           # the first edge Kruskal throws away
assert {k: (name(c), r3(c['birth']), r3(STAB(c))) for k, c in CL.items() if k != 'R'} == {
    'R1': ('ABCDEF', .408, 2.485), 'R11': ('ABC', .822, 3.534), 'R12': ('DEF', .822, 3.417), 'R2': ('GHIJ', .408, .994)}
assert sorted(name(c) for c in H3['chosen']) == ['ABC', 'DEF', 'GHIJ']
assert r3(CL['R']['out']['L']) == .228 and r3(CL['R']['out']['K']) == .307
# the two worked pairs of mutual reachability
assert (r3(CORE['B']), r3(CORE['D']), r3(d('B', 'D')), r3(H3['mr']('B', 'D'))) == (.5, .447, 1.217, 1.217)
assert (r3(CORE['E']), r3(CORE['K']), r3(d('E', 'K')), r3(H3['mr']('E', 'K'))) == (.51, 3.256, 3.036, 3.256)
# parameters
HC4 = hdbscan(3, 4); HS4 = hdbscan(4, 3)
assert sorted(name(c) for c in HC4['chosen']) == ['ABCDEF', 'GHIJ'] == sorted(name(c) for c in HS4['chosen'])
assert [r3(HS4['core'][p]) for p in 'ABCDEF'] == [1.603, 1.217, 1.649, 1.217, 1.649, 1.503]

# ---------- DBSCAN at one eps (min_samples 3) ----------
def dbscan(eps, ms=3):
    core = [p for p in N if sum(d(p, q) <= eps for q in N) >= ms]
    lab, k = {}, 0
    for p in core:
        if p in lab: continue
        k += 1; st = [p]
        while st:
            x = st.pop()
            if x in lab: continue
            lab[x] = k
            if x in core: st += [q for q in N if d(x, q) <= eps and q not in lab]
    return sorted(''.join(p for p in N if lab.get(p) == j) for j in range(1, k + 1))

# ---------- single-linkage tree from the MST ----------
def sltree(mst):
    nodes = {p: dict(h=0, pts=[p], kids=[]) for p in N}
    top = {p: p for p in N}; made = []
    for w, a, b in mst:
        ra, rb = top[a], top[b]
        ka, kb = sorted((nodes[ra], nodes[rb]), key=lambda n: min(n['pts']))
        n = dict(h=w, pts=sorted(ka['pts'] + kb['pts']), kids=[ka, kb], edge=a + b); key = 'n%d' % len(made)
        nodes[key] = n; made.append(n)
        for p in n['pts']: top[p] = key
    root = made[-1]
    order = []
    def walk(n):
        if not n['kids']: order.append(n['pts'][0])
        for k in n['kids']: walk(k)
    walk(root)
    return root, made, order
ROOT, MADE, ORDER = sltree(MST)
assert ''.join(ORDER) == 'ABCDEFGHIJKL'
# DBSCAN at eps = cutting the same tree at height eps
def cut(eps, mst=MST, core=CORE):
    par = {p: p for p in N}
    def find(x):
        while par[x] != x: x = par[x]
        return x
    for w, a, b in mst:
        if w <= eps: par[find(a)] = find(b)
    groups = {}
    for p in N:
        if core[p] <= eps: groups.setdefault(find(p), []).append(p)
    return sorted(''.join(g) for g in groups.values() if len(g) > 1 or core[g[0]] <= eps)
EPS = [1.0, 2.0, 3.3]
CUTS = [cut(e) for e in EPS]
assert CUTS == [['ABC', 'DEF'], ['ABCDEF', 'GHIJ'], ['ABCDEFGHIJK']] == [dbscan(e) for e in EPS]
# no single eps gives the HDBSCAN answer: ABC, DEF need eps < 1.217, GHIJ needs eps >= 1.523
assert all(cut(e) != ['ABC', 'DEF', 'GHIJ'] for e in [w for w, _, _ in MST] + [x / 100 for x in range(0, 500)])

# ---------- drawing ----------
SC, OX, OY = 40, 24, 270                      # plane: data x 0..10, y 0..5
def PX(p): return OX + P[p][0] * SC, OY - P[p][1] * SC
LOFF = {'A': (-9, -7, 'end'), 'B': (9, -5, 'start'), 'C': (-9, 12, 'end'), 'D': (-8, -8, 'end'), 'E': (4, -10, 'start'),
        'F': (9, 12, 'start'), 'G': (-9, -6, 'end'), 'H': (9, 12, 'start'), 'I': (-9, -7, 'end'), 'J': (9, -6, 'start'),
        'K': (9, -6, 'start'), 'L': (-9, -7, 'end')}
def lab_(p, x, y, c):
    dx, dy, a = LOFF[p]; return T(x + dx, y + dy, p, c or FA, a, mono=True, bold=bool(c))
KCOL = {'ABC': VI, 'DEF': FI, 'GHIJ': GR, 'ABCDEF': RO, 'ABCDEFGHIJK': BR}
def colof(groups):
    out = {p: None for p in N}
    for g in groups:
        for p in g: out[p] = KCOL[g]
    return out

def plane(f):
    s = R(OX - 14, OY - 4.6 * SC - 14, 9.6 * SC + 28, 4.6 * SC + 28, 'none', RULE, 6, 1)
    f.static(s)

def pts(f, col=None, lab=True, skip=()):
    for p in N:
        if p in skip: continue
        x, y = PX(p); c = (col or {}).get(p)
        f.static(pdot(x, y, c) + (lab_(p, x, y, c) if lab else ''))

def recolour(f, col, t, hide=None, lab=True):
    for k, p in enumerate(N):
        x, y = PX(p); c = col.get(p)
        f.show(R(x - 7, y - 7, 14, 14, BG, 'none', 7) + pdot(x, y, c) +
               (lab_(p, x, y, c) if lab else ''), t + k * .04, hide=hide)

CLIPN = [0]
def circ(x, y, r, c, sw=1.4, dash=None, fill='none'):
    da = ' stroke-dasharray="%s"' % dash if dash else ''
    if r > 60:   # big circles: only the arcs inside the plane frame, so they never cover captions or the table
        x0, y0, x1, y1 = OX - 14, OY - 4.6 * SC - 14, OX + 9.6 * SC + 14, OY + 14
        segs, cur = [], []
        for i in range(361):
            px, py = x + r * math.cos(math.radians(i)), y + r * math.sin(math.radians(i))
            if x0 <= px <= x1 and y0 <= py <= y1: cur.append((px, py))
            elif cur: segs.append(cur); cur = []
        if cur: segs.append(cur)
        if len(segs) > 1 and segs[0][0] == (x + r, y) and segs[-1][-1][0] > x: segs[0] = segs.pop() + segs[0]
        return ''.join('<path d="M%s" fill="none" stroke="%s" stroke-width="%s"%s/>' % (' L'.join('%.1f %.1f' % q for q in g), c, sw, da)
                       for g in segs if len(g) > 1)
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, r, fill, c, sw, da)

def edge(a, b, c=RULE_HI, sw=2, dash=None):
    (x1, y1), (x2, y2) = PX(a), PX(b)
    return L(x1, y1, x2, y2, c, sw, dash)

# dendrogram (distance axis)
class Dendro:
    def __init__(self, x0, top, bot, hmax, sp):
        self.x0, self.top, self.bot, self.hmax, self.sp = x0, top, bot, hmax, sp
        self.lx = {p: x0 + i * sp for i, p in enumerate(ORDER)}
    def Y(self, h): return self.bot - h / self.hmax * (self.bot - self.top)
    def X(self, n): return self.lx[n['pts'][0]] if not n['kids'] else sum(self.X(k) for k in n['kids']) / 2
    def node(self, n, c=RULE_HI, cs=None, sw=1.8, dash=None):
        y = self.Y(n['h']); xs = [self.X(k) for k in n['kids']]
        s = L(xs[0], y, xs[1], y, c, sw, dash)
        for k, x in zip(n['kids'], xs):
            s += L(x, y, x, self.Y(k['h']), (cs or {}).get(id(k), c), sw, dash)
        return s
    def axis(self, xa, ticks):
        s = L(xa, self.top, xa, self.bot, RULE_HI, 1.2)
        for v in ticks:
            s += L(xa - 3, self.Y(v), xa, self.Y(v), RULE_HI, 1) + T(xa - 6, self.Y(v) + 4, '%g' % v, FA, 'end', mono=True)
        return s
    def leaves(self, col=None):
        s = ''
        for p in ORDER:
            c = (col or {}).get(p)
            s += T(self.lx[p], self.bot + 15, p, c or FA, mono=True, bold=bool(c))
        return s

# ---------- 01 Mental model ----------
def fig_mental():
    f = Anim('hd1-', 720, 0, 'Twelve points: a tight pair of groups A B C and D E F, a looser group G H I J, and two strays K '
             'and L. A circle around each point shows how crowded it is. Eleven edges join all points into one tree, '
             'shortest first. The longest edges are cut, from the top down: I to L, E to K, E to G, B to D. What is left '
             'are three clusters, A B C, D E F and G H I J, while K and L stay grey as noise.',
             'MEASURE DENSITY · JOIN INTO A TREE · CUT THE LONG EDGES · KEEP WHAT LASTS')
    plane(f)
    for p in 'ABDEGHIJ':
        x, y = PX(p); f.show(circ(x, y, CORE[p] * SC, FA, 1, '3 3'), .4, hide=2.4)
    for k, (w, a, b) in enumerate(MST):
        f.show(edge(a, b, RULE_HI, 2), 2.6 + k * .22)
    TC = 5.4
    cuts = sorted(MST, reverse=True)[:3] + [e for e in MST if e[1:] == ('B', 'D')]
    for k, (w, a, b) in enumerate(cuts):
        (x1, y1), (x2, y2) = PX(a), PX(b)
        f.show(L(x1, y1, x2, y2, BG, 4) + edge(a, b, RD, 1.6, '4 3'), TC + k * .6)
    pts(f)
    recolour(f, colof(['ABC', 'DEF', 'GHIJ']), TC + 2.8)
    steps = [('core distance', 'how far to the k-th neighbour', .4, 2.4), ('mutual reachability', 'stretch gaps around sparse points', 1.6, 2.6),
             ('spanning tree', 'join all points, cheapest edges first', 2.6, 5.4), ('cut longest first', 'every cut may split a cluster', 5.4, 8.2),
             ('keep the stable clusters', 'the rest is noise', 8.2, None)]
    X0 = 440
    for k, (a, b, t0, t1) in enumerate(steps):
        y = 34 + k * 48
        f.static(R(X0, y, 272, 40, BG, RULE, 6, 1) + T(X0 + 12, y + 17, '%d · %s' % (k + 1, a), TX, 'start', bold=True) +
                 S(X0 + 12, y + 32, b, MU))
        f.show(R(X0, y, 272, 40, 'none', AM, 6, 1.8), t0, hide=t1)
        if k < 4: f.static(L(X0 + 20, y + 40, X0 + 20, y + 48, RULE_HI, 1.2))
    f.show(pill(X0 + 136, 286, '3 clusters · K, L noise', 'gr', 170), TC + 3.4)
    return finish(f, 312)

# ---------- 02 Core distance ----------
def fig_core():
    f = Anim('hd2-', 720, 0, 'Each point in turn draws a circle out to its third point, counting itself: min_samples 3. A, B, '
             'C sit in a crowd, radius 0.5. G is in the loose group, radius 1.52. K is alone, its circle reaches 3.26 to find '
             'two neighbours; L reaches 4.39. Each radius drops into the core column of the table.',
             'CORE DISTANCE = RADIUS THAT HOLDS min_samples POINTS')
    plane(f)
    t = Table(470, 30, [('id', 34), ('core', 62, 'k = 3')], step=20, rh=18)
    f.static(t.head())
    for i, p in enumerate(N):
        f.static(R(t.x, t.ry(i), t.w, t.rh, BG, RULE_HI, 3, 1) + T(t.cx(0), t.ry(i) + 13, p, TX))
    pts(f)
    keep = {'A', 'G'}
    for i, p in enumerate(N):
        t0 = .5 + i * .75; x, y = PX(p)
        nb = sorted(N, key=lambda q: d(p, q))[2]; nx, ny = PX(nb); r = CORE[p] * SC
        hide = None if p in keep else t0 + 1.1
        f.show(ring(x, y, AM, 9), t0, hide=t0 + 1.1)
        if p != 'L':
            f.show(circ(x, y, r, VI if p in keep else AM, 1.4, None if p in keep else '4 3',
                        tc(VI, '.06') if p in keep else 'none'), t0 + .1, hide=hide)
        f.show(L(x, y, nx, ny, AM, 1.4), t0 + .1, hide=t0 + 1.1)
        v = fmt(round(CORE[p], 2)); c = RD if CORE[p] > 3 else (GR if CORE[p] > 1 else VI)
        cx, cy = t.cx(1), t.ry(i) + 13
        f.path(T(cx, cy, v, c, mono=True, bold=True), [(0, (x + nx) / 2 - cx, (y + ny) / 2 - cy - 8), (t0 + .5, 0, 0)], t0 + .2, d=.5)
    f.show(S(10, 304, 'small radius = dense · large radius = sparse', MU), 9.8)
    return finish(f, 314)

# ---------- 03 Mutual reachability ----------
def fig_mreach():
    f = Anim('hd3-', 720, 0, 'Two pairs. B and D: core distances 0.5 and 0.45 are both shorter than the gap 1.22, so the '
             'distance stays 1.22. E and K: the gap is 3.04 but K\'s own core distance is 3.26, so the distance between them '
             'is stretched to 3.26. Dense points keep their distances; a sparse point is pushed away from everything.',
             'DISTANCE = THE LARGEST OF CORE a, CORE b AND THE GAP')
    plane(f); pts(f)
    X0 = 440
    rows = [('B', 'D', 1.0), ('E', 'K', 5.6)]
    for k, (a, b, t0) in enumerate(rows):
        (xa, ya), (xb, yb) = PX(a), PX(b)
        hide = 5.2 if k == 0 else None
        f.show(circ(xa, ya, CORE[a] * SC, VI, 1.4, None, tc(VI, '.07')), t0, hide=hide)
        f.show(circ(xb, yb, CORE[b] * SC, FI if k == 0 else RD, 1.4, None, tc(FI if k == 0 else RD, '.06')), t0 + .5, hide=hide)
        f.show(L(xa, ya, xb, yb, AM, 2), t0 + 1.0, hide=hide)
        y = 50 + k * 120
        f.show(T(X0, y, 'pair %s – %s' % (a, b), TX, 'start', bold=True), t0)
        heads = ['core %s' % a, 'core %s' % b, 'd(%s, %s)' % (a, b)]
        vals = [CORE[a], CORE[b], d(a, b)]
        cols = [VI, FI if k == 0 else RD, AM]
        src = [(xa + CORE[a] * SC * .7, ya - CORE[a] * SC * .7), (xb + CORE[b] * SC * .7, yb - CORE[b] * SC * .7),
               ((xa + xb) / 2, (ya + yb) / 2)]
        win = max(range(3), key=lambda j: vals[j])
        for j in range(3):
            cx = X0 + 40 + j * 80
            f.show(S(cx, y + 24, heads[j], MU, 'middle'), t0 + .2)
            tj = t0 + .6 + j * .5
            f.path(T(cx, y + 48, '%.2f' % vals[j], cols[j], mono=True, bold=True),
                   [(0, src[j][0] - cx, src[j][1] - y - 48), (tj + .3, 0, 0)], tj, d=.6)
        f.show(R(X0 + 40 + win * 80 - 32, y + 32, 64, 24, 'none', GR, 5, 1.8), t0 + 2.6)
        f.show(T(X0, y + 76, 'max =', MU, 'start', mono=True), t0 + 2.6)
        f.show(T(X0 + 44, y + 76, '%.2f' % vals[win], GR, 'start', mono=True, bold=True), t0 + 3.0)
        note = 'gap wins · unchanged' if k == 0 else 'core K wins · stretched'
        f.show(S(X0 + 100, y + 76, note, GR if k == 0 else RD, bold=True), t0 + 3.2)
    return finish(f, 312)

# ---------- 04 Minimum spanning tree ----------
def fig_mst():
    f = Anim('hd4-', 720, 0, 'All pairs are sorted by mutual reachability distance. Kruskal takes them shortest first: A–B 0.5, '
             'A–C 0.5; B–C is skipped because B and C are already joined; then D–E, D–F, B–D, I–J, G–H, G–I, E–G, E–K and '
             'finally I–L at 4.39. Eleven edges connect twelve points with no loop.',
             'TAKE THE SHORTEST EDGE THAT JOINS TWO SEPARATE PIECES · 11 EDGES FOR 12 POINTS')
    plane(f)
    t = Table(452, 30, [('#', 26), ('edge', 56), ('d_mreach', 76)], step=20, rh=18)
    f.static(t.head())
    sk = H3['skipped'][0]
    TS = [.6 + k * .7 for k in range(len(MST))]
    TS = [x + (.9 if k >= 2 else 0) for k, x in enumerate(TS)]
    for k, (w, a, b) in enumerate(MST):
        f.show(edge(a, b, GR if k < 11 else RULE_HI, 2.2), TS[k])
        f.show(t.row(k, [str(k + 1), '%s – %s' % (a, b), '%.2f' % w]).replace('y="%.1f" style' % (t.ry(k) + 17),
               'y="%.1f" style' % (t.ry(k) + 13)), TS[k])
        f.show(t.outline(k, k, c=AM), TS[k], hide=TS[k] + .7)
    ts = TS[1] + .7
    f.show(edge(sk[1], sk[2], RD, 1.8, '4 3'), ts, hide=ts + .8)
    f.show(S(t.x + t.w + 12, t.ry(2) + 12, 'B – C 0.50 skipped: loop', RD, bold=True), ts, hide=ts + .8)
    pts(f)
    f.show(pill(t.x + t.w / 2, t.ry(11) + 6, 'one tree · no loop', 'gr', 130), TS[-1] + .8)
    return finish(f, t.ry(11) + 34)

# ---------- 05 Cluster hierarchy ----------
def fig_hier():
    f = Anim('hd5-', 720, 0, 'The tree\'s edges are cut from the longest down. Cutting I–L at 4.39 splits L off; the dendrogram '
             'on the right draws its top bar at height 4.39. Then E–K at 3.26, E–G at 2.45 which separates the two groups, '
             'G–H and G–I at 1.52, I–J at 1.27, B–D at 1.22 and finally the short edges inside A B C and D E F. Every cut '
             'adds one bar, at the height of the edge that was cut.',
             'CUT THE LONGEST EDGE · EVERY CUT IS ONE MERGE IN THE DENDROGRAM')
    plane(f)
    for w, a, b in MST: f.static(edge(a, b, RULE_HI, 2))
    pts(f)
    D = Dendro(456, 40, 270, 4.6, 21)
    f.static(D.axis(440, [0, 1, 2, 3, 4]) + T(440, 30, 'd_mreach', MU, 'middle') + D.leaves())
    for k, n in enumerate(sorted(MADE, key=lambda n: -n['h'])):
        t0 = .6 + k * .75; a, b = n['edge']
        (x1, y1), (x2, y2) = PX(a), PX(b)
        f.show(L(x1, y1, x2, y2, BG, 4) + edge(a, b, RD, 1.6, '4 3'), t0)
        f.show(D.node(n, TX, sw=1.8), t0 + .2)
        f.show(R(D.X(n) - 18, D.Y(n['h']) - 15, 36, 13, BG, 'none', 2) + T(D.X(n), D.Y(n['h']) - 5, '%.2f' % n['h'], AM, mono=True),
               t0 + .2, hide=t0 + .75 if n['h'] < 2 else None)
    for p in N:
        x, y = PX(p); f.static('')
    return finish(f, 312)

# ---------- condensed tree: cluster of every branch ----------
def owners(H, mcs=3):
    """map id(sl-node) -> cluster colour for the dendrogram branch above it, or None if it fell out"""
    root, made, _ = sltree(H['mst'])
    cols = {}; log = []
    def walk(n, c, live):
        for k in n['kids']:
            if not live: cols[id(k)] = None; walk(k, None, False); continue
            big = [x for x in n['kids'] if len(x['pts']) >= mcs]
            if len(big) == 2: kc = KCOL.get(''.join(k['pts']), BR)
            elif len(k['pts']) >= mcs: kc = c
            else: kc = None
            cols[id(k)] = kc; walk(k, kc, kc is not None)
    cols[id(root)] = BR; walk(root, BR, True)
    return root, made, cols

def fig_condensed():
    f = Anim('hd6-', 720, 0, 'The same dendrogram read from the top with min_cluster_size 3. At 4.39 only L splits off: one '
             'point is less than 3, so L falls out as noise and the big cluster carries on. K falls out the same way at 3.26. At '
             '2.45 both sides have at least 3 points, 6 and 4: a real split into two clusters. Under G H I J every piece has 2 '
             'points or fewer, so the cluster simply ends. At 1.22 A B C and D E F are 3 each: another real split.',
             'BRANCH SMALLER THAN min_cluster_size = POINTS FALLING OUT, NOT A NEW CLUSTER')
    root, made, cols = owners(H3)
    D = Dendro(40, 40, 270, 4.6, 26)
    f.static(D.axis(24, [0, 1, 2, 3, 4]) + T(24, 30, 'd_mreach', MU, 'middle'))
    for n in made: f.static(D.node(n, RULE, sw=1.4))
    f.static(L(D.X(root), D.Y(root['h']), D.X(root), D.Y(root['h']) - 14, RULE, 1.4))
    f.static(D.leaves())
    log = []
    for n in sorted(made, key=lambda n: -n['h']):
        c = cols[id(n)]
        if c is None: continue
        sizes = [len(k['pts']) for k in n['kids']]
        kc = [cols[id(k)] for k in n['kids']]
        if all(kc): msg, tone = '%d and %d ≥ 3 · real split' % tuple(sizes), 'gr'
        elif any(kc): msg, tone = '%s leaves · %d < 3 · noise' % (''.join(n['kids'][kc.index(None)]['pts']), min(sizes)), 'rd'
        else: msg, tone = '%d and %d < 3 · cluster ends' % tuple(sizes), 'am'
        log.append((n, msg, tone))
    T0 = .6
    f.show(L(D.X(root), D.Y(root['h']), D.X(root), D.Y(root['h']) - 14, BR, 3), T0 - .3)
    for k, (n, msg, tone) in enumerate(log):
        t0 = T0 + k * 1.3; y = D.Y(n['h'])
        f.show(R(D.X(n) - 8 - 22, y - 7, 60, 14, 'none', AM, 4, 1.6), t0, hide=t0 + 1.2)
        for kid in n['kids']:
            c = cols[id(kid)]; x = D.X(kid)
            s = L(D.X(n), y, x, y, cols[id(n)], 3) + L(x, y, x, D.Y(kid['h']), c or GH, 3 if c else 1.6, None if c else '3 3')
            f.show(s, t0 + .3)
            if c:   # the whole branch under a live kid is drawn when its own split is read; dead subtrees go grey now
                pass
            else:
                def grey(m):
                    for g in m['kids']:
                        f.show(L(D.X(m), D.Y(m['h']), D.X(g), D.Y(m['h']), GH, 1.6, '3 3') +
                               L(D.X(g), D.Y(m['h']), D.X(g), D.Y(g['h']), GH, 1.6, '3 3'), t0 + .4); grey(g)
                grey(kid)
        X1 = 392; yy = 52 + k * 30
        f.show(T(X1, yy, '%.2f' % n['h'], AM, 'start', mono=True, bold=True) + S(X1 + 44, yy, msg, {'gr': GR, 'rd': RD, 'am': AM}[tone], bold=True), t0 + .3)
    tend = T0 + len(log) * 1.3 + .3
    f.show(R(0, 0, 0, 0, 'none', 'none') + D.leaves({p: KCOL[name(c)] for c in H3['chosen'] for p in c['pts']}), tend)
    y = 52 + len(log) * 30 + 14
    f.show(L(392, y - 12, 712, y - 12, RULE, 1) + S(392, y + 6, 'condensed tree: 4 clusters below the root', TX, bold=True) +
           S(392, y + 24, 'ABCDEF → ABC + DEF, and GHIJ', MU), tend)
    assert [m for _, m, _ in log] == ['L leaves · 1 < 3 · noise', 'K leaves · 1 < 3 · noise', '6 and 4 ≥ 3 · real split',
                                      '2 and 2 < 3 · cluster ends', '3 and 3 ≥ 3 · real split', '2 and 1 < 3 · cluster ends',
                                      '2 and 1 < 3 · cluster ends']
    return finish(f, 312)

# ---------- icicle: condensed tree on a lambda axis, area = stability ----------
CCOL = {'R': BR}
def icicle(f, H, x0, top, sl, u, t0, dt=.9, labels=True, table=None):
    """draw every cluster as a stack of bars: width = points still inside, height = lambda span; returns times"""
    cl = H['cl']; root = H['root']
    pos = {}
    def place(c, cx):
        pos[c['id']] = cx
        if c['ch']:
            ws = [len(ch['pts']) * u for ch in c['ch']]
            tot = sum(ws) + 16 * (len(ws) - 1); x = cx - tot / 2
            for ch, w in zip(c['ch'], ws):
                place(ch, x + w / 2); x += w + 16
    place(root, x0)
    Y = lambda lam: top + lam * sl
    times = {}
    for k, c in enumerate(cl):
        col = KCOL.get(name(c), BR) if c is not root else BR
        events = sorted(set(c['out'].values()))
        cur, n, s = c['birth'], len(c['pts']), ''
        for lam in events:
            w = n * u
            s += R(pos[c['id']] - w / 2, Y(cur), w, Y(lam) - Y(cur), tc(col, '.30' if c is not root else '.12'), col, 1, 1)
            n -= sum(1 for v in c['out'].values() if v == lam); cur = lam
        tk = t0 + k * dt; times[c['id']] = tk
        f.show(s, tk)
        if labels and c is not root:
            f.show(T(pos[c['id']], Y(c['birth']) + 14, name(c), col, mono=True, bold=True), tk + .2)
    return pos, Y, times

def fig_stability():
    f = Anim('hd7-', 720, 0, 'The condensed tree redrawn on a lambda axis, lambda = 1 / distance, growing downward. Each cluster '
             'is a bar as wide as its points and as tall as it lives. Its area is its stability: G H I J, 4 points from 0.41 '
             'to 0.66, gives 0.99; A B C D E F gives 2.48; A B C 3.53 and D E F 3.42. Bottom-up: the children of A B C D E F '
             'sum to 6.95, more than 2.48, so the children are kept. Result: A B C, D E F, G H I J; K and L are noise.',
             'STABILITY = Σ ( λ when a point leaves − λ when the cluster is born ) · KEEP THE MOST STABLE SET')
    pos, Y, times = icicle(f, H3, 150, 44, 118, 12, .4, 1.0)
    f.static(L(8, Y(0), 8, Y(2.0), RULE_HI, 1.2) + T(8, 34, 'λ', MU, 'middle', 'sv-m'))
    for v in (0, .5, 1, 1.5, 2): f.static(L(5, Y(v), 8, Y(v), RULE_HI, 1) + T(14, Y(v) + 4, '%g' % v, FA, 'start', mono=True))
    root = CL['R']
    for p, xo in (('L', -78), ('K', 78)):
        f.show(T(150 + xo + (10 if xo > 0 else -10), Y(root['out'][p]) + 4, p + ' out', RD, 'start' if xo > 0 else 'end', mono=True, bold=True), 1.0)
    t = Table(372, 30, [('cluster', 70), ('n', 26), ('λ birth', 54), ('λ leave', 54), ('stability', 72)], step=24, rh=20)
    f.static(t.head())
    rows = ['R2', 'R1', 'R11', 'R12']
    T1 = 4.8
    for i, k in enumerate(rows):
        c = CL[k]; col = KCOL[name(c)]; lv = sorted(set(c['out'].values()))
        tr = T1 + i * 1.0
        f.show(t.row(i, [name(c), str(len(c['pts'])), '%.3f' % c['birth'], '%.3f' % lv[0], '']).replace(
            'y="%.1f" style' % (t.ry(i) + 17), 'y="%.1f" style' % (t.ry(i) + 14), 6), tr)
        cx, cy = t.cx(4), t.ry(i) + 14
        sx, sy = pos[k], (Y(c['birth']) + Y(lv[0])) / 2 + 4
        f.path(T(cx, cy, '%.2f' % STAB(c), col, mono=True, bold=True), [(0, sx - cx, sy - cy), (tr + .5, 0, 0)], tr + .2, d=.6)
    yb = t.ry(4) + 12
    T2 = T1 + 4.6
    s11, s12, s1 = STAB(CL['R11']), STAB(CL['R12']), STAB(CL['R1'])
    f.show(M(372, yb + 14, '%.2f + %.2f = %.2f  >  %.2f' % (s11, s12, s11 + s12, s1), TX, 'start'), T2)
    f.show(S(372, yb + 34, 'children beat the parent → keep ABC and DEF', GR, bold=True), T2 + .4)
    f.show(S(372, yb + 56, 'GHIJ has no children → keep it', GR, bold=True), T2 + 1.0)
    # parent crossed, winners ringed
    p1 = CL['R1']; w = 6 * 12
    f.show(L(pos['R1'] - w / 2 - 4, Y(p1['birth']) - 2, pos['R1'] + w / 2 + 4, Y(.822) + 2, RD, 2), T2 + .4)
    for k in ('R11', 'R12', 'R2'):
        c = CL[k]; w = len(c['pts']) * 12; lv = max(c['out'].values())
        f.show(R(pos[k] - w / 2 - 4, Y(c['birth']) - 4, w + 8, Y(lv) - Y(c['birth']) + 8, 'none', GR, 4, 2), T2 + (1.0 if k == 'R2' else .6))
    f.show(pill(372 + 165, yb + 76, 'ABC · DEF · GHIJ · noise K, L', 'gr', 220), T2 + 1.6)
    assert round(s11 + s12, 2) == 6.95 and s11 + s12 > s1
    return finish(f, max(Y(2.0) + 12, yb + 104))

# ---------- 08 parameters ----------
def fig_param(H, pre, aria, capt, note):
    f = Anim(pre, 720, 0, aria, capt)
    plane(f)
    base = colof(['ABC', 'DEF', 'GHIJ']); new = colof([name(c) for c in H['chosen']])
    pts(f, base)
    recolour(f, new, 4.6)
    icicle(f, H, 590, 44, 118, 12, .5, .9)
    f.static(L(452, 44, 452, 44 + 2 * 118, RULE_HI, 1.2) + T(452, 34, 'λ', MU, 'middle', 'sv-m'))
    for v in (0, .5, 1, 1.5, 2): f.static(L(449, 44 + v * 118, 452, 44 + v * 118, RULE_HI, 1) + T(458, 44 + v * 118 + 4, '%g' % v, FA, 'start', mono=True))
    f.show(S(10, 304, note, RO, bold=True), 5.2)
    return finish(f, 314)

def fig_mcs():
    return fig_param(HC4, 'hd8-', 'Same points, min_cluster_size raised to 4. A B C and D E F have only 3 points each, so their '
                     'split no longer counts: the points fall out of A B C D E F together. The condensed tree keeps two '
                     'clusters, A B C D E F and G H I J, and the plane recolours: the two tight groups merge into one.',
                     'min_cluster_size = 4 · A GROUP OF 3 IS NO LONGER A CLUSTER', 'ABC and DEF merge: 3 < 4')

def fig_ms():
    return fig_param(HS4, 'hd9-', 'Same points, min_samples raised to 4 with min_cluster_size back at 3. Every core distance grows: '
                     'A to F now reach 1.2 to 1.6, as far as the gap between A B C and D E F, so the dip between them '
                     'disappears. The condensed tree has two clusters again, A B C D E F and G H I J, and their points leave '
                     'at different lambdas, so the bars narrow step by step.',
                     'min_samples = 4 · BIGGER CIRCLES · SMOOTHER DENSITY', 'core A–F grow to 1.2–1.6: the gap is smoothed away')

# ---------- 09 DBSCAN at every eps ----------
def fig_dbscan():
    f = Anim('hd10-', 720, 0, 'The dendrogram again, with a horizontal line for DBSCAN\'s eps. At eps 1.0 the line cuts out A B C '
             'and D E F, and G H I J is noise. At eps 2.0 it gives A B C D E F and G H I J. At eps 3.3 everything except L '
             'is one cluster. No single line gives the HDBSCAN answer, which takes A B C and D E F from low in the tree and '
             'G H I J from higher up.', 'ONE eps = ONE HORIZONTAL CUT · HDBSCAN PICKS BRANCHES AT DIFFERENT HEIGHTS')
    plane(f); pts(f)
    D = Dendro(456, 40, 270, 4.6, 21)
    f.static(D.axis(440, [0, 1, 2, 3, 4]) + T(440, 30, 'd_mreach', MU, 'middle') + D.leaves())
    for n in MADE: f.static(D.node(n, RULE_HI, sw=1.6))
    TS = [.8, 3.6, 6.4]
    yfirst = D.Y(EPS[0])
    pts_ = [(0, 0, D.Y(4.6) - yfirst)] + [(TS[k] - .7, 0, D.Y(e) - yfirst) for k, e in enumerate(EPS)]
    f.path(L(440, yfirst, 712, yfirst, AM, 2, '6 4'), [(0, 0, 0)] + [(TS[k] - .7, 0, D.Y(e) - yfirst) for k, e in enumerate(EPS)],
           .3, d=.6, hide=TS[-1] + 2.4)
    for k, e in enumerate(EPS):
        hide = TS[k + 1] - .7 if k < 2 else TS[-1] + 2.4
        f.show(R(652, D.Y(e) - 20, 60, 16, BG, 'none', 3) + T(682, D.Y(e) - 8, 'eps %g' % e, AM, mono=True, bold=True), TS[k] - .1, hide=hide)
        recolour(f, colof(CUTS[k]), TS[k], hide=hide)
        f.show(S(10, 304, 'DBSCAN eps %g → %s' % (e, ' · '.join(CUTS[k]) + ' · rest noise'), AM, bold=True), TS[k], hide=hide)
    tf = TS[-1] + 2.6
    for c in H3['chosen']:
        nd = [n for n in MADE if n['pts'] == sorted(c['pts'])][0]
        col = KCOL[name(c)]
        def paint(m):
            s = ''
            for g in m['kids']:
                s += L(D.X(m), D.Y(m['h']), D.X(g), D.Y(m['h']), col, 2.6) + L(D.X(g), D.Y(m['h']), D.X(g), D.Y(g['h']), col, 2.6)
                s += paint(g)
            return s
        f.show(paint(nd) + L(D.X(nd), D.Y(nd['h']), D.X(nd), D.Y(nd['h']) - 10, col, 2.6), tf)
    recolour(f, colof(['ABC', 'DEF', 'GHIJ']), tf)
    f.show(S(10, 304, 'HDBSCAN → ABC · DEF · GHIJ · no single eps gives this', GR, bold=True), tf + .3)
    return finish(f, 314)

BODY = r'''<header class="hero">
  <p class="eyebrow">Machine learning · Clustering</p>
  <h1><em>HDBSCAN</em></h1>
  <p class="lede">HDBSCAN builds the whole tree of density clusters from one spanning tree, then keeps the branches that <b>last longest</b> — no <code>eps</code> to choose.</p>
</header>

<section id="hdb-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Measure how crowded each point is, join all points into one tree, cut it <em>from the longest edge down</em>, and keep the pieces that survive.</p>
{hd1}
  <ul class="why">
    <li>It is <a href="../dbscan/index.html">DBSCAN</a> without a fixed <code>eps</code>: clusters of different density, like A B C and G H I J here, come out together.</li>
    <li>Points that never join a lasting piece are <b>noise</b>, label <code>−1</code>, as in DBSCAN.</li>
  </ul>
</section>

<section id="hdb-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Core distance</h2></div>
  <p class="key">A point's core distance is the radius it needs to hold <em><code>min_samples</code> points</em>, itself included.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">core</b><sub><var>k</var></sub>(<var>a</var>)</span><em>core distance of a</em></span>
      <span class="op">=</span>
      <span class="t b"><span><var>d</var>(<var>a</var>, <var>k</var>-th nearest point)</span><em>k = min_samples, a counts as the first</em></span>
    </div>
  </div>
{hd2}
  <ul class="why">
    <li>Small radius = dense neighbourhood; large radius = sparse. It is DBSCAN's core-point test turned into a number.</li>
    <li>It is still a distance: <b>scale the features first</b>, or one large unit decides every radius.</li>
  </ul>
</section>

<section id="hdb-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Mutual reachability distance</h2></div>
  <p class="key">Two points are never closer than <em>either one's core distance</em>: sparse points get pushed away.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>d</var><sub>mreach</sub>(<var>a</var>, <var>b</var>)</span><em>new distance</em></span>
      <span class="op">=</span>
      <span class="t"><span><b class="fn">max</b>(</span><em></em></span>
      <span class="t b"><span><b class="fn">core</b>(<var>a</var>), <b class="fn">core</b>(<var>b</var>)</span><em>density of each end</em></span>
      <span class="op">,</span>
      <span class="t p"><span><var>d</var>(<var>a</var>, <var>b</var>) )</span><em>plain distance</em></span>
    </div>
  </div>
{hd3}
  <ul class="why">
    <li>Inside a crowd nothing changes; a lone point like K is far from everything, so it joins the tree late.</li>
  </ul>
</section>

<section id="hdb-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Minimum spanning tree</h2></div>
  <p class="key">Join all points with the <em>cheapest set of edges</em> under mutual reachability: n − 1 edges, no loop.</p>
{hd4}
  <ul class="why">
    <li>Kruskal: sort the edges, take each one that joins two separate pieces (the union-find of DSA). Prim grows the same tree from one point.</li>
    <li>This tree holds every DBSCAN result at once — section 09.</li>
  </ul>
</section>

<section id="hdb-s5" class="lesson">
  <div class="sh"><b>05</b><h2>Cluster hierarchy</h2></div>
  <p class="key">Remove the tree's edges <em>longest first</em>: each removal splits a piece, and the splits stacked by height form a dendrogram.</p>
{hd5}
  <ul class="why">
    <li>This is single-linkage hierarchical clustering on the mutual reachability distance.</li>
    <li>A dendrogram with 12 leaves has 11 merges — too many pieces, mostly single points. The next step prunes it.</li>
  </ul>
</section>

<section id="hdb-s6" class="lesson">
  <div class="sh"><b>06</b><h2>Condensed tree</h2></div>
  <p class="key">A split counts only if both sides have at least <em><code>min_cluster_size</code></em> points; a smaller side is points falling out.</p>
{hd6}
  <ul class="why">
    <li>Each cluster now has a life: it is <b>born</b> at a real split and <b>ends</b> when its points fall out or it splits again.</li>
    <li>Distance turns into <span class="mth"><var>λ</var> = 1 / <var>d</var></span>: a cluster lives from a small λ (loose) to a large λ (dense).</li>
  </ul>
</section>

<section id="hdb-s7" class="lesson">
  <div class="sh"><b>07</b><h2>Stability &amp; selection</h2></div>
  <p class="key">A cluster's stability is how long its points stay in it; keep the set of clusters with <em>the largest total</em>, never one inside another.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><b class="fn">stability</b>(<var>C</var>)</span><em>area of the bar</em></span>
      <span class="op">=</span>
      <span class="t"><span>Σ<sub><var>p</var> ∈ <var>C</var></sub></span><em>every point of C</em></span>
      <span class="t g"><span>( <var>λ</var><sub><var>p</var></sub></span><em>λ when p leaves C</em></span>
      <span class="op">−</span>
      <span class="t r"><span><var>λ</var><sub>birth</sub>(<var>C</var>) )</span><em>λ when C was born</em></span>
    </div>
  </div>
{hd7}
  <ul class="why">
    <li><b>Excess of mass</b> (the default): bottom-up, keep the children if their stabilities sum to more than the parent's, else keep the parent.</li>
    <li><b>Soft membership</b>: <code>probabilities_</code> scores each point 0–1 by how long it stayed in its cluster compared with the longest-staying point; noise gets 0.</li>
  </ul>
</section>

<section id="hdb-s8" class="lesson">
  <div class="sh"><b>08</b><h2>Parameters</h2></div>
  <p class="key">Two knobs instead of <code>eps</code>: the <em>smallest group worth a name</em>, and how much to smooth density.</p>
  <div class="subsec" id="hdb-s8-1">
    <h3 class="ssh"><b>8.1</b>min_cluster_size</h3>
    <p class="skey">The smallest number of points that still counts as a cluster: raise it and <em>small groups merge or become noise</em>.</p>
{hd8}
    <ul class="why">
      <li>The main parameter, and it reads in business terms: "a segment needs at least 50 customers".</li>
    </ul>
  </div>
  <div class="subsec" id="hdb-s8-2">
    <h3 class="ssh"><b>8.2</b>min_samples</h3>
    <p class="skey">The k of the core distance: raise it and density is <em>smoothed over more neighbours</em>, so small dips vanish.</p>
{hd9}
    <ul class="why">
      <li>Defaults to <code>min_cluster_size</code>; larger values are more conservative and usually label more points noise.</li>
    </ul>
  </div>
</section>

<section id="hdb-s9" class="lesson">
  <div class="sh"><b>09</b><h2>DBSCAN at every eps</h2></div>
  <p class="key">DBSCAN with one <code>eps</code> is <em>one horizontal cut</em> of this dendrogram; HDBSCAN chooses branches at whatever height each is most stable.</p>
{hd10}
  <ul class="why">
    <li>That is why it handles mixed density: the tight groups are cut low, the loose group high.</li>
    <li>Costs more than one DBSCAN run, and density loses meaning in hundreds of dimensions — reduce embeddings first (UMAP is the usual partner).</li>
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

<footer>Machine learning · Clustering · continues from <a href="../dbscan/index.html">DBSCAN</a>; the map of the families is in <a href="../clustering-overview/index.html">Clustering overview</a>.</footer>
'''

def build():
    figs = dict(hd1=fig_mental(), hd2=fig_core(), hd3=fig_mreach(), hd4=fig_mst(), hd5=fig_hier(), hd6=fig_condensed(),
                hd7=fig_stability(), hd8=fig_mcs(), hd9=fig_ms(), hd10=fig_dbscan())
    return re.sub(r'\{(hd\d+)\}', lambda m: figs[m.group(1)], BODY)

if __name__ == '__main__':
    splice(PAGE, build(), 'Core distances, mutual reachability, a spanning tree cut from the longest edge down, and the most '
           'stable branches of the condensed tree: DBSCAN at every eps at once.')
