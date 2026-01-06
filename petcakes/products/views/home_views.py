from django.shortcuts import render

def home(request):
    return render(request, 'products/home.html')

def legal_page(request, tipo):
    # Diccionario con los textos legales básicos
    content = {
        'privacidad': {
            'title': 'Política de Privacidad',
            'text': 'En Pucakes nos tomamos muy en serio la privacidad de tus datos y los de tu mascota. Solo usamos tu información para coordinar los pedidos y enviarte cosas ricas. No compartimos tus datos con terceros.'
        },
        'terminos': {
            'title': 'Términos y Condiciones',
            # Texto actualizado con lo de la seña y las 48hs
            'text': 'Al realizar un pedido en Pucakes, aceptas que nuestros productos son artesanales y requieren un mínimo de 48hs de anticipación para su elaboración. Para confirmar cualquier pedido, es obligatorio abonar una seña del 50% del total o el pago completo por adelantado. El saldo restante se abona al momento de la entrega o retiro.'
        },
        'reembolso': {
            'title': 'Política de Reembolso',
            'text': 'Debido a que nuestros productos son alimentos perecederos y personalizados, no aceptamos devoluciones una vez entregado el producto. Si hubo un error en la decoración (ej. nombre mal escrito por nosotros).'
           #  , te reintegraremos el 50% del valor o te enviaremos un producto de compensación.'
        },
        'envio': {
            'title': 'Política de Envío',
            'text': 'Realizamos envíos dentro de Corrientes Capital. El envío se coordina a través de WhatsApp con un costo adicional dependiendo la zona. También ofrecemos la opción de retiro gratuito por nuestro domicilio.'
        }
    }

    # Si el tipo no existe, mostramos uno por defecto o error
    data = content.get(tipo, content['privacidad'])

    return render(request, 'products/legal.html', {'data': data})