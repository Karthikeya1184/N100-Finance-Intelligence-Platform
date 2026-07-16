# 📈 N100 Finance Intelligence Platform

A comprehensive Business Intelligence platform for analyzing **Nifty 100 companies** using Python, SQLite, Streamlit, and Plotly.

The platform enables users to explore company fundamentals, compare peers, screen stocks using financial metrics, visualize historical trends, analyze sectors, study capital allocation patterns, access annual reports, and evaluate company valuations through an interactive dashboard.

---

# Project Overview

The N100 Finance Intelligence Platform was developed as part of the Bluestock Sprint project to provide an end-to-end analytics solution for the Nifty 100 universe.

The platform integrates financial data from multiple sources into a centralized SQLite database and presents interactive visualizations through a Streamlit dashboard.

---

# Features

## Dashboard

- Home Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation Map
- Annual Reports
- Valuation Module

---

# Technology Stack

### Programming Language

- Python 3.12

### Database

- SQLite

### Dashboard

- Streamlit

### Libraries

- Pandas
- NumPy
- Plotly
- OpenPyXL

### Version Control

- Git
- GitHub

---

# Project Structure

```
N100-Finance-Intelligence-Platform
│
├── dashboard
│   ├── app.py
│   ├── pages
│   └── utils
│
├── db
│   └── nifty100.db
│
├── output
│   ├── valuation_summary.xlsx
│   └── valuation_flags.csv
│
├── src
│   ├── analytics
│   ├── database
│   ├── etl
│   └── screener
│
├── tests
│
├── requirements.txt
│
└── README.md
```

---

# Installation

Clone the repository

```bash
https://github.com/Karthikeya1184/N100-Finance-Intelligence-Platform
```

Move into the project folder

```bash
cd N100-Finance-Intelligence-Platform
```

Create Virtual Environment

```bash
python -m venv .venv
```

Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Dashboard

Launch the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

After launching, open the local Streamlit URL shown in the terminal (typically `http://localhost:8501`).

---

# Dashboard Screens

## 1. Home

Displays overall project KPIs including:

- Average ROE
- Median Debt-to-Equity
- Company Count
- Revenue CAGR
- Composite Quality Score
- Sector Distribution
- Top Quality Companies

---

## 2. Company Profile

Displays:

- Company Information
- Business Description
- Sector Information
- Financial Ratios
- Key Metrics
- Company Overview

---

## 3. Stock Screener

Interactive stock filtering using:

- ROE
- Debt to Equity
- Free Cash Flow
- Revenue CAGR
- PAT CAGR
- Operating Margin
- P/E
- P/B
- Dividend Yield
- Interest Coverage

Includes:

- Preset Filters
- Live Results
- CSV Download

---

## 4. Peer Comparison

Compare companies within the same peer group.

Features:

- Radar Chart
- Benchmark Comparison
- KPI Comparison Table

---

## 5. Trend Analysis

Historical financial trend visualization.

Supports multiple metrics including:

- Revenue
- ROE
- Net Profit
- Operating Margin
- Cash Flow

Interactive Plotly charts with Year-over-Year analysis.

---

## 6. Sector Analysis

Provides:

- Sector Bubble Chart
- Sector Median KPIs
- Company Distribution
- Sub-sector Analysis

---

## 7. Capital Allocation

Visualizes capital allocation strategy using:

- Treemap
- Capital Allocation Categories
- Company List by Pattern

---

## 8. Annual Reports

Allows users to:

- Search Companies
- View Available Annual Reports
- Open Report Links
- Identify Missing Reports

---

## 9. Valuation Module

Performs valuation analytics including:

- Free Cash Flow Yield
- Sector Median P/E
- 5-Year Median P/E
- Premium / Discount Analysis
- Valuation Flags

Exports:

```
output/
│
├── valuation_summary.xlsx
└── valuation_flags.csv
```

---

# Data Sources

The project uses structured financial datasets stored inside SQLite.

Major tables include:

- Companies
- Sectors
- Market Cap
- Financial Ratios
- Profit & Loss
- Balance Sheet
- Cash Flow
- Peer Groups
- Documents

---

# Key Outputs

Generated outputs include:

- Interactive Dashboard
- KPI Visualizations
- CSV Downloads
- Excel Reports
- Valuation Summary
- Flagged Companies Report

---

# Testing & Quality Assurance

The dashboard was tested for:

- Screen Navigation
- Company Profile
- Screener Filters
- Peer Comparison
- Trend Charts
- Sector Charts
- Capital Allocation
- Annual Reports
- Missing Data Handling
- Performance

---

# Sprint 4 Retrospective

## UX Decisions

- Clean sidebar navigation
- Interactive Plotly visualizations
- KPI cards for quick insights
- Responsive dashboard layout
- Downloadable reports

---

## Data Edge Cases

Handled:

- Missing financial metrics
- Companies with partial history
- Empty screener results
- Missing annual reports
- Missing valuation metrics

---

## Performance Findings

- SQLite provided fast local querying.
- Streamlit caching improved dashboard responsiveness.
- Interactive Plotly charts rendered smoothly.
- Dashboard navigation remained responsive across all screens.

---

# Future Improvements

- Live NSE/BSE market integration
- User authentication
- Portfolio analytics
- Watchlist functionality
- AI-based stock recommendations
- Financial statement forecasting

---

# Developed By

**Karthikeya Bammidi**

MBA Business Analytics

SRM Institute of Science and Technology

GitHub:
https://github.com/Karthikeya1184

LinkedIn:
https://www.linkedin.com/

---

# License

This project was developed for educational and internship purposes as part of the Bluestock Sprint Program.
