'''
    Module to handle full data orchestration 
'''
import argparse
from pandas import DataFrame

from life_expectancy.countries import Region

from life_expectancy.cleaning import LifeExpectancyOperations
from life_expectancy.data_io import load_data

IMPORT_FILE_PATH = './life_expectancy/data/eu_life_expectancy_raw.tsv'

def life_expectancy_orchestration(country_code: Region = Region.PT,
                                  input_file_path = None) -> DataFrame:
    '''Performs whole orchestrantion pipeline for life_expectancy data.'''
    
    lifeExpectancyOperations = LifeExpectancyOperations(
        raw_df=load_data(input_file_path)
        ) # pylint: disable=invalid-name

    df_filtered = lifeExpectancyOperations.filter_region(country_code)

    return df_filtered


if __name__ == "__main__":
    # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("country_code", help = 'country code', nargs="?", type=str, default='PT')
    args = parser.parse_args()

    region = Region[args.country_code]
    
    life_expectancy_orchestration(country_code=region,
                                  input_file_path=IMPORT_FILE_PATH)