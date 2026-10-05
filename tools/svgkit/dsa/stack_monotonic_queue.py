"""Figures for content/01-dsa/03-data-structures/stack-monotonic-queue (visual-first DSA lesson).
Writes /tmp/dsa/stack-monotonic-queue.json  {figure key: <figure> html}."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *

PT, MID, TG = 'var(--brand)', 'var(--violet)', 'var(--filled)'
def vt(a): return 'rgba(var(--violet-a),%s)' % a
def it(a): return 'rgba(var(--blue-a),%s)' % a
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
LH = 20
CW, CH, G = 42, 36, 6

class Code2:
    def __init__(s, x, y, lines, w=None):
        s.x, s.y, s.lines = x, y, lines
        s.w = w or max(300, 28 + max(len(l) for l in lines) * 6.7)
    def svg(s):
        o = R(s.x, s.y, s.w, len(s.lines) * LH + 14, 'var(--bg)', RULE_HI, 8)
        for i, l in enumerate(s.lines):
            n = len(l) - len(l.lstrip())
            o += T(s.x + 14, s.y + 22 + i * LH, esc(l).replace(' ', '\u00a0'), TX, 'start', mono=True)
        return o
    def bar(s): return R(s.x + 4, s.y + 8, s.w - 8, LH, vt('.13'), 'none', 4) + R(s.x + 4, s.y + 8, 3, LH, MID, 'none', 1.5)
    def h(s): return len(s.lines) * LH + 14

class Bar:
    """the violet running-line bar; call at(t, line) in time order, then emit(f)."""
    def __init__(s, code): s.code, s.pts = code, [(0, 0, 0)]
    def at(s, t, i): s.pts.append((t, 0, i * LH))
    def emit(s, f): f.path(s.code.bar(), s.pts, 0, appear=False, d=.3)

def box(x, y, v, kind='n', w=CW, h=CH, sub=None):
    """n plain · g discarded · f answer (solid) · t written result (tinted)"""
    fill, st, c, sw = {'n': ('var(--bg)', RULE_HI, TX, 1.2), 'g': ('var(--sunk)', 'var(--rule)', 'var(--ghost)', 1),
                       'f': (TG, TG, 'var(--on-fill)', 1.2), 't': (it('.12'), TG, TG, 1.3)}[kind]
    o = R(x, y, w, h, fill, st, 6, sw) + T(x + w / 2, y + h / 2 + 5, esc(v), c, mono=True, bold=kind != 'g')
    if sub is not None: o += T(x + w / 2, y + h + 15, esc(sub), FA, cls='sv-s', mono=True)
    return o

def ring(x, y, w=CW, h=CH): return R(x - 3, y - 3, w + 6, h + 6, vt('.10'), MID, 8, 2.2)
def ptr_up(cx, y, name, ln=14):   # pointer under a cell: arrow pointing up at y
    return arrow(cx, y + ln, cx, y, PT, 1.6, None, 6) + T(cx, y + ln + 13, name, PT, mono=True, bold=True)
def say(f, x, y, txt, t, hide=None, c=TX, bold=False, a='start'):
    f.show(T(x, y, esc(txt), c, a, mono=True, bold=bold), t, hide=hide)
def chip(x, y, txt):
    w = 24 + len(txt) * 7
    return R(x, y, w, 24, it('.12'), TG, 12, 1.3) + T(x + w / 2, y + 16, esc(txt), TG, mono=True, bold=True)

class Track:
    """things that are born, slide between positions and die (stack cells, deque cells…)."""
    def __init__(s): s.its = []
    def add(s, fn, pos, t, frm=None):
        s.its.append(dict(fn=fn, base=pos, t0=t, mv=[], die=None, frm=frm)); return len(s.its) - 1
    def move(s, k, pos, t): s.its[k]['mv'].append((t, pos))
    def kill(s, k, t): s.its[k]['die'] = t
    def emit(s, f, d=.45):
        for i in s.its:
            bx, by = i['base']
            if i['frm']:
                pts = [(0, i['frm'][0] - bx, i['frm'][1] - by), (i['t0'] + .3, 0, 0)]
            else:
                pts = [(0, 0, 0)]
            pts += [(t, x - bx, y - by) for t, (x, y) in i['mv']]
            f.path(i['fn'](bx, by), pts, i['t0'], hide=i['die'], d=d)

figs = {}

# ---------------------------------------------------------------- vertical stack helpers
VW, VH, VG = 56, 30, 4
def vy(yb, k): return yb - (k + 1) * (VH + VG)
def vcell(x, yb, k, v, kind='n'):
    y = vy(yb, k)
    fill, st, c = {'n': ('var(--bg)', RULE_HI, TX), 'g': ('var(--sunk)', 'var(--rule)', 'var(--ghost)'),
                   'f': (TG, TG, 'var(--on-fill)')}[kind]
    return R(x, y, VW, VH, fill, st, 5, 1.2) + T(x + VW / 2, y + VH / 2 + 5, esc(v), c, mono=True, bold=kind != 'g')
def vring(x, yb, k): y = vy(yb, k); return R(x - 3, y - 3, VW + 6, VH + 6, vt('.10'), MID, 7, 2.2)
def cup(x, yb, n):
    top = vy(yb, n - 1) - 10
    return ('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f" fill="none" stroke="%s" stroke-width="1.6" '
            'stroke-linejoin="round"/>' % (x - 6, top, x - 6, yb + 2, x + VW + 6, yb + 2, x + VW + 6, top, MU))
def topptr(x, yb, k, name='top'):
    y = vy(yb, k) + VH / 2
    return arrow(x + VW + 46, y, x + VW + 10, y, PT, 1.6, None, 6) + T(x + VW + 50, y + 4, name, PT, 'start', mono=True, bold=True)

# ---------------------------------------------------------------- m1 · last in, first out
LS = ['st = []', 'st.append(3)', 'st.append(8)', 'st.append(5)', 'st.pop()   # → 5', 'st[-1]     # → 8']
code = Code2(0, 40, LS); X0 = code.w + 60; YB = 250; SX = X0 + 190
f = Anim('stk-m1-', 760, 0, 'A stack drawn as an open box. 3, 8 and 5 are pushed on top of each other; pop takes 5, the last one in; st[-1] reads 8 without removing it. The top pointer moves with every push and pop, and the running code line follows.',
         'A STACK · ONLY THE TOP IS EVER TOUCHED', 3)
f.static(code.svg()); bar = Bar(code); tr = Track()
f.show(cup(X0, YB, 4) + T(X0 + VW / 2, YB + 22, 'st', MU, mono=True), .3)
say(f, SX, 70, 'st = []  · size 0', .6, hide=1.6, c=PT)
t = 1.6; tp = None; vals = [3, 8, 5]; ks = []
for k, v in enumerate(vals):
    bar.at(t, k + 1)
    ks.append(tr.add(lambda x, y, v=v, k=k: vcell(X0, YB, k, v), (0, 0), t + .2, frm=(0, -50)))
    if tp is None:
        tp = tr.add(lambda x, y: topptr(X0, YB, 0), (0, 0), t + .6)
    else:
        tr.move(tp, (0, vy(YB, k) - vy(YB, 0)), t + .6)
    say(f, SX, 70, 'push %d · size %d' % (v, k + 1), t + .2, hide=t + 1.4, c=PT)
    t += 1.5
# pop
bar.at(t, 4)
f.show(vring(X0, YB, 2), t + .3, hide=t + 1.6)
say(f, SX, 70, 'pop() → 5', t + .3, hide=t + 2.2, c=MID)
say(f, SX, 92, 'last in, first out', t + .3, hide=t + 2.2)
tr.move(ks[2], (0, -50), t + 1.6); tr.kill(ks[2], t + 1.9)
tr.move(tp, (0, vy(YB, 1) - vy(YB, 0)), t + 1.9)
t += 2.6
bar.at(t, 5)
f.show(vring(X0, YB, 1), t + .3, hide=t + 2.0)
say(f, SX, 70, 'st[-1] → 8', t + .3, hide=t + 2.0, c=MID)
say(f, SX, 92, 'read only · nothing moves', t + .3, hide=t + 2.0)
t += 2.2
tr.emit(f); bar.emit(f)
f.show(vcell(X0, YB, 1, 8, 'f'), t)
f.show(T(X0 + VW / 2, vy(YB, 1) - 10, '✓ top', TG, mono=True, bold=True), t + .2)
f.show(T(SX, 70, 'push and pop both happen at the top', TG, 'start', bold=True), t + .3)
f.h = YB + 34
figs['m1'] = f.render()

# ---------------------------------------------------------------- monotonic run (m2, q2)
def mono(pre, caption, aria, a, lines, LI, ans=False, hint=''):
    code = Code2(0, 40, lines); X0 = code.w + 26
    n = len(a); cx = lambda i: X0 + i * (CW + G) + CW / 2; AY = 60
    SYK = AY + 92                      # stack row y
    ANY = SYK + 80 if ans else None    # ans row y
    STY = (ANY if ans else SYK) + 78   # status y
    W = max(760, X0 + n * (CW + G) + 10)
    f = Anim(pre, W, 0, aria, caption, 3); f.static(code.svg()); bar = Bar(code); tr = Track()
    for i, v in enumerate(a): f.show(box(X0 + i * (CW + G), AY, v, sub=i), .2 + i * .05)
    f.show(T(X0, SYK - 10, 'stack · bottom → top', MU, 'start'), .7)
    f.show(L(X0, SYK + CH + 4, X0 + n * (CW + G) - G, SYK + CH + 4, 'var(--rule)', 1, '3 3'), .7)
    if ans:
        f.show(T(X0, ANY - 8, 'ans', MU, 'start', mono=True), .9)
        for i in range(n): f.show(R(X0 + i * (CW + G), ANY, CW, CH, 'var(--bg)', RULE_HI, 6, 1.2) + T(X0 + i * (CW + G) + CW / 2, ANY + 23, '0', FA, mono=True), .9 + i * .03)
    f.show(T(X0 + n * (CW + G) - G, AY - 14, hint, MU, 'end'), 1.0)
    bar.at(1.4, 0)
    t = 2.2; st = []; ip = None; cnt = dict(push=0, pop=0)
    def sx(k): return X0 + k * (CW + G)
    for i, v in enumerate(a):
        bar.at(t, LI['for'])
        if ip is None: ip = tr.add(lambda x, y: ptr_up(cx(0), AY + CH + 20, 'i'), (0, 0), t)
        else: tr.move(ip, (i * (CW + G), 0), t)
        say(f, X0, STY, 'i = %d · a[i] = %d' % (i, v), t, hide=t + .9, c=PT)
        t += 1.0
        while True:
            if not st:
                say(f, X0, STY, 'stack empty → push', t, hide=t + .8); bar.at(t, LI['while']); t += .9; break
            j, kid = st[-1]
            bar.at(t, LI['while'])
            f.show(ring(sx(len(st) - 1), SYK), t, hide=t + 1.05)
            pop = a[j] < v
            say(f, X0, STY, ('a[%d] = %d < %d → pop' if pop else 'a[%d] = %d ≥ %d → stop') % (j, a[j], v), t, hide=t + 1.05)
            if not pop: t += 1.2; break
            bar.at(t + .55, LI['pop']); tr.kill(kid, t + .7); st.pop(); cnt['pop'] += 1
            if ans:
                bar.at(t + .95, LI['ans'])
                f.show(R(sx(j), ANY, CW, CH, 'var(--bg)', 'none', 6) + box(sx(j), ANY, i - j, 't'), t + 1.0)
                f.show(T(X0, STY + 22, 'ans[%d] = %d - %d = %d' % (j, i, j, i - j), TG, 'start', mono=True), t + 1.0, hide=t + 1.6)
                t += .5
            t += 1.25
        bar.at(t, LI['push'])
        k = len(st)
        kid = tr.add(lambda x, y, v=v, i=i: box(x, y, v, sub=i), (sx(k), SYK), t, frm=(sx(i), AY))
        st.append((i, kid)); cnt['push'] += 1
        t += 1.0
    tr.emit(f); bar.emit(f)
    return f, X0, SYK, STY, st, cnt, t, sx

m2 = [5, 3, 4, 1, 2, 6]
f, X0, SYK, STY, st, cnt, t, sx = mono('stk-m2-', 'MONOTONIC STACK · A BIGGER VALUE POPS EVERY SMALLER ONE ON TOP',
    'Array 5 3 4 1 2 6 is read left to right. Each new value pops every smaller value from the top of the stack, then is pushed. 4 pops 3, 2 pops 1, and 6 pops 2, 4 and 5. The stack always stays decreasing from bottom to top.',
    m2, ['st = []', 'for i in range(len(a)):', '    while st and a[st[-1]] < a[i]:', '        st.pop()', '    st.append(i)'],
    dict(push=4, pop=3, **{'for': 1, 'while': 2}), hint='keep the stack decreasing')
f.show(R(sx(0), SYK, CW, CH, 'var(--bg)', 'none', 6) + box(sx(0), SYK, 6, 'f'), t)
f.show(T(X0, STY, '✓ stack stays decreasing · %d pushes + %d pops for %d values' % (cnt['push'], cnt['pop'], len(m2)), TG, 'start', bold=True), t + .2)
f.h = STY + 28
figs['m2'] = f.render()

# ---------------------------------------------------------------- p1–p3 · push / pop / peek on two sizes
def ops_fig(op):
    line = {'push': 'st.append(9)', 'pop': 'x = st.pop()', 'peek': 'x = st[-1]'}[op]
    code = Code2(0, 40, [line], 230); X0 = 330
    small, big = [4, 7], [4, 7, 1, 9, 2, 6]
    YB = 300; xs = [X0, X0 + 230]
    LIFT = vy(YB, 6) - 14 - VH   # y of a cell lifted above the cup
    cap_, aria = {
        'push': ('PUSH · ONE NEW CELL ON TOP, WHATEVER THE SIZE', 'Two stacks, size 2 and size 6. Pushing 9 drops one cell on top of each and moves the top pointer up by one: one step at both sizes, O(1).'),
        'pop': ('POP · TAKE THE TOP CELL OFF, WHATEVER THE SIZE', 'Two stacks, size 2 and size 6. pop lifts the top cell off each, returns 7 and 6, and moves the top pointer down by one: one step at both sizes, O(1).'),
        'peek': ('PEEK · READ THE TOP CELL, LEAVE IT THERE', 'Two stacks, size 2 and size 6. st[-1] reads the top cell, 7 and 6, and leaves both stacks unchanged: one step at both sizes, O(1).')}[op]
    f = Anim('stk-p%d-' % {'push': 1, 'pop': 2, 'peek': 3}[op], 760, 0, aria, cap_, 3)
    f.static(code.svg()); tr = Track()
    for s_, (x, vals) in enumerate(zip(xs, (small, big))):
        f.show(cup(x, YB, 6) + T(x + VW / 2, YB + 20, 'size %d' % len(vals), MU), .2 + s_ * .3)
        for k, v in enumerate(vals):
            if op == 'pop' and k == len(vals) - 1: continue
            f.show(vcell(x, YB, k, v), .3 + s_ * .3 + k * .06)
    f.show(chip(0, 120, {'push': 'push 9', 'pop': 'pop()', 'peek': 'st[-1]'}[op]), 1.0)
    f.show(code.bar(), 2.0)
    t = 2.6
    for s_, (x, vals) in enumerate(zip(xs, (small, big))):
        k = len(vals) - 1
        p = tr.add(lambda x_, y_, x=x, k=k: topptr(x, YB, k), (0, 0), 1.4)
        if op == 'push':
            tr.add(lambda x_, y_, x=x, k=k: vcell(x, YB, k + 1, 9), (0, 0), t, frm=(0, LIFT - vy(YB, k + 1)))
            tr.move(p, (0, -(VH + VG)), t + .7)
            f.show(vring(x, YB, k + 1), t + .5, hide=t + 2.0)
        elif op == 'pop':
            c = tr.add(lambda x_, y_, x=x, k=k, v=vals[k]: vcell(x, YB, k, v), (0, 0), .3 + s_ * .3 + k * .06)
            f.show(vring(x, YB, k), t, hide=t + .9)
            tr.move(c, (0, LIFT - vy(YB, k)), t + 1.0)
            tr.move(p, (0, VH + VG), t + 1.2)
        else:
            f.show(vring(x, YB, k), t, hide=t + 1.6)
        f.show(T(x + VW / 2, YB + 38, '1 step', MID, mono=True, bold=True), t + .9)
    tr.emit(f)
    t += 2.3
    for x, vals in zip(xs, (small, big)):
        k = len(vals) - 1
        if op == 'push': f.show(vcell(x, YB, k + 1, 9, 'f'), t)
        elif op == 'pop':
            f.show(R(x, LIFT, VW, VH, TG, TG, 5, 1.2) + T(x + VW / 2, LIFT + VH / 2 + 5, str(vals[k]), 'var(--on-fill)', mono=True, bold=True), t)
            f.show(T(x - 10, LIFT + VH / 2 + 5, 'x =', TG, 'end', mono=True, bold=True), t + .1)
        else: f.show(vcell(x, YB, k, vals[k], 'f'), t)
    msg = {'push': '✓ pushed', 'pop': '✓ returned 7 and 6', 'peek': '✓ read 7 and 6 · nothing moved'}[op]
    f.show(T(0, 190, msg, TG, 'start', mono=True, bold=True), t + .2)
    f.show(T(0, 212, 'same 1 step at size 2 and size 6', TG, 'start', bold=True), t + .3)
    f.show(T(0, 240, 'O(1)', TG, 'start', mono=True, bold=True), t + .4)
    f.h = YB + 66
    return f.render()
figs['p1'] = ops_fig('push')
figs['p2'] = ops_fig('pop')
figs['p3'] = ops_fig('peek')

# ---------------------------------------------------------------- p4 · search
def search_fig():
    LS = ['for i in range(len(st) - 1, -1, -1):', '    if st[i] == t: return i', 'return -1']
    code = Code2(0, 40, LS); X0 = code.w + 60
    vals = [4, 7, 1, 9, 2, 6]; target = 7; ans = vals.index(target)
    YB = 270; SX = X0 + 170
    f = Anim('stk-p4-', 760, 0, 'Stack 4 7 1 9 2 6, target 7 near the bottom. Only the top is reachable, so i walks down from the top: 6, 2, 9, 1 are checked and grey out; 7 is found after 5 checks. Search is O(n).',
             'SEARCH · WALK DOWN FROM THE TOP, ONE CELL AT A TIME', 3)
    f.static(code.svg()); bar = Bar(code); tr = Track()
    f.show(cup(X0, YB, 6), .2)
    for k, v in enumerate(vals): f.show(vcell(X0, YB, k, v) + T(X0 - 14, vy(YB, k) + VH / 2 + 4, str(k), FA, 'end', cls='sv-s', mono=True), .3 + k * .06)
    f.show(R(X0 - 4, vy(YB, ans) - 4, VW + 8, VH + 8, 'none', TG, 7, 1.4, '4 3'), 1.0)
    f.path(chip(X0 + VW + 14, vy(YB, ans) + 3, 'target = 7'), [(0, 0, 0), (2.2, SX - (X0 + VW + 14), 26 - (vy(YB, ans) + 3))], 1.0)
    t = 3.2; ip = None; steps = 0
    for k in range(len(vals) - 1, -1, -1):
        steps += 1
        bar.at(t, 0)
        if ip is None: ip = tr.add(lambda x, y: topptr(X0, YB, len(vals) - 1, 'i'), (0, 0), t)
        else: tr.move(ip, (0, vy(YB, k) - vy(YB, len(vals) - 1)), t)
        say(f, SX, 90, 'i = %d' % k, t, hide=t + 1.7, c=PT)
        bar.at(t + .6, 1)
        f.show(vring(X0, YB, k), t + .6, hide=t + 1.7)
        hit = vals[k] == target
        say(f, SX, 112, 'st[%d] = %d %s 7%s' % (k, vals[k], '==' if hit else '≠', '' if hit else ' → go down'), t + .6, hide=t + 1.7 if not hit else t + 1.8)
        if hit: break
        f.show(vcell(X0, YB, k, vals[k], 'g'), t + 1.3)
        t += 2.0
    tr.kill(ip, t + 1.8)
    tr.emit(f); bar.emit(f)
    t += 2.0
    f.show(vcell(X0, YB, ans, target, 'f'), t)
    f.show(T(X0 + VW + 12, vy(YB, ans) + VH / 2 + 5, '✓ found', TG, 'start', mono=True, bold=True), t + .2)
    f.show(T(SX, 90, 'found at index %d · %d checks for %d cells' % (ans, steps, len(vals)), TG, 'start', bold=True), t + .3)
    f.show(T(SX, 112, 'worst case: every cell · O(n)', TG, 'start', bold=True), t + .4)
    f.h = YB + 12
    return f.render()
figs['p4'] = search_fig()

# ---------------------------------------------------------------- p5 · amortised O(n): each index in once, out once
def amort_fig():
    a = [6, 5, 4, 3, 2, 7]; n = len(a)
    X0 = 0; AY = 40; SYK = 128
    f = Anim('stk-p5-', 760, 0, 'Array 6 5 4 3 2 7 with a monotonic stack. The first five values are pushed one per step. Then 7 pops all five in one step, which looks expensive, but every value entered once and left once: 6 pushes plus 5 pops, at most 2n. A graph then shows total work against n: the 2n line stays far below the n squared curve.',
             'TOTAL COST OF THE MONOTONIC LOOP · EVERY INDEX GOES IN ONCE AND OUT ONCE', 3)
    for i, v in enumerate(a): f.show(box(X0 + i * (CW + G), AY, v, sub=i), .2 + i * .05)
    f.show(T(X0, SYK - 10, 'stack', MU, 'start'), .6)
    tr = Track(); st = []; t = 1.2; ops = 0; ip = None
    cx = lambda i: X0 + i * (CW + G) + CW / 2
    CX = 350
    for i, v in enumerate(a):
        if ip is None: ip = tr.add(lambda x, y: ptr_up(cx(0), AY + CH + 20, 'i'), (0, 0), t)
        else: tr.move(ip, (i * (CW + G), 0), t)
        pops = 0
        while st and a[st[-1][0]] < v:
            j, k = st.pop(); tr.kill(k, t + .6 + pops * .25); pops += 1
        ops += pops + 1
        k = tr.add(lambda x, y, v=v, i=i: box(x, y, v), (X0 + len(st) * (CW + G), SYK), t + .6 + pops * .25 + .2, frm=(X0 + i * (CW + G), AY))
        st.append((i, k))
        txt = 'push %d' % v if not pops else '%d pops + 1 push in one step' % pops
        say(f, CX, AY + 18, txt, t + .3, hide=t + (2.2 if pops else 1.0), c=MID if pops else PT, bold=bool(pops))
        say(f, CX, AY + 40, 'total so far = %d' % ops, t + .3, hide=t + (2.2 if pops else 1.0), c=PT)
        t += 2.4 if pops else 1.1
    tr.emit(f)
    f.show(T(CX, AY + 18, '✓ %d pushes + %d pops = %d ≤ 2n = %d' % (n, n - 1, ops, 2 * n), TG, 'start', mono=True, bold=True), t)
    # graph
    gx, gy, gw, gh = 60, 210, 560, 170
    NMAX, OMAX = 20, 100
    px = lambda v: gx + v / NMAX * gw; py = lambda o: gy + gh - o / OMAX * gh
    t += .8
    ax = L(gx, gy + gh, gx + gw + 10, gy + gh, MU, 1.2) + L(gx, gy + gh, gx, gy - 6, MU, 1.2)
    for v in (5, 10, 15, 20): ax += T(px(v), gy + gh + 16, str(v), FA, cls='sv-s', mono=True) + L(px(v), gy + gh, px(v), gy + gh + 4, MU, 1)
    for o in (25, 50, 75, 100): ax += T(gx - 8, py(o) + 4, str(o), FA, 'end', cls='sv-s', mono=True) + L(gx, py(o), gx + gw, py(o), 'var(--rule)', 1, '2 4')
    ax += T(gx + gw + 14, gy + gh + 4, 'n', MU, 'start', mono=True) + T(gx - 8, gy - 12, 'operations', MU, 'start', mono=True)
    f.show(ax, t)
    sq = 'M' + ' L'.join('%.1f %.1f' % (px(v), py(v * v)) for v in [x * .1 for x in range(0, 101)])
    f.show('<path d="%s" fill="none" stroke="var(--ghost)" stroke-width="2"/>' % sq + T(px(10) + 8, py(100) + 14, 'n² if every step rescanned', MU, 'start'), t + .8)
    f.show('<path d="M%.1f %.1f L%.1f %.1f" fill="none" stroke="%s" stroke-width="2.6"/>' % (px(0), py(0), px(20), py(40), TG)
           + T(px(20) - 4, py(40) - 10, '2n', TG, 'end', mono=True, bold=True), t + 1.8, d=.8)
    f.show('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s"/>' % (px(6), py(11), MID) + L(px(6) + 5, py(11) + 3, px(11) - 4, py(6), MID, 1, '3 3') + T(px(11), py(6) + 4, 'our run: n = 6 → 11 operations', MID, 'start', mono=True, bold=True), t + 2.6)
    f.show(T(gx + gw, gy + gh + 38, 'a while inside a for is still O(n) when each pop uses up a pushed index', TG, 'end', bold=True), t + 3.2)
    f.h = gy + gh + 50
    return f.render()
figs['p5'] = amort_fig()

# ---------------------------------------------------------------- q1 · valid parentheses
def paren_fig():
    s = '([]{()})'; pair = {')': '(', ']': '[', '}': '{'}
    LS = ['st = []', 'for c in s:', "    if c in '([{': st.append(c)", '    elif st.pop() != pair[c]:', '        return False', 'return not st']
    code = Code2(0, 40, LS); X0 = code.w + 26
    n = len(s); AY = 60; SYK = 150; STY = 236
    cx = lambda i: X0 + i * (CW + G) + CW / 2
    f = Anim('stk-q1-', 760, 0, 'String ( [ ] { ( ) } ) is read left to right. Every opening bracket is pushed. Every closing bracket pops the top and checks it is its partner. At the end the stack is empty, so the string is valid.',
             'MATCHING BRACKETS · EVERY CLOSER MUST MEET ITS OPENER ON TOP', 3)
    f.static(code.svg()); bar = Bar(code); tr = Track()
    for i, c in enumerate(s): f.show(box(X0 + i * (CW + G), AY, c, sub=i), .2 + i * .05)
    f.show(T(X0, SYK - 10, 'stack · bottom → top', MU, 'start'), .7)
    f.show(L(X0, SYK + CH + 4, X0 + 5 * (CW + G), SYK + CH + 4, 'var(--rule)', 1, '3 3'), .7)
    bar.at(1.2, 0); t = 1.9; st = []; ip = None
    sx = lambda k: X0 + k * (CW + G)
    for i, c in enumerate(s):
        bar.at(t, 1)
        if ip is None: ip = tr.add(lambda x, y: ptr_up(cx(0), AY + CH + 20, 'i'), (0, 0), t)
        else: tr.move(ip, (i * (CW + G), 0), t)
        if c in '([{':
            bar.at(t + .5, 2)
            say(f, X0, STY, "'%s' opens → push" % c, t + .5, hide=t + 1.4)
            st.append(tr.add(lambda x, y, c=c: box(x, y, c), (sx(len(st)), SYK), t + .7, frm=(sx(i), AY)))
            t += 1.5
        else:
            bar.at(t + .5, 3)
            f.show(ring(sx(len(st) - 1), SYK), t + .5, hide=t + 1.6)
            say(f, X0, STY, "'%s' pops '%s' → a pair ✓" % (c, pair[c]), t + .5, hide=t + 1.6)
            tr.kill(st.pop(), t + 1.3)
            t += 1.9
    bar.at(t, 5)
    tr.kill(ip, t + 1.0)
    tr.emit(f); bar.emit(f)
    say(f, X0, STY, 'stack empty → not st = True', t + .3, hide=t + 1.3)
    t += 1.5
    f.show(R(X0, SYK, 2 * (CW + G) + CW, CH, TG, TG, 6, 1.2) + T(X0 + (3 * CW + 2 * G) / 2, SYK + 23, '✓ valid', 'var(--on-fill)', mono=True, bold=True), t)
    f.show(T(X0, STY, '✓ every closer met its opener · %d chars, one pass · O(n)' % n, TG, 'start', bold=True), t + .2)
    f.h = STY + 28
    return f.render()
figs['q1'] = paren_fig()

# ---------------------------------------------------------------- q2 · next greater element (daily temperatures)
tmp = [73, 74, 75, 71, 69, 72, 76, 73]
f, X0, SYK, STY, st, cnt, t, sx = mono('stk-q2-', 'NEXT GREATER ELEMENT · DAYS UNTIL A WARMER DAY',
    'Temperatures 73 74 75 71 69 72 76 73. The stack holds days still waiting for a warmer day. Each warmer day pops the waiting days it beats and writes the distance into ans. 72 answers 69 and 71; 76 answers 72 and 75. 76 and 73 never get an answer and stay 0.',
    tmp, ['ans, st = [0] * len(a), []', 'for i in range(len(a)):', '    while st and a[st[-1]] < a[i]:', '        j = st.pop()', '        ans[j] = i - j', '    st.append(i)'],
    {'for': 1, 'while': 2, 'pop': 3, 'ans': 4, 'push': 5}, ans=True, hint='stack = days still waiting')
res = [1, 1, 4, 2, 1, 1, 0, 0]
ANY = SYK + 80
for k, (j, _) in enumerate(st): f.show(box(sx(k), SYK, tmp[j], 'g'), t)
for j in (6, 7): f.show(box(sx(j), ANY, 0, 'g'), t + .2)
for j in range(len(tmp)):
    if res[j]: f.show(R(sx(j), ANY, CW, CH, 'var(--bg)', 'none', 6) + box(sx(j), ANY, res[j], 'f'), t + .2)
f.show(T(X0, STY, '✓ ans = %s · days 6 and 7 never see a warmer day' % res, TG, 'start', bold=True), t + .4)
f.h = STY + 28
figs['q2'] = f.render()

# ---------------------------------------------------------------- q3 · largest rectangle in a histogram
def hist_fig():
    a = [2, 1, 5, 6, 2, 3]; n = len(a)
    LS = ['st, best = [], 0', 'for i, h in enumerate(a + [0]):', '    while st and a[st[-1]] > h:', '        top = st.pop()',
         '        l = st[-1] + 1 if st else 0', '        best = max(best, a[top] * (i - l))', '    st.append(i)']
    code = Code2(0, 40, LS); X0 = code.w + 30
    BW, BG, U = 40, 8, 22; BASE = 200
    bx = lambda i: X0 + i * (BW + BG)
    SYK = BASE + 46; STY = SYK + 80
    f = Anim('stk-q3-', 780, 0, 'Bars 2 1 5 6 2 3. The stack holds bars whose right edge is not known yet. A lower bar pops the taller ones; each popped bar spreads from just after the new top of the stack to just before the lower bar, and its rectangle is measured. Popping 5 at i = 4 gives 5 times 2 = 10, the largest area.',
             'LARGEST RECTANGLE · A LOWER BAR CLOSES EVERY TALLER BAR BEFORE IT', 3)
    f.static(code.svg()); bar = Bar(code); tr = Track()
    def barsvg(i, kind='n'):
        h = a[i] * U
        fill, st_ = {'n': ('var(--bg)', RULE_HI), 'g': ('var(--sunk)', 'var(--rule)')}[kind]
        return R(bx(i), BASE - h, BW, h, fill, st_, 4, 1.2) + T(bx(i) + BW / 2, BASE - h + 16, str(a[i]), TX if kind == 'n' else 'var(--ghost)', mono=True, bold=True)
    f.show(L(X0 - 6, BASE, bx(n) + 4, BASE, MU, 1.2), .2)
    for i in range(n):
        f.show(barsvg(i) + T(bx(i) + BW / 2, BASE + 16, str(i), FA, cls='sv-s', mono=True), .3 + i * .06)
    f.show(T(bx(n) + BW / 2, BASE + 16, 'end', FA, cls='sv-s', mono=True), .7)
    f.show(T(X0, SYK - 8, 'stack (bar indices)', MU, 'start'), .8)
    SW = 34
    sx = lambda k: X0 + k * (SW + 6)
    bar.at(1.2, 0); t = 2.0; st = []; best = 0; bestrect = None; ip = None
    for i, h in enumerate(a + [0]):
        bar.at(t, 1)
        if ip is None: ip = tr.add(lambda x, y: ptr_up(bx(0) + BW / 2, BASE + 22, 'i', 10), (0, 0), t)
        else: tr.move(ip, (i * (BW + BG), 0), t)
        say(f, X0, STY, 'i = %d · h = %d' % (i, h) + (' (sentinel)' if i == n else ''), t, hide=t + .9, c=PT)
        t += 1.0
        while st and a[st[-1][0]] > h:
            bar.at(t, 2)
            f.show(ring(sx(len(st) - 1), SYK, SW, 30), t, hide=t + .75)
            j, kid = st.pop()
            l = st[-1][0] + 1 if st else 0
            area = a[j] * (i - l)
            bar.at(t + .5, 3); tr.kill(kid, t + .7)
            bar.at(t + .9, 5)
            rect = R(bx(l) - 2, BASE - a[j] * U, (i - l) * (BW + BG) - BG + 4, a[j] * U, vt('.16'), MID, 4, 2)
            f.show(rect, t + 1.0, hide=t + 2.0)
            say(f, X0, STY, 'pop %d (h %d) · spans %d..%d · %d × %d = %d' % (j, a[j], l, i - 1, a[j], i - l, area), t + 1.0, hide=t + 2.0)
            if area > best:
                best = area; bestrect = (l, i, a[j])
            say(f, X0, STY + 22, 'best = %d' % best, t + 1.0, hide=t + 2.0, c=TG, bold=True)
            t += 2.2
        if i < n:
            bar.at(t, 6)
            st.append((i, tr.add(lambda x, y, i=i: box(x, y, i, w=SW, h=30), (sx(len(st)), SYK), t + .1, frm=(bx(i) + 3, BASE + 2))))
            t += 1.0
    tr.kill(ip, t)
    tr.emit(f); bar.emit(f)
    l, r, hh = bestrect
    f.show(R(bx(l) - 2, BASE - hh * U, (r - l) * (BW + BG) - BG + 4, hh * U, TG, TG, 4, 1.4)
           + T((bx(l) + bx(r) - BG) / 2, BASE - hh * U / 2 + 5, '10', 'var(--on-fill)', mono=True, bold=True), t)
    f.show(T(bx(r) - BG + 8, BASE - hh * U + 14, '✓ max', TG, 'start', mono=True, bold=True), t + .2)
    f.show(T(X0, STY, '✓ largest area = %d · bars 2..3 at height 5 · each bar in and out once · O(n)' % best, TG, 'start', bold=True), t + .3)
    f.h = STY + 30
    return f.render()
figs['q3'] = hist_fig()

# ---------------------------------------------------------------- q4 · sliding window maximum (monotonic deque)
def deque_fig2():
    a = [1, 3, -1, -3, 5, 3, 6, 7]; k = 3; n = len(a)
    LS = ['dq, out = deque(), []', 'for i, x in enumerate(a):', '    while dq and a[dq[-1]] <= x: dq.pop()', '    dq.append(i)',
         '    if dq[0] <= i - k: dq.popleft()', '    if i >= k - 1: out.append(a[dq[0]])']
    code = Code2(0, 40, LS); X0 = code.w + 26
    AY = 60; DQY = AY + 96; OY = DQY + 84; STY = OY + 74
    cxl = lambda i: X0 + i * (CW + G)
    W = max(760, cxl(n) + 4)
    f = Anim('stk-q4-', W, 0, 'Window of 3 slides over 1 3 -1 -3 5 3 6 7. A deque keeps indices whose values decrease from front to back. A new value pops smaller-or-equal ones from the back; the front leaves when it falls out of the window. The front is always the window maximum: 3 3 5 5 6 7.',
             'SLIDING WINDOW MAXIMUM · A DEQUE KEEPS ONLY VALUES THAT CAN STILL WIN', 3)
    f.static(code.svg()); bar = Bar(code); tr = Track()
    for i, v in enumerate(a): f.show(box(cxl(i), AY, v, sub=i), .2 + i * .05)
    f.show(T(X0, DQY - 10, 'deque · front → back', MU, 'start'), .7)
    f.show(T(X0, OY - 10, 'out', MU, 'start', mono=True), .8)
    f.show(T(cxl(n) - G, AY - 26, 'window k = 3', PT, 'end', mono=True), .9)
    bar.at(1.2, 0)
    # the window frame: 3 cells wide, starts over 0..2, slides one cell at each i >= 3
    WF = lambda x, y: R(x - 4, y - 6, 3 * (CW + G) - G + 8, CH + 12, 'none', PT, 9, 1.8)
    wf = tr.add(WF, (cxl(0), AY), 1.6)
    t = 2.2; dq = []; out = 0; ip = None
    def place(t):
        for p, (j, kid) in enumerate(dq): tr.move(kid, (cxl(p), DQY), t)
    for i, x in enumerate(a):
        bar.at(t, 1)
        if ip is None: ip = tr.add(lambda x_, y_: ptr_up(cxl(0) + CW / 2, AY + CH + 22, 'i'), (0, 0), t)
        else: tr.move(ip, (i * (CW + G), 0), t)
        if i >= k: tr.move(wf, (cxl(i - k + 1), AY), t)
        say(f, X0, STY, 'i = %d · x = %d' % (i, x), t, hide=t + .9, c=PT)
        t += 1.0
        while dq and a[dq[-1][0]] <= x:
            bar.at(t, 2)
            f.show(ring(cxl(len(dq) - 1), DQY), t, hide=t + 1.0)
            say(f, X0, STY, 'back a[%d] = %d ≤ %d → pop back' % (dq[-1][0], a[dq[-1][0]], x), t, hide=t + 1.0)
            tr.kill(dq.pop()[1], t + .7); t += 1.2
        bar.at(t, 3)
        dq.append((i, tr.add(lambda x_, y_, x=x, i=i: box(x_, y_, x, sub=i), (cxl(len(dq)), DQY), t + .1, frm=(cxl(i), AY))))
        t += 1.0
        if dq[0][0] <= i - k:
            bar.at(t, 4)
            f.show(ring(cxl(0), DQY), t, hide=t + 1.0)
            say(f, X0, STY, 'front index %d ≤ %d - 3 → out of window' % (dq[0][0], i), t, hide=t + 1.0)
            tr.kill(dq.pop(0)[1], t + .7); place(t + .8); t += 1.5
        if i >= k - 1:
            bar.at(t, 5)
            f.show(ring(cxl(0), DQY), t, hide=t + 1.0)
            say(f, X0, STY, 'window %d..%d → max = front = %d' % (i - k + 1, i, a[dq[0][0]]), t, hide=t + 1.0, c=MID)
            f.show(R(cxl(out), OY, CW, CH, 'var(--bg)', 'none', 6) + box(cxl(out), OY, a[dq[0][0]], 't'), t + .5)
            out += 1
            t += 1.2
    tr.kill(ip, t); tr.kill(wf, t)
    tr.emit(f); bar.emit(f)
    t += .3
    for p, v in enumerate([3, 3, 5, 5, 6, 7]): f.show(box(cxl(p), OY, v, 'f'), t)
    f.show(T(X0, STY, '✓ out = [3, 3, 5, 5, 6, 7] · each index enters and leaves once · O(n)', TG, 'start', bold=True), t + .2)
    f.h = STY + 28
    return f.render()
figs['q4'] = deque_fig2()

# ---------------------------------------------------------------- q5 · remove k digits (greedy monotonic stack)
def digits_fig():
    num = '1432219'; K = 3; n = len(num)
    LS = ['st = []', 'for d in num:', '    while k and st and st[-1] > d:', '        st.pop(); k -= 1', '    st.append(d)', "return ''.join(st[:len(st) - k])"]
    code = Code2(0, 40, LS); X0 = code.w + 26
    AY = 66; SYK = AY + 96; STY = SYK + 80
    cxl = lambda i: X0 + i * (CW + G)
    f = Anim('stk-q5-', 760, 0, 'Remove 3 digits from 1432219 to get the smallest number. Digits go on a stack; a smaller digit pops a bigger one before it while removals remain. 3 pops 4, 2 pops 3, 1 pops 2. The stack ends as 1219.',
             'REMOVE K DIGITS · A SMALLER DIGIT POPS A BIGGER ONE BEFORE IT', 3)
    f.static(code.svg()); bar = Bar(code); tr = Track()
    for i, v in enumerate(num): f.show(box(cxl(i), AY, v, sub=i), .2 + i * .05)
    f.show(T(X0, SYK - 10, 'stack · bottom → top', MU, 'start'), .7)
    f.show(chip(X0, 24, 'remove k = 3 digits'), .9)
    bar.at(1.2, 0); t = 2.0; st = []; k = K; ip = None
    klab = [(K, 1.0)]
    for i, d in enumerate(num):
        bar.at(t, 1)
        if ip is None: ip = tr.add(lambda x_, y_: ptr_up(cxl(0) + CW / 2, AY + CH + 22, 'i'), (0, 0), t)
        else: tr.move(ip, (i * (CW + G), 0), t)
        t += .7
        while True:
            if not (k and st):
                if st and not k: say(f, X0, STY, 'k = 0 → no more removals', t, hide=t + .9)
                break
            bar.at(t, 2)
            f.show(ring(cxl(len(st) - 1), SYK), t, hide=t + 1.0)
            pop = st[-1][0] > d
            say(f, X0, STY, ("top %s > %s → pop" if pop else "top %s ≤ %s → keep") % (st[-1][0], d), t, hide=t + 1.0)
            if not pop: t += 1.1; break
            bar.at(t + .5, 3); tr.kill(st.pop()[1], t + .7); k -= 1
            klab.append((k, t + .7))
            t += 1.3
        bar.at(t, 4)
        st.append((d, tr.add(lambda x_, y_, d=d: box(x_, y_, d), (cxl(len(st)), SYK), t + .1, frm=(cxl(i), AY))))
        t += 1.0
    bar.at(t, 5); tr.kill(ip, t)
    for q, (kv, kt) in enumerate(klab):
        f.show(T(cxl(n) - G, SYK + 23, 'k = %d' % kv, PT, 'end', mono=True, bold=True), kt, hide=klab[q + 1][1] - .2 if q + 1 < len(klab) else None)
    tr.emit(f); bar.emit(f)
    t += .6
    for p, (d, _) in enumerate(st): f.show(box(cxl(p), SYK, d, 'f'), t)
    f.show(T(cxl(len(st)) + 4, SYK + 23, '✓ 1219', TG, 'start', mono=True, bold=True), t + .2)
    f.show(T(X0, STY, '✓ smallest after removing 3 digits = 1219 · one pass · O(n)', TG, 'start', bold=True), t + .3)
    f.h = STY + 28
    return f.render()
figs['q5'] = digits_fig()

os.makedirs('/tmp/dsa', exist_ok=True)
json.dump(figs, open('/tmp/dsa/stack-monotonic-queue.json', 'w'))
print('figures:', list(figs))
