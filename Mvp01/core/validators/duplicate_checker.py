# core/validators/duplicate_checker.py
import pandas as pd
from core.validators.status_calculator import calculate_status
from core.ports.validator_port import DatasetCheckResult


class DuplicateChecker:
    name = "duplicates"
    GREEN_THRESHOLD = 5.0
    YELLOW_THRESHOLD = 10.0

    def check(self, df: pd.DataFrame) -> DatasetCheckResult:
        total_rows = len(df)
        total_duplicates = int(df.duplicated().sum())
        percentage = (total_duplicates / total_rows) * 100 if total_rows > 0 else 0.0
        status = calculate_status(percentage, self.GREEN_THRESHOLD, self.YELLOW_THRESHOLD)

        return DatasetCheckResult(
            count=total_duplicates,
            percentage=round(percentage, 2),
            status=status
        )