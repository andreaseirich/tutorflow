"""
Views für Contract-CRUD-Operationen.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.contracts.models import Contract, ContractMonthlyPlan
from apps.contracts.forms import ContractForm
from apps.contracts.formsets import ContractMonthlyPlanFormSet, generate_monthly_plans_for_contract


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ContractMonthlyPlanFormSet(self.request.POST)
        else:
            # Initial: Formset ist leer, wird nach Speichern des Contracts gefüllt
            context['formset'] = ContractMonthlyPlanFormSet()
        return context

    def form_valid(self, form):
        # Speichere Contract zuerst
        self.object = form.save()
        
        # Generiere monatliche Pläne für den Vertragszeitraum
        if self.object.start_date:
            generate_monthly_plans_for_contract(self.object)
            # Weiterleitung zur Update-View, um monatliche Planung zu bearbeiten
            messages.success(self.request, 'Vertrag erstellt. Bitte geben Sie die geplanten Einheiten pro Monat ein.')
            return redirect('contracts:update', pk=self.object.pk)
        else:
            messages.success(self.request, 'Vertrag erfolgreich erstellt.')
            return redirect(self.success_url)


class ContractUpdateView(UpdateView):
    """Vertrag bearbeiten."""
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_form.html'
    success_url = reverse_lazy('contracts:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ContractMonthlyPlanFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            # Lade vorhandene Pläne oder generiere neue
            if self.object.start_date:
                # Stelle sicher, dass alle Monate im Zeitraum abgedeckt sind
                generate_monthly_plans_for_contract(self.object)
                # Lösche Pläne außerhalb des Zeitraums
                if self.object.end_date:
                    ContractMonthlyPlan.objects.filter(
                        contract=self.object
                    ).exclude(
                        year__gte=self.object.start_date.year,
                        month__gte=self.object.start_date.month
                    ).filter(
                        year__lte=self.object.end_date.year,
                        month__lte=self.object.end_date.month
                    ).delete()
                else:
                    # Bei unbefristeten Verträgen: Lösche nur sehr alte Pläne (älter als 2 Jahre)
                    from datetime import date
                    today = date.today()
                    ContractMonthlyPlan.objects.filter(
                        contract=self.object
                    ).filter(
                        year__lt=today.year - 2
                    ).delete()
            
            context['formset'] = ContractMonthlyPlanFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        # Speichere Contract
        self.object = form.save()
        
        # Wenn Zeitraum geändert wurde, generiere neue Pläne
        generate_monthly_plans_for_contract(self.object)
        
        # Formset aktualisieren
        formset.instance = self.object
        
        if formset.is_valid():
            formset.save()
            messages.success(self.request, 'Vertrag erfolgreich aktualisiert.')
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Bitte korrigieren Sie die Fehler in der monatlichen Planung.')
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ContractDeleteView(DeleteView):
    """Vertrag löschen."""
    model = Contract
    template_name = 'contracts/contract_confirm_delete.html'
    success_url = reverse_lazy('contracts:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Vertrag erfolgreich gelöscht.')
        return super().delete(request, *args, **kwargs)
