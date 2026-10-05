# -*- coding: utf-8 -*-
"""Animated figures built from tables — the visual language of the classical-ML lessons
(knn, logistic-regression, naive-bayes), reusable for any table-shaped topic (SQL first).

Notation
  caption   one uppercase muted line at the top (sv-hv)
  table     centred cells, muted header (+ optional second header line for a type or formula),
            a rule under the header, rows as rounded rects on the sunk figure background
  outline   amber box around the rows / cells being looked at right now
  pill      rounded result chip; colour = meaning (green kept/true, red rejected/false,
            amber pointer/null/unknown, blue data)
  leader    dashed line from a cell to a short coloured note
  query     SQL lines in a box; the line being executed gets an amber bar
  strip     execution order along the bottom: boxes "label / value", the last one amber
  lane      a horizontal timeline for one transaction (sequence-diagram style)

Animation
  One timeline per figure. Every item may fade in (show), fade out (hide) and slide (move).
  The static render (reduced motion, or before the observer starts it) is the FINAL state:
  hidden items carry opacity="0", moved items carry their final translate().
  Only opacity and transform are animated, inside prefers-reduced-motion:no-preference.

Usage
  f = Fig('f3-', 860, 300, 'aria text', 'CAPTION')
  t = Table(0, 40, [('id', 40), ('name', 90)])
  f(t.head()); f(t.row(0, ['1', 'Alice']), show=0.4)
  html = f.render()
"""
import math

MU, TX, FA = 'var(--muted)', 'var(--text)', 'var(--faint)'
AM, GR, RD, BL = 'var(--probe)', 'var(--ok)', 'var(--tomb)', 'var(--filled)'
RULE, RULE_HI = 'var(--rule)', 'var(--rule-hi)'
RGB = {'am': '--amber-a', 'gr': '--green-a', 'rd': '--red-a', 'bl': '--blue-a'}
COL = {'am': AM, 'gr': GR, 'rd': RD, 'bl': BL}
MONO = 'font-family:ui-monospace,SFMono-Regular,Menlo,monospace'


def T(x, y, s, c=TX, a='middle', cls='sv-d', mono=False, bold=False):
    st = 'fill:%s' % c + (';' + MONO if mono else '') + (';font-weight:600' if bold else '')
    an = ' text-anchor="%s"' % a if a else ''
    return '<text class="%s" x="%.1f" y="%.1f" style="%s"%s>%s</text>' % (cls, x, y, st, an, s)


def R(x, y, w, h, fill='var(--bg)', stroke=RULE_HI, rx=3, sw=1, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" '
            'stroke-width="%s"%s/>' % (x, y, w, h, rx, fill, stroke, sw, d))


def tint(tone, al='.16'):
    return 'rgba(var(%s),%s)' % (RGB[tone], al)


def L(x1, y1, x2, y2, c=RULE_HI, sw=1.2, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, c, sw, d))


def arrow(x1, y1, x2, y2, c=MU, sw=1.3, dash=None, head=7):
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(a), y2 - head * math.sin(a)
    w = head * 0.5
    p = '%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (x2, y2, bx - w * math.sin(a), by + w * math.cos(a),
                                           bx + w * math.sin(a), by - w * math.cos(a))
    return L(x1, y1, bx, by, c, sw, dash) + '<polygon points="%s" fill="%s"/>' % (p, c)


