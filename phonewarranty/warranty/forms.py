from django import forms
from .models import Phone, Warranty

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ('serial', 'name', 'start_date', 'end_date', 'NCC', 'description')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
    }
        
        labels = {
            'serial': 'Serial',
            'name': 'Tên thiết bị',
            'start_date': 'Ngày bắt đầu bảo hành',
            'end_date': 'Ngày kết thúc bảo hành',
            'NCC': 'Nhà cung cấp',
            'description': 'Mô tả'
        }
    
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False, label="Mô tả")

    

class WarrantyForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = ('MKH', 'name', 'start_date', 'end_date', 'NCC', 'description',)
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
    }
        
        labels = {
            'MKH': 'Mã khách hàng',
            'name': 'Tên thiết bị',
            'start_date': 'Ngày nhận bảo hành',
            'end_date': 'Ngày trả bảo hành',
            'NCC': 'Nhà cung cấp',
            'description': 'Mô tả',
            
        }
    
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False, label="Mô tả")
        

        
        





