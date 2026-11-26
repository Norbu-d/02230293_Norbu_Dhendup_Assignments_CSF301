"""Tests for booking.py. Run with:  python -m unittest test_booking -v"""
import random
import unittest

from booking import (best_schedule, brute_force, greedy_earliest_finish,
                     greedy_highest_fee)

ALL = (greedy_earliest_finish, greedy_highest_fee, best_schedule, brute_force)


def random_requests(rng, n, max_time=30, max_len=8, max_fee=100):
    out = []
    for _ in range(n):
        s = rng.randint(0, max_time)
        out.append((s, s + rng.randint(1, max_len), rng.randint(1, max_fee)))
    return out


def is_valid(requests, chosen):
    """Chosen indices are unique and no two chosen requests overlap."""
    if len(set(chosen)) != len(chosen):
        return False
    iv = sorted((requests[i][0], requests[i][1]) for i in chosen)
    return all(iv[k][1] <= iv[k + 1][0] for k in range(len(iv) - 1))


def fee_of(requests, chosen):
    return sum(requests[i][2] for i in chosen)


class TestBrief(unittest.TestCase):
    def test_example_from_brief(self):
        r = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000),
             (12, 14, 2500), (16, 18, 2000)]
        self.assertEqual(greedy_earliest_finish(r), (7500, [0, 3, 4]))
        self.assertEqual(best_schedule(r), (10000, [1, 4]))
        self.assertEqual(brute_force(r)[0], 10000)


class TestEdgeCases(unittest.TestCase):
    def test_no_requests(self):
        for f in ALL:
            self.assertEqual(f([]), (0, []))

    def test_one_request(self):
        for f in ALL:
            self.assertEqual(f([(9, 12, 3000)]), (3000, [0]))

    def test_all_overlapping(self):
        r = [(0, 10, 5), (1, 9, 7), (2, 8, 6), (3, 11, 4)]
        for f in (best_schedule, brute_force):
            self.assertEqual(f(r), (7, [1]))
        for f in ALL:
            total, chosen = f(r)
            self.assertEqual(len(chosen), 1)
            self.assertTrue(is_valid(r, chosen))

    def test_none_overlapping(self):
        r = [(0, 1, 5), (2, 3, 7), (4, 5, 6), (6, 7, 4)]
        for f in ALL:
            self.assertEqual(f(r), (22, [0, 1, 2, 3]))

    def test_back_to_back(self):
        r = [(9, 12, 100), (12, 14, 100), (14, 16, 100)]
        for f in ALL:
            self.assertEqual(f(r), (300, [0, 1, 2]))

    def test_input_not_in_time_order(self):
        r = [(14, 16, 3), (9, 12, 1), (12, 14, 2)]
        for f in ALL:
            self.assertEqual(f(r), (6, [0, 1, 2]))

    def test_input_not_modified(self):
        r = [(5, 6, 1), (0, 2, 4), (1, 3, 9)]
        copy = list(r)
        for f in ALL:
            f(r)
        self.assertEqual(r, copy)


class TestAgainstBruteForce(unittest.TestCase):
    def test_dp_matches_brute_force_600_random_inputs(self):
        rng = random.Random(303)
        for _ in range(600):
            r = random_requests(rng, rng.randint(0, 10))
            total, chosen = best_schedule(r)
            self.assertEqual(total, brute_force(r)[0], r)
            self.assertTrue(is_valid(r, chosen), r)
            self.assertEqual(fee_of(r, chosen), total, r)

    def test_greedy_results_are_valid_schedules(self):
        rng = random.Random(7)
        for _ in range(600):
            r = random_requests(rng, rng.randint(0, 10))
            for f in (greedy_earliest_finish, greedy_highest_fee):
                total, chosen = f(r)
                self.assertTrue(is_valid(r, chosen), r)
                self.assertEqual(fee_of(r, chosen), total, r)
                self.assertLessEqual(total, brute_force(r)[0], r)

    def test_equal_fees_earliest_finish_is_optimal(self):
        rng = random.Random(11)
        for _ in range(600):
            r = [(s, f, 1000) for s, f, _ in
                 random_requests(rng, rng.randint(0, 10))]
            self.assertEqual(greedy_earliest_finish(r)[0],
                             brute_force(r)[0], r)


class TestCounterexamples(unittest.TestCase):
    def test_earliest_finish_can_lose(self):
        r = [(9, 11, 1000), (10, 14, 9000)]
        self.assertEqual(greedy_earliest_finish(r)[0], 1000)
        self.assertEqual(best_schedule(r)[0], 9000)

    def test_highest_fee_can_lose(self):
        r = [(9, 17, 10000), (9, 13, 6000), (13, 17, 6000)]
        self.assertEqual(greedy_highest_fee(r)[0], 10000)
        self.assertEqual(best_schedule(r)[0], 12000)

    def test_brute_force_size_limit(self):
        with self.assertRaises(ValueError):
            brute_force([(0, 1, 1)] * 16)


if __name__ == "__main__":
    unittest.main()
