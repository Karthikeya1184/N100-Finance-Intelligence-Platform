import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

indexes = [

"""
CREATE INDEX IF NOT EXISTS idx_financial_ratios_company_year
ON financial_ratios(company_id, year)
""",

"""
CREATE INDEX IF NOT EXISTS idx_profit_company_year
ON profitandloss(company_id, year)
""",

"""
CREATE INDEX IF NOT EXISTS idx_balance_company_year
ON balancesheet(company_id, year)
""",

"""
CREATE INDEX IF NOT EXISTS idx_cashflow_company_year
ON cashflow(company_id, year)
"""

]

for sql in indexes:
    cursor.execute(sql)

conn.commit()

print("Indexes created successfully.")

conn.close()