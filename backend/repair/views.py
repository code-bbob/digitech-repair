from django.shortcuts import render, HttpResponse, redirect 
from .models import Repair
from .forms import RepairForm, SubmitForm
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login


def RepairHome(request):

    form = SubmitForm()
    if request.method == 'GET':
        repairs = Repair.objects.exclude(repair_status="Completed").order_by('-id')
        completed_repairs = Repair.objects.filter(repair_status="Completed").order_by('-id')
        incomplete_repairs = Repair.objects.filter(repair_status="Not repaired").order_by('-id')
        print(incomplete_repairs)
        completed_paginator = Paginator(completed_repairs, 10)
        repaired_repairs = Repair.objects.filter(repair_status="Repaired").order_by('-id')
        repaired_paginator = Paginator(repaired_repairs,10)
        incomplete_paginator = Paginator(incomplete_repairs,10)
        page_number = request.GET.get("page")
        completed_page_obj = completed_paginator.get_page(page_number)
        incomplete_page_obj = incomplete_paginator.get_page(page_number)
        repaired_page_obj = repaired_paginator.get_page(page_number)
        context = {'completed_page_obj': completed_page_obj,'incomplete_page_obj':incomplete_page_obj,'repaired_page_obj':repaired_page_obj,'form': form}
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

def CompleteForm(request,repair_id,condition):
    repair = Repair.objects.get(repair_id=repair_id)
    form = SubmitForm(instance=repair)
    if request.method == 'POST':
        if condition == 'paid':
            form = SubmitForm(request.POST, instance=repair)
            if form.is_valid():
                repair.repair_status = 'Completed'
                repair = form.save()
                return redirect('/repair/')
            else:
                return HttpResponse('Form is not valid')
        elif condition == 'repaired':
            repair.repair_status = 'Unrepairable'
            print(repair.repair_status)
            print("########################")
            repair.save()
            return redirect('/repair/')
    else:
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

    
def Login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
            ...
        else:
            return HttpResponse("Invalid login")
    elif request.method == 'GET':
        return render(request,'repair/login.html')