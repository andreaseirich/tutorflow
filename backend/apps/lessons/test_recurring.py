"""
Tests für RecurringLesson und RecurringLessonService.
"""
from django.test import TestCase
from datetime import date, time, timedelta
from decimal import Decimal
from apps.students.models import Student
from apps.contracts.models import Contract
from apps.lessons.models import Lesson
from apps.lessons.recurring_models import RecurringLesson
from apps.lessons.recurring_service import RecurringLessonService
from apps.lessons.calendar_service import CalendarService


class RecurringLessonModelTest(TestCase):
    """Tests für RecurringLesson Model."""
    
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
            start_date=date(2025, 8, 1),
            end_date=date(2025, 12, 31),
            is_active=True
        )
    
    def test_create_recurring_lesson(self):
        """Test: Erstellen einer RecurringLesson."""
        recurring = RecurringLesson.objects.create(
            contract=self.contract,
            start_date=date(2025, 8, 25),
            start_time=time(14, 0),
            duration_minutes=60,
            monday=True,
            is_active=True
        )
        self.assertEqual(recurring.contract, self.contract)
        self.assertEqual(recurring.start_date, date(2025, 8, 25))
        self.assertTrue(recurring.monday)
        self.assertFalse(recurring.tuesday)
    
    def test_get_active_weekdays(self):
        """Test: get_active_weekdays() Methode."""
        recurring = RecurringLesson.objects.create(
            contract=self.contract,
            start_date=date(2025, 8, 25),
            start_time=time(14, 0),
            duration_minutes=60,
            monday=True,
            thursday=True,
            friday=True
        )
        weekdays = recurring.get_active_weekdays()
        self.assertEqual(set(weekdays), {0, 3, 4})  # Mo, Do, Fr


class RecurringLessonServiceTest(TestCase):
    """Tests für RecurringLessonService."""
    
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Anna",
            last_name="Schmidt",
            email="anna@example.com"
        )
        self.contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('30.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 8, 1),
            end_date=date(2025, 8, 31),
            is_active=True
        )
    
    def test_generate_lessons_single_weekday(self):
        """Test: Generierung für einen einzelnen Wochentag (Montag)."""
        recurring = RecurringLesson.objects.create(
            contract=self.contract,
            start_date=date(2025, 8, 25),  # Montag
            end_date=date(2025, 8, 31),
            start_time=time(14, 0),
            duration_minutes=60,
            monday=True
        )
        
        result = RecurringLessonService.generate_lessons(recurring, check_conflicts=False)
        
        # Sollte 1 Lesson erstellen (25.08.2025 ist ein Montag)
        self.assertEqual(result['created'], 1)
        self.assertEqual(result['skipped'], 0)
        
        # Prüfe, dass Lesson erstellt wurde
        lesson = Lesson.objects.filter(contract=self.contract, date=date(2025, 8, 25)).first()
        self.assertIsNotNone(lesson)
        self.assertEqual(lesson.start_time, time(14, 0))
    
    def test_generate_lessons_multiple_weekdays(self):
        """Test: Generierung für mehrere Wochentage (Do + Fr)."""
        recurring = RecurringLesson.objects.create(
            contract=self.contract,
            start_date=date(2025, 8, 1),  # Freitag
            end_date=date(2025, 8, 15),
            start_time=time(15, 0),
            duration_minutes=90,
            thursday=True,
            friday=True
        )
        
        result = RecurringLessonService.generate_lessons(recurring, check_conflicts=False)
        
        # Sollte mehrere Lessons erstellen (Do und Fr im Zeitraum)
        self.assertGreater(result['created'], 0)
        
        # Prüfe, dass nur Donnerstage und Freitage erstellt wurden
        lessons = Lesson.objects.filter(contract=self.contract)
        for lesson in lessons:
            weekday = lesson.date.weekday()
            self.assertIn(weekday, [3, 4])  # Do=3, Fr=4
    
    def test_generate_lessons_skips_existing(self):
        """Test: Überspringt bereits vorhandene Lessons."""
        # Erstelle manuell eine Lesson
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 8, 25),  # Montag
            start_time=time(14, 0),
            duration_minutes=60,
            status='planned'
        )
        
        recurring = RecurringLesson.objects.create(
            contract=self.contract,
            start_date=date(2025, 8, 25),
            end_date=date(2025, 8, 31),
            start_time=time(14, 0),
            duration_minutes=60,
            monday=True
        )
        
        result = RecurringLessonService.generate_lessons(recurring, check_conflicts=False)
        
        # Sollte die vorhandene Lesson überspringen
        self.assertEqual(result['skipped'], 1)
        # Sollte keine neue erstellen, da nur ein Montag im Zeitraum
        self.assertEqual(result['created'], 0)
    
    def test_generate_lessons_at_contract_boundaries(self):
        """Test: Serien, die exakt am Vertragsstart/-ende beginnen/enden."""
        recurring = RecurringLesson.objects.create(
            contract=self.contract,
            start_date=self.contract.start_date,  # Exakt Vertragsstart
            end_date=self.contract.end_date,  # Exakt Vertragsende
            start_time=time(10, 0),
            duration_minutes=60,
            monday=True,
            wednesday=True
        )
        
        result = RecurringLessonService.generate_lessons(recurring, check_conflicts=False)
        
        # Sollte Lessons erstellen
        self.assertGreater(result['created'], 0)
        
        # Prüfe, dass alle Lessons im Vertragszeitraum liegen
        lessons = Lesson.objects.filter(contract=self.contract)
        for lesson in lessons:
            self.assertGreaterEqual(lesson.date, self.contract.start_date)
            self.assertLessEqual(lesson.date, self.contract.end_date)
    
    def test_preview_lessons(self):
        """Test: Vorschau-Funktion ohne Speicherung."""
        recurring = RecurringLesson.objects.create(
            contract=self.contract,
            start_date=date(2025, 8, 25),
            end_date=date(2025, 8, 31),
            start_time=time(14, 0),
            duration_minutes=60,
            monday=True
        )
        
        preview = RecurringLessonService.preview_lessons(recurring)
        
        # Sollte Lesson-Instanzen zurückgeben
        self.assertGreater(len(preview), 0)
        # Aber nicht gespeichert sein
        self.assertEqual(Lesson.objects.filter(contract=self.contract).count(), 0)


class CalendarServiceTest(TestCase):
    """Tests für CalendarService."""
    
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Tom",
            last_name="Weber",
            email="tom@example.com"
        )
        self.contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('28.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            is_active=True
        )
    
    def test_get_calendar_data_groups_lessons(self):
        """Test: Kalenderdaten gruppieren Lessons korrekt nach Tagen."""
        # Erstelle Lessons für Januar 2025
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 1, 5),
            start_time=time(14, 0),
            duration_minutes=60,
            status='planned'
        )
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 1, 5),
            start_time=time(16, 0),
            duration_minutes=60,
            status='planned'
        )
        Lesson.objects.create(
            contract=self.contract,
            date=date(2025, 1, 10),
            start_time=time(15, 0),
            duration_minutes=60,
            status='planned'
        )
        
        calendar_data = CalendarService.get_calendar_data(2025, 1)
        
        # Prüfe Gruppierung
        self.assertIn(date(2025, 1, 5), calendar_data['lessons_by_date'])
        self.assertEqual(len(calendar_data['lessons_by_date'][date(2025, 1, 5)]), 2)
        self.assertIn(date(2025, 1, 10), calendar_data['lessons_by_date'])
        self.assertEqual(len(calendar_data['lessons_by_date'][date(2025, 1, 10)]), 1)

