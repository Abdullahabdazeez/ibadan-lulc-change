# Data Sources

The analysis combines satellite imagery, spectral indices and administrative boundary data to measure land-cover change across Ibadan between 2013 and 2023.

| Dataset | Provider | Spatial detail | Application |
|---|---|---:|---|
| Landsat Collection 2 Level-2 Surface Reflectance | USGS / Google Earth Engine | 30 m | Primary imagery for the 2013 and 2023 land-cover classifications |
| Dynamic World V1 | Google / World Resources Institute | 10 m probabilities | Supporting land-cover reference information during sample interpretation |
| Administrative boundary data | FAO / project boundary workflow | Administrative polygons | Delineation of the Ibadan metropolitan study area |

## Predictor variables

The Random Forest classification used six Landsat surface-reflectance bands — **SR_B2, SR_B3, SR_B4, SR_B5, SR_B6 and SR_B7** — together with three spectral indices:

- **NDVI** — vegetation response;
- **NDBI** — built-up response; and
- **MNDWI** — surface-water response.

All predictor layers were aligned to a common **30 m analysis grid** in **WGS 84 / UTM Zone 31N (EPSG:32631)** so that the 2013 and 2023 classifications could be compared cell-for-cell.

## Reference and validation data

Reference samples were interpreted for four classes: **Built-up, Vegetation, Water and Bare soil**. Model-development samples were kept separate from a **16-sample independent holdout**, allowing final predictive performance to be assessed on observations excluded from model fitting and selection.

## Data stewardship

The repository contains derived analytical products and documentation rather than redistributing unrestricted copies of source imagery. Original datasets remain subject to the licences, attribution requirements and terms of their respective providers.

---

**Project:** Ibadan Land-Cover Change and Urban Expansion, 2013–2023  
**Author:** Abdullah Abdazeez Ayomide  
Urban & Regional Planner · GIS & Remote Sensing · Spatial Decision Support
