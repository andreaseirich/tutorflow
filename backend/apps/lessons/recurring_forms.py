"""
Forms für RecurringLesson-Model.
"""
from django import forms
from apps.lessons.recurring_models import RecurringLesson
from apps.contracts.models import Contract


class RecurringLessonForm(forms.ModelForm):
    """Form für RecurringLesson-Erstellung und -Bearbeitung."""
    
    class Meta:
        model = RecurringLesson
        fields = [
            'contract', 'start_date', 'end_date', 'start_time',
            'duration_minutes', 'travel_time_before_minutes', 'travel_time_after_minutes',
            'recurrence_type',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'is_active', 'notes'
        ]
        widgets = {
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'travel_time_before_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'travel_time_after_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'recurrence_type': forms.Select(attrs={'class': 'form-control'}),
            'monday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tuesday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wednesday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'thursday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'friday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'saturday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sunday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        # Prüfe, dass mindestens ein Wochentag ausgewählt ist
        weekdays = [
            cleaned_data.get('monday'),
            cleaned_data.get('tuesday'),
            cleaned_data.get('wednesday'),
            cleaned_data.get('thursday'),
            cleaned_data.get('friday'),
            cleaned_data.get('saturday'),
            cleaned_data.get('sunday'),
        ]
        if not any(weekdays):
            raise forms.ValidationError("Mindestens ein Wochentag muss ausgewählt werden.")
        return cleaned_data

