from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
# Create your views here.
def home(request):
    Products = Product.objects.all()
    instock_count = Product.objects.filter(state='in stock').count()
    outofstock_count = Product.objects.filter(state='out of stock').count()
    intransit_count = Product.objects.filter(state='in transit').count()
    damaged_count = Product.objects.filter(state='damaged').count()
    last_5_products = Products.order_by('-created_at')[:3]
    product= request.GET.get("productid")  # from ?productid=1
    if product:
        try:
            product = Product.objects.get(id=int(product))
        except Product.DoesNotExist:
            return HttpResponse("Product not found", status=404)
    else:
        product = None


    context = {
        'Products': Products,
        'instock_count': instock_count,
        'outofstock_count': outofstock_count,
        'intransit_count': intransit_count,
        'damaged_count': damaged_count,
        'last_5_products': last_5_products,
        'product': product
    }
    return render(request, 'home.html', context)
