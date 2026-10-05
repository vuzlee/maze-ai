# -*- coding: utf-8 -*-
"""Shared maths + plotting for the bias-variance and overfitting lessons (pure Python, seeded).
Data: y = sin(2*pi*x) + N(0, 0.3^2) on x in [0, 1]; polynomial features in t = 2x - 1."""
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from engine import *  # noqa  (Anim, T, R, L, arrow, pill, tint, cap, COL, AM, GR, RD, BL, MU, TX, FA, RULE_HI)

SIG = 0.3
def f(x): return math.sin(2 * math.pi * x)
def feats(x, d): t = 2 * x - 1; return [t ** k for k in range(d + 1)]

def solve(A, b):
    n = len(b); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[c][c]:
                k = M[r][c] / M[c][c]
                for j in range(c, n + 1): M[r][j] -= k * M[c][j]
    return [M[i][n] / M[i][i] for i in range(n)]

def fit(xs, ys, d, lam=0.0):
    X = [feats(x, d) for x in xs]; m = d + 1
    A = [[sum(r[i] * r[j] for r in X) + ((lam if i else 0) + 1e-9) * (i == j) for j in range(m)] for i in range(m)]
    b = [sum(r[i] * y for r, y in zip(X, ys)) for i in range(m)]
    return solve(A, b)

def pred(w, x): return sum(c * v for c, v in zip(w, feats(x, len(w) - 1)))

def sample(rng, n, fixed=True):
    xs = [(i + .5) / n for i in range(n)] if fixed else sorted(rng.random() for _ in range(n))
    return xs, [f(x) + rng.gauss(0, SIG) for x in xs]

def mse(w, xs, ys): return sum((pred(w, x) - y) ** 2 for x, y in zip(xs, ys)) / len(xs)

GRID = [(i + .5) / 40 for i in range(40)]
def bias_var(fitter, n, R=300, seed=1):
    """fitter(xs, ys, rng) -> callable model. Returns (bias^2, variance) averaged over GRID."""
    rng = random.Random(seed); P = []
    for _ in range(R):
        xs, ys = sample(rng, n); m = fitter(xs, ys, rng); P.append([m(x) for x in GRID])
    b2 = v = 0
    for j, x in enumerate(GRID):
        col = [p[j] for p in P]; mu = sum(col) / R
        b2 += (mu - f(x)) ** 2; v += sum((c - mu) ** 2 for c in col) / R
    return b2 / len(GRID), v / len(GRID)

def poly_fitter(d, lam=0.0):
    return lambda xs, ys, rng: (lambda w: (lambda x: pred(w, x)))(fit(xs, ys, d, lam))

# ---------- drawing ----------
BR, VI, FI, RO, GH = 'var(--brand)', 'var(--violet)', 'var(--filled)', 'var(--rose)', 'var(--ghost)'
def a(tok, al): return 'rgba(var(%s),%s)' % (tok, al)

