from django import forms
from .models import LoyaltyReward

class LoyaltyRewardForm(forms.ModelForm):
    class Meta:
        model = LoyaltyReward
        fields = ['name', 'description', 'points_cost']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'e.g. Free Car Wash'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'rows': 3,
                'placeholder': 'Describe what the customer receives'
            }),
            'points_cost': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Points required to redeem'
            }),
        }
