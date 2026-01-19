'''
    Module to handle DataFrame input/ouput
'''
# pylint: disable=trailing-whitespace
# pylint: disable=too-few-public-methods
# pylint: disable=protected-access
from pandas import DataFrame, read_csv

OUTPUT_FILE_PATH = './life_expectancy/data/{}_life_expectancy.csv'

def load_data(input_file_path: str) -> DataFrame:
    '''Load raw life expectancy data.'''
    return read_csv(input_file_path, sep='\t', header=0)

def write_data(df: DataFrame,
               country_code: str = 'PT') -> None:
    '''Write cleaned data to CSV file.'''
    df.to_csv(OUTPUT_FILE_PATH.format(country_code.lower()))
