"""Assignment 2: Closest Camera Traps (closest pair of points)."""
import math


def closest_pair_brute(points):
    """Check every pair: Theta(n^2). Returns (d, i, j) with i < j."""
    n = len(points)
    if n < 2:
        raise ValueError("need at least 2 points")
    best = None                                  # (squared distance, i, j)
    for i in range(n - 1):
        xi, yi = points[i]
        for j in range(i + 1, n):
            dx = xi - points[j][0]
            dy = yi - points[j][1]
            d2 = dx * dx + dy * dy
            if best is None or d2 < best[0]:
                best = (d2, i, j)
    return (math.sqrt(best[0]), best[1], best[2])


def _brute(pts):
    """Brute force on a small list of (x, y, original_index) triples."""
    best = None
    for a in range(len(pts) - 1):
        for b in range(a + 1, len(pts)):
            dx = pts[a][0] - pts[b][0]
            dy = pts[a][1] - pts[b][1]
            i, j = pts[a][2], pts[b][2]
            cand = (dx * dx + dy * dy, min(i, j), max(i, j))
            if best is None or cand < best:
                best = cand
    return best


def _solve(px):
    """px is sorted by x. Returns (best, py): best = (d^2, i, j), py = px sorted by y."""
    n = len(px)
    if n <= 3:                                   # base case
        return _brute(px), sorted(px, key=lambda p: p[1])
    mid = n // 2
    mid_x = px[mid][0]                           # dividing line
    best_l, py_l = _solve(px[:mid])              # T(n/2)
    best_r, py_r = _solve(px[mid:])              # T(n/2)
    best = min(best_l, best_r)
    # Merge the two y-sorted halves (two sorted runs -> linear merge)
    py = sorted(py_l + py_r, key=lambda p: p[1])
    # Strip of width 2*delta around the dividing line, kept in y order
    d2 = best[0]
    strip = [p for p in py if (p[0] - mid_x) ** 2 < d2]
    for a in range(len(strip) - 1):
        for b in range(a + 1, len(strip)):
            dy = strip[b][1] - strip[a][1]
            if dy * dy >= best[0]:               # too far apart in y: stop
                break
            dx = strip[a][0] - strip[b][0]
            i, j = strip[a][2], strip[b][2]
            cand = (dx * dx + dy * dy, min(i, j), max(i, j))
            if cand < best:
                best = cand
    return best, py


def closest_pair(points):
    """Divide and conquer, Theta(n log n). Returns (d, i, j) with i < j."""
    if len(points) < 2:
        raise ValueError("need at least 2 points")
    px = sorted((x, y, i) for i, (x, y) in enumerate(points))   # sort by x
    best, _ = _solve(px)
    return (math.sqrt(best[0]), best[1], best[2])
