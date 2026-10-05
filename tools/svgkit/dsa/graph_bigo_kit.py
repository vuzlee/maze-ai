"""Shared helpers for the graph / shortest-path / big-O DSA figures.
Builds on engine.py (Anim, Code bar idea from binary_search.py). Owned by those three lessons."""
import sys, os, json, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *
import engine as _engine
_T0 = T
def T(x, y, s, *a, **k):
    s = str(s).replace('&', '&amp;').replace('<', '&lt;') if '<' in str(s) and not str(s).lstrip().startswith('<') else s
    return _T0(x, y, s, *a, **k)

PT, MID, TG = 'var(--brand)', 'var(--violet)', 'var(--filled)'
GH = 'var(--ghost)'
def vt(a): return 'rgba(var(--violet-a),%s)' % a
def it(a): return 'rgba(var(--blue-a),%s)' % a
NR = 17
LH = 20
CH = 6.6   # mono char width at sv-d size

def circ(x, y, r, fill, stroke='none', sw=1, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, r, fill, stroke, sw, d)

def node(x, y, lab, st='plain', r=NR):
    fill, stroke, tc, sw = {
        'plain': ('var(--bg)', RULE_HI, TX, 1.3),
        'seen': (it('.14'), TG, TG, 1.6),
        'grey': ('var(--sunk)', 'var(--rule)', GH, 1),
        'ans': (TG, TG, 'var(--on-fill)', 1.6)}[st]
    return circ(x, y, r, 'var(--bg)') + circ(x, y, r, fill, stroke, sw) + T(x, y + 4.5, str(lab), tc, mono=True, bold=True)

def ring(x, y, r=NR + 5):
    return circ(x, y, r, vt('.10'), MID, 2.2)

def goal_ring(x, y, r=NR + 5):
    return circ(x, y, r, 'none', TG, 1.4, '4 3')

def seg(p, q, r1=NR, r2=NR):
    (x1, y1), (x2, y2) = p, q
    d = math.hypot(x2 - x1, y2 - y1) or 1
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return x1 + ux * r1, y1 + uy * r1, x2 - ux * r2, y2 - uy * r2

def edge(p, q, c=RULE_HI, sw=1.4, directed=False, dash=None, r=NR):
    x1, y1, x2, y2 = seg(p, q, r, r + (1 if directed else 0))
    if directed: return arrow(x1, y1, x2, y2, c, sw, dash, 7)
    return L(x1, y1, x2, y2, c, sw, dash)

def wlab(p, q, w, c=MU, off=(0, 0), wide=None):
    x, y = (p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1]
    s = str(w).replace('-', '−'); bw = wide or 8 + len(s) * 6.6
    return R(x - bw / 2, y - 8, bw, 16, 'var(--sunk)', 'none', 4) + T(x, y + 4, s, c, cls='sv-s', mono=True, bold=True)

def badge(x, y, txt, c=TG, dy=-NR - 8):
    w = 14 + len(str(txt)) * 7.6
    return R(x - w / 2, y + dy - 12, w, 16, 'var(--bg)', c, 8, 1) + T(x, y + dy, str(txt), c, cls='sv-s', mono=True, bold=True)

def chip(x, y, txt, c=TG, a='middle', solid=False):
    w = 24 + len(txt) * 7.5
    x0 = x - w / 2 if a == 'middle' else x
    if solid: return R(x0, y, w, 24, c, c, 12, 1.3) + T(x0 + w / 2, y + 16.5, txt, 'var(--on-fill)', mono=True, bold=True)
    return R(x0, y, w, 24, 'var(--bg)', 'none', 12) + R(x0, y, w, 24, it('.12'), c, 12, 1.3) + T(x0 + w / 2, y + 16.5, txt, c, mono=True, bold=True)

def box(x, y, v, st='plain', w=40, h=32, small=False):
    fill, stroke, tc, sw = {
        'plain': ('var(--bg)', RULE_HI, TX, 1.2),
        'seen': (it('.14'), TG, TG, 1.4),
        'grey': ('var(--sunk)', 'var(--rule)', GH, 1),
        'ans': (TG, TG, 'var(--on-fill)', 1.4),
        'pt': ('var(--bg)', PT, PT, 1.4)}[st]
    return R(x, y, w, h, 'var(--bg)', 'none', 6) + R(x, y, w, h, fill, stroke, 6, sw) + T(x + w / 2, y + h / 2 + 4.5, str(v), tc, cls='sv-s' if small else 'sv-d', mono=True, bold=st != 'grey')

