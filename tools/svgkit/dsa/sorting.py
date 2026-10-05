"""Figures for content/01-dsa/04-algorithms/sorting. Writes /tmp/dsa/sorting.json."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from algo4 import *

figs = {}

# ---------------------------------------------------------------- 1.1 insertion sort
def insertion():
    vals = [5, 2, 4, 6, 1, 3]; n = len(vals)
    lines = ['for i in range(1, len(a)):', '    j = i',
             '    while j > 0 and a[j-1] > a[j]:', '        a[j-1], a[j] = a[j], a[j-1]',
             '        j -= 1']
    code = Code2(0, 40, lines)
    X0 = code.w + 34; CY = 96
    f = Anim('srt-m1-', 760, 0, 'Insertion sort on 5 2 4 6 1 3. Each new element i is swapped left past every bigger neighbour; '
             'the sorted prefix grows by one each round. 9 swaps, ending 1 2 3 4 5 6.', 'INSERTION SORT · GROW A SORTED PREFIX', 3.2)
    f.static(code.svg())
    A = Arr(X0, CY, vals, 46, 36, 8); A.reserve(f)
    f.show(chip(X0, 24, 'goal: ascending order'), .9)
    pi = Ptr(A, 'i', 1); pj = Ptr(A, 'j', 1, up=True)
    SY = CY + 160; ov = []; bar = []; t = 2.4; swaps = 0
    for i in range(1, n):
        bar += [(t, 0)]; pi.to(t, i)
        bar += [(t + .4, 1)]; pj.to(t + .4, i)
        f.show(st(X0, SY, 'i = %d · take a[%d] = %d' % (i, i, A.val(i)), PT, True), t, hide=t + .9)
        t += 1.0; j = i
        while True:
            if j == 0:
                bar.append((t, 2)); f.show(st(X0, SY, 'j = 0 → nothing left of it, stop', TX), t, hide=t + 1.1); t += 1.3; break
            x, y = A.val(j - 1), A.val(j)
            bar.append((t, 2))
            f.show(A.ring(j - 1, j), t, hide=t + 1.5)
            if x > y:
                f.show(st(X0, SY, 'a[%d] = %d > a[%d] = %d → swap' % (j - 1, x, j, y), TX), t, hide=t + 1.5)
                bar.append((t + .7, 3)); A.swap(t + .7, j - 1, j); swaps += 1
                bar.append((t + 1.3, 4)); pj.to(t + 1.3, j - 1); j -= 1; t += 1.8
            else:
                f.show(st(X0, SY, 'a[%d] = %d ≤ a[%d] = %d → stop' % (j - 1, x, j, y), TX), t, hide=t + 1.3); t += 1.5; break
        br = L(A.xl(0), CY + 118, A.xl(i) + A.w, CY + 118, TG, 1.6) + L(A.xl(0), CY + 113, A.xl(0), CY + 118, TG, 1.6) + \
            L(A.xl(i) + A.w, CY + 113, A.xl(i) + A.w, CY + 118, TG, 1.6)
        ov.append((br + lab(A.xl(i) + A.w + 8, CY + 122, 'sorted', TG, bold=True), t - .2, None if i == n - 1 else t + 2.4))
    end = t
    A.commit(f, .2); pi.commit(f, 2.4, hide=end); pj.commit(f, 2.8, hide=end)
    for s, a, h in ov: f.show(s, a, hide=h)
    code.run(f, bar + [(end, 0)])
    for k in range(n): f.show(A.cell(k, 'f', end + .2), end + .2 + k * .06)
    f.show(T(X0 + A.w * 3 + 8 * 2.5, CY + 80, '✓ sorted', TG, mono=True, bold=True), end + .6)
    f.show(lab(X0, SY + 6, '%d swaps · worst case n(n−1)/2 = %d for n = %d' % (swaps, n * (n - 1) // 2, n), TG, bold=True), end + .8)
    assert swaps == 9
    f.h = max(code.y + code.h(), SY + 16) + 8
    return f.render()
figs['m1'] = insertion()

# ---------------------------------------------------------------- 1.2 merge sort
def merge_sort():
    a = [5, 2, 7, 4, 8, 1, 6, 3]; n = 8
    W = 760; CW, G, GG = 40, 5, 22
    f = Anim('srt-m2-', W, 0, 'Merge sort on 5 2 7 4 8 1 6 3. Split into halves down to single cells, then merge pairs back up: '
             'each merge repeatedly takes the smaller front value. Three levels of eight cells: 24 moves, n log n.',
             'MERGE SORT · SPLIT DOWN, MERGE BACK UP', 3.2)
    def groups(level):   # level 0 = 1 group of 8 ... 3 = 8 groups of 1
        s = n >> level; return [list(range(g * s, g * s + s)) for g in range(n // s)]
    def gx(level, k):    # x of slot k at a level with that many groups
        s = n >> level; g = k // s
        width = n * CW + (n - 1) * G + (n // s - 1) * GG
        return (W - 120 - width) / 2 + 120 + k * (CW + G) + g * GG
    RH = 50; Y0 = 36
    rows = {}
    t = .3
    # split rows 0..3
    for lv in range(4):
        y = Y0 + lv * RH
        f.show(lab(0, y + 23, ['input', 'split', 'split', 'split'][lv], MU), t)
        for k in range(n): f.show(box(gx(lv, k), y, a[k], CW, 34), t + k * .04)
        t += 1.1
    cur = {(k,): a[k] for k in range(n)}
    # merge rows
    lists = [[a[k]] for k in range(n)]
    t += .3; level_y = Y0 + 4 * RH
    stat_y = Y0 + 7 * RH + 26
    picks = 0
    for out_lv, lv in ((4, 2), (5, 1), (6, 0)):
        y = Y0 + out_lv * RH; srcy = y - RH
        f.show(lab(0, y + 23, 'merge', MU), t)
        new = []
        for g in range(0, len(lists), 2):
            A_, B_ = lists[g], lists[g + 1]; base = sum(len(x) for x in lists[:g])
            merged = []; i = j = 0
            slow = out_lv == 6
            while i < len(A_) or j < len(B_):
                takeA = j >= len(B_) or (i < len(A_) and A_[i] <= B_[j])
                src = base + (i if takeA else len(A_) + j)
                v = A_[i] if takeA else B_[j]
                dst = base + len(merged)
                sx, dx_ = gx(lv + 1, src), gx(lv, dst)
                if slow:
                    ia, jb = base + i, base + len(A_) + j
                    if i < len(A_) and j < len(B_):
                        f.show(ring(gx(lv + 1, ia), srcy, CW, 34) + ring(gx(lv + 1, jb), srcy, CW, 34), t, hide=t + 1.0)
                        f.show(st(gx(0, 0), stat_y, '%d %s %d → take %d' % (A_[i], '≤' if takeA else '>', B_[j], v), TX), t, hide=t + 1.0)
                    else:
                        f.show(st(gx(0, 0), stat_y, 'one side empty → take %d' % v, TX), t, hide=t + 1.0)
                    f.path(box(sx, srcy, v, CW, 34), [(0, 0, 0), (t + .45, dx_ - sx, RH)], t + .3, d=.45)
                    f.show(box(sx, srcy, v, CW, 34, 'g'), t + .5)
                    t += 1.15
                else:
                    f.path(box(sx, srcy, v, CW, 34), [(0, 0, 0), (t + .2, dx_ - sx, RH)], t, d=.45)
                    f.show(box(sx, srcy, v, CW, 34, 'g'), t + .25)
                    t += .12
                picks += 1
                merged.append(v)
                if takeA: i += 1
                else: j += 1
            new.append(merged)
            if not slow: t += .25
        lists = new
        if out_lv < 6:
            f.show(st(gx(0, 0), stat_y, ['pairs merged: 8 moves', 'fours merged: 8 moves'][out_lv - 4], TX), t, hide=t + 1.4)
            t += 1.6
    end = t
    y6 = Y0 + 6 * RH
    for k in range(n): f.show(box(gx(0, k), y6, lists[0][k], CW, 34, 'f'), end + k * .05)
    assert lists[0] == sorted(a) and picks == 24
    f.show(T(gx(0, n - 1) + CW + 34, y6 + 22, '✓ sorted', TG, mono=True, bold=True), end + .5)
    f.show(lab(gx(0, 0), stat_y, '3 levels × 8 cells = 24 moves · n log₂ n', TG, bold=True), end + .7)
    f.h = stat_y + 12
    return f.render()
figs['m2'] = merge_sort()

# ---------------------------------------------------------------- 1.3 n^2 vs n log n
def growth():
    f = Anim('srt-m3-', 760, 400, 'For 8 items, insertion sort may compare every pair: an 8 by 8 grid, 64. Merge sort does 3 levels of 8: 24. '
             'The graph shows n squared shooting up while n log n stays low.', 'O(n²) vs O(n log n) · n = 8, THEN THE GRAPH', 3)
    S, G = 13, 3
    f.static(lab(0, 40, 'insertion · up to n × n', MU))
    for r in range(8):
        for c in range(8):
            f.show(R(c * (S + G), 50 + r * (S + G), S, S, it('.14'), TG, 2, .8), .3 + (r * 8 + c) * .02)
    f.show(st(0, 50 + 8 * (S + G) + 16, '8 × 8 = 64', TG, True), 1.7)
    X2 = 200
    f.static(lab(X2, 40, 'merge · log₂ n levels × n', MU))
    for r in range(3):
        for c in range(8):
            f.show(R(X2 + c * (S + G), 50 + r * (S + G), S, S, vt('.16'), MID, 2, .8), 2.0 + (r * 8 + c) * .03)
    f.show(st(X2, 50 + 3 * (S + G) + 16, '3 × 8 = 24', MID, True), 2.9)
    gx, gy, gw, gh = 430, 50, 290, 260
    NM, YM = 64, 1000
    px = lambda v: gx + v / NM * gw; py = lambda v: gy + gh - v / YM * gh
    t = 3.6
    f.show(axes(gx, gy, gw, gh, (16, 32, 48, 64), (250, 500, 750, 1000), 'n', 'steps', px, py), t)
    sq = [(x / 2, (x / 2) ** 2) for x in range(0, 64) if (x / 2) ** 2 <= YM]
    sq.append((math.sqrt(YM), YM))
    f.show(poly([(px(a), py(b)) for a, b in sq], GH, 2.2) + lab(px(31.6) + 6, py(960), 'n²', MU, bold=True), t + .8, d=.8)
    nl = [(x, x * math.log2(x)) for x in [1 + i * .5 for i in range(127)]]
    f.show(poly([(px(a), py(b)) for a, b in nl], TG, 2.6) + lab(px(64), py(384) - 10, 'n log₂ n', TG, 'end', True), t + 1.9, d=.8)
    for k, v in enumerate((8, 16, 32, 64)):
        f.show(dot(px(v), py(v * math.log2(v)), MID), t + 2.8 + k * .25)
    for k, v in enumerate((8, 16, 31.6)):
        f.show(dot(px(v), py(min(YM, v * v)), GH), t + 2.8 + k * .25)
    f.show(st(px(32) + 6, py(160) + 18, '32 → 160', MID, True) + st(px(16) + 6, py(256) - 4, '16 → 256', MU, True), t + 4.0)
    f.show(lab(gx + gw + 10, gy + gh + 40, 'n = 10⁶: 10¹² vs 2·10⁷ steps', TG, 'end', True), t + 4.5)
    return f.render()
figs['m3'] = growth()

# ---------------------------------------------------------------- 1.4 stable sort
def stable():
    items = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd'), (3, 'e')]
    f = Anim('srt-m4-', 760, 210, 'Cards 2a 1b 2c 1d 3e sorted by number. A stable sort keeps b before d and a before c, as in the input.',
             'STABLE SORT · EQUAL KEYS KEEP THEIR INPUT ORDER', 3)
    X0 = 150; CY = 60
    A = Arr(X0, CY, ['%d%s' % (k, s) for k, s in items], 58, 40, 12); A.reserve(f)
    f.static(lab(0, CY + 25, 'sort by number', MU))
    f.show(chip(X0, 24, 'key = the number'), .9)
    order = sorted(range(5), key=lambda e: items[e][0])
    t = 2.2
    f.show(st(X0, CY + 108, 'sorted(cards, key=number)', PT, True), t, hide=t + 1.8)
    A.place(t + .4, order)
    t += 2.2
    for (e1, e2), msg in (((1, 3), 'two 1s: b came before d in the input → still b, d'),
                          ((0, 2), 'two 2s: a came before c → still a, c')):
        k1, k2 = A.slot[e1], A.slot[e2]
        f.show(A.ring(k1, k2), t, hide=t + 1.9)
        f.show(st(X0, CY + 108, msg, TX), t, hide=t + 1.9)
        t += 2.2
    A.commit(f, .2)
    for k in range(5): f.show(A.cell(k, 'f', t), t + k * .06)
    f.show(T(A.cx(2), CY + 80, '✓ stable', TG, mono=True, bold=True), t + .4)
    f.show(lab(X0, CY + 112, "Python's sort (Timsort) is stable → sort by name, then by score, works", TG, bold=True), t + .6)
    return f.render()
figs['m4'] = stable()

# ---------------------------------------------------------------- 2.1 sort then scan (h-index)
def hindex():
    c = [3, 0, 6, 1, 5]
    lines = ['c.sort(reverse=True)', 'h = 0', 'for i, x in enumerate(c):', '    if x >= i + 1: h = i + 1', '    else: break']
    code = Code2(0, 40, lines)
    X0 = code.w + 40; CY = 96
    f = Anim('srt-q1-', 760, 0, 'H-index of citations 3 0 6 1 5. Sort descending to 6 5 3 1 0, then scan: 6 ≥ 1, 5 ≥ 2, 3 ≥ 3 pass, 1 ≥ 4 fails. h = 3.',
             'SORT, THEN ONE PASS · H-INDEX OF 3 0 6 1 5', 3.2)
    f.static(code.svg())
    A = Arr(X0, CY, c, 46, 36, 8); A.reserve(f)
    f.show(chip(X0, 24, 'goal: largest h with h papers ≥ h'), .9)
    t = 2.2; bar = [(t, 0)]
    f.show(st(X0, CY + 128, 'sort descending', PT, True), t, hide=t + 1.6)
    order = sorted(range(5), key=lambda e: -c[e]); A.place(t + .3, order)
    t += 2.0; bar.append((t, 1)); t += .5
    p = Ptr(A, 'i', 0); ov = []; h = 0
    for i in range(5):
        x = A.val(i); bar.append((t, 2)); p.to(t, i)
        f.show(A.ring(i), t + .3, hide=t + 1.7)
        bar.append((t + .5, 3))
        if x >= i + 1:
            h = i + 1
            f.show(st(X0, CY + 128, 'c[%d] = %d ≥ %d → h = %d' % (i, x, i + 1, h), TX), t + .3, hide=t + 1.7)
            ov.append((A.cell(i, 'b', 0), t + 1.0)); t += 2.0
        else:
            f.show(st(X0, CY + 128, 'c[%d] = %d < %d → stop' % (i, x, i + 1), TX), t + .3, hide=t + 1.7)
            bar.append((t + 1.0, 4))
            for k in range(i, 5): ov.append((A.cell(k, 'g', 0), t + 1.2))
            t += 2.0; break
    end = t
    A.commit(f, .2); p.commit(f, 4.7, hide=end)
    for s, a_ in ov: f.show(s, a_)
    code.run(f, bar)
    for k in range(h): f.show(A.cell(k, 'f', end), end + k * .06)
    f.show(T(A.cx(1), CY + 80, '✓ found', TG, mono=True, bold=True), end + .4)
    f.show(lab(X0, CY + 128, 'h = 3 · sort O(n log n) + one pass O(n)', TG, bold=True), end + .6)
    assert h == 3
    f.h = max(code.y + code.h(), CY + 140) + 10
    return f.render()
figs['q1'] = hindex()

# ---------------------------------------------------------------- 2.2 custom order (largest number)
def largest():
    w = ['3', '30', '34', '5', '9']
    f = Anim('srt-q2-', 760, 230, 'Largest number from 3 30 34 5 9. Order two strings by which concatenation is bigger: 3 before 30 because 330 > 303, '
             '9 before 5 because 95 > 59. Sorted: 9 5 34 3 30, giving 9534330.', 'CUSTOM ORDER · a BEFORE b IF a+b > b+a', 3)
    X0 = 130; CY = 60
    A = Arr(X0, CY, w, 56, 36, 12); A.reserve(f)
    f.static(lab(0, CY + 23, 'numbers', MU))
    f.show(chip(X0, 24, 'goal: biggest joined number'), .9)
    t = 2.2
    for a_, b_ in (('3', '30'), ('9', '5')):
        k1, k2 = A.slot[w.index(a_)], A.slot[w.index(b_)]
        f.show(A.ring(min(k1, k2), max(k1, k2)) if abs(k1 - k2) == 1 else A.ring(k1) + A.ring(k2), t, hide=t + 2.2)
        f.show(st(X0, CY + 90, '"%s"+"%s" = %s  vs  "%s"+"%s" = %s' % (a_, b_, a_ + b_, b_, a_, b_ + a_), PT, True), t, hide=t + 2.2)
        f.show(st(X0, CY + 112, '%s > %s → %s goes first' % (a_ + b_, b_ + a_, a_), TX), t + .7, hide=t + 2.2)
        t += 2.6
    import functools
    order = sorted(range(5), key=functools.cmp_to_key(lambda x, y: -1 if w[x] + w[y] > w[y] + w[x] else 1))
    f.show(st(X0, CY + 90, 'sort every pair by this rule', PT, True), t, hide=t + 1.6)
    A.place(t + .3, order); t += 2.0
    A.commit(f, .2)
    res = ''.join(w[e] for e in order); assert res == '9534330'
    for k in range(5): f.show(A.cell(k, 'f', t), t + k * .06)
    f.show(T(A.cx(2), CY + 74, '✓ found', TG, mono=True, bold=True), t + .4)
    f.show(lab(X0, CY + 112, 'join → 9534330 · the rule replaces "<" in the sort', TG, bold=True), t + .6)
    return f.render()
figs['q2'] = largest()

# ---------------------------------------------------------------- 2.3 three-way partition (sort colors)
def colors():
    a = [2, 0, 2, 1, 1, 0]
    lines = ['l, i, r = 0, 0, len(a) - 1', 'while i <= r:', '    if a[i] == 0:', '        a[l], a[i] = a[i], a[l]; l += 1; i += 1',
             '    elif a[i] == 2:', '        a[i], a[r] = a[r], a[i]; r -= 1', '    else: i += 1']
    code = Code2(0, 40, lines)
    X0 = code.w + 30; CY = 96
    f = Anim('srt-q3-', 760, 0, 'Sort colors 2 0 2 1 1 0 in one pass with three pointers: zeros are swapped to l, twos to r, ones stay. Ends 0 0 1 1 2 2.',
             'THREE-WAY PARTITION · 0s LEFT, 2s RIGHT, ONE PASS', 3.2)
    f.static(code.svg())
    A = Arr(X0, CY, a, 42, 36, 6); A.reserve(f)
    f.show(chip(X0, 24, 'goal: 0s | 1s | 2s'), .9)
    pl = Ptr(A, 'l', 0, up=True); pi = Ptr(A, 'i', 0); pr = Ptr(A, 'r', 5, up=True)
    l, i, r = 0, 0, 5; t = 2.2; bar = [(t, 0)]; SY = CY + 130; ov = []
    f.show(st(X0, SY, 'l = 0 · i = 0 · r = 5', PT, True), t, hide=t + 1.2); t += 1.4
    while i <= r:
        bar.append((t, 1)); v = A.val(i)
        f.show(A.ring(i), t + .2, hide=t + 1.9)
        if v == 0:
            bar.append((t + .4, 2)); bar.append((t + .8, 3))
            f.show(st(X0, SY, 'a[%d] = 0 → swap with l = %d · l, i move right' % (i, l), TX), t + .2, hide=t + 1.9)
            A.swap(t + .8, l, i); ov.append((l, t + 1.4)); l += 1; i += 1; pl.to(t + 1.4, l); pi.to(t + 1.4, i)
        elif v == 2:
            bar.append((t + .4, 2)); bar.append((t + .7, 4)); bar.append((t + 1.0, 5))
            f.show(st(X0, SY, 'a[%d] = 2 → swap with r = %d · r moves left' % (i, r), TX), t + .2, hide=t + 1.9)
            A.swap(t + 1.0, i, r); ov.append((r, t + 1.6)); r -= 1; pr.to(t + 1.6, r)
        else:
            bar.append((t + .4, 2)); bar.append((t + .7, 4)); bar.append((t + 1.0, 6))
            f.show(st(X0, SY, 'a[%d] = 1 → leave it · i moves right' % i, TX), t + .2, hide=t + 1.9)
            i += 1; pi.to(t + 1.4, i)
        t += 2.2
    bar.append((t, 1)); end = t + .4
    A.commit(f, .2); pl.commit(f, 2.2, hide=end); pi.commit(f, 2.2, hide=end); pr.commit(f, 2.2, hide=end)
    for k, ts in ov: f.show(A.cell(k, 'g', 0, v=A.val(k)), ts)
    code.run(f, bar)
    assert [A.val(k) for k in range(6)] == [0, 0, 1, 1, 2, 2]
    for k in range(6): f.show(A.cell(k, 'f', end), end + k * .06)
    f.show(T(A.cx(2) + 24, CY + 80, '✓ sorted', TG, mono=True, bold=True), end + .4)
    f.show(lab(X0, SY, 'one pass, O(n) · no comparison sort needed', TG, bold=True), end + .6)
    f.h = max(code.y + code.h(), SY + 12) + 8
    return f.render()
figs['q3'] = colors()

# ---------------------------------------------------------------- 2.4 partition around a pivot (quickselect)
def quickselect():
    a = [3, 2, 1, 5, 6, 4]; k = 2; n = 6; want = n - k
    f = Anim('srt-q4-', 760, 260, 'Second largest of 3 2 1 5 6 4 = the value at index 4 once sorted. Pivot 4: smaller values move left, '
             'larger right, 4 lands at index 3, too far left, keep the right part. Pivot 6 lands at 5, too far right. Index 4 holds 5.',
             'PARTITION AROUND A PIVOT · 2nd LARGEST = INDEX n − k = 4', 3.2)
    X0 = 140; CY = 80
    A = Arr(X0, CY, a, 48, 36, 10); A.reserve(f)
    f.static(lab(0, CY + 23, 'array', MU))
    f.show(chip(X0, 24, 'goal: value at sorted index 4'), .9)
    pl = Ptr(A, 'l', 0); pr = Ptr(A, 'r', 5, ln=30)
    t = 2.4; l, r = 0, 5; SY = CY + 130
    f.show(st(X0, SY, 'l = 0 · r = 5', PT, True), t, hide=t + 1.1); t += 1.4
    while True:
        ids = [A.at(q) for q in range(l, r + 1)]; pv = A.vals[ids[-1]]
        f.show(A.ring(r), t, hide=t + 2.4)
        f.show(st(X0, SY, 'pivot = a[r] = %d · smaller left, larger right' % pv, MID, True), t, hide=t + 2.4)
        sm = [e for e in ids[:-1] if A.vals[e] < pv]; bg = [e for e in ids[:-1] if A.vals[e] > pv]
        order = [A.at(q) for q in range(l)] + sm + [ids[-1]] + bg + [A.at(q) for q in range(r + 1, n)]
        A.place(t + .9, order); p = l + len(sm); t += 2.6
        if p == want:
            f.show(st(X0, SY, 'pivot landed at %d = 4 → done' % p, TX), t, hide=t + 1.2); t += 1.4; break
        go = 'right' if p < want else 'left'
        f.show(st(X0, SY, 'pivot landed at %d %s 4 → keep the %s part' % (p, '<' if p < want else '>', go), TX), t, hide=t + 2.0)
        drop = range(l, p + 1) if p < want else range(p, r + 1)
        for q in drop: f.show(A.cell(q, 'g', 0), t + .6)
        if p < want: l = p + 1; pl.to(t + 1.0, l)
        else: r = p - 1; pr.to(t + 1.0, r)
        t += 2.3
        if l == r:
            f.show(st(X0, SY, 'l = r = %d → one cell left, done' % l, TX), t, hide=t + 1.2); t += 1.4; break
    end = t
    A.commit(f, .2); pl.commit(f, 2.4, hide=end); pr.commit(f, 2.4, hide=end)
    assert A.val(want) == 5
    f.show(A.cell(want, 'f', end), end)
    f.show(T(A.cx(want), CY + 80, '✓ found', TG, mono=True, bold=True), end + .3)
    f.show(lab(X0, SY, '2nd largest = 5 · each partition keeps one side → O(n) on average', TG, bold=True), end + .5)
    f.h = SY + 14
    return f.render()
figs['q4'] = quickselect()

os.makedirs('/tmp/dsa', exist_ok=True)
json.dump(pad(figs), open('/tmp/dsa/sorting.json', 'w'))
print({k: len(v) for k, v in figs.items()})
