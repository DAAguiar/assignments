"""
Unit tests for the pyproject.toml file.

It's very uncommon to write unit tests for a configuration file. However,
since we are learning, this is a special case.

Once you have ensured that the package and its dependencies are installed,
feel free to delete this file.
"""

from pkg_resources import DistributionNotFound, get_distribution
from unittest.mock import patch
from unittest import mock


import toml
import pytest
import pylint
import pytest_cov
import pandas as pd

from . import PROJECT_DIR

from life_expectancy.cleaning import LifeExpectancyOperations

def test_dependencies():
    """Test that the get_versions function return 4 values."""
    deps = (
        pd.__version__,
        pytest.__version__,
        pytest_cov.__version__,
        pylint.__version__,
    )
    assert len(deps) == 4


def test_pyproject():
    """Test that the pyproject.toml is correct."""
    pyproject = toml.load(PROJECT_DIR / "pyproject.toml")

    authors = pyproject["project"]["authors"]
    has_new_author = False
    for author in authors:
        if not author["name"].startswith("Fernando Cordeiro"):
            has_new_author = True

    assert pyproject["project"]["name"] == "life_expectancy"
    assert has_new_author, (
        "The author of the package is not Fernando Cordeiro. You should "
        "add your own name to the pyproject.toml file."
    )


def test_package():
    """Test that the life_expectancy package is installed."""
    try:
        installed_package = get_distribution("life_expectancy")
    except DistributionNotFound:
        assert False, (
            "The life_expectancy package is not installed. If you have "
            "installed the package, check that the name of the package "
            "in the pyproject.toml file is `life_expectancy`."
        )
    assert installed_package.version == "0.1.0", (
        "The life_expectancy package is installed, but it is not the "
        "correct version. If you have installed the package, check "
        "that the version of the package in the pyproject.toml file "
        "is `0.1.0`."
    )


@patch("life_expectancy.data_io.read_csv")
def test_load_data(mock_read_csv: mock):
    from life_expectancy.data_io import load_data

    input_str = "./life_expectancy/data/eu_life_expectancy_raw.tsv"
    _ = load_data(input_str)
    mock_read_csv.assert_called_once_with(input_str, sep="\t", header=0)


def test_write_data():
    from life_expectancy.data_io import OUTPUT_FILE_PATH, write_data

    output_path = OUTPUT_FILE_PATH.format("pt")

    with patch.object(pd.DataFrame, "to_csv", return_value=None) as mock_write_csv:
        df = pd.DataFrame()

        write_data(df)

    mock_write_csv.assert_called_once_with(output_path)


@patch("life_expectancy.full_orchestration.LifeExpectancyOperations")
@patch("life_expectancy.full_orchestration.load_data")
def test_life_expectancy_orchestration(mock_load_data, mock_life_exp_ops):
    from life_expectancy.full_orchestration import life_expectancy_orchestration

    input_file_path = "./test_path.tsv"

    mock_df_raw = pd.DataFrame({"col": [1, 2, 3]})
    mock_df_filtered = pd.DataFrame({"col": [1]})

    mock_load_data.return_value = mock_df_raw
    mock_instance = mock_life_exp_ops.return_value
    mock_instance.filter_region.return_value = mock_df_filtered

    result = life_expectancy_orchestration(
        country_code="PT", input_file_path=input_file_path
    )

    mock_load_data.assert_called_once_with(input_file_path)
    mock_life_exp_ops.assert_called_once_with(raw_df=mock_df_raw)
    mock_instance.filter_region.assert_called_once_with(country_code="PT")
    assert result.equals(mock_df_filtered)


def test_clean_and_filter_region(raw_df, expected_filtered_df):
    lifeExpectancyOperations = LifeExpectancyOperations(raw_df)

    df_filtered = lifeExpectancyOperations.filter_region(country_code="PT")

    pd.testing.assert_frame_equal(df_filtered, expected_filtered_df)


@patch.object(LifeExpectancyOperations, '_clean_data')
def test_filter_region_unit(mock_clean_data):
    
    mock_cleaned_df = pd.DataFrame([
        ["YR", "F", "Y65", "PT", 2020, 21.0],
        ["YR", "F", "Y65", "BE", 2020, 22.2],
        ["YR", "F", "Y65", "PT", 2021, 21.2],
    ], columns=["unit", "sex", "age", "region", "year", "value"])
    
    mock_clean_data.return_value = mock_cleaned_df
    
    ops = LifeExpectancyOperations(pd.DataFrame()) 
    result = ops.filter_region(country_code='PT')
    
    expected = pd.DataFrame([
        ["YR", "F", "Y65", "PT", 2020, 21.0],
        ["YR", "F", "Y65", "PT", 2021, 21.2],
    ], columns=["unit", "sex", "age", "region", "year", "value"]).reset_index(drop=True)
    
    pd.testing.assert_frame_equal(result, expected)

@pytest.fixture()
def raw_df():
    data = [
        ["YR,F,Y65,PT", "21.0", "21.2"],
        ["YR,F,Y65,BE", "22.2", "15.6"],
        ["YR,F,Y65,CH", ":", "23.1"],
    ]
    return pd.DataFrame(data, columns=["unit,sex,age,geo\time", "2020", "2021"])


@pytest.fixture()
def expected_filtered_df():
    data = [["YR", "F", "Y65", "PT", 2020, 21.0], ["YR", "F", "Y65", "PT", 2021, 21.2]]

    return pd.DataFrame(
        data, columns=["unit", "sex", "age", "region", "year", "value"]
    ).reset_index(drop=True)
