"""Helpers for the tree-shaped DSA lessons: tree-bst-traversal, trie, union-find.
Built on engine.py (Anim timeline). Do not import from other lessons' files.

Vocabulary (blue-violet family only, all through tokens):
  node      circle with its value; plain = --bg + --rule-hi border
  vis       light indigo tint: node already visited / part of the result
  grey      --sunk + --ghost text: discarded subtree
  fill      solid --filled: the answer
  probe     violet ring that SLIDES from node to node, brand label = pointer name
  code      box on the LEFT, one violet bar sliding line to line
"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Anim, R, T, L, arrow, cap, RULE_HI, TX, FA, MU

PT, MID, TG, GH = 'var(--brand)', 'var(--violet)', 'var(--filled)', 'var(--ghost)'
ONF = 'var(--on-fill)'
def vt(a): return 'rgba(var(--violet-a),%s)' % a
def it(a): return 'rgba(var(--blue-a),%s)' % a
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
LH = 20
NR = 16


def circ(x, y, r, fill, stroke, sw=1.2, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, r, fill, stroke, sw, d)


STY = {
    'plain': ('var(--bg)', RULE_HI, TX, 1.3),
    'vis':   (it('.14'), TG, TG, 1.4),
    'grey':  ('var(--sunk)', 'var(--rule)', GH, 1.1),
    'fill':  (TG, TG, ONF, 1.3),
}


def node(x, y, v, st='plain', r=NR, end=False):
    """end=True draws the inner ring that marks 'a word ends here' (trie)."""
    f, s, c, w = STY[st]
    o = circ(x, y, r, 'var(--bg)', 'none', 0) + circ(x, y, r, f, s, w)
    if end:
        o += circ(x, y, r - 3.5, 'none', ONF if st == 'fill' else (s if st != 'plain' else 'var(--dim)'), 1.1)
    return o + T(x, y + 4.5, esc(v), c, mono=True, bold=st != 'grey')


def edge(a, b, r=NR, c=RULE_HI, sw=1.4, dash=None):
    (x1, y1), (x2, y2) = a, b
    d = math.hypot(x2 - x1, y2 - y1) or 1
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return L(x1 + ux * r, y1 + uy * r, x2 - ux * r, y2 - uy * r, c, sw, dash)


def up_arrow(a, b, r=NR, c=MU, sw=1.3):
    """child a -> parent b, head touching the parent's border."""
    (x1, y1), (x2, y2) = a, b
    d = math.hypot(x2 - x1, y2 - y1) or 1
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return arrow(x1 + ux * r, y1 + uy * r, x2 - ux * (r + 1), y2 - uy * (r + 1), c, sw, None, 6)


def self_loop(x, y, r=NR, c=MU):
    """root points at itself: small arc above the node."""
    return ('<path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="1.2"/>'
            % (x - 6, y - r + 1, x - 14, y - r - 16, x + 14, y - r - 16, x + 6, y - r + 1, c)
            + '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>' % (x + 6, y - r + 1, x + 3, y - r - 6, x + 10, y - r - 4, c))


def ring(x, y, r=NR + 5):
    return circ(x, y, r, vt('.10'), MID, 2.2)


def goal_ring(x, y, r=NR + 5):
    return circ(x, y, r, 'none', TG, 1.4, '4 3')


def chip(x, y, text, a='start'):
    w = 24 + len(text) * 6.6
    x0 = x if a == 'start' else x - w / 2
    return R(x0, y, w, 24, 'var(--bg)', 'none', 12) + R(x0, y, w, 24, it('.12'), TG, 12, 1.3) + T(x0 + w / 2, y + 16.5, esc(text), TG, mono=True, bold=True)


def ocell(x, y, v, st='plain', w=34, h=30):
    """output / array cell."""
    f, s, c, sw = STY[st]
    return R(x, y, w, h, 'var(--bg)', 'none', 6) + R(x, y, w, h, f, s, 6, sw) + T(x + w / 2, y + h / 2 + 5, esc(v), c, mono=True, bold=st != 'grey')


