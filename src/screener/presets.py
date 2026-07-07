from src.screener.engine import ScreenerEngine


class PresetScreeners:

    def __init__(self):
        self.engine = ScreenerEngine()
        self.df = self.engine.load_data()

    def quality_compounder(self):

        df = self.df.copy()

        df = df[
            (df["return_on_equity_pct"] > 15) &
            (
                (df["broad_sector"] == "Financials") |
                (df["debt_to_equity"] < 1)
            ) &
            (df["free_cash_flow_cr"] > 0) &
            (df["revenue_cagr_5yr"] > 10)
        ]

        return df.sort_values(
            "composite_quality_score",
            ascending=False
        )

    def value_pick(self):

        df = self.df.copy()

        df = df[
            (df["pe_ratio"] < 20) &
            (df["pb_ratio"] < 3) &
            (
                (df["broad_sector"] == "Financials") |
                (df["debt_to_equity"] < 2)
            ) &
            (df["dividend_yield_pct"] > 1)
        ]

        return df.sort_values(
            "composite_quality_score",
            ascending=False
        )

    def growth_accelerator(self):

        df = self.df.copy()

        df = df[
            (df["pat_cagr_5yr"] > 20) &
            (df["revenue_cagr_5yr"] > 15) &
            (
                (df["broad_sector"] == "Financials") |
                (df["debt_to_equity"] < 2)
            )
        ]

        return df.sort_values(
            "composite_quality_score",
            ascending=False
        )

    def dividend_champion(self):

        df = self.df.copy()

        df = df[
            (df["dividend_yield_pct"] > 2) &
            (df["dividend_payout_ratio_pct"] < 80) &
            (df["free_cash_flow_cr"] > 0)
        ]

        return df.sort_values(
            "composite_quality_score",
            ascending=False
        )

    def debt_free_blue_chip(self):

        df = self.df.copy()

        df = df[
            (df["debt_to_equity"] == 0) &
            (df["return_on_equity_pct"] > 12) &
            (df["sales"] > 5000)
        ]

        return df.sort_values(
            "composite_quality_score",
            ascending=False
        )

    def turnaround_watch(self):

        df = self.df.copy()

        # Temporary implementation until 3-year CAGR
        # and YoY D/E trend are available.

        df = df[
            (df["revenue_cagr_5yr"] > 10) &
            (df["free_cash_flow_cr"] > 0) &
            (df["debt_to_equity"] < 2)
        ]

        return df.sort_values(
            "composite_quality_score",
            ascending=False
        )