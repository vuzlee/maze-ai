# Usage: python3 tools/svgkit/rendercheck.py [pages...]  (default: every content page)
# Loads each page in headless Chrome and checks what app.js must build: TOC links, breadcrumb,
# prev/next, and that no JS error was thrown. Catches pages that look fine as HTML but render empty.
import re, sys, glob, subprocess, os
pages = sys.argv[1:] or sorted(glob.glob('content/*/*/*/index.html'))
PROBE = ('<script>window.__err=[];addEventListener("error",e=>__err.push(e.message));'
         'addEventListener("load",()=>setTimeout(()=>{const d=document.createElement("pre");d.id="RC";'
         'd.textContent=[document.querySelectorAll("#toc a").length,document.querySelectorAll("section.lesson").length,'
         '(document.getElementById("crumbTitle")||{}).textContent?1:0,document.querySelectorAll("#np a").length,__err.join(" / ")].join("|");'
         'document.body.appendChild(d)},300))</script>')
bad = 0
for p in pages:
    h = open(p).read()
    t = p.replace('index.html', '_rc.html')
    open(t, 'w').write(h.replace('<head>', '<head>' + PROBE, 1))
    r = subprocess.run(['google-chrome', '--headless', '--no-sandbox', '--virtual-time-budget=3000', '--dump-dom',
                        'file://' + os.path.abspath(t)], capture_output=True, text=True)
    os.remove(t)
    m = re.search(r'<pre id="RC">(.*?)</pre>', r.stdout, re.S)
    if not m:
        bad += 1; print('%-30s NO RENDER' % p.split('/')[-2]); continue
    toc, secs, crumb, np_, err = m.group(1).split('|', 4)
    probs = []
    if int(secs) and int(toc) < int(secs): probs.append('toc %s/%s' % (toc, secs))
    if crumb == '0': probs.append('no breadcrumb')
    if int(np_) == 0: probs.append('no prev/next')
    if err: probs.append('JS: ' + err[:120])
    if probs:
        bad += 1; print('%-30s %s' % (p.split('/')[-2], ' | '.join(probs)))
print('%d / %d pages with render problems' % (bad, len(pages)))
