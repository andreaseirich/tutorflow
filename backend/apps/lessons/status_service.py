"""
Service für automatische Status-Setzung von Lessons basierend auf Datum/Zeit.
"""
from datetime import datetime, timedelta
from django.utils import timezone
from apps.lessons.models import Lesson


class LessonStatusService:
    """Service für automatische Status-Verwaltung von Lessons."""

    @staticmethod
    def update_status_for_lesson(lesson: Lesson) -> bool:
        """
        Aktualisiert den Status einer Lesson basierend auf Datum/Zeit.
        
        Regeln:
        - Wenn end_datetime < jetzt und Status PLANNED → setze auf TAUGHT
        - Wenn start_datetime >= jetzt und Status leer/None → setze auf PLANNED
        - PAID oder CANCELLED werden NICHT überschrieben
        
        Args:
            lesson: Die Lesson-Instanz
            
        Returns:
            True, wenn Status geändert wurde, False sonst
        """
        now = timezone.now()
        
        # Berechne start_datetime und end_datetime
        start_datetime = timezone.make_aware(
            datetime.combine(lesson.date, lesson.start_time)
        )
        end_datetime = start_datetime + timedelta(minutes=lesson.duration_minutes)
        
        # Status PAID oder CANCELLED nicht überschreiben
        if lesson.status in ['paid', 'cancelled']:
            return False
        
        status_changed = False
        
        # Vergangene Lesson (end_datetime < jetzt) mit Status PLANNED → TAUGHT
        if end_datetime < now and lesson.status == 'planned':
            lesson.status = 'taught'
            status_changed = True
        
        # Zukünftige Lesson (start_datetime >= jetzt) ohne Status → PLANNED
        elif start_datetime >= now and (not lesson.status or lesson.status == ''):
            lesson.status = 'planned'
            status_changed = True
        
        if status_changed:
            lesson.save(update_fields=['status', 'updated_at'])
        
        return status_changed

    @staticmethod
    def bulk_update_past_lessons() -> int:
        """
        Setzt alle Lessons mit end_datetime < jetzt und Status PLANNED auf TAUGHT.
        Überspringt Lessons mit Status PAID oder CANCELLED.
        
        Returns:
            Anzahl der aktualisierten Lessons
        """
        now = timezone.now()
        updated_count = 0
        
        # Lade alle Lessons mit Status PLANNED
        lessons = Lesson.objects.filter(status='planned')
        
        for lesson in lessons:
            # Berechne end_datetime
            start_datetime = timezone.make_aware(
                datetime.combine(lesson.date, lesson.start_time)
            )
            end_datetime = start_datetime + timedelta(minutes=lesson.duration_minutes)
            
            # Wenn vergangen, setze auf TAUGHT
            if end_datetime < now:
                lesson.status = 'taught'
                lesson.save(update_fields=['status', 'updated_at'])
                updated_count += 1
        
        return updated_count

