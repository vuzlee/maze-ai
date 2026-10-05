"""Rebuild content/01-dsa/03-data-structures/trie/index.html from /tmp/dsa/trie.json.
Run trie.py first. LeetCode links come verbatim from the pristine copy /tmp/dsa/orig-trie.html;
the old single list is split across the three patterns it already named."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from treekit_page import build, probs_of

ROOT = '/home/vuzle/Documents/mazeai/'
PAGE = ROOT + 'content/01-dsa/03-data-structures/trie/index.html'
P = probs_of(open('/tmp/dsa/orig-trie.html').read())
assert len(P) == 1
links = {re.search(r'<i>(\d+)</i>', a).group(1): a for a in re.findall(r'<a .*?</a>', P[0], re.S)}
def pl(*ids): return '<div class="probs">\n' + '\n'.join('    ' + links.pop(i) for i in ids) + '\n  </div>'
q1, q2, q3 = pl('208', '211', '648'), pl('212'), pl('421')
assert not links

art = '<article class="doc" id="art-trie" data-title="Trie" data-tag="Data structure" data-blurb="A tree of letters where words with the same start share one path.">'
hero = '''        <header class="hero">
  <p class="eyebrow">DSA · data structures</p>
  <h1><em>Trie</em> — the prefix tree</h1>
  <p class="lede">One letter per step: lookups cost the word length, not the number of words.</p>
</header>'''
S = [
    ('Mental model', 'A tree of letters: <em>words with the same start share one path</em>.', [
        ('Shared prefixes', 'Each word is a path from the root; <em>◎ marks where a word ends</em>.', 'm1', None, None),
    ]),
    ('Properties', 'Every operation walks <em>one letter per step</em>: O(L) for a word of length L.', [
        ('Search a word', 'Step down letter by letter, then <em>check the end mark</em>.', 'p1', None, None),
        ('Search a prefix', 'The same walk <em>without</em> the end check.', 'p2', None, None),
        ('Insert', 'Walk down, <em>create the missing letters</em>, mark the end.', 'p3', None, None),
        ('The end mark', 'Without it, <em>every prefix looks like a word</em>.', 'p4', None, None),
        ('Cost', 'Steps grow with <em>the word</em>, not with the store.', 'p5', None, None),
    ]),
    ('Patterns', 'Build the trie once, then <em>walk it many times</em>.', [
        ('Prefix lookup and autocomplete', 'Walk to the prefix, then <em>collect the subtree</em>.', 'q1',
         '"prefix" · autocomplete · <b>many</b> lookups against the same word list · a <code>.</code> wildcard', q1),
        ('Pruning a search', 'Drop a path the moment it is <em>no prefix of any word</em>.', 'q2',
         'search a grid or a string for many words at once · a trie inside backtracking', q2),
        ('Binary trie for XOR', 'Numbers as bit strings; <em>take the opposite bit</em> when it exists.', 'q3',
         '"maximum XOR" · pairs of numbers compared bit by bit', q3),
    ]),
]
build(PAGE, '/tmp/dsa/trie.json', art, hero, 'trie', S, 'DSA · trie.')
print('written', PAGE)
