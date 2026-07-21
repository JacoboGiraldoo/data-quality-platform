# core/validators/duplicate_checker.py
from dataclasses import dataclass
import pandas as pd
from core.validators.status_calculator import calculate_status


@dataclass
class DuplicateResult:
    total_duplicates: int
    percentage: float
    status: str  # "green", "yellow", "red"


class DuplicateChecker:
    GREEN_THRESHOLD = 5.0
    YELLOW_THRESHOLD = 10.0

    def check(self, df: pd.DataFrame) -> DuplicateResult:
        total_rows = len(df)
        total_duplicates = int(df.duplicated().sum())
        percentage = (total_duplicates / total_rows) * 100 if total_rows > 0 else 0.0
        status = calculate_status(percentage, self.GREEN_THRESHOLD, self.YELLOW_THRESHOLD)

        return DuplicateResult(
            total_duplicates=total_duplicates,
            percentage=round(percentage, 2),
            status=status
        )