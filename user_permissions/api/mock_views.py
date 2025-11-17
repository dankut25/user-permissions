from http import HTTPStatus

from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes

from permissions.models import BusinessElements, Permissions
from api.mock_permissions import MockRolesPermissions


from unittest.mock import Mock
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status


User = get_user_model()


@api_view(['get', 'post', 'put', 'patch', 'delete'])
@permission_classes([MockRolesPermissions])
def mock_view(request):
    potential_objects = {'objects': ['obj1', 'obj2', 'obj3']}
    return HttpResponse(str(potential_objects), status=HTTPStatus.OK)
