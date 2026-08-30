from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from django.contrib import messages
import re 

def cake_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # 1. Obtener datos
        pet_name = request.POST.get('pet_name', '').strip()
        pet_age_str = request.POST.get('pet_age', '')
        animal_type = request.POST.get('animal_type')
        flavor = request.POST.get('flavor')
        # Capturamos el color principal
        cream_color_base = request.POST.get('cream_color')
        decoration_color = request.POST.get('decoration_color')
        
        # Verificamos si eligió la opción doble y la formateamos
        if cream_color_base == 'Personalizar':
            color_1 = request.POST.get('color_crema_1', '')
            color_2 = request.POST.get('color_crema_2', '')
            cream_color = f"{color_1} y {color_2}"
        else:
            cream_color = cream_color_base
        
        # === VALIDACIONES DE SEGURIDAD ===
        
        # A. Validar que no estén vacíos
        if not pet_name or not pet_age_str:
            messages.error(request, "Por favor completa todos los campos obligatorios.")
            return render(request, 'products/catalog/cake_detail.html', {'product': product})

        # B. Validar Nombre (Solo letras y espacios)
        # Expresión regular que permite letras, tildes, ñ y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', pet_name):
            messages.error(request, "El nombre de la mascota no puede contener números ni símbolos.")
            return render(request, 'products/catalog/cake_detail.html', {'product': product})

        # C. Validar Edad (Entero >= 1)
        try:
            pet_age = int(pet_age_str)
            if pet_age < 1:
                messages.error(request, "La edad debe ser mayor o igual a 1.")
                return render(request, 'products/catalog/cake_detail.html', {'product': product})
        except ValueError:
            messages.error(request, "La edad debe ser un número válido.")
            return render(request, 'products/catalog/cake_detail.html', {'product': product})

        # === FIN VALIDACIONES ===

        # 2. Si pasó todas las pruebas, preparamos el carrito
        cart_item = {
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image': product.image.url if product.image else '',
            'type': 'Torta',
            'quantity': 1,
            'details': {
                'Mascota': pet_name,
                'Edad': pet_age, # Usamos la variable ya convertida a int
                'Tipo': animal_type,
                'Sabor': flavor,
                'Cobertura': cream_color,
                'Decoración (Globo/Cinta)': decoration_color
            }
        }

        # 3. Guardar en sesión
        cart = request.session.get('cart', [])
        cart.append(cart_item)
        request.session['cart'] = cart
        
        messages.success(request, 'abrir_carrito')
        return redirect('catalogo') 

    return render(request, 'products/catalog/cake_detail.html', {'product': product})
