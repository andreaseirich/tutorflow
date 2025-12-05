"""
Views für Lesson-CRUD-Operationen und Planungsübersicht.
"""
from django.shortcuts import get_object_or_404, redirect
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
            'contract', 'contract__student'
        )
        # Füge Konflikt-Info hinzu
        for lesson in queryset:
            lesson.conflicts = LessonConflictService.check_conflicts(lesson)
        return queryset




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
        if hasattr(self, 'object') and self.object:
            lesson = self.object
            return reverse_lazy('lessons:week') + f'?year={lesson.date.year}&month={lesson.date.month}&day={lesson.date.day}'
        # Fallback
        return reverse_lazy('lessons:week')

    def form_valid(self, form):
        from django.utils.translation import gettext_lazy as _
        from apps.lessons.recurring_models import RecurringLesson
        from apps.lessons.recurring_service import RecurringLessonService
        
        is_recurring = form.cleaned_data.get('is_recurring', False)
        
        if is_recurring:
            # Create RecurringLesson instead of single lesson
            recurrence_type = form.cleaned_data.get('recurrence_type')
            recurrence_end_date = form.cleaned_data.get('recurrence_end_date')
            recurrence_weekdays = form.cleaned_data.get('recurrence_weekdays', [])
            
            if not recurrence_type or not recurrence_weekdays:
                form.add_error('is_recurring', _('Please select a recurrence pattern and at least one weekday.'))
                return self.form_invalid(form)
            
            # Create RecurringLesson
            recurring_lesson = RecurringLesson.objects.create(
                contract=form.cleaned_data['contract'],
                start_date=form.cleaned_data['date'],
                end_date=recurrence_end_date,
                start_time=form.cleaned_data['start_time'],
                duration_minutes=form.cleaned_data['duration_minutes'],
                travel_time_before_minutes=form.cleaned_data.get('travel_time_before_minutes', 0),
                travel_time_after_minutes=form.cleaned_data.get('travel_time_after_minutes', 0),
                recurrence_type=recurrence_type,
                notes=form.cleaned_data.get('notes', ''),
                monday='0' in recurrence_weekdays,
                tuesday='1' in recurrence_weekdays,
                wednesday='2' in recurrence_weekdays,
                thursday='3' in recurrence_weekdays,
                friday='4' in recurrence_weekdays,
                saturday='5' in recurrence_weekdays,
                sunday='6' in recurrence_weekdays,
            )
            
            # Generate lessons from recurring lesson
            result = RecurringLessonService.generate_lessons(
                recurring_lesson,
                check_conflicts=True,
                dry_run=False
            )
            
            # Set self.object to first generated lesson for redirect
            generated_lessons = Lesson.objects.filter(
                contract=form.cleaned_data['contract'],
                date=form.cleaned_data['date'],
                start_time=form.cleaned_data['start_time']
            ).order_by('date', 'start_time')
            
            if generated_lessons.exists():
                self.object = generated_lessons.first()
            else:
                # Fallback: create single lesson
                self.object = form.save()
                LessonStatusService.update_status_for_lesson(self.object)
            
            messages.success(
                self.request,
                _('Recurring lesson created and {count} lesson(s) generated.').format(
                    count=result.get('created', 0)
                )
            )
            
            if result.get('conflicts'):
                messages.warning(
                    self.request,
                    _('{count} conflict(s) detected in generated lessons.').format(
                        count=len(result.get('conflicts', []))
                    )
                )
        else:
            # Create single lesson as before
            lesson = form.save()
            self.object = lesson
            
            # Automatische Status-Setzung
            LessonStatusService.update_status_for_lesson(lesson)
            
            conflicts = LessonConflictService.check_conflicts(lesson, exclude_self=False)
            if conflicts:
                messages.warning(
                    self.request,
                    _('Lesson created, but {count} conflict(s) detected!').format(count=len(conflicts))
                )
            else:
                messages.success(self.request, _('Lesson successfully created.'))
        
        return super().form_valid(form)


