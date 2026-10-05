# figcheck.py page.html ... : for every animated figure, sample times; report text boxes that overlap while both visible,
# and text that spills outside the svg.
import sys,subprocess,json,time,base64,os,socket,urllib.request,struct
port=int(os.environ.get('CDP_PORT','9334'))
chrome=os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome")
p=subprocess.Popen([chrome,"--headless=new","--disable-gpu",f"--remote-debugging-port={port}","--window-size=1100,1400","about:blank"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
for _ in range(50):
    try: tabs=json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json")); break
    except Exception: time.sleep(.2)
ws=[t for t in tabs if t["type"]=="page"][0]["webSocketDebuggerUrl"]
host,rest=ws[5:].split("/",1); h,pt=host.split(":")
s=socket.create_connection((h,int(pt))); key=base64.b64encode(os.urandom(16)).decode()
s.send(f"GET /{rest} HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
buf=b""
while b"\r\n\r\n" not in buf: buf+=s.recv(4096)
buf=buf.split(b"\r\n\r\n",1)[1]
def send(o):
    d=json.dumps(o).encode(); m=os.urandom(4); hd=bytearray([0x81]); n=len(d)
    if n<126: hd.append(0x80|n)
    elif n<65536: hd.append(0x80|126); hd+=struct.pack(">H",n)
    else: hd.append(0x80|127); hd+=struct.pack(">Q",n)
    s.send(bytes(hd)+m+bytes(b^m[i%4] for i,b in enumerate(d)))
def recv():
    global buf
    def need(k):
        global buf
        while len(buf)<k: buf+=s.recv(1<<20)
    need(2); b1=buf[1]&127; o=2
    if b1==126: need(4); n=struct.unpack(">H",buf[2:4])[0]; o=4
    elif b1==127: need(10); n=struct.unpack(">Q",buf[2:10])[0]; o=10
    else: n=b1
    need(o+n); d=buf[o:o+n]; buf=buf[o+n:]; return json.loads(d)
mid=[0]
def call(m,pr=None):
    mid[0]+=1; send({"id":mid[0],"method":m,"params":pr or {}})
    while True:
        r=recv()
        if r.get("id")==mid[0]: return r.get("result",{})
def ev(js): return call("Runtime.evaluate",{"expression":js,"returnByValue":True,"awaitPromise":True}).get("result",{}).get("value")
JS=r"""
(async()=>{
 const out=[]; const svgs=[...document.querySelectorAll('figure svg[data-anim]')];
 const heads=[...document.querySelectorAll('h2,h3.ssh')];
 for(const [fi,sv] of svgs.entries()){
   const anims=document.getAnimations().filter(a=>a.effect&&sv.contains(a.effect.target));
   const dur=Math.max(0,...anims.map(a=>a.effect.getTiming().duration||0));
   let title=''; for(const h of heads){ if(h.compareDocumentPosition(sv)&Node.DOCUMENT_POSITION_FOLLOWING) title=h.textContent.replace(/^[\d.]+/,'').trim(); }
   const svr=sv.getBoundingClientRect(); const seen=new Set();
   const ts=[]; for(let t=0;t<=dur;t+=Math.max(150,dur/40)) ts.push(t); ts.push(dur);
   for(const t of ts){
     anims.forEach(a=>{a.pause();a.currentTime=t;});
     const tx=[...sv.querySelectorAll('text')].map(e=>{
       let o=1,n=e; while(n&&n!==sv){o*=parseFloat(getComputedStyle(n).opacity);n=n.parentElement;}
       const r=e.getBoundingClientRect(); return {e,o,r,s:e.textContent.trim()};
     }).filter(x=>x.o>0.35&&x.s&&x.r.width>0);
     for(let i=0;i<tx.length;i++){
       const a=tx[i];
       if(a.r.right>svr.right+1||a.r.left<svr.left-1||a.r.bottom>svr.bottom+1||a.r.top<svr.top-1){
         const k='spill|'+a.s; if(!seen.has(k)){seen.add(k);out.push([fi,title,Math.round(t),'SPILL',a.s]);}
       }
       for(let j=i+1;j<tx.length;j++){
         const b=tx[j]; if(a.s===b.s && Math.abs(a.r.x-b.r.x)<1 && Math.abs(a.r.y-b.r.y)<1 && Math.abs(a.r.width-b.r.width)<1.5) continue;
         if(a.o<0.3||b.o<0.3) continue;
         const w=Math.min(a.r.right,b.r.right)-Math.max(a.r.left,b.r.left), h=Math.min(a.r.bottom,b.r.bottom)-Math.max(a.r.top,b.r.top);
         const later=(a.e.compareDocumentPosition(b.e)&Node.DOCUMENT_POSITION_FOLLOWING)?b:a, earlier=later===b?a:b;
         const grp=later.e.closest('g[class]')||later.e.parentElement;
         const cx=earlier.r.x+earlier.r.width/2, cy=earlier.r.y+earlier.r.height/2;
         const hid=[...grp.querySelectorAll('rect')].some(rc=>{const f=getComputedStyle(rc).fill; if(!f||f==='none'||f.startsWith('rgba')&&f.endsWith(', 0)')) return false;
            if(rc.compareDocumentPosition(earlier.e)&Node.DOCUMENT_POSITION_FOLLOWING && grp.contains(earlier.e)) return false;
            const q=rc.getBoundingClientRect(); return cx>=q.left&&cx<=q.right&&cy>=q.top&&cy<=q.bottom;});
         if(hid) continue;
         if(w>2&&h>3){ const k=[a.s,b.s].sort().join('|'); if(!seen.has(k)){seen.add(k);out.push([fi,title,Math.round(t),'OVERLAP',a.s+'  ⟂  '+b.s]);} }
       }
     }
   }
 }
 return out;
})()
"""
call("Page.enable")
for path in sys.argv[1:]:
    call("Page.navigate",{"url":"file://"+os.path.abspath(path)}); time.sleep(1.4)
    res=ev(JS) or []
    name=path.split('/')[-2]
    for r in res: print(f"{name} | fig{r[0]+1} {r[1]} | t={r[2]}ms | {r[3]} | {r[4]}")
    if not res: print(f"{name} | clean")
p.kill()
