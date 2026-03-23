from django import forms
from .models import StaffReport

class StaffReportForm(forms.ModelForm):
    class Meta:
        model = StaffReport
        fields = ['title', 'report_type', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Brief title of the report'
            }),
            'report_type': forms.Select(attrs={
                'class': 'form-select bg-dark text-white border-secondary'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'rows': 5,
                'placeholder': 'Describe the situation in detail...'
            }),
        }

class ApprovalNoteForm(forms.Form):
    """Simple form for accountant/admin approval notes."""
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control bg-dark text-white border-secondary',
            'rows': 3,
            'placeholder': 'Add a note (optional)...'
        }),
        label='Approval Note'
    )

class RejectionForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control bg-dark text-white border-secondary',
            'rows': 3,
            'placeholder': 'Explain why this report is being rejected...'
        }),
        label='Rejection Reason'
    )
