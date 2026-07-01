import pandas as pd


class CashFlowEngine:

    @staticmethod
    def free_cash_flow(cfo, cfi):
        """
        Free Cash Flow = CFO + CFI
        """
        return cfo + cfi

    @staticmethod
    def cfo_quality_score(cfo_list, pat_list):
        """
        Average CFO/PAT over available years.
        """

        ratios = []

        for cfo, pat in zip(cfo_list, pat_list):

            if pat == 0:
                continue

            ratios.append(cfo / pat)

        if len(ratios) == 0:
            return None

        avg = sum(ratios) / len(ratios)

        if avg > 1:
            return "High Quality"

        elif avg >= 0.5:
            return "Moderate"

        return "Accrual Risk"

    @staticmethod
    def capex_intensity(investing_activity, sales):

        if sales == 0:
            return None, "Unavailable"

        value = abs(investing_activity) / sales * 100

        if value < 3:
            label = "Asset Light"

        elif value <= 8:
            label = "Moderate"

        else:
            label = "Capital Intensive"

        return round(value, 2), label

    @staticmethod
    def fcf_conversion(fcf, operating_profit):

        if operating_profit == 0:
            return None

        return round((fcf / operating_profit) * 100, 2)

    @staticmethod
    def capital_pattern(cfo, cfi, cff, quality=None):

        signs = (
            "+" if cfo >= 0 else "-",
            "+" if cfi >= 0 else "-",
            "+" if cff >= 0 else "-"
        )

        mapping = {

            ("+","-","-"):"Reinvestor",

            ("+","+","-"):"Liquidating Assets",

            ("-","+","+"):"Distress Signal",

            ("-","-","+"):"Growth Funded by Debt",

            ("+","+","+"):"Cash Accumulator",

            ("-","-","-"):"Pre-Revenue",

            ("+","-","+"):"Mixed"

        }

        pattern = mapping.get(signs, "Unknown")

        if signs == ("+","-","-") and quality == "High Quality":
            pattern = "Shareholder Returns"

        return signs, pattern