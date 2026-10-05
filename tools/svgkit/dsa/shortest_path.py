"""Figures for content/01-dsa/04-algorithms/shortest-path. Writes /tmp/dsa/shortest-path.json and splices the page."""
import sys, os, json, re, math, heapq, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graph_bigo_kit import *
INF = float('inf')
figs = {}

BELOW = {'B'}
def bdg(P, k, txt, c=TG):
    return badge(P[k][0], P[k][1], txt, c, NR + 20 if k in BELOW else -NR - 8)

def ds(d): return '∞' if d == INF else str(d)

# shared weighted digraph
POS = {'S': (20, 110), 'A': (150, 35), 'B': (150, 185), 'C': (290, 110), 'T': (410, 110)}
E1 = [('S', 'A', 4), ('S', 'B', 1), ('B', 'A', 2), ('B', 'C', 5), ('A', 'C', 1), ('A', 'T', 6), ('C', 'T', 3)]
WOFF = {('S', 'A'): (-12, -8), ('S', 'B'): (-12, 8), ('B', 'A'): (12, 0), ('B', 'C'): (10, 10), ('A', 'C'): (10, -10), ('A', 'T'): (0, -12), ('C', 'T'): (0, -12)}

def draw_graph(S, P, E, woff, t0=.2, r=NR, shift=None):
    shift = shift or {}
    for i, (a, b, w) in enumerate(E):
        dx, dy = shift.get((a, b), (0, 0))
        pa, pb = (P[a][0] + dx, P[a][1] + dy), (P[b][0] + dx, P[b][1] + dy)
        S.at(t0 + i * .05, edge(pa, pb, RULE_HI, 1.4, True) + wlab(P[a], P[b], w, MU, woff.get((a, b), (0, -12))))
    for i, k in enumerate(P): S.at(t0 + .1 + i * .07, node(*P[k], k), key='n' + k)

# ---------- 1.1 Dijkstra ----------
def dijkstra_fig():
    lines = ['dist, h = {s: 0}, [(0, s)]', 'while h:', '    d, u = heappop(h)', '    if d > dist[u]: continue',
             '    for v, w in adj[u]:', '        if d + w < dist.get(v, inf):', '            dist[v] = d + w', '            heappush(h, (dist[v], v))']
    S = Story('sm1-', 0, 'Five vertices with weighted arrows, target T. The heap starts with S at 0. Pop S: A gets 4, B gets 1. Pop B: A improves to 3, C gets 6. Pop A: C improves to 4, T gets 9. The old entry A 4 is popped and skipped as stale. Pop C: T improves to 7. C 6 is stale. Pop T at 7: done.',
              'DIJKSTRA · ALWAYS POP THE CHEAPEST VERTEX')
    code = S.setcode(0, 40, lines)
    X0, Y0 = code.w + 44, 44
    P = {k: (X0 + x, Y0 + y) for k, (x, y) in POS.items()}
    S.f.w = int(X0 + 470)
    draw_graph(S, P, E1, WOFF)
    S.at(1.1, goal_ring(*P['T']))
    tx, ty = P['T']
    S.path(chip(tx, ty - 50, 'target = T'), [(0, 0, 0), (2.4, S.f.w - 70 - tx, 2 - (ty - 50))], 1.1)
    HY = Y0 + 228; HX = X0 + 50; HW = 46
    S.static(T(X0, HY + 20, 'heap', MU, 'start', mono=True))
    S.sx, S.sy = X0, HY + 64
    def heaprow(t, h, ring_first=False):
        items = sorted(h)
        g = R(HX - 4, HY - 4, 9 * (HW + 6), 38, 'var(--sunk)', 'none', 0)
        for k, (d, v) in enumerate(items): g += box(HX + k * (HW + 6), HY, '%d·%s' % (d, v), 'plain', HW, 30)
        S.at(t, g, key='heap')
    t = 3.0; S.line(t, 0)
    dist = {'S': 0}; h = [(0, 'S')]; done = set()
    S.at(t, bdg(P, 'S', 0), key='bS')
    heaprow(t + .2, h)
    S.say(t, 'dist[S] = 0 · heap = [(0, S)]', 0, PT)
    t += 1.4; ring_pts = []; adj = {k: [(b, w) for a, b, w in E1 if a == k] for k in POS}
    while h:
        S.line(t, 1); S.line(t + .3, 2)
        S.at(t + .3, bring(HX, HY, HW, 30), hide=t + 1.0)
        d, u = heapq.heappop(h)
        S.say(t + .3, 'heappop → (%d, %s), the smallest' % (d, u), 0, MID)
        heaprow(t + 1.0, h)
        rx, ry = P[u]
        S.line(t + 1.1, 3)
        if d > dist[u]:
            S.say(t + 1.1, '%d > dist[%s] = %d → stale entry, skip' % (d, u, dist[u]), 1, MU)
            t += 2.2; continue
        if not ring_pts: ring_pts = [(0, rx - P['S'][0], ry - P['S'][1])]; rt0 = t + 1.1
        else: ring_pts.append((t + 1.1, rx - P['S'][0], ry - P['S'][1]))
        done.add(u)
        S.at(t + 1.1, node(*P[u], u, 'seen'), key='n' + u)
        if u == 'T':
            S.say(t + 1.1, 'T is the target → its dist is final', 1, TX)
            fin = t + 1.8; break
        S.say(t + 1.1, 'dist[%s] = %d is now final' % (u, d), 1, TX)
        t += 1.8
        for v, w in adj[u]:
            S.line(t, 4); S.line(t + .3, 5)
            S.at(t, edge(P[u], P[v], MID, 2.4, True), hide=t + 1.2)
            old = dist.get(v, INF)
            if d + w < old:
                dist[v] = d + w; heapq.heappush(h, (dist[v], v))
                S.say(t + .3, '%d + %d = %d < %s → dist[%s] = %d' % (d, w, d + w, ds(old), v, d + w), 1, TX)
                S.line(t + .7, 6); S.line(t + 1.0, 7)
                S.at(t + .7, bdg(P, v, dist[v]), key='b' + v)
                heaprow(t + 1.0, h)
            else:
                S.say(t + .3, '%d + %d = %d ≥ %s → no change' % (d, w, d + w, ds(old)), 1, MU)
            t += 1.5
    S.path(ring(*P['S']), ring_pts, rt0, hide=fin)
    assert dist['T'] == 7
    S.at(fin, node(*P['T'], 'T', 'ans'), key='nT')
    S.at(fin + .2, T(P['T'][0], P['T'][1] + NR + 16, '✓ found', TG, mono=True, bold=True))
    for a, b in (('S', 'B'), ('B', 'A'), ('A', 'C'), ('C', 'T')): S.at(fin + .3, edge(P[a], P[b], TG, 2.6, True))
    S.say(fin + .4, 'dist[T] = 7 via S → B → A → C → T', 0, TG, True)
    S.say(fin + .4, '', 1)
    return S.render(max(code.y + code.h(), S.sy + 30) + 8)
