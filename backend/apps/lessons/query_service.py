"""
Service for lesson queries and filtering.
"""

from datetime import date, timedelta

from apps.lessons.models import Lesson
from django.utils import timezone


class LessonQueryService:
    """Service for lesson queries and filtering."""

    @staticmethod
    def get_lessons_for_month(year: int, month: int) -> list[Lesson]:
        """
        Returns all lessons for a specific month.

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            List of Lesson objects
        """
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        return (
            Lesson.objects.filter(date__gte=start_date, date__lt=end_date)
            .select_related("contract", "contract__student")
            .order_by("date", "start_time")
        )

    @staticmethod
    def get_today_lessons() -> list[Lesson]:
        """Returns all lessons for today."""
        today = timezone.now().date()
        return (
            Lesson.objects.filter(date=today)
            .select_related("contract", "contract__student")
            .order_by("start_time")
        )

    @staticmethod
    def get_upcoming_lessons(days: int = 7) -> list[Lesson]:
        """
        Returns upcoming lessons (excluding today's lessons).

        Today's lessons are excluded as they are already shown in
        the separate "Today" section.

        Args:
            days: Number of days into the future (starting from tomorrow)

        Returns:
            List of Lesson objects (from tomorrow up to today + days)
        """
        today = timezone.now().date()
        end_date = today + timedelta(days=days)

        # Only lessons from tomorrow (date > today), not today
        return (
            Lesson.objects.filter(date__gt=today, date__lte=end_date)
            .select_related("contract", "contract__student")
            .order_by("date", "start_time")[:10]
        )
