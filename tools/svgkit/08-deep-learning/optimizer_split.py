# -*- coding: utf-8 -*-
"""Split the old all-in-one Optimizer overview into its five lessons (2026-10-09).

The old page taught every optimizer itself while sgd/momentum/adagrad-rmsprop/adam/adamw were empty
skeletons. This moves each section, with its figure and words unchanged, to the lesson that owns it.
Figures still come from tools/svgkit/dsa/optimizer_overview.py (one shared toy valley), so the five
lessons share the same picture. Run once on the old page:

    python3 tools/svgkit/08-deep-learning/optimizer_split.py <old-overview.html>
"""
import re, sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
DIR = os.path.join(ROOT, 'content/08-deep-learning/03-optimizer')

src = open(sys.argv[1], encoding='utf-8').read()


def block(start_pat, end_pat):
    a = src.index(start_pat)
    b = src.index(end_pat, a)
    return src[a:b]


def sub(sid):
    """Inner content of a .subsec (without the wrapper and its h3)."""
    a = src.index(f'<div class="subsec" id="{sid}">')
    a = src.index('</h3>', a) + 5
    # subsec ends at the next subsec or section end
    nxt = [i for i in (src.find('<div class="subsec"', a), src.find('</section>', a)) if i > 0]
    b = min(nxt)
    body = src[a:b].rstrip()
    assert body.endswith('</div>')
    return body[:-6].strip('\n')


def skey_to_key(s):
    return s.replace('<p class="skey">', '<p class="key">', 1)


S1 = block('<section id="optim-s1"', '</section>')            # mental model: valley + 12 GD steps
EQ_GD = block('  <div class="eq">', '  <div class="subsec" id="optim-s2-1">')
EQ_GD = EQ_GD[:EQ_GD.rindex('</div>') + 6] if False else EQ_GD
s2_mini, s2_lr, s2_sched = sub('optim-s2-1'), sub('optim-s2-2'), sub('optim-s2-3')
s3_mom, s3_rms, s3_adam = sub('optim-s3-1'), sub('optim-s3-2'), sub('optim-s3-3')
S4 = block('<section id="optim-s4"', '</section>')
s4_inner = S4[S4.index('</div>') + 6:]                         # drop the sh header

TOY = ('<li>The toy shared by the whole Optimizer group: eight rows, a model <span class="mth"><var>ŷ</var> = '
       '<var>w</var><sub>1</sub><var>x</var><sub>1</sub> + <var>w</var><sub>2</sub><var>x</var><sub>2</sub></span>, mean squared '
       'error. <var>x</var><sub>2</sub> has a third of the spread of <var>x</var><sub>1</sub>, so the loss is a long thin valley — '
       'the shape that makes optimizers differ.</li>')


def sec(slug, n, title, inner):
    return f'<section id="{slug}-s{n}" class="lesson">\n  <div class="sh"><b>{n:02d}</b><h2>{title}</h2></div>\n{inner}\n</section>\n'


def lesson(slug, d, sections, foot):
    page = os.path.join(DIR, d, 'index.html')
    s = open(page, encoding='utf-8').read()
    a = s.index('</header>') + len('</header>')
    b = s.index('<footer>')
    s = s[:a] + '\n\n' + '\n'.join(sec(slug, i + 1, t, x) for i, (t, x) in enumerate(sections)) + '\n' + REPLAY + '\n\n' + s[b:]
    s = re.sub(r'<footer>.*?</footer>', f'<footer>{foot}</footer>', s, count=1, flags=re.S)
    s = s.replace(' data-skeleton="1"', '')
    s = re.sub(r'\s*<p class="wip">.*?</p>', '', s, count=1)
    open(page, 'w', encoding='utf-8').write(s)


REPLAY = src[src.index('<script>\n/* Figures start'):src.index('</script>', src.index('<script>\n/* Figures start')) + 9]
OV = 'Deep learning · Optimizer · overview: <a href="../optimizer-overview/index.html">Optimizer overview</a>'

# --- sgd: mental model (12 GD steps) + mini-batch + learning rate + schedule
mental = S1[S1.index('</div>') + 6:]
mental = mental.replace('<li>The toy for the whole lesson:', '<li>The toy for the whole Optimizer group:')
mental = mental.replace('this lesson only decides what to do with it', 'an optimizer only decides what to do with it')
gd_sec = ('  <p class="key">Step against the gradient: <em>which rows</em> it is computed on and <em>how far</em> to step are the two knobs.</p>\n'
          + EQ_GD[EQ_GD.index('  <div class="eq">'):].rstrip() + '\n'
          + skey_to_key(s2_mini))
lesson('sgd', 'sgd', [('Mental model', mental), ('Mini-batch', gd_sec),
                      ('Learning rate', skey_to_key(s2_lr)), ('Learning-rate schedule', skey_to_key(s2_sched))],
       OV + ' · next: <a href="../momentum/index.html">Momentum</a>.')

# --- momentum
lesson('mom', 'momentum', [('Velocity', skey_to_key(s3_mom))],
       OV + ' · previous: <a href="../sgd/index.html">SGD &amp; mini-batch</a> · next: '
       '<a href="../adagrad-rmsprop/index.html">AdaGrad &amp; RMSProp</a>.')

# --- adagrad / rmsprop
lesson('rms', 'adagrad-rmsprop', [('RMSProp', skey_to_key(s3_rms))],
       OV + ' · previous: <a href="../momentum/index.html">Momentum</a> · next: <a href="../adam/index.html">Adam</a>.')

# --- adam
lesson('adam', 'adam', [('Adam update', skey_to_key(s3_adam))],
       OV + ' · previous: <a href="../adagrad-rmsprop/index.html">AdaGrad &amp; RMSProp</a> · next: '
       '<a href="../adamw/index.html">AdamW</a>.')

# --- adamw
lesson('adamw', 'adamw', [('Decoupled weight decay', s4_inner.strip('\n'))],
       OV + ' · previous: <a href="../adam/index.html">Adam</a>.')
print('split ok')
