'''
    Module to import and clean eu_life_expectancy_raw
'''
# pylint: disable=trailing-whitespace
# pylint: disable=too-few-public-methods
# pylint: disable=protected-access

from pandas import DataFrame, melt
from numpy import nan

class LifeExpectancyOperations():
    '''Class to handle life expectancy data loading, cleaning, and saving operations.'''

    # IMPORT_FILE_PATH = './life_expectancy/data/eu_life_expectancy_raw.tsv'
    # OUTPUT_FILE_PATH = './life_expectancy/data/{}_life_expectancy.csv'
    
    def __init__(self, raw_df: DataFrame):
        self.raw_df = raw_df

        self.clean_df: DataFrame = self._clean_data()
        self.filtered_df: DataFrame

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

    def _clean_data(self) -> DataFrame:
        '''Apply all cleaning transformations to the raw data.'''
        df = self.raw_df

        columns = df.columns
        year_columns = columns[1:]
        variable_columns = columns[:1]

        df_unpivot = self._unpivot_years(df, year_columns, variable_columns)

        df_unpivot = self._seperate_and_rename_categories(df_unpivot, variable_columns)

        df_unpivot = self._cast_numeric_fields(df_unpivot)        

        df_unpivot = df_unpivot.dropna()

        return df_unpivot
    
    def filter_region(self, country_code: str = 'PT') -> DataFrame:
        self.filtered_df = self.clean_df[self.clean_df['region'] == country_code.upper()]

        self.filtered_df = self.filtered_df.reset_index(drop=True)

        return self.filtered_df    