def cring(x, y, w=34, h=30):
    return R(x - 3, y - 3, w + 6, h + 6, vt('.10'), MID, 8, 2.2)


def plabel(x, y, name, side='ul', r=NR):
    """pointer name next to a node, brand colour. side: ul (upper-left), ur, l, r, u, d."""
    o = {'ul': (x - r - 4, y - r + 1, 'end'), 'ur': (x + r + 4, y - r + 1, 'start'),
         'l': (x - r - 9, y + 4, 'end'), 'r': (x + r + 9, y + 4, 'start'),
         'u': (x, y - r - 9, 'middle'), 'd': (x, y + r + 17, 'middle')}[side]
    return T(o[0], o[1], name, PT, o[2], mono=True, bold=True)


class Code2:
    def __init__(s, x, y, lines, w=None):
        s.x, s.y, s.lines = x, y, lines
        s.w = w or max(200, 30 + max(len(l) for l in lines) * 6.6)
    def svg(s):
        o = R(s.x, s.y, s.w, s.h(), 'var(--bg)', RULE_HI, 8)
        for i, l in enumerate(s.lines):
            n = len(l) - len(l.lstrip())
            o += T(s.x + 14, s.y + 22 + i * LH, '\u00a0' * n + esc(l.lstrip()), TX, 'start', mono=True)
        return o
    def bar(s): return R(s.x + 4, s.y + 8, s.w - 8, LH, vt('.13'), 'none', 4) + R(s.x + 4, s.y + 8, 3, LH, MID, 'none', 1.5)
    def h(s): return len(s.lines) * LH + 14


class Fig:
    """Anim + code bar + text slots (each new line in a slot hides the previous one) + sliding items."""
    def __init__(s, pre, w, aria, caption, hold=3.0):
        s.f = Anim(pre, w, 0, aria, caption, hold)
        s.code = None; s.bar = [(0, 0, 0)]
        s.slots = {}; s.said = {}; s.movers = {}
    def static(s, svg): s.f.static(svg); return s
    def show(s, svg, t, hide=None, d=.35): s.f.show(svg, t, hide, d); return s
    # code
    def add_code(s, x, y, lines, w=None):
        s.code = Code2(x, y, lines, w); s.f.static(s.code.svg()); return s.code
    def line(s, t, i): s.bar.append((t, 0, i * LH))
    # text slots
    def slot(s, k, x, y, a='start'): s.slots[k] = (x, y, a)
    def say(s, k, t, text, c=TX, bold=False):
        s.said.setdefault(k, []).append([t, text, c, bold, None])
    def clear(s, k, t):
        if s.said.get(k): s.said[k][-1][4] = t
    # sliding items: svg drawn at (x, y) via fn; moves are absolute positions
    def mover(s, k, fn, t, x, y):
        s.movers[k] = dict(fn=fn, t0=t, pts=[(t, x, y)], hide=None)
    def move(s, k, t, x, y): s.movers[k]['pts'].append((t, x, y))
    def hide(s, k, t): s.movers[k]['hide'] = t
    def render(s, h, d=.5):
        for k, items in s.said.items():
            x, y, a = s.slots[k]
            for i, (t, text, c, b, end) in enumerate(items):
                hide = end if end is not None else (max(t + .3, items[i + 1][0] - .35) if i + 1 < len(items) else None)
                s.f.show(T(x, y, esc(text), c, a, mono=True, bold=b), t, hide)
        for k, m in s.movers.items():
            x0, y0 = m['pts'][0][1], m['pts'][0][2]
            rel = [(m['pts'][0][0], 0, 0)] + [(t, x - x0, y - y0) for t, x, y in m['pts'][1:]]
            s.f.path(m['fn'](x0, y0), rel, m['t0'], d=d, hide=m['hide'])
        if s.code: s.f.path(s.code.bar(), s.bar, 0, appear=False, d=.3)
        s.f.h = h
        return s.f.render()


