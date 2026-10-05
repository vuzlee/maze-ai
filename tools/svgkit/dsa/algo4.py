"""Shared helpers for the sorting / greedy / backtracking / dynamic-programming generators.
Same palette and shapes as binary_search.py; nothing here edits engine.py."""
import sys, os, json, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *  # noqa: F401,F403  (Anim, T, R, L, arrow, cap, tint, MU, TX, FA, RULE_HI)

PT, MID, TG, GH = 'var(--brand)', 'var(--violet)', 'var(--filled)', 'var(--ghost)'
ON = 'var(--on-fill)'
def vt(a): return 'rgba(var(--violet-a),%s)' % a
def it(a): return 'rgba(var(--blue-a),%s)' % a
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

LH = 20
class Code2:
    """Code box; one violet bar slides from line to line (see bar_path)."""
    def __init__(s, x, y, lines, w=None):
        s.x, s.y, s.lines = x, y, lines
        s.w = w or max(220, 30 + max(len(l) for l in lines) * 6.6)
    def svg(s):
        o = R(s.x, s.y, s.w, len(s.lines) * LH + 14, 'var(--bg)', RULE_HI, 8)
        for i, l in enumerate(s.lines):
            n = len(l) - len(l.lstrip())
            o += T(s.x + 14, s.y + 22 + i * LH, '\u00a0' * n + esc(l.lstrip()), TX, 'start', mono=True)
        return o
    def bar(s):
        return R(s.x + 4, s.y + 8, s.w - 8, LH, vt('.13'), 'none', 4) + R(s.x + 4, s.y + 8, 3, LH, MID, 'none', 1.5)
    def h(s): return len(s.lines) * LH + 14
    def run(s, f, steps, t0=0):
        """steps = [(t, line_index)] -> sliding bar."""
        pts = [(0, 0, steps[0][1] * LH)] + [(t, 0, i * LH) for t, i in steps]
        f.path(s.bar(), pts, t0, d=.3)

def box(x, y, v, w=40, h=36, st='n', small=False):
    cls = 'sv-s' if small else 'sv-d'
    if st == 'n':   return R(x, y, w, h, 'var(--bg)', RULE_HI, 6, 1.2) + T(x + w / 2, y + h / 2 + 4, esc(v), TX, cls=cls, mono=True, bold=True)
    if st == 'g':   return R(x, y, w, h, 'var(--sunk)', 'var(--rule)', 6, 1) + T(x + w / 2, y + h / 2 + 4, esc(v), GH, cls=cls, mono=True)
    if st == 'f':   return R(x, y, w, h, TG, TG, 6, 1.2) + T(x + w / 2, y + h / 2 + 4, esc(v), ON, cls=cls, mono=True, bold=True)
    if st == 'b':   return R(x, y, w, h, 'var(--bg)', 'none', 6) + R(x, y, w, h, it('.12'), TG, 6, 1.3) + T(x + w / 2, y + h / 2 + 4, esc(v), TG, cls=cls, mono=True, bold=True)
    if st == 'v':   return R(x, y, w, h, 'var(--bg)', 'none', 6) + R(x, y, w, h, vt('.12'), MID, 6, 1.4) + T(x + w / 2, y + h / 2 + 4, esc(v), MID, cls=cls, mono=True, bold=True)
    raise ValueError(st)

def ring(x, y, w=40, h=36, r=8): return R(x - 3, y - 3, w + 6, h + 6, vt('.10'), MID, r, 2.2)
def goal_ring(x, y, w=40, h=36): return R(x - 4, y - 4, w + 8, h + 8, 'none', TG, 8, 1.4, '4 3')
def ptr(cx, y, name, c=PT, ln=14):
    """pointer under a cell whose bottom is y: arrow up + label."""
    return arrow(cx, y + 6 + ln, cx, y + 4, c, 1.6, None, 6) + T(cx, y + ln + 19, name, c, mono=True, bold=True)
def ptr_up(cx, y, name, c=PT):
    """pointer above a cell whose top is y."""
    return T(cx, y - 22, name, c, mono=True, bold=True) + arrow(cx, y - 17, cx, y - 4, c, 1.6, None, 6)
def st(x, y, s, c=TX, bold=False, a='start'): return T(x, y, esc(s), c, a, mono=True, bold=bold)
def lab(x, y, s, c=MU, a='start', bold=False): return T(x, y, esc(s), c, a, bold=bold)
def idx(cx, y, i): return T(cx, y, str(i), FA, cls='sv-s', mono=True)
def chip(x, y, s, c=TG):
    w = 24 + len(s) * 6.9
    return R(x, y, w, 24, it('.12'), c, 12, 1.3) + T(x + 12, y + 16, esc(s), c, 'start', mono=True, bold=True)

