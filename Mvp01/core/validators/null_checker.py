import pandas as pd
from core.validators.status_calculator import calculate_status
from core.ports.validator_port import ColumnCheckResult




class NullChecker:
    name = 'nulls'
    GREEN_THRESHOLD = 10.0
    YELLOW_THRESHOLD = 25.0

    def check(self, df: pd.DataFrame) -> dict[str, ColumnCheckResult]:
        results = {}
        total_rows = len(df)

        for column in df.columns:
            null_count = int(df[column].isnull().sum())
            percentage = (null_count / total_rows) * 100 if total_rows > 0 else 0.0
            status = calculate_status(percentage, self.GREEN_THRESHOLD, self.YELLOW_THRESHOLD)

            results[column] = ColumnCheckResult(
                count=null_count,
                percentage=round(percentage, 2),
                status=status
            )

        return results