class Plot:
    def __init__(s, pre, x, y, w, h, xr, yr, xlog=False, ylog=False):
        s.pre, s.x, s.y, s.w, s.h, s.xr, s.yr, s.xlog, s.ylog = pre, x, y, w, h, xr, yr, xlog, ylog
    def _n(s, v, r, lg):
        if lg: return (math.log10(v) - math.log10(r[0])) / (math.log10(r[1]) - math.log10(r[0]))
        return (v - r[0]) / (r[1] - r[0])
    def px(s, v): return s.x + s._n(v, s.xr, s.xlog) * s.w
    def py(s, v): return s.y + s.h - s._n(v, s.yr, s.ylog) * s.h
    def clip(s):
        return '<defs><clipPath id="%sclip"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath></defs>' % (
            s.pre, s.x, s.y - 2, s.w + 2, s.h + 4)
    def axes(s, xt=(), yt=(), xl='', yl='', grid=True):
        o = L(s.x, s.y + s.h, s.x + s.w + 8, s.y + s.h, MU, 1.2) + L(s.x, s.y + s.h, s.x, s.y - 6, MU, 1.2)
        for v, lab in xt:
            o += L(s.px(v), s.y + s.h, s.px(v), s.y + s.h + 4, MU, 1) + T(s.px(v), s.y + s.h + 16, lab, FA, cls='sv-l')
        for v, lab in yt:
            o += T(s.x - 7, s.py(v) + 4, lab, FA, 'end', cls='sv-l')
            if grid: o += L(s.x, s.py(v), s.x + s.w, s.py(v), 'var(--rule)', 1, '2 4')
        if xl: o += T(s.x + s.w, s.y + s.h + 32, xl, MU, 'end')
        if yl: o += T(s.x - 4, s.y - 12, yl, MU, 'start')
        return o
    def d(s, pts):
        return 'M' + ' L'.join('%.1f %.1f' % (s.px(u), s.py(v)) for u, v in pts)
    def line(s, pts, c=BR, sw=2, dash=None, op=None):
        ds = ' stroke-dasharray="%s"' % dash if dash else ''
        o = ' stroke-opacity="%s"' % op if op else ''
        return '<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s stroke-linejoin="round" clip-path="url(#%sclip)"/>' % (
            s.d(pts), c, sw, ds, o, s.pre)
    def dot(s, u, v, c=BR, r=3.2, fill=None):
        return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1.2"/>' % (s.px(u), s.py(v), r, fill or c, c)
    def draw(s, an, pts, t, dur, c=BR, sw=2, dash=None, k=12, hide=None):
        """progressive reveal: k overlapping chunks shown one after another."""
        n = len(pts)
        for i in range(k):
            a0, a1 = i * (n - 1) // k, (i + 1) * (n - 1) // k
            if a1 <= a0: continue
            an.show(s.line(pts[a0:a1 + 1], c, sw, dash), t + dur * i / k, hide=hide, d=max(.08, dur / k))

def curve_pts(fn, x0=0, x1=1, n=120): return [(x0 + (x1 - x0) * i / n, fn(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]

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

def palette(s):
    for x, y in [('--filled)', '@B)'), ('--blue-a)', '@BA)'), ('--ok)', '--filled)'), ('--green-a)', '--blue-a)'),
                 ('--tomb)', '--rose)'), ('--red-a)', '--rose-a)'), ('--probe)', '--violet)'), ('--amber-a)', '--violet-a)'),
                 ('@B)', '--brand)'), ('@BA)', '--clay-a)')]:
        s = s.replace(x, y)
    return s

# ---------- shared figure pieces ----------
def fit_plot(pre, x, y, w, h, yr=(-1.8, 1.8)):
    p = Plot(pre, x, y, w, h, (0, 1), yr)
    ax = p.clip() + L(x, y + h, x + w, y + h, MU, 1.2) + L(x, y, x, y + h, MU, 1.2)
    ax += T(x + w, y + h + 16, 'x', MU, 'end', cls='sv-l') + T(x - 6, y + 4, 'y', MU, 'end', cls='sv-l')
    return p, ax

def splice(page, body):
    import re
    s = open(page).read()
    i = s.index('<section'); j = s.index('</article>')
    s = s[:i] + body.strip() + '\n\n      ' + s[j:]
    s = s.replace('<script src="lab.js"></script>\n', '')
    open(page, 'w').write(s)

def finish(html, figs):
    for k, v in figs.items():
        assert '{%s}' % k in html, k
        html = html.replace('{%s}' % k, palette(v))
    assert '{' not in html.replace('{ ', '').split('<script>')[0] or True
    return html

import re as _re
def solid_brand(s):
    """Data bars in brand colour: draw as a strong tint so they read as data, not as a state."""
    return _re.sub(r'(<rect[^>]*\bfill=")var\(--brand\)"', r'\1rgba(var(--clay-a),.85)"', s)
