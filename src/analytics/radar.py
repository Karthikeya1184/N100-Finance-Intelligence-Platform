import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class RadarChartEngine:

    DB = "db/nifty100.db"

    METRICS = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "composite_quality_score"
    ]

    def __init__(self):

        self.conn = sqlite3.connect(self.DB)

        os.makedirs(
            "reports/radar_charts",
            exist_ok=True
        )

    def load(self):

        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        peers = pd.read_sql(
            "SELECT * FROM peer_groups",
            self.conn
        )

        return ratios.merge(
            peers,
            on="company_id",
            how="left"
        )

    def plot_company(self, company):

        df = self.load()

        row = df[df["company_id"] == company]

        if row.empty:
            print(company, "not found")
            return

        peer = row.iloc[0]["peer_group_name"]

        values = row.iloc[0][self.METRICS].fillna(0).astype(float)

        if pd.isna(peer):

            peer_avg = df[self.METRICS].mean()

        else:

            peer_avg = (
                df[df["peer_group_name"] == peer][self.METRICS]
                .mean()
            )

        labels = self.METRICS

        angles = np.linspace(
            0,
            2*np.pi,
            len(labels),
            endpoint=False
        )

        values = np.concatenate(
            [values, [values.iloc[0]]]
        )

        peer_avg = np.concatenate(
            [peer_avg, [peer_avg.iloc[0]]]
        )

        angles = np.concatenate(
            [angles, [angles[0]]]
        )

        fig = plt.figure(figsize=(8, 8))

        ax = plt.subplot(
            111,
            polar=True
        )

        ax.plot(
            angles,
            values,
            linewidth=2,
            label=company
        )

        ax.fill(
            angles,
            values,
            alpha=0.25
        )

        ax.plot(
            angles,
            peer_avg,
            linestyle="--",
            linewidth=2,
            label="Peer Average"
        )

        ax.set_xticks(
            angles[:-1]
        )

        ax.set_xticklabels(
            labels,
            fontsize=10
        )

        ax.set_title(
            f"{company} Radar",
            fontsize=14
        )

        ax.legend(
            loc="upper right"
        )

        plt.tight_layout()

        plt.savefig(
            f"reports/radar_charts/{company}_radar.png",
            dpi=300
        )

        plt.close()

    def generate_all(self):

        df = self.load()

        for company in sorted(df["company_id"].unique()):

            self.plot_company(company)

        print(
            "Radar charts created."
        )


if __name__ == "__main__":

    RadarChartEngine().generate_all()