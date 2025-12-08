"""
URL-Konfiguration für Core-App (Dashboard, Einnahmen).
"""

from apps.core import views
from apps.core.views_health import health_status
from django.urls import path

app_name = "core"

urlpatterns = [
    path("health/", health_status, name="health"),
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("income/", views.IncomeOverviewView.as_view(), name="income"),
]