figs['m1'] = dijkstra_fig()

# ---------- 1.2 negative edge ----------
def negative():
    P0 = {'S': (30, 110), 'A': (230, 40), 'B': (230, 180)}
    E = [('S', 'A', 2), ('S', 'B', 5), ('B', 'A', -4)]
    S = Story('sm2-', 620, 'S to A costs 2, S to B costs 5, B to A costs minus 4. Dijkstra pops A first at 2 and locks it. Later, from B, the negative edge offers 5 minus 4 equals 1, cheaper than the locked 2, but A is already final. The true shortest distance to A is 1.',
              'NEGATIVE EDGE · "POPPED MEANS FINAL" STOPS BEING TRUE')
    P = {k: (x + 40, y + 30) for k, (x, y) in P0.items()}
    draw_graph(S, P, E, {('S', 'A'): (-10, -12), ('S', 'B'): (-10, 12), ('B', 'A'): (18, 0)})
    S.at(1.0, goal_ring(*P['A']))
    S.at(1.0, chip(440, 14, 'shortest S → A', a='start'))
    S.sx, S.sy = 340, 120
    t = 2.2
    S.at(t, bdg(P, 'S', 0), key='bS'); S.at(t, node(*P['S'], 'S', 'seen'), key='nS')
    S.at(t + .6, bdg(P, 'A', 2), key='bA'); S.at(t + .6, bdg(P, 'B', 5), key='bB')
    S.say(t, 'pop S → A = 2, B = 5', 0, PT)
    t += 2.0
    S.at(t, ring(*P['A']), hide=t + 1.6)
    S.at(t, node(*P['A'], 'A', 'seen'), key='nA')
    S.at(t + .3, T(P['A'][0] + 30, P['A'][1] + 5, 'locked', PT, 'start', cls='sv-s', mono=True, bold=True))
    S.say(t, 'pop A (2 < 5) → dist[A] = 2 is final', 0, MID)
    t += 2.2
    S.at(t, ring(*P['B']), hide=t + 2.4)
    S.at(t, node(*P['B'], 'B', 'seen'), key='nB')
    S.say(t, 'pop B (5)', 0, MID)
    S.at(t + .6, edge(P['B'], P['A'], MID, 2.6, True), hide=t + 2.4)
    S.say(t + .6, '5 + (−4) = 1 < 2, but A is already final', 1, TX)
    t += 3.0
    S.at(t, bdg(P, 'A', 1), key='bA')
    S.at(t, node(*P['A'], 'A', 'ans'), key='nA')
    S.at(t, edge(P['S'], P['B'], TG, 2.6, True) + edge(P['B'], P['A'], TG, 2.6, True))
    S.say(t + .2, 'true dist[A] = 1 · Dijkstra answered 2', 0, TG, True)
    S.say(t + .2, '→ negative edges need Bellman-Ford', 1, TG)
    return S.render(250)
