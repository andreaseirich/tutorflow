"""
Tests für Formularwerte bei Rechnungsvorschau.
"""

from datetime import date, time
from decimal import Decimal

from apps.billing.views import InvoiceCreateView
from apps.contracts.models import Contract
from apps.lessons.models import Lesson
from apps.students.models import Student
from django.test import Client, RequestFactory, TestCase


class InvoicePreviewFormValuesTest(TestCase):
    """Tests für Erhaltung der Formularwerte bei Vorschau."""

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.student = Student.objects.create(
            first_name="Max", last_name="Mustermann", email="max@example.com"
        )
        self.contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal("25.00"),
            unit_duration_minutes=60,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            is_active=True,
        )

    def test_form_preserves_values_after_preview(self):
        """Test: Formularwerte bleiben nach Vorschau erhalten."""
        # Erstelle GET-Request mit Query-Parametern (wie nach Klick auf "Vorschau anzeigen")
        request = self.factory.get(
            "/billing/create/",
            {
                "period_start": "2025-08-01",
                "period_end": "2025-08-31",
                "contract": str(self.contract.pk),
            },
        )

        view = InvoiceCreateView()
        view.request = request
        view.setup(request)

        # Hole Formular
        form = view.get_form()

        # Prüfe, dass initial values gesetzt sind
        self.assertEqual(form.initial.get("period_start"), date(2025, 8, 1))
        self.assertEqual(form.initial.get("period_end"), date(2025, 8, 31))
        self.assertEqual(form.initial.get("contract"), self.contract.pk)

    def test_form_renders_with_values_in_html(self):
        """Test: Formular rendert mit Werten in HTML (value-Attribute)."""
        # Erstelle Lesson für Vorschau
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 15),
            start_time=time(14, 0),
            duration_minutes=60,
            status="taught",
        )

        # GET-Request mit Query-Parametern
        response = self.client.get(
            "/billing/create/",
            {
                "period_start": "2025-08-01",
                "period_end": "2025-08-31",
                "contract": str(self.contract.pk),
            },
        )

        # Prüfe, dass Response erfolgreich ist
        self.assertEqual(response.status_code, 200)

        # Prüfe, dass HTML die Werte enthält
        content = response.content.decode("utf-8")
        self.assertIn('value="2025-08-01"', content)
        self.assertIn('value="2025-08-31"', content)
        # Prüfe, dass der Vertrag ausgewählt ist (selected-Attribut)
        self.assertIn(f'value="{self.contract.pk}"', content)

    def test_form_preserves_values_without_contract(self):
        """Test: Formularwerte bleiben erhalten auch ohne Vertrag-Filter."""
        request = self.factory.get(
            "/billing/create/", {"period_start": "2025-08-01", "period_end": "2025-08-31"}
        )

        view = InvoiceCreateView()
        view.request = request
        view.setup(request)

        form = view.get_form()

        # Prüfe, dass Datumswerte gesetzt sind
        self.assertEqual(form.initial.get("period_start"), date(2025, 8, 1))
        self.assertEqual(form.initial.get("period_end"), date(2025, 8, 31))
        # Contract sollte nicht gesetzt sein
        self.assertIsNone(form.initial.get("contract"))

    def test_form_handles_invalid_dates_gracefully(self):
        """Test: Formular behandelt ungültige Datumswerte korrekt."""
        request = self.factory.get(
            "/billing/create/", {"period_start": "invalid-date", "period_end": "2025-08-31"}
        )

        view = InvoiceCreateView()
        view.request = request
        view.setup(request)

        form = view.get_form()

        # Ungültiges Datum sollte nicht in initial sein
        self.assertNotIn("period_start", form.initial)
        # Gültiges Datum sollte gesetzt sein
        self.assertEqual(form.initial.get("period_end"), date(2025, 8, 31))
