"""
Forms für Location-Model.
"""
from django import forms
from apps.locations.models import Location


class LocationForm(forms.ModelForm):
    """Form für Location-Erstellung und -Bearbeitung."""
    
    class Meta:
        model = Location
        fields = ['name', 'address', 'latitude', 'longitude']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
        }

