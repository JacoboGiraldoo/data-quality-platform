import pandas as pd
from core.orchestrator import Orchestrator
from core.validators.null_checker import NullChecker
from core.validators.outlier_checker import OutlierChecker
from core.validators.type_checker import TypeChecker
from core.validators.duplicate_checker import DuplicateChecker
from core.validators.descriptive_stats_analyzer import DescriptiveStatsAnalyzer


df = pd.DataFrame({
    "edad": [25, 30, None, 40, 999],
    "nombre": ["Ana", "Luis", "Ana", "Carlos", "125"],
})

orchestrator = Orchestrator(
    column_validators=[NullChecker(), OutlierChecker(), TypeChecker()],
    dataset_validators=[DuplicateChecker()],
    analyzers=[DescriptiveStatsAnalyzer()]
)

report = orchestrator.run(df)

for check_name, results in report.column_checks.items():
    print(f"\n{check_name}:")
    for column, result in results.items():
        print(f"  {column}: count={result.count}, status={result.status}")

for check_name, result in report.dataset_checks.items():
    print(f"\n{check_name}: count={result.count}, status={result.status}")


for name, results in report.analyses.items():
    print(f"\n{name}:")
    for column, stats in results.items():
        print(f"  {column}: {stats}")