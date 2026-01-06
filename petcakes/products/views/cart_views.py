from django.shortcuts import redirect
from django.contrib import messages

def ver_carrito(request):
    # Como usamos el Sidebar Lateral, no hay página exclusiva de carrito.
    # Si alguien intenta entrar aquí, lo mandamos al catálogo.
    return redirect('catalogo')

def vaciar_carrito(request):
    # Borramos el carrito de la sesión
    if 'cart' in request.session:
        del request.session['cart']
    
    # Volvemos al catálogo (el carrito aparecerá vacío)
    return redirect('catalogo')

# Borrar un solo ítem por su posición (índice)
def remove_item(request, item_index):
    cart = request.session.get('cart', [])
    
    # Verificamos que el índice exista para no dar error
    if 0 <= item_index < len(cart):
        del cart[item_index] # Borramos el ítem
        request.session['cart'] = cart # Guardamos
        request.session.modified = True 
    
    # Enviamos la señal para que el carrito se abra solo
    messages.success(request, 'abrir_carrito')
    
    return redirect('catalogo')
