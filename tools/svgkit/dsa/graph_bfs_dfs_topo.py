"""Figures for content/01-dsa/04-algorithms/graph-bfs-dfs-topo. Writes /tmp/dsa/graph-bfs-dfs-topo.json"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graph_bigo_kit import *
from collections import deque

figs = {}

# ---------- the shared example graph ----------
POS = {'A': (20, 95), 'B': (110, 35), 'C': (110, 155), 'D': (210, 35), 'E': (210, 155), 'F': (300, 95)}
EDGES = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('C', 'E'), ('D', 'F'), ('E', 'F')]
ADJ = {k: sorted([b for a, b in EDGES if a == k] + [a for a, b in EDGES if b == k]) for k in POS}

def ekey(u, v): return tuple(sorted((u, v)))

def traverse(pre, kind, caption, aria):
    """kind = 'bfs' (queue, dist) or 'dfs' (stack, visit order). Target F."""
    if kind == 'bfs':
        lines = ['q, dist = deque([s]), {s: 0}', 'while q:', '    u = q.popleft()', '    if u == t: return dist[u]',
                 '    for v in adj[u]:', '        if v not in dist:', '            dist[v] = dist[u] + 1', '            q.append(v)']
        LP, LT, LF, LI, LS, LA = 2, 3, 4, 5, 6, 7
    else:
        lines = ['st, seen = [s], {s}', 'while st:', '    u = st.pop()', '    if u == t: return True',
                 '    for v in adj[u]:', '        if v not in seen:', '            seen.add(v)', '            st.append(v)']
        LP, LT, LF, LI, LS, LA = 2, 3, 4, 5, 6, 7
    S = Story(pre, 0, aria, caption)
    code = S.setcode(0, 40, lines)
    X0, Y0 = code.w + 40, 40
    P = {k: (X0 + x, Y0 + y) for k, (x, y) in POS.items()}
    W = int(X0 + 360)
    S.f.w = W
    # 1. data: edges then nodes
    for i, (a, b) in enumerate(EDGES): S.at(.2 + i * .05, edge(P[a], P[b]))
    for i, k in enumerate(POS): S.at(.3 + i * .08, node(*P[k], k), key='n' + k)
    # 2. goal on the data
    S.at(1.1, goal_ring(*P['F']))
    gx, gy = P['F']
    S.path(chip(gx, gy - 46, 'target = F'), [(0, 0, 0), (2.4, X0 + 50 - gx, 6 - (gy - 46))], 1.1)
    # frontier row
    FY = Y0 + 200; FX = X0 + 62; CW = 34
    S.static(T(X0, FY + 21, 'queue' if kind == 'bfs' else 'stack', MU, 'start', mono=True))
    S.sx, S.sy = X0, FY + 76
    sx = lambda k: FX + k * (CW + 6)
    # 3. start
    t = 3.0
    S.line(t, 0)
    S.at(t, node(*P['A'], 'A', 'seen'), key='nA')
    if kind == 'bfs': S.at(t + .2, badge(*P['A'], 0), key='bA')
    S.at(t + .2, box(sx(0), FY, 'A', 'plain', CW, 30), key='s0')
    S.say(t, 'start at s = A', 0, PT)
    q = ['A']; dist = {'A': 0}; seen = {'A'}; order = 0
    head = 0                         # bfs: index of first live slot
    top_pts = [(0, 0, 0)]; ring_pts = []; nslot = 1; slotval = {0: 'A'}
    live = [0]                       # live slot indices
    t += 1.4
    ptr_pts = [(0, 0, 0)]
    found_t = None
    while True:
        # pop
        S.line(t, 1); S.line(t + .4, LP)
        if kind == 'bfs': k = live.pop(0)
        else: k = live.pop()
        u = slotval[k]
        S.at(t + .4, box(sx(k), FY, u, 'grey', CW, 30), key='s%d' % k)
        if kind == 'dfs': S.off('s%d' % k, t + 1.0)
        rx, ry = P[u]
        if not ring_pts: ring_pts = [(0, rx - P['A'][0], ry - P['A'][1])]; ring_t0 = t + .4
        else: ring_pts.append((t + .4, rx - P['A'][0], ry - P['A'][1]))
        order += 1
        if kind == 'dfs': S.at(t + .6, badge(*P[u], '#%d' % order, PT), key='b' + u)
        S.say(t + .4, '%s → u = %s' % ('popleft' if kind == 'bfs' else 'pop', u), 0, MID)
        S.say(t + .4, '', 1)
        # pointer under next frontier item
        t += 1.0
        S.line(t, LT)
        if u == 'F':
            S.say(t, 'u == t → reached F', 1, TX)
            found_t = t + .6; break
        S.say(t, '%s ≠ F → look at neighbours' % u, 1, TX)
        t += .8
        for v in ADJ[u]:
            S.line(t, LF)
            S.at(t, edge(P[u], P[v], MID, 2.4), hide=t + .9)
            S.line(t + .35, LI)
            if v in seen:
                S.say(t + .35, 'v = %s: already %s → skip' % (v, 'in dist' if kind == 'bfs' else 'seen'), 1, MU)
                t += 1.0; continue
            seen.add(v)
            S.line(t + .8, LS)
            if kind == 'bfs':
                dist[v] = dist[u] + 1
                S.say(t + .35, 'v = %s: new → dist[%s] = %d + 1 = %d' % (v, v, dist[u], dist[v]), 1, TX)
                S.at(t + .8, badge(*P[v], dist[v]), key='b' + v)
            else:
                S.say(t + .35, 'v = %s: new → mark seen, push' % v, 1, TX)
            S.at(t + .8, node(*P[v], v, 'seen'), key='n' + v)
            S.line(t + 1.2, LA)
            # push into a slot
            if kind == 'bfs': k2 = nslot; nslot += 1
            else: k2 = (live[-1] + 1) if live else 0
            slotval[k2] = v; live.append(k2)
            S.at(t + 1.2, box(sx(k2), FY, v, 'plain', CW, 30), key='s%d' % k2)
            t += 1.8
        t += .2
    # head/top pointer: under the slot that will be popped next (drawn as a path from slot 0)
    # rebuild from the recorded order is simpler: show a label beside the row instead
    S.path(ring(*P['A']), ring_pts, ring_t0, hide=found_t)
    # finish
    S.at(found_t, node(*P['F'], 'F', 'ans'), key='nF')
    S.at(found_t + .2, T(P['F'][0], P['F'][1] + NR + 16, '✓ found', TG, mono=True, bold=True))
    if kind == 'bfs':
        path = ['A', 'B', 'D', 'F']
        for a, b in zip(path, path[1:]): S.at(found_t + .4, edge(P[a], P[b], TG, 2.6))
        S.say(found_t + .5, 'dist[F] = 3 · the fewest edges', 0, TG, True)
    else:
        path = ['A', 'C', 'E', 'F']
        for a, b in zip(path, path[1:]): S.at(found_t + .4, edge(P[a], P[b], TG, 2.6))
        S.say(found_t + .5, 'reached F after %d pops · dives A → C → E → F' % order, 0, TG, True)
    S.say(found_t + .5, '', 1)
    return S.render(max(code.y + code.h(), S.sy + 30) + 8)

figs['m1'] = traverse('gm1-', 'bfs', 'BFS · A QUEUE · TAKE FROM THE FRONT',
    'Six vertices A to F, target F. BFS starts at A with a queue. It pops A and pushes B and C at distance 1, pops B and pushes D at distance 2, pops C and pushes E at distance 2, then D pushes F at distance 3. Popping F returns 3, the fewest edges. The highlighted code line follows each step.')
figs['m2'] = traverse('gm2-', 'dfs', 'DFS · A STACK · TAKE FROM THE BACK',
    'Same graph, target F. DFS uses a stack: it pops A, pushes B and C, then pops C, the newest, pushes D and E, pops E, pushes F and pops F. It dives A, C, E, F and reaches F after four pops, leaving B and D waiting.')

# ---------- 1.3  O(V + E) ----------
def cost():
    S = Story('gm3-', 0, 'Full BFS over the same graph. Each vertex is popped once: six pops. Each edge is checked once from each end: fourteen checks. Six plus fourteen is V plus 2E, so the cost is O(V + E).',
              'O(V + E) · EVERY VERTEX ONCE, EVERY EDGE TWICE')
    X0, Y0 = 20, 40
    P = {k: (X0 + x, Y0 + y) for k, (x, y) in POS.items()}
    S.f.w = 640
    for i, (a, b) in enumerate(EDGES): S.at(.2 + i * .05, edge(P[a], P[b]))
    for i, k in enumerate(POS): S.at(.3 + i * .08, node(*P[k], k), key='n' + k)
    CX = X0 + 380
    S.static(T(CX, 70, 'vertex pops', MU, 'start') + T(CX, 120, 'edge checks', MU, 'start'))
    S.num(1.2, CX + 100, 72, 0, 'cv')
    S.num(1.2, CX + 100, 122, 0, 'ce')
    t = 2.0; seen = {'A'}; q = deque(['A']); pops = 0; checks = 0
    S.at(t - .4, node(*P['A'], 'A', 'seen'), key='nA')
    ring_pts = []
    while q:
        u = q.popleft(); pops += 1
        rx, ry = P[u]
        if not ring_pts: ring_pts = [(0, rx - P['A'][0], ry - P['A'][1])]
        else: ring_pts.append((t, rx - P['A'][0], ry - P['A'][1]))
        S.num(t, CX + 100, 72, pops, 'cv')
        t += .5
        for v in ADJ[u]:
            checks += 1
            (x1, y1, x2, y2) = seg(P[u], P[v])
            mx, my = x1 + (x2 - x1) * .3, y1 + (y2 - y1) * .3
            S.at(t, edge(P[u], P[v], MID, 2.4), hide=t + .35)
            S.at(t, circ(mx, my, 4, MID))
            S.num(t, CX + 100, 122, checks, 'ce')
            if v not in seen:
                seen.add(v); q.append(v)
                S.at(t + .1, node(*P[v], v, 'seen'), key='n' + v)
            t += .42
        t += .2
    S.path(ring(*P['A']), ring_pts, 2.0, hide=t)
    assert pops == 6 and checks == 2 * len(EDGES) == 14
    S.at(t + .2, R(CX - 8, 150, 236, 30, TG, TG, 8) + T(CX + 110, 170, '6 + 14 = V + 2E', 'var(--on-fill)', mono=True, bold=True))
    S.at(t + .6, T(CX - 8, 206, '→ O(V + E)', TG, 'start', bold=True))
    S.at(t + .6, T(CX - 8, 228, 'one dot = one edge check', MU, 'start'))
    return S.render(Y0 + 215)
figs['m3'] = cost()

# ---------- 2.1 islands ----------
def islands():
    G = [[1, 1, 0, 0, 1], [1, 0, 0, 0, 1], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]]
    lines = ['count = 0', 'for i, j in cells:', '    if g[i][j] == 1 and (i, j) not in seen:', '        count += 1', '        dfs(i, j)   # adds the island to seen']
    S = Story('gp1-', 0, 'A 4 by 5 grid of land 1 and water 0. A ring scans the cells row by row; water greys out. At the first unseen land cell count becomes 1 and DFS tints the whole island. The second island at the top right makes count 2, the single cell in the middle makes 3. Answer: 3 islands.',
              'COUNT ISLANDS · SCAN, AND FLOOD EACH NEW ISLAND')
    code = S.setcode(0, 40, lines)
    X0 = code.w + 40; Y0 = 44; C = 40; G_ = 6
    S.f.w = int(X0 + 5 * (C + G_) + 150)
    cx = lambda j: X0 + j * (C + G_); cy = lambda i: Y0 + i * (C - 4 + G_)
    for i in range(4):
        for j in range(5):
            S.at(.2 + (i * 5 + j) * .03, box(cx(j), cy(i), G[i][j], 'plain', C, 36), key='c%d%d' % (i, j))
    S.sx, S.sy = X0, Y0 + 4 * 42 + 30
    CX = X0 + 5 * (C + G_) + 18
    S.at(1.2, T(CX, Y0 + 20, 'count', MU, 'start'))
    S.num(1.2, CX + 50, Y0 + 21, 0, 'cnt')
    S.line(1.2, 0)
    t = 2.2; seen = set(); count = 0; ring_pts = []
    def flood(si, sj):
        st = [(si, sj)]; seen.add((si, sj)); out = []
        while st:
            i, j = st.pop(); out.append((i, j))
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = i + di, j + dj
                if 0 <= a < 4 and 0 <= b < 5 and G[a][b] == 1 and (a, b) not in seen:
                    seen.add((a, b)); st.append((a, b))
        return out
    for i in range(4):
        for j in range(5):
            if not ring_pts: ring_pts = [(0, 0, 0)]
            else: ring_pts.append((t, cx(j) - cx(0), cy(i) - cy(0)))
            S.line(t, 1); S.line(t + .15, 2)
            if G[i][j] == 1 and (i, j) not in seen:
                count += 1
                S.say(t + .3, 'g[%d][%d] = 1, not seen → new island' % (i, j), 0, TX)
                S.line(t + .7, 3)
                S.num(t + .7, CX + 50, Y0 + 21, count, 'cnt')
                S.line(t + 1.2, 4)
                cells = flood(i, j)
                for k, (a, b) in enumerate(cells):
                    S.at(t + 1.3 + k * .3, box(cx(b), cy(a), '#%d' % count, 'seen', C, 36), key='c%d%d' % (a, b))
                t += 1.6 + len(cells) * .3
            elif G[i][j] == 1:
                S.say(t + .3, 'g[%d][%d] already seen → skip' % (i, j), 0, MU)
                t += .7
            else:
                S.say(t + .3, 'g[%d][%d] = 0 water → skip' % (i, j), 0, MU)
                S.at(t + .3, box(cx(j), cy(i), 0, 'grey', C, 36), key='c%d%d' % (i, j))
                t += .38
    S.path(bring(cx(0), cy(0), C, 36), ring_pts, 2.2, hide=t, d=.25)
    assert count == 3
    S.at(t, R(CX - 4, Y0 + 2, 84, 28, TG, TG, 8) + T(CX + 38, Y0 + 21, 'count = 3', 'var(--on-fill)', mono=True, bold=True))
    S.say(t + .2, '✓ 3 islands · every cell looked at once → O(R · C)', 0, TG, True)
    return S.render(max(code.y + code.h(), S.sy + 14) + 10)
figs['p1'] = islands()

# ---------- 2.2 multi-source BFS ----------
def multi():
    R_, C_ = 4, 6
    src = [(0, 0), (3, 5)]; wall = {(1, 2), (2, 2), (1, 3)}
    lines = ['q = deque(all_sources)    # minute 0', 'while q:', '    i, j = q.popleft()', '    for a, b in around(i, j):',
             '        if fresh(a, b):', '            t[a][b] = t[i][j] + 1', '            q.append((a, b))']
    S = Story('gp2-', 0, 'Grid with two rotten sources at opposite corners and three empty cells. Both sources enter the queue at minute 0. Each layer the rot spreads one cell: minute 1, 2, 3, 4. The last fresh cells are reached at minute 4.',
              'MULTI-SOURCE BFS · ALL SOURCES START TOGETHER')
    code = S.setcode(0, 40, lines)
    X0 = code.w + 40; Y0 = 50; C = 38
    S.f.w = int(X0 + C_ * (C + 5) + 210)
    cx = lambda j: X0 + j * (C + 5); cy = lambda i: Y0 + i * (C + 5)
    for i in range(R_):
        for j in range(C_):
            if (i, j) in wall: S.static(R(cx(j), cy(i), C, C, 'none', 'var(--rule)', 6, 1, '3 3'))
            else: S.at(.2 + (i * C_ + j) * .02, box(cx(j), cy(i), '', 'plain', C, C), key='c%d%d' % (i, j))
    S.sx, S.sy = X0, Y0 + R_ * (C + 5) + 26
    # BFS by layers
    dist = {s: 0 for s in src}; layer = list(src); layers = [layer]
    while layer:
        nxt = []
        for (i, j) in layer:
            for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= a < R_ and 0 <= b < C_ and (a, b) not in wall and (a, b) not in dist:
                    dist[(a, b)] = dist[(i, j)] + 1; nxt.append((a, b))
        if nxt: layers.append(nxt)
        layer = nxt
    t = 1.3
    S.at(t, chip(X0 + C_ * (C + 5) + 20, 54, 'when is all reached?', a='start'))
    t = 2.2; S.line(t, 0)
    for s in src: S.at(t + .2, box(cx(s[1]), cy(s[0]), 0, 'ans', C, C), key='c%d%d' % s)
    S.say(t + .2, 'minute 0: both sources in the queue', 0, PT)
    t += 1.4
    last = layers[-1]
    for m, L_ in enumerate(layers[1:], 1):
        S.line(t, 1); S.line(t + .3, 2)
        par = layers[m - 1]
        g = ''.join(bring(cx(j), cy(i), C, C) for i, j in par)
        S.at(t + .3, g, hide=t + 1.6)
        S.say(t + .3, 'pop the %d cell%s of minute %d' % (len(par), '' if len(par) == 1 else 's', m - 1), 0, MID)
        S.line(t + .8, 3); S.line(t + 1.0, 4); S.line(t + 1.2, 5)
        for (i, j) in L_: S.at(t + 1.2, box(cx(j), cy(i), m, 'seen', C, C), key='c%d%d' % (i, j))
        S.say(t + 1.2, 'minute %d: %d new cell%s' % (m, len(L_), '' if len(L_) == 1 else 's'), 1, TX)
        S.line(t + 1.6, 6)
        for s in par: S.at(t + 1.7, box(cx(s[1]), cy(s[0]), dist[s], 'grey', C, C), key='c%d%d' % s)
        t += 2.4
    M = len(layers) - 1
    for (i, j) in last: S.at(t, box(cx(j), cy(i), M, 'ans', C, C), key='c%d%d' % (i, j))
    S.say(t + .2, '✓ all reached after %d minutes · one BFS for all sources' % M, 0, TG, True)
    S.say(t + .2, '', 1)
    return S.render(max(code.y + code.h(), S.sy + 30) + 8)
figs['p2'] = multi()

# ---------- 2.3 topological sort ----------
def topo():
    POSD = {'A': (20, 40), 'B': (20, 150), 'C': (130, 40), 'D': (130, 150), 'E': (240, 95), 'F': (330, 95)}
    ED = [('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'F')]
    lines = ['q = deque(v for v in V if indeg[v] == 0)', 'while q:', '    u = q.popleft()', '    order.append(u)', '    for v in adj[u]:',
             '        indeg[v] -= 1', '        if indeg[v] == 0: q.append(v)', 'return len(order) == n']
    S = Story('gp3-', 0, 'Six courses with arrows from prerequisite to course. In-degrees appear: A 0, B 0, C 2, D 1, E 2, F 1. A and B start the queue. Each pop goes to the order row and lowers the in-degree of its targets; a vertex reaching 0 joins the queue. The order comes out A B C D E F, all six placed, so there is no cycle.',
              'TOPOLOGICAL SORT · TAKE WHAT HAS NO PREREQUISITE LEFT')
    code = S.setcode(0, 40, lines)
    X0 = code.w + 40; Y0 = 62
    P = {k: (X0 + x, Y0 + y) for k, (x, y) in POSD.items()}
    S.f.w = int(X0 + 370)
    for i, (a, b) in enumerate(ED): S.at(.2 + i * .05, edge(P[a], P[b], RULE_HI, 1.4, True))
    for i, k in enumerate(POSD): S.at(.3 + i * .06, node(*P[k], k), key='n' + k)
    indeg = {k: sum(1 for a, b in ED if b == k) for k in POSD}
    adj = {k: [b for a, b in ED if a == k] for k in POSD}
    t = 1.2
    S.at(t, chip(X0 + 200, 14, 'goal: an order', a='start'))
    t = 2.0
    for k in POSD: S.at(t + .1, badge(*P[k], 'in %d' % indeg[k], PT), key='b' + k)
    S.sx, S.sy = X0, Y0 + 290
    S.say(t, 'count arrows into each vertex', 0, PT)
    QY = Y0 + 196; OY = Y0 + 232; CW = 32
    S.static(T(X0, QY + 20, 'queue', MU, 'start', mono=True) + T(X0, OY + 20, 'order', MU, 'start', mono=True))
    qx = lambda k: X0 + 60 + k * (CW + 6)
    t += 1.4; S.line(t, 0)
    q = deque(); nq = 0
    for k in POSD:
        if indeg[k] == 0:
            q.append((k, nq)); S.at(t + .2, box(qx(nq), QY, k, 'plain', CW, 28), key='q%d' % nq); nq += 1
    S.say(t, 'in 0: A and B → queue', 0, PT)
    t += 1.2; order = []; ring_pts = []
    while q:
        u, slot = q.popleft()
        S.line(t, 1); S.line(t + .3, 2); S.line(t + .5, 3)
        rx, ry = P[u]
        if not ring_pts: ring_pts = [(0, rx - P['A'][0], ry - P['A'][1])]; rt0 = t + .3
        else: ring_pts.append((t + .3, rx - P['A'][0], ry - P['A'][1]))
        S.at(t + .3, box(qx(slot), QY, u, 'grey', CW, 28), key='q%d' % slot)
        S.at(t + .5, box(qx(len(order)), OY, u, 'seen', CW, 28))
        S.at(t + .5, node(*P[u], u, 'seen'), key='n' + u)
        S.say(t + .3, 'pop %s → order' % u, 0, MID)
        order.append(u)
        t += 1.0
        for v in adj[u]:
            indeg[v] -= 1
            S.line(t, 4); S.line(t + .2, 5)
            S.at(t, edge(P[u], P[v], MID, 2.4, True), hide=t + 1.0)
            S.at(t + .3, badge(*P[v], 'in %d' % indeg[v], PT), key='b' + v)
            if indeg[v] == 0:
                S.line(t + .7, 6)
                q.append((v, nq)); S.at(t + .8, box(qx(nq), QY, v, 'plain', CW, 28), key='q%d' % nq); nq += 1
                S.say(t + .3, 'in[%s] → 0 → push %s' % (v, v), 1, TX)
            else:
                S.say(t + .3, 'in[%s] → %d, still waiting' % (v, indeg[v]), 1, MU)
            t += 1.3
        t += .2
    S.path(ring(*P['A']), ring_pts, rt0, hide=t)
    assert order == list('ABCDEF')
    S.line(t, 7)
    for k, u in enumerate(order): S.at(t + .2 + k * .08, box(qx(k), OY, u, 'ans', CW, 28))
    S.say(t + .4, '✓ 6 of 6 placed → no cycle', 0, TG, True)
    S.say(t + .4, '', 1)
    return S.render(max(code.y + code.h(), S.sy + 30) + 8)
figs['p3'] = topo()

# ---------- 2.4 implicit graph ----------
def implicit():
    S = Story('gp4-', 760, 'States are numbers, moves are plus 1 and times 2, start 1, target 10. BFS builds the graph level by level: 2; then 3 and 4; then 6, 5 and 8; repeats grey out. In level 4, 5 times 2 gives 10: found in 4 moves, 1 to 2 to 4 to 5 to 10.',
              'STATES AS VERTICES · MOVES "+1" AND "×2" · FROM 1 TO 10')
    CWb, CHb, DX, DY = 46, 30, 140, 42
    X0, Y0 = 30, 70
    S.at(1.0, chip(640, 0, 'target = 10', a='start'))
    lv = {0: [(1, None, None)]}
    seen = {1}; frontier = [1]; level = 0; found = None; par = {}
    while not found:
        level += 1; out = []
        for u in frontier:
            for op, v in (('+1', u + 1), ('×2', u * 2)):
                out.append((v, u, op, v in seen))
                if v not in seen: seen.add(v); par[v] = (u, op)
                if v == 10: found = level; break
            if found: break
        lv[level] = out; frontier = [v for v, _, _, d in out if not d]
    pos = {}
    def xy(L_, k): return X0 + L_ * DX, Y0 + k * DY
    t = 1.8
    for L_ in range(level + 1):
        S.static(T(X0 + L_ * DX + CWb / 2, 48, 'step %d' % L_, MU, cls='sv-s'))
    x, y = xy(0, 0); S.at(.4, box(x, y, 1, 'plain', CWb, CHb)); pos[1] = (x, y)
    S.sx, S.sy = X0, Y0 + 4 * DY + 36
    S.say(1.6, 'level 0: the start state', 0, PT)
    for L_ in range(1, level + 1):
        S.say(t, 'level %d: apply +1 and ×2 to every state of level %d' % (L_, L_ - 1), 0, PT)
        for k, (v, u, op, dup) in enumerate(lv[L_]):
            x, y = xy(L_, k); ux, uy = pos[u]
            S.at(t, bring(ux, uy, CWb, CHb), hide=t + .7)
            ln = L(ux + CWb, uy + CHb / 2, x, y + CHb / 2, 'var(--rule)' if dup else RULE_HI, 1.2)
            S.at(t + .2, ln + T((ux + CWb + x) / 2, (uy + y) / 2 + CHb / 2 - 4, op, GH if dup else MU, cls='sv-s', mono=True))
            if dup:
                S.at(t + .3, box(x, y, v, 'grey', CWb, CHb))
                S.say(t + .3, '%s %s = %d already seen → drop' % (u, op, v), 1, MU)
            else:
                S.at(t + .3, box(x, y, v, 'plain', CWb, CHb)); pos[v] = (x, y)
                S.say(t + .3, '%s %s = %d → new state' % (u, op, v), 1, TX)
            t += .9
        t += .3
    # finish: path
    path = [10]
    while path[-1] != 1: path.append(par[path[-1]][0])
    path = path[::-1]
    assert path == [1, 2, 4, 5, 10]
    for a, b in zip(path, path[1:]):
        (ax, ay), (bx, by) = pos[a], pos[b]
        S.at(t, L(ax + CWb, ay + CHb / 2, bx, by + CHb / 2, TG, 2.4))
    for v in path[:-1]: S.at(t, box(*pos[v], v, 'seen', CWb, CHb))
    S.at(t + .2, box(*pos[10], 10, 'ans', CWb, CHb))
    S.at(t + .3, T(pos[10][0] + CWb + 8, pos[10][1] + 20, '✓ found', TG, 'start', mono=True, bold=True))
    S.say(t + .4, '1 → 2 → 4 → 5 → 10 · 4 moves', 0, TG, True)
    S.say(t + .4, '', 1)
    return S.render(S.sy + 30)
figs['p4'] = implicit()

# ---------- 2.5 weighted edges ----------
def weighted():
    S = Story('gp5-', 640, 'Vertices S, A, B, T. A direct edge S to T costs 10; the path S A B T has three edges of cost 2. BFS returns the one-edge path, total 10. The cheapest path has more edges but costs 6. With different weights the queue must become a heap.',
              'WEIGHTED EDGES · FEWEST EDGES ≠ CHEAPEST')
    P = {'S': (40, 150), 'A': (170, 60), 'B': (330, 60), 'T': (460, 150)}
    E = [('S', 'A', 2), ('A', 'B', 2), ('B', 'T', 2), ('S', 'T', 10)]
    for i, (a, b, w) in enumerate(E): S.at(.2 + i * .05, edge(P[a], P[b]) + wlab(P[a], P[b], w, MU, (0, -12) if b != 'T' or a != 'S' else (0, 14)))
    for i, k in enumerate(P): S.at(.3 + i * .08, node(*P[k], k), key='n' + k)
    S.at(1.1, goal_ring(*P['T']))
    S.at(1.1, chip(560, 14, 'cheapest S → T'))
    S.sx, S.sy = 0, 218
    t = 2.4
    S.say(t, 'BFS (queue): fewest edges first', 0, PT)
    S.at(t + .6, edge(P['S'], P['T'], MID, 2.8), hide=t + 3.2)
    S.say(t + .6, 'S → T: 1 edge, cost 10', 1, MID)
    t += 3.4
    S.say(t, 'heap: cheapest total first', 0, PT)
    for k, (a, b) in enumerate((('S', 'A'), ('A', 'B'), ('B', 'T'))):
        S.at(t + .5 + k * .5, edge(P[a], P[b], TG, 2.8))
        S.at(t + .5 + k * .5, badge(*P[b], 2 * (k + 1)), key='b' + b)
    S.say(t + .5, 'S → A → B → T: 3 edges, cost 2 + 2 + 2 = 6', 1, TX)
    t += 2.4
    S.at(t, node(*P['T'], 'T', 'ans'), key='nT')
    S.at(t + .2, T(P['T'][0], P['T'][1] + NR + 16, '✓ found', TG, mono=True, bold=True))
    S.say(t + .3, 'cheapest = 6 < 10 · swap the queue for a heap: Dijkstra', 0, TG, True)
    return S.render(S.sy + 30)
figs['p5'] = weighted()

os.makedirs('/tmp/dsa', exist_ok=True)
json.dump(figs, open('/tmp/dsa/graph-bfs-dfs-topo.json', 'w'))
print({k: len(v) for k, v in figs.items()})

# ---------- splice into the page ----------
import subprocess
PAGE = 'content/01-dsa/04-algorithms/graph-bfs-dfs-topo/index.html'
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
old = subprocess.run(['git', 'show', 'HEAD:' + PAGE], cwd=ROOT, capture_output=True, text=True).stdout
probs = re.findall(r'<div class="probs">.*?</div>', old, re.S)
assert len(probs) == 5

def sub(sid, num, title, skey, fig, sig=None, pr=None):
    s = '  <div class="subsec" id="%s">\n    <h3 class="ssh"><b>%s</b>%s</h3>\n    <p class="skey">%s</p>\n%s\n' % (sid, num, title, skey, figs[fig])
    if sig: s += '    <p class="sig">Signals: %s</p>\n    %s\n' % (sig, pr)
    return s + '  </div>\n'

art = '''<article class="doc" id="art-graph" data-title="Graph — BFS, DFS, topo sort" data-tag="Technique" data-blurb="One loop with a box of waiting vertices: a queue gives BFS, a stack gives DFS.">
        <header class="hero">
  <p class="eyebrow">DSA · algorithms</p>
  <h1>Graph — BFS, DFS, topo <em>sort</em></h1>
  <p class="lede">One loop, one box of waiting vertices.</p>
</header>

<section id="graph-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Pop a vertex, push its unseen neighbours — <em>the box decides the order</em>.</p>
''' + sub('graph-s1-1', '1.1', 'BFS — a queue', 'Take from the <em>front</em>: the search spreads in rings, so the first hit has the fewest edges.', 'm1') \
    + sub('graph-s1-2', '1.2', 'DFS — a stack', 'Take from the <em>back</em>: the search dives down one branch before trying the next.', 'm2') \
    + sub('graph-s1-3', '1.3', 'O(V + E)', 'Each vertex is popped <em>once</em>, each edge checked <em>once from each end</em>.', 'm3') + '''</section>

<section id="graph-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Patterns</h2></div>
  <p class="key">Same loop every time — <em>only the start and the check change</em>.</p>
''' + sub('graph-s2-1', '2.1', 'Counting islands on a grid', 'Scan every cell; each unseen land cell is <em>a new island</em> to flood.', 'p1',
          'a <b>matrix</b> · "number of islands" · "largest region" · "flood fill"', probs[0]) \
    + sub('graph-s2-2', '2.2', 'Fewest steps from many sources', 'Push <em>every source</em> at minute 0, then run one BFS.', 'p2',
          '"fewest steps" · "shortest time" · every edge costs <b>the same</b>', probs[1]) \
    + sub('graph-s2-3', '2.3', 'Topological sort', 'Take a vertex once <em>nothing points into it</em> any more.', 'p3',
          '"prerequisite courses" · "order of execution" · "can it be completed"', probs[2]) \
    + sub('graph-s2-4', '2.4', 'Hidden graphs', 'A state is a vertex, a move is an edge — <em>then plain BFS</em>.', 'p4',
          'the problem <b>never says "graph"</b> · "states" and "moves" · fewest moves', probs[3]) \
    + sub('graph-s2-5', '2.5', 'Weighted edges', 'BFS counts edges, not cost — <em>different weights need a heap</em>.', 'p5',
          'each edge has <b>a different cost</b> → <a href="../shortest-path/index.html">Shortest path</a>', probs[4]) + '''</section>

''' + REPLAY + '''

<footer>DSA · graph · BFS, DFS and topological sort.</footer>

      </article>'''
splice(os.path.join(ROOT, PAGE), art)
print('spliced', PAGE)
