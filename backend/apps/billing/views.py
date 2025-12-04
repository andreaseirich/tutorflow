"""
Views für Billing-App.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from datetime import date
from apps.billing.models import Invoice, InvoiceItem
from apps.billing.forms import InvoiceCreateForm, InvoiceForm
from apps.billing.services import InvoiceService
from apps.billing.document_service import InvoiceDocumentService


class InvoiceListView(ListView):
    """Liste aller Rechnungen."""
    model = Invoice
    template_name = 'billing/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 20


class InvoiceDetailView(DetailView):
    """Detailansicht einer Rechnung."""
    model = Invoice
    template_name = 'billing/invoice_detail.html'
    context_object_name = 'invoice'


class InvoiceCreateView(CreateView):
    """Erstellung einer neuen Rechnung aus Lessons."""
    form_class = InvoiceCreateForm
    template_name = 'billing/invoice_create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Lade Lessons für Vorschau, falls Zeitraum vorhanden
        period_start = self.request.GET.get('period_start')
        period_end = self.request.GET.get('period_end')
        contract_id = self.request.GET.get('contract')
        
        if period_start and period_end:
            try:
                period_start = date.fromisoformat(period_start)
                period_end = date.fromisoformat(period_end)
                contract = None
                if contract_id:
                    from apps.contracts.models import Contract
                    contract = Contract.objects.get(pk=contract_id)
                
                billable_lessons = InvoiceService.get_billable_lessons(
                    period_start, period_end, contract
                )
                context['billable_lessons'] = billable_lessons
                context['period_start'] = period_start
                context['period_end'] = period_end
                context['contract'] = contract
            except (ValueError, Exception):
                pass
        
        return context
    
    def form_valid(self, form):
        period_start = form.cleaned_data['period_start']
        period_end = form.cleaned_data['period_end']
        contract = form.cleaned_data.get('contract')
        lesson_ids_str = form.cleaned_data.get('lesson_ids', '')
        
        if not lesson_ids_str:
            messages.error(self.request, 'Bitte wählen Sie mindestens eine Unterrichtsstunde aus.')
            return self.form_invalid(form)
        
        lesson_ids = [int(id.strip()) for id in lesson_ids_str.split(',') if id.strip()]
        
        try:
            invoice = InvoiceService.create_invoice_from_lessons(
                lesson_ids, period_start, period_end, contract
            )
            messages.success(self.request, f'Rechnung {invoice.id} erfolgreich erstellt.')
            return redirect('billing:invoice_detail', pk=invoice.pk)
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


def generate_invoice_document(request, pk):
    """Generiert das Rechnungsdokument für eine Invoice."""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    try:
        InvoiceDocumentService.save_document(invoice)
        messages.success(request, 'Rechnungsdokument erfolgreich generiert.')
    except Exception as e:
        messages.error(request, f'Fehler beim Generieren des Dokuments: {str(e)}')
    
    return redirect('billing:invoice_detail', pk=pk)
