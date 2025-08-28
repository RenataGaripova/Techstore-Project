"""URL for products app."""
from django.urls import path

from . import views

app_name = 'carts'


urlpatterns = [
    path('cart_add/<slug:product_slug>', views.cart_add, name='cart_add'),
    path(
        'cart_change/<slug:product_slug>',
        views.cart_change,
        name='cart_change'
    ),
    path(
        'cart_remove/<slug:product_slug>',
        views.cart_remove, 
        name='cart_remove'
    ),
    path('cart_items/', views.cart_items, name='cart_items'),
    path(
        'wishlist_add/<slug:product_slug>',
        views.wishlist_add,
        name='wishlist_add'
    ),
    path(
        'wishlist_remove/<slug:product_slug>',
        views.wishlist_remove,
        name='wishlist_remove'
    ),
    path('wishlist_items/', views.wishlist_items, name='wishlist_items'),
]
