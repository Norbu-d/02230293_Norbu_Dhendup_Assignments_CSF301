# CSF302 – Algorithm Design & Analysis (AS2026)

## Assignment 3 Report

**By:** Norbu Dhendup  
**Student no:** 02230293  
**Programme:** BE 3SWE  
**Date:** 10/10/2026

---

## Fixing a Slow Quicksort

I used Claude (Anthropic, 2026) to produce the code files and initial report. Both sorting algorithms were verified using the `sorted()` function and 600 sets of random data, together with the 6 necessary extreme data sets (total 11 – all successful). All the timings below are from the benchmark script which was executed using Python 3.12.3.

## Method

All timings are for the fastest of 3 tries. Python’s default recursion limit of 1,000 was not changed and so a `RecursionError` caused by exceeding this is deemed to be a crash. The improved quicksort selects a random pivot and performs insertion sort on sub-arrays of length 16 and under. It recurses on just the smaller sub-array. Furthermore, it 3-way partitions (values less than, equal to and greater than the pivot). Without this, even using a random pivot with Lomuto partitioning resulted in 1.15s for 16,000 values in the range [0,9]. With 3-way partitioning, this reduced to 0.006s as groups of identical values still result in quadratic behaviour.

## Results

**Table 1**  
*Running Time in Milliseconds by Input Type and Size*

| n | Random: Basic | Random: Improved | Already sorted: Basic | Already sorted: Improved | Many duplicates: Basic | Many duplicates: Improved |
|---:|---:|---:|---:|---:|---:|---:|
| 1,000 | 0.67 | 1.06 | Crash | 0.91 | 3.47 | 0.23 |
| 2,000 | 1.47 | 2.10 | Crash | 2.13 | 13.2 | 0.53 |
| 4,000 | 3.34 | 5.24 | Crash | 4.57 | 54.2 | 0.99 |
| 8,000 | 7.30 | 11.1 | Crash | 10.7 | 216 | 1.86 |
| 16,000 | 16.8 | 24.0 | Crash | 21.7 | Crash | 3.49 |
| 32,000 | 37.8 | 56.6 | Crash | 60.7 | Crash | 7.34 |
| 64,000 | 75.3 | 120 | Crash | 107 | Crash | 14.7 |

*Note.* Crash = `RecursionError`. Basic quicksort crashed on every sorted input and on duplicates from n = 16,000.

**Figure 1**  
*Time vs n (Log-Log plot)*

![Figure 1: running time of the basic, improved and built-in sort against n on random, already sorted and many-duplicates data (log-log)](images/a3_figure1.png)

*Note:* The red line ends at the point at which the basic sort crashed. The built-in `sorted()` function is also shown for comparison.

With random data, both algorithms have time complexity O(n log n) – approximately doubling in time with each doubling of n. However, the basic sort is quicker (75ms vs 120ms for n = 64,000) as the improved sort has additional processing for each data item. For authentic data, the improved sort is quicker. It sorted 64,000 ordered values in 107ms and 64,000 identical values in 14.7ms – whereas the basic sort crashed.

## Why is the Basic Quicksort Slow?

As the final value is always the largest for ordered data, Lomuto partitioning produces one sub-array of length n-1 and one of 0. This costs Θ(n) comparisons. And so T(n) = T(n-1) + Θ(n) = Θ(n) + Θ(n-1) + ... + Θ(1) = Θ(n²). Checking how many comparisons were made for ordered data verifies this. For n = 100, 200, 400 and 800, this was precisely n(n-1)/2 (i.e. 4950, 19900, 79800 and 319600 respectively). Again, this shows that processing effort increases by a factor of 4 with each doubling of n. The recursion depth is also n. Python can only recurse 1,000 times and so at n = 1,000 this was reached. Identical values also exhibit similar behaviour. As <= sends all instances of the pivot to the left, a group of k identical values will result in recursion depth of k. As with ordered data, timings generally increased by around 4x with each doubling of n (from 1,000 to 8,000: 3.5, 13.2, 54.2 and 216 ms). However, for n = 16,000 (with around 1,600 instances of each value), the basic sort again crashed (Hoare, 1962).

