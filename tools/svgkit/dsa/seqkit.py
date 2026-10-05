"""Shared helpers for the array-string, linked-list and hash-map lessons (built on engine.py).

Fig wraps engine.Anim with: a code box on the left and one violet bar sliding line to line,
cells / nodes / slots in the DSA palette, pointers, probe rings, status lines.
Colours: --brand pointers, --violet probe + running line, --filled goal/answer,
--sunk + --ghost discarded, --bg + --rule-hi untouched.
"""
import sys, os, re, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Anim, R, T, L, arrow, cap, RULE_HI, TX, FA, MU
from tablefig import curve

PT, MID, TG, GH = 'var(--brand)', 'var(--violet)', 'var(--filled)', 'var(--ghost)'
ONF = 'var(--on-fill)'
def vt(a): return 'rgba(var(--violet-a),%s)' % a
def it(a): return 'rgba(var(--blue-a),%s)' % a
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

LH = 20
CW, CH, G = 42, 36, 6
P = CW + G


class Code2:
    def __init__(s, x, y, lines, w): s.x, s.y, s.lines, s.w = x, y, lines, w
    def svg(s):
        o = R(s.x, s.y, s.w, s.h(), 'var(--bg)', RULE_HI, 8)
        for i, l in enumerate(s.lines):
            n = len(l) - len(l.lstrip())
            o += T(s.x + 14 + n * 6.3, s.y + 22 + i * LH, esc(l.lstrip()), TX, 'start', mono=True)
        return o
    def bar(s): return R(s.x + 4, s.y + 8, s.w - 8, LH, vt('.13'), 'none', 4) + R(s.x + 4, s.y + 8, 3, LH, MID, 'none', 1.5)
    def h(s): return len(s.lines) * LH + 14


# ---------- shapes ----------
def cellv(x, y, v, w=CW, h=CH, idx=None):
    o = R(x, y, w, h, 'var(--bg)', RULE_HI, 6, 1.2) + T(x + w / 2, y + h / 2 + 5, esc(v), TX, mono=True, bold=True)
    if idx is not None: o += T(x + w / 2, y + h + 16, str(idx), FA, cls='sv-s', mono=True)
    return o
def cellg(x, y, v, w=CW, h=CH):
    return R(x, y, w, h, 'var(--sunk)', 'var(--rule)', 6, 1) + T(x + w / 2, y + h / 2 + 5, esc(v), GH, mono=True)
def cellf(x, y, v, w=CW, h=CH):
    return R(x, y, w, h, TG, TG, 6, 1.2) + T(x + w / 2, y + h / 2 + 5, esc(v), ONF, mono=True, bold=True)
def ring(x, y, w=CW, h=CH):
    return R(x - 3, y - 3, w + 6, h + 6, vt('.10'), MID, 8, 2.2)
def goalring(x, y, w=CW, h=CH):
    return R(x - 4, y - 4, w + 8, h + 8, 'none', TG, 8, 1.4, '4 3')
def ptr_below(cx, y, name, ln=14):
    return arrow(cx, y + ln, cx, y, PT, 1.6, None, 6) + T(cx, y + ln + 13, name, PT, mono=True, bold=True)
def ptr_above(cx, y, name, ln=14):
    return T(cx, y - ln - 5, name, PT, mono=True, bold=True) + arrow(cx, y - ln, cx, y, PT, 1.6, None, 6)
def ptr_left(x, cy, name, ln=16):
    return T(x - ln - 5, cy + 4, name, PT, 'end', mono=True, bold=True) + arrow(x - ln, cy, x, cy, PT, 1.6, None, 6)
def chip(x, y, txt, a='start'):
    w = 24 + len(txt) * 6.6
    x0 = x if a == 'start' else x - w / 2
    return R(x0, y, w, 24, it('.12'), TG, 12, 1.3) + T(x0 + w / 2, y + 16.5, esc(txt), TG, mono=True, bold=True)

