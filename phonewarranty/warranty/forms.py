from django import forms
from .models import Phone, Warranty
from dal import autocomplete
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        
        widgets = {
            'password1' : forms.PasswordInput(attrs={'placeholder':'Mật khẩu'}),
            'username' : forms.TextInput(attrs={'placeholder':'Tên đăng nhập'}),
            'password2': forms.PasswordInput(attrs={'placeholder':'Xác nhận mật khẩu'}),
        }


class PhoneForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={
        'rows': 4}),
        required=False,
        empty_value='',
        label="Mô tả"
    )
    
    class Meta:
        model = Phone
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }


class WarrantyForm(forms.ModelForm):
    phone = forms.ModelChoiceField(
        queryset=Phone.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='phone-autocomplete',
            attrs={
                'data-placeholder': 'Type to autocomplete...',
                'data-minimum-input-length': 2,
                'id': 'id_phone'
            },
        )
    )

    name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    NCC = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    name_brand = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    note = forms.CharField(
        widget=forms.Textarea(attrs={
        'rows': 4}),
        required=False,
        empty_value='',
        label="Ghi chú"
    )

    class Meta:
        model = Warranty
        fields = ('phone', 'MGD', 'name_KH', 'phone_number', 'ngaynhan', 'ngaytra', 'note')

        widgets = {
            'ngaynhan': forms.DateInput(attrs={'type': 'date'}),
            'ngaytra': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            self.fields['name'].initial = self.instance.phone.name
            self.fields['NCC'].initial = self.instance.phone.NCC
            self.fields['name_brand'].initial = self.instance.phone.name_brand
            self.fields['phone'].disabled = True
            
