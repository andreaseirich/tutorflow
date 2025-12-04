from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.students.models import Student


class Contract(models.Model):
    """Vertrag zwischen Nachhilfelehrer und Schüler/Institut."""
    
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='contracts',
        help_text="Schüler, für den der Vertrag gilt"
    )
    institute = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Name des Instituts (falls vorhanden)"
    )
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Honorar pro Einheit in Euro"
    )
    unit_duration_minutes = models.PositiveIntegerField(
        default=60,
        help_text="Dauer einer Einheit in Minuten"
    )
    start_date = models.DateField(help_text="Vertragsbeginn")
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Vertragsende (optional, leer = unbefristet)"
    )
    planned_units_per_month = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Geplante Einheiten pro Monat (optional)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Ist der Vertrag aktiv?"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Zusätzliche Notizen zum Vertrag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', 'student']
        verbose_name = 'Vertrag'
        verbose_name_plural = 'Verträge'

    def __str__(self):
        institute_str = f" ({self.institute})" if self.institute else ""
        return f"{self.student} - {self.hourly_rate}€/Einheit{institute_str}"
