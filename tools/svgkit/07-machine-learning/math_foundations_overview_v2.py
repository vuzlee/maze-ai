"""Math foundations group overview as a map (2026-10-09): how the four connect (old mental-model figure, kept) ·
lesson table · learning order. Old 2.1-2.4 dropped: each re-taught its lesson, and the lessons already own that
material (probability 5.2 MSE from the bell, linear-algebra 3.1/3.4, calculus 1.1/3.1, statistics 1.4).
Run: python3 tools/svgkit/07-machine-learning/math_foundations_overview_v2.py  (re-runnable)"""
# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from groupmap import rewrite, sec, gist, table, order, keep_figure
from overview import Fig, text
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
L = lambda d: "../%s/index.html" % d

PAGE = os.path.join(ROOT, "content/07-machine-learning/02-math-foundations/math-foundations-overview/index.html")
src = open(PAGE, encoding="utf-8").read()
CHAIN = keep_figure(src, "Data points appear; a bell curve sits on each point")
T = table("mathmap", "FOUR LESSONS · ONE JOB EACH · CLICK A ROW",
  "A table of the four math lessons, each with its job and where it comes back. Probability writes down the loss: distributions, Bayes, maximum likelihood; it returns in log loss, Naive Bayes and Ridge. "
  "Linear algebra packs the data: vectors, dot product, matrices; it returns in every linear model, PCA, embeddings and attention. "
  "Calculus finds the minimum: derivative, gradient, chain rule; it returns in gradient descent and backpropagation. "
  "Statistics checks the result: intervals, tests, A/B testing; it returns whenever two models are compared.",
  [(0, "LESSON"), (130, "ITS JOB"), (330, "COMES BACK IN")],
  [("Probability", "write down the loss", "log loss · Naive Bayes · Ridge as a prior", L("probability")),
   ("Linear algebra", "pack data into matrices", "linear models · PCA · embeddings · attention", L("linear-algebra")),
   ("Calculus", "walk down to the minimum", "gradient descent · backpropagation", L("calculus")),
   ("Statistics", "check the result is real", "model comparison · A/B tests", L("statistics"))], rowh=36)
ORD = order("mathord", "LEARNING ORDER · THE CHAIN FIRST, THE CHECK LAST",
  "Four lessons in reading order, each a link: probability, linear algebra, calculus, statistics.",
  [("Probability", "the loss", L("probability")), ("Linear algebra", "the data", L("linear-algebra")),
   ("Calculus", "the minimum", L("calculus")), ("Statistics", "the check", L("statistics"))], per_row=4)
BODY = """<header class="hero">
  <p class="eyebrow">Machine learning · Math foundations</p>
  <h1>Math foundations <em>overview</em></h1>
  <p class="lede">Not a math course. Math in ML does two things — <b>write down the loss</b> and <b>find where it is smallest</b> — and four lessons cover it. Reading and explaining is enough; no proofs.</p>
</header>

""" + sec("mathov", 1, "How the four connect",
  "Fit a line to points: <em>probability says what “wrong” costs, calculus walks downhill to the cheapest line.</em>", CHAIN,
  ["Linear algebra is what lets the same picture run with thousands of weights at once; statistics asks whether the final score is real or luck."]) + "\n"  + sec("mathov", 2, "Lesson map", "Each lesson owns <em>one step</em> of the picture above.", gist(T)) + "\n"  + sec("mathov", 3, "Learning order", "Probability, linear algebra and calculus form <em>one chain</em>; statistics checks the result.", gist(ORD))
rewrite(PAGE, BODY, "The four bits of math ML uses, on one page: how probability, linear algebra and calculus chain into a trained model, what statistics checks, and the order to read them.",
  "Machine learning · Math foundations · first lesson: <a href=\"../probability/index.html\">Probability</a>.")
print("ok")
