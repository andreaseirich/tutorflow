"""
Formsets für ContractMonthlyPlan.
"""
from django import forms
from django.forms import inlineformset_factory
from apps.contracts.models import Contract, ContractMonthlyPlan
from datetime import date
from calendar import monthrange


class ContractMonthlyPlanForm(forms.ModelForm):
    """Form für einen einzelnen ContractMonthlyPlan-Eintrag."""
    
    class Meta:
        model = ContractMonthlyPlan
        fields = ['year', 'month', 'planned_units']
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'month': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'planned_units': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


ContractMonthlyPlanFormSet = inlineformset_factory(
    Contract,
    ContractMonthlyPlan,
    form=ContractMonthlyPlanForm,
    extra=0,
    can_delete=False,
    fields=['year', 'month', 'planned_units']
)


def generate_monthly_plans_for_contract(contract: Contract) -> list:
    """
    Generiert ContractMonthlyPlan-Einträge für alle Monate im Vertragszeitraum.
    
    Args:
        contract: Der Contract, für den die Pläne erstellt werden sollen
    
    Returns:
        Liste der erstellten ContractMonthlyPlan-Objekte
    """
    if not contract.start_date:
        return []
    
    # Bestimme Enddatum (end_date oder aktuelles Datum + 1 Jahr)
    end_date = contract.end_date
    if not end_date:
        today = date.today()
        end_date = date(today.year + 1, today.month, today.day)
    
    plans = []
    current_year = contract.start_date.year
    current_month = contract.start_date.month
    end_year = end_date.year
    end_month = end_date.month
    
    while (current_year, current_month) <= (end_year, end_month):
        # Prüfe, ob bereits ein Plan für diesen Monat existiert
        plan, created = ContractMonthlyPlan.objects.get_or_create(
            contract=contract,
            year=current_year,
            month=current_month,
            defaults={'planned_units': 0}
        )
        plans.append(plan)
        
        # Nächster Monat
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
    
    return plans

