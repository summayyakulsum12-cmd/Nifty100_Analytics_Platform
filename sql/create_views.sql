CREATE OR REPLACE VIEW vw_company_financials AS
SELECT
    c.symbol,
    c.company_name,
    y.year_label,

    b.total_assets,
    b.borrowings,
    b.debt_to_equity,
    b.equity_ratio,

    p.sales,
    p.net_profit,
    p.net_profit_margin_pct,

    cf.operating_activity,
    cf.net_cash_flow,
    cf.free_cash_flow

FROM dim_company c

LEFT JOIN fact_balance_sheet b
ON c.symbol = b.symbol

LEFT JOIN fact_profit_loss p
ON c.symbol = p.symbol
AND b.year_id = p.year_id

LEFT JOIN fact_cash_flow cf
ON c.symbol = cf.symbol
AND b.year_id = cf.year_id

LEFT JOIN dim_year y
ON b.year_id = y.year_id;