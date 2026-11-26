import random, statistics as st
from booking import *

def gen_indep(rng, n=50):
    out=[]
    for _ in range(n):
        s=rng.randint(0,168); d=rng.randint(1,12)
        out.append((s,s+d,rng.randint(1000,20000)))
    return out

def gen_prop(rng, n=50):
    out=[]
    for _ in range(n):
        s=rng.randint(0,168); d=rng.randint(1,12)
        out.append((s,s+d,d*rng.randint(800,1200)))
    return out

def run(gen, seed):
    rng=random.Random(seed)
    ratios={'ef':[], 'hf':[]}
    for _ in range(1000):
        r=gen(rng)
        opt=best_schedule(r)[0]
        ratios['ef'].append(greedy_earliest_finish(r)[0]/opt)
        ratios['hf'].append(greedy_highest_fee(r)[0]/opt)
    return {k:(st.mean(v),min(v)) for k,v in ratios.items()}

print('independent', run(gen_indep,4))
print('proportional', run(gen_prop,4))

# how many random small tests pass before first failure (Q1)
rng=random.Random(1)
def small(rng):
    n=rng.randint(2,4); out=[]
    for _ in range(n):
        s=rng.randint(0,10); out.append((s,s+rng.randint(1,5),rng.randint(1,10)))
    return out
for name,f in (('ef',greedy_earliest_finish),('hf',greedy_highest_fee)):
    fails=0; trials=2000
    first=None
    for t in range(trials):
        r=small(rng)
        if f(r)[0]!=best_schedule(r)[0]:
            fails+=1
            if first is None: first=t+1
    print(name,'fail rate small',fails/trials,'first fail at',first)

# sanity: also first failing for hand-written tests: the brief example
# timing
import time
for n in (1000,10000):
    r=gen_indep(random.Random(2),n)
    for f in (greedy_earliest_finish,greedy_highest_fee,best_schedule):
        t=time.time(); f(r); print(n,f.__name__,round(time.time()-t,4))
# DP vs brute at n=15
rng=random.Random(5); ok=True
for _ in range(100):
    r=gen_indep(rng,15)
    ok&= best_schedule(r)[0]==brute_force(r)[0]
print('n=15 match',ok)
