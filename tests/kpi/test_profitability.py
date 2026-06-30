from src.analytics.ratios import RatioEngine


def test_npm():

    assert RatioEngine.net_profit_margin(100,1000)==10


def test_npm_zero_sales():

    assert RatioEngine.net_profit_margin(10,0) is None


def test_opm():

    assert RatioEngine.operating_profit_margin(250,1000)==25


def test_roe():

    assert RatioEngine.roe(100,500,500)==10


def test_negative_equity():

    assert RatioEngine.roe(100,-100,-200) is None


def test_roce():

    assert RatioEngine.roce(100,500,500,500)==6.67


def test_roa():

    assert RatioEngine.roa(100,1000)==10


def test_roa_zero():

    assert RatioEngine.roa(100,0) is None

def test_opm_crosscheck_ok():

    assert RatioEngine.opm_cross_check(20,20.5)==True

def test_opm_crosscheck_fail():

    assert RatioEngine.opm_cross_check(20,25)==False

def test_roce_status():

    assert RatioEngine.roce_status(18,"IT")=="Excellent"

def test_financial_sector():

    assert RatioEngine.roce_status(5,"Financials")=="Sector Benchmark"            