"""Assignment 3: Fixing a slow quicksort (sorts.py).

quicksort_basic    : Lomuto partition, last element as pivot.
quicksort_improved : random pivot, insertion sort for small parts,
                     recurse on the smaller part and loop on the larger.
Neither function uses sorted() or list.sort().
"""
import random


def quicksort_basic(a):
    """Sort list a in place (ascending). Last element is the pivot."""
    _basic(a, 0, len(a) - 1)


def _basic(a, lo, hi):
    if lo >= hi:
        return
    p = _lomuto(a, lo, hi)
    _basic(a, lo, p - 1)
    _basic(a, p + 1, hi)


def _lomuto(a, lo, hi):
    """Partition a[lo..hi] around a[hi]; return the pivot's final index."""
    pivot = a[hi]
    i = lo                      # a[lo..i-1] holds items <= pivot
    for j in range(lo, hi):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i


def _insertion(a, lo, hi):
    """Insertion sort on a[lo..hi] (inclusive)."""
    for i in range(lo + 1, hi + 1):
        x = a[i]
        j = i - 1
        while j >= lo and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


def quicksort_improved(a, cutoff=16, three_way=True):
    """Sort list a in place. Random pivot, insertion sort for parts of size
    <= cutoff, recursion only on the smaller part (depth O(log n)).
    three_way=True splits into <, ==, > so repeated values are not
    re-sorted; three_way=False uses Lomuto (kept only for the report's
    comparison)."""
    _improved(a, 0, len(a) - 1, max(cutoff, 1), three_way)


def _improved(a, lo, hi, cutoff, three_way):
    while hi - lo + 1 > cutoff:
        if three_way:
            p = a[random.randint(lo, hi)]
            lt, i, gt = lo, lo, hi      # a[lo:lt] < p, a[lt:i] == p, a[gt+1:] > p
            while i <= gt:
                if a[i] < p:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif a[i] > p:
                    a[i], a[gt] = a[gt], a[i]
                    gt -= 1
                else:
                    i += 1
            left_hi, right_lo = lt - 1, gt + 1
        else:
            r = random.randint(lo, hi)
            a[r], a[hi] = a[hi], a[r]
            m = _lomuto(a, lo, hi)
            left_hi, right_lo = m - 1, m + 1
        # recurse on the smaller part, loop on the larger
        if left_hi - lo < hi - right_lo:
            _improved(a, lo, left_hi, cutoff, three_way)
            lo = right_lo
        else:
            _improved(a, right_lo, hi, cutoff, three_way)
            hi = left_hi
    _insertion(a, lo, hi)
