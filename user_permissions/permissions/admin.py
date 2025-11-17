from django.contrib import admin

from .models import BusinessElements, Permissions


@admin.register(BusinessElements)
class RolesAdmin(admin.ModelAdmin):
    """Названия приложений."""

    search_fields = ('name', 'slug')
    list_display = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    """Права доступа к приложениям."""

    search_fields = (
        'business_element__name', 'business_element__slug', 'role'
    )
    list_display = (
        'business_element__name', 'business_element__slug', 'role',
        'get_list_permission'
    )
    list_display_links = ('business_element__slug',)
    empty_value_display = '-пусто-'
    list_editable = ('role', 'get_list_permission')
    empty_value_display = '-пусто-'
