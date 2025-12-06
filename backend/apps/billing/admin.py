"""
Admin-Konfiguration für Billing-App.
"""

from apps.billing.models import Invoice, InvoiceItem
from django.contrib import admin


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "payer_name",
        "period_start",
        "period_end",
        "total_amount",
        "status",
        "created_at",
    ]
    list_filter = ["status", "created_at", "period_start"]
    search_fields = ["payer_name", "payer_address"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ["id", "invoice", "description", "date", "amount"]
    list_filter = ["date", "invoice"]
    search_fields = ["description"]
    raw_id_fields = ["invoice", "lesson"]
