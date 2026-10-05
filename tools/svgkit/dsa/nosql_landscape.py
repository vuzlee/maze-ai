"""Figures for content/06-nosql-data/02-nosql/nosql-landscape. Run: python3 nosql_landscape.py > figs.json"""
import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from hldfig import *  # noqa

GH = 'var(--ghost)'
def swap(h):
    # analogous blue-violet palette (same token swap as the Python / CS shelves)
    for a, b in [('var(--filled)', 'var(--brand)'), ('--blue-a', '--clay-a'), ('var(--probe)', 'var(--violet)'),
                 ('var(--ok)', 'var(--filled)'), ('var(--tomb)', 'var(--rose)'), ('--amber-a', '--violet-a'),
                 ('--green-a', '--blue-a'), ('--red-a', '--rose-a')]:
        h = h.replace(a, b)
    return h
def mono(x, y, s, c=TX, a='start'):
    return T(x, y, s.replace('<', '&lt;'), c, a, mono=True)
def qbox(x, y, w, s, title='query'):
    return cap(x, y + 10, title) + R(x, y + 16, w, 28, 'var(--bg)', AM, 6, 1.4) + R(x + 3, y + 21, 3, 18, AM, 'none', 1) + mono(x + 14, y + 35, s)
def ghost(x, y, w, h, rx=4):
    return R(x, y, w, h, 'var(--sunk)', 'none', rx)
OUT = {}

# ---------- 1 mental model: one app, four query shapes ----------
f = Fig('mm-', 720, 330, 'One app sends four kinds of question. Get by key goes to a key-value store, find by field to a document store, append by time to a wide-column store, follow links to a graph database.', 'FOUR QUESTION SHAPES · FOUR FAMILIES')
f(icon('server', 70, 140, 'app'))
fam = [('key-value', 'Redis', 'GET by key'), ('document', 'MongoDB', 'find by field'),
       ('wide-column', 'Cassandra', 'append by time'), ('graph', 'Neo4j', 'follow links')]
for i, (n, ex, q) in enumerate(fam):
    y = 34 + i * 72
    f(icon('db', 560, y, '', None) + T(596, y + 22, n, TX, 'start', 'sv-s') + T(596, y + 38, ex, MU, 'start', 'sv-l'), show=.2 + i * .12)
    t = 1.0 + i * 1.3
    send(f, 100, 164, 530, y + 24, q, t, 'bl', .9, w=112)
    f(icon('db', 560, y, '', 'am') + T(596, y + 22, n, AM, 'start', 'sv-s') + T(596, y + 38, ex, MU, 'start', 'sv-l'), show=t + .9)
f(note(0, 318, 'Pick the family whose shape matches the question you ask most.', GR), show=6.6)
OUT['mm'] = f.render()

# ---------- 2.1 key-value: hash buckets ----------
f = Fig('kv-', 720, 290, 'GET user:42. The key is hashed, hash mod 4 is 2, the store jumps straight to bucket 2 and returns the value. No scan.', 'KEY → HASH → BUCKET → VALUE')
buckets = [['cart:7 → [3 items]'], ['session:a1 → {...}'], ['user:9 → {Bob}', 'user:42 → {Alice}'], ['count:home → 1832']]
BX = 400
for i, es in enumerate(buckets):
    y = 40 + i * 52
    s = R(BX, y, 320, 42, 'var(--bg)', RULE_HI, 6) + T(BX + 18, y + 26, 'b%d' % i, MU, 'middle', mono=True) + L(BX + 34, y + 6, BX + 34, y + 36)
    for j, e in enumerate(es):
        s += R(BX + 42 + j * 138, y + 8, 132, 26, tint('bl', '.10'), BL, 4, 1) + mono(BX + 50 + j * 138, y + 25, e, TX)
    f(s, show=.2 + i * .15)
f(qbox(0, 40, 170, 'GET user:42'), show=1.0)
f(R(120, 140, 200, 44, 'var(--bg)', RULE_HI, 6) + mono(220, 167, 'hash("user:42") % 4', TX, 'middle'), show=1.4)
f(arrow(85, 86, 150, 138, MU), show=1.6, d=.3)
f(R(124, 192, 192, 22, 'var(--bg)', 'none', 4) + mono(220, 208, '= 2', AM, 'middle'), show=2.4)
send(f, 322, 162, BX - 4, 166, 'b2', 2.9, 'am', .8)
f(R(BX + 178, 40 + 2 * 52 + 6, 136, 30, 'none', AM, 5, 1.8), show=3.8)
f(R(BX + 40, 40 + 2 * 52 + 6, 136, 30, 'var(--sunk)', 'none', 5).replace('/>', ' opacity=".7"/>'), show=3.8)
f(pill(220, 236, '{name: "Alice"}', 'gr', 130), show=4.4, move=(4.4, 360, -60, .9))
f(note(0, 278, 'One jump, any size — but you can only ask by the exact key.', GR), show=5.6)
OUT['kv'] = f.render()

