from django.shortcuts import get_object_or_404

from permissions.models import BusinessElements, Permissions
from permissions.constants import (
    APP_NAME,
    PERMISSIONS_ROLES_METHODS
)
from users.constants import ROLE_ADMIN
from users.models import Roles
from users.permissions import BasicPermission


class IsAuthenticatedAndAdminPermissions(BasicPermission):
    """Проверка is_authenticated и доступа по роли Админ."""

    def has_permission(self, request, view):
        """Проверка для роли Admin на действия с объектами."""
        if request.user.is_authenticated:
            user_roles = Roles.objects.filter(user=request.user)
            application = get_object_or_404(BusinessElements, slug=APP_NAME)
            if request.method in [_.upper() for _ in PERMISSIONS_ROLES_METHODS]:
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
