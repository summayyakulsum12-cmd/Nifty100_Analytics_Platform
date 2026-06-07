SELECT
    company_name,
    MAX(total_assets) AS assets
FROM vw_company_financials
GROUP BY company_name
ORDER BY assets DESC
LIMIT 10;
SELECT
    company_name,
    MAX(sales) AS sales
FROM vw_company_financials
GROUP BY company_name
ORDER BY sales DESC
LIMIT 10;
SELECT
    company_name,
    MAX(net_profit_margin_pct) AS margin
FROM vw_company_financials
GROUP BY company_name
ORDER BY margin DESC
LIMIT 10;
SELECT
    company_name,
    MAX(free_cash_flow) AS fcf
FROM vw_company_financials
GROUP BY company_name
ORDER BY fcf DESC
LIMIT 10;