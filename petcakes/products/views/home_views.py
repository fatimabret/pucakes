from django.shortcuts import render

def home(request):
    return render(request, 'products/home.html')

def politicas_view(request):
    # Diccionario con TODAS las políticas juntas
    all_policies = {
        'pedidos': {
            'title': 'Cómo realizar pedidos (Anticipación y Seña)',
            'text': 'Al realizar un pedido en Pucakes, aceptas que nuestros productos son artesanales y requieren un mínimo de 48hs de anticipación para su elaboración. Para confirmar cualquier pedido, es obligatorio abonar una seña del 50% del total o el pago completo por adelantado. El saldo restante se abona al momento de la entrega o retiro.'
        },
        'envios': {
            'title': 'Política de Envíos y Retiros',
            'text': 'Realizamos envíos dentro de Corrientes Capital. El envío se coordina a través de WhatsApp con un costo adicional dependiendo la zona. También ofrecemos la opción de retiro gratuito por nuestro domicilio.'
        },
        'reembolso': {
            'title': 'Política de Reembolso',
            'text': 'Debido a que nuestros productos son alimentos perecederos y personalizados, NO aceptamos devoluciones una vez entregado o retirado el producto. Recomendamos revisar el producto al momento de la entrega.'
        },
        'privacidad': {
            'title': 'Privacidad de Datos',
            'text': 'En Pucakes nos tomamos muy en serio la privacidad de tus datos y los de tu mascota. Solo usamos tu información para coordinar los pedidos y enviarte cosas ricas. No compartimos tus datos con terceros.'
        }
    }

    return render(request, 'products/legal.html', {'policies': all_policies})