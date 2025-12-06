"""
Service für automatische Status-Setzung von Lessons basierend auf Datum/Zeit.
"""
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, F
from django.db import transaction
from apps.lessons.models import Lesson


class LessonStatusUpdater:
    """
    Service-Klasse für automatische Status-Aktualisierung von Lessons.
    
    Setzt Lessons mit Status 'planned' automatisch auf 'taught', sobald
    ihre Endzeit in der Vergangenheit liegt.
    """

    @staticmethod
    def update_past_lessons_to_taught(now=None) -> int:
        """
        Setzt alle Lessons mit Status 'planned' auf 'taught', deren Endzeit
        in der Vergangenheit liegt.
        
        Regeln:
        - Nur Lessons mit Status 'planned' werden aktualisiert
        - Lessons mit Status 'paid' oder 'cancelled' werden NICHT verändert
        - Endzeit = start_datetime + duration_minutes (ohne Fahrtzeiten)
        
        Args:
            now: Optional datetime-Objekt (default: timezone.now(), Europe/Berlin)
        
        Returns:
            Anzahl der aktualisierten Lessons
        """
        if now is None:
            now = timezone.now()
        
        # Lade alle Lessons mit Status 'planned'
        # Verwende select_for_update für Thread-Safety (optional, aber sauber)
        lessons = Lesson.objects.filter(status='planned').select_for_update(skip_locked=True)
        
        updated_lessons = []
        
        for lesson in lessons:
            # Berechne end_datetime (nur Lesson-Dauer, ohne Fahrtzeiten)
            start_datetime = timezone.make_aware(
                datetime.combine(lesson.date, lesson.start_time)
            )
            end_datetime = start_datetime + timedelta(minutes=lesson.duration_minutes)
            
            # Wenn Endzeit in der Vergangenheit liegt, markiere zum Update
            if end_datetime < now:
                lesson.status = 'taught'
                updated_lessons.append(lesson)
        
        # Bulk-Update für Performance
        if updated_lessons:
            with transaction.atomic():
                Lesson.objects.bulk_update(
                    updated_lessons,
                    fields=['status', 'updated_at'],
                    batch_size=100
                )
        
        return len(updated_lessons)


# Alias für Rückwärtskompatibilität
LessonStatusService = LessonStatusUpdater

