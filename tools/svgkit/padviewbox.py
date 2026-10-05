# Usage: python3 tools/svgkit/padviewbox.py <page.html>...
# Grow each figure's viewBox so EVERY element fits — including groups that are only visible mid-animation
# (highlight rings, moving pills), which a final-state check misses. Adds an 8px margin where content touches
# or crosses an edge. Measured in headless Chrome with all opacity forced to 1 and transforms at final state.
import re, sys, subprocess, os
CSS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'style.css')
JS = '''<style>svg *{opacity:1!important;animation:none!important}</style><script>
const o=[];document.querySelectorAll("figure svg[viewBox]").forEach((s,i)=>{const v=s.viewBox.baseVal,sr=s.getBoundingClientRect(),k=sr.width/v.width;
let a=1e9,b=1e9,c=-1e9,d=-1e9;s.querySelectorAll("text,rect,line,path,circle,polygon,ellipse").forEach(e=>{const r=e.getBoundingClientRect();if(!r.width&&!r.height)return;
a=Math.min(a,r.left);b=Math.min(b,r.top);c=Math.max(c,r.right);d=Math.max(d,r.bottom)});
o.push([i,(a-sr.left)/k+v.x,(b-sr.top)/k+v.y,(c-sr.left)/k+v.x,(d-sr.top)/k+v.y].map(z=>z.toFixed(1)).join(" "))});
const p=document.createElement("pre");p.id="BB";p.textContent=o.join(";");document.body.appendChild(p);</script>'''
M = 8
for page in sys.argv[1:]:
    h = open(page).read()
    spans = [m.span() for m in re.finditer(r'<figure class="gist">.*?</figure>', h, re.S)]
    if not spans: continue
    tmp = '/tmp/_padvb.html'
    open(tmp, 'w').write('<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="file://%s"><style>body{margin:16px;width:780px}</style>%s%s'
                         % (os.path.abspath(CSS), ''.join(h[a:b] for a, b in spans), JS))
    r = subprocess.run(['google-chrome', '--headless', '--no-sandbox', '--force-prefers-reduced-motion', '--virtual-time-budget=2000',
                        '--dump-dom', 'file://' + tmp], capture_output=True, text=True)
    m = re.search(r'<pre id="BB">(.*?)</pre>', r.stdout, re.S)
    if not m: print('no result', page); continue
    box = {int(float(t.split()[0])): list(map(float, t.split()[1:])) for t in m.group(1).split(';') if t.strip()}
    out, n = h, 0
    for i, (a, b) in reversed(list(enumerate(spans))):
        f = h[a:b]; vm = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', f)
        if not vm or i not in box: continue
        x, y, w, hh = map(float, vm.groups()); L, T, R, B = box[i]
        nx = min(x, L - M) if L < x + 1 else x
        ny = min(y, T - M) if T < y + 1 else y
        nr = max(x + w, R + M) if R > x + w - 1 else x + w
        nb = max(y + hh, B + M) if B > y + hh - 1 else y + hh
        if (round(nx), round(ny), round(nr), round(nb)) == (round(x), round(y), round(x + w), round(y + hh)): continue
        vb = 'viewBox="%g %g %g %g"' % (round(nx), round(ny), round(nr - nx), round(nb - ny))
        out = out[:a] + f.replace(vm.group(0), vb, 1) + out[b:]; n += 1
    if n:
        open(page, 'w').write(out); print('%2d  %s' % (n, page.split('/')[-2]))
