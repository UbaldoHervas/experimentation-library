# API reference

## `sample_size_proportions`

```python
sample_size_proportions(
    baseline,
    mde_absolute,
    *,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
)
```

| Parameter | Meaning |
| --- | --- |
| `baseline` | Control event probability, strictly between 0 and 1. |
| `mde_absolute` | Nonzero absolute difference; `baseline + mde_absolute` must remain strictly between 0 and 1. |
| `alpha` | Two-sided significance level, strictly between 0 and 1. |
| `power` | Target approximate power, above both 0.5 and `alpha`, and below 1. |
| `ratio` | Positive planned variant/control sample-size ratio. |

Returns `SampleSizeResult`, with `n_control`, `n_variant`, `baseline`,
`variant_rate`, `mde_absolute`, `alpha`, `power` and `ratio`. The `total`
property returns the sum of the two rounded sample sizes.

Raises `ValueError` for unsupported inputs, or when the resulting design has
fewer than five expected events or non-events in either arm.

## `check_srm`

```python
check_srm(observed, allocation=None, *, alpha=0.001)
```

| Parameter | Meaning |
| --- | --- |
| `observed` | Mapping of at least two nonempty string arm labels to nonnegative integer assignment counts. |
| `allocation` | Optional mapping with the same labels and positive proportions summing to 1. Defaults to equal allocation. |
| `alpha` | SRM threshold, strictly between 0 and 1. Defaults to 0.001. |

Returns `SRMResult`, with `labels`, `observed`, `expected`, `statistic`,
`pvalue`, `degrees_of_freedom` and `alpha`. The `has_srm` property evaluates
whether `pvalue < alpha`.

Raises `ValueError` for invalid input, zero total assignment count, or an
expected count below five in any arm. A zero observed count in an arm is
supported when the expected-count requirement holds.

The observed mapping determines the order of the result tuples. Allocation
values are matched by arm label, regardless of mapping order.
