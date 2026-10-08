"""Language core group overview as a map (2026-10-09): lesson map (linked tree) · syntax to lesson (kept) · learning order (kept).
Run: python3 tools/svgkit/02-python/language_core_overview.py  (re-runnable)"""
# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from groupmap import rewrite, sec, gist, table, order, keep_figure
from overview import Fig, text
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
L = lambda d: "../%s/index.html" % d

PAGE = os.path.join(ROOT, "content/02-python/02-language-core/language-core-overview/index.html")
src = open(PAGE, encoding="utf-8").read()
SYN = keep_figure(src, "A table builds row by row: len(x)")
ORDF = keep_figure(src, "The seven lessons in reading order")
a = src.index("<table>", src.index("The seven lessons in reading order")); b = src.index("</table>", a) + 8
ORDT = src[a:b]
f = Fig("lcmap", 680, 250, "ONE RULE · SEVEN QUESTIONS IT RAISES · ONE LESSON EACH",
  "One rule at the top, a name is a tag on an object, branches into seven lessons, each with the question it answers and a link: "
  "memory model, is it copied; memory and GC, when is it freed; scope, where is the name; data model, what does syntax call; "
  "iterator, one item at a time; decorator, wrap a function; exceptions, what if it fails.")
f.node(340, 52, "a name is a tag on an object", "", "filled", f.step(.2), None, None, w=230, h=36)
kids = [("Memory model", "is it copied?", "memory-model-mutability"), ("Memory & GC", "when is it freed?", "memory-management-gc"),
        ("Scope & LEGB", "where is the name?", "scope-legb"), ("Data model", "what does syntax call?", "data-model-dunder"),
        ("Iterator", "one item at a time?", "iterator-generator"), ("Decorator", "wrap a function?", "decorator-context-manager"),
        ("Exceptions", "what if it fails?", "exception-handling")]
w, gap = 152, (680 - 4 * 152) / 3
xs1 = [w / 2 + c * (w + gap) for c in range(4)]
xs2 = [(xs1[c] + xs1[c + 1]) / 2 for c in range(3)]   # row 2 sits under the gaps, so its drops pass between row-1 boxes
f.add(f'<path class="{f.step(.4, draw=True)}" pathLength="1" d="M340,70 V96 M{xs1[0]},96 H{xs1[3]}" fill="none" stroke="var(--rule-hi)" stroke-width="1.6"/>')
for i, (n, q, d) in enumerate(kids):
    r = 0 if i < 4 else 1
    cx = xs1[i] if r == 0 else xs2[i - 4]
    cy = 130 + r * 76
    f.add(f'<line class="{f.step(.6 + i * .08, draw=True)}" pathLength="1" x1="{cx:.1f}" y1="96" x2="{cx:.1f}" y2="{cy - 22}" stroke="var(--rule-hi)" stroke-width="1.6"/>')
    f.node(cx, cy, n, q, "plain", f.step(.7 + i * .12), L(d), None, w=w, h=44)
MAP = f.svg()
BODY = """<header class="hero">
  <p class="eyebrow">Python · language core</p>
  <h1>Language core <em>overview</em></h1>
  <p class="lede">The rules every other part of Python is built on: one rule about names, and seven lessons that follow from it.</p>
</header>

""" + sec("lcov", 1, "Lesson map", "Every lesson here answers <em>one question</em> left open by the same rule.", gist(MAP)) + "\n"  + sec("lcov", 2, "Syntax to lesson", "Each piece of syntax <em>runs a method or a rule</em> underneath; the row says which lesson explains it.", SYN) + "\n"  + sec("lcov", 3, "Learning order", "Read in order; <em>skip a lesson</em> if you can answer its question.", ORDF, after=ORDT)
rewrite(PAGE, BODY)
print("ok")
