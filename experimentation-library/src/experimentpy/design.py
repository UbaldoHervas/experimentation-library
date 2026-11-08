"""Fixed-horizon planning for two independent binary outcomes."""

from dataclasses import dataclass
from math import ceil, isfinite, sqrt

from scipy.stats import norm

from ._validation import finite_real, probability


@dataclass(frozen=True)
class SampleSizeResult:
    """Required independent experimental units, rounded up by arm."""

    n_control: int
    n_variant: int
    baseline: float
    variant_rate: float
    mde_absolute: float
    alpha: float
    power: float
    ratio: float

    @property
    def total(self) -> int:
        return self.n_control + self.n_variant


def sample_size_proportions(
    baseline: float,
    mde_absolute: float,
    *,
    alpha: float = 0.05,
    power: float = 0.80,
    ratio: float = 1.0,
) -> SampleSizeResult:
    """Plan a two-sided, fixed-horizon, two-proportion z-test.

    ``baseline`` and ``mde_absolute`` use proportions, not percentages:
    baseline=0.05 and mde_absolute=0.005 plan for 5% versus 5.5%.
    A negative MDE plans for a decrease. ``ratio`` is n_variant/n_control.

    Uses a normal approximation with pooled null variance and unpooled
    alternative variance, without continuity correction. Power is approximate.
    Assumes independent Bernoulli units and a single planned comparison.
    """
    baseline = probability(baseline, "baseline")
    alpha = probability(alpha, "alpha")
    power = probability(power, "power")
    if power <= max(0.5, alpha):
        raise ValueError("power must exceed both 0.5 and alpha.")
    mde_absolute = finite_real(mde_absolute, "mde_absolute")
    if mde_absolute == 0:
        raise ValueError("mde_absolute must be nonzero.")
    variant = probability(baseline + mde_absolute, "baseline + mde_absolute")
    ratio = finite_real(ratio, "ratio")
    if ratio <= 0:
        raise ValueError("ratio must be positive.")

    # Weighted event rate across the two planned allocation sizes.
    weight = ratio / (1.0 + ratio)
    pooled = baseline * (1.0 - weight) + variant * weight
    variance_null = pooled * (1.0 - pooled) * (1.0 + 1.0 / ratio)
    variance_alternative = (
        baseline * (1.0 - baseline) + variant * (1.0 - variant) / ratio
    )
    # isf avoids loss of precision from computing 1 - alpha/2.
    critical = norm.isf(alpha / 2.0)
    z_power = norm.ppf(power)
    required = ((critical * sqrt(variance_null)
                 + z_power * sqrt(variance_alternative)) / abs(mde_absolute)) ** 2
    if not isfinite(required) or required <= 0:
        raise ValueError("Inputs exceed the supported numerical range.")
    n_control = max(1, ceil(required))
    n_variant = max(1, ceil(ratio * n_control))
    # Explicitly reject sparse designs instead of silently promising accuracy.
    if min(n_control * baseline, n_control * (1 - baseline),
           n_variant * variant, n_variant * (1 - variant)) < 5:
        raise ValueError(
            "The normal approximation requires at least 5 expected events "
            "and non-events per arm; use an exact or simulation-based design."
        )
    return SampleSizeResult(
        n_control, n_variant, baseline, variant, mde_absolute, alpha, power, ratio
    )
