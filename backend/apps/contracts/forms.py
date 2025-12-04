"""
Forms für Contract-Model.
"""
from django import forms
from apps.contracts.models import Contract
from apps.students.models import Student


class ContractForm(forms.ModelForm):
    """Form für Contract-Erstellung und -Bearbeitung."""
    
    class Meta:
        model = Contract
        fields = [
            'student', 'institute', 'hourly_rate', 'unit_duration_minutes',
            'start_date', 'end_date', 'is_active', 'notes'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'institute': forms.TextInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit_duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

