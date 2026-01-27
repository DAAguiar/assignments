"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import LifeExpectancyOperations

def test_clean_data(pt_life_expectancy_expected: pd.DataFrame,
                    pt_life_expectancy_raw: pd.DataFrame):
    """Run the `clean_data` function and compare the output to the expected output"""
    lifeExpectancyOperations = LifeExpectancyOperations(
        pt_life_expectancy_raw
        )
    
    pt_life_expectancy_actual = lifeExpectancyOperations.filter_region(country_code="PT")

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
