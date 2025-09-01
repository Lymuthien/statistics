import pandas as pd


class DataCleaner:
    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        if "Pollution Index" in df.columns:
            df["Pollution Index"] = df["Pollution Index"].interpolate(method="linear")

        for col in ["Local Purchasing Power Index", "Time Index"]:
            if col in df.columns:
                df[col] = df.groupby("City")[col].transform(
                    lambda x: x.fillna(x.median())
                )

        return df

    @staticmethod
    def remove_outliers(df: pd.DataFrame, column: str) -> pd.DataFrame:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1

        return df[(df[column] >= q1 - 1.5 * iqr) & (df[column] <= q3 + 1.5 * iqr)]

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.handle_missing_values(df)
        for col in ["Pollution Index", "Local Purchasing Power Index", "Time Index"]:
            if col in df.columns:
                df = self.remove_outliers(df, col)

        return df
