-- 10 analytical queries for the mutual fund DB

-- 1. Top 5 funds by latest AUM
SELECT amfi_code, MAX(as_on) as latest_date, SUM(aum) as aum_total
FROM fact_aum
GROUP BY amfi_code
ORDER BY aum_total DESC
LIMIT 5;

-- 2. Average NAV per month (amfi_code, year, month)
SELECT amfi_code, strftime('%Y', date) as year, strftime('%m', date) as month, AVG(nav) as avg_nav
FROM fact_nav
GROUP BY amfi_code, year, month
ORDER BY amfi_code, year, month;

-- 3. SIP YoY growth: total SIP amount per year
SELECT strftime('%Y', date) as year, SUM(amount) as sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year
ORDER BY year;

-- 4. Transactions by state
SELECT state, COUNT(*) as txn_count, SUM(amount) as total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- 5. Funds with expense_ratio < 1%
SELECT amfi_code, expense_ratio
FROM fact_performance
WHERE expense_ratio < 1.0
ORDER BY expense_ratio ASC;

-- 6. Top 5 funds by 1Y return
SELECT amfi_code, return_1y
FROM fact_performance
ORDER BY return_1y DESC
LIMIT 5;

-- 7. Monthly NAV volatility (std dev)
SELECT amfi_code, strftime('%Y-%m', date) as ym, AVG(nav) as mean_nav,    
       (CASE WHEN COUNT(nav)>1 THEN ( (SUM((nav - AVG(nav))*(nav - AVG(nav)))/(COUNT(nav)-1)) END) as var_nav
FROM fact_nav
GROUP BY amfi_code, ym
ORDER BY amfi_code, ym;

-- 8. Redemption ratio: redemptions / total transactions per fund
SELECT amfi_code,
  SUM(CASE WHEN transaction_type='Redemption' THEN 1 ELSE 0 END)*1.0/COUNT(*) as redemption_ratio
FROM fact_transactions
GROUP BY amfi_code
ORDER BY redemption_ratio DESC;

-- 9. Average expense ratio by fund house
SELECT f.fund_house, AVG(p.expense_ratio) as avg_expense
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
GROUP BY f.fund_house
ORDER BY avg_expense ASC;

-- 10. SIP count by investor (top 10 investors)
SELECT investor_id, COUNT(*) as sip_count, SUM(amount) as total_sip
FROM fact_transactions
WHERE transaction_type='SIP'
GROUP BY investor_id
ORDER BY total_sip DESC
LIMIT 10;
