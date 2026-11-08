"""Shared input validation."""

from math import isfinite
from numbers import Integral, Real


def finite_real(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite real number.")
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"{name} must be a finite real number.")
    return result


def probability(value: Real, name: str) -> float:
    result = finite_real(value, name)
    if not 0 < result < 1:
        raise ValueError(f"{name} must be strictly between 0 and 1.")
    return result


def count(value: Integral, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer count.")
    return int(value)
