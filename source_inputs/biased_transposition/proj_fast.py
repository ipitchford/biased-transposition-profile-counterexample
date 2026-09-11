import numpy as np, sys, time
from exact_tv import build_swap_index, t_star
from run_families import families
n=int(sys.argv[1]); T=int(sys.argv[2])
cache=build_swap_index(n); P,idx,fixed_cnt=cache; N=P.shape[0]
fixedmat=(P==np.arange(n,dtype=np.int8)[None,:])
key_set=(fixedmat.astype(np.int64)*(2**np.arange(n))[None,:]).sum(1)
fams=families(n)
for fam in sys.argv[3].split(','):
    p=fams[fam]; classes=np.unique(np.round(p*n,6)); cls=np.array([np.where(classes==round(x*n,6))[0][0] for x in p])
    # class-refined fixed counts key
    counts=np.stack([fixedmat[:,cls==k].sum(1) for k in range(len(classes))],1)
    key_cls=np.zeros(N,dtype=np.int64)
    for k in range(counts.shape[1]): key_cls=key_cls*(n+1)+counts[:,k]
    key_tot=fixed_cnt.astype(np.int64)
    q=float(np.sum(p**2)); dist=np.zeros(N); dist[0]=1; unif=1/N
    print("family",fam,"n",n,"classes(x n):",classes.tolist(),"t*=%.2f"%t_star(p))
    print("   t    d(t)    fixed-set   class-refined counts   total count")
    for t in range(T+1):
        if t%3==0 or abs(t-t_star(p))<1.5:
            d=0.5*np.abs(dist-unif).sum()
            vals=[]
            for key in (key_set,key_cls,key_tot):
                a=np.bincount(key,weights=dist); b=np.bincount(key)/N; vals.append(0.5*np.abs(a-b).sum())
            print("  %3d  %.5f   %.5f   %.5f   %.5f"%(t,d,*vals),flush=True)
        new=q*dist
        for (i,j),ind in idx.items(): new+=2*p[i]*p[j]*dist[ind]
        dist=new
