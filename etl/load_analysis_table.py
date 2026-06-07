import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:1234@localhost:5432/nifty100_warehouse"
)

# -----------------------------
# Load tables
# -----------------------------

pl = pd.read_sql(
    """
    SELECT *
    FROM fact_profit_loss
    """,
    engine
)

bs = pd.read_sql(
    """
    SELECT *
    FROM fact_balance_sheet
    """,
    engine
)

cf = pd.read_sql(
    """
    SELECT *
    FROM fact_cash_flow
    """,
    engine
)

# -----------------------------
# Merge
# -----------------------------

df = pl.merge(
    bs,
    on=["symbol", "year_id"]
)

df = df.merge(
    cf,
    on=["symbol", "year_id"]
)

# -----------------------------
# ROA
# -----------------------------

df["roa"] = (
    df["net_profit"] /
    df["total_assets"]
) * 100

# -----------------------------
# Asset Turnover
# -----------------------------

df["asset_turnover"] = (
    df["sales"] /
    df["total_assets"]
)

# -----------------------------
# Cash Conversion Ratio
# -----------------------------

df["cash_conversion_ratio"] = (
    df["operating_activity"] /
    df["net_profit"]
)

# -----------------------------
# YoY Growth
# -----------------------------

df = df.sort_values(
    ["symbol", "year_id"]
)

df["sales_growth"] = (
    df.groupby("symbol")["sales"]
    .pct_change() * 100
)

df["profit_growth"] = (
    df.groupby("symbol")["net_profit"]
    .pct_change() * 100
)

# -----------------------------
# ROE
# -----------------------------

df["roe"] = (
    df["net_profit"] /
    (
        df["equity_capital"] +
        df["reserves"]
    )
) * 100

# -----------------------------
# Final
# -----------------------------

final_df = df[
    [
        "symbol",
        "year_id",
        "sales_growth",
        "profit_growth",
        "roe",
        "roa",
        "asset_turnover",
        "cash_conversion_ratio"
    ]
]

final_df = final_df.fillna(0)

# -----------------------------
# Load
# -----------------------------

final_df.to_sql(
    "fact_analysis",
    engine,
    if_exists="append",
    index=False
)

print(
    "Analysis Records Loaded:",
    len(final_df)
)