def circ(cx, cy, r, fill, stroke, sw=1.3, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (cx, cy, r, fill, stroke, sw, d)
def node(cx, cy, s, kind='n', r=15):
    if kind == 'n': return circ(cx, cy, r, 'var(--bg)', RULE_HI, 1.3) + T(cx, cy + 4, esc(s), TX, mono=True, bold=True)
    if kind == 'g': return circ(cx, cy, r, 'var(--sunk)', 'var(--rule)', 1) + T(cx, cy + 4, esc(s), GH, mono=True)
    if kind == 'f': return circ(cx, cy, r, TG, TG, 1.3) + T(cx, cy + 4, esc(s), ON, mono=True, bold=True)
    if kind == 'b': return circ(cx, cy, r, 'var(--bg)', 'none') + circ(cx, cy, r, it('.12'), TG, 1.4) + T(cx, cy + 4, esc(s), TG, mono=True, bold=True)
    if kind == 'v': return circ(cx, cy, r, 'var(--bg)', 'none') + circ(cx, cy, r, vt('.12'), MID, 1.6) + T(cx, cy + 4, esc(s), MID, mono=True, bold=True)
    raise ValueError(kind)
def nring(cx, cy, r=15): return circ(cx, cy, r + 4, 'none', MID, 2.2)
def edge(x1, y1, x2, y2, c=RULE_HI, sw=1.4, r1=15, r2=15, dash=None, head=False):
    a = math.atan2(y2 - y1, x2 - x1)
    ax, ay = x1 + r1 * math.cos(a), y1 + r1 * math.sin(a)
    bx, by = x2 - r2 * math.cos(a), y2 - r2 * math.sin(a)
    return arrow(ax, ay, bx, by, c, sw, dash, 6) if head else L(ax, ay, bx, by, c, sw, dash)
def cross(cx, cy, s=6, c=GH, sw=2):
    return L(cx - s, cy - s, cx + s, cy + s, c, sw) + L(cx - s, cy + s, cx + s, cy - s, c, sw)
def pathd(pts): return 'M' + ' L'.join('%.1f %.1f' % p for p in pts)
def poly(pts, c, sw=2.4, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s/>' % (pathd(pts), c, sw, d)
def dot(cx, cy, c=MID, r=4): return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (cx, cy, r, c)

def axes(gx, gy, gw, gh, xt, yt, xl, yl, px, py):
    """axes with ticks; px/py map data -> svg."""
    o = L(gx, gy + gh, gx + gw + 10, gy + gh, MU, 1.2) + L(gx, gy + gh, gx, gy - 6, MU, 1.2)
    for v in xt: o += T(px(v), gy + gh + 16, str(v), FA, cls='sv-s', mono=True) + L(px(v), gy + gh, px(v), gy + gh + 4, MU, 1)
    for v in yt: o += T(gx - 8, py(v) + 4, str(v), FA, 'end', cls='sv-s', mono=True) + L(gx, py(v), gx + gw, py(v), 'var(--rule)', 1, '2 4')
    o += T(gx + gw + 14, gy + gh + 4, xl, MU, 'start', mono=True) + T(gx - 8, gy - 12, yl, MU, 'start', mono=True)
    return o

REPLAY = '''<script>
/* Figures start when first scrolled into view, play once and hold the last frame. Click a figure to replay. */
(function () {
  if (!window.IntersectionObserver || !document.getAnimations) return;
  var svgs = [].slice.call(document.querySelectorAll("figure svg[data-anim]"));
  if (!svgs.length) return;
  function anims(s) {
    return document.getAnimations().filter(function (a) { var t = a.effect && a.effect.target; return t && s.contains(t); });
  }
  function restart(s) { anims(s).forEach(function (a) { a.currentTime = 0; a.play(); }); }
  svgs.forEach(function (s) { anims(s).forEach(function (a) { a.pause(); a.currentTime = 0; }); });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting || e.target.__played) return;
      e.target.__played = true; restart(e.target); io.unobserve(e.target);
    });
  }, { threshold: 0.4 });
  svgs.forEach(function (s) {
    io.observe(s); s.style.cursor = "pointer";
    s.addEventListener("click", function () { restart(s); });
  });
})();
</script>'''

def splice(page, article_open, body, figs, footer):
    """Replace the whole <article> of page; <!--FIG:key--> in body -> figure html."""
    for k, v in figs.items():
        assert '<!--FIG:%s-->' % k in body, k
        body = body.replace('<!--FIG:%s-->' % k, v)
    assert '<!--FIG:' not in body
    s = open(page, encoding='utf-8').read()
    i = s.index('<article'); j = s.index('</article>')
    s = (s[:i] + article_open + '\n' + body.strip() + '\n\n' + REPLAY + '\n\n<footer>' + footer +
         '</footer>\n\n      ' + s[j:])
    s = s.replace('<script src="lab.js"></script>\n', '')
    assert 'lab.js' not in s
    open(page, 'w', encoding='utf-8').write(s)

class Arr:
    """A row of cells whose values can move between slots (swaps, reorders)."""
    def __init__(s, x0, y, vals, w=40, h=36, g=6, small=False):
        s.x0, s.y, s.vals, s.w, s.h, s.g, s.small = x0, y, list(vals), w, h, g, small
        s.slot = list(range(len(vals)))          # slot of element id
        s.mv = [[] for _ in vals]               # (t, slot)
    def xl(s, k): return s.x0 + k * (s.w + s.g)
    def cx(s, k): return s.xl(k) + s.w / 2
    def at(s, k): return s.slot.index(k)        # element id sitting in slot k
    def val(s, k): return s.vals[s.at(k)]
    def swap(s, t, k1, k2):
        a, b = s.at(k1), s.at(k2)
        if a == b: return
        s.slot[a], s.slot[b] = k2, k1
        s.mv[a].append((t, k2)); s.mv[b].append((t, k1))
    def place(s, t, order):
        """order = list of element ids, new slot = position in list"""
        for k, e in enumerate(order):
            if s.slot[e] != k: s.slot[e] = k; s.mv[e].append((t, k))
    def reserve(s, f): s._at = len(f.items)
    def commit(s, f, t0, idxs=True, step=.05, hide=None):
        """draw the moving cells; if reserve(f) was called, they go underneath later items."""
        at = getattr(s, '_at', None); keep = f.items[at:] if at is not None else []
        if at is not None: del f.items[at:]
        s._commit(f, t0, idxs, step, hide); f.items += keep
    def _commit(s, f, t0, idxs, step, hide):
        p = s.w + s.g
        for e, v in enumerate(s.vals):
            pts = [(0, 0, 0)] + [(t, (k - e) * p, 0) for t, k in s.mv[e]]
            f.path(box(s.xl(e), s.y, v, s.w, s.h, 'n', s.small), pts, t0 + e * step, d=.5, hide=hide)
        if idxs:
            for k in range(len(s.vals)): f.show(idx(s.cx(k), s.y + s.h + 16, k), t0 + k * step)
    def cell(s, k, st, t, hide=None, v=None):
        v = s.val(k) if v is None else v
        return box(s.xl(k), s.y, v, s.w, s.h, st, s.small)
    def ring(s, k1, k2=None):
        k2 = k1 if k2 is None else k2
        return ring(s.xl(k1), s.y, s.xl(k2) + s.w - s.xl(k1), s.h)

class Ptr:
    """Pointer that slides between slots of an Arr."""
    def __init__(s, arr, name, k, up=False, c=PT, ln=14):
        s.a, s.name, s.k0, s.up, s.c, s.ln = arr, name, k, up, c, ln
        s.pts = [(0, 0, 0)]
    def to(s, t, k): s.pts.append((t, (k - s.k0) * (s.a.w + s.a.g), 0))
    def commit(s, f, t0, hide=None):
        x = s.a.cx(s.k0)
        g = ptr_up(x, s.a.y, s.name, s.c) if s.up else ptr(x, s.a.y + s.a.h + (18 if s.up is False else 0), s.name, s.c, s.ln)
        f.path(g, s.pts, t0, d=.5, hide=hide)

def pad(figs, extra=14):
    """add bottom room to every figure (the last text line sits close to the edge); escape < > in aria-label."""
    import re
    out = {}
    for k, v in figs.items():
        v = re.sub(r'aria-label="([^"]*)"', lambda m: 'aria-label="%s"' % m.group(1).replace('<', '&lt;').replace('>', '&gt;'), v, count=1)
        out[k] = re.sub(r'viewBox="0 0 (\d+) (\d+)"', lambda m: 'viewBox="0 0 %s %d"' % (m.group(1), int(m.group(2)) + extra), v, count=1)
    return out
