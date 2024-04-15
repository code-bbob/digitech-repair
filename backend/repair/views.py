from django.shortcuts import render, HttpResponse, redirect 
from .models import Repair
from .forms import RepairForm
def RepairHome(request):
    repairs = Repair.objects.all()
    form = RepairForm()

    if request.method  == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'repairs':repairs,'form':form}
    return render(request,'repair/home.html', context)