"""Reference checks, invalid inputs, and independent Monte Carlo checks."""

import math
import unittest

import numpy as np
from scipy.stats import chisquare, norm

from experimentpy import __version__, check_srm, sample_size_proportions


class SampleSizeTests(unittest.TestCase):
    def test_balanced_reference_design(self):
        # Standard 5% -> 6% normal-approximation design: ~8150 per arm.
        result = sample_size_proportions(0.05, 0.01)
        self.assertTrue(8140 <= result.n_control <= 8160)
        self.assertEqual(result.n_control, result.n_variant)
        self.assertEqual(result.total, result.n_control * 2)

    def test_mde_and_power_behaviour(self):
        base = sample_size_proportions(0.05, 0.005)
        self.assertGreater(base.total, sample_size_proportions(0.05, 0.01).total)
        self.assertGreater(sample_size_proportions(0.05, 0.005, power=0.9).total, base.total)
        self.assertGreater(sample_size_proportions(0.05, 0.005, alpha=0.01).total, base.total)

    def test_unequal_allocation(self):
        result = sample_size_proportions(0.10, 0.02, ratio=2)
        self.assertEqual(result.n_variant, 2 * result.n_control)

    def test_decrease_and_swapped_arms(self):
        increase = sample_size_proportions(0.05, 0.01)
        decrease = sample_size_proportions(0.06, -0.01)
        self.assertEqual(increase.total, decrease.total)
        self.assertLess(decrease.variant_rate, decrease.baseline)

    def test_invalid_inputs(self):
        cases = [
            dict(baseline=0), dict(baseline=1), dict(baseline=True),
            dict(baseline=float('nan')), dict(mde_absolute=0),
            dict(mde_absolute=1), dict(mde_absolute=-0.1),
            dict(mde_absolute='0.01'), dict(alpha=0), dict(alpha=float('inf')),
            dict(power=1), dict(power=0.01), dict(power=0.5), dict(ratio=0), dict(ratio=-1),
        ]
        for case in cases:
            args = dict(baseline=0.05, mde_absolute=0.005)
            args.update(case)
            with self.subTest(case=case), self.assertRaises(ValueError):
                sample_size_proportions(**args)

    def test_sparse_design_rejected(self):
        with self.assertRaises(ValueError):
            sample_size_proportions(0.000001, 0.1)

    def test_power_with_independent_binomial_simulation(self):
        # Independent generator and rejection rule check the complete design.
        rng = np.random.default_rng(20261107)
        for p0, delta, ratio in [(0.05, 0.01, 1), (0.1, 0.02, 2), (0.1, -0.02, 0.5)]:
            with self.subTest(p0=p0, delta=delta, ratio=ratio):
                plan = sample_size_proportions(p0, delta, ratio=ratio)
                x0 = rng.binomial(plan.n_control, p0, size=30000)
                x1 = rng.binomial(plan.n_variant, p0 + delta, size=30000)
                pooled = (x0 + x1) / plan.total
                se = np.sqrt(pooled * (1 - pooled) *
                             (1 / plan.n_control + 1 / plan.n_variant))
                z = (x1 / plan.n_variant - x0 / plan.n_control) / se
                empirical = np.mean(np.abs(z) > norm.isf(0.025))
                self.assertLess(abs(empirical - 0.80), 0.02)


class SRMTests(unittest.TestCase):
    def test_balanced_allocation(self):
        result = check_srm({'control': 5000, 'variant': 5000})
        self.assertEqual(result.statistic, 0)
        self.assertEqual(result.pvalue, 1)
        self.assertFalse(result.has_srm)

    def test_hand_calculated_reference(self):
        result = check_srm({'control': 600, 'variant': 400})
        self.assertAlmostEqual(result.statistic, 40)
        self.assertAlmostEqual(result.pvalue, math.erfc(math.sqrt(20)), places=20)
        self.assertTrue(result.has_srm)

    def test_unequal_allocation_and_mapping_order(self):
        result = check_srm({'a': 200, 'b': 800}, {'b': 0.8, 'a': 0.2})
        self.assertEqual(result.expected, (200., 800.))
        self.assertEqual(result.pvalue, 1)

    def test_multiple_arms_against_scipy(self):
        result = check_srm({'a': 110, 'b': 190, 'c': 300},
                           {'a': 1/6, 'b': 1/3, 'c': 1/2})
        reference = chisquare([110, 190, 300], [100, 200, 300])
        self.assertEqual(result.degrees_of_freedom, 2)
        self.assertAlmostEqual(result.statistic, reference.statistic)
        self.assertAlmostEqual(result.pvalue, reference.pvalue)

    def test_zero_observed_arm_is_supported(self):
        self.assertTrue(check_srm({'a': 0, 'b': 100}).has_srm)

    def test_numpy_integer_counts(self):
        self.assertEqual(check_srm({'a': np.int64(50), 'b': np.int64(50)}).pvalue, 1)

    def test_invalid_counts(self):
        cases = [{}, {'a': 10}, {'a': 0, 'b': 0}, {'a': 1, 'b': 1},
                 {'a': -1, 'b': 100}, {'a': 1.5, 'b': 100},
                 {'a': True, 'b': 100}, {'a': float('nan'), 'b': 100},
                 {'': 100, 'b': 100}]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                check_srm(case)

    def test_invalid_allocations(self):
        cases = [{'a': 50, 'b': 50}, {'a': 0, 'b': 1},
                 {'a': -0.1, 'b': 1.1}, {'a': 0.5, 'c': 0.5},
                 {'a': float('nan'), 'b': 0.5}]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                check_srm({'a': 100, 'b': 100}, case)


class PackageTests(unittest.TestCase):
    def test_version(self):
        self.assertEqual(__version__, '0.1.1')


if __name__ == '__main__':
    unittest.main()
