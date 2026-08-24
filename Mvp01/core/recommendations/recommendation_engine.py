from dataclasses import dataclass
from typing import Callable

from core.ports.validator_port import AnalysisReport


@dataclass
class Recommendation:
    severity: str
    column: str | None
    message: str


# Fixed templates per (checker_name, status). No template exists for
# "green" statuses on purpose: a healthy column has nothing to recommend.
TEMPLATES: dict[tuple[str, str], Callable[[float], str]] = {
    ("nulls", "red"): lambda pct: f"{pct}% of values are missing. Consider imputing or dropping this column before training.",
    ("nulls", "yellow"): lambda pct: f"{pct}% of values are missing. Review whether imputation is appropriate.",
    ("outliers", "red"): lambda pct: f"{pct}% of values are extreme outliers. Consider investigating the IQR-flagged rows.",
    ("outliers", "yellow"): lambda pct: f"{pct}% of values are flagged as outliers. Worth a quick visual check before trusting the distribution.",
    ("types", "red"): lambda pct: f"{pct}% of values don't match the expected type. Validate the source data or adjust the schema.",
    ("duplicates", "red"): lambda pct: f"{pct}% of rows are duplicates. Consider deduplicating before analysis.",
    ("duplicates", "yellow"): lambda pct: f"{pct}% of rows are duplicates. Review whether they're intentional.",
}


class RecommendationEngine:
    name = "recommendation_engine"

    def generate(self, report: AnalysisReport) -> list[Recommendation]:
        recommendations = []

        for checker_name, columns in report.column_checks.items():
            for column_name, result in columns.items():
                if result.status == "green":
                    continue

                template = TEMPLATES.get((checker_name, result.status))
                if template is None:
                    continue

                recommendations.append(
                    Recommendation(
                        severity=result.status,
                        column=column_name,
                        message=template(result.percentage),
                    )
                )

        for checker_name, result in report.dataset_checks.items():
            if result.status == "green":
                continue

            template = TEMPLATES.get((checker_name, result.status))
            if template is None:
                continue

            recommendations.append(
                Recommendation(
                    severity=result.status,
                    column=None,
                    message=template(result.percentage),
                )
            )

        return recommendations