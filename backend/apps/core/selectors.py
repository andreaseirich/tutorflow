"""
Selector-Layer für Einnahmenauswertungen.
Abgeleitete Monats-/Jahresauswertungen ohne eigenes Model.
"""
from decimal import Decimal
from datetime import datetime, date
from django.db.models import Sum, Count, Q
from django.utils import timezone
from apps.lessons.models import Lesson
from apps.contracts.models import Contract, ContractMonthlyPlan


class IncomeSelector:
    """Selector für Einnahmenberechnungen und -auswertungen."""

    @staticmethod
    def get_monthly_income(year: int, month: int, status: str = 'paid') -> dict:
        """
        Berechnet die Einnahmen für einen bestimmten Monat.
        
        Args:
            year: Jahr
            month: Monat (1-12)
            status: Status der Lessons ('paid' = ausgezahlt)
        
        Returns:
            Dict mit Einnahmen-Details
        """
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        lessons = Lesson.objects.filter(
            date__gte=start_date,
            date__lt=end_date,
            status=status
        ).select_related('contract')
        
        total_income = Decimal('0.00')
        lesson_count = 0
        contract_details = {}
        
        for lesson in lessons:
            hourly_rate = lesson.contract.hourly_rate
            # Berechnung basierend auf Dauer (in Stunden)
            hours = Decimal(lesson.duration_minutes) / Decimal('60')
            lesson_income = hourly_rate * hours
            total_income += lesson_income
            lesson_count += 1
            
            contract_id = lesson.contract.id
            if contract_id not in contract_details:
                contract_details[contract_id] = {
                    'contract': lesson.contract,
                    'lessons': 0,
                    'income': Decimal('0.00')
                }
            contract_details[contract_id]['lessons'] += 1
            contract_details[contract_id]['income'] += lesson_income
        
        return {
            'year': year,
            'month': month,
            'total_income': total_income,
            'lesson_count': lesson_count,
            'contract_details': list(contract_details.values()),
        }

    @staticmethod
    def get_monthly_planned_vs_actual(year: int, month: int) -> dict:
        """
        Vergleicht geplante vs. tatsächliche Einheiten und Einnahmen für einen Monat.
        
        Args:
            year: Jahr
            month: Monat (1-12)
        
        Returns:
            Dict mit planned_units, planned_amount, actual_units, actual_amount
        """
        # Geplante Einheiten aus ContractMonthlyPlan
        monthly_plans = ContractMonthlyPlan.objects.filter(year=year, month=month)
        planned_units = sum(plan.planned_units for plan in monthly_plans)
        planned_amount = Decimal('0.00')
        
        for plan in monthly_plans:
            # Berechne geplantes Einkommen basierend auf Stundensatz und Dauer
            hourly_rate = plan.contract.hourly_rate
            unit_duration_hours = Decimal(plan.contract.unit_duration_minutes) / Decimal('60')
            planned_amount += hourly_rate * unit_duration_hours * Decimal(plan.planned_units)
        
        # Tatsächliche Einheiten aus Lessons
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        lessons = Lesson.objects.filter(
            date__gte=start_date,
            date__lt=end_date
        ).select_related('contract')
        
        actual_units = lessons.count()
        actual_amount = Decimal('0.00')
        
        for lesson in lessons:
            hourly_rate = lesson.contract.hourly_rate
            hours = Decimal(lesson.duration_minutes) / Decimal('60')
            actual_amount += hourly_rate * hours
        
        return {
            'year': year,
            'month': month,
            'planned_units': planned_units,
            'planned_amount': planned_amount,
            'actual_units': actual_units,
            'actual_amount': actual_amount,
            'difference_units': actual_units - planned_units,
            'difference_amount': actual_amount - planned_amount,
        }

    @staticmethod
    def get_yearly_income(year: int, status: str = 'paid') -> dict:
        """
        Berechnet die Einnahmen für ein ganzes Jahr.
        
        Args:
            year: Jahr
            status: Status der Lessons ('paid' = ausgezahlt)
        
        Returns:
            Dict mit Einnahmen-Details pro Monat und Gesamt
        """
        monthly_incomes = []
        total_income = Decimal('0.00')
        total_lessons = 0
        
        for month in range(1, 13):
            monthly_data = IncomeSelector.get_monthly_income(year, month, status)
            monthly_incomes.append(monthly_data)
            total_income += monthly_data['total_income']
            total_lessons += monthly_data['lesson_count']
        
        return {
            'year': year,
            'total_income': total_income,
            'total_lessons': total_lessons,
            'monthly_breakdown': monthly_incomes,
        }

    @staticmethod
    def get_income_by_status(year: int = None, month: int = None) -> dict:
        """
        Gruppiert Einnahmen nach Status.
        
        Args:
            year: Optional - Jahr
            month: Optional - Monat
        
        Returns:
            Dict mit Einnahmen nach Status
        """
        query = Q()
        if year and month:
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1)
            else:
                end_date = date(year, month + 1, 1)
            query &= Q(date__gte=start_date, date__lt=end_date)
        elif year:
            query &= Q(date__year=year)
        
        lessons = Lesson.objects.filter(query).select_related('contract')
        
        status_breakdown = {}
        for status_code, status_name in Lesson.STATUS_CHOICES:
            status_lessons = lessons.filter(status=status_code)
            total_income = Decimal('0.00')
            lesson_count = status_lessons.count()
            
            for lesson in status_lessons:
                hourly_rate = lesson.contract.hourly_rate
                hours = Decimal(lesson.duration_minutes) / Decimal('60')
                total_income += hourly_rate * hours
            
            status_breakdown[status_code] = {
                'name': status_name,
                'income': total_income,
                'lesson_count': lesson_count,
            }
        
        return status_breakdown
