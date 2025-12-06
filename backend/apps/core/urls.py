"""
URL-Konfiguration für Core-App (Dashboard, Einnahmen).
"""

from apps.core import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("income/", views.IncomeOverviewView.as_view(), name="income"),
]
