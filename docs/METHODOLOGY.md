# Methodology

## Analysis framework

I compared land cover in Ibadan for 2013 and 2023 on an identical **30 m** analysis grid in **WGS 84 / UTM Zone 31N (EPSG:32631)**. The common study footprint contains **3,578,423 pixels**, equivalent to **3,220.581 km²**.

Landsat surface-reflectance imagery provided the spectral basis for the analysis. I used **SR_B2, SR_B3, SR_B4, SR_B5, SR_B6 and SR_B7** together with **NDVI, NDBI and MNDWI** to improve separation of the four mapped classes: Built-up, Vegetation, Water and Bare soil. A Random Forest classifier was used because it performs well with multi-band remote-sensing data and can model non-linear relationships between spectral predictors and land-cover classes.

## Reference data and model development

I used visually interpreted reference samples to support model development and independent evaluation, with particular attention to locations where Built-up, Vegetation and Bare soil were difficult to distinguish spectrally. The final reference design contained **48 reviewed samples** divided before final evaluation into:

- **32 calibration samples** used for model-development decisions; and
- **16 locked holdout samples** reserved exclusively for independent evaluation.

The locked holdout labels were excluded from model fitting, calibration weighting, feature selection, threshold selection and hyperparameter tuning. This separation provided an independent test of how well the final classifier generalised beyond the samples used during model development.

## Validation and consistency checks

The primary independent validation evidence comes from the **16-sample locked holdout**. The classifier correctly classified **14 of 16 samples**, producing Overall Accuracy of **0.8750**, Balanced Accuracy of **0.9259**, Macro F1 of **0.6354** and Cohen's Kappa of **0.7935**.

I also used three supporting checks to assess the consistency of the mapped outputs:

1. calibration-only out-of-fold evaluation during model development;
2. wall-to-wall spectral checks using NDVI, NDBI and MNDWI; and
3. temporal and spatial consistency checks, including identical analysis footprints and review of mapped change patterns.

These diagnostics are reported separately from the independent holdout metrics so that model-development evidence is not presented as additional independent accuracy.

## Change analysis

I compared the accepted 2013 and 2023 classifications pixel by pixel to quantify both persistence and transition. The analysis produced a complete **4 × 4 transition matrix**, stable-versus-changed mapping, built-up expansion mapping, vegetation-to-built-up conversion, class-area summaries and net-change statistics.

This approach makes it possible to move beyond asking how much each land-cover class changed and examine **where change occurred and which land-cover transitions contributed most to Ibadan's expansion**.
