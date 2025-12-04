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
    def get_billable_lessons(period_start, period_end, contract_id=None):
        """
        Gibt alle Lessons zurück, die für eine Abrechnung in Frage kommen.
        
        Nur Lessons mit Status TAUGHT, die noch nicht in einer Invoice sind.
        Lessons mit Status PLANNED oder PAID werden ausgeschlossen.
        Eine Lesson kann nur in einer Rechnung vorkommen.
        
        Args:
            period_start: Startdatum des Zeitraums
            period_end: Enddatum des Zeitraums
            contract_id: Optional: Filter nach Vertrag-ID
            
        Returns:
            QuerySet von Lessons mit Status TAUGHT, die noch nicht in einem InvoiceItem sind
        """
        queryset = Lesson.objects.filter(
            status='taught',  # Nur unterrichtete Lessons (nicht PLANNED oder PAID)
            date__gte=period_start,
            date__lte=period_end
        ).exclude(
            invoice_items__isnull=False  # Keine Lessons, die bereits in einer Rechnung sind (1:1-Beziehung)
        ).select_related('contract', 'contract__student', 'location')
        
        if contract_id:
            queryset = queryset.filter(contract_id=contract_id)
        
        return queryset.order_by('date', 'start_time')
    
    @staticmethod
    def create_invoice_from_lessons(period_start, period_end, contract=None):
        """
        Erstellt eine Invoice mit InvoiceItems aus allen verfügbaren Lessons im Zeitraum.
        
        Automatisch werden alle Lessons mit Status TAUGHT im angegebenen Zeitraum verwendet,
        die noch nicht in einer Rechnung sind.
        
        Args:
            period_start: Startdatum
            period_end: Enddatum
            contract: Optional: Filter nach Vertrag
            
        Returns:
            Invoice-Instanz
        """
        # Lade automatisch alle abrechenbaren Lessons im Zeitraum
        contract_id = contract.id if contract else None
        lessons = InvoiceService.get_billable_lessons(period_start, period_end, contract_id)
        
        if not lessons.exists():
            raise ValueError("Keine abrechenbaren Unterrichtsstunden im angegebenen Zeitraum gefunden.")
        
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
            # Berechne Betrag basierend auf Einheiten
            # units = lesson_duration_minutes / contract_unit_duration_minutes
            # amount = units * rate_per_unit
            contract = lesson.contract
            unit_duration = Decimal(str(contract.unit_duration_minutes))
            lesson_duration = Decimal(str(lesson.duration_minutes))
            units = lesson_duration / unit_duration
            rate_per_unit = contract.hourly_rate
            amount = units * rate_per_unit
            
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
        
        # Setze Gesamtbetrag (Summe aller InvoiceItems)
        invoice.total_amount = total_amount
        invoice.save(update_fields=['total_amount', 'updated_at'])
        
        return invoice
    
    @staticmethod
    def delete_invoice(invoice: Invoice):
        """
        Löscht eine Rechnung und setzt Lessons zurück auf TAUGHT, falls sie nicht in anderen Rechnungen sind.
        
        Args:
            invoice: Die zu löschende Invoice
            
        Returns:
            Anzahl der zurückgesetzten Lessons
        """
        # Sammle alle Lessons dieser Rechnung (vor dem Löschen!)
        invoice_items = list(invoice.items.all())
        lesson_ids = [item.lesson_id for item in invoice_items if item.lesson_id]
        
        # Lösche die Invoice (CASCADE löscht automatisch alle InvoiceItems)
        invoice.delete()
        
        # Setze Lessons zurück auf TAUGHT, falls sie nicht in anderen Rechnungen sind
        reset_count = 0
        for lesson_id in lesson_ids:
            if not lesson_id:
                continue
                
            lesson = Lesson.objects.filter(pk=lesson_id).first()
            if lesson:
                # Prüfe, ob Lesson noch in anderen Rechnungen ist
                other_invoices = InvoiceItem.objects.filter(
                    lesson_id=lesson_id
                ).exists()
                
                # Nur zurücksetzen, wenn Lesson nicht in anderen Rechnungen ist
                if not other_invoices and lesson.status == 'paid':
                    lesson.status = 'taught'
                    lesson.save(update_fields=['status', 'updated_at'])
                    reset_count += 1
        
        return reset_count

