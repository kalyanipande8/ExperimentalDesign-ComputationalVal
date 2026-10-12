import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.simulate_benchmark import simulate
from src.validation_workflow import run_validation
from src.reproducibility_check import check_reproducibility


@pytest.fixture(scope="module")
def df():
    return simulate()


def test_150_compounds_simulated(df):
    assert len(df) == 150


def test_computational_and_lab_values_are_correlated_but_not_identical(df):
    assert not (df["computational_prediction"] == df["lab_measurement"]).all()
    corr = df["computational_prediction"].corr(df["lab_measurement"])
    assert corr > 0.5


def test_validation_workflow_returns_all_sections(df):
    result = run_validation(df)
    assert set(result.keys()) == {"n_compounds", "correlation", "error_metrics", "bland_altman"}


def test_correlation_is_statistically_significant(df):
    result = run_validation(df)
    assert result["correlation"]["pearson_p_value"] < 0.001


def test_bland_altman_most_points_within_limits(df):
    result = run_validation(df)
    assert result["bland_altman"]["pct_within_limits"] >= 90.0


def test_reproducibility_is_genuinely_100_percent():
    result = check_reproducibility()
    assert result["data_identical"] is True
    assert result["n_mismatches"] == 0
    assert result["pct_reproducible"] == 100.0
