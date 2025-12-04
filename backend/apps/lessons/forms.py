"""
Forms für Lesson-Model.
"""
from django import forms
from apps.lessons.models import Lesson
from apps.contracts.models import Contract
from apps.locations.models import Location


class LessonForm(forms.ModelForm):
    """Form für Lesson-Erstellung und -Bearbeitung."""
    
    class Meta:
        model = Lesson
        fields = [
            'contract', 'date', 'start_time', 'duration_minutes',
            'location', 'travel_time_before_minutes', 'travel_time_after_minutes', 'notes'
        ]
        widgets = {
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'travel_time_before_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'travel_time_after_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

