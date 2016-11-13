from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from deaspo.models import Product, Project

# Create your views here.

def index(request):
    products = Product.objects.all() #returns all the products and services
    #pintro = Product.objects.filter(Q(category__exact='Web')| Q(category__exact='Mobile'))
    pintro = Product.objects.filter(pmain=True)[:2][::1]
    pcont = Product.objects.filter(pmain=False)[:3][::1]
    return render(request, "projects/index.html", {'services':products, 'servTwo':pintro, 'servThree':pcont})