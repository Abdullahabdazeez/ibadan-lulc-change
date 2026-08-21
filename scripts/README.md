# Scripts

This repository preserves only scripts that are consistent with the final public record.

## Final reconstruction status

The authoritative 2026 reconstruction was completed through a staged Colab workflow that included predictor rebuilding, blinded human review, leakage-free calibration, locked-holdout validation, final reclassification, consistency audits and Stage-10 product freezing.

The superseded single-script Earth Engine workflow was removed from the public repository because it reproduced the withdrawn original classification and validation framework. The `gee/README.md` file records that provenance decision.

For the final scientific method, use:

- `../docs/METHODOLOGY.md`
- `../docs/RESULTS.md`
- `../outputs/tables/`

The maintained `python/reproduce_summary.py` validates and recomputes the final tabular summaries from the frozen reconstructed tables included in the repository.