# ---------- 2.2 document: JSON documents ----------
f = Fig('doc-', 720, 330, 'Three JSON documents with different fields. The query find city Paris looks inside each document; Alice and Carol match, Bob does not.', 'EACH RECORD IS ONE JSON DOCUMENT')
docs = [['{ _id: 1,', '  name: "Alice",', '  city: "Paris",', '  tags: ["admin"] }'],
        ['{ _id: 2,', '  name: "Bob",', '  city: "Rome",', '  phone: "555-01" }'],
        ['{ _id: 3,', '  name: "Carol",', '  city: "Paris",', '  orders: [ {...} ] }']]
match = [True, False, True]
for i, d in enumerate(docs):
    x = i * 240
    s = R(x, 96, 220, 96, 'var(--bg)', RULE_HI, 6)
    for k, l in enumerate(d):
        s += mono(x + 12, 118 + k * 20, l, TX)
    f(s, show=.2 + i * .3, move=(.2 + i * .3, 0, -30, .6))
f(qbox(0, 30, 270, 'find({ city: "Paris" })'), show=1.4)
for i, m in enumerate(match):
    x, t = i * 240, 2.2 + i * 1.0
    f(R(x + 6, 145, 208, 22, 'none', AM, 4, 1.6), show=t, hide=t + .8)
    if m:
        f(R(x, 96, 220, 96, 'none', GR, 6, 2) + pill(x + 110, 202, 'match', 'gr', 70), show=t + .7)
    else:
        f(ghost(x, 96, 220, 96, 6) + T(x + 110, 150, 'no match', GH, 'middle', 'sv-s'), show=t + .7)
f(note(0, 258, 'Different documents may carry different fields — no ALTER TABLE.', MU), show=5.6)
f(note(0, 280, 'You can query any field inside; an index makes it fast.', GR), show=6.0)
OUT['doc'] = f.render()

# ---------- 2.3 wide-column ----------
f = Fig('wc-', 720, 300, 'Rows keyed by sensor. Each new reading appends a column to the end of its row. The query for sensor A after 10:01 reads one row and a slice of it.', 'ROW KEY → MANY COLUMNS, SORTED BY TIME')
CX0, CW = 120, 92
f(T(60, 72, 'row key', MU) + T(CX0 + 3 * CW, 72, 'column family: readings', MU) + L(0, 80, 720, 80))
rows = [('sensor:A', ['10:00 21°', '10:01 22°', '10:02 22°']), ('sensor:B', ['10:00 18°']), ('sensor:C', ['10:00 30°', '10:01 31°'])]
ry = lambda i: 90 + i * 44
for i, (k, cs) in enumerate(rows):
    s = R(0, ry(i), 112, 34, tint('bl', '.10'), BL, 4) + mono(56, ry(i) + 22, k, TX, 'middle')
    for j, c in enumerate(cs):
        s += R(CX0 + j * CW, ry(i), CW - 6, 34, 'var(--bg)', RULE_HI, 4) + mono(CX0 + j * CW + 43, ry(i) + 22, c, TX, 'middle')
    f(s, show=.2 + i * .2)
# writes append at row end
ws = [(0, 3, '10:03 23°'), (1, 1, '10:03 19°'), (0, 4, '10:04 23°')]
for k, (i, j, v) in enumerate(ws):
    t = 1.2 + k * .9
    f(R(CX0 + j * CW, ry(i), CW - 6, 34, tint('bl', '.10'), BL, 4) + mono(CX0 + j * CW + 43, ry(i) + 22, v, TX, 'middle'),
      show=t, move=(t, 120, 0, .7))
f(qbox(0, 228, 360, "WHERE row = 'sensor:A' AND time > 10:01", 'query'), show=4.2)
f(R(-1, ry(0) - 3, 114, 40, 'none', AM, 5, 1.8), show=4.9)
f(ghost(CX0, ry(0), 2 * CW - 6, 34) + R(0, ry(1) - 4, 720, 92, 'var(--sunk)', 'none', 4).replace('/>', ' opacity=".6"/>'), show=5.4)
f(R(CX0 + 2 * CW - 3, ry(0) - 3, 3 * CW, 40, 'none', GR, 5, 2), show=5.8)
f(note(380, 262, 'one row, one contiguous slice', GR), show=6.3)
OUT['wc'] = f.render()

