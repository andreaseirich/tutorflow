"""
Service für Wochenansicht - Gruppierung von Lessons und Blockzeiten nach Tagen und Zeiten.
"""

from datetime import date, datetime, time, timedelta
from typing import Dict, List
from collections import defaultdict
from django.utils import timezone
from apps.lessons.models import Lesson
from apps.blocked_times.models import BlockedTime
from apps.lessons.services import LessonConflictService
from apps.blocked_times.recurring_models import RecurringBlockedTime
from apps.blocked_times.recurring_service import RecurringBlockedTimeService


class WeekService:
    """Service für Wochenansicht."""

    @staticmethod
    def get_week_data(year: int, month: int, day: int) -> Dict:
        """
        Lädt alle Lessons und Blockzeiten für eine Woche (Montag bis Sonntag).

        Args:
            year: Jahr
            month: Monat (1-12)
            day: Tag des Monats (1-31) - wird verwendet, um die Woche zu bestimmen

        Returns:
            Dict mit:
            - 'week_start': date (Montag der Woche)
            - 'week_end': date (Sonntag der Woche)
            - 'lessons_by_date': Dict[date, List[Lesson]]
            - 'blocked_times_by_date': Dict[date, List[BlockedTime]]
            - 'conflicts_by_lesson': Dict[Lesson.id, List[conflicts]]
        """
        # Bestimme den Montag der Woche
        target_date = date(year, month, day)
        days_since_monday = target_date.weekday()  # 0=Montag, 6=Sonntag
        week_start = target_date - timedelta(days=days_since_monday)
        week_end = week_start + timedelta(days=6)  # Sonntag

        # Lade Lessons für die Woche
        lessons = (
            Lesson.objects.filter(date__gte=week_start, date__lte=week_end)
            .select_related("contract", "contract__student")
            .order_by("date", "start_time")
        )

        # Lade Blockzeiten für die Woche
        start_datetime = timezone.make_aware(datetime.combine(week_start, time.min))
        end_datetime = timezone.make_aware(datetime.combine(week_end, time.max))
        blocked_times = BlockedTime.objects.filter(
            start_datetime__lt=end_datetime, end_datetime__gt=start_datetime
        ).order_by("start_datetime")

        # Lade wiederkehrende Blockzeiten und generiere temporäre Blockzeiten für die Woche
        recurring_blocked_times = RecurringBlockedTime.objects.filter(
            start_date__lte=week_end, end_date__gte=week_start, is_active=True
        ) | RecurringBlockedTime.objects.filter(
            start_date__lte=week_end, end_date__isnull=True, is_active=True
        )

        # Gruppiere Lessons nach Datum
        lessons_by_date = defaultdict(list)
        conflicts_by_lesson = {}

        for lesson in lessons:
            lessons_by_date[lesson.date].append(lesson)
            # Prüfe Konflikte
            conflicts = LessonConflictService.check_conflicts(lesson)
            if conflicts:
                conflicts_by_lesson[lesson.id] = conflicts

        # Gruppiere Blockzeiten nach Datum
        blocked_times_by_date = defaultdict(list)

        # Füge normale Blockzeiten hinzu
        for blocked_time in blocked_times:
            current_date = blocked_time.start_datetime.date()
            end_date_bt = blocked_time.end_datetime.date()

            # Füge für jeden betroffenen Tag hinzu
            while current_date <= end_date_bt and current_date <= week_end:
                if current_date >= week_start:
                    blocked_times_by_date[current_date].append(blocked_time)
                current_date += timedelta(days=1)

        # Füge generierte Blockzeiten aus RecurringBlockedTime hinzu
        for rbt in recurring_blocked_times:
            generated_blocked_times_preview = RecurringBlockedTimeService.preview_blocked_times(rbt)
            for bt_preview in generated_blocked_times_preview:
                # Filter nur für die aktuelle Woche
                if week_start <= bt_preview.start_datetime.date() <= week_end:
                    blocked_times_by_date[bt_preview.start_datetime.date()].append(bt_preview)

        return {
            "week_start": week_start,
            "week_end": week_end,
            "lessons_by_date": dict(lessons_by_date),
            "blocked_times_by_date": dict(blocked_times_by_date),
            "conflicts_by_lesson": conflicts_by_lesson,
        }
