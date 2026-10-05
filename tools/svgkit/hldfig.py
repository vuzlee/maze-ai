# -*- coding: utf-8 -*-
"""Animated HLD (high-level design) figures for the distributed-systems shelf.

Same notation and timeline engine as tablefig.py (classical-ML style), plus:
  icon     user · client · server · db · cache · lb · queue · topic · cdn · worker
  ring     amber dashed box around the node that is working *now*
  packet   a labelled pill that travels along a link, then vanishes (or stays)
  trail    the link the packet used, drawn in colour once it has been used
  steps    the execution-order strip along the bottom, one box per step, revealed in time

Geometry: an icon at (cx, y) occupies cx±22 × y..y+48, its label sits at y+62 (sub at y+76).
Link anchors: right edge (cx+28, y+24), left edge (cx-28, y+24).
"""
import math
from tablefig import *          # noqa: F401,F403  (Fig, T, R, L, arrow, pill, leader, callout, cap, note, tint, COL …)

TONES = {None: ('var(--bg)', MU), 'gr': (tint('gr', '.18'), GR), 'rd': (tint('rd', '.18'), RD),
         'am': (tint('am', '.18'), AM), 'bl': (tint('bl', '.16'), BL), 'off': ('var(--sunk)', RULE_HI)}


def _shape(kind, cx, y, f, s):
    w = 'stroke-width="1.6"'
    if kind == 'user':
        return ('<circle cx="%.1f" cy="%.1f" r="9" fill="%s" stroke="%s" %s/>' % (cx, y + 12, f, s, w) +
                '<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" fill="%s" stroke="%s" %s/>'
                % (cx - 17, y + 44, cx - 17, y + 24, cx, y + 24, cx + 17, y + 24, cx + 17, y + 44, f, s, w))
    if kind == 'client':
        return (R(cx - 26, y + 6, 52, 36, f, s, 4, 1.6) + L(cx - 26, y + 15, cx + 26, y + 15, s, 1.6) +
                ''.join('<circle cx="%.1f" cy="%.1f" r="1.6" fill="%s"/>' % (cx - 20 + i * 6, y + 10.5, s) for i in range(3)))
    if kind == 'server':
        g = R(cx - 22, y + 2, 44, 44, f, s, 4, 1.6) + L(cx - 22, y + 16.6, cx + 22, y + 16.6, s, 1.6) + L(cx - 22, y + 31.3, cx + 22, y + 31.3, s, 1.6)
        for i in range(3):
            yy = y + 9.5 + i * 14.7
            g += '<circle cx="%.1f" cy="%.1f" r="2" fill="%s"/>' % (cx + 14, yy, s) + L(cx - 15, yy, cx + 2, yy, s, 1.2)
        return g
    if kind == 'db':
        return ('<path d="M%.1f %.1f V%.1f A22 7 0 0 0 %.1f %.1f V%.1f" fill="%s" stroke="%s" %s/>' % (cx - 22, y + 8, y + 40, cx + 22, y + 40, y + 8, f, s, w) +
                '<ellipse cx="%.1f" cy="%.1f" rx="22" ry="7" fill="%s" stroke="%s" %s/>' % (cx, y + 8, f, s, w) +
                '<path d="M%.1f %.1f A22 7 0 0 0 %.1f %.1f" fill="none" stroke="%s" %s/>' % (cx - 22, y + 24, cx + 22, y + 24, s, w))
    if kind == 'cache':
        return (R(cx - 22, y + 2, 44, 44, f, s, 10, 1.6) +
                '<path d="M%.1f %.1f L%.1f %.1f H%.1f L%.1f %.1f L%.1f %.1f H%.1f Z" fill="%s"/>'
                % (cx + 4, y + 9, cx - 9, y + 27, cx, cx - 4, y + 40, cx + 10, y + 20, cx + 1, s))
    if kind == 'lb':
        c = y + 24
        return ('<circle cx="%.1f" cy="%.1f" r="22" fill="%s" stroke="%s" %s/>' % (cx, c, f, s, w) +
                '<path d="M%.1f %.1f H%.1f M%.1f %.1f L%.1f %.1f M%.1f %.1f H%.1f M%.1f %.1f L%.1f %.1f" stroke="%s" '
                'stroke-width="2" fill="none" stroke-linecap="round"/>'
                % (cx - 13, c, cx - 2, cx - 2, c, cx + 11, c - 9, cx - 2, c, cx + 13, cx - 2, c, cx + 11, c + 9, s))
    if kind in ('queue', 'topic'):
        g = R(cx - 42, y + 10, 84, 28, f, s, 14, 1.6)
        g += ''.join(R(cx - 30 + i * 21, y + 17, 15, 14, 'var(--bg)', s, 2, 1.2) for i in range(3))
        if kind == 'topic':
            g += '<path d="M%.1f %.1f l8 -8 M%.1f %.1f h10 M%.1f %.1f l8 8" stroke="%s" %s fill="none"/>' % (
                cx + 42, y + 24, cx + 42, y + 24, cx + 42, y + 24, s, w)
        return g
    if kind == 'cdn':
        return ('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f '
                'Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" fill="%s" stroke="%s" %s/>' % (
                    cx - 22, y + 40, cx - 32, y + 40, cx - 32, y + 30, cx - 32, y + 19, cx - 20, y + 20, cx - 16, y + 6, cx - 1, y + 8,
                    cx + 12, y + 2, cx + 18, y + 16, cx + 31, y + 16, cx + 31, y + 29, cx + 31, y + 40, cx + 20, y + 40, f, s, w))
    if kind == 'worker':
        c = y + 24
        pts = []
        for i in range(32):
            a = math.radians(i * 11.25)
            r = 21 if (i % 4) in (0, 1) else 15
            pts.append('%.1f,%.1f' % (cx + r * math.cos(a), c + r * math.sin(a)))
        return ('<polygon points="%s" fill="%s" stroke="%s" %s/>' % (' '.join(pts), f, s, w) +
                '<circle cx="%.1f" cy="%.1f" r="6" fill="var(--sunk)" stroke="%s" %s/>' % (cx, c, s, w))
    raise ValueError(kind)


