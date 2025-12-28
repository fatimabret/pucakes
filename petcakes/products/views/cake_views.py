from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from django.contrib import messages

def cake_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # 1. Obtener datos del formulario
        pet_name = request.POST.get('pet_name')
        pet_age = request.POST.get('pet_age')
        flavor = request.POST.get('flavor')
        cream_color = request.POST.get('cream_color')
        decoration_color = request.POST.get('decoration_color')
        
        # 2. Preparar el objeto para el carrito
        cart_item = {
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image': product.image.url if product.image else '',
            'type': 'Torta',
            'quantity': 1, # Las tortas suelen ser de a una
            'details': {
                'Mascota': pet_name,
                'Edad': pet_age,
                'Sabor': flavor,
                'Cobertura': cream_color,
                'Decoración (Globo/Cinta)': decoration_color
            }
        }

        # 3. Guardar en sesión
        cart = request.session.get('cart', [])
        cart.append(cart_item)
        request.session['cart'] = cart
        
        messages.success(request, f'¡{product.name} agregado al pedido!')
        
        # CORRECCIÓN AQUÍ: Redirigimos al carrito para ver el resumen
        return redirect('ver_carrito') 

    return render(request, 'products/catalog/cake_detail.html', {'product': product})