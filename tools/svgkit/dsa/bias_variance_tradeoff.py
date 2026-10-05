# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/04-core-concepts/bias-variance-tradeoff.
Every number is simulated here: y = sin(2*pi*x) + N(0, 0.3^2), polynomial fits, 300 redrawn training sets.
Run: python3 bias_variance_tradeoff.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fitkit_bvof import *  # noqa

PAGE = os.path.join(HERE, '../../../content/07-machine-learning/04-core-concepts/bias-variance-tradeoff/index.html')
figs = {}

# ---------- 1.1 / 1.2 target ----------
def target(pre, d, n, cap_, aria, kind):
    rng = random.Random(5); shots, fits = [], []
    for _ in range(8):
        xs, ys = sample(rng, n); w = fit(xs, ys, d); fits.append(w)
        shots.append((pred(w, .25) - f(.25), pred(w, .75) - f(.75)))
    b2, v = bias_var(poly_fitter(d), n)
    an = Anim(pre, 720, 300, aria, cap_, 2.5)
    # left: the fits
    p, ax = fit_plot(pre, 30, 40, 330, 200)
    an.static(ax)
    for xm in (.25, .75):
        an.static(L(p.px(xm), p.y, p.px(xm), p.y + p.h, 'var(--rule-hi)', 1, '3 3') + T(p.px(xm), p.y + p.h + 16, 'x = %.2f' % xm, FA, cls='sv-l'))
    an.static(p.line(curve_pts(f), FI, 2.2, '5 4') + T(p.x + p.w - 4, p.py(-1.05) + 26, 'truth f(x)', FI, 'end'))
    cx, cy, S = 560, 150, 95
    an.static(''.join('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="var(--rule-hi)" stroke-width="1"/>' % (cx, cy, r, fl)
                      for r, fl in ((S, 'var(--bg)'), (S * 2 / 3, 'var(--bg)'), (S / 3, 'var(--sunk)'))) +
              '<circle cx="%d" cy="%d" r="4" fill="%s"/>' % (cx, cy, FI) +
              T(cx, cy + S + 18, 'miss at x = 0.25 →', FA, cls='sv-l') +
              T(cx - S - 8, cy + 4, 'miss at 0.75', FA, 'end', cls='sv-l') + T(cx + 8, cy - 8, 'truth', FI, 'start', cls='sv-l'))
    t = .6
    for k, (w, (ex, ey)) in enumerate(zip(fits, shots)):
        pts = curve_pts(lambda x: pred(w, x))
        an.show(p.line(pts, VI, 2.2), t, hide=t + .9)
        an.show(p.line(pts, BR, 1.1, op='.45'), t + .9)
        sx, sy = cx + ex * S, cy - ey * S
        an.show(p.dot(.25, pred(w, .25), VI, 3.5) + p.dot(.75, pred(w, .75), VI, 3.5), t + .3, hide=t + .9)
        an.show('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (sx, sy, VI), t + .5, hide=t + 1.0)
        an.show('<circle cx="%.1f" cy="%.1f" r="4.2" fill="%s" fill-opacity=".75"/>' % (sx, sy, BR), t + 1.0)
        t += 1.0
    an.show(T(30, 284, '8 training sets → 8 fitted curves → 8 shots', MU, 'start'), .6, hide=t)
    mx = sum(s[0] for s in shots) / 8; my = sum(s[1] for s in shots) / 8
    gx, gy = cx + mx * S, cy - my * S
    if kind == 'bias':
        an.show(arrow(cx, cy, gx, gy, VI, 2, None, 8) + '<circle cx="%.1f" cy="%.1f" r="6" fill="none" stroke="%s" stroke-width="2"/>' % (gx, gy, VI), t + .2)
        an.show(T((cx + gx) / 2 - 10, (cy + gy) / 2 - 2, 'bias', VI, 'end', bold=True), t + .5)
    else:
        rad = (sum((s[0] - mx) ** 2 + (s[1] - my) ** 2 for s in shots) / 8) ** .5 * S
        an.show('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="rgba(var(--violet-a),.10)" stroke="%s" stroke-width="1.6" stroke-dasharray="4 3"/>' % (gx, gy, rad, VI), t + .2)
        an.show(T(gx + rad + 6, gy - rad + 6, 'variance', VI, 'start', bold=True), t + .5)
    an.show(T(30, 284, 'degree %d · %d points · over 300 sets: bias² = %.3f · variance = %.3f' % (d, n, b2, v), FI, 'start', bold=True), t + .9)
    return an.render(), (b2, v)

figs['F11'], bv1 = target('t1-', 1, 12, 'BIAS · THE SHOTS LAND TOGETHER, OFF CENTRE',
    'Left: eight training sets each give a straight line fitted to sine-shaped data; each line is compared with the truth at x = 0.25 and x = 0.75. Right: each line becomes one shot on a target, its miss at 0.25 horizontally and at 0.75 vertically. The shots cluster tightly but away from the centre; an arrow from the centre to their mean is the bias.', 'bias')
figs['F12'], bv2 = target('t2-', 8, 12, 'VARIANCE · THE SHOTS SCATTER AROUND THE CENTRE',
    'Left: eight training sets each give a degree-8 polynomial; the curves wiggle differently each time. Right: each curve becomes one shot; the shots sit around the centre but spread widely. A dashed circle around their mean is the variance.', 'var')
assert bv1[0] > 10 * bv1[1] and bv2[1] > 10 * bv2[0]

# ---------- 1.3 noise ----------
def noise():
    rng = random.Random(11); xs, ys = sample(rng, 16)
    ms = sum((y - f(x)) ** 2 for x, y in zip(xs, ys)) / len(xs)
    an = Anim('n3-', 720, 292, 'Sixteen points scatter around the true sine curve. A short stick joins each point to the curve: even the true function misses every point. Their mean squared length is about sigma squared, 0.09.', 'NOISE · EVEN THE TRUTH MISSES', 2.5)
    p, ax = fit_plot('n3-', 40, 40, 640, 190)
    an.static(ax); an.show(p.line(curve_pts(f), FI, 2.4), .2, d=.6)
    an.static(T(p.px(.06), p.py(1.25), 'truth f(x)', FI, 'start'))
    for k, (x, y) in enumerate(zip(xs, ys)):
        t = .9 + k * .3
        an.show(p.dot(x, y, BR, 3.8), t)
        an.show(L(p.px(x), p.py(f(x)), p.px(x), p.py(y), VI, 2), t + .15)
    t = .9 + 16 * .3 + .4
    an.show(T(40, 272, 'mean squared stick = %.3f ≈ σ² = 0.09 · no model can go below it' % ms, FI, 'start', bold=True), t)
    return an.render(), ms
figs['F13'], ms = noise(); assert abs(ms - .09) < .05

# ---------- 2 decomposition bars ----------
DEC = [(d, bias_var(poly_fitter(d), 12)) for d in (1, 3, 8)]
def decomp():
    an = Anim('d2-', 720, 230, 'Three stacked bars, one per model: degree 1, degree 3, degree 8, all fitted on 12 points. Each bar grows segment by segment: bias squared, then variance, then the fixed noise of 0.09. Degree 1 is mostly bias, degree 8 mostly variance, degree 3 has the shortest total.', 'TOTAL ERROR = BIAS² + VARIANCE + NOISE', 2.5)
    X0, SC = 110, 520 / .32
    leg = [(BR, 'bias²'), (VI, 'variance'), (GH, 'noise σ²')]
    an.static(''.join(R(X0 + k * 120, 30, 12, 12, c, 'none', 2) + T(X0 + k * 120 + 18, 40, l, MU, 'start') for k, (c, l) in enumerate(leg)))
    best = min(DEC, key=lambda r: sum(r[1]))
    for i, (d, (b2, v)) in enumerate(DEC):
        y = 66 + i * 50; t = .5 + i * 1.6
        an.show(T(X0 - 12, y + 19, 'degree %d' % d, TX, 'end'), t)
        x = X0
        for k, (val, c) in enumerate(((b2, BR), (v, VI), (.09, GH))):
            w = max(val * SC, 1.5)
            an.show(R(x, y, w, 28, c, 'none', 2), t + .2 + k * .4)
            if w > 44:
                an.show(T(x + w / 2, y + 19, '%.3f' % val, 'var(--on-fill)'), t + .35 + k * .4)
            x += w
        tot = b2 + v + .09
        an.show(T(x + 8, y + 19, '= %.3f' % tot, FI if d == best[0] else TX, 'start', bold=d == best[0]), t + 1.4)
    an.show(T(X0, 222, 'degree %d: lowest total — neither the lowest bias nor the lowest variance' % best[0], FI, 'start', bold=True), .5 + 3 * 1.6 + .3)
    return an.render()
figs['F2'] = decomp()
assert min(DEC, key=lambda r: sum(r[1]))[0] == 3

# ---------- 3 U curve ----------
DEG = list(range(9)); BV = [bias_var(poly_fitter(d), 12) for d in DEG]
def ucurve():
    an = Anim('u3-', 720, 320, 'Error against polynomial degree from 0 to 8, on 12 points. Bias squared falls, variance rises, the noise floor stays at 0.09. Their sum is U-shaped, lowest at degree 3.', 'COMPLEXITY UP · BIAS DOWN · VARIANCE UP', 2.5)
    p = Plot('u3-', 70, 40, 560, 220, (0, 8), (0, .65))
    an.static(p.clip() + p.axes([(d, str(d)) for d in DEG], [(v, '%.1f' % v) for v in (.2, .4, .6)], 'model complexity (degree)', 'error'))
    an.show(p.line([(0, .09), (8, .09)], GH, 1.6, '5 4') + T(p.px(8) + 8, p.py(.09) + 4, 'noise', FA, 'start'), .3)
    def series(vals, c, t, lab, ly):
        pts = list(zip(DEG, vals)); p.draw(an, pts, t, 1.4, c, 2.4, k=8)
        for d, v in pts: an.show(p.dot(d, v, c, 3), t + 1.4 * d / 8)
        an.show(T(p.px(8) + 8, ly, lab, c, 'start', bold=True), t + 1.4)
    series([b for b, _ in BV], BR, .6, 'bias²', p.py(BV[8][0]) - 6)
    series([v for _, v in BV], VI, 2.4, 'variance', p.py(BV[8][1]) + 4)
    tot = [b + v + .09 for b, v in BV]
    series(tot, FI, 4.2, 'total', p.py(tot[8]) - 2)
    k = min(DEG, key=lambda d: tot[d])
    an.show(L(p.px(k), p.py(tot[k]) - 10, p.px(k), p.py(0), FI, 1.2, '3 3') + '<circle cx="%.1f" cy="%.1f" r="7" fill="none" stroke="%s" stroke-width="2"/>' % (p.px(k), p.py(tot[k]), FI), 6.0)
    an.show(T(p.px(k) + 10, p.py(tot[k]) - 12, 'best: degree %d · total %.3f' % (k, tot[k]), FI, 'start', bold=True), 6.2)
    an.show(T(p.px(.2), 312, '← underfit: bias dominates', MU, 'start'), 6.6)
    an.show(T(p.px(8), 312, 'overfit: variance dominates →', MU, 'end'), 6.6)
    return an.render(), k
figs['F3'], best = ucurve(); assert best == 3

# ---------- 4 fixes ----------
def fix(pre, cap_, aria, change, before, after):
    an = Anim(pre, 720, 204, aria, cap_, 2.5)
    an.static(T(0, 44, change, TX, 'start', bold=True))
    X0, SC = 100, 470 / max(max(before), max(after))
    for i, (lab, c, b, a_) in enumerate((('bias²', BR, before[0], after[0]), ('variance', VI, before[1], after[1]))):
        y = 66 + i * 58
        an.static(T(X0 - 12, y + 18, lab, c, 'end', bold=True))
        an.show(R(X0, y, max(b * SC, 1.5), 26, c, 'none', 2) + T(X0 + max(b * SC, 1.5) + 8, y + 18, '%.3f' % b, MU, 'start'), .4 + i * .3, hide=2.2)
        an.show(R(X0, y, max(b * SC, 1.5), 26, 'none', GH, 2, 1.2, '4 3'), 2.2)
        an.show(R(X0, y, max(a_ * SC, 1.5), 26, c, 'none', 2), 2.4)
        r = a_ / b if b > 1e-9 else 1
        verdict = 'unchanged' if (.7 < r < 1.4 or max(a_, b) < .006) else ('×%.1f' % r if r > 1 else '÷%.0f' % (1 / r) if r < .2 else '÷%.1f' % (1 / r))
        an.show(T(X0 + max(b, a_) * SC + 8, y + 18, '%.3f → %.3f  %s' % (b, a_, verdict), c, 'start', bold=True), 2.8 + i * .3)
    an.show(T(0, 186, 'total (with noise 0.09): %.3f → %.3f' % (sum(before) + .09, sum(after) + .09), FI, 'start', bold=True), 3.6)
    return an.render()

F41 = (bias_var(poly_fitter(7), 12), bias_var(poly_fitter(7), 48))
F42 = (bias_var(poly_fitter(9, 0), 12), bias_var(poly_fitter(9, .1), 12))
F43 = (bias_var(poly_fitter(1), 20), bias_var(poly_fitter(3), 20))
def nn1(xs, ys): return lambda x: ys[min(range(len(xs)), key=lambda i: abs(xs[i] - x))]
def bag(B=40):
    def fm(xs, ys, rng):
        ms_ = []
        for _ in range(B):
            idx = sorted(set(rng.randrange(len(xs)) for _ in xs)); ms_.append(nn1([xs[i] for i in idx], [ys[i] for i in idx]))
        return lambda x: sum(m(x) for m in ms_) / B
    return fm
F44 = (bias_var(lambda xs, ys, rng: nn1(xs, ys), 20, 200), bias_var(bag(), 20, 200))
assert F41[1][1] < F41[0][1] / 3 and F42[1][0] > F42[0][0] and F43[1][0] < F43[0][0] / 10 and F44[1][1] < F44[0][1] * .7
figs['F41'] = fix('m41-', 'MORE DATA · VARIANCE ONLY', 'Degree-7 polynomial, training set grows from 12 to 48 points. The bias squared bar stays near zero; the variance bar shrinks to a fraction.', 'n: 12 → 48 points (degree 7)', *F41)
figs['F42'] = fix('m42-', 'STRONGER REGULARIZATION · BIAS UP, VARIANCE DOWN', 'Degree-9 polynomial with an L2 penalty, lambda raised from 0 to 0.1. Variance collapses, bias squared grows slightly: the classic trade.', 'λ: 0 → 0.1 (degree 9, 12 points)', *F42)
figs['F43'] = fix('m43-', 'STRONGER MODEL · BIAS DOWN, VARIANCE UP', 'From a straight line to a cubic on 20 points. Bias squared collapses, variance grows a little.', 'degree: 1 → 3 (20 points)', *F43)
figs['F44'] = fix('m44-', 'BAGGING · VARIANCE DOWN, BIAS KEPT', 'A 1-nearest-neighbour model versus the average of 40 of them, each trained on a bootstrap resample. Bias squared stays the same; variance roughly halves.', '1 model → average of 40 bootstrap models (1-NN, 20 points)', *F44)

def mth(s): return '<span class="mth">%s</span>' % s
BODY = '''<section id="bv-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Mental model</h2></div>
  <p class="key">Retrain the same model on <em>many different training sets</em> and look at where its predictions land: <b>off target together</b> is bias, <b>scattered</b> is variance, and the truth itself still misses by the noise.</p>
  <div class="subsec" id="bv-s1-1">
    <h3 class="ssh"><b>1.1</b>Bias</h3>
    <p class="skey">A model too simple for the data <em>misses the same way every time</em>.</p>
{F11}
    <ul class="why">
      <li>Bias is the gap between the <b>average prediction</b> and the truth: the arrow from the centre to the middle of the shots.</li>
      <li>More data does not move the shots: the error lives in the model's <em>shape</em>.</li>
    </ul>
  </div>
  <div class="subsec" id="bv-s1-2">
    <h3 class="ssh"><b>1.2</b>Variance</h3>
    <p class="skey">A model too flexible <em>changes a lot when the training set changes</em>.</p>
{F12}
    <ul class="why">
      <li>Variance is how far the shots spread around their own average.</li>
      <li>Each curve chases the noise of its own sample, so every retrain lands somewhere new.</li>
    </ul>
  </div>
  <div class="subsec" id="bv-s1-3">
    <h3 class="ssh"><b>1.3</b>Noise</h3>
    <p class="skey">Even the true function <em>misses every point</em> by the noise in the labels.</p>
{F13}
    <ul class="why">
      <li>Noise <span class="mth"><var>σ</var><sup>2</sup></span> is a floor: two customers with identical features, one buys and one does not.</li>
      <li>Once validation error sits on that floor, only <b>new features</b> help, not more capacity.</li>
    </ul>
  </div>
</section>

<section id="bv-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Error decomposition</h2></div>
  <p class="key">Expected squared error splits into <em>exactly three parts</em>; the goal is the smallest <b>total</b>, not the smallest part.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>E</var>[(<var>y</var> − <var>f̂</var>(<var>x</var>))<sup>2</sup>]</span><em>expected error</em></span>
      <span class="op">=</span>
      <span class="t b"><span>(<var>E</var>[<var>f̂</var>(<var>x</var>)] − <var>f</var>(<var>x</var>))<sup>2</sup></span><em>bias²</em></span>
      <span class="op">+</span>
      <span class="t"><span><var>E</var>[(<var>f̂</var>(<var>x</var>) − <var>E</var>[<var>f̂</var>(<var>x</var>)])<sup>2</sup>]</span><em>variance</em></span>
      <span class="op">+</span>
      <span class="t"><span><var>σ</var><sup>2</sup></span><em>noise</em></span>
    </div>
    <dl>
      <dt>f(x)</dt><dd>the truth, fixed and unknown</dd>
      <dt>f̂(x)</dt><dd>the learned model, different for every training set</dd>
      <dt>E[·]</dt><dd>average over all training sets that could be drawn</dd>
    </dl>
  </div>
{F2}
  <ul class="why">
    <li>Every regularization technique is the same deal: <b>give up a little bias to win back a lot of variance</b>.</li>
    <li>The decomposition is exact for squared error; for other losses the same intuition holds.</li>
  </ul>
</section>

<section id="bv-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Tradeoff curve</h2></div>
  <p class="key">Push complexity up: bias falls, variance rises, and <em>their sum is U-shaped</em>. Stop at the bottom of the U.</p>
{F3}
  <ul class="why">
    <li>"Complexity" is whatever the model exposes: polynomial degree, <code>max_depth</code>, number of layers, <span class="mth">1/<var>λ</var></span>.</li>
    <li>In practice you cannot compute bias and variance; you read them from train and validation error — see <a href="../overfitting-regularization/index.html">Overfitting &amp; regularization</a>.</li>
    <li>Very large neural networks show <b>double descent</b>: past the point where parameters exceed samples, test error falls again.</li>
  </ul>
</section>

<section id="bv-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Which fix hits which term</h2></div>
  <p class="key">Every fix moves <em>one term down and often the other up</em>. Diagnose first, then pick the fix.</p>
  <div class="subsec" id="bv-s4-1">
    <h3 class="ssh"><b>4.1</b>More data</h3>
    <p class="skey">Cuts <em>variance</em>; bias does not move.</p>
{F41}
    <ul class="why"><li>Useless when the problem is bias — the learning curve tells you which, see <a href="../overfitting-regularization/index.html#overfit-s2-2">Learning curves</a>.</li></ul>
  </div>
  <div class="subsec" id="bv-s4-2">
    <h3 class="ssh"><b>4.2</b>Regularization</h3>
    <p class="skey">Trades a little <em>bias</em> for a lot less <em>variance</em>.</p>
{F42}
    <ul class="why"><li>L1, L2, dropout and early stopping all live here: <a href="../overfitting-regularization/index.html#overfit-s3">Regularization</a>.</li></ul>
  </div>
  <div class="subsec" id="bv-s4-3">
    <h3 class="ssh"><b>4.3</b>Stronger model</h3>
    <p class="skey">More features or capacity: the <em>reverse</em> trade.</p>
{F43}
    <ul class="why"><li>Boosting works on this side: each round cuts bias, so it needs early stopping before variance takes over.</li></ul>
  </div>
  <div class="subsec" id="bv-s4-4">
    <h3 class="ssh"><b>4.4</b>Bagging</h3>
    <p class="skey">Averaging many models trained on resamples <em>cuts variance and keeps bias</em>.</p>
{F44}
    <ul class="why"><li>That is why Random Forest beats a single deep tree: see <a href="../../06-tree-models/tree-family-overview/index.html">Tree family overview</a>.</li></ul>
  </div>
</section>

''' + REPLAY + '''

<footer>Machine learning · Core concepts · continued in <a href="../overfitting-regularization/index.html">Overfitting &amp; regularization</a> (diagnosis and fixes) and <a href="../train-val-test-cv/index.html">Train/val/test &amp; cross-validation</a> (measuring it right).</footer>
'''

if __name__ == '__main__':
    body = BODY
    for k, v in figs.items():
        assert '{%s}' % k in body, k
        body = body.replace("{%s}" % k, solid_brand(v))
    s = open(PAGE).read()
    i = s.index('<section'); j = s.index('</article>')
    s = s[:i] + body + '\n      ' + s[j:]
    s = s.replace('<script src="lab.js"></script>\n', '')
    s = s.replace('data-blurb="Decomposing error into three parts, the tradeoff curve, and which technique targets which part."',
                  'data-blurb="Error splits into bias, variance and noise; complexity trades one for the other, and each fix targets one term." data-reviewed="2"')
    open(PAGE, 'w').write(s)
    print('ok', F41, F42, F43, F44)
