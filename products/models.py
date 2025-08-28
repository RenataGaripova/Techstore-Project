"""Setting up models."""
from django.db import models
from django.db.models import Q


class Category(models.Model):
    """Category model."""

    slug = models.SlugField(unique=True, null=True)
    name = models.CharField(max_length=128)
    description = models.TextField()
    photo = models.ImageField(upload_to='category_images')
    parent = models.ForeignKey(
        "self",
        related_name="subcategories",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta class."""

        verbose_name_plural = 'Categories'

    def __str__(self):
        """Magic method to show name of a category."""
        return self.name

    def get_all_products(self):
        """Get all products from parent category and it's subcategories."""
        direct_subcategories = self.subcategories.all()
        return Product.objects.filter(
            Q(category=self) | Q(category__in=direct_subcategories)
        )

    def count_all_products(self):
        """Get the number of products from parent and it's subcategories."""
        return self.get_all_products().count()


class Product(models.Model):
    """Product model."""

    slug = models.SlugField(unique=True, null=True)
    name = models.CharField(max_length=128)
    producer = models.CharField(max_length=128, blank=True)
    info = models.TextField(default="Product info.")
    description = models.TextField()
    quantity = models.IntegerField()
    color = models.CharField(max_length=128, null=True, blank=True)
    rating = models.FloatField(blank=True, default=1.0)
    discount = models.DecimalField(
        default=0.00,
        max_digits=7,
        decimal_places=2,
        verbose_name='discount in %',
    )
    created_at = models.DateTimeField(
        'Created',
        auto_now_add=True
    )
    price = models.DecimalField(
        default=0.00,
        max_digits=7,
        decimal_places=2,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    class Meta:
        """Meta class."""

        default_related_name = 'products'

    def __str__(self):
        """Magic method to show product's name."""
        return self.name

    def get_coverage_photo(self):
        """Method to get image for a product card."""
        return self.images.first().photo

    @property
    def sell_price(self):
        """Method to get result price of a product."""
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price


class Gallery(models.Model):
    """Gallery model."""

    photo = models.ImageField(upload_to='product_images')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
    )

    class Meta:
        """Meta class."""

        verbose_name_plural = 'Galleries'
