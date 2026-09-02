# Study Limitations and Interpretation

The project is designed for **metropolitan-scale land-cover change assessment and urban-growth interpretation**. The following considerations define the appropriate use of the results.

## Spatial resolution

Landsat imagery has a **30 m spatial resolution**. Individual pixels may therefore contain combinations of roofs, roads, vegetation, exposed soil or water, particularly along urban edges and within heterogeneous neighbourhoods. The resulting maps are appropriate for city-scale pattern analysis rather than parcel-level development control.

## Classification detail

The analysis uses four broad land-cover classes — **Built-up, Vegetation, Water and Bare soil**. These classes provide a consistent basis for measuring physical landscape change but do not distinguish individual urban land uses, vegetation communities, agricultural systems or building types.

## Independent validation

Final predictive performance is assessed using a **16-sample independent holdout**, with **14 of 16 samples correctly classified**. The holdout provides evidence independent of model fitting, while its limited size means that percentage metrics are interpreted alongside the underlying case count. Per-class statistics with small sample support should likewise be interpreted cautiously.

## Spectral interpretation

NDVI, NDBI and MNDWI provide useful spectral evidence for vegetation, built-up surfaces and water. Their wall-to-wall consistency patterns support interpretation of the classified maps but are not substitutes for independent reference observations.

## Change attribution

Post-classification comparison identifies the **location, direction and magnitude of mapped land-cover transitions**. It does not independently establish the demographic, economic, institutional or regulatory causes of urban expansion. Explaining those drivers requires complementary socioeconomic, planning-policy and field evidence.

## Appropriate application

The outputs support metropolitan planning, urban-growth monitoring, environmental assessment and identification of areas experiencing substantial land-cover conversion. Higher-resolution imagery, cadastral information and field verification should be incorporated before site-specific or regulatory decisions are made.

---

**Project:** Ibadan Land-Cover Change and Urban Expansion, 2013–2023  
**Author:** Abdullah Abdazeez Ayomide  
Urban & Regional Planner · GIS & Remote Sensing · Spatial Decision Support
