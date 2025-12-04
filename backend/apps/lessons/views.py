"""
Views für Lesson-CRUD-Operationen und Planungsübersicht.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import date, timedelta
from calendar import monthrange
from apps.lessons.models import Lesson
from apps.lessons.forms import LessonForm
from apps.lessons.services import LessonQueryService, LessonConflictService
from apps.lessons.calendar_service import CalendarService


class LessonListView(ListView):
    """Liste aller Unterrichtsstunden."""
    model = Lesson
    template_name = 'lessons/lesson_list.html'
    context_object_name = 'lessons'
    paginate_by = 30

    def get_queryset(self):
        """Erweitert Queryset um Konfliktinformationen."""
        queryset = super().get_queryset().select_related(
            'contract', 'contract__student', 'location'
        )
        # Füge Konflikt-Info hinzu
        for lesson in queryset:
            lesson.conflicts = LessonConflictService.check_conflicts(lesson)
        return queryset


class LessonDetailView(DetailView):
    """Detailansicht einer Unterrichtsstunde."""
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conflicts'] = LessonConflictService.check_conflicts(self.object)
        
        # LessonPlan-Informationen
        from apps.lesson_plans.models import LessonPlan
        from apps.core.utils import is_premium_user
        
        lesson_plans = LessonPlan.objects.filter(lesson=self.object).order_by('-created_at')
        context['lesson_plans'] = lesson_plans
        context['has_lesson_plan'] = lesson_plans.exists()
        context['latest_lesson_plan'] = lesson_plans.first() if lesson_plans.exists() else None
        context['is_premium'] = is_premium_user(self.request.user) if self.request.user.is_authenticated else False
        
        return context


class LessonCreateView(CreateView):
    """Neue Unterrichtsstunde erstellen."""
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/lesson_form.html'

    def get_initial(self):
        """Setzt initiale Werte, z. B. Datum aus Query-Parameter."""
        initial = super().get_initial()
        date_param = self.request.GET.get('date')
        if date_param:
            try:
                initial['date'] = date_param
            except ValueError:
                pass
        return initial

    def get_success_url(self):
        """Weiterleitung zurück zum Kalender mit Jahr/Monat."""
        lesson = self.object
        return reverse_lazy('lessons:calendar') + f'?year={lesson.date.year}&month={lesson.date.month}'

    def form_valid(self, form):
        lesson = form.save()
        conflicts = LessonConflictService.check_conflicts(lesson, exclude_self=False)
        if conflicts:
            messages.warning(
                self.request,
                f'Unterrichtsstunde erstellt, aber {len(conflicts)} Konflikt(e) erkannt!'
            )
        else:
            messages.success(self.request, 'Unterrichtsstunde erfolgreich erstellt.')
        return super().form_valid(form)


class LessonUpdateView(UpdateView):
    """Unterrichtsstunde bearbeiten."""
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/lesson_form.html'

    def get_success_url(self):
        """Weiterleitung zurück zum Kalender mit Jahr/Monat."""
        lesson = self.object
        return reverse_lazy('lessons:calendar') + f'?year={lesson.date.year}&month={lesson.date.month}'

    def form_valid(self, form):
        lesson = form.save()
        conflicts = LessonConflictService.check_conflicts(lesson)
        if conflicts:
            messages.warning(
                self.request,
                f'Unterrichtsstunde aktualisiert, aber {len(conflicts)} Konflikt(e) erkannt!'
            )
        else:
            messages.success(self.request, 'Unterrichtsstunde erfolgreich aktualisiert.')
        return super().form_valid(form)


class LessonDeleteView(DeleteView):
    """Unterrichtsstunde löschen."""
    model = Lesson
    template_name = 'lessons/lesson_confirm_delete.html'

    def get_success_url(self):
        """Weiterleitung zurück zum Kalender."""
        from django.utils import timezone
        today = timezone.localdate()
        return reverse_lazy('lessons:calendar') + f'?year={today.year}&month={today.month}'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Unterrichtsstunde erfolgreich gelöscht.')
        return super().delete(request, *args, **kwargs)


class LessonMonthView(ListView):
    """Monatsansicht aller Unterrichtsstunden."""
    model = Lesson
    template_name = 'lessons/lesson_month.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        """Gibt Lessons für den angegebenen Monat zurück."""
        year = int(self.kwargs.get('year', timezone.now().year))
        month = int(self.kwargs.get('month', timezone.now().month))
        return LessonQueryService.get_lessons_for_month(year, month)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = int(self.kwargs.get('year', timezone.now().year))
        month = int(self.kwargs.get('month', timezone.now().month))
        
        # Füge Konflikt-Info hinzu
        for lesson in context['lessons']:
            lesson.conflicts = LessonConflictService.check_conflicts(lesson)
        
        context['year'] = year
        context['month'] = month
        return context


class CalendarView(TemplateView):
    """Monatskalender-Ansicht für Lessons und Blockzeiten."""
    template_name = 'lessons/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        
        # Jahr und Monat aus URL-Parametern oder aktuelles Datum
        year = int(self.request.GET.get('year', now.year))
        month = int(self.request.GET.get('month', now.month))
        
        # Lade Kalenderdaten
        calendar_data = CalendarService.get_calendar_data(year, month)
        
        # Erstelle Kalender-Grid
        first_day = date(year, month, 1)
        last_day = date(year, month, monthrange(year, month)[1])
        
        # Erster Wochentag (0=Montag, 6=Sonntag)
        first_weekday = first_day.weekday()
        
        # Erstelle Kalender-Wochen
        weeks = []
        current_date = first_day - timedelta(days=first_weekday)  # Starte am Montag der ersten Woche
        
        while current_date <= last_day or len(weeks) == 0 or current_date.weekday() != 0:
            week = []
            for day in range(7):
                day_date = current_date + timedelta(days=day)
                week.append({
                    'date': day_date,
                    'is_current_month': day_date.month == month,
                    'lessons': calendar_data['lessons_by_date'].get(day_date, []),
                    'blocked_times': calendar_data['blocked_times_by_date'].get(day_date, []),
                })
            weeks.append(week)
            current_date += timedelta(days=7)
            
            # Stoppe, wenn wir über den Monat hinaus sind
            if current_date > last_day and current_date.weekday() == 0:
                break
        
        context.update({
            'year': year,
            'month': month,
            'weeks': weeks,
            'conflicts_by_lesson': calendar_data['conflicts_by_lesson'],
            'month_names': ['', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                           'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
            'weekday_names': ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'],
        })
        
        # Navigation
        if month == 1:
            prev_year, prev_month = year - 1, 12
        else:
            prev_year, prev_month = year, month - 1
        
        if month == 12:
            next_year, next_month = year + 1, 1
        else:
            next_year, next_month = year, month + 1
        
        context['prev_year'] = prev_year
        context['prev_month'] = prev_month
        context['next_year'] = next_year
        context['next_month'] = next_month
        
        return context
