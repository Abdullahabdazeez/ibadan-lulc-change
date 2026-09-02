# Results

## A decade of urban expansion

The analysis covers **3,220.581 km²** of the Ibadan metropolitan area on a common 30 m grid. Built-up land increased from **99.866 km² (3.101%)** in 2013 to **330.177 km² (10.252%)** in 2023. This represents a net increase of **230.311 km²**, or **230.62%** relative to the 2013 built-up area.

Over the same period, Vegetation declined from **3,112.233 km² (96.636%)** to **2,881.903 km² (89.484%)**, a net loss of **230.331 km²**. Water changed from **5.063 km²** to **4.199 km²**, while Bare soil changed from **3.418 km²** to **4.302 km²**.

## Where did the new built-up land come from?

The dominant transition was **Vegetation → Built-up**, covering **246.104 km²**. Gross new built-up land totalled **248.235 km²**, meaning **99.14%** of land newly mapped as built-up had been classified as vegetation in 2013.

Across the full study area, **91.50%** remained in the same land-cover class and **8.50%** changed class. The spatial pattern therefore shows substantial urban expansion concentrated within a relatively small share of the metropolitan landscape.

## Independent validation

I evaluated the final classifier using a **16-sample locked holdout** kept separate from model fitting and calibration. The classifier correctly identified **14 of 16** independent samples.

| Metric | Result |
|---|---:|
| Overall Accuracy | **0.8750** |
| Balanced Accuracy | **0.9259** |
| Macro F1 | **0.6354** |
| Cohen's Kappa | **0.7935** |

The holdout is intentionally independent but small, so the **14/16 case count** should be considered alongside the percentage-based metrics. Supporting spectral, temporal and spatial consistency checks provide additional context but are not treated as separate independent accuracy estimates.

## Planning interpretation

The results point to rapid outward growth and substantial conversion of previously vegetated land. For planning, the important issue is not simply that Ibadan became more built-up, but **where expansion occurred and how future growth can be coordinated with infrastructure, environmental protection and development control**.
