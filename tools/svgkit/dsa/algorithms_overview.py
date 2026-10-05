"""Algorithms overview figures (content/01-dsa/04-algorithms/algorithms-overview).
Run: python3 tools/svgkit/dsa/algorithms_overview.py -> /tmp/dsa/algorithms-overview.json + page"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsa_overview import *

SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
def sup(k): return str(k).translate(SUP)

def budget(pre, caption, aria, cases, W=760):
    """Rows = complexity classes, fastest-growing first. For each case n: every row shows its op count,
    rows above 10^8 turn grey, the first row that fits turns solid with its usual approach."""
    rows = [('O(2ⁿ)', lambda n: 2 ** n, 'backtracking, bitmask DP'),
            ('O(n³)', lambda n: n ** 3, '3D DP, Floyd-Warshall'),
            ('O(n²)', lambda n: n ** 2, 'DP over two strings'),
            ('O(n log n)', lambda n: n * math.log2(n), 'sorting, binary search, heap'),
            ('O(n)', lambda n: n, 'two pointers, window, prefix sum')]
    f = Anim(pre, W, 0, aria, caption, 3.2)
    LIM = 1e8; RX, RW, RH, GP, Y0 = 0, 120, 30, 8, 92
    BX, BW = 140, 280  # bar region (log scale 0 .. 10^12)
    ys = [Y0 + i * (RH + GP) for i in range(len(rows))]
    lx = lambda v: BX + min(1, math.log10(max(v, 1)) / 12) * BW
    f.static(cap(0, Y0 - 12, 'COST') + cap(BX, Y0 - 12, 'OPERATIONS (LOG SCALE)') + cap(BX + BW + 84, Y0 - 12, 'USUAL APPROACH'))
    for i, (nm, _, ap) in enumerate(rows):
        f.show(box(RX, ys[i], RW, RH, nm), .2 + i * .06)
        f.show(R(BX, ys[i], BW, RH, 'var(--bg)', RULE_HI, 4, 1), .3 + i * .06)
    yb = ys[-1] + RH
    f.show(L(lx(LIM), Y0 - 6, lx(LIM), yb + 6, MID, 1.6, '4 3') + T(lx(LIM), yb + 20, '10⁸ ≈ 1 second', MID, mono=True, bold=True), .9)
    t = 1.8; SY = yb + 52; dt = 5.0
    for c, n in enumerate(cases):
        last = c == len(cases) - 1; end = None if last else t + dt - .3
        f.show(chip(0, 28, 'n = %s' % n[1]), t, hide=end)
        hit = None
        for i, (nm, fn, ap) in enumerate(rows):
            v = fn(n[0]); ti = t + .6 + i * .5
            w = lx(v) - BX
            fits = v <= LIM
            bar = R(BX, ys[i] + 6, max(w, 3), RH - 12, it('.30') if fits else 'var(--sunk)', TG if fits else RULE_HI, 3, 1)
            f.show(bar + T(BX + BW + 10, ys[i] + RH / 2 + 4, ('≈ 10' + sup(round(math.log10(max(v, 1))))) if v < 1e12 else '> 10¹²', TX if fits else GH, 'start', mono=True), ti, hide=end)
            if not fits:
                f.show(dead(RX, ys[i], RW, RH, nm), ti + .2, hide=end)
            elif hit is None:
                hit = i
                f.show(ring(RX, ys[i], RW, RH), ti + .1, hide=ti + .9)
                f.show(solid(RX, ys[i], RW, RH, nm), ti + .9, hide=end)
                f.show(say(BX + BW + 84, ys[i] + RH / 2 + 4, ap, TG, True, mono=False), ti + 1.0, hide=end)
        f.show(say(0, SY, 'n = %s → slowest that fits: %s' % (n[1], rows[hit][0]), TG if last else MID, True), t + .6 + 5 * .5 + .4, hide=end)
        t += dt
    f.h = SY + 12
    return f.render()

def main():
    figs = {}
    sig = [('sorted array, "pair / triplet"', 0), ('"longest / shortest subarray"', 0),
           ('"smallest value such that…"', 1), ('answer range up to 10⁹', 1),
           ('meetings, intervals, "most you can pick"', 2), ('"obvious once sorted"', 2),
           ('"how many ways", "min cost"', 3), ('grid, network, "all combinations"', 3)]
    tg = ['Two pointers · window', 'Binary search', 'Greedy · sorting', 'Search + memo']
    cases = [('Minimum Size Subarray Sum ≥ 7', 1, '"shortest subarray" → two pointers / sliding window'),
             ('Koko Eating Bananas — smallest speed', 2, '"smallest such that" → binary search on the answer'),
             ('Climbing Stairs — how many ways', 6, '"how many ways" → search + memo (dynamic programming)')]
    figs['m1'] = route('alo-m1-', 'FOUR PATTERN FAMILIES · THE WORDING POINTS TO ONE',
                       'Eight wordings on the left joined to four pattern families on the right. Three problems play in turn: Minimum Size Subarray Sum lights shortest subarray and two pointers; Koko lights smallest value such that and binary search; Climbing Stairs lights how many ways and search plus memo. The chosen families stay solid.',
                       'WORDING IN THE PROBLEM', 'FAMILY', sig, tg, cases,
                       'the wording gives a direction; the size of n then allows it or rules it out',
                       W=760, lw=330, rw=200, rh=28, gap=6)
    figs['c1'] = budget('alo-c1-', 'CHOOSING AN ALGORITHM · n DECIDES WHICH SPEEDS FIT IN ONE SECOND',
                        'Five cost rows from O(2^n) down to O(n), with operation bars on a log scale and a dashed line at 10^8, about one second. For n = 20 every row fits, so O(2^n) backtracking is allowed. For n = 5,000 the 2^n and n^3 rows go grey and O(n^2) is the slowest that fits. For n = 100,000 only O(n log n) and O(n) fit, and O(n log n) lights with sorting, binary search, heap.',
                        [(20, '20'), (5000, '5,000'), (100000, '10⁵')])
    return figs

if __name__ == '__main__':
    figs = main()
    json.dump(figs, open('/tmp/dsa/algorithms-overview.json', 'w'))
    page = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../content/01-dsa/04-algorithms/algorithms-overview/index.html')
    art = '''<article class="doc" id="art-alov" data-title="Algorithms overview" data-tag="Overview" data-blurb="Which wording points to which pattern, and which speeds the data size allows.">
        <header class="hero">
  <p class="eyebrow">DSA · opening the algorithms group</p>
  <h1>Algorithms — <em>the map</em></h1>
  <p class="lede">Two questions after reading a problem: <b>which pattern</b>, and <b>which speed does n allow</b>.</p>
</header>

<section id="alov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">The lessons in this group fall into <em>four pattern families</em>; the wording tells you which.</p>
  <div class="subsec" id="alov-s1-1">
    <h3 class="ssh"><b>1.1</b>Wording to pattern</h3>
    <p class="skey">Spot the phrase, follow its line to a family.</p>
%s
  </div>
</section>

<section id="alov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Choosing an algorithm</h2></div>
  <p class="key">The data size <em>rules out most speeds</em> before you start thinking.</p>
  <div class="subsec" id="alov-s2-1">
    <h3 class="ssh"><b>2.1</b>Data size to speed</h3>
    <p class="skey">About 10⁸ simple operations fit in one second; pick the slowest speed under that line.</p>
%s
  <table>
    <tr><th>Given</th><th>Allowed up to</th><th>Common approach</th></tr>
    <tr><td><span class="mth"><var>n</var> ≤ 20</span></td><td><span class="mth">O(2<sup><var>n</var></sup>)</span></td><td><a href="../backtracking/index.html">backtracking</a>, bitmask DP</td></tr>
    <tr><td><span class="mth"><var>n</var> ≤ 500</span></td><td><span class="mth">O(<var>n</var>³)</span></td><td>3D DP, Floyd-Warshall</td></tr>
    <tr><td><span class="mth"><var>n</var> ≤ 5,000</span></td><td><span class="mth">O(<var>n</var>²)</span></td><td><a href="../dynamic-programming/index.html">DP</a> over two strings</td></tr>
    <tr><td><span class="mth"><var>n</var> ≤ 10⁵</span></td><td><span class="mth">O(<var>n</var> <b class="fn">log</b> <var>n</var>)</span></td><td><a href="../sorting/index.html">sorting</a>, <a href="../binary-search/index.html">binary search</a>, heap, <a href="../graph-bfs-dfs-topo/index.html">graph</a></td></tr>
    <tr><td><span class="mth"><var>n</var> ≤ 10⁷</span></td><td><span class="mth">O(<var>n</var>)</span></td><td><a href="../two-pointers/index.html">two pointers</a>, <a href="../sliding-window/index.html">sliding window</a>, <a href="../prefix-sum/index.html">prefix sum</a></td></tr>
    <tr><td><span class="mth"><var>n</var> ≥ 10⁹</span></td><td><span class="mth">O(<b class="fn">log</b> <var>n</var>)</span></td><td>binary search on the answer, a formula</td></tr>
  </table>
  <p class="stripnote"><span>details: <a href="../../02-foundations/big-o-complexity/index.html">Big-O</a></span><span><em>n up to 10⁵ and your idea is O(n²)? not there yet</em></span></p>
  </div>
</section>

%s
<footer>DSA · algorithms · next: <a href="../two-pointers/index.html">Two pointers</a>.</footer>

      </article>''' % (figs['m1'], figs['c1'], REPLAY.strip())
    splice(page, art)
    print('ok', {k: len(v) for k, v in figs.items()})
