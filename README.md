# Ibadan Land-Cover Change and Urban Expansion, 2013–2023

<p align="center">
  <img src="outputs/maps/final_lulc_comparison.svg" alt="Ibadan land-cover comparison for 2013 and 2023" width="100%">
</p>

## Planning question

**How did Ibadan's land cover change between 2013 and 2023, and what type of land was most often converted as the city expanded?**

This project uses Landsat imagery to map four broad land-cover classes — **Built-up, Vegetation, Water and Bare soil** — for 2013 and 2023. The analysis was designed around one practical planning objective: to measure the scale and spatial pattern of urban expansion and identify the dominant land-cover transitions associated with that growth.

The result is clear: **Ibadan expanded substantially, and most of the mapped new built-up land came from areas classified as vegetation in 2013.**

## Key findings

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

The dominant mapped transition was **Vegetation → Built-up**, covering **246.104 km²**. This does not, by itself, explain the demographic or economic causes of expansion, but it clearly identifies where the physical growth of the city was concentrated in the mapped landscape.

## Validation

The final classification was evaluated using an independent **16-sample locked holdout** that was not used for model fitting or calibration selection.

| Metric | Final result |
|---|---:|
| Correct cases | **14/16** |
| Overall Accuracy | **0.8750** |
| Balanced Accuracy | **0.9259** |
| Macro F1 | **0.6354** |
| Cohen's Kappa | **0.7935** |

Because the holdout is small, the raw case count is reported alongside the percentage-based metrics rather than treating the percentages as more precise than the evidence supports.

## Data and model

The final classification uses Landsat surface-reflectance bands **SR_B2, SR_B3, SR_B4, SR_B5, SR_B6 and SR_B7**, together with **NDVI, NDBI and MNDWI**. Both years were aligned to the same **30 m** grid in **WGS 84 / UTM Zone 31N (EPSG:32631)**.

A Random Forest classifier was used to map the four land-cover classes.

## Workflow

1. Prepared comparable 2013 and 2023 Landsat predictor stacks.
2. Developed and reviewed reference samples for the four land-cover classes.
3. Separated calibration data from an independent locked holdout.
4. Trained and selected the final classification model.
5. Classified both years on one common analysis footprint.
6. Evaluated spectral, temporal and spatial consistency.
7. Measured land-cover transitions and built-up expansion.
8. Produced final maps, charts and machine-readable planning evidence.

## Land-cover transitions

All values below are in km².

| 2013 → 2023 | Built-up | Vegetation | Water | Bare soil |
|---|---:|---:|---:|---:|
| **Built-up** | 81.9414 | 17.8236 | 0.0360 | 0.0648 |
| **Vegetation** | **246.1041** | 2861.2584 | 0.6633 | 4.2075 |
| **Water** | 0.0072 | 1.5570 | 3.4992 | 0.0000 |
| **Bare soil** | 2.1240 | 1.2636 | 0.0009 | 0.0297 |

The machine-readable table is available at [`outputs/tables/transition_matrix_sqkm.csv`](outputs/tables/transition_matrix_sqkm.csv).

## Planning implications

The pattern points to rapid outward growth and substantial conversion of land previously mapped as vegetation. For planners, this supports closer monitoring of peri-urban expansion, stronger coordination between infrastructure provision and new development, and greater attention to the protection of important green areas at the urban edge.

This project measures mapped land-cover change. The imagery identifies where physical conversion occurred, while the demographic, economic and regulatory drivers behind that change require separate evidence.

## Maps and outputs

The final cartographic products are organised in [`outputs/maps`](outputs/maps/), while charts and machine-readable tables are available in [`outputs/charts`](outputs/charts/) and [`outputs/tables`](outputs/tables/).

Supporting documentation includes:

- [`docs/PROJECT_REPORT.md`](docs/PROJECT_REPORT.md)
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

The independent holdout contains 16 samples. Landsat's 30 m pixels can also contain more than one surface type in dense or fragmented urban areas, while the four-class scheme simplifies a more complex urban landscape.

The results are therefore most appropriate for broad land-cover change and urban-growth interpretation rather than parcel-level decisions.

## Author

**Abdullah Abdazeez Ayomide**  
Urban & Regional Planner · GIS & Remote Sensing · Spatial Decision Support

[GitHub](https://github.com/Abdullahabdazeez) · [LinkedIn](https://ng.linkedin.com/in/abdazeez-abdullah-4b814719a) · [Email](mailto:abdazeezabdullah1@gmail.com)

## Citation and licence

Code is available under the MIT License. Results and visual outputs should be cited from this repository and attributed to **Abdullah Abdazeez Ayomide (2026)**.