def bring(x, y, w=40, h=32):
    return R(x - 3, y - 3, w + 6, h + 6, vt('.10'), MID, 8, 2.2)

class Code2:
    def __init__(s, x, y, lines, w=None):
        s.x, s.y, s.lines = x, y, lines
        s.w = w or 28 + max(len(l) for l in lines) * CH
    def svg(s):
        o = R(s.x, s.y, s.w, len(s.lines) * LH + 14, 'var(--bg)', RULE_HI, 8)
        for i, l in enumerate(s.lines):
            n = len(l) - len(l.lstrip())
            o += T(s.x + 14, s.y + 22 + i * LH, '\u00a0' * n + l.lstrip().replace('>', '&gt;'), TX, 'start', mono=True)
        return o
    def bar(s): return R(s.x + 4, s.y + 8, s.w - 8, LH, vt('.13'), 'none', 4) + R(s.x + 4, s.y + 8, 3, LH, MID, 'none', 1.5)
    def h(s): return len(s.lines) * LH + 14

class Story:
    """Timeline with keyed states: showing a new version of a key hides the previous one."""
    def __init__(s, pre, w, aria, caption, hold=3.2):
        s.f = Anim(pre, w, 0, aria, caption, hold)
        s.items = []; s.cur = {}; s.code = None; s.bar = []; s.paths = []; s.statics = []
        s.sx, s.sy = 0, 0
    def static(s, svg): s.items.append([svg, None, None, .35]); return s
    def at(s, t, svg, key=None, hide=None, d=.35):
        if key is not None and key in s.cur and s.cur[key][2] is None:
            prev = s.cur[key]
            prev[2] = max(t - .3, prev[1] + prev[3] + .01) if prev[1] is not None else t - .3
        it_ = [svg, t, hide, d]; s.items.append(it_)
        if key is not None: s.cur[key] = it_
        return it_
    def off(s, key, t):
        if key in s.cur and s.cur[key][2] is None: s.cur[key][2] = t
    def path(s, svg, pts, t0, hide=None, appear=True, d=.6):
        s.items.append(('path', svg, pts, t0, hide, appear, d))
    def setcode(s, x, y, lines, w=None):
        s.code = Code2(x, y, lines, w); s.static(s.code.svg()); s.bar = [(0, 0, 0)]; return s.code
    def line(s, t, i): s.bar.append((t, 0, i * LH))
    def say(s, t, txt, row=0, c=TX, bold=False, hide=None, a='start', x=None):
        x0 = s.sx if x is None else x
        bw = getattr(s, 'sw', None) or (s.f.w - x0 if a == 'start' else s.f.w)
        back = R(x0 - 2, s.sy + row * 22 - 15, bw, 21, 'var(--sunk)', 'none', 0) if s.f.w else ''
        return s.at(t, back + T(x0, s.sy + row * 22, txt, c, a, mono=True, bold=bold), key='say%d' % row, hide=hide)
    def num(s, t, x, y, txt, key, c=PT):
        back = R(x - 2, y - 15, 10 + len(str(txt)) * 9, 21, 'var(--sunk)', 'none', 0)
        return s.at(t, back + T(x, y, str(txt), c, 'start', mono=True, bold=True), key=key)
    def render(s, h):
        for x in s.items:
            if x[0] == 'path':
                _, svg, pts, t0, hide, appear, d = x
                s.f.path(svg, pts, t0, appear, d, hide)
            elif x[1] is None: s.f.static(x[0])
            else: s.f.show(x[0], x[1], x[2], x[3])
        if s.code is not None and len(s.bar) > 1:
            s.f.path(s.code.bar(), s.bar, 0, appear=False, d=.3)
        s.f.h = h
        return s.f.render()

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

def splice(page, article):
    """Replace the whole <article>…</article> and drop lab.js."""
    h = open(page, encoding='utf-8').read()
    a, b = h.index('<article'), h.index('</article>') + len('</article>')
    h = h[:a] + article + h[b:]
    h = h.replace('<script src="lab.js"></script>\n', '').replace('<script src="lab.js"></script>', '')
    open(page, 'w', encoding='utf-8').write(h)
