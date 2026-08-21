# Scripts

This repository preserves selected analysis scripts from the project history.

## Final reconstruction status

The authoritative 2026 reconstruction was completed through a staged Colab workflow that included predictor rebuilding, blinded human review, leakage-free calibration, locked-holdout validation, final reclassification, consistency audits and Stage-10 product freezing.

The older Earth Engine script under `gee/` belongs to the **superseded original workflow** and is retained only as provenance. It should not be used to reproduce or cite the final headline statistics.

For the final scientific method, use:

- `../docs/METHODOLOGY.md`
- `../docs/RESULTS.md`
- `../outputs/tables/`

The maintained `python/reproduce_summary.py` validates and recomputes the final tabular summaries from the frozen reconstructed tables included in the repository.
