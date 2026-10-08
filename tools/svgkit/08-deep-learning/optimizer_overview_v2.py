# -*- coding: utf-8 -*-
"""Optimizer group overview (2026-10-09): the family at a glance, not the lessons themselves.

    01 Family tree      top-down: gradient descent -> SGD -> momentum / AdaGrad -> RMSProp -> Adam -> AdamW
    02 Race             the four optimizers on the shared toy valley, same 12 steps, side by side
    03 Comparison       what each keeps in memory, its knobs, where it is used
    04 Learning order
Run: python3 tools/svgkit/08-deep-learning/optimizer_overview_v2.py   (re-runnable)
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, os.path.join(HERE, '../dsa'))
from overview import Fig, text
import optimizer_overview as O          # shared toy valley, runs and Surf
from engine import Anim
from linear_algebra import finish, S, M, BR, VI, FI, RO
from tablefig import T, R, L, MU, TX, FA

ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
PAGE = os.path.join(ROOT, 'content/08-deep-learning/03-optimizer/optimizer-overview/index.html')
L_ = {'sgd': '../sgd/index.html', 'mom': '../momentum/index.html', 'rms': '../adagrad-rmsprop/index.html',
      'adam': '../adam/index.html', 'adamw': '../adamw/index.html'}


def family():
    f = Fig('opov1', 680, 486, 'FAMILY TREE · EACH OPTIMIZER FIXES ONE PROBLEM OF ITS PARENT',
            'A top-down family tree of optimizers. At the top, gradient descent: step against the gradient of all '
            'rows. Below it SGD with mini-batches, cheaper steps. SGD splits into two branches: momentum, which '
            'remembers past steps so zig-zags cancel, and AdaGrad, which gives every weight its own step size; '
            'AdaGrad leads to RMSProp, which forgets old gradients so steps do not shrink forever. The two branches '
            'join in Adam, momentum plus RMSProp. Adam leads to AdamW, which takes weight decay out of the Adam '
            'division. Each arrow is labelled with the problem it fixes. Every box links to its lesson.')
    P = {'gd': (340, 58), 'sgd': (340, 140), 'mom': (170, 226), 'ada': (510, 226), 'rms': (510, 290),
         'adam': (340, 372), 'adamw': (340, 458)}
    W = 168
    def E(a, b, t, note, side='start', dx=8, col='var(--rule-hi)'):
        (x1, y1), (x2, y2) = P[a], P[b]
        f.edge((x1, y1 + 22), (x2, y2 - 22), cls=f.step(t, draw=True), col=col)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + 4
        f.add(f'<g class="{f.step(t + .3)}">' + text(mx + dx, my, note, 'sv-d', 'var(--violet)', side, ';font-style:italic') + '</g>')
    E('gd', 'sgd', .6, 'every row per step is slow')
    E('sgd', 'mom', 1.3, 'zig-zags across the valley', 'end', -14)
    E('sgd', 'ada', 1.3, 'one step size for all weights', 'start', 14)
    E('ada', 'rms', 2.0, 'steps shrink forever')
    E('mom', 'adam', 2.7, 'combine both', 'end', -30, 'var(--violet)')
    f.edge((P['rms'][0], P['rms'][1] + 22), (P['adam'][0] + 40, P['adam'][1] - 22), cls=f.step(2.7, draw=True), col='var(--violet)')
    f.edge((P['adam'][0], P['adam'][1] + 22), (P['adamw'][0], P['adamw'][1] - 22), cls=f.step(3.4, draw=True))
    f.add(f'<g class="{f.step(3.7)}">' + text(352, 419, 'L2 decay gets divided by √v', 'sv-d', 'var(--violet)', 'start', ';font-style:italic') + '</g>')
    a = f.step(.2)
    f.node(*P['gd'], 'Gradient descent', 'w ← w − η · ∇L', 'filled', a, None, None, w=W + 20)
    f.node(*P['sgd'], 'SGD · mini-batch', 'gradient on a few rows', 'plain', f.step(.9), L_['sgd'], None, w=W)
    b = f.step(1.6)
    f.node(*P['mom'], 'Momentum', 'remember past steps', 'plain', b, L_['mom'], None, w=W)
    f.node(*P['ada'], 'AdaGrad', 'a step size per weight', 'plain', b, L_['rms'], None, w=W)
    f.node(*P['rms'], 'RMSProp', 'forget old gradients', 'plain', f.step(2.3), L_['rms'], None, w=W)
    f.node(*P['adam'], 'Adam', 'momentum + RMSProp', 'violet', f.step(3.0), L_['adam'], None, w=W)
    f.node(*P['adamw'], 'AdamW', 'decay outside Adam', 'violet', f.step(3.9), L_['adamw'], None, w=W)
    f.add(f'<g class="{f.step(4.2)}">' + text(0, 384, '2012 → 2017: Hinton’s RMSProp, Kingma & Ba’s Adam (2014), Loshchilov & Hutter’s AdamW',
                                             'sv-d', 'var(--faint)', 'start', ';font-size:9.5px') + '</g>') if False else None
    return f.svg()


def race():
    runs = [('SGD', O.GD2, FA, L_['sgd']), ('Momentum', O.MOM, BR, L_['mom']),
            ('RMSProp', O.RMS, FI, L_['rms']), ('Adam', O.ADAM, VI, L_['adam'])]
    f = Anim('opov2-', 720, 0, 'Four copies of the same loss valley seen from above, the long thin valley shared by every '
             'Optimizer lesson. From the same start each optimizer takes twelve steps at the same time. Plain SGD '
             'zig-zags across the valley and creeps along it. Momentum overshoots, then swings in along the floor. '
             'RMSProp turns straight down the long axis. Adam moves a fixed distance per step and heads for the '
             'minimum. Under each panel is the loss after twelve steps.',
             'SAME VALLEY · SAME START · 12 STEPS EACH')
    pw, ph, gap = 165, 150, 10
    for i, (name, path, c, href) in enumerate(runs):
        x = i * (pw + gap)
        sf = O.Surf('opov2-%d' % i, x, 40, pw, ph)
        body = sf.svg(levels=(.02, .07, .16, .32, .6, 1.0, 1.6, 2.6))
        # drop the axis labels Surf adds under/left of the panel
        body = body[:body.rindex('<text')] if False else body
        body = re.sub(r'<text[^>]*>(?:(?!</text>).)*?₁ →</text>', '', body)
        body = re.sub(r'<text[^>]*>(?:(?!</text>).)*?₂</text>', '', body)
        f.static(body)
        f.static(T(x + 8, 34, name, c if c != FA else TX, 'start', 'sv-s', bold=True))
        O.walk(f, sf, path, c, 1.0, .45, r=5, trail=2)
        lv = O.loss(path[-1])
        f.show(T(x + pw / 2, 40 + ph + 20, 'loss %s' % O.f4(lv), c if c != FA else MU, 'middle', mono=True, bold=True), 1.0 + 12 * .45)
    f.static(T(0, 40 + ph + 44, 'start loss %s · each ball = one optimizer, one step every 0.45 s' % O.f2(O.loss(O.W0)), MU, 'start'))
    out = finish(f, 40 + ph + 52)
    return out[out.index('<svg'):out.rindex('</svg>') + 6]


def table():
    rows = [('SGD', 'nothing', 'η', 'rarely alone', L_['sgd']),
            ('SGD + momentum', 'velocity v', 'η, β ≈ 0.9', 'CNNs on images', L_['mom']),
            ('RMSProp', 'squared avg s', 'η, β ≈ 0.9', 'RNNs, RL (older)', L_['rms']),
            ('Adam', 'm and v', 'η, β₁ 0.9, β₂ 0.999', 'default to start', L_['adam']),
            ('AdamW', 'm and v', '+ decay λ ≈ 0.01–0.1', 'Transformers, LLMs', L_['adamw'])]
    f = Fig('opov3', 680, 248, 'WHICH ONE TO USE', 'A comparison table of five optimizers with what each keeps in memory '
            'per weight, its main settings, and where it is the usual choice: SGD keeps nothing; SGD with momentum keeps a '
            'velocity and is still standard for CNNs; RMSProp keeps a squared average; Adam keeps two averages and is the '
            'default to start with; AdamW adds decoupled weight decay and is the standard for Transformers and LLMs.')
    cols = [(0, 'OPTIMIZER'), (176, 'KEEPS PER WEIGHT'), (330, 'SETTINGS'), (504, 'USUAL HOME')]
    for x, h in cols:
        f.add(text(x + 10, 44, h, 'sv-hv', 'var(--muted)', 'start'))
    f.add('<line x1="0" y1="54" x2="680" y2="54" stroke="var(--rule-hi)"/>')
    for i, (a, b, c, d, href) in enumerate(rows):
        y = 64 + i * 36
        hl = a == 'AdamW'
        cls = f.step(.3 + i * .3)
        inner = (f'<rect class="nd" x="0" y="{y}" width="680" height="32" rx="7" '
                 f'fill="{"rgba(var(--violet-a),.08)" if hl else "var(--bg)"}" stroke="{"var(--violet)" if hl else "var(--rule)"}"/>'
                 + text(10, y + 20, a, 'sv-s', 'var(--violet)' if hl else 'var(--brand-hi)', 'start', ';font-weight:600')
                 + text(186, y + 20, b, 'sv-d', 'var(--text)', 'start', ';font-family:var(--mono)')
                 + text(340, y + 20, c, 'sv-d', 'var(--text)', 'start', ';font-family:var(--mono)')
                 + text(514, y + 20, d, 'sv-d', 'var(--violet)' if hl else 'var(--muted)', 'start', ';font-weight:600' if hl else ''))
        f.add(f'<g class="{cls}"><a href="{href}">{inner}</a></g>')
    return f.svg()


def order():
    f = Fig('opov4', 680, 104, 'LEARNING ORDER · EACH LESSON ADDS ONE IDEA TO THE LAST',
            'Five stops in a row, each a link: SGD and mini-batch, momentum, AdaGrad and RMSProp, Adam, AdamW.')
    stops = [('SGD & mini-batch', 'step · batch · rate', L_['sgd']), ('Momentum', '+ memory', L_['mom']),
             ('AdaGrad · RMSProp', '+ per-weight size', L_['rms']), ('Adam', 'both together', L_['adam']),
             ('AdamW', '+ clean decay', L_['adamw'])]
    w, gap = 126, 12.5
    for i, (n, sub, href) in enumerate(stops):
        cx = i * (w + gap) + w / 2
        if i:
            f.add(f'<line class="{f.step(.4 + i * .35, draw=True)}" pathLength="1" x1="{cx - w - gap + w/2 + 2}" y1="62" '
                  f'x2="{cx - w/2 - 2}" y2="62" stroke="var(--rule-hi)" stroke-width="1.6"/>')
        f.node(cx, 62, n, sub, 'violet' if i == 4 else 'plain', f.step(.3 + i * .35), href, None, w=w, h=44)
    return f.svg()


BODY = '''<header class="hero">
  <p class="eyebrow">Deep learning · Optimizer</p>
  <h1>Optimizer <em>overview</em></h1>
  <p class="lede">Backprop gives the gradient; an <b>optimizer</b> turns it into a step. Five optimizers, each fixing one problem of the one before — from plain SGD to <b>AdamW</b>, the default for LLMs.</p>
</header>

<section id="optim-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Family tree</h2></div>
  <p class="key">Two ideas grow out of SGD — <em>remember past steps</em> and <em>a step size per weight</em> — and Adam joins them.</p>
<figure class="gist">
{f1}
</figure>
  <ul class="why">
    <li>Every optimizer still computes the same gradient from <a href="../../02-neural-network/backpropagation/index.html">Backpropagation</a>; they differ only in how that gradient becomes a step.</li>
    <li>Variants you will meet by name — Nesterov, AMSGrad, Adafactor, Lion — are small changes to one box on this tree.</li>
  </ul>
</section>

<section id="optim-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Same valley, four paths</h2></div>
  <p class="key">On a long thin valley the difference is visible at a glance: <em>SGD zig-zags, adaptive steps go straight down the floor</em>.</p>
<figure class="gist">
{f2}
</figure>
  <ul class="why">
    <li>The valley is the toy every lesson in this group uses: one weight's direction is 8.5× steeper than the other's — the shape that makes optimizers differ.</li>
    <li>Fastest here is not best everywhere: tuned SGD + momentum often generalises a little better on image models.</li>
  </ul>
</section>

<section id="optim-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Which one to use</h2></div>
  <p class="key">Start with <em>AdamW + warmup + cosine decay</em>; reach for SGD + momentum only when a CNN recipe says so.</p>
<figure class="gist">
{f3}
</figure>
  <ul class="why">
    <li>Adam-style optimizers keep two numbers per weight, so they need about 3× the weight memory — the reason 8-bit optimizers exist for large models.</li>
    <li>The learning rate matters more than the choice of optimizer; its schedule is in <a href="../sgd/index.html#sgd-s4">SGD &amp; mini-batch</a>.</li>
  </ul>
</section>

<section id="optim-s4" class="lesson">
  <div class="sh"><b>04</b><h2>Learning order</h2></div>
  <p class="key">Read in the order the ideas were invented: <em>each lesson adds one idea</em> to the last.</p>
<figure class="gist">
{f4}
</figure>
</section>

'''


def build():
    s = open(PAGE, encoding='utf-8').read()
    a = s.index('<header class="hero">')
    b = s.index('<script>\n/* Figures start')
    body = BODY.format(f1=family(), f2=race(), f3=table(), f4=order())
    s = s[:a] + body + s[b:]
    blurb = ('The optimizer family on one page: a top-down tree from SGD through momentum, AdaGrad and RMSProp to Adam '
             'and AdamW, four optimizers racing on one valley, and which one to use.')
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s"' % blurb, s, count=1)
    s = re.sub(r'<footer>.*?</footer>', '<footer>Deep learning · Optimizer · first lesson: '
               '<a href="../sgd/index.html">SGD &amp; mini-batch</a>.</footer>', s, count=1, flags=re.S)
    open(PAGE, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    build(); print('ok')
