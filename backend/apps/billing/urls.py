"""
URL-Konfiguration für Billing-App.
"""

from apps.billing import views
from django.urls import path

app_name = "billing"

urlpatterns = [
    path("", views.InvoiceListView.as_view(), name="invoice_list"),
    path("<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice_detail"),
    path("<int:pk>/delete/", views.InvoiceDeleteView.as_view(), name="invoice_delete"),
    path("create/", views.InvoiceCreateView.as_view(), name="invoice_create"),
    path(
        "<int:pk>/generate-document/",
        views.generate_invoice_document,
        name="invoice_generate_document",
    ),
    path("<int:pk>/document/", views.serve_invoice_document, name="invoice_document"),
]
