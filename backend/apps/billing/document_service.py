"""
Service für Rechnungsdokument-Generierung.
"""

from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.conf import settings
import os
from apps.billing.models import Invoice


class InvoiceDocumentService:
    """Service für die Generierung von Rechnungsdokumenten."""

    @staticmethod
    def generate_html_document(invoice: Invoice) -> str:
        """
        Generiert ein HTML-Dokument für eine Invoice.

        Args:
            invoice: Invoice-Instanz

        Returns:
            HTML-String
        """
        context = {
            "invoice": invoice,
            "items": invoice.items.all(),
        }

        html = render_to_string("billing/invoice_document.html", context)
        return html

    @staticmethod
    def save_document(invoice: Invoice) -> str:
        """
        Generiert und speichert das Rechnungsdokument.

        Args:
            invoice: Invoice-Instanz

        Returns:
            Pfad zum gespeicherten Dokument
        """
        html_content = InvoiceDocumentService.generate_html_document(invoice)

        # Erstelle Dateinamen
        filename = f"invoice_{invoice.id}_{invoice.period_start}_{invoice.period_end}.html"

        # Speichere als FileField
        invoice.document.save(filename, ContentFile(html_content.encode("utf-8")), save=True)

        return invoice.document.path
