"""
Tests für Rechnungsberechnung und Status-Übergänge.
"""
from django.test import TestCase
from datetime import date, time
from decimal import Decimal
from apps.students.models import Student
from apps.contracts.models import Contract
from apps.lessons.models import Lesson
from apps.billing.models import Invoice, InvoiceItem
from apps.billing.services import InvoiceService


class InvoiceCalculationTest(TestCase):
    """Tests für korrekte Rechnungsberechnung basierend auf Einheiten."""
    
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Max",
            last_name="Mustermann",
            email="max@example.com"
        )
        # Vertrag: 45 Min/Einheit, 12€/Einheit
        self.contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('12.00'),
            unit_duration_minutes=45,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            is_active=True
        )
    
    def test_invoice_calculation_90_minutes_45_unit_12_rate(self):
        """Test: 90 Min bei 45 Min/Einheit und 12€/Einheit → 24€ pro Lesson."""
        # Erstelle Lesson mit 90 Minuten
        lesson = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 15),
            start_time=time(14, 0),
            duration_minutes=90,
            status='taught'
        )
        
        # Erstelle Rechnung
        invoice = InvoiceService.create_invoice_from_lessons(
            [lesson.id],
            date(2025, 8, 1),
            date(2025, 8, 31),
            self.contract
        )
        
        # Prüfe Berechnung: 90 Min / 45 Min = 2 Einheiten, 2 * 12€ = 24€
        invoice_item = invoice.items.first()
        self.assertEqual(invoice_item.amount, Decimal('24.00'))
        self.assertEqual(invoice.total_amount, Decimal('24.00'))
    
    def test_invoice_calculation_multiple_lessons(self):
        """Test: Mehrere Lessons → Gesamtsumme korrekt."""
        # Erstelle 3 Lessons: 90 Min, 45 Min, 60 Min
        lesson1 = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 15),
            start_time=time(14, 0),
            duration_minutes=90,
            status='taught'
        )
        lesson2 = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 16),
            start_time=time(15, 0),
            duration_minutes=45,
            status='taught'
        )
        lesson3 = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 17),
            start_time=time(16, 0),
            duration_minutes=60,
            status='taught'
        )
        
        # Erstelle Rechnung
        invoice = InvoiceService.create_invoice_from_lessons(
            [lesson1.id, lesson2.id, lesson3.id],
            date(2025, 8, 1),
            date(2025, 8, 31),
            self.contract
        )
        
        # Prüfe Berechnung:
        # Lesson1: 90/45 = 2 Einheiten * 12€ = 24€
        # Lesson2: 45/45 = 1 Einheit * 12€ = 12€
        # Lesson3: 60/45 = 1.33... Einheiten * 12€ = 16€
        # Gesamt: 24 + 12 + 16 = 52€
        expected_total = Decimal('24.00') + Decimal('12.00') + (Decimal('60') / Decimal('45') * Decimal('12.00'))
        self.assertEqual(invoice.total_amount, expected_total)
        self.assertEqual(invoice.items.count(), 3)


class InvoiceStatusTransitionTest(TestCase):
    """Tests für Status-Übergänge bei Rechnungen."""
    
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Lisa",
            last_name="Müller",
            email="lisa@example.com"
        )
        self.contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('25.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            is_active=True
        )
    
    def test_lessons_set_to_paid_on_invoice_creation(self):
        """Test: Lessons werden auf PAID gesetzt beim Erstellen einer Rechnung."""
        # Erstelle Lessons mit Status TAUGHT
        lesson1 = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 15),
            start_time=time(14, 0),
            duration_minutes=60,
            status='taught'
        )
        lesson2 = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 16),
            start_time=time(15, 0),
            duration_minutes=60,
            status='taught'
        )
        
        # Erstelle Rechnung
        invoice = InvoiceService.create_invoice_from_lessons(
            [lesson1.id, lesson2.id],
            date(2025, 8, 1),
            date(2025, 8, 31),
            self.contract
        )
        
        # Prüfe, dass Lessons auf PAID gesetzt wurden
        lesson1.refresh_from_db()
        lesson2.refresh_from_db()
        self.assertEqual(lesson1.status, 'paid')
        self.assertEqual(lesson2.status, 'paid')
    
    def test_lessons_reset_to_taught_on_invoice_deletion(self):
        """Test: Lessons werden auf TAUGHT zurückgesetzt beim Löschen einer Rechnung."""
        # Erstelle Lesson und Rechnung
        lesson = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 15),
            start_time=time(14, 0),
            duration_minutes=60,
            status='taught'
        )
        
        invoice = InvoiceService.create_invoice_from_lessons(
            [lesson.id],
            date(2025, 8, 1),
            date(2025, 8, 31),
            self.contract
        )
        
        # Prüfe, dass Lesson auf PAID gesetzt wurde
        lesson.refresh_from_db()
        self.assertEqual(lesson.status, 'paid')
        
        # Lösche Rechnung
        reset_count = InvoiceService.delete_invoice(invoice)
        
        # Prüfe, dass Lesson auf TAUGHT zurückgesetzt wurde
        lesson.refresh_from_db()
        self.assertEqual(lesson.status, 'taught')
        self.assertEqual(reset_count, 1)
    
    def test_lessons_not_reset_if_in_other_invoice(self):
        """Test: Lessons werden nicht zurückgesetzt, wenn sie in anderen Rechnungen sind."""
        # Erstelle Lesson
        lesson = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 15),
            start_time=time(14, 0),
            duration_minutes=60,
            status='taught'
        )
        
        # Erstelle erste Rechnung
        invoice1 = InvoiceService.create_invoice_from_lessons(
            [lesson.id],
            date(2025, 8, 1),
            date(2025, 8, 31),
            self.contract
        )
        
        # Erstelle zweite Rechnung mit derselben Lesson (manuell, da sie bereits PAID ist)
        # In der Praxis sollte das nicht passieren, aber testen wir trotzdem
        invoice2 = Invoice.objects.create(
            payer_name=self.student.full_name,
            payer_address="",
            contract=self.contract,
            period_start=date(2025, 8, 1),
            period_end=date(2025, 8, 31),
            status='draft'
        )
        InvoiceItem.objects.create(
            invoice=invoice2,
            lesson=lesson,
            description="Test",
            date=lesson.date,
            duration_minutes=lesson.duration_minutes,
            amount=Decimal('25.00')
        )
        
        # Prüfe, dass Lesson auf PAID ist
        lesson.refresh_from_db()
        self.assertEqual(lesson.status, 'paid')
        
        # Lösche erste Rechnung
        reset_count = InvoiceService.delete_invoice(invoice1)
        
        # Prüfe, dass Lesson NICHT zurückgesetzt wurde (weil sie in invoice2 ist)
        lesson.refresh_from_db()
        self.assertEqual(lesson.status, 'paid')
        self.assertEqual(reset_count, 0)
        
        # Lösche zweite Rechnung
        reset_count = InvoiceService.delete_invoice(invoice2)
        
        # Jetzt sollte Lesson zurückgesetzt werden
        lesson.refresh_from_db()
        self.assertEqual(lesson.status, 'taught')
        self.assertEqual(reset_count, 1)

