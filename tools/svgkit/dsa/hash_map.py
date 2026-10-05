"""Figures for content/01-dsa/03-data-structures/hash-map. Output: /tmp/dsa/hash-map.json
Hash values are a toy hash (sum of letter positions) so every number is reproducible."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seqkit import *

def h(k): return sum(ord(c) - 96 for c in k)          # toy hash: a=1 … z=26
assert h('cat') == 24 and h('dog') == 26 and h('fox') == 45 and h('act') == 24 and h('ant') == 35

class Table:
    """vertical column of buckets; entries as Obj boxes to the right of each bucket (chaining)."""
    def __init__(s, f, x, y, n, t0=.2, bh=30, gap=6, label=True):
        s.f, s.x, s.y, s.n, s.bh, s.gap = f, x, y, n, bh, gap
        s.chain = {i: [] for i in range(n)}
        for i in range(n):
            f.show(R(x, s.by(i), 40, bh, 'var(--sunk)', RULE_HI, 5, 1) + T(x + 20, s.by(i) + bh / 2 + 4, str(i), FA, mono=True), t0 + i * .05)
    def by(s, i): return s.y + i * (s.bh + s.gap)
    def ex(s, i, k): return s.x + 52 + k * 96
    def put(s, i, obj, t):
        k = len(s.chain[i]); s.chain[i].append(obj)
        obj.move(t, s.ex(i, k), s.by(i) + 3)
        if k: s.f.show(arrow(s.ex(i, k) - 12, s.by(i) + s.bh / 2, s.ex(i, k) - 1, s.by(i) + s.bh / 2, MU, 1.2, None, 5), t + .5)
        return k
    def ring(s, i, t, hide): s.f.show(ring(s.x, s.by(i), 40, s.bh), t, hide)

def entry(f, t, x, y, txt, tone='u'): return Box(f, t, x, y, txt, w=84, h=24, tone=tone)

figs = {}
CHIPX = 0

# ---------------------------------------------------------------- m1 key -> hash -> slot
L1 = ['i = hash(key) % len(slots)', 'slots[i] = (key, value)']
f = Fig('hm-m1-', 'A hash map stores cat, dog and fox in 8 slots. Each key is turned into a number by a hash function, the number modulo 8 picks the slot, and the key-value pair is placed straight into that slot. No searching.',
        'KEY → NUMBER → SLOT · THE POSITION IS COMPUTED', L1, W=780)
X0 = f.X0 + 10
TB = Table(f, X0 + 200, 40, 8)
keys = [('cat', 3), ('dog', 7), ('fox', 2)]
t = 1.2; SY = 40 + 8 * 36 + 20
for k, (key, val) in enumerate(keys):
    y0 = 60 + k * 70
    e = entry(f, t, X0, y0, '%s: %d' % (key, val))
    f.line(t + .3, 0)
    hv = h(key); i = hv % 8
    status(f, X0, SY, 'hash("%s") = %d · %d %% 8 = %d' % (key, hv, hv, i), t + .5, hide=t + 2.4)
    TB.ring(i, t + 1.2, t + 2.4)
    f.line(t + 1.6, 1)
    TB.put(i, e, t + 1.7)
    e.tone(t + 2.6, 'f')
    t += 2.8
finish(f, X0, SY, '3 keys placed · each one by a computation, no scan', t)
figs['m1'] = f.render(SY + 12)

# ---------------------------------------------------------------- p1 get/set O(1) + graph
L2 = ['i = hash(key) % len(slots)', 'return slots[i]']
f = Fig('hm-p1-', 'get dog in a table of 8 slots: hash 26, 26 mod 8 = 2, look at slot 2, found in one step. Graph: steps against the number of keys n: a list scan climbs with n, the hash map stays flat at one step.',
        'GET AND SET · ONE COMPUTATION, ONE LOOK · O(1) ON AVERAGE', L2, W=880)
X0 = f.X0 + 10
TB = Table(f, X0 + 40, 40, 8)
for key, val in [('cat', 3), ('fox', 2), ('dog', 7), ('ant', 1)]:
    i = h(key) % 8
    e = entry(f, .4, TB.ex(i, len(TB.chain[i])), TB.by(i) + 3, '%s: %d' % (key, val)); TB.chain[i].append(e)
goal_on(f, TB.ex(2, 0), TB.by(2) + 3, 'get("dog")', 1.0, X0 + 250, 40, w=84, h=24, ring_hide=4.2)
f.line(2.6, 0)
status(f, X0 + 250, 90, 'hash("dog") = 26 · 26 % 8 = 2', 2.6, hide=4.4)
TB.ring(2, 3.2, 4.4)
f.line(3.6, 1)
TB.chain[2][0].tone(4.2, 'f')
f.show(T(TB.ex(2, 0) + 100, TB.by(2) + 20, '✓ found', TG, 'start', mono=True, bold=True), 4.4)
finish(f, X0 + 250, 90, '1 look · same for 8 keys or 8 million', 4.6)
gx, gy, gw, gh = X0 + 300, 150, 170, 130
graph(f, gx, gy, gw, gh, 10, 10, [
    (lambda v: v, 'list scan: n', GH, 2, 0),
    (lambda v: 1, 'hash map: 1', TG, 2.6, 0)], 5.4, xt=(2, 4, 6, 8, 10), yt=(5, 10), xl='keys', yl='steps')
figs['p1'] = f.render(40 + 8 * 36 + 10)

# ---------------------------------------------------------------- p2 collisions
L3 = ['i = hash(key) % len(slots)', 'for k, v in slots[i]:', '    if k == key: return v']
f = Fig('hm-p2-', 'cat and act have the same letters, so the toy hash gives 24 for both: same slot 0. They are chained in one bucket. Looking up act walks the bucket: cat is not it, act is. A collision costs one extra comparison; a bucket holding every key would cost n.',
        'COLLISIONS · TWO KEYS, ONE SLOT · THE BUCKET IS SCANNED', L3, W=760)
X0 = f.X0 + 10
TB = Table(f, X0 + 40, 40, 4)
for k, (key, val) in enumerate([('cat', 3), ('act', 5)]):
    t = 1.0 + k * 2.4; y0 = 40 + 4 * 36 + 20
    e = entry(f, t, X0 + 40, y0, '%s: %d' % (key, val))
    hv = h(key)
    status(f, X0 + 150, y0 + 16, 'hash %d · %d %% 4 = %d' % (hv, hv, hv % 4), t + .3, hide=t + 2.0)
    TB.ring(hv % 4, t + .8, t + 1.8)
    TB.put(hv % 4, e, t + 1.2)
f.show(T(TB.ex(0, 2) - 6, TB.by(0) + 20, '← collision: same slot', MID, 'start', mono=True), 5.4, hide=7.0)
SY = 40 + 4 * 36 + 40
goal_on(f, TB.ex(0, 1), TB.by(0) + 3, 'get("act")', 7.2, TB.ex(0, 2) + 10, TB.by(0) + 3, w=84, h=24, ring_hide=10.6)
t = 8.6
f.line(t, 0); TB.ring(0, t, t + .8)
for k in range(2):
    f.line(t + .9 + k * 1.2, 1); f.line(t + 1.3 + k * 1.2, 2)
    f.show(ring(TB.ex(0, k), TB.by(0) + 3, 84, 24), t + 1.3 + k * 1.2, hide=t + 2.1 + k * 1.2)
    status(f, X0 + 40, SY + 6, ['"cat" ≠ "act" → next', '"act" == "act"'][k], t + 1.3 + k * 1.2, hide=t + 2.1 + k * 1.2 if k == 0 else t + 3.0)
TB.chain[0][1].tone(t + 3.0, 'f')
finish(f, X0 + 40, SY + 6, '2 comparisons · cost = bucket length · O(n) if all keys collide', t + 3.2)
figs['p2'] = f.render(SY + 18)

# ---------------------------------------------------------------- p3 resize
f = Fig('hm-p3-', 'A table of 4 slots holds three keys: load 3 of 4 is above the limit. A new table of 8 slots is allocated and every key is hashed again, so each key lands in a slot of the bigger table. Rehashing touches all n keys, but it happens rarely, so insert stays O(1) on average.',
        'RESIZE · TOO FULL → DOUBLE AND REHASH EVERY KEY', W=760)
X0 = 0
A = Table(f, X0 + 20, 50, 4)
items = [('cat', 3), ('dog', 7), ('fox', 1)]
for key, val in items:
    i = h(key) % 4
    e = entry(f, .4, A.ex(i, len(A.chain[i])), A.by(i) + 3, '%s: %d' % (key, val)); A.chain[i].append(e)
status(f, X0 + 20, 50 + 8 * 36 + 24, 'load = 3 / 4 = 0.75 > 2/3 → too full', 1.6, hide=3.4)
f.show(T(X0 + 20, 40, '4 slots', FA, 'start', cls='sv-s'), .2)
B = Table(f, X0 + 380, 50, 8, t0=3.0)
f.show(T(X0 + 380, 40, '8 slots', FA, 'start', cls='sv-s'), 3.0)
t = 3.8
for i_, (key, val) in enumerate(items):
    i4 = h(key) % 4; i8 = h(key) % 8
    o = [c for c in sum(A.chain.values(), []) if c is not None][0] if False else None
    src = A.chain[i4][0]
    f.show(ring(src.ev[0][3] if False else A.ex(i4, 0), A.by(i4) + 3, 84, 24), t, hide=t + 1.4)
    status(f, X0 + 20, 50 + 8 * 36 + 24, 'hash("%s") = %d · %d %% 8 = %d' % (key, h(key), h(key), i8), t, hide=t + 1.6)
    src.move(t + .4, B.ex(i8, 0), B.by(i8) + 3)
    t += 1.8
for c in [A.chain[h(k) % 4][0] for k, _ in items]: c.tone(t, 'f')
finish(f, X0 + 20, 50 + 8 * 36 + 24, '3 keys rehashed · n work, but only after n inserts → O(1) average', t + .2)
f.show(R(X0 + 14, 44, 160, 4 * 36 + 6, 'var(--sunk)', 'var(--rule)', 8, 1) + T(X0 + 94, 44 + 2 * 36 + 6, 'old table freed', GH, cls='sv-s'), t + .2)
figs['p3'] = f.render(50 + 8 * 36 + 36)

# ---------------------------------------------------------------- q1 complement lookup
L4 = ['seen = {}', 'for i, x in enumerate(a):', '    if t - x in seen:', '        return seen[t - x], i', '    seen[x] = i']
f = Fig('hm-q1-', 'Two Sum with a = 2 7 11 15 and target 9. i walks the array; for each x the map is asked for 9 − x. At 2 the map is empty, so 2 is recorded at index 0. At 7 the map has 2: answer indexes 0 and 1.',
        'COMPLEMENT LOOKUP · TWO SUM, target = 9', L4, W=760)
X0 = f.X0 + 10; Y = 76
a = [2, 7, 11, 15]
row = Row(f, X0, Y, a)
goal_corner(f, X0, 'target = 9', 1.0)
f.line(1.4, 0)
MX, MY = X0, Y + 122
f.static(T(MX, MY - 8, 'seen', FA, 'start', cls='sv-s'))
ip = Ptr(f, 'i', 2.0, row.cx(0), Y + CH + 22)
t = 2.4; seen = {}; SY = MY + 60
for i, x in enumerate(a):
    f.line(t, 1)
    if i: ip.move(t, row.cx(i), Y + CH + 22)
    f.line(t + .4, 2)
    row.ring(i, t + .4, t + 2.2)
    need = 9 - x
    if need in seen:
        status(f, X0, SY, '9 − %d = %d → in seen at index %d' % (x, need, seen[need]), t + .4)
        f.line(t + 1.2, 3)
        mb[need].tone(t + 1.2, 'v')
        row.c[seen[need]].tone(t + 1.8, 'f'); row.c[i].tone(t + 1.8, 'f')
        ip.die(t + 1.8)
        finish(f, X0, SY + 22, 'answer [%d, %d] · one pass · O(n) time, O(n) memory' % (seen[need], i), t + 2.0)
        break
    status(f, X0, SY, '9 − %d = %d → not seen yet' % (x, need), t + .4, hide=t + 2.2)
    f.line(t + 1.2, 4)
    seen[x] = i
    if i == 0: mb = {}
    mb[x] = Box(f, t + 1.4, MX + len(mb) * 76, MY, '%d: %d' % (x, i), w=64)
    t += 2.4
figs['q1'] = f.render(SY + 34)

# ---------------------------------------------------------------- q2 counting
L5 = ['count = {}', 'for c in s:', '    count[c] = count.get(c, 0) + 1']
f = Fig('hm-q2-', 'Count the letters of anagram: i walks the string and each letter bumps its own counter: a reaches 3, n 1, g 1, r 1, m 1. Comparing two such counters decides whether two words are anagrams.',
        'COUNTING · ONE COUNTER PER DISTINCT KEY', L5, W=760)
X0 = f.X0 + 10; Y = 70
s = 'anagram'
row = Row(f, X0, Y, list(s), w=36, pitch=42)
f.line(1.0, 0)
MY = Y + 110
f.static(T(X0, MY - 8, 'count', FA, 'start', cls='sv-s'))
ip = Ptr(f, 'i', 1.6, row.cx(0), Y + CH + 22)
t = 2.0; cnt = {}; boxes = {}; order = []
for i, c in enumerate(s):
    f.line(t, 1)
    if i: ip.move(t, row.cx(i), Y + CH + 22)
    f.line(t + .4, 2)
    row.ring(i, t + .4, t + 1.4)
    cnt[c] = cnt.get(c, 0) + 1
    if c not in order: order.append(c)
    k = order.index(c)
    if c in boxes: boxes[c].die(t + .8)
    boxes[c] = Box(f, t + .8, X0 + k * 64, MY, '%s: %d' % (c, cnt[c]), w=54, tone='v')
    boxes[c].tone(t + 1.4, 'u')
    row.c[i].tone(t + 1.0, 'g')
    t += 1.6
ip.die(t)
for b in boxes.values(): b.tone(t, 'f')
finish(f, X0, MY + 50, 'a: 3 · n: 1 · g: 1 · r: 1 · m: 1 · same counts ⇔ anagrams', t + .2)
figs['q2'] = f.render(MY + 62)

# ---------------------------------------------------------------- q3 group by a key
L6 = ['groups = {}', 'for w in words:', '    key = "".join(sorted(w))', '    groups.setdefault(key, []).append(w)']
f = Fig('hm-q3-', 'Group anagrams: eat, tea, tan, ate, nat. Each word is turned into a key by sorting its letters: aet or ant. Words with the same key slide into the same group: eat tea ate, and tan nat.',
        'GROUP BY A KEY · SORTED LETTERS AS THE KEY', L6, W=800, cw=330)
X0 = f.X0 + 10; Y = 50
words = ['eat', 'tea', 'tan', 'ate', 'nat']
W = [Box(f, .2 + k * .1, X0 + k * 76, Y, w_, w=60) for k, w_ in enumerate(words)]
f.line(1.0, 0)
GY = Y + 110
groups = {}; t = 1.8
for k, w_ in enumerate(words):
    f.line(t, 1); f.line(t + .3, 2)
    key = ''.join(sorted(w_))
    W[k].tone(t + .3, 'v')
    f.show(T(X0 + k * 76 + 30, Y + 46, key, MID, 'middle', mono=True, bold=True), t + .5, hide=t + 1.2)
    f.line(t + 1.0, 3)
    if key not in groups:
        groups[key] = []
        gi = list(groups).index(key)
        f.show(R(X0 - 6, GY + gi * 44 - 6, 260, 36, 'none', RULE_HI, 8, 1, '4 3') + T(X0 + 262, GY + gi * 44 + 16, 'key ' + key, MU, 'start', mono=True), t + 1.0)
    gi = list(groups).index(key)
    W[k].move(t + 1.2, X0 + len(groups[key]) * 66, GY + gi * 44); W[k].tone(t + 1.8, 'u')
    groups[key].append(w_)
    t += 2.2
for b in W: b.tone(t, 'f')
finish(f, X0, GY + 2 * 44 + 16, '2 groups · one pass · O(n · k log k) for k-letter words', t + .2)
figs['q3'] = f.render(GY + 2 * 44 + 28)

# ---------------------------------------------------------------- q4 longest run with a set
L7 = ['s = set(a)', 'for x in s:', '    if x - 1 not in s:          # start of a run', '        n = 1', '        while x + n in s: n += 1']
f = Fig('hm-q4-', 'Longest consecutive run in 100 4 200 1 3 2. The numbers go into a set. Only a number whose x − 1 is missing starts a run: 100, 200 and 1. From 1 the set answers 2, 3, 4 one by one: run of length 4.',
        'SET MEMBERSHIP · START ONLY WHERE x − 1 IS MISSING', L7, W=800, cw=330)
X0 = f.X0 + 10; Y = 60
a = [100, 4, 200, 1, 3, 2]
row = Row(f, X0, Y, a, w=46, pitch=54)
f.line(1.0, 0)
f.show(T(X0, Y + CH + 40, 'all in a set: "is y in s?" costs O(1)', MU, 'start'), 1.0, hide=2.4)
t = 2.4; SY = Y + 150; best = 0; done = set()
for i, x in enumerate(a):
    f.line(t, 1); f.line(t + .3, 2)
    row.ring(i, t + .3, t + 1.4)
    if x - 1 in a:
        status(f, X0, SY, '%d − 1 = %d is in s → not a start, skip' % (x, x - 1), t + .3, hide=t + 1.4)
        if x not in done: row.c[i].tone(t + 1.0, 'g')
        t += 1.6; continue
    status(f, X0, SY, '%d − 1 missing → start a run' % x, t + .3, hide=t + 1.6)
    f.line(t + 1.0, 3)
    n = 1; tt = t + 1.4
    while x + n in a:
        f.line(tt, 4)
        j = a.index(x + n)
        row.ring(j, tt, tt + .8)
        status(f, X0, SY + 22, '%d in s ✓ → length %d' % (x + n, n + 1), tt, hide=tt + .9)
        n += 1; tt += 1.0
    if n > 1:
        for v in range(x, x + n):
            j = a.index(v)
            row.c[j].tone(tt, 'f')
            done.add(v)
    else:
        row.c[i].tone(tt - .2, 'g')
    best = max(best, n)
    t = tt + .4
finish(f, X0, SY, 'longest run 1 2 3 4 = 4 · each number visited ≤ 2 times · O(n)', t)
figs['q4'] = f.render(SY + 12)

# ---------------------------------------------------------------- q5 prefix sum counts
L8 = ['seen = {0: 1}; s = ans = 0', 'for x in a:', '    s += x', '    ans += seen.get(s - k, 0)', '    seen[s] = seen.get(s, 0) + 1']
f = Fig('hm-q5-', 'Count subarrays of 1 2 1 2 1 with sum k = 3. Keep a running sum s and a map of how often each running sum has appeared. At each step, s − 3 already seen means a subarray ending here sums to 3. Four subarrays in total.',
        'RUNNING SUM + COUNTS · SUBARRAYS WITH SUM k = 3', L8, W=820, cw=330)
X0 = f.X0 + 10; Y = 66
a = [1, 2, 1, 2, 1]
row = Row(f, X0, Y, a)
goal_corner(f, X0, 'k = 3', .8)
MY = Y + 106
f.static(T(X0, MY - 8, 'seen (sum: times)', FA, 'start', cls='sv-s'))
f.line(1.2, 0)
seen = {0: 1}; boxes = {0: Box(f, 1.4, X0, MY, '0: 1', w=56)}; order = [0]
ip = Ptr(f, 'i', 1.8, row.cx(0), Y + CH + 22)
s = ans = 0; t = 2.2; SY = MY + 56
for i, x in enumerate(a):
    f.line(t, 1)
    if i: ip.move(t, row.cx(i), Y + CH + 22)
    f.line(t + .3, 2); s += x
    row.ring(i, t + .3, t + 2.4)
    f.line(t + .9, 3)
    got = seen.get(s - 3, 0)
    if got: boxes[s - 3].tone(t + .9, 'v'); boxes[s - 3].tone(t + 2.2, 'u')
    ans += got
    status(f, X0, SY, 's = %d · s − 3 = %d seen %d× → ans = %d' % (s, s - 3, got, ans), t + .9, hide=t + 2.4)
    f.line(t + 1.6, 4)
    seen[s] = seen.get(s, 0) + 1
    if s not in order: order.append(s)
    if s in boxes: boxes[s].die(t + 1.7)
    boxes[s] = Box(f, t + 1.7, X0 + order.index(s) * 66, MY, '%d: %d' % (s, seen[s]), w=56)
    t += 2.6
ip.die(t)
f.show(T(X0 + 5 * P + 10, Y + 23, 'ans = %d' % ans, TG, 'start', mono=True, bold=True), t)
finish(f, X0, SY, '4 subarrays sum to 3 · one pass · O(n)', t + .2)
figs['q5'] = f.render(SY + 12)

dump('hash-map', figs)
