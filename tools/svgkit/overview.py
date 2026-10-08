# -*- coding: utf-8 -*-
"""Figure kit for shelf overviews.

Overviews show the whole field at a glance, so their figures are calmer than lesson figures:
layers fade in once (root -> branches -> leaves), edges draw in, nothing moves afterwards.
The final frame must read on its own.

    from overview import Fig
    f = Fig('dsov1', 680, 400, 'CAPTION', 'aria label')
    a = f.step(0.2)                       # one reveal step -> class name
    f.node(x, y, 'Name', 'note', cls=a, href='...', glyph='array')
    f.edge((x1, y1), (x2, y2), cls=f.step(0.6, draw=True))
    html = f.svg()

Colours: brand (structure), filled (data), violet (highlight / hybrid), rose (wall).
Never a solid brand fill (soat check 3); tints are 6-14 %.
"""

TONE = {
    'brand':  ('var(--brand)',  'rgba(var(--clay-a),.10)', 'var(--brand-hi)'),
    'filled': ('var(--filled)', 'rgba(var(--blue-a),.09)', 'var(--filled)'),
    'violet': ('var(--violet)', 'rgba(var(--violet-a),.09)', 'var(--violet)'),
    'rose':   ('var(--rose)',   'rgba(var(--rose-a),.08)', 'var(--rose)'),
    'plain':  ('var(--rule-hi)', 'var(--bg)', 'var(--text)'),
}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def text(x, y, s, cls='sv-s', fill='var(--text)', anchor='middle', extra=''):
    return (f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" style="fill:{fill}{extra}" '
            f'text-anchor="{anchor}">{esc(s)}</text>')


def glyph(kind, x, y, col):
    """A tiny picture of the concept itself, about 22x18, top-left at (x, y)."""
    g = []
    if kind == 'array':
        for i in range(4):
            g.append(f'<rect x="{x+i*5.5:.1f}" y="{y+5}" width="5" height="8" fill="none" stroke="{col}" stroke-width="1.1"/>')
    elif kind == 'node':
        g.append(f'<rect x="{x}" y="{y+5}" width="8" height="8" rx="1.5" fill="none" stroke="{col}" stroke-width="1.1"/>')
        g.append(f'<path d="M{x+8},{y+9} H{x+17}" stroke="{col}" stroke-width="1.1"/><path d="M{x+15},{y+6.5} L{x+19},{y+9} L{x+15},{y+11.5}z" fill="{col}"/>')
    elif kind == 'list':
        for i in range(3):
            g.append(f'<rect x="{x+i*8:.1f}" y="{y+6}" width="5" height="6" rx="1" fill="none" stroke="{col}" stroke-width="1.1"/>')
            if i < 2:
                g.append(f'<path d="M{x+i*8+5},{y+9} H{x+i*8+8}" stroke="{col}" stroke-width="1"/>')
    elif kind == 'stack':
        for i in range(3):
            g.append(f'<rect x="{x+3}" y="{y+2+i*5}" width="14" height="4" rx="1" fill="none" stroke="{col}" stroke-width="1.1"/>')
    elif kind == 'hash':
        for i in range(3):
            g.append(f'<rect x="{x}" y="{y+2+i*5}" width="5" height="4" fill="none" stroke="{col}" stroke-width="1"/>')
        g.append(f'<path d="M{x+5},{y+4} H{x+10} M{x+5},{y+14} H{x+10} M{x+15},{y+14} H{x+18}" stroke="{col}" stroke-width="1"/>')
        g.append(f'<circle cx="{x+12.5}" cy="{y+4}" r="2.2" fill="none" stroke="{col}" stroke-width="1"/><circle cx="{x+12.5}" cy="{y+14}" r="2.2" fill="none" stroke="{col}" stroke-width="1"/>')
    elif kind in ('tree', 'heap', 'bst', 'trie'):
        pts = [(x+10, y+3), (x+4, y+10), (x+16, y+10), (x+1, y+16), (x+7, y+16)]
        g.append(f'<path d="M{pts[0][0]},{pts[0][1]} L{pts[1][0]},{pts[1][1]} M{pts[0][0]},{pts[0][1]} L{pts[2][0]},{pts[2][1]} M{pts[1][0]},{pts[1][1]} L{pts[3][0]},{pts[3][1]} M{pts[1][0]},{pts[1][1]} L{pts[4][0]},{pts[4][1]}" stroke="{col}" stroke-width="1"/>')
        for px, py in pts:
            g.append(f'<circle cx="{px}" cy="{py}" r="2.1" fill="var(--bg)" stroke="{col}" stroke-width="1"/>')
    elif kind == 'graph':
        pts = [(x+3, y+4), (x+17, y+3), (x+10, y+10), (x+3, y+16), (x+18, y+15)]
        g.append(f'<path d="M{pts[0][0]},{pts[0][1]} L{pts[1][0]},{pts[1][1]} L{pts[2][0]},{pts[2][1]} L{pts[0][0]},{pts[0][1]} M{pts[2][0]},{pts[2][1]} L{pts[3][0]},{pts[3][1]} L{pts[4][0]},{pts[4][1]} L{pts[2][0]},{pts[2][1]}" fill="none" stroke="{col}" stroke-width="1"/>')
        for px, py in pts:
            g.append(f'<circle cx="{px}" cy="{py}" r="2.1" fill="var(--bg)" stroke="{col}" stroke-width="1"/>')
    elif kind == 'groups':
        for cx, cy in ((x+4, y+6), (x+10, y+12), (x+4, y+15)):
            g.append(f'<circle cx="{cx}" cy="{cy}" r="2.3" fill="none" stroke="{col}" stroke-width="1"/>')
        g.append(f'<circle cx="{x+16}" cy="{y+6}" r="2.3" fill="none" stroke="{col}" stroke-width="1"/><circle cx="{x+18}" cy="{y+14}" r="2.3" fill="none" stroke="{col}" stroke-width="1"/>')
        g.append(f'<path d="M{x+4},{y+8.3} L{x+8.5},{y+10.5} M{x+4},{y+12.7} L{x+8},{y+11.5} M{x+16.5},{y+8.3} L{x+17.5},{y+11.7}" stroke="{col}" stroke-width="1"/>')
    return ''.join(g)


