# Project Report: Ibadan Land-Cover Change, 2013–2023

## Background

Ibadan has experienced substantial physical expansion over the past decade, making land-cover change an important planning issue. I developed this project to measure how the city's landscape changed between 2013 and 2023, identify the dominant land-cover transitions, and interpret what those changes mean for urban growth management.

The analysis focuses on four broad classes: **Built-up, Vegetation, Water and Bare soil**.

## What I did

I prepared comparable Landsat imagery for 2013 and 2023 and used a Random Forest classifier to map the four land-cover classes. The predictor set combined six Landsat surface-reflectance bands with **NDVI, NDBI and MNDWI**.

I designed the validation process to keep model development separate from final evaluation. Reference samples were reviewed, calibration data were separated from an independent locked holdout, and the final model was evaluated only after the classification workflow had been fixed. Both years were then classified on the same **30 m** analysis grid to ensure that land-cover change was measured on a common spatial footprint.

## What I found

Built-up land increased from **99.866 km² in 2013 to 330.177 km² in 2023**, a net increase of **230.311 km²**.

The clearest transition was from vegetation to built-up land. **246.104 km²** of land mapped as vegetation in 2013 was mapped as built-up in 2023, accounting for **99.14% of gross new built-up land** in the final transition analysis.

The independent locked holdout contained 16 samples, with **14 of 16 cases classified correctly**. Overall accuracy was **87.50%**, with a **0.7935 Cohen's Kappa**. Because the holdout is small, the raw case count is reported alongside the percentage metrics.

## What the result means

The analysis points to substantial outward urban expansion and a large conversion of land previously mapped as vegetation. For planning, this strengthens the case for closer monitoring of peri-urban growth, better coordination between infrastructure provision and new development, and greater attention to green-area protection at the expanding urban edge.

The maps show where physical land-cover conversion occurred. They do not, on their own, establish the demographic, economic or policy drivers behind that change.

## Methodological considerations

A larger independent reference sample would strengthen future accuracy assessment, while higher-resolution imagery could improve interpretation in areas where 30 m Landsat pixels contain mixtures of buildings, vegetation and bare surfaces.

A useful next step would be to relate the mapped expansion pattern to planning approvals, road development, population growth or land-market change using independent datasets designed for those questions.

## Main outputs

The repository contains final land-cover maps, a 2013–2023 comparison, transition statistics, validation results and supporting methodology. Key numerical outputs are available in [`outputs/tables`](../outputs/tables/), while the main visual products are organised in [`outputs/maps`](../outputs/maps/) and [`outputs/charts`](../outputs/charts/).

## Professional takeaway

This project demonstrates how satellite imagery and spatial analysis can move beyond describing urban growth to provide evidence for land-use monitoring, infrastructure planning and environmental management.

---

**Abdullah Abdazeez Ayomide**  
Urban & Regional Planner · GIS & Remote Sensing · Spatial Decision Support
