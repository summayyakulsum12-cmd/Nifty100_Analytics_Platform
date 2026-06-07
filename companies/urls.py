from django.urls import path

from admin_insights import views
from .views import (
    company_peers,
    home,
    companies_page,
    company_page,
    company_list,
    company_detail,
    company_charts,
    company_forecast,
    screener_page
)
from companies import views

urlpatterns = [

    # Website Pages
    path("home/", home),
    path("companies-page/", companies_page),
    path("company/<str:symbol>/", company_page),
    path("screener/", screener_page),
    path("compare/",views.compare_page,name="compare"),
    path("api/v1/compare/",views.compare_api,name="compare_api"),
    # APIs
    path("", company_list),
    path("<str:symbol>/", company_detail),
    path("<str:symbol>/charts/", company_charts),
    path("<str:symbol>/peers/", company_peers),
    path("<str:symbol>/forecast/", company_forecast),
    path("screener/", screener_page),
    
]