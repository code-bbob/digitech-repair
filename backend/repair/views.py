from django.shortcuts import render, HttpResponse, redirect 
from .models import Repair
from .forms import RepairForm
from django.views import View
from html2image import Html2Image
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

hti = Html2Image()


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


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

        # if repairs.count()==0:
            # messages.warning(request, "No search results found. Please refine your query.")

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
    context = {'repairs':repairs,'form':form}
    return render(request,'repair/form.html', context)



def Product(request,repair_id):
    repair = Repair.objects.get(repair_id = repair_id)
    return render(request,'repair/naya.html', {'repair':repair})

def Pdf(request,repair_id):

    repair = Repair.objects.get(repair_id = repair_id)
    pdf = render_to_pdf('repair/naya.html', {'repair':repair})
    return HttpResponse(pdf, content_type='application/pdf')