figs['m2'] = negative()

# ---------- 1.3 Bellman-Ford ----------
def bellman():
    P0 = {'S': (20, 100), 'A': (150, 30), 'B': (150, 170), 'C': (280, 100)}
    EL = [('A', 'C', 3), ('B', 'A', -4), ('S', 'B', 5), ('S', 'A', 2)]
    lines = ['for _ in range(V - 1):', '    for u, v, w in edges:', '        if dist[u] + w < dist[v]:', '            dist[v] = dist[u] + w']
    S = Story('sm3-', 0, 'Four vertices, four edges, one negative. Bellman-Ford relaxes every edge in a fixed order, three rounds for four vertices. Round 1 sets B to 5 and A to 2. Round 2 sets C to 5 and improves A to 1. Round 3 improves C to 4. Final: S 0, A 1, B 5, C 4.',
              'BELLMAN-FORD · RELAX EVERY EDGE, V − 1 ROUNDS')
    code = S.setcode(0, 40, lines)
    EX = 0; EY = 40 + code.h() + 34
    S.static(T(EX, EY - 10, 'edges', MU, 'start', mono=True))
    EW = 120
    for k, (a, b, w) in enumerate(EL):
        S.static(R(EX, EY + k * 34, EW, 28, 'var(--bg)', RULE_HI, 6) + T(EX + EW / 2, EY + k * 34 + 19, '%s → %s   %s' % (a, b, ('%d' % w).replace('-', '−')), TX, mono=True))
    X0, Y0 = max(code.w, EW) + 50, 50
    P = {k: (X0 + x, Y0 + y) for k, (x, y) in P0.items()}
    S.f.w = int(X0 + 330)
    draw_graph(S, P, EL, {('S', 'A'): (-12, -8), ('S', 'B'): (-12, 8), ('B', 'A'): (14, 0), ('A', 'C'): (10, -10)})
    S.sx, S.sy = X0, Y0 + 250
    dist = {k: INF for k in P0}; dist['S'] = 0
    t = 1.6
    for k in P0: S.at(t, bdg(P, k, ds(dist[k]), PT), key='b' + k)
    S.say(t, 'dist[S] = 0, the rest ∞', 0, PT)
    t += 1.4; rp = []; rt0 = None
    for rnd in range(1, 4):
        S.line(t, 0)
        S.say(t, 'round %d of 3 (V − 1 = 3)' % rnd, 0, PT)
        t += .6
        for k, (a, b, w) in enumerate(EL):
            S.line(t, 1); S.line(t + .2, 2)
            if rt0 is None: rt0 = t; rp = [(0, 0, 0)]
            else: rp.append((t, 0, k * 34))
            S.at(t + .2, edge(P[a], P[b], MID, 2.4, True), hide=t + 1.0)
            if dist[a] + w < dist[b]:
                old = dist[b]; dist[b] = dist[a] + w
                S.say(t + .2, '%s + %s = %d < %s → dist[%s] = %d' % (ds(dist[a]), ('%d' % w).replace('-', '−') if w < 0 else w, dist[b], ds(old), b, dist[b]), 1, TX)
                S.line(t + .6, 3)
                S.at(t + .6, bdg(P, b, dist[b]), key='b' + b)
                t += 1.4
            else:
                S.say(t + .2, '%s → %s: %s' % (a, b, 'dist[%s] = ∞, skip' % a if dist[a] == INF else 'no improvement'), 1, MU)
                t += 1.0
    S.path(R(EX - 3, EY - 3, EW + 6, 34, vt('.10'), MID, 8, 2.2), rp, rt0, hide=t, d=.3)
    assert dist == {'S': 0, 'A': 1, 'B': 5, 'C': 4}
    S.at(t, node(*P['A'], 'A', 'ans') + node(*P['C'], 'C', 'ans') + node(*P['B'], 'B', 'seen') + node(*P['S'], 'S', 'seen'))
    S.say(t + .2, '✓ S 0 · A 1 · B 5 · C 4 after 3 rounds', 0, TG, True)
    S.say(t + .2, 'a 4th round that still improves = negative cycle', 1, MU)
    return S.render(max(EY + 4 * 34, S.sy + 30) + 8)
figs['m3'] = bellman()

# ---------- Floyd-Warshall helpers ----------
FP0 = {'0': (40, 20), '1': (160, 20), '2': (160, 140), '3': (40, 140)}
FE = [('0', '1', 3), ('1', '2', 1), ('2', '3', 2), ('0', '3', 9), ('3', '0', 1)]
def fw_init():
    n = 4; D = [[INF] * n for _ in range(n)]
    for i in range(n): D[i][i] = 0
    for a, b, w in FE: D[int(a)][int(b)] = w
    return D

