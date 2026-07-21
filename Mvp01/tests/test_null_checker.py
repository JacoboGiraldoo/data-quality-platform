import pandas as pd
from core.validators.null_checker import NullChecker

#Test no nulls
def test_no_nulls_returns_all_green():
    df = pd.DataFrame({
        "edad": [25, 30, 35],
        "nombre": ["Ana", "Luis", "Carlos"]
    })

    checker = NullChecker()
    result = checker.check(df)

    assert result["edad"].count == 0
    assert result["edad"].status == "green"
    assert result["nombre"].count == 0
    assert result["nombre"].status == "green"


#Test only nulls
def test_only_nulls():
    df = pd.DataFrame({
        "edad": [None, None, None],
        "nombre": [None, None, None]
    })

    checker = NullChecker()
    result = checker.check(df)

    assert result["edad"].percentage == 100
    assert result["edad"].status == "red"
    assert result["nombre"].percentage == 100
    assert result["nombre"].status == "red"


def test_mixed():
    df = pd.DataFrame({
        "edad": [20, 15, 35, 55],
        "nombre": ["juan", "erick", "esteban",None],
        "peso":[None,None,None,None]
    })

    checker = NullChecker()
    result = checker.check(df)

    assert result["edad"].percentage == 0
    assert result["edad"].status == "green"
    

    assert result["nombre"].percentage == 25
    assert result["nombre"].status == "yellow"
    


    assert result["peso"].percentage == 100
    assert result["peso"].status == "red"

def test_null_values():
    df = pd.DataFrame({
        "edad": [],
        "nombre": [],
        "peso":[]
    })

    checker = NullChecker()
    result = checker.check(df)

    assert result["edad"].percentage == 0
    assert result["edad"].status == "green"
    

    assert result["nombre"].percentage == 0
    assert result["nombre"].status == "green"
    


    assert result["peso"].percentage == 0
    assert result["peso"].status == "green"
