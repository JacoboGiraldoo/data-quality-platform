from fastapi.testclient import TestClient
from api.main import app

from pathlib import Path
FIXTURES = Path(__file__).parent / "fixtures"

client = TestClient(app)


# Case 1: invalid extension (.pdf instead of .csv)
def test_invalid_extension_returns_422():
    with open(FIXTURES / "invalid_extension.pdf", "rb") as f:
        response = client.post(
            "/analyze",
            files={"file": ("resume.pdf", f, "application/pdf")},
        )

    assert response.status_code == 422
    assert response.json()["detail"] == "Only .csv files are supported"


# Case 2: file exceeds the 10MB limit
def test_oversized_file_returns_413():
    with open(FIXTURES / "oversized.csv", "rb") as f:
        response = client.post(
            "/analyze",
            files={"file": ("oversized.csv", f, "text/csv")},
        )

    assert response.status_code == 413
    assert response.json()["detail"] == "File exceeds the 10MB limit"


# Case 3: .csv extension but the content is not a parseable CSV
def test_unparseable_content_returns_422():
    with open(FIXTURES / "unparseable.csv", "rb") as f:
        response = client.post(
            "/analyze",
            files={"file": ("unparseable.csv", f, "text/csv")},
        )

    assert response.status_code == 422
    assert response.json()["detail"] == "The file could not be parsed as a valid CSV"


# Case 4: valid CSV but with no data rows (header only)
def test_empty_csv_returns_400():
    with open(FIXTURES / "empty_data.csv", "rb") as f:
        response = client.post(
            "/analyze",
            files={"file": ("empty_data.csv", f, "text/csv")},
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "The CSV file contains no rows"


# Case 5: happy path — real, valid CSV with data
def test_valid_csv_returns_200_with_expected_shape():
    with open(FIXTURES / "valid_data.csv", "rb") as f:
        response = client.post(
            "/analyze",
            files={"file": ("valid_data.csv", f, "text/csv")},
        )

    assert response.status_code == 200

    body = response.json()
    # We don't compare the full JSON (that would be fragile against
    # any change to the test CSV); we only confirm it has the shape
    # the orchestrator promises to return.
    assert "column_checks" in body
    assert "dataset_checks" in body
    assert "analyses" in body