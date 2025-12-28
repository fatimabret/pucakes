from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from django.contrib import messages

def cookie_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # 1. Obtener datos
        try:
            qty = int(request.POST.get('quantity'))
        except (ValueError, TypeError):
            qty = 6 # Valor por defecto si falla
        
        shape = request.POST.get('shape')

        # 2. Validación de seguridad (Backend)
        if qty < 6:
            messages.error(request, "El mínimo es de 6 galletitas.")
            return render(request, 'products/cookie_detail.html', {'product': product})
        if qty > 24:
            messages.error(request, "El máximo es de 24 galletitas.")
            return render(request, 'products/cookie_detail.html', {'product': product})

        # 3. Armar carrito
        cart_item = {
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image': product.image.url if product.image else '',
            'type': 'Galletitas',
            'quantity': qty, # Cantidad real elegida
            'details': {
                'Forma': shape
            }
        }

        # 4. Guardar
        cart = request.session.get('cart', [])
        cart.append(cart_item)
        request.session['cart'] = cart
        
        messages.success(request, '¡Galletitas agregadas!')
        return redirect('ver_carrito')

    return render(request, 'products/catalog/cookie_detail.html', {'product': product})