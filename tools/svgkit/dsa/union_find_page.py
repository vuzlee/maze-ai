"""Rebuild content/01-dsa/03-data-structures/union-find/index.html from /tmp/dsa/union-find.json.
Run union_find.py first. LeetCode lists come verbatim from the pristine copy /tmp/dsa/orig-union-find.html."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from treekit_page import build, probs_of

ROOT = '/home/vuzle/Documents/mazeai/'
PAGE = ROOT + 'content/01-dsa/03-data-structures/union-find/index.html'
P = probs_of(open('/tmp/dsa/orig-union-find.html').read())
assert len(P) == 5

art = '<article class="doc" id="art-dsu" data-title="Union-Find (DSU)" data-tag="Data structure" data-blurb="Groups as trees: same root means same group, and two tricks keep every query almost O(1).">'
hero = '''        <header class="hero">
  <p class="eyebrow">DSA · data structures</p>
  <h1>Union-Find<br><em>(DSU)</em></h1>
  <p class="lede">"Are these two in the same group?" — answered almost instantly while groups keep merging.</p>
</header>'''
S = [
    ('Mental model', 'Each group is a tree; <em>same root means same group</em>.', [
        ('Groups as trees', 'Every element points at a parent; <em>the root points at itself</em>.', 'm1', None, None),
    ]),
    ('Properties', 'Two operations, <code>find</code> and <code>union</code>; <em>their cost is the height of the tree</em>.', [
        ('Find', 'Climb the arrows <em>until a node points at itself</em>.', 'p1', None, None),
        ('Union', 'Find both roots, <em>hang one under the other</em>.', 'p2', None, None),
        ('Path compression', 'After a find, <em>every node passed points straight at the root</em>.', 'p3', None, None),
        ('Union by size', 'The <em>small tree goes under the big one</em>, so trees stay short.', 'p4', None, None),
        ('Cost', 'With both tricks, <em>almost O(1)</em> per operation.', 'p5', None, None),
    ]),
    ('Patterns', 'Turn the problem into <em>"join these two" and "are these together?"</em>.', [
        ('Counting groups', 'Start at n; <em>each successful union removes one</em>.', 'q1',
         '"number of friend circles" · "number of islands" · "how many clusters"', P[0]),
        ('Redundant edge', 'A union that <em>returns False</em> closes a cycle.', 'q2',
         '"remove one edge to make a tree" · "which edge creates a cycle"', P[1]),
        ('Minimum spanning tree', 'Cheapest edge first; <em>skip it if the union fails</em> (Kruskal).', 'q3',
         '"connect all points at minimum cost"', P[2]),
        ('Merging by key', 'Map each key to a number <em>with a dict</em>, then union.', 'q4',
         'merging accounts · merging consecutive runs · elements that are not 0…n-1', P[3]),
        ('Two opposite sides', 'Give each x a twin <em>x′ = the other side</em>.', 'q5',
         '<b>adversarial</b> relations — "these two must be in different groups"', P[4]),
    ]),
]
build(PAGE, '/tmp/dsa/union-find.json', art, hero, 'dsu', S, 'DSA · union-find.')
print('written', PAGE)
