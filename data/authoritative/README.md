# Authoritative raster inputs

This directory is reserved for the two accepted Ibadan land-cover classification rasters used to generate the final portfolio map suite.

Required files:

- `Ibadan_LULC_2013_FINAL.tif`
  - SHA-256: `a5c3250f3044286ca29fc1ece13ddea282b71b9d34d1844c2c96c88cab04cc61`
- `Ibadan_LULC_2023_FINAL.tif`
  - SHA-256: `e9e85c1dc0b64ea2943fe5983d409e6d7b6e2a5ece08d4dd90d19dc109f94ff7`

Both rasters use the locked class schema:

- 0 = outside final common analysis footprint
- 1 = Built-up
- 2 = Vegetation
- 3 = Water
- 4 = Bare soil

The GitHub Actions map workflow verifies both SHA-256 hashes before generating any publication asset. This prevents an older or non-authoritative classification from being used accidentally.

The authoritative common analysis footprint is 3,578,423 pixels (3,220.581 km²) at 30 m resolution in WGS 84 / UTM Zone 31N (EPSG:32631).
