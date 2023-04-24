from django.shortcuts import render, get_object_or_404
from .models import Warranty, Phone
from django.shortcuts import render, redirect
from .forms import PhoneForm, WarrantyForm
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q, Count
from datetime import date, datetime


def phone_list(request): 
    phones = Phone.objects.all()
    return render(request, 'warranty/phone_list.html', {'phones': phones})


def warranty_list(request):
    warranties = Warranty.objects.all()
    return render(request, 'warranty/warranty_list.html', {'warranties': warranties})


def add_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('phone_list')
    else:
        form = PhoneForm()
    return render(request, 'warranty/add_phone.html', {'form': form})


def update_phone(request, phone_id):
    phone = Phone.objects.get(id=phone_id)
    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=phone)
        if form.is_valid():
            form.save()
            return redirect('phone_list')
    else:
        form = PhoneForm(instance=phone)
    return render(request, 'warranty/update_phone.html', {'form': form})


def delete_phone(request, phone_id):
    phone = Phone.objects.get(id=phone_id)
    phone.delete()
    return redirect('phone_list')


def search_phone(request):
    query = request.GET.get('q')
    phones = Phone.objects.filter(Q(serial__icontains=query) | Q(name__icontains=query))
    return render(request, 'warranty/kq_search_phone.html', {'phones': phones})

def search_warranty(request):
    query = request.GET.get('q')
    warranties = Warranty.objects.filter(Q(MKH__icontains=query) | Q(name__icontains=query) | Q(NCC__icontains=query))
    return render(request, 'warranty/kq_search_warranty.html', {'warranties': warranties})

def add_warranty(request):
    if request.method == 'POST':
        form = WarrantyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('warranty_list')
    else:
        form = WarrantyForm()
    return render(request, 'warranty/add_warranty.html', {'form': form})


def update_warranty(request, warranty_id):
    warranty = Warranty.objects.get(id=warranty_id)
    if request.method == 'POST':
        form = WarrantyForm(request.POST, instance=warranty)
        if form.is_valid():
            form.save()
            return redirect('warranty_list')
    else:
        form = WarrantyForm(instance=warranty)
    return render(request, 'warranty/update_warranty.html', {'form': form})


def delete_warranty(request, warranty_id):
    warranty = Warranty.objects.get(id=warranty_id)
    warranty.delete()
    return redirect('warranty_list')


def expired_warranty(request):
    phones = Phone.objects.filter(end_date__lt=date.today())
    return render(request, 'warranty/expired_warranty.html', {'phones': phones})


def high_warranty(request):
    warranties = Warranty.objects.values('name').annotate(name_count=Count('name')).order_by('-name_count')
    return render(request, 'warranty/high_warranty.html', {'warranties': warranties})
