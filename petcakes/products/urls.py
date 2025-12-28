from django.urls import path
from products.views.home_views import home
from products.views.catalog_views import product_catalog
from products.views.order_views import confirm_order

# Importamos las vistas de detalle
from products.views.cake_views import cake_detail
from products.views.muffin_views import muffin_detail
from products.views.cookies_views import cookie_detail

# IMPORTANTE: Importamos las vistas del carrito que creamos antes
from products.views.cart_views import ver_carrito, vaciar_carrito
from products.views.whatsapp_views import send_whatsapp

urlpatterns = [
    path('', home, name='home'),
    path('catalogo/', product_catalog, name='catalogo'),
    
    # Rutas de Detalle y Personalización
    path('producto/torta/<int:product_id>/', cake_detail, name='cake_detail'),
    path('producto/muffin/<int:product_id>/', muffin_detail, name='muffin_detail'),
    path('producto/cookie/<int:product_id>/', cookie_detail, name='cookie_detail'),

    # Rutas del Carrito (Reemplazan al add_to_cart)
    path('mi-pedido/', ver_carrito, name='ver_carrito'),
    path('limpiar-pedido/', vaciar_carrito, name='vaciar_carrito'),

    path('confirm-order/', confirm_order, name='confirm_order'),

    path('whatsapp/', send_whatsapp, name='send_whatsapp'),
]