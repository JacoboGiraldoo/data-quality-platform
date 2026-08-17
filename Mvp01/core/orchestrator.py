import pandas as pd
from core.ports.validator_port import (
    ColumnValidatorPort,
    DatasetValidatorPort,
    AnalysisReport,
)


class Orchestrator:
    def __init__(
        self,
        column_validators: list[ColumnValidatorPort],
        dataset_validators: list[DatasetValidatorPort],
    ):
        self.column_validators = column_validators
        self.dataset_validators = dataset_validators

    def run(self, df: pd.DataFrame) -> AnalysisReport:
        column_checks = {}
        for validator in self.column_validators:
            column_checks[validator.name] = validator.check(df)

        dataset_checks = {}
        for validator in self.dataset_validators:
            dataset_checks[validator.name] = validator.check(df)

        return AnalysisReport(
            column_checks=column_checks,
            dataset_checks=dataset_checks,
        )