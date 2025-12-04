"""
Views für Lesson-CRUD-Operationen und Planungsübersicht.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import date
from apps.lessons.models import Lesson
from apps.lessons.forms import LessonForm
from apps.lessons.services import LessonQueryService, LessonConflictService


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
            lesson._conflicts = LessonConflictService.check_conflicts(lesson)
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
    success_url = reverse_lazy('lessons:list')

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
    success_url = reverse_lazy('lessons:list')

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
    success_url = reverse_lazy('lessons:list')

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
            lesson._conflicts = LessonConflictService.check_conflicts(lesson)
        
        context['year'] = year
        context['month'] = month
        return context
