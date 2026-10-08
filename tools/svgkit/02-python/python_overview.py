# -*- coding: utf-8 -*-
"""Python shelf overview: gallery of the language's pictures, life of one line, family tree.

    python3 tools/svgkit/02-python/python_overview.py   # rewrites sections 01-03 in place
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from overview import Fig, text, gallery, cell, dot, ln, arr, B, V, FL, TINT, VTINT

PAGE = 'content/02-python/01-overview/python-overview/index.html'
LC = '../../02-language-core/'
BS = '../../03-builtin-structures/'
CC = '../../04-concurrency/'
ML = '../../../07-machine-learning/01-overview/ml-overview/index.html'
M = ';font-family:var(--mono);font-size:9px'
R = 'var(--rose)'

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

# ---- gallery drawings: box 138 x 58, top-left (x, y) ----
def d_names(x, y):
    o = box(x + 2, y + 6, 26, 15, V, VTINT, rx=7) + t(x + 15, y + 17, 'a', V, 'middle')
    o += box(x + 2, y + 36, 26, 15, V, VTINT, rx=7) + t(x + 15, y + 47, 'b', V, 'middle')
    o += arrow(x + 30, y + 13, x + 82, y + 26) + arrow(x + 30, y + 43, x + 82, y + 32)
    o += box(x + 84, y + 18, 50, 22) + t(x + 109, y + 32, '[1, 2]', 'var(--text)', 'middle')
    return o + t(x + 109, y + 54, 'one object', 'var(--faint)', 'middle', ';font-size:8.5px')

def d_list(x, y):
    o = ''.join(cell(x + 4 + i * 20, y + 2, 19, 16) for i in range(5))
    vals = ['3', "'a'", '2.5', 'None']
    for i, v in enumerate(vals):
        cx = x + 13.5 + i * 20
        o += dot(cx, y + 10, '', False, 2.4)
        ox = x + 8 + i * 33
        o += arrow(cx, y + 13, ox + 14, y + 36)
        o += box(ox, y + 37, 28, 15, 'var(--rule-hi)', 'var(--bg)') + t(ox + 14, y + 48, v, 'var(--text)', 'middle', ';font-size:8.5px;font-family:var(--mono)')
    return o + t(x + 108, y + 13, 'pointers', 'var(--faint)', 'start', ';font-size:8.5px')

def d_dict(x, y):
    o = t(x + 0, y + 30, "'cat'", V) + arrow(x + 26, y + 27, x + 46, y + 27, V)
    o += t(x + 36, y + 20, 'hash', 'var(--faint)', 'middle', ';font-size:8px')
    for i in range(4):
        o += cell(x + 50, y + 1 + i * 14, 16, 13, i, i == 1)
    o += arrow(x + 66, y + 22, x + 78, y + 22, V) + box(x + 80, y + 15, 56, 14, V, VTINT) + t(x + 108, y + 25, "'cat': 4", V, 'middle')
    o += box(x + 80, y + 43, 56, 14, 'var(--rule-hi)', 'var(--bg)', True) + t(x + 108, y + 53, 'empty', 'var(--faint)', 'middle', ';font-size:8px')
    return o

def d_gen(x, y):
    o = ln(x + 6, y + 30, x + 132, y + 30, 'var(--rule-hi)', 1.4)
    for i, xx in enumerate((22, 68, 114)):
        on = i == 1
        o += f'<rect x="{x+xx-3:.1f}" y="{y+23}" width="2.5" height="14" fill="{VTINT if on else TINT}" stroke="{V if on else B}" stroke-width=".8"/><rect x="{x+xx+1.5:.1f}" y="{y+23}" width="2.5" height="14" fill="{VTINT if on else TINT}" stroke="{V if on else B}" stroke-width=".8"/>'
        o += t(x + xx, y + 13, f'yield {i+1}', V if on else 'var(--text)', 'middle', ';font-size:8.5px;font-family:var(--mono)')
        o += t(x + xx, y + 52, 'next()', 'var(--faint)', 'middle', ';font-size:8px;font-family:var(--mono)')
    return o

def d_deco(x, y):
    o = box(x + 6, y + 4, 126, 52, V, VTINT, rx=8) + t(x + 14, y + 16, 'wrapper', V)
    o += t(x + 126, y + 16, '@timer', V, 'end')
    o += box(x + 34, y + 24, 70, 24, B, TINT, rx=6) + t(x + 69, y + 39, 'f(x)', 'var(--text)', 'middle')
    o += arrow(x + 14, y + 36, x + 33, y + 36, V) + arrow(x + 105, y + 36, x + 126, y + 36, V)
    return o

def d_exc(x, y):
    names = ['main()', 'load()', 'parse()']
    o = ''
    for i, n in enumerate(names):
        yy = y + 2 + i * 19
        o += box(x + 4, yy, 82, 16, R if i == 2 else B, 'rgba(var(--rose-a),.08)' if i == 2 else TINT) + t(x + 10, yy + 11.5, n, R if i == 2 else 'var(--text)')
    o += t(x + 80, y + 51.5, '✕', R, 'end', ';font-weight:700')
    o += f'<path d="M{x+88},{y+48} C{x+108},{y+48} {x+108},{y+12} {x+92},{y+10}" fill="none" stroke="{R}" stroke-width="1.2"/>'
    o += f'<path d="M{x+92},{y+10} l5,-3 l0,6z" fill="{R}"/>'
    o += t(x + 110, y + 26, 'raise', R, 'start', ';font-size:8.5px') + t(x + 104, y + 12, 'except', B, 'start', ';font-size:8.5px')
    return o

def d_class(x, y):
    o = box(x + 40, y + 1, 58, 18, B, TINT, rx=5) + t(x + 69, y + 13.5, 'Dog', 'var(--text)', 'middle')
    for xx, n in ((x + 6, 'rex'), (x + 80, 'fido')):
        o += ln(xx + 26, y + 36, x + 69, y + 20, 'var(--muted)', 1.1, True)
        o += box(xx, y + 36, 52, 18, 'var(--rule-hi)', 'var(--bg)', rx=5) + t(xx + 26, y + 48.5, n, 'var(--text)', 'middle')
    return o + t(x + 69, y + 32, '__class__', 'var(--faint)', 'middle', ';font-size:8px;font-family:var(--mono)')

def d_gil(x, y):
    o = ''
    runs = [[(0, 30)], [(30, 64)], [(64, 100)]]
    for i in range(3):
        yy = y + 6 + i * 17
        o += t(x, yy + 8, f'T{i+1}', 'var(--muted)')
        o += f'<rect x="{x+18}" y="{yy}" width="116" height="10" rx="2" fill="var(--sunk)"/>'
        for a, b in runs[i]:
            o += f'<rect x="{x+18+a}" y="{yy}" width="{b-a}" height="10" rx="2" fill="{VTINT}" stroke="{V}" stroke-width="1"/>'
    return o + t(x + 134, y + 2, 'one at a time', V, 'end', ';font-size:8px')

def d_async(x, y):
    import math
    cx, cy, r = x + 46, y + 29, 22
    o = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{B}" stroke-width="1.2" stroke-dasharray="3 2"/>'
    o += f'<path d="M{cx+r-3},{cy-6} l3,6 l4,-5z" fill="{B}"/>'
    o += t(cx, cy + 3, 'loop', B, 'middle', ';font-size:8.5px')
    for i, a in enumerate((-90, 30, 150)):
        px, py = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        o += dot(px, py, '', i == 0, 5)
    for i, s in enumerate(('task A: run', 'task B: await', 'task C: await')):
        o += t(x + 76, y + 14 + i * 15, s, V if i == 0 else 'var(--faint)', 'start', ';font-size:8px;font-family:var(--mono)')
    return o

def d_ref(x, y):
    o = box(x + 2, y + 6, 22, 14, 'var(--rule-hi)', 'var(--bg)', True, 7) + t(x + 13, y + 16, 'a', 'var(--faint)', 'middle')
    o += ln(x + 26, y + 13, x + 56, y + 24, 'var(--rule-hi)', 1.1, True) + t(x + 41, y + 14, '✕', R, 'middle', ';font-weight:700')
    o += box(x + 58, y + 14, 46, 22, R, 'rgba(var(--rose-a),.06)', True) + t(x + 81, y + 28, '[1, 2]', 'var(--faint)', 'middle')
    o += t(x + 110, y + 24, 'refs', 'var(--muted)', 'start', ';font-size:8px') + t(x + 110, y + 35, '0', R, 'start', ';font-weight:700;font-size:10px;font-family:var(--mono)')
    return o + t(x + 81, y + 52, 'freed at once', R, 'middle', ';font-size:8.5px')

CORE = [('Name → object', d_names, LC + 'memory-model-mutability/index.html'),
        ('List', d_list, BS + 'list-tuple-set/index.html'),
        ('Dict', d_dict, BS + 'dict-hash-table/index.html'),
        ('Generator', d_gen, LC + 'iterator-generator/index.html'),
        ('Decorator', d_deco, LC + 'decorator-context-manager/index.html'),
        ('Exception', d_exc, LC + 'exception-handling/index.html')]
RUN = [('Class & instance', d_class, '../../06-oop/oop-python/index.html'),
       ('GIL', d_gil, CC + 'thread-process-gil/index.html'),
       ('Asyncio event loop', d_async, CC + 'asyncio/index.html'),
       ('Refcount → 0', d_ref, LC + 'memory-management-gc/index.html')]

def fig_gallery():
    f = Fig('pyov1', 680, 400, 'THE WHOLE LANGUAGE · SIX CORE PICTURES, FOUR AT RUN TIME',
            'Two bands of pictures. Core: two names pointing at one object; a list as an array of pointers to '
            'objects; a dict hashing a key to a slot; a generator pausing at each yield until next is called; a '
            'decorator, a wrapper function around the original; an exception raised in the innermost frame and '
            'climbing up the call stack to the frame that catches it. Run time: a class with two instances; three '
            'threads taking turns to hold the GIL; an asyncio event loop cycling through tasks; an object whose '
            'reference count hits zero and is freed. Each tile links to its lesson.')
    f.h = gallery(f, [('CORE', 'what every line is made of', CORE),
                      ('RUN TIME', 'what happens while it runs', RUN)]) + 4
    return f.svg()

def fig_line():
    f = Fig('pyov2', 680, 270, 'LIFE OF ONE LINE · x = a + b FROM SOURCE TO HEAP',
            'The line x = a + b travels left to right through four stages. Source: the text in app.py. '
            'Bytecode: the compiler turns it into four instructions, LOAD_NAME a, LOAD_NAME b, BINARY_OP plus, '
            'STORE_NAME x, cached in a .pyc file. CPython VM: a loop written in C runs one instruction at a time; '
            'only when BINARY_OP runs does it check the types, int plus int, so a type error appears at run time. '
            'Heap: a and b name int objects 2 and 3; the result 5 is a new object that x now names; any object '
            'no name points to has reference count zero and is freed. A small packet moves along the stages.')
    W, G, top = 152, 24, 50
    xs = [i * (W + G) for i in range(4)]
    heads = [('SOURCE', 'app.py'), ('BYTECODE', 'compiled once · .pyc'), ('CPYTHON VM', 'a loop in C'), ('HEAP', 'objects live here')]
    for i, (h, sub) in enumerate(heads):
        s = f.step(0.2 + i * 0.5)
        o = text(xs[i], top - 14, h, 'sv-hv', B, 'start')
        o += f'<rect x="{xs[i]}" y="{top}" width="{W}" height="150" rx="10" fill="var(--bg)" stroke="var(--rule-hi)" stroke-width="1.2"/>'
        o += t(xs[i] + 10, top + 140, sub, 'var(--muted)', 'start', ';font-size:9.5px')
        f.add(f'<g class="{s}">{o}</g>')
    # source
    f.add(f'<g class="{f.step(0.4)}">' + box(xs[0] + 12, top + 46, 128, 30, B, TINT, rx=6)
          + t(xs[0] + 76, top + 65, 'x = a + b', 'var(--text)', 'middle', ';font-size:12px') + '</g>')
    # bytecode
    ops = [('LOAD_NAME', 'a'), ('LOAD_NAME', 'b'), ('BINARY_OP', '+'), ('STORE_NAME', 'x')]
    o = ''
    for i, (op, arg) in enumerate(ops):
        yy = top + 18 + i * 24
        hl = op == 'BINARY_OP'
        o += box(xs[1] + 10, yy, 132, 19, V if hl else B, VTINT if hl else TINT)
        o += t(xs[1] + 16, yy + 13, op, V if hl else 'var(--text)') + t(xs[1] + 134, yy + 13, arg, V if hl else 'var(--muted)', 'end')
    f.add(f'<g class="{f.step(0.9)}">{o}</g>')
    # VM
    vx = xs[2]
    o = f'<circle cx="{vx+76}" cy="{top+50}" r="26" fill="none" stroke="{B}" stroke-width="1.3" stroke-dasharray="4 3"/>'
    o += f'<path d="M{vx+102},{top+44} l0,10 l-6,-6z" fill="{B}"/>'
    o += t(vx + 76, top + 47, 'fetch', 'var(--text)', 'middle', ';font-size:8.5px') + t(vx + 76, top + 58, 'run op', 'var(--text)', 'middle', ';font-size:8.5px')
    o += box(vx + 10, top + 88, 132, 30, V, VTINT, rx=6)
    o += t(vx + 76, top + 100, 'types checked now', V, 'middle', ';font-size:9px;font-weight:600')
    o += t(vx + 76, top + 112, 'int + int → ok', V, 'middle')
    f.add(f'<g class="{f.step(1.4)}">{o}</g>')
    # heap
    hx = xs[3]
    o = ''
    for i, (n, v, hl) in enumerate((('a', '2', False), ('b', '3', False), ('x', '5', True))):
        yy = top + 16 + i * 30
        o += box(hx + 10, yy, 24, 18, V, VTINT, rx=8) + t(hx + 22, yy + 12.5, n, V, 'middle')
        o += arrow(hx + 36, yy + 9, hx + 72, yy + 9)
        o += box(hx + 74, yy, 66, 18, V if hl else B, VTINT if hl else TINT) + t(hx + 107, yy + 12.5, f'int {v}', V if hl else 'var(--text)', 'middle')
    o += t(hx + 10, top + 120, 'refs 0 → freed', 'var(--rose)', 'start', ';font-size:9px')
    f.add(f'<g class="{f.step(1.9)}">{o}</g>')
    # arrows between stages
    for i in range(3):
        f.add(f'<g class="{f.step(0.6 + i * 0.5)}">' + arrow(xs[i] + W + 3, top + 75, xs[i + 1] - 3, top + 75, 'var(--muted)') + '</g>')
    # bottom notes
    notes = ['compile: no build step', 'one op at a time', 'interpreted, not machine code', 'garbage-collected']
    # packet
    path = f'M{xs[0]+76},{top+61} L{xs[0]+W+12},{top+75} L{xs[2]+76},{top+75} L{xs[3]-6},{top+75} L{xs[3]+54},{top+85}'
    f.add('<style>@keyframes pyov2-pk{0%,8%{offset-distance:0%;opacity:0}12%{opacity:1}'
          '100%{offset-distance:100%;opacity:1}}'
          f'.pyov2-pk{{offset-path:path("{path}");offset-distance:100%;offset-rotate:0deg}}'
          '@media (prefers-reduced-motion:no-preference){.pyov2-pk{animation:pyov2-pk 3.2s ease-in-out 1 forwards}}</style>')
    f.add(f'<circle class="pyov2-pk" r="4" fill="{V}" fill-opacity=".85"/>')
    f.add(f'<g class="{f.step(2.4)}">' + t(0, top + 178, 'source → bytecode → VM → objects: every Python line, every time it runs',
                                          V, 'start', ';font-size:10px;font-weight:600;font-family:var(--body)') + '</g>')
    f.h = top + 186
    return f.svg()

def fig_tree():
    f = Fig('pyov3', 680, 400, 'LINEAGE · FOUR ANCESTORS ABOVE, LANGUAGES AND AN ECOSYSTEM BELOW',
            'A top-down family tree. At the top, four ancestors: ABC, a teaching language that gave Python its '
            'indentation; Modula-3, which gave modules and exceptions; C, the language CPython is written in; Lisp, '
            'which gave lambda, map and filter. They join into Python, 1991. Two violet notes beside Python: 2008, '
            'Python 3 breaks compatibility with Python 2; 2024, Python 3.13 ships a free-threaded build without the GIL. '
            'Below, on the left, languages it influenced: Ruby, Julia and Mojo. On the right, the ecosystem branch: '
            'NumPy, from which grow pandas, scikit-learn and PyTorch, the road into machine learning.')
    anc = [(85, 'ABC', 'indentation · teaching'), (255, 'Modula-3', 'modules · exceptions'),
           (425, 'C', 'CPython is written in C'), (595, 'Lisp', 'lambda · map · filter')]
    PY = (340, 160)
    for i, (x, n, note) in enumerate(anc):
        f.edge((x, 82), (PY[0], PY[1] - 24), cls=f.step(0.6, draw=True))
    a = f.step(0.2)
    for x, n, note in anc:
        f.node(x, 60, n, note, 'plain', a, None, None, w=156, h=44)
    # descendants edges
    lang = [(70, 'Ruby', '1995'), (190, 'Julia', '2012'), (310, 'Mojo', '2023')]
    for x, n, y in lang:
        f.edge((PY[0], PY[1] + 24), (x, 238), cls=f.step(1.5, draw=True))
    NP = (540, 260)
    f.edge((PY[0], PY[1] + 24), (NP[0], NP[1] - 22), cls=f.step(1.5, draw=True), col=V)
    eco = [(390, 'pandas'), (505, 'scikit-learn'), (620, 'PyTorch')]
    for x, n in eco:
        f.edge((NP[0], NP[1] + 22), (x, 334), cls=f.step(2.3, draw=True), col=V)
    f.node(*PY, 'Python · 1991', 'Guido van Rossum', 'brand', f.step(1.0), None, None, w=180, h=48)
    s = f.step(1.3)
    f.pill(16, 148, '2008 · Python 3 breaks with 2', 'violet', s, w=200)
    f.pill(464, 148, '2024 · 3.13 free-threaded, no GIL', 'violet', s, CC + 'thread-process-gil/index.html', w=210)
    f.add(f'<g class="{f.step(1.6)}">' + text(16, 300, 'LANGUAGES IT SHAPED', 'sv-hv', B, 'start')
          + text(664, 224, 'ECOSYSTEM IT GREW', 'sv-hv', V, 'end') + '</g>')
    d = f.step(1.9)
    for x, n, y in lang:
        f.node(x, 260, n, y, 'plain', d, None, None, w=104, h=44)
    f.node(*NP, 'NumPy · 2006', 'fast arrays in C', 'violet', d, None, None, w=150, h=44)
    e = f.step(2.7)
    for x, n in eco:
        f.node(x, 356, n, 'ML shelf', 'violet', e, ML, None, w=106, h=44)
    f.h = 384
    return f.svg()

SECTIONS = '''<section id="pyov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>What Python is</h2></div>
  <p class="key">Python is <em>names pointing at objects</em>, a few built-in shapes to hold them, and a runtime that shares one interpreter. These ten pictures are the whole shelf.</p>
<figure class="gist">
{g1}
</figure>
  <ul class="why">
    <li>The core band explains nearly every surprising bug: a shared list, a dict key that will not hash, an exception caught three frames up.</li>
    <li>The run-time band is what interviews probe after the core: why threads do not speed up CPU work, when to reach for asyncio.</li>
  </ul>
</section>

<section id="pyov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Life of a line</h2></div>
  <p class="key">Every line is <em>compiled to bytecode, run by a C loop, and leaves objects on the heap</em> — that is what “interpreted, dynamically typed, garbage-collected” means.</p>
<figure class="gist">
{g2}
</figure>
  <ul class="why">
    <li><b>Interpreted:</b> CPython — the <code>python3</code> you run — never turns your code into machine code, so a plain loop is slow; push hot loops into C libraries, see <a href="../../08-performance/performance-profiling/index.html">Performance &amp; profiling</a>.</li>
    <li><b>Dynamically typed:</b> the type lives on the object and is checked only when <code>BINARY_OP</code> runs; type hints document intent but are not enforced — see <a href="../../07-typing/typing-dataclass/index.html">Type hints &amp; dataclass</a>.</li>
    <li><b>Garbage-collected:</b> an object no name points to is freed — see <a href="../../02-language-core/memory-management-gc/index.html">Memory management &amp; GC</a>.</li>
  </ul>
</section>

<section id="pyov-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Lineage</h2></div>
  <p class="key">Python took <em>readability from ABC and power from C</em>, then won through the libraries built on top of it.</p>
<figure class="gist">
{g3}
</figure>
  <ul class="why">
    <li>The 2008 break to Python 3 (text is Unicode, <code>print</code> is a function) took a decade to finish; all code you meet now is Python 3.</li>
    <li>NumPy is why ML speaks Python: the language orchestrates, C and CUDA do the arithmetic — the road continues in the <a href="../../../07-machine-learning/01-overview/ml-overview/index.html">Machine learning shelf</a>.</li>
  </ul>
</section>

'''

if __name__ == '__main__':
    s = open(PAGE, encoding='utf-8').read()
    a = s.index('<section id="pyov-s1"')
    b = s.index('<section id="pyov-s4"')
    s = s[:a] + SECTIONS.format(g1=fig_gallery(), g2=fig_line(), g3=fig_tree()) + s[b:]
    blurb = ('What Python is in ten pictures, the life of one line from source to bytecode to objects, '
             'the family tree from ABC to PyTorch, and the order to learn this shelf.')
    s = re.sub(r'(id="art-pyov"[^>]*data-blurb=")[^"]*"', lambda m: m.group(1) + blurb + '"', s)
    s = re.sub(r'<p class="lede">.*?</p>', '<p class="lede">Python is <b>names pointing at objects</b>, run line by line by a C program — short, readable code on top, fast C libraries underneath. It is the language of ML and of most coding interviews.</p>', s, count=1)
    open(PAGE, 'w', encoding='utf-8').write(s)
    print('ok')
