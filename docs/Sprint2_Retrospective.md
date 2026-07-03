# Sprint 2 Retrospective

## Objective

Build a Financial Ratio Engine capable of computing profitability, leverage, efficiency, CAGR and cash flow KPIs for all companies.

---

## Formula Decisions

- Net Profit Margin = Net Profit / Sales ×100
- Operating Margin = Operating Profit / Sales ×100
- ROE = Net Profit / (Equity + Reserves)
- ROCE = EBIT / Capital Employed
- ROA = Net Profit / Total Assets
- Debt to Equity = Borrowings / Equity
- Interest Coverage = EBIT / Interest
- Asset Turnover = Sales / Total Assets
- Free Cash Flow = CFO + Investing Activity
- Revenue CAGR = CAGR over 5 years
- PAT CAGR = CAGR over 5 years
- EPS CAGR = CAGR over 5 years

---

## Edge Cases

- Zero denominator returns None
- Negative equity returns None
- Debt-free companies return D/E = 0
- Financial sector excluded from High Leverage warning
- CAGR handles:
  - Turnaround
  - Decline to Loss
  - Zero Base
  - Both Negative
  - Insufficient History

---

## Testing

- Total Tests Passed: 94
- Failed Tests: 0

---

## Deliverables

- Ratio Engine
- CAGR Engine
- Cash Flow KPIs
- SQLite financial_ratios table
- ratio_edge_cases.log
- Capital Allocation CSV