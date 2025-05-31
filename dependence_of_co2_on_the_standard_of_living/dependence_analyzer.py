import pandas as pd
from scipy.stats import ttest_ind


class DependenceAnalyzer(object):
    @staticmethod
    def calculate_dependence_statistics(
        df: pd.DataFrame,
        comparer_column: str,
        comparable_column: str,
    ) -> tuple[float, float, float, float, float, float, float, float]:
        """
        Calculates statistical dependence between two specified columns.

        This method computes medians for the comparer and comparable columns,
        divides the data into two groups based on the median of the comparer
        column, and determines median values for the comparable column within
        these groups. Additionally, it calculates the correlation between the
        columns and performs a two-sample t-test to assess statistical
        differences between the high and low comparer groups.

        :param df: DataFrame containing the columns to analyze.
        :param comparer_column: Column in the DataFrame used to create groups
            based on its median.
        :param comparable_column: Column to analyze in relation to the comparer
            column.
        :return: A tuple containing:
            - the median of the comparer column,
            - the median of the comparable column,
            - the median of the comparable column for the high comparer group,
            - the median of the comparable column for the low comparer group,
            - the correlation coefficient between the two columns,
            - the p-value from the two-sample t-test.
            - the difference between the high and low median of comparer group.
            - the percent of difference from the median of comparer group.
        """

        median_comparer = df[comparer_column].median().round(3)
        median_comparable = df[comparable_column].median().round(3)

        group_high_comparer = df[df[comparer_column] > median_comparer].round(3)
        group_low_comparer = df[df[comparer_column] <= median_comparer].round(3)

        median_comparable_high = (
            group_high_comparer[comparable_column].median().round(3)
        )
        median_comparable_low = group_low_comparer[comparable_column].median().round(3)

        correlation = df[comparer_column].corr(df[comparable_column]).round(3)

        group_high = group_high_comparer[comparable_column].dropna()
        group_low = group_low_comparer[comparable_column].dropna()
        t_stat, p_value = ttest_ind(group_high, group_low)
        p_value = p_value.round(3)

        diff = round(abs(median_comparable_high - median_comparable_low), 3)
        diff_percent = round(diff / median_comparable * 100, 3)

        return (
            median_comparer,
            median_comparable,
            median_comparable_high,
            median_comparable_low,
            correlation,
            p_value,
            diff,
            diff_percent,
        )

    @staticmethod
    def save_stats_to_df(
        df: pd.DataFrame,
        comparer_column: str,
        median_comparer: float,
        median_comparable_high: float,
        median_comparable_low: float,
        median_comparable: float,
        corr: float,
        p_value: float,
        diff: float,
        diff_percent: float,
    ):
        """
        Saves statistical information into a given DataFrame. This includes
        details such as median values, differences, correlation, and
        statistical p-value.

        :param df: The DataFrame where the statistics will be saved.
        :param comparer_column: The column name in the DataFrame that represents the comparer.
        :param median_comparer: The median value of the comparer column.
        :param median_comparable_high: The higher median value of the comparable column.
        :param median_comparable_low: The lower median value of the comparable column.
        :param median_comparable: The median of the comparable values.
        :param corr: The correlation coefficient between the comparer and comparable columns.
        :param p_value: The p-value representing the significance of the correlation.
        :param diff: The difference between the high and low comparer groups.
        :param diff_percent: The percent of difference from the median of comparer group.
        """

        df.loc[comparer_column] = {
            "COMPARER_COLUMN": comparer_column,
            "MEDIAN_COMPARER": median_comparer,
            "MEDIAN_COMPARABLE": median_comparable,
            "MEDIAN_COMPARABLE_HIGHER": median_comparable_high,
            "MEDIAN_COMPARABLE_LOWER": median_comparable_low,
            "DIFFERENCE": diff,
            "DIFFERENCE_PERCENT": diff_percent,
            "CORRELATION": corr,
            "P_VALUE": p_value,
        }

    def calculate_dependence_by_column(
        self,
        df: pd.DataFrame,
        df_result: pd.DataFrame,
        comparer_column: str,
        comparable_column: str,
        year: str = "",
        only_year: bool = False,
    ):
        """
        Calculate dependence statistics between columns in a dataframe and save the
        results into another dataframe.

        :param df: Input dataframe containing the data to analyze.
        :param df_result: Dataframe to store the computed statistics.
        :param comparer_column: Column name in the input dataframe to use as the
            comparer in the statistical analysis.
        :param comparable_column: Column name in the input dataframe used as the
            comparable against the comparer column in the analysis.
        :param year: The year to analyze in the input dataframe.
        :param only_year: If True, only print the year in the input dataframe.
        """

        (
            avg_comparer,
            avg_comparable,
            avg_comparable_high,
            avg_comparable_low,
            corr,
            p_value,
            diff,
            percent,
        ) = self.calculate_dependence_statistics(df, comparer_column, comparable_column)

        self.save_stats_to_df(
            df_result,
            comparer_column + " " + year if not only_year else year,
            avg_comparer,
            avg_comparable_high,
            avg_comparable_low,
            avg_comparable,
            corr,
            p_value,
            diff,
            percent,
        )
