from django.db import models


class BlockedTime(models.Model):
    """Eigene Termine/Blockzeiten (z. B. Uni, Job, Gemeinde)."""
    
    title = models.CharField(
        max_length=200,
        help_text="Titel der Blockzeit (z. B. 'Uni-Vorlesung', 'Gemeinde')"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Beschreibung der Blockzeit"
    )
    start_datetime = models.DateTimeField(help_text="Startzeitpunkt")
    end_datetime = models.DateTimeField(help_text="Endzeitpunkt")
    is_recurring = models.BooleanField(
        default=False,
        help_text="Ist dies eine wiederkehrende Blockzeit?"
    )
    recurring_pattern = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Wiederholungsmuster (z. B. 'weekly', 'daily') - für zukünftige Erweiterung"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_datetime']
        verbose_name = 'Blockzeit'
        verbose_name_plural = 'Blockzeiten'
        indexes = [
            models.Index(fields=['start_datetime', 'end_datetime']),
        ]

    def __str__(self):
        return f"{self.title} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"
