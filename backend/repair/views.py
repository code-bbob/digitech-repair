from django.shortcuts import render, HttpResponse, redirect 
from .models import Repair

def RepairHome(request):
    repairs = Repair.objects.all()
    context = {'repairs':repairs}
    return render(request,'repair/home.html', context)