class LessonUpdateView(UpdateView):
    """Unterrichtsstunde bearbeiten."""
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/lesson_form.html'

    def get_success_url(self):
        """Weiterleitung zurück zur Wochenansicht."""
        lesson = self.object
        # Verwende year/month/day aus Request, falls vorhanden, sonst aus Lesson-Datum
        year = int(self.request.GET.get('year', lesson.date.year))
        month = int(self.request.GET.get('month', lesson.date.month))
        day = self.request.GET.get('day', lesson.date.day)
        return reverse_lazy('lessons:week') + f'?year={year}&month={month}&day={day}'

    def form_valid(self, form):
        from django.utils.translation import gettext_lazy as _
        from apps.lessons.services import recalculate_conflicts_for_affected_lessons
        
        lesson = form.save()
        
        # Automatische Status-Setzung
        LessonStatusService.update_status_for_lesson(lesson)
        
        # Recalculate conflicts for this lesson and affected lessons
        recalculate_conflicts_for_affected_lessons(lesson)
        
        conflicts = LessonConflictService.check_conflicts(lesson)
        if conflicts:
            messages.warning(
                self.request,
                _('Lesson updated, but {count} conflict(s) detected!').format(count=len(conflicts))
            )
        else:
            messages.success(self.request, _('Lesson successfully updated.'))
        return super().form_valid(form)


class LessonDetailView(DetailView):
    """Detailansicht einer Unterrichtsstunde mit Konfliktinformationen und Premium-Features."""
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
        
        # LessonPlan-Informationen
        from apps.lesson_plans.models import LessonPlan
        from apps.core.utils import is_premium_user
        
        lesson_plans = LessonPlan.objects.filter(lesson=lesson).order_by('-created_at')
        
        context.update({
            'conflicts': conflicts,
            'conflict_lessons': conflict_lessons,
            'conflict_blocked_times': conflict_blocked_times,
            'quota_conflicts': quota_conflicts,
            'has_conflicts': len(conflicts) > 0,
            'lesson_plans': lesson_plans,
            'has_lesson_plan': lesson_plans.exists(),
            'latest_lesson_plan': lesson_plans.first() if lesson_plans.exists() else None,
            'is_premium': is_premium_user(self.request.user) if self.request.user.is_authenticated else False,
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
        quota_conflicts = []
        
        for conflict in conflicts:
            if conflict['type'] == 'lesson':
                conflict_lessons.append(conflict['object'])
            elif conflict['type'] == 'blocked_time':
                conflict_blocked_times.append(conflict['object'])
            elif conflict['type'] == 'quota':
                quota_conflicts.append(conflict)
        
        context.update({
            'lesson': lesson,
            'conflicts': conflicts,
            'conflict_lessons': conflict_lessons,
            'conflict_blocked_times': conflict_blocked_times,
            'quota_conflicts': quota_conflicts,
            'has_conflicts': len(conflicts) > 0,
        })
        
        return context


class LessonDeleteView(DeleteView):
    """Unterrichtsstunde löschen."""
    model = Lesson
    template_name = 'lessons/lesson_confirm_delete.html'

    def get_success_url(self):
        """Weiterleitung zurück zur Wochenansicht."""
        lesson = self.object
        year = int(self.request.GET.get('year', lesson.date.year))
        month = int(self.request.GET.get('month', lesson.date.month))
        day = self.request.GET.get('day', lesson.date.day)
        return reverse_lazy('lessons:week') + f'?year={year}&month={month}&day={day}'

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
    """Redirect to week view - legacy calendar view."""
    
    def get(self, request, *args, **kwargs):
        """Redirect to week view with appropriate parameters."""
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        
        year_param = request.GET.get('year')
        month_param = request.GET.get('month')
        day_param = request.GET.get('day')
        
        if year_param and month_param:
            year = int(year_param)
            month = int(month_param)
            day = int(day_param) if day_param else 1
        else:
            # Fallback to today
            now = timezone.now()
            year = now.year
            month = now.month
            day = now.day
        
        url = reverse('lessons:week') + f'?year={year}&month={month}&day={day}'
        return HttpResponseRedirect(url)
