"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import life_expectancy_orchestration
from . import FIXTURES_DIR


def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""
    input_file_path = FIXTURES_DIR / "eu_life_expectancy_raw.tsv"

    pt_life_expectancy_actual = life_expectancy_orchestration(input_file_path = input_file_path)

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
