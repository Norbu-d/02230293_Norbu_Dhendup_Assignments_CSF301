# CSF302 – Algorithm Design & Analysis (AS2026)

## Assignment 2 Report

**By:** Norbu Dhendup  
**Student No:** 02230293  
**Programme:** BE 3SWE  
**Date:** 10/10/2026

---

## Closest camera traps

Claude (Anthropic, 2026) was used to write code for `closest.py`, `test_closest.py` and the benchmark script. It was also used to produce an initial draft of this report. `closest_pair` was validated against `closest_pair_brute` for 600 sets of randomly-generated 2-50 traps and for the 11 necessary extreme values, all of which were successful. All the times outlined were obtained from the benchmark script and are for Python 3.12.3.

## Method

`closest_pair` uses divide and conquer. Firstly, data is ordered by x value. This is then divided and each section is solved recursively. Subsequently, a ‘strip’ of width 2δ is analysed either side of the division line, where δ is the smaller of the two recursive results. Within this strip, data is ordered by y value – again without further sorting as this is derived from the ordered y values of the recursive sections. Each trap in the strip is then only compared to higher traps within the strip that are within a y distance of δ (a fixed value). Again, this is a fixed number of comparisons. Combining the two recursive sections provides the ordered y values. For n ≤ 3, brute force is used. Distances are calculated using squared values and the square root is only applied at the end. Best of 3 timings were recorded for random integer traps in the [0, 10⁶]² area. As brute force times for n = 8000 and 16000 were obtained, n = 32000 was not assessed as 4x15.3s ≈ 61s was expected and this would exceed the 60 second time limit.

## Recurrence and Master Method

As n is halved in each recursive call, for n > 3, T(n) = 2T(n/2) + Θ(n). For n ≤ 3, T(n) = Θ(1). Therefore, a = 2, b = 2 and f(n) = Θ(n). This is equivalent to n (since n log b n = n log₂n = n). Using case 2 of the Master Method (Cormen et al, 2022), T(n) = Θ(n log n). As the initial x-sort is also Θ(n log n), overall this is Θ(n log n) compared to Θ(n²) for brute force.

## Results

**Table 1**  
*Number of Traps and Running Times*

| n | Brute force (ms) | Divide and conquer (ms) | Brute/ D&C |
|---:|---:|---:|---:|
| 1,000 | 52.7 | 2.47 | 21x |
| 2,000 | 211.6 | 5.30 | 40x |
| 4,000 | 859.5 | 11.85 | 73x |
| 8,000 | 3,948.8 | 25.22 | 157x |
| 16,000 | 15,277.8 | 53.61 | 285x |
| 32,000 | - | 141.02 | - |
| 64,000 | - | 312.39 | - |

*Note:* Best of 3 runs (except for brute force for n = 8000 and 16000 which were one run only). '-' indicates that the run was not performed as the predicted time exceeded 60 seconds. D&C = divide and conquer.

**Figure 1**  
*Brute force and divide and conquer running times*

![Figure 1: (a) log-log running times of brute force and divide and conquer for n = 1,000 to 64,000; (b) crossover for n = 16 to 60](images/a2_figure1.png)

*Note:* (a) Brute force could not be run for n = 16000 due to the 60 second time limit. Dashed and dotted lines represent the n log n and n² functions normalised to the first data point. (b) Mean for 40 sets of random data for each n. Best of 15 runs.

Where n was doubled, brute force increased by approximately 4 times (values of 4.0, 4.1, 4.6 and 3.9) – consistent with its Θ(n²) complexity. At n = 16000 brute force took 15.3 seconds. Divide and conquer, which doubles in running time by between 2.1 and 2.6 when n is doubled, processed 64000 traps in 0.31 seconds. The log-log line of best fit for brute force had a gradient of 2.06 and for divide and conquer 1.16 (Figure 1a). This is close to the expected 1.1 gradient for n log n within this n-range.

## What is better for small n?

Although divide and conquer initially equals brute force at n = 42, from n = 45 it is quicker (Figure 1b). Thus, for this machine the approximate point at which divide and conquer becomes superior is n = 45. Previously it had been found to be 43.

## Critical reflection

### How well did my results correspond to my recurrence?

Generally well. As T(n) = 2T(n/2) + Θ(n), I would expect a doubling factor of just over 2. My results showed a factor of 2.1-2.6. Furthermore, time/n log 2 n remained relatively stable at ~0.24µs for n = 1000-16000. It then increased to 0.29 and 0.31 µs for n = 32000 and 64000 respectively. Although I made no attempt to investigate this, given that the recurrence relates to processing steps and not to memory, it is probable that cache misses were responsible. Brute force was very consistent with its Θ(n²) complexity (gradient 2.06).

### Why is brute force quicker for small n?

As mentioned, Θ only applies for large n. Brute force has minimal additional processing – simply two loops and one comparison per trap-pair. Divide and conquer however requires sorting, sectioning and combining of data. Furthermore, there is a function call for each sub-section. For n = 30, brute force was 21.4 µs and divide and conquer 28.8 µs. Until n was approximately 45, therefore, the constant multiple in the n log n complexity dominated over the n² complexity. Even at n = 1000, divide and conquer was 21x quicker.

### Which extreme situation was most challenging to process, and how did I assess this?

When the closest pair is on different sides of the division line. Even if there is an issue with the strip analysis, each half will still provide a plausibly correct result. Thus, there is no program failure. In order to ensure that my assessment adequately addresses this situation, I bypassed the strip analysis and re-ran the test suite. Four tests then failed – those for cross-side pairs, for random integer and float data and for larger numbers of traps. Other tests were successful. Consequently, both deliberately created and random test data are necessary to identify this problem. In addition, a vertical division line was also of concern as all traps would fall into the strip. Only early termination based on y-distance ensures that the strip analysis remains quick.

## References

Anthropic. (2026). *Claude Sonnet 5.5* [Large language model]. https://claude.ai

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
