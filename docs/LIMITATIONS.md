# Limitations

- The final independent locked holdout contains **16 samples**. Percentage metrics should therefore be interpreted together with the raw result of **14/16 correctly classified**.
- Per-class precision, recall and F1 values with very small support should be treated cautiously.
- Landsat's **30 m** pixels can mix roofs, roads, vegetation, soil and other land-cover types within one cell, especially in heterogeneous urban areas and along class boundaries.
- The final map uses four broad classes—Built-up, Vegetation, Water and Bare soil—and does not distinguish detailed urban land uses, vegetation types or agricultural categories.
- Spectral consistency checks using NDVI, NDBI and MNDWI are plausibility diagnostics, not independent ground-truth validation.
- Temporal and spatial consistency checks support interpretation of the reconstruction but do not directly measure classification correctness.
- The transition analysis quantifies mapped land-cover conversion. It does not establish the demographic, economic, institutional or regulatory causes of change without additional evidence.
- The maps are suitable for regional and metropolitan-scale analysis, but higher-resolution imagery and field evidence should be used before parcel-level regulatory or site-specific decisions.
