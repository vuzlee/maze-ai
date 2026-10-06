# -*- coding: utf-8 -*-
"""SVM 4.3 RBF kernel: the RBF kernel is an infinite Taylor series of polynomial kernels.
Figure: rewrite K, expand e^{2γ x·x'} term by term — each term (x·x')^k is a degree-k polynomial kernel
= one more block of dimensions — and the partial sums converge to K. Every number is computed.
Run: python3 svm_rbf_taylor.py -> rewrites subsection svm-s4-3 (eq + figure + bullets)."""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from linear_algebra import Anim, T, R, L, MU, TX, FA, BR, VI, FI, RO, RULE, RULE_HI, BG, tn, M, S, dot, poly, Plane, finish
PAGE = os.path.join(HERE, '../../../content/07-machine-learning/05-classical-ml/svm/index.html')

# 1-D example so every number is readable: x = 1.0, x' = 0.8, gamma = 0.5
X, XP, G = 1.0, 0.8, 0.5
K = math.exp(-G * (X - XP) ** 2)            # 0.9802
PRE = math.exp(-G * X * X) * math.exp(-G * XP * XP)   # e^{-γx²} e^{-γx'²}
t = 2 * G * X * XP                          # 0.8
TERMS = [t ** k / math.factorial(k) for k in range(7)]
SUMS = [sum(TERMS[:k + 1]) * PRE for k in range(7)]
assert abs(PRE * math.exp(t) - K) < 1e-12

def EXP(base, exp):
    """base with a raised exponent, LaTeX-like, inside an sv-m text."""
    return '%s<tspan dy="-7" style="font-size:.7em">%s</tspan><tspan dy="7">​</tspan>' % (base, exp)

def phi(x, k):
    """k-th coordinate of the RBF feature map (1-D, gamma = 0.5): e^{-x²/2} x^k / sqrt(k!)."""
    return math.exp(-G * x * x) * math.sqrt((2 * G) ** k / math.factorial(k)) * x ** k

def fig():
    N = 7
    A = [phi(X, k) for k in range(N)]
    B = [phi(XP, k) for k in range(N)]
    run = [sum(A[i] * B[i] for i in range(k + 1)) for k in range(N)]
    assert abs(run[-1] - K) < .002
    f = Anim('rbt-', 720, 0, 'Two points x = 1 and x prime = 0.8 become infinitely long vectors phi(x) and phi(x prime). '
             'Each Taylor term adds one coordinate: dimension 1 holds the constant, dimension 2 holds x, dimension 3 x squared, '
             'and so on. The bars get shorter and shorter, so the tail barely matters. Multiplying the two vectors '
             'coordinate by coordinate and adding gives 0.44, 0.79, 0.93, 0.97, 0.98: the dot product converges to '
             'K(x, x prime) = 0.980, the value the kernel formula gives in one step.',
             'RBF LIFTS EACH POINT INTO AN INFINITELY LONG VECTOR')
    x0, step, SC = 118, 62, 62
    rows = [(140, A, 'φ({x})', '{x} = 1'), (240, B, 'φ({x}′)', '{x}′ = 0.8')]
    names = ['1', '{x}', '{x}²', '{x}³', '{x}⁴', '{x}⁵', '{x}⁶']
    for k in range(N):
        f.static(M(x0 + k * step, 40, names[k], MU, 'middle') + T(x0 + k * step, 56, 'dim %d' % (k + 1), FA, cls='sv-d'))
    f.static(T(x0 + N * step + 6, 48, '… dim ∞', MU, 'start', 'sv-s'))
    for base, V, lab, val in rows:
        f.static(M(0, base - 22, lab, TX, 'start') + M(0, base - 2, val, MU, 'start') + L(x0 - 26, base, x0 + N * step + 60, base, RULE_HI, 1))
    t = .5
    for k in range(N):
        cx = x0 + k * step
        for base, V, _, _ in rows:
            h = V[k] * SC
            f.show(R(cx - 18, base - h, 36, max(h, 1.5), tn(BR, '.24'), BR, 3, 1.1) + T(cx, base - h - 5, '%.2f' % V[k], BR, cls='sv-d'), t)
        prod = A[k] * B[k]
        f.show(T(cx, 266, '×', FA, cls='sv-d') + T(cx, 284, '%.2f' % prod, VI, cls='sv-d', bold=True), t + .2)
        last = k == N - 1
        f.show(M(0, 326, 'φ({x})·φ({x}′) so far = %.3f' % run[k], VI if not last else FI, 'start'), t + .25, None if last else t + .8)
        t += .8
    # the tail: ever smaller ghost cells to say "it never ends"
    for j in range(4):
        cx = x0 + N * step + 20 + j * 16
        for base, _, _, _ in rows:
            hh = 6 / (j + 1)
            f.show(R(cx - 5, base - hh, 10, hh, tn(BR, '.15'), 'var(--ghost)', 2, .8), t)
    f.show(L(x0 - 26, 298, x0 + N * step + 60, 298, RULE, 1) + M(330, 326, '→  {K}({x}, {x}′) = %.3f' % K, FI, 'start'), t + .2)
    f.show(T(0, 352, 'bars shrink like 1/√k!, so infinitely many dimensions still add up to a finite number — the kernel formula gives it in one step', MU, 'start', 'sv-d'), t + .5)
    return finish(f, 366)

