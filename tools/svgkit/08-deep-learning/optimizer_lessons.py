# -*- coding: utf-8 -*-
"""Thicken four Optimizer lessons (2026-10-09) with one new section each, on the shared toy valley.

    momentum         + Nesterov momentum       (after Velocity)
    adagrad-rmsprop  + AdaGrad                 (before RMSProp)
    adam             + Adam vs SGD             (after Adam update)
    adamw            + L2 inside Adam          (before Decoupled weight decay)

Toy, optimisers and drawing helpers come from tools/svgkit/dsa/optimizer_overview.py (imported, not
modified). Every number drawn is computed here and pinned with assert. Re-runnable: sections are
matched by their h2 title, the new one is inserted or replaced, then ids and numbers are rewritten.

    python3 tools/svgkit/08-deep-learning/optimizer_lessons.py
"""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'dsa'))
from optimizer_overview import (D, grad, loss, run, mom, rms, W0, N, Surf, walk, ghost, side_eq, f2, f3, f4, MLR, RLR, RMS, RE)
from linear_algebra import Anim, T, R, L, arrow, MU, TX, FA, BR, VI, FI, RO, RULE, RULE_HI, BG, tn, M, S, dot, finish
DIR = os.path.abspath(os.path.join(HERE, '../../../content/08-deep-learning/03-optimizer'))

def clean(svg):   # Surf marks the minimum with --ok; new figures keep to the blue palette
    svg = svg.replace('var(--ok)', BR).replace('var(--probe)', VI)
    assert not re.search(r'--(ok|probe|tomb|amber-a|green-a|red-a)\b|#[0-9a-fA-F]{3,6}\b', svg)
    return svg

# ---------- Nesterov ----------
NB = .7
def nesterov(lr, b, log):
    def f(w, g, s, t):
        v = s.get('v', (0, 0)); la = (w[0] - lr * b * v[0], w[1] - lr * b * v[1]); gg = grad(la, D)
        v = (b * v[0] + gg[0], b * v[1] + gg[1]); s['v'] = v; log.append(la)
        return (w[0] - lr * v[0], w[1] - lr * v[1])
    return f
LA = []
NES, _ = run(nesterov(MLR, NB, LA))
MOM7, _ = run(mom(MLR, NB))
assert round(loss(NES[-1]), 4) == .0045 and round(loss(MOM7[-1]), 4) == .0413

def fig_nesterov():
    f = Anim('optn-', 720, 0, 'The same valley. Grey dashed: plain momentum, rate 1.5, beta 0.7, which swings past the floor and '
             'back. Violet: Nesterov momentum with the same settings. At each step a hollow dot marks the look-ahead point, where '
             'the old velocity would carry the ball, and the gradient is read there; the ball then steps. Reading the slope ahead '
             'brakes before the overshoot: loss after 12 steps 0.0045 against 0.0413.', 'READ THE GRADIENT WHERE THE VELOCITY IS TAKING YOU')
    sf = Surf('optn-', 20, 34, 300, 260)
    f.static(sf.svg() + sf.legend(330))
    f.show(ghost(sf, MOM7) + S(sf.x + 150, 330, '- - plain momentum', FA), .3)
    X = 380
    side_eq(f, X, 56, ['{w̃} = {w} − {η}{β}{v}', '{v} ← {β}{v} + ∇{L}({w̃})', '{w} ← {w} − {η}{v}'])
    f.static(S(X, 132, 'η = 1.5 · β = 0.7 · same as the grey run', MU))
    dt, t0 = .8, 1.2
    for k in range(1, N + 1):
        tk = t0 + (k - 1) * dt; last = k == N
        a = sf.P(*NES[k - 1]); la = sf.P(*LA[k - 1])
        if k > 1 and sf.inside(LA[k - 1]):
            f.show(L(a[0], a[1], la[0], la[1], VI, 1.2, '3 3') +
                   '<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s" stroke="%s" stroke-width="1.6"/>' % (la[0], la[1], BG, VI),
                   tk - .45, hide=tk + .45, d=.2)
        f.show(R(X, 150, 300, 22, BG, 'none') + T(X, 166, 'step %d · look ahead, then step' % k, MU, 'start', 'sv-s', bold=True),
               tk - .45, hide=None if last else tk + dt - .45, d=.15)
    walk(f, sf, NES, VI, t0, dt)
    te = t0 + N * dt
    f.show(S(X, 220, 'loss after 12 steps, same η and β', MU) +
           T(X, 242, 'plain momentum  %s' % f4(loss(MOM7[-1])), FA, 'start', mono=True) +
           T(X, 262, 'Nesterov        %s' % f4(loss(NES[-1])), VI, 'start', mono=True, bold=True), te)
    return clean(finish(f, 346))

