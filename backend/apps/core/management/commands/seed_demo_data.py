"""
Management Command zum Erstellen von Demo-Daten für TutorFlow.

Verwendung:
    python manage.py seed_demo_data

Erstellt:
    - 4 Schüler mit unterschiedlichen Profilen
    - Zugehörige Verträge (inkl. ContractMonthlyPlan für Quota-Konflikte)
    - Mehrere Lessons (inkl. Konflikten und Recurring Lessons)
    - Blockzeiten (inkl. mehrtägiger Urlaub und Konflikten)
    - Premium-User mit generiertem LessonPlan
    - Non-Premium-User zum Vergleich
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import date, time, timedelta
from apps.students.models import Student
from apps.contracts.models import Contract, ContractMonthlyPlan
from apps.lessons.models import Lesson
from apps.lessons.recurring_models import RecurringLesson
from apps.lessons.recurring_service import RecurringLessonService
from apps.blocked_times.models import BlockedTime
from apps.core.models import UserProfile
from apps.lesson_plans.models import LessonPlan
from apps.billing.models import Invoice, InvoiceItem
from apps.billing.services import InvoiceService


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
            RecurringLesson.objects.all().delete()
            BlockedTime.objects.all().delete()
            ContractMonthlyPlan.objects.all().delete()
            Contract.objects.all().delete()
            Student.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(self.style.SUCCESS('Erstelle Demo-Daten...'))
        
        # Schüler
        student1 = Student.objects.create(
            first_name="Max",
            last_name="Mustermann",
            email="max.mustermann@example.com",
            phone="0123-456789",
            school="Gymnasium XY",
            grade="10. Klasse",
            subjects="Mathe, Physik",
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
            notes="Gute Schülerin, möchte sich auf Abitur vorbereiten"
        )
        
        student3 = Student.objects.create(
            first_name="Tom",
            last_name="Weber",
            email="tom.weber@example.com",
            school="Gymnasium XY",
            grade="11. Klasse",
            subjects="Mathe, Chemie"
        )
        
        student4 = Student.objects.create(
            first_name="Lisa",
            last_name="Müller",
            email="lisa.mueller@example.com",
            school="Gymnasium XY",
            grade="8. Klasse",
            subjects="Deutsch, Englisch",
            notes="Recurring lessons every Monday and Wednesday"
        )
        
        # Verträge
        # Contract 1: Mit monatlichen Kontingenten (für Quota-Konflikte)
        contract1 = Contract.objects.create(
            student=student1,
            hourly_rate=Decimal('25.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 11, 1),
            is_active=True,
            notes="Wöchentlich 2x Mathe - mit monatlichen Kontingenten"
        )
        
        # ContractMonthlyPlan für Quota-Konflikte
        ContractMonthlyPlan.objects.create(
            contract=contract1,
            year=2025,
            month=11,
            planned_units=3
        )
        ContractMonthlyPlan.objects.create(
            contract=contract1,
            year=2025,
            month=12,
            planned_units=5
        )
        
        # Contract 2: Mit Recurring Lessons
        contract2 = Contract.objects.create(
            student=student2,
            institute="Nachhilfe-Institut ABC",
            hourly_rate=Decimal('30.00'),
            unit_duration_minutes=90,
            start_date=date(2025, 10, 15),
            is_active=True,
            notes="Recurring lessons weekly"
        )
        
        # Contract 3: Nur Einzelstunden
        contract3 = Contract.objects.create(
            student=student3,
            hourly_rate=Decimal('28.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 12, 1),
            is_active=True,
            notes="Nur Einzelstunden"
        )
        
        # Contract 4: Mit Recurring Lessons (Mo+Mi)
        contract4 = Contract.objects.create(
            student=student4,
            hourly_rate=Decimal('22.00'),
            unit_duration_minutes=60,
            start_date=date(2025, 11, 1),
            is_active=True,
            notes="Recurring lessons Monday and Wednesday"
        )
        
        # Lessons (mit Konflikt)
        today = timezone.now().date()
        
        lesson1 = Lesson.objects.create(
            contract=contract1,
            date=today + timedelta(days=1),
            start_time=time(14, 0),
            duration_minutes=60,
            status='planned',
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
            travel_time_before_minutes=20,
            notes="Deutsch: Textanalyse"
        )
        
        lesson3 = Lesson.objects.create(
            contract=contract1,
            date=today + timedelta(days=3),
            start_time=time(16, 0),
            duration_minutes=60,
            status='planned',
            notes="Physik: Mechanik"
        )
        
        # Lesson4: Wird als "taught" erstellt und dann in eine Rechnung aufgenommen (wird automatisch "paid")
        lesson4 = Lesson.objects.create(
            contract=contract3,
            date=today - timedelta(days=2),
            start_time=time(15, 0),
            duration_minutes=60,
            status='taught',  # Zuerst als "taught" erstellen
            notes="Mathe: Analysis"
        )
        
        # Quota-Konflikt: Versuche mehr Lessons zu erstellen als geplant
        # November: 3 geplant, aber 4 Lessons erstellen (4. sollte Konflikt haben)
        lesson5 = Lesson.objects.create(
            contract=contract1,
            date=date(2025, 11, 5),
            start_time=time(10, 0),
            duration_minutes=60,
            status='planned',
            notes="Mathe: Algebra - 1. Lesson im November"
        )
        lesson6 = Lesson.objects.create(
            contract=contract1,
            date=date(2025, 11, 12),
            start_time=time(10, 0),
            duration_minutes=60,
            status='planned',
            notes="Mathe: Algebra - 2. Lesson im November"
        )
        lesson7 = Lesson.objects.create(
            contract=contract1,
            date=date(2025, 11, 19),
            start_time=time(10, 0),
            duration_minutes=60,
            status='planned',
            notes="Mathe: Algebra - 3. Lesson im November"
        )
        # Diese Lesson sollte einen Quota-Konflikt haben (4. Lesson, aber nur 3 geplant)
        lesson8 = Lesson.objects.create(
            contract=contract1,
            date=date(2025, 11, 26),
            start_time=time(10, 0),
            duration_minutes=60,
            status='planned',
            notes="Mathe: Algebra - 4. Lesson im November (QUOTA CONFLICT)"
        )
        
        # Recurring Lessons
        # Recurring Lesson 1: Weekly, Monday and Wednesday
        recurring1_start = today + timedelta(days=(7 - today.weekday()) % 7)  # Next Monday
        if recurring1_start <= today:
            recurring1_start += timedelta(days=7)
        
        recurring1 = RecurringLesson.objects.create(
            contract=contract4,
            start_date=recurring1_start,
            end_date=recurring1_start + timedelta(days=30),  # 4 weeks
            start_time=time(16, 0),
            duration_minutes=60,
            travel_time_before_minutes=15,
            travel_time_after_minutes=15,
            recurrence_type='weekly',
            notes="Deutsch: Grammatik und Rechtschreibung",
            monday=True,
            tuesday=False,
            wednesday=True,
            thursday=False,
            friday=False,
            saturday=False,
            sunday=False,
            is_active=True
        )
        
        # Generate lessons from recurring lesson
        RecurringLessonService.generate_lessons(recurring1, check_conflicts=True, dry_run=False)
        
        # Recurring Lesson 2: Weekly, Tuesday and Thursday
        recurring2_start = today + timedelta(days=(1 - today.weekday()) % 7)  # Next Tuesday
        if recurring2_start <= today:
            recurring2_start += timedelta(days=7)
        
        recurring2 = RecurringLesson.objects.create(
            contract=contract2,
            start_date=recurring2_start,
            end_date=recurring2_start + timedelta(days=21),  # 3 weeks
            start_time=time(15, 0),
            duration_minutes=90,
            travel_time_before_minutes=20,
            travel_time_after_minutes=20,
            recurrence_type='weekly',
            notes="Englisch: Conversation and Grammar",
            monday=False,
            tuesday=True,
            wednesday=False,
            thursday=True,
            friday=False,
            saturday=False,
            sunday=False,
            is_active=True
        )
        
        # Generate lessons from recurring lesson
        RecurringLessonService.generate_lessons(recurring2, check_conflicts=True, dry_run=False)
        
        # Blockzeiten
        # Blockzeit 1: Uni-Vorlesung (einmalig)
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
        
        # Blockzeit 2: Mehrtägiger Urlaub (3 Tage)
        vacation_start = today + timedelta(days=10)
        blocked_time2 = BlockedTime.objects.create(
            title="Urlaub",
            description="Mehrtägiger Urlaub",
            start_datetime=timezone.make_aware(
                timezone.datetime.combine(vacation_start, time(0, 0))
            ),
            end_datetime=timezone.make_aware(
                timezone.datetime.combine(vacation_start + timedelta(days=2), time(23, 59))
            ),
            is_recurring=False
        )
        
        # Blockzeit 3: Konflikt mit einer Lesson (bewusst)
        conflict_date = today + timedelta(days=5)
        blocked_time3 = BlockedTime.objects.create(
            title="Andere Tätigkeit",
            description="Bewusst konflikt mit einer Lesson",
            start_datetime=timezone.make_aware(
                timezone.datetime.combine(conflict_date, time(14, 0))
            ),
            end_datetime=timezone.make_aware(
                timezone.datetime.combine(conflict_date, time(15, 30))
            ),
            is_recurring=False
        )
        
        # Erstelle eine Lesson, die mit blocked_time3 kollidiert
        lesson_conflict = Lesson.objects.create(
            contract=contract3,
            date=conflict_date,
            start_time=time(14, 30),  # Überschneidung mit blocked_time3
            duration_minutes=60,
            status='planned',
            notes="Mathe: Analysis - CONFLICT WITH BLOCKED TIME"
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
        
        # Non-Premium-User zum Vergleich
        non_premium_user, created = User.objects.get_or_create(
            username='demo_standard',
            defaults={
                'email': 'standard@example.com',
                'is_staff': True,
                'is_active': True,
            }
        )
        non_premium_user.set_password('demo123')
        non_premium_user.is_staff = True
        non_premium_user.is_active = True
        non_premium_user.save()
        
        # Erstelle oder aktualisiere UserProfile (non-premium)
        non_premium_profile, _ = UserProfile.objects.get_or_create(
            user=non_premium_user,
            defaults={
                'is_premium': False,
            }
        )
        non_premium_profile.is_premium = False
        non_premium_profile.save()
        
        # Demo LessonPlan 1 (für lesson1 - bereits existierend)
        lesson_plan1 = LessonPlan.objects.create(
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
        
        # Demo LessonPlan 2 (für lesson3 - noch kein Plan, kann AI generieren)
        # lesson3 hat noch keinen Plan, damit Premium-User die AI-Funktion testen kann
        
        # Demo LessonPlan 3 (für eine der Recurring Lessons, falls vorhanden)
        recurring_lessons = Lesson.objects.filter(contract=contract4).order_by('date')
        if recurring_lessons.exists():
            first_recurring_lesson = recurring_lessons.first()
            lesson_plan3 = LessonPlan.objects.create(
                student=student4,
                lesson=first_recurring_lesson,
                topic="Deutsche Grammatik: Satzglieder",
                subject="Deutsch",
                content="""# Unterrichtsplan: Satzglieder

