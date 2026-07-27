import pandas as pd

from src.etl.dq_rules import *


def test_dq01_duplicate():

    df = pd.DataFrame({"id": [1, 1]})

    result = dq01_company_pk(df)

    assert result["rule"] == "DQ01"


def test_dq02_missing():

    df = pd.DataFrame({"company_name": [None]})

    result = dq02_company_name(df)

    assert result["rule"] == "DQ02"


def test_dq03_negative_sales():

    df = pd.DataFrame({"Sales": [-10]})

    result = dq03_positive_sales(df)

    assert result["rule"] == "DQ03"
