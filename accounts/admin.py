from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Branding customization
admin.site.site_header = "MediCare Hospital Administration"
admin.site.site_title = "MediCare Portal"
admin.site.index_title = "Welcome to the MediCare Hospital Management Dashboard"

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Roles', {'fields': ('role',)}),
    )