## Selecting a Cutoff

**Table 2**  
*Time to Sort 100,000 Random Values according to Cutoff*

| Cutoff | Best of 12 (s) | Median of 12 (s) |
|---:|---:|---:|
| 1 | 0.230 | 0.249 |
| 4 | 0.209 | 0.244 |
| 8 | 0.186 | 0.214 |
| 16 | 0.182 | 0.197 |
| 32 | 0.188 | 0.212 |
| 64 | 0.202 | 0.220 |

*Note:* Improved quicksort. 12 attempts were made for each cutoff.

Both the best and median times were quickest for a cutoff of 16. 32 was also close (within 3%). I therefore selected 16. The graph is in the shape of a ‘W’. Under a cutoff of 8, there is excessive fine-grained partitioning. Above 32, the quadratic cost of insertion sort increases.

## Comparison with sorted()

`sorted()` processed 100,000 random values in 0.019s. My most efficient algorithm (with cutoff 16) took 0.182s – so was approximately 9.7x slower. For ordered data with n = 64,000, this was even more marked – around 630x (0.17ms vs 107ms). Python’s `sorted()` function uses Timsort which exploits pre-existing ordered sections of data (Python Software Foundation, n.d.).

## Critical Reflection

### What was it about the ordered data that led to the basic quicksort crashing?

As previously mentioned, the basic sort always takes the final value as the pivot. Consequently, for ordered data, each partitioning produces sub-arrays of size n-1 and 0. This incurs Θ(n²) processing effort. I accurately recorded that the number of comparisons was n(n-1)/2. Furthermore, the recursion depth reached n and so exceeded the 1,000 frame recursion limit for Python. Analysis of average case behaviour is based on the premise that all data orders are equally probable. Thus, pivots are randomly positioned and partitions are on average evenly sized. However, the bank data was almost ordered and featured many duplicates. As there were 10 different values, all instances of the pivot were directed to one side. Recursion depth was therefore affected by the number of duplicates and at n = 16,000, the basic sort crashed.

### Why is it beneficial to use insertion sort for smaller sub-arrays?

Although insertion sort has time complexity Θ(n²), this is not problematic for small sub-arrays. For a sub-array of size k, it typically performs around k²/4 low-cost operations. Crucially, it does not require function calls. In contrast, even for sub-arrays of 2 or 3 values, quicksort requires a function call, random pivot selection and a loop to perform the partitioning. Premature termination of recursion minimises function calls. My results highlight this balance. Using cutoff 1 resulted in a time of 0.230s. Cutoff 16 (the chosen value) was quicker (0.182s – 21% better). However, for cutoff 64, the k² term dominates and so the time increased to 0.202s.

### Why is sorted() still quicker?

On random data, it was roughly 10x faster. Moreover, analysing the number of comparisons further explains why. My algorithm undertook 2.96 million and Timsort 1.53 million. Therefore, the algorithm accounts for around a 2x difference. This is because my 3-way partitioning typically compares each data item twice. The remaining 5x difference stems from the programming language. As `sorted()` is implemented in C, it can directly compare integer values. My code however interprets bytecode for each comparison and swap. For ordered data, the algorithm is especially influential. Timsort made 99,999 comparisons compared to my algorithm’s 2.99 million.

## References

Anthropic. (2026). *Claude Sonnet 5.5* [Large language model]. https://claude.ai

Hoare, C. A. R. (1962). Quicksort. *The Computer Journal, 5*(1), 10–16. https://doi.org/10.1093/comjnl/5.1.10

Python Software Foundation. (n.d.). *Sorting techniques*. Python documentation. https://docs.python.org/3/howto/sorting.html
