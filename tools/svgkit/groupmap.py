# -*- coding: utf-8 -*-
"""Shared pieces for group overviews of parallel / sequential topics (2026-10-09).

A group map is 2-3 figures: a map (gallery or connecting structure), an optional lookup table,
a learning order. Each page script builds its figures and calls rewrite().

    from groupmap import rewrite, sec, table, order, keep_figure
"""
import re
from overview import Fig, text, esc

def keep_figure(page_src, needle):
    """Return the <figure class="gist">...</figure> whose svg aria-label contains needle."""
    i = page_src.index(needle)
    a = page_src.rindex('<figure', 0, i)
    b = page_src.index('</figure>', i) + 9
    return page_src[a:b]

def sec(slug, n, title, key, fig, why=None, after=''):
    w = ''
    if why:
        w = '\n  <ul class="why">' + ''.join(f'<li>{x}</li>' for x in why) + '</ul>'
    return (f'<section id="{slug}-s{n}" class="lesson">\n  <div class="sh"><b>{n:02d}</b><h2>{title}</h2></div>\n'
            f'  <p class="key">{key}</p>\n{fig}{after}{w}\n</section>\n')

def gist(svg):
    return f'<figure class="gist">\n{svg}\n</figure>'

def table(prefix, caption, label, cols, rows, hl=None, rowh=32, mono=()):
    """cols = [(x, HEADER), ...]; rows = [(cells..., href)]; mono = column indexes in mono font."""
    h = 64 + len(rows) * (rowh + 4) + 4
    f = Fig(prefix, 680, h, caption, label)
    for x, head in cols:
        f.add(text(x + 10, 44, head, 'sv-hv', 'var(--muted)', 'start'))
    f.add('<line x1="0" y1="54" x2="680" y2="54" stroke="var(--rule-hi)"/>')
    for i, r in enumerate(rows):
        *cells, href = r
        y = 64 + i * (rowh + 4)
        on = hl is not None and i in hl
        inner = (f'<rect class="nd" x="0" y="{y}" width="680" height="{rowh}" rx="7" '
                 f'fill="{"rgba(var(--violet-a),.08)" if on else "var(--bg)"}" '
                 f'stroke="{"var(--violet)" if on else "var(--rule)"}"/>')
        for j, ((x, _), c) in enumerate(zip(cols, cells)):
            if j == 0:
                inner += text(x + 10, y + rowh / 2 + 4, c, 'sv-s', 'var(--violet)' if on else 'var(--brand-hi)',
                              'start', ';font-weight:600')
            else:
                inner += text(x + 10, y + rowh / 2 + 4, c, 'sv-d', 'var(--text)', 'start',
                              ';font-family:var(--mono)' if j in mono else '')
        if href:
            inner = f'<a href="{href}">{inner}</a>'
        f.add(f'<g class="{f.step(.3 + i * .18)}">{inner}</g>')
    return f.svg()

def order(prefix, caption, label, stops, per_row=5, last_hl=True):
    """stops = [(name, note, href)]; wraps into rows of per_row, numbered."""
    gap = 14
    w = (680 - gap * (per_row - 1)) / per_row
    rows = (len(stops) + per_row - 1) // per_row
    f = Fig(prefix, 680, 40 + rows * 62 + 4, caption, label)
    for i, (n, note, href) in enumerate(stops):
        r, c = divmod(i, per_row)
        cx, cy = c * (w + gap) + w / 2, 62 + r * 62
        if c:
            f.add(f'<line class="{f.step(.4 + i * .25, draw=True)}" pathLength="1" x1="{cx - w/2 - gap + 2:.1f}" '
                  f'y1="{cy}" x2="{cx - w/2 - 2:.1f}" y2="{cy}" stroke="var(--rule-hi)" stroke-width="1.6"/>')
        tone = 'violet' if (last_hl and i == len(stops) - 1) else 'plain'
        f.node(cx, cy, f'{i+1} · {n}', note, tone, f.step(.3 + i * .25), href, None, w=w, h=44)
    return f.svg()

def rewrite(page, body, blurb=None, footer=None):
    s = open(page, encoding='utf-8').read()
    a = s.index('<header class="hero">')
    b = s.index('<script>\n/* Figures start')
    s = s[:a] + body + '\n' + s[b:]
    if blurb:
        s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s"' % blurb, s, count=1)
    if footer:
        s = re.sub(r'<footer>.*?</footer>', f'<footer>{footer}</footer>', s, count=1, flags=re.S)
    open(page, 'w', encoding='utf-8').write(s)
