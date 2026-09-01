from pathlib import Path
import json
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
fail = []

required = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "project.json",
    "docs/METHODOLOGY.md",
    "docs/RESULTS.md",
    "docs/LIMITATIONS.md",
    "outputs/tables/classification_accuracy.csv",
    "outputs/tables/key_findings.csv",
    "outputs/tables/lulc_area_change_summary.csv",
    "outputs/tables/transition_matrix_sqkm.csv",
    "outputs/charts/final_area_comparison.svg",
    "outputs/charts/final_change_summary.svg",
    "outputs/charts/final_validation.svg",
    "data/processed/tables/Ibadan_Final_Area_Table_2013.csv",
    "data/processed/tables/Ibadan_Final_Area_Table_2023.csv",
    "data/processed/tables/Ibadan_Final_Net_Change_2013_2023.csv",
    "data/processed/tables/Ibadan_Final_Transition_Table_2013_2023.csv",
]

for rel in required:
    if not (ROOT / rel).exists():
        fail.append(f"Missing: {rel}")

# Public summary tables intentionally round areas to three decimals.
summary_path = ROOT / "outputs/tables/lulc_area_change_summary.csv"
if summary_path.exists():
    df = pd.read_csv(summary_path)
    built = df.loc[df["class_name"] == "Built-up"].iloc[0]
    veg = df.loc[df["class_name"] == "Vegetation"].iloc[0]
    checks = {
        "Built-up 2013": (float(built["area_2013_sqkm"]), 99.8658),
        "Built-up 2023": (float(built["area_2023_sqkm"]), 330.1767),
        "Built-up net change": (float(built["net_change_sqkm"]), 230.3109),
        "Vegetation net change": (float(veg["net_change_sqkm"]), -230.3307),
    }
    for name, (actual, expected) in checks.items():
        if abs(actual - expected) > 5e-4:
            fail.append(f"{name}: {actual} != {expected} within rounding tolerance")

acc_path = ROOT / "outputs/tables/classification_accuracy.csv"
if acc_path.exists():
    acc = pd.read_csv(acc_path).iloc[0]
    if int(acc["n"]) != 16 or int(acc["correct"]) != 14:
        fail.append("Locked-holdout case count is not 14/16")
    if abs(float(acc["overall_accuracy_pct"]) - 87.50) > 1e-6:
        fail.append("Final overall accuracy is not 87.50%")
    if abs(float(acc["kappa"]) - 0.7935) > 1e-6:
        fail.append("Final Kappa is not 0.7935")

transition_path = ROOT / "outputs/tables/transition_matrix_sqkm.csv"
if transition_path.exists():
    tr = pd.read_csv(transition_path)
    veg_to_built = float(tr.loc[tr["from_class_name"] == "Vegetation", "Built-up"].iloc[0])
    total = tr[["Built-up", "Vegetation", "Water", "Bare soil"]].to_numpy().sum()
    if abs(veg_to_built - 246.1041) > 1e-4:
        fail.append("Vegetation-to-built-up transition is not 246.1041 km²")
    if abs(total - 3220.5807) > 1e-4:
        fail.append(f"Transition area total is {total}, expected 3220.5807")

metadata_path = ROOT / "project.json"
if metadata_path.exists():
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("status") != "final-reconstruction-accepted-and-frozen":
        fail.append("project.json does not mark the reconstruction as final and frozen")

superseded = [
    "outputs/maps/01_lulc_2013.png",
    "outputs/maps/02_lulc_2023.png",
    "outputs/maps/03_built_up_gain_2013_2023.png",
    "outputs/maps/04_major_transitions_2013_2023.png",
    "outputs/charts/00_workflow.png",
    "outputs/charts/01_area_comparison.png",
    "outputs/charts/02_net_change.png",
    "outputs/charts/03_transition_matrix.png",
    "data/processed/rasters/Ibadan_Final_LULC_2013.tif",
    "data/processed/rasters/Ibadan_Final_LULC_2023.tif",
    "data/processed/rasters/Ibadan_Final_Transition_2013_2023.tif",
    "data/processed/rasters/Ibadan_BuiltUp_Gain_2013_2023.tif",
]
for rel in superseded:
    if (ROOT / rel).exists():
        fail.append(f"Superseded public artifact still present: {rel}")

for path in ROOT.rglob("*"):
    if path.is_file() and path.stat().st_size > 95 * 1024 * 1024:
        fail.append(f"Large file: {path.relative_to(ROOT)}")

if fail:
    print("VALIDATION FAILED")
    for item in fail:
        print("-", item)
    sys.exit(1)

print("VALIDATION PASSED")
print("Final tables, validation metrics, metadata and public artifact provenance are synchronized with the frozen reconstruction.")
