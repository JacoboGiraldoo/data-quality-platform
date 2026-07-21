from dataclasses import dataclass
import pandas as pd
from core.validators.status_calculator import calculate_status


@dataclass
class ColumnOutlierResult:
    count: int
    percentage: float
    status: str  # "green", "yellow", "red"


class OutlierChecker:
    GREEN_THRESHOLD = 5.0
    YELLOW_THRESHOLD = 10.0
    IQR_MULTIPLIER = 1.5

    def check(self, df: pd.DataFrame) -> dict[str, ColumnOutlierResult]:
        results = {}
        total_rows = len(df)

        for column in df.columns:
            if not pd.api.types.is_numeric_dtype(df[column]):
                continue

            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1

            lower_limit = q1 - self.IQR_MULTIPLIER * iqr
            upper_limit = q3 + self.IQR_MULTIPLIER * iqr

            outlier_count = ((df[column] < lower_limit) | (df[column] > upper_limit)).sum()

            percentage = (outlier_count / total_rows) * 100 if total_rows > 0 else 0.0
            status = calculate_status(percentage, self.GREEN_THRESHOLD, self.YELLOW_THRESHOLD)

            results[column] = ColumnOutlierResult(
                count=int(outlier_count),
                percentage=round(percentage, 2),
                status=status
            )

        return results