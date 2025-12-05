"""
Management Command zum Erstellen von Demo-Daten für TutorFlow.

Verwendung:
    python manage.py seed_demo_data

Erstellt:
    - 3 Schüler mit unterschiedlichen Profilen
    - Zugehörige Verträge
    - Mehrere Lessons (inkl. einem Konflikt)
    - Blockzeiten
    - 1 Premium-User mit generiertem LessonPlan
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import date, time, timedelta
from apps.locations.models import Location
from apps.students.models import Student
from apps.contracts.models import Contract
from apps.lessons.models import Lesson
from apps.blocked_times.models import BlockedTime
from apps.core.models import UserProfile
from apps.lesson_plans.models import LessonPlan


class Command(BaseCommand):
    help = 'Erstellt Demo-Daten für TutorFlow'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Löscht zuerst alle vorhandenen Daten (Vorsicht!)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Lösche vorhandene Daten...'))
            LessonPlan.objects.all().delete()
            Lesson.objects.all().delete()
            BlockedTime.objects.all().delete()
            Contract.objects.all().delete()
            Student.objects.all().delete()
            Location.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(self.style.SUCCESS('Erstelle Demo-Daten...'))
        
        # Orte
        location_home = Location.objects.create(
            name="Zuhause",
            address="Musterstraße 1, 12345 Musterstadt"
        )
        location_school = Location.objects.create(
            name="Gymnasium XY",
            address="Schulstraße 5, 12345 Musterstadt"
        )
        
        # Schüler
        student1 = Student.objects.create(
            first_name="Max",
            last_name="Mustermann",
            email="max.mustermann@example.com",
            phone="0123-456789",
            school="Gymnasium XY",
            grade="10. Klasse",
            subjects="Mathe, Physik",
            default_location=location_home,
            notes="Sehr motiviert, braucht Unterstützung bei Algebra"
        )
        
        student2 = Student.objects.create(
            first_name="Anna",
            last_name="Schmidt",
            email="anna.schmidt@example.com",
            phone="0123-456790",
            school="Realschule ABC",
            grade="9. Klasse",
            subjects="Deutsch, Englisch",
            default_location=location_school,
            notes="Gute Schülerin, möchte sich auf Abitur vorbereiten"
        )
        
        student3 = Student.objects.create(
            first_name="Tom",
            last_name="Weber",
            email="tom.weber@example.com",
            school="Gymnasium XY",
            grade="11. Klasse",
            subjects="Mathe, Chemie",
            default_location=location_home
        )
        
        # Verträge
        contract1 = Contract.objects.create(
            student=student1,
            hourly_rate=Decimal('25.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 11, 1),
            is_active=True,
            notes="Wöchentlich 2x Mathe"
        )
        
        contract2 = Contract.objects.create(
            student=student2,
            institute="Nachhilfe-Institut ABC",
            hourly_rate=Decimal('30.00'),
            unit_duration_minutes=90,
            start_date=date(2025, 10, 15),
            is_active=True
        )
        
        contract3 = Contract.objects.create(
            student=student3,
            hourly_rate=Decimal('28.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 12, 1),
            is_active=True
        )
        
        # Lessons (mit Konflikt)
        today = timezone.now().date()
        
        lesson1 = Lesson.objects.create(
            contract=contract1,
            date=today + timedelta(days=1),
            start_time=time(14, 0),
            duration_minutes=60,
            status='planned',
            location=location_home,
            travel_time_before_minutes=15,
            travel_time_after_minutes=20,
            notes="Algebra: Lineare Gleichungen"
        )
        
        # Konflikt: Überschneidung mit lesson1
        lesson2 = Lesson.objects.create(
            contract=contract2,
            date=today + timedelta(days=1),
            start_time=time(14, 30),  # Überschneidung!
            duration_minutes=90,
            status='planned',
            location=location_school,
            travel_time_before_minutes=20,
            notes="Deutsch: Textanalyse"
        )
        
        lesson3 = Lesson.objects.create(
            contract=contract1,
            date=today + timedelta(days=3),
            start_time=time(16, 0),
            duration_minutes=60,
            status='planned',
            location=location_home,
            notes="Physik: Mechanik"
        )
        
        lesson4 = Lesson.objects.create(
            contract=contract3,
            date=today - timedelta(days=2),
            start_time=time(15, 0),
            duration_minutes=60,
            status='paid',
            location=location_home,
            notes="Mathe: Analysis"
        )
        
        # Blockzeiten
        blocked_time1 = BlockedTime.objects.create(
            title="Uni-Vorlesung",
            description="Mathematik-Vorlesung",
            start_datetime=timezone.make_aware(
                timezone.datetime.combine(today + timedelta(days=2), time(10, 0))
            ),
            end_datetime=timezone.make_aware(
                timezone.datetime.combine(today + timedelta(days=2), time(12, 0))
            ),
            is_recurring=False
        )
        
        # Premium-User mit LessonPlan
        # Prüfe, ob User bereits existiert, sonst erstelle ihn
        premium_user, created = User.objects.get_or_create(
            username='demo_premium',
            defaults={
                'email': 'premium@example.com',
                'is_staff': True,  # Erforderlich für Admin-Login
                'is_active': True,
            }
        )
        
        # Setze Passwort (auch wenn User bereits existiert, um sicherzustellen, dass es korrekt ist)
        premium_user.set_password('demo123')
        premium_user.is_staff = True  # Erforderlich für Admin-Login
        premium_user.is_active = True
        premium_user.save()
        
        # Erstelle oder aktualisiere UserProfile
        profile, profile_created = UserProfile.objects.get_or_create(
            user=premium_user,
            defaults={
                'is_premium': True,
                'premium_since': timezone.now()
            }
        )
        
        # Aktualisiere Profile, falls es bereits existiert
        if not profile_created:
            profile.is_premium = True
            if not profile.premium_since:
                profile.premium_since = timezone.now()
            profile.save()
        
        # Demo LessonPlan (ohne echten LLM-Call)
        lesson_plan = LessonPlan.objects.create(
            student=student1,
            lesson=lesson1,
            topic="Lineare Gleichungen",
            subject="Mathe",
            content="""# Unterrichtsplan: Lineare Gleichungen

