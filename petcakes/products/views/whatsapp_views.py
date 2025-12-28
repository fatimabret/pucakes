from django.shortcuts import redirect
from django.conf import settings
from products.models import Product, Order, OrderItem
import urllib.parse

def send_whatsapp(request):
    # 1. Recuperamos el carrito de la sesión
    cart = request.session.get('cart', [])

    # Si el carrito está vacío, volver al catálogo
    if not cart:
        return redirect('catalogo')

    # =====================================================
    # PASO A: CREAR EL PEDIDO EN BASE DE DATOS
    # =====================================================
    
    order = Order.objects.create(
        customer_name="Cliente Web (Por confirmar)",
        phone_number="",
        status='PENDING'
    )

    # =====================================================
    # PASO B: GUARDAR ÍTEMS Y ARMAR MENSAJE
    # =====================================================

    lines = []
    lines.append(f"👋 Hola Pucakes! Confirmo mi pedido *#{order.id}*")
    lines.append("")

    total_acumulado = 0

    for item in cart:
        # 1. Recuperar el producto real de la BD
        try:
            product_instance = Product.objects.get(id=item['product_id'])
        except Product.DoesNotExist:
            continue # Si el producto se borró, lo saltamos

        # 2. Calcular valores
        qty = item.get('quantity', 1)
        
        # Precio: Si es galleta multiplicamos, si es torta es unitario
        if item.get('type') == 'Galletitas':
            price_per_unit = item['price'] 
            subtotal = price_per_unit * qty
        else:
            price_per_unit = item['price']
            subtotal = price_per_unit 
        
        # 3. Guardar en Base de Datos (OrderItem)
        OrderItem.objects.create(
            order=order,
            product=product_instance,
            quantity=qty,
            price=price_per_unit 
        )

        # 4. Agregar al Texto de WhatsApp
        nombre_producto = f"🧁 *{item['name']}*"
        if qty > 1:
            nombre_producto += f" (x{qty})"
        
        lines.append(nombre_producto)

        # AQUI AGREGAMOS LA LÓGICA DE DIMENSIONES (TORTAS)
        if hasattr(product_instance, 'cake'):
            lines.append(f"   📏 Medida: {product_instance.cake.dimensions}")

        # Agregar detalles de personalización (Rex, Colores, etc.)
        if 'details' in item:
            for label, value in item['details'].items():
                lines.append(f"   • {label}: {value}")

        lines.append(f"   💲 Subtotal: ${subtotal}")
        lines.append("")

        total_acumulado += subtotal

    # =====================================================
    # PASO C: FINALIZAR Y LIMPIAR
    # =====================================================

    lines.append(f"💰 *TOTAL A PAGAR: ${total_acumulado}*")
    lines.append("")
    lines.append("Quedo a la espera para coordinar pago y entrega. 🐾")

    # 1. Limpiar el carrito de la sesión
    request.session['cart'] = []

    # 2. Generar Link
    message = urllib.parse.quote("\n".join(lines))
    
    # Usamos la variable de settings
    phone = settings.WHATSAPP_PHONE 
    
    url = f"https://wa.me/{phone}?text={message}"

    return redirect(url)