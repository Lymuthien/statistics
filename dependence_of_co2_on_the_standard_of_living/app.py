from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from dependence_analyzer import DependenceAnalyzer


class DfDependencePlotter(object):
    @staticmethod
    def plot_dependence(
        df: pd.DataFrame, comparer_column: str, comparable_column: str, year: str
    ):
        """
        Generate a plot with regression line to visualize the relationship
        between two specified columns of a DataFrame.

        :param df: A pandas DataFrame containing the data to plot.
        :param comparer_column: The name of the column to use for the x-axis
            of the scatter plot.
        :param comparable_column: The name of the column to use for the y-axis
            of the scatter plot.
        :param year: The year that the dependence plot will be plotted on.
        """

        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=comparer_column, y=comparable_column, data=df)
        sns.regplot(
            x=comparer_column, y=comparable_column, data=df, scatter=False, color="red"
        )
        plt.title(f"{comparer_column} vs {comparable_column}: {year}")
        plt.show()

    @staticmethod
    def plot_correlation_over_years(
        dependence_df: pd.DataFrame,
        title: str,
        comparer_name: str,
        correlation_name: str,
    ):
        """
        Generate and display or save a plot of correlation coefficients over years.

        This static method takes a DataFrame containing yearly correlation data
        and produces a line plot of the correlation coefficients. A horizontal
        line at zero is also added to visually separate positive and negative
        correlations. The plot can either be displayed interactively or saved
        to a file, depending on whether an output path is specified.

        :param dependence_df: A pandas DataFrame containing `COMPARER_COLUMN` and
            `CORRELATION` columns which represent the years and their
            corresponding correlation coefficients.
        :param title: Title of the plot, representing the context or purpose of the
            correlation data.
        :param comparer_name: The name of the comparer column to use for.
        :param correlation_name: The name of the correlation column.
        :return: None
        """
        if comparer_name not in dependence_df or correlation_name not in dependence_df:
            raise ValueError

        plt.figure(figsize=(10, 6))
        plt.plot(
            dependence_df[comparer_name],
            dependence_df[correlation_name],
            marker="o",
            label="Correlation",
        )
        plt.axhline(0, color="grey", linestyle="--", linewidth=1)
        plt.title(title)
        plt.xlabel("Year")
        plt.ylabel("Correlation Coefficient")
        plt.grid(True)
        plt.legend()

        plt.show()


class DfDependenceFactory(object):
    def __init__(self):
        self.columns = (
            "COMPARER_COLUMN",
            "MEDIAN_COMPARER",
            "MEDIAN_COMPARABLE",
            "MEDIAN_COMPARABLE_HIGHER",
            "MEDIAN_COMPARABLE_LOWER",
            "DIFFERENCE",
            "DIFFERENCE_PERCENT",
            "CORRELATION",
            "P_VALUE",
        )

    def create_df(self):
        return pd.DataFrame(columns=self.columns)


class App(object):
    def __init__(self, directory: Path):
        self._dir: Path = directory
        self._analyzer = DependenceAnalyzer()
        self._plotter = DfDependencePlotter()
        self._df_factory = DfDependenceFactory()
        self._dependence_dfs: dict[str, pd.DataFrame] = {}
        self._min_year = 2012
        self._max_year = 2025

    def _get_merged_df(self, year: int) -> pd.DataFrame | None:
        try:
            col_df = pd.read_csv(
                self._dir / "cost_of_living" / f"cost_of_living_{year}.csv", sep=";"
            )
            pollution_df = pd.read_csv(
                self._dir / "pollution" / f"pollution_{year}.csv", sep=";"
            )
            traffic_df = pd.read_csv(
                self._dir / "traffic" / f"traffic_{year}.csv", sep=";"
            )
            pol_col_df = pd.merge(pollution_df, col_df, on="City")
            pol_traffic_col_df = pd.merge(pol_col_df, traffic_df, on="City")

            return pol_traffic_col_df
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
                df, f"Pollution-{k} Correlation", "COMPARER_COLUMN", "CORRELATION"
            )

    def _create_dependence_df(self):
        self._dependence_dfs["COL"] = self._df_factory.create_df()
        self._dependence_dfs["time_in_road"] = self._df_factory.create_df()

    def _save_dependence_df(self):
        for k, df in self._dependence_dfs.items():
            df.to_csv(self._dir / f"pollution_{k}_dependence.csv")

    def _make_tables(self):
        for year in range(self._min_year, self._max_year + 1):
            merged_dfs = self._get_merged_df(year)
            if not merged_dfs:
                continue

            for df, comparer_column in zip(
                self._dependence_dfs.values(),
                ("Local Purchasing Power Index", "Time Index"),
            ):
                self._analyzer.calculate_dependence_by_column(
                    merged_dfs,
                    df,
                    comparer_column,
                    "Pollution Index",
                    year=str(year),
                    only_year=True,
                )

            if year == self._max_year or year == self._min_year or year % 5 == 0:
                for comparer_column in ("Local Purchasing Power Index", "Time Index"):
                    self._plotter.plot_dependence(
                        df=merged_dfs,
                        comparer_column=comparer_column,
                        comparable_column="Pollution Index",
                        year=str(year),
                    )

    def run(self):
        self._create_dependence_df()
        self._make_tables()
        self._save_dependence_df()
        self._plot_correlation()


if __name__ == "__main__":
    path = Path(__file__).resolve().parent / "data"
    app = App(path)
    app.run()
