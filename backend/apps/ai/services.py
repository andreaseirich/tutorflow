"""
High-Level-Service für LessonPlan-Generierung.
"""

from typing import Optional, Dict, Any
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.lessons.models import Lesson
from apps.lesson_plans.models import LessonPlan
from apps.ai.client import LLMClient, LLMClientError
from apps.ai.prompts import build_lesson_plan_prompt, extract_subject_from_student


class LessonPlanGenerationError(Exception):
    """Exception für Fehler bei der LessonPlan-Generierung."""

    pass


class LessonPlanService:
    """Service für die Generierung von KI-Unterrichtsplänen."""

    def __init__(self, client: Optional[LLMClient] = None):
        """
        Initialisiert den Service.

        Args:
            client: Optional LLM-Client (für Tests/Mocking)
        """
        self.client = client or LLMClient()

    def gather_context(self, lesson: Lesson) -> Dict[str, Any]:
        """
        Sammelt Kontext-Informationen für die Prompt-Generierung.

        Args:
            lesson: Lesson-Objekt

        Returns:
            Dict mit Kontext-Informationen
        """
        student = lesson.contract.student

        # Hole vorherige Lessons (max. 5, sortiert nach Datum)
        previous_lessons = Lesson.objects.filter(
            contract__student=student, date__lt=lesson.date
        ).order_by("-date")[:5]

        return {
            "previous_lessons": list(previous_lessons),
            "student_notes": student.notes,
            "contract_duration": lesson.contract.unit_duration_minutes,
        }

    def generate_lesson_plan(self, lesson: Lesson) -> LessonPlan:
        """
        Generiert einen KI-Unterrichtsplan für eine Lesson.

        Args:
            lesson: Lesson-Objekt

        Returns:
            LessonPlan-Objekt

        Raises:
            LessonPlanGenerationError: Bei Fehlern bei der Generierung
        """
        # Sammle Kontext
        context = self.gather_context(lesson)

        # Baue Prompt
        system_prompt, user_prompt = build_lesson_plan_prompt(lesson, context)

        # Rufe LLM auf
        try:
            generated_content = self.client.generate_text(
                prompt=user_prompt, system_prompt=system_prompt, max_tokens=1500, temperature=0.7
            )
        except LLMClientError as e:
            raise LessonPlanGenerationError(_("LLM error: {error}").format(error=str(e)))

        # Erstelle oder aktualisiere LessonPlan
        student = lesson.contract.student
        subject = extract_subject_from_student(student)

        lesson_plan, created = LessonPlan.objects.update_or_create(
            lesson=lesson,
            defaults={
                "student": student,
                "topic": _("Lesson plan for {date}").format(date=lesson.date),
                "subject": subject,
                "content": generated_content,
                "grade_level": student.grade or "",
                "duration_minutes": lesson.duration_minutes,
                "llm_model": settings.LLM_MODEL_NAME,
            },
        )

        return lesson_plan
