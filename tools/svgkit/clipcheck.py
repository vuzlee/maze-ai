# Usage: python3 tools/svgkit/clipcheck.py <page.html>...  -> lists figures whose visible content spills outside the viewBox (final state).
# For every figure of the given pages: render final state (reduced motion), measure visible content vs viewBox.
import re,sys,subprocess,os,glob
css=os.path.abspath('assets/style.css')
JS='''<script>
const out=[];document.querySelectorAll("figure svg[viewBox]").forEach((s,i)=>{const v=s.viewBox.baseVal,sr=s.getBoundingClientRect(),k=sr.width/v.width;
let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
s.querySelectorAll("text,rect,line,path,circle,polygon,ellipse").forEach(e=>{let g=e,hid=false;while(g&&g!==s){if(getComputedStyle(g).opacity==="0"||g.getAttribute("opacity")==="0"){hid=true;break}g=g.parentElement}if(hid)return;
const r=e.getBoundingClientRect();if(r.width===0&&r.height===0)return;x0=Math.min(x0,r.left);y0=Math.min(y0,r.top);x1=Math.max(x1,r.right);y1=Math.max(y1,r.bottom)});
const L=(x0-sr.left)/k+v.x,T=(y0-sr.top)/k+v.y,R=(x1-sr.left)/k+v.x,B=(y1-sr.top)/k+v.y;
const bad=[];if(L<v.x-1)bad.push("left "+Math.round(v.x-L));if(T<v.y-1)bad.push("top "+Math.round(v.y-T));if(R>v.x+v.width+1)bad.push("right "+Math.round(R-v.x-v.width));if(B>v.y+v.height+1)bad.push("bottom "+Math.round(B-v.y-v.height));
if(bad.length)out.push(i+": "+bad.join(", "))});
const p=document.createElement("pre");p.id="CLIP";p.textContent=out.join("\\n")||"clean";document.body.appendChild(p);
</script>'''
for p in sys.argv[1:]:
    h=open(p).read(); figs=re.findall(r'<figure class="gist">.*?</figure>',h,re.S)
    page='<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="file://%s"><style>body{background:var(--bg);margin:16px;width:780px}</style>%s%s'%(css,''.join(figs),JS)
    open('/tmp/fix/clip.html','w').write(page)
    r=subprocess.run(['google-chrome','--headless','--no-sandbox','--force-prefers-reduced-motion','--virtual-time-budget=3000','--dump-dom','file:///tmp/fix/clip.html'],capture_output=True,text=True)
    m=re.search(r'<pre id="CLIP">(.*?)</pre>',r.stdout,re.S)
    res=m.group(1).strip() if m else 'NO RESULT'
    if res!='clean': print('==',p.split('/')[-2]); print('  '+res.replace('\n','\n  '))