# ---------- 2.4 graph ----------
f = Fig('gr-', 720, 300, 'A graph of people. The query friends of friends of Alice walks one hop to Bob and Carol, then a second hop to Dan and Eve.', 'NODES + EDGES · A QUERY WALKS THE EDGES')
P = {'Alice': (90, 150), 'Bob': (270, 80), 'Carol': (270, 220), 'Dan': (460, 60), 'Eve': (460, 170), 'Finn': (460, 250)}
E = [('Alice', 'Bob'), ('Alice', 'Carol'), ('Bob', 'Dan'), ('Bob', 'Eve'), ('Carol', 'Eve'), ('Carol', 'Finn')]
for a, b in E:
    f(L(*P[a], *P[b], RULE_HI, 1.4), show=.2)
def node(n, tone=None):
    x, y = P[n]
    fill, st, c = ('var(--bg)', RULE_HI, TX) if tone is None else (tint(tone, '.22'), COL[tone], COL[tone])
    return '<circle cx="%.1f" cy="%.1f" r="26" fill="var(--bg)"/><circle cx="%.1f" cy="%.1f" r="26" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, y, x, y, fill, st) + T(x, y + 4, n, c, 'middle', 'sv-s')
for k, n in enumerate(P):
    f(node(n), show=.3 + k * .1)
f(qbox(505, 30, 212, '(Alice)-[:FRIEND*2]->(x)', 'query'), show=1.2)
f(node('Alice', 'am'), show=1.8)
def hop(a, b, t):
    (x1, y1), (x2, y2) = P[a], P[b]
    import math
    g = math.atan2(y2 - y1, x2 - x1)
    f(arrow(x1 + 26 * math.cos(g), y1 + 26 * math.sin(g), x2 - 28 * math.cos(g), y2 - 28 * math.sin(g), AM, 2), show=t, d=.4)
hop('Alice', 'Bob', 2.4); hop('Alice', 'Carol', 2.4)
f(node('Bob', 'bl') + node('Carol', 'bl') + T(270, 290, 'hop 1', BL, 'middle'), show=3.0)
hop('Bob', 'Dan', 3.8); hop('Bob', 'Eve', 3.8); hop('Carol', 'Finn', 3.8); hop('Carol', 'Eve', 3.8)
f(node('Dan', 'gr') + node('Eve', 'gr') + node('Finn', 'gr') + T(460, 290, 'hop 2 · result', GR, 'middle'), show=4.4)
f(note(540, 160, 'each hop follows a', MU) + note(540, 178, 'stored pointer —', MU) + note(540, 196, 'no JOIN per hop', GR), show=5.2)
OUT['gr'] = f.render()

# ---------- 3.1 schema-on-write ----------
f = Fig('sw-', 720, 270, 'Table users has name NOT NULL. A row without a name is rejected by the database at write time; a complete row slides in.', 'THE DATABASE CHECKS EVERY WRITE')
t = Table(360, 40, [('id', 60, 'INT'), ('name', 140, 'TEXT NOT NULL'), ('city', 120, 'TEXT')], 'users')
f(t.head()); f(t.row(0, ['1', 'Alice', 'Paris']), show=.3); f(t.row(1, ['2', 'Bob', 'Rome']), show=.5)
f(qbox(0, 40, 300, "INSERT (3, NULL, 'Oslo')", 'write'), show=1.0)
f(pill(t.cx(1), t.ry(2) + 3, '3 · NULL · Oslo', 'bl', 140), show=1.6, hide=3.0, move=(1.6, -300, -40, .9))
f(t.colbox(1, 2), show=2.4, hide=3.6)
f(pill(150, 120, '✕ rejected: name is NOT NULL', 'rd', 210), show=3.0, move=(3.0, 140, 30, .6))
f(qbox(0, 160, 300, "INSERT (3, 'Carol', 'Oslo')", 'write'), show=4.2)
f(t.row(2, ['3', 'Carol', 'Oslo'], 'gr'), show=4.8, move=(4.8, -300, 40, .9))
f(note(0, 258, 'Every row has the same shape — changing it needs a migration.', MU), show=6.0)
OUT['sw'] = f.render()

