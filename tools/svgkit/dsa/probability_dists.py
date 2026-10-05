# -*- coding: utf-8 -*-
"""Probability 1.3: one subsection per common distribution, each with its own figure.
Run: python3 probability_dists.py  -> replaces subsection prob-s1-3 in the page (idempotent)."""
import os, sys, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from probability import T, L, R, Fig, MU, TX, FA, BR, VI, FI, BRA, FIA, VIA, P, C, area, Plot, draw, npdf
PAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '../../../content/07-machine-learning/02-math-foundations/probability/index.html')
def ncdf(x): return .5 * (1 + math.erf(x / math.sqrt(2)))
W = 720

def bars_fig(pre, cap, aria, dists, xr, ytop, xt, yt, note):
    """Each (label, pmf) in dists plays in turn on the same axes; the last one stays."""
    F = Fig(pre, W, 270, aria, cap)
    A = Plot(60, 46, 420, 150, xr, (0, ytop))
    F(A.axes(xt, yt, 'k', 'P(X = k)'))
    t = .4
    for i, (lab, d, mean) in enumerate(dists):
        last = i == len(dists) - 1
        hide = None if last else t + 1.6
        bw = min(34, A.w / (xr[1] - xr[0]) * .7)
        for k, (v, p) in enumerate(d):
            F(A.bar(v, p, bw, BRA('.24') if last else BRA('.12'), BR if last else 'var(--ghost)'), show=t + k * .05, hide=hide)
        F(T(510, 70 + i * 22, lab, FI if last else FA, 'start', mono=True), show=t)
        if mean is not None:
            F(L(A.px(mean), A.y - 4, A.px(mean), A.py(0), VI, 1.6, '4 3') + T(A.px(mean) + 5, A.y + 6, 'E = %g' % mean, VI, 'start', 'sv-l'),
              show=t + .6, hide=hide)
        t += 2.0
    F(T(60, 258, note, MU, 'start'), show=t)
    return F.render()

def bernoulli():
    d = lambda p: [(0, 1 - p), (1, p)]
    return bars_fig('pbe-', 'BERNOULLI · ONE COIN, TWO OUTCOMES',
        'Bars for 0 and 1. With p 0.5 both bars are 0.5; with p 0.3 the bars are 0.7 and 0.3, and the mean line moves to 0.3.',
        [('p = 0.5', d(.5), .5), ('p = 0.3', d(.3), .3)], (-.6, 1.6), 1, [(0, '0'), (1, '1')], [(.5, '0.5'), (1, '1')],
        'one yes/no trial — a click, a fraud flag, a binary label')

def binomial():
    d = lambda n, p: [(k, math.comb(n, k) * p ** k * (1 - p) ** (n - k)) for k in range(n + 1)]
    return bars_fig('pbi-', 'BINOMIAL · COUNT THE YESES IN n COINS',
        'Number of successes in 10 trials. With p 0.5 the bars form a symmetric hump at 5; with p 0.2 the hump moves to 2.',
        [('n = 10, p = 0.5', d(10, .5), 5), ('n = 10, p = 0.2', d(10, .2), 2)], (-.7, 10.7), .32,
        [(0, '0'), (5, '5'), (10, '10')], [(.25, '0.25')], 'conversions out of n visitors in an A/B test')

def poisson():
    d = lambda lam: [(k, math.exp(-lam) * lam ** k / math.factorial(k)) for k in range(13)]
    return bars_fig('ppo-', 'POISSON · COUNT OF RARE EVENTS IN A WINDOW',
        'Count of events per window. With rate 1 most mass sits at 0 and 1; with rate 4 the bars spread right around 4.',
        [('λ = 1', d(1), 1), ('λ = 4', d(4), 4)], (-.7, 12.7), .4, [(0, '0'), (4, '4'), (8, '8'), (12, '12')], [(.25, '0.25')],
        'requests per second, errors per day — mean and variance are both λ')

