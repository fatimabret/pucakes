from django.shortcuts import render, redirect

def ver_carrito(request):
    # Recuperamos el carrito de la sesión. Si no existe, devuelve una lista vacía.
    cart = request.session.get('cart', [])
    
    # Calculamos el total
    total = 0
    for item in cart:
        # Si tienes lógica de precio por cantidad (como cookies), ajusta aquí
        if item.get('type') == 'Galletitas':
            total += item['price'] * item['quantity']
        else:
            # Para tortas y muffins el precio suele ser por unidad/pack
            total += item['price'] 

    return render(request, 'products/cart_detail.html', {
        'cart': cart,
        'total': total
    })

def vaciar_carrito(request):
    if 'cart' in request.session:
        del request.session['cart']
    
    # Redirige al catálogo para empezar de nuevo
    return redirect('catalogo')