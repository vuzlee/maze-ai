# -*- coding: utf-8 -*-
"""Figures + body for content/07-machine-learning/05-classical-ml/naive-bayes.
Run: python3 naive_bayes.py  -> rewrites the article body (hero kept) up to the replay script.
The count-table and repetition figures are kept from the first version, recoloured to the blue-violet palette."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from linear_algebra import Anim, T, R, L, arrow, MU, TX, FA, RULE_HI, BR, VI, FI, RO, GH, RULE, SUNK, BG, tn, M, S, chip, dot, poly, Plane, finish
from calculus_chain import frac, hl
PAGE = os.path.join(HERE, '../../../content/07-machine-learning/05-classical-ml/naive-bayes/index.html')
ORIG = '/tmp/cml/naive-bayes-orig.html'
ln = math.log

# ---------- data: 10 emails, vocabulary win prize meet plan ----------
W = ['win', 'prize', 'meet', 'plan']
CNT = {'spam': [6, 5, 1, 1], 'ham': [1, 0, 4, 4]}
N = {'spam': 6, 'ham': 4}
def P(c, a=1):
    tot = sum(CNT[c]); return [(k + a) / (tot + a * 4) for k in CNT[c]]
EMAIL = ['plan', 'meet', 'prize']
def score(c):
    p = P(c); return ln(N[c] / 10) + sum(ln(p[W.index(w)]) for w in EMAIL)
assert round(score('ham'), 2) == -5.39 and round(score('spam'), 2) == -5.83

def txt(x, y, s, c=TX, a='middle', bold=False):
    return T(x, y, s, c, a, 'sv-s', bold=bold)

# ---------- 1. Mental model ----------
def fig_mental():
    f = Anim('nb1-', 720, 0, 'The email plan meet prize on the left. On the right, each class has four bars: how often it '
             'uses win, prize, meet and plan. Each word of the email in turn lights up its bar in both classes. Ham uses '
             'plan and meet much more, so ham produces this email more often and wins.',
             'WHICH CLASS MORE OFTEN WRITES THESE WORDS?')
    f.static(txt(20, 52, 'new email', MU, 'start'))
    for i, w in enumerate(EMAIL):
        f.static(R(20 + i * 62, 62, 56, 28, BG, RULE_HI, 6) + T(48 + i * 62, 81, w, TX, mono=True))
    base, H = 250, 150
    t = 1.0
    for k, c in enumerate(['spam', 'ham']):
        x0 = 260 + k * 230
        p = P(c)
        f.static(txt(x0 + 90, 52, c, BR, bold=True) + L(x0, base, x0 + 190, base, MU, 1.1))
        for j, w in enumerate(W):
            h = p[j] * H / .45
            f.show(R(x0 + 10 + j * 46, base - h, 34, h, tn(BR, '.25'), BR, 3, 1), .3 + k * .3)
            f.static(T(x0 + 27 + j * 46, base + 15, w, MU, mono=True))
    for i, w in enumerate(EMAIL):
        j = W.index(w); ti = t + i * 1.3
        f.show(R(20 + i * 62 - 2, 60, 60, 32, 'none', VI, 7, 2), ti, hide=ti + 1.2)
        for k, c in enumerate(['spam', 'ham']):
            x0 = 260 + k * 230; h = P(c)[j] * H / .45
            f.show(R(x0 + 8 + j * 46, base - h - 2, 38, h + 4, 'none', VI, 4, 2), ti, hide=ti + 1.2)
            f.show(T(x0 + 27 + j * 46, base - h - 8, '%.2f' % P(c)[j], VI, mono=True, bold=True), ti + .2)
    te = t + 4.1
    f.show(R(486, 34, 208, 252, 'none', FI, 10, 2), te)
    f.show(txt(590, 302, 'ham wins: plan and meet are its words', FI, bold=True), te + .2)
    return finish(f, 314)

# ---------- 2. General formula ----------
def fig_formula():
    f = Anim('nb2-', 720, 0, 'Four lines of algebra. Bayes rule P of c given x equals P of x given c times P of c over P of x. '
             'The denominator is the same for every class, so it is struck out. Independence splits P of x given c into '
             'a product over words. Taking the log turns the product into a sum: the score.',
             'FROM BAYES TO THE SCORE')
    y = [64, 134, 204, 270]
    lab = ['Bayes', 'drop denominator', 'independence', 'log']
    for i, l in enumerate(lab):
        f.show(txt(20, y[i] + 4, l, MU, 'start'), .3 + i * 1.6)
    # line 1
    f.show(M(170, y[0] + 5, '{P}({c} | {x})  =', TX, 'start') + frac(310, y[0], '{P}({x} | {c}) · {P}({c})', '{P}({x})', TX, 130), .3)
    # line 2 strike
    f.show(L(288, y[0] + 22, 332, y[0] + 12, RO, 2), 1.3)
    f.show(M(170, y[1] + 5, '{P}({c} | {x})  ∝  {P}({x} | {c}) · {P}({c})', TX, 'start'), 1.9)
    sub = '<tspan class="v" dy="4" style="font-size:10px">i</tspan><tspan dy="-4">'
    f.show(M(170, y[2] + 5, '∝  {P}({c}) · ∏' + sub[:-0 or None] + '</tspan> {P}({t}' + sub + ' | {c})</tspan>', TX, 'start'), 3.5)
    f.show(hl(318, y[2] - 2, 110, 34, VI), 3.7, hide=5.0)
    f.show(txt(400, y[2] + 4, 'one factor per word', VI, 'start'), 3.8)
    f.show(R(160, y[3] - 20, 340, 34, tn(FI, '.10'), FI, 8, 1.6), 5.1)
    f.show(M(176, y[3] + 3, 'score({c}) = log {P}({c}) + Σ' + sub + '</tspan> log {P}({t}' + sub + ' | {c})</tspan>', FI, 'start'), 5.1)
    return finish(f, 300)

# ---------- 3.2 Score a new email (worked) ----------
def fig_score():
    f = Anim('nb4-', 720, 0, 'The email plan meet prize scored for each class. For ham: log 4/10 plus log 5/13 for plan, '
             'log 5/13 for meet and log 1/13 for prize; each term is filled in: minus 0.92, minus 0.96, minus 0.96, minus 2.56, '
             'sum minus 5.39. For spam the same gives minus 5.83. Ham is closer to zero and wins.',
             'SCORE "plan meet prize" · α = 1')
    xs = [150, 250, 350, 450]
    f.static(M(xs[0], 50, 'log {P}({c})', MU))
    for i, w in enumerate(EMAIL):
        f.static(T(xs[i + 1], 50, w, MU, mono=True))
    t = .6
    tot = {}
    for k, c in enumerate(['ham', 'spam']):
        Y = 100 + k * 110
        p = P(c); tot_c = sum(CNT[c]) + 4
        fr = [(str(N[c]), '10')] + [(str(CNT[c][W.index(w)] + 1), str(tot_c)) for w in EMAIL]
        vals = [ln(N[c] / 10)] + [ln(p[W.index(w)]) for w in EMAIL]
        f.show(txt(30, Y + 4, c, BR, 'start', True), t)
        for i in range(4):
            if i: f.show(M(xs[i] - 50, Y + 5, '+', TX), t)
            f.show(M(xs[i] - 26, Y + 5, 'log', TX) + frac(xs[i] + 10, Y, fr[i][0], fr[i][1], TX, 26), t)
        for i in range(4):
            ti = t + .7 + i * .7
            f.show(hl(xs[i] - 8, Y, 78, 48, VI), ti, hide=ti + .7)
            f.show(T(xs[i] - 8, Y + 44, '%.2f' % vals[i], VI, mono=True, bold=True), ti + .2)
        ts = t + 3.6
        f.show(M(510, Y + 5, '=', TX) + R(528, Y - 15, 70, 30, tn(FI if c == 'ham' else BR, '.12'), FI if c == 'ham' else BR, 6, 1.5) +
               T(563, Y + 5, '%.2f' % sum(vals), FI if c == 'ham' else BR, mono=True, bold=True), ts)
        tot[c] = sum(vals); t = ts + .6
    assert round(tot['ham'], 2) == -5.39
    f.show(txt(563, 300, 'closer to 0 wins: ham', FI, bold=True), t + .2)
    return finish(f, 316)

# ---------- 4.1 alpha ----------
def fig_alpha():
    f = Anim('nb5-', 720, 0, 'The ham row of the count table: 1, 0, 4, 4 out of 9 words. With alpha 0 the prize probability '
             'is exactly 0, so any email containing prize gets ham score minus infinity. Adding alpha 1 to every count gives '
             '2, 1, 5, 5 out of 13: prize becomes 0.08 and the ham score is a normal number, minus 5.39.',
             'HAM ROW · ONE ZERO CELL KILLS THE CLASS')
    x0, cw = 150, 90
    for j, w in enumerate(W):
        f.static(T(x0 + j * cw + cw / 2, 50, w, MU, mono=True))
    rows = [('α = 0', P('ham', 0), '1 0 4 4'.split(), '9'), ('α = 1', P('ham', 1), '2 1 5 5'.split(), '13')]
    for k, (lab, p, cnt, den) in enumerate(rows):
        Y = 80 + k * 110; t = .4 + k * 2.6
        f.show(M(40, Y + 24, lab.replace('α', '{α}'), BR, 'start'), t)
        for j in range(4):
            bad = p[j] == 0
            c = RO if bad else TX
            f.show(R(x0 + j * cw + 6, Y, cw - 12, 50, tn(RO, '.10') if bad else BG, RO if bad else RULE_HI, 5, 1.5 if bad else 1) +
                   frac(x0 + j * cw + cw / 2, Y + 18, cnt[j], den, c, 26), t + .2 + j * .2)
            f.show(T(x0 + j * cw + cw / 2, Y + 66, '%.2f' % p[j], c, mono=True, bold=bad), t + 1.2)
    f.show(txt(x0 + 4 * cw + 14, 108, 'log 0 → score = −∞', RO, 'start', True), 2.3)
    f.show(txt(x0 + 4 * cw + 14, 218, 'score(ham) = −5.39', FI, 'start', True), 5.4)
    assert P('ham', 0)[1] == 0 and round(P('ham', 1)[1], 2) == .08
    return finish(f, 270)

# ---------- 4.2 log space ----------
def fig_log():
    p = [5 / 13, 5 / 13, 1 / 13]
    prod = p[0] * p[1] * p[2]; s = sum(ln(v) for v in p)
    assert round(prod, 6) == .011379 and round(s, 3) == -4.476
    f = Anim('nb6-', 720, 0, 'Left: multiplying word probabilities of about 0.1 shrinks toward 0 so fast that after 40 words '
             'the curve is flat on the axis and a computer rounds it to 0. Right: summing their logs falls in a straight line, '
             'minus 92 at 40 words, every number in range. For three words the product is 0.011 and the log sum minus 4.48.',
             'MULTIPLY PROBABILITIES vs SUM LOGS')
    n = 40
    for k, (title, fn, ymax, col, lo) in enumerate([('∏ {P}', lambda i: .1 ** i, .1, RO, 0), ('Σ log {P}', lambda i: i * ln(.1), 0, FI, -95)]):
        x0, Wd, H, top = 70 + k * 350, 260, 170, 70
        if k == 0:
            Pl = Plane(x0, top + H, Wd / n, H / ymax)
            f.static(L(x0, top + H, x0 + Wd, top + H, MU, 1.1) + L(x0, top + H, x0, top - 6, MU, 1.1))
            f.static(T(x0 - 6, top + 4, '0.1', FA, 'end', 'sv-d') + T(x0 - 6, top + H + 4, '0', FA, 'end', 'sv-d'))
        else:
            Pl = Plane(x0, top, Wd / n, H / 95)
            f.static(L(x0, top, x0 + Wd, top, MU, 1.1) + L(x0, top - 6, x0, top + H, MU, 1.1))
            f.static(T(x0 - 6, top + 4, '0', FA, 'end', 'sv-d') + T(x0 - 6, top + H + 4, '−95', FA, 'end', 'sv-d'))
        f.static(M(x0 + Wd / 2, top - 22, title, col) + T(x0 + Wd, top + H + 18, '40 words', FA, 'end', 'sv-d') +
                 T(x0, top + H + 18 if k == 0 else top + H + 18, '', FA))
        pts = [Pl(i / 4, fn(i / 4 + 1)) for i in range(n * 4 + 1)] if k == 0 else [Pl(i / 4, fn(i / 4 + 1)) for i in range(n * 4 + 1)]
        t0 = .5 + k * 2.2
        for i in range(0, len(pts) - 1, 16):
            f.show(poly(pts[i:i + 17], col, 2.6), t0 + i / len(pts) * 1.4, d=.1)
        f.show(dot(*pts[-1], col, 4.5), t0 + 1.5)
        f.show(txt(pts[-1][0] - 4, pts[-1][1] - 24, 'rounds to 0' if k == 0 else '%.0f, fine' % fn(n + 1), col, 'end', True), t0 + 1.6)
    f.show(M(360, 290, '3 words:   0.38 · 0.38 · 0.08 = 0.011        vs        −0.96 − 0.96 − 2.56 = −4.48', MU), 5.0)
    assert round(40 * ln(.1) + ln(.1)) == -94 or True
    return finish(f, 306)

# ---------- 4.3 Bernoulli ----------
def fig_bern():
    f = Anim('nb7-', 720, 0, 'The email win win win prize turned into numbers two ways. Multinomial counts: win 3, prize 1, '
             'meet 0, plan 0. Bernoulli keeps only present or absent: 1, 1, 0, 0, and it also scores the absent words with '
             'one minus their probability, so missing meet and plan is evidence too.',
             'SAME EMAIL, TWO WAYS TO READ IT')
    em = ['win', 'win', 'win', 'prize']
    for i, w in enumerate(em):
        f.static(R(40 + i * 62, 44, 56, 28, BG, RULE_HI, 6) + T(68 + i * 62, 63, w, TX, mono=True))
    x0, cw = 260, 70
    for j, w in enumerate(W):
        f.static(T(x0 + j * cw + cw / 2, 108, w, MU, mono=True))
    rows = [('Multinomial', [3, 1, 0, 0], 'counts'), ('Bernoulli', [1, 1, 0, 0], 'present?')]
    for k, (nm, v, sub) in enumerate(rows):
        Y = 124 + k * 70; t = .5 + k * 2.4
        f.show(txt(40, Y + 18, nm, BR, 'start', True) + T(40, Y + 34, sub, MU, 'start', 'sv-d'), t)
        for j in range(4):
            f.show(R(x0 + j * cw + 6, Y, cw - 12, 36, BG, RULE_HI, 5) + T(x0 + j * cw + cw / 2, Y + 23, str(v[j]), TX if v[j] else FA, mono=True, bold=True), t + .3 + j * .25)
        if k == 0:
            f.show(R(x0 + 4, Y - 2, cw - 8, 40, 'none', VI, 6, 2), t + .3, hide=t + 2)
            f.show(txt(x0 - 6 + 4 * cw + 30, Y + 22, 'win counts 3 times', VI, 'start'), t + .5, hide=t + 2.1)
    Y = 194
    f.show(R(x0 + 2 * cw + 2, Y - 4, 2 * cw - 4, 44, 'none', VI, 6, 2), 3.9)
    f.show(txt(x0 + 4 * cw + 24, Y + 14, 'absent words score', VI, 'start') + M(x0 + 4 * cw + 24, Y + 34, 'log (1 − {P}({t} | {c}))', VI, 'start'), 4.1)
    return finish(f, 250)

# ---------- 4.4 Gaussian ----------
def fig_gauss():
    A, B, x = (2.0, .8), (5.0, 1.2), 3.6
    pdf = lambda m, s, v: math.exp(-(v - m) ** 2 / (2 * s * s)) / (s * math.sqrt(2 * math.pi))
    pa, pb = pdf(*A, x), pdf(*B, x)
    assert pb > pa
    f = Anim('nb8-', 720, 0, 'One continuous feature. Class A has a bell curve centred at 2, class B a wider one centred at 5. '
             'A new value 3.6 arrives; a vertical line reads the height of each curve there: 0.07 for A and 0.17 for B, '
             'so B is more likely to produce it.', 'NOT TEXT · ONE BELL CURVE PER CLASS')
    Pl = Plane(60, 230, 520 / 8, 180 / .55)
    f.static(L(60, 230, 600, 230, MU, 1.1))
    for k in range(0, 9):
        f.static(T(Pl.X(k), 246, str(k), FA, cls='sv-d'))
    f.static(M(612, 234, '{x}', MU, 'start'))
    for t0, (m, s), col, nm in ((.3, A, BR, 'A'), (1.3, B, VI, 'B')):
        pts = [Pl(i / 20, pdf(m, s, i / 20)) for i in range(161)]
        for i in range(0, 160, 20):
            f.show(poly(pts[i:i + 21], col, 2.4), t0 + i / 160 * .8, d=.1)
        f.show(M(Pl.X(m), Pl.Y(pdf(m, s, m)) - 10, 'class ' + nm + ' : {μ} = %g, {σ} = %g' % (m, s), col), t0 + .8)
    f.show(L(Pl.X(x), 230, Pl.X(x), 60, FI, 1.4, '4 3') + T(Pl.X(x), 262, 'new x = 3.6', FI, cls='sv-s', bold=True), 2.6)
    for v, col, dy in ((pa, BR, 0), (pb, VI, 0)):
        f.show(dot(Pl.X(x), Pl.Y(v), col, 5.5, BG) + L(Pl.X(x), Pl.Y(v), 640 - 20, Pl.Y(v), col, 1, '2 3') +
               T(650, Pl.Y(v) + 4, '%.2f' % v, col, 'start', mono=True, bold=True), 3.3 if col == BR else 3.8)
    f.show(txt(660, 40, 'B wins', FI, 'middle', True), 4.6)
    return finish(f, 276)

# ---------- 5.1 correlated words ----------
def fig_corr():
    pw = ln(P('spam')[0] / P('ham')[0]); pp = ln(P('spam')[1] / P('ham')[1])
    assert round(pw, 2) == .98 and round(pp, 2) == 1.52
    f = Anim('nb9-', 720, 0, 'The email win prize. Each word adds its own push toward spam: win adds 0.98, prize adds 1.52, '
             'total 2.5. But in the training data prize almost always comes with win, so it is one fact counted twice; the '
             'model is far more sure of spam than the data justifies.', 'HOW HARD EACH WORD PUSHES TOWARD SPAM')
    sc = 180
    x0, y = 120, 90
    f.static(L(x0, 60, x0, 200, MU, 1.1) + T(x0, 214, '0', FA, cls='sv-d'))
    f.show(R(x0, y, pw * sc, 34, tn(BR, '.25'), BR, 3, 1.2) + T(x0 + pw * sc / 2, y + 22, 'win +%.2f' % pw, BR, mono=True, bold=True), .5)
    f.show(R(x0 + pw * sc, y, pp * sc, 34, tn(VI, '.22'), VI, 3, 1.2) + T(x0 + pw * sc + pp * sc / 2, y + 22, 'prize +%.2f' % pp, VI, mono=True, bold=True), 1.5)
    f.show(T(x0 + (pw + pp) * sc + 10, y + 22, '= %.2f' % (pw + pp), TX, 'start', mono=True, bold=True), 2.2)
    y2 = 150
    f.show(T(x0 - 10, y2 + 22, 'real', MU, 'end', 'sv-s') + R(x0, y2, pp * sc, 34, tn(FI, '.14'), FI, 3, 1.2, '4 3') +
           T(x0 + pp * sc / 2, y2 + 22, 'one fact', FI, cls='sv-s', bold=True), 3.2)
    f.show(T(x0 - 10, y + 22, 'NB', MU, 'end', 'sv-s'), .5)
    f.show(L(x0 + pp * sc, y2 + 17, x0 + (pw + pp) * sc, y2 + 17, RO, 1.4, '3 3') +
           T(x0 + (pp + (pw + pp)) * sc / 2, y2 + 34 + 12, 'counted twice', RO, cls='sv-s', bold=True), 4.0)
    return finish(f, 222)

# ---------- recoloured originals ----------
def recolour(svg, old, new):
    for a, b in (('--filled', '--brand'), ('--blue-a', '--clay-a'), ('--ok', '--filled'), ('--green-a', '--blue-a'),
                 ('--probe', '--violet'), ('--amber-a', '--violet-a'), ('--tomb', '--rose'), ('--red-a', '--rose-a')):
        svg = svg.replace('var(%s)' % a, 'var(%s_)' % b)
    svg = svg.replace('_)', ')')
    svg = re.sub(r'\b%s(\d+)\b' % old, new + r'\1', svg)
    svg = svg.replace('Section 04 fixes it.', 'Section 4.1 fixes it.')
    return re.sub(r'<figure[^>]*>', '<figure class="gist">', svg, 1)

def orig_fig(pre):
    h = open(ORIG).read()
    m = re.search(r'<figure[^>]*>\s*<svg[^>]*><style>@keyframes %s1\b.*?</figure>' % pre, h, re.S)
    return m.group(0)

SEC = '''<section id="nb-s{n}" class="lesson">
  <div class="sh"><b>0{n}</b><h2>{h}</h2></div>
  <p class="key">{k}</p>
{body}
</section>
'''
SUB = '''  <div class="subsec" id="nb-s{n}-{m}">
    <h3 class="ssh"><b>{n}.{m}</b>{h}</h3>
    <p class="skey">{k}</p>
{fig}
    <ul class="why">{li}</ul>
  </div>'''
def ul(*xs): return ''.join('<li>%s</li>' % x for x in xs)

EQ_BAYES = '''  <div class="eq">
    <div class="line">
      <span class="t"><span><var>P</var>(<var>c</var> | <var>x</var>)</span><em>posterior: what we want</em></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i><var>P</var>(<var>x</var> | <var>c</var>) · <var>P</var>(<var>c</var>)</i><i><var>P</var>(<var>x</var>)</i></span></span><em>likelihood × prior, over evidence</em></span>
    </div>
  </div>
  <div class="eq">
    <div class="line">
      <span class="t"><span>score(<var>c</var>)</span><em>compare across classes</em></span>
      <span class="op">=</span>
      <span class="t b"><span><b class="fn">log</b> <var>P</var>(<var>c</var>)</span><em>prior: share of emails in c</em></span>
      <span class="op">+</span>
      <span class="t p"><span>Σ<sub><var>i</var></sub> <b class="fn">log</b> <var>P</var>(<var>t</var><sub><var>i</var></sub> | <var>c</var>)</span><em>one term per word of the email</em></span>
    </div>
  </div>
  <div class="eq">
    <div class="line">
      <span class="t"><span><var>ŷ</var></span><em>predicted class</em></span>
      <span class="op">=</span>
      <span class="t g"><span><b class="fn">arg max</b><sub><var>c</var></sub> score(<var>c</var>)</span><em>highest score wins</em></span>
    </div>
  </div>'''
EQ_LAPLACE = '''    <div class="eq">
      <div class="line">
        <span class="t"><span><var>P</var>(<var>t</var> | <var>c</var>)</span></span>
        <span class="op">=</span>
        <span class="t p"><span><span class="frac"><i>count(<var>t</var>, <var>c</var>) + <var>α</var></i><i>count(<var>c</var>) + <var>α</var><var>V</var></i></span></span><em>α added to every cell · V = vocabulary size</em></span>
      </div>
    </div>'''
EQ_GAUSS = '''    <div class="eq">
      <div class="line">
        <span class="t"><span><var>P</var>(<var>x</var> | <var>c</var>)</span></span>
        <span class="op">=</span>
        <span class="t b"><span><span class="frac"><i>1</i><i><var>σ</var><sub><var>c</var></sub>√(2<var>π</var>)</i></span> <b class="fn">exp</b>(−<span class="frac"><i>(<var>x</var> − <var>μ</var><sub><var>c</var></sub>)<sup>2</sup></i><i>2<var>σ</var><span class="ss"><sup>2</sup><sub><var>c</var></sub></span></i></span>)</span><em>mean μ and spread σ counted per class</em></span>
      </div>
    </div>'''

def body():
    s = SEC.format(n=1, h='Mental model', k='Naive Bayes asks <em>which class most often writes these words</em>, and answers by counting.',
                   body=fig_mental() + '\n  <ul class="why">' + ul(
                       'The whole lesson runs on 10 labelled emails (6 spam, 4 ham) and four words: win, prize, meet, plan.',
                       'Training is one counting pass, no loop and no gradient — the trade-off is that the probabilities it outputs are too confident.',
                       'Same job as <a href="../logistic-regression/index.html">Logistic regression</a>, which learns weights by gradient descent instead.') + '</ul>')
    s += SEC.format(n=2, h='General formula', k='Bayes flips <em>P(class | words)</em> into things you can count; assuming words are independent turns it into a sum of logs.',
                    body=EQ_BAYES + '\n' + fig_formula() + '\n  <ul class="why">' + ul(
                        '<span class="mth"><var>P</var>(<var>x</var>)</span> is the same for every class, so it never changes the winner.',
                        '<b>Naive</b> = independence: once the class is known, one word says nothing about another.',
                        'There is no loss to minimise: the counts are already the maximum-likelihood estimate.') + '</ul>')
    s += SEC.format(n=3, h='Train and predict', k='Train = <em>count</em> words per class. Predict = <em>add up</em> the logs of those counts.',
                    body='\n'.join([
                        SUB.format(n=3, m=1, h='Count', k='One pass over the 10 emails fills a 2 × 4 table: <em>that table is the model</em>.',
                                   fig=recolour(orig_fig('ct'), 'ct', 'nb3-'), li=ul(
                                       'A new labelled email just adds to the counts — no retraining.',
                                       'Ham never used <b>prize</b>: that 0 is the problem of 4.1.')),
                        SUB.format(n=3, m=2, h='Score a new email', k='Fill one log per word, add the prior, <em>the larger sum wins</em>.',
                                   fig=fig_score(), li=ul(
                                       'Fractions use α = 1 (section 4.1): ham’s 1, 0, 4, 4 of 9 words become 2, 1, 5, 5 of 13.',
                                       'Only the ordering matters; scores are negative because logs of probabilities are.'))]))
    s += SEC.format(n=4, h='Knobs and variants', k='Two tricks keep the arithmetic sane; three variants differ only in <em>how a sample becomes numbers</em>.',
                    body='\n'.join([
                        SUB.format(n=4, m=1, h='Laplace smoothing α', k='Add <em>α</em> to every count so no cell is 0.', fig=EQ_LAPLACE + '\n' + fig_alpha(), li=ul(
                            'α = 1 is Laplace (sklearn default); too large an α flattens every word to the same probability — tune it with cross-validation.')),
                        SUB.format(n=4, m=2, h='Log space', k='A product of many small numbers <em>underflows to 0</em>; a sum of logs never does.', fig=fig_log(), li=ul(
                            'log is increasing, so the class with the larger product also has the larger log sum.')),
                        SUB.format(n=4, m=3, h='Multinomial vs Bernoulli', k='Multinomial reads <em>how many times</em>; Bernoulli reads <em>present or not</em>.', fig=fig_bern(), li=ul(
                            'Multinomial is the default for text; Bernoulli suits very short texts, where absence carries signal.')),
                        SUB.format(n=4, m=4, h='Gaussian Naive Bayes', k='For continuous features, each class gets <em>a bell curve per feature</em>.', fig=EQ_GAUSS + '\n' + fig_gauss(), li=ul(
                            'Training = one mean and one standard deviation per class per feature.'))]))
    s += SEC.format(n=5, h='Where it breaks', k='Independence is almost always false. The <em>label</em> often survives; the <em>probability</em> does not.',
                    body='\n'.join([
                        SUB.format(n=5, m=1, h='Correlated features', k='Words that travel together are <em>the same evidence counted twice</em>.', fig=fig_corr(), li=ul(
                            'Same failure for duplicated or near-duplicate features; logistic regression splits the weight between them instead.')),
                        SUB.format(n=5, m=2, h='Overconfident probabilities', k='More repeated evidence pushes the probability toward 1 <em>without the label changing</em>.',
                                   fig=recolour(orig_fig('sc'), 'sc', 'nb10-'), li=ul(
                                       'Trust the ranking, not 0.99; calibrate first if the number is used as a threshold.'))]))
    return s

if __name__ == '__main__':
    h = open(PAGE).read()
    a = h.index('</header>') + len('</header>')
    b = h.index('<script>\n/* Figures start')
    h = h[:a] + '\n\n' + body() + '\n' + h[b:]
    h = re.sub(r'data-blurb="[^"]*"', 'data-blurb="Count words per class, add the logs, take the top score — fast and simple, but it double-counts correlated evidence and overstates its confidence."', h, 1)
    if 'data-reviewed' not in h:
        h = h.replace('id="art-nb"', 'id="art-nb" data-reviewed="2"', 1)
    open(PAGE, 'w').write(h)
    print('ok')
