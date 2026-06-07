from django.http import JsonResponse
from httpx import request
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql+psycopg2://postgres:1234@localhost:5432/nifty100_warehouse"
)


def company_list(request):

    query = """
    SELECT *
    FROM dim_company
    ORDER BY symbol
    """

    df = pd.read_sql(query, engine)

    return JsonResponse(
        df.to_dict(orient="records"),
        safe=False
    )

def company_detail(request, symbol):

    company = pd.read_sql(
        f"""
        SELECT *
        FROM dim_company
        WHERE symbol='{symbol}'
        """,
        engine
    )

    profit = pd.read_sql(
        f"""
        SELECT *
        FROM fact_profit_loss
        WHERE symbol='{symbol}'
        ORDER BY year_id
        """,
        engine
    )

    balance = pd.read_sql(
        f"""
        SELECT *
        FROM fact_balance_sheet
        WHERE symbol='{symbol}'
        ORDER BY year_id
        """,
        engine
    )

    cashflow = pd.read_sql(
        f"""
        SELECT *
        FROM fact_cash_flow
        WHERE symbol='{symbol}'
        ORDER BY year_id
        """,
        engine
    )

    score = pd.read_sql(
        f"""
        SELECT *
        FROM fact_ml_scores
        WHERE symbol='{symbol}'
        ORDER BY year_id DESC
        LIMIT 1
        """,
        engine
    )

    return JsonResponse({
        "company": company.to_dict(orient="records"),
        "profit_loss": profit.to_dict(orient="records"),
        "balance_sheet": balance.to_dict(orient="records"),
        "cash_flow": cashflow.to_dict(orient="records"),
        "health_score": score.to_dict(orient="records")
    })

def company_charts(request, symbol):

    df = pd.read_sql(
        f"""
        SELECT
            year_id,
            sales,
            net_profit,
            opm_percentage,
            eps,
            dividend_payout
        FROM fact_profit_loss
        WHERE symbol='{symbol}'
        ORDER BY year_id
        """,
        engine
    )
    df = df.fillna(0)
    debt = pd.read_sql(
        f"""
        SELECT
            year_id,
            borrowings,
            debt_to_equity
        FROM fact_balance_sheet
        WHERE symbol='{symbol}'
        ORDER BY year_id
        """,
        engine
    )
    debt = debt.fillna(0)

    cashflow = pd.read_sql(
        f"""
        SELECT
            year_id,
            operating_activity,
            investing_activity,
            financing_activity,
            free_cash_flow
        FROM fact_cash_flow
        WHERE symbol='{symbol}'
        ORDER BY year_id
        """,
        engine
    )
    cashflow = cashflow.fillna(0)

    balance = pd.read_sql(
        f"""
        SELECT
            year_id,
            debt_to_equity,
            equity_ratio
        FROM fact_balance_sheet
        WHERE symbol='{symbol}'
        ORDER BY year_id
        """,
        engine
    )
    balance = balance.fillna(0) 

    return JsonResponse({
        "financials": df.to_dict(orient="records"),
        "debt": debt.to_dict(orient="records"),
        "cashflow": cashflow.to_dict(orient="records"),
        "balance": balance.to_dict(orient="records")
    })

from django.shortcuts import render

def home(request):

    company_count = pd.read_sql(
        """
        SELECT COUNT(*) AS total
        FROM dim_company
        """,
        engine
    ).iloc[0]["total"]

    profit_count = pd.read_sql(
        """
        SELECT COUNT(*) AS total
        FROM fact_profit_loss
        """,
        engine
    ).iloc[0]["total"]

    balance_count = pd.read_sql(
        """
        SELECT COUNT(*) AS total
        FROM fact_balance_sheet
        """,
        engine
    ).iloc[0]["total"]

    score_count = pd.read_sql(
        """
        SELECT COUNT(*) AS total
        FROM fact_ml_scores
        """,
        engine
    ).iloc[0]["total"]
    top_health = pd.read_sql(
        """
        SELECT
            symbol,
            health_score
        FROM fact_ml_scores
        ORDER BY health_score DESC
        LIMIT 5
        """,
        engine
    )

    top_health = top_health.to_dict(
        orient="records"
    )
    

    return render(
        request,
        "home.html",
        {
            "company_count": company_count,
            "profit_count": profit_count,
            "balance_count": balance_count,
            "score_count": score_count,
            "top_health": top_health
            
        }
    )

