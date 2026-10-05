"""Figures for content/01-dsa/03-data-structures/tree-bst-traversal (visual-first DSA lesson).
Writes /tmp/dsa/tree-bst-traversal.json  {figure key: <figure> html}."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from treekit_tbu import *

W = 760
CY = 40           # code box top


def probe(name='node', side='l'):
    return lambda x, y: ring(x, y) + plabel(x, y, name, side, NR + 5)


def place_tree(spec, X0, y0, dx=46, dy=56, W=W):
    b = BT(spec, 0, y0, dx, dy)
    w = (len(b.n) - 1) * dx
    off = X0 + (W - X0 - w) / 2
    for n in b.n: n['x'] += off
    return b


def out_row(f, x, y, label='out'):
    f.static(T(x - 10, y + 20, label, MU, 'end', mono=True))
    return lambda k: (x + k * 40, y)


# ---------------------------------------------------------------- 1.2-1.4 DFS orders
def dfs_fig(pre, order, caption, aria):
    tpl = {'pre': ['def dfs(node):', '    if not node: return', '    out.append(node.val)', '    dfs(node.left)', '    dfs(node.right)'],
           'in': ['def dfs(node):', '    if not node: return', '    dfs(node.left)', '    out.append(node.val)', '    dfs(node.right)'],
           'post': ['def dfs(node):', '    if not node: return', '    dfs(node.left)', '    dfs(node.right)', '    out.append(node.val)']}[order]
    LN = {'pre': dict(e=2, l=3, r=4), 'in': dict(l=2, e=3, r=4), 'post': dict(l=2, r=3, e=4)}[order]
    f = Fig(pre, W, aria, caption, 3.2)
    code = f.add_code(0, CY, tpl, 250)
    X0 = code.w + 40
    b = place_tree((4, (2, 1, 3), (6, 5, 7)), X0, 70)
    t = b.draw(f, .2, .12)
    oy = 70 + 2 * 56 + 46
    cell = out_row(f, X0 + 60, oy)
    f.slot('s', X0 + 60 - 40, oy + 62)
    ev = []
    def go(i):
        if order == 'pre': ev.append(('e', i))
        if b.L(i) is not None: ev.append(('d', b.L(i), 'l')); go(b.L(i)); ev.append(('u', i, 'l'))
        if order == 'in': ev.append(('e', i))
        if b.Rr(i) is not None: ev.append(('d', b.Rr(i), 'r')); go(b.Rr(i)); ev.append(('u', i, 'r'))
        if order == 'post': ev.append(('e', i))
    go(b.root)
    t += .6
    f.line(t, 0); f.say('s', t, 'dfs(%d)' % b.v(b.root), PT)
    f.mover('p', probe(), t, *b.p(b.root)); t += 1.0
    out = []
    for e in ev:
        if e[0] == 'd':
            f.line(t, LN[e[2]]); f.move('p', t + .15, *b.p(e[1])); f.say('s', t, 'dfs(%d)  ↓ %s' % (b.v(e[1]), 'left' if e[2] == 'l' else 'right'), PT); t += .9
        elif e[0] == 'u':
            f.line(t, LN[e[2]]); f.move('p', t + .1, *b.p(e[1])); f.say('s', t, 'back to %d' % b.v(e[1]), MU); t += .8
        else:
            i = e[1]; f.line(t, LN['e'])
            f.show(node(*b.p(i), b.v(i), 'vis'), t + .1)
            f.show(ocell(*cell(len(out)), b.v(i), 'vis'), t + .25)
            out.append(b.v(i))
            f.say('s', t, 'out.append(%d)' % b.v(i), TG, True); t += 1.0
    f.hide('p', t); f.line(t, 0)
    for k, v in enumerate(out): f.show(ocell(*cell(k), v, 'fill'), t + .1 + k * .06)
    msg = {'pre': 'node before its children · root comes first', 'in': 'left · node · right → 1 2 3 4 5 6 7 sorted',
           'post': 'children before the node · root comes last'}[order]
    f.say('s', t + .3, '✓ ' + msg, TG, True)
    return f.render(max(code.y + code.h(), oy + 76) + 14)


# ---------------------------------------------------------------- 1.5 level order
def level_fig():
    lines = ['q = deque([root])', 'while q:', '    node = q.popleft()', '    out.append(node.val)', '    q.extend(node.left, node.right)']
    f = Fig('tb-m5-', W, 'Level order on the tree 4, 2, 6, 1, 3, 5, 7. A queue starts with the root. Each step pops the front node, appends it to out and pushes its children to the back. out fills 4 2 6 1 3 5 7, one level after another.',
            'LEVEL ORDER · A QUEUE VISITS ONE LEVEL AT A TIME', 3.2)
    code = f.add_code(0, CY, lines, 270)
    X0 = code.w + 40
    b = place_tree((4, (2, 1, 3), (6, 5, 7)), X0, 70)
    t = b.draw(f, .2, .12)
    qy = 70 + 2 * 56 + 40
    oy = qy + 46
    qx = X0 + 60
    f.static(T(qx - 10, qy + 20, 'q', MU, 'end', mono=True))
    cell = out_row(f, qx, oy)
    f.slot('s', qx - 40, oy + 62)
    t += .6
    q = [b.root]; qk = {}
    f.line(t, 0); f.mover(('q', b.root), lambda x, y, v=b.v(b.root): ocell(x, y, v), t, qx, qy)
    f.say('s', t, 'q = [4]', PT); t += 1.1
    out = []
    first = True
    while q:
        i = q.pop(0)
        f.line(t, 1); t += .5
        f.line(t, 2)
        f.mover('p', probe(), t, *b.p(i)) if first else f.move('p', t, *b.p(i)); first = False
        f.hide(('q', i), t + .4)
        for k, j in enumerate(q): f.move(('q', j), t + .4, qx + k * 40, qy)
        f.say('s', t, 'pop %d' % b.v(i), PT); t += 1.0
        f.line(t, 3); f.show(node(*b.p(i), b.v(i), 'vis'), t + .1); f.show(ocell(*cell(len(out)), b.v(i), 'vis'), t + .2)
        out.append(b.v(i)); f.say('s', t, 'out.append(%d)' % b.v(i), TG, True); t += .9
        kids = [c for c in (b.L(i), b.Rr(i)) if c is not None]
        if kids:
            f.line(t, 4)
            for c in kids:
                f.mover(('q', c), lambda x, y, v=b.v(c): ocell(x, y, v), t + .1, qx + len(q) * 40, qy); q.append(c)
            f.say('s', t, 'q = [%s]' % ', '.join(str(b.v(c)) for c in q), PT); t += 1.0
    f.line(t, 1); f.hide('p', t)
    for k, v in enumerate(out): f.show(ocell(*cell(k), v, 'fill'), t + .1 + k * .06)
    f.say('s', t + .3, '✓ level 0 · level 1 · level 2 → 4 | 2 6 | 1 3 5 7', TG, True)
    return f.render(max(code.y + code.h(), oy + 76) + 14)


# ---------------------------------------------------------------- 1.1 anatomy
def anatomy_fig():
    f = Fig('tb-m1-', W, 'A binary tree of seven nodes appears level by level, depth 0, 1, 2. The top node is the root. Every node has at most a left and a right child. Nodes with no children, 1, 3, 5 and 7, are leaves. Height is 3 levels.',
            'A BINARY TREE · EACH NODE HAS A LEFT AND A RIGHT CHILD', 3)
    X0 = 150
    b = place_tree((4, (2, 1, 3), (6, 5, 7)), X0, 70, 60, 64, W=620)
    for d in range(3):
        f.show(T(X0 - 30, 74 + d * 64, 'depth %d' % d, MU, 'end', mono=True), .2 + d * .5)
        for i in [k for k, n in enumerate(b.n) if n['d'] == d]:
            g = node(*b.p(i), b.v(i))
            if b.n[i]['par'] is not None: g = edge(b.p(b.n[i]['par']), b.p(i)) + g
            f.show(g, .3 + d * .5)
    t = 2.0
    rx, ry = b.p(b.root)
    f.show(ring(rx, ry) + plabel(rx, ry, 'root', 'r', NR + 5), t)
    f.slot('s', 150, 70 + 2 * 64 + 50)
    f.say('s', t, 'root: no parent', PT)
    t += 1.4
    x2, y2 = b.p(b.by(2))
    f.show(T(x2 - 34, y2 + 40, 'left', MU, 'middle', mono=True), t)
    x6, y6 = b.p(b.by(6))
    f.show(T(x6 + 34, y6 + 40, 'right', MU, 'middle', mono=True), t)
    f.say('s', t, 'child: left or right', PT); t += 1.6
    for k, v in enumerate((1, 3, 5, 7)):
        f.show(node(*b.p(b.by(v)), v, 'vis'), t + k * .25)
    f.say('s', t, 'leaf: no children', TG, True); t += 1.8
    f.show(L(40, 60, 40, 76 + 128, PT, 1.4) + L(34, 60, 46, 60, PT, 1.4) + L(34, 204, 46, 204, PT, 1.4), t)
    f.say('s', t, 'height = 3 levels', PT, True); t += 1.2
    f.show(node(rx, ry, 4, 'fill'), t)
    f.say('s', t + .1, '✓ 7 nodes · 4 leaves · height 3', TG, True)
    return f.render(70 + 2 * 64 + 62)


# ---------------------------------------------------------------- BST helpers
BST = (8, (3, 1, (6, 4, 7)), (10, None, (14, 13, None)))


def search_fig():
    lines = ['while node:', '    if t == node.val: return node', '    if t < node.val: node = node.left', '    else:            node = node.right', 'return None']
    f = Fig('tb-p1-', W, 'BST 8, 3, 10, 1, 6, 14, 4, 7, 13. The target 7 is marked. At 8, 7 is smaller: go left, the right subtree greys out. At 3, go right: 1 greys out. At 6, go right: 4 greys out. At 7: found in 4 steps, one node per level.',
            'SEARCH A BST · FIND 7 · SMALLER GOES LEFT, BIGGER GOES RIGHT', 3.2)
    code = f.add_code(0, CY, lines)
    X0 = code.w + 40
    b = place_tree(BST, X0, 74, 42, 52)
    t = b.draw(f, .2, .08)
    g = b.by(7); gx, gy = b.p(g)
    f.show(goal_ring(gx, gy), 1.2)
    f.mover('chip', lambda x, y: chip(x, y, 'target = 7', 'middle'), 1.2, gx, gy - 40)
    f.move('chip', 2.2, X0 + 60, 28)
    sy = 74 + 3 * 52 + 44
    f.slot('s', X0, sy); f.slot('v', X0, sy + 22)
    t = 3.4; i = b.root; steps = 0; first = True
    while True:
        steps += 1; v = b.v(i)
        f.line(t, 0)
        if first: f.mover('p', probe(), t, *b.p(i)); first = False
        else: f.move('p', t, *b.p(i))
        f.say('s', t, 'node = %d' % v, PT); t += .8
        f.line(t, 1)
        if v == 7:
            f.say('v', t, '7 == 7 → found', TG, True); t += .6; break
        right = 7 > v
        f.line(t + .7, 2 if not right else 3)
        f.say('v', t, '7 %s %d → go %s' % ('>' if right else '<', v, 'right' if right else 'left'), TX)
        drop = [i] + b.sub(b.L(i) if right else b.Rr(i))
        for k in drop: f.show(node(*b.p(k), b.v(k), 'grey'), t + 1.0)
        f.clear('v', t + 2.0)
        i = b.Rr(i) if right else b.L(i); t += 2.1
    f.hide('p', t); f.clear('v', t + .3)
    f.show(node(gx, gy, 7, 'fill'), t + .1)
    f.show(T(gx + 30, gy + 5, '✓ found', TG, 'start', mono=True, bold=True), t + .3)
    f.say('s', t + .4, 'found 7 · %d steps = one node per level · O(h)' % steps, TG, True)
    return f.render(max(code.y + code.h(), sy + 44))


def insert_fig():
    lines = ['def insert(node, v):', '    if not node: return Node(v)', '    if v < node.val:', '        node.left = insert(node.left, v)', '    else:', '        node.right = insert(node.right, v)', '    return node']
    f = Fig('tb-p2-', W, 'Insert 5 into the BST 8, 3, 10, 1, 6, 14, 4, 7, 13. At 8 go left, at 3 go right, at 6 go left, at 4 go right: the right child of 4 is empty, so the new node 5 is created there. Four comparisons, one per level.',
            'INSERT INTO A BST · WALK DOWN LIKE A SEARCH, ATTACH AT THE EMPTY SPOT', 3.2)
    code = f.add_code(0, CY, lines, 300)
    X0 = code.w + 30
    b = place_tree((8, (3, 1, (6, (4, None, 5), 7)), (10, None, (14, 13, None))), X0, 74, 40, 50)
    new = b.by(5)
    order = [k for k in b.sub(b.root) if k != new]
    t = b.draw(f, .2, .08, order)
    f.show(chip(X0 + 10, 28, 'insert 5'), 1.2)
    sy = 74 + 4 * 50 + 40
    f.slot('s', X0, sy); f.slot('v', X0, sy + 22)
    t = 2.4; i = b.root; first = True; steps = 0
    while i != new:
        v = b.v(i); steps += 1
        f.line(t, 0)
        if first: f.mover('p', probe(), t, *b.p(i)); first = False
        else: f.move('p', t, *b.p(i))
        f.say('s', t, 'node = %d' % v, PT); t += .7
        right = 5 > v
        f.line(t, 2); t += .5
        f.line(t, 5 if right else 3)
        f.say('v', t - .5, '5 %s %d → go %s' % ('>' if right else '<', v, 'right' if right else 'left'), TX)
        drop = [i] + b.sub(b.L(i) if right else b.Rr(i))
        for k in drop:
            if k != new: f.show(node(*b.p(k), b.v(k), 'grey'), t + .5)
        f.clear('v', t + 1.4)
        i = b.Rr(i) if right else b.L(i); t += 1.5
    x, y = b.p(new)
    f.move('p', t, x, y); f.line(t, 1)
    f.say('s', t, 'node = None → empty spot', PT); t += .9
    f.show(edge(b.p(b.n[new]['par']), (x, y)) + node(x, y, 5, 'fill'), t)
    f.hide('p', t + .2); f.line(t, 6)
    f.show(T(x + 28, y + 5, '✓ inserted', TG, 'start', mono=True, bold=True), t + .3)
    f.say('s', t + .4, 'new leaf under 4 · %d comparisons · O(h)' % steps, TG, True)
    return f.render(max(code.y + code.h(), sy + 44))


def delete_fig():
    lines = ['# node has two children', 's = node.right', 'while s.left:', '    s = s.left', 'node.val = s.val', 'remove(s)  # s has no left child']
    f = Fig('tb-p3-', W, 'Delete 3 from the BST. 3 has two children, so it cannot simply be cut out. Its successor is the smallest value on its right: step to 6, then left to 4, which has no left child. Copy 4 into the node, then remove the old leaf 4. The tree stays sorted: 1 4 6 7 8 10 13 14.',
            'DELETE FROM A BST · TWO CHILDREN → BORROW THE NEXT VALUE', 3.2)
    code = f.add_code(0, CY, lines, 270)
    X0 = code.w + 40
    b = place_tree(BST, X0, 74, 42, 52)
    four = b.by(4)
    t = b.draw(f, .2, .08, [k for k in b.sub(b.root) if k != four])
    tg = b.by(3); tx, ty = b.p(tg)
    f.show(goal_ring(tx, ty), 1.2)
    f.mover('chip', lambda x, y: chip(x, y, 'delete 3', 'middle'), 1.2, tx, ty - 40)
    f.move('chip', 2.2, X0 + 50, 28)
    sy = 74 + 3 * 52 + 44
    f.slot('s', X0, sy); f.slot('v', X0, sy + 22)
    t = 3.4
    f.show(ring(tx, ty) + plabel(tx, ty, 'node', 'l', NR + 5), t, hide=t + 7.6)
    f.line(t, 0); f.say('s', t, 'node = 3 · two children', PT); t += 1.2
    six = b.by(6)
    f.line(t, 1); f.mover('s', probe('s', 'r'), t, *b.p(six)); f.say('s', t, 's = node.right = 6', PT)
    f.say('v', t, 'smallest value on the right of 3', TX); t += 1.2
    f.line(t, 2); f.say('s', t, 's.left = 4 exists', PT); t += .7
    f.line(t, 3); f.move('s', t, *b.p(four)); f.say('s', t, 's = 4', PT); t += 1.0
    f.line(t, 2); f.say('s', t, 's.left is None → stop', PT); t += 1.0
    f.line(t, 4)
    f.mover('copy', lambda x, y: chip(x, y, '4', 'middle'), t, b.p(four)[0], b.p(four)[1] - 12)
    f.move('copy', t + .3, tx, ty - 12); f.hide('copy', t + 1.1)
    f.show(node(tx, ty, 4, 'vis'), t + 1.0)
    f.say('s', t, 'node.val = 4', PT); f.clear('v', t); t += 1.8
    f.line(t, 5)
    f.show(edge(b.p(six), b.p(four)) + node(*b.p(four), 4), .2, hide=t)
    f.hide('s', t)
    f.say('s', t, 'remove(s): the old leaf 4 goes', PT); t += 1.2
    f.show(node(tx, ty, 4, 'fill'), t)
    f.show(T(tx - 30, ty + 5, '✓ deleted 3', TG, 'end', mono=True, bold=True), t + .2)
    f.say('s', t + .3, 'still sorted: 1 4 6 7 8 10 13 14 · O(h)', TG, True)
    return f.render(max(code.y + code.h(), sy + 44))


def height_fig():
    f = Fig('tb-p4-', W, 'The same seven values in two shapes. Balanced: searching 7 visits 4, 6, 7, three steps. Chain: it visits 1 to 7, seven steps. The graph plots steps against n: a chain grows like n, a balanced tree like log2 n.',
            'COST = HEIGHT · SAME 7 VALUES, TWO SHAPES', 3.2)
    b = place_tree((4, (2, 1, 3), (6, 5, 7)), 40, 72, 40, 52, W=340)
    b.draw(f, .2, .06)
    f.static(T(40, 46, 'balanced · height 3', MU, 'start', mono=True))
    cx0, cy0 = 420, 50
    ch = [(cx0 + k * 38, cy0 + 12 + k * 24) for k in range(7)]
    f.static(T(cx0 - 10, 34, 'chain · height 7', MU, 'start', mono=True))
    for k, p in enumerate(ch):
        g = node(*p, k + 1, r=13)
        if k: g = edge(ch[k - 1], p, 13) + g
        f.show(g, .2 + k * .06)
    f.slot('a', 40, 236); f.slot('b', 420, 236)
    t = 1.6
    path = [b.by(4), b.by(6), b.by(7)]
    f.mover('pa', probe('node', 'l'), t, *b.p(path[0]))
    f.mover('pb', lambda x, y: circ(x, y, 18, vt('.10'), MID, 2.2), t, *ch[0])
    for k in range(7):
        if k < 3:
            if k: f.move('pa', t, *b.p(path[k]))
            f.say('a', t, 'steps = %d' % (k + 1), PT)
        if k: f.move('pb', t, *ch[k])
        f.say('b', t, 'steps = %d' % (k + 1), PT)
        t += .8
    f.hide('pa', t); f.hide('pb', t)
    f.show(node(*b.p(path[-1]), 7, 'fill'), t); f.show(node(*ch[-1], 7, 'fill', r=13), t)
    f.say('a', t, '✓ 3 steps', TG, True); f.say('b', t, '✓ 7 steps', TG, True)
    t += 1.2
    px, py = graph(f, 70, 280, 560, 170, 64, 64, [
        (lambda n: n, 'chain: n', 'var(--ghost)', 2, 40),
        (lambda n: math.log2(max(n, 1)), 'balanced: log₂ n', TG, 2.6, 46)], t, xt=(16, 32, 48, 64), yt=(16, 32, 48, 64))
    for k, n in enumerate((7, 63)):
        f.show(circ(px(n), py(n), 4, MID, 'none', 0) + circ(px(n), py(math.log2(n + 1)), 4, MID, 'none', 0), t + 2.6 + k * .4)
    f.show(T(px(63) - 8, py(36), 'n = 63 → 6 steps vs 63', MID, 'end', mono=True, bold=True), t + 3.4)
    f.show(T(70, 500, 'keep the tree balanced → O(log n) for search, insert, delete', TG, 'start', bold=True), t + 4)
    return f.render(512)


# ---------------------------------------------------------------- patterns
def combine_fig():
    lines = ['def h(node):', '    if not node: return 0', '    return 1 + max(h(node.left),', '                   h(node.right))']
    f = Fig('tb-q1-', W, 'Height computed bottom-up. Leaves return 1 because both children are empty. Each parent waits for its children and returns 1 plus the larger child height: 6 gets 2, 3 gets 3, 14 gets 2, 10 gets 3, and the root 8 gets 4.',
            'BOTTOM-UP · A NODE ANSWERS AFTER ITS CHILDREN ANSWER', 3.2)
    code = f.add_code(0, CY, lines, 260)
    X0 = code.w + 40
    b = place_tree(BST, X0, 74, 42, 52)
    b.draw(f, .2, .08)
    f.show(chip(X0 + 10, 28, 'height of the tree'), 1.0)
    sy = 74 + 3 * 52 + 44
    f.slot('s', X0, sy)
    H = {}
    post = []
    def go(i):
        if i is None: return 0
        a, c = go(b.L(i)), go(b.Rr(i)); H[i] = (a, c, 1 + max(a, c)); post.append(i); return H[i][2]
    go(b.root)
    t = 2.0; first = True
    for i in post:
        a, c, h = H[i]; x, y = b.p(i)
        f.line(t, 0)
        if first: f.mover('p', probe(), t, x, y); first = False
        else: f.move('p', t, x, y)
        f.line(t + .5, 2)
        f.say('s', t + .3, 'h(%d) = 1 + max(%d, %d) = %d' % (b.v(i), a, c, h), PT)
        st = 'fill' if i == b.root else 'vis'
        f.show(R(x + 11, y - 27, 18, 16, 'var(--bg)', 'none', 8) + R(x + 11, y - 27, 18, 16, TG if st == 'fill' else it('.14'), TG, 8, 1)
               + T(x + 20, y - 15, str(h), ONF if st == 'fill' else TG, cls='sv-s', mono=True, bold=True), t + .7)
        f.show(node(x, y, b.v(i), st), t + .7)
        t += 1.3
    f.hide('p', t); f.line(t, 2)
    f.say('s', t + .1, '✓ height = 4 · each node visited once · O(n)', TG, True)
    return f.render(max(code.y + code.h(), sy + 22))


def rightview_fig():
    lines = ['q = [root]', 'while q:', '    out.append(q[-1].val)', '    q = [c for n in q', '         for c in (n.left, n.right) if c]']
    f = Fig('tb-q2-', W, 'Right side view of the tree 1; 2, 3; 4, 5, 6; 7. The queue holds one whole level. The last node of each level is what you see from the right: 1, then 3, then 6, then 7. out = 1 3 6 7.',
            'LEVEL BY LEVEL · RIGHT SIDE VIEW = LAST NODE OF EACH LEVEL', 3.2)
    code = f.add_code(0, CY, lines, 300)
    X0 = code.w + 40
    b = place_tree((1, (2, 4, (5, 7, None)), (3, None, 6)), X0, 70, 46, 50)
    b.draw(f, .2, .08)
    oy = 70 + 3 * 50 + 34
    cell = out_row(f, X0 + 50, oy)
    f.slot('s', X0 + 10, oy + 56)
    f.show(T(W - 4, 50, 'view from the right →', MU, 'end', mono=True), 1.0)
    level = [b.root]; t = 2.0; out = []; d = 0
    while level:
        f.line(t, 1)
        f.say('s', t, 'q = [%s]' % ', '.join(str(b.v(i)) for i in level), PT)
        y = b.p(level[0])[1]
        xs = [b.p(i)[0] for i in level]
        f.show(R(min(xs) - 24, y - 22, max(xs) - min(xs) + 48, 44, 'none', PT, 22, 1.2, '4 3'), t, hide=t + 2.2)
        t += .8
        last = level[-1]; x, yy = b.p(last)
        f.line(t, 2)
        f.show(ring(x, yy), t, hide=t + 1.4)
        f.show(node(x, yy, b.v(last), 'vis'), t + .3)
        f.show(ocell(*cell(len(out)), b.v(last), 'vis'), t + .4); out.append(b.v(last))
        for i in level[:-1]: f.show(node(*b.p(i), b.v(i), 'grey'), t + .6)
        f.say('s', t, 'last of level %d = %d → out' % (d, b.v(last)), TG, True)
        t += 1.4
        f.line(t, 3)
        level = [c for i in level for c in (b.L(i), b.Rr(i)) if c is not None]; d += 1
        t += .2
    f.line(t, 1)
    for k, v in enumerate(out): f.show(ocell(*cell(k), v, 'fill'), t + .1 + k * .06)
    f.say('s', t + .3, '✓ right view = 1 3 6 7 · O(n)', TG, True)
    return f.render(max(code.y + code.h(), oy + 76))


def kth_fig():
    lines = ['def walk(node):', '    if not node: return', '    walk(node.left)', '    k -= 1', '    if k == 0: ans = node.val', '    walk(node.right)']
    f = Fig('tb-q3-', W, 'Third smallest value in the BST. An inorder walk visits values in sorted order: 1, then 3, then 4. k counts down 3, 2, 1, 0; at 0 the answer is 4 and the walk stops. The rest of the tree is never visited.',
            'BST IN SORTED ORDER · 3RD SMALLEST = THE 3RD NODE INORDER', 3.2)
    code = f.add_code(0, CY, lines, 260)
    X0 = code.w + 40
    b = place_tree(BST, X0, 74, 42, 52)
    b.draw(f, .2, .08)
    f.show(chip(X0 + 10, 28, 'k = 3'), 1.0)
    oy = 74 + 3 * 52 + 36
    cell = out_row(f, X0 + 60, oy, 'sorted')
    f.slot('s', X0 + 20, oy + 56)
    t = 2.0
    n8, n3, n1, n6, n4 = (b.by(v) for v in (8, 3, 1, 6, 4))
    f.mover('p', probe(), t, *b.p(n8)); f.line(t, 0); f.say('s', t, 'walk(8)', PT); t += .8
    seq = [('d', n3), ('d', n1), ('e', n1, 2), ('u', n3), ('e', n3, 1), ('d', n6), ('d', n4), ('e', n4, 0)]
    k = 0
    for e in seq:
        if e[0] == 'd':
            f.line(t, 2); f.move('p', t + .1, *b.p(e[1])); f.say('s', t, 'walk(%d) ↓ left' % b.v(e[1]) if e[1] != n6 else 'walk(6) ↓ right', PT); t += .9
        elif e[0] == 'u':
            f.line(t, 2); f.move('p', t + .1, *b.p(e[1])); f.say('s', t, 'back to %d' % b.v(e[1]), MU); t += .8
        else:
            i = e[1]; f.line(t, 3)
            f.show(node(*b.p(i), b.v(i), 'vis'), t + .1)
            f.show(ocell(*cell(k), b.v(i), 'vis'), t + .2); k += 1
            f.say('s', t, 'visit %d · k = %d' % (b.v(i), e[2]), TG, True); t += 1.1
    f.line(t, 4); f.hide('p', t)
    x, y = b.p(n4)
    f.show(node(x, y, 4, 'fill'), t); f.show(ocell(*cell(2), 4, 'fill'), t)
    f.show(T(x - 26, y + 5, '✓ ans', TG, 'end', mono=True, bold=True), t + .2)
    f.say('s', t + .3, 'k == 0 → ans = 4 · stopped after 3 of 9 nodes', TG, True)
    return f.render(max(code.y + code.h(), oy + 76))


def lca_fig():
    lines = ['def lca(node):', '    if not node or node in (p, q): return node', '    L, R = lca(node.left), lca(node.right)', '    if L and R: return node', '    return L or R']
    f = Fig('tb-q4-', W, 'Lowest common ancestor of 4 and 1. The recursion returns a target when it reaches one. 4 is returned up to 6, and 6 passes it to 3. 1 is returned to 3 from the other side. 3 gets a target from both sides, so 3 is the answer and 8 just passes it on.',
            'COMMON ANCESTOR · THE NODE THAT GETS A TARGET FROM BOTH SIDES', 3.2)
    code = f.add_code(0, CY, lines, 330)
    X0 = code.w + 30
    b = place_tree(BST, X0, 74, 40, 52)
    b.draw(f, .2, .08)
    n4, n1, n6, n3, n8 = (b.by(v) for v in (4, 1, 6, 3, 8))
    for k, i in enumerate((n4, n1)): f.show(goal_ring(*b.p(i)), 1.1 + k * .2)
    f.show(chip(X0 + 10, 28, 'p = 4 · q = 1'), 1.2)
    sy = 74 + 3 * 52 + 44
    f.slot('s', X0, sy)
    t = 2.4
    def badge(v): return lambda x, y: chip(x, y, str(v), 'middle')
    f.line(t, 1); f.say('s', t, 'lca(1): node is q → return 1', PT)
    x, y = b.p(n1); f.mover('c1', badge(1), t, x, y - 44); f.show(node(x, y, 1, 'vis'), t); t += 1.3
    f.say('s', t, 'lca(4): node is p → return 4', PT)
    x, y = b.p(n4); f.mover('c4', badge(4), t, x, y - 44); f.show(node(x, y, 4, 'vis'), t); t += 1.3
    f.line(t, 4); f.say('s', t, 'lca(6): L = 4, R = None → return 4', PT)
    x, y = b.p(n6); f.move('c4', t + .2, x + 28, y - 30); f.show(node(x, y, 6, 'vis'), t + .5); t += 1.5
    f.line(t, 2); f.say('s', t, 'lca(3): L = 1, R = 4', PT)
    x, y = b.p(n3); f.move('c1', t + .2, x - 26, y - 34); f.move('c4', t + .2, x + 26, y - 34)
    f.show(ring(x, y), t + .6, hide=t + 2.2); t += 1.6
    f.line(t, 3); f.say('s', t, 'L and R → return 3', TG, True)
    f.hide('c1', t + .6); f.hide('c4', t + .6)
    f.show(node(x, y, 3, 'fill'), t + .6); t += 1.5
    f.line(t, 4); f.say('s', t, 'lca(8): L = 3, R = None → return 3', PT); t += 1.3
    f.show(T(x - 28, y + 5, '✓ ans', TG, 'end', mono=True, bold=True), t)
    f.say('s', t, '✓ lowest common ancestor of 4 and 1 = 3 · O(n)', TG, True)
    return f.render(max(code.y + code.h(), sy + 22))


def invert_fig():
    lines = ['def invert(node):', '    if not node: return', '    node.left, node.right = node.right, node.left', '    invert(node.left)', '    invert(node.right)']
    f = Scene('tb-q5-', W, 'Invert the tree 4; 2, 7; 1, 3, 6, 9. At each node, swap the left and right subtrees: first at 4 the whole 2-subtree and 7-subtree trade places, then inside 7 the children 9 and 6 swap, then inside 2 the children 3 and 1 swap. The result is the mirror image.',
              'TRANSFORM · SWAP THE TWO CHILDREN AT EVERY NODE', 3.2)
    code = f.add_code(0, CY, lines, 340)
    X0 = code.w + 30
    b = place_tree((4, (2, 1, 3), (7, 6, 9)), X0, 74, 46, 56)
    for k, i in enumerate(b.sub(b.root)):
        f.node(i, b.v(i), .2 + k * .08, *b.p(i))
        if b.n[i]['par'] is not None: f.edge_on(.2 + k * .08, i, b.n[i]['par'])
    # mirror positions
    xs = sorted(n['x'] for n in b.n)
    sy = 74 + 2 * 56 + 46
    f.slot('s', X0, sy)
    t = 1.8
    cur = {i: b.p(i) for i in range(len(b.n))}
    kids = {i: [b.L(i), b.Rr(i)] for i in range(len(b.n))}
    def mirror_sub(i):
        """swap at i: every node in the two subtrees moves to the mirrored x inside i's span."""
        L_, R_ = kids[i]
        sub = [k for c in (L_, R_) if c is not None for k in walk(c)]
        if not sub: return
        lo = min(cur[k][0] for k in sub); hi = max(cur[k][0] for k in sub)
        for k in sub: cur[k] = (lo + hi - cur[k][0], cur[k][1])
        kids[i] = [R_, L_]
    def walk(i):
        return [] if i is None else [i] + walk(kids[i][0]) + walk(kids[i][1])
    first = True
    def visit(i):
        nonlocal t, first
        if i is None: return
        x, y = cur[i]
        f.line(t, 0)
        if first: f.mover('p', probe(), t, x, y); first = False
        else: f.move('p', t, x, y)
        t += .7
        if any(kids[i]):
            f.line(t, 2)
            f.say('s', t, 'at %d: swap %s and %s' % (b.v(i), b.v(kids[i][0]), b.v(kids[i][1])), PT)
            mirror_sub(i)
            for k in walk(kids[i][0]) + walk(kids[i][1]): f.place(t + .3, k, *cur[k])
            t += 1.6
        f.over(i, lambda x, y, v=b.v(i): node(x, y, v, 'vis'), t - .2)
        l, r = kids[i]
        if l is not None: f.line(t, 3); t += .1; visit(l)
        if r is not None: f.line(t, 4); t += .1; visit(r)
    visit(b.root)
    f.hide('p', t); f.line(t, 0)
    f.say('s', t + .2, '✓ mirror image · inorder 9 7 6 4 3 2 1 · O(n)', TG, True)
    return f.render(max(code.y + code.h(), sy + 22))


figs = {
    'm1': anatomy_fig(),
    'm2': dfs_fig('tb-m2-', 'pre', 'PREORDER · NODE FIRST, THEN LEFT, THEN RIGHT', 'Preorder on the tree 4; 2, 6; 1, 3, 5, 7. The pointer node walks down and back up; each node is appended when first reached. out = 4 2 1 3 6 5 7.'),
    'm3': dfs_fig('tb-m3-', 'in', 'INORDER · LEFT, THEN NODE, THEN RIGHT', 'Inorder on the same tree. A node is appended after its whole left side. out = 1 2 3 4 5 6 7, sorted, because the tree is a BST.'),
    'm4': dfs_fig('tb-m4-', 'post', 'POSTORDER · LEFT, THEN RIGHT, THEN NODE', 'Postorder on the same tree. A node is appended after both children. out = 1 3 2 5 7 6 4; the root comes last.'),
    'm5': level_fig(),
    'p1': search_fig(), 'p2': insert_fig(), 'p3': delete_fig(), 'p4': height_fig(),
    'q1': combine_fig(), 'q2': rightview_fig(), 'q3': kth_fig(), 'q4': lca_fig(), 'q5': invert_fig(),
}
dump('tree-bst-traversal', figs)
print('ok', len(figs))
