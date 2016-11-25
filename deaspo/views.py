from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from deaspo.models import Product, Project, ProductWebOrder, EmailPlan, Plan
from deaspo.forms import WebOrderForm

# Create your views here.

def index(request):
    products = Product.objects.all() #returns all the products and services
    #pintro = Product.objects.filter(Q(category__exact='Web')| Q(category__exact='Mobile'))
    pintro = Product.objects.filter(pmain=True)[:2][::1]
    pcont = Product.objects.filter(pmain=False)[:3][::1]
    return render(request, "home/index.html", {'services':products, 'servTwo':pintro, 'servThree':pcont})


def services(request):
    products = Product.objects.all()  # returns all the products and services
    return render(request, "services/index.html", {'services':products})

def service(request, service_id):
    service = get_object_or_404(Product, pk=service_id)
    return render(request, 'services/service2.html', {'service': service})

def webOrders(request, service_id, plan_id):
    eplans = EmailPlan.objects.all()
    service =  get_object_or_404(Product, pk=service_id)
    splan = get_object_or_404(Plan, pk=plan_id)
    if not request.POST:
        form = WebOrderForm()
        form.total_price = splan.pn_yearly

    else:
        form = WebOrderForm(request.POST)
        form.hosting_plan = splan.pn_name
    return render(request,'services/webOrder.html',{'eplans':eplans,'service':service,'splan':splan,'form':form})
