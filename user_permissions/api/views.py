from http import HTTPStatus

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken
)

from .serializers import (
    BusinessElementsSerializer,
    PermissionsSerializer,
    RolesSerializer,
    UsersLoginSerializer,
    UserSerializer,
    UsersRegistrationSerializer
)
from permissions.models import BusinessElements, Permissions
from permissions.permissions import IsAuthenticatedAndAdminPermissions
from users.constants import (
    USER_LOGIN_REGISTER_DELETE,
    USER_ROLES_METHODS,
    USER_UPDATE_METHODS_LIST
)
from users.models import Roles
from users.permissions import (
    IsAuthenticatedAndAdminUsers,
    IsAuthenticatedAndRolesUsers
)


User = get_user_model()


@api_view(USER_LOGIN_REGISTER_DELETE)
@permission_classes([AllowAny])
def registration_view(request):
    """Функция для регистрации пользователей."""
    serializer = UsersRegistrationSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError:
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    serializer.validated_data.pop('password_confirm')
    serializer.save()
    return Response(serializer.validated_data, status=HTTPStatus.OK)


@api_view(USER_LOGIN_REGISTER_DELETE)
@permission_classes([AllowAny])
def login_view(request):
    """Функция для аутентификации пользователей.

    Аутентифицируем пользователся по email и паролю, а в ответ
    выдаем токены доступа JWT.
    """
    serializer = UsersLoginSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError:
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    user = User.objects.get(email=serializer.validated_data['email'])
    token = RefreshToken.for_user(user)
    return Response(
        {
            'refresh': str(token),
            'access': str(token.access_token),
        },
        status=HTTPStatus.OK
    )


@api_view(USER_UPDATE_METHODS_LIST)
@permission_classes([IsAuthenticatedAndRolesUsers])
def user_update_view(request):
    """Функция обработки запросов через эндпоинт /users/me/."""
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    serializer = UserSerializer(
        request.user,
        data=request.data,
        partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(USER_LOGIN_REGISTER_DELETE)
@permission_classes([IsAuthenticatedAndRolesUsers])
def soft_delete_view(request):
    """Функция для мягкого удаления пользователя."""
    request.user.is_active = False
    request.user.save()
    tokens = OutstandingToken.objects.filter(user_id=request.user.id)
    for token in tokens:
        t, _ = BlacklistedToken.objects.get_or_create(token=token)
    return Response(
        {'detail': f'User {request.user.email} удален. '
         'Все токены заблокированы.'},
        status=HTTPStatus.OK)


@api_view(USER_LOGIN_REGISTER_DELETE)
@permission_classes([IsAuthenticatedAndRolesUsers])
def logout_view(request):
    """Действия в случае Logout.

    Получаем Refresh токен в запросе и заносим его в черный список.
    """
    if 'refresh' not in request.data:
        raise ValidationError(
            {'refresh': 'Не указан refresh токен в запросе.'}
        )
    token = OutstandingToken.objects.get(token=request.data['refresh'])
    t, _ = BlacklistedToken.objects.get_or_create(token=token)
    return Response(status=HTTPStatus.OK)


class RolesViewSet(viewsets.ModelViewSet):
    """ViewSet для ролей пользователя."""

    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    permission_classes = [IsAuthenticatedAndAdminUsers]
    filter_backends = [SearchFilter]
    search_fields = ['user__email']
    http_method_names = USER_ROLES_METHODS

    def destroy(self, request, *args, **kwargs):
        """Проверки перед удалением роли.."""
        if Roles.objects.filter(user=self.get_object().user).count() == 1:
            raise ValidationError(
                {'role': 'У пользователя должна быть хотя бы одна роль.'}
            )
        if self.get_object().user.is_active is False:
            raise ValidationError(
                {'role': 'Данный аккаунт был удален.'}
            )
        return super().destroy(request, *args, **kwargs)


class BusinessElementsViewSet(viewsets.ModelViewSet):
    """ViewSet для ролей названия приложений."""

    queryset = BusinessElements.objects.all()
    serializer_class = BusinessElementsSerializer
    permission_classes = [IsAuthenticatedAndAdminPermissions]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'slug']
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'patch', 'delete']


class PermissionsViewSet(viewsets.ModelViewSet):
    """ViewSet для ролей названия приложений."""

    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer
    permission_classes = [IsAuthenticatedAndAdminPermissions]
    filter_backends = [SearchFilter]
    search_fields = ['business_element', 'role']
    http_method_names = ['get', 'post', 'patch', 'delete']
