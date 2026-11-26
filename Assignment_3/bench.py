"""Assignment 3, Part C: benchmarks. Writes results.json and PNG graphs."""
import json, platform, random, sys, time
from sorts import quicksort_basic, quicksort_improved

random.seed(2026)
SIZES = [1000 * 2 ** k for k in range(7)]            # 1,000 ... 64,000
REPEATS = 3

def make(kind, n):
    if kind == "random":
        return [random.randint(0, 10**6) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    return [random.randint(0, 9) for _ in range(n)]  # duplicates

def best_time(f, data, repeats=REPEATS):
    best = None
    for _ in range(repeats):
        a = list(data)
        t = time.perf_counter()
        try:
            f(a)
        except RecursionError:
            return "RecursionError"
        dt = time.perf_counter() - t
        assert a == sorted(data)                       # brute-force check
        best = dt if best is None else min(best, dt)
    return best

res = {"env": f"Python {platform.python_version()} on {platform.platform()}"}
funcs = {
    "basic": quicksort_basic,
    "improved": lambda a: quicksort_improved(a, 16),
    "sorted()": lambda a: a.sort(),                   # reference only
}
res["scaling"] = {}
for kind in ("random", "sorted", "duplicates"):
    for name, f in funcs.items():
        res["scaling"][f"{kind}|{name}"] = [best_time(f, make(kind, n)) for n in SIZES]
        print(kind, name, res["scaling"][f"{kind}|{name}"], flush=True)

# comparison counts for basic quicksort on sorted input (below crash depth)
class C:
    cnt = 0
    def __init__(s, v): s.v = v
    def __le__(s, o): C.cnt += 1; return s.v <= o.v
res["counts"] = []
for n in (100, 200, 400, 800):
    C.cnt = 0
    quicksort_basic([C(i) for i in range(n)])
    res["counts"].append([n, C.cnt, n * (n - 1) // 2])

# crash threshold of the basic sort on sorted input
lo = 1
for n in range(100, 2000, 10):
    try:
        quicksort_basic(list(range(n)))
    except RecursionError:
        lo = n; break
res["crash_n_sorted"] = lo
res["recursion_limit"] = sys.getrecursionlimit()

# Lomuto-based improved on duplicates (ablation)
res["lomuto_dups"] = {}
for n in (2000, 4000, 8000, 16000):
    d = make("duplicates", n)
    res["lomuto_dups"][n] = [best_time(lambda a: quicksort_improved(a, 16, three_way=False), d, 1),
                             best_time(lambda a: quicksort_improved(a, 16), d)]
print(res["lomuto_dups"], flush=True)

# cutoff study, n = 100,000 random
data = make("random", 100000)
res["cutoff"] = {c: best_time(lambda a, c=c: quicksort_improved(a, c), data, 5) for c in (1, 4, 8, 16, 32, 64)}
res["cutoff_sorted_builtin"] = best_time(lambda a: a.sort(), data, 5)
print(res["cutoff"], res["cutoff_sorted_builtin"], flush=True)
json.dump(res, open("results.json", "w"), indent=1)