def uniform():
    F = Fig('pun-', W, 270, 'A flat density of height 1 over 0 to 1. A sampled point drops anywhere with equal chance; the shaded area '
            'between 0.2 and 0.5 is 0.3.', 'UNIFORM · EVERY VALUE IN [a, b] EQUALLY LIKELY')
    A = Plot(60, 46, 420, 150, (-.3, 1.3), (0, 1.4))
    F(A.axes([(0, 'a = 0'), (1, 'b = 1')], [(1, '1')], 'x', 'f(x)'))
    F(P([(A.px(-.3), A.py(0)), (A.px(0), A.py(0)), (A.px(0), A.py(1)), (A.px(1), A.py(1)), (A.px(1), A.py(0)), (A.px(1.3), A.py(0))], BR, 2.2), show=.3)
    F(area([(A.px(0), A.py(1)), (A.px(1), A.py(1))], A.py(0), BRA('.14')), show=.5)
    import random; rnd = random.Random(7)
    for k in range(12):
        x = rnd.random()
        F(C(A.px(x), A.py(0) - 6, 3.2, VI), show=1.0 + k * .12, move=(1.0 + k * .12, 0, -110, .5))
    t = 3.0
    F(area([(A.px(.2), A.py(1)), (A.px(.5), A.py(1))], A.py(0), FIA('.32')), show=t)
    F(T(A.px(.35), A.py(.5), '0.3', FI, cls='sv-s', bold=True), show=t + .2)
    F(T(510, 90, 'P(0.2 ≤ X ≤ 0.5)', FI, 'start', mono=True), show=t + .2)
    F(T(510, 110, '= width × height = 0.3', FI, 'start', mono=True), show=t + .4)
    F(T(60, 260, 'random initial weights, a random split point, "no idea" priors', MU, 'start'), show=t + .8)
    return F.render()

def gaussian():
    F = Fig('pga-', W, 290, 'A bell with mean 0 and sd 1. Then the bands within 1, 2 and 3 standard deviations shade in turn, '
            'holding 68, 95 and 99.7 percent. Then a value x = 1.5 is marked: z = 1.5 sigma from the mean.',
            'GAUSSIAN · THE BELL AND THE 68–95–99.7 RULE')
    G = Plot(60, 40, 560, 150, (-3.6, 3.6), (0, .42))
    F(L(G.x, G.py(0), G.x + G.w, G.py(0), MU, 1.1))
    for v in (-3, -2, -1, 0, 1, 2, 3):
        F(T(G.px(v), G.py(0) + 16, ('%+dσ' % v) if v else 'μ', FA, cls='sv-l') + L(G.px(v), G.py(.41), G.px(v), G.py(0), 'var(--rule)', 1, '2 4'))
    tb = draw(F, G.curve(npdf, -3.6, 3.6), .3, BR, 1.0)
    for k, (al, lab) in enumerate([('.32', '68%'), ('.18', '95%'), ('.09', '99.7%')], 1):
        assert abs((ncdf(k) - ncdf(-k)) * 100 - float(lab[:-1])) < .5
        tk = tb + .3 + (k - 1) * .9
        inner = 0 if k == 1 else k - 1
        F(area(G.curve(npdf, -k, -inner, 20), G.py(0), FIA(al)) + area(G.curve(npdf, inner, k, 20), G.py(0), FIA(al)), show=tk)
        yb = G.py(0) + 22 + k * 14
        F(L(G.px(-k), yb, G.px(k), yb, FI, 1.4) + L(G.px(-k), yb - 4, G.px(-k), yb + 4, FI, 1.4) +
          L(G.px(k), yb - 4, G.px(k), yb + 4, FI, 1.4) + T(G.px(k) + 8, yb + 4, lab, FI, 'start', 'sv-l'), show=tk)
    tz = tb + 3.2
    F(L(G.px(1.5), G.py(npdf(1.5)) - 4, G.px(1.5), G.py(0), VI, 2) + C(G.px(1.5), G.py(npdf(1.5)), 4, VI), show=tz)
    F(T(G.px(1.5) + 8, G.py(npdf(1.5)) - 8, 'x = 1.5 → z = 1.5', VI, 'start', 'sv-s'), show=tz)
    return F.render()

