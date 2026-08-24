import io

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile

from core.orchestrator import Orchestrator
from core.validators.null_checker import NullChecker
from core.validators.outlier_checker import OutlierChecker
from core.validators.type_checker import TypeChecker
from core.validators.duplicate_checker import DuplicateChecker
from core.validators.descriptive_stats_analyzer import DescriptiveStatsAnalyzer

app = FastAPI(title="Data Quality Platform")

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


@app.get("/health")
def health():
    return {"status": "ok"}

##/Analyze 
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Validations are ordered from cheapest to most expensive:
    # checking a filename costs nothing, parsing a CSV does.

    # 1. Filename check — rejects obvious non-CSV uploads early.
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=422,
            detail="Only .csv files are supported",
        )

    # Reads the uploaded file as raw bytes (no file exists on disk).
    contents = await file.read()

    # 2. Size check — protects the server from running out of memory.
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the {MAX_FILE_SIZE_MB}MB limit",
        )

    # 3. Parse check — BytesIO wraps the raw bytes in a file-like
    # object so pandas can read them without touching the disk.
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="The file could not be parsed as a valid CSV",
        )

    # 4. Content check — a header-only CSV would break the checkers
    # (division by zero when computing percentages).
    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="The CSV file contains no rows",
        )

    # Dependencies are injected here, in the adapter layer.
    # The domain never decides which validators to run.
    orchestrator = Orchestrator(
        column_validators=[NullChecker(), OutlierChecker(), TypeChecker()],
        dataset_validators=[DuplicateChecker()],
        analyzers=[DescriptiveStatsAnalyzer()],
    )

    return orchestrator.run(df)