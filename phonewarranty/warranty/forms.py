from django import forms
from .models import Phone, Warranty

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ('serial', 'name', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class WarrantyForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = ('serial', 'name', 'start_date', 'end_date', 'NCC', 'description')
