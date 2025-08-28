"""Models to work with users."""
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from products.models import Product


class MyUser(AbstractUser):
    """Custom User Model."""

    phone_number = models.CharField(
        blank=True,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: "
                "'+999999999'. Up to 15 digits allowed."
            )
        ]
    )


class Review(models.Model):
    """Review model."""

    text = models.TextField()
    rating = models.IntegerField(
        validators=(MinValueValidator(0), MaxValueValidator(5)),
        verbose_name='Rating',
        default=0,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta class."""

        default_related_name = 'reviews'
        ordering = ('-created_at',)

    def __str__(self):
        """Magic str method."""
        return f'Comment from author {self.author.username}'
