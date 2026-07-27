import pandas as pd
from dataclasses import dataclass


@dataclass
class NumericColumnStats:
    mean: float
    median: float
    std_dev: float
    min_value: float
    max_value: float


@dataclass
class CategoricalColumnStats:
    unique_count: int
    most_frequent_value: str
    most_frequent_count: int


class DescriptiveStatsAnalyzer:

    def analyze(self, df: pd.DataFrame) -> dict[str, NumericColumnStats | CategoricalColumnStats]:
        results = {}

        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                results[column] = self._analyze_numeric(df[column])
            else:
                results[column] = self._analyze_categorical(df[column])

        return results

    def _analyze_numeric(self, series: pd.Series) -> NumericColumnStats:
        return NumericColumnStats(
            mean= series.mean(),
            median=series.median(),
            std_dev=series.std(),
            min_value=series.min(),
            max_value=series.max()
        )

    def _analyze_categorical(self, series: pd.Series) -> CategoricalColumnStats:
        # pista: series.value_counts() te da, ordenado de mayor a menor,
        # cuántas veces aparece cada valor único
        value_counts = series.value_counts()

        return CategoricalColumnStats(
            unique_count=series.nunique(),
            most_frequent_value=value_counts.index[0],
            most_frequent_count=value_counts.iloc[0]
        )