# Experimentation Library

Statistical tools for online experimentation.

Published on [PyPI as **experimentpy**](https://pypi.org/project/experimentpy/).
The GitHub repository is named `experimentation-library`; install and import
the current release using `experimentpy`.

**Version 0.1.0** provides two working tools: sample-size planning for binary
A/B metrics and sample ratio mismatch (SRM) checks. This library concerns
statistical experiments; it is independent of the `pytest` software-testing framework.

## Install

Python 3.10 or newer is required. SciPy is the only direct runtime dependency.

```bash
pip install experimentpy
```

To install from a local checkout instead:

```bash
python -m pip install .
```

## Sample size for a binary A/B metric

```python
from experimentpy import sample_size_proportions

plan = sample_size_proportions(
    baseline=0.05,        # 5% control conversion rate
    mde_absolute=0.005,  # +0.5 percentage points: 5% -> 5.5%
    alpha=0.05,
    power=0.80,
    ratio=1.0,           # variant units / control units
)
print(plan.n_control, plan.n_variant, plan.total)
```

An MDE of `0.005` means **0.5 percentage points**, or a **10% relative lift**
on a 5% baseline. For a relative MDE, calculate `baseline * relative_lift`
before calling the function. Negative absolute MDEs plan for decreases.

The design uses a two-sided normal approximation for two independent
proportions, pooled variance under the null and unpooled variance under the
alternative. With `p0=baseline`, `p1=p0+mde_absolute`, and
`r=n_variant/n_control`, the unrounded control sample size is:

```text
p_bar = (p0 + r*p1) / (1+r)
n_control = (
    (z_(1-alpha/2)*sqrt(p_bar*(1-p_bar)*(1+1/r))
     + z_power*sqrt(p0*(1-p0) + p1*(1-p1)/r)) / abs(p1-p0)
)**2
```

Arm sizes are rounded up. Power is approximate; there is no continuity
correction. Designs with fewer than five expected events or non-events in
either arm are rejected. This is a single-comparison, fixed-horizon design:
repeated peeking, multiple comparisons and cluster randomization require
different procedures. Users, sessions or other units must match the unit
of independent randomization.

## Sample ratio mismatch

```python
from experimentpy import check_srm

quality = check_srm(
    observed={"control": 5100, "variant": 4900},
    allocation={"control": 0.5, "variant": 0.5},
    alpha=0.001,
)
print(f"SRM p-value: {quality.pvalue:.4f}")
print(f"SRM detected: {quality.has_srm}")
```

Pearson's goodness-of-fit test compares observed counts with the prespecified
allocation, with `number_of_arms - 1` degrees of freedom. Omit `allocation`
for equal allocation. Two or more arms are supported. Allocation proportions
must be positive and sum to one, and expected counts must be at least five
per arm. Counts must be nonnegative integers, not event totals or weights.

Use each randomized unit once and avoid post-treatment filters. SRM signals
an allocation discrepancy; it does not identify its cause. Absence of SRM
does not establish overall experiment validity. The default SRM alpha is
0.001 and is separate from the outcome-analysis alpha.

Results are dataclasses and can be exported with `dataclasses.asdict(result)`.

## Scope and next steps

This release implements sample-size planning and SRM only. Outcome p-values,
effect intervals, practical significance, variance reduction and
quasi-experimental methods are planned extensions, not implemented APIs.

## Development

```bash
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -v
python -m build
python -m twine check dist/*
```

Tests use Python's standard `unittest` framework; no `pytest` dependency is
needed. See `examples/quickstart.py` for an executable example.

## References

- [SciPy Pearson chi-square documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html)
- [statsmodels two-proportion power documentation](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.power_proportions_2indep.html)

## License

MIT. Copyright (c) 2026 Ubaldo Hervas.
