"""
Models für wiederholende Unterrichtsstunden (Serientermine).
"""
from django.db import models
from django.core.validators import MinValueValidator
from apps.contracts.models import Contract


class RecurringLesson(models.Model):
    """Wiederholende Unterrichtsstunde - Vorlage für Serientermine."""
    
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='recurring_lessons',
        help_text="Zugehöriger Vertrag"
    )
    start_date = models.DateField(help_text="Startdatum der Serie")
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Enddatum der Serie (optional, leer = bis Vertragsende)"
    )
    start_time = models.TimeField(help_text="Startzeit")
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Dauer in Minuten"
    )
    travel_time_before_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Fahrtzeit vorher in Minuten"
    )
    travel_time_after_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Fahrtzeit nachher in Minuten"
    )
    # Wiederholungsart
    RECURRENCE_TYPE_CHOICES = [
        ('weekly', 'Wöchentlich'),
        ('biweekly', 'Alle 2 Wochen'),
        ('monthly', 'Monatlich'),
    ]
    recurrence_type = models.CharField(
        max_length=20,
        choices=RECURRENCE_TYPE_CHOICES,
        default='weekly',
        help_text="Wiederholungsart: Wöchentlich, alle 2 Wochen oder monatlich"
    )
    # Wochentage als Boolean-Felder
    monday = models.BooleanField(default=False, help_text="Montag")
    tuesday = models.BooleanField(default=False, help_text="Dienstag")
    wednesday = models.BooleanField(default=False, help_text="Mittwoch")
    thursday = models.BooleanField(default=False, help_text="Donnerstag")
    friday = models.BooleanField(default=False, help_text="Freitag")
    saturday = models.BooleanField(default=False, help_text="Samstag")
    sunday = models.BooleanField(default=False, help_text="Sonntag")
    is_active = models.BooleanField(
        default=True,
        help_text="Ist die Serie aktiv?"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notizen zur Serie"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', 'contract']
        verbose_name = 'Wiederholende Unterrichtsstunde'
        verbose_name_plural = 'Wiederholende Unterrichtsstunden'

    def __str__(self):
        weekdays = self.get_active_weekdays_display()
        return f"{self.contract.student} - {weekdays} {self.start_time} (ab {self.start_date})"

    def get_active_weekdays(self):
        """Gibt eine Liste der aktiven Wochentage zurück (0=Montag, 6=Sonntag)."""
        weekdays = []
        if self.monday:
            weekdays.append(0)
        if self.tuesday:
            weekdays.append(1)
        if self.wednesday:
            weekdays.append(2)
        if self.thursday:
            weekdays.append(3)
        if self.friday:
            weekdays.append(4)
        if self.saturday:
            weekdays.append(5)
        if self.sunday:
            weekdays.append(6)
        return weekdays

    def get_active_weekdays_display(self):
        """Gibt eine lesbare Darstellung der aktiven Wochentage zurück."""
        weekday_names = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        active = [weekday_names[i] for i in self.get_active_weekdays()]
        return ', '.join(active) if active else 'Keine'

