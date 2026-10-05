"""Figures for content/01-dsa/03-data-structures/union-find (visual-first DSA lesson).
Writes /tmp/dsa/union-find.json  {figure key: <figure> html}.
Groups are drawn as trees: arrow child -> parent, roots on top. When a link changes, the
whole forest is laid out again and the nodes SLIDE to their new places (treekit_tbu.Scene)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from treekit_tbu import *

W = 760
CY = 40


def probe(name='x', side='l'):
    return lambda x, y: ring(x, y) + plabel(x, y, name, side, NR + 5)


class DSU:
    """Parent array on a Scene. ids = node keys in display order; lab = key -> text."""
    def __init__(s, sc, ids, lab, x0, y0, dx=48, dy=54, t=.2, gap=.5, sizes=False, by_size=False):
        s.sc, s.ids, s.x0, s.y0, s.dx, s.dy, s.gap = sc, list(ids), x0, y0, dx, dy, gap
        s.p = {u: u for u in ids}; s.sz = {u: 1 for u in ids}; s.by_size = by_size
        pos = s.layout()
        for k, u in enumerate(ids): sc.node(u, lab[u], t + k * .05, *pos[u])
        s.steps = 0
    def roots(s): return [u for u in s.ids if s.p[u] == u]
    def layout(s):
        kids = {u: [] for u in s.ids}
        for u in s.ids:
            if s.p[u] != u: kids[s.p[u]].append(u)
        pos = {}; slot = [0.0]
        def go(u, d):
            if not kids[u]:
                x = s.x0 + slot[0] * s.dx; slot[0] += 1
            else:
                xs = [go(k, d + 1) for k in kids[u]]; x = (xs[0] + xs[-1]) / 2
            pos[u] = (x, s.y0 + d * s.dy); return x
        for r in s.roots():
            go(r, 0); slot[0] += s.gap
        return pos
    def set_parent(s, t, u, v):
        """p[u] = v at time t: old arrow fades, nodes slide, new arrow appears after the slide."""
        if s.p[u] != u: s.sc.edge_off(t, u, s.p[u], 'up')
        s.p[u] = v
        pos = s.layout()
        for w in s.ids: s.sc.place(t, w, *pos[w])
        if u != v: s.sc.edge_on(t + Scene.D, u, v, 'up')
    def link_now(s, t, u, v):
        """initial state, no animation of the move: place everything at t."""
        s.p[u] = v
        pos = s.layout()
        for w in s.ids: s.sc.ptl[w] = [(s.sc.ptl[w][0][0], *pos[w])]
        s.sc.edge_on(t, u, v, 'up')
    def find_path(s, x):
        path = [x]
        while s.p[path[-1]] != path[-1]: path.append(s.p[path[-1]])
        return path
    def find(s, x): return s.find_path(x)[-1]
    def pos(s, u, t): return s.sc.pos(u, t)


# ---------------------------------------------------------------- 1.1 mental model
def model_fig():
    sc = Scene('uf-m1-', W, 'Six elements 0 to 5, each first its own group. Arrows point from a child to its parent: 1 and 2 hang under 0, 4 under 3. The parent list below holds exactly these arrows. To ask whether 2 and 4 are in the same group, climb from each to its root: 2 reaches 0, 4 reaches 3. Different roots, so different groups.',
               'EACH GROUP IS A TREE · SAME ROOT = SAME GROUP', 3.2)
    ids = list(range(6))
    d = DSU(sc, ids, {u: str(u) for u in ids}, 70, 70, 60, 60, gap=.6)
    ax, ay = 70, 232
    sc.static(T(ax - 12, ay + 20, 'p', MU, 'end', mono=True))
    for u in ids:
        sc.show(ocell(ax + u * 44, ay, u), .3 + u * .05)
        sc.show(T(ax + u * 44 + 17, ay + 46, str(u), FA, cls='sv-s', mono=True), .3)
    sc.slot('s', 380, ay + 20)
    t = 1.4
    for (u, v) in ((1, 0), (2, 1), (4, 3)):
        sc.say('s', t, 'p[%d] = %d' % (u, v), PT)
        d.set_parent(t, u, v)
        sc.show(ocell(ax + u * 44, ay, v, 'vis'), t + .3)
        t += 1.5
    for k, (x, nm) in enumerate(((2, 'a'), (4, 'b'))):
        path = d.find_path(x)
        key = 'p' + nm
        sc.mover(key, probe(nm, 'l' if nm == 'a' else 'r'), t, *d.pos(x, t))
        sc.say('s', t, 'find(%d): climb to the root' % x, PT); t += .8
        for u in path[1:]:
            sc.move(key, t, *d.pos(u, t)); t += .7
        sc.hide(key, t)
        r = path[-1]
        sc.over(r, lambda X, Y, r=r: node(X, Y, r, 'fill'), t)
        sc.say('s', t, 'root of %d = %d' % (x, r), TG, True); t += 1.2
    sc.say('s', t, '✓ roots 0 ≠ 3 → 2 and 4 are in different groups', TG, True)
    return sc.render(ay + 56)


# ---------------------------------------------------------------- 2.1 find
def find_fig():
    lines = ['def find(x):', '    while p[x] != x:', '        x = p[x]', '    return x']
    sc = Scene('uf-p1-', W, 'find(4) on the chain 4 → 3 → 2 → 1 → 0. Each step reads p[x] and moves x to the parent. After four steps p[0] = 0, so 0 is the root. The cost is the depth of the start node.',
               'FIND · FOLLOW THE ARROWS UP UNTIL A NODE POINTS AT ITSELF', 3.2)
    code = sc.add_code(0, CY, lines, 220)
    X0 = code.w + 60
    ids = list(range(5))
    d = DSU(sc, ids, {u: str(u) for u in ids}, X0 + 120, 46, 50, 48)
    for u in range(1, 5): d.link_now(.2, u, u - 1)
    sy = 46 + 4 * 48 + 40
    sc.slot('s', X0, sy); sc.slot('v', X0, sy + 22)
    sc.show(goal_ring(*d.pos(4, 0)), .8, hide=1.6)
    t = 1.6
    sc.line(t, 0); sc.mover('x', probe(), t, *d.pos(4, t)); sc.say('s', t, 'x = 4', PT); t += 1.0
    x = 4; steps = 0
    while d.p[x] != x:
        sc.line(t, 1); sc.say('v', t, 'p[%d] = %d ≠ %d → climb' % (x, d.p[x], x), TX); t += .7
        sc.line(t, 2); x = d.p[x]; steps += 1
        sc.move('x', t, *d.pos(x, t)); sc.say('s', t, 'x = %d · steps = %d' % (x, steps), PT); t += 1.1
    sc.line(t, 1); sc.say('v', t, 'p[0] = 0 → root', TX); t += .8
    sc.line(t, 3); sc.hide('x', t); sc.clear('v', t)
    sc.over(0, lambda X, Y: node(X, Y, 0, 'fill'), t)
    sc.show(T(d.pos(0, t)[0] + 26, d.pos(0, t)[1] + 5, '✓ root', TG, 'start', mono=True, bold=True), t + .2)
    sc.say('s', t + .3, 'root = 0 · %d steps = depth of 4' % steps, TG, True)
    return sc.render(max(code.y + code.h(), sy + 32))


# ---------------------------------------------------------------- 2.2 union
def union_fig():
    lines = ['def union(a, b):', '    ra, rb = find(a), find(b)', '    if ra == rb: return False', '    p[rb] = ra', '    return True']
    sc = Scene('uf-p2-', W, 'Two groups: 0 with 1 and 2, and 3 with 4. union(2, 4) finds both roots, 0 and 3. They differ, so p[3] = 0: the whole tree of 3 slides under 0. Then union(1, 4) finds root 0 twice: same root, so it returns False, the two were already in one group.',
               'UNION · FIND BOTH ROOTS, HANG ONE ROOT UNDER THE OTHER', 3.2)
    code = sc.add_code(0, CY, lines, 250)
    X0 = code.w + 50
    ids = list(range(5))
    d = DSU(sc, ids, {u: str(u) for u in ids}, X0 + 30, 60, 52, 56, gap=1.2)
    for u, v in ((1, 0), (2, 0), (4, 3)): d.link_now(.2, u, v)
    sy = 60 + 3 * 56 + 30
    sc.slot('s', X0, sy); sc.slot('v', X0, sy + 22)
    t = 1.2
    for (a, b) in ((2, 4), (1, 4)):
        sc.line(t, 0); sc.say('s', t, 'union(%d, %d)' % (a, b), PT); t += .9
        sc.line(t, 1)
        ra, rb = d.find(a), d.find(b)
        sc.mover(('a', a), probe('ra', 'l'), t, *d.pos(a, t)); sc.move(('a', a), t + .5, *d.pos(ra, t))
        sc.mover(('b', a), probe('rb', 'r'), t, *d.pos(b, t)); sc.move(('b', a), t + .5, *d.pos(rb, t))
        sc.say('s', t, 'ra = find(%d) = %d · rb = find(%d) = %d' % (a, ra, b, rb), PT); t += 1.5
        sc.line(t, 2)
        if ra == rb:
            sc.say('v', t, 'ra == rb → already one group', TX); t += 1.0
            sc.hide(('a', a), t); sc.hide(('b', a), t)
            sc.over(ra, lambda X, Y: node(X, Y, 0, 'fill'), t)
            sc.say('s', t, 'return False', PT); sc.clear('v', t); t += .8
            break
        sc.say('v', t, '%d ≠ %d → link them' % (ra, rb), TX); t += .9
        sc.line(t, 3); sc.clear('v', t)
        sc.hide(('a', a), t); sc.hide(('b', a), t)
        sc.say('s', t, 'p[%d] = %d · tree of %d slides under %d' % (rb, ra, rb, ra), PT)
        d.set_parent(t + .2, rb, ra); t += 1.6
        sc.line(t, 4); sc.say('s', t, 'return True', PT); t += 1.2
    sc.say('s', t, '✓ one group of 5 · cost = two finds', TG, True)
    return sc.render(max(code.y + code.h(), sy + 32))


# ---------------------------------------------------------------- 2.3 path compression
def compress_fig():
    lines = ['def find(x):', '    if p[x] != x:', '        p[x] = find(p[x])', '    return p[x]']
    sc = Scene('uf-p3-', W, 'find(4) with path compression on the chain 4 → 3 → 2 → 1 → 0. The recursion climbs to the root 0 in four steps. On the way back, each node it passed is pointed straight at 0: 2, then 3, then 4 slide up to hang directly under the root. The next find(4) takes one step.',
               'PATH COMPRESSION · EVERY NODE CLIMBED PAST NOW POINTS AT THE ROOT', 3.2)
    code = sc.add_code(0, CY, lines, 240)
    X0 = code.w + 60
    ids = list(range(5))
    d = DSU(sc, ids, {u: str(u) for u in ids}, X0 + 60, 46, 54, 48)
    for u in range(1, 5): d.link_now(.2, u, u - 1)
    sy = 46 + 4 * 48 + 40
    sc.slot('s', X0, sy)
    t = 1.4
    sc.line(t, 0); sc.mover('x', probe(), t, *d.pos(4, t)); sc.say('s', t, 'find(4)', PT); t += .9
    for u in (3, 2, 1, 0):
        sc.line(t, 2); sc.move('x', t, *d.pos(u, t)); sc.say('s', t, 'climb to %d' % u, PT); t += .8
    sc.line(t, 3); sc.say('s', t, 'p[0] = 0 → root 0', PT)
    sc.over(0, lambda X, Y: node(X, Y, 0, 'fill'), t); t += 1.0
    sc.hide('x', t)
    for u in (2, 3, 4):
        sc.line(t, 2); sc.say('s', t, 'back in find(%d): p[%d] = 0' % (u, u), PT)
        d.set_parent(t, u, 0); t += 1.4
    sc.line(t, 3)
    sc.mover('y', probe(), t, *d.pos(4, t)); sc.say('s', t, 'next find(4)', PT); t += .8
    sc.move('y', t, *d.pos(0, t)); t += .9
    sc.hide('y', t)
    sc.say('s', t, '✓ 4 steps the first time · 1 step from now on', TG, True)
    return sc.render(max(code.y + code.h(), sy + 12))


# ---------------------------------------------------------------- 2.4 union by size
def size_fig():
    sc = Scene('uf-p4-', W, 'The same union on two copies: a group of four rooted at 0, and the single node 4. Left, without sizes, 0 is hung under 4 and the tree grows to height 3. Right, by size, the small tree 4 is hung under the big root 0, and the height stays 2.',
               'UNION BY SIZE · HANG THE SMALL TREE UNDER THE BIG ONE', 3.2)
    lab = {}
    ids = []
    for side in 'ab':
        for u in range(5): lab[side + str(u)] = str(u); ids.append(side + str(u))
    A = DSU(sc, ids[:5], {k: lab[k] for k in ids[:5]}, 60, 80, 50, 56, gap=1.3)
    B = DSU(sc, ids[5:], {k: lab[k] for k in ids[5:]}, 440, 80, 50, 56, gap=1.3)
    for D_, s in ((A, 'a'), (B, 'b')):
        for u in (1, 2, 3): D_.link_now(.2, s + str(u), s + '0')
    sc.static(T(40, 40, 'without size: p[0] = 4', MU, 'start', mono=True) + T(420, 40, 'by size: p[4] = 0', MU, 'start', mono=True))
    def badge(k, n): return lambda X, Y: R(X + 12, Y - 28, 34, 16, 'var(--bg)', 'none', 8) + R(X + 12, Y - 28, 34, 16, it('.12'), TG, 8, 1) + T(X + 29, Y - 16, 'sz %d' % n, TG, cls='sv-s', mono=True, bold=True)
    for k in ('a0', 'b0'): sc.top(k, badge(k, 4), .9, hide=None)
    for k in ('a4', 'b4'): sc.top(k, badge(k, 1), .9, hide=2.4)
    sc.slot('l', 40, 290); sc.slot('r', 420, 290)
    t = 2.4
    A.set_parent(t, 'a0', 'a4'); sc.say('l', t, 'big tree hangs under 4', PT)
    t += 2.0
    B.set_parent(t, 'b4', 'b0'); sc.say('r', t, 'small tree hangs under 0', PT)
    t += 2.0
    for k in ('a1', 'b4'):
        sc.over(k, lambda X, Y, k=k: node(X, Y, lab[k], 'vis'), t)
    sc.say('l', t, 'height 3 · deepest find: 2 steps', MU, True)
    sc.say('r', t, '✓ height 2 · deepest find: 1 step', TG, True)
    return sc.render(300)


# ---------------------------------------------------------------- 2.5 cost
def measure(n, comp, size):
    """worst input for a plain DSU: union(0, i) for i = 1..n-1 with the naive link p[ra] = rb,
    so the old root always goes under the new single node and node 0 sinks ever deeper."""
    p = list(range(n)); sz = [1] * n; hops = [0]; finds = [0]
    def find(x):
        finds[0] += 1
        path = []
        while p[x] != x:
            path.append(x); x = p[x]; hops[0] += 1
        if comp:
            for y in path: p[y] = x
        return x
    for i in range(1, n):
        ra, rb = find(0), find(i)
        if ra == rb: continue
        if size and sz[ra] > sz[rb]: ra, rb = rb, ra   # small (ra) goes under big (rb)
        p[ra] = rb; sz[rb] += sz[ra]
    return hops[0] / finds[0]


def cost_fig():
    f = Fig('uf-p5-', W, 'Measured average climb steps per find, on the worst input for a plain DSU: union(0, i) for every i, which keeps hanging the old root under a single new node, so node 0 sinks one level deeper each time. Without either optimisation the average grows with n, about n / 4 steps per find. With path compression and union by size it stays below one step for every n.',
            'COST · AVERAGE STEPS PER find, MEASURED ON THE WORST INPUT', 3.2)
    ns = [250, 500, 1000, 2000, 4000]
    plain = [measure(n, False, False) for n in ns]
    both = [measure(n, True, True) for n in ns]
    assert plain[-1] > 900 and max(both) < 1.0
    f.slot('s', 70, 312)
    px, py = graph(f, 70, 50, 560, 210, 4000, 1000, [
        (lambda n: n / 4, 'neither: ≈ n / 4', MU, 2, 1300),
        (lambda n: 0.5, 'both: < 1 step', TG, 2.6, 3000)], .4, xt=(1000, 2000, 3000, 4000), yt=(250, 500, 750, 1000), xl='n', yl='steps')
    t = 3.0
    for k, (n, a, b) in enumerate(zip(ns, plain, both)):
        f.show(circ(px(n), py(a), 4, MID, 'none', 0) + circ(px(n), py(b), 4, MID, 'none', 0), t + k * .5)
        f.say('s', t + k * .5, 'n = %d → %.0f steps vs %.2f' % (n, a, b), PT)
    t += 3.0
    f.say('s', t, '✓ both optimisations: almost O(1) per operation · missing them: O(n)', TG, True)
    return f.render(322)


# ---------------------------------------------------------------- 3.1 counting groups
def count_fig():
    lines = ['groups = n', 'for a, b in edges:', '    if union(a, b):', '        groups -= 1']
    sc = Scene('uf-q1-', W, 'Six people, four friend links. groups starts at 6. union(0, 1), union(2, 3) and union(4, 5) each join two groups, so groups drops to 3. union(1, 3) joins the groups of 0 and 2: groups = 2. The answer is two friend circles.',
               'COUNT GROUPS · START AT n, EACH SUCCESSFUL UNION REMOVES ONE', 3.2)
    code = sc.add_code(0, CY, lines, 220)
    X0 = code.w + 40
    ids = list(range(6))
    d = DSU(sc, ids, {u: str(u) for u in ids}, X0 + 20, 64, 54, 56, gap=.5)
    E = [(0, 1), (2, 3), (4, 5), (1, 3)]
    ex = 0
    sc.static(T(ex, CY + code.h() + 30, 'edges', MU, 'start', mono=True))
    for k, (a, b) in enumerate(E): sc.show(ocell(ex + k * 52, CY + code.h() + 40, '%d-%d' % (a, b), 'plain', 46, 28), .3)
    sy = 64 + 3 * 56 + 24
    sc.slot('s', X0, sy); sc.slot('g', X0, sy + 22)
    t = 1.2; g = 6
    sc.line(t, 0); sc.say('g', t, 'groups = 6', PT, True); t += 1.0
    for k, (a, b) in enumerate(E):
        sc.line(t, 1); sc.show(cring(ex + k * 52, CY + code.h() + 40, 46, 28), t, hide=t + 2.6)
        ra, rb = d.find(a), d.find(b)
        if d.sz[ra] < d.sz[rb]: ra, rb = rb, ra
        sc.line(t + .5, 2); sc.say('s', t + .5, 'union(%d, %d): roots %d, %d → link' % (a, b, d.find(a), d.find(b)), PT)
        d.set_parent(t + .9, rb, ra); d.sz[ra] += d.sz[rb]
        g -= 1
        sc.line(t + 1.6, 3); sc.say('g', t + 1.6, 'groups = %d' % g, PT, True)
        sc.show(ocell(ex + k * 52, CY + code.h() + 40, '%d-%d' % (a, b), 'vis', 46, 28), t + 1.6)
        t += 2.8
    sc.line(t, 1); sc.clear('s', t)
    for r in d.roots(): sc.over(r, lambda X, Y, r=r: node(X, Y, r, 'fill'), t)
    sc.say('g', t + .2, '✓ groups = 2 · one root per group', TG, True)
    return sc.render(max(CY + code.h() + 80, sy + 32))


# ---------------------------------------------------------------- 3.2 redundant edge
def redundant_fig():
    lines = ['for a, b in edges:', '    if not union(a, b):', '        return [a, b]']
    sc = Scene('uf-q2-', W, 'Edges 1-2, 1-3, 2-3. union(1, 2) and union(1, 3) succeed and build one group rooted at 1. union(2, 3) finds root 1 for both ends: they are already connected, so this edge closes a cycle. It is the redundant edge.',
               'REDUNDANT EDGE · A UNION THAT FAILS CLOSES A CYCLE', 3.2)
    code = sc.add_code(0, CY, lines, 220)
    X0 = code.w + 60
    ids = [1, 2, 3]
    d = DSU(sc, ids, {u: str(u) for u in ids}, X0 + 60, 70, 70, 60, gap=.6)
    E = [(1, 2), (1, 3), (2, 3)]
    ey = CY + code.h() + 40
    sc.static(T(0, ey - 10, 'edges', MU, 'start', mono=True))
    for k, (a, b) in enumerate(E): sc.show(ocell(k * 52, ey, '%d-%d' % (a, b), 'plain', 46, 28), .3)
    sy = 70 + 2 * 60 + 40
    sc.slot('s', X0, sy); sc.slot('v', X0, sy + 22)
    t = 1.2
    for k, (a, b) in enumerate(E):
        sc.line(t, 0); sc.show(cring(k * 52, ey, 46, 28), t, hide=t + 2.4)
        ra, rb = d.find(a), d.find(b)
        sc.line(t + .5, 1); sc.say('s', t + .5, 'union(%d, %d): roots %d, %d' % (a, b, ra, rb), PT)
        if ra != rb:
            d.set_parent(t + 1.0, rb, ra)
            sc.show(ocell(k * 52, ey, '%d-%d' % (a, b), 'vis', 46, 28), t + 1.2)
            sc.say('v', t + 1.0, 'different → link', TX); t += 2.6
        else:
            for u in (a, b):
                sc.mover(('c', u), probe('a' if u == a else 'b', 'l' if u == a else 'r'), t + .6, *d.pos(u, t))
                sc.move(('c', u), t + 1.2, *d.pos(ra, t)); sc.hide(('c', u), t + 2.4)
            sc.say('v', t + 1.0, 'same root %d → already connected' % ra, TX)
            t += 2.6
            sc.line(t, 2); sc.clear('v', t)
            sc.show(ocell(k * 52, ey, '%d-%d' % (a, b), 'fill', 46, 28), t)
            sc.say('s', t + .2, '✓ redundant edge = [%d, %d]' % (a, b), TG, True)
    return sc.render(max(ey + 40, sy + 32))


# ---------------------------------------------------------------- 3.3 Kruskal
def kruskal_fig():
    P = {'A': (60, 70), 'B': (200, 50), 'C': (170, 170), 'D': (320, 150), 'E': (330, 260)}
    E = sorted([('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 3), ('C', 'D', 4), ('B', 'D', 5), ('D', 'E', 6), ('C', 'E', 7)], key=lambda e: e[2])
    f = Fig('uf-q3-', W, 'Kruskal on five points. Edges are tried from cheapest to most expensive. A-B 1 and B-C 2 are taken. A-C 3 is skipped: A and C already share a root. C-D 4 is taken, B-D 5 skipped, D-E 6 taken. Four edges join all five points; total cost 13.',
            'MINIMUM SPANNING TREE · CHEAPEST EDGE FIRST, SKIP IT IF union FAILS', 3.2)
    GX = 380
    def at(k): return (P[k][0] + GX, P[k][1])
    def wl(a, b, w):
        (x1, y1), (x2, y2) = at(a), at(b)
        return R((x1 + x2) / 2 - 9, (y1 + y2) / 2 - 9, 18, 16, 'var(--sunk)', 'none', 4) + T((x1 + x2) / 2, (y1 + y2) / 2 + 3, str(w), MU, cls='sv-s', mono=True)
    for a, b, w in E:
        f.show(edge(at(a), at(b), NR) + wl(a, b, w), .3)
    for k, u in enumerate(P): f.show(node(*at(u), u), .2 + k * .05)
    f.static(T(0, 40, 'edges, cheapest first', MU, 'start', mono=True))
    ey = lambda k: 50 + k * 34
    for k, (a, b, w) in enumerate(E): f.show(ocell(0, ey(k), '%s-%s  %d' % (a, b, w), 'plain', 90, 28), .5 + k * .05)
    f.slot('s', 110, 300); f.slot('v', 110, 322)
    p = {u: u for u in P}
    def find(x):
        while p[x] != x: x = p[x]
        return x
    t = 1.6; cost = 0; taken = 0
    f.mover('e', lambda x, y: cring(x, y, 90, 28), t, 0, ey(0))
    for k, (a, b, w) in enumerate(E):
        if taken == 4: break
        if k: f.move('e', t, 0, ey(k))
        ra, rb = find(a), find(b)
        f.say('s', t, 'find(%s) = %s · find(%s) = %s' % (a, ra, b, rb), PT)
        (x1, y1), (x2, y2) = at(a), at(b)
        if ra != rb:
            p[rb] = ra; cost += w; taken += 1
            f.say('v', t + .5, 'different → take it · cost = %d' % cost, TX)
            f.show(edge((x1, y1), (x2, y2), NR, TG, 3) + wl(a, b, w), t + .7)
            for u in (a, b): f.show(node(*at(u), u, 'vis'), t + .7)
            f.show(ocell(0, ey(k), '%s-%s  %d' % (a, b, w), 'vis', 90, 28), t + .7)
        else:
            f.say('v', t + .5, 'same root → would close a cycle, skip', TX)
            f.show(ocell(0, ey(k), '%s-%s  %d' % (a, b, w), 'grey', 90, 28), t + .7)
            f.show(edge((x1, y1), (x2, y2), NR, 'var(--rule)', 1.4, '3 4') + wl(a, b, w), t + .7)
        t += 1.9
    f.hide('e', t); f.clear('v', t)
    for k in range(len(E)):
        if k >= 6: f.show(ocell(0, ey(k), '%s-%s  %d' % E[k], 'grey', 90, 28), t)
    for u in P: f.show(node(*at(u), u, 'fill'), t)
    f.say('s', t + .2, '✓ 4 edges join 5 points · total cost %d' % cost, TG, True)
    assert cost == 13
    return f.render(332)


# ---------------------------------------------------------------- 3.4 merging by key
def accounts_fig():
    acc = [('Alice', ['a@x', 'b@x']), ('Alice', ['b@x', 'c@x']), ('Bob', ['d@x'])]
    sc = Scene('uf-q4-', W, 'Three accounts: 0 Alice with a and b, 1 Alice with b and c, 2 Bob with d. A dict maps each email to the first account that used it. Account 1 meets b, already owned by 0, so union(1, 0) and account 1 slides under 0. The result: accounts 0 and 1 are one person, 2 is another.',
               'MERGE BY KEY · A DICT MAPS EACH KEY TO A NUMBER, THEN UNION', 3.2)
    for i, (nm, em) in enumerate(acc):
        y = 50 + i * 40
        sc.show(T(0, y + 19, str(i), FA, 'start', mono=True) + T(18, y + 19, nm, TX, 'start', mono=True, bold=True), .2 + i * .1)
        for j, e in enumerate(em): sc.show(ocell(70 + j * 56, y, e, 'plain', 50, 28), .2 + i * .1)
    DX = 320
    sc.static(T(DX, 40, 'owner = {}', MU, 'start', mono=True))
    d = DSU(sc, [0, 1, 2], {0: '0', 1: '1', 2: '2'}, 560, 70, 60, 60, gap=.6)
    sc.static(T(540, 40, 'accounts', MU, 'start', mono=True))
    sc.slot('s', 0, 210)
    owner = {}; t = 1.2; row = 0
    for i, (nm, em) in enumerate(acc):
        for j, e in enumerate(em):
            y = 50 + i * 40
            sc.show(cring(70 + j * 56, y, 50, 28), t, hide=t + 1.6)
            if e not in owner:
                owner[e] = i
                sc.show(T(DX, 66 + row * 24, '%s → %d' % (e, i), TX, 'start', mono=True), t + .4); row += 1
                sc.say('s', t, 'new email %s → owner[%s] = %d' % (e, e, i), PT); t += 1.6
            else:
                o = owner[e]
                sc.say('s', t, '%s already owned by %d → union(%d, %d)' % (e, o, i, o), PT)
                sc.show(ocell(70 + j * 56, y, e, 'vis', 50, 28), t + .4)
                d.set_parent(t + .8, i, o); t += 2.2
    for r in d.roots(): sc.over(r, lambda X, Y, r=r: node(X, Y, r, 'fill'), t)
    sc.say('s', t + .2, '✓ 2 people: Alice = accounts 0 + 1 · Bob = account 2', TG, True)
    return sc.render(222)


# ---------------------------------------------------------------- 3.5 two sides
def sides_fig():
    sc = Scene('uf-q5-', W, 'Possible bipartition of 1, 2, 3 with dislikes 1-2, 2-3, 1-3. Each person x has a twin x\' meaning the opposite side. A dislike a-b does union(a, b\') and union(b, a\'). After 1-2 and 2-3, person 1 and 3 share a side. The dislike 1-3 then checks find(1) against find(3): equal, so two people who must be apart are together. Not possible.',
               'TWO SIDES · x AND ITS TWIN x\' = "THE OPPOSITE SIDE OF x"', 3.2)
    ids = ['1', '2', '3', "1'", "2'", "3'"]
    d = DSU(sc, ids, {u: u for u in ids}, 300, 70, 52, 56, gap=.5)
    D = [('1', '2'), ('2', '3'), ('1', '3')]
    sc.static(T(0, 40, 'dislikes', MU, 'start', mono=True))
    for k, (a, b) in enumerate(D): sc.show(ocell(0, 50 + k * 36, '%s-%s' % (a, b), 'plain', 46, 28), .3)
    sc.slot('s', 0, 250); sc.slot('v', 0, 272)
    t = 1.2
    for k, (a, b) in enumerate(D):
        sc.show(cring(0, 50 + k * 36, 46, 28), t, hide=t + 3.0)
        if k == 2:
            ra, rb = d.find(a), d.find(b)
            for u, nm in ((a, 'a'), (b, 'b')):
                sc.mover(('c', u), probe(nm, 'l' if nm == 'a' else 'r'), t, *d.pos(u, t))
                sc.move(('c', u), t + .6, *d.pos(ra, t)); sc.hide(('c', u), t + 2.0)
            sc.say('s', t, 'check: find(1) = %s · find(3) = %s' % (ra, rb), PT)
            sc.say('v', t + .8, 'equal → 1 and 3 are on the same side', TX); t += 2.2
            sc.clear('v', t)
            for u in (a, b): sc.over(u, lambda X, Y, u=u: node(X, Y, u, 'fill'), t)
            sc.show(ocell(0, 50 + k * 36, '%s-%s' % (a, b), 'fill', 46, 28), t)
            sc.say('s', t + .2, '✓ conflict found: 1 and 3 must be apart → not possible', TG, True)
            break
        for (u, v) in ((a, b + "'"), (b, a + "'")):
            ru, rv = d.find(u), d.find(v)
            if d.sz[ru] < d.sz[rv]: ru, rv = rv, ru
            sc.say('s', t, "union(%s, %s)" % (u, v), PT)
            if ru != rv:
                d.set_parent(t + .3, rv, ru); d.sz[ru] += d.sz[rv]
            t += 1.5
        sc.show(ocell(0, 50 + k * 36, '%s-%s' % (a, b), 'vis', 46, 28), t - .3)
    return sc.render(282)


figs = {'m1': model_fig(), 'p1': find_fig(), 'p2': union_fig(), 'p3': compress_fig(), 'p4': size_fig(), 'p5': cost_fig(),
        'q1': count_fig(), 'q2': redundant_fig(), 'q3': kruskal_fig(), 'q4': accounts_fig(), 'q5': sides_fig()}
dump('union-find', figs)
print('ok', len(figs))