def floyd():
    S = Story('sm4-', 0, 'Four vertices, five arrows, and a 4 by 4 distance matrix starting with the direct edges. For k = 0 to 3 every pair i, j checks whether going through k is cheaper. Via 0: 3 to 1 becomes 4. Via 1: 0 to 2 becomes 4, 3 to 2 becomes 5. Via 2: 0 to 3 becomes 6, 1 to 3 becomes 3. Via 3: row 1 and 2 learn to reach 0.',
              'FLOYD-WARSHALL · EVERY PAIR, "MAY I GO THROUGH k?"')
    lines = ['for k in range(n):', '  for i in range(n):', '    for j in range(n):', '      d[i][j] = min(d[i][j],', '                    d[i][k] + d[k][j])']
    code = S.setcode(0, 40, lines)
    GX, GY = code.w + 40, 60
    P = {k: (GX + x, GY + y) for k, (x, y) in FP0.items()}
    draw_graph(S, P, FE, {('0', '1'): (0, -12), ('1', '2'): (12, 0), ('2', '3'): (0, 12), ('0', '3'): (-20, 0), ('3', '0'): (20, 0)}, shift={('0', '3'): (-6, 0), ('3', '0'): (6, 0)})
    # parallel edges 0->3 and 3->0 overlap: acceptable since labels sit on both sides
    MX, MY, C = GX + 240, 60, 42
    S.f.w = int(MX + 4 * C + 20)
    for i in range(4):
        S.static(T(MX - 14, MY + i * C + 26, str(i), MU, mono=True) + T(MX + i * C + C / 2, MY - 8, str(i), MU, mono=True))
    D = fw_init()
    def cellxy(i, j): return MX + j * C, MY + i * C
    for i in range(4):
        for j in range(4):
            S.at(.6 + (i * 4 + j) * .03, box(*cellxy(i, j), ds(D[i][j]), 'plain', C - 4, C - 6), key='c%d%d' % (i, j))
    S.sx, S.sy = 0, max(40 + code.h(), MY + 4 * C) + 30
    t = 1.8; S.say(t, 'start: direct edges only, ∞ = no edge', 0, PT)
    t += 1.4
    for k in range(4):
        S.line(t, 0)
        hl = R(MX - 2, MY + k * C - 2, 4 * C, C - 2, 'none', PT, 6, 2) + R(MX + k * C - 2, MY - 2, C, 4 * C - 2, 'none', PT, 6, 2)
        S.at(t, hl, hide=t + 3.2 if k < 3 else None, key='hl')
        S.at(t, ring(*P[str(k)]), key='kr')
        S.say(t, 'k = %d: may i → j go through %d?' % (k, k), 0, PT)
        t += .9; ch = []
        for i in range(4):
            for j in range(4):
                if D[i][k] + D[k][j] < D[i][j]: ch.append((i, j, D[i][j], D[i][k] + D[k][j]))
        for i, j, old, new in ch:
            S.line(t, 3)
            x, y = cellxy(i, j)
            S.at(t, bring(x, y, C - 4, C - 6), hide=t + 1.1)
            S.say(t, 'd[%d][%d] = min(%s, %d + %d) = %d' % (i, j, ds(old), D[i][k], D[k][j], new), 1, TX)
            S.at(t + .4, box(x, y, new, 'seen', C - 4, C - 6), key='c%d%d' % (i, j))
            D[i][j] = new; t += 1.3
        if not ch: S.say(t, 'no pair improves', 1, MU); t += 1.0
        t += .3
    S.off('kr', t); S.off('hl', t)
    for i in range(4):
        for j in range(4): S.at(t + .1, box(*cellxy(i, j), ds(D[i][j]), 'ans', C - 4, C - 6), key='c%d%d' % (i, j))
    assert D == [[0, 3, 4, 6], [4, 0, 1, 3], [3, 6, 0, 2], [1, 4, 5, 0]]
    S.say(t + .3, '✓ all 16 shortest distances · n³ = 64 checks', 0, TG, True)
    S.say(t + .3, '', 1)
    return S.render(S.sy + 30), D
figs['m4'], FW = floyd()

