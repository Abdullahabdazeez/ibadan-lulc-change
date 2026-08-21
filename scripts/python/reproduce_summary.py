from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "data" / "processed" / "tables"
OUTPUT = ROOT / "outputs" / "tables"

EXPECTED_AREA = 3220.5807


def main():
    area13 = pd.read_csv(TABLES / "Ibadan_Final_Area_Table_2013.csv")
    area23 = pd.read_csv(TABLES / "Ibadan_Final_Area_Table_2023.csv")
    net = pd.read_csv(TABLES / "Ibadan_Final_Net_Change_2013_2023.csv")
    transitions = pd.read_csv(TABLES / "Ibadan_Final_Transition_Table_2013_2023.csv")

    assert abs(area13["Area_km2"].sum() - EXPECTED_AREA) < 1e-6
    assert abs(area23["Area_km2"].sum() - EXPECTED_AREA) < 1e-6
    assert abs(transitions["area_km2"].sum() - EXPECTED_AREA) < 1e-6

    summary = area13[["Class", "Area_km2", "Percent"]].rename(
        columns={"Area_km2": "Area_2013_km2", "Percent": "Percent_2013"}
    ).merge(
        area23[["Class", "Area_km2", "Percent"]].rename(
            columns={"Area_km2": "Area_2023_km2", "Percent": "Percent_2023"}
        ),
        on="Class",
    )

    summary = summary.merge(
        net[["Class", "Net_Change_km2", "Relative_Change_Percent"]],
        on="Class",
    )

    summary.to_csv(OUTPUT / "recomputed_area_change.csv", index=False)

    veg_to_built = transitions.loc[
        (transitions["from_class"] == "Vegetation")
        & (transitions["to_class"] == "Built-up"),
        "area_km2",
    ].iloc[0]

    print(summary.to_string(index=False))
    print(f"Vegetation -> Built-up: {veg_to_built:.4f} km²")
    print("Final frozen tabular results validated.")


if __name__ == "__main__":
    main()
