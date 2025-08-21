from django.urls import path
from .views import (
    index,
    budget_sheet_list,
    budget_sheet_detail,
    budget_sheet_create,
    created_budget,
    chart_budget,
    chart_budget_month

)

app_name="gestionbudget"

urlpatterns = [
    path('', budget_sheet_list, name='budget_sheet_list'),
    path('budget_sheet_detail/<str:pid>/', budget_sheet_detail, name='budget_sheet_detail'),
    path('budget_sheet_create/', budget_sheet_create, name='budget_sheet_create'),
    path("created_budget/<str:pid>/", created_budget, name="created_budget"),
    path("chart_budget/<str:pid>/", chart_budget, name="chart_budget"),
    path("chart_budget_month/<str:pid>", chart_budget_month, name="chart_budget_month"),

]