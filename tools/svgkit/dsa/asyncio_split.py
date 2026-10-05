"""Event-loop figures for content/02-python/04-concurrency/asyncio (sections aio-s2-1/2, aio-s2-4/5)."""
import sys,os,json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from engine import *
PT,MID,TG,RS='var(--brand)','var(--violet)','var(--filled)','var(--rose)'
LH=20
class Code2:
    def __init__(s,x,y,lines,w): s.x,s.y,s.lines,s.w=x,y,lines,w
    def svg(s):
        o=R(s.x,s.y,s.w,len(s.lines)*LH+14,'var(--bg)',RULE_HI,8)
        for i,l in enumerate(s.lines): o+=T(s.x+14,s.y+22+i*LH,l.replace(' ','\u00a0'),TX,'start',mono=True)
        return o
    def bar(s): return R(s.x+4,s.y+8,s.w-8,LH,'rgba(var(--violet-a),.13)','none',4)+R(s.x+4,s.y+8,3,LH,MID,'none',1.5)
def box(x,y,w,h,label,sub=None,c=PT,fill='var(--bg)'):
    o=R(x,y,w,h,fill,c,8,1.6)+T(x+w/2,y+(24 if sub else h/2+5),label,c,mono=True,bold=True)
    if sub: o+=T(x+w/2,y+42,sub,MU)
    return o
def badge(x,y,text,c=MID,w=None):   # opaque, so a newer badge hides the older one
    w=w or 20+len(text)*7.4
    return R(x,y,w,24,'var(--bg)','none',12)+R(x,y,w,24,'rgba(var(--violet-a),.08)' if c==MID else 'var(--bg)',c,12,1.3)+T(x+w/2,y+16,text,c,mono=True,bold=True)
def flags(x,y,run,closed,c=MID):
    return R(x,y,210,26,'var(--bg)','none',6)+T(x,y+17,'is_running=%s  is_closed=%s'%(run,closed),c,'start',mono=True)
figs={}

# 2.1 Startup
code=Code2(0,40,['asyncio.run(main()):','  loop = new_event_loop()','  task = loop.create_task(main())','  loop.run_forever()'],290)
f=Anim('aio-s21a-',720,250,'asyncio.run first creates a new event loop, then wraps the main coroutine in a Task, then runs the loop. The loop repeats its pass thousands of times while main is running.','STARTUP · asyncio.run BUILDS ONE LOOP, THEN SPINS IT',2.5)
f.static(code.svg())
LX,LY,LW,LHh=360,50,340,150
f.show(R(LX,LY,LW,LHh,'var(--bg)',PT,10,1.6)+T(LX+14,LY+22,'event loop',PT,'start',mono=True,bold=True),2.0)
f.show(box(LX+20,LY+40,180,50,'Task(main())','pending'),4.0)
f.show(badge(LX+20,LY+108,'idle'),2.2,hide=6.0)
for i,n in enumerate(['pass 1','pass 2','pass 3','pass 4,812']):
    t=6.0+i*0.9
    f.show(badge(LX+20,LY+108,'running · '+n,w=200),t,hide=None if i==3 else t+0.9)
f.show(T(LX+230,LY+70,'↻',MID,bold=True),6.0)
f.show(T(0,LY+150,'set up once · the loop inside turns thousands of times',MU,'start'),9.8)
f.path(code.bar(),[(0,0,0),(2.0,0,LH),(4.0,0,2*LH),(6.0,0,3*LH)],.5)
figs['a']=f.render()

