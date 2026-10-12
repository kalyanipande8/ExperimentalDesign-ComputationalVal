"""End-to-end: simulate paired computational/lab data, run the validation
workflow (correlation, error metrics, Bland-Altman), and verify
reproducibility."""
import json
import os

from src.simulate_benchmark import simulate
from src.validation_workflow import run_validation
from src.reproducibility_check import check_reproducibility

os.makedirs("data", exist_ok=True)
os.makedirs("results", exist_ok=True)

print("=== Simulating 150 paired computational/lab measurements ===")
df = simulate()
df.to_csv("data/benchmark_pairs.csv", index=False)
print(df.shape)

print("\n=== Validation workflow ===")
validation = run_validation(df)
print(json.dumps(validation, indent=2))

print("\n=== Reproducibility check (same seed, run twice) ===")
reproducibility = check_reproducibility()
print(reproducibility)

summary = {
    "n_compounds": validation["n_compounds"],
    "pearson_r": validation["correlation"]["pearson_r"],
    "rmse": validation["error_metrics"]["rmse"],
    "bland_altman_pct_within_limits": validation["bland_altman"]["pct_within_limits"],
    "pct_reproducible": reproducibility["pct_reproducible"],
}
with open("results/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== Summary ===")
print(json.dumps(summary, indent=2))
