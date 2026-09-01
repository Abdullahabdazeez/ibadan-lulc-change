# Project Report: Ibadan Land-Cover Change, 2013–2023

## Background

Ibadan has expanded rapidly, but the scale and direction of that growth are easier to understand when the physical change on the ground is measured consistently over time. I developed this project to compare the city's land cover in 2013 and 2023 and to see which land-cover types were most often converted as built-up areas expanded.

The analysis focuses on four broad classes: Built-up, Vegetation, Water and Bare soil.

## What I did

I prepared comparable Landsat imagery for 2013 and 2023 and used a Random Forest classifier to map the four land-cover classes. The predictors included six Landsat surface-reflectance bands together with NDVI, NDBI and MNDWI.

The project was not accepted after the first classification. A later review showed that the original validation evidence was weaker than I was comfortable presenting as final. I therefore rebuilt the reference data and validation process, introduced blinded review, separated calibration samples from a locked holdout, and froze the final model before opening the holdout.

Both years were then classified on the same 30 m analysis grid so that the change calculation was made on a common footprint.

## What I found

Built-up land increased from **99.866 km² in 2013 to 330.177 km² in 2023**, a net increase of **230.311 km²**.

The clearest transition was from vegetation to built-up land. **246.104 km²** of land mapped as vegetation in 2013 was mapped as built-up in 2023. That accounts for **99.14% of gross new built-up land** in the final transition analysis.

The final locked holdout contained 16 samples. The repaired model correctly classified **14 of 16 cases**, giving an overall accuracy of **87.50%**. Because the holdout is small, I treat the case count and the percentage together rather than presenting the percentage as highly precise.

## What the result means

The analysis points to substantial outward urban expansion and a large conversion of land previously mapped as vegetation. For planning, this supports closer attention to peri-urban growth, development control, green-area protection and the timing of infrastructure provision around the expanding urban edge.

The maps show where land-cover conversion occurred. They do not, on their own, explain the economic, demographic or policy reasons behind the change.

## What I would improve with better data

A larger independent reference sample would strengthen the final accuracy assessment. Higher-resolution imagery could also help in areas where 30 m Landsat pixels contain a mixture of buildings, vegetation and bare surfaces.

A future extension could connect the mapped expansion pattern to planning approvals, road development, population growth or land-market change, but those relationships would need separate evidence rather than being inferred from the land-cover maps alone.

## Main outputs

The repository contains the final land-cover comparison map, transition tables, accuracy results and supporting methodology. The key numerical tables are in [`outputs/tables`](../outputs/tables/) and the main visual comparison is in [`outputs/maps/final_lulc_comparison.svg`](../outputs/maps/final_lulc_comparison.svg).

## Final note

One of the main lessons from this project was methodological rather than cartographic: a convincing map is not enough if the validation behind it is weak. Rebuilding the analysis took longer, but it produced a result I am much more comfortable defending.