# ---------- 1.5 cost ----------
def cost():
    S = Story('sm5-', 720, 'Work for one graph with V = 1,000 vertices and E = 5,000 edges, on a log scale. BFS: V + E, six thousand. Dijkstra: (V + E) log V, about sixty thousand. Bellman-Ford: V times E, five million. Floyd-Warshall: V cubed, one billion.',
              'COST · V = 1,000 VERTICES · E = 5,000 EDGES · LOG SCALE')
    V, E = 1000, 5000
    rows = [('BFS', 'V + E', V + E), ('Dijkstra', '(V+E) log V', round((V + E) * math.log2(V))), ('Bellman-Ford', 'V · E', V * E), ('Floyd-Warshall', 'V³', V ** 3)]
    X0, Y0, BW, RH = 210, 50, 460, 46
    px = lambda v: X0 + math.log10(v) / 9 * BW
    ax = L(X0, Y0 + 4 * RH + 2, X0 + BW, Y0 + 4 * RH + 2, MU, 1.2)
    for e in range(0, 10, 3): ax += L(px(10 ** e), Y0 + 4 * RH + 2, px(10 ** e), Y0 + 4 * RH + 6, MU) + T(px(10 ** e), Y0 + 4 * RH + 20, '10%s' % '⁰¹²³⁴⁵⁶⁷⁸⁹'[e], FA, cls='sv-s', mono=True) + L(px(10 ** e), Y0 - 6, px(10 ** e), Y0 + 4 * RH, 'var(--rule)', 1, '2 4')
    S.static(ax)
    t = .4
    for k, (nm, f, v) in enumerate(rows):
        y = Y0 + k * RH
        S.at(t, T(0, y + 18, nm, TX, 'start', bold=True) + T(110, y + 18, f, MU, 'start', mono=True))
        # bar grows one decade at a time
        dec = math.log10(v)
        segs = int(math.ceil(dec)); x = X0
        for s in range(segs):
            x2 = px(min(10 ** (s + 1), v))
            S.at(t + .3 + s * .18, R(X0, y + 4, x2 - X0, 22, TG if k == 1 else it('.35'), 'none', 0), key='bar%d' % k)
            x = x2
        S.at(t + .3 + segs * .18, T(px(v) + 8 if k < 3 else px(v) - 8, y + 20, '{:,}'.format(v), TG if k == 1 else TX, 'start' if k < 3 else 'end', mono=True, bold=True,) if k < 3 else T(px(v) - 8, y + 20, '{:,}'.format(v), 'var(--on-fill)', 'end', mono=True, bold=True))
        t += .6 + segs * .18 + .5
    S.at(t + .2, T(X0 + BW, Y0 + 4 * RH + 44, 'Dijkstra is the default · Floyd-Warshall only when V is small', TG, 'end', bold=True))
    return S.render(Y0 + 4 * RH + 56)
figs['m5'] = cost()

# ---------- 2.1 signal to everyone (743) ----------
def network():
    S = Story('sp1-', 680, 'Same graph as Dijkstra above. After one Dijkstra from S every vertex has its distance: S 0, B 1, A 3, C 4, T 7. A signal sent from S reaches everyone when the farthest vertex hears it. A ring scans the distances and ans follows the largest: 7 at T.',
              'SIGNAL TO EVERYONE · ONE DIJKSTRA, THEN TAKE THE LARGEST dist')
    X0, Y0 = 40, 50
    P = {k: (X0 + x, Y0 + y) for k, (x, y) in POS.items()}
    draw_graph(S, P, E1, WOFF)
    S.at(1.0, chip(480, 14, 'time for all?', a='start'))
    dist = {'S': 0, 'B': 1, 'A': 3, 'C': 4, 'T': 7}
    t = 1.8
    for k, v in enumerate(['S', 'B', 'A', 'C', 'T']):
        S.at(t + k * .35, bdg(P, v, dist[v]) + node(*P[v], v, 'seen'), key='n' + v)
    S.sx, S.sy = 480, 110
    S.say(t, 'run Dijkstra from S', 0, PT)
    t += 2.4
    best = None; rp = []; ap = []
    order = ['S', 'A', 'B', 'C', 'T']
    for v in order:
        rx, ry = P[v]
        if not rp: rp = [(0, rx - P['S'][0], ry - P['S'][1])]; rt0 = t
        else: rp.append((t, rx - P['S'][0], ry - P['S'][1]))
        if best is None or dist[v] > dist[best]:
            S.say(t + .3, 'dist[%s] = %d → largest' % (v, dist[v]), 0, TX)
            if best is None: ap = [(0, 0, 0)]; at0 = t + .5
            else: ap.append((t + .5, P[v][0] - P['S'][0], P[v][1] - P['S'][1]))
            best = v
        else:
            S.say(t + .3, 'dist[%s] = %d ≤ %d → keep' % (v, dist[v], dist[best]), 0, MU)
        t += 1.3
    S.path(ring(*P['S']), rp, rt0, hide=t)
    S.path(arrow(P['S'][0] - 30, P['S'][1] + 32, P['S'][0] - 13, P['S'][1] + 15, PT, 1.6, None, 6) + T(P['S'][0] - 34, P['S'][1] + 46, 'ans', PT, mono=True, bold=True), ap, at0, hide=t)
    S.at(t, node(*P['T'], 'T', 'ans'), key='nT')
    S.at(t + .2, T(P['T'][0], P['T'][1] + NR + 16, '✓ found', TG, mono=True, bold=True))
    S.say(t + .3, 'answer = max dist = 7', 0, TG, True)
    S.at(t + .3, T(480, 136, '∞ anywhere → return −1', MU, 'start'))
    return S.render(Y0 + 230)
figs['p1'] = network()

