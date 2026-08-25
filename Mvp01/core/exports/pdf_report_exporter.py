from fpdf import FPDF

from core.ports.validator_port import AnalysisReport
from core.recommendations.recommendation_engine import Recommendation

STATUS_COLORS = {
    "green": (76, 175, 80),
    "yellow": (255, 193, 7),
    "red": (244, 67, 54),
}

COL_WIDTHS = {
    "name": 70,
    "count": 30,
    "percentage": 30,
    "status": 15,
}


class PDFReportExporter:
    name = "pdf_report_exporter"

    def generate(self, report: AnalysisReport, recommendations: list[Recommendation]) -> bytes:
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, "Data Quality Report", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

        for checker_name, columns in report.column_checks.items():
            self._draw_column_table(pdf, checker_name, columns)

        for checker_name, result in report.dataset_checks.items():
            self._draw_dataset_row(pdf, checker_name, result)

        self._draw_recommendations(pdf, recommendations)

        return bytes(pdf.output())

    def _draw_table_header(self, pdf: FPDF, first_column_label: str) -> None:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(COL_WIDTHS["name"], 8, first_column_label, border=1)
        pdf.cell(COL_WIDTHS["count"], 8, "Count", border=1)
        pdf.cell(COL_WIDTHS["percentage"], 8, "Percentage", border=1)
        pdf.cell(COL_WIDTHS["status"], 8, "Status", border=1)
        pdf.ln()

    def _draw_status_cell(self, pdf: FPDF, status: str) -> None:
        pdf.set_fill_color(*STATUS_COLORS[status])
        pdf.cell(COL_WIDTHS["status"], 8, "", border=1, fill=True)

    def _fit_text(self, pdf: FPDF, text: str, max_width: float) -> str:
        if pdf.get_string_width(text) <= max_width:
            return text
        while text and pdf.get_string_width(text + "...") > max_width:
            text = text[:-1]
        return text + "..."

    def _draw_column_table(self, pdf: FPDF, checker_name: str, columns: dict) -> None:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, checker_name.capitalize(), new_x="LMARGIN", new_y="NEXT")

        self._draw_table_header(pdf, "Column")

        pdf.set_font("Helvetica", "", 10)
        for column_name, result in columns.items():
            display_name = self._fit_text(pdf, column_name, COL_WIDTHS["name"] - 2)
            pdf.cell(COL_WIDTHS["name"], 8, display_name, border=1)
            pdf.cell(COL_WIDTHS["count"], 8, str(result.count), border=1)
            pdf.cell(COL_WIDTHS["percentage"], 8, f"{result.percentage}%", border=1)
            self._draw_status_cell(pdf, result.status)
            pdf.ln()

        pdf.ln(4)

    def _draw_dataset_row(self, pdf: FPDF, checker_name: str, result) -> None:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, checker_name.capitalize(), new_x="LMARGIN", new_y="NEXT")

        self._draw_table_header(pdf, "Dataset")

        pdf.set_font("Helvetica", "", 10)
        pdf.cell(COL_WIDTHS["name"], 8, "(entire dataset)", border=1)
        pdf.cell(COL_WIDTHS["count"], 8, str(result.count), border=1)
        pdf.cell(COL_WIDTHS["percentage"], 8, f"{result.percentage}%", border=1)
        self._draw_status_cell(pdf, result.status)
        pdf.ln()

        pdf.ln(4)

    def _draw_recommendations(self, pdf: FPDF, recommendations: list[Recommendation]) -> None:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 12, "Recommendations", new_x="LMARGIN", new_y="NEXT")

        if not recommendations:
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 8, "No issues found. All checks passed.", new_x="LMARGIN", new_y="NEXT")
            return

        pdf.set_font("Helvetica", "", 10)
        for rec in recommendations:
            self._draw_status_cell(pdf, rec.severity)
            label = f" [{rec.column}] " if rec.column else " "
            pdf.multi_cell(0, 8, f"{label}{rec.message}")
            pdf.ln(2)