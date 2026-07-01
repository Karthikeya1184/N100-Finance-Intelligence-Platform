class CAGRCalculator:

    @staticmethod
    def calculate(start, end, years):

        """
        CAGR Formula

        ((End / Start) ** (1 / Years) - 1) * 100
        """

        if years is None:
            return None, "INSUFFICIENT"

        if years <= 0:
            return None, "INVALID_PERIOD"

        if start == 0:
            return None, "ZERO_BASE"

        if start > 0 and end < 0:
            return None, "DECLINE_TO_LOSS"

        if start < 0 and end > 0:
            return None, "TURNAROUND"

        if start < 0 and end < 0:
            return None, "BOTH_NEGATIVE"

        cagr = ((end / start) ** (1 / years) - 1) * 100

        return round(cagr, 2), "NORMAL"


def revenue_cagr(start, end, years):
    return CAGRCalculator.calculate(start, end, years)


def pat_cagr(start, end, years):
    return CAGRCalculator.calculate(start, end, years)


def eps_cagr(start, end, years):
    return CAGRCalculator.calculate(start, end, years)

# Revenue CAGR

def revenue_cagr_3yr(start, end):
    return revenue_cagr(start, end, 3)


def revenue_cagr_5yr(start, end):
    return revenue_cagr(start, end, 5)


def revenue_cagr_10yr(start, end):
    return revenue_cagr(start, end, 10)


# PAT CAGR

def pat_cagr_3yr(start, end):
    return pat_cagr(start, end, 3)


def pat_cagr_5yr(start, end):
    return pat_cagr(start, end, 5)


def pat_cagr_10yr(start, end):
    return pat_cagr(start, end, 10)


# EPS CAGR

def eps_cagr_3yr(start, end):
    return eps_cagr(start, end, 3)


def eps_cagr_5yr(start, end):
    return eps_cagr(start, end, 5)


def eps_cagr_10yr(start, end):
    return eps_cagr(start, end, 10)
