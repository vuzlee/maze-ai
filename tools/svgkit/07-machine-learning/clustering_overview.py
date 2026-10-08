# -*- coding: utf-8 -*-
"""Clustering group overview (2026-10-09): a map of the group, not a lesson.

    01 Same points, four families  gallery: k-means, DBSCAN, agglomerative, Gaussian mixture run on the
                                   one shared toy set (labels computed in dsa/clustering_overview.py)
    02 Family tree                 top-down: k-means -> DBSCAN -> HDBSCAN, with the two side families
    03 Learning order
Dropped: Mental model; the per-family animated sections (lessons own k-means/DBSCAN/HDBSCAN; the two
families with no lesson keep a short note under the gallery); Silhouette (owned by K-means "Choosing k").
Run: python3 tools/svgkit/07-machine-learning/clustering_overview.py   (re-runnable)
"""
import os, re, sys, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, os.path.join(HERE, '../dsa'))
from overview import Fig, text, gallery, ln, B, V, FL
with contextlib.redirect_stdout(io.StringIO()):
    import clustering_overview as C

ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
PAGE = os.path.join(ROOT, 'content/07-machine-learning/07-clustering/clustering-overview/index.html')
L = {'km': '../kmeans-clustering/index.html', 'db': '../dbscan/index.html', 'hdb': '../hdbscan/index.html'}
R = 'var(--rose)'
COL = [FL, V, B]
SC = 13.6

def cloud(lab):
    def draw(x, y):
        o = f'<rect x="{x-4}" y="{y-4}" width="{10*SC+8:.0f}" height="{9*SC+8:.0f}" rx="4" fill="none" stroke="var(--rule)"/>'
        for i, (px, py) in enumerate(C.P):
            cx, cy = x + px * SC, y + (9.6 - py) * SC
            l = lab[i]
            if l < 0:
                o += (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.6" fill="var(--bg)" stroke="{R}" stroke-width="1.3"/>'
                      + ln(cx - 2, cy - 2, cx + 2, cy + 2, R, 1.1) + ln(cx - 2, cy + 2, cx + 2, cy - 2, R, 1.1))
            else:
                o += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.4" fill="{COL[l]}" stroke="var(--bg)" stroke-width=".8"/>'
        return o
    return draw

def caught(lab):
    n = 0
    for name, idx in C.SHAPES:
        idx = list(idx)
        if name == 'outliers':
            n += all(lab[i] < 0 for i in idx); continue
        c = lab[idx[0]]; mem = [j for j in range(C.N) if lab[j] == c]
        n += c >= 0 and all(lab[i] == c for i in idx) and len(idx) >= .75 * len(mem)
    return n

def families():
    runs = [('K-means · k = 3', C.KM, L['km']), ('DBSCAN', C.DB, L['db']),
            ('Agglomerative · single', C.AGD, None), ('Gaussian mixture', C.GLAB, None)]
    f = Fig('clov1', 680, 0, 'SAME 33 POINTS · FOUR DEFINITIONS OF A GROUP',
            'Four copies of the same 33 points: a round blob top left, a round blob in the middle, a moon curving '
            'round it and three outliers. Colours show the groups each family finds. K-means cuts the moon into '
            'pieces and forces the outliers into groups. DBSCAN finds both blobs, the whole moon, and marks the three '
            'outliers as noise. Single-linkage agglomerative, cut at one height, also follows the moon and leaves the '
            'outliers alone. The Gaussian mixture fits ellipses, so it mixes the moon with the middle blob. Under each '
            'panel: how many of the four shapes it recovered. K-means and DBSCAN link to their lessons.')
    items = [(n, cloud(lab), h) for n, lab, h in runs]
    bot = gallery(f, [('ONE DATASET, FOUR RUNS', 'colour = group · ✕ = noise', items)], top=40, cols=4, tw=164, th=172)
    for i, (n, lab, h) in enumerate(runs):
        k = caught(lab)
        f.add(text(i * 172 + 82, bot - 10 - 172 + 166, f'{k} of 4 shapes', 'sv-d', V if k == 4 else 'var(--muted)', 'middle', ';font-weight:600'))
    f.h = bot + 6
    return f.svg()

