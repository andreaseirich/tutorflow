"""
Views für Location-CRUD-Operationen.
"""
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.locations.models import Location
from apps.locations.forms import LocationForm


class LocationListView(ListView):
    """Liste aller Orte."""
    model = Location
    template_name = 'locations/location_list.html'
    context_object_name = 'locations'
    paginate_by = 30


class LocationDetailView(DetailView):
    """Detailansicht eines Ortes."""
    model = Location
    template_name = 'locations/location_detail.html'
    context_object_name = 'location'


class LocationCreateView(CreateView):
    """Neuen Ort erstellen."""
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'
    success_url = reverse_lazy('locations:list')

    def form_valid(self, form):
        messages.success(self.request, 'Ort erfolgreich erstellt.')
        return super().form_valid(form)


class LocationUpdateView(UpdateView):
    """Ort bearbeiten."""
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'
    success_url = reverse_lazy('locations:list')

    def form_valid(self, form):
        messages.success(self.request, 'Ort erfolgreich aktualisiert.')
        return super().form_valid(form)


class LocationDeleteView(DeleteView):
    """Ort löschen."""
    model = Location
    template_name = 'locations/location_confirm_delete.html'
    success_url = reverse_lazy('locations:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Ort erfolgreich gelöscht.')
        return super().delete(request, *args, **kwargs)
