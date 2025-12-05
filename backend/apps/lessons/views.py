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
from apps.lessons.week_service import WeekService
from apps.lessons.status_service import LessonStatusService


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
        """Setzt initiale Werte, z. B. Datum und Zeiten aus Query-Parametern."""
        initial = super().get_initial()
        
        # Unterstützung für start/end aus Drag-to-Create
        start_param = self.request.GET.get('start')
        end_param = self.request.GET.get('end')
        
        if start_param and end_param:
            try:
                from datetime import datetime
                start_dt = datetime.fromisoformat(start_param.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end_param.replace('Z', '+00:00'))
                
                # Konvertiere zu timezone-aware, falls nötig
                if timezone.is_naive(start_dt):
                    start_dt = timezone.make_aware(start_dt)
                if timezone.is_naive(end_dt):
                    end_dt = timezone.make_aware(end_dt)
                
                initial['date'] = start_dt.date()
                initial['start_time'] = start_dt.time()
                
                # Berechne Dauer in Minuten
                duration = (end_dt - start_dt).total_seconds() / 60
                initial['duration_minutes'] = int(duration)
                
                return initial
            except (ValueError, TypeError):
                pass
        
        # Fallback: Normale Datum-Parameter
        date_param = self.request.GET.get('date')
        if date_param:
            try:
                parsed_date = date.fromisoformat(date_param)
                initial['date'] = parsed_date
            except (ValueError, TypeError):
                year_param = self.request.GET.get('year')
                month_param = self.request.GET.get('month')
                if year_param and month_param:
                    try:
                        initial['date'] = date(int(year_param), int(month_param), 1)
                    except (ValueError, TypeError):
                        initial['date'] = timezone.localdate()
                else:
                    initial['date'] = timezone.localdate()
        else:
            year_param = self.request.GET.get('year')
            month_param = self.request.GET.get('month')
            if year_param and month_param:
                try:
                    initial['date'] = date(int(year_param), int(month_param), 1)
                except (ValueError, TypeError):
                    initial['date'] = timezone.localdate()
            else:
                initial['date'] = timezone.localdate()
        return initial

    def get_success_url(self):
        """Weiterleitung zurück zur Wochenansicht."""
        lesson = self.object
        return reverse_lazy('lessons:week') + f'?year={lesson.date.year}&month={lesson.date.month}&day={lesson.date.day}'

    def form_valid(self, form):
        lesson = form.save()
        
        # Automatische Status-Setzung
        LessonStatusService.update_status_for_lesson(lesson)
        
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
        # Verwende year/month aus Request, falls vorhanden, sonst aus Lesson-Datum
        year = int(self.request.GET.get('year', lesson.date.year))
        month = int(self.request.GET.get('month', lesson.date.month))
        return reverse_lazy('lessons:calendar') + f'?year={year}&month={month}'

    def form_valid(self, form):
        lesson = form.save()
        
        # Automatische Status-Setzung
        LessonStatusService.update_status_for_lesson(lesson)
        
        conflicts = LessonConflictService.check_conflicts(lesson)
        if conflicts:
            messages.warning(
                self.request,
                f'Unterrichtsstunde aktualisiert, aber {len(conflicts)} Konflikt(e) erkannt!'
            )
        else:
            messages.success(self.request, 'Unterrichtsstunde erfolgreich aktualisiert.')
        return super().form_valid(form)


class LessonDetailView(DetailView):
    """Detailansicht einer Unterrichtsstunde mit Konfliktinformationen."""
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.object
        
        # Konflikte laden
        conflicts = LessonConflictService.check_conflicts(lesson, exclude_self=True)
        
        # Konflikt-Lessons extrahieren
        conflict_lessons = []
        conflict_blocked_times = []
        quota_conflicts = []
        
        for conflict in conflicts:
            if conflict['type'] == 'lesson':
                conflict_lessons.append(conflict['object'])
            elif conflict['type'] == 'blocked_time':
                conflict_blocked_times.append(conflict['object'])
            elif conflict['type'] == 'quota':
                quota_conflicts.append(conflict)
        
        context.update({
            'conflicts': conflicts,
            'conflict_lessons': conflict_lessons,
            'conflict_blocked_times': conflict_blocked_times,
            'quota_conflicts': quota_conflicts,
            'has_conflicts': len(conflicts) > 0,
        })
        
        return context


