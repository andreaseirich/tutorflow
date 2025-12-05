from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from apps.contracts.models import Contract

# Import RecurringLesson für Django-Erkennung
from .recurring_models import RecurringLesson


class Lesson(models.Model):
    """Tutoring lesson with date, time, status, and travel times."""
    
    STATUS_CHOICES = [
        ('planned', _('Planned')),
        ('taught', _('Taught')),
        ('cancelled', _('Cancelled')),
        ('paid', _('Paid')),
    ]
    
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='lessons',
        help_text=_("Associated contract")
    )
    date = models.DateField(help_text=_("Lesson date"))
    start_time = models.TimeField(help_text=_("Start time"))
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text=_("Duration in minutes")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        help_text=_("Lesson status")
    )
    travel_time_before_minutes = models.PositiveIntegerField(
        default=0,
        help_text=_("Travel time before in minutes")
    )
    travel_time_after_minutes = models.PositiveIntegerField(
        default=0,
        help_text=_("Travel time after in minutes")
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text=_("Notes for the lesson")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
        indexes = [
            models.Index(fields=['date', 'start_time']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.contract.student} - {self.date} {self.start_time} ({self.get_status_display()})"

    @property
    def total_time_minutes(self):
        """Total time including travel times."""
        return self.duration_minutes + self.travel_time_before_minutes + self.travel_time_after_minutes

    @property
    def has_conflicts(self):
        """Checks if this lesson has conflicts."""
        from apps.lessons.services import LessonConflictService
        return LessonConflictService.has_conflicts(self)

    def get_conflicts(self):
        """Returns all conflicts for this lesson."""
        from apps.lessons.services import LessonConflictService
        return LessonConflictService.check_conflicts(self)
