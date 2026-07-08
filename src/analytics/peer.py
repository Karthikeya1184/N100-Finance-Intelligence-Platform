import sqlite3
import pandas as pd


class PeerEngine:

    DB = "db/nifty100.db"

    METRICS = [
        "return_on_equity_pct",
        # Uncomment if available
        # "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "eps_cagr_5yr",
        "interest_coverage",
        "asset_turnover",
    ]

    def __init__(self):

        self.conn = sqlite3.connect(self.DB)

    def load(self):

        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn,
        )

        peer = pd.read_sql(
            "SELECT * FROM peer_groups",
            self.conn,
        )

        df = ratios.merge(
            peer,
            on="company_id",
            how="left",
        )

        return df

    def calculate(self):

        df = self.load()

        # -------------------------
        # Companies without peer group
        # -------------------------

        missing = df[df["peer_group_name"].isna()]

        if not missing.empty:

            print("\nNo peer group assigned:")

            print(missing["company_id"].unique())

        output = []

        # -------------------------
        # Peer Ranking
        # -------------------------

        for group in df["peer_group_name"].dropna().unique():

            peer_df = df[df["peer_group_name"] == group].copy()

            for metric in self.METRICS:

                if metric not in peer_df.columns:
                    continue

                ranks = peer_df[metric].rank(
                    pct=True,
                    method="average"
                )

                # Lower D/E is better
                if metric == "debt_to_equity":
                    ranks = 1 - ranks

                for idx in peer_df.index:

                    output.append({

                        "company_id":
                            peer_df.loc[idx, "company_id"],

                        "peer_group_name":
                            group,

                        "metric":
                            metric,

                        "value":
                            peer_df.loc[idx, metric],

                        "percentile_rank":
                            round(ranks.loc[idx], 4),

                        "year":
                            peer_df.loc[idx, "year"]

                    })

        result = pd.DataFrame(output)

        result.to_sql(

            "peer_percentiles",

            self.conn,

            if_exists="replace",

            index=False

        )

        print("\nPeer Percentiles Created Successfully")

        print(result.head())

        print()

        print("Rows:", len(result))

        self.conn.close()

        return result


if __name__ == "__main__":

    PeerEngine().calculate()