from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore


class ClusterProfiling:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.db_path = self.project_root / "db" / "nifty100.db"

        self.output_dir = self.project_root / "output"

        self.report_dir = self.project_root / "reports"

        self.output_dir.mkdir(exist_ok=True)
        self.report_dir.mkdir(exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)

        print("Database Connected Successfully")



    # ============================================================
    # Load Data
    # ============================================================

    def load_data(self):

        query = """
        SELECT
            c.id AS company_id,
            c.company_name,
            s.broad_sector,

            fr.return_on_equity_pct,
            fr.debt_to_equity,
            fr.revenue_cagr_5yr,
            fr.free_cash_flow_cr,
            fr.operating_profit_margin_pct,
            fr.net_profit_margin_pct,
            fr.interest_coverage,
            fr.asset_turnover,
            fr.pat_cagr_5yr,
            fr.eps_cagr_5yr,
            fr.composite_quality_score

        FROM companies c

        LEFT JOIN sectors s
            ON c.id = s.company_id

        LEFT JOIN financial_ratios fr
            ON c.id = fr.company_id

        WHERE fr.year = (
            SELECT MAX(fr2.year)
            FROM financial_ratios fr2
            WHERE fr2.company_id = fr.company_id
        )

        ORDER BY c.company_name
        """

        financial_df = pd.read_sql_query(query, self.conn)

        cluster_path = self.output_dir / "cluster_labels.csv"

        cluster_df = pd.read_csv(cluster_path)

        df = financial_df.merge(
            cluster_df,
            on="company_id",
            how="left"
        )

        print(f"Loaded {len(df)} companies")

        return df



    # ============================================================
    # Cluster Profiling
    # ============================================================

    def generate_cluster_profile(self, df):

        features = [
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "free_cash_flow_cr",
            "operating_profit_margin_pct",
        ]

        profile = (
            df.groupby("cluster_id")[features]
            .agg(["mean", "median"])
            .round(2)
        )

        output_path = self.output_dir / "cluster_profile.csv"

        profile.to_csv(output_path)

        print(f"Cluster profile saved to {output_path}")

        return profile



    # ============================================================
    # Assign Cluster Names
    # ============================================================

    def assign_cluster_names(self, df):

        cluster_names = {
            0: "High-Quality Compounders",
            1: "Defensive Dividend Payers",
            2: "Value Cyclicals",
            3: "Distressed or Turnaround",
            4: "Emerging Growth"
        }

        df["cluster_name"] = df["cluster_id"].map(cluster_names)

        output_path = self.output_dir / "cluster_labels.csv"

        df[
            [
                "company_id",
                "cluster_id",
                "cluster_name",
                "distance_from_centroid"
            ]
        ].to_csv(output_path, index=False)

        print(f"Updated cluster labels saved to {output_path}")

        return df



    # ============================================================
    # Correlation Heatmap
    # ============================================================

    def generate_correlation_heatmap(self, df):

        kpis = [
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "free_cash_flow_cr",
            "operating_profit_margin_pct",
            "net_profit_margin_pct",
            "interest_coverage",
            "asset_turnover",
            "pat_cagr_5yr",
            "eps_cagr_5yr"
        ]

        corr = df[kpis].corr(method="pearson")

        plt.figure(figsize=(10, 8))

        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            fmt=".2f"
        )

        plt.title("Correlation Matrix")

        output_path = self.report_dir / "correlation_heatmap.png"

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

        print(f"Correlation heatmap saved to {output_path}")



    # ============================================================
    # Outlier Detection
    # ============================================================

    def generate_outlier_report(self, df):

        metrics = [
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "free_cash_flow_cr",
            "operating_profit_margin_pct"
        ]

        outlier_frames = []

        for sector, group in df.groupby("broad_sector"):

            temp = group.copy()

            z_scores = temp[metrics].apply(zscore, nan_policy="omit")

            temp["is_outlier"] = (z_scores.abs() > 3).any(axis=1)

            outlier_frames.append(temp)

        result = pd.concat(outlier_frames)

        result = result[result["is_outlier"]]

        output_path = self.output_dir / "outlier_report.csv"

        result.to_csv(output_path, index=False)

        print(f"Outlier report saved to {output_path}")


    # ============================================================
    # Portfolio Statistics
    # ============================================================

    def generate_portfolio_statistics(self, df):

        metrics = [
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "free_cash_flow_cr",
            "operating_profit_margin_pct",
            "net_profit_margin_pct",
            "interest_coverage",
            "asset_turnover",
            "pat_cagr_5yr",
            "eps_cagr_5yr"
        ]

        stats = pd.DataFrame(index=metrics)

        stats["P10"] = df[metrics].quantile(0.10)
        stats["P25"] = df[metrics].quantile(0.25)
        stats["P50"] = df[metrics].quantile(0.50)
        stats["P75"] = df[metrics].quantile(0.75)
        stats["P90"] = df[metrics].quantile(0.90)
        stats["Mean"] = df[metrics].mean()
        stats["Std"] = df[metrics].std()

        output_path = self.output_dir / "portfolio_stats.csv"

        stats.round(2).to_csv(output_path)

        print(f"Portfolio statistics saved to {output_path}")



    # ============================================================
    # Close Database
    # ============================================================

    def close(self):

        self.conn.close()

        print("Database Connection Closed")


if __name__ == "__main__":

    app = ClusterProfiling()

    df = app.load_data()

    app.generate_cluster_profile(df)

    df = app.assign_cluster_names(df)

    app.generate_correlation_heatmap(df)

    app.generate_outlier_report(df)

    app.generate_portfolio_statistics(df)

    app.close()



