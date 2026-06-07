import pandas as pd

def load_raw_tables():

    tables = {
        "companies": pd.read_excel(
            "data/raw/companies.xlsx",
            header=1
        ),

        "analysis": pd.read_excel(
            "data/raw/analysis.xlsx",
            header=1
        ),

        "balancesheet": pd.read_excel(
            "data/raw/balancesheet.xlsx",
            header=1
        ),

        "profitandloss": pd.read_excel(
            "data/raw/profitandloss.xlsx",
            header=1
        ),

        "cashflow": pd.read_excel(
            "data/raw/cashflow.xlsx",
            header=1
        ),

        "prosandcons": pd.read_excel(
            "data/raw/prosandcons.xlsx",
            header=1
        ),

        "documents": pd.read_excel(
            "data/raw/documents.xlsx",
            header=1
        )
    }

    return tables
def clean_companies(df):

    text_cols = [
        "company_name",
        "about_company",
        "website"
    ]

    for col in text_cols:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace("\r", "")
                .str.replace("\n", "")
            )

    return df
import re

def standardize_year(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if re.match(r"^\d{4}$", value):
        return f"Mar {value}"

    if re.match(r"^[A-Za-z]{3}-\d{2}$", value):

        month, year = value.split("-")

        year = int(year)

        if year < 50:
            year += 2000
        else:
            year += 1900

        return f"{month} {year}"

    return value
def create_year_flags(df):

    if "year" not in df.columns:
        return df

    df["is_ttm"] = (
        df["year"]
        .astype(str)
        .str.contains("TTM", case=False)
    )

    df["is_half_year"] = (
        df["year"]
        .astype(str)
        .str.contains("2024.5")
    )

    df["is_9_month"] = (
        df["year"]
        .astype(str)
        .str.contains("9m")
    )

    df["is_15_month"] = (
        df["year"]
        .astype(str)
        .str.contains("15")
    )

    return df

def clean_year_column(df):

    if "year" not in df.columns:
        return df

    df["year"] = (
        df["year"]
        .apply(standardize_year)
    )

    return df
import os

def save_clean_tables(tables):

    os.makedirs(
        "data/clean",
        exist_ok=True
    )

    for name, df in tables.items():

        path = f"data/clean/{name}.csv"

        df.to_csv(
            path,
            index=False
        )

        print(f"Saved: {path}")


def main():

    tables = load_raw_tables()

    tables["companies"] = clean_companies(
        tables["companies"]
    )

    for table in [
        "balancesheet",
        "profitandloss",
        "cashflow"
    ]:

        tables[table] = clean_year_column(
            tables[table]
        )

        tables[table] = create_year_flags(
            tables[table]
        )

    save_clean_tables(tables)


if __name__ == "__main__":
    main()