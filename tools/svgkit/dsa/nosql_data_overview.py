# -*- coding: utf-8 -*-
"""Figures for content/06-nosql-data/01-overview/nosql-data-overview (shelf overview).
Run: python3 nosql_data_overview.py  -> splices the three figures into the page."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from hldfig import *  # noqa

PAGE = os.path.join(HERE, '../../../content/06-nosql-data/01-overview/nosql-data-overview/index.html')

def palette(s):
    """Analogous blue-violet palette (same swap as the Python and CS shelves)."""
    for a, b in [('--filled)', '@B)'), ('--blue-a)', '@BA)'), ('--ok)', '--filled)'), ('--green-a)', '--blue-a)'),
                 ('--tomb)', '--rose)'), ('--red-a)', '--rose-a)'), ('--probe)', '--violet)'), ('--amber-a)', '--violet-a)'),
                 ('@B)', '--brand)'), ('@BA)', '--clay-a)')]:
        s = s.replace(a, b)
    return s

def box(x, y, w, h, title, sub, tone=None):
    fill = tint(tone, '.14') if tone else 'var(--bg)'
    c = COL[tone] if tone else RULE_HI
    tc = COL[tone] if tone else TX
    return (R(x, y, w, h, fill, c, 6, 1.4) + T(x + w / 2, y + h / 2 - (2 if sub else -4), title, tc, 'middle', 'sv-s') +
            (T(x + w / 2, y + h / 2 + 14, sub, MU, 'middle', 'sv-l') if sub else ''))

# ---------- 1. Mental model: one data journey ----------
def fig1():
    f = Fig('nqa-', 720, 330, 'A user writes to the app; rows land in the OLTP database or a NoSQL store; '
            'a pipeline copies them into a warehouse that feeds a dashboard', 'ONE DATA JOURNEY')
    Y1, Y2 = 60, 210
    f(frame(110, 36, 260, 118, 'SQL SHELF'))
    f(frame(110, 186, 260, 118, 'NOSQL'), show=4.2)
    f(frame(400, 36, 320, 118, 'DATA SYSTEMS'), show=6.4)
    f(icon('user', 40, Y1, 'user'))
    f(icon('server', 170, Y1, 'app'))
    f(icon('db', 310, Y1, 'OLTP db', sub='few rows, exact'))
    t = send(f, 68, Y1 + 24, 140, Y1 + 24, 'order', .6)
    f(ring(170, Y1), show=t, hide=t + 1.2)
    t = send(f, 198, Y1 + 24, 280, Y1 + 24, 'INSERT', t + .3)
    f(icon('db', 310, Y1, 'OLTP db', 'bl', sub='few rows, exact', wipe=True), show=t)
    # NoSQL branch
    f(icon('db', 220, Y2, 'document store', 'am', sub='any shape, by key'), show=4.4)
    t = send(f, 175, Y1 + 80, 210, Y2 - 4, '{ json }', 4.8, 'am')
    f(note(300, 240, 'shape varies:', AM), show=t)
    f(note(300, 256, 'leave the table', AM), show=t)
    # pipeline
    f(icon('worker', 450, Y1, 'pipeline', sub='ETL'), show=6.6)
    f(icon('db', 560, Y1, 'warehouse', sub='all history'), show=6.6)
    f(icon('client', 670, Y1, 'dashboard'), show=6.6)
    t = send(f, 338, Y1 + 24, 422, Y1 + 24, 'rows', 7.0)
    f(ring(450, Y1), show=t, hide=t + 1.2)
    t = send(f, 478, Y1 + 24, 532, Y1 + 24, 'batch', t + .3, 'bl', w=48)
    f(icon('db', 560, Y1, 'warehouse', 'gr', sub='all history', wipe=True), show=t)
    t = send(f, 588, Y1 + 24, 644, Y1 + 24, 'sum', t + .3, 'gr', w=40)
    f(icon('client', 670, Y1, 'dashboard', 'gr', wipe=True), show=t)
    f(note(420, 230, 'one question scans everything —', GR), show=t + .2)
    f(note(420, 248, 'so it runs on a separate system', GR), show=t + .2)
    return f.render()

# ---------- 2. Which lesson for which problem ----------
# Each symptom plays out as a small incident with HLD icons, then a packet carries it to the lesson.
def lesson(x, y, title, sub, lit=False):
    tone = 'gr' if lit else None
    return box(x, y, 190, 48, title, sub, tone)

def fig2():
    f = Fig('nqb-', 740, 400, 'Three incidents. A record with a new shape does not fit the table: NoSQL landscape. '
            'A big report blocks a user order on the app database: OLTP vs OLAP. '
            'A rerun loads the same rows twice and the dashboard total doubles: Data systems.',
            'THREE INCIDENTS · EACH POINTS TO ONE LESSON')
    LX = 530
    rows = [60, 175, 320]
    for y in rows:
        f(lesson(LX, y - 2, '', ''))
    # 1. shape does not fit
    y = rows[0]
    f(icon('server', 40, y - 14, 'app'), show=.3)
    f(icon('db', 250, y - 14, 'table'), show=.3)
    t = send(f, 68, y + 10, 222, y + 10, '{ +tags[] }', .7, 'bl', w=78)
    f(icon('db', 250, y - 14, 'table', 'rd', wipe=True), show=t)
    xmark(300, y + 4, t, f, 'no column for it')
    t2 = send(f, 420, y + 22, LX - 4, y + 22, 'fix', t + .6, 'am', w=34)
    f(lesson(LX, y - 2, 'NoSQL landscape', 'store it as a document', True), show=t2)
    # 2. report blocks the app
    y = rows[1]; t0 = t2 + .6
    f(icon('user', 40, y - 14, 'user'), show=t0)
    f(icon('db', 250, y - 14, 'app db'), show=t0)
    f(icon('client', 120, y + 56, 'report'), show=t0)
    t = send(f, 152, y + 80, 212, y + 36, 'SUM all', t0 + .4, 'rd', w=58)
    f(icon('db', 250, y - 14, 'app db', 'rd', sub='busy', wipe=True), show=t)
    f(arrow(152, y + 80, 212, y + 36, RD, 1.5), show=t, d=.2)
    t = send(f, 68, y + 10, 222, y + 10, 'order', t + .3, 'bl', w=48)
    xmark(300, y + 4, t, f, 'order times out')
    t2 = send(f, 420, y + 22, LX - 4, y + 22, 'fix', t + .6, 'am', w=34)
    f(lesson(LX, y - 2, 'OLTP vs OLAP', 'move reports to a warehouse', True), show=t2)
    # 3. rerun doubles the total
    y = rows[2]; t0 = t2 + .6
    f(icon('worker', 40, y - 14, 'pipeline'), show=t0)
    f(icon('client', 250, y - 14, 'dashboard'), show=t0)
    t = send(f, 68, y + 10, 222, y + 10, '100 rows', t0 + .4, 'bl', w=62)
    f(note(300, y + 8, 'total 100', MU), show=t, hide=t + 1.2)
    t = send(f, 68, y + 10, 222, y + 10, 'rerun: 100', t + .6, 'bl', w=72)
    f(icon('client', 250, y - 14, 'dashboard', 'rd', wipe=True), show=t)
    xmark(300, y + 4, t, f, 'total 200 — counted twice')
    t2 = send(f, 420, y + 22, LX - 4, y + 22, 'fix', t + .6, 'am', w=34)
    f(lesson(LX, y - 2, 'Data systems', 'safe reruns · quality checks', True), show=t2)
    return f.render()

# ---------- 3. Learning order ----------
# A track with three stations; a traveller stops at each and picks up one idea.
def fig3():
    f = Fig('nqc-', 720, 230, 'A track from the SQL shelf through NoSQL landscape and OLTP vs OLAP, in either order, '
            'to Data systems. At each stop one idea is collected: data shape, workload type, pipelines.',
            'LEARNING ORDER · ONE IDEA PER STOP')
    ST = [(70, 'SQL shelf', 'tables · keys'), (230, 'NoSQL landscape', 'data shape'),
          (420, 'OLTP vs OLAP', 'workload type'), (630, 'Data systems', 'pipelines')]
    Y = 90
    f(L(70, Y, 630, Y, RULE_HI, 3))
    for x, name, _ in ST:
        f('<circle cx="%.1f" cy="%.1f" r="9" fill="var(--bg)" stroke="var(--rule-hi)" stroke-width="2"/>' % (x, Y))
        f(T(x, Y - 22, name, TX, 'middle', 'sv-s'))
    f(T(325, Y + 30, 'either order', MU, 'middle', 'sv-l'))
    f(R(230, Y + 18, 190, 1, 'none', RULE_HI, 0, 1, '3 3'))
    # traveller rides the track
    t = .6
    for k, (x, name, idea) in enumerate(ST):
        if k:
            px = ST[k - 1][0]
            f(L(px, Y, x, Y, BL, 3), show=t, d=.6)
            t += .7
        f('<circle cx="%.1f" cy="%.1f" r="9" fill="%s" stroke="%s" stroke-width="2"/>' % (x, Y, BL, BL), show=t)
        f(pill(x, Y + 46, idea, 'gr' if k else 'bl', 18 + len(idea) * 6.4), show=t + .2, move=(t + .2, 0, -30, .5))
        t += .9
    # the bag: ideas line up at the bottom
    f(note(20, 206, 'by the end: shape → workload → pipeline — every later data lesson builds on these three', GR), show=t + .2)
    return f.render()

if __name__ == '__main__':
    s = open(PAGE).read()
    figs = [fig1(), fig2(), fig3()]
    for i, svg in enumerate(figs, 1):
        svg = palette(svg)
        s = re.sub(r'<!--FIG%d-->.*?<!--/FIG%d-->' % (i, i), lambda m: '<!--FIG%d-->\n%s\n<!--/FIG%d-->' % (i, svg, i), s, flags=re.S)
    open(PAGE, 'w').write(s)
