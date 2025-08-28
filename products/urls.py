"""URL for products app."""
from django.urls import path

from . import views

app_name = 'products'


urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.category_list_view, name='category_list'),
    path(
        'category/<slug:category_slug>/',
        views.products_by_category_view,
        name='category_products'
    ),
    path(
        'products/',
        views.all_products_view,
        name='all_products'
    ),
    path(
        'products/<slug:product_slug>',
        views.ProductDetailView.as_view(),
        name='product_details'
    ),
    path(
        'products/<slug:product_slug>/review/',
        views.ReviewCreateView.as_view(),
        name='add_review'
        ),
    path('products/<slug:product_slug>/edit_review/<int:review_id>',
         views.ReviewUpdateView.as_view(),
         name='edit_review'),
    path('products/<slug:product_slug>/delete_review/<int:review_id>',
         views.ReviewDeleteView.as_view(),
         name='delete_review'),
]