EQ = '''<div class="eq">
      <div class="line">
        <span class="t"><span><var>K</var>(<var>x</var>, <var>x</var>′)</span></span>
        <span class="op">=</span>
        <span class="t b"><span><var>e</var><sup>−<var>γ</var>‖<var>x</var>‖<sup>2</sup></sup> <var>e</var><sup>−<var>γ</var>‖<var>x</var>′‖<sup>2</sup></sup></span><em>one point each</em></span>
        <span class="op">·</span>
        <span class="t p"><span><span class="frac"><i>∞</i><i></i></span></span></span>
      </div>
    </div>'''
EQ = '''<div class="eq">
      <div class="line">
        <span class="t"><span><var>K</var>(<var>x</var>, <var>x</var>′) = <var>e</var><sup>−<var>γ</var>‖<var>x</var> − <var>x</var>′‖<sup>2</sup></sup></span></span>
        <span class="op">=</span>
        <span class="t b"><span><var>e</var><sup>−<var>γ</var>‖<var>x</var>‖<sup>2</sup></sup><var>e</var><sup>−<var>γ</var>‖<var>x</var>′‖<sup>2</sup></sup></span><em>one point each</em></span>
        <span class="op">·</span>
        <span class="t p"><span><var>e</var><sup>2<var>γ</var> <var>x</var>·<var>x</var>′</sup></span><em>expand by Taylor</em></span>
      </div>
      <div class="line">
        <span class="t p"><span><var>e</var><sup>2<var>γ</var> <var>x</var>·<var>x</var>′</sup></span></span>
        <span class="op">=</span>
        <span class="t g"><span><span class="bigop"><i>∞</i><b>Σ</b><i><var>k</var> = 0</i></span> <span class="frac"><i>(2<var>γ</var>)<sup><var>k</var></sup></i><i><var>k</var>!</i></span> (<var>x</var>·<var>x</var>′)<sup><var>k</var></sup></span><em>a polynomial kernel of every degree k → infinitely many dimensions</em></span>
      </div>
    </div>'''

if __name__ == '__main__':
    h = open(PAGE).read()
    a = h.index('<div class="subsec" id="svm-s4-3">')
    b = h.index('</section>', a)
    sub = h[a:b]
    old_fig = re.search(r'<figure class="gist">.*?</figure>', sub, re.S).group(0)   # keep the gamma bump figure
    new = '''<div class="subsec" id="svm-s4-3">
    <h3 class="ssh"><b>4.3</b>RBF kernel</h3>
    <p class="skey">At heart <em>an infinite Taylor series</em>: one polynomial kernel of every degree, summed — so it works in infinitely many dimensions without ever building them.</p>
    %s
%s
    <ul class="why">
      <li>No coordinate vector can hold infinitely many dimensions; the kernel gets the dot product in one step, which is the whole point of the trick.</li>
      <li>Seen from the data, each training point puts a bump of width set by <span class="mth"><var>γ</var></span>; the score is their sum:</li>
    </ul>
%s
    <ul class="why">
      <li>Small <span class="mth"><var>γ</var></span>: wide bumps, a smooth boundary. Large <span class="mth"><var>γ</var></span>: a spike on every point, memorises the training set (overfitting). RBF is the default kernel in SVC.</li>
    </ul>
  </div>
''' % (EQ, fig(), old_fig)
    tail = sub[sub.rindex('</div>') + 6:]  # anything after the subsection (section-level bullets) stays
    h = h[:a] + new + tail.lstrip('\n') + h[b:]
    open(PAGE, 'w').write(h)
    print('ok', round(K, 4), [round(s, 2) for s in SUMS])
