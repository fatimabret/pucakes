from django.shortcuts import get_object_or_404, render
from products.models import Product

def product_catalog(request):
    # Traemos todos los productos
    products = Product.objects.all()
    
    return render(request, 'products/catalog/catalog.html', {
        'products': products
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Lógica para elegir el template según el tipo
    template = 'products/cake_detail.html' # Default
    
    # chequeo simple por nombre o categoría si existe
    if 'Muffin' in product.name: 
        template = 'products/muffin_detail.html'
    elif 'Galletita' in product.name or 'Cookie' in product.name:
        template = 'products/cookie_detail.html'
    
    context = {
        'product': product
    }

    return render(request, template, context)