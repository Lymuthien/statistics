from pathlib import Path

import pandas as pd

from .df_model import DfDependenceFactory
from .df_plotter import DfDependencePlotter
from .statistics_calculator import StatisticsCalculator


class App(object):
    def __init__(self, directory: Path):
        self._dir: Path = directory
        self._statistics_calculator = StatisticsCalculator()
        self._df_factory = DfDependenceFactory()
        self._plotter = DfDependencePlotter()
        self._new_dfs: dict[str, pd.DataFrame] = {}
        self._min_year = 2015
        self._max_year = 2023

    def _get_merged_df(self) -> pd.DataFrame:
        crime_df, religious_df, gdp_df = self._read_df()
        crime_gdp_df = pd.merge(
            gdp_df, crime_df, on=["Country Name", "Year"], how="inner"
        )
        crime_religious_gdp_df = pd.merge(
            religious_df, crime_gdp_df, on=["Country Name", "Year"], how="inner"
        )
        return crime_religious_gdp_df

    def _read_df(self):
        crime_df = pd.read_csv(self._dir / f"crime.csv", sep=";")
        religious_df = pd.read_csv(self._dir / f"religious.csv", sep=",")
        gdp_df = pd.read_csv(self._dir / f"gdp.csv", sep=",")

        return crime_df, religious_df, gdp_df

    def _plot_correlation(self):
        for k, df in self._new_dfs.items():
            self._plotter.plot_correlation_over_years(
                df, f"GDP-{k} Correlation", "YEAR", "CORRELATION"
            )

    def _create_dependence_df(self):
        self._new_dfs["crime_by_gdp"] = self._df_factory.create_df()
        self._new_dfs["muslim_crime_gdp"] = self._df_factory.create_df()
        self._new_dfs["christian_crime_gdp"] = self._df_factory.create_df()
        # self._new_dfs["catholic_crime_gdp"] = self._df_factory.create_df()

    def _save_dependence_df(self):
        for k, df in self._new_dfs.items():
            df.to_csv(self._dir / f"{k}_dependence.csv")

    def _make_tables(self):
        merged_df = self._get_merged_df()
        dfs = (
            merged_df,
            merged_df[merged_df["Religion"] == "Muslim"],
            # merged_df[merged_df["Religion"] == "Christian"],
            merged_df[
                (merged_df["Religion"] == "Catholic")
                | (merged_df["Religion"] == "Christian")
                | (merged_df["Religion"] == "Orthodox")
                | (merged_df["Religion"] == "Protestant")
                | (merged_df["Religion"] == "Lutheran")
            ],
        )
        years = range(self._min_year, self._max_year + 1)
        comparer_column = "GDP"
        comparable_column = "Crime Index"

        for df, new_df in zip(dfs, self._new_dfs.values()):
            for year in years:
                current_df = df[df["Year"] == year]

                stats = self._statistics_calculator.calculate_dependence_statistics(
                    current_df, comparer_column, comparable_column, str(year)
                )
                new_df.loc[len(new_df)] = stats

                if year == self._max_year or year == self._min_year or year % 5 == 0:
                    self._plotter.plot_dependence(
                        df=current_df,
                        comparer_column=comparer_column,
                        comparable_column=comparable_column,
                        year=str(year),
                    )

    def run(self):
        self._create_dependence_df()
        self._make_tables()
        self._save_dependence_df()
        self._plot_correlation()
