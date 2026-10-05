"""Figures for content/01-dsa/04-algorithms/sliding-window. Uses arrkit.py (shared, not edited)."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arrkit import *  # noqa

W = 760
def frame(row, l, r):
    return R(row.xl(l) - 5, row.y - 5, row.xl(r) + row.w - row.xl(l) + 10, row.h + 10, 'none', PT, 9, 2)

def play(f, row, code, steps, t0, sy, dt=1.5):
    """steps: dict(l, r, line, s=status, v=verdict, probe=i). Window frame, pointers, greys, code bar."""
    pl, pr = Ptr(row, 'l', 0), Ptr(row, 'r', 0, up=True)
    stat, frm, ver = [], [], []
    greyed = 0; t = t0
    for k, e in enumerate(steps):
        if code: code.at(t, e['line'])
        pl.to(t, e['l']); pr.to(t, e['r'])
        while greyed < e['l']:
            f.show(row.cell(greyed, 'g'), t + .3); greyed += 1
        stat.append((t, st(row.x0, sy, e['s'], TX, True)))
        frm.append((t + .4, frame(row, e['l'], e['r']) if e['r'] >= e['l'] else ''))
        p = e.get('probe')
        ver.append((t + .4, (row.ring(p) if p is not None else '') + st(row.x0, sy + 22, e['v'], MID)))
        t += dt
    end = t
    states(f, stat, end); states(f, frm, end); states(f, ver, end)
    pl.emit(f, t0, hide=end); pr.emit(f, t0, hide=end)
    if code: code.emit(f)
    return end

figs = {}

# m1 shortest subarray with sum >= 7, code left
a = [2, 3, 1, 2, 4, 3]
f = Anim('swm1-', W, 300, 'Array 2 3 1 2 4 3, goal: shortest piece with sum at least 7. r stretches the window to the right and adds a value; while the sum is at least 7, the length is recorded and l shrinks the window from the left. Answer: 4 3, length 2.', 'STRETCH WITH r · SHRINK WITH l · SHORTEST PIECE WITH SUM ≥ 7')
code = Code2(0, 40, ['l, s, ans = 0, 0, inf', 'for r in range(n):', '    s += a[r]', '    while s >= 7:', '        ans = min(ans, r-l+1)', '        s -= a[l]; l += 1', 'return ans'], 250)
f.static(code.svg())
row = Row(300, 100, a); row.draw(f, .2)
f.show(chip(W - 16 - chipw('sum ≥ 7, shortest'), 30, 'sum ≥ 7, shortest'), .8)
S = []
l = s = 0; ans = None
for r in range(len(a)):
    s += a[r]
    S.append(dict(l=l, r=r, line=2, probe=r, s='r = %d · s = %d' % (r, s), v='add a[%d] = %d → s = %d' % (r, a[r], s) + (' < 7, stretch' if s < 7 else ' ≥ 7')))
    while s >= 7:
        ln = r - l + 1; ans = ln if ans is None else min(ans, ln); best = (l, r)
        s -= a[l]; l += 1
        S.append(dict(l=l, r=r, line=5, probe=l - 1, s='len %d → ans = %d · s = %d' % (ln, ans, s), v='drop a[%d], shrink from the left' % (l - 1)))
end = play(f, row, code, S, 1.4, 210, 1.3)
for i in range(best[0], best[1] + 1): f.show(row.cell(i, 'f'), end)
f.show(st((row.cx(best[0]) + row.cx(best[1])) / 2, 178, '✓ found', TG, True, 'middle') + st(row.x0, 232, 'ans = 2 · each pointer only moves right', TG, True), end)
figs['m1'] = f.render()

# m2 complexity: moves count, then graph
f = Anim('swm2-', W, 360, 'r moves 8 times, l moves at most 8 times: 16 moves in total for 8 cells. Graph: checking every subarray grows as n squared, the window grows as 2n, a straight line.', 'O(n) · r AND l EACH CROSS THE ARRAY ONCE')
row = Row(0, 40, list('abcdefgh'), 40, 30); row.draw(f, .2)
pr = Ptr(row, 'r', 0, up=True, ln=8); pl = Ptr(row, 'l', 0, ln=8)
for k in range(1, 8): pr.to(.6 + k * .35, k)
for k in range(1, 8): pl.to(3.4 + k * .35, k)
pr.emit(f, .5); pl.emit(f, .5)
for k in range(8): f.show(row.cell(k, 'g'), 3.5 + k * .35)
f.show(st(420, 70, 'r: 8 moves + l: ≤ 8 moves = 16', TX, True), 6.5)
gx, gy, gw, gh = 70, 150, 520, 160
px = lambda n: gx + n / 16 * gw; py = lambda v: gy + gh - v / 64 * gh
f.show(axes(gx, gy, gw, gh, (4, 8, 12, 16), (16, 32, 48, 64), 'n', 'steps', px, py), 7.2)
f.show(poly([(px(x / 4), py((x / 4) ** 2 / 2)) for x in range(0, 46)], 'var(--ghost)', 2) + lab(px(11.3), py(64) + 4, 'all subarrays ≈ n²/2', MU), 7.8, d=.8)
f.show(poly([(px(0), py(0)), (px(16), py(32))], TG, 2.6) + lab(px(16), py(32) - 10, 'window 2n', TG, 'end', True), 8.8, d=.8)
for k, n in enumerate((4, 8, 12, 16)): f.show(dot(px(n), py(2 * n)), 9.6 + k * .25)
f.show(st(gx + gw, gy + gh + 40, 'n = 8 → 16 moves instead of 36 checks', TG, True, 'end'), 10.8)
figs['m2'] = f.render()

# p1 fixed window k=3 max sum
a = [1, 3, 2, 6, 4, 1, 5]
f = Anim('swp1-', W, 230, 'Fixed window of 3 over 1 3 2 6 4 1 5. Each slide adds the new right value and removes the one that falls off the left. Best sum 12 at 2 6 4.', 'FIXED WINDOW k = 3 · LARGEST SUM')
row = Row(0, 70, a); row.draw(f, .2)
f.show(chip(W - 16 - chipw('max sum of 3'), 20, 'max sum of 3'), .6)
S = [dict(l=0, r=2, line=0, probe=2, s='sum = 1+3+2 = 6', v='first window → best = 6')]
s, best, bi = 6, 6, 0
for r in range(3, len(a)):
    s += a[r] - a[r - 3]
    nb = s > best
    if nb: best, bi = s, r - 2
    S.append(dict(l=r - 2, r=r, line=0, probe=r, s='sum = %d + %d − %d = %d' % (s - a[r] + a[r - 3], a[r], a[r - 3], s), v=('%d > old best → best = %d' % (s, best)) if nb else ('%d ≤ best %d, keep' % (s, best))))
end = play(f, row, None, S, 1.2, 175, 1.5)
for i in range(bi, bi + 3): f.show(row.cell(i, 'f'), end)
f.show(st(row.right() + 20, 95, '✓ best = 12', TG, True), end)
figs['p1'] = f.render()

# p2 longest substring without repeat
a = list('abcabcbb')
f = Anim('swp2-', W, 230, 'String abcabcbb. r adds a letter; if it is already inside the window, l shrinks past the old copy. Longest window without a repeat: abc, length 3.', 'STRETCH AND SHRINK · LONGEST PIECE WITHOUT A REPEATED LETTER')
row = Row(0, 70, a); row.draw(f, .2)
f.show(chip(W - 16 - chipw('longest, no repeat'), 20, 'longest, no repeat'), .6)
S = []; l = 0; best = 0; bl = 0
for r in range(len(a)):
    if a[r] in a[l:r]:
        nl = a.index(a[r], l) + 1
        S.append(dict(l=l, r=r, line=0, probe=r, s='window "%s" + %s' % (''.join(a[l:r]), a[r]), v='%s already inside → shrink' % a[r]))
        l = nl
    ln = r - l + 1
    if ln > best: best, bl = ln, l
    S.append(dict(l=l, r=r, line=0, probe=r, s='window "%s" · len %d' % (''.join(a[l:r + 1]), ln), v='no repeat · best = %d' % best))
end = play(f, row, None, S, 1.2, 175, 1.0)
for i in range(bl, bl + best): f.show(row.cell(i, 'f'), end)
f.show(st(row.right() + 20, 95, '✓ best = 3', TG, True), end)
figs['p2'] = f.render()

# p3 count via at-most-K
a = [1, 0, 1, 0, 1]
f = Anim('swp3-', W, 300, 'Binary array 1 0 1 0 1, count subarrays with sum at most 2. At each r, all r - l + 1 subarrays ending at r are valid, so they are added to the count. Then exactly 2 = at most 2 minus at most 1.', 'COUNT = Σ (r − l + 1) · SUBARRAYS WITH SUM ≤ 2')
code = Code2(0, 40, ['for r in range(n):', '    s += a[r]', '    while s > k:', '        s -= a[l]; l += 1', '    cnt += r - l + 1'], 230)
f.static(code.svg())
row = Row(290, 90, a); row.draw(f, .2)
f.show(chip(W - 16 - chipw('count, sum ≤ 2'), 30, 'count, sum ≤ 2'), .6)
S = []; l = s = cnt = 0
for r in range(len(a)):
    s += a[r]
    while s > 2:
        S.append(dict(l=l, r=r, line=3, probe=l, s='s = %d > 2' % s, v='drop a[%d], shrink' % l)); s -= a[l]; l += 1
    cnt += r - l + 1
    S.append(dict(l=l, r=r, line=4, probe=r, s='r = %d · s = %d · cnt += %d' % (r, s, r - l + 1), v='cnt = %d' % cnt))
end = play(f, row, code, S, 1.2, 200, 1.4)
f.show(st(row.x0, 248, 'at_most(2) = 14 · at_most(1) = 10', TX, True), end)
f.show(st(row.x0, 272, '✓ exactly 2 = 14 − 10 = 4', TG, True), end + .6)
figs['p3'] = f.render()

json.dump(figs, open('/tmp/dsa/sliding-window.json', 'w'))
print( {k: len(v) for k, v in figs.items()})
