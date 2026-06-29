"""
Data Quality Rules for Sprint 1
"""

import pandas as pd


def create_result(rule, severity, table, rows, message):
    """
    Create a standard validation result.
    """
    return {
        "rule": rule,
        "severity": severity,
        "table": table,
        "failed_rows": rows,
        "message": message
    }

def dq01_company_pk(df):

    duplicates = df["id"].duplicated().sum()

    if duplicates > 0:

        return create_result(
            "DQ01",
            "CRITICAL",
            "companies",
            duplicates,
            "Duplicate Company IDs found."
        )

    return None

def dq02_company_name(df):

    missing = df["company_name"].isna().sum()

    if missing > 0:

        return create_result(
            "DQ02",
            "CRITICAL",
            "companies",
            missing,
            "Company Name is missing."
        )

    return None

def dq03_positive_sales(df):

    if "Sales" not in df.columns:
        return None

    failed = (df["Sales"] <= 0).sum()

    if failed > 0:

        return create_result(
            "DQ03",
            "WARNING",
            "profitandloss",
            failed,
            "Sales should be positive."
        )

    return None