# ---------- 2.2 grid, path cost = max step ----------
def effort():
    H = [[1, 2, 2], [3, 8, 2], [5, 3, 5]]
    n = 3
    S = Story('sp2-', 700, 'A 3 by 3 grid of heights. A path costs its largest single climb. Dijkstra pops cells by their cost: each cell shows the best effort found. The bottom-right corner is reached with effort 2 along 1, 3, 5, 3, 5, avoiding the 8.',
              'GRID · PATH COST = THE BIGGEST SINGLE CLIMB')
    X0, Y0, C = 20, 46, 56
    cx = lambda j: X0 + j * (C + 8); cy = lambda i: Y0 + i * (C + 8)
    for i in range(n):
        for j in range(n):
            S.at(.2 + (i * n + j) * .05, box(cx(j), cy(i), H[i][j], 'plain', C, C), key='c%d%d' % (i, j))
    S.at(1.0, R(cx(2) - 4, cy(2) - 4, C + 8, C + 8, 'none', TG, 8, 1.4, '4 3'))
    S.at(1.0, chip(260, 46, 'least effort to the corner', a='start'))
    S.sx, S.sy = 260, 100
    S.static(T(260, 176, 'big number: height', MU, 'start') + T(260, 196, 'small number: best effort so far', MU, 'start'))
    eff = {(0, 0): 0}; h = [(0, 0, 0)]; done = set(); par = {}
    t = 1.8
    def tag(i, j, e, tt, col=TG):
        S.at(tt, R(cx(j) + C - 22, cy(i) + 3, 19, 15, 'var(--bg)', 'none', 3) + T(cx(j) + C - 5, cy(i) + 14, str(e), col, 'end', cls='sv-s', mono=True, bold=True), key='e%d%d' % (i, j))
    tag(0, 0, 0, t)
    rp = []
    while h:
        e, i, j = heapq.heappop(h)
        if (i, j) in done: continue
        done.add((i, j))
        if not rp: rp = [(0, 0, 0)]; rt0 = t
        else: rp.append((t, cx(j) - cx(0), cy(i) - cy(0)))
        S.say(t, 'pop (%d, %d) with effort %d' % (i, j, e), 0, MID)
        S.at(t + .3, box(cx(j), cy(i), H[i][j], 'seen', C, C), key='c%d%d' % (i, j))
        if (i, j) != (2, 2): tag(i, j, e, t + .3)
        if (i, j) == (2, 2): fin = t + .8; break
        t += .8
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n and (a, b) not in done:
                ne = max(e, abs(H[a][b] - H[i][j]))
                if ne < eff.get((a, b), INF):
                    eff[(a, b)] = ne; par[(a, b)] = (i, j); heapq.heappush(h, (ne, a, b))
                    S.say(t, 'to (%d, %d): max(%d, |%d − %d|) = %d' % (a, b, e, H[a][b], H[i][j], ne), 1, TX)
                    tag(a, b, ne, t)
                    t += .9
        t += .2
    S.path(bring(cx(0), cy(0), C, C), rp, rt0, hide=fin, d=.4)
    path = [(2, 2)]
    while path[-1] != (0, 0): path.append(par[path[-1]])
    assert eff[(2, 2)] == 2
    for i in range(n):
        for j in range(n):
            if (i, j) not in path:
                S.at(fin, box(cx(j), cy(i), H[i][j], 'grey', C, C), key='c%d%d' % (i, j)); S.off('e%d%d' % (i, j), fin)
    S.at(fin, box(cx(2), cy(2), H[2][2], 'ans', C, C), key='c22')
    S.at(fin + .1, T(cx(2) + C - 5, cy(2) + 14, '2', 'var(--on-fill)', 'end', cls='sv-s', mono=True, bold=True)); S.off('e22', fin)
    S.say(fin + .3, '✓ effort 2 · the path goes around the 8', 0, TG, True)
    S.say(fin + .3, 'same loop, only "d + w" became "max(d, w)"', 1, MU)
    return S.render(max(Y0 + 3 * (C + 8) + 10, 210))
figs['p2'] = effort()

