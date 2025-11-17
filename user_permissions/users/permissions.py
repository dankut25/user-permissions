from django.shortcuts import get_object_or_404
from rest_framework import permissions

from permissions.models import BusinessElements, Permissions
from users.constants import (
    APP_NAME,
    ROLE_ADMIN,
    USER_LOGIN_REGISTER_DELETE,
    USER_ROLES_METHODS,
    USER_UPDATE_METHODS_LIST
)
from users.models import Roles


class BasicPermission(permissions.BasePermission):
    """Доступ для администратора при инициализации проекта."""

    def has_permission(self, request, view):
        """Проверка неаутентицированного администратора."""
        print('Zaprashivau', request.user.is_admin)
        return request.user.is_admin


class IsAuthenticatedAndRolesUsers(BasicPermission):
    """Проверка is_authenticated и доступа по роли пользователя."""

    def has_permission(self, request, view):
        """Проверка для ролей и типа запросов."""
        if request.user.is_authenticated:
            user_roles = Roles.objects.filter(user=request.user)
            application = get_object_or_404(BusinessElements, slug=APP_NAME)
            if (
                request.method in USER_UPDATE_METHODS_LIST
                or request.method in USER_LOGIN_REGISTER_DELETE
            ):
                for role in user_roles:
                    permission = Permissions.objects.get(
                        business_element=application.id,
                        role=role.role
                    )
                    return (
                        (permission.get_list_permission is True
                         and request.method == 'GET'
                         )
                        or (
                            permission.partial_update_obj_permission is True
                            and request.method == 'PATCH'
                        )
                        or (
                            permission.create_obj_permission is True
                            and request.method == 'POST'
                        )
                    )
                return super().has_permission(request, view)


class IsAuthenticatedAndAdminUsers(BasicPermission):
    """Проверка is_authenticated и доступа по роли Админ."""

    def has_permission(self, request, view):
        """Проверка для роли Admin на действия с объектами."""
        if request.user.is_authenticated:
            user_roles = Roles.objects.filter(user=request.user)
            application = get_object_or_404(BusinessElements, slug=APP_NAME)
            if request.method in [_.upper() for _ in USER_ROLES_METHODS]:
                for role in user_roles:
                    if role.role == ROLE_ADMIN:
                        permission = Permissions.objects.get(
                            business_element=application.id,
                            role=role.role
                        )
                        return (
                            (permission.get_list_permission is True
                             and request.method == 'GET'
                             )
                            or (
                                permission.create_obj_permission is True
                                and request.method == 'POST'
                            )
                            or (
                                permission.partial_update_obj_permission is True
                                and request.method == 'PATCH'
                            )
                            or (permission.delete_obj_permission is True
                                and request.method == 'DELETE'
                                )
                        )
                return super().has_permission(request, view)
