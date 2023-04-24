from django.shortcuts import render, get_object_or_404
from .models import Phone, Warranty, Customer
from django.shortcuts import render, redirect
from .forms import PhoneForm, WarrantyForm
from django.contrib import messages
from django.urls import reverse




def phone_list(request):
    phones = Phone.objects.all()
    return render(request, 'warranty/phone_list.html', {'phones': phones})


def warranty_detail(request, pk):
    if request.method == 'POST':
        form = WarrantyForm(request.POST)
        if form.is_valid():
            warranty = form.save()
            phone = Phone.objects.create(serial=warranty.serial, name=warranty.name, start_date=warranty.start_date, end_date=warranty.end_date)
            # Trở về trang phone_list
            return redirect('phone_list')
    else:
        form = WarrantyForm()
    return render(request, 'warranty/warranty_detail.html', {'form': form})



def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'warranty/warranty_list.html', {'customers': customers})

def add_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.save()
            return redirect('phone_list')
    else:
        form = PhoneForm()
    return render(request, 'warranty/add_phone.html', {'form': form})

def add_warranty(request, phone_id):
    phone = Phone.objects.get(id=phone_id)
    if request.method == 'POST':
        form = WarrantyForm(request.POST)
        if form.is_valid():
            warranty = form.save(commit=False)
            warranty.phone = phone
            warranty.save()
            messages.success(request, 'Warranty added successfully')
            return redirect(reverse('warranty_detail', args=[phone.id]))
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = WarrantyForm()
    return render(request, 'warranty/add_warranty.html', {'form': form})
