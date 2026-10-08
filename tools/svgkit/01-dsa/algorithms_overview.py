"""Algorithms group overview as a lookup tool (2026-10-09): data size to speed (kept) · pattern list · learning order.
The shelf overview owns the problem-to-technique tree, so the old "wording to pattern" figure is dropped.
Run: python3 tools/svgkit/01-dsa/algorithms_overview.py  (re-runnable)"""
# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from groupmap import rewrite, sec, gist, table, order, keep_figure
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))

import re
PAGE = os.path.join(ROOT, "content/01-dsa/04-algorithms/algorithms-overview/index.html")
src = open(PAGE, encoding="utf-8").read()
SIZE = keep_figure(src, "Five cost rows from O(2^n)")
a = src.index("<table>", src.index("Five cost rows from O(2^n)")); b = src.index("</p>", src.index('class="stripnote"', a)) + 4
SIZE_TAB = "\n  " + src[a:b]
L = lambda d: "../%s/index.html" % d
PAT = table("alovp", "PATTERNS · THE WORDING THAT GIVES EACH ONE AWAY · CLICK A ROW",
  "A table of eleven patterns with the wording that signals each one and its usual cost. Sorting: order matters, O(n log n). Two pointers: sorted array, pair, in place, O(n). "
  "Sliding window: longest or shortest subarray, O(n). Prefix sum: sum of a range, many queries, O(n) build then O(1). Binary search: sorted, or smallest value such that, O(log n). "
  "Greedy: take the best local choice, O(n log n). Intervals: overlapping ranges, merge, O(n log n). Backtracking: all combinations, n up to 20, O(2^n). "
  "Graph BFS DFS: grid, connected, dependencies, O(V+E). Shortest path: weighted edges, cheapest route, O(E log V). Dynamic programming: how many ways, min or max cost, O(n·state). Each row links.",
  [(0, "PATTERN"), (160, "WORDING IN THE PROBLEM"), (520, "USUAL COST")],
  [("Sorting", "order matters · k-th · group equal items", "O(n log n)", L("sorting")),
   ("Two pointers", "sorted array · pair with sum · in place", "O(n)", L("two-pointers")),
   ("Sliding window", "longest / shortest contiguous subarray", "O(n)", L("sliding-window")),
   ("Prefix sum", "sum of a range · many range queries", "O(n) + O(1)", L("prefix-sum")),
   ("Binary search", "sorted · smallest value such that …", "O(log n)", L("binary-search")),
   ("Greedy", "best local choice never needs undoing", "O(n log n)", L("greedy")),
   ("Intervals", "overlapping ranges · merge · rooms", "O(n log n)", L("intervals")),
   ("Backtracking", "all subsets / permutations · n ≤ 20", "O(2ⁿ)", L("backtracking")),
   ("Graph BFS · DFS", "grid · connected · prerequisites", "O(V + E)", L("graph-bfs-dfs-topo")),
   ("Shortest path", "weighted edges · cheapest route", "O(E log V)", L("shortest-path")),
   ("Dynamic programming", "how many ways · min / max cost", "O(n · state)", L("dynamic-programming"))],
  mono=(2,), rowh=28)
ORD = order("alovo", "LEARNING ORDER · ARRAYS FIRST, THEN SEARCH, THEN GRAPHS AND DP",
  "Eleven lessons in reading order, each a link: sorting, two pointers, sliding window, prefix sum, binary search, greedy, intervals, backtracking, graph BFS and DFS, shortest path, dynamic programming.",
  [("Sorting", "", L("sorting")), ("Two pointers", "", L("two-pointers")), ("Sliding window", "", L("sliding-window")),
   ("Prefix sum", "", L("prefix-sum")), ("Binary search", "", L("binary-search")), ("Greedy", "", L("greedy")),
   ("Intervals", "", L("intervals")), ("Backtracking", "", L("backtracking")), ("Graph BFS · DFS", "", L("graph-bfs-dfs-topo")),
   ("Shortest path", "", L("shortest-path")), ("Dynamic prog.", "", L("dynamic-programming"))], per_row=4)
BODY = """<header class="hero">
  <p class="eyebrow">DSA · algorithms &amp; patterns</p>
  <h1>Algorithms <em>overview</em></h1>
  <p class="lede">A lookup page: which speed the data size allows, and which wording points to which pattern. The problem-to-technique tree is on the <a href="../../01-overview/dsa-overview/index.html">DSA overview</a>.</p>
</header>

""" + sec("alov", 1, "Data size to speed",
  "About 10⁸ simple operations fit in one second; <em>the data size rules out most speeds</em> before you start thinking.", SIZE, after=SIZE_TAB) + "\n" + sec("alov", 2, "Pattern list",
  "Spot the phrase, <em>check its cost against the size above</em>, open the lesson.", gist(PAT)) + "\n" + sec("alov", 3, "Learning order",
  "Array patterns first, then search, then <em>recursion, graphs and DP</em>.", gist(ORD))
rewrite(PAGE, BODY, "A lookup page for algorithms: which speeds the data size allows, and the wording that gives away each of the eleven patterns.",
  "DSA · algorithms · next: <a href=\"../sorting/index.html\">Sorting</a>.")
print("ok")
