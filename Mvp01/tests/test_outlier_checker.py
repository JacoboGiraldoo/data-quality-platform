# mvp01/tests/test_outlier_checker.py
import pandas as pd
from core.validators.outlier_checker import OutlierChecker


def test_no_outliers():
    df = pd.DataFrame({
        "edad": [20, 22, 25, 27, 30, 32, 35, 38]
    })

    checker = OutlierChecker()
    result = checker.check(df)

    assert result["edad"].count == 0
    assert result["edad"].status == "green"


def test_with_clear_outlier():
    df = pd.DataFrame({
        "edad": [20, 22, 25, 27, 30, 32, 35, 500]
    })

    checker = OutlierChecker()
    result = checker.check(df)

    assert result["edad"].count == 1
    assert result["edad"].status in ("yellow", "red")  # 1/8 = 12.5%


def test_non_numeric_column_is_skipped():
    df = pd.DataFrame({
        "nombre": ["Ana", "Luis", "Carlos"],
        "edad": [20, 25, 30]
    })

    checker = OutlierChecker()
    result = checker.check(df)

    assert "nombre" not in result
    assert "edad" in result


def test_mixed_numeric_and_text_with_outlier():
    df = pd.DataFrame({
        "nombre": ["Ana", "Luis", "Carlos", "Marta"],
        "precio": [10, 12, 11, 1000]
    })

    checker = OutlierChecker()
    result = checker.check(df)

    assert "nombre" not in result
    assert result["precio"].count == 1


def test_empty_dataframe():
    df = pd.DataFrame({
        "edad": []
    })

    checker = OutlierChecker()
    result = checker.check(df)

    assert result["edad"].count == 0
    assert result["edad"].percentage == 0
    assert result["edad"].status == "green"