import numpy as np
import pandas as pd


class FeatureEngineer:
    def add_features(self, df: pd.DataFrame) -> pd.DataFrame:
        if "Pollution Index" in df.columns:
            df["Log Pollution"] = df["Pollution Index"].apply(
                lambda x: 0 if x <= 0 else np.log(x)
            )

        if "Time Index" in df.columns and "Pollution Index" in df.columns:
            df["Pollution per Minute"] = df["Pollution Index"] / df["Time Index"]

        if "Local Purchasing Power Index" in df.columns:
            df["Purchasing Power Category"] = pd.qcut(
                df["Local Purchasing Power Index"],
                q=3,
                labels=["Low", "Medium", "High"],
            )
        return df
