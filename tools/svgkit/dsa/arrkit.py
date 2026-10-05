"""Shared helpers for the two-pointers, sliding-window, prefix-sum and intervals generators.
Builds on engine.py (Anim timeline). Palette as in binary_search.py:
--brand pointers · --violet probe ring + running code line · --filled goal / answer ·
--sunk + --ghost discarded · --bg + --rule-hi untouched."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Anim, T, R, L, arrow, cap, RULE_HI, TX, FA, MU  # noqa: F401

PT, MID, TG, GH, ON = 'var(--brand)', 'var(--violet)', 'var(--filled)', 'var(--ghost)', 'var(--on-fill)'
def vt(a): return 'rgba(var(--violet-a),%s)' % a
def it(a): return 'rgba(var(--blue-a),%s)' % a
def pt_(a): return 'rgba(var(--clay-a),%s)' % a
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
NB = ' '

LH = 20
CW, CH, G = 42, 36, 6
P = CW + G

class Code2:
    """code box on the left; one violet bar slides line to line (at(t, i) then emit)."""
    def __init__(s, x, y, lines, w=None):
        s.x, s.y, s.lines = x, y, lines
        s.w = w or max(250, 30 + max(len(l) for l in lines) * 6.7)
        s.pts = None
    def svg(s):
        o = R(s.x, s.y, s.w, s.h(), 'var(--bg)', RULE_HI, 8)
        for i, l in enumerate(s.lines):
            o += T(s.x + 14, s.y + 22 + i * LH, esc(l).replace(' ', NB), TX, 'start', mono=True)
        return o
    def h(s): return len(s.lines) * LH + 14
    def bar(s): return R(s.x + 4, s.y + 8, s.w - 8, LH, vt('.13'), 'none', 4) + R(s.x + 4, s.y + 8, 3, LH, MID, 'none', 1.5)
    def at(s, t, i):
        if s.pts is None: s.pts = [(0, 0, i * LH)]; s.t0 = t
        else: s.pts.append((t, 0, i * LH))
    def emit(s, f): f.path(s.bar(), s.pts, s.t0, d=.3)

def box(x, y, v, kind='n', w=CW, h=CH):
    """n untouched · g discarded · f answer (solid) · b kept/seen (tinted) · v probed (violet tint)"""
    fill, st, c, sw = {'n': ('var(--bg)', RULE_HI, TX, 1.2), 'g': ('var(--sunk)', 'var(--rule)', GH, 1),
                       'f': (TG, TG, ON, 1.2), 'b': (it('.12'), TG, TG, 1.3), 'v': (vt('.12'), MID, MID, 1.3)}[kind]
    back = R(x, y, w, h, 'var(--bg)', 'none', 6) if kind in 'bv' else ''
    return back + R(x, y, w, h, fill, st, 6, sw) + T(x + w / 2, y + h / 2 + 5, esc(v), c, mono=True, bold=kind != 'g')
def ring(x, y, w=CW, h=CH): return R(x - 3, y - 3, w + 6, h + 6, vt('.10'), MID, 8, 2.2)
def goal_ring(x, y, w=CW, h=CH): return R(x - 4, y - 4, w + 8, h + 8, 'none', TG, 8, 1.4, '4 3')
def idx(cx, y, i): return T(cx, y, str(i), FA, cls='sv-s', mono=True)
def st(x, y, s, c=TX, bold=False, a='start'): return T(x, y, esc(s), c, a, mono=True, bold=bold)
def lab(x, y, s, c=MU, a='start', bold=False): return T(x, y, esc(s), c, a, bold=bold)
def chip(x, y, s, c=TG):
    w = 24 + len(s) * 7
    return R(x, y, w, 24, 'var(--bg)', 'none', 12) + R(x, y, w, 24, it('.12'), c, 12, 1.3) + T(x + w / 2, y + 16, esc(s), c, mono=True, bold=True)
def chipw(s): return 24 + len(s) * 7
def ptr_dn(cx, y, name, c=PT, ln=14):
    """pointer under a cell whose bottom is y: arrow up + label under it."""
    return arrow(cx, y + ln + 4, cx, y + 3, c, 1.6, None, 6) + T(cx, y + ln + 17, name, c, mono=True, bold=True)
def ptr_up(cx, y, name, c=PT, ln=14):
    """pointer above a cell whose top is y."""
    return T(cx, y - ln - 8, name, c, mono=True, bold=True) + arrow(cx, y - ln - 3, cx, y - 3, c, 1.6, None, 6)
def circ(cx, cy, r, fill, stroke='none', sw=1.3, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (cx, cy, r, fill, stroke, sw, d)
def pathd(pts): return 'M' + ' L'.join('%.1f %.1f' % p for p in pts)
def poly(pts, c, sw=2.4, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s/>' % (pathd(pts), c, sw, d)
def dot(cx, cy, c=MID, r=4): return circ(cx, cy, r, c)
def bracket(x1, x2, y, c=TG, up=False, sw=1.6):
    k = -5 if up else 5
    return L(x1, y, x2, y, c, sw) + L(x1, y - k, x1, y, c, sw) + L(x2, y - k, x2, y, c, sw)

def axes(gx, gy, gw, gh, xt, yt, xl, yl, px, py):
    o = L(gx, gy + gh, gx + gw + 10, gy + gh, MU, 1.2) + L(gx, gy + gh, gx, gy - 6, MU, 1.2)
    for v in xt: o += T(px(v), gy + gh + 16, str(v), FA, cls='sv-s', mono=True) + L(px(v), gy + gh, px(v), gy + gh + 4, MU, 1)
    for v in yt: o += T(gx - 8, py(v) + 4, str(v), FA, 'end', cls='sv-s', mono=True) + L(gx, py(v), gx + gw, py(v), 'var(--rule)', 1, '2 4')
    o += T(gx + gw + 14, gy + gh + 4, xl, MU, 'start', mono=True) + T(gx - 8, gy - 12, yl, MU, 'start', mono=True)
    return o

class Row:
    """a row of cells at x0,y."""
    def __init__(s, x0, y, vals, w=CW, h=CH, g=G):
        s.x0, s.y, s.vals, s.w, s.h, s.g = x0, y, list(vals), w, h, g
    def xl(s, i): return s.x0 + i * (s.w + s.g)
    def cx(s, i): return s.xl(i) + s.w / 2
    def right(s): return s.xl(len(s.vals) - 1) + s.w
    def draw(s, f, t0, step=.05, idxs=True, idx0=0):
        for i, v in enumerate(s.vals):
            f.show(box(s.xl(i), s.y, v, 'n', s.w, s.h) + (idx(s.cx(i), s.y + s.h + 16, i + idx0) if idxs else ''), t0 + i * step)
    def cell(s, i, kind, v=None): return box(s.xl(i), s.y, s.vals[i] if v is None else v, kind, s.w, s.h)
    def ring(s, i, j=None):
        j = i if j is None else j
        return ring(s.xl(i), s.y, s.xl(j) + s.w - s.xl(i), s.h)
    def goal(s, i, j=None):
        j = i if j is None else j
        return goal_ring(s.xl(i), s.y, s.xl(j) + s.w - s.xl(i), s.h)
    def band(s, i, j, c=PT, a='.10'):
        """window frame around cells i..j (drawn behind? no: a frame only, transparent)."""
        return R(s.xl(i) - 5, s.y - 5, s.xl(j) + s.w - s.xl(i) + 10, s.h + 10, 'none', c, 9, 2)

class Ptr:
    """pointer that slides between cells of a Row."""
    def __init__(s, row, name, k, up=False, c=PT, ln=14, dy=0):
        s.r, s.name, s.k0, s.up, s.c, s.ln, s.dy = row, name, k, up, c, ln, dy
        s.pts = [(0, 0, 0)]
    def to(s, t, k): s.pts.append((t, (k - s.k0) * (s.r.w + s.r.g), 0))
    def emit(s, f, t0, hide=None):
        x = s.r.cx(s.k0)
        g = ptr_up(x, s.r.y - s.dy, s.name, s.c, s.ln) if s.up else ptr_dn(x, s.r.y + s.r.h + 20 + s.dy, s.name, s.c, s.ln)
        f.path(g, s.pts, t0, d=.5, hide=hide)

def states(f, seq, end=None):
    """seq = [(t, svg)], each shown until the next one starts; the last until end (None = stays)."""
    for k, (t, s) in enumerate(seq):
        h = seq[k + 1][0] if k + 1 < len(seq) else end
        f.show(s, t, hide=h - .05 if h is not None else None, d=.3)

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

def splice(page, orig, article_open, body, figs, footer, meta_desc=None):
    """rebuild the <article> of page from the saved original; <!--FIG:k--> -> figure html."""
    for k, v in figs.items():
        assert '<!--FIG:%s-->' % k in body, k
        body = body.replace('<!--FIG:%s-->' % k, v)
    assert '<!--FIG:' not in body
    s = open(orig, encoding='utf-8').read()
    i = s.index('<article'); j = s.index('</article>')
    s = (s[:i] + article_open + '\n' + body.strip() + '\n\n' + REPLAY + '\n\n<footer>' + footer +
         '</footer>\n\n      ' + s[j:])
    s = s.replace('<script src="lab.js"></script>\n', '')
    assert 'lab.js' not in s
    open(page, 'w', encoding='utf-8').write(s)
