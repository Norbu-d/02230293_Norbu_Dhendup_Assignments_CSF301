"""Assignment 4: Booking the Hall (CSF302).

A request is a tuple (start, finish, fee). Two requests fit together if one
finishes no later than the other starts. Every function returns
(total_fee, chosen) where chosen is a sorted list of original indices.
"""
from bisect import bisect_right


def _by_finish(requests):
    """Indices sorted by finish time (ties: earlier start, then index)."""
    return sorted(range(len(requests)),
                  key=lambda i: (requests[i][1], requests[i][0], i))


def greedy_earliest_finish(requests):
    """Accept each request, in order of finish time, that fits. O(n log n)."""
    chosen, last_finish, total = [], None, 0
    for i in _by_finish(requests):
        start, finish, fee = requests[i]
        if last_finish is None or start >= last_finish:
            chosen.append(i)
            total += fee
            last_finish = finish
    return total, sorted(chosen)


def greedy_highest_fee(requests):
    """Accept each request, highest fee first, that fits. O(n^2) worst case."""
    order = sorted(range(len(requests)), key=lambda i: (-requests[i][2], i))
    chosen, total = [], 0
    for i in order:
        start, finish, fee = requests[i]
        # fits if it ends before, or starts after, every accepted request
        if all(finish <= requests[j][0] or requests[j][1] <= start
               for j in chosen):
            chosen.append(i)
            total += fee
    return total, sorted(chosen)


def best_schedule(requests):
    """Weighted interval scheduling by dynamic programming. O(n log n).

    With requests sorted by finish time, p(j) is the number of requests that
    finish no later than request j starts, and
        OPT(j) = max(OPT(j-1), fee_j + OPT(p(j))).
    """
    order = _by_finish(requests)
    n = len(order)
    finishes = [requests[i][1] for i in order]
    opt = [0] * (n + 1)          # opt[j] = best total using first j requests
    p = [0] * (n + 1)            # p[j] for 1-based request j
    for j in range(1, n + 1):
        start, _, fee = requests[order[j - 1]]
        p[j] = bisect_right(finishes, start, 0, j - 1)
        opt[j] = max(opt[j - 1], fee + opt[p[j]])
    chosen, j = [], n
    while j > 0:                 # walk back through the decisions
        fee = requests[order[j - 1]][2]
        if fee + opt[p[j]] > opt[j - 1]:
            chosen.append(order[j - 1])
            j = p[j]
        else:
            j -= 1
    return opt[n], sorted(chosen)


def brute_force(requests):
    """Try every subset. For checking only (n <= 15). O(n * 2^n)."""
    n = len(requests)
    if n > 15:
        raise ValueError("brute_force is limited to n <= 15")
    order = _by_finish(requests)
    best_total, best_set = 0, []
    for mask in range(1 << n):
        total, last_finish, ok, picked = 0, None, True, []
        for i in order:
            if mask >> i & 1:
                start, finish, fee = requests[i]
                if last_finish is not None and start < last_finish:
                    ok = False
                    break
                last_finish = finish
                total += fee
                picked.append(i)
        if ok and total > best_total:
            best_total, best_set = total, picked
    return best_total, sorted(best_set)
