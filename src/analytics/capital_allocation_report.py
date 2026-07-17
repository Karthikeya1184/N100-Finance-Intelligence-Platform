"""
Sprint 5 - Day 32
Capital Allocation Report

Outputs:
1. output/capital_allocation_summary.csv
2. output/pattern_changes.csv
3. Updated output/cashflow_intelligence.xlsx
"""

from pathlib import Path
import sqlite3

import pandas as pd


class CapitalAllocationReport:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]

        self.db_path = self.project_root / "db" / "nifty100.db"

        self.capital_file = (
            self.project_root / "output" / "capital_allocation.csv"
        )

        self.cashflow_excel = (
            self.project_root / "output" / "cashflow_intelligence.xlsx"
        )

        self.output_dir = self.project_root / "output"
        self.output_dir.mkdir(exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)

    def close(self):
        self.conn.close()

    # --------------------------------------------------------
    # Load capital allocation data
    # --------------------------------------------------------

    def load_capital_data(self):

        if not self.capital_file.exists():
            raise FileNotFoundError(
                f"Missing file: {self.capital_file}"
            )

        df = pd.read_csv(self.capital_file)

        return df

    # --------------------------------------------------------
    # Load company names
    # --------------------------------------------------------

    def load_companies(self):

        query = """
        SELECT
            id AS company_id,
            company_name
        FROM companies
        """

        return pd.read_sql(query, self.conn)

    # --------------------------------------------------------
    # Verification
    # --------------------------------------------------------

    def verify_data(self, df):

        print("\nVerifying capital allocation dataset...")

        print(f"Rows                : {len(df):,}")
        print(f"Companies           : {df['company_id'].nunique()}")
        print(f"Years               : {df['year'].nunique()}")

        duplicates = df.duplicated(
            subset=["company_id", "year"]
        ).sum()

        print(f"Duplicate rows      : {duplicates}")

        missing = df["pattern_label"].isna().sum()

        print(f"Missing patterns    : {missing}")

        if duplicates > 0:
            print("WARNING: Duplicate company/year rows detected.")

        if missing > 0:
            print("WARNING: Missing capital allocation patterns.")

        print("Verification complete.\n")

    # --------------------------------------------------------
    # Latest year per company
    # --------------------------------------------------------

    def latest_patterns(self, df):

        latest = (
            df.sort_values(["company_id", "year"])
              .groupby("company_id")
              .tail(1)
              .reset_index(drop=True)
        )

        return latest
    


    # --------------------------------------------------------
    # Distribution summary
    # --------------------------------------------------------

    def generate_distribution_summary(self, latest_df):

        summary = (
            latest_df["pattern_label"]
            .value_counts()
            .rename_axis("pattern")
            .reset_index(name="company_count")
            .sort_values("company_count", ascending=False)
        )

        summary_path = (
            self.output_dir / "capital_allocation_summary.csv"
        )

        summary.to_csv(summary_path, index=False)

        print(f"✓ Distribution summary saved: {summary_path}")

        return summary

    # --------------------------------------------------------
    # Pattern changes
    # --------------------------------------------------------

    def generate_pattern_changes(self, df):

        df = df.sort_values(["company_id", "year"])

        previous = (
            df.groupby("company_id")["pattern_label"]
            .shift(1)
        )

        changes = df.copy()

        changes["previous_pattern"] = previous

        changes["changed"] = (
            changes["previous_pattern"]
            != changes["pattern_label"]
        )

        latest_changes = (
            changes.groupby("company_id")
            .tail(1)
            .copy()
        )

        companies = self.load_companies()

        latest_changes = latest_changes.merge(
            companies,
            on="company_id",
            how="left"
        )

        latest_changes.rename(
            columns={
                "pattern_label": "current_pattern"
            },
            inplace=True
        )

        latest_changes = latest_changes[
            [
                "company_id",
                "company_name",
                "previous_pattern",
                "current_pattern",
                "changed",
            ]
        ]

        latest_changes["changed"] = (
            latest_changes["changed"]
            .map({True: "Yes", False: "No"})
        )

        output_path = (
            self.output_dir / "pattern_changes.csv"
        )

        latest_changes.to_csv(
            output_path,
            index=False
        )

        print(f"✓ Pattern changes saved: {output_path}")

        return latest_changes

    # --------------------------------------------------------
    # Console summary
    # --------------------------------------------------------

    def print_summary(self, summary):

        print("\n" + "=" * 60)
        print("Capital Allocation Distribution (Latest Year)")
        print("=" * 60)

        print(summary.to_string(index=False))

        print("=" * 60)




    # --------------------------------------------------------
    # Update Cash Flow Intelligence Workbook
    # --------------------------------------------------------

    def update_cashflow_excel(self, latest_df):

        if not self.cashflow_excel.exists():
            raise FileNotFoundError(
                f"Missing file: {self.cashflow_excel}"
            )

        excel_df = pd.read_excel(self.cashflow_excel)

        latest_df = latest_df[
            ["company_id", "pattern_label"]
        ].rename(
            columns={
                "pattern_label": "capital_allocation_pattern"
            }
        )

        updated = excel_df.merge(
            latest_df,
            on="company_id",
            how="left"
        )

        updated.to_excel(
            self.cashflow_excel,
            index=False
        )

        print(
            f"✓ Updated workbook: {self.cashflow_excel}"
        )

    # --------------------------------------------------------
    # Run Day 32
    # --------------------------------------------------------

    def run(self):

        capital_df = self.load_capital_data()

        self.verify_data(capital_df)

        latest_df = self.latest_patterns(capital_df)

        summary = self.generate_distribution_summary(
            latest_df
        )

        self.generate_pattern_changes(capital_df)

        self.update_cashflow_excel(latest_df)

        self.print_summary(summary)

        print("\n" + "=" * 60)
        print("DAY 32 COMPLETED")
        print("=" * 60)
        print(f"Companies Processed : {latest_df['company_id'].nunique()}")
        print(f"Latest Records      : {len(latest_df)}")
        print()
        print("Files Generated")
        print("✓ output/capital_allocation_summary.csv")
        print("✓ output/pattern_changes.csv")
        print("✓ output/cashflow_intelligence.xlsx")



if __name__ == "__main__":
    app = CapitalAllocationReport()

    try:
        app.run()
    finally:
        app.close()