# ---------- 2.3 at most k stops ----------
def kstops():
    P0 = {'0': (20, 120), '1': (150, 30), '2': (300, 30), '3': (430, 120)}
    E = [('0', '1', 100), ('1', '2', 100), ('2', '3', 100), ('1', '3', 300), ('0', '3', 500)]
    S = Story('sp3-', 720, 'Cities 0 to 3, find the cheapest flight 0 to 3 with at most 1 stop, so at most 2 flights. Bellman-Ford runs exactly 2 rounds, each from a copy of the previous prices. Round 1: city 1 costs 100, city 3 costs 500. Round 2: city 2 costs 200, city 3 drops to 400 via 1. The 300 route needs 2 stops and is never reached.',
              'AT MOST k STOPS · BELLMAN-FORD FOR EXACTLY k + 1 ROUNDS · k = 1')
    X0, Y0 = 30, 50
    P = {k: (X0 + x, Y0 + y) for k, (x, y) in P0.items()}
    draw_graph(S, P, E, {('0', '1'): (-14, -6), ('1', '2'): (0, -12), ('2', '3'): (14, -6), ('1', '3'): (0, -12), ('0', '3'): (0, 12)})
    S.at(1.0, goal_ring(*P['3']))
    S.at(1.0, chip(530, 14, 'cheapest 0 → 3', a='start'))
    S.sx, S.sy = X0, Y0 + 200
    dist = {'0': 0, '1': INF, '2': INF, '3': INF}
    t = 1.8
    for k in P0: S.at(t, bdg(P, k, ds(dist[k]), PT), key='b' + k)
    t += 1.0
    for rnd in (1, 2):
        prev = dict(dist)
        S.say(t, 'round %d: flights = %d · read prices from the copy' % (rnd, rnd), 0, PT)
        t += .8
        for a, b, w in E:
            if prev[a] == INF: continue
            S.at(t, edge(P[a], P[b], MID, 2.4, True), hide=t + 1.0)
            if prev[a] + w < dist[b]:
                old = dist[b]; dist[b] = prev[a] + w
                S.say(t, '%d + %d = %d < %s → price[%s] = %d' % (prev[a], w, dist[b], ds(old), b, dist[b]), 1, TX)
                S.at(t + .4, bdg(P, b, dist[b]), key='b' + b)
            else:
                S.say(t, '%d + %d = %d ≥ %s → keep' % (prev[a], w, prev[a] + w, ds(dist[b])), 1, MU)
            t += 1.3
    assert dist['3'] == 400
    S.at(t, edge(P['2'], P['3'], 'var(--ghost)', 1.4, True, '4 3'))
    S.at(t, T(P['2'][0] + 28, P['2'][1] + 4, '0→1→2→3 = 2 stops ✗', GH, 'start', cls='sv-s', mono=True))
    S.at(t + .3, edge(P['0'], P['1'], TG, 2.6, True) + edge(P['1'], P['3'], TG, 2.6, True))
    S.at(t + .3, node(*P['3'], '3', 'ans'), key='n3')
    S.at(t + .4, T(P['3'][0], P['3'][1] + NR + 16, '✓ found', TG, mono=True, bold=True))
    S.say(t + .5, 'price = 400 via 1 · 1 stop', 0, TG, True)
    S.say(t + .5, 'no copy → round 1 could chain 0→1→2 and break the limit', 1, MU)
    return S.render(S.sy + 30)
figs['p3'] = kstops()

# ---------- 2.4 all pairs + threshold ----------
def threshold():
    D = FW; th = 3
    S = Story('sp4-', 640, 'The finished Floyd-Warshall matrix. Threshold 3: for each city count the others within distance 3. City 0 reaches 1, city 1 reaches 2, city 2 reaches 2, city 3 reaches 1. Cities 0 and 3 tie with the fewest; the larger id, 3, is the answer.',
              'EVERY PAIR · FLOYD-WARSHALL, THEN COUNT PER ROW · threshold = 3')
    MX, MY, C = 40, 50, 46
    for i in range(4):
        S.static(T(MX - 16, MY + i * C + 26, str(i), MU, mono=True) + T(MX + i * C + C / 2, MY - 8, str(i), MU, mono=True))
        for j in range(4):
            S.at(.2 + (i * 4 + j) * .03, box(MX + j * C, MY + i * C, D[i][j], 'plain', C - 4, C - 6), key='c%d%d' % (i, j))
    S.static(T(MX + 4 * C + 16, MY - 8, 'count', MU, 'start'))
    S.at(1.0, chip(300, 50, 'fewest within 3', a='start'))
    S.sx, S.sy = 300, 110
    t = 1.8; best = None; rp = []; cnts = []
    for i in range(4):
        if not rp: rp = [(0, 0, 0)]; rt0 = t
        else: rp.append((t, 0, i * C))
        c = 0
        for j in range(4):
            if i == j: S.at(t + .2, box(MX + j * C, MY + i * C, 0, 'grey', C - 4, C - 6), key='c%d%d' % (i, j)); continue
            if D[i][j] <= th: c += 1; S.at(t + .2, box(MX + j * C, MY + i * C, D[i][j], 'seen', C - 4, C - 6), key='c%d%d' % (i, j))
            else: S.at(t + .2, box(MX + j * C, MY + i * C, D[i][j], 'grey', C - 4, C - 6), key='c%d%d' % (i, j))
        cnts.append(c)
        S.at(t + .5, T(MX + 4 * C + 30, MY + i * C + 25, str(c), PT, mono=True, bold=True))
        S.say(t + .5, 'city %d: %d others within 3' % (i, c), 0, TX)
        t += 1.5
    S.path(R(MX - 4, MY - 4, 4 * C, C - 6 + 8, 'none', MID, 8, 2.2), rp, rt0, hide=t, d=.4)
    ans = max(i for i in range(4) if cnts[i] == min(cnts))
    assert ans == 3 and cnts == [1, 2, 2, 1]
    S.at(t, R(MX + 4 * C + 16, MY + ans * C, 28, C - 6, TG, TG, 6) + T(MX + 4 * C + 30, MY + ans * C + 25, str(cnts[ans]), 'var(--on-fill)', mono=True, bold=True))
    S.say(t + .2, '✓ answer = city 3 (tie → larger id)', 0, TG, True)
    return S.render(MY + 4 * C + 14)
