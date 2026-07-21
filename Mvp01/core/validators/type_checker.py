from dataclasses import dataclass
import pandas as pd
from core.validators.status_calculator import calculate_status


@dataclass
class ColumnTypeResult:
    expected_type: str  # "numeric" o "text"
    count: int
    percentage: float
    status: str


class TypeChecker:
    GREEN_THRESHOLD = 5.0
    YELLOW_THRESHOLD = 10.0
    MAJORITY_THRESHOLD = 0.5

    def check(self, df: pd.DataFrame) -> dict[str, ColumnTypeResult]:
        results = {}
        total_rows = len(df)

        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                continue

            non_null_count = df[column].notna().sum()
            if non_null_count == 0:
                continue

            converted = pd.to_numeric(df[column], errors="coerce")
            numeric_count = converted.notna().sum()
            numeric_ratio = numeric_count / non_null_count

            if numeric_ratio > self.MAJORITY_THRESHOLD:
                expected_type = "numeric"
                inconsistent_count = non_null_count - numeric_count
            else:
                expected_type = "text"
                inconsistent_count = numeric_count

            percentage = (inconsistent_count / total_rows) * 100 if total_rows > 0 else 0.0
            status = calculate_status(percentage, self.GREEN_THRESHOLD, self.YELLOW_THRESHOLD)

            results[column] = ColumnTypeResult(
                expected_type=expected_type,
                count=int(inconsistent_count),
                percentage=round(percentage, 2),
                status=status
            )

        return results