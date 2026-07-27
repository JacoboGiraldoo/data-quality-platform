import pandas as pd
from core.validators.descriptive_stats_analyzer import DescriptiveStatsAnalyzer, NumericColumnStats, CategoricalColumnStats

def test_numeric_column_analysis():
    df = pd.DataFrame({
        "edad": [20, 25, 22, 20, 20, 20, 50, 55, 33, 32, 36, 30, 32]
    })

    analyzer = DescriptiveStatsAnalyzer()        # instancia la clase correcta
    result = analyzer.analyze(df)

    assert result["edad"].min_value == 20   # ¿cuál es el mínimo de esa lista?
    assert result["edad"].max_value == 55
    assert round(result["edad"].mean, 2) == 30.38
    assert result["edad"].median == 30


def test_categorical_column_analysis():
    df = pd.DataFrame({
        "ciudad": ["Bogota", "Medellín", "Bogota", "Cali", "Bogota"]
    })

    analyzer = DescriptiveStatsAnalyzer()   
    result = analyzer.analyze(df)

    assert result["ciudad"].unique_count == 3
    assert result["ciudad"].most_frequent_value == "Bogota"
    assert result["ciudad"].most_frequent_count == 3

def test_empty_dataframe():
    df = pd.DataFrame({
        "edad": pd.array([], dtype="float64")
    })

    analyzer = DescriptiveStatsAnalyzer()
    result = analyzer.analyze(df)

    assert pd.isna(result["edad"].mean)
    assert pd.isna(result["edad"].median)
    assert pd.isna(result["edad"].min_value)
    assert pd.isna(result["edad"].max_value)