## Einstieg (10 Min)
- Wiederholung: Was sind Satzglieder?
- Beispiele: Subjekt, Prädikat, Objekt

## Hauptteil (40 Min)
- Bestimmung von Satzgliedern in Beispielsätzen
- Übungsaufgaben
- Gemeinsame Besprechung

## Abschluss (10 Min)
- Zusammenfassung
- Hausaufgaben: 5 Sätze analysieren""",
                grade_level="8. Klasse",
                duration_minutes=60,
                llm_model="gpt-3.5-turbo"
            )
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Demo-Daten erfolgreich erstellt:'))
        self.stdout.write(f'  - {Student.objects.count()} Schüler')
        self.stdout.write(f'  - {Contract.objects.count()} Verträge')
        self.stdout.write(f'  - {ContractMonthlyPlan.objects.count()} Monatspläne')
        self.stdout.write(f'  - {Lesson.objects.count()} Unterrichtsstunden')
        self.stdout.write(f'  - {RecurringLesson.objects.count()} Recurring Lessons')
        self.stdout.write(f'  - {BlockedTime.objects.count()} Blockzeiten')
        self.stdout.write(f'  - {UserProfile.objects.filter(is_premium=True).count()} Premium-User')
        self.stdout.write(f'  - {UserProfile.objects.filter(is_premium=False).count()} Non-Premium-User')
        self.stdout.write(f'  - {LessonPlan.objects.count()} Unterrichtspläne')
        self.stdout.write(self.style.SUCCESS(f'\n📝 Demo-Logins:'))
        self.stdout.write(f'  Premium User:')
        self.stdout.write(f'    Username: demo_premium')
        self.stdout.write(f'    Password: demo123')
        self.stdout.write(f'  Standard User:')
        self.stdout.write(f'    Username: demo_standard')
        self.stdout.write(f'    Password: demo123')
        self.stdout.write(self.style.WARNING(f'\n⚠️  Hinweise:'))
        self.stdout.write(f'  - Lesson1 und Lesson2 haben einen Zeit-Konflikt!')
        self.stdout.write(f'  - Lesson8 hat einen Quota-Konflikt (4. Lesson, aber nur 3 geplant)!')
        self.stdout.write(f'  - lesson_conflict hat einen Konflikt mit blocked_time3!')
        self.stdout.write(f'  - Recurring Lessons wurden generiert (Mo+Mi für student4, Di+Do für student2)!')
        self.stdout.write(f'  - lesson3 hat noch keinen LessonPlan (kann mit AI generiert werden)!')

