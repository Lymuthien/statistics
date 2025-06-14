from typing import TypedDict

import pandas as pd


class StatsRow(TypedDict):
    YEAR: str
    MEDIAN_COMPARER: float
    MEDIAN_COMPARABLE: float
    MEDIAN_COMPARABLE_HIGHER: float
    MEDIAN_COMPARABLE_LOWER: float
    DIFFERENCE: float
    DIFFERENCE_PERCENT: float
    CORRELATION: float
    P_VALUE: float


class DfDependenceFactory(object):
    def create_df(self):
        return pd.DataFrame(columns=list(StatsRow.__annotations__.keys()))
