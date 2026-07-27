import numpy as np
from src.etl.normaliser import normalize_year


def test_year_2021():
    assert normalize_year("2021") == 2021


def test_year_spaces():
    assert normalize_year(" 2022 ") == 2022


def test_fy23():
    assert normalize_year("FY23") == 2023


def test_fy24_lower():
    assert normalize_year("fy24") == 2024


def test_range():
    assert normalize_year("2022-23") == 2023


def test_nan():
    assert normalize_year(np.nan) is None


def test_none():
    assert normalize_year(None) is None


def test_invalid():
    assert normalize_year("ABC") is None


def test_empty():
    assert normalize_year("") is None


def test_spaces():
    assert normalize_year("   ") is None
