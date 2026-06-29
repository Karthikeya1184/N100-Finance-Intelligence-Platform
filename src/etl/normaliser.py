import re
import pandas as pd
def normalize_year(year):
    """
    Converts year values into integer format.

    Examples

    FY23 -> 2023

    2022-23 -> 2023

    2021 -> 2021
    """

    if pd.isna(year):
        return None

    year = str(year).strip()

    if re.match(r"^\d{4}$", year):
        return int(year)

    if re.match(r"^\d{4}-\d{2}$", year):
        return int("20" + year[-2:])

    if year.upper().startswith("FY"):
        return int("20" + year[-2:])

    return None

def normalize_ticker(name):

    if pd.isna(name):
        return None

    name = str(name).upper()

    name = name.replace(".NS", "")

    name = name.replace("&", "AND")

    name = name.strip()

    return name