from django.db import models
from apps.students.models import Student
from apps.lessons.models import Lesson


class LessonPlan(models.Model):
    """KI-generierter Unterrichtsplan mit Text und Metadaten."""
    
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='lesson_plans',
        help_text="Schüler, für den der Plan erstellt wurde"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lesson_plans',
        help_text="Verknüpfte Unterrichtsstunde (optional)"
    )
    topic = models.CharField(
        max_length=200,
        help_text="Thema des Unterrichtsplans"
    )
    subject = models.CharField(
        max_length=100,
        help_text="Fach (z. B. 'Mathe', 'Deutsch')"
    )
    content = models.TextField(
        help_text="KI-generierter Unterrichtsplan (Text)"
    )
    grade_level = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Klassenstufe (z. B. '10. Klasse')"
    )
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Geplante Dauer in Minuten"
    )
    llm_model = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Verwendetes LLM-Modell (z. B. 'gpt-4', 'claude-3')"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Unterrichtsplan'
        verbose_name_plural = 'Unterrichtspläne'
        indexes = [
            models.Index(fields=['student', '-created_at']),
        ]

    def __str__(self):
        return f"{self.student} - {self.topic} ({self.subject})"
