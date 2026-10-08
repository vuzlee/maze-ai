# -*- coding: utf-8 -*-
"""Distributed systems shelf overview: an architecture growing with load + what becomes hard.

    python3 tools/svgkit/04-distributed/distributed_overview.py   # rewrites sections 01-02 in place
Re-runnable: everything from section 01 up to the Learning order section is regenerated.
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from overview import Fig, text, ln

PAGE = 'content/04-distributed/01-overview/distributed-overview/index.html'
L = {'cache': '../../03-scaling/caching/index.html', 'lb': '../../03-scaling/load-balancing/index.html',
     'shard': '../../03-scaling/sharding-replication/index.html',
     'mq': '../../04-messaging/messaging-queue-pubsub/index.html',
     'cap': '../../02-fundamentals/cap-theorem-consistency/index.html'}
B, V, R, F = 'var(--brand)', 'var(--violet)', 'var(--rose)', 'var(--filled)'
TINT, VT, RT = 'rgba(var(--clay-a),.10)', 'rgba(var(--violet-a),.14)', 'rgba(var(--rose-a),.10)'

# ---- small HLD icons, centred at (cx, cy), about 26 x 24 (same shapes as hldfig.py) ----
def ic(kind, cx, cy, hl=False, bad=False):
    s = R if bad else (V if hl else B)
    f = RT if bad else (VT if hl else TINT)
    w = 'stroke-width="1.3"'
    if kind == 'user':
        return (f'<circle cx="{cx}" cy="{cy-5}" r="5" fill="{f}" stroke="{s}" {w}/>'
                f'<path d="M{cx-9},{cy+11} Q{cx-9},{cy+2} {cx},{cy+2} Q{cx+9},{cy+2} {cx+9},{cy+11}Z" fill="{f}" stroke="{s}" {w}/>')
    if kind == 'server':
        o = f'<rect x="{cx-12}" y="{cy-11}" width="24" height="22" rx="3" fill="{f}" stroke="{s}" {w}/>'
        o += ln(cx - 12, cy - 3.7, cx + 12, cy - 3.7, s, 1.1) + ln(cx - 12, cy + 3.7, cx + 12, cy + 3.7, s, 1.1)
        o += ''.join(f'<circle cx="{cx+7}" cy="{cy-7.4+i*7.4:.1f}" r="1.2" fill="{s}"/>' for i in range(3))
        return o
    if kind == 'db':
        return (f'<path d="M{cx-12},{cy-7} V{cy+7} A12 4 0 0 0 {cx+12},{cy+7} V{cy-7}" fill="{f}" stroke="{s}" {w}/>'
                f'<ellipse cx="{cx}" cy="{cy-7}" rx="12" ry="4" fill="{f}" stroke="{s}" {w}/>'
                f'<path d="M{cx-12},{cy} A12 4 0 0 0 {cx+12},{cy}" fill="none" stroke="{s}" {w}/>')
    if kind == 'cache':
        return (f'<rect x="{cx-12}" y="{cy-11}" width="24" height="22" rx="6" fill="{f}" stroke="{s}" {w}/>'
                f'<path d="M{cx+2},{cy-7} L{cx-5},{cy+2} H{cx} L{cx-2},{cy+8} L{cx+6},{cy-2} H{cx+1}Z" fill="{s}"/>')
    if kind == 'lb':
        return (f'<circle cx="{cx}" cy="{cy}" r="11" fill="{f}" stroke="{s}" {w}/>'
                f'<path d="M{cx-7},{cy} H{cx-1} M{cx-1},{cy} L{cx+6},{cy-5} M{cx-1},{cy} H{cx+7} M{cx-1},{cy} L{cx+6},{cy+5}" '
                f'stroke="{s}" stroke-width="1.4" fill="none" stroke-linecap="round"/>')
    if kind == 'queue':
        o = f'<rect x="{cx-22}" y="{cy-9}" width="44" height="18" rx="9" fill="{f}" stroke="{s}" {w}/>'
        return o + ''.join(f'<rect x="{cx-15+i*11}" y="{cy-5}" width="8" height="10" rx="1.5" fill="var(--bg)" stroke="{s}" stroke-width="1"/>' for i in range(3))
    raise ValueError(kind)

def wire(a, b, hl=False):
    return ln(a[0], a[1], b[0], b[1], V if hl else 'var(--muted)', 1.3 if hl else 1)

# ---- figure 1: six frames ---------------------------------------------------------
FW, FH, GX, GY = 220, 206, 10, 12

def frame(n):
    """Diagram for stage n inside a 220-wide frame; returns svg relative to (0, 0)."""
    o = []
    cx = 110
    yU, yL, yS, yD = 62, 98, 134, 172
    o.append(ic('user', cx, yU))
    lb = n >= 2
    servers = [cx] if n < 2 else [cx - 40, cx, cx + 40]
    if lb:
        o.append(wire((cx, yU + 12), (cx, yL - 11)))
        o += [wire((cx, yL + 11), (sx, yS - 11), n == 2) for sx in servers]
        o.append(ic('lb', cx, yL, n == 2))
    else:
        o.append(wire((cx, yU + 12), (cx, yS - 11)))
    # data layer
    if n < 3:
        dbs = [cx]
    elif n == 3:
        dbs = [cx - 34, cx, cx + 34]       # primary + replicas
    else:
        dbs = [cx - 40, cx, cx + 40]       # shards
    for sx in servers:
        for dx in dbs:
            if n < 3 or (n == 3 and dx == cx) or n >= 4:
                if n >= 4 and abs(sx - dx) > 0.1 and len(servers) > 1:
                    continue
                o.append(wire((sx, yS + 11), (dx, yD - 11)))
    if n == 3:
        o.append(f'<path d="M{cx+12},{yD} H{cx+22} M{cx-12},{yD} H{cx-22}" stroke="{V}" stroke-width="1.2" stroke-dasharray="2 2"/>')
    for i, dx in enumerate(dbs):
        hl = (n == 3 and dx != cx) or n == 4
        o.append(ic('db', dx, yD, hl))
        if n >= 4:
            o.append(text(dx, yD + 22, 'A–H I–P Q–Z'.split()[i], 'sv-d', V if n == 4 else 'var(--muted)', 'middle', ';font-size:8.5px;font-family:var(--mono)'))
        elif n == 3:
            o.append(text(dx, yD + 22, 'copy' if dx != cx else 'primary', 'sv-d', V if dx != cx else 'var(--muted)', 'middle', ';font-size:8.5px'))
    for sx in servers:
        o.append(ic('server', sx, yS))
    if n >= 1:   # cache beside the server tier
        cxx = 30 if n >= 2 else 160
        o.append(f'<line x1="{cxx+12 if n<2 else cxx+12}" y1="{yS}" x2="{(servers[0]-12) if n>=2 else cx+12}" y2="{yS}" '
                 f'stroke="{V if n==1 else "var(--muted)"}" stroke-width="1" stroke-dasharray="2 2"/>' if n >= 2 else
                 f'<line x1="{cx+12}" y1="{yS}" x2="{cxx-12}" y2="{yS}" stroke="{V}" stroke-width="1.2" stroke-dasharray="2 2"/>')
        o.append(ic('cache', cxx, yS, n == 1))
    if n >= 5:
        qx = 185
        o.append(f'<path d="M{servers[-1]+12},{yS} H{qx-6} V{yL+9}" fill="none" stroke="{V}" stroke-width="1.2"/>')
        o.append(ic('queue', qx, yL, True))
        o.append(text(qx, yL - 14, 'later', 'sv-d', V, 'middle', ';font-size:8.5px'))
    return ''.join(o)

STAGES = [
    ('1 · One server', 'simple, until it fills up', None),
    ('2 · + Cache', 'repeat reads skip the DB', L['cache']),
    ('3 · + Load balancer', 'traffic spread over many servers', L['lb']),
    ('4 · + Replicas', 'a copy survives a crash', L['shard']),
    ('5 · + Shards', 'data too big for one DB', L['shard']),
    ('6 · + Message queue', 'slow work leaves the request', L['mq']),
]

def growth():
    H = 30 + 2 * FH + GY + 6
    f = Fig('dsov1', 680, H, 'ONE SERVICE GROWING WITH LOAD · EACH STEP ADDS ONE COMPONENT (VIOLET)',
            'Six small architecture diagrams, left to right then top to bottom, each adding one component. '
            '1: users talk to one server and one database — simple until it fills up. 2: a cache beside the '
            'server answers repeated reads so they skip the database. 3: a load balancer spreads traffic over '
            'three servers. 4: the database gets replicas, copies that survive a crash, but copies can disagree, '
            'which is the CAP trade-off. 5: the data is split into shards A–H, I–P, Q–Z, one per database. '
            '6: a message queue takes slow work out of the request so it runs later. Each frame links to its lesson.')
    for i, (name, why, href) in enumerate(STAGES):
        r, c = divmod(i, 3)
        x, y = c * (FW + GX), 30 + r * (FH + GY)
        inner = (f'<rect class="nd" x="0" y="0" width="{FW}" height="{FH}" rx="10" fill="var(--bg)" stroke="var(--rule-hi)" stroke-width="1.2"/>'
                 + text(12, 20, name, 'sv-s', 'var(--text)', 'start', ';font-weight:600;font-size:11.5px')
                 + text(12, 36, why, 'sv-d', 'var(--muted)', 'start')
                 + frame(i))
        if href:
            inner = f'<a href="{href}">{inner}</a>'
        g = f'<g transform="translate({x},{y})">{inner}'
        if i == 3:   # copies can disagree -> CAP
            g += f'<a href="{L["cap"]}"><rect class="nd" x="150" y="8" width="60" height="18" rx="9" fill="{VT}" stroke="{V}" stroke-width="1"/>' \
                 + text(180, 20.5, 'CAP →', 'sv-d', V, 'middle', ';font-weight:600;font-size:9.5px') + '</a>'
        f.add(f'<g class="{f.step(0.2 + i * 0.45)}">{g}</g></g>')
    return f.svg()

# ---- figure 2: what becomes hard ----------------------------------------------------
def hard():
    H = 250
    f = Fig('dsov2', 680, H, 'WHAT ONE MACHINE NEVER HAD · PART FAILS · MESSAGES VANISH · COPIES MUST CHOOSE',
            'Three panels. Partial failure: four servers, one crashed and crossed out, one slow, two still working — '
            'the system is half broken, never simply up or down. Unreliable network: server A sends three messages to '
            'server B; the first arrives, the second is lost, the third arrives late, and from silence A cannot tell '
            'a dead B from a slow link. CAP trade-off: a network partition cuts two database copies apart; during the '
            'cut each copy must either refuse writes to stay consistent, or keep answering and risk stale data. '
            'The third panel links to the CAP lesson.')
    PW = 220
    def panel(i, title, sub, body, href=None):
        x = i * (PW + 10)
        inner = (f'<rect class="nd" x="0" y="0" width="{PW}" height="{H-34}" rx="10" fill="var(--bg)" stroke="var(--rule-hi)" stroke-width="1.2"/>'
                 + text(12, 20, title, 'sv-s', 'var(--text)', 'start', ';font-weight:600;font-size:11.5px')
                 + text(12, 36, sub, 'sv-d', 'var(--muted)', 'start') + body)
        if href:
            inner = f'<a href="{href}">{inner}</a>'
        f.add(f'<g class="{f.step(0.2 + i * 0.6)}"><g transform="translate({x},30)">{inner}</g></g>')
    # partial failure
    b = ''
    for k, (st, lab) in enumerate([('ok', 'ok'), ('slow', 'slow'), ('dead', 'down'), ('ok', 'ok')]):
        sx, sy = 46 + (k % 2) * 128, 82 + (k // 2) * 74
        if st == 'dead':
            b += ic('server', sx, sy, bad=True) + ln(sx - 15, sy - 14, sx + 15, sy + 14, R, 1.6) + ln(sx + 15, sy - 14, sx - 15, sy + 14, R, 1.6)
        else:
            b += ic('server', sx, sy, st == 'slow')
        col = R if st == 'dead' else (V if st == 'slow' else 'var(--muted)')
        b += text(sx, sy + 26, lab, 'sv-d', col, 'middle', ';font-weight:600' if st != 'ok' else '')
    b += text(110, 200, 'half broken, not up or down', 'sv-d', 'var(--text)', 'middle', ';font-style:italic')
    panel(0, 'Partial failure', 'some machines fail, the rest run', b)
    # unreliable network
    ax, bx = 34, 186
    b = ic('server', ax, 70) + ic('server', bx, 70) + text(ax, 98, 'A', 'sv-s', 'var(--text)') + text(bx, 98, 'B', 'sv-s', 'var(--text)')
    b += ln(ax, 84, ax, 190, 'var(--rule-hi)', 1, True) + ln(bx, 84, bx, 190, 'var(--rule-hi)', 1, True)
    def msg(y1, y2, lab, kind):
        if kind == 'lost':
            o = ln(ax, y1, 110, (y1 + y2) / 2, R, 1.3, True)
            return o + text(118, (y1 + y2) / 2 + 4, '✕ lost', 'sv-d', R, 'start', ';font-weight:600')
        col = V if kind == 'late' else 'var(--muted)'
        o = ln(ax, y1, bx - 4, y2, col, 1.3) + f'<path d="M{bx-6},{y2-4} L{bx},{y2} L{bx-7},{y2+2}z" fill="{col}"/>'
        return o + text(ax + 8, y1 - 4, lab, 'sv-d', col, 'start', ';font-size:9.5px')
    b += msg(112, 122, 'm1', 'ok') + msg(140, 152, 'm2', 'lost') + msg(166, 192, 'm3 · late', 'late')
    b += text(110, 208, 'silence: dead or slow?', 'sv-d', 'var(--text)', 'middle', ';font-style:italic')
    panel(1, 'Unreliable network', 'messages lost or late', b)
    # CAP
    b = ic('db', 46, 82) + ic('db', 174, 82) + text(46, 108, 'copy 1', 'sv-d', 'var(--muted)') + text(174, 108, 'copy 2', 'sv-d', 'var(--muted)')
    b += ln(60, 82, 100, 82, 'var(--muted)', 1.2) + ln(120, 82, 160, 82, 'var(--muted)', 1.2)
    b += f'<path d="M110,58 L104,70 L116,78 L104,90 L112,104" fill="none" stroke="{R}" stroke-width="1.8"/>'
    b += text(110, 122, 'partition', 'sv-d', R, 'middle', ';font-weight:600')
    for k, (h, d) in enumerate([('C · consistent', 'refuse writes, stay correct'), ('A · available', 'keep answering, maybe stale')]):
        yy = 140 + k * 36
        b += f'<rect x="14" y="{yy}" width="192" height="30" rx="6" fill="{VT if k == 0 else TINT}" stroke="{V if k == 0 else B}" stroke-width="1"/>'
        b += text(24, yy + 13, h, 'sv-d', V if k == 0 else 'var(--brand-hi)', 'start', ';font-weight:600')
        b += text(24, yy + 25, d, 'sv-d', 'var(--muted)', 'start', ';font-size:9.5px')
    panel(2, 'CAP trade-off', 'during a cut, pick one', b, L['cap'])
    return f.svg()

def sections():
    return f'''<section id="distov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Growing with load</h2></div>
  <p class="key">A large service is <em>one small service that kept adding a part</em> each time a limit was hit.</p>
<figure class="gist">
{growth()}
</figure>
  <ul class="why">
    <li>Every part answers one limit: speed (<a href="{L['cache']}">cache</a>), traffic (<a href="{L['lb']}">load balancer</a>), crashes and size (<a href="{L['shard']}">replicas, shards</a> — and copies then face <a href="{L['cap']}">CAP</a>), slow work (<a href="{L['mq']}">queue</a>).</li>
    <li>Add parts only when the limit is real — each one is another machine that can fail.</li>
  </ul>
</section>

<section id="distov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>What becomes hard</h2></div>
  <p class="key">Many machines bring problems one machine never had: <em>parts fail, messages vanish, copies disagree</em>.</p>
<figure class="gist">
{hard()}
</figure>
  <ul class="why">
    <li>Timeouts and retries are the only tools against silence — so every request must be safe to repeat.</li>
    <li>The choice between consistent and available is made per feature; the <a href="{L['cap']}">CAP lesson</a> shows how.</li>
  </ul>
</section>

'''

if __name__ == '__main__':
    s = open(PAGE, encoding='utf-8').read()
    a = s.index('<section id="distov-s1"')
    lo = s.index('<h2>Learning order</h2>')
    b = s.rindex('<section id=', 0, lo)
    tail = s[b:]
    tail = re.sub(r'<section id="distov-s\d+" class="lesson">\n  <div class="sh"><b>\d+</b><h2>Learning order',
                  '<section id="distov-s3" class="lesson">\n  <div class="sh"><b>03</b><h2>Learning order', tail, 1)
    s = s[:a] + sections() + tail
    s = re.sub(r'<p class="lede">.*?</p>', '<p class="lede">One server grows into many by <b>adding one part per limit</b> — cache, load balancer, replicas, shards, queue — and pays for it with <b>partial failure, lost messages and copies that must choose</b>.</p>', s, 1, flags=re.S)
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="How one server grows into a distributed system — cache, load balancer, replicas, shards, queue — what becomes hard with many machines, and the order to learn this shelf."', s, 1)
    open(PAGE, 'w', encoding='utf-8').write(s)
    print('ok')
