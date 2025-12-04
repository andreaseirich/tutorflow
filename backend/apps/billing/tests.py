"""
Tests für Billing-App.
"""
from django.test import TestCase
from datetime import date, time, timedelta
from decimal import Decimal
from django.utils import timezone
from apps.students.models import Student
from apps.contracts.models import Contract
from apps.lessons.models import Lesson
from apps.billing.models import Invoice, InvoiceItem
from apps.billing.services import InvoiceService


class InvoiceModelTest(TestCase):
    """Tests für Invoice Model."""
    
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Lisa",
            last_name="Müller",
            email="lisa@example.com"
        )
        self.contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('30.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            is_active=True
        )
    
    def test_create_invoice(self):
        """Test: Erstellen einer Invoice."""
        invoice = Invoice.objects.create(
            payer_name="Test Payer",
            payer_address="Test Street 1",
            contract=self.contract,
            period_start=date(2025, 1, 1),
            period_end=date(2025, 1, 31),
            status='draft',
            total_amount=Decimal('100.00')
        )
        
        self.assertEqual(invoice.payer_name, "Test Payer")
        self.assertEqual(invoice.total_amount, Decimal('100.00'))
        self.assertEqual(invoice.status, 'draft')
    
    def test_invoice_calculate_total(self):
        """Test: calculate_total() berechnet Gesamtbetrag korrekt."""
        invoice = Invoice.objects.create(
            payer_name="Test Payer",
            period_start=date(2025, 1, 1),
            period_end=date(2025, 1, 31)
        )
        
        InvoiceItem.objects.create(
            invoice=invoice,
            description="Item 1",
            date=date(2025, 1, 5),
            duration_minutes=60,
            amount=Decimal('30.00')
        )
        InvoiceItem.objects.create(
            invoice=invoice,
            description="Item 2",
            date=date(2025, 1, 10),
            duration_minutes=60,
            amount=Decimal('30.00')
        )
        
        invoice.calculate_total()
        
        self.assertEqual(invoice.total_amount, Decimal('60.00'))


class InvoiceServiceTest(TestCase):
    """Tests für InvoiceService."""
    
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Tom",
            last_name="Weber",
            email="tom@example.com"
        )
        self.contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('25.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            is_active=True
        )
    
    def test_get_billable_lessons(self):
        """Test: get_billable_lessons gibt nur TAUGHT Lessons ohne Invoice zurück."""
        period_start = date(2025, 1, 1)
        period_end = date(2025, 1, 31)
        
        # Erstelle Lessons
        lesson1 = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 1, 5),
            start_time=time(14, 0),
            duration_minutes=60,
            status='taught'
        )
        lesson2 = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 1, 10),
            start_time=time(15, 0),
            duration_minutes=60,
            status='taught'
        )
        # Lesson mit Status PLANNED sollte nicht erscheinen
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 1, 15),
            start_time=time(16, 0),
            duration_minutes=60,
            status='planned'
        )
        
        billable = InvoiceService.get_billable_lessons(period_start, period_end, None)
        
        self.assertEqual(billable.count(), 2)
        self.assertIn(lesson1, billable)
        self.assertIn(lesson2, billable)
    
    def test_create_invoice_from_lessons(self):
        """Test: create_invoice_from_lessons erstellt Invoice mit Items."""
        period_start = date(2025, 1, 1)
        period_end = date(2025, 1, 31)
        
        lesson1 = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 1, 5),
            start_time=time(14, 0),
            duration_minutes=60,
            status='taught'
        )
        lesson2 = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 1, 10),
            start_time=time(15, 0),
            duration_minutes=60,
            status='taught'
        )
        
        invoice = InvoiceService.create_invoice_from_lessons(
            [lesson1.id, lesson2.id],
            period_start,
            period_end,
            self.contract
        )
        
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.items.count(), 2)
        # Berechnung: 60 Min / 60 Min = 1 Einheit, 1 * 25€ = 25€ pro Lesson
        # 2 Lessons = 2 * 25€ = 50€
        self.assertEqual(invoice.total_amount, Decimal('50.00'))
        
        # Prüfe, dass Lessons auf PAID gesetzt wurden
        lesson1.refresh_from_db()
        lesson2.refresh_from_db()
        self.assertEqual(lesson1.status, 'paid')
        self.assertEqual(lesson2.status, 'paid')
    
    def test_invoice_items_persist_lesson_data(self):
        """Test: InvoiceItems behalten Lesson-Daten auch wenn Lesson gelöscht wird."""
        lesson = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 1, 5),
            start_time=time(14, 0),
            duration_minutes=60,
            status='taught'
        )
        
        invoice = InvoiceService.create_invoice_from_lessons(
            [lesson.id],
            date(2025, 1, 1),
            date(2025, 1, 31),
            self.contract
        )
        
        item = invoice.items.first()
        self.assertEqual(item.date, date(2025, 1, 5))
        self.assertEqual(item.duration_minutes, 60)
        
        # Lösche Lesson
        lesson.delete()
        
        # Item sollte noch existieren
        item.refresh_from_db()
        self.assertEqual(item.date, date(2025, 1, 5))
        self.assertIsNone(item.lesson)
