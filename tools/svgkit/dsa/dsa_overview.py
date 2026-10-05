"""DSA overview figures (content/01-dsa/01-overview/dsa-overview).
Also holds small helpers reused by data_structures_overview.py, algorithms_overview.py and
leetcode_toolkit.py: cells, rings, the code box with the sliding bar, and route() — a decision
flow that lights the path from a problem's wording to the structure / algorithm / tool.
Run: python3 tools/svgkit/dsa/dsa_overview.py  -> /tmp/dsa/dsa-overview.json"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *

PT, MID, TG, GH, ONF = 'var(--brand)', 'var(--violet)', 'var(--filled)', 'var(--ghost)', 'var(--on-fill)'
def vt(a): return 'rgba(var(--violet-a),%s)' % a
def it(a): return 'rgba(var(--blue-a),%s)' % a
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

LH = 20
class Code2:
    """Code box; one violet bar slides line to line (same look as binary_search.py)."""
    def __init__(s, x, y, lines, w=None):
        s.x, s.y, s.lines = x, y, lines
        s.w = w or max(200, 30 + max(len(l) for l in lines) * 6.7)
    def svg(s):
        o = R(s.x, s.y, s.w, len(s.lines) * LH + 14, 'var(--bg)', RULE_HI, 8)
        for i, l in enumerate(s.lines):
            n = len(l) - len(l.lstrip())
            o += T(s.x + 14, s.y + 22 + i * LH, esc(l).replace('  ', '&#160;&#160;'), TX, 'start', mono=True)
        return o
    def bar(s): return R(s.x + 4, s.y + 8, s.w - 8, LH, vt('.13'), 'none', 4) + R(s.x + 4, s.y + 8, 3, LH, MID, 'none', 1.5)
    def h(s): return len(s.lines) * LH + 14
    def track(s, f, pts, first=0.0):
        """pts = [(t, line)] ; bar starts on pts[0] line."""
        l0 = pts[0][1]
        f.path(s.bar(), [(0, 0, l0 * LH)] + [(t, 0, l * LH) for t, l in pts[1:]], pts[0][0], d=.35)

def box(x, y, w, h, s, c=TX, fill='var(--bg)', stroke=RULE_HI, rx=6, a='middle', mono=True, bold=True, sw=1.2, cls='sv-d'):
    tx = x + w / 2 if a == 'middle' else x + 12
    return R(x, y, w, h, fill, stroke, rx, sw) + T(tx, y + h / 2 + 4, esc(s), c, a, cls=cls, mono=mono, bold=bold)
def dead(x, y, w, h, s, rx=6, a='middle', mono=True):
    return box(x, y, w, h, s, GH, 'var(--sunk)', 'var(--rule)', rx, a, mono, False, 1)
def solid(x, y, w, h, s, rx=6, a='middle', mono=True):
    return box(x, y, w, h, s, ONF, TG, TG, rx, a, mono, True)
def ring(x, y, w, h, rx=6):
    return R(x - 3, y - 3, w + 6, h + 6, vt('.10'), MID, rx + 2, 2.2)
def goal(x, y, w, h, rx=6):
    return R(x - 4, y - 4, w + 8, h + 8, 'none', TG, rx + 2, 1.4, '4 3')
def chip(x, y, s):
    w = 24 + len(s) * 6.8
    return R(x, y, w, 24, it('.12'), TG, 12, 1.3) + T(x + 12, y + 16, esc(s), TG, 'start', mono=True, bold=True)
def say(x, y, s, c=TX, bold=False, a='start', mono=True):
    return T(x, y, esc(s), c, a, mono=mono, bold=bold)
def ptr(x, y, s, c=PT, ln=14):
    """pointer under a cell whose bottom edge is y: arrow up + label"""
    return arrow(x, y + ln, x, y + 2, c, 1.6, None, 6) + T(x, y + ln + 13, s, c, mono=True, bold=True)


def route(pre, caption, aria, ltitle, rtitle, signals, targets, cases, summary, W=760, lw=320, rw=220, rh=30, gap=8, dt=3.4):
    """Decision flow. signals: [(text, target index)]; targets: [name]; cases: [(problem, signal index, verdict)].
    Each case: the problem shows → its signal row is ringed → a violet arrow runs to the target → the
    target turns solid and stays. The thin grey lines are the fixed lookup the reader learns."""
    f = Anim(pre, W, 0, aria, caption, 3.2)
    RX = W - rw - 2
    PY, HY, Y0 = 44, 80, 92
    f.static(cap(0, HY, ltitle) + cap(RX, HY, rtitle))
    sy = [Y0 + i * (rh + gap) for i in range(len(signals))]
    ty = []
    for k in range(len(targets)):
        ys = [sy[i] for i, (_, t) in enumerate(signals) if t == k]
        ty.append(sum(ys) / len(ys))
    links = ''
    for i, (s, k) in enumerate(signals):
        links += L(lw, sy[i] + rh / 2, RX, ty[k] + rh / 2, 'var(--rule-hi)', 1)
    f.show(links, .3 + len(signals) * .04)
    for i, (s, k) in enumerate(signals):
        f.show(box(0, sy[i], lw, rh, s, TX, a='start', mono=False, bold=False, cls='sv-s'), .2 + i * .04)
    for k, nm in enumerate(targets):
        f.show(box(RX, ty[k], rw, rh, nm, TX), .4 + k * .05)
    t = 1.6
    BY = sy[-1] + rh + 30
    for c, (prob, si, verdict) in enumerate(cases):
        k = signals[si][1]; end = t + dt - .3 if c < len(cases) - 1 else None
        f.show(T(0, PY, 'problem', MU, 'start', cls='sv-hv') + T(70, PY, esc(prob), TX, 'start', cls='sv-s', bold=True), t, hide=end)
        f.show(ring(0, sy[si], lw, rh), t + .8, hide=end)
        f.show(arrow(lw + 4, sy[si] + rh / 2, RX - 6, ty[k] + rh / 2, MID, 2, None, 8), t + 1.4, hide=end)
        f.show(say(0, BY, verdict, MID), t + 1.4, hide=end)
        f.show(solid(RX, ty[k], rw, rh, targets[k]), t + 2.0)
        t += dt
    f.show(T(0, BY + 24, esc(summary), TG, 'start', bold=True), t - dt + 2.6)
    f.h = BY + 36
    return f.render()


def main():
    figs = {}
    # ---- 1. Two Sum: the steps (code) run on the storage (hash map)
    a = [2, 7, 11, 15]
    lines = ['seen = {}', 'for i, x in enumerate(a):', '    if 9 - x in seen: return seen[9 - x], i', '    seen[x] = i']
    code = Code2(0, 46, lines)
    X0 = code.w + 40; CW, G, CY = 52, 8, 64
    cx = lambda i: X0 + i * (CW + G) + CW / 2; cxl = lambda i: X0 + i * (CW + G)
    W = 760
    f = Anim('dov-m1-', W, 0, 'Two Sum with target 9 on 2 7 11 15. The code box is the algorithm, the seen map below the array is the data structure. i = 0: 9 - 2 = 7 is not in seen, store 2 at index 0. i = 1: 9 - 7 = 2 is in seen at index 0, so the answer is indices 0 and 1 after one pass.',
             'TWO SUM · THE STEPS (ALGORITHM) RUN ON THE STORAGE (DATA STRUCTURE)', 3.2)
    f.static(cap(0, 38, 'ALGORITHM — the steps') + code.svg())
    for i, v in enumerate(a):
        f.show(box(cxl(i), CY, CW, 36, v) + T(cx(i), CY + 52, str(i), FA, cls='sv-s', mono=True), .2 + i * .06)
    f.show(chip(X0 + 4 * (CW + G) + 10, CY + 6, 'target = 9'), .8)
    MY = CY + 116
    f.static(cap(X0, MY - 8, 'DATA STRUCTURE — the storage'))
    f.show(R(X0, MY, 250, 44, 'var(--bg)', RULE_HI, 8) + T(X0 + 12, MY + 27, 'seen = {', MU, 'start', mono=True) + T(X0 + 238, MY + 27, '}', MU, 'end', mono=True), 1.6)
    SY = MY + 74
    bar = [(1.6, 0)]
    t = 2.6
    # i = 0
    bar += [(t, 1)]; f.path(ptr(cx(0), CY + 58, 'i'), [(0, 0, 0), (t + 4.2, CW + G, 0)], t, d=.6)
    f.show(say(X0, SY, 'i = 0 · x = a[0] = 2', PT), t, hide=t + 3.9)
    bar += [(t + 1.0, 2)]
    f.show(ring(cxl(0), CY, CW, 36), t + 1.0, hide=t + 3.9)
    f.show(say(X0, SY + 22, '9 − 2 = 7 not in seen'), t + 1.0, hide=t + 3.9)
    bar += [(t + 2.2, 3)]
    f.show(box(X0 + 80, MY + 10, 64, 24, '2 → 0', PT, it('.08'), PT, 12), t + 2.6)
    f.show(say(X0, SY + 44, 'store seen[2] = 0', PT, True), t + 2.6, hide=t + 3.9)
    t += 4.2
    bar += [(t, 1)]
    f.show(say(X0, SY, 'i = 1 · x = a[1] = 7', PT), t)
    bar += [(t + 1.0, 2)]
    f.show(ring(cxl(1), CY, CW, 36) + ring(X0 + 80, MY + 10, 64, 24, 10), t + 1.0, hide=t + 2.6)
    f.show(say(X0, SY + 22, '9 − 7 = 2 is in seen → index 0'), t + 1.0)
    code.track(f, bar)
    end = t + 2.6
    for i in (0, 1): f.show(solid(cxl(i), CY, CW, 36, a[i]), end)
    f.show(T((cx(0) + cx(1)) / 2, CY - 10, '✓ found', TG, mono=True, bold=True), end + .2)
    f.show(T(X0, SY + 46, 'answer (0, 1) · one pass, no pair-by-pair check', TG, 'start', bold=True), end + .4)
    f.h = SY + 58
    figs['m1'] = f.render()

    # ---- 2. Same task, two methods: scan vs halve
    v = [2, 5, 8, 12, 16, 23, 31, 38, 40, 47, 52, 60, 65, 71, 80, 92]; tgt = 12
    CW, G, X0 = 34, 4, 130; W = 760
    cxl = lambda i: X0 + i * (CW + G); cx = lambda i: cxl(i) + CW / 2
    f = Anim('dov-m2-', W, 0, 'Find 65 in 16 sorted numbers two ways. Reading front to back the pointer looks at 13 cells. Opening the middle and dropping half looks at 4 cells. For a million entries the counts become 1,000,000 and 20.',
             'FIND 65 · SAME LIST, TWO METHODS', 3.2)
    R1, R2 = 44, 150
    f.static(T(0, R1 + 22, 'read front to back', MU, 'start', cls='sv-s') + T(0, R2 + 22, 'open the middle,', MU, 'start', cls='sv-s') + T(0, R2 + 38, 'drop half', MU, 'start', cls='sv-s'))
    for row, y in ((0, R1), (1, R2)):
        for i, x in enumerate(v):
            f.show(box(cxl(i), y, CW, 32, x, cls='sv-d'), .2 + i * .03 + row * .2)
        f.show(goal(cxl(tgt), y, CW, 32), 1.2)
    # row 1: linear
    t = 2.0; st = .32
    f.path(ptr(cx(0), R1 + 32, 'i', PT, 12), [(0, 0, 0)] + [(t + k * st, k * (CW + G), 0) for k in range(1, tgt + 1)], t, d=.2)
    for k in range(tgt):
        f.show(dead(cxl(k), R1, CW, 32, v[k]), t + k * st + .25)
    for k in range(tgt + 1):
        f.show(say(X0 + 0, R1 + 70, 'looks: %d' % (k + 1), PT, True), t + k * st, hide=t + (k + 1) * st if k < tgt else None, d=.1)
    t1 = t + tgt * st + .4
    f.show(solid(cxl(tgt), R1, CW, 32, v[tgt]), t1)
    f.show(say(X0 + 100, R1 + 70, '✓ found after 13 looks', TG, True), t1 + .2)
    # row 2: halving
    t = t1 + 1.2; l, r = 0, len(v) - 1; looks = 0; mpos = []; m0 = None
    while True:
        m = (l + r) // 2; looks += 1; m0 = m if m0 is None else m0
        mpos.append((t, (m - m0) * (CW + G), 0))
        f.show(ring(cxl(m), R2, CW, 32, 5), t, hide=t + 1.5)
        if v[m] == 65: break
        f.show(say(X0 + 160, R2 + 70, '%d %s 65 → drop the %s half' % (v[m], '<' if v[m] < 65 else '>', 'left' if v[m] < 65 else 'right'), TX), t + .4, hide=t + 1.5)
        drop = range(l, m + 1) if v[m] < 65 else range(m, r + 1)
        for i in drop: f.show(dead(cxl(i), R2, CW, 32, v[i]), t + .9)
        if v[m] < 65: l = m + 1
        else: r = m - 1
        f.show(say(X0, R2 + 70, 'looks: %d' % looks, PT, True), t, hide=t + 1.6, d=.1)
        t += 1.6
    f.show(say(X0, R2 + 70, 'looks: %d' % looks, PT, True), t, d=.1)
    f.path(T(cx(m0), R2 - 8, 'mid', MID, mono=True, bold=True), mpos, mpos[0][0], d=.5)
    f.show(solid(cxl(tgt), R2, CW, 32, v[tgt]), t + .4)
    f.show(say(X0 + 100, R2 + 70, '✓ found after 4 looks', TG, True), t + .6)
    # scale up
    t += 1.6; BY = R2 + 104
    f.show(T(0, BY, 'n = 1,000,000', MU, 'start', cls='sv-s', bold=True), t)
    f.show(R(X0, BY - 14, 600, 16, it('.16'), TG, 3, 1) + say(X0 + 594, BY - 2, '1,000,000 looks', TG, True, 'end'), t + .4)
    f.show(R(X0, BY + 10, 4, 16, MID, MID, 1, 1) + say(X0 + 12, BY + 23, '20 looks — same machine, better method; needs the list sorted', MID, True), t + 1.0)
    f.h = BY + 36
    figs['m2'] = f.render()

    # ---- 3. Learning order: six stages, one new idea each
    st = [('Big-O', 'read n, know which speed is allowed'),
          ('Array & string → hash map', 'store data; trade memory for speed'),
          ('Two pointers → window → binary search', 'the three cheapest ways to scan'),
          ('Stack · heap · tree & BST', 'store for order; trees bring recursion'),
          ('Graph → backtracking', 'walk over every possible situation'),
          ('Dynamic programming', 'recursion + memory, the hardest group')]
    W = 760; BX, BW, BH, GP = 60, 280, 34, 12
    f = Anim('dov-m3-', W, 0, 'Six stages in a column. A you-are-here pointer walks down them; at each stage a line on the right names the one new idea it adds. The last stage, dynamic programming, turns solid: ready.',
             'LEARNING ORDER · EACH STAGE ADDS ONE IDEA', 3.2)
    Y0 = 40; ys = [Y0 + i * (BH + GP) for i in range(len(st))]
    for i, (nm, _) in enumerate(st):
        f.show(box(BX, ys[i], BW, BH, '%d · %s' % (i + 1, nm), TX, a='start', mono=False, bold=True, cls='sv-s'), .2 + i * .08)
        if i: f.show(arrow(BX + 24, ys[i - 1] + BH + 1, BX + 24, ys[i] - 1, RULE_HI, 1.2, None, 5), .3 + i * .08)
    t = 1.4; dtt = 1.3
    you = arrow(0, ys[0] + BH / 2, BX - 8, ys[0] + BH / 2, PT, 1.8, None, 7) + T(0, ys[0] + BH / 2 - 7, 'you', PT, 'start', mono=True, bold=True)
    f.path(you, [(0, 0, 0)] + [(t + i * dtt, 0, ys[i] - ys[0]) for i in range(1, len(st))], t, d=.5)
    for i, (nm, idea) in enumerate(st):
        ti = t + i * dtt
        last = i == len(st) - 1
        f.show(ring(BX, ys[i], BW, BH), ti + .3, hide=None if last else ti + dtt)
        f.show(say(BX + BW + 20, ys[i] + BH / 2 + 4, '+ ' + idea, MID if not last else TG, last, mono=False), ti + .4)
    end = t + (len(st) - 1) * dtt + 1.2
    f.show(solid(BX, ys[-1], BW, BH, '6 · Dynamic programming', a='start', mono=False), end)
    f.show(T(BX, ys[-1] + BH + 30, '✓ six stages · each one adds a single new idea to the last', TG, 'start', bold=True), end + .3)
    f.h = ys[-1] + BH + 50
    figs['m3'] = f.render()
    return figs


_BS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../content/01-dsa/04-algorithms/binary-search/index.html'), encoding='utf-8').read()
REPLAY = _BS[_BS.index('<script>\n/* Figures start'):_BS.index('</script>', _BS.index('<script>\n/* Figures start')) + 9]

def splice(page, article):
    """Replace the whole <article ...>...</article> of page with article."""
    h = open(page, encoding='utf-8').read()
    a = h.index('<article'); b = h.index('</article>') + len('</article>')
    h = h[:a] + article + h[b:]
    h = h.replace('  <script src="lab.js"></script>\n', '').replace('<script src="lab.js"></script>\n', '')
    open(page, 'w', encoding='utf-8').write(h)

def sub(slug, n, m, title, skey, fig, extra=''):
    return ('  <div class="subsec" id="%s-s%d-%d">\n    <h3 class="ssh"><b>%d.%d</b>%s</h3>\n    <p class="skey">%s</p>\n%s\n%s  </div>\n'
            % (slug, n, m, n, m, title, skey, fig, extra))


if __name__ == '__main__':
    os.makedirs('/tmp/dsa', exist_ok=True)
    figs = main()
    json.dump(figs, open('/tmp/dsa/dsa-overview.json', 'w'))
    page = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../content/01-dsa/01-overview/dsa-overview/index.html')
    art = '''<article class="doc" id="art-dsaov" data-title="DSA overview" data-tag="Overview" data-blurb="What DSA is, its two halves, and the order to learn it in.">
        <header class="hero">
  <p class="eyebrow">DSA · first lesson of the shelf</p>
  <h1>DSA — <em>the map</em></h1>
  <p class="lede">What the subject is, what it contains, where to start.</p>
</header>

<section id="dsaov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Two halves: <em>algorithms</em> (the steps) run on <em>data structures</em> (the storage).</p>
  <div class="subsec" id="dsaov-s1-1">
    <h3 class="ssh"><b>1.1</b>Steps and storage</h3>
    <p class="skey">Choose the storage, and the steps almost write themselves.</p>
%s
  </div>
</section>

<section id="dsaov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>What DSA is</h2></div>
  <p class="key">Same answer, very different speed — <em>DSA is the study of doing it fast</em>.</p>
  <div class="subsec" id="dsaov-s2-1">
    <h3 class="ssh"><b>2.1</b>Method beats machine</h3>
    <p class="skey">Sort once, then <em>open the middle and drop half</em> instead of reading every entry.</p>
%s
  </div>
</section>

<section id="dsaov-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Learning order</h2></div>
  <p class="key">Follow this order and each lesson <em>adds just one new idea</em>.</p>
  <div class="subsec" id="dsaov-s3-1">
    <h3 class="ssh"><b>3.1</b>Six stages</h3>
    <p class="skey">Big-O first, dynamic programming last.</p>
%s
  <div class="stack">
    <div class="s"><b>1 · <a href="../../02-foundations/big-o-complexity/index.html">Big-O</a></b><span>Read the data size, know which approach is allowed.</span></div>
    <div class="s"><b>2 · <a href="../../03-data-structures/array-string/index.html">Array &amp; string</a> → <a href="../../03-data-structures/hash-map/index.html">hash map</a></b><span>The two storage choices behind most problems.</span></div>
    <div class="s"><b>3 · <a href="../../04-algorithms/two-pointers/index.html">Two pointers</a> → <a href="../../04-algorithms/sliding-window/index.html">sliding window</a> → <a href="../../04-algorithms/binary-search/index.html">binary search</a></b><span>The three cheapest ways to scan.</span></div>
    <div class="s"><b>4 · <a href="../../03-data-structures/stack-monotonic-queue/index.html">Stack</a> · <a href="../../03-data-structures/heap-priority-queue/index.html">heap</a> · <a href="../../03-data-structures/tree-bst-traversal/index.html">tree &amp; BST</a></b><span>Storage for order; trees open the door to recursion.</span></div>
    <div class="s"><b>5 · <a href="../../04-algorithms/graph-bfs-dfs-topo/index.html">Graph</a> → <a href="../../04-algorithms/backtracking/index.html">backtracking</a></b><span>Walk over every situation that can occur.</span></div>
    <div class="s ok"><b>6 · <a href="../../04-algorithms/dynamic-programming/index.html">Dynamic programming</a></b><span>Last, because it builds on recursion.</span></div>
  </div>
  <p class="stripnote"><span>alongside every stage: <a href="../../05-toolkit/leetcode-toolkit/index.html">LeetCode toolkit</a></span><span>about <em>200–300 good problems</em> is enough</span></p>
  </div>
</section>

%s
<footer>DSA · overview · next: <a href="../../02-foundations/big-o-complexity/index.html">Big-O</a>.</footer>

      </article>''' % (figs['m1'], figs['m2'], figs['m3'], REPLAY.strip())
    splice(page, art)
    print('ok', {k: len(v) for k, v in figs.items()})
