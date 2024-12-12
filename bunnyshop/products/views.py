from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    products=Product.objects.filter(isTrending=True)
    return render(request,"index.html",{"products":products})

def productDetail(request,id):
    product=Product.objects.get(pk=id)
    return render(request,"details.html",{"product":product})

def products(request):
    all_products=Product.objects.all().order_by("name")
    
    page=request.GET.get("page")
    paginator=Paginator(all_products,3)

    all_products=paginator.get_page(page)
    return render(request,"product.html",{"all_products":all_products})