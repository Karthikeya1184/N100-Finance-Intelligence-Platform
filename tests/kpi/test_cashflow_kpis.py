from src.analytics.cashflow_kpis import CashFlowEngine


def test_fcf():

    assert CashFlowEngine.free_cash_flow(100,-40)==60


def test_negative_fcf():

    assert CashFlowEngine.free_cash_flow(50,-100)==-50


def test_quality_high():

    cfo=[100,120,150,180,200]
    pat=[80,100,120,150,160]

    assert CashFlowEngine.cfo_quality_score(cfo,pat)=="High Quality"


def test_quality_moderate():

    cfo=[50,60,70]
    pat=[100,100,100]

    assert CashFlowEngine.cfo_quality_score(cfo,pat)=="Moderate"


def test_quality_risk():

    cfo=[20,30]
    pat=[100,100]

    assert CashFlowEngine.cfo_quality_score(cfo,pat)=="Accrual Risk"


def test_quality_pat_zero():

    assert CashFlowEngine.cfo_quality_score([100],[0]) is None


def test_capex():

    value,label=CashFlowEngine.capex_intensity(-50,1000)

    assert label=="Moderate"


def test_capital_intensive():

    value,label=CashFlowEngine.capex_intensity(-300,1000)

    assert label=="Capital Intensive"


def test_asset_light():

    value,label=CashFlowEngine.capex_intensity(-10,1000)

    assert label=="Asset Light"


def test_fcf_conversion():

    assert CashFlowEngine.fcf_conversion(50,100)==50


def test_fcf_conversion_zero():

    assert CashFlowEngine.fcf_conversion(50,0) is None


def test_reinvestor():

    signs,label=CashFlowEngine.capital_pattern(100,-20,-50)

    assert label=="Reinvestor"


def test_shareholder_returns():

    signs,label=CashFlowEngine.capital_pattern(
        100,-20,-50,
        quality="High Quality"
    )

    assert label=="Shareholder Returns"


def test_distress():

    signs,label=CashFlowEngine.capital_pattern(
        -50,
        20,
        10
    )

    assert label=="Distress Signal"