## Einstieg (10 Min)
- Wiederholung: Was sind lineare Gleichungen?
- Beispiel: 2x + 3 = 7

## Hauptteil (40 Min)
- Lösen einfacher linearer Gleichungen
- Übungsaufgaben aus dem Buch
- Gemeinsame Besprechung

## Abschluss (10 Min)
- Zusammenfassung der wichtigsten Schritte
- Hausaufgaben: 3 weitere Aufgaben""",
            grade_level="10. Klasse",
            duration_minutes=60,
            llm_model="gpt-3.5-turbo"
        )
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Demo-Daten erfolgreich erstellt:'))
        self.stdout.write(f'  - {Location.objects.count()} Orte')
        self.stdout.write(f'  - {Student.objects.count()} Schüler')
        self.stdout.write(f'  - {Contract.objects.count()} Verträge')
        self.stdout.write(f'  - {Lesson.objects.count()} Unterrichtsstunden')
        self.stdout.write(f'  - {BlockedTime.objects.count()} Blockzeiten')
        self.stdout.write(f'  - {UserProfile.objects.filter(is_premium=True).count()} Premium-User')
        self.stdout.write(f'  - {LessonPlan.objects.count()} Unterrichtspläne')
        self.stdout.write(self.style.SUCCESS(f'\n📝 Demo-Login:'))
        self.stdout.write(f'  Username: demo_premium')
        self.stdout.write(f'  Password: demo123')
        self.stdout.write(self.style.WARNING(f'\n⚠️  Hinweis: Lesson1 und Lesson2 haben einen Konflikt!'))