# ---------- AdaGrad ----------
def adagrad(lr, keep):
    def f(w, g, s, t):
        v = s.get('s', (0, 0)); v = tuple(v[i] + g[i] ** 2 for i in range(2)); s['s'] = v
        keep.append(tuple(lr / math.sqrt(v[i]) for i in range(2)))
        return tuple(w[i] - lr * g[i] / (math.sqrt(v[i]) + 1e-8) for i in range(2))
    return f
AE = []
ADA, _ = run(adagrad(RLR, AE))
assert round(loss(ADA[-1]), 3) == .589 and round(loss(RMS[-1]), 4) == .0071
assert round(AE[0][1], 2) == .72 and round(AE[-1][1], 2) == .28 and round(RE[-1][1], 2) == 2.53
assert all(AE[i][j] > AE[i + 1][j] for i in range(N - 1) for j in range(2))   # AdaGrad steps only shrink

def fig_adagrad():
    f = Anim('opta-', 720, 0, 'The valley. Grey dashed: RMSProp, rate 0.3. Violet: AdaGrad, same rate, which divides by the root of '
             'the SUM of all past squared gradients. On the right two bars track the effective step of w2: AdaGrad\'s starts at '
             '0.72 and only shrinks, to 0.28 at step 12; RMSProp\'s averages and grows to 2.53. AdaGrad stalls half way down the '
             'valley with loss 0.589.', 'ADAGRAD SUMS EVERY SQUARE · ITS STEPS CAN ONLY SHRINK')
    sf = Surf('opta-', 20, 34, 300, 260)
    f.static(sf.svg() + sf.legend(330))
    f.show(ghost(sf, RMS) + S(sf.x + 150, 330, '- - RMSProp', FA), .3)
    X = 380
    side_eq(f, X, 56, ['{s} ← {s} + (∇{L})²', '{w} ← {w} − ({η} / √{s}) ∇{L}'])
    f.static(S(X, 110, 'η = 0.3 · effective step for w₂:', MU))
    BX, BW = X + 80, 180; sc = BW / 3
    for j, (yy, lab) in enumerate(((140, 'AdaGrad'), (186, 'RMSProp'))):
        f.static(S(X, yy + 13, lab, VI if j == 0 else MU, bold=j == 0) + R(BX, yy, BW, 18, BG, RULE, 3, 1))
    for v in (1, 2, 3): f.static(L(BX + v * sc, 136, BX + v * sc, 208, RULE, .8, '2 3') + T(BX + v * sc, 224, str(v), FA, mono=True))
    dt, t0 = .8, 1.2
    for k in range(1, N + 1):
        tk = t0 + (k - 1) * dt - .4; last = k == N; s = ''
        for j, (yy, e, c) in enumerate(((140, AE[k - 1][1], VI), (186, min(RE[k - 1][1], 3), FA))):
            s += (R(BX, yy, e * sc, 18, tn(VI, '.30') if j == 0 else 'var(--sunk)', c, 3, 1.2) + R(BX + BW + 4, yy, 44, 18, BG, 'none') +
                  T(BX + BW + 8, yy + 13, f2(AE[k - 1][1] if j == 0 else RE[k - 1][1]), c, 'start', mono=True, bold=True))
        f.show(s, tk, hide=None if last else tk + dt, d=.2)
        f.show(R(X, 240, 120, 18, BG, 'none') + T(X, 254, 'step %d' % k, MU, 'start', 'sv-s', bold=True), tk,
               hide=None if last else tk + dt - .05, d=.15)
    walk(f, sf, ADA, VI, t0, dt)
    f.show(T(X, 286, 'loss after 12: AdaGrad %s · RMSProp %s' % (f3(loss(ADA[-1])), f4(loss(RMS[-1]))), TX, 'start', mono=True), t0 + N * dt)
    return clean(finish(f, 346))

# ---------- Adam vs SGD: memory ----------
PARAMS = 7e9; BYTES = 4
OPTS = [('SGD', ['w', 'g']), ('SGD + momentum', ['w', 'g', 'v']), ('Adam / AdamW', ['w', 'g', 'm', 'v'])]
GB = {n: len(c) * PARAMS * BYTES / 1e9 for n, c in OPTS}
assert GB['SGD'] == 56 and GB['SGD + momentum'] == 84 and GB['Adam / AdamW'] == 112

