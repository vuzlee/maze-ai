# -*- coding: utf-8 -*-
"""NoSQL & data systems shelf overview: gallery of store shapes + one real data system.

    python3 tools/svgkit/06-nosql-data/nosql_data_overview.py   # rewrites figures in place
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from overview import Fig, text, gallery, cell, dot, ln, arr, B, V, FL, TINT, VTINT

PAGE = 'content/06-nosql-data/01-overview/nosql-data-overview/index.html'
NL = '../../02-nosql/nosql-landscape/index.html'
OO = '../../02-nosql/oltp-vs-olap/index.html'
DSY = '../../03-data-systems/data-systems/index.html'
M = ';font-family:var(--mono);font-size:9px'

def t(x, y, s, col='var(--text)', a='start', ex=M):
    return text(x, y, s, 'sv-d', col, a, ex)

def d_kv(x, y):
    o = ''
    for i, (k, v) in enumerate([('user:7', '"Ana"'), ('cart:7', '[3 items]'), ('sess:9', 'token')]):
        yy = y + 2 + i * 19
        o += cell(x + 2, yy, 52, 16, '', i == 0) + t(x + 28, yy + 11.5, k, V if i == 0 else 'var(--text)', 'middle')
        o += arr(x + 56, yy + 8, x + 72) + cell(x + 74, yy, 62, 16) + t(x + 105, yy + 11.5, v, 'var(--text)', 'middle')
    return o

def d_doc(x, y):
    o = t(x + 2, y + 6, '{ order 42', B)
    P = [(x + 8, y + 10)]
    kids = [('id: 42', 18), ('customer: {…}', 32), ('items: [', 46)]
    o += ln(x + 6, y + 9, x + 6, y + 44)
    for s, yy in kids:
        o += ln(x + 6, y + yy - 3, x + 14, y + yy - 3) + t(x + 17, y + yy, s)
    o += ln(x + 20, y + 49, x + 20, y + 58) + ln(x + 20, y + 56, x + 28, y + 56)
    o += cell(x + 30, y + 50, 46, 12, '', True) + cell(x + 80, y + 50, 46, 12, '', True)
    return o

def d_wide(x, y):
    o = f'<rect x="{x+34}" y="{y}" width="50" height="11" rx="2" fill="{TINT}" stroke="{B}" stroke-width="1"/>'
    o += f'<rect x="{x+86}" y="{y}" width="50" height="11" rx="2" fill="{VTINT}" stroke="{V}" stroke-width="1"/>'
    o += t(x + 59, y + 8.5, 'profile', B, 'middle', ';font-size:8px') + t(x + 111, y + 8.5, 'events', V, 'middle', ';font-size:8px')
    for r, (key, n1, n2) in enumerate([('u1', 2, 3), ('u2', 1, 2), ('u3', 2, 1)]):
        yy = y + 15 + r * 15
        o += t(x + 2, yy + 10, key)
        o += ''.join(cell(x + 34 + i * 17, yy, 15, 12) for i in range(n1))
        o += ''.join(cell(x + 86 + i * 17, yy, 15, 12, '', True) for i in range(n2))
    return o

def d_graph(x, y):
    P = {'Ana': (x + 18, y + 12), 'Bo': (x + 70, y + 6), 'Cy': (x + 122, y + 16), 'Di': (x + 44, y + 50), 'Ed': (x + 100, y + 50)}
    E = [('Ana', 'Bo'), ('Bo', 'Cy'), ('Ana', 'Di'), ('Di', 'Ed'), ('Bo', 'Ed'), ('Cy', 'Ed')]
    o = ''.join(ln(*P[a], *P[b], V if (a, b) in (('Ana', 'Bo'), ('Bo', 'Ed')) else None, 1.8 if (a, b) in (('Ana', 'Bo'), ('Bo', 'Ed')) else 1.1) for a, b in E)
    o += t(x + 44, y + 36, 'follows', 'var(--faint)', 'middle', ';font-size:8px')
    return o + ''.join(dot(px, py, k[0], k in ('Ana', 'Bo', 'Ed'), 8) for k, (px, py) in P.items())

def d_rowcol(x, y):
    o = t(x + 30, y + 4, 'row store', 'var(--muted)', 'middle', ';font-size:8px') + t(x + 108, y + 4, 'column store', 'var(--muted)', 'middle', ';font-size:8px')
    for r in range(4):
        for c in range(3):
            o += cell(x + 6 + c * 16, y + 8 + r * 10, 15, 9, '', r == 1)
            o += cell(x + 84 + c * 16, y + 8 + r * 10, 15, 9, '', c == 2)
    o += t(x + 30, y + 58, 'OLTP: one row', V, 'middle', ';font-size:8px') + t(x + 108, y + 58, 'OLAP: one column', V, 'middle', ';font-size:8px')
    return o

def d_etl(x, y):
    o = ''
    for i, (s, hl) in enumerate([('E', False), ('T', True), ('L', False)]):
        cx = x + 4 + i * 48
        o += f'<rect x="{cx}" y="{y+16}" width="34" height="26" rx="4" fill="{VTINT if hl else TINT}" stroke="{V if hl else B}" stroke-width="1.1"/>'
        o += t(cx + 17, y + 33, s, V if hl else B, 'middle', ';font-family:var(--mono);font-size:11px;font-weight:600')
        if i < 2:
            o += arr(cx + 35, y + 29, cx + 47)
    return o + t(x + 69, y + 56, 'nightly, all at once', 'var(--muted)', 'middle', ';font-size:8.5px')

def d_stream(x, y):
    o = arr(x + 2, y + 28, x + 136)
    for i in range(7):
        o += cell(x + 6 + i * 18, y + 21, 12, 14, '', i == 6)
    o += t(x + 2, y + 12, 'events, one by one →', 'var(--muted)', 'start', ';font-size:8.5px')
    o += t(x + 136, y + 52, 'now', V, 'end', ';font-size:8.5px')
    return o

def d_lake(x, y):
    o = f'<path d="M{x+4},{y+30} q8,-5 16,0 t16,0 t16,0 t16,0" fill="none" stroke="{FL}" stroke-width="1.1"/>'
    o += f'<rect x="{x+4}" y="{y+30}" width="64" height="26" rx="3" fill="rgba(var(--blue-a),.08)" stroke="none"/>'
    for i, (px, py) in enumerate([(12, 40), (28, 46), (44, 38), (58, 48)]):
        o += f'<rect x="{x+px}" y="{y+py}" width="7" height="6" rx="1" fill="none" stroke="{FL}" stroke-width="1"/>'
    o += t(x + 36, y + 18, 'lake: raw files', 'var(--muted)', 'middle', ';font-size:8px')
    o += arr(x + 70, y + 42, x + 82)
    for r in range(3):
        for c in range(3):
            o += cell(x + 86 + c * 17, y + 26 + r * 11, 16, 10, '', r == 0)
    o += t(x + 111, y + 18, 'warehouse', 'var(--muted)', 'middle', ';font-size:8px')
    return o

def fig_gallery():
    f = Fig('nsov1', 680, 500, 'THE WHOLE SHELF · FOUR SHAPES OF NOSQL STORE, FOUR WAYS DATA MOVES AND IS READ',
            'Two bands of pictures. NoSQL stores: key-value pairs, a document as a JSON tree with nested items, '
            'wide-column rows grouped into column families, and a graph of people linked by follows edges. '
            'Data systems: row store versus column store, OLTP reading one row and OLAP reading one column; '
            'batch ETL extract, transform, load; a stream of events arriving one by one; and a data lake of raw '
            'files feeding a warehouse table. Each tile links to its lesson.')
    bands = [('NOSQL STORES', 'one shape of data each', [
                ('Key-value', d_kv, NL), ('Document', d_doc, NL), ('Wide-column', d_wide, NL), ('Graph', d_graph, NL)]),
             ('DATA SYSTEMS', 'how data is read and moved', [
                ('Row vs column store', d_rowcol, OO), ('Batch ETL', d_etl, DSY), ('Stream of events', d_stream, DSY),
                ('Lake · warehouse', d_lake, DSY)])]
    f.h = gallery(f, bands) + 6
    return f.svg()

def fig_system():
    f = Fig('nsov2', 680, 330, 'ONE REAL DATA SYSTEM · LIVE DATA ON THE LEFT, ANALYTICS ON THE RIGHT',
            'A left-to-right data system. The app writes to an OLTP database, with a cache and a document store '
            'beside it. Change data capture copies every change into a stream of events. The stream lands in a '
            'data lake and a warehouse. From there BI dashboards and machine learning read. Data packets flow '
            'along the arrows. Live side is fast small reads and writes; analytics side is big scans.')
    # zones
    z = f.step(0.1)
    f.add(f'<g class="{z}"><rect x="0" y="34" width="300" height="262" rx="12" fill="rgba(var(--clay-a),.05)" stroke="none"/>'
          f'<rect x="384" y="34" width="296" height="262" rx="12" fill="rgba(var(--violet-a),.05)" stroke="none"/>'
          + text(12, 52, 'LIVE · OLTP', 'sv-hv', B, 'start') + text(668, 52, 'ANALYTICS · OLAP', 'sv-hv', V, 'end')
          + text(150, 288, 'small reads and writes, milliseconds', 'sv-d', 'var(--muted)')
          + text(532, 288, 'big scans, minutes are fine', 'sv-d', 'var(--muted)') + '</g>')
    Y = 160
    N = {'app': (62, Y), 'db': (210, Y), 'cache': (210, 86), 'docs': (210, 234),
         'cdc': (342, Y), 'lake': (470, 104), 'wh': (470, 216), 'bi': (612, 104), 'ml': (612, 216)}
    def E(a, b, d, col='var(--rule-hi)'):
        (x1, y1), (x2, y2) = N[a], N[b]
        f.hedge((x1 + (44 if a != 'cdc' else 40), y1), (x2 - (50 if b not in ('cdc',) else 40), y2), cls=f.step(d, draw=True), col=col)
    f.edge((62, Y - 22), (62, Y - 22), cls='')  # placeholder no-op path keeps step count simple
    f.body.pop()
    E('app', 'db', 0.6, B)
    f.add(f'<path class="{f.step(0.6, draw=True)}" pathLength="1" d="M106,150 C150,150 120,86 158,86" fill="none" stroke="var(--rule-hi)" stroke-width="1.4"/>')
    f.add(f'<path class="{f.step(0.6, draw=True)}" pathLength="1" d="M106,170 C150,170 120,234 158,234" fill="none" stroke="var(--rule-hi)" stroke-width="1.4"/>')
    E('db', 'cdc', 1.3, V)
    E('cdc', 'lake', 1.9, V); E('cdc', 'wh', 1.9, V)
    E('lake', 'bi', 2.6); E('wh', 'bi', 2.6); E('lake', 'ml', 2.6); E('wh', 'ml', 2.6)
    a = f.step(0.3)
    f.node(*N['app'], 'App', 'users click', 'plain', a, None, None, w=88)
    b = f.step(0.9)
    f.node(*N['db'], 'OLTP DB', 'rows, ACID', 'brand', b, '../../../05-sql/01-overview/db-overview/index.html', 'array', w=104)
    f.node(*N['cache'], 'Key-value', 'cache', 'plain', b, NL, 'hash', w=104)
    f.node(*N['docs'], 'Document', 'flexible JSON', 'plain', b, NL, 'tree', w=124)
    c = f.step(1.6)
    f.node(*N['cdc'], 'CDC', 'stream', 'violet', c, DSY, 'list', w=80)
    d = f.step(2.2)
    f.node(*N['lake'], 'Data lake', 'raw files', 'filled', d, DSY, None, w=100)
    f.node(*N['wh'], 'Warehouse', 'column store', 'filled', d, OO, 'array', w=110)
    e = f.step(2.9)
    f.node(*N['bi'], 'BI', 'dashboards', 'plain', e, None, None, w=88)
    f.node(*N['ml'], 'ML', 'features', 'plain', e, None, None, w=88)
    # packets: final frame shows them parked on the arrows
    pk = f.step(3.3)
    f.add(f'<g class="{pk}">' + ''.join(
        f'<rect x="{px-4}" y="{py-4}" width="8" height="8" rx="2" fill="{VTINT}" stroke="{V}" stroke-width="1.1"/>'
        for px, py in ((132, 160), (283, 160), (406, 145), (406, 176), (547, 104), (547, 216))) + '</g>')
    return f.svg()

def put(html, sec_id, svg):
    i = html.index(f'id="{sec_id}"')
    a = html.index('<svg', i)
    b = html.index('</svg>', a) + 6
    return html[:a] + svg + html[b:]

if __name__ == '__main__':
    s = open(PAGE, encoding='utf-8').read()
    s = put(s, 'nsqov-s1', fig_gallery())
    s = put(s, 'nsqov-s2', fig_system())
    open(PAGE, 'w', encoding='utf-8').write(s)
    print('ok')
