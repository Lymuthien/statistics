from pathlib import Path

import pandas as pd

from .df_model import DfDependenceFactory
from .df_plotter import DfDependencePlotter
from .statistics_calculator import StatisticsCalculator
from .cleaning import DataCleaner
from .feature_engineering import FeatureEngineer


class Pipelane(object):
    def __init__(self, directory: Path):
        self._dir: Path = directory
        self._cleaner = DataCleaner()
        self._engineer = FeatureEngineer()
        self._stats = StatisticsCalculator()
        self._df_factory = DfDependenceFactory()
        self._plotter = DfDependencePlotter()
        self._dependence_dfs = {
            "COL": self._df_factory.create_df(),
            "time_in_road": self._df_factory.create_df(),
        }

    def _get_merged_df(self, year: int) -> pd.DataFrame | None:
        col_df, pollution_df, traffic_df = self._read_df(year)

        merged_df = pd.merge(
            pd.merge(pollution_df, col_df, on="City"), traffic_df, on="City"
        )
        merged_df["Year"] = year

        return merged_df

    def _read_df(self, year):
        col_df = pd.read_csv(
            self._dir / "cost_of_living" / f"cost_of_living_{year}.csv", sep=";"
        )
        pollution_df = pd.read_csv(
            self._dir / "pollution" / f"pollution_{year}.csv", sep=";"
        )
        traffic_df = pd.read_csv(self._dir / "traffic" / f"traffic_{year}.csv", sep=";")

        return col_df, pollution_df, traffic_df

    def _plot_correlation(self):
        for k, df in self._dependence_dfs.items():
            self._plotter.plot_correlation_over_years(
                df, f"Pollution-{k} Correlation", "YEAR", "CORRELATION"
            )

    def _save_dependence_df(self):
        for k, df in self._dependence_dfs.items():
            df.to_csv(
                self._dir / "processed" / f"pollution_{k}_dependence.csv", index=False
            )

    def process_year(self, year: int):
        df = self._get_merged_df(year)
        df = self._cleaner.clean(df)
        df = self._engineer.add_features(df)

        for dep_df, col in zip(
            self._dependence_dfs.values(),
            ["Local Purchasing Power Index", "Time Index"],
        ):
            stats = self._stats.calculate_dependence_statistics(
                df, col, "Pollution Index", str(year)
            )
            dep_df.loc[len(dep_df)] = stats

        return df

    def _process_over_years(self, min_year, max_year):
        all_data = []

        for year in range(min_year, max_year + 1):
            try:
                df = self.process_year(year)
                all_data.append(df)

                # if year == self._max_year or year == self._min_year or year % 5 == 0:
                #     for comparer_column in (
                #         "Local Purchasing Power Index",
                #         "Time Index",
                #     ):
                #         self._plotter.plot_dependence(
                #             df=df,
                #             comparer_column=comparer_column,
                #             comparable_column="Pollution Index",
                #             year=str(year),
                #         )
            except Exception as e:
                print(f"Year {year} skipped due to error: {e}")
                continue

        final_df = pd.concat(all_data)
        final_df.to_csv(self._dir / "processed" / "all_data_cleaned.csv", index=False)

    def run(self, min_year: int = 2012, max_year: int = 2025):
        self._process_over_years(min_year, max_year)
        self._save_dependence_df()
        self._plot_correlation()
