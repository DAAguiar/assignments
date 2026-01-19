import argparse

from pandas import DataFrame

from life_expectancy.cleaning import LifeExpectancyOperations
from life_expectancy.data_io import load_data, write_data

IMPORT_FILE_PATH = './life_expectancy/data/eu_life_expectancy_raw.tsv'

def life_expectancy_orchestration(country_code: str = 'PT',
                                  input_file_path = None) -> DataFrame:
    '''Performs whole orchestrantion pipeline for life_expectancy data.'''
    
    
    
    lifeExpectancyOperations = LifeExpectancyOperations(
        raw_df=load_data(input_file_path)
        ) # pylint: disable=invalid-name

    df_filtered = lifeExpectancyOperations.filter_region(country_code=country_code)

    write_data(df_filtered, country_code)
    
    return df_filtered


if __name__ == "__main__":
    # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("country_code", help = 'country code', nargs="?", type=str, default='PT')
    args = parser.parse_args()

    life_expectancy_orchestration(country_code=args.country_code,
                                  input_file_path=IMPORT_FILE_PATH)