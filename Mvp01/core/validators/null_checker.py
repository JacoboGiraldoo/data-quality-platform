from dataclasses import dataclass
import pandas as pd


@dataclass
class ColumnNullResult:
    count: int
    percentage: float
    status: str  # "green", "yellow", "red"


class NullChecker:
    GREEN_THRESHOLD = 10.0
    YELLOW_THRESHOLD = 25.0

    def check(self, df: pd.DataFrame) -> dict[str, ColumnNullResult]:
        results = {}
        total_rows = len(df)

        for column in df.columns:
            null_count = int(df[column].isnull().sum())
            percentage = (null_count / total_rows) * 100 if total_rows > 0 else 0.0
            status = self._get_status(percentage)

            results[column] = ColumnNullResult(
                count=null_count,
                percentage=round(percentage, 2),
                status=status
            )

        return results

    def _get_status(self, percentage: float) -> str:
        if percentage <= self.GREEN_THRESHOLD:
            return "green"
        elif percentage <= self.YELLOW_THRESHOLD:
            return "yellow"
        return "red"