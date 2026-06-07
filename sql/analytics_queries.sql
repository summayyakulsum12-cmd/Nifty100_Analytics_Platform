-- Top 10 companies by assets

SELECT
    c.company_name,
    y.year_label,
    b.total_assets
FROM fact_balance_sheet b
JOIN dim_company c
ON b.symbol = c.symbol
JOIN dim_year y
ON b.year_id = y.year_id
ORDER BY b.total_assets DESC
LIMIT 10;


-- Highest ROE companies

SELECT
    company_name,
    roe_percentage
FROM dim_company
ORDER BY roe_percentage DESC
LIMIT 10;


-- Highest Net Profit Margin

SELECT
    c.company_name,
    y.year_label,
    p.net_profit_margin_pct
FROM fact_profit_loss p
JOIN dim_company c
ON p.symbol = c.symbol
JOIN dim_year y
ON p.year_id = y.year_id
ORDER BY p.net_profit_margin_pct DESC
LIMIT 10;