class ConflictDetailView(TemplateView):
    """Detailansicht für Konflikte einer Lesson."""
    template_name = 'lessons/conflict_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson_id = self.kwargs.get('pk')
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        
        # Konflikte laden
        conflicts = LessonConflictService.check_conflicts(lesson, exclude_self=True)
        
        # Konflikt-Lessons extrahieren
        conflict_lessons = []
        conflict_blocked_times = []
        
        for conflict in conflicts:
            if conflict['type'] == 'lesson':
                conflict_lessons.append(conflict['object'])
            elif conflict['type'] == 'blocked_time':
                conflict_blocked_times.append(conflict['object'])
        
        context.update({
            'lesson': lesson,
            'conflicts': conflicts,
            'conflict_lessons': conflict_lessons,
            'conflict_blocked_times': conflict_blocked_times,
        })
        
        return context


class LessonDeleteView(DeleteView):
    """Unterrichtsstunde löschen."""
    model = Lesson
    template_name = 'lessons/lesson_confirm_delete.html'

    def get_success_url(self):
        """Weiterleitung zurück zum Kalender."""
        lesson = self.object
        return reverse_lazy('lessons:calendar') + f'?year={lesson.date.year}&month={lesson.date.month}'

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


class WeekView(TemplateView):
    """Wochenansicht für Lessons und Blockzeiten."""
    template_name = 'lessons/week.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Jahr, Monat und Tag aus URL-Parametern (Fallback: aktuelles Datum)
        year_param = self.request.GET.get('year')
        month_param = self.request.GET.get('month')
        day_param = self.request.GET.get('day')
        
        if year_param and month_param and day_param:
            year = int(year_param)
            month = int(month_param)
            day = int(day_param)
        else:
            # Fallback: aktuelles Datum
            now = timezone.now()
            year = now.year
            month = now.month
            day = now.day
        
        # Lade Wochen-Daten
        week_data = WeekService.get_week_data(year, month, day)
        
        # Navigation: Vorige/Nächste Woche
        week_start = week_data['week_start']
        prev_week = week_start - timedelta(days=7)
        next_week = week_start + timedelta(days=7)
        
        # Erstelle Wochentage-Liste
        weekdays = []
        weekday_names = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        weekday_names_short = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        
        for i in range(7):
            day_date = week_start + timedelta(days=i)
            weekdays.append({
                'date': day_date,
                'name': weekday_names[i],
                'name_short': weekday_names_short[i],
                'lessons': week_data['lessons_by_date'].get(day_date, []),
                'blocked_times': week_data['blocked_times_by_date'].get(day_date, []),
            })
        
        # Heute für Template-Vergleich
        today = timezone.localdate()
        
        # Stundenliste für Template (8-22)
        hours = list(range(8, 23))
        
        context.update({
            'week_start': week_start,
            'week_end': week_data['week_end'],
            'weekdays': weekdays,
            'conflicts_by_lesson': week_data['conflicts_by_lesson'],
            'prev_week': prev_week,
            'next_week': next_week,
            'today': today,
            'hours': hours,
        })
        
        return context


class CalendarView(TemplateView):
    """Monatskalender-Ansicht für Lessons und Blockzeiten."""
    template_name = 'lessons/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Jahr und Monat ausschließlich aus URL-Parametern (Fallback: aktuelles Datum)
        year_param = self.request.GET.get('year')
        month_param = self.request.GET.get('month')
        
        if year_param and month_param:
            year = int(year_param)
            month = int(month_param)
        else:
            # Fallback nur wenn Parameter fehlen
            now = timezone.now()
            year = now.year
            month = now.month
        
        # Zentrale Variable: aktueller Monat
        current_month_date = date(year, month, 1)
        
        # Lade Kalenderdaten
        calendar_data = CalendarService.get_calendar_data(year, month)
        
        # Erstelle Kalender-Grid
        last_day = date(year, month, monthrange(year, month)[1])
        
        # Erster Wochentag (0=Montag, 6=Sonntag)
        first_weekday = current_month_date.weekday()
        
        # Erstelle Kalender-Wochen
        weeks = []
        current_date = current_month_date - timedelta(days=first_weekday)  # Starte am Montag der ersten Woche
        
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
        
        # Monatsname aus current_month_date ableiten
        month_names = ['', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                      'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
        month_label = month_names[month]
        
        # Navigation basierend auf current_month_date
        if month == 1:
            prev_year, prev_month = year - 1, 12
        else:
            prev_year, prev_month = year, month - 1
        
        if month == 12:
            next_year, next_month = year + 1, 1
        else:
            next_year, next_month = year, month + 1
        
        # Heute für Template-Vergleich
        today = timezone.localdate()
        
        context.update({
            'year': year,
            'month': month,
            'month_label': month_label,
            'weeks': weeks,
            'conflicts_by_lesson': calendar_data['conflicts_by_lesson'],
            'month_names': month_names,
            'weekday_names': ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'],
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,
            'today': today,
        })
        
        return context
