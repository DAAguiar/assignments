'''
    Module to import and clean eu_life_expectancy_raw
'''
# pylint: disable=trailing-whitespace
# pylint: disable=too-few-public-methods
# pylint: disable=protected-access
import argparse

from pandas import DataFrame, read_csv, melt
from numpy import nan

class LifeExpectancyOperations():
    '''Class to handle life expectancy data loading, cleaning, and saving operations.'''

    IMPORT_FILE_PATH = './life_expectancy/data/eu_life_expectancy_raw.tsv'
    OUTPUT_FILE_PATH = './life_expectancy/data/{}_life_expectancy.csv'
    
    def __init__(self):
        pass

    def _load_data(self) -> DataFrame :
        '''Load raw life expectancy data from TSV file.'''
        return read_csv(self.IMPORT_FILE_PATH, sep='\t', header=0)
    
    def _unpivot_years(self, df: DataFrame, year_columns: str, variable_columns: str):
        '''Transform year columns into rows.'''
        return melt(df, id_vars=variable_columns, value_vars=year_columns, var_name='year')

    def _seperate_and_rename_categories(self, df: DataFrame, variable_columns: str):
        '''Split combined category column into separate unit, sex, age, and region columns.'''
        df[['unit','sex','age','geo\time']] = df[variable_columns[0]].str.split(',',expand=True)
        
        df = df.drop(variable_columns[0],axis=1)
        
        df = df.rename(columns={"geo\time":'region'})

        df = df.reindex(columns=['unit','sex','age','region', 'year', 'value'])
        
        return df
    
    def _cast_numeric_fields(self, df:DataFrame):
        '''Convert year and value columns to appropriate numeric types.'''
        df['year'] = df['year'].astype("int")
        df['value'] = df['value'].str.extract(r'(\d+(?:\.\d+)?)', expand=False)
        df['value'] = df['value'].replace(":", nan)
        df['value'] = df['value'].replace("...", nan)
        df['value'] = df['value'].astype("float")
        return df 

    def _remove_nan(self, df: DataFrame) -> DataFrame:
        '''Remove rows containing missing values.'''
        return df.dropna()

    def _clean_data(self, df: DataFrame) -> DataFrame:
        '''Apply all cleaning transformations to the raw data.'''
        columns = df.columns
        year_columns = columns[1:]
        variable_columns = columns[:1]

        df_unpivot = self._unpivot_years(df, year_columns, variable_columns)
        
        df_unpivot = self._seperate_and_rename_categories(df_unpivot, variable_columns)

        df_unpivot = self._cast_numeric_fields(df_unpivot)
        
        df_unpivot = df_unpivot.dropna()
        
        return df_unpivot
    
    def _write_dataframe(self, df: DataFrame, country_code: str) -> None:
        '''Save cleaned dataframe to CSV file.'''
        df.to_csv(self.OUTPUT_FILE_PATH.format(country_code.lower()), 
                  index=False)


def load_data(data_operations: LifeExpectancyOperations) -> DataFrame:
    '''Load raw life expectancy data.'''
    return data_operations._load_data()


def clean_data(data_operations: LifeExpectancyOperations,
               df: DataFrame,
               country_code: str = 'PT') -> DataFrame:
    '''Clean data and filter for specified country.'''
    df_cleaned = data_operations._clean_data(df)

    df_cleaned_country = df_cleaned[df_cleaned['region'] == country_code.upper()]

    return df_cleaned_country

def write_data(data_operations: LifeExpectancyOperations,
               df: DataFrame,
               country_code: str = 'PT') -> None:
    '''Write cleaned data to CSV file.'''
    data_operations._write_dataframe(df, country_code.upper())


def life_expectancy_orchestration(country_code: str = 'PT') -> DataFrame:
    '''Performs whole orchestrantion pipeline for life_expectancy data.'''
    lifeExpectancyOperations = LifeExpectancyOperations() # pylint: disable=invalid-name

    df_life_expectancy = load_data(lifeExpectancyOperations)

    df_life_expectancy_country_clean = clean_data(lifeExpectancyOperations,
                                                  df_life_expectancy,
                                                  country_code)
    
    write_data(lifeExpectancyOperations,
               df_life_expectancy_country_clean,
               country_code)

if __name__ == "__main__":
    # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("country_code", help = 'country code', nargs="?", type=str, default='PT')
    args = parser.parse_args()

    life_expectancy_orchestration(country_code=args.country_code)