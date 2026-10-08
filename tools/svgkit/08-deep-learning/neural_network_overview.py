# -*- coding: utf-8 -*-
"""Neural network group overview (2026-10-09): a map of the group, not a lesson.

    01 The network       one annotated network: input -> layers -> output -> loss, backprop arrow back;
                         every piece labelled and linked to its lesson
    02 Remove one piece  gallery: one tile per piece, a small picture of the failure without it
    03 Learning order
The old 2.1-2.7 sections are dropped: each child lesson already teaches its failure in full.
Run: python3 tools/svgkit/08-deep-learning/neural_network_overview.py   (re-runnable)
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from overview import Fig, text, gallery, ln, arr, dot, B, V, FL, TINT, VTINT

ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
PAGE = os.path.join(ROOT, 'content/08-deep-learning/02-neural-network/neural-network-overview/index.html')
L = {'mlp': '../perceptron-mlp/index.html', 'act': '../activation-functions/index.html',
     'bp': '../backpropagation/index.html', 'init': '../weight-initialization/index.html',
     'norm': '../normalization/index.html', 'drop': '../dropout-regularization/index.html',
     'opt': '../../03-optimizer/optimizer-overview/index.html'}
R = 'var(--rose)'

def network():
    f = Fig('nnov1', 680, 380, 'ONE NETWORK · EVERY PIECE AND THE LESSON THAT OWNS IT',
            'A small network drawn left to right: three inputs, two hidden layers of four neurons, one output, '
            'then the loss. Labels point to each piece: the layers of neurons (Perceptron and MLP), the '
            'activation inside a neuron, the starting weights on the edges (Weight initialization), a '
            'normalization step between layers, a dropped neuron (Dropout and regularization), and the loss. '
            'A violet arrow runs back from the loss to the inputs: backpropagation, followed by the optimizer '
            'step that updates the weights. Each label links to its lesson.')
    xs = [70, 210, 350, 480]
    ys = [[140, 190, 240], [115, 165, 215, 265], [115, 165, 215, 265], [190]]
    e = f.step(.5, draw=True)
    edges = []
    for li in range(3):
        for y1 in ys[li]:
            for y2 in ys[li + 1]:
                edges.append(f'<line x1="{xs[li]+9}" y1="{y1}" x2="{xs[li+1]-9}" y2="{y2}" stroke="var(--rule-hi)" stroke-width=".9"/>')
    f.add(f'<g class="{f.step(.4)}">' + ''.join(edges) + '</g>')
    nodes = []
    for li, col in enumerate(ys):
        for y in col:
            drop = li == 2 and y == 215
            nodes.append(dot(xs[li], y, '×' if drop else '', hl=(li == 3), r=9) if not drop else
                         f'<circle cx="{xs[li]}" cy="{y}" r="9" fill="var(--bg)" stroke="{R}" stroke-width="1.2" stroke-dasharray="3 2"/>'
                         + text(xs[li], y + 4, '×', 'sv-d', R, 'middle', ';font-weight:700'))
    f.add(f'<g class="{f.step(.2)}">' + ''.join(nodes) + '</g>')
    # norm bands between layers
    f.add(f'<g class="{f.step(.9)}">' + ''.join(
        f'<rect x="{x-5}" y="100" width="10" height="180" rx="4" fill="rgba(var(--violet-a),.10)" stroke="var(--violet)" stroke-width="1" stroke-dasharray="3 2"/>'
        for x in (280, 415)) + '</g>')
    # loss box
    f.add(f'<g class="{f.step(1.0)}">' + arr(492, 190, 556) +
          '<rect x="560" y="170" width="96" height="40" rx="8" fill="rgba(var(--blue-a),.09)" stroke="var(--filled)" stroke-width="1.3"/>'
          + text(608, 188, 'Loss', 'sv-s', FL, 'middle', ';font-weight:600') + text(608, 202, 'L(ŷ, y)', 'sv-d', FL, 'middle', ';font-family:var(--mono)') + '</g>')
    # backprop arrow
    f.add(f'<path class="{f.step(1.6, draw=True)}" pathLength="1" d="M608,212 C608,320 300,320 72,300" fill="none" stroke="var(--violet)" stroke-width="1.8"/>')
    f.add(f'<g class="{f.step(2.1)}"><path d="M78,296 L70,300 L78,305z" fill="var(--violet)"/></g>')
    # labels (pill + leader)
    def lab(x, y, s, href, tone, tx, ty, t):
        g = ln(tx, ty, x, y + (11 if y < ty else -11), 'var(--muted)', .9, True)
        f.add(f'<g class="{f.step(t)}">' + g + '</g>')
        f.pill(x, y, s, tone, f.step(t), href, anchor='middle')
    lab(140, 60, 'Neurons in layers', L['mlp'], 'brand', 210, 104, 1.2)
    lab(290, 60, 'Normalization', L['norm'], 'violet', 280, 100, 1.3)
    lab(470, 60, 'Activation in each neuron', L['act'], 'brand', 480, 179, 1.4)
    lab(395, 350, 'Dropout · regularization', L['drop'], 'rose', 350, 226, 1.6)
    lab(110, 350, 'Weight initialization', L['init'], 'brand', 140, 212, 1.5)
    f.add(f'<g class="{f.step(2.2)}">' + text(220, 326, 'gradients flow back', 'sv-d', V, 'middle', ';font-style:italic') + '</g>')
    f.pill(608, 290, 'Backpropagation', 'violet', f.step(2.3), L['bp'], anchor='middle')
    f.pill(608, 350, 'Optimizer step', 'filled', f.step(2.5), L['opt'], anchor='middle')
    f.add(f'<g class="{f.step(2.5)}">' + ln(608, 302, 608, 338, 'var(--muted)', .9, True) + '</g>')
    f.add(f'<g class="{f.step(.3)}">' + text(70, 285, 'input', 'sv-d', 'var(--muted)', 'middle')
          + text(280, 296, 'hidden layers', 'sv-d', 'var(--muted)', 'middle') + text(480, 215, 'output ŷ', 'sv-d', 'var(--muted)', 'middle') + '</g>')
    return f.svg()

# ---- gallery tiles: each draw(x, y) fills a 138x58 box -------------------------------------
def t_layers(x, y):
    o = ''
    for i, (px, py, hl) in enumerate([(10, 10, 0), (50, 48, 0), (10, 48, 1), (50, 10, 1)]):
        o += dot(x + px + 20, y + py, '', hl, 5)
    o += ln(x + 18, y + 58, x + 92, y + 0, R, 1.4)
    o += text(x + 100, y + 32, 'XOR', 'sv-d', R, 'start', ';font-weight:600')
    return o

def t_act(x, y):
    o = ''.join(ln(x + 4, y + 52 - i * 6, x + 64, y + 22 - i * 6, B, 1) for i in range(3))
    o += text(x + 70, y + 26, '=', 'sv-s', 'var(--muted)', 'middle')
    o += ln(x + 80, y + 52, x + 134, y + 16, R, 1.6)
    o += text(x + 107, y + 58, 'still one line', 'sv-d', R, 'middle', ';font-size:9px')
    return o

def t_bp(x, y):
    o = ''
    for i in range(10):
        o += f'<rect x="{x + i*13:.1f}" y="{y + 18}" width="10" height="14" rx="2" fill="{TINT}" stroke="{B}" stroke-width="1"/>'
    o += text(x + 66, y + 50, '1 forward pass per weight', 'sv-d', R, 'middle', ';font-size:9px')
    return o

def bars(x, y, hs, col):
    return ''.join(f'<rect x="{x + i*14:.1f}" y="{y + 50 - h:.1f}" width="9" height="{h:.1f}" rx="1.5" fill="{TINT}" stroke="{col}" stroke-width="1"/>'
                   for i, h in enumerate(hs))

def t_init(x, y):
    return (bars(x, y, [40, 24, 14, 8, 4, 2, 1, .5, .5], B) + ln(x, y + 50, x + 130, y + 50, 'var(--rule-hi)')
            + text(x + 120, y + 14, 'signal → 0', 'sv-d', R, 'end', ';font-size:9px'))

def t_norm(x, y):
    return (bars(x, y, [3, 5, 8, 12, 18, 26, 36, 46, 50], R) + ln(x, y + 50, x + 130, y + 50, 'var(--rule-hi)')
            + text(x + 2, y + 14, 'doubles per layer', 'sv-d', R, 'start', ';font-size:9px'))

def t_opt(x, y):
    o = f'<ellipse cx="{x+68}" cy="{y+28}" rx="64" ry="20" fill="none" stroke="var(--rule-hi)"/>'
    o += f'<ellipse cx="{x+68}" cy="{y+28}" rx="30" ry="9" fill="none" stroke="var(--rule-hi)"/>'
    pts = [(10, 18), (40, 44), (58, 8), (84, 50), (104, 4), (128, 54)]
    o += f'<polyline points="{" ".join(f"{x+a},{y+b}" for a, b in pts)}" fill="none" stroke="{R}" stroke-width="1.3"/>'
    return o + f'<circle cx="{x+68}" cy="{y+28}" r="2" fill="{FL}"/>'

def t_drop(x, y):
    o = ln(x, y + 54, x + 134, y + 54, 'var(--rule-hi)') + ln(x, y, x, y + 54, 'var(--rule-hi)')
    o += f'<path d="M{x+2},{y+8} C{x+40},{y+40} {x+90},{y+50} {x+132},{y+52}" fill="none" stroke="{B}" stroke-width="1.3"/>'
    o += f'<path d="M{x+2},{y+12} C{x+40},{y+36} {x+70},{y+36} {x+132},{y+10}" fill="none" stroke="{R}" stroke-width="1.3"/>'
    return o + text(x + 132, y + 22, 'val', 'sv-d', R, 'end', ';font-size:9px') + text(x + 132, y + 48, 'train', 'sv-d', B, 'end', ';font-size:9px')

def failures():
    f = Fig('nnov2', 680, 0, 'REMOVE ONE PIECE · WHAT BREAKS',
            'Seven tiles, one per piece, each showing the failure when that piece is missing. No hidden layer: one '
            'straight line cannot split XOR. No activation: stacked linear layers collapse into one line. No '
            'backpropagation: one forward pass per weight to get its gradient. Bad initialization: the signal '
            'shrinks to zero layer after layer. No normalization: the signal doubles every layer. Bad optimizer '
            'step: the path zig-zags across the valley. No regularization: training loss falls while validation '
            'loss rises. Each tile links to its lesson.')
    bands = [('WITHOUT', 'click a tile for the lesson', [
        ('No hidden layer', t_layers, L['mlp']), ('No activation', t_act, L['act']),
        ('No backprop', t_bp, L['bp']), ('Bad initialization', t_init, L['init']),
        ('No normalization', t_norm, L['norm']), ('Bad step size', t_opt, L['opt']),
        ('No regularization', t_drop, L['drop'])])]
    bot = gallery(f, bands, top=40)
    f.h = bot + 6
    return f.svg()

def order():
    f = Fig('nnov3', 680, 196, 'LEARNING ORDER · EACH LESSON FIXES WHAT THE LAST ONE EXPOSES',
            'Seven stops in two rows, each a link: Perceptron and MLP, Activation functions, Backpropagation, '
            'Weight initialization, then Normalization, Optimizer, Dropout and regularization.')
    stops = [('Perceptron & MLP', 'layers', L['mlp']), ('Activation', 'bend', L['act']),
             ('Backpropagation', 'gradients', L['bp']), ('Weight init', 'start scale', L['init']),
             ('Normalization', 'steady signal', L['norm']), ('Optimizer group', 'good steps', L['opt']),
             ('Dropout · reg.', 'generalise', L['drop'])]
    w, gap = 152, 24
    for i, (n, sub, href) in enumerate(stops):
        r, c = divmod(i, 4)
        cx = c * (w + gap) + w / 2
        cy = 62 + r * 90
        if c:
            f.add(f'<line class="{f.step(.4 + i * .3, draw=True)}" pathLength="1" x1="{cx - w/2 - gap + 2}" y1="{cy}" '
                  f'x2="{cx - w/2 - 2}" y2="{cy}" stroke="var(--rule-hi)" stroke-width="1.6"/>')
        elif r:
            f.edge((3 * (w + gap) + w / 2, 84), (w / 2, cy - 22), cls=f.step(.4 + i * .3, draw=True))
        f.node(cx, cy, n, sub, 'violet' if i == 5 else 'plain', f.step(.3 + i * .3), href, None, w=w, h=44)
    return f.svg()

BODY = '''<header class="hero">
  <p class="eyebrow">Deep learning · Neural network</p>
  <h1>Neural network <em>overview</em></h1>
  <p class="lede">A deep network is neurons in layers plus a handful of fixes, each patching the failure that appears as the network gets deeper. This page is the map; every piece has its own lesson.</p>
</header>

<section id="nnov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>The network</h2></div>
  <p class="key">Inputs go forward through <em>weighted, bent layers</em> to a loss; gradients come back and the optimizer nudges every weight.</p>
<figure class="gist">
{f1}
</figure>
  <ul class="why">
    <li>Forward: each layer computes <span class="mth"><var>h</var> = σ(<var>W</var><var>x</var> + <var>b</var>)</span>. Backward: one pass gives the gradient of every weight.</li>
    <li>The optimizer has its own group: <a href="../../03-optimizer/optimizer-overview/index.html">Optimizer overview</a>.</li>
  </ul>
</section>

<section id="nnov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>What breaks without each piece</h2></div>
  <p class="key">Every piece exists because <em>something visibly fails</em> without it.</p>
<figure class="gist">
{f2}
</figure>
  <ul class="why">
    <li>The first three are about whether a network can learn at all; the last four about whether a <em>deep</em> one trains well and generalises.</li>
  </ul>
</section>

<section id="nnov-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Learning order</h2></div>
  <p class="key">Read in the order the failures appear as the network grows.</p>
<figure class="gist">
{f3}
</figure>
  <ul class="why">
    <li>Next group: CNN, starting with <a href="../../04-cnn/cnn-mobilenet/index.html">CNN &amp; MobileNet</a>.</li>
  </ul>
</section>

'''

def build():
    s = open(PAGE, encoding='utf-8').read()
    a = s.index('<header class="hero">')
    b = s.index('<script>\n/* Figures start')
    s = s[:a] + BODY.format(f1=network(), f2=failures(), f3=order()) + s[b:]
    blurb = ('The neural network group on one page: one annotated network with every piece linked to its lesson, '
             'what breaks when each piece is removed, and the order to learn them.')
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s"' % blurb, s, count=1)
    open(PAGE, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    build(); print('ok')
