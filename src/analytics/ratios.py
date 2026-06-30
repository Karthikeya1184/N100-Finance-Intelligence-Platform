import pandas as pd
import numpy as np


class RatioEngine:

    @staticmethod
    def net_profit_margin(net_profit, sales):
        if sales is None or sales == 0:
            return None

        return round((net_profit / sales) * 100, 2)

    @staticmethod
    def operating_profit_margin(op, sales):
        if sales is None or sales == 0:
            return None

        return round((op / sales) * 100, 2)

    @staticmethod
    def opm_cross_check(calculated_opm, source_opm):
        if calculated_opm is None or source_opm is None:
            return True

        difference = abs(calculated_opm - source_opm)

        return difference <= 1

    @staticmethod
    def log_opm_difference(company, year, calculated, source, logfile):
        difference = abs(calculated - source)

        if difference <= 1:
            return

        with open(logfile, "a") as f:
            f.write(
                f"{company},{year},Calculated={calculated},"
                f"Source={source},Difference={difference:.2f}\n"
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
    def roa(net_profit, assets):
        if assets == 0:
            return None

        return round((net_profit / assets) * 100, 2)