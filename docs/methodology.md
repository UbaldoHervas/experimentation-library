# Statistical methods

## Sample size for two proportions

The design uses a normal approximation with pooled variance under the null
and unpooled variance under the alternative, without a continuity correction.
The target power is approximate, not an exact finite-sample guarantee.

Let `p0` be the baseline rate, `p1 = p0 + mde_absolute`, and
`r = n_variant / n_control`. The unrounded control sample size is:

```text
p_bar = (p0 + r*p1) / (1+r)
n_control = (
    (z_(1-alpha/2)*sqrt(p_bar*(1-p_bar)*(1+1/r))
     + z_power*sqrt(p0*(1-p0) + p1*(1-p1)/r)) / abs(p1-p0)
)**2
```

The control size is rounded up first, and the variant size is rounded up
from `ratio * n_control`. The implementation rejects designs with fewer
than five expected events or non-events in either arm.

Assumptions: independent Bernoulli experimental units, a fixed analysis
horizon and one planned comparison. Repeated outcome peeking, clustered
assignment and multiple comparisons need different or additional procedures.
The MDE is a design input; it is not a measurement of an observed effect.

## Sample ratio mismatch

Pearson's chi-square goodness-of-fit test compares assignment counts with
prespecified allocation proportions. For `k` arms, the test uses `k - 1`
degrees of freedom. Every expected arm count must be at least five.

```text
expected_i = total_assigned * allocation_i
chi_square = sum((observed_i - expected_i)**2 / expected_i)
```

The p-value is the upper-tail probability under that chi-square distribution.
The default SRM alpha is 0.001, independently of outcome-analysis alpha.

The inputs should count each independent randomized unit once. SRM identifies
an allocation discrepancy; it does not identify its cause. A nonsignificant
result does not establish overall experiment validity.

## References

- [SciPy Pearson chi-square test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html)
- [statsmodels two-proportion power](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.power_proportions_2indep.html)
