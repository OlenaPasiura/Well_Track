from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "profile_type", "gender", "age", "is_staff", "is_active")
    list_filter = ("profile_type", "is_staff", "is_active")
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password", "profile_type")}),
        ("Особиста інформація", {"fields": ("gender", "age")}),
        ("Права", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "profile_type", "is_staff", "is_active"),
        }),
    )