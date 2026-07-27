from src.analytics.ratios import RatioEngine


def test_roe_positive():
    assert RatioEngine.roe(100, 500, 500) == 10.0


def test_roe_negative_equity():
    assert RatioEngine.roe(100, -100, -50) is None


def test_debt_free():
    assert RatioEngine.debt_to_equity(0, 100, 100) == 0


def test_interest_zero():
    assert RatioEngine.interest_coverage(100, 20, 0) is None


def test_high_leverage():
    assert RatioEngine.high_leverage_flag(6, "Manufacturing")


def test_financial_not_flagged():
    assert not RatioEngine.high_leverage_flag(8, "Financials")


def test_asset_turnover():
    assert RatioEngine.asset_turnover(200, 100) == 2.0


def test_roa():
    assert RatioEngine.roa(100, 1000) == 10.0
