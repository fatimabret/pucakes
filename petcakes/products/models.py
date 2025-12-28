from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import urllib.parse


# =====================================================
# CHOICES (enumeraciones reutilizables)
# =====================================================

class AnimalType(models.TextChoices):
    DOG = 'DOG', 'Dog'
    CAT = 'CAT', 'Cat'


class CreamColor(models.TextChoices):
    PINK = 'PINK', 'Pink'
    BLUE = 'BLUE', 'Blue'
    BEIGE = 'BEIGE', 'Beige'

class DecorationColor(models.TextChoices):
    PINK = 'PINK', 'Pink'
    BLUE = 'BLUE', 'Blue'

class CakeFlavor(models.TextChoices):
    # Sabores del bizcocho
    MEAT = 'MEAT', 'Meat'
    CHICKEN = 'CHICKEN', 'Chicken'
    TUNA = 'TUNA', 'Tuna'

class CakeSize(models.TextChoices):
    IMA = 'IMA', 'Ima (Small)'
    RUBI = 'RUBI', 'Rubi (Large)'
    LASSIE = 'LASSIE', 'Lassie (Double)'

class ProductStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'

class CookieShape(models.TextChoices):
    HUELLA = 'HUELLA', 'Huella'
    HUESO = 'HUESO', 'Hueso'


# =====================================================
# PRODUCT
# Producto base reutilizable (tortas, muffins, cookies)
# =====================================================
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Imagen de portada (thumbnail)
    image = models.ImageField(
        upload_to='products/', 
        null=True, 
        blank=True
    )

    status = models.CharField(
        max_length=8,
        choices=ProductStatus.choices,
        default=ProductStatus.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def category(self):
        if hasattr(self, 'cake'):
            return "Tortas"
        elif hasattr(self, 'muffin'):
            return "Muffins"
        elif hasattr(self, 'cookie'):
            return "Galletitas"
        return "Otros"

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        related_name='images', 
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='products_gallery/')

    def __str__(self):
        return f"Imagen extra de {self.product.name}"


# =====================================================
# CAKE
# Customization for cakes only
# =====================================================

class Cake(models.Model):
    # One cake customization per product (IMA / RUBI / LASSIE)
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE
    )

    animal_type = models.CharField(
        max_length=3,
        choices=AnimalType.choices
    )

    size = models.CharField(
        max_length=6,
        choices=CakeSize.choices
    )

    flavor = models.CharField(
        max_length=7,
        choices=CakeFlavor.choices
    )

    cream_color = models.CharField(
        max_length=5,
        choices=CreamColor.choices
    )

    decoration_color = models.CharField(
        max_length=5,
        choices=DecorationColor.choices
    )

    pet_name = models.CharField(max_length=50)
    pet_age = models.PositiveIntegerField()

    @property
    def dimensions(self):
        if self.size == CakeSize.IMA:
            return "10 cm de diámetro"
        elif self.size == CakeSize.RUBI:
            return "16 cm de diámetro"
        elif self.size == CakeSize.LASSIE:
            return "Dos pisos: Base 16 cm + Tope 10 cm"
        return ""



# =====================================================
# MUFFIN
# Customization for muffins only
# =====================================================

class Muffin(models.Model):
    # One muffin configuration per product
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE
    )

    cream_color = models.CharField(
        max_length=5,
        choices=CreamColor.choices
    )

    quantity = models.PositiveIntegerField(
        default=6,
        help_text="Minimum 6 – Maximum 24"
    )

    def __str__(self):
        return f"Muffin - {self.product.name}"


# =====================================================
# COOKIE
# =====================================================

class Cookie(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE
    )

    shape = models.CharField(
        max_length=10,
        choices=CookieShape.choices,
        default=CookieShape.HUELLA
    )

    quantity = models.PositiveIntegerField(
        default=6,
        help_text="Minimo 6 – Maximo 24"
    )

    def __str__(self):
        return f"Cookie - {self.product.name}"
    

# -------------------------
# ORDER
# -------------------------

#   customer_name → nombre del cliente, phone_number → WhatsApp, status → pendiente / confirmado / cancelado, total_price → se calcula solo
class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    CANCELLED = 'CANCELLED', 'Cancelled'


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())
    

# -------------------------
# ORDER ITEM
# -------------------------

#   apunta a Order, apunta a Product, guarda cantidad (3 a 24 luego lo validamos), guarda el precio (por si cambia después)
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1) # Permitimos 1 para Tortas
        ]
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.quantity * self.price

