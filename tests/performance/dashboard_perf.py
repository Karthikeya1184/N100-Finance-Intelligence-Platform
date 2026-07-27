import requests
import time

tickers = ["TCS", "INFY", "RELIANCE", "HDFCBANK", "ITC"]

for ticker in tickers:

    start = time.perf_counter()

    r = requests.get(f"http://127.0.0.1:8000/api/v1/companies/{ticker}")

    elapsed = time.perf_counter() - start

    print(f"{ticker}: " f"{elapsed:.3f}s " f"Status={r.status_code}")
