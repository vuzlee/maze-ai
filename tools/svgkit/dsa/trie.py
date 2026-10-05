"""Figures for content/01-dsa/03-data-structures/trie (visual-first DSA lesson).
Writes /tmp/dsa/trie.json  {figure key: <figure> html}."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from treekit_tbu import *

W = 760
CY = 40
DY = 50


def probe(name='node', side='l'):
    return lambda x, y: ring(x, y) + plabel(x, y, name, side, NR + 5)


class Trie:
    """Trie of words laid out as a tree: leaves get consecutive slots, parents centre on children."""
    def __init__(s, words, x0, y0, dx=40, dy=DY, root_label='·'):
        s.kids = {'': []}; s.end = set()
        for w in words:
            for k in range(1, len(w) + 1):
                p = w[:k]
                if p not in s.kids:
                    s.kids[p] = []; s.kids[w[:k - 1]].append(p)
            s.end.add(w)
        s.pos = forest(s.kids, '', x0, y0, dx, dy)
        s.root_label = root_label
    def lab(s, p): return p[-1] if p else s.root_label
    def order(s):
        out = []
        def go(p):
            out.append(p)
            for c in s.kids[p]: go(c)
        go(''); return out
    def width(s): return max(x for x, _ in s.pos.values()) - min(x for x, _ in s.pos.values())
    def shift(s, dx):
        for k in s.pos: s.pos[k] = (s.pos[k][0] + dx, s.pos[k][1])
    def draw(s, f, t0=.2, dt=.06, only=None, ends=True):
        for k, p in enumerate([p for p in s.order() if only is None or p in only]):
            g = node(*s.pos[p], s.lab(p), end=ends and p in s.end)
            if p: g = edge(s.pos[p[:-1]], s.pos[p]) + g
            f.show(g, t0 + k * dt)


def forest(kids, root, x0, y0, dx, dy):
    pos = {}; slot = [0]
    def go(u, d):
        ks = kids.get(u, [])
        if not ks:
            x = x0 + slot[0] * dx; slot[0] += 1
        else:
            xs = [go(k, d + 1) for k in ks]; x = (xs[0] + xs[-1]) / 2
        pos[u] = (x, y0 + d * dy); return x
    go(root, 0)
    return pos


def centre(tr, X0, W=W):
    xs = [x for x, _ in tr.pos.values()]
    tr.shift(X0 + (W - X0 - (max(xs) - min(xs))) / 2 - min(xs))


WORDS = ['car', 'cart', 'cat', 'dog', 'do']


# ---------------------------------------------------------------- 1.1 shared prefixes
def model_fig():
    f = Fig('tr-m1-', W, 'Five words are added one by one: car, cart, cat, dog, do. car makes a path c, a, r. cart reuses c, a, r and adds only t. cat reuses c, a and adds t. dog makes a new branch. do adds no node at all, it only marks o as the end of a word. A double ring marks where a word ends.',
            'WORDS WITH THE SAME START SHARE ONE PATH', 3.2)
    tr = Trie(WORDS, 0, 66, 52, 54)
    centre(tr, 200)
    f.show(node(*tr.pos[''], '·'), .2)
    f.show(T(tr.pos[''][0] + 26, tr.pos[''][1] + 4, 'root', MU, 'start', mono=True), .2)
    f.static(T(0, 66, 'words', MU, 'start', mono=True))
    t = 1.0; made = {''}
    for wi, w in enumerate(WORDS):
        wy = 92 + wi * 30
        f.show(ocell(0, wy - 20, w, 'plain', 60, 26), t, hide=None)
        f.show(R(0, wy - 20, 60, 26, 'none', MID, 6, 2), t, hide=t + 2.6)
        new = 0
        for k in range(1, len(w) + 1):
            p = w[:k]
            if p not in made:
                f.show(edge(tr.pos[p[:-1]], tr.pos[p]) + node(*tr.pos[p], p[-1], 'vis'), t + .3 + k * .35)
                f.show(node(*tr.pos[p], p[-1]), t + 2.4)
                made.add(p); new += 1
            else:
                f.show(ring(*tr.pos[p]), t + .3 + k * .35, hide=t + 2.4)
        ex, ey = tr.pos[w]
        f.show(circ(ex, ey, NR - 3.5, 'none', 'var(--dim)', 1.1), t + .5 + len(w) * .35)
        f.show(T(66, wy - 2, '+%d node%s' % (new, '' if new == 1 else 's'), TG if new else MU, 'start', mono=True, bold=True), t + .5 + len(w) * .35)
        t += 3.0
    f.show(T(0, 92 + 5 * 30 + 10, '✓ 5 words · 9 nodes · ◎ = a word ends here', TG, 'start', bold=True), t)
    return f.render(66 + 4 * 54 + 26)


# ---------------------------------------------------------------- walk helper
def walk_fig(pre, cap_, aria, word, lines, kind, words=WORDS):
    """kind: 'search' (needs end mark), 'prefix', 'insert'."""
    f = Fig(pre, W, aria, cap_, 3.2)
    code = f.add_code(0, CY, lines, 270)
    X0 = code.w + 40
    all_words = words + ([word] if kind == 'insert' else [])
    tr = Trie(all_words, 0, 80, 46, DY)
    centre(tr, X0)
    base = Trie(words, 0, 0)
    exists = set(base.kids)
    tr.end = set(words)
    tr.draw(f, .2, .06, only=exists)
    # the query word as cells; the current char is ringed
    f.show(T(X0, 34, kind if kind != 'prefix' else 'starts_with', MU, 'start', mono=True), .8)
    qx = X0 + 90
    for k, ch in enumerate(word):
        f.show(ocell(qx + k * 30, 16, ch, 'plain', 26, 26), .9 + k * .05)
    sy = 80 + 4 * DY + 30
    f.slot('s', X0, sy); f.slot('v', X0, sy + 22)
    t = 2.0; p = ''
    f.line(t, 0); f.mover('p', probe(), t, *tr.pos['']); f.say('s', t, 'node = root', PT); t += 1.0
    ok = True
    for k, ch in enumerate(word):
        f.line(t, 1)
        f.show(cring(qx + k * 30, 16, 26, 26), t, hide=t + 1.6)
        q = p + ch
        f.line(t + .4, 2)
        if q in exists:
            f.say('v', t + .4, "'%s' in node → step down" % ch, TX)
            f.line(t + .9, 3 if kind != 'insert' else 2)
            f.move('p', t + 1.0, *tr.pos[q]); f.say('s', t + 1.0, 'node = "%s"' % q, PT)
            f.show(node(*tr.pos[q], ch, 'vis', end=q in tr.end), t + 1.3)
            f.show(ocell(qx + k * 30, 16, ch, 'vis', 26, 26), t + 1.3)
        else:
            if kind == 'insert':
                f.say('v', t + .4, "'%s' missing → create it" % ch, TG, True)
                f.move('p', t + 1.0, *tr.pos[q]); f.say('s', t + 1.0, 'node = "%s" (new)' % q, PT)
                f.show(edge(tr.pos[p], tr.pos[q]) + node(*tr.pos[q], ch, 'vis'), t + .9)
                f.show(ocell(qx + k * 30, 16, ch, 'vis', 26, 26), t + 1.3)
            else:
                f.say('v', t + .4, "'%s' not in node → stop" % ch, TX)
                f.show(ocell(qx + k * 30, 16, ch, 'grey', 26, 26), t + 1.1)
                ok = False; t += 1.8; break
        p = q; t += 1.8
    f.clear('v', t)
    return f, tr, code, t, p, ok, sy, qx


def search_fig():
    lines = ['node = root', 'for ch in word:', '    if ch not in node: return False', '    node = node[ch]', 'return END in node']
    f, tr, code, t, p, ok, sy, qx = walk_fig('tr-p1-', 'SEARCH "cat" · ONE STEP PER LETTER, THEN CHECK THE END MARK',
        'Search cat in the trie of car, cart, cat, dog, do. From the root step to c, then a, then t: each letter is a child. At t the end mark is there, so cat is a stored word. Three steps for three letters, whatever the number of words.',
        'cat', lines, 'search')
    f.line(t, 4); x, y = tr.pos[p]
    f.say('s', t, 'END in node → True', PT); t += .8
    f.hide('p', t)
    f.show(node(x, y, 't', 'fill', end=True), t)
    f.show(T(x, y + 36, '✓ found', TG, mono=True, bold=True), t + .2)
    f.say('s', t + .3, 'found "cat" · 3 steps for 3 letters · O(L)', TG, True)
    return f.render(max(code.y + code.h(), sy + 34))


def prefix_fig():
    lines = ['node = root', 'for ch in prefix:', '    if ch not in node: return False', '    node = node[ch]', 'return True']
    f, tr, code, t, p, ok, sy, qx = walk_fig('tr-p2-', 'PREFIX "ca" · SAME WALK, NO END CHECK',
        'starts_with ca in the same trie. Step to c, then a. The walk did not fall off, so some word starts with ca: everything under a, car, cart and cat, is the answer set. A hash map would have to scan every key.',
        'ca', lines, 'prefix')
    f.line(t, 4); x, y = tr.pos[p]
    f.say('s', t, 'walk did not fall off → True', PT); t += .8
    f.hide('p', t)
    f.show(node(x, y, 'a', 'fill'), t)
    sub = [q for q in tr.pos if q.startswith('ca') and q != 'ca']
    for k, q in enumerate(sorted(sub)): f.show(node(*tr.pos[q], q[-1], 'vis', end=q in tr.end), t + .3 + k * .2)
    f.show(T(x - 26, y + 5, '✓ prefix', TG, 'end', mono=True, bold=True), t + .2)
    f.say('s', t + .4, 'under "ca": car · cart · cat · O(L) to get there', TG, True)
    return f.render(max(code.y + code.h(), sy + 34))


def insert_fig():
    lines = ['node = root', 'for ch in word:', '    node = node.setdefault(ch, {})', 'node[END] = True']
    f, tr, code, t, p, ok, sy, qx = walk_fig('tr-p3-', 'INSERT "dot" · WALK, CREATE WHAT IS MISSING, MARK THE END',
        'Insert dot. d and o already exist, so the walk just steps down. t is missing under o, so one new node is created. The end mark goes on the new t. Cost: one step per letter.',
        'dot', lines, 'insert')
    f.line(t, 3); x, y = tr.pos[p]
    f.say('s', t, 'node[END] = True', PT); t += .8
    f.hide('p', t)
    f.show(node(x, y, 't', 'fill', end=True), t)
    f.show(T(x + 26, y + 5, '✓ inserted', TG, 'start', mono=True, bold=True), t + .2)
    f.say('s', t + .3, '2 nodes reused · 1 created · O(L)', TG, True)
    return f.render(max(code.y + code.h(), sy + 34))


def endmark_fig():
    f = Fig('tr-p4-', W, 'Search ca in a trie that holds only car. The walk reaches a without falling off, but a has no end mark, so ca is not a word. Then search car: the walk reaches r, which has the end mark, so car is a word.',
            'WHY THE END MARK · "ca" IS ON THE PATH OF "car" BUT IS NOT A WORD', 3.2)
    tr = Trie(['car'], 0, 70, 46, DY)
    for k, (word, X) in enumerate((('ca', 160), ('car', 480))):
        tr2 = Trie(['car'], X, 70, 46, DY)
        tr2.draw(f, .2 + k * .1)
        f.show(T(X - 40, 40, 'search("%s")' % word, MU, 'start', mono=True), .6)
    t = 1.4
    for k, (word, X) in enumerate((('ca', 160), ('car', 480))):
        tr2 = Trie(['car'], X, 70, 46, DY)
        key = 'p%d' % k
        f.mover(key, probe(), t, *tr2.pos['']); t += .7
        for j in range(1, len(word) + 1):
            f.move(key, t, *tr2.pos[word[:j]])
            f.show(node(*tr2.pos[word[:j]], word[j - 1], 'vis', end=word[:j] == 'car'), t + .3); t += .8
        x, y = tr2.pos[word]
        f.hide(key, t)
        if word == 'ca':
            f.show(T(x + 26, y + 5, 'no ◎ → False', MU, 'start', mono=True, bold=True), t)
        else:
            f.show(node(x, y, 'r', 'fill', end=True), t)
            f.show(T(x + 26, y + 5, '◎ → True', TG, 'start', mono=True, bold=True), t)
        t += 1.0
    f.show(T(160 - 40, 70 + 3 * DY + 30, '✓ without the end mark every prefix would count as a word', TG, 'start', bold=True), t)
    return f.render(70 + 3 * DY + 42)


def cost_fig():
    f = Fig('tr-p5-', W, 'Cost of a lookup. A word of 3 letters takes 3 steps whether the trie holds 5 words or 5 million. The graph plots steps against the number of stored words: a flat line at L for the trie, against a rising line for scanning every word for a prefix.',
            'COST · STEPS = LETTERS IN THE WORD, NOT WORDS STORED', 3.2)
    for k, (lab, n) in enumerate((('5 words', 5), ('5,000,000 words', 5000000))):
        y = 50 + k * 50
        f.static(T(0, y + 20, lab, MU, 'start', mono=True))
        for j, ch in enumerate('cat'):
            f.show(ocell(150 + j * 40, y, ch, 'plain'), .2 + k * .1)
        for j, ch in enumerate('cat'):
            f.show(ocell(150 + j * 40, y, ch, 'vis'), 1.0 + k * 1.6 + j * .4)
        f.show(T(280, y + 20, '3 steps', TG, 'start', mono=True, bold=True), 2.2 + k * 1.6)
    t = 4.8
    px, py = graph(f, 70, 180, 560, 160, 100, 100, [
        (lambda n: n, '', 'var(--ghost)', 2, 30),
        (lambda n: 3, 'trie: O(L), L = 3', TG, 2.6, 70)], t, xt=(25, 50, 75, 100), yt=(25, 50, 75, 100), xl='words', yl='steps')
    f.show(T(px(50) - 8, py(50) - 8, 'hash map, prefix scan: O(n)', MU, 'end', mono=True, bold=True), t + 1.2)
    f.show(T(70, 386, 'exact lookup: a hash map is O(L) too · prefix lookup: only the trie stays O(L)', TG, 'start', bold=True), t + 3.4)
    return f.render(396)


# ---------------------------------------------------------------- patterns
def autocomplete_fig():
    lines = ['node = walk(root, prefix)', 'def dfs(node, path):', '    if END in node: out.append(path)', '    for ch in node:', '        dfs(node[ch], path + ch)']
    f = Fig('tr-q1-', W, 'Autocomplete ca. First walk to the node for ca. Then a depth-first walk under it collects every word that ends there: car, cart, cat, in alphabetical order. Nodes outside the ca subtree are never touched.',
            'AUTOCOMPLETE · WALK TO THE PREFIX, THEN COLLECT THE SUBTREE', 3.2)
    code = f.add_code(0, CY, lines, 270)
    X0 = code.w + 40
    tr = Trie(WORDS, 0, 80, 46, DY); centre(tr, X0)
    tr.draw(f)
    f.show(chip(W - 130, 26, 'prefix = "ca"'), .8)
    oy = 80 + 4 * DY + 32
    out_x = X0 + 50
    f.static(T(out_x - 10, oy + 20, 'out', MU, 'end', mono=True))
    f.slot('s', X0, oy + 60)
    t = 1.6
    f.line(t, 0); f.mover('p', probe(), t, *tr.pos['']); t += .6
    for q in ('c', 'ca'):
        f.move('p', t, *tr.pos[q]); f.show(node(*tr.pos[q], q[-1], 'vis'), t + .3); t += .8
    f.say('s', t - .6, 'walk to "ca"', PT)
    for q in ('d', 'do', 'dog'): f.show(node(*tr.pos[q], q[-1], 'grey', end=q in tr.end), t)
    t += .6
    k = 0
    seq = ['car', 'cart', 'cat']
    for q in seq:
        f.line(t, 4); f.move('p', t, *tr.pos[q]); f.say('s', t, 'dfs("%s")' % q, PT); t += .8
        f.line(t, 2)
        f.show(node(*tr.pos[q], q[-1], 'vis', end=True), t)
        f.show(ocell(out_x + k * 64, oy, q, 'vis', 58, 30), t + .2); k += 1
        f.say('s', t, 'END → out.append("%s")' % q, TG, True); t += 1.0
    f.hide('p', t); f.line(t, 0)
    for j, q in enumerate(seq): f.show(ocell(out_x + j * 64, oy, q, 'fill', 58, 30), t + j * .06)
    f.say('s', t + .2, '✓ 3 suggestions · dog, do never visited', TG, True)
    return f.render(max(code.y + code.h(), oy + 72))


def prune_fig():
    f = Fig('tr-q2-', W, 'Word search on a grid with the trie of cat and car. From c the walk moves to a, which is in the trie, then to t: cat is found. Another path from c tries o: no child o under c, so that branch stops right away instead of exploring further.',
            'PRUNE A SEARCH · STOP AS SOON AS THE PATH IS NO PREFIX', 3.2)
    grid = ['cat', 'oxr', 'dzq']
    gx, gy, cw = 0, 50, 46
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            f.show(ocell(gx + j * cw, gy + i * cw, ch, 'plain', 40, 40), .2 + (i * 3 + j) * .04)
    tr = Trie(['cat', 'car'], 0, 60, 46, DY); centre(tr, 200, 560)
    tr.draw(f, .3)
    f.static(T(gx, 36, 'grid', MU, 'start', mono=True) + T(tr.pos[''][0] - 40, 36, 'trie: cat · car', MU, 'start', mono=True))
    f.slot('s', 0, 240); f.slot('v', 0, 262)
    cell = lambda i, j: (gx + j * cw, gy + i * cw)
    t = 1.4
    f.mover('g', lambda x, y: cring(x, y, 40, 40), t, *cell(0, 0))
    f.mover('p', probe(), t, *tr.pos['c'])
    f.show(ocell(*cell(0, 0), 'c', 'vis', 40, 40), t + .2); f.show(node(*tr.pos['c'], 'c', 'vis'), t + .2)
    f.say('s', t, 'start at c · trie has c', PT); t += 1.4
    f.move('g', t, *cell(1, 0)); f.say('s', t, 'try c → o', PT)
    f.say('v', t + .5, "no child 'o' under c → stop this branch", TX)
    f.show(ocell(*cell(1, 0), 'o', 'grey', 40, 40), t + .8)
    for (i, j) in ((2, 0), (2, 1)): f.show(ocell(*cell(i, j), grid[i][j], 'grey', 40, 40), t + 1.0)
    f.clear('v', t + 2.2); t += 2.4
    f.move('g', t, *cell(0, 1)); f.move('p', t, *tr.pos['ca']); f.say('s', t, 'try c → a · trie has ca', PT)
    f.show(ocell(*cell(0, 1), 'a', 'vis', 40, 40), t + .4); f.show(node(*tr.pos['ca'], 'a', 'vis'), t + .4); t += 1.4
    f.move('g', t, *cell(0, 2)); f.move('p', t, *tr.pos['cat']); f.say('s', t, 'try ca → t · trie has cat ◎', PT); t += 1.2
    f.hide('g', t); f.hide('p', t)
    f.show(ocell(*cell(0, 2), 't', 'fill', 40, 40), t); f.show(node(*tr.pos['cat'], 't', 'fill', end=True), t)
    f.say('s', t + .2, '✓ found "cat" · the "co…" branch died after one step', TG, True)
    return f.render(272)


def xor_fig():
    nums = [3, 10, 5]
    f = Fig('tr-q3-', W, 'Binary trie of 3, 10 and 5 written as 4 bits: 0011, 1010, 0101. To find the best XOR partner for 5, 0101, walk from the top bit and take the opposite bit whenever it exists: want 1, take 1; want 0, take 0; want 1, missing, take 0; want 0, take 0. The path is 1010 = 10, and 5 XOR 10 = 15.',
            'BINARY TRIE · MAXIMUM XOR = ALWAYS TRY THE OPPOSITE BIT', 3.2)
    bits = [format(n, '04b') for n in nums]
    tr = Trie(bits, 0, 60, 56, 46, root_label='·'); centre(tr, 220)
    for k, (n, b) in enumerate(zip(nums, bits)):
        f.show(T(0, 70 + k * 26, '%2d = %s' % (n, b), MU, 'start', mono=True), .2 + k * .1)
    tr.end = set()
    tr.draw(f, .4, .05)
    for b, n in zip(bits, nums):
        x, y = tr.pos[b]
        f.show(T(x, y + 32, str(n), FA, cls='sv-s', mono=True), .9)
    q = '0101'
    f.show(chip(0, 160, 'x = 5 = 0101'), 1.2)
    f.slot('s', 0, 290); f.slot('v', 0, 312)
    t = 2.2; p = ''
    f.mover('p', probe('node', 'r'), t, *tr.pos['']); t += .8
    for k, bq in enumerate(q):
        want = '1' if bq == '0' else '0'
        take = want if p + want in tr.pos else bq
        f.say('s', t, 'bit %d of x = %s → want %s' % (3 - k, bq, want), PT)
        f.say('v', t + .4, ('%s exists → take it' % want) if take == want else ('%s missing → take %s' % (want, take)), TX)
        p += take
        f.move('p', t + .6, *tr.pos[p]); f.show(node(*tr.pos[p], take, 'vis'), t + .9)
        f.clear('v', t + 1.7); t += 1.9
    f.hide('p', t)
    x, y = tr.pos[p]
    f.show(node(x, y, p[-1], 'fill'), t)
    f.say('s', t + .2, '✓ partner 1010 = 10 · 5 XOR 10 = 1111 = 15 · 4 steps for 4 bits', TG, True)
    return f.render(322)


figs = {'m1': model_fig(), 'p1': search_fig(), 'p2': prefix_fig(), 'p3': insert_fig(), 'p4': endmark_fig(), 'p5': cost_fig(),
        'q1': autocomplete_fig(), 'q2': prune_fig(), 'q3': xor_fig()}
dump('trie', figs)
print('ok', len(figs))
