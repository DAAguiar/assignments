"""Pytest configuration file"""
import pandas as pd
import pytest
from life_expectancy.data_io import load_data


from . import FIXTURES_DIR

# pylint: disable=trailing-whitespace


@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected.csv")

@pytest.fixture(scope="session")
def pt_life_expectancy_raw() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return load_data(FIXTURES_DIR / "eu_life_expectancy_raw.tsv")

