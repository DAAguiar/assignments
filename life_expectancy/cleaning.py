'''
    Module to import and clean pt_life_expectancy
'''
# pylint: disable=trailing-whitespace
# pylint: disable=too-few-public-methods
# pylint: disable=protected-access
import argparse

from pandas import DataFrame, read_csv, melt
from numpy import nan



class DataOperations():
    '''
    Docstring for DataOperations
    '''

    IMPORT_FILE_PATH = './life_expectancy/data/eu_life_expectancy_raw.tsv'
    OUTPUT_FILE_PATH = './life_expectancy/data/{}_life_expectancy.csv'
    
    def __init__(self):
        pass

    def _load_data(self) -> DataFrame :
        return read_csv(self.IMPORT_FILE_PATH, sep='\t', header=0)
    
    def _shift_columns(self, df: DataFrame, variable_columns: str) -> DataFrame:
        df_shifed = df.shift(periods=-1, axis='columns')
        df_shifed[variable_columns] = df[variable_columns]        
        return df_shifed
    
    def _unpivot_years(self, df: DataFrame, year_columns: str, variable_columns: str):
        return melt(df, id_vars=variable_columns, value_vars=year_columns, var_name='year')

    def _seperate_and_rename_categories(self, df: DataFrame, variable_columns: str):
        df[['unit', 'sex','age','geo\time']] = df[variable_columns[0]].str.split(',',expand=True)
        
        df = df.drop(variable_columns[0],axis=1)
        
        df = df.rename(columns={"geo\time":'region'})
        
        return df
    
    def _cast_numeric_fields(self, df:DataFrame):
        df['year'] = df['year'].astype("int")
        df['value'] = df['value'].str.extract(r'(\d+(?:\.\d+)?)', expand=False)
        df['value'] = df['value'].replace(":", nan)
        df['value'] = df['value'].replace("...", nan)
        df['value'] = df['value'].astype("float")
        return df 

    def _clean_data(self, df: DataFrame) -> DataFrame:
        columns = df.columns
        year_columns = columns[1:]
        variable_columns = columns[:1]


        df_shifted = self._shift_columns(df, variable_columns)

        df_unpivot = self._unpivot_years(df_shifted, year_columns, variable_columns)
        
        df_unpivot = self._seperate_and_rename_categories(df_unpivot, variable_columns)

        df_unpivot = self._cast_numeric_fields(df_unpivot)
        
        return df_unpivot
    
    def _write_dataframe(self, df: DataFrame, country_code: str) -> None:
        df.to_csv(self.OUTPUT_FILE_PATH.format(country_code.lower()), 
                  index=False)


def clean_data(country_code: str = 'PT') -> None:
    '''
    Docstring for clean_data
    '''

    data_operations = DataOperations()

    df = data_operations._load_data()

    df_cleaned = data_operations._clean_data(df)

    df_cleaned_pt = df_cleaned[df_cleaned['region'] == country_code]

    data_operations._write_dataframe(df_cleaned_pt, country_code.upper())
        
if __name__ == "__main__":
    # pragma: no cover

    parser = argparse.ArgumentParser()
    parser.add_argument("country_code", help = 'country code', type=str, default='PT')
    args = parser.parse_args()

    clean_data(args.country_code)