def companies_page(request):

    df = pd.read_sql(
        """
        SELECT *
        FROM dim_company
        ORDER BY symbol
        """,
        engine
    )

    companies = df.to_dict(
        orient="records"
    )

    return render(
        request,
        "company_list.html",
        {"companies": companies}
    )

def company_page(request, symbol):

    company = pd.read_sql(
        f"""
        SELECT *
        FROM dim_company
        WHERE symbol='{symbol}'
        """,
        engine
    )

    company = company.iloc[0].to_dict()

    score = pd.read_sql(
        f"""
        SELECT *
        FROM fact_ml_scores
        WHERE symbol='{symbol}'
        ORDER BY year_id DESC
        LIMIT 1
        """,
        engine
    )

    if len(score) > 0:
        score = score.iloc[0].to_dict()
    else:
        score = {}

    return render(
        request,
        "company_detail.html",
        {
            "company": company,
            "score": score
        }
    )

def company_peers(request, symbol):

    peers = pd.read_sql(
        f"""
        SELECT
            peer_symbol,
            peer_rank,
            similarity_score
        FROM fact_peers
        WHERE symbol='{symbol}'
        ORDER BY peer_rank
        """,
        engine
    )

    peers = peers.fillna(0)

    return JsonResponse(
        peers.to_dict(orient="records"),
        safe=False
    )

def company_forecast(request, symbol):

    forecast = pd.read_sql(
        f"""
        SELECT
            year_id,
            trend_slope,
            trend_label,
            forecast_sales
        FROM fact_forecasts
        WHERE symbol='{symbol}'
        """,
        engine
    )

    forecast = forecast.fillna(0)

    return JsonResponse(
        forecast.to_dict(orient="records"),
        safe=False
    )

def screener_page(request):

    df = pd.read_sql(
    """
    SELECT
        m.symbol,
        m.health_score,
        m.health_label,
        a.roe,
        b.debt_to_equity

    FROM fact_ml_scores m

    LEFT JOIN fact_analysis a
        ON m.symbol = a.symbol
        AND m.year_id = a.year_id

    LEFT JOIN fact_balance_sheet b
        ON m.symbol = b.symbol
        AND m.year_id = b.year_id

    WHERE m.year_id = (
        SELECT MAX(m2.year_id)
        FROM fact_ml_scores m2
        WHERE m2.symbol = m.symbol
    )

    ORDER BY m.health_score DESC
    """,
    engine
)
    df["health_score"] = df["health_score"].fillna(0)
    df["roe"] = df["roe"].fillna(0)
    df["debt_to_equity"] = df["debt_to_equity"].fillna(0)

    companies = df.to_dict(
        orient="records"
    )


    return render(
        request,
        "screener.html",
        {
            "companies": companies
        }
    )
def compare_page(request):

    companies = pd.read_sql(
        """
        SELECT symbol
        FROM dim_company
        ORDER BY symbol
        """,
        engine
    )

    return render(
        request,
        "compare.html",
        {
            "companies":
            companies.to_dict(
                orient="records"
            )
        }
    )
def compare_api(request):

    stock1 = request.GET.get("stock1")
    stock2 = request.GET.get("stock2")

    query = f"""
    SELECT
        m.symbol,
        m.health_score,
        m.health_label,
        a.roe,
        b.debt_to_equity,
        p.sales,
        p.net_profit

    FROM fact_ml_scores m

    LEFT JOIN fact_analysis a
        ON m.symbol=a.symbol
        AND m.year_id=a.year_id

    LEFT JOIN fact_balance_sheet b
        ON m.symbol=b.symbol
        AND m.year_id=b.year_id

    LEFT JOIN fact_profit_loss p
        ON m.symbol=p.symbol
        AND m.year_id=p.year_id

    WHERE m.symbol IN (
        '{stock1}',
        '{stock2}'
    )

    AND m.year_id = (
        SELECT MAX(year_id)
        FROM fact_ml_scores x
        WHERE x.symbol=m.symbol
    )
    """

    df = pd.read_sql(
        query,
        engine
    )

    df = df.fillna(0)

    return JsonResponse(
        df.to_dict(
            orient="records"
        ),
        safe=False
    )
