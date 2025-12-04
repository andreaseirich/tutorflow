"""
Tests für automatische Rechnungserstellung mit allen Lessons im Zeitraum.
"""
from django.test import TestCase
from datetime import date, time
from decimal import Decimal
from apps.students.models import Student
from apps.contracts.models import Contract
from apps.lessons.models import Lesson
from apps.billing.models import Invoice, InvoiceItem
from apps.billing.services import InvoiceService


class AutomaticInvoiceCreationTest(TestCase):
    """Tests für automatische Rechnungserstellung."""
    
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Max",
            last_name="Mustermann",
            email="max@example.com"
        )
        self.contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('25.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            is_active=True
        )
    
    def test_only_taught_lessons_included(self):
        """Test: Nur Lessons mit Status TAUGHT werden in Rechnung aufgenommen."""
        # Erstelle Lessons mit verschiedenen Status
        taught_lesson = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 15),
            start_time=time(14, 0),
            duration_minutes=60,
            status='taught'
        )
        planned_lesson = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 16),
            start_time=time(15, 0),
            duration_minutes=60,
            status='planned'
        )
        paid_lesson = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 17),
            start_time=time(16, 0),
            duration_minutes=60,
            status='paid'
        )
        
        # Erstelle Rechnung
        invoice = InvoiceService.create_invoice_from_lessons(
            date(2025, 8, 1),
            date(2025, 8, 31),
            self.contract
        )
        
        # Nur TAUGHT Lesson sollte in Rechnung sein
        self.assertEqual(invoice.items.count(), 1)
        self.assertEqual(invoice.items.first().lesson, taught_lesson)
        self.assertNotIn(planned_lesson, [item.lesson for item in invoice.items.all() if item.lesson])
        self.assertNotIn(paid_lesson, [item.lesson for item in invoice.items.all() if item.lesson])
    
    def test_all_taught_lessons_in_period_included(self):
        """Test: Alle TAUGHT Lessons im Zeitraum werden automatisch aufgenommen."""
        # Erstelle mehrere TAUGHT Lessons
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
        lesson3 = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 17),
            start_time=time(16, 0),
            duration_minutes=60,
            status='taught'
        )
        
        # Erstelle Rechnung
        invoice = InvoiceService.create_invoice_from_lessons(
            date(2025, 8, 1),
            date(2025, 8, 31),
            self.contract
        )
        
        # Alle drei Lessons sollten in Rechnung sein
        self.assertEqual(invoice.items.count(), 3)
        lesson_ids = [item.lesson_id for item in invoice.items.all() if item.lesson_id]
        self.assertIn(lesson1.id, lesson_ids)
        self.assertIn(lesson2.id, lesson_ids)
        self.assertIn(lesson3.id, lesson_ids)
    
    def test_lesson_cannot_be_in_multiple_invoices(self):
        """Test: Eine Lesson kann nicht in zwei Rechnungen landen."""
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
            date(2025, 8, 1),
            date(2025, 8, 31),
            self.contract
        )
        
        # Prüfe, dass Lesson in erster Rechnung ist
        self.assertEqual(invoice1.items.count(), 1)
        self.assertEqual(invoice1.items.first().lesson, lesson)
        
        # Versuche zweite Rechnung zu erstellen
        # Lesson sollte nicht mehr in get_billable_lessons erscheinen
        billable = InvoiceService.get_billable_lessons(
            date(2025, 8, 1),
            date(2025, 8, 31),
            self.contract.id
        )
        
        self.assertNotIn(lesson, billable)
        
        # Zweite Rechnung sollte leer sein
        try:
            invoice2 = InvoiceService.create_invoice_from_lessons(
                date(2025, 8, 1),
                date(2025, 8, 31),
                self.contract
            )
            # Sollte ValueError werfen oder leer sein
            self.assertEqual(invoice2.items.count(), 0)
        except ValueError:
            # Erwartetes Verhalten: ValueError wenn keine Lessons gefunden
            pass
    
    def test_lessons_set_to_paid_on_invoice_creation(self):
        """Test: Lessons werden auf PAID gesetzt beim Erstellen einer Rechnung."""
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
        lesson = Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 15),
            start_time=time(14, 0),
            duration_minutes=60,
            status='taught'
        )
        
        # Erstelle Rechnung
        invoice = InvoiceService.create_invoice_from_lessons(
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
    
    def test_get_billable_lessons_excludes_already_invoiced(self):
        """Test: get_billable_lessons schließt Lessons aus, die bereits in einer Rechnung sind."""
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
        
        # Erstelle Rechnung mit lesson1
        invoice = InvoiceService.create_invoice_from_lessons(
            date(2025, 8, 1),
            date(2025, 8, 31),
            self.contract
        )
        
        # get_billable_lessons sollte nur lesson2 zurückgeben (lesson1 ist bereits in Rechnung)
        billable = InvoiceService.get_billable_lessons(
            date(2025, 8, 1),
            date(2025, 8, 31),
            self.contract.id
        )
        
        # lesson1 sollte nicht mehr in billable sein
        self.assertNotIn(lesson1, billable)
        # lesson2 sollte noch in billable sein (wenn invoice nur lesson1 enthält)
        # Aber da automatisch alle Lessons aufgenommen werden, sind beide in invoice
        # Also sollte billable leer sein
        self.assertEqual(billable.count(), 0)

