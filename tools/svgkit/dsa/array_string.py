"""Figures for content/01-dsa/03-data-structures/array-string. Output: /tmp/dsa/array-string.json"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seqkit import *

figs = {}

def lift_swap(row, i, j, t, lift=26):
    """swap cells i and j without them passing through each other: i over the top, j under."""
    a, b = row.c[i], row.c[j]
    a.move(t, row.x(i), row.y - lift); a.move(t + .5, row.x(j), row.y - lift); a.move(t + 1.0, row.x(j), row.y)
    b.move(t, row.x(j), row.y + lift); b.move(t + .5, row.x(i), row.y + lift); b.move(t + 1.0, row.x(i), row.y)
    row.c[i], row.c[j] = b, a; row.v[i], row.v[j] = row.v[j], row.v[i]

# ---------------------------------------------------------------- m1 cells side by side
f = Fig('as-m1-', 'Eight cells in a row, each 8 bytes, starting at address 1000. To read a[5] the machine computes 1000 + 5 x 8 = 1040 and jumps straight there: one step, whatever the length.',
        'CELLS SIDE BY SIDE · ONE MULTIPLICATION FINDS ANY CELL', W=640)
vals = [17, 4, 9, 23, 8, 15, 42, 6]
X0, Y = 70, 104
f.static(T(X0 - 12, Y - 18, 'address', FA, 'end', cls='sv-s'))
f.static(T(X0 - 12, Y + 23, 'value', FA, 'end', cls='sv-s'))
f.static(T(X0 - 12, Y + 52, 'index', FA, 'end', cls='sv-s'))
P2 = 64
row = Row(f, X0, Y, vals, w=56, pitch=P2)
for i in range(8): f.show(T(row.cx(i), Y - 18, str(1000 + 8 * i), FA, cls='sv-s', mono=True), .2 + i * .06)
goal_on(f, row.x(5), Y, 'a[5]', 1.2, 0, 22, w=56)
base = Ptr(f, 'a', 2.8, row.cx(0), Y + CH + 22)
status(f, 0, Y + 108, 'address = 1000 + 5 × 8 = 1040', 3.6, hide=7.6, c=MID)
# a violet jump arc from cell 0 to cell 5
arc = '<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="1.8" stroke-dasharray="5 4"/>' % (
    row.cx(0), Y - 30, (row.cx(0) + row.cx(5)) / 2, Y - 70, row.cx(5), Y - 30, MID)
f.show(arc + arrow(row.cx(5) - 6, Y - 38, row.cx(5), Y - 30, MID, 1.8, None, 7), 4.4, hide=7.6)
f.show(ring(row.x(5), Y, 56), 5.2, hide=7.6)
status(f, 0, Y + 130, 'jump to 1040 → a[5] = 15', 5.2, hide=7.6)
row.c[5].tone(7.6, 'f')
f.show(T(row.cx(5), Y + CH + 50, '✓ found', TG, mono=True, bold=True), 7.8)
finish(f, 0, Y + 108, '1 step · the same for 8 cells or 8 million', 8.0)
figs['m1'] = f.render(Y + 142)

# ---------------------------------------------------------------- m2 frozen strings
L2 = ['s = "cat"', 's[0] = "b"     # TypeError', 's = "b" + s[1:]   # new string']
f = Fig('as-m2-', 'A string cat sits in three cells. Writing s[0] fails: strings cannot change. Instead a new row bat is built: b is new, a and t are copied down; the old row is dropped and s points at the new one.',
        'STRINGS ARE FROZEN · A CHANGE BUILDS A NEW STRING', L2, W=640)
X0 = f.X0 + 40; Y1, Y2 = 60, 150
f.line(.2, 0)
r1 = Row(f, X0, Y1, list('cat'), t0=.3)
sp = Ptr(f, 's', .9, X0, Y1 + CH / 2, side='left')
f.line(2.0, 1)
f.show(ring(r1.x(0), Y1), 2.2, hide=4.4)
status(f, f.X0, Y2 + 90, 's[0] = "b" → error: str is immutable', 2.2, hide=4.4)
f.line(4.6, 2)
status(f, f.X0, Y2 + 90, 'build a new row: "b" + copy of s[1:]', 4.6, hide=8.6)
new = [Obj(f, cdraw('b'), 5.0, X0, Y2)]
for k in (1, 2):
    o = Obj(f, cdraw(r1.v[k]), 5.6 + k * .7, r1.x(k), Y1); o.move(5.8 + k * .7, r1.x(k), Y2); new.append(o)
for i in range(3): f.show(T(r1.cx(i), Y2 + CH + 16, str(i), FA, cls='sv-s', mono=True), 5.0)
sp.move(7.8, X0, Y2 + CH / 2)
for c in r1.c: c.tone(8.0, 'g')
for o in new: o.tone(8.8, 'f')
finish(f, f.X0, Y2 + 90, 's = "bat" · old "cat" untouched · every char copied', 9.0)
figs['m2'] = f.render(Y2 + 100)

# ---------------------------------------------------------------- p1 index O(1) + graph
f = Fig('as-p1-', 'Reading a[3] from 4 cells, a[700] from 1,000 cells and a[9999999] from ten million cells each takes one jump. Graph: steps against n: reading by index is a flat line at 1, scanning is the line y = n.',
        'READ BY INDEX · O(1) · THE LENGTH NEVER ENTERS', W=700)
cases = [(4, 3, 'a[3]'), (1000, 700, 'a[700]'), (10_000_000, 9_999_999, 'a[9999999]')]
y = 40; t = .3
for k, (n, i, lab) in enumerate(cases):
    yy = y + k * 56
    f.show(T(0, yy + 22, 'n = {:,}'.format(n), MU, 'start', mono=True), t)
    xs = [150, 186, 222, 258, 330, 366]
    for q, x in enumerate(xs):
        f.show(R(x, yy, 32, 30, 'var(--bg)', RULE_HI, 5, 1.1), t + q * .04)
    f.show(T(310, yy + 20, '…', FA, mono=True), t)
    # the target cell
    tx = 150 + 36 * min(i, 3) if n == 4 else 330
    f.show(ring(tx, yy, 32, 30), t + .8, hide=t + 2.2)
    f.show(R(tx, yy, 32, 30, TG, TG, 5, 1.1), t + 2.2)
    f.show(T(420, yy + 20, '%s → 1 jump' % lab, TG, 'start', mono=True, bold=True), t + 1.2)
    t += 2.4
gx, gy, gw, gh = 60, 230, 520, 150
px, py = graph(f, gx, gy, gw, gh, 10, 10, [
    (lambda v: v, 'scan: n steps', GH, 2, 8.6),
    (lambda v: 1, 'a[i]: 1 step', TG, 2.6, 7.6)], t, xt=(2, 4, 6, 8, 10), yt=(2, 4, 6, 8, 10), yl='steps')
finish(f, gx, gy + gh + 40, 'address = start + i × size: one multiplication, any n', t + 3.2)
figs['p1'] = f.render(gy + gh + 50)

# ---------------------------------------------------------------- p2 append amortized
L3 = ['def append(x):', '    if n == cap:', '        grow()   # copy n cells', '    a[n] = x', '    n += 1']
f = Fig('as-p2-', 'Appending 1 to 8 into a block of capacity 4. The first four are one step each. At 5 the block is full: a block of 8 is allocated, the four cells are copied down, the old block is dropped. 6, 7, 8 are one step again. 8 appends cost 4 copies: about one per append.',
        'APPEND · FULL → GROW AND COPY · O(1) ON AVERAGE', L3, W=760)
X0 = f.X0 + 10; Y1, Y2 = 66, 156
def block(x, y, cap, t, hide=None):
    f.show(R(x - 5, y - 5, cap * P + 4, CH + 10, 'none', RULE_HI, 9, 1.2, '5 4') + T(x + cap * P - 4, y - 10, 'cap = %d' % cap, FA, 'end', cls='sv-s', mono=True), t, hide)
block(X0, Y1, 4, .2)
cells = []; t = 1.0; copies = 0
def st(txt, t, h): status(f, f.X0, Y2 + 82, txt, t, hide=h)
for v in range(1, 9):
    f.line(t, 1)
    n = v - 1
    if v == 5:
        f.show(ring(X0 - 2, Y1 - 2, 4 * P - 2, CH + 4), t + .4, hide=t + 4.6)
        st('n = 4 == cap → grow', t + .4, t + 1.6)
        f.line(t + 1.2, 2)
        block(X0, Y2, 8, t + 1.4)
        st('allocate 8 cells, copy 4', t + 1.8, t + 4.6)
        for k, o in enumerate(cells):
            o.move(t + 2.0 + k * .4, X0 + k * P, Y2)
        f.show(R(X0 - 5, Y1 - 5, 4 * P + 4, CH + 10, 'var(--sunk)', 'var(--rule)', 9, 1) + T(X0 + 2 * P - 3, Y1 + 23, 'old block freed', GH, cls='sv-s'), t + 4.0)
        copies = 4; t += 4.6
    yy = Y1 if v <= 4 else Y2
    f.line(t, 3)
    o = Obj(f, cdraw(v), t, X0 + n * P, yy); cells.append(o)
    st('a[%d] = %d · copies so far %d' % (n, v, copies), t, t + 1.2)
    f.line(t + .6, 4)
    t += 1.3
cells[-1].tone(t, 'f')
for k in range(8): f.show(T(X0 + k * P + CW / 2, Y2 + CH + 16, str(k), FA, cls='sv-s', mono=True), t)
finish(f, f.X0, Y2 + 82, '8 appends · 4 copies · ≈ 1 per append = O(1) amortized', t + .2)
f.show(T(f.X0, Y2 + 104, 'Python grows by ~1.125× instead of 2×: more grows, still O(1) on average', MU, 'start'), t + .6)
figs['p2'] = f.render(Y2 + 114)

# ---------------------------------------------------------------- p3 insert at front + graph
L4 = ['for k in range(n - 1, -1, -1):', '    a[k + 1] = a[k]   # shift', 'a[0] = x']
f = Fig('as-p3-', 'Insert 7 at the front of six cells: starting from the last, each cell slides one place right, six shifts, then 7 goes into index 0. Graph: shifts against n: insert at front climbs as n, append at the end stays at 0.',
        'INSERT AT THE FRONT · EVERY CELL SHIFTS · O(n)', L4, W=760)
X0 = f.X0 + 10; Y = 76
vals = [4, 9, 23, 8, 15, 42]
row = Row(f, X0, Y, vals)
f.show(T(X0 + 6 * P + CW / 2, Y + CH + 16, '6', FA, cls='sv-s', mono=True), 3.0)
goal_corner(f, f.X0, 'insert 7 at index 0', 1.0)
kp = Ptr(f, 'k', 2.0, row.cx(5), Y + CH + 22)
t = 2.4
for k in range(5, -1, -1):
    f.line(t, 0)
    if k < 5: kp.move(t, row.cx(k), Y + CH + 22)
    f.line(t + .5, 1)
    f.show(ring(row.x(k), Y), t + .5, hide=t + 1.4)
    status(f, f.X0, Y + 112, 'a[%d] = a[%d] → shifts = %d' % (k + 1, k, 6 - k), t + .5, hide=t + 1.6)
    row.c[k].move(t + .9, row.x(k + 1), Y)
    t += 1.7
f.line(t, 2)
kp.die(t)
Obj(f, cdraw(7), t + .2, row.x(0), Y, 'f')
f.show(T(row.cx(0), Y + CH + 34, '✓ done', TG, mono=True, bold=True), t + .5)
status(f, f.X0, Y + 112, '6 shifts for 6 cells → O(n)', t + .5, c=TG, bold=True)
t += 1.4
gx, gy, gw, gh = f.X0 + 40, Y + 150, 280, 120
graph(f, gx, gy, gw, gh, 10, 10, [
    (lambda v: v, 'insert at front: n', MID, 2.4, 6.0),
    (lambda v: 0.05, 'append: 0 shifts', TG, 2.4, 6.4)], t, xt=(2, 4, 6, 8, 10), yt=(5, 10), yl='shifts')
figs['p3'] = f.render(gy + gh + 30)

# ---------------------------------------------------------------- p4 delete
L5 = ['for k in range(i, n - 1):', '    a[k] = a[k + 1]   # shift', 'n -= 1']
f = Fig('as-p4-', 'Delete a[2] from six cells: 23 is removed and the three cells after it each slide one place left. Three shifts; deleting the last cell would need none.',
        'DELETE IN THE MIDDLE · THE TAIL SHIFTS LEFT · O(n)', L5, W=700)
X0 = f.X0 + 10; Y = 76
vals = [4, 9, 23, 8, 15, 42]
row = Row(f, X0, Y, vals, idx={5: 9.0})
goal_on(f, row.x(2), Y, 'delete a[2]', 1.0, f.X0, 22, ring_hide=3.8)
row.c[2].tone(3.0, 'g'); row.c[2].die(3.8)
kp = Ptr(f, 'k', 3.0, row.cx(2), Y + CH + 22)
t = 3.4
for k in range(2, 5):
    f.line(t, 0)
    if k > 2: kp.move(t, row.cx(k), Y + CH + 22)
    f.line(t + .5, 1)
    f.show(ring(row.x(k + 1), Y), t + .5, hide=t + 1.4)
    status(f, f.X0, Y + 112, 'a[%d] = a[%d] → shifts = %d' % (k, k + 1, k - 1), t + .5, hide=t + 1.6)
    row.c[k + 1].move(t + .9, row.x(k), Y)
    t += 1.7
f.line(t, 2); kp.die(t)
finish(f, f.X0, Y + 112, '3 shifts · cost n − 1 − i · pop() at the end: 0', t + .5)
figs['p4'] = f.render(Y + 124)

# ---------------------------------------------------------------- p5 search by value
L6 = ['for i in range(n):', '    if a[i] == x:', '        return i', 'return -1']
f = Fig('as-p5-', 'Search for 15 in an unsorted list of seven: i walks from index 0, each cell that is not 15 greys out. a[4] = 15: found after 5 checks; a missing value would cost all 7.',
        'SEARCH BY VALUE · LOOK AT EVERY CELL · O(n)', L6, W=700)
X0 = f.X0 + 10; Y = 76
vals = [4, 9, 23, 8, 15, 42, 6]
row = Row(f, X0, Y, vals)
goal_on(f, row.x(4), Y, 'x = 15', 1.0, f.X0, 22)
ip = Ptr(f, 'i', 2.8, row.cx(0), Y + CH + 22)
t = 3.2
for i in range(5):
    f.line(t, 0)
    if i: ip.move(t, row.cx(i), Y + CH + 22)
    f.line(t + .5, 1)
    f.show(ring(row.x(i), Y), t + .5, hide=t + 1.6)
    eq = vals[i] == 15
    status(f, f.X0, Y + 112, 'a[%d] = %d %s 15%s' % (i, vals[i], '==' if eq else '≠', '' if eq else ' → next'), t + .5, hide=t + 1.6 if not eq else None)
    if not eq: row.c[i].tone(t + 1.3, 'g')
    t += 1.8
f.line(t - 1.0, 2)
ip.die(t - .6)
row.c[4].tone(t - .6, 'f')
f.show(T(row.cx(4), Y + CH + 34, '✓ found', TG, mono=True, bold=True), t - .4)
finish(f, f.X0, Y + 134, 'found at index 4 · 5 checks · worst case n checks', t - .2)
figs['p5'] = f.render(Y + 146)

# ---------------------------------------------------------------- p6 building a string
L7 = ['s = ""', 'for c in "abcd":', '    s += c   # copies all of s', '# better: "".join(parts)']
f = Fig('as-p6-', 'Building abcd with s += c: each step makes a new string and copies every character so far: 1, 2, 3, 4 copies, 10 in total, which grows as n squared over 2. join copies each character once: 4.',
        'BUILDING A STRING · += COPIES EVERYTHING EACH TIME', L7, W=720)
X0 = f.X0 + 10; Y0 = 44; RH = 44
f.line(.2, 0)
total = 0; t = .8; prev = []
for k, c in enumerate('abcd'):
    f.line(t, 1); f.line(t + .4, 2)
    y = Y0 + k * RH
    cur = []
    for q, o in enumerate(prev):
        n = Obj(f, cdraw('abcd'[q], 34, 30), t + .5, X0 + q * 38, y - RH); n.move(t + .6 + q * .15, X0 + q * 38, y); cur.append(n)
    cur.append(Obj(f, cdraw(c, 34, 30), t + 1.2, X0 + k * 38, y))
    for o in prev: o.tone(t + 1.6, 'g')
    total += k + 1
    f.show(T(X0 + 4 * 38 + 14, y + 20, 's = "%s"   +%d copies' % ('abcd'[:k + 1], k + 1), MU, 'start', mono=True), t + 1.4)
    prev = cur; t += 2.4
for o in prev: o.tone(t, 'f')
f.line(t, 3)
status(f, f.X0, Y0 + 4 * RH + 20, '1 + 2 + 3 + 4 = 10 copies · n chars → n²/2 copies', t + .2, c=TG, bold=True)
status(f, f.X0, Y0 + 4 * RH + 42, '"".join(parts) → 4 copies: each char once', t + 1.2, c=MU)
figs['p6'] = f.render(Y0 + 4 * RH + 52)

# ---------------------------------------------------------------- q1 in-place filter
L8 = ['j = 0', 'for i in range(n):', '    if a[i] != val:', '        a[j] = a[i]', '        j += 1', 'return j']
f = Fig('as-q1-', 'Remove every 3 from 3 2 2 3 4 3 5 in place. i reads every cell, j marks where the next kept value goes. Kept values are copied to j; 3s are skipped and greyed. The first four cells end as 2 2 4 5, k = 4.',
        'IN-PLACE FILTER · i READS, j WRITES · REMOVE val = 3', L8, W=760)
X0 = f.X0 + 10; Y = 86
vals = [3, 2, 2, 3, 4, 3, 5]
row = Row(f, X0, Y, vals)
goal_corner(f, f.X0, 'val = 3', 1.0)
f.line(1.6, 0)
jp = Ptr(f, 'j', 2.0, row.cx(0), Y, side='above')
ip = Ptr(f, 'i', 2.4, row.cx(0), Y + CH + 22)
t = 3.0; j = 0
for i, v in enumerate(vals):
    f.line(t, 1)
    if i: ip.move(t, row.cx(i), Y + CH + 22)
    f.line(t + .5, 2)
    f.show(ring(row.x(i), Y), t + .5, hide=t + 1.8)
    if v == 3:
        status(f, f.X0, Y + 122, 'a[%d] = 3 → skip' % i, t + .5, hide=t + 1.8)
        row.c[i].tone(t + 1.1, 'g')
        t += 2.0
    else:
        status(f, f.X0, Y + 122, 'a[%d] = %d ≠ 3 → a[%d] = %d' % (i, v, j, v), t + .5, hide=t + 2.6)
        f.line(t + 1.0, 3)
        if i != j: row.fly(v, row.x(i), Y, j, t + 1.0)
        f.line(t + 1.9, 4)
        j += 1; jp.move(t + 2.0, row.cx(j), Y)
        t += 2.8
f.line(t, 5)
ip.die(t); jp.die(t)
for k in range(j): row.c[k].tone(t + .2, 'f')
for k in range(j, 7): row.c[k].tone(t + .2, 'g') if row.c[k] and vals[k] != 3 else None
finish(f, f.X0, Y + 122, 'k = 4 · kept 2 2 4 5 · one pass, no extra array', t + .4)
figs['q1'] = f.render(Y + 134)

# ---------------------------------------------------------------- q2 fill from the back
L9 = ['i, j, k = m - 1, n - 1, m + n - 1', 'while j >= 0:', '    if i >= 0 and a[i] > b[j]:', '        a[k] = a[i]; i -= 1', '    else:', '        a[k] = b[j]; j -= 1', '    k -= 1']
f = Fig('as-q2-', 'Merge b = 2 5 6 into a = 1 4 7 with three spare cells at the end. Write from the back: compare a[i] with b[j], the bigger one goes to a[k], k moves left. Nothing ever shifts. a ends as 1 2 4 5 6 7.',
        'FILL FROM THE BACK · MERGE b INTO a WITHOUT SHIFTING', L9, W=760)
X0 = f.X0 + 30; YA, YB = 80, 196
f.static(T(X0 - 12, YA + 23, 'a', MU, 'end', mono=True, bold=True)); f.static(T(X0 - 12, YB + 23, 'b', MU, 'end', mono=True, bold=True))
A = Row(f, X0, YA, [1, 4, 7, 0, 0, 0]); B = Row(f, X0, YB, [2, 5, 6], t0=.6)
goal_corner(f, f.X0, 'merge sorted b into a', 1.0)
f.line(1.6, 0)
i, j, k = 2, 2, 5
kp = Ptr(f, 'k', 2.0, A.cx(5), YA, side='above')
ip = Ptr(f, 'i', 2.0, A.cx(2), YA + CH + 22)
jp = Ptr(f, 'j', 2.0, B.cx(2), YB + CH + 22)
t = 2.8; SY = YB + 98
while j >= 0:
    f.line(t, 1); f.line(t + .4, 2)
    if i >= 0: f.show(ring(A.x(i), YA), t + .4, hide=t + 2.0)
    f.show(ring(B.x(j), YB), t + .4, hide=t + 2.0)
    if i >= 0 and A.v[i] > B.v[j]:
        status(f, f.X0, SY, 'a[%d] = %d > b[%d] = %d → a[%d] = %d' % (i, A.v[i], j, B.v[j], k, A.v[i]), t + .4, hide=t + 2.4)
        f.line(t + 1.0, 3); v = A.v[i]
        if i != k: A.fly(v, A.x(i), YA, k, t + 1.0); Obj(f, cdraw(v), t + 1.6, A.x(i), YA, 'g')
        i -= 1
        if i >= 0: ip.move(t + 1.9, A.cx(i), YA + CH + 22)
        else: ip.die(t + 1.9)
    else:
        status(f, f.X0, SY, ('a[%d] = %d < b[%d] = %d' % (i, A.v[i], j, B.v[j]) if i >= 0 else 'i < 0') + ' → a[%d] = %d' % (k, B.v[j]), t + .4, hide=t + 2.4)
        f.line(t + 1.0, 5); v = B.v[j]
        A.fly(v, B.x(j), YB, k, t + 1.0); B.c[j].tone(t + 1.0, 'g')
        j -= 1
        if j >= 0: jp.move(t + 1.9, B.cx(j), YB + CH + 22)
        else: jp.die(t + 1.9)
    f.line(t + 2.0, 6)
    k -= 1
    if j >= 0: kp.move(t + 2.2, A.cx(k), YA)
    else: kp.die(t + 2.2)
    t += 2.9
if i >= 0: ip.die(t)
for c in A.c: c.tone(t, 'f')
f.show(T(A.cx(0) + 2.5 * P, YA + CH + 50, '✓ merged', TG, mono=True, bold=True), t + .2)
finish(f, f.X0, SY, 'a = 1 2 4 5 6 7 · each cell written once · O(m + n)', t + .3)
figs['q2'] = f.render(SY + 12)

# ---------------------------------------------------------------- q3 three reversals
L10 = ['def rev(l, r):', '    while l < r:', '        a[l], a[r] = a[r], a[l]', '        l += 1; r -= 1', 'rev(0, n - 1)', 'rev(0, k - 1)', 'rev(k, n - 1)']
f = Fig('as-q3-', 'Rotate 1 2 3 4 5 6 7 right by k = 3 with three reversals. Reverse all: 7 6 5 4 3 2 1. Reverse the first 3: 5 6 7 4 3 2 1. Reverse the rest: 5 6 7 1 2 3 4. Each reversal swaps the ends with l and r walking inward.',
        'REVERSE IN PLACE · ROTATE RIGHT BY k = 3 WITH THREE REVERSALS', L10, W=760)
X0 = f.X0 + 10; Y = 92
row = Row(f, X0, Y, [1, 2, 3, 4, 5, 6, 7])
goal_corner(f, f.X0, 'rotate right by 3', 1.0)
t = 2.0; SY = Y + 130
for call, (l, r) in zip((4, 5, 6), ((0, 6), (0, 2), (3, 6))):
    f.line(t, call); t0 = t; l0, r0 = l, r
    lp = Ptr(f, 'l', t + .4, row.cx(l), Y + CH + 30); rp = Ptr(f, 'r', t + .4, row.cx(r), Y + CH + 30)
    t += 1.0
    while l < r:
        f.line(t, 1); f.line(t + .3, 2)
        f.show(ring(row.x(l), Y), t + .3, hide=t + 1.6); f.show(ring(row.x(r), Y), t + .3, hide=t + 1.6)
        lift_swap(row, l, r, t + .5)
        f.line(t + 1.6, 3)
        l += 1; r -= 1
        if l < r: lp.move(t + 1.7, row.cx(l), Y + CH + 30); rp.move(t + 1.7, row.cx(r), Y + CH + 30)
        t += 2.2
    lp.die(t); rp.die(t)
    br = L(row.x(l0), Y - 40, row.x(r0) + CW, Y - 40, MID, 2) + L(row.x(l0), Y - 44, row.x(l0), Y - 36, MID, 2) + L(row.x(r0) + CW, Y - 44, row.x(r0) + CW, Y - 36, MID, 2)
    f.show(br, t0 + .2, hide=t)
    status(f, f.X0, SY, 'rev(%d, %d)' % (l0, r0), t0 + .2, hide=t + .9)
    status(f, f.X0, SY + 22, 'a = ' + ' '.join(map(str, row.v)), t, hide=t + .9, c=MU)
    t += 1.1
for c in row.c: c.tone(t, 'f')
finish(f, f.X0, SY, '5 6 7 1 2 3 4 · 3 reversals · O(n) time, O(1) memory', t + .2)
figs['q3'] = f.render(SY + 12)

# ---------------------------------------------------------------- q4 prefix and suffix products
L11 = ['ans = [1] * n', 'p = 1', 'for i in range(n):', '    ans[i] = p; p *= a[i]', 's = 1', 'for i in range(n - 1, -1, -1):', '    ans[i] *= s; s *= a[i]']
f = Fig('as-q4-', 'Product of the array except self for a = 1 2 3 4. Left pass: ans[i] gets the product of everything left of i (1 1 2 6). Right pass: ans[i] is multiplied by the product of everything right of i, giving 24 12 8 6. No division.',
        'TWO PASSES · LEFT PRODUCT × RIGHT PRODUCT · NO DIVISION', L11, W=760)
X0 = f.X0 + 60; YA, YN = 70, 170
f.static(T(X0 - 12, YA + 23, 'a', MU, 'end', mono=True, bold=True)); f.static(T(X0 - 12, YN + 23, 'ans', MU, 'end', mono=True, bold=True))
a = [1, 2, 3, 4]
A = Row(f, X0, YA, a, w=54, pitch=64)
f.line(.6, 0)
N = Row(f, X0, YN, [1, 1, 1, 1], t0=.8, idx=False, w=54, pitch=64)
goal_corner(f, f.X0 + 0, 'ans[i] = product of all but a[i]', 1.2)
SY = YN + 70
f.line(2.0, 1); f.line(2.4, 2)
ip = Ptr(f, 'i', 2.6, A.cx(0), YA + CH + 22)
p = 1; t = 3.0
for i in range(4):
    f.line(t, 3)
    if i: ip.move(t - .4, A.cx(i), YA + CH + 22)
    f.show(ring(A.x(i), YA, 54), t, hide=t + 1.6)
    status(f, f.X0, SY, 'ans[%d] = p = %d · p = %d × %d = %d' % (i, p, p, a[i], p * a[i]), t, hide=t + 1.8)
    N.set(i, p, t + .6)
    p *= a[i]; t += 2.0
f.line(t, 4); f.line(t + .4, 5)
ip.move(t + .4, A.cx(3), YA + CH + 22)
s = 1; t += 1.0
for i in range(3, -1, -1):
    f.line(t, 6)
    if i < 3: ip.move(t - .4, A.cx(i), YA + CH + 22)
    f.show(ring(A.x(i), YA, 54), t, hide=t + 1.6)
    old = N.v[i]
    status(f, f.X0, SY, 'ans[%d] = %d × s = %d · s = %d × %d = %d' % (i, old, old * s, s, a[i], s * a[i]), t, hide=t + 1.8)
    N.set(i, old * s, t + .6)
    s *= a[i]; t += 2.0
ip.die(t)
for c in N.c: c.tone(t, 'f')
finish(f, f.X0, SY, 'ans = 24 12 8 6 · two passes · O(n)', t + .2)
figs['q4'] = f.render(SY + 12)

# ---------------------------------------------------------------- q5 spiral walk
L12 = ['top, bot, l, r = 0, m - 1, 0, n - 1', 'while top <= bot and l <= r:', '    top row    l → r;    top += 1', '    right col  top → bot; r -= 1', '    bottom row r → l;    bot -= 1', '    left col   bot → top; l += 1']
f = Fig('as-q5-', 'Spiral order of a 3 by 4 matrix 1 to 12. Walk the top row, the right column, the bottom row, the left column; after each side its boundary moves inward. Output: 1 2 3 4 8 12 11 10 9 5 6 7.',
        'SPIRAL WALK · FOUR BOUNDARIES SHRINK INWARD', L12, W=760)
GX = f.X0 + 56; GY = 72; GP = 48
M = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
cell_o = {}
for rr in range(3):
    for cc in range(4):
        cell_o[rr, cc] = Obj(f, cdraw(M[rr][cc]), .2 + (rr * 4 + cc) * .04, GX + cc * GP, GY + rr * GP)
OY = GY + 3 * GP + 34; OW = 30; OP = 34
f.static(T(f.X0, OY - 8, 'output', FA, 'start', cls='sv-s'))
top, bot, l, r = 0, 2, 0, 3
tp = Ptr(f, 'top', 1.2, GX, GY + CH / 2 + top * GP, side='left'); bp = Ptr(f, 'bot', 1.2, GX, GY + CH / 2 + bot * GP, side='left')
lp = Ptr(f, 'l', 1.2, GX + CW / 2 + l * GP, GY, side='above'); rp = Ptr(f, 'r', 1.2, GX + CW / 2 + r * GP, GY, side='above')
f.line(1.0, 0)
out = []; t = 2.0
def visit(rr, cc):
    global t
    ro = Obj(f, lambda x, y, tn: ring(x, y), t, GX + cc * GP, GY + rr * GP); ro.die(t + .7)
    k = len(out)
    o = Obj(f, cdraw(M[rr][cc], OW, 30), t + .2, GX + cc * GP, GY + rr * GP); o.move(t + .3, f.X0 + k * OP, OY)
    out.append(o); cell_o[rr, cc].tone(t + .5, 'g'); t += .9
while top <= bot and l <= r:
    f.line(t, 2)
    for cc in range(l, r + 1): visit(top, cc)
    top += 1; tp.move(t, GX, GY + CH / 2 + top * GP); t += .5
    f.line(t, 3)
    for rr in range(top, bot + 1): visit(rr, r)
    r -= 1; rp.move(t, GX + CW / 2 + r * GP, GY); t += .5
    if top <= bot:
        f.line(t, 4)
        for cc in range(r, l - 1, -1): visit(bot, cc)
        bot -= 1; bp.move(t, GX, GY + CH / 2 + bot * GP); t += .5
    if l <= r:
        f.line(t, 5)
        for rr in range(bot, top - 1, -1): visit(rr, l)
        l += 1; lp.move(t, GX + CW / 2 + l * GP, GY); t += .5
    f.line(t, 1); t += .5
for o in out: o.tone(t, 'f')
for p_ in (tp, bp, lp, rp): p_.die(t)
finish(f, f.X0, OY + 56, '12 cells · each visited once · O(m × n)', t + .2)
figs['q5'] = f.render(OY + 66)

# ---------------------------------------------------------------- q6 rotate a matrix
L13 = ['for i in range(n):', '    for j in range(i + 1, n):', '        m[i][j], m[j][i] = m[j][i], m[i][j]', 'for row in m:', '    row.reverse()']
f = Fig('as-q6-', 'Rotate a 3 by 3 matrix 90 degrees clockwise in place. First transpose: swap m[i][j] with m[j][i] across the diagonal, three swaps. Then reverse each row. Result 7 4 1 / 8 5 2 / 9 6 3.',
        'ROTATE A MATRIX · TRANSPOSE, THEN REVERSE EACH ROW', L13, W=760)
GX = f.X0 + 40; GY = 70; GP = 52
M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
G_ = {}
for rr in range(3):
    for cc in range(3):
        G_[rr, cc] = Obj(f, cdraw(M[rr][cc]), .2 + (rr * 3 + cc) * .05, GX + cc * GP, GY + rr * GP)
goal_corner(f, f.X0, 'rotate 90° clockwise', 1.0)
DIAG = L(GX - 8, GY - 8, GX + 2 * GP + CW + 8, GY + 2 * GP + CH + 8, MID, 1.2, '4 4')
SY = GY + 3 * GP + 26
t = 2.6
def swap2(a_, b_, t):
    A_, B_ = G_[a_], G_[b_]
    ax, ay = GX + a_[1] * GP, GY + a_[0] * GP; bx, by = GX + b_[1] * GP, GY + b_[0] * GP
    f.show(ring(ax, ay), t, hide=t + 1.6); f.show(ring(bx, by), t, hide=t + 1.6)
    mx, my = (ax + bx) / 2, (ay + by) / 2
    dx, dy = bx - ax, by - ay; n_ = math.hypot(dx, dy); ox, oy = -dy / n_ * 22, dx / n_ * 22
    A_.move(t + .3, mx + ox, my + oy); A_.move(t + .8, bx, by)
    B_.move(t + .3, mx - ox, my - oy); B_.move(t + .8, ax, ay)
    G_[a_], G_[b_] = B_, A_; M[a_[0]][a_[1]], M[b_[0]][b_[1]] = M[b_[0]][b_[1]], M[a_[0]][a_[1]]
for i in range(3):
    for j in range(i + 1, 3):
        f.line(t, 0); f.line(t + .3, 1); f.line(t + .6, 2)
        status(f, f.X0, SY, 'swap m[%d][%d] ↔ m[%d][%d]' % (i, j, j, i), t + .6, hide=t + 2.2)
        swap2((i, j), (j, i), t + .6); t += 2.4
status(f, f.X0, SY, 'transposed: rows became columns', t, hide=t + 1.4); t += 1.6
f.show(DIAG, 2.0, hide=t)
for rr in range(3):
    f.line(t, 3); f.line(t + .4, 4)
    status(f, f.X0, SY, 'reverse row %d' % rr, t + .4, hide=t + 2.0)
    swap2((rr, 0), (rr, 2), t + .4); t += 2.2
for o in G_.values(): o.tone(t, 'f')
finish(f, f.X0, SY, '7 4 1 / 8 5 2 / 9 6 3 · turned 90° · O(1) extra memory', t + .2)
figs['q6'] = f.render(SY + 12)

dump('array-string', figs)
