import pandas as pd
from pandas import DataFrame


class ReligiousTable(object):
    def __init__(self, religion_table: DataFrame):
        self.table = religion_table

    def filter_by_max_religious(self):
        unique_religion_country_table = DataFrame(columns=self.table.columns)

        countries: set[str] = set(self.table["Country Name"])
        for country in countries:
            for row in self._get_max_row_by_value(country):
                if row is not None:
                    unique_religion_country_table = pd.concat(
                        [unique_religion_country_table, row], ignore_index=True
                    )

        self.table = unique_religion_country_table

    def _get_max_row_by_value(self, country: str):
        if not country.isdigit():
            country_rows: DataFrame = self.table.loc[
                self.table["Country Name"] == country
            ]

            for sex in ("Male", "Female", "Both Sexes"):
                sex_rows = country_rows[country_rows["Sex"] == sex]
                if sex_rows.empty:
                    continue

                sex_rows = sex_rows[sex_rows["Religion"] != "Total"]

                for year in range(2006, 2025):
                    rows = sex_rows[sex_rows["Year"] == str(year)]
                    if rows.empty:
                        continue
                    max_row: DataFrame = rows.loc[rows["Value"].idxmax()].to_frame().T
                    yield max_row


if __name__ == "__main__":
    t = pd.read_csv("data/religious.csv", sep=",")
    r = ReligiousTable(t)
    r.filter_by_max_religious()
    r.table.to_csv("data/sorted_religious.csv", index=False)
