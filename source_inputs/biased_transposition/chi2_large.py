import time, numpy as np, math, json, sys
from spectrum import two_class_spectrum, chi2_from_spectrum
from exact_tv import t_star, U_of_t
n=int(sys.argv[1]); be=float(sys.argv[2])
res={}
for m in [int(x) for x in sys.argv[3].split(',')]:
    al=(n-(n-m)*be)/m
    if al<=be: continue
    p=np.array([al/n]*m+[be/n]*(n-m)); assert abs(p.sum()-1)<1e-12
    t0=time.time(); spec=two_class_spectrum(n,m,al,be); 
    ts=t_star(p)
    # chi2 mixing time: first t with chi2<=1 (and <=0.25)
    def tchi(th):
        t=0
        while chi2_from_spectrum(spec,t)>th: t+=1
        return t
    # standard-rep lower bound: (n-1) * sum over label-chain nonzero eigenvalues (1-lam)^{2t}
    D=np.diag(2*p); L=D-2*np.outer(p,p); lam=np.sort(np.linalg.eigvalsh(L))[1:]
    def lb(t): return (n-1)*np.sum((1-lam)**(2*t))
    tc1,tc4=tchi(1.0),tchi(0.25)
    ta=int(math.ceil(ts))
    print('n=%d m=%2d al=%.3f be=%.2f  t*=%6.2f  t_chi2(<=1)=%3d  t_chi2(<=.25)=%3d  chi2(t*)=%9.3f  std-rep LB(t*)=%9.3f  U(2t*)*(n-1)=%8.3f  [%.0fs]'%(n,m,al,be,ts,tc1,tc4,chi2_from_spectrum(spec,ta),lb(ta),(n-1)*U_of_t(p,2*ta),time.time()-t0),flush=True)
    res[m]={'t_star':ts,'tchi1':tc1,'tchi4':tc4,'chi2_tstar':chi2_from_spectrum(spec,ta),'lb_tstar':float(lb(ta)),'al':al,'be':be}
json.dump(res,open('chi2_n%d_be%g.json'%(n,be),'w'))
