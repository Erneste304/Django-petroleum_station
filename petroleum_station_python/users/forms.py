from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, InternalMessage, GlobalShareConfig, PartnerShare

class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'role': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['password1', 'password2']:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control bg-dark text-white border-secondary'
            })


class UserEditForm(forms.ModelForm):
    """Form for editing existing users — no password fields."""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'role': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    """Form for users to edit their own profile info."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }

class InternalMessageForm(forms.ModelForm):
    class Meta:
        model = InternalMessage
        fields = ['recipient_role', 'subject', 'body']
        widgets = {
            'recipient_role': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'subject': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'body': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 4}),
        }
class ShareTransactionForm(forms.Form):
    TRANSACTION_TYPES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )
    transaction_type = forms.ChoiceField(choices=TRANSACTION_TYPES, widget=forms.HiddenInput())
    amount_shares = forms.DecimalField(max_digits=15, decimal_places=4, widget=forms.NumberInput(attrs={
        'class': 'form-control bg-dark text-white border-secondary',
        'placeholder': 'Enter amount of shares',
        'step': '0.0001'
    }))

class GlobalShareConfigForm(forms.ModelForm):
    class Meta:
        model = GlobalShareConfig
        fields = ['current_price', 'commission_percentage']
        widgets = {
            'current_price': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'step': '0.01'}),
            'commission_percentage': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'step': '0.000001'}),
        }

class PartnerShareForm(forms.ModelForm):
    class Meta:
        model = PartnerShare
        fields = ['total_shares', 'total_investment']
        widgets = {
            'total_shares': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'step': '0.0001'}),
            'total_investment': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'step': '0.01'}),
        }
