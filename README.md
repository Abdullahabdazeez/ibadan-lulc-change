<p align="center">
  <img src="assets/project-cover.png" alt="Ibadan land-cover change project" width="100%">
</p>

# Ibadan Land-Cover Change, 2013–2023

A remote-sensing and GIS assessment of how built-up land, vegetation, water and bare soil changed across the Ibadan study area between 2013 and 2023, with particular attention to the source and scale of urban expansion.

> **Project status: final reconstruction accepted and frozen.**
>
> The original workflow was subjected to a later scientific audit after its validation evidence proved insufficient for the headline claims. Those earlier results were withdrawn from use, the classification was rebuilt, deployment errors were repaired through blinded human review, and the final products were frozen only after independent holdout validation and wall-to-wall consistency checks.

## Research question

**How did the spatial distribution of built-up land, vegetation, water and bare soil change across Ibadan between 2013 and 2023, and which land-cover class contributed most to new urban development?**

## Key findings

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

The dominant mapped conversion was **Vegetation → Built-up**, covering about **246.104 km²**. This means almost all gross new built-up land identified in the change analysis had been mapped as vegetation in 2013.

## Data and predictors

The final classification used Landsat-derived surface-reflectance and spectral-index predictors:

- SR_B2
- SR_B3
- SR_B4
- SR_B5
- SR_B6
- SR_B7
- NDVI
- NDBI
- MNDWI

Both years were aligned to a common **30 m** grid in **WGS 84 / UTM Zone 31N (EPSG:32631)**.

Final classes:

1. Built-up
2. Vegetation
3. Water
4. Bare soil

## Workflow

1. Rebuilt comparable 2013 and 2023 Landsat predictor stacks.
2. Used a Random Forest classifier for four-class LULC mapping.
3. Audited the initial reconstruction for leakage, domain shift and implausible class patterns.
4. Conducted targeted blinded human review of deployment-domain samples.
5. Split the final deployment review into **32 calibration samples** and **16 locked holdout samples**.
6. Selected the deployment repair without using locked-holdout labels.
7. Froze the repaired model before opening the holdout.
8. Reclassified both years on an identical common analysis footprint.
9. Ran spectral, temporal and spatial consistency checks.
10. Froze the final classification before producing maps, transition analysis, figures and public documentation.

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

Because the locked holdout contains only 16 samples, the raw case count should be interpreted alongside the percentage metrics. Per-class scores with very small support should also be treated cautiously.

## Scientific evidence hierarchy

The project keeps four evidence types separate:

1. **Independent locked-holdout validation** — final predictive evidence.
2. **Calibration-only out-of-fold evaluation** — development evidence used during repair selection.
3. **Spectral consistency diagnostics** — wall-to-wall plausibility checks using NDVI, NDBI and MNDWI.
4. **Temporal and spatial consistency checks** — common-footprint and change-pattern sanity checks.

Only the locked holdout is treated as final independent classification accuracy. The other diagnostics support scientific plausibility but are not merged into a synthetic accuracy score.

## Planning interpretation

The final reconstruction shows substantial urban expansion accompanied by a nearly equal decline in vegetation. The transition matrix indicates that this was overwhelmingly associated with conversion of vegetated land to built-up surfaces.

For planning, the pattern supports closer monitoring of peripheral urban growth, stronger development control, protection of strategically important green areas, and infrastructure planning that anticipates continued outward expansion. The analysis identifies where land-cover conversion occurred; it does not by itself establish the demographic, economic or regulatory causes of that conversion.

## Main project outputs

The completed scientific package includes:

- final 2013 and 2023 LULC rasters;
- publication-quality 2013 and 2023 maps;
- a 2013–2023 comparison map;
- a full 4 × 4 transition matrix;
- stable-vs-changed mapping;
- built-up expansion mapping;
- vegetation-to-built-up conversion mapping;
- class-area and net-change tables;
- eight statistical figures;
- independent validation evidence;
- spectral and temporal consistency audits; and
- final technical and portfolio documentation.

## Repository structure

```text
.
├── assets/                 # Cover and repository graphics
├── data/                   # Data and processed project inputs
├── docs/                   # Project documentation
├── notebooks/              # Analysis / review notebooks
├── outputs/                # Maps, charts and result products
├── scripts/                # Earth Engine and Python workflows
└── validation/             # Validation and repository checks
```

The historical files are retained as provenance. Final published claims should use the frozen reconstruction results reported in this README rather than superseded original statistics.

## Tools

- Google Earth Engine
- Python
- Rasterio
- GeoPandas
- Pandas
- NumPy
- scikit-learn
- Matplotlib
- Google Colab
- Git / GitHub

## Limitations

- The final independent holdout contains 16 samples.
- Landsat's 30 m resolution can produce mixed pixels in heterogeneous urban areas.
- The four-class scheme generalises more detailed urban and environmental land-cover types.
- Spectral and temporal consistency tests do not replace independent reference data.
- Change detection quantifies mapped conversion but does not establish its socioeconomic causes.

## Author

**Abdullah Abdazeez Ayomide**  
Geo-spatial Planner | GIS & Remote Sensing Analyst | Urban & Environmental Planning Researcher

- [GitHub](https://github.com/Abdullahabdazeez)
- [LinkedIn](https://ng.linkedin.com/in/abdazeez-abdullah-4b814719a)
- [Email](mailto:abdazeezabdullah1@gmail.com)

## Citation and licence

Code is available under the MIT License. When citing results, use the **final reconstructed and frozen 2013–2023 outputs** rather than superseded statistics from the original workflow.
