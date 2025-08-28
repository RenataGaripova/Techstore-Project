"""Models to work with carts and wishlists."""
from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product

User = get_user_model()


class CartQuerySet(models.QuerySet):
    """Cart QuerySet."""

    def total_price(self):
        """Get total price of user's carts."""
        return sum(cart.get_products_price() for cart in self)

    def total_quantity(self):
        """Get total quantity of items in the user's carts."""
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    """Cart Model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(default=0)
    session_key = models.CharField(max_length=32, blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartQuerySet().as_manager()

    class Meta:
        """Meta class."""

        ordering = ("-created_timestamp",)

    def __str__(self):
        """Magic method."""
        return f"{self.user.username}'s cart"

    def get_products_price(self):
        """Get the subtotal of a cart."""
        return round(self.product.sell_price * self.quantity, 2)


class Wishlist(models.Model):
    """Wishlist model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    session_key = models.CharField(max_length=32, blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class."""

        ordering = ("-created_timestamp",)
        constraints = [
            models.constraints.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_wishlist_product'
            ),
        ]
