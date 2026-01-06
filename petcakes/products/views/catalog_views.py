from django.shortcuts import get_object_or_404, render
from products.models import Product, Cake, Muffin, Cookie

def product_catalog(request):
    print("--- INICIANDO DEBUG DEL CATÁLOGO ---")

    # 1. TORTAS
    ids_tortas = list(Cake.objects.values_list('product_id', flat=True))
    # QUITAMOS status='active' para ver si aparecen
    tortas = Product.objects.filter(id__in=ids_tortas) 
    print(f"IDs encontrados en tabla Cake: {ids_tortas}")
    print(f"Productos Tortas recuperados: {tortas.count()}")

    # 2. MUFFINS
    ids_muffins = list(Muffin.objects.values_list('product_id', flat=True))
    muffins = Product.objects.filter(id__in=ids_muffins)
    print(f"IDs encontrados en tabla Muffin: {ids_muffins}")
    print(f"Productos Muffins recuperados: {muffins.count()}")

    # 3. GALLETITAS
    ids_galletitas = list(Cookie.objects.values_list('product_id', flat=True))
    galletitas = Product.objects.filter(id__in=ids_galletitas)
    print(f"IDs encontrados en tabla Cookie: {ids_galletitas}")
    print(f"Productos Galletitas recuperados: {galletitas.count()}")

    # 4. OTROS (Huérfanos)
    todos_los_ids = ids_tortas + ids_muffins + ids_galletitas
    otros = Product.objects.exclude(id__in=todos_los_ids)
    print(f"Productos sin categoría (Otros): {otros.count()}")
    
    print("--- FIN DEBUG ---")

    context = {
        'tortas': tortas,
        'muffins': muffins,
        'galletitas': galletitas,
        'otros': otros,
    }
    
    return render(request, 'products/product_catalog.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Lógica para elegir el template según el tipo
    template = 'products/cake_detail.html' # Default
    
    # chequeo simple por nombre o categoría si existe
    if 'Muffin' in product.name: 
        template = 'products/muffin_detail.html'
    elif 'Galletita' in product.name or 'Cookie' in product.name:
        template = 'products/cookie_detail.html'
    
    context = {
        'product': product
    }

    return render(request, template, context)