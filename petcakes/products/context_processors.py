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
    
    # Calculamos el total aquí para tenerlo disponible siempre
    for item in cart:
        if item.get('type') == 'Galletitas':
            total += item['price'] * item['quantity']
        else:
            total += item['price'] # Tortas y Muffins (precio unitario o pack)
            
    return {
        'cart': cart,
        'cart_total': total,
        'cart_count': len(cart)
    }