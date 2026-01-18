from django.shortcuts import redirect
from django.conf import settings
from products.models import Product, Order, OrderItem
import urllib.parse

def send_whatsapp(request):
    # Si intentan entrar directo por URL sin enviar formulario, redirigir
    if request.method != 'POST':
        return redirect('catalogo')

    cart = request.session.get('cart', [])
    if not cart:
        return redirect('catalogo')

    # 1. RECUPERAR LA FECHA DEL FORMULARIO
    delivery_date = request.POST.get('delivery_date', 'A coordinar')

    # Formatear la fecha (dd/mm/aaaa)
    try:
        parts = delivery_date.split('-')
        if len(parts) == 3:
            delivery_date_fmt = f"{parts[2]}/{parts[1]}/{parts[0]}"
        else:
            delivery_date_fmt = delivery_date
    except:
        delivery_date_fmt = delivery_date

    # 2. Creamos el Pedido en la Base de Datos (Para tener historial)
    # Status 'PENDING' porque aún no pagó
    
    order = Order.objects.create(
        customer_name="Cliente Web",
        status='PENDING'
    )

    # 3. Empezamos a escribir el mensaje

    lines = []
    lines.append(f"   ¡Hola Pucakes! Confirmo mi pedido *#{order.id}*")
    # AQUI AGREGAMOS LA FECHA 
    lines.append(f"   *Fecha de entrega solicitada:* {delivery_date_fmt}")
    lines.append("")

    total_acumulado = 0

    for item in cart:
        # 1. Recuperar el producto real de la BD
        try:
            product_instance = Product.objects.get(id=item['product_id'])
        except Product.DoesNotExist:
            continue # Si el producto se borró, lo saltamos

        # 2. Calcular valores
        qty = int(item.get('quantity', 1))
        price = float(item['price'])
        subtotal = price * qty

        # Convertimos el diccionario de detalles a un texto simple
        detalles_texto = ""
        if 'details' in item and item['details']:
            for label, value in item['details'].items():
                detalles_texto += f"{label}: {value}\n"

        # 3. Guardar en Base de Datos (OrderItem)
        OrderItem.objects.create(
            order=order,
            product=product_instance,
            quantity=qty,
            price=price,
            details=detalles_texto
        )

        # 4. Agregar al Texto de WhatsApp
        nombre_producto = f"   *{item['name']}*"
        if qty > 1:
            nombre_producto += f" (x{qty} unidades)"
        lines.append(nombre_producto)

        # Detalles de Personalización (Aquí sale: Mascota, Edad, Tipo, etc.)
        if 'details' in item and item['details']:
            lines.append("   _Detalles:_")
            for label, value in item['details'].items():
                # Ej: "   • Mascota: Firulais"
                lines.append(f"  • {label}: {value}")
        
        # Medidas (solo si es torta y el modelo lo tiene)
        if hasattr(product_instance, 'cake'):
            lines.append(f"   Medida: {product_instance.cake.dimensions}")

        # Subtotal del ítem
        lines.append(f"   Subtotal: ${subtotal:,.0f}") # Formato sin decimales si prefieres
        lines.append("") # Línea vacía para separar productos

        total_acumulado += subtotal

    # 4. FINALIZAR Y LIMPIAR

    lines.append("-------------------------------------------------")
    lines.append(f"   *TOTAL A PAGAR: ${total_acumulado:,.0f}*")
    lines.append("")

    senia = total_acumulado * 0.5  # Calculamos el 50%
    lines.append(f"   *Seña mínima (50%): ${senia:,.0f}* _(Requerida para confirmar fecha)_")

    lines.append("")
    lines.append("Quedo a la espera para coordinar pago y entrega. ¡Gracias!")

    # 1. Limpiar el carrito de la sesión
    request.session['cart'] = []

    # 2. Generar Link
    full_text = "\n".join(lines)
    message = urllib.parse.quote(full_text)
    
    # Usamos la variable de settings
    phone = settings.WHATSAPP_PHONE 
    
    url = f"https://wa.me/{phone}?text={message}"

    return redirect(url)