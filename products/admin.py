"""Setting up the admin-zone."""
from django.contrib import admin
from .models import Product, Category, Gallery


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin-zone for product model."""

    list_display = ('name', 'description', 'quantity', 'price', 'category')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name', 'price')
    inlines = (GalleryInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin-zone for category model."""

    list_display = ('name', 'description', 'parent')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Gallery)
