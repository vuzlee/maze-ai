"""Core concepts group overview as a map (2026-10-09): workflow (where each lesson sits) · symptom to lesson · learning order.
Old mental model (1-NN memorises) and 2.1-2.5 dropped: each re-taught a lesson that already owns it
(supervised-unsupervised 3.1/3.2, bias-variance 1.1, train-val-test 2.1, overfitting 1/2, feature-engineering 2.1/4.2).
Run: python3 tools/svgkit/07-machine-learning/core_concepts_overview_v2.py  (re-runnable)"""
# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from groupmap import rewrite, sec, gist, table, order, keep_figure
from overview import Fig, text
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
L = lambda d: "../%s/index.html" % d

PAGE = os.path.join(ROOT, "content/07-machine-learning/04-core-concepts/core-concepts-overview/index.html")
f = Fig("ccmap", 680, 196, "ONE MODELLING LOOP · EACH LESSON OWNS ONE STEP",
  "A left-to-right loop of five steps, each a link to its lesson: define the problem type (supervised, unsupervised and reinforcement), "
  "build features (feature engineering), split the data (train, val, test and cross-validation), fit and diagnose the error (bias-variance tradeoff), "
  "then fix overfitting (overfitting and regularization). A dashed arrow from the last step back to features says: change and try again.")
steps = [("Problem type", "label? number? class?", "supervised-unsupervised"), ("Features", "columns → numbers", "feature-engineering"),
         ("Split", "train · val · test", "train-val-test-cv"), ("Diagnose", "bias or variance?", "bias-variance-tradeoff"),
         ("Fix", "regularize · data", "overfitting-regularization")]
w, gap = 126, 12
for i, (n, note, d) in enumerate(steps):
    cx = i * (w + gap) + w / 2
    if i:
        f.add(f'<line class="{f.step(.3 + i * .3, draw=True)}" pathLength="1" x1="{cx - w - gap + w/2 + 2:.1f}" y1="80" x2="{cx - w/2 - 3:.1f}" y2="80" stroke="var(--rule-hi)" stroke-width="1.6"/>')
    f.node(cx, 80, n, note, "violet" if i == 4 else "plain", f.step(.2 + i * .3), L(d), None, w=w, h=48)
x1 = 4 * (w + gap) + w / 2; x0 = 1 * (w + gap) + w / 2
f.add(f'<path class="{f.step(1.9, draw=True)}" pathLength="1" d="M{x1},104 C{x1},160 {x0},160 {x0},108" fill="none" stroke="var(--violet)" stroke-width="1.4" stroke-dasharray="4 3"/>'
      f'<path class="{f.step(2.2)}" d="M{x0-4},114 L{x0},106 L{x0+4},114z" fill="var(--violet)"/>')
f.add(f'<g class="{f.step(2.3)}">' + text((x0 + x1) / 2, 172, "change something, split stays fixed, try again", "sv-d", "var(--violet)", "middle", ";font-style:italic") + "</g>")
LOOP = f.svg()
T = table("ccsym", "WHAT YOU SEE → WHICH LESSON · CLICK A ROW",
  "A lookup table from a symptom to the lesson that explains it. Unsure what the label is: Supervised, unsupervised and reinforcement. "
  "Text, dates or categories in the table: Feature engineering. Test score much worse once deployed: Train, val, test and cross-validation, data leakage. "
  "Train and validation error both high: Bias-variance tradeoff, high bias. Train error low, validation error high: Overfitting and regularization.",
  [(0, "YOU SEE"), (330, "LESSON")],
  [("not sure what the label is, or there is none", "Supervised, unsupervised & RL", L("supervised-unsupervised")),
   ("text, dates or categories in the table", "Feature engineering", L("feature-engineering")),
   ("great offline score, poor once deployed", "Train / val / test · leakage", L("train-val-test-cv")),
   ("train and validation error both high", "Bias–variance · high bias", L("bias-variance-tradeoff")),
   ("train error low, validation error high", "Overfitting & regularization", L("overfitting-regularization"))], rowh=30)
ORD = order("ccord", "LEARNING ORDER", "Five lessons in reading order, each a link: problem type, bias and variance, data splits, overfitting, feature engineering.",
  [("Problem type", "", L("supervised-unsupervised")), ("Bias–variance", "", L("bias-variance-tradeoff")),
   ("Data splits", "", L("train-val-test-cv")), ("Overfitting", "", L("overfitting-regularization")),
   ("Features", "", L("feature-engineering"))], per_row=5)
BODY = """<header class="hero">
  <p class="eyebrow">Machine learning · Core concepts</p>
  <h1>Core concepts <em>overview</em></h1>
  <p class="lede">Five lessons, one question: <em>did the model learn, or did it memorise?</em> Each owns one step of the loop every model goes through.</p>
</header>

""" + sec("ccov", 1, "Modelling loop", "Every model goes through the same loop; <em>each lesson owns one step</em>.", gist(LOOP)) + "\n"  + sec("ccov", 2, "Symptom to lesson", "Start from what you see in the numbers, <em>not from the lesson titles</em>.", gist(T)) + "\n"  + sec("ccov", 3, "Learning order", "Ideas first, then the tools: <em>bias and variance explain why splits and regularization exist</em>.", gist(ORD))
rewrite(PAGE, BODY, "Five ideas every model reuses, on one page: the modelling loop, which lesson owns each step, and which lesson to open for the symptom you see.",
  "Machine learning · Core concepts · first lesson: <a href=\"../supervised-unsupervised/index.html\">Supervised, unsupervised &amp; reinforcement</a>.")
print("ok")
