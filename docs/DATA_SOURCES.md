# Data sources

| Dataset | Provider | Resolution / level | Final role |
|---|---|---:|---|
| Landsat Collection 2 Level-2 surface reflectance | USGS / Google Earth Engine | 30 m | Rebuilt 2013 and 2023 predictor stacks and final spectral indices |
| Dynamic World V1 | Google / World Resources Institute | 10 m probabilities | Supporting reference information during earlier candidate-generation and review stages; not treated as final independent validation |
| Administrative boundary data | FAO / project boundary workflow | Administrative polygons | Delineation of the Ibadan metropolitan analysis area |

The final Random Forest predictor set consisted of **SR_B2, SR_B3, SR_B4, SR_B5, SR_B6, SR_B7, NDVI, NDBI and MNDWI** on a common 30 m grid in **EPSG:32631**.

Final predictive performance was evaluated using visually reviewed deployment-domain samples, including a **16-sample locked holdout** that was not used in model fitting or calibration selection.

All source datasets remain subject to their providers' terms and licences.
