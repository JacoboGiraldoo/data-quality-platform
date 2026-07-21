# mvp01/tests/test_type_checker.py
import pandas as pd
from core.validators.type_checker import TypeChecker


def test_pure_numeric_column_is_skipped():
    df = pd.DataFrame({
        "edad": [25, 30, 35, 40]
    })

    checker = TypeChecker()
    result = checker.check(df)

    assert "edad" not in result


def test_mostly_numeric_with_text_inconsistency():
    df = pd.DataFrame({
        "edad": [25, 30, "treinta y cinco", 40, 45]
    })

    checker = TypeChecker()
    result = checker.check(df)

    assert result["edad"].expected_type == "numeric"
    assert result["edad"].count == 1
    assert result["edad"].status == "red"  # 1/5 = 20%... verifica este número


def test_mostly_text_with_numeric_inconsistency():
    df = pd.DataFrame({
        "nombre": ["Ana", "Luis", "Carlos", "125"]
    })

    checker = TypeChecker()
    result = checker.check(df)

    assert result["nombre"].expected_type == "text"
    assert result["nombre"].count == 1


def test_all_null_column_is_skipped():
    df = pd.DataFrame({
        "columna_vacia": [None, None, None]
    })

    checker = TypeChecker()
    result = checker.check(df)

    assert "columna_vacia" not in result


def test_empty_dataframe():
    df = pd.DataFrame({
        "edad": []
    })

    checker = TypeChecker()
    result = checker.check(df)

    assert "edad" not in result  # 0 filas → non_null_count es 0 → se salta