from .models import BlockedDate
import json
from django.core.serializers.json import DjangoJSONEncoder

def blocked_dates(request):
    # Obtenemos todas las fechas y las convertimos a formato texto "YYYY-MM-DD"
    dates = list(BlockedDate.objects.values_list('date', flat=True))
    # Las convertimos a string para que Javascript las entienda
    dates_str = [d.strftime("%Y-%m-%d") for d in dates]
    
    return {
        'blocked_dates_json': json.dumps(dates_str)
    }

def cart_context(request):
    cart = request.session.get('cart', [])
    total = 0
    updated_cart = []
    
    # Lógica Universal: Precio x Cantidad
    for item in cart:
        price = float(item['price'])
        quantity = int(item.get('quantity', 1)) # Si no tiene cantidad (ej. tortas viejas), asume 1
        
        # --- NUEVO: Calculamos el subtotal aquí mismo ---
        subtotal = price * quantity
        
        # Agregamos este dato al ítem para poder usarlo en el HTML
        # (Creamos una copia para no modificar la sesión original permanentemente si no queremos)
        item_with_subtotal = item.copy()
        item_with_subtotal['subtotal'] = subtotal
        
        updated_cart.append(item_with_subtotal)
        
        # Sumamos al total general
        total += subtotal
            
    return {
        'cart': updated_cart, # Enviamos la lista nueva con los subtotales
        'cart_total': total, 
        'cart_count': len(cart)
    }