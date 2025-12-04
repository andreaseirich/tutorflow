"""
URL-Konfiguration für Core-App (Dashboard, Einnahmen).
"""
from django.urls import path
from apps.core import views

app_name = 'core'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('income/', views.IncomeOverviewView.as_view(), name='income'),
]

