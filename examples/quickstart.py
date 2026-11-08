"""Run after installing experimentpy: python examples/quickstart.py."""

from experimentpy import check_srm, sample_size_proportions

plan = sample_size_proportions(baseline=0.05, mde_absolute=0.005)
print(f"Control: {plan.n_control:,}; variant: {plan.n_variant:,}; total: {plan.total:,}")

quality = check_srm({"control": 5100, "variant": 4900})
print(f"SRM p-value: {quality.pvalue:.4f}; detected: {quality.has_srm}")
