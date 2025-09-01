import pandas as pd
from scipy.stats import mannwhitneyu

from .df_model import StatsRow


class StatisticsCalculator(object):
    @staticmethod
    def calculate_dependence_statistics(
        df: pd.DataFrame,
        comparer_column: str,
        comparable_column: str,
        year: str,
    ) -> StatsRow:
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
        :param year: The year of the stat.
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
        t_stat, p_value = mannwhitneyu(group_high, group_low, alternative="two-sided")
        p_value = p_value.round(3)

        diff = round(abs(median_comparable_high - median_comparable_low), 3)
        diff_percent = round(diff / median_comparable * 100, 3)

        return {
            "YEAR": year,
            "MEDIAN_COMPARER": median_comparer,
            "MEDIAN_COMPARABLE": median_comparable,
            "MEDIAN_COMPARABLE_HIGHER": median_comparable_high,
            "MEDIAN_COMPARABLE_LOWER": median_comparable_low,
            "DIFFERENCE": diff,
            "DIFFERENCE_PERCENT": diff_percent,
            "CORRELATION": correlation,
            "P_VALUE": p_value,
        }
