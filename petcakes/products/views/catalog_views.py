from django.shortcuts import render
from products.models import Product


def product_catalog(request):
    products = Product.objects.filter(status='ACTIVE')

    context = {
        'products': products
    }

    return render(request, 'products/catalog.html', context)
