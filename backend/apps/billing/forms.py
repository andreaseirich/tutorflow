"""
Forms für Billing-App.
"""
from django import forms
from datetime import date
from apps.billing.models import Invoice
from apps.contracts.models import Contract


class InvoiceCreateForm(forms.Form):
    """Form für die Erstellung einer Rechnung mit Lesson-Auswahl."""
    
    period_start = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text="Beginn des Abrechnungszeitraums"
    )
    period_end = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text="Ende des Abrechnungszeitraums"
    )
    contract = forms.ModelChoiceField(
        queryset=Contract.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Optional: Nach Vertrag filtern"
    )
    lesson_ids = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        help_text="IDs der ausgewählten Lessons (kommagetrennt)"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        period_start = cleaned_data.get('period_start')
        period_end = cleaned_data.get('period_end')
        
        if period_start and period_end and period_start > period_end:
            raise forms.ValidationError("Das Enddatum darf nicht vor dem Startdatum liegen.")
        
        return cleaned_data


class InvoiceForm(forms.ModelForm):
    """Form für Invoice-Bearbeitung."""
    
    class Meta:
        model = Invoice
        fields = ['payer_name', 'payer_address', 'status']
        widgets = {
            'payer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'payer_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