# ---------- layouts ----------
class BT:
    """Binary tree from nested tuples (v, left, right); x by inorder slot, y by depth."""
    def __init__(s, spec, x0, y0, dx=44, dy=54):
        s.n = []; s.root = s._add(spec, None, 0)
        s.inorder = []
        def ino(i):
            if i is None: return
            ino(s.n[i]['l']); s.inorder.append(i); ino(s.n[i]['r'])
        ino(s.root)
        for k, i in enumerate(s.inorder):
            s.n[i]['x'] = x0 + k * dx; s.n[i]['y'] = y0 + s.n[i]['d'] * dy
    def _add(s, sp, par, d):
        if sp is None: return None
        if not isinstance(sp, tuple): sp = (sp, None, None)
        i = len(s.n); s.n.append(dict(v=sp[0], par=par, d=d, l=None, r=None))
        s.n[i]['l'] = s._add(sp[1], i, d + 1); s.n[i]['r'] = s._add(sp[2], i, d + 1)
        return i
    def p(s, i): return (s.n[i]['x'], s.n[i]['y'])
    def v(s, i): return s.n[i]['v']
    def by(s, v): return [i for i, n in enumerate(s.n) if n['v'] == v][0]
    def L(s, i): return s.n[i]['l']
    def Rr(s, i): return s.n[i]['r']
    def sub(s, i):
        if i is None: return []
        return [i] + s.sub(s.n[i]['l']) + s.sub(s.n[i]['r'])
    def edges_svg(s, skip=()):
        return ''.join(edge(s.p(n['par']), s.p(i)) for i, n in enumerate(s.n) if n['par'] is not None and i not in skip)
    def draw(s, f, t0=.2, dt=.08, order=None):
        """fade in nodes top-down (preorder), edges with their child."""
        order = order or s.sub(s.root)
        for k, i in enumerate(order):
            g = node(*s.p(i), s.v(i))
            if s.n[i]['par'] is not None: g = edge(s.p(s.n[i]['par']), s.p(i)) + g
            f.show(g, t0 + k * dt)
        return t0 + len(order) * dt


def dump(name, figs):
    os.makedirs('/tmp/dsa', exist_ok=True)
    json.dump(figs, open('/tmp/dsa/%s.json' % name, 'w'))


def graph(f, gx, gy, gw, gh, xmax, ymax, curves, t, xt=(), yt=(), xl='n', yl='steps'):
    """axes + curves drawn one after another. curves=[(fn, label, colour, width, label_x)]."""
    px = lambda v: gx + v / xmax * gw
    py = lambda v: gy + gh - min(v, ymax) / ymax * gh
    ax = L(gx, gy + gh, gx + gw + 10, gy + gh, MU, 1.2) + L(gx, gy + gh, gx, gy - 6, MU, 1.2)
    for v in xt: ax += T(px(v), gy + gh + 16, str(v), FA, cls='sv-s', mono=True) + L(px(v), gy + gh, px(v), gy + gh + 4, MU, 1)
    for v in yt: ax += T(gx - 8, py(v) + 4, str(v), FA, 'end', cls='sv-s', mono=True) + L(gx, py(v), gx + gw, py(v), 'var(--rule)', 1, '2 4')
    ax += T(gx + gw + 14, gy + gh + 4, xl, MU, 'start', mono=True) + T(gx - 8, gy - 12, yl, MU, 'start', mono=True)
    f.show(ax, t)
    for k, (fn, lab, c, sw, lx) in enumerate(curves):
        pts, v = [], 0.0
        while v <= xmax + 1e-9:
            yv = fn(v); pts.append((px(v), py(yv)))
            if yv > ymax: break
            v += xmax / 240
        d = 'M' + ' L'.join('%.1f %.1f' % p for p in pts)
        ly = py(min(fn(lx), ymax))
        f.show('<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (d, c, sw)
               + T(px(lx) + 6, ly - 7, lab, c, 'start', mono=True, bold=True), t + .8 + k * 1.0, d=.6)
    return px, py


