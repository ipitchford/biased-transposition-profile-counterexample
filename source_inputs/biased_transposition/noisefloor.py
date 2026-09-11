import numpy as np, math, sys
from montecarlo import stats, emp_tv, emp_tv_joint
n=2000; R=20000; rng=np.random.default_rng(7)
for m in (45,1000,200,600):
    slow=np.zeros(n,bool); slow[:m]=True
    A=np.array([rng.permutation(n) for _ in range(R)]); B=np.array([rng.permutation(n) for _ in range(R)])
    sa=stats(A,slow); sb=stats(B,slow)
    line=["m=%d"%m]
    for key in ['fix_s','fix_f','two','two_slow','slow_at_slow','cyc']:
        line.append("%s %.3f"%(key,emp_tv(sa[key],sb[key])))
    line.append("pair %.3f"%emp_tv_joint([sa['fix_s'],sa['fix_f']],[sb['fix_s'],sb['fix_f']]))
    print("  ".join(line),flush=True)
