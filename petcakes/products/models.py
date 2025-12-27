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


# =====================================================
# PRODUCT
# Producto base reutilizable (tortas, muffins, cookies)
# =====================================================

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    status = models.CharField(
        max_length=8,
        choices=ProductStatus.choices,
        default=ProductStatus.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


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

    pet_name = models.CharField(max_length=50)
    pet_age = models.PositiveIntegerField()

    def __str__(self):
        return f"Cake - {self.product.name}"



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
    
def whatsapp_message(self):
    lines = []
    lines.append(f"Pedido #{self.id}")
    lines.append("")

    for item in self.items.all():
        product = item.product

        lines.append(f"• {product.name}")
        lines.append(f"  Cantidad: {item.quantity}")

        # =====================
        # CAKE
        # =====================
        if hasattr(product, 'cake'):
            cake = product.cake

            emoji = "🐶" if cake.animal_type == "DOG" else "🐱"

            lines.append(f"  Mascota: {cake.pet_name} {emoji}")
            lines.append(f"  Edad: {cake.pet_age} años")
            lines.append(f"  Tamaño: {cake.get_size_display()}")
            lines.append(f"  Sabor: {cake.get_flavor_display()}")
            lines.append(f"  Crema: {cake.get_cream_color_display()}")

        # =====================
        # MUFFIN
        # =====================
        if hasattr(product, 'muffin'):
            muffin = product.muffin
            lines.append(f"  Crema: {muffin.get_cream_color_display()}")

        lines.append(f"  Precio unitario: ${item.price}")
        lines.append("")

    lines.append(f"Total: ${self.total_price}")

    return urllib.parse.quote("\n".join(lines))

def whatsapp_url(self):
    phone = self.phone_number.replace("+", "").replace(" ", "")
    return f"https://wa.me/{phone}?text={self.whatsapp_message()}"


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
            MinValueValidator(6),
            MaxValueValidator(24)
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

