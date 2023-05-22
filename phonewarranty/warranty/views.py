from django.shortcuts import render, get_object_or_404, redirect, Http404
from .models import Warranty, Phone
from .forms import PhoneForm, WarrantyForm, RegisterForm
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q, Count, F, Case, When, BooleanField, Sum, IntegerField
from datetime import date
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from dal import autocomplete
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout

def phone_list(request):
    phones = Phone.objects.all()
    sort_param = request.GET.get('sort', '')
    brands = request.GET.getlist('brands')
    nccs = request.GET.getlist('nccs')

    if brands:
        phones = phones.filter(name_brand__in=brands)

    if nccs:
        phones = phones.filter(NCC__in=nccs)

    sorting_options = {
        'name_asc': 'name',
        'name_desc': '-name',
        'start_date_asc': 'start_date',
        'start_date_desc': '-start_date',
        'end_date_asc': 'end_date',
        'end_date_desc': '-end_date',
    }

    if sort_param in sorting_options:
        phones = phones.order_by(sorting_options[sort_param])

    if sort_param == 'warranty':
        phones = phones.filter(end_date__gte=date.today())
    elif sort_param == 'no_warranty':
        phones = phones.filter(end_date__lt=date.today())

    paginator = Paginator(phones, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    unique_brands = Phone.objects.values_list('name_brand', flat=True).distinct()
    unique_nccs = Phone.objects.values_list('NCC', flat=True).distinct()

    context = {
        'phones': page_obj,
        'sort_param': sort_param,
        'brands': unique_brands,
        'nccs': unique_nccs,
    }

    return render(request, 'warranty/phone_list.html', context)


def warranty_list(request):
    warranties = Warranty.objects.select_related('phone').annotate(name_brand=F('phone__name_brand'))
    sort_param = request.GET.get('sort', '')
    brands = request.GET.getlist('brands')
    nccs = request.GET.getlist('nccs')
    
    if len(brands) > 0:
        warranties = warranties.filter(name_brand__in=brands)

    if len(nccs) > 0:
        warranties = warranties.filter(phone__NCC__in=nccs)

    sort_options = {
        'name_asc': 'phone__name',
        'name_desc': '-phone__name',
        'name_KH_asc': 'name_KH',
        'name_KH_desc': '-name_KH',
        'ngaynhan_asc': 'ngaynhan',
        'ngaynhan_desc': '-ngaynhan',
        'ngaytra_asc': 'ngaytra',
        'ngaytra_desc': '-ngaytra',
    }

    if sort_param in sort_options:
        sort_field = sort_options[sort_param]
        warranties = warranties.order_by(sort_field)

    paginator = Paginator(warranties, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    unique_brands = Phone.objects.values_list('name_brand', flat=True).distinct()
    unique_nccs = Phone.objects.values_list('NCC', flat=True).distinct()

    return render(request, 'warranty/warranty_list.html', {'warranties': page_obj, 'sort_param': sort_param, 'brands': unique_brands, 'nccs': unique_nccs})


def add_phone(request):
    nccs = Phone.objects.values('NCC').distinct()
    
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('phone_list')
    else:
        form = PhoneForm()

    context = {'form': form, 'nccs': nccs}
    return render(request, 'warranty/add_phone.html', context)


def update_phone(request, phone_id):
    nccs = Phone.objects.values('NCC').distinct()
    
    try:
        phone_id = int(phone_id)
    except ValueError:
        raise Http404('Invalid phone ID')
        
    phone = get_object_or_404(Phone, id=phone_id)
    
    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=phone)
        if form.is_valid():
            form.save()
            return redirect('phone_list')
    else:
        form = PhoneForm(instance=phone)
    
    context = {'form': form, 'nccs': nccs, 'phone_id': phone_id}
    return render(request, 'warranty/update_phone.html', context)




def delete_phone(request, phone_id):
    phone = Phone.objects.get(id=phone_id)
    phone.delete()
    return redirect('phone_list')


def search_phone(request):
    query = request.GET.get('q')
    phones = Phone.objects.filter(Q(serial__icontains=query))
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
    names = Phone.objects.values('name').annotate(name_count=Count('name')).order_by('-name_count')

    nccs = Phone.objects.values('NCC', 'name_brand').annotate(
        name_count=Count('name'),
        under_warranty=Sum(
            Case(
                When(end_date__gte=date.today(), then=1),
                default=0,
                output_field=IntegerField()
            )
        ),
        expired_warranty=Sum(
            Case(
                When(end_date__lt=date.today(), then=1),
                default=0,
                output_field=IntegerField()
            )
        )
    ).order_by('-name_count')

    nccs = Phone.objects.values('NCC').annotate(name_count=Count('name')).order_by('-name_count')
    brands = Phone.objects.values('name_brand').distinct()

    return render(request, 'warranty/TK.html', {'nccs': nccs, 'names': names, 'brands': brands})


def get_data(queryset):
    data = {
        'labels': [obj['name'] for obj in queryset],
        'data': [obj['name_count'] for obj in queryset]
    }
    return data

def ajax_get_all_names(request):
    names = Phone.objects.values('name').annotate(name_count=Count('name')).order_by('-name_count')

    labels = [name['name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)


def ajax_get_names_by_brand(request):
    brand = request.GET.get('brand')
    if brand == 'all':
        names = Phone.objects.values('name').annotate(name_count=Count('name')).order_by('-name_count')
    else:
        names = Phone.objects.filter(name_brand=brand).values('name').annotate(name_count=Count('name')).order_by('-name_count')

    labels = [name['name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)

def ajax_get_names_by_ncc(request):
    ncc = request.GET.get('ncc')
    if ncc == 'all':
        names = Phone.objects.values('name').annotate(name_count=Count('name')).order_by('-name_count')
    else:
        names = Phone.objects.filter(NCC=ncc).values('name').annotate(name_count=Count('name')).order_by('-name_count')

    labels = [name['name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)

def ajax_get_names_by_brand_and_ncc(request):
    brand = request.GET.get('brand')
    ncc = request.GET.get('ncc')
    if brand == 'all' and ncc == 'all':
        names = Phone.objects.values('name').annotate(name_count=Count('name')).order_by('-name_count')
    elif brand == 'all':
        names = Phone.objects.filter(NCC=ncc).values('name').annotate(name_count=Count('name')).order_by('-name_count')
    elif ncc == 'all':
        names = Phone.objects.filter(name_brand=brand).values('name').annotate(name_count=Count('name')).order_by('-name_count')
    else:
        names = Phone.objects.filter(name_brand=brand, NCC=ncc).values('name').annotate(name_count=Count('name')).order_by('-name_count')

    labels = [name['name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)

def ajax_get_names_by_warranty_status(request):
    status = request.GET.get('status')

    names = Phone.objects.filter(status=status).values('name').annotate(name_count=Count('name')).order_by('-name_count')

    labels = [name['name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)


def ajax_get_names_by_brand_and_warranty_status(request):
    brand = request.GET.get('brand')
    status = request.GET.get('status')
    
    phones = Phone.objects.all()
    
    if brand != 'all':
        phones = phones.filter(name_brand=brand)
        
    if status == 'under_warranty':
        phones = phones.filter(end_date__gte=date.today())
    elif status == 'expired_warranty':
        phones = phones.filter(end_date__lt=date.today())
    
    names = phones.values('name').annotate(name_count=Count('name')).order_by('-name_count')
    
    labels = [name['name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)



def ajax_get_names_by_ncc_and_warranty_status(request):
    ncc = request.GET.get('ncc')
    status = request.GET.get('status')
    
    phones = Phone.objects.all()
    
    if ncc != 'all':
        phones = phones.filter(NCC=ncc)
        
    if status == 'under_warranty':
        phones = phones.filter(end_date__gte=date.today())
    elif status == 'expired_warranty':
        phones = phones.filter(end_date__lt=date.today())
    
    names = phones.values('name').annotate(name_count=Count('name')).order_by('-name_count')
    
    labels = [name['name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)




def ajax_get_names_by_brand_ncc_and_warranty_status(request):
    brand = request.GET.get('brand')
    ncc = request.GET.get('ncc')
    status = request.GET.get('status')
    
    phones = Phone.objects.filter(name_brand=brand, NCC=ncc)
    
    if status == 'under_warranty':
        phones = phones.filter(end_date__gte=date.today())
    elif status == 'expired_warranty':
        phones = phones.filter(end_date__lt=date.today())
    
    names = phones.values('name').annotate(name_count=Count('name')).order_by('-name_count')
    
    labels = [name['name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)


def TK_baohanh(request):
    nccs = Warranty.objects.values('phone__NCC').annotate(name_count=Count('phone__name')).order_by('-name_count')
    names = Warranty.objects.values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')
    brands = Warranty.objects.values('phone__name_brand').distinct()
    
    return render(request, 'warranty/TK_baohanh.html', {'nccs': nccs, 'names': names, 'brands': brands})


def get_data_baohanh(queryset):
    data = {
        'labels': [obj['phone__name'] for obj in queryset],
        'data': [obj['name_count'] for obj in queryset]
    }
    return data

def ajax_get_all_names_baohanh(request):
    names = Warranty.objects.values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')

    labels = [name['phone__name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)


def ajax_get_names_by_brand_baohanh(request):
    brand = request.GET.get('brand')
    if brand == 'all':
        names = Warranty.objects.values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')
    else:
        names = Warranty.objects.filter(phone__name_brand=brand).values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')

    labels = [name['phone__name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)

def ajax_get_names_by_ncc_baohanh(request):
    ncc = request.GET.get('ncc')
    if ncc == 'all':
        names = Warranty.objects.values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')
    else:
        names = Warranty.objects.filter(phone__NCC=ncc).values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')

    labels = [name['phone__name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)

def ajax_get_names_by_brand_and_ncc_baohanh(request):
    brand = request.GET.get('brand')
    ncc = request.GET.get('ncc')
    if brand == 'all' and ncc == 'all':
        names = Warranty.objects.values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')
    elif brand == 'all':
        names = Warranty.objects.filter(phone__NCC=ncc).values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')
    elif ncc == 'all':
        names = Warranty.objects.filter(phone__name_brand=brand).values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')
    else:
        names = Warranty.objects.filter(phone__name_brand=brand, phone__NCC=ncc).values('phone__name').annotate(name_count=Count('phone__name')).order_by('-name_count')

    labels = [name['phone__name'] for name in names]
    data = [name['name_count'] for name in names]
    response = {'labels': labels, 'data': data}
    return JsonResponse(response)




class PhoneAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Phone.objects.all()
        if self.q:
            qs = qs.filter(Q(serial__icontains=self.q))
        return qs

    def get_result_label(self, item):
        return item.serial

    def get_selected_result_label(self, item):
        return item.serial
    
    def get_paginated_response(self, results, has_more):
        return JsonResponse({
        'results': results,
        'pagination': {
            'more': has_more,
        }
    })

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            qs = self.get_queryset()
            paginator = self.paginator_class(list(qs), self.paginate_by)
            page = paginator.get_page(self.request.GET.get('page'))
            results = []
            if page is not None:
                for obj in page.object_list:
                    results.append({'id': obj.pk, 'text': self.get_result_label(obj)})
                has_more = page.has_next()
            else:
                for obj in qs:
                    results.append({'id': obj.pk, 'text': self.get_result_label(obj)})
                has_more = False
            return self.get_paginated_response(results, has_more)

        return super().get(request, *args, **kwargs)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created!')
            print('Đăng ký thành công !')
            return redirect('phone_list')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = RegisterForm()
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