# 2.2 Teardown
code=Code2(0,40,['# main() returned','loop.stop()','loop.shutdown_asyncgens()','loop.close()'],290)
f=Anim('aio-s22a-',720,250,'When main finishes the loop stops, open async generators are closed, then the loop is closed: is_closed becomes True and it cannot be reused.','TEARDOWN · STOP → CLEAN UP → CLOSE, EXACTLY ONCE',2.5)
f.static(code.svg())
f.static(R(LX,LY,LW,LHh,'var(--bg)',PT,10,1.6)+T(LX+14,LY+22,'event loop',PT,'start',mono=True,bold=True))
f.show(box(LX+20,LY+40,180,50,'Task(main())','pending'),0,hide=0.9)
f.show(box(LX+20,LY+40,180,50,'Task(main())','done',c=TG),0.9)
f.show(badge(LX+20,LY+108,'running',w=200),0,hide=2.2)
f.show(badge(LX+20,LY+108,'stopped',w=200),2.2)
f.show(box(LX+214,LY+40,110,50,'async gen','open'),0.4,hide=4.2)
f.show(box(LX+214,LY+40,110,50,'async gen','closed',c='var(--ghost)',fill='var(--sunk)'),4.2)
f.show(R(LX,LY,LW,LHh,'var(--sunk)','var(--ghost)',10,1.6)+T(LX+14,LY+22,'event loop',FA,'start',mono=True,bold=True)+T(LX+LW/2,LY+82,'closed',FA,mono=True,bold=True)+badge(LX+20,LY+108,'is_closed = True',w=200),6.4)
f.show(T(0,LY+150,'next asyncio.run builds a brand-new loop',MU,'start'),7.0)
f.path(code.bar(),[(0,0,0),(2.2,0,LH),(4.2,0,2*LH),(6.4,0,3*LH)],.5)
figs['b']=f.render()

# 2.4 Closed is final
code=Code2(0,40,['lp = new_event_loop()','lp.run_until_complete(c())','lp.close()','lp.run_until_complete(c())'],290)
f=Anim('aio-s24a-',720,230,'A loop goes new, running, closed. The flags track it: is_running True only while running, is_closed True after close. Running a closed loop again raises RuntimeError: Event loop is closed.','LOOP STATES · CLOSED IS FINAL',2.5)
f.static(code.svg())
BX,BY=360,50
f.show(box(BX,BY,240,50,'loop','new'),.4,hide=2.0)
f.show(flags(BX,BY+64,'False','False'),.4,hide=2.0)
f.show(box(BX,BY,240,50,'loop','running',c=MID),2.0,hide=4.0)
f.show(flags(BX,BY+64,'True ','False'),2.0,hide=4.0)
f.show(box(BX,BY,240,50,'loop','closed',c='var(--ghost)',fill='var(--sunk)'),4.0)
f.show(flags(BX,BY+64,'False','True',PT),4.0)
f.show(R(BX,BY+104,320,46,'var(--bg)',RS,8,1.6)+T(BX+14,BY+124,'RuntimeError:',RS,'start',mono=True,bold=True)+T(BX+14,BY+141,'Event loop is closed',RS,'start',mono=True),6.2)
f.show(T(0,BY+150,'also: asyncio.run() inside a running loop → RuntimeError',MU,'start'),7.0)
f.path(code.bar(),[(0,0,0),(2.0,0,LH),(4.0,0,2*LH),(6.0,0,3*LH)],.5)
figs['c']=f.render()

# 2.5 Pending task cancelled
code=Code2(0,40,['async def main():','  t = create_task(sleep(5))','  return  # no await t','# asyncio.run cleans up'],290)
f=Anim('aio-s25a-',720,230,'main starts a task that sleeps 5 seconds and returns without awaiting it. At shutdown asyncio.run cancels every task still pending, so the task ends with cancelled=True and its work never finishes.','A TASK STILL PENDING AT CLOSE · CANCELLED',2.5)
f.static(code.svg())
f.show(box(BX,BY,240,50,'task t','in sleep(5)'),2.0,hide=6.0)
f.show(badge(BX,BY+64,'pending',w=240),2.0,hide=6.0)
f.show(T(BX,BY+112,'main() returned · t never awaited',MU,'start'),4.0,hide=6.0)
f.show(box(BX,BY,240,50,'task t','CANCELLED',c=RS),6.0)
f.show(badge(BX,BY+64,'cancelled=True',c=RS,w=240),6.0)
f.show(T(BX,BY+112,'gather your tasks before main() returns',TG,'start',bold=True),7.0)
f.path(code.bar(),[(0,0,0),(2.0,0,LH),(4.0,0,2*LH),(6.0,0,3*LH)],.5)
figs['d']=f.render()
json.dump(figs,open('/tmp/aio/figs.json','w'))
