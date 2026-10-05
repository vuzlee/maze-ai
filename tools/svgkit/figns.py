# give every animated <svg> its own class + keyframe names, so figures on one page don't override each other's timing
import re,sys
def fix(path):
    s=open(path).read(); n=[0]
    def one(m):
        svg=m.group(0); n[0]+=1; p=f"f{n[0]}-"
        st=re.search(r'<style>(.*?)</style>',svg,re.S)
        if not st: return svg
        css=st.group(1)
        if re.search(r'\.f\d+-',css): return svg
        kf=set(re.findall(r'@keyframes\s+([A-Za-z][\w-]*)',css))
        cl=set(c for c in re.findall(r'\.([A-Za-z][\w-]*)',css) if not c.startswith("sv-"))
        for k in sorted(kf,key=len,reverse=True): css=re.sub(r'(?<![\w-])'+re.escape(k)+r'(?![\w-])',p+k,css)
        for c in sorted(cl,key=len,reverse=True): css=re.sub(r'\.'+re.escape(c)+r'(?![\w-])','.'+p+c,css)
        body=svg[:st.start(1)]+css+svg[st.end(1):]
        def cls(mm):
            q=mm.group(1); toks=[p+t if t in cl else t for t in mm.group(2).split()]
            return f'class={q}{" ".join(toks)}{q}'
        return re.sub(r'class=(["\'])([^"\']*)\1',cls,body)
    s2=re.sub(r'<svg [^>]*data-anim.*?</svg>',one,s,flags=re.S)
    open(path,"w").write(s2); return n[0]
for p in sys.argv[1:]: print(p.split("/")[-2],fix(p))
