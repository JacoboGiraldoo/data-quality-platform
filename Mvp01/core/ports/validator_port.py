from typing import Protocol, Any
from dataclasses import dataclass, field
import pandas as pd


@dataclass
class ColumnCheckResult:
    count: int
    percentage: float
    status: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DatasetCheckResult:
    count: int
    percentage: float
    status: str


class ColumnValidatorPort(Protocol):
    name: str

    def check(self, df: pd.DataFrame) -> dict[str, ColumnCheckResult]: ...


class DatasetValidatorPort(Protocol):
    name: str

    def check(self, df: pd.DataFrame) -> DatasetCheckResult: ...