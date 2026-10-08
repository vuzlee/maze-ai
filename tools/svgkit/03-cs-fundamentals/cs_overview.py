# -*- coding: utf-8 -*-
"""CS fundamentals shelf overview: gallery of OS and networking pictures + one URL through the layers.

    python3 tools/svgkit/03-cs-fundamentals/cs_overview.py   # rewrites sections 01-02 in place
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from overview import Fig, text, gallery, cell, dot, ln, arr, B, V, FL, TINT, VTINT

PAGE = 'content/03-cs-fundamentals/01-overview/cs-overview/index.html'
OS = '../../02-os/'
NW = '../../03-networking/'
PY_GIL = '../../../02-python/04-concurrency/thread-process-gil/index.html'
M = ';font-family:var(--mono);font-size:9px'
R = 'var(--rose)'
RT = 'rgba(var(--rose-a),.08)'

def t(x, y, s, col='var(--text)', a='start', ex=M):
    return text(x, y, s, 'sv-d', col, a, ex)

def box(x, y, w, h, col=B, fill=TINT, dash=False, rx=3):
    d = ' stroke-dasharray="3 2"' if dash else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{col}" stroke-width="1.1"{d}/>'

def arrow(x1, y1, x2, y2, col='var(--muted)'):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - 5 * math.cos(a), y2 - 5 * math.sin(a)
    px, py = 3 * math.sin(a), -3 * math.cos(a)
    return (ln(x1, y1, bx, by, col) +
            f'<path d="M{x2:.1f},{y2:.1f} L{bx+px:.1f},{by+py:.1f} L{bx-px:.1f},{by-py:.1f}z" fill="{col}"/>')

# ---- one machine ----
def d_process(x, y):
    o = box(x + 30, y, 78, 58, 'var(--rule-hi)', 'var(--bg)', rx=5)
    for i, (n, hl) in enumerate((('code', False), ('heap ↓', False), ('', False), ('stack ↑', True))):
        if n:
            o += box(x + 34, y + 3 + i * 13.5, 70, 11.5, V if hl else B, VTINT if hl else TINT, rx=2) + t(x + 69, y + 11.5 + i * 13.5, n, V if hl else 'var(--text)', 'middle', ';font-size:8px;font-family:var(--mono)')
    o += t(x + 112, y + 10, 'low', 'var(--faint)', 'start', ';font-size:8px') + t(x + 112, y + 56, 'high', 'var(--faint)', 'start', ';font-size:8px')
    return o

def d_threads(x, y):
    o = box(x + 2, y + 36, 134, 20, B, TINT, rx=4) + t(x + 69, y + 49, 'shared heap', 'var(--text)', 'middle')
    for i in range(3):
        cx = x + 22 + i * 47
        o += f'<path d="M{cx},{y+2} q5,8 0,14 q-5,8 0,14" fill="none" stroke="{V}" stroke-width="1.4"/>'
        o += arrow(cx, y + 30, cx + (6 if i == 0 else 0), y + 35, V)
        o += t(cx + 7, y + 12, f'T{i+1}', V, 'start', ';font-size:8px;font-family:var(--mono)')
    return o

def d_vm(x, y):
    o = t(x + 14, y + 4, 'virtual', 'var(--faint)', 'middle', ';font-size:8px') + t(x + 69, y + 4, 'page table', 'var(--faint)', 'middle', ';font-size:8px') + t(x + 122, y + 4, 'RAM', 'var(--faint)', 'middle', ';font-size:8px')
    for i in range(4):
        o += cell(x + 4, y + 9 + i * 12, 20, 11, '', i == 1)
        o += cell(x + 52, y + 9 + i * 12, 34, 11, ['→ 2', '→ 0', '→ 3', 'disk'][i], i == 1)
        o += cell(x + 112, y + 9 + i * 12, 20, 11, '', i == 0)
    o += arrow(x + 25, y + 26.5, x + 50, y + 26.5, V) + arrow(x + 87, y + 26.5, x + 110, y + 15, V)
    return o

def d_lock(x, y):
    o = box(x + 50, y + 18, 38, 22, B, TINT, rx=4) + t(x + 69, y + 32, 'n = 5', 'var(--text)', 'middle')
    o += f'<path d="M{x+64},{y+18} v-6 a5,5 0 0 1 10,0 v6" fill="none" stroke="{B}" stroke-width="1.3"/>'
    o += box(x + 2, y + 6, 34, 16, V, VTINT, rx=8) + t(x + 19, y + 17, 'T1', V, 'middle') + arrow(x + 37, y + 16, x + 49, y + 24, V)
    o += box(x + 102, y + 36, 34, 16, R, RT, True, 8) + t(x + 119, y + 47, 'T2', R, 'middle')
    o += t(x + 119, y + 28, 'waits', R, 'middle', ';font-size:8px')
    o += t(x + 19, y + 50, 'holds', V, 'middle', ';font-size:8px')
    return o

# ---- two machines ----
def d_layers(x, y):
    L = ['application', 'transport', 'internet', 'link']
    o = ''
    for i, n in enumerate(L):
        o += box(x + 18, y + i * 14.5, 102, 12.5, V if i == 1 else B, VTINT if i == 1 else TINT, rx=2)
        o += t(x + 69, y + 9.3 + i * 14.5, n, V if i == 1 else 'var(--text)', 'middle', ';font-size:8px;font-family:var(--mono)')
    return o

def d_dns(x, y):
    steps = [('.', 'root'), ('com.', 'TLD'), ('ex.com', '93.184…')]
    o = box(x, y + 20, 30, 18, B, TINT, rx=4) + t(x + 15, y + 32, 'you', 'var(--text)', 'middle', ';font-size:8px')
    for i, (n, sub) in enumerate(steps):
        xx = x + 36 + i * 34
        hl = i == 2
        o += box(xx, y + 4, 33, 16, V if hl else 'var(--rule-hi)', VTINT if hl else 'var(--bg)', rx=4) + t(xx + 16.5, y + 15, n, V if hl else 'var(--text)', 'middle', ';font-size:7.5px;font-family:var(--mono)')
        o += arrow(x + 30, y + 27, xx + 16.5, y + 21, 'var(--muted)')
    o += t(x + 138, y + 50, 'ex.com → 93.184.216.34', V, 'end', ';font-size:7.5px;font-family:var(--mono)')
    return o

def seqbase(x, y):
    o = t(x + 18, y + 4, 'client', 'var(--muted)', 'middle', ';font-size:8px') + t(x + 120, y + 4, 'server', 'var(--muted)', 'middle', ';font-size:8px')
    o += ln(x + 18, y + 8, x + 18, y + 58, 'var(--rule-hi)') + ln(x + 120, y + 8, x + 120, y + 58, 'var(--rule-hi)')
    return o

def d_tcp(x, y):
    o = seqbase(x, y)
    for i, (n, right) in enumerate((('SYN', True), ('SYN-ACK', False), ('ACK', True))):
        yy = y + 16 + i * 15
        o += arrow(x + 18, yy, x + 120, yy + 8, B) if right else arrow(x + 120, yy, x + 18, yy + 8, V)
        o += t(x + 69, yy + 1, n, V if not right else 'var(--text)', 'middle', ';font-size:8px;font-family:var(--mono)')
    return o

def d_tls(x, y):
    o = seqbase(x, y)
    o += arrow(x + 18, y + 16, x + 120, y + 22, B) + t(x + 69, y + 16, 'hello + key share', 'var(--text)', 'middle', ';font-size:7.5px;font-family:var(--mono)')
    o += arrow(x + 120, y + 30, x + 18, y + 36, B) + t(x + 69, y + 30, 'cert + key share', 'var(--text)', 'middle', ';font-size:7.5px;font-family:var(--mono)')
    o += box(x + 30, y + 42, 78, 13, V, VTINT, rx=6) + t(x + 69, y + 51.5, 'shared secret', V, 'middle', ';font-size:8px')
    return o

def d_http(x, y):
    o = box(x + 2, y + 2, 64, 54, B, TINT, rx=4)
    o += t(x + 6, y + 13, 'GET /users/7', 'var(--text)', 'start', ';font-size:7.5px;font-family:var(--mono)')
    o += t(x + 6, y + 25, 'Host: ex.com', 'var(--muted)', 'start', ';font-size:7.5px;font-family:var(--mono)')
    o += box(x + 72, y + 2, 64, 54, V, VTINT, rx=4)
    o += t(x + 76, y + 13, '200 OK', V, 'start', ';font-size:7.5px;font-family:var(--mono);font-weight:600')
    o += t(x + 76, y + 25, '{"id": 7}', 'var(--text)', 'start', ';font-size:7.5px;font-family:var(--mono)')
    o += t(x + 34, y + 48, 'request', 'var(--faint)', 'middle', ';font-size:8px') + t(x + 104, y + 48, 'response', 'var(--faint)', 'middle', ';font-size:8px')
    return o

def d_rest(x, y):
    o = t(x + 2, y + 12, '/users/7/orders', 'var(--text)', 'start', ';font-size:9.5px;font-family:var(--mono)')
    for i, (m, s) in enumerate((('GET', 'read'), ('POST', 'create'), ('DELETE', 'remove'))):
        yy = y + 24 + i * 12
        o += box(x + 2, yy, 40, 10.5, B, TINT, rx=2) + t(x + 22, yy + 8, m, 'var(--text)', 'middle', ';font-size:7.5px;font-family:var(--mono)')
        o += t(x + 48, yy + 8, s, 'var(--muted)', 'start', ';font-size:8px')
    return o

ONE = [('Process', d_process, OS + 'os-overview/index.html'),
       ('Threads share memory', d_threads, PY_GIL),
       ('Virtual memory', d_vm, OS + 'memory-virtual-paging/index.html'),
       ('Lock · race', d_lock, OS + 'lock-deadlock-race/index.html')]
TWO = [('Layer stack', d_layers, NW + 'osi-model/index.html'),
       ('DNS lookup', d_dns, NW + 'dns-tls/index.html'),
       ('TCP handshake', d_tcp, NW + 'tcp-http/index.html'),
       ('TLS key exchange', d_tls, NW + 'dns-tls/index.html'),
       ('HTTP request', d_http, NW + 'tcp-http/index.html'),
       ('REST resource', d_rest, NW + 'rest-api-design/index.html')]

def fig_gallery():
    f = Fig('csov1', 680, 400, 'THE WHOLE SHELF · FOUR PICTURES OF ONE MACHINE, SIX OF TWO MACHINES TALKING',
            'Two bands of pictures. One machine: a process with code, heap and stack regions; three threads '
            'sharing one heap; virtual pages mapped through a page table onto physical RAM; one thread holding a '
            'lock while another waits. Two machines: the layer stack application, transport, internet, link; a DNS '
            'lookup walking from the root to com to the name\'s address; the TCP three-way handshake SYN, SYN-ACK, '
            'ACK; a TLS key exchange ending in a shared secret; an HTTP GET request and its 200 OK response; a REST '
            'resource URL with the verbs GET, POST and DELETE. Each tile links to its lesson.')
    f.h = gallery(f, [('ONE MACHINE', 'the operating system shares it', ONE),
                      ('TWO MACHINES', 'the network connects them', TWO)]) + 4
    return f.svg()

def fig_url():
    f = Fig('csov2', 680, 420, 'TYPE A URL · DOWN THE CLIENT LAYERS, ACROSS THE WIRE, UP THE SERVER',
            'You type https://ex.com/users/7. On the client, the request goes down a stack of layers: the '
            'application layer builds the HTTP request after DNS turns the name into an address; TLS encrypts it; '
            'TCP splits it into numbered segments after a handshake; IP puts an address on each packet; the link '
            'layer sends frames on the wire. The packets cross the internet, then climb the same layers on the '
            'server in reverse: link, IP, TCP reassembles, TLS decrypts, and the HTTP server answers 200 OK. The '
            'operating system on each side runs the lower layers in its kernel. Each layer links to its lesson.')
    L = [('HTTP', 'request · response', NW + 'tcp-http/index.html', 'GET /users/7'),
         ('DNS · TLS', 'name → IP · encrypt', NW + 'dns-tls/index.html', 'lookup · encrypt'),
         ('TCP', 'reliable, in order', NW + 'tcp-http/index.html', 'handshake · segments'),
         ('IP', 'address · route', NW + 'osi-model/index.html', 'packets'),
         ('Link', 'frames on a wire', NW + 'osi-model/index.html', 'frames')]
    top, dy, W = 70, 58, 190
    CX, SX = 120, 560
    f.add(f'<g class="{f.step(0.1)}">' + text(CX, 46, 'CLIENT · your laptop', 'sv-hv', B, 'middle')
          + text(SX, 46, 'SERVER · ex.com', 'sv-hv', B, 'middle') + '</g>')
    # kernel bands
    kb = f.step(0.2)
    for cx in (CX, SX):
        f.add(f'<g class="{kb}"><rect x="{cx-W/2-8}" y="{top+2*dy-28}" width="{W+16}" height="{3*dy+16}" rx="10" fill="var(--sunk)" stroke="var(--rule-hi)" stroke-dasharray="4 3"/>'
              + t(cx + W / 2 + 4, top + 5 * dy - 16, 'OS kernel', 'var(--faint)', 'end', ';font-size:8.5px') + '</g>')
    # down path / across / up path
    pc = f.step(0.4, draw=True)
    yb = top + 4 * dy
    f.add(f'<path class="{pc}" pathLength="1" d="M{CX-W/2-20},{top} V{yb+50} H{SX+W/2+20} V{top}" fill="none" stroke="{V}" stroke-width="2" stroke-dasharray="none"/>')
    f.add(f'<path class="{f.step(0.9)}" d="M{CX-W/2-24},{top+dy*2.5} l4,8 l4,-8z" fill="{V}"/>')
    f.add(f'<path class="{f.step(2.8)}" d="M{SX+W/2+16},{top+8} l4,-8 l4,8z" fill="{V}"/>')
    f.add(f'<g class="{f.step(1.6)}">' + t(340, yb + 66, 'the internet · routers forward packets', V, 'middle', ';font-size:10px;font-weight:600;font-family:var(--body)') + '</g>')
    for i, (n, note, href, act) in enumerate(L):
        y = top + i * dy
        f.node(CX, y, n, note, 'violet' if i == 0 else 'brand', f.step(0.4 + i * 0.25), href, None, w=W, h=42)
        f.node(SX, y, n, note, 'violet' if i == 0 else 'brand', f.step(2.6 - i * 0.2), href, None, w=W, h=42)
        f.add(f'<g class="{f.step(0.5 + i * 0.25)}">' + t(340, y + 4, ('↓ ' if True else '') + act, 'var(--muted)', 'middle', ';font-size:9px;font-family:var(--mono)') + '</g>')
    f.add(f'<g class="{f.step(3.0)}">' + t(340, top - 22, 'https://ex.com/users/7', V, 'middle', ';font-size:11px;font-weight:600')
          + t(340, top + 5 * dy + 46, 'response: 200 OK climbs back the same way', 'var(--muted)', 'middle', ';font-size:9.5px;font-family:var(--body)') + '</g>')
    f.h = top + 5 * dy + 54
    return f.svg()

SECTIONS = '''<section id="csov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>What CS fundamentals is</h2></div>
  <p class="key">The operating system <em>shares one machine</em> between many programs; networking lets <em>two machines talk</em>. This shelf is these ten pictures.</p>
<figure class="gist">
{g1}
</figure>
  <ul class="why">
    <li>Both halves hide hard problems behind a simple promise — “you have the whole machine” and “bytes arrive in order” — and knowing how the promise is kept explains why it sometimes breaks.</li>
    <li>Language-independent: Python, Java and C all ask the same OS for threads, memory and sockets. Thread scheduling is taught once, in <a href="../../../02-python/04-concurrency/thread-process-gil/index.html">Process, thread &amp; GIL</a>.</li>
  </ul>
</section>

<section id="csov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>What happens when you type a URL</h2></div>
  <p class="key">One request <em>goes down every layer on your machine, crosses the wire, and climbs the same layers</em> on the server.</p>
<figure class="gist">
{g2}
</figure>
  <ul class="why">
    <li>Each layer only talks to the one above and below — that is why HTTP does not care whether the wire is Wi-Fi or fibre. The full model is in <a href="../../03-networking/osi-model/index.html">OSI model</a>.</li>
    <li>The lower layers run inside the OS kernel, which is where the two halves of this shelf meet. Many machines acting as one opens the <a href="../../../04-distributed/01-overview/distributed-overview/index.html">Distributed systems shelf</a>.</li>
  </ul>
</section>

'''

if __name__ == '__main__':
    s = open(PAGE, encoding='utf-8').read()
    a = s.index('<section id="csov-s1"')
    b = s.rindex('<section', 0, s.index('<h2>Learning order</h2>'))
    s = re.sub(r'<section id="csov-s\d" class="lesson">\n  <div class="sh"><b>\d+</b><h2>Learning order',
               '<section id="csov-s3" class="lesson">\n  <div class="sh"><b>03</b><h2>Learning order', s)
    s = s[:a] + SECTIONS.format(g1=fig_gallery(), g2=fig_url()) + s[b:]
    blurb = ('What operating systems and networking are in ten pictures, what happens layer by layer when you '
             'type a URL, and the order to learn this shelf.')
    s = re.sub(r'(id="art-csov"[^>]*data-blurb=")[^"]*"', lambda m: m.group(1) + blurb + '"', s)
    s = re.sub(r'<p class="lede">.*?</p>', '<p class="lede">The layer under every program you write: <b>the operating system shares one machine</b>, and <b>networking connects two</b>. Every web request crosses both.</p>', s, count=1)
    open(PAGE, 'w', encoding='utf-8').write(s)
    print('ok')
