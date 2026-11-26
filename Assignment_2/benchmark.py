"""Timing for closest.py. Writes results.json."""
import json, platform, random, sys, time
from closest import closest_pair, closest_pair_brute

def make(n, seed):
    r = random.Random(seed)
    return [(r.randint(0, 10**6), r.randint(0, 10**6)) for _ in range(n)]

def best_of(f, pts, reps):
    best = float("inf")
    for _ in range(reps):
        t = time.perf_counter(); f(pts); best = min(best, time.perf_counter() - t)
    return best

res = {"python": platform.python_version(), "machine": platform.processor() or platform.machine(), "main": [], "cross": []}
prev = None
for n in [1000, 2000, 4000, 8000, 16000, 32000, 64000]:
    pts = make(n, n)
    assert abs(closest_pair(pts)[0] - closest_pair_brute(pts)[0]) < 1e-9 if n <= 4000 else True
    dc = best_of(closest_pair, pts, 3)
    if prev is not None and prev * 4 > 60:
        bf = None                                  # predicted > 60 s: stopped
    else:
        bf = best_of(closest_pair_brute, pts, 3 if n <= 4000 else 1)
        prev = bf
    res["main"].append({"n": n, "dc": dc, "brute": bf})
    print(n, dc, bf, flush=True)

for n in list(range(4, 60, 2)) + list(range(60, 301, 10)):
    pts = make(n, 1000 + n)
    inner = max(1, 2000 // n)
    def rep(f):
        best = float("inf")
        for _ in range(25):
            t = time.perf_counter()
            for _ in range(inner): f(pts)
            best = min(best, (time.perf_counter() - t) / inner)
        return best
    res["cross"].append({"n": n, "dc": rep(closest_pair), "brute": rep(closest_pair_brute)})
json.dump(res, open("results.json", "w"), indent=1)
print("done", flush=True)
