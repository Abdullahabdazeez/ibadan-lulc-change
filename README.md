# Ibadan Land-Cover Change and Urban Expansion, 2013–2023

<p align="center">
  <img src="outputs/maps/final_lulc_comparison.svg" alt="Ibadan land-cover comparison for 2013 and 2023" width="100%">
</p>

## What this project asks

How did Ibadan's land cover change over ten years, and what type of land was most often converted as the city expanded?

I used Landsat imagery to map four broad classes — **Built-up, Vegetation, Water and Bare soil** — for 2013 and 2023. The final workflow was rebuilt after an audit of the earlier classification showed that the validation evidence needed to be stronger.

The important result is straightforward: **Ibadan expanded substantially, and most of the new built-up land had been mapped as vegetation in 2013.**

## Main findings

| Indicator | Result |
|---|---:|
| Analysis area | **3,220.581 km²** |
| Built-up area, 2013 | **99.866 km² (3.101%)** |
| Built-up area, 2023 | **330.177 km² (10.252%)** |
| Net built-up increase | **230.311 km²** |
| Relative built-up increase | **230.62%** |
| Gross new built-up land | **248.235 km²** |
| Vegetation → Built-up | **246.104 km²** |
| Share of gross new built-up from vegetation | **99.14%** |
| Changed landscape | **8.50%** |

The dominant transition was **Vegetation → Built-up**, covering **246.104 km²**. That does not by itself explain *why* the conversion happened, but it clearly shows where the physical growth of the city was concentrated in the mapped landscape.

## Why I rebuilt the analysis

The first version of this project produced attractive results, but a later audit raised questions about the strength of the validation evidence. Rather than keep those results, I rebuilt the classification and validation workflow.

The final version uses seasonally matched Landsat predictors, blinded human review, leakage controls, a locked holdout and wall-to-wall consistency checks. The model was frozen before the holdout was opened.

## Independent validation

The strongest final test is a **16-sample locked holdout** that was not used for fitting or calibration selection.

| Metric | Earlier baseline | Final model |
|---|---:|---:|
| Correct cases | 6/16 | **14/16** |
| Overall Accuracy | 0.3750 | **0.8750** |
| Balanced Accuracy | 0.2593 | **0.9259** |
| Macro F1 | 0.2448 | **0.6354** |
| Cohen's Kappa | 0.1304 | **0.7935** |

The repaired model corrected **8** previously wrong holdout cases and introduced **0 regressions**.

The holdout is small, so I do not treat the percentage scores as more precise than they really are. The raw case count is just as important here.

## Data and model

The final classification uses Landsat surface-reflectance bands **SR_B2, SR_B3, SR_B4, SR_B5, SR_B6 and SR_B7**, together with **NDVI, NDBI and MNDWI**. Both years were aligned to the same **30 m** grid in **WGS 84 / UTM Zone 31N (EPSG:32631)**.

A Random Forest classifier was used for the four land-cover classes.

## How the final workflow was built

1. Rebuilt comparable 2013 and 2023 Landsat predictor stacks.
2. Reconstructed the reference data and reviewed difficult cases blindly.
3. Separated calibration samples from a locked independent holdout.
4. Selected the repair without looking at holdout labels.
5. Froze the model and then opened the holdout.
6. Reclassified both years on one common analysis footprint.
7. Checked spectral, temporal and spatial consistency.
8. Produced the final change maps and transition tables only after the classification was accepted.

## Land-cover transitions

All values below are in km².

| 2013 → 2023 | Built-up | Vegetation | Water | Bare soil |
|---|---:|---:|---:|---:|
| **Built-up** | 81.9414 | 17.8236 | 0.0360 | 0.0648 |
| **Vegetation** | **246.1041** | 2861.2584 | 0.6633 | 4.2075 |
| **Water** | 0.0072 | 1.5570 | 3.4992 | 0.0000 |
| **Bare soil** | 2.1240 | 1.2636 | 0.0009 | 0.0297 |

The machine-readable table is available at [`outputs/tables/transition_matrix_sqkm.csv`](outputs/tables/transition_matrix_sqkm.csv).

## What the result means for planning

The pattern points to rapid outward growth and a large loss of land previously mapped as vegetation. For planners, that strengthens the case for monitoring peri-urban expansion, protecting important green areas, coordinating infrastructure with new development and paying closer attention to the cumulative effect of small land conversions at the urban edge.

This project measures mapped land-cover change. It does not claim that the imagery alone can identify the demographic, economic or regulatory causes behind that change.

## Outputs and documentation

The repository contains the final comparison map, summary charts, transition tables, methods, results and limitations. The main supporting files are:

- [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)
- [`docs/RESULTS.md`](docs/RESULTS.md)
- [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md)
- [`outputs/tables/key_findings.csv`](outputs/tables/key_findings.csv)
- [`outputs/tables/classification_accuracy.csv`](outputs/tables/classification_accuracy.csv)
- [`outputs/tables/lulc_area_change_summary.csv`](outputs/tables/lulc_area_change_summary.csv)
- [`outputs/tables/transition_matrix_sqkm.csv`](outputs/tables/transition_matrix_sqkm.csv)

## Tools

Google Earth Engine · Python · Rasterio · GeoPandas · Pandas · NumPy · scikit-learn · Matplotlib · Google Colab · Git · GitHub

## Limitations

The final independent holdout contains only 16 samples. Landsat's 30 m pixels can also mix more than one surface type in dense or fragmented urban areas, and the four-class scheme simplifies a much more complex landscape.

The analysis is therefore best used for broad land-cover change and urban-growth interpretation rather than parcel-level decisions.

## Author

**Abdullah Abdazeez Ayomide**  
Geospatial Planner · GIS & Remote Sensing Analyst · Urban & Environmental Planning Researcher

[GitHub](https://github.com/Abdullahabdazeez) · [LinkedIn](https://ng.linkedin.com/in/abdazeez-abdullah-4b814719a) · [Email](mailto:abdazeezabdullah1@gmail.com)

## Citation and licence

Code is available under the MIT License. For any citation or reuse of the results, use the **final reconstructed 2013–2023 outputs** rather than statistics from the superseded workflow.
