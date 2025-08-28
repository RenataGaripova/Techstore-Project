"""URL for products app."""
from django.urls import path

from . import views

app_name = 'accounts'


urlpatterns = [
    path('profile_details/<username>/', views.profile_details, name='profile'),
    path(
        'edit_profile/',
        views.edit_profile,
        name='edit_profile'
    ),
]
