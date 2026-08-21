# Results

The final reconstruction covers **3,220.581 km²** on a common 30 m analysis grid. Built-up land increased from **99.866 km² (3.101%)** in 2013 to **330.177 km² (10.252%)** in 2023, a net increase of **230.311 km²** or **230.62%** relative to the 2013 built-up area.

Vegetation declined from **3,112.233 km² (96.636%)** to **2,881.903 km² (89.484%)**, a net loss of **230.331 km²**. Water changed from **5.063 km²** to **4.199 km²**, while bare soil changed from **3.418 km²** to **4.302 km²**.

The dominant actual transition was **Vegetation → Built-up**, covering **246.104 km²**. Gross new built-up land totalled **248.235 km²**, meaning **99.14%** of gross new built-up land had been mapped as vegetation in 2013. Overall, **91.50%** of the study area remained in the same class and **8.50%** changed class.

## Independent validation

The final deployment-repaired classifier was evaluated on a **16-sample locked holdout** that was excluded from model fitting and calibration selection. The baseline correctly classified **6/16** cases; the final model correctly classified **14/16**, correcting **8** cases with **0 regressions**.

Final independent metrics:

- Overall Accuracy: **0.8750**
- Balanced Accuracy: **0.9259**
- Macro F1: **0.6354**
- Cohen's Kappa: **0.7935**

Because the locked holdout contains only 16 samples, the raw case count should be interpreted alongside percentage-based metrics. Calibration-only OOF results, spectral consistency checks and temporal/spatial consistency checks are retained separately and are not treated as additional independent accuracy measures.
