"""LeetCode toolkit figures (content/01-dsa/05-toolkit/leetcode-toolkit).
One figure per tool: what the call does to the data. Code box left (<= 3 lines), data right.
Run: python3 tools/svgkit/dsa/leetcode_toolkit.py -> /tmp/dsa/leetcode-toolkit.json + page"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsa_overview import *

W = 760

def frame(pre, caption, aria, lines, cw=None):
    f = Anim(pre, W, 0, aria, caption, 3.2)
    code = Code2(0, 40, lines, cw)
    f.static(code.svg())
    return f, code, code.w + 36


def fig_bisect():
    a = [3, 8, 12, 16, 23, 31, 40, 47]; x = 20
    f, code, X0 = frame('lck-b1-', 'bisect_left(a, 20) · WHERE WOULD 20 GO?',
                        'bisect_left on 3 8 12 16 23 31 40 47 with x = 20. l = 0, r = 8. mid 4 holds 23, not less than 20: r = 4. mid 2 holds 12, less: l = 3. mid 3 holds 16, less: l = 4. l meets r at index 4, so 20 belongs before 23 at index 4, three looks.',
                        ['from bisect import bisect_left', 'i = bisect_left(a, 20)'])
    CW, G, CY = 44, 6, 74
    cxl = lambda i: X0 + i * (CW + G); cx = lambda i: cxl(i) + CW / 2
    for i, v in enumerate(a):
        f.show(box(cxl(i), CY, CW, 34, v) + T(cx(i), CY + 50, str(i), FA, cls='sv-s', mono=True), .2 + i * .05)
    f.show(chip(X0, 26, 'x = 20'), .9)
    SY = CY + 136
    t = 2.0
    f.show(say(X0, SY, 'l = 0 · r = 8 (one past the end)', PT), t, hide=t + 1.1)
    l, r = 0, len(a); lp = [(0, 0, 0)]; rp = [(0, 0, 0)]; mp = []; m0 = None; looks = 0; t += 1.2
    PY = CY + 58
    while l < r:
        m = (l + r) // 2; looks += 1; m0 = m if m0 is None else m0
        mp.append((t, (m - m0) * (CW + G), 0))
        f.show(say(X0, SY, 'mid = (%d + %d) // 2 = %d' % (l, r, m), MID), t, hide=t + 2.7)
        f.show(ring(cxl(m), CY, CW, 34), t + .6, hide=t + 2.7)
        less = a[m] < x
        f.show(say(X0, SY + 22, 'a[%d] = %d %s 20 → %s' % (m, a[m], '<' if less else '≥', 'l = mid + 1' if less else 'r = mid'), TX), t + .6, hide=t + 2.7)
        drop = range(l, m + 1) if less else range(m, r)
        for i in drop: f.show(dead(cxl(i), CY, CW, 34, a[i]), t + 1.6)
        if less: l = m + 1; lp.append((t + 1.8, l * (CW + G), 0))
        else: r = m; rp.append((t + 1.8, (r - len(a)) * (CW + G), 0))
        t += 3.0
    end = t
    code.track(f, [(.2, 0), (1.8, 1)])
    f.path(ptr(cx(0), PY, 'l', PT, 12), lp, 2.0, hide=end)
    # r starts one past the end: a pointer with no cell, at x of index 8
    f.path(ptr(cx(len(a)), PY, 'r', PT, 30), rp, 2.0, hide=end)
    f.path(T(cx(m0), CY - 10, 'mid', MID, mono=True, bold=True), mp, mp[0][0], hide=end)
    # answer: insertion point before a[4]
    f.show(solid(cxl(4), CY, CW, 34, 23) + L(cxl(4) - 3, CY - 6, cxl(4) - 3, CY + 40, TG, 3) + T(cx(4), CY + 76, '✓ i = 4', TG, mono=True, bold=True), end)
    f.show(say(X0, SY, '✓ 20 goes at index 4, before 23 · %d looks for %d cells' % (looks, len(a)), TG, True), end + .3)
    f.h = SY + 32
    return f.render()


def fig_counter():
    s = 'banana'
    f, code, X0 = frame('lck-c1-', 'Counter(s) · ONE PASS, ONE TALLY PER LETTER',
                        'Counter over the letters b a n a n a. Pointer i walks the six letters; each one adds 1 to its tally: b 1, a 3, n 2. Then most_common(1) picks the largest tally, a with 3.',
                        ['from collections import Counter', 'c = Counter(s)', 'c.most_common(1)'])
    CW, G, CY = 40, 6, 52
    cxl = lambda i: X0 + i * (CW + G); cx = lambda i: cxl(i) + CW / 2
    for i, ch in enumerate(s):
        f.show(box(cxl(i), CY, CW, 34, ch) + T(cx(i), CY + 50, str(i), FA, cls='sv-s', mono=True), .2 + i * .05)
    keys = ['b', 'a', 'n']; KY = CY + 112; KW = 96
    kx = lambda k: X0 + k * (KW + 14)
    f.static(T(X0, KY - 10, 'c =', MU, 'start', mono=True))
    t = 1.6; cnt = {}
    SY = KY + 84
    f.path(ptr(cx(0), CY + 56, 'i', PT, 12), [(0, 0, 0)] + [(t + k * 1.2, k * (CW + G), 0) for k in range(1, 6)], t, hide=t + 6 * 1.2)
    for k, ch in enumerate(s):
        tk = t + k * 1.2
        f.show(ring(cxl(k), CY, CW, 34), tk + .3, hide=tk + 1.1)
        new = ch not in cnt; cnt[ch] = cnt.get(ch, 0) + 1; j = keys.index(ch)
        f.show(box(kx(j), KY, KW, 34, "'%s': %d" % (ch, cnt[ch]), PT, 'var(--bg)', PT), tk + .6, hide=None if cnt[ch] == s.count(ch) else tk + 1.2 + (s.index(ch, k + 1) - k - 1) * 1.2 + .5)
        f.show(say(X0, SY, "s[%d] = '%s' → c['%s'] = %d%s" % (k, ch, ch, cnt[ch], '  (new key, starts at 0)' if new else ''), TX), tk + .3, hide=tk + 1.15)
    end = t + 6 * 1.2
    f.show(ring(kx(1), KY, KW, 34), end + .9, hide=end + 1.8)
    f.show(solid(kx(1), KY, KW, 34, "'a': 3"), end + 1.8)
    f.show(T(kx(1) + KW / 2, KY + 52, '✓ most common', TG, mono=True, bold=True), end + 2.0)
    f.show(say(X0, SY, "most_common(1) = [('a', 3)] · one pass over 6 letters", TG, True), end + 2.2)
    code.track(f, [(.2, 1), (end + .9, 2)])
    f.h = SY + 14
    return f.render()


def fig_defaultdict():
    ws = ['eat', 'tea', 'tan', 'ate', 'nat']
    f, code, X0 = frame('lck-d1-', 'defaultdict(list) · GROUP WORDS BY THEIR SORTED LETTERS',
                        'defaultdict(list) groups eat tea tan ate nat by sorted letters. eat makes key aet with a fresh empty list, then appends; tea and ate join aet; tan makes key ant; nat joins ant. No if-key-missing line is needed. Result: two groups.',
                        ['g = defaultdict(list)', 'for w in words:', "    g[''.join(sorted(w))].append(w)"])
    CW, G, CY = 56, 8, 52
    cxl = lambda i: X0 + i * (CW + G); cx = lambda i: cxl(i) + CW / 2
    for i, w in enumerate(ws):
        f.show(box(cxl(i), CY, CW, 34, w), .2 + i * .05)
    GY = CY + 110; KW = 70
    rows = {'aet': 0, 'ant': 1}; RH = 40
    f.static(T(X0, GY - 12, 'g =', MU, 'start', mono=True))
    t = 1.6; filled = {'aet': 0, 'ant': 0}
    SY = GY + 2 * RH + 26
    bar = [(.2, 0)]
    f.path(ptr(cx(0), CY + 34, 'w', PT, 12), [(0, 0, 0)] + [(t + k * 1.8, k * (CW + G), 0) for k in range(1, 5)], t, hide=t + 5 * 1.8)
    for k, w in enumerate(ws):
        tk = t + k * 1.8; key = ''.join(sorted(w)); r = rows[key]; y = GY + r * RH
        bar += [(tk, 1), (tk + .5, 2)]
        f.show(ring(cxl(k), CY, CW, 34), tk + .2, hide=tk + 1.6)
        if filled[key] == 0:
            f.show(box(X0, y, KW, 32, key, MID, vt('.08'), MID) + R(X0 + KW + 10, y, 360, 32, 'var(--bg)', RULE_HI, 6, 1) + T(X0 + KW + 22, y + 20, '[ ]', GH, 'start', mono=True), tk + .5)
            f.show(say(X0, SY, "'%s' sorted → '%s' · new key → starts as []" % (w, key), MID), tk + .5, hide=tk + 1.7)
        else:
            f.show(say(X0, SY, "'%s' sorted → '%s' · key exists" % (w, key), TX), tk + .5, hide=tk + 1.7)
        f.show(R(X0 + KW + 14 + filled[key] * 62, y + 4, 56, 24, 'var(--bg)', 'none', 4) + box(X0 + KW + 16 + filled[key] * 62, y + 4, 54, 24, w, PT, it('.08'), PT, 12), tk + 1.1)
        filled[key] += 1
    end = t + 5 * 1.8
    code.track(f, bar)
    for key, r in rows.items():
        f.show(solid(X0, GY + r * RH, KW, 32, key), end)
    f.show(say(X0, SY, '✓ 2 groups · no "if key not in g" line anywhere', TG, True), end + .3)
    f.h = SY + 14
    return f.render()


def fig_deque():
    v = [4, 7, 1, 9, 5]
    f, code, X0 = frame('lck-q1-', 'popleft() · deque TAKES THE FRONT, list SHIFTS EVERYTHING',
                        'Two rows hold 4 7 1 9 5. list.pop(0) removes 4 and the four remaining cells each slide one step left: 4 moves. deque.popleft() removes 4 and only the front marker moves: no cell moves. One move instead of n.',
                        ['a.pop(0)       # list', 'q.popleft()    # deque'])
    CW, G = 46, 8
    R1, R2 = 70, 170
    cxl = lambda i: X0 + 40 + i * (CW + G); cx = lambda i: cxl(i) + CW / 2
    f.static(T(X0, R1 + 22, 'list', MU, 'start', cls='sv-s', bold=True) + T(X0, R2 + 22, 'deque', MU, 'start', cls='sv-s', bold=True))
    t = 1.6
    # list row
    f.show(box(cxl(0), R1, CW, 34, v[0]), .2, hide=t + .9)
    for i in range(1, 5):
        f.path(box(cxl(i), R1, CW, 34, v[i]), [(0, 0, 0), (t + 1.2 + (i - 1) * .35, -(CW + G), 0)], .2 + i * .05, d=.35)
    for i in range(4): f.static(T(cx(i), R1 + 50, str(i), FA, cls='sv-s', mono=True))
    f.show(T(cx(4), R1 + 50, '4', FA, cls='sv-s', mono=True), .2, hide=t + 1.2 + 3 * .35 + .3)
    f.show(ring(cxl(0), R1, CW, 34), t, hide=t + .9)
    f.show(say(cxl(5) + 10, R1 + 22, 'take 4', MID), t + .3, hide=t + 1.1)
    for i in range(1, 5):
        f.show(say(cxl(5) + 10, R1 + 22, 'shift %d left · moves: %d' % (v[i], i), TX), t + 1.2 + (i - 1) * .35, hide=t + 1.2 + i * .35 if i < 4 else None, d=.15)
    t2 = t + 1.2 + 4 * .35 + .8
    # deque row: cells never move, the front marker does
    for i in range(5):
        f.show(box(cxl(i), R2, CW, 34, v[i]), .3 + i * .05, hide=t2 + .9 if i == 0 else None)
        f.static(T(cx(i), R2 + 50, str(i), FA, cls='sv-s', mono=True))
    f.path(ptr(cx(0), R2 + 56, 'front', PT, 12), [(0, 0, 0), (t2 + 1.2, CW + G, 0)], 1.0)
    f.show(ring(cxl(0), R2, CW, 34), t2, hide=t2 + .9)
    f.show(dead(cxl(0), R2, CW, 34, ''), t2 + .9)
    f.show(say(cxl(5) + 10, R2 + 22, 'take 4 · moves: 0', TX), t2 + .3)
    code.track(f, [(.2, 0), (t2, 1)])
    end = t2 + 2.0
    f.show(say(cxl(5) + 10, R1 + 44, 'O(n)', GH, True), end)
    f.show(say(cxl(5) + 10, R2 + 44, '✓ O(1)', TG, True), end)
    f.show(say(X0, R2 + 108, 'popleft: no cell moves · pop(0) on a list moves all n − 1', TG, True), end + .3)
    f.h = R2 + 126
    return f.render()


def fig_heap():
    h = [2, 5, 3, 8, 9, 7]; new = 1
    f, code, X0 = frame('lck-h1-', 'heappush(h, 1) · THE SMALLEST ALWAYS SITS AT THE ROOT',
                        'Min-heap 2 5 3 8 9 7 drawn as a tree with the list below. heappush adds 1 at index 6, the first free slot. 1 is smaller than its parent 3 at index 2: swap. 1 is smaller than its parent 2 at index 0: swap. 1 is now the root, h[0] = 1, after 2 swaps for 7 items, about log n.',
                        ['import heapq', 'heapq.heappush(h, 1)', 'h[0]   # smallest'])
    # tree positions
    TX0 = X0 + 40; TW = 360; TY = 50; LV = 62
    pos = {0: (TX0 + TW / 2, TY), 1: (TX0 + TW / 4, TY + LV), 2: (TX0 + 3 * TW / 4, TY + LV)}
    for i in range(3, 7):
        px, py = pos[(i - 1) // 2]; pos[i] = (px + (-1 if i % 2 else 1) * TW / 8, TY + 2 * LV)
    rr = 17
    edges = ''.join(L(pos[i][0], pos[i][1], pos[(i - 1) // 2][0], pos[(i - 1) // 2][1], RULE_HI, 1.4) for i in range(1, 6))
    f.show(edges, .2)
    f.show(L(pos[6][0], pos[6][1], pos[2][0], pos[2][1], RULE_HI, 1.4), 1.8)
    node = lambda x, y, v, c=TX, fill='var(--bg)', st=RULE_HI: '<circle cx="%.1f" cy="%.1f" r="%d" fill="%s" stroke="%s" stroke-width="1.3"/>' % (x, y, rr, fill, st) + T(x, y + 5, str(v), c, mono=True, bold=True)
    # list row
    AY = TY + 2 * LV + 46; CW, G = 40, 6
    cxl = lambda i: TX0 + i * (CW + G); cx = lambda i: cxl(i) + CW / 2
    f.static(T(X0, AY + 22, 'h', MU, 'start', mono=True, bold=True))
    vals = h[:]
    # static nodes/cells for items that never move; movers tracked separately
    path_nodes = [6, 2, 0]   # 1 travels 6 -> 2 -> 0 ; 3 travels 2 -> 6 ; 2 travels 0 -> 2
    t = 1.8
    for i, v in enumerate(h):
        if i in (0, 2): continue
        f.show(node(*pos[i], v), .3 + i * .06)
        f.show(box(cxl(i), AY, CW, 32, v) + T(cx(i), AY + 48, str(i), FA, cls='sv-s', mono=True), .4 + i * .06)
    f.show(T(cx(6), AY + 48, '6', FA, cls='sv-s', mono=True), 1.8)
    for i in (0, 2): f.static(T(cx(i), AY + 48, str(i), FA, cls='sv-s', mono=True))
    SY = AY + 76
    t1 = t + 1.2; t2 = t1 + 3.0; t3 = t2 + 3.0
    dxy = lambda a, b: (pos[b][0] - pos[a][0], pos[b][1] - pos[a][1])
    # value 3 : node 2 -> node 6 at t2 ; value 2 : node 0 -> node 2 at t3
    f.path(node(*pos[2], 3), [(0, 0, 0), (t2,) + dxy(2, 6)], .3 + 2 * .06, d=.6)
    f.path(box(cxl(2), AY, CW, 32, 3), [(0, 0, 0), (t2, cxl(6) - cxl(2), 0)], .4 + 2 * .06, d=.6)
    f.path(node(*pos[0], 2), [(0, 0, 0), (t3,) + dxy(0, 2)], .3, d=.6)
    f.path(box(cxl(0), AY, CW, 32, 2), [(0, 0, 0), (t3, cxl(2) - cxl(0), 0)], .4, d=.6)
    # new value 1 appears at slot 6 then rises
    f.path(node(*pos[6], 1, PT, it('.10'), PT), [(0, 0, 0), (t2,) + dxy(6, 2), (t3,) + dxy(6, 0)], t, d=.6)
    f.path(box(cxl(6), AY, CW, 32, 1, PT, it('.10'), PT), [(0, 0, 0), (t2, cxl(2) - cxl(6), 0), (t3, cxl(0) - cxl(6), 0)], t, d=.6)
    f.show(say(X0, SY, 'append 1 at index 6, the first free slot', PT), t, hide=t1 - .1)
    # compare 1: with parent index 2
    f.show('<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s" stroke-width="2.2"/>' % (pos[2][0], pos[2][1], rr + 4, MID), t1, hide=t2)
    f.show(say(X0, SY, 'parent of 6 = (6 − 1) // 2 = 2 · h[2] = 3', MID), t1, hide=t2 - .1)
    f.show(say(X0, SY + 22, '1 < 3 → swap', TX), t1 + .6, hide=t2 - .1)
    f.show('<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s" stroke-width="2.2"/>' % (pos[0][0], pos[0][1], rr + 4, MID), t2 + .8, hide=t3)
    f.show(say(X0, SY, 'parent of 2 = (2 − 1) // 2 = 0 · h[0] = 2', MID), t2 + .8, hide=t3 - .1)
    f.show(say(X0, SY + 22, '1 < 2 → swap', TX), t2 + 1.4, hide=t3 - .1)
    end = t3 + 1.0
    f.show(node(*pos[0], 1, ONF, TG, TG), end)
    f.show(solid(cxl(0), AY, CW, 32, 1), end)
    f.show(T(pos[0][0] + 30, pos[0][1] + 5, '✓ h[0] = 1', TG, 'start', mono=True, bold=True), end + .2)
    f.show(say(X0, SY, '2 swaps for 7 items · push and pop cost O(log n)', TG, True), end + .3)
    code.track(f, [(.2, 1), (end, 2)])
    f.h = SY + 34
    return f.render()


def fig_comp():
    a = [3, 4, 7, 6, 2]
    f, code, X0 = frame('lck-p1-', 'COMPREHENSION · FILTER AND TRANSFORM IN ONE LINE',
                        'The comprehension x*x for x in a if x is even walks 3 4 7 6 2. 3 is odd: skipped, greyed. 4 is even: 16 drops into the output. 7 odd: skipped. 6 even: 36. 2 even: 4. Result 16 36 4.',
                        ['out = [x * x for x in a', '       if x % 2 == 0]'])
    CW, G, CY = 46, 8, 60
    cxl = lambda i: X0 + 30 + i * (CW + G); cx = lambda i: cxl(i) + CW / 2
    f.static(T(X0, CY + 22, 'a', MU, 'start', mono=True, bold=True))
    for i, v in enumerate(a):
        f.show(box(cxl(i), CY, CW, 34, v) + T(cx(i), CY + 50, str(i), FA, cls='sv-s', mono=True), .2 + i * .05)
    OY = CY + 112
    f.static(T(X0, OY + 22, 'out', MU, 'start', mono=True, bold=True))
    t = 1.6; dt = 1.6; o = 0; SY = OY + 72; bar = [(.2, 0)]
    f.path(ptr(cx(0), CY + 56, 'x', PT, 12), [(0, 0, 0)] + [(t + k * dt, k * (CW + G), 0) for k in range(1, 5)], t, hide=t + 5 * dt)
    for k, x in enumerate(a):
        tk = t + k * dt
        bar += [(tk + .2, 1), (tk + .9, 0)]
        f.show(ring(cxl(k), CY, CW, 34), tk + .2, hide=tk + 1.4)
        if x % 2:
            f.show(say(X0, SY, '%d %% 2 = 1 → skip' % x, TX), tk + .2, hide=tk + dt - .1)
            f.show(dead(cxl(k), CY, CW, 34, x), tk + 1.0)
        else:
            f.show(say(X0, SY, '%d %% 2 = 0 → keep, %d * %d = %d' % (x, x, x, x * x), TX), tk + .2, hide=tk + dt - .1)
            f.path(box(cxl(k), CY, CW, 34, x * x, PT, it('.08'), PT), [(0, 0, 0), (tk + .9, cxl(o) - cxl(k), OY - CY)], tk + .6, d=.5)
            o += 1
    end = t + 5 * dt
    bar += [(end, 0)]
    code.track(f, bar)
    for j, v in enumerate([16, 36, 4]): f.show(solid(cxl(j), OY, CW, 34, v), end)
    f.show(say(X0, SY, '✓ out = [16, 36, 4] · one line, no append calls', TG, True), end + .3)
    f.h = SY + 14
    return f.render()


def fig_choose():
    sig = [('sorted list, "first position ≥ x"', 0), ('count how often each value appears', 1),
           ('group items by a key, build a graph', 2), ('BFS, take from the front', 3),
           ('k smallest / largest, Dijkstra', 4), ('filter or transform a list', 5)]
    tg = ['bisect', 'Counter', 'defaultdict', 'deque', 'heapq', 'comprehension']
    cases = [('Top K Frequent Elements', 1, 'count how often → Counter, then heapq for the top k'),
             ('Rotting Oranges — minutes until all rot', 3, 'BFS layer by layer → deque'),
             ('Group Anagrams', 2, 'group by sorted letters → defaultdict(list)')]
    return route('lck-t1-', 'CHOOSING A TOOL · SIGNAL IN THE PROBLEM → STANDARD LIBRARY',
                 'Six problem signals on the left, each joined to one standard-library tool on the right. Top K Frequent lights count how often and Counter; Rotting Oranges lights BFS and deque; Group Anagrams lights group by key and defaultdict. The chosen tools stay solid.',
                 'SIGNAL IN THE PROBLEM', 'TOOL', sig, tg, cases,
                 'all six ship with Python — nothing to install', W=760, lw=330, rw=170, rh=30, gap=8)


if __name__ == '__main__':
    figs = {'b': fig_bisect(), 'c': fig_counter(), 'd': fig_defaultdict(), 'q': fig_deque(), 'h': fig_heap(), 'p': fig_comp(), 't': fig_choose()}
    json.dump(figs, open('/tmp/dsa/leetcode-toolkit.json', 'w'))
    page = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../content/01-dsa/05-toolkit/leetcode-toolkit/index.html')
    S = lambda m, title, skey, k: sub('lc', 1, m, title, skey, figs[k])
    art = '''<article class="doc" id="art-kit" data-title="LeetCode toolkit" data-tag="Toolkit" data-blurb="Six standard-library tools that shorten solutions: bisect, Counter, defaultdict, deque, heapq, comprehensions.">
        <header class="hero">
  <p class="eyebrow">Python · toolkit</p>
  <h1>LeetCode <em>toolkit</em></h1>
  <p class="lede">Six standard-library tools that shorten solutions the most.</p>
</header>

<section id="lc-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Tools</h2></div>
  <p class="key">Each tool does one job on the data <em>in one call</em>.</p>
%s%s%s%s%s%s</section>

<section id="lc-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Choosing a tool</h2></div>
  <p class="key">Recognise <em>the signal in the problem</em> and the tool follows.</p>
  <div class="subsec" id="lc-s2-1">
    <h3 class="ssh"><b>2.1</b>Signal to tool</h3>
    <p class="skey">Follow the line from the problem's wording to the tool.</p>
%s
  </div>
</section>

%s
<footer>DSA · toolkit · the basics are in <a href="../../../02-python/03-builtin-structures/list-tuple-set/index.html">List, tuple &amp; set</a> on the Python shelf.</footer>
      </article>''' % (
        S(1, 'bisect', 'In a sorted list, find <em>where a value would go</em> by halving.', 'b'),
        S(2, 'Counter', 'Count every value <em>in one pass</em>; a missing key reads as 0.', 'c'),
        S(3, 'defaultdict', 'A missing key <em>starts with a default</em>, so grouping needs no key check.', 'd'),
        S(4, 'deque', 'Take from the front <em>without shifting</em> the rest.', 'q'),
        S(5, 'heapq', 'The smallest item is <em>always at index 0</em>; push and pop cost <span class="mth">O(<b class="fn">log</b> <var>n</var>)</span>.', 'h'),
        S(6, 'Comprehension', 'Filter and transform a list <em>in one line</em>.', 'p'),
        figs['t'], REPLAY.strip())
    splice(page, art)
    print('ok', {k: len(v) for k, v in figs.items()})