EQ = {
 'bern': '''<div class="eq">
      <div class="line"><span class="t"><span><var>P</var>(<var>X</var> = 1) = <var>p</var>,&nbsp; <var>P</var>(<var>X</var> = 0) = 1 − <var>p</var></span></span></div>
      <div class="line"><span class="t g"><span>E[<var>X</var>] = <var>p</var></span><em>mean</em></span><span class="op">·</span><span class="t p"><span>Var(<var>X</var>) = <var>p</var>(1 − <var>p</var>)</span><em>largest at p = 0.5</em></span></div>
    </div>''',
 'bin': '''<div class="eq">
      <div class="line"><span class="t"><span><var>P</var>(<var>X</var> = <var>k</var>)</span></span><span class="op">=</span><span class="t b"><span>C(<var>n</var>, <var>k</var>)</span><em>ways to pick k</em></span><span class="t p"><span><var>p</var><sup><var>k</var></sup> (1 − <var>p</var>)<sup><var>n</var>−<var>k</var></sup></span><em>one such sequence</em></span></div>
      <div class="line"><span class="t g"><span>E[<var>X</var>] = <var>np</var></span><em>mean</em></span><span class="op">·</span><span class="t"><span>Var(<var>X</var>) = <var>np</var>(1 − <var>p</var>)</span><em>variance</em></span></div>
    </div>''',
 'poi': '''<div class="eq">
      <div class="line"><span class="t"><span><var>P</var>(<var>X</var> = <var>k</var>)</span></span><span class="op">=</span><span class="t b"><span><span class="frac"><i><var>λ</var><sup><var>k</var></sup> <var>e</var><sup>−<var>λ</var></sup></i><i><var>k</var>!</i></span></span><em>λ = average count per window</em></span></div>
      <div class="line"><span class="t g"><span>E[<var>X</var>] = Var(<var>X</var>) = <var>λ</var></span><em>mean equals variance</em></span></div>
    </div>''',
 'uni': '''<div class="eq">
      <div class="line"><span class="t"><span><var>f</var>(<var>x</var>)</span></span><span class="op">=</span><span class="t b"><span><span class="frac"><i>1</i><i><var>b</var> − <var>a</var></i></span></span><em>flat height, area 1</em></span><span class="t"><span>&nbsp;for <var>a</var> ≤ <var>x</var> ≤ <var>b</var></span></span></div>
      <div class="line"><span class="t g"><span>E[<var>X</var>] = <span class="frac"><i><var>a</var> + <var>b</var></i><i>2</i></span></span><em>midpoint</em></span><span class="op">·</span><span class="t"><span>Var(<var>X</var>) = <span class="frac"><i>(<var>b</var> − <var>a</var>)<sup>2</sup></i><i>12</i></span></span><em>variance</em></span></div>
    </div>''',
}

def sub(n, sid, title, skey, eq, fig, bullets):
    lis = ''.join('<li>%s</li>' % b for b in bullets)
    return '''  <div class="subsec" id="prob-s1-%s">
    <h3 class="ssh"><b>1.%s</b>%s</h3>
    <p class="skey">%s</p>
    %s
%s
    <ul class="why">%s</ul>
  </div>
''' % (sid, n, title, skey, eq, fig, lis)

if __name__ == '__main__':
    h = open(PAGE).read()
    m = re.search(r'  <div class="subsec" id="prob-s1-3">.*?(?=  <div class="subsec" id="prob-s1-4">)', h, re.S)
    if not m:
        sys.exit('subsection 1.3 not found (already split?)')
    old = m.group(0)
    geq = re.search(r'<div class="eq">.*?</div>\s*</div>', old, re.S).group(0)
    geq = geq.replace('<div class="line">\n        <span class="t p">', '<div class="line"><span class="t g"><span>E[<var>X</var>] = <var>μ</var>,&nbsp; Var(<var>X</var>) = <var>σ</var><sup>2</sup></span><em>mean, variance</em></span></div>\n      <div class="line">\n        <span class="t p">', 1)
    intro = '''  <div class="subsec" id="prob-s1-3">
    <h3 class="ssh"><b>1.3</b>Common distributions</h3>
    <p class="skey">Five shapes cover most data: <em>one coin, a count of coins, a count of rare events, flat, and the bell</em>. Counts get bars (PMF), measurements get curves (PDF).</p>
'''
    parts = [
      ('3', '3-1', 'Bernoulli', 'One trial, <em>yes or no</em>.', EQ['bern'], bernoulli(),
       ['Binary labels are Bernoulli; its negative log-likelihood is the log loss in 4.2.']),
      ('3', '3-2', 'Binomial', 'Count the <em>yeses</em> in <var>n</var> independent trials.', EQ['bin'], binomial(),
       ['A sum of <var>n</var> Bernoullis; for large <var>n</var> it looks Gaussian (CLT, 3.2).']),
      ('3', '3-3', 'Poisson', 'Count of <em>rare events</em> in a fixed window.', EQ['poi'], poisson(),
       ['The binomial with many tries and a tiny <var>p</var>; if the variance is much bigger than the mean, the data is overdispersed.']),
      ('3', '3-4', 'Uniform', 'Every value in <span class="mth">[<var>a</var>, <var>b</var>]</span> is <em>equally likely</em>.', EQ['uni'], uniform(),
       ['Probability is width × height — the simplest picture of "area is probability".']),
      ('3', '3-5', 'Gaussian', 'The <em>bell</em>: sums of many small effects end up here.', geq, gaussian(),
       ['68–95–99.7: about 68%, 95% and 99.7% of a Gaussian lies within 1, 2 and 3 σ of μ, so <span class="mth">|<var>z</var>| &gt; 3</span> is rare.',
        'Measurement noise, linear-regression errors and weight initialisation all assume it.']),
    ]
    out = intro + '  </div>\n'
    for n, sid, title, skey, eq, fig, b in parts:
        out += sub('3.' + sid[-1], sid, title, skey, eq, fig, b).replace('<b>1.3.', '<b>1.3.')
    h = h.replace(old, out)
    open(PAGE, 'w').write(h)
    print('split ok')
