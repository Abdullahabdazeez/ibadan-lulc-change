# Methodology

The analysis used Landsat 8 Collection 2 Level-2 imagery to produce separate 2013 and 2023 median composites. QA-based cloud, shadow, cirrus, and saturation masks were applied before calculating NDVI, NDBI, MNDWI, BSI, and EVI alongside the six optical bands.

Dynamic World class probabilities and conservative spectral rules supplied reference candidates for built-up land, vegetation, water, and bare soil. Stratified samples were balanced across the four classes and split into 70% training and 30% validation subsets. Separate Random Forest models were trained for each year using 300 trees, a 0.70 bag fraction, and two-sample minimum leaf population. A one-pixel focal mode filter reduced isolated classification noise.

Classification performance was assessed with confusion matrices, overall accuracy, Kappa, producer’s accuracy, and consumer’s accuracy. Post-classification comparison generated the 16-class transition raster, area statistics, net-change table, and built-up gain layer. All final rasters use WGS 84 / UTM Zone 31N (EPSG:32631) at 30 m resolution.
