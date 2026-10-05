"""Data structures overview figures (content/01-dsa/03-data-structures/data-structures-overview).
Run: python3 tools/svgkit/dsa/data_structures_overview.py -> /tmp/dsa/data-structures-overview.json + page"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsa_overview import *

def main():
    figs = {}
    # ---- 1. Same data, two questions, two structures
    a = [9, 14, 27, 4, 23, 30, 16, 5]
    W = 760; CW, G = 44, 6; AX = 120; AY = 70
    cxl = lambda i: AX + i * (CW + G); cx = lambda i: cxl(i) + CW / 2
    f = Anim('dso-m1-', W, 0, 'Eight numbers stored twice: as an array and as a hash map with four buckets keyed by value mod 4. Question 1, get the item at index 5: the array jumps straight to it, one look; the hash map has no positions. Question 2, is 23 in here: the array scans 5 cells; the hash map computes 23 mod 4 = 3 and looks only in bucket 3. Each structure is cheap at a different question.',
             'SAME 8 NUMBERS, TWO WAYS TO STORE THEM', 3.2)
    f.static(T(0, AY + 22, 'array', MU, 'start', cls='sv-s', bold=True))
    for i, v in enumerate(a):
        f.show(box(cxl(i), AY, CW, 34, v) + T(cx(i), AY + 50, str(i), FA, cls='sv-s', mono=True), .2 + i * .04)
    HY = AY + 108; BW = 92; BG = 10
    f.static(T(0, HY + 22, 'hash map', MU, 'start', cls='sv-s', bold=True) + T(0, HY + 38, 'key = x mod 4', FA, 'start', cls='sv-s'))
    buckets = {k: [x for x in a if x % 4 == k] for k in range(4)}
    bx = lambda k: AX + k * (BW + 2 * BG + 10)
    for k in range(4):
        f.show(R(bx(k), HY, BW + 2 * BG, 34, 'var(--bg)', RULE_HI, 6, 1.2) + T(bx(k) + (BW + 2 * BG) / 2, HY + 50, 'bucket %d' % k, FA, cls='sv-s', mono=True), .6 + k * .05)
        for j, x in enumerate(buckets[k]):
            f.show(box(bx(k) + 6 + j * 36, HY + 5, 32, 24, x, cls='sv-d'), .8 + k * .05)
    SY = HY + 86
    # Q1: index 5
    t = 1.8
    f.show(chip(AX, 30, 'get a[5]'), t, hide=t + 4.6)
    f.show(say(0, SY, 'array: address = start + 5 → jump', PT), t + .6, hide=t + 4.6)
    f.path(ptr(cx(5), AY + 56, 'i', PT, 12), [(0, 0, 0)], t + .6, hide=t + 4.4)
    f.show(ring(cxl(5), AY, CW, 34), t + 1.0, hide=t + 4.4)
    f.show(say(0, SY + 22, 'hash map: no positions → cannot answer', GH), t + 1.8, hide=t + 4.6)
    f.show(say(0, SY + 44, 'array 1 look · hash map —', TG, True), t + 2.8, hide=t + 4.6)
    t += 5.0
    # Q2: is 23 here
    f.show(chip(AX, 30, 'is 23 here?'), t)
    f.show(say(0, SY, 'array: no position given → scan from i = 0', PT), t + .4)
    pts = [(0, 0, 0)] + [(t + .6 + k * .4, k * (CW + G), 0) for k in range(1, 5)]
    f.path(ptr(cx(0), AY + 56, 'i', PT, 12), pts, t + .4, d=.25, hide=t + 3.4)
    for k in range(4): f.show(dead(cxl(k), AY, CW, 34, a[k]), t + .6 + (k + 1) * .4)
    f.show(ring(cxl(4), AY, CW, 34), t + .6 + 4 * .4 + .3, hide=t + 3.4)
    t2 = t + 3.4
    f.show(solid(cxl(4), AY, CW, 34, 23), t2)
    f.show(say(0, SY + 22, 'hash map: 23 mod 4 = 3 → look only in bucket 3', MID), t2 + .4)
    for k in range(3):
        f.show(R(bx(k) + 1, HY + 1, BW + 2 * BG - 2, 32, 'var(--sunk)', 'none', 5) + ''.join(box(bx(k) + 6 + j * 36, HY + 5, 32, 24, x, GH, 'var(--sunk)', 'var(--rule)', 6, sw=1, bold=False) for j, x in enumerate(buckets[k])), t2 + .9)
    f.show(ring(bx(3), HY, BW + 2 * BG, 34), t2 + .9, hide=t2 + 2.0)
    j = buckets[3].index(23)
    f.show(solid(bx(3) + 6 + j * 36, HY + 5, 32, 24, 23), t2 + 2.0)
    f.show(T(bx(3) + (BW + 2 * BG) / 2, HY - 8, '✓ found', TG, mono=True, bold=True) + T(cx(4), AY - 8, '✓ found', TG, mono=True, bold=True), t2 + 2.2)
    f.show(say(0, SY + 44, 'array 5 looks · hash map 1 look — no structure wins every question', TG, True), t2 + 2.6)
    f.h = SY + 56
    figs['m1'] = f.render()

    # ---- 2. Choosing a structure: signal -> structure
    sig = [('you know the position, scan in order', 0), ('look up by key, count, "seen before?"', 1),
           ('splice items in and out a lot', 2), ('last-in first-out, or first-in first-out', 3),
           ('always need the smallest / largest', 4), ('keep order, ask for a range', 5),
           ('match a word prefix, autocomplete', 6), ('only need "same group?"', 7)]
    tg = ['Array', 'Hash map', 'Linked list', 'Stack / queue', 'Heap', 'Balanced BST', 'Trie', 'Union-Find']
    cases = [('Group Anagrams — bucket words by sorted letters', 1, 'look up by key → hash map, O(1) per word'),
             ('Kth Largest Element in a Stream', 4, 'always the smallest of the top k → heap, O(log k)'),
             ('Implement autocomplete for a search box', 6, 'match a word prefix → trie, O(L) per word')]
    figs['m2'] = route('dso-c1-', 'CHOOSING A STRUCTURE · READ THE PROBLEM, FOLLOW THE LINE',
                       'Eight problem signals on the left, each joined to one structure on the right. Three problems play in turn: Group Anagrams lights look up by key and the hash map; Kth Largest in a Stream lights always need the smallest and the heap; autocomplete lights match a word prefix and the trie. The chosen structures stay solid.',
                       'SIGNAL IN THE PROBLEM', 'STRUCTURE', sig, tg, cases,
                       'the innermost loop asks one question most often — pick the structure that makes it cheap',
                       W=760, lw=330, rw=170, rh=28, gap=6)
    return figs

if __name__ == '__main__':
    figs = main()
    json.dump(figs, open('/tmp/dsa/data-structures-overview.json', 'w'))
    page = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../content/01-dsa/03-data-structures/data-structures-overview/index.html')
    M = lambda s: '<span class="mth">%s</span>' % s
    O1, On, Olog, OL = M('O(1)'), M('O(<var>n</var>)'), M('O(<b class="fn">log</b> <var>n</var>)'), M('O(<var>L</var>)')
    art = '''<article class="doc" id="art-dsov" data-title="Data structures overview" data-tag="Overview" data-blurb="Eight ways to store data and the operation each one makes cheap.">
        <header class="hero">
  <p class="eyebrow">DSA · opening the data structures group</p>
  <h1>Data structures — <em>the map</em></h1>
  <p class="lede">Eight ways to store data, side by side. Open this mid-practice to choose fast.</p>
</header>

<section id="dsov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">No storage is good at everything: <em>each one makes a different question cheap</em>.</p>
  <div class="subsec" id="dsov-s1-1">
    <h3 class="ssh"><b>1.1</b>One data set, two questions</h3>
    <p class="skey">Position questions favour the array; value questions favour the hash map.</p>
%s
  </div>
</section>

<section id="dsov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Choosing a structure</h2></div>
  <p class="key">Find the question your loop asks most, then <em>pick the structure that makes it cheap</em>.</p>
  <div class="subsec" id="dsov-s2-1">
    <h3 class="ssh"><b>2.1</b>Signal to structure</h3>
    <p class="skey">Read the problem's wording, follow its line to a structure, then check the cost below.</p>
%s
  <table>
    <tr><th>Structure</th><th>Access</th><th>Search</th><th>Insert / delete</th></tr>
    <tr><td><a href="../array-string/index.html">Array</a></td><td><b>%s</b></td><td>%s</td><td>%s middle · %s* end</td></tr>
    <tr><td><a href="../hash-map/index.html">Hash map</a></td><td>—</td><td><b>%s</b> avg</td><td><b>%s</b> avg</td></tr>
    <tr><td><a href="../linked-list/index.html">Linked list</a></td><td>%s</td><td>%s</td><td><b>%s</b> at a known node</td></tr>
    <tr><td><a href="../stack-monotonic-queue/index.html">Stack / queue</a></td><td>—</td><td>—</td><td><b>%s</b> at its end</td></tr>
    <tr><td><a href="../heap-priority-queue/index.html">Heap</a></td><td>%s top</td><td>%s</td><td>%s</td></tr>
    <tr><td><a href="../tree-bst-traversal/index.html">Balanced BST</a></td><td>%s</td><td>%s</td><td>%s</td></tr>
    <tr><td><a href="../trie/index.html">Trie</a></td><td>—</td><td><b>%s</b></td><td>%s</td></tr>
    <tr><td><a href="../union-find/index.html">Union-Find</a></td><td>—</td><td>near %s</td><td>near %s</td></tr>
  </table>
  <p class="stripnote"><span>* averaged over many appends — see <a href="../../02-foundations/big-o-complexity/index.html">Big-O</a></span><span><em>L = word length</em></span></p>
  </div>
</section>

%s
<footer>DSA · data structures · next: <a href="../array-string/index.html">Array &amp; string</a>.</footer>

      </article>''' % (figs['m1'], figs['m2'], O1, On, On, O1, O1, O1, On, On, O1, O1, O1, On, Olog, Olog, Olog, Olog, OL, OL, O1, O1, REPLAY.strip())
    splice(page, art)
    print('ok', {k: len(v) for k, v in figs.items()})
