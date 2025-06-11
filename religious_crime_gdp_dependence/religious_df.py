import pandas as pd
from pandas import DataFrame
from typing import Generator


class ReligiousDf(object):
    def __init__(self, religion_df: DataFrame):
        self.df = religion_df

    def filter_by_max_religious(self):
        religion_country_df = DataFrame(columns=["Country Name", "Year", "Religion"])

        countries: set[str] = set(self.df["Country Name"])
        for country in countries:
            for row in self._get_max_row_by_value(country):
                if row is not None:
                    religion_country_df.loc[len(religion_country_df)] = {
                        "Country Name": country,
                        "Year": row["Year"],
                        "Religion": row["Religion"],
                    }

        self.df = religion_country_df

    def _get_max_row_by_value(self, country: str) -> Generator[DataFrame, None]:
        if not country.isdigit():
            country_rows: DataFrame = self.df.loc[self.df["Country Name"] == country]

            sex_rows = country_rows[country_rows["Sex"] == "Both Sexes"]
            sex_rows = sex_rows[sex_rows["Religion"] != "Total"]

            for year in range(2006, 2025):
                rows = sex_rows[sex_rows["Year"] == str(year)]
                if rows.empty:
                    continue
                row: DataFrame = rows.loc[rows["Value"].idxmax()]

                yield row


class GDPDf(object):
    def __init__(self, gdp_df: DataFrame):
        self.df = gdp_df

    def clear_by_year(self):
        gdp_by_year_df = DataFrame(columns=["Country Name", "Year", "GDP"])

        for row in self.df.iterrows():
            for year in range(2015, 2024):
                year = str(year)
                if pd.isna(row[1]["Country Name"]) or pd.isna(row[1][year]):
                    continue
                gdp_by_year_df.loc[len(gdp_by_year_df)] = {
                    "Country Name": row[1]["Country Name"],
                    "Year": year,
                    "GDP": row[1][year],
                }

        self.df = gdp_by_year_df
