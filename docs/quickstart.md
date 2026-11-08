# Quickstart

## Plan a binary metric

```python
from experimentpy import sample_size_proportions

plan = sample_size_proportions(0.05, 0.005, power=0.80)
print(plan.n_control, plan.n_variant, plan.total)
# 31234 31234 62468
```

The inputs use proportions: `0.05` is 5%, and `0.005` is an absolute
difference of 0.5 percentage points. To plan for a 10% relative lift from a
5% baseline, set `mde_absolute=0.05 * 0.10`.

For unequal allocation, `ratio` is the variant size divided by the control
size. For example, `ratio=2` assigns twice as many units to the variant:

```python
unequal = sample_size_proportions(0.10, 0.02, ratio=2)
assert unequal.n_variant == 2 * unequal.n_control
```

A negative MDE plans for a decrease:

```python
decrease = sample_size_proportions(0.10, -0.02)
```

Power is approximate. This design is for a two-sided test at a fixed horizon
with independent binary outcomes. It does not adjust for sequential peeking,
multiple comparisons or clustered assignment.

## Check sample ratio mismatch

```python
from experimentpy import check_srm

result = check_srm({"control": 5100, "variant": 4900})
print(f"{result.pvalue:.4f}", result.has_srm)
# 0.0455 False
```

Omitting `allocation` means equal allocation. To check an intended 20/80 split:

```python
result = check_srm(
    {"control": 200, "variant": 800},
    {"control": 0.2, "variant": 0.8},
)
assert result.pvalue == 1.0
```

Use counts of independently randomized units, counting each unit once.
Conversion counts and repeated visits are not assignment counts. Avoid
post-treatment filtering when constructing the input.

## Export results

Both functions return dataclasses:

```python
from dataclasses import asdict

record = asdict(plan)
record["total"] = plan.total
```

Computed properties such as `total` and `has_srm` are not included by
`asdict()`; add them explicitly when needed.
