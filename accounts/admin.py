# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser, Review

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('phone_number',)}),
)

admin.site.register(MyUser, UserAdmin)
admin.site.register(Review)
