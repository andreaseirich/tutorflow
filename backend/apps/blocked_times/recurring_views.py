"""
Views für RecurringBlockedTime-CRUD-Operationen.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.blocked_times.recurring_models import RecurringBlockedTime
from apps.blocked_times.recurring_forms import RecurringBlockedTimeForm
from apps.blocked_times.recurring_service import RecurringBlockedTimeService


class RecurringBlockedTimeDetailView(DetailView):
    """Detailansicht einer wiederholenden Blockzeit."""
    model = RecurringBlockedTime
    template_name = 'blocked_times/recurring_blockedtime_detail.html'
    context_object_name = 'recurring_blocked_time'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Vorschau der zu erzeugenden BlockedTime-Einträge
        preview = RecurringBlockedTimeService.preview_blocked_times(self.object)
        context['preview'] = preview
        return context


class RecurringBlockedTimeCreateView(CreateView):
    """Neue wiederholende Blockzeit erstellen."""
    model = RecurringBlockedTime
    form_class = RecurringBlockedTimeForm
    template_name = 'blocked_times/recurring_blockedtime_form.html'

    def get_success_url(self):
        """Weiterleitung zurück zum Kalender."""
        from django.utils import timezone
        now = timezone.now()
        return reverse_lazy('lessons:calendar') + f'?year={now.year}&month={now.month}'

    def form_valid(self, form):
        messages.success(self.request, 'Wiederholende Blockzeit erfolgreich erstellt.')
        return super().form_valid(form)


class RecurringBlockedTimeUpdateView(UpdateView):
    """Wiederholende Blockzeit bearbeiten."""
    model = RecurringBlockedTime
    form_class = RecurringBlockedTimeForm
    template_name = 'blocked_times/recurring_blockedtime_form.html'

    def get_success_url(self):
        """Weiterleitung zurück zum Kalender."""
        from django.utils import timezone
        now = timezone.now()
        return reverse_lazy('lessons:calendar') + f'?year={now.year}&month={now.month}'

    def form_valid(self, form):
        messages.success(self.request, 'Wiederholende Blockzeit erfolgreich aktualisiert.')
        return super().form_valid(form)


class RecurringBlockedTimeDeleteView(DeleteView):
    """Wiederholende Blockzeit löschen."""
    model = RecurringBlockedTime
    template_name = 'blocked_times/recurring_blockedtime_confirm_delete.html'

    def get_success_url(self):
        """Weiterleitung zurück zum Kalender."""
        from django.utils import timezone
        now = timezone.now()
        return reverse_lazy('lessons:calendar') + f'?year={now.year}&month={now.month}'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Wiederholende Blockzeit erfolgreich gelöscht.')
        return super().delete(request, *args, **kwargs)


class RecurringBlockedTimeGenerateView(DetailView):
    """Generiert BlockedTime-Einträge aus einer RecurringBlockedTime."""
    model = RecurringBlockedTime
    template_name = 'blocked_times/recurring_blockedtime_generate.html'

    def post(self, request, *args, **kwargs):
        recurring_blocked_time = self.get_object()
        check_conflicts = request.POST.get('check_conflicts', 'on') == 'on'
        
        result = RecurringBlockedTimeService.generate_blocked_times(
            recurring_blocked_time,
            check_conflicts=check_conflicts,
            dry_run=False
        )
        
        if result['conflicts']:
            messages.warning(
                request,
                f"{result['created']} Blockzeiten erstellt, "
                f"{result['skipped']} übersprungen, "
                f"{len(result['conflicts'])} Konflikt(e) erkannt!"
            )
        else:
            messages.success(
                request,
                f"{result['created']} Blockzeiten erfolgreich erstellt, "
                f"{result['skipped']} übersprungen."
            )
        
        return redirect('blocked_times:recurring_detail', pk=recurring_blocked_time.pk)

