"""
Service für wiederholende Unterrichtsstunden (Recurring Lessons).
"""
from datetime import date, timedelta
from typing import List, Optional
from apps.lessons.models import Lesson
from apps.lessons.recurring_models import RecurringLesson
from apps.lessons.services import LessonConflictService
from apps.lessons.status_service import LessonStatusService


class RecurringLessonService:
    """Service für die Generierung von Lessons aus RecurringLesson-Vorlagen."""

    @staticmethod
    def generate_lessons(
        recurring_lesson: RecurringLesson,
        check_conflicts: bool = True,
        dry_run: bool = False
    ) -> dict:
        """
        Generiert Lessons für eine RecurringLesson über den Zeitraum [start_date, end_date].
        
        Args:
            recurring_lesson: Die RecurringLesson-Vorlage
            check_conflicts: Ob Konflikte geprüft werden sollen
            dry_run: Wenn True, werden keine Lessons gespeichert, nur Vorschau
        
        Returns:
            Dict mit:
            - 'created': Anzahl erstellter Lessons
            - 'skipped': Anzahl übersprungener (bereits vorhandene)
            - 'conflicts': Liste von Konflikten (wenn check_conflicts=True)
            - 'preview': Liste von Lesson-Instanzen (wenn dry_run=True)
        """
        if not recurring_lesson.is_active:
            return {'created': 0, 'skipped': 0, 'conflicts': [], 'preview': []}
        
        # Bestimme Enddatum
        end_date = recurring_lesson.end_date
        if not end_date:
            # Falls kein Enddatum, verwende Vertragsende oder 1 Jahr
            if recurring_lesson.contract.end_date:
                end_date = recurring_lesson.contract.end_date
            else:
                end_date = date(recurring_lesson.start_date.year + 1, 
                               recurring_lesson.start_date.month, 
                               recurring_lesson.start_date.day)
        
        # Aktive Wochentage
        active_weekdays = recurring_lesson.get_active_weekdays()
        if not active_weekdays:
            return {'created': 0, 'skipped': 0, 'conflicts': [], 'preview': []}
        
        # Iteriere über den Zeitraum
        current_date = recurring_lesson.start_date
        created = 0
        skipped = 0
        conflicts = []
        preview = []
        
        while current_date <= end_date:
            weekday = current_date.weekday()  # 0=Montag, 6=Sonntag
            
            if weekday in active_weekdays:
                # Prüfe, ob bereits eine Lesson für diesen Tag existiert
                existing = Lesson.objects.filter(
                    contract=recurring_lesson.contract,
                    date=current_date,
                    start_time=recurring_lesson.start_time
                ).first()
                
                if existing:
                    skipped += 1
                else:
                    # Erstelle neue Lesson (ohne Status - wird automatisch gesetzt)
                    lesson = Lesson(
                        contract=recurring_lesson.contract,
                        date=current_date,
                        start_time=recurring_lesson.start_time,
                        duration_minutes=recurring_lesson.duration_minutes,
                        location=recurring_lesson.location,
                        travel_time_before_minutes=recurring_lesson.travel_time_before_minutes,
                        travel_time_after_minutes=recurring_lesson.travel_time_after_minutes,
                        status='',  # Leer - wird automatisch gesetzt
                        notes=recurring_lesson.notes
                    )
                    
                    # Automatische Status-Setzung (vor dem Speichern)
                    LessonStatusService.update_status_for_lesson(lesson)
                    
                    if dry_run:
                        preview.append(lesson)
                    else:
                        lesson.save()
                        # Status nochmal setzen nach Speichern (falls nötig)
                        LessonStatusService.update_status_for_lesson(lesson)
                        
                        # Prüfe Konflikte
                        if check_conflicts:
                            lesson_conflicts = LessonConflictService.check_conflicts(lesson)
                            if lesson_conflicts:
                                conflicts.append({
                                    'lesson': lesson,
                                    'date': current_date,
                                    'conflicts': lesson_conflicts
                                })
                        
                        created += 1
            
            # Nächster Tag
            current_date += timedelta(days=1)
        
        result = {
            'created': created,
            'skipped': skipped,
            'conflicts': conflicts,
        }
        
        if dry_run:
            result['preview'] = preview
        
        return result

    @staticmethod
    def preview_lessons(recurring_lesson: RecurringLesson) -> List[Lesson]:
        """
        Gibt eine Vorschau der zu erzeugenden Lessons zurück (ohne Speicherung).
        
        Args:
            recurring_lesson: Die RecurringLesson-Vorlage
        
        Returns:
            Liste von Lesson-Instanzen (nicht gespeichert)
        """
        result = RecurringLessonService.generate_lessons(
            recurring_lesson,
            check_conflicts=False,
            dry_run=True
        )
        return result.get('preview', [])

