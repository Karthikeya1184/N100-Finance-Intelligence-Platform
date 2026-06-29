import pandas as pd

from pathlib import Path

from src.etl.loader import load_all_files

from src.etl.dq_rules import *

OUTPUT = Path("output")

OUTPUT.mkdir(exist_ok=True)

def run_validation():

    datasets = load_all_files()

    results = []

    companies = datasets["companies"]

    pnl = datasets["profitandloss"]

    rules = [

        dq01_company_pk(companies),

        dq02_company_name(companies),

        dq03_positive_sales(pnl)

    ]

    for rule in rules:

        if rule is not None:

            results.append(rule)

    report = pd.DataFrame(results)

    report.to_csv(

        OUTPUT / "validation_failures.csv",

        index=False

    )

    print()

    print("=" * 60)

    print("Validation Summary")

    print("=" * 60)

    print(report)

    return report