from django.shortcuts import render, HttpResponse, redirect 
from .models import Repair
from .forms import RepairForm, SubmitForm, OutsideForm
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def RepairHome(request):

    form = SubmitForm()
    if request.method == 'GET':
        completed_repairs = Repair.objects.filter(repair_status="Completed").order_by('-id')
        incomplete_repairs = Repair.objects.filter(repair_status="Not repaired").order_by('-id')
        completed_paginator = Paginator(completed_repairs, 10)
        repaired_repairs = Repair.objects.filter(repair_status="Repaired").order_by('-id')
        repaired_paginator = Paginator(repaired_repairs,10)
        incomplete_paginator = Paginator(incomplete_repairs,10)
        page_number = request.GET.get("page")
        completed_page_obj = completed_paginator.get_page(page_number)
        incomplete_page_obj = incomplete_paginator.get_page(page_number)
        repaired_page_obj = repaired_paginator.get_page(page_number)
        user = request.user
        groups = user.groups.all()
        print(groups)
        context = {'completed_page_obj': completed_page_obj,'incomplete_page_obj':incomplete_page_obj,'repaired_page_obj':repaired_page_obj,'form': form,'groups':groups}
        return render(request,'repair/arko.html', context)

    else:
        pass

@login_required(login_url='/login/')
def RepairHometest(request):

    form = SubmitForm()
    if request.method == 'GET':
        date = request.GET.get('date')
        if date:
            completed_repairs = Repair.objects.filter(repair_status="Completed",received_date=date).order_by('-id')
            completed_paginator = Paginator(completed_repairs, 10)
            incomplete_repairs = Repair.objects.filter(repair_status="Not repaired",received_date=date).order_by('-id')
            incomplete_paginator = Paginator(incomplete_repairs,10)
            repaired_repairs = Repair.objects.filter(repair_status="Repaired",received_date=date).order_by('-id')
            repaired_paginator = Paginator(repaired_repairs,10)
            unrepairable_repairs = Repair.objects.filter(repair_status="Unrepairable",received_date=date).order_by('-id')
            unrepairable_paginator = Paginator(unrepairable_repairs,10)
            outrepaired_repairs = Repair.objects.filter(repair_status="Outrepaired",received_date=date).order_by('-id')
            outrepaired_paginator = Paginator(outrepaired_repairs,10)
            page_number = request.GET.get("page")
            completed_page_obj = completed_paginator.get_page(page_number)
            incomplete_page_obj = incomplete_paginator.get_page(page_number)
            repaired_page_obj = repaired_paginator.get_page(page_number)
            unrepairable_page_obj = unrepairable_paginator.get_page(page_number)
            outrepaired_page_obj = outrepaired_paginator.get_page(page_number)
            user = request.user
            groups = user.groups.all()
            print("88888888888888888888888888888",outrepaired_page_obj)
            context = {'completed_page_obj': completed_page_obj,'incomplete_page_obj':incomplete_page_obj,'repaired_page_obj':repaired_page_obj,'unrepairable_page_obj':unrepairable_page_obj, 'outrepaired_page_obj':outrepaired_page_obj , 'form': form,'groups':groups}
            return render(request,'repair/arko.html', context)
        
        completed_repairs = Repair.objects.filter(repair_status="Completed").order_by('-id')
        incomplete_repairs = Repair.objects.filter(repair_status="Not repaired").order_by('-id')
        completed_paginator = Paginator(completed_repairs, 10)
        repaired_repairs = Repair.objects.filter(repair_status="Repaired").order_by('-id')
        repaired_paginator = Paginator(repaired_repairs,10)
        incomplete_paginator = Paginator(incomplete_repairs,10)
        unrepairable_repairs = Repair.objects.filter(repair_status="Unrepairable").order_by('-id')
        outrepaired_repairs = Repair.objects.filter(repair_status="Outrepaired").order_by('-id')
        outrepaired_paginator = Paginator(outrepaired_repairs,10)
        unrepairable_paginator = Paginator(unrepairable_repairs,10)
        print(outrepaired_paginator)
        print(outrepaired_repairs)
        page_number = request.GET.get("page")
        completed_page_obj = completed_paginator.get_page(page_number)
        incomplete_page_obj = incomplete_paginator.get_page(page_number)
        repaired_page_obj = repaired_paginator.get_page(page_number)
        unrepairable_page_obj = unrepairable_paginator.get_page(page_number)
        outrepaired_page_obj = outrepaired_paginator.get_page(page_number)
        for repairss in outrepaired_page_obj:
            print(repairss) 
        user = request.user
        groups = user.groups.all()
        context = {'completed_page_obj': completed_page_obj,'incomplete_page_obj':incomplete_page_obj,'repaired_page_obj':repaired_page_obj,'unrepairable_page_obj':unrepairable_page_obj,'outrepaired_page_obj':outrepaired_page_obj,'form': form,'groups':groups}
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
    repair_form = RepairForm()
    outside_form = OutsideForm()


    if request.method  == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            repair =form.save()
            return redirect(f'/repair/product/{repair.repair_id}')
    context = {'repair_form':repair_form,'outside_form':outside_form}
    return render(request,'repair/form.html', context)

def UpdateStatus(request,repair_id,status):
    if status == 'repaired':
        repair = Repair.objects.get(repair_id=repair_id)
        if repair.repair_status == 'Not repaired':
            repair.repair_status = 'Repaired'
            repair.save()
            return redirect('/repair/')
    elif status == 'unrepairable':
        repair = Repair.objects.get(repair_id=repair_id)
        if repair.repair_status == 'Not repaired':
            repair.repair_status = 'Unrepairable'
            repair.save()
            return redirect('/repair/')
    else:
        return HttpResponse("NOT VALID CONTACT BBOB THE GREAT")

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
            repair.repair_status = 'Repaired'
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

    context = {'repair_form':form}
    print(form)
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