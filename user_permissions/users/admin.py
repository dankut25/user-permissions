"""Настройка админ-панели для модели пользователя."""
from django.contrib import admin

from .constants import ROLE_GUEST
from .models import Roles, User


admin.site.empty_value_display = 'Не задано'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Расширенная модель пользователя для администрирования."""

    search_fields = ('email', 'first_name', 'last_name')
    list_display = ('email', 'get_user_roles', 'date_joined')
    empty_value_display = '-пусто-'

    @admin.display(description='Роли пользователя')
    def get_user_roles(self, obj):
        return ', '.join([role.role for role in obj.roles.all()])

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.roles.exists():
            obj.roles.create(role=ROLE_GUEST)


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    """Расширенная модель пользователя для администрирования."""

    search_fields = ('user__email', 'role', 'user__id')
    list_display = ('user__id', 'user', 'role')
    list_display_links = ('user',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'
