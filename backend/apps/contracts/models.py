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


class ContractMonthlyPlan(models.Model):
    """Monatliche Planung für einen Vertrag - explizite geplante Einheiten pro Monat."""
    
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='monthly_plans',
        help_text="Zugehöriger Vertrag"
    )
    year = models.PositiveIntegerField(help_text="Jahr")
    month = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Monat (1-12)"
    )
    planned_units = models.PositiveIntegerField(
        default=0,
        help_text="Geplante Einheiten für diesen Monat"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['year', 'month']
        unique_together = [['contract', 'year', 'month']]
        verbose_name = 'Monatlicher Vertragsplan'
        verbose_name_plural = 'Monatliche Vertragspläne'

    def __str__(self):
        return f"{self.contract} - {self.year}-{self.month:02d}: {self.planned_units} Einheiten"
