from django import forms
from .models import Sale
from inventory.models import Pump
from users.models import Customer
from stations.models import Employee

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'employee', 'pump', 'quantity', 'total_amount']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'employee': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'pump': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'step': '0.01',
                'placeholder': 'Liters sold'
            }),
            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'step': '0.01',
                'placeholder': 'Total amount in RWF'
            }),
        }