def icon(kind, cx, y, label='', tone=None, sub=None, side=False, wipe=False, lc=None):
    """One HLD icon. tone recolours it; wipe also blanks the label area (use when the label changes)."""
    f, s = TONES[tone]
    lc = lc or (s if tone in ('rd', 'am', 'gr') else TX)
    bw = 100 if kind in ('queue', 'topic') else 64
    g = R(cx - bw / 2, y - 2, bw, 52, 'var(--sunk)', 'none', 0)
    if wipe:   # blank a generous label area so any earlier, longer label is fully hidden
        if side:
            g += R(cx + 28, y + 6, 150, 40, 'var(--sunk)', 'none', 0)
        else:
            g += R(cx - 70, y + 50, 140, 32, 'var(--sunk)', 'none', 0)
    g += _shape(kind, cx, y, f, s)
    if side:
        if label:
            g += T(cx + 32, y + (22 if sub else 29), label, lc, 'start', 'sv-s')
        if sub:
            g += T(cx + 32, y + 38, sub, MU, 'start', 'sv-l')
    else:
        if label:
            g += T(cx, y + 62, label, lc, 'middle', 'sv-s')
        if sub:
            g += T(cx, y + 76, sub, MU, 'middle', 'sv-l')
    return g


def ring(cx, y, w=64, h=56, c=AM):
    return R(cx - w / 2, y - 4, w, h, 'none', c, 10, 1.6, '4 3')


def mid(cx, y):
    return cx, y + 24


def link(x1, y1, x2, y2, dash=None):
    return L(x1, y1, x2, y2, RULE_HI, 1.2, dash)


def shape(kind, cx, y, tone=None):
    f, s = TONES[tone]
    return _shape(kind, cx, y, f, s)


def packet(f, x1, y1, x2, y2, text, t, tone='bl', dur=.8, keep=False, w=None):
    """A pill centred on (x2, y2) that slides in from (x1, y1)."""
    f(pill(x2, y2 - 10, text, tone, w), show=t, hide=None if keep else t + dur + .15,
      move=(t, x1 - x2, y1 - y2, dur), d=.2)
    return t + dur


def trail(f, x1, y1, x2, y2, t, c=BL, dash=None):
    f(arrow(x1, y1, x2, y2, c, 1.5, dash), show=t, d=.3)


def send(f, x1, y1, x2, y2, text, t, tone='bl', dur=.8, w=None, dash=None):
    """A message: the arrow draws in, a labelled packet rides along it and disappears on arrival.
    The arrow stays, so the final frame still shows who talked to whom. Returns the arrival time."""
    c = COL[tone] if tone else MU
    f(arrow(x1, y1, x2, y2, c, 1.5, dash), show=t, d=.25)
    ang = math.atan2(y2 - y1, x2 - x1)
    ex, ey = x2 - 34 * math.cos(ang), y2 - 34 * math.sin(ang)
    sx, sy = x1 + 34 * math.cos(ang), y1 + 34 * math.sin(ang)
    f(pill(ex, ey - 22, text, tone, w), show=t, hide=t + dur + .1, move=(t, sx - ex, sy - ey, dur), d=.15)
    return t + dur


def xmark(cx, cy, t, f, text=None):
    f(T(cx, cy + 5, '✕', RD, 'middle', 'sv-s') + (T(cx + 10, cy + 5, text, RD, 'start') if text else ''), show=t)


def steps(f, y, items, times, w=700, x=0, gap=22, caption='step by step'):
    n = len(items)
    bw = (w - (n - 1) * gap) / n
    f(T(x, y + 10, caption, MU, 'start'))
    for k, ((lab, val), t) in enumerate(zip(items, times)):
        bx = x + k * (bw + gap)
        last = k == n - 1
        s = R(bx, y + 18, bw, 40, tint('am', '.14') if last else 'var(--bg)', AM if last else RULE_HI, 6, 1.4 if last else 1)
        s += T(bx + bw / 2, y + 34, lab, MU) + T(bx + bw / 2, y + 50, val, AM if last else TX)
        if k:
            s = arrow(bx - gap + 4, y + 38, bx - 4, y + 38, FA, 1.2, None, 6) + s
        f(s, show=t)


def frame(x, y, w, h, t):
    return R(x, y, w, h, 'none', RULE_HI, 10, 1, '6 4') + T(x + 12, y + 16, t, MU, 'start', 'sv-hv')


def cut(x, y1, y2, label='✂ partition'):
    return L(x, y1, x, y2, RD, 2, '5 4') + T(x, y1 - 6, label, RD, 'middle')
