"""
Tests für Kalender-Datum-Synchronisation.
"""
from django.test import TestCase
from datetime import date, time
from decimal import Decimal
from django.utils import timezone
from apps.students.models import Student
from apps.contracts.models import Contract
from apps.lessons.views import LessonCreateView, CalendarView
from django.test import RequestFactory


class CalendarDateAlignmentTest(TestCase):
    """Tests für Kalender-Monatsname und Default-Datum-Synchronisation."""
    
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Test",
            last_name="Student",
            email="test@example.com"
        )
        self.contract = Contract.objects.create(
            student=self.student,
            hourly_rate=Decimal('25.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            is_active=True
        )
        self.factory = RequestFactory()
    
    def test_calendar_view_shows_correct_month_name(self):
        """Test: CalendarView zeigt korrekten Monatsnamen für angegebenen Monat."""
        request = self.factory.get('/lessons/calendar/?year=2025&month=8')
        view = CalendarView()
        view.request = request
        view.setup(request)
        
        context = view.get_context_data()
        
        self.assertEqual(context['year'], 2025)
        self.assertEqual(context['month'], 8)
        # Prüfe, dass Monatsname korrekt ist (August ist Index 8)
        self.assertEqual(context['month_names'][8], 'August')
    
    def test_create_view_uses_date_parameter(self):
        """Test: LessonCreateView verwendet date-Parameter für initiales Datum."""
        request = self.factory.get('/lessons/create/?date=2025-08-25&year=2025&month=8')
        view = LessonCreateView()
        view.request = request
        view.setup(request)
        
        initial = view.get_initial()
        
        self.assertEqual(initial['date'], date(2025, 8, 25))
    
    def test_create_view_uses_year_month_for_redirect(self):
        """Test: Create-View verwendet year/month aus Request für Redirect."""
        request = self.factory.get('/lessons/create/?date=2025-08-25&year=2025&month=8')
        view = LessonCreateView()
        view.request = request
        view.setup(request)
        
        # Simuliere gespeicherte Lesson
        from apps.lessons.models import Lesson
        lesson = Lesson(
            contract=self.contract,
            date=date(2025, 8, 25),
            start_time=time(14, 0),
            duration_minutes=60
        )
        view.object = lesson
        
        success_url = view.get_success_url()
        
        # URL sollte year=2025&month=8 enthalten
        self.assertIn('year=2025', success_url)
        self.assertIn('month=8', success_url)