figs['p4'] = threshold()

os.makedirs('/tmp/dsa', exist_ok=True)
json.dump(figs, open('/tmp/dsa/shortest-path.json', 'w'))
print({k: len(v) for k, v in figs.items()})

# ---------- splice ----------
PAGE = 'content/01-dsa/04-algorithms/shortest-path/index.html'
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
old = subprocess.run(['git', 'show', 'HEAD:' + PAGE], cwd=ROOT, capture_output=True, text=True).stdout
probs = re.search(r'<div class="probs">(.*?)</div>', old, re.S).group(1)
A = {m.group(1): m.group(0) for m in re.finditer(r'<a href="[^"]+" target="_blank" rel="noopener"><i>(\d+)</i>.*?</a>', probs)}
assert sorted(A) == sorted(['743', '1631', '1514', '787', '778', '1334'])
def pl(*ids): return '<div class="probs">\n' + ''.join('    %s\n' % A[i] for i in ids) + '  </div>'

def sub(sid, num, title, skey, fig, sig=None, pr=None):
    s = '  <div class="subsec" id="%s">\n    <h3 class="ssh"><b>%s</b>%s</h3>\n    <p class="skey">%s</p>\n%s\n' % (sid, num, title, skey, figs[fig])
    if sig: s += '    <p class="sig">Signals: %s</p>\n    %s\n' % (sig, pr)
    return s + '  </div>\n'

art = '''<article class="doc" id="art-sp" data-title="Shortest path" data-tag="Technique" data-blurb="Dijkstra pops the cheapest vertex first; Bellman-Ford handles negative edges; Floyd-Warshall gives every pair.">
        <header class="hero">
  <p class="eyebrow">DSA · algorithms</p>
  <h1>Shortest <em>path</em></h1>
  <p class="lede">Weighted edges: BFS with the queue swapped for a heap.</p>
</header>

<section id="sp-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Three algorithms, three assumptions — <em>read the weights before picking one</em>.</p>
''' + sub('sp-s1-1', '1.1', 'Dijkstra', 'Pop the <em>cheapest</em> vertex; once popped, its distance is final.', 'm1') \
    + sub('sp-s1-2', '1.2', 'Why negative edges break Dijkstra', 'A later negative edge can beat a distance <em>already locked</em>.', 'm2') \
    + sub('sp-s1-3', '1.3', 'Bellman-Ford', 'No heap: relax <em>every edge</em>, <span class="mth"><var>V</var> − 1</span> times.', 'm3') \
    + sub('sp-s1-4', '1.4', 'Floyd-Warshall', 'Every pair at once: for each <var>k</var>, <em>is going through k cheaper?</em>', 'm4') \
    + sub('sp-s1-5', '1.5', 'Cost', 'Dijkstra <span class="mth">O((<var>V</var> + <var>E</var>) <b class="fn">log</b> <var>V</var>)</span> — <em>the default</em>; the other two only when needed.', 'm5') + '''</section>

<section id="sp-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Patterns</h2></div>
  <p class="key">Same loops every time — <em>only what you read off the result changes</em>.</p>
''' + sub('sp-s2-1', '2.1', 'Time for a signal to reach everyone', 'One Dijkstra, then the answer is the <em>largest</em> distance.', 'p1',
          '"minimum cost" · "time for all nodes" · weighted edge list', pl('743')) \
    + sub('sp-s2-2', '2.2', 'Different path cost', 'Swap <code>d + w</code> for <em>max</em> or <em>product</em> — the loop stays.', 'p2',
          'a grid of heights · "minimum effort" · "maximum probability"', pl('1631', '1514', '778')) \
    + sub('sp-s2-3', '2.3', 'At most k stops', 'Bellman-Ford for exactly <em><var>k</var> + 1 rounds</em>, from a copy.', 'p3',
          '"at most k stops" · "within k edges"', pl('787')) \
    + sub('sp-s2-4', '2.4', 'Every pair of cities', 'Floyd-Warshall the matrix, then <em>read each row</em>.', 'p4',
          '"for every city" · <span class="mth"><var>V</var> ≤ 400</span>', pl('1334')) + '''</section>

''' + REPLAY + '''

<footer>DSA · shortest path · Dijkstra, Bellman-Ford, Floyd-Warshall. BFS and DFS are in the <a href="../graph-bfs-dfs-topo/index.html">Graph</a> lesson.</footer>

      </article>'''
splice(os.path.join(ROOT, PAGE), art)
print('spliced', PAGE)
