from cleaning import LifeExpectancyOperations
from pandas import read_csv

# pylint: disable-all

def make_fixture() -> None:
    df = read_csv(
        "./life_expectancy/data/eu_life_expectancy_raw.tsv", sep="\t", header=0
    )

    df_truncated = df[:300]
    df_truncated = df_truncated.loc[:, :"2012"]

    df_truncated.to_csv(
        "./life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv",
        sep="\t",
        index=False,
    )

if __name__ == "__main__":
    df = read_csv(
        "./life_expectancy/data/eu_life_expectancy_raw.tsv", sep="\t", header=0
    )

    cleaningOperations = LifeExpectancyOperations(df)

    cleaned_df = cleaningOperations.clean_df

    print(cleaned_df[["region"]].drop_duplicates())