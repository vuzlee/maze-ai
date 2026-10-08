# -*- coding: utf-8 -*-
"""DSA shelf overview: family tree of structures + problem -> technique decision tree.

    python3 tools/svgkit/dsa/dsa_overview_v2.py   # rewrites figures in place
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from overview import Fig, text

PAGE = 'content/01-dsa/01-overview/dsa-overview/index.html'
DS = '../../03-data-structures/'
AL = '../../04-algorithms/'


B, V, F = 'var(--brand)', 'var(--violet)', 'var(--filled)'
TINT = 'rgba(var(--clay-a),.10)'
VT = 'rgba(var(--violet-a),.14)'
DS = '../../03-data-structures/'
AL = '../../04-algorithms/'
TW, TH, GAP = 164, 98, 8

def cell(x, y, w, h, s='', hl=False):
    o = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="2.5" fill="{VT if hl else TINT}" stroke="{V if hl else B}" stroke-width="1.1"/>'
    if s != '':
        o += text(x + w / 2, y + h / 2 + 3.5, str(s), 'sv-d', V if hl else 'var(--text)', 'middle', ';font-family:var(--mono);font-size:9.5px')
    return o

def dot(x, y, s='', hl=False, r=8):
    o = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{VT if hl else "var(--bg)"}" stroke="{V if hl else B}" stroke-width="1.2"/>'
    if s != '':
        o += text(x, y + 3.3, str(s), 'sv-d', V if hl else 'var(--text)', 'middle', ';font-family:var(--mono);font-size:9px')
    return o

def ln(x1, y1, x2, y2, col=None, w=1.1, dash=False):
    d = ' stroke-dasharray="3 2"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col or "var(--rule-hi)"}" stroke-width="{w}"{d}/>'

def arr(x1, y, x2, col=None):
    c = col or 'var(--muted)'
    return ln(x1, y, x2 - 4, y, c) + f'<path d="M{x2-5},{y-3} L{x2},{y} L{x2-5},{y+3}z" fill="{c}"/>'

# ---- drawings: each gets the inner box origin (x, y), width 138, height 58 ----
def d_array(x, y):
    o = ''.join(cell(x + 4 + i * 21, y + 18, 20, 20, v, i == 3) for i, v in enumerate([7, 2, 9, 4, 1, 6]))
    o += ''.join(text(x + 14 + i * 21, y + 50, str(i), 'sv-d', 'var(--faint)', 'middle', ';font-size:8.5px;font-family:var(--mono)') for i in range(6))
    return o + text(x + 77, y + 10, 'a[3]', 'sv-d', V, 'middle', ';font-size:9px;font-family:var(--mono)')
def d_list(x, y):
    o = ''
    for i, v in enumerate([3, 8, 5]):
        cx = x + 4 + i * 44
        o += cell(cx, y + 22, 18, 18, v) + cell(cx + 18, y + 22, 9, 18)
        o += arr(cx + 23, y + 31, cx + 44 if i < 2 else cx + 38)
    return o + text(x + 141, y + 35, '∅', 'sv-d', 'var(--faint)', 'start')
def d_stackq(x, y):
    o = ''.join(cell(x + 8, y + 10 + i * 12, 34, 11, '', i == 0) for i in range(4))
    o += text(x + 46, y + 19, 'top', 'sv-d', V, 'start', ';font-size:9px')
    o += ''.join(cell(x + 74 + i * 14, y + 26, 13, 18, '', i == 0) for i in range(4))
    o += text(x + 74, y + 56, 'out', 'sv-d', V, 'start', ';font-size:8.5px') + text(x + 130, y + 56, 'in', 'sv-d', 'var(--faint)', 'end', ';font-size:8.5px')
    return o
def d_hash(x, y):
    o = ''
    for i in range(4):
        o += cell(x + 44, y + 2 + i * 14, 16, 13, i)
    o += text(x + 4, y + 26, '"cat"', 'sv-d', V, 'start', ';font-size:9px;font-family:var(--mono)')
    o += arr(x + 30, y + 23, x + 44, V)
    o += arr(x + 60, y + 22.5, x + 76) + cell(x + 76, y + 16, 32, 13, '', True)
    o += arr(x + 60, y + 50.5, x + 76) + cell(x + 76, y + 44, 32, 13) + arr(x + 108, y + 50.5, x + 118) + cell(x + 118, y + 44, 20, 13)
    return o
def tree(x, y, vals, hl=()):
    P = [(x + 69, y + 8), (x + 36, y + 30), (x + 102, y + 30), (x + 18, y + 52), (x + 54, y + 52), (x + 86, y + 52), (x + 120, y + 52)]
    o = ''.join(ln(*P[p], *P[c]) for p, c in ((0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)))
    return o + ''.join(dot(px, py, v, i in hl) for i, ((px, py), v) in enumerate(zip(P, vals)))
def d_bst(x, y): return tree(x, y, [8, 4, 12, 2, 6, 10, 14], (0, 1, 4))
def d_heap(x, y): return tree(x, y, [1, 3, 2, 7, 4, 5, 9], (0,))
def d_trie(x, y):
    P = {'r': (x + 69, y + 4), 'c': (x + 40, y + 21), 'd': (x + 98, y + 21), 'a': (x + 40, y + 38), 'o': (x + 98, y + 38), 't': (x + 22, y + 55), 'r2': (x + 58, y + 55)}
    o = ''.join(ln(*P[a], *P[b]) for a, b in (('r', 'c'), ('r', 'd'), ('c', 'a'), ('d', 'o'), ('a', 't'), ('a', 'r2')))
    lab = {'r': '', 'c': 'c', 'd': 'd', 'a': 'a', 'o': 'o', 't': 't', 'r2': 'r'}
    return o + ''.join(dot(*P[k], lab[k], k in ('c', 'a', 't'), 7) for k in P)
GP = [(14, 14), (56, 6), (100, 18), (128, 46), (78, 50), (30, 52)]
GE = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (1, 4), (0, 4))
def d_graph(x, y, hl=(), w=False):
    o = ''
    for a, b in GE:
        on = (a, b) in hl
        o += ln(x + GP[a][0], y + GP[a][1], x + GP[b][0], y + GP[b][1], V if on else None, 2 if on else 1.1)
    return o + ''.join(dot(x + px, y + py, '', False, 6.5) for px, py in GP)

# algorithms
def d_sort(x, y):
    hs = [10, 18, 26, 34, 42, 50]
    o = ''
    for i, h in enumerate([34, 10, 50, 18, 42, 26]):
        o += f'<rect x="{x + 2 + i * 10}" y="{y + 56 - h}" width="8" height="{h}" rx="1.5" fill="{TINT}" stroke="{B}" stroke-width="1"/>'
    o += arr(x + 66, y + 34, x + 76, 'var(--muted)')
    for i, h in enumerate(hs):
        o += f'<rect x="{x + 80 + i * 10}" y="{y + 56 - h}" width="8" height="{h}" rx="1.5" fill="{VT if i == 5 else TINT}" stroke="{V if i == 5 else B}" stroke-width="1"/>'
    return o
def d_bsearch(x, y):
    o = ''.join(cell(x + 2 + i * 17, y + 26, 16, 16, '', i == 5) for i in range(8))
    o += f'<rect x="{x + 2}" y="{y + 26}" width="{4 * 17 - 1}" height="16" fill="var(--sunk)" opacity=".75"/>'
    o += f'<path d="M{x+70},{y+20} V{y+12} H{x+138} V{y+20}" fill="none" stroke="{V}" stroke-width="1.2"/>'
    o += text(x + 104, y + 8, 'keep half', 'sv-d', V, 'middle', ';font-size:9px') + text(x + 36, y + 56, 'drop', 'sv-d', 'var(--faint)', 'middle', ';font-size:9px')
    return o
def d_window(x, y):
    o = ''.join(cell(x + 2 + i * 17, y + 22, 16, 16) for i in range(8))
    o += f'<rect x="{x + 36}" y="{y + 18}" width="54" height="24" rx="4" fill="none" stroke="{V}" stroke-width="1.6"/>'
    o += text(x + 10, y + 56, 'L', 'sv-d', V, 'middle', ';font-family:var(--mono);font-weight:600') + text(x + 129, y + 56, 'R', 'sv-d', V, 'middle', ';font-family:var(--mono);font-weight:600')
    o += arr(x + 18, y + 52, x + 32, V) + arr(x + 121, y + 52, x + 107, V)
    return o
def d_bfs(x, y):
    o = ''
    for r, a in ((10, .20), (18, .11), (26, .05)):
        o += f'<circle cx="{x + 14}" cy="{y + 14}" r="{r}" fill="rgba(var(--violet-a),{a})"/>'
    return o + d_graph(x, y, ((0, 1), (5, 0), (0, 4)))
def d_path(x, y):
    o = d_graph(x, y, ((0, 4), (4, 3)))
    for (a, b), w in zip(GE, [4, 7, 2, 3, 6, 9, 5, 1]):
        mx, my = x + (GP[a][0] + GP[b][0]) / 2, y + (GP[a][1] + GP[b][1]) / 2
        o += text(mx, my - 2, str(w), 'sv-d', 'var(--faint)', 'middle', ';font-size:8px;font-family:var(--mono)')
    return o
def d_greedy(x, y):
    iv = [(0, 40, True), (20, 70, False), (46, 80, True), (60, 110, False), (86, 132, True)]
    o = ''
    for i, (a, b, on) in enumerate(iv):
        yy = y + 6 + i * 11
        o += f'<rect x="{x + 4 + a}" y="{yy}" width="{b - a}" height="7" rx="3.5" fill="{VT if on else "var(--sunk)"}" stroke="{V if on else "var(--rule-hi)"}" stroke-width="1"/>'
    return o
def d_back(x, y):
    P = [(x + 69, y + 6), (x + 32, y + 28), (x + 106, y + 28), (x + 14, y + 52), (x + 50, y + 52), (x + 88, y + 52), (x + 124, y + 52)]
    o = ''
    for p, c in ((0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)):
        on = (p, c) in ((0, 1), (1, 4))
        dead = c in (2, 5, 6)
        o += ln(*P[p], *P[c], V if on else None, 1.8 if on else 1.1, dead)
    for i, (px, py) in enumerate(P):
        o += dot(px, py, '', i in (0, 1, 4), 6)
    o += text(x + 106, y + 31.5, '✕', 'sv-d', 'var(--rose)', 'middle', ';font-weight:700')
    return o
def d_dp(x, y):
    o = ''
    for r in range(3):
        for c in range(6):
            hl = (r, c) == (2, 5)
            dep = (r, c) in ((1, 5), (2, 4))
            o += cell(x + 12 + c * 19, y + 4 + r * 18, 18, 17, '', hl or dep) if hl else cell(x + 12 + c * 19, y + 4 + r * 18, 18, 17)
            if dep:
                o += f'<rect x="{x + 12 + c * 19}" y="{y + 4 + r * 18}" width="18" height="17" rx="2.5" fill="rgba(var(--violet-a),.07)"/>'
    return o

DSL = [('Array', 'index in O(1)', d_array, DS + 'array-string/index.html'),
       ('Linked list', 'nodes + pointers', d_list, DS + 'linked-list/index.html'),
       ('Stack · queue', 'only the ends', d_stackq, DS + 'stack-monotonic-queue/index.html'),
       ('Hash map', 'key → slot', d_hash, DS + 'hash-map/index.html'),
       ('Tree · BST', 'smaller left', d_bst, DS + 'tree-bst-traversal/index.html'),
       ('Heap', 'min on top', d_heap, DS + 'heap-priority-queue/index.html'),
       ('Trie', 'one char per level', d_trie, DS + 'trie/index.html'),
       ('Graph', 'anything to anything', lambda x, y: d_graph(x, y), AL + 'graph-bfs-dfs-topo/index.html')]
ALL = [('Sorting', 'put in order', d_sort, AL + 'sorting/index.html'),
       ('Binary search', 'halve each step', d_bsearch, AL + 'binary-search/index.html'),
       ('Two pointers · window', 'walk from both ends', d_window, AL + 'sliding-window/index.html'),
       ('BFS · DFS', 'visit by layers', d_bfs, AL + 'graph-bfs-dfs-topo/index.html'),
       ('Shortest path', 'cheapest route', d_path, AL + 'shortest-path/index.html'),
       ('Greedy · intervals', 'best choice now', d_greedy, AL + 'greedy/index.html'),
       ('Backtracking', 'try, undo, prune', d_back, AL + 'backtracking/index.html'),
       ('Dynamic programming', 'reuse sub-answers', d_dp, AL + 'dynamic-programming/index.html')]

def gallery():
    H = 528
    f = Fig('dsov1', 680, H, 'THE WHOLE FIELD · EIGHT WAYS TO HOLD DATA, EIGHT WAYS TO WORK ON IT',
            'Two galleries. Data structures, how data is held: array, linked list, stack and queue, hash map, '
            'tree and binary search tree, heap, trie, graph — each drawn in its classic shape. Algorithms, the '
            'steps that run on them: sorting, binary search, two pointers and sliding window, breadth- and '
            'depth-first search, shortest path, greedy over intervals, backtracking with a pruned branch, and a '
            'dynamic-programming table. Each tile links to its lesson.')
    def band(y0, label, sub, items, t0):
        f.add(f'<g class="{f.step(t0)}">' + text(0, y0, label, 'sv-hv', B, 'start')
              + text(680, y0, sub, 'sv-d', 'var(--muted)', 'end') + '</g>')
        for i, (name, note, draw, href) in enumerate(items):
            r, c = divmod(i, 4)
            x, y = c * (TW + GAP), y0 + 10 + r * (TH + 10)
            inner = (f'<rect class="nd" x="{x:.1f}" y="{y}" width="{TW}" height="{TH}" rx="10" fill="var(--bg)" stroke="var(--rule-hi)" stroke-width="1.2"/>'
                     + text(x + 10, y + 17, name, 'sv-s', 'var(--text)', 'start', ';font-weight:600;font-size:11px')
                     + draw(x + 13, y + 30))
            f.add(f'<g class="{f.step(t0 + 0.25 + i * 0.12)}"><a href="{href}">{inner}</a></g>')
    band(44, 'DATA STRUCTURES', 'how data is held', DSL, 0.1)
    band(44 + 2 * (TH + 10) + 34, 'ALGORITHMS', 'steps that run on it', ALL, 1.4)
    f.h = 44 + 2 * (2 * (TH + 10) + 34) - 34 + 4
    return f.svg()



def family():
    f = Fig('dsov2', 680, 384, 'FAMILY TREE · TWO ROOTS AT THE TOP, EVERY STRUCTURE BRANCHES DOWN FROM THEM',
            'A top-down family tree of data structures with two roots at the top. Left root: array, cells side by '
            'side in memory, giving instant access by index. Right root: linked node, a value plus a pointer, '
            'giving cheap insert anywhere. From the array grow stack and queue, and the heap, a tree stored '
            'inside an array. From the linked node grow the linked list and the tree; the tree grows into the '
            'binary search tree and the trie, and a tree whose nodes may link in cycles is a graph. The hash '
            'map is a hybrid of both roots: an array of buckets whose collisions chain as linked nodes. '
            'Union-find is a forest stored in an array. Each block links to its lesson.')
    W = 136
    # positions (cx, cy)
    P = {
        'array': (150, 60), 'node': (530, 60),
        'stack': (78, 152), 'heap': (226, 152), 'hash': (380, 152), 'list': (602, 152),
        'tree': (530, 244),
        'uf': (200, 336), 'bst': (350, 336), 'trie': (480, 336), 'graph': (610, 336),
    }
    top = lambda k: (P[k][0], P[k][1] - 22)
    bot = lambda k: (P[k][0], P[k][1] + 22)
    t = 0.2
    # layer 0: roots
    a0 = f.step(t)
    # era labels on the left
    f.add(text(0, 390, '', 'sv-d'))
    # edges first so nodes sit on top
    def E(a, b, delay, col='var(--rule-hi)', dashed=False):
        f.edge(bot(a), top(b), cls=f.step(delay, draw=True), col=col, dashed=dashed)
    E('array', 'stack', 0.8); E('array', 'hash', 0.8, 'var(--violet)'); E('node', 'hash', 0.8, 'var(--violet)')
    E('node', 'list', 0.8)
    E('array', 'heap', 0.8); E('node', 'tree', 1.6); E('tree', 'uf', 2.4, 'var(--violet)')
    f.add(f'<path class="{f.step(1.6, draw=True)}" pathLength="1" d="M226,174 C226,244 380,244 462,244" fill="none" '
          'stroke="var(--violet)" stroke-width="1.6"/>')
    f.add(f'<g class="{f.step(1.9)}">' + text(395, 236, 'shaped like a tree', 'sv-d', 'var(--violet)') + '</g>')
    E('tree', 'bst', 2.4); E('tree', 'trie', 2.4); E('tree', 'graph', 2.4)
    # roots
    f.node(*P['array'], 'Array', 'cells side by side · O(1) index', 'filled', a0, DS + 'array-string/index.html', 'array', w=196, h=46)
    f.node(*P['node'], 'Linked node', 'value + pointer · O(1) insert', 'filled', a0, DS + 'linked-list/index.html', 'node', w=196, h=46)
    b = f.step(1.1)
    f.node(*P['stack'], 'Stack · queue', 'only the ends', 'plain', b, DS + 'stack-monotonic-queue/index.html', 'stack', w=W)
    f.node(*P['hash'], 'Hash map', 'array + chains', 'violet', b, DS + 'hash-map/index.html', 'hash', w=W)
    f.node(*P['list'], 'Linked list', 'nodes in a row', 'plain', b, DS + 'linked-list/index.html', 'list', w=W)
    b2 = f.step(1.1)
    f.node(*P['heap'], 'Heap', 'tree in an array', 'violet', b2, DS + 'heap-priority-queue/index.html', 'heap', w=W)
    c = f.step(1.9)
    d0 = f.step(2.7)
    f.node(*P['uf'], 'Union-find', 'forest in an array', 'violet', d0, DS + 'union-find/index.html', 'groups', w=W)
    f.node(*P['tree'], 'Tree', 'node → children', 'plain', c, DS + 'tree-bst-traversal/index.html', 'tree', w=W)
    d = f.step(2.7)
    f.node(*P['bst'], 'BST', 'sorted, O(log n)', 'plain', d, DS + 'tree-bst-traversal/index.html', 'bst', w=120)
    f.node(*P['trie'], 'Trie', 'one char / level', 'plain', d, DS + 'trie/index.html', 'trie', w=120)
    f.node(*P['graph'], 'Graph', 'any links', 'plain', d, AL + 'graph-bfs-dfs-topo/index.html', 'graph', w=110)
    # legend
    lg = f.step(3.3)
    f.add(f'<g class="{lg}"><line x1="20" y1="372" x2="40" y2="372" stroke="var(--violet)" stroke-width="1.6"/>'
          + text(46, 376, 'hybrid of both roots', 'sv-d', 'var(--violet)', 'start') + '</g>')
    return f.svg()


def decide():
    f = Fig('dsov3', 680, 404, 'READ THE PROBLEM → PICK THE TECHNIQUE',
            'A left-to-right decision tree. Start from what the input looks like. A sorted array leads to two '
            'pointers or binary search. A contiguous range of an array leads to sliding window or prefix sum. '
            'Needing fast lookup or counting leads to a hash map. Needing the top k or the next smallest leads '
            'to a heap. Nodes and edges lead to BFS, DFS or topological sort, and weighted edges to Dijkstra. '
            'Listing every option leads to backtracking; asking for the best count or value with overlapping '
            'subproblems leads to dynamic programming. One path lights up as an example: sorted array, find a '
            'pair, two pointers.')
    q = [  # question, y, leaves [(name, href)]
        ('Sorted array?', [('Two pointers', AL + 'two-pointers/index.html'), ('Binary search', AL + 'binary-search/index.html')]),
        ('Contiguous range?', [('Sliding window', AL + 'sliding-window/index.html'), ('Prefix sum', AL + 'prefix-sum/index.html')]),
        ('Look up / count fast?', [('Hash map', DS + 'hash-map/index.html')]),
        ('Top k · next smallest?', [('Heap', DS + 'heap-priority-queue/index.html')]),
        ('Nodes and edges?', [('BFS · DFS · topo', AL + 'graph-bfs-dfs-topo/index.html'), ('Dijkstra', AL + 'shortest-path/index.html')]),
        ('List every option?', [('Backtracking', AL + 'backtracking/index.html')]),
        ('Best value · overlaps?', [('Dynamic programming', AL + 'dynamic-programming/index.html')]),
    ]
    y0, dy = 50, 50
    root = (92, y0 + dy * 3)
    a = f.step(0.2)
    f.node(root[0], root[1], 'The input', 'what does it look like?', 'brand', a, None, None, w=150, h=46)
    hl = 0  # example path
    for i, (qq, leaves) in enumerate(q):
        y = y0 + i * dy
        on = i == hl
        f.hedge((167, root[1]), (220, y), cls=f.step(0.5 + i * 0.12, draw=True),
                col='var(--violet)' if on else 'var(--rule-hi)', width=2 if on else 1.4)
        s = f.step(0.7 + i * 0.12)
        f.node(318, y, qq, '', 'violet' if on else 'plain', s, None, None, w=196, h=34)
        x = 446
        for j, (name, href) in enumerate(leaves):
            on2 = on and j == 0
            if j == 0:
                f.add(f'<line class="{f.step(1.7 + i * 0.1, draw=True)}" pathLength="1" x1="416" y1="{y}" x2="{x}" y2="{y}" '
                      f'stroke="{"var(--violet)" if on2 else "var(--rule-hi)"}" stroke-width="{2 if on2 else 1.4}"/>')
            w = f.pill(x, y, name, 'violet' if on2 else 'brand', f.step(1.9 + i * 0.1 + j * 0.05), href)
            x += w + 8
    e = f.step(3.3)
    f.add(f'<g class="{e}">' + text(680, y0 + dy * 6 + 40, 'example: “pair in a sorted array that sums to k” → two pointers',
                                    'sv-d', 'var(--violet)', 'end', ';font-weight:600') + '</g>')
    return f.svg()


def put(html, sec_id, svg):
    i = html.index(f'id="{sec_id}"')
    a = html.index('<svg', i)
    b = html.rindex('</svg>', a, html.index('</figure>', a)) + 6
    return html[:a] + svg + html[b:]


if __name__ == '__main__':
    s = open(PAGE, encoding='utf-8').read()
    s = put(s, 'dsaov-s1', gallery())
    s = put(s, 'dsaov-s2', family())
    s = put(s, 'dsaov-s3', decide())
    open(PAGE, 'w', encoding='utf-8').write(s)
    print('ok')
