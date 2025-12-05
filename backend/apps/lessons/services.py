"""
Service-Layer für Lesson-Planungslogik und Konfliktprüfung.
"""
from datetime import datetime, date, time, timedelta
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import Q
from apps.lessons.models import Lesson
from apps.blocked_times.models import BlockedTime
from apps.lessons.quota_service import ContractQuotaService


class LessonConflictService:
    """Service für Konfliktprüfung bei Lessons."""

    @staticmethod
    def calculate_time_block(lesson: Lesson) -> tuple[datetime, datetime]:
        """
        Berechnet den Gesamtzeitblock einer Lesson inkl. Fahrtzeiten.
        
        Args:
            lesson: Lesson-Objekt
        
        Returns:
            Tuple (start_datetime, end_datetime) mit timezone-aware datetime
        """
        # Kombiniere Datum und Startzeit
        lesson_datetime = timezone.make_aware(
            datetime.combine(lesson.date, lesson.start_time)
        )
        
        # Start = Startzeit - Fahrtzeit vorher
        start_datetime = lesson_datetime - timedelta(minutes=lesson.travel_time_before_minutes)
        
        # Ende = Startzeit + Dauer + Fahrtzeit nachher
        end_datetime = lesson_datetime + timedelta(
            minutes=lesson.duration_minutes + lesson.travel_time_after_minutes
        )
        
        return start_datetime, end_datetime

    @staticmethod
    def check_conflicts(lesson: Lesson, exclude_self: bool = True) -> list[dict]:
        """
        Prüft, ob eine Lesson Konflikte mit anderen Lessons oder Blockzeiten hat.
        
        Args:
            lesson: Lesson-Objekt
            exclude_self: Wenn True, wird die Lesson selbst von der Prüfung ausgeschlossen
        
        Returns:
            Liste von Konfliktdicts mit 'type', 'object', 'message'
        """
        conflicts = []
        start_datetime, end_datetime = LessonConflictService.calculate_time_block(lesson)
        
        # Prüfe Konflikte mit anderen Lessons
        query = Q(
            date=lesson.date,
            start_time__isnull=False
        )
        
        if exclude_self and lesson.pk:
            query &= ~Q(pk=lesson.pk)
        
        other_lessons = Lesson.objects.filter(query).select_related('contract', 'contract__student')
        
        for other_lesson in other_lessons:
            other_start, other_end = LessonConflictService.calculate_time_block(other_lesson)
            
            # Prüfe Überlappung
            if not (end_datetime <= other_start or start_datetime >= other_end):
                conflicts.append({
                    'type': 'lesson',
                    'object': other_lesson,
                    'message': _("Overlap with lesson for {student} ({time})").format(
                        student=other_lesson.contract.student,
                        time=other_lesson.start_time.strftime('%H:%M')
                    ),
                    'start': other_start,
                    'end': other_end,
                })
        
        # Prüfe Konflikte mit Blockzeiten
        blocked_times = BlockedTime.objects.filter(
            start_datetime__lt=end_datetime,
            end_datetime__gt=start_datetime
        )
        
        for blocked_time in blocked_times:
            conflicts.append({
                'type': 'blocked_time',
                'object': blocked_time,
                'message': _("Overlap with blocked time: {title}").format(title=blocked_time.title),
                'start': blocked_time.start_datetime,
                'end': blocked_time.end_datetime,
            })
        
        # Prüfe Kontingent-Konflikt (Quota)
        quota_conflict = ContractQuotaService.check_quota_conflict(lesson, exclude_self)
        if quota_conflict:
            conflicts.append({
                'type': 'quota',
                'object': lesson.contract,
                'message': quota_conflict['message'],
                'planned_total': quota_conflict['planned_total'],
                'actual_total': quota_conflict['actual_total'],
                'month': quota_conflict['month'],
                'year': quota_conflict['year'],
            })
        
        return conflicts

    @staticmethod
    def has_conflicts(lesson: Lesson, exclude_self: bool = True) -> bool:
        """
        Prüft, ob eine Lesson Konflikte hat (vereinfachte Version).
        
        Args:
            lesson: Lesson-Objekt
            exclude_self: Wenn True, wird die Lesson selbst ausgeschlossen
        
        Returns:
            True wenn Konflikte vorhanden, sonst False
        """
        return len(LessonConflictService.check_conflicts(lesson, exclude_self)) > 0


class LessonQueryService:
    """Service für Lesson-Abfragen und Filterung."""

    @staticmethod
    def get_lessons_for_month(year: int, month: int) -> list[Lesson]:
        """
        Gibt alle Lessons für einen bestimmten Monat zurück.
        
        Args:
            year: Jahr
            month: Monat (1-12)
        
        Returns:
            Liste von Lesson-Objekten
        """
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        return Lesson.objects.filter(
            date__gte=start_date,
            date__lt=end_date
        ).select_related('contract', 'contract__student').order_by('date', 'start_time')

    @staticmethod
    def get_today_lessons() -> list[Lesson]:
        """Gibt alle Lessons für heute zurück."""
        today = timezone.now().date()
        return Lesson.objects.filter(
            date=today
        ).select_related('contract', 'contract__student').order_by('start_time')

    @staticmethod
    def get_upcoming_lessons(days: int = 7) -> list[Lesson]:
        """
        Gibt die nächsten Lessons zurück.
        
        Args:
            days: Anzahl der Tage in die Zukunft
        
        Returns:
            Liste von Lesson-Objekten
        """
        today = timezone.now().date()
        end_date = today + timedelta(days=days)
        
        return Lesson.objects.filter(
            date__gte=today,
            date__lte=end_date
        ).select_related('contract', 'contract__student').order_by('date', 'start_time')[:10]

