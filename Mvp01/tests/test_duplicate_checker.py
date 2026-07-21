# mvp01/tests/test_duplicate_checker.py
import pandas as pd
from core.validators import duplicate_checker
from core.validators.duplicate_checker import DuplicateChecker


def test_no_duplicates():
    df = pd.DataFrame({
        "nombre": ["Ana", "Luis", "Carlos", "Marta"],
        "edad": [25, 30, 35, 40]
    })

    checker = DuplicateChecker()
    result = checker.check(df)

    assert result.total_duplicates == 0
    assert result.percentage == 0
    assert result.status == "green"


def test_all_duplicates():
    df = pd.DataFrame({
        "nombre": ["Ana", "Ana", "Ana", "Ana"],
        "edad": [25, 25, 25, 25]
    })

    checker = DuplicateChecker()
    result = checker.check(df)

    assert result.total_duplicates == 3
    assert result.percentage == 75.0
    assert result.status == "red"


def test_mixed_duplicates():
    df = pd.DataFrame({
        "nombre": ["Ana", "Luis", "Ana", "Carlos", "Marta", "Pedro", "Sofia", "Diego", "Elena", "Mario"],
        "edad": [25, 30, 25, 40, 45, 50, 55, 60, 65, 70]
    })

    checker = DuplicateChecker()
    result = checker.check(df)

    # 10 filas totales, 1 duplicado ("Ana", 25 se repite una vez) → 10%
    assert result.total_duplicates == 1
    assert result.percentage == 10.0
    assert result.status == "yellow"


def test_empty_dataframe():
    df = pd.DataFrame({
        "nombre": [],
        "edad": []
    })

    checker = DuplicateChecker()
    result = checker.check(df)

    assert result.total_duplicates == 0
    assert result.percentage == 0
    assert result.status == "green"