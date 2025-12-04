"""
Views für Contract-CRUD-Operationen.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.contracts.models import Contract
from apps.contracts.forms import ContractForm


class ContractListView(ListView):
    """Liste aller Verträge."""
    model = Contract
    template_name = 'contracts/contract_list.html'
    context_object_name = 'contracts'
    paginate_by = 20


class ContractDetailView(DetailView):
    """Detailansicht eines Vertrags."""
    model = Contract
    template_name = 'contracts/contract_detail.html'
    context_object_name = 'contract'


class ContractCreateView(CreateView):
    """Neuen Vertrag erstellen."""
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_form.html'
    success_url = reverse_lazy('contracts:list')

    def form_valid(self, form):
        messages.success(self.request, 'Vertrag erfolgreich erstellt.')
        return super().form_valid(form)


class ContractUpdateView(UpdateView):
    """Vertrag bearbeiten."""
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_form.html'
    success_url = reverse_lazy('contracts:list')

    def form_valid(self, form):
        messages.success(self.request, 'Vertrag erfolgreich aktualisiert.')
        return super().form_valid(form)


class ContractDeleteView(DeleteView):
    """Vertrag löschen."""
    model = Contract
    template_name = 'contracts/contract_confirm_delete.html'
    success_url = reverse_lazy('contracts:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Vertrag erfolgreich gelöscht.')
        return super().delete(request, *args, **kwargs)
