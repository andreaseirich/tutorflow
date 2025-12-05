"""
Views für Dashboard und Einnahmenübersicht.
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import date
from apps.lessons.services import LessonQueryService
from apps.lessons.services import LessonConflictService
from apps.core.selectors import IncomeSelector


class DashboardView(TemplateView):
    """Dashboard mit Übersicht über heutige Stunden, Konflikte und Einnahmen."""
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        
        # Heutige Stunden
        today_lessons = LessonQueryService.get_today_lessons()
        for lesson in today_lessons:
            lesson.conflicts = LessonConflictService.check_conflicts(lesson)
        
        # Nächste Stunden
        upcoming_lessons = LessonQueryService.get_upcoming_lessons(days=7)
        for lesson in upcoming_lessons:
            lesson.conflicts = LessonConflictService.check_conflicts(lesson)
        
        # Konflikte zählen (beide QuerySets zu Listen konvertieren für Kombination)
        all_lessons = list(today_lessons) + list(upcoming_lessons)
        conflict_count = sum(1 for lesson in all_lessons if lesson.conflicts)
        
        # Einnahmen für aktuellen Monat
        current_month_income = IncomeSelector.get_monthly_income(
            now.year, now.month, status='paid'
        )
        
        # Einnahmen nach Status für aktuellen Monat
        income_by_status = IncomeSelector.get_income_by_status(
            year=now.year, month=now.month
        )
        
        # Premium status
        from apps.core.utils import is_premium_user
        context['is_premium'] = is_premium_user(self.request.user) if self.request.user.is_authenticated else False
        
        context.update({
            'today_lessons': today_lessons,
            'upcoming_lessons': upcoming_lessons,
            'conflict_count': conflict_count,
            'current_month_income': current_month_income,
            'income_by_status': income_by_status,
            'current_year': now.year,
            'current_month': now.month,
        })
        
        return context


class IncomeOverviewView(TemplateView):
    """Einnahmenübersicht mit Monats- und Jahresansicht."""
    template_name = 'core/income_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        
        # Jahr und Monat aus URL-Parametern oder aktuelles Datum
        year = int(self.request.GET.get('year', now.year))
        month = int(self.request.GET.get('month', now.month)) if 'month' in self.request.GET else None
        
        if month:
            # Monatsansicht
            monthly_income = IncomeSelector.get_monthly_income(year, month, status='paid')
            income_by_status = IncomeSelector.get_income_by_status(year=year, month=month)
            planned_vs_actual = IncomeSelector.get_monthly_planned_vs_actual(year, month)
            billing_status = IncomeSelector.get_billing_status(year=year, month=month)
            context.update({
                'view_type': 'month',
                'year': year,
                'month': month,
                'monthly_income': monthly_income,
                'income_by_status': income_by_status,
                'planned_vs_actual': planned_vs_actual,
                'billing_status': billing_status,
            })
        else:
            # Jahresansicht
            yearly_income = IncomeSelector.get_yearly_income(year, status='paid')
            income_by_status = IncomeSelector.get_income_by_status(year=year)
            billing_status = IncomeSelector.get_billing_status(year=year)
            context.update({
                'view_type': 'year',
                'year': year,
                'yearly_income': yearly_income,
                'income_by_status': income_by_status,
                'billing_status': billing_status,
            })
        
        return context
