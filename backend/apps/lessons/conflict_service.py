"""
Service for conflict detection and recalculation.
"""

from datetime import datetime, timedelta

from apps.blocked_times.models import BlockedTime
from apps.lessons.models import Lesson
from apps.lessons.quota_service import ContractQuotaService
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _


def recalculate_conflicts_for_affected_lessons(lesson: Lesson):
    """
    Recalculates conflicts for a lesson and all potentially affected lessons.

    This should be called after a lesson is created, updated, or deleted
    to ensure all conflict flags are up to date.

    Args:
        lesson: The lesson that was changed
    """
    # Recalculate conflicts for the lesson itself (if it still exists)
    if lesson.pk:
        # This will be done when the lesson is accessed, but we can force it here
        pass

    # Find all lessons on the same date that might be affected
    affected_lessons = Lesson.objects.filter(date=lesson.date).exclude(
        pk=lesson.pk if lesson.pk else None
    )

    # Recalculate conflicts for affected lessons
    # (The conflicts will be recalculated on-demand when accessed)
    # But we can trigger a check here to ensure consistency
    for affected_lesson in affected_lessons:
        # Force conflict check (this will be cached in the property)
        affected_lesson.get_conflicts()


def recalculate_conflicts_for_blocked_time(blocked_time: BlockedTime):
    """
    Recalculates conflicts for all lessons that might be affected by a blocked time change.

    Args:
        blocked_time: The blocked time that was changed or deleted
    """
    # Find all lessons that might overlap with this blocked time
    start_datetime = blocked_time.start_datetime

    # Find lessons on the same date
    affected_lessons = Lesson.objects.filter(date=start_datetime.date())

    # Check each lesson for conflicts with this blocked time
    for lesson in affected_lessons:
        # Force conflict check
        lesson.get_conflicts()


class LessonConflictService:
    """Service for conflict detection in lessons."""

    @staticmethod
    def intervals_overlap(
        start1: datetime, end1: datetime, start2: datetime, end2: datetime
    ) -> bool:
        """
        Checks if two time intervals overlap.

        Two intervals overlap if:
        - end1 > start2 AND start1 < end2

        Args:
            start1: Start of first interval
            end1: End of first interval
            start2: Start of second interval
            end2: End of second interval

        Returns:
            True if overlap, otherwise False
        """
        return end1 > start2 and start1 < end2

    @staticmethod
    def calculate_time_block(lesson: Lesson) -> tuple[datetime, datetime]:
        """
        Calculates the total time block of a lesson including travel times.

        Args:
            lesson: Lesson object

        Returns:
            Tuple (start_datetime, end_datetime) with timezone-aware datetime
        """
        # Combine date and start time
        lesson_datetime = timezone.make_aware(datetime.combine(lesson.date, lesson.start_time))

        # Start = start time - travel time before
        start_datetime = lesson_datetime - timedelta(minutes=lesson.travel_time_before_minutes)

        # End = start time + duration + travel time after
        end_datetime = lesson_datetime + timedelta(
            minutes=lesson.duration_minutes + lesson.travel_time_after_minutes
        )

        return start_datetime, end_datetime

    @staticmethod
    def check_conflicts(lesson: Lesson, exclude_self: bool = True) -> list[dict]:
        """
        Checks if a lesson has conflicts with other lessons or blocked times.

        Args:
            lesson: Lesson object
            exclude_self: If True, the lesson itself is excluded from the check

        Returns:
            List of conflict dicts with 'type', 'object', 'message'
        """
        conflicts = []
        start_datetime, end_datetime = LessonConflictService.calculate_time_block(lesson)

        # Check conflicts with other lessons
        query = Q(date=lesson.date, start_time__isnull=False)

        if exclude_self and lesson.pk:
            query &= ~Q(pk=lesson.pk)

        other_lessons = Lesson.objects.filter(query).select_related("contract", "contract__student")

        for other_lesson in other_lessons:
            other_start, other_end = LessonConflictService.calculate_time_block(other_lesson)

            # Check overlap with explicit helper function
            if LessonConflictService.intervals_overlap(
                start1=start_datetime, end1=end_datetime, start2=other_start, end2=other_end
            ):
                conflicts.append(
                    {
                        "type": "lesson",
                        "object": other_lesson,
                        "message": _("Overlap with lesson for {student} ({time})").format(
                            student=other_lesson.contract.student,
                            time=other_lesson.start_time.strftime("%H:%M"),
                        ),
                        "start": other_start,
                        "end": other_end,
                    }
                )

        # Check conflicts with blocked times
        # Use a broader query, but then explicitly check for overlap
        # Filter by date to improve performance (for multi-day blocked times)
        # Find blocked times that could overlap: start before lesson ends, end after lesson starts
        blocked_times = BlockedTime.objects.filter(
            start_datetime__lt=end_datetime, end_datetime__gt=start_datetime
        )

        for blocked_time in blocked_times:
            # Explicit overlap check with helper function
            if LessonConflictService.intervals_overlap(
                start1=start_datetime,
                end1=end_datetime,
                start2=blocked_time.start_datetime,
                end2=blocked_time.end_datetime,
            ):
                conflicts.append(
                    {
                        "type": "blocked_time",
                        "object": blocked_time,
                        "message": _("Overlap with blocked time: {title}").format(
                            title=blocked_time.title
                        ),
                        "start": blocked_time.start_datetime,
                        "end": blocked_time.end_datetime,
                    }
                )

        # Check quota conflict
        quota_conflict = ContractQuotaService.check_quota_conflict(lesson, exclude_self)
        if quota_conflict:
            conflicts.append(
                {
                    "type": "quota",
                    "object": lesson.contract,
                    "message": quota_conflict["message"],
                    "planned_total": quota_conflict["planned_total"],
                    "actual_total": quota_conflict["actual_total"],
                    "month": quota_conflict["month"],
                    "year": quota_conflict["year"],
                }
            )

        return conflicts

    @staticmethod
    def has_conflicts(lesson: Lesson, exclude_self: bool = True) -> bool:
        """
        Checks if a lesson has conflicts (simplified version).

        Args:
            lesson: Lesson object
            exclude_self: If True, the lesson itself is excluded

        Returns:
            True if conflicts exist, otherwise False
        """
        return len(LessonConflictService.check_conflicts(lesson, exclude_self)) > 0
