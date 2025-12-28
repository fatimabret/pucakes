from django.shortcuts import render
from .models import Order
from .models import Cake

def catalogo(request):
    productos = Cake.objects.all()
    return render(request, 'products/catalogo.html', {
        'productos': productos
    })