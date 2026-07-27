import pandas as pd
from unittest.mock import patch

from src.etl.loader import load_excel


def test_load_excel_success():

    df = pd.DataFrame({"A":[1]})

    with patch("pandas.read_excel", return_value=df):
        result = load_excel("dummy.xlsx",0)

    assert result.equals(df)


def test_load_excel_failure():

    with patch("pandas.read_excel", side_effect=Exception("Error")):
        result = load_excel("dummy.xlsx",0)

    assert result is None