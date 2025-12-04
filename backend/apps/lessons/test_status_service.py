"""
Tests für LessonStatusService.
"""
from django.test import TestCase
from datetime import date, time, timedelta
from decimal import Decimal
from django.utils import timezone
from apps.students.models import Student
from apps.contracts.models import Contract
from apps.lessons.models import Lesson
from apps.lessons.status_service import LessonStatusService


class LessonStatusServiceTest(TestCase):
    """Tests für LessonStatusService."""
    
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
    
    def test_update_status_past_lesson_to_taught(self):
        """Test: Vergangene Lesson mit Status PLANNED wird auf TAUGHT gesetzt."""
        past_date = timezone.localdate() - timedelta(days=5)
        past_time = time(14, 0)
        
        lesson = Lesson.objects.create(
            contract=self.contract,
            date=past_date,
            start_time=past_time,
            duration_minutes=60,
            status='planned'
        )
        
        status_changed = LessonStatusService.update_status_for_lesson(lesson)
        
        self.assertTrue(status_changed)
        lesson.refresh_from_db()
        self.assertEqual(lesson.status, 'taught')
    
    def test_update_status_future_lesson_to_planned(self):
        """Test: Zukünftige Lesson ohne Status wird auf PLANNED gesetzt."""
        future_date = timezone.localdate() + timedelta(days=5)
        future_time = time(14, 0)
        
        lesson = Lesson.objects.create(
            contract=self.contract,
            date=future_date,
            start_time=future_time,
            duration_minutes=60,
            status=''  # Leerer Status
        )
        
        status_changed = LessonStatusService.update_status_for_lesson(lesson)
        
        self.assertTrue(status_changed)
        lesson.refresh_from_db()
        self.assertEqual(lesson.status, 'planned')
    
    def test_update_status_paid_not_overwritten(self):
        """Test: Status PAID wird nicht überschrieben."""
        past_date = timezone.localdate() - timedelta(days=5)
        
        lesson = Lesson.objects.create(
            contract=self.contract,
            date=past_date,
            start_time=time(14, 0),
            duration_minutes=60,
            status='paid'
        )
        
        status_changed = LessonStatusService.update_status_for_lesson(lesson)
        
        self.assertFalse(status_changed)
        lesson.refresh_from_db()
        self.assertEqual(lesson.status, 'paid')
    
    def test_update_status_cancelled_not_overwritten(self):
        """Test: Status CANCELLED wird nicht überschrieben."""
        past_date = timezone.localdate() - timedelta(days=5)
        
        lesson = Lesson.objects.create(
            contract=self.contract,
            date=past_date,
            start_time=time(14, 0),
            duration_minutes=60,
            status='cancelled'
        )
        
        status_changed = LessonStatusService.update_status_for_lesson(lesson)
        
        self.assertFalse(status_changed)
        lesson.refresh_from_db()
        self.assertEqual(lesson.status, 'cancelled')
    
    def test_bulk_update_past_lessons(self):
        """Test: bulk_update_past_lessons aktualisiert mehrere Lessons."""
        past_date = timezone.localdate() - timedelta(days=10)
        
        # Erstelle mehrere vergangene Lessons
        for i in range(3):
            Lesson.objects.create(
                contract=self.contract,
                date=past_date - timedelta(days=i),
                start_time=time(14, 0),
                duration_minutes=60,
                status='planned'
            )
        
        updated_count = LessonStatusService.bulk_update_past_lessons()
        
        self.assertEqual(updated_count, 3)
        
        # Prüfe, dass alle auf TAUGHT gesetzt wurden
        lessons = Lesson.objects.filter(date__lte=past_date, status='taught')
        self.assertEqual(lessons.count(), 3)

