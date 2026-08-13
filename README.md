<p align="center">
  <img src="assets/project-cover.png" alt="Ibadan land-cover change project" width="100%">
</p>

# Ibadan Land-Cover Change, 2013–2023

> **Audit status — reconstruction in progress**
>
> The results currently stored in this repository came from the original workflow and are retained for transparency. A later forensic review could not recover adequate independent reference samples, confusion matrices or acquisition-date evidence for the published accuracy and change claims. Those figures are therefore **superseded and should not be cited as validated results**.

## Why the project is being reconstructed

The original study classified built-up land, vegetation, water and bare soil from Landsat imagery and compared the 2013 and 2023 maps. During a 2026 scientific audit, I found that the repository did not contain enough evidence to independently verify:

- the reported 2013 and 2023 accuracy figures;
- the independence of the original calibration and validation samples;
- seasonal comparability between the two observation years; and
- the headline land-cover change estimates.

I therefore started a full reconstruction instead of continuing to present the earlier results as final.

## Reconstruction completed so far

The revised workflow now includes:

- seasonally matched April–June Landsat composites for both years;
- six surface-reflectance bands and NDVI, NDBI and MNDWI predictors;
- a human-reviewed reference set;
- nested, stratified out-of-fold validation;
- explicit checks for overlap between model-development and validation records; and
- a strict common spatial mask for year-to-year comparison.

The current leakage-free model was evaluated on 182 human-reference records and produced:

| Metric | Current reconstruction result |
|---|---:|
| Overall accuracy | 78.57% |
| Balanced accuracy | 71.46% |
| Macro F1 | 72.51% |
| Kappa | 0.639 |
| Built-up precision | 69.23% |
| Built-up recall | 52.94% |

These results are more modest than the original figures but are supported by a stronger validation design.

## Current limitation

The first common-mask reconstruction still showed an implausible class pattern, especially unusually extensive water and very limited bare soil. Its audit therefore ended with **CLASS_PATTERN_REVIEW_REQUIRED**.

A targeted human-review and deployment-repair stage began but has not yet been completed. For that reason:

- no revised land-cover area table is presented as final;
- no revised change statistic is promoted as authoritative;
- the old maps and tables remain historical repository material; and
- the project should currently be described as **under reconstruction**, not completed.

## Repository contents

The existing folders preserve the original workflow, outputs and supporting files:

```text
.
├── assets/                 # Cover and preview graphics
├── data/processed/         # Superseded original rasters and tables
├── docs/                   # Original project documentation
├── notebooks/              # Results-review notebook
├── outputs/                # Superseded original maps, charts and summaries
├── scripts/                # Original Earth Engine and Python scripts
└── validation/             # Repository-level file checks
```

Repository validation confirms that files are present and readable; it does not establish scientific accuracy.

## Next steps

1. Complete the remaining blinded human review.
2. Repair the built-up/vegetation deployment boundary.
3. Reclassify both years with the accepted model.
4. Inspect class patterns and spatial plausibility.
5. Recalculate change on the strict common mask.
6. Replace the superseded repository outputs only after the final validation gate passes.

## Author

**Abdullah Abdazeez Ayomide**  
Geo-spatial Planner | GIS & Remote Sensing Analyst

- [GitHub](https://github.com/Abdullahabdazeez)
- [LinkedIn](https://ng.linkedin.com/in/abdazeez-abdullah-4b814719a)
- [Email](mailto:abdazeezabdullah1@gmail.com)

## Citation and licence

The code and original documentation remain available under the MIT License. The numerical results currently stored in the repository should not be cited as validated findings while reconstruction is in progress.
