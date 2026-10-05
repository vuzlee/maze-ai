"""Rebuild content/01-dsa/03-data-structures/tree-bst-traversal/index.html from /tmp/dsa/tree-bst-traversal.json.
Run tree_bst_traversal.py first. Reads the LeetCode lists from the pristine copy /tmp/dsa/orig-tree-bst-traversal.html."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from treekit_page import build, probs_of

ROOT = '/home/vuzle/Documents/mazeai/'
PAGE = ROOT + 'content/01-dsa/03-data-structures/tree-bst-traversal/index.html'
P = probs_of(open('/tmp/dsa/orig-tree-bst-traversal.html').read())
assert len(P) == 5

art = '<article class="doc" id="art-tree" data-title="Tree, BST &amp; traversal" data-tag="Data structure" data-blurb="Nodes and children, four ways to walk a tree, and why a BST costs its height.">'
hero = '''        <header class="hero">
  <p class="eyebrow">DSA · data structures</p>
  <h1>Tree, BST &amp; <em>traversal</em></h1>
  <p class="lede">Nodes with children, walked in the order the question needs.</p>
</header>'''

S = [
    ('Mental model', 'A tree is nodes with children; <em>the walk order decides what you see first</em>.', [
        ('Root, children, leaves', 'One root on top, <em>at most two children</em> per node, leaves at the bottom.', 'm1', None, None),
        ('Preorder', 'Write the node <em>before</em> its children: the root comes first.', 'm2', None, None),
        ('Inorder', 'Left side, then the node, then the right side: <em>a BST comes out sorted</em>.', 'm3', None, None),
        ('Postorder', 'Write the node <em>after</em> both children: the root comes last.', 'm4', None, None),
        ('Level order', 'A queue visits the tree <em>one level at a time</em>.', 'm5', None, None),
    ]),
    ('Properties', 'In a BST every left value is smaller and every right value bigger, so <em>each operation walks one path: O(h)</em>.', [
        ('Search', 'Compare, then drop <em>a whole side</em>.', 'p1', None, None),
        ('Insert', 'Walk down like a search; the new node goes <em>where the walk falls off</em>.', 'p2', None, None),
        ('Delete', 'Two children: copy in <em>the next bigger value</em>, then delete that leaf.', 'p3', None, None),
        ('Height decides the cost', 'Balanced: <em>O(log n)</em>. A chain: <em>O(n)</em>.', 'p4', None, None),
    ]),
    ('Patterns', 'One recursive walk; <em>what you do at each node</em> is the pattern.', [
        ('Combine answers from the children', 'Return a value up; the parent <em>combines its children\'s answers</em>.', 'q1',
         'height · diameter · sum · "is the tree balanced" · return a tuple for more than one value', P[0]),
        ('Level by level', 'A queue holds <em>one whole level</em>.', 'q2',
         '"level by level" · "view from the right" · "average of each level"', P[1]),
        ('BST in sorted order', 'Inorder on a BST is <em>sorted</em>; count as you go.', 'q3',
         'the problem says <b>BST</b> · "k-th smallest" · "check whether it is a BST"', P[2]),
        ('Common ancestor and paths', 'The answer is the node that gets <em>one target from each side</em>.', 'q4',
         '"lowest common ancestor" · "path whose sum equals" · counting paths', P[3]),
        ('Rebuild and transform', 'Do one local change <em>at every node</em>.', 'q5',
         '"build a tree from two traversals" · serialize · invert · compare two trees', P[4]),
    ]),
]
build(PAGE, '/tmp/dsa/tree-bst-traversal.json', art, hero, 'tree', S, 'DSA · tree &amp; BST.')
print('written', PAGE)
