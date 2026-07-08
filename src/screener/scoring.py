import pandas as pd


class CompositeScorer:

    @staticmethod
    def winsorize(series):

        p10 = series.quantile(0.10)
        p90 = series.quantile(0.90)

        return series.clip(lower=p10, upper=p90)

    @staticmethod
    def normalize(series):

        s = CompositeScorer.winsorize(series)

        mn = s.min()
        mx = s.max()

        if mx == mn:
            return pd.Series([50] * len(s), index=s.index)

        return ((s - mn) / (mx - mn)) * 100

    def score(self, df):

        df = df.copy()

        metrics = [
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "net_profit_margin_pct",
            "free_cash_flow_cr",
            "cash_from_operations_cr",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "debt_to_equity",
            "interest_coverage"
        ]

        for m in metrics:

            if m in df.columns:

                df[m + "_score"] = self.normalize(df[m])

        # Profitability

        profitability = (

    df["return_on_equity_pct_score"] * 0.25 +

    df["net_profit_margin_pct_score"] * 0.10

)

        # Cash Quality

        cash = (

            df["free_cash_flow_cr_score"] * 0.20 +

            df["cash_from_operations_cr_score"] * 0.10

        )

        # Growth

        growth = (

            df["revenue_cagr_5yr_score"] * 0.10 +

            df["pat_cagr_5yr_score"] * 0.10

        )

        # Leverage

        leverage = (

            (100 - df["debt_to_equity_score"]) * 0.10 +

            df["interest_coverage_score"] * 0.05

        )

        df["composite_quality_score"] = (

            profitability +

            cash +

            growth +

            leverage

        ).round(2)

        return df