class Fig:
    def __init__(self, prefix, w, h, caption, label, dur=None):
        self.p, self.w, self.h, self.caption, self.label = prefix, w, h, caption, label
        self.steps = []          # (delay, kind)
        self.body = []
        self.dur = dur

    # ---- animation ----------------------------------------------------------
    def step(self, delay, draw=False):
        self.steps.append((delay, 'draw' if draw else 'fade'))
        return f'{self.p}-a{len(self.steps)}'

    def _style(self):
        dur = self.dur or (max(d for d, _ in self.steps) + 0.8)
        ks, cs = [], []
        for i, (d, kind) in enumerate(self.steps, 1):
            a = d / dur * 100
            b = min((d + (0.6 if kind == 'draw' else 0.4)) / dur * 100, 100)
            n = f'{self.p}-a{i}'
            if kind == 'draw':
                frm, to = 'stroke-dashoffset:1', 'stroke-dashoffset:0'
                cs.append(f'.{n}{{stroke-dasharray:1;animation:{n} {dur:.2f}s ease-out 1 forwards}}')
            else:
                frm, to = 'opacity:0;transform:translateY(5px)', 'opacity:1;transform:none'
                cs.append(f'.{n}{{animation:{n} {dur:.2f}s ease-out 1 forwards}}')
            ks.append(f'@keyframes {n}{{0%{{{frm}}}{a:.2f}%{{{frm}}}{b:.2f}%{{{to}}}100%{{{to}}}}}')
        hover = (f'.{self.p} a:hover rect.nd{{fill:var(--brand-soft)}}'
                 f'.{self.p} a rect.nd{{transition:fill .15s}}')
        return ('<style>' + ''.join(ks) + hover +
                '@media (prefers-reduced-motion:no-preference){' + ''.join(cs) + '}</style>')

    # ---- primitives ----------------------------------------------------------
    def add(self, s):
        self.body.append(s)

    def node(self, cx, cy, name, note='', tone='plain', cls='', href=None, glyph_kind=None,
             w=132, h=44, dashed=False):
        stroke, fill, ink = TONE[tone]
        x, y = cx - w / 2, cy - h / 2
        dash = ' stroke-dasharray="4 3"' if dashed else ''
        g = [f'<rect class="nd" x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="10" '
             f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"{dash}/>']
        tx = x + 12
        if glyph_kind:
            g.append(glyph(glyph_kind, x + 10, cy - 9, stroke if tone != 'plain' else 'var(--muted)'))
            tx = x + 38
        if note:
            g.append(text(tx, cy - 3, name, 'sv-s', ink, 'start', ';font-weight:600'))
            g.append(text(tx, cy + 12, note, 'sv-d', 'var(--muted)', 'start'))
        else:
            g.append(text(tx, cy + 4, name, 'sv-s', ink, 'start', ';font-weight:600'))
        inner = ''.join(g)
        if href:
            inner = f'<a href="{href}">{inner}</a>'
        self.add(f'<g class="{cls}">{inner}</g>' if cls else inner)

    def edge(self, a, b, cls='', col='var(--rule-hi)', width=1.6, dashed=False, arrow=False):
        (x1, y1), (x2, y2) = a, b
        my = (y1 + y2) / 2
        d = f'M{x1:.1f},{y1:.1f} C{x1:.1f},{my:.1f} {x2:.1f},{my:.1f} {x2:.1f},{y2:.1f}'
        dash = ' stroke-dasharray="4 3"' if dashed else ''
        c = f' class="{cls}"' if cls else ''
        self.add(f'<path{c} d="{d}" pathLength="1" fill="none" stroke="{col}" stroke-width="{width}"{dash}/>')

    def hedge(self, a, b, cls='', col='var(--rule-hi)', width=1.4):
        """Horizontal S-curve, for left-to-right trees."""
        (x1, y1), (x2, y2) = a, b
        mx = (x1 + x2) / 2
        c = f' class="{cls}"' if cls else ''
        self.add(f'<path{c} d="M{x1:.1f},{y1:.1f} C{mx:.1f},{y1:.1f} {mx:.1f},{y2:.1f} {x2:.1f},{y2:.1f}" '
                 f'pathLength="1" fill="none" stroke="{col}" stroke-width="{width}"/>')

    def pill(self, x, cy, label, tone='brand', cls='', href=None, w=None, anchor='start'):
        stroke, fill, ink = TONE[tone]
        w = w or (len(label) * 6.6 + 22)
        if anchor == 'middle':
            x -= w / 2
        inner = (f'<rect class="nd" x="{x:.1f}" y="{cy-11:.1f}" width="{w:.1f}" height="22" rx="11" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
                 + text(x + w / 2, cy + 4, label, 'sv-d', ink, 'middle', ';font-weight:600'))
        if href:
            inner = f'<a href="{href}">{inner}</a>'
        self.add(f'<g class="{cls}">{inner}</g>' if cls else inner)
        return w

    def svg(self):
        head = (f'<svg class="{self.p}" viewBox="0 0 {self.w} {self.h}" role="img" '
                f'aria-label="{esc(self.label)}" data-anim>')
        cap = text(0, 14, self.caption, 'sv-hv', 'var(--muted)', 'start')
        return head + self._style() + cap + ''.join(self.body) + '</svg>'


# ---- drawing helpers for gallery tiles -------------------------------------------------------
B, V, FL = 'var(--brand)', 'var(--violet)', 'var(--filled)'
TINT, VTINT = 'rgba(var(--clay-a),.10)', 'rgba(var(--violet-a),.14)'


def cell(x, y, w, h, s='', hl=False):
    """A small box (array cell, table cell). hl = violet highlight."""
    o = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="2.5" fill="{VTINT if hl else TINT}" '
         f'stroke="{V if hl else B}" stroke-width="1.1"/>')
    if s != '':
        o += text(x + w / 2, y + h / 2 + 3.5, str(s), 'sv-d', V if hl else 'var(--text)', 'middle',
                  ';font-family:var(--mono);font-size:9.5px')
    return o


