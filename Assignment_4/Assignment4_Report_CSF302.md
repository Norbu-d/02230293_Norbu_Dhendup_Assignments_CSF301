# CSF302 Algorithm Design & Analysis (AS2026)

## Assignment 4 Report

**Name:** Norbu Dhendup
**Student No.:** 02230293
**Programme:** BE 3SWE
**Date:** 11/26/2026

---

# Assignment 4 – Hall booking

Claude (Anthropic) was used to write: `booking.py`, `test_booking.py` and the ratio experiment. Submitted code all successfully completes the brute-force validation process (Part B).

## Part A and B

`booking.py` contains the 4 functions. Data is ordered by (finish, start, index) so that results are reproducible. Functions output indices in ascending order. However, `brute_force` throws an error from 16 data items or more. `test_booking.py` has 14 tests, all of which succeed (`python -m unittest test_booking -v`). Test details are shown below.

**Table 1:** `test_booking.py` tests

| Test type | Inputs | Expected |
|---|---|---|
| `best_schedule` and `brute_force` | 600 random data sets of 0–10 items | Consistent overall revenue. Output is both valid and matches this figure |
| Edge conditions | Zero, one, fully conflicting, non-conflicting, consecutive and unordered data | All 4 functions operate correctly. Data remains unaltered. |
| Same fee per item | 600 random data sets where all have a fee of 1000 | `greedy_earliest_finish` always matches the optimal solution |
| Contrived data and upper bound | See Table 2 and 16 items | Greedy solutions underdeliver. `brute_force` also rejects 16 items. |

## Part C

### C1. Contrived data

**Table 2:** Small contrived data sets (each row is start, finish, fee)

| Guideline | Data | Greedy revenue | Optimal revenue | Ratio |
|---|---|---|---|---|
| Earliest finish | (9, 11, 1000); (10, 14, 9000) | 1000 (item 0) | 9000 (item 1) | 0.111 |
| Highest fee | (9, 17, 10000); (9, 13, 6000); (13, 17, 6000) | 10000 (item 0) | 12000 (items 1 and 2) | 0.833 |

The earliest finish guideline selects based on finishing time and ignores fees. Even though the 9–11 workshop finishes earlier, it is selected and prevents the 10–14 wedding, which is 9x more lucrative. The highest fee guideline selects based on fees and does not consider time. The 10000 item lasts for a full day and so prevents the two workshops running at the same time, which earn 12000 together. As individual workshops earn less than this, their combined revenue is never considered.

### C2. Validity of recurrence relation

Order data by finish time and label items 1 to n. Consider item j. An optimal selection for 1–j will either exclude j or include it. If excluded then it is an optimal selection for 1–(j−1). Any improved selection for 1–(j−1) could easily be applied to this case to further improve it. Thus it is OPT(j−1). If included then all selected items other than j must finish before j begins. As data is ordered by finish time these items are precisely those labelled 1 to p(j). Items p(j)+1 to (j−1) all finish after j begins and so are conflicting. The remainder of the selection must be an optimal selection for 1–p(j) as replacing this with a better selection will increase revenue without affecting j. Thus it is fee_j plus OPT(p(j)). The optimal solution is whichever of these is greater. Therefore OPT(j) is optimal. This demonstrates optimal substructure: optimal solutions for larger data can be constructed from optimal solutions for smaller data. To trace back a selection, begin from n. If fee_j plus OPT(p(j)) is greater than OPT(j−1), then select item j and transfer to p(j). Otherwise transfer to j−1.

### C3. Greedy and optimal revenues

I created 1000 data sets of 50 items each (seed 4) for a 168 hour week. Start times were random integers between 0 and 168. Durations were 1–12 hours. For model A, fee was a random integer between 1000 and 20000 and was independent of duration. Model B instead related fee to duration and had a random hourly rate of 800–1200. This was a more realistic approach. Revenue ratio was calculated as greedy revenue divided by `best_schedule` revenue. Code for this experiment is given in `experiment.py`.

**Table 3:** Revenue ratio of greedy and optimal for 1000 data sets of 50 items

| Fee model | Guideline | Avg ratio | Poorest ratio |
|---|---|---:|---:|
| A – independent of duration | Earliest finish | 0.843 | 0.600 |
| A – independent of duration | Highest fee | 0.950 | 0.766 |
| B – proportional to duration | Earliest finish | 0.711 | 0.434 |
| B – proportional to duration | Highest fee | 0.939 | 0.784 |

### C4. Complexity

**Table 4:** Complexity of functions for n items

| Function | Complexity | Explanation |
|---|---|---|
| `greedy_earliest_finish` | O(n log n) | Data is ordered. Data is then scanned once to compare with final finish time |
| `greedy_highest_fee` | O(n²) | Data is ordered (O(n log n)). Data is then compared with at most n accepted items |
| `best_schedule` | O(n log n) | Data is ordered. For each item j, binary search is used to find p(j). A table is then populated (O(n)) and traced back |
| `brute_force` | O(n · 2ⁿ) | Each of the 2ⁿ combinations of items is validated. This involves one scan (O(n)) of the ordered data |

## Part D: Critical evaluation

### Limitations of testing for validity

While `greedy_highest_fee` produced optimal overall revenue for the scenario in the assignment brief and for the first 8 (of 2–4 item) random data sets that I tested, it failed 3.1% of the time for over 2000 such data sets. Similarly, while `greedy_earliest_finish` successfully validated for 600 data sets with equal fees, it failed on the third random data set with differing fees. A faulty guideline that fails 3 in 100 data sets will pass 10 tests approximately 73% of the time. Although tests do highlight the presence of a problem, they cannot confirm that no problem exists. Thus, a sound argument such as that in C2 is needed. Testing is however valuable as it allows comparison with `brute_force`.

### Should the manager continue using the simple guideline?

No. On average, earliest finish attained 84.3% of optimal revenue. The poorest performance of 1000 random weeks resulted in 60.0%. Where fee was proportional to duration, this figure reduced to 71.1% on average and 43.4% at its poorest. Despite this, highest fee still on average underperformed by around 5%. The additional complexity of `best_schedule` is small. It is approximately 20 lines long. Moreover, for 10,000 items it ran in 0.013s compared to 0.010s for the simple guideline. The manager should therefore only continue to use the simple guideline if all bookings charge the same amount. In this case, the guideline is known to be optimal. As the data used to calculate these ratios was random, a hall with less conflicting data would achieve a greater proportion of optimal revenue.

### Benefits of earliest finish with equal fees and its limitations

When fees are equal, the main aim is to maximise the number of bookings. For any optimal selection, the first booking can be replaced by another non-conflicting booking that finishes earliest. As this latter booking does not finish later than the original, no reduction in the number of bookings occurs. Thus, selecting the earliest finish item never reduces the number of bookings and the same logic can be applied recursively. However, when fees differ, replacing a booking also alters the revenue. In my first contrived data set, for example, the earliest finishing booking (fee 1000) prevented a more lucrative booking (fee 9000). Again, early finishing allowed space to be freed up but, as revenue was now also a consideration, this line of reasoning no longer applied.
