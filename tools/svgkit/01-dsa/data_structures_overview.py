"""Data structures group overview as a lookup tool (2026-10-09). The shelf overview owns the gallery
and family tree; this page keeps: operation cost table · signal to structure · learning order.
Run: python3 tools/svgkit/01-dsa/data_structures_overview.py  (re-runnable)"""
# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from groupmap import rewrite, sec, gist, table, order, keep_figure
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))

PAGE = os.path.join(ROOT, "content/01-dsa/03-data-structures/data-structures-overview/index.html")
src = open(PAGE, encoding="utf-8").read()
SIG = keep_figure(src, "Eight problem signals on the left")
L = lambda d: "../%s/index.html" % d
COST = table("dsovc", "OPERATION COST · AVERAGE CASE · CLICK A ROW TO OPEN ITS LESSON",
  "A table of eight data structures and the cost of four operations. Array: access O(1), search O(n), insert and delete O(n) in the middle, O(1) at the end. "
  "Hash map: no access by position, search, insert and delete O(1) on average. Linked list: access and search O(n), insert and delete O(1) at a known node. "
  "Stack and queue: only the end, push and pop O(1). Heap: read the top O(1), search O(n), insert and delete O(log n). Balanced BST: all O(log n). "
  "Trie: search, insert and delete O(L) for a word of length L. Union-Find: find and union near O(1). Each row links to its lesson.",
  [(0, "STRUCTURE"), (150, "ACCESS"), (270, "SEARCH"), (400, "INSERT"), (540, "DELETE")],
  [("Array", "O(1)", "O(n)", "O(n) · end O(1)*", "O(n) · end O(1)", L("array-string")),
   ("Hash map", "—", "O(1) avg", "O(1) avg", "O(1) avg", L("hash-map")),
   ("Linked list", "O(n)", "O(n)", "O(1) at node", "O(1) at node", L("linked-list")),
   ("Stack / queue", "end only", "—", "O(1) push", "O(1) pop", L("stack-monotonic-queue")),
   ("Heap", "O(1) top", "O(n)", "O(log n)", "O(log n) top", L("heap-priority-queue")),
   ("Balanced BST", "O(log n)", "O(log n)", "O(log n)", "O(log n)", L("tree-bst-traversal")),
   ("Trie", "—", "O(L)", "O(L)", "O(L)", L("trie")),
   ("Union-Find", "—", "find ≈ O(1)", "union ≈ O(1)", "—", L("union-find"))],
  mono=(1, 2, 3, 4))
ORD = order("dsovo", "LEARNING ORDER · EACH LESSON REUSES THE ONE BEFORE",
  "Eight lessons in reading order, each a link: array and string, linked list, hash map, stack and queue, heap, tree and BST, trie, union-find.",
  [("Array & string", "index, slice", L("array-string")), ("Linked list", "pointers", L("linked-list")),
   ("Hash map", "key → value", L("hash-map")), ("Stack & queue", "one end", L("stack-monotonic-queue")),
   ("Heap", "smallest first", L("heap-priority-queue")), ("Tree & BST", "sorted links", L("tree-bst-traversal")),
   ("Trie", "prefix tree", L("trie")), ("Union-Find", "merge groups", L("union-find"))], per_row=4)
BODY = """<header class="hero">
  <p class="eyebrow">DSA · data structures</p>
  <h1>Data structures <em>overview</em></h1>
  <p class="lede">A lookup page: what each structure costs, and which wording points to which one. The pictures of every structure are on the <a href="../../01-overview/dsa-overview/index.html">DSA overview</a>.</p>
</header>

""" + sec("dsov", 1, "Operation cost",
  "Find the operation your loop repeats, then <em>pick the row where it is cheap</em>.", gist(COST),
  ["* averaged over many appends — see <a href=\"../../02-foundations/big-o-complexity/index.html\">Big-O</a>. <i>L</i> = word length.",
   "No row is cheap everywhere: the hash map loses order, the BST pays log n for keeping it."]) + "\n" + sec("dsov", 2, "Signal to structure",
  "The problem's wording usually <em>names the operation</em>; follow its line to a structure.", SIG) + "\n" + sec("dsov", 3, "Learning order",
  "Read top row first: <em>every later structure is built from arrays, pointers or both</em>.", gist(ORD))
rewrite(PAGE, BODY, "A lookup page for data structures: the cost of access, search, insert and delete for each one, and which problem wording points to which structure.",
  "DSA · data structures · next: <a href=\"../array-string/index.html\">Array &amp; string</a>.")
print("ok")
