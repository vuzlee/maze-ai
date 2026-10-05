"""Figures for content/01-dsa/04-algorithms/backtracking. Writes /tmp/dsa/backtracking.json."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from algo4 import *

figs = {}

class Tree:
    """Decision tree laid out by leaf order. nodes: id -> (parent, label, edge label)."""
    def __init__(s, x0, y0, dx, dy, r=15):
        s.x0, s.y0, s.dx, s.dy, s.r = x0, y0, dx, dy, r
        s.kids, s.lab, s.elab, s.depth, s.pos = {}, {}, {}, {}, {}
    def add(s, nid, parent, label, elab=''):
        s.kids.setdefault(nid, []); s.lab[nid] = label; s.elab[nid] = elab
        s.depth[nid] = 0 if parent is None else s.depth[parent] + 1
        s.par = getattr(s, 'par', {}); s.par[nid] = parent
        if parent is not None: s.kids[parent].append(nid)
    def layout(s, root):
        c = [0]
        def go(n):
            if not s.kids[n]: s.pos[n] = (s.x0 + c[0] * s.dx, s.y0 + s.depth[n] * s.dy); c[0] += 1
            else:
                for k in s.kids[n]: go(k)
                xs = [s.pos[k][0] for k in s.kids[n]]
                s.pos[n] = ((min(xs) + max(xs)) / 2, s.y0 + s.depth[n] * s.dy)
        go(root)
    def edge(s, n, c=RULE_HI, sw=1.4, dash=None):
        p = s.par[n]; (x1, y1), (x2, y2) = s.pos[p], s.pos[n]
        o = edge(x1, y1, x2, y2, c, sw, s.r, s.r, dash)
        if s.elab[n]:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            o += T(mx + (-8 if x2 < x1 else 8 if x2 > x1 else 8), my + 2, esc(s.elab[n]), MU, 'end' if x2 < x1 else 'start', cls='sv-s', mono=True)
        return o
    def node(s, n, kind='n'):
        x, y = s.pos[n]; return node(x, y, s.lab[n], kind, s.r)

def main():
    # ---------------------------------------------------------------- 1.1 choose, explore, unchoose (subsets of [1,2,3])
    def subsets():
        nums = [1, 2, 3]
        lines = ['def bt(start):', '    res.append(path[:])', '    for i in range(start, len(a)):',
                 '        path.append(a[i])', '        bt(i + 1)', '        path.pop()']
        code = Code2(0, 40, lines)
        X0 = code.w + 40
        tr = Tree(X0 + 10, 66, 52, 58, 16)
        tr.add('r', None, '∅')
        def build(nid, start, path):
            for i in range(start, 3):
                c = nid + str(nums[i]); tr.add(c, nid, ''.join(map(str, path + [nums[i]])), '+%d' % nums[i]); build(c, i + 1, path + [nums[i]])
        build('r', 0, []); tr.layout('r')
        f = Anim('bt-m1-', 760, 0, 'Subsets of 1 2 3 as a decision tree. Going down appends a number to path (choose), coming back up pops it (unchoose). '
                 'Every node visited is recorded: 8 subsets.', 'CHOOSE · EXPLORE · UNCHOOSE · ALL SUBSETS OF [1, 2, 3]', 3.2)
        f.static(code.svg())
        f.show(chip(X0, 22, 'goal: every subset'), .6)
        # path box (right bottom)
        PY = 300; PX = X0
        for n in tr.pos:
            f.show(tr.node(n, 'n'), .3)
            if n != 'r': f.show(tr.edge(n, 'var(--rule)', 1.2, '3 3'), .3)
        t = 1.8; bar = []; res = []
        pathcells = []   # list of (value, show_t)
        PATHX = PX + 44
        def visit(n, t, depth):
            bar.append((t, 1))
            if n != 'r': f.show(tr.edge(n, MID, 2), t - .4)
            f.show(nring(*tr.pos[n], 16), t, hide=t + .9)
            f.show(tr.node(n, 'b'), t + .3)
            res.append(tr.lab[n]); t += 1.0
            for k in tr.kids[n]:
                v = int(tr.lab[k][-1])
                bar.append((t, 2)); bar.append((t + .3, 3))
                pc = box(PATHX + depth * 38, PY, v, 34, 32, 'v', True)
                ts = t + .4
                t = visit(k, t + .9, depth + 1)
                bar.append((t, 4)); bar.append((t + .1, 5))
                f.show(pc, ts, hide=t + .3)
                f.show(nring(*tr.pos[n], 16), t + .2, hide=t + .7)
                t += .8
            return t
        t = visit('r', t, 0)
        end = t
        code.run(f, bar + [(end, 0)])
        f.show(lab(PX, PY + 22, 'path', MU), .3, hide=end)
        for n in tr.pos: f.show(tr.node(n, 'f'), end + .05 * len(n))
        assert len(res) == 8
        f.show(lab(PX, PY + 22, '✓ 8 subsets = 2³ · every node is one subset, path is empty again', TG, bold=True), end + .4)
        f.h = PY + 40
        return f.render()
    figs['m1'] = subsets()

    # ---------------------------------------------------------------- 1.2 pruning (combination sum target 5 from [2,3,5]? use subsets of [3,2,4] sum<=5)
    def prune():
        a = [1, 2, 3, 4]; target = 5
        f = Anim('bt-m2-', 760, 330, 'Pick numbers from 1 2 3 4 adding up to 5, each once. A branch whose sum is already over 5 is cut at once: its whole subtree is never built. '
                 'Answers 1+4 and 2+3.', 'PRUNING · CUT A BRANCH AS SOON AS IT CANNOT WORK · SUM = 5', 3.2)
        tr = Tree(70, 70, 84, 62, 16)
        tr.add('r', None, '0')
        order = []
        def build(nid, start, s):
            for i in range(start, 4):
                c = nid + str(a[i]); ns = s + a[i]; tr.add(c, nid, str(ns), '+%d' % a[i]); order.append(c)
                if ns < target: build(c, i + 1, ns)
        build('r', 0, 0); tr.layout('r')
        f.show(chip(40, 22, 'goal: sum = 5'), .6)
        t = 1.6; SY = 330 - 12; hits = []
        f.show(tr.node('r', 'b'), t); t += .6
        def visit(n, t):
            for k in tr.kids[n]:
                s = int(tr.lab[k])
                f.show(tr.edge(k, MID, 2), t)
                f.show(nring(*tr.pos[k], 16), t + .3, hide=t + 1.2)
                if s == target:
                    f.show(tr.node(k, 'f'), t + .5); hits.append(k)
                    f.show(st(40, SY, 'sum %s = 5 → record %s' % ('+'.join(k[1:]), '+'.join(k[1:])), TX), t + .3, hide=t + 1.2); t += 1.4
                elif s > target:
                    f.show(tr.node(k, 'g'), t + .5)
                    f.show(cross(tr.pos[k][0], tr.pos[k][1] + 28, 5, MID, 2), t + .6)
                    f.show(st(40, SY, 'sum %d > 5 → cut, do not go deeper' % s, TX), t + .3, hide=t + 1.2); t += 1.4
                else:
                    f.show(tr.node(k, 'b'), t + .5)
                    f.show(st(40, SY, 'sum %d < 5 → go deeper' % s, TX), t + .3, hide=t + 1.0); t += 1.1
                    t = visit(k, t)
                    if not tr.kids[k]: pass
            return t
        for n in tr.pos:
            f.show(tr.node(n, 'n'), .2)
            if n != 'r': f.show(tr.edge(n, 'var(--rule)', 1.2, '3 3'), .2)
        t = visit('r', t)
        total = 2 ** 4
        f.show(lab(40, SY, '✓ 2 answers: 1+4 and 2+3 · %d branches cut before going deeper' % len([n for n in tr.pos if int(tr.lab[n]) > target]), TG, bold=True), t + .3)
        assert sorted(hits) == ['r14', 'r23']
        return f.render()
    figs['m2'] = prune()

    # ---------------------------------------------------------------- 1.3 tree size growth: 2^n vs n!
    def growth():
        f = Anim('bt-m3-', 760, 330, 'Unpruned tree sizes. Subsets: every element in or out, 2 to the n leaves. Permutations: n choices, then n−1, n!. '
                 'At n = 10: 1,024 vs 3,628,800. Pruning is what keeps real problems small.', 'TREE SIZE · 2ⁿ SUBSETS vs n! PERMUTATIONS', 3)
        gx, gy, gw, gh = 70, 50, 560, 220
        NM = 10; YM = 7   # log10 axis
        px = lambda n: gx + n / NM * gw; py = lambda v: gy + gh - v / YM * gh
        ax = axes(gx, gy, gw, gh, (2, 4, 6, 8, 10), (), 'n', 'leaves', px, py)
        for e in range(0, 8, 2): ax += T(gx - 8, py(e) + 4, '10' + '⁰¹²³⁴⁵⁶⁷'[e], FA, 'end', cls='sv-s', mono=True) + L(gx, py(e), gx + gw, py(e), 'var(--rule)', 1, '2 4')
        f.show(ax, .3)
        sub = [(n, math.log10(2 ** n)) for n in range(1, 11)]
        per = [(n, math.log10(math.factorial(n))) for n in range(1, 11)]
        t = 1.2
        f.show(poly([(px(n), py(v)) for n, v in sub], TG, 2.6) + lab(px(10) + 6, py(sub[-1][1]) + 4, '2ⁿ', TG, bold=True), t, d=.8)
        for k, (n, v) in enumerate(sub): f.show(dot(px(n), py(v), TG), t + .5 + k * .08)
        t += 1.8
        f.show(poly([(px(n), py(v)) for n, v in per], MID, 2.6) + lab(px(10) + 6, py(per[-1][1]) + 4, 'n!', MID, bold=True), t, d=.8)
        for k, (n, v) in enumerate(per): f.show(dot(px(n), py(v), MID), t + .5 + k * .08)
        t += 1.8
        f.show(st(px(10) - 6, py(per[-1][1]) - 12, '10! = 3,628,800', MID, True, 'end') + st(px(10) - 6, py(sub[-1][1]) + 22, '2¹⁰ = 1,024', TG, True, 'end'), t)
        f.show(lab(gx + gw, gy + gh + 40, 'log scale · each step up is ×10 · prune early or the tree explodes', TG, 'end', True), t + .6)
        return f.render()
    figs['m3'] = growth()

    # ---------------------------------------------------------------- 2.1 subsets with duplicates (subsets II)
    def subsets_dup():
        a = [1, 2, 2]
        f = Anim('bt-q1-', 760, 300, 'Subsets of 1 2 2, sorted. At one level, the second 2 would start the same branch again, so it is skipped: '
                 'if i > start and a[i] == a[i-1]: continue. 6 subsets, no duplicates.', 'SUBSETS · SKIP THE SAME VALUE ON ONE LEVEL · [1, 2, 2]', 3.2); f.h = 312
        tr = Tree(80, 76, 96, 60, 16)
        tr.add('r', None, '∅'); skips = []
        def build(nid, start, path):
            for i in range(start, 3):
                c = nid + '_' + str(i)
                dup = i > start and a[i] == a[i - 1]
                tr.add(c, nid, ''.join(map(str, path + [a[i]])), '+%d' % a[i])
                if dup: skips.append(c); continue
                build(c, i + 1, path + [a[i]])
        build('r', 0, []); tr.layout('r')
        f.show(chip(60, 22, 'goal: subsets without repeats'), .6)
        for n in tr.pos:
            f.show(tr.node(n, 'n'), .2)
            if n != 'r': f.show(tr.edge(n, 'var(--rule)', 1.2, '3 3'), .2)
        SY = 306; t = 1.6; res = []
        f.show(tr.node('r', 'b'), t); res.append('∅'); t += .6
        def visit(n, t):
            for k in tr.kids[n]:
                f.show(tr.edge(k, MID, 2), t)
                f.show(nring(*tr.pos[k], 16), t + .3, hide=t + 1.3)
                if k in skips:
                    f.show(tr.node(k, 'g'), t + .5); f.show(cross(tr.pos[k][0], tr.pos[k][1] + 28, 5, MID, 2), t + .6)
                    f.show(st(60, SY, 'a[%s] = 2 == a[%d] on this level → skip' % (k[-1], int(k[-1]) - 1), TX), t + .3, hide=t + 1.3); t += 1.5
                else:
                    f.show(tr.node(k, 'b'), t + .5); res.append(tr.lab[k])
                    f.show(st(60, SY, 'record %s' % tr.lab[k], TX), t + .3, hide=t + 1.0); t += 1.1
                    t = visit(k, t)
            return t
        t = visit('r', t)
        for n in tr.pos:
            if n not in skips: f.show(tr.node(n, 'f'), t)
        assert sorted(res) == sorted(['∅', '1', '12', '122', '2', '22'])
        f.show(lab(60, SY, '✓ 6 subsets: ∅ 1 12 122 2 22 · sort first, then skip on the same level', TG, bold=True), t + .3)
        return f.render()
    figs['q1'] = subsets_dup()

    # ---------------------------------------------------------------- 2.2 permutations
    def perms():
        a = [1, 2, 3]
        f = Anim('bt-q2-', 760, 300, 'Permutations of 1 2 3. Every level loops over all numbers and skips the ones already used. 3 then 2 then 1 choices: 6 leaves.',
                 'PERMUTATIONS · EVERY LEVEL TRIES ALL UNUSED · [1, 2, 3]', 3.2); f.h = 320
        tr = Tree(60, 70, 58, 66, 16); tr.add('r', None, '·')
        def build(nid, path):
            for v in a:
                if v in path: continue
                c = nid + str(v); tr.add(c, nid, str(v), ''); build(c, path + [v])
        build('r', []); tr.layout('r')
        f.show(chip(60, 22, 'goal: every order'), .6)
        UX = 470
        f.static(lab(UX, 96, 'used', MU))
        for k, v in enumerate(a): f.show(box(UX + 44 + k * 40, 76, v, 34, 32, 'n', True), .3)
        for n in tr.pos:
            f.show(tr.node(n, 'n'), .2)
            if n != 'r': f.show(tr.edge(n, 'var(--rule)', 1.2, '3 3'), .2)
        SY = 312; t = 1.6; leaves = []
        def visit(n, t, used):
            for k in tr.kids[n]:
                v = int(k[-1])
                f.show(tr.edge(k, MID, 2), t); f.show(nring(*tr.pos[k], 16), t + .2, hide=t + .8)
                f.show(tr.node(k, 'b'), t + .3)
                f.show(box(UX + 44 + (v - 1) * 40, 76, v, 34, 32, 'g', True), t + .3, hide=None)
                ts = t + .3
                if not tr.kids[k]:
                    leaves.append(k[1:])
                    f.show(st(UX, 150, 'leaf → record %s' % k[1:], TX), t + .3, hide=t + .9)
                    t += 1.0
                else:
                    t = visit(k, t + .9, used + [v])
                f.show(box(UX + 44 + (v - 1) * 40, 76, v, 34, 32, 'n', True), t)
                t += .2
            return t
        t = visit('r', t, [])
        for n in tr.pos:
            if not tr.kids[n]: f.show(tr.node(n, 'f'), t)
        assert len(leaves) == 6
        f.show(lab(60, SY, '✓ 6 orders = 3 · 2 · 1 = n! · a used[] mark is set going down, cleared coming up', TG, bold=True), t + .3)
        return f.render()
    figs['q2'] = perms()

    # ---------------------------------------------------------------- 2.3 grid path (word search)
    def grid():
        G = ['ABCE', 'SFCS', 'ADEE']; word = 'ABCCED'
        f = Anim('bt-q3-', 760, 250, 'Word search for ABCCED in a 3 by 4 grid. From A, step to a neighbour holding the next letter, mark it used, '
                 'go on; a dead end is unmarked on the way back. Path A B C C E D found.', 'GRID PATH · FIND "ABCCED" · MARK, EXPLORE, UNMARK', 3.2); f.h = 236
        CW = 44; X0, Y0 = 40, 40
        xy = lambda r, c: (X0 + c * (CW + 20), Y0 + r * (CW + 20))
        for r in range(3):
            for c in range(4): f.show(box(*xy(r, c), G[r][c], CW, CW), .2 + (r * 4 + c) * .03)
        WX = 340
        f.static(lab(WX, 60, 'word', MU))
        for k, ch in enumerate(word): f.show(box(WX + 50 + k * 36, 42, ch, 32, 30, 'n', True), .4)
        f.show(chip(WX, 96, 'goal: "ABCCED" in the grid'), .8)
        # scripted DFS: (cell, ok, note)
        steps = [((0, 0), 1, 'A matches word[0] → mark'), ((0, 1), 1, 'B matches → mark'), ((0, 2), 1, 'C matches → mark'),
                 ((0, 3), 0, 'E ≠ C → back'), ((1, 2), 1, 'C matches → mark'), ((2, 2), 1, 'E matches → mark'),
                 ((2, 3), 0, 'E ≠ D → back'), ((2, 1), 1, 'D matches → whole word found')]
        t = 2.2; k = 0; SY = 230; prev = None; marks = []
        for (r, c), ok, msg in steps:
            x, y = xy(r, c)
            f.show(ring(x, y, CW, CW), t, hide=t + 1.2)
            f.show(st(WX, SY - 60, msg, TX), t, hide=t + 1.2)
            if ok:
                f.show(box(x, y, G[r][c], CW, CW, 'b'), t + .5)
                if prev:
                    dx, dy = (x - prev[0]) / (CW + 20), (y - prev[1]) / (CW + 20)
                    ax, ay = prev[0] + CW / 2 + dx * (CW / 2 + 1), prev[1] + CW / 2 + dy * (CW / 2 + 1)
                    f.show(arrow(ax, ay, ax + dx * 18, ay + dy * 18, MID, 2, None, 6), t + .4)
                f.show(box(WX + 50 + k * 36, 42, word[k], 32, 30, 'b', True), t + .5)
                prev = (x, y); k += 1
            t += 1.4
        for (r, c), ok, _ in steps:
            if ok: f.show(box(*xy(r, c), G[r][c], CW, CW, 'f'), t)
        for j, ch in enumerate(word): f.show(box(WX + 50 + j * 36, 42, ch, 32, 30, 'f', True), t)
        f.show(lab(WX, SY - 60, '✓ found · mark a cell going in, unmark it coming back', TG, bold=True), t + .3)
        return f.render()
    figs['q3'] = grid()

    # ---------------------------------------------------------------- 2.4 build a string piece by piece (generate parentheses n=2)
    def parens():
        n = 2
        f = Anim('bt-q4-', 760, 300, 'Generate all valid strings of 2 bracket pairs. Add "(" while opens < 2, add ")" while closes < opens. Branches that would break the rule are never made. Answers (()) and ()().',
                 'BUILD A STRING · ADD "(" OR ")" ONLY WHEN STILL VALID · n = 2', 3.2); f.h = 326
        tr = Tree(80, 70, 70, 52, 18); tr.add('r', None, '·')
        cut = []
        def build(nid, s, o, c):
            if len(s) == 2 * n: return
            for ch in '()':
                no, nc = o + (ch == '('), c + (ch == ')')
                cid = nid + ch
                tr.add(cid, nid, s + ch, ch)
                if no > n or nc > no: cut.append(cid); continue
                build(cid, s + ch, no, nc)
        build('r', '', 0, 0); tr.layout('r')
        def nd(nid, kind):
            x, y = tr.pos[nid]; s = tr.lab[nid]; w = 16 + len(s) * 8
            if kind == 'n': return R(x - w / 2, y - 13, w, 26, 'var(--bg)', RULE_HI, 6, 1.2) + T(x, y + 4, esc(s), TX, mono=True, bold=True)
            if kind == 'g': return R(x - w / 2, y - 13, w, 26, 'var(--sunk)', 'var(--rule)', 6, 1) + T(x, y + 4, esc(s), GH, mono=True)
            if kind == 'b': return R(x - w / 2, y - 13, w, 26, 'var(--bg)', 'none', 6) + R(x - w / 2, y - 13, w, 26, it('.12'), TG, 6, 1.3) + T(x, y + 4, esc(s), TG, mono=True, bold=True)
            return R(x - w / 2, y - 13, w, 26, TG, TG, 6, 1.2) + T(x, y + 4, esc(s), ON, mono=True, bold=True)
        tr.r = 14
        f.show(chip(80, 22, 'goal: every valid string'), .6)
        for nid in tr.pos:
            f.show(nd(nid, 'n'), .2)
            if nid != 'r': f.show(tr.edge(nid, 'var(--rule)', 1.2, '3 3'), .2)
        SY = 318; t = 1.6; res = []
        def visit(nid, t, o, c):
            for k in tr.kids[nid]:
                ch = k[-1]; no, nc = o + (ch == '('), c + (ch == ')')
                x, y = tr.pos[k]; w = 16 + len(tr.lab[k]) * 8
                f.show(tr.edge(k, MID, 2), t); f.show(ring(x - w / 2, y - 13, w, 26, 6), t + .2, hide=t + 1.1)
                if k in cut:
                    why = 'opens %d > 2' % no if no > n else 'closes %d > opens %d' % (nc, no)
                    f.show(nd(k, 'g'), t + .4); f.show(st(80, SY, '%s: %s → cut' % (tr.lab[k], why), TX), t + .2, hide=t + 1.1); t += 1.3
                else:
                    f.show(nd(k, 'b'), t + .4)
                    if len(tr.lab[k]) == 2 * n:
                        res.append(tr.lab[k]); f.show(st(80, SY, '%s: length 4 → record' % tr.lab[k], TX), t + .2, hide=t + 1.1); t += 1.3
                    else:
                        t = visit(k, t + .9, no, nc)
            return t
        t = visit('r', t, 0, 0)
        for nid in tr.pos:
            if tr.lab[nid] in ('(())', '()()'): f.show(nd(nid, 'f'), t)
        assert sorted(res) == ['(())', '()()']
        f.show(lab(80, SY, '✓ (()) and ()() · the rule cuts bad branches before they grow', TG, bold=True), t + .3)
        return f.render()
    figs['q4'] = parens()

    def queen(x, y, w, kind):
        fill, stroke, tc = (TG, TG, ON) if kind == 'f' else (it('.12'), TG, TG)
        return (R(x, y, w, w, 'var(--bg)', 'none', 5) + R(x, y, w, w, fill, stroke, 5, 1.3) +
                '<text x="%.1f" y="%.1f" text-anchor="middle" style="fill:%s;font-size:22px">♛</text>' % (x + w / 2, y + w / 2 + 8, tc))

    # ---------------------------------------------------------------- 2.5 n-queens 4x4
    def queens():
        N = 4
        f = Anim('bt-q5-', 760, 270, '4-queens. Place one queen per row. A cell attacked by an earlier queen (same column or diagonal) is skipped at once. '
                 'Row 2 dead-ends after queen at column 0, so the search backs up and moves it. Solution columns 1 3 0 2.', 'STRONG CONSTRAINTS · 4 QUEENS · CHECK EACH ROW BEFORE GOING DOWN', 3.2)
        CW = 44; X0, Y0 = 60, 40
        xy = lambda r, c: (X0 + c * (CW + 4), Y0 + r * (CW + 4))
        for r in range(N):
            for c in range(N): f.show(R(*xy(r, c), CW, CW, 'var(--bg)', RULE_HI, 5, 1.2), .2 + (r * 4 + c) * .02)
            f.static(T(X0 - 14, xy(r, 0)[1] + CW / 2 + 4, str(r), FA, cls='sv-s', mono=True))
        for c in range(N): f.static(T(xy(0, c)[0] + CW / 2, Y0 + N * (CW + 4) + 14, str(c), FA, cls='sv-s', mono=True))
        f.show(chip(300, 22, 'goal: 4 queens, no two attack'), .6)
        SX, SY = 300, 80
        t = 1.6; cols = []; q = {}
        sol = None
        def ok(r, c): return all(c != cc and abs(c - cc) != r - rr for rr, cc in enumerate(cols))
        log = []
        def bt(r):
            nonlocal sol
            if r == N: sol = list(cols); return True
            for c in range(N):
                log.append(('try', r, c, ok(r, c)))
                if ok(r, c):
                    cols.append(c); log.append(('put', r, c, None))
                    if bt(r + 1): return True
                    cols.pop(); log.append(('pop', r, c, None))
            return False
        bt(0)
        shown = {}
        for ev, r, c, good in log:
            x, y = xy(r, c)
            if ev == 'try':
                f.show(ring(x, y, CW, CW, 6), t, hide=t + .55)
                if not good:
                    g = R(x, y, CW, CW, 'var(--sunk)', 'var(--rule)', 5, 1) + cross(x + CW / 2, y + CW / 2, 6, GH, 1.8)
                    shown.setdefault((r, c), []).append([g, t + .3, None])
                    f.show(st(SX, SY, 'row %d, col %d: attacked → skip' % (r, c), TX), t, hide=t + .55)
                t += .65
            elif ev == 'put':
                qq = queen(x + 4, y + 4, CW - 8, 'b')
                shown.setdefault((r, c, 'q'), []).append([qq, t, None])
                f.show(st(SX, SY, 'row %d, col %d: safe → place, go to row %d' % (r, c, r + 1), TX), t, hide=t + .8)
                t += .9
            else:
                for key in list(shown):
                    if key[0] > r or (key[0] == r and len(key) == 3 and key[1] == c):
                        for item in shown[key]:
                            if item[2] is None: item[2] = t + .3
                f.show(st(SX, SY, 'row %d has no safe cell → remove queen (%d, %d), back up' % (r + 1, r, c), MID, True), t, hide=t + 1.4)
                t += 1.6
        for key, items in shown.items():
            for g, a_, h in items: f.show(g, a_, hide=h)
        end = t
        for r, c in enumerate(sol): f.show(queen(xy(r, c)[0] + 4, xy(r, c)[1] + 4, CW - 8, 'f'), end + r * .08)
        assert sol == [1, 3, 0, 2]
        f.show(lab(SX, SY, '✓ columns 1 3 0 2', TG, bold=True), end + .4)
        f.show(lab(SX, SY + 24, 'attacked cells are skipped before going down → most of 4⁴ = 256 boards never built', TG), end + .6)
        return f.render()
    figs['q5'] = queens()

    os.makedirs('/tmp/dsa', exist_ok=True)
    json.dump(pad(figs), open('/tmp/dsa/backtracking.json', 'w'))
    print({k: len(v) for k, v in figs.items()})

if __name__ == '__main__':
    main()
