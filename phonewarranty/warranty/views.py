from django.shortcuts import render, get_object_or_404, redirect, Http404
from .models import Warranty, Phone
from django.shortcuts import render, redirect
from .forms import PhoneForm, WarrantyForm
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q, Count, F
from datetime import date, datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_GET
from dal import autocomplete
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse


def phone_list(request): 
    sort_param = request.GET.get('sort', '')
    if sort_param == 'name_asc':
        phones = Phone.objects.order_by('name')
    elif sort_param == 'name_desc':
        phones = Phone.objects.order_by('-name')
    elif sort_param == 'name_brand_asc':
        phones = Phone.objects.order_by('name_brand')
    elif sort_param == 'name_brand_desc':
        phones = Phone.objects.order_by('-name_brand')
    elif sort_param == 'NCC_asc':
        phones = Phone.objects.order_by('NCC')
    elif sort_param == 'NCC_desc':
        phones = Phone.objects.order_by('-NCC')
    elif sort_param == 'warranty':
        phones = Phone.objects.filter(end_date__gte=date.today())
    elif sort_param == 'no_warranty':
        phones = Phone.objects.filter(end_date__lt=date.today())
    else:
        phones = Phone.objects.all()
    return render(request, 'warranty/phone_list.html', {'phones': phones})

    
def warranty_list(request):
    warranties = Warranty.objects.select_related('phone').annotate(name_brand=F('phone__name_brand'))
    sort_param = request.GET.get('sort', '')
    brands = request.GET.getlist('brands')
    nccs = request.GET.getlist('nccs')
    if len(brands) > 0:
        warranties = Warranty.objects.filter(name_brand__in=brands)

    if len(nccs) > 0:
        warranties = warranties.filter(NCC__in=nccs)
        
    else:
        warranties = Warranty.objects.all()

    if sort_param == 'name_asc':
        warranties = warranties.order_by('name')
    elif sort_param == 'name_desc':
        warranties = warranties.order_by('-name')
    elif sort_param == 'name_KH_asc':
        warranties = warranties.order_by('name_KH')
    elif sort_param == 'name_KH_desc':
        warranties = warranties.order_by('-name_KH')
    elif sort_param == 'ncc_asc':
        warranties = warranties.order_by('phone__NCC')
    elif sort_param == 'ncc_desc':
        warranties = warranties.order_by('-phone__NCC')
        
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
    try:
        phone_id = int(phone_id)
    except ValueError:
        # If phone_id is not a valid integer, return a 404 error
        raise Http404('Invalid phone ID')
        
    phone = get_object_or_404(Phone, id=phone_id)
    
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
    warranties = Warranty.objects.filter(Q(name_KH__icontains=query) | Q(phone_number__icontains=query))
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


def TK(request):
    brands = Warranty.objects.values('phone__name_brand').annotate(name_brand_count=Count('phone__name_brand')).order_by('-name_brand_count')
    names = Warranty.objects.values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')
    return render(request, 'warranty/TK.html', {'brands': brands, 'names': names})


# Additional imports we'll need:
from django.contrib.auth import authenticate, login, logout


def get_data(queryset):
    data = {
        'labels': [obj['name'] for obj in queryset],
        'data': [obj['name_count'] for obj in queryset]
    }
    return data

@require_GET
def ajax_get_all_names(request):
    queryset = Warranty.objects.values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')
    return JsonResponse(get_data(queryset))

def ajax_get_names_by_brand(request):
    brand = request.GET.get('brand')
    queryset = Warranty.objects.filter(name_brand=brand).values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')
    return JsonResponse(get_data(queryset))

from dal import autocomplete

class PhoneAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Phone.objects.all()
        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(serial__icontains=self.q))
        return qs

    def get_result_label(self, item):
        return item.name

    def get_selected_result_label(self, item):
        return item.name

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            qs = self.get_queryset()
            page = self.paginate_queryset(qs)
            results = []
            if page is not None:
                for obj in page:
                    results.append({'id': obj.pk, 'text': self.get_result_label(obj)})
                return self.get_paginated_response(results)
            else:
                for obj in qs:
                    results.append({'id': obj.pk, 'text': self.get_result_label(obj)})
                return JsonResponse({'results': results})
        return super().get(request, *args, **kwargs)
    
    
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('login_view')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('phone_list')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('login_view')
