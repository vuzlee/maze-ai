# -*- coding: utf-8 -*-
"""2x2 target grid for bias-variance Mental model. Run: python3 bias_variance_fix.py > out.svg"""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fitkit_bvof import *  # noqa

def grid():
    an = Anim('bg-', 720, 440, 'A two by two grid of targets. Columns: low and high variance. Rows: low and high bias. Shots land one cell at a time: tight on the centre, scattered around the centre, tight but off centre, scattered and off centre. Labels then read ideal, overfitting, underfitting, worst.', 'BIAS AND VARIANCE · WHERE THE SHOTS LAND', 3.0)
    cols, rows, R0 = (330, 560), (130, 320), 66
    an.static(T(cols[0], 44, 'low variance', MU, cls='sv-l') + T(cols[1], 44, 'high variance', MU, cls='sv-l'))
    an.static(T(150, rows[0] + 4, 'low bias', MU, 'end', cls='sv-l') + T(150, rows[1] + 4, 'high bias', MU, 'end', cls='sv-l'))
    for cy in rows:
        for cx in cols:
            an.static(''.join('<circle cx="%d" cy="%d" r="%.1f" fill="%s" stroke="var(--rule-hi)" stroke-width="1"/>' % (cx, cy, r, fl)
                for r, fl in ((R0, 'var(--bg)'), (R0 * 2 / 3, 'var(--bg)'), (R0 / 3, 'var(--sunk)'))) +
                '<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (cx, cy, FI))
    rng = random.Random(3); t = .5
    cells = [(0, 0, 0, 6, 'ideal'), (1, 0, 0, 24, 'overfitting'), (0, 1, 1, 6, 'underfitting'), (1, 1, 1, 24, 'worst')]
    for ci, ri, off, sp, lab in cells:
        cx, cy = cols[ci], rows[ri]; ox, oy = (26, -24) if off else (0, 0)
        for _ in range(8):
            x = cx + ox + rng.gauss(0, sp); y = cy + oy + rng.gauss(0, sp)
            dx, dy = x - cx, y - cy; r = (dx*dx + dy*dy) ** .5
            if r > R0 - 8: x, y = cx + dx * (R0 - 8) / r, cy + dy * (R0 - 8) / r
            an.show('<circle cx="%.1f" cy="%.1f" r="4.2" fill="%s" fill-opacity=".85"/>' % (x, y, VI), t, d=.2)
            t += .2
        t += .3
    for ci, ri, off, sp, lab in cells:
        an.show(T(cols[ci], rows[ri] + R0 + 22, lab, FI if lab == 'ideal' else VI, bold=True), t)
        t += .5
    return an.render()

if __name__ == '__main__':
    print(grid())
