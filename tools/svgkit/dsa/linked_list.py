"""Figures for content/01-dsa/03-data-structures/linked-list. Output: /tmp/dsa/linked-list.json"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seqkit import *

PITCH = 92

class LL:
    """Nodes as sliding Objs + links that are redrawn whenever the structure or a position changes."""
    def __init__(s, f):
        s.f = f; s.o = {}; s.pos = {}; s.val = {}; s.w = {}; s.kind = {}
        s.cur = {}   # edge key -> (t_start, svg)
    def add(s, i, v, t, x, y, tone='u', kind='node'):
        s.val[i] = v; s.pos[i] = (x, y); s.kind[i] = kind
        if kind == 'none':
            s.w[i] = 38
            s.o[i] = Obj(s.f, lambda xx, yy, tn: T(xx + 2, yy + NH / 2 + 4, 'None', FA, 'start', mono=True), t, x, y)
        else:
            s.w[i] = NW
            s.o[i] = Obj(s.f, lambda xx, yy, tn, v=v: node(xx, yy, v, tn), t, x, y, tone)
        return s.o[i]
    def move(s, i, t, x, y): s.o[i].move(t, x, y); s.pos[i] = (x, y)
    def tone(s, i, t, tn): s.o[i].tone(t, tn)
    def die(s, i, t): s.o[i].die(t); del s.pos[i]
    def _edge(s, a, b, c, kind):
        (x1, y1), (x2, y2) = s.pos[a], s.pos[b]
        sw = 1.8 if c == MID else 1.4
        if kind == 'dbl':
            return (arrow(x1 + NW, y1 + 12, x2 - 1, y2 + 12, c, sw, None, 6)
                    + arrow(x2, y2 + 25, x1 + NW + 1, y1 + 25, c, sw, None, 6))
        dx, dy = x1 + NV + (NW - NV) / 2, y1 + NH / 2
        if x2 >= x1 + s.w[a] - 1:
            if abs(y1 - y2) < 1 and x2 - x1 > NW * 2.2:
                sx, ex = x1 + NV + (NW - NV) / 2, x2 + 10
                qx, qy = (sx + ex) / 2, y1 - 34
                a_ = math.atan2(y2 - qy, ex - qx); hx, hy = ex - 7 * math.cos(a_), y2 - 7 * math.sin(a_)
                poly = '%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (ex, y2, hx - 3.5 * math.sin(a_), hy + 3.5 * math.cos(a_), hx + 3.5 * math.sin(a_), hy - 3.5 * math.cos(a_))
                return ('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="%s"/>' % (sx, y1 + NH / 2, qx, qy, hx, hy, c, sw)
                        + '<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (sx, y1 + NH / 2, c) + '<polygon points="%s" fill="%s"/>' % (poly, c))
            if abs(y1 - y2) < 1: return arrow(dx, dy, x2 - 1, y2 + NH / 2, c, sw, None, 6)
            return arrow(dx, dy + (6 if y2 > y1 else -6), x2 - 1, y2 + NH / 2, c, sw, None, 6)
        # backwards: arc over the top
        sx, sy = dx, y1
        ex, ey = x2 + s.w[b] / 2 + 6, y2
        top = min(y1, y2) - 26 - abs(sx - ex) * .08
        qx, qy = (sx + ex) / 2, top
        a_ = math.atan2(ey - qy, ex - qx); hx, hy = ex - 7 * math.cos(a_), ey - 7 * math.sin(a_)
        poly = '%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (ex, ey, hx - 3.5 * math.sin(a_), hy + 3.5 * math.cos(a_), hx + 3.5 * math.sin(a_), hy - 3.5 * math.cos(a_))
        return ('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="%s"/>' % (sx, sy, qx, qy, hx, hy, c, sw)
                + '<polygon points="%s" fill="%s"/>' % (poly, c))
    def links(s, t_hide, t_show, edges, hot=(), kind='one'):
        """edges: list of (a, b). hot: edges drawn violet this step."""
        new = {}
        for a, b in edges:
            c = MID if (a, b) in hot else MU
            k = (a, b, s.pos[a], s.pos[b], c, kind)
            new[k] = None
        for k in list(s.cur):
            if k not in new:
                t0, svg = s.cur.pop(k); s.f.show(svg, t0, hide=t_hide)
        for k in new:
            if k not in s.cur: s.cur[k] = (t_show, s._edge(k[0], k[1], k[4], k[5]))
    def flush(s):
        for k, (t0, svg) in s.cur.items(): s.f.show(svg, t0)
        s.cur = {}

class NP:
    """named pointer that follows nodes"""
    def __init__(s, ll, name, side='above', ln=14, x_off=0):
        s.ll, s.name, s.side, s.ln, s.o, s.xo = ll, name, side, ln, None, x_off
    def _xy(s, i):
        x, y = s.ll.pos[i]
        cx = x + (NV / 2 if s.ll.kind[i] == 'node' else 16) + s.xo
        return cx, (y if s.side == 'above' else y + NH)
    def at(s, t, i):
        cx, y = s._xy(i)
        if s.o is None: s.o = Ptr(s.ll.f, s.name, t, cx, y, side=s.side, ln=s.ln)
        else: s.o.move(t, cx, y)
        return s
    def die(s, t): s.o.die(t)

def chain(ids): return list(zip(ids, ids[1:]))
figs = {}

# ---------------------------------------------------------------- m1 nodes and arrows
f = Fig('ll-m1-', 'Four nodes 3, 7, 1, 9 appear scattered in memory. Each node holds a value and an arrow to the next node; head points at the first, the last points to None. The nodes then slide into a row, but only the arrows define the order.',
        'NODES AND ARROWS · EACH NODE KNOWS ONLY THE NEXT ONE', W=640)
ll = LL(f)
scat = [(40, 150), (170, 60), (320, 180), (450, 80)]
vals = [3, 7, 1, 9]
for k, ((x, y), v) in enumerate(zip(scat, vals)): ll.add(k, v, .3 + k * .25, x, y)
ll.add('N', None, .3, 570, 170, kind='none')
f.show(T(320, 270, 'nodes live anywhere in memory', MU, 'middle'), .4, hide=5.4)
t = 1.6
for k in range(4):
    ll.links(t, t, chain(list(range(k + 1)) + (['N'] if k == 3 else [])), hot=[(k - 1, k)] if k else [])
    t += .9
hp = NP(ll, 'head', 'above', 18).at(1.2, 0)
ll.links(t + .6, t + .6, chain([0, 1, 2, 3, 'N']))
t += 1.2
Y = 120
for k in range(4): ll.move(k, t, 60 + k * PITCH, Y)
ll.move('N', t, 60 + 4 * PITCH, Y)
hp.at(t, 0)
ll.links(t, t + .7, chain([0, 1, 2, 3, 'N']))
t += 1.4
finish(f, 60, Y + 90, 'head → 3 → 7 → 1 → 9 → None · follow arrows to move', t)
ll.flush()
figs['m1'] = f.render(Y + 104)

# ---------------------------------------------------------------- p1 insert at head
L1 = ['node = Node(5)', 'node.next = head', 'head = node']
f = Fig('ll-p1-', 'List 3 7 1 9. A new node 5 is created to the left. Its arrow is set to the old head, then head moves to the new node. Two pointer changes, no matter how long the list is.',
        'INSERT AT HEAD · TWO POINTER CHANGES · O(1)', L1, W=800)
X0 = f.X0 + 96; Y = 96
ll = LL(f)
for k, v in enumerate([3, 7, 1, 9]): ll.add(k, v, .2 + k * .1, X0 + k * PITCH, Y)
ll.add('N', None, .2, X0 + 4 * PITCH, Y, kind='none')
ll.links(0, .8, chain([0, 1, 2, 3, 'N']))
hp = NP(ll, 'head', 'above', 18).at(.9, 0)
goal_corner(f, f.X0, 'push 5 at the front', 1.2)
f.line(2.2, 0)
ll.add('n', 5, 2.4, X0 - PITCH, Y)
np_ = NP(ll, 'node', 'below', 16).at(2.6, 'n')
status(f, f.X0, Y + 100, 'node = Node(5) · not linked yet', 2.6, hide=4.0)
f.line(4.0, 1)
ll.links(4.2, 4.2, chain(['n', 0, 1, 2, 3, 'N']), hot=[('n', 0)])
status(f, f.X0, Y + 100, 'node.next = head → 5 points at 3', 4.2, hide=5.8)
f.line(5.8, 2)
hp.at(6.0, 'n')
status(f, f.X0, Y + 100, 'head = node → head moves to 5', 6.0, hide=7.4)
np_.die(7.4)
ll.links(7.4, 7.4, chain(['n', 0, 1, 2, 3, 'N']))
ll.tone('n', 7.4, 'f')
f.show(T(X0 - PITCH + NV / 2, Y + NH + 34, '✓ done', TG, mono=True, bold=True), 7.6)
finish(f, f.X0, Y + 100, '2 pointer changes · nothing shifts · O(1) for any length', 7.8)
ll.flush()
figs['p1'] = f.render(Y + 112)

# ---------------------------------------------------------------- p2 find
L2 = ['cur = head', 'while cur:', '    if cur.val == x: return cur', '    cur = cur.next', 'return None']
f = Fig('ll-p2-', 'Find 1 in the list 3 7 5 1 9. cur starts at head and follows one arrow per step; 3, 7, 5 are checked and greyed. At the fourth node cur finds 1. Graph: steps against n; finding by value or by position climbs with n, unlike a[i] in an array.',
        'FIND · FOLLOW THE ARROWS ONE BY ONE · O(n)', L2, W=760)
X0 = f.X0 + 10; Y = 86
ll = LL(f)
vals = [3, 7, 5, 1, 9]
for k, v in enumerate(vals): ll.add(k, v, .2 + k * .1, X0 + k * 84, Y)
ll.add('N', None, .2, X0 + 5 * 84, Y, kind='none')
ll.links(0, .8, chain([0, 1, 2, 3, 4, 'N']))
goal_on(f, X0 + 3 * 84, Y, 'x = 1', 1.0, f.X0 + 0, 24, w=NW, h=NH)
f.line(2.8, 0)
cp = NP(ll, 'cur', 'below', 16).at(3.0, 0)
t = 3.4
for k in range(4):
    f.line(t, 1); f.line(t + .4, 2)
    x, y = ll.pos[k]
    f.show(ring(x, y, NW, NH), t + .4, hide=t + 1.6)
    hit = vals[k] == 1
    status(f, f.X0, Y + 100, 'cur.val = %d %s 1%s' % (vals[k], '==' if hit else '≠', '' if hit else ' → follow the arrow'), t + .4, hide=None if hit else t + 1.7)
    if hit: break
    ll.tone(k, t + 1.2, 'g')
    f.line(t + 1.4, 3)
    cp.at(t + 1.5, k + 1)
    t += 2.1
cp.die(t + 1.4)
ll.tone(3, t + 1.4, 'f')
f.show(T(ll.pos[3][0] + NV / 2, Y + NH + 34, '✓ found', TG, mono=True, bold=True), t + 1.6)
finish(f, f.X0, Y + 122, 'found after 4 steps · no index jump: reaching node k costs k steps', t + 1.8)
t += 2.6
ll.flush()
gx, gy, gw, gh = f.X0 + 40, Y + 160, 300, 110
graph(f, gx, gy, gw, gh, 10, 10, [
    (lambda v: v, 'linked list: n', MID, 2.4, 0),
    (lambda v: 1, 'array a[i]: 1', TG, 2.4, 0)], t, xt=(2, 4, 6, 8, 10), yt=(5, 10), yl='steps')
figs['p2'] = f.render(gy + gh + 30)

# ---------------------------------------------------------------- p3 delete a node you hold
L3 = ['prev.next = prev.next.next']
f = Fig('ll-p3-', 'List 3 7 1 9 with prev already on 7. Delete 1: the arrow from 7 is re-pointed to 9, skipping 1. Node 1 greys out and drops away, 9 slides left. One pointer change.',
        'DELETE · RE-POINT ONE ARROW · O(1) ONCE YOU HOLD prev', L3, W=760, cw=260)
X0 = f.X0 + 10; Y = 90
ll = LL(f)
for k, v in enumerate([3, 7, 1, 9]): ll.add(k, v, .2 + k * .1, X0 + k * PITCH, Y)
ll.add('N', None, .2, X0 + 4 * PITCH, Y, kind='none')
ll.links(0, .8, chain([0, 1, 2, 3, 'N']))
goal_on(f, X0 + 2 * PITCH, Y, 'delete 1', 1.0, f.X0, 24, w=NW, h=NH, ring_hide=4.6)
pp = NP(ll, 'prev', 'below', 16).at(2.6, 1)
status(f, f.X0, Y + 106, 'prev is already on 7 (found earlier)', 2.8, hide=4.0)
f.line(4.0, 0)
f.show(ring(ll.pos[1][0], Y, NW, NH), 4.0, hide=5.8)
ll.links(4.2, 4.2, [(0, 1), (1, 3), (2, 3), (3, 'N')], hot=[(1, 3)])
status(f, f.X0, Y + 106, 'prev.next = 9 → node 1 is skipped', 4.2, hide=7.2)
ll.tone(2, 5.0, 'g')
ll.move(2, 5.8, X0 + 2 * PITCH, Y + 70)
ll.links(5.8, 6.5, [(0, 1), (1, 3), (3, 'N')], hot=[(1, 3)])
ll.die(2, 6.8)
ll.move(3, 6.8, X0 + 2 * PITCH, Y); ll.move('N', 6.8, X0 + 3 * PITCH, Y)
ll.links(6.8, 7.5, chain([0, 1, 3, 'N']))
ll.tone(3, 7.6, 'f') if False else None
finish(f, f.X0, Y + 106, '3 → 7 → 9 · 1 pointer change · O(1) — finding prev is the O(n) part', 7.7)
ll.flush()
figs['p3'] = f.render(Y + 118)

# ---------------------------------------------------------------- p4 reverse
L4 = ['prev, cur = None, head', 'while cur:', '    nxt = cur.next', '    cur.next = prev', '    prev, cur = cur, nxt', 'return prev']
f = Fig('ll-p4-', 'Reverse 3 7 1 9 with three pointers. Each loop: nxt saves the next node, cur.next is flipped to point back at prev, then prev and cur step forward. After four flips prev is on 9, the new head: 9 7 ... read backwards gives 9 1 7 3.',
        'REVERSE · FLIP ONE ARROW PER STEP · O(n)', L4, W=760)
X0 = f.X0 + 60; Y = 96
ll = LL(f)
ll.add('L', None, .2, X0 - 64, Y, kind='none')
for k, v in enumerate([3, 7, 1, 9]): ll.add(k, v, .2 + k * .1, X0 + k * PITCH, Y)
ll.add('N', None, .2, X0 + 4 * PITCH, Y, kind='none')
E = {0: 1, 1: 2, 2: 3, 3: 'N'}
ll.links(0, .8, list(E.items()))
goal_corner(f, f.X0, 'reverse the list', 1.0)
f.line(1.6, 0)
pp = NP(ll, 'prev', 'below', 16).at(1.8, 'L'); cp = NP(ll, 'cur', 'above', 18).at(1.8, 0)
xp = NP(ll, 'nxt', 'below', 16)
t = 2.8; SY = Y + 112
order = [0, 1, 2, 3, 'N']; prev = 'L'
for k in range(4):
    f.line(t, 1); f.line(t + .4, 2)
    xp.at(t + .5, order[k + 1])
    status(f, f.X0, SY, 'nxt = cur.next → %s' % ll.val[order[k + 1]], t + .5, hide=t + 1.4)
    f.line(t + 1.4, 3)
    E[k] = prev
    ll.links(t + 1.5, t + 1.5, [(a, b) for a, b in E.items() if not (a == k)] + [(k, prev)], hot=[(k, prev)])
    f.show(ring(ll.pos[k][0], Y, NW, NH), t + 1.5, hide=t + 2.6)
    status(f, f.X0, SY, 'cur.next = prev → %d now points back to %s' % (ll.val[k], ll.val[prev]), t + 1.5, hide=t + 2.6)
    f.line(t + 2.6, 4)
    pp.at(t + 2.8, k); cp.at(t + 2.8, order[k + 1]); prev = k
    t += 3.5
xp.die(t - .3)
f.line(t, 1); f.line(t + .4, 5)
cp.die(t + .4)
ll.links(t + .4, t + .4, [(a, b) for a, b in E.items()])
ll.tone(3, t + .6, 'f'); ll.die('N', t + .4)
f.show(T(ll.pos[3][0] + NV / 2, Y - 30, 'new head', TG, mono=True, bold=True), t + .8)
finish(f, f.X0, SY, '9 → 1 → 7 → 3 → None · 4 flips for 4 nodes · O(n), O(1) memory', t + .8)
ll.flush()
figs['p4'] = f.render(SY + 12)

# ---------------------------------------------------------------- q1 dummy node merge
L5 = ['tail = dummy = Node(0)', 'while a and b:', '    if a.val <= b.val:', '        tail.next, a = a, a.next', '    else:', '        tail.next, b = b, b.next', '    tail = tail.next', 'tail.next = a or b', 'return dummy.next']
f = Fig('ll-q1-', 'Merge 1 3 5 and 2 4. A dummy node D starts the result row, tail on it. Each step compares the two front nodes; the smaller one slides down after tail, and tail moves to it. When b runs out, the rest of a is attached in one step. Result 1 2 3 4 5.',
        'DUMMY NODE · MERGE TWO SORTED LISTS', L5, W=800)
X0 = f.X0 + 40; YA, YB, YR = 56, 132, 216; P_ = 76
ab_lbl = T(X0 - 14, YA + 23, 'a', MU, 'end', mono=True, bold=True) + T(X0 - 14, YB + 23, 'b', MU, 'end', mono=True, bold=True)
ll = LL(f)
A = [('a0', 1), ('a1', 3), ('a2', 5)]; B = [('b0', 2), ('b1', 4)]
for k, (i, v) in enumerate(A): ll.add(i, v, .2 + k * .1, X0 + k * P_, YA)
for k, (i, v) in enumerate(B): ll.add(i, v, .4 + k * .1, X0 + k * P_, YB)
ea = {'a0': 'a1', 'a1': 'a2'}; eb = {'b0': 'b1'}; er = {}
def E(): return list(ea.items()) + list(eb.items()) + list(er.items())
ll.links(0, .8, E())
goal_corner(f, f.X0, 'one sorted list', 1.0, y=YR + 70)
f.line(1.6, 0)
ll.add('D', 'D', 1.8, X0 - 14, YR)
tp = NP(ll, 'tail', 'below', 16).at(2.2, 'D')
ap = NP(ll, 'a', 'above', 14).at(2.2, 'a0'); bp = NP(ll, 'b', 'above', 14).at(2.2, 'b0')
qa, qb = [i for i, _ in A], [i for i, _ in B]; tail = 'D'; slot = 1; t = 3.0; SY = YR + 98
while qa and qb:
    f.line(t, 1); f.line(t + .3, 2)
    a_, b_ = qa[0], qb[0]
    f.show(ring(*ll.pos[a_], NW, NH), t + .3, hide=t + 1.4); f.show(ring(*ll.pos[b_], NW, NH), t + .3, hide=t + 1.4)
    useA = ll.val[a_] <= ll.val[b_]
    f.line(t + .8, 3 if useA else 5)
    take = a_ if useA else b_
    status(f, f.X0, SY + 20, '%d %s %d → take %d' % (ll.val[a_], '≤' if useA else '>', ll.val[b_], ll.val[take]), t + .3, hide=t + 2.6)
    src = ea if useA else eb
    q = qa if useA else qb; q.pop(0)
    src.pop(take, None)
    if q: (ap if useA else bp).at(t + 1.2, q[0])
    else: (ap if useA else bp).die(t + 1.2)
    ll.move(take, t + 1.2, X0 - 14 + slot * P_, YR)
    er[tail] = take
    ll.links(t + 1.2, t + 1.9, E(), hot=[(tail, take)])
    f.line(t + 2.0, 6)
    tp.at(t + 2.1, take); tail = take; slot += 1
    t += 2.8
f.line(t, 7)
rest = qa or qb
status(f, f.X0, SY + 20, 'b is empty → tail.next = a (5): no loop needed', t, hide=t + 1.8)
for k, i in enumerate(rest): ll.move(i, t + .3, X0 - 14 + (slot + k) * P_, YR)
er[tail] = rest[0]
for i in rest: ea.pop(i, None)
(ap if qa else bp).die(t + .3)
ll.links(t + .3, t + 1.0, E(), hot=[(tail, rest[0])])
t += 1.8
f.line(t, 8)
tp.die(t)
ll.links(t, t, E())
ll.tone('D', t, 'g')
for i in ['a0', 'b0', 'a1', 'b1', 'a2']: ll.tone(i, t + .2, 'f')
f.show(ab_lbl, 0, hide=t)
finish(f, f.X0, SY + 20, 'dummy.next → 1 2 3 4 5 · no special case for the first node', t + .4)
ll.flush()
figs['q1'] = f.render(SY + 32)

# ---------------------------------------------------------------- q2 middle
L6 = ['slow = fast = head', 'while fast and fast.next:', '    slow, fast = slow.next, fast.next.next', 'return slow']
f = Fig('ll-q2-', 'Five nodes 1 to 5. slow moves one node per step, fast moves two. After two steps fast is on the last node and slow is on 3, the middle.',
        'FAST AND SLOW · fast MOVES 2, slow MOVES 1', L6, W=800, cw=320)
X0 = f.X0 + 10; Y = 96; P_ = 80
ll = LL(f)
for k in range(5): ll.add(k, k + 1, .2 + k * .1, X0 + k * P_, Y)
ll.add('N', None, .2, X0 + 5 * P_, Y, kind='none')
ll.links(0, .8, chain([0, 1, 2, 3, 4, 'N']))
goal_corner(f, f.X0, 'find the middle', 1.0)
f.line(1.6, 0)
sp = NP(ll, 'slow', 'above', 18).at(1.8, 0); fp = NP(ll, 'fast', 'below', 16).at(1.8, 0)
s_, q_ = 0, 0; t = 2.8; SY = Y + 108
while q_ + 2 <= 4 + 1 and q_ + 1 <= 4:
    f.line(t, 1); f.line(t + .4, 2)
    s_ += 1; q_ += 2
    sp.at(t + .6, s_); fp.at(t + .6, q_)
    status(f, f.X0, SY, 'slow → %d · fast → %d' % (s_ + 1, q_ + 1), t + .6, hide=t + 2.0)
    t += 2.2
f.line(t, 1)
f.show(ring(*ll.pos[q_], NW, NH), t, hide=t + 1.2)
status(f, f.X0, SY, 'fast.next is None → stop', t, hide=t + 1.4)
f.line(t + 1.4, 3)
fp.die(t + 1.4)
ll.tone(s_, t + 1.5, 'f')
f.show(T(ll.pos[s_][0] + NV / 2, Y + NH + 30, '✓ middle', TG, mono=True, bold=True), t + 1.6)
finish(f, f.X0, SY, 'middle = 3 · one pass · fast covers the list while slow covers half', t + 1.8)
ll.flush()
figs['q2'] = f.render(SY + 12)

# ---------------------------------------------------------------- q3 cycle
L7 = ['slow = fast = head', 'while fast and fast.next:', '    slow, fast = slow.next, fast.next.next', '    if slow is fast: return True', 'return False']
f = Fig('ll-q3-', 'Six nodes 1 to 6 where 6 points back to 3, a cycle. slow moves one, fast moves two; fast enters the loop and laps around. After four steps both stand on node 5: they met, so there is a cycle.',
        'CYCLE · IF fast EVER MEETS slow, THERE IS A LOOP', L7, W=820, cw=320)
X0 = f.X0 + 10; Y = 120; P_ = 74
ll = LL(f)
for k in range(6): ll.add(k, k + 1, .2 + k * .1, X0 + k * P_, Y)
ll.links(0, .8, chain([0, 1, 2, 3, 4, 5]) + [(5, 2)])
goal_corner(f, f.X0, 'is there a loop?', 1.0)
f.line(1.6, 0)
sp = NP(ll, 'slow', 'above', 14, -8).at(1.8, 0); fp = NP(ll, 'fast', 'below', 16).at(1.8, 0)
nxt = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 2}
s_, q_ = 0, 0; t = 2.8; SY = Y + 100
while True:
    f.line(t, 1); f.line(t + .4, 2)
    s_ = nxt[s_]; q1 = nxt[q_]; q_ = nxt[q1]
    sp.at(t + .6, s_)
    fp.at(t + .6, q1); fp.at(t + 1.1, q_)
    status(f, f.X0, SY, 'slow → %d · fast → %d → %d' % (s_ + 1, q1 + 1, q_ + 1), t + .6, hide=t + 2.2)
    f.line(t + 1.7, 3)
    if s_ == q_: break
    t += 2.4
f.show(ring(*ll.pos[s_], NW, NH), t + 1.9, hide=t + 2.6)
sp.die(t + 2.6); fp.die(t + 2.6)
ll.tone(s_, t + 2.6, 'f')
f.show(T(ll.pos[s_][0] + NV / 2, Y + NH + 30, '✓ met', TG, mono=True, bold=True), t + 2.8)
finish(f, f.X0, SY, 'slow is fast at node 5 → cycle · O(n) time, O(1) memory', t + 2.9)
ll.flush()
figs['q3'] = f.render(SY + 12)

# ---------------------------------------------------------------- q4 gap of n
L8 = ['fast = slow = dummy', 'for _ in range(n + 1): fast = fast.next', 'while fast:', '    fast, slow = fast.next, slow.next', 'slow.next = slow.next.next']
f = Fig('ll-q4-', 'Remove the 2nd node from the end of 1 2 3 4 5. Start at a dummy node. fast runs 3 nodes ahead; then both move together until fast falls off the end. slow stops on 3, just before 4; 3 is re-pointed to 5 and 4 drops out.',
        'TWO POINTERS A FIXED GAP APART · REMOVE THE n-TH FROM THE END', L8, W=860, cw=346)
X0 = f.X0 + 10; Y = 100; P_ = 70
ll = LL(f)
ll.add('D', 'D', .2, X0, Y)
for k in range(1, 6): ll.add(k, k, .2 + k * .1, X0 + k * P_, Y)
ll.add('N', None, .2, X0 + 6 * P_, Y, kind='none')
ll.links(0, .8, chain(['D', 1, 2, 3, 4, 5, 'N']))
goal_on(f, X0 + 4 * P_, Y, 'n = 2 from the end', 1.0, f.X0, 24, w=NW, h=NH, keep_ring=False)
f.line(2.8, 0)
sp = NP(ll, 'slow', 'above', 14).at(3.0, 'D'); fp = NP(ll, 'fast', 'below', 16).at(3.0, 'D')
order = ['D', 1, 2, 3, 4, 5, 'N']; qi = 0; si = 0; t = 3.8; SY = Y + 100
f.line(t, 1)
for k in range(3):
    qi += 1; fp.at(t + .2 + k * .7, order[qi])
status(f, f.X0, SY, 'fast runs n + 1 = 3 ahead → gap of 3', t + .2, hide=t + 2.6)
t += 2.8
while order[qi] != 'N':
    f.line(t, 2); f.line(t + .3, 3)
    qi += 1; si += 1
    fp.at(t + .5, order[qi]); sp.at(t + .5, order[si])
    status(f, f.X0, SY, 'both step · fast → %s · slow → %s' % ('None' if order[qi] == 'N' else order[qi], order[si]), t + .5, hide=t + 1.7)
    t += 1.9
f.line(t, 2)
status(f, f.X0, SY, 'fast is None → slow sits just before the target', t, hide=t + 1.8)
fp.die(t + .2)
f.line(t + 1.8, 4)
ll.links(t + 2.0, t + 2.0, [('D', 1), (1, 2), (2, 3), (3, 5), (4, 5), (5, 'N')], hot=[(3, 5)])
ll.tone(4, t + 2.6, 'g'); f.show(goalring(X0 + 4 * P_, Y, NW, NH), 1.0, hide=t + 2.6)
ll.move(4, t + 3.2, X0 + 4 * P_, Y + 66)
ll.links(t + 3.2, t + 3.8, [('D', 1), (1, 2), (2, 3), (3, 5), (5, 'N')], hot=[(3, 5)])
ll.die(4, t + 4.0)
sp.die(t + 4.0)
ll.move(5, t + 4.0, X0 + 4 * P_, Y); ll.move('N', t + 4.0, X0 + 5 * P_, Y)
ll.links(t + 4.0, t + 4.6, [('D', 1), (1, 2), (2, 3), (3, 5), (5, 'N')])
for i in (1, 2, 3, 5): ll.tone(i, t + 4.2, 'f')
finish(f, f.X0, SY, '1 → 2 → 3 → 5 · one pass, the gap does the counting', t + 4.4)
ll.flush()
figs['q4'] = f.render(SY + 12)

# ---------------------------------------------------------------- q5 reorder
L9 = ['mid = middle(head)          # fast & slow', 'b = reverse(mid.next)       # 2.4', 'mid.next = None', 'a = head', 'while b:', '    a.next, b.next, a, b = b, a.next, a.next, b.next']
f = Fig('ll-q5-', 'Reorder 1 2 3 4 5 into 1 5 2 4 3. Find the middle 3, cut after it, reverse the second half 4 5 into 5 4 on a second row, then weave: 5 slides in after 1, 4 after 2.',
        'COMBINE THE TOOLS · MIDDLE, REVERSE, WEAVE', L9, W=900, cw=420)
X0 = f.X0 + 10; YA, YB = 96, 186; P_ = 78
ll = LL(f)
for k in range(1, 6): ll.add(k, k, .2 + k * .1, X0 + (k - 1) * P_, YA)
ll.add('N', None, .2, X0 + 5 * P_, YA, kind='none')
ll.links(0, .8, chain([1, 2, 3, 4, 5, 'N']))
goal_corner(f, f.X0, 'L0 Ln L1 Ln-1 …', 1.0)
f.line(1.8, 0)
mp = NP(ll, 'mid', 'above', 14)
mp.at(2.6, 3)
f.show(ring(*ll.pos[3], NW, NH), 2.6, hide=3.6)
status(f, f.X0, YB + 92, 'middle = 3 (fast & slow, 3.2)', 2.4, hide=3.8)
t = 4.0
f.line(t, 1)
ll.move(5, t + .3, X0 + 0 * P_ + P_ * 1 - P_, YB); ll.move(4, t + .3, X0 + 1 * P_, YB)
ll.move('N', t + .3, X0 + 2 * P_, YB)
f.line(t + 1.4, 2)
ll.add('N2', None, t + 1.4, X0 + 3 * P_, YA, kind='none')
ll.links(t + .3, t + 1.0, [(1, 2), (2, 3), (5, 4), (4, 'N')], hot=[(5, 4)])
ll.links(t + 1.4, t + 1.5, [(1, 2), (2, 3), (3, 'N2'), (5, 4), (4, 'N')], hot=[(3, 'N2')])
ab2 = T(X0 - 14, YA + 23, 'a', MU, 'end', mono=True, bold=True) + T(X0 - 14, YB + 23, 'b', MU, 'end', mono=True, bold=True)
status(f, f.X0, YB + 92, 'second half reversed: 5 4 · first half cut after 3', t + .5, hide=t + 2.4)
mp.die(t + 1.6)
t += 2.6
f.line(t, 3); f.line(t + .3, 4)
# weave: final row YA: 1 5 2 4 3
final = [1, 5, 2, 4, 3]
ll.move(2, t + .5, X0 + 2 * P_, YA); ll.move(3, t + .5, X0 + 4 * P_, YA); ll.move('N2', t + .5, X0 + 5 * P_, YA)
ll.links(t + .5, t + 1.1, [(1, 2), (2, 3), (3, 'N2'), (5, 4), (4, 'N')])
f.line(t + 1.4, 5)
ll.move(5, t + 1.6, X0 + 1 * P_, YA)
ll.links(t + 1.6, t + 2.2, [(1, 5), (5, 2), (2, 3), (3, 'N2'), (4, 'N')], hot=[(1, 5), (5, 2)])
status(f, f.X0, YB + 92, '5 goes between 1 and 2', t + 1.6, hide=t + 3.0)
t += 3.0
f.line(t, 4); f.line(t + .3, 5)
ll.move(4, t + .5, X0 + 3 * P_, YA)
ll.die('N', t + .5)
ll.links(t + .5, t + 1.1, [(1, 5), (5, 2), (2, 4), (4, 3), (3, 'N2')], hot=[(2, 4), (4, 3)])
status(f, f.X0, YB + 92, '4 goes between 2 and 3', t + .5, hide=t + 1.9)
t += 2.0
f.line(t, 4)
ll.links(t, t, [(1, 5), (5, 2), (2, 4), (4, 3), (3, 'N2')])
for i in final: ll.tone(i, t + .2, 'f')
f.show(ab2, 4.6, hide=t)
finish(f, f.X0, YB + 92, '1 → 5 → 2 → 4 → 3 · three O(n) passes, O(1) memory', t + .4)
ll.flush()
figs['q5'] = f.render(YB + 104)

# ---------------------------------------------------------------- q6 LRU
L10 = ['def get(k):', '    node = map[k]           # O(1) find', '    move_to_front(node)     # O(1) relink', 'def put(k, v):', '    map[k] = push_front(Node(k, v))', '    if len(map) > cap:', '        del map[pop_back().key]']
f = Fig('ll-q6-', 'LRU cache with capacity 3: a hash map of keys points into a doubly linked list ordered from most to least recent: 3, 2, 1. get(1) finds node 1 through the map and moves it to the front: 1 3 2. put(4) adds 4 at the front; the list is over capacity, so the tail node 2 is dropped and its key deleted. Final 4 1 3.',
        'HASH MAP + DOUBLY LINKED LIST · LRU CACHE, CAPACITY 3', L10, W=860, cw=330)
MX = f.X0 + 4; X0 = f.X0 + 110; Y = 120; P_ = 100
ll = LL(f)
f.static(T(MX + 22, Y - 52, 'map', FA, 'middle', cls='sv-s') + T(X0, Y - 52, 'most recent', FA, 'start', cls='sv-s') + T(X0 + 3 * P_ - 40, Y - 52, 'least recent', FA, 'end', cls='sv-s'))
keys = {}
def key_box(k, t, row, tone='u'):
    keys[k] = Box(f, t, MX, Y - 34 + row * 30, 'k=%d' % k, w=44, h=24, tone=tone); return keys[k]
for r_, k in enumerate([1, 2, 3]): key_box(k, .3 + r_ * .1, r_)
for k, n_ in enumerate([3, 2, 1]): ll.add(n_, n_, .3 + k * .1, X0 + k * P_, Y)
order = [3, 2, 1]
ll.links(0, .8, chain(order), kind='dbl')
f.line(1.4, 0)
goal_corner(f, f.X0, 'get(1), then put(4)', 1.2)
t = 2.0; SY = Y + 96
f.line(t, 1)
keys[1].tone(t, 'v')
kx, ky = MX + 44, Y - 34 + 12
nx, ny = ll.pos[1]
f.show(L(kx, ky, nx, ny + 4, MID, 1.4, '4 3'), t + .3, hide=t + 2.0)
f.show(ring(nx, ny, NW, NH), t + .4, hide=t + 2.0)
status(f, f.X0, SY + 46, 'map[1] → node 1 at once, no walking', t + .3, hide=t + 2.0)
keys[1].tone(t + 2.0, 'u')
f.line(t + 2.0, 2)
order = [1, 3, 2]
ll.move(1, t + 2.2, X0, Y); ll.move(3, t + 2.2, X0 + P_, Y); ll.move(2, t + 2.2, X0 + 2 * P_, Y)
ll.links(t + 2.2, t + 2.9, chain(order), hot=[(1, 3)], kind='dbl')
status(f, f.X0, SY + 46, 'unlink 1, push it to the front → 1 3 2', t + 2.4, hide=t + 4.0)
t += 4.2
f.line(t, 3); f.line(t + .3, 4)
ll.move(1, t + .5, X0 + P_, Y); ll.move(3, t + .5, X0 + 2 * P_, Y); ll.move(2, t + .5, X0 + 3 * P_, Y)
ll.links(t + .5, t + 1.1, chain([1, 3, 2]), kind='dbl')
ll.add(4, 4, t + 1.2, X0, Y)
key_box(4, t + 1.2, 3)
ll.links(t + 1.2, t + 1.4, chain([4, 1, 3, 2]), hot=[(4, 1)], kind='dbl')
status(f, f.X0, SY + 46, 'push 4 at the front · map[4] added · size 4 > 3', t + 1.3, hide=t + 3.0)
f.line(t + 2.6, 5); f.line(t + 3.0, 6)
f.show(ring(*ll.pos[2], NW, NH), t + 3.0, hide=t + 3.8)
ll.tone(2, t + 3.4, 'g'); keys[2].tone(t + 3.4, 'g')
status(f, f.X0, SY + 46, 'evict the tail: node 2 and map[2]', t + 3.2, hide=t + 4.8)
ll.links(t + 3.8, t + 3.8, chain([4, 1, 3]), kind='dbl')
ll.move(2, t + 3.9, X0 + 3 * P_, Y + 50)
ll.die(2, t + 4.6); keys[2].die(t + 4.6)
keys[3].move(t + 4.7, MX, Y - 34 + 30); keys[4].move(t + 4.7, MX, Y - 34 + 60)
t += 5.0
ll.links(t, t, chain([4, 1, 3]), kind='dbl')
for i in (4, 1, 3): ll.tone(i, t, 'f')
finish(f, f.X0, SY + 46, 'cache = 4 1 3 · get and put are both O(1)', t + .2)
ll.flush()
figs['q6'] = f.render(SY + 58)

dump('linked-list', figs)