# linked-list node: value part + pointer part with a dot
NW, NV, NH = 60, 40, 36
def node(x, y, v, tone='u'):
    fill, st, tc = {'u': ('var(--bg)', RULE_HI, TX), 'g': ('var(--sunk)', 'var(--rule)', GH), 'f': (TG, TG, ONF)}[tone]
    dot = ONF if tone == 'f' else (GH if tone == 'g' else MU)
    return (R(x, y, NW, NH, fill, st, 6, 1.2) + L(x + NV, y, x + NV, y + NH, st, 1)
            + T(x + NV / 2, y + NH / 2 + 5, esc(v), tc, mono=True, bold=tone != 'g')
            + '<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (x + NV + (NW - NV) / 2, y + NH / 2, dot))
def link(x1, y, x2, c=MU, sw=1.4):
    """arrow from the pointer dot of the node at x1 to the left edge of the node at x2 (same row y)"""
    return arrow(x1 + NV + (NW - NV) / 2, y + NH / 2, x2 - 1, y + NH / 2, c, sw, None, 6)
def none_lbl(x, y):
    return T(x + 4, y + NH / 2 + 4, 'None', FA, 'start', mono=True)


class Fig:
    def __init__(s, pre, aria, caption, lines=None, W=760, hold=3.2, cw=None):
        s.a = Anim(pre, W, 0, aria, caption, hold)
        s.code = None; s.X0 = 0; s.bars = [(0, 0, 0)]; s.objs = []
        if lines:
            cw = cw or max(260, 30 + max(len(l) for l in lines) * 6.6)
            s.code = Code2(0, 40, lines, cw); s.a.static(s.code.svg()); s.X0 = cw + 26
    def line(s, t, i): s.bars.append((t, 0, i * LH))
    def show(s, svg, t, hide=None, d=.35): s.a.show(svg, t, hide, d); return s
    def path(s, svg, pts, t0=0, appear=True, d=.6, hide=None): s.a.path(svg, pts, t0, appear, d, hide); return s
    def static(s, svg): s.a.static(svg); return s
    def text(s, x, y, txt, t, hide=None, c=TX, a='start', bold=False, mono=True, cls='sv-d'):
        return s.show(T(x, y, esc(txt), c, a, cls, mono, bold), t, hide)
    def render(s, h, W=None):
        for o in s.objs: o.emit()
        s.objs = []
        if s.code:
            s.a.path(s.code.bar(), sorted(s.bars, key=lambda b: b[0]), 0, appear=False, d=.35)
            h = max(h, s.code.y + s.code.h() + 8)
        s.a.h = h
        if W: s.a.w = W
        html = s.a.render()
        m = re.search(r'linear 1 forwards', html)
        TT = float(re.search(r'animation:\S+ ([\d.]+)s linear', html).group(1)) if m else 0
        return html, TT


def dump(name, figs):
    os.makedirs('/tmp/dsa', exist_ok=True)
    json.dump({k: v[0] for k, v in figs.items()}, open('/tmp/dsa/%s.json' % name, 'w'))
    json.dump({k: v[1] for k, v in figs.items()}, open('/tmp/dsa/%s.times.json' % name, 'w'))
    for k, v in figs.items(): print(k, '%.1fs' % v[1])


class Obj:
    """A thing that lives on the timeline: born, moves (slides), changes tone (crossfade), dies.
    draw(x, y, tone) -> svg drawn at absolute (x, y)."""
    def __init__(s, fig, draw, t, x, y, tone='u'):
        s.f, s.draw, s.ev = fig, draw, [(t, 0, 'born', x, y, tone)]; s.k = 1
        fig.objs.append(s)
    def _e(s, *e): s.ev.append((e[0], s.k) + e[1:]); s.k += 1; return s
    def move(s, t, x, y): return s._e(t, 'move', x, y)
    def tone(s, t, tone): return s._e(t, 'tone', tone)
    def die(s, t): return s._e(t, 'die')
    def emit(s):
        ev = sorted(s.ev, key=lambda e: (e[0], e[1]))
        t0, _, _, x, y, tone = ev[0]
        seg = dict(t0=t0, ox=x, oy=y, tone=tone, pts=[(0, 0, 0)])
        def close(hide):
            s.f.a.path(s.draw(seg['ox'], seg['oy'], seg['tone']), seg['pts'], seg['t0'], True, .6, hide)
        alive = True
        for e in ev[1:]:
            t, kind = e[0], e[2]
            if kind == 'move':
                x, y = e[3], e[4]; seg['pts'].append((t, x - seg['ox'], y - seg['oy']))
            elif kind == 'tone':
                close(t); seg = dict(t0=t, ox=x, oy=y, tone=e[3], pts=[(0, 0, 0)])
            elif kind == 'die':
                close(t); alive = False; break
        if alive: close(None)


def graph(f, gx, gy, gw, gh, xmax, ymax, curves, t, xt=(), yt=(), xl='n', yl='steps', dots=()):
    """Axes (origin bottom-left at gx, gy+gh) then curves drawing in one by one.
    curves = [(fn, label, colour, width, label_x)]."""
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
            yv = fn(v)
            pts.append((px(v), py(yv)))
            if yv > ymax: break
            v += xmax / 200
        d = 'M' + ' L'.join('%.1f %.1f' % p for p in pts)
        ex, ey = pts[-1]
        f.show('<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (d, c, sw)
               + T(ex + 8, (ey - 8) if ey > gy + gh - 12 else (ey + 4), lab, c, 'start', mono=True, bold=True), t + .8 + k * 1.0, d=.6)
    return px, py


def cdraw(v, w=CW, h=CH):
    def d(x, y, tone):
        return {'u': cellv, 'g': cellg, 'f': cellf}[tone](x, y, v, w, h)
    return d

class Row:
    """Array cells as Obj; index labels static under the slots."""
    def __init__(s, f, x0, y, vals, t0=.2, dt=.06, idx=True, w=CW, h=CH, pitch=None):
        s.f, s.x0, s.y, s.w, s.h = f, x0, y, w, h; s.p = pitch or (w + G)
        s.c = [Obj(f, cdraw(v, w, h), t0 + i * dt, s.x(i), y) for i, v in enumerate(vals)]
        s.v = list(vals)
        s.idx_hide = idx if isinstance(idx, dict) else {}
        if idx:
            for i in range(len(vals)): f.show(T(s.cx(i), y + h + 16, str(i), FA, cls='sv-s', mono=True), t0 + i * dt, s.idx_hide.get(i))
    def x(s, i): return s.x0 + i * s.p
    def cx(s, i): return s.x(i) + s.w / 2
    def ring(s, i, t, hide): s.f.show(ring(s.x(i), s.y, s.w, s.h), t, hide)


def _row_ext():
    def set_(s, i, v, t, tone='u'):
        """overwrite slot i: old object leaves, new value appears in place."""
        s.c[i].die(t); s.v[i] = v
        s.c[i] = Obj(s.f, cdraw(v, s.w, s.h), t, s.x(i), s.y, tone); return s.c[i]
    def fly(s, v, x, y, i, t, tone='u'):
        """a copy of v is born at (x, y) and slides into slot i, replacing what was there."""
        o = Obj(s.f, cdraw(v, s.w, s.h), t, x, y, tone); o.move(t + .3, s.x(i), s.y)
        if s.c[i] is not None: s.c[i].die(t + .9)
        s.c[i] = o; s.v[i] = v; return o
    def swap(s, i, j, t):
        s.c[i].move(t, s.x(j), s.y); s.c[j].move(t, s.x(i), s.y)
        s.c[i], s.c[j] = s.c[j], s.c[i]; s.v[i], s.v[j] = s.v[j], s.v[i]
    Row.set = set_; Row.fly = fly; Row.swap = swap
_row_ext()

def status(f, x, y, txt, t, hide=None, c=TX, bold=False):
    f.show(T(x, y, esc(txt), c, 'start', mono=True, bold=bold), t, hide)


def Ptr(f, name, t, cx, y, side='below', ln=14, c=None):
    """pointer arrow + label as a sliding Obj; position = the cell centre x / cell edge y."""
    def d(x, yy, tone):
        if side == 'below': return ptr_below(x, yy, name, ln)
        if side == 'above': return ptr_above(x, yy, name, ln)
        return ptr_left(x, yy, name, ln)
    return Obj(f, d, t, cx, y)

def Box(f, t, x, y, txt, w=None, h=24, tone='u', mono=True):
    """a small labelled box (dict entry, chip) as Obj"""
    w = w or 16 + len(str(txt)) * 7.4
    def d(xx, yy, tn):
        fill, st, tc = {'u': ('var(--bg)', RULE_HI, TX), 'g': ('var(--sunk)', 'var(--rule)', GH),
                        'f': (TG, TG, ONF), 'v': (vt('.10'), MID, TX)}[tn]
        return R(xx, yy, w, h, fill, st, 6, 1.2) + T(xx + w / 2, yy + h / 2 + 4.5, esc(txt), tc, mono=mono, bold=tn != 'g')
    o = Obj(f, d, t, x, y, tone); o.w = w; return o


def goal_on(f, x, y, txt, t, cx_to, cy_to=24, w=CW, h=CH, keep_ring=True, ring_hide=None):
    """known target: dashed ring on its cell, chip born above the cell then floats to (cx_to, cy_to)."""
    if keep_ring: f.show(goalring(x, y, w, h), t, ring_hide)
    cw = 24 + len(txt) * 6.6
    c = chip(x + w / 2, y - 30, txt, 'middle')
    f.path(c, [(0, 0, 0), (t + 1.2, cx_to - (x + w / 2 - cw / 2), cy_to - (y - 30))], t)

def goal_corner(f, x, txt, t, y=24):
    f.show(chip(x, y, txt), t)

def finish(f, x, y, txt, t):
    f.show(T(x, y, esc(txt), TG, 'start', mono=True, bold=True), t)
