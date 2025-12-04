"""
Views für RecurringLesson-CRUD-Operationen.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.lessons.recurring_models import RecurringLesson
from apps.lessons.recurring_forms import RecurringLessonForm
from apps.lessons.recurring_service import RecurringLessonService


class RecurringLessonListView(ListView):
    """Liste aller wiederholenden Unterrichtsstunden."""
    model = RecurringLesson
    template_name = 'lessons/recurringlesson_list.html'
    context_object_name = 'recurring_lessons'
    paginate_by = 20


class RecurringLessonDetailView(DetailView):
    """Detailansicht einer wiederholenden Unterrichtsstunde."""
    model = RecurringLesson
    template_name = 'lessons/recurringlesson_detail.html'
    context_object_name = 'recurring_lesson'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Vorschau der zu erzeugenden Lessons
        preview = RecurringLessonService.preview_lessons(self.object)
        context['preview_count'] = len(preview)
        context['preview'] = preview[:10]  # Zeige nur erste 10
        return context


class RecurringLessonCreateView(CreateView):
    """Neue wiederholende Unterrichtsstunde erstellen."""
    model = RecurringLesson
    form_class = RecurringLessonForm
    template_name = 'lessons/recurringlesson_form.html'
    success_url = reverse_lazy('lessons:recurring_list')

    def form_valid(self, form):
        messages.success(self.request, 'Serientermin erfolgreich erstellt.')
        return super().form_valid(form)


class RecurringLessonUpdateView(UpdateView):
    """Wiederholende Unterrichtsstunde bearbeiten."""
    model = RecurringLesson
    form_class = RecurringLessonForm
    template_name = 'lessons/recurringlesson_form.html'
    success_url = reverse_lazy('lessons:recurring_list')

    def form_valid(self, form):
        messages.success(self.request, 'Serientermin erfolgreich aktualisiert.')
        return super().form_valid(form)


class RecurringLessonDeleteView(DeleteView):
    """Wiederholende Unterrichtsstunde löschen."""
    model = RecurringLesson
    template_name = 'lessons/recurringlesson_confirm_delete.html'
    success_url = reverse_lazy('lessons:recurring_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Serientermin erfolgreich gelöscht.')
        return super().delete(request, *args, **kwargs)


def generate_lessons_from_recurring(request, pk):
    """Generiert Lessons aus einer RecurringLesson."""
    recurring_lesson = get_object_or_404(RecurringLesson, pk=pk)
    
    result = RecurringLessonService.generate_lessons(
        recurring_lesson,
        check_conflicts=True
    )
    
    if result['created'] > 0:
        messages.success(
            request,
            f"{result['created']} Unterrichtsstunde(n) erfolgreich erstellt."
        )
    
    if result['skipped'] > 0:
        messages.info(
            request,
            f"{result['skipped']} Unterrichtsstunde(n) übersprungen (bereits vorhanden)."
        )
    
    if result['conflicts']:
        conflict_count = len(result['conflicts'])
        messages.warning(
            request,
            f"{conflict_count} Unterrichtsstunde(n) mit Konflikten erkannt. "
            f"Bitte prüfen Sie die Details."
        )
    
    return redirect('lessons:recurring_detail', pk=pk)