def fig_adam_sgd():
    f = Anim('optm-', 720, 0, 'Numbers kept per weight during training. Plain SGD keeps the weight and its gradient. SGD with momentum '
             'adds one velocity. Adam adds two: m and v. For a 7-billion-weight model in 32-bit floats every number per weight '
             'costs 28 GB, so the three need 56, 84 and 112 GB before any activations.', 'NUMBERS KEPT PER WEIGHT · ADAM PAYS 2 EXTRA')
    cw, gap, X0 = 52, 8, 190
    for i, (name, cells) in enumerate(OPTS):
        y = 50 + i * 62; t = .4 + i * 1.2
        f.show(T(0, y + 26, name, TX, 'start', 'sv-s', bold=True), t)
        for j, c in enumerate(cells):
            extra = c in ('m', 'v')
            col = VI if extra else (FI if c == 'g' else BR)
            f.show(R(X0 + j * (cw + gap), y, cw, 38, tn(col, '.18' if extra else '.10'), col, 5, 1.6 if extra else 1) +
                   M(X0 + j * (cw + gap) + cw / 2, y + 25, '{%s}' % c, col), t + .2 + j * .2)
        f.show(T(X0 + 4 * (cw + gap) + 30, y + 25, '%d × 28 GB = %d GB' % (len(cells), GB[name]), VI if i == 2 else TX, 'start',
                 mono=True, bold=i == 2), t + 1.0)
    f.static(S(0, 248, '7B weights × 4 bytes = 28 GB per number kept · activations not counted', MU))
    return clean(finish(f, 262))

# ---------- L2 inside Adam ----------
def l2_run(sig, w=1.0, lam=.1, lr=.01, n=100, b1=.9, b2=.999):
    m = v = 0; out = [w]; root = []
    for t in range(1, n + 1):
        g = sig * (1 if t % 2 else -1) + lam * w
        m = b1 * m + (1 - b1) * g; v = b2 * v + (1 - b2) * g * g; vh = v / (1 - b2 ** t); root.append(math.sqrt(vh))
        w = w - lr * (m / (1 - b1 ** t)) / (math.sqrt(vh) + 1e-8); out.append(w)
    return out, root
LA_, LA_R = l2_run(1); LB_, LB_R = l2_run(.01)
assert round(LA_[-1], 3) == .890 and round(LB_[-1], 3) == .230
assert round(LA_R[-1], 2) == 1.00 and round(LB_R[-1], 3) == .062

def fig_l2():
    f = Anim('optl-', 720, 0, 'Two weights start at 1.0. Both get the same L2 penalty 0.1 times w added to their gradient, and Adam '
             'divides the whole gradient by its running size √v. Weight a has large gradients, so √v stays about 1.00 and the '
             'penalty is divided by 1: a only shrinks to 0.890 in 100 steps. Weight b has tiny gradients, √v is about 0.062, so '
             'its penalty is multiplied about sixteen-fold and b collapses to 0.230.', 'THE PENALTY GOES THROUGH THE ADAM DIVISION')
    f.static(M(0, 48, '{g} = ∇{L} + 0.1 {w}     step = {η} · {m̂} / √{v̂}', TX, 'start'))
    BX, BW = 200, 330
    marks = [0, 25, 50, 75, 100]
    for j, (lab, path, root, c) in enumerate((('a · big gradients', LA_, LA_R, FI), ('b · tiny gradients', LB_, LB_R, RO))):
        yy = 96 + j * 70
        f.static(S(0, yy + 14, lab, TX, bold=True) + R(BX, yy, BW, 22, BG, RULE, 3, 1))
        for v in (.25, .5, .75, 1): f.static(L(BX + v * BW, yy - 2, BX + v * BW, yy + 24, RULE, .8, '2 3'))
        for k, st in enumerate(marks):
            w = path[st]; t = .6 + k * 1.1; last = k == len(marks) - 1
            f.show(R(BX, yy, w * BW, 22, tn(c, '.25'), c, 3, 1.3) + R(BX + BW + 6, yy, 60, 22, BG, 'none') +
                   T(BX + BW + 10, yy + 16, f3(w), c, 'start', mono=True, bold=True), t, hide=None if last else t + 1.1, d=.25)
        f.show(S(BX, yy + 42, '√v ≈ %s → penalty ÷ %s' % (f3(root[-1]) if root[-1] < .5 else f2(root[-1]),
                                                         f3(root[-1]) if root[-1] < .5 else f2(root[-1])), c, bold=True), 1.2)
    for v in (0, .5, 1): f.static(T(BX + v * BW, 252, '%g' % v, FA, mono=True))
    for k, st in enumerate(marks):
        t = .6 + k * 1.1
        f.show(R(BX, 70, 200, 18, BG, 'none') + T(BX, 84, 'after %d steps' % st, VI, 'start', 'sv-s', bold=True), t,
               hide=None if k == len(marks) - 1 else t + 1.1, d=.2)
    return clean(finish(f, 262))

