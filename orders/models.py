"""Order models."""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db.models import CheckConstraint, Q

from products.models import Product

User = get_user_model()


CASH_ON_DELIVERY_CHOICES = [
    ('cash', 'Cash on delivery'),
    ('card', 'Payment by card'),
]

REQUIRES_DELIVERY_CHOICES = [
    ('required', 'Delivery required'),
    ('not_required', 'Pickup'),
]

STATUS_CHOICES = [
    ('P', 'Processing'),
    ('S', 'Shipped'),
    ('D', 'Delivered'),
]


class OrderItemQuerySet(models.QuerySet):
    """Order Itam Query Set."""

    def total_price(self):
        """Get total price of user's carts."""
        return sum(cart.get_products_price() for cart in self)

    def total_quantity(self):
        """Get total quantity of items."""
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    """Order Model."""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=None,
    )
    created_timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: "
                "'+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    delivery_adress = models.TextField(
        null=True,
        blank=True,
        help_text='Provide a full adress,'
        ' including your state, city, apartment, etc.'
    )
    cash_on_delivery = models.CharField(
        max_length=32,
        choices=CASH_ON_DELIVERY_CHOICES,
        default='card',
    )
    requires_delivery = models.CharField(
        max_length=32,
        choices=REQUIRES_DELIVERY_CHOICES,
        default='required',
    )
    is_paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Processing'
        )

    class Meta:
        """Meta class."""

        ordering = ("-created_timestamp",)
        constraints = [
            CheckConstraint(
                check=(
                    Q(requires_delivery='not_required') |
                    Q(delivery_adress__isnull=False, delivery_adress__gt="")
                ),
                name="requires_delivery_adress_is_not_null"
            )
        ]

    def __str__(self):
        """Magic str method."""
        return (f"Order № {self.pk}"
                f" User: {self.user.first_name} {self.user.last_name}")


class OrderItem(models.Model):
    """Order Item."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_DEFAULT,
        null=True,
        default=None,
    )
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class."""

        ordering = ("-created_timestamp",)

    def __str__(self):
        """Magic str method."""
        return f'Order Item from order: {self.order.id}'
