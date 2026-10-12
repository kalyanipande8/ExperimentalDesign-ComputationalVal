"""Simulate paired computational-prediction vs. lab-benchmark measurements
for 150 compounds -- a real, imperfect correlation (computational
predictions are informative but not perfect), the realistic setting an
experimental validation workflow is designed to characterize."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_COMPOUNDS = 150
SEED = 103


def simulate(n: int = N_COMPOUNDS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    true_property = rng.normal(50, 15, n)  # the real underlying compound property
    computational_prediction = true_property + rng.normal(0, 6, n)  # model error
    lab_measurement = true_property + rng.normal(0, 4, n)  # assay noise

    return pd.DataFrame({
        "compound_id": [f"CPD-{i:04d}" for i in range(n)],
        "computational_prediction": np.round(computational_prediction, 2),
        "lab_measurement": np.round(lab_measurement, 2),
    })


if __name__ == "__main__":
    df = simulate()
    print(df.shape)
    print(df.head())
