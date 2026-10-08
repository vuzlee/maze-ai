# -*- coding: utf-8 -*-
"""Deep learning shelf overview v2: gallery of the field's classic pictures (section 01).

Sections 02-04 (learned features, history timeline, learning order) keep the figures drawn by
tools/svgkit/dsa/dl_overview.py; this script only replaces the svg in dlov-s1.

    python3 tools/svgkit/08-deep-learning/dl_overview_v2.py
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from overview import Fig, text, gallery, cell, dot, ln, arr, B, V, FL, TINT, VTINT

PAGE = 'content/08-deep-learning/01-overview/dl-overview/index.html'
NN = '../../02-neural-network/'
M = ';font-size:8.5px'

def t(x, y, s, col='var(--muted)', a='middle', ex=M):
    return text(x, y, s, 'sv-d', col, a, ex)
def path(d, col=V, w=1.6, dash=False):
    ds = ' stroke-dasharray="3 2"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}"{ds}/>'

def d_neuron(x, y):
    o = ''
    for i, yy in enumerate((8, 29, 50)):
        o += ln(x + 14, y + yy, x + 70, y + 29, B) + dot(x + 10, y + yy, '', False, 6)
        
    o += dot(x + 76, y + 29, 'Σ', True, 11) + arr(x + 88, y + 29, x + 116, V)
    return o + t(x + 128, y + 32, 'y', V) + t(x + 40, y + 62, 'Σ wᵢxᵢ + b', 'var(--muted)')
def d_mlp(x, y):
    L = [(10, 3), (52, 4), (94, 4), (132, 2)]
    pos = [[(x + lx, y + 29 + (j - (n - 1) / 2) * 15) for j in range(n)] for lx, n in L]
    o = ''
    for a, b in zip(pos, pos[1:]):
        o += ''.join(ln(*p, *q, 'var(--rule-hi)', .8) for p in a for q in b)
    for k, layer in enumerate(pos):
        o += ''.join(dot(px, py, '', k == 3, 5) for px, py in layer)
    return o
def d_act(x, y):
    o = ln(x + 2, y + 44, x + 136, y + 44, 'var(--rule-hi)') + ln(x + 69, y + 2, x + 69, y + 58, 'var(--rule-hi)')
    o += path(f'M{x+4},{y+44} L{x+69},{y+44} L{x+120},{y+4}', B, 1.8)
    o += path('M' + ' L'.join(f'{x+4+i*2.6:.1f},{y+44-30/(1+math.exp(-(i*2.6-65)/9)):.1f}' for i in range(51)), V, 1.8)
    return o + t(x + 100, y + 8, 'ReLU', B, 'end') + t(x + 4, y + 30, 'sigmoid', V, 'start')
def d_backprop(x, y):
    xs = [10, 52, 94, 128]
    o = ''
    for i, px in enumerate(xs):
        o += f'<rect x="{x+px-9}" y="{y+8}" width="18" height="20" rx="4" fill="{TINT}" stroke="{B}" stroke-width="1.1"/>'
        if i < 3:
            o += arr(x + px + 11, y + 18, x + xs[i + 1] - 11, 'var(--muted)')
            o += arr(x + xs[i + 1] - 11, y + 42, x + px + 11, V)
    o += t(x + 69, y + 4, 'forward', 'var(--muted)') + t(x + 69, y + 56, '∂loss flows back', V)
    return o + t(x + 124, y + 21, 'L', B, 'middle', ';font-size:9px;font-weight:600')
def d_conv(x, y):
    o = ''
    for r in range(4):
        for c in range(5):
            o += cell(x + 2 + c * 13, y + 3 + r * 13, 12, 12)
    o += f'<rect x="{x+15}" y="{y+17}" width="38" height="38" rx="3" fill="rgba(var(--violet-a),.14)" stroke="{V}" stroke-width="1.6"/>'
    o += arr(x + 70, y + 30, x + 92, V)
    for r in range(2):
        for c in range(3):
            o += cell(x + 96 + c * 13, y + 17 + r * 13, 12, 12, '', (r, c) == (1, 1))
    return o + t(x + 34, y + 66, '3×3 filter slides')
def d_rnn(x, y):
    o = ''
    for i in range(4):
        cx = x + 14 + i * 36
        o += f'<rect x="{cx-12}" y="{y+18}" width="24" height="20" rx="4" fill="{TINT}" stroke="{B}" stroke-width="1.1"/>'
        o += t(cx, y + 31.5, 'h', B) + ln(cx, y + 50, cx, y + 39, 'var(--muted)') + t(cx, y + 60, f'x{i+1}', 'var(--faint)')
        if i < 3:
            o += arr(cx + 12, y + 28, cx + 24, V)
    return o + t(x + 69, y + 10, 'same weights, every step', V)
def d_lstm(x, y):
    o = path(f'M{x+2},{y+14} H{x+136}', V, 2) + t(x + 136, y + 4, 'cell state', V, 'end')
    for i, (g, lab) in enumerate((('×', 'forget'), ('+', 'input'), ('×', 'output'))):
        cx = x + 26 + i * 44
        o += ln(cx, y + 14, cx, y + 34, 'var(--rule-hi)')
        o += dot(cx, y + 14, g, i == 0, 7)
        o += f'<rect x="{cx-17}" y="{y+36}" width="34" height="14" rx="3" fill="{VTINT if i == 0 else TINT}" stroke="{V if i == 0 else B}" stroke-width="1"/>'
        o += t(cx, y + 46, lab, V if i == 0 else 'var(--text)', 'middle', ';font-size:8px')
    return o
def d_gen(x, y):
    # autoencoder bottleneck
    o = f'<path d="M{x+2},{y+4} L{x+30},{y+20} L{x+30},{y+38} L{x+2},{y+54}z" fill="{TINT}" stroke="{B}" stroke-width="1.1"/>'
    o += f'<rect x="{x+32}" y="{y+22}" width="8" height="14" rx="2" fill="{VTINT}" stroke="{V}" stroke-width="1.1"/>'
    o += f'<path d="M{x+42},{y+20} L{x+70},{y+4} L{x+70},{y+54} L{x+42},{y+38}z" fill="{TINT}" stroke="{B}" stroke-width="1.1"/>'
    o += t(x + 36, y + 66, 'autoencoder')
    # GAN two nets
    o += f'<rect x="{x+84}" y="{y+6}" width="22" height="18" rx="4" fill="{TINT}" stroke="{B}" stroke-width="1.1"/>' + t(x + 95, y + 18.5, 'G', B, 'middle', ';font-size:9px;font-weight:600')
    o += f'<rect x="{x+114}" y="{y+34}" width="22" height="18" rx="4" fill="{VTINT}" stroke="{V}" stroke-width="1.1"/>' + t(x + 125, y + 46.5, 'D', V, 'middle', ';font-size:9px;font-weight:600')
    o += path(f'M{x+106},{y+15} C{x+124},{y+15} {x+125},{y+22} {x+125},{y+33}', 'var(--muted)', 1.1)
    o += path(f'M{x+113},{y+43} C{x+95},{y+43} {x+95},{y+36} {x+95},{y+25}', V, 1.1, True)
    return o + t(x + 110, y + 66, 'GAN')

def fig_gallery():
    f = Fig('dlov1', 680, 380, 'THE WHOLE SHELF · EIGHT PICTURES EVERY DEEP LEARNING COURSE DRAWS',
            'A gallery of eight pictures. A single neuron: three inputs times weights summed into one output. '
            'A multilayer perceptron: layers of neurons fully connected. Activation curves: ReLU and sigmoid. '
            'Backpropagation: a forward pass left to right and gradients of the loss flowing back right to left. '
            'Convolution: a three by three filter sliding over a grid to make a smaller feature map. A recurrent '
            'network unrolled over four time steps with the same weights. An LSTM cell: a cell state line with '
            'forget, input and output gates. Generative models: an autoencoder squeezing through a bottleneck, and '
            'a GAN where a generator and a discriminator play against each other. Tiles whose lesson is written '
            'link to it.')
    bands = [('THE CORE', 'every network needs these', [
        ('Neuron', d_neuron, NN + 'perceptron-mlp/index.html'),
        ('MLP · layers', d_mlp, NN + 'neural-network-overview/index.html'),
        ('Activation', d_act, NN + 'activation-functions/index.html'),
        ('Backpropagation', d_backprop, NN + 'backpropagation/index.html')]),
        ('LAYERS FOR EACH DATA SHAPE', 'images, sequences, generation', [
        ('CNN · filter', d_conv, '../../04-cnn/cnn-mobilenet/index.html'),
        ('RNN · unrolled', d_rnn, None),
        ('LSTM gates', d_lstm, None),
        ('Autoencoder · GAN', d_gen, None)])]
    f.h = gallery(f, bands) + 6
    return f.svg()

def put(html, sec_id, svg):
    i = html.index(f'id="{sec_id}"')
    a = html.index('<svg', i)
    b = html.index('</svg>', a) + 6
    return html[:a] + svg + html[b:]

if __name__ == '__main__':
    s = open(PAGE, encoding='utf-8').read()
    s = put(s, 'dlov-s1', fig_gallery())
    open(PAGE, 'w', encoding='utf-8').write(s)
    print('ok')
