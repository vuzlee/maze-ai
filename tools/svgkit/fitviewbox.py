# Usage: python3 tools/svgkit/fitviewbox.py <page.html>...  -> grows each spilling figure's viewBox to fit its content (+8px).
# Grow each figure's viewBox to its real content box + 8px pad when content spills out (final state).
import re,sys,subprocess,os
css=os.path.abspath('assets/style.css')
JS=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'clipcheck.py')).read().split("JS='''")[1].split("'''")[0]
JS=JS.replace('if(bad.length)out.push(i+": "+bad.join(", "))','out.push(i+" "+[L,T,R,B].map(z=>Math.round(z)).join(" "))').replace('||"clean"','')
for p in sys.argv[1:]:
    h=open(p).read()
    spans=[m.span() for m in re.finditer(r'<figure class="gist">.*?</figure>',h,re.S)]
    figs=[h[a:b] for a,b in spans]
    open('/tmp/fix/fit.html','w').write('<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="file://%s"><style>body{margin:16px;width:780px}</style>%s%s'%(css,''.join(figs),JS))
    r=subprocess.run(['google-chrome','--headless','--no-sandbox','--force-prefers-reduced-motion','--virtual-time-budget=3000','--dump-dom','file:///tmp/fix/fit.html'],capture_output=True,text=True)
    m=re.search(r'<pre id="CLIP">(.*?)</pre>',r.stdout,re.S)
    if not m: continue
    txt=m.group(1).replace(chr(92)+"n",chr(10))
    box={int(l.split()[0]):list(map(float,l.split()[1:])) for l in txt.strip().splitlines() if l.strip()}
    out=h; changed=0
    for i,(a,b) in reversed(list(enumerate(spans))):
        f=h[a:b]; vm=re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"',f)
        if not vm or i not in box: continue
        x,y,w,hh=map(float,vm.groups()); L,T,R,B=box[i]; P=8
        nx=min(x,L-P) if L<x-3 else x; ny=min(y,T-P) if T<y-3 else y
        nr=max(x+w,R+P) if R>x+w+3 else x+w; nb=max(y+hh,B+P) if B>y+hh+3 else y+hh
        if (nx,ny,nr,nb)==(x,y,x+w,y+hh): continue
        nf=f.replace(vm.group(0),'viewBox="%g %g %g %g"'%(nx,ny,nr-nx,nb-ny),1)
        out=out[:a]+nf+out[b:]; changed+=1
        print('%s fig %d: %s -> %g %g %g %g'%(p.split('/')[-2],i,vm.group(0)[9:-1],nx,ny,nr-nx,nb-ny))
    if changed: open(p,'w').write(out)
