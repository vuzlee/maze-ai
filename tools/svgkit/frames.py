# usage: frames.py file.html fig_index out_prefix t1 t2 ...  -> pauses all animations at time t (s) and screenshots the figure
import sys,subprocess,json,time,base64,os,socket,urllib.request
import http.client
path,idx,out=sys.argv[1],int(sys.argv[2]),sys.argv[3]; ts=[float(x) for x in sys.argv[4:]]
port=int(os.environ.get('CDP_PORT','9333'))
chrome=os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome")
if not os.path.exists(chrome): chrome="google-chrome"
p=subprocess.Popen([chrome,"--headless=new","--disable-gpu",f"--remote-debugging-port={port}","--window-size=1100,1400","about:blank"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
for _ in range(50):
    try: tabs=json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json")); break
    except Exception: time.sleep(.2)
ws_url=[t for t in tabs if t["type"]=="page"][0]["webSocketDebuggerUrl"]
# minimal websocket client
import hashlib,struct
host,rest=ws_url[5:].split("/",1)
s=socket.create_connection(host.split(":")[0:1][0] and (host.split(":")[0],int(host.split(":")[1])))
key=base64.b64encode(os.urandom(16)).decode()
s.send(f"GET /{rest} HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
buf=b""
while b"\r\n\r\n" not in buf: buf+=s.recv(4096)
buf=buf.split(b"\r\n\r\n",1)[1]
def send(o):
    d=json.dumps(o).encode(); m=os.urandom(4); h=bytearray([0x81])
    n=len(d)
    if n<126: h.append(0x80|n)
    elif n<65536: h.append(0x80|126); h+=struct.pack(">H",n)
    else: h.append(0x80|127); h+=struct.pack(">Q",n)
    s.send(bytes(h)+m+bytes(b^m[i%4] for i,b in enumerate(d)))
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
call("Page.enable"); call("Page.navigate",{"url":"file://"+os.path.abspath(path)}); time.sleep(1.5)
def ev(js): return call("Runtime.evaluate",{"expression":js,"returnByValue":True}).get("result",{}).get("value")
rect=ev(f"""(()=>{{document.documentElement.style.scrollBehavior='auto';const s=[...document.querySelectorAll('figure svg')][{idx}];s.scrollIntoView({{block:'center',behavior:'instant'}});const r=s.getBoundingClientRect();return [r.x,r.y,r.width,r.height];}})()""")
time.sleep(1.0)   # let the page's IntersectionObserver fire its restart BEFORE we pause, or it would undo the pause
rect=ev(f"""(()=>{{const s=[...document.querySelectorAll('figure svg')][{idx}];const r=s.getBoundingClientRect();return [r.x+scrollX,r.y+scrollY,r.width,r.height];}})()""")
for t in ts:
    ev(f"""(()=>{{const s=[...document.querySelectorAll('figure svg')][{idx}];document.getAnimations().filter(a=>a.effect&&s.contains(a.effect.target)).forEach(a=>{{a.pause();a.currentTime={t*1000};}});}})()""")
    time.sleep(.15)
    r=call("Page.captureScreenshot",{"format":"png","captureBeyondViewport":True,"clip":{"x":rect[0],"y":rect[1],"width":rect[2],"height":rect[3],"scale":1}})
    open(f"{out}_{t:05.2f}.png","wb").write(base64.b64decode(r["data"]))
p.kill()
print(len(ts),"frames",rect)
