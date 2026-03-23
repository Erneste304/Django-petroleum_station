from django import forms
from .models import FuelType, FuelDelivery, Tank

class FuelDeliveryForm(forms.ModelForm):
    class Meta:
        model = FuelDelivery
        fields = ['supplier', 'tank', 'quantity']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'tank': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'step': '0.01',
                'placeholder': 'Liters delivered'
            }),
        }

class FuelPriceForm(forms.ModelForm):
    class Meta:
        model = FuelType
        fields = ['price_per_liter']
        widgets = {
            'price_per_liter': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'step': '0.01',
                'placeholder': 'New price per liter (RWF)'
            }),
        }

class TankForm(forms.ModelForm):
    class Meta:
        model = Tank
        fields = ['fuel', 'capacity', 'current_stock']
        widgets = {
            'fuel': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'current_stock': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }
