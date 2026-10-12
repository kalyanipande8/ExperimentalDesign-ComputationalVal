"""Rigorous experimental validation workflow: Pearson/Spearman
correlation with significance testing, RMSE, and Bland-Altman agreement
analysis (the standard method-comparison technique, Bland & Altman 1986)
-- comparing computational predictions against lab benchmark measurements.
"""
from __future__ import annotations

import numpy as np
from scipy import stats


def correlation_analysis(df) -> dict:
    pearson_r, pearson_p = stats.pearsonr(df["computational_prediction"], df["lab_measurement"])
    spearman_r, spearman_p = stats.spearmanr(df["computational_prediction"], df["lab_measurement"])
    return {
        "pearson_r": round(float(pearson_r), 4), "pearson_p_value": round(float(pearson_p), 6),
        "spearman_r": round(float(spearman_r), 4), "spearman_p_value": round(float(spearman_p), 6),
    }


def rmse_analysis(df) -> dict:
    diff = df["computational_prediction"] - df["lab_measurement"]
    rmse = float(np.sqrt((diff ** 2).mean()))
    mae = float(diff.abs().mean())
    return {"rmse": round(rmse, 3), "mae": round(mae, 3)}


def bland_altman_analysis(df) -> dict:
    """Bland & Altman (1986), Lancet -- the standard method-agreement
    technique: mean difference (bias) and 95% limits of agreement."""
    diff = df["computational_prediction"] - df["lab_measurement"]
    mean_diff = float(diff.mean())
    sd_diff = float(diff.std())
    loa_lower = mean_diff - 1.96 * sd_diff
    loa_upper = mean_diff + 1.96 * sd_diff
    return {
        "mean_bias": round(mean_diff, 3),
        "limits_of_agreement": [round(loa_lower, 3), round(loa_upper, 3)],
        "pct_within_limits": round(100 * ((diff >= loa_lower) & (diff <= loa_upper)).mean(), 2),
    }


def run_validation(df) -> dict:
    return {
        "n_compounds": len(df),
        "correlation": correlation_analysis(df),
        "error_metrics": rmse_analysis(df),
        "bland_altman": bland_altman_analysis(df),
    }


if __name__ == "__main__":
    from .simulate_benchmark import simulate

    df = simulate()
    import json
    print(json.dumps(run_validation(df), indent=2))
