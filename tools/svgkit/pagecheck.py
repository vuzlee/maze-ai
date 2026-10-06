# Usage: python3 tools/svgkit/pagecheck.py [pages...]   (default: every content page)
# Structural checks a lesson page must pass, or the site chrome breaks silently:
# the three app scripts, toc/stage/np containers, one <article>, balanced tags, one replay script,
# no nested figures, no duplicate ids, <html>/<body> closed exactly once.
import re, sys, glob, collections
pages = sys.argv[1:] or sorted(glob.glob('content/*/*/*/index.html'))
bad = 0
for p in pages:
    h = open(p).read(); err = []
    base = re.search(r'data-base="([^"]*)"', h)
    b = base.group(1) if base else ''
    for js in ('catalog.js', 'search-index.js', 'app.js'):
        if not re.search(r'<script src="%sassets/%s"></script>' % (re.escape(b), js), h): err.append('missing ' + js)
    for need in ('id="toc"', 'id="stage"', 'id="np"', 'id="results"', 'id="q"', 'class="hero"', '<footer>'):
        if need not in h: err.append('missing ' + need)
    for tag in ('article', 'section', 'figure', 'svg', 'main', 'nav'):
        o, c = len(re.findall(r'<%s[\s>]' % tag, h)), h.count('</%s>' % tag)
        if o != c: err.append('%s %d/%d' % (tag, o, c))
    if h.count('<article') != 1: err.append('%d <article>' % h.count('<article'))
    for t in ('</html>', '</body>', '<html'):
        if h.count(t) != 1: err.append('%d %s' % (h.count(t), t))
    if h.count('new IntersectionObserver') > 1: err.append('replay script x%d' % h.count('new IntersectionObserver'))
    if re.search(r'<figure[^>]*>\s*<figure', h): err.append('nested figure')
    ids = [i for i in re.findall(r'\sid="([^"]+)"', h)]
    d = [i for i, n in collections.Counter(ids).items() if n > 1]
    if d: err.append('dup ids ' + ','.join(d[:3]))
    if 'data-anim' in h and 'IntersectionObserver' not in h: err.append('animated figures but no replay script')
    if 'lab.js' in h and not glob.glob(p.replace('index.html', 'lab.js')): err.append('lab.js tag, no file')
    if err:
        bad += 1; print('%-32s %s' % (p.split('/')[-2], ' | '.join(err)))
print('%d / %d pages with problems' % (bad, len(pages)))
