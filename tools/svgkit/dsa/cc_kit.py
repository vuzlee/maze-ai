# -*- coding: utf-8 -*-
"""Shared helpers for the ML core-concepts figures (supervised-unsupervised, train-val-test-cv,
feature-engineering). Built on tablefig.Fig; tones are written in tablefig names and mapped to the
analogous palette by palette(): 'am' -> --violet (looked at now), 'gr' -> --filled (result),
'bl' -> --brand (data), 'rd' -> --rose (wrong)."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from tablefig import *  # noqa
from nosql_data_overview import palette  # noqa

GHOST = 'var(--ghost)'
SUNK = 'var(--sunk)'

def dot(x, y, tone=None, r=5.5, hollow=False):
    if tone is None:
        return '<circle cx="%.1f" cy="%.1f" r="%s" fill="var(--bg)" stroke="%s" stroke-width="1.4"/>' % (x, y, r, FA)
    if tone == 'off':
        return '<circle cx="%.1f" cy="%.1f" r="%s" fill="var(--sunk)" stroke="%s" stroke-width="1.2"/>' % (x, y, r, GHOST)
    fill = 'var(--bg)' if hollow else tint(tone, '.55')
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, y, r, fill, COL[tone])

def ring(x, y, r=11, c=AM, dash='3 3'):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="%s"/>' % (x, y, r, c, dash)

def path(pts, c=BL, sw=2, dash=None, fill='none'):
    d = 'M' + ' L'.join('%.1f %.1f' % p for p in pts)
    da = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (d, fill, c, sw, da)

class Plot:
    """Axes box: data (xr, yr) -> pixels inside (x0, y0, w, h)."""
    def __init__(s, x0, y0, w, h, xr, yr):
        s.x0, s.y0, s.w, s.h, s.xr, s.yr = x0, y0, w, h, xr, yr
    def px(s, x): return s.x0 + (x - s.xr[0]) / (s.xr[1] - s.xr[0]) * s.w
    def py(s, y): return s.y0 + s.h - (y - s.yr[0]) / (s.yr[1] - s.yr[0]) * s.h
    def p(s, x, y): return (s.px(x), s.py(y))
    def axes(s, xl='', yl='', xt=(), yt=()):
        b = s.y0 + s.h
        o = L(s.x0, b, s.x0 + s.w, b, RULE_HI, 1.2) + L(s.x0, s.y0, s.x0, b, RULE_HI, 1.2)
        if xl: o += T(s.x0 + s.w, b + 30 if xt else b + 16, xl, MU, 'end')
        if yl: o += T(s.x0 + 6, s.y0 - 6, yl, MU, 'start')
        for v, lab in xt:
            o += L(s.px(v), b, s.px(v), b + 4, RULE_HI) + T(s.px(v), b + 15, lab, FA)
        for v, lab in yt:
            o += L(s.x0 - 4, s.py(v), s.x0, s.py(v), RULE_HI) + T(s.x0 - 7, s.py(v) + 4, lab, FA, 'end')
        return o
    def curve(s, f, a, b, n=80, c=GR, sw=2.4, dash=None):
        return path([s.p(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)], c, sw, dash)

def status(x, y, t, c=TX):
    return R(x - 2, y - 13, 330, 18, 'var(--bg)', 'none') + T(x, y, t, c, 'start', 'sv-s')

def splice(page, figs):
    s = open(page).read()
    for i, svg in enumerate(figs, 1):
        svg = palette(svg)
        assert '--probe' not in svg and '--ok)' not in svg and '--tomb' not in svg
        s, n = re.subn(r'<!--FIG%d-->.*?<!--/FIG%d-->' % (i, i),
                       lambda m: '<!--FIG%d-->\n%s\n<!--/FIG%d-->' % (i, svg, i), s, flags=re.S)
        assert n == 1, (page, i)
    open(page, 'w').write(s)