class Scene(Fig):
    """Fig whose nodes can slide. Edges follow their nodes rigidly when both ends move together;
    when the shape changes the old edge fades out and the new one fades in after the slide.

      sc.place(t, u, x, y)        node u is (or moves to) (x, y) at time t
      sc.edge_on(t, a, b, kind)   kind 'line' (tree edge) or 'up' (arrow a -> parent b)
      sc.edge_off(t, a, b, kind)
      sc.over(u, fn, t, hide)     overlay fn(x, y) that follows node u from t (style change)
      sc.top(u, fn, t, hide)      same, drawn above everything (rings, labels)
    """
    D = .55
    def __init__(s, pre, w, aria, caption, hold=3.0, r=NR):
        Fig.__init__(s, pre, w, aria, caption, hold)
        s.r = r; s.ptl = {}; s.born = {}; s.lab = {}; s.es = {}; s.ov = []; s.tops = []; s.nend = {}
    def node(s, u, label, t, x, y, end=False):
        s.lab[u] = label; s.born[u] = t; s.ptl[u] = [(t, x, y)]; s.nend[u] = end
    def place(s, t, u, x, y):
        if s.ptl[u][-1][1:] != (x, y): s.ptl[u].append((t, x, y))
    def pos(s, u, t):
        p = None
        for tt, x, y in s.ptl[u]:
            if tt <= t + 1e-6: p = (x, y)
        return p or s.ptl[u][0][1:]
    def edge_on(s, t, a, b, kind='line'): s.es.setdefault((a, b, kind), []).append([t, None])
    def edge_off(s, t, a, b, kind='line'):
        iv = s.es[(a, b, kind)][-1]
        if iv[1] is None: iv[1] = t
    def over(s, u, fn, t, hide=None): s.ov.append((u, fn, t, hide))
    def top(s, u, fn, t, hide=None): s.tops.append((u, fn, t, hide))
    def _follow(s, u, fn, t, hide):
        x0, y0 = s.pos(u, t)
        pts = [(t, 0, 0)] + [(tt, x - x0, y - y0) for tt, x, y in s.ptl[u] if tt > t + 1e-6 and (hide is None or tt < hide)]
        s.f.path(fn(x0, y0), pts, t, d=s.D, hide=hide)
    def render(s, h, d=None):
        D = s.D
        for (a, b, kind), ivs in s.es.items():
            draw = (lambda pa, pb: edge(pa, pb, s.r)) if kind == 'line' else (lambda pa, pb: up_arrow(pa, pb, s.r))
            for on, off in ivs:
                mt = sorted(set(tt for u in (a, b) for tt, _, _ in s.ptl[u][1:] if tt > on + 1e-6 and (off is None or tt < off)))
                seg_t = on; pa, pb = s.pos(a, on), s.pos(b, on); pts = [(on, 0, 0)]
                for tm in mt:
                    na, nb = s.pos(a, tm), s.pos(b, tm)
                    da = (na[0] - pa[0], na[1] - pa[1]); db = (nb[0] - pb[0], nb[1] - pb[1])
                    if abs(da[0] - db[0]) < .01 and abs(da[1] - db[1]) < .01:
                        pts.append((tm, da[0], da[1]))      # both ends slide together: edge slides too
                    else:                                   # shape changes: fade out, redraw after the slide
                        s.f.path(draw(pa, pb), pts, seg_t, d=D, hide=tm)
                        seg_t = tm + D; pa, pb = na, nb; pts = [(seg_t, 0, 0)]
                s.f.path(draw(pa, pb), pts, seg_t, d=D, hide=off)
        for u in s.lab:
            s._follow(u, lambda x, y, u=u: node(x, y, s.lab[u], r=s.r, end=s.nend[u]), s.born[u], None)
        for u, fn, t, hide in s.ov: s._follow(u, fn, t, hide)
        for u, fn, t, hide in s.tops: s._follow(u, fn, t, hide)
        return Fig.render(s, h)
