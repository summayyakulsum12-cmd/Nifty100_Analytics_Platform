import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine(
    "postgresql://postgres:1234@localhost:5432/nifty100_warehouse"
)
def load_companies():

    df = pd.read_excel(
        "data/raw/companies.xlsx",
        header=1
    )

    company_df = pd.DataFrame({
        "symbol": df["id"],
        "company_name": df["company_name"],
        "website": df["website"],
        "face_value": df["face_value"],
        "book_value": df["book_value"],
        "roce_percentage": df["roce_percentage"],
        "roe_percentage": df["roe_percentage"]
    })

    company_df.to_sql(
        "dim_company",
        engine,
        if_exists="append",
        index=False
    )

    print("Companies Loaded:", len(company_df))

def load_years():

    years = set()

    for file in [
        "balancesheet",
        "profitandloss",
        "cashflow"
    ]:

        df = pd.read_csv(
            f"data/clean/{file}.csv"
        )

        years.update(
            df["year"].dropna().unique()
        )

    year_df = pd.DataFrame({
        "year_label": sorted(list(years))
    })

    year_df["fiscal_year"] = (
        year_df["year_label"]
        .str.extract(r'(\d{4})')
        .astype(float)
    )

    year_df.to_sql(
        "dim_year",
        engine,
        if_exists="append",
        index=False
    )

    print("Years Loaded:", len(year_df))
def clear_tables():

    with engine.begin() as conn:

        conn.execute(
            text("TRUNCATE TABLE dim_company CASCADE")
        )

        conn.execute(
            text("TRUNCATE TABLE dim_year CASCADE")
        )
        
def main():

    clear_tables()

    load_companies()

    load_years()

    print("Warehouse Load Complete")


if __name__ == "__main__":
    main()