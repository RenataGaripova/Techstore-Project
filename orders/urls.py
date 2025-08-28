"""URL for products app."""
from django.urls import path

from . import views

app_name = 'orders'


urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('order_list/', views.order_list, name='order_list'),
]