def curve(x1, y1, x2, y2, c=AM, bend=30, sw=1.3, dash=None, head=True):
    """Quadratic connector bowing to the right of the direction of travel."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy) or 1
    qx, qy = mx - dy / n * bend, my + dx / n * bend
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    s = ('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="%s"%s/>'
         % (x1, y1, qx, qy, x2, y2, c, sw, d))
    if head:
        a = math.atan2(y2 - qy, x2 - qx)
        bx, by = x2 - 7 * math.cos(a), y2 - 7 * math.sin(a)
        s += '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>' % (
            x2, y2, bx - 3.5 * math.sin(a), by + 3.5 * math.cos(a),
            bx + 3.5 * math.sin(a), by - 3.5 * math.cos(a), c)
    return s


def pill(cx, y, t, tone='gr', w=None):
    """Rounded chip. tone None = neutral (white, grey border, dark text)."""
    w = w or 18 + len(t) * 6.4
    fill, st, c = (('var(--bg)', RULE_HI, TX) if tone is None else (tint(tone, '.18'), COL[tone], COL[tone]))
    return (R(cx - w / 2, y, w, 20, 'var(--bg)', 'none', 10) +
            R(cx - w / 2, y, w, 20, fill, st, 10, 1.2) + T(cx, y + 14, t, c))


def leader(x1, y1, x2, y2, t, c=AM, a='start'):
    tx = x2 + (5 if a == 'start' else -5)
    return L(x1, y1, x2, y2, c, 1, '3 3') + T(tx, y2 + 4, t, c, a)


def callout(x, y, t1, t2=None):
    s = R(x, y, 3, 20 if not t2 else 34, AM, 'none', 1.5) + T(x + 12, y + 14, t1, AM, 'start')
    if t2:
        s += T(x + 12, y + 30, t2, MU, 'start')
    return s


def cap(x, y, t, c=MU):
    return T(x, y, t, c, 'start', 'sv-hv')


def note(x, y, t, c=MU, a='start'):
    return T(x, y, t, c, a)


class Table:
    """A table drawn in the classical-ML style. cols = [(name, width) or (name, width, sub)]."""

    def __init__(self, x, y, cols, title=None, step=30, rh=26):
        self.x, self.y, self.cols, self.title = x, y, cols, title
        self.step, self.rh = step, rh
        self.w = sum(c[1] for c in cols)
        self.sub = any(len(c) > 2 for c in cols)
        self.hb = y + (18 if title else 0) + 10          # header baseline
        self.line = self.hb + (21 if self.sub else 8)
        self.r0 = self.line + 3                           # first row top

    def cx(self, j):
        return self.x + sum(c[1] for c in self.cols[:j]) + self.cols[j][1] / 2

    def colx(self, j):
        return self.x + sum(c[1] for c in self.cols[:j])

    def ry(self, i):
        return self.r0 + i * self.step

    def head(self):
        s = cap(self.x, self.y + 10, self.title) if self.title else ''
        for j, c in enumerate(self.cols):
            s += T(self.cx(j), self.hb, c[0], MU)
            if len(c) > 2 and c[2]:
                s += T(self.cx(j), self.hb + 13, c[2], FA)
        return s + L(self.x, self.line, self.x + self.w, self.line)

    def row(self, i, vals, tone=None, colors=None, j0=0):
        """One row. tone tints the whole row; colors={col: css colour} for single values."""
        y = self.ry(i)
        x0 = self.colx(j0)
        w = self.w - (x0 - self.x)
        fill = tint(tone, '.14') if tone else 'var(--bg)'
        st = COL[tone] if tone else RULE_HI
        s = R(x0, y, w, self.rh, 'var(--bg)', 'none') if tone else ''
        s += R(x0, y, w, self.rh, fill, st, 3, 1)
        for j, v in enumerate(vals):
            jj = j + j0
            c = (colors or {}).get(jj, COL[tone] if tone in ('rd',) else TX)
            s += T(self.cx(jj), y + 17, v, c)
        return s

    def cell(self, i, j, v, tone=None, c=None, pad=3):
        """A single cell redrawn on top of a row (opaque backing first, so old text is hidden)."""
        x, y, w = self.colx(j) + pad, self.ry(i) + 2, self.cols[j][1] - 2 * pad
        s = R(x, y, w, self.rh - 4, 'var(--bg)', 'none', 2)
        if tone:
            s += R(x, y, w, self.rh - 4, tint(tone, '.20'), COL[tone], 2, 1)
        return s + T(self.cx(j), self.ry(i) + 17, v, c or (COL[tone] if tone else TX))

    def outline(self, i0, i1=None, j0=0, j1=None, c=AM, sw=1.6, dash=None):
        i1 = i0 if i1 is None else i1
        j1 = len(self.cols) - 1 if j1 is None else j1
        x = self.colx(j0) - 2
        w = self.colx(j1) + self.cols[j1][1] - self.colx(j0) + 4
        y = self.ry(i0) - 2
        h = self.ry(i1) + self.rh - self.ry(i0) + 4
        return R(x, y, w, h, 'none', c, 4, sw, dash)

    def colbox(self, j, n, c=AM, head=True, dash=None):
        x = self.colx(j) + 1
        y = (self.hb - 12) if head else self.ry(0) - 2
        h = self.ry(n - 1) + self.rh + 2 - y
        return R(x, y, self.cols[j][1] - 2, h, 'none', c, 4, 1.6, dash)

    def dimcol(self, j, n):
        x = self.colx(j) + 1
        y = self.hb - 12
        h = self.ry(n - 1) + self.rh - y
        return R(x, y, self.cols[j][1] - 2, h, 'var(--sunk)', 'none', 2).replace('/>', ' opacity=".82"/>')

    def strike(self, i, c=RD):
        y = self.ry(i) + self.rh / 2
        return L(self.x + 6, y, self.x + self.w - 6, y, c, 1.4)

    def bottom(self, n):
        return self.ry(n - 1) + self.rh


class Query:
    """SQL lines in a box. bar(i) marks the line being executed."""

    def __init__(self, x, y, lines, w=None, title=None):
        self.x, self.y, self.lines = x, y + (16 if title else 0), lines
        self.title, self.ty = title, y
        self.w = w or 22 + max(len(l) for l in lines) * 6.6
        self.h = len(lines) * 18 + 12

    def svg(self):
        s = cap(self.x, self.ty + 10, self.title) if self.title else ''
        s += R(self.x, self.y, self.w, self.h, 'var(--bg)', RULE_HI, 6)
        for i, l in enumerate(self.lines):
            lead = len(l) - len(l.lstrip(' '))
            s += T(self.x + 12, self.y + 20 + i * 18, '\u00a0' * lead + l.lstrip(' '), TX, 'start', mono=True)
        return s

    def bar(self, i, tone='am'):
        y = self.y + 6 + i * 18
        return (R(self.x + 3, y, self.w - 6, 18, tint(tone, '.18'), 'none', 2) +
                R(self.x + 3, y, 3, 18, COL[tone], 'none', 1))

    def bottom(self):
        return self.y + self.h


def strip(y, caption, steps, w=860, x=0, gap=24, hl=True):
    """Execution order along the bottom. Returns [caption, box0, arrow0, box1, ...]."""
    n = len(steps)
    bw = (w - (n - 1) * gap) / n
    out = [T(x, y + 10, caption, MU, 'start')]
    for k, (lab, val) in enumerate(steps):
        bx = x + k * (bw + gap)
        last = hl and k == n - 1
        s = R(bx, y + 18, bw, 42, tint('am', '.14') if last else 'var(--bg)',
              AM if last else RULE_HI, 6, 1.4 if last else 1)
        s += T(bx + bw / 2, y + 35, lab, MU)
        s += T(bx + bw / 2, y + 51, val, AM if last else TX)
        out.append(s)
        if k < n - 1:
            out.append(arrow(bx + bw + 4, y + 39, bx + bw + gap - 4, y + 39, FA, 1.2, None, 6))
    return out


def lane(x, y, w, label):
    return T(x, y + 4, label, MU, 'start', 'sv-s') + L(x + 34, y, x + w, y, RULE, 1, '4 4')


class Fig:
    """One figure, one timeline."""

    def __init__(self, pre, w, h, aria, caption=None, end_hold=1.8):
        self.pre, self.w, self.h, self.aria = pre, w, h, aria
        self.items, self.hold = [], end_hold
        if caption:
            self.items.append((cap(0, 14, caption), None, None, None, .5))

    def __call__(self, svg, show=None, hide=None, move=None, d=.5):
        """move = (start, dx, dy[, duration]): the item slides IN from offset (dx, dy) to where it is drawn."""
        if move and len(move) == 3:
            move = (move[0], move[1], move[2], .9)
        self.items.append((svg, show, hide, move, d))
        return self

    def strip(self, parts, t0, dt=.35):
        for k, p in enumerate(parts):
            self(p, None if k == 0 else t0 + (k - 1) // 2 * dt * 2 + ((k - 1) % 2) * dt)
        return self

    def render(self):
        ends = [0]
        for _, sh, hd, mv, d in self.items:
            for t in (sh, hd):
                if t is not None:
                    ends.append(t + d)
            if mv:
                ends.append(mv[0] + mv[3])
        TT = max(ends) + self.hold
        css, kfs, body = [], [], []
        k = 0
        for svg, sh, hd, mv, d in self.items:
            if sh is None and hd is None and mv is None:
                body.append(svg)
                continue
            k += 1
            nm = '%sa%d' % (self.pre, k)
            pts = {0.0, TT}
            for t in (sh, hd):
                if t is not None:
                    pts |= {t, t + d}
            if mv:
                pts |= {mv[0], mv[0] + mv[3]}
            fr = []
            for t in sorted(p for p in pts if p <= TT):
                o = 1.0
                if sh is not None:
                    o = 0.0 if t <= sh else (1.0 if t >= sh + d else (t - sh) / d)
                if hd is not None and t >= hd:
                    o = min(o, max(0.0, 1 - (t - hd) / d))
                f = '%.3f%%{animation-timing-function:ease-in-out;opacity:%.2f' % (100 * t / TT, o)
                if mv:
                    tm, dx, dy, dm = mv
                    q = 0.0 if t <= tm else (1.0 if t >= tm + dm else (t - tm) / dm)
                    f += ';transform:translate(%.1fpx,%.1fpx)' % (dx * (1 - q), dy * (1 - q))
                fr.append(f + '}')
            kfs.append('@keyframes %s{%s}' % (nm, ''.join(fr)))
            css.append('.%s{animation:%s %.2fs linear 1 forwards}' % (nm, nm, TT))
            attr = ' opacity="0"' if hd is not None else ''
            body.append('<g class="%s"%s>%s</g>' % (nm, attr, svg))
        style = ''.join(kfs) + '@media (prefers-reduced-motion:no-preference){%s}' % ''.join(css)
        return ('<figure class="gist">\n<svg viewBox="0 0 %d %d" role="img" aria-label="%s" data-anim>'
                '<style>%s</style>\n%s\n</svg>\n</figure>' % (self.w, self.h, self.aria.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'), style, '\n'.join(body)))
