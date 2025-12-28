from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from django.contrib import messages

def muffin_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # 1. Capturamos los datos del formulario HTML
        pack_size = request.POST.get('pack_size') 
        cream_color = request.POST.get('cream_color')
        
        # 2. Creamos el diccionario del producto
        cart_item = {
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image': product.image.url if product.image else '',
            'type': 'Muffins',
            'quantity': 1, 
            'details': {
                'Tamaño': pack_size,
                'Color de crema': cream_color
            }
        }

        # 3. Guardamos en la sesión
        cart = request.session.get('cart', [])
        cart.append(cart_item)
        request.session['cart'] = cart
        
        messages.success(request, '¡Muffins agregados al pedido!')
        
        # CORRECCIÓN AQUÍ: Redirigimos al carrito
        return redirect('ver_carrito')

    return render(request, 'products/catalog/muffin_detail.html', {'product': product})
