from django import forms
from .models import CarWashBooking, CarWashService

class CarWashBookingForm(forms.ModelForm):
    class Meta:
        model = CarWashBooking
        fields = ['customer', 'service', 'booking_date', 'status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'service': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'booking_date': forms.DateTimeInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
        }
