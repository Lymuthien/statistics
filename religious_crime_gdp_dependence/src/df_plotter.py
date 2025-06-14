import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


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
