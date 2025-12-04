from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Location(models.Model):
    """Unterrichtsort mit Name, Adresse und optionalen Koordinaten."""
    
    name = models.CharField(
        max_length=200,
        help_text="Name des Ortes (z. B. 'Zuhause', 'Schule XY')"
    )
    address = models.TextField(
        help_text="Vollständige Adresse"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Breitengrad (optional)"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Längengrad (optional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ort'
        verbose_name_plural = 'Orte'

    def __str__(self):
        return f"{self.name} ({self.address})"