def tree():
    f = Fig('clov2', 680, 296, 'FAMILY TREE · WHAT EACH ONE FIXES',
            'A top-down tree. At the top, the question: which points form a group? Three answers branch off. '
            'Nearest to a centre: k-means, with the Gaussian mixture below it, which makes membership soft and '
            'circles into ellipses. A dense region: DBSCAN, fixing k-means splitting non-round shapes and forcing '
            'outliers in; below it HDBSCAN, fixing one eps for every density. A chain of joins: agglomerative '
            'clustering, which gives every number of clusters as one dendrogram. K-means, DBSCAN and HDBSCAN link '
            'to their lessons.')
    f.node(340, 52, 'Which points form a group?', '', 'filled', f.step(.2), None, None, w=210, h=36)
    P = {'km': (110, 140), 'db': (340, 140), 'ag': (570, 140), 'gm': (110, 250), 'hdb': (340, 250)}
    for k, t in (('km', .5), ('db', .5), ('ag', .5)):
        f.edge((340, 70), (P[k][0], P[k][1] - 22), cls=f.step(t, draw=True))
    b = f.step(.8)
    f.node(*P['km'], 'K-means', 'nearest centre', 'plain', b, L['km'], None, w=160)
    f.node(*P['db'], 'DBSCAN', 'dense region + noise', 'plain', b, L['db'], None, w=160)
    f.node(*P['ag'], 'Agglomerative', 'join closest, cut tree', 'plain', b, None, None, w=160, dashed=True)
    for a, c, t, note in (('km', 'gm', 1.2, 'hard, round groups'), ('db', 'hdb', 1.2, 'one eps for all densities')):
        f.edge((P[a][0], P[a][1] + 22), (P[c][0], P[c][1] - 22), cls=f.step(t, draw=True))
        f.add(f'<g class="{f.step(t + .3)}">' + text(P[a][0] + 10, 199, note, 'sv-d', V, 'start', ';font-style:italic') + '</g>')
    f.add(f'<g class="{f.step(1.0)}">' + ln(192, 140, 254, 140, V, 1.3, True)
          + f'<path d="M253,136.5 L259,140 L253,143.5z" fill="{V}"/>'
          + text(225, 160, 'splits moon,', 'sv-d', V, 'middle', ';font-style:italic')
          + text(225, 173, 'forces outliers', 'sv-d', V, 'middle', ';font-style:italic') + '</g>')
    c = f.step(1.6)
    f.node(*P['gm'], 'Gaussian mixture', 'soft, ellipses', 'plain', c, None, None, w=160, dashed=True)
    f.node(*P['hdb'], 'HDBSCAN', 'every eps at once', 'violet', c, L['hdb'], None, w=160)
    f.add(f'<g class="{f.step(1.9)}">' + text(680, 250, 'dashed = no lesson of its own', 'sv-d', 'var(--muted)', 'end') + '</g>')
    return f.svg()

def order():
    f = Fig('clov3', 680, 104, 'LEARNING ORDER · EACH LESSON FIXES WHERE THE LAST ONE BREAKS',
            'Three stops in a row, each a link: K-means, DBSCAN, HDBSCAN.')
    stops = [('K-means', 'round groups, k given', L['km']), ('DBSCAN', 'any shape + noise', L['db']),
             ('HDBSCAN', 'mixed densities', L['hdb'])]
    w, gap = 200, 40
    for i, (n, sub, href) in enumerate(stops):
        cx = i * (w + gap) + w / 2
        if i:
            f.add(f'<line class="{f.step(.4 + i * .35, draw=True)}" pathLength="1" x1="{cx - w/2 - gap + 2}" y1="62" '
                  f'x2="{cx - w/2 - 2}" y2="62" stroke="var(--rule-hi)" stroke-width="1.6"/>')
        f.node(cx, 62, n, sub, 'violet' if i == 2 else 'plain', f.step(.3 + i * .35), href, None, w=w, h=44)
    return f.svg()

BODY = '''<header class="hero">
  <p class="eyebrow">Machine learning · Clustering</p>
  <h1>Clustering <em>overview</em></h1>
  <p class="lede">With no labels, a clustering method decides what "a group" means — a centre, a dense region, a chain of near points, or a bell curve — and that choice decides <b>which shapes it can find</b>.</p>
</header>

<section id="clov-s1" class="lesson">
  <div class="sh"><b>01</b><h2>Same points, four families</h2></div>
  <p class="key">Run each family on the same points and the definition of a group becomes visible: <em>only density and chains follow the moon</em>.</p>
<figure class="gist">
{f1}
</figure>
  <ul class="why">
    <li><b>Agglomerative</b> clustering starts with every point alone and joins the two closest groups again and again; the record of joins is a <b>dendrogram</b>, cut at a height. "Closest" needs a <b>linkage</b>: single, complete, average or Ward. One tree gives every number of clusters, but pairwise distances cost O(<var>n</var><sup>2</sup>) memory.</li>
    <li>A <b>Gaussian mixture model</b> (GMM) is k-means with soft membership and tilted ellipses, fitted by <b>EM</b>; it still needs <var>k</var> and convex shapes.</li>
    <li>Distance needs features on one scale — standardise first (<a href="../../04-core-concepts/feature-engineering/index.html">Feature engineering</a>). Scoring a clustering with no labels (silhouette) is in <a href="../kmeans-clustering/index.html">K-means</a>.</li>
  </ul>
</section>

<section id="clov-s2" class="lesson">
  <div class="sh"><b>02</b><h2>Family tree</h2></div>
  <p class="key">Three answers to "what is a group", and <em>each child fixes one failure of its parent</em>.</p>
<figure class="gist">
{f2}
</figure>
</section>

<section id="clov-s3" class="lesson">
  <div class="sh"><b>03</b><h2>Learning order</h2></div>
  <p class="key">Three lessons, each born to fix <em>where the one before breaks</em>.</p>
<figure class="gist">
{f3}
</figure>
  <ul class="why">
    <li>For many features, read <a href="../../08-dimensionality/pca-dimensionality/index.html">PCA</a> too: in high dimensions every distance looks alike.</li>
  </ul>
</section>

'''

def build():
    s = open(PAGE, encoding='utf-8').read()
    a = s.index('<header class="hero">')
    b = s.index('<script>\n/* Figures start')
    s = s[:a] + BODY.format(f1=families(), f2=tree(), f3=order()) + s[b:]
    blurb = ('The clustering group on one page: k-means, DBSCAN, agglomerative and Gaussian mixture run on the same '
             'points, the family tree of what each fixes, and the order to learn them.')
    s = re.sub(r'data-blurb="[^"]*"', 'data-blurb="%s"' % blurb, s, count=1)
    open(PAGE, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    build(); print('ok')
