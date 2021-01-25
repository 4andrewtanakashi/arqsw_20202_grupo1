from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm


def list_products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def delete_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('list_products')

    return render(request, 'prod-delete-confirm.html', {'product': product})
