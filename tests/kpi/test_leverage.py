from src.analytics.ratios import RatioEngine


def test_debt_to_equity_normal():
    assert RatioEngine.debt_to_equity(200, 500, 500) == 0.2


def test_debt_free():
    assert RatioEngine.debt_to_equity(0, 500, 500) == 0


def test_negative_equity():
    assert RatioEngine.debt_to_equity(200, -100, -200) is None


def test_high_leverage():
    assert RatioEngine.high_leverage_flag(6, "IT") is True


def test_financial_sector_no_flag():
    assert RatioEngine.high_leverage_flag(8, "Financials") is False


def test_interest_coverage():
    assert RatioEngine.interest_coverage(100, 20, 10) == 12


def test_interest_zero():
    assert RatioEngine.interest_coverage(100, 20, 0) is None


def test_icr_label():
    assert RatioEngine.icr_label(None) == "Debt Free"


def test_icr_warning():
    assert RatioEngine.icr_warning(1.2) is True


def test_net_debt():
    assert RatioEngine.net_debt(1000, 300) == 700


def test_asset_turnover():
    assert RatioEngine.asset_turnover(1000, 500) == 2


def test_asset_turnover_zero():
    assert RatioEngine.asset_turnover(1000, 0) is None