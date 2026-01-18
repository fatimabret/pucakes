from django.contrib import admin
from django.utils.html import mark_safe # Para mostrar HTML (imágenes)
from .models import (
    Product,
    ProductImage,
    Cake,
    Muffin,
    Cookie,
    Order,
    OrderItem
)
from .models import BlockedDate

# =====================================================
# CONFIGURACIÓN DE IMÁGENES EXTRA
# =====================================================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    # Mostramos una miniatura de la imagen extra también
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 100px; height: auto;" />')
        return "No Image"

# =====================================================
# PRODUCT ADMIN (MEJORADO)
# =====================================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Agregamos 'image_preview' a la lista
    list_display = ('image_preview', 'name', 'price', 'category_display', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name',)
    list_editable = ('status', 'price') # ¡Permite editar precio y estado sin entrar al producto!
    inlines = [ProductImageInline]

    # Función para mostrar la miniatura en el listado
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />')
        return "No Image"
    
    image_preview.short_description = "Foto"

    # Función para mostrar qué tipo de producto es
    def category_display(self, obj):
        return obj.category
    category_display.short_description = "Categoría"


# =====================================================
# PEDIDOS (ORDER ADMIN MEJORADO)
# =====================================================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal_display', 'details') # Solo lectura para no tocar precios históricos
    can_delete = False # No borrar ítems de un pedido histórico

    def subtotal_display(self, obj):
        return f"${obj.subtotal}"
    subtotal_display.short_description = "Subtotal"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'status', # Estado
        'total_items', # Cantidad de cosas
        'total_price_display', # Total $
        'created_at'
    )
    # Filtros laterales para encontrar rápido pedidos pendientes
    list_filter = ('status', 'created_at')
    
    # Buscador por nombre de cliente
    search_fields = ('customer_name', 'phone_number')
    
    # ¡Súper útil! Cambiar estado de "Pendiente" a "Confirmado" desde la lista
    list_editable = ('status',)
    
    inlines = [OrderItemInline]
    
    # Ordenar por el más reciente primero
    ordering = ('-created_at',)

    def total_items(self, obj):
        return obj.items.count()
    total_items.short_description = "Items"

    def total_price_display(self, obj):
        return f"${obj.total_price}"
    total_price_display.short_description = "Total"


# =====================================================
# SUB-PRODUCTOS (TORTAS, MUFFINS, COOKIES)
# =====================================================
# Los dejamos igual, solo para detalles técnicos
@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('product', 'animal_type', 'pet_name')

@admin.register(Muffin)
class MuffinAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')

@admin.register(Cookie)
class CookieAdmin(admin.ModelAdmin):
    list_display = ('product', 'shape')

@admin.register(BlockedDate)
class BlockedDateAdmin(admin.ModelAdmin):
    list_display = ('date', 'reason')
    ordering = ('date',)