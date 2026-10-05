import math
def lin(a,b): return a[0]*b[0]+a[1]*b[1]
def rbf(g): return lambda a,b: math.exp(-g*((a[0]-b[0])**2+(a[1]-b[1])**2))
def smo(X,y,C,K=lin,tol=1e-9,maxit=20000):
    n=len(X); Km=[[K(X[i],X[j]) for j in range(n)] for i in range(n)]
    a=[0.0]*n; b=0.0
    def f(i): return sum(a[j]*y[j]*Km[j][i] for j in range(n) if a[j])+b
    it=0
    while it<maxit:
        it+=1; ch=0
        for i in range(n):
            Ei=f(i)-y[i]
            if not ((y[i]*Ei< -1e-7 and a[i]<C-1e-12) or (y[i]*Ei>1e-7 and a[i]>1e-12)): continue
            E=[f(k)-y[k] for k in range(n)]
            order=sorted([k for k in range(n) if k!=i],key=lambda k:-abs(Ei-E[k]))
            for j in order:
                Ej=E[j]; ai,aj=a[i],a[j]
                if y[i]!=y[j]: Lo,Hi=max(0,aj-ai),min(C,C+aj-ai)
                else: Lo,Hi=max(0,ai+aj-C),min(C,ai+aj)
                if Hi-Lo<1e-12: continue
                eta=2*Km[i][j]-Km[i][i]-Km[j][j]
                if eta>=-1e-12: continue
                nj=min(Hi,max(Lo,aj-y[j]*(Ei-Ej)/eta))
                if abs(nj-aj)<1e-10: continue
                ni=ai+y[i]*y[j]*(aj-nj)
                b1=b-Ei-y[i]*(ni-ai)*Km[i][i]-y[j]*(nj-aj)*Km[i][j]
                b2=b-Ej-y[i]*(ni-ai)*Km[i][j]-y[j]*(nj-aj)*Km[j][j]
                a[i],a[j]=ni,nj
                b=b1 if 0<ni<C else (b2 if 0<nj<C else (b1+b2)/2)
                ch+=1; break
        if ch==0: break
    free=[i for i in range(n) if 1e-6<a[i]<C-1e-6]
    if free:
        b=sum(y[i]-sum(a[j]*y[j]*Km[j][i] for j in range(n)) for i in free)/len(free)
    return a,b
def wvec(X,y,a): return (sum(a[i]*y[i]*X[i][0] for i in range(len(X))),sum(a[i]*y[i]*X[i][1] for i in range(len(X))))
