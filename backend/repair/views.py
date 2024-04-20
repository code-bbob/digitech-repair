from django.shortcuts import render, HttpResponse, redirect 
from .models import Repair
from .forms import RepairForm, SubmitForm
from django.http import HttpResponse
from django.core.paginator import Paginator


def RepairHome(request):

    form = SubmitForm()
    if request.method == 'GET':
        repairs = Repair.objects.exclude(repair_status="Completed").order_by('-id')
        completed_repairs = Repair.objects.filter(repair_status="Completed").order_by('-id')
        print(completed_repairs)
        incomplete_repairs = Repair.objects.exclude(repair_status="Completed").order_by('-id')
        completed_paginator = Paginator(completed_repairs, 1)
        incomplete_paginator = Paginator(incomplete_repairs,1)
        page_number = request.GET.get("page")
        completed_page_obj = completed_paginator.get_page(page_number)
        incomplete_page_obj = incomplete_paginator.get_page(page_number)
        print(completed_page_obj)
        context = {'completed_page_obj': completed_page_obj,'incomplete_page_obj':incomplete_page_obj,'form': form}
        return render(request,'repair/arko.html', context)

    else:
        pass

def Search(request):
    query = request.GET['query']
    if len(query)>40:
        repairs=Repair.objects.none()
    else:
        repair_customer_name= Repair.objects.filter(customer_name__icontains=query)
        repair_phone_model= Repair.objects.filter(phone_model__icontains=query)
        repair_id =Repair.objects.filter(repair_id__exact=query)
        repair_customer_phone_number = Repair.objects.filter(customer_phone_number__icontains=query)
        repairs=  repair_customer_name.union(repair_customer_phone_number,repair_phone_model,repair_id)

        # if repairs.count()==0:
        #     return HttpResponse( "No search results found. Please refine your query.")

        params = {'repairs':repairs, 'query':query}
        return render(request, 'repair/search.html', params)
    
def Form(request):
    repairs = Repair.objects.all()
    form = RepairForm()

    if request.method  == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            repair =form.save()
            return redirect(f'/repair/product/{repair.repair_id}')
    context = {'form':form}
    return render(request,'repair/form.html', context)

def CompleteForm(request,repair_id):
    repair = Repair.objects.get(repair_id=repair_id)
    form = SubmitForm(instance=repair)

    if request.method == 'POST':
        form = SubmitForm(request.POST, instance=repair)
        if form.is_valid():
            repair.repair_status = 'Completed'
            repair = form.save()
            return redirect('/repair/')
        else:
             return HttpResponse('Form is not valid')

    context = {'form':form}
    return render(request,'repair/form.html', context)

def UpdateForm(request, repair_id):
    repair = Repair.objects.get(repair_id=repair_id)
    form = RepairForm(instance=repair)

    if request.method == 'POST':
        form = RepairForm(request.POST, instance=repair)
        if form.is_valid():
            repair = form.save()
            return redirect('/repair/')
        else:
             return HttpResponse('Form is not valid')

    context = {'form':form}
    return render(request,'repair/form.html', context)



def Product(request,repair_id):
    repair = Repair.objects.get(repair_id = repair_id)
    return render(request,'repair/product.html', {'repair':repair})

def Print(request,repair_id):
    repair = Repair.objects.get(repair_id = repair_id)
    return render(request,'repair/print.html', {'repair':repair})

    
