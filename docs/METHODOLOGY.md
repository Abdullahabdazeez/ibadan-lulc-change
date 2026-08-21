# Methodology

## Final reconstruction

The final Ibadan LULC reconstruction compares 2013 and 2023 on an identical **30 m** analysis grid in **WGS 84 / UTM Zone 31N (EPSG:32631)**. The authoritative common footprint contains **3,578,423 pixels**, equivalent to **3,220.581 km²**.

Landsat-derived predictors were rebuilt for both years and included **SR_B2, SR_B3, SR_B4, SR_B5, SR_B6, SR_B7, NDVI, NDBI and MNDWI**. A Random Forest classifier was used to map four classes: Built-up, Vegetation, Water and Bare soil.

## Reconstruction and deployment repair

A later audit found that the earlier validation framework did not adequately represent deployment-domain performance. The original headline results were therefore withdrawn from use and the classification was reconstructed rather than simply republished.

Targeted human-review stages were used to diagnose difficult class boundaries and deployment errors. The final deployment review contained **48 visually reviewed samples**, divided before final evaluation into:

- **32 calibration samples** used for model-development decisions; and
- **16 locked holdout samples** reserved for independent evaluation.

The locked holdout labels were not used for model fitting, calibration weighting, feature selection, threshold selection or hyperparameter tuning. The final repaired model was frozen before the holdout labels were opened.

## Validation and scientific checks

The primary final predictive evidence is the **16-sample locked holdout**. The final repaired classifier correctly classified **14/16** samples, with Overall Accuracy **0.8750**, Balanced Accuracy **0.9259**, Macro F1 **0.6354** and Cohen's Kappa **0.7935**.

Three additional evidence types were retained separately:

1. calibration-only out-of-fold evaluation used during development;
2. wall-to-wall spectral consistency diagnostics using NDVI, NDBI and MNDWI; and
3. temporal/spatial consistency checks, including identical analysis footprints and change-pattern plausibility.

These supporting diagnostics are not combined with the locked holdout into a synthetic accuracy score.

## Change analysis

Post-classification comparison generated a complete **4 × 4 transition matrix**, stable-vs-changed mapping, built-up expansion mapping, vegetation-to-built-up conversion, class-area summaries and net-change statistics. All downstream maps and figures were generated only after the accepted 2013 and 2023 rasters were frozen as authoritative inputs.
