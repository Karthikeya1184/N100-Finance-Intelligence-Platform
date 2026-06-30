class RatioEngine:

    # -------------------------
    # DAY 08
    # -------------------------

    @staticmethod
    def net_profit_margin(net_profit, sales):
        if sales == 0:
            return None
        return round((net_profit / sales) * 100, 2)

    @staticmethod
    def operating_profit_margin(operating_profit, sales):
        if sales == 0:
            return None
        return round((operating_profit / sales) * 100, 2)

    @staticmethod
    def opm_cross_check(calculated, source):
        if calculated is None or source is None:
            return True

        return abs(calculated - source) <= 1

    @staticmethod
    def log_opm_difference(company, year, calculated, source, logfile):
        if abs(calculated - source) <= 1:
            return

        with open(logfile, "a") as f:
            f.write(
                f"{company},{year},Calculated={calculated},"
                f"Source={source}\n"
            )

    @staticmethod
    def roe(net_profit, equity, reserves):
        capital = equity + reserves

        if capital <= 0:
            return None

        return round((net_profit / capital) * 100, 2)

    @staticmethod
    def roce(ebit, equity, reserves, borrowings):
        capital = equity + reserves + borrowings

        if capital <= 0:
            return None

        return round((ebit / capital) * 100, 2)

    @staticmethod
    def roce_status(roce, sector):
        if roce is None:
            return "Unavailable"

        if sector == "Financials":
            return "Sector Benchmark"

        if roce >= 15:
            return "Excellent"

        if roce >= 10:
            return "Good"

        return "Weak"

    @staticmethod
    def roa(net_profit, total_assets):
        if total_assets == 0:
            return None

        return round((net_profit / total_assets) * 100, 2)

    # -------------------------
    # DAY 09
    # -------------------------

    @staticmethod
    def debt_to_equity(borrowings, equity_capital, reserves):

        if borrowings == 0:
            return 0

        capital = equity_capital + reserves

        if capital <= 0:
            return None

        return round(borrowings / capital, 2)

    @staticmethod
    def high_leverage_flag(de_ratio, sector):

        if de_ratio is None:
            return False

        if sector == "Financials":
            return False

        return de_ratio > 5

    @staticmethod
    def interest_coverage(operating_profit, other_income, interest):

        if interest == 0:
            return None

        return round((operating_profit + other_income) / interest, 2)

    @staticmethod
    def icr_label(icr):

        if icr is None:
            return "Debt Free"

        return ""

    @staticmethod
    def icr_warning(icr):

        if icr is None:
            return False

        return icr < 1.5

    @staticmethod
    def net_debt(borrowings, investments):

        return borrowings - investments

    @staticmethod
    def asset_turnover(sales, total_assets):

        if total_assets == 0:
            return None

        return round(sales / total_assets, 2)