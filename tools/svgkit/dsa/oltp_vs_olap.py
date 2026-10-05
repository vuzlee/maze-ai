# -*- coding: utf-8 -*-
"""Figures for content/06-nosql-data/02-nosql/oltp-vs-olap.
Run: python3 oltp_vs_olap.py  -> splices figures into <!--FIGn--> markers of the page."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from hldfig import *  # noqa
from nosql_data_overview import palette

PAGE = os.path.join(HERE, '../../../content/06-nosql-data/02-nosql/oltp-vs-olap/index.html')
OFF = 'var(--sunk)'

def c(x, y, v, w=40, tone=None, h=28, off=False):
    if off:
        return R(x, y, w, h, OFF, RULE_HI, 3, 1) + T(x + w / 2, y + h / 2 + 4, v, FA)
    fill = tint(tone, '.18') if tone else 'var(--bg)'
    s = R(x, y, w, h, 'var(--bg)', 'none', 3) if tone else ''
    return s + R(x, y, w, h, fill, COL[tone] if tone else RULE_HI, 3, 1.2 if tone else 1) + \
        T(x + w / 2, y + h / 2 + 4, v, COL[tone] if tone else TX)

ROWS = [('1', 'Alice', '500', 'Paris'), ('2', 'Bob', '200', 'Rome'), ('3', 'Alice', '300', 'Paris')]
assert sum(int(r[2]) for r in ROWS) == 1000

# ---------- 1. Mental model ----------
def fig1():
    f = Fig('ov1-', 720, 300, 'Left, OLTP: five small UPDATE statements arrive one after another, each changes a single '
            'stock value in milliseconds. Right, OLAP: one query scans every row of the orders table and '
            'returns a total per month.', 'MANY SMALL WRITES · FEW HUGE SCANS')
    f(T(0, 44, 'OLTP · app database', MU, 'start', 'sv-s'))
    t1 = Table(0, 56, [('id', 50), ('item', 90), ('stock', 70)])
    f(t1.head())
    stock = [5, 3, 8, 2, 6, 4]
    items = ['pen', 'cup', 'bag', 'hat', 'mug', 'box']
    for i in range(6):
        f(t1.row(i, [str(i + 1), items[i], str(stock[i])]))
    ups = [2, 0, 4, 1, 3]
    for k, i in enumerate(ups):
        t = .6 + k * .8
        stock[i] -= 1
        y = t1.ry(i)
        f(pill(t1.cx(2) + 60 + 40, y + 3, 'UPDATE #%d' % (i + 1), 'am', 84), show=t, hide=t + .9,
          move=(t, 0, -y + 40, .5), d=.15)
        f(t1.cell(i, 2, str(stock[i]), 'am'), show=t + .5, hide=t + 1.0, d=.15)
        f(t1.cell(i, 2, str(stock[i])), show=t + 1.0, d=.15)
    yb = t1.bottom(6)
    f(T(0, yb + 24, '5 statements · 1 row each · ~1 ms', BL, 'start'), show=4.6)

    X = 400
    f(T(X, 44, 'OLAP · warehouse', MU, 'start', 'sv-s'), show=5.0)
    t2 = Table(X, 56, [('month', 60), ('revenue', 70)])
    data = [('Jan', 300), ('Jan', 400), ('Feb', 250), ('Jan', 200), ('Feb', 450), ('Feb', 100)]
    f(t2.head(), show=5.0)
    for i, (m, v) in enumerate(data):
        f(t2.row(i, [m, str(v)]), show=5.0)
    # scan band slides down over every row
    for i in range(6):
        f(R(X - 3, t2.ry(i) - 3, 136, t2.rh + 6, 'none', AM, 4, 1.8), show=5.7 + i * .5, hide=6.2 + i * .5, d=.12)
        f(t2.cell(i, 1, str(data[i][1]), 'bl'), show=5.8 + i * .5, d=.2)
    tot = {'Jan': 900, 'Feb': 800}
    assert tot['Jan'] == 300 + 400 + 200 and tot['Feb'] == 250 + 450 + 100
    t3 = Table(X + 180, 56, [('month', 60), ('SUM', 70)])
    f(t3.head(), show=8.8)
    for i, m in enumerate(['Jan', 'Feb']):
        f(t3.row(i, [m, str(tot[m])], 'gr'), show=9.0 + i * .3, move=(9.0 + i * .3, -40, 0, .5))
    f(arrow(X + 140, t2.ry(1), X + 172, t2.ry(1), FA, 1.2), show=8.8)
    f(T(X, yb + 24, '1 query · every row · seconds', GR, 'start'), show=9.6)
    return f.render()

# ---------- 2.x storage layouts ----------
CW, G = 46, 3
def layout(pre, kind):
    col = kind == 'col'
    f = Fig(pre, 720, 300 if True else 0,
            ('Column-oriented: the table is stored column by column, so all ids sit together, then all customers, '
             'all revenues, all cities. SELECT SUM(revenue) reads only the three revenue blocks and skips the rest: '
             'read 3 values, used 3.') if col else
            ('Row-oriented: the table is stored row by row, each row one contiguous block of id, customer, revenue, '
             'city. SELECT SUM(revenue) must read every block whole: read 12 values, used 3.'),
            'COLUMN-ORIENTED · EACH COLUMN IS ONE BLOCK ON DISK' if col else 'ROW-ORIENTED · EACH ROW IS ONE BLOCK ON DISK')
    t = Table(0, 30, [('id', 40), ('cust', 60), ('revenue', 66), ('city', 60)])
    f(t.head())
    for i, r in enumerate(ROWS):
        f(t.row(i, list(r)))
    q = Query(280, 36, ['SELECT SUM(revenue)', 'FROM orders'], w=190)
    f(q.svg())
    DY = 190
    f(T(0, DY + 19, 'on disk', MU, 'start', 'sv-s'))
    # order of cells on disk
    order = [(i, j) for j in range(4) for i in range(3)] if col else [(i, j) for i in range(3) for j in range(4)]
    pos = {}
    x = 70
    for k, (i, j) in enumerate(order):
        if k and k % (3 if col else 4) == 0:
            x += 14
        pos[(i, j)] = x
        x += CW + G
    assert x < 720
    # group labels
    for g in range(4 if col else 3):
        cells = order[g * (3 if col else 4):(g + 1) * (3 if col else 4)]
        x0 = pos[cells[0]]; x1 = pos[cells[-1]] + CW
        lab = ['id', 'cust', 'revenue', 'city'][g] if col else 'row %d' % (g + 1)
        f(L(x0, DY - 4, x1, DY - 4, RULE_HI, 1) + T((x0 + x1) / 2, DY - 8, lab, MU), show=.3 + g * .5)
    # cells slide from the table down to disk, one block (row or column) at a time
    for k, (i, j) in enumerate(order):
        g = k // (3 if col else 4)
        tt = .3 + g * .5
        sx, sy = t.colx(j) + (t.cols[j][1] - CW) / 2, t.ry(i)
        f(c(pos[(i, j)], DY, ROWS[i][j], CW), show=tt, move=(tt, sx - pos[(i, j)], sy - DY, .6), d=.15)
    T0 = 2.8
    f(q.bar(0), show=T0)
    # read head sweeps blocks in disk order
    used = 0; read = 0
    for g in range(4 if col else 3):
        cells = order[g * (3 if col else 4):(g + 1) * (3 if col else 4)]
        x0 = pos[cells[0]]; x1 = pos[cells[-1]] + CW
        if col and g != 2:
            tt = T0 + .4 + g * .25
            for (i, j) in cells:
                f(c(pos[(i, j)], DY, ROWS[i][j], CW, off=True), show=tt + .5)
            continue
        tt = T0 + .4 + (g * .25 if col else g * .9)
        f(R(x0 - 4, DY - 4, x1 - x0 + 8, 36, 'none', AM, 5, 1.8), show=tt, hide=tt + .8, d=.15)
        for (i, j) in cells:
            read += 1
            if j == 2:
                used += 1
                f(c(pos[(i, j)], DY, ROWS[i][j], CW, 'gr'), show=tt + .2)
            else:
                f(c(pos[(i, j)], DY, ROWS[i][j], CW, 'rd'), show=tt + .2)
    te = T0 + (1.6 if col else 3.4)
    assert (read, used) == ((3, 3) if col else (12, 3))
    f(pill(535, 50, 'SUM = 1000', 'gr', 100), show=te, move=(te, 0, DY - 50, .6))
    f(T(0, DY + 62, 'read %d values · used %d' % (read, used), GR if col else RD, 'start', 'sv-s'), show=te)
    if col:
        f(T(0, DY + 80, 'other columns never leave the disk', MU, 'start'), show=te + .3)
    else:
        f(T(0, DY + 80, 'id, cust, city were read for nothing', MU, 'start'), show=te + .3)
    return f.render()

# ---------- 3. schema shape ----------
def fig3():
    f = Fig('sc3-', 720, 312, 'Normalized OLTP schema: orders hold a customer id and an amount, customers hold the name, '
            'cities hold the city. For each order the matching customer row is found and its name and city are '
            'copied into one wide fact row, so analytics reads one table with no JOIN.',
            'NORMALIZED FOR WRITES · ONE WIDE TABLE FOR READS')
    o = Table(0, 30, [('id', 36), ('cust_id', 60), ('amt', 50)], title='orders')
    cu = Table(0, 170, [('id', 36), ('name', 66), ('city', 64)], title='customers')
    w = Table(400, 30, [('id', 36), ('name', 66), ('city', 64), ('amt', 50)], title='sales (wide)')
    ords = [('1', '10', '500'), ('2', '11', '200'), ('3', '10', '300')]
    cust = {'10': ('Alice', 'Paris'), '11': ('Bob', 'Rome')}
    f(o.head()); f(cu.head())
    for i, r in enumerate(ords):
        f(o.row(i, list(r)))
    for i, (k, v) in enumerate(cust.items()):
        f(cu.row(i, [k, v[0], v[1]]))
    f(T(250, 120, 'each fact once', BL, 'middle'))
    f(w.head(), show=.6)
    ck = list(cust)
    for i, r in enumerate(ords):
        t = 1.0 + i * 1.8
        ci = ck.index(r[1])
        f(o.outline(i, c=AM), show=t, hide=t + 1.5, d=.15)
        f(cu.outline(ci, c=AM), show=t + .3, hide=t + 1.5, d=.15)
        f(L(o.colx(1) + 30, o.ry(i) + o.rh, cu.colx(0) + 18, cu.ry(ci), AM, 1.2, '3 3'), show=t + .3, hide=t + 1.5, d=.15)
        ty = w.ry(i)
        f(w.row(i, ['', '', '', ''], ), show=t + .5, d=.2)
        def mv(v, j, sx, sy, tt):
            f(T(w.cx(j), ty + 17, v, TX), show=tt, move=(tt, sx - w.cx(j), sy - ty, .7), d=.1)
        mv(r[0], 0, o.cx(0), o.ry(i), t + .6)
        mv(cust[r[1]][0], 1, cu.cx(1), cu.ry(ci), t + .8)
        mv(cust[r[1]][1], 2, cu.cx(2), cu.ry(ci), t + .9)
        mv(r[2], 3, o.cx(2), o.ry(i), t + 1.0)
    te = 1.0 + 3 * 1.8
    f(w.outline(0, 2, 1, 2, GR), show=te)
    f(leader(w.cx(1) + 33, w.bottom(3) + 4, w.cx(1) + 33, w.bottom(3) + 30, 'Alice · Paris copied twice — no JOIN at query time', GR, 'middle'), show=te)
    return f.render()

# ---------- 4. why split ----------
def fig4():
    f = Fig('sp4-', 720, 290, 'Users send orders to the app, which writes to the app database. A report runs a 50 million '
            'row scan on the same database: the database is overloaded and a user order times out. The fix: an ETL job '
            'copies data from the app database into a warehouse, and the dashboard queries the warehouse instead, '
            'so orders are fast again.', 'REPORTS ON THE APP DB · THEN SPLIT WITH ETL')
    Y = 50
    f(icon('user', 40, Y, 'users'))
    f(icon('server', 170, Y, 'app'))
    f(icon('db', 300, Y, 'app DB', sub='OLTP'))
    f(icon('client', 450, 200, 'dashboard'))
    t = send(f, 68, Y + 24, 142, Y + 24, 'order', .4)
    t = send(f, 198, Y + 24, 272, Y + 24, 'INSERT', t + .1)
    f(icon('db', 300, Y, 'app DB', 'gr', sub='OLTP', wipe=True), show=t, hide=t + .6)
    t += .8
    # report hits the same DB
    tr = t
    f(arrow(420, 220, 322, Y + 70, RD, 1.5), show=tr, hide=tr + 3.0, d=.25)
    t = packet(f, 400, 200, 345, Y + 100, 'SUM 50M rows', tr, 'rd', w=110)
    f(icon('db', 300, Y, 'app DB', 'rd', sub='overloaded', wipe=True), show=t, hide=t + 2.6)
    t2 = send(f, 68, Y + 24, 142, Y + 24, 'order', t + .2)
    f(T(105, Y + 46, '✕ timeout', RD, 'middle'), show=t2 + .9, hide=t + 2.6)
    f(icon('server', 170, Y, 'app', 'rd', wipe=True), show=t2 + .9, hide=t + 2.6)
    t = t + 2.8
    # split: ETL to warehouse
    f(icon('worker', 450, Y, 'ETL', sub='nightly'), show=t)
    f(icon('db', 600, Y, 'warehouse', sub='OLAP'), show=t)
    t = send(f, 328, Y + 24, 422, Y + 24, 'copy', t + .3, 'bl')
    t = send(f, 478, Y + 24, 572, Y + 24, 'load', t + .1, 'bl')
    f(icon('db', 600, Y, 'warehouse', 'bl', sub='OLAP', wipe=True), show=t)
    t = send(f, 480, 220, 578, Y + 70, 'SUM 50M rows', t + .3, 'gr', w=110)
    f(icon('db', 600, Y, 'warehouse', 'gr', sub='OLAP', wipe=True), show=t)
    t = send(f, 68, Y + 24, 142, Y + 24, 'order', t + .1)
    t = send(f, 198, Y + 24, 272, Y + 24, 'INSERT', t + .1)
    f(icon('db', 300, Y, 'app DB', 'gr', sub='fast again', wipe=True), show=t)
    return f.render()

if __name__ == '__main__':
    s = open(PAGE).read()
    figs = [fig1(), layout('ro2-', 'row'), layout('co2-', 'col'), fig3(), fig4()]
    for i, svg in enumerate(figs, 1):
        svg = palette(svg)
        s, n = re.subn(r'<!--FIG%d-->.*?<!--/FIG%d-->' % (i, i), lambda m: '<!--FIG%d-->\n%s\n<!--/FIG%d-->' % (i, svg, i), s, flags=re.S)
        assert n == 1, i
    open(PAGE, 'w').write(s)
