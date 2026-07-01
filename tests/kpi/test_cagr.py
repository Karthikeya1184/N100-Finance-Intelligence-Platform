from src.analytics.cagr import (
    CAGRCalculator,
    revenue_cagr,
    pat_cagr,
    eps_cagr,
    revenue_cagr_3yr,
    revenue_cagr_5yr,
    revenue_cagr_10yr,
    pat_cagr_3yr,
    pat_cagr_5yr,
    pat_cagr_10yr,
    eps_cagr_3yr,
    eps_cagr_5yr,
    eps_cagr_10yr
)

def test_normal_cagr():

    value, flag = CAGRCalculator.calculate(100,200,5)

    assert round(value,2)==14.87

    assert flag=="NORMAL"

def test_turnaround():

    value,flag=CAGRCalculator.calculate(-100,100,5)

    assert value is None

    assert flag=="TURNAROUND"

def test_decline_to_loss():

    value,flag=CAGRCalculator.calculate(100,-100,5)

    assert value is None

    assert flag=="DECLINE_TO_LOSS"

def test_both_negative():

    value,flag=CAGRCalculator.calculate(-100,-50,5)

    assert value is None

    assert flag=="BOTH_NEGATIVE"

def test_zero_base():

    value,flag=CAGRCalculator.calculate(0,200,5)

    assert value is None

    assert flag=="ZERO_BASE"

def test_invalid_period():

    value,flag=CAGRCalculator.calculate(100,200,0)

    assert value is None

    assert flag=="INVALID_PERIOD"

def test_revenue():

    value,flag=revenue_cagr(100,200,5)

    assert flag=="NORMAL"

def test_pat():

    value,flag=pat_cagr(100,200,5)

    assert flag=="NORMAL"

def test_eps():

    value,flag=eps_cagr(100,200,5)

    assert flag=="NORMAL"

def test_insufficient():

    value,flag=CAGRCalculator.calculate(100,200,None)

    assert value is None

    assert flag=="INSUFFICIENT"    


def test_revenue_3yr():
    value, flag = revenue_cagr_3yr(100, 200)
    assert flag == "NORMAL"


def test_revenue_5yr():
    value, flag = revenue_cagr_5yr(100, 200)
    assert flag == "NORMAL"


def test_revenue_10yr():
    value, flag = revenue_cagr_10yr(100, 200)
    assert flag == "NORMAL"


def test_pat_5yr():
    value, flag = pat_cagr_5yr(100, 200)
    assert flag == "NORMAL"


def test_eps_5yr():
    value, flag = eps_cagr_5yr(100, 200)
    assert flag == "NORMAL"