"""Figures for content/06-nosql-data/03-data-systems/data-systems (visual-first rework).
Written with tablefig/hldfig tones (am=highlight, gr=result, rd=error, bl=data), then remapped
to the analogous blue-violet palette at the end. Output: /tmp/nosql/figs.json"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from hldfig import *  # noqa

def go(f, x1, y1, x2, y2, text, t, tone='bl', dur=.9):
    """Arrow draws in, a short pill rides along it (centred on the line) and vanishes on arrival."""
    f(arrow(x1, y1, x2, y2, COL[tone], 1.5), show=t, d=.25)
    w = 18 + len(text) * 6.4
    import math
    L_ = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L_, (y2 - y1) / L_
    a = w / 2 + 4 if abs(ux) > .5 else 14
    b = w / 2 + 10 if abs(ux) > .5 else 20
    sx, sy = x1 + ux * a, y1 + uy * a
    ex, ey = x2 - ux * b, y2 - uy * b
    f(pill(ex, ey - 10, text, tone, w), show=t, hide=t + dur + .1, move=(t, sx - ex, sy - ey, dur), d=.15)
    return t + dur

def badge(cx, y, n):
    return ('<circle cx="%.1f" cy="%.1f" r="9" fill="%s"/>' % (cx, y, AM) +
            T(cx, y + 4, str(n), 'var(--on-fill)', 'middle', 'sv-d', bold=True))

figs = {}
Y = 34; E = Y + 24          # icon top, link height

# ---- 1 mental model -------------------------------------------------------------------
f = Fig('ds1-', 720, 172, 'An order is written by the app into the OLTP database. A nightly pipeline copies the rows, cleans them and loads them into the warehouse. The dashboard asks the warehouse for a sum and shows revenue.',
        'WRITE SIDE → PIPELINE → READ SIDE')
xs = [40, 200, 360, 520, 680]
for k, (kind, lab) in enumerate([('server', 'app'), ('db', 'OLTP db'), ('worker', 'pipeline'), ('db', 'warehouse'), ('client', 'dashboard')]):
    f(icon(kind, xs[k], Y, lab))
t = .5
for k, txt in enumerate(['order', 'rows', 'clean', 'SUM']):
    t = go(f, xs[k] + 28, E, xs[k + 1] - 28, E, txt, t, 'bl') + .35
    f(ring(xs[k + 1], Y), show=t - .35, hide=t + .9 if k < 3 else None, d=.2)
f(pill(660, 128, 'revenue 70', 'gr'), show=t + .2)
f(R(0, 128, 410, 20, 'none', 'none') + T(0, 142, 'app writes one row at a time', MU, 'start'), show=t + .6)
figs['s1'] = f.render()

# ---- 2.1 warehouse --------------------------------------------------------------------
def store_fig(pre, aria, caption, lake):
    f = Fig(pre, 720, 196, aria, caption)
    if not lake:
        nodes = [('server', 'source'), ('worker', 'clean + schema'), ('db', 'warehouse'), ('client', 'reader')]
    else:
        nodes = [('server', 'source'), ('db', 'lake'), ('worker', 'parse + schema'), ('client', 'reader')]
    xs = [40, 250, 460, 670]
    for k, (kind, lab) in enumerate(nodes):
        f(icon(kind, xs[k], Y, lab))
    if not lake:
        t = go(f, 68, E, 222, E, 'age=-3', .5, 'rd')
        f(ring(250, Y, c=RD), show=t, hide=t + 1.2, d=.2)
        f(T(250, Y + 112, '✕ rejected on write', RD, 'middle'), show=t + .2)
        t = go(f, 68, E, 222, E, 'row', t + 1.3, 'bl')
        f(ring(250, Y), show=t, hide=t + 1, d=.2)
        t = go(f, 278, E, 432, E, 'typed row', t + .2, 'bl')
        t = go(f, 642, E, 488, E, 'SQL', t + .5, 'bl')
        f(pill(670, 116, 'answer', 'gr'), show=t + .2)
        f(R(170, 150, 160, 34, 'none', AM, 8, 1.4, '4 3') + T(250, 171, 'cost paid on write', AM, 'middle', bold=True), show=t + .8)
    else:
        t = .5
        for txt in ['json', 'csv', 'log']:
            t = go(f, 68, E, 222, E, txt, t, 'bl', .7) + .1
        f(T(250, Y + 112, 'stored as-is, cheap', MU, 'middle'), show=t)
        t = go(f, 642, E, 488, E, 'query', t + .5, 'bl')
        f(ring(460, Y), show=t, hide=t + 2.2, d=.2)
        t = go(f, 432, E, 278, E, 'read files', t + .2, 'bl')
        t = go(f, 488, E + 14, 642, E + 14, 'rows', t + .4, 'gr')
        f(pill(670, 116, 'answer', 'gr'), show=t + .2)
        f(R(380, 150, 160, 34, 'none', AM, 8, 1.4, '4 3') + T(460, 171, 'cost paid on read', AM, 'middle', bold=True), show=t + .8)
    return f.render()
figs['s2a'] = store_fig('ds2a-', 'Warehouse, schema on write: a bad row with age -3 is rejected by the clean-and-schema step before storage; a good row is typed and stored; the reader sends SQL and gets the answer straight away. The cost is paid on write.', 'SCHEMA ON WRITE', False)
figs['s2b'] = store_fig('ds2b-', 'Lake, schema on read: json, csv and log files land in the lake as-is. When the reader queries, a parse-and-schema step reads the files and returns rows. The cost is paid on read.', 'SCHEMA ON READ', True)

# ---- 3 star schema --------------------------------------------------------------------
cust = [('1', 'Alice', 'Paris'), ('2', 'Bob', 'Rome'), ('3', 'Carol', 'Paris')]
prod = [('10', 'Pen', 'office'), ('11', 'Mug', 'kitchen')]
fact = [('1', 'Mon', '30', '10'), ('2', 'Mon', '40', '11'), ('3', 'Tue', '25', '10'), ('1', 'Tue', '15', '11')]
city = {c[0]: c[2] for c in cust}
agg = {}
for r in fact:
    agg[city[r[0]]] = agg.get(city[r[0]], 0) + int(r[2])
assert agg == {'Paris': 70, 'Rome': 40}
f = Fig('ds3-', 720, 330, 'A star schema: the fact table fact_orders in the middle holds keys and revenue, one row per order. dim_customer on the left and dim_product on the right describe the keys. Four order rows slide in. Then the query joins fact rows to dim_customer by cust_id, and the result revenue by city fills: Paris 70, Rome 40.',
        'ONE FACT TABLE, DIMENSIONS AROUND IT')
dc = Table(0, 30, [('name', 64), ('city', 60), ('cust_id', 60)], 'dim_customer')
ft = Table(240, 30, [('cust_id', 60), ('day', 50), ('revenue', 66), ('prod_id', 60)], 'fact_orders')
dp = Table(536, 30, [('prod_id', 60), ('name', 54), ('category', 70)], 'dim_product')
f(dc.head() + dp.head() + ft.head())
for i, r in enumerate(cust):
    f(dc.row(i, [r[1], r[2], r[0]]), show=.3)
for i, r in enumerate(prod):
    f(dp.row(i, list(r)), show=.3)
for i, r in enumerate(fact):
    f(ft.row(i, list(r)), show=1 + i * .5, move=(1 + i * .5, 0, -24, .45))
f(L(dc.x + dc.w, dc.ry(0) + 13, ft.x, ft.ry(0) + 13, RULE_HI, 1.2, '3 3') + L(ft.x + ft.w, ft.ry(0) + 13, dp.x, dp.ry(0) + 13, RULE_HI, 1.2, '3 3'), show=3.3)
f(T(ft.x + ft.w / 2, ft.bottom(4) + 18, 'keys + numbers only', MU), show=3.3)
q = Query(0, 196, ['SELECT c.city, SUM(f.revenue)', 'FROM fact_orders f', 'JOIN dim_customer c', '  ON f.cust_id = c.cust_id', 'GROUP BY c.city'], 260, 'query')
f(q.svg(), show=4)
rt = Table(470, 196, [('city', 90), ('revenue', 90)], 'revenue by city')
f(rt.head(), show=4)
t = 4.8
f(q.bar(3), show=t, hide=t + 3.6, d=.2)
for i, r in enumerate(fact):
    ci = int(r[0]) - 1
    f(ft.outline(i, i, 0, 0) + dc.outline(ci, ci, 1, 2), show=t + i * .8, hide=t + i * .8 + .7, d=.15)
t2 = t + 3.6
f(q.bar(4), show=t2, d=.2)
for i, c in enumerate(['Paris', 'Rome']):
    f(rt.row(i, [c, str(agg[c])], 'gr'), show=t2 + .4 + i * .5, move=(t2 + .4 + i * .5, -40, 0, .5))
figs['s3'] = f.render()

# ---- 4.1 layers -----------------------------------------------------------------------
raw = [(' alice ', '30.0'), ('BOB', '40'), (' alice ', '30.0'), ('carol', 'n/a')]
f = Fig('ds41-', 720, 236, 'Three layers. Raw keeps rows exactly as they came: padded names, text amounts, a duplicate row, n/a. Cleaned trims and types them, drops the duplicate and turns n/a into NULL. Mart aggregates for one team: 3 customers, revenue 70.',
        'RAW → CLEANED → MART')
ra = Table(0, 30, [('name', 90), ('amount', 80)], 'raw · as-is')
cl = Table(260, 30, [('name', 90), ('amount', 80)], 'cleaned · typed, deduped')
mt = Table(520, 30, [('customers', 90), ('revenue', 90)], 'mart · per team')
f(ra.head() + cl.head() + mt.head())
for i, r in enumerate(raw):
    f(ra.row(i, [r[0].replace(' ', ' '), r[1]]), show=.4 + i * .4, move=(.4 + i * .4, 0, -24, .4))
t = 2.4
f(arrow(178, 100, 252, 100, MU, 1.3) + T(215, 92, 'cast · trim', MU), show=t)
cleaned = [('Alice', '30'), ('Bob', '40'), ('Carol', 'NULL')]
src = [0, 1, 3]
for k, (r, s) in enumerate(zip(cleaned, src)):
    tk = t + .4 + k * .9
    f(ra.outline(s), show=tk, hide=tk + .8, d=.15)
    f(cl.row(k, list(r), colors={1: AM} if r[1] == 'NULL' else None), show=tk + .3, move=(tk + .3, -60, 0, .5))
    if k == 1:
        f(ra.outline(2, c=RD) + T(ra.x + ra.w / 2, ra.bottom(4) + 18, 'duplicate dropped', RD), show=tk + .8)
        f(ra.strike(2), show=tk + .8)
t = t + 3.6
f(arrow(438, 100, 512, 100, MU, 1.3) + T(475, 92, 'aggregate', MU), show=t)
f(cl.outline(0, 2, c=AM), show=t + .2, hide=t + 1.2, d=.2)
f(mt.row(0, ['3', '70'], 'gr'), show=t + .7, move=(t + .7, -60, 0, .5))
f(T(mt.x + mt.w / 2, mt.ry(1) + 17, 'teams read here', MU), show=t + 1.4)
f(T(cl.x + cl.w / 2, cl.ry(3) + 17, 'one shared truth', MU), show=t + 1.4)
figs['s4a'] = f.render()

# ---- 4.2 ETL / 4.3 ELT ---------------------------------------------------------------
f = Fig('ds42-', 640, 176, 'ETL: rows leave the source, are transformed in a separate engine, and only clean rows are loaded into the warehouse. The engine is extra infrastructure to run.', 'EXTRACT → TRANSFORM → LOAD')
xs = [40, 300, 560]
for k, (kind, lab) in enumerate([('db', 'source'), ('worker', 'transform engine'), ('db', 'warehouse')]):
    f(icon(kind, xs[k], Y, lab))
t = go(f, 68, E, 272, E, 'raw rows', .5, 'bl')
f(ring(300, Y), show=t, hide=t + 1.4, d=.2)
t = go(f, 328, E, 532, E, 'clean rows', t + 1, 'gr')
f(pill(560, 116, 'only clean data', 'gr'), show=t + .2)
f(R(220, 116, 160, 34, 'none', AM, 8, 1.4, '4 3') + T(300, 137, 'extra infra to run', AM, 'middle', bold=True), show=t + .8)
figs['s4b'] = f.render()

f = Fig('ds43-', 640, 196, 'ELT: raw rows are loaded straight into the warehouse. Inside the warehouse, SQL (usually dbt) turns raw tables into clean tables, using the warehouse own compute.', 'EXTRACT → LOAD → TRANSFORM IN PLACE')
f(frame(200, 24, 440, 128, 'inside the warehouse'))
xs = [40, 300, 540]
for k, (kind, lab) in enumerate([('db', 'source'), ('db', 'raw tables'), ('db', 'clean tables')]):
    f(icon(kind, xs[k], Y + 10, lab))
E2 = E + 10
t = go(f, 68, E2, 272, E2, 'raw rows', .5, 'bl')
f(ring(300, Y + 10), show=t, hide=t + 1, d=.2)
t = go(f, 328, E2, 512, E2, 'dbt SQL', t + .6, 'am')
f(ring(540, Y + 10, c=GR), show=t, d=.2)
f(R(380, 160, 260, 26, 'none', 'none') + T(630, 178, 'uses the warehouse compute, no extra engine', AM, 'end', bold=True), show=t + .6)
figs['s4c'] = f.render()

# ---- 4.4 idempotent rerun --------------------------------------------------------------
f = Fig('ds44-', 720, 228, 'Two pipelines load the same day, then crash and retry. Plain INSERT appends again on retry: 5 blocks become 10, revenue doubles. Delete the day first, then insert: the retry wipes the first copy and writes the same 5 blocks, still 10,000 rows.', 'RUN, CRASH, RETRY')
BW, G, X0 = 26, 4, 300
def blocks(y, n0, tone, k0=0):
    return ''.join(R(X0 + (k0 + i) * (BW + G), y, BW, 26, tint(tone, '.22'), COL[tone], 3, 1.2) for i in range(n0))
for row, (y, lines, good) in enumerate([(34, ['INSERT INTO orders', 'SELECT * FROM staging'], False),
                                        (138, ['DELETE FROM orders', ' WHERE day = \'10-05\';', 'INSERT INTO orders ...'], True)]):
    q = Query(0, y, lines, 260)
    f(q.svg())
    f(R(X0 - 6, y + 4, 10 * (BW + G) + 8, 36, 'var(--sunk)', RULE_HI, 6))
    f(T(X0 - 6, y + 56, 'run 1', MU, 'start'), show=.4 + row * .1)
    t0 = .5 + row * 5.2
    f(q.bar(len(lines) - 1), show=t0, hide=t0 + 1.2, d=.2)
    for i in range(5):
        f(blocks(y + 9, 1, 'bl', i), show=t0 + .2 + i * .15, move=(t0 + .2 + i * .15, 0, -20, .3))
    f(T(X0 + 160, y + 56, '✕ crash · retry', RD, 'start'), show=t0 + 1.5)
    t1 = t0 + 2.4
    if not good:
        f(q.bar(0), show=t1, hide=t1 + 1.4, d=.2)
        for i in range(5):
            f(blocks(y + 9, 1, 'rd', 5 + i), show=t1 + .2 + i * .15, move=(t1 + .2 + i * .15, 0, -20, .3))
        f(pill(X0 + 340, y + 12, '20,000 rows', 'rd'), show=t1 + 1.3)
    else:
        f(q.bar(0), show=t1, hide=t1 + 1, d=.2)
        f(R(X0 - 2, y + 7, 5 * (BW + G) + 2, 30, 'var(--sunk)', 'none', 3), show=t1 + .4, d=.4)
        f(q.bar(2), show=t1 + 1, d=.2)
        for i in range(5):
            f(blocks(y + 9, 1, 'gr', i), show=t1 + 1.2 + i * .15, move=(t1 + 1.2 + i * .15, 0, -20, .3))
        f(pill(X0 + 340, y + 12, '10,000 rows', 'gr'), show=t1 + 2.2)
figs['s4d'] = f.render()

# ---- 5.x time axis helpers -------------------------------------------------------------
AX0, AX1 = 40, 680
def axis(f, y, labels, n):
    s = L(AX0, y, AX1, y, RULE_HI, 1.4)
    for k, lab in labels:
        x = AX0 + (AX1 - AX0) * k / n
        s += L(x, y - 4, x, y + 4, RULE_HI, 1.2) + T(x, y + 18, lab, MU, mono=True)
    f(s)
def X(v, n): return AX0 + (AX1 - AX0) * v / n
def dot(x, y, tone='bl', r=6):
    return '<circle cx="%.1f" cy="%.1f" r="%d" fill="%s" stroke="%s" stroke-width="1.4"/>' % (x, y, r, tint(tone, '.3'), COL[tone])

# 5.1 batch: hours 8..32 (8:00 to 08:00 next day)
f = Fig('ds51-', 720, 196, 'Batch: orders arrive all day and pile up. At 02:00 a scheduled job reads the whole day at once; the report is ready at 07:00. Latency is hours.', 'BATCH · ONE JOB ON A SCHEDULE')
N = 24
axis(f, 120, [(0, '08:00'), (6, '14:00'), (12, '20:00'), (18, '02:00'), (23, '07:00')], N)
ev = [1, 2.5, 3.2, 5, 6.5, 8, 9.1, 10.4, 12, 13.5]
for i, v in enumerate(ev):
    f(dot(X(v, N), 104), show=.4 + i * .3, move=(.4 + i * .3, 0, -40, .35))
f(T(X(6, N), 82, 'orders pile up all day', MU), show=3.6)
t = 4.4
f(R(X(0, N) - 10, 92, X(14, N) - X(0, N) + 20, 24, 'none', AM, 6, 1.6), show=t)
f(icon('worker', X(18, N), 34, '02:00 job', 'am', side=False), show=t)
f(arrow(X(14, N) + 14, 104, X(18, N) - 26, 70, AM, 1.4), show=t + .3)
f(pill(X(23, N) - 10, 64, 'report 07:00', 'gr'), show=t + 1.4)
f(L(X(13.5, N), 160, X(23, N), 160, AM, 1.4) + T(X(18, N), 176, 'latency: hours', AM, 'middle', bold=True), show=t + 2)
figs['s5a'] = f.render()

# 5.2 stream
f = Fig('ds52-', 720, 196, 'Stream: each order is processed the moment it arrives, so the running total on the dashboard ticks up within seconds: 1, 2, 3, 4, 5. The job runs all the time.', 'STREAM · EACH EVENT AT ONCE')
N = 60
axis(f, 120, [(0, '12:00:00'), (20, ':20'), (40, ':40'), (60, '12:01:00')], N)
ev = [6, 17, 26, 41, 52]
f(icon('worker', 640, 26, 'always on', 'am', side=False))
for i, v in enumerate(ev):
    ti = .5 + i * 1.2
    f(dot(X(v, N), 104), show=ti, move=(ti, 0, -40, .35))
    f(arrow(X(v, N) + 6, 98, 610, 56, AM, 1), show=ti + .4, hide=ti + 1.1, d=.2)
    f(pill(525, 32, 'total = %d' % (i + 1), 'gr', 100), show=ti + .6, hide=None if i == 4 else ti + 1.25, d=.15)
f(T(640, 176, 'latency: seconds', AM, 'middle', bold=True), show=7)
figs['s5b'] = f.render()

# 5.3 windows + late event
f = Fig('ds53-', 720, 232, 'Tumbling windows of five minutes on event time. A cursor shows processing time moving forward. Events land in the window of their event time. Each window closes one minute after its end (the watermark) and its count is final: 3, 2, 2. An event that happened at 00:04 arrives at 00:08, after the first window closed, and is dropped without any error.',
        'TUMBLING WINDOWS · WATERMARK 1 MIN')
N = 15
WY = 70
axis(f, 150, [(0, '00:00'), (5, '00:05'), (10, '00:10'), (15, '00:15')], N)
f(T(AX1, 186, 'event time', MU, 'end'))
for w in range(3):
    f(R(X(5 * w, N) + 3, WY - 34, X(5, N) - X(0, N) - 6, 104, 'var(--bg)', RULE_HI, 8))
    f(T(X(5 * w + 2.5, N), WY - 18, 'window %d' % (w + 1), MU))
events = [(.5, .7), (1.8, 2.0), (3.2, 3.4), (5.5, 5.8), (7.0, 7.2), (4.2, 8.0), (11, 11.3), (13.5, 13.8)]
S = .55; T0 = .6
def tm(m): return T0 + m * S
# processing-time cursor, one segment per minute
for m in range(15):
    seg = L(X(m + 1, N), WY - 40, X(m + 1, N), 146, AM, 1.6, '4 3') + T(X(m + 1, N), WY - 44, 'now', AM)
    f(seg, show=tm(m), hide=None if m == 14 else tm(m + 1), move=(tm(m), X(m, N) - X(m + 1, N), 0, S), d=.03)
counts = [0, 0, 0]
closed = [False] * 3
for et, arr in events:
    w = int(et // 5)
    late = arr >= 5 * (w + 1) + 1
    ti = tm(arr)
    yy = WY + 40 + (counts[w] if not late else 0) * 0
    if late:
        f(dot(X(et, N), WY + 12, 'rd'), show=ti, move=(ti, X(arr, N) - X(et, N), -30, .5))
        f(L(X(et, N), WY + 20, X(et, N), 196, RD, 1, '3 3') + T(X(et, N) + 6, 214, 'happened 00:04, arrived 00:08: window 1 already closed · dropped, no error', RD, 'start'), show=ti + .5)
        continue
    counts[w] += 1
    f(dot(X(et, N), WY + 40), show=ti, move=(ti, 0, -30, .35))
    f(R(X(5 * w + 2.5, N) - 18, WY - 6, 36, 22, 'var(--bg)', 'none') + pill(X(5 * w + 2.5, N), WY - 6, str(counts[w]), 'bl', 32), show=ti + .3, hide=None, d=.15)
assert counts == [3, 2, 2]
for w in range(3):
    tc = tm(5 * (w + 1) + 1) if w < 2 else tm(15) + .2
    f(R(X(5 * w + 2.5, N) - 18, WY - 6, 36, 22, 'var(--bg)', 'none') + pill(X(5 * w + 2.5, N), WY - 6, str(counts[w]), 'gr', 32) +
      R(X(5 * w, N) + 3, WY - 34, X(5, N) - X(0, N) - 6, 104, 'none', GR, 8, 1.4), show=tc)
figs['s5c'] = f.render()

# ---- 6.1 quality dimensions ----------------------------------------------------------
rows = [('1', 'Alice', '30', 'USD', '10-05'), ('2', 'Bob', 'NULL', 'USD', '10-05'), ('3', 'Carol', '25', 'USD', '10-05'),
        ('3', 'Carol', '25', 'USD', '10-05'), ('4', 'Dan', '-5', 'USD', '10-05'), ('5', 'Eve', '20', 'usd', '10-05')]
f = Fig('ds61-', 720, 290, 'An orders table is checked one dimension at a time. Completeness finds a NULL amount. Uniqueness finds id 3 twice. Validity finds a negative amount. Consistency finds usd written two ways. Timeliness finds the newest row is from yesterday. Accuracy: Alice paid 300, not 30, and only a business rule can see it.',
        'SIX QUESTIONS, ONE QUERY EACH')
tb = Table(0, 30, [('id', 36), ('customer', 70), ('amount', 64), ('cur', 50), ('day', 60)], 'orders · today 10-06')
f(tb.head())
for i, r in enumerate(rows):
    f(tb.row(i, list(r)), show=.2)
checks = [('completeness', 'amount IS NULL', [(1, 1, 2, 2)], 'rd'),
          ('uniqueness', 'COUNT(DISTINCT id)', [(2, 3, 0, 0)], 'rd'),
          ('validity', 'amount >= 0', [(4, 4, 2, 2)], 'rd'),
          ('consistency', 'one spelling per value', [(5, 5, 3, 3)], 'rd'),
          ('timeliness', 'MAX(day) = today', [(0, 5, 4, 4)], 'rd'),
          ('accuracy', 'business rule only', [(0, 0, 2, 2)], 'am')]
CX = 330
t = 1
for k, (name, rule, outs, tone) in enumerate(checks):
    y = tb.ry(k)
    f(T(CX, y + 17, name, TX, 'start', bold=True) + T(CX + 100, y + 17, rule, MU, 'start', mono=True), show=t)
    o = ''.join(tb.outline(a, b, c, d, AM) for a, b, c, d in outs)
    f(o, show=t + .2, hide=t + 1.3, d=.15)
    lab = 'fail' if tone == 'rd' else 'paid 300?'
    f(pill(680, y + 3, lab, tone, 66), show=t + .7)
    t += 1.6
f(T(CX, tb.bottom(6) + 26, 'first five check form · only accuracy checks meaning', AM, 'start', bold=True), show=t)
figs['s6a'] = f.render()

# ---- 6.2 where to check --------------------------------------------------------------
f = Fig('ds62-', 720, 214, 'Three checkpoints. At the source database, constraints block a row with age -3. In the pipeline, tests on the staging table catch a duplicate batch from a partner feed. At the dashboard, a sanity check catches revenue ten times too high caused by a wrong join, although every table was valid.',
        'CHEAPEST CLOSEST TO THE SOURCE')
xs = [40, 200, 360, 520, 680]
for k, (kind, lab) in enumerate([('server', 'app'), ('db', 'source db'), ('worker', 'staging tests'), ('db', 'warehouse'), ('client', 'dashboard')]):
    f(icon(kind, xs[k], Y, lab))
for n, x in [(1, 200), (2, 360), (3, 680)]:
    f(badge(x + 26, Y + 2, n))
t = go(f, 68, E, 172, E, 'age=-3', .5, 'rd')
f(T(200, Y + 112, '✕ NOT NULL · CHECK', RD), show=t)
t = go(f, 228, E, 332, E, 'dup', t + .8, 'rd')
f(T(360, Y + 112, '✕ duplicate batch', RD), show=t)
t = go(f, 388, E, 492, E, 'rows', t + .8, 'bl')
t = go(f, 548, E, 652, E, '×10', t + .4, 'rd')
f(T(680, Y + 112, '✕ revenue ×10', RD, 'end'), show=t)
f(T(0, 196, 'each checkpoint catches what the next one cannot', AM, 'start', bold=True), show=t + .6)
figs['s6b'] = f.render()

# ---- palette remap: data→brand, highlight→violet, result→filled, error→rose ---------------
MAP = [('var(--filled)', '@B@'), ('--blue-a', '@b@'), ('var(--probe)', 'var(--violet)'), ('--amber-a', '--violet-a'),
       ('var(--ok)', 'var(--filled)'), ('--green-a', '--blue-a'), ('var(--tomb)', 'var(--rose)'), ('--red-a', '--rose-a'),
       ('@B@', 'var(--brand)'), ('@b@', '--clay-a')]
for k in figs:
    for a, b in MAP:
        figs[k] = figs[k].replace(a, b)
json.dump(figs, open('/tmp/nosql/figs.json', 'w'))
print(len(figs))
