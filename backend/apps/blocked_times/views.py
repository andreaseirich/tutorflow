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

    def form_valid(self, form):
        messages.success(self.request, 'Blockzeit erfolgreich erstellt.')
        return super().form_valid(form)


class BlockedTimeUpdateView(UpdateView):
    """Blockzeit bearbeiten."""
    model = BlockedTime
    form_class = BlockedTimeForm
    template_name = 'blocked_times/blockedtime_form.html'
    success_url = reverse_lazy('blocked_times:list')

    def form_valid(self, form):
        messages.success(self.request, 'Blockzeit erfolgreich aktualisiert.')
        return super().form_valid(form)


class BlockedTimeDeleteView(DeleteView):
    """Blockzeit löschen."""
    model = BlockedTime
    template_name = 'blocked_times/blockedtime_confirm_delete.html'
    success_url = reverse_lazy('blocked_times:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Blockzeit erfolgreich gelöscht.')
        return super().delete(request, *args, **kwargs)