# ---------- section bodies ----------
NES_SEC = '''  <p class="key"><em>Nesterov</em> reads the gradient at the look-ahead point the velocity is heading for, so it brakes before it overshoots.</p>
{fig}
  <ul class="why">
    <li>Same two numbers to tune as momentum (<span class="mth"><var>η</var></span>, <span class="mth"><var>β</var></span>); the only change is <i>where</i> the gradient is read.</li>
    <li>It helps most when <span class="mth"><var>β</var></span> is large: here at <span class="mth"><var>β</var></span> = 0.7 plain momentum overshoots the floor, Nesterov does not.</li>
    <li>In PyTorch: <code>torch.optim.SGD(params, lr, momentum=0.9, nesterov=True)</code>.</li>
  </ul>'''
ADA_SEC = '''  <p class="key"><em>AdaGrad</em> divides each weight's step by the root of the <em>sum</em> of all its past squared gradients — the first per-weight step size.</p>
{fig}
  <ul class="why">
    <li>The sum never forgets, so every step is smaller than the last; on a long run it stalls before the minimum.</li>
    <li>Still useful for sparse features (rare words, embeddings): a weight that rarely gets a gradient keeps a large step.</li>
    <li>RMSProp, next, keeps the per-weight idea but swaps the sum for a decaying average.</li>
  </ul>'''
ASGD_SEC = '''  <p class="key"><em>Adam</em> converges fast with little tuning; <em>SGD + momentum</em> is cheaper in memory and often generalises a little better.</p>
{fig}
  <ul class="why">
    <li>Adam wins on transformers, LLMs, sparse or badly scaled gradients and short tuning budgets — the default for new models.</li>
    <li>SGD + momentum wins on image CNNs (ResNet on ImageNet): with a tuned schedule it often reaches slightly higher test accuracy — the <b>generalisation gap</b>; AdamW narrows it.</li>
    <li>Adam keeps two extra numbers per weight (<span class="mth"><var>m</var></span>, <span class="mth"><var>v</var></span>); at LLM scale that is why 8-bit optimizers and sharded optimizer state exist.</li>
  </ul>'''
L2_SEC = '''  <p class="key">Adding the L2 penalty <span class="mth">λ<var>w</var></span> to the gradient sends it through Adam's division, so <em>weights with big gradients barely decay</em>.</p>
{fig}
  <ul class="why">
    <li>The penalty is meant to be the same pull toward 0 for every weight; dividing by √<var>v̂</var> makes it weak exactly where gradients are large.</li>
    <li>This is what <code>torch.optim.Adam(weight_decay=…)</code> does — the setting looks like weight decay but is L2 inside Adam.</li>
    <li>The fix, next, takes the decay out of the gradient.</li>
  </ul>'''

def sections(s):
    return [(m.group(0), re.search(r'<h2>(.*?)</h2>', m.group(0)).group(1)) for m in
            re.finditer(r'<section id="[^"]*" class="lesson">.*?</section>\n?', s, re.S)]

def patch(d, slug, new_title, body, fig, where):
    page = os.path.join(DIR, d, 'index.html'); s = open(page, encoding='utf-8').read()
    secs = sections(s); assert secs
    a = s.index(secs[0][0]); b = s.index(secs[-1][0]) + len(secs[-1][0])
    keep = [(x, t) for x, t in secs if t != new_title]
    new = ('<section id="X" class="lesson">\n  <div class="sh"><b>00</b><h2>%s</h2></div>\n%s\n</section>\n'
           % (new_title, body.replace('{fig}', fig)), new_title)
    keep.insert(where if where >= 0 else len(keep), new)
    out = []
    for i, (x, t) in enumerate(keep, 1):
        x = re.sub(r'<section id="[^"]*"', '<section id="%s-s%d"' % (slug, i), x, count=1)
        x = re.sub(r'<div class="sh"><b>\d+</b>', '<div class="sh"><b>%02d</b>' % i, x, count=1)
        out.append(x.rstrip('\n') + '\n')
    s = s[:a] + '\n'.join(out) + s[b:]
    open(page, 'w', encoding='utf-8').write(s)
    print(d, [t for _, t in keep])

if __name__ == '__main__':
    patch('momentum', 'mom', 'Nesterov momentum', NES_SEC, fig_nesterov(), -1)
    patch('adagrad-rmsprop', 'rms', 'AdaGrad', ADA_SEC, fig_adagrad(), 0)
    patch('adam', 'adam', 'Adam vs SGD', ASGD_SEC, fig_adam_sgd(), -1)
    patch('adamw', 'adamw', 'L2 inside Adam', L2_SEC, fig_l2(), 0)
