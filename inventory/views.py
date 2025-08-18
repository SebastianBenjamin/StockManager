from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def home(request):
    Products = Product.objects.all()
    instock_count = Product.objects.filter(state='in stock').count()
    outofstock_count = Product.objects.filter(state='out of stock').count()
    intransit_count = Product.objects.filter(state='in transit').count()
    damaged_count = Product.objects.filter(state='damaged').count()
    last_5_products = Products.order_by('-updated_at')[:3]
    product= request.GET.get("productid")  
    status = request.GET.get("status")
    if  product and product.isdigit():
        product = int(product)
        product = Product.objects.filter(id=product).first()
        if not product:
            messages.error(request, "Product not found.")
            return HttpResponseRedirect(reverse('home'))
    elif product and not product.isdigit():
        product = product.strip().lower()
        product = Product.objects.filter(name__icontains=product).first()
        if not product:
            messages.error(request, "Product not found.")
            return HttpResponseRedirect(reverse('home'))
    else:
        product = None
    


    context = {
        'Products': Products,
        'instock_count': instock_count,
        'outofstock_count': outofstock_count,
        'intransit_count': intransit_count,
        'damaged_count': damaged_count,
        'last_5_products': last_5_products,
        'product': product,
        'status': status,
    }
    return render(request, 'home.html', context)
def get_all_products():
    products = Product.objects.all()
    return products
def add_product(request):
    products= get_all_products()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        state = request.POST.get('state', 'not available')
        
        if name and description and price and quantity and state:
            for product in products:
                if product.name.strip().lower() == name.strip().lower():
                    messages.error(request, "Product with this name already exists.")
                    return HttpResponseRedirect(reverse('home'))
            try :
                price = float(price)
                quantity = int(quantity)
                product = Product.objects.create(
                    name=name,
                    description=description,
                    price=price,
                    quantity=quantity,
                    state=state
                )
                product.save()
                messages.success(request, "Product added successfully.")
                
            except ValueError:
                messages.error(request, "Invalid input. Please check the data you entered.")
            
        else:
            messages.error(request, "All fields are required.")
    else:
        messages.error(request, "Invalid request method.")

    return HttpResponseRedirect(reverse('home'))

def edit_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('productid')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        state = request.POST.get('state', 'not available')
        
        try:
                product = Product.objects.get(id=int(product_id))
                if name:
                    product.name = name
                if description:
                    product.description = description
                if price:
                    product.price = float(price)
                if quantity:
                    product.quantity = int(quantity)
                if state:
                    product.state = state
                product.updated_at = None  # Reset updated_at to current time
                if product.state not in ['in stock', 'out of stock', 'in transit', 'damaged']:
                    messages.error(request, "Invalid state. Please select a valid state.")
               
                
                product.save()
                messages.success(request, "Product updated successfully.")
        except Product.DoesNotExist:
                messages.error(request, "Product not found.")
        except ValueError:
                messages.error(request, "Invalid input. Please check the data you entered.")
    else:
        messages.error(request, "Invalid request method.")
    return HttpResponseRedirect(reverse('home'))
def delete_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('productid')
        if product_id:
            try:
                product = Product.objects.get(id=int(product_id))
                product.delete()
                messages.success(request, "Product deleted successfully.")
            except Product.DoesNotExist:
                messages.error(request, "Product not found.")
            except ValueError:
                messages.error(request, "Invalid product ID.")
        else:
            messages.error(request, "Product ID is required.")
    else:
        messages.error(request, "Invalid request method.")
    return HttpResponseRedirect(reverse('home'))