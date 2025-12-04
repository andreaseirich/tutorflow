from django.db import models
from apps.locations.models import Location


class Student(models.Model):
    """Schüler mit Kontaktdaten, Schule/Klasse, Fächern und Standard-Unterrichtsort."""
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    school = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Name der Schule"
    )
    grade = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Klasse/Stufe (z. B. '10. Klasse', 'Q1')"
    )
    subjects = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Fächer (kommagetrennt, z. B. 'Mathe, Deutsch, Englisch')"
    )
    default_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        help_text="Standard-Unterrichtsort"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Zusätzliche Notizen zum Schüler"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Schüler'
        verbose_name_plural = 'Schüler'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        """Vollständiger Name des Schülers."""
        return f"{self.first_name} {self.last_name}"