def dot(x, y, s='', hl=False, r=8):
    """A graph / tree node."""
    o = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{VTINT if hl else "var(--bg)"}" '
         f'stroke="{V if hl else B}" stroke-width="1.2"/>')
    if s != '':
        o += text(x, y + 3.3, str(s), 'sv-d', V if hl else 'var(--text)', 'middle',
                  ';font-family:var(--mono);font-size:9px')
    return o


def ln(x1, y1, x2, y2, col=None, w=1.1, dash=False):
    d = ' stroke-dasharray="3 2"' if dash else ''
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{col or "var(--rule-hi)"}" stroke-width="{w}"{d}/>')


def arr(x1, y, x2, col=None):
    """Horizontal arrow from x1 to x2 at height y."""
    c = col or 'var(--muted)'
    return ln(x1, y, x2 - 4, y, c) + f'<path d="M{x2-5},{y-3} L{x2},{y} L{x2-5},{y+3}z" fill="{c}"/>'


def gallery(f, bands, top=44, cols=4, tw=164, th=98, gap=8, t0=0.1):
    """Fill Fig f with bands of picture tiles; returns the bottom y.

    bands = [(LABEL, 'right note', [(name, draw, href), ...]), ...]
    draw(x, y) returns SVG for a 138x58 drawing box with top-left (x, y).
    Each band is a caption row then rows of `cols` tiles; tiles fade in one by one.
    """
    y0, t = top, t0
    for label, sub, items in bands:
        f.add(f'<g class="{f.step(t)}">' + text(0, y0, label, 'sv-hv', B, 'start')
              + text(f.w, y0, sub, 'sv-d', 'var(--muted)', 'end') + '</g>')
        for i, (name, draw, href) in enumerate(items):
            r, c = divmod(i, cols)
            x, y = c * (tw + gap), y0 + 10 + r * (th + 10)
            inner = (f'<rect class="nd" x="{x:.1f}" y="{y}" width="{tw}" height="{th}" rx="10" fill="var(--bg)" '
                     f'stroke="var(--rule-hi)" stroke-width="1.2"/>'
                     + text(x + 10, y + 17, name, 'sv-s', 'var(--text)', 'start', ';font-weight:600;font-size:11px')
                     + draw(x + 13, y + 30))
            if href:
                inner = f'<a href="{href}">{inner}</a>'
            f.add(f'<g class="{f.step(t + 0.25 + i * 0.12)}">{inner}</g>')
        rows = (len(items) + cols - 1) // cols
        y0 = y0 + 10 + rows * (th + 10) + 24
        t += 0.25 + len(items) * 0.12 + 0.2
    return y0 - 24
