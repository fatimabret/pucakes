from django.contrib import admin
from .models import (
    Product,
    Cake,
    Muffin,
    Order,
    OrderItem
)


#   list_display → qué columnas ves en la lista
#   list_filter → filtros laterales
#   search_fields → buscador


# =====================================================
# PRODUCT ADMIN
# =====================================================

#   Productos: Ves nombre, precio y estado.
#   Podés activar/desactivar sin entrar. Filtro por estado.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)


# =====================================================
# CAKE ADMIN
# =====================================================

#   Tortas: tipo de animal, sabor, color de crema, nombre y edad de la mascota.
#   Buscás por nombre de mascota o producto.

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'animal_type',
        'cream_color',
        'pet_name',
        'pet_age'
    )
    list_filter = ('animal_type', 'cream_color')
    search_fields = ('pet_name',)


# =====================================================
# MUFFIN ADMIN
# =====================================================

#   Muffins: Ves color y cantidad. Fácil de identificar packs.

@admin.register(Muffin)
class MuffinAdmin(admin.ModelAdmin):
    list_display = ('product', 'cream_color', 'quantity')
    list_filter = ('cream_color',)


# -------------------------
# ORDER ITEM INLINE
# -------------------------

#   Podés ver: cliente, teléfono, estado, total del pedido.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# -------------------------
# ORDER ADMIN
# -------------------------

#   Desde un Order podés: agregar tortas, agregar muffins, agregar galletas, definir cantidades.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'phone_number',
        'status',
        'created_at',
        'total_price'
    )
    list_filter = ('status',)
    search_fields = ('customer_name', 'phone_number')
    inlines = [OrderItemInline]

