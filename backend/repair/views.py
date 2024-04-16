from django.shortcuts import render, HttpResponse, redirect 
from .models import Repair
from .forms import RepairForm
from django.contrib import messages
def RepairHome(request):
    repairs = Repair.objects.all().order_by('-id')
    context = {'repairs':repairs}
    return render(request,'repair/home.html', context)


def Search(request):
    query = request.GET['query']
    print("#############################################")
    if len(query)>40:
        repairs=Repair.objects.none()
    else:
        repair_customer_name= Repair.objects.filter(customer_name__icontains=query)
        repair_phone_model= Repair.objects.filter(phone_model__icontains=query)
        repair_id =Repair.objects.filter(repair_id__icontains=query)
        repair_customer_phone_number = Repair.objects.filter(customer_phone_number__icontains=query)
        repairs=  repair_customer_name.union(repair_customer_phone_number,repair_phone_model,repair_id)

        if repairs.count()==0:
            messages.warning(request, "No search results found. Please refine your query.")

        params = {'repairs':repairs, 'query':query}
        return render(request, 'repair/search.html', params)
    
def Form(request):
    repairs = Repair.objects.all()
    form = RepairForm()

    if request.method  == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/bibhab')
    context = {'repairs':repairs,'form':form}
    return render(request,'repair/form.html', context)

def Product(request,repair_id):
    repair = Repair.objects.get(repair_id = repair_id)
    print(repair)
    return render(request,'repair/product.html', {'repair':repair})