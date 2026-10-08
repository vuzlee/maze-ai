# -*- coding: utf-8 -*-
"""SQL & relational shelf overview: gallery of the field, data-model pendulum, types of database.

    python3 tools/svgkit/05-sql/db_overview.py   # rewrites sections 01-03 in place (re-runnable)
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from overview import Fig, text, cell, dot, ln, arr, gallery

PAGE = 'content/05-sql/01-overview/db-overview/index.html'
RB, SB, SA = '../../02-relational-basics/', '../../03-sql-basics/', '../../04-sql-advanced/'
B, V, R = 'var(--brand)', 'var(--violet)', 'var(--rose)'
TINT, VT = 'rgba(var(--clay-a),.10)', 'rgba(var(--violet-a),.14)'
MONO = ';font-family:var(--mono);font-size:8.5px'

def t(x, y, s, col='var(--muted)', a='middle', ex=''):
    return text(x, y, s, 'sv-d', col, a, MONO + ex)

def table(x, y, cols, rows, cw=20, rh=11, hl_rows=(), hl_col=None, head=True):
    o = ''
    for c in range(cols):
        o += f'<rect x="{x+c*cw}" y="{y}" width="{cw}" height="{rh}" fill="{"rgba(var(--clay-a),.18)" if head else TINT}" stroke="{B}" stroke-width=".9"/>'
    for r in range(rows):
        for c in range(cols):
            hl = r in hl_rows or c == hl_col
            o += f'<rect x="{x+c*cw}" y="{y+(r+1)*rh}" width="{cw}" height="{rh}" fill="{VT if hl else "var(--bg)"}" stroke="{V if hl else B}" stroke-width=".9"/>'
    return o

# ---- MODEL ----
def d_table(x, y):
    o = table(x + 14, y + 6, 4, 3, 26, 12)
    o += t(x + 27, y + 15, 'id', 'var(--brand-hi)') + t(x + 53, y + 15, 'name', 'var(--brand-hi)')
    o += ln(x + 120, y + 18, x + 120, y + 48, V, 1) + t(x + 128, y + 34, 'row', V, 'start')
    o += t(x + 66, y + 62, '← column →', V)
    o += f'<rect x="{x+14}" y="{y+30}" width="104" height="12" fill="none" stroke="{V}" stroke-width="1.4"/>'
    return o
def d_keys(x, y):
    o = table(x + 2, y + 10, 2, 3, 22, 12, hl_col=0) + table(x + 84, y + 10, 3, 3, 18, 12, hl_col=2)
    o += t(x + 13, y + 6, 'PK', V) + t(x + 129, y + 6, 'FK', V)
    o += f'<path d="M{x+129},{y+52} C{x+129},{y+64} {x+13},{y+64} {x+13},{y+52}" fill="none" stroke="{V}" stroke-width="1.2"/>'
    o += f'<path d="M{x+10},{y+55} L{x+13},{y+50} L{x+16},{y+55}z" fill="{V}"/>'
    return o
def d_norm(x, y):
    o = table(x + 2, y + 12, 4, 2, 13, 11, hl_col=3)
    o += arr(x + 58, y + 30, x + 72)
    o += table(x + 76, y + 6, 2, 2, 13, 10) + table(x + 108, y + 26, 2, 2, 13, 10, hl_col=1)
    o += t(x + 28, y + 64, '1 table', 'var(--muted)') + t(x + 108, y + 64, '2 tables', V)
    return o
def d_er(x, y):
    o = ''
    for ex, lab in ((x + 2, 'User'), (x + 98, 'Order')):
        o += f'<rect x="{ex}" y="{y+18}" width="40" height="20" rx="2" fill="{TINT}" stroke="{B}" stroke-width="1"/>' + t(ex + 20, y + 31, lab, 'var(--text)')
    o += f'<path d="M{x+70},{y+16} L{x+86},{y+28} L{x+70},{y+40} L{x+54},{y+28}z" fill="{VT}" stroke="{V}" stroke-width="1"/>'
    o += ln(x + 42, y + 28, x + 54, y + 28, B) + ln(x + 86, y + 28, x + 98, y + 28, B)
    o += t(x + 70, y + 31, 'has', V) + t(x + 48, y + 22, '1', 'var(--muted)') + t(x + 92, y + 22, 'N', 'var(--muted)')
    o += t(x + 70, y + 58, 'entities + relationships')
    return o

# ---- QUERY ----
def d_select(x, y):
    o = table(x + 4, y + 4, 4, 4, 18, 11, hl_rows=(1, 3))
    o += arr(x + 82, y + 32, x + 98, V) + table(x + 102, y + 21, 2, 2, 16, 11, hl_rows=(0, 1))
    o += t(x + 40, y + 66, 'WHERE', V, 'middle', ';font-weight:600')
    return o
def d_join(x, y):
    o = table(x + 2, y + 6, 2, 3, 16, 11) + table(x + 44, y + 6, 2, 3, 16, 11)
    o += ln(x + 34, y + 23, x + 44, y + 23, V, 1.2) + ln(x + 34, y + 34, x + 44, y + 34, V, 1.2)
    o += arr(x + 80, y + 28, x + 94) + table(x + 96, y + 6, 4, 3, 10, 11, hl_rows=(0, 1, 2))
    o += t(x + 38, y + 64, 'ON a.id = b.id', V)
    return o
def d_group(x, y):
    o = ''
    for i, (n, h) in enumerate(((3, 'A'), (2, 'B'), (4, 'C'))):
        bx = x + 8 + i * 44
        o += f'<rect x="{bx}" y="{y+6}" width="34" height="38" rx="4" fill="{TINT}" stroke="{B}" stroke-width="1"/>'
        o += ''.join(dot(bx + 9 + (k % 2) * 16, y + 15 + (k // 2) * 10, '', False, 3.5) for k in range(n))
        o += t(bx + 17, y + 56, f'{h}: {n}', V, 'middle', ';font-weight:600')
    return o
def d_cte(x, y):
    o = f'<rect x="{x+2}" y="{y+4}" width="134" height="52" rx="4" fill="none" stroke="{B}" stroke-width="1"/>'
    o += t(x + 8, y + 16, 'WITH big AS (', 'var(--text)', 'start')
    o += f'<rect x="{x+16}" y="{y+21}" width="110" height="14" rx="3" fill="{VT}" stroke="{V}" stroke-width="1"/>'
    o += t(x + 22, y + 31, 'SELECT … WHERE', V, 'start')
    o += t(x + 8, y + 50, ') SELECT … FROM big', 'var(--text)', 'start')
    return o
def d_window(x, y):
    o = ''
    for r in range(6):
        hl = r < 3
        o += cell(x + 20, y + 2 + r * 9.5, 40, 9, '', False)
    o += f'<rect x="{x+16}" y="{y}" width="48" height="31" rx="4" fill="none" stroke="{V}" stroke-width="1.5"/>'
    o += f'<rect x="{x+16}" y="{y+29}" width="48" height="31" rx="4" fill="none" stroke="{B}" stroke-width="1.2" stroke-dasharray="3 2"/>'
    o += ''.join(t(x + 78, y + 9 + r * 9.5, str(r % 3 + 1), V if r < 3 else 'var(--muted)', 'start') for r in range(6))
    o += t(x + 92, y + 22, 'rank', V, 'start') + t(x + 92, y + 52, 'partition', 'var(--muted)', 'start')
    return o
def d_index(x, y):
    o = cell(x + 52, y + 2, 34, 13, '40')
    for i, lab in enumerate(('10 20', '50 60', '80 90')):
        cx = x + 6 + i * 46
        o += ln(x + 69, y + 15, cx + 18, y + 26) + cell(cx, y + 26, 36, 13, lab, i == 1)
    o += ln(x + 69, y + 15, x + 70, y + 26, V, 1.4)
    o += t(x + 69, y + 54, 'B-tree: 3 hops, not a scan', V)
    return o
def d_tx(x, y):
    o = t(x + 2, y + 10, 'BEGIN', V, 'start', ';font-weight:600')
    for i, s in enumerate(('−100 from A', '+100 to B')):
        o += f'<rect x="{x+12}" y="{y+16+i*14}" width="90" height="12" rx="2" fill="{TINT}" stroke="{B}" stroke-width=".9"/>' + t(x + 18, y + 25 + i * 14, s, 'var(--text)', 'start')
    o += f'<path d="M{x+6},{y+14} V{y+44}" stroke="{V}" stroke-width="1.4"/>'
    o += t(x + 2, y + 56, 'COMMIT', V, 'start', ';font-weight:600') + t(x + 136, y + 56, 'all or none', 'var(--muted)', 'end')
    return o

MODEL = [('Table · row · column', d_table, RB + 'relational-model/index.html'),
         ('Primary · foreign key', d_keys, RB + 'constraints-integrity/index.html'),
         ('Normalization', d_norm, RB + 'db-normalization/index.html'),
         ('ER diagram', d_er, RB + 'er-modeling/index.html')]
QUERY = [('SELECT · WHERE', d_select, SB + 'sql-select-filter/index.html'),
         ('JOIN', d_join, SB + 'sql-join/index.html'),
         ('GROUP BY', d_group, SB + 'sql-group-aggregate/index.html'),
         ('Subquery · CTE', d_cte, SB + 'sql-subquery-cte/index.html'),
         ('Window function', d_window, SA + 'sql-window-functions/index.html'),
         ('Index', d_index, SA + 'sql-index-query-plan/index.html'),
         ('Transaction', d_tx, SA + 'transaction-isolation/index.html')]

def fig_gallery():
    f = Fig('dbov1', 680, 400, 'THE WHOLE FIELD · HOW DATA IS SHAPED, HOW IT IS ASKED',
            'Two galleries. Model, how data is shaped: a table of rows and columns; a primary key and a foreign key '
            'arrow between two tables; normalization splitting one table into two; an ER diagram of User has Order. '
            'Query, how it is asked: SELECT with WHERE keeping some rows; JOIN of two tables on matching ids; GROUP BY '
            'putting rows into buckets with counts; a subquery or CTE nested inside a query; a window function ranking '
            'rows within each partition; a B-tree index reaching a row in three hops; a transaction BEGIN, two '
            'updates, COMMIT, all or none. Each tile links to its lesson.')
    f.h = gallery(f, [('MODEL', 'how data is shaped', MODEL), ('QUERY', 'how it is asked', QUERY)]) + 4
    return f.svg()

def fig_pendulum():
    H = 334
    f = Fig('dbov2', 680, H, 'THE DATA-MODEL PENDULUM · STRICT SCHEMA ↔ FREE SCHEMA, 1966 → 2012',
            'A pendulum hangs from a pivot at the top and swings along an arc between strict schema on the left and '
            'free schema on the right. Stops along the arc, in date order: hierarchical IMS in 1966, rigid trees; '
            'the relational model by Codd in 1970 and SQL standardised in 1986, strict tables but any question; '
            'object databases in the 1990s, swinging toward free; NoSQL in 2009, schema-free and easy to scale; '
            'NewSQL and Spanner in 2012, swinging back toward SQL with scale added. The final position of the bob is '
            'NewSQL, near the relational side.')
    import math
    px, py, Rr = 340, 34, 215
    def pos(deg):
        a = math.radians(deg)
        return px + Rr * math.sin(a), py + Rr * math.cos(a)
    # arc
    a0, a1 = pos(-62), pos(62)
    f.add(f'<g class="{f.step(0.1)}"><path d="M{a0[0]:.1f},{a0[1]:.1f} A{Rr},{Rr} 0 0 0 {a1[0]:.1f},{a1[1]:.1f}" fill="none" stroke="var(--rule-hi)" stroke-width="1.2" stroke-dasharray="4 3"/>'
          + f'<circle cx="{px}" cy="{py}" r="4" fill="var(--muted)"/>'
          + text(30, 306, '← STRICT SCHEMA', 'sv-hv', B, 'start') + text(650, 306, 'FREE SCHEMA →', 'sv-hv', V, 'end')
          + text(30, 320, 'tables, types, rules checked', 'sv-d', 'var(--muted)', 'start')
          + text(650, 320, 'any shape, checked by the app', 'sv-d', 'var(--muted)', 'end') + '</g>')
    stops = [(-60, '1966', 'IMS · hierarchical', 'rigid trees', 'left'),
             (-34, '1970 · 1986', 'Codd · SQL', 'strict tables, any question', 'left'),
             (24, '1990s', 'Object DBs', 'store objects as-is', 'right'),
             (56, '2009', 'NoSQL', 'no schema, easy scale', 'right'),
             (-12, '2012', 'NewSQL · Spanner', 'SQL again, at scale', 'below')]
    for i, (deg, yr, name, note, side) in enumerate(stops):
        x, y = pos(deg)
        last = i == len(stops) - 1
        s = f.step(0.6 + i * 0.5)
        col = V if last else B
        o = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{VT if last else "var(--bg)"}" stroke="{col}" stroke-width="1.4"/>'
        if side == 'left':
            tx, ty, an = x - 12, y - 18, 'end'
        elif side == 'right':
            tx, ty, an = x + 12, y - 18, 'start'
        else:
            tx, ty, an = x, y + 28, 'middle'
        o += text(tx, ty, yr, 'sv-d', col, an, ';font-family:var(--mono);font-weight:600')
        o += text(tx, ty + 14, name, 'sv-s', 'var(--text)', an, ';font-weight:600')
        o += text(tx, ty + 27, note, 'sv-d', 'var(--muted)', an)
        f.add(f'<g class="{s}">{o}</g>')
    # rod and bob at final position
    bx, by = pos(-12)
    f.add(f'<g class="{f.step(3.2)}"><line x1="{px}" y1="{py}" x2="{bx:.1f}" y2="{by-12:.1f}" stroke="{V}" stroke-width="1.6"/>'
          f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="12" fill="{VT}" stroke="{V}" stroke-width="1.6"/></g>')
    # swing trail
    f.add(f'<g class="{f.step(2.6)}">' + ''.join(
        f'<path d="M{pos(a)[0]:.1f},{pos(a)[1]-30:.1f} A{Rr-30},{Rr-30} 0 0 {sw} {pos(b)[0]:.1f},{pos(b)[1]-30:.1f}" fill="none" stroke="var(--faint)" stroke-width="1"/>'
        for a, b, sw in ()) + '</g>')
    return f.svg()

def fig_types():
    H = 214
    f = Fig('dbov3', 680, H, 'FOUR SHAPES OF DATABASE · SAME CUSTOMER, STORED FOUR WAYS',
            'Four panels side by side, each storing the same customer. Relational: two tables, users and orders, '
            'joined by a key — fixed schema, joins, transactions. Key-value: a key user:42 pointing to an opaque '
            'value — fastest lookup by key only. Document: one nested JSON document with the orders inside — '
            'flexible shape, read in one go. Graph: nodes for the user and products, edges for bought and '
            'follows — relationships first.')
    PW = 163
    def panel(i, title, use, body, hl=False):
        x = i * (PW + 9)
        o = (f'<rect class="nd" x="0" y="0" width="{PW}" height="{H-34}" rx="10" fill="var(--bg)" stroke="var(--rule-hi)" stroke-width="1.2"/>'
             + text(12, 20, title, 'sv-s', 'var(--text)', 'start', ';font-weight:600;font-size:11.5px')
             + body + text(PW / 2, H - 46, use, 'sv-d', V if hl else 'var(--muted)', 'middle', ';font-style:italic'))
        f.add(f'<g class="{f.step(0.2 + i * 0.45)}"><g transform="translate({x},30)">{o}</g></g>')
    b = table(14, 46, 3, 3, 22, 13, hl_col=0) + table(96, 58, 2, 3, 22, 13, hl_col=1)
    b += t(47, 42, 'users', 'var(--brand-hi)') + t(118, 54, 'orders', 'var(--brand-hi)')
    b += f'<path d="M129,110 C129,128 25,128 25,110" fill="none" stroke="{V}" stroke-width="1.2"/>'
    panel(0, 'Relational', 'schema · JOIN · ACID', b, True)
    b = ''
    for k, (kk, vv) in enumerate((('user:42', '▒▒▒▒'), ('cart:42', '▒▒'), ('sess:9f', '▒▒▒'))):
        yy = 42 + k * 28
        b += f'<rect x="12" y="{yy}" width="62" height="18" rx="3" fill="{VT if k == 0 else TINT}" stroke="{V if k == 0 else B}" stroke-width="1"/>' + t(43, yy + 12, kk, V if k == 0 else 'var(--text)')
        b += arr(76, yy + 9, 94) + f'<rect x="96" y="{yy}" width="54" height="18" rx="3" fill="var(--sunk)" stroke="var(--rule-hi)" stroke-width="1"/>' + t(123, yy + 12, 'blob')
    panel(1, 'Key-value', 'lookup by key only', b)
    lines = ['{ "id": 42,', '  "name": "Lan",', '  "orders": [', '    { "sku": "A1" },', '    { "sku": "B7" }', '  ] }']
    b = f'<rect x="12" y="34" width="139" height="94" rx="4" fill="{TINT}" stroke="{B}" stroke-width="1"/>'
    b += f'<rect x="16" y="68" width="131" height="54" rx="3" fill="{VT}" stroke="{V}" stroke-width=".9"/>'
    b += ''.join(t(20, 48 + k * 14.5, s, V if 2 <= k <= 5 else 'var(--text)', 'start') for k, s in enumerate(lines))
    panel(2, 'Document', 'nested · flexible shape', b)
    N = {'u': (40, 62), 'p1': (122, 50), 'p2': (122, 112), 'u2': (40, 118)}
    N = {'u': (34, 64), 'p1': (128, 50), 'p2': (128, 112), 'u2': (34, 118)}
    b = ln(*N['u'], *N['p1'], V, 1.3) + ln(*N['u'], *N['p2'], V, 1.3) + ln(*N['u2'], *N['p2'], B, 1.1) + ln(*N['u'], *N['u2'], B, 1.1, True)
    b += t(84, 48, 'bought', V) + t(28, 94, 'follows', 'var(--muted)', 'end') if False else t(84, 48, 'bought', V) + t(46, 92, 'follows', 'var(--muted)', 'start')
    b += ''.join(f'<circle cx="{N[k][0]}" cy="{N[k][1]}" r="14" fill="var(--bg)"/>' for k in N)
    b += dot(*N['u'], 'Lan', True, 14) + dot(*N['u2'], 'Minh', False, 14) + dot(*N['p1'], 'A1', False, 12) + dot(*N['p2'], 'B7', False, 12)
    panel(3, 'Graph', 'relationships first', b)
    return f.svg()

def mtab(x, y, rows, hl=(), strike=(), newcol=False, cw=52, rh=13):
    o = ''
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            head = r == 0
            on = r in hl or (newcol and c == len(row) - 1)
            fill = 'rgba(var(--clay-a),.18)' if head else (VT if on else ('rgba(var(--rose-a),.10)' if r in strike else 'var(--bg)'))
            st = V if on else (R if r in strike else B)
            o += f'<rect x="{x+c*cw}" y="{y+r*rh}" width="{cw}" height="{rh}" fill="{fill}" stroke="{st}" stroke-width=".9"/>'
            o += t(x + c * cw + cw / 2, y + r * rh + 9.5, v, V if on else (R if r in strike else ('var(--brand-hi)' if head else 'var(--text)')))
        if r in strike:
            o += ln(x + 3, y + r * rh + 6.5, x + len(row) * cw - 3, y + r * rh + 6.5, R, 1.2)
    return o

def fig_commands():
    H = 246
    f = Fig('dbov4', 680, H, 'SQL COMMANDS · DEFINE THE SHAPE, CHANGE THE ROWS, CONTROL WHO MAY',
            'Five panels, each a tiny customers table before and after one statement. DDL: ALTER TABLE adds an email '
            'column; CREATE, ALTER, DROP and TRUNCATE change the shape of tables. INSERT adds a new row, Carol from Oslo. '
            'UPDATE with WHERE id = 2 changes Bob’s city to Berlin; without WHERE every row changes. DELETE with WHERE '
            'id = 1 removes Alice; without WHERE every row is deleted. DCL: GRANT SELECT ON orders TO analyst lets the '
            'analyst read but a DELETE is not granted; REVOKE takes the right back.')
    PW, GX = 128, 10
    base = [['name', 'city'], ['Alice', 'Paris'], ['Bob', 'Rome']]
    P = [('DDL', 'shape of tables', mtab(14, 0, base, cw=50), mtab(4, 0, [['name', 'city', 'email'], ['Alice', 'Paris', ''], ['Bob', 'Rome', '']], newcol=True, cw=40),
          ['ALTER TABLE customers', '  ADD email', 'CREATE · DROP · TRUNCATE']),
         ('INSERT', 'add a row', mtab(14, 0, base, cw=50), mtab(14, 0, base + [['Carol', 'Oslo']], hl=(3,), cw=50),
          ['INSERT INTO customers', "  VALUES ('Carol','Oslo')"]),
         ('UPDATE', 'change rows', mtab(14, 0, base, cw=50), mtab(14, 0, [['name', 'city'], ['Alice', 'Paris'], ['Bob', 'Berlin']], hl=(2,), cw=50),
          ["UPDATE … SET city='Berlin'", '  WHERE id = 2', 'no WHERE → every row']),
         ('DELETE', 'remove rows', mtab(14, 0, base, cw=50), mtab(14, 0, base, strike=(1,), cw=50),
          ['DELETE FROM customers', '  WHERE id = 1', 'no WHERE → every row']),
         ('DCL', 'who may do what', '', '', ['GRANT SELECT ON orders', '  TO analyst', 'REVOKE takes it back'])]
    for i, (name, sub, before, after, stmt) in enumerate(P):
        x = i * (PW + GX)
        o = (f'<rect class="nd" x="0" y="0" width="{PW}" height="{H-34}" rx="10" fill="var(--bg)" stroke="var(--rule-hi)" stroke-width="1.2"/>'
             + text(12, 20, name, 'sv-s', 'var(--text)', 'start', ';font-weight:600;font-size:11.5px')
             + text(12, 33, sub, 'sv-d', 'var(--muted)', 'start', ';font-size:9.5px'))
        if name == 'DCL':
            o += f'<g transform="translate(0,44)">' + text(PW / 2, 14, 'analyst', 'sv-s', 'var(--text)', 'middle', ';font-weight:600')
            for k, (op, ok) in enumerate((('SELECT', True), ('INSERT', False), ('DELETE', False))):
                yy = 26 + k * 22
                o += (f'<rect x="20" y="{yy}" width="88" height="17" rx="3" fill="{VT if ok else "var(--sunk)"}" stroke="{V if ok else "var(--rule-hi)"}" stroke-width="1"/>'
                      + t(30, yy + 12, op, V if ok else 'var(--faint)', 'start') + t(100, yy + 12, '✓' if ok else '✕', V if ok else R, 'end', ';font-weight:700'))
            o += '</g>'
        else:
            o += f'<g transform="translate(0,42)">{before}</g>' + text(PW / 2, 96, '↓', 'sv-s', 'var(--muted)')
            o += f'<g transform="translate(0,102)">{after}</g>'
        for k, line in enumerate(stmt):
            o += t(10, 170 + k * 12, line, 'var(--muted)' if k == 2 else V, 'start', ';font-size:8px')
        f.add(f'<g class="{f.step(0.2 + i * 0.4)}"><g transform="translate({x},30)">{o}</g></g>')
    return f.svg()

SEC = lambda n, title, key, body, why: f'''<section id="dbov-s{n}" class="lesson">
  <div class="sh"><b>0{n}</b><h2>{title}</h2></div>
  <p class="key">{key}</p>
<figure class="gist">
{body}
</figure>
  <ul class="why">
{why}
  </ul>
</section>

'''

def sections():
    return (SEC(1, 'What SQL &amp; relational is',
                'Relational data is <em>tables linked by keys</em>; SQL is <em>one language to ask them anything</em>. This shelf is these eleven pictures.',
                fig_gallery(),
                '    <li>Model first: a well-shaped table makes every later query short.</li>\n'
                '    <li>Every query is a pipeline of the same moves — filter, join, group, rank — and an index decides how fast it runs.</li>')
            + SEC(2, 'Data-model pendulum',
                  'Databases have swung <em>between strict and free schema</em> for sixty years — and keep swinging back to SQL.',
                  fig_pendulum(),
                  '    <li>Each swing fixed the last one’s pain: rigid trees → any question; slow joins at scale → no schema; lost guarantees → SQL at scale.</li>\n'
                  '    <li>Today the default is a relational database; other shapes are chosen for one specific need.</li>')
            + SEC(3, 'Types of database',
                  'Four shapes for the same data — pick by <em>how you will read it</em>.',
                  fig_types(),
                  '    <li>Unsure? Start relational. Move a piece out only when one access pattern clearly fits another shape.</li>\n'
                  '    <li>The other three are taught on the <a href="../../../06-nosql-data/02-nosql/nosql-landscape/index.html">NoSQL shelf</a>.</li>')
            + SEC(4, 'SQL commands',
                  'Beyond asking, SQL <em>defines the shape</em>, <em>changes the rows</em> and <em>controls who may</em>.',
                  fig_commands(),
                  '    <li>DDL — <code>CREATE</code> · <code>ALTER</code> · <code>DROP</code> · <code>TRUNCATE</code>; DML — <code>INSERT</code> · <code>UPDATE</code> · <code>DELETE</code>; DCL — <code>GRANT</code> · <code>REVOKE</code>.</li>\n'
                  '    <li>An <code>UPDATE</code> or <code>DELETE</code> without <code>WHERE</code> touches every row — run it inside a <a href="../../04-sql-advanced/transaction-isolation/index.html">transaction</a>.</li>'))

if __name__ == '__main__':
    s = open(PAGE, encoding='utf-8').read()
    a = s.index('<section id="dbov-s1"')
    lo = s.index('<h2>Learning order</h2>')
    b = s.rindex('<section id=', 0, lo)
    tail = re.sub(r'<section id="dbov-s\d+" class="lesson">\n  <div class="sh"><b>\d+</b><h2>Learning order',
                  '<section id="dbov-s5" class="lesson">\n  <div class="sh"><b>05</b><h2>Learning order', s[b:], 1)
    s = s[:a] + sections() + tail
    s = re.sub(r'<p class="lede">.*?</p>', '<p class="lede">Data lives in <b>tables linked by keys</b>, and <b>one language, SQL,</b> shapes it, changes it and asks it anything — the side the pendulum keeps swinging back to.</p>', s, 1, flags=re.S)
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="What relational data and SQL are in eleven pictures, how data models swung between strict and free schema from IMS to Spanner, the four types of database, the SQL command families, and the order to learn this shelf."', s, 1)
    open(PAGE, 'w', encoding='utf-8').write(s)
    print('ok')
