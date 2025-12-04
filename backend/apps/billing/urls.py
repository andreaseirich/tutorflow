"""
URL-Konfiguration für Billing-App.
"""
from django.urls import path
from apps.billing import views

app_name = 'billing'

urlpatterns = [
    path('', views.InvoiceListView.as_view(), name='invoice_list'),
    path('<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('create/', views.InvoiceCreateView.as_view(), name='invoice_create'),
    path('<int:pk>/generate-document/', views.generate_invoice_document, name='invoice_generate_document'),
]

