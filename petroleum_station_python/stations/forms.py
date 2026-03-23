from django import forms
from .models import Station

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['station_name', 'location']
        widgets = {
            'station_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'location': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }
