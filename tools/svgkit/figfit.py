# figfit.py page.html ... : sample every animated figure over its timeline, measure the union bbox of everything drawn,
# and rewrite its viewBox so nothing is cut off (pad 6). Run after generating figures.
import sys,re,os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'figcheck.py')).read().split("call(\"Page.enable\")")[0])
JS=r"""
(async()=>{
 const res=[];
 for(const sv of document.querySelectorAll('figure svg[data-anim]')){
   const anims=document.getAnimations().filter(a=>a.effect&&sv.contains(a.effect.target));
   const dur=Math.max(0,...anims.map(a=>a.effect.getTiming().duration||0));
   const vb=sv.viewBox.baseVal; const ctm=sv.getScreenCTM().inverse();
   let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
   const ts=[]; for(let t=0;t<=dur;t+=Math.max(200,dur/25)) ts.push(t); ts.push(dur);
   for(const t of ts){
     anims.forEach(a=>{a.pause();a.currentTime=t;});
     for(const e of sv.querySelectorAll('text,rect,circle,ellipse,path,line,polygon')){
       let o=1,n=e; while(n&&n!==sv){o*=parseFloat(getComputedStyle(n).opacity);n=n.parentElement;}
       if(o<0.05) continue;
       const r=e.getBoundingClientRect(); if(!r.width&&!r.height) continue;
       const p=new DOMPoint(r.left,r.top).matrixTransform(ctm), q=new DOMPoint(r.right,r.bottom).matrixTransform(ctm);
       x0=Math.min(x0,p.x);y0=Math.min(y0,p.y);x1=Math.max(x1,q.x);y1=Math.max(y1,q.y);
     }
   }
   res.push([vb.x,vb.width,vb.height,x0,y0,x1,y1]);
 }
 return res;
})()
"""
call("Page.enable")
for path in sys.argv[1:]:
    call("Page.navigate",{"url":"file://"+os.path.abspath(path)}); time.sleep(1.4)
    boxes=ev(JS) or []
    src=open(path).read(); k=[0]; ch=[]
    def fix(m):
        i=k[0]; k[0]+=1
        if i>=len(boxes): return m.group(0)
        vx,w,h,x0,y0,x1,y1=boxes[i]
        nx=min(0,round(x0-4)); ny=min(0,round(y0-4)); nw=max(round(vx+w),round(x1+6))-nx; nh=max(round(y1+8),40)-ny
        if abs(nx)>.5 or abs(ny)>.5 or abs(nw-w)>.5 or abs(nh-h)>2: ch.append(f"fig{i+1}: {w:.0f}x{h:.0f} → {nw:.0f}x{nh:.0f}")
        return f'<svg viewBox="{nx:.0f} {ny:.0f} {nw:.0f} {nh:.0f}"'
    src=re.sub(r'<svg viewBox="[^"]*"(?=[^>]*data-anim)',fix,src)
    open(path,"w").write(src)
    print(path.split('/')[-2],"|"," · ".join(ch) or "ok")
p.kill()
