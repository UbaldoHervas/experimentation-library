# ExperimentPy documentation

ExperimentPy provides statistical tools for planning and checking online
experiments. Install it with `pip install experimentpy`.

| Guide | What it covers |
| --- | --- |
| [Quickstart](quickstart.md) | Plan a binary A/B test, check SRM and export results. |
| [API reference](api.md) | Parameters, return values and input validation. |
| [Statistical methods](methodology.md) | Sample-size formula, SRM test and assumptions. |

Source: [UbaldoHervas/experimentation-library](https://github.com/UbaldoHervas/experimentation-library).

PyPI: [experimentpy](https://pypi.org/project/experimentpy/).

## Rebuild the figures

From the repository root:

```bash
python -m pip install -e ".[docs]"
python tools/build_readme_assets.py
```

The sample-size plot uses the real `sample_size_proportions()` function.
The banner's A/B allocation is an illustrative design schematic.
