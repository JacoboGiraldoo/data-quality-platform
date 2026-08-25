from core.ports.validator_port import (
    AnalysisReport,
    ColumnCheckResult,
    DatasetCheckResult,
)
from core.recommendations.recommendation_engine import Recommendation
from core.exports.pdf_report_exporter import PDFReportExporter

exporter = PDFReportExporter()


# Case 1 + 2: a report with multiple recommendations generates valid,
# well-formed PDF bytes without raising (regression test for the
# multi_cell/ln() bug found today).
def test_generates_valid_pdf_with_multiple_recommendations():
    report = AnalysisReport(
        column_checks={
            "nulls": {
                "a": ColumnCheckResult(count=5, percentage=15.0, status="red", metadata={}),
            }
        },
        dataset_checks={},
        analyses={},
    )
    recommendations = [
        Recommendation(severity="red", column="a", message="First issue found."),
        Recommendation(severity="yellow", column="a", message="Second issue found."),
    ]

    pdf_bytes = exporter.generate(report, recommendations)

    assert pdf_bytes[:5] == b"%PDF-"


# Case 3: an extremely long column name does not raise (regression test
# for the _fit_text overflow bug found today). We can't assert it "looks
# right" — only that it doesn't crash.
def test_extremely_long_column_name_does_not_raise():
    report = AnalysisReport(
        column_checks={
            "nulls": {
                "a" * 200: ColumnCheckResult(count=1, percentage=1.0, status="green", metadata={}),
            }
        },
        dataset_checks={},
        analyses={},
    )

    exporter.generate(report, [])


# Case 4: a report with zero recommendations does not raise, and exercises
# the "No issues found" branch.
def test_no_recommendations_does_not_raise():
    report = AnalysisReport(
        column_checks={
            "nulls": {
                "a": ColumnCheckResult(count=0, percentage=0.0, status="green", metadata={}),
            }
        },
        dataset_checks={},
        analyses={},
    )

    exporter.generate(report, [])


# Case 5: a dataset-level check (not per-column) does not raise. This
# exercises the separate _draw_dataset_row path.
def test_dataset_level_check_does_not_raise():
    report = AnalysisReport(
        column_checks={},
        dataset_checks={
            "duplicates": DatasetCheckResult(count=50, percentage=12.5, status="red"),
        },
        analyses={},
    )

    exporter.generate(report, [])