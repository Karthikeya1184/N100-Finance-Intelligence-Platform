-- 1. Total Companies
SELECT COUNT(*) FROM companies;

-- 2. Total Profit & Loss Records
SELECT COUNT(*) FROM profitandloss;

-- 3. Total Balance Sheet Records
SELECT COUNT(*) FROM balancesheet;

-- 4. Total Cash Flow Records
SELECT COUNT(*) FROM cashflow;

-- 5. Top 10 Companies by ROE
SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- 6. Top 10 Companies by ROCE
SELECT company_name, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;

-- 7. Highest Sales
SELECT company_id, year, sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

-- 8. Highest Net Profit
SELECT company_id, year, net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- 9. Companies by Sector
SELECT broad_sector, COUNT(*)
FROM sectors
GROUP BY broad_sector;

-- 10. Latest Stock Prices
SELECT company_id, date, close_price
FROM stock_prices
ORDER BY date DESC
LIMIT 20;