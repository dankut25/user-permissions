from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .constants import API_VERSION
from .views import (
    BusinessElementsViewSet,
    logout_view,
    login_view,
    PermissionsViewSet,
    registration_view,
    RolesViewSet,
    soft_delete_view,
    user_update_view
)
from api.mock_views import mock_view


router_v1 = DefaultRouter()
router_v1.register(r'users/role', RolesViewSet)
router_v1.register(r'applications', BusinessElementsViewSet)
router_v1.register(r'permissions', PermissionsViewSet)

urlpatterns = [
    path(f'{API_VERSION}/auth/signup/', registration_view, name='register'),
    path(f'{API_VERSION}/auth/login/', login_view, name='login'),
    path(f'{API_VERSION}/auth/logout/', logout_view, name='logout'),
    path(
        f'{API_VERSION}/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(f'{API_VERSION}/users/me/', user_update_view, name='edit_user'),
    path(
        f'{API_VERSION}/users/me/delete/',
        soft_delete_view,
        name='soft_delete_user'
    ),
    path(f'{API_VERSION}/', include(router_v1.urls)),
    path(f'{API_VERSION}/mock-view/', mock_view, name='mock-view'),
]
