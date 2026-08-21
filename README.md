# Ibadan Land-Cover Change, 2013–2023


A remote-sensing and GIS assessment of how built-up land, vegetation, water and bare soil changed across the Ibadan study area between 2013 and 2023, with particular attention to the source and scale of urban expansion.


## Research question

**How did the spatial distribution of built-up land, vegetation, water and bare soil change across Ibadan between 2013 and 2023, and which land-cover class contributed most to new urban development?**

## Results at a glance

| Indicator | Final result |
|---|---:|
| Analysis area | **3,220.581 km²** |
| Built-up area, 2013 | **99.866 km² (3.101%)** |
| Built-up area, 2023 | **330.177 km² (10.252%)** |
| Net built-up increase | **230.311 km²** |
| Relative built-up increase | **230.62%** |
| Vegetation area, 2013 | **3,112.233 km² (96.636%)** |
| Vegetation area, 2023 | **2,881.903 km² (89.484%)** |
| Vegetation net change | **−230.331 km²** |
| Gross new built-up land | **248.235 km²** |
| Vegetation → Built-up | **246.104 km²** |
| Share of gross new built-up from vegetation | **99.14%** |
| Stable landscape | **91.50%** |
| Changed landscape | **8.50%** |

The dominant mapped conversion was **Vegetation → Built-up**, covering **246.104 km²**. Almost all gross new built-up land identified in the change analysis had therefore been mapped as vegetation in 2013.

## Data and predictors

The final classification used Landsat-derived surface-reflectance and spectral-index predictors: **SR_B2, SR_B3, SR_B4, SR_B5, SR_B6, SR_B7, NDVI, NDBI and MNDWI**. Both years were aligned to a common **30 m** grid in **WGS 84 / UTM Zone 31N (EPSG:32631)**.

Final classes were **Built-up, Vegetation, Water and Bare soil**.

## Final reconstruction workflow

1. Rebuilt comparable 2013 and 2023 Landsat predictor stacks.
2. Used a Random Forest classifier for four-class LULC mapping.
3. Audited the initial reconstruction for leakage, domain shift and implausible class patterns.
4. Conducted targeted blinded human review of deployment-domain samples.
5. Split the final deployment review into **32 calibration samples** and **16 locked holdout samples**.
6. Selected the deployment repair without using locked-holdout labels.
7. Froze the repaired model before opening the holdout.
8. Reclassified both years on an identical common analysis footprint.
9. Ran spectral, temporal and spatial consistency checks.
10. Froze the accepted classification before producing change products and publication documentation.

## Independent validation

The strongest final predictive evidence is the **16-sample locked holdout**, which was excluded from model fitting and calibration selection.

| Metric | Baseline A6F | Final repaired model |
|---|---:|---:|
| Correct cases | 6/16 | **14/16** |
| Overall Accuracy | 0.3750 | **0.8750** |
| Balanced Accuracy | 0.2593 | **0.9259** |
| Macro F1 | 0.2448 | **0.6354** |
| Cohen's Kappa | 0.1304 | **0.7935** |

The repair corrected **8** previously incorrect holdout cases and introduced **0 regressions**.

Because the locked holdout contains only 16 samples, the raw case count should be interpreted alongside the percentage metrics. Per-class scores with very small support should be treated cautiously.

## Final transition matrix

All values are km².

| 2013 → 2023 | Built-up | Vegetation | Water | Bare soil |
|---|---:|---:|---:|---:|
| **Built-up** | 81.9414 | 17.8236 | 0.0360 | 0.0648 |
| **Vegetation** | **246.1041** | 2861.2584 | 0.6633 | 4.2075 |
| **Water** | 0.0072 | 1.5570 | 3.4992 | 0.0000 |
| **Bare soil** | 2.1240 | 1.2636 | 0.0009 | 0.0297 |

The machine-readable version is available at [`outputs/tables/transition_matrix_sqkm.csv`](outputs/tables/transition_matrix_sqkm.csv).

## Scientific evidence hierarchy

The project keeps four evidence types separate:

1. **Independent locked-holdout validation** — final predictive evidence.
2. **Calibration-only out-of-fold evaluation** — model-development evidence.
3. **Spectral consistency diagnostics** — wall-to-wall plausibility checks.
4. **Temporal/spatial consistency checks** — common-footprint and change-pattern sanity checks.

Only the locked holdout is treated as final independent classification accuracy. The other diagnostics support scientific plausibility but are not merged into a synthetic accuracy score.

## Planning interpretation

The final reconstruction shows substantial urban expansion accompanied by a nearly equal decline in vegetation. The transition analysis indicates that expansion was overwhelmingly associated with conversion of vegetated land to built-up surfaces.

For planning, the pattern supports closer monitoring of peripheral urban growth, stronger development control, protection of strategically important green areas, and infrastructure planning that anticipates continued outward expansion. The analysis identifies where land-cover conversion occurred; it does not by itself establish the demographic, economic or regulatory causes of that conversion.

## Cartographic products

The final reconstruction produced publication-quality 2013 and 2023 LULC maps, a comparison map, a major-transition map, a built-up-expansion map and a stable-vs-changed map. Superseded pre-reconstruction PNGs previously stored in this repository have been removed so that no outdated classification is presented as final evidence.

The README now surfaces the principal final maps directly so a reviewer can understand the spatial results before reading the technical documentation. Full-resolution final raster and cartographic products remain preserved in the frozen Stage-10 scientific package.

## Repository structure

```text
.
├── data/                   # Project inputs / supporting data
├── docs/                   # Final methods, results and limitations
├── notebooks/              # Analysis / review notebooks
├── outputs/
│   ├── charts/             # Final repository-safe SVG summaries
│   ├── maps/               # Cartographic product notes
│   └── tables/             # Final numerical summaries
├── scripts/                # Analysis workflows
└── validation/             # Repository and validation records
```

## Tools

Google Earth Engine · Python · Rasterio · GeoPandas · Pandas · NumPy · scikit-learn · Matplotlib · Google Colab · Git · GitHub

## Limitations

- The final independent holdout contains 16 samples.
- Landsat's 30 m resolution can produce mixed pixels in heterogeneous urban areas.
- The four-class scheme generalises more detailed urban and environmental land-cover types.
- Spectral and temporal consistency tests do not replace independent reference data.
- Change detection quantifies mapped conversion but does not establish its socioeconomic causes.

## Documentation

- [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)
- [`docs/RESULTS.md`](docs/RESULTS.md)
- [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md)
- [`outputs/tables/key_findings.csv`](outputs/tables/key_findings.csv)
- [`outputs/tables/classification_accuracy.csv`](outputs/tables/classification_accuracy.csv)
- [`outputs/tables/lulc_area_change_summary.csv`](outputs/tables/lulc_area_change_summary.csv)
- [`outputs/tables/transition_matrix_sqkm.csv`](outputs/tables/transition_matrix_sqkm.csv)

## Author

**Abdullah Abdazeez Ayomide**  
Geo-spatial Planner | GIS & Remote Sensing Analyst | Urban & Environmental Planning Researcher

- [GitHub](https://github.com/Abdullahabdazeez)
- [LinkedIn](https://ng.linkedin.com/in/abdazeez-abdullah-4b814719a)
- [Email](mailto:abdazeezabdullah1@gmail.com)

## Citation and licence

Code is available under the MIT License. When citing results, use the **final reconstructed and frozen 2013–2023 outputs** rather than superseded statistics from the original workflow.
