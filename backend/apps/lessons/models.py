from django.db import models
from django.core.validators import MinValueValidator
from apps.contracts.models import Contract

# Import RecurringLesson für Django-Erkennung
from .recurring_models import RecurringLesson


class Lesson(models.Model):
    """Nachhilfestunde mit Datum, Zeit, Status, Ort und Fahrtzeiten."""
    
    STATUS_CHOICES = [
        ('planned', 'Geplant'),
        ('taught', 'Unterrichtet'),
        ('cancelled', 'Ausgefallen'),
        ('paid', 'Ausgezahlt'),
    ]
    
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='lessons',
        help_text="Zugehöriger Vertrag"
    )
    date = models.DateField(help_text="Datum der Unterrichtsstunde")
    start_time = models.TimeField(help_text="Startzeit")
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Dauer in Minuten"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        help_text="Status der Unterrichtsstunde"
    )
    travel_time_before_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Fahrtzeit vorher in Minuten"
    )
    travel_time_after_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Fahrtzeit nachher in Minuten"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notizen zur Unterrichtsstunde"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']
        verbose_name = 'Unterrichtsstunde'
        verbose_name_plural = 'Unterrichtsstunden'
        indexes = [
            models.Index(fields=['date', 'start_time']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.contract.student} - {self.date} {self.start_time} ({self.get_status_display()})"

    @property
    def total_time_minutes(self):
        """Gesamtzeit inklusive Fahrtzeiten."""
        return self.duration_minutes + self.travel_time_before_minutes + self.travel_time_after_minutes

    @property
    def has_conflicts(self):
        """Prüft, ob diese Lesson Konflikte hat."""
        from apps.lessons.services import LessonConflictService
        return LessonConflictService.has_conflicts(self)

    def get_conflicts(self):
        """Gibt alle Konflikte dieser Lesson zurück."""
        from apps.lessons.services import LessonConflictService
        return LessonConflictService.check_conflicts(self)
