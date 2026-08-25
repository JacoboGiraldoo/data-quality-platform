from core.ports.validator_port import (
    AnalysisReport,
    ColumnCheckResult,
    DatasetCheckResult,
)
from core.recommendations.recommendation_engine import RecommendationEngine

engine = RecommendationEngine()


# Case 1: red status with an existing template generates a recommendation
def test_red_status_generates_recommendation():
    report = AnalysisReport(
        column_checks={
            "types": {
                "price": ColumnCheckResult(count=100, percentage=29.13, status="red", metadata={}),
            }
        },
        dataset_checks={},
        analyses={},
    )

    recommendations = engine.generate(report)

    assert len(recommendations) == 1
    assert recommendations[0].severity == "red"
    assert recommendations[0].column == "price"
    assert "29.13%" in recommendations[0].message


# Case 2: yellow status with an existing template generates a recommendation
def test_yellow_status_generates_recommendation():
    report = AnalysisReport(
        column_checks={
            "outliers": {
                "amount": ColumnCheckResult(count=10, percentage=9.15, status="yellow", metadata={}),
            }
        },
        dataset_checks={},
        analyses={},
    )

    recommendations = engine.generate(report)

    assert len(recommendations) == 1
    assert recommendations[0].severity == "yellow"


# Case 3: green status never generates a recommendation, regardless of checker
def test_green_status_generates_nothing():
    report = AnalysisReport(
        column_checks={
            "nulls": {
                "clean_column": ColumnCheckResult(count=0, percentage=0.0, status="green", metadata={}),
            }
        },
        dataset_checks={},
        analyses={},
    )

    recommendations = engine.generate(report)

    assert recommendations == []


# Case 4: a (checker, status) combination with no template is skipped silently,
# not raised as an error. This is what would have hidden the missing
# ("types", "yellow") template if we hadn't caught it during design.
def test_missing_template_combination_is_skipped():
    report = AnalysisReport(
        column_checks={
            "descriptive_stats": {
                "some_column": ColumnCheckResult(count=1, percentage=1.0, status="red", metadata={}),
            }
        },
        dataset_checks={},
        analyses={},
    )

    recommendations = engine.generate(report)

    assert recommendations == []


# Case 5: dataset-level checks (not per-column) produce a recommendation
# with column=None, coming from the second loop in generate().
def test_dataset_level_check_has_no_column():
    report = AnalysisReport(
        column_checks={},
        dataset_checks={
            "duplicates": DatasetCheckResult(count=50, percentage=12.5, status="red"),
        },
        analyses={},
    )

    recommendations = engine.generate(report)

    assert len(recommendations) == 1
    assert recommendations[0].column is None
    assert "12.5%" in recommendations[0].message


# Case 6: a fully healthy report (everything green) returns an empty list
# without errors.
def test_fully_healthy_report_returns_empty_list():
    report = AnalysisReport(
        column_checks={
            "nulls": {
                "a": ColumnCheckResult(count=0, percentage=0.0, status="green", metadata={}),
            },
            "outliers": {
                "a": ColumnCheckResult(count=0, percentage=0.0, status="green", metadata={}),
            },
        },
        dataset_checks={
            "duplicates": DatasetCheckResult(count=0, percentage=0.0, status="green"),
        },
        analyses={},
    )

    recommendations = engine.generate(report)

    assert recommendations == []


# Case 7: multiple findings across columns and dataset checks all
# accumulate into the same list, not just the first one found.
def test_multiple_findings_all_accumulate():
    report = AnalysisReport(
        column_checks={
            "nulls": {
                "a": ColumnCheckResult(count=5, percentage=15.0, status="red", metadata={}),
            },
            "outliers": {
                "b": ColumnCheckResult(count=3, percentage=9.0, status="yellow", metadata={}),
            },
        },
        dataset_checks={
            "duplicates": DatasetCheckResult(count=2, percentage=2.0, status="yellow"),
        },
        analyses={},
    )

    recommendations = engine.generate(report)

    assert len(recommendations) == 3