# Methodology

## Analysis framework

I compared land cover across the Ibadan metropolitan study area for **2013 and 2023** using an identical **30 m** analysis grid in **WGS 84 / UTM Zone 31N (EPSG:32631)**. The common footprint contains **3,578,423 pixels**, equivalent to **3,220.581 km²**.

Four broad classes were mapped: **Built-up, Vegetation, Water and Bare soil**.

## Predictor variables

Landsat Collection 2 Surface Reflectance imagery provided the spectral basis for the analysis. The predictor stack included:

- SR_B2
- SR_B3
- SR_B4
- SR_B5
- SR_B6
- SR_B7
- NDVI
- NDBI
- MNDWI

A Random Forest classifier was used to model the relationship between these predictors and the four land-cover classes.

## Reference data and validation design

Visually interpreted reference samples supported model development and evaluation. The final reviewed reference set contained **48 samples**:

- **32 calibration samples** for model-development decisions; and
- **16 holdout samples** reserved for independent evaluation.

The holdout samples were excluded from model fitting and model-selection decisions. The accepted classifier correctly classified **14 of 16** holdout samples.

| Metric | Result |
|---|---:|
| Overall Accuracy | 0.8750 |
| Balanced Accuracy | 0.9259 |
| Macro F1 | 0.6354 |
| Cohen's Kappa | 0.7935 |

The small holdout size is an important limitation, so the raw **14/16** result is reported alongside the summary metrics.

## Change analysis

The accepted 2013 and 2023 classifications were compared pixel by pixel. The change analysis produced:

1. class-area summaries for both years;
2. net change by land-cover class;
3. a complete 4 × 4 transition matrix;
4. built-up expansion mapping;
5. vegetation-to-built-up conversion statistics; and
6. stable-versus-changed mapping.

This approach answers two different planning questions: **how much the landscape changed** and **which land-cover conversions were associated with urban expansion**.

## Interpretation

The analysis measures physical land-cover conversion visible in the imagery. It should not be interpreted as direct evidence of the demographic, economic or regulatory causes of urban expansion.