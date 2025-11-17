from django.shortcuts import get_object_or_404

from permissions.models import BusinessElements, Permissions
from users.models import Roles
from users.permissions import BasicPermission


APP_NAME = 'mock'
PERMISSIONS_MOCK_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']


class MockRolesPermissions(BasicPermission):
    """Проверка по ролям пользователей."""

    def has_permission(self, request, view):
        """Проверка ролей пользователей."""
        if request.user.is_authenticated:
            user_roles = Roles.objects.filter(user=request.user)
            application = get_object_or_404(BusinessElements, slug=APP_NAME)
            if request.method in PERMISSIONS_MOCK_METHODS:
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
                            permission.create_obj_permission is True
                            and request.method == 'POST'
                        )
                        or (
                            permission.update_obj_permission is True
                            and request.method == 'PUT'
                        )
                        or (
                            permission.partial_update_obj_permission is True
                            and request.method == 'PATCH'
                        )
                        or (permission.delete_obj_permission is True
                            and request.method == 'DELETE'
                            )
                    )
