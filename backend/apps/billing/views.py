"""
Views für Billing-App.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView
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
    model = None  # Kein Model, da wir ein normales Form verwenden
    
    def get_form_kwargs(self):
        """Entfernt 'instance' aus kwargs, da InvoiceCreateForm kein ModelForm ist."""
        kwargs = super().get_form_kwargs()
        # Entferne 'instance', falls vorhanden (wird von CreateView hinzugefügt)
        kwargs.pop('instance', None)
        return kwargs
    
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
                    period_start, period_end, contract_id
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
        
        try:
            # Erstelle Rechnung automatisch mit allen verfügbaren Lessons im Zeitraum
            invoice = InvoiceService.create_invoice_from_lessons(
                period_start, period_end, contract
            )
            lesson_count = invoice.items.count()
            messages.success(
                self.request,
                f'Rechnung {invoice.id} erfolgreich erstellt mit {lesson_count} Unterrichtsstunde(n).'
            )
            return redirect('billing:invoice_detail', pk=invoice.pk)
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class InvoiceDeleteView(DeleteView):
    """Löschen einer Rechnung."""
    model = Invoice
    template_name = 'billing/invoice_confirm_delete.html'
    success_url = reverse_lazy('billing:invoice_list')
    
    def delete(self, request, *args, **kwargs):
        """Löscht die Rechnung und setzt Lessons zurück."""
        invoice = self.get_object()
        reset_count = InvoiceService.delete_invoice(invoice)
        
        if reset_count > 0:
            messages.success(
                request,
                f'Rechnung gelöscht. {reset_count} Unterrichtsstunde(n) wurden auf "unterrichtet" zurückgesetzt.'
            )
        else:
            messages.success(request, 'Rechnung erfolgreich gelöscht.')
        
        return redirect(self.success_url)


def generate_invoice_document(request, pk):
    """Generiert das Rechnungsdokument für eine Invoice."""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    try:
        InvoiceDocumentService.save_document(invoice)
        messages.success(request, 'Rechnungsdokument erfolgreich generiert.')
    except Exception as e:
        messages.error(request, f'Fehler beim Generieren des Dokuments: {str(e)}')
    
    return redirect('billing:invoice_detail', pk=pk)


def serve_invoice_document(request, pk):
    """Serviert das Rechnungsdokument für eine Invoice."""
    from django.http import FileResponse, Http404
    from django.conf import settings
    import os
    
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if not invoice.document:
        raise Http404("Rechnungsdokument nicht gefunden.")
    
    # Prüfe, ob Datei existiert
    file_path = invoice.document.path
    if not os.path.exists(file_path):
        raise Http404("Rechnungsdokument-Datei nicht gefunden.")
    
    # Serviere die Datei
    return FileResponse(
        open(file_path, 'rb'),
        content_type='text/html',
        filename=os.path.basename(file_path)
    )
