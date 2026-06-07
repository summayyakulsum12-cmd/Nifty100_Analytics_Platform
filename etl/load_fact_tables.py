import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:1234@localhost:5432/nifty100_warehouse"
)


def get_valid_symbols():
    companies = pd.read_sql(
        "SELECT symbol FROM dim_company",
        engine
    )

    return set(companies["symbol"])


def load_balance_sheet():

    df = pd.read_csv("data/clean/balancesheet.csv")

    years = pd.read_sql(
        "SELECT year_id, year_label FROM dim_year",
        engine
    )

    df = df.merge(
        years,
        left_on="year",
        right_on="year_label",
        how="left"
    )

    df["symbol"] = df["company_id"]

    valid_symbols = get_valid_symbols()

    df = df[
        df["symbol"].isin(valid_symbols)
    ]

    df = df[
        df["year_id"].notna()
    ]

    df["debt_to_equity"] = (
        df["borrowings"] /
        (df["equity_capital"] + df["reserves"])
    )

    df["equity_ratio"] = (
        (df["equity_capital"] + df["reserves"]) /
        df["total_assets"]
    )

    final_df = df[
        [
            "symbol",
            "year_id",
            "equity_capital",
            "reserves",
            "borrowings",
            "other_liabilities",
            "total_liabilities",
            "fixed_assets",
            "cwip",
            "investments",
            "other_asset",
            "total_assets",
            "debt_to_equity",
            "equity_ratio"
        ]
    ]

    final_df.to_sql(
        "fact_balance_sheet",
        engine,
        if_exists="append",
        index=False
    )

    print("Balance Sheet Loaded:", len(final_df))


def load_profit_loss():

    df = pd.read_csv("data/clean/profitandloss.csv")

    years = pd.read_sql(
        "SELECT year_id, year_label FROM dim_year",
        engine
    )

    df = df.merge(
        years,
        left_on="year",
        right_on="year_label",
        how="left"
    )

    df["symbol"] = df["company_id"]

    valid_symbols = get_valid_symbols()

    df = df[
        df["symbol"].isin(valid_symbols)
    ]

    df = df[
        df["year_id"].notna()
    ]

    df["net_profit_margin_pct"] = (
        df["net_profit"] / df["sales"]
    ) * 100

    df["expense_ratio_pct"] = (
        df["expenses"] / df["sales"]
    ) * 100

    df["interest_coverage"] = (
        df["operating_profit"] /
        df["interest"]
    )

    final_df = df[
        [
            "symbol",
            "year_id",
            "sales",
            "expenses",
            "operating_profit",
            "opm_percentage",
            "other_income",
            "interest",
            "depreciation",
            "profit_before_tax",
            "tax_percentage",
            "net_profit",
            "eps",
            "dividend_payout",
            "net_profit_margin_pct",
            "expense_ratio_pct",
            "interest_coverage"
        ]
    ]

    final_df.to_sql(
        "fact_profit_loss",
        engine,
        if_exists="append",
        index=False
    )

    print("Profit Loss Loaded:", len(final_df))


def load_cashflow():

    df = pd.read_csv("data/clean/cashflow.csv")

    years = pd.read_sql(
        "SELECT year_id, year_label FROM dim_year",
        engine
    )

    df = df.merge(
        years,
        left_on="year",
        right_on="year_label",
        how="left"
    )

    df["symbol"] = df["company_id"]

    valid_symbols = get_valid_symbols()

    df = df[
        df["symbol"].isin(valid_symbols)
    ]

    df = df[
        df["year_id"].notna()
    ]

    df["free_cash_flow"] = (
        df["operating_activity"] +
        df["investing_activity"]
    )

    final_df = df[
        [
            "symbol",
            "year_id",
            "operating_activity",
            "investing_activity",
            "financing_activity",
            "net_cash_flow",
            "free_cash_flow"
        ]
    ]

    final_df.to_sql(
        "fact_cash_flow",
        engine,
        if_exists="append",
        index=False
    )

    print("Cash Flow Loaded:", len(final_df))


def main():

    load_balance_sheet()
    load_profit_loss()
    load_cashflow()

    print("Fact Tables Loaded Successfully")


if __name__ == "__main__":
    main()