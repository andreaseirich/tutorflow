"""
Models für Abrechnung und Rechnungen.
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.contracts.models import Contract
from apps.lessons.models import Lesson


class Invoice(models.Model):
    """Rechnung für abgerechnete Unterrichtsstunden."""
    
    STATUS_CHOICES = [
        ('draft', 'Entwurf'),
        ('sent', 'Versendet'),
        ('paid', 'Bezahlt'),
    ]
    
    payer_name = models.CharField(
        max_length=200,
        help_text="Name des Zahlungspflichtigen"
    )
    payer_address = models.TextField(
        blank=True,
        help_text="Adresse des Zahlungspflichtigen"
    )
    contract = models.ForeignKey(
        Contract,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices',
        help_text="Zugehöriger Vertrag (optional)"
    )
    period_start = models.DateField(help_text="Beginn des Abrechnungszeitraums")
    period_end = models.DateField(help_text="Ende des Abrechnungszeitraums")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Status der Rechnung"
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Gesamtbetrag der Rechnung"
    )
    document = models.FileField(
        upload_to='invoices/',
        null=True,
        blank=True,
        help_text="Generiertes Rechnungsdokument (HTML/PDF)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Rechnung'
        verbose_name_plural = 'Rechnungen'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['period_start', 'period_end']),
        ]
    
    def __str__(self):
        return f"Rechnung {self.id} - {self.payer_name} ({self.period_start} - {self.period_end})"
    
    def calculate_total(self):
        """Berechnet den Gesamtbetrag aus allen InvoiceItems."""
        total = sum(item.amount for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount', 'updated_at'])
        return total


class InvoiceItem(models.Model):
    """Einzelposten einer Rechnung (entspricht einer Lesson)."""
    
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Zugehörige Rechnung"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoice_items',
        help_text="Zugehörige Lesson (kann später gelöscht werden)"
    )
    description = models.CharField(
        max_length=500,
        help_text="Beschreibung des Postens"
    )
    date = models.DateField(help_text="Datum der Unterrichtsstunde (Kopie)")
    duration_minutes = models.PositiveIntegerField(
        help_text="Dauer in Minuten (Kopie)"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Betrag für diesen Posten"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'description']
        verbose_name = 'Rechnungsposten'
        verbose_name_plural = 'Rechnungsposten'
    
    def __str__(self):
        return f"{self.description} - {self.amount}€"
