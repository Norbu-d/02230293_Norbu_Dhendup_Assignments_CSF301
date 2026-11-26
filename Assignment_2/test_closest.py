"""Tests for closest.py. Run: python -m unittest test_closest -v"""
import math
import random
import unittest

from closest import closest_pair, closest_pair_brute


def dist(points, i, j):
    return math.dist(points[i], points[j])


class TestClosest(unittest.TestCase):
    def check(self, pts):
        d, i, j = closest_pair(pts)
        db, _, _ = closest_pair_brute(pts)
        self.assertTrue(math.isclose(d, db, abs_tol=1e-9), (pts, d, db))
        self.assertLess(i, j)
        self.assertTrue(math.isclose(dist(pts, i, j), d, abs_tol=1e-9))
        return d, i, j

    def test_example_from_brief(self):
        pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        d, i, j = closest_pair(pts)
        self.assertAlmostEqual(d, math.sqrt(2))
        self.assertEqual((i, j), (0, 5))
        self.assertEqual(closest_pair_brute(pts)[1:], (0, 5))

    def test_random_vs_brute(self):              # 600 random inputs, 2-50 points
        rng = random.Random(293)
        for t in range(600):
            n = rng.randint(2, 50)
            span = rng.choice([5, 30, 1000])     # small span forces ties/duplicates
            pts = [(rng.randint(-span, span), rng.randint(-span, span)) for _ in range(n)]
            self.check(pts)

    def test_random_floats(self):
        rng = random.Random(7)
        for _ in range(100):
            pts = [(rng.uniform(-50, 50), rng.uniform(-50, 50)) for _ in range(rng.randint(2, 50))]
            self.check(pts)

    def test_larger_inputs(self):
        rng = random.Random(11)
        for n in (200, 1000, 2000):
            pts = [(rng.randint(0, 10**6), rng.randint(0, 10**6)) for _ in range(n)]
            self.check(pts)

    def test_exactly_two_points(self):
        self.assertEqual(closest_pair([(0, 0), (3, 4)]), (5.0, 0, 1))
        self.assertEqual(closest_pair([(3, 4), (0, 0)]), (5.0, 0, 1))

    def test_duplicate_points(self):
        pts = [(1, 1), (9, 9), (4, 7), (9, 9), (20, 3)]
        d, i, j = self.check(pts)
        self.assertEqual((d, i, j), (0.0, 1, 3))
        self.assertEqual(closest_pair([(5, 5), (5, 5)]), (0.0, 0, 1))

    def test_all_on_vertical_line(self):
        rng = random.Random(5)
        ys = rng.sample(range(0, 1000), 40)
        pts = [(7, y) for y in ys]
        d, i, j = self.check(pts)
        s = sorted(ys)
        self.assertEqual(d, min(b - a for a, b in zip(s, s[1:])))

    def test_all_on_horizontal_line(self):
        pts = [(x, 4) for x in random.Random(6).sample(range(0, 1000), 40)]
        self.check(pts)

    def test_closest_pair_across_dividing_line(self):
        # Sorted by x the middle split is after (49, 10); the closest pair is
        # (49, 10) and (51, 10), one in each half. Each half's own best is > 30.
        pts = [(0, 0), (10, 50), (20, 0), (49, 10), (51, 10), (80, 50), (90, 0), (100, 50)]
        d, i, j = closest_pair(pts)
        self.assertEqual((d, i, j), (2.0, 3, 4))
        self.check(pts)

    def test_shuffled_order_keeps_indices_valid(self):
        pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        random.Random(1).shuffle(pts)
        self.check(pts)

    def test_too_few_points(self):
        for f in (closest_pair, closest_pair_brute):
            with self.assertRaises(ValueError):
                f([(1, 1)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
