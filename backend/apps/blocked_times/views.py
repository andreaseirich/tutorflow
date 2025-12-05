"""
Views für BlockedTime-CRUD-Operationen.
"""
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.blocked_times.models import BlockedTime
from apps.blocked_times.forms import BlockedTimeForm


class BlockedTimeListView(ListView):
    """Liste aller Blockzeiten."""
    model = BlockedTime
    template_name = 'blocked_times/blockedtime_list.html'
    context_object_name = 'blocked_times'
    paginate_by = 30


class BlockedTimeDetailView(DetailView):
    """Detailansicht einer Blockzeit."""
    model = BlockedTime
    template_name = 'blocked_times/blockedtime_detail.html'
    context_object_name = 'blocked_time'


class BlockedTimeCreateView(CreateView):
    """Neue Blockzeit erstellen."""
    model = BlockedTime
    form_class = BlockedTimeForm
    template_name = 'blocked_times/blockedtime_form.html'
    success_url = reverse_lazy('blocked_times:list')

    def get_initial(self):
        """Setzt initiale Werte, z. B. Datum aus Query-Parameter."""
        initial = super().get_initial()
        date_param = self.request.GET.get('date')
        if date_param:
            from datetime import datetime
            from django.utils import timezone
            try:
                parsed_date = datetime.fromisoformat(date_param).date()
                # Setze start_datetime und end_datetime auf den Tag
                initial['start_datetime'] = timezone.make_aware(
                    datetime.combine(parsed_date, datetime.min.time().replace(hour=9))
                )
                initial['end_datetime'] = timezone.make_aware(
                    datetime.combine(parsed_date, datetime.min.time().replace(hour=10))
                )
            except (ValueError, TypeError):
                pass
        return initial

    def get_success_url(self):
        """Weiterleitung zurück zum Kalender mit Jahr/Monat."""
        blocked_time = self.object
        year = blocked_time.start_datetime.year
        month = blocked_time.start_datetime.month
        return reverse_lazy('lessons:calendar') + f'?year={year}&month={month}'

    def form_valid(self, form):
        messages.success(self.request, 'Blockzeit erfolgreich erstellt.')
        return super().form_valid(form)


class BlockedTimeUpdateView(UpdateView):
    """Blockzeit bearbeiten."""
    model = BlockedTime
    form_class = BlockedTimeForm
    template_name = 'blocked_times/blockedtime_form.html'
    success_url = reverse_lazy('blocked_times:list')

    def get_success_url(self):
        """Weiterleitung zurück zum Kalender mit Jahr/Monat."""
        blocked_time = self.object
        year = blocked_time.start_datetime.year
        month = blocked_time.start_datetime.month
        # Verwende year/month aus Request, falls vorhanden, sonst aus BlockedTime-Datum
        year = int(self.request.GET.get('year', year))
        month = int(self.request.GET.get('month', month))
        return reverse_lazy('lessons:calendar') + f'?year={year}&month={month}'

    def form_valid(self, form):
        messages.success(self.request, 'Blockzeit erfolgreich aktualisiert.')
        return super().form_valid(form)


class BlockedTimeDeleteView(DeleteView):
    """Blockzeit löschen."""
    model = BlockedTime
    template_name = 'blocked_times/blockedtime_confirm_delete.html'
    success_url = reverse_lazy('blocked_times:list')

    def get_success_url(self):
        """Weiterleitung zurück zum Kalender mit Jahr/Monat."""
        blocked_time = self.object
        year = blocked_time.start_datetime.year
        month = blocked_time.start_datetime.month
        return reverse_lazy('lessons:calendar') + f'?year={year}&month={month}'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Blockzeit erfolgreich gelöscht.')
        return super().delete(request, *args, **kwargs)
