from src.analytics.ratios import RatioEngine
from src.analytics.cashflow_kpis import CashFlowEngine
from src.analytics.cagr import (
    revenue_cagr_5yr,
    pat_cagr_5yr,
    eps_cagr_5yr
)


class RatioCalculator:

    @staticmethod
    def calculate(row, company_df, company_master):

        result = {}

        result["net_profit_margin_pct"] = RatioEngine.net_profit_margin(
            row["net_profit"],
            row["sales"]
        )

        result["operating_profit_margin_pct"] = RatioEngine.operating_profit_margin(
            row["operating_profit"],
            row["sales"]
        )

        result["return_on_equity_pct"] = RatioEngine.roe(
            row["net_profit"],
            row["equity_capital"],
            row["reserves"]
        )

        result["debt_to_equity"] = RatioEngine.debt_to_equity(
            row["borrowings"],
            row["equity_capital"],
            row["reserves"]
        )

        result["interest_coverage"] = RatioEngine.interest_coverage(
            row["operating_profit"],
            row["other_income"],
            row["interest"]
        )

        result["asset_turnover"] = RatioEngine.asset_turnover(
            row["sales"],
            row["total_assets"]
        )

        result["free_cash_flow_cr"] = CashFlowEngine.free_cash_flow(
            row["operating_activity"],
            row["investing_activity"]
        )

        result["capex_cr"] = CashFlowEngine.capex_intensity(
            row["investing_activity"],
            row["sales"]
        )[0]

        result["earnings_per_share"] = row["eps"]

        result["book_value_per_share"] = company_master["book_value"]

        result["dividend_payout_ratio_pct"] = row["dividend_payout"]

        result["total_debt_cr"] = row["borrowings"]

        result["cash_from_operations_cr"] = row["operating_activity"]

        sales = company_df["sales"].tolist()

        profit = company_df["net_profit"].tolist()

        eps = company_df["eps"].tolist()

        if len(sales) >= 6:

            revenue, _ = revenue_cagr_5yr(
                sales[-6],
                sales[-1]
            )

            pat, _ = pat_cagr_5yr(
                profit[-6],
                profit[-1]
            )

            eps_growth, _ = eps_cagr_5yr(
                eps[-6],
                eps[-1]
            )

        else:

            revenue = None
            pat = None
            eps_growth = None

        result["revenue_cagr_5yr"] = revenue

        result["pat_cagr_5yr"] = pat

        result["eps_cagr_5yr"] = eps_growth

        score = 0

        if result["return_on_equity_pct"] is not None:

            if result["return_on_equity_pct"] > 15:
                score += 1

        if result["debt_to_equity"] is not None:

            if result["debt_to_equity"] < 1:
                score += 1

        if result["interest_coverage"] is not None:

            if result["interest_coverage"] > 3:
                score += 1

        result["composite_quality_score"] = score

        return result