"""Assignment 3, Part B: tests. Run with:  python test_sorts.py  (or pytest)."""
import random
import unittest

from sorts import quicksort_basic, quicksort_improved

SORTS = {
    "basic": quicksort_basic,
    "improved": quicksort_improved,
    "improved_c1": lambda a: quicksort_improved(a, cutoff=1),
    "improved_c64": lambda a: quicksort_improved(a, cutoff=64),
    "improved_lomuto": lambda a: quicksort_improved(a, three_way=False),
}


class TestSorts(unittest.TestCase):
    def check(self, f, data):
        a = list(data)
        result = f(a)
        self.assertIsNone(result)            # sorts in place, returns nothing
        self.assertEqual(a, sorted(data))    # sorted() used only to check

    def test_random_lists(self):             # 600 random lists vs sorted()
        rng = random.Random(303)
        for name, f in SORTS.items():
            for _ in range(600):
                n = rng.randint(0, 200)
                data = [rng.randint(-1000, 1000) for _ in range(n)]
                with self.subTest(sort=name, n=n):
                    self.check(f, data)

    def test_empty(self):
        for f in SORTS.values():
            self.check(f, [])

    def test_one_element(self):
        for f in SORTS.values():
            self.check(f, [7])

    def test_all_equal(self):
        for f in SORTS.values():
            self.check(f, [5] * 100)

    def test_already_sorted(self):
        for f in SORTS.values():
            self.check(f, list(range(300)))

    def test_reverse_sorted(self):
        for f in SORTS.values():
            self.check(f, list(range(300, 0, -1)))

    def test_negative_numbers(self):
        for f in SORTS.values():
            self.check(f, [-5, -1, -100, 0, 3, -1, -7, 42, -42])
            self.check(f, list(range(-150, 0)))

    def test_many_duplicates(self):
        rng = random.Random(1)
        for f in SORTS.values():
            self.check(f, [rng.randint(0, 9) for _ in range(500)])

    def test_two_elements(self):
        for f in SORTS.values():
            self.check(f, [2, 1])
            self.check(f, [1, 2])

    def test_improved_large_adversarial_inputs(self):
        # inputs that crash quicksort_basic with RecursionError
        n = 20000
        rng = random.Random(5)
        for data in (list(range(n)), list(range(n, 0, -1)), [3] * n,
                     [rng.randint(0, 9) for _ in range(n)]):
            self.check(quicksort_improved, data)

    def test_basic_crashes_on_large_sorted(self):
        # documents the failure that Part C explains
        with self.assertRaises(RecursionError):
            quicksort_basic(list(range(5000)))


if __name__ == "__main__":
    unittest.main(verbosity=1)