# ---------- 3.2 schema-on-read ----------
f = Fig('sr-', 720, 300, 'A collection accepts three documents of different shapes from three app versions. Later the reader code must handle every shape; the one with fullName instead of name breaks it.', 'ANY SHAPE IS ACCEPTED · THE CODE CHECKS ON READ')
dv = [('v1', '{ name: "Alice" }'), ('v2', '{ fullName: "Bob" }'), ('v3', '{ name: "Carol", age: 31 }')]
for i, (v, d) in enumerate(dv):
    y = 40 + i * 44
    f(T(0, y + 22, 'app ' + v, MU, 'start', 'sv-s'), show=.3 + i * .7)
    f(R(380, y, 240, 32, tint('bl', '.10'), BL, 5) + mono(392, y + 21, d) + T(640, y + 21, '✓ stored', BL, 'start'), show=.3 + i * .7, move=(.3 + i * .7, -300, 0, .7))
f(qbox(0, 180, 300, 'print(doc["name"])', 'reader code, later'), show=2.8)
for i, ok in enumerate([True, False, True]):
    y, tt = 40 + i * 44, 3.6 + i * .9
    f(R(377, y - 3, 246, 38, 'none', AM, 6, 1.8), show=tt, hide=tt + .8)
    f(pill(330, y + 6, 'Alice' if i == 0 else ('KeyError' if not ok else 'Carol'), 'gr' if ok else 'rd', 80), show=tt + .6)
f(note(0, 262, 'The schema did not go away — it moved into every reader.', GR), show=6.6)
f(note(0, 284, 'Good when records truly differ; bad when you only dread migrations.', MU), show=7.0)
OUT['sr'] = f.render()

# ---------- 4 query-driven design ----------
f = Fig('qd-', 720, 372, 'List the queries first: orders by customer and orders by day. Build one table per query. A new order is written to both tables.', 'QUERIES FIRST · ONE TABLE PER QUERY')
f(qbox(0, 30, 330, 'Q1  orders of customer X', 'query list'), show=.2)
f(qbox(380, 30, 340, 'Q2  orders placed on day D', 'query list').replace('query list', ''), show=.6)
a = Table(0, 110, [('customer', 110), ('order', 90), ('total', 90)], 'orders_by_customer')
b = Table(380, 110, [('day', 110), ('order', 90), ('total', 90)], 'orders_by_day')
f(a.head(), show=1.2); f(a.row(0, ['Alice', '#5', '$20']), show=1.4); f(a.row(1, ['Bob', '#6', '$35']), show=1.5)
f(b.head(), show=1.6); f(b.row(0, ['Oct 5', '#5', '$20']), show=1.8); f(b.row(1, ['Oct 6', '#6', '$35']), show=1.9)
f(icon('server', 330, 250, 'new order #7'), show=2.6)
send(f, 308, 258, a.cx(1), a.ry(2) + 30, '#7', 3.2, 'am', .8)
send(f, 352, 258, b.cx(1), b.ry(2) + 30, '#7', 3.2, 'am', .8)
f(a.row(2, ['Alice', '#7', '$12'], 'gr') + b.row(2, ['Oct 6', '#7', '$12'], 'gr'), show=4.1)
f(note(0, 350, 'Same order stored twice, on purpose — no JOIN at read time.', GR), show=4.8)
f(note(720, 350, 'cost: two writes', RD, 'end'), show=5.3)
OUT['qd'] = f.render()

# ---------- 5 polyglot persistence ----------
f = Fig('pg-', 720, 330, 'The app writes only to Postgres, the source of truth. Changes are copied to Redis for cache and to Elasticsearch for search. Reads go to the store that fits.', 'ONE SOURCE OF TRUTH · REBUILDABLE COPIES')
f(icon('user', 40, 110, 'user'))
f(icon('server', 180, 110, 'app'), show=.2)
f(icon('db', 360, 110, 'Postgres', 'gr', 'source of truth'), show=.4)
f(icon('cache', 600, 30, 'Redis', None, 'cache · sessions'), show=.6)
f(icon('db', 600, 190, 'Elasticsearch', None, 'search index'), show=.8)
send(f, 68, 134, 152, 134, 'buy', 1.2, 'bl', .6)
send(f, 208, 134, 332, 134, 'write', 2.0, 'gr', .7)
send(f, 388, 120, 572, 60, 'copy', 3.0, None, .8, dash='5 4')
send(f, 388, 148, 572, 210, 'copy', 3.0, None, .8, dash='5 4')
f(note(470, 168, 'async', MU, 'middle'), show=3.6)
f(T(0, 240, '1 written directly', GR, 'start', 'sv-s') + T(0, 258, '2 copies can be deleted and rebuilt', MU, 'start', 'sv-s'), show=4.4)
f(note(0, 302, 'each extra store = one more sync path to run', RD), show=5.2)
OUT['pg'] = f.render()

print(json.dumps({k: swap(v) for k, v in OUT.items()}))
