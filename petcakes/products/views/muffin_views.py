from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from django.contrib import messages

def muffin_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # 1. Capturamos los datos
        qty_str = request.POST.get('quantity', '6')
        
        # Evitamos errores si no mandan número
        try:
            quantity = int(qty_str)
        except ValueError:
            quantity = 6

        # --- SEGURIDAD: FORZAR LÍMITES ---
        if quantity < 6:
            quantity = 6
        elif quantity > 24:
            quantity = 24
        
        cream_color_base = request.POST.get('color_crema')
        
        if cream_color_base == 'Personalizar':
            color_1 = request.POST.get('color_crema_1', '')
            color_2 = request.POST.get('color_crema_2', '')
            cream_color = f"{color_1} y {color_2}"
        else:
            cream_color = cream_color_base
        
        # 2. Creamos el diccionario del producto
        cart_item = {
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image': product.image.url if product.image else '',
            'type': 'Muffins',
            'quantity': quantity,
            'details': {
                'Pack Seleccionado': f"x{quantity} unidades",
                'Color de crema': cream_color
            }
        }

        # 3. Guardamos en la sesión
        cart = request.session.get('cart', [])
        cart.append(cart_item)
        request.session['cart'] = cart
        
        # Enviamos la señal para abrir el sidebar
        messages.success(request, 'abrir_carrito')
        
        # Redirigimos al catálogo en lugar de la página de carrito
        return redirect('catalogo') 

    return render(request, 'products/catalog/muffin_detail.html', {'product': product})
