# -*- coding: utf-8 -*-
"""Targeted additions to the linear-algebra page: 3.4 Linear layer, 3.5 Transpose & inverse,
L1 norm eq in 2.1, covariance eq in 5.2. Run once: python3 linear_algebra_fix.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from linear_algebra import *

def fig_layer():
    f = Anim('la12-', 720, 0, 'A linear layer. The input x has 3 numbers. W has 2 rows of 3 weights. Row 1 of W times x, plus b1, '
             'gives y1; row 2 times x, plus b2, gives y2. Shapes: (2 by 3) times (3 by 1) plus (2 by 1) gives (2 by 1).',
             'A LINEAR LAYER · EACH ROW OF W MAKES ONE OUTPUT')
    W = [[1, 0, 2], [-1, 3, 1]]; x = [2, 1, 1]; b = [1, 0]
    y = [sum(W[i][j] * x[j] for j in range(3)) + b[i] for i in range(2)]
    wx, wy, cw, ch = 40, 60, 40, 32
    f.show(matrix(wx, wy, W, cw, ch, '{W}') + T(wx + 60, wy + 90, '2 × 3', MU, mono=True), .3)
    xx = 210
    f.show(M(190, wy + 37, '·', MU) + matrix(xx, wy - 16, [[v] for v in x], cw, ch, '{x}', BR) + T(xx + 20, wy + 106, '3 × 1', MU, mono=True), .9)
    bx = 300
    f.show(M(280, wy + 37, '+', MU) + matrix(bx, wy, [[v] for v in b], cw, ch, '{b}') + T(bx + 20, wy + 90, '2 × 1', MU, mono=True), 1.5)
    yx = 410
    f.static(M(380, wy + 37, '=', MU))
    t = 2.3
    for i in range(2):
        f.show(R(wx - 3, wy + i * ch - 3, 3 * cw + 6, ch + 6, 'none', VI, 5, 2) + R(xx - 3, wy - 19, cw + 6, 3 * ch + 6, 'none', VI, 5, 2), t, t + 1.6)
        terms = ' + '.join('%d·%d' % (W[i][j], x[j]) for j in range(3))
        f.show(S(500, wy + 20 + i * 34, '%s + %d = %d' % (terms, b[i], y[i]), VI), t + .5, t + 1.6)
        f.show(mcell(yx, wy + i * ch, y[i], cw, ch, FI, tn(FI)), t + 1.1)
        t += 2
    f.show(M(yx + 20, wy - 9, '{y}', FI) + T(yx + 20, wy + 90, '2 × 1', FI, mono=True, bold=True), t)
    f.show(S(500, wy + 37, '3 inputs → 2 outputs', FI, bold=True), t + .4)
    f.show(S(0, 200, 'a batch stacks n inputs as rows: Y = XWᵀ + b, shape (n × 3)(3 × 2) → (n × 2)', MU), t + 1)
    return finish(f, 214)

def fig_transpose():
    f = Anim('la13-', 720, 0, 'Transpose. A is 2 by 3. Each entry at row i, column j slides to row j, column i, flipping across the '
             'diagonal; the result is 3 by 2. Entries on the diagonal stay put. Then A times its inverse gives the identity I.',
             'TRANSPOSE · FLIP ACROSS THE DIAGONAL')
    A = [[1, 2, 3], [4, 5, 6]]; cw = ch = 38; ox, oy = 60, 60
    for i in range(3):
        for j in range(3):
            f.static(R(ox + j * cw, oy + i * ch, cw, ch, 'none', RULE, 2, 1, '3 3'))
    f.static(M(ox + 57, oy - 12, '{A}  (2 × 3)', MU))
    f.show(L(ox - 10, oy - 10, ox + 3 * cw + 10, oy + 3 * ch + 10, VI, 1.6, '5 4') + S(ox + 3 * cw + 12, oy + 3 * ch + 14, 'diagonal', VI), .6)
    t = 1.4
    for i in range(2):
        for j in range(3):
            c = FI if i == j else BR
            cel = mcell(ox + j * cw, oy + i * ch, A[i][j], cw, ch, c, tn(c, '.12'))
            if i == j: f.show(cel, .3)
            else:
                f.path(cel, [(0, 0, 0), (t, (i - j) * cw, (j - i) * ch)], t0=.3); t += .7
    f.show(M(ox + 57, oy + 3 * ch + 34, '{A}ᵀ  (3 × 2)', FI), t + .3)
    f.show(S(300, 90, '(Aᵀ)ᵢⱼ = Aⱼᵢ : row i becomes column i', TX), t + .6)
    I = [['1', '0'], ['0', '1']]
    f.show(M(330, 160, '{A} · {A}⁻¹ =', TX, 'start') + matrix(450, 136, I, 32, 26) +
           S(530, 158, 'undoes A', FI, bold=True), t + 1.4)
    f.show(S(300, 210, 'only square, full-rank A has an inverse', MU), t + 2)
    return finish(f, 230)

LAYER = '''
  <div class="subsec" id="linalg-s3-4">
    <h3 class="ssh"><b>3.4</b>Linear layer</h3>
    <p class="skey">A dense layer is one matrix multiplication plus a shift: each row of <span class="mth"><var>W</var></span> turns the whole input into one output.</p>
  <div class="eq">
    <div class="line">
      <span class="t g"><span><var>y</var></span><em>(k × 1) output</em></span>
      <span class="op">=</span>
      <span class="t b"><span><var>W</var></span><em>(k × d) weights</em></span>
      <span class="t p"><span><var>x</var></span><em>(d × 1) input</em></span>
      <span class="op">+</span>
      <span class="t"><span><var>b</var></span><em>(k × 1) bias</em></span>
    </div>
  </div>
%s
    <ul class="why">
      <li>Stack layers with an activation in between and you have an MLP; without the activation they collapse into one matrix.</li>
      <li>Parameter count is <span class="mth"><var>k</var>·<var>d</var> + <var>k</var></span>: a 784 → 256 layer has about 200k weights.</li>
    </ul>
  </div>

  <div class="subsec" id="linalg-s3-5">
    <h3 class="ssh"><b>3.5</b>Transpose &amp; inverse</h3>
    <p class="skey">Transpose swaps rows and columns; the inverse is the matrix that undoes a move.</p>
  <div class="eq">
    <div class="line">
      <span class="t"><span>(<var>A</var><sup>T</sup>)<sub><var>ij</var></sub></span></span>
      <span class="op">=</span>
      <span class="t b"><span><var>A</var><sub><var>ji</var></sub></span><em>row i becomes column i</em></span>
    </div>
    <div class="line">
      <span class="t"><span><var>A</var><var>A</var><sup>−1</sup></span></span>
      <span class="op">=</span>
      <span class="t g"><span><var>I</var></span><em>identity: the move that changes nothing</em></span>
    </div>
  </div>
%s
    <ul class="why">
      <li>Transpose appears everywhere shapes need to line up: <span class="mth"><var>X</var><sup>T</sup><var>X</var></span>, <span class="mth"><var>Q</var><var>K</var><sup>T</sup></span> in attention.</li>
      <li>In practice you solve <span class="mth"><var>A</var><var>x</var> = <var>b</var></span> directly instead of computing <span class="mth"><var>A</var><sup>−1</sup></span>; it is faster and more stable.</li>
    </ul>
  </div>
'''

L1 = '''    <div class="line">
      <span class="t"><span>‖<var>a</var>‖<sub>1</sub></span></span>
      <span class="op">=</span>
      <span class="t p"><span>|<var>a</var><sub>1</sub>| + |<var>a</var><sub>2</sub>| + … + |<var>a</var><sub><var>n</var></sub>|</span><em>L1: add the absolute values (city-block distance)</em></span>
    </div>
'''
COV = '''    <div class="line">
      <span class="t"><span><var>C</var></span></span>
      <span class="op">=</span>
      <span class="t b"><span><span class="frac"><i><var>X</var><sup>T</sup><var>X</var></i><i><var>n</var> − 1</i></span></span><em>covariance of centred X (each column minus its mean), d × d</em></span>
    </div>
'''

def main():
    s = open(PAGE).read()
    assert 'linalg-s3-4' not in s
    # 2.1: L1 line after L2 line inside first .eq of s2-1
    a = s.index('id="linalg-s2-1"'); e = s.index('  </div>\n<figure', a)
    s = s[:e] + L1 + s[e:]
    s = s.replace('<li>This is the L2 norm;', '<li>The first line is the L2 norm, the second the L1 norm (Lasso penalty);', 1)
    # 3.4/3.5 before end of section 3
    a = s.index('<section id="linalg-s4"'); e = s.rindex('</section>', 0, a)
    s = s[:e] + (LAYER % (fig_layer(), fig_transpose())).lstrip('\n') + s[e:]
    # 5.2 covariance line first in its .eq
    a = s.index('id="linalg-s5-2"'); e = s.index('<div class="eq">\n', a) + len('<div class="eq">\n')
    s = s[:e] + COV + s[e:]
    open(PAGE, 'w').write(s)

if __name__ == '__main__':
    main()
