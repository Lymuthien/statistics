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
        self._dependence_dfs: dict[str, pd.DataFrame] = {}
        self._min_year = 2012
        self._max_year = 2025

    def _get_merged_df(self, year: int) -> pd.DataFrame | None:
        try:
            col_df, pollution_df, traffic_df = self._read_df(year)
            pol_col_df = pd.merge(pollution_df, col_df, on="City")
            return pd.merge(pol_col_df, traffic_df, on="City")
        except Exception as e:
            print(f"Error reading dataframes {year}: {e}")
            return None

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

    def _create_dependence_df(self):
        self._dependence_dfs["COL"] = self._df_factory.create_df()
        self._dependence_dfs["time_in_road"] = self._df_factory.create_df()

    def _save_dependence_df(self):
        for k, df in self._dependence_dfs.items():
            df.to_csv(self._dir / f"pollution_{k}_dependence.csv")

    def _make_tables(self):
        for year in range(self._min_year, self._max_year + 1):
            merged_df = self._get_merged_df(year)
            if merged_df is None:
                continue

            for df, comparer_column in zip(
                self._dependence_dfs.values(),
                ("Local Purchasing Power Index", "Time Index"),
            ):
                stats = self._statistics_calculator.calculate_dependence_statistics(
                    merged_df, comparer_column, "Pollution Index", str(year)
                )
                df.loc[len(df)] = stats

            if year == self._max_year or year == self._min_year or year % 5 == 0:
                for comparer_column in ("Local Purchasing Power Index", "Time Index"):
                    self._plotter.plot_dependence(
                        df=merged_df,
                        comparer_column=comparer_column,
                        comparable_column="Pollution Index",
                        year=str(year),
                    )

    def run(self):
        self._create_dependence_df()
        self._make_tables()
        self._save_dependence_df()
        self._plot_correlation()
