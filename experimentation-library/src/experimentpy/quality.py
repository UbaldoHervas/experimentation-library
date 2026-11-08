"""Sample ratio mismatch checks on assignment counts."""

from collections.abc import Mapping
from dataclasses import dataclass
from math import fsum, isclose

from scipy.stats import chi2

from ._validation import count, finite_real, probability


@dataclass(frozen=True)
class SRMResult:
    """Pearson goodness-of-fit result for planned allocation proportions."""

    labels: tuple[str, ...]
    observed: tuple[int, ...]
    expected: tuple[float, ...]
    statistic: float
    pvalue: float
    degrees_of_freedom: int
    alpha: float

    @property
    def has_srm(self) -> bool:
        return self.pvalue < self.alpha


def check_srm(
    observed: Mapping[str, int],
    allocation: Mapping[str, float] | None = None,
    *,
    alpha: float = 0.001,
) -> SRMResult:
    """Check assignment counts against a prespecified allocation.

    Defaults to equal allocation. Allocation values must be positive
    proportions summing to 1; keys must match observed exactly. Supports
    two or more arms. Uses Pearson's chi-square with k-1 degrees of freedom.

    Count each independent randomized unit once, before post-treatment
    filters. A nonsignificant result does not establish experiment validity.
    Raises ValueError if any expected arm count is below 5.
    """
    alpha = probability(alpha, "alpha")
    if not isinstance(observed, Mapping) or len(observed) < 2:
        raise ValueError("observed must map at least two arm labels to counts.")
    labels = tuple(observed)
    if any(not isinstance(label, str) or not label for label in labels):
        raise ValueError("Arm labels must be nonempty strings.")
    counts = tuple(count(observed[label], label) for label in labels)
    total = sum(counts)
    if total == 0:
        raise ValueError("The total observed count must be positive.")
    if allocation is None:
        weights = (1.0 / len(labels),) * len(labels)
    else:
        if not isinstance(allocation, Mapping) or set(allocation) != set(labels):
            raise ValueError("allocation and observed must have identical arm labels.")
        weights = tuple(finite_real(allocation[label], label) for label in labels)
        if any(weight <= 0 for weight in weights):
            raise ValueError("Allocation proportions must be positive.")
        if not isclose(fsum(weights), 1.0, rel_tol=0, abs_tol=1e-12):
            raise ValueError("Allocation proportions must sum to 1.")
        # Remove harmless floating-point summation error only.
        weights = tuple(weight / fsum(weights) for weight in weights)
    expected = tuple(total * weight for weight in weights)
    if min(expected) < 5:
        raise ValueError("Chi-square approximation requires expected counts >= 5 per arm.")
    statistic = fsum((actual - target) ** 2 / target
                     for actual, target in zip(counts, expected))
    df = len(labels) - 1
    pvalue = float(chi2.sf(statistic, df))
    return SRMResult(labels, counts, expected, statistic, pvalue, df, alpha)
