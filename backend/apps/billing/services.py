"""
Services für Billing-Funktionalität.
"""
from datetime import datetime
from decimal import Decimal
from django.utils import timezone
from apps.billing.models import Invoice, InvoiceItem
from apps.lessons.models import Lesson


class InvoiceService:
    """Service für Invoice-Operationen."""
    
    @staticmethod
    def get_billable_lessons(period_start, period_end, contract=None):
        """
        Gibt alle Lessons zurück, die für eine Abrechnung in Frage kommen.
        
        Args:
            period_start: Startdatum des Zeitraums
            period_end: Enddatum des Zeitraums
            contract: Optional: Filter nach Vertrag
            
        Returns:
            QuerySet von Lessons mit Status TAUGHT, die noch nicht in einer Invoice sind
        """
        queryset = Lesson.objects.filter(
            status='taught',
            date__gte=period_start,
            date__lte=period_end
        ).exclude(
            invoice_items__isnull=False
        ).select_related('contract', 'contract__student', 'location')
        
        if contract:
            queryset = queryset.filter(contract=contract)
        
        return queryset.order_by('date', 'start_time')
    
    @staticmethod
    def create_invoice_from_lessons(lesson_ids, period_start, period_end, contract=None):
        """
        Erstellt eine Invoice mit InvoiceItems aus ausgewählten Lessons.
        
        Args:
            lesson_ids: Liste von Lesson-IDs
            period_start: Startdatum
            period_end: Enddatum
            contract: Optional: Vertrag
            
        Returns:
            Invoice-Instanz
        """
        lessons = Lesson.objects.filter(id__in=lesson_ids, status='taught')
        
        if not lessons.exists():
            raise ValueError("Keine gültigen Lessons gefunden.")
        
        # Bestimme payer_name und payer_address
        if contract:
            payer_name = contract.student.full_name
            payer_address = getattr(contract.student, 'address', '') or ""
        else:
            # Nehme den ersten Vertrag als Basis
            first_lesson = lessons.first()
            payer_name = first_lesson.contract.student.full_name
            payer_address = getattr(first_lesson.contract.student, 'address', '') or ""
        
        # Erstelle Invoice
        invoice = Invoice.objects.create(
            payer_name=payer_name,
            payer_address=payer_address,
            contract=contract or lessons.first().contract,
            period_start=period_start,
            period_end=period_end,
            status='draft'
        )
        
        # Erstelle InvoiceItems
        total_amount = Decimal('0.00')
        for lesson in lessons:
            # Berechne Betrag basierend auf Vertrag
            hourly_rate = lesson.contract.hourly_rate
            hours = Decimal(str(lesson.duration_minutes)) / Decimal('60')
            amount = hourly_rate * hours
            
            InvoiceItem.objects.create(
                invoice=invoice,
                lesson=lesson,
                description=f"Unterrichtsstunde {lesson.date} {lesson.start_time.strftime('%H:%M')} - {lesson.contract.student.full_name}",
                date=lesson.date,
                duration_minutes=lesson.duration_minutes,
                amount=amount
            )
            
            total_amount += amount
            
            # Markiere Lesson als abgerechnet (Status PAID)
            lesson.status = 'paid'
            lesson.save(update_fields=['status', 'updated_at'])
        
        # Setze Gesamtbetrag
        invoice.total_amount = total_amount
        invoice.save(update_fields=['total_amount', 'updated_at'])
        
        return invoice

