# Project Report: Ibadan Land-Cover Change and Urban Expansion, 2013–2023

## Project overview

This project examines how the Ibadan metropolitan landscape changed between 2013 and 2023, with particular attention to the scale of urban expansion and the land-cover types converted as the built-up footprint grew.

The analysis covers **3,220.581 km²** and maps four broad classes: **Built-up, Vegetation, Water and Bare soil**.

## Planning question

**How did Ibadan's land cover change between 2013 and 2023, and what types of land were converted as the city expanded?**

## Data and method

I used Landsat Collection 2 Surface Reflectance imagery for the two study years. The predictor set combined six surface-reflectance bands — **SR_B2, SR_B3, SR_B4, SR_B5, SR_B6 and SR_B7** — with **NDVI, NDBI and MNDWI**.

The 2013 and 2023 datasets were aligned to a common **30 m** analysis grid in **WGS 84 / UTM Zone 31N (EPSG:32631)**. A Random Forest classifier was used to map the four classes, followed by pixel-by-pixel post-classification change analysis.

## Validation

The accepted classification was evaluated with an independent **16-sample holdout**, of which **14 samples were correctly classified**.

| Metric | Result |
|---|---:|
| Overall Accuracy | 0.8750 |
| Balanced Accuracy | 0.9259 |
| Macro F1 | 0.6354 |
| Cohen's Kappa | 0.7935 |

The holdout is small, so the raw **14/16** result is reported alongside the percentage-based metrics.

## Results

Built-up land increased from **99.866 km² (3.101%)** in 2013 to **330.177 km² (10.252%)** in 2023. This represents a net gain of **230.311 km²** and a **230.62%** increase relative to the 2013 built-up area.

Vegetation declined by **230.331 km²** over the same period. The dominant mapped transition was **Vegetation → Built-up**, covering **246.104 km²**.

Gross new built-up land totalled **248.235 km²**, meaning **99.14%** of new built-up land had been classified as vegetation in 2013.

Across the complete study area, **91.50%** remained in the same land-cover class and **8.50%** changed class.

## Planning interpretation

The results show substantial outward urban expansion associated primarily with conversion of vegetated land. This pattern has direct relevance for metropolitan planning because expansion at the urban edge can increase pressure on green/open land while also creating new infrastructure and service requirements.

The evidence supports:

- regular monitoring of urban growth fronts;
- stronger coordination of infrastructure with new development;
- integration of green-space protection into urban expansion strategies; and
- periodic remote-sensing updates to support development management.

The analysis measures physical land-cover conversion. Demographic, economic, land-market and regulatory drivers require complementary evidence and are not inferred directly from the imagery.

## Limitations

The independent holdout contains only 16 samples. Landsat's 30 m pixels may contain mixtures of buildings, roads, vegetation and exposed soil in heterogeneous urban areas. The four-class system also simplifies a more detailed landscape.

The project is therefore most appropriate for **metropolitan-scale land-cover change and urban-growth interpretation**, rather than parcel-level development decisions.

## Main outputs

The repository contains final land-cover maps, change maps, statistical figures, transition tables and validation evidence. Numerical outputs are organised in [`outputs/tables`](../outputs/tables/), maps in [`outputs/maps`](../outputs/maps/) and charts in [`outputs/charts`](../outputs/charts/).

## Author

**Abdullah Abdazeez Ayomide**  
Urban & Regional Planner · GIS & Remote Sensing · Spatial Decision Support
