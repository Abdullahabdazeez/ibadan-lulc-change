from pathlib import Path
import pandas as pd
import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "data" / "processed" / "tables"
RASTERS = ROOT / "data" / "processed" / "rasters"
OUTPUT = ROOT / "outputs" / "tables"


def main():
    area13 = pd.read_csv(TABLES / "Ibadan_Final_Area_Table_2013.csv")
    area23 = pd.read_csv(TABLES / "Ibadan_Final_Area_Table_2023.csv")
    for frame in (area13, area23):
        frame.drop(columns=[c for c in ["system:index", ".geo"] if c in frame], inplace=True)

    summary = area13[["class_code", "class_name", "area_sqkm"]].rename(
        columns={"area_sqkm": "area_2013_sqkm"}
    ).merge(
        area23[["class_code", "class_name", "area_sqkm"]].rename(
            columns={"area_sqkm": "area_2023_sqkm"}
        ), on=["class_code", "class_name"]
    )
    summary["net_change_sqkm"] = summary["area_2023_sqkm"] - summary["area_2013_sqkm"]
    summary["percentage_change"] = summary["net_change_sqkm"] / summary["area_2013_sqkm"] * 100
    summary.to_csv(OUTPUT / "recomputed_area_change.csv", index=False)

    expected_classes = {0, 1, 2, 3, 4}
    for raster in ["Ibadan_Final_LULC_2013.tif", "Ibadan_Final_LULC_2023.tif"]:
        with rasterio.open(RASTERS / raster) as src:
            values = set(np.unique(src.read(1)).tolist())
            assert values.issubset(expected_classes), f"Unexpected classes in {raster}: {values}"
            assert src.crs.to_epsg() == 32631
            assert abs(src.res[0] - 30) < 1e-6
    print(summary.to_string(index=False))
    print("Input rasters and summary statistics validated.")


if __name__ == "__main__":
    main()
