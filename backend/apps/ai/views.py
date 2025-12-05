"""
Views für AI-Funktionen (LessonPlan-Generierung).
"""
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from apps.lessons.models import Lesson
from apps.core.utils import is_premium_user
from apps.ai.services import LessonPlanService, LessonPlanGenerationError


@login_required
@require_POST
def generate_lesson_plan(request, lesson_id):
    """
    Generiert einen KI-Unterrichtsplan für eine Lesson.
    Nur für Premium-User verfügbar.
    """
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    
    # Premium-Check
    if not is_premium_user(request.user):
        messages.error(
            request,
            "Diese Funktion ist nur für Premium-User verfügbar."
        )
        return redirect('lessons:detail', pk=lesson_id)
    
    # Generiere LessonPlan
    try:
        service = LessonPlanService()
        lesson_plan = service.generate_lesson_plan(lesson)
        messages.success(
            request,
            f"Unterrichtsplan erfolgreich generiert! "
            f"Modell: {lesson_plan.llm_model or 'N/A'}"
        )
    except LessonPlanGenerationError as e:
            messages.error(
                request,
                _("The lesson plan could not be generated: {error}").format(error=str(e))
            )
    except Exception as e:
        messages.error(
            request,
            "Ein unerwarteter Fehler ist aufgetreten. Bitte versuchen Sie es später erneut."
        )
    
    return redirect('lessons:detail', pk=lesson_id)
