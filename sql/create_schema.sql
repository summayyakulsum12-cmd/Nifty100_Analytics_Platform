CREATE TABLE dim_company (
    symbol VARCHAR(30) PRIMARY KEY,
    company_name TEXT,
    sector VARCHAR(100),
    sub_sector VARCHAR(100),
    website TEXT,
    face_value NUMERIC,
    book_value NUMERIC,
    roce_percentage NUMERIC,
    roe_percentage NUMERIC
);

CREATE TABLE dim_year (
    year_id SERIAL PRIMARY KEY,
    year_label VARCHAR(50) UNIQUE,
    fiscal_year INT,
    is_ttm BOOLEAN DEFAULT FALSE,
    is_half_year BOOLEAN DEFAULT FALSE,
    is_9_month BOOLEAN DEFAULT FALSE,
    is_15_month BOOLEAN DEFAULT FALSE
);

CREATE TABLE fact_profit_loss (

    id SERIAL PRIMARY KEY,

    symbol VARCHAR(30),
    year_id INT,

    sales NUMERIC,
    expenses NUMERIC,
    operating_profit NUMERIC,
    opm_percentage NUMERIC,

    other_income NUMERIC,
    interest NUMERIC,
    depreciation NUMERIC,

    profit_before_tax NUMERIC,
    tax_percentage NUMERIC,

    net_profit NUMERIC,
    eps NUMERIC,
    dividend_payout NUMERIC,

    net_profit_margin_pct NUMERIC,
    expense_ratio_pct NUMERIC,
    interest_coverage NUMERIC,

    FOREIGN KEY (symbol)
    REFERENCES dim_company(symbol),

    FOREIGN KEY (year_id)
    REFERENCES dim_year(year_id)
);

CREATE TABLE fact_balance_sheet (

    id SERIAL PRIMARY KEY,

    symbol VARCHAR(30),
    year_id INT,

    equity_capital NUMERIC,
    reserves NUMERIC,
    borrowings NUMERIC,
    other_liabilities NUMERIC,
    total_liabilities NUMERIC,

    fixed_assets NUMERIC,
    cwip NUMERIC,
    investments NUMERIC,
    other_asset NUMERIC,
    total_assets NUMERIC,

    debt_to_equity NUMERIC,
    equity_ratio NUMERIC,

    FOREIGN KEY (symbol)
    REFERENCES dim_company(symbol),

    FOREIGN KEY (year_id)
    REFERENCES dim_year(year_id)
);

CREATE TABLE fact_cash_flow (

    id SERIAL PRIMARY KEY,

    symbol VARCHAR(30),
    year_id INT,

    operating_activity NUMERIC,
    investing_activity NUMERIC,
    financing_activity NUMERIC,

    net_cash_flow NUMERIC,
    free_cash_flow NUMERIC,

    FOREIGN KEY (symbol)
    REFERENCES dim_company(symbol),

    FOREIGN KEY (year_id)
    REFERENCES dim_year(year_id)
);
CREATE TABLE dim_sector(
    sector_id SERIAL PRIMARY KEY,
    sector_name VARCHAR(100) UNIQUE
);

CREATE TABLE fact_analysis(
    id SERIAL PRIMARY KEY,

    symbol VARCHAR(30),
    year_id INT,

    sales_growth NUMERIC,
    profit_growth NUMERIC,

    roe NUMERIC,
    roa NUMERIC,

    asset_turnover NUMERIC,

    cash_conversion_ratio NUMERIC,

    FOREIGN KEY(symbol)
        REFERENCES dim_company(symbol),

    FOREIGN KEY(year_id)
        REFERENCES dim_year(year_id)
);

CREATE TABLE fact_ml_scores(
    id SERIAL PRIMARY KEY,

    symbol VARCHAR(30),
    year_id INT,

    profitability_score NUMERIC,
    growth_score NUMERIC,
    leverage_score NUMERIC,
    cashflow_score NUMERIC,
    dividend_score NUMERIC,

    final_score NUMERIC,

    health_label VARCHAR(20),

    FOREIGN KEY(symbol)
        REFERENCES dim_company(symbol),

    FOREIGN KEY(year_id)
        REFERENCES dim_year(year_id)
);

CREATE TABLE fact_pros_cons(
    id SERIAL PRIMARY KEY,

    symbol VARCHAR(30),

    statement TEXT,

    type VARCHAR(10),

    FOREIGN KEY(symbol)
        REFERENCES dim